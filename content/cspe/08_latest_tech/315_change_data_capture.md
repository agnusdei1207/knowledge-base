---
title: "Change Data Capture 변경 데이터 캡처 (Change Data Capture)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 315
---

# 📖 【암기용】 개념 완전 이해

> 목적: Change Data Capture를 데이터베이스 변경 내용을 전체 재추출하지 않고 insert, update, delete 이벤트로 포착해 다른 시스템에 전달하는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: DB 변경분을 감지해 이벤트나 증분 데이터로 전달하는 데이터 동기화 기법
- **왜 필요한가**: 매번 전체 테이블을 복사하면 원천 DB 부하, 지연, 중복 처리, 삭제 반영 누락 문제가 생긴다.
- **핵심 직관**: 전체 장부를 매번 복사하지 않고 새로 적힌 거래와 수정·삭제 내역만 복사하는 방식임.

## 깊이 이해
- **배경·문제의식**: 데이터 웨어하우스, 검색색인, 캐시, 이벤트 기반 서비스는 원천 DB 변경을 업무 지연 SLA 안에서 받아야 한다.
- **작동 원리**: CDC는 transaction log/binlog/WAL을 읽거나 trigger, timestamp 비교로 변경을 감지하고 before/after image와 operation type을 event로 전달한다.
- **비유**: 신문 전체를 매일 다시 인쇄하지 않고 정정 기사와 신규 기사 목록만 배포해 구독자가 자기 사본을 갱신하는 방식이다.
- **구체 예시**: Debezium이 MySQL binlog를 읽어 `customers` 테이블의 insert/update/delete를 Kafka topic에 발행하고, sink connector가 lakehouse와 검색엔진을 갱신한다.
- **흔한 오해·주의점**: CDC는 항상 exactly-once를 보장하지 않는다. offset 관리, idempotent sink, schema evolution, tombstone 처리까지 설계해야 한다.

## 연결 개념
- Debezium — log-based CDC 오픈소스 플랫폼
- Kafka Connect — CDC source/sink connector 실행 프레임워크
- Lakehouse — CDC 이벤트의 분석 저장 대상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: CDC는 전체 적재 대체가 아니라 transaction log 기반 변경 이벤트, schema 변화, 삭제 반영, sink idempotence를 함께 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CDC는 원천 DB의 변경분을 감지해 다른 시스템에 이벤트 또는 증분 데이터로 전달하는 동기화 패턴임.
> 2. **가치**: 전체 추출 부하를 줄이고 검색, 캐시, lakehouse, MSA 이벤트를 업무 지연 SLA 안에서 갱신함.
> 3. **판단 포인트**: log-based CDC, operation type, offset, schema evolution, delete/tombstone, idempotent sink가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 데이터 동기화 방식 이해 확인 | full load vs incremental vs log-based CDC | 단순 polling으로만 설명 |
| 스트리밍 아키텍처 판단 확인 | DB log, connector, broker, sink | DB trigger만 제시 |
| 운영 리스크 확인 | schema 변경, delete, lag, 중복 | insert/update만 다룸 |

> 요약: 이 문제는 CDC를 변경 감지 방식과 downstream 정합성 설계까지 연결해야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | DB 변경분을 감지해 이벤트나 증분 데이터로 전달하는 데이터 동기화 기법 | "핵심 기술 요소" |
| **왜 필요한가** | 매번 전체 테이블을 복사하면 원천 DB 부하, 지연, 중복 처리, 삭제 반영 누락 문제가 생긴다 | "핵심 기술 요소" |
| **핵심 직관** | 전체 장부를 매번 복사하지 않고 새로 적힌 거래와 수정·삭제 내역만 복사하는 방식임 | "핵심 기술 요소" |
| **배경·문제의식** | 데이터 웨어하우스, 검색색인, 캐시, 이벤트 기반 서비스는 원천 DB 변경을 업무 지연 SLA 안에서 받아야 한다 | "서비스 약속" |
| **비유** | 신문 전체를 매일 다시 인쇄하지 않고 정정 기사와 신규 기사 목록만 배포해 구독자가 자기 사본을 갱신하는 방식이다 | "핵심 기술 요소" |
| **흔한 오해·주의점** | CDC는 항상 exactly-once를 보장하지 않는다 | "자동 배송 시스템" |
| **본질** | CDC는 원천 DB의 변경분을 감지해 다른 시스템에 이벤트 또는 증분 데이터로 전달하는 동기화 패턴임 | "자동 배송 시스템" |

---


## Ⅰ. 개요 및 필요성

- 개요: DB 변경분 캡처 기법
- 배경: 전체 테이블 재적재는 원천 DB 부하와 지연이 크고 delete/update 반영 오류가 발생하기 쉬움.
- 필요성: 운영 DB 변경을 Kafka, lakehouse, cache, search index에 증분 전파해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Source DB -> Transaction Log / Binlog / WAL -> CDC Connector
        +-> Kafka Topic / Event Bus
        +-> Sink Connector -> Lakehouse / Search / Cache
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source Log | commit된 변경 순서 제공 | binlog, WAL, redo log |
| CDC Connector | 변경 이벤트 생성과 offset 관리 | Debezium, Kafka Connect |
| Event Broker | 변경 이벤트 보관·전달 | topic per table |
| Sink Processor | upsert/delete 반영 | idempotent key 필요 |

> 요약: CDC는 DB transaction log에서 변경 순서를 읽고 broker를 통해 downstream 시스템에 증분 반영한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
초기 snapshot -> log position 저장 -> insert/update/delete 감지
-> change event 발행 -> sink upsert/delete -> offset commit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 초기 snapshot으로 기준 데이터 적재 | snapshot consistency |
| 2 | transaction log position부터 변경 이벤트 읽기 | log offset |
| 3 | operation type과 before/after image를 topic에 발행 | schema compatibility |
| 4 | sink가 primary key 기준 upsert/delete 수행 | idempotent result |

> 요약: CDC는 초기 snapshot과 이후 log stream을 연결해 전체 재적재 없이 데이터 상태를 동기화한다.

---

## Ⅳ. 특징

| 구분 | Batch Full Load | Query Polling | Log-Based CDC |
|:---|:---|:---|:---|
| 부하 | 전체 스캔 | 조건 쿼리 반복 | transaction log 읽기 |
| 지연 | 배치 주기 의존 | polling 주기 의존 | log 전달 지연 의존 |
| 삭제 반영 | 별도 비교 필요 | 누락 가능 | delete/tombstone 이벤트 |
| 정합성 | snapshot 시점 관리 필요 | update timestamp 의존 | commit order 추적 |

> 요약: Log-based CDC는 원천 DB 전체 스캔을 줄이고 commit 순서 기반 변경 이벤트를 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 동기화 주기 | 일/시간 단위 batch | 초~분 단위 변경 스트림 | 데이터 지연 SLA |
| 원천 부하 | full scan | log read | 운영 DB 여유 |
| downstream | overwrite table | upsert/delete sink | target 원자성 |

> 요약: CDC는 지연 요구가 낮고 원천 DB 전체 스캔이 부담인 경우 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| lag 증가 | connector 처리량 부족 | connector scale, topic partition 조정 | source-to-sink lag |
| schema 깨짐 | 컬럼 변경·타입 변경 | schema registry, compatibility rule | schema error count |
| 삭제 누락 | tombstone 미처리 | delete event contract | orphan record count |

> 요약: CDC 리스크는 lag, schema evolution, delete 처리이며 contract와 sink 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정합성 | 원천과 sink row count/key 일치 | reconciliation query |
| 지연 | source commit부터 sink 반영 SLA 충족 | event timestamp diff |
| 복구 | connector 재시작 후 offset 연속성 유지 | offset audit |

> 요약: CDC 성과는 이벤트 발행 수가 아니라 원천-sink 정합성, 지연, offset 복구로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 초기 snapshot 시점과 log position을 함께 기록하고, snapshot 이후 변경 이벤트와 중복되지 않게 connector를 구성함.
2. primary key, operation type, schema version, event timestamp를 CDC event contract에 포함함.
3. sink는 upsert/delete idempotence를 보장하고 원천-sink reconciliation job으로 정합성을 주기 검증함.

**결론 (2줄):**
- 기술사 판단: 낮은 지연의 데이터 동기화와 이벤트 기반 확장이 필요하면 log-based CDC가 적합하고, 단순 월간 보고는 batch가 단순함.
- 향후 방향: CDC는 Kafka, Flink, lakehouse table format과 결합해 실시간 데이터 제품과 AI feature pipeline의 입력 계층으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CDC를 설명하시오" | snapshot과 log stream 연결 흐름 | full load·polling 대비 차이 |
| 요구사항 명시형 | "데이터 동기화 방안을 제시하시오" | connector, broker, sink idempotence | lag·schema·delete 리스크 |

> 요약: 설명형은 변경 캡처 원리를, 방안형은 downstream 정합성과 운영 리스크를 중심으로 작성한다.
