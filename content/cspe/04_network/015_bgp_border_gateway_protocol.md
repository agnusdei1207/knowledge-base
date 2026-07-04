---
title: "BGP 경계 게이트웨이 프로토콜 (BGP Border Gateway Protocol)"
date: "2026-07-04"
tags:
  - "cspe-network"
weight: 15
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: BGP(Border Gateway Protocol)는 자율 시스템(AS) 간에 도달 가능한 대역과 그 대역까지의 AS 경로 목록(AS-Path)을 교환해, 홉 수가 아닌 정책으로 최적 경로를 고르는 인터넷의 유일한 표준 EGP(경로 벡터, Path Vector)임(IGP·라우팅 기본은 012·013 참조).
- **왜 필요한가**: OSPF·RIP 같은 IGP는 하나의 AS 내부 최단경로를 계산할 뿐, 서로 다른 사업자(AS) 사이에서는 "누구 트래픽을 어디로 보낼지"가 기술이 아닌 계약·정책 문제라, 정책을 실을 수 있는 별도 프로토콜이 필요함.
- **핵심 직관**: IGP가 "우리 회사 건물 안 최단 복도 찾기"라면, BGP는 "회사와 회사 사이 어느 협력사를 거쳐 물건을 보낼지"를 계약 조건에 따라 정하는 국가 간 물류 협정과 같음.

## 핵심 용어 정리 (내부에 등장하는 것들)
아래는 답안(Ⅰ~Ⅵ·표)에 나오는 용어를 미리 풀어 둔 것임. 최상위 키워드는 **경로 벡터 EGP(BGP)**임.

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| AS(Autonomous System) | 단일 정책으로 운영되는 라우터 집단, ASN으로 식별 | 하나의 사업자·국가 |
| EGP/IGP | AS 간(EGP=BGP) vs AS 내부(IGP=OSPF) 라우팅 | 국가 간 vs 국내 도로 |
| Path Vector(경로 벡터) | 거쳐온 AS 목록(AS-Path)을 실어 경로 표현 | 통과 국가 도장 목록 |
| AS-Path | 목적지까지 거친 AS 번호들의 나열 | 여권의 경유국 스탬프 |
| eBGP | 서로 다른 AS 간 BGP 세션 | 국경 넘는 협정 |
| iBGP | 같은 AS 내부 BGP 라우터 간 세션 | 국내 지사 간 정보 공유 |
| BGP Attribute | 경로 선택 기준값(정책 파라미터) | 배송 우선순위 규칙 |
| Local Preference | AS 내 나가는 경로 선호도(높을수록 우선) | 우리 쪽 선호 출구 |
| AS-Path Length | 경유 AS 수(짧을수록 우선) | 경유국 적은 항로 우선 |
| MED | 이웃 AS에 들어오는 경로 선호 힌트(낮을수록 우선) | 상대에게 권하는 입구 |
| TCP 179 | BGP 세션이 쓰는 신뢰 전송 포트 | 협정용 전용 회선 |
| Route Reflector | iBGP 풀메시를 대신하는 경로 반사기 | 지사 정보 중계 허브 |

## 깊이 이해
- **배경·문제의식**: 인터넷은 수만 개 AS의 연합인데, 각 AS는 요금·계약·보안 정책이 달라 단순 최단경로로는 운영이 불가함. 거리 벡터(RIP, 014 참조)를 AS 단위로 확장하되 카운트 투 인피니티를 없애고 정책을 실을 수 있는 BGP-4(RFC 4271)가 사실상 인터넷 표준이 됨.
- **작동 원리(어떻게+왜)**: BGP는 TCP 179로 이웃과 세션을 맺고, 자신이 도달 가능한 대역(Prefix)을 AS-Path·Attribute와 함께 광고함. 수신 라우터는 광고에 자기 AS 번호를 앞에 붙여 전파하는데, 이미 자기 AS가 AS-Path에 있으면 루프로 보고 폐기함(경로 벡터의 루프 차단). 최적 경로는 Weight→Local Preference→AS-Path 길이→MED 등 Attribute 우선순위로 선택해 정책을 반영함. eBGP는 AS 사이, iBGP는 AS 내부에서 외부 경로를 공유하며, iBGP는 풀메시가 원칙이나 규모가 크면 Route Reflector로 대체함.
- **비유**: 국제 택배가 "어느 나라들을 거쳐 갈지"를 관세·협정에 따라 정하는 것과 같음. 이미 지나온 나라가 경유 목록에 또 있으면 빙빙 도는 것이므로 그 경로를 버리는데, 이게 AS-Path 기반 루프 차단임.
- **구체 예시**: 멀티홈 기업이 ISP A·B 두 회선을 쓸 때, 나가는 트래픽은 Local Preference를 A에 높게 줘 A로 내보내고, 들어오는 트래픽은 AS-Path Prepending으로 B 경로를 길게 보이게 해 A로 유도함. 즉 BGP는 단일 최적이 아니라 방향별 정책을 세밀히 제어함.
- **흔한 오해·주의점**: BGP는 "가장 빠른/짧은" 경로를 고르는 프로토콜이 아니라 "정책상 가장 선호하는" 경로를 고름. 또 AS-Path가 짧아도 Local Preference가 높은 경로가 우선하므로, AS-Path 길이만으로 선택을 단정하면 안 됨.

## 연결 개념
- 라우팅 기본·경로 벡터 (012 참조) — BGP는 Path Vector로 분류되며 AD는 eBGP 20·iBGP 200임.
- 거리 벡터·RIP (014 참조) — BGP의 뿌리. AS-Path로 카운트 투 인피니티를 제거한 확장형.
- BGP 하이재킹 방지·RPKI (139·140 참조) — BGP 경로 위·변조를 검증하는 보안 확장.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BGP는 AS 간 도달성과 AS-Path를 교환해 정책 Attribute로 경로를 고르는 경로 벡터 EGP로, 인터넷을 잇는 유일한 표준 프로토콜임.
> 2. **가치**: AS-Path 기반 루프 차단과 Local Preference·MED 등 정책 제어로 사업자 간 계약·트래픽 방향을 세밀히 반영함.
> 3. **판단**: AS 내부 최단경로는 IGP(OSPF, 013 참조)에 맡기고, AS 간·멀티홈·멀티클라우드 연동은 BGP로 정책 라우팅을 구현해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 경로 벡터·EGP 위치 | AS·AS-Path·eBGP/iBGP·TCP 179 | IGP(OSPF)와 역할 혼동 |
| 정책 기반 경로 선택 | Local Preference·AS-Path·MED 우선순위 | "짧은 경로 우선"으로 단정 |
| 루프 차단·확장 | AS-Path 루프 검출·Route Reflector | 카운트 투 인피니티 미차단 오해 |

> 요약: BGP는 'AS-Path 교환+정책 Attribute 선택'으로 EGP 위치를 증명하고, 루프 차단·멀티홈 정책·IGP 위임으로 결론지어야 함.

---

## Ⅰ. 개요 및 필요성

- 정의: AS 간 도달 대역과 AS-Path를 TCP로 교환해 정책 Attribute로 최적 경로를 선택하는 경로 벡터 EGP임.
- 배경: 정책·계약이 제각각인 수만 AS를 잇기에 IGP의 단순 최단경로는 부적합함.
- 필요성: AS 간 도달성 확보와 사업자별 정책·트래픽 방향 제어, AS-Path 기반 루프 차단이 필요함.

---

## Ⅱ. 구조 및 구성요소

구조도(선형):

```text
AS 100 --(eBGP, TCP 179)-- AS 200 --(eBGP)-- AS 300
  AS 200 내부: 경계 라우터끼리 iBGP로 외부 경로 공유 (풀메시 또는 Route Reflector)
경로 광고: Prefix + AS-Path + Attribute -> 수신 시 자기 ASN을 AS-Path 앞에 추가
최적 선택: Weight -> Local Preference -> AS-Path 길이 -> MED 순 정책 평가
```

| 구성요소 | 역할 | 특징 |
|:---|:---|:---|
| eBGP 세션 | 서로 다른 AS 경계 라우터 연결 | TCP 179, AS-Path에 ASN 추가 |
| iBGP 세션 | AS 내부에 외부 경로 전파 | 풀메시 원칙, RR로 확장 |
| AS-Path | 경유 AS 목록 | 루프 차단·경로 길이 지표 |
| Attribute | Local Pref·MED·Community 등 | 정책 기반 경로 선택 기준 |
| Route Reflector | iBGP 풀메시 대체 반사기 | O(n^2) 세션 폭증 완화 |

> 요약: BGP는 eBGP로 AS를 잇고 iBGP로 내부에 전파하며, AS-Path와 Attribute로 루프를 막고 정책 경로를 선택함.

---

## Ⅲ. 동작원리 및 흐름도

흐름도(선형):

```text
경계 라우터가 TCP 179로 이웃과 세션 수립 -> Open으로 ASN·파라미터 협상
  -> 도달 대역(Prefix)을 AS-Path·Attribute와 함께 Update로 광고
  -> 수신 라우터가 자기 ASN이 AS-Path에 있으면 폐기(루프 차단)
  -> Attribute 우선순위로 최적 경로 선택 -> 변화 시 증분 Update, Keepalive로 유지
```

- 1단계: 경계 라우터가 이웃과 TCP 179 세션을 맺고 Open 메시지로 AS 번호·타이머를 협상함.
- 2단계: 각 라우터가 자신이 도달 가능한 Prefix를 AS-Path·Attribute와 함께 Update로 광고하고, 전파 시 자기 ASN을 AS-Path 앞에 붙임.
- 3단계: 수신 라우터가 AS-Path에 자기 AS가 이미 있으면 루프로 보고 폐기하며, 없으면 Weight→Local Preference→AS-Path 길이→MED 순으로 최적 경로를 선택함.
- 4단계: 경로 변화가 생기면 해당 부분만 증분 Update로 알리고, Keepalive로 세션을 유지하며 정책에 따라 재수렴함.

> 요약: BGP는 TCP 세션 위에서 Prefix·AS-Path를 광고하고, 자기 AS 중복 시 폐기해 루프를 막으며 Attribute 우선순위로 정책 경로를 선택함.

---

## Ⅳ. 특징

- 정책 기반 선택: 최단경로가 아니라 Local Preference·AS-Path·MED·Community 등 Attribute 우선순위로 경로를 골라 계약·트래픽 방향을 반영함.
- 경로 벡터 루프 차단: AS-Path에 자기 AS가 있으면 폐기하므로, 거리 벡터(014 참조)의 카운트 투 인피니티가 구조적으로 발생하지 않음.
- 신뢰 전송·증분 갱신: TCP 179 위에서 동작해 재전송·순서를 보장하고, 변경분만 Update해 대규모 인터넷 라우팅 테이블을 안정적으로 유지함.
- eBGP/iBGP 분리: AS 간은 eBGP, 내부 전파는 iBGP로 나뉘며 iBGP 풀메시 부담은 Route Reflector·Confederation으로 완화함.
- 대규모 확장성: 전 세계 90만 개 이상 경로를 수용하나, 그만큼 오광고 1건이 전 세계에 전파되는 안정성·보안 취약도 동반함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | IGP(OSPF, 013 참조) | EGP(BGP) |
|:---|:---|:---|
| 적용 범위 | 단일 AS 내부 | AS 간(인터넷 전역) |
| 경로 방식 | 링크 상태(LSDB+SPF) | 경로 벡터(AS-Path) |
| 선택 기준 | 대역폭 기반 Cost 최단 | 정책 Attribute 우선순위 |
| 수렴 목표 | 수초 내 빠른 수렴 | 안정성 우선(정책·필터) |
| 확장 규모 | 수백~수천 경로 | 수십만~90만+ 경로 |

> 요약: IGP는 AS 내부 최단경로에, BGP는 AS 간 정책 라우팅에 특화되어 상호 보완하며, 둘의 역할 경계를 지키는 것이 설계 원칙임.

리스크·대응(불릿):
- BGP 하이재킹 — 타 AS의 Prefix 무단 광고 — RPKI(139 참조)·ROA 검증·Prefix Filtering(140 참조) 적용.
- 경로 누출(Route Leak) — 정책 위반 재광고 — AS-Path·Community 필터, RFC 8212 기본 거부(default deny) 적용.
- iBGP 세션 폭증 — 내부 풀메시 O(n^2) — Route Reflector·Confederation으로 세션 축소.

지표(불릿):
- 수용 경로 수 — Full Route 90만+ 수용 여부 — RIB/FIB 엔트리 계수로 측정.
- 경로 안정성 — 플랩 최소화 — Route Flap Damping·Update 빈도 모니터링.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. **멀티홈 정책 제어**: ISP 이중 회선에서 나가는 트래픽은 Local Preference로, 들어오는 트래픽은 AS-Path Prepending·MED로 방향을 제어해 회선 부하를 분산함.
2. **iBGP 확장 설계**: 내부 BGP 라우터가 늘면 풀메시 대신 Route Reflector(이중화)로 세션 수를 줄이고, IGP(OSPF, 013 참조)로 Next-hop 도달성을 확보함.
3. **경로 보안 강화**: RPKI-ROA(139 참조)와 Prefix/AS-Path 필터, RFC 8212 기본 거부를 적용해 하이재킹·경로 누출을 차단함.

**결론(2줄):**
- 기술사 판단: AS 내부 최단경로는 IGP(OSPF)로, AS 간·멀티홈·멀티클라우드 연동은 BGP 정책 라우팅으로 분담하되 경로 보안을 필수 병행해야 함.
- 향후 방향: RPKI 확산과 SDN(066 참조) 기반 중앙 경로 제어가 결합해, BGP의 정책 표현력에 검증·자동화를 더하는 방향으로 진화함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "BGP 동작원리를 설명하시오" | AS-Path 광고·루프 차단·Attribute 선택 흐름 | IGP vs EGP 위치·역할 분담 판단 |
| 요구사항 명시형 | "멀티홈 BGP 트래픽 제어 방안을 제시하시오" | Local Pref·MED·Prepending 흐름 | 방향별 정책·경로 보안(RPKI) 적용 |

> 요약: 포괄형은 AS-Path 루프 차단과 정책 선택 원리에, 명시형은 멀티홈 방향 제어와 RPKI 보안 적용에 초점을 둠.
