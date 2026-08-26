---
sidebar:
  order: 110
  label: "110. 시계열 데이터베이스"
  badge:
    text: "미출 · 30%"
    variant: note
title: "시계열 데이터베이스 (Time Series Database)"
date: "2026-08-26T13:10:00+09:00"
tags:
  - "notes-software"
weight: 110
extra:
  question_no: "110"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "시계열 수집•보존•다운샘플링 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TSDB(Time Series Database)**: 시간(Timestamp)을 1차 기준으로 삼아 대규모 수치 데이터를 고속 적재하고 시간 범위 집계에 특화된 데이터베이스.
- **Downsampling & Retention Policy**: 오래된 고해상도 데이터를 저해상도 대표값(평균/최대)으로 요약하고 원본을 자동 삭제하는 수명주기 정책.

</details>

- 정의/개념: 시간의 흐름에 따라 발생하는 연속 측정 데이터를 **초고속 적재하고 시간 범위 집계 및 자동 다운샘플링·보존 정책(Retention)에 특화**된 데이터베이스
- 배경/필요성: 고빈도 측정값 증가로 RDBMS의 **쓰기·구간 집계 성능 제약**

#### 한줄 요약
- 시간 인덱싱과 델타 압축, 다운샘플링을 통해 대규모 시계열 데이터를 효율적으로 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Append-Only Write**: 갱신이나 삭제 없이 시간 순서대로 덧붙이기만 수행하여 쓰기 I/O를 극대화하는 구조.
- **Gorilla Compression**: 페이스북이 고안한 시계열 압축 기법으로, 타임스탬프 델타와 부동소수점 XOR 차이값만 저장하여 90% 이상 용량 절감.

</details>

- 갱신/삭제 없는 시간 순차 추가 기반의 **초고속 순차 쓰기(Append-Only Write)**
- 타임스탬프 및 수치 변화량만을 인코딩하는 **델타 압축(Gorilla Delta-of-Delta)**
- 시간 경과에 따라 데이터 해상도를 조절하는 **연속 다운샘플링 및 보존 정책(Retention)**

#### 한줄 요약
- 덧붙이기 전용 쓰기, 고효율 델타 압축, 수명주기 자동화로 시계열 데이터를 최적화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TSDB 핵심 구조**: Metric & Tag(식별 인덱스), Time Partition(시간 단위 파티셔닝), Compressed Block(압축 청크), Retention Worker(보존 관리자).

</details>

```text
[TSDB 시계열 데이터 저장 및 수명주기 파이프라인]
|-- Ingestion Layer (고속 수집기: 초당 수십만 메트릭 버퍼링)
`-- Time-Series Storage Engine
    |-- Tag Index (역색인 / Inverted Index: host, region 등 다차원 필터링)
    |-- Time Partitioning (시간 단위 파티션 분할: 일별/주별 청크 생성)
    |-- Columnar Compressed Chunk (Gorilla XOR + Double Delta 압축)
    `-- Lifecycle Engine (Downsampling 집계 + Retention 자동 만료 파기)
```

선의 의미: 계층 및 수집된 시계열 데이터가 태그 인덱싱과 시간 파티션을 거쳐 압축·보존 관리되는 구조

| 구성요소 | 책임 |
|:---|:---|
| 메트릭·태그 | 시계열 식별과 **다차원 역색인** |
| 시간 파티션 | 구간별 **조회·일괄 삭제 가속** |
| Gorilla 압축 엔진 | 시각·수치 차이의 **비트 압축** |
| 수명주기 관리자 | **다운샘플링·보존 정책** 실행 |

#### 한줄 요약
- 태그 인덱스, 시간 파티션, 압축 청크, 보존 관리자가 결합하여 시계열을 수명주기별로 통제한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **High Cardinality**: 태그 조합의 고유 개수가 수천만 개로 폭증하여 인덱스 메모리가 고갈되는 현상.

</details>

```text
IoT 센서 및 서버 모니터링 메트릭 유입
        │
   [시계열 식별] Metric 이름과 Tag 집합을 매핑하여 해당 Series ID 식별 ($O(1)$)
        │
   [시간 파티션 배치] Timestamp 기준으로 현재 활성 시간 청크 메모리 버퍼에 할당
        │
   [델타 압축 및 디스크 플러시] Gorilla 알고리즘으로 압축 후 디스크 불변 블록에 기록
        │
   [다운샘플링 롤업] 7일 경과 시 초 단위 데이터를 5분 평균/최대값으로 자동 재집계
        │
   [보존 정책 만료] 30일 초과된 원본 시간 파티션 블록을 디스크에서 즉시 일괄 삭제
```

#### 한줄 요약
- 시계열 식별 → 시간 파티션 배치 → 델타 압축 플러시 → 다운샘플링 롤업 → 만료 삭제 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TSDB vs RDBMS**: 시계열 전용 압축과 시간 파티셔닝에 특화된 TSDB와 범용 정규화 테이블을 관리하는 RDBMS.

</details>

| 비교 항목 | 범용 RDBMS (PostgreSQL, MySQL) | 전용 TSDB (Prometheus, InfluxDB, TimescaleDB) |
|:---|:---|:---|
| 데이터 쓰기 패턴 | 임의 행 갱신(Update) 및 단건 삭제 | **100% 시간순 덧붙이기 쓰기 (Append-Only)** |
| 압축률 및 효율 | 범용 페이지 압축 (보통 2~3배) | **Gorilla 전용 비트 압축 (최대 10~20배 압축)** |
| 시간 범위 집계 | B+Tree 인덱스 스캔 부하 발생 | **시간 파티션 기반 연속 집계(Continuous Aggregate)** |
| 데이터 수명주기 | 수동 `DELETE`로 인한 디스크 파편화 | **시간 청크 단위 즉시 Drop 및 자동 Downsampling** |

#### 한줄 요약
- 정형 비즈니스 원장은 RDBMS, 시간 변화와 구간 통계 중심 데이터는 TSDB를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cardinality Explosion**: 태그 필드에 사용자 ID나 UUID 같은 유일값을 넣어 인덱스 엔트리가 수억 개로 폭증하는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| UUID/User-ID 태그 지정으로 **High Cardinality** 인덱스 폭발 | **고선택성 고유값은 Tag 대신 Value/Field로 격리 지정** | 인덱스 메모리 폭주 원천 차단 |
| 초 단위 원본 데이터 영구 보관으로 인한 디스크 고갈 | **Retention Policy 수립 (7일 보관 후 1시간 단위 다운샘플링)** | 스토리지 비용 90% 절감 |
| 서버 간 클럭 오차(Clock Drift)로 인한 타임스탬프 역전 | **NTP 시간 동기화 강제 및 Late-Arriving 허용 윈도 버퍼 설정** | 시계열 정렬 무결성 보장 |
| 피크 시 메트릭 폭증으로 인한 수집 엔진 다운 | **전면에 Kafka/Vector 버퍼 큐 배치 및 배치 쓰기(Batch Write)** | 수집 지연 스파이크 흡수 |

#### 한줄 요약
- 태그 카디널리티 제어, 다운샘플링 정책, NTP 동기화, 카프카 버퍼링으로 운영한다.

## Ⅶ. 결론

- 시계열 수집은 **TSDB**, 용량 최적화는 **다운샘플링** 선택

#### 한줄 요약
- TSDB는 시간 인덱싱과 고효율 델타 압축, 수명주기 관리를 통해 대규모 시계열 데이터를 최적 처리하는 특화 데이터베이스다.
