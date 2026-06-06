---
title: "Data Lineage Impact Analysis Provenance"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 리니지(Data Lineage)는 ETL/ELT 파이프라인, DW, Lakehouse, AI/ML 모델까지 아우르는 데이터 자산의 **출처(Provenance)·흐름·변환 이력**을 메타데이터 그래프(Directed Acyclic Graph, DAG)로 추적·기록하는 능동적 메타데이터(Active Metadata) 거버넌스 체계이며, 영향도 분석(Impact Analysis)은 그래프의 역방향/순방향 탐색과 Column-Level Lineage 매핑을 통해 변경 전·후 위험을 정량화하는 기법이다.
> 2. **가치**: Gartner에 따르면 데이터 엔지니어의 **작업 시간 중 60~80%가 “데이터 디스커버리 및 의존성 파악”** 에 소요되며, W3C PROV 기반 리니지 도입 시 평균 MTTR(Mean Time To Repair) **45% 단축, 데이터 신뢰도(Trust Score) 30% 이상 향상, GDPR/개인정보보호법·데이터산업법·AI 신뢰성 법규 대응의 객관적 증거** 확보가 가능하다.
> 3. **판단 포인트**: ① 자동 추론(Automatic Inference, SQL 파싱/Log 분석) vs 수동 선언(Manual Annotation) 비율, ② Column-Level/Row-Level 해상도, ③ 메타데이터 그래프 저장소 선택(RDF/SPARQL vs Property Graph/Neo4j vs JSON-LD), ④ 실시간 Push 기반 vs 배치 Pull 기반 수집 모델, ⑤ W3C PROV-O 표준 준용 여부, ⑥ 개인정보 마스킹과 리니지 동시 처리 설계가 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

현대 데이터 플랫폼은 Hadoop->Lakehouse->Data Mesh로 빠르게 진화하면서, 한 개의 도메인 테이블이 수십~수백 개의 다운스트림(Downstream) 소비처(BI 대시보드, ML Feature Store, API, 규제 보고서)를 갖는 **N:N 의존성 그래프** 구조로 변모했다. 전통적인 데이터 카탈로그(Data Catalog)가 “데이터가 무엇인가(What)”만 답했다면, **리니지(Lineage)는 “데이터가 어디서 와서 어디로 가는가(Where) + 어떻게 변형되었는가(How) + 누가/언제 변경했는가(Who/When)”** 라는 5W1H 기반의 시간·인과 추적을 가능케 한다.

국내에서도 2022년 데이터산업법 시행, 2023년 개정 개인정보보호법의 가명·익명 처리 의무, 2024년 AI 기본법(안) 발의, 마이데이터 사업자 의무 등으로 인해 **“어떤 원천 데이터가 어떤 AI/리포트 결과를 만들었는가”** 를 법적으로 입증해야 하는 수요가 폭증했다. 또한 Apache Airflow/Dagster/Spark 기반 분산 환경에서 한 컬럼의 데이터 타입 변경이 3개월 뒤 KPI 대시보드 오류로 나타나는 등, **“보이지 않는 데이터 사일로(Invisible Data Silo)”** 가 컴플라이언스·재무·운영 리스크로 직결된다.

```text
+----------------------------------------------------------------------+
|           데이터 리니지 & 영향도 분석 거버넌스 전(全)景观                 |
+----------------------------------------------------------------------+

  [Source]        [Ingest]         [Transform]        [Serve]       [Consume]
  +-------+      +---------+       +----------+      +--------+    +--------+
  | ERP   |      | Kafka   |       |  Spark   |      | DW     |    | BI     |
  | CRM   |--+   | CDC     |--+    |  dbt     |--+   | Lake   |---->| Tableau|
  | Logs  |  |   | API GW  |  |    | Airflow  |  |   | Iceberg|    | PowerBI|
  | IoT   |  |   +----+----+  |    +----+-----+  |   +----+---+    +----+---+
  +-------+  |        v       |         v        |        v            |
             |   +--------+   |   +----------+   |   +---------+       |
             |   |Raw Zone|   |   |Cleansed  |   |   | Mart    |       |
             |   |(Bronze)|   |   |(Silver)  |   |   |(Gold)   |       |
             |   +----+---+   |   +----+-----+   |   +----+----+       |
             |        |       |        |         |        |            |
             |        v       |        v         |        v            v
             |   +------------------------------------------------------+
             |   |       Metadata Graph (Lineage Backbone)               |
             |   |  +-------------------------------------------------+  |
             |   |  |  Node: Table/Column/Job/MLModel/Dashboard       |  |
             |   |  |  Edge: TRANSFORMS / DERIVES / READS / WRITES     |  |
             |   |  |  Attr : ts, actor, query_hash, schema_hash       |  |
             |   |  +-------------------------------------------------+  |
             |   +-----------------+------------------------------------+
             |                     |
             |                     v
             |      +------------------------------+
             |      |  Lineage & Impact Analytics  |
             |      |  +- Upstream Provenance (Root)|
             |      |  +- Downstream Impact (Blast)|
             |      |  +- Column-Level Diff        |
             |      |  +- SLA / Freshness Heatmap  |
             |      |  +- GDPR/PIAI Data Flow Map  |
             |      +------------------------------+
```

**기존 패러다임(Pre-Lineage Era)** 은 데이터 사전을 Excel/Confluence로 관리하는 **수동·정적·문서 중심** 방식이었고, 결과적으로 카탈로그와 실제 운영 환경의 괴리(Drift)가 40~60%에 달했다. **신규 패러다임(Active Metadata Era)** 은 Airflow/OpenLineage 같은 이벤트 기반 자동 추론 + W3C PROV 표준 메타모델 + Property Graph DB(Neo4j/Amazon Neptune/Apache JanusGraph) 기반의 **자동·동적·그래프 중심** 방식으로, “코드(Pipeline as Code) -> 메타데이터 자동 추출 -> 그래프 즉시 갱신 -> 영향도 즉시 분석” 의 폐루프(Closed-Loop) 구조를 실현한다.

- **📢 섹션 요약 비유**: 데이터 리니지가 없는 조직은 “출처를 모르는 유통기한이 지난 음식을 그대로 먹는 식당” 같고, 리니지가 갖춰진 조직은 “어느 농장의 어느 날짜 농산물인지, 어떤 조리사를 거쳤는지, 어디로 배달됐는지 블록체인에 기록된 푸드 체인” 과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

데이터 리니지 시스템은 일반적으로 **① 수집 계(Ingestion Layer) ② 그래프 저장 계(Graph Store) ③ 의미·추론 계(Semantic Layer) ④ 영향도 분석 계(Impact Engine) ⑤ 거버넌스 UI/API 계** 의 5-Tier 아키텍처로 구성된다. OpenLineage, W3C PROV, OpenMetadata 같은 개방형 표준이 등장하면서 벤더 종속(Apache Atlas 전용, Collibra 전용) 문제가 상당 부분 해소되었다.

```text
+----------------------------------------------------------------------+
|        리니지 & 영향도 분석 아키텍처 (OpenLineage/PROV 기반)           |
+----------------------------------------------------------------------+

   +-------------------------------------------------------------+
   |  ① Source Systems & Pipeline Engines                        |
   |  Spark | Airflow | dbt | Dagster | Snowflake | Kafka | Fivetran|
   |  ML:   | MLflow | TFX  | Kubeflow | SageMaker              |
   +----------------------+--------------------------------------+
                          | (emit events: START/COMPLETE/FAIL/FACET)
                          v
   +-------------------------------------------------------------+
   |  ② Ingestion Layer (Collectors/Adapters)                   |
   |  +- SQL Parser (sqlglot, jOOQ, Apache Calcite)             |
   |  +- Query Log Listener (JDBC proxy: MaxGauge, pganalyze)   |
   |  +- OpenLineage HTTP Transport (Marquez, DataHub)          |
   |  +- SDK/Operator Hook (airflow-openlineage, dbt-artifacts) |
   +----------------------+--------------------------------------+
                          |  (JSON-LD / Avro / Kafka)
                          v
   +-------------------------------------------------------------+
   |  ③ Graph Store & Metadata DB                                |
   |  +----------------+   +------------------------------+     |
   |  | Property Graph |   | Search Index (Elasticsearch) |     |
   |  | Neo4j / Neptune|   | Full-text / Facet Search      |     |
   |  | JanusGraph     |   +------------------------------+     |
   |  | + RDF/SPARQL   |   +------------------------------+     |
   |  | (Apache Atlas) |   | Feature/Vector Store (Pinecone|     |
   |  +----------------+   | -> AI Auto-Tagging)            |     |
   |                       +------------------------------+     |
   +----------------------+--------------------------------------+
                          |
                          v
   +-------------------------------------------------------------+
   |  ④ Semantic & Reasoning Layer (W3C PROV-O / SHACL)         |
   |  • Entity: Dataset(D), Column(C), Job(J), Process(P)        |
   |  • Relation: wasDerivedFrom, used, wasGeneratedBy           |
   |  • Inference: transitive closure, temporal validity         |
   |  • Ontology: Business Glossary ↔ Technical Asset 매핑        |
   +----------------------+--------------------------------------+
                          |
                          v
   +-------------------------------------------------------------+
   |  ⑤ Impact Analysis Engine                                   |
   |  +---------------------+  +-----------------------------+  |
   |  | Forward Impact(BFS)  |  | Backward Provenance(BFS)    |  |
   |  | "이 컬럼 바꾸면?"   |  | "이 결과는 어디서 왔나?"   |  |
   |  +---------------------+  +-----------------------------+  |
   |  +---------------------+  +-----------------------------+  |
   |  | Schema Diff &       |  | SLA/Freshness Heatmap       |  |
   |  | Column-Level Diff   |  | (Critical Path 탐지)         |  |
   |  +---------------------+  +-----------------------------+  |
   |  +-----------------------------------------------------+   |
   |  | Privacy/PII Flow Mapping (GDPR Art.30 / PIPA)        |   |
   |  | -> 자동 DPIA(Data Protection Impact Assessment)        |   |
   |  +-----------------------------------------------------+   |
   +----------------------+--------------------------------------+
                          |
                          v
   +-------------------------------------------------------------+
   |  ⑥ Governance UI / API / Webhook                            |
   |  • DataHub | Unity Catalog | Collibra | Alation | DataHub   |
   |  • Webhook -> Slack/Jira (Change Mgmt)                       |
   |  • API: GraphQL/REST/OPC-UA for IIoT edge                  |
   +-------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① 소스/파이프라인 엔진** | 데이터의 실제 생성·이동·변환 수행 | Apache Spark(`executionListener`), Airflow(`on_success_callback`), dbt(`run_results.json`+`manifest.json`), Snowflake(`ACCESS_HISTORY`), BigQuery(`INFORMATION_SCHEMA.JOBS_BY_PROJECT`), Kafka Schema Registry |
| **② 수집(Ingestion) 어댑터** | 실행 이벤트를 캡처하여 표준 메타데이터로 변환 | **OpenLineage**(Marquez 기반, JSON-LD, FACET 스펙: `dataQualityMetrics`, `schema`, `lifecycleStateChange`), **SQL 파서**(`sqlglot`, Apache Calcite) -> Column-Level Lineage 자동 추론, **JDBC Proxy**(`MaxGauge`, `pganalyze`)로 누락된 쿼리 보완 |
| **③ 그래프/메타데이터 저장소** | 노드/엣지의 영속 저장과 인덱싱 | **Property Graph**: Neo4j(2.4억 노드 지원, Cypher), Amazon Neptune(RDF/SPARQL + Gremlin), TigerGraph; **Document**: MongoDB; **Search**: Elasticsearch/OpenSearch(전문검색·시각화); **벡터 DB**: Milvus/Pinecone(LLM 기반 자동 분류·태깅) |
| **④ 시맨틱·추론 계층** | 메타데이터에 의미·제약·시간 속성 부여 | **W3C PROV-O**(`prov:Entity`, `prov:Activity`, `prov:Agent`, `prov:wasDerivedFrom`), **DCAT v3**, **SHACL**(Shape Constraint Language)로 데이터 품질 제약 표현, **OWL2 RL** 추론기로 transitive closure 계산 |
| **⑤ 영향도 분석 엔진** | 그래프 탐색·시뮬레이션·스코어링 | **BFS/DFS**(Forward=Downstream Impact, Backward=Upstream Provenance), **PageRank 변형**(Criticality Score = 다운스트림 테이블 수 × BI 의존도 × SLA 우선순위), **What-If 시뮬레이션**(스키마 diff -> 영향 노드 마킹), **SLA 파급 효과 계산** |
| **⑥ 거버넌스 UI/API** | 비기술 사용자에게 시각화·자동화 제공 | DataHub(DataHub Lite 포함), Unity Catalog(MS Fabric/Databricks 통합), Apache Atlas(Ranger 정책 연동), Grafana 리니지 플러그인, Webhook->Jira(변경 관리 티켓 자동 생성) |

### 핵심 알고리즘과 기술 파라미터

1. **Column-Level Lineage 자동 추론 알고리즘**
   - SQL AST(Abstract Syntax Tree) -> `SELECT target_col FROM ... WHERE ...` 구문에서 projection/join/aggregation/udf 노드를 따라가며 source->target 매핑 행렬(M × N) 생성.
   - 예: `SELECT a.id, SUM(b.amt) FROM orders a JOIN payments b ON a.id=b.oid GROUP BY a.id` -> `mart.daily_revenue.oid <- orders.id`, `mart.daily_revenue.total_amt <- payments.amt`.
   - 한계: 동적 SQL, View 체인, Stored Procedure, dbt 매크로는 별도 후처리(ML 기반 콜럼 매칭, Jaccard 0.7+ 임계치) 필요.

2. **Forward Impact Analysis 수식**

$$
\text{ImpactScore}(N) = \sum_{i=1}^{k} \big( w_{criticality}(C_i) \cdot w_{sla}(S_i) \cdot w_{pii}(P_i) \cdot \frac{1}{1+\log d(N,C_i)} \big)
$$

   여기서 $C_i$=다운스트림 자산, $S_i$=SLA 등급, $P_i$=PII 민감도(0~1), $d(N,C_i)$=그래프 거리. 임계치 ≥0.7이면 **High Impact**(Change Advisory Board 승인 필요)로 분류.

3. **W3C PROV-O 핵심 트리플**
   ```
   :job_123  a  prov:Activity ;
             prov:used    :source_table ;
             prov:generated :target_table ;
             prov:wasAssociatedWith :user_alice ;
             prov:startedAtTime  "2024-05-01T10:00:00Z"^^xsd:dateTime .
   :target_table  prov:wasDerivedFrom :source_table .
   ```

4. **OpenLineage 이벤트
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 262 / 300

<- **이전**: [261. 데이터 카탈로그 메타데이터 검색 자동 분류 (Data Catalog Metadata Discovery Auto Classification)](/studynote/14_data_engineering/05_exam_keywords/261_data_catalog/)
**다음**: [263. 데이터 품질 관리 프로파일링 정합성 검증 (Data Quality Management Profiling Validation)](/studynote/14_data_engineering/05_exam_keywords/263_data_quality/) ->

---
