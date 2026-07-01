---
title: "정확히 한 번 처리 Exactly-Once (Exactly-Once Semantics)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 139
---

# 📖 【암기용】 개념 완전 이해

> 목적: Exactly-Once가 실제로는 source·state·sink가 함께 맞아야 하는 처리 보장임을 이해하게 만든다.

## 한눈에
- **개요**: 장애·재시도 후에도 결과 상태가 이벤트를 한 번 처리한 것과 같게 보장하는 의미론
- **왜 필요한가**: 결제·정산·포인트 적립은 중복 처리 시 금액 오류가 발생하고, 누락 처리 시 고객 피해가 발생함.
- **핵심 직관**: 택배 송장을 다시 스캔해도 재고 차감은 한 번만 반영되도록 장부와 스캔 위치를 같이 저장하는 방식임.

## 깊이 이해
- **배경·문제의식**: 분산 시스템은 네트워크 실패, consumer 재시작, sink commit 실패가 발생함. at-least-once는 중복 가능성이 있고, at-most-once는 유실 가능성이 있음. exactly-once는 처리 결과가 한 번 반영된 상태와 동일하도록 설계함.
- **작동 원리**: source offset, processing state, sink transaction commit을 checkpoint 또는 transaction으로 묶음. Kafka는 idempotent producer와 transaction id를 제공하고, Flink는 checkpoint와 two-phase commit sink를 사용함.
- **비유**: 은행 이체에서 버튼을 두 번 눌러도 idempotency key로 같은 거래는 한 번만 승인하는 구조임.
- **구체 예시**: Kafka Streams에서 producer idempotence와 transaction을 켜면 input offset commit과 output record write가 하나의 transaction으로 묶임.
- **흔한 오해·주의점**: Exactly-Once는 "코드가 한 번만 실행됨"이 아님. 장애 시 코드는 재실행될 수 있으나 최종 결과가 한 번 처리한 상태와 같다는 의미임.

## 연결 개념
- Idempotency — 중복 요청 결과 동일화
- Kafka Transaction — source offset과 output write 원자화
- Flink Checkpoint — state와 source offset snapshot

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Exactly-Once 문제에서 보장 수준, 구현 조건, 비용·한계를 명확히 판단함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Exactly-Once Semantics는 장애·재시도 후 최종 결과가 각 이벤트를 한 번 반영한 상태와 같도록 하는 처리 보장임.
> 2. **가치**: 결제·정산·포인트·재고처럼 중복·누락 비용이 큰 이벤트 처리에서 결과 정합성을 확보함.
> 3. **판단 포인트**: source offset, state checkpoint, sink transaction, idempotency key 중 하나라도 빠지면 end-to-end 보장이 깨짐.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메시징 보장 수준 이해 확인 | at-most-once, at-least-once, exactly-once | 정확히 한 번 실행으로 오해 |
| 구현 조건 판단 확인 | idempotent producer, transaction, checkpoint | sink DB idempotency 누락 |
| 비용·한계 확인 | latency, throughput, transaction timeout | 모든 이벤트에 무조건 적용한다고 단정 |

> 요약: Exactly-Once 답안은 처리 실행 횟수가 아니라 결과 상태 보장이라는 점을 명확히 해야 함.

---

## Ⅰ. 개요 및 필요성

Exactly-Once는 이벤트 처리 결과가 한 번 반영된 상태와 같도록 보장하는 의미론임. 스트리밍 시스템은 장애·재시도·네트워크 오류로 중복 처리와 유실이 발생할 수 있음. 금액·재고·정산 업무는 source부터 sink까지 end-to-end 정합성 설계가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Source Offset -> Processor State -> Checkpoint/Transaction
                              / Idempotency Key -> Sink Commit
                              / Recovery -> Replay from Offset
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Offset | 읽은 위치 추적 | commit 시점이 보장 수준 결정 |
| Processor State | 중간 집계 상태 | checkpoint와 함께 저장 |
| Transaction | output과 offset 원자화 | Kafka transaction, 2PC sink |
| Idempotency Key | 중복 반영 차단 | business key 기반 unique constraint |

> 요약: Exactly-Once는 offset, state, sink commit을 하나의 일관된 경계로 묶을 때 성립함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 읽기 -> state 갱신 -> sink write 준비
-> checkpoint/transaction 시작 -> offset+output commit -> 장애 시 replay
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | source에서 이벤트와 offset 수신 | offset monotonicity |
| 2 | processor state 갱신 | checkpoint 포함 여부 |
| 3 | sink에 transaction 또는 idempotent write | unique key, transaction id |
| 4 | commit 후 offset 확정 | duplicate output 0건 |

> 요약: 장애 시 이벤트는 다시 읽힐 수 있으나, sink commit과 idempotency가 중복 결과를 차단함.

---

## Ⅳ. 특징

| 구분 | At-Least-Once | Exactly-Once | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 유실 | 낮음 | 낮음 | replay 가능 |
| 중복 | 발생 가능 | 결과 중복 차단 | duplicate output 0건 |
| 비용 | 구조 단순 | transaction·checkpoint 비용 | p95 latency 증가 측정 |
| 적용 | 로그·알림 | 결제·정산·재고 | 업무 손실 금액 기준 |

> 요약: Exactly-Once는 중복 반영 비용이 큰 업무에 적용하고, 단순 로그는 at-least-once+dedup으로 충분할 수 있음.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | at-least-once + 수동 dedup | transaction/checkpoint 기반 | 금액·재고 정합성 필수 |
| 비용/성능 | 낮은 지연 | commit 경계 비용 | 지연 증가 허용치 10~30% |
| 운영/위험 | 중복 보정 필요 | transaction timeout 관리 | timeout, retry, poison message |

> 요약: Exactly-Once는 정합성 비용이 처리 지연 증가보다 클 때 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| end-to-end 단절 | sink가 transaction 미지원 | idempotent write, unique key | duplicate key violation |
| 처리 지연 | checkpoint·transaction 대기 | interval 조정, batch commit | p95 latency |
| poison message | 반복 실패 이벤트 | DLQ, retry limit | retry count, DLQ rate |

> 요약: Exactly-Once의 약점은 sink 연계와 지연이며, DLQ와 idempotency key로 운영 통제를 추가함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 중복 결과 | duplicate output 0건 | reconciliation query |
| 유실 결과 | missing event 0건 | source-sink count 비교 |
| 복구 | checkpoint restore 5분 이하 | 장애 주입 테스트 |

> 요약: 보장 수준은 장애 주입 후 중복·누락·복구 시간을 실제로 측정해야 확인됨.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. business event_id를 전 구간 표준화하고 sink DB에 unique constraint 또는 idempotency table을 둠
2. Kafka는 idempotent producer, transactional.id, read_committed consumer를 적용하고 transaction timeout을 SLA에 맞춤
3. Flink는 checkpoint interval 30초, two-phase commit sink, DLQ topic을 적용해 장애·독성 이벤트를 분리함

**결론 (2줄):**
- 기술사 판단: 금액·재고·정산은 Exactly-Once, 모니터링 로그·추천 노출 이벤트는 at-least-once+dedup을 선택함
- 향후 방향: streaming platform은 exactly-once 보장을 기본 제공하되, 최종 DB와 외부 API idempotency 설계가 계속 핵심임

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Exactly-Once를 설명하시오" | offset, state, sink commit 흐름 | 보장 수준별 차이 |
| 요구사항 명시형 | "구현 방안을 제시하시오", "비교하시오" | Kafka/Flink transaction, idempotency | 비용·지연·업무 중요도 선택 기준 |

> 요약: 설명형은 의미론, 방안형은 source-state-sink end-to-end 조건을 중심으로 작성함.
