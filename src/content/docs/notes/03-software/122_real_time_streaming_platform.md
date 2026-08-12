---
sidebar:
  order: 122
  label: "122. 실시간 스트리밍 플랫폼 (Real-Time Streaming Platform)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "실시간 스트리밍 플랫폼 (Real-Time Streaming Platform)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 122
extra:
  question_no: "122"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "실시간 수집•처리•저장 통합 설계 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Real-Time Streaming Platform (실시간 스트리밍 플랫폼)**: 발생 즉시 흘러나오는 연속적인 비동기 이벤트(Events/Logs/Metrics)를 소스로부터 수집(Ingestion), 분산 버퍼링(Messaging Broker), 실시간 연산(Stream Processing), 서빙 저장소(Serving DB)까지 서브밀리초~초 단위 지연으로 통합 처리하는 엔드투엔드 파이프라인 아키텍처.
- **Data Pipeline Decoupling**: 수집(Kafka)과 연산(Flink/Spark)과 저장(Cassandra/Redis)의 물리적 레이어를 완벽히 분리하여 노드 장애 전파를 차단하는 아키텍처 사상.
- **Event-Driven Architecture (EDA)**: 중앙 집중식 요청-응답(REST API)이 아닌, 상태 변경 이벤트 발생(Event Publication)을 구독(Subscribe)하여 즉각 반응하는 시스템 구조.

</details>

- 정의/개념: 이종 시스템에서 연속적으로 유입되는 대규모 이벤트 스트림을 수집, 분산 버퍼링, 실시간 가공, 서빙 레이어 렌더링까지 초저지연(Sub-second)으로 통합 관리하는 빅데이터 아키텍처인 **Real-Time Streaming Platform**
- 배경/필요성: 기존 일괄 배치(Batch)의 몇 시간 지연 극복, 실시간 이상 거래 탐지(FDS), 개인화 실시간 추천, 실시간 관제 모니터링 수용 요구성

#### 한줄 요약

- 우체국이 편지를 일단 쌓아 두고 분류하듯, 브로커가 연속 이벤트를 보존해 처리 속도 차이를 흡수하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Low Latency & High Throughput**: 수십만 QPS 이벤트를 수ms 이내 초저지연 처리.
- **Stateful Processing & End-to-End EOS**: 파이프라인 전체에 걸쳐 단 1번 처리(Exactly-Once) 보장.

</details>

- **End-to-End Real-Time Pipeline (Ingestion $\rightarrow$ Broker $\rightarrow$ Engine $\rightarrow$ Serving)**
- **Sub-second Low Latency & High Ingestion Throughput**
- **Stateful Stream Processing & Exactly-Once Consistency**

#### 한줄 요약

- 브로커는 이벤트를 보존하고 처리기는 상태를 계산하므로 두 계층의 위치•상태•출력 복구 경계를 맞춰야 한다.

## Ⅲ. 구조 및 구성요소 (실시간 스트리밍 파이프라인 4대 토폴로지)

<details><summary>핵심 용어</summary>

- **Ingestion, Message Broker, Stream Engine, Serving Store**: 실시간 스트리밍 플랫폼을 지탱하는 4대 레이어.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Real-Time Streaming Platform Pipeline                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Ingestion Layer   ──► [Kafka Connect, Debezium CDC, Flume]          │
│ 2. Broker Layer      ──► [Apache Kafka / Redpanda (Log Ingestion)]     │
│ 3. Processing Layer  ──► [Apache Flink / Spark Streaming (State Engine)]│
│ 4. Serving Layer     ──► [Redis / Cassandra / ElasticSearch / Pinot]  │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터 수집 커넥터부터 메시지 브로커, 스트림 연산 엔진, 최종 서비스 디스플레이 DB까지 일체형으로 연결되는 파이프라인.

| 아키텍처 레이어 | 담당 주요 역할 | 대표 표준 기술 스택 |
|:---|:---|:---|
| **1. Ingestion Layer** | **앱 로그 및 DB 변경분(CDC) 실시간 추출 수집** | **Kafka Connect, Debezium CDC, Vector** |
| **2. Message Broker Layer** | **이벤트 100% 보존, 버퍼링, Pub/Sub 분산 라우팅** | **Apache Kafka, Apache Pulsar, Redpanda** |
| **3. Stream Processing** | **이벤트 시간 기반 Windowing, Stateful 연산** | **Apache Flink, Spark Structured Streaming**|
| **4. Serving Store Layer** | **최종 가공된 실시간 통계/알림 1ms 서빙 렌더링**| **Redis, Cassandra, Apache Pinot, Druid** |

#### 한줄 요약

- 작성자, 사건 일지, 계산자, 복구 사진, 서비스 장부로 구성된다.

## Ⅳ. 흐름도 (End-to-End 실시간 파이프라인 데이터 흐름)

<details><summary>핵심 용어</summary>

- **Stream-Table Duality (KTable)**: 이벤트 스트림(Stream)은 변화의 기록이고, 테이블(Table)은 특정 시점의 현재 상태라는 스트림-테이블 이중성 이론.

</details>

```text
[User Action Event] ──► [CDC / Kafka Ingest] ──► [Kafka Topic Partition]
                                                        │
                                                        ▼
  [Client Real-Time Dashboard] ◄── [Redis Serving] ◄── [Flink Engine (State Window)]
```

### 동작 원리

1. **Ingest & Buffer**: 유저 모바일 앱 이벤트가 Debezium CDC를 거쳐 Kafka Topic에 1ms 만에 저장.
2. **Stream Calculate**: Apache Flink가 Kafka Partition에서 메시지를 읽어 5분 Sliding Window 상태 연산.
3. **Serving Render**: Flink 가공 결과가 Redis/Pinot 뷰어 DB에 인서트되어 유저 실시간 대시보드 표출.

#### 한줄 요약

- 일지 위치와 계산 상태, 외부 장부 결과를 같은 경계로 맞춰 다시 시작해도 틀어지지 않게 한다.

## Ⅴ. 종류 및 비교 (배치 파이프라인 대 실시간 스트리밍 파이프라인)

<details><summary>핵심 용어</summary>

- **Batch vs Real-Time**: 배치는 T+1일 일괄 처리, 실시간 스트리밍은 발생 1초 이내 즉각 연산 및 알림.

</details>

| 비교 항목 | Batch Data Pipeline (배치 파이프라인) | Real-Time Streaming Pipeline (실시간 파이프라인) |
|:---|:---|:---|
| **데이터 연산 시점**| **주기적 일괄 처리 (매일 자정 T+1일)** | **이벤트 발생 즉시 연속 처리 (Sub-second)** |
| **핵심 메시지 브로커**| HDFS, AWS S3, File Storage | **Apache Kafka, Apache Pulsar** |
| **핵심 연산 프레임워크**| Hadoop MapReduce, Spark Batch | **Apache Flink, Spark Structured Streaming** |
| **주요 사용 도메인** | 정기 결제 정산, 월간 일괄 보고서 | **실시간 FDS 결제차단, 랭킹 차트, 실시간 추천** |

#### 한줄 요약

- Kafka는 사건을 남기고 Flink•Spark는 사건을 계산하며 Sink는 서비스할 결과를 보관한다.

## Ⅵ. 실무 고려사항 및 대책 (실시간 파이프라인 3대 난제 대책)

<details><summary>핵심 용어</summary>

- **Data Spikes (트래픽 폭증)**: 이벤트 폭증 시 브로커 파티션 및 스트림 연산자 튜닝으로 역압력(Backpressure) 방지.

</details>

| 3대 스트리밍 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Backpressure 현상** | Serving DB 과부하로 Stream 연산자 멈춤 | **Async I/O 적용 및 Serving DB 인메모리/캐시 확장**|
| **2. Out-of-Order Events** | 네트워크 지연으로 이벤트 순서 뒤틀림 | **Watermark 및 Allowed Lateness 버퍼 레이어 설정**|
| **3. End-to-End EOS 파행** | 파이프라인 일부 노드 다운 시 중복 렌더링| **Kafka (acks=all) + Flink 2PC + Redis UPSERT 결합**|

> 사례: **카카오뱅크 실시간 FDS & 당근마켓 실시간 피드 추천 파이프라인 아키텍처**

#### 한줄 요약

- 같은 장치 사건은 순서대로 처리하되 한 장치가 전체 처리량을 독점하지 않는지 확인한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **스트리밍 파이프라인 수립 기준(Streaming Architecture Standards)**: Ingestion QPS, Kafka-Flink-Redis 3대 통합성, EOS 및 Watermark 설계에 의거한 체계.

</details>

- **스트리밍 파이프라인 수립 기준**에 따라 차세대 실시간 시스템 구축 시 **Kafka + Flink + Redis 기반 통합 플랫폼** 필수 수용

#### 한줄 요약

- 사건 위치•계산 상태•최종 결과가 같은 시점으로 복구되어야 믿을 수 있다.
