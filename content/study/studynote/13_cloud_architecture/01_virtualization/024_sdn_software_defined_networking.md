+++
weight = 24
title = "24. SDN (Software Defined Networking) — 소프트웨어 정의 네트워킹"
date = "2026-04-29"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[633_sdn_whitebox|SDN]] ([[215_sdn_software_defined_networking_openflow|Software Defined Networking]], [[850_sdn_software_defined_networking_concept|소프트웨어 정의 네트워킹]])은 네트워크 장비의 제어 평면(Control Plane)과 [[001_dikw_pyramid|데이터]] 전송 평면([[001_dikw_pyramid|Data]] Plane)을 분리하여, 중앙 집중형 컨트롤러([[633_sdn_whitebox|SDN]] Controller)가 전체 네트워크를 소프트웨어로 프로그래밍·관리하는 아키텍처다.
> 2. **가치**: 전통 네트워크는 각 장비([[238_switch_operation_principles|스위치]]·라우터)가 독립적으로 제어 로직을 실행하여 복잡한 변경이 장비별 개별 [[009_config|설정]]을 요구하지만, SDN은 컨트롤러에서 전체 네트워크를 코드로 제어하여 민첩성(Agility)·자동화·비용 절감을 달성한다.
> 3. **판단 포인트**: SDN의 핵심 약점은 컨트롤러의 [[454_spof|단일 장애점]]([[454_spof|SPOF]], Single Point of Failure) 위험이다. 컨트롤러 장애 시 전체 네트워크 제어가 불능이 되므로, HA(High [[452_availability|Availability]]) 클러스터 컨트롤러 구성과 장애 시 [[001_dikw_pyramid|데이터]] 평면 독립 동작(Fail-open/Fail-close) 전략이 필수다.

---

## Ⅰ. 개요 및 필요성

전통 네트워크에서 [[238_switch_operation_principles|스위치]]·라우터는 제어 로직([[365_bgp_border_gateway_protocol_path_vector|BGP]], [[357_ospf_open_shortest_path_first_overview|OSPF]], [[570_stp_vs_mtp|STP]] 등)과 패킷 포워딩을 내장하여 "[[136_variance|분산]] 제어" 방식으로 동작한다. 네트워크 변경이 필요하면 각 장비에 CLI로 개별 접속하여 [[009_config|설정]]해야 하는 비효율이 있다.

SDN은 이 제어 로직을 중앙 컨트롤러로 추출하여 "소프트웨어처럼" 관리한다.

```text
┌────────────────────────────────────────────────────────────┐
│            SDN 3계층 아키텍처                               │
├────────────────────────────────────────────────────────────┤
│  애플리케이션 레이어 (Application Layer)                     │
│  [네트워크 앱: 로드밸런서, 방화벽, 트래픽 엔지니어링]           │
│       │ 노스바운드 API (Northbound API, REST)               │
│  제어 레이어 (Control Layer)                                │
│  [SDN 컨트롤러: OpenDaylight, ONOS, Cisco ACI]             │
│       │ 사우스바운드 API (Southbound API, OpenFlow)         │
│  인프라 레이어 (Infrastructure/Data Layer)                  │
│  [물리·가상 스위치: 패킷 포워딩만 담당]                        │
└────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 전통 네트워크는 각 교통경찰이 자기 교차로를 독립 관리하는 것이고, SDN은 중앙 교통 관제센터(컨트롤러)가 도시 모든 신호를 소프트웨어로 일괄 제어하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] — 사우스바운드 [[295_protocol_field_tcp_udp_icmp|프로토콜]]

OpenFlow는 [[633_sdn_whitebox|SDN]] 컨트롤러와 [[238_switch_operation_principles|스위치]] 사이의 표준 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]]로, 컨트롤러가 [[238_switch_operation_principles|스위치]]의 플로우 테이블(Flow Table)에 직접 규칙을 설치한다.

```text
컨트롤러 → [OpenFlow 메시지: "IP=10.0.0.5면 포트3으로 전송"]
스위치 플로우 테이블 업데이트 → 패킷 도착 시 테이블 매칭 후 포워딩
```

### [[633_sdn_whitebox|SDN]] vs 전통 네트워크 비교

| 항목 | 전통 네트워크 | [[633_sdn_whitebox|SDN]] |
|:---|:---|:---|
| **제어 방식** | [[136_variance|분산]] (장비별) | 중앙 집중 (컨트롤러) |
| **[[009_config|설정]] 변경** | 장비별 CLI 접속 | 컨트롤러 [[014_api_posix|API]] 1회 호출 |
| **프로그래밍** | 제한적 (CLI/[[528_snmp_simple_network_management_protocol|SNMP]]) | 완전 프로그래밍 가능 |
| **[[454_spof|SPOF]] 위험** | 없음 ([[136_variance|분산]]) | 있음 (컨트롤러) |
| **주요 활용** | 전통 엔터프라이즈 | 클라우드 DC, [[865_nfv_network_functions_virtualization_architecture|NFV]] |

- **📢 섹션 요약 비유**: SDN은 항공 관제 시스템과 같다. 각 비행기(패킷)가 스스로 항로를 결정하는 대신, 관제탑(컨트롤러)이 모든 비행기의 경로를 통합 관리한다. 효율적이지만 관제탑이 고장나면 전체가 위험하다.

---

## Ⅲ. 비교 및 연결

| 기술 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| **[[865_nfv_network_functions_virtualization_architecture|NFV]] (Network Function [[190_virtualization_computing_architecture_cloud|Virtualization]])** | SDN의 보완 기술 | 네트워크 기능([[690_firewall_generation_evolution|방화벽]] 등)을 VM으로 [[015_virtualization|가상화]] |
| **[[855_openflow_standard_protocol_sdn_southbound|OpenFlow]]** | [[633_sdn_whitebox|SDN]] 사우스바운드 표준 | 컨트롤러-[[238_switch_operation_principles|스위치]] 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[205_kubernetes_container_orchestration|Kubernetes]] [[822_cni_container_network_interface_kubernetes|CNI]]** | [[633_sdn_whitebox|SDN]] 응용 | [[561_container_based_deployment|컨테이너]] 네트워킹에 [[633_sdn_whitebox|SDN]] 원리 적용 |
| **[[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]]** | [[633_sdn_whitebox|SDN]] [[001_dikw_pyramid|데이터]] 평면 | L2 오버레이 [[377_tunneling_mechanism_overview|터널링]]; SDN과 결합 |

클라우드에서 [[836_vpc_virtual_private_cloud_subnet_isolation|VPC]] ([[028_vpc|Virtual Private Cloud]])의 [[339_routing_overview_best_path_selection|라우팅]]·보안그룹 [[164_policy|정책]]이 [[633_sdn_whitebox|SDN]] 원리로 구현되며, AWS [[836_vpc_virtual_private_cloud_subnet_isolation|VPC]], Azure Virtual Network 모두 [[633_sdn_whitebox|SDN]] 기반이다.

- **📢 섹션 요약 비유**: AWS VPC를 클릭 몇 번으로 [[009_config|설정]]하는 것이 바로 SDN의 힘이다. 물리 케이블을 연결하는 대신 소프트웨어로 네트워크를 설계한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 대규모 클라우드 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 네트워크 자동화
1,000개 서버 규모 클라우드 DC에서 신규 테넌트 네트워크 [[528_provisioning|프로비저닝]] 자동화.

1. **기존 방식**: 네트워크 엔지니어가 [[224_vlan_virtual_lan_broadcast_domain|VLAN]]·[[339_routing_overview_best_path_selection|라우팅]]·ACL을 장비별 수동 [[009_config|설정]] → 2주 소요.
2. **[[633_sdn_whitebox|SDN]] 도입 ([[539_netflow_sflow_traffic_monitoring|Cisco]] ACI)**: [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] + ACI API로 네트워크 [[164_policy|정책]] 코드화.
3. **자동화 결과**: 신규 테넌트 네트워크 [[528_provisioning|프로비저닝]] 2주 → 15분 단축 (99% 감소).
4. **추가 효과**: 네트워크 오설정 사고 70% 감소 (코드 검토·테스트 가능).

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- [[633_sdn_whitebox|SDN]] 컨트롤러를 단일 인스턴스로 운영하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]. 컨트롤러 장애 시 네트워크 전체의 제어가 불가능해진다. Active-Active 또는 Active-Standby HA 구성과 [[001_dikw_pyramid|데이터]] 평면의 Fail-open(마지막 [[164_policy|정책]]으로 계속 동작) 또는 Fail-close(모든 트래픽 차단) [[164_policy|정책]]을 사전에 결정해야 한다.

- **📢 섹션 요약 비유**: [[633_sdn_whitebox|SDN]] 컨트롤러 단일 운영은 도시 교통 관제를 서버 1대로 운영하는 것이다. 서버 장애 시 도시 전체 신호등이 멈춘다. 반드시 예비 관제 시스템(HA 컨트롤러)을 준비해야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **네트워크 민첩성** | [[014_api_posix|API]] 기반 프로그래밍 가능한 네트워크 |
| **자동화** | 코드로 네트워크 [[528_provisioning|프로비저닝]], [[793_iac_idempotency_template|IaC]] 통합 |
| **비용 절감** | [[859_whitebox_switch_open_hardware_nos|화이트박스 스위치]] + [[191_oss_license_compliance|오픈소스]] 컨트롤러 |

SDN은 [[782_o_ran_open_ran_white_box_interface|O-RAN]] (Open Radio Access Network, 개방형 무선 접속망)에서 [[418_5g_embb_urllc_mmtc_slicing|5G]] 기지국 제어에 적용되며, [[190_ai_llm_requirements_specification|AI]]/ML 기반 자율 네트워킹(Autonomous Networking)이 [[633_sdn_whitebox|SDN]] 컨트롤러의 의사결정을 자동화하는 미래 방향이다.

- **📢 섹션 요약 비유**: SDN은 네트워크의 소프트웨어화다. 하드웨어에 갇혀있던 네트워크 지능을 소프트웨어로 해방시켜, 클라우드처럼 API로 제어하고 코드로 자동화할 수 있게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[855_openflow_standard_protocol_sdn_southbound|OpenFlow]]** | SDN의 표준 사우스바운드 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[865_nfv_network_functions_virtualization_architecture|NFV]]** | SDN과 보완 [[083_relationship_in_er_model|관계]]; [[865_nfv_network_functions_virtualization_architecture|네트워크 기능 가상화]] |
| **[[205_kubernetes_container_orchestration|Kubernetes]] [[822_cni_container_network_interface_kubernetes|CNI]]** | [[633_sdn_whitebox|SDN]] 원리의 [[561_container_based_deployment|컨테이너]] 네트워크 적용 |
| **[[454_spof|SPOF]] ([[454_spof|단일 장애점]])** | [[633_sdn_whitebox|SDN]] 컨트롤러 HA 구성 필요 이유 |
| **[[782_o_ran_open_ran_white_box_interface|O-RAN]]** | [[418_5g_embb_urllc_mmtc_slicing|5G]] 기지국에 [[633_sdn_whitebox|SDN]] 적용한 개방형 무선망 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 네트워크 — 분산 제어, 장비별 독립 설정]
    │
    ▼
[SDN — 제어/데이터 평면 분리, 중앙 컨트롤러]
    │
    ▼
[NFV + SDN — 네트워크 기능 가상화 결합]
    │
    ▼
[클라우드 네트워킹 — VPC, Kubernetes CNI]
    │
    ▼
[AI 자율 네트워킹 — ML 기반 자동 트래픽 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SDN은 학교 모든 교실([[238_switch_operation_principles|스위치]])에 따로 선생님을 두는 대신, 교장선생님(컨트롤러) 한 명이 전체 학교를 소프트웨어로 관리하는 것이에요!
2. 교장선생님이 한 번만 지시하면 모든 교실이 동시에 바뀌어서, 학교 규칙 변경이 훨씬 빠르고 쉬워져요.
3. 클라우드 회사들이 수만 개의 서버 네트워크를 몇 분 만에 [[009_config|설정]]할 수 있는 이유가 바로 [[633_sdn_whitebox|SDN]] 덕분이랍니다!
