+++
weight = 428
title = "428. MAC 연산 (Multiply-Accumulate)"
date = "2026-03-20"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[673_mac_message_authentication_code|MAC]] (Multiply-Accumulate) 연산은 `A × B + C`를 한 흐름으로 처리해, 행렬 곱과 내적에서 반복되는 핵심 계산을 하드웨어 친화적으로 압축한 연산 단위다.
> 2. **가치**: [[231_ai_turing_test|인공지능]]과 디지털 [[130_signal|신호]] 처리에서는 계산 자체보다 중간 결과를 옮기는 비용이 더 크기 쉬운데, MAC은 곱셈과 누산을 결합해 [[139_throughput|처리량]]과 전력 효율을 함께 높인다.
> 3. **판단 포인트**: 좋은 [[673_mac_message_authentication_code|MAC]] 설계는 단순히 유닛 개수를 늘리는 것이 아니라, [[233_precision_recall_f1_roc_auc_threshold|정밀도]], [[161_accumulator|누산기]] 폭, 메모리 공급 속도, [[001_dikw_pyramid|데이터]] 재사용 구조까지 함께 맞출 때 비로소 효과가 난다.

---

## Ⅰ. 개요 및 필요성

[[673_mac_message_authentication_code|MAC]] (Multiply-Accumulate) 연산은 두 값을 곱한 뒤 그 결과를 누산값에 더하는 연산이다. 수식으로는 `Y = Y + (A × B)` 또는 `Σ(xᵢ × wᵢ)` 형태로 나타나며, 필터링, 벡터 내적, 행렬 곱, [[089_CNN_Convolutional|합성곱 신경망]] ([[089_CNN_Convolutional|Convolutional Neural Network]], [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]) 계산의 가장 작은 반복 단위가 된다.

이 연산이 중요해진 이유는 같은 패턴이 너무 자주 반복되기 때문이다. 예를 들어 음성 필터는 샘플과 계수를 계속 곱해 누적하고, 인공신경망은 입력값과 가중치를 계속 곱해 편향까지 누적한다. 이때 곱셈 명령과 덧셈 명령을 따로 처리하면 [[158_instruction|명령어]] 인출, 중간 저장, [[057_register|레지스터]] 이동이 반복되어 실제 계산보다 [[001_dikw_pyramid|데이터]] 이동 비용이 더 커진다.

특히 [[190_ai_llm_requirements_specification|AI]] ([[001_artificial_intelligence|Artificial Intelligence]]) 가속기에서는 수십억 번의 곱셈-누산이 한 번의 추론 안에 몰려 있다. 따라서 MAC은 "복잡한 알고리즘을 위한 보조 연산"이 아니라, 하드웨어가 가장 자주 수행해야 하는 일을 가장 짧은 경로로 재구성한 기본 설계 원리라고 보는 편이 맞다.

이 그림은 왜 MAC이 별도 회로로 분리되었는지 보여준다. 핵심은 계산식이 아니라 **중간 결과를 어디서 끊느냐**다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                분리 실행과 MAC 실행의 차이: 중간 저장의 유무              │
├───────────────────────────────┬────────────────────────────────────────────┤
│ 분리된 MUL + ADD              │ MAC                                         │
│                               │                                             │
│ A, B ─▶ [Multiplier]          │ A, B ─▶ [Multiplier]                        │
│              │                │              │                              │
│              ▼                │              ▼                              │
│        [Temp Register]        │         [Adder] ◀── Accumulator            │
│              │                │              │                              │
│              ▼                │              ▼                              │
│ Temp, C ─▶ [Adder] ─▶ Result  │        Updated Sum                          │
│                               │                                             │
│ 추가 저장/읽기 발생           │ 곱셈 결과가 바로 누산 경로로 연결됨         │
└───────────────────────────────┴────────────────────────────────────────────┘
```

분리 실행은 제어가 단순하지만, 누적 계산이 길어질수록 임시값 저장과 읽기 비용이 커진다. 반면 MAC은 연산 경로를 짧게 만들어 동일한 수학식을 더 적은 제어 오버헤드와 더 낮은 에너지로 수행한다.

- **📢 섹션 요약 비유**: MAC은 계산을 두 번 접수하는 창구가 아니라, 곱하기와 더하기를 한 줄로 이어 붙인 전용 계산 레인이다. 손님이 많을수록 창구를 오가게 하는 방식보다 한 번에 처리하는 레인이 훨씬 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[673_mac_message_authentication_code|MAC]] 유닛의 내부는 보통 곱셈기 (Multiplier), [[161_accumulator|누산기]] ([[161_accumulator|Accumulator]]), 가산기 (Adder), 파이프라인 [[057_register|레지스터]]로 구성된다. 입력 [[001_dikw_pyramid|데이터]]와 가중치가 들어오면 먼저 곱셈이 수행되고, 그 결과가 기존 누산값과 더해져 부분합 (Partial Sum)을 만든다. 이 부분합은 다음 사이클의 입력이 되어 긴 내적을 한 줄로 이어 간다.

핵심은 단순히 `곱한다 → 더한다`가 아니라, **누산 폭과 [[001_dikw_pyramid|데이터]] 흐름을 어떻게 잡느냐**다. 예를 들어 8비트 정수 (INT8) 두 개를 곱하면 결과는 16비트까지 커질 수 있고, 이것을 수백 번 더하면 [[161_accumulator|누산기]]는 더 넓은 [[073_bit|비트]] 폭을 가져야 오버플로를 피할 수 있다. 그래서 저정밀 입력을 사용하더라도 [[161_accumulator|누산기]]는 32비트 이상으로 유지하는 설계가 흔하다.

| 구성 요소 | 역할 | 설계 시 주의점 |
| :-- | :-- | :-- |
| 곱셈기 (Multiplier) | 입력값과 가중치의 곱 계산 | [[073_bit|비트]] 폭이 넓어질수록 면적과 [[015_지연_데이터_관점|지연]] 증가 |
| 가산기 (Adder) | 곱 결과와 누산값 결합 | 캐리 전파 [[015_지연_데이터_관점|지연]]과 파이프라인 균형 |
| [[161_accumulator|누산기]] ([[161_accumulator|Accumulator]]) | 부분합 저장 | 오버플로 방지용 충분한 폭 필요 |
| 파이프라인 [[057_register|레지스터]] | 높은 클럭 유지를 위한 단계 분리 | [[015_지연_데이터_관점|지연]]은 줄지만 [[459_quic_fec_forward_error_correction|초기]] 레이턴시는 증가 |

이 그림은 MAC이 한 번의 계산기가 아니라, 반복되는 내적을 흘려보내는 누산 파이프라인이라는 점을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                  MAC 파이프라인: 내적이 만들어지는 흐름                   │
├────────────────────────────────────────────────────────────────────────────┤
│ x0, w0 ─▶ [×] ─▶ (+) ─▶ s0                                                │
│                     ▲                                                      │
│                     │                                                      │
│                초기값 0                                                    │
│                                                                            │
│ x1, w1 ─▶ [×] ─▶ (+) ─▶ s1                                                │
│                     ▲                                                      │
│                     │                                                      │
│                     s0                                                     │
│                                                                            │
│ x2, w2 ─▶ [×] ─▶ (+) ─▶ s2  ...  최종 출력 = Σ(xᵢ × wᵢ) + bias            │
│                     ▲                                                      │
│                     │                                                      │
│                     s1                                                     │
└────────────────────────────────────────────────────────────────────────────┘
```

이 구조가 중요한 이유는 한 번 계산한 부분합을 버리지 않고 다음 연산으로 즉시 연결하기 때문이다. 그래서 [[673_mac_message_authentication_code|MAC]] [[055_array|배열]]이 충분히 채워져 있을 때는 사이클마다 새 결과를 내보낼 수 있고, 이것이 [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]])의 [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]])나 [[424_npu|NPU]] ([[424_npu|Neural Processing Unit]])의 [[426_systolic_array|시스톨릭 어레이]] ([[426_systolic_array|Systolic Array]])로 확장된다.

또 하나의 핵심은 FMA (Fused Multiply-Add)다. FMA는 곱셈 결과를 중간에서 반올림하지 않고 덧셈까지 묶어 마지막에 한 번만 반올림함으로써, 분리된 연산보다 수치 오차를 줄인다. 즉 MAC은 [[139_throughput|처리량]] 관점의 핵심이고, FMA는 그 MAC을 [[087_floating_point|부동소수점]] 정확도 측면에서 더 정교하게 만든 형태라고 이해하면 좋다.

- **📢 섹션 요약 비유**: MAC은 작은 계산기 여러 개가 아니라, 이전 합계를 계속 들고 달리는 이어달리기 주자와 같다. 바통을 바닥에 내려놓지 않고 바로 다음 주자에게 넘겨야 속도와 정확도가 함께 유지된다.

---

## Ⅲ. 비교 및 연결

MAC의 경계는 일반적인 곱셈·덧셈 조합, FMA, 그리고 대규모 행렬 가속 구조와 비교할 때 가장 선명해진다. 같은 수학식을 계산해도 어디에서 끊고, 얼마나 넓게 저장하고, 얼마나 많이 [[430_index_fast_full_scan|병렬]]화하느냐에 따라 [[282_performance_tactics|성능]]과 활용처가 달라진다.

| 구분 | 특징 | 강점 | 한계 |
| :-- | :-- | :-- | :-- |
| 분리된 MUL + ADD | [[158_instruction|명령어]]와 [[001_dikw_pyramid|데이터]] 경로가 분리됨 | 범용성 높음 | 중간 저장과 제어 오버헤드 큼 |
| [[673_mac_message_authentication_code|MAC]] | 곱셈과 누산을 한 [[001_dikw_pyramid|데이터]] 경로로 결합 | 반복 계산에 효율적 | 메모리 공급이 느리면 유닛이 놀게 됨 |
| FMA | 곱셈과 덧셈을 융합해 한 번만 반올림 | [[087_floating_point|부동소수점]] 정확도 우수 | 구현 복잡도와 회로 비용 증가 |
| [[426_systolic_array|시스톨릭 어레이]] | MAC을 2차원 격자로 배치 | 대규모 행렬 연산에 최적 | 불규칙·희소 연산에는 비효율 가능 |

CPU (Central Processing Unit)는 제어 분기와 범용 처리에 강하므로 소수의 벡터 [[673_mac_message_authentication_code|MAC]]/FMA 유닛을 정교하게 활용한다. 반면 GPU는 같은 연산을 대량으로 반복하는 구조에 유리해 많은 [[673_mac_message_authentication_code|MAC]] 유닛을 [[430_index_fast_full_scan|병렬]]로 배치한다. [[425_tpu|TPU]] ([[425_tpu|Tensor Processing Unit]])나 NPU는 여기서 더 나아가 제어 유연성을 줄이고, [[673_mac_message_authentication_code|MAC]] [[055_array|배열]]의 밀도와 [[001_dikw_pyramid|데이터]] 재사용 경로를 극단적으로 최적화한다.

이 비교가 중요한 이유는 [[282_performance_tactics|성능]] 병목의 위치가 달라지기 때문이다. CPU에서는 제어와 캐시 효율이 핵심일 수 있지만, [[190_ai_llm_requirements_specification|AI]] 가속기에서는 [[673_mac_message_authentication_code|MAC]] 자체보다 메모리 대역폭과 온칩 재사용 구조가 더 큰 병목이 된다. 그래서 "MAC이 많다"는 말만으로는 충분하지 않고, 그 MAC에 [[001_dikw_pyramid|데이터]]를 끊김 없이 공급할 수 있는지가 더 중요하다.

또한 [[434_quantization|양자화]] ([[434_quantization|Quantization]])는 MAC과 직접 연결된다. 32비트 [[087_floating_point|부동소수점]] (FP32) 대신 16비트 [[087_floating_point|부동소수점]] (FP16)이나 8비트 정수 (INT8)를 쓰면 같은 면적에 더 많은 MAC을 넣을 수 있어 [[139_throughput|처리량]]과 전력 효율이 좋아진다. 대신 누산 폭, [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 손실, 재학습 필요 여부를 함께 판단해야 한다.

- **📢 섹션 요약 비유**: 같은 주방이라도 일반 식당은 다양한 요리를 조금씩 잘하고, 패스트푸드 매장은 햄버거 조립 라인을 극도로 최적화한다. [[673_mac_message_authentication_code|MAC]] 기반 가속기는 "햄버거를 가장 빨리 많이 만드는 구조"에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 MAC은 단순 연산 개념이 아니라, 모델과 하드웨어의 궁합을 판단하는 기준이 된다. 예를 들어 추론 칩의 [[282_performance_tactics|성능]]이 40 TOPS (Tera Operations Per Second)라고 해도, 실제 모델이 요구하는 [[001_dikw_pyramid|데이터]] 형식과 메모리 이동량이 맞지 않으면 광고 수치만큼의 [[139_throughput|처리량]]이 나오지 않는다. 일반적으로 1 MAC을 곱셈 1회와 덧셈 1회로 세어 2 OPS로 환산하므로, TOPS 해석도 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 기준과 함께 봐야 한다.

### 실무 체크포인트

1. **[[233_precision_recall_f1_roc_auc_threshold|정밀도]] 선택이 먼저다**: 정확도 요구가 높지 않은 추론은 INT8 또는 FP16으로 낮춰 더 많은 [[673_mac_message_authentication_code|MAC]] [[430_index_fast_full_scan|병렬]]성을 확보할 수 있다.
2. **[[161_accumulator|누산기]] 폭을 분리해서 본다**: 입력을 저정밀도로 줄여도 [[161_accumulator|누산기]]까지 너무 좁히면 합산 과정에서 정보가 무너진다.
3. **메모리 재사용 구조를 확인한다**: 같은 가중치와 입력 타일을 반복 재사용하지 못하면 [[673_mac_message_authentication_code|MAC]] 유닛은 계산보다 대기 시간이 길어진다.
4. **희소성 활용 여부를 본다**: 값의 대부분이 0인 희소 행렬은 조밀 행렬용 [[673_mac_message_authentication_code|MAC]] [[055_array|배열]]에서 기대만큼 빠르지 않을 수 있다.

### 채택 판단 예시

- **채택이 유리한 경우**: [[228_cnn_1d_2d_3d_video_medical|합성곱]], 행렬 곱, 내적처럼 동일한 계산 패턴이 대량 반복되는 워크로드
- **주의가 필요한 경우**: 제어 분기, 불규칙 메모리 접근, 작은 배치 크기처럼 [[673_mac_message_authentication_code|MAC]] [[055_array|배열]] 활용률이 낮은 워크로드
- **회피를 검토할 경우**: 계산량보다 [[001_dikw_pyramid|데이터]] 이동과 분기 비용이 큰 작업을 억지로 대형 가속기에 올리는 경우

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모델 파라미터 수만 보고 연산량을 판단하는 것
- 입력 [[073_bit|비트]] 폭만 줄이고 누산 오차를 검증하지 않는 것
- 하드웨어 스펙의 TOPS 수치만 보고 메모리 병목을 무시하는 것

기술사 관점에서는 "[[673_mac_message_authentication_code|MAC]] 수가 많다"보다 "[[001_dikw_pyramid|데이터]] 공급, [[233_precision_recall_f1_roc_auc_threshold|정밀도]], 활용률이 균형 잡혔는가"를 답해야 설계 판단이 된다. 결국 좋은 가속기는 큰 엔진이 아니라, 연료와 공기 공급까지 맞춘 엔진이다.

- **📢 섹션 요약 비유**: [[673_mac_message_authentication_code|MAC]] 유닛을 많이 싣는 것은 버스를 늘리는 일에 가깝고, 실제 [[282_performance_tactics|성능]]은 승객을 제때 태워 보내는 배차 시스템이 좌우한다. 버스만 많고 정류장 운영이 엉키면 도로에 빈차만 늘어난다.

---

## Ⅴ. 기대효과 및 결론

[[673_mac_message_authentication_code|MAC]] 중심 설계의 가장 큰 효과는 반복 계산을 하드웨어의 자연스러운 흐름으로 바꾼다는 점이다. 내적과 행렬 곱처럼 현대 컴퓨팅의 중심이 되는 작업을 짧은 [[001_dikw_pyramid|데이터]] 경로와 높은 [[430_index_fast_full_scan|병렬]]성으로 처리할 수 있어, [[139_throughput|처리량]]과 전성비가 동시에 좋아진다. 그래서 DSP (Digital [[130_signal|Signal]] Processor), [[418_gpu|GPU]], [[425_tpu|TPU]], [[424_npu|NPU]] 모두 각기 다른 방식으로 [[673_mac_message_authentication_code|MAC]] 밀도를 높여 왔다.

다만 효과는 전제가 있을 때만 성립한다. 첫째, [[001_dikw_pyramid|데이터]] 재사용 구조가 있어야 메모리 병목이 줄어든다. 둘째, [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 축소로 확보한 [[430_index_fast_full_scan|병렬]]성이 실제 정확도 저하를 감당할 수 있어야 한다. 셋째, [[055_array|배열]] 활용률이 높아야 많은 MAC이 실제 [[282_performance_tactics|성능]]으로 환산된다. 이 조건이 무너지면 많은 MAC은 유휴 회로와 발열로 돌아온다.

앞으로의 방향은 세 가지로 요약된다. 첫째, 저정밀·혼합정밀도 누산의 고도화, 둘째, 희소성 인지형 [[673_mac_message_authentication_code|MAC]] 스케줄링, 셋째, 메모리 근처에서 연산하는 [[430_pim|Processing-in-Memory]] 계열 확장이다. 따라서 MAC은 "곱하고 더하는 작은 연산"이 아니라, 현대 가속기 설계가 [[282_performance_tactics|성능]]과 전력을 조율하는 중심 축으로 기억해야 한다.

- **📢 섹션 요약 비유**: MAC은 공장의 핵심 프레스 기계다. 좋은 공장은 프레스만 크게 만들지 않고, 자재 투입, 중간 운반, 불량 관리까지 함께 설계해서 전체 생산성을 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 내적 ([[519_dot_dns_over_tls|Dot]] Product) | MAC이 가장 직접적으로 반복되는 대표 계산 형태 |
| FMA (Fused Multiply-Add) | MAC을 [[087_floating_point|부동소수점]] 정확도 측면에서 고도화한 형태 |
| [[426_systolic_array|시스톨릭 어레이]] ([[426_systolic_array|Systolic Array]]) | 다수의 [[673_mac_message_authentication_code|MAC]] 유닛을 규칙적으로 연결해 행렬 연산을 가속하는 구조 |
| [[434_quantization|양자화]] ([[434_quantization|Quantization]]) | 같은 면적과 전력 안에서 더 많은 [[673_mac_message_authentication_code|MAC]] [[430_index_fast_full_scan|병렬]]성을 확보하게 하는 방법 |
| [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]]) | [[418_gpu|GPU]] 내부에서 행렬 [[673_mac_message_authentication_code|MAC]] 연산을 높은 밀도로 처리하는 전용 블록 |

### 📈 관련 키워드 및 발전 흐름도

```text
곱셈기 + 가산기 분리
        │
        ▼
MAC (Multiply-Accumulate) 기본 누산 구조
        │
        ▼
FMA (Fused Multiply-Add)로 정확도 개선
        │
        ▼
SIMD (Single Instruction, Multiple Data) · 벡터 MAC 확장
        │
        ▼
시스톨릭 어레이 · 텐서 코어 · NPU 대규모 병렬화
        │
        ▼
저정밀 양자화 · 희소성 최적화 · 메모리 근접 연산
```

이 흐름은 "연산 결합 → 정확도 개선 → [[430_index_fast_full_scan|병렬]] 확장 → [[001_dikw_pyramid|데이터]] 이동 최적화"로 [[673_mac_message_authentication_code|MAC]] 개념이 성장해 온 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MAC은 숫자 두 개를 곱한 다음, 그 답을 바로 저금통에 넣어 계속 모으는 계산 기계예요.
2. 이렇게 하면 매번 종이에 적었다가 다시 읽지 않아도 돼서 더 빨리 계산할 수 있어요.
3. [[231_ai_turing_test|인공지능]] 칩은 이런 저금통 계산기를 아주 많이 모아 놓고, 모두가 동시에 일하게 만든 거예요.
