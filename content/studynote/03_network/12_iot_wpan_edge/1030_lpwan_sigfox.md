+++
title = "1030. 시그폭스 (SigFox) 협대역 통신"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SigFox(시그폭스)는 프랑스의 동명 회사가 독자 개발한 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/)([저전력 광역 통신망](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/)) 기술로, 아주 좁은 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)(Ultra Narrow Band, 100Hz)을 사용하여 전파의 도달 거리를 극대화한 통신 규격이자 서비스다.
> 2. **가치**: 한 번에 보낼 수 있는 데이터가 딱 12바이트([Byte](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/))에 불과하지만, 배터 소모가 거의 없어 AAA 건전지 하나로 10년을 버틸 수 있고, 칩셋 가격이 1달러 수준으로 저렴하여 일회용 센서나 화물 추적기에 공격적으로 탑재할 수 있다.
> 3. **판단 포인트**: 극단적인 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)(Up-link 위주) 통신과 프랑스 본사에 종속된 독점적 망 운영 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 때문에, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 원격 업데이트(OTA)가 필요하거나 자체 사설망(Private 망)을 구축하려는 엔터프라이즈 환경에서는 절대 채택할 수 없는 치명적 한계를 지닌다.

---

## Ⅰ. 개요 및 필요성

[사물인터넷](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)([IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 센서 중에는 하루 종일 잠만 자다가 "나 여기 살아있어", "문이 열렸어"라는 단 한 마디만 하루에 한 번씩 보내면 끝나는 단순한 기기들이 수백억 개 존재한다. 이런 기기들에게 [LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/)([로라](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/))나 [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) 같은 양방향 통신 [모뎀](/knowledge-base/studynote/03_network/03_physical_layer_media/146_modem_modulator_demodulator/)을 달아주는 것조차 사치였다. 

"가장 싸게, 가장 멀리, 가장 배터리를 적게 쓰게 만들자." 이 극단적인 세 가지 목표를 달성하기 위해, 프랑스의 스타트업 SigFox는 전송 속도와 다운로드 기능(양방향 통신)을 완전히 포기해버리는 과감한 결단을 내렸다. [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 극도로 좁힌 초협대역(UNB) 기술을 앞세워 글로벌 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 망을 구축하려 한 시도가 바로 SigFox다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">LPWAN 로라</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시그폭스 협대역 통신</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">NB-IoT 전력 최적화</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 대화를 주고받는 스마트폰이나 카카오톡 대신, 하루에 딱 한 번 "잘 도착함"이라는 세 글자만 적힌 무료 엽서를 날려 보내는 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 통신망이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SigFox의 가장 큰 특징은 **UNB(Ultra Narrow Band)** 기술과 망 운영의 중앙집중화다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">SigFox Cloud (프랑스 본사)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(모든 글로벌 데이터가 이곳으로 일단 모임)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SigFox Base Station</div><div class="kb-diagram-node">SigFox Base Station</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(한국 통신망)</div><div class="kb-diagram-cell">(유럽 통신망)</div></div>
<div class="kb-diagram-note">(100Hz 초협대역 900MHz 무선 전파, 최대 50km)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">화물 트래커</div><div class="kb-diagram-cell">해상 부표</div><div class="kb-diagram-cell">도난 방지기</div><div class="kb-diagram-cell">원격 온도계</div></div>
</div>
</div>



1. **UNB (Ultra Narrow Band)**: 일반적인 Wi-Fi가 20MHz의 폭을 쓴다면, SigFox는 불과 100Hz라는 바늘구멍 같은 좁은 폭으로 신호를 쏜다. [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 좁히면 잡음(Noise)이 들어올 틈이 적어져 수신 감도가 엄청나게 올라간다. 덕분에 적은 힘(배터리)으로도 전파를 수십 km 밖까지 밀어낼 수 있다.
2. **랜덤 액세스 (Random Access)**: 단말기는 자신이 보내야 할 타이밍(스케줄링)을 묻지 않는다. 잠에서 깨면 그냥 주파수 대역 중 빈 곳에 12바이트짜리 메시지를 똑같이 3번(중복 전송) 쏘고 다시 잠든다. 하나라도 기지국에 걸리기를 바라는 극도로 단순한 구조다(이 때문에 충돌 확률이 높다).
3. **독점적 클라우드**: 전 세계 어디서 SigFox 단말기가 신호를 보내든, 그 데이터는 각국의 기지국을 거쳐 프랑스의 SigFox 클라우드 본사 서버로 모두 모인 다음, 고객사의 앱으로 라우팅된다.

- **📢 섹션 요약 비유**: 목소리를 크게([전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/)) 내는 대신, 아주 얇고 높은 휘파람(초협대역)을 불어 멀리까지 들리게 한다. 언제 휘파람을 불지 눈치 보지 않고 그냥 허공에 대고 불어버린 다음 잠들어 버린다.

---

## Ⅲ. 비교 및 연결

LPWAN을 대표하는 세 기술의 철학을 1회 전송량(Payload)과 양방향 통신 관점에서 비교해 보자.

| 비교 항목 | SigFox | [LoRa](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) | [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) |
|:---:|:---|:---|:---|
| **1회 전송 데이터량** | <strong>최대 12 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/">Byte</a> (극단적 제한)</strong> | 최대 약 250 [Byte](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) | 최대 수 KByte |
| **양방향 (다운링크)** | 거의 불가능 (단말이 켤 때만 잠깐 수신) | 지원 (클래스별 다름) | 상시 양방향 지원 (스마트폰과 유사) |
| <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/146_modem_modulator_demodulator/">모뎀</a>/칩셋 가격</strong> | **약 1~2 달러 (일회용 가능)** | 약 3~5 달러 | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 달러 이상 |
| **인프라 구축 방식** | 오직 SigFox 사(또는 파트너)가 망 운영 | 누구나 사설망 구축 가능 | 이통사 면허 대역 기지국 사용 |
| **비즈니스 모델** | 글로벌 [로밍](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/560_roaming/) 통신비 과금 | 사설망은 무료 ([로밍](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/560_roaming/) 불가) | 통신사 요금제 가입 |

SigFox 단말기는 한국에서 배를 타고 출발해 유럽에 도착해도, 중간에 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경 없이 유럽 SigFox 망에 그대로 붙어 글로벌 [로밍](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/560_roaming/)(Global [Roaming](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/560_roaming/))이 된다는 엄청난 장점이 있다(클라우드가 하나로 통합되어 있기 때문).

- **📢 섹션 요약 비유**: NB-IoT가 무거운 택배 박스(대용량)를 안전하게 주고받는다면, SigFox는 글자 수가 12자로 제한된 무료 우편엽서를 전 세계 어디서든 우체통에 툭 던져넣는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
'글로벌 콜드체인(냉장 물류) 추적'에 가장 이상적이다. 백신이 든 상자에 1달러짜리 SigFox 센서를 버려질 각오로(일회용) 하나씩 넣는다. 이 센서는 배터리 충전 없이 한국에서 프랑스까지 가는 한 달 동안 "현재 온도 4도, 위치 좌표"라는 12바이트 데이터를 하루 3번씩 본사 클라우드로 쏜다.

**기술사 판단 포인트 (Trade-off):**
기술사가 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 프로젝트에서 SigFox를 검토할 때는 <strong>'다운링크(제어/업데이트)'와 '서비스의 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/">영속성</a>'</strong>을 최우선 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)로 삼아야 한다.
1. **OTA(Over The Air) 불가**: 버그가 발생하여 센서의 소프트웨어를 원격으로 업데이트(다운로드)해야 할 때, SigFox는 다운링크 속도가 비참할 정도로 느려 수천 대의 기기를 업데이트하는 것이 불가능하다. 제어가 필요한 시스템에는 절대 써서는 안 된다.
2. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/">벤더 종속</a> <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a></strong>: SigFox 본사가 파산하거나 한국의 파트너사가 사업을 철수하면, 깔아놓은 모든 센서가 한순간에 쇳덩어리가 된다(실제로 2022년 SigFox 본사가 파산 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 신청 후 인수됨). 사설망 구축이 안 되는 폐쇄형 생태계의 가장 무서운 단점이다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기기를 한 번 풀어놓으면 절대 수정할 수 없는 '던져놓고 잊는(Fire and Forget)' 일회용 무기다. 본사(SigFox) 망이 문을 닫는 순간 내가 산 무전기도 통째로 먹통이 된다는 점을 명심해야 한다.

---

## Ⅴ. 기대효과 및 결론

SigFox는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 통신망 설계에서 '데이터의 양을 극단적으로 다이어트하면 배터리와 비용의 혁신을 이룰 수 있다'는 철학을 세상에 증명했다. 모든 사물에 무거운 통신 모듈을 달아야 한다는 고정관념을 부수고, 1달러짜리 센서로 글로벌 [로밍](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/560_roaming/)을 구현한 아이디어는 획기적이었다.

결론적으로 SigFox는 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성과 일방통행이라는 기술적 한계 때문에 LoRa와 NB-IoT와의 주도권 싸움에서 밀려나 위기를 겪고 있다. 그러나 '가장 싸고 단순한 12바이트의 미학'이 필요한 글로벌 물류 추적과 농업 분야에서는 여전히 대체 불가능한 틈새(Niche) 시장을 점유하고 있으며, [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 시대에 수조 개의 '먼지(Dust) 센서'들을 연결할 초저비용 백스캐터(Backscatter) 통신의 선구적 모델로 평가받는다. 향후에는 자율형 엣지 협업 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 인터넷이 엄청나게 발전해도 누군가는 싸고 가벼운 '삐삐(호출기)'나 '엽서'를 원하듯, SigFox는 화려한 스마트폰 시대에 살아남은 가장 작고 끈질긴 아날로그 엽서다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) [로라](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 저전력 통신 (Low [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Communication) | 배터리 수명과 직접 연결된다. |
| [센서 네트워크](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/103_wsn_sensor_network/) (Sensor Network) | 수많은 단말의 연결 구조를 결정한다. |
| [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) 전력 최적화 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: LPWAN 로라</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: 시그폭스 협대역 통신</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: NB-IoT 전력 최적화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 자율형 엣지 협업</div></div>
</div>
</div>



시그폭스 협대역 통신는 [LPWAN](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/109_lpwan_low_power_wide_area_network/) [로라](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/283_lora_low_rank_adaptation/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [NB-IoT](/knowledge-base/studynote/03_network/12_iot_wpan_edge/620_nbiot_narrowband_iot_lte_guardband/) 전력 최적화와 자율형 엣지 협업 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스마트폰으로 전 세계에 톡을 보내려면 돈도 많이 들고 매일 배터리를 충전해야 해요.
2. 시그폭스는 "나 살아있어!"라는 딱 세 글자만 보낼 수 있지만, 동전 건전지 하나로 10년 동안 버티는 신기한 호출기예요.
3. 기계값이 천원밖에 안 해서, 소중한 택배 상자 안에 쏙 넣어두면 배 타고 외국에 가도 잃어버리지 않고 위치를 알려준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 133 / 1120

← **이전**: [102. TDD (Time Division Duplexing) - 시분할 이중화 (업/다운링크 분리)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/102_tdd/)
**다음**: [1031. NB-IoT 전력 최적화](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1031_nbiot_psm_edrx_power_saving/) →

---
