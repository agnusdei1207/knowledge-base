---
title: 223. 데이터 패브릭 (Data Fabric) 메타데이터 가상화 AI 통합
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]])은 이기종 [[001_dikw_pyramid|데이터]] 소스를 이동 없이 [[015_virtualization|가상화]]([[247_data_virtualization_federated_query|Data Virtualization]])로 연결하고, [[190_ai_llm_requirements_specification|AI]]/ML이 [[012_metadata|메타데이터]]를 자동으로 탐색·[[104_classification_analysis|분류]]하여 통합 [[001_dikw_pyramid|데이터]] 접근 레이어를 형성하는 아키텍처다.
> 2. **가치**: [[001_dikw_pyramid|데이터]]를 물리적으로 복사하지 않아도 어디서든 일관된 뷰([[151_sql_view_virtual_table|View]])를 제공하므로, 멀티클라우드·[[061_on_premise_legacy_infrastructure|온프레미스]] 혼합 환경에서 [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]([[001_dikw_pyramid|Data]] [[002_silo_hyeonhyung|Silo]])를 제거한다.
> 3. **판단 포인트**: [[212_data_fabric_virtualization|데이터 패브릭]]은 기술 중심([[012_metadata|메타데이터]]·[[015_virtualization|가상화]])이고 [[211_data_mesh_domain_ownership|데이터 메시]]는 조직 중심([[064_relation_domain|도메인]] 소유권)이므로, 두 접근법은 배타적이 아니라 상호 보완 [[083_relationship_in_er_model|관계]]다.

---

## Ⅰ. 개요 및 필요성

Gartner는 [[212_data_fabric_virtualization|데이터 패브릭]]을 **"[[001_dikw_pyramid|데이터]] 관리 설계 개념으로, [[136_variance|분산]]·이기종 환경 전반에 걸쳐 유연하고 탄력적인 [[001_dikw_pyramid|데이터]] 통합을 가능하게 하는 아키텍처"** 로 정의한다. 핵심은 [[001_dikw_pyramid|데이터]]를 한 곳에 모으지 않고, 있는 자리에서 연결하는 것이다.

### 등장 배경

| 문제 | 설명 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]] ([[001_dikw_pyramid|Data]] [[002_silo_hyeonhyung|Silo]]) | 부서별·시스템별 고립된 [[001_dikw_pyramid|데이터]] 저장소 |
| 멀티클라우드 복잡성 | AWS·Azure·GCP·[[061_on_premise_legacy_infrastructure|온프레미스]] 혼재 |
| 거버넌스 파편화 | 소스별 상이한 보안·품질 [[164_policy|정책]] |
| [[215_etl_vs_elt_pipeline|ETL]] 비용 | 모든 소스를 복사하는 파이프라인 유지 비용 |

📢 **섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]]은 "도서관 책을 한 곳으로 모으지 않고, 전국 도서관 통합 검색 시스템을 구축하는 것"이다. 책은 제자리에 있지만 어디서든 검색하고 대출 예약할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. [[212_data_fabric_virtualization|데이터 패브릭]] 아키텍처 전체 구조

```
        애플리케이션 / 분석 / AI·ML 소비자
              │          │          │
              ▼          ▼          ▼
┌──────────────────────────────────────────────────┐
│           Unified Data Access Layer              │
│        (통합 데이터 접근 레이어)                  │
│  ┌────────────────────────────────────────────┐  │
│  │   Data Virtualization Engine               │  │
│  │   (데이터 가상화 엔진, 물리 이동 없이 쿼리) │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │   Intelligent Metadata Layer               │  │
│  │   (AI 기반 메타데이터 자동 탐색·분류·추천)  │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │   Federated Governance & Security          │  │
│  │   (접근제어·마스킹·감사 로그 통합 관리)     │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
          │         │         │         │
          ▼         ▼         ▼         ▼
    ┌──────┐   ┌──────┐  ┌──────┐  ┌──────┐
    │Oracle│   │ S3   │  │Kafka │  │SAP   │
    │ DB   │   │Lake  │  │Stream│  │ERP   │
    └──────┘   └──────┘  └──────┘  └──────┘
     온프레미스    AWS       이벤트    SaaS
```

### 2-2. 핵심 구성 요소

| 구성 요소 | 역할 | 기술 예시 |
|:---|:---|:---|
| [[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]] (능동 [[012_metadata|메타데이터]]) | AI가 [[012_metadata|메타데이터]]를 자동 수집·[[104_classification_analysis|분류]]·추천 | Atlan, Alation |
| [[247_data_virtualization_federated_query|Data Virtualization]] ([[360_data_virtualization|데이터 가상화]]) | 물리 이동 없이 이기종 소스 통합 [[298_qkv_attention|쿼리]] | Denodo, Dremio, Starburst |
| [[160_knowledge_graph_graphrag_integration|Knowledge Graph]] ([[160_knowledge_graph_graphrag_integration|지식 그래프]]) | [[001_dikw_pyramid|데이터]] 간 [[083_relationship_in_er_model|관계]]·리니지 [[033_graph_representation|그래프 표현]] | Neo4j, AWS Neptune |
| Governance Automation | [[164_policy|정책]] 자동 적용, 마스킹, 접근제어 | Apache Ranger, [[237_opa_open_policy_agent_gatekeeper|OPA]] |
| [[014_api_posix|API]] Fabric | RESTful·[[246_graphql_query_language_overfetching_solution|GraphQL]] 통합 [[001_dikw_pyramid|데이터]] [[014_api_posix|API]] | Kong, MuleSoft |

### 2-3. [[190_ai_llm_requirements_specification|AI]] 기반 [[012_metadata|메타데이터]] 자동화 흐름

```
데이터 소스 연결
      │
      ▼
┌─────────────────────────────────────┐
│  Metadata Crawler (자동 탐색 봇)    │
│  - 스키마 자동 감지                  │
│  - PII (개인식별정보) 자동 태그      │
│  - 데이터 분류 (민감도 레벨)         │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Active Metadata Engine             │
│  - 사용 패턴 학습 → 연관 데이터 추천 │
│  - 품질 이상 자동 감지               │
│  - 리니지 자동 생성                  │
└─────────────────────────────────────┘
      │
      ▼
   데이터 소비자에게 "검색 → 이해 → 신뢰" 경험 제공
```

📢 **섹션 요약 비유**: [[190_ai_llm_requirements_specification|AI]] [[012_metadata|메타데이터]] 엔진은 "도서관 사서 [[190_ai_llm_requirements_specification|AI]]"다. 새 책이 들어오면 자동으로 제목·저자·장르를 [[104_classification_analysis|분류]]하고, 이 책을 좋아하는 독자에게 추천까지 한다.

---

## Ⅲ. 비교 및 연결

### 3-1. [[212_data_fabric_virtualization|데이터 패브릭]] vs [[211_data_mesh_domain_ownership|데이터 메시]] 비교

| 구분 | [[212_data_fabric_virtualization|데이터 패브릭]] ([[212_data_fabric_virtualization|Data Fabric]]) | [[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]]) |
|:---|:---|:---|
| 중심축 | 기술 ([[012_metadata|메타데이터]]·[[015_virtualization|가상화]]) | 조직 ([[064_relation_domain|도메인]] 소유권) |
| 접근 방식 | 중앙 기술 레이어로 통합 | [[064_relation_domain|도메인]]별 [[136_variance|분산]] 자율 운영 |
| 거버넌스 | 자동화된 중앙 [[164_policy|정책]] 엔진 | 연합(Federated) 공동 협의 |
| [[190_ai_llm_requirements_specification|AI]] 활용 | 핵심 ([[012_metadata|메타데이터]] 자동화) | 보조적 (품질 모니터링) |
| 적합 조직 | 기존 시스템 복잡한 대기업 | [[064_relation_domain|도메인]] 팀 역량 높은 조직 |
| 배타 여부 | 상호 보완 가능 | 상호 보완 가능 |

### 3-2. [[360_data_virtualization|데이터 가상화]]([[247_data_virtualization_federated_query|Data Virtualization]]) 심화

[[360_data_virtualization|데이터 가상화]]는 원본 [[001_dikw_pyramid|데이터]]를 복사하지 않고, [[298_qkv_attention|쿼리]] 시점에 소스에서 직접 [[001_dikw_pyramid|데이터]]를 가져와 통합 뷰를 제공한다.

- **Push-Down Optimization (푸시다운 최적화)**: 필터·집계 연산을 원본 소스에서 실행해 네트워크 전송량 최소화
- **Semantic Layer (시맨틱 레이어)**: 비즈니스 용어로 [[298_qkv_attention|쿼리]] 가능하게 [[198_abstraction_control_data_process|추상화]]
- **[[195_federated_query_data_fabric_distributed_join|Federated Query]] (연합 [[298_qkv_attention|쿼리]])**: 여러 소스를 단일 SQL로 조회

📢 **섹션 요약 비유**: [[360_data_virtualization|데이터 가상화]]는 "여러 은행 잔액을 하나의 금융 앱에서 보는 것"이다. 돈을 한 은행으로 옮기지 않아도 전체 자산 현황을 즉시 볼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 멀티클라우드 [[212_data_fabric_virtualization|데이터 패브릭]] 구현 시나리오

**시나리오: 금융그룹 멀티클라우드 통합**

```
온프레미스 Oracle ERP ─┐
AWS S3 데이터 레이크   ─┤  Data Fabric Layer  ─→  통합 BI·AI 분석
Azure Synapse DW      ─┤  (Denodo + Atlan)
GCP BigQuery          ─┘
```

| 단계 | 작업 | 기술 |
|:---|:---|:---|
| 연결 | 4개 소스 커넥터 [[009_config|설정]] | JDBC, [[156_rest_representational_state_transfer|REST]], ODBC |
| 탐색 | [[190_ai_llm_requirements_specification|AI]] 크롤러로 [[012_metadata|메타데이터]] 자동 수집 | Atlan Crawler |
| [[015_virtualization|가상화]] | 통합 뷰 [[087_process_state_transition|생성]], 푸시다운 최적화 | Denodo VQL |
| 거버넌스 | PII 자동 탐지, 마스킹 [[164_policy|정책]] 적용 | Apache Ranger |
| 서빙 | 단일 [[156_rest_representational_state_transfer|REST]] API로 소비자 제공 | [[246_graphql_query_language_overfetching_solution|GraphQL]] [[014_api_posix|API]] |

### 4-2. Gartner [[212_data_fabric_virtualization|데이터 패브릭]] 구성 요소 (2023 정의 기준)

1. **[[001_dikw_pyramid|Data]] Integration & Transformation** — 통합 [[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]] 파이프라인
2. **[[213_data_catalog_metadata|Data Catalog]] & [[012_metadata|Metadata]]** — 능동 [[342_metadata_catalog|메타데이터 카탈로그]]
3. **[[247_data_virtualization_federated_query|Data Virtualization]]** — 물리 이동 없는 가상 통합
4. **[[052_data_governance_framework|Data Governance]] & [[283_security_tactics|Security]]** — 자동화된 [[164_policy|정책]] 관리
5. **Master [[001_dikw_pyramid|Data]] [[372_management|Management]] ([[539_mdm_master_data_management|MDM]], [[051_mdm_master_data_management|마스터 데이터 관리]])** — 단일 진실 소스 유지
6. **Analytics & Insights** — 통합 [[001_dikw_pyramid|데이터]] 분석 레이어

📢 **섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]] 도입은 "여러 나라 전화망을 하나의 국제전화 시스템으로 연결하는 것"이다. 각 나라 망은 그대로지만 어디서나 통화할 수 있게 된다.

---

## Ⅴ. 기대효과 및 결론

[[212_data_fabric_virtualization|데이터 패브릭]]은 [[645_data_pipeline_acceleration|데이터 파이프라인]] 구축·유지 비용을 최소화하면서도 통합 [[292_accessibility_kwcag_wcag|접근성]]과 거버넌스를 제공한다. 특히 레거시 시스템이 많고 클라우드 마이그레이션이 점진적으로 [[216_progress_in_synchronization|진행]] 중인 대기업에 가장 적합하다.

### 기대 효과 요약

| 영역 | 기대 효과 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] [[292_accessibility_kwcag_wcag|접근성]] | 이기종 소스 단일 인터페이스 접근 |
| [[215_etl_vs_elt_pipeline|ETL]] 비용 | [[001_dikw_pyramid|데이터]] 복사 제거 → 30~50% 파이프라인 감소 |
| 거버넌스 | [[190_ai_llm_requirements_specification|AI]] 자동 [[104_classification_analysis|분류]] → 컴플라이언스 대응 속도 80% 향상 |
| 시간 절감 | [[001_dikw_pyramid|데이터]] 탐색·이해 시간 70% 단축 |

기술사 시험에서 [[212_data_fabric_virtualization|데이터 패브릭]]은 **"능동 [[012_metadata|메타데이터]]([[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]])와 [[360_data_virtualization|데이터 가상화]]([[247_data_virtualization_federated_query|Data Virtualization]])가 핵심 차별점"** 임을 중심으로 설명해야 한다.

📢 **섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]]의 최종 목표는 "모든 직원이 회사 어딘 [[001_dikw_pyramid|데이터]]든 구글 검색하듯 찾아 쓸 수 있는 세상"을 만드는 것이다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기술 | [[247_data_virtualization_federated_query|Data Virtualization]] ([[360_data_virtualization|데이터 가상화]]) | 물리 이동 없는 통합 [[298_qkv_attention|쿼리]] |
| 핵심 기술 | [[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]] (능동 [[012_metadata|메타데이터]]) | [[190_ai_llm_requirements_specification|AI]] 기반 자동 탐색·[[104_classification_analysis|분류]] |
| 핵심 기술 | [[160_knowledge_graph_graphrag_integration|Knowledge Graph]] ([[160_knowledge_graph_graphrag_integration|지식 그래프]]) | [[001_dikw_pyramid|데이터]] [[083_relationship_in_er_model|관계]]·리니지 표현 |
| 비교 | [[320_data_mesh|Data Mesh]] ([[211_data_mesh_domain_ownership|데이터 메시]]) | 조직 중심 [[136_variance|분산]] 아키텍처 |
| 비교 | [[208_data_lake_schema_on_read|Data Lake]] ([[208_data_lake_schema_on_read|데이터 레이크]]) | 물리 집중 저장소 |
| 도구 | Denodo / Dremio | [[360_data_virtualization|데이터 가상화]] 플랫폼 |
| 도구 | Atlan / Alation | [[190_ai_llm_requirements_specification|AI]] [[342_metadata_catalog|메타데이터 카탈로그]] |
| 표준 | Gartner [[212_data_fabric_virtualization|Data Fabric]] Definition | 산업 표준 정의 |
| 연관 | [[213_data_catalog_metadata|Data Catalog]] ([[213_data_catalog_metadata|데이터 카탈로그]]) | [[012_metadata|메타데이터]] 탐색·관리 |
| 연관 | [[539_mdm_master_data_management|MDM]] (Master [[001_dikw_pyramid|Data]] [[372_management|Management]]) | [[539_mdm_master_data_management|마스터 데이터]] [[194_consistency_database_integrity|일관성]] 관리 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 도서관의 책을 한 곳으로 모으지 않고, 통합 검색 앱 하나만 만들어서 어느 도서관 책이든 검색하고 빌릴 수 있게 하는 것이 [[212_data_fabric_virtualization|데이터 패브릭]]이다.

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 사일로 (시스템 간 단절)
    │
    ▼
Data Fabric: 메타데이터 기반 통합 · 가상화
    ├─► 메타데이터 자동 수집 · AI 기반 추천
    ├─► 데이터 가상화: 물리 이동 없이 접근
    └─► 통합 거버넌스 · 보안 정책
    │
    ▼
Data Mesh와 상호 보완 관계
```
2. 앱이 새 책을 자동으로 인식하고 장르·내용을 AI가 [[104_classification_analysis|분류]]해 주는 것이 능동 [[012_metadata|메타데이터]] 기능이다.
3. 각 도서관의 규칙(거버넌스)은 그대로지만, 앱이 어느 책이 어린이용인지 성인용인지 자동으로 알아서 접근을 통제해준다.
