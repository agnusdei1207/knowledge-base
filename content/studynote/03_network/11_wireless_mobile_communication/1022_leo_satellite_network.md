---
title: "1022. 저궤도 위성망 (LEO)과 스타링크"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)망과 스타링크는 무선·이동통신에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)망과 스타링크를 이해하면 스펙트럼 효율과 이동성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

지구상의 광케이블과 해저 케이블 망은 도심지에 집중되어 있어, 산간벽지, 사막, 바다, 항공기 등 전 세계 면적의 절반 이상은 여전히 '인터넷 사각지대'로 남아있다. 이를 해결하기 위해 과거부터 36,000km 상공에 띄운 정지궤도([GEO](/studynote/03_network/11_wireless_mobile_communication/593_geo_geostationary_earth_orbit_satellite/)) [위성 통신](/studynote/03_network/11_wireless_mobile_communication/592_satellite_communication_characteristics/)을 사용했으나, 거리가 너무 멀어 전파가 왕복하는 데만 0.5초가 넘어 실시간 화상회의나 게임이 불가능했다.

이 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 문제를 물리적으로 해결하기 위해 위성을 땅과 가까운 500km 상공으로 확 끌어내린 것이 저궤도([LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)) 위성망이다. 고도가 낮아진 대신 지구 전체를 덮으려면 수천 개의 위성이 촘촘한 그물망(Constellation)을 형성해야 하므로, 로켓 재사용 기술(발사 비용 절감)을 앞세운 스페이스X의 '스타링크(Starlink)'가 이 시장을 폭발적으로 개화시켰다.

```text
[가시광 통신 라이파이]
    |
    v
[저궤도 위성망과 스타링크]
    |
    +---> [위성 통신 핸드오버 (ISL]
```

- **📢 섹션 요약 비유**: 엄청나게 높은 곳에 뜬 아주 밝은 태양 1개(정지궤도)는 빛이 도달하는 데 오래 걸리지만, 아주 낮게 뜬 수만 개의 작은 가로등(저궤도)을 촘촘히 깔면 그림자 없이 즉각적으로 땅을 밝힐 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

스타링크로 대표되는 [LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 위성망 아키텍처는 크게 세 가지 요소로 구성된다. 지상 단말(User Terminal), [저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 군집(Constellation), 그리고 지상의 게이트웨이(Ground [Station](/studynote/03_network/04_data_link_layer_error/218_hdlc_station_primary_secondary/))다.

```text
+--------------------------------------------------------+
|               [ LEO 위성 군집 (고도 500km) ]             |
|                                                        |
|  [위성 A] <------ (위성 간 레이저 통신, ISL) ------> [위성 B] |
|   ^  |                                          ^  | |
|   |  | (RF 전파: Ku/Ka 대역)                    |  | |
|   |  v                                          |  v |
+--------------------------------------------------------+
|+--------------+                          +--------------+|
|| 지상 단말기  |                          | 지상 게이트웨이||
||(위상배열 안테나)|                          |(인터넷 백본 연결)||
|+--------------+                          +--------------+|
+--------------------------------------------------------+
```

1. <strong>위상배열 <a href="/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/">안테나</a> (Phased <a href="/studynote/08_algorithm_stats/04_datastructure/055_array/">Array</a> <a href="/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/">Antenna</a>)</strong>: 지상 단말(접시 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/))은 모터를 돌려 위성을 쫓아가는 것이 아니라, 수백 개의 미세한 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 소자가 전파의 위상(Phase)을 전자적으로 조절하여 눈에 보이지 않는 전파 빔의 방향을 1초에도 수백 번씩 꺾어 날아가는 위성을 정밀하게 추적한다([Beamforming](/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/)).
2. <strong><a href="/studynote/03_network/05_lan_wan_l2_devices/249_isl_inter_switch_link_cisco/">ISL</a> (<a href="/studynote/03_network/11_wireless_mobile_communication/1023_satellite_isl_handover/">Inter-Satellite Link</a>)</strong>: 초창기 [LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 위성은 지상 단말과 지상 게이트웨이를 단순 중계하는 '구부러진 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)(Bent-pipe)' 역할만 했으나, 최근에는 위성끼리 우주 공간에서 레이저(Optical)로 직접 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는 ISL을 탑재하여 지상 기지국 없이도 대륙 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송이 가능해졌다.

- **📢 섹션 요약 비유**: KTX처럼 엄청나게 빨리 지나가는 기차(위성)를 향해, 고개를 돌리지 않고 눈동자만 휙휙 굴려가며(위상배열 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)) 끊김 없이 대화를 주고받는 엄청난 동체 시력의 결과물이다.

---

## Ⅲ. 비교 및 연결

위성의 고도에 따른 통신 시스템을 비교하면 LEO의 극단적인 특성이 드러난다.

| 비교 항목 | [GEO](/studynote/03_network/11_wireless_mobile_communication/593_geo_geostationary_earth_orbit_satellite/) (정지궤도) | [MEO](/studynote/03_network/11_wireless_mobile_communication/594_meo_medium_earth_orbit_gps/) (중궤도) | [LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) (저궤도) |
|:---:|:---|:---|:---|
| **고도** | 약 36,000 km | 2,000 ~ 36,000 km | **500 ~ 1,200 km** |
| <strong><a href="/studynote/03_network/01_data_communication/017_전송_지연/">전송 지연</a> (<a href="/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/">RTT</a>)</strong>| 약 500 ~ 600 ms (느림) | 약 100 ~ 150 ms | **약 20 ~ 40 ms (유선 광랜 급)** |
| **전 지구 커버 필요 수**| 단 3대 | 수십 대 | **수천 ~ 수만 대 (Constellation)** |
| **위성의 움직임** | 지상에서 볼 때 정지해 있음 | 천천히 이동 | **시속 27,000km로 빠르게 이동 (90분/1주)** |
| <strong>단말 <a href="/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/">안테나</a></strong> | 고정형 파라볼라 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) | 추적형 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 필요 | **초정밀 위상배열 (전자식 트래킹) 필수** |

[LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 위성망은 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)/[6G](/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 통신에서 NTN(Non-Terrestrial Network, [비지상 네트워크](/studynote/06_ict_convergence/02_iot_mobility/154_ntn_non_terrestrial_network_6g/))이라는 핵심 표준으로 편입되어, 하늘을 나는 드론(UAV), 도심항공교통([UAM](/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/)), 바다 위 선박까지 모두 스마트폰 하나로 연결되는 '3차원 공간 통신망'의 기반이 된다.

- **📢 섹션 요약 비유**: GEO가 산꼭대기에 사는 한 명의 확성기 아저씨(멀고 느리지만 다 들림)라면, LEO는 동네 골목골목을 뛰어다니며 귓속말을 전해주는 수만 명의 배달부 소년들이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
도심지에서는 기존 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)/광랜이 훨씬 싸고 빠르므로 LEO가 경쟁력이 없다. 그러나 재난재해로 지상 기지국이 붕괴된 상황(예: 우크라이나 전쟁, 대규모 지진), 광케이블을 깔 수 없는 사막의 태양광 발전소나 해상 시추선, 비행기 기내 와이파이 환경에서는 유일무이한 백본망([Backhaul](/studynote/03_network/20_performance_evaluation_advanced/1009_backhaul_network_base_station_core_connection/)) 솔루션이 된다.

**기술사 판단 포인트 (Trade-off):**
[LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 위성망 도입을 검토할 때는 <strong>'전파 대역의 한계'와 '하늘의 혼잡도'</strong>를 판단해야 한다.
1. [LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 위성은 매우 높은 고주파수(Ku/Ka 대역, 12~30GHz)를 사용하므로 폭우나 폭설이 내리면 전파가 빗방울에 흡수되어 통신이 끊어지는 '강우 감쇠(Rain Fade)' 현상이 치명적이다.
2. 따라서 임무 수행 크리티컬(Mission Critical) 환경에서는 [LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)만 믿어선 안 되며, 기존 지상 4G/LTE나 다른 저주파수(L/S 대역) 위성망과의 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)(Multi-path) 설계로 가용성을 확보해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 비가 많이 오면 택배(고주파 전파)가 비에 젖어 훼손될 수 있으니, 아주 중요한 물건은 느리더라도 비바람에 끄떡없는 튼튼한 장갑차(저주파 지상망)에 나누어 싣는 설계가 필요하다.

---

## Ⅴ. 기대효과 및 결론

[저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)망은 전 세계 30억 명의 통신 소외 계층에게 디지털 평등(Digital Divide 해소)을 가져다줄 가장 강력한 수단이다. [6G](/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 시대에 이르면 지상 기지국과 우주 기지국(위성)의 경계가 허물어지며, 사용자는 스마트폰이 기지국에 연결되었는지 위성에 연결되었는지조차 인식하지 못하게 될 것이다.

결론적으로 [LEO](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/) 위성망은 발사체 기술(우주공학)과 초고주파 [빔포밍](/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/) 기술(전자공학), 그리고 수만 개의 위성을 엮는 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 기술(네트워크 공학)이 결합된 인류 최대의 IT 인프라 프로젝트다. 기술사는 이를 단순한 위성이 아닌 '우주에 떠 있는 거대한 소프트웨어 정의 라우터([SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/))'망으로 인식하고 아키텍처에 통합해야 한다. 향후에는 지능형 무선 자원 제어 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 땅을 파서 선을 묻는 시대가 끝나고, 하늘에 보이지 않는 거대한 '우주 와이파이 공유기 텐트'를 쳐서 지구촌 어디서든 뚜껑만 열면 인터넷이 쏟아지게 만든 혁명이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [가시광 통신](/studynote/03_network/03_physical_layer_media/158_vlc_lifi_visible_light/) 라이파이 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 셀 (Cell) | 무선 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 범위를 나누는 기본 단위다. |
| [핸드오버](/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/) ([Handover](/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/)) | 이동 중에도 연결을 유지하게 만든다. |
| [위성 통신 핸드오버](/studynote/09_security/uncategorized/1101_isl_inter_satellite_link_low_earth_orbit_routing/) ([ISL](/studynote/03_network/05_lan_wan_l2_devices/249_isl_inter_switch_link_cisco/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 가시광 통신 라이파이]
    |
    v
[현재 개념: 저궤도 위성망과 스타링크]
    |
    +---> [확장 A: 위성 통신 핸드오버 (ISL]
    +---> [확장 B: 지능형 무선 자원 제어]
```

[저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/)망과 스타링크는 [가시광 통신](/studynote/03_network/03_physical_layer_media/158_vlc_lifi_visible_light/) 라이파이에서 출발해 현재 메커니즘을 정교화하고, 이후 [위성 통신 핸드오버](/studynote/09_security/uncategorized/1101_isl_inter_satellite_link_low_earth_orbit_routing/) (ISL와 지능형 무선 자원 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 보통 우주 위성은 너무 멀리 있어서 지구에서 카카오톡을 보내면 한참 뒤에 답장이 와요.
2. 스타링크([저궤도 위성](/studynote/03_network/11_wireless_mobile_communication/595_leo_low_earth_orbit_starlink_6g/))는 위성 수만 개를 지구 코앞으로 바짝 끌어내려서 전파가 눈 깜짝할 새에 도착하게 만들었어요.
3. 사막 한가운데나 태평양 바다 한가운데서도 밤하늘만 보이면 광랜처럼 빠른 인터넷을 쓸 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 1120

<- **이전**: [1021. 가시광 통신 (VLC) 라이파이 (Li-Fi)](/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/)
**다음**: [1023. 위성 통신 핸드오버와 ISL (Inter-Satellite Link)](/studynote/03_network/11_wireless_mobile_communication/1023_satellite_isl_handover/) ->

---
