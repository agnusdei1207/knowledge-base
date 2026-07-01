---
title: "실시간 스트리밍 플랫폼 (Real-Time Streaming Platform)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 140
---

# 📖 【암기용】 개념 완전 이해

> 목적: 실시간 스트리밍 플랫폼이 Kafka 하나가 아니라 수집·처리·저장·관측을 포함한 아키텍처임을 이해하게 만든다.

## 한눈에
- **개요**: 이벤트를 수집, 전송, 처리, 저장, 제공하는 end-to-end 실시간 데이터 플랫폼
- **왜 필요한가**: 추천, 이상탐지, 모니터링, 정산 보정은 분·초 단위 데이터 반영과 장애 시 재처리가 필요함.
- **핵심 직관**: 도시 교통 관제처럼 센서 신호를 모으고, 즉시 판단하고, 기록을 남겨 이후 분석까지 하는 체계임.

## 깊이 이해
- **배경·문제의식**: 배치 데이터 플랫폼은 하루 뒤 리포트에는 적합하지만 사기 탐지·재고 반영·장애 알림에는 지연이 큼. 실시간 플랫폼은 event backbone, stream processor, serving store, observability를 통합해 data freshness를 관리함.
- **작동 원리**: source에서 이벤트를 publish하고 Kafka/Pulsar가 durable log로 보존함. Flink/Spark Streaming이 window·state 처리를 수행하고, 결과는 OLAP store, cache, feature store, data lake로 전달됨.
- **비유**: 물류 허브가 상품을 받는 즉시 분류하고, 실시간 배송 현황과 월말 정산 데이터를 동시에 만드는 구조임.
- **구체 예시**: 결제 fraud 탐지 플랫폼은 Kafka 24 partition, Flink keyed state, Redis risk score cache를 사용해 1초 이하로 차단 여부를 계산함.
- **흔한 오해·주의점**: 실시간은 모든 데이터를 즉시 처리한다는 뜻이 아님. 지연 허용치, late event 정책, replay 범위를 업무별로 정의해야 함.

## 연결 개념
- Kafka — event backbone
- Flink/Spark Streaming — stream processing
- Exactly-Once — 정합성 보장 수준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 실시간 스트리밍 플랫폼 문제에서 수집부터 제공까지 end-to-end 설계와 지표 기반 운영을 제시함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 실시간 스트리밍 플랫폼은 이벤트 수집·전송·처리·저장·제공을 연결하는 데이터 처리 아키텍처임.
> 2. **가치**: batch 지연을 줄여 fraud 탐지, 실시간 추천, 모니터링, CDC 동기화를 초·분 단위로 처리함.
> 3. **판단 포인트**: latency, throughput, ordering, delivery guarantee, replay, schema governance를 요구사항별로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 실시간 데이터 아키텍처 이해 확인 | source, broker, processor, serving, observability | Kafka 단품 설명으로 축소 |
| 품질 속성 판단 확인 | latency, throughput, ordering, exactly-once | "실시간"을 수치 없이 표현 |
| 운영 리스크 확인 | lag, backpressure, schema evolution, DLQ | late event와 replay 전략 누락 |

> 요약: 실시간 플랫폼 답안은 구성요소 나열보다 지연·정합성·재처리·관측성 지표를 중심으로 써야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 실시간 스트리밍 플랫폼은 이벤트 기반 처리 체계임.
- 배경: 배치 중심 플랫폼은 의사결정 지연과 장애 탐지 지연을 만든다.
- 필요성: event broker, stream processor, serving store, observability를 결합해 초·분 단위 반영과 장애 복구를 지원함.

---

## Ⅱ. 구조 및 구성요소

```text
Event Source -> Ingestion/CDC -> Event Broker -> Stream Processor
                                      / Schema Registry -> DLQ
Stream Processor -> Serving Store/Data Lake -> API/Dashboard/ML Feature
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event Source | 업무 이벤트·로그·CDC 생성 | event_id, event_time 표준화 |
| Event Broker | durable log와 fan-out 제공 | Kafka, Pulsar, retention |
| Stream Processor | window·state·join 처리 | Flink, Spark Streaming |
| Serving Store | 결과 조회 제공 | Redis, Druid, ClickHouse |
| Observability | lag·오류·품질 관측 | metric, trace, data quality |

> 요약: 실시간 플랫폼은 broker와 processor뿐 아니라 schema, DLQ, serving, observability까지 포함한 end-to-end 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 생성 -> schema 검증 -> broker append -> stream 처리
-> state/window 갱신 -> 결과 저장 -> API/대시보드 제공 -> 지표 관측
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 이벤트 생성·스키마 검증 | schema compatibility 100% |
| 2 | broker append와 복제 | RF 3, min ISR 2 |
| 3 | stream processor 상태 처리 | processing lag, checkpoint |
| 4 | serving store 반영과 관측 | p95 freshness, DLQ rate |

> 요약: 실시간 처리는 이벤트가 생성된 순간부터 serving 결과가 갱신될 때까지의 end-to-end freshness로 평가함.

---

## Ⅳ. 특징

| 구분 | 배치 플랫폼 | 실시간 스트리밍 플랫폼 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 지연 | 시간·일 단위 | 초·분 단위 | p95 freshness 5초~5분 |
| 처리 | 파일 단위 | 이벤트 단위 | throughput events/sec |
| 정합성 | 재계산 중심 | checkpoint, idempotency | duplicate output 0건 |
| 운영 | scheduler 중심 | lag·backpressure 관측 | consumer lag, DLQ rate |

> 요약: 실시간 플랫폼은 지연을 줄이는 대신 ordering, late event, replay, backpressure 운영이 설계 핵심이 됨.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Batch ETL | event-driven streaming | freshness SLA 5분 이하 |
| 비용/성능 | 낮은 상시 비용 | 상시 broker·processor 비용 | fraud·추천 등 지연 손실이 큰 업무 |
| 운영/위험 | 실패 후 재실행 | lag·DLQ·schema 관리 | 24x7 운영·알림 체계 필요 |

> 요약: 실시간 플랫폼은 지연 손실이 비용으로 연결되는 업무에 적용하고, 단순 리포트는 batch로 유지함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| backpressure | processor 처리량 부족 | autoscaling, partition 증설 | lag 증가율, CPU 70% 이하 |
| schema 장애 | producer 변경 | Schema Registry, compatibility check | schema reject rate |
| late event | 네트워크·source 지연 | watermark, allowed lateness, replay | late event ratio |

> 요약: 실시간 플랫폼 리스크는 lag, schema, late event이며 관측성과 DLQ로 장애 범위를 격리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Freshness | p95 5초~5분 | event_time vs serving_time |
| 처리량 | 목표 EPS 2배 부하 통과 | load test, broker metrics |
| 품질 | DLQ rate 0.1% 이하 | DLQ topic, data quality rule |

> 요약: 도입 후 성공 여부는 freshness, 처리량 여유, DLQ 비율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 이벤트 표준은 event_id, event_time, producer, schema_version을 필수 필드로 정의하고 schema compatibility를 CI에서 검증함
2. Kafka RF 3, Flink checkpoint 30초, DLQ topic, replay runbook을 구성해 장애 시 유실·중복을 통제함
3. freshness SLO를 업무별로 5초·1분·5분으로 분류하고 lag·DLQ·checkpoint 실패를 알림 기준으로 설정함

**결론 (2줄):**
- 기술사 판단: 지연 손실이 크고 이벤트 재사용이 필요하면 streaming platform, 정기 통계와 정산 확정은 batch/lakehouse를 선택함
- 향후 방향: real-time feature store, CDC, lakehouse streaming table이 결합되어 운영계와 분석계 경계가 줄어듦

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "실시간 스트리밍 플랫폼을 설명하시오" | source-broker-processor-serving 흐름 | batch 대비 지연·정합성 특징 |
| 요구사항 명시형 | "설계하시오", "운영 방안을 제시하시오" | freshness SLO, replay, DLQ, schema | latency·throughput·exactly-once 선택 기준 |

> 요약: 설명형은 end-to-end 구조, 설계형은 SLO와 운영 통제 지표 중심으로 작성함.
