---
sidebar:
  order: 103
  label: "103. CAP 정리"
  badge:
    text: "기출 · 70%"
    variant: note
title: "CAP 정리 (CAP Theorem)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 103
extra:
  question_no: "103"
  source_status: "기출"
  source_history: "131회"
  priority: 70
  priority_note: "131회 기출, 일관성•가용성 절충의 정본"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CAP 정리**: Eric Brewer가 제안한 분산 시스템 이론으로, 일관성(Consistency), 가용성(Availability), 분할내성(Partition Tolerance)을 동시 만족 불가.
- **P(분할내성)의 불가피성**: 네트워크 패킷 유실 및 단절은 분산 환경의 필연적 현상이므로, 실제 선택지는 CP 대 AP로 귀결됨.

</details>

- 정의/개념: 분산 시스템에서 네트워크 분할(P) 발생 시 **일관성(Consistency), 가용성(Availability), 분할내성(Partition Tolerance)** 중 2가지만 선택 가능하다는 정리
- 배경/필요성: 분산 노드 간 네트워크 단절 상황에서 **최신 데이터 동기화와 무중단 성공 응답의 동시 보장 불가 한계**

#### 한줄 요약
- 네트워크 분할(P) 하에서 일관성 중심(CP)과 가용성 중심(AP) 간의 불가피한 절충을 규정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PACELC 정리**: 네트워크 분할(P) 시 A와 C의 선택, 정상(Else) 시 지연시간(Latency)과 일관성(Consistency) 간의 절충을 규정한 확장 이론.
- **Quorum(정족수 합의)**: $R + W > N$ 공식을 통해 읽기/쓰기 노드 과반수 합의로 최신 데이터의 일관성을 판정하는 메커니즘.

</details>

- 분산 네트워크 단절(P)을 전제로 한 **일관성(CP) 대 가용성(AP)의 양자택일 구조**
- 노드 정족수(Quorum) 기반의 **과반수 노드 합의 메커니즘 연계**
- 정상 상태에서의 지연시간(L)과 일관성(C)의 절충을 설명하는 **PACELC 확장 이론과 조화**

#### 한줄 요약
- 네트워크 분할 시 응답을 차단(CP)할지, 구버전이라도 반환(AP)할지 결정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CP vs AP 대표 시스템**: 과반수 정족수 미달 시 에러를 내는 CP(MongoDB, HBase, Redis)와 Stale 데이터를 허용하는 AP(Cassandra, DynamoDB).

</details>

```text
[CAP 정리 및 CP / AP 분기 아키텍처]
|-- Partition Tolerance (P: 네트워크 단절 발생 - 분산 시스템 필수 전제)
|   |-- CP 시스템 (일관성 선택: MongoDB, HBase, Spanner)
|   |   |-- 정족수(Quorum) 과반수 미달 시 쓰기/읽기 차단 (에러 반환)
|   |   `-- 모든 클라이언트에게 100% 최신 일관된 데이터만 제공
|   `-- AP 시스템 (가용성 선택: Cassandra, DynamoDB, CouchDB)
|       |-- 분할 중에도 살아있는 로컬 복제본 노드가 무조건 성공 응답 반환
|       `-- Stale Data 허용 및 네트워크 복구 후 최종 일관성(Eventual) 수렴
```

선의 의미: 계층 및 네트워크 분할(P) 발생 시 CP 경로와 AP 경로로 분기되는 구조

| CAP 속성 | 핵심 엔지니어링 정의 | 시스템 판정 기준 |
|:---|:---|:---|
| **일관성 (Consistency)** | 모든 클라이언트가 어느 노드에 붙더라도 **가장 최근에 쓰인 동일한 최신 데이터 반환** | 최신 복제 미완료 시 읽기 차단 |
| **가용성 (Availability)**| 일부 노드 장애/단절 시에도 **살아있는 정상 노드가 에러 없이 유한 시간 내 응답** | Stale 데이터라도 무조건 반환 |
| **분할 내성 (Partition)** | 노드 간 네트워크 통신이 단절되거나 메시지 유실 시에도 **분산 시스템 동작 유지** | 분산 환경의 필수 불변 전제 |
| **정족수 검증기 (Quorum)**| 분할 발생 시 과반수 노드($R + W > N$) 도달 여부를 확인하여 **요청 승인/거부 판정** | 스플릿 브레인 방지 |

#### 한줄 요약
- 일관성(C), 가용성(A), 분할내성(P)의 상호작용 속에서 정족수 검증을 통해 시스템 동작을 결정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Hinted Handoff**: AP 시스템에서 분할로 전달하지 못한 쓰기 이력을 로컬에 임시 저장했다가 네트워크 복구 시 전달하는 기법.

</details>

```text
1. 분산 노드 간 네트워크 분할(Partition) 감지
        │
   2. [정족수 검사] 현재 분리된 서브 클러스터가 과반수(Quorum) 노드를 확보했는가?
   ┌────┴───────────────────────────┐
[CP 시스템 경로]               [AP 시스템 경로]
과반수 미달 시 요청 거부 (Fail-Fast)   로컬 복제본으로 즉시 200 OK 응답
데이터 불일치 원천 차단 (신뢰성)      Stale Data 반환 허용 (무중단 가용성)
        │                               │
   3. 네트워크 복구 감지 및 힌트 핸드오프(Hinted Handoff) / Read Repair 동기화
        │
   4. 벡터 시계(Vector Clock) 기반 데이터 병합으로 최종 일관성(Eventual Consistency) 달성
```

#### 한줄 요약
- 분할 감지 → 정족수 검사 → CP(차단) / AP(응답) → 복구 및 최종 일관성 수렴 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CP vs AP 비교**: 데이터 정합성이 최우선인 금융/결제용 CP와 24/365 무중단 서비스가 최우선인 쇼핑몰/SNS용 AP.

</details>

| 비교 항목 | CP 시스템 (Consistency & Partition) | AP 시스템 (Availability & Partition) |
|:---|:---|:---|
| 최우선 가치 | **데이터 무결성 및 엄격한 정합성** | **시스템 무중단 가용성 (High Availability)** |
| 분할 시 동작 | **정족수 미달 시 쓰기/읽기 차단 및 에러**| **구버전 데이터(Stale)라도 무조건 성공 응답** |
| 대표 엔진 | **MongoDB, HBase, Redis Cluster, Spanner**| **Cassandra, DynamoDB, CouchDB, Riak** |
| 주 활용 분야 | **은행 계좌 이체, 결제 원장, 주식 주문** | **SNS 피드, 쇼핑몰 장바구니, IoT 센서 수집** |

#### 한줄 요약
- 데이터 정확성이 최우선이면 CP, 무중단 고가용성이 최우선이면 AP 시스템을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tunable Consistency**: Cassandra 등에서 쿼리마다 정족수 레벨(ONE, QUORUM, ALL)을 동적으로 지정하여 CP/AP를 유연하게 조절하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AP 시스템 채택 시 비즈니스 데이터 불일치 발생 | **가변 일관성(Tunable Consistency: $R + W > N$) 강제 설정** | AP 기반 DB에서 강력한 일관성 확보 |
| CP 시스템 채택 시 네트워크 단절로 인한 쿼리 타임아웃 | **Circuit Breaker 패턴 연동 및 캐시 기반 Fallback 응답 구성** | 서비스 전면 장애 전파 차단 |
| AP 환경에서 노드 간 동시 쓰기로 인한 충돌(Conflict) | **Vector Clock 및 Last-Write-Wins(LWW) 충돌 해결기 적용** | 충돌 데이터의 원활한 최종 수렴 |
| PACELC 관점의 정상 시 지연시간(Latency) 증가 | **로컬 리전 내 복제본 우선 읽기(Local Quorum) 정책 적용** | 글로벌 네트워크 지연 최소화 |

#### 한줄 요약
- 가변 정족수 튜닝, 서킷 브레이커 도입, 충돌 해결 메커니즘, Local Quorum으로 CAP의 한계를 보완한다.

## Ⅶ. 결론

- 분산 아키텍처 설계 시 **단일 시스템 전체를 일률적으로 규정하지 않고, 결제·원장 모듈은 CP로, 조회·추천 모듈은 AP로 분리하는 도메인 주도 하이브리드 아키텍처**를 구축하여 정합성과 가용성을 양립

#### 한줄 요약
- CAP 정리는 분산 컴퓨팅의 절대 원칙이며, 네트워크 분할 내성 하에서 비즈니스 도메인에 부합하는 CP와 AP의 최적 배치가 핵심이다.