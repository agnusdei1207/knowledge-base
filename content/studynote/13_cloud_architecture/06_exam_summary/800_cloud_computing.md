+++
title = "800. 클라우드 / 데이터 / DevOps 융합 아키텍처 마스터 맵 종결"
description = "클라우드 컴퓨팅의 정의, 특성, 발전 과정"
date = 2026-03-26

[taxonomies]
tags = ["cloud_architecture"]

[extra]
tags = ["cloud_architecture"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) ([Cloud Computing](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/))은 온디맨드 (On-Demand) 방식으로 컴퓨팅 자원 (CPU, Memory, Storage, Network)을 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 형태로 제공하여, 사용자가 인프라를 소유하지 않고도 필요 시 언제든지 인프라를 활용할 수 있는 패러다임이다.
> 2. **가치**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자 비용 (CapEx, Capital Expenditure)을 운영 비용 (OpEx, Operational Expenditure)으로 전환하고, 물리적 인프라 조달 시간 수 주를 수 분으로 단축하여 비즈니스 민첩성을 비약적으로 향상시킨다.
> 3. **융합**: [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/)), [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/)), [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) 기술과 결합하여 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) (Development and Operations), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)/[Continuous Deployment](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/)), [하이브리드 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/) 아키텍처의 기반이 된다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

### 개념 정의

[클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) ([Cloud Computing](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/))은 NIST (National Institute of Standards and Technology)에서 "세 가지 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델 ([IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/), [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/), [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/))"과 "네 가지 배포 모델 (Public, Private, Hybrid, Community)"로 공식 정의한 표준 모델이다. 이 정의에 따르면 클라우드는 필수 특성 다섯 가지를 모두 충족해야 한다. 온디맨드 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (On-Demand Self-[Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 사용자가Provisioning (プロビジョニング) 없이도 자동으로 컴퓨팅 자원을 얻을 수 있어야 하고, 범용 네트워크 접근 (Broad Network Access)은 네트워크를 통해 어디서나 표준 메커니즘으로 자원에 접근 가능해야 한다. [자원 풀링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/638_resource_pooling_cxl/) (Resource [Pooling](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/))은 다중 테넌시 ([Multi-Tenancy](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)) 환경에서 물리적 자원이 동적으로 할당/회수되며, 신속한 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/) (Rapid Elasticity)은 수요에 따라 인프라를 자동으로 확장/축소할 수 있어야 한다. 마지막으로 측정된 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Measured [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 사용량에 따라 과금되는 투명한 과금 모델을 의미한다.

### 등장 배경

기존 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) (On-Premises) [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 방식의 한계가 클라우드 도입의 근본적 동력이됐다. 첫째, 하드웨어 구매에서 설치·[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·운영까지 수개월이 소요되어 비즈니스 요구에 신속 대응이 불가능했다. 둘째, 피크 시점의 수요를 예측해 과도한 하드웨어를 사전 구매하므로 자원 활용률이 평균 15~20%에 불과했다. 셋째, [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 냉각, 전력, 물리적 보안에 막대한 운영비가 발생했다. 이러한 비효율성을 해결하기 위해 등장한 것이 [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)이다.

[온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 환경의 자원 활용률 저하 문제를 보여주는 구조도를 살펴보면, 미리 구매한 하드웨어 용량이 실제 수요를 크게 상회하여 상당 부분이 낭비되고 있음을 알 수 있다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │               온프레미스 데이터센터의 자원 활용률 현실                │
  ├────────────────────────────────────────────────────────────────────┤
  │                                                                    │
  │  ┌──────────────────────────────────────────────────────────────┐  │
  │  │                    평균 활용률: 15~20%                        │  │
  │  │                                                              │  │
  │  │  CPU 사용량:    ████████████░░░░░░░░░░░░░░░░░░░░░░░░░  20%  │  │
  │  │  Memory 사용량: ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░  15%  │  │
  │  │  Storage 사용량: ██████████████░░░░░░░░░░░░░░░░░░░░░░  25%  │  │
  │  │  Network 사용량: ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10%  │  │
  │  │                                                              │  │
  │  │  █ = 실제 사용   ░ = 유휴 (낭비)                               │  │
  │  └──────────────────────────────────────────────────────────────┘  │
  │                                                                    │
  │  문제: 피크 수요 예측 → 과도 구매 → 낭비 → 비용 편익 악순환         │
  └────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 환경에서 IT 관리자는 예측된 피크 수요를 기반으로 하드웨어를 구매한다. 그러나 실제 워크로드가 피크에 도달하는 시간은 전체 운영 시간의 극히 일부에 불과하므로, 대다수 시간에 자원이 유휴 상태로 낭비된다. 이 낭비율이 평균 80%에 달하는 것이 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)의 구조적 비효율성이다. [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)은 이 문제를 필요 시마다 자원을 탄력적으로 확보하고, 사용한 만큼만 비용을 지불하는 모델로 해결한다.

### 비즈니스적 가치

클라우드로의 전환이 기업 재무 구조에 미치는 영향을 분석하면 명확히 드러난다. CapEx (자본적 지출)로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)되던 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 구축 비용이 OpEx (운영 지출)로 변경되어, 대규모 선불 투자가 필요한 인프라 대신 종량과금제 (Pay-[as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-You-Go) 모델로 월 단위 비용만 지불하면 된다. 이로 인해 기업의 손익 계산서 (P/L, Profit and Loss)에서 인프라 비용이 고정비가 아닌 변동비로 전환되어, 경기 변동에 대한 재무 유연성이 크게 개선된다.

### 비유

[클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)은 넓은 강물 (컴퓨팅 수요)에다 댐 (클라우드 인프라)을 쌓아 물을ため (자원 확보)두었다가, 수문 ([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))을 열어 필요한 만큼만 물을 흘려보내며 그 양에 비례하여 사용료를 받는 대규모 수도 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 계층 ([Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/))** | 물리 서버를 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 분할 | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), CPU/Memory 할당, 격리 실행 | Xen, [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), VMware ESXi | 아파트의 층별 세분화 |
| **클라우드 관리 플랫폼** | 전체 인프라 조율 및Orchestration | [자원 풀링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/638_resource_pooling_cxl/), 스케줄링, 모니터링, 과금 | OpenStack, VMware vCloud, AWS (Amazon Web Services) Console | 건물의 관리 사무실 |
| **[Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 엔진** | 복잡한 워크플로우 자동화 | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), 네트워크, 스토리지 조합을 자동 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/), CloudFormation | 건축의 도면 대로 시공하는 감리사 |
| **计量子系统 (Metering)** | 사용량 수집 및 과금 | CPU 시간, 스토리지 용량, 네트워크 트래픽을 실시간 수집 | CloudWatch, Azure [Monitor](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/), GCP (Google Cloud Platform) Operations | 아파트 관리비의 검침원 |
| ** identity & Access [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) ([IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/))** | [사용자 인증](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) 및 권한 부여 | 역할 기반 접근 제어 ([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), [Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) 적용 | AWS [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/), Azure AD ([Active Directory](/knowledge-base/studynote/09_security/11_iam_access_control/548_active_directory/)), GCP [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) | 건물의 출입 카드 시스템 |

### [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)의 핵심 구조

클라우드 인프라의根基는 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/)) 기술이다. [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/))는 물리적 서버 위에 다수의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 파티션을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여, 각 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이 독립된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 자원을 할당받는 환경을 제공한다. Type 1 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) (Bare-Metal)는 하드웨어 위에 직접 설치되어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 우수하고, Type 2 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) (Hosted)는 호스트 OS ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) 위에 설치되어 관리가 용이하다. 현대 클라우드 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)에서는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 효율성을 위해 주로 Type 1 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 사용된다.

[하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 기반의 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) architecture를 시각화하면, 물리적 서버 하나 위에 여러 VM이 독립된 게스트 OS (Guest [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))와 함께 동작하는 구조를 명확히 파악할 수 있다.

```text
  ┌──────────────────────────────────────────────────────────────────────┐
  │                     하이퍼바이저 기반 가상화 구조                        │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  ┌──────────────────────────────────────────────────────────────┐    │
  │  │                    물리적 서버 (Bare Metal)                  │    │
  │  │                                                              │    │
  │  │   ┌──────────────────────────────────────────────────────┐  │    │
  │  │   │              Type 1 하이퍼바이저 (Bare-Metal)          │  │    │
  │  │   ├─────────────┬─────────────┬─────────────┬───────────┤  │    │
  │  │   │             │             │             │           │  │    │
  │  │   │   ┌─────┐  │   ┌─────┐  │   ┌─────┐  │   ┌─────┐ │  │    │
  │  │   │   │ VM1 │  │   │ VM2 │  │   │ VM3 │  │   │ VM4 │ │  │    │
  │  │   │   │Linux│  │   │ Win │  │   │Linux│  │   │FreeBSD│ │  │    │
  │  │   │   │     │  │   │     │  │   │     │  │   │     │ │  │    │
  │  │   │   │ App │  │   │ App │  │   │ App │  │   │ App │ │  │    │
  │  │   │   └─────┘  │   └─────┘  │   └─────┘  │   └─────┘ │  │    │
  │  │   │   vCPU:2   │   vCPU:4   │   vCPU:2   │   vCPU:1  │  │    │
  │  │   │   Mem:4GB  │   Mem:8GB  │   Mem:4GB  │   Mem:2GB │  │    │
  │  │   └─────────────┴─────────────┴─────────────┴───────────┘  │    │
  │  └──────────────────────────────────────────────────────────────┘    │
  │                                                                      │
  │  각 VM은 격리된 환경에서 독립된 OS와 애플리케이션을 실행              │
  │  물리적 자원이 논리적으로 분할되어 동시에 다양한 워크로드 지원         │
  └──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 물리적 하드웨어 (CPU, Memory, Storage, Network)를 각 VM에 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 할당하는 자원 분배자 역할만 할 뿐, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리는 각 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 내의 게스트 OS와 애플리케이션이 직접 수행한다. 그러나 이 간접 계층이 존재하기 때문에 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 간 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) overhead가 발생하며, 이 문제를 해결하기 위해 등장한 기술이 바로 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/))다. VM은 전체 게스트 OS를 포함하므로起動 시간이 수십 초에서 수 분이 소요되는 반면, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 호스트 OS의 커널을 공유하여起動 시간이 수 밀리초에 불과하다.

### 온디맨드 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메커니즘

클라우드의 핵심 특성 중 하나인 온디맨드 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 사용자가 웹 콘솔이나 CLI ([Command](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Line Interface)를 통해 인프라 자원을 직접 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)하는自动化 시스템으로 구현된다. 사용자가 인스턴스를 요청하면 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway가 요청을 수신하여 IAM에서 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/인가를 수행하고, [Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 엔진이 자원 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 확인한 뒤 VM을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 네트워크를 연결한다. 전체 과정이 자동화되어 있어서 사람의 개입 없이 수 분 내에 완료된다.

### [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)의 동작 원리

신속한 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/) (Rapid Elasticity)은 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) ([Auto Scaling](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/)) 그룹에 의해 구현된다. 모니터링 시스템이 CPU 사용률, 메모리 사용량, 네트워크 트래픽 등의 메트릭을 실시간으로 수집하고, 미리 정의된 임계값을 초과하면 인스턴스를 추가Provision([Provisioning](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/))하고, 임계값 이하로 하락하면 인스턴스를 자동으로 회수한다. 이 과정에서 사용자는 최대 용량만 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하면 되고, 실제 자원 증감은 플랫폼이 자동으로 관리한다.

### 섹션 요약 비유

클라우드의 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)은 아파트의 자동 급수 시스템과 같아서, 상시 최대 수압에 맞춰관을 준비하는 것이 아니라 수전 (꼬리) 을 틀면 자동으로 물이涌き出하고, 사용량이 줄어들면 수전을关了瞬間に水流가 멈추는 것과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교 1: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) vs [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) vs [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)

| 비교 항목 | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) (On-Premises) | [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) ([Public Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)) | [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) ([Private Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)) |
|:---|:---|:---|:---|
| **[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자 (CapEx)** | 높음 (서버, 네트워킹, [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)) | 낮음 (선불 없음) | 중간~높음 |
| **운영 비용 (OpEx)** | 고정 (인력, 유지보수, 전기료) | 사용량 비례 과금 | 중간 (전용 자원 유지 비용) |
| **확장성** | 제한적 (하드웨어 구매 필요) | 사실상 무제한 | 제한적 (자원 용량 내) |
| **보안/규제 준수** | 직접 제어 가능 | 공유 책임 모델 ([CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) (Cloud [Service Provider](/knowledge-base/studynote/09_security/11_iam_access_control/535_sp_service_provider/)) + 사용자) | 직접 제어 + 전용 자원 |
| **전개 속도** | 수 주~수 개월 | 수 분~수 시간 | 수 주 |
| **[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)/[SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))** | 자체 설계/구현 | [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) (예: AWS 99.99%) | 자체 설계/구현 |

세 가지 배포 모델의 차이를 비교하면, [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)는 보안과 제어력에서 우세하지만 비용 효율성과 확장성에서 불리하고, [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)는 그 반대다. [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)는 양자의 트레이드오프 지점에 위치한다.

### 비교 2: 전통 호스팅 vs [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)

전통적인 공유 호스팅 (Shared Hosting)이나 전용 서버 (Dedicated Server)도 일종의 클라우드 이전 기술이지만, 클라우드와의 본질적 차이는 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) 방식의 유연성에 있다. 전통 호스팅은 계약 시점에 자원이 고정되며弹性이 전혀 없다. 클라우드는 [자원 풀링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/638_resource_pooling_cxl/)과 자동 확장 기능을 통해 수요 변화에 실시간으로 대응한다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │            전통 호스팅 vs 클라우드 컴퓨팅 자원 할당 비교              │
  ├────────────────────────────────────────────────────────────────────┤
  │                                                                    │
  │  [전통 호스팅]                                                      │
  │  │████████████│                    │████████████│                 │
  │  │  계약 시점  │                    │  계약 용량  │                 │
  │  └────────────┴────────────────────┴────────────┴──── 시간 轴     │
  │                                                                    │
  │  수요:  ────────────────峰值───────────────────                     │
  │        (자원 부족)         (여유)        (다시 부족)                │
  │                                                                    │
  │  [클라우드]                                                            │
  │  │████│                      │████████│     │████│                │
  │  └────┴──────────────────────┴────────┴─────┴────┴──── 시간 轴     │
  │                                                                    │
  │  수요:  ────────────────峰值───────────────────                     │
  │  공급:  ════════════════════ 자동 확장 ═══════════                  │
  │                                                                    │
  │  핵심: 계약 용량 개념 없음 → 수요 따라 자원이 증감                    │
  └────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전통 호스팅은 물리적 서버를 계약 시점에 특정 용량으로 고정 구매하므로, 수요가 계약 용량을 초과하면 처리 못하고, 반대로 수요가 적으면 남은 자원이 낭비된다. [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)은 모니터링 기반의 자동 확장으로 이러한刚性结构를 제거했다. 특히 Commerce (전자상거래) 플랫폼에서 블랙프라이데이 같은促销活动期间에는 수小时内에 자원이 수십 배 확장되었다가, 활동结束后数时间内 다시 축소되는 것이 가능해졌다.

### 과목 융합 관점

- **[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS)**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기술 ([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))은 Linux Namespaces와 [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ([Control Groups](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/))에 기반하여 프로세스 수준의 격리를 제공하며, 이는 클라우드의 핵심 기술 구성 요소다.
- **네트워크 (Network)**: [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) ([Virtual Private Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/028_vpc/))는 [VXLAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/) ([Virtual Extensible LAN](/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/))이나 [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) ([Generic Routing Encapsulation](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/)) 터널링을 통해 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 격리된 네트워크를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여, 물리적 네트워크 인프라 위에 다중 테넌트 환경을 구현한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 스타트업의 [MVP](/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/) ([Minimum Viable Product](/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/)) 배포**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 자금력이 부족한 스타트업이AWS EC2 (Elastic Compute Cloud) t3.micro 인스턴스로 웹 애플리케이션을 배포하여 월 $[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 수준의 비용으로 운영을 시작했다. 사용자 증가 시 애저 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 크기 업그레이드와 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)을 통해infra 구조를 점진적으로 확장했다. 핵심 의사결정 포인트는 "완벽한 인프라를 갖추고 시작하는 것이 아니라, 필요에 따라 확장 가능한 기반으로 시작하는 것"이다.

2. **시나리오 — 기존 기업의 리프트 앤 시프트 (Lift-and-Shift) 마이그레이션**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)에서 실행 중던 3계층 (Web-App-DB) 웹 애플리케이션을AWS의 VM으로 직접 이전하는 전략이다. 애플리케이션 코드를 수정하지 않고 인프라만 이전하므로 migration 기간이 짧고 리스크가 낮다. 그러나 이 방식은 클라우드의 진정한 가치인弹性과 자동화를 활용하지 못하므로, 장기적으로는Re-architecting (재설계)이 필요하다.

3. **시나리오 — 규제 industries를 위한 [하이브리드 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/)**: 금융이나 의료 산업에서는 고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의本地 저장 의무로 인해 [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)에서 핵심 시스템을 운영하면서, 개발/테스트 환경과burst workloads만 [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)를 활용하는 하이브리드 모델을 구축한다. 이때 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디에 저장되는지를 명확히 구분하고,跨 클라우드 네트워크를 PrivateLink나 [Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) Connect로 안전하게 연결하는 것이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- **기술적**: 현재 워크로드의 컴퓨팅 요구사항 (CPU, Memory, I/O)을 분석했는가? 마이그레이션 후 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 문제가 발생할 소지가 있는 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) ([라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), OS [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 네트워크 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))은 점검했는가?
- **운영·보안적**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) (Governance) 정책에 따라 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)에 저장 가능한지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)했는가? 클라우드Provifencer간의 주요 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 차이점 (예: AWS S3 vs Azure Blob Storage [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/))을 확인했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **과잉 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) (Over [Provisioning](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/))**: 예상 수요를 과대 평가하여 실제 사용량의 몇 배에 해당하는 자원을 사전 구매하면, 클라우드의成本 절감 효과가 완전히 상쇄된다. 반드시 실제 사용량 모니터링 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 기반으로Rightsizing (권장 크기 조정)을 정기적으로 수행해야 한다.
- **시큐리티 코너 케이트 ([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Corner Case)**: "클라우드는 안전하다"는 과도한 신뢰에서 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다. CSP의 공유 책임 모델을 정확히 이해하지 못하면, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출이나 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 실패 시 책임 소재가 모호해지는 문제가 발생한다.

### 섹션 요약 비유

클라우드 도입은 Sears 백화점에서 아마존으로의 쇼핑 방식 전환과 같아서, 큰 빌딩 ([온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/))을 직접 사들이는 것이 아니라的手指하나로 (온라인 주문) 필요한 순간에 필요한 만큼의商品(컴퓨팅 자원)을 받고, 사용한 만큼만 비용을 지불하는 것입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 최적화 전 ([온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) | 최적화 후 (클라우드) | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 구축 $500K (1회성) + 연간 운영 $100K | 종량제 월 $3K (연 $36K) | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자 **87% 절감** (3년 기준) |
| **정량** | 인프라Provisioning 6~8주 | 인스턴스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 5분 | 전개 속도 **99% 향상** |
| **정성** | 피크 대응 불가 (하드웨어 제한) | 오토 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)으로 피크 순간도 안정적 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 비즈니스 민첩성 극대화 |
| **정성** | 인력 5명 인프라 팀 운영 | Managed [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 활용으로 인원 축소 가능 | 운영 효율성 향상 |

### 미래 전망

- **[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)) 확산**: [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/) (Function [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 모델이进一步发展되어, 인프라 관리 조차 불필요하게 되면 개발자는 비즈니스 로직 작성에만 집중할 수 있게 된다. AWS [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), Azure Functions, GCP Cloud Functions가 이미 이를 구현하고 있다.
- **엣지 클라우드 (Edge Cloud) 통합**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 상용화와 함께 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간에 민감한 애플리케이션 (자율주행, AR/VR)을 위해 네트워크 엣지에微型 클라우드를 배치하는 방식이 확산될 전망이다.

### 참고 표준

- **NIST [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) 800-145**: [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)의 공식 정의 및 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 표준
- **ISO/IEC 17789**: [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 아키텍처
- **CSA ([Cloud Security](/knowledge-base/studynote/09_security/17_framework_compliance/842_iso_27017_cloud_security/) Alliance) CCM (Cloud Controls Matrix)**: 클라우드 보안 통제 프레임워크

[클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)은 단순한 기술이 아니라, 기업의 비용 구조, 운영 모델, 비즈니스 민첩성을 동시에 혁신하는 전략적 패러다임이다. 단기적인 비용 절감뿐 아니라, 장기적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 의사결정과 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 개발 문화를 구축하는 기반이 된다.

### 섹션 요약 비유

[클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)의 진화는 도시의 수도 시스템과 같아서,家家户户가 직접 우물을 파거나 물탱크를 들여놓던 시절에서, 중앙 공급 시스템으로切换되어 수전만 틀면 언제든지 깨끗한 물을 받을 수 있게 된 것과 같습니다.

---

## 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

| 개념 명칭 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 및 시너지 설명 |
|:---|:---|
| **[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) ([Virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/))** | 클라우드의根基 기술로, 단일 물리 서버에서 다중 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 서버를 분리하여 자원 활용도를 극대화한다. |
| **[Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) ([오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/))** | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), 네트워크, 스토리지 등 복합 자원을 자동 provisioning하여 사람이 수동으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 하는 작업을 줄인다. |
| **[멀티 테넌시](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) ([Multi-Tenancy](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/))** | 하나의 물리적 자원을 여러 고객이 공유使用时하되, 서로의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 완전히 격리되는 구조다. |
| **[IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/))** | 인프라를 코드로 정의하여 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 and 자동 배포를 가능하게 하며, 클라우드의 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)을代码로 관리한다. |
| **[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) (Development and Operations)** | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인과 결합하여 개발->테스트->배포 주기를 자동화하고, 클라우드의 빠른Provisioning과 맞물려 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 개발을 실현한다. |
| **[SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))** | CSP가 제공하는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 보증을 문서화한 계약으로, 클라우드의信頼性을定量化한다. |
| **[FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/) (Financial Operations)** | 클라우드 비용을 최적화하는 실무 분야로,Rightsizing, Reserved Instance, Savings Plans 등을 활용하여 비용을 절감한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)은 **레고 블록을 여러 사람과 함께 사는 것**예요. 각자全部 살 필요 없이, 내가 필요한 만큼만 빌려 쓰고 싶은 만큼만 비용을 내면 돼요.

### 📈 관련 키워드 및 발전 흐름도

```text
온프레미스 (자체 데이터센터)
    │
    ▼
클라우드 서비스 모델
    ├─► IaaS: VM · 스토리지 (EC2 · GCE)
    ├─► PaaS: 런타임 관리 (App Engine · Beanstalk)
    └─► SaaS: 완성 앱 제공 (Gmail · Salesforce)
    │
    ▼
컨테이너 + K8s + Serverless → 클라우드 네이티브
```
2.Amazon, Microsoft, Google 같은 큰 회사들이 방대한 컴퓨터 (서버) 숲을建設해두었기 때문에, 우리는 그 숲에서 필요한 만큼의 컴퓨터 파워를数분 만에 얻을 수 있어요.
3. 특히 놀이공원 (애플리케이션)이 인파ピーク (피크 수요) 에 대비해 항상 놀이기구를 여덟 개씩 준비할 필요가 없는 것처럼, 클라우드는 입구에서 표를 파는 만큼만 입장료를 내고 놀 수 있게 해줍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 371 / 371

← **이전**: [371. 클라우드 아키텍트 최고 난이도 기출 핵심 키워드망 요약 결론 (Cloud Architect Summary)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/371_process/)

✅ **마지막 글입니다.**

---
