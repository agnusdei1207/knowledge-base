---
title: "466. MLOps 파이프라인과 CI/CD/CT"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/)([Machine Learning Operations](/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 주피터 노트북(Jupyter)에서 실험용으로 만든 딥러닝 코드를, 실제 고객이 1년 365일 1초의 끊김 없이 쓸 수 있도록 코딩(Dev)부터 배포(Ops)까지의 전 과정을 톱니바퀴처럼 자동화한 파이프라인 철학이다.
> 2. **가치**: 기존 소프트웨어는 코드만 배포([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD)하면 끝이었지만, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)은 세상([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 변하면 모델이 바보가 되므로 모델을 끝없이 다시 학습시키는 <strong>지속적 학습(<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a>, <a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">Continuous Training</a>)</strong>이라는 완전히 새로운 개념의 자동화 장치를 추가했다.
> 3. **판단 포인트**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 추출 $\rightarrow$ 전처리 $\rightarrow$ 학습 $\rightarrow$ [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) $\rightarrow$ 배포로 이어지는 이 파이프라인은 사람이 손으로 돌리면 반드시 휴먼 에러가 터지므로, 기술사는 Airflow나 [Kubeflow](/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) 같은 오케스트레이터(Orchestrator)를 써서 전 과정을 버튼 하나로 자동화해야만 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 레벨을 달성할 수 있다.

---

## Ⅰ. 개요 및 필요성

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 3개월 동안 철야를 해서 정확도 99%의 주가 예측 모델을 만들었다. 모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(pt)을 서버 팀에 넘겼다.
그런데 서버 팀이 이 모델을 배포하자마자 정확도가 50%로 떨어졌다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 내 컴퓨터에서는 잘 돌았는데 왜 그러냐고 싸운다. 원인은 서버의 파이썬 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 다르고, 전처리 코드가 안 맞고, 어제부터 주식 시장의 패턴([데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/))이 아예 바뀌었기 때문이다.

"모델 하나 던져주고 끝나는 게 아니구나. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 계속 변하니까, <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 수집부터 모델 재학습, 그리고 서버에 안전하게 배포하는 것까지를 사람 손 안 거치고 하나의 거대한 공장 컨베이어 벨트처럼 엮을 순 없을까?</strong>"
이 눈물겨운 실패의 역사에서 탄생한 '[머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 전용 [데브옵스](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))'가 바로 <strong><a href="/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a></strong>다.

- **📢 섹션 요약 비유**: 셰프([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자)가 집에서 혼자 끓여본 완벽한 김치찌개 레시피(모델)를 식당(서버)에 그냥 넘기면 식당 알바생은 절대 그 맛을 못 낸다. MLOps는 식재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 손질부터 가스불 조절, 찌개 끓이기, 손님상에 내기까지의 전 과정을 완벽하게 세팅한 프랜차이즈 레시피 자동화 공장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MLOps는 기존 소프트웨어의 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD에 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)(지속적 학습)라는 심장을 하나 더 단 3-Step 파이프라인이다.

```text
+--------------------------------------------------------+
|             [ MLOps의 3대 자동화 (CI / CD / CT) 파이프라인 ]    |
+--------------------------------------------------------+
| 1. CI (Continuous Integration, 지속적 통합)            |
|    - 개발자가 새로운 AI 코드를 짜서 GitHub에 올림(Push)         |
|    - 시스템이 "코드가 안 깨지나? 전처리는 잘 되나?" 자동으로 테스트함|
|    - 즉, '코드와 데이터'를 안전하게 합치는(Integration) 단계    |
|                                                        |
| 2. CT (Continuous Training, 지속적 학습) ⭐️ 머신러닝의 꽃 ⭐️ |
|    - 데이터가 변했다는 알람(Data Drift)이 울림               |
|    - 사람이 개입하지 않고, 시스템이 알아서 최신 데이터를 끌어와서  |
|      AI 모델을 다시 학습시키고 99점(성능)이 나오는지 스스로 시험 봄|
|                                                        |
| 3. CD (Continuous Deployment, 지속적 배포)             |
|    - CT에서 99점을 받은 똑똑한 새 모델이 탄생함                 |
|    - 서버가 멈추지 않게(무중단), 낡은 모델을 내리고 새 모델을    |
|      API 형태로 부드럽게 갈아 끼워서(Deploy) 손님들에게 서비스함 |
+--------------------------------------------------------+
```

1. <strong>파이프라인 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a> (<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">Orchestration</a>)</strong>: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 긁어오기 -> 전처리 -> 학습 -> 모델 평가 -> 배포라는 5개의 컨베이어 벨트 작업은 순서대로 맞물려 돌아가야 한다. 이 작업 순서를 스케줄링하고 앞선 작업이 끝나면 뒤의 작업을 자동으로 쳐주는 현장 소장이 필요한데, 이 역할을 <strong><a href="/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/">Apache Airflow</a>, <a href="/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/">Kubeflow</a>, <a href="/studynote/10_ai/02_dl_architecture_new/180_mlflow/">MLflow</a></strong> 같은 툴이 담당한다.
2. <strong><a href="/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/">모델 레지스트리</a> (<a href="/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/">Model Registry</a>)</strong>: 학습이 끝난 모델의 성적표, [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 그때 썼던 파이썬 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 등을 도서관처럼 꼼꼼하게 기록해 두는 모델 저장소다. 나중에 배포한 모델이 사고를 치면, [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)를 뒤져 어제 배포했던 건강한 모델로 1초 만에 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)([Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/))시킬 수 있다.

- **📢 섹션 요약 비유**: CI는 "새로 짠 레시피가 요리법에 맞는지 검사하는 것"이고, CT는 "철마다 바뀌는 제철 식재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 넣어서 찌개를 매일 다시 끓이는 것"이며, CD는 "손님이 밥 먹고 있는데 몰래 반찬통을 방금 만든 신선한 반찬으로 스윽 갈아 끼우는 것"이다.

---

## Ⅲ. 비교 및 연결

구글은 MLOps의 성숙도(Maturity)를 3단계 레벨로 엄격하게 쪼개어 기업의 IT 수준을 뼈때린다.

| 비교 항목 | Level 0 (수동 파이프라인) | Level 1 (파이프라인 자동화) | Level 2 ([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 완전 자동화) |
|:---:|:---|:---|:---|
| **작동 방식** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 **주피터 노트북에서 일일이 손으로 돌림** | 모델의 <strong>학습 과정(<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a>)만 자동으로 스크립트화함</strong> | 코드를 고치거나 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 변하면 **모든 과정이 전자동으로 돎** |
| **배포 대상** | 저장된 <strong>'모델 <a href="/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a>(pkl)'</strong> [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자체를 수동으로 배포함 | 모델을 찍어내는 <strong>'파이프라인 코드'</strong>를 배포함 | <strong><a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD/<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a> 통합 인프라</strong> 자체를 띄움 |
| **적용 환경** | AI로 장난치는 스타트업 수준 | 일반적인 IT 기업의 1차 목표 | 구글, 넷플릭스 등 초격차 빅테크 |
| **단점** | 재학습(Retrain)할 때마다 에러 터짐 | 새로운 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(코드)을 추가할 땐 여전히 수동 배포해야 함 | 구축하는 데 수억 원의 인프라 비용과 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 천재 엔지니어 필요 |

대부분의 회사가 Level 0에 머물러 있다가, 막상 서비스가 대박이 나면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 터져나가며 모델 유지보수(Ops) 지옥에 빠져 허우적댄다. MLOps는 "초반에 인프라 세팅하느라 1년을 버리더라도, 반드시 Level 1 이상의 파이프라인을 구축하고 시작해라"라고 경고하는 개발 방법론이다.

- **📢 섹션 요약 비유**: Level 0은 장인이 한 땀 한 땀 구두를 만드는 공방이다(고장 나면 수리가 안 됨). Level 1은 구두를 찍어내는 공장 기계(파이프라인)를 세운 것이다. Level 2는 구두가 닳으면([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화) 공장이 스스로 가죽을 구해와서 새 구두를 찍어내 손님 발에 자동으로 신겨주는 궁극의 자동화 공장이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
쇼핑몰 추천 AI를 배포 중이다. 갑자기 유행이 바뀌어 어제 배포한 추천 AI의 매출이 떡락했다. [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 모니터링 툴(Evidently)이 <strong><a href="/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">데이터 드리프트</a>(<a href="/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">Data Drift</a>)</strong> 알람을 울린다.
즉시 <strong><a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a>(<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">Continuous Training</a>)</strong> 파이프라인이 자동 발동된다. Kubeflow가 어제 들어온 최신 유행 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 10만 건을 끌어와 모델을 스스로 재학습(Retrain)시킨다. 모델의 점수(AUC)가 예전보다 5% 높게 나오자(평가 통과), <strong>CD(<a href="/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/">Continuous Deployment</a>)</strong> 시스템이 기존 컨테이너를 내리고 새 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 컨테이너로 말아서 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버에 무중단 배포한다. 이 모든 과정이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 잠든 새벽 3시에 1시간 만에 전자동으로 쾌적하게 끝난다.

**기술사 판단 포인트 (Trade-off):**
엔터프라이즈 환경에서 기술사는 <strong>'배포 <a href="/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a>'와 'A/B 테스트'</strong> 전략을 통제해야 한다.
1. CT가 아무리 똑똑해서 지 혼자 99점을 맞았다고 해도, 그 모델을 내일 아침 1,000만 명의 고객에게 한 번에 100% 배포(Big Bang [Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))하는 것은 미친 짓이다.
2. 기술사는 무조건 <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a>(<a href="/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">Canary Deployment</a>)</strong>나 **A/B 테스트** 라우팅을 파이프라인 끝단에 설계해야 한다.
3. 새 모델(B)에게는 전체 트래픽의 딱 5%만 흘려보내고, 기존 모델(A)이 95%를 처리하게 한다. 며칠 동안 5% 트래픽에서 서버가 안 뻗고 매출도 진짜 올랐다는 로그가 확인될 때만, 점진적으로 트래픽을 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%, 50%, 100%로 스위칭하는 안전망을 구축해야 한다.

- **📢 섹션 요약 비유**: 아무리 훌륭한 신약(새 모델)을 개발했더라도, 내일 아침 전 국민 1,000만 명에게 다 주사할 수는 없다. 부작용이 있을 수 있으니, 아주 적은 수의 자원자(5% [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 트래픽)에게 먼저 투약해 보고 완벽히 안전할 때 전 국민에게 배포하는 것이 MLOps의 깐깐한 식약처 철학이다.

---

## Ⅴ. 기대효과 및 결론

MLOps는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자는 수학 공식만 짜는 사람이 아니라, 그 공식이 살아 숨 쉬며 돌아가는 거대한 공장의 설계자가 되어야 한다"는 사상을 IT 업계에 이식했다. [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)이 실험실의 논문을 넘어, 24시간 멈추지 않고 돈을 벌어다 주는 진짜 '소프트웨어 자산'으로 진화하는 교두보를 마련한 것이다.

결론적으로 MLOps가 없는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 서비스는 한 달짜리 시한부 생명이다. 기술사는 주피터 노트북에 깔끔하게 적힌 코드에 감동할 것이 아니라, 그 코드가 <strong>"언제 재학습될 것인지(<a href="/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a> Trigger)", "어떻게 테스트될 것인지(<a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>)", "어떤 전략으로 서버에 안착할 것인지(CD)"</strong>를 묻는 파이프라인의 혹독한 검열관이 되어야 한다. AI의 성능은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에서 나오지만, AI의 생명력은 전적으로 이 파이프라인 인프라에서 나오기 때문이다.

- **📢 섹션 요약 비유**: 멋진 레이싱카([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델)를 만드는 것도 중요하지만, 레이싱카는 경기 중 반드시 타이어가 닳고 기름이 떨어진다([데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)). MLOps는 차가 달리는 도중에 타이어를 1초 만에 갈아 끼우고 기름을 채워주는([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD/[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) 완벽한 호흡의 피트 스탑(Pit Stop) 크루들을 훈련시키는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 상위 개념 | [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 생태계, [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) |
| 하위 개념 | 지속적 학습 ([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)), [지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포 ([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD), 파이프라인 ([Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/)) |
| 연결 개념 | [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/), [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/), [모델 레지스트리](/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) ([MLflow](/studynote/10_ai/02_dl_architecture_new/180_mlflow/)), [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) ([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) |

### 📈 관련 키워드 및 발전 흐름도

```text
[인공지능 생태계 · 소프트웨어 공학] -> [MLOps 파이프라인과 CI · CD] -> [데이터 드리프트 · 카나리 배포]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 공장에서 예전엔 아저씨가 손으로 하나하나 로봇을 만들어서 실수도 많고 너무 느렸어요.
2. [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 마법사는 공장에 "자동 컨베이어 벨트(파이프라인)"를 깔아줬어요. 이제 나사가 빠진 로봇은 알아서 걸러내고([CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)), 고장 나면 1초 만에 새 로봇으로 바꿔줘요(CD).
3. 심지어 유행이 바뀌면, 기계가 스스로 최신 설명서를 읽고 더 멋진 로봇으로 업그레이드해서 만들어내는([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) 무적의 로봇 공장이 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 466 / 552

<- **이전**: [465. DQN (Deep Q-Network)과 경험 리플레이, 타겟 네트워크](/studynote/06_ict_convergence/04_ai_llm/465_dqn_deep_q_network/)
**다음**: [467. 피처 스토어 (Feature Store)와 특징 변수 공유](/studynote/06_ict_convergence/04_ai_llm/467_feature_store_data_sharing/) ->

---
