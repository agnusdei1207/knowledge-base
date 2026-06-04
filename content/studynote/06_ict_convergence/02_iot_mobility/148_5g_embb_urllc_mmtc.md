+++
title = "148. 5G 통신망의 3대 초격차 특성 - eMBB (초고속), uRLLC (초저지연/고신뢰 1ms), mMTC (초연결 IoT)"
date = 2026-05-03

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 통신망은 단순히 다운로드 속도만 높인 4G의 연장선이 아니라, 전혀 다른 성격의 3대 핵심 특성인 <strong>초고속/대용량(<a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/">eMBB</a>), 초저지연/고신뢰(<a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/">uRLLC</a>), 대규모 사물 초연결(<a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/">mMTC</a>)</strong>을 단일 물리망에서 동시에 충족시키는 융합 인프라다.
> 2. **가치**: 이 3가지 특성 덕분에 과거에는 불가능했던 자율주행 자동차(0.1초 랙이 치명적인 분야), 4K VR/AR 실시간 스트리밍, 수백만 개의 도심 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 통제 등 B2B 및 B2G [스마트 시티](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/) 서비스가 현실화되었다.
> 3. **판단 포인트**: 서로 상충하는 이 극단적인 요구조건들을 물리적 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 1대에서 간섭 없이 제공하기 위해, 클라우드 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 기술로 네트워크 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)를 독립적으로 쪼개는 <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">네트워크 슬라이싱</a>(<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">Network Slicing</a>)</strong>과 연산 뇌를 전봇대 끝단으로 전진 배치하는 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/">엣지 컴퓨팅</a>(<a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/">MEC</a>)</strong>이 5G의 진정한 코어 아키텍처다.

---

## Ⅰ. 개요 및 필요성

[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)(IMT-2020)는 국제전기통신연합(ITU)이 정의한 5세대 이동통신 기술이다. 4G([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/))가 사람 중심의 스마트폰 통신(B2C)에 머물렀다면, 5G는 하늘의 [UAM](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/)(에어택시), 무인 공장 로봇, 수백만 개의 깡통 센서 등 사물과 산업 생태계(B2B) 전체를 100% 무선으로 엮어내기 위해 고안되었다.

4G 시대의 단일 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인(1차선 도로)에서는 치명적인 병목 문제가 터졌다. 로봇 원격 수술 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 유튜브 4K 영상 트래픽이 한 망에 뒤섞이면, 영상 때문에 랙([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))이 발생해 수술 로봇의 제어가 빗나가 생명이 위험해진다. 산업계는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 용량을 20배 늘려라([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/))", "통신 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 1ms로 끊어라([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))", "1제곱킬로미터에 100만 대의 센서가 접속해도 뻗지 않게 해라([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))"라는 극단적인 3가지 조건(트라이앵글)을 요구했고, 5G는 이 모순된 과제를 모두 만족시키는 괴물 융합망으로 탄생했다.

- **📢 섹션 요약 비유**: 4G 고속도로는 덤프트럭(대용량), 앰뷸런스(초저지연 수술), 자전거 100만 대([IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서)가 한 차선에서 뒤엉켜 달리다 사고가 났습니다. 5G는 이 도로를 완벽하게 분리된 3차선으로 개조하여, 앰뷸런스는 하이패스로 1초 만에 뚫고, 자전거 100만 대는 전용 갓길로 안전하게 다니게 만든 기적의 도로 공학입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 3대 특성의 성능은 단순히 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 전파만 쏴서 달성되는 것이 아니라 정교한 클라우드 및 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 백엔드 기술이 융합되어 완성된다.

```text
+-------------------------------------------------------------+
|          5G 트라이앵글: 3대 초격차 요구사항의 융합 구조도                 |
+-------------------------------------------------------------+
|                      [ 🚀 1. eMBB (초고속/대용량) ]                |
|         (Enhanced Mobile Broadband / 20Gbps 타겟)                  |
|                  /\    "VR, 홀로그램 4K 스트리밍, 3D 맵 다운"             |
|                 /  \   (핵심 기술: 28GHz 초고주파, 빔포밍 Massive MIMO)   |
|                /    \                                               |
| +------------+------+------------+-------------------+|
| | 🤖 2. uRLLC (초저지연/고신뢰)      | 📡 3. mMTC (초연결/대량접속)||
| |  (Ultra-Reliable Low Latency)  |  (Massive Machine Type)  ||
| |  - 타겟: 1ms 응답 (1/1000초 컷)   |  - 타겟: 1km^당 100만 대 연결 ||
| |  - 용도: 자율주행 제어, 원격 수술    |  - 용도: 스마트팜, 수도 검침 센서||
| |  - 기술: MEC (모바일 엣지 컴퓨팅)   |  - 기술: 배터리 초절전, 무허가 접속||
| +--------------------------------+-------------------+|
| |  🌟 [ 코어 융합 뼈대: Network Slicing (네트워크 슬라이싱) 🔪 ] ||
| |  - 1개의 물리적 통신망을 3개의 독립된 가상망으로 찢어서 맞춤형 임대 서비스 ||
| +--------------------------------+-------------------+|
+-------------------------------------------------------------+
```

1. <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/">eMBB</a> (Enhanced Mobile Broadband)</strong>: 속도를 20Gbps로 폭발시키기 위해 텅텅 빈 28GHz 초고주파 대역([mmWave](/knowledge-base/studynote/03_network/03_physical_layer_media/156_mmwave_millimeter_wave/))을 도입했다. 전파가 직진성이 강해 잘 끊기는 단점은 수십 개의 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 구멍에서 전파를 한 유저에게 레이저처럼 쏘는 [빔포밍](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/)([Beamforming](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/)) 기술로 극복했다.
2. <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/">uRLLC</a> (Ultra-Reliable Low <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a>)</strong>: 통신 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 1ms를 맞추기 위해 클라우드 서버 뇌를 물리적으로 극단적 전진 배치하는 [MEC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/)([모바일 엣지 컴퓨팅](/knowledge-base/studynote/03_network/12_iot_wpan_edge/999_mec_mobile_edge_computing/))를 사용했다. 서울 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터까지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보내지 않고 기지국 바로 밑에 달린 초미니 서버에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 즉시 0.001초 만에 반사해 낸다.
3. <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/">mMTC</a> (Massive Machine Type Communications)</strong>: 기지국 과부하를 막기 위해, 센서들이 연결 전 허락(Handshake)을 받는 복잡한 통신 오버헤드를 생략하고 무지성으로 패킷을 던지게 만들어 저전력과 대규모 동시 접속을 달성했다.

- **📢 섹션 요약 비유**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 훈련소는 100m 단거리 우사인 [볼트](/knowledge-base/studynote/15_devops_sre/05_devsecops/236_vault_dynamic_secrets_ttl/)([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/)), 0.001초 만에 찌르는 펜싱 국가대표([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)), 물 한 모금 먹고 수십 킬로미터를 버티는 마라톤 좀비 군단([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))이라는 세 명의 완전 다른 선수를 한 건물 안에서 맞춤형으로 훈련시키는 스포츠 과학 센터입니다.

---

## Ⅲ. 비교 및 연결

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 망 구축 과정에서 통신사들의 비용 절감 꼼수로 짝퉁 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)([NSA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/))와 진짜 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/))의 딜레마가 발생했다.

| 비교 기준 | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [NSA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/) (Non-[Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/) / 과도기 혼종) | [5G SA](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/) ([Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/) / 진정한 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어망) |
| :--- | :--- | :--- |
| **코어망 아키텍처** | <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/">낡은 4G [LTE</a> 코어 뇌]</strong> + 5G [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 입구] | **5G 전용 클라우드 코어 뇌]** + 5G [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 입구] |
| **특성 지원 여부** | [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/)(속도)만 반쪽짜리로 빨라짐. 낡은 뇌 때문에 **uRLLC와 mMTC는 지원 불가** | <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/">eMBB</a>, <a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/">uRLLC</a>, <a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/">mMTC</a> 트라이앵글 100% 융합 달성</strong> |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">네트워크 슬라이싱</a></strong>| 불가능 (물리망 찢기 불가) | **완벽한 가상망 분할 지원 (핵심 비즈니스 무기)** |
| **통화 널뛰기 문제**| [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 안 잡히면 LTE로 휙휙 스위칭하느라 폰 배터리 타죽고 전화 끊김 잦음 | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용 망으로 널뛰기([Handover](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/) 랙) 없고 배터리 20% 절약 |

진짜 자율주행이나 B2B 무인 공장 제어를 하려면 통신망의 뇌부터 발끝까지 100% [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용 쇳덩이로 채워진 [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)([Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/)) 모드가 필수적이다.

- **📢 섹션 요약 비유**: NSA는 낡은 경운기([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어)에 포르쉐 바퀴([5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/))만 달아놓고 5G라고 홍보한 셈입니다. 겉보기엔 빨라 보여도 짐을 많이 싣거나 정밀한 핸들링([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))은 절대 안 됩니다. 반면 SA는 엔진과 뼈대 전체를 100% 포르쉐 순정 부품으로 갈아 끼운 진정한 스포츠카입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

산업 현장에서 5G의 강점을 극대화하려면 무턱대고 도입하는 것이 아니라 특성에 맞는 정교한 융합 아키텍처 설계가 필요하다.

### 실무 판단 시나리오
1. <strong>스마트 팩토리의 Wi-Fi 붕괴와 특화망(이음 <a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a>) 구원</strong>: 무인 운반 로봇(AGV) 제어를 싸구려 Wi-Fi로 구축하면, 기지국이 넘어갈 때([로밍](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/560_roaming/)) 통신이 끊기거나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 충돌 회피([CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/[CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)) 랙으로 로봇이 기둥에 들이박는다. 아키텍트는 퍼블릭 통신사 망을 쓰지 않고 정부 주파수(4.7GHz)를 직접 할당받아 공장 앞마당에 나만의 <strong><a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">폐쇄형 이음 [5G</a> 특화망 (<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/365_5g_tsn/">Private 5G</a>)]</strong>을 박아 넣는다. 완벽한 [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) 1ms 통제권을 확보하여 보안 유출을 차단하고 기계 충돌을 0%로 만든다.
2. **저전력 비면허망(LPWA)과의 이기종 하이브리드 설계**: 100만 평 농장의 온도 센서에 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/)) 모뎀을 모두 박으면 기곗값과 통신비 폭탄으로 농장이 파산한다. 지능형 아키텍트는 끝단 센서들에는 통신비가 0원이고 건전지가 10년 가는 [로라](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)([LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)) 비면허 통신 깡통을 달고, 이 신호를 가운데서 싹 모아주는 대장 단말기(Gateway) 딱 1대에만 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 유심칩을 박아 클라우드로 쏜다. 비용을 1/100로 찢어발기는 극한의 가성비 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 설계다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">네트워크 슬라이싱</a> 격리(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">Isolation</a>) 실패</strong>: 1개의 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 망을 쪼개서 [센서용 [mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/) 슬라이스]와 [일반인 폰용 [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/) 슬라이스]로 나눠 팔았다. 해커가 깡통 센서 100만 대를 좀비로 감염시켜 디도스(DDoS) 폭격을 날렸다. 이때 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 격리 설계(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 통제)가 부실하면, 센서망이 터지면서 옆 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)인 시민 스마트폰 통신망까지 같이 도미노 셧다운으로 뻗어버리는 대재앙이 터진다.

- **📢 섹션 요약 비유**: 비닐하우스 온도계 100개에 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 폰을 다 달아주는 것은 유치원생 100명 소풍 갈 때 애들 100명에게 일일이 100만 원짜리 스마트폰을 쥐여주고 집에 카톡하라는 미친 짓입니다. 천재 원장님은 애들에게 천 원짜리 호루라기([LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/))만 걸어주고, 선생님 1명만 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 폰으로 연락을 취합하는 완벽한 가성비 구조를 짭니다.

---

## Ⅴ. 기대효과 및 결론

5G는 단순히 더 넓은 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))를 제공하는 것을 넘어 네트워크 장비 쇳덩이를 클라우드 소프트웨어로 해체하고 융합한 진정한 인프라 대혁명이다. [5G SA](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/) 코어([SBA](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/) 구조)는 통신 프로토콜을 웹 개발자들의 [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API와 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 컨테이너로 갈아치워, 트래픽 폭주 시 1초 만에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 엔진(UPF)을 100개로 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 방어하는 클라우드 네이티브의 유연성을 갖추었다.

이 [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/), [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/), mMTC라는 극단적 3대 특성의 십자 융합은 4G 시대 사람 중심의 모바일 생태계를 자율주행, 원격 로봇 수술, 무인 공장이라는 거대한 사물 통제 제국(B2B)으로 끌어올렸다. 비록 초고주파([mmWave](/knowledge-base/studynote/03_network/03_physical_layer_media/156_mmwave_millimeter_wave/))의 회절 한계로 전국망 커버리지 비용의 벽에 부딪혔지만, 네트워크를 가상으로 썰어 임대하는(Slicing) 비즈니스 모델과 시공간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 압살한 [엣지 컴퓨팅](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)([MEC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/))의 뼈대는 다가올 [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/)(1Tbps 초감각 하이퍼 커넥티비티) 시대를 위한 완벽한 주춧돌로 기록될 것이다.

- **📢 섹션 요약 비유**: 4G 시대 통신망이 오직 사람 승객만 태워 나르는 '일반 고속버스'였다면, [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 트라이앵글은 '3단 변신 만능 기차'입니다. 앞 칸([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/))은 거대한 짐을 나르는 화물칸, 중간 칸([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))은 목적지 역을 무정차 하이패스로 뚫고 가는 0.1초 구급 캡슐 칸, 꼬리 칸([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))은 모기 100만 마리가 한 번에 타도 무너지지 않는 미세 곤충 전용 객실입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">Network Slicing</a> (<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/">네트워크 슬라이싱</a>)</strong> | 하나의 물리적 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 쇳덩이 장비를 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 칼([SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/[NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/))로 썰어서 테슬라 전용 1조각, 넷플릭스 전용 1조각 등 독립망([VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 급)으로 임대하는 특급 마법. |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/">MEC</a> (Mobile <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/">Edge Computing</a> <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/">엣지 컴퓨팅</a>)</strong> | 클라우드 대장 서버까지 다녀오는 왕복 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)(50ms)을 지우기 위해, 사용자 바로 코앞 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 밑에 초미니 서버 뇌를 박아 1ms([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)) 응답을 달성하는 얍삽한 공간 압축술. |
| <strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a> (<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/">Standalone</a>) 코어망</strong> | 무늬만 5G인 [NSA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)(과도기)를 넘어 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)부터 심장까지 100% [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용 클라우드 소프트웨어로 채워진 진짜 무결점 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 구조. |
| <strong>이음 <a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> (<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/365_5g_tsn/">Private 5G</a> 특화망)</strong> | 공장이나 병원 내부에 통신사(SKT 등)를 거치지 않고 나만의 사설 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국과 코어망을 직접 깔아, 완벽한 초저지연과 제로 보안 유출을 달성하는 엔터프라이즈 사내망 융합 아키텍처. |

### 📈 관련 키워드 및 발전 흐름도

```text
4G (LTE) 모바일 브로드밴드 / 스마트폰 속도 및 모바일 B2C 중심 진화
    |
    v
[5G 트라이앵글 3대 특성 융합]
 eMBB (초고속 대용량 20Gbps) --> 28GHz 초고주파, Massive MIMO 빔포밍
 uRLLC (초저지연 고신뢰 1ms) --> MEC (모바일 엣지 컴퓨팅) 시공간 지연 소각
 mMTC (초연결 IoT 대량 접속) --> 저전력 Grant-free 접속 및 무허가 슬립 모드
    |
    v
네트워크 슬라이싱 (Network Slicing) / 3대 특성을 한 망에서 가상 분리 독립 임대
    |
    v
SBA (Service Based Architecture) / 5G 코어망의 웹 기반 마이크로서비스(MSA) 전환
    |
    v
6G (초감각 하이퍼 커넥티비티) / 1Tbps 쾌속 및 원격 촉각/후각 데이터 무선 전송 시대 도래
```

### 👶 어린이를 위한 3줄 비유 설명

1. 4G([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)) 고속도로는 스마트폰(빠른 차)과 로봇(앰뷸런스), 수많은 센서(자전거)가 한 차선에서 뒤엉켜 달려서 매일 빵빵거리고 차가 막혔어요.
2. 천재 발명가들이 만든 <strong>'<a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a>'</strong>는 이 도로를 절대 부딪히지 않는 마법의 3차선 전용 도로로 갈라놓았어요!
3. 첫 번째 차선(<strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/">eMBB</a></strong>)은 엄청난 짐을 실은 덤프트럭이, 두 번째 차선(<strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/">uRLLC</a></strong>)은 0.001초 만에 쌩 통과하는 앰뷸런스 하이패스가, 세 번째 갓길(<strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/">mMTC</a></strong>)은 자전거 100만 대가 안전하게 달릴 수 있어서 기계들이 평화롭게 춤을 춘답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 148 / 552

<- **이전**: [147. UTM (Unmanned Aircraft System Traffic Management) - 무인 비행체 교통 관제 시스템](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/147_utm_unmanned_aircraft_system_traffic_management/)
**다음**: [149. 네트워크 슬라이싱 (Network Slicing) - 5G 융합 가상 격리 전용망](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) ->

---
