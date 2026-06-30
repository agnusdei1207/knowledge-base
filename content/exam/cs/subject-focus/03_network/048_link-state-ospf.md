---
title: "링크상태 라우팅·OSPF (Link State/Open Shortest Path First)"
date: "2026-06-30"
weight: 48
tags:
  - "exam-cspe-network"
---

## Ⅰ. 1교시 핵심 답안

> OSPF는 링크상태 기반의 대표적인 IGP로, 라우터들이 동일한 토폴로지 데이터베이스를 공유한 뒤 `SPF` 알고리즘으로 최단 경로를 계산한다.

- **핵심 요소**: `LSA`, `LSDB`, `SPF`, `Cost`
- **특징**: 빠른 수렴, 계층형 Area 구조
- **메트릭**: 대역폭 기반 Cost
- **출제 포인트**: RIP/EIGRP/BGP와의 비교

## Ⅱ. 구조 및 동작 원리

```text
Link State 수집
 -> LSA Flooding
 -> LSDB 동기화
 -> Dijkstra SPF 계산
 -> Routing Table 반영

Area 0 <-> ABR <-> Other Areas
```

- **LSA**: 링크 상태와 비용 광고
- **LSDB**: 전체 망 지도를 각 라우터가 동일하게 보유
- **SPF**: 각 라우터가 독립적으로 최단경로 계산
- **Area 구조**: 대규모 망의 확장성과 제어용

## Ⅲ. 비교표

| 구분 | RIP | OSPF | BGP |
|:---|:---|:---|:---|
| 분류 | IGP/거리벡터 | IGP/링크상태 | EGP/경로벡터 |
| 메트릭 | Hop Count | Cost | 정책/속성 |
| 수렴 속도 | 느림 | 빠름 | 상대적으로 느림 |
| 적용 범위 | 소규모 내부망 | 대규모 내부망 | AS 간 |

## Ⅳ. 기술사 답안 포인트

- **장점**: 빠른 수렴, 루프 억제, 표준 기반 상호운용
- **설계 포인트**: `Area 0`, ABR, Stub/NSSA, 요약 광고
- **운영 포인트**: LSDB와 SPF 계산에 따른 CPU/메모리 부담
- **비교 확장**: `RIP vs OSPF`, `OSPF vs EIGRP`, `OSPF vs BGP`

## Ⅴ. 결론

OSPF의 본질은 `전체 망 상태를 공유한 뒤 각자 계산`하는 구조에 있다.  
따라서 답안에서는 `LSA-LSDB-SPF-Area` 흐름을 한 묶음으로 제시해야 서술형 확장이 쉽다.
