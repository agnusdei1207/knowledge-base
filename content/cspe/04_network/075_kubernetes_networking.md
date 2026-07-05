---
title: "쿠버네티스 네트워킹 — CNI·Ingress (Kubernetes Networking)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 75
---

# 📖 【암기용】 개념 완전 이해

> 목적: 쿠버네티스 네트워킹을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Pod, Service, Ingress가 클러스터 내부·외부 통신을 제공하는 컨테이너 네트워크 구조
- **왜 필요한가**: Pod는 생성·삭제 때마다 IP가 바뀐다. 쿠버네티스는 CNI로 Pod IP를 할당하고, Service로 고정 접근점을 만들며, Ingress로 HTTP/HTTPS 외부 유입을 제어한다.
- **핵심 직관**: Pod는 이동하는 좌석, Service는 고정 내선번호, Ingress는 건물 정문 안내 데스크와 같다.

## 깊이 이해
- **배경·문제의식**: 컨테이너는 초 단위로 배포되고 노드 간 이동한다. 전통 서버 IP 중심 접근은 Pod 생명주기와 맞지 않으므로, 클러스터는 IPAM, 라우팅, 로드밸런싱, 정책 통제를 자동 제공해야 한다.
- **작동 원리**: CNI 플러그인은 Pod 생성 시 veth, IPAM, route, overlay/underlay 연결을 구성한다. Service는 ClusterIP와 kube-proxy 또는 eBPF로 로드밸런싱한다. Ingress Controller는 L7 규칙을 Envoy, NGINX, HAProxy 등으로 반영한다.
- **비유**: 호텔 객실 번호는 매일 바뀌지만, 프런트 대표번호와 예약 시스템은 동일하게 유지되어 투숙객을 정확한 객실로 안내하는 구조이다.
- **구체 예시**: `frontend.default.svc.cluster.local`은 ClusterIP로 해석되고, kube-proxy iptables/IPVS 또는 Cilium eBPF가 실제 Pod IP 10.244.x.x로 분산한다. Ingress는 `/api` 경로를 backend Service로 라우팅한다.
- **흔한 오해·주의점**: Service와 Ingress는 같은 계층이 아니다. Service는 클러스터 내부 L3/L4 가상 IP, Ingress는 HTTP/HTTPS L7 라우팅 규칙이다.

## 연결 개념
- CNI — Pod 네트워크 플러그인 표준
- Service Mesh — Pod 간 L7 통신 정책과 관측성 확장
- NetworkPolicy — namespace와 label 기반 Pod 통신 제어

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Pod IP, Service VIP, Ingress L7 라우팅, NetworkPolicy를 계층별로 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes Networking은 CNI 기반 Pod 네트워크, Service 기반 L4 추상화, Ingress 기반 L7 외부 유입 제어로 구성된다.
> 2. **가치**: Pod IP 변동과 노드 이동을 Service DNS, ClusterIP, EndpointSlice, Ingress Controller로 추상화한다.
> 3. **판단 포인트**: CNI 방식(overlay/underlay/eBPF), kube-proxy 모드, Ingress Controller, NetworkPolicy 적용 범위를 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| K8s 네트워크 계층 이해 확인 | Pod, CNI, Service, EndpointSlice, Ingress | Service와 Ingress를 동일 기능으로 서술 |
| 운영 설계 판단 | overlay vs underlay, iptables/IPVS/eBPF, DNS | Pod IP 직접 접근 중심 설명 |
| 보안·관측 통제 | NetworkPolicy, mTLS 연계, L7 log, flow log | namespace 격리와 네트워크 격리 혼동 |

> 요약: 이 문제는 컨테이너 네트워크를 Pod 생성, 내부 서비스 발견, 외부 유입, 정책 통제 흐름으로 설명해야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **쿠버네티스 네트워킹 — CNI·Ingress** | 쿠버네티스 네트워킹 — CNI·Ingress (Kubernetes Networking)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: Pod·Service 중심 클러스터 통신
- 배경: Pod는 짧은 수명과 동적 IP를 가지므로 서버 IP 고정 운영 방식으로 서비스 발견과 접근 제어를 처리하기 어렵다.
- 필요성: CNI, Service, Ingress, NetworkPolicy를 결합해 컨테이너 생명주기와 분리된 통신 경로를 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Pod Network CNI -> Service ClusterIP/EndpointSlice -> kube-proxy/eBPF
-> Ingress Controller -> External Client
                 +-> CoreDNS
                 +-> NetworkPolicy
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| CNI | Pod IP 할당과 veth/route 구성 | Calico, Cilium, Flannel |
| Service | Pod 집합에 고정 VIP 제공 | ClusterIP, NodePort, LoadBalancer |
| EndpointSlice | Service 대상 Pod 목록 관리 | scale 기준 endpoint 분할 |
| Ingress | HTTP/HTTPS L7 라우팅 규칙 | NGINX, Envoy, Gateway API |
| NetworkPolicy | Pod 간 허용 통신 정의 | label selector, namespace selector |

> 요약: K8s 네트워크는 CNI가 Pod 연결을 만들고, Service와 Ingress가 내부·외부 접근을 추상화한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod Create -> CNI ADD -> Pod IP/Route Setup -> Service DNS Query
-> ClusterIP Load Balancing -> Endpoint Pod Delivery
-> Ingress L7 Routing for External Traffic
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | kubelet이 CNI ADD 호출 | Pod IP allocated |
| 2 | CoreDNS가 Service FQDN을 ClusterIP로 응답 | DNS latency p95 50ms 이하 |
| 3 | kube-proxy/eBPF가 ClusterIP를 Pod IP로 변환 | endpoint hit, conntrack 상태 |
| 4 | Ingress Controller가 Host/Path를 Service로 라우팅 | HTTP 2xx/5xx, TLS cert |
| 5 | NetworkPolicy가 허용·차단 정책 적용 | denied flow count, policy audit |

> 요약: Pod 통신은 CNI로 네트워크를 만들고, DNS와 Service로 대상 Pod를 찾으며, Ingress는 외부 HTTP 경로를 내부 Service로 연결한다.

---

## Ⅳ. 특징

| 구분 | 전통 서버 네트워크 | Kubernetes Networking | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 주소 | 서버 고정 IP | Pod 동적 IP + Service VIP | Pod churn, EndpointSlice 수 |
| 로드밸런싱 | L4/L7 장비 중심 | kube-proxy IPVS/eBPF, Ingress | p95 latency, conntrack 사용률 |
| 정책 | VLAN/ACL 중심 | NetworkPolicy label 기반 | default deny, allowed flow |
| 확장 | 장비 설정 변경 | CNI와 Controller 자동 반영 | node/pod scale, route count |

> 요약: K8s 네트워킹은 IP 고정이 아니라 Service 추상화와 label 정책으로 컨테이너 이동성을 처리한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| CNI 방식 | overlay VXLAN | underlay BGP/eBPF | MTU, 라우트 규모, 지연 요구 |
| Service 처리 | iptables | IPVS/eBPF | Service 1,000개 이상, conntrack 압박 |
| 외부 유입 | NodePort | Ingress/Gateway API | L7 TLS, path routing, WAF 연계 |

> 요약: CNI와 Service 구현은 클러스터 규모, MTU, L7 정책, 관측성 요구로 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| DNS 병목 | CoreDNS replica 부족 | HPA, cache, node-local DNS | DNS p95 50ms 이하 |
| MTU 단편화 | overlay 헤더 증가 | MTU 1450/1550 설계, PMTUD | fragmentation count 0 |
| 정책 누락 | default allow 운영 | default deny, namespace baseline | unauthorized flow 0건 |

> 요약: K8s 네트워크 장애는 DNS, MTU, 정책 누락에서 자주 발생하므로 사전 점검 지표가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Service 지연 | p95 50ms~100ms 이하 | Prometheus, eBPF tracing |
| 패킷 손실 | pod-to-pod loss 0.1% 이하 | synthetic probe |
| 정책 준수 | NetworkPolicy audit pass 100% | flow log, policy test |

> 요약: 운영 판단은 Pod 연결 성공 여부보다 DNS 지연, 패킷 손실, 정책 준수율로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. CNI는 클러스터 규모와 네트워크 요구에 따라 Calico BGP, Cilium eBPF, Flannel VXLAN 중 선택하고 MTU 값을 표준화함
2. Service는 ClusterIP와 EndpointSlice, CoreDNS HPA, kube-proxy IPVS/eBPF 모드를 점검해 1,000개 이상 Service 규모를 대비함
3. Ingress는 TLS, path routing, rate limit, WAF 연계를 적용하고 NetworkPolicy는 default deny를 namespace baseline으로 설정함

**결론 (2줄):**
- 기술사 판단: Pod 동적성과 L7 유입이 핵심이면 CNI, Service, Ingress, NetworkPolicy를 하나의 통신 경로로 설계해야 함
- 향후 방향: Gateway API, eBPF CNI, Service Mesh 연계로 L4/L7 정책과 관측성이 통합되는 방향임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | Pod 생성, Service DNS, Ingress 라우팅 흐름 | 전통 서버 네트워크 대비 추상화 |
| 요구사항 명시형 | "설계하시오", "방안을 제시하시오", "운영하시오" | CNI 선택, DNS, NetworkPolicy 적용 절차 | MTU, p95 latency, policy audit 지표 |

> 요약: 설명형은 구성 계층, 설계형은 CNI·Ingress·정책의 선택 기준과 검증 지표를 중심으로 작성한다.
