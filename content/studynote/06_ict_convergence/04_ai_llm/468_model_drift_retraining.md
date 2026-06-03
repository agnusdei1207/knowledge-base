+++
title = "468. 모델 드리프트 (Model Drift)와 재학습 (Retraining)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모델 드리프트(Model Drift)는 세상의 트렌드, 경제 상황, 사람들의 입맛 등 환경([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 변하면서, 어제까지 완벽하게 정답을 맞히던 천재 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델이 오늘부터 갑자기 바보가 되어버리는 '[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [노화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/182_aging/) 현상'이다.
> 2. **가치**: 이 현상을 막으려면 단순히 모델을 배포하고 끝내는 것이 아니라, 24시간 내내 들어오는 새로운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 감시하다가 에러율이 커지면 모델을 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 다시 공부시키는 **재학습(Retraining)** 파이프라인([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/))을 구축해야 한다.
> 3. **판단 포인트**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 아주 서서히 변하는지(Gradual), 아니면 코로나19처럼 하루아침에 세상이 뒤집히는지(Sudden)를 통계적으로 모니터링하여, 재학습 주기를 '매일'로 할지 '점수([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))가 떨어질 때'만 할지 동적으로 결정하는 것이 운영 비용([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))을 절감하는 핵심이다.

---

## Ⅰ. 개요 및 필요성

2019년, 완벽하게 돌아가던 항공사 수요 예측 AI가 2020년 3월에 갑자기 모든 티켓 예측을 100% 틀리기 시작했다. 이유는 코로나19 때문이었다. AI는 "봄이 되면 사람들이 여행을 간다"고 과거 10년 치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 배웠는데, 코로나라는 전대미문의 사건([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 대격변)이 터지자 과거의 지식은 쓸모없는 쓰레기가 되었다.

이처럼 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)은 일반 소프트웨어와 다르다. 소프트웨어 코드는 한 번 짜두면 영원히 똑같이 작동하지만, <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a> 모델은 시간이 지나면 세상(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>)과 동떨어져 무조건 부패한다.</strong>
이 피할 수 없는 '[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 부패' 현상을 <strong>모델 드리프트(Model Drift)</strong>라고 부르며, 이를 치료하는 유일한 백신이 바로 <strong>재학습(Retraining)</strong>이다.

- **📢 섹션 요약 비유**: 어제까지 "비트코인은 무조건 오른다"는 투자 법칙(모델)을 깨우친 주식 고수가, 오늘 아침 갑자기 발생한 전쟁 뉴스([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화)를 보지 않고 어제 법칙대로 계속 투자를 하다가 전 재산을 날려먹는 것이 모델 드리프트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

드리프트는 크게 '입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 변하는 병'과 '정답의 룰 자체가 변하는 병' 두 가지로 나뉜다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">모델 드리프트의 2대 유형과 모니터링 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 데이터 드리프트 (Data Drift / Covariate Shift)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- "입력(X)의 분포가 변했다!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 과거: 주로 20대가 쇼핑몰에 옴 -&gt; 현재: 갑자기 60대가 몰려옴</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 모델이 한 번도 본 적 없는 데이터(60대)가 쏟아져서 당황함</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 컨셉 드리프트 (Concept Drift)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- "정답(Y)의 법칙 자체가 변했다!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 과거: '마스크'를 검색하면 방한용 면 마스크를 샀음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 현재: '마스크'를 검색하면 코로나용 KF94 마스크를 삼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 똑같은 X(마스크 검색)가 들어와도 정답 Y가 완전히 바뀌어버림!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 모니터링 및 재학습 트리거 (Retraining Trigger)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- PSI(Population Stability Index)나 KL 발산 지표를 사용해</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">어제 데이터와 오늘 데이터의 모양이 5% 이상 틀어지면 삐용삐용!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 알람이 울리면 사람을 안 부르고 시스템이 알아서 재학습 시작(CT)</div></div>
</div>
</div>



1. <strong>지속적 학습 (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">Continuous Training</a>, <a href="/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/">CT</a>)</strong>: 모델 [노화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/182_aging/)를 막는 자동화 파이프라인이다. 드리프트 알람이 울리면, 최신 1달 치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 긁어와서 모델 가중치를 다시 훈련한다. 이때 예전 지식을 너무 다 까먹게(Catastrophic Forgetting) 덮어씌우면 안 되므로 [미세 조정](/knowledge-base/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)([Fine-tuning](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) 기법을 정교하게 쓴다.
2. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/">섀도우 배포</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/118_shadow_deployment_traffic_mirroring/">Shadow Deployment</a>)</strong>: 재학습이 끝난 새 모델을 바로 손님에게 서비스하지 않는다. 기존 모델이 일하고 있는 뒤쪽(그림자)에 숨겨두고, 똑같은 손님 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 줘보면서 "새 모델이 진짜 기존 모델보다 낫나?" 조용히 성적표를 매긴 뒤에 통과하면 교체한다.

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 붕어빵 장수(모델)가 팥을 좋아하던 초등학생들만 상대하다가 갑자기 외국인 관광객들이 몰려와서 당황하는 것이고, [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)는 여전히 초등학생들이 오긴 오는데 애들이 갑자기 팥 대신 슈크림빵만 달라고 입맛(정답의 룰)이 확 바뀌어버린 현상이다.

---

## Ⅲ. 비교 및 연결

드리프트의 발생 속도에 따른 3가지 패턴과 그 대응 방안을 비교해 본다.

| 비교 항목 | 점진적 드리프트 (Gradual Drift) | 갑작스러운 드리프트 (Sudden Drift) | 주기적 드리프트 (Recurring Drift) |
|:---:|:---|:---|:---|
| **발생 원인** | 시간이 지나며 서서히 트렌드가 변함 | 전쟁, 코로나, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경 등 대격변 | 요일, 계절 등 특정 주기로 변함 |
| **현상 예시** | 유선 이어폰 -> 무선 이어폰으로 유행 변화| 코로나 터지고 항공 수요 0으로 증발 | 겨울엔 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/), 여름엔 반팔 수요 폭발 |
| **모니터링 난이도**| 감지하기 어려움 (가랑비에 옷 젖음) | **바로 감지됨 (에러율 수직 상승)** | 감지 쉬움 (매년 똑같이 일어남) |
| <strong>최적의 재학습 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>| **1주일, 1달 주기의 정기적 재학습(배치)** | **알람 울리면 즉시 비상 재학습 (Trigger)**| 겨울용 모델, 여름용 모델 여러 개 준비 |

현업에서 가장 무서운 것은 '점진적 드리프트(Gradual Drift)'다. 에러율이 하루에 0.01%씩 야금야금 떨어지기 때문에 모니터링 대시보드에 알람이 울리지 않는다. 6개월 뒤에 눈치챘을 때는 이미 수억 원의 매출이 날아간 뒤다.

- **📢 섹션 요약 비유**: 갑작스러운 드리프트는 타이타닉호가 빙산에 충돌한 것처럼 모두가 당장 위기임을 알고 비상벨을 누르는 상황이다. 점진적 드리프트는 배 밑바닥에 아주 미세한 구멍이 나서 물이 한 방울씩 새고 있는데, 선원들이 눈치채지 못하고 놀다가 서서히 배가 가라앉는 가장 무서운 재앙이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 적용 시나리오:**
신용카드 회사의 사기 결제([FDS](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/)) 탐지 AI를 운영 중이다. 해커들은 AI를 피하기 위해 매주 새로운 사기 수법을 만들어낸다(극심한 [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)).
[MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 엔지니어는 <strong>Evidently <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong> 같은 드리프트 탐지 오픈소스를 파이프라인에 붙인다. 과거 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))의 분포와 오늘 들어온 실시간 결제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Current](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/))의 분포를 1시간마다 비교하여 <strong>PSI (<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/">Population Stability Index</a>)</strong> 점수를 잰다. PSI가 0.2를 넘어가자(드리프트 경고), 시스템은 밤 12시에 Airflow를 깨워 최근 1주일 치 해커들의 사기 패턴 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 먹여 모델을 재학습시키고 아침 6시에 무중단으로 새 AI를 배포한다. 해커의 새로운 패턴을 하루 만에 AI가 완벽 방어해 낸다.

**기술사 판단 포인트 (Trade-off):**
재학습 아키텍처 설계 시 기술사는 <strong>'재학습 비용(<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a>)'과 '<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하로 인한 손실'</strong>을 저울질해야 한다.
1. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 바뀔 때마다 매시간 재학습([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/))을 시키면 AI는 똑똑해지겠지만, 클라우드 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 서버비가 1억 원씩 터져나가 회사가 파산한다.
2. 반대로 돈 아낀다고 1년에 한 번만 재학습하면 AI가 바보가 되어 고객이 이탈한다.
3. 기술사는 재학습 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)(Trigger)를 설계할 때 무작정 "매일 밤 12시에 학습해라" 같은 멍청한 타임 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)(Time-based)을 쓰지 말고, 모델의 정확도나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포 편차(PSI)가 임계치를 넘었을 때만 똑똑하게 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 전원을 켜는 <strong>이벤트 기반(Event-based) 재학습 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong>를 설계해야 MLOps의 가성비를 극대화할 수 있다.

- **📢 섹션 요약 비유**: 집에 먼지가 쌓이는 것(드리프트)을 치우기 위해 청소 로봇을 돌린다. 먼지가 1톨 떨어질 때마다 매초 로봇을 돌리면 전기세([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 비용)가 폭탄을 맞는다. 현명한 집주인은 바닥에 먼지가 '1cm 두께'로 쌓였을 때만(이벤트 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)) 로봇의 전원을 켜서 전기세를 아끼면서도 집의 청결을 유지한다.

---

## Ⅴ. 기대효과 및 결론

모델 드리프트에 대한 대응 체계([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 파이프라인)는, 인공지능이라는 소프트웨어가 1회성 예술 작품([Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/))이 아니라 매일매일 기름을 치고 나사를 조여야 하는 거대한 생명체(Organism)임을 증명한다. 세상이 변하면 기계의 뇌도 함께 변해야 살아남을 수 있다.

결론적으로 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 레벨의 완성도는 "모델을 얼마나 잘 만들었느냐"가 아니라, "모델이 바보가 되었을 때 사람 손을 안 거치고 얼마나 빨리 스스로 최신 버전으로 부활할 수 있느냐"에 달려 있다. 기술사는 딥러닝 코드를 짜는 시간을 줄이고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 분포가 틀어지는 순간을 포착하는 감시탑(Monitoring)과, 죽은 모델을 다시 살려내는 재학습(Retraining) 심폐소생술 자동화 인프라를 구축하는 시스템의 설계자로 거듭나야 한다.

- **📢 섹션 요약 비유**: 모델 드리프트는 기계가 걸리는 자연스러운 치매([노화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/182_aging/)) 현상이다. 치매를 막을 수는 없지만, MLOps라는 최첨단 병원 시스템([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 파이프라인)에 기계를 입원시켜 매일매일 새로운 지식(최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 주사해 줌으로써 기계가 영원히 젊고 똑똑하게 살아가도록 만드는 영생의 비법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 상위 개념 | [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학 수명 주기 |
| 하위 개념 | [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/), [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/), PSI ([Population Stability Index](/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/)) |
| 연결 개념 | 지속적 학습 ([CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/), [Continuous Training](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)), [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/), [KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[MLOps · 데이터 과학 수명 주기] → [모델 드리프트 · 재학습] → [지속적 학습 · 섀도우 배포]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 작년에 "겨울에는 사람들이 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)을 좋아해"라고 배운 똘똘한 점원 로봇이 있어요.
2. 그런데 지금은 8월 한여름인데(세상의 변화, 드리프트), 로봇은 옛날 기억만 믿고 들어오는 손님마다 땀을 뻘뻘 흘리는데도 털 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)을 추천해요!
3. 그래서 사장님이 "지금은 여름이야, 반팔을 추천해야지!"라고 오늘 날씨(최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 다시 가르쳐주는 것(재학습)이 꼭 필요하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 468 / 552

← **이전**: [467. 피처 스토어 (Feature Store)와 특징 변수 공유](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/467_feature_store_data_sharing/)
**다음**: [469. XAI, LIME, SHAP: 국소/전역 기여도 해석 (XAI LIME SHAP Local Global Attribution)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/469_xai_lime_shap_local_global_attribution/) →

---
