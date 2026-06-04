---
title: "769. SBA (Service Based Architecture 네트워크 기능 요소가 컨테이너/마이크로 서비스 RESTful API 간 메시지 연동 호출 통신 플랫폼 융합 모델 기반 구축 코어 서비스 규격 표준)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SBA는 차세대 통신 아키텍처에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: SBA를 이해하면 유연성과 확장성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어망([5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/)) 제어 평면의 모든 구성 요소([AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/), [SMF](/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/), [PCF](/studynote/03_network/15_nextgen_communication_architecture/772_pcf_policy_control_function_qos/) 등 네트워크 기능(NF))들을 단단한 하드웨어 장비가 아닌 독립적인 <strong>마이크로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>(Microservice)</strong> 형태의 소프트웨어로 쪼개고, <strong>이들 간의 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 교환 방식을 현대적인 웹 프로그래밍 표준인 <a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/2 및 <a href="/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/">RESTful API</a> 호출 방식으로 완전히 뜯어고친 아키텍처 플랫폼 융합 모델</strong>입니다. ([3GPP](/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) 릴리즈 15 표준)

```text
[5GC]
    |
    v
[SBA]
    |
    +---> [AMF]
```

- **📢 섹션 요약 비유**: SBA는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 구시대의 [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) ([Point-to-Point](/studynote/07_enterprise_systems/03_eai_esb_msa/142_point_to_point_integration_spaghetti/)) 메쉬 구조
- 4G LTE까지는 [MME](/studynote/03_network/15_nextgen_communication_architecture/754_mme_mobility_management_entity/) 장비, [HSS](/studynote/03_network/15_nextgen_communication_architecture/755_hss_home_subscriber_server/) 장비, S-GW 장비 사이에 마치 복잡한 거미줄처럼 <strong>1:1 전용 통신선(<a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">Reference</a> Point)</strong>이 얽히고설켜 있었습니다.
- **문제점**: 여기에 새로운 부가서비스 장비 하나를 추가하려면, 그 장비에서 [MME](/studynote/03_network/15_nextgen_communication_architecture/754_mme_mobility_management_entity/), HSS로 가는 통신선을 또 일일이 새로 뚫고 연결해야 하는 끔찍한 스파게티 코드(Spaghetti) 구조라 확장이 불가능에 가까웠습니다.

### 2. [SBA](/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/) [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)) 구조와 [RESTful API](/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/) 도입 🌟
- <strong>소프트웨어 <a href="/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/">버스</a>(<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> Based Interface)</strong>: 5G는 이 복잡한 거미줄을 싹둑 다 잘라버리고, 가운데에 거대한 고속도로(소프트웨어 통신 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)) 하나만 딱 깔아두었습니다.
- 모든 [AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/), [SMF](/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/) 등의 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)(NF)들은 이 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)에 꽂혀 있습니다.
- AMF가 [HSS](/studynote/03_network/15_nextgen_communication_architecture/755_hss_home_subscriber_server/)(가입자 DB) 정보가 필요하면, 1:1 [전용선](/studynote/03_network/05_lan_wan_l2_devices/266_leased_line_basics_e1_t1_t3/)으로 무겁게 통신(Diameter [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))하는 것이 아니라, <strong>웹 개발자가 서버에서 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 당겨올 때 쓰는 방식인 <code>HTTP GET /구독자정보/홍길동</code> 이라는 <a href="/studynote/03_network/19_frequent_topics_terms/974_restful_api_stateless_http_methods_uri/">RESTful API</a></strong>를 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(단톡방)에 가볍게 휙 던집니다. [HSS](/studynote/03_network/15_nextgen_communication_architecture/755_hss_home_subscriber_server/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)은 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 형태로 가볍게 응답해 줍니다.

1. <strong>클라우드 네이티브와 마이크로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)</strong>:
   - 거대한 통신 소프트웨어를 작고 독립적인 기능([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))으로 쪼갰기 때문에, 통신사 서버([AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/)) 하나가 다운되어도 전체 망이 죽지 않고 옆에 켜진 새 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/) 2호기)가 즉시 일을 이어받는 오토 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)(Auto-scaling)이 가능해졌습니다.
2. **NRF (Network Repository Function)를 통한 플러그 앤 플레이**:
   - 중앙에 NRF라는 특별한 '전화번호부([DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/))' [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 있습니다.
   - 새로운 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)(예: 자율주행 특화 제어기)을 서버실에 새로 띄우면, 자기가 스스로 NRF에 "나 태어났고, 자율주행 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 지원해!"라고 등록([Register](/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/))합니다. 다른 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)들은 NRF 검색 한 번으로 1초 만에 이 새 장비와 대화를 시작할 수 있습니다(Discovery).
3. **IT와 통신(Telco)의 융합**:
   - 통신망이 전 세계 IT 표준인 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/REST를 쓰게 되면서, 외부의 게임 개발자나 클라우드 회사들이 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통신망(슬라이싱 등)에 직접 접속해 자기들 앱을 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 망과 한 몸처럼 연동하기가 미친 듯이 쉬워졌습니다.

```text
[5GC]
    |
    v
[SBA]
    |
    +---> [AMF]
```

- **📢 섹션 요약 비유**: 옛날 4G 구조는 회사 부서끼리 업무 연락을 할 때, 1층 영업부에서 3층 재무부 책상까지 매번 종이컵 전화기 선([P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) [전용선](/studynote/03_network/05_lan_wan_l2_devices/266_leased_line_basics_e1_t1_t3/))을 수십 가닥 직접 연결해 놓고 썼던 촌스러운 아날로그 구조입니다. [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [SBA](/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/) 구조는 부서 간의 종이컵 실을 가위로 싹둑 잘라버리고, 회사 전체 '사내 슬랙(Slack/단톡방)' 하나를 판 것입니다([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)). 영업부([AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/))가 단톡방에 `@재무부(HSS) 홍길동 예산 줘(REST API)`라고 카톡을 치면, 재무부가 즉각 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([JSON](/studynote/11_design_supervision/06_exam_summary/343_json/))을 올려줍니다. 새 부서가 생겨도 단톡방에 초대(NRF 등록)만 하면 1초 만에 전사 통신이 완료되는 혁명적인 유연성입니다.

---

## Ⅲ. 비교 및 연결

SBA를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 5GC가 기반 조건을 만든다면, SBA는 그 위에서 핵심 메커니즘을 구현하고, AMF는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 유연성과 확장성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 5GC의 기반 정리 | SBA의 핵심 동작 | AMF의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: SBA는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 SBA를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/) 수준의 기본 대책으로 충분한지, 아니면 SBA가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 AMF와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 유연성 부족인지, 확장성 악화인지 먼저 분리한다.
2. SBA가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 AMF와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- SBA의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- 5GC와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: SBA를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

SBA는 차세대 통신 아키텍처를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: SBA는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [5GC](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기반 구조 ([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)-Based [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/)) | 기능을 느슨하게 결합해 유연성을 높인다. |
| [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) ([Network Slicing](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 요구사항을 논리적으로 분리한다. |
| [AMF](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 5GC]
    |
    v
[현재 개념: SBA]
    |
    +---> [확장 A: AMF]
    +---> [확장 B: AI 기반 네트워크 최적화]
```

SBA는 5GC에서 출발해 현재 메커니즘을 정교화하고, 이후 AMF와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 장난감 도시를 여러 구역으로 나누고 필요한 규칙만 골라 쓰는 것과 같아요.
2. 이 개념은 빠른 길, 안전한 길, 많은 사람이 쓰는 길을 각각 다르게 꾸미게 해줘요.
3. 그래서 미래 통신망이 더 똑똑하고 유연해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 890 / 1120

<- **이전**: [768. 5GC (5G Core Network 차세대 코어망 SBA 아키텍처)](/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/)
**다음**: [770. AMF (Access and Mobility Management Function / MME 대체)](/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/) ->

---
