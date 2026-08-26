---
sidebar:
  order: 123
  label: "123. 변경 데이터 캡처 CDC"
  badge:
    text: "미출 · 50%"
    variant: note
title: "변경 데이터 캡처 CDC (Change Data Capture)"
date: "2026-08-26T09:54:00+09:00"
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

<details><summary>용어 설명</summary>

- **CDC(Change Data Capture)**: 데이터베이스의 삽입·수정·삭제(CUD) 변경을 감지하여 타깃 시스템으로 실시간 동기화하는 기술.
- **Log-based CDC**: 데이터베이스의 트랜잭션 로그(Binlog, WAL)를 직접 파싱하여 소스 DB 부하를 최소화하는 표준 방식.

</details>

- 정의/개념: 원천 데이터베이스의 CUD 변경 이벤트를 감지하여 **타깃 시스템(검색엔진, 캐시, 데이터 레이크)으로 부하 없이 실시간 동기화 전파하는 기술**
- 배경/필요성: 주기적 SQL 폴링 방식의 **소스 DB CPU 부하 폭증, `DELETE` 삭제 감지 불가 및 데이터 동기화 지연 해결 불가**

#### 한줄 요약
- 트랜잭션 로그 파싱을 통해 소스 DB 부하 없이 CUD 이벤트를 타깃 저장소로 실시간 동기화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Debezium**: MySQL Binlog, PostgreSQL WAL 등을 읽어 Kafka 토픽으로 JSON/Avro 이벤트를 발행하는 오픈소스 CDC 플랫폼.
- **Tombstone Event**: 원본 레코드 삭제(`DELETE`) 시 타깃 캐시/검색엔진에서도 즉시 삭제되도록 발행하는 `null` 페이로드 메시지.

</details>

- 쿼리 실행 없이 이진 로그를 읽어 소스 DB 부하를 0화하는 **로그 기반 저부하(Zero-Overhead) 추출**
- SQL 폴링에서 불가능한 **삭제 이벤트(`DELETE`) 완벽 포착 및 전파**
- `ALTER TABLE` 등 소스 DDL 변경을 추적하는 **스키마 진화(Schema Evolution) 대응**

#### 한줄 요약
- 저부하 로그 추출, 삭제 이벤트 포착, 스키마 변경 추적을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CDC 4대 컴포넌트**: Transaction Log(Binlog/WAL), Debezium Connector(파서), Kafka Topic(이벤트 허브), Sink Consumer(타깃 반영기).

</details>

```text
[Log-based CDC 데이터 동기화 아키텍처]
|-- Source DB (MySQL / PostgreSQL: 트랜잭션 로그 Binlog / WAL 기록)
`-- Debezium CDC Connector (Kafka Connect 프레임워크 기반 Log 파싱)
    |-- Schema History Topic (DDL 변경 이력 메타데이터 보관)
    `-- Kafka Cluster (Event Topic: CUD 변경 JSON 이벤트 스트림)
        |-- Elasticsearch (검색 인덱스 실시간 동기화)
        |-- Redis Cache (캐시 데이터 자동 무효화 / 갱신)
        `-- Snowflake / Iceberg (데이터 레이크하우스 실시간 적재)
```

선의 의미: 계층 및 Source DB의 로그가 Debezium을 통해 Kafka로 전파되고 타깃 시스템들로 다중 동기화되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 트랜잭션 로그 (Log) | 커밋된 순서대로 데이터 변경(CUD) 바이너리 기록을 **디스크에 영구 보관** | Binlog, WAL, Redo Log |
| CDC 커넥터 (Debezium) | 트랜잭션 로그를 논블로킹 파싱하여 **표준 이벤트 포맷으로 변환 후 Kafka 발행** | Initial Snapshot + Streaming |
| 오프셋 저장소 (Offset) | 마지막으로 안전하게 파싱 완료한 **로그 파일명 및 포지션 바이트 위치 저장** | 재시작 시 중복/유실 방지 |
| 이벤트 브로커 (Kafka) | 변경 이벤트를 토픽 파티션에 저장하고 **다수의 타깃 시스템에 병렬 전파** | 멱등성 및 순서 보장 |
| 타깃 컨슈머 (Sink) | 변경 이벤트를 수신하여 **검색엔진, 캐시, DW에 UPSERT/DELETE 멱등 반영** | 최종 일관성 수렴 |

#### 한줄 요약
- 트랜잭션 로그, CDC 커넥터, 오프셋 저장소, 카프카 브로커, 타깃 컨슈머가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Initial Snapshot $\to$ Streaming 전환**: 최초 가동 시 기존 테이블 데이터를 읽어 초기 스냅샷을 뜬 후, 스냅샷 시점의 Binlog 오프셋부터 실시간 스트리밍으로 전환하는 기법.

</details>

```text
소스 DB에서 비즈니스 트랜잭션 커밋 (`UPDATE users SET score=95 WHERE id=101`)
        │
   [트랜잭션 로그 기록] DB 엔진이 Binlog 파일에 변경 전(before)/변경 후(after) 바이트 기록
        │
   [논블로킹 로그 파싱] Debezium이 Binlog 꼬리를 물고 읽어 JSON 변경 이벤트로 직렬화
        │
   [Kafka 토픽 발행] PK(id=101)를 메시지 키로 지정하여 Kafka `db.users` 토픽으로 전송
        │
   [오프셋 위치 커밋] 처리 완료된 Binlog 파일 위치(Pos=120485)를 커넥터 메타데이터에 기록
        │
   Elasticsearch 및 Redis 컨슈머가 이벤트를 읽어 캐시 및 인덱스를 즉시 갱신
```

#### 한줄 요약
- 로그 기록 → 논블로킹 파싱 → 카프카 발행 → 오프셋 커밋 → 타깃 저장소 반영 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CDC 3대 구현 방식**: Log-based(트랜잭션 로그 파싱), Trigger-based(DB 트리거 작성), Query-based(타임스탬프 폴링).

</details>

| 비교 항목 | Log-based CDC (로그 기반) | Trigger-based CDC (트리거 기반) | Query-based CDC (쿼리 폴링) |
|:---|:---|:---|:---|
| 데이터 추출 원리 | **DB 이진 트랜잭션 로그 파싱** | **테이블별 CUD DB 트리거 생성** | **`WHERE updated_at > ?` 주기적 SQL 실행**|
| 소스 DB 부하 | **거의 없음 (디스크 읽기 최소화)**| **높음 (소스 DB 쓰기 지연 증가)**| **매우 높음 (주기적 Full Table Scan)** |
| `DELETE` 감지 | **완벽 지원 (Tombstone 이벤트)** | **지원 (트리거 내 삭제 감지)** | **원천 불가 (삭제된 행 조회 불가)** |
| 구현 복잡도 | DB 로그 권한 및 커넥터 구성 필요 | 테이블마다 트리거 관리 부담 | 매우 단순 (표준 SQL) |

#### 한줄 요약
- 성능과 삭제 감지가 필수적인 환경에서는 Log-based CDC가 표준 선택지다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Binlog Retention**: 대용량 트래픽 발생 시 Binlog 디스크가 차서 파일이 일찍 삭제되는 현상을 방지하기 위한 보존 기간 설정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트래픽 급증 시 Binlog 조기 삭제로 CDC 동기화 단절 | **Binlog 보존 기간(Retention)을 최소 3~7일 이상 확보** | 로그 유실로 인한 전면 재동기화 방지 |
| 소스 DB `ALTER TABLE` DDL 실행 시 CDC 파싱 에러 | **Debezium Schema Registry 연동 및 Avro/Protobuf 스키마 자동 진화**| 무중단 스키마 마이그레이션 |
| 수억 건 대용량 초기 스냅샷 도중 테이블 락 병목 | **`Consistent Snapshot Mode` (Lockless Snapshot) 옵션 적용** | 서비스 무중단 초기 동기화 완료 |
| 네트워크 단절 재연결 시 메시지 중복 발행 | **타깃 Sink 계층에 고유 PK 기반 UPSERT 및 멱등성 로직 강제** | 중복 데이터 왜곡 0화 |

#### 한줄 요약
- Binlog 보존 주기 확장, 스키마 레지스트리 연동, Lockless 스냅샷, 멱등 Sink로 운영한다.

## Ⅶ. 결론

- 실시간 동기화는 **로그 CDC**, 부하 격리는 **Kafka** 선택

#### 한줄 요약
- CDC는 소스 DB의 트랜잭션 로그를 직접 파싱하여 부하 없이 타깃 시스템으로 변경을 실시간 전파하는 현대 이벤트 주도 아키텍처의 필수 기술이다.