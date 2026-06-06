---
title: "171. Smart City Platform Architecture"
date: "2026-05-06"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스마트 시티 플랫폼은 도시 전역의 [사물인터넷](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) ([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), Internet of Things) 센서, 교통 시스템, 폐쇄회로 텔레비전 ([CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/), Closed-Circuit Television), 공공 업무 시스템을 공통 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 이벤트 흐름으로 묶는 도시 운영 플랫폼이다.
> 2. **가치**: 진짜 효과는 화면 통합이 아니라, 교통·안전·환경·에너지를 같은 상황 정보로 해석해 경보, 제어, 시민 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 하나의 폐루프 운영으로 연결하는 데서 나온다.
> 3. **판단 포인트**: 성공 여부는 센서 숫자보다 [데이터 표준화](/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/), 위치·시간 기준 통합, 엣지/중앙 처리 분담, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/), 부처 간 거버넌스를 얼마나 먼저 설계했는가에 달려 있다.

---

## Ⅰ. 개요 및 필요성

스마트 시티 플랫폼은 도시 인프라를 위한 단순 대시보드가 아니라, <strong>도시의 여러 운영 시스템이 같은 사건을 같은 좌표와 시간축으로 이해하게 만드는 공통 운영 기반</strong>이다. 교통 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 제어기, 미세먼지 센서, 방범 [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/), 스마트 가로등, 재난 경보 시스템이 각각 따로 움직이면 개별 관제는 가능해도 도시 단위의 종합 대응은 어렵다.

이 플랫폼이 필요해진 배경은 도시 문제가 더 이상 한 부서만의 문제가 아니기 때문이다. 화재는 소방만의 이벤트가 아니라 교통 우회, 대피 안내, 공기질 관리, 병원 이송, 시민 알림과 동시에 연결된다. 하지만 레거시 도시 시스템은 대개 "교통 센터", "방범 센터", "환경 센터"처럼 부서별로 따로 구축되어 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포맷과 운영 기준이 달랐다.

[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 유시티 (U-City, Ubiquitous City) 사업이 인프라 설치 중심으로 흐르며 한계를 드러낸 것도 이 지점이다. 센서와 네트워크를 많이 깔아도, 공통 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)과 연계 절차가 없으면 결국 또 다른 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)가 생긴다. 그래서 현대적 스마트 시티 플랫폼은 <strong>센서 설치 프로젝트</strong>가 아니라 <strong>도시 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 업무 흐름의 통합 프로젝트</strong>로 이해해야 한다.

아래 그림은 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)형 관제와 플랫폼형 관제의 차이를 보여 준다.

```text
+----------------------------------------------------------------------+
|          City operations: silo centers versus shared platform        |
+----------------------------------------------------------------------+
| Legacy                                                               |
| CCTV   -> safety center                                               |
| signals -> traffic center      each domain keeps its own IDs/events   |
| sensors -> env center                                                 |
|                                                                      |
| Smart City Platform                                                  |
| devices -> ingestion -> city data hub -> analytics -> command/apps   |
|                           |                    |                      |
|                           +- shared time / geo / asset context       |
+----------------------------------------------------------------------+
```

핵심은 "모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 곳에 모은다"가 아니라, <strong>서로 다른 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 같은 문맥으로 해석하게 만든다</strong>는 데 있다. 도시 운영에서 문맥이란 위치, 시간, 시설물 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), 사건 유형, 권한 범위를 의미한다.

- **📢 섹션 요약 비유**: 예전 도시는 경찰, 소방, 교통이 서로 다른 언어로 말하는 팀이었다면, 스마트 시티 플랫폼은 모두가 같은 지도와 같은 시계를 보며 움직이게 만드는 공동 작전실과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

스마트 시티 플랫폼의 핵심은 "수집"보다 "상황 이해와 제어"에 있다. 실무적으로는 보통 <strong>현장/엣지 계층 -> 통신 계층 -> 수집/연계 계층 -> 도시 <a href="/studynote/16_bigdata/09_platform/180_data_hub/">데이터 허브</a> 계층 -> <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>/거버넌스 계층</strong>으로 나뉜다. 여기서 가장 중요한 것은 중간의 도시 [데이터 허브](/studynote/16_bigdata/09_platform/180_data_hub/)가 단순 저장소가 아니라, 사건을 표준화된 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)로 바꾸는 변환기라는 점이다.

| 계층 | 주요 구성 | 역할 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| 현장/엣지 계층 | [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/), 센서, 가로등, [신호](/studynote/02_operating_system/02_process_thread/130_signal/)기, 차량 단말 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 1차 필터링, 현장 제어 | 영상 전처리, 비식별화, 장애 시 로컬 동작 |
| 통신 계층 | 5세대 이동통신 ([5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)), 광통신, [저전력 광역 통신망](/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) ([LPWAN](/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/), [Low-Power Wide-Area Network](/studynote/03_network/12_iot_wpan_edge/615_lpwan_low_power_wide_area_network/)), 와이파이 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송과 현장 연결 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 커버리지, 비용, 업링크 품질 |
| 수집/연계 계층 | [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/), 애플리케이션 프로그래밍 인터페이스 ([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 게이트웨이, [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) | 이기종 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집·표준화 | [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변환, 장비 벤더 호환 |
| 도시 [데이터 허브](/studynote/16_bigdata/09_platform/180_data_hub/) | 시계열 저장소, 공간 정보 시스템 (GIS, Geographic Information System), 규칙 엔진, [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) | 도시 상황을 공통 모델로 통합 | 시간·위치·자산 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 통합 |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)/거버넌스 계층 | 관제 화면, 시민 앱, 개방 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 보안/[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 체계 | 운영 의사결정과 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공 | 권한 관리, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 개방 수준, 책임 분담 |

도시 [데이터 허브](/studynote/16_bigdata/09_platform/180_data_hub/) 안에서는 서로 다른 장비가 보내는 값을 같은 의미 체계로 맞춘다. 예를 들어 "교차로 A의 차량 평균 속도", "학교 앞 보행자 밀도", "미세먼지 수치", "인근 병원 응급실 가용 병상"은 형식이 다르지만, 같은 위치와 시간 문맥 안에서 하나의 사건으로 묶일 수 있어야 한다. 이 문맥 통합이 있어야만 "사고가 났으니 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 우회 제어하고 시민 앱에 경보를 보내라" 같은 교차 영역 자동화가 가능하다.

또한 현대 플랫폼은 중앙 집중만으로는 버티지 못하므로 엣지 컴퓨팅을 함께 쓴다. 예를 들어 영상은 원본 전체를 매번 전송하지 않고, 현장 장치에서 사람 수·차량 번호·이상 행동 같은 특징을 먼저 추출한 뒤 중앙으로 보낸다. 이렇게 해야 통신비와 저장 부담을 줄이면서도 실시간성을 확보할 수 있다.

아래 구조는 스마트 시티 플랫폼이 단순 수집이 아니라 폐루프 제어라는 점을 보여 준다.

```text
+----------------------------------------------------------------------+
|            Smart city platform is a closed operational loop          |
+----------------------------------------------------------------------+
| Field devices -> Edge filter -> Event broker -> City data hub        |
|                                         |                            |
|                                         +- time series / GIS         |
|                                         +- digital twin / AI         |
|                                         +- rules / workflow          |
|                                              |                       |
|                                  operator UI / open API / alerts     |
|                                              |                       |
|                         signal control / dispatch / citizen service   |
+----------------------------------------------------------------------+
```

여기서 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 과 [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)은 부가 기능이 아니라, 도시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 "예측 가능한 운영 정보"로 바꾸는 핵심 확장 계층이다. [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 는 패턴을 찾고, [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)은 그 패턴이 공간 위에서 어떤 결과를 낼지 시뮬레이션한다.

- **📢 섹션 요약 비유**: 스마트 시티 플랫폼은 도시 곳곳의 눈과 귀에서 들은 소식을 한곳에서 판단하고 다시 손발로 명령을 내리는 신경계와 같다.

---

## Ⅲ. 비교 및 연결

스마트 시티 플랫폼을 제대로 이해하려면 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모아 두는 시스템"과 구분해야 한다. 플랫폼은 저장소가 아니라 <strong>운영 문맥과 행정 프로세스를 연결하는 실행 기반</strong>이다. 그래서 부처별 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/), 단순 [데이터 레이크](/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/), 플랫폼형 아키텍처는 비슷해 보여도 역할이 다르다.

| 비교 축 | 부처별 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/) 관제 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 중심 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) | 스마트 시티 플랫폼 |
| :--- | :--- | :--- | :--- |
| 초점 | 개별 업무 화면 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적재와 분석 | 실시간 상황 공유와 제어 |
| [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/) | 부서별 상이 | 일부 통합 | 도시 공통 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 중심 |
| 실시간성 | 낮음, 전화·수동 연계 | 분석 위주 | 이벤트 기반 자동 연계 |
| 제어 기능 | 해당 부서 내부만 | 거의 없음 | 교통·안전·에너지 간 교차 제어 |
| 생태계 확장 | 폐쇄적 | 제한적 | 개방 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반 민관 연계 가능 |

이 플랫폼은 다른 도시 기술과도 강하게 연결된다. [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)은 공간 시뮬레이션 계층이 되고, 협력 지능형 교통체계 ([C-ITS](/studynote/06_ict_convergence/02_iot_mobility/173_c_its_cooperative_intelligent_transport_systems/), Cooperative-Intelligent Transport Systems) 는 실시간 교통 제어 계층이 되며, 모빌리티 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형 (MaaS, Mobility [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 은 시민 접점 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계층이 된다. 즉 스마트 시티 플랫폼은 교통, 안전, 환경, 복지, 에너지를 한 번에 끌어안는 상위 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 층에 가깝다.

반대로 플랫폼이 성공하려면 기술보다 거버넌스가 더 중요해지는 구간이 있다. 어떤 부서가 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 언제까지 공개할지, 민간 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 어디까지 제어 명령을 보낼 수 있을지, 영상과 위치 정보는 어떤 수준으로 비식별화할지가 정해지지 않으면 아키텍처는 멈춘다.

따라서 스마트 시티 플랫폼은 "큰 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)"가 아니라, <strong>도시 전체가 같은 상황판을 보고 행동하게 만드는 공통 규칙 체계</strong>로 이해해야 한다.

- **📢 섹션 요약 비유**: 재료만 창고에 쌓아 둔다고 식당이 돌아가지 않듯, 스마트 시티도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 쌓는 것으로 끝나지 않고 주문·조리·서빙 규칙이 함께 있어야 진짜 플랫폼이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 설득력 있는 스마트 시티 사례는 교차 영역 대응이다. 예를 들어 학교 근처에서 화재와 교통 혼잡이 동시에 발생했다고 하자. 플랫폼은 연기 센서 경보, [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 영상, 도로 점유 센서, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 위치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 대피소 정보, 병원 가용 자원을 한 문맥으로 엮어 소방 출동 경로 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 우선, 시민 대피 알림, 인근 도로 우회, 공조 설비 제어까지 연쇄적으로 실행할 수 있어야 한다.

이때 중요한 것은 "많이 연결했다"가 아니라 "어떤 이벤트를 어떤 책임 체계로 묶었는가"다. 도시 운영은 민감한 공공 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)이므로, 기술적으로 가능하다고 해서 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 무조건 통합하면 안 된다. 위치 정보와 영상은 비식별화, [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/), [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 로그가 선행되어야 하며, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별로 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 허용치와 실패 시 수동 절차도 정의해야 한다.

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 위치·시간·시설물 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)를 부처 공통 기준으로 정했는가?
2. 영상·센서·행정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 같은 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 모델로 연결할 수 있는가?
3. 엣지와 중앙 중 어디서 분석·익명화·제어를 수행할지 역할을 나누었는가?
4. [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)와 공공 책임성을 고려한 권한·[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 체계가 있는가?
5. 개방 API를 제공하더라도 제어 명령과 조회 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 분리해 관리하는가?

### 채택 / 회피 판단

- **채택**: 교통·안전·환경처럼 여러 부서가 같은 위치 사건을 함께 다뤄야 하는 도시 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)
- **단계적 접근**: 단일 부서 내부 자동화부터 시작해 공통 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)을 확장하는 경우
- **회피 또는 재설계**: 센서 도입만 우선하고 운영 프로세스, 법적 근거, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준이 없는 사업

### 자주 나오는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 센서 설치 수를 성과로 삼고 공통 [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/)은 뒤로 미루는 경우
- 모든 원본 영상을 중앙으로 보내 비용과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 폭증시키는 경우
- 부처별로 다른 좌표·시간 기준을 유지해 연계가 안 되는 경우
- 개방 API는 선언했지만 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 품질과 책임 주체가 없어 실제 활용이 안 되는 경우
- [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)를 나중 문제로 미뤄 사업 저항을 키우는 경우

좋은 스마트 시티 플랫폼은 거대한 단일 시스템이 아니라, <strong>공통 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 언어와 운영 규칙 위에 여러 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>를 올릴 수 있게 만드는 도시용 공공 플랫폼</strong>이다. 처음부터 모든 도시 업무를 한 번에 통합하려 하기보다, 응급 대응·교통 최적화·에너지 효율처럼 가치가 분명한 시나리오부터 닫힌 루프를 만들어 가는 편이 현실적이다.

- **📢 섹션 요약 비유**: 운동장을 한 번에 완벽한 도시로 만들 수 없듯, 스마트 시티도 먼저 길과 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 규칙을 만들고 그 위에 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), 가게, 집을 차근차근 올려야 제대로 굴러간다.

---

## Ⅴ. 기대효과 및 결론

스마트 시티 플랫폼을 제대로 구축하면 도시 운영은 사후 대응 중심에서 상황 예측과 선제 제어 중심으로 이동한다. [사고 대응](/studynote/09_security/01_intro_principles/009_incident_response/) 시간 단축, 교통 혼잡 완화, 에너지 절감, 유지보수 효율 향상, 민간 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 생태계 활성화가 모두 같은 기반에서 나올 수 있다.

하지만 이 플랫폼은 기술만으로 완성되지 않는다. 표준화되지 않은 레거시 시스템, 부서 간 권한 충돌, 장비 [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/), [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 규제, 유지운영 비용은 장기 과제로 남는다. 따라서 플랫폼은 "스마트 장비 묶음"이 아니라 <strong>도시 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 거버넌스와 운영 아키텍처의 재설계</strong>로 기억해야 한다.

결론적으로 스마트 시티 플랫폼의 핵심은 센서 수집이 아니라 <strong>공통 문맥, 이벤트 연계, 제어 피드백</strong>이다. 이 세 가지가 연결될 때 비로소 교통·안전·환경·복지가 같은 도시 운영 체계 안에서 움직인다.

- **📢 섹션 요약 비유**: 좋은 스마트 시티 플랫폼은 도시 곳곳의 이야기를 한데 모아 듣고, 필요한 곳에 바로 지시를 내리는 믿을 수 있는 지휘자와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [사물인터넷](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) ([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), Internet of Things) | 현장 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 도시 상태의 1차 입력원 |
| 도시 [데이터 허브](/studynote/16_bigdata/09_platform/180_data_hub/) | 시간·위치·자산 기준으로 이기종 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통합 |
| [디지털 트윈](/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) | 도시 상황을 공간 모델 위에서 시뮬레이션 |
| 협력 지능형 교통체계 ([C-ITS](/studynote/06_ict_convergence/02_iot_mobility/173_c_its_cooperative_intelligent_transport_systems/), Cooperative-Intelligent Transport Systems) | 교통 제어와 차량 연동의 실시간 실행 계층 |
| 모빌리티 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형 (MaaS, Mobility [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | 시민 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 민간 생태계 확장 포인트 |
| 프라이버시 바이 디자인 | 영상·위치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용의 필수 거버넌스 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
Urban sensors and legacy systems
    |
    v
Shared context model + event integration
    |
    +- traffic
    +- safety
    +- environment
    +- energy
    +- citizen services / open APIs
    |
    v
Digital twin, AI analytics, closed-loop city operations
```

이 흐름은 개별 도시 시스템이 공통 문맥과 이벤트 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)를 통해 통합 운영 플랫폼으로 발전하는 방향을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스마트 시티 플랫폼은 동네의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등, 가로등, 카메라가 모두 같은 반 친구처럼 서로 소식을 나누는 거예요.
2. 그래서 한곳에서 문제가 생기면 다른 친구들도 바로 알고 같이 도와줄 수 있어요.
3. 선생님이 한 장의 큰 지도 위에서 모두를 움직이게 하는 것처럼 도시도 더 똑똑하게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 171 / 552

<- **이전**: [170. 프라이빗 5G (Private 5G, 특화망 / 이음5G)](/studynote/06_ict_convergence/02_iot_mobility/170_private_5g_network/)
**다음**: [172. 마스 (MaaS, Mobility as a Service)](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/) ->

---
