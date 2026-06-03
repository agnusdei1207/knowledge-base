+++
title = "56. 표본화 (Sampling)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 표본화는 연속 신호를 일정한 시간 간격으로 샘플링해 이산 신호로 바꾸는 과정이다.
> 2. **가치**: Nyquist (나이퀴스트) 조건을 만족해야 원신호 복원이 가능하다.
> 3. **판단 포인트**: 샘플링 주파수가 낮으면 [aliasing](/knowledge-base/studynote/03_network/01_data_communication/057_에일리어싱_Aliasing/) ([에일리어싱](/knowledge-base/studynote/03_network/01_data_communication/057_에일리어싱_Aliasing/))이 발생한다.

---

## Ⅰ. 개요 및 필요성

아날로그 신호를 디지털로 바꾸려면 먼저 표본을 떠야 한다. 표본화는 [PCM](/knowledge-base/studynote/03_network/19_frequent_topics_terms/943_pcm_pulse_code_modulation_sampling_quantization/) (Pulse [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Modulation)의 첫 단계다.

음성, 영상, 센서 신호를 디지털 시스템으로 처리하려면 필수다.

- **📢 섹션 요약 비유**: 표본화는 강물을 일정 간격으로 떠서 물 상태를 검사하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

표본화는 시간축에서 신호를 끊어 값만 읽는다. 샘플링 주파수는 원신호의 최고 주파수의 최소 두 배 이상이어야 한다.

```text
Analog Signal → Sampling → Discrete-Time Samples
```

| 항목 | 의미 | 포인트 |
| :--- | :--- | :--- |
| Sampling Rate | 초당 샘플 수 | Hz |
| Nyquist Rate | 최소 조건 | 2fmax |
| Anti-[aliasing](/knowledge-base/studynote/03_network/01_data_communication/057_에일리어싱_Aliasing/) Filter | 사전 필터 | 고주파 제거 |

핵심은 충분히 빠르게 샘플링해야 원신호 정보가 겹치지 않는다는 점이다.

- **📢 섹션 요약 비유**: 표본화는 사진을 너무 천천히 찍으면 움직임이 이상하게 보이는 것과 같다.

---

## Ⅲ. 비교 및 연결

표본화는 양자화와 구분된다. 표본화는 시간축 이산화이고, 양자화는 진폭축 이산화다.

| 단계 | 무엇을 이산화하나 |
| :--- | :--- |
| Sampling | 시간 |
| [Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 진폭 |
| Encoding | 비트화 |

Nyquist 조건을 넘기지 못하면 aliasing으로 인해 저주파처럼 잘못 보이게 된다.

- **📢 섹션 요약 비유**: 표본화는 시간에 줄을 긋는 일, 양자화는 높이를 칸으로 나누는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 센서, 음성, 이미지 처리에서 샘플링 주파수와 필터를 맞춘다. 디지털 신호처리(DSP) 설계에서 기본이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 샘플링 주파수가 충분한가?
2. anti-[aliasing](/knowledge-base/studynote/03_network/01_data_communication/057_에일리어싱_Aliasing/) filter가 있는가?
3. 복원 조건을 만족하는가?
4. 시간축과 진폭축을 구분하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 너무 낮은 샘플링 주파수
- 필터 없이 직접 샘플링
- 표본화와 양자화를 혼동하는 경우

기술사 관점에서는 표본화가 디지털화의 첫 관문이며, Nyquist 조건이 핵심이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: 표본화는 도로를 너무 듬성듬성 촬영하면 중간 장면이 사라지는 것이다.

---

## Ⅴ. 기대효과 및 결론

표본화는 연속 세계를 디지털 세계로 옮기는 첫 단계다. 샘플링이 잘못되면 이후 모든 처리가 흔들린다.

정리하면, 충분히 빠르게, 그리고 미리 필터링하면서 샘플링해야 한다.

- **📢 섹션 요약 비유**: 표본화는 물건을 대표 샘플만 골라 기록하는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Sampling Rate | 주기 |
| Nyquist | 복원 조건 |
| Anti-[aliasing](/knowledge-base/studynote/03_network/01_data_communication/057_에일리어싱_Aliasing/) | 사전 필터 |
| [Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 다음 단계 |
| [PCM](/knowledge-base/studynote/03_network/19_frequent_topics_terms/943_pcm_pulse_code_modulation_sampling_quantization/) | 디지털화 |

### 📈 관련 키워드 및 발전 흐름도

```text
연속 신호
    │
    ▼
표본화
    │
    ▼
양자화
    │
    ▼
부호화 / 디지털 신호
```

이 흐름은 아날로그 신호가 디지털 신호로 바뀌는 기본 절차를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 표본화는 사진을 일정한 간격으로 찍는 거예요.
2. 너무 천천히 찍으면 움직임이 이상하게 보여요.
3. 그래서 충분히 빨리 찍어야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 56 / 1120

← **이전**: [55. 아날로그 연속파 변조 (AM/FM/PM)](/knowledge-base/studynote/03_network/01_data_communication/055_아날로그_연속파_변조_AM_FM_PM/)
**다음**: [57. 에일리어싱 (Aliasing) - 표본화 주파수 부족시 발생](/knowledge-base/studynote/03_network/01_data_communication/057_에일리어싱_Aliasing/) →

---
