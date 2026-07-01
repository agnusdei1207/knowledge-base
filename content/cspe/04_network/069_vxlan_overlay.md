---
title: "VXLAN 오버레이 네트워크 (VXLAN Overlay)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 69
---

# 📖 【암기용】 개념 완전 이해

> 목적: VXLAN Overlay를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: L3 네트워크 위에 L2 세그먼트를 캡슐화해 대규모 테넌트 네트워크를 만드는 오버레이 기술
- **왜 필요한가**: VLAN 12-bit는 약 4,096개 세그먼트 한계가 있고, 데이터센터는 수만 개 테넌트·네트워크 격리가 필요함
- **핵심 직관**: 기존 도로망(L3 Underlay) 위에 택배 상자(VXLAN Header)를 씌워 가상 동네(L2 Segment)를 멀리까지 연결하는 방식임

## 깊이 이해
- **배경·문제의식**: 전통 VLAN/STP 기반 L2 확장은 세그먼트 수, 장애 도메인, 링크 활용 한계가 있음. VXLAN은 UDP 캡슐화와 24-bit VNI로 L3 Fabric 위에 논리 L2 네트워크를 생성함.
- **작동 원리**: VTEP(VXLAN Tunnel Endpoint)가 원본 Ethernet Frame을 VXLAN Header로 캡슐화하고, IP/UDP Underlay를 통해 원격 VTEP로 전달함. 원격 VTEP는 디캡슐화해 목적 VM/서버에 전달함.
- **비유**: 같은 회사 사무실을 여러 도시에 두고도 내부 우편 봉투 규칙은 유지하되, 외부 택배망으로 봉투를 포장해 보내는 구조와 같음.
- **구체 예시**: 테넌트 A는 VNI 10010, 테넌트 B는 VNI 10020으로 분리하고, Leaf 스위치 VTEP가 VM MAC과 VTEP IP 매핑을 EVPN으로 교환함.
- **흔한 오해·주의점**: VXLAN은 암호화 기술이 아님. 테넌트 분리와 오버레이 확장이 목적이며, 트래픽 암호화는 IPsec, MACsec, TLS 등 별도 통제를 적용해야 함.

## 연결 개념
- VTEP — VXLAN 캡슐화·디캡슐화 종단
- VNI 24-bit — 약 1,600만 개 논리 세그먼트 식별자
- EVPN — VXLAN의 MAC/IP 학습과 제어 평면을 제공하는 BGP 기반 기술

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: VXLAN은 24-bit VNI와 VTEP 캡슐화로 L3 Fabric 위 L2 세그먼트를 제공하며, MTU·BUM 트래픽·EVPN 제어 평면을 반드시 언급한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VXLAN은 Ethernet Frame을 UDP로 캡슐화해 L3 Underlay 위에 L2 Overlay를 구성하는 데이터센터 네트워크 기술이다.
> 2. **가치**: VLAN 4,096개 한계를 VNI 24-bit로 확장하고, Leaf-Spine L3 Fabric 위에서 테넌트 격리를 제공한다.
> 3. **판단 포인트**: VTEP, VNI, MTU 50바이트 오버헤드, BUM 처리, EVPN MAC/IP Route, 보안 분리를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 오버레이 구조 이해 확인 | Underlay/Overlay, VTEP, VNI | VXLAN을 단순 VLAN 확장으로만 설명 금지 |
| 데이터센터 적용 판단 확인 | Leaf-Spine, EVPN, 테넌트 격리 | STP 기반 L2 확장과 혼동 금지 |
| 운영 리스크 확인 | MTU, BUM Flooding, MAC 이동 | 캡슐화 오버헤드와 제어 평면 누락 금지 |

> 요약: 이 문제는 VXLAN 캡슐화 구조와 EVPN 기반 운영 판단을 함께 요구한다.

---

## Ⅰ. 개요 및 필요성

VXLAN은 L3 네트워크 위에 L2 세그먼트를 캡슐화하는 오버레이 기술이다. 데이터센터는 가상머신·컨테이너·테넌트 증가로 VLAN 12-bit 약 4,096개 한계를 초과한다. VXLAN은 24-bit VNI와 VTEP를 사용해 대규모 테넌트 분리와 L3 Fabric 기반 확장을 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Tenant VM -> Access Port -> Local VTEP
-> VXLAN Header with VNI -> IP/UDP Underlay -> Remote VTEP
-> Decapsulation -> Destination VM
EVPN Control Plane -> MAC/IP Route -> VTEP Mapping
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Underlay | IP 기반 물리 네트워크 | Leaf-Spine, ECMP |
| Overlay | 논리 L2 네트워크 | VNI별 테넌트 분리 |
| VTEP | 캡슐화·디캡슐화 종단 | 스위치 또는 하이퍼바이저 |
| VNI | VXLAN Segment 식별자 | 24-bit, 약 1,600만 개 |
| EVPN | MAC/IP 학습 제어 평면 | BGP Route Type 2/5 |

> 요약: VXLAN은 VTEP가 VNI 기반 캡슐화를 수행하고 EVPN이 원격 MAC/IP 위치를 제어 평면으로 전달한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
VM Frame 수신 -> VNI 매핑 -> VXLAN Encapsulation
-> Underlay IP Routing -> Remote VTEP 수신
-> VXLAN Decapsulation -> 목적지 MAC 전달
-> EVPN으로 MAC/IP 이동 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Access VLAN 또는 VRF를 VNI와 매핑 | VLAN-VNI Table |
| 2 | VTEP가 원본 Frame에 VXLAN/UDP/IP Header 추가 | UDP 4789, VNI |
| 3 | Underlay가 VTEP IP 기준 라우팅 | ECMP, MTU |
| 4 | 원격 VTEP가 디캡슐화 후 L2 전달 | MAC Table, ARP/ND |
| 5 | EVPN이 MAC/IP Route와 이동을 갱신 | BGP EVPN Route |

> 요약: VXLAN은 VNI 매핑, VTEP 캡슐화, L3 라우팅, 원격 디캡슐화, EVPN 학습으로 동작한다.

---

## Ⅳ. 특징

| 구분 | VLAN 기반 L2 | VXLAN Overlay | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 세그먼트 수 | 12-bit VLAN 약 4,096개 | 24-bit VNI 약 1,600만 개 | VNI 24-bit |
| 확장 구조 | STP, L2 확장 | L3 Underlay, ECMP | Leaf-Spine |
| 캡슐화 | 원본 Ethernet | UDP 4789 VXLAN Header | 약 50바이트 오버헤드 |
| 제어 평면 | Flood/Learn | EVPN BGP | Route Type 2/5 |

> 요약: VXLAN은 세그먼트 수와 L3 Fabric 확장성을 제공하나 MTU와 BUM 제어를 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | VXLAN Overlay | 선택 기준 |
|:---|:---|:---|:---|
| 테넌트 격리 | VLAN | VNI 24-bit | 4,096개 초과, 멀티테넌시 |
| Fabric 구조 | L2 Spine/Access | L3 Leaf-Spine | ECMP, 장애 도메인 축소 |
| 제어 평면 | Flood/Learn | EVPN Control Plane | MAC/IP 규모, BUM 감소 |

> 요약: VXLAN은 대규모 멀티테넌트 데이터센터와 L3 Leaf-Spine Fabric에서 선택 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| MTU 문제 | VXLAN Header 약 50바이트 | Underlay MTU 1550 이상 또는 Jumbo MTU | Fragment Count |
| BUM 폭주 | Broadcast/Unknown/Multicast 처리 | EVPN, ARP Suppression | BUM Traffic Ratio |
| 보안 오해 | VXLAN 자체 암호화 없음 | VRF/ACL, IPsec/MACsec, 마이크로세그먼트 | Policy Violation Count |

> 요약: VXLAN 운영 리스크는 MTU, BUM, 보안 오해이며 EVPN과 정책 통제로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Underlay | ECMP 경로 정상, MTU 충족 | ping DF, traceroute, Telemetry |
| Overlay | VNI별 MAC/IP 학습 정상 | BGP EVPN Route, VTEP Table |
| 품질 | p95 지연·Drop 기준 충족 | Flow Telemetry, Interface Counter |

> 요약: VXLAN 검증은 Underlay MTU, EVPN Route, VNI별 전달 품질을 동시에 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Leaf-Spine Underlay는 BGP 또는 OSPF 기반 L3 ECMP로 구성하고 VXLAN 오버헤드를 고려해 MTU 1550 이상을 검증함
2. EVPN Control Plane을 적용해 MAC/IP Route를 교환하고 ARP Suppression으로 BUM Traffic Ratio를 낮춤
3. 테넌트별 VNI, VRF, ACL을 매핑하고 VXLAN 암호화 필요 구간은 IPsec 또는 MACsec을 별도 적용함

**결론 (2줄):**
- 기술사 판단: 대규모 멀티테넌트와 L3 Fabric이 필요하면 VXLAN/EVPN, 소규모 단일 세그먼트는 VLAN 단순 구조를 선택함
- 향후 방향: VXLAN은 EVPN, Kubernetes CNI, 멀티클라우드 네트워크와 결합해 데이터센터 표준 오버레이로 활용됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "VXLAN을 설명하시오" | VTEP 캡슐화와 EVPN 학습 흐름 | VLAN 대비 VNI·L3 Fabric 특징 |
| 요구사항 명시형 | "데이터센터 오버레이 설계 방안을 제시하시오" | MTU, VNI, EVPN Route 흐름 | BUM·보안·Underlay 지표 |

> 요약: 설명형은 캡슐화 원리, 설계형은 MTU·EVPN·테넌트 분리 기준으로 전개한다.
