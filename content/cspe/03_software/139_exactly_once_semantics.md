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
- **개요**: Exactly-Once Semantics는 분산 스트림·메시징 시스템에서 장애·재시도가 있어도 최종 결과가 각 이벤트를 정확히 한 번 반영한 것과 동일하도록 만드는 **메시지 처리 보장 수준**(Delivery Guarantee)이다 — 코드가 물리적으로 한 번만 실행됨을 뜻하는 게 아니라, 재실행되더라도 눈에 보이는 결과가 한 번 처리한 상태와 같다는 뜻이다.
- **왜 필요한가**: 분산 시스템은 네트워크 단절, 컨슈머 재시작, sink 커밋 실패가 일상적으로 발생한다. 이런 장애 후 이벤트를 재시도하면 중복(같은 결제가 두 번 반영)되거나, 확인 없이 넘어가면 유실(결제가 아예 반영 안 됨)될 수 있다. 결제·정산·재고처럼 금액이 걸린 업무는 두 오류 모두 치명적이다.
- **핵심 직관**: 이체 버튼을 실수로 두 번 눌러도, "이 거래 번호는 이미 처리했다"는 표(멱등성 키)를 확인해 두 번째 요청은 무시하는 것과 같다 — 요청은 두 번 왔어도 결과는 한 번만 반영된다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 전달 보장(Delivery Guarantee) | 메시지가 몇 번 전달·반영되는지에 대한 시스템의 약속 — exactly-once가 속하는 상위 분류 | 택배 배송 규정(분실 없음/중복 없음 등) |
| At-Most-Once | 최대 한 번 — 실패해도 재전송 안 함, 유실 가능 | "한 번 던지고 안 던져도 그만" |
| At-Least-Once | 최소 한 번 — 확인 안 되면 재전송, 중복 가능 | "받았다는 답 올 때까지 계속 다시 보냄" |
| Exactly-Once | 정확히 한 번 반영된 것과 동일한 결과 | "몇 번 보내도 최종 장부엔 한 줄만" |
| 오프셋(Offset) | 컨슈머가 어디까지 읽었는지 가리키는 위치 | 책갈피 |
| 멱등성(Idempotency) | 같은 연산을 여러 번 적용해도 결과가 한 번 적용한 것과 같은 성질 | "켜기" 스위치는 몇 번 눌러도 결과는 항상 켜짐 |
| 멱등성 키(Idempotency Key) | 같은 요청·이벤트를 식별해 중복 반영을 막는 고유 값 | 거래 번호, 주문 번호 |
| 트랜잭션(Transaction) | 여러 작업(오프셋 커밋 + 결과 쓰기)을 하나의 원자적 단위로 묶는 것 | "전부 성공 또는 전부 취소" |
| 2단계 커밋(Two-Phase Commit) | 준비(prepare) 후 확정(commit)하는 2단계 절차로 여러 시스템 간 원자성을 맞추는 방식 | 계약서에 먼저 가서명 후 최종 도장 |

## 깊이 이해

### 세 가지 보장 수준이 왜 나뉘나 — 어디서 실패가 나는지로 구분
- 이벤트 처리는 "읽기(source) → 계산(processing) → 쓰기(sink)" 3단계다. 각 단계 사이 장애에 대한 재시도 여부에 따라 결과가 달라진다.
- At-most-once: 장애 시 재시도하지 않는다. 읽었는데 처리 중 죽으면 그 이벤트는 그냥 사라진다 — 유실.
- At-least-once: 장애 시 마지막으로 확인(ack)되지 않은 지점부터 다시 읽는다. 이미 처리했지만 offset commit 전에 죽었다면 같은 이벤트를 또 처리한다 — 중복.
- Exactly-once: at-least-once처럼 재시도는 하되(유실 방지), 재시도로 생긴 중복을 트랜잭션이나 멱등키로 걸러내(중복 방지) 결과만 한 번 반영된 것처럼 만든다.

### Kafka에서 exactly-once를 만드는 방법 — 수치로 이해
- **Producer 중복 방지(Idempotent Producer)**: 각 producer에 고유 PID(Producer ID)를 부여하고 메시지마다 sequence number를 붙인다. 같은 PID+sequence number가 브로커에 다시 오면 브로커가 중복으로 판단해 버린다. 예: producer가 네트워크 타임아웃으로 같은 레코드를 재전송해도 sequence number가 같으므로 브로커에는 한 번만 저장된다.
- **Transaction**: transactional.id를 설정하면 "input offset commit"과 "output record 쓰기"를 하나의 트랜잭션으로 묶는다. consumer는 read_committed 격리 수준으로 읽어, 커밋되지 않은(진행 중이거나 abort된) 트랜잭션의 레코드는 보이지 않는다.
- 예: 주문 이벤트를 읽어 결제 이벤트를 쓰는 job이 output 쓰기 중 죽으면 해당 트랜잭션은 미완료(abort) 상태로 남고, read_committed consumer는 그 output을 아예 보지 못한다. job이 재시작되어 같은 주문을 다시 처리하고 트랜잭션을 성공적으로 커밋해야만 output이 보인다 — 결과적으로 정확히 한 번만 반영된 것처럼 보인다.

### Flink의 2단계 커밋 sink — 수치 예제
- Flink는 체크포인트(138 참고)와 2단계 커밋을 결합한다. 체크포인트 시작 시 sink는 "새 트랜잭션을 준비(pre-commit)"만 해두고 실제 커밋은 하지 않는다. 체크포인트가 성공적으로 완료됐다는 통지(notifyCheckpointComplete)를 받은 뒤에야 트랜잭션을 확정 커밋한다.
- 예: 체크포인트 간격 30초, 세 번째 체크포인트(90초 시점)에서 job이 실패했다고 하자. 아직 커밋되지 않은 90초 시점 트랜잭션은 자동 폐기(abort)되고, job은 두 번째 체크포인트(60초 시점) 상태로 복구되어 60초~90초 구간 이벤트를 재처리한다. sink에는 90초 시점의 미완료 쓰기가 반영되지 않으므로 중복이 생기지 않는다.

### sink가 트랜잭션을 지원하지 않을 때 — 멱등키로 대체
- 모든 sink가 트랜잭션을 지원하지는 않는다(예: 단순 REST API, 일부 NoSQL). 이때는 비즈니스 키(예: order_id)에 DB unique constraint를 걸어 같은 order_id로 두 번 insert하면 두 번째는 실패·무시되도록 멱등 쓰기로 exactly-once와 동일한 효과를 낸다.
- 예: `INSERT INTO orders (order_id, amount) VALUES (...) ON CONFLICT (order_id) DO NOTHING` — order_id가 이미 있으면 재시도로 들어온 중복 이벤트를 조용히 무시한다.

### 비유와 흔한 오해
- **비유**: 은행 창구에서 이체 요청서를 두 번 제출해도, 요청서에 적힌 접수번호(멱등키)로 "이미 처리됨"을 확인하고 두 번째 요청서는 처리하지 않고 돌려보내는 것과 같다. 요청은 두 번 왔지만 계좌 잔액 변화는 한 번뿐이다.
- **흔한 오해 1**: "exactly-once는 코드가 정확히 한 번 실행된다는 뜻이다" — 틀렸다. 장애 시 코드·task는 몇 번이고 재실행될 수 있다. 보장하는 것은 "재실행 결과가 최종적으로 한 번 처리한 상태와 같다"는 것뿐이다.
- **흔한 오해 2**: "exactly-once를 켜면 모든 문제가 끝난다" — source부터 sink까지 오프셋·상태·트랜잭션이 전부 연결되어야 end-to-end exactly-once가 성립한다. 중간에 트랜잭션을 지원하지 않는 sink가 하나라도 끼면 그 지점에서 보장이 깨진다.

## 연결 개념
- Idempotency(멱등성) — 중복 요청이 와도 결과가 동일하게 유지되는 성질, sink에서 exactly-once를 구현하는 대체 수단
- Kafka Transaction — producer의 오프셋 커밋과 output 쓰기를 원자화하는 메커니즘
- Flink Checkpoint(138) — 상태와 소스 오프셋을 일관된 시점으로 스냅샷해 2단계 커밋과 연결하는 메커니즘

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

- 개요: Exactly-Once는 처리 결과를 한 번 반영된 상태로 보장하는 의미론임.
- 배경: 스트리밍 시스템은 장애·재시도·네트워크 오류로 중복 처리와 유실이 발생할 수 있음.
- 필요성: 금액·재고·정산 업무는 source부터 sink까지 end-to-end 정합성 설계가 필요함.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
