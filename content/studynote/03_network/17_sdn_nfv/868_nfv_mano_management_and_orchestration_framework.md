+++
title = "868. NFV MANO 프레임워크"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크는 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크를 이해하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: ETSI(유럽통신표준협회)가 정의한 [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) 아키텍처의 맨 우측에 위치하는 최상위 중앙 통제 시스템으로, **모든 하드웨어 인프라 자원([NFVI](/knowledge-base/studynote/03_network/17_sdn_nfv/867_nfvi_nfv_infrastructure_physical_virtual_resources/))과 소프트웨어 네트워크 앱([VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/))들을 모니터링하고, 배포([생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)), 연결, 삭제, 확장을 100% 자동으로 지휘하는 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)(지휘) 및 관리 프레임워크**입니다.
- 통신사(SKT, KT)가 클라우드 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 망을 돌리기 위해 수천억 원을 주고 구축하는 운영의 핵심 심장입니다.

```text
[NFVI]
    │
    ▼
[NFV MANO 프레임워크]
    │
    └──▶ [NFVO]
```

- **📢 섹션 요약 비유**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MANO는 단일 프로그램이 아닙니다. 철저하게 계급이 나뉜 3명의 관리자로 이루어져 있습니다. (아주 중요합니다.)

### 1. [VIM](/knowledge-base/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/) ([가상화 인프라 관리자](/knowledge-base/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/), Virtualised Infrastructure Manager) - "땅 관리 소장"
- **가장 밑바닥 관리자 (871번 문서 상세)**
- **역할**: [NFVI](/knowledge-base/studynote/03_network/17_sdn_nfv/867_nfvi_nfv_infrastructure_physical_virtual_resources/)(하드웨어 서버와 [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)) 땅덩어리만 전문으로 관리합니다. "1번 서버 CPU 80% 찼습니다! 2번 서버 램 널널합니다!"라고 자원 현황을 윗선에 보고하고, 위에서 명령이 내려오면 멍청하게 "네, 2번 서버에 가상머신([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) 빈방 하나 파겠습니다" 하고 껍데기 방을 만들어 냅니다. (대표 솔루션: OpenStack, [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))

### 2. [VNFM](/knowledge-base/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/) ([VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) 매니저, [VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) Manager) - "앱 생명주기 의사"
- **중간 관리자 (870번 문서 상세)**
- **역할**: 빈방([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이 만들어지면 거기에 '[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 소프트웨어([VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/))'를 설치하고 생명줄을 쥐고 흔듭니다. "[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) 1호기 켜졌습니다! 어? 트래픽 몰려서 1호기가 힘들어하네요! 당장 2호기 하나 더 복제하겠습니다([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))!"라며 오직 특정 [VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) 앱 하나하나의 건강과 생사(Lifecycle)만을 전담 마크합니다.

### 3. [NFVO](/knowledge-base/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/) ([NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) 오케스트레이터, [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) Orchestrator) - "최고 존엄 총사령관" 🌟
- **맨 꼭대기의 신 (869번 문서 상세)**
- **역할**: 밑에 있는 VIM과 VNFM을 노예처럼 부리는 빅 픽처 설계자입니다.
- "자, 내일 서울 콘서트 열리니까, [VIM](/knowledge-base/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/) 너는 서울 서버에 빈방 10개 만들어! [VNFM](/knowledge-base/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/) 너는 그 10개 방에 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 5개, [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어 라우터 5개 깔아! 그리고 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 끝나면 라우터로 트래픽 흘러가게 길([서비스 체이닝](/knowledge-base/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/)) 뚫어놔!"라고 네트워크망 전체의 거시적인 숲을 그리고 지휘합니다.

```text
[NFVI]
    │
    ▼
[NFV MANO 프레임워크]
    │
    └──▶ [NFVO]
```

- **📢 섹션 요약 비유**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- 옛날엔 트래픽이 터지면 엔지니어 수십 명이 야근하며 서버에 코드를 치고 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)을 수동으로 늘렸습니다.
- MANO가 지배하는 통신망에서는 모든 것이 **자동(Automation)**입니다. VIM이 "CPU 모자람" 신호를 보내면, NFVO가 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))을 보고 즉시 VNFM에게 "[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 3대 추가해!"라고 지시하여, 인간이 커피 한 잔 마시고 오는 5분 사이에 네트워크가 알아서 스스로 커졌다가([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 다시 쪼그라드는(Scale-in) 살아 숨 쉬는 유기체가 완성됩니다.

[NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. NFVI가 기반 조건을 만든다면, [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크는 그 위에서 핵심 메커니즘을 구현하고, NFVO는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | NFVI의 기반 정리 | [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크의 핵심 동작 | NFVO의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) 생태계가 '거대한 교향악단(오케스트라)'이라면, **MANO 프레임워크**는 이 악단을 완벽하게 통제하는 지휘부입니다. 3명의 간부가 역할을 나눕니다. **[VIM](/knowledge-base/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/)(땅 관리자)**은 '무대 진행요원'입니다. 무대 위에 의자(가상머신)와 악보대(자원)를 가져다 세팅하는 막일을 합니다. **[VNFM](/knowledge-base/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/)(앱 관리자)**은 '악기별 파트장'입니다. 바이올린 연주자([VNF](/knowledge-base/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))의 컨디션(생명주기)을 관리하고 연주자가 부족하면 한 명 더 데려옵니다. 그리고 맨 꼭대기에 있는 **[NFVO](/knowledge-base/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/)(총사령관 지휘자)**는 숲을 봅니다. 지휘봉을 흔들며 "진행요원([VIM](/knowledge-base/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/)), 의자 10개 더 깔아! 파트장([VNFM](/knowledge-base/studynote/03_network/17_sdn_nfv/870_vnfm_vnf_manager_lifecycle_scaling_healing/)), 바이올린 10명 더 앉혀서 연주해!" 라며 무대 전체의 웅장한 교향곡(종단 간 네트워크 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))을 인간의 개입 없이 전자동으로 지휘해 내는 통신망의 마에스트로입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [NFVI](/knowledge-base/studynote/03_network/17_sdn_nfv/867_nfvi_nfv_infrastructure_physical_virtual_resources/) 수준의 기본 대책으로 충분한지, 아니면 [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 NFVO와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 부족인지, 자동화 수준 악화인지 먼저 분리한다.
2. [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 NFVO와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- NFVI와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크는 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [NFVO](/knowledge-base/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/), 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [NFVI](/knowledge-base/studynote/03_network/17_sdn_nfv/867_nfvi_nfv_infrastructure_physical_virtual_resources/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 경로 결정을 담당한다. |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane) | 실제 패킷 전달을 수행한다. |
| [NFVO](/knowledge-base/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: NFVI]
    │
    ▼
[현재 개념: NFV MANO 프레임워크]
    │
    ├──▶ [확장 A: NFVO]
    └──▶ [확장 B: 프로그래머블 네트워크]
```

[NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) MANO 프레임워크는 NFVI에서 출발해 현재 메커니즘을 정교화하고, 이후 NFVO와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 989 / 1120

← **이전**: [867. NFVI (NFV 인프라)](/knowledge-base/studynote/03_network/17_sdn_nfv/867_nfvi_nfv_infrastructure_physical_virtual_resources/)
**다음**: [869. NFVO (NFV 오케스트레이터)](/knowledge-base/studynote/03_network/17_sdn_nfv/869_nfvo_nfv_orchestrator_network_service_lifecycle/) →

---
