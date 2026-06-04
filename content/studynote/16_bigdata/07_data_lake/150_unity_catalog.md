+++
title = "150. Unity Catalog (Databricks) — 레이크하우스 통합 거버넌스"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. Unity Catalog는 Databricks의 통합 거버넌스 솔루션으로, <strong>3-수준 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/">네임스페이스</a>(<a href="/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/">catalog</a>.<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/">schema</a>.table)</strong>를 통해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·ML 모델·[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 단일 제어 지점에서 관리한다.
2. <strong>컬럼/행 수준의 세밀한 접근 제어(<a href="/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/">Fine-Grained</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/">Access Control</a>)</strong>, <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">데이터 리니지</a> 자동 추적</strong>, <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a></strong>를 제공하여 [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/), [HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/), SOC2 규정 준수를 지원한다.
3. <strong>Delta Sharing</strong>은 Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 위의 오픈 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사하지 않고 다른 클라우드·플랫폼의 소비자와 안전하게 공유할 수 있다.

---

## Ⅰ. 개요 및 필요성

Databricks의 기존 거버넌스 체계는 각 워크스페이스마다 독립적인 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) Metastore를 사용하는 구조였다. 이 구조는 멀티 워크스페이스 환경에서 테이블 중복 등록, 접근 권한 불일치, 리니지 단절 등 관리 복잡성을 야기했다.

2022년 출시된 Unity Catalog는 Account 레벨의 단일 메타스토어로 이 문제를 해결한다. 모든 워크스페이스가 동일한 Unity Catalog를 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하므로 거버넌스 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 전사에 일관되게 적용된다.

| 거버넌스 요구사항 | [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) Metastore (기존) | Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) |
|:---|:---|:---|
| 접근 제어 단위 | 테이블 수준 | 컬럼·행 수준 |
| 리니지 추적 | 없음 | 자동 추적 (컬럼 단위) |
| 멀티 워크스페이스 | 워크스페이스별 분리 | 단일 Account 메타스토어 |
| [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 기본 없음 | 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 기록 |
| 외부 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) | 별도 구현 필요 | Delta Sharing 내장 |

> 📢 **섹션 요약 비유**: 기존 방식은 각 부서마다 자체 자물쇠와 열쇠를 관리하던 방식이었다면, Unity Catalog는 전사 통합 [스마트 카드](/knowledge-base/studynote/09_security/12_identity_threat_advanced/607_smart_card/) 시스템으로 누가 언제 어느 방에 들어갔는지 모두 기록된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|                Unity Catalog 3-수준 네임스페이스                  |
+------------------------------------------------------------------+
|  [Account 메타스토어]                                             |
|       |                                                          |
|       +-- catalog_prod          (Catalog 수준)                   |
|       |       +-- sales         (Schema 수준)                    |
|       |       |     +-- orders  (Table / View / Volume)          |
|       |       |     +-- customers                               |
|       |       +-- marketing                                      |
|       |             +-- campaigns                               |
|       |                                                          |
|       +-- catalog_dev           (개발용 Catalog)                 |
|                                                                  |
|  [접근 제어 레이어]                                               |
|  +----------------------------------------------------------+   |
|  |  GRANT SELECT ON TABLE catalog.schema.table TO group_a   |   |
|  |  CREATE ROW FILTER ON TABLE orders (dept = current_user) |   |
|  |  CREATE COLUMN MASK ON TABLE users (ssn -> 'XXXX')        |   |
|  +----------------------------------------------------------+   |
|                                                                  |
|  [Delta Sharing]                                                 |
|  +---------------+   공유   +------------------------------+   |
|  | Unity Catalog  | -------> | 외부 소비자 (Snowflake / R / |   |
|  | (공유자)       |         |  Pandas / Power BI)          |   |
|  +---------------+         +------------------------------+   |
+------------------------------------------------------------------+
```

**핵심 기능 요약**

| 기능 | 설명 | 적용 레벨 |
|:---|:---|:---|
| [Fine-Grained](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/) Access | 컬럼 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹, 행 필터링 | 컬럼·행 수준 |
| [Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/) | SQL 파싱으로 컬럼 리니지 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 컬럼 단위 |
| [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/) Log | 모든 [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/)/[DML](/knowledge-base/studynote/12_it_management/02_itsm_itil/083_dml/) 이벤트 기록 | 테이블 접근 |
| Delta Sharing | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 없이 외부 공유 | 테이블 |
| Volumes | 비정형 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(CSV, 이미지 등) 거버넌스 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수준 |
| [Model Registry](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) | ML 모델 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 통합 | ML 모델 |

> 📢 **섹션 요약 비유**: Unity Catalog는 병원 의료정보 시스템과 같다. 의사·간호사·행정직 모두 같은 시스템을 쓰되, 각자 볼 수 있는 진료 기록이 다르게 제한되고, 누가 언제 어떤 기록을 봤는지 모두 남는다.

---

## Ⅲ. 비교 및 연결

<strong>Unity <a href="/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/">Catalog</a> vs 경쟁 거버넌스 솔루션</strong>

| 항목 | Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) | AWS Lake Formation | Apache Atlas |
|:---|:---|:---|:---|
| 플랫폼 | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) | AWS 전용 | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |
| 접근 제어 | 컬럼·행 수준 | 컬럼 수준 | 테이블 수준 |
| 리니지 | 자동 (SQL 파싱) | 제한적 | 수동 등록 가능 |
| ML 모델 관리 | 내장 ([MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) 통합) | 없음 | 없음 |
| 외부 공유 | Delta Sharing | Cross-account S3 | 없음 |
| 설치·운영 | 완전 관리형 | 완전 관리형 | 자체 설치 |

**연관 기술 연결**

- <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/">Delta Lake</a></strong>: Unity Catalog가 관리하는 테이블의 기본 저장 포맷
- <strong><a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/">MLflow</a></strong>: Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 내 [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)로 통합
- <strong><a href="/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/">Databricks</a> SQL</strong>: Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 권한을 기반으로 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 실행
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a></strong>: Unity Catalog가 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 연합 거버넌스 방식으로 관리하는 인프라

> 📢 **섹션 요약 비유**: Unity Catalog는 회사의 정보보안팀 역할이다. 누가 어떤 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 봐도 되는지 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 관리하고, 외부 협력사와 자료를 공유할 때도 보안 채널(Delta Sharing)을 통해서만 허용한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**도입 시나리오**

- <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a> <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong>: 주민등록번호 컬럼 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 + 특정 부서만 복호화 권한 부여
- **멀티 팀 거버넌스**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 팀은 Silver 레이어 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 분석 팀은 Gold 레이어 읽기만 허용
- <strong>규정 <a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a></strong>: SOC2 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 시 Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/) Log로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 이력 제출
- <strong>외부 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 판매</strong>: Delta Sharing으로 고객사에 실시간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 피드 제공 (복사 없음)

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 3-수준 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 의미 | [catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)(조직/환경 구분) -> [schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/)([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)) -> table(오브젝트) |
| [Fine-Grained](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/) [AC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/) 구현 | ROW FILTER 함수 + COLUMN MASK [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 동적 적용 |
| Delta Sharing 원리 | 서버가 서명된 URL 발급, 소비자가 직접 스토리지 읽기 (복사 없음) |
| 리니지 추적 방식 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 실행 시 SQL 파싱 -> 컬럼 -> 컬럼 매핑 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

> 📢 **섹션 요약 비유**: Unity [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 운영은 마치 건물 출입 통제와 같다. 각 방(테이블)마다 카드키 권한을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하고, 특정 서류(컬럼)는 권한자에게만 보이며, 모든 출입 기록은 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)([감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))로 남는다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 거버넌스 일원화 | 워크스페이스별 파편화된 권한 관리 -> 단일 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 관리 |
| 규정 준수 자동화 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/) 컬럼 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹을 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 선언, 운영 오버헤드 최소화 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | 리니지 추적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제 원인 신속 파악 |
| [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 활성화 | Delta Sharing으로 복사 없는 안전한 외부 공유 실현 |

Unity Catalog는 [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 플랫폼 위에서 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)를 완성하는 핵심 레이어다. [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mesh의 연합 거버넌스 원칙을 기술적으로 구현하는 도구로서, 2024년 이후 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심 조직에서 빠르게 채택되고 있다. 기술사 시험에서는 <strong>3-수준 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/">네임스페이스</a></strong>, <strong><a href="/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/">Fine-Grained</a> 접근 제어 (ROW FILTER + COLUMN MASK)</strong>, <strong>Delta Sharing 원리</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Unity Catalog는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 왕국의 법전이다. 왕국의 모든 창고(테이블)에 대한 법(권한)이 한 권의 책으로 통합되어 있고, 무엇이든 꺼내거나 넣을 때마다 법에 따라 자동으로 허가 여부가 결정된다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| 3-수준 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) | 핵심 구조 | [catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/).[schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/).table 계층 |
| ROW FILTER | 행 수준 접근 제어 | 동적 행 필터링 함수 |
| COLUMN MASK | 컬럼 수준 접근 제어 | 민감 컬럼 동적 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 |
| Delta Sharing | 외부 공유 | 오픈 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 없음 |
| [Data Lineage](/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/) | 추적 기능 | SQL 파싱 기반 자동 컬럼 리니지 |
| [MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/) 통합 | ML 거버넌스 | [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)를 Unity Catalog에서 관리 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[분산 데이터 사일로 (Data Silo) — 거버넌스 부재]
    |
    v
[데이터 카탈로그 (Data Catalog) — 메타데이터 관리]
    |
    v
[Unity Catalog — 3-수준 네임스페이스 (catalog.schema.table)]
    |
    v
[행/컬럼 수준 접근 제어 (Row Filter / Column Mask)]
    |
    v
[Delta Sharing — 오픈 프로토콜 안전 데이터 공유]
```

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)에서 중앙화된 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)와 세분화된 접근 제어를 거쳐 안전한 외부 공유로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. Unity Catalog는 학교 도서관에서 학생마다 빌릴 수 있는 책이 다르게 정해진 도서관 카드 시스템이에요.
2. 비밀 책(민감 컬럼)은 특별 카드를 가진 사람만 볼 수 있고, 누가 어느 책을 빌렸는지 모두 기록돼요.
3. 다른 학교(외부 소비자)와 책을 나눌 때도 사진만 보내고 원본은 여기에 안전하게 보관된답니다(Delta Sharing).

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 150 / 262

<- **이전**: [149. Apache Hudi (Hadoop Upserts Deletes Incrementals) — CDC 지원 레이크](/knowledge-base/studynote/16_bigdata/07_data_lake/149_apache_hudi/)
**다음**: [151. 다중 계층 아키텍처 (Multi-Tier Architecture) — Bronze/Silver/Gold](/knowledge-base/studynote/16_bigdata/07_data_lake/151_multi_tier_architecture/) ->

---
