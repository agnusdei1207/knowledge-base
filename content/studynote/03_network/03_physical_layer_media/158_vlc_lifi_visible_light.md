+++
title = "158. 가시광 통신 (VLC, Visible Light Communication) / Li-Fi"
date = 2026-04-05

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가시광 통신 ([VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/), Visible Light Communication)은 [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) (Light Emitting [Diode](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/)) 조명의 빛 세기를 사람 눈에 느껴지지 않을 만큼 빠르게 변조해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전달하는 광무선 통신 기술이다.
> 2. **가치**: Li-Fi는 VLC를 네트워크 형태로 확장한 개념으로, RF (Radio Frequency) 혼잡과 전자파 간섭 문제를 줄이면서 실내 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)·고보안 무선 접속을 제공할 수 있다.
> 3. **판단 포인트**: [VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/)/Li-Fi는 Wi-Fi의 완전 대체재가 아니라, 가시선 확보, 조명 밀도, 상향 링크, 외란광 차단이 가능한 실내 공간에서 강점을 발휘하는 보완 기술로 봐야 한다.

---

## Ⅰ. 개요 및 필요성

가시광 통신은 우리가 조명으로 쓰는 빛을 통신 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)로 재활용하는 기술이다. 전파 기반 무선 통신이 안테나로 보이지 않는 전자파를 내보낸다면, VLC는 천장 조명의 밝기를 매우 빠르게 조절해 0과 1을 실어 보낸다. 사람 눈은 이런 고속 깜빡임을 인지하지 못하므로, 조명 기능과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송을 동시에 수행할 수 있다.

이 기술이 주목받는 이유는 무선 트래픽 증가와 RF 대역 혼잡 때문이다. 병원, 항공기, 산업 현장처럼 전자파 간섭이 민감한 공간에서는 전파 사용이 제한되기도 한다. 또한 실내 위치 기반 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 고밀도 소형 셀, 물리적 보안이 중요한 회의실에서는 “벽을 뚫고 퍼지는 전파”보다 “방 안에서만 머무는 빛”이 더 적합할 수 있다. 이런 필요가 VLC와 Li-Fi의 실용성을 키웠다.

- **📢 섹션 요약 비유**: VLC는 천장 전등이 단순히 방을 밝히는 것에서 끝나지 않고, 깜빡이는 비밀 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 정보를 속삭여 주는 똑똑한 등불과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

VLC의 기본 원리는 IM/[DD](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/) (Intensity Modulation / [Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))이다. 송신부는 [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) 전류를 조절해 빛의 세기를 변조하고, 수신부는 포토다이오드 (Photodiode)나 이미지 센서가 이를 감지해 전기 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 복원한다. Li-Fi는 여기서 더 나아가 다중 사용자 접속, 상향 링크, [이동성 관리](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/561_mobility_management_hlr_vlr_paging/), IP 네트워킹을 포함하는 시스템 수준 개념이다.

### 구성 요소와 설계 포인트

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) 조명 / 드라이버 | 빛으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 송신 | 고속 스위칭, 조명 품질, 디밍 지원 |
| 광 수신기 (Photodiode) | 빛 세기 변화 감지 | 감도, 시야각, 잡광 내성 |
| 변조 방식 | OOK (On-Off Keying), OFDM (Orthogonal Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) [Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 등 | 속도와 복원 복잡도의 균형 |
| 상향 링크 | 적외선 ([IR](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/165_ir/), Infrared) 또는 RF 보조 | 단말 배터리 소모와 비대칭성 해결 |
| 컨트롤러 | 셀 관리, [핸드오버](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/), [백홀](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1009_backhaul_network_base_station_core_connection/) 연동 | Wi-Fi/Ethernet과의 통합 운영 |

아래 그림은 Li-Fi 셀에서 조명과 통신이 함께 동작하는 모습을 보여 준다.

```text
+----------------------------------------------------------------------------+
|                    Li-Fi room cell: light and data together               |
+----------------------------------------------------------------------------+
| [Ethernet / Switch]                                                       |
|        |                                                                   |
|        v                                                                   |
| [Li-Fi Controller]                                                         |
|        |                                                                   |
|        v                                                                   |
| [Ceiling LED AP]  >>> visible-light downlink >>>  [Laptop / Phone + PD]   |
|        ^                                              |                    |
|        +------------ IR / RF uplink (optional) -------+                    |
|                                                                            |
| Wall blocks light leakage  -> higher spatial reuse / stronger room security |
+----------------------------------------------------------------------------+
```

이 구조의 핵심은 다운로드는 천장 조명에서 넓게 제공하되, 업로드는 적외선이나 다른 보조 채널로 분리할 수 있다는 점이다. 또한 조명 셀 반경이 작아 같은 건물 안에서도 공간 재사용이 쉽고, 벽을 통과하지 않으므로 [보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)이 높다. 반면 손으로 수신부를 가리거나, 직사광선이 강하게 들어오거나, 단말이 빠르게 이동하면 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 품질이 급격히 나빠질 수 있다.

- **📢 섹션 요약 비유**: Li-Fi는 천장 스피커가 노래를 틀어 주는 동시에, 박자 속에만 숨겨진 암호를 보내는 것과 같다. 음악은 들리지만, 암호는 전용 수신기만 알아듣는다.

---

## Ⅲ. 비교 및 연결

[VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/)/Li-Fi의 위치를 이해하려면 Wi-Fi와 적외선 기반 광통신과 비교하는 것이 좋다.

| 항목 | Wi-Fi | [VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/) / Li-Fi | 적외선 ([IR](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/165_ir/), Infrared) 통신 |
| :--- | :--- | :--- | :--- |
| [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) | RF (Radio Frequency) | 가시광선 | 적외선 |
| 벽 투과 | 가능 | 거의 불가 | 거의 불가 |
| 전자파 간섭 | 존재 가능 | 매우 낮음 | 낮음 |
| 주 사용 환경 | 범용 무선 LAN | 실내 조명 기반 고밀도 셀 | 리모컨, 짧은 점대점 링크 |
| 강점 | 이동성, 범용성 | [보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), [주파수 재사용](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/554_frequency_reuse_cluster_capacity/), EMI 민감 환경 | 간단한 근거리 제어 |
| 약점 | 혼잡, 간섭 | 가시선/잡광/업링크 제약 | 네트워킹 확장성 낮음 |

이 비교에서 Li-Fi는 단순한 “빛 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) Wi-Fi”가 아니라는 점이 드러난다. VLC는 광무선 통신 (OWC, Optical Wireless Communication)의 한 갈래이고, Li-Fi는 그중에서도 실내 네트워크 접속을 목표로 한 시스템 개념이다. 따라서 Wi-Fi와 경쟁하면서도 동시에 상호 보완 관계다. 예를 들어 기본 이동성과 광역 커버리지는 Wi-Fi가 맡고, 회의실·병실·생산라인 같은 특정 공간에서는 Li-Fi가 추가 용량과 보안을 제공하는 방식이 현실적이다.

- **📢 섹션 요약 비유**: Wi-Fi가 건물 전체에 울려 퍼지는 무전기라면, Li-Fi는 방 안에서만 통하는 손전등 암호다. 멀리 퍼지진 않지만, 같은 공간 안에서는 더 조용하고 안전하게 쓸 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/)/Li-Fi는 병원 수술실, 항공기 객실, [스마트 팩토리](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/), 군·금융 보안실, 박물관 안내, 실내 정밀 위치 추정처럼 “전파 간섭이 부담되거나, 셀을 잘게 나누고 싶은 공간”에서 특히 유리하다. 조명 인프라가 이미 존재하므로, 잘 설계하면 통신 인프라와 실내 조명을 함께 운영할 수 있다는 장점도 있다. 반면 사용자가 스마트폰을 자유롭게 흔들며 이동하고, 창가 햇빛이 강하고, 조명이 자주 꺼지는 환경이라면 설계 난도가 크게 올라간다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **가시선 (LoS, Line of Sight)과 조명 커버리지가 확보되는가?** 그림자 영역이 많으면 품질이 불안정하다.
2. **상향 링크를 어떻게 설계할 것인가?** 적외선, RF 보조, 하이브리드 구성을 미리 정해야 한다.
3. **외란광과 디밍 조건을 감당할 수 있는가?** 태양광, 반사광, 저조도 조건을 함께 검증해야 한다.
4. <strong>Wi-Fi와 <a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/">핸드오버</a>를 통합할 것인가?</strong> 단독망보다 하이브리드 운영이 현실적인 경우가 많다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Li-Fi를 모든 무선 환경에 동일하게 적용 가능한 만능 기술로 보는 판단
- 업로드 경로와 사용자 이동성을 검토하지 않고 다운로드 성능만 강조하는 설계
- 조명 품질, 눈부심, 유지보수, 보안 정책을 네트워크와 분리해서 따로 보는 접근

- **📢 섹션 요약 비유**: Li-Fi 도입은 집 안 모든 길을 유리 다리로 바꾸는 일이 아니다. 밝고 통제된 방에서는 아주 좋지만, 비바람이 들이치는 야외까지 같은 방식으로 덮을 수는 없다.

---

## Ⅴ. 기대효과 및 결론

[VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/)/Li-Fi가 성숙하면 실내 무선 네트워크는 단순히 더 빠른 접속을 넘어, 조명·위치·보안이 결합된 공간형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 발전할 수 있다. 조명 인프라와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송을 통합하면 공간 재사용성이 높아지고, 전파 혼잡을 줄이며, 특정 구역에 매우 높은 용량을 집중할 수 있다. 특히 [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 실내망, XR (Extended Reality), 산업 자동화, 정밀 위치 인식과의 연계 가능성이 크다.

다만 이 기술은 물리 조건에 민감하고, 상향 링크와 [핸드오버](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/556_handover_handoff_types_concept/) 설계가 까다롭다. 따라서 [VLC](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/1021_vlc_lifi/)/Li-Fi는 Wi-Fi를 없애는 기술이 아니라 <strong>RF 무선망을 보완하는 실내 고밀도 광셀 기술</strong>로 기억하는 편이 정확하다. 빛의 속도보다 중요한 것은, 그 빛을 안정적으로 네트워크 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 바꾸는 시스템 설계 능력이다.

- **📢 섹션 요약 비유**: Li-Fi는 천장 조명을 인터넷 도로로 바꾸는 기술이다. 방 안에서는 아주 빠른 전용차로가 되지만, 건물 전체를 잇는 고속도로 역할까지 혼자 맡지는 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| OWC (Optical Wireless Communication) | VLC와 Li-Fi가 속하는 상위 광무선 통신 범주 |
| IM/[DD](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/) (Intensity Modulation / [Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/)) | VLC의 기본 송수신 방식 |
| [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) (Light Emitting [Diode](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/)) | 조명과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 송신을 동시에 담당하는 핵심 소자 |
| Photodiode | 빛 세기 변화를 전기 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 복원하는 수신기 |
| Wi-Fi | Li-Fi와 경쟁하면서도 하이브리드로 공존하는 대표 무선 LAN |
| 실내 위치기반 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Indoor Positioning) | 조명 셀 기반 정밀 위치 추정으로 확장 가능한 응용 |

### 📈 관련 키워드 및 발전 흐름도

```text
광무선 통신 (OWC)
    |
    v
가시광 통신 (VLC)
    |
    +-- IM/DD · LED 변조 · Photodiode 수신
    |
    v
Li-Fi 네트워킹
    |
    v
실내 고밀도 셀 · 보안 구역 통신 · 위치기반 서비스 · 6G 실내망
```

이 흐름은 VLC가 단순 조명 제어가 아니라, 광무선 전송에서 시작해 실내 네트워크와 공간 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 확장되는 기술 축임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Li-Fi는 방 전등이 불만 켜는 게 아니라, 아주 빠르게 깜빡이며 인터넷 편지를 보내는 거예요.
2. 벽 밖으로 잘 새지 않아서 같은 방 안에서는 더 비밀스럽게 쓸 수 있어요.
3. 하지만 빛이 가려지면 편지도 잘 안 보이니까, 밝은 길을 잘 만들어 줘야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 279 / 1120

<- **이전**: [157. 테라헤르츠 (THz) - 6G 통신 대상 대역](/knowledge-base/studynote/03_network/03_physical_layer_media/157_terahertz_thz_6g/)
**다음**: [159. 음향 통신 (수중 음파 통신)](/knowledge-base/studynote/03_network/03_physical_layer_media/159_underwater_acoustic_communication/) ->

---
