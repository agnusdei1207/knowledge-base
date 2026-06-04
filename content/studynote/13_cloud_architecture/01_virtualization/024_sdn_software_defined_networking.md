+++
title = "24. SDN (Software Defined Networking) — 소프트웨어 정의 네트워킹"
date = 2026-04-29

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) ([Software Defined Networking](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/215_sdn_software_defined_networking_openflow/), [소프트웨어 정의 네트워킹](/knowledge-base/studynote/03_network/17_sdn_nfv/850_sdn_software_defined_networking_concept/))은 네트워크 장비의 제어 평면(Control Plane)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 평면([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane)을 분리하여, 중앙 집중형 컨트롤러([SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) Controller)가 전체 네트워크를 소프트웨어로 프로그래밍·관리하는 아키텍처다.
> 2. **가치**: 전통 네트워크는 각 장비([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)·라우터)가 독립적으로 제어 로직을 실행하여 복잡한 변경이 장비별 개별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 요구하지만, SDN은 컨트롤러에서 전체 네트워크를 코드로 제어하여 민첩성(Agility)·자동화·비용 절감을 달성한다.
> 3. **판단 포인트**: SDN의 핵심 약점은 컨트롤러의 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure) 위험이다. 컨트롤러 장애 시 전체 네트워크 제어가 불능이 되므로, HA(High [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 클러스터 컨트롤러 구성과 장애 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 독립 동작(Fail-open/Fail-close) 전략이 필수다.

---

## Ⅰ. 개요 및 필요성

전통 네트워크에서 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)·라우터는 제어 로직([BGP](/knowledge-base/studynote/03_network/07_network_layer_routing/365_bgp_border_gateway_protocol_path_vector/), [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/), [STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) 등)과 패킷 포워딩을 내장하여 "[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 제어" 방식으로 동작한다. 네트워크 변경이 필요하면 각 장비에 CLI로 개별 접속하여 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 하는 비효율이 있다.

SDN은 이 제어 로직을 중앙 컨트롤러로 추출하여 "소프트웨어처럼" 관리한다.

```text
+------------------------------------------------------------+
|            SDN 3계층 아키텍처                               |
+------------------------------------------------------------+
|  애플리케이션 레이어 (Application Layer)                     |
|  [네트워크 앱: 로드밸런서, 방화벽, 트래픽 엔지니어링]           |
|       | 노스바운드 API (Northbound API, REST)               |
|  제어 레이어 (Control Layer)                                |
|  [SDN 컨트롤러: OpenDaylight, ONOS, Cisco ACI]             |
|       | 사우스바운드 API (Southbound API, OpenFlow)         |
|  인프라 레이어 (Infrastructure/Data Layer)                  |
|  [물리·가상 스위치: 패킷 포워딩만 담당]                        |
+------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 전통 네트워크는 각 교통경찰이 자기 교차로를 독립 관리하는 것이고, SDN은 중앙 교통 관제센터(컨트롤러)가 도시 모든 신호를 소프트웨어로 일괄 제어하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [OpenFlow](/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/) — 사우스바운드 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)

OpenFlow는 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러와 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 사이의 표준 통신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로, 컨트롤러가 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 플로우 테이블(Flow Table)에 직접 규칙을 설치한다.

```text
컨트롤러 -> [OpenFlow 메시지: "IP=10.0.0.5면 포트3으로 전송"]
스위치 플로우 테이블 업데이트 -> 패킷 도착 시 테이블 매칭 후 포워딩
```

### [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) vs 전통 네트워크 비교

| 항목 | 전통 네트워크 | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) |
|:---|:---|:---|
| **제어 방식** | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) (장비별) | 중앙 집중 (컨트롤러) |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 변경</strong> | 장비별 CLI 접속 | 컨트롤러 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 1회 호출 |
| **프로그래밍** | 제한적 (CLI/[SNMP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/528_snmp_simple_network_management_protocol/)) | 완전 프로그래밍 가능 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a> 위험</strong> | 없음 ([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) | 있음 (컨트롤러) |
| **주요 활용** | 전통 엔터프라이즈 | 클라우드 DC, [NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) |

- **📢 섹션 요약 비유**: SDN은 항공 관제 시스템과 같다. 각 비행기(패킷)가 스스로 항로를 결정하는 대신, 관제탑(컨트롤러)이 모든 비행기의 경로를 통합 관리한다. 효율적이지만 관제탑이 고장나면 전체가 위험하다.

---

## Ⅲ. 비교 및 연결

| 기술 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/">NFV</a> (Network Function <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/">Virtualization</a>)</strong> | SDN의 보완 기술 | 네트워크 기능([방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 등)을 VM으로 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) |
| <strong><a href="/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/">OpenFlow</a></strong> | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 사우스바운드 표준 | 컨트롤러-[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 통신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">Kubernetes</a> <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/">CNI</a></strong> | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 응용 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 네트워킹에 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 원리 적용 |
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/817_vxlan_virtual_extensible_lan_mac_in_udp/">VXLAN</a></strong> | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 | L2 오버레이 [터널링](/knowledge-base/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/); SDN과 결합 |

클라우드에서 [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) ([Virtual Private Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/028_vpc/))의 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·보안그룹 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 원리로 구현되며, AWS [VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/), Azure Virtual Network 모두 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 기반이다.

- **📢 섹션 요약 비유**: AWS VPC를 클릭 몇 번으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 것이 바로 SDN의 힘이다. 물리 케이블을 연결하는 대신 소프트웨어로 네트워크를 설계한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 대규모 클라우드 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 네트워크 자동화
1,000개 서버 규모 클라우드 DC에서 신규 테넌트 네트워크 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) 자동화.

1. **기존 방식**: 네트워크 엔지니어가 [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/)·[라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)·ACL을 장비별 수동 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) -> 2주 소요.
2. <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a> 도입 (<a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/">Cisco</a> ACI)</strong>: [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) + ACI API로 네트워크 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 코드화.
3. **자동화 결과**: 신규 테넌트 네트워크 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) 2주 -> 15분 단축 (99% 감소).
4. **추가 효과**: 네트워크 오설정 사고 70% 감소 (코드 검토·테스트 가능).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러를 단일 인스턴스로 운영하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). 컨트롤러 장애 시 네트워크 전체의 제어가 불가능해진다. Active-Active 또는 Active-Standby HA 구성과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면의 Fail-open(마지막 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 계속 동작) 또는 Fail-close(모든 트래픽 차단) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 사전에 결정해야 한다.

- **📢 섹션 요약 비유**: [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러 단일 운영은 도시 교통 관제를 서버 1대로 운영하는 것이다. 서버 장애 시 도시 전체 신호등이 멈춘다. 반드시 예비 관제 시스템(HA 컨트롤러)을 준비해야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **네트워크 민첩성** | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반 프로그래밍 가능한 네트워크 |
| **자동화** | 코드로 네트워크 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 통합 |
| **비용 절감** | [화이트박스 스위치](/knowledge-base/studynote/03_network/17_sdn_nfv/859_whitebox_switch_open_hardware_nos/) + [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 컨트롤러 |

SDN은 [O-RAN](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/782_o_ran_open_ran_white_box_interface/) (Open Radio Access Network, 개방형 무선 접속망)에서 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국 제어에 적용되며, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 기반 자율 네트워킹(Autonomous Networking)이 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러의 의사결정을 자동화하는 미래 방향이다.

- **📢 섹션 요약 비유**: SDN은 네트워크의 소프트웨어화다. 하드웨어에 갇혀있던 네트워크 지능을 소프트웨어로 해방시켜, 클라우드처럼 API로 제어하고 코드로 자동화할 수 있게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/">OpenFlow</a></strong> | SDN의 표준 사우스바운드 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><a href="/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/">NFV</a></strong> | SDN과 보완 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/); [네트워크 기능 가상화](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/">Kubernetes</a> <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/">CNI</a></strong> | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 원리의 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 네트워크 적용 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a> (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">단일 장애점</a>)</strong> | [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 컨트롤러 HA 구성 필요 이유 |
| <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/782_o_ran_open_ran_white_box_interface/">O-RAN</a></strong> | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국에 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 적용한 개방형 무선망 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 네트워크 — 분산 제어, 장비별 독립 설정]
    |
    v
[SDN — 제어/데이터 평면 분리, 중앙 컨트롤러]
    |
    v
[NFV + SDN — 네트워크 기능 가상화 결합]
    |
    v
[클라우드 네트워킹 — VPC, Kubernetes CNI]
    |
    v
[AI 자율 네트워킹 — ML 기반 자동 트래픽 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SDN은 학교 모든 교실([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))에 따로 선생님을 두는 대신, 교장선생님(컨트롤러) 한 명이 전체 학교를 소프트웨어로 관리하는 것이에요!
2. 교장선생님이 한 번만 지시하면 모든 교실이 동시에 바뀌어서, 학교 규칙 변경이 훨씬 빠르고 쉬워져요.
3. 클라우드 회사들이 수만 개의 서버 네트워크를 몇 분 만에 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)할 수 있는 이유가 바로 [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 덕분이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 23 / 371

<- **이전**: [23. SDDC (Software-Defined Data Center) — 소프트웨어 정의 데이터센터](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/023_sddc_software_defined_data_center/)
**다음**: [25. SDS (Software Defined Storage) — 소프트웨어 정의 스토리지](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/025_sds_software_defined_storage/) ->

---
