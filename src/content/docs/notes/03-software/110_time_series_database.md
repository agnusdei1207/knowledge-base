---
sidebar:
  order: 110
  label: "110. 시계열 데이터베이스 (Time Series Database)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "시계열 데이터베이스 (Time Series Database)"
date: "2026-08-13T21:28:00+09:00"
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

- **TSDB (Time Series Database / 시계열 데이터베이스)**: 시간의 흐름(Timestamp)에 따라 발생하는 연속적인 수치 측정 데이터(Metrics, Log, Event, Financial Tick)를 고속 적재하고, 압축 및 다운샘플링(Downsampling) 처리에 특화된 전용 데이터베이스.
- **Timestamp Indexing**: 타임스탬프를 1차 클러스터링 인덱스 키로 지정하여 시간 범위 검색(`WHERE time >= now() - 1h`)을 $O(1)$ 수준으로 가속화하는 구조.
- **Downsampling & Retention Policy**: 시간이 오래된 고해상도 초 단위 데이터를 5분/1시간 단위의 대표 통계값(Avg, Max, Min)으로 축약(Downsample)하고 오래된 원본을 자동 파기(Retention)하는 수명주기 관리 정책.

</details>

- 정의/개념: 시간순 측정값의 적재•집계•보존에 특화된 **TSDB**
- 배경/필요성: 고빈도 측정값 누적으로 **저장량•시간 범위 집계 비용** 증가

#### 한줄 요약

- 시간 도장이 찍힌 측정값을 빠르게 쌓고 요약 및 보관하는 데이터베이스이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **High-Rate Append-Only Write**: 갱신(Update) 및 삭제(Delete)가 거의 발생하지 않고, 무조건 시간 순서대로 덧붙이는 쓰기 전용 특성.
- **Gorilla Compression Algorithm**: 페이스북이 개발한 시계열 압축 알고리즘으로, 타임스탬프와 수치 float 값의 XOR 차이값만 저장해 90% 이상 디스크 압축률 달성.

</details>

- **Append-Only Write**: 시간순 덧붙이기 중심 쓰기 경로
- **Delta Compression**: 값•시간 차이를 활용한 압축
- **Continuous Downsampling & Retention Policy (수명주기 자동화)**

#### 한줄 요약

- 연속 쓰기에 강하지만 태그가 폭증하면 색인과 메모리 비용이 커진다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Metric & Tags (Labels)**: `cpu_usage{host="server01", region="us-east"}`와 같이 메트릭 이름과 메타데이터 태그(Tag Set)의 조합 구조.

</details>

```text
[시계열 표본] ───── [태그 인덱스]
      │                   │
[시간 파티션] ───── [압축 블록]
      │                   │
[집계 규칙] ─────── [보존 정책]
```

선의 의미: 표본 식별•시간 배치•압축•집계•보존의 정적 관계.

| 구성요소 | 책임 |
|:---|:---|
| 시계열 표본 | 시간•메트릭•태그•필드 값 저장 |
| 태그 인덱스 | 시계열 식별과 필터 후보 탐색 |
| 시간 파티션 | 시간 범위별 데이터 배치•제거 |
| 압축 블록 | 시간•값 차이를 묶어 저장량 절감 |
| 집계 규칙 | 구간별 평균•최댓값 등 생성 |
| 보존 정책 | 해상도별 보관 기간과 삭제 관리 |

#### 한줄 요약

- 측정 이름표, 색인, 시간 상자, 압축 묶음, 보존 담당자로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **High Cardinality**: 태그(Tag) 값의 조합 수가 무한히 많아져(예: `user_id`를 태그로 삽입), TSDB 인덱스 메모리가 수십 GB 이상 폭증하여 DB가 다운되는 안티패턴.

</details>

```text
[측정값 수신]
      │
      ▼
1. 시계열 식별
      │
      ▼
2. 시간 파티션 배치
      │
      ▼
3. 압축 블록 기록
      │
      ▼
4. 구간 집계 생성
      │
      ▼
5. 보존 만료 처리
      │
      ▼
[조회용 데이터]
```

### 동작 원리

1. **시계열 식별**: 메트릭과 태그 집합으로 계열 결정
2. **시간 파티션 배치**: 타임스탬프로 저장 구간 선택
3. **압축 블록 기록**: 시간•값 차이를 압축해 저장
4. **구간 집계 생성**: 정책별 해상도의 요약값 계산
5. **보존 만료 처리**: 만료 원본•집계 파티션 제거

#### 한줄 요약

- 측정값을 시간 상자에 모아 압축하고 오래된 구간은 요약값만 남긴다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TimescaleDB vs InfluxDB**: TimescaleDB는 PostgreSQL 기반의 확장 TSDB(SQL 통용), InfluxDB는 전용 NoSQL 엔진.

</details>

| 비교 항목 | RDBMS (PostgreSQL, MySQL) | TSDB (Prometheus, InfluxDB, TimescaleDB) |
|:---|:---|:---|
| 데이터 갱신/삭제 | 업무 행 갱신•삭제 지원 | **덧붙이기 중심•지연 표본 처리** |
| 압축률 및 용량 | 범용 행•열 압축 적용 | **시간•값 상관성을 활용한 압축** |
| 시간 범위 집계 | 인덱스•파티션 설계에 좌우 | **시간 파티션•연속 집계 활용** |
| 데이터 수명주기 | 수동 `DELETE FROM` (디스크 파편화) | **자동 Retention Policy & Downsampling** |

#### 한줄 요약

- 시계열 모델 선택 기준에서 관계형 데이터베이스는 업무 관계를, 시계열 데이터베이스는 시간 변화와 구간 통계를 다룬다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **TSDB 수립 기준(TSDB Architecture Standards)**: Ingestion QPS, High Cardinality 제어, Gorilla 압축 및 Retention Downsampling 정책에 의거한 체계.

</details>

- 시간 범위 집계•보존 자동화가 핵심이면 **TSDB** 선택

#### 한줄 요약

- 시계열 보존 적용 기준은 측정 주기•보존 기간•해상도를 함께 정한다.
