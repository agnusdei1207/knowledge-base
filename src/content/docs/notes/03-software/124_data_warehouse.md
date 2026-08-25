---
sidebar:
  order: 124
  label: "124. 데이터 웨어하우스"
  badge:
    text: "기출 · 30%"
    variant: note
title: "데이터 웨어하우스 (Data Warehouse)"
date: "2026-08-25T11:00:00+09:00"
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

- **데이터 웨어하우스(DW)**: 전사 비즈니스 의사결정을 지원하기 위해 다수의 원천 시스템으로부터 데이터를 추출·변환하여 통합 저장하는 분석용 DB.
- **DW 4대 특성(Inmon)**: 주제 지향성(Subject-Oriented), 통합성(Integrated), 시계열성(Time-Variant), 비휘발성(Non-Volatile).

</details>

- 정의/개념: 기업의 의사결정을 지원하기 위해 **주제 지향성, 통합성, 시계열성, 비휘발성 4대 특성을 바탕으로 전사 이력 데이터를 정제·저장**하는 분석용 데이터베이스
- 배경/필요성: 운영 OLTP DB를 대상으로 직접 대규모 통계 쿼리 실행 시 발생하는 **트랜잭션 성능 급락, 지표 정의 불일치 및 다차원 분석 한계 해결 불가**

#### 한줄 요약
- 4대 특성과 차원 모델링을 기반으로 전사 단일 진실 공급원(SSOT) 분석 환경을 구축한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Star Schema**: 중앙의 사실 테이블(Fact Table)과 주변의 비정규화된 차원 테이블(Dimension Table)이 1단계로 직결되는 모델링.
- **SCD(Slowly Changing Dimension)**: 시간의 흐름에 따라 변화하는 고객 주소 등의 차원 속성 이력을 보존하는 기법(Type 2: 신규 행 추가).

</details>

- 주제 지향성, 통합성, 시계열성, 비휘발성의 **4대 엔지니어링 특성 완비**
- Fact Table(수치 측정값)과 Dimension Table(분석 축) 기반의 **차원 모델링(Dimensional Modeling)**
- 대용량 집계 쿼리를 가속화하는 **열 지향 저장(Columnar Storage) 및 OLAP 최적화**

#### 한줄 요약
- 4대 특성과 스타 스키마 기반 차원 모델링을 통해 고속 다차원 분석을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Fact Table vs Dimension Table**: 매출액 등 수치 측정값을 담는 사실 테이블과 고객/상품/일자 등 분석 기준을 담는 차원 테이블.

</details>

```text
[데이터 웨어하우스 스타 스키마 아키텍처]
|-- Dim_Customer (고객 차원: Customer_ID PK, Name, City, Segment)
|-- Dim_Product (상품 차원: Product_ID PK, Category, Brand)
|-- Dim_Date (날짜 차원: Date_ID PK, Year, Quarter, Month, Day)
`-- Fact_Sales (매출 사실 테이블)
    |-- FK 연결 (Customer_ID, Product_ID, Date_ID)
    `-- Measures 수치 측정값 (Amount, Quantity, Discount_Rate)
```

선의 의미: 계층 및 중앙의 Fact Table(측정값)과 주변의 Dimension Table(분석 축)이 1:N 연결되는 스타 스키마 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **사실 테이블 (Fact Table)** | 매출액, 판매 수량 등 비즈니스 수치 측정값(Measure)과 **차원 외래키(FK)를 정밀 보관** | 수억 건 이상의 대용량 |
| **차원 테이블 (Dimension)** | 분석의 기준이 되는 고객, 상품, 지역, 일자의 **상세 설명 속성 및 이력(SCD) 관리** | 스타 스키마 비정규화 |
| **ETL/ELT 파이프라인** | 다양한 원천 시스템에서 데이터를 추출(Extract), 변환(Transform), **DW로 적재(Load)** | 배치/CDC 기반 동기화 |
| **데이터 마트 (Data Mart)** | 특정 부서(마케팅, 재무 등)의 특화된 목적을 위해 **DW에서 요약 가공된 서브셋** | 부서별 특화 OLAP |

#### 한줄 요약
- 사실 테이블, 차원 테이블, ETL 파이프라인, 데이터 마트가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DW ETL 파이프라인 5단계**: 원천 데이터 추출 $\to$ 스테이징 품질 정제 $\to$ Fact/Dim 적재 $\to$ 마트 집계 $\to$ BI 대시보드 서빙.

</details>

```text
운영계 OLTP 원천 시스템 데이터 발생
        │
   1. [데이터 추출] Debezium CDC 또는 배치 스케줄러를 통해 변경 로그 추출 (Staging)
        │
   2. [품질 정제] 전사 공통 코드 표준화, 결측치 보정, 중복 제거 및 데이터 클렌징
        │
   3. [Fact/Dim 적재] 정해진 Grain 입도와 SCD Type 2 정책에 따라 사실/차원 테이블 적재
        │
   4. [데이터 마트 롤업] 마케팅, 재무 등 주제별 Data Mart 및 사전 집계(Aggregation) 뷰 생성
        │
   5. Tableau, PowerBI, SQL 클라이언트를 통해 경영진과 분석가에게 다차원 리포트 서빙
```

#### 한줄 요약
- 데이터 추출 → 품질 정제 → Fact/Dim 적재 → 마트 집계 → BI 서빙 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Star Schema vs Snowflake Schema**: 차원 테이블을 비정규화한 스타 스키마와 차원 테이블을 3NF로 정규화한 스노우플레이크 스키마.

</details>

| 비교 항목 | 스타 스키마 (Star Schema) | 스노우플레이크 스키마 (Snowflake Schema) |
|:---|:---|:---|
| 차원 테이블 구조 | **비정규화 구조 (중복 허용, 단순성)** | **3NF 정규화 구조 (중복 제거, 다단계 분할)**|
| 조인 연산 복잡도 | **1단계 Direct 조인 (Fact-Dimension)** | **다단계 계층 조인 (Fact-Dim-SubDim)** |
| 쿼리 성능 및 속도 | **매우 빠름 (OLAP 최적화)** | 다소 느림 (다단계 조인 오버헤드) |
| 저장 공간 효율 | 차원 테이블 중복으로 일부 용량 낭비 | 저장 공간 절약 및 차원 무결성 보존 |

#### 한줄 요약
- 조회 속도와 단순성이 최우선이면 스타 스키마, 저장 공간 절약과 정규화가 목적이면 스노우플레이크를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Columnar Storage**: 디스크 블록에 데이터를 행 단위가 아닌 컬럼 단위로 저장하여 특정 컬럼 집계 쿼리 시 디스크 I/O를 90% 이상 절감하는 포맷.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수억 건 Fact 테이블 풀 스캔으로 인한 쿼리 타임아웃 | **날짜 기반 파티셔닝(Partition Key) 및 Columnar Parquet 포맷 적용** | 스캔 데이터량 90% 이상 절감 |
| 차원 속성 갱신 시 과거 분석 수치가 변조되는 왜곡 현상 | **SCD Type 2(신규 레코드 추가 + 유효기간 컬럼 부여) 이력 관리** | 과거 시점의 정확한 분석 일관성 보존 |
| 전사 공통 지표 정의 불일치로 인한 부서 간 수치 왜곡 | **시맨틱 레이어(Semantic Layer / Metric Layer) 표준화 거버넌스 수립** | 단일 진실 공급원(SSOT) 확립 |
| 일일 배치 지연으로 인한 오전 보고서 미반영 | **ELT 전환(dbt 활용) 및 클라우드 DW 가상 웨어하우스 오토스케일링** | 배치 소요 시간 70% 단축 |

#### 한줄 요약
- 열 지향 포맷, SCD Type 2 이력 관리, 시맨틱 레이어 표준화, ELT 전환으로 운영한다.

## Ⅶ. 결론

- 엔터프라이즈 데이터 기반 의사결정을 지원하기 위해 **주제 지향성과 시계열성을 보장하는 스타 스키마 기반 차원 모델링을 표준 채택**하고, **클라우드 DW(Snowflake, BigQuery)와 dbt ELT 파이프라인**을 결합하여 고성능 단일 진실 공급원(SSOT) 완성

#### 한줄 요약
- 데이터 웨어하우스는 4대 특성과 차원 모델링을 기반으로 전사 비즈니스 의사결정을 가속하는 핵심 분석 데이터 인프라다.