---
title: 183. 하이퍼파라미터 오토튜닝과 NAS (AutoML)
date: '2026-05-06'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[176_automl_hyperparameter_optimization_bayesian|AutoML]] ([[176_automl_hyperparameter_optimization_bayesian|Automated Machine Learning]])은 [[080_gradient_descent_learning_rate|학습률]], 배치 크기, [[093_normalization|정규화]] 계수 같은 HPO (Hyperparameter Optimization)와 경우에 따라 [[492_nas_network_attached_storage|NAS]] (Neural [[319_architecture|Architecture]] Search)까지 자동화해, 모델 설계 공간을 체계적으로 탐색하는 최적화 프레임워크다.
> 2. **가치**: 사람의 감과 반복 실험에 의존하던 튜닝을 예산 제한, [[281_early_stopping|조기 종료]], [[130_probability|확률]]적 탐색으로 바꾸어 정확도·[[015_지연_데이터_관점|지연]]시간·메모리 조건을 함께 만족하는 후보를 빠르게 찾을 수 있다.
> 3. **판단 포인트**: 실무에서는 [[395_verification_process_review|검증]]된 기본 모델 위에 HPO부터 적용하고, NAS는 아키텍처 자체가 [[282_performance_tactics|성능]]·[[015_지연_데이터_관점|지연]]시간을 결정하는 문제에서만 제한된 탐색 공간과 [[136_variance|분산]] 인프라를 갖춘 뒤 도입해야 한다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델의 품질은 파라미터(Parameter)만으로 결정되지 않는다. [[080_gradient_descent_learning_rate|학습률]], [[163_optimizer_sql_execution_plan_generator|옵티마이저]], 배치 크기, [[093_normalization|정규화]] 강도, 레이어 폭처럼 사람이 사전에 정하는 선택들도 수렴 속도와 일반화 [[282_performance_tactics|성능]]을 크게 바꾼다. 이 값들은 학습 도중 스스로 업데이트되는 [[267_weight_bias_activation|가중치]]와 달리 사람이 정해야 하므로, 전통적으로는 경험 많은 엔지니어의 반복 실험에 의존했다.

문제는 탐색 공간이 너무 빨리 커진다는 데 있다. [[080_gradient_descent_learning_rate|학습률]] 후보 5개, 배치 크기 4개, [[163_optimizer_sql_execution_plan_generator|옵티마이저]] 3개, [[280_dropout|드롭아웃]] 4개만 잡아도 조합은 240개가 된다. 여기에 [[001_dikw_pyramid|데이터]] 증강, [[079_kube_scheduler_pod_placement|스케줄러]], 아키텍처 깊이까지 포함하면 수작업 탐색은 금방 예산과 시간을 초과한다. 특히 모델을 한 번 학습하는 데 수시간에서 수일이 걸리는 환경에서는 "조금씩 바꿔 보자"는 접근 자체가 비효율적이다.

그래서 AutoML은 모델 개발을 감이 아니라 탐색 문제로 바꾼다. 좋은 AutoML의 핵심은 단순히 많은 실험을 돌리는 것이 아니라, 제한된 계산 자원 안에서 어떤 후보를 먼저 시도하고, 어떤 후보를 빨리 포기하며, 어떤 후보를 끝까지 키울지 체계적으로 결정하는 데 있다.

- **📢 섹션 요약 비유**: AutoML은 요리사가 간을 한 숟갈씩 바꿔 가며 끝없이 맛보는 대신, 제한된 재료 안에서 가장 가능성 높은 레시피부터 골라 시험해 보는 주방 실험 관리자와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[176_automl_hyperparameter_optimization_bayesian|AutoML]] [[123_pipe|파이프]]라인은 보통 다섯 요소로 구성된다. 첫째, 무엇을 바꿀지 정의하는 탐색 공간(Search Space). 둘째, 다음 후보를 제안하는 탐색기(Searcher). 셋째, 어떤 후보를 언제 중단하거나 승격할지 정하는 [[079_kube_scheduler_pod_placement|스케줄러]](Scheduler). 넷째, 실제 학습과 [[395_verification_process_review|검증]]을 수행하는 실험 워커. 다섯째, [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 [[075_artifact_management_nexus_docker_registry|아티팩트]]를 남기는 추적 저장소다. 이 다섯 가지가 연결돼야 AutoML이 "자동 반복 실행"이 아니라 "예산 제약하의 최적화 루프"가 된다.

| 구성 요소 | 역할 | 핵심 판단 포인트 |
| :--- | :--- | :--- |
| 탐색 공간 | 바꿀 변수의 범위와 형식 정의 | 넓을수록 유연하지만 계산비 폭증 |
| 탐색기 | 다음 후보 제안 | Random, Bayesian, Evolutionary 등 선택 |
| [[079_kube_scheduler_pod_placement|스케줄러]] | 실험 자원 배분과 [[281_early_stopping|조기 종료]] | [[281_early_stopping|Early Stopping]], Hyperband, ASHA 활용 |
| 평가기 | 학습·[[395_verification_process_review|검증]]·추론 지표 산출 | 정확도만이 아니라 [[141_latency|latency]], memory도 반영 |
| 추적 저장소 | 실험 결과와 모델 [[288_version_ihl_tos_total_length|버전]] 보관 | 재현성·비교·승격 판단의 근거 |

HPO는 주로 숫자와 범주형 [[009_config|설정]]을 탐색한다. 반면 NAS는 블록 종류, 깊이, 너비, skip connection, 연산자 선택처럼 모델 구조 자체를 탐색 공간에 넣는다. 따라서 NAS는 HPO보다 더 넓은 공간을 다루고, 단일 실험 비용도 훨씬 커지는 경향이 있다. 그래서 실제 AutoML은 완전 탐색보다 Bayesian Optimization, Evolutionary Search, ASHA (Asynchronous Successive [[062_bitcoin_halving_supply_shock|Halving]] [[001_algorithm_definition|Algorithm]]), Hyperband 같은 "유망 후보에 자원을 더 주는" [[268_strategy_pattern|전략]]을 쓴다.

아래 그림은 현대 AutoML의 공통 실행 루프를 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ AutoML search loop                                                  │
├──────────────────────────────────────────────────────────────────────┤
│ Search space                                                        │
│  - HPO: lr, batch, optimizer, dropout                               │
│  - NAS: depth, width, block, skip connection                        │
│         │                                                            │
│         ▼                                                            │
│ Searcher (random / Bayesian / evolutionary)                          │
│         │ propose candidate                                           │
│         ▼                                                            │
│ Scheduler (ASHA / Hyperband / queue)                                 │
│         │ launch trials on workers                                    │
│         ▼                                                            │
│ Train + validate -> metric + cost + latency                          │
│         │                                                            │
│         ├─ poor early signal -> stop early                           │
│         └─ promising trial  -> continue / promote                    │
│         ▼                                                            │
│ Tracker / registry -> best config or architecture                    │
└──────────────────────────────────────────────────────────────────────┘
```

여기서 중요한 점은 AutoML이 단일 목표만 다루지 않는다는 것이다. 실무에서는 정확도 1점보다 추론 [[015_지연_데이터_관점|지연]]시간 20밀리초(ms), 메모리 200메가바이트(MB), [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]]) 비용 상한 같은 제약이 더 중요할 때가 많다. 그래서 좋은 AutoML은 "가장 높은 점수"가 아니라 **예산과 제약을 만족하는 최적점**을 찾는 방향으로 설계된다.

- **📢 섹션 요약 비유**: AutoML은 경주마를 많이 출전시키는 것이 아니라, 초반 기록이 느린 말은 빨리 제외하고 끝까지 달릴 말에게만 먹이와 트랙 시간을 더 주는 대회 운영과 같다.

---

## Ⅲ. 비교 및 연결

AutoML이라는 이름 아래에서도 HPO와 NAS는 역할이 다르다. HPO는 "같은 모델 가족 안에서 최적 [[009_config|설정]]을 찾는 일"이고, NAS는 "어떤 모델 가족을 쓸지까지 함께 찾는 일"이다. 따라서 둘을 같은 비용과 기대효과로 보면 안 된다.

| 비교 축 | HPO | [[492_nas_network_attached_storage|NAS]] |
| :--- | :--- | :--- |
| 주 탐색 대상 | [[080_gradient_descent_learning_rate|학습률]], 배치, [[093_normalization|정규화]], [[163_optimizer_sql_execution_plan_generator|옵티마이저]] | 블록 구조, 깊이, 너비, 연결 방식 |
| 계산 비용 | 중간 | 높음~매우 높음 |
| 일반적 실무성 | 높음 | 제한적 |
| 가장 큰 효과 | 수렴 안정화, 일반화 향상 | 정확도-[[015_지연_데이터_관점|지연]]시간 구조 최적화 |
| 대표 적용 상황 | [[395_verification_process_review|검증]]된 Backbone 위 [[133_fine_tuning|미세 조정]] | 온디바이스 제약, 신규 구조 탐색 |
| 주요 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] | 탐색 공간 과대설계, [[001_dikw_pyramid|데이터]] 누수 | 비용 폭증, 재현성 저하, 운영 복잡성 |

연결 관점에서는 182번의 [[136_variance|분산]] 학습 인프라와도 이어진다. AutoML은 혼자 존재하지 않고, Ray 같은 [[136_variance|분산]] 실행 엔진이나 [[205_kubernetes_container_orchestration|Kubernetes]] 기반 워커 [[073_container_orchestration_tools|오케스트레이션]] 위에서 돌아가며, [[180_mlflow|MLflow]] 같은 실험 추적 체계가 있어야 결과를 의미 있게 비교할 수 있다. 즉 AutoML이 "무엇을 시험할지"를 결정한다면, [[136_variance|분산]] 인프라는 "어디서 [[430_index_fast_full_scan|병렬]]로 실행할지", [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]])는 "무엇을 남기고 승격할지"를 담당한다.

또한 수작업 튜닝과의 경계도 분명히 해야 한다. 좋은 팀은 [[176_automl_hyperparameter_optimization_bayesian|AutoML]] 이전에 이미 강한 기본 모델과 합리적 [[459_quic_fec_forward_error_correction|초기]] 범위를 갖고 있다. AutoML은 그 이후의 반복을 줄여 주는 가속기이지, 엉성한 [[001_dikw_pyramid|데이터]]셋과 불명확한 목표를 마법처럼 해결해 주는 도구가 아니다.

- **📢 섹션 요약 비유**: HPO가 이미 있는 자동차의 타이어 압력과 기어비를 조정하는 일이라면, NAS는 차체 모양과 엔진 배치까지 새로 설계하는 일이라서 비용과 책임이 훨씬 크다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 먼저 해야 할 일은 "무엇을 자동화할지"보다 "무엇은 고정할지"를 정하는 것이다. [[001_dikw_pyramid|데이터]] 분할 방식, 평가지표, 재현 가능한 학습 스크립트, 기본 모델이 먼저 안정되어야 탐색 결과가 의미를 가진다. 이 바닥이 흔들리면 AutoML은 좋은 후보를 찾는 것이 아니라, 우연히 점수가 높게 나온 실험을 많이 만드는 장치가 된다.

| 실무 상황 | 권장 방향 | 이유 |
| :--- | :--- | :--- |
| 표준 모델이 이미 강한 문제 | HPO 우선 | 가장 낮은 비용으로 [[282_performance_tactics|성능]] 개선 가능 |
| 엣지 디바이스 추론 제약이 큰 비전 모델 | 제약 기반 [[492_nas_network_attached_storage|NAS]] 검토 | [[141_latency|latency]], memory, accuracy를 함께 맞춰야 함 |
| [[263_llm_large_language_model|LLM]] ([[263_llm_large_language_model|Large Language Model]]) 미세조정 | HPO 중심 | [[080_gradient_descent_learning_rate|학습률]], [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] ([[145_peft_lora_low_rank_adaptation|Low-Rank Adaptation]]) rank, batch, sequence length가 효과적 |
| [[001_dikw_pyramid|데이터]]도 작고 [[025_baseline|기준선]]도 없는 문제 | 수작업 [[025_baseline|baseline]] 먼저 | 탐색보다 문제 정의가 선행돼야 함 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[395_verification_process_review|검증]] [[001_dikw_pyramid|데이터]] 분할과 실험 시드(seed)가 고정되어 있는가?
2. 탐색 공간이 [[064_relation_domain|도메인]] 지식을 반영해 충분히 좁혀져 있는가?
3. ASHA, Hyperband, [[281_early_stopping|Early Stopping]] 같은 다단계 예산 절감 장치를 걸어 두었는가?
4. 정확도 외에 [[015_지연_데이터_관점|지연]]시간, 메모리, 추론 비용을 함께 측정하는가?
5. 실험 결과를 추적 저장소에 남겨 재현과 [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 가능한가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- baseline도 약한 상태에서 무작정 NAS부터 시작하는 경우
- [[395_verification_process_review|검증]]셋과 테스트셋을 사실상 같은 [[001_dikw_pyramid|데이터]]처럼 사용해 과적합된 탐색 결과를 믿는 경우
- 탐색 공간을 지나치게 넓게 잡아 [[418_gpu|GPU]] 예산만 소모하는 경우
- 학습 성공률이 낮은 실험 코드에 AutoML을 덮어씌워 실패를 대량 증식시키는 경우

기술사 답안에서는 **"AutoML은 모델 개발을 탐색 문제로 바꾸는 체계이며, 실무에서는 HPO를 우선 적용하고 NAS는 [[282_performance_tactics|성능]]-자원 제약을 함께 최적화해야 하는 제한된 문제에만 선택적으로 쓴다"**고 정리하면 핵심이 살아난다.

- **📢 섹션 요약 비유**: AutoML을 잘 쓰는 팀은 시험 범위를 정해 놓고 모의고사를 돌리는 팀이고, 못 쓰는 팀은 교과서 전체를 무작정 찍어 보는 팀과 같다.

---

## Ⅴ. 기대효과 및 결론

AutoML의 가장 큰 효과는 실험을 체계화한다는 점이다. 사람마다 다른 감과 습관에 좌우되던 모델 튜닝을 [[568_logs_distributed_logging_elk_fluentd|로그]]가 남는 반복 가능한 탐색으로 바꾸면, 조직은 같은 예산으로 더 많은 후보를 공정하게 비교할 수 있다. 특히 제품마다 비슷한 모델을 반복 개발하는 조직에서는 이 표준화 효과가 크다.

다만 AutoML은 계산비를 없애 주지 않는다. 탐색 공간이 넓고 목적 함수가 불안정할수록 결과는 쉽게 흔들리고, NAS처럼 구조까지 건드리면 재현성·비용·배포 복잡도 문제가 따라온다. 따라서 좋은 AutoML의 기준은 "가장 똑똑한 탐색기"가 아니라, **가장 선명한 목표와 가장 엄격한 예산 통제**다.

결론적으로 기억할 문장은 간단하다. AutoML은 "모델을 대신 발명하는 마법"이 아니라, "정해진 제약 안에서 더 나은 후보를 빨리 찾는 최적화 운영체계"다. 그래서 HPO는 널리 쓰이고, NAS는 여전히 선택적이다.

- **📢 섹션 요약 비유**: AutoML은 무한히 많은 레시피를 다 만들어 보는 요술이 아니라, 주방 예산 안에서 가장 가능성 높은 요리를 빠르게 골라내는 셰프 보조 시스템과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 하이퍼파라미터 (Hyperparameter) | AutoML에서 가장 먼저 탐색하는 [[009_config|설정]] 변수다. |
| Bayesian Optimization | 적은 실험으로 유망 후보를 찾는 대표 탐색 [[268_strategy_pattern|전략]]이다. |
| ASHA (Asynchronous Successive [[062_bitcoin_halving_supply_shock|Halving]] [[001_algorithm_definition|Algorithm]]) | 초반 성적이 나쁜 실험을 빨리 중단하는 다단계 자원 절감 기법이다. |
| [[492_nas_network_attached_storage|NAS]] (Neural [[319_architecture|Architecture]] Search) | 구조 자체를 탐색 공간에 넣는 고비용 [[176_automl_hyperparameter_optimization_bayesian|AutoML]] 기법이다. |
| Experiment Tracking | 어떤 후보가 왜 좋았는지 재현하고 비교하는 운영 기반이다. |
| Distributed [[588_mlops_pipeline_automation|Training]] | AutoML을 실무 규모로 돌리기 위한 [[430_index_fast_full_scan|병렬]] 실행 기반이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
수작업 튜닝
    │
    ▼
Grid / Random Search
    │
    ▼
Bayesian Optimization + Early Stopping
    │
    ▼
분산 HPO 자동화
    │
    ├─ 정확도 최적화
    ├─ latency / memory 제약 반영
    └─ 실험 추적 자동화
    │
    ▼
제한적 NAS + 다목적 AutoML
```

이 흐름은 AutoML이 단순 반복 실행에서 출발해, 예산 제약과 운영 추적을 포함한 [[136_variance|분산]] 최적화 체계로 발전했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. AutoML은 로봇이 여러 공부 방법을 대신 시험해 보고 제일 잘 맞는 방법을 골라주는 것과 같아요.
2. HPO는 같은 문제집으로 공부하되 연필, 시간표, 쉬는 시간을 바꿔 보는 거예요.
3. NAS는 아예 어떤 문제집과 책상을 쓸지까지 바꿔 보는 거라서 더 똑똑할 수 있지만 훨씬 더 큰 비용이 들어요.
