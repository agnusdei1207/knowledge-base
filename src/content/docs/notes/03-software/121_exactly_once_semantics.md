---
sidebar:
  order: 121
  label: "121. 정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics)"
date: "2026-08-13T22:45:00+09:00"
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

<details><summary>용어 설명</summary>

- **EOS (Exactly-Once Semantics)**: 분산 스트리밍 환경에서 네트워크 재시도, 시스템 장애 시에도 메시지 유실(Zero Loss) 및 중복(Zero Duplication) 없이 단 1회만 처리를 보장하는 메커니즘.
- **At-Least-Once (최소 한 번 처리)**: 메시지 유실은 없으나 수신 재시도로 인해 데이터 중복 가능성이 있는 보장 레벨.
- **At-Most-Once (최대 한 번 처리)**: 메시지 중복은 없으나 네트워크 장애 시 데이터 유실이 발생할 수 있는 보장 레벨.

</details>

- 정의/개념: 재시도 후에도 결과를 한 번만 반영하는 **Exactly-Once**
- 배경/필요성: 장애 복구 재처리는 **중복 반영•오프셋 유실** 위험 유발

#### 한줄 요약

- 장애 발생 시 재처리해도 타깃 시스템에 결과가 중복 반영되지 않도록 관리하는 원칙.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Idempotency (멱등성)**: 동일 연산을 반복 수행해도 최종 상태가 1번 수행한 결과와 동일하게 유지되는 성질.
- **2PC (Two-Phase Commit / 2단계 커밋)**: 스트림 처리 엔진과 타깃 저장소 간 트랜잭션을 준비(Prepare)와 커밋(Commit) 단계로 나누어 원자성을 보장하는 분산 트랜잭션 프로토콜.

</details>

- **결과 단일 반영**: 입력 위치•상태•출력 확정의 일관성
- **Idempotent Producer & Transactional Consumer (멱등 생산자 및 트랜잭션 소비자)**
- **End-to-End Exactly-Once (Source $\rightarrow$ Engine $\rightarrow$ Sink 전체 구간 2PC 보장)**

#### 한줄 요약

- 재시도 시에도 데이터 처리의 최종 장부상 반영 횟수가 단 1회임을 보장하는 논리적 정합성 원칙.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Transactional Coordinator**: Kafka/Flink 내부에서 트랜잭션 오프셋과 상태 스냅샷을 단일 트랜잭션 ID로 묶어 atomic commit을 관장하는 보장 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   End-to-End Exactly-Once Semantics (EOS)              │
├────────────────────────────────────────────────────────────────────────┤
│ [1. 재처리 가능 소스] ──► [2. 상태 유지 엔진] ──► [3. 트랜잭션 Sink]
│ (오프셋 관리)             (스냅샷 체크포인트)      (2단계 커밋 확정)
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Source(Offset), Engine(Checkpoint), Sink(2PC/Idempotent) 3개 영역이 모두 삼위일체로 맞물려야만 End-to-End EOS가 달성되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 재생 가능 소스 | 체크포인트 위치부터 입력 재공급 |
| 상태 스냅샷 | 입력 위치와 연산 상태를 함께 저장 |
| 트랜잭션 조정자 | 체크포인트와 출력 확정 순서 조정 |
| 트랜잭션•멱등 Sink | 중복 시도에도 결과를 한 번만 반영 |

#### 한줄 요약

- 재생 가능한 원본, 엔진 상태 스냅샷, 분산 트랜잭션 확정 관리자로 구성.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Two-Phase Commit Protocol in Flink**: `beginTransaction()` $\rightarrow$ `preCommit()` $\rightarrow$ `commit()` 3단계 훅(Hook)을 통한 타깃 시스템 원자적 출력.

</details>

```text
[이벤트 처리]
      │
      ▼
1. 출력 트랜잭션 시작
      │
      ▼
2. 출력 사전 기록
      │
      ▼
3. 상태•오프셋 스냅샷
      │
      ▼
4. 체크포인트 완료 판정
      │
      ▼
5. 출력 커밋•중단
```

### 동작 원리

1. 출력 트랜잭션 시작: 체크포인트별 Sink 거래 생성
2. 출력 사전 기록: 결과를 미확정 상태로 기록
3. 상태•오프셋 스냅샷: 연산 상태와 입력 위치 저장
4. 체크포인트 완료 판정: 모든 연산자 저장 성공 확인
5. 출력 커밋•중단: 성공 시 확정, 실패 시 폐기•재시도

#### 한줄 요약

- 입력 오프셋과 상태 스냅샷이 동기화된 이후 외부 확정을 수행하여 정합성 보장.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **트랜잭션 비용 (Performance Tradeoff)**: 2PC 락 및 멱등성 검사로 인해 최소 1번 처리(At-Least-Once) 대비 지연 시간 발생.

</details>

| 처리 보장 레벨 | At-Most-Once (최대 1번) | At-Least-Once (최소 1번) | Exactly-Once (정확히 1번) |
|:---|:---|:---|:---|
| 처리 누락 위험 | ACK 전 손실 가능 | 재시도로 누락 억제 | 전체 경계 실패 시 보장 제한 |
| 중복 반영 위험 | 재시도하지 않아 낮음 | 재시도로 발생 가능 | 거래•멱등 경계에서 억제 |
| 네트워크 재시도 | 안 함 (Fire and Forget) | 성공할 때까지 계속 재시도 | 멱등성/2PC 기반 재시도 |
| 처리 성능  | **최상 ** | 상 (고성능) | **중간 (2PC/스냅샷 오버헤드)** |

#### 한줄 요약

- 데이터 처리 시 입력, 계산, 출력 단계별 확정 관리로 결과 무결성 달성.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **멱등성 부재 출력 위험 (Non-Idempotent Sink)**: Sink DB가 Unique Key 없는 INSERT 전용일 경우 장애 시 중복 데이터 발생 위험.

</details>

| 2대 EOS 장애 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. 멱등성 미지원 | Unique Constraint 없는 일반 INSERT | **UPSERT(Merge Into) 또는 고유 식별자 부여** |
| 2. 트랜잭션 타임아웃 | 보존 시간(`transaction.timeout.ms`) 초과 | **설정값 확장 및 스냅샷 주기 동기화**|

> 사례: **카카오페이 / 토스 실시간 결제 스트림 파이프라인 Kafka-Flink EOS 적용**

#### 한줄 요약

- 동일한 거래 식별자 기반의 중복 요청 필터링을 통해 결과 무결성 유지.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **EOS 수립 기준**: 재생 가능 소스, 엔진 스냅샷, 2단계 커밋 확정 및 멱등성 기반의 데이터 처리 체계.

</details>

- Sink 거래 지원은 **2PC**, 미지원 Sink는 멱등 키로 단일 반영

#### 한줄 요약

- 최종 데이터 반영 정합성 보장 체계 적용
