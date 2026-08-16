---
sidebar:
  order: 124
  label: "124. 데이터 웨어하우스 (Data Warehouse)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "데이터 웨어하우스 (Data Warehouse)"
date: "2026-08-13T23:06:00+09:00"
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

<details><summary>용어 설명</summary>

- **Data Warehouse (DW / 데이터 웨어하우스)**: 빌 인몬(Bill Inmon) 및 랄프 킴볼(Ralph Kimball)이 정립한 기업용 통합 의사결정 지원 분석 DB로, 주제 지향성(Subject-Oriented), 통합성(Integrated), 시계열성(Time-Variant), 비휘발성(Non-Volatile) 4대 특징을 지닌 데이터 집적소.
- **Star Schema vs Snowflake Schema**: 차원 모델링의 대표 2대 구조로, 중앙의 사실 테이블(Fact Table)을 중심으로 차원 테이블(Dimension Table)이 직접 1:N 조인(Star)되거나 차원 테이블이 재정규화(Snowflake)되는 형태.
- **Fact & Dimension Table**: 사실 테이블은 거래 금액, 수량 등 수치적 측정값(Measure) 및 FK 축적, 차원 테이블은 사용자, 상품, 날짜 등 분석 기준 텍스트 속성 관리.

</details>

- 정의/개념: 통합 이력을 주제별 분석에 제공하는 **데이터 웨어하우스**
- 배경/필요성: 운영 DB 직접 집계는 **업무 부하•지표 정의 불일치** 유발

#### 한줄 요약

- 여러 부서의 장부를 같은 항목표와 시간축으로 다시 묶어 하나의 보고서를 만드는 분석 창고이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Subject-Oriented (주제 지향성)**: 고객, 상품, 매출 등 비즈니스 주요 주제 영역별 데이터 구성.
- **Time-Variant (시계열성)**: 데이터 갱신 시 과거 이력을 삭제하지 않고 5~10년 치 시간 차원의 스냅샷으로 축적.

</details>

- **4대 고유 특성 (Subject-Oriented, Integrated, Time-Variant, Non-Volatile)**
- **Star Schema & Snowflake Schema 기반 Dimensional Modeling**
- **Columnar Storage (열 지향 저장) & OLAP (On-Line Analytical Processing) 집계 지원**

#### 한줄 요약

- 데이터 웨어하우스는 여러 부서가 같은 지표 정의를 쓰게 하지만 원천 적재가 늦으면 보고서의 최신 시점도 늦어짐이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| Fact Table | 정해진 Grain의 측정값•차원 키 저장 |
| Dimension Table | 분석 축의 설명 속성과 이력 관리 |
| ETL•ELT Pipeline | 원천 추출•표준화•품질 검증•적재 |
| Data Mart | 부서•주제별 분석 모델과 집계 제공 |

#### 한줄 요약

- 원천 보관함, 정제소, 측정 장부, 분류표, 공통 지표 화면으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Kimball vs Inmon**: 킴볼은 데이터 마트(DM)를 선 구축 후 통합하는 Bottom-Up 방식, 인몬은 전사 DW를 선 구축 후 마트로 분출하는 Top-Down 방식.

</details>

```text
[운영계 원천]
      │
      ▼
1. 변경 데이터 추출
      │
      ▼
2. 공통 코드•품질 정제
      │
      ▼
3. Fact•Dimension 적재
      │
      ▼
4. 주제 집계 생성
      │
      ▼
5. 지표•리니지 제공
```

### 동작 원리

1. 변경 데이터 추출: 배치•CDC로 원천 이력 수집
2. 공통 코드•품질 정제: 명칭•단위•키•오류 표준화
3. Fact•Dimension 적재: Grain과 SCD 정책에 따라 저장
4. 주제 집계 생성: 반복 질의를 위한 마트•요약 구성
5. 지표•리니지 제공: 정의•출처•기준 시점과 함께 서빙

#### 한줄 요약

- 서로 다른 이름표를 공통 분류표에 맞춘 뒤 거래 이력을 쌓아 같은 매출 지표를 제공한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Snowflake Schema**: 스타 스키마의 차원 테이블을 2NF/3NF로 추가 재정규화하여 디스크 중복을 줄인 형태 (조인 수 증가).

</details>

| 비교 항목 | Star Schema (스타 스키마) | Snowflake Schema (스노우플레이크 스키마) |
|:---|:---|:---|
| 차원 테이블 정규화 | **비정규화 (Denormalized, 단순 구조)** | **정규화 (Normalized 3NF, 복잡한 계층 구조)** |
| 조인(`JOIN`) 복잡도 | **낮음 (Fact와 Dim 간 1단계 direct 조인)** | 높음 (Dim 간 다단계 조인 필요) |
| 쿼리 처리 특성 | 조인 단계가 적어 단순 | 차원 계층 조인 비용 증가 |
| 스토리지 용량 | 차원 속성 중복 가능 | 정규화로 차원 중복 감소 |

#### 한줄 요약

- 온라인 트랜잭션 처리는 지금 거래를 처리하고 웨어하우스는 정리된 이력을 분석하며 레이크는 원본을 넓게 보관한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Columnar Storage & Partitioning**: DW 데이터를 행(Row)이 아닌 컬럼(Column) 단위로 디스크에 수평 정렬하여, 특정 컬럼 집계 쿼리 처리속도 10배 이상 가속화.

</details>

| 성능 최적화 기법 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| Columnar Format | 행 기반 파일 탐색으로 무의미한 I/O 발생 | **Parquet / ORC 열 지향 저장 포맷 전면 적용** |
| Partition & Sort Key | 수억 건 Fact 테이블 풀 스캔 | **날짜 파티셔닝 (`date_key`) 및 조회 조건 Sort Key 설정** |
| SCD Type 2 Overwrite | 차원 변경 시 과거 이력 유실 | **`effective_date / current_flag` 컬럼 추가 이력 관리**|

> 사례: **Snowflake / AWS Redshift / Google BigQuery 모던 클라우드 DW 구축**

#### 한줄 요약

- 한 행이 무엇을 뜻하고 어느 시점의 분류를 쓰는지 정해야 과거 매출이 바뀌지 않는다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DW 수립 기준(Data Warehouse Standards)**: Kimball 차원 모델링, Star Schema, Parquet Columnar 포맷 및 Cloud DW(Snowflake) 수용성에 의거한 체계.

</details>

- 조회 단순성은 **Star**, 차원 계층 재사용은 Snowflake 선택

#### 한줄 요약

- 같은 숫자의 뜻•출처•기준 시점을 모두 설명할 수 있어야 믿을 수 있는 분석 저장소이다.
