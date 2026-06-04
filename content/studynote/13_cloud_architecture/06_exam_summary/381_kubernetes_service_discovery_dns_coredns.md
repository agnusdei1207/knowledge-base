---
title: "381. 쿠버네티스 서비스 디스커버리 DNS CoreDNS (Kubernetes Service Discovery DNS CoreDNS)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스 클러스터 내부의 동적 IP 할당 환경에서 서비스/파드 간 통신을 위해 CoreDNS(Go 기반 플러그인 아키텍처 DNS 서버, Caddy 임베디드)가 FQDN `<svc>.<ns>.svc.cluster.local` 규약으로 가상 IP(Service ClusterIP)와 엔드포인트(EndpointSlice)를 자동 매핑하는 인-클러스터 DNS 기반 서비스 디스커버리 메커니즘이다.
> 2. **가치**: 애플리케이션이 파드 재스케줄링·롤링 업데이트·장애 복구로 변동되는 IP를 추적할 필요 없이 DNS 질의 한 번으로 로드밸런싱된 엔드포인트에 도달할 수 있어(헤드리스 서비스 시 DNS RR 반환) 서비스 가용성 99.99% 환경에서 디스커버리 지연을 ~1ms(PodLocalCache 적용 시 P99 5ms 이하)로 단축하고, SRV 레코드를 통한 포트/우선순위 인지형 디스커버리까지 지원한다.
> 3. **판단 포인트**: CoreDNS 단일 인스턴스/단일 AZ 배치의 SPOF 위험과 `ndots:5`로 인한 후행 질의 비용, 클러스터 규모 1,000 노드·5,000 서비스 초과 시 발생하는 캐시 적중률 저하, 그리고 NodeLocal DNSCache·CoreDNS HPA·Split-horizon DNS 설계가 핵심 트레이드오프이며, 컨테이너 런타임(containerd/CRI-O)별 resolv.conf 동기화 차이까지 검토해야 한다.

---

## Ⅰ. 개요 및 필요성

쿠버네티스는 본질적으로 **선언형(Declarative)** 컨트롤 루프를 통해 파드 IP를 수시로 재할당한다. 기본 CNI(예: Calico VXLAN, Cilium eBPF, Flannel) 위에서 파드는 노드 장애·HPA·Deployment 롤아웃 시 평균 수십 초~수 분 주기로 IP가 변동되므로, 클라이언트가 IP를 하드코딩하면 24시간 내 접속 실패가 불가피하다. 전통적인 3-tier 환경에서는 F5 BIG-IP LTM, HAProxy, Consul Template, Netflix Eureka, Zookeeper 등이 디스커버리를 담당했으나, 컨테이너 오케스트레이터 표준인 쿠버네티스는 이를 **클러스터 네이티브 DNS**로 통합하여 별도의 에이전트 없이 kube-apiserver의 Watch 메커니즘을 통해 Service/EndpointSlice 객체를 실시간으로 반영한다.

초기 쿠버네티스(1.0~1.10)에서는 `kube-dns`(SkyDNS + dnsmasq + sidecar 3-tier 구조)을 사용했으나, kube-dns는 2018년경 Deprecate 결정 후 **1.13 버전부터 CoreDNS가 기본 DNS 플러그인으로 채택**되었다(GA 1.11, Default 1.13). CoreDNS는 단일 바이너리·단일 프로세스·플러그인 체인 구조로 메모리 풋프린트를 약 60% 절감(150MB -> 60MB)하고, dnsmasq의 race condition·메모리 누수 이슈를 해소했다.

**도입 전후 패러다임 비교**

| 구분 | 전통 디스커버리 (Eureka/Consul) | 쿠버네티스 CoreDNS |
|---|---|---|
| 등록 주체 | 애플리케이션 SDK가 Heartbeat | kubelet + kube-controller-manager가 자동 |
| 데이터 저장 | 별도 Key-Value 스토어(Raft) | in-memory + apiserver watch |
| 질의 프로토콜 | 전용 gRPC/REST API | 표준 DNS(UDP/TCP 53), mDNS |
| 헬스체크 | 클라이언트 Heartbeat | kube-proxy + EndpointSlice condition |
| 운영 복잡도 | 클러스터 별도 구성 | 컨트롤 플레인과 통합 |
| 확장성 | 수백~수천 인스턴스 | 수만 서비스/수십만 엔드포인트 |

```text
  +--------------------------------------------------------------------+
  |          쿠버네티스 클러스터 내부 DNS 질의 흐름 (요약)               |
  |                                                                    |
  |  [App Pod] ---(UDP 53, ndots:5)--► [CoreDNS Pod 10.96.0.10:53]    |
  |       |                                  |                         |
  |       | 1) /etc/resolv.conf                | 2) kubernetes 플러그인  |
  |       |    search: ns.svc.cluster.local    |    apiserver watch      |
  |       |    ndots:5                         |    Service/Endpoint    |
  |       |                                   v                        |
  |       |                            +--------------+                |
  |       |  3) 응답 (A, SRV, PTR) ◄----| Corefile     |                |
  |       |                            | plugin chain |                |
  |       |                            | (cache,      |                |
  |       |                            |  forward,    |                |
  |       |                            |  kubernetes) |                |
  |       |                            +--------------+                |
  |       v                                                           |
  |  [실제 Endpoint Pod IP로 직접 접속]                                  |
  |  (Service ClusterIP는 kube-proxy가 DNAT/SNAT 처리)                |
  +--------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: CoreDNS는 마치 **"학교 급식실의 식단표 게시판"**과 같다. 학년(class)·반(namespace)·날짜(svc.cluster.local)별로 매일 바뀌는 식단이 자동으로 반영되어, 학생(파드)은 "오늘 점심 뭐야?" 한 마디면 자기 자리에 배달받을 수 있다. 식단이 바뀌어도 학생은 식당 위치를 다시 외울 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CoreDNS는 **Caddy(HTTP/2 웹서버) 프레임워크를 차용**한 Go 기반 DNS 서버로, DNS 메시지 처리 파이프라인을 **플러그인 체인(Plugin Chain)**으로 구성한다. 각 플러그인은 `ServeDNS(ctx, zone, w, msg) (int, error)` 시그니처를 구현하며, 요청은 체인을 순차 통과하면서 forward, cache, rewrite, log 등의 액션이 적용된다.

### 1) CoreDNS 컨테이너 내부 아키텍처

```text
   +---------------------------------------------------------------------+
   |               CoreDNS Pod  (kube-system 네임스페이스)                 |
   |  +--------------------------------------------------------------+  |
   |  |                    Corefile (ConfigMap)                       |  |
   |  |  .:53 {                                                        |  |
   |  |      errors                                                   |  |
   |  |      health { lameduck 5s }                                   |  |
   |  |      ready                                                    |  |
   |  |      kubernetes cluster.local in-addr.arpa iparpa.168.96.in-  |  |
   |  |                addr.arpa { pods insecure fallthrough in-addr  |  |
   |  |                                  arpa iparpa.168.96.in-addr  |  |
   |  |                                  .arpa ttl 30                |  |
   |  |                  pods verified                               |  |
   |  |                  loadbalance                                  |  |
   |  |                  cache 30                                     |  |
   |  |                  loop                                         |  |
   |  |                  reload                                       |  |
   |  |                  forward . /etc/resolv.conf                   |  |
   |  |                  prometheus :9153                             |  |
   |  |      }                                                         |  |
   |  |  }                                                             |  |
   |  +--------------------------------------------------------------+  |
   |                            |                                        |
   |  +-------------------------v----------------------------------+    |
   |  |             Caddy DNS Server (go routine per query)          |    |
   |  |                                                              |    |
   |  |  Query --► [errors] --► [health] --► [ready]                |    |
   |  |           --► [kubernetes] ◄-- watch Service/EndpointSlice  |    |
   |  |           --► [loadbalance] (A 레코드 RR 셔플)              |    |
   |  |           --► [cache]  (Lmax=1000, TTL=30s 기본)            |    |
   |  |           --► [loop]   (forward loop 감지)                  |    |
   |  |           --► [forward] (외부 도메인 -> upstream)             |    |
   |  |           --► [prometheus] :9153/metrics                     |    |
   |  |           --► [log] (query log)                              |    |
   |  +--------------------------------------------------------------+    |
   |                                                                     |
   |  kube-dns Service  (10.96.0.10 ClusterIP)                            |
   |   +-- EndpointSlice: replicas=2 (HA), lameduck 5s                    |
   +---------------------------------------------------------------------+
```

### 2) DNS 질의 처리 시퀀스

```text
  Application Pod                      CoreDNS                          kube-apiserver
  --------------                       -------                          --------------
  1) getent hosts my-svc.default.svc
     -> libc (glibc/musl)                    |
     -> nsswitch.conf (files dns)            |
  2) name resolution to 10.96.x.x:53        |
     +------------------------+             |
     | Pod /etc/resolv.conf:  |             |
     | nameserver 10.96.0.10  |             |
     | search default.svc.    |             |
     |  cluster.local svc.    |             |
     |  cluster.local cluster.local        |
     | ndots:5                |             |
     | options ndots:5 ...    |             |
     +------------------------+             |
  3) UDP 53: A? my-svc.default.svc  --------►|
  4) ndots:5 이므로 search domain 추가 시도  |
     - my-svc (실패)                        |
     - my-svc.default.svc (실패)            |
     - my-svc.default.svc.cluster.local (성공)|
  5)                              kubernetes 플러그인:
                                     +- Service "my-svc" 검색
                                     +- Spec.ClusterIP = 10.96.45.123
                                     +- EndpointSlice 조회 (ready=true)
                                     +- Endpoints = [10.244.1.5, 10.244.2.7]
  6)                              loadbalance 플러그인:
                                     +- 순서 셔플 (라운드로빈)
  7)                              cache 플러그인:
                                     +- TTL=30초 동안 메모리 캐시
  8)                              ◄--- A record 응답
     A 10.96.45.123 (ClusterIP)            |
  9) 앱은 kube-proxy가 DNAT한 IP로 접속    |
     -> 10.244.1.5:80 (실제 파드)
```

### 3) 핵심 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Corefile (ConfigMap)** | DNS 서버 동작 정책 선언 | `.:53 { ... }` 블록 단위로 zone과 플러그인 정의, kubeadm/클라우드 프로바이더가 자동 주입, `kubectl edit cm coredns -n kube-system`으로 라이브 패치 |
| **kubernetes 플러그인** | Service/EndpointSlice -> DNS 레코드 변환 | apiserver에 `List+Watch`로 informer 캐시 구성, `cluster.local` zone 내 A/AAAA/SRV/PTR 생성, `pods verified` 시 파드 hostname/domain 검증, ttl 5~30s |
| **CoreDNS 컨테이너 (Deployment)** | DNS 쿼리 처리 | replicas=2 기본(HA), `--conf=/etc/coredns/Corefile`로 실행, 컨테이너당 ~30~80MB RSS, 단일 프로세스 모델 |
| **kube-dns Service (ClusterIP)** | 가상 서비스 엔드포인트 | 기본 IP `10.96.0.10`(kube-proxy의 `clusterIP` 정적 할당), 포트 53/UDP+TCP, 9153/TCP는 prometheus 메트릭 |
| **Pod resolv.conf 동기화** | 파드의 DNS 클라이언트 설정 | kubelet이 파드 생성 시 `--resolv-conf` 옵션으로 노드의 `/etc/resolv.conf`를 읽어 search 옵션·ndots 주입, `dnsPolicy`에 따라 4가지 모드 |
| **NodeLocal DNSCache (DaemonSet)** | 노드 단위 DNS 캐시 | 각 노드에 `node-cache` Pod 배치, CoreDNS로의 질의량을 80% 감소, nodelocaldns가 169.254.25.10 IP로 listen, P99 지연시간 5ms 이하 |
| **EndpointSlice (K8s 1.21+)** | 엔드포인트 샤딩 | Service당 100개 엔드포인트를 default로 분할, CoreDNS는 단일 slice watch가 아닌 multi-slice watch로 성능 개선 |

### 4) DNS 레코드 타입과 FQDN 명명 규칙

| 레코드 타입 | 생성 조건 | 예시 | TTL |
|---|---|---|---|
| **A (IPv4)** | 모든 Service ClusterIP | `my-svc.default.svc.cluster.local. 30 IN A 10.96.45.123` | 30s (변경 가능) |
| **AAAA (IPv6)** | Service에 `ipFamilies: [IPv6]` 또는 dual-stack | `my-svc.default.svc.cluster.local. 30 IN AAAA fd00::1` | 30s |
| **SRV** | Named Port 명시 시 자동 생성, `_port-name._proto.service.namespace.svc` | `_http._tcp.my-svc.default.svc.cluster.local. 30 IN SRV 0 50 80 10-96-45-123...` | 30s |
| **PTR** | Reverse lookup zone `in-addr.arpa`, `ipv6.arpa`, `iparpa.fd00::/8` | `10.96.45.123.in-addr.arpa. 30 IN PTR my-svc.default.svc.cluster.local.` | 30s |
| **Headless A** | `clusterIP: None` 인 Service | `my-svc.default.svc.cluster.local. 30 IN A 10.244.1.5` (실제 파드 IP, RR 셔플) | 30s |
| **Pod Hostname A** | `pods verified` / `pods insecure` 옵션 | `10-244-1-5.default.pod.cluster.local.` | 30s |

### 5) DNS Policy 및 ndots 메커니즘

| dnsPolicy | 동작 | 적용 대상 |
|---|---|---|
| **ClusterFirst** | 클러스터 내 DNS 우선, 외부 fallback | 일반 Pod (default) |
| **Default** | 노드 `/etc/resolv.conf` 그대로 사용 | hostNetwork Pod, 시스템 Pod |
| **ClusterFirstWithHostNet** | hostNetwork이면서 ClusterFirst | kube-proxy, CNI DaemonSet 등 |
| **None** | dnsConfig로 완전 커스터마이즈 | 게임 서버, 외부 DNS 전용 |

**ndots:5 알고리즘**: 검색할 도메인 이름에 점(`.`)이 5개 미만이면 search 도메인을 차례로 append. `
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 381 / 800

<- **이전**: [380. 쿠버네티스 인그레스 컨트롤러 로드 밸런싱](/studynote/13_cloud_architecture/06_exam_summary/380_kubernetes_ingress_controller_load_balancing/)
**다음**: [382. 헬름 차트 패키지 관리 배포 자동화](/studynote/13_cloud_architecture/06_exam_summary/382_helm_chart_package_management_deployment/) ->

---
