---
sidebar:
  order: 138
  label: "138. ETL•ELT 파이프라인 (ETL ELT Pipeline)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "ETL•ELT 파이프라인 (ETL ELT Pipeline)"
date: "2026-08-14T00:44:00+09:00"
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

- **ETL (Extract, Transform, Load)**: 소스 DB에서 데이터를 추출(Extract)하여 별도의 중간 변환 서버(Spark/ETL Tool)에서 정제/변환(Transform)을 모두 마친 후, 타깃 DW/DB에 적재(Load)하는 전통적 파이프라인.
- **ELT (Extract, Load, Transform)**: 소스 DB의 날것 그대로 데이터(Raw Data)를 타깃 데이터 레이크/DW(S3, Snowflake)에 일단 우선 적재(Load)한 후, 타깃 엔진의 초고속 컴퓨팅 파워로 내부 변환(Transform)을 수행하는 모던 파이프라인.
- **dbt (data build tool)**: ELT 파이프라인에서 SQL 기반으로 타깃 DW 내부 변환 로직(Transform)을 모듈화하고 테스팅하는 대표 오픈소스 툴.

</details>

- 정의/개념: 변환과 적재 순서를 달리하는 **ETL**•**ELT**
- 배경/필요성: 보안 선처리와 원본 재가공은 **변환 위치•시점** 요구 상충

#### 한줄 요약

- 자료를 밖에서 정리해 넣는 ETL과 먼저 넣고 안에서 정리하는 ELT이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Compute Layer Offloading**: ETL은 중간 서버 컴퓨터가 변환 연산 부담, ELT는 타깃 클라우드 DW(Snowflake, BigQuery)가 변환 연산 부담.
- **Data Preservation (원본 보존성)**: ELT는 Raw 데이터가 타깃 S3에 100% 보존되어 언제든 재가공 가능.

</details>

- **ETL (Transform Pre-Load: 보안/PII 선 마스킹 및 레거시 DW에 적합)**
- **ELT (Transform Post-Load: Raw 보존, 클라우드 레이크하우스 & dbt 연동에 적합)**
- **Pipeline Latency & Scalability Tradeoff (적재 속도 및 확장성 트레이드오프)** #### 한줄 요약

- 어디까지 성공했는지 기억하고 같은 구간을 다시 넣어도 결과가 한 번만 남게 만든다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Transformation Offloading Layer**: ETL의 경우 Spark/Informatica 서버, ELT의 경우 Snowflake/BigQuery/dbt internal SQL 연산.

</details>

| 구성요소 | 책임 |
|:---|:---|
| Extractor | 원천 변경•배치 데이터를 증분 추출 |
| Transformer | 정제•표준화•마스킹•업무 규칙 적용 |
| Loader | 스테이징•타깃에 멱등 적재 |
| Orchestrator | 의존성•재시도•체크포인트 관리 |
| Quality•Lineage | 계약 검사와 입력•출력 증거 기록 |

#### 한줄 요약

- 밖에서 정리해 넣거나 먼저 넣고 안에서 정리한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **dbt Transformation Flow**: S3/Snowflake에 덤프된 Bronze Raw 테이블을 dbt SQL 모델로 가공하여 Silver/Gold 테이블로 승격시키는 ELT 변환 과정.

</details>

```text
[원천 변경]
      │
      ▼
1. 증분 추출
      │
      ▼
2. 체크포인트 기록
      │
      ▼
3. 변환•적재 실행
      │
      ▼
4. 품질•멱등 검증
      │
      ▼
5. 결과 공개•위치 확정
```

### 동작 원리

1. 증분 추출: 로그 위치•수정 시각으로 신규 범위 수집
2. 체크포인트 기록: 재시작 가능한 원천 위치 저장
3. 변환•적재 실행: ETL은 변환 선행, ELT는 적재 선행
4. 품질•멱등 검증: 계약•중복•행 수•합계 대조
5. 결과 공개•위치 확정: 성공 후 타깃과 체크포인트 전환

#### 한줄 요약

- 새 자료를 따로 보관하고 선택한 순서로 처리한 뒤 결과가 맞아야 완료 표시를 옮긴다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Domain Selection Criteria**: 보안/PII 민감 데이터는 ETL, 대용량 빅데이터 및 실시간 머신러닝은 ELT.

</details>

| 선택 요구사항 | ETL (Extract-Transform-Load) | ELT (Extract-Load-Transform) |
|:---|:---|:---|
| 보안 및 규제  | **적재 전 PII 암호화 필수 시 (ETL 우수)** | 타깃 저장소 보안 정책으로 커버 |
| 데이터 스토리지 비용 | 온프레미스 디스크가 비싼 경우 | **클라우드 S3 스토리지 가격이 매우 저렴한 경우** |
| 유연성 및 재가공 | 중간 원본 보존 정책에 좌우 | **Raw 보존 시 타깃에서 재가공** |
| 엔지니어링 기술 | Spark, Scala 전문 엔지니어 필요 | **SQL 숙련 데이터 분석가도 파이프라인 개발** |

#### 한줄 요약

- 밖에서 가려야 할 값은 먼저 처리하고 반복 분석할 원본은 안에 보관해 다시 가공할 수 있다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Snowflake Compute Credit Explosion**: ELT 변환 쿼리가 비효율적일 경우 타깃 클라우드 DW의 컴퓨팅 노드 사용료(Credit) 폭증 위험.

</details>

| 3대 ELT 구축 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Target DW Cost Surge | ELT dbt 변환 SQL 과다 실행으로 쿼리 비용 폭발| **`dbt incremental` 모델로 변환 쿼리 증분화** |
| 2. PII Data Exposure | PII 생값이 S3/DW Raw 영역에 그대로 노출 | **Ingestion 커넥터 단에서 PII Hash 단방향 암호화**|
| 3. Raw Data Swamp | ELT Raw 지대에 자잘한 쓰레기 파일 폭발 | **Lifecycle Policy 적용하여 90일 후 Cold Storage**|

> 사례: **카카오 / 당근마켓 / 쿠팡 Fivetran + Snowflake + dbt 기반 Modern Data Stack ELT 운용** #### 한줄 요약

- 급여의 주민번호는 적재 전에 마스킹하고 분석에 필요한 나머지는 원본으로 보관한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **ELT 수립 기준(Modern Data Stack Standards)**: Cloud DW, S3 Raw Preserved, dbt SQL Transformation 및 Airflow Orchestration에 의거한 체계.

</details>

- 적재 전 통제가 필수면 **ETL**, 원본 재가공이 중요하면 ELT 선택

#### 한줄 요약

- 먼저 가려야 하면 ETL, 먼저 보관해 여러 번 가공해야 하면 ELT가 기본 선택이다.
