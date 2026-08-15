---
sidebar:
  order: 103
  label: "103. CAP 정리 (CAP Theorem)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "CAP 정리 (CAP Theorem)"
date: "2026-08-13T20:38:00+09:00"
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

- **CAP Theorem (CAP 정리 / 브루어의 정리)**: Eric Brewer 교수가 제창한 분산 시스템 트레이드오프 정리로, 분산 데이터베이스 환경에서 일관성(Consistency), 가용성(Availability), 분할 내성(Partition Tolerance)의 3가지 특성을 100% 동시에 만족시키는 것은 절대 불가능하며, 무조건 2 가지만 선택할 수 있다는 이론.
- **Consistency (일관성, C)**: 분산 노드 중 어떤 노드에 읽기 쿼리를 던져도 항상 가장 최근에 쓰여진 동일하고 정확한 데이터를 반환받는 성질.
- **Availability (가용성, A)**: 일부 분산 노드가 다운되더라도, 살아있는 모든 노드는 항상 에러 없이 성공 응답을 반환받는 성질.
- **Partition Tolerance (분할 내성, P)**: 분산 노드 간의 네트워크 통신망이 절단(Network Partitioning)되거나 패킷이 유실되더라도 분산 시스템 전체가 계속 정상 구동되는 성질.

</details>

- 정의/개념: 분할 중 **일관성(C)•가용성(A)** 동시 보장 한계를 밝힌 CAP 정리
- 배경/필요성: 네트워크 분할 시 **정확한 응답•지속 응답** 동시 보장 불가

#### 한줄 요약

- 지점 간 전화가 끊기면 최신 장부를 확인할 때까지 멈출지, 임시 장부로 계속 영업할지 정해야 한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **P is Mandatory (P는 필수 선택 조건)**: 분산 네트워크 환경에서 통신 단절(P)은 제어 불가능한 물리적 장애이므로, 실질적 선택은 CP(일관성 선택) 대 AP(가용성 선택)의 2지선다로 귀결.
- **PACELC Theorem**: CAP 정리를 확장하여, 네트워크 분할(P) 시 A와 C의 선택, 정상(Else) 시 Latency(L)와 Consistency(C) 간의 트레이드오프를 설명한 확장 이론.

</details>

- **분할 내성(P)**: 분할 발생을 전제로 서비스 정책 판정
- **트레이드오프**: 일관성(C)과 가용성(A) 간의 상충 관계(CP 대 AP).
- **확장 이론(PACELC 정리)**: 분할 발생 시(`P`)의 선택과 정상 상태(`Else`)에서의 응답 속도(`L`) 및 일관성(`C`) 간의 절충안.

#### 한줄 요약

- 연결이 끊긴 동안 틀리지 않게 멈출지, 잠시 다를 수 있어도 답할지를 정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CP System (HBase, Redis, MongoDB, RDBMS Cluster)**: 네트워크 단절 시 데이터 일관성을 위해 에러를 내거나 읽기/쓰기를 블로킹하는 시스템.
- **AP System (Cassandra, DynamoDB, Couchbase)**: 네트워크 단절 시 데이터 불일치(Stale Data)를 감수하더라도 무조건 성공 응답을 반환하는 시스템.

</details>

| 구성요소 | 분할 중 보장 의미 |
|:---|:---|
| **Consistency** | 모든 정상 읽기가 최신 쓰기 또는 오류 반환 |
| **Availability** | 모든 정상 노드 요청이 유한 시간 내 응답 |
| **Partition Tolerance** | 노드 간 메시지 손실에도 시스템 동작 지속 |

#### 한줄 요약

- 지점 연결 상태와 업무 규칙으로 멈출 요청과 계속할 요청을 나눈다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Quorum Check (정족수 검사)**: CP 시스템에서 노드 분할 시 과반수 노드(Quorum)에 도달하지 못하면 쓰기/읽기 연산을 거부하는 메커니즘.

</details>

```text
[노드 간 분할 감지]
          │
          ▼
1. 정족수 도달 판정
          │
    ┌─────┴─────┐
    │미달       │지역 처리
    ▼           ▼
2. 요청 거부   3. 임시 응답
    │           │
    └─────┬─────┘
          ▼
4. 연결 복구 감지
          │
          ▼
5. 데이터 수렴
```

### 동작 원리

1. **정족수 도달 판정**: 최신 값을 확인할 노드 수 검사
2. **요청 거부**: CP 정책으로 불확실한 읽기•쓰기 차단
3. **임시 응답**: AP 정책으로 지역 복제본 기반 처리
4. **연결 복구 감지**: 노드 간 메시지 교환 재개 확인
5. **데이터 수렴**: 충돌 정책으로 복제본 차이 해소

#### 한줄 요약

- 다른 지점의 최신 장부를 확인하지 못할 때 CP는 멈추고 AP는 지역 장부로 처리한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PACELC Theorem**: If **P**artition: choose **A** or **C** / **E**lse (정상 상태): choose **L**atency or **C**onsistency.

</details>

| 분산 DB 제품 | PACELC 표기 | 장애 발생 시 (P) 선택 | 정상 구동 시 (Else) 선택 |
|:---|:---|:---|:---|
| **PC/EC** | 분할 중 일관성 | 정상 시 일관성 |
| **PA/EL** | 분할 중 가용성 | 정상 시 지연시간 |
| **가변 정책** | 요청별 정족수 선택 | 읽기 일관성 수준 선택 |

#### 한줄 요약

- CP는 틀린 답보다 중단을, AP는 중단보다 임시 차이를 택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **CAP 선택 수립 기준(CAP Theorem Decision Standards)**: 비즈니스 허용 오차, RPO/RTO 목표 및 PACELC 트레이드오프 분석성에 의거한 체계.

</details>

- 오류 응답이 허용되면 **CP**, 임시 불일치가 허용되면 AP 선택

#### 한줄 요약

- CAP 정책 적용 기준은 분할 중 정확성•응답성과 복구 뒤 값의 수렴을 함께 다룬다.
