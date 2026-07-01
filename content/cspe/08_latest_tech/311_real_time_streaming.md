---
title: "Real-time Streaming 실시간 스트리밍 (Real-time Streaming)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 311
---

# 📖 【암기용】 개념 완전 이해

> 목적: 실시간 스트리밍을 데이터가 쌓인 뒤 한꺼번에 처리하는 배치와 달리 이벤트가 발생하는 즉시 지속적으로 처리하는 데이터 아키텍처로 이해하게 만든다.

## 한눈에
- **개요**: 이벤트를 지속적으로 수집·처리·전달하는 데이터 처리 방식
- **왜 필요한가**: 결제 이상탐지, IoT 모니터링, 실시간 추천처럼 분 단위 지연도 업무 손실로 이어지는 서비스가 늘었다.
- **핵심 직관**: 하루 장부를 마감 후 계산하는 대신 계산대에서 결제될 때마다 재고와 매출을 바로 반영하는 방식임.

## 깊이 이해
- **배경·문제의식**: 배치 처리는 대량 데이터를 일정 주기로 계산하지만, 이벤트 발생과 의사결정 사이에 지연이 생긴다.
- **작동 원리**: Producer가 event를 broker에 기록하고, stream processor가 window, state, watermark, checkpoint를 사용해 연속 계산을 수행한 뒤 sink로 전달한다.
- **비유**: 강물의 수위를 주기적으로 사진 찍는 방식이 배치라면, 센서가 초 단위로 수위를 보내 위험 기준을 넘을 때 즉시 알림을 보내는 방식이 streaming이다.
- **구체 예시**: 카드 결제 이벤트를 Kafka topic에 쓰고 Flink가 5분 sliding window로 사용자별 거래 빈도를 계산해 이상 거래를 탐지한다.
- **흔한 오해·주의점**: 실시간은 지연 0초가 아니다. 업무 SLA에 맞춘 end-to-end latency, ordering, late event 처리 기준을 명시해야 한다.

## 연결 개념
- Apache Kafka — 이벤트 저장과 전달 플랫폼
- Apache Flink — 상태 기반 스트림 처리 엔진
- Exactly-Once Semantics — 중복·손실 통제 보장 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 실시간 스트리밍은 broker와 processor만 쓰는 것이 아니라 지연, 순서, 상태, 장애복구, backpressure 기준을 함께 설계해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Real-time Streaming은 이벤트를 저장 후 일괄 처리하지 않고 발생 흐름에 따라 연속 처리하는 아키텍처임.
> 2. **가치**: 이상탐지, 추천, 모니터링, CDC 동기화에서 이벤트 발생과 조치 사이의 지연을 업무 SLA 안으로 줄임.
> 3. **판단 포인트**: event time, window, state, watermark, checkpoint, backpressure, delivery semantics가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 배치와 스트리밍 차이 확인 | bounded/unbounded data, latency, state | 단순 실시간 조회로 설명 |
| 아키텍처 설계 역량 확인 | producer, broker, processor, sink | Kafka만 쓰면 해결로 단정 |
| 운영 리스크 판단 확인 | late event, backpressure, duplicate | 지연 0초 표현 사용 |

> 요약: 이 문제는 스트리밍의 처리 모델과 운영 보장을 함께 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 이벤트 연속 처리 구조
- 배경: 배치 주기 기반 처리로는 이상탐지, 재고 동기화, 실시간 지표의 업무 지연을 줄이기 어려움.
- 필요성: 이벤트 발생 후 수초~수분 내 판단이 필요한 업무는 streaming pipeline과 상태 관리가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Event Source -> Producer -> Broker / Topic -> Stream Processor
        +-> State Store / Checkpoint
        +-> Sink / Alert / Dashboard
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event Source | 업무 이벤트 생성 | DB log, app event, sensor |
| Broker | 이벤트 저장·전달·재처리 지원 | Kafka, Pulsar |
| Stream Processor | window, join, aggregation 처리 | Flink, Kafka Streams |
| Sink | 결과 저장·알림·서빙 | DB, lakehouse, API |

> 요약: 스트리밍 구조는 이벤트 저장 계층과 상태 기반 처리 계층을 분리해 재처리와 장애복구를 지원한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 발생 -> topic 기록 -> consumer offset 진행
-> window / state 처리 -> checkpoint 저장 -> sink commit -> 지표 관측
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | producer가 이벤트 key와 timestamp를 포함해 발행 | schema validation |
| 2 | broker가 partition에 순서대로 저장 | partition ordering |
| 3 | processor가 event time window와 state를 갱신 | watermark lag |
| 4 | checkpoint와 sink commit으로 복구 지점 확보 | recovery success |

> 요약: 스트리밍은 이벤트 시간과 상태를 관리하고 checkpoint로 장애 이후 처리 위치를 복원한다.

---

## Ⅳ. 특징

| 구분 | Batch Processing | Real-time Streaming | 판단 기준 |
|:---|:---|:---|:---|
| 데이터 범위 | bounded dataset | unbounded event stream | 업무 지연 허용치 |
| 처리 단위 | job run | continuous operator | 운영 방식 |
| 시간 기준 | 처리 시각 중심 | event time+watermark | late event 존재 |
| 장애복구 | job 재실행 | offset+checkpoint 복구 | 상태 크기 |

> 요약: 스트리밍은 지연을 줄이는 대신 상태·순서·late event 처리 복잡도가 증가한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 업무 요구 | 일 단위 리포트 | 초~분 단위 대응 | SLA latency |
| 처리 모델 | stateless ETL | stateful window processing | 집계·join 필요 |
| 저장 전략 | DW 적재 후 조회 | broker+sink 이중 관리 | 재처리 요구 |

> 요약: 업무 SLA가 초~분 단위이고 이벤트 상태 계산이 필요할 때 스트리밍을 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지연 증가 | consumer lag, backpressure | partition 조정, operator scale-out | end-to-end latency |
| 중복 처리 | 재시도·sink commit 실패 | idempotent sink, transaction | duplicate rate |
| late event 손실 | event time 지연 | watermark, allowed lateness | late event count |

> 요약: 스트리밍 운영 리스크는 지연, 중복, late event이며 offset·checkpoint·watermark로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | 업무 SLA 내 p95/p99 latency | tracing, broker lag |
| 처리량 | peak event rate 처리 | load test |
| 복구 | 장애 후 checkpoint 복원 성공 | failover drill |

> 요약: 스트리밍 성과는 평균 지연보다 p95/p99 지연, peak 처리량, 복구 검증으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 이벤트 schema, key, timestamp, partition 전략을 표준화하고 schema registry로 호환성을 검증함.
2. Flink 또는 Kafka Streams에서 window, state, checkpoint, watermark 정책을 업무 SLA에 맞게 정의함.
3. consumer lag, backpressure, checkpoint duration, sink error를 dashboard와 alert로 운영함.

**결론 (2줄):**
- 기술사 판단: 실시간성이 업무 손실과 직접 연결될 때 streaming을 적용하고, 단순 일괄 집계는 batch가 운영 비용 측면에서 적합함.
- 향후 방향: 스트리밍은 CDC, lakehouse, feature store, 실시간 AI inference와 결합해 event-driven data platform으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Real-time Streaming을 설명하시오" | event time·window·checkpoint 흐름 | batch 대비 차이 |
| 요구사항 명시형 | "실시간 데이터 처리 설계 방안을 제시하시오" | broker·processor·sink 설계 | 지연·중복·late event 대응 |

> 요약: 설명형은 처리 모델을, 설계형은 SLA와 장애복구 조건을 중심으로 작성한다.
