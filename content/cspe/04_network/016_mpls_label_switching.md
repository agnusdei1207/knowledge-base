---
title: "MPLS 레이블 스위칭 (MPLS Label Switching)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 16
---

# 📖 【암기용】 개념 완전 이해

> 목적: MPLS를 처음 봐도 IP 주소 대신 레이블로 경로를 바꾸는 이유와 VPN, TE 활용을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: IP 패킷에 짧은 레이블을 붙여 LSR이 레이블 값으로 전달 경로를 결정하는 스위칭 기술
- **왜 필요한가**: 라우터가 매 홉마다 긴 IP prefix를 조회하면 서비스별 경로 제어와 VPN 분리가 복잡해진다. MPLS는 FEC 단위로 레이블을 붙여 L3 VPN, Traffic Engineering, QoS 경로를 구현한다.
- **핵심 직관**: 택배 상자 주소를 매번 읽지 않고, 물류센터가 붙인 색상 라벨만 보고 컨베이어 라인을 바꾸는 방식이다.

## 깊이 이해
- **배경·문제의식**: 통신사업자 백본은 고객 VPN, 음성, 데이터, 전용회선을 같은 물리망에서 분리해야 한다. MPLS는 IP 라우팅 위에 label switched path를 만들어 고객별 VRF와 경로 정책을 분리한다.
- **작동 원리**: Edge LSR은 IP prefix를 FEC로 분류하고 label을 push한다. Core LSR은 label swap만 수행한다. Egress LSR은 label을 pop하고 원래 IP 패킷을 목적지로 전달한다.
- **비유**: 공항 수하물이 최종 주소가 아니라 목적지 코드 태그로 분류되는 방식과 같다.
- **구체 예시**: MPLS label은 20비트, TC 3비트, S 1비트, TTL 8비트로 구성된다. Ethernet 위 MPLS unicast EtherType은 0x8847이다.
- **흔한 오해·주의점**: MPLS는 암호화 기술이 아니다. VPN 분리는 label과 VRF 기반 논리 분리이며, 암호화가 필요하면 IPsec, MACsec 등 별도 통제가 필요하다.

## 연결 개념
- LDP/RSVP-TE — 레이블 배포와 TE 경로 예약 방식
- VRF/MPLS L3VPN — 고객별 라우팅 테이블 분리
- Segment Routing — MPLS label stack 또는 SRv6 SID로 경로를 명시하는 발전 방향

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: MPLS 답안은 레이블 push/swap/pop 동작과 FEC, LSP, VPN/TE 적용 판단을 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MPLS(Multiprotocol Label Switching)는 IP 패킷 앞에 label stack을 붙여 LSR이 label 기반으로 전달하는 2.5계층 스위칭 기술이다.
> 2. **가치**: FEC, LSP, VRF를 이용해 사업자 백본에서 L3VPN, Traffic Engineering, QoS 경로 분리를 구현한다.
> 3. **판단 포인트**: label 20비트, TTL propagation, MTU 증가, PHP, LDP/RSVP-TE, VRF route leaking을 점검해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MPLS 동작 원리 확인 | push, swap, pop, FEC, LSP | IP 라우팅과 동일하게 서술 |
| 적용 영역 판단 확인 | L3VPN, TE, QoS, 백본 분리 | MPLS를 암호화 VPN으로 단정 |
| 운영 리스크 이해 확인 | MTU, label 고갈, LSP 장애 | TTL, PHP, OAM 누락 |

> 요약: MPLS는 label 기반 전달 원리와 VPN/TE 적용 조건, MTU·OAM 리스크를 함께 써야 한다.

---

## Ⅰ. 개요 및 필요성

MPLS는 IP 패킷에 레이블을 부여해 백본에서 label 기반으로 전달하는 기술이다. IP prefix 조회와 서비스별 정책을 분리해 고객 VPN과 트래픽 엔지니어링을 구현한다. 대규모 백본에서는 LSP와 VRF 단위로 경로·고객·품질을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
Customer Edge -> Provider Edge Push Label -> Core LSR Swap
  / FEC
  / LSP
  / Label Stack
Provider Edge Pop Label -> Customer Network
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| FEC | 동일 전달 처리를 받는 패킷 집합 | prefix, VPN, QoS 기준 |
| LER/PE | label push/pop 수행 | 고객망과 MPLS망 경계 |
| LSR/P Router | label swap 수행 | core에서 IP lookup 최소화 |
| LSP | label switched path | LDP 또는 RSVP-TE로 구성 |

> 요약: MPLS 구조는 Ingress PE가 label push, P가 label swap, Egress PE가 label pop하는 경계-코어 모델이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Packet Ingress -> FEC Classification -> Label Push
  -> Label Swap per LSR -> Penultimate Hop Pop or Egress Pop
  -> IP Forwarding to Destination
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PE가 IP prefix, VRF, QoS로 FEC 분류 | LFIB entry 존재 |
| 2 | MPLS label stack 부여 | label 20비트, TTL 8비트 |
| 3 | Core LSR이 label swap 수행 | LSP next-hop 일치 |
| 4 | Egress에서 label pop 후 IP 전달 | ping mpls, traceroute mpls |

> 요약: MPLS는 ingress 분류, label push, core swap, egress pop 순서로 IP 전달 경로를 제어한다.

---

## Ⅳ. 특징

| 구분 | MPLS | 순수 IP 라우팅 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 전달 기준 | label lookup | longest prefix match | label 20비트 |
| 서비스 분리 | VRF, label stack | ACL, VRF-lite | EtherType 0x8847 |
| 경로 제어 | RSVP-TE, SR-MPLS | IGP metric 중심 | explicit path 가능 |
| 패킷 영향 | label당 4바이트 추가 | IP 헤더만 사용 | MTU 여유 필요 |

> 요약: MPLS는 IP 라우팅 위에서 label 기반 서비스 분리와 경로 제어를 제공하지만 MTU 증가를 반영해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | LDP 기반 MPLS | RSVP-TE/SR-MPLS | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | IGP 경로를 따라 label 배포 | 명시 경로 또는 segment 지정 | 단순 VPN은 LDP, TE는 RSVP-TE/SR |
| 비용/성능 | 설정 부담 낮음 | 정책·상태 관리 증가 | 회선 사용률 70% 기준 |
| 운영/위험 | IGP 장애 영향 | 경로 정책 오류 가능 | OAM과 path validation 필수 |

> 요약: 일반 L3VPN은 LDP, 특정 회선 우회와 TE가 필요하면 RSVP-TE 또는 Segment Routing을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| MTU 초과 | label stack 4바이트 이상 추가 | core MTU 1500 초과 설계, PMTUD | fragmentation, drop count |
| LSP 단절 | LDP neighbor 장애 | LDP sync, BFD, FRR | LSP up/down event |
| VPN 혼선 | VRF route leaking 오류 | RT/RD 정책 검토 | 잘못된 prefix 유입 0건 |

> 요약: MPLS 리스크는 MTU, LSP 단절, VRF 혼선이며 OAM과 정책 점검으로 제어한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| LSP 상태 | 핵심 LSP 100% up | mpls lsp ping |
| MTU | label stack 포함 무손실 전달 | DF ping, PMTUD |
| VPN 분리 | VRF 간 비인가 route 0건 | route-target audit |

> 요약: MPLS 운영 품질은 LSP 상태, MTU 여유, VRF 분리 정확성으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. MPLS 코어 MTU는 label stack과 서비스 헤더를 고려해 1500바이트보다 큰 jumbo MTU로 설계함
2. L3VPN은 고객별 VRF, RD, RT를 분리하고 route-target import/export 정책을 변경 승인 대상으로 관리함
3. 백본 장애 대응은 MPLS OAM, BFD, Fast Reroute로 LSP 단절 시간을 목표 범위 내로 줄임

**결론 (2줄):**
- 기술사 판단: 고객 VPN과 TE가 필요한 사업자·대기업 백본은 MPLS, 단순 인터넷 edge는 IP 라우팅과 VRF-lite를 선택함
- 향후 방향: SR-MPLS와 SRv6로 label distribution 상태를 줄이고 intent 기반 경로 검증을 적용해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MPLS를 설명하시오" | push, swap, pop 흐름 | MPLS와 IP 라우팅 비교 |
| 요구사항 명시형 | "VPN 백본 설계 방안을 제시하시오" | VRF, LSP, MTU 검증 | LDP/TE 선택, 리스크 대응 |

> 요약: MPLS는 설명형이면 레이블 동작, 설계형이면 VRF·MTU·OAM 중심으로 목차를 전환한다.
