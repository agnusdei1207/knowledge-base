---
sidebar:
  order: 103
  label: "103. CAP 정리 (CAP Theorem)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "CAP 정리 (CAP Theorem)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **CAP Theorem (CAP 정리 / 브루어의 정리)**: Eric Brewer 교수가 제창한 분산 시스템 트레이드오프 정리로, 분산 데이터베이스 환경에서 일관성(Consistency), 가용성(Availability), 분할 내성(Partition Tolerance)의 3가지 특성을 100% 동시에 만족시키는 것은 절대 불가능하며, 무조건 2 가지만 선택할 수 있다는 이론.
- **Consistency (일관성, C)**: 분산 노드 중 어떤 노드에 읽기 쿼리를 던져도 항상 가장 최근에 쓰여진 동일하고 정확한 데이터를 반환받는 성질.
- **Availability (가용성, A)**: 일부 분산 노드가 다운되더라도, 살아있는 모든 노드는 항상 에러 없이 성공 응답을 반환받는 성질.
- **Partition Tolerance (분할 내성, P)**: 분산 노드 간의 네트워크 통신망이 절단(Network Partitioning)되거나 패킷이 유실되더라도 분산 시스템 전체가 계속 정상 구동되는 성질.

</details>

- 정의/개념: 분산 데이터베이스 시스템에서 네트워크 분할(P)이 발생하는 순간, 일관성(C)과 가용성(A)을 동시에 100% 만족시키는 것은 불가능하며 둘 중 하나를 포기해야 한다는 대전제인 **CAP Theorem**
- 배경/필요성: 네트워크 단절이라는 물리적 한계 상황(Network Partition) 발생 시, 데이터 불일치를 감수할 것인가(AP) 혹은 서비스 응답 실패를 감수할 것인가(CP)에 대한 아키텍처 선택 기준 정립 요구성

#### 한줄 요약

- 지점 간 전화가 끊기면 최신 장부를 확인할 때까지 멈출지, 임시 장부로 계속 영업할지 정해야 한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **P is Mandatory (P는 필수 선택 조건)**: 분산 네트워크 환경에서 통신 단절(P)은 제어 불가능한 물리적 장애이므로, 실질적 선택은 CP(일관성 선택) 대 AP(가용성 선택)의 2지선다로 귀결.
- **PACELC Theorem**: CAP 정리를 확장하여, 네트워크 분할(P) 시 A와 C의 선택, 정상(Else) 시 Latency(L)와 Consistency(C) 간의 트레이드오프를 설명한 확장 이론.

</details>

- 분산 네트워크 환경에서 **P(Partition Tolerance)는 불가피한 선택 항목**
- **CP (Consistency + Partition Tolerance)** 대 **AP (Availability + Partition Tolerance)** 상충 트레이드오프
- 정상 상태의 Latency(응답시간)와 Consistency를 다루는 **PACELC 정리**로 발전 확장

#### 한줄 요약

- 연결이 끊긴 동안 틀리지 않게 멈출지, 잠시 다를 수 있어도 답할지를 정한다.

## Ⅲ. 구조 및 구성요소 (CAP 3대 요소 & CP/AP/CA 분류)

<details><summary>핵심 용어</summary>

- **CP System (HBase, Redis, MongoDB, RDBMS Cluster)**: 네트워크 단절 시 데이터 일관성을 위해 에러를 내거나 읽기/쓰기를 블로킹하는 시스템.
- **AP System (Cassandra, DynamoDB, Couchbase)**: 네트워크 단절 시 데이터 불일치(Stale Data)를 감수하더라도 무조건 성공 응답을 반환하는 시스템.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                         CAP Theorem 3대 분류 구조                      │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. CP System      │ 2. AP System      │ 3. CA System (상상 속의 체계)  │
│ (Consistency + P) │ (Availability + P)│ (Consistency + Availability)   │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ • 네트워크 분할 시│ • 네트워크 분할 시│ • 네트워크 분할(P)이 절대 발생 │
│   응답 에러/블로킹│   최종일관성 허용 │   하지 않는 단일 DB 전제       │
│ • HBase, MongoDB  │ • Cassandra       │ • 단일 노드 RDBMS (Oracle, MySQL)│
└───────────────────┴───────────────────┴────────────────────────────────┘
```

선의 의미: 네트워크 분할(P) 발생 시 일관성(CP) 또는 가용성(AP)을 선택하는 트레이드오프 아키텍처.

| 구분 (Category) | 일관성 (Consistency) | 가용성 (Availability) | 분할 내성 (Partition) | 대표적 적용 DB |
|:---|:---|:---|:---|:---|
| **CP System** | **100% 완벽 보장 (Strict)** | **일부 응답 에러/블로킹 발생**| **수용 (P 보장)** | **HBase, MongoDB, Redis, Spanner** |
| **AP System** | **최종 일관성 (Eventual)** | **100% 에러 없이 성공 응답** | **수용 (P 보장)** | **Cassandra, DynamoDB, Couchbase** |
| **CA System** | **100% 완벽 보장** | **100% 성공 응답** | **미수용 (P 불가능)**| **단일 RDBMS (MySQL, PostgreSQL)**|

#### 한줄 요약

- 지점 연결 상태와 업무 규칙으로 멈출 요청과 계속할 요청을 나눈다.

## Ⅳ. 흐름도 (네트워크 분할 발생 시 CP 대 AP 수용 메커니즘)

<details><summary>핵심 용어</summary>

- **Quorum Check (정족수 검사)**: CP 시스템에서 노드 분할 시 과반수 노드(Quorum)에 도달하지 못하면 쓰기/읽기 연산을 거부하는 메커니즘.

</details>

```text
[Node 1] ─── (X Network Partition Cut X) ─── [Node 2]
    │                                            │
    ▼ (Client 가 Node 1 과 Node 2 에 동시 접근 시)   ▼
[CP 선택] : Node 2 는 동기화 실패로 에러(Error) 반환 ──► 일관성 보존 (C)
[AP 선택] : Node 2 는 구 데이터(Stale Data) 즉시 응답 ──► 가용성 보존 (A)
```

### 동작 원리

1. **Network Partition Event**: Node 1과 Node 2 사이의 네트워크 케이블 단절.
2. **Client Write to Node 1**: Node 1에 새로운 값 `X=20` 쓰기 완료.
3. **Client Read from Node 2**:
   - **CP (HBase)**: Node 2는 Node 1과 동기화가 안 되었음을 인지하고 **조회 거부 에러(Timeout Error)** 반환.
   - **AP (Cassandra)**: Node 2는 과거 값 `X=10`을 감수하고 **즉시 200 OK 응답** 반환 (추후 Eventual Consistency로 동기화).

#### 한줄 요약

- 다른 지점의 최신 장부를 확인하지 못할 때 CP는 멈추고 AP는 지역 장부로 처리한다.

## Ⅴ. 종류 및 비교 (PACELC 정리: CAP의 확장)

<details><summary>핵심 용어</summary>

- **PACELC Theorem**: If **P**artition: choose **A** or **C** / **E**lse (정상 상태): choose **L**atency or **C**onsistency.

</details>

| 분산 DB 제품 | PACELC 표기 | 장애 발생 시 (P) 선택 | 정상 구동 시 (Else) 선택 |
|:---|:---|:---|:---|
| **MongoDB / HBase** | **PC / EC** | **Consistency (일관성)** | **Consistency (일관성)** |
| **Cassandra / Dynamo**| **PA / EL** | **Availability (가용성)**| **Latency (속도/응답성)** |
| **Amazon DynamoDB** | **PA / EC** (설정가변) | **Availability (가용성)**| **Consistency (강한 일관성 옵션)** |

#### 한줄 요약

- CP는 틀린 답보다 중단을, AP는 중단보다 임시 차이를 택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Tunable Consistency (가변 일관성)**: Cassandra/DynamoDB에서 읽기/쓰기 시 정족수 레벨(ONE, QUORUM, ALL)을 쿼리별로 조정하여 CP와 AP 성격을 가변적으로 변경하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AP 데이터베이스 선택 시 비즈니스 일관성 파괴 | **Tunable Consistency (QUORUM: $R + W > N$) 설정** | 일관성/가용성 조율 |
| CP 데이터베이스 선택 시 네트워크 끊김에 의한 쿼리 타임아웃 | **Circuit Breaker 패턴 연동 및 빠른 Fallback 응답 구현** | 시스템 다운 방지 |
| AP 환경에서 데이터 충돌(Conflict) 발생 | **Vector Clock / LWW (Last-Write-Wins) 충돌 해결기 가동**| 데이터 수렴 완결 |

> 사례: **결제/금융 서비스는 CP (MongoDB/Spanner), SNS 피드/로그 서비스는 AP (Cassandra) 채택**

#### 한줄 요약

- 같은 쇼핑몰도 재고 판매는 멈추고 상품 설명은 잠시 오래된 값으로 보여줄 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CAP 선택 수립 기준(CAP Theorem Decision Standards)**: 비즈니스 허용 오차, RPO/RTO 목표 및 PACELC 트레이드오프 분석성에 의거한 체계.

</details>

- **CAP 선택 수립 기준**에 따라 도메인 특성에 맞춰 **금융 결제는 CP, 로깅/SNS는 AP 서비스** 필수 분리 수용

#### 한줄 요약

- CAP 정책 적용 기준은 분할 중 정확성•응답성과 복구 뒤 값의 수렴을 함께 다룬다.
