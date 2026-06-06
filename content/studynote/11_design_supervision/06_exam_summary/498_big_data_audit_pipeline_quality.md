---
title: "Big Data Audit Pipeline Quality"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 빅데이터 감리 파이프라인 품질 검증은 데이터의 6V(Volume·Velocity·Variety·Veracity·Value·Variability) 특성을 고려하여 **Ingestion -> Transformation -> Storage -> Serving 4단계 전 구간**에 데이터 품질 차원(Accuracy·Completeness·Consistency·Timeliness·Validity·Uniqueness)을 자동화된 메트릭·계약·계보(Lineage)·이상탐지로 연속 검증하는 거버넌스 체계이다.
> 2. **가치**: 결측률 1% 이내·스키마 드리프트 0건·SLA 지연 5분 이내를 KPI로 설정할 경우, 데이터 신뢰성 사고를 **평균 73% 감소**(Monte Carlo 2024 State of Data Quality 기준)시키고, 감리 지적 사항 중 데이터 관련 항목(M2~M4 결함)을 **0건**으로 만들 수 있다.
> 3. **판단 포인트**: 배치/스트림/하이브리드 파이프라인별 검증 임계치, **푸시다운 검증(Pushdown Validation, Spark SQL·Deequ·DPP) vs 풀패스 검증(Full-Pass, Great Expectations)**, 메타데이터·계약·관측(Observability) 3축 비중, 그리고 감리 기준(한국데이터진흥원 데이터품질진단 가이드라인 v3.0, 행정안전부 데이터 품질관리 매뉴얼) 준수 여부가 기술사 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

빅데이터 시스템 감리는 행정안전부 「정보시스템 감리 기준」(2023 개정) 및 한국데이터진흥원 「빅데이터 품질관리 가이드라인」에 따라 **데이터 기반 의사결정의 신뢰성을 객관적으로 입증**하기 위한 절차이다. 전통적인 SI 감리는 트랜잭션 무결성·처리량·보안 통제에 집중했으나, 빅데이터 환경에서는 ① 비정형·반정형·정형의 혼재, ② 일배치/실시간/증분 처리의 동시 운영, ③ 스키마리스·Schema-on-Read, ④ 다중 다운스트림 컨슈머(BI, ML, API) 로 인해 **파이프라인 내부에서 발생하는 품질 열화가 최종 산출물까지 전파**되는 구조적 문제가 발생한다.

특히 공공·금융·의료 빅데이터는 **개인정보보호법 §28의2(가명정보), 데이터 산업법 §23(데이터 품질 인증)**과 직결되므로, 감리원이 1차·2차 산출물(원천데이터, 전처리데이터, 분석데이터, 서비스데이터)의 품질 메트릭을 실시간으로 확인할 수 있는 **자동화된 검증 파이프라인**이 필수적이다.

```text
+------------------------------------------------------------------------+
|            빅데이터 감리 품질 검증 4-Stage End-to-End Pipeline          |
+------------------------------------------------------------------------+
  [원천시스템]      [수집 Ingest]      [처리 Processing]    [저장 Storage]   [서비스 Serving]
  +----------+      +----------+      +--------------+     +----------+    +----------+
  | RDBMS    |      |  Kafka   |      | Spark/Flink  |     | HDFS     |    | BI/ML    |
  | NoSQL    | ---► | Nifi     | ---► | Hive/Spark   | --► | Iceberg  | --► | API/CSV  |
  | Files/IoT|      | Pulsar   |      | Trino        |     | Delta    |    | Dashboard|
  | API/CDC  |      | Sqoop    |      | dbt SQL      |     | BigQuery |    | Serving  |
  +----+-----+      +----+-----+      +------+-------+     +----+-----+    +----+-----+
       | Quality Gate v  | Quality Gate v   | Quality Gate v | Quality Gate v| Quality Gate v
  +----+----------------+-------------------+----------------+---------------+----------+
  |  [P0] 메타·계약·계보·관측 4축 통합 품질 검증 계층 (Data Quality Control Plane)         |
  |  • Schema Registry  • DQ Rules  • Lineage Atlas  • Anomaly Detection                |
  |  • SLA Monitoring   • PII Mask  • Statistical Profiling  • Audit Trail              |
  +--------------------------------------------------------------------------------------+
                                       |
                                       v
                            +----------------------+
                            |   감리원 검증 포털    |
                            |  (KData 품질 대시보드)|
                            |  - 결함 등급 M1~M4   |
                            |  - KPI/메트릭 리포트  |
                            |  - 증적 수집(Immutable)|
                            +----------------------+
```

**기존 SI 감리 대비 변화점**

| 구분 | 기존 정보시스템 감리 | 빅데이터 감리 |
|---|---|---|
| 데이터 특성 | 정형·정적 | 비정형·반정형·스트리밍 |
| 품질 검증 시점 | 출력 후 사후 | 수집·처리·저장·서비스 4단계 실시간 |
| 검증 도구 | SQL 단발성 체크 | 계약 기반(Contract)·메트릭·ML 이상탐지 |
| 증적 수집 | 산출물 스냅샷 | 불변 로그(Ledger) + 데이터 계보 |
| 거버넌스 표준 | ISO 25040, KS X 5700 | KData 품질관리 v3.0 + DataOps 관측성 |

- **📢 섹션 요약 비유**: 빅데이터 파이프라인을 수도관에 비유하면, 기존 SI 감리는 수도꼭지에서 물 샘플을 채수한 뒤 검사하는 방식이고, 빅데이터 감리는 수도관 입구·정수기·배수관·배출구 4곳에 **수질 센서와 자동 차단기**를 설치해 실시간으로 부유물·pH·유량을 감시하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

빅데이터 감리 파이프라인은 **Control Plane(제어평면)** + **Data Plane(데이터평면)** 으로 분리된다. Data Plane은 실제 데이터 흐름(Spark, Kafka, Iceberg 등)이고, Control Plane은 그 흐름 위에서 메타·계약·계보·관측을 통합 관리한다. 한국데이터진흥원 가이드라인은 품질 진단 항목을 **4영역 17항목**으로 분류하며, 이를 Control Plane 7-Layer로 매핑한다.

```text
+----------------------------------------------------------------------------+
|                       Control Plane 7-Layer 아키텍처                       |
+----------------------------------------------------------------------------+

  +--------------------------------------------------------------------+
  |  L7. 감리 증적 & 리포팅 (Audit & Evidence)                          |
  |      - Evidence Ledger(불변)·M1~M4 결함 분류·증적 해시 체인         |
  +--------------------------------------------------------------------+
  |  L6. SLA·관측성 (Observability & SLA)                              |
  |      - DataDog DQ·Monte Carlo·Prometheus DQ Exporter·SLO Burn      |
  +--------------------------------------------------------------------+
  |  L5. 이상탐지·ML 기반 품질 (Anomaly & ML)                          |
  |      - 통계분포 Drift(KS-test)·IsolationForest·AutoEncoder        |
  +--------------------------------------------------------------------+
  |  L4. 데이터 계보·영향도 (Lineage & Impact)                          |
  |      - Apache Atlas·DataHub·OpenLineage·Marquez·Spline            |
  +--------------------------------------------------------------------+
  |  L3. 데이터 계약 (Data Contract)                                   |
  |      - Schema Registry(Avro·Proto)·dbt tests·Great Expectations   |
  +--------------------------------------------------------------------+
  |  L2. 품질 규칙 엔진 (DQ Rules Engine)                              |
  |      - Soda Core·Deequ·Griffin·Anomalo·Talend DQ                  |
  +--------------------------------------------------------------------+
  |  L1. 메타·스키마 카탈로그 (Meta Catalog)                            |
  |      - Apache Hive Metastore·Glue Catalog·Unity·Hive Metastore    |
  +--------------------------------------------------------------------+

  -------------------- Data Plane (Spark/Flink/Kafka/Iceberg) ------------
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **L1. 메타·스키마 카탈로그** | 모든 테이블·컬럼·파티션의 메타데이터 단일 진실 원천(SSOT) | Hive Metastore, AWS Glue Data Catalog, Unity Catalog, Iceberg REST Catalog. **컬럼 단위 PII 태깅**(개인정보), 분류코드(공개/내부/기밀), SLA 등급(0–5) 부여 |
| **L2. 품질 규칙 엔진** | 룰셋 기반 일/실시간 데이터 품질 검사 | **Soda Core**: SQL DSL(`checks` YAML)·다중 데이터소스·증분 검증 / **Deequ**: Spark 기반 `Constraint` API·Null·MinLength·Correlation·Completeness·Uniqueness / **Apache Griffin**: 배치·스트림 통합, **Completeness·Accuracy·Timeliness·Consistency·Uniqueness 5차원** 매핑 |
| **L3. 데이터 계약 (Data Contract)** | 프로듀서-컨슈머 간 **스키마·SLA·품질 보증** 명세 | Avro/Protobuf **Schema Registry**(Confluent·Apicurio), **dbt tests**(`unique`, `not_null`, `relationships`, `accepted_values`, `custom`), **Great Expectations**(Expectation Suite, JSON), **Data Contract CLI**(Bitol 사양) |
| **L4. 데이터 계보 (Lineage)** | 컬럼 단위 ETL 변환 추적, 영향도 분석 | Apache Atlas(컬럼 단위 Hook), DataHub(GMS), OpenLineage(Marquez·Spline), Iceberg **metadata.json** 스냅샷 차이 분석, Airflow OpenLineage Hook |
| **L5. 이상탐지·ML 기반 품질** | 룰로 정의 어려운 통계적·의미론적 이상 탐지 | **KS-test·Chi-square** 분포 드리프트, **Isolation Forest·DBSCAN** 이상치, **AutoEncoder** 시계열, **LLM 기반** 의미론적 스키마 매칭(스타버스키마) |
| **L6. SLA·관측성** | Data SLO·Error Budget·대시보드·알림 | Monte Carlo / Soda Cloud(필드 헬스), Datafold(회귀 감지), Prometheus DQ Exporter -> Grafana, OpenTelemetry DQ Span |
| **L7. 감리 증적 & 리포팅** | 불변 증적·결함 분류·감리원 제출용 리포트 | Apache Iceberg **불변 스냅샷** + AWS QLDB·Hyperledger Fabric 증적, KData 품질 진단 4영역 17항목 매핑, 결함 등급 M1(중대)~M4(경미) 자동 분류, **증적 해시 체인**(SHA-256) 위변조 검증 |

**핵심 동작 메커니즘 — 푸시다운 검증(Pushdown) 알고리즘**

빅데이터 풀패스(Full-Pass) 스캔은 O(N) 비용으로 페타바이트급에서 비현실적이다. 따라서 다음과 같은 **푸시다운 최적화**가 필수이다.

```
DQ 검증 비용 =  α · FullScan   +  β · Pushdown   +  γ · Anomaly
             =  α · O(N)       +  β · O(파티션)   +  γ · O(sampling)
             where  α < 0.1, β > 0.7, γ ≈ 0.2 (목표 비율)
```

| 푸시다운 기법 | 적용 단계 | 원리 | 대표 구현 |
| :--- | :--- | :--- | :--- |
| **컬럼 프루닝** | Ingest | `_row_count`, `sum_hash`, `min/max` 메타만 검사 | Iceberg **파티션 통계**, Parquet footer min/max |
| **푸시다운 SQL** | Transform | Spark SQL에 DQ 규칙을 `WHERE` 절로 통합 실행 | Deequ `Analyzer` 푸시다운, Soda SQL Pushdown |
| **Bloom Filter** | Storage | 멤버십·중복 검사 O(1) | Iceberg **Bloom Filter Index**, Parquet BF |
| **Apache DPP** | Transform | Spark 3.3+ Dynamic Partition Pruning | DPP + DQ 룰 결합 |
| **샘플링** | Anomaly | Reservoir sampling 1–5% | Algebird `HyperLogLog·CountMinSketch` |
| **WASM/UDF** | Edge | IoT/엣지 노드 사전 필터링 | Wasmtime + Rust UDF |

**품질 차원의 정량적 임계치(감리 권고 표준)**

| 차원 | 정의 | 수식/측정 | 권고 임계치 (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 498 / 600

<- **이전**: [497. 블록체인 감리 스마트 계약 검증](/studynote/11_design_supervision/06_exam_summary/497_blockchain_audit_smart_contract_verifica)
**다음**: [499. ERP 감리 프로세스 적합성 평가](/studynote/11_design_supervision/06_exam_summary/499_erp_audit_process_fitness_evaluation/) ->

---
