---
sidebar:
  order: 121
  label: "121. 정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 121
extra:
  question_no: "121"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Exactly-once는 중복 방지•커밋 설계 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **EOS (Exactly-Once Semantics / 정확히 한 번 처리)**: 메시징/스트리밍 시스템에서 네트워크 재시도, 시스템 다운, 컨슈머 장애가 발생하더라도 메시지 유실(Zero Loss)과 메시지 중복(Zero Duplication)을 동시에 100% 방지하여, 최종 결과 시스템에 단 1번만 계산 결과가 반영되는 최고 등급 데이터 처리 보장 보증.
- **At-Least-Once (최소 한 번 처리)**: 메시지 유실은 없으나 수신 재시도로 인한 데이터 중복이 발생할 수 있는 보장 레벨.
- **At-Most-Once (최대 한 번 처리)**: 메시지 중복은 없으나 네트워크 장애 시 데이터 유실이 발생할 수 있는 보장 레벨.

</details>

- 정의/개념: 시스템 분산 장애 및 재시도(Retry) 속에서도 데이터 유실과 데이터 중복을 100% 차단하여 최종 타깃 시스템에 단 한 번(Exactly-Once)만 비즈니스 결과를 렌더링하는 최고 등급 메시징 처리 보장 메커니즘인 **EOS**
- 배경/필요성: 금융 이체, 결제 승인, 실시간 계산기 등 1건의 중복이나 유실도 허용되지 않는 미션 크리티컬 도메인의 데이터 무결성 보장 요구성

#### 한줄 요약

- 이벤트를 다시 읽더라도 장부에는 한 번 반영된 효과를 만듦이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Idempotency (멱등성)**: 동일한 연산을 N번 반복 수행하더라도 최종 결과 상태가 1번 수행한 결과와 완전히 동일하게 유지되는 성질.
- **Two-Phase Commit (2PC) Sink**: 스트림 처리 엔진과 타깃 저장소(DB, Kafka) 간에 2단계 커밋을 적용하여 비동기 커밋 원자성 달성.

</details>

- **Zero Loss (유실 0%) & Zero Duplication (중복 0%)**
- **Idempotent Producer & Transactional Consumer (멱등 생산자 및 트랜잭션 소비자)**
- **End-to-End Exactly-Once (Source $\rightarrow$ Engine $\rightarrow$ Sink 전체 구간 2PC 보장)**

#### 한줄 요약

- 정확히 한 번은 내부 함수 호출 횟수가 아니라 재시도 뒤 최종 장부에 남는 논리적 효과가 한 번임을 뜻하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소 (End-to-End EOS 3대 통합 레벨)

<details><summary>핵심 용어</summary>

- **Transactional Coordinator**: Kafka/Flink 내부에서 트랜잭션 오프셋과 상태 스냅샷을 단일 트랜잭션 ID로 묶어 atomic commit을 관장하는 보장 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   End-to-End Exactly-Once Semantics (EOS)              │
├────────────────────────────────────────────────────────────────────────┤
│ [1. Replayable Source]  ──► [2. Stateful Engine]  ──► [3. Transactional Sink]
│ (Kafka Partition Offset)     (Flink/Spark Checkpoint) (Two-Phase Commit 2PC)
│ (재생 가능 소스)             (상태 스냅샷)            (원자적 출력 확정)
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Source(Offset), Engine(Checkpoint), Sink(2PC/Idempotent) 3개 영역이 모두 삼위일체로 맞물려야만 End-to-End EOS가 달성되는 아키텍처.

| EOS 구현 영역 | 필수 전제 조건 및 기술 메커니즘 | 미충족 시 발생하는 위험 요소 |
|:---|:---|:---|
| **1. Replayable Source** | **과거 특정 Offset으로 되돌아가 재시작 가능 (Kafka)** | 파티션 데이터 소멸 시 유실 발생 |
| **2. Stateful Engine** | **Chandy-Lamport 알고리즘 기반 Checkpoint 스냅샷**| 엔진 다운 시 연산 상태 파행 |
| **3. Transactional / Idempotent Sink**| **2PC (Two-Phase Commit) 또는 Idempotency Key 적용**| 타깃 DB에 중복 인서트 렌더링 |

#### 한줄 요약

- 재생 원본, 계산 상태, 복구 사진, 확정 관리자, 중복 방지 장부로 구성된다.

## Ⅳ. 흐름도 (Kafka & Flink 2PC 기반 End-to-End EOS 흐름)

<details><summary>핵심 용어</summary>

- **Two-Phase Commit Protocol in Flink**: `beginTransaction()` $\rightarrow$ `preCommit()` $\rightarrow$ `commit()` 3단계 훅(Hook)을 통한 타깃 시스템 원자적 출력.

</details>

```text
[Source Read] ──► [Pre-Commit Phase: Target DB에 임시 Transaction 열고 Write]
                           │
                           ▼ (Engine Checkpoint Barrier 도달 성공 시)
                  [Commit Phase: Target DB 임시 Transaction 최종 Commit!]
```

### 동작 원리

1. **Pre-Commit Phase**: Flink가 Sink DB에 트랜잭션을 열고 데이터를 렌더링하되 아직 Commit하지 않음 (Uncommitted 상태).
2. **Checkpoint Barrier**: Engine의 모든 Checkpoint 저장이 무사히 성공.
3. **Commit Phase**: Flink가 Sink DB에 `commit()` 신호를 전파하여 타깃 DB에 데이터를 단 1번 최종 커밋 확정 (**End-to-End EOS 완결**).

#### 한줄 요약

- 읽던 위치와 계산 상태의 사진이 안전하게 저장된 뒤 그 구간의 외부 결과를 확정한다.

## Ⅴ. 종류 및 비교 (메시징 3대 처리 보장 수준 비교)

<details><summary>핵심 용어</summary>

- **Processing Guarantee Tradeoff**: Exactly-Once는 최고 안전성을 제공하지만, 2PC 락 및 멱등성 검사로 인해 Latency가 At-Least-Once 대비 약 20~30% 저하.

</details>

| 처리 보장 레벨 | At-Most-Once (최대 1번) | At-Least-Once (최소 1번) | Exactly-Once (정확히 1번) |
|:---|:---|:---|:---|
| **데이터 유실 위험**| **유실 발생 가능 (Loss)** | **유실 0% (Zero Loss)** | **유실 0% (Zero Loss)** |
| **데이터 중복 위험**| **중복 없음 (Zero Duplication)**| **중복 발생 가능 (Duplication)**| **중복 0% (Zero Duplication)** |
| **네트워크 재시도** | 안 함 (Fire and Forget) | 성공할 때까지 계속 재시도 | 멱등성/2PC 기반 재시도 |
| **처리 성능 (TPS)** | **최상 (Sub-millisecond)** | 상 (고성능) | **중간 (2PC/스냅샷 오버헤드)** |

#### 한줄 요약

- 다시 실행해도 장부 효과가 한 번만 남도록 입력•계산•출력의 확정을 묶는다.

## Ⅵ. 실무 고려사항 및 대책 (EOS 구현 시 2대 난제 해결책)

<details><summary>핵심 용어</summary>

- **Non-Idempotent Sink Danger**: Sink DB가 `INSERT` 전용이고 Unique Key가 없는 구조일 경우 2PC가 실패하면 무조건 중복 데이터 발생.

</details>

| 2대 EOS 장애 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Non-Idempotent Sink** | Unique Constraint 없는 일반 RDBMS `INSERT` | **`UPSERT` (Merge Into) 또는 Unique Key 멱등 식별자 부여** |
| **2. Transaction Timeout** | Kafka/Flink 트랜잭션 보존 시간(`transaction.timeout.ms`) 초과 | **`transaction.timeout.ms` 확장 및 Checkpoint 주기 동기화**|

> 사례: **카카오페이 / 토스 실시간 결제 스트림 파이프라인 Kafka-Flink EOS 적용**

#### 한줄 요약

- 같은 결제 번호가 다시 와도 새 거래로 세지 않고 처음 결과를 재사용한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **EOS 수립 기준(Exactly-Once Semantics Standards)**: Replayable Source, Flink Checkpoint, 2PC Sink 및 Idempotent UPSERT에 의거한 체계.

</details>

- **EOS 수립 기준**에 따라 금융/결제 스트림 구축 시 **End-to-End Exactly-Once (Kafka + Flink 2PC)** 필수 적용

#### 한줄 요약

- 몇 번 다시 실행됐는지가 아니라 최종 장부에 몇 번 반영됐는지가 기준이다.
