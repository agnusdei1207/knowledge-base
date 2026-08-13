---
sidebar:
  order: 123
  label: "123. 변경 데이터 캡처 CDC (Change Data Capture)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "변경 데이터 캡처 CDC (Change Data Capture)"
date: "2026-08-13T22:59:00+09:00"
tags:
  - "notes-software"
weight: 123
extra:
  question_no: "123"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "CDC는 변경 이벤트•동기화 설계에 중요"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **CDC (Change Data Capture / 변경 데이터 캡처)**: 소스 데이터베이스의 CUD(Create, Update, Delete) 데이터 변경 이벤트를 실시간 감지하여, 타깃 시스템(Search Engine, Data Lake, Cache)으로 부하 없이 100% 동기화 전파하는 파이프라인 기술.
- **Log-based CDC**: 데이터베이스 내부 트랜잭션 로그(MySQL Binlog, PostgreSQL WAL)를 직접 꼬리 물어 파싱함으로써 소스 DB CPU 부하를 0%에 가깝게 최소화하는 대표 CDC 메커니즘.
- **Debezium**: Apache Kafka Connect 기반의 오픈소스 대표 Log-based CDC 커넥터 프레임워크.

</details>

- 정의/개념: DB 변경 로그를 이벤트로 전파하는 **CDC(Change Data Capture)**
- 배경/필요성: 주기 조회는 **삭제 누락•DB 부하•동기화 지연** 유발

#### 한줄 요약

- 원본 장부를 매번 복사하지 않고 바뀐 부분만 찾아 다른 시스템에 전달하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Zero DB Performance Overhead**: 쿼리가 아닌 이진 파일(Binlog)을 직접 읽으므로 DB CPU 부하 최소화.
- **Delete Capture Support**: SQL 폴링과 달리 `DELETE` 구문에 의한 삭제 이벤트(Tombstone Record)까지 100% 포착.

</details>

- **낮은 조회 부하**: 트랜잭션 로그 기반 변경 추출
- **삭제 이벤트 추적**: 제품•설정이 제공하는 삭제 기록 캡처
- **Schema History Tracking (테이블 DDL 변경 이력 실시간 추적)**

#### 한줄 요약

- CDC는 첫 전체 복사와 이후 로그 사이의 빈 구간을 없애고 마지막 확정 위치부터 안전하게 다시 읽어야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Initial Snapshot & Binlog Streaming**: 최초 가동 시 전체 테이블의 Initial Snapshot을 뜨고, 이후부터 Binlog를 실시간 스트리밍으로 전환하는 2단계 절차.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Log-based CDC Architecture                      │
├────────────────────────────────────────────────────────────────────────┤
│ [Source DB (MySQL/PG)] ──► [Binlog / WAL File]                         │
│                                  │ (Log Parsing)                       │
│                                  ▼                                     │
│                     [Debezium CDC Connector]                           │
│                                  │ (Kafka Topic Publish)               │
│                                  ▼                                     │
│                     [Kafka Cluster (Event Stream)]                     │
│                                  │                                     │
│        ┌─────────────────────────┼─────────────────────────┐           │
│        ▼                         ▼                         ▼           │
│  [ElasticSearch]           [Redis Cache]           [Snowflake DW]      │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 소스 DB의 Binlog를 Debezium 커넥터가 읽어 Kafka로 전파하고, ElasticSearch/Redis/DW 등 타깃 시스템으로 실시간 무부하 동기화하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| **Transaction Log** | 커밋 순서와 행 변경 내용 보관 |
| **CDC Connector** | 로그 파싱•스키마 해석•이벤트 변환 |
| **Offset Store** | 마지막 안전 처리 로그 위치 저장 |
| **Event Broker** | 변경 이벤트 순서 보존•다중 전파 |
| **Sink Consumer** | 키 기반 UPSERT•DELETE 멱등 반영 |

#### 한줄 요약

- 원본 장부, 일지 판독기, 책갈피, 전달 일지, 대상 반영기로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Log-based vs Trigger-based vs Query-based**: Log-based는 DB 로그 파싱(부하 0%), Trigger-based는 DB 트리거 생성(쓰기 부하 발생), Query-based는 `WHERE updated_at` SQL 폴링(삭제 감지 불가).

</details>

| CDC 구현 방식 | 메커니즘 및 동작 원리 | 장점 및 단점 비교 |
|:---|:---|:---|
| **Log-based CDC** | **DB 이진 트랜잭션 로그 파싱** | 낮은 조회 부하•로그 권한 필요 |
| **Trigger-based CDC** | **테이블마다 CUD DB Trigger 작성** | 모든 DB 적용 가능, **소스 DB 쓰기 Latency 증가** |
| **Query-based CDC** | **`WHERE updated_at > ?` 쿼리 폴링** | 구현 단순함, **`DELETE` 감지 불가, DB CPU 병목** |

#### 한줄 요약

- 변경 일지를 읽는 방식이 가장 자연스럽지만 권한이 없으면 표식이나 주기 조회를 사용한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Before & After Field**: Debezium CDC 이벤트 내부에 변경 전 상태(`before`)와 변경 후 상태(`after`)가 함께 담기는 JSON 페이로드 구조.

</details>

```text
{
  "before": { "id": 101, "name": "홍길동", "score": 80 },
  "after":  { "id": 101, "name": "홍길동", "score": 95 },
  "op": "u",   // 'c': Create, 'u': Update, 'd': Delete
  "ts_ms": 1770854400000
}
```

#### 한줄 요약

- 첫 전체 복사의 끝과 변경 일지의 시작을 맞추고 마지막 발행 위치를 책갈피로 남긴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Schema Evolution (DDL 변경)**: 소스 DB에 `ALTER TABLE`로 컬럼이 변경될 때 CDC 커넥터가 이를 실시간 감지하여 타깃 DB 스키마도 자동 갱신 조치.

</details>

| 3대 CDC 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Binlog Expiration** | 대용량 트래픽 시 Binlog 파일이 일찍 삭제됨| **Binlog 보존 기간(Retention) 최소 3일 이상 연장** |
| **2. DDL Schema Change** | 소스 DB 컬럼 추가/삭제 시 CDC 파행 | **Debezium Schema Registry 연동 및 DDL 이력 자동 추적**|
| **3. Initial Snapshot Lag**| 수억 건 초기 스냅샷 도중 Binlog 오프셋 상실 | **Consistent Snapshot Mode (Lockless Snapshotting) 적용**|

> 사례: **배달의민족 / 쿠팡 MySQL $\rightarrow$ Debezium CDC $\rightarrow$ Kafka $\rightarrow$ ElasticSearch 검색 엔진 동기화**

#### 한줄 요약

- 같은 원본 키와 최신 변경 번호로 검색 문서를 고치고 삭제까지 전달해야 오래된 결과가 남지 않는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CDC 아키텍처 수립 기준(CDC Architecture Standards)**: Log-based Binlog 파싱, Debezium Kafka Connect 및 ElasticSearch/Redis 실시간 동기화성에 의거한 체계.

</details>

- 로그 권한•삭제 추적이 가능하면 **Log-based**, 아니면 Trigger•Query 선택

#### 한줄 요약

- 첫 복사와 변경 일지의 경계, 마지막 책갈피, 삭제와 구조 변경까지 맞아야 한다.
