+++
title = "54. 반송파 (Carrier Wave)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 반송파 (Carrier [Wave](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/590_wave_ieee_802_11p_dsrc_v2x/))는 정보를 실어 나르기 위한 고주파 정현파다.
> 2. **가치**: 베이스밴드 ([Baseband](/knowledge-base/studynote/03_network/19_frequent_topics_terms/940_baseband_line_coding_nrz_rz_manchester/)) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 원거리 전송 가능한 패스밴드 (Passband)로 바꾸는 데 필요하다.
> 3. **판단 포인트**: AM (Amplitude Modulation), FM (Frequency Modulation), PM (Phase Modulation) 등 변조 방식에 따라 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 잡음 내성이 달라진다.

---

## Ⅰ. 개요 및 필요성

저주파 정보 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)는 그대로 멀리 보내기 어렵다. 그래서 고주파 반송파에 실어 보낸다. 반송파는 정보 그 자체가 아니라 정보를 운반하는 매개체다.

라디오, 무선 통신, [위성 통신](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/592_satellite_communication_characteristics/), 셀룰러 시스템은 모두 반송파와 변조를 기본으로 한다.

- **📢 섹션 요약 비유**: 반송파는 편지를 싣고 달리는 트럭이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

반송파는 보통 `s(t)=A cos(2πf_ct+φ)` 형태의 사인파로 표현된다. 정보는 진폭, 주파수, 위상을 바꿔 실린다.

```text
정보 신호 → 변조 → 반송파 → 전송 채널 → 복조 → 정보 신호
```

| 항목 | 의미 | 포인트 |
| :--- | :--- | :--- |
| A | 진폭 | 세기 |
| f_c | 반송 주파수 | 채널 위치 |
| φ | 위상 | 시간 기준 |
| 변조 | 정보 부호화 | 전송 가능화 |

핵심은 정보 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 반송파에 "실어" 보내야 멀리 보내고, 주파수 대역을 효율적으로 사용할 수 있다는 점이다.

- **📢 섹션 요약 비유**: 반송파는 말 자체가 아니라, 말을 멀리 보내는 확성기다.

---

## Ⅲ. 비교 및 연결

베이스밴드는 원래 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 대역이고, 패스밴드는 반송파에 실린 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)다. 디지털 통신에서는 QAM, [PSK](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/) 같은 디지털 변조가 반송파 위에서 작동한다.

| 항목 | 베이스밴드 | 패스밴드 |
| :--- | :--- | :--- |
| 중심 주파수 | 0Hz 부근 | [fc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) 부근 |
| 전송 방식 | 직접 | 반송파 사용 |
| 활용 | 유선 일부 | 무선 대부분 |

반송파는 채널 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 크기, 간섭 회피와도 연결된다. 주파수가 너무 낮으면 멀리 보내기 불리하고, 너무 높으면 손실과 직진성 문제가 생길 수 있다.

- **📢 섹션 요약 비유**: 베이스밴드는 마을 길, 패스밴드는 고속도로다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 반송파 주파수, 변조 방식, [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 전파 환경, 수신기 감도를 함께 본다. 변조를 바꾸면 속도와 내성이 동시에 바뀐다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 반송 주파수가 채널에 맞는가?
2. AM/FM/PM 중 요구사항에 맞는 변조인가?
3. [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 잡음 내성의 균형이 맞는가?
4. 복조기와 동기 기준이 안정적인가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 반송파와 정보 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 구분하지 않는 경우
- 채널 특성을 무시하고 고차 변조를 고집하는 경우
- [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)만 보고 전송 품질을 무시하는 경우

기술사 관점에서는 반송파가 단순 파형이 아니라 무선 통신의 전달 매개체라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: 반송파는 편지를 싣는 배이고, 변조는 배에 주소를 붙이는 일이다.

---

## Ⅴ. 기대효과 및 결론

반송파는 정보를 멀리, 효율적으로, 선택적으로 보내게 해 준다. 현대 통신의 기본 전제다.

정리하면, 반송파는 정보를 전달하는 이동 수단이고, 변조는 그 수단에 정보를 싣는 방법이다.

- **📢 섹션 요약 비유**: 반송파는 택배차, 변조는 상자에 주소를 쓰는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Baseband](/knowledge-base/studynote/03_network/19_frequent_topics_terms/940_baseband_line_coding_nrz_rz_manchester/) | 원 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) |
| Passband | 전송 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) |
| AM/FM/PM | 변조 방식 |
| Carrier Frequency | 채널 위치 |
| Demodulation | 복원 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">정보 신호</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">변조</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">반송파 실음</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">전송 채널</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">복조</div>
</div>
</div>



이 흐름은 정보가 전파에 실려 이동하고 다시 원형으로 돌아오는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 반송파는 멀리 가는 트럭이에요.
2. 편지를 트럭에 싣고 보내면 멀리까지 갈 수 있어요.
3. 도착하면 편지를 다시 꺼내 읽어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 54 / 1120

← **이전**: [53. 성상도 (Constellation Diagram)](/knowledge-base/studynote/03_network/01_data_communication/053_성상도_Constellation_Diagram/)
**다음**: [55. 아날로그 연속파 변조 (AM/FM/PM)](/knowledge-base/studynote/03_network/01_data_communication/055_아날로그_연속파_변조_AM_FM_PM/) →

---
