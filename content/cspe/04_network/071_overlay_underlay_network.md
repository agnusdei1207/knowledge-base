---
title: "오버레이·언더레이 네트워크 (Overlay Underlay Network)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 71
---

# 📖 【암기용】 개념 완전 이해

> 목적: 오버레이·언더레이 네트워크를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 물리 IP망 위에 논리 터널망을 얹어 테넌트별 네트워크를 분리하는 구조
- **왜 필요한가**: 데이터센터와 클라우드는 수천 개 테넌트, VM, 컨테이너가 같은 장비를 공유한다. VLAN 12-bit 4,096개 한계만으로는 격리와 이동성을 처리하기 어렵다.
- **핵심 직관**: 언더레이는 도로망, 오버레이는 같은 도로 위에서 택배사별 송장과 경로 규칙을 붙인 가상 배송망이다.

## 깊이 이해
- **배경·문제의식**: 기존 L2 확장은 STP, 대형 브로드캐스트 도메인, VLAN ID 고갈 문제를 만든다. 클라우드에서는 워크로드가 랙과 리전을 넘어 이동하므로 물리 토폴로지와 논리 세그먼트를 분리해야 한다.
- **작동 원리**: 언더레이는 IP Clos, ECMP, OSPF/IS-IS/BGP로 VTEP 간 도달성을 보장한다. 오버레이는 VXLAN, Geneve, GRE 같은 캡슐화로 원본 프레임에 VNI, 터널 헤더, 외부 IP 헤더를 붙여 전송한다.
- **비유**: 사무실 건물의 실제 복도와 엘리베이터가 언더레이라면, 부서별 출입증과 방문 예약 규칙은 오버레이이다. 같은 복도를 지나도 부서별 접근 범위는 다르게 통제된다.
- **구체 예시**: VXLAN은 24-bit VNI로 약 1,677만 개 세그먼트를 표현한다. VLAN 4,096개보다 테넌트 수용 폭이 크며, VTEP는 UDP 4789 포트로 캡슐화 트래픽을 전달한다.
- **흔한 오해·주의점**: 오버레이만 구성하면 문제가 끝난다고 보면 안 된다. 언더레이 MTU가 VXLAN 헤더 약 50바이트 증가분을 수용하지 못하면 단편화와 패킷 손실이 발생한다.

## 연결 개념
- VXLAN — 오버레이 캡슐화의 대표 기술
- EVPN — 오버레이 제어평면에서 MAC/IP 위치를 배포하는 방식
- SDN — 중앙 제어로 오버레이 정책과 경로를 자동화하는 접근

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 물리 도달성(언더레이)과 논리 격리(오버레이)를 분리해, 확장성·운영성·장애 분리 기준을 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Overlay/Underlay는 IP 물리망 위에 VXLAN/Geneve 터널을 구성해 테넌트 네트워크를 논리 분리하는 데이터센터 네트워크 모델이다.
> 2. **가치**: VLAN 12-bit 한계를 VXLAN VNI 24-bit로 확장하고, VM/Pod 이동 시 물리 토폴로지 변경 없이 세그먼트 유지가 가능하다.
> 3. **판단 포인트**: 언더레이 ECMP·MTU·라우팅 수렴과 오버레이 VTEP·VNI·제어평면을 분리해 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 가상화 네트워크 구조 이해 확인 | Underlay IP Clos, Overlay VXLAN, VTEP, VNI 24-bit | 오버레이를 VPN과 동일 개념으로만 서술 |
| 확장성 한계와 해소 방식 판단 | VLAN 4,096개 vs VXLAN 약 1,677만 VNI | 캡슐화 오버헤드와 MTU 1550 이상 고려 누락 |
| 장애 분석 역량 확인 | Underlay reachability, Overlay MAC/IP learning 분리 진단 | 물리 링크 장애와 VNI 정책 오류를 혼동 |

> 요약: 이 문제는 논리 네트워크 확장 기술을 물리 IP망 설계, 터널 캡슐화, 장애 진단 관점으로 분리해 쓰는 역량을 요구한다.

---

## Ⅰ. 개요 및 필요성

오버레이·언더레이는 물리 IP망과 논리 터널망을 분리한 네트워크 구조이다. 데이터센터·클라우드는 테넌트 격리, 워크로드 이동성, 랙 간 L2 확장을 동시에 요구한다. VLAN 12-bit, STP 기반 L2 확장 한계를 피하기 위해 IP 기반 언더레이와 VXLAN 기반 오버레이를 결합한다.

---

## Ⅱ. 구조 및 구성요소

```text
Tenant Segment -> VNI Mapping -> VTEP Encapsulation -> Underlay IP Fabric -> Remote VTEP
                                +-> Control Plane EVPN/SDN
                                +-> Telemetry MTU/ECMP/Loss
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Underlay IP Fabric | VTEP 간 L3 도달성 제공 | Spine-Leaf, ECMP, OSPF/IS-IS/BGP |
| Overlay Tunnel | 논리 세그먼트 캡슐화 | VXLAN UDP 4789, Geneve, GRE |
| VTEP | 원본 프레임 캡슐화·복원 | ToR Switch, Hypervisor, SmartNIC |
| VNI | 테넌트/세그먼트 식별자 | VXLAN 24-bit, 약 1,677만 ID |

> 요약: 언더레이는 도달성, 오버레이는 격리와 세그먼트 확장을 담당하며 VTEP가 두 계층을 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Endpoint Frame -> VNI Lookup -> VXLAN Header Add -> Underlay ECMP Forwarding
-> Remote VTEP Decapsulation -> Destination Endpoint Delivery
-> Telemetry Check MTU/Loss/Latency
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | MAC/IP를 VNI와 매핑 | tenant to VNI table 일치 |
| 2 | VTEP가 VXLAN 헤더와 외부 IP/UDP 헤더 추가 | UDP 4789, MTU 1550 이상 |
| 3 | 언더레이가 외부 IP 기준 ECMP 전달 | VTEP loopback reachability |
| 4 | 원격 VTEP가 디캡슐화 후 내부 프레임 전달 | MAC/IP table hit, ARP/ND 응답 |
| 5 | 손실·지연·단편화 측정 | packet loss 0.1% 이하, p95 RTT 기준 |

> 요약: 패킷은 VNI 기반으로 캡슐화되고, 언더레이는 터널 외부 IP만 보고 전달하며, 원격 VTEP가 원본 프레임을 복원한다.

---

## Ⅳ. 특징

| 구분 | 기존 VLAN/L2 확장 | Overlay/Underlay | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 식별자 | VLAN 12-bit | VXLAN VNI 24-bit | 4,096개 vs 약 1,677만 개 |
| 장애 범위 | 대형 L2 도메인 | VNI 단위 격리 | 브로드캐스트 도메인 축소 |
| 경로 활용 | STP 차단 링크 발생 | ECMP 다중 경로 사용 | Spine-Leaf 링크 활용률 측정 |
| 오버헤드 | 원본 프레임 중심 | VXLAN 약 50바이트 추가 | MTU 1550 또는 jumbo frame 필요 |

> 요약: Overlay/Underlay는 식별자 확장과 ECMP 활용을 제공하지만 MTU, 제어평면, 운영 복잡도를 함께 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VLAN + STP | VXLAN Overlay + IP Underlay | 멀티테넌트 4,096 세그먼트 초과 |
| 제어평면 | Flood and Learn | EVPN, SDN Controller | ARP/ND 폭주와 MAC 이동 빈도 |
| 운영/위험 | 장비별 수동 설정 | VNI 정책 자동 배포 | IaC, 변경 승인, drift 검출 |

> 요약: 테넌트 수, 워크로드 이동성, ARP/ND 규모가 커질수록 EVPN 기반 오버레이 선택 근거가 명확해진다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 단편화 | VXLAN 헤더 추가로 MTU 초과 | MTU 1550 이상, PMTUD 검증 | fragmentation count 0 |
| 블랙홀 | VTEP loopback 도달성 손실 | BFD, ECMP next-hop 감시 | BFD down, VTEP reachability |
| MAC 폭주 | Flood and Learn 의존 | EVPN type-2 route 사용 | BUM traffic 비율 5% 이하 |

> 요약: 오버레이 장애는 터널, 제어평면, 언더레이 도달성을 분리해 지표로 확인해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| MTU | VXLAN 포함 1550 이상 또는 jumbo 9000 | ping DF bit, path MTU test |
| ECMP | spine-leaf 경로 분산 편차 20% 이하 | flow telemetry, sFlow/NetFlow |
| 제어평면 | MAC/IP route 수렴 1초~5초 | EVPN route update timestamp |

> 요약: 성공 기준은 VNI 확장 개수보다 MTU 무단편, ECMP 분산, 제어평면 수렴 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Underlay는 Spine-Leaf L3 Clos, loopback 기반 BGP/OSPF, BFD 300ms~1s 타이머로 VTEP 도달성 보장
2. Overlay는 VXLAN VNI 24-bit, EVPN type-2/type-5, Anycast Gateway로 L2/L3 세그먼트 구성
3. 운영은 MTU 1550 이상, VNI/IPAM 관리, BUM traffic 5% 이하, flow telemetry 기반 변경 검증 적용

**결론 (2줄):**
- 기술사 판단: 테넌트·세그먼트가 VLAN 4,096개 한계에 접근하거나 VM/Pod 이동성이 요구되면 VXLAN Overlay를 선택함
- 향후 방향: EVPN, SmartNIC, Kubernetes CNI 연동으로 데이터센터와 클라우드 네트워크의 정책 일관성을 확보함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | VTEP 캡슐화, VNI 매핑, 언더레이 ECMP 흐름 | VLAN 대비 VNI 확장, MTU 오버헤드 |
| 요구사항 명시형 | "비교하시오", "설계하시오", "방안을 제시하시오" | VXLAN/EVPN 설계 절차, 장애 진단 순서 | MTU, BUM traffic, 제어평면 수렴 지표 |

> 요약: 설명형은 계층 분리 원리, 설계형은 MTU·ECMP·EVPN 제어평면 검증 기준을 중심으로 전개한다.
