---
title: "483. IPv6 전환 클라우드 듀얼 스택 (IPv6 Transition Cloud Dual Stack)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IPv6 전환 클라우드 듀얼 스택은 클라우드 인프라(VPC/VNet/VPC) 내에서 IPv4와 IPv6를 동시 운용하는 아키텍처로, AWS Egress-only Internet Gateway, Azure NAT Gateway, GCP Cloud NAT의 IPv6 지원, Kubernetes Dual-stack CNI(Cilium, Calico), Istio mTLS Dual-listener 등 클라우드 네이티브 계층 전반에서 양 프로토콜을 Native하게 처리하는 통합 라우팅 및 주소 정책 체계이다.
> 2. **가치**: IPv4 주소 고갈(ARIN/RIPE NCC의 /8 할당 종료), 5G/IoT 디바이스 폭증으로 인한 엔드포인트 확장성 한계, RFC 8305 Happy Eyeballs 기반의 Dual-stack Latency Advantage(연결 수립 시간 평균 30~45% 단축), 클라우드 egress 비용 절감(IPv6 egress는 AWS 기준 50% 저렴), 그리고 Zero-trust 보안 모델의 양방향 검증 구현을 가능케 한다.
> 3. **판단 포인트**: 듀얼 스택의 운영 복잡도(주소 추적, ACL 2배 관리, DNS A/AAAA 분리 운영)와 이기종 클라우드 간의 라우팅 정책 표준화 부재, IPv4/IPv6 헤더 변환 시 MTU/Fragmentation 이슈(PMTUD 경로 차이), 그리고 IPv6 Extension Header 기반의 침입탐지 회피(SIEM 룰셋 2배 작업)라는 세 가지 핵심 트레이드오프를 어떻게 설계 단계에서 절충할지가 기술사의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

IPv6 전환은 단순한 주소 체계 확장이 아닌, 클라우드 시대의 **네트워크 경계(Perimeter) 재정의** 문제이다. 2023년 RIPE NCC의 마지막 /8 블록 할당, 2024년 APNIC의 신규 IPv4 할당 사실상 중단, 그리고 IETF가 IPv4를 "legacy address"로 분류하는 흐름은 클라우드 아키텍트의 필수 역량을 "단일 프로토콜 최적화"에서 **"이중 프로토콜 공존 운영(Coexistence Operation)"** 으로 전환시켰다.

특히 클라우드 환경은 엔터프라이즈 데이터센터와 달리 **탄력적 스케일링, 멀티 리전, 멀티 VPC 피어링, 그리고 매니지드 서비스 종속성**이라는 4가지 특이점이 있어, 온프레미스에서 사용하던 6rd나 DS-Lite 같은 CPE 기반 터널링 기법을 그대로 적용할 수 없다. 클라우드에서는 **가상 라우터(VRF), Transit Gateway, SD-WAN Edge, 그리고 CNI Plugin 수준에서의 이중 처리**가 요구된다.

```text
+----------------------------------------------------------------------+
|           IPv6 전환 클라우드 듀얼 스택의 패러다임 비교               |
+----------------------------------------------------------------------+
|                                                                      |
| [Legacy Paradigm - IPv4 Single Stack]                                |
|                                                                      |
|   Internet --IPv4--> NAT Gateway --> Private VPC (10.0.0.0/16)      |
|                                          |                            |
|                                          +-> EC2/VM (IPv4 only)      |
|                                                                      |
|   문제점: 주소 고갈, 1:1 NAT 비용, EIP 부족, 로그 4-tuple 제한       |
|                                                                      |
| -------------------------------------------------------------------- |
|                                                                      |
| [Modern Paradigm - Cloud Dual Stack + IPv6 Native]                   |
|                                                                      |
|   Internet --+--IPv4--> NAT GW --+                                  |
|              |                    +--> Transit GW --> VPC Dual      |
|              |                    |      |                            |
|              +--IPv6--> EIGW -----+      +-> Subnet1: 10.0.1.0/24    |
|                                          |    + 2600:1f01::/64        |
|                                          +-> Subnet2: 10.0.2.0/24    |
|                                          |    + 2600:1f02::/64        |
|                                          +-> EKS/AKS Pod (Dual CIDR) |
|                                                                      |
|   효과: EIP-free, Path MTU 1500 보존, End-to-End 암호화(WAM/EH)      |
+----------------------------------------------------------------------+
```

기존 IPv4 단일 스택 운영은 **NAT444, CGN(Carrier-Grade NAT), Stateful Firewall의 3중 의존**으로 인해 클라우드 워크로드의 east-west 트래픽 가시성을 저해하고, 컨테이너 오케스트레이션(Kubernetes Service Mesh)의 mTLS 인증서 발급을 IPv4 소스 NAT 한정으로 강제하는 한계를 노출했다. 듀얼 스택은 이를 **L3/L4 헤더 양방향 검증 + SLAAC Stateless Addressing + Privacy Extension(RFC 4941)** 으로 해결한다.

- **📢 섹션 요약 비유**: IPv4 단일 스택은 "한 국어만 쓰는 호텔"이고, 듀얼 스택은 "체크인부터 룸서비스까지 한국어·영어·일본어 메뉴를 동시 제공하는 글로벌 호텔"입니다. 손님(트래픽)은 자국어로 즉시 통하고, 호텔은 손님의 신분을 양방향으로 검증할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 듀얼 스택의 아키텍처는 **7개 계층(Underlay/Overlay/Subnet/Service/Pod/Service-Mesh/Egress)** 에서 각각 다른 메커니즘으로 동작한다. 핵심은 **Dual CIDR Allocation, Multi-protocol Routing, Happy Eyeballs Connection, 그리고 Dual DNS Resolution**의 4대 원리다.

```text
+----------------------------------------------------------------------+
|         Cloud Dual Stack 7-Layer Reference Architecture              |
+----------------------------------------------------------------------+
|                                                                      |
|  [Layer 1: Internet Edge]                                            |
|    +------------+    +------------+    +------------+                |
|    |  IPv4 IGW  |    |  IPv6 IGW  |    |   CDN/Edge |                |
|    | (Anycast)  |    |  (Egress-  |    |  CloudFront|                |
|    +-----+------+    |   only IGW)|    | /Azure CDN |                |
|          |           +-----+------+    +-----+------+                |
|          |                 |                  |                       |
|  [Layer 2: Transit / Routing Plane]                                  |
|    +-----+-----------------+------------------+-----+                |
|    |  Transit GW  /  Virtual WAN Hub  /  NCC Spoke    |                |
|    |  - BGP IPv4 Unicast + Labeled IPv6 Unicast -    |                |
|    |  - Route Reflector: 2개 AS-Path 정책 동시 유지 -|                |
|    +---------------------+---------------------------+                |
|                          |                                            |
|  [Layer 3: VPC/VNet Dual CIDR]                                       |
|    +---------------------+---------------------------+                |
|    |  VPC: 10.0.0.0/16  +  2600:1f00:4860::/56       |                |
|    |  +- Subnet A: 10.0.1.0/24 + 2600:1f01:4860::/64 |                |
|    |  +- Subnet B: 10.0.2.0/24 + 2600:1f02:4860::/64 |                |
|    |  +- Route Table: IPv4 0.0.0.0/0 -> NAT GW         |                |
|    |                 IPv6 ::/0      -> EIGW            |                |
|    +---------------------+---------------------------+                |
|                          |                                            |
|  [Layer 4: Compute - VM/Bare-metal]                                  |
|    +---------------------+---------------------------+                |
|    |  ENI/VNIC: Primary IPv4 + Multiple IPv6 /128    |                |
|    |  - Privacy Extension(RFC 4941) Stable SLAAC      |                |
|    |  - DHCPv6-PD: 멀티 서브넷 /60, /56 위임          |                |
|    +---------------------+---------------------------+                |
|                          |                                            |
|  [Layer 5: Container Orchestration]                                   |
|    +---------------------+---------------------------+                |
|    |  K8s:  --feature-gates=IPv6DualStack=true        |                |
|    |       --ip-family=IPv4,IPv6                       |                |
|    |  CNI: Cilium DualStack (--ipv4-range, --ipv6-range)|             |
|    |       Calico IPAM: IPv6 pool /48                 |                |
|    |  Pod CIDR:  fd00::/64 per namespace              |                |
|    +---------------------+---------------------------+                |
|                          |                                            |
|  [Layer 6: Service Mesh / API Gateway]                               |
|    +---------------------+---------------------------+                |
|    |  Istio:  Dual Listener (0.0.0.0:443, [::]:443)  |                |
|    |  Envoy:  Happy Eyeballs v3 (RFC 8305)            |                |
|    |  mTLS:  SPIFFE ID = spiffe://trust/domain/ipv4   |                |
|    |         spiffe://trust/domain/ipv6                |                |
|    +---------------------+---------------------------+                |
|                          |                                            |
|  [Layer 7: Egress / Observability]                                   |
|    +---------------------+---------------------------+                |
|    |  NAT64 (RFC 6146) + DNS64 (RFC 6147)             |                |
|    |  Cloud NAT IPv6 egress (GCP), NAT GW IPv6 (Azure)|                |
|    |  VPC Flow Logs v6 + v4, ALB Access Log dual      |                |
|    +--------------------------------------------------+                |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **VPC Dual CIDR Block** | 클라우드 가상 네트워크의 이중 주소 공간 | AWS는 Primary + 4개의 Secondary IPv4 CIDR(총 5개, RFC 1918 범위), IPv6는 /56 할당 후 /64 서브넷 분할(총 256 서브넷). Azure VNet은 IPv4/IPv6를 주소 공간에 동시 등록, GCP VPC는 IPv6는 별도 Internal/External 구분(Internal은 /48, External은 /48). |
| **Internet Gateway / Egress-only IGW** | 양방향/단방향 외부 연결 종단점 | AWS EIGW는 IPv6 **stateful outbound only** (인바운드 불가, NAT 역방향 안 함), IGW는 v4+v6 stateful. Azure Basic SKU LB는 IPv6 frontend 미지원, Standard SKU부터 지원. |
| **NAT Gateway (IPv6-aware)** | IPv4 아웃바운드 SNAT + IPv6 옵션 처리 | AWS NAT GW는 v4만 처리, IPv6는 EIGW 경유. Azure NAT GW는 v4/v6 동시 처리(2023 GA), GCP Cloud NAT는 v6 egress를 NAT66 형태로 처리하며 /64 prefix 단위 SNAT. |
| **Kubernetes CNI (Dual-stack)** | Pod의 양 프로토콜 IP 할당 및 라우팅 | Cilium은 eBPF datapath에서 v4/v6를 분리된 map(bpf_lxc, bpf_lxc6)에 저장, Calico v3.21+는 BGP Peering으로 v6 NLRI advertise, Flannel은 host-gw/vxlan 모두 dual 지원. |
| **Service Mesh Dual Listener** | L7 프록시의 양 프로토콜 동시 처리 | Istio는 iptables로 IPv4/IPv6 트래픽을 모두 15006 inbound, 15001 outbound로 redirect, Envoy Happy Eyeballs는 `getaddrinfo` 후 `connect()` 시 양쪽 family를 race condition으로 연결(첫 성공 시 나머지 close). |
| **DNS Resolver (Dual A/AAAA)** | FQDN의 이중 레코드 반환 정책 | Route 53 Resolver는 A+AAAA 동시 반환(기본), Azure DNS Private Resolver는 response policy로 A-only 강제 가능, BIND 9.18+는 `dns64` 옵션으로 RFC 6147 synthetic AAAA 자동 생성. |
| **Observability Stack (Dual Flow)** | 네트워크 가시성 및 SIEM 연동 | VPC Flow Logs는 v4/v6 분리 로그(`srcaddr`, `dstaddr` v6 컬럼), CloudTrail는 `vpcEndpointId`에 v6 포함, Splunk/ELK는 `ipfamily` 필드 인덱싱 필수. |

**핵심 알고리즘: Happy Eyeballs v2 (RFC 8305)**

듀얼 스택 환경에서 클라이언트(브라우저, curl, Envoy 등)는 다음의 **3-Phase Race**를 수행한다:

1. **Resolution Phase**: `getaddrinfo("api.example.com")` -> IPv4 주소 리스트와 IPv6 주소 리스트를 별도 배열로 수신
2. **Sort Phase**: RFC 6724 알고리즘으로 양 리스트를 **Policy Table**(12개 rule: Loopback > Global > Site-local > ... ) 기반 정렬. 같은 Prefix Length면 IPv6가 우선(Site/Organization Local이 아닌 Global Unicast일 때).
3. **Race Phase**: 첫 번째 IPv6 주소로 `connect()` 시도(300ms timeout), 그 사이 50ms 간격으로 IPv4 주소도 `connect()` 시도. **먼저 connect()가 성공한 family의 socket을 사용**하고 나머지는 RST로 폐기.

이 메커니즘이 주는 핵심 통찰은 **"IPv6가 다운되더라도 IPv4 fallback이 300ms 이내에 보장된다"**는 점이다. 즉, 듀얼 스택의 **이중성(Dual-homing)**은 단일 장애점이 아니라 **결합 가용성(Joint Availability)**을 수학적으로 보장한다(P_total = 1 - (1 - p4)(1 - p6) = p4 + p6 - p4·p6).

- **📢 섹션 요약 비유**: 듀얼 스택 라우팅은 "두 개의 출구가 있는 아파트"입니다. 정문(IPv6)이 막히면 30cm 옆에 있는 옆문(IPv4)으로 자동 이동하며, 1초 이상 기다리지 않습니다. 두 출구 모두 막혀야만 갇히게 됩니다.

---

## Ⅲ. 비교 및 연결

| 구분 | IPv4 Single Stack (Legacy) | IPv6 Single Stack (Greenfield) | **IPv4/IPv6 Dual Stack (Hybrid)** |
| :--- | :--- | :--- | :--- |
| **주소 공간** | 32-bit, /8 할당 고갈, CGN 강제 | 128-bit, 사실상 무한, SLAAC | 양쪽 모두 활성, 2배 라우팅 테이블 |
| **End-to-End 연결성** | NAT로 차단, P2P 불가, STUN/TURN 의존 | Native, 모든 단말 직접 도달 | IPv6는 Direct, IPv4는 NAT(legacy) |
| **보안 모델** | Stateful Firewall + NAT(암묵적 차단) | IPsec 의무화(원칙), RA Guard, SEND | IPsec/QUIC는 v6 우선, v4는 v4 정책 유지 |
| **클라우드 비용** | EIP/NAT GW 과금, ALB IPv4 charge | Egress IPv6 50% 저렴(AWS 기준), EIP 무료 | 양쪽 요금 동시 발생, 단 IPv6 트래픽 ^ 시 TCO v |
| **운영 복잡도** | 1 set (단일 ACL, 단일 Flow Log) | 1 set but SIEM 룰셋 v6 확장 | 2 set (ACL×2, Flow Log×2, DNS×2), DNS Resolver 정책 2배 |
| **Fragmentation / MTU** | PMTUD 표준, MSS Clamp 일반화 | Path MTU 1280 minimum, EH Fragment 사용 | 이기종 패킷 병행 시 MTU Mismatch(IPv4 1500, IPv6 1500 + EH),
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 483 / 800

<- **이전**: [482. 클라우드 인터커넥트 전용 연결 피어링](/studynote/13_cloud_architecture/06_exam_summary/482_cloud_interconnect_dedicated_connection_peeri/)
**다음**: [484. DNS 기반 글로벌 로드 밸런싱 GSLB](/studynote/13_cloud_architecture/06_exam_summary/484_dns_based_global_load_balancing_gslb/) ->

---
