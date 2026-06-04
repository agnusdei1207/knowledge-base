---
title: "260. 데이터 프로덕트 데이터 서비스 계약 (Data Product Data Contract SLA)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 프로덕트(Data Product)는 도메인이 소유하고 SLA/품질/스키마를 코드(ODCS, JSON Schema)로 계약을 정의한 **"주소 지정·검색 가능·거버넌스 가능한 1급 데이터 자산"**이며, 데이터 컨트랙트(Data Contract)는 프로듀서와 컨슈머 간의 **버전 관리 가능한 명세적 합의(Schema, Semantics, SLA, Policy, SLA Tier, PII)**이다.
> 2. **가치**: 컨트랙트 기반 거버넌스 도입 시 **ETL 실패율 약 60~80% 감소, 컨슈머 데이터 통합 시간 70% 단축, 데이터 인시던트 MTTR 평균 4.2시간->27분 단축, 도메인 자율성 확보**로 데이터 레이크의 "쓰레기 투입(Garbage In) 현상"을 구조적으로 차단한다.
> 3. **판단 포인트**: **Pull/Federated Compute vs Push/Replicated**의 배포 모델 선택, **Bronze/Silver/Gold 등급별 SLA(Quality 95/99/99.9%, Latency 1h/15min/1min)** 차등화, **ODCS(Open Data Contract Standard) v3.0 기반 표준화 vs 조직별 커스텀**, 그리고 **Schema Evolution 전략(Backward-compatible -> Forward-compatible)**이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적 데이터 레이크(Data Lake 1.0)는 **"Schema-on-Read"** 원칙 하에 자유로운 적재를 허용했으나, 이는 곧 **데이터 스왐프(Data Swamp)** 문제를 야기했다. 2020년 쯤 Zhamak Dehghani가 제안한 **데이터 메시(Data Mesh)** 패러다임은 데이터를 인프라 자원이 아닌 **제품(Product)**으로 간주하도록 패러다임을 전환했고, 이후 데이터 컨트랙트(Data Contract)라는 명세적 합의 메커니즘이 데이터 제품의 신뢰성을 보증하는 핵심 수단으로 자리 잡았다.

특히 Gartner는 2024년 보고서에서 **"Data Products are the unit of data monetization"**라고 명시하며, 2026년까지 분석/AI 프로젝트의 70%가 데이터 프로덕트 카탈로그를 통해 발견될 것으로 예측했다. 데이터 컨트랙트가 부재하면 다음과 같은 문제가 다발한다.

- **Silent Schema Drift**: 프로듀서가 컬럼 타입을 `STRING->BIGINT`로 변경했으나 컨슈머 파이프라인은 이를 인지하지 못해 운영 중 오류 발생
- **SLA 모호성**: "데이터가 어제 기준이다"라는 비정형적 표현으로 컨슈머가 의존성 있게 사용 불가
- **책임 경계 불분명**: 도메인 간 데이터 품질 책임 소재가 모호하여 사일로(Silo)화 심화
- **PII/규제 컴플라이언스 누락**: GDPR/개인정보보호법 적용 대상 필드가 계약서에 명시되지 않아 컴플라이언스 사고 발생

```text
+----------------------------------------------------------------------+
|              전통적 데이터 레이크 vs 데이터 메시 패러다임 비교         |
+----------------------------------------------------------------------+

[Legacy: 중앙 집중형 데이터 팀 + Schema-on-Read]
+--------------+     +--------------+     +--------------+
| Source DB 1  |     | Source DB 2  |     | SaaS API     |
| (CRM)        |     | (ERP)        |     | (Salesforce) |
+------+-------+     +------+-------+     +------+-------+
       |                    |                    |
       +------------+-------+------------+-------+
                    v                    v
         +--------------------------------------+
         |  Central Data Lake (S3/HDFS)         |
         |  - Schema-on-Read                    |
         |  - No Formal Contract                |
         |  - Unknown Quality                   |
         |  - Unknown Freshness                 |
         +--------------------------------------+
                            |
            +---------------+---------------+
            v               v               v
        Consumer A     Consumer B      Consumer C
        (ML 팀)        (BI 팀)         (App 팀)
   ❓ "데이터 언제           ❓ "어떤 컬럼이     ❓ "이 필드 사용해도
    갱신됐지?"                  정의되지 않음"      안전한가?"

-------------------------------------------------------

[Modern: 데이터 메시 + Data Product + Data Contract]
+--------------+  +--------------+  +--------------+
| 도메인 A     |  | 도메인 B     |  | 도메인 C     |
| (고객 도메인) |  | (주문 도메인) |  | (상품 도메인) |
|              |  |              |  |              |
| [Data Product]|  |[Data Product]|  |[Data Product]|
| - customers  |  | - orders     |  | - products   |
| - sessions   |  | - payments   |  | - inventory  |
|              |  |              |  |              |
| [Contract]   |  | [Contract]   |  | [Contract]   |
| - Schema     |  | - Schema     |  | - Schema     |
| - SLA 99.9%  |  | - SLA 99%    |  | - SLA 95%    |
| - Fresh 1min |  | - Fresh 15m  |  | - Fresh 1h   |
| - PII Tags   |  | - PII Tags   |  | - PII Tags   |
+------+-------+  +------+-------+  +------+-------+
       |                 |                 |
       +--------+--------+--------+--------+
                v                 v
         +------------------------------+
         |   Self-Serve Data Platform   |
         |  - Catalog (DataHub)         |
         |  - Discovery (검색/태깅)     |
         |  - Lineage (OpenLineage)     |
         |  - Contract Registry         |
         |  - Quality Observer          |
         +------------------------------+
                      |
       +--------------+--------------+
       v              v              v
   Consumer A     Consumer B     Consumer C
   ✅ "SLA 명시"  ✅ "Schema 검증" ✅ "PII 식별"
```

**📢 섹션 요약 비유**: 데이터 컨트랙트 없는 데이터 레이크는 **"약속 없이 물을 파이프로 보내는 도시 배수관"**과 같다 — 누가, 언제, 어떤 순도로 보냈는지 알 수 없어 수질 검사를 하려면 매번 입구마다 수질 분석을 해야 한다. 데이터 프로덕트와 컨트랙트는 **"정수 처리장과 수질 검사 인증서가 부착된 정수 페트병"**이다 — 라벨에 성분표, 유통기한, 제조사가 명확히 적혀 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

데이터 프로덕트는 일반적으로 **"Input -> Compute -> Output Port"**라는 3계층 구조로 모델링되며, **ODCS(Open Data Contract Standard) v3.0**, **Data Product Specification (DPS)** 등 표준 명세를 따른다. 핵심 메타데이터는 (1) **Identity**, (2) **Schema**, (3) **SLA**, (4) **Policy**, (5) **Quality** 5대 영역으로 구성된다.

```text
+------------------------------------------------------------------+
|       데이터 프로덕트 아키텍처 (Input/Compute/Output Port)        |
+------------------------------------------------------------------+

  +-------------------------------------------------------------+
  |  Data Product: customer-360                                  |
  |  +- Version: 2.4.1  (SemVer)                                |
  |  +- Owner: domain.customer@company.com                       |
  |  +- Tier: 🥇 GOLD                                           |
  +-------------------------------------------------------------+

  [Input Port]              [Compute Port]            [Output Port]
  +--------------+         +--------------+         +--------------+
  | Upstream     |         | Transformation|         | Deliverable  |
  | Dependencies |         | Logic         |         | Assets       |
  |              |         |              |         |              |
  | - postgres  | --CDC-->| - dbt Model  | -->     | - Parquet    |
  |   :5432     |         | - Spark Job  |         |   on S3      |
  | - kafka     | --KSQL->| - Airflow    | -->     | - Iceberg    |
  |   topic     |         |   DAG        |         |   Table      |
  | - s3 raw    | -->     | - Dataframe  | -->     | - JDBC/SQL   |
  |   zone      |         |   API        |         |   Endpoint   |
  +--------------+         +--------------+         +--------------+
        |                         |                         |
        v                         v                         v
  [Contract Spec]  -------------------------------------------+
   {                                                        |
    "apiVersion": "v3.0.0",                                  |
    "kind": "DataContract",                                  |
    "id": "urn:contract:customer-360",                       |
    "version": "2.4.1",                                      |
    "name": "customer_360_gold",                             |
    "domain": "customer",                                    |
    "sla": {                                                 |
      "availability": "99.9%",                               |
      "freshness": "PT1M",   <- ISO 8601 Duration            |
      "latency_p95_ms": 5000,                                |
      "completeness": 0.999,                                 |
      "accuracy": 0.995                                      |
    },                                                       |
    "schema": [                                              |
      {"name": "customer_id", "type": "BIGINT",              |
       "pii": false, "nullable": false, "logical_type": "id"}|
    ],                                                       |
    "quality": {                                             |
      "checks": [                                            |
        {"type": "not_null", "field": "customer_id"},        |
        {"type": "row_count", "min": 1000000}                |
      ]                                                      |
    },                                                       |
    "policy": {                                              |
      "classification": "confidential",                      |
      "retention_days": 730,                                  |
      "encryption": "AES-256",                               |
      "access": "role:analyst,role:data-scientist"           |
    }                                                        |
   }                                                        |
                                                              |
  [Self-Serve Platform 레이어]                               |
  +------------------------------------------------------+  |
  |  • DataHub/Unity Catalog : 카탈로그 + Discovery      |  |
  |  • OpenLineage/Marquez   : Lineage 추적              |  |
  |  • Great Expectations    : Quality Assertion         |  |
  |  • Monte Carlo/Databrew  : Anomaly Detection         |  |
  |  • Confluent SR          : Schema Evolution 관리     |  |
  |  • Data Contract Registry (Bitol, Data Mesh Mgr)     |--+
  +------------------------------------------------------+
```

### 데이터 프로덕트 핵심 4대 속성 (4 Pillars)

| 속성 | 정의 | 측정 지표 (KPI) |
|:---|:---|:---|
| **Discoverable (검색 가능)** | 카탈로그에 등록되어 있고 태그/도메인/용도로 검색 가능 | 카탈로그 등록률 100%, Mean Time to Discover(MTTD) ≤ 5분 |
| **Addressable (주소 지정)** | 고유 식별자(URN/URI) 존재, API/경로로 직접 접근 | URN 유일성, Deprecation 전 충분한 notice (≥ 90일) |
| **Trustworthy (신뢰 가능)** | SLA/품질/리니지가 검증 가능하고 보증됨 | SLA Compliance ≥ 99.5%, 품질 검증 통과율 ≥ 99% |
| **Self-Describing (자체 기술)** | 컨슈머가 외부 문서 없이 컨트랙트만으로 사용 가능 | 컨트랙트 완전성 스코어 ≥ 0.95, README-to-Contract drift 0건 |

### 데이터 컨트랙트 SLA 계층 (Tiered SLA Design)

| Tier | 가용성 | 신선도(Freshness) | 레이턴시(p95) | 품질(Completeness) | 용도 / 컨슈머 |
|:---|:---:|:---:|:---:|:---:|:---|
| **🥉 Bronze** | 95.0% | ≤ 24h | ≤ 6h | 90% | 탐색적 분석, 데이터 사이언스 PoC |
| **🥈 Silver** | 99.0% | ≤ 15min | ≤ 1h | 99% | 대시보드, 정기 리포트 |
| **🥇 Gold** | 99.9% | ≤ 1min | ≤ 5min | 99.9% | 실시간 의사결정, 운영 자동화, ML Feature Store |
| **💎 Platinum** | 99.99% | ≤ 1sec (Streaming) | ≤ 100ms | 99.99% | 미션 크리티컬(금융 결제, 사기 탐지) |

- **📢 섹션 요약 비유**: 데이터 프로덕트의 Tier 시스템은 **"택배 등급"**과 같다 — 일반 우편(3일, 95%) / 등기(1일, 99%) / 특급(당일, 99.9%) / 당일 새벽배송(오전 9시까지, 99.99%)처럼, **가격·책임 범위·도착 보장 시간**이 명확히 다르다. 컨슈머는 자신의 비즈니스 요구에 맞는 등급을 선택한다.

---

## Ⅲ. 비교 및 연결

### 1. 데이터 컨트랙트 vs API 컨트랙트(OpenAPI)

| 구분 | API Contract (OpenAPI 3.x) | Data Contract (ODCS/DPS) |
|:---|:---|:---|
| **소비 자원** | 함수/서비스(동작) | 테이블/스트림/파일(상태) |
| **스키마 진화** | 대부분 후방호환 위주, 폐기 가능 | Append-only가 원칙, Backward->Forward->Full 호환성 단계 |
| **버전 관리** | URL Path(`/v1`, `/v2`) | SemVer + `effectiveDate` + `deprecationDate` |
| **품질 보증** | HTTP Status Code, Rate Limit | Row Count, Freshness, Completeness, Distribution |
| **계약 위반** | 4xx/5xx 응답 | 컨슈머 차단, SLO 위반 알림, **Grace Period** 제공 |
| **인프라** | API Gateway (Kong, Apigee) | DataHub, Unity Catalog, Apache Polaris |

### 2. 데이터 메시 vs 데이터 패브릭 vs 데이터 레이크하우스

| 구분 | Data Lakehouse (Databricks, Snowflake) | Data Fabric (Informatica, IBM) | Data Mesh (조직+기술) |
|:---|:---|:---|:---|

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 260 / 300

<- **이전**: [259. 259. 데이터 패브릭 통합 메타데이터 자동화 (Data Fabric Unified Metadata Automation)](/studynote/14_data_engineering/05_exam_keywords/259_data_fabric/)
**다음**: [261. 데이터 카탈로그 메타데이터 검색 자동 분류 (Data Catalog Metadata Discovery Auto Classification)](/studynote/14_data_engineering/05_exam_keywords/261_data_catalog/) ->

---
