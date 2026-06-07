---
title: "dbt Data Transformation Modeling Testing"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: dbt(Data Build Tool)는 SQL 기반의 ELT 패러다임에서 `SELECT` 문만으로 클라우드 데이터 웨어하우스 내 변환 로직을 모델링하고, Jinja2 템플릿·Ref 함수·Materialization·Schema Test·Docs 블록을 통해 소프트웨어 엔지니어링 원칙(DRY, 모듈화, 버전관리, CI/CD)을 데이터 파이프라인에 적용하는 Transformation-as-Code 프레임워크이다.
> 2. **가치**: 수동 ETL 작성 대비 모델 재사용성 70%^, 스키마 변경 추적·리니지 자동화로 데이터 다운타임 평균 60%v, `dbt test`/`dbt docs` 자동화로 분석가-엔지니어 간 핸드오프 비용 절감 및 데이터 신뢰도(Quality) 측정 가능.
> 3. **판단 포인트**: View/Table/Incremental/Ephemeral 4종 Materialization 선택 시 트레이드오프(저장·비용·신선도), 테스트 4종 기본제 vs Singular Test 작성 비중, `sources`를 통한 Raw 데이터 계약(Contract) 정의, 멀티 프로젝트 모노레포 vs 폴리레포 운영 전략, 카탈로그(Snowflake/BigQuery/Redshift/Databricks)별 한계 식별.

---

## Ⅰ. 개요 및 필요성

전통적 ETL 파이프라인은 Informatica, Talend 같은 GUI 기반 도구로 추출·변환·적재 로직을 블랙박스 형태로 관리했다. 이는 ① 변환 로직 추적 불가 ② 비즈니스 로직과 데이터 모델 간 분절 ③ 레거시 의존성 ④ 테스트 부재로 인한 데이터 신뢰성 저하 문제를 야기했다. Snowflake·BigQuery·Redshift 같은 클라우드 DWH의 컴퓨팅-스토리지 분리 구조가 보편화되면서, **"Warehouse 내 In-Place Transformation"** 개념이 등장했고, dbt가 이를 SQL-first로 실현했다.

dbt는 dbt Labs(Fishtown Analytics)에서 2016년 출시되었으며, 2024년 기준 30,000+ 기업이 도입했고, Analytics Engineer라는 직무를 만들어낸 기술로 평가된다. 핵심 가치는 **"Analytics as Code"** — SQL+Jinja+YAML을 Git으로 버전관리하고, DAG(Directed Acyclic Graph) 기반 의존성 자동 해석, 테스트 자동화, 자동 문서화를 제공한다.

```text
+---------------------------------------------------------------------+
|            전통 ETL vs dbt 기반 ELT 패러다임 비교                    |
+---------------------------------------------------------------------+
|                                                                     |
|  [Legacy ETL]              [Modern ELT + dbt]                       |
|                                                                     |
|  Source ---> [Informatica] ---> [Staging DB] ---> [DW]                |
|             (ETL Server)     (전용 DB)                              |
|             (비-버전관리)      (중간 적재)                          |
|                  |                |                                |
|                  v                v                                |
|             Black Box         Black Box                            |
|                                                                     |
|  ---------------------------------------------------------         |
|                                                                     |
|  Source ---> [Cloud DWH(Snowflake/BQ/Redshift)] <--- dbt run        |
|   Raw       |         |         |         |         |              |
|   Tables    v         v         v         v         v              |
|          staging  intermediate  marts  snapshots  seeds            |
|          (.sql)   (.sql)      (.sql)   (SCD)     (.csv)           |
|                          |                                        |
|                          v                                        |
|                    dbt test (스키마·데이터)                         |
|                    dbt docs (자동 문서·리니지)                      |
+---------------------------------------------------------------------+
```

기존에는 분석가가 SQL을 작성하면 데이터 엔지니어가 이를 Airflow/Spark 작업으로 wrap-up했다. dbt는 이 간극을 메워 분석가가 직접 `model.sql`을 작성하고, 데이터 엔지니어는 인프라·오케스트레이션·CI/CD에 집중하게 만드는 **책임 분리(SoR, Separation of Responsibility)** 모델을 제시한다.

- **📢 섹션 요약 비유**: dbt는 데이터 웨어하우스 안의 **"변환 전용 공장 컨베이어 벨트"**로, 원자재(Raw Data)를 받아 가공 매뉴얼(SQL)대로 제품을 만들고, 자동 검사장치(Test)와 제품 카탈로그(Docs)를 함께 출력합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

dbt의 아키텍처는 4계층으로 구성된다: **① 프로젝트 구조(파일시스템) ② 컴파일러(Jinja+SQL) ③ 어댑터(어댑터 플러그인) ④ 오케스트레이션 레이어(dbt Cloud/Airflow/Prefect)**.

핵심 메커니즘은 `ref()` 함수를 통한 **DAG 자동 구성**이다. `&#123;&#123; ref('stg_orders') }}`는 컴파일 시 CTE(Common Table Expression) 형태의 의존성 그래프 노드로 해석되며, dbt는 이를 topological sort하여 실행 순서를 결정한다. 또한 `source()` 함수는 Raw 데이터에 대한 **계약(Contract)**을 정의하여, 업스트림 변경 시 다운스트림 모델을 보호한다.

```text
+----------------------------------------------------------------------+
|                  dbt 프로젝트 아키텍처 및 실행 흐름                  |
+----------------------------------------------------------------------+
|                                                                      |
|  📂 프로젝트 구조 (dbt_project.yml 루트)                              |
|  +----------------------------------------------------+             |
|  | models/         staging/   intermediate/   marts/  |             |
|  |   stg_orders.sql     +--- fct_orders.sql          |             |
|  |   stg_customers.sql  +--- dim_customers.sql       |             |
|  | tests/         (schema.yml / singular .sql)       |             |
|  | macros/        (재사용 가능한 Jinja 매크로)        |             |
|  | snapshots/     (SCD Type 2)                        |             |
|  | seeds/         (소규모 참조 데이터 .csv)           |             |
|  | analyses/      (임시 Ad-hoc 쿼리)                  |             |
|  +----------------------------------------------------+             |
|                          |                                           |
|                          v  dbt parse / compile                     |
|  +----------------------------------------------------+             |
|  |  Jinja2 템플릿 엔진 ---> SQL 변환 (CTE 생성)        |             |
|  |  ref('model')    ---> {{ database }}.{{ schema }}  |             |
|  |                       .{{ identifier }}            |             |
|  |  source('raw', 'orders') ---> raw.orders             |             |
|  |  var('start_date')        ---> '2024-01-01'         |             |
|  |  config(materialized='incremental')                |             |
|  |           |                                        |             |
|  |           v                                        |             |
|  |  +------------------------------------+           |             |
|  |  |   DAG(Directed Acyclic Graph)      |           |             |
|  |  |   sources -> staging -> intermediate  |           |             |
|  |  |             -> marts -> exposures     |           |             |
|  |  +------------------------------------+           |             |
|  |           |                                        |             |
|  |           v                                        |             |
|  |  어댑터 (dbt-snowflake, dbt-bigquery,              |             |
|  |          dbt-redshift, dbt-databricks,              |             |
|  |          dbt-postgres, dbt-spark)                  |             |
|  |           |                                        |             |
|  |           v                                        |             |
|  |  Warehouse DML/DDL 실행 (CREATE/INSERT/MERGE)      |             |
|  +----------------------------------------------------+             |
|                          |                                           |
|                          v                                           |
|  +----------------------------------------------------+             |
|  |  검증 레이어:                                       |             |
|  |   ✅ dbt test    (스키마 4종 + Singular)             |             |
|  |   📚 dbt docs    (카탈로그·리니지·컬럼 단위)         |             |
|  |   🔍 dbt source freshness (신선도 SLA)              |             |
|  |   📊 dbt-expectations, dbt-utils (패키지)           |             |
|  +----------------------------------------------------+             |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **dbt Project** | 변환 로직 컨테이너 | `dbt_project.yml`로 모델 경로·Materialization 기본값·변수 정의. `name`, `version`, `profile`, `model-paths`, `seed-paths`, `test-paths`, `macro-paths` 등 |
| **Models (.sql)** | 변환 단위 SQL 파일 | `&#123;&#123; config(materialized='incremental', unique_key='order_id', on_schema_change='append_new_columns') }}` 메타데이터. `SELECT`문만 작성 (CREATE TABLE 등은 dbt가 생성) |
| **Schema YAML (sources/tests/docs)** | 데이터 계약·테스트·문서 | `sources:` (raw 테이블 정의+신선도), `models:` (description, columns, tests, meta), `exposures:` (BI 대시보드 의존성) |
| **Macros** | Jinja2 기반 재사용 함수 | `{% macro cents_to_dollars(column_name) %} {{ column_name }}/100.0 {% endmacro %}` 패턴. `dbt_utils` 같은 패키지로 생태계 확장 |
| **Tests** | 데이터 품질 검증 | ① 내장: `unique`, `not_null`, `accepted_values`, `relationships` ② Singular: `tests/assert_positive_revenue.sql` (Boolean 결과 반환) ③ Generic: 패키지 형태의 재사용 가능 테스트 |
| **Snapshots** | SCD Type 2 구현 | `dbt snapshot`으로 slowly changing dimension 추적. `strategy: timestamp` vs `check` 컬럼 비교, `unique_key`로 멱등성 보장 |
| **Seeds** | CSV 참조 데이터 적재 | `dbt seed`로 소규모(<수만 행) 정적 데이터 적재. 국가코드, 우편번호 매핑 등 |
| **Adapter Layer** | DWH 종속성 추상화 | `dbt-snowflake`, `dbt-bigquery`, `dbt-redshift`, `dbt-databricks`, `dbt-postgres` 등 12+ 어댑터. Database/Schema 매핑, Incremental merge 전략 차별화 |
| **Artifacts (run_results.json, manifest.json)** | 메타데이터 산출물 | DAG 노드 ID, 의존성 그래프, 실행 로그. 외부 도구(Elementary, Re_data, dbt-monitor)가 이를 소비해 모니터링·경보 |

핵심 파라미터/알고리즘:

- **Incremental 전략**: `append` (중복 허용), `merge` (unique_key 기반 UPSERT, `dbt-1.0+`에서 기본), `delete+insert`, `insert_overwrite`(파티션 기반). BigQuery는 `merge`를 `MERGE STATEMENT`로, Snowflake는 `MERGE INTO`로 변환.
- **Ref 해석 알고리즘**: `ref()` 함수 호출 시 manifest.json에 노드 등록 -> DAG 정렬 시 Kahn's Algorithm 위상 정렬 -> 의존 모델 우선 컴파일·실행.
- **Schema Test 컴파일**: `unique` -> `SELECT col FROM (SELECT col, COUNT(*) OVER (PARTITION BY col) cnt FROM tbl) WHERE cnt > 1` 형태로 변환, 실패 시 `dbt test --store-failures` 옵션으로 결과 테이블 적재.
- **dbt parse 시간**: 프로젝트 1000+ 모델 기준 평균 30~90초. `--no-partial-parse`로 캐시 무효화.

- **📢 섹션 요약 비유**: dbt는 **"SQL로 만드는 레고 블록"**과 같습니다. 작은 블록(Model)을 Ref로 연결해 큰 조형물(Marts)을 짓고, 매 블록마다 자동 검사(Test)를 통과해야만 다음 단계로 넘어갈 수 있습니다.

---

## Ⅲ. 비교 및 연결

dbt는 데이터 변환 영역의 사실상 표준(de facto)이지만, Apache Airflow, Dataform, SQLMesh, Coalesce 같은 경쟁 도구와 비교 시 차별점이 분명하다. 또한 Great Expectations, Soda Core 같은 데이터 품질 도구, Atlan·DataHub 같은 카탈로그 도구, Monte Carlo·Bigeye 같은 observability 도구와 보완 관계에 있다.

| 구분 | **dbt** | **Apache Airflow** | **Dataform (Google)** | **SQLMesh** | **Great Expectations** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | SQL 변환+테스트+문서 | 워크플로우 오케스트레이션 | SQL 변환 (dbt와 유사) | SQL 변환+가상환경 | 데이터 품질 검증 |
| **언어** | SQL + Jinja | Python (DAG 정의) | SQL + JavaScript | SQL + Python | Python/YAML |
| **테스트** | 내장 4종 + 사용자 정의 | 별도 구현 필요 | assertions 블록 | 내장 + audit | 강력한 Expectation 시스템 |
| **리니지** | 자동 (manifest.json) | OpenLineage 통합 | 자동 (Dataform Web) | 자동 (UI 내장) | 미제공 |
| **환경 격리** | dbt Cloud only (Dev/Prod) | Celery/K8s Executor | Git 통합 | 내장 (Dev/Prod 가상 환경) | 별도 |
| **상태(state) 관리** | Weak (스키마 기반) | Weak | Weak | **Strong (snapshot 기반 변경 감지)** | Weak |
| **실행 단위** | Model (DAG 노드) | Task | Table | Model | Checkpoint |
| **커뮤니티** | 매우 활발 (dbt Slack 80K+) | 매우 활발 | 활발 | 성장 중 | 활발 |
| **라이선스** | Core: Apache 2.0 / Cloud: 상용 | Apache 2.0 | 상용 (Google) | Apache 2.0 | Apache 2.0 |
| **DWH 의존성** | 어댑터 12+ | 없음 (범용) | BigQuery 우선 | 어댑터 7+ | 없음 (범용) |
| **학습 곡선** | 낮음 (SQL만 알면 됨) | 중간 (Python+DAG) | 낮음 | 중간 | 높음 (Python) |

**연계 통합 패턴:**

- **dbt + Airflow**: Airflow의 `DbtRunOperationOperator`/`DbtRunOperator`로 dbt Cloud API 호출 또는 `BashOperator`로 `dbt-core` CLI 실행. Airflow는 외부 시스템(API, S3) -> Warehouse 적재(EL의 L) 담당, dbt는 T 담당.
- **dbt + Great Expectations/Soda Core**: `dbt-expectations` 패키지(Great Expectations의 GE Expectation을 dbt 테스트로 래핑) 또는 Soda의 `soda scan`을 `dbt run` 후 CI 단계에서 실행. 이 경우 품질 검증의 단일 진실 공급원은 dbt로 통합.
- **dbt + DataHub/Atlan**: `dbt-artifacts` 또는 `dbt_manifest_parser`로 manifest.json을 카탈로그에 push, column-level 리니지 시각화.
- **dbt + Elementary**: `dbt run` 후 `elementary` 패키지가 anomaly detection, freshness, volume 추적.
- **dbt + dbt-mesh/Cross-project ref**: `dbt-project-dependencies`로 멀티팀 모노레포 운영. 동일 카탈로그 내 다른 프로젝트의 모델 참조 가능 (`+group:finance`).

- **📢 섹션 요약 비유**: Airflow가 **"전체 공장 스케줄러"**라면, dbt는 **"변환 라인 전용 작업 매뉴얼"**입니다. 두 도구를 합치면 L(적재)은 Airflow가, T(변환)는 dbt가 각자 전문 영역을 담당합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **Materialization 전략 수립**: `staging` 레이어는 `view`(저장비용 0,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 288 / 300

<- **이전**: [287. 데이터 오케스트레이션 Airflow DAG 워크플로 (Data Orchestration Airflow DAG Workflow)](/studynote/14_data_engineering/05_exam_keywords/287_data_orchestration_airflow/)
**다음**: [289. 스키마 진화 호환성 레지스트리 관리 (Schema Evolution Compatibility Registry)](/studynote/14_data_engineering/05_exam_keywords/289_schema_evolution/) ->

---
