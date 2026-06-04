---
title: "872. 서비스 체이닝 (SFC)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝은 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝을 이해하면 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 기계, [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 기계, L4 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 기계를 사서, 1번 기계 엉덩이에 선을 꽂아 2번 기계 입구에 꽂고, 2번 엉덩이 선을 3번 입구에 꽂았습니다.
- **비극 발생**: 만약 중간에 '웹 필터링' 장비를 하나 더 끼워 넣고 싶으면? 주말 새벽 2시에 엔지니어가 전산실에 가서 물리 랜선을 다 뽑고 다시 꽂아야(Re-cabling) 했습니다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단은 필수였고 확장성은 제로였습니다.

```text
[VIM (Virtualised Infrast…]
    |
    v
[서비스 체이닝]
    |
    +---> [NSH]
```

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: [NFV](/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) 환경에서 허공에 분산되어 떠 있는 수많은 [가상 네트워크 기능](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/) 앱들([VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/): v방화벽, vIPS, vLB 등)을, 물리적 랜선 연결 없이 <strong>소프트웨어 정의 네트워크(<a href="/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a>) <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 기술을 이용해 특정 트래픽이 내가 원하는 논리적 순서대로 빠짐없이 징검다리처럼 통과하도록 강제로 실(경로)을 엮어주는 차세대 트래픽 스티어링(Steering) 기술</strong>입니다.

```text
[VIM (Virtualised Infrast…]
    |
    v
[서비스 체이닝]
    |
    +---> [NSH]
```

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

선이 없는데 패킷이 어떻게 순서를 알고 1번, 2번, 3번 앱을 정확히 찾아갈까요? 850번 문서의 뇌([SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러)가 조종합니다.

1. <strong>지시 하달 (<a href="/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a> <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a>)</strong>:
   - 중앙 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러가 밑바닥 [가상 스위치](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/)([OVS](/studynote/03_network/17_sdn_nfv/860_ovs_open_vswitch_sdn_openflow/))들에게 플로우 테이블(엑셀 장부)을 쫙 뿌립니다.
   - "밖에서 들어온 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 트래픽은 <strong>무조건 목적지 무시하고 1번 가상 <a href="/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/">방화벽</a>으로 꺾어버려(Steering)!</strong> [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)에서 토해내면 <strong>그다음엔 2번 <a href="/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/">IPS</a> 서버로 꺾어!</strong>"
2. **동적 룰(Rule) 변경의 사기성**:
   - 주말에 갑자기 '웹 필터링' 가상 앱([VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/))을 하나 새로 허공에 띄웠습니다.
   - 관리자가 마우스로 체인 순서를 `방화벽 ➜ 필터링 ➜ IPS`로 쏙 드래그 앤 드롭합니다.
   - [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러가 0.1초 만에 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 룰을 업데이트합니다. 전산실에 가서 랜선을 뽑을 필요 단 하나 없이, 1초 만에 징검다리의 순서가 완벽하게 바뀝니다. (무중단 인프라 혁신)

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [VIM](/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/) (Virtualised Infrast…가 기반 조건을 만든다면, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝은 그 위에서 핵심 메커니즘을 구현하고, NSH는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [VIM](/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/) (Virtualised Infrast…의 기반 정리 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝의 핵심 동작 | NSH의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

패킷이 징검다리를 건널 때 길을 잃지 않게 붙여주는 '놀이공원 자유이용권 팔찌'입니다. (873번 문서에서 상세히 다룸)
- 패킷 겉면에 <strong><a href="/studynote/03_network/17_sdn_nfv/873_nsh_network_service_header_sfc_metadata/">NSH</a> 꼬리표(헤더)</strong>를 찰싹 붙여둡니다. 이 꼬리표에는 "너는 1번 체인 코스를 밟고 있고, 방금 1번 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 무사 통과했어([Index](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)=2)"라는 정보가 적혀 있습니다.
- [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들은 패킷 내용물은 안 보고, 오직 이 [NSH](/studynote/03_network/17_sdn_nfv/873_nsh_network_service_header_sfc_metadata/) 팔찌의 징검다리 도장([Index](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))만 보고 "아, 1번 끝났네? 그럼 다음은 2번 IPS로 던질게!" 라며 기가 막히게 다음 코스로 릴레이 패스를 해줍니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

- [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)(773번)을 만들 때 절대적으로 쓰입니다.
- "자율주행 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 망 패킷은 ➜ [초저지연 검사기 [VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/)] ➜ [암호화 [VNF](/studynote/03_network/17_sdn_nfv/866_vnf_virtual_network_function_software_appliance/)] 순으로 체인을 엮어라!" 맞춤형 네트워크 길을 레고 블록처럼 무한대로 조립할 수 있는 클라우드 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 인프라의 완성판입니다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 기존 하드웨어 체이닝은 공장의 '일체형 컨베이어 벨트'입니다. 세척 기계, 건조 기계, 포장 기계가 볼트로 바닥에 단단히 고정되어 순서대로 쇠파이프로 이어져 있습니다. 중간에 '코팅 기계'를 하나 넣으려면 공장 바닥을 뜯고 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 용접을 다시 해야 합니다. <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 체이닝(SFC)</strong>은 기계들이 모두 바퀴가 달려 허공을 떠다니는 '자율주행 지게차 공장'입니다. 중앙 통제 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러)가 물건(패킷)을 실은 지게차에게 무전기로 "1번 세척기 텐트로 가! 끝났으면 2번 건조기 텐트로 가!"라고 실시간 네비게이션 경로(체인)를 머릿속에 쏴줍니다. 코팅 기계를 중간에 추가하고 싶으면 기계 위치는 냅두고, 지게차의 네비게이션 경로만 '세척기 ➜ 코팅기 ➜ 건조기'로 마우스 클릭 한 번에 쓱 바꿔주면 끝나는, 랜선 없는 극한의 논리적 조립 라인입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [VIM](/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/) (Virtualised Infrast… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 경로 결정을 담당한다. |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane) | 실제 패킷 전달을 수행한다. |
| [NSH](/studynote/03_network/17_sdn_nfv/873_nsh_network_service_header_sfc_metadata/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: VIM (Virtualised Infrast…]
    |
    v
[현재 개념: 서비스 체이닝]
    |
    +---> [확장 A: NSH]
    +---> [확장 B: 프로그래머블 네트워크]
```

[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체이닝는 [VIM](/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/) (Virtualised Infrast…에서 출발해 현재 메커니즘을 정교화하고, 이후 NSH와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 993 / 1120

<- **이전**: [871. VIM (가상화 인프라 관리자)](/studynote/03_network/17_sdn_nfv/871_vim_virtualised_infrastructure_manager_openstack_k8s/)
**다음**: [873. 네트워크 서비스 헤더 (NSH)](/studynote/03_network/17_sdn_nfv/873_nsh_network_service_header_sfc_metadata/) ->

---
