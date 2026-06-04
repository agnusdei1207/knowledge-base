---
title: "2. IaaS (Infrastructure as a Service) - 서버(VM), 스토리지, 네트워크 인프라 제공 (AWS EC2, S3)"
date: "2024-05-24"
description: "서버, 스토리지, 네트워크 등 클라우드 인프라 자원을 가상화하여 제공하는 IaaS의 핵심 원리와 실무 아키텍처 가이드"
tags:
  - "cloud_architecture"
---


# [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) (Infrastructure [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IaaS는 물리적 컴퓨팅 자원(서버, 스토리지, 네트워크)을 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)와 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/[SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 기술로 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)하여 사용자에게 API나 콘솔을 통해 주문형으로 제공하는 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델이다.
> 2. **가치**: 인프라의 막대한 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 자본 지출(CapEx)을 운영 지출(OpEx)로 전환하고, 벤더 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)을 최소화하며, OS 및 애플리케이션 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 대한 최고 수준의 제어권을 보장한다.
> 3. **융합**: [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 위에서 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)), [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 관리([Ansible](/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/)), [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)([Immutable Infrastructure](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)) 배포가 결합되어야 비로소 [데브옵스](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)의 온전한 자동화가 실현된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

[IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) (Infrastructure [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 클라우드 컴퓨팅의 3대 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/), [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/), [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)) 중 가장 근간이 되는 기초 레이어이다. 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공자([CSP](/studynote/09_security/05_web_app_security/475_csp/))가 물리적 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 공간, 전력, 냉각, 서버 장비, 스토리지, 네트워크 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 모두 소유하고 관리하며, 사용자는 가상 머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)), 서브넷, 블록 스토리지 형태의 '추상화된 인프라'를 임대하여 사용한다. AWS의 EC2, EBS, VPC나 Google Cloud Compute 엔진이 대표적이다.

과거 기업들은 자체 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)(IDC)를 구축하거나 [코로케이션](/studynote/07_enterprise_systems/01_strategy_governance/062_colocation_data_center_leasing/) 환경에 물리 서버를 직접 입고시켰다. 이 방식은 피크 타임 부하를 감당하기 위해 평상시에는 잉여 자원으로 방치되는 '오버프로비저닝'을 강제했다. 또한 새로운 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 런칭 시 하드웨어 발주 및 네트워크 결선에 수개월이 소요되었다. IaaS는 이러한 하드웨어의 물리적 족쇄를 끊어내고, 인프라를 '소프트웨어(코드)'처럼 즉각적으로 다룰 수 있는 근본적 변혁을 가져왔다.

다음은 기존 레거시 인프라와 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 환경의 자원 관리 병목을 비교한 도식이다.

```text
[기존 물리적 인프라 환경의 병목]
요청 -> [발주/배송 (Weeks)] -> [IDC 입고/마운트 (Days)] -> [OS/네트워크 수동 설정 (Days)] -> 투입
              ^ 물리적 시간 지연이 비즈니스 속도를 제약

[IaaS 환경의 소프트웨어 정의 인프라]
요청 -> [Cloud API/IaC 실행] -> [하이퍼바이저 자원 논리 할당 (ms)] -> [가상 인스턴스 부팅 (Sec)] -> 투입
              ^ 모든 물리 장비가 추상화되어 API 엔드포인트로 통제됨
```

이 그림이 보여주듯, IaaS의 본질은 하드웨어의 제거가 아니라 '하드웨어 제어권의 API화'에 있다. 사용자는 복잡한 물리적 케이블링 대신 [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)([Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) 같은 코드를 통해 몇 줄의 텍스트로 가상 네트워크([VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/))를 뚫고 수백 대의 서버를 동시에 띄울 수 있다. 따라서 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 환경에서는 시스템 장애 시 서버를 고쳐 쓰는(Mutable) 것이 아니라 파기하고 새로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)([Immutable](/studynote/13_cloud_architecture/05_data_engineering/298_immutable/))하는 새로운 운영 패러다임이 요구된다.

📢 **섹션 요약 비유**: 맨땅에 직접 시멘트와 철근을 사서 건물을 짓는 대신, 수도와 전기가 완벽히 깔린 모듈식 조립 공간을 임대하여 내 마음대로 실내 인테리어(OS, 앱)를 꾸미는 것과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

IaaS를 구성하는 백엔드 아키텍처는 컴퓨팅, 네트워크, 스토리지의 3대 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 기술([SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/): [Software-Defined Data Center](/studynote/13_cloud_architecture/01_virtualization/023_sddc_software_defined_data_center/))로 이루어진다.

| 구성 요소 | 역할 | 핵심 기술/메커니즘 | 실무 예시 (AWS 기준) | 비유 |
|:---|:---|:---|:---|:---|
| <strong>컴퓨팅 <a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (SDC)</strong> | CPU, RAM 자원 분할 할당 | [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), Xen, Nitro), [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) | EC2, [Auto Scaling](/studynote/13_cloud_architecture/01_virtualization/030_auto_scaling/) | 넓은 땅을 구획으로 쪼개기 |
| <strong>스토리지 <a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/632_sds/">SDS</a>)</strong> | 영구 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 및 객체 보관 | [분산 파일 시스템](/studynote/02_operating_system/09_file_system/553_distributed_file_system/), 블록 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 매핑 | EBS (블록), S3 (객체) | 거대한 공용 창고 할당 |
| <strong>네트워크 <a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a>)</strong> | 통신 트래픽 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)/격리 | [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/) ([VXLAN](/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/)), [가상 스위치](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/) | [VPC](/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/), [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group | 가상의 투명 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 연결 |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a>/제어 평면</strong> | 자원 생명주기 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 제어 | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이, [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/), 미터링 엔진 | AWS [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), CloudWatch | 인프라 중앙 통제실 |
| <strong><a href="/studynote/09_security/11_iam_access_control/526_iam/">IAM</a> (Identity &amp; Access)</strong> | 자원에 대한 접근/권한 제어 | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/), 토큰 기반 임시 권한(STS) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | AWS [IAM](/studynote/09_security/11_iam_access_control/526_iam/) Role | 출입증 발급 게이트 |

다음 구조도는 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 환경 내에서 사용자의 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청이 실제 물리 서버(Host)에서 VM으로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 내부 구조를 나타낸다.

```text
이 도식은 IaaS의 제어 평면(Control Plane)과 데이터 평면(Data Plane)이 분리되어, 사용자의 프로비저닝 명령이 어떻게 하이퍼바이저로 전달되는지를 보여준다.

+--------------- [IaaS Control Plane / IaaS 제어 평면] ---------------+
| [사용자 API/CLI] --> [API Server & Auth (IAM)]       |
|                             |                        |
|                     [Resource Scheduler / 스케줄러]  |
+-----------------------------|------------------------+
                              v (Hypercall / API)
+--------------- [ IaaS Data Plane (물리 서버) ] --------+
|  +----- VM 1 -----+  +----- VM 2 -----+              |
|  | Guest OS (Web) |  | Guest OS (DB)  |              |
|  +----------------+  +----------------+              |
|  =========== Hypervisor (KVM / Nitro) ===========    |
|  [ 가상 스위치(OVS) ]  ↔  [ 오버레이 네트워크 통로 ] |
|  [ CPU / RAM 할당 ]  ↔  [ 물리 NIC / Disk I/O  ]     |
+------------------------------------------------------+
```

이 흐름의 핵심은 제어 평면의 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 수만 대의 물리 노드 중 자원 여유가 있는 노드를 탐색하고, 해당 노드의 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)에게 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 지시한다는 점이다. 특히 최신 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 벤더(예: AWS Nitro System)는 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 부하(네트워크, 스토리지 I/O 처리)를 메인 CPU가 아닌 별도의 하드웨어 카드([DPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/)/SmartNIC)로 오프로드(Offload)하여, [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 오버헤드를 제로에 가깝게 만들고 보안을 극대화한다. 실무에서는 이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면의 격리 수준([가상 스위치](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/), 보안 그룹)을 철저히 설계해야만 [멀티 테넌트](/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/) 환경의 해킹 위협([Hypervisor Escape](/studynote/13_cloud_architecture/01_virtualization/060_hypervisor_escape_vm_security_threat/) 등)을 막을 수 있다.

📢 **섹션 요약 비유**: 건물(물리 서버) 전체를 관리하는 총지배인([하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/))이 고객(사용자 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))의 요청을 받아 순식간에 가벽을 세우고 수도관(가상 네트워크)을 연결하여 독립된 원룸([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 만들어내는 과정입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 모델은 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/), [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 모델과 명확한 책임 분담(Shared Responsibility Model)의 차이를 가진다.

| 항목 | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) (Infrastructure) | [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) (Platform) | 판단 포인트 |
|:---|:---|:---|:---|
| **제공 수준** | 서버([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)), 네트워크, 스토리지 볼륨 | OS, 미들웨어, 런타임, 런타임 프레임워크 | 사용자가 제어하길 원하는 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 범위 |
| **사용자 책임** | OS 패치, 보안, 런타임 설치, 애플리케이션 | 애플리케이션 코드, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 | 관리 오버헤드 vs 자유도 트래픽 |
| <strong>벤더 <a href="/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a> (<a href="/studynote/12_it_management/05_security_compliance/362_lock_in_portability/">Lock-in</a>)</strong> | 낮음 ([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 이미지를 타 클라우드로 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 가능) | 중간~높음 (특정 DB/런타임 환경 종속) | [멀티 클라우드 전략](/studynote/06_ict_convergence/03_cloud_infrastructure/189_multi_cloud_strategy_vendor_lock_in/) 가능성 |
| **장점** | 레거시 환경(모놀리식)의 가장 빠르고 쉬운 마이그레이션([Lift](/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift) | 인프라 관리 없이 비즈니스 로직 개발에만 집중 가능 | 전환 비용 (마이그레이션 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) |

다음은 온프레미스에서 클라우드로 넘어갈 때, 제어권과 관리 부담의 트레이드오프를 보여주는 상태 비교도이다.

```text
이 도식은 클라우드 서비스 모델에 따른 '사용자의 관리 영역(노란색)'과 '클라우드 제공자의 관리 영역(파란색)'의 경계를 명확히 보여준다.

[On-Premise / 온프레미스]     [IaaS]           [PaaS]           [SaaS]
+----------+     +----------+     +----------+     +----------+
| Apps     |     | Apps     |     | Apps     |     | Apps     | (Data)
| Runtime  |     | Runtime  |     | Runtime  |     +----------+
| OS / DB  |     | OS / DB  |     +----------+     | OS / DB  |
| Virtual  |     +----------+     | Virtual  |     | Virtual  |
| Server   |     | Server   |     | Server   |     | Server   |
| Network  |     | Network  |     | Network  |     | Network  | (Provider)
+----------+     +----------+     +----------+     +----------+
```

[IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 모델은 사용자가 OS 계층부터 위쪽으로 모든 권한(Root Access)을 갖는다. 이는 커스텀 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 튜닝이나 상용 레거시 소프트웨어를 수정 없이 얹어 쓰기에는 최고지만, 반대로 말하면 OS 보안 패치, 미들웨어 업그레이드, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 스크립트를 사용자가 직접 구성해야 한다는 뜻이다. 반면 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 방식은 단건 지연은 다소 크지만 운영 복잡도를 벤더에게 전가할 수 있어, 신규 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 앱을 구축할 때 더 유리할 수 있다.

📢 **섹션 요약 비유**: IaaS는 빈 렌터카를 빌려 내가 직접 운전하고 기름도 넣는 것이고, PaaS는 운전기사가 포함된 택시를 타는 것이며, SaaS는 정해진 노선대로 알아서 움직이는 대중교통([버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/))을 타는 것입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 IaaS를 도입하거나 아키텍처를 설계할 때는 보안과 비용 최적화가 가장 큰 판단 기준이 된다.

1. <strong>마이그레이션 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> (Rehost vs <a href="/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/">Refactor</a>)</strong>: 레거시 시스템을 IaaS로 가장 빨리 옮기는 방법은 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 이미지를 그대로 복사하는 Rehost ([Lift](/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) and Shift)이다. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 마이그레이션 속도는 빠르지만 클라우드의 [탄력성](/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/) 이점을 100% 누릴 수 없으므로, 추후 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반으로 [Refactoring](/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/) 하는 2단계 로드맵이 필수적이다.
2. <strong>비용 낭비(Zombie <a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>) 방지</strong>: 클릭 몇 번으로 서버가 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되다 보니, 테스트용으로 띄워둔 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 인스턴스가 끄는 것을 잊어버린 채 방치되어 과금되는 '좀비 인스턴스'가 흔히 발생한다. 리소스 태깅(Tagging)을 강제하고, 주기적으로 사용률 5% 미만 자원을 셧다운하는 [FinOps](/studynote/12_it_management/05_security_compliance/344_finops/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 등)을 설계해야 한다.
3. <strong>네트워크 격리 (<a href="/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/">VPC</a> / Subnet)</strong>: [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 환경에서 DB 서버에 외부 퍼블릭 IP를 할당하는 것은 치명적 안티패턴이다. 웹 서버(Public Subnet)와 DB 서버(Private Subnet)를 엄격히 분리하고, 외부 접근은 배스천 호스트([Bastion Host](/studynote/09_security/05_web_app_security/218_bastion_host_dmz_security/))나 VPN을 통과하도록 [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group)을 겹겹이 쳐야 한다.

```text
[실무 IaaS 고가용성 및 보안 라우팅 플로우]
이 구조도는 IaaS 도입 시 장애 전파를 막고 보안을 확보하기 위한 멀티-가용영역(AZ) 배치의 모범 사례를 보여준다.

[Internet / 인터넷]
   v
[ Internet Gateway / WAF ]
   v
+--[ VPC (Virtual Private Cloud) ]---------------------------+
|  +-[ 가용영역(AZ) A ]-+           +-[ 가용영역(AZ) B ]-+   |
|  | Public Subnet      | -- LB --> | Public Subnet      |   |
|  |  [Web VM / 웹 VM]  |           |  [Web VM / 웹 VM]  |   |
|  +--------------------+           +--------------------+   |
|  | Private Subnet     | -- Sync - | Private Subnet     |   |
|  |  [DB Master VM / DB 마스터 VM]    |           |  [DB Replica VM / DB 레플리카]   |   |
|  +--------------------+           +--------------------+   |
+------------------------------------------------------------+
```

이 흐름도의 핵심은 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))을 제거하기 위해 서로 다른 물리적 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)(가용영역 A, B)에 인스턴스를 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 배치하고, DB를 프라이빗 서브넷에 숨겼다는 점이다. 실무에서는 이러한 구성을 수동 클릭으로 만들면 휴먼 에러가 필연적으로 발생하므로, [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)([Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) 코드로 작성하여 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 자동 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 거친 후 프로비저닝해야 한다.

📢 **섹션 요약 비유**: 아무리 튼튼한 레고 블록([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 자원)이 제공되어도, 설명서([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드) 없이 손으로 대충 조립하면 쉽게 무너집니다. 뼈대부터 다중 안전장치(AZ [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), 프라이빗망 격리)를 고려해 조립해야만 튼튼한 성이 됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

IaaS의 도입은 기업 인프라 운영의 민첩성과 유연성을 극대화한다. 개발팀은 인프라 대기 시간 없이 즉시 실험하고 실패할 권리를 얻게 되며, 이는 곧 소프트웨어 딜리버리 속도의 비약적 향상([DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 개선)으로 이어진다.

| 지표 | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 도입 전 | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 운영 모범 사례 적용 후 |
|:---|:---|:---|
| 인프라 [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) | 수 주 소요 (장비 반입) | 5분 이내 ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 자동화) |
| 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간([RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))| 수 시간 ~ 수 일 (수동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | 수 분 (오토스케일링 및 AZ 페일오버) |
| 비용 구조 | 고정 자본 투자 (100% 낭비 위험) | 트래픽 연동 변동 비용 (초 단위 낭비 제거)|

미래의 IaaS는 단순한 가상 머신 임대를 넘어, 클라우드 벤더의 전용 칩셋([DPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/), 맞춤형 ARM 프로세서)을 통해 베어메탈 급의 성능을 제공하는 방향으로 진화 중이다. 또한, 사용자 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내부에 클라우드 장비의 축소판을 갖다 놓는 [분산 클라우드](/studynote/06_ict_convergence/03_cloud_infrastructure/242_distributed_cloud_edge_computing_aws_outposts/)(AWS Outposts, Azure [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/)) 형태로 확장되며 온프레미스와 퍼블릭 클라우드의 경계를 지우고 있다. 결론적으로 IaaS는 현대 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 애플리케이션이 딛고 서는 가장 견고하고 필수적인 대지(Ground) 역할을 지속할 것이다.

📢 **섹션 요약 비유**: IaaS는 현대 디지털 비즈니스의 '도로망'입니다. 내가 직접 아스팔트를 깔 필요 없이, 원하는 크기의 고속도로 차선을 필요한 시간만큼만 열어 물류([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 초고속으로 실어 나르는 최적의 물류 기반입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- [소프트웨어 정의 데이터센터](/studynote/03_network/17_sdn_nfv/858_sddc_software_defined_data_center_infrastructure/) ([SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/)) | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) 인프라를 논리적으로 분할하고 API로 제어하는 기반 철학
- [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([Hypervisor](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)) | 물리 서버 위에 다수의 가상 머신을 띄우고 CPU/RAM을 중재하는 S/W
- [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) ([Immutable Infrastructure](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)) | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) VM을 수정하지 않고 패치 시 완전히 새로운 VM으로 교체 배포하는 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 유지 기법
- [데브옵스](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) / [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)) | [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) API를 호출하여 전체 인프라망을 선언형 코드로 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리하는 도구
- [베어메탈 클라우드](/studynote/01_computer_architecture/15_advanced_topics/629_bare_metal_cloud/) ([Bare Metal Cloud](/studynote/01_computer_architecture/15_advanced_topics/629_bare_metal_cloud/)) | [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 오버헤드 없이 강력한 DB 성능을 위해 클라우드 내 물리 서버 전체 단독 임대받는 모델

### 📈 관련 키워드 및 발전 흐름도

```text
[소프트웨어 정의 데이터센터 (SDDC)]
    |
    v
[하이퍼바이저 (Hypervisor)]
    |
    v
[불변 인프라 (Immutable Infrastructure)]
    |
    v
[데브옵스 / IaC (테라폼)]
    |
    v
[베어메탈 클라우드 (Bare Metal Cloud)]
```

이 흐름도는 [소프트웨어 정의 데이터센터](/studynote/03_network/17_sdn_nfv/858_sddc_software_defined_data_center_infrastructure/) ([SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/))에서 출발해 [베어메탈 클라우드](/studynote/01_computer_architecture/15_advanced_topics/629_bare_metal_cloud/) ([Bare Metal Cloud](/studynote/01_computer_architecture/15_advanced_topics/629_bare_metal_cloud/))까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 컴퓨터 게임을 만들려면 비싼 컴퓨터 부품을 직접 다 사서 조립해야 했어요.
2. IaaS는 엄청나게 큰 슈퍼컴퓨터 공장에서 내가 원하는 만큼의 컴퓨터 화면과 부품을 인터넷으로 빌려주는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)예요.
3. 클릭 몇 번이면 내 방에 최고급 컴퓨터가 생기는 것과 같고, 다 쓰고 나면 바로 반납해서 돈을 아낄 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1 / 371

<- **이전**: (첫 번째 글입니다)

**다음**: [3. PaaS (Platform as a Service) - OS, 런타임, 미들웨어, DB가 세팅된 개발/운영 플랫폼 제공 (AWS](/studynote/13_cloud_architecture/01_virtualization/003_paas/) ->

---
