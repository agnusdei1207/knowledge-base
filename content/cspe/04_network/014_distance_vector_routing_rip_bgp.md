---
title: "거리 벡터 라우팅 — RIP·BGP (Distance Vector Routing RIP BGP)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 14
---

# 📖 【암기용】 개념 완전 이해

> 목적: 거리 벡터 라우팅을 처음 봐도 이웃에게 거리 정보를 듣고 경로를 고르는 원리를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 이웃 라우터가 알려준 목적지까지의 거리와 방향을 기준으로 경로를 선택하는 라우팅 방식
- **왜 필요한가**: 모든 라우터가 전체 지도를 가질 필요 없이 이웃에게 받은 경로 정보만으로 라우팅 테이블을 만들 수 있다. 구조는 단순하지만 루프와 수렴 지연을 통제해야 한다.
- **핵심 직관**: 목적지까지 직접 가본 사람은 없고, 옆 사람에게 "거기까지 몇 정거장인지" 물어 다음 방향을 고르는 방식이다.

## 깊이 이해
- **배경·문제의식**: 거리 벡터는 초기 인터넷과 소규모망에서 구현이 간단했다. RIP은 hop count만 사용해 단순하고, BGP는 AS 경로 벡터와 정책 속성을 사용해 인터넷 규모의 라우팅을 수행한다.
- **작동 원리**: 라우터는 주기적으로 라우팅 테이블 일부 또는 전체를 이웃에게 알린다. 더 낮은 metric 또는 정책상 우선 경로가 오면 테이블을 갱신한다. 루프 방지는 split horizon, poison reverse, hold-down, AS_PATH 검사로 수행한다.
- **비유**: 친구에게 목적지까지 몇 번 갈아타는지 듣고 이동하는데, 친구도 내 말을 듣고 있으면 같은 정보를 서로 되풀이할 수 있어 루프 방지 규칙이 필요하다.
- **구체 예시**: RIP은 15 hop까지 도달 가능, 16 hop은 unreachable로 처리한다. BGP는 AS_PATH에 자기 AS가 포함된 경로를 폐기해 AS 수준 루프를 차단한다.
- **흔한 오해·주의점**: BGP는 단순 거리 벡터가 아니라 path vector로 분류한다. 다만 전체 링크 지도가 아니라 이웃이 광고한 경로 속성을 기반으로 선택한다는 점에서 비교 대상으로 출제된다.

## 연결 개념
- RIP — hop count 기반 거리 벡터 IGP
- BGP — AS_PATH 기반 경계 라우팅 프로토콜
- 라우팅 루프 — count-to-infinity, AS_PATH loop 방지 필요

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 거리 벡터 답안은 RIP의 hop count 한계와 BGP의 path vector 정책성을 구분해 작성해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 거리 벡터 라우팅은 이웃이 광고한 목적지 거리와 next-hop을 기준으로 라우팅 테이블을 갱신하는 방식이다.
> 2. **가치**: 구현이 단순하고 라우터별 전체 토폴로지 저장 부담이 낮으며, BGP는 AS 간 정책 라우팅으로 확장된다.
> 3. **판단 포인트**: count-to-infinity, split horizon, hold-down, AS_PATH loop detection, convergence time을 반드시 비교한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 거리 벡터 원리 확인 | distance, vector, next-hop, periodic update | 링크 상태 라우팅과 동일하게 설명 |
| RIP·BGP 비교 역량 확인 | RIP hop count, BGP AS_PATH·policy | BGP를 RIP과 같은 단순 metric으로 서술 |
| 루프 방지 이해 확인 | split horizon, poison reverse, AS_PATH 검사 | count-to-infinity 누락 |

> 요약: 거리 벡터 문제는 단순성보다 루프 방지와 수렴 지연 통제 방안을 쓰는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 이웃 라우터가 알려준 거리와 방향으로 경로를 선택하는 라우팅 방식
- 배경: RIP은 hop count 기반 IGP, BGP는 AS_PATH·정책 속성 기반 path vector EGP로 분류됨
- 필요성: 단순 경로 교환 구조이므로 루프 방지와 수렴 시간 관리가 필요함

---

## Ⅱ. 구조 및 구성요소

```text
Router A -> Route Advertisement -> Router B
  / Destination Network
  / Distance Metric
  / Next-Hop or AS_PATH
Route Table Update -> Loop Prevention -> Forwarding
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Distance | 목적지까지의 비용 | RIP hop count, BGP policy 속성 |
| Vector | 목적지 방향 또는 next-hop | 이웃 라우터 기준 |
| Update Message | 경로 정보 광고 | RIP 30초 주기, BGP TCP 179 |
| Loop Prevention | 순환 경로 차단 | split horizon, AS_PATH 검사 |

> 요약: 거리 벡터 구조는 목적지, 거리, next-hop, 루프 방지 규칙으로 라우팅 테이블을 갱신한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Neighbor Update Receive -> Metric Add or Policy Check
  -> Better Route Select -> Routing Table Install
  -> Route Advertise to Neighbors -> Loop Rule Apply
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이웃으로부터 경로 광고 수신 | RIP update, BGP UPDATE |
| 2 | metric 증가 또는 BGP 속성 평가 | hop count, LOCAL_PREF, AS_PATH |
| 3 | 최적 경로를 라우팅 테이블에 반영 | next-hop reachability |
| 4 | 다른 이웃에 경로 재광고 | split horizon, AS loop check |

> 요약: 거리 벡터는 이웃 광고를 수신해 metric과 정책을 평가하고, 루프 규칙을 적용한 뒤 재광고한다.

---

## Ⅳ. 특징

| 구분 | RIP | BGP | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 분류 | 거리 벡터 IGP | path vector EGP | RIP UDP 520, BGP TCP 179 |
| metric | hop count | LOCAL_PREF, AS_PATH, MED 등 | RIP 15 hop 제한 |
| 수렴 | 주기 업데이트 중심 | 정책 기반 업데이트 | RIP 30초 update |
| 적용 범위 | 소규모 내부망 | 인터넷 AS 간 라우팅 | eBGP, iBGP 구분 |

> 요약: RIP은 단순 hop count, BGP는 AS 경로와 정책 속성으로 인터넷 규모 경로를 제어한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 거리 벡터 | 링크 상태 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 이웃에게 거리 광고 | 전체 링크 상태 공유 | 소규모망은 거리 벡터, 대규모 내부망은 OSPF |
| 비용/성능 | CPU·메모리 부담 낮음 | LSDB와 SPF 비용 필요 | 장비 자원과 수렴 목표 비교 |
| 운영/위험 | count-to-infinity | LSA 폭주, SPF 부하 | 루프 방지와 토폴로지 규모 기준 |

> 요약: 거리 벡터는 단순 구조가 장점이나 장애 수렴과 루프 통제 한계를 설계에 반영해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| count-to-infinity | 잘못된 경로 정보 반복 광고 | split horizon, poison reverse | unreachable route count |
| 수렴 지연 | 주기 업데이트 의존 | triggered update, hold-down 조정 | convergence time |
| 정책 오류 | BGP 속성 우선순위 오설정 | prefix-list, route-map 검증 | unexpected AS_PATH |

> 요약: 거리 벡터 운영은 잘못된 경로 반복, 수렴 지연, 정책 오류를 루프 방지 규칙과 필터로 제어한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 루프 방지 | 반복 hop 또는 AS loop 0건 | traceroute, BGP table |
| 수렴 시간 | 장애 후 목표 시간 내 경로 전환 | link fail test |
| 경로 정책 | 허용 prefix만 광고 | prefix-list audit |

> 요약: 거리 벡터 검증은 루프 발생 여부, 수렴 시간, 광고 prefix 정확성으로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. RIP은 실습·소규모 폐쇄망에 한정하고 hop count 15 제한과 30초 update 주기를 문서화함
2. BGP는 prefix-list, AS_PATH filter, route-map으로 수신·광고 경로를 통제함
3. 장애 시험은 링크 down 후 convergence time과 traceroute 반복 hop 여부를 함께 측정함

**결론 (2줄):**
- 기술사 판단: 내부 대규모망은 OSPF, AS 간 경계는 BGP, RIP은 제한된 소규모 구간에만 적용함
- 향후 방향: BGP 정책 검증, RPKI, 라우팅 telemetry로 거리 벡터 계열의 잘못된 경로 광고를 사전 차단해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "거리 벡터 라우팅을 설명하시오" | 이웃 광고, metric, 재광고 흐름 | RIP과 BGP 비교 |
| 요구사항 명시형 | "라우팅 루프 방안을 제시하시오" | count-to-infinity, AS_PATH 검사 | split horizon, 필터링, 수렴 지표 |

> 요약: 거리 벡터는 설명형이면 동작 원리, 방안형이면 루프 방지와 경로 필터링으로 목차를 전환한다.
