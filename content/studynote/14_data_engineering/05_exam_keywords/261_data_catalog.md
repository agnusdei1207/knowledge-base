---
title: "261. 데이터 카탈로그 메타데이터 검색 자동 분류 (Data Catalog Metadata Discovery Auto Classification)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 카탈로그 자동 분류는 분산된 데이터소스( RDBMS, Lake, SaaS, Streaming )에서 **기술/비즈니스/운영 메타데이터**를 추출·정규화하고, 규칙 엔진·임베딩 유사도·LLM 시맨틱 추론을 결합하여 컬럼 수준 PII/도메인/용어 클래스(예: GDPR Art.4, FIBO, KR-CDE)를 자동 라벨링하는 **Knowledge Graph + Vector Index 하이브리드** 메타데이터 파이프라인이다.
> 2. **가치**: Gartner에 따르면 조직 내 데이터 분석가의 약 60%가 데이터 탐색에만 업무시간의 30~40%를 소비하는데, 자동 분류가 적용된 카탈로그는 탐색시간을 평균 65% 단축하고, 미분류 상태 대비 PII·PCI·PHI 노출 리스크를 사전 차단하여 컴플라이언스 위반 비용을 최대 70% 절감한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① 수집 방식(스키마-only vs Full Profiling vs CDC) ② 분류 정확도 vs 처리비용(LLM 호출 비용) ③ 메타데이터 저장소(Graph DB vs RDBMS vs Document Store) ④ 능동적(Active) 메타데이터와 패시브 카탈로그 선택이며, 한국 환경에서는 **개인정보보호법 가명/익명 처리 기준** 및 **공공데이터 데이터셋 표준(DS-1001)** 준수가 결정 변수다.
```

---

## Ⅰ. 개요 및 필요성

현대 기업은 평균 200~400개의 데이터소스(Snowflake, BigQuery, Kafka, Salesforce, SAP, S3 등)를 운영하며, 한 조직당 1만~10만 개의 테이블과 50만~500만 개의 컬럼이 존재한다. 전통적 방식인 **Excel 기반 데이터 사전(Glossary)**이나 **Confluence 위키**는 작성 시점의 스키마만 반영하고, 컬럼 변경·신규 테이블 추가·테넌트 분리 같은 이벤트에 대응하지 못해 **메타데이터 부패(Metadata Decay)** 문제가 발생한다. IDC 보고(2023)에 따르면 분석가의 64%가 *"신뢰할 수 있는 데이터셋을 찾는 것"*이 가장 큰 생산성 저해 요인이라고 응답했다.

**자동 분류(Auto-Classification)**는 이러한 문제를 해결하기 위해 ① 컬럼명·데이터 타입·샘플 값·통계 프로파일을 피처로 추출하고, ② 사전 학습된 임베딩 모델(BGE-M3, text-embedding-3-large 등)로 의미 벡터를 생성하며, ③ 룰 엔진·사전 매칭·LLM 추론을 앙상블하여 도메인 클래스(고객, 금융, 의료 등)와 민감도 레벨(Public, Internal, Confidential, Restricted)을 자동 부여하는 파이프라인이다. 이는 **DataOps**와 **AI Governance**가 만나는 접점이며, EU AI Act·개인정보보호법·PCI-DSS 4.0 같은 규제 대응의 기술적 기반이 된다.

```text
        [Legacy Paradigm: 수동 카탈로그]                [New Paradigm: AI-Driven Active Catalog]
   +-------------------------------+              +---------------------------------------+
   | • Excel/Confluence 수동 등록   |              | • 크롤러+CDC 자동 수집               |
   | • 스키마 변경 시 1~3개월 지연  |      --►     | • 스키마 변경 -> 실시간 메타 갱신     |
   | • 담당자 의존, Inconsistency  |              | • LLM/임베딩 기반 시맨틱 자동 분류   |
   | • 검색 = 키워드 단순 매칭     |              | • "매출이 큰 이탈 고객" 자연어 질의  |
   +-------------------------------+              +---------------------------------------+
                  |                                              |
                  v                                              v
         데이터 사일로화, "Dark Data"                지식 그래프 + 벡터 인덱스, "Data as a Product"
         ≈ 조직의 60~80% 미활용                       ↳ 데이터 리터러시, 셀프서비스 분석
```

- **📢 섹션 요약 비유**: 수동 카탈로그는 **수첩에 손글씨로 책 위치를 적어두는 사서** 같아서 책이 이동하면 주석이 틀어지지만, AI 카탈로그는 **전체 도서관에 RFID와 의미 태그를 자동 부착하고 "비즈니스 관련 책"을 의미 단위로 검색**해주는 사서 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

데이터 카탈로그의 자동 분류는 **5계층 파이프라인**으로 구성된다. ① **Ingestion(수집)** ② **Metadata Extraction & Profiling(추출/프로파일링)** ③ **Storage & Knowledge Graph(저장)** ④ **Auto-Classification Engine(분류)** ⑤ **Discovery & Governance Interface(검색/거버넌스)**. 각 계층은 비동기 메시지 큐(Kafka/Pulsar)와 REST/gRPC API로 결합된다.

```text
[1] SOURCE SYSTEMS                [2] INGESTION              [3] METADATA EXTRACTION
+--------------+                +--------------+         +--------------------------+
| Snowflake    |--JDBC/ODBC----►|              |--------►|  Schema Parser           |
| BigQuery     |--API---------►|  Connector   |         |  (DDL, Avro, Parquet)    |
| Kafka/Confluent|Schema Reg---►|  Manager     |         +--------------------------+
| Salesforce   |--Bulk API----►| (Airbyte /   |         |  Profiler                |
| S3/ADLS      |--SQS Event---►|  Fivetran/   |         |  • Cardinality           |
| SAP HANA     |--ODP---------►|  Custom)     |         |  • Null Rate / Min/Max   |
| MongoDB      |--Change Stream►|              |         |  • Histogram Top-K       |
+--------------+                +------+-------+         |  • PII Regex Sampling    |
                                       |                 +------------+-------------+
                                       v                              v
                              [4] CLASSIFICATION ENGINE        [5] STORAGE LAYER
                              +----------------------+         +------------------+
                              | Rule-Based           |         | Graph DB         |
                              |  • Regex/Dictionary  |         |  Neo4j/Janus     |
                              |  • 14 GDPR Art./PII  |         |  (Table->Col->Tag) |
                              +----------------------+         +------------------+
                              | Embedding Similarity |--------►| Vector Index     |
                              |  • Column name BERT  |         |  Milvus/Qdrant   |
                              |  • Cosine ≥ 0.78     |         |  (HNSW, IVF-PQ)  |
                              +----------------------+         +------------------+
                              | LLM Semantic         |         | Search Index     |
                              |  • GPT-4o/Claude 3.5 |         |  Elasticsearch   |
                              |  • Few-shot prompt   |         |  (BM25 + dense)  |
                              +----------------------+         +------------------+
                              | Active Learning      |         | Object Storage   |
                              |  • HITL feedback     |         |  S3/ADLS(Parquet)|
                              +----------+-----------+         +------------------+
                                         v
                              [6] GOVERNANCE & DISCOVERY UI
                              +----------------------------------+
                              |  • 자연어 검색("연간 이탈률 Top") |
                              |  • 자동 태깅 / 데이터 리니지      |
                              |  • PII 대시보드 / 접근제어 정책   |
                              |  • 데이터 품질 점수 / SLA 모니터 |
                              +----------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Connector Manager** | 소스 시스템 메타데이터 수집 | JDBC/ODBC, Iceberg/Hudi 메타 카탈로그, Schema Registry, Debezium CDC, Custom Python SDK. Airbyte·Fivetran 패턴을 차용하되 메타데이터 전용 경량화. |
| **Metadata Profiler** | 컬럼 단위 통계·패턴 추출 | Apache Spark `summary` API, Great Expectations, Pandas Profiling. 샘플링 전략: 상위 10K row (대용량은 Reservoir Sampling), 통계: `min/max/mean/std/topK/distinct_ratio`. |
| **Knowledge Graph Store** | 테이블-컬럼-도메인-비즈니스 용어 관계 저장 | Neo4j / JanusGraph / Amazon Neptune. 노드 타입: `Database->Schema->Table->Column->Tag->GlossaryTerm->Domain->Owner`. OpenLineage·Marquez 명세로 리니지 표현. |
| **Auto-Classifier** | 컬럼 클래스 라벨링 | **3-Layer Ensemble**: ① Rule (Regex, KR SSN/사업자등록번호 패턴) -> ② Embedding (Column name + sample -> BGE-M3 1024-dim -> cosine vs Class centroid) -> ③ LLM (JSON schema constrained output, e.g. `{class, confidence, rationale}`). 가중치: Rule 0.4, Embedding 0.3, LLM 0.3. |
| **Vector + Lexical Index** | 시맨틱·키워드 하이브리드 검색 | Elasticsearch BM25 + Dense Vector (ELSER, Cohere Rerank). Milvus IVF-PQ 또는 Qdrant HNSW. RRF(Reciprocal Rank Fusion, k=60)로 결과 융합. |
| **Governance & Lineage** | PII 탐지·접근제어·리니지 시각화 | OpenLineage 명세, Unity Catalog, AWS Lake Formation. 정책 엔진: OPA(Open Policy Agent), Cerbos. |

### 분류 알고리즘 심층 분석

**① 임베딩 기반 분류**는 컬럼명(`cust_birth_dt`)과 샘플 값(`"1990-04-15"`)을 결합하여 Sentence-BERT로 인코딩한 뒤, **클래스 프로토타입(centroid)**과의 코사인 유사도를 계산한다. 학습 데이터가 부족한 경우(콜드 스타트) Few-Shot Contrastive Learning으로 5-shot 수준에서도 F1 0.82 달성 가능하다. 임계값은 일반적으로 0.78, 미달 시 LLM 라우팅한다.

**② LLM 시맨틱 분류**는 다음 예시 프롬프트 구조를 따른다:

```text
SYSTEM: You are a data classification expert. Output strict JSON.
USER: Column: cust_birth_dt | Type: DATE | Sample: ["1990-04-15", "1985-12-01"]
      Domain candidates: [customer, finance, healthcare, marketing, other]
      Sensitivity: [Public, Internal, Confidential, Restricted, PII]
      Korean PIPA Article mapping: [Art.2(개인정보), Art.23(민감정보), None]
      Respond: {"class":"customer","sensitivity":"PII","law":"PIPA Art.2","conf":0.94}
```

**③ 능동 학습(Active Learning) 루프**는 분류 신뢰도가 낮거나(예: 0.6~0.78)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 261 / 300

<- **이전**: [260. 데이터 프로덕트 데이터 서비스 계약 (Data Product Data Contract SLA)](/studynote/14_data_engineering/05_exam_keywords/260_data_product_contract/)
**다음**: [262. 데이터 리니지 혈통 추적 영향도 분석 (Data Lineage Impact Analysis Provenance)](/studynote/14_data_engineering/05_exam_keywords/262_data_lineage/) ->

---
