---
sidebar:
  order: 103
  label: "103. CAP 정리"
  badge:
    text: "기출 · 70%"
    variant: note
title: "CAP 정리 (CAP Theorem)"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: 분산 시스템에서 네트워크 분할(P) 발생 시 일관성(Consistency), 가용성(Availability), **분할내성**(Partition Tolerance) 중 2가지만 선택 가능하다는 정리
- 배경/필요성: 네트워크 지연과 패킷 유실이 필연적인 분산 환경에서 **일관성(C)·가용성(A)·분할내성(P) 동시 100% 만족의 수학적·물리적 불가결성 한계**

#### 한줄 요약
- CAP는 상시 셋 중 둘을 고르는 문제가 아니라 분할이 실제로 발생한 순간에만 발동하는 제약이므로, 실무 판단은 평시 성능이 아니라 분할 중 어떤 종류의 오답을 감수할 것인가로 좁혀진다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PACELC 정리**: 네트워크 분할(P) 시 A와 C의 선택, 정상(Else) 시 지연시간(Latency)과 일관성(Consistency) 간의 절충을 규정한 확장 이론.
- **Quorum(정족수 합의)**: $R + W > N$ 공식을 통해 읽기/쓰기 노드 과반수 합의로 최신 데이터의 일관성을 판정하는 메커니즘.

</details>

- 분산 네트워크 단절(P)을 전제로 한 일관성(CP) 대 가용성(AP)의 양자택일 구조
- 노드 정족수(Quorum) 기반의 과반수 노드 합의 메커니즘 연계
- 정상 상태에서의 지연시간(L)과 일관성(C)의 절충을 설명하는 PACELC 확장 이론과 조화

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

| 구성요소 | 책임 |
|:---|:---|
| 일관성 | 모든 노드의 최신 데이터 반환 |
| 가용성 | 정상 노드의 유한 시간 응답 |
| 분할 내성 | 네트워크 단절 중 분산 동작 유지 |
| 정족수 검증기 | 과반수 기반 요청 승인·거부 |

#### 한줄 요약
- 정족수는 C와 A 사이의 눈금을 조절하는 장치라 읽기·쓰기 정족수의 합을 전체 사본 수보다 크게 잡으면 일관성이, 작게 잡으면 가용성이 앞서므로 CAP의 선택은 이 두 값의 설정으로 구현된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Hinted Handoff**: AP 시스템에서 분할로 전달하지 못한 쓰기 이력을 로컬에 임시 저장했다가 네트워크 복구 시 전달하는 기법.

</details>

```text
분산 노드 간 네트워크 분할(Partition) 감지
        │
   [정족수 검사] 현재 분리된 서브 클러스터가 과반수(Quorum) 노드를 확보했는가?
   ┌────┴───────────────────────────┐
[CP 시스템 경로]               [AP 시스템 경로]
과반수 미달 시 요청 거부 (Fail-Fast)   로컬 복제본으로 즉시 200 OK 응답
데이터 불일치 원천 차단 (신뢰성)      Stale Data 반환 허용 (무중단 가용성)
        │                               │
   네트워크 복구 감지 및 힌트 핸드오프(Hinted Handoff) / Read Repair 동기화
        │
   벡터 시계(Vector Clock) 기반 데이터 병합으로 최종 일관성(Eventual Consistency) 달성
```

#### 한줄 요약
- CP는 분할 중의 오류 응답을 감수하는 대신 복구 후 별도의 정합 작업을 없애고, AP는 응답을 계속 돌려주는 대신 복구 시점에 갈라진 버전을 합치는 비용을 뒤로 미룬다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CP vs AP 비교**: 데이터 정합성이 최우선인 금융/결제용 CP와 24/365 무중단 서비스가 최우선인 쇼핑몰/SNS용 AP.

</details>

| 비교 항목 | CP 시스템 (Consistency & Partition) | AP 시스템 (Availability & Partition) |
|:---|:---|:---|
| 최우선 가치 | 데이터 무결성 및 엄격한 정합성 | 시스템 무중단 가용성 (High Availability) |
| 분할 시 동작 | 정족수 미달 시 쓰기/읽기 차단 및 에러| 구버전 데이터(Stale)라도 무조건 성공 응답 |
| 대표 엔진 | MongoDB, HBase, Redis Cluster, Spanner| Cassandra, DynamoDB, CouchDB, Riak |
| 주 활용 분야 | 은행 계좌 이체, 결제 원장, 주식 주문 | SNS 피드, 쇼핑몰 장바구니, IoT 센서 수집 |

#### 한줄 요약
- 데이터 정확성이 최우선이면 CP, 무중단 고가용성이 최우선이면 AP 시스템을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tunable Consistency**: Cassandra 등에서 쿼리마다 정족수 레벨(ONE, QUORUM, ALL)을 동적으로 지정하여 CP/AP를 유연하게 조절하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AP 시스템 채택 시 비즈니스 데이터 불일치 발생 | 가변 일관성(**Tunable Consistency**: $R + W > N$) 강제 설정 | AP 기반 DB에서 강력한 일관성 확보 |
| CP 시스템 채택 시 네트워크 단절로 인한 쿼리 타임아웃 | Circuit Breaker 패턴 연동 및 캐시 기반 Fallback 응답 구성 | 서비스 전면 장애 전파 차단 |
| AP 환경에서 노드 간 동시 쓰기로 인한 충돌(Conflict) | Vector Clock 및 Last-Write-Wins(LWW) 충돌 해결기 적용 | 충돌 데이터의 원활한 최종 수렴 |
| PACELC 관점의 정상 시 지연시간(Latency) 증가 | 로컬 리전 내 복제본 우선 읽기(Local **Quorum**) 정책 적용 | 글로벌 네트워크 지연 최소화 |

#### 한줄 요약
- 가변 정족수 튜닝, 서킷 브레이커 도입, 충돌 해결 메커니즘, Local Quorum으로 CAP의 한계를 보완한다.

## Ⅶ. 결론

- 글로벌 분산 컴퓨팅 및 클라우드 네이티브 데이터베이스 설계의 **가장 근본적인 아키텍처 제약 원칙**으로 확립되었으며, 실무 시스템 구축 시에는 **금융 결제·원장 등 정합성 중심 도메인에는 정족수 과반수를 강제하는 CP(Spanner/MongoDB), SNS 피드·쇼핑몰 장바구니 등 무중단 고가용성 중심 도메인에는 최종 일관성(Eventual Consistency) 기반의 AP(Cassandra/DynamoDB)를 배치하고, PACELC 이론에 기초한 Tunable Consistency($R+W>N$) 및 Local Quorum 최적화**를 결합하여 상황별 최적의 데이터 신뢰성을 확보

#### 한줄 요약
- CAP 정리는 분산 컴퓨팅의 절대 원칙이며, 네트워크 분할 내성 하에서 비즈니스 도메인에 부합하는 CP와 AP의 최적 배치가 핵심이다.
