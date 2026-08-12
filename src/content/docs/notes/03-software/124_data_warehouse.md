---
sidebar:
  order: 124
  label: "124. 데이터 웨어하우스 (Data Warehouse)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "데이터 웨어하우스 (Data Warehouse)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 124
extra:
  question_no: "124"
  source_status: "기출"
  source_history: "122회"
  priority: 30
  priority_note: "122회 기출, 분석 저장소 구조의 기본"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Data Warehouse (DW / 데이터 웨어하우스)**: 빌 인몬(Bill Inmon) 및 랄프 킴볼(Ralph Kimball)이 정립한 기업용 통합 의사결정 지원 분석 DB로, 주제 지향성(Subject-Oriented), 통합성(Integrated), 시계열성(Time-Variant), 비휘발성(Non-Volatile) 4대 특징을 지닌 데이터 집적소.
- **Star Schema vs Snowflake Schema**: 차원 모델링의 대표 2대 구조로, 중앙의 사실 테이블(Fact Table)을 중심으로 차원 테이블(Dimension Table)이 직접 1:N 조인(Star)되거나 차원 테이블이 재정규화(Snowflake)되는 형태.
- **Fact & Dimension Table**: 사실 테이블은 거래 금액, 수량 등 수치적 측정값(Measure) 및 FK 축적, 차원 테이블은 사용자, 상품, 날짜 등 분석 기준 텍스트 속성 관리.

</details>

- 정의/개념: 이종 산재된 운영계(OLTP) 데이터베이스로부터 데이터를 추출(ETL)하여, 4대 고유 특성(주제 지향, 통합, 시계열, 비휘발)을 기반으로 정제 및 축적하는 기업 통합 대용량 분석 DB인 **Data Warehouse**
- 배경/필요성: OLTP 운영 DB에 집계 쿼리 실행 시 발생하는 시스템 락업 방지, 기업 전사 레벨의 단일 진실 고리(Single Source of Truth) 확보 요구성

#### 한줄 요약

- 여러 부서의 장부를 같은 항목표와 시간축으로 다시 묶어 하나의 보고서를 만드는 분석 창고이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Subject-Oriented (주제 지향성)**: 고객, 상품, 매출 등 비즈니스 주요 주제 영역별 데이터 구성.
- **Time-Variant (시계열성)**: 데이터 갱신 시 과거 이력을 삭제하지 않고 5~10년 치 시간 차원의 스냅샷으로 축적.

</details>

- **4대 고유 특성 (Subject-Oriented, Integrated, Time-Variant, Non-Volatile)**
- **Star Schema & Snowflake Schema 기반 Dimensional Modeling**
- **Columnar Storage (열 지향 저장) & OLAP (On-Line Analytical Processing) 집계 지원**

#### 한줄 요약

- 데이터 웨어하우스는 여러 부서가 같은 지표 정의를 쓰게 하지만 원천 적재가 늦으면 보고서의 최신 시점도 늦어짐이 핵심이다.

## Ⅲ. 구조 및 구성요소 (데이터 웨어하우스 4대 핵심 구조 & 스타 스키마)

<details><summary>핵심 용어</summary>

- **SCD (Slowly Changing Dimension)**: 시간 경과에 따른 차원 속성의 변경(예: 유저 주소 변경)을 이력 관리하는 기술 (Type 1: 덮어쓰기, Type 2: 신규 행 추가 이력 보존).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Data Warehouse Star Schema Architecture              │
├────────────────────────────────────────────────────────────────────────┤
│  [Dim_Customer] ──────┐                        ┌────── [Dim_Product]   │
│  (Customer_ID, City)  │                        │  (Product_ID, Category)│
│                       ▼                        ▼                       │
│             ┌────────────────────────────────────┐                     │
│             │  Fact_Sales (Fact Table)           │                     │
│             │  • Sales_ID (PK)                   │                     │
│             │  • Customer_ID, Product_ID, Date_ID│                     │
│             │  • Amount, Quantity (Measures)     │                     │
│             └────────────────────────────────────┘                     │
│                       ▲                                                │
│  [Dim_Date] ──────────┘ (Date_ID, Year, Month, Day)                    │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 중앙의 Fact Table(측정값)과 주변의 Dimension Table(분석 축)이 직접 1:N 연결되는 스타 스키마 아키텍처.

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 실무 튜닝 지침 |
|:---|:---|:---|
| **Fact Table (사실)** | **비즈니스 트랜잭션의 수치 측정값(Amount, Qty) 및 FK 저장** | Row Count 수억~수십억 건, 열 지향 압축 |
| **Dimension Table (차원)**| **분석의 기준이 되는 텍스트 속성 및 카테고리 정보** | **SCD Type 2 (유효기간 `valid_from/to`) 적용** |
| **ETL Pipeline** | **운영 DB에서 Extract, Transform, Load 연산 수행** | 야간 배치 스케줄러(Airflow) 연동 |
| **Data Mart (DM)** | **전사 DW에서 특정 부서(마케팅, 재무) 전용으로 분출한 소형 DW** | 특정 도메인 맞춤 집계 테이블 |

#### 한줄 요약

- 원천 보관함, 정제소, 측정 장부, 분류표, 공통 지표 화면으로 구성된다.

## Ⅳ. 흐름도 (Kimball Bottom-Up vs Inmon Top-Down 아키텍처 흐름)

<details><summary>핵심 용어</summary>

- **Kimball vs Inmon**: 킴볼은 데이터 마트(DM)를 선 구축 후 통합하는 Bottom-Up 방식, 인몬은 전사 DW를 선 구축 후 마트로 분출하는 Top-Down 방식.

</details>

```text
[1. Inmon Enterprise DW Architecture (Top-Down)]
 Operational DBs ──► ETL ──► [Enterprise DW (3NF)] ──► [Data Marts] ──► BI / Report

[2. Kimball Dimensional Architecture (Bottom-Up)]
 Operational DBs ──► ETL ──► [Dimensional Data Marts (Star Schema)] ──► BI / Report
```

### 동작 원리

1. **Inmon Model**: 정교한 3NF 정규화 기반 전사 DW 선 구축 후 Data Mart 분출 (구축 기간 길고 완벽한 일관성).
2. **Kimball Model**: 스타 스키마 차원 모델링 기반 Data Mart를 먼저 구축 후 연결 통합 (초기 구축 빠르고 현업 반응 우수).

#### 한줄 요약

- 서로 다른 이름표를 공통 분류표에 맞춘 뒤 거래 이력을 쌓아 같은 매출 지표를 제공한다.

## Ⅴ. 종류 및 비교 (Star Schema vs Snowflake Schema)

<details><summary>핵심 용어</summary>

- **Snowflake Schema**: 스타 스키마의 차원 테이블을 2NF/3NF로 추가 재정규화하여 디스크 중복을 줄인 형태 (조인 수 증가).

</details>

| 비교 항목 | Star Schema (스타 스키마) | Snowflake Schema (스노우플레이크 스키마) |
|:---|:---|:---|
| **차원 테이블 정규화**| **비정규화 (Denormalized, 단순 구조)** | **정규화 (Normalized 3NF, 복잡한 계층 구조)** |
| **조인(`JOIN`) 복잡도** | **낮음 (Fact와 Dim 간 1단계 direct 조인)** | 높음 (Dim 간 다단계 조인 필요) |
| **쿼리 처리 속도** | **초고속 (OLAP BI 쿼리에 최적화)** | 비교적 느림 (조인 오버헤드 증가) |
| **스토리지 용량** | 비정규화로 약간의 데이터 중복 발생 | **중복 0% (디스크 저장 용량 최소화)** |

#### 한줄 요약

- 온라인 트랜잭션 처리는 지금 거래를 처리하고 웨어하우스는 정리된 이력을 분석하며 레이크는 원본을 넓게 보관한다.

## Ⅵ. 실무 고려사항 및 대책 (DW 성능 최적화 3대 기법)

<details><summary>핵심 용어</summary>

- **Columnar Storage & Partitioning**: DW 데이터를 행(Row)이 아닌 컬럼(Column) 단위로 디스크에 수평 정렬하여, 특정 컬럼 집계 쿼리 처리속도 10배 이상 가속화.

</details>

| 성능 최적화 기법 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **Columnar Format** | 행 기반 파일 탐색으로 무의미한 I/O 발생 | **Parquet / ORC 열 지향 저장 포맷 전면 적용** |
| **Partition & Sort Key**| 수억 건 Fact 테이블 풀 스캔 | **날짜 파티셔닝 (`date_key`) 및 조회 조건 Sort Key 설정** |
| **SCD Type 2 Overwrite**| 차원 변경 시 과거 이력 유실 | **`effective_date / current_flag` 컬럼 추가 이력 관리**|

> 사례: **Snowflake / AWS Redshift / Google BigQuery 모던 클라우드 DW 구축**

#### 한줄 요약

- 한 행이 무엇을 뜻하고 어느 시점의 분류를 쓰는지 정해야 과거 매출이 바뀌지 않는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **DW 수립 기준(Data Warehouse Standards)**: Kimball 차원 모델링, Star Schema, Parquet Columnar 포맷 및 Cloud DW(Snowflake) 수용성에 의거한 체계.

</details>

- **DW 수립 기준**에 따라 전사 BI/분석 시스템 구축 시 **Snowflake / Redshift & Star Schema** 필수 적용

#### 한줄 요약

- 같은 숫자의 뜻•출처•기준 시점을 모두 설명할 수 있어야 믿을 수 있는 분석 저장소이다.
