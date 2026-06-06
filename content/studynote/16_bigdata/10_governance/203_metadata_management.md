---
title: "203. Metadata Management"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)([Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/))는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 관한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"로, 비즈니스 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)(의미), 기술 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)(구조), 운영 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)(이력)의 3계층으로 구성되며 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색성·계보·거버넌스의 기반이다.
- **가치**: [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) 개념의 등장으로 ML이 자동으로 PII(개인식별정보)를 태깅하고, 사용 빈도 기반 인기도 점수를 부여하는 등 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리가 수동 작업에서 지능형 자동화로 진화하고 있다.
- **판단 포인트**: DataHub(LinkedIn [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/))·OpenMetadata·Apache Atlas([Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)) 중 기술 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 생태계 연동 요구사항에 따라 선택하되, 표준(Dublin Core, DCAT)을 준수하면 도구 변경 시 이식성이 보장된다.

---

## Ⅰ. 개요 및 필요성

[메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)([Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/))는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 <a href="/studynote/02_operating_system/01_overview_architecture/033_context/">컨텍스트</a>(<a href="/studynote/02_operating_system/01_overview_architecture/033_context/">Context</a>)를 제공하는 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>다. "고객 테이블의 age 컬럼"이라는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체보다, "이 컬럼이 만 나이인지 세는 나이인지, 언제 마지막으로 업데이트되었는지, 누가 소유하는지, PII인지"를 알려주는 것이 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)다.

### [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 없이 발생하는 문제

- <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 탐색 비용</strong>: 분석가가 "어떤 테이블에 고객 구매 이력이 있나?"를 파악하는 데 수일 소요
- **의미 혼란**: 같은 이름의 컬럼이 시스템마다 다른 의미로 사용
- **컴플라이언스 실패**: 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 PII인지 파악 불가 -> [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 위반 위험
- <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 계보 부재</strong>: ML 모델이 어떤 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 훈련되었는지 추적 불가

**📢 섹션 요약 비유**: [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)는 <strong>도서관의 카드 목록</strong>이다. 책([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 아무리 많아도 카드 목록([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)) 없이는 원하는 책을 찾을 수 없고, 책의 내용·저자·출판연도를 알 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 3계층 아키텍처

```
+--------------------------------------------------------------+
|                  메타데이터 3계층 구조                        |
+--------------------------------------------------------------+
|                                                              |
|  1. 비즈니스 메타데이터 (Business Metadata)                   |
|  +--------------------------------------------------------+  |
|  | • 비즈니스 용어 정의 (예: "활성 고객" = 최근 30일 로그인)|  |
|  | • 데이터 소유자 정보 (Owner: CMO)                       |  |
|  | • 사용 정책 (누가 어떤 목적으로 사용 가능)              |  |
|  | • 데이터 분류 (기밀/내부/공개)                          |  |
|  | • PII 플래그 (이 컬럼은 개인식별정보)                  |  |
|  +--------------------------------------------------------+  |
|                                                              |
|  2. 기술 메타데이터 (Technical Metadata)                      |
|  +--------------------------------------------------------+  |
|  | • 스키마: 테이블명, 컬럼명, 데이터 타입                 |  |
|  | • 파티셔닝: 파티션 키, 파티션 수                        |  |
|  | • 인덱스: 인덱스 컬럼, 인덱스 유형                      |  |
|  | • 외래키: 참조 관계, 조인 경로                          |  |
|  | • 파일 포맷: Parquet/ORC/CSV, 압축 코덱                 |  |
|  +--------------------------------------------------------+  |
|                                                              |
|  3. 운영 메타데이터 (Operational Metadata)                    |
|  +--------------------------------------------------------+  |
|  | • 마지막 업데이트 타임스탬프                            |  |
|  | • ETL 잡 실행 이력 (성공/실패, 소요 시간)               |  |
|  | • 레코드 수 히스토리 (볼륨 추이)                        |  |
|  | • 데이터 품질 점수 이력                                 |  |
|  | • 데이터 계보 잡 정보 (어느 ETL이 생성했는지)           |  |
|  +--------------------------------------------------------+  |
+--------------------------------------------------------------+
```

### [메타데이터 카탈로그](/studynote/05_database/06_dw_olap_trends/342_metadata_catalog/) 도구 비교

| 도구 | 유형 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| **DataHub** (LinkedIn) | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | [GraphQL](/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [푸시 기반](/studynote/15_devops_sre/02_cicd_gitops/087_push_based_deployment_jenkins_ci_cd_security_risk/) [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집, 활발한 커뮤니티 | 범용, [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경 |
| **OpenMetadata** | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 통합 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 플랫폼, 품질·계보·협업 통합 | 스타트업·중견기업 |
| **Apache Atlas** | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | HCatalog 기반, [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/[Hive](/studynote/05_database/04_transactions_concurrency/544_hive/) 네이티브 | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 |
| **Alation** | 상용 | [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/), [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 기반 자동 태깅, 협업 | 대기업 |
| **Collibra** | 상용 | 엔터프라이즈 거버넌스 전문, 워크플로우 강점 | 규제 산업 |

**📢 섹션 요약 비유**: [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 3계층은 **사람의 신원 정보** 3종이다. 비즈니스 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) = 이름·직업·성격(의미), 기술 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) = 혈액형·신장·체중(구조), 운영 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) = 진료 이력·방문 기록(이력). 세 정보가 모여야 그 사람([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 완전히 이해할 수 있다.

---

## Ⅲ. 비교 및 연결

### [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/): 지능형 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리

<strong><a href="/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/">Active</a> <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">Metadata</a></strong>는 Atlan, Alation 등이 제창하는 개념으로, 정적으로 관리되던 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 ML이 동적으로 발전시키는 방식이다:

| 기존 Passive [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) | [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) |
|:---|:---|
| 수동 태깅 | ML 기반 자동 PII 감지·태깅 |
| 정적 문서 | 사용 패턴 기반 자동 인기도 점수 |
| 고정된 비즈니스 정의 | 자동 유사 용어 추천 |
| 수동 계보 작성 | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/)으로 자동 계보 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

### [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 표준

| 표준 | 적용 영역 |
|:---|:---|
| **Dublin Core** | 웹 자원·문서 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) (15개 기본 요소) |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/505_schema/">Schema</a>.org</strong> | 웹 크롤러를 위한 구조화된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **OWL (Web Ontology Language)** | [시맨틱 웹](/studynote/06_ict_convergence/01_blockchain/003_semantic_web/) 온톨로지 정의 |
| <strong>DCAT (<a href="/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">Data Catalog</a> Vocabulary)</strong> | W3C [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) [상호운용성](/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/) 표준 |

**📢 섹션 요약 비유**: [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Metadata는 <strong>Netflix 추천 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>과 같다. 사용자 시청 이력([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사용 패턴)을 분석해 자동으로 다음에 볼 영상(관련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋)을 추천하고, 콘텐츠를 자동 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집 방식

```
소스 시스템 -> 메타데이터 카탈로그

방식 1: 푸시(Push) 기반
  데이터 파이프라인이 실행 시 메타데이터를 카탈로그 API로 전송
  예: OpenLineage -> DataHub
  장점: 실시간성 높음, 이벤트 기반

방식 2: 풀(Pull) 기반 크롤링
  카탈로그가 소스 시스템에 주기적으로 접속해 스키마·통계 수집
  예: DataHub Ingestion Framework -> BigQuery, Snowflake 크롤링
  장점: 소스 시스템 변경 없음

방식 3: 하이브리드
  중요 이벤트는 푸시, 스키마 변경 감지는 풀 크롤링
```

### DataHub 아키텍처 특징

DataHub(LinkedIn [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 현 Acryl [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 <strong><a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 이벤트 스트리밍</strong> 기반으로 설계되었다. Kafka를 통해 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 변경 이벤트를 실시간 스트리밍하고, 검색은 [Elasticsearch](/studynote/05_database/05_distributed_nosql_newsql/302_cdc/), 저장은 MySQL/PostgreSQL을 사용한다.

**📢 섹션 요약 비유**: DataHub는 <strong>실시간 뉴스 피드</strong>와 같다. [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에서 변경이 일어날 때마다 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 뉴스가 Kafka를 통해 실시간으로 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)에 전달된다.

---

## Ⅴ. 기대효과 및 결론

### [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리 성과 지표

| 항목 | 효과 |
|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/">탐색 시간</a></strong> | 수일 -> 수분 단축 ([카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) 검색) |
| <strong>PII <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 파악</strong> | 수동 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 수주 -> 자동 탐지 수시간 |
| **신규 분석가 온보딩** | 2주 -> 3일 단축 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 계보 파악</strong> | 불가 -> 클릭 한 번에 상·하류 추적 |

### 결론

[메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리는 <strong><a href="/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a>의 기초 인프라</strong>다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 찾고(탐색성), 이해하고(비즈니스 정의), 신뢰하고(품질·계보), [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는(PII 태깅) 모든 활동의 기반이 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)다. [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) 기술의 발전으로 수동 관리 부담이 크게 줄어들고 있으며, 정보통신기술사는 이 기술 변화를 거버넌스 설계에 반영해야 한다.

**📢 섹션 요약 비유**: [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리 없는 빅데이터 플랫폼은 <strong>목차 없는 백과사전</strong>이다. 정보가 있어도 찾을 수 없고, 어떤 내용인지 알 수 없고, 믿을 수 있는지도 모른다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 저장소 | 비즈니스/기술/운영 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 통합 관리 플랫폼 |
| DataHub | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) | LinkedIn 개발, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반 실시간 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) |
| Apache Atlas | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) | HCatalog 기반 [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) |
| [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/) | 지능형 관리 | ML 기반 자동 태깅·추천·이상 감지 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 | 운영 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 잡 실행 이력·변환 경로 추적 |
| DCAT | 표준 | W3C [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) [상호운용성](/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/) 어휘 |
| PII | 비즈니스 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 항목 | 개인식별정보 여부 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[메타데이터 (Metadata) — 데이터의 의미·구조·출처·품질을 설명하는 데이터]
    |
    v
[메타데이터 관리 (Metadata Management) — 기술·비즈니스·운영 메타데이터 중앙 관리]
    |
    v
[데이터 카탈로그 (Data Catalog) — 비즈니스 용어 사전 + 데이터 계보 + 검색 기능]
    |
    v
[데이터 계보 (Data Lineage) — 데이터의 출처·변환·흐름 추적으로 신뢰성 확보]
    |
    v
[능동형 메타데이터 (Active Metadata) — AI 기반 자동 태깅·추천·품질 모니터링]
```

이 흐름은 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리가 기술적 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리에서 비즈니스 의미와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보를 포함한 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)로 발전하고, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 능동형 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 관리로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)는 <strong>책 표지와 목차</strong>예요: 책의 내용([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))뿐 아니라 제목, 저자, 출판 날짜, 어떤 내용인지([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/))가 있어야 원하는 책을 빠르게 찾을 수 있어요.
- 비즈니스 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)는 "이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 무슨 의미인지", 기술 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)는 "이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어떻게 저장되어 있는지", 운영 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)는 "언제 만들어지고 어떻게 사용되었는지"를 알려줘요.
- [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 <strong>디지털 도서관 목록 시스템</strong>이에요: 검색창에 "고객"을 치면 고객 관련 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋이 나오고, 누가 소유하고, 어떻게 써야 하는지까지 바로 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 203 / 262

<- **이전**: [196. 데이터 품질 관리 도구 (Data Quality Tools) — Great Expectations/Deequ/Soda Core](/studynote/16_bigdata/10_governance/202_data_quality_tools/)
**다음**: [198. 마스터 데이터 관리 (MDM, Master Data Management) — 황금 레코드 생성](/studynote/16_bigdata/10_governance/204_mdm/) ->

---
