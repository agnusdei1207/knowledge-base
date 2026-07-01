---
title: "Exactly-Once Semantics 정확히 한 번 처리 (Exactly-Once Semantics)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 314
---

# 📖 【암기용】 개념 완전 이해

> 목적: Exactly-Once Semantics를 이벤트가 실제 물리적으로 한 번만 도착한다는 뜻이 아니라, 장애와 재시도 후에도 최종 결과가 한 번 처리한 것과 같게 만드는 보장으로 이해하게 만든다.

## 한눈에
- **개요**: 재시도·장애 상황에서도 처리 결과가 중복·손실 없이 한 번 반영되도록 하는 의미론
- **왜 필요한가**: 결제, 정산, 재고 차감에서 같은 이벤트가 두 번 반영되면 금전·재고 오류가 발생한다.
- **핵심 직관**: 같은 쿠폰을 여러 번 스캔해도 시스템이 쿠폰 ID를 보고 한 번만 사용 처리하는 것과 같다.

## 깊이 이해
- **배경·문제의식**: 분산 시스템은 네트워크 실패, producer 재시도, consumer 재시작, sink commit 실패가 발생해 중복 또는 손실 위험이 생긴다.
- **작동 원리**: Kafka는 idempotent producer와 transaction으로 중복 로그 기록과 atomic write를 줄이고, Flink는 checkpoint와 transactional sink로 source offset, state, output commit을 맞춘다.
- **비유**: 택배 기사가 배송 완료 버튼을 두 번 눌러도 운송장 번호로 이미 완료된 건은 한 번만 기록하는 구조다.
- **구체 예시**: Flink가 Kafka에서 결제 이벤트를 읽어 집계 후 Kafka sink에 쓸 때 checkpoint 사이의 출력은 transaction으로 묶고, 장애 시 미완료 transaction을 abort한다.
- **흔한 오해·주의점**: Exactly-once는 모든 외부 시스템에 자동 적용되지 않는다. source, processor, sink가 offset, state, commit을 함께 조정해야 한다.

## 연결 개념
- Idempotence — 같은 요청 반복 시 결과 불변
- Transactional Sink — commit/abort로 결과 원자성 보장
- Checkpoint — 처리 상태와 입력 위치의 복구 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Exactly-once는 메시지 물리 전달 횟수가 아니라 최종 처리 결과의 의미론이며, source-state-sink 원자성 조건을 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Exactly-Once Semantics는 장애와 재시도 후에도 최종 상태가 각 이벤트를 한 번 처리한 결과와 같게 만드는 처리 보장임.
> 2. **가치**: 결제, 정산, 재고, feature update에서 중복 반영과 누락 반영을 통제함.
> 3. **판단 포인트**: idempotent producer, transaction, checkpoint, offset commit, sink 원자성, deduplication key가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전달 보장 개념 확인 | at-most/at-least/exactly-once 차이 | 물리적 1회 도착으로 오해 |
| 분산 처리 설계 확인 | source offset, state, sink commit 일치 | Kafka 단독 기능으로 설명 |
| 운영 리스크 판단 확인 | transaction timeout, idempotent sink, dedup | 성능 지표만 강조 |

> 요약: 이 문제는 최종 결과 기준의 보장과 이를 위한 원자적 commit 조건을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 결과 기준 단일 처리 보장
- 배경: 분산 스트리밍은 producer retry, consumer crash, sink timeout으로 중복·손실 처리 위험이 있음.
- 필요성: 금전·재고·정산 데이터는 이벤트 중복 반영을 허용하지 않으므로 idempotence와 transaction이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Source Offset -> Processor State / Checkpoint -> Transactional Sink
        +-> Idempotent Producer
        +-> Deduplication Key / Commit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Offset | 입력 처리 위치 추적 | commit timing 중요 |
| Processor State | 집계·join 상태 저장 | checkpoint와 결합 |
| Transactional Sink | 출력 commit/abort 제어 | Kafka transaction, DB transaction |
| Idempotency Key | 중복 요청 식별 | event id, business key |

> 요약: Exactly-once는 입력 위치, 처리 상태, 출력 commit이 같은 복구 지점으로 묶일 때 성립한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 읽기 -> state 갱신 -> 출력 transaction 시작
-> checkpoint 완료 -> sink commit -> offset commit / 장애 시 rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | source offset과 event id를 읽음 | offset tracking |
| 2 | state를 갱신하고 checkpoint에 포함 | state consistency |
| 3 | sink 결과를 transaction 또는 idempotent key로 기록 | commit atomicity |
| 4 | 장애 시 checkpoint 이후 record를 재처리하고 중복 반영을 차단 | duplicate audit |

> 요약: 장애 후 재처리는 발생할 수 있으나 최종 sink 결과가 한 번 처리한 상태와 같아야 exactly-once다.

---

## Ⅳ. 특징

| 구분 | At-Most-Once | At-Least-Once | Exactly-Once |
|:---|:---|:---|:---|
| 손실 | 가능 | 방지 목표 | 방지 목표 |
| 중복 | 없음 또는 낮음 | 가능 | 결과 중복 차단 |
| 구현 | 처리 전 offset commit | 처리 후 offset commit | transaction/checkpoint 결합 |
| 적합 | 로그 샘플링 | 알림·검색 색인 | 결제·정산·재고 |

> 요약: Exactly-once는 at-least-once 재처리 위에 중복 결과를 차단하는 transaction 또는 idempotence가 결합된 모델이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 처리 비용 | at-least-once+중복 허용 | exactly-once | 중복 반영 비용 |
| sink 조건 | 일반 API | transaction/idempotent sink | 외부 시스템 지원 |
| 지연 | 낮은 commit 조정 | transaction commit 지연 | SLA와 정합성 우선순위 |

> 요약: exactly-once는 정합성 요구가 중복 처리 비용보다 클 때 적용하며 sink 지원 여부가 핵심 조건이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 가짜 보장 | sink가 transaction 미지원 | idempotency key, dedup table | duplicate rate |
| transaction timeout | checkpoint 지연·broker 설정 불일치 | timeout 조정, state 최적화 | aborted transaction |
| offset 불일치 | 처리 전 commit 또는 수동 commit 오류 | checkpoint-managed offset | replay mismatch |

> 요약: Exactly-once 실패는 대부분 sink 원자성, transaction 시간, offset commit 위치 불일치에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 중복 | business key 기준 중복 0건 | reconciliation query |
| 손실 | input-output count 검증 | audit table |
| 복구 | 장애 주입 후 결과 일치 | failover test |

> 요약: exactly-once 검증은 설정값이 아니라 장애 주입 후 business result가 중복·손실 없이 일치하는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 이벤트마다 immutable event id와 business key를 부여하고 sink에 unique constraint 또는 dedup table을 설계함.
2. Kafka producer는 idempotence와 transaction 설정을 사용하고, Flink는 checkpoint와 transactional sink를 함께 구성함.
3. 장애 주입 테스트로 producer retry, consumer restart, sink timeout 상황의 중복·손실 여부를 검증함.

**결론 (2줄):**
- 기술사 판단: exactly-once는 모든 스트림에 적용할 기본값이 아니라 금전·정산처럼 중복 비용이 큰 업무에 선택해야 함.
- 향후 방향: 스트리밍 보장은 Kafka transaction, Flink checkpoint, lakehouse atomic commit이 결합된 end-to-end 검증 중심으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Exactly-Once Semantics를 설명하시오" | source-state-sink commit 흐름 | at-most/at-least와 차이 |
| 요구사항 명시형 | "중복 없는 스트리밍 처리 방안을 제시하시오" | idempotency key와 transaction 설계 | sink 미지원·timeout 리스크 |

> 요약: 설명형은 의미론을, 방안형은 원자적 commit과 중복 차단 설계를 중심으로 작성한다.
