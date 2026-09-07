---
sidebar:
  order: 121
  label: "121. 정확히 한 번 처리 Exactly-Once"
  badge:
    text: "미출 · 50%"
    variant: note
title: "정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics)"
date: "2026-09-07T10:05:00+09:00"
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

- **EOS(Exactly-Once Semantics)**: 분산 스트리밍 환경에서 장애 재시도가 발생해도 데이터의 유실(Zero Loss)과 중복(Zero Duplication) 없이 결과가 단 1회만 반영되는 처리 보장 수준.
- **End-to-End EOS**: Source(재생 가능), Engine(상태 스냅샷), Sink(2PC 트랜잭션/멱등성)의 3단계가 모두 결합되어야만 달성되는 완전한 단일 반영 체계.

</details>

- 정의/개념: 분산 스트림 환경에서 시스템 장애나 재시도가 발생해도 데이터의 유실과 중복 없이 결과가 정확히 단 1회만 반영됨을 보장하는 처리 규약
- 배경/필요성: 분산 네트워크 타임아웃 및 장애 시 단순 재시도로 인한 **데이터 중복 처리(At-Least-Once) 또는 유실(At-Most-Once)에 따른 데이터 불일치 한계**

#### 한줄 요약
- Exactly-Once는 메시지를 한 번만 보내는 규약이 아니라 여러 번 도착해도 결과가 한 번만 반영되게 만드는 규약이므로, 비용은 전송이 아니라 상태와 출력을 함께 커밋하는 조정 단계에서 발생한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Idempotency(멱등성)**: 동일한 연산이나 메시지 처리를 여러 번 반복 수행하더라도 시스템의 최종 상태가 1회 수행 결과와 동일하게 유지되는 성질.
- **Two-Phase Commit Sink**: Flink 등의 스트림 엔진이 외부 Sink 스토리지와 연동하여 체크포인트 성공 시점에만 데이터를 영구 커밋하는 프로토콜.

</details>

- Source 재생, Engine 상태 스냅샷, Sink 2PC가 결합된 End-to-End **Exactly-Once** 보장
- 중복 수신 시에도 최종 상태를 1회로 유지하는 **멱등성(Idempotency)** 기반 쓰기
- 트랜잭션 코디네이터 및 체크포인트 장벽을 통한 분산 원자적 커밋(Atomic Commit)

#### 한줄 요약
- 멱등성 생산자와 2단계 커밋 소비자를 통해 장애 복구 시에도 100% 데이터 정합성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EOS 3대 구성요소**: Replayable Source(Kafka 오프셋), Stateful Engine(Flink Chandy-Lamport 스냅샷), Transactional Sink(2PC 지원 스토리지).

</details>

```text
[정확히 한 번 처리 (End-to-End EOS)]
├─ [재생 가능 소스 (Source)]
│  └─ Kafka / Kinesis (오프셋 기반 재공급)
├─ [상태 유지 엔진 (Engine)]
│  └─ Flink / Spark (체크포인트 스냅샷)
├─ [트랜잭션 조정자 (Coordinator)]
│  └─ 2PC 동기화 (체크포인트-커밋 연동)
└─ [트랜잭션/멱등 싱크 (Sink)]
   ├─ 2PC Transactional Sink (원자 커밋)
   └─ Idempotent Sink (UPSERT 중복 무해화)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 재생 가능 소스 (Source) | 장애 복구 시 지정된 체크포인트 오프셋부터 데이터를 유실 없이 재공급 | Kafka, Kinesis 등 |
| 상태 유지 엔진 (Engine) | 연산자 내부 상태와 읽기 오프셋을 Chandy-Lamport 알고리즘으로 동시 스냅샷 | Flink, Spark Streaming |
| 트랜잭션 조정자 | 스트림 체크포인트 완료 시점과 Sink 스토리지의 물리 커밋 시점을 1:1 동기화| 2PC Coordinator 역할 |
| 트랜잭션/멱등 Sink | 중복 메시지가 도달하더라도 2PC 트랜잭션 또는 UPSERT로 1회만 영구 반영 | Kafka Producer, RDB UPSERT |

#### 한줄 요약
- 재생 가능한 소스·스냅샷 가능한 상태·트랜잭션이나 멱등을 지원하는 싱크 중 하나라도 빠지면 나머지 둘이 갖춰져도 보장이 무너지므로, 보장 수준은 구성요소의 합이 아니라 전 구간의 최소 조건으로 결정된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Two-Phase Commit Sink 파이프라인**: 트랜잭션 시작 $\to$ 사전 기록(Pre-Commit) $\to$ 체크포인트 스냅샷 $\to$ 최종 커밋(Commit).

</details>

```text
스트림 데이터 유입 및 체크포인트 주기 도달
        │
   [트랜잭션 시작] Sink 연산자가 타깃 DB에 `beginTransaction()` 호출하여 임시 트랜잭션 오픈
        │
   [사전 기록 (Pre-Commit)] 처리 결과를 타깃 DB의 트랜잭션 버퍼에 사전 기록 (미확정 상태)
        │
   [상태 스냅샷 완료] 모든 연산자의 State 스냅샷이 S3에 저장되고 JobManager가 완료 판정
        │
   [최종 커밋 전파] JobManager가 Sink 연산자에 `commit()` 명령을 전파하여 물리 커밋 확정
        │
   장애 발생 시 이전 체크포인트로 롤백하고 열려있던 미완료 트랜잭션은 즉시 `abort()` 폐기
```

#### 한줄 요약
- 출력을 미리 기록해 두고 스냅샷이 끝난 뒤에야 확정하므로 결과는 체크포인트 주기만큼 늦게 보이며, 주기를 줄이면 지연은 짧아지지만 스냅샷 비용이 그만큼 자주 발생한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **처리 보장 3단계 레벨**: At-Most-Once(최대 1번), At-Least-Once(최소 1번), Exactly-Once(정확히 1번).

</details>

| 비교 항목 | At-Most-Once (최대 1번) | At-Least-Once (최소 1번) | Exactly-Once (정확히 1번) |
|:---|:---|:---|:---|
| 데이터 유실 위험 | 네트워크 장애 시 유실 발생 가능 | 유실 0% (Zero Loss 보장) | 유실 0% (Zero Loss 보장) |
| 데이터 중복 위험 | 중복 없음 | 재시도로 인한 중복 발생 가능 | 중복 0% (Zero Duplication 보장)|
| 처리 지연 및 오버헤드| 지연 없음 (최고 처리량) | 낮음 (단순 재시도 오버헤드) | 2PC 및 스냅샷으로 인한 추가 지연|
| 최적 적용 분야 | 단순 로그 수집, IoT 원격 센서 | 클릭스트림, 대용량 웹 로그 집계 | 금융 계좌 이체, 결제 정산, 재고 관리|

#### 한줄 요약
- 속도 중심은 At-Most-Once, 유실 방지는 At-Least-Once, 금융 결제는 Exactly-Once를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Non-Idempotent Sink Risk**: 대상 DB에 기본키(PK) 제약이 없어 단순 `INSERT`가 반복 실행될 경우 데이터가 N배로 증식하는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| PK 제약 없는 일반 `INSERT`로 인한 중복 데이터 증식 | `UPSERT` (Merge Into / ON DUPLICATE KEY UPDATE) 적용 | 중복 메시지 수신 시 자동 덮어쓰기 |
| 2PC 트랜잭션 유지 시간 초과로 타깃 DB 타임아웃 | `transaction.timeout.ms` 확장 및 Flink 체크포인트 주기 최적화 | 트랜잭션 만료 크래시 방지 |
| 분산 노드 크래시 후 미완료 좀비 트랜잭션 누적 | Kafka 트랜잭션 프로듀서의 `transactional.id` 고정 재사용 | 장애 재시작 시 이전 좀비 자동 정리 |
| 체크포인트 지연으로 인한 End-to-End Latency 증가 | 미니배치 버퍼 튜닝 및 RocksDB 증분 스냅샷 적용 | 지연시간 50% 단축 |

#### 한줄 요약
- UPSERT 멱등 쓰기, 트랜잭션 타임아웃 동기화, 트랜잭션 ID 재사용, 증분 스냅샷으로 운영한다.

## Ⅶ. 결론

- 엔터프라이즈 실시간 결제, 핀테크 정산 및 분산 이벤트 파이프라인의 **가장 강력한 최고 수준의 데이터 정합성 보장 표준**으로 확립되었으며, 실무 구축 시에는 **2PC 커밋 지연을 최소화하는 타임아웃/체크포인트 주기 최적화, 타깃 저장소의 `UPSERT`/고유키 제약을 활용한 멱등성(Idempotent) Sink 이중화, 좀비 트랜잭션을 방지하는 고정 `transactional.id` 거버넌스**를 결합하여 처리 지연(Latency)과 데이터 무결성 간의 최적 균형을 달성

#### 한줄 요약
- Exactly-Once는 재생 가능한 소스와 상태 스냅샷, 분산 2PC 커밋을 유기적으로 결합하여 장애 시에도 단 1회 처리를 보장하는 분산 컴퓨팅의 최고 정합성 모델이다.
