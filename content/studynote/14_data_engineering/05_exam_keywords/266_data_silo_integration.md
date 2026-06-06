---
title: "Data Silo Breaking Integration Strategy"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 사일로(Data Silo) 해소는 도메인 간 데이터의 **물리적·논리적·거버넌스적 결합 고리(Coupling Link)**를 EDA(Event-Driven Architecture), CDC(Change Data Capture), Data Mesh, Data Fabric, API-Led Connectivity로 재설계하여, **단일 진실 공급원(Single Source of Truth, SSoT)**과 **데이터 컨트랙트(Data Contract)** 기반의 자율적·연결형·공유형 데이터 자산 체계를 구축하는 전략이다.
> 2. **가치**: 사일로 해소 시 Gartner 기준 마스터 데이터 정확도 **95% 이상**, 데이터 사내 재활용률 **2.4배 증가**, 의사결정 지연(Latency to Insight) **수 시간 -> 수 분(80% 단축)**, 통합·유지보수 비용 **TCO 30~45% 절감**, 신규 분석 워크로드 배포 시간(MTTD) **70% 단축**의 정량적 효과를 달성할 수 있다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) 중앙집중형 vs 분산형 거버넌스(Hub-and-Spoke ↔ Data Mesh)**, **(b) 동기식 API 연동 vs 비동기식 EDA**, **(c) ETL(추출-변환-적재) vs ELT(추출-적재-변환)**, **(d) Data Fabric(가상화) vs Data Lakehouse(물리적 통합)**의 4축이며, 도메인 자율성, 데이터 볼륨, 일관성 요구 수준, 레거시 결합도에 따라 **적응형 통합 패턴(Adaptive Integration Pattern)**을 선정해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 데이터 사일로의 발생 배경

데이터 사일로는 동일한 조직 내 **업무 부서·애플리케이션·플랫폼·네트워크 경계**에서 데이터가 **독립적으로 생성·저장·관리**되어 외부 시스템과의 의미적·구조적·접근적 상호운용성을 상실한 상태를 의미한다. 이는 1980년대 메인프레임 시대를 거쳐 2000년대 SOA(Service-Oriented Architecture) 이전까지의 **수직 통합(Vertical Integration) 방식**에서 기인하며, 2010년대 클라우드·SaaS 도입 확대로 **다중 벤더·다중 클라우드(Hybrid/Multi-Cloud)** 환경이 보편화되면서 **수평적 파편화(Horizontal Fragmentation)** 문제가 가중되었다.

### 2. 기술적 도전 과제

| 도전 유형 | 구체적 증상 | 기술적 원인 |
|:---|:---|:---|
| **구조적 사일로** | 동일 고객 데이터가 CRM, ERP, MES에 3중 저장 | 시스템 간 ID 불일치, Primary Key 충돌, 비정규화 스키마 |
| **의미적 사일로** | "고객" 의미가 부서별로 다름 (CRM: 잠재고객, ERP: 거래처) | 마스터 데이터 표준 부재, 온톨로지(Ontology) 미정의 |
| **접근적 사일로** | 데이터를 얻기 위해 **수십 건의 티켓·이메일** 필요 | API 미노출, 방화벽 차단, 권한 정책 분산 |
| **거버넌스 사일로** | 데이터 품질·보안 정책이 부서별 상이 | 중앙 Data Governance Office(DGO) 부재 |
| **파이프라인 사일로** | ETL이 부서별로 중복 작성 (예: 5개 부서가 같은 매출 데이터 추출) | 카탈로그 부재, Lineage 추적 불가 |

### 3. 패러다임 변화: 통합 진화의 4단계

```text
[단계 1: Point-to-Point (1980s~1990s)]
   A --EDI/직접 DB Link-- B
   C --FTP 파일 전송-- D
   문제: N×N 연결 복잡도, 결합도 100%

[단계 2: ESB/EAI (2000s)]
          +----------+
   A ----►|          |◄---- D
          |  ESB     |
   B ----►| (Hub)   |◄---- E
          +----------+
   문제: 단일 장애점(SPOF), 벤더 종속, 배치 중심 latency

[단계 3: API-Led / iPaaS (2010s)]
   System --► Experience API --► Process API --► System API
            (MuleSoft / Apigee / WSO2 계층)
   문제: API 카탈로그와 데이터 카탈로그 분리, 의미적 중재 부족

[단계 4: Data Mesh / Fabric / Lakehouse (2020s~)]
   +---------+  +---------+  +---------+
   |도메인 A |  |도메인 B |  |도메인 C |  <- 도메인 자율성
   |+ Data   |  |+ Data   |  |+ Data   |     + Data-as-a-Product
   |Product  |  |Product  |  |Product  |     + Federated Governance
   +----+----+  +----+----+  +----+----+
        +------+------+------+-----+
               v              v
       [Data Catalog]   [Policy Engine]
       (DataHub/Atlas)  (Apache Ranger)

   + Data Plane: Kafka + Iceberg/Delta Lake
   + Control Plane: Schema Registry + Data Contracts
```

- **📢 섹션 요약 비유**: 사일로 해소를 **건물의 리모델링**에 비유하면, 구시대의 **담장 쌓기(데이터 격리)**로는 보안을 확보했으나 빛과 바람(정보 흐름)이 막혔고, 이를 **중정(中庭)·통로·엘리베이터(API·이벤트 버스)**로 개방하여 **단단한 골조(Federated Governance)** 위에서 각 세대(도메인)가 자율적으로 꾸미는 **주상복합 아파트(Data Mesh)**로 재설계하는 과정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 4-Layer 통합 참조 아키텍처

```text
+-------------------------------------------------------------+
|  L4. Consumer Layer (소비자)                                 |
|  BI(Tableau/PowerBI), ML(AutoML), LLM(RAG), Ops Dashboard   |
+-------------------------------------------------------------+
|  L3. Semantic & Governance Layer (의미·거버넌스)              |
|  Data Catalog ◄--► Data Lineage ◄--► Data Quality          |
|  (DataHub / Apache Atlas / Unity Catalog)                   |
|  + Knowledge Graph (Neo4j/Amazon Neptune) + Ontology        |
+-------------------------------------------------------------+
|  L2. Integration & Processing Layer (통합·처리)              |
|  +----------+----------+----------+----------+              |
|  | EDA Bus  | CDC/ETL  | API GW   | Federated|              |
|  | Kafka    | Debezium | Kong     | Query    |              |
|  | + Avro   | + Flink  | + OAuth2 | (Trino)  |              |
|  +----------+----------+----------+----------+              |
|  + Schema Registry (Confluent / Apicurio)                   |
|  + Data Contracts (Protobuf-based, OpenDataContract 표준)    |
+-------------------------------------------------------------+
|  L1. Source / Domain Data Products (원천·도메인 제품)        |
|  +----------+----------+----------+----------+              |
|  | CRM      | ERP      | IoT/OT   | 외부     |              |
|  | (도메인) | (도메인) | (도메인) | (API)    |              |
|  | + Owner  | + Owner  | + Owner  | + SLA    |              |
|  +----------+----------+----------+----------+              |
|  + Storage: Iceberg / Delta Lake / Hudi (Open Table Format) |
+-------------------------------------------------------------+
   ^                       |
   | Observability         | Policy as Code
   | (OpenTelemetry)       | (OPA / Cedar)
```

### 2. 핵심 컴포넌트 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Schema Registry** | 스키마 진화(Evolution)와 호환성 보장 | **Confluent Schema Registry** + **Avro/Protobuf/JSON Schema** 저장. `BACKWARD`, `FORWARD`, `FULL` 호환성 모드로 Topic 단위 스키마 버전 관리. 호환성 위반 시 Producer 차단. **Apicurio Registry** 오픈소스 대안. |
| **CDC (Change Data Capture) Connector** | 원천 DB의 변경을 실시간 캡처 | **Debezium**(MySQL/PostgreSQL/MongoDB Binlog/WAL 기반), **Oracle GoldenGate**, **AWS DMS**, **Maxwell's Daemon** 등. `op: c/u/d/r` (create/update/delete/read) 이벤트 발행. 초기 스냅샷 + 증분 Tail 모드. |
| **Event Streaming Backbone** | 도메인 간 비동기 메시지 전달 | **Apache Kafka**(Partition=병렬성 단위, Replication Factor≥3, ISR 관리), **Pulsar**(계층적 스토리지), **Redpanda**(C++ Raft), **NATS JetStream**(경량). 멱등성 보장을 위해 **Exactly-Once Semantics(EOS)** + Transactional Producer/Consumer. |
| **Data Lakehouse** | 통합 저장 + 트랜잭션 보장 | **Apache Iceberg**(Partition Evolution, Hidden Partitioning, Time Travel), **Delta Lake**(ACID on S3), **Apache Hudi**(Copy-on-Write vs Merge-on-Read). Parquet 컬럼형 + 메타데이터 레이어로 Petabyte급 분석/ML 동시 지원. |
| **Data Catalog & Lineage** | 자산 발견·품질·혈통 추적 | **DataHub**(LinkedIn, 메타데이터 모델 P/E/S), **Apache Atlas**(Hadoop 생태계 통합), **Amundsen**(Lyft), **Unity Catalog**(Databricks). OpenLineage 표준 + Marquez API로 **자동 혈통 수집**. |
| **Data Quality Engine** | 데이터 신뢰도 검증 | **Great Expectations**(Expectation Suite), **Deequ**(Amazon, Spark 기반), **Monte Carlo / Datafold**(외부 관측), **Soda Core**(YAML 기반 체크). SLA 위반 시 Schema Registry에 **Quarantine Topic** 발행. |
| **Federated Query Engine** | 물리적 이동 없는 가상 통합 | **Trino(구 PrestoSQL)**, **Apache Doris**, **ClickHouse**, **Starburst(엔터프라이즈)**. Catalog 플러그인으로 S3/Hive/Iceberg/PostgreSQL/MongoDB를 단일 SQL로 횡단 질의. Data Mesh의 **Polyglot Storage** 핵심. |
| **API Gateway & Service Mesh** | 동기식 통합 + 트래픽 통제 | **Kong**, **Apigee**, **AWS API Gateway** + **Istio/Linkerd**(mTLS, Circuit Breaker, Retry). gRPC + Protocol Buffers로 내부 통신, REST/GraphQL로 외부 노출. |
| **Policy Engine** | 보안·컴플라이언스 자동 집행 | **OPA(Open Policy Agent) + Rego**, **Apache Ranger**(Hadoop), **AWS Lake Formation**, **Collibra**(거버넌스). **Attribute-Based Access Control(ABAC)** + Row/Column-Level Security. |
| **Knowledge Graph** | 의미론적 통합(Semantic Integration) | **Neo4j / Amazon Neptune / Stardog**. 온톨로지(RDFS/OWL)로 도메인 간 **개체(Entity)와 관계(Relationship)** 명세. ETL에서 발견되지 않는 **암묵지(Hidden Relationship)** 추론. |

### 3. 핵심 메커니즘: Data Contract 패턴

```text
+------------ Producer (도메인) ------------+    +------------ Consumer -------------+
|  Data Product: "customer_profile"         |    | Analytics / ML Pipeline            |
|  +----------------------------------+     |    |                                   |
|  | SLA: latency ≤ 5s, freshness ≤  |     |    |  Schema 이해                      |
|  | 1m, availability 99.9%           |     |    |  v                                |
|  | Owner: crm-data-team             |     |    |  자동 코드 생성                    |
|  | Schema:                          |     |    |  (dbt / Spark / Pandas)           |
|  |  - id: BIGINT PK                 |     |    |                                   |
|  |  - email: STRING NOT NULL        |     |    |  Contract Test                    |
|  |  - gdpr_consent: BOOL            |     |    |  - Schema 호환성                  |
|  |  - updated_at: TIMESTAMP         |     |    |  - SLA 위반 감지                  |
|  +----------------------------------+     |    |  - PII 마스킹 검증                |
|             |                              |    |                                   |
|             v                              |    |                                   |
|  Protobuf 정의 -> Schema Registry 등록     |    |  Schema Registry에서 최신 버전 pull|
|             |                              |    |                                   |
|             v                              |    |                                   |
|  Kafka Topic: customer.profile.v1 ---------+---►|  Consumer Group: analytics-cg    |
|  (Partitioned by region, RF=3)             |    |                                   |
+--------------------------------------------+    +-----------------------------------+
```

**Data Contract 핵심 속성**: (1) **Schema**, (2) **SLA**(latency, freshness, availability), (3) **Owner**(도메인 책임), (4) **PII/보안 분류**, (5) **Versioning 규칙**, (6) **Breach 시 알림 채널**. 이를 **OpenDataContract Standard(OASIS 표준화 진행 중)**로 표현하며, **Schema-as-Code**(GitOps)로 관리한다.

### 4. CDC 이벤트 순차화(Idempotency & Ordering) 원리

```text
[원천 DB: PostgreSQL]                  [Kafka Topic: orders.cdc]
   +------------+                          +------------------+
   | WAL Log    |   Debezium Engine         | Partition 0      |
   | (LSN 순)   +-------------------------►|  LSN 100: INSERT |
   +------------+   1. Snapshot            |  LSN 105: UPDATE |
                     2. Streaming Tail     |  LSN 110: COMMIT |
                                            +------------------+
                                            | Partition 1      |
                                            |  (별도 PK 범위)  |
                                            +------------------+
                                                      |
                                                      v
                                            [Flink / Spark Streaming]
                                            keyBy(pk) -> 1:1 순서 보장
                                            (같은 PK는 같은 Partition)
```

**핵심 파라미터**: `binlog.row.image = FULL` (변경 전/후 전체), `tombstones.on.delete = true` (DELETE 시 null 레코드), `exactly.once = true` (Kafka Transaction), `max.batch.size = 2048`, `max.queue.size = 8192`.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 266 / 300

<- **이전**: [265. 데이터 거버넌스 프레임워크 정책 표준 (Data Governance Framework DAMA DMBOK)](/studynote/14_data_engineering/05_exam_keywords/265_data_governance_framework/)
**다음**: [267. 스트리밍 ETL 실시간 파이프라인 설계 (Streaming ETL Real-time Pipeline Design)](/studynote/14_data_engineering/05_exam_keywords/267_streaming_etl/) ->

---
