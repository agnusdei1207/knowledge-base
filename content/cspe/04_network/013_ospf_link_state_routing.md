---
title: "링크 상태 라우팅 — OSPF·OSPFv3 (OSPF Link State Routing)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 13
---

# 📖 【암기용】 개념 완전 이해

> 목적: OSPF와 OSPFv3를 처음 봐도 링크 상태 라우팅의 지도 작성 방식과 SPF 계산을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 라우터가 링크 상태 정보를 공유하고 각자 최단 경로 트리를 계산하는 IGP
- **왜 필요한가**: 거리 벡터 방식은 이웃이 알려준 거리만 믿기 때문에 수렴 지연과 루프 위험이 있다. OSPF는 네트워크 지도를 각 라우터가 보유해 장애 시 SPF 계산으로 경로를 갱신한다.
- **핵심 직관**: 모든 라우터가 같은 지도를 받아 각자 현재 위치에서 최단 경로를 다시 그리는 방식이다.

## 깊이 이해
- **배경·문제의식**: 기업 내부망은 수십~수백 개 라우터와 다중 링크를 가진다. OSPF는 Area 구조, LSA 홍수, Dijkstra SPF로 내부 라우팅을 빠르게 수렴시키기 위해 설계되었다.
- **작동 원리**: 라우터는 Hello로 이웃을 맺고, LSA(Link State Advertisement)를 교환해 LSDB(Link State Database)를 동기화한다. 각 라우터는 동일 LSDB에서 SPF를 계산해 라우팅 테이블을 만든다.
- **비유**: 각 지점이 자기 주변 도로 공사 정보를 본사 지도 시스템에 알리고, 모든 지점이 같은 최신 지도를 내려받아 이동 경로를 다시 계산하는 구조다.
- **구체 예시**: OSPF 기본 reference bandwidth 100 Mbps일 때 100 Mbps 링크는 cost 1, 10 Mbps 링크는 cost 10으로 자동 계산된다. SPF는 총 cost가 낮은 경로를 선택한다. 기준 bandwidth를 100 Gbps로 조정하지 않으면 고속 링크 차이가 반영되지 않을 수 있다.
- **흔한 오해·주의점**: OSPFv3는 단순히 IPv6 주소만 추가한 것이 아니다. 링크 로컬 주소 사용, 주소 패밀리 확장, 인증 방식 변화까지 함께 고려해야 한다.

## 연결 개념
- Dijkstra SPF — LSDB 기반 최단 경로 계산 알고리즘
- Area 0 Backbone — OSPF 영역 간 라우팅의 중심 영역
- BFD — OSPF 장애 감지를 수백 ms 단위로 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: OSPF 답안은 Hello/LSA/SPF 순서와 Area 설계, DR/BDR, OSPFv2·v3 차이를 함께 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OSPF는 라우터 간 링크 상태를 LSA로 공유하고 LSDB를 동기화한 뒤 SPF로 최단 경로를 계산하는 링크 상태 IGP이다.
> 2. **가치**: Area 구조, cost 기반 경로 선택, 장애 수렴(BFD 300ms~dead 40초 기준)으로 대규모 내부망의 라우팅 테이블과 LSA 범위를 통제한다.
> 3. **판단 포인트**: Area 0 연결성, DR/BDR, hello/dead timer, LSA flooding 범위, OSPFv3 IPv6 링크 로컬 동작을 확인한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 링크 상태 라우팅 원리 확인 | Hello, adjacency, LSA, LSDB, SPF | 거리 벡터처럼 이웃 거리 전달로 설명 |
| OSPF 설계 역량 확인 | Area 0, ABR, ASBR, DR/BDR | 단일 Area만 전제 |
| OSPFv3 차이 확인 | IPv6, link-local, IPSec 또는 인증 방식 | OSPFv2와 동일하다고 서술 |

> 요약: OSPF 문제는 LSA 기반 지도 동기화와 Area 설계, OSPFv3 차이를 함께 쓰는 것이 채점 포인트다.

---

## Ⅰ. 개요 및 필요성

OSPF는 링크 상태 정보를 교환해 내부망 최단 경로를 계산하는 IGP이다. 라우터는 LSDB를 동기화하고 Dijkstra SPF로 목적지별 next-hop을 산출한다. 대규모 기업망에서는 Area 분할과 route summarization으로 라우팅 범위를 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
OSPF Router -> Hello Neighbor Discovery -> Adjacency
  / LSA Flooding -> LSDB
  / SPF Calculation -> Routing Table
Area 0 -> ABR -> Non-Backbone Area
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Hello Protocol | 이웃 탐색과 dead 판단 | hello 10초, dead 40초 예시 |
| LSA/LSDB | 링크 상태 광고와 데이터베이스 | Area 내 동일 LSDB 유지 |
| SPF Engine | Dijkstra 알고리즘으로 경로 계산 | cost 합산 기준 |
| Area/ABR | LSA 범위 분리와 요약 | Area 0 backbone 필수 |

> 요약: OSPF 구조는 Hello 인접성, LSA/LSDB 동기화, SPF 계산, Area 분리로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Interface Up -> Hello Exchange -> Neighbor State Form
  -> DBD/LSR/LSU Exchange -> LSDB Sync
  -> SPF Run -> Route Install -> LSA Refresh or Triggered Update
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Hello 패킷으로 이웃 발견 | neighbor state 2-Way 이상 |
| 2 | DBD, LSR, LSU로 LSDB 동기화 | LSDB checksum 일치 |
| 3 | SPF 계산으로 최단 cost 경로 산출 | 누적 OSPF cost |
| 4 | 장애 발생 시 LSA 재홍수와 SPF 재계산 | convergence time 측정 |

> 요약: OSPF는 이웃 형성 후 LSDB를 맞추고, 장애 이벤트마다 SPF 재계산으로 라우팅 테이블을 갱신한다.

---

## Ⅳ. 특징

| 구분 | OSPF | RIP/정적 라우팅 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 경로 기준 | cost 기반 누적 비용 | hop count 또는 수동 경로 | RFC 2328, RFC 5340 |
| 수렴 방식 | triggered LSA와 SPF | 주기 업데이트 또는 수동 변경 | hello/dead 10/40초 예시 |
| 규모 제어 | Area, ABR, summarization | 단순 테이블 관리 | Area 0 backbone |
| LAN 최적화 | DR/BDR로 LSA 교환 감소 | 모든 노드 직접 교환 | multi-access network |

> 요약: OSPF는 cost, LSA, Area, DR/BDR을 통해 내부망 규모와 수렴 시간을 통제한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | OSPFv2 | OSPFv3 | 선택 기준 |
|:---|:---|:---|:---|
| 주소 체계 | IPv4 라우팅 | IPv6 라우팅, 주소 패밀리 확장 | IPv6 전환 구간은 OSPFv3 |
| 이웃 형성 | IPv4 인터페이스 주소 | link-local 주소 사용 | 링크 로컬 도달성 점검 |
| 인증 | OSPF 자체 인증 | IPsec 또는 구현별 인증 | 장비 지원 방식 확인 |

> 요약: IPv6 내부망은 OSPFv3의 링크 로컬 동작과 인증 방식을 별도 검증해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SPF 폭증 | 링크 flap 반복 | SPF throttle, BFD dampening | SPF run count |
| Area 불연속 | Area 0 미연결 | virtual link 또는 설계 수정 | inter-area route 누락 |
| DR 장애 | multi-access DR 단일 장애점 | BDR 구성, priority 설정 | neighbor state Full |

> 요약: OSPF 리스크는 SPF 부하, Area 설계 오류, DR/BDR 장애이며 로그와 neighbor 상태로 확인한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 인접성 | 핵심 링크 neighbor Full | show ospf neighbor |
| 수렴 시간 | 링크 장애 후 1초~40초 범위 목표 | failover test, BFD |
| LSDB 일관성 | Area 내 LSA checksum 일치 | LSDB compare |

> 요약: OSPF 운영은 neighbor Full, convergence time, LSDB 일관성으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 백본은 Area 0으로 고정하고 지점·부서는 Area 10, 20처럼 분리해 LSA flooding 범위를 제한함
2. 고속 링크는 reference bandwidth를 100 Gbps 이상으로 조정해 1G/10G/100G cost 차이를 반영함
3. 장애 감지는 OSPF timer만 의존하지 않고 BFD 300ms~1s와 SPF throttle을 함께 적용함

**결론 (2줄):**
- 기술사 판단: 단일 AS 내부 대규모망은 OSPF, AS 간 정책 라우팅은 BGP를 선택하고 경계 구간은 재분배 정책을 제한함
- 향후 방향: OSPFv3, BFD, telemetry 기반 LSDB 검증으로 IPv6 전환망의 수렴성과 운영 가시성을 확보해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OSPF를 설명하시오" | Hello, LSA, LSDB, SPF 동작 | OSPF와 RIP 차이, Area 구조 |
| 요구사항 명시형 | "OSPFv3 설계 방안을 제시하시오" | link-local, IPv6, Area 설계 | OSPFv2/v3 차이, BFD 적용 |

> 요약: OSPF는 설명형이면 링크 상태 원리, 설계형이면 Area와 OSPFv3 운영 조건을 중심으로 전환한다.
