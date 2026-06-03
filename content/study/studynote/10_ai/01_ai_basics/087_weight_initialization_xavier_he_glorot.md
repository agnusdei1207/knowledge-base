+++
weight = 87
title = "87. 가중치 초기화 (Weight Initialization) - Xavier와 He 초기화"
date = "2026-04-10"
[extra]
categories = "studynote-ai"
+++

## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: [[267_weight_bias_activation|가중치]] [[459_quic_fec_forward_error_correction|초기]]화는 [[130_signal|신호]]와 기울기의 [[136_variance|분산]]을 유지해 딥러닝 학습이 멈추거나 폭주하지 않게 하는 출발점이다.
    > 2. **가치**: Xavier (Glorot) [[459_quic_fec_forward_error_correction|초기]]화와 He [[459_quic_fec_forward_error_correction|초기]]화는 [[129_activation_function|활성화 함수]]에 맞춰 fan_in과 fan_out의 균형을 조절한다.
    > 3. **판단 포인트**: [[129_activation_function|활성화 함수]]와 [[459_quic_fec_forward_error_correction|초기]]화 [[268_strategy_pattern|전략]]을 무시하면 같은 네트워크라도 수렴 속도와 안정성이 크게 달라진다.

    ---

    ## Ⅰ. 개요 및 필요성

    [[267_weight_bias_activation|가중치]] [[459_quic_fec_forward_error_correction|초기]]화는 학습이 시작되는 순간의 분포를 정한다. 신경망이 너무 큰 값으로 시작하면 기울기 (Gradient)가 폭주하고, 너무 작은 값으로 시작하면 기울기가 사라져 학습이 느려진다.

Xavier (Glorot) [[459_quic_fec_forward_error_correction|초기]]화와 He [[459_quic_fec_forward_error_correction|초기]]화는 이런 문제를 줄이기 위해 설계되었다. 둘 다 층을 지날 때 활성값의 [[136_variance|분산]]이 급격히 무너지지 않도록 맞추며, [[129_activation_function|활성화 함수]]의 특성에 따라 다른 공식을 쓴다.

    - **📢 섹션 요약 비유**: 종이비행기를 처음 접을 때 접는 모양이 틀리면 끝까지 똑바로 날지 못하는 것과 같다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    핵심은 fan_in과 fan_out이다. fan_in은 들어오는 연결 수, fan_out은 나가는 연결 수이며, 이 값에 맞춰 [[459_quic_fec_forward_error_correction|초기]] [[136_variance|분산]]을 정하면 forward와 backward [[130_signal|신호]]가 균형을 유지하기 쉽다.

| 방법 | 분포 | 권장 활성화 | 핵심 효과 |
| :-- | :-- | :-- | :-- |
| Xavier/Glorot | `Var(W) = 2 / (fan_in + fan_out)` | [[070_hyperbolic_tangent_tanh_activation|tanh]], [[268_sigmoid_vanishing_gradient|sigmoid]], linear | 입력·출력 [[136_variance|분산]] 균형 |
| Xavier Uniform | `U[-√(6/(fan_in+fan_out)), +√(6/(fan_in+fan_out))]` | [[070_hyperbolic_tangent_tanh_activation|tanh]] 계열 | 범위 기반 안정화 |
| He | `Var(W) = 2 / fan_in` | [[269_relu_activation|ReLU]] ([[269_relu_activation|Rectified Linear Unit]]), Leaky [[269_relu_activation|ReLU]] | ReLU의 절반만 살아나는 특성 보정 |
| [[585_zero_skipping|Zero]] init | 모두 0 | 거의 없음 | 대칭성 때문에 실패 |

```text
입력 분포 ─► 초기 가중치 ─► 활성값 분산 유지 ─► 기울기 유지
                  │
                  ├─ 너무 작음 → 소실
                  └─ 너무 큼   → 폭주
```

Xavier는 입력과 출력의 평균적인 균형을 보고, He는 ReLU처럼 음수를 잘라내는 활성화에 맞춰 더 큰 [[136_variance|분산]]을 허용한다.

    - **📢 섹션 요약 비유**: 출발선에서 너무 약하게 뛰면 금방 멈추고, 너무 세게 뛰면 넘어진다. 딱 맞는 힘이 필요하다.

    ---

    ## Ⅲ. 비교 및 연결

    [[459_quic_fec_forward_error_correction|초기]]화는 [[129_activation_function|활성화 함수]]와 함께 봐야 한다. sigmoid와 tanh는 포화 영역이 있기 때문에 너무 큰 [[459_quic_fec_forward_error_correction|초기]]값을 주면 쉽게 막히고, ReLU는 음수 영역이 0이므로 더 큰 [[136_variance|분산]]이 필요하다.

| 비교 대상 | 장점 | 한계 |
| :-- | :-- | :-- |
| Xavier | [[070_hyperbolic_tangent_tanh_activation|tanh]]/linear에 균형적 | [[269_relu_activation|ReLU]] 깊은 네트워크에서는 약할 수 있음 |
| He | [[269_relu_activation|ReLU]] 계열에 적합 | sigmoid에는 과할 수 있음 |
| Orthogonal init | 정보 보존에 유리 | 구현과 튜닝이 더 까다로움 |
| [[282_batch_normalization|Batch Normalization]] (Batch Norm)와 병행 | 분포 안정화 강화 | [[459_quic_fec_forward_error_correction|초기]]화 자체의 중요성을 없애지는 못함 |

결국 [[459_quic_fec_forward_error_correction|초기]]화는 [[129_activation_function|활성화 함수]], [[093_normalization|정규화]], 깊이를 함께 설계해야 효과가 난다.

    - **📢 섹션 요약 비유**: tanh용 신발과 ReLU용 신발이 다르듯, 활성화마다 맞는 시작값이 있다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 다음 순서로 판단하면 된다. 먼저 [[129_activation_function|활성화 함수]]가 무엇인지 보고, 그다음 층 수와 [[093_normalization|정규화]] 유무를 [[396_validation|확인]]한다. [[269_relu_activation|ReLU]] 계열이 깊다면 He를 기본값으로 두고, tanh나 선형층 중심이면 Xavier를 먼저 검토한다.

### [[435_checklist_based_testing|체크리스트]]
1. [[129_activation_function|활성화 함수]]와 [[459_quic_fec_forward_error_correction|초기]]화 공식이 맞는가?
2. 학습 [[459_quic_fec_forward_error_correction|초기]]에 gradient histogram이 한쪽으로 무너지지 않는가?
3. Batch Norm이나 residual connection과 함께 동작하는가?
4. 재현성을 위해 seed를 고정했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 모든 층에 동일한 난수 범위를 무작정 적용하는 것
- hidden layer를 [[585_zero_skipping|zero]] init으로 두는 것
- [[269_relu_activation|ReLU]] 네트워크에 너무 작은 [[459_quic_fec_forward_error_correction|초기]]값을 쓰는 것

    - **📢 섹션 요약 비유**: 모든 블록을 같은 크기로 쌓으면 기울기가 막히니, 층의 역할에 맞게 출발점을 잡아야 한다.

    ---

    ## Ⅴ. 기대효과 및 결론

    좋은 [[459_quic_fec_forward_error_correction|초기]]화는 학습을 빠르게 만드는 것이 아니라, 학습이 시작될 수 있게 만든다. [[130_signal|신호]]가 유지되면 더 적은 에폭으로도 안정적으로 수렴하고, 디버깅과 재학습도 쉬워진다.

따라서 [[459_quic_fec_forward_error_correction|초기]]화는 하이퍼파라미터 중 부수적인 항목이 아니라, 최적화 지형을 설계하는 첫 번째 선택으로 기억해야 한다.

    - **📢 섹션 요약 비유**: 탑을 세울 때 첫 블록이 너무 작거나 크면 전체가 흔들리므로, 시작 크기가 중요하다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| fan_in / fan_out | [[459_quic_fec_forward_error_correction|초기]] [[136_variance|분산]] 계산의 기준 |
| Xavier (Glorot) | 균형형 [[459_quic_fec_forward_error_correction|초기]]화 |
| He | [[269_relu_activation|ReLU]] 계열 보정 [[459_quic_fec_forward_error_correction|초기]]화 |
| [[269_relu_activation|ReLU]] ([[269_relu_activation|Rectified Linear Unit]]) | 음수 절단 [[129_activation_function|활성화 함수]] |
| [[282_batch_normalization|Batch Normalization]] (Batch Norm) | 분포 안정화를 돕는 [[093_normalization|정규화]] |

    ### 📈 관련 키워드 및 발전 흐름도

    입력 분포 파악
    │
    ▼
fan_in / fan_out 계산
    │
    ▼
Xavier 또는 He 선택
    │
    ▼
기울기 유지 / 안정적 수렴

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 탑을 세울 때 첫 블록이 중요해요.
    2. 작게 시작하면 너무 약하고, 크게 시작하면 무너질 수 있어요.
    3. 그래서 신경망도 시작 크기를 잘 골라야 해요.
