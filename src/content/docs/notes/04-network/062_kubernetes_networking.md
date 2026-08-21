---
sidebar:
  order: 62
  label: "062. 쿠버네티스 네트워킹 - CNI•Ingress"
  badge:
    text: "기출 · 50%"
    variant: note
title: "쿠버네티스 컨테이너 네트워킹 : CNI, Service, Ingress 및 NetworkPolicy"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 62
extra:
  question_no: "062"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "CNI 플러그인(Calico, Cilium), Service VIP(kube-proxy/eBPF), Ingress 및 Gateway API"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **쿠버네티스 네트워킹(Kubernetes Networking)**: 모든 파드(Pod)가 NAT(Network Address Translation) 없이 고유한 IP를 부여받아 클러스터 전역에서 상호 1:1 직접 통신할 수 있도록 규정한 평면 네트워크(Flat Network) 모델.
- **컨테이너 네트워크 인터페이스(Container Network Interface, CNI)**: 쿠버네티스 런타임(Kubelet)이 파드의 생성 및 삭제 시 가상 네트워크 인터페이스(veth)를 동적으로 할당하고 IP 라우팅을 구성하는 표준 플러그인 규격.
- **인그레스(Ingress) 및 게이트웨이 API**: 클러스터 외부의 HTTP/HTTPS 트래픽을 호스트명(Host) 및 URL 경로(Path) 기반으로 서비스(Service)에 라우팅하는 L7 프록시 계층.

</details>

- 정의/개념: 파드 간 무손실 직접 통신을 위한 **CNI(Container Network Interface)**, 파드의 동적 IP 변경을 추상화하는 **서비스(Service VIP)**, 외부 L7 라우팅을 담당하는 **인그레스(Ingress)** 및 L3/L4 보안 격리를 집행하는 **NetworkPolicy** 로 구성된 클라우드 네이티브 네트워크 아키텍처
- 배경/필요성: 동적으로 생성·소멸하는 대규모 컨테이너 환경에서 포트 충돌을 방지하고, 고정 엔드포인트를 제공하며 마이크로서비스 간 안전한 제로 트러스트 통신을 달성할 요구

#### 한줄 요약
- CNI 평면 네트워크, Service VIP 로드밸런싱, Ingress L7 라우팅, NetworkPolicy 보안을 통합 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **서비스 가상 IP(Service VIP)**: 여러 파드로 구성된 워크로드의 단일 진입점 역할을 수행하며, kube-proxy(iptables/IPVS) 또는 eBPF를 통해 활성 파드로 L4 로드밸런싱을 수행하는 불변 가상 IP.
- **네트워크 정책(NetworkPolicy)**: 레이블 셀렉터(Label Selector)를 기반으로 파드 간 인그레스(Ingress) 및 이그레스(Egress) 트래픽을 화이트리스트 방식으로 격리 통제하는 가상 방화벽 리소스.

</details>

- **모든 파드 간 NAT-less 평면 통신**: 노드 위치와 무관하게 모든 파드가 자신의 고유 IP로 타 노드의 파드와 포트 변환 없이 직접 통신
- **서비스 디스커버리 및 가상 로드밸런싱**: CoreDNS와 연계하여 서비스 도메인 이름을 VIP로 해석하고, 백엔드 파드로 균등 트래픽 분배
- **커널 레벨 eBPF 가속 (Cilium CNI)**: 전통적인 iptables의 $O(N)$ 순차 룩업 병목을 극복하고, eBPF 맵을 통한 $O(1)$ 초고속 커널 패킷 포워딩 실현

#### 한줄 요약
- NAT 없는 평면 통신, Service VIP 기반 로드밸런싱, eBPF 커널 가속 및 NetworkPolicy 제로 트러스트 격리를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **게이트웨이 API(Gateway API)**: 기존 Ingress의 벤더별 어노테이션(Annotation) 파편화 한계를 극복하고, 인프라 관리자(Gateway)와 앱 개발자(HTTPRoute)의 권한을 명확히 분리한 차세대 L4~L7 라우팅 표준.

</details>

```text
[ 클러스터 외부 사용자 (HTTP / HTTPS) ]
   │
   ▼ (외부 DNS ➔ Ingress Controller / Gateway API)
[ Ingress Controller (Envoy / Nginx) ] ── (L7 호스트 / 경로 분기 및 TLS 종단)
   │
   ▼ (Service VIP 라우팅 / kube-proxy or eBPF)
[ Service (ClusterIP / LoadBalancer) ]
   │
   ▼ (NetworkPolicy 화이트리스트 접근 제어 검증)
[ CNI 네트워크 패브릭 (Calico / Cilium eBPF) ]
   ├───────────────────────────────┬───────────────────────────────┐
   ▼ (Node 1)                      ▼ (Node 2)                      ▼ (Node 3)
[ Pod A (veth0) ]               [ Pod B (veth0) ]               [ Pod C (veth0) ]
```

선의 의미: 외부 트래픽이 Ingress에서 L7 라우팅된 후 Service VIP를 거쳐 NetworkPolicy 검증을 통과하고 CNI 패브릭을 통해 최종 대상 파드로 전달되는 계층 흐름

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **Ingress / Gateway API** | 클러스터 외부 L7 트래픽 수용, TLS 종단(Offload), 경로 기반 라우팅 | L7 프록시 |
| **Service (ClusterIP/NodePort)** | 파드 그룹에 고정 VIP를 부여하고 백엔드 엔드포인트(EndpointSlice)로 부하 분산 | L4 가상 로드밸런서 |
| **NetworkPolicy** | 네임스페이스 및 파드 레이블 기반의 인그레스/이그레스 L3/L4 패킷 필터링 | 선언적 보안 정책 |
| **CNI 플러그인** | veth 페어 생성, IPAM(IP 주소 할당), 노드 간 오버레이(VXLAN/Geneve) 또는 BGP 라우팅 | Calico, Cilium, Flannel |
| **eBPF 커널 엔진** | iptables를 대체하여 리눅스 커널 레벨에서 소켓 계층 직결 고속 포워딩 수행 | Cilium BPF Datapath |

#### 한줄 요약
- Ingress, Service, NetworkPolicy, CNI, eBPF 엔진이 결합하여 쿠버네티스 네트워킹을 완성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **엔드포인트 슬라이스(EndpointSlice)**: 서비스에 속한 백엔드 파드들의 실시간 IP/포트 상태를 추적하고, 대규모 클러스터에서 etcd 부하를 줄이기 위해 파드 목록을 분할 관리하는 리소스.
- **준비성 프로브(Readiness Probe)**: 컨테이너 내부 애플리케이션이 실제 트래픽을 수신할 준비가 완료되었는지를 검증하여 정상 판정 시에만 Service VIP 엔드포인트에 IP를 등록하는 메커니즘.

</details>

```text
1. 외부 클라이언트가 `api.domain.com/user`로 HTTPS 요청 전송 ➔ Ingress 공인 IP 수신
            │
            ▼
2. Ingress Controller가 TLS 복호화 및 Host/Path 룰 파싱 ➔ 대상 Service(User-Service) 매핑
            │
            ▼
3. Service가 EndpointSlice에서 Readiness Probe를 통과한 정상 파드(Pod IP) 목록 조회
            │
            ▼
4. kube-proxy(IPVS) 또는 eBPF 맵이 대상 Pod IP로 패킷 헤더 변환(DNAT) 및 부하 분산
            │
            ▼
5. CNI 패브릭을 거쳐 NetworkPolicy 검증 후 대상 노드의 veth 인터페이스로 패킷 주입
```

**동작 원리**

1. **외부 인입 및 L7 처리**: Ingress가 단일 로드밸런서 IP에서 여러 도메인 요청을 라우팅
2. **서비스 디스커버리**: EndpointSlice 컨트롤러가 파드 헬스체크 결과를 반영하여 유효 파드 풀 유지
3. **가상 로드밸런싱**: 커널 eBPF/IPVS 맵이 ClusterIP를 목적지 Pod IP로 1:1 주소 변환
4. **보안 인가**: CNI 에이전트가 송수신 파드의 레이블을 검증하여 허용된 트래픽만 통과
5. **로컬 전달**: 노드 내부 veth pair 및 네트워크 네임스페이스를 통해 컨테이너 소켓으로 패킷 전달

#### 한줄 요약
- Ingress L7 파싱, Service VIP 매핑, EndpointSlice 유효성 검증, eBPF 변환, CNI 전달 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **오버레이 CNI vs 언더레이/BGP CNI**: 패킷을 VXLAN/Geneve로 캡슐화하여 노드 간 전달하는 방식과, 물리 네트워크 스위치와 BGP 피어링을 맺어 파드 IP를 네이티브 라우팅하는 방식.

</details>

| 비교 항목 | Flannel CNI (기본형) | Calico CNI (보안/BGP) | Cilium CNI (차세대 eBPF) |
|:---|:---|:---|:---|
| **데이터 평면 기술** | Linux Bridge / VXLAN 오버레이 | iptables / Linux Routing (BGP) | **eBPF (Extended BPF 커널 가속)** |
| **NetworkPolicy 지원** | **미지원 (보안 통제 불가)** | **지원 (강력한 L3~L4 방화벽)** | **지원 (L3~L7 API 단위 심층 제어)** |
| **성능 확장성** | 소규모 적합 (캡슐화 오버헤드) | 중대규모 적합 (BGP 네이티브 전송) | **초대규모 고성능 ($O(1)$ BPF Map)** |
| **서비스 프록시 구현** | 표준 kube-proxy (iptables) | 표준 kube-proxy / eBPF 모드 | **kube-proxy 완전 대체 (eBPF Host-Routing)** |
| **서비스 메시 통합** | 별도 사이드카 프록시 필수 | 별도 사이드카 프록시 필수 | **사이드카 없는(Sidecarless) 서비스 메시** |

#### 한줄 요약
- Flannel은 단순 오버레이, Calico는 BGP/NetworkPolicy, Cilium은 eBPF 기반 고성능/L7 보안 CNI이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CoreDNS 지연 및 Conntrack 고갈**: 대규모 파드가 외부 도메인 질의 시 iptables conntrack 테이블 경합으로 인해 5초 타임아웃 지연(UDP 레이스 컨디션)이 발생하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 컨테이너 부팅 중 미준비 상태에서 트래픽 유입으로 인한 503/502 오류 발생 | **Readiness Probe(준비성 검사)** 및 `initialDelaySeconds` 정밀 구성 | 미준비 파드 트래픽 유입 차단 및 무중단 배포 보증 |
| 대규모 클러스터에서 수만 개 파드 생성 시 iptables 룰 순차 룩업으로 CPU 과부하 | iptables를 전면 배제하고 **eBPF 기반 Cilium CNI** 도입 | 룰 개수 무관 $O(1)$ 초고속 패킷 포워딩 및 CPU 자원 70% 절감 |
| CoreDNS 질의 폭증 및 conntrack 테이블 경합으로 인한 간헐적 5초 DNS 지연 | 각 노드에 **NodeLocal DNSCache** 데몬셋 배포 및 TCP DNS 활성화 | 로컬 캐싱을 통한 DNS 응답 시간 1ms 단축 및 conntrack 고갈 방지 |

#### 한줄 요약
- Readiness Probe로 503을 방지하고, Cilium eBPF로 성능을 가속하며, NodeLocal DNSCache로 DNS 지연을 차단한다.

## Ⅶ. 결론

- 클라우드 네이티브 환경의 확장성과 보안성을 달성하기 위해 **쿠버네티스 표준 네트워킹 아키텍처**를 구축하되, 대규모 엔터프라이즈 환경에서는 **eBPF 기반 Cilium CNI**, **Gateway API 표준**, **엄격한 NetworkPolicy 화이트리스트 보안**, **NodeLocal DNSCache**를 통합 적용하여 고성능·고보안 컨테이너 인프라를 완성

#### 한줄 요약
- CNI, Service, Gateway API 및 eBPF 가속을 결합하여 고성능 클라우드 네이티브 네트워크를 구현한다.
