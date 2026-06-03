+++
title = "59. 양자화 (Quantization) - 선형/비선형"
date = 2026-03-30

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))는 아날로그 진폭을 컴퓨터가 다룰 수 있는 유한한 정수 단계로 반올림하는 과정이다.
> 2. **가치**: [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Depth)와 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 방식에 따라 저장 용량, 음질, 잡음 특성이 동시에 달라진다.
> 3. **판단 포인트**: 선형 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)와 비선형 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Companding](/knowledge-base/studynote/03_network/01_data_communication/061_컴팬딩_압신_mu_law_A_law/), 압신)를 언제 쓰는지 구분해야 통신 품질을 지킬 수 있다.

---

## Ⅰ. 개요 및 필요성

[표본화](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/)([Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/))가 시간축을 잘라낸다면, [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 높이축을 잘라낸다. 즉, 연속적인 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 값을 계단처럼 끊어서 디지털 숫자로 바꾸는 단계다.

메모리와 전송 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)은 유한하므로 무한한 소수점을 그대로 저장할 수 없다. 결국 아날로그 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)는 가장 가까운 단계로 끼워 맞춰져야 하고, 그 차이는 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 오차로 남는다.

- **📢 섹션 요약 비유**: 키를 재서 옷 사이즈를 고르는 일처럼, 실제 값은 연속적이지만 선택지는 몇 개의 규격뿐이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)의 가장 기본은 선형 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)다. 전체 진폭 범위를 같은 크기의 계단으로 나누고, 들어온 값이 가장 가까운 계단으로 올라가거나 내려간다.

```text
전압
 4.0 ┤               ● 3.8V → 4.0V
 3.0 ┤        ● 2.8V → 3.0V
 2.0 ┤  ● 2.2V → 2.0V
 1.0 ┤
 0.0 └────────────────────────
       00      01      10     11
```

| 항목 | 의미 |
| :-- | :-- |
| [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수([Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Depth) | 계단 개수 `L = 2^n` |
| 스텝 크기(Step Size) | 계단 간격 `Δ = (Vmax - Vmin) / L` |
| [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 오차 | 원래 값과 반올림된 값의 차이 |
| [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 노이즈 | 오차가 누적되어 들리는 잡음 |

비선형 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 소리의 크기별로 계단 폭을 다르게 잡는다. 작은 소리 구간은 촘촘하게, 큰 소리 구간은 넓게 나눠서 같은 8비트로도 더 좋은 체감 품질을 얻는다.

- **📢 섹션 요약 비유**: 작은 글씨는 돋보기를 쓰고, 큰 글씨는 멀리서 보는 것처럼 구간마다 확대율을 다르게 주는 방식이다.

---

## Ⅲ. 비교 및 연결

[양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 선형과 비선형의 차이만 보는 것이 아니라, [표본화](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/)와 부호화 사이에서 어떤 역할을 하는지도 함께 봐야 한다.

| 구분 | 선형 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 비선형 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) |
| :-- | :-- | :-- |
| 계단 폭 | 일정 | 구간별 가변 |
| 장점 | 단순, 예측 가능 | 음성 대역에서 효율적 |
| 단점 | 작은 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 해상도 불리 | 구현과 표준 선택이 필요 |
| 대표 표준 | 일반 ADC(Analog-to-Digital Converter) | μ-law, A-law |

통신망에서는 `G.711 μ-law`와 `G.711 A-law`가 대표적이다. 둘은 같은 8비트를 쓰더라도 계단 분포가 달라서, 잘못 맞추면 복원 음질이 깨진다.

- **📢 섹션 요약 비유**: 같은 크기 상자에 물건을 넣더라도, 안쪽 칸막이를 어떻게 나누느냐에 따라 담기는 모양이 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수만 늘리는 것이 답이 아니다. [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 특성에 맞는 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 방식과 코덱을 골라야 저장 공간과 품질을 같이 맞출 수 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 음성처럼 작은 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 구간이 중요한가?
2. 저장 용량과 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 제한적인가?
3. 송수신 양쪽의 μ-law / A-law 설정이 같은가?

### 실무 시나리오

- 콜센터 녹취 서버: 8비트와 16비트의 저장량 차이 검토
- VoIP(Voice over IP): 코덱 불일치로 인한 음성 왜곡 점검
- 센서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/): [SNR](/knowledge-base/studynote/03_network/01_data_communication/024_신호_대_잡음비/)([신호 대 잡음비](/knowledge-base/studynote/03_network/01_data_communication/024_신호_대_잡음비/))와 동적 범위(Dynamic Range) 확보

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수만 높이고 저장·[대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 예산을 무시하는 설계
- 송신기와 수신기의 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 규칙이 다른데도 통합 테스트를 생략하는 설계

- **📢 섹션 요약 비유**: 숫자판을 촘촘하게 만들수록 정확하긴 하지만, 그만큼 옮기고 저장하는 비용도 커진다.

---

## Ⅴ. 기대효과 및 결론

[양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 연속 세계를 디지털 세계로 넘기는 관문이다. 오차는 피할 수 없지만, 그 오차를 관리해야 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 저장, 전송, 복원이 가능해진다.

좋은 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 설계는 적정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수, 적절한 계단 분포, 표준 코덱 선택을 함께 만족한다. 결국 이 개념은 "얼마나 잘게 자를 것인가"와 "그 비용을 감당할 수 있는가"의 문제다.

- **📢 섹션 요약 비유**: 모자이크 타일이 촘촘할수록 그림은 선명하지만, 타일 상자를 옮기는 일은 더 힘들어진다.

---

## 관련 개념 맵

```text
표본화(Sampling)
   ↓
양자화(Quantization)
   ↓
부호화(Encoding)
   ↓
PCM / 코덱 / 전송
```

---

## 관련 키워드 및 발전 흐름도

```text
아날로그 연속파
   ↓
표본화
   ↓
선형 양자화
   ↓
비선형 양자화(μ-law / A-law)
   ↓
PCM 기반 음성 통신
```

---

## 어린이를 위한 3줄 비유 설명

[양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 끝이 없는 소수점을 딱 떨어지는 숫자 칸으로 바꾸는 일이에요.  
칸을 촘촘히 나누면 더 정확하지만, 그만큼 저장하기도 더 어려워져요.  
그래서 컴퓨터는 상황에 맞게 칸 크기를 골라요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 59 / 1120

← **이전**: [58. 폴딩 주파수 (Folding Frequency)](/knowledge-base/studynote/03_network/01_data_communication/058_폴딩_주파수_Folding_Frequency/)
**다음**: [60. 양자화 잡음 (Quantization Noise/Error), 양자화 스텝](/knowledge-base/studynote/03_network/01_data_communication/060_양자화_잡음_양자화_스텝/) →

---
