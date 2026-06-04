---
title: "871. VIM (가상화 인프라 관리자)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VIM는 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: VIM를 이해하면 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 868번 MANO 아키텍처의 3계층 중 <strong>가장 맨 밑바닥에서, 물리적 서버/스토리지/네트워크 장비들(<a href="/studynote/03_network/17_sdn_nfv/867_nfvi_nfv_infrastructure_physical_virtual_resources/">NFVI</a>)을 <a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a>하여 거대한 자원 풀(Pool)로 만들고, 윗선(<a href="/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/">VNFM</a>, <a href="/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/">NFVO</a>)의 명령에 따라 가상머신(<a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>)이나 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>를 실제로 뚝딱 만들어내어 하드웨어 자원을 할당(Allocation)하고 회수하는 인프라 관리 플랫폼</strong>입니다.
- **실무의 제왕**: 이 VIM 자리를 전 세계 100% 독점하다시피 한 거대한 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 괴물이 바로 <strong>오픈스택(OpenStack)</strong>입니다. (최근엔 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 시대가 오며 <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a>(k8s)</strong>가 VIM의 자리를 급속도로 뺏어 먹고 있습니다.)

```text
[VNFM]
    |
    v
[VIM]
    |
    +---> [서비스 체이닝 (Service Chainin…]
```

- **📢 섹션 요약 비유**: VIM는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 무한한 가상 자원 찍어내기 ([Resource Allocation](/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/))
- 윗선([VNFM](/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/))에서 "가상 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 띄우게 방 하나 파줘([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출)"라고 명령서가 내려옵니다.
- VIM(오픈스택 Nova)은 전국 1만 대의 물리 서버의 램(RAM)과 CPU 엑셀 장부를 뒤적입니다. "오, 부산 3번 서버에 CPU 4코어 빈 공간 있네!"
- 즉시 3번 서버의 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)([KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/))에게 명령을 때려 <strong>CPU 4코어짜리 텅 빈 깡통 가상머신(<a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>)을 1초 만에 뚝딱 파내어 VNFM에게 상납</strong>합니다.

### 2. 가상 네트워크 핏줄 뚫어주기 (Network Connectivity)
- VM만 달랑 만들어주면 인터넷이 안 됩니다.
- VIM(오픈스택 Neutron)은 [OVS](/studynote/03_network/17_sdn_nfv/860_ovs_open_vswitch_sdn_openflow/)([가상 스위치](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/), 860번)를 조작해서 새로 파낸 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 엉덩이에 가상 랜선(VIF)을 푹 꽂아주고, 사설 IP `10.0.0.5`를 딱 세팅해서 위로 보고합니다.

### 3. 자원 감시 및 하자 보고 (Inventory & Telemetry) 🌟
- VIM은 땅 바닥의 흙(서버) 상태를 24시간 현미경으로 감시합니다.
- "10번 서버 하드디스크가 뻑났습니다! 5번 서버 온도가 100도입니다!"라는 비명 소리(물리적 장애)를 가장 먼저 수집하여, 위에 있는 사령관([NFVO](/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/))과 매니저([VNFM](/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/))에게 긴급 보고타전(Notification)을 날립니다. 이 보고를 받아야 VNFM이 앱([VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/))을 다른 서버로 살려서 이사(마이그레이션)시킬 수 있습니다.

```text
[VNFM]
    |
    v
[VIM]
    |
    +---> [서비스 체이닝 (Service Chainin…]
```

- **📢 섹션 요약 비유**: VIM의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- **1세대 VIM (OpenStack)**: 무거운 운영체제를 통째로 띄우는 가상머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) 시대의 절대 군주입니다. 통신사의 4G [EPC](/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/) 코어망은 다 오픈스택 VIM 위에서 돌아갑니다.
- <strong>2세대 VIM (<a href="/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">Kubernetes</a>, k8s) 🌟</strong>: 무거운 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 대신 가벼운 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/))로 모든 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/)(이젠 CNF라 부름)를 쪼개서 돌리는 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 시대의 새로운 VIM 대장입니다. 부팅 속도가 0.1초라 트래픽 폭주 대처([스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 능력이 오픈스택을 압살합니다.

VIM를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. VNFM가 기반 조건을 만든다면, VIM는 그 위에서 핵심 메커니즘을 구현하고, [서비스 체이닝](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Chainin…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | VNFM의 기반 정리 | VIM의 핵심 동작 | [서비스 체이닝](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Chainin…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: VIM는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- 아무리 위에서 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))이 화려하게 트래픽을 분석하고 오케스트레이션을 하려 해도, 바닥의 VIM(오픈스택)이 렉이 걸려서 가상머신을 제때 안 뱉어내면([프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) 클라우드 통신망 전체가 한순간에 멈춰버립니다. VIM의 안정성이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터의 멱살을 쥐고 있습니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: MANO가 거대한 빌딩 건설 회사라면, NFVO가 본사 회장님이고, VNFM이 인테리어 업자입니다. 그렇다면 <strong>VIM(<a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> 인프라 관리자)</strong>은 흙먼지 날리는 공사판 현장을 지휘하는 '골조 공사 노가다 현장 소장님(오픈스택)'입니다. 인테리어 업자([VNFM](/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/))가 "여기에 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 가구 들여놓을 거니까 방 좀 하나 만들어줘!" 하면, 현장 소장님(VIM)은 즉각 시멘트(물리 CPU)와 철근(물리 RAM) 재고를 쓱 파악한 뒤 인부들을 시켜 빈 콘크리트 방(가상머신 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 벽돌로 1초 만에 뚝딱 지어냅니다. 방에 수도관과 전기선(가상 랜선과 IP)까지 완벽하게 꽂아준 뒤 "방 다 뺐습니다! 가구 들이십쇼!"라고 위로 깍듯이 보고하는 가장 핵심적인 인프라 바닥의 일꾼 대장입니다.

---

## Ⅴ. 기대효과 및 결론

VIM는 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [서비스 체이닝](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Chainin…, 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: VIM는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [VNFM](/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 경로 결정을 담당한다. |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane) | 실제 패킷 전달을 수행한다. |
| [서비스 체이닝](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Chainin… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: VNFM]
    |
    v
[현재 개념: VIM]
    |
    +---> [확장 A: 서비스 체이닝 (Service Chainin…]
    +---> [확장 B: 프로그래머블 네트워크]
```

VIM는 VNFM에서 출발해 현재 메커니즘을 정교화하고, 이후 [서비스 체이닝](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Chainin…와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 992 / 1120

<- **이전**: [870. VNFM (VNF 매니저)](/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/)
**다음**: [872. 서비스 체이닝 (SFC)](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) ->

---
