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
- **개요**: 실시간 스트리밍 플랫폼은 이벤트를 수집 → 전송 → 처리 → 저장 → 제공하는 end-to-end **이벤트 기반 아키텍처**(Event-Driven Architecture)다 — Kafka나 Flink 한 가지 제품이 아니라 이 다섯 단계를 갖춘 시스템 전체를 가리킨다.
- **왜 필요한가**: 배치 플랫폼은 "어제까지의 데이터"를 다루므로 하루 단위 리포트에는 맞지만, 사기 탐지·재고 실시간 반영·장애 알림처럼 "지금 이 순간"의 판단이 필요한 업무에는 지연이 너무 크다. 실시간 플랫폼은 이벤트 발생과 처리 결과 반영 사이의 시간(freshness)을 초·분 단위로 줄인다.
- **핵심 직관**: 도시 교통 관제센터가 각 교차로 센서 신호를 실시간으로 모아(수집), 신호등을 즉시 조정하고(처리), 동시에 하루치 통행량 기록도 남기는(저장) 것과 같다 — 즉시 판단과 이후 분석을 한 체계로 같이 한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 이벤트 기반 아키텍처 | 상태 변화를 이벤트로 만들어 시스템 간에 전달·반응하는 설계 방식 — 실시간 스트리밍 플랫폼이 속하는 상위 분류 | 사건이 생길 때마다 알림이 도는 신문 속보 체계 |
| 이벤트 브로커(Event Broker) | 이벤트를 순서대로 오래 보관하며 여러 소비자에게 나눠주는 중계소(Kafka, Pulsar) | 우체국 중앙 집하장 |
| 스트림 프로세서(Stream Processor) | 브로커의 이벤트를 읽어 집계·조인·상태 계산을 수행하는 엔진(Flink, Spark Streaming) | 컨베이어벨트 위 검수·가공 라인 |
| 서빙 스토어(Serving Store) | 처리 결과를 빠르게 조회하도록 저장하는 곳(Redis, Druid, ClickHouse) | 완성품을 진열하는 매대 |
| 스키마 레지스트리(Schema Registry) | 이벤트 형식(필드·타입)을 중앙에서 등록·검증하는 저장소 | 우편물 규격을 정한 규정집 |
| DLQ(Dead Letter Queue) | 처리에 반복 실패한 이벤트를 따로 모아두는 큐 | 반송 우편물 보관함 |
| 컨슈머 랙(Consumer Lag) | 브로커에 쌓인 이벤트 수 − 소비자가 읽은 이벤트 수 (처리가 밀린 정도) | 쌓여가는 미결 우편함 |
| 프레시니스(Freshness) | 이벤트 발생 시각부터 서빙 결과 반영까지 걸린 시간 | 뉴스 속보의 "몇 분 전" 표시 |
| 백프레셔(Backpressure) | 처리 속도가 유입 속도를 못 따라가 상류로 압력이 역전파되는 현상 | 배수구가 막혀 물이 역류하는 것 |

## 깊이 이해

### 왜 "플랫폼"인가 — 구성요소가 5단계로 나뉘는 이유
- 실시간 처리를 Kafka 하나로 착각하기 쉽지만, Kafka는 이 중 "이벤트 브로커" 한 단계일 뿐이다. 실제 플랫폼은 (1) 이벤트 소스, (2) 브로커, (3) 스트림 프로세서, (4) 서빙 스토어, (5) 관측성(observability)까지 5개 계층이 맞물려야 동작한다.
- 예: 사기 탐지 시스템에서 결제 앱(소스) → Kafka 24개 파티션(브로커) → Flink keyed state 집계(프로세서) → Redis 위험 점수 캐시(서빙) → 지연·오류를 보는 대시보드(관측성)까지가 하나의 플랫폼이다. 서빙 스토어가 없으면 계산 결과를 API가 조회할 방법이 없듯, 하나라도 빠지면 "실시간"이 완성되지 않는다.

### freshness를 수치로 정의하기
- freshness = 서빙 결과에 반영된 시각 − 이벤트가 실제 발생한 시각(event_time). 예: 11:00:00에 결제가 발생하고 11:00:03에 위험 점수 캐시가 갱신되면 freshness는 3초다.
- 업무별로 freshness 목표(SLO)를 다르게 잡는다: 사기 차단은 p95 1초 이하, 실시간 추천은 p95 5초 이하, 재고 동기화는 p95 1분 이하, 정산 보정은 p95 5분 이하로 나눈다. 목표가 다르면 파티션 수, 체크포인트 간격, 캐시 갱신 주기 같은 설계가 전부 달라진다.

### 처리량과 랙(lag)의 관계 — 수치 예제
- 초당 유입 이벤트가 10,000건(EPS)이고 스트림 프로세서가 초당 8,000건만 처리할 수 있다면, 매초 2,000건씩 컨슈머 랙이 쌓인다. 1분 뒤에는 랙이 120,000건까지 쌓여 freshness가 12초(120,000÷10,000)까지 벌어진다.
- 이를 막으려면 파티션을 늘려 병렬 처리량을 확보하거나(예: 파티션 12개 → 24개로 늘려 처리량 2배 확보), 오토스케일링으로 프로세서 인스턴스를 늘린다. 목표는 "평상시 처리량이 피크 유입량의 2배 여유를 갖도록" 설계하고 부하 테스트로 검증하는 것이다.

### 스키마 변경과 DLQ — 장애를 국소화하는 법
- producer가 필드 타입을 바꾸면(예: amount를 정수에서 문자열로) 다운스트림 컨슈머가 파싱에 실패한다. 스키마 레지스트리는 새 스키마가 이전 스키마와 호환(backward compatible)되는지 등록 시점에 검증해 이런 장애를 사전에 막는다.
- 그래도 처리 중 실패하는 이벤트(예: 필수 필드 누락)는 즉시 버리지 않고 DLQ로 보내, 전체 스트림을 막지 않으면서 나중에 재처리하거나 원인을 분석한다. 예: DLQ 비율이 0.1%를 넘으면 알림을 울려 원천 시스템의 이벤트 생성 로직을 점검한다.

### 비유와 흔한 오해
- **비유**: 물류 허브가 상품을 받는 즉시 목적지별로 분류해 당일 배송 현황판에 반영하면서도(실시간 서빙), 동시에 월말 정산용 전체 기록도 차곡차곡 쌓는(레이크·DW 적재) 것과 같다. 하나의 이벤트가 실시간 판단과 이후 배치 분석에 동시에 쓰인다.
- **흔한 오해**: "실시간"은 모든 데이터를 지연 없이 처리한다는 뜻이 아니다. 늦게 도착하는 이벤트(late event)를 얼마나 기다릴지, 장애 후 어디서부터 재생(replay)할지, 어떤 데이터까지 즉시 반영이 필요한지를 업무별로 명확히 정의하지 않으면 "실시간"이라는 말만 있고 실제로는 지연·유실이 방치된다.

## 연결 개념
- Kafka/Pulsar — event broker로서 durable log를 담당
- Apache Flink(138) — stream processor로서 window·state 처리를 담당
- Exactly-Once Semantics(139) — 플랫폼 전체의 정합성 보장 수준
- Change Data Capture(141) — 운영 DB 변경을 이벤트로 만들어 플랫폼에 유입시키는 소스

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
