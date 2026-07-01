---
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 138
---

# 📖 【암기용】 개념 완전 이해

> 목적: Flink가 Spark Streaming과 비교되는 지점인 stateful stream processing을 이해하게 만든다.

## 한눈에
- **개요**: 이벤트 시간, 상태 관리, checkpoint를 기반으로 연속 데이터를 처리하는 스트림 처리 엔진
- **왜 필요한가**: 실시간 이상탐지·정산·추천은 이벤트 도착 지연, 순서 뒤바뀜, 장애 복구 후 중복 처리까지 통제해야 함.
- **핵심 직관**: 컨베이어벨트 위 물건을 보며 즉시 계산하되, 중간 계산 장부를 주기적으로 금고에 저장하는 방식임.

## 깊이 이해
- **배경·문제의식**: 마이크로배치 방식은 처리 단위를 묶어 지연이 발생하고, event time 처리가 복잡함. Flink는 record-at-a-time 처리, event time window, checkpoint barrier로 상태 일관성을 관리함.
- **작동 원리**: source가 이벤트를 읽고 operator chain이 transformation을 수행함. keyed state는 RocksDB 또는 heap에 저장되고, checkpoint가 주기적으로 state snapshot을 만든다. 장애 시 checkpoint에서 state와 source offset을 복구함.
- **비유**: 택배 분류 작업 중 5분마다 현재 분류표를 저장해 두고, 정전이 나면 마지막 저장 시점부터 다시 시작하는 구조임.
- **구체 예시**: 결제 fraud 탐지에서 user_id key별 최근 10분 거래 횟수와 금액을 keyed state에 저장하고, watermark가 지나면 window 결과를 확정함.
- **흔한 오해·주의점**: Flink도 설정만으로 exactly-once가 완성되지 않음. source, state, sink가 checkpoint와 transaction commit을 함께 지원해야 함.

## 연결 개념
- Kafka — 주요 source/sink
- Exactly-Once Semantics — checkpoint와 transaction 연계
- Kappa Architecture — stream-only 아키텍처

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Flink 문제에서 event time, watermark, state, checkpoint, exactly-once를 연결해 답안화함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Flink는 event time과 stateful operator를 지원하는 low-latency stream processing engine임.
> 2. **가치**: checkpoint 기반 상태 복구와 watermark 기반 late event 처리로 연속 데이터 처리의 정합성을 확보함.
> 3. **판단 포인트**: state size, checkpoint interval, watermark delay, sink transaction 지원 여부가 설계 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스트림 처리 원리 확인 | event time, watermark, window, state | 단순 실시간 처리 엔진으로만 설명 |
| 장애 복구 판단 확인 | checkpoint, savepoint, state backend | exactly-once 조건 누락 |
| Spark/Kafka Streams 비교 확인 | record processing, stateful job | batch engine과 동일하게 서술 |

> 요약: Flink 답안은 event time 처리와 상태 일관성 보장을 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Apache Flink는 stateful stream processing engine임.
- 배경: 실시간 서비스는 초 단위 처리뿐 아니라 지연 도착 이벤트, 장애 복구, 중복 처리 제어가 필요함.
- 필요성: event time, watermark, checkpoint로 연속 데이터 처리의 정합성과 복구를 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Kafka Source -> Operator Chain -> Keyed State -> Window/Timer -> Sink
                         / Checkpoint Coordinator -> State Backend
                         / Watermark -> Event Time Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source | 이벤트 입력 | Kafka offset과 checkpoint 연계 |
| Operator | map, keyBy, window 처리 | operator chain 최적화 |
| Keyed State | key별 상태 저장 | RocksDB state backend 사용 가능 |
| Checkpoint | 상태 snapshot | interval, timeout, alignment 설정 |
| Watermark | event time 진행 제어 | late event 허용 범위 결정 |

> 요약: Flink는 source offset, operator state, sink commit을 checkpoint로 묶어 스트림 처리 상태를 복구함.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 수신 -> timestamp 추출 -> watermark 생성 -> keyed state 갱신
-> window/timer 평가 -> checkpoint snapshot -> sink commit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | source에서 record 읽기 | source lag |
| 2 | event time과 watermark 계산 | watermark delay |
| 3 | keyed state와 window 갱신 | state size, timer 수 |
| 4 | checkpoint 후 sink 반영 | checkpoint duration, failure count |

> 요약: Flink는 이벤트 시간을 기준으로 상태를 갱신하고 checkpoint를 통해 장애 후 동일 상태로 복구함.

---

## Ⅳ. 특징

| 구분 | Micro-batch 처리 | Apache Flink | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 처리 단위 | 배치 묶음 | record-at-a-time | end-to-end lag 1초 이하 목표 |
| 시간 모델 | processing time 중심 | event time + watermark | late event 허용 5분 |
| 상태 | 외부 저장소 의존 가능 | 내장 keyed state | state size GB~TB |
| 복구 | batch 재시작 | checkpoint/savepoint | checkpoint success 99.9% |

> 요약: Flink는 상태 기반 저지연 스트림에 적합하지만, state와 checkpoint 비용을 지속 측정해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Spark Structured Streaming | continuous stateful stream | sub-second, event time 요구 |
| 비용/성능 | micro-batch 운영 | checkpoint와 state 비용 | state size와 checkpoint SLA |
| 운영/위험 | batch job 운영 | savepoint 기반 배포 | state schema 변경 관리 |

> 요약: Flink는 fraud 탐지·실시간 정산처럼 event time과 state가 핵심인 업무에 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| checkpoint 지연 | state size 증가 | incremental checkpoint, RocksDB tuning | duration/interval 0.5 이하 |
| late event 누락 | watermark 과도 설정 | allowed lateness, side output | late drop count |
| state migration 실패 | schema 변경 | savepoint 검증, compatible serializer | restore failure 0건 |

> 요약: Flink 리스크는 checkpoint, late event, state migration이며 배포 전 savepoint 복구 테스트가 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리 지연 | end-to-end lag 1초 이하 | Flink metrics |
| 복구 | checkpoint success 99.9% | JobManager metric |
| 상태 크기 | state growth 예측선 이내 | state backend metrics |

> 요약: Flink 도입 효과는 지연, checkpoint 성공률, state 성장률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. event_time 필드를 표준화하고 watermark delay를 업무 SLA에 맞춰 1분·5분 등으로 설정함
2. RocksDB incremental checkpoint와 checkpoint interval 30초를 적용해 state snapshot 비용을 제한함
3. 배포는 savepoint 생성, 새 job restore, dual run diff 0.1% 이하 검증 후 전환함

**결론 (2줄):**
- 기술사 판단: sub-second 지연과 stateful event time 처리가 필요하면 Flink, 단순 배치성 스트림은 Spark Structured Streaming을 선택함
- 향후 방향: Flink는 real-time feature, CDC, streaming warehouse와 결합해 실시간 데이터 제품의 실행 계층으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Flink를 설명하시오" | event time, watermark, checkpoint 흐름 | micro-batch 대비 특징 |
| 요구사항 명시형 | "Spark와 비교하시오", "설계하시오" | state backend, checkpoint, sink commit | 지연·정확성·운영 지표 선택 |

> 요약: 설명형은 처리 원리, 비교·설계형은 event time과 exactly-once 조건 중심으로 작성함.
