+++
title = "224. 데이터 리니지 (Data Lineage) 흐름 족보 카탈로그 태그 거버넌스"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)([Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디서 왔고(Origin), 어떻게 변환됐고(Transformation), 어디로 흘러갔는지(Destination)를 추적하는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 족보"로, 신뢰할 수 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석의 전제조건이다.
> 2. **가치**: 컬럼 레벨 리니지(Column-Level Lineage)와 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) 통합을 통해 [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[CCPA](/knowledge-base/studynote/09_security/16_data_privacy/800_ccpa/) 컴플라이언스 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응, 장애 근본 원인 분석, 중복 파이프라인 제거가 가능해진다.
> 3. **판단 포인트**: 리니지 자동화 수준이 낮으면 거버넌스는 문서화에 그치고 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 보장은 어렵다. 도구 선택 시 자동 크롤링·컬럼 레벨 추적·[그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 시각화를 반드시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

---

## Ⅰ. 개요 및 필요성

### [데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)가 필요한 이유

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가가 "이 매출 수치가 왜 어제와 다르냐"라는 질문을 받았을 때, 리니지 없이는 수십 개 파이프라인을 수동으로 추적해야 한다. 반면 리니지 시스템이 있으면 [그래프 탐색](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/613_graph_bfs_memory/) 한 번으로 원인 파이프라인을 찾을 수 있다.

| 필요 상황 | 리니지 없을 때 | 리니지 있을 때 |
|:---|:---|:---|
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 삭제 요청 | 어느 시스템에 퍼졌는지 불명확 | 컬럼 리니지로 전파 경로 즉시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 이슈 | 수동 파이프라인 역추적 (수 시간) | [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 역방향 탐색 (수 분) |
| [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | 영향 범위 파악 불가 | 다운스트림 의존 즉시 파악 |
| [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) ([Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/)) | 증거 자료 수동 수집 | 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 리포트 제출 |

📢 **섹션 요약 비유**: [데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)는 "식품 이력 추적제"다. 내 식탁에 오른 쇠고기가 어느 농장 → 어느 도축장 → 어느 가공 공장을 거쳤는지 QR 하나로 추적하는 것처럼, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 출처·변환 이력을 추적한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 리니지 유형: 테이블 vs 컬럼 레벨

```
[테이블 레벨 리니지 (Coarse-Grained)]
raw_orders ──→ stg_orders ──→ int_revenue ──→ fct_daily_revenue

[컬럼 레벨 리니지 (Column-Level Lineage, 세밀)]
raw_orders.order_amount
    │
    ▼  (SUM + ROUND)
int_revenue.revenue_usd
    │
    ▼  (GROUP BY date)
fct_daily_revenue.daily_total
    │
    ▼  (JOIN + SELECT)
rpt_executive_dashboard.revenue_kpi
```

컬럼 레벨 리니지가 중요한 이유: GDPR에서 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 컬럼(예: `user_email`)이 어느 파생 테이블·BI 뷰에까지 전파됐는지 알아야 삭제 요청을 완전히 이행할 수 있다.

### 2-2. [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) 구성 요소

| 구성 요소 | 설명 |
|:---|:---|
| [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) Repository ([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 저장소) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·통계·소유자·태그 저장 |
| Lineage [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/) (리니지 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름 방향성 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| Business Glossary (비즈니스 용어집) | 기술 용어 ↔ 비즈니스 용어 매핑 |
| Tag & [Classification](/knowledge-base/studynote/12_it_management/03_ea_isp/107_classification/) (태그·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)) | PII·SENSITIVE·PUBLIC 등 레이블 |
| Search & Discovery (검색·탐색) | 풀텍스트 검색, 추천 |
| [Data Quality](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/) [Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/) (품질 지표) | 완전성·[정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)·적시성 점수 |

### 2-3. 주요 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 도구 비교

```
┌──────────────────────────────────────────────────────────────┐
│  Apache Atlas           │  오픈소스, HBase·Hive 강결합        │
│  (아파치 아틀라스)       │  태그 기반 분류, 정책 연동(Ranger)   │
├──────────────────────────────────────────────────────────────┤
│  Amundsen               │  Lyft 오픈소스, 검색·탐색 최적화    │
│  (아문센)               │  Neo4j 기반 메타데이터 그래프        │
├──────────────────────────────────────────────────────────────┤
│  DataHub                │  LinkedIn 오픈소스, 푸시·풀 수집    │
│  (데이터허브)           │  GraphQL API, 플러그인 생태계 풍부   │
├──────────────────────────────────────────────────────────────┤
│  Alation / Atlan        │  상용, AI 기반 추천·자동 분류        │
│  (앨레이션 / 아틀란)    │  Data Fabric 통합 지원               │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 "회사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 도서관"이다. 어떤 책(테이블)이 있고, 누가 썼고(오너), 어떤 내용이고([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)), 어느 책에서 파생됐는지(리니지)를 모두 기록한다.

---

## Ⅲ. 비교 및 연결

### 3-1. 태그 기반 [데이터 분류](/knowledge-base/studynote/09_security/16_data_privacy/808_data_classification/) 체계

```
데이터 분류 태그 계층
┌─────────────────────────────────────────────┐
│ 민감도 (Sensitivity)                        │
│   PUBLIC → INTERNAL → CONFIDENTIAL → SECRET │
├─────────────────────────────────────────────┤
│ 개인정보 (Privacy)                          │
│   PII (개인식별정보) → PHI (건강정보)        │
│   → PCI (카드정보) → Non-PII               │
├─────────────────────────────────────────────┤
│ 품질 (Quality)                              │
│   GOLDEN (황금 데이터) → TRUSTED → RAW      │
├─────────────────────────────────────────────┤
│ 도메인 (Domain)                             │
│   ORDER · CUSTOMER · PRODUCT · FINANCE      │
└─────────────────────────────────────────────┘
```

### 3-2. [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·CCPA와 리니지 연계

| 규제 | 요구사항 | 리니지 역할 |
|:---|:---|:---|
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/). 17 (잊혀질 권리) | [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 완전 삭제 | PII 컬럼 전파 경로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 삭제 |
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/). 30 (처리 기록 의무) | 처리 활동 기록 | 리니지 = 자동 처리 활동 기록 |
| [CCPA](/knowledge-base/studynote/09_security/16_data_privacy/800_ccpa/) (캘리포니아 소비자 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)법) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 판매 경로 공개 | [3rd Party](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 전달 리니지 추적 |
| [SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/855_soc_2/) Type II | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 | [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 접근 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) + 리니지 |

📢 **섹션 요약 비유**: 리니지와 컴플라이언스의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 "약품 유통 이력 시스템"과 같다. 리콜이 발생하면 그 약이 어느 병원·약국까지 배포됐는지 즉시 추적해야 하듯, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 유출 시 영향 범위를 즉시 파악해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. dbt([data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) build tool) 기반 리니지 자동화

dbt([data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) build tool, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 빌드 툴)는 SQL 변환 모델 간 의존관계에서 리니지를 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.

```
dbt 프로젝트 DAG (Directed Acyclic Graph, 방향성 비순환 그래프)
raw_orders ─┐
raw_customers─┤─→ stg_orders ─→ int_order_enriched ─→ fct_orders
raw_products ─┘         ↑                                    │
                   컬럼 리니지 자동 추적                      │
                                                             ▼
                                                    BI 대시보드
```

### 4-2. 리니지 도입 로드맵

| 단계 | 작업 | 산출물 |
|:---|:---|:---|
| 1단계 테이블 리니지 | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 파이프라인 소스·타깃 자동 수집 | 테이블 의존 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| 2단계 컬럼 리니지 | SQL 파싱으로 컬럼 단위 추적 | 컬럼 전파 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| 3단계 비즈니스 리니지 | 비즈니스 용어집 연계, 오너 지정 | [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능 리포트 |
| 4단계 자동화 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), 실시간 리니지 갱신 | 자동 컴플라이언스 증적 |

📢 **섹션 요약 비유**: 리니지 자동화는 "GPS 내비게이션이 실시간으로 지도를 갱신하는 것"이다. 새 도로(파이프라인)가 생기면 자동으로 경로 지도(리니지 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/))가 업데이트된다.

---

## Ⅴ. 기대효과 및 결론

[데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)는 단순한 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 도구가 아니라, <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Trust)의 근간</strong>이다. 리니지가 없으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제의 근본 원인을 찾지 못하고, 컴플라이언스 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)에서 증거를 제출하지 못한다.

### [핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/)

| [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) | 기대 효과 |
|:---|:---|
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 삭제 요청 처리 시간 | 수 일 → 수 시간 단축 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 이슈 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) | 80% 단축 (근본 원인 즉시 파악) |
| [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 증적 제출 시간 | 수동 → 자동 리포트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 중복 파이프라인 발견 | 리니지 분석으로 20~30% 중복 제거 |

기술사 시험에서 [데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)는 <strong>"컬럼 레벨 추적과 <a href="/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a> 연계"</strong> 를 중심으로, [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 도구(Atlas·DataHub·Amundsen)별 특성을 비교 설명할 수 있어야 한다.

📢 **섹션 요약 비유**: 완성된 [데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/) 시스템은 "모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입자에 GPS 추적기가 달린 것"이다. 어디서 왔고 어디로 가는지, 어떻게 변했는지를 항상 알 수 있다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 유형 | Table-Level Lineage (테이블 리니지) | 테이블 단위 흐름 추적 |
| 유형 | Column-Level Lineage (컬럼 리니지) | 컬럼 단위 세밀 추적 |
| 도구 | Apache Atlas (아파치 아틀라스) | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) |
| 도구 | DataHub ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)허브) | LinkedIn [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) |
| 도구 | Amundsen (아문센) | Lyft 검색 최적화 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) |
| 규제 연계 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) (유럽 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 규정) | 잊혀질 권리, 처리 기록 의무 |
| 규제 연계 | [CCPA](/knowledge-base/studynote/09_security/16_data_privacy/800_ccpa/) (캘리포니아 소비자 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)법) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 판매 경로 공개 |
| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | PII (Personally Identifiable Information) | 개인식별정보 태그 |
| 자동화 | dbt ([data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) build tool) | SQL 의존관계 자동 리니지 |
| 연관 | [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) / [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) | 리니지를 거버넌스 기반으로 활용 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 슈퍼에서 파는 쌀이 어느 농장에서 왔는지, 어느 창고를 거쳐 왔는지 QR코드로 알 수 있는 것처럼, [데이터 리니지](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 출처와 여정을 추적한다.

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 출처 불명 (신뢰 부족)
    │
    ▼
데이터 리니지: 원본 → 변환 → 소비 경로 추적
    │
    ▼
데이터 카탈로그: 메타데이터 · 태깅 · 검색
    │
    ▼
도구: DataHub · Amundsen · OpenLineage · Atlas
```
2. 이 정보가 있으면 "이 분석 결과가 왜 틀렸지?"라는 질문에 원재료(원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))부터 조리 과정(변환)까지 바로 찾아볼 수 있다.
3. 특히 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)법([GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)) 위반 시 "이 정보가 어디까지 퍼졌나"를 즉시 추적할 수 있어 법적 책임을 다할 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 224 / 258

← **이전**: [223. 데이터 패브릭 (Data Fabric) 메타데이터 가상화 AI 통합](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/223_data_fabric_metadata_virtualization_integration/)
**다음**: [225. KDD (Knowledge Discovery in Databases) T검정 ANOVA 통계 분석](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/225_kdd_t_test_anova_statistical_analysis/) →

---
