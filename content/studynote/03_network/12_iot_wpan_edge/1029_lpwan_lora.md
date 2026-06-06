---
title: "LoRa"
date: "2026-05-08"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [LPWAN](/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) [로라](/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)는 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), [WPAN](/studynote/03_network/12_iot_wpan_edge/604_wpan_wireless_personal_area_network/), 엣지에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [LPWAN](/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) [로라](/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)를 이해하면 전력 효율과 현장 반응성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[사물인터넷](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 시대가 도래하면서 산속의 산불 감지기, 땅속의 수도 계량기, 바다의 양식장 온도계 등 수백만 개의 센서를 인터넷에 연결해야 했다. 스마트폰에 쓰는 [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 모뎀을 달면 한 달 만에 배터리가 방전되고 매달 통신비를 내야 했다. 반대로 Wi-Fi나 블루투스를 쓰면 거리가 100m도 안 되어 산속까지 망을 깔 수가 없었다.

"속도는 아주 느려도 좋으니, 동전 배터리 하나로 10년을 버티면서 10km 밖까지 문자를 보낼 수 없을까?" 이 모순적인 요구사항을 완벽하게 해결한 기술이 바로 <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/">LPWAN</a>(Low <a href="/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/">Power</a> Wide Area Network)</strong>이며, 그중에서도 누구나 기지국을 세워 쓸 수 있는(비면허 대역) 개방형 생태계의 절대 강자가 바로 <strong><a href="/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRa</a>(<a href="/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/">로라</a>)</strong>다.

```text
[체내 통신]
    |
    v
[LPWAN 로라]
    |
    +---> [시그폭스 협대역 통신]
```

- **📢 섹션 요약 비유**: 택배([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 보낼 때 엄청 비싸고 빠른 비행기([LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/))나 동네만 가는 오토바이(Wi-Fi) 대신, 한 달에 한 번 편지 한 장만 싣고 전국을 걸어가는 마라토너([LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))를 고용한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 생태계는 하위 물리 계층인 '[LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)'와 상위 네트워크 프로토콜인 'LoRaWAN'으로 구분된다. 아키텍처는 전력을 아끼기 위해 극도로 단순한 Star-of-Stars(별) 모양을 취한다.

```text
+--------------------------------------------------------------+
|                    [ 애플리케이션 서버 ]                     |
|               (수도 검침, 산불 감시 대시보드)                |
+--------------^-----------------------------------------------+
               | (인터넷 / TCP/IP)
+--------------v-----------------------------------------------+
|                   [ LoRaWAN Network Server ]                 |
|               (중복 패킷 제거, 보안 검사, 라우팅)            |
+--------------^-----------------------------------------------+
               | (인터넷 / 3G, 4G 백홀)
+--------------v----------+        +------------v------------+
|      [ LoRa Gateway 1 ]     |        |     [ LoRa Gateway 2 ]    |
|    (산꼭대기 / 고층 빌딩)   |        |     (다른 동네 건물)      |
+--------------^----------+        +------------^------------+
               | (LoRa 전파: CSS 변조, 비면허 대역 900MHz)
         +-----+--------+-------------------+
+--------v---+   +------v-----+   +--------v---+
|  수도 계량기 |   | 산불 감지기 |   | 애완견 목걸이| <- End Nodes
+------------+   +-------------+   +------------+
```

1. <strong><a href="/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/">CSS</a> (Chirp <a href="/studynote/03_network/01_data_communication/068_스펙트럼_확산_Spread_Spectrum/">Spread Spectrum</a>)</strong>: LoRa의 핵심 변조 기술이다. 박쥐가 소리를 낼 때 주파수가 주욱 올라가거나 내려가는 '처프(Chirp)' [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 이용한다. [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 넓은 주파수 대역으로 쭉 늘여서(확산) 보내기 때문에, 중간에 엄청난 노이즈가 섞이거나 벽에 부딪혀도 수신기가 원래 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 기가 막히게 복원해 낸다(수신 감도가 -148dBm에 달함).
2. **단순한 통신 (Star Topology)**: 단말기들은 센서 값을 게이트웨이로 툭 던지고 곧바로 깊은 수면(Deep Sleep)에 빠져버린다. 배터리를 아끼기 위해 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)([Mesh](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)) 네트워크처럼 남의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 릴레이로 전송해주지 않는다.

- **📢 섹션 요약 비유**: 박쥐([LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))가 동굴 속에서 초음파(Chirp [신호](/studynote/02_operating_system/02_process_thread/130_signal/))를 쏘면, 주변이 아무리 시끄럽고 벽이 많아도 그 메아리를 정확히 알아듣고 먹이의 위치를 찾아내는 완벽한 생존 기술이다.

---

## Ⅲ. 비교 및 연결

[LPWAN](/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) 시장을 삼분하는 대표적인 경쟁 기술들과 비교해 보면 LoRa의 포지셔닝을 알 수 있다.

| 비교 항목 | [LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) (LoRaWAN) | [SigFox](/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) | [NB-IoT](/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) ([NarrowBand IoT](/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/)) |
|:---:|:---|:---|:---|
| **주파수 대역** | 비면허 대역 (무료, 한국 900MHz) | 비면허 대역 (무료) | <strong>면허 대역 (<a href="/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/">LTE</a>/<a href="/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a>, 통신비 발생)</strong> |
| **망 구축 방식** | **자가망 구축 가능 (사설망)** | [SigFox](/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) 사업자 전용망 | 이통사 기지국망 종속 |
| **전송 속도** | 최대 ~50 kbps | 100 bps (매우 느림) | ~250 kbps (비교적 빠름) |
| **양방향 통신** | 지원 (클래스 A, B, C) | 제한적 (거의 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)) | 완벽 지원 |
| **주요 적용처** | 스마트 팜, 사설 공장, 지자체망 | 단순 위치 추적, 수도 검침 | [스마트 시티](/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/), 대규모 국가 인프라 |

LoRa는 기업이나 지자체가 통신사에 돈을 내지 않고 자기들만의 독립적인 무선망(사설 LoRa망)을 쉽게 구축할 수 있다는 개방성 덕분에 NB-IoT의 거센 추격에도 살아남아 글로벌 생태계를 장악했다.

- **📢 섹션 요약 비유**: NB-IoT가 돈을 내고 타는 빠르고 안전한 '고속버스'라면, SigFox는 정해진 길로만 가는 느린 '우편 배달부'고, LoRa는 내가 직접 길을 개척해서 타고 다닐 수 있는 튼튼한 '오프로드 자전거'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
산악 지형이 많은 한국의 '스마트 트레킹'이나 '치매 노인 배회 감지' 시스템에 널리 쓰인다. 도심의 높은 건물 옥상에 [LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) 게이트웨이 몇 대만 설치하면 반경 10km의 모든 센서를 커버할 수 있어, [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 인프라 구축 비용이 거의 들지 않는다.

**기술사 판단 포인트 (Trade-off):**
LoRa망을 설계할 때는 <strong>'Duty Cycle(통신 시간 제한)'과 '<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 페이로드 한계'</strong>를 반드시 아키텍처에 반영해야 한다.
1. 무료 주파수를 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문에 한 단말기가 주파수를 독점하지 못하도록 법적으로 통신 시간(예: 1% Duty Cycle)이 제한된다. 즉, 하루 종일 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 계속 보낼 수 없으며, 한 번 보낸 후에는 일정 시간 쉬어야 한다.
2. 한 번에 보낼 수 있는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 수십 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)([Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/))에 불과하므로, [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) 사진 전송 등은 원천적으로 불가능하다. 센서에서 자체적으로 의미 있는 수치(온도 25도)만 뽑아내어 보내는 엣지 프로세싱 설계가 병행되어야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 공중전화(비면허 대역)는 누구나 무료로 쓸 수 있지만 뒷사람을 위해 1분(Duty Cycle) 이상 통화할 수 없다. 따라서 장황하게 수다를 떨면 안 되고 "나 지금 부산이야"라는 핵심 단어만 짧게 말하고 끊어야 한다.

---

## Ⅴ. 기대효과 및 결론

LoRa는 수백억 개의 사물들이 인터넷에 연결되는 진정한 'Massive [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)(대규모 [사물인터넷](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))' 시대를 열어젖힌 일등 공신이다. 배터리 교체의 저주에서 인류를 해방시켰으며, 스마트 팜, [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/), 해상 물류 추적 등 산업 전반에 보이지 않는 신경망을 깔았다.

결론적으로 LoRa는 속도경쟁([5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)/[6G](/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/))으로만 치닫던 통신 업계에 '느림과 저전력의 미학'이라는 새로운 패러다임을 증명한 기술이다. 향후 [저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 통신([LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/))과 결합한 '위성 [LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)(Satellite [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))'가 상용화되면, 태평양 한가운데 떠 있는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 박스의 위치까지 배터리 없이 10년간 실시간으로 추적하는 궁극의 글로벌 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 망이 완성될 것이다.

- **📢 섹션 요약 비유**: [로라](/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)는 화려한 스포트라이트를 받는 스포츠카([5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/))는 아니지만, 아무도 없는 깊은 산속과 땅속에서 10년 동안 묵묵히 살아남아 우리에게 생존 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보내주는 가장 끈질긴 생명체다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [체내 통신](/studynote/03_network/12_iot_wpan_edge/1028_wban_wireless_body_area_network/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 저전력 통신 (Low [Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Communication) | 배터리 수명과 직접 연결된다. |
| [센서 네트워크](/studynote/06_ict_convergence/02_iot_mobility/103_wsn_sensor_network/) (Sensor Network) | 수많은 단말의 연결 구조를 결정한다. |
| [시그폭스](/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) 협대역 통신 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 체내 통신]
    |
    v
[현재 개념: LPWAN 로라]
    |
    +---> [확장 A: 시그폭스 협대역 통신]
    +---> [확장 B: 자율형 엣지 협업]
```

[LPWAN](/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) [로라](/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)는 [체내 통신](/studynote/03_network/12_iot_wpan_edge/1028_wban_wireless_body_area_network/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [시그폭스](/studynote/03_network/12_iot_wpan_edge/1030_lpwan_sigfox/) 협대역 통신와 자율형 엣지 협업 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스마트폰으로 산속에서 와이파이를 잡으려 하면 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 금방 끊어지고 배터리도 훅훅 닳아요.
2. [로라](/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)([LoRa](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))는 아주 작은 동전 건전지 하나만으로 산 너머 10km까지 카톡을 보낼 수 있는 마법의 무전기예요.
3. 대신 사진이나 동영상은 못 보내고 "온도 25도", "나 여기 있어" 같은 아주 짧은 글씨만 보낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 1120

<- **이전**: [1028. 체내 통신 (WBAN: Wireless Body Area Network)](/studynote/03_network/12_iot_wpan_edge/1028_wban_wireless_body_area_network/)
**다음**: [102. TDD (Time Division Duplexing) - 시분할 이중화 (업/다운링크 분리)](/studynote/03_network/02_multiplexing_multiple_access/102_tdd/) ->

---
