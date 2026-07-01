---
title: "BGP 경계 게이트웨이 프로토콜 (BGP Border Gateway Protocol)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 15
---

# 📖 【암기용】 개념 완전 이해

> 목적: BGP를 처음 봐도 인터넷이 AS 단위 정책으로 경로를 선택하는 구조를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: AS 간 IP prefix 도달성을 교환하고 정책으로 경로를 선택하는 인터넷 경계 라우팅 프로토콜
- **왜 필요한가**: 인터넷은 하나의 관리자가 운영하지 않는다. 각 ISP, 클라우드, 기업은 AS 번호를 갖고 자신이 소유하거나 위임받은 prefix를 광고하며, 비용·정책·계약에 따라 경로를 선택한다.
- **핵심 직관**: 가장 짧은 길만 고르는 내비게이션이 아니라, 계약된 도로와 통행료, 경유 금지 구간을 반영하는 국제 물류 경로 선택이다.

## 깊이 이해
- **배경·문제의식**: OSPF 같은 IGP는 단일 조직 내부 최단 경로 계산에 적합하다. BGP는 AS 간 규모, 정책, 장애 격리, prefix 필터링, 다중 ISP 연결을 처리하기 위해 TCP 기반 path vector로 동작한다.
- **작동 원리**: BGP 라우터는 TCP 179로 세션을 맺고 OPEN, KEEPALIVE, UPDATE, NOTIFICATION 메시지를 사용한다. 경로 선택은 LOCAL_PREF, AS_PATH 길이, ORIGIN, MED, eBGP/iBGP, IGP metric 등 순서로 진행된다.
- **비유**: 택배사가 목적지까지 여러 운송사를 경유할 때, 단순 거리보다 계약 우선순위와 경유 회사 목록을 보고 노선을 선택하는 방식이다.
- **구체 예시**: `203.0.113.0/24 AS_PATH 64500 64496` 경로와 `203.0.113.0/24 AS_PATH 64510 64520 64496` 경로가 있으면, 다른 조건이 같을 때 AS_PATH 길이 2인 전자가 우선된다.
- **흔한 오해·주의점**: BGP는 최단 지연시간을 자동 보장하지 않는다. 정책 라우팅이므로 더 긴 AS_PATH라도 LOCAL_PREF가 높으면 선택될 수 있다.

## 연결 개념
- AS(Autonomous System) — 독립 라우팅 정책을 가진 관리 도메인
- RPKI/ROA — prefix와 origin AS의 정합성을 검증하는 체계
- iBGP/eBGP — AS 내부 BGP와 AS 간 BGP 세션 구분

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: BGP는 인터넷 라우팅의 최단 경로 프로토콜이 아니라 AS 간 정책·신뢰·prefix 통제 프로토콜로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BGP(Border Gateway Protocol)는 AS 간 prefix 도달성을 TCP 179 기반 UPDATE로 교환하는 path vector 라우팅 프로토콜이다.
> 2. **가치**: 다중 ISP, 클라우드 연결, 인터넷 edge에서 경로 정책, 트래픽 엔지니어링, 장애 우회를 구현한다.
> 3. **판단 포인트**: LOCAL_PREF, AS_PATH, MED, community, prefix-list, RPKI, flap damping을 기준으로 경로 품질과 보안을 통제한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| BGP 동작 원리 확인 | TCP 179, OPEN/UPDATE/KEEPALIVE, AS_PATH | OSPF처럼 SPF 계산으로 설명 |
| 경로 선택 정책 이해 확인 | LOCAL_PREF, AS_PATH, MED, community | hop count만 기준으로 서술 |
| 인터넷 라우팅 리스크 판단 | prefix hijack, route leak, RPKI | 보안 검증 누락 |

> 요약: BGP 문제는 경로 속성 순서와 prefix 검증 체계를 함께 써야 고득점 답안이 된다.

---

## Ⅰ. 개요 및 필요성

BGP는 AS 간 라우팅 정보를 교환하는 인터넷 경계 프로토콜이다. 각 AS는 자신이 도달 가능한 IP prefix와 경로 속성을 광고한다. 다중 회선, 클라우드 전용 연결, 인터넷 edge에서는 비용·계약·보안 정책에 따른 경로 제어가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
AS Border Router -> BGP Peer TCP 179 -> Route Update
  / NLRI Prefix
  / Path Attributes
  / Policy Filter
Best Path -> RIB -> FIB -> Packet Forwarding
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| NLRI | 도달 가능한 prefix 정보 | IPv4/IPv6 address family |
| Path Attributes | 경로 선택 속성 | LOCAL_PREF, AS_PATH, MED |
| BGP Peer | eBGP 또는 iBGP 세션 | TCP 179, keepalive 사용 |
| Policy Filter | 광고·수신 prefix 제어 | prefix-list, route-map |

> 요약: BGP 구조는 prefix 정보, 경로 속성, peer 세션, 정책 필터를 통해 AS 간 경로를 선택한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
TCP Session Establish -> OPEN Exchange -> KEEPALIVE
  -> UPDATE Receive -> Policy Filter -> Best Path Selection
  -> RIB Install -> Advertisement to Peers
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | TCP 179 세션과 BGP OPEN 교환 | Established state |
| 2 | NLRI와 path attributes 수신 | prefix, AS_PATH, next-hop |
| 3 | import policy와 best path 알고리즘 적용 | LOCAL_PREF 우선순위 |
| 4 | 선택 경로를 RIB/FIB에 반영 후 광고 | advertised-routes 확인 |

> 요약: BGP는 세션 수립, 경로 수신, 정책 평가, 최적 경로 반영, 재광고 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | BGP | OSPF 등 IGP | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 적용 범위 | AS 간, 인터넷 edge | 단일 AS 내부 | RFC 4271, TCP 179 |
| 경로 기준 | 정책 속성 기반 | cost 기반 최단 경로 | LOCAL_PREF, AS_PATH |
| 수렴 특성 | 정책 반영으로 지연 가능 | 내부 링크 중심 수렴 | hold timer 180초 예시 |
| 보안 이슈 | hijack, route leak | 내부 오설정 중심 | RPKI, max-prefix |

> 요약: BGP는 최단 경로보다 AS 정책과 prefix 신뢰성을 우선하는 인터넷 경계 라우팅 프로토콜이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | eBGP | iBGP | 선택 기준 |
|:---|:---|:---|:---|
| 연결 범위 | 서로 다른 AS 간 | 동일 AS 내부 | ISP 연동은 eBGP, 내부 전달은 iBGP |
| next-hop 처리 | 기본 변경 | 기본 유지 | next-hop-self 필요 여부 |
| 확장 구조 | peer 직접 연결 중심 | full mesh 또는 route reflector | peer 수 증가 시 RR 적용 |

> 요약: eBGP는 AS 경계, iBGP는 AS 내부 경로 전달이며 next-hop과 route reflector 설계가 다르다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Prefix Hijack | 잘못된 origin AS 광고 | RPKI ROA, prefix-list | invalid route 0건 |
| Route Leak | provider/customer 정책 오류 | AS_PATH filter, community | unexpected transit route |
| 세션 장애 | keepalive 손실, TCP 차단 | BFD, MD5/TCP-AO, max-prefix | BGP state Established |

> 요약: BGP 리스크는 잘못된 prefix 광고와 세션 장애이며 RPKI, 필터, 세션 보호로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Prefix 검증 | 수신 prefix 100% 정책 매칭 | prefix-list audit |
| 세션 가용성 | 주요 peer Established 유지 | BGP session monitor |
| 경로 품질 | AS_PATH, latency, loss 기준 충족 | route table, active probe |

> 요약: BGP 운영은 prefix 검증, peer 상태, 경로 품질을 동시에 점검해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 외부 peer에는 prefix-list, max-prefix, AS_PATH filter를 적용해 허용된 NLRI만 수신·광고함
2. 트래픽 엔지니어링은 inbound AS_PATH prepending, outbound LOCAL_PREF 조정으로 회선별 정책을 분리함
3. RPKI ROA 검증과 BGP monitoring을 적용해 hijack·leak 탐지 시간을 분 단위로 줄임

**결론 (2줄):**
- 기술사 판단: 인터넷 edge와 다중 ISP 연동은 BGP가 필수이며, 내부 최단 경로 계산은 OSPF/IS-IS로 분리함
- 향후 방향: RPKI, BGPsec, 자동 정책 검증으로 AS 간 라우팅 신뢰성을 운영 지표로 관리해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "BGP를 설명하시오" | 세션, UPDATE, best path 흐름 | BGP와 IGP 비교 |
| 요구사항 명시형 | "BGP 보안 방안을 제시하시오" | prefix filter, RPKI 검증 | hijack·route leak 리스크 대응 |

> 요약: BGP는 설명형이면 path vector 원리, 보안형이면 prefix 신뢰성과 정책 필터를 중심으로 목차를 전환한다.
