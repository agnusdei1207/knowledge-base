+++
title = "1108. OT 망 (운영 기술 망) 분리 원단 통제"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제를 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

보안의 절대 우선순위([CIA Triad](/knowledge-base/studynote/09_security/01_intro_principles/001_cia_triad/))가 180도 완전히 뒤집힙니다.
- **IT 망 (사무실, 인터넷)**:
  - <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a> (<a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">Confidentiality</a>)이 1순위</strong>입니다. 고객 개인정보가 털리는 게 최악입니다. 백신 돌리느라 서버가 1초 멈추거나 재부팅 해도 아무도 안 죽습니다.
- <strong><a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/">OT</a> 망 (공장, 발전소, 철도, <a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/">SCADA</a>/<a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/">ICS</a>) 🌟</strong>:
  - <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)이 무조건 0순위</strong>입니다. 기밀이 털리든 말든, 돌아가는 용광로 밸브 시스템이 백신 업데이트하느라 '1초 정지(재부팅)'되는 순간 폭발 사고로 전 직원이 몰살당합니다.
  - **딜레마**: 공장 기계는 윈도우 95, [XP](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/073_xp_extreme_programming/) 같은 구석기 OS를 20년째 안 끄고 그냥 돌립니다(패치/백신 설치 불가). 해커가 들어오면 100% 감염되는 걸 알면서도 끌 수가 없는 최악의 무방비 시한폭탄입니다.

```text
[산업용 이더넷 PROFINET 망]
    |
    v
[OT 망 분리 원단 통제]
    |
    +---> [OPC UA 자동화 프레임 표준 통신]
```

- **📢 섹션 요약 비유**: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- 옛날엔 공장(OT망)과 사무실(IT망) 랜선을 아예 끊어버렸습니다(Air-Gap 물리적 [망분리](/knowledge-base/studynote/12_it_management/05_security_compliance/182_network_separation_model/)).
- **저주**: 4차 산업혁명([스마트 팩토리](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/))이 시작되면서, 서울 본사 사장님이 스마트폰 앱으로 부산 공장 용광로 온도를 실시간으로 보고 싶어 합니다.
- 결국 끊어놨던 IT망과 OT망 사이에 몰래 랜선을 이어버렸고(IT-[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) Convergence), 해커가 사장님의 이메일을 털어서 IT망으로 들어온 뒤, 연결된 다리를 타고 내려와 공장(OT망)의 로봇 팔을 마비시켜 버리는 [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 지옥이 열렸습니다. (TSMC, 대만 주유소 해킹 등)

구석기 윈도우 95 기계들을 살리기 위해 네트워크 길목을 극단적으로 틀어막습니다.

### 1. 퍼듀 모델 ([Purdue Model](/knowledge-base/studynote/09_security/18_iot_ot_physical/902_purdue_model/)) 기반 [마이크로 세그멘테이션](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)
- 전체 회사를 레벨 0부터 5까지 철저한 계급제([DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/)) 층으로 나눕니다.
  - 레벨 4/5: 본사 이메일, 웹서핑 (가장 더러움)
  - 레벨 3/3.5 ([DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/)): IT와 OT가 만나는 유일한 완충지대
  - 레벨 0/1/2: 공장 로봇 제어(OT망, 가장 깨끗함)
- 1044번에서 배운 [마이크로 세그멘테이션](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)으로 **레벨 4의 패킷이 레벨 1로 한 방에 다이렉트로 내려찍는(점프) 행위를 방화벽으로 모조리 다 찢어버립니다.**

### 2. 물리적 일방향 전송 (Unidirectional [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Diode](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/)) 🌟 최고 무기 🌟
방화벽은 소프트웨어라 해커가 뚫을 수 있습니다. 물리학으로 방어합니다.
- 공장의 온도를 사장님에게 보내줘야 하니 선은 연결해야 합니다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/">다이오드</a> 마법</strong>: 공장([OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) ➜ 사장님(IT) 방향으로만 레이저 빛을 쏠 수 있고, <strong>사장님(IT) 쪽에서 공장(<a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/">OT</a>)으로는 수신 센서(광 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/">다이오드</a>) 자체를 아예 하드웨어적으로 도려내어 부숴버린 1,000만 원짜리 전용 장비</strong>를 길목에 박아버립니다.
- 해커가 사장님 망을 다 뚫고 공장으로 악성 코드를 날려도, 반대편에서 빛을 받아주는 렌즈 칩 자체가 물리학적으로 존재하지 않기 때문에 패킷이 허공에 툭 떨어져 증발해 버리는(역류 100% 불가) 절대 에어갭 융합 장비입니다.

### 3. [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 화이트리스팅 및 키오스크 소독
- 인터넷을 다 끊어놔도, 협력 업체 직원이 들고 온 오염된 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 1개가 스턱스넷처럼 공장 기계를 박살 냅니다.
- **소독 키오스크**: 공장에 들어가려면 현관문에 있는 검역 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)(키오스크)에 USB를 꽂고 30개의 백신 엔진으로 영혼까지 털어 소독(포맷급)해야만 사내망에 꽂을 권한을 줍니다. 또한 기계의 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 포트는 글루건(실리콘)으로 쏴서 아예 못 꽂게 막거나(물리적 통제), '인가된 1개의 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)'만 인식하는 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 제어([DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/)) 솔루션을 떡칠합니다.

```text
[산업용 이더넷 PROFINET 망]
    |
    v
[OT 망 분리 원단 통제]
    |
    +---> [OPC UA 자동화 프레임 표준 통신]
```

- **📢 섹션 요약 비유**: 사무실 인터넷(IT망)이 정보 유출을 막는 <strong>'철저한 신분증 검사(<a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>)'</strong>라면, 공장의 기계망(OT망)은 심장 수술실의 기계가 절대 1초도 멈추면 안 되는 <strong>'무정전 생명 유지 장치(<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>)'</strong>입니다. 수술실 컴퓨터는 20년 된 구형이라 감기([바이러스](/knowledge-base/studynote/02_operating_system/10_security/589_virus/))에 걸리면 즉사합니다. 그래서 병원은 수술실과 바깥 로비를 두꺼운 철문([망분리](/knowledge-base/studynote/12_it_management/05_security_compliance/182_network_separation_model/))으로 막았습니다(에어갭). 하지만 원장님이 로비에서 수술 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)를 보겠다며 철문에 구멍을 뚫었습니다. 해커가 로비로 들어와 이 구멍으로 독가스([랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/))를 뿌려 수술실을 다 죽입니다. 이 참사를 막기 위한 <strong>일방향 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/">다이오드</a> 장비</strong>는 수술실 벽 구멍에 <strong>'안에서 밖만 내다볼 수 있는 두꺼운 <a href="/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a> 투명 거울'</strong>을 설치한 것입니다. 원장님은 밖에서 수술 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/) 빛([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 일방향으로 전달받아 볼 수 있지만, 밖에서 안으로 독가스를 뿌리거나 말을 걸어도 벽에 튕겨 나와 1%도 수술실 안으로 역류하지 못하는 궁극의 물리학적 방수 격벽 시스템입니다.

---

## Ⅲ. 비교 및 연결

[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. 산업용 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) 망이 기반 조건을 만든다면, [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 그 위에서 핵심 메커니즘을 구현하고, [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | 산업용 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) 망의 기반 정리 | [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제의 핵심 동작 | [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 산업용 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) 망 수준의 기본 대책으로 충분한지, 아니면 [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 측정 정확도 부족인지, 모델 적합성 악화인지 먼저 분리한다.
2. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- 산업용 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) 망와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 산업용 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) 망 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 실제 전달 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 나타내는 대표 지표다. |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 사용자 체감 품질을 좌우한다. |
| [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 산업용 이더넷 PROFINET 망]
    |
    v
[현재 개념: OT 망 분리 원단 통제]
    |
    +---> [확장 A: OPC UA 자동화 프레임 표준 통신]
    +---> [확장 B: AI 기반 성능 예측]
```

[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) 망 분리 원단 통제는 산업용 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) 망에서 출발해 현재 메커니즘을 정교화하고, 이후 [OPC UA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/631_opc_ua_smart_factory_protocol/) 자동화 프레임 표준 통신와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 218 / 1120

<- **이전**: [1107. 산업용 이더넷 PROFINET 망](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1107_industrial_ethernet_profinet_ot_network/)
**다음**: [1109. OPC UA 자동화 프레임 표준 통신](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1109_opc_ua_industrial_automation_protocol/) ->

---
