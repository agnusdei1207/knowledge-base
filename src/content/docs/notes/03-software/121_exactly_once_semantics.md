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

- **EOS (Exactly-Once Semantics / 정확히 한 번 처리)**: 메시징/스트리밍 시스템에서 네트워크 재시도, 시스템 다운 등 장애 상황에서도 메시지 유실(Zero Loss)과 메시지 중복(Zero Duplication)을 방지하여 최종 목적지에 단 1회만 계산 결과가 반영되도록 보장하는 고신뢰 데이터 처리 메커니즘.
- **At-Least-Once (최소 한 번 처리)**: 메시지 유실은 없으나 수신 재시도로 인해 데이터 중복이 발생할 수 있는 보장 레벨.
- **At-Most-Once (최대 한 번 처리)**: 메시지 중복은 없으나 네트워크 장애 시 데이터 유실이 발생할 수 있는 보장 레벨.

</details>

- 정의/개념: 분산 환경의 장애 및 재시도(Retry) 과정에서 데이터 유실과 중복을 차단하여 최종 타깃에 단 한 번(Exactly-Once)만 비즈니스 결과가 반영되도록 하는 최고 등급 메시징 처리 보장 메커니즘.
- 배경/필요성: 금융 이체, 결제 승인 등 데이터 무결성과 정합성이 필수적인 미션 크리티컬 도메인의 요구사항 충족.

#### 한줄 요약

- 장애 발생 시 재처리해도 타깃 시스템에 결과가 중복 반영되지 않도록 관리하는 원칙.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Idempotency (멱등성)**: 동일 연산을 반복 수행해도 최종 상태가 1번 수행한 결과와 동일하게 유지되는 성질.
- **2PC (Two-Phase Commit / 2단계 커밋)**: 스트림 처리 엔진과 타깃 저장소 간 트랜잭션을 준비(Prepare)와 커밋(Commit) 단계로 나누어 원자성을 보장하는 분산 트랜잭션 프로토콜.

</details>

- **Zero Loss (유실 0%) & Zero Duplication (중복 0%)**
- **Idempotent Producer & Transactional Consumer (멱등 생산자 및 트랜잭션 소비자)**
- **End-to-End Exactly-Once (Source $\rightarrow$ Engine $\rightarrow$ Sink 전체 구간 2PC 보장)**

#### 한줄 요약

- 재시도 시에도 데이터 처리의 최종 장부상 반영 횟수가 단 1회임을 보장하는 논리적 정합성 원칙.

## Ⅲ. 구조 및 구성요소 (End-to-End EOS 3대 통합 레벨)

<details><summary>핵심 용어</summary>

- **Transactional Coordinator**: Kafka/Flink 내부에서 트랜잭션 오프셋과 상태 스냅샷을 단일 트랜잭션 ID로 묶어 atomic commit을 관장하는 보장 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   End-to-End Exactly-Once Semantics (EOS)              │
├────────────────────────────────────────────────────────────────────────┤
│ [1. Replayable Source]  ──► [2. Stateful Engine]  ──► [3. Transactional Sink]
│ (카프카 파티션 오프셋)     (플링크/스파크 스냅샷) (2단계 커밋 확정)
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Source(Offset), Engine(Checkpoint), Sink(2PC/Idempotent) 3개 영역이 모두 삼위일체로 맞물려야만 End-to-End EOS가 달성되는 아키텍처.

| EOS 구현 영역 | 필수 전제 조건 및 기술 메커니즘 | 미충족 시 발생하는 위험 요소 |
|:---|:---|:---|
| **1. 재생 가능 소스 (Replayable Source)** | **과거 특정 오프셋 재시작 가능 (카프카)** | 파티션 데이터 소멸 시 유실 발생 |
| **2. 상태 유지 엔진 (Stateful Engine)** | **Chandy-Lamport 알고리즘 기반 스냅샷**| 엔진 장애 시 연산 상태 파행 |
| **3. 트랜잭션/멱등 출력 (Transactional Sink)**| **2단계 커밋(2PC) 또는 멱등 식별자 적용**| 타깃 DB에 중복 반영 |

#### 한줄 요약

- 재생 가능한 원본, 엔진 상태 스냅샷, 분산 트랜잭션 확정 관리자로 구성.

## Ⅳ. 흐름도 (Kafka & Flink 2PC 기반 End-to-End EOS 흐름)

<details><summary>핵심 용어</summary>

- **Two-Phase Commit Protocol in Flink**: `beginTransaction()` $\rightarrow$ `preCommit()` $\rightarrow$ `commit()` 3단계 훅(Hook)을 통한 타깃 시스템 원자적 출력.

</details>

```text
[소스 읽기] ──► [준비 단계: 타깃 DB에 임시 트랜잭션 열고 쓰기]
                            │
                            ▼ (엔진 스냅샷 성공 시)
                   [확정 단계: 타깃 DB 임시 트랜잭션 최종 커밋!]
```

### 동작 원리

1. **준비 단계(Pre-Commit)**: Sink DB에 트랜잭션을 열고 데이터를 쓰되 확정하지 않음(미커밋 상태).
2. **스냅샷 장벽(Checkpoint Barrier)**: 엔진 상태 저장이 성공.
3. **확정 단계(Commit)**: `commit()` 신호를 전파하여 타깃 DB에 데이터를 단 1회 확정.

#### 한줄 요약

- 입력 오프셋과 상태 스냅샷이 동기화된 이후 외부 확정을 수행하여 정합성 보장.

## Ⅴ. 종류 및 비교 (메시징 3대 처리 보장 수준 비교)

<details><summary>핵심 용어</summary>

- **트랜잭션 비용 (Performance Tradeoff)**: 2PC 락 및 멱등성 검사로 인해 최소 1번 처리(At-Least-Once) 대비 지연 시간 발생.

</details>

| 처리 보장 레벨 | At-Most-Once (최대 1번) | At-Least-Once (최소 1번) | Exactly-Once (정확히 1번) |
|:---|:---|:---|:---|
| **데이터 유실 위험**| **유실 발생 가능 (Loss)** | **유실 0% (Zero Loss)** | **유실 0% (Zero Loss)** |
| **데이터 중복 위험**| **중복 없음 (Zero Duplication)**| **중복 발생 가능 (Duplication)**| **중복 0% (Zero Duplication)** |
| **네트워크 재시도** | 안 함 (Fire and Forget) | 성공할 때까지 계속 재시도 | 멱등성/2PC 기반 재시도 |
| **처리 성능 (TPS)** | **최상 (Sub-millisecond)** | 상 (고성능) | **중간 (2PC/스냅샷 오버헤드)** |

#### 한줄 요약

- 데이터 처리 시 입력, 계산, 출력 단계별 확정 관리로 결과 무결성 달성.

## Ⅵ. 실무 고려사항 및 대책 (EOS 구현 시 2대 난제 해결책)

<details><summary>핵심 용어</summary>

- **멱등성 부재 출력 위험 (Non-Idempotent Sink)**: Sink DB가 Unique Key 없는 INSERT 전용일 경우 장애 시 중복 데이터 발생 위험.

</details>

| 2대 EOS 장애 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 멱등성 미지원** | Unique Constraint 없는 일반 INSERT | **UPSERT(Merge Into) 또는 고유 식별자 부여** |
| **2. 트랜잭션 타임아웃** | 보존 시간(`transaction.timeout.ms`) 초과 | **설정값 확장 및 스냅샷 주기 동기화**|

> 사례: **카카오페이 / 토스 실시간 결제 스트림 파이프라인 Kafka-Flink EOS 적용**

#### 한줄 요약

- 동일한 거래 식별자 기반의 중복 요청 필터링을 통해 결과 무결성 유지.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **EOS 수립 기준**: 재생 가능 소스, 엔진 스냅샷, 2단계 커밋 확정 및 멱등성 기반의 데이터 처리 체계.

</details>

- **EOS 수립 기준**에 따라 금융/결제 스트림 구축 시 End-to-End Exactly-Once(Kafka+Flink 2PC) 체계 적용

#### 한줄 요약

- 최종 데이터 반영 정합성 보장 체계 적용
