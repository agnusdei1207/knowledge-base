---
sidebar:
  order: 110
  label: "110. 시계열 데이터베이스 (Time Series Database)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "시계열 데이터베이스 (Time Series Database)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **TSDB (Time Series Database / 시계열 데이터베이스)**: 시간의 흐름(Timestamp)에 따라 발생하는 연속적인 수치 측정 데이터(Metrics, Log, Event, Financial Tick)를 고속 적재하고, 압축 및 다운샘플링(Downsampling) 처리에 특화된 전용 데이터베이스.
- **Timestamp Indexing**: 타임스탬프를 1차 클러스터링 인덱스 키로 지정하여 시간 범위 검색(`WHERE time >= now() - 1h`)을 $O(1)$ 수준으로 가속화하는 구조.
- **Downsampling & Retention Policy**: 시간이 오래된 고해상도 초 단위 데이터를 5분/1시간 단위의 대표 통계값(Avg, Max, Min)으로 축약(Downsample)하고 오래된 원본을 자동 파기(Retention)하는 수명주기 관리 정책.

</details>

- 정의/개념: 시간의 경과에 따른 연속적 메트릭/로그 데이터를 고속 적재하고, 시간 윈도 범위 조회 및 데이터 자동 다운샘플링/보존(Retention) 정책을 전담하는 특화 DB인 **TSDB (Time Series Database)**
- 배경/필요성: IoT 센서, 서버 모니터링(Prometheus), 주식 차트 등 초당 수십만 건의 시계열 적재 시 일반 RDBMS/NoSQL의 디스크 용량 폭증 및 범위 조회 지연 극복 요구성

#### 한줄 요약

- 시간 도장이 찍힌 측정값을 빠르게 쌓고 요약 및 보관하는 데이터베이스이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **High-Rate Append-Only Write**: 갱신(Update) 및 삭제(Delete)가 거의 발생하지 않고, 무조건 시간 순서대로 덧붙이는 쓰기 전용 특성.
- **Gorilla Compression Algorithm**: 페이스북이 개발한 시계열 압축 알고리즘으로, 타임스탬프와 수치 float 값의 XOR 차이값만 저장해 90% 이상 디스크 압축률 달성.

</details>

- **Append-Only Write (100% 순차 쓰기 I/O 최적화)**
- **High Data Compression Ratio (Gorilla 압축 알고리즘 기반 90%+ 디스크 절감)**
- **Continuous Downsampling & Retention Policy (수명주기 자동화)**

#### 한줄 요약

- 연속 쓰기에 강하지만 태그가 폭증하면 색인과 메모리 비용이 커진다.

## Ⅲ. 구조 및 구성요소 (TSDB 데이터 모델 및 압축 파이프라인)

<details><summary>핵심 용어</summary>

- **Metric & Tags (Labels)**: `cpu_usage{host="server01", region="us-east"}`와 같이 메트릭 이름과 메타데이터 태그(Tag Set)의 조합 구조.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        TSDB Arch & Downsampling Pipeline               │
├────────────────────────────────────────────────────────────────────────┤
│ Write ──► [WAL Log] ──► [In-Memory Buffer] ──► [TSM Block File (Disk)] │
│                                                      │                 │
│ Raw Data (1s resolution, 7 Days) ────────────────────┤                 │
│    │ (Downsampling Rule)                             ▼                 │
│    └──────────────────────────► Aggregated Data (1h resolution, 1 Year)│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 초 단위 원본 데이터를 고속 적재한 후 다운샘플링 룰을 통해 장기 보관용 1시간 단위 통계 데이터로 축약 및 원본 파기하는 구조.

| 구성요소 (Component) | 역할 및 기술 메커니즘 | 대표적 실무 제품 예시 |
|:---|:---|:---|
| **Data Model** | **`Timestamp + Metric Name + Tag-Set + Float Value`** | **Prometheus, InfluxDB, TimescaleDB** |
| **Storage Engine** | **TSM (Time Structured Merge-tree)** | InfluxDB의 시계열 전용 엔진 |
| **Compression** | **Gorilla XOR Delta-of-Delta Compression** | 타임스탬프 및 수치 비트 압축 |
| **Downsampling Engine**| **CQ (Continuous Query) / Retention Policy** | 시간 경과 데이터 자동 요약/삭제 |

#### 한줄 요약

- 측정 이름표, 색인, 시간 상자, 압축 묶음, 보존 담당자로 구성된다.

## Ⅳ. 흐름도 (High Cardinality 문제 및 Downsampling 흐름)

<details><summary>핵심 용어</summary>

- **High Cardinality**: 태그(Tag) 값의 조합 수가 무한히 많아져(예: `user_id`를 태그로 삽입), TSDB 인덱스 메모리가 수십 GB 이상 폭증하여 DB가 다운되는 안티패턴.

</details>

```text
[High-Frequency Sensor Data (100k/s Input)]
                    │
                    ▼
       [Gorilla Compression & TSM Block Ingestion]
                    │
                    ▼ (1주일 경과 시)
 [Retention Engine: 1초 원본 DROP, 1시간 AVG/MAX/MIN 축약본 유지]
```

### 동작 원리

1. **Ingestion**: 초당 수십만 건의 메트릭 데이터를 Gorilla Delta-of-Delta 압축 후 TSM 블록에 순차 저장.
2. **Downsampling Trigger**: 7일이 지난 데이터에 대해 1시간 단위 `AVG, MAX, MIN, SUM` 요약 데이터로 축약 생성.
3. **Retention Purge**: 7일 넘은 1초 해상도 원본 디스크 블록을 `DROP`하여 저장 공간 90% 회수.

#### 한줄 요약

- 측정값을 시간 상자에 모아 압축하고 오래된 구간은 요약값만 남긴다.

## Ⅴ. 종류 및 비교 (RDBMS vs TSDB)

<details><summary>핵심 용어</summary>

- **TimescaleDB vs InfluxDB**: TimescaleDB는 PostgreSQL 기반의 확장 TSDB(SQL 통용), InfluxDB는 전용 NoSQL 엔진.

</details>

| 비교 항목 | RDBMS (PostgreSQL, MySQL) | TSDB (Prometheus, InfluxDB, TimescaleDB) |
|:---|:---|:---|
| 데이터 갱신/삭제 | **자주 발생 (In-Place Update)** | **발생 안 함 (Append-Only Write)** |
| 압축률 및 용량 | 보통 (기본 16KB 페이지 구조) | **극대화 (Gorilla 압축 알고리즘 90%+)** |
| 시간 범위 집계속도 | 느림 (`GROUP BY date_trunc` 인덱스 한계) | **초고속 (시간 윈도 파티션 및 미리 렌더링)**|
| 데이터 수명주기 | 수동 `DELETE FROM` (디스크 파편화) | **자동 Retention Policy & Downsampling** |

#### 한줄 요약

- 시계열 모델 선택 기준에서 관계형 데이터베이스는 업무 관계를, 시계열 데이터베이스는 시간 변화와 구간 통계를 다룬다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Cardinality Control**: 태그 키-값으로 유일한 값(UUID, User ID, IP 등)을 절대 넣지 않고, 카테고리성 범주값만 사용하는 규칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| `user_id`를 Tag로 지정하여 **High Cardinality** 인덱스 폭발 | **고선택성 고유값은 Tag 대신 Value/Field로 지정** | 메모리 락업 방지 |
| 원본 초 단위 데이터를 영구 보관하여 디스크 고갈 | **Retention Policy (7일 후 1시간 다운샘플링 및 파기)** | 디스크 90% 절감 |
| 클럭 디비에이션(Clock Drift)으로 타임스탬프 역전 | **NTP (Network Time Protocol) 동기화 및 Late Data 허용 윈도**| 수집 정합성 보장 |

> 사례: **쿠버네티스 클러스터 모니터링 (Prometheus + Thanos) & Smart Factory IoT TSDB 구축**

#### 한줄 요약

- 이름표 종류를 제한하고 오래된 원본은 필요한 통계만 남겨 비용을 관리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **TSDB 수립 기준(TSDB Architecture Standards)**: Ingestion QPS, High Cardinality 제어, Gorilla 압축 및 Retention Downsampling 정책에 의거한 체계.

</details>

- **TSDB 수립 기준**에 따라 IT 인프라 모니터링/IoT 시스템 구축 시 **Prometheus / TimescaleDB & Downsampling** 필수 수용

#### 한줄 요약

- 시계열 보존 적용 기준은 측정 주기•보존 기간•해상도를 함께 정한다.
