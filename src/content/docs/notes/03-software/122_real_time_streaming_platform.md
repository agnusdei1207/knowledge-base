---
sidebar:
  order: 122
  label: "122. 실시간 스트리밍 플랫폼"
  badge:
    text: "미출 · 50%"
    variant: note
title: "실시간 스트리밍 플랫폼 (Real-Time Streaming Platform)"
date: "2026-08-31T10:48:00+09:00"
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

<details><summary>용어 설명</summary>

- **실시간 스트리밍 플랫폼**: 이벤트 발생 즉시 수집, 메시지 브로커 버퍼링, 분산 연산, 서빙 저장소까지 밀리초 단위 초저지연으로 연결하는 데이터 아키텍처.
- **4대 파이프라인 레이어**: Ingestion(수집), Broker(버퍼링), Processing(연산), Serving(조회).

</details>

- 정의/개념: 발생 즉시 흘러나오는 비동기 이벤트를 **수집(Ingestion), 분산 버퍼링(Broker), 실시간 연산(Processing), 서빙(Serving)까지 초저지연으로 통합 처리하는 파이프라인**
- 배경/필요성: 전통적 배치 파이프라인(T+1일 주기)의 **데이터 반영 지연으로 인한 실시간 이상거래 탐지(FDS) 및 동적 의사결정 대응 불가 한계**

#### 한줄 요약
- 계층을 나눈 목적은 속도 자체가 아니라 각 구간이 서로 다른 속도로 확장될 수 있게 하는 데 있으므로, 파이프라인의 종단 지연은 가장 느린 한 계층이 전부 결정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Pipeline Decoupling**: 수집기, 메시지 큐, 연산 엔진, 서빙 DB의 책임을 분리하여 노드 장애 전파를 차단하는 구조.
- **End-to-End Low Latency**: 이벤트 발생부터 화면 조회까지 전체 소요 시간을 1초 미만(Sub-second)으로 단축.

</details>

- 이벤트 발생부터 화면 반영까지 **1초 미만의 엔드투엔드 초저지연(Sub-second Latency)**
- 각 계층 간의 장애 전파를 차단하는 **느슨한 결합(Decoupled Pipeline)**
- 수십만 QPS 트래픽을 유실 없이 수용하는 **수평 확장(Scale-Out) 기반 고처리량**

#### 한줄 요약
- 초저지연, 계층 분리, 수평 확장을 통해 대규모 이벤트를 실시간으로 처리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **4대 핵심 컴포넌트**: Debezium/Kafka Connect(수집), Apache Kafka(브로커), Apache Flink(스트림 연산), Redis/Elasticsearch(서빙).

</details>

```text
[실시간 스트리밍 플랫폼 구성]
|-- 수집 계층
|-- 이벤트 브로커
|-- 스트림 처리기
`-- 서빙 저장소
```

선의 의미: 계층 및 수집된 원천 이벤트가 브로커 버퍼와 연산 엔진을 거쳐 서빙 DB로 파이프라이닝되는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 수집 계층 (Ingestion) | RDB 트랜잭션 로그 및 앱 로그를 **실시간 이벤트 포맷으로 추출/발행** | Debezium, Kafka Connect |
| 이벤트 브로커 (Broker) | 대량 이벤트를 디스크에 순차 보존하고 **생산자와 소비자의 속도 차이 버퍼링** | Kafka, Pulsar |
| 스트림 처리기 (Engine) | 이벤트 시간 기준 윈도우 집계 및 **키별 상태(Keyed State) 실시간 계산** | Flink, Spark Streaming |
| 서빙 저장소 (Serving) | 가공된 집계 결과를 색인하여 **최종 사용자/API에 10ms 이내 초고속 서빙** | Redis, Elasticsearch |

#### 한줄 요약
- 브로커가 생산 속도와 소비 속도를 떼어 놓기에 하류가 느려져도 상류가 멈추지 않지만, 그 완충은 보존 용량만큼만 유효하고 그 뒤에는 유실이나 역압으로 되돌아온다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **실시간 스트림 처리 5단계**: CDC 이벤트 캡처 $\to$ 카프카 토픽 버퍼링 $\to$ Flink 윈도우 연산 $\to$ 서빙 DB 멱등 쓰기 $\to$ 대시보드 푸시.

</details>

```text
서비스 DB 트랜잭션 및 사용자 액션 발생
        │
   [CDC 수집] Debezium이 DB Binlog를 실시간 감지하여 JSON 이벤트로 변환
        │
   [브로커 버퍼링] Apache Kafka의 특정 파티션에 Append-Only 순차 기록 및 ISR 복제
        │
   [스트림 연산] Apache Flink가 Event Time Watermark 기준으로 5분 슬라이딩 윈도우 집계
        │
   [서빙 저장소 멱등 쓰기] 가공된 집계 결과를 Redis / Elasticsearch에 UPSERT 반영
        │
   웹소켓을 통해 프론트엔드 관제 대시보드 및 실시간 FDS 차단 엔진에 즉시 푸시
```

#### 한줄 요약
- 계층마다 지연이 조금씩 더해지므로 종단 지연은 한 구간을 빠르게 해서가 아니라 계층 수와 각 구간의 버퍼링 정책을 함께 줄여야 낮아진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **배치 vs 실시간 스트리밍**: 주기적 일괄 연산(배치)과 이벤트 발생 즉시 연속 연산(실시간).

</details>

| 비교 항목 | 배치 데이터 파이프라인 (Batch) | 실시간 스트리밍 플랫폼 (Streaming) |
|:---|:---|:---|
| 데이터 처리 주기 | **주기적 일괄 실행 (매일 자정, T+1일)** | **이벤트 발생 즉시 연속 실행 (밀리초 단위)** |
| 핵심 저장/버퍼 | HDFS, S3 객체 스토리지 | **Apache Kafka, Apache Pulsar** |
| 핵심 연산 엔진 | Hadoop MapReduce, Spark Batch | **Apache Flink, Spark Structured Streaming** |
| 최적 적용 도메인 | **월간 결제 정산, 일일 재무 보고서** | **이상금융거래 탐지(FDS), 실시간 피드 추천**|

#### 한줄 요약
- 사후 분석은 배치 파이프라인, 즉시 대응이 필요한 서비스는 실시간 스트리밍 플랫폼을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Backpressure**: 서빙 DB의 쓰기 지연으로 인해 스트림 엔진의 버퍼가 차올라 전체 파이프라인이 멈추는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 서빙 DB 병목으로 인한 파이프라인 **Backpressure** 차단 | **Async I/O 적용 및 서빙 DB 전면에 Redis 캐시 버퍼 배치** | 파이프라인 정체 해소 |
| 네트워크 지연으로 인한 지연 이벤트(Late Data) 순서 왜곡 | **Watermark 튜닝 및 `allowedLateness` 지연 허용 버퍼 설정** | 지연 데이터 유실 없는 정확한 집계 |
| 파이프라인 장애 복구 시 데이터 중복 표출 | **Kafka `acks=all` + Flink 2PC + 서빙 DB UPSERT 삼위일체 결합**| End-to-End Exactly-Once 달성 |
| 트래픽 급증 시 브로커 파티션 병목 | **파티션 키 Salt 해싱 및 파티션 수 동적 확장** | 브로커 부하 균등 분산 |

#### 한줄 요약
- Async I/O, 워터마크 튜닝, End-to-End EOS 결합, 파티션 분산으로 파이프라인을 최적화한다.

## Ⅶ. 결론

- 현대 디지털 비즈니스의 실시간 의사결정 및 이벤트 주도 엔터프라이즈(EDE)의 **가장 핵심적인 데이터 파이프라인 아키텍처**로 확립되었으며, 실무 아키텍처 구현 시에는 **다운스트림 쓰기 병목을 해소하는 Async I/O 및 인메모리 서빙 캐시 배치, 네트워크 지연에 대응하는 워터마크(Watermark) 튜닝, 엔드투엔드 데이터 무결성을 보장하는 Kafka-Flink-DB 간 Exactly-Once(EOS) 결합**을 통해 서비스 복원력과 초저지연 성능을 동시 보증

#### 한줄 요약
- 실시간 스트리밍 플랫폼은 수집, 버퍼링, 연산, 서빙의 4대 계층을 유기적으로 결합하여 이벤트 발생 즉시 비즈니스 가치를 창출하는 현대 데이터 인프라의 핵심이다.
