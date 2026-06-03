+++
title = "53. 성상도 (Constellation Diagram)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 성상도 (Constellation Diagram)는 I/Q 평면에서 심볼 배치를 보여 주는 변조 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 도구다.
> 2. **가치**: 점 간 거리가 클수록 잡음에 강하고, 촘촘할수록 전송 효율은 높지만 오류 가능성도 커진다.
> 3. **판단 포인트**: [SNR](/knowledge-base/studynote/03_network/01_data_communication/024_신호_대_잡음비/) ([Signal-to-Noise Ratio](/knowledge-base/studynote/03_network/01_data_communication/024_신호_대_잡음비/)), [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) (Error Vector Magnitude), BER ([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Error Rate)을 함께 봐야 해석이 완성된다.

---

## Ⅰ. 개요 및 필요성

디지털 통신에서는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 전파에 실어 보내야 한다. 성상도는 어떤 심볼이 어떤 좌표에 배치되는지 보여 주어 변조 품질을 직관적으로 확인하게 해 준다.

현장에서 성상도는 변조기의 상태, 채널 품질, 위상 회전, 잡음, 심볼 확산을 판단하는 빠른 진단 수단이다.

- **📢 섹션 요약 비유**: 성상도는 좌표평면 위에 놓인 좌석 배치도와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

성상도는 I축과 Q축으로 구성된다. 각 점은 특정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 패턴을 의미하며, 복소수 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)의 진폭과 위상을 함께 나타낸다.

```text
           Q
           ↑
      •    |    •
           |
  •─────────┼─────────• → I
           |
      •    |    •
```

| 요소 | 의미 | 해석 포인트 |
| :--- | :--- | :--- |
| I축 | 동상 성분 | 좌우 위치 |
| Q축 | 직교 성분 | 상하 위치 |
| 점 간 거리 | 잡음 내성 | 멀수록 유리 |
| 점 퍼짐 | 채널 왜곡 | [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 증가 |

핵심 원리는 심볼이 이상적으로는 점 위에 있어야 하지만, 실제 채널에서는 잡음과 위상 오차로 점이 퍼진다는 것이다.

- **📢 섹션 요약 비유**: 성상도는 빗속에서도 어디에 서 있는지 보여 주는 지도다.

---

## Ⅲ. 비교 및 연결

성상도는 변조 차수를 비교할 때 특히 유용하다. BPSK, QPSK, 16-QAM, 64-QAM으로 갈수록 점이 많아지고 더 촘촘해진다.

| 변조 | 점 수 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| BPSK | 2 | 매우 강인함 | 효율 낮음 |
| QPSK | 4 | 균형적 | 중간 |
| 16-QAM | 16 | 효율 높음 | 잡음 민감 |
| 64-QAM | 64 | 효율 매우 높음 | 더 민감 |

성상도는 스펙트럼 효율과 신뢰성의 trade-off (상충관계)를 보여 준다. 고차 변조일수록 한 주파수에 더 많은 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 실을 수 있지만, 채널 품질이 나쁘면 오류가 증가한다.

- **📢 섹션 요약 비유**: 성상도는 같은 운동장에 더 많은 학생을 앉히는 것과 같다. 자리는 늘지만 서로 더 가까워진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 성상도로 변조기 이상, 위상 잡음, 증폭기 비선형성, 채널 페이딩을 본다. EVM이 커지면 심볼이 원래 위치에서 멀어졌다는 뜻이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 점이 기준 위치에서 얼마나 퍼졌는가?
2. 위상 회전이나 타원 왜곡이 있는가?
3. 변조 차수에 맞는 SNR이 확보되는가?
4. Gray coding이 적용되었는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 성상도만 보고 BER을 무시하는 경우
- 채널 변화 없이 고차 변조를 고집하는 경우
- [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 측정을 하지 않고 감으로 판단하는 경우

기술사 관점에서는 성상도가 단순 그림이 아니라 채널 품질과 변조 효율을 동시에 설명하는 증거라는 점이 중요하다.

- **📢 섹션 요약 비유**: 성상도는 물에 비친 별자리다. 물결이 흔들리면 별 모양도 흐트러진다.

---

## Ⅴ. 기대효과 및 결론

성상도는 디지털 변조 상태를 빠르게 진단하고, 고차 변조의 한계를 판단하게 해 준다. 통신 품질 분석의 기본 시각 도구다.

정리하면, 점 간 거리와 점의 퍼짐을 보면 전송 품질과 효율의 균형을 읽을 수 있다.

- **📢 섹션 요약 비유**: 성상도는 바둑판 위 돌 배치처럼 보이지만, 사실은 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 얼마나 잘 맞아 들어가는지 보여 주는 표이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| I/Q 평면 | [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 표현 |
| [EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) | 변조 오차 |
| [SNR](/knowledge-base/studynote/03_network/01_data_communication/024_신호_대_잡음비/) | 잡음 대비 |
| BER | 실제 오류 |
| QAM / [PSK](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/) | 변조 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
비트
    │
    ▼
심볼 매핑
    │
    ▼
I/Q 변조
    │
    ▼
성상도
    │
    ▼
EVM / SNR / BER 분석
```

이 흐름은 디지털 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 아날로그 파형으로 바뀌고, 다시 품질 지표로 읽히는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 성상도는 점심시간 자리 배치도예요.
2. 자리가 넓게 떨어져 있으면 친구랑 부딪히지 않아요.
3. 자리가 너무 빽빽하면 서로 헷갈리기 쉬워요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 53 / 1120

← **이전**: [52. 고차 QAM (16-QAM, 64-QAM, 256-QAM, 1024-QAM)](/knowledge-base/studynote/03_network/01_data_communication/052_고차_QAM_16_64_256_1024/)
**다음**: [54. 반송파 (Carrier Wave)](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) →

---
