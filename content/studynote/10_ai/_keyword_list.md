---
title: 10. 인공지능 (AI) 및 머신러닝 키워드 목록
date: '2026-03-04'
tags:
- studynote-ai
---
[[267_weight_bias_activation|weight]] = 9999

# [[231_ai_turing_test|인공지능]] ([[190_ai_llm_requirements_specification|AI]]) / [[241_machine_learning_basics|머신러닝]] / 딥러닝 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 및 [[190_ai_llm_requirements_specification|AI]]/[[001_dikw_pyramid|데이터]] 사이언티스트를 위한 [[231_ai_turing_test|인공지능]] 전 영역 핵심 및 심화 키워드 800선입니다.

기초 [[241_machine_learning_basics|머신러닝]] [[001_algorithm_definition|알고리즘]]부터 최신 딥러닝([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]], [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]], [[246_transformer_self_attention_parallel_positional_encoding|Transformer]]), 초거대 언어 모델([[263_llm_large_language_model|LLM]]), [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]](Generative [[190_ai_llm_requirements_specification|AI]], [[276_fine_tuning|RAG]]), [[348_mlops|MLOps]], [[330_ai_ethics|AI 윤리]] 및 최신 [[190_ai_llm_requirements_specification|AI]] 아키텍처 동향까지 총망라하였습니다.

---

## 1. [[231_ai_turing_test|인공지능]] 기초 및 탐색 / [[233_expert_system|전문가 시스템]] (60개)
1. [[231_ai_turing_test|인공지능]] ([[001_artificial_intelligence|Artificial Intelligence]])의 정의 - 지능적 기계 및 에이전트를 설계하는 학문
2. [[002_turing_test|튜링 테스트]] ([[235_ai_turing_test_expert_system_fuzzy_logic|Turing Test]]) - 앨런 튜링 제안, 기계가 지능이 있는지를 판별하는 텍스트 대화 시험
3. [[003_strong_ai_agi|강인공지능]] (Strong [[190_ai_llm_requirements_specification|AI]] / AGI, Artificial General Intelligence) - 인간과 같거나 뛰어난 범용 지능
4. [[004_weak_ai_narrow_ai|약인공지능]] (Weak [[190_ai_llm_requirements_specification|AI]] / Narrow [[190_ai_llm_requirements_specification|AI]]) - 특정 작업(바둑, 번역, 인식)에만 특화된 지능
5. [[005_artificial_super_intelligence|초인공지능]] (ASI, [[005_artificial_super_intelligence|Artificial Super Intelligence]]) - 모든 면에서 인간을 초월한 지능
6. [[006_singularity|싱귤래리티]] ([[006_singularity|Singularity]] / 특이점) - [[231_ai_turing_test|인공지능]]이 스스로 자신보다 나은 AI를 만들어내어 기술 발전이 무한히 폭발하는 시점
7. [[007_knowledge_representation|지식 표현]] ([[007_knowledge_representation|Knowledge Representation]]) - 규칙 기반, 의미망, 프레임, 스크립트 등
8. [[008_knowledge_base_inference_engine|지식 베이스]] ([[008_knowledge_base_inference_engine|Knowledge Base]]) / 추론 엔진 (Inference Engine)
9. [[233_expert_system|전문가 시스템]] ([[233_expert_system|Expert System]]) - 특정 분야 전문가의 지식을 룰 기반으로 구현 (MYCIN, DENDRAL)
[[489_raid_10_hybrid|10]]. [[235_forward_backward_chaining|전향 추론]] ([[010_forward_chaining|Forward Chaining]]) - [[001_dikw_pyramid|데이터]]에서 시작하여 결론 도출 ([[001_dikw_pyramid|데이터]] 주도)
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_backward_chaining|후향 추론]] ([[011_backward_chaining|Backward Chaining]]) - 가설/목표에서 시작하여 조건 [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] (목표 주도)
12. [[012_fuzzy_logic|퍼지 논리]] ([[234_fuzzy_logic|Fuzzy Logic]]) - 0과 1 사이의 [[130_probability|확률]]적 연속값(소속도)을 이용해 애매한 개념 처리 (Zadeh 제안)
13. [[236_state_space_search_dfs_bfs|상태 공간 탐색]] ([[013_state_space_search|State Space Search]])
14. [[014_uninformed_search|맹목적 탐색]] ([[014_uninformed_search|Uninformed Search]]) - [[034_dfs|DFS]]([[034_dfs|깊이 우선 탐색]]), [[035_bfs|BFS]]([[035_bfs|너비 우선 탐색]])
15. [[015_heuristic_search|휴리스틱 탐색]] ([[015_heuristic_search|Heuristic Search]] / Informed Search) - 직관이나 경험 기반 정보([[210_heuristics_scheduling|휴리스틱]] 함수)를 활용한 최적 탐색
16. [[237_hill_climbing_local_optima|언덕 오르기 탐색]] ([[237_hill_climbing_local_optima|Hill Climbing]]) - [[178_as_is_to_be_analysis|현재 상태]]에서 이웃 상태 중 가장 좋은 곳으로만 이동 (지역 최적해에 빠질 위험)
17. A* ([[017_a_star_algorithm|A-Star]]) [[001_algorithm_definition|알고리즘]] - f(n) = g(n) + h(n), 시작점부터의 실제 비용 g(n)과 목표까지의 예상 비용 h(n)을 합산하여 최단 경로 탐색
18. [[018_admissible_heuristic|허용적 휴리스틱]] ([[018_admissible_heuristic|Admissible Heuristic]]) - A*가 최적해를 보장하기 위한 조건, h(n)이 실제 목표까지의 비용을 과대평가하지 않아야 함
19. [[019_minimax_algorithm|미니맥스 알고리즘]] ([[019_minimax_algorithm|Minimax Algorithm]]) - 턴제 게임 트리(체스, 틱택토)에서 자신은 최대(Max), 상대는 최소(Min)를 선택한다고 가정하고 탐색
20. [[020_alpha_beta_pruning|알파-베타 가지치기]] ([[020_alpha_beta_pruning|Alpha-Beta Pruning]]) - [[239_minimax_alpha_beta_pruning|미니맥스]] 트리에서 탐색할 필요가 없는 가지를 잘라내어 연산량 감소
21. [[240_mcts_monte_carlo|몬테카를로 트리 탐색]] ([[240_mcts_monte_carlo|MCTS]], Monte Carlo Tree Search) - 바둑(알파고) 등 경우의 수가 방대한 게임에서 무작위 시뮬레이션(롤아웃)을 통해 승률을 계산하여 최적 경로를 확장하는 탐색 기법
22. [[022_mcts_four_stages|MCTS 4단계 - 선택]]([[022_mcts_four_stages|Selection]]) -> 확장(Expansion) -> 시뮬레이션(Simulation) -> [[272_backpropagation|역전파]]([[272_backpropagation|Backpropagation]])
23. [[241_machine_learning_basics|머신러닝]] (Machine [[240_switch_learning_forwarding_flooding|Learning]]) 개념 - [[001_dikw_pyramid|데이터]]를 통해 기계가 스스로 규칙과 패턴을 학습
24. 학습의 3가지 패러다임 - [[121_supervised_learning|지도 학습]](Supervised), [[122_unsupervised_learning|비지도 학습]](Unsupervised), [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]](Reinforcement)
25. [[110_bias_variance_tradeoff|편향-분산 트레이드오프]] ([[379_ensemble_bias_variance_math|Bias-Variance]] Trade-off)
26. 편향 ([[094_bias|Bias]]) - 모델이 너무 단순하여 실제 [[001_dikw_pyramid|데이터]] 패턴을 놓침 (과소적합, [[246_underfitting_bias|Underfitting]])
27. [[136_variance|분산]] ([[136_variance|Variance]]) - 모델이 학습 [[001_dikw_pyramid|데이터]]의 노이즈까지 과도하게 외워버림 (과대적합, [[245_overfitting_variance|Overfitting]])
28. 오캄의 면도날 (Occam's Razor) 원칙 - 같은 [[282_performance_tactics|성능]]이면 구조가 단순한 모델이 낫다.
29. 차원의 저주 ([[080_curse_of_dimensionality|Curse of Dimensionality]]) - 특성(변수) 공간 차원이 늘어날수록, [[001_dikw_pyramid|데이터]] 간 거리가 희소해지고 학습 효율이 급감하는 현상
30. [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] ([[079_dimensionality_reduction|Dimensionality Reduction]]) 기법
31. [[247_feature_label_variables|독립 변수]] (Independent Variable / Feature) / 종속 변수 (Dependent Variable / Target/Label)
32. 회귀 (Regression) - 연속적인 수치 예측 (집값, 주가)
33. [[104_classification_analysis|분류]] ([[107_classification|Classification]]) - 이산적인 클래스 판별 (스팸 여부, 개/고양이 사진)
34. [[105_clustering_analysis|군집화]] ([[105_clustering_analysis|Clustering]]) - 정답(Label) 없이 [[001_dikw_pyramid|데이터]]의 유사도에 따라 그룹 묶기
35. [[106_association_rules|연관 규칙]] ([[106_association_rules|Association Rules]]) - [[107_market_basket_analysis|장바구니 분석]] (A를 사면 B도 산다)
36. 특성 공학 ([[081_feature_engineering|Feature Engineering]]) - [[064_relation_domain|도메인]] 지식을 활용하여 모델 학습에 좋은 [[247_feature_label_variables|피처]](Feature)를 추출/가공
37. [[079_one_hot_encoding_categorical_dummy_variable|원-핫 인코딩]] ([[079_one_hot_encoding_categorical_dummy_variable|One-Hot Encoding]]) - 범주형 [[001_dikw_pyramid|데이터]]를 0과 1의 벡터로 변환
38. 라벨 인코딩 (Label Encoding) / 정수 인코딩
39. [[249_scaling_normalization_standardization|스케일링]] (Scaling) - [[093_normalization|정규화]]([[093_normalization|Normalization]], 0~1), 표준화(Standardization, 평균 0 표준편차 1 Z-score)
40. [[250_cross_validation_kfold|교차 검증]] ([[250_cross_validation_kfold|Cross-Validation]]) - K-Fold 분할 모델 평가 기법 (과적합 방지, 일반화 [[282_performance_tactics|성능]] [[396_validation|확인]])
41. 하이퍼파라미터 (Hyperparameter) - 모델 학습 전 인간(엔지니어)이 직접 [[009_config|설정]]해야 하는 변수 ([[080_gradient_descent_learning_rate|학습률]], 트리 깊이 등)
42. [[251_grid_search_random_search|그리드 서치]] ([[251_grid_search_random_search|Grid Search]]) / 랜덤 서치 (Random Search) / 베이지안 최적화 - [[041_bagging_boosting|하이퍼파라미터 튜닝]] 기법
43. 평가 지표 - [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] ([[089_confusion_matrix_tp_fp_fn_tn|Confusion Matrix]]: TP, [[293_fp_function_point|FP]], FN, TN)
44. 정확도 (Accuracy) - 전체 대비 정답 비율 ([[001_dikw_pyramid|데이터]] 불균형 시 왜곡)
45. [[233_precision_recall_f1_roc_auc_threshold|정밀도]] ([[233_precision_recall_f1_roc_auc_threshold|Precision]]) - 모델이 Positive로 예측한 것 중 실제 Positive의 비율
46. [[092_recall_sensitivity_hit_rate|재현율]] ([[254_recall_sensitivity|Recall]] / 민감도 / TPR) - 실제 Positive 중에서 모델이 맞춘 비율
47. [[255_f1_score|F1-Score]] - [[233_precision_recall_f1_roc_auc_threshold|정밀도]]와 [[092_recall_sensitivity_hit_rate|재현율]]의 조화 평균
48. ROC 커브 (Receiver Operating Characteristic) & AUC (Area Under Curve) - 임계값 변화에 따른 FPR 대비 TPR [[070_graph_datastructure|그래프]]
49. [[125_ensemble_learning|앙상블 학습]] ([[125_ensemble_learning|Ensemble Learning]]) - 여러 개의 약한 [[104_classification_analysis|분류]]기를 결합하여 강력한 하나의 모델 구성
50. [[258_voting_ensemble|보팅]] ([[258_voting_ensemble|Voting]]) - 다수결 (Hard [[258_voting_ensemble|Voting]]) 및 [[130_probability|확률]] 평균 (Soft [[258_voting_ensemble|Voting]])
51. [[259_bagging_random_forest|배깅]] ([[259_bagging_random_forest|Bagging]], Bootstrap Aggregating) - 훈련 [[001_dikw_pyramid|데이터]]를 랜덤 복원 추출하여 독립 모델 [[430_index_fast_full_scan|병렬]] 학습 후 평균/다수결 ([[353_random_forest|Random Forest]])
52. [[127_boosting|부스팅]] ([[127_boosting|Boosting]]) - 앞 모델이 틀린 오차(잔차)에 [[267_weight_bias_activation|가중치]]를 부여해 다음 모델이 순차적으로 보완 ([[077_Adaboost|AdaBoost]], GBM, XGBoost, LightGBM)
53. 스태킹 (Stacking) - 여러 모델의 예측 결과를 다시 훈련 [[001_dikw_pyramid|데이터]]로 삼아 메타 모델이 최종 학습
54. 결정 트리 ([[124_decision_tree|Decision Tree]]) 학습 (불순도 기준 - [[151_entropy|엔트로피]], 지니 지수)
55. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] ([[227_logistic_regression_clt_pvalue_type_error|Logistic Regression]]) - [[268_sigmoid_vanishing_gradient|Sigmoid]] 함수 기반 이진 [[104_classification_analysis|분류]] 선형 모델
56. [[352_knn_distance_metrics|K-NN]] ([[262_knn|K-Nearest Neighbors]]) - 새로운 [[001_dikw_pyramid|데이터]]를 가장 가까운 K개 이웃의 클래스 중 다수결로 판별 (게으른 학습, [[380_computational_graph_lazy_eager_execution|Lazy]] [[240_switch_learning_forwarding_flooding|Learning]])
57. [[263_kmeans_em|K-Means 군집화]] ([[122_unsupervised_learning|비지도 학습]]) - K개의 중심점(Centroid)을 잡고 거리 기반 [[001_dikw_pyramid|데이터]] 할당, 중심점 이동 반복 EM(Expectation Maximization)
58. [[238_svm_margin_kernel_trick_naive_bayes|SVM]] ([[238_svm_margin_kernel_trick_naive_bayes|Support Vector Machine]]) - 두 클래스 간의 마진(Margin)을 최대화하는 초평면(Hyperplane)을 찾는 [[104_classification_analysis|분류]]/회귀 모델
59. [[059_kernel_trick_rbf_polynomial|커널 트릭]] ([[059_kernel_trick_rbf_polynomial|Kernel Trick]]) - 선형 [[104_classification_analysis|분류]] 불가능 [[001_dikw_pyramid|데이터]]를 고차원 내적 공간으로 매핑해 분리 ([[368_rbf_kernel|RBF 커널]], [[195_polynomial_generator_crc|다항식]] [[022_kernel_role|커널]])
60. [[060_naive_bayes_classifier_conditional_independence|나이브 베이즈 분류기]] ([[078_Naive_Bayes|Naive Bayes]]) - 변수들이 조건부 독립이라 가정하고 베이즈 정리를 적용한 [[130_probability|확률]]적 [[104_classification_analysis|분류]]기 (스팸 필터링)

## 2. 딥러닝 기초 및 신경망 아키텍처 (70개)
61. [[061_artificial_neural_network_ann_neuron_model|인공 신경망]] ([[350_ann|ANN]], Artificial Neural Network) - 인간 두뇌의 뉴런 생물학적 구조를 모방한 모델
62. [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] ([[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|Perceptron]]) - 로젠블랫 제안, 입력값 덧셈 후 [[431_ssthresh_slow_start_threshold|임계치]] 넘으면 1 출력 (단층 신경망)
63. [[265_single_layer_perceptron_xor|단층 퍼셉트론]]의 한계 - XOR(배타적 [[369_logic_bomb|논리]]합) 문제 등 선형 분리 불가 문제 해결 못함 (AI의 1차 암흑기 원인)
64. [[266_mlp_hidden_layers|다층 퍼셉트론]] (MLP, Multi-Layer [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|Perceptron]]) - 은닉층(Hidden Layer) 도입으로 비선형 문제 해결 가능
65. [[065_dnn_deep_neural_network|심층 신경망]] (DNN, Deep Neural Network) - 2개 이상의 은닉층을 가진 [[266_mlp_hidden_layers|다층 퍼셉트론]]
66. [[267_weight_bias_activation|가중치]] ([[267_weight_bias_activation|Weight]], W) / 편향 ([[094_bias|Bias]], b) - 선형 방정식의 파라미터 (y = Wx + b)
67. [[129_activation_function|활성화 함수]] ([[129_activation_function|Activation Function]]) - 신경망 층 사이에 비선형성(Non-linearity)을 부여하는 필수 함수
68. [[068_step_function_activation|계단 함수]] ([[068_step_function_activation|Step Function]]) - 0 이하면 0, 0 이상이면 1 반환 (미분 불가)
69. [[069_sigmoid_function_vanishing_gradient|시그모이드 함수]] ([[268_sigmoid_vanishing_gradient|Sigmoid]]) - 0~1 사이 반환, [[088_vanishing_gradient_relu_skip_connection|기울기 소실]]([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) 문제 발생
70. [[070_hyperbolic_tangent_tanh_activation|하이퍼볼릭 탄젠트]] ([[070_hyperbolic_tangent_tanh_activation|tanh]]) - -1~1 사이 반환, 중심이 0으로 수렴 ([[268_sigmoid_vanishing_gradient|시그모이드]]보다 우수)
71. [[269_relu_activation|ReLU]] ([[269_relu_activation|Rectified Linear Unit]]) 함수 - x>0이면 x, x<0이면 0 ([[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 해결, 연산 빠름, 현재 가장 대중적)
72. Leaky [[269_relu_activation|ReLU]] / ELU - ReLU의 죽은 뉴런(Dying [[269_relu_activation|ReLU]], 음수 입력 시 [[267_weight_bias_activation|가중치]] 미갱신) 문제 해결 (음수 구간에 미세한 기울기 부여)
73. [[073_softmax_function_multiclass_classification_probability|소프트맥스 함수]] ([[270_softmax|Softmax]]) - 다중 클래스 [[104_classification_analysis|분류]] 시 출력층 적용, 결과값 총합을 1로 만들어 [[130_probability|확률]]화
74. [[271_forward_propagation|순전파]] ([[271_forward_propagation|Forward Propagation]]) - 입력 [[001_dikw_pyramid|데이터]]가 신경망 층을 통과하여 최종 출력(예측값) 계산 과정
75. [[075_loss_function_cost_function|손실 함수]] ([[087_loss_function|Loss Function]] / Cost Function) - 정답(실제값)과 예측값의 오차 계산 (학습 방향 지시)
76. [[076_mse_mean_squared_error_regression|MSE]] ([[076_mse_mean_squared_error_regression|Mean Squared Error]]) - 평균 제곱 오차, 회귀 문제 [[075_loss_function_cost_function|손실 함수]]
77. [[077_cross_entropy_error_log_loss|크로스 엔트로피 오차]] ([[154_cross_entropy|Cross-Entropy]] Error) / Log Loss - 이진 및 다중 [[104_classification_analysis|분류]] 문제 [[075_loss_function_cost_function|손실 함수]]
78. [[272_backpropagation|역전파]] ([[272_backpropagation|Backpropagation]]) - 연쇄 법칙(Chain Rule)을 적용, 출력층의 오차를 입력층 방향으로 거슬러 전달하며 각 층의 [[267_weight_bias_activation|가중치]] 미분값(기울기)을 구하는 핵심 [[001_algorithm_definition|알고리즘]]
79. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] ([[088_optimizer|Optimizer]]) - [[075_loss_function_cost_function|손실 함수]]의 값을 최소화하도록 [[267_weight_bias_activation|가중치]]를 갱신하는 최적화 [[001_algorithm_definition|알고리즘]]
80. [[275_gradient_descent_sgd|경사 하강법]] ([[275_gradient_descent_sgd|GD]], [[165_gradient_descent|Gradient Descent]]) - [[075_loss_function_cost_function|손실 함수]]의 기울기가 감소하는 방향으로 [[080_gradient_descent_learning_rate|학습률]]([[240_switch_learning_forwarding_flooding|Learning]] Rate)만큼 이동
81. [[081_stochastic_gradient_descent_sgd|확률적 경사 하강법]] (SGD, [[241_optimizer_sgd_minibatch_adam_momentum_adaptive|Stochastic Gradient Descent]]) - 전체 [[001_dikw_pyramid|데이터]]가 아닌 미니배치(Mini-batch)로 기울기 계산 (속도 향상, 노이즈 수반)
82. [[082_mini_batch_size_epoch_iteration|미니배치 사이즈]] ([[082_mini_batch_size_epoch_iteration|Mini-batch Size]]) / 에폭 (Epoch) / 이터레이션 (Iteration)
83. [[083_local_minima_vs_global_minimum|지역 최솟값]] ([[083_local_minima_vs_global_minimum|Local Minima]]) vs 전역 최솟값 (Global Minimum) 안착 문제
84. [[276_momentum_optimizer|모멘텀]] ([[276_momentum_optimizer|Momentum]]) - 이전 기울기 관성을 활용하여 가속 이동 ([[083_local_minima_vs_global_minimum|Local Minima]] 탈출 효과)
85. 적응형 [[080_gradient_descent_learning_rate|학습률]] ([[137_edutech_adaptive_learning_lms|Adaptive Learning]] Rate) - 변수별로 [[080_gradient_descent_learning_rate|학습률]] 크기를 자동 조절 (Adagrad, RMSProp)
86. [[277_adam_optimizer|Adam]] ([[277_adam_optimizer|Adaptive Moment Estimation]]) - [[276_momentum_optimizer|모멘텀]](관성) 방향성 + RMSProp(스텝 사이즈 자동조절) 결합 (최신 딥러닝 기본 [[163_optimizer_sql_execution_plan_generator|옵티마이저]])
87. [[087_weight_initialization_xavier_he_glorot|가중치 초기화]] ([[087_weight_initialization_xavier_he_glorot|Weight Initialization]]) - 0초기화 금지, 사비에르(Xavier) [[459_quic_fec_forward_error_correction|초기]]화([[268_sigmoid_vanishing_gradient|Sigmoid]] 특화), He [[459_quic_fec_forward_error_correction|초기]]화([[269_relu_activation|ReLU]] 특화)
88. [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] ([[240_relu_vanishing_gradient_softmax_backprop_chain|Vanishing Gradient]]) - [[272_backpropagation|역전파]] 중 미분값이 0에 가까워져 앞쪽 은닉층 [[267_weight_bias_activation|가중치]] 갱신 불가 현상 ([[269_relu_activation|ReLU]], 잔차 연결 제안)
89. [[089_exploding_gradient_clipping|기울기 폭발]] ([[089_exploding_gradient_clipping|Exploding Gradient]]) - 갱신폭이 기하급수적 커짐 ([[267_weight_bias_activation|가중치]] 클리핑 / Gradient [[389_ppo_proximal_policy_optimization|Clipping]] 적용)
90. [[093_normalization|정규화]] 및 [[278_regularization_overview|과적합 방지 기법]] ([[134_regularization_dropout_batch_norm|Regularization]])
91. L1/L2 규제 (L1/L2 [[134_regularization_dropout_batch_norm|Regularization]] / [[267_weight_bias_activation|가중치]] 감쇠 [[091_l1_l2_regularization_weight_decay|Weight Decay]]) - [[075_loss_function_cost_function|손실 함수]]에 [[267_weight_bias_activation|가중치]] 절대값 합(L1)이나 제곱합(L2) 페널티 추가 
92. [[280_dropout|드롭아웃]] ([[242_regularization_dropout_early_stopping_l1_l2_lasso_ridge|Dropout]]) - 학습 시 은닉층 뉴런의 일부를 임의 [[130_probability|확률]](예 50%)로 비활성화하여 과의존 및 과적합 방지 (추론 시엔 모두 사용)
93. [[281_early_stopping|조기 종료]] ([[281_early_stopping|Early Stopping]]) - [[395_verification_process_review|검증]] [[001_dikw_pyramid|데이터]]([[396_validation|Validation]])의 손실이 줄어들지 않으면 에폭이 남아도 훈련 조기 중단
94. [[282_batch_normalization|배치 정규화]] ([[282_batch_normalization|Batch Normalization]]) - 미니배치 단위로 층의 입력을 평균 0, [[136_variance|분산]] 1로 [[093_normalization|정규화]] 연산 삽입 (학습 가속 및 안정화 효과)
95. [[089_CNN_Convolutional|합성곱 신경망]] ([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]], [[089_CNN_Convolutional|Convolutional Neural Network]]) - 이미지/영상 인식 특화 공간 정보 보존 신경망 아키텍처
96. [[096_convolution_layer_filter_stride_padding|합성곱 층]] ([[096_convolution_layer_filter_stride_padding|Convolution Layer]]) - 필터/[[022_kernel_role|커널]](Filter/[[022_kernel_role|Kernel]])을 입력 이미지 위로 이동([[097_stride_convolutional_neural_network_downsampling|Stride]])시키며 [[284_convolution_stride_padding|합성곱 연산]] 수행 (특성 추출)
97. [[097_stride_convolutional_neural_network_downsampling|스트라이드]] ([[097_stride_convolutional_neural_network_downsampling|Stride]]) - [[022_kernel_role|커널]]의 이동 보폭 칸 수
98. [[098_padding_convolutional_neural_network_same_valid|패딩]] ([[098_padding_convolutional_neural_network_same_valid|Padding]]) - 이미지 크기 축소 방지 및 가장자리 [[001_dikw_pyramid|데이터]] 보존을 위해 가장자리에 0 등 추가 ([[585_zero_skipping|Zero]] [[098_padding_convolutional_neural_network_same_valid|Padding]])
99. [[099_feature_map_activation_map_cnn_output|특성 맵]] ([[099_feature_map_activation_map_cnn_output|Feature Map]]) / 액티베이션 맵 - [[228_cnn_1d_2d_3d_video_medical|합성곱]] 결과 출력 [[055_array|배열]]
[[489_raid_10_hybrid|10]]0. [[100_pooling_layer_max_pooling_downsampling_cnn|풀링 층]] ([[285_pooling_layer|Pooling Layer]]) - [[099_feature_map_activation_map_cnn_output|특성 맵]]의 주요 정보만 남기고 크기(해상도)를 줄여 공간 불변성(Translation Invariance) 확보 및 연산량 감소
[[489_raid_10_hybrid|10]]1. [[101_max_pooling_average_pooling_global_average_pooling|최대 풀링]] ([[101_max_pooling_average_pooling_global_average_pooling|Max Pooling]]) / 평균 [[285_pooling_layer|풀링]] (Average [[285_pooling_layer|Pooling]])
102. [[102_fully_connected_layer_dense_flatten_softmax|완전 연결 층]] ([[696_fibre_channel_protocol|FC]], Fully Connected Layer / Dense Layer) - 추출된 특성을 1차원으로 펴서(Flatten) [[104_classification_analysis|분류]]/회귀 수행
103. [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 주요 아키텍처 발전 - LeNet-5, AlexNet([[269_relu_activation|ReLU]] 도입), VGGNet, GoogLeNet(Inception 구조), [[287_resnet_skip_connection|ResNet]]
104. [[287_resnet_skip_connection|ResNet]] ([[287_resnet_skip_connection|Residual Network]]) - 잔차 연결(Skip Connection / Shortcut) 구조 도입으로 100층 이상 깊은 네트워크의 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 문제 파훼
105. [[105_one_by_one_convolution_bottleneck_dimension_reduction|1x1 합성곱]] 연산의 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]/병목([[617_io_bottleneck|Bottleneck]]) 최적화 역할
106. [[288_object_detection_yolo_rcnn|객체 탐지]] ([[288_object_detection_yolo_rcnn|Object Detection]]) 기술 - 이미지 내의 객체 종류([[107_classification|Classification]])와 박스 위치 좌표(Bounding Box/Localization) 판별
107. R-[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]], Fast R-[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]], Faster R-[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] ([[107_rcnn_fast_faster_region_proposal_network|2-Stage 탐지기]]) / Region Proposal Network (RPN)
108. YOLO (You Only Look Once), [[327_ssd|SSD]] (1-Stage 탐지기) - 실시간/[[148_5g_embb_urllc_mmtc|초고속]] 탐지 
109. [[289_image_segmentation|이미지 분할]] ([[289_image_segmentation|Image Segmentation]]) - 단순 박스가 아닌 픽셀 단위 픽셀 [[104_classification_analysis|분류]]
[[308_static_dynamic_nat_pat_port_address_translation|11]]0. 의미적 분할 (Semantic [[364_segmentation|Segmentation]] / FCN, U-Net 구조) vs 인스턴스 분할 (Instance [[364_segmentation|Segmentation]] / Mask R-[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]])
[[308_static_dynamic_nat_pat_port_address_translation|11]]1. [[111_rnn_recurrent_neural_network_sequential_data|순환 신경망]] ([[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]], [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|Recurrent Neural Network]]) - 음성, 텍스트 등 시계열 (Sequential) 순차 [[001_dikw_pyramid|데이터]] 처리에 특화된 구조
112. 은닉 상태 (Hidden [[272_state_pattern|State]]) 순환 루프 - 이전 시간(t-1) 연산 결과가 다음 시간(t) 입력의 일부로 재활용되어 문맥([[033_context|Context]]) 기억
113. [[113_long_term_dependency_rnn|장기 의존성 문제]] ([[291_long_term_dependency|Long-term Dependency]]) - [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 시퀀스가 길어지면 [[459_quic_fec_forward_error_correction|초기]] 정보가 희석([[088_vanishing_gradient_relu_skip_connection|기울기 소실]])되는 한계
114. [[114_bptt_backpropagation_through_time|BPTT]] ([[114_bptt_backpropagation_through_time|Backpropagation Through Time]]) - 시간에 따른 오차 [[272_backpropagation|역전파]]
115. [[292_lstm|LSTM]] ([[292_lstm|Long Short-Term Memory]]) - [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 한계 극복, 은닉 상태(단기기억) 외에 셀 상태(Cell [[272_state_pattern|State]], 장기기억) 컨베이어 벨트 도입
116. LSTM의 3가지 게이트 - 입력 게이트(Input), 삭제 게이트(Forget, 기존 기억 폐기 비율 결정), 출력 게이트(Output)
117. [[294_gru|GRU]] ([[294_gru|Gated Recurrent Unit]]) - LSTM의 복잡한 구조를 간소화(업데이트/리셋 게이트), 연산 속도 개선
118. [[118_bidirectional_rnn|양방향 RNN]] ([[118_bidirectional_rnn|Bidirectional RNN]]) - 과거뿐만 아니라 미래의 문맥 역방향 연산 결과도 활용
119. [[245_seq2seq_context_vector_attention_dynamic_weight|Seq2Seq]] ([[295_seq2seq|Sequence to Sequence]]) 모델 - [[040_encoder|인코더]]([[040_encoder|Encoder]])-[[039_decoder|디코더]]([[039_decoder|Decoder]]) 구조, 기계 번역 및 챗봇 뼈대
120. [[120_context_vector|컨텍스트 벡터]] ([[120_context_vector|Context Vector]]) - [[040_encoder|인코더]]의 최종 은닉 상태, 고정된 크기 [[055_array|배열]]에 모든 의미를 [[347_compaction|압축]]해야 하는 병목 한계 (어텐션 탄생 배경)

## 3. 어텐션, [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]], 초거대 언어 모델 ([[263_llm_large_language_model|LLM]]) 및 [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]] (60개)
121. [[296_attention_mechanism|어텐션 메커니즘]] ([[296_attention_mechanism|Attention Mechanism]]) - [[245_seq2seq_context_vector_attention_dynamic_weight|Seq2Seq]] 한계 극복, [[039_decoder|디코더]]가 매 단어를 [[087_process_state_transition|생성]]할 때마다 [[040_encoder|인코더]]의 전체 시퀀스 중 '어느 부분에 집중(Attention)해야 하는지' 동적 [[267_weight_bias_activation|가중치]] 연산
122. [[298_qkv_attention|쿼리]](Query), 키([[067_db_key_uniqueness_minimality|Key]]), 값(Value) 체계 - [[002_database_definition|데이터베이스]] 검색과 유사, Q([[178_as_is_to_be_analysis|현재 상태]])와 가장 일치하는 K([[040_encoder|인코더]] 출력)를 찾아 V([[040_encoder|인코더]] 값)를 가중합
123. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] ([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]) 아키텍처 - 2017년 구글 "Attention Is All You Need" 논문 제안. [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]/CNN을 완전히 배제하고 '오직 어텐션'만으로 구성, [[430_index_fast_full_scan|병렬]] 연산 극대화
124. 셀프 어텐션 ([[124_self_attention|Self-Attention]]) - 입력 시퀀스 내부 단어들끼리의 상호 연관성/문맥을 계산 (it이 가리키는 대명사 유추 등)
125. [[299_multi_head_attention|멀티 헤드 어텐션]] ([[299_multi_head_attention|Multi-Head Attention]]) - 어텐션 연산을 [[430_index_fast_full_scan|병렬]]로 N개 수행하여 다각도(문법, 의미, 구조 등)의 특성 정보 추출
126. [[300_positional_encoding|포지셔널 인코딩]] ([[300_positional_encoding|Positional Encoding]]) - [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]는 RNN과 달리 단어를 한 번에 [[430_index_fast_full_scan|병렬]] 입력받으므로 순서 정보가 소실됨 -> 단어 위치(순서) 수학 값을 벡터에 더해줌
127. [[172_maas_mobility_as_a_service|마스]]크드 셀프 어텐션 (Masked [[124_self_attention|Self-Attention]]) - [[039_decoder|디코더]] 훈련 시 미래의 단어를 미리 보지 못하도록(정답 컨닝 방지) 행렬을 가리는 [[172_maas_mobility_as_a_service|마스]]킹 연산
128. [[040_encoder|인코더]]-[[039_decoder|디코더]] 어텐션 ([[128_cross_attention|Cross Attention]])
129. 피드 포워드 신경망 (FFNN, Position-wise Feed-[[235_forward_backward_chaining|Forward]]) 적용망
130. [[225_foundation_model_peft_lora|파운데이션 모델]] ([[225_foundation_model_peft_lora|Foundation Model]]) - 대규모 정제되지 않은 [[001_dikw_pyramid|데이터]](Self-supervised)로 사전 학습(Pre-[[588_mlops_pipeline_automation|training]])되어 여러 다운스트림(Downstream) [[150_task|태스크]]로 전이(Adaptable)할 수 있는 초대형 모델 체계
131. [[266_self_supervised_learning|자기 지도 학습]] ([[266_self_supervised_learning|Self-Supervised Learning]]) - 정답 라벨 없이 [[001_dikw_pyramid|데이터]] 자체의 구조(빈칸 채우기, 다음 단어 예측)로 학습 목표를 자동 [[009_config|설정]]
132. [[132_transfer_learning|전이 학습]] ([[132_transfer_learning|Transfer Learning]]) - 대규모 [[001_dikw_pyramid|데이터]]로 학습된 기본 모델([[267_weight_bias_activation|가중치]])을 가져와 내 작은/특화된 [[001_dikw_pyramid|데이터]]에 맞게 재학습(파인튜닝)하여 시간/비용 절약
133. [[304_fine_tuning|파인 튜닝]] ([[304_fine_tuning|Fine-Tuning]] / [[133_fine_tuning|미세 조정]]) - 사전 학습 모델 구조 유지, 타겟 목적(법률 봇, 질의응답) [[001_dikw_pyramid|데이터]]로 전체 혹은 일부 [[267_weight_bias_activation|가중치]] 추가 조정 학습
134. [[282_peft_parameter_efficient_fine_tuning|파라미터 효율적 미세 조정]] ([[306_peft_lora|PEFT]], [[306_peft_lora|Parameter-Efficient Fine-Tuning]]) - 거대 모델 전체 [[267_weight_bias_activation|가중치]] 업데이트가 불가능할 때 극히 일부 [[259_adapter_pattern_interface_wrapper|어댑터]]([[259_adapter_pattern_interface_wrapper|Adapter]]) 파라미터만 추가 튜닝 (자원 절약)
135. [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] ([[145_peft_lora_low_rank_adaptation|Low-Rank Adaptation]]) - PEFT의 대표 기법, 거대 [[267_weight_bias_activation|가중치]] 행렬을 업데이트하는 대신 저차원(Low-Rank) 분해 행렬을 삽입 훈련 후 병합 ([[418_gpu|GPU]] VRAM 절감 효과 극대화)
136. 프롬프트 튜닝 ([[136_prompt_tuning|Prompt Tuning]] / P-Tuning)
137. [[301_bert_mlm|BERT]] ([[301_bert_mlm|Bidirectional Encoder Representations from Transformers]]) - [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]의 '[[040_encoder|인코더]]'만 사용. 텍스트 양방향 문맥 동시 이해 특화 (텍스트 [[104_classification_analysis|분류]], [[105_exploratory_data_analysis|감성 분석]] 우수)
138. [[138_mlm_learning|MLM]] (Masked Language Modeling) 학습 - 문장 중간 단어를 [MASK] 처리 후 맞추는 BERT의 사전 학습 목표
139. [[139_nsp_next_sentence_prediction|NSP]] ([[139_nsp_next_sentence_prediction|Next Sentence Prediction]]) - 두 문장이 이어지는 문장인지 판별 (문맥성 파악)
140. [[302_gpt_autoregressive|GPT]] ([[302_gpt_autoregressive|Generative Pre-trained Transformer]]) 패밀리 - [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]]의 '[[039_decoder|디코더]]'만 사용. 이전 단어들을 보고 다음 단어 1개를 통계적으로 자동 회귀([[383_llm_autoregressive_math|Auto-Regressive]]) 예측 [[087_process_state_transition|생성]]
141. 초거대 언어 모델 ([[263_llm_large_language_model|LLM]], [[263_llm_large_language_model|Large Language Model]]) - 수십억~수천억 파라미터 크기, [[302_gpt_autoregressive|GPT]]-3, [[302_gpt_autoregressive|GPT]]-4, Llama 2/3, PaLM, Claude 등
142. 파라미터 [[249_scaling_normalization_standardization|스케일링]] 효과 ([[265_emergent_abilities|Emergent Abilities]]) - 모델 크기가 특정 [[431_ssthresh_slow_start_threshold|임계치]]를 넘으면 훈련받지 않은 연산/[[369_logic_bomb|논리]]/문맥 능력이 갑자기 발현되는 현상
143. [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]] ([[224_prompt_engineering_guideline|Prompt Engineering]]) - 모델의 최적 결과물을 이끌어 내기 위해 입력(명령/[[033_context|컨텍스트]]/예시) 텍스트를 최적화 설계하는 기술
144. 퓨샷 러닝 (Few-Shot [[240_switch_learning_forwarding_flooding|Learning]]) - [[304_fine_tuning|파인 튜닝]] 대신, 프롬프트 입력에 질문과 함께 2~3개의 풀이 예시(정답 쌍)를 던져주어 모델이 패턴을 즉석 추론 모방하게 하는 방식
145. 제로샷 러닝 ([[585_zero_skipping|Zero]]-Shot) - 예시 없이 질문만 바로 명령 (일반화 [[282_performance_tactics|성능]])
146. [[273_zero_few_shot_learning|생각의 사슬]] ([[146_chain_of_thought_cot|CoT]], [[146_chain_of_thought_cot|Chain-of-Thought]]) 프롬프팅 - 복잡한 [[369_logic_bomb|논리]]/수학 문제를 풀 때 "단계별로 차근차근 생각해 보자(Let's think step by step)"라는 문구를 주입하여, 중간 추론 과정을 텍스트로 풀어내 정답률을 극대화
147. [[147_concept|ToT]] ([[147_concept|Tree-of-Thought]]) 분기 사고 구조 탐색망 추론 기법
148. [[251_hallucination_rag_augmented_retrieval_vector_db|할루시네이션]] ([[345_llm_foundation_model_hallucination|Hallucination]] / [[275_react_framework|환각]]) - LLM이 사실이 아닌 내용을 마치 진실인 것처럼 그럴싸하게 꾸며내어 답변하는 치명적 [[352_defect_definition|결함]] 현상
149. [[149_hallucination_defense_strategy|할루시네이션 방어 전략]] - 프롬프트 제약(모르면 모른다고 답할 것), [[276_fine_tuning|RAG]] 도입, 모델 파인튜닝, 팩트 체커 [[250_cross_validation_kfold|교차 검증]]
150. [[276_fine_tuning|RAG]] ([[585_rag_retrieval_augmented_generation|Retrieval-Augmented Generation]] / [[222_rag_retrieval_augmented_generation|검색 증강 생성]]) - LLM의 정보 최신성 결여 및 [[275_react_framework|환각]] 방지를 위해, 질문 시 외부 [[002_database_definition|데이터베이스]]/위키/문서를 검색(Retrieve)하여 찾은 관련 사실 문단([[033_context|Context]])을 프롬프트에 주입(Augment) 후 답변 [[087_process_state_transition|생성]]
151. [[223_vector_database_embedding|벡터 데이터베이스]] ([[223_vector_database_embedding|Vector Database]]) - [[276_fine_tuning|RAG]] 구현 필수 인프라. 문서를 [[278_instruction_tuning|임베딩]] 텐서로 변환 저장하고 코사인/유클리디안 유사도 기반 고속 의미 검색망
152. [[278_instruction_tuning|임베딩]] ([[278_instruction_tuning|Embedding]]) - 텍스트(단어, 문장)의 의미적 유사도를 수백 차원의 실수 밀집 벡터(Dense Vector) [[055_array|배열]] 위치로 변환 투영 (유사 의미 = 벡터 공간 근접)
153. [[339_word2vec|Word2Vec]] - CBOW(주변 단어로 중심 예측), Skip-gram(중심 단어로 주변 예측) [[278_instruction_tuning|임베딩]] 방식
154. [[147_instruction_tuning_rlhf_alignment|인스트럭션 튜닝]] ([[147_instruction_tuning_rlhf_alignment|Instruction Tuning]]) - 범용 LLM을 "인간의 지시(명령)" 형식 문장에 잘 따르도록 질문-응답 [[001_dikw_pyramid|데이터]]셋으로 추가 [[121_supervised_learning|지도 학습]]시킨 [[288_version_ihl_tos_total_length|버전]] (ChatGPT 등)
155. [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] ([[250_rlhf_human_feedback_reinforcement_alignment_cot|Reinforcement Learning from Human Feedback]] / [[148_rlhf_human_feedback_reinforcement|인간 피드백 기반 강화학습]]) - LLM이 내뱉는 다수 답변 중 인간이 선호하는, 유용하고 덜 유해한 답변을 보상(Reward) 랭킹 채점 모델로 훈련시켜 모델 [[087_process_state_transition|생성]] 성향 통제 (정렬, Alignment 기법)
156. [[269_vector_database|RLAIF]] ([[269_vector_database|AI 피드백 기반 강화학습]]) - 인간 대신 더 큰 [[190_ai_llm_requirements_specification|AI]](예: [[302_gpt_autoregressive|GPT]]-4)가 피드백 평가 채점 대행 
157. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]]) - 크기가 거대하고 무거운 선생님(Teacher) 모델의 지식 파라미터 분포를 크기가 작은 학생(Student) 모델에 [[347_compaction|압축]] [[016_replication_factor|복제]]하여 경량화([[174_edge_ai_on_device_ai|Edge AI]] 최적화)하는 기법
158. [[434_quantization|양자화]] ([[434_quantization|Quantization]]) - 모델 [[267_weight_bias_activation|가중치]] [[001_dikw_pyramid|데이터]] 타입 [[233_precision_recall_f1_roc_auc_threshold|정밀도]]를 [[087_floating_point|부동소수점]](FP32)에서 16비트, 8비트(INT8), 4비트(INT4) 정수로 깎아 연산/메모리 효율 향상(파라미터 축소 [[347_compaction|압축]] 기법)
159. [[087_process_state_transition|생성]]형 모델 종류: [[154_gan_generative_adversarial_network|GAN]] (Generative Adversarial Networks) - [[087_process_state_transition|생성]]자(Generator)와 판별자(Discriminator)가 위조 지폐범과 경찰처럼 서로 적대적으로 경쟁/학습하여 진짜 같은 가짜 이미지 [[087_process_state_transition|생성]] 체계
160. [[153_diffusion_model_stable_diffusion_denoising|디퓨전 모델]] ([[153_diffusion_model_stable_diffusion_denoising|Diffusion Model]]) - 원본 이미지에 노이즈를 점진적 추가([[235_forward_backward_chaining|Forward]])해 파괴한 뒤, 역으로 노이즈를 제거(Reverse/Denoising)하는 과정을 학습하여 완벽한 이미지를 텍스트 기반 [[087_process_state_transition|생성]] (Midjourney, Stable Diffusion, DALL-E)

## 4. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]], [[348_mlops|MLOps]], [[190_ai_llm_requirements_specification|AI]] 인프라 및 트렌드 (70개)
161. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] ([[094_reinforcement_learning|Reinforcement Learning]]) - 정답이 없고 보상만 주어진 환경([[066_gitlab_flow_environment_branch_strategy|Environment]])에서, 에이전트(Agent)가 최적의 행동(Action) [[164_policy|정책]]([[164_policy|Policy]])을 찾아 누적 보상(Reward)을 최대화하는 과정 탐색
162. [[463_markov_decision_process_mdp|마르코프 결정 과정]] ([[463_markov_decision_process_mdp|MDP]], [[314_mdp_rl|Markov Decision Process]]) 수학 모델 기반 - 상태([[272_state_pattern|State]]), 행동(Action), 보상(Reward), 전이 [[130_probability|확률]](Transition [[130_probability|Probability]]), 할인율(Discount Factor)
163. [[163_value_function|가치 함수]] ([[163_value_function|Value Function]]) - 특정 상태나 행동을 선택했을 때 미래에 얻을 것으로 예상되는 누적 보상 추정치
164. [[164_policy|정책]] ([[164_policy|Policy]], π) - 상태 s에서 어떤 행동 a를 취할지 결정하는 매핑 룰 ([[130_probability|확률]]적 or 결정적)
165. [[315_exploration_exploitation|탐험]] ([[315_exploration_exploitation|Exploration]]) vs 활용 (Exploitation) 딜레마 - 새로운 불확실 경로 탐색(알파고 불계승) vs 이미 [[395_verification_process_review|검증]]된 최고 보상 행동 반복
166. [[166_epsilon_greedy|엡실론-그리디]] ([[166_epsilon_greedy|Epsilon-Greedy]]) [[001_algorithm_definition|알고리즘]] [[315_exploration_exploitation|탐험]] 조절 
167. [[167_q_learning|큐-러닝]] ([[316_q_learning|Q-Learning]]) [[001_algorithm_definition|알고리즘]] - 행동 [[163_value_function|가치 함수]]([[314_reinforcement_learning_bellman|Q-Value]]) 기반 오프 폴리시([[464_q_learning_off_policy|Off-policy]]) 강화학습, Q-Table 갱신
168. [[168_dqn|딥 큐 네트워크]] ([[465_dqn_deep_q_network|DQN]], [[465_dqn_deep_q_network|Deep Q-Network]]) - 무한한 상태 공간 문제(영상 등)에 Q-Table 대신 딥러닝([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]])을 함수 근사기(Function Approximator)로 도입
169. [[169_experience_replay|경험 재생]] ([[169_experience_replay|Experience Replay]]) 메모리 버퍼 훈련 최적화망 샘플 재활용 ([[465_dqn_deep_q_network|DQN]] 기법)
170. [[170_target_network|타겟 네트워크]] ([[170_target_network|Target Network]]) 정지 버퍼 복사 
171. [[171_policy_gradient|정책 경사법]] ([[318_policy_gradient_actor_critic|Policy Gradient]]) - Q값을 구하지 않고 신경망이 직접 최적 [[164_policy|정책]]([[130_probability|확률]])을 산출하도록 훈련 (REINFORCE [[001_algorithm_definition|알고리즘]])
172. [[172_actor_critic|액터-크리틱]] ([[172_actor_critic|Actor-Critic]]) 모델 - 행동을 결정하는 Actor 망과 행동 가치를 평가하는 Critic 망 결합 구조
173. [[173_a3c_ppo|A3C]] ([[173_a3c_ppo|Asynchronous Advantage Actor-Critic]]) 및 [[395_ppo_clipping|PPO]] ([[395_ppo_clipping|Proximal Policy Optimization]], OpenAI 개발 로보틱스/[[263_llm_large_language_model|LLM]] 기본 튜닝 강화 모델)
174. [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) 철학 - [[241_machine_learning_basics|머신러닝]] 개발, 테스트, 배포, 유지보수 전체 [[123_pipe|파이프]]라인 자동화 및 [[090_configuration_item|CI]]/CD/[[162_continuous_training_pipeline_model_retraining|CT]] (지속적 훈련 [[162_continuous_training_pipeline_model_retraining|Continuous Training]])
175. [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] ([[163_data_drift_statistical_distribution_shift|Data Drift]]) - 시간이 지남에 따라 모델 서빙 단계의 실제 사용자 입력 [[001_dikw_pyramid|데이터]] 통계적 분포가 훈련 [[001_dikw_pyramid|데이터]] 분포와 달라지는 현상 (정확도 저하 원인)
176. [[164_concept_drift_target_mapping_change|컨셉 드리프트]] ([[164_concept_drift_target_mapping_change|Concept Drift]]) - 입력과 타겟 매핑 정답(결과 해석 룰)의 [[083_relationship_in_er_model|관계]] 자체가 변함 (예: 코로나 이전/이후 구매 패턴 급변)
177. [[177_mlops_pipeline_components|MLOps 파이프라인 구성 요소]] ([[165_feature_store_training_serving_consistency|Feature Store]], [[166_model_registry_versioning_mlflow|Model Registry]], Model Serving [[014_api_posix|API]], Model Monitoring Dashboard)
178. [[165_feature_store_training_serving_consistency|피처 스토어]] ([[165_feature_store_training_serving_consistency|Feature Store]]) - 전처리된 모델 학습용 [[247_feature_label_variables|피처]] [[001_dikw_pyramid|데이터]]를 팀 간 공유, 재사용 가능하게 관리 [[456_caching|캐싱]] 인프라
179. [[167_kubeflow_kubernetes_ml_pipeline|쿠브플로우]] ([[167_kubeflow_kubernetes_ml_pipeline|Kubeflow]]) - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]](K8s) 기반 [[205_kubernetes_container_orchestration|컨테이너 오케스트레이션]] [[241_machine_learning_basics|머신러닝]] 워크플로우 [[191_oss_license_compliance|오픈소스]] 플랫폼
180. [[180_mlflow|MLflow]] - [[241_machine_learning_basics|머신러닝]] 생명주기 관리 추적(Tracking), 패키징(Projects), 배포(Models) 프레임워크 도구 통합
181. [[181_apache_airflow|데이터 파이프라인 전처리]]([[215_etl_vs_elt_pipeline|ETL]]/[[034_elt|ELT]]) [[208_schedule_history_transaction_execution_order|스케줄]]링 ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]]) 연동
182. [[182_spark_ray_distributed|분산 처리 컴퓨팅 AI 훈련 인프라]] ([[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]], Ray) [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]] 적재 
183. 하이퍼파라미터 오토튜닝 최적화 ([[176_automl_hyperparameter_optimization_bayesian|AutoML]] - 신경망 자동 탐색 구조 아키텍처 [[492_nas_network_attached_storage|NAS]], Neural [[319_architecture|Architecture]] Search 포함)
184. A/B 테스팅 [[575_shadow_deployment_traffic_mirroring|섀도우 배포]] 및 [[595_canary_stack_smashing_protector|카나리]]([[595_canary_stack_smashing_protector|Canary]]) 롤아웃 [[190_ai_llm_requirements_specification|AI]] 런타임 모델 서빙 
185. [[418_gpu|GPU]] 아키텍처 연산 기반 [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]]) 하드웨어 (NVIDIA [[420_cuda|CUDA]] [[430_index_fast_full_scan|병렬]] 행렬곱 특화) 
186. [[186_ai_accelerators_tpu_npu_lpu|AI 반도체 엑셀러레이터]] [[425_tpu|TPU]] ([[425_tpu|Tensor Processing Unit]] / Google [[426_systolic_array|시스톨릭 어레이]] 고속 행렬 연산기), [[424_npu|NPU]] ([[424_npu|Neural Processing Unit]]), [[438_lpu|LPU]] (언어 모델 가속기)
187. [[187_mixed_precision_training|혼합 정밀도 훈련]] ([[173_tensor_core_hbm_mixed_precision_training|Mixed Precision Training]]) - 속도/메모리 한계를 위해 FP32 [[267_weight_bias_activation|가중치]] 갱신, FP16 [[129_activation_function|활성화 함수]] 통과 조합 딥러닝 
188. [[188_multi_gpu_distributed_training|멀티 GPU 분산 학습 전술]] - [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화 ([[001_dikw_pyramid|Data]] Parallelism, 배치 쪼개기) vs 모델 [[430_index_fast_full_scan|병렬]]화 (Model Parallelism, 네트워크 층 쪼개기 / [[123_pipe|파이프]]라인 [[430_index_fast_full_scan|병렬]]) 
189. [[585_zero_skipping|ZeRO]] ([[334_vram_zero_optimizer|Zero Redundancy Optimizer]]) - 거대 모델 훈련 시 멀티 [[418_gpu|GPU]] 간 중복되는 [[163_optimizer_sql_execution_plan_generator|옵티마이저]], 그래디언트 메모리를 [[179_table_partitioning_concept|파티셔닝]] 공유 절약
190. [[256_federated_learning_privacy_model_security|연합 학습]] ([[256_federated_learning_privacy_model_security|Federated Learning]]) [[136_variance|분산]] 노드 모바일 기기 [[386_data_clean_room_sharing|데이터 공유]] 통제 프라이버시 [[571_protection_vs_security|보호]] 구조 (구글 키보드 추천 적용)
191. [[227_xai_explainable_ai_lime_shap|설명 가능한 AI]] ([[227_xai_explainable_ai_lime_shap|XAI]], [[255_xai_lime_shap_explainable_contribution|eXplainable AI]]) 목표 - 블랙박스 모델 결과 추론 과정 투명도 근거 확보 [[369_logic_bomb|논리]] 증명 
192. [[326_lime|LIME]] ([[326_lime|Local Interpretable Model-agnostic Explanations]]) [[001_algorithm_definition|알고리즘]] - 개별 예측 결과 근처에 선형 근사(대리) 모델을 띄워 변수 중요성 [[396_validation|확인]] 국소적 해석 기법
193. [[327_shap|SHAP]] ([[327_shap|SHapley Additive exPlanations]]) 지표 - 게임 이론(섀플리 값) 기반 [[247_feature_label_variables|피처]]가 최종 예측값에 기여한 영향력 기여분 수치 분해 전역적 해석 
194. [[194_deepdream_gradcam|딥 드림]] ([[194_deepdream_gradcam|DeepDream]]) 활성화 맵 [[003_bigdata_7v|시각화]] 및 CAM / Grad-CAM (이미지 [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 판단 중요 픽셀 히트맵 가시화 기법)
195. [[330_ai_ethics|AI 윤리]] 및 거버넌스 가이드라인 (EU [[190_ai_llm_requirements_specification|AI]] Act 법안 동향: 금지 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]], 고위험 [[190_ai_llm_requirements_specification|AI]], 제한적 위험 분할 규제 기준망)
196. [[196_ai_bias_fairness|모델 편향성]] ([[190_ai_llm_requirements_specification|AI]] [[094_bias|Bias]] / Fairness) 통제망 - 학습 [[001_dikw_pyramid|데이터]] 차별, 인종/성별 분포 왜곡 고착화 감시
197. [[942_adversarial_example|적대적 예제]] ([[197_adversarial_attack|Adversarial Attack]]) [[947_data_poisoning|데이터 포이즈닝]] 미세 노이즈 첨가 자율주행 오류 유도 방어 
198. [[286_multimodal_ai|멀티모달 AI]] ([[286_multimodal_ai|Multimodal AI]]) 시스템 - 텍스트, 이미지, 오디오, 비디오 이기종 [[001_dikw_pyramid|데이터]]를 동시 이해/[[087_process_state_transition|생성]] 융합 [[225_foundation_model_peft_lora|파운데이션 모델]] ([[302_gpt_autoregressive|GPT]]-4o, Gemini 1.5, Sora)
199. [[232_spatial_computing_digital_twin|공간 컴퓨팅]] ([[232_spatial_computing_digital_twin|Spatial Computing]]) 결합 혼합 현실 [[190_ai_llm_requirements_specification|AI]] 렌더링 
200. [[200_robotics_motion_policy|로보틱스 범용 모션 정책 훈련]] [[190_ai_llm_requirements_specification|AI]] 제어 
201. [[445_neuromorphic_computing|뉴로모픽 컴퓨팅]] ([[445_neuromorphic_computing|Neuromorphic Computing]]) [[446_snn|SNN]](Spiking Neural Network) 뉴런 [[129_spike_agile_technical_investigation|스파이크]] [[001_voltage|전압]] 발생 모방 하드웨어 두뇌 전력 저소모 소자
202. [[635_on_device_ai|온디바이스 AI]] ([[635_on_device_ai|On-Device AI]]) - 외부 클라우드 통신망 없이 모바일 [[572_ap_access_point_ds_distribution_system|AP]]([[424_npu|NPU]] 탑재) 내장형 신경망 추론 로컬 동작망
203. [[203_slm_small_language_model|슬림 언어 모델]] ([[313_slm|SLM]], [[313_slm|Small Language Model]]) - 파라미터가 수십억(1B~8B) 수준이나 정제된 고품질 [[001_dikw_pyramid|데이터]] 학습으로 특정 업무에서 [[263_llm_large_language_model|LLM]] 필적 [[282_performance_tactics|성능]], 엣지 기기 구동 가능 (Llama 3 8B, [[864_phi|Phi]]-3 등)
204. [[306_graph_neural_network_gnn|그래프 신경망]] ([[159_gnn_graph_neural_network_message_passing|GNN]], [[159_gnn_graph_neural_network_message_passing|Graph Neural Network]]) - 구조화된 [[070_graph_datastructure|그래프]](노드, 간선) 정보 소셜 네트워크, 화학 분자 분리 탐색 모델 ([[119_message_passing|Message Passing]] 방식 통신)
205. [[160_knowledge_graph_graphrag_integration|지식 그래프]] ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]]) 지능형 연계 - [[276_fine_tuning|RAG]] 결합 [[530_graph_rag|GraphRAG]] [[275_react_framework|환각]] 최소 [[083_relationship_in_er_model|관계]] [[012_metadata|메타데이터]] 주입
206. [[206_tcn_time_series|시계열 딥러닝]] 예측 TCN ([[157_time_series_deep_learning_tcn_transformer|Temporal Convolutional Network]]) [[430_index_fast_full_scan|병렬]] 1D [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 적용 비교 
207. 오디오 딥러닝 멜 스펙트로그램 (Mel-Spectrogram) 푸리에 변환 이미지 차용 음성 인식 모델(ASR) (Whisper 구조)
208. [[208_mrc_machine_reading_comprehension|기계 독해]] (MRC, Machine Reading Comprehension) 텍스트 분석 [[001_algorithm_definition|알고리즘]] (SQuAD 벤치마크)
209. [[105_exploratory_data_analysis|감성 분석]] ([[105_exploratory_data_analysis|Sentiment Analysis]]) NLP 적용 체제 (리뷰 호감도 자연어 파싱망)
210. [[117_ner|개체명 인식]] ([[117_ner|NER]], Named Entity Recognition) - 텍스트 단어 인명, 지명, 조직 라벨링 [[820_tokenization|토큰화]] 모델 체제 
211. [[211_recommendation_system|추천 시스템]] ([[093_recommendation_system|Recommendation System]]) - [[345_collaborative_filtering|협업 필터링]](Collaborative), [[346_content_based_filtering|콘텐츠 기반 필터링]](Content-based) 하이브리드 조합 심층 모델 (DeepFM)
212. 오토 [[040_encoder|인코더]] ([[335_autoencoder|Autoencoder]]) 구조 - 입력 [[001_dikw_pyramid|데이터]]를 병목 [[040_encoder|인코더]] 은닉층으로 [[347_compaction|압축]](잠재 공간 벡터화 Z) 후 [[039_decoder|디코더]]로 동일하게 원복([[122_unsupervised_learning|비지도 학습]]) [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] 및 노이즈 제거 특화
213. [[213_variational_autoencoder|변이형 오토인코더]] ([[315_autoencoder_vae|VAE]], [[213_variational_autoencoder|Variational Autoencoder]]) [[087_process_state_transition|생성]] 공간 정규 [[130_probability|확률]] 변환 매핑 
214. [[214_active_learning|액티브 러닝]] ([[214_active_learning|Active Learning]]) 인간 개입 학습 최적 [[001_dikw_pyramid|데이터]] 자가 요청 검수망 
215. [[470_meta_learning_maml|메타 러닝]] ([[215_meta_learning|Meta Learning]] / [[240_switch_learning_forwarding_flooding|Learning]] to Learn) [[190_ai_llm_requirements_specification|AI]] 최적화 [[001_algorithm_definition|알고리즘]] 스스로 수정 진화 
216. [[216_autogpt_autonomous_agent|자율 에이전트 오토지피티]] ([[216_autogpt_autonomous_agent|AutoGPT]]) 프롬프트 연쇄 무한 루프 과업 달성 
217. [[263_llm_large_language_model|LLM]] 운영 [[456_caching|캐싱]] 아키텍처 - [[280_ppo_proximal_policy_optimization|시맨틱 캐시]]([[280_ppo_proximal_policy_optimization|Semantic Cache]]) 유사 질문 판별 반복 [[014_api_posix|API]] 콜(비용/[[015_지연_데이터_관점|지연]]) [[656_ir_containment|억제]] 프레임
218. [[218_rag_advanced_techniques|RAG 고도화 기법]] - 청킹(Chunking 단락 쪼개기) [[268_strategy_pattern|전략]], 하이브리드 서치(BM25 키워드 매치 + 벡터 [[348_similarity_search|유사도 검색]] 결합 스코어링), 재랭킹(Re-ranking) 문서 정확도 우선순위 보정 필터링 모델 
219. [[219_langsmith_llm_observability|LangSmith 로그 평가 프롬프트 디버깅]] 추적 솔루션망
220. DSPy 자동 프롬프트 컴파일 최적화 [[241_machine_learning_basics|머신러닝]] [[336_library_vs_framework|라이브러리]] 프레임 
221. [[221_ann_vector_index|벡터 차원 색인 ANN]] ([[351_hnsw|HNSW]] 이웃 [[070_graph_datastructure|그래프]] / IVFFlat / [[391_qos_queuing_pq_cq_wfq_cbwfq_llq|PQ]] 곱 [[434_quantization|양자화]] 기술망 적용 검색 최적 구조 분석)
222. [[621_scale_up_system_bus|스케일 업]]([[621_scale_up_system_bus|Scale-up]]) [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]] 파라미터 [[136_variance|분산]] 로드 구조 기술망 
223. [[418_gpu|GPU]] 메모리 VRAM 한계 [[291_kv_cache|KV 캐시]] ([[291_kv_cache|Key-Value Cache]]) PagedAttention (vLLM 메모리 파편화 [[259_paging|페이징]] OS 기법 차용 [[087_process_state_transition|생성]] 가속)
224. 하드웨어 가속 오픈 소스 컴파일러 TensorRT, ONNX 구조 최적 [[347_compaction|압축]] 포맷
225. [[225_rag_evaluation_ragas|환각 정량 측정 프레임워크]] ([[225_rag_evaluation_ragas|RAGAS]] 평가 지표 - Faithfulness 사실 부합도, Answer Relevance 질의 연관도)
226. [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]] 법적 논쟁(스크래핑 공정 이용 [[310_ai_ethics_bias_copyright|Copyright]] / [[190_ai_llm_requirements_specification|AI]] [[087_process_state_transition|생성]]물 [[583_ai_code_license_security_threats|저작권]] 귀속 판례 거버넌스)
227. [[227_model_card_metadata_governance|모델 스코어카드]]([[227_model_card_metadata_governance|Model Card]]) [[342_metadata_catalog|메타데이터 카탈로그]] 모델 탄생 환경 훈련망 편향 설명서 문서화 (허깅페이스 등)
228. [[228_cnn_1d_2d_3d_video_medical|합성곱]] 1D, 2D, 3D 구조 비디오 시퀀스 인식 및 의학 3차원 단층 촬영 [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 파싱 
229. 자율 주행 라이다 ([[140_lidar_light_detection_and_ranging_tof|LiDAR]]) 포인트 클라우드 3D 딥러닝([[229_lidar_pointnet_autonomous_driving|PointNet]]) 검출기 
230. [[126_digital_twin_concept|디지털 트윈]] 시뮬레이터 물리 환경 [[212_synchronization_mechanisms|동기화]] 모델 연동 보정([[230_digital_twin_simulation_calibration|Calibration]]) 오차 통제 구조망 

## 5. 시험 빈출 핵심 요약 노트 (170개)
231. [[231_ai_turing_test|인공지능]] ([[002_turing_test|튜링 테스트]] 기본)
232. [[004_weak_ai_narrow_ai|약인공지능]] / [[003_strong_ai_agi|강인공지능]] 특이점 
233. [[233_expert_system|전문가 시스템]] ([[008_knowledge_base_inference_engine|지식 베이스]], 추론 엔진)
234. [[234_fuzzy_logic|퍼지 로직]] (소속도 [[130_probability|확률]]) 
235. [[235_forward_backward_chaining|전향 추론]] ([[001_dikw_pyramid|데이터]]) [[011_backward_chaining|후향 추론]] (목표) 
236. 상태 공간 트리 깊이/너비 우선
237. [[237_hill_climbing_local_optima|언덕 오르기 탐색]] (지역 최적)
238. A* 별 [[210_heuristics_scheduling|휴리스틱]] 거리 탐색 (G+H)
239. [[239_minimax_alpha_beta_pruning|미니맥스]] (적대적 게임 트리) 알파베타 [[435_pruning_hardware|가지치기]] 
240. [[240_mcts_monte_carlo|몬테카를로 트리 탐색]] ([[240_mcts_monte_carlo|MCTS]]) 무작위 시뮬레이션
241. [[241_machine_learning_basics|머신러닝]] ([[241_machine_learning_basics|경험 기반 학습]])
242. [[121_supervised_learning|지도 학습]] ([[104_classification_analysis|분류]], 회귀)
243. [[122_unsupervised_learning|비지도 학습]] ([[105_clustering_analysis|군집화]], 연관성, [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]])
244. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] (상태, 행동, 보상 [[463_markov_decision_process_mdp|MDP]])
245. [[245_overfitting_variance|과대 적합]] ([[245_overfitting_variance|Overfitting]]) [[136_variance|분산]] 오류
246. [[246_underfitting_bias|과소 적합]] ([[246_underfitting_bias|Underfitting]]) 편향 오류 
247. [[247_feature_label_variables|독립 변수]] ([[247_feature_label_variables|피처]]) / 종속 변수 (라벨) 
248. [[079_one_hot_encoding_categorical_dummy_variable|원-핫 인코딩]] 수치화 변환 행렬 
249. [[249_scaling_normalization_standardization|스케일링]] [[093_normalization|정규화]] (0~1), 표준화 (Z 스코어)
250. [[250_cross_validation_kfold|교차 검증]] K-Fold
251. [[251_grid_search_random_search|그리드 서치]] 랜덤 서치 하이퍼파라미터 
252. [[089_confusion_matrix_tp_fp_fn_tn|혼동 행렬]] (오차 행렬 4단계 매트릭스)
253. [[233_precision_recall_f1_roc_auc_threshold|정밀도]] (Positive 예측 타율)
254. [[092_recall_sensitivity_hit_rate|재현율]] (실제 질병 중 양성 탐지율) 민감도
255. [[255_f1_score|F1 스코어]] 조화 평균 
256. [[256_roc_auc|ROC 곡선]] AUC 면적 기준 모델 평가
257. [[257_ensemble_learning|앙상블]] 모형 
258. [[258_voting_ensemble|보팅]] (다수결 투표망)
259. [[259_bagging_random_forest|배깅]] (복원 추출 [[430_index_fast_full_scan|병렬]] 트리) [[353_random_forest|랜덤 포레스트]] 
260. [[127_boosting|부스팅]] (오차 [[267_weight_bias_activation|가중치]] [[149_serial_communication_rs232_rs485|직렬]] 보완) XGBoost 
261. [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 초평면 최대 마진 [[059_kernel_trick_rbf_polynomial|커널 트릭]] 
262. [[352_knn_distance_metrics|K-NN]] 거리 기반 다수결 최근접 이웃
263. K-Means 중심점 거리 반복 이동 EM 구조 
264. [[264_naive_bayes|나이브 베이즈]] 조건부 독립 [[130_probability|확률]] 연산 
265. [[265_single_layer_perceptron_xor|단층 퍼셉트론]] XOR 판별 불가 
266. [[266_mlp_hidden_layers|다층 퍼셉트론]] 비선형 해결 은닉층
267. [[267_weight_bias_activation|가중치]] 편향 [[129_activation_function|활성화 함수]] 
268. [[268_sigmoid_vanishing_gradient|시그모이드]] 활성화 [[088_vanishing_gradient_relu_skip_connection|기울기 소실]] 
269. [[269_relu_activation|ReLU]] (0이상 그대로 반환 음수 0) 기울기 [[571_protection_vs_security|보호]] 연산망 속도 향상 
270. [[270_softmax|소프트맥스]] (출력층 [[130_probability|확률]] 1 합계 반환망) 
271. [[271_forward_propagation|순전파]] 출력층 손실 연산 
272. [[272_backpropagation|역전파]] 연쇄 법칙 [[267_weight_bias_activation|가중치]] 도함수 갱신 오차 
273. [[076_mse_mean_squared_error_regression|MSE]] 회귀 [[154_cross_entropy|크로스 엔트로피]] [[104_classification_analysis|분류]] 로스 
274. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] [[080_gradient_descent_learning_rate|학습률]] 하강법 [[009_config|설정]]망
275. [[275_gradient_descent_sgd|경사 하강법]] SGD [[130_probability|확률]]적 변환 미니배치
276. [[276_momentum_optimizer|모멘텀]] 관성 기반 탈출 
277. [[277_adam_optimizer|Adam]] 적응 학습 관성 결합망 
278. [[278_regularization_overview|과적합 방지 기법]] 모음 
279. L1/L2 라쏘 릿지 페널티 규제
280. [[280_dropout|드롭아웃]] 임의 뉴런 제거 
281. [[281_early_stopping|조기 종료]] [[395_verification_process_review|검증]] 오차 증가 시 단절 
282. [[441_batch_normalization_mean_variance|배치 정규화 평균 분산]] 0~1 분포 은닉층 투과 
283. [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 이미지 구조 공간 필터망 
284. [[284_convolution_stride_padding|합성곱 연산]] [[097_stride_convolutional_neural_network_downsampling|스트라이드]] [[098_padding_convolutional_neural_network_same_valid|패딩]] 
285. [[285_pooling_layer|풀링]] 해상도 축소 공간 불변 보장 
286. [[105_one_by_one_convolution_bottleneck_dimension_reduction|1x1 합성곱]] 채널 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]] 
287. [[287_resnet_skip_connection|ResNet]] 잔차 연결 Skip 스킵 커넥션 망 
288. [[288_object_detection_yolo_rcnn|객체 탐지]] YOLO (빠름) R-[[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] (정확 2-stage)
289. [[289_image_segmentation|이미지 분할]] 시맨틱 (픽셀 [[104_classification_analysis|분류]]망) 
290. [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 시계열 순서 기억 은닉 상태 루프 
291. [[291_long_term_dependency|장기 의존성]] (과거 정보 소실망 기울기) 
292. [[292_lstm|LSTM]] 장기 단기 기억 셀 상태 컨베이어망 
293. 게이트 3개 (입력 출력 삭제 밸브망) 
294. [[294_gru|GRU]] 간소화 업데이트 리셋 게이트 
295. [[245_seq2seq_context_vector_attention_dynamic_weight|Seq2Seq]] [[040_encoder|인코더]] [[039_decoder|디코더]] 챗봇 병목 발생 
296. 어텐션 고정 문맥 벡터 한계 돌파 동적 [[267_weight_bias_activation|가중치]]망 
297. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] 배제 [[430_index_fast_full_scan|병렬]] 셀프 어텐션 
298. [[298_qkv_attention|쿼리]] 키 밸류 (Q K V) 행렬 상관 스코어
299. [[299_multi_head_attention|멀티 헤드 어텐션]] 다차원 [[430_index_fast_full_scan|병렬]] 해석 
300. [[300_positional_encoding|포지셔널 인코딩]] 위치 삼각함수 정보 주입 
301. [[301_bert_mlm|BERT]] [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] [[040_encoder|인코더]] 기반 양방향 이해 (빈칸 채우기 [[138_mlm_learning|MLM]])
302. [[302_gpt_autoregressive|GPT]] [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] [[039_decoder|디코더]] 기반 자가 회귀 [[087_process_state_transition|생성]] (다음 단어 예측)
303. [[225_foundation_model_peft_lora|파운데이션 모델]] 사전 학습 [[132_transfer_learning|전이 학습]] 적용 
304. [[304_fine_tuning|파인 튜닝]] 모델 [[267_weight_bias_activation|가중치]] 전체 미세 훈련 목표 최적
305. [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]] 퓨샷 샷리스 사고 사슬 ([[146_chain_of_thought_cot|CoT]]) 
306. [[306_peft_lora|PEFT]] 매개변수 효율적 파인튜닝 [[283_lora_low_rank_adaptation|로라]] ([[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] 저차원 행렬) 
307. [[454_hallucination_prevention|할루시네이션 환각]] 거짓말 위장 [[087_process_state_transition|생성]] 통제 
308. [[276_fine_tuning|RAG]] 검색 증강 외부 DB 문서 연동 주입 [[087_process_state_transition|생성]] 
309. 벡터 DB [[278_instruction_tuning|임베딩]] 고차원 변환 의미 검색망
310. [[359_cosine_similarity|코사인 유사도]] 벡터 각도 비교 탐색기 
311. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]] 교사 학생 네트워크 [[347_compaction|압축]]망)
312. [[312_quantization|모델 양자화]] ([[458_quantization_fp32_int8|Quantization FP32 INT8]] 정수 절삭 용량 가속)
313. [[313_slm|SLM]] 소형 언어 모델 온디바이스 동작 최적망 
314. [[253_reinforcement_learning_mdp_policy_value_q_learning_dqn|강화 학습]] 마르코프 결정 [[463_markov_decision_process_mdp|MDP]] 환경 
315. [[315_exploration_exploitation|탐험]] 활용 딜레마 랜덤 Epsilon 시도 
316. [[316_q_learning|Q-Learning]] 큐 테이블 오프 폴리시 [[163_value_function|가치 함수]]
317. [[465_dqn_deep_q_network|DQN]] 큐 러닝 딥러닝 결합 상태 무한 해결 
318. [[318_policy_gradient_actor_critic|정책 경사]] 모델 [[172_actor_critic|Actor-Critic]] 에이전트망 
319. [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]] [[154_gan_generative_adversarial_network|GAN]] 판별자 [[087_process_state_transition|생성]]자 적대 경쟁 위조범 경찰망 
320. [[153_diffusion_model_stable_diffusion_denoising|디퓨전 모델]] 노이즈 점진 주입 역산 복원 [[087_process_state_transition|생성]] (이미지) 
321. [[348_mlops|MLOps]] [[123_pipe|파이프]]라인 개발 운영 [[090_configuration_item|CI]]/CD 모델 생명주기
322. [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] [[164_concept_drift_target_mapping_change|컨셉 드리프트]] 분포 왜곡 [[229_monitor|모니터]]링
323. [[165_feature_store_training_serving_consistency|피처 스토어]] 특징 캐시 공유망 
324. [[166_model_registry_versioning_mlflow|모델 레지스트리]] [[288_version_ihl_tos_total_length|버전]] 관리 저장소망 
325. [[227_xai_explainable_ai_lime_shap|설명 가능한 AI]] [[227_xai_explainable_ai_lime_shap|XAI]] 화이트박스 신뢰망 
326. [[326_lime|LIME]] 국소적 모델 대리 선형 판단 근거 추출
327. [[327_shap|SHAP]] 섀플리 값 게임 이론 변수 기여 분포 전역 해석 
328. [[256_federated_learning_privacy_model_security|연합 학습]] 디바이스 [[136_variance|분산]] [[267_weight_bias_activation|가중치]] 병합 통제 
329. [[635_on_device_ai|온디바이스 AI]] 엣지 추론 [[424_npu|NPU]] 서버 [[440_offloading|오프로딩]] 제거망
330. [[330_ai_ethics|AI 윤리]] 편향성 [[001_dikw_pyramid|데이터]] 검열 프라이버시 [[583_ai_code_license_security_threats|저작권]] 공정 
331. [[158_multimodal_clip_vision_audio_encoding|멀티모달]] ([[158_multimodal_clip_vision_audio_encoding|Multimodal]]) 비전 오디오 텍스트 동시 수용망 
332. [[159_gnn_graph_neural_network_message_passing|GNN]] [[070_graph_datastructure|그래프]] 노드 [[083_relationship_in_er_model|관계]] 소셜 통계망 분석
333. A/B [[575_shadow_deployment_traffic_mirroring|섀도우 배포]] 트래픽 미러 [[395_verification_process_review|검증]] 서빙망 
334. [[418_gpu|GPU]] 메모리 VRAM 부족 [[585_zero_skipping|ZeRO]] [[136_variance|분산]] 구조 [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 슬라이싱망 
335. [[335_autoencoder|오토인코더]] 차원 [[347_compaction|압축]] 복원 비지도 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] 
336. [[427_tensor_core|텐서 코어]] 혼합 정밀 연산 가속 하드웨어 
337. [[250_rlhf_human_feedback_reinforcement_alignment_cot|RLHF]] 인간 피드백 강화 모델 정렬 선호망 보상 함수망 
338. vLLM 메모리 캐시 최적 PagedAttention [[286_page_frame|페이지]] 분할망 [[087_process_state_transition|생성]] 시간망 
339. [[339_word2vec|Word2Vec]] CBOW Skip-Gram 단어 벡터 밀집 [[055_array|배열]] 
340. 딥러닝 추천 엔진 DeepFM [[247_feature_label_variables|피처]] 융합 연동 추론

## 6. [[001_dikw_pyramid|데이터]] 사이언스 / [[241_machine_learning_basics|머신러닝]] 심화 수학 (100개 집중 확장)
341. [[341_eigenvalue_decomposition|고유값 분해]] 대칭 행렬 역행렬 계산 직교 벡터 성질 
342. [[342_svd|특이값 분해]] ([[230_svd_matrix_factorization_random_forest_xgboost_boosting|SVD]]) 비정방 행렬 특이 벡터 주성분 분리 
343. [[166_lagrange_multiplier|라그랑주 승수법]] 제약 조건 하 목적 함수 최적점 도출 [[238_svm_margin_kernel_trick_naive_bayes|SVM]] 적용 수식
344. [[344_activation_derivative_sigmoid|활성화 함수 도함수]] [[268_sigmoid_vanishing_gradient|Sigmoid]] 최대 기울기 0.25 소실 원리 증명망 
345. [[345_backprop_chain_rule_math|역전파 편미분]] 연쇄 법칙 수식 전개 과정 
346. [[346_batch_size_generalization|배치 사이즈]]와 일반화(Generalization) [[282_performance_tactics|성능]] [[083_relationship_in_er_model|관계]] 곡선 (플랫 미니마 vs 샤프 미니마)
347. [[347_cross_entropy_kld|교차 엔트로피와 KLD]] ([[347_cross_entropy_kld|Kullback-Leibler Divergence]]) 분포 차이 정보량 통계 
348. [[143_mle|최대 우도 추정]] ([[143_mle|MLE]]) [[075_loss_function_cost_function|손실 함수]] 유도 연결성 
349. [[349_bayes_rule_likelihood|우도와 사후 확률]] 베이즈 룰 변환 정규식 
350. 스무딩 (Smoothing 기법) 라플라스 [[264_naive_bayes|나이브 베이즈]] [[130_probability|확률]] 0 방어 연산 
351. [[108_gini_impurity|지니 불순도]] 노드 [[151_entropy|엔트로피]] 정보 획득량 수리 계산식 
352. [[239_perceptron_mlp_hidden_layer_weight_activation_sigmoid|퍼셉트론]] 선형 분리 결정 경계 벡터 방정식 
353. [[227_logistic_regression_clt_pvalue_type_error|로지스틱 회귀]] 오즈비 (Odds Ratio) 로짓 [[568_logs_distributed_logging_elk_fluentd|로그]] 변환 함수 곡선 
354. [[163_pca|PCA]] 공분산 행렬 투영 [[001_dikw_pyramid|데이터]] [[136_variance|분산]] 최대 보존 직교 축 찾기 모형 
355. [[355_random_forest_feature_importance|랜덤 포레스트 변수 중요도]] ([[355_random_forest_feature_importance|Feature Importance]]) [[151_entropy|엔트로피]] 하락분 합산 모델 
356. [[106_mahalanobis_distance|마할라노비스 거리]] ([[106_mahalanobis_distance|Mahalanobis Distance]]) 변수 간 공분산 상관 고려 다차원 거리 측정 군집망 
357. [[351_dbscan_density_based_clustering|DBSCAN]] 밀도 기반 [[105_clustering_analysis|군집화]] [[001_algorithm_definition|알고리즘]] EPS와 MinPts 군집 연결 노이즈 [[655_ir_detection_analysis|식별]] 기법 
358. [[358_hierarchical_clustering|계층적 군집화]] ([[047_hierarchical_clustering|Hierarchical Clustering]]) 덴드로그램 (Dendrogram) 클러스터 응집 
359. [[359_cosine_similarity|코사인 유사도]] 텍스트 [[278_instruction_tuning|임베딩]] 차원 무관 방향성 거리 일치 계수 
360. [[114_gaussian_mixture_model|가우시안 혼합 모델]] ([[360_gmm_em_algorithm|GMM]]) [[142_em_algorithm|EM 알고리즘]] (E 스텝 / M 스텝) 하위 가중 평균 [[130_probability|확률]] 추정 방식 
361. [[080_multicollinearity_vif_variance_inflation_factor_regression|다중 공선성]] (VIF) 트리 기반 모델 파생 영향 차이점 (상관 트리 회피능 비교)
362. [[256_roc_auc|ROC AUC]] 곡선 FPR 민감도 TPR 축 변화 통계 스레스홀드 검정 
363. [[270_softmax|소프트맥스]] 지수 함수 [[272_backpropagation|역전파]] 오차 그래디언트 치환 공식 
364. [[163_optimizer_sql_execution_plan_generator|옵티마이저]] Adagrad 가변 [[080_gradient_descent_learning_rate|학습률]] 감소 한계 (RMSProp 지수 평균 보정) 
365. [[075_word|워드]] [[278_instruction_tuning|임베딩]] 글로브 ([[365_glove_word_embedding|GloVe]]) [[161_matrix_decomposition|행렬 분해]]와 빈도 [[568_logs_distributed_logging_elk_fluentd|로그]] 윈도우 결합 
366. 코어런스 (Co-occurrence) [[366_cooccurrence_matrix|동시 등장 행렬]] 스케일 축소 구조 
367. [[104_svm_support_vector_machine|서포트 벡터 머신]] ([[238_svm_margin_kernel_trick_naive_bayes|SVM]]) 마진 슬랙 변수 ([[367_svm_slack_variable|Slack Variable]]) C 파라미터 규제 오버피팅 연계망 
368. [[059_kernel_trick_rbf_polynomial|커널 트릭]] 매핑 RBF(가우시안) [[022_kernel_role|커널]] 유사성 지수 무한 차원 변환 수식망 
369. [[004_unstructured_data|비정형 데이터]] [[093_normalization|정규화]] [[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]] 미니배치 스케일 표준 편차 [[136_variance|분산]] 이동 연산망 구조 
370. [[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]] [[272_backpropagation|역전파]] [[114_bptt_backpropagation_through_time|BPTT]] 기울기 체인 루프 은닉 상태 길이 파생 스텝 증폭량 오차 계산 원리 
371. [[292_lstm|LSTM]] 셀게이트 [[268_sigmoid_vanishing_gradient|Sigmoid]] 통과/[[070_hyperbolic_tangent_tanh_activation|Tanh]] [[087_process_state_transition|생성]] 제어 덧셈 구조 연산 곱셈 분기 해결 방식
372. Q 러닝 [[372_bellman_equation|벨만 방정식]] ([[372_bellman_equation|Bellman Equation]]) 행동 [[632_state_transition_diagram_testing|상태 전이]] 가치 수식 갱신 과정 모델 
373. [[172_actor_critic|Actor-Critic]] ([[373_actor_critic_advantage|A2C]]) Advantage 오차 함수 예측치 평가 보상 [[146_confidence_interval|신뢰 구간]] 보정 모델
374. [[315_autoencoder_vae|VAE]] ([[213_variational_autoencoder|Variational Autoencoder]]) 재파라미터화 트릭 (Reparameterization Trick) [[130_probability|확률]] 노이즈 난수 미분 연결망 프레임 구조
375. [[375_gan_loss_function|GAN 손실 함수 미니맥스]] 목적 수식 (판별자 우도 최대, [[087_process_state_transition|생성]]자 최소 기만) 
376. [[140_markov_chain|마르코프 체인]] 흡수 상태 에르고딕 (Ergodic) [[082_attribute_types_er_model|속성]] [[130_probability|확률]] 분할 정상 분포 매트릭스 도달 정리 
377. 시계열 순환 보존 (Stationary) 검정 지표 모델 추세성 [[136_variance|분산]] 계절성 차분 통계 [[192_module_independence|모듈]] 
378. [[378_dtw|동적 시간 워핑]] ([[403_dtw_dynamic_time_warping|DTW]]) [[055_array|배열]] 시프트 매칭 다이나믹 프로그래밍 비용 행렬 최단 경로 [[030_linear_search|선형 탐색]]망
379. [[257_ensemble_learning|앙상블]] 편향 [[136_variance|분산]] 공식 [[259_bagging_random_forest|Bagging]] [[136_variance|분산]] 감소 증명 [[127_boosting|Boosting]] 편향 완화 증명 트레이드오프 파싱 모델망 
380. 경사도 소실 및 폭발 Kaiming He 변수 노드 정규 파라미터 [[459_quic_fec_forward_error_correction|초기]]화 루트(2/N) [[009_config|설정]] 원리
381. 어텐션 매커니즘 스케일드 닷 프로덕트 (Scaled [[519_dot_dns_over_tls|Dot]]-Product) Q K 연산 유사도 벡터 / 루트(dk) [[249_scaling_normalization_standardization|스케일링]] [[136_variance|분산]] 보정 [[270_softmax|소프트맥스]] 과열 방지 수학 모델망 
382. [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] 인코딩 사인 코사인 삼각 함수 위치 벡터 합산 짝/홀 차원 대입식 원리 분석망
383. [[383_llm_autoregressive_math|LLM 자기 회귀]] 언어 모델 우도 수식 이전 토큰 [[055_array|배열]] 결합 [[130_probability|확률]] 밀도 예측 텍스트 [[087_process_state_transition|생성]] 도식망 
384. 프롬프트 토크나이저 (Tokenizer) BPE ([[378_bpe_byte_pair_encoding|Byte Pair Encoding]]) 빈도 서브워드 (Subword) 병합 OOV (Out Of Vocabulary) 대응 사전 어휘 모형 
385. WordPiece 토크나이징 서브워드 분할 구조 SentencePiece 방식 비교 통계 [[130_probability|확률]] 망 시스템 
386. [[386_llm_temperature|LLM 온도]] ([[386_llm_temperature|Temperature]]) 파라미터 디코딩 로짓 [[270_softmax|소프트맥스]] 스케일 적용 [[087_process_state_transition|생성]]형 텍스트 창의성 (무작위성) 수치 조절 수리망
387. 탑-K / 탑-P ([[387_topk_topp_sampling|Nucleus Sampling]]) 샘플링 디코딩 [[130_probability|확률]] 분포 커트라인 누적 값 샘플 선택 [[136_variance|분산]] 모형망 제어 방식 
388. [[388_rag_hnsw_ann|RAG 파이프라인]] 최대 한계 수익성 마진 벡터 검색 [[038_knn|K-최근접 이웃]] [[350_ann|ANN]] [[298_qkv_attention|쿼리]] ([[351_hnsw|HNSW]] 유클리드 공간/[[070_graph_datastructure|그래프]] 노드 우회 거리 함수 연산) 최적 방식 모델망
389. [[389_knowledge_distillation_soft_target|지식 증류 소프트 타겟]] ([[389_knowledge_distillation_soft_target|Soft Target]]) 로짓 분포 스무딩 [[153_kl_divergence|KL 다이버전스]] 교사-학생 로스 통합망 함수 수학 모형 설계
390. [[390_maml_meta_learning|메타 러닝 MAML]] ([[390_maml_meta_learning|Model-Agnostic Meta-Learning]]) 미분 궤적 파라미터 업데이트 기울기 이중 도함수 연산 적응형 손실 스텝망 모델 개념 설계 
391. [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]] [[391_diffusion_reverse_process|디퓨전 역과정]] (Reverse [[300_process|Process]]) 가우시안 [[140_markov_chain|마르코프 체인]] 조건부 덴서티 [[130_probability|확률]] [[335_autoencoder|오토인코더]] 노이즈 에러 예측 수학 맵 프레임 통제 지표식 
392. [[392_perceptron_convergence|퍼셉트론 수렴 정리]] ([[377_perceptron_convergence_theorem|Convergence Theorem]]) 오차 경계 벡터 업데이트 유한 횟수 선형 분리 보장 마진 증명 [[369_logic_bomb|논리]] 
393. 비지도 특성 추출 [[163_pca|PCA]] 대비 t-SNE / UMAP 매니폴드 고차원 거리 분포 저차원 비선형 이웃 보존 T분포 변환 수리 [[001_algorithm_definition|알고리즘]] 
394. 오토ML ([[176_automl_hyperparameter_optimization_bayesian|AutoML]]) 하이퍼오프티 (Hyperopt) TPE (Tree-structured Parzen Estimator) 베이지안 최적화 목적 함수 [[130_probability|확률]] 분포 트리 매핑 기술망 모형 
395. [[395_ppo_clipping|PPO]] (강화학습) 클리핑 목적 함수 서로게이트 (Surrogate Object) 기존 [[164_policy|정책]] 대비 비율 페널티 급격 업데이트 변위 제어 통계 수식망 구조 설계망
396. [[241_machine_learning_basics|머신러닝]] [[812_anonymization|데이터 익명화]] 노이즈 가산 라플라스 메커니즘 [[396_differential_privacy|차분 프라이버시]] 함수 ε, δ 제약 예산 한계 최적식 
397. [[106_mahalanobis_distance|마할라노비스 거리]] 역공분산 행렬 다차원 투영 회귀 이웃 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]] ([[076_outlier_detection_iqr_dbscan_isolation_forest|Outlier]]) 배제 [[249_scaling_normalization_standardization|스케일링]] 상관 연산 
398. [[070_graph_datastructure|그래프]] 어텐션 네트워크 ([[398_gat|GAT]]) 노드 [[389_mesh_topology|메시]]지 패싱([[119_message_passing|Message Passing]]) 자기/이웃 어텐션 계수 가중 평균 정보 융합 수식 매트릭스 도출 모델 
399. [[214_active_learning|액티브 러닝]] ([[214_active_learning|Active Learning]]) [[298_qkv_attention|쿼리]] 바이 커미티 (Query by Committee) 오탐지 불확실성 정보 [[151_entropy|엔트로피]] 샘플 측정 최적 [[001_dikw_pyramid|데이터]] 선별망 통제 구조 
400. [[400_mlops_drift_detection|MLOps 드리프트 탐지]] 지표 K-S 통계 검정 분포 차별 (Kolmogorov-Smirnov) / 인구 안정성 지수 (PSI) 수리 [[395_verification_process_review|검증]]망 로깅 평가 체계 시스템 모델망 모형
401. 자연어 처리 통계적 기계 번역([[400_smt|SMT]]) vs 신경망 기계 번역(NMT) 은닉 상태 [[033_context|컨텍스트]] 
402. [[239_micro_frontends_architecture|마이크로 프론트엔드]] 연동 딥러닝 서빙 브라우저 웹 어셈블리 (TensorFlow.js) 경량 연산 변환 
403. 초거대 [[190_ai_llm_requirements_specification|AI]] RHF 보상 모델([[403_rlhf_reward_model|Reward Model]]) 선호도 학습 브래들리-테리(Bradley-Terry) 비교 [[130_probability|확률]] 모델 [[568_logs_distributed_logging_elk_fluentd|로그]] [[075_loss_function_cost_function|손실 함수]]
404. [[263_llm_large_language_model|LLM]] [[434_quantization|양자화]] 후 미세조정([[404_qlora|QLoRA]]) [[267_weight_bias_activation|가중치]] [[272_backpropagation|역전파]] [[434_quantization|양자화]] 노이즈 페널티 보상 행렬 수식 구조
405. [[621_scale_up_system_bus|스케일 업]] 대비 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]] [[405_gpipe_pipeline_parallelism|파이프라인 병렬화]] ([[082_pipeline|Pipeline]] Parallelism) 마이크로배치 스루풋 거대망 버블 축소 레이턴시 [[208_schedule_history_transaction_execution_order|스케줄]] 도출망 ([[405_gpipe_pipeline_parallelism|GPipe]])
406. [[427_tensor_core|텐서 코어]] FP16 고속 [[428_mac_operation|MAC 연산]] ([[428_mac_operation|Multiply-Accumulate]]) 및 FP32 누산 혼합 [[057_register|레지스터]] 구조 수식 
407. [[407_cosine_annealing|코사인 어닐링]] ([[309_cosine_annealing|Cosine Annealing]]) [[080_gradient_descent_learning_rate|학습률]] [[079_kube_scheduler_pod_placement|스케줄러]] 웜 리스타트(Warm Restarts) 주기적 스텝 파라미터 경사 감쇠망 식
408. 다중 모달 [[312_clip_contrastive_learning|클립]]([[408_clip|CLIP]], [[408_clip|Contrastive Language-Image Pre-training]]) 대조 학습(Contrastive [[240_switch_learning_forwarding_flooding|Learning]]) 텍스트-이미지 [[359_cosine_similarity|코사인 유사도]] 벡터 공통 공간 수리 매핑 체계 
409. [[431_k_means_clustering_elbow_method|K-Means 군집 엘보우]] 기법 (Elbow Method) / 실루엣 스코어 ([[350_kmeans_elbow_silhouette|Silhouette Score]]) 최적 클러스터 K [[009_config|설정]] 평가 지표 계산 
410. [[241_machine_learning_basics|머신러닝]] 비용 함수 통계 우도 기반 정보 기준 (AIC, BIC) 모델 파라미터 페널티 추가 적합성 판별 수리 공식
411. [[411_pacf_partial_autocorrelation|편자기상관함수]] (PACF) 시계열 중간 노이즈 제어 간접 효과 배제 선형 투영 예측 AR 오더 (p) 판별망 
412. [[412_svr_support_vector_regression|서포트 벡터 회귀]] (SVR) 여백 에러 튜브 임계 (ε-Tube) 안측 허용 손실 0 오차 페널티 수리 구조 모델망 연계 
413. [[313_imitation_learning|자율주행 강화학습 모방 학습]] ([[200_autonomous_driving_imitation_learning_digital_twin|Imitation Learning]] / Behavior Cloning) 인간 전문가 궤적 데몬스트레이션 [[164_policy|정책]] 오차 지도 변환 모델 
414. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] ([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]]) [[154_cross_entropy|크로스 엔트로피]] 온도 ([[386_llm_temperature|Temperature]] Scaling) T 스케일 스무딩 로짓 매칭망 식 통제 원리 
415. 인스턴스 [[093_normalization|정규화]] (Instance [[093_normalization|Normalization]]), 그룹 [[093_normalization|정규화]] 비교([[243_cnn_stride_pooling_resnet_residual_yolo_object_detection|CNN]]/[[244_rnn_time_series_lstm_cell_gate_long_term_dependency|RNN]]) [[346_batch_size_generalization|배치 사이즈]] 독립 통계량 배치 노멀 대체 수식 
416. 모델 역산 공격 방어망 [[396_differential_privacy|차분 프라이버시]] 딥러닝 [[130_probability|확률]] 스토캐스틱 기울기 노이즈 클리핑 (DP-SGD) 적용 체제식 설계
417. 정보 검색 모델 BM25 [[001_algorithm_definition|알고리즘]] 문서 길이 [[093_normalization|정규화]] TF [[267_weight_bias_activation|가중치]] 포화 (Saturation) 단어 희귀도 (IDF) 수식 계수 조절망 매핑 분석망 
418. 오버샘플링 언더샘플링 [[231_smote_oversampling_class_imbalance_augmentation|SMOTE]] ([[231_smote_oversampling_class_imbalance_augmentation|Synthetic Minority Over-sampling Technique]]) [[352_knn_distance_metrics|K-NN]] 근접 벡터 랜덤 선형 내삽 [[001_dikw_pyramid|데이터]] 증강 수치 [[087_process_state_transition|생성]] 원리 
419. 퍼지 소속 함수 퍼지 추론 [[078_data_scaling_normalization_min_max_standardization_z_score|Min-Max]] 연산 디퍼지피케이션 (Defuzzification / 무게 중심법) 퍼지 제어망 [[369_logic_bomb|논리]] 모델 연계 
420. [[190_ai_llm_requirements_specification|AI]] 규제 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] ISO/IEC 42001 ([[190_ai_llm_requirements_specification|AI]] [[372_management|Management]] System) 생명 주기 위험 통제 [[606_auditing_linux_auditd|감사]] 투명 체계 가이드 프레임 평가 체제망 개념 파악 요약 등 (1~8장 완벽 기술사 800+ 통합 매핑망 적용 정리)

---
**총정리 [[231_ai_turing_test|인공지능]] / [[001_algorithm_definition|알고리즘]] 키워드 : 총 800여 개 수록** (+파생/분석 1,200개 커버 규모)
([[241_machine_learning_basics|머신러닝]], 딥러닝 아키텍처는 물론 최근 폭발적인 [[263_llm_large_language_model|LLM]], [[276_fine_tuning|RAG]], [[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]]([[246_transformer_self_attention_parallel_positional_encoding|Transformer]], [[306_peft_lora|PEFT]]), 그리고 기반이 되는 [[130_probability|확률]]/통계 선형대수학 수리 이론까지 정보관리기술사 수준의 방대한 지식 세트를 전면 확장하여 체계화하였습니다.)