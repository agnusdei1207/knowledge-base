---
title: "Quantization"
date: "2026-04-17"
tags:
  - "studynote-ai"
weight: 158
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))는 모델의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)와 활성화 값을 더 적은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수로 표현해, 같은 모델을 더 작은 메모리와 더 빠른 정수 연산 위에서 돌리게 만드는 추론 최적화 기술이다.
> 2. **가치**: 32비트 [부동소수점](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/)(FP32, 32-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) [Floating Point](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/))을 16비트 [부동소수점](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/)(FP16, 16-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) [Floating Point](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/)), 8비트 정수(INT8, 8-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Integer), 4비트 정수(INT4, 4-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Integer)처럼 더 낮은 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)로 바꾸면 모델 크기, 메모리 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)이 함께 줄어들어 온디바이스 AI와 대규모 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 비용 절감이 가능해진다.
> 3. **판단 포인트**: [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 줄일수록 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 오차가 커지므로, 정확도 손실 허용치·하드웨어 지원 수준·보정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 확보 여부를 보고 사후 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)(PTQ, Post-[Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))와 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 인지 학습(QAT, [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)-Aware [Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) 중 적절한 방식을 골라야 한다.

---

## Ⅰ. 개요 및 필요성

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))는 신경망이 쓰는 실수값을 더 적은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수의 정수 또는 저정밀 형식으로 바꾸는 모델 경량화 기법이다. 대형 모델은 파라미터 수가 수십억 개를 넘기 때문에, 정확도만 보고 FP32를 유지하면 메모리 용량과 메모리 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이 먼저 한계에 도달한다. 이때 병목은 계산기 자체보다 "[가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 얼마나 빨리 읽어 올 수 있는가"에서 자주 발생한다.

예를 들어 70억 개 파라미터 모델을 FP32로 저장하면 약 28GB가 필요하지만, INT8이면 약 7GB 수준까지 내려간다. 같은 그래픽 처리 장치([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))나 모바일 [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/))에서도 더 큰 모델을 올릴 수 있고, 캐시 [적중률](/studynote/01_computer_architecture/06_memory_hierarchy_cache/264_hit_ratio/)과 배치 효율도 좋아진다. [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)가 중요한 이유는 단순 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)이 아니라, 실제 배포 가능 하드웨어 범위를 넓히는 "실행 가능성 확보 기술"이기 때문이다.

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)가 없다면 엣지 디바이스는 물론 서버 환경에서도 추론 비용이 빠르게 증가한다. 특히 대화형 [대규모 언어 모델](/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/)([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), [Large Language Model](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 동시 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 곧 사용자 경험과 비용으로 연결되므로, 모델 품질을 조금만 희생하고도 인프라 효율을 크게 올릴 수 있는 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)가 실무에서 강한 선택지가 된다.

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 여행 가방을 싸며 두꺼운 겨울옷을 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)팩에 넣는 일과 같다. 옷의 형태는 약간 구겨지지만, 같은 가방에 더 많은 짐을 담고 이동도 훨씬 수월해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)의 핵심은 연속적인 실수 범위를 제한된 정수 구간에 대응시키는 것이다. 보통 스케일 (Scale)과 영점 ([Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-point)을 계산해 실수값을 정수값으로 사상하고, 연산 후 필요하면 다시 근사 복원한다. 이때 중요한 것은 "모든 값을 똑같이 자르는가"가 아니라, 레이어별 분포와 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))를 얼마나 잘 반영하느냐다.

아래 그림은 추론 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)가 어디에 개입하는지 보여준다.

```text
+--------------------------------------------------------------------+
|        양자화 추론 파이프라인: 저장 비용과 메모리 이동량을 줄임     |
+--------------------------------------------------------------------+
| FP32 학습 완료 모델                                                |
|      |                                                             |
|      +--> 보정(Calibration) 데이터로 값의 범위 측정                 |
|      |        |                                                    |
|      |        +--> Scale / Zero-point 결정                          |
|      |                                                             |
|      +--> 가중치·활성화 양자화                                      |
|                 |                                                   |
|                 +--> INT8 / INT4 저장                               |
|                 +--> 정수 커널로 행렬 연산                          |
|                 +--> 필요 시 역양자화(Dequantization) 후 출력        |
|                                                                    |
| 병목 변화: [메모리 읽기] 중심  ------>  [저정밀 정수 연산] 중심       |
+--------------------------------------------------------------------+
```

이 구조에서 가장 흔한 수식은 다음과 같다.

- [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/): `q = round(x / scale) + zero_point`
- 역양자화: `x' = (q - zero_point) × scale`

여기서 `x'`는 원본 `x`와 완전히 같지 않다. 이 차이가 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 오차 ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) Error)이며, [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수를 줄일수록 계단 간격이 커져 오차도 커진다. 그래서 실무에서는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)만 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)하는지, 활성화까지 함께 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)하는지, 레이어 전체를 한 스케일로 묶는지(Per-Tensor), 채널별로 세밀하게 나누는지(Per-Channel)를 함께 설계한다.

| 설계 축 | 선택지 | 특징 | 실무 의미 |
| :--- | :--- | :--- | :--- |
| 대상 | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 구현이 단순함 | [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 추론에서 첫 적용 지점 |
| 대상 | 활성화 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 추가 이득이 큼 | 정확도 저하 관리가 더 중요 |
| 범위 | Per-Tensor | 계산이 단순함 | 속도 우선 환경에 적합 |
| 범위 | Per-Channel | 정확도 방어에 유리 | 컨볼루션·선형층 품질 유지에 유리 |
| 방식 | 대칭형(Symmetric) | 0 중심 표현이 쉬움 | 하드웨어 구현 단순 |
| 방식 | 비대칭형(Asymmetric) | 분포 치우침 대응 | 입력 분포가 비대칭일 때 유리 |

결국 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)의 본질은 "[정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 버리고 시스템 효율을 산다"는 트레이드오프다. 따라서 좋은 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 단순히 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 많이 깎는 것이 아니라, 어느 층이 민감하고 어느 층은 둔감한지를 구분해 손실을 통제하는 설계다.

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 높은 해상도의 사진을 작은 화면용으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하는 과정과 같다. 모든 픽셀을 똑같이 버리면 얼굴이 뭉개지지만, 중요한 윤곽을 살리며 줄이면 용량은 작아져도 사진은 여전히 알아볼 수 있다.

---

## Ⅲ. 비교 및 연결

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 경계는 주로 사후 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)와 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 인지 학습에서 드러난다. 사후 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 이미 학습된 모델을 가져와 빠르게 변환하므로 배포 속도가 빠르지만, [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 많이 낮출수록 정확도 하락 위험이 커진다. 반면 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 인지 학습은 학습 중 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 오차를 미리 경험하게 만들어, 저정밀 환경에 맞는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 분포를 학습하게 한다.

| 항목 | PTQ (Post-[Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | QAT ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)-Aware [Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) |
| :--- | :--- | :--- |
| 적용 시점 | 학습 완료 후 | 재학습 또는 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/) 중 |
| 장점 | 빠르고 저렴함 | 정확도 방어력이 높음 |
| 약점 | INT4 이하에서 민감층 붕괴 가능 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·시간·[GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 비용 필요 |
| 적합 상황 | 빠른 배포, 기존 모델 최적화 | 임베디드, 엄격한 정확도 요구 |
| 대표 판단 | "지금 바로 줄일 수 있는가" | "낮은 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)에서도 품질을 지킬 수 있는가" |

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([Knowledge Distillation](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/))와도 자주 비교된다. [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)가 "작은 학생 모델을 새로 만드는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)"이라면, [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 "기존 모델을 더 얇게 포장하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)"에 가깝다. 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 둘 중 하나만 고집하기보다, 증류로 모델 구조를 줄이고 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)로 표현 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 낮추는 식의 결합 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 흔하다.

최근 [대규모 언어 모델](/studynote/04_software_engineering/09_cloud_native_ai_architecture/582_llm_based_code_generation_tools/)([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), [Large Language Model](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 영역에서는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)만 우선 줄이는 [Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)-Only [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/), 활성화 분포를 반영하는 AWQ (Activation-aware [Weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)), 헤시안 근사를 활용하는 GPTQ ([Generative Pre-trained Transformer](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) 같은 고도화된 PTQ 계열이 널리 쓰인다. 이는 재학습 비용을 피하면서도 실제 배포 품질을 확보하려는 흐름으로 이해하면 된다.

- **📢 섹션 요약 비유**: PTQ는 이미 완성된 가구를 문 크기에 맞춰 현장에서 조금 깎아 넣는 방식이고, QAT는 처음부터 그 문을 통과하도록 치수를 계산해 가구를 제작하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "몇 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)까지 가능한가"보다 "어떤 하드웨어와 어떤 품질 기준에서 가능한가"를 먼저 물어야 한다. 예를 들어 GPU가 INT8 [텐서 코어](/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)는 잘 지원하지만 INT4 가속은 제한적이라면, 이론상 INT4가 더 작아도 실제 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)은 기대만큼 줄지 않을 수 있다. 따라서 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 모델 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)만이 아니라 런타임, 컴파일러, 칩 지원 여부까지 함께 보는 아키텍처 결정이다.

### 적용 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong>하드웨어 지원 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/), 중앙 처리 장치(CPU, Central Processing Unit)가 목표 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)(INT8, INT4, FP8, 8-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) [Floating Point](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/))를 실제 가속하는가?
2. <strong>보정 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 확보</strong>: 실제 입력 분포를 닮은 [calibration](/studynote/10_ai/03_llm_nlp/230_digital_twin_simulation_calibration/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는가?
3. **민감 레이어 분리**: [임베딩](/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/), 출력 헤드, [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 큰 레이어는 혼합 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)(Mixed [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/))로 남길 것인가?
4. **품질 기준 정의**: 정확도, perplexity, [latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), [throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중 무엇을 우선할 것인가?
5. **운영 대상 구분**: 오프라인 배치 추론과 실시간 대화형 추론 중 어느 환경인가?

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- <strong>지원하지 않는 <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 수를 무리하게 채택</strong>: 모델은 INT4인데 실제 런타임은 내부에서 다시 INT8이나 FP16으로 변환해 오히려 느려지는 경우
- <strong>캘리브레이션 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 부실</strong>: 샘플 분포가 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 달라 운영 환경에서 정확도가 급락하는 경우
- **전 레이어 동일 처리**: 민감층까지 일괄 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)해 출력 품질이 무너지는 경우

기술사 관점에서는 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)를 "모델 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 기법"으로만 쓰지 말고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 요구사항과 인프라 제약을 맞추는 "배치 의사결정 도구"로 기억하는 것이 좋다. 즉 정확도 0.5% 손실로 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 2배를 얻는다면 채택 가치가 높지만, 금융·의료처럼 작은 오류도 치명적이면 혼합 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)나 QAT로 방어선을 세워야 한다.

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 이삿짐을 작은 엘리베이터에 맞춰 다시 포장하는 일과 같다. 상자만 줄인다고 끝나는 게 아니라, 엘리베이터 크기·짐의 중요도·깨지기 쉬운 물건 여부를 같이 봐야 안전하게 옮길 수 있다.

---

## Ⅴ. 기대효과 및 결론

[양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)의 가장 큰 효과는 같은 모델을 더 넓은 하드웨어에서 실행 가능하게 만든다는 점이다. 메모리 사용량이 줄고, 메모리 이동량이 줄며, 저정밀 연산 가속기를 활용할 수 있어 비용 대비 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 좋아진다. 그래서 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 초거대 모델 시대의 선택 옵션이 아니라, 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)화 과정에서 거의 필수에 가까운 최적화 수단이 되었다.

다만 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 만능이 아니다. 비전 모델, 음성 모델, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)형 언어 모델은 민감한 층이 서로 다르고, 동일한 INT8이라도 프레임워크와 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 구현에 따라 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 달라진다. 또한 배포 후 입력 분포가 바뀌면 캘리브레이션 전제가 무너질 수 있으므로, 품질 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링과 재양자화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 함께 준비해야 한다.

앞으로의 흐름은 FP8 (8-[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) [Floating Point](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/)), 하이브리드 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/), KV 캐시 ([Key-Value Cache](/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/)) [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)처럼 "전체를 일괄 축소"하기보다 "병목이 큰 부분만 정교하게 낮추는 방식"으로 갈 가능성이 높다. 따라서 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 "[비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 줄이는 기술"이 아니라, "정확도 예산 안에서 하드웨어 효율을 재배치하는 기술"로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 두꺼운 종이책을 전자책으로 옮기는 일과 비슷하다. 종이의 질감은 줄어들 수 있지만, 훨씬 가볍고 빠르게 들고 다니며 필요한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 즉시 펼칠 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| FP32 / FP16 / INT8 / INT4 | 모델 표현 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)와 메모리 사용량을 결정하는 기본 형식 |
| 스케일 (Scale) / 영점 ([Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-point) | 실수와 정수 사이를 변환하는 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) 수학의 핵심 파라미터 |
| PTQ (Post-[Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | 학습 완료 후 빠르게 적용하는 현실적인 배포 최적화 방식 |
| QAT ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)-Aware [Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) | 저비트 환경에서도 정확도를 지키기 위한 재학습 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| 혼합 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) (Mixed [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)) | 민감 레이어만 높은 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)로 남겨 품질과 효율을 절충하는 방식 |
| [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([Knowledge Distillation](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)) | 모델 구조를 줄이는 경량화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로, [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)와 병행되기 쉬움 |

### 📈 관련 키워드 및 발전 흐름도

```text
대형 모델 확산
    |
    v
메모리·대역폭 병목
    |
    +--> 지식 증류 (Knowledge Distillation)
    |
    +--> 양자화 (Quantization)
            |
            +--> PTQ (Post-Training Quantization)
            +--> QAT (Quantization-Aware Training)
            +--> INT8 / INT4 / FP8 최적화
            +--> KV Cache 양자화 · 온디바이스 LLM
```

이 흐름은 "모델 대형화 -> 경량화 필요 -> 정밀한 저비트 최적화"로 이어지는 현재 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인프라의 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 큰 장난감 상자를 더 작은 상자에 꼭 맞게 다시 포장하는 방법이에요.
2. 조금 덜 예쁘게 접히더라도 더 많은 장난감을 가방에 넣고 빨리 옮길 수 있어요.
3. 그래서 컴퓨터는 똑똑함을 많이 잃지 않으면서도 더 가볍고 빠르게 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)을 움직일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 420

<- **이전**: [157. 지식 증류 (Knowledge Distillation)](/studynote/10_ai/02_dl_architecture_new/157_knowledge_distillation/)
**다음**: [159. GAN (생성적 적대 신경망)](/studynote/10_ai/02_dl_architecture_new/159_gan/) ->

---
