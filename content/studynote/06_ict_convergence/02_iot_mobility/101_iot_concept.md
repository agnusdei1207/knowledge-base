---
title: 사물인터넷 (IoT) 개념
date: '2024-03-21'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)
1. **본질**: 사물인터넷 (IoT, Internet of Things)은 주변의 모든 사물에 센서와 통신 모듈을 내장하여, 물리적 세계의 정보를 디지털화하고 인터넷에 연결하는 초연결 네트워크 기술이다.
2. **가치**: 인간의 명시적 개입 없이 사물들끼리 스스로 [[001_dikw_pyramid|데이터]]를 수집, 분석, 통신하여 최적의 물리적 동작을 수행하는 'Sense-Think-Act' 자동화 루프를 완성한다.
3. **판단 포인트**: IoT 도입의 핵심은 단순히 기기를 연결하는 것이 아니라, 연결을 통해 쏟아지는 방대한 [[001_dikw_pyramid|데이터]]에서 어떤 '비즈니스 가치(Insight)'를 추출하고 통제할 수 있는가를 설계하는 데 있다.

---

## Ⅰ. 개요 및 필요성

사물인터넷 (IoT)은 PC와 스마트폰이라는 한정된 기기를 넘어, 가전제품, 자동차, 공장 설비 등 모든 사물이 인터넷 주소(IP)를 갖고 네트워크에 참여하는 패러다임이다. 과거에는 [[001_dikw_pyramid|데이터]]의 생성이 인간의 키보드 입력이나 터치에 의존했다면, IoT 환경에서는 사물이 스스로 상태를 감지하고 [[001_dikw_pyramid|데이터]]를 생산한다.

이러한 기술이 확산된 배경에는 하드웨어의 미세화로 인한 센서의 저가격화, 배터리 소모를 극적으로 줄인 저전력 무선 통신 기술([[109_lpwan_low_power_wide_area_network|LPWAN]], [[607_ble_bluetooth_low_energy_iot|BLE]]), 그리고 생성된 대규모 [[001_dikw_pyramid|데이터]]를 처리할 [[052_cloud_computing_os|클라우드 컴퓨팅]] 인프라의 완성이 있다. IoT가 없으면 우리는 현실 세계의 비효율(전력 낭비, 기계 고장, 교통 체증)을 사후에 사람이 직접 점검하고 대처해야만 한다.

- **📢 섹션 요약 비유**: IoT는 세상의 모든 물건에 '눈과 귀(센서)'와 '입(통신)'을 달아주는 것이다. 예전에는 사람이 일일이 화분에 물이 부족한지 만져봐야 했지만, 이제는 화분이 스스로 목이 마르다고 수도꼭지에게 말을 거는 시대가 된 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IoT 시스템은 크게 3개의 계층으로 구성된다. [[001_dikw_pyramid|데이터]]를 빨아들이는 감지(Sensing), 이를 전달하는 네트워크(Connectivity), 그리고 모인 [[001_dikw_pyramid|데이터]]를 해석하고 명령을 내리는 [[090_service_kubernetes_network_load_balancing|서비스]]([[090_service_kubernetes_network_load_balancing|Service]]/Application) 계층이다.

| 계층 | 역할 | 주요 기술 및 구성 요소 |
| :--- | :--- | :--- |
| **[[090_service_kubernetes_network_load_balancing|서비스]] 계층 ([[090_service_kubernetes_network_load_balancing|Service]]/App)** | [[001_dikw_pyramid|데이터]] 분석 및 가시화, [[090_service_kubernetes_network_load_balancing|서비스]] 제공 | 클라우드 플랫폼, BigData 처리, UI/UX, 대시보드 |
| **네트워크 계층 (Connectivity)** | 센서 [[001_dikw_pyramid|데이터]]를 플랫폼으로 안전하게 전송 | [[418_5g_embb_urllc_mmtc_slicing|5G]], Wi-Fi, [[109_lpwan_low_power_wide_area_network|LPWAN]] ([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]], [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]]), [[622_mqtt_publish_subscribe_qos|MQTT]] |
| **디바이스 계층 (Sensing)** | 아날로그 물리량 측정 및 제어(Actuation) | 센서(온도, 조도, 위치 등), 액추에이터(모터, [[238_switch_operation_principles|스위치]]), RFID |

```text
┌──────────────────────────────────────────────────────────────┐
│                  IoT의 Sense - Think - Act 루프              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ [ 3. Actuation ]                       [ 2. Processing ]     │
│  행동 실행 / 제어 ◀───── 명령 ────── 클라우드 / 엣지 서버    │
│       │                                      ▲               │
│       │ 물리적 변화 발생                     │ 데이터 분석   │
│       ▼                                      │               │
│ [ 현실 세계 (Physical World) ]               │               │
│       │                                      │               │
│       │ 물리량 감지                          │ 원격 전송     │
│       ▼                                      │               │
│ [ 1. Sensing ]  ──────── 데이터 ──────▶ [ Network (LPWAN) ]  │
│  센서 단말기                                                 │
└──────────────────────────────────────────────────────────────┘
```

이 다이어그램은 현실의 변화를 감지해 디지털로 보내고, 분석된 결과가 다시 현실의 물리적 동작(모터 제어, 온도 조절 등)으로 환원되는 IoT의 본질적 순환 고리를 보여준다.

- **📢 섹션 요약 비유**: IoT의 원리는 사람의 몸과 같다. 손끝의 감각 신경(센서)이 뜨거움을 느끼면, 신경망(네트워크)을 타고 뇌(클라우드)로 전달되고, 뇌는 즉각 근육(액추에이터)에 손을 떼라는 명령을 내리는 완벽한 반사 신경 시스템이다.

---

## Ⅲ. 비교 및 연결

IoT는 과거의 기기 간 통신인 M2M을 포괄하고, 나아가 사람과 프로세스까지 아우르는 IoE로 진화하는 징검다리 역할을 한다.

| 비교 항목 | [[602_m2m_machine_to_machine_telemetry|M2M]] (Machine to Machine) | IoT (Internet of Things) | IoE (Internet of Everything) |
| :--- | :--- | :--- | :--- |
| **연결 대상** | 특정 기기 간 1:1, 1:N 연결 | 만물과 인터넷의 개방형 연결 | 사물 + 사람 + [[001_dikw_pyramid|데이터]] + 프로세스 |
| **통신 인프라** | 폐쇄망 (Cellular, 전용망 등) | 표준 IP 기반 개방형 네트워크 | 상황 인지형 지능형 네트워크 |
| **[[001_dikw_pyramid|데이터]] 활용** | 단순 기기 모니터링 및 제어 | 빅데이터 분석을 통한 가치 창출 | 지능형 판단 및 생태계 융합 ([[033_context|Context]]) |

최근에는 클라우드의 [[141_latency|지연 시간]]([[141_latency|Latency]]) 문제를 해결하기 위해, [[001_dikw_pyramid|데이터]]가 발생하는 말단 기기 주변에서 1차적인 연산과 [[190_ai_llm_requirements_specification|AI]] 추론을 수행하는 **[[235_edge_computing_smart_factory|엣지 컴퓨팅]]([[235_edge_computing_smart_factory|Edge Computing]])** 및 **[[640_aiot_ai_and_iot_edge_cloud_latency|AIoT]]([[190_ai_llm_requirements_specification|AI]] + IoT)** 기술과 결합하여 한계를 돌파하고 있다.

- **📢 섹션 요약 비유**: M2M이 두 사람이 종이컵 전화기로 비밀 얘기를 나누는 닫힌 통신이라면, IoT는 모두가 스마트폰을 들고 광장(인터넷)에 모여 수만 명과 동시에 정보를 교환하는 열린 생태계다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 IoT 프로젝트를 설계할 때 가장 경계해야 할 것은 '무목적적인 센서 달기'다. [[001_dikw_pyramid|데이터]]를 모으는 것 자체가 목적이 되어서는 안 되며, 수집 비용 대비 비즈니스적 가치를 철저히 계산해야 한다.

- **통신망 선택 판단**: 초당 수백 메가바이트를 쏟아내는 자율주행차(고대역폭)에는 5G가 필요하지만, 하루에 한 번 수도 사용량만 보내면 되는 스마트 미터기에는 배터리가 10년 가는 저전력 장거리 통신망인 [[109_lpwan_low_power_wide_area_network|LPWAN]]([[617_lora_lorawan_css_chirp_spread_spectrum|LoRa]], [[620_nbiot_narrowband_iot_lte_guardband|NB-IoT]])을 채택해야 ROI가 맞는다.
- **보안 설계 ([[058_security_by_design|Security by Design]])**: IoT 기기는 CPU와 메모리가 빈약하여 기존의 무거운 암호화 모듈을 얹기 어렵다. [[459_quic_fec_forward_error_correction|초기]] 설계부터 경량 암호 알고리즘을 적용하고, [[032_firmware|펌웨어]] 무선 업데이트(OTA) 기능을 반드시 구현하여 해커의 [[990_botnet_cnc|봇넷]](Mirai [[990_botnet_cnc|Botnet]] 등) 공격 기지로 전락하는 것을 막아야 한다.

- **📢 섹션 요약 비유**: 고속도로를 설계할 때 자전거(저전력 센서)와 대형 트럭(영상 [[001_dikw_pyramid|데이터]])이 같은 차선에서 달리게 하면 사고가 난다. [[001_dikw_pyramid|데이터]]의 특성과 크기에 맞춰 좁은 골목길([[109_lpwan_low_power_wide_area_network|LPWAN]])과 고속도로([[418_5g_embb_urllc_mmtc_slicing|5G]])를 알맞게 깔아주는 것이 설계자의 몫이다.

---

## Ⅴ. 기대효과 및 결론

IoT 인프라가 제대로 구축되면 기업은 '예측 유지보수(Predictive Maintenance)'를 통해 기계가 고장 나기 전에 미리 부품을 교체하여 공장 가동 중단을 막을 수 있다. 또한, 단순히 제품을 파는 것을 넘어 고객이 제품을 어떻게 사용하는지 [[001_dikw_pyramid|데이터]]를 얻어 '구독형 [[090_service_kubernetes_network_load_balancing|서비스]]([[309_saas|SaaS]])'로 비즈니스 모델을 전환할 수 있다.

결론적으로 IoT는 4차 산업혁명의 눈과 귀 역할을 하는 가장 기초적인 감각 기관이다. 향후 이기종 기기 간의 통신 표준([[612_matter_csa_smart_home_standard|Matter]] 등)이 통일되고, 생성형 AI가 디바이스 단에 탑재되면, 기기가 스스로 상황을 인지하고 판단하는 진정한 의미의 자율 지능 사회로 도약할 것이다.

- **📢 섹션 요약 비유**: IoT는 건물 곳곳에 신경망을 심는 공사다. 처음에는 선을 까는 게 귀찮고 돈이 들지만, 완성되고 나면 건물이 스스로 온도를 조절하고 도둑을 잡아내는 똑똑한 로봇으로 다시 태어난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[109_lpwan_low_power_wide_area_network|LPWAN]] (Low [[069_type_1_2_error_statistical_power|Power]] Wide Area Network)** | IoT 센서의 배터리 수명을 획기적으로 늘려주는 저전력 통신망 |
| **[[235_edge_computing_smart_factory|Edge Computing]] ([[235_edge_computing_smart_factory|엣지 컴퓨팅]])** | 클라우드로 [[001_dikw_pyramid|데이터]]를 다 보내지 않고 센서 가까이서 즉시 처리해 [[015_지연_데이터_관점|지연]]을 줄이는 구조 |
| **[[126_digital_twin_concept|Digital Twin]] ([[126_digital_twin_concept|디지털 트윈]])** | IoT가 수집한 현실 [[001_dikw_pyramid|데이터]]를 가상 공간에 똑같이 복제해 시뮬레이션하는 기술 |
| **[[612_matter_csa_smart_home_standard|Matter]] ([[612_matter_csa_smart_home_standard|매터]])** | 삼성, 애플 등 제조사가 달라도 IoT 기기들이 서로 통신할 수 있게 해주는 국제 연동 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
M2M (Machine to Machine) - 폐쇄망 단방향 제어
    │
    ▼
IoT (Internet of Things) - IP 기반 개방형 초연결 네트워크 구축
    │
    ▼
Edge Computing + IoT - 클라우드 부하 분산 및 실시간 처리 확보
    │
    ▼
AIoT (AI + IoT) - 단말기 스스로 추론 및 의사결정 수행
    │
    ▼
IoE (Internet of Everything) - 만물과 프로세스의 지능적 융합 및 최적화
```
이 흐름도는 단순한 '연결'에서 출발해 연산 [[015_지연_데이터_관점|지연]]을 줄이고, 궁극적으로 사물 자체가 지능을 가지는 방향으로 진화하는 IoT의 궤적을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 사물인터넷은 우리 집 장난감과 가구들이 '말을 배우는 것'과 같아요.
2. 곰 인형이 내가 집에 온 걸 알아채고 거실 전등에게 "빨리 불 켜줘!"라고 카톡을 보내는 거예요.
3. 물건들이 서로 수다를 떨면서 우리가 시키기 전에 미리 알아서 도와주니까, 집 전체가 마법의 성처럼 편리해진답니다!
