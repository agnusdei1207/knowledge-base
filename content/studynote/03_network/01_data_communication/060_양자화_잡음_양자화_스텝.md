---
title: "060. Quantization Noise & Step Size"
date: "2024-05-15"
tags:
  - "studynote-network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 잡음은 연속 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 이산 레벨로 반올림하는 과정에서 생기는 오차다.
> 2. **가치**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 스텝을 줄이면 잡음이 줄고 품질은 좋아지지만, 저장과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 비용이 커진다.
> 3. **판단 포인트**: [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수, 선형/비선형 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/), [SNR](/studynote/03_network/01_data_communication/024_신호_대_잡음비/)([Signal-to-Noise Ratio](/studynote/03_network/01_data_communication/024_신호_대_잡음비/))을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

아날로그 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)는 무한히 부드럽지만, 디지털 시스템은 유한한 단계만 저장할 수 있다. 그래서 표본화된 값을 가장 가까운 계단으로 맞추는 과정이 필요하다.

그 계단의 간격이 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 스텝이고, 원래 값과 계단 값의 차이가 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 잡음이다. 이 차이는 오디오 왜곡과 통화 품질 저하의 직접 원인이 된다.

- **📢 섹션 요약 비유**: 부드러운 비탈길을 계단으로 바꿀 때 생기는 울퉁불퉁함이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 스텝은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수가 늘수록 작아진다. 스텝이 작아질수록 원 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 더 잘 따라가고, [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 잡음도 줄어든다.

```text
입력 신호
   v
표본화
   v
양자화(계단화)
   v
양자화 잡음 발생
```

| 항목 | 의미 |
| :-- | :-- |
| [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Depth | 계단 개수 `2^n` |
| Step Size(Δ) | 계단 간격 |
| SQNR | [신호 대 잡음비](/studynote/03_network/01_data_communication/024_신호_대_잡음비/) |
| Dithering | 잡음 패턴을 무작위화하는 기법 |

이론적으로 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수가 1 증가하면 SQNR은 약 6dB 좋아진다. 즉, 해상도를 올리면 품질은 좋아지지만 데이터는 커진다.

- **📢 섹션 요약 비유**: 계단을 촘촘히 쌓으면 발이 편하지만, 재료가 더 많이 든다.

---

## Ⅲ. 비교 및 연결

| 구분 | 선형 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 비선형 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) |
| :-- | :-- | :-- |
| 계단 폭 | 일정 | 구간별 가변 |
| 장점 | 단순 | 작은 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)에 유리 |
| 대표 | 일반 ADC | μ-law, A-law |
| 적합한 곳 | 고품질 오디오 | 전화 음성 통신 |

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 잡음은 열잡음과 달리 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 처리 과정에서 만들어진다. 그래서 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수와 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 방식만 잘 선택해도 줄일 수 있다.

- **📢 섹션 요약 비유**: 똑같이 시끄러워 보여도, 어떤 소리는 공사장 소음이고 어떤 소리는 계단 밟는 소리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

VoIP, 센서, 오디오 인코딩에서는 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수와 스텝 크기 선택이 품질과 비용을 동시에 결정한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 작은 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 영역이 중요한가?
2. [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 저장 비용이 제한적인가?
3. 선형보다 비선형 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)가 더 적절한가?
4. 필요하면 디더링이나 컴팬딩을 적용했는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 너무 적은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수로 SNR을 망치는 설계
- [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 특성을 무시하고 선형만 쓰는 설계
- 삭제/복원이 아닌 원본 그대로를 기대하는 설계

- **📢 섹션 요약 비유**: 옷 사이즈가 너무 거칠면 맞지 않고, 너무 세분화하면 옷장만 커지는 문제다.

---

## Ⅴ. 기대효과 및 결론

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 잡음은 디지털화의 대가다. 하지만 스텝과 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수를 조절하면 품질과 비용의 균형을 맞출 수 있다.

결국 핵심은 "오차를 없애는 것"이 아니라 "오차를 감당 가능한 수준으로 줄이는 것"이다.

- **📢 섹션 요약 비유**: 사진을 모자이크로 바꿀 때, 타일을 너무 크게 하면 얼굴이 깨지는 것과 같다.

---

## 관련 개념 맵

```text
표본화
   v
양자화 스텝
   v
양자화 잡음
   v
SNR / 음질
```

---

## 관련 키워드 및 발전 흐름도

```text
아날로그 신호
   v
표본화
   v
양자화
   v
비트 수 / 스텝 최적화
   v
압축 통신 품질 향상
```

---

## 어린이를 위한 3줄 비유 설명

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 부드러운 길을 계단으로 바꾸는 일이에요.
계단이 촘촘할수록 덜 흔들리지만 더 많은 재료가 필요해요.
그래서 적당한 계단 크기를 찾는 게 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 60 / 1120

<- **이전**: [59. 양자화 (Quantization) - 선형/비선형](/studynote/03_network/01_data_communication/059_양자화_Quantization/)
**다음**: [61. 컴팬딩 (Companding) / 압신 - μ-law, A-law](/studynote/03_network/01_data_communication/061_컴팬딩_압신_mu_law_A_law/) ->

---
