+++
title = "107. MLOps - 머신러닝 생명주기 관리"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/knowledge-base/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 실험실에서 만든 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 운영 서버에 올리고, 지속적으로 학습시켜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 부패를 막는 전 과정의 자동화 생태계다.
> 2. **가치**: 기존 소프트웨어의 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD ([지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포)에 [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/), 지속적 학습)를 결합하여, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화에 따른 예측 정확도 저하 ([Model Drift](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/))를 실시간으로 탐지하고 복구한다.
> 3. **판단 포인트**: 모델은 배포되는 순간부터 퇴화하기 시작하므로, 단순한 서빙 컨테이너화가 아닌 [피처 스토어](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ([Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/))와 재학습 파이프라인 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기준이 설계되어 있는지 여부가 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 도입의 성공을 가른다.

---

## Ⅰ. 개요 및 필요성

MLOps는 기계 학습 모델의 개발, 배포, 운영 과정을 통합하여 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 시스템의 신뢰성과 속도를 높이는 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) ([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))의 확장 프레임워크다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 로컬에서 3달간 훈련시켜 만든 '정확도 95%짜리 모델'을 백엔드 개발자에게 넘겨 운영 서버에 띄워 놓더라도, 시장 트렌드와 고객 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 변하면 그 AI는 몇 달 안에 엉뚱한 결과를 뱉는 쓰레기가 되고 만다. 이것을 모델 부패 (Model Decay) 또는 [모델 드리프트](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/) ([Model Drift](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/))라 부른다.

단순한 소프트웨어 코드는 한 번 짜놓으면 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)(Logic)가 변하지 않지만, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 모델은 먹고 자라는 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))'가 계속 변하기 때문에 지속적인 돌봄이 필수적이다. 사람이 수동으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 긁어모아 튜닝하고 다시 서버를 껐다 켜서 런칭하는 과정은 속도와 비용 면에서 불가능에 가깝다. 따라서 모델이 스스로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 감지해 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 다시 공부하고 운영계에 스무스하게 엎어 치는 전용 자동화 파이프라인이 탄생한 것이다.

- **📢 섹션 요약 비유**: 일반 소프트웨어가 공장에서 찍어내면 평생 그 모양대로 쓰는 '플라스틱 의자'라면, [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) AI는 매일 물과 햇빛을 줘야 하는 '살아있는 화초'와 같다. MLOps는 화초가 시들 기미를 보이면 센서가 스스로 물과 영양제(최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 공급해 영원히 싱싱하게 유지하는 '최첨단 스마트 온실'이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MLOps의 핵심은 소프트웨어 코드의 배포를 넘어 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 모델의 배포'를 통제하는 파이프라인에 있다. 특히 가장 중심이 되는 기어는 지속적 재학습 ([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) 메커니즘이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MLOps 파이프라인: CI/CD에 CT를 더한 생태계</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1. 데이터 추출 &amp; 피처 엔지니어링</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">원시 데이터 ──▶ 피처 스토어 (Feature Store, 깔끔한 밥상)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2. 모델 훈련 및 검증 (CT, Continuous Training)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 주입 ──▶ 하이퍼파라미터 튜닝 ──▶ 모델 파일(.pkl/.onnx) 생성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">※ 핵심: 이 과정이 '자동 트리거'에 의해 스크립트로 굴러가야 함!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3. 지속적 통합 및 배포 (CI/CD)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">모델 도커 패키징 ──▶ 카나리/블루그린 배포 ──▶ 운영 서버(Serving)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4. 모니터링 및 성능 감시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실시간 예측 오차율 감지 (Drift 감지)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">2번의 CT 재가동 핑 쏘기!</div></div>
</div>
</div>



운영 중인 모델의 예측값이 실제 정답(Ground Truth)과 얼마나 틀려지는지를 실시간으로 모니터링하다가 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 넘는 순간([Data Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 포착), 모니터링 봇은 사람을 부르지 않고 곧바로 파이프라인의 1번 단계로 신호를 쏜다. 시스템은 알아서 최근 1주일 치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 끌고 와 야간에 재학습을 빡세게 돌린 뒤 다음 날 아침 100% 똑똑해진 새 모델 컨테이너를 갈아 끼운다.

- **📢 섹션 요약 비유**: 이는 똑똑한 직원을 채용(모델 배포)하는 데 그치지 않고, 직원의 업무 성과가 떨어지는 순간(정확도 하락) 자동으로 최신 업무 트렌드 학원([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 재학습)에 보내 다시 일잘러로 만들어 자리에 앉히는 무한 자동화 인사관리 시스템이다.

---

## Ⅲ. 비교 및 연결

DevOps가 개발(Dev)과 운영(Ops)의 벽을 깼다면, MLOps는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Science)까지 포함된 3각 편대의 융합을 만들어낸다.

| 비교 항목 | 전통적 소프트웨어 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) | 결정적 차이 |
|:---|:---|:---|:---|
| <strong>관리 대상 (<a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리)</strong> | 소스 코드 (Git) | 소스 코드 + <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 셋 + 모델 <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a>(<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">Weight</a>)</strong> | 코드가 같아도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 다르면 결과가 아예 달라짐 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/">지속적 통합</a>) 대상</strong> | 코드 [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/), 빌드 테스트 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유효성 검사, 모델 학습 **스크립트** 통합 | 모델 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자체가 아니라 학습 과정을 통합함 |
| <strong>핵심 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하 원인</strong> | 서버 트래픽 폭주, [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 분포의 변화 (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a>/<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/">Concept Drift</a>)</strong> | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 결함이 없어도 외부 세계가 변하면 장애로 간주 |

소프트웨어는 입력이 같으면 출력이 100% 보장되는 결정론적 시스템이지만, 모델은 확률론적이다. 따라서 MLOps는 '모델 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(.pkl)'을 산출물로 취급해 배포하는 것이 아니라, 모델을 훈련시키는 '학습 파이프라인 코드 자체'를 산출물로 취급해 서버에 올린다는 엄청난 패러다임의 전환을 가진다.

- **📢 섹션 요약 비유**: DevOps가 '완성된 빵(소프트웨어)'을 굽고 빠르게 배송하는 공장이라면, MLOps는 빵이 아니라 '매일 변하는 제철 밀가루([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))로 알아서 최고의 빵을 반죽해 내는 로봇 오븐(학습 파이프라인)' 자체를 공장에 설치하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

MLOps는 도구의 도입이 아니라 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))화 된 팀 간의 파이프라인 조립 설계다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 판단 기준
1. <strong>역할별 파이프라인 분리 (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/">Kubeflow</a> / <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/">MLflow</a> 등 도입)</strong>: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어는 더러운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정제해 [피처 스토어](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ([Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/))에 밀어넣고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 튜닝에만 집중하며, 운영자는 서빙 인프라 관리를 하도록 플랫폼 위에서 협업선이 그어져 있는가?
2. <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a> 규칙의 명확화</strong>: 재학습([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/))을 언제 돌릴 것인가? '매주 일요일 자정'처럼 정기적 스케줄링으로 갈 것인가, 아니면 '정확도가 85% 밑으로 떨어질 때'처럼 이벤트 기반 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)로 갈 것인가에 대한 비즈니스 판단이 있어야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **수동 모델 넘기기 (Throw over the wall)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 로컬 주피터 노트북(Jupyter Notebook)에서 훈련시킨 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 USB나 슬랙으로 백엔드 개발자에게 던져주는 짓이다. 나중에 모델을 재현(Reproducibility)하려 할 때 당시 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 썼는지, 파이썬 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 뭐였는지 아무도 몰라 결국 처음부터 다시 짜야 하는 지옥이 펼쳐진다.

- **📢 섹션 요약 비유**: 명검을 대장장이([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자)가 자기 집에서 비밀리에 두드려 만들어 기사(운영팀)에게 던져주는 게 기존 방식이다. 검이 부러지면 다시 대장장이를 찾아가 몇 달을 빌어야 한다. MLOps는 대장장이의 두드리는 '기술(파이프라인)' 자체를 전방 진지 옆에 공장으로 복제해 놓는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅴ. 기대효과 및 결론

MLOps의 구축은 초기에 엄청난 플랫폼 세팅 비용과 러닝 커브를 요구하지만, 일단 맞물려 돌아가기 시작하면 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 서비스의 타임-투-마켓(Time-to-Market)을 수개월에서 수 시간으로 단축시킨다.

더 이상 비싼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자가 반복적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 끌어오기와 모델 재배포에 매달리지 않고 새로운 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 연구에만 몰두할 수 있게 해 준다. 예측 모델은 배포되는 첫날부터 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 썩기 시작한다는 숙명을 역으로 이용해, '스스로 썩은 부위를 도려내고 새살을 채우는 불사조 아키텍처'를 만들어내는 것이 MLOps의 최종 결론이다.

- **📢 섹션 요약 비유**: 수백만 원짜리 최신형 레이싱카([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델)를 사놓고 오일 교환을 할 줄 몰라 창고에 방치하는 낭비를 없애준다. 차가 달리면서 타이어 마모(모델 부패)를 스스로 감지하면 달리면서 피트스톱([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/))을 호출해 바퀴를 갈아 끼우고 레이스를 영원히 이어가는 르망 24시 레이싱의 피트크루 시스템이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">데이터 드리프트</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">Data Drift</a>)</strong> | 과거 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 현재 실제 운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 분포가 달라져 엉뚱한 답을 내놓게 되는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 부패의 주범 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/">피처 스토어</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/">Feature Store</a>)</strong> | 더러운 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 씻고 깎아 모델이 바로 학습할 수 있게 미리 만들어둔 '밀키트 저장소'. 모델 재사용성을 극대화함 |
| <strong>A/B 테스트 및 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a></strong> | 새로 학습된 모델이 미쳐 날뛸 가능성에 대비해 트래픽의 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%만 새 모델에 부어보고 간을 보는 안전 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/">Model Registry</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/">모델 레지스트리</a>)</strong> | "2026년 3월 4일에 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 학습한 V1.3 모델 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)" 등 모델의 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 깃허브처럼 완벽히 추적 보관하는 금고 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">개발과 운영의 결합 (소프트웨어)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DevOps (CI/CD 파이프라인)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터와 모델의 통제 필요성 대두</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">MLOps 등장 (CT 추가, Model Drift 감시)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">거대 모델 및 생성형 AI 운영으로 확장</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">LLMOps (프롬프트 관리, RAG 파이프라인 모니터링 결합)</div>
</div>
</div>


이 흐름도는 단순한 코드 배포 자동화에서 시작해 확률적 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 유지보수로 진화하고, 궁극적으로 거대 언어 모델([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))을 통제하는 [LLMOps](/knowledge-base/studynote/12_it_management/05_security_compliance/221_llmops_large_language_model_ops/) 생태계로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MLOps는 우리가 키우는 '[인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 로봇 강아지'를 돌봐주는 똑똑한 자동화 공장이에요.
2. 강아지가 옛날 지식만 고집해서 바보 같은 소리를 하기 시작하면(모델 부패), 기계가 삐뽀삐뽀 울리며 알아서 강아지를 학원에 보내 최신 책을 읽게(재학습) 만들어요.
3. 그렇게 학원을 다녀온 강아지가 다음 날 아침이면 예전처럼 완벽하게 심부름을 잘하게 만들어주는 마법의 시스템이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 107 / 973

← **이전**: [106. FinOps - 클라우드 비용 최적화 및 관리](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/106_finops_cloud_cost_optimization/)
**다음**: [108. LLMOps (대규모 언어 모델 운영)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/108_llmops_large_language_model/) →

---
