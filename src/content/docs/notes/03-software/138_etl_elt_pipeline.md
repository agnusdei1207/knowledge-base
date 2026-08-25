---
sidebar:
  order: 138
  label: "138. ETL•ELT 파이프라인"
  badge:
    text: "미출 · 50%"
    variant: note
title: "ETL•ELT 파이프라인 (ETL ELT Pipeline)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 138
extra:
  question_no: "138"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "ETL•ELT 선택은 처리 위치•비용 절충"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ETL vs ELT**: 중간 서버에서 변환 후 적재하는 전통적 방식(ETL)과 타깃 저장소에 원본을 먼저 적재한 후 클라우드 DW 엔진으로 변환하는 현대적 방식(ELT).
- **dbt(data build tool)**: ELT 파이프라인에서 SQL 기반으로 타깃 DW 내부의 데이터 변환(Transform)을 모듈화하고 테스트하는 프레임워크.

</details>

- 정의/개념: 데이터 파이프라인에서 추출(Extract), 변환(Transform), 적재(Load)의 **실행 순서와 연산 위치를 인프라 및 보안 요구에 맞추어 최적화하는 처리 방식**
- 배경/필요성: 클라우드 환경에서 과거 ETL 방식 고수 시 발생하는 **타깃 DW 컴퓨팅 파워 미활용, 사전 변환 병목 및 원천 데이터 재가공 불가 해결 불가**

#### 한줄 요약
- 보안 통제가 우선이면 ETL, 원본 보존과 고속 변환이 우선이면 ELT를 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Compute Offloading**: ETL은 별도 전용 변환 서버(Spark)가 연산 부하를 담당하고, ELT는 타깃 클라우드 DW(Snowflake, BigQuery)의 분산 엔진이 연산 담당.
- **Raw Data Preservation**: ELT는 원시(Raw) 데이터를 레이크/DW에 100% 보존하므로 요구사항 변경 시 언제든 재가공 가능.

</details>

- 적재 전 PII 민감정보를 완벽히 마스킹하는 **보안 중심 사전 변환(ETL)**
- 원시 데이터를 보존하고 클라우드 DW 엔진으로 고속 가공하는 **확장 중심 사후 변환(ELT)**
- dbt 및 SQL 기반으로 비즈니스 분석가가 직접 변환 로직을 작성하는 **모던 데이터 스택 연동**

#### 한줄 요약
- 사전 변환(ETL)의 보안성과 사후 변환(ELT)의 유연성·확장성을 상호 절충한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **파이프라인 5대 컴포넌트**: Extractor(추출기), Transformer(변환기), Loader(적재기), Orchestrator(스케줄러), Quality Validator(검증기).

</details>

```text
[ETL vs ELT 데이터 파이프라인 아키텍처 비교]
|-- 1. ETL 파이프라인 (Extract -> Transform -> Load)
|   `-- Source DB ──(추출)──► [Spark/ETL 서버 (변환/마스킹)] ──(적재)──► Target DW
|-- 2. ELT 파이프라인 (Extract -> Load -> Transform)
|   `-- Source DB ──(추출)──► [Target Lakehouse/S3 (Raw 적재)] ──(dbt SQL 변환)──► Gold Mart
`-- 3. Orchestration & Governance Layer (Apache Airflow / Dagster + OpenLineage)
```

선의 의미: 계층 및 ETL(중간 서버 변환)과 ELT(타깃 스토리지 내 변환)의 데이터 흐름 차이 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **추출기 (Extractor)** | 원천 시스템으로부터 CDC 또는 배치 쿼리를 통해 **데이터를 안전하게 증분 추출** | Fivetran, Airbyte |
| **변환기 (Transformer)** | 정제, 결측치 보정, 공통 코드 매핑, **비즈니스 파생 컬럼 연산 수행** | Spark(ETL), dbt(ELT) |
| **적재기 (Loader)** | 가공된 데이터 또는 원시 데이터를 **타깃 레이크/DW에 멱등(Idempotent) 적재** | Parquet / Iceberg |
| **오케스트레이터** | 작업 간의 의존성(DAG) 관리, 스케줄링, **장애 시 자동 재시도 통제** | Airflow, Prefect |
| **품질/계보 검증기** | 데이터 계약(Contract) 준수 여부를 검증하고 **상하류 계보 메타데이터 기록** | Great Expectations |

#### 한줄 요약
- 추출기, 변환기, 적재기, 오케스트레이터, 품질 검증기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ELT dbt 변환 파이프라인**: Raw Ingestion $\to$ Bronze S3 적재 $\to$ dbt SQL 모델링 $\to$ Silver/Gold 구체화 $\to$ BI 서빙.

</details>

```text
원천 시스템 데이터 변경 발생
        │
   1. [증분 추출] Airbyte 커넥터가 원천 DB 변경분을 JSON/Parquet으로 추출
        │
   2. [Raw 우선 적재] 변환 없이 타깃 클라우드 S3 / Snowflake Bronze 영역에 즉시 Load
        │
   3. [dbt SQL 변환] 타깃 DW의 분산 컴퓨팅 파워를 활용하여 SQL 기반 모델 변환 실행
        │
   4. [품질 및 멱등 검증] dbt test를 통해 고유성, Not Null, 외래키 무결성 자동 검사
        │
   5. 검증 완료된 결과를 Silver/Gold 테이블로 승격하고 BI 대시보드에 즉시 서빙
```

#### 한줄 요약
- 증분 추출 → Raw 우선 적재 → dbt SQL 변환 → 품질 검증 → Gold 마트 서빙 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ETL vs ELT 비교**: 중간 서버 변환(ETL)과 타깃 저장소 내부 변환(ELT).

</details>

| 비교 항목 | ETL (Extract-Transform-Load) | ELT (Extract-Load-Transform) |
|:---|:---|:---|
| 변환 연산 위치 | **별도 독립 변환 서버 (Spark, ETL 툴)** | **타깃 클라우드 DW / Lakehouse 내부 엔진** |
| 원시 데이터 보존 | 타깃에 정제 결과만 적재 (재가공 제한) | **Raw 데이터가 타깃에 100% 영구 보존** |
| 데이터 적재 속도 | 변환 완료 후 적재하므로 상대적 지연 | **원시 데이터를 즉시 적재하므로 매우 빠름** |
| 최적 적용 환경 | **금융/공공 엄격한 PII 사전 비식별화 필수 환경**| **대규모 빅데이터, AI/ML 학습, 클라우드 DW 환경**|

#### 한줄 요약
- 사전 보안 마스킹은 ETL, 대규모 확장성과 유연한 재가공은 ELT를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Compute Credit Surge**: ELT 환경에서 비효율적인 SQL 쿼리가 반복 실행될 경우 클라우드 DW의 컴퓨팅 비용이 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ELT dbt 변환 쿼리 과다 실행으로 클라우드 DW 비용 폭증 | **`dbt incremental` 모델 적용하여 변경 증분 데이터만 가공** | 쿼리 컴퓨팅 비용 70% 절감 |
| 원본 개인정보(PII)가 Raw S3 영역에 평문으로 노출 | **수집(Ingestion) 커넥터 단에서 SHA-256 단방향 해시 마스킹** | 컴플라이언스 및 개인정보 보호 |
| ELT Raw 지대에 자잘한 쓰레기 파일 누적으로 인한 늪화 | **S3 Lifecycle 정책 적용하여 90일 경과 파일 Glacier 이전** | 스토리지 비용 최적화 |
| 파이프라인 실패 시 중간 데이터 중복 적재 | **Target 테이블에 `MERGE INTO` 기반 멱등 쓰기 강제** | 중복 데이터 왜곡 원천 차단 |

#### 한줄 요약
- dbt 증분 모델, 수집 단 PII 마스킹, S3 수명주기 관리, MERGE 멱등 쓰기로 운영한다.

## Ⅶ. 결론

- 엔터프라이즈 데이터 플랫폼 구축 시 **보안 민감 데이터는 ETL 기반으로 사전 마스킹하고, 대규모 분석 및 AI 데이터는 ELT(Fivetran + Snowflake + dbt) 기반으로 구축하는 하이브리드 파이프라인 전략**을 수립하여 처리 속도와 보안성을 동시에 완성

#### 한줄 요약
- ETL과 ELT는 변환의 위치와 순서를 최적화하여 데이터 파이프라인의 보안성과 확장성을 결정짓는 핵심 엔지니어링 아키텍처다.