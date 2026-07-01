---
title: "EVPN·BGP EVPN (EVPN BGP)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 72
---

# 📖 【암기용】 개념 완전 이해

> 목적: EVPN·BGP EVPN을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: BGP로 MAC/IP 위치와 L2/L3 VPN 정보를 배포하는 오버레이 제어평면
- **왜 필요한가**: VXLAN Flood and Learn은 ARP, unknown unicast, MAC 이동이 늘면 BUM 트래픽이 커진다. EVPN은 MAC/IP 정보를 라우팅 정보처럼 교환해 플러딩 의존도를 낮춘다.
- **핵심 직관**: 데이터센터의 단말 위치를 전화번호부처럼 BGP에 등록해, 물어보지 않고 목적지 VTEP로 바로 보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: L2 확장망은 MAC 학습을 데이터평면에 맡기면 브로드캐스트와 unknown unicast가 증가한다. 멀티테넌트 VXLAN에서는 각 VNI의 MAC/IP 이동을 제어평면에서 추적해야 한다.
- **작동 원리**: VTEP는 로컬 MAC/IP를 EVPN NLRI로 BGP에 광고한다. Type-2는 MAC/IP route, Type-3은 inclusive multicast, Type-5는 IP prefix route를 담당한다. 원격 VTEP는 수신 route로 MAC table과 routing table을 채운다.
- **비유**: 아파트에서 방문객이 매번 전 세대를 호출하지 않고, 관리사무소 명부에서 호수를 확인한 뒤 바로 찾아가는 구조와 같다.
- **구체 예시**: VXLAN VNI 10010의 VM `10.1.1.10/MAC A`가 Leaf-1에 있으면 Leaf-1은 EVPN Type-2로 MAC/IP와 VTEP IP를 광고한다. Leaf-2는 해당 정보를 받아 VXLAN 터널 next-hop을 Leaf-1로 설정한다.
- **흔한 오해·주의점**: EVPN은 VXLAN 자체가 아니라 제어평면이다. VXLAN 없이 MPLS EVPN도 가능하며, VXLAN EVPN은 데이터평면 VXLAN과 제어평면 BGP EVPN의 조합이다.

## 연결 개념
- VXLAN — EVPN이 제어하는 대표 오버레이 데이터평면
- MP-BGP — EVPN NLRI를 운반하는 라우팅 프로토콜 확장
- Anycast Gateway — VTEP별 동일 게이트웨이 IP/MAC 제공 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: EVPN은 VXLAN의 플러딩 문제를 BGP 제어평면으로 줄이는 기술이며, route type별 역할을 구분해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EVPN은 MP-BGP로 MAC/IP, multicast membership, IP prefix를 배포해 L2/L3 VPN을 통합 제공하는 제어평면이다.
> 2. **가치**: VXLAN Flood and Learn의 BUM 트래픽을 줄이고, MAC mobility, multihoming, Anycast Gateway를 표준 route type으로 처리한다.
> 3. **판단 포인트**: Type-2/3/5 route, RD/RT, VNI 매핑, VTEP next-hop을 묶어 설명해야 답안 밀도가 확보된다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| EVPN 제어평면 이해 확인 | MP-BGP, EVPN NLRI, Type-2/3/5 route | VXLAN 터널 기술로만 서술 |
| 데이터센터 L2/L3 통합 설계 판단 | L2VNI, L3VNI, Anycast Gateway, RT import/export | VLAN 확장과 동일 수준으로 단순화 |
| 운영 리스크 식별 | MAC mobility, route scale, BUM 억제, multihoming | BGP 수렴·route 정책 누락 |

> 요약: 이 문제는 EVPN route type과 VXLAN VNI 매핑을 통해 플러딩 억제와 L3 확장을 설명하는 답안이 필요하다.

---

## Ⅰ. 개요 및 필요성

EVPN은 BGP 기반 이더넷 VPN 제어평면이다. 멀티테넌트 VXLAN 환경에서는 MAC/IP 위치와 세그먼트 정보를 장비 간 동기화해야 한다. EVPN은 MAC 학습을 데이터평면 플러딩에서 제어평면 광고로 전환해 대규모 데이터센터의 L2/L3 오버레이를 구성한다.

---

## Ⅱ. 구조 및 구성요소

```text
Tenant Endpoint -> Local VTEP -> EVPN NLRI Advertisement -> MP-BGP Route Reflector
                              -> Remote VTEP Route Import -> VXLAN Forwarding Table
                              +-> RD/RT/VNI Policy
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| MP-BGP | EVPN NLRI 배포 | AFI 25, SAFI 70 |
| Route Type-2 | MAC/IP 위치 광고 | host route, MAC mobility sequence |
| Route Type-3 | VNI별 BUM 복제 대상 광고 | inclusive multicast ethernet tag |
| Route Type-5 | IP prefix route 광고 | inter-subnet routing, L3VNI |
| RD/RT | route 식별·수입 정책 | VRF, tenant 분리 |

> 요약: EVPN은 MP-BGP route type과 RD/RT 정책으로 VTEP 간 MAC/IP 위치와 테넌트 경계를 배포한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Endpoint Attach -> VTEP Learns MAC/IP -> BGP EVPN Type-2 Advertise
-> Route Reflector Distribute -> Remote VTEP Import by RT
-> VXLAN Encapsulation to Next-hop VTEP -> Delivery
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 로컬 VTEP가 MAC/IP와 VNI 학습 | MAC/IP binding 일치 |
| 2 | Type-2 route로 MAC/IP와 VTEP next-hop 광고 | BGP EVPN table 수신 |
| 3 | RT import 정책으로 테넌트 route 반영 | VRF route-target 일치 |
| 4 | 원격 VTEP가 VXLAN forwarding entry 생성 | VNI, next-hop, MAC table 확인 |
| 5 | MAC 이동 시 sequence 값으로 최신 위치 선택 | duplicate MAC, mobility counter |

> 요약: EVPN은 엔드포인트 위치를 BGP route로 배포하고, VTEP는 수신 route를 VXLAN 포워딩 테이블로 변환한다.

---

## Ⅳ. 특징

| 구분 | Flood and Learn VXLAN | BGP EVPN | 수치·판단 포인트 |
|:---|:---|:---|:---|
| MAC 학습 | 데이터평면 플러딩 | Type-2 제어평면 광고 | BUM traffic 비율 5% 이하 목표 |
| L3 확장 | 외부 라우터 의존 | Type-5 IP prefix route | L3VNI, VRF 연동 |
| 멀티호밍 | 벤더별 구현 차이 | Ethernet Segment, DF election | ESI, split-horizon label |
| 규모 | VTEP 증가 시 플러딩 증가 | RR 기반 route scale 관리 | EVPN route count, BGP memory |

> 요약: EVPN은 VXLAN 오버레이의 제어평면을 BGP로 표준화해 MAC/IP 위치, L3 prefix, 멀티호밍을 일관되게 처리한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 제어평면 | Flood and Learn | MP-BGP EVPN | VTEP 10대 이상, BUM 증가 |
| 라우팅 | VLAN gateway 집중 | Distributed Anycast Gateway | east-west 트래픽 비중 60% 이상 |
| 운영/위험 | 장비별 MAC table 확인 | EVPN route table 기반 진단 | BGP route visibility 필요 |

> 요약: 대규모 VXLAN에서는 EVPN route table을 기준으로 MAC/IP 위치를 검증하는 운영 모델이 요구된다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Route 폭증 | VM/Pod 증가로 Type-2 증가 | RR 분리, route summarization, L3VNI 설계 | EVPN route count, BGP memory |
| MAC 이동 루프 | 동일 MAC 다중 위치 광고 | MAC mobility sequence, duplicate detection | MAC move rate, dampening count |
| 정책 오배포 | RT import/export 오류 | VRF별 RT 표준화, CI lint | wrong route import 0건 |

> 요약: EVPN 운영 리스크는 route scale, MAC mobility, RT 정책 오류이며 BGP 테이블 기준으로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| BGP 수렴 | route update 1초~5초 | BGP event timestamp |
| BUM 억제 | BUM traffic 5% 이하 | sFlow/NetFlow, interface counter |
| Route 정확도 | Type-2/5 route 누락 0건 | EVPN table diff, VNI inventory |

> 요약: 도입 성공은 BGP 수렴, BUM 비율, EVPN route 정확도 세 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Spine 또는 전용 노드에 BGP Route Reflector를 배치하고 EVPN AFI/SAFI, RR redundancy, BFD를 구성함
2. L2VNI와 L3VNI, RD/RT, VRF naming 규칙을 IPAM/CMDB에 등록해 테넌트별 import/export 오류를 차단함
3. Type-2/3/5 route count, MAC move rate, BUM traffic, BGP convergence를 telemetry로 수집해 변경 전후 diff를 수행함

**결론 (2줄):**
- 기술사 판단: VXLAN이 10대 이상 VTEP와 다수 테넌트로 확장되면 Flood and Learn보다 BGP EVPN 제어평면을 선택함
- 향후 방향: EVPN은 데이터센터, DCI, Kubernetes 네트워킹과 결합해 MAC/IP 위치 기반 정책 자동화로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | Type-2/3/5 route 동작과 VTEP 포워딩 | Flood and Learn 대비 BUM 억제 |
| 요구사항 명시형 | "비교하시오", "설계하시오", "운영 방안을 제시하시오" | RD/RT, L2VNI/L3VNI, RR 설계 절차 | route scale, MAC mobility, 수렴 지표 |

> 요약: 설명형은 EVPN route type, 설계형은 RT 정책과 BGP 수렴 검증을 중심으로 목차를 전환한다.
