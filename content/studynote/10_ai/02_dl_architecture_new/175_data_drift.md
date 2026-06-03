+++
title = "175. 데이터 드리프트 (Data Drift)"
date = 2026-04-17

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/))는 모델이 학습한 입력 분포 `P_train(X)`와 실제 서빙 입력 분포 `P_serving(X)`가 달라지는 현상으로, 보통 `P(Y|X)`의 의미 자체는 크게 바뀌지 않은 상태를 가리킨다.
> 2. **가치**: 배포 직후에는 잘 맞던 모델이 시간이 지나며 조용히 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 잃는 대표 원인이므로, [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/knowledge-base/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))에서 반드시 감시해야 하는 운영 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)다.
> 3. **판단 포인트**: 드리프트 알람이 곧바로 모델 교체를 뜻하지는 않으며, [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)), 타깃 드리프트 (Target Drift), [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew와 구분한 뒤 재학습·전처리 수정·임계값 조정 중 맞는 처방을 골라야 한다.

---

## Ⅰ. 개요 및 필요성

[데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 "모델이 세상을 배운 교과서"와 "실제 운영에서 마주치는 세상"이 조금씩 달라지는 현상이다. 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 겨울철 검색어, 낮 시간대 사용자, 특정 센서 상태에 맞춰져 있었다면, 봄철 트래픽·새로운 사용자군·교체된 장비가 들어오는 순간 입력 분포는 자연스럽게 흔들린다. 모델 코드가 멀쩡해도 예측 품질은 서서히 떨어질 수 있다.

이 문제가 위험한 이유는 일반 소프트웨어 버그처럼 즉시 오류를 내지 않기 때문이다. [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)은 계속 추천을 내보내고, 사기 탐지 모델도 계속 점수를 반환하며, 이미지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델도 여전히 라벨을 출력한다. 하지만 실제로는 사용자의 행동 패턴, 센서 노이즈, 시장 구성, 계절성 같은 외부 변화가 모델이 기대한 입력과 멀어지면서 정확도를 갉아먹는다.

아래 그림은 왜 오프라인에서 좋던 모델이 운영에서 조용히 약해지는지를 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Why offline accuracy decays after deployment</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Training window</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">winter queries, old camera, weekday-heavy users</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Model deployment</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Live window</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">spring queries, new camera noise, mobile-heavy users</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ predictions continue, labels arrive later</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">-&gt; silent quality decay</div></div>
</div>
</div>



결국 [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)를 이해한다는 것은 "모델의 수명은 코드가 아니라 입력 환경에 의해 결정된다"는 사실을 받아들이는 일이다. 운영 중인 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 시스템은 배포 완료가 끝이 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 환경 변화와의 장기전 안에 놓여 있다.

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 같은 시험 문제집으로 공부했는데 실제 시험장 조명, 종이 색, 감독 방식이 달라진 상황과 같다. 정답 개념은 같아도 시험 환경이 바뀌면 익숙한 학생도 실수를 늘리게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)의 핵심 수식은 `P_train(X) ≠ P_serving(X)`이다. 즉 입력 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)(feature)의 분포가 달라졌다는 뜻이다. 보통은 `P(Y|X)` 자체가 완전히 바뀌지 않았다는 가정 아래 논의하므로, 올바른 대응은 "세상이 달라진 현재 입력을 기준으로 모델을 다시 맞춰 주는 것"이다. 이 때문에 [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)보다 상대적으로 관리 가능한 편이지만, 그만큼 조기 감지가 중요하다.

실무에서는 학습 시점의 기준 분포를 저장해 두고, 운영 입력을 일정 시간 창(window)으로 묶어 비교한다. 이때 PSI ([Population Stability Index](/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/)), KS 검정 (Kolmogorov-Smirnov Test), KL 발산 ([Kullback-Leibler Divergence](/knowledge-base/studynote/10_ai/05_data_science_ml/347_cross_entropy_kld/)), Jensen-Shannon Divergence 같은 통계 거리를 사용해 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)별 변화를 측정한다. 수치형과 범주형, 단일 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)와 결합 분포에 따라 적합한 지표가 달라지므로 "한 개 지표로 끝내는 감시"는 보통 부족하다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Drift monitoring loop</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Training data -&gt; baseline stats / schema</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Live feature window -&gt; drift scorer -&gt; alert threshold</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ PSI / KS / KL / Jensen-Shannon</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ segment-level comparison</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Root-cause analysis -&gt; retrain / preprocess fix / threshold tune</div></div>
</div>
</div>



| 감시 대상 | 대표 지표 | 해석 포인트 |
| :--- | :--- | :--- |
| 수치형 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) | KS 검정, Wasserstein Distance | 평균이 같아도 꼬리 분포가 달라질 수 있다. |
| 범주형 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) | PSI, Jensen-Shannon Divergence | 신규 범주 출현과 비율 급변을 함께 봐야 한다. |
| 다변량 조합 | [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) 거리, [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 후 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 개별 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)는 멀쩡해도 조합 분포는 달라질 수 있다. |
| 세그먼트별 입력 | 국가·기기·시간대별 비교 | 전체 평균이 정상이어도 특정 집단에서만 붕괴가 날 수 있다. |

여기서 중요한 실무 포인트는 <strong>라벨 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong>이다. 사기 탐지나 이탈 예측처럼 정답이 며칠, 몇 주 뒤에야 확정되면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 직접 보기 전에 입력 분포 이상부터 먼저 감지해야 한다. 그래서 [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링은 모델 정확도 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링의 대체재가 아니라, 늦게 도착하는 정답을 기다리기 전에 위험 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 잡는 조기 경보 체계다.

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 감시는 냉장고 온도계를 다는 것과 같다. 음식이 상한 뒤에 냄새를 맡는 것보다, 온도가 평소보다 올라가는 순간 먼저 알아차리는 편이 훨씬 안전하다.

---

## Ⅲ. 비교 및 연결

[데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)를 제대로 대응하려면 비슷해 보이는 다른 문제와 경계를 나눠야 한다. 특히 [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/), 타깃 드리프트, [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew는 이름이 비슷해도 원인과 처방이 다르다.

| 구분 | 무엇이 변하는가 | 대표 원인 | 주된 대응 |
| :--- | :--- | :--- | :--- |
| [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) | 입력 분포 `P(X)` | 계절성, 사용자군 변화, 센서 상태 변화 | 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 반영, 전처리 조정, 선택적 재학습 |
| [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) | 조건부 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) `P(Y|X)` | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경, 시장 룰 변화, 외부 충격 | 룰 재학습, 과거 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 축소, 모델 재설계 |
| 타깃 드리프트 (Target Drift) | 정답 분포 `P(Y)` | 클래스 불균형 변화, 이벤트 빈도 변화 | 임계값 조정, 재표본화, 캘리브레이션 |
| [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew | 학습·서빙 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 불일치 | 전처리 코드 차이, 누락된 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/), [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 미스매치 | [피처 스토어](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)([Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)), 공통 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, 배포 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |

이 비교가 중요한 이유는 [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 경보가 떠도 실제 문제는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 버그일 수 있기 때문이다. 예를 들어 학습 때는 결측치를 평균으로 채웠는데 서빙에서는 결측치를 0으로 넣고 있다면, 분포 차이는 자연 현상이 아니라 시스템 구현 오류다. 반대로 입력 분포가 크게 달라졌어도 그 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)가 모델에서 거의 쓰이지 않는다면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향은 제한적일 수 있다.

따라서 드리프트 분석은 항상 "무엇이 변했는가"와 "그 변화가 정말 예측 품질을 흔드는가"를 함께 묻는 방식이어야 한다. 통계적 차이와 비즈니스 영향은 같지 않다.

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)와 다른 문제를 구분하는 일은 몸살, 감기, 알레르기, 약 부작용을 구분하는 진단과 같다. 다 열이 나 보일 수 있지만, 원인을 잘못 짚으면 약도 틀리게 처방된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 드리프트를 "잡아내는 것"보다 "어떻게 다룰 것인가"가 더 중요하다. 모든 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 동일하게 감시하면 잡음이 많아지고, 모든 경보에 전체 재학습을 걸면 비용이 폭증한다. 따라서 중요 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/), 핵심 세그먼트, 비즈니스 임계값을 먼저 정하고 운영해야 한다.

| 시나리오 | 흔한 드리프트 원인 | 권장 판단 |
| :--- | :--- | :--- |
| [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) | 계절성 검색어, 신규 유저 유입, 캠페인 유입 채널 변화 | 최근 기간 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 강화, 세그먼트별 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 주기적 재학습 |
| 컴퓨터 비전 품질 검사 | 카메라 교체, 조명 변화, 렌즈 오염 | 전처리 재보정, 샘플 재라벨링, 배포 전 shadow 테스트 |
| 이상 거래 탐지 | 결제 채널 구조 변화, 국가별 이용 패턴 변화 | 고위험 세그먼트 우선 감시, 임계값 조정, 부분 재학습 |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 학습 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)이 전체 평균뿐 아니라 국가, 기기, 시간대 같은 세그먼트까지 포함하는가?
2. 드리프트 지표와 실제 비즈니스 지표 전환율, 오탐 비용, [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 함께 보고 있는가?
3. 알람 발생 후 재학습, 전처리 수정, 임계값 재조정 중 어떤 경로로 대응할지 런북(runbook)이 준비되어 있는가?
4. 정답 라벨이 늦게 들어오는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이라면 입력 드리프트를 조기 경보로 활용하고 있는가?
5. [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)와 [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew를 구분할 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 있는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 평균값 몇 개만 비교하고 "문제 없음"이라고 결론내리는 운영
- 모든 드리프트 알람에 무조건 전체 재학습을 연결하는 구성
- 전체 분포만 보고 소수 세그먼트 붕괴를 놓치는 대시보드
- 중요하지 않은 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)의 미세한 흔들림을 과대 해석해 경보 피로를 만드는 운영

기술사 답안에서는 <strong>"<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">데이터 드리프트</a>는 배포 후 입력 환경 변화에 따른 통계적 분포 이동이며, <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하 여부와 원인 구분을 위해 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링·세그먼트 분석·재학습 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>을 함께 설계해야 한다"</strong>라고 정리하면 실무적 깊이가 살아난다.

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 대응은 기상 특보를 보고 바로 학교를 폐쇄하는 일이 아니라, 비의 양과 지역, 등굣길 상황을 보고 우산만 챙길지 휴교할지 결정하는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

[데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)를 체계적으로 다루면 모델 운영은 "한 번 배포한 뒤 운에 맡기는 일"이 아니라, 변화하는 환경을 관찰하며 품질을 유지하는 관리 체계가 된다. 그 결과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락을 더 빨리 발견하고, 필요한 경우에만 재학습해 비용을 통제하며, 예측 품질과 비즈니스 성과를 함께 안정화할 수 있다.

다만 모든 변화가 나쁜 것은 아니다. 입력 분포 변화가 곧바로 모델 실패를 뜻하지는 않으며, 지나친 경보 체계는 운영팀을 지치게 만든다. 그래서 기억해야 할 핵심은 [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)를 "무조건 막아야 하는 적"으로 보는 것이 아니라, <strong>운영 중인 모델이 현실과 얼마나 멀어졌는지를 재는 계기판</strong>으로 이해하는 것이다.

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 자동차 바퀴의 마모 상태를 알려 주는 계기판과 같다. 계기판이 있다고 매일 타이어를 갈 필요는 없지만, 경고를 무시하면 결국 큰 사고로 이어진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/knowledge-base/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/)) | [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) 감시, 재학습, 배포 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 포함하는 운영 체계다. |
| [Concept Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) | 입력이 아니라 정답 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 자체가 바뀌는 더 근본적인 변화다. |
| [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)-Serving Skew | 자연스러운 분포 변화가 아니라 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구현 차이에서 오는 불일치다. |
| [Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) | 학습과 서빙의 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의를 일치시키는 핵심 인프라다. |
| PSI ([Population Stability Index](/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/)) | 범주형·구간화된 입력 변화 감시에 자주 쓰이는 지표다. |
| [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) | 드리프트 대응을 자동화하는 재학습 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 연결된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">정적 오프라인 학습 데이터</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">운영 입력 모니터링</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">피처별 분포 거리 계산</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">원인 분석</div>
<div class="kb-diagram-tree-item" style="--depth:2">계절성 변화</div>
<div class="kb-diagram-tree-item" style="--depth:2">사용자군 변화</div>
<div class="kb-diagram-tree-item" style="--depth:2">센서 / 채널 변화</div>
<div class="kb-diagram-tree-item" style="--depth:2">파이프라인 오류 구분</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">재학습 · 전처리 수정 · 임계값 조정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">폐루프 MLOps 운영</div>
</div>
</div>



이 흐름은 [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)가 단순 통계 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)에서 출발해, 원인 분석과 운영 자동화까지 연결되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 로봇이 봄 사진만 배우고 나서 갑자기 겨울 풍경을 많이 보게 되는 것과 비슷해요.
2. 로봇이 고장 난 건 아니지만, 익숙한 모습이 달라져서 예전보다 헷갈릴 수 있어요.
3. 그래서 어른들은 로봇이 보는 세상이 얼마나 달라졌는지 계속 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 필요하면 새 사진으로 다시 연습시켜 준답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 175 / 420

← **이전**: [174. MLOps (Machine Learning Operations)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/174_mlops/)
**다음**: [176. 컨셉 드리프트 (Concept Drift)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/176_concept_drift/) →

---
