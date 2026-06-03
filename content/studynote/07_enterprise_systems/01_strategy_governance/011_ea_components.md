+++
title = "11. EA 구성요소 (BA: 비즈니스, DA: 데이터, AA: 애플리케이션, TA: 기술 아키텍처) + SA (보안 아키텍처)"
description = "전사적 아키텍처(EA)를 구성하는 핵심 도메인별 세부 아키텍처(BA, DA, AA, TA, SA)의 구조와 유기적 연계 메커니즘 심층 분석"
date = 2024-05-24

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

# [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성요소 ([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/), [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/), [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/), [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전사적 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/))는 비즈니스([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))를 필두로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)), 애플리케이션([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)), 기술([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)), 보안([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) 아키텍처가 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 결합된 기업의 종합 정보화 청사진이다.
> 2. **가치**: IT와 비즈니스의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 연계를 보장하여, 중복 투자를 30% 이상 줄이고 시스템 간 [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/)([Interoperability](/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/))을 극대화한다.
> 3. **융합**: 전통적인 4대 아키텍처에 클라우드/제로트러스트 시대의 필수 요소인 [보안 아키텍처](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/)([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))가 융합되어, 민첩성과 안정성을 동시에 달성하는 구조로 진화 중이다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

**전사적 아키텍처([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/), [Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/))의 하위 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)**은 기업의 복잡한 비즈니스 목표와 IT 인프라를 체계적으로 연결하기 위해 구조화된 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 집합체이다. 과거 정보시스템 구축은 부서 단위의 파편화된 요구사항에 따라 개별적으로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)되었다([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) Effect). 이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복, 인터페이스 복잡도 증가, 유지보수 비용의 기하급수적 상승이라는 한계에 봉착했다. 이 문제를 해결하기 위해 도입된 EA는 기업 전체의 관점에서 일관된 표준과 지침을 제공하는 패러다임이다. 

현대의 비즈니스 환경은 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 전환, [마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) 도입 등으로 인해 아키텍처의 유연성과 추적성 확보가 필수적이다. 비즈니스 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 IT 시스템의 말단 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)까지 어떻게 매핑되는지 증명하지 못하면 [디지털 트랜스포메이션](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/071_digital_transformation_dx/)은 실패한다. 따라서 각 구성요소([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/), [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/), [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/), [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))는 단절된 도면이 아니라, 비즈니스 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 IT 구현물로 번역하는 정교한 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 역할을 수행한다.

이 도식은 비즈니스 요구사항이 하위 IT 요소로 어떻게 전파되고 구체화되는지를 보여준다. 최상위 계층인 [비즈니스 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))에서 정의된 목표는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))와 애플리케이션([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/))의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 설계를 거쳐 물리적 기술([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))과 보안([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) 인프라로 안착된다. 따라서 하위 계층의 어떠한 변경도 상위 계층의 비즈니스 목적을 위배해서는 안 된다는 추적성([Traceability](/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/))이 강조된다.

```text
┌────────────────────────────────────────────────────────┐
│ [Business Strategy & Goals]                            │
├────────────────────────────────────────────────────────┤
│ ▼ 추진                                                 │
│ [BA] Business Architecture (프로세스, 조직, 기능)      │
├───────────────────────┬────────────────────────────────┤
│ ▼ 요구               │ ▼ 요구                        │
│ [DA] Data Arch.       │ [AA] Application Arch.         │
│ (개념/논리/물리 DB)   │ (서비스, 컴포넌트, 인터페이스) │
├───────────────────────┴────────────────────────────────┤
│ ▼ 탑재 및 보호                                        │
│ [TA] Technology Arch. (서버, 네트워크, 클라우드 등)    │
│ [SA] Security Arch. (인증, 암호화, 접근통제)           │
└────────────────────────────────────────────────────────┘
```
*해설: 이 계층 구조도는 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 간의 의존성과 수직적 정렬(Alignment) 상태를 보여준다. BA가 변화하면 DA와 AA가 반드시 영향을 받고, 이를 지원하기 위해 TA와 SA의 용량/[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 재조정되어야 한다. 실무에서는 상향식 도입([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/) 우선)보다 하향식([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/) 우선) 전개가 아키텍처 정합성 유지에 훨씬 유리하다.*

📢 **섹션 요약 비유**: [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성요소는 초고층 빌딩을 짓는 것과 같습니다. BA가 건물의 용도(주거용/상업용)를 정하면, DA와 AA는 배관과 전기 회로도를 그리고, TA는 실제 사용할 철근과 콘크리트 자재를 결합하며, SA는 출입 통제 시스템과 화재 경보기를 설치하는 유기적 협업입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

EA를 구성하는 5대 핵심 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 아키텍처는 각각 독립적인 뷰([View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))를 가지면서도 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 통해 강력히 결합된다.

| 아키텍처 | 핵심 역할 | 산출물 (Artifacts) | 실무 초점 |
|:---|:---|:---|:---|
| **[BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/) (비즈니스)** | 기업의 목적, 구조, 프로세스의 정의 | 프로세스 맵, 조직도, 업무 기능 분할도 | IT 투자의 정당성 확보, 중복 업무 통폐합 |
| **[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))** | 전사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조와 관리 체계 수립 | 개념/[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)/물리 ERD, [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [Single Source of Truth](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) |
| **[AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/) (애플리케이션)** | 비즈니스를 지원하는 SW 구조와 통합 | 앱 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)폴리오, 인터페이스([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 명세 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재사용성, [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/), [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 저하 |
| **[TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/) (기술)** | 앱과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실행하는 H/W, N/W 인프라 | 네트워크 구성도, HW 사양서, SW 표준 | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)(HA), 확장성([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| **[SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) (보안)** | 정보 자산의 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/)서, 암호화 아키텍처, [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 체계 | [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)), 규제 준수 |

[EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성요소 간의 작동 원리는 상호 연계 매트릭스(Cross-[Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) Matrix)에 기반한다. 예를 들어 비즈니스 프로세스([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))의 특정 활동(Activity)은 반드시 하나 이상의 애플리케이션([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)) 기능에 의해 지원되어야 하며, 해당 애플리케이션은 특정 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔터티([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))를 C/R/U/D(Create, Read, Update, Delete) 한다. 이 연결 고리가 끊어진다면 해당 IT 시스템은 비즈니스 가치가 없거나, 비즈니스 프로세스가 수작업으로 방치되어 있다는 뜻이다.

```text
[연계 메커니즘: 프로세스 - 애플리케이션 - 데이터의 상호작용]

(BA) "주문 처리" 프로세스
       │
       ├─ 지원 ─▶ (AA) "주문 관리 마이크로서비스"
       │                 │
       │                 ├─ 접근 ─▶ (DA) "Order_Master" 테이블 (Insert)
       │                 ├─ 접근 ─▶ (DA) "Item_Inventory" 테이블 (Update)
       │                 │
       │                 ▼ 실행
       └────────▶ (TA) AWS EKS 클러스터 (컨테이너 노드)
                         │
                         ▼ 보호
                  (SA) mTLS 적용 및 WAF(웹 방화벽) 정책 통과
```
*해설: 이 흐름도는 단일 비즈니스 이벤트("주문 처리")가 하위 아키텍처 전반을 어떻게 관통하는지를 나타낸다. 이러한 가시성이 확보되면, 특정 서버([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))가 다운되었을 때 어떤 비즈니스 프로세스([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))가 마비되는지 즉각적인 영향도 분석(Impact Analysis)이 가능해진다. 따라서 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 관리 시스템([EAMS](/knowledge-base/studynote/12_it_management/03_ea_isp/124_eams_ea_management_system/))에서는 이 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 맵핑이 핵심 자산이다.*

📢 **섹션 요약 비유**: 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 연계는 인체의 신경망과 같습니다. 뇌([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))에서 의사결정을 내리면 운동 신경([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/))이 근육([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))을 움직여 뼈대([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))를 지지하며, 이 모든 과정은 백혈구와 면역 체계([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))의 지속적인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 아래 안전하게 이루어집니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

IT 경영 측면에서 과거의 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 시스템 아키텍처와 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 기반의 통합 아키텍처는 비용 구조와 변화 수용성에서 큰 차이를 보인다.

| 비교 항목 | [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) ([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 시스템 기반 | [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) ([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)/[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)/[AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)/[TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)/[SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) 프레임워크 기반 |
|:---|:---|:---|
| **정렬 (Alignment)** | 현업 부서 단위의 단기적, 전술적 정렬 | 전사적 관점의 중장기적, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 정렬 |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조** | 부서별 중복 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 불일치 발생 ([Data Swamp](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/288_data_swamp_metadata_management_absence/)) | [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)([MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)) 통합, Single Truth 보장 |
| **확장성/재사용** | 개별 시스템 간 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 스파게티 연동 (확장 어려움) | 표준 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [ESB](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/)/[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 기반의 높은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재사용성 |
| **보안/거버넌스** | 개별 시스템 패치 적용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 사각지대 존재 | 중앙 통제형 [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/)([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)), 일괄 규제 대응 |

특히 최신 아키텍처 진화 방향과 결합하면 각 구성요소의 역할이 변화한다.
1. **[마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))와의 융합**: AA는 모놀리식에서 잘게 쪼개진 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 집합으로 변하고, [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 역시 '[Database per Service](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/311_database_per_service_pattern/)' 패턴을 적용하여 [폴리글랏 퍼시스턴스](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/308_pgvector/)([Polyglot Persistence](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/132_polyglot_persistence/))를 추구하게 된다. 이때 전체 정합성을 유지해주는 것이 [BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/) 프로세스의 [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)([Bounded Context](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)) 설계이다.
2. **[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/))와의 융합**: TA의 영역이 물리적 장비 구매에서 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/)) 기반의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 코드로 변환되며, [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 역시 경계망 보안에서 신원 기반의 [제로 트러스트 구조](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1043_ztna_zero_trust_network_access_architecture/)로 통합된다.

```text
┌───────────────┬───────────────────────────┬───────────────────────────┐
│ EA 도메인     │ 전통적 아키텍처 (Legacy)  │ 최신 아키텍처 (Modern IT) │
├───────────────┼───────────────────────────┼───────────────────────────┤
│ AA (앱)       │ Monolithic, ERP 패키지    │ MSA, Serverless, API G/W  │
│ DA (데이터)   │ Centralized RDBMS (Oracle)│ Data Lake, NoSQL 분산 DB  │
│ TA (인프라)   │ On-Premise, Bare-metal    │ Multi-Cloud, Kubernetes   │
│ SA (보안)     │ 방화벽 기반 망분리 (경계) │ ZTNA, IAM, DevSecOps      │
└───────────────┴───────────────────────────┴───────────────────────────┘
```
*해설: 이 매트릭스는 기술 패러다임 변화에 따른 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 진화를 보여준다. 과거에는 [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)(인프라) 도입이 수개월 걸렸으나 현재는 초 단위로 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)된다. 따라서 아키텍처 관리의 중심축은 TA의 물리적 자산 관리에서 AA와 DA의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)/[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)로 급격히 이동하고 있다.*

📢 **섹션 요약 비유**: 과거의 시스템이 각자 자기 악기만 크게 연주하는 소음이 섞인 밴드였다면, [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 프레임워크는 지휘자([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))의 악보([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/))에 맞춰 모든 악기([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))가 정확한 타이밍과 조율([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) 속에 연주하는 거대한 오케스트라입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성을 완벽하게 유지하는 것은 막대한 오버헤드를 수반한다. 따라서 아키텍트와 IT 관리자는 어느 수준까지 상세화를 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)할지 트레이드오프를 결정해야 한다.

1. **상세화 수준(Level of Detail) 조절**: 모든 애플리케이션의 소스 코드 수준까지 AA에 문서화하는 것은 불가능하며 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다. 핵심 비즈니스 로직과 시스템 간 연동(Interface) 위주로 모델링하여 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 갱신의 민첩성을 확보해야 한다.
2. **[As-Is](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 분석의 늪(Analysis Paralysis) 주의**: [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)([As-Is](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/))의 아키텍처를 파악하는 데 전체 예산의 80%를 소진하는 경우가 잦다. 실무에서는 To-Be (목표 아키텍처)의 핵심 트랜지션(Transition)에 영향을 주는 범위 내에서만 [As](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-Is를 파악하고, 신규 도입되는 [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)/AA에 집중하는 가치 중심 접근법이 요구된다.
3. **거버넌스와 자동화 결합**: 시스템이 배포될 때마다 아키텍처 산출물이 수동 갱신된다면 100% [현행화](/knowledge-base/studynote/12_it_management/03_ea_isp/125_asis_update_ea_maintenance_synchronization/) 실패로 이어진다. [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [인프라 코드](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))나 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스웨거(Swagger) 문서가 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 저장소로 자동 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)되도록 [데이터옵스](/knowledge-base/studynote/14_data_engineering/04_mlops/196_dataops_dbt_ci_cd_data_testing/)([DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/)) 및 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) 연계가 필수적이다.

```text
[EA 아키텍처 거버넌스 의사결정 트리]

[신규 IT 프로젝트 발의]
         │
         ▼
[BA 검토] 기존 비즈니스 프로세스와 중복되는가?
   ├─ (Yes) ──▶ [반려] 기존 시스템 재사용 권고
   │
   └─ (No) ───▶ [AA/DA 검토] 표준 API/데이터 모델을 준수하는가?
                   ├─ (No) ──▶ [설계 수정] 전사 표준 체계로 재설계 지시
                   │
                   └─ (Yes) ─▶ [TA/SA 검토] 클라우드 인프라/보안 규정에 적합한가?
                                  ├─ (No) ──▶ 망분리, 암호화 아키텍처 보강
                                  │
                                  └─ (Yes) ─▶ [아키텍처 위원회(ARB) 승인 및 구현]
```
*해설: 이 플로우차트는 일선 기업의 [아키텍처 검토 위원회](/knowledge-base/studynote/12_it_management/03_ea_isp/123_arb_architecture_review_board/)(ARB, [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) [Review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/) Board)가 IT 프로젝트를 통제하는 과정을 보여준다. 가장 큰 병목은 각 부서가 자신의 편의를 위해 전사 표준([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))을 우회하려 할 때 발생한다. 예외(Exception)를 무분별하게 허용하면 EA는 무너진다. 실무에서는 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)([Technical Debt](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/))를 지고 예외를 한시적 허용하되, 차기 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에 표준화하는 조건부 승인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 혼용한다.*

📢 **섹션 요약 비유**: 아키텍처 관리는 정원 가꾸기와 같습니다. 처음 도면대로 완벽히 심어놓더라도, 잡초(비표준 IT)가 자라나고 가지(기능 확장)가 뻗어나가므로 주기적인 전지와 자동화된 스프링클러(거버넌스) 없이는 순식간에 난장판이 됩니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성요소 체계화를 통해 기업은 복잡성을 관리 가능한 상태로 낮추고, IT 투자의 투명성을 획기적으로 개선할 수 있다.

| 지표 | 정량적 / 정성적 기대효과 | 비고 |
|:---|:---|:---|
| **[ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) / 비용** | IT [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)폴리오 중복 제거로 시스템 운영비 20~30% 절감 | 인프라 통합([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)) 및 라이선스 최적화 |
| **민첩성 (Agility)** | 신규 비즈니스([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)) 론칭 시 IT 지원 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 40% 단축 | 표준 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)) 조립 및 재사용 |
| **위험 관리** | 사이버 보안([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)) 위협 발생 시 신속한 영향도 파악 및 격리 | 컴플라이언스 및 BCP 복원력 향상 |

미래의 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성요소는 정적인 문서 형태에서 벗어나, 런타임 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)을 기반으로 스스로 [현행화](/knowledge-base/studynote/12_it_management/03_ea_isp/125_asis_update_ea_maintenance_synchronization/)되는 '동적이고 살아있는 아키텍처(Living [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))'로 진화할 것이다. 또한, TOGAF나 [GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/)(범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)) 같은 글로벌/국가 표준 프레임워크는 더욱 간결해지고 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 생태계를 수용하는 방향으로 개정되고 있어, 기업은 뼈대(표준)는 유지하되 실행(개발)은 자유로운 [양손잡이 조직](/knowledge-base/studynote/12_it_management/01_governance_strategy/037_ambidextrous_organization/)의 아키텍처를 구현해야 한다.

📢 **섹션 요약 비유**: 훌륭하게 정립된 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 요소들은 잘 정돈된 도시 계획과 같습니다. 구역([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/))이 명확하고 수도관([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))과 도로([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/))가 규격화되어 있으며 변전소([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))와 경찰서([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))가 완비되어 있다면, 새로운 건물을 세울 때 고민 없이 인프라에 바로 접속해 가치를 창출할 수 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* **[TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) ([The Open Group Architecture Framework](/knowledge-base/studynote/09_security/17_framework_compliance/875_togaf/))** | [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성요소([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/), [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/), [TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/))를 실제로 구현하는 방법론([ADM](/knowledge-base/studynote/03_network/01_data_communication/066_적응형_델타_변조_ADM/))을 제공하는 국제 표준 프레임워크
* **[Zachman Framework](/knowledge-base/studynote/12_it_management/03_ea_isp/112_zachman_framework/) ([잭맨 프레임워크](/knowledge-base/studynote/12_it_management/03_ea_isp/112_zachman_framework/))** | 6하 원칙과 [이해관계자](/knowledge-base/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) 관점을 교차시켜 EA의 모든 산출물을 누락 없이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 6x6 매트릭스
* **[EAMS](/knowledge-base/studynote/12_it_management/03_ea_isp/124_eams_ea_management_system/) ([Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) System)** | 아키텍처 산출물([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)) 간의 매핑 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 저장, [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/), 통제하는 중앙 리포지토리 도구
* **[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/))** | 거대 앱을 작게 분리하는 AA의 현대적 접근으로, [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 체계가 잡혀있지 않으면 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)의 복잡도로 인해 오히려 실패 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 높아짐
* **[IT Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/001_it_governance/) (IT 거버넌스)** | EA가 단순히 도면으로 남지 않도록 경영진이 조직, 프로세스, 통제 위원회(ARB)를 통해 강제하는 관리 체계

### 📈 관련 키워드 및 발전 흐름도

```text
[비즈니스 아키텍처 (BA) — 전략·프로세스·조직 모델 정의]
    │
    ▼
[데이터 아키텍처 (DA) — 정보 자산·흐름·품질 기준 수립]
    │
    ▼
[애플리케이션 아키텍처 (AA) — 시스템 포트폴리오·통합 인터페이스 설계]
    │
    ▼
[기술 아키텍처 (TA) — 인프라·네트워크·플랫폼 표준 정의]
    │
    ▼
[IT 거버넌스 (IT Governance) — ARB 통해 EA 준수 강제, 투자 통제]
```

이 흐름은 비즈니스 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에서 기술 인프라까지 4계층 아키텍처 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 정렬되고 거버넌스로 통제되는 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 구성 체계를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. 컴퓨터나 회사 시스템을 만들 때는 무작정 코딩부터 하는 게 아니라 큰 그림을 먼저 그려야 해요. 이 큰 그림이 바로 '아키텍처'예요.
2. 어떤 일을 할지([BA](/knowledge-base/studynote/12_it_management/03_ea_isp/103_ba_as_is_analysis/)), 정보는 어떻게 모을지([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)), 무슨 앱을 쓸지([AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/)), 어떤 컴퓨터와 인터넷을 쓸지([TA](/knowledge-base/studynote/12_it_management/03_ea_isp/106_ta_as_is_analysis/)), 해커를 어떻게 막을지([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))를 순서대로 꼼꼼히 설계해요.
3. 이렇게 5가지 설계를 레고 블록처럼 딱 맞게 연결해두면, 나중에 회사가 커지거나 고장이 나도 어디를 고쳐야 할지 금방 알 수 있어서 돈과 시간을 아낄 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 11 / 482

← **이전**: [10. EA (Enterprise Architecture, 전사적 아키텍처) - 기업의 비즈니스, 데이터, 애플리케이션, 기술 인프라를](/knowledge-base/studynote/12_it_management/01_governance_strategy/010_ea_enterprise_architecture/)
**다음**: [12. 잭맨 프레임워크 (Zachman Framework) - 6x6 매트릭스 (Who, What, Where, When, Why, How](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/012_zachman_framework/) →

---
