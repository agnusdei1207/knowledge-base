+++
title = "234. 마스터 데이터 관리 (MDM, Master Data Management) 골든 레코드 클린 룸"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)(Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))은 조직 전체에서 공유되는 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(고객·제품·공급자)의 단일 권위 있는 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 관리하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치와 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))를 제거한다.
> 2. **가치**: 골든 레코드(Golden Record)는 중복 제거·병합·스코어링을 거쳐 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 "유일한 진실의 출처(Single Source of Truth)"로, 기업 의사결정의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 보장한다.
> 3. **판단 포인트**: 아키텍처 유형([허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)형·가상형·레지스트리형)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통제 강도, 시스템 연계 복잡도, 실시간 요건에 따라 선택하며, 프라이버시 이슈는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸([Data Clean Room](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/))으로 해결한다.

## Ⅰ. 개요 및 필요성

### MDM이 없을 때의 문제

대기업에는 수십 개의 시스템([CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)·[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)·[SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)·e-커머스)이 존재하고, 같은 고객이 각 시스템에 다르게 등록되어 있다.

```
CRM 시스템:   홍길동 / 서울시 강남구 / 010-1234-5678
ERP 시스템:   Hong Gil-dong / Seoul Gangnam / 01012345678
e-커머스:     홍 길동 / 강남구 서울 / 010.1234.5678
```

이로 인해 발생하는 문제들:
- **중복 마케팅**: 같은 고객에게 3개의 DM 발송
- **분석 부정확**: 고객 수 집계 시 1명이 3명으로 계산
- **규정 위반**: [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)(General [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Regulation) [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 삭제 요청 시 모든 시스템에서 삭제 불가

### MDM의 정의와 범위

[MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)(Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))은 기업의 핵심(Master) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔터티를 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고, 정제하며, 단일 권위 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 유지·관리하는 체계이다.

| [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 대상 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 주요 엔터티 | 핵심 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) |
|:---|:---|:---|
| 고객 마스터 ([C고객](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) | 개인·법인 고객 | [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 연락처, 거래 이력 |
| 제품 마스터 (Product [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) | 제품·SKU·[카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) | 제품명, 사양, 가격, [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 공급자 마스터 (Supplier [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) | 협력사·[공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) | 사업자번호, 계좌, 계약 조건 |
| 위치 마스터 (Location [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) | 지점·창고·주소 | 좌표, 행정구역, 운영 시간 |
| 직원 마스터 (Employee [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) | HR 인력 | 사번, 부서, 직책, 자격증 |

📢 **섹션 요약 비유**: MDM이 없는 기업은 같은 사람을 다른 이름으로 여러 주소록에 등록한 것과 같다. 전화하려면 어느 주소록이 맞는지 매번 확인해야 하는 혼란이 생긴다.

## Ⅱ. 아키텍처 및 핵심 원리

### 골든 레코드 (Golden Record) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 과정

```
+-----------------------------------------------------------------+
|                  골든 레코드 생성 파이프라인                         |
|                                                                 |
|  소스 시스템      수집         정제          매칭         병합       |
|                                                                 |
|  CRM ------+                                                    |
|  ERP ------+---> [프로파일링] -> [표준화]  -> [중복    -> [골든     |
|  ECM ------+    데이터 품질    주소·이름    탐지·     레코드]     |
|                 분석          정규화]      링킹]                  |
|                                                                 |
|         1단계        2단계       3단계       4단계     5단계      |
|        수집·통합    데이터 정제  표준화    매칭·링킹   병합·게시    |
+-----------------------------------------------------------------+
```

#### 각 단계 상세

| 단계 | 활동 | 기술/방법 |
|:---|:---|:---|
| **1. 수집** | 다중 소스에서 레코드 수집 | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)([Extract Transform Load](/knowledge-base/studynote/14_data_engineering/01_infrastructure/033_etl/)), [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) |
| <strong>2. <a href="/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/">프로파일링</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·완전성 분석 | 통계 분석, 이상값 탐지 |
| **3. 정제** | 결측·오류·불일치 수정 | 규칙 기반 보정, ML 보완 |
| **4. 표준화** | 주소·이름·전화번호 형식 통일 | 표준 주소 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 정규식 |
| **5. 매칭·링킹** | 동일 엔터티 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)·연결 | 확률적 매칭(Probabilistic Matching), [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) |
| **6. 병합·스코어링** | 최신·[신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 높은 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 선택 | [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 점수([Confidence](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) Score) |
| **7. 골든 레코드 게시** | 단일 권위 레코드 배포 | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 이벤트 스트림 |

### [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 아키텍처 유형

```
+-----------------------------------------------------------------+
|                 MDM 아키텍처 유형 비교                             |
+------------------+--------------------------------------------+
|  허브형          |          가상형                              |
|  (Hub Style)     |         (Virtual/Federation Style)          |
|                  |                                            |
|  MDM Hub         |  소스시스템1 --+                            |
|  +---------+     |  소스시스템2 --+---> [가상 레이어]            |
|  |골든레코드|     |  소스시스템3 --+   (실시간 연합)             |
|  +--+--+---+     |                                            |
|     |  |         |  원본 유지, 물리적 복사 없음                  |
|  CRM ERP SCM     |                                            |
+------------------+--------------------------------------------+

레지스트리형 (Registry Style):
  소스시스템 -> 각자 원본 유지
  MDM       -> 식별자·링크만 관리 (실제 데이터 미보유)
  특징: 가볍고 빠르나 통제력 낮음
```

### 아키텍처 유형 비교

| 유형 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치 | 통제 강도 | 구현 복잡도 | 적합 상황 |
|:---|:---|:---:|:---:|:---|
| [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)형 ([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) [Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 중앙 저장 | ⭐⭐⭐ | 높음 | 강한 거버넌스 필요 |
| 가상형 (Virtual) | 소스 시스템 원본 | ⭐⭐ | 중간 | 실시간 연동 중요 |
| 레지스트리형 ([Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)) | 소스 시스템 원본 | ⭐ | 낮음 | 간단한 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 연계 |
| 하이브리드 (Hybrid) | 혼합 | ⭐⭐⭐ | 매우 높음 | 대기업 복합 요건 |

📢 **섹션 요약 비유**: [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)형은 모든 주소록을 하나의 마스터 노트에 통합하는 것, 레지스트리형은 "각 주소록 몇 번째 줄에 있는 사람이 동일인"이라는 색인만 만드는 것이다.

## Ⅲ. 비교 및 연결

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸 ([Data Clean Room](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/))

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 <strong>두 조직이 원시 <a href="/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a>를 공유하지 않고</strong> 공통 고객 분석을 수행할 수 있는 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 환경이다.

```
        광고주 A                   플랫폼 B
    (구매 이력 보유)            (광고 노출 데이터 보유)
           |                          |
           v                          v
     +---------------------------------+
     |         데이터 클린 룸           |
     |  (Data Clean Room)              |
     |                                |
     |  원시 데이터 직접 공유 금지      |
     |  집계 결과·통계만 반출 허용      |
     |  개인 식별 불가 보장             |
     |                                |
     |  분석: 광고 도달 고객의 구매 전환율|
     +---------------------------------+
           결과: "캠페인 전환율 3.2%"만 공유
```

### 클린 룸 구현 기술

| 기술 | 설명 | 제공 업체 |
|:---|:---|:---|
| 안전한 다자 계산 (MPC, Multi-Party Computation) | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없이 공동 계산 | 학술/스타트업 |
| [연합 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) ([Federated Learning](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)) | 모델만 이동, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불동 | Google, Apple |
| [차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/) (DP, [Differential Privacy](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/)) | 노이즈 추가로 개인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | Apple, US Census |
| [신뢰 실행 환경](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([TEE](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/), [Trusted Execution Environment](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/)) | 하드웨어 격리 분석 | [Intel SGX](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/480_intel_sgx/) |
| Google ADH | Google Ads [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸 | Google |
| AWS Clean Rooms | AWS 기반 클린 룸 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | AWS |

📢 **섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 두 회사가 각자 레시피 비밀을 지키면서도 같이 요리한 결과물(분석 결과)만 보는 공유 주방이다.

## Ⅳ. 실무 적용 및 기술사 판단

### [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 구축 단계별 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

```
Phase 1: 준비 (0~3개월)
  ☐ 마스터 데이터 도메인 식별
  ☐ 데이터 오너십·거버넌스 체계 수립
  ☐ 데이터 품질 현황 진단 (프로파일링)

Phase 2: 설계 (3~6개월)
  ☐ MDM 아키텍처 유형 선택 (Hub/Virtual/Registry)
  ☐ 골든 레코드 모델 설계
  ☐ 매칭 규칙·신뢰도 점수 기준 정의

Phase 3: 구현 (6~12개월)
  ☐ ETL 파이프라인 구축
  ☐ 중복 탐지·병합 알고리즘 구현
  ☐ MDM 플랫폼 구축 (Informatica, IBM InfoSphere 등)

Phase 4: 운영
  ☐ 데이터 스튜어드 역할 배정
  ☐ 변경 이벤트 스트림 발행 (CDC)
  ☐ 품질 KPI 모니터링 대시보드
```

### 기술사 판단 포인트

1. **아키텍처 선택**: 통합 강도 vs 유연성 트레이드오프 명확히 제시
2. <strong>매칭 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>: 결정적 매칭(완전 일치) + 확률적 매칭(유사도) 조합
3. **거버넌스**: 기술보다 조직·프로세스 문제가 더 어려움 — [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) 필수
4. **클린 룸**: [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) 준수하면서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공동 활용 시 필수 선택지

📢 **섹션 요약 비유**: [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 구축은 집 정리와 같다. 먼저 무엇이 있는지 파악([프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/))하고, 중복을 버리고(중복 제거), 제자리에 놓고(표준화), 잘 정돈된 상태를 유지(거버넌스)해야 한다.

## Ⅴ. 기대효과 및 결론

### [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 도입 기대효과

| 영역 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 | 중복률 15~30% | 중복률 < 1% | 90%+ 개선 |
| 마케팅 효율 | 동일 고객 중복 발송 | 단일 정확 고객 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 마케팅 비용 절감 |
| 분석 정확도 | 집계 오차 큼 | 신뢰 가능 집계 | [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 확보 |
| 규정 준수 | [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 위치 불명 | 전 시스템 즉시 삭제 가능 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 대응 |
| 시스템 통합 | 포인트-투-포인트 연결 | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 단일 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) | 통합 복잡도 감소 |

### 결론

MDM은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 경영의 기반 인프라다. 기술적 구현보다 조직의 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 체계와 [데이터 스튜어드십](/knowledge-base/studynote/12_it_management/05_security_compliance/273_data_stewardship/) 문화가 성공 요인이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 MDM의 경계를 넘어 파트너사·플랫폼 간 프라이버시 안전 협업을 가능케 하는 차세대 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 패러다임이다.

📢 **섹션 요약 비유**: MDM은 기업의 "공식 전화번호부"다. 모든 부서가 같은 전화번호부를 쓰면 혼선이 없어진다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 두 회사가 서로의 전화번호부를 직접 보지 않고 "공통 고객이 몇 명인지"만 확인하는 방법이다.

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 목표 | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) (Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/)) | 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 단일 권위 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| 최종 산출물 | 골든 레코드 (Golden Record) | 중복 제거·병합된 단일 진실 레코드 |
| 아키텍처 | [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)형 / 가상형 / 레지스트리형 | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 시스템 설계 방식 |
| [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸 ([Data Clean Room](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/)) | 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 공동 분석 환경 |
| 관련 기술 | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 변경 이벤트 실시간 전파 |
| 관련 프레임워크 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) / [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) | 클린 룸 도입 동인 |
| 조직 역할 | [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 책임자 |

### 👶 어린이를 위한 3줄 비유 설명

1. MDM은 학교에서 "홍길동"이 1반에도, 2반에도, 3반에도 다른 이름으로 등록된 것을 하나로 합쳐 "우리 학교 홍길동은 이 한 명"이라고 확정하는 것이다.

### 📈 관련 키워드 및 발전 흐름도

```text
마스터 데이터 사일로 (부서별 중복 · 불일치)
    |
    v
MDM: 골든 레코드 생성 · 데이터 통합
    +-► 매칭 · 머지 · 서바이버십 규칙
    +-► Clean Room: 개인정보 보호 합동 분석
    |
    v
데이터 거버넌스: 품질 · 보안 · 컴플라이언스
```
2. 골든 레코드는 여러 반의 기록 중 가장 정확한 정보만 골라 만든 "공식 학생 기록부"다.
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 두 학교가 서로의 학생 명단을 공유하지 않고 "두 학교에 모두 다니는 학생이 몇 명인지"만 같이 세어보는 비밀 방이다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 234 / 258

<- **이전**: [233. 정밀도(Precision) 재현율(Recall) F1 스코어 ROC AUC 임계 곡선](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)
**다음**: [235. AI 튜링 테스트 (Turing Test) 전문가 시스템 (Expert System) 퍼지 논리 (Fuzzy Logic)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/235_ai_turing_test_expert_system_fuzzy_logic/) ->

---
