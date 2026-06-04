+++
title = "306. 데이터 거버넌스 3요소 원칙 조직 프로세스 IT시스템 (Data Governance)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기업 자산으로 관리하는 원칙([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))·조직(역할)·프로세스+IT 시스템의 3요소 체계다.
> 2. **가치**: [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/)-DMBOK ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/) Body of Knowledge) 기반 거버넌스 도입 기업은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 인시던트 50~70% 감소와 규제 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응 시간 60% 단축을 경험한다.
> 3. **판단 포인트**: [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))가 없으면 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디 있는지 모르는 "[데이터 늪](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/))"이 되어 모든 거버넌스 활동이 무력화된다.

## Ⅰ. 개요 및 필요성

기업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 급증하면서 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 많은데 믿을 수 없다", "어디 있는지 모른다", "누가 책임자인지 모른다"는 문제가 만연해졌다.
[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)([Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)·보안·[사용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/286_usability_tactics/)을 확보하기 위한 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 조직, 프로세스, IT 시스템의 통합 프레임워크다.

국제 표준 [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/)-DMBOK는 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)를 11개 지식 영역의 중심에 위치시키며, 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 활동의 방향을 결정하는 상위 프레임워크로 정의한다.

[데이터 거버넌스 3요소](/knowledge-base/studynote/05_database/04_transactions_concurrency/522_group_by/):
1. **원칙(Principles)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/), [데이터 분류](/knowledge-base/studynote/09_security/16_data_privacy/808_data_classification/) 기준
2. **조직(Organization)**: [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) ([Chief Data Officer](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/)), [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/), [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/), [Data Governance Council](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/246_data_governance_council_operation/)
3. **프로세스+IT 시스템**: [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/), [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보, 품질 측정

📢 **섹션 요약 비유**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 도서관 운영 체계다. 규칙(원칙), 사서(조직), 도서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 시스템(프로세스+IT)이 갖춰져야 어떤 책이 어디 있는지 믿고 찾을 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리

### 거버넌스 조직 구조

| 역할 | 책임 범위 | 주요 활동 |
|:---|:---|:---|
| [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) ([Chief Data Officer](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/)) | 전사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 거버넌스 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 승인, 이사회 보고 |
| [Data Governance Council](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/246_data_governance_council_operation/) | 부서 간 의사결정 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 심의, 분쟁 조정 |
| [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) | 비즈니스 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 소유 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정의, 품질 기준 결정 |
| [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 실무 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 유지, 품질 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 |

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/)

| [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) | 측정 방법 | 목표 기준 |
|:---|:---|:---|
| 완전성 (Completeness) | NULL 비율 | 핵심 필드 99% 이상 |
| [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) (Accuracy) | 원천 대비 오차율 | 오차 <0.1% |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | 시스템 간 동일 값 비율 | 99.5% 이상 |
| 적시성 (Timeliness) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 내 갱신 95% 이상 |
| 유일성 (Uniqueness) | 중복 레코드 비율 | 중복 0.01% 이하 |

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: 거버넌스 3요소 + IT 지원 레이어

```
  +--------------------------------------------------------------+
  |               데이터 거버넌스 프레임워크                       |
  |                                                              |
  |  ① 원칙 (Principles)                                         |
  |  +---------------------------------------------------------+ |
  |  | 데이터 분류 정책 | 품질 기준 | 보안 정책 | 생명주기 정책  | |
  |  +---------------------------------------------------------+ |
  |                           |                                  |
  |  ② 조직 (Organization)    v                                  |
  |  +---------------------------------------------------------+ |
  |  |  CDO -> Governance Council -> Data Owner -> Data Steward  | |
  |  +---------------------------------------------------------+ |
  |                           |                                  |
  |  ③ 프로세스 + IT 시스템   v                                  |
  |  +-----------+  +-----------+  +-----------+  +----------+  |
  |  |데이터 카탈로그|  | 데이터 계보 |  |품질 모니터링|  |메타데이터|  |
  |  |(Atlas/   |  |(OpenLinea-|  |(dbt test/ |  |  관리    |  |
  |  | Alation) |  |  ge)      |  | GE)       |  |          |  |
  |  +-----------+  +-----------+  +-----------+  +----------+  |
  +--------------------------------------------------------------+
```

### [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 비교

| 제품 | 유형 | 주요 특징 |
|:---|:---|:---|
| Apache Atlas | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 연동, 자동 계보 |
| Alation | 상용 | ML 기반 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 사용자 협업 |
| DataHub (LinkedIn) | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 실시간 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| OpenMetadata | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | All-in-one, 빠른 성장 |

📢 **섹션 요약 비유**: [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 도서관 목록 시스템이다. 책 제목([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)명), 위치(저장소), 빌린 사람(사용자)을 기록해 누구나 원하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 찾을 수 있다.

## Ⅲ. 비교 및 연결

### [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/)-DMBOK 11개 지식 영역 (핵심)

| 영역 | 핵심 내용 |
|:---|:---|
| [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) (중심) | 전체 관리 방향 결정 |
| [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) | 엔터프라이즈 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) |
| [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)·[마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) (Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/)) |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 웨어하우징·BI | [DW](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/), 분석 레이어 |
| [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) | [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), 계보 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 | [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/), [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/) |

📢 **섹션 요약 비유**: [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/)-DMBOK는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리의 헌법이다. 11개 조항이 있고, [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 그 헌법의 전문(前文)이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 거버넌스 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) 또는 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) 전담 조직 존재 여부
- [ ] 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산 목록([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Asset Inventory) 작성
- [ ] [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 도구 도입 및 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 입력
- [ ] [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 5가지 측정 자동화
- [ ] [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보(Lineage) 자동 수집 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구축

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 거버넌스 규정 너무 엄격 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 민첩성 저하, 현업 반발 | 최소 필수 규정만 우선 적용 |
| [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)만 도입, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 미입력 | 빈 껍데기 도구 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 입력 전담 Steward 지정 |

📢 **섹션 요약 비유**: 거버넌스 성숙도는 학생의 공부 습관 성장과 같다. 1단계는 시험 전날 벼락치기, 5단계는 매일 계획적으로 공부하며 스스로 취약점을 찾아 보완하는 수준이다.

## Ⅴ. 기대효과 및 결론

| 항목 | 거버넌스 미도입 | 도입 후 |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) | "이 수치 믿어도 되나?" | [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 기반 품질 점수 공개 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) | 평균 4~8시간/건 | [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)로 15분 이내 |
| 규제 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응 | 수주~수개월 | 계보·[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)로 수일 |

📢 **섹션 요약 비유**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 교통 법규다. 규칙이 없으면 사고가 나지만, 규칙이 너무 많으면 아무도 차를 못 몬다. 적절한 균형이 핵심이다.

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) | 조직 | [Chief Data Officer](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/), 거버넌스 총괄 |
| [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 조직 | 실무 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·품질 관리자 |
| [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | IT 시스템 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 중앙 저장·검색 |
| [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/)-DMBOK | 표준 프레임워크 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 지식 체계 |
| [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | 연관 영역 | [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 단일 진실 원천 관리 |

### 📈 관련 키워드 및 발전 흐름도

```
데이터 품질 문제 인식 - 임시방편 대응
    |
    v
데이터 관리 정책 수립 (조직·프로세스·IT 3요소)
    |
    v
Data Catalog + Data Steward 체계화
    |
    v
DAMA-DMBOK 기반 거버넌스 성숙도 모델 적용
    |
    v
능동적 거버넌스 (Active Metadata + AI 자동화)
```

> **키워드**: [Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/), [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/), [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/), [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/)-DMBOK, [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/), [Data Quality](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/), [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)는 도서관 운영 규칙이에요. 어떤 책이 어디 있는지, 누가 관리하는지, 빌리는 규칙은 뭔지 정해두는 거예요.
2. CDO는 도서관장이고, [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Steward는 각 서가를 담당하는 사서예요.
3. [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 컴퓨터 검색 시스템이에요. 원하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 검색하면 어디 있는지, 누가 만들었는지 바로 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 306 / 482

<- **이전**: [305. 프라이버시 클린 룸 기업간 익명 조인 (Data Clean Room)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/)
**다음**: [307. 다차원 큐브 MOLAP ROLAP HOLAP 성능 튜닝 (Multidimensional OLAP)](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/307_molap_rolap_holap/) ->

---
