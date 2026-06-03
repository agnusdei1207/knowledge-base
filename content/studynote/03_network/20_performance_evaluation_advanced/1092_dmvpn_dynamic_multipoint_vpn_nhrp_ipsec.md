+++
title = "1092. DMVPN 동적 라우팅 결합형 지점"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **구조**: 서울 본사([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) 라우터에 100개 지점(Spoke)이 방사형으로 터널([GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) over [IPsec](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/))을 뚫어놓은 구조입니다.
- **재앙**: 지점과 지점끼리(Spoke-to-Spoke) 대용량 파일을 주고받으려 하면 무조건 본사 라우터([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/))를 거쳐서 가야 합니다. 본사 라우터의 트래픽이 터져버리고, 지점 간 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)(Delay)이 미친 듯이 치솟습니다.

```text
[GRE 일반 캡슐화 포맷 오버헤드]
    │
    ▼
[DMVPN 동적 라우팅 결합형 지점]
    │
    └──▶ [MPLS VPN L3 경로 격리 라벨 스위치]
```

- **📢 섹션 요약 비유**: [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 시스코가 개발한 기술로, 본사([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/))에만 스태틱 터널을 뚫어두면, **지점(Spoke)과 지점 간에 트래픽이 발생할 때만 실시간으로(동적으로) 1:1 다이렉트 [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 터널을 뚫어서 통신하고 끝나면 터널을 허물어버리는 지능형 멀티포인트 [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 아키텍처**입니다.

```text
[GRE 일반 캡슐화 포맷 오버헤드]
    │
    ▼
[DMVPN 동적 라우팅 결합형 지점]
    │
    └──▶ [MPLS VPN L3 경로 격리 라벨 스위치]
```

- **📢 섹션 요약 비유**: [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

이 마법은 1091번에서 배운 [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) 터널, [IPsec](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 암호화에 아래의 특별한 무기들을 얹어서 완성합니다.

### 1. mGRE (Multipoint [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/)) - 문어발 인터페이스
- 원래 [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) 터널은 출발지와 도착지를 고정해 두는 1:1 전용선입니다. 지점 100개면 터널(인터페이스) 100개를 세팅해야 합니다.
- **mGRE의 마법**: 터널 껍데기 설정창에 **목적지 IP(Destination IP)를 텅 비워버립니다.** 1개의 mGRE 인터페이스만 뚫어놓으면, 나중에 동적으로 IP를 받아와서 지점 1개든 1,000개든 1개의 포트로 다 통신할 수 있는 기적의 문어발 포트입니다.

### 2. NHRP (Next Hop Resolution [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) - "지점용 전화번호부" 🌟
DMVPN의 절대적인 뇌(심장)입니다. (ARP와 비슷한 역할을 합니다.)
- **등록 (Registration)**: 부산 지점(Spoke) 라우터가 켜지면, 서울 본사([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)) 라우터에게 툭 인사합니다. "나 방금 켜졌어, 내 공인 IP는 `1.1.1.1`이야." 서울 본사는 이 주소들을 **NHRP 캐시(전화번호부)**에 쫙 적어둡니다.
- **조회 (Resolution)**: 부산 직원이 광주 지점에 파일을 보내려 합니다. 부산 라우터가 서울 본사로 패킷을 쏘는 게 아니라, 일단 **본사한테 NHRP 편지만 날립니다. "야 광주 지점 공인 IP 좀 알려줘!"**
- 본사가 "광주는 `2.2.2.2`야"라고 대답해주면, 1085번 [IKEv2](/knowledge-base/studynote/09_security/03_network_security/280_ikev2/) 협상이 터지며 그 즉시 **부산과 광주 사이에 다이렉트 mGRE [IPsec](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 터널(Spoke-to-Spoke)이 1초 만에 쾅 뚫립니다.**

### 3. [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 프로토콜의 결합 ([EIGRP](/knowledge-base/studynote/03_network/07_network_layer_routing/355_eigrp_enhanced_igrp_dual_algorithm/), [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/))
- 터널만 뚫리면 길을 모릅니다. 그래서 [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) 터널 위로 [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) 같은 길 찾기 프로토콜을 얹어, 지점들이 켜질 때마다 "나 부산인데, 내 밑에 `192.168.10.x` 서브넷 있어!"라고 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 정보를 자동으로 본사에 퍼뜨리게 만듭니다.

[DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) 일반 캡슐화 포맷 오버헤드가 기반 조건을 만든다면, [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점은 그 위에서 핵심 메커니즘을 구현하고, [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) L3 경로 격리 라벨 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) 일반 캡슐화 포맷 오버헤드의 기반 정리 | [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점의 핵심 동작 | [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) L3 경로 격리 라벨 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- 본사 장비 세팅이 미치도록 편해집니다. 지점이 1개든 1,000개든 본사 라우터([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/))에 입력할 명령어는 단 10줄(mGRE 세팅)로 끝납니다. 지점이 늘어날 때마다 본사를 건드릴 필요가 없는 제로 터치 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)(Zero-Touch [Provisioning](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/))의 조상님입니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기존 **[Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) and Spoke [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)**은 부산 지사에서 광주 지사로 짐을 보낼 때, **무조건 서울 본사([Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 물류 센터)를 거쳐서 배달해야 하는 비효율적인 택배망**이었습니다. 부산과 광주는 서로의 전화번호(공인 IP)를 모르기 때문입니다. **[DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/)(동적 다중 지점 [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/))**은 이 한계를 부수기 위해 서울 본사에 **'114 글로벌 전화번호부 센터(NHRP 서버)'**를 세운 혁명입니다. 부산 지사가 켜질 때 본사에 자기 번호를 등록해 둡니다. 부산이 광주로 짐을 보내고 싶을 땐 짐을 서울로 안 보냅니다. 서울 본사엔 오직 "광주 전화번호 좀!" 하고 묻기만 합니다. 본사가 번호를 알려주면, 부산은 0.1초 만에 광주와 **'일회용 직통 고속도로(Spoke-to-Spoke 동적 터널)'**를 허공에 깔아버립니다. 고속도로를 타고 짐([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 다이렉트로 빛의 속도로 날아가고, 볼일이 끝나면 이 고속도로는 신기루처럼 허물어져 사라집니다. 본사로 몰리던 트래픽 병목을 완벽하게 0으로 만들어주는 동적 터널링의 결정판입니다.

---

## Ⅴ. 기대효과 및 결론

[DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) L3 경로 격리 라벨 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) 일반 캡슐화 포맷 오버헤드 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) L3 경로 격리 라벨 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: GRE 일반 캡슐화 포맷 오버헤드]
    │
    ▼
[현재 개념: DMVPN 동적 라우팅 결합형 지점]
    │
    ├──▶ [확장 A: MPLS VPN L3 경로 격리 라벨 스위치]
    └──▶ [확장 B: AI 기반 성능 예측]
```

[DMVPN](/knowledge-base/studynote/03_network/07_network_layer_routing/386_dmvpn_dynamic_multipoint_vpn_gre_ipsec_nhrp/) [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) 결합형 지점는 [GRE](/knowledge-base/studynote/03_network/07_network_layer_routing/378_gre_generic_routing_encapsulation/) 일반 캡슐화 포맷 오버헤드에서 출발해 현재 메커니즘을 정교화하고, 이후 [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) L3 경로 격리 라벨 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 201 / 1120

← **이전**: [1091. GRE 일반 캡슐화 포맷 오버헤드](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1091_gre_generic_routing_encapsulation_tunneling/)
**다음**: [1093. MPLS VPN L3 경로 격리 라벨 스위치](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1093_mpls_vpn_l3vpn_vrf_label_switching/) →

---
