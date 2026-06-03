+++
title = "157. 지식 증류 (Knowledge Distillation)"
date = 2026-04-17

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([Knowledge Distillation](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/))는 큰 교사 모델이 만든 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포를 작은 학생 모델이 모방하게 해, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 크게 잃지 않으면서 모델을 경량화하는 학습 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 단순 정답만 학습할 때보다 클래스 간 미묘한 유사도까지 전달할 수 있어, 엣지 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) (Edge [Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/))이나 저지연 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 적합한 소형 모델을 만들기 쉽다.
> 3. **판단 포인트**: 좋은 교사, 적절한 온도 ([Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/)), 학생의 수용 가능한 용량이 함께 맞아야 하며, 그렇지 않으면 작은 모델은 교사의 지식을 받지 못하고 오히려 불안정해질 수 있다.

---

## Ⅰ. 개요 및 필요성

[지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 대형 모델의 판단 방식을 소형 모델에 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 전달하는 모델 경량화 기법이다. 최근 딥러닝은 파라미터를 늘려 정확도를 높여 왔지만, 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 메모리 사용량, 추론 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, [전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/)가 곧 비용과 사용자 경험 문제로 이어진다. 특히 모바일, 센서, 차량, 로봇 같은 환경에서는 거대한 모델을 그대로 배포하기 어렵다.

단순히 모델을 줄이는 것만으로는 문제가 해결되지 않는다. 작은 모델을 처음부터 독립 학습시키면 표현력이 부족해 정확도가 크게 떨어지기 쉽고, [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))나 프루닝 ([Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/))은 이미 만들어진 모델을 깎는 방식이라 구조적 한계가 남는다. [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 "큰 모델이 어떻게 고민했는가"를 함께 넘겨주기 때문에, 작은 모델이 적은 자원으로도 더 나은 일반화 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 내도록 돕는다.

따라서 이 개념의 핵심은 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 그 자체보다 <strong>판단의 분포를 전수하는 것</strong>에 있다. 정답 한 칸만 맞추게 하는 학습이 아니라, 비슷한 클래스끼리 얼마나 헷갈렸는지까지 전달해야 작은 모델도 문제의 구조를 더 깊게 이해한다.

- **📢 섹션 요약 비유**: [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 두꺼운 전공서 전체를 들고 다니는 대신, 교수의 핵심 해설이 적힌 요약 노트를 받아 시험장에 들어가는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)의 기본 구조는 교사 모델, 학생 모델, 그리고 두 모델의 출력을 비교하는 [손실 함수](/knowledge-base/studynote/10_ai/01_ai_basics/075_loss_function_cost_function/)로 이루어진다. 이때 학생은 실제 정답뿐 아니라 교사가 만든 소프트 타깃 ([Soft Target](/knowledge-base/studynote/10_ai/05_data_science_ml/389_knowledge_distillation_soft_target/))도 함께 학습한다. 보통 손실은 교차 [엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/) ([Cross-Entropy](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/154_cross_entropy/), CE)와 쿨백-라이블러 발산 ([Kullback-Leibler Divergence](/knowledge-base/studynote/10_ai/05_data_science_ml/347_cross_entropy_kld/), [KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/))을 조합해 구성한다.

아래 그림은 같은 입력을 교사와 학생이 동시에 보고, 학생이 두 종류의 목표를 함께 학습하는 구조를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Distillation pipeline: one input, two learning signals              │
├──────────────────────────────────────────────────────────────────────┤
│ input x ─┬─▶ Teacher ─▶ logits z_t ─▶ Softmax(T) ─▶ q_t             │
│          │                                                           │
│          └─▶ Student ─▶ logits z_s ─▶ Softmax(T) ─▶ q_s             │
│                                   └─▶ Softmax(1) ─▶ y_hat           │
│                                                                      │
│ Loss = α·CE(y, y_hat) + (1-α)·KL(q_t || q_s)                         │
│        hard label fitting      teacher distribution matching         │
└──────────────────────────────────────────────────────────────────────┘
```

여기서 온도는 매우 중요하다. [Softmax](/knowledge-base/studynote/10_ai/03_llm_nlp/270_softmax/) 함수의 온도 T를 높이면 정답 이외의 클래스 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)도 더 평평하게 드러나서, 학생이 교사의 "헷갈림 구조"를 볼 수 있다. 이 정보는 흔히 다크 지식 (Dark Knowledge)이라 부르며, 예를 들어 고양이 사진에서 "개와는 조금 비슷하지만 자동차와는 거의 무관하다"는 식의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 전달한다.

| 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Teacher Model | 기준 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제공 | 충분히 학습된 고품질 모델이어야 함 |
| Student Model | 경량 추론 담당 | 목표 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 메모리에 맞는 크기 선정 |
| [Soft Target](/knowledge-base/studynote/10_ai/05_data_science_ml/389_knowledge_distillation_soft_target/) | 클래스 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 전달 | 온도 조절로 정보량 확보 |
| Hard Target | 실제 정답 보정 | 교사 편향을 직접 완화 |
| Distillation Loss | 두 목표의 균형 | α, T 값을 함께 튜닝 |

실무에서는 출력만 모방하는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)릿 기반 증류 외에도 중간 특징 맵을 맞추는 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 증류, 여러 교사를 쓰는 멀티 티처 증류, 자기 자신을 교사로 삼는 셀프 디스틸레이션 (Self-Distillation)도 사용된다. 중요한 점은 학생이 교사와 완전히 같은 구조일 필요는 없다는 것이다. [트랜스포머](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) ([Transformer](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)) 교사의 지식을 더 작은 [합성곱 신경망](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/) ([Convolutional Neural Network](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_CNN_Convolutional/), [CNN](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/243_cnn_stride_pooling_resnet_residual_yolo_object_detection/)) 학생에게 일부 이전하는 식의 교차 아키텍처 증류도 가능하다.

- **📢 섹션 요약 비유**: 정답만 외우는 공부가 아니라, 선생님이 어떤 보기들을 왜 비슷하게 봤는지까지 배우는 과외가 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)다.

---

## Ⅲ. 비교 및 연결

[지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)를 이해하려면 다른 경량화 기법과의 경계를 분명히 봐야 한다. 프루닝은 기존 모델에서 덜 중요한 연결을 제거하는 방식이고, [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 수치 표현 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 줄여 메모리와 연산량을 낮춘다. 반면 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 <strong>작은 모델을 새로 훈련해 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 넘겨받게 한다</strong>는 점에서 접근법이 다르다.

| 구분 | [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) | 프루닝 | [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) |
| :--- | :--- | :--- | :--- |
| 출발점 | 교사-학생 학습 | 기존 모델 절삭 | 기존 모델 수치 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |
| 핵심 자산 | 교사의 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포 | 희소성 (Sparsity) | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수 축소 |
| 장점 | 구조 자유도 높음, 정확도 보존 우수 | 모델 크기 감소 | 추론 속도·메모리 절감 큼 |
| 한계 | 추가 학습 비용 필요 | 과도하면 정확도 급락 | 하드웨어 지원 영향 큼 |

또한 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 [전이 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) ([Transfer Learning](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))과도 연결된다. [전이 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)이 사전학습된 표현을 새로운 과제에 옮기는 개념이라면, [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 <strong>모델의 출력 분포 자체를 다른 모델로 전달</strong>하는 쪽에 더 가깝다. 그래서 둘은 경쟁 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 아니라, 사전학습 교사를 만든 뒤 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)로 배포형 학생을 얻는 순차 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 자주 결합된다.

결국 비교의 핵심은 "무엇을 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하는가"다. 프루닝과 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 모델 자체를 깎고, [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 모델이 학습한 판단 방식을 옮긴다. 이 차이 때문에 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 정확도 보존에 강하고, 다른 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 기법과 함께 쓸 때 효과가 더 커진다.

- **📢 섹션 요약 비유**: 프루닝이 큰 짐가방에서 안 쓰는 물건을 빼는 일이라면, [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 꼭 필요한 내용만 작은 가방에 다시 정리해 담는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "작아질 수 있는가"보다 "목표 환경에서 충분히 쓸 만한가"를 먼저 판단해야 한다. 예를 들어 스마트폰 음성 비서나 공장 비전 검사 시스템은 50ms 이하 응답, 수십 메가바이트 이하 메모리, 낮은 [전력 소모](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/)가 중요하므로 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)가 매우 유효하다. 반대로 교사 추론 비용이 지나치게 크거나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋이 교사 편향을 그대로 담고 있으면, 학생은 빠르지만 왜곡된 모델이 될 수 있다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 교사 모델이 현재 업무 기준에서 충분히 높은 품질을 보이는가?
2. 학생 모델의 파라미터 수와 목표 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 배포 환경과 맞는가?
3. 온도 T와 손실 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) α를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 셋으로 튜닝했는가?
4. 학생과 교사의 용량 차이, 즉 캐퍼시티 갭 (Capacity Gap)이 지나치게 크지 않은가?
5. 증류 후에도 실제 하드웨어에서 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 전력 이득이 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)되는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 정확도가 낮은 교사를 그대로 기준으로 쓰는 경우
- 오프라인 정확도만 보고 온디바이스 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 측정하지 않는 경우
- 학생 모델이 너무 작아 표현력 한계를 넘은 경우
- 편향된 교사 출력을 그대로 모방시켜 오류를 증폭하는 경우

시험형 답안에서는 "정확도-[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간-메모리"의 삼각 균형을 말하는 것이 중요하다. [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 거의 항상 유용하지만, 교사 품질과 배포 환경 제약을 함께 보지 않으면 설계 판단이 반쪽이 된다.

- **📢 섹션 요약 비유**: [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 대형 트럭의 짐을 소형 밴으로 옮기는 일과 같아서, 무엇을 싣고 무엇을 포기할지 목적지 도로 사정까지 보고 결정해야 한다.

---

## Ⅴ. 기대효과 및 결론

[지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)의 가장 큰 효과는 대형 모델의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 더 넓은 환경으로 확장하는 데 있다. 같은 과제를 더 작은 모델로 처리하면 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 줄고, 클라우드 호출 비용과 배터리 사용량도 줄어든다. 이는 단순한 최적화를 넘어, 원래는 실행이 불가능했던 엣지 환경에서 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 가능하게 만든다는 의미가 있다.

다만 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)가 만능은 아니다. 교사가 잘못 배운 편향, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불균형, 학생의 표현력 부족이 있으면 품질 저하가 발생할 수 있고, 경우에 따라서는 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)나 프루닝을 추가로 결합해야 목표 자원 수준에 도달한다. 앞으로는 셀프 디스틸레이션, [멀티모달](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) 교사, 하드웨어 인지형 증류처럼 "배포 환경까지 포함해 설계하는 증류"가 더 중요해질 가능성이 높다.

따라서 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)는 "큰 모델을 작게 줄이는 기술"로만 기억하면 부족하다. 더 정확하게는 <strong>큰 모델의 판단 구조를 작은 모델로 이식해, 배포 가능한 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>으로 바꾸는 전달 기술</strong>로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 큰 나무를 화분에 옮겨 심을 수는 없지만, 좋은 씨앗을 받아 작은 화분에서도 같은 품종을 키우는 것이 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)다.

---

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Teacher Model | 학생에게 기준 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 분포를 제공하는 원천 모델 |
| Student Model | 경량 배포를 담당하는 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 대상 모델 |
| [Soft Target](/knowledge-base/studynote/10_ai/05_data_science_ml/389_knowledge_distillation_soft_target/) | 클래스 간 유사도와 다크 지식을 담는 분포 |
| [Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/) | 소프트 타깃 정보량을 조절하는 핵심 하이퍼파라미터 |
| [Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) / [Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) | 증류 후 추가 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)에 결합되는 대표 기법 |
| [Edge AI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/174_edge_ai_on_device_ai/) | [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)의 대표 적용 환경 |

### 관련 키워드 및 발전 흐름도

```text
Large Teacher Model
       │
       ▼
Soft Target + Dark Knowledge
       │
       ▼
Knowledge Distillation
       │
       ├──▶ Self-Distillation
       ├──▶ Feature Distillation
       └──▶ Multi-Teacher Distillation
       │
       ▼
Edge AI / On-device Inference / Low-latency Service
```

이 흐름은 "대형 모델의 지식 확보 → 분포 전달 → 경량 학생 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 배포 최적화"로 이어지는 확장 경로를 보여준다.

### 어린이를 위한 3줄 비유 설명

1. 아주 똑똑한 큰 로봇이 문제를 푸는 비밀 요령을 작은 로봇에게 알려주는 것이 [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)예요.
2. 작은 로봇은 정답만 외우는 게 아니라, 왜 다른 답이 비슷했는지도 같이 배워서 더 똑똑해져요.
3. 그래서 몸집은 작아도 휴대폰 안에서 빠르게 움직이는 똑똑한 로봇이 될 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 157 / 420

← **이전**: [156. RLAIF (AI 피드백 기반 강화학습)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/156_rlaif/)
**다음**: [158. 양자화 (Quantization)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/158_quantization/) →

---
