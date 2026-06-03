+++
title = "322. 데이터 드리프트 (Data Drift) / 컨셉 드리프트 (Concept Drift)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/))는 모델 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 통계적 분포가 시간에 따라 변화하는 현상이고, [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/))는 입력-출력 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 자체(P(Y|X))가 변화하는 더 근본적인 현상으로, 두 드리프트 모두 배포된 ML 모델의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 저하시키는 주요 원인이다.
> 2. **가치**: 드리프트를 조기에 탐지하고 자동 재학습 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)를 설계하는 것이 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링의 핵심이며, 특히 금융·의료·마케팅처럼 세상이 빠르게 변하는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 모델 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 유지의 생명선이다.
> 3. **판단 포인트**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 통계 검정(PSI, [KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/), KS Test)으로 탐지 가능하지만, [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)는 실제 레이블이 있어야 탐지 가능하여 탐지가 더 어렵다. 라벨 없이 드리프트를 탐지하는 비지도 탐지 방법이 중요한 이유다.

---

## Ⅰ. 개요 및 필요성

2019년 코로나 이전에 학습한 여행 수요 예측 모델이 있다. 2020년 팬데믹 이후 여행 패턴이 완전히 바뀌어([컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) 모델 정확도가 폭락했다. [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 없이 그대로 두면 잘못된 예측으로 항공사가 수천억 원의 좌석 과잉 공급·재고 손실을 본다.

이것이 드리프트 문제다. ML 모델은 훈련 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포를 학습하는데, 세상이 변하면(코로나·경제 위기·계절 변화·사용자 행동 변화 등) 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 분포 간 격차가 벌어진다. 이 격차를 탐지하지 않으면 모델은 "오래된 지식으로 새 세상을 예측하는" 최악의 상황이 된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Background Problem → Need → Adoption Value</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Existing limitation</div><div class="kb-diagram-cell">Operational pressure</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">New requirement</div><div class="kb-diagram-cell">Design decision point</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 드리프트는 수면 밑에서 서서히 이동하는 빙하다. 표면(모델 예측)은 멀쩡해 보이지만 수면 아래([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포)가 천천히 이동해, 언젠가 배(모델)가 빙하에 부딪힌다. 빙하 감지 시스템(드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링) 없이는 타이타닉 사고를 예방할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">드리프트 유형 분류 및 탐지 방법</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 데이터 드리프트 (Data Drift / Feature Drift):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P_train(X) ≠ P_serve(X) — 입력 분포 변화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">예: 원래 25~35세 고객 → 현재 45~55세 고객으로 이동</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐지: 통계 검정 (레이블 불필요)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 컨셉 드리프트 (Concept Drift):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P_train(Y</div><div class="kb-diagram-cell">X) ≠ P_serve(Y</div><div class="kb-diagram-cell">X) — 입력-출력 관계 변화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">예: 같은 나이 고객이 코로나 전후로 다른 구매 행동</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐지: 실제 레이블 수집 필요 (지연 탐지)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 라벨 드리프트 (Label Drift):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P_train(Y) ≠ P_serve(Y) — 출력 클래스 분포 변화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">예: 사기 탐지에서 사기 비율이 갑자기 증가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">탐지 방법:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">방법</div><div class="kb-diagram-cell">적용 대상</div><div class="kb-diagram-cell">핵심 원리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">KS Test</div><div class="kb-diagram-cell">단변량 연속</div><div class="kb-diagram-cell">분포 누적함수 최대 차이</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PSI (Population</div><div class="kb-diagram-cell">범주형/연속</div><div class="kb-diagram-cell">분포 변화율 측정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stability Index)</div><div class="kb-diagram-cell">PSI&gt;0.25: 심각한 드리프트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">KL Divergence</div><div class="kb-diagram-cell">확률 분포</div><div class="kb-diagram-cell">두 분포의 정보 차이</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MMD (Maximum</div><div class="kb-diagram-cell">고차원</div><div class="kb-diagram-cell">커널 거리 측정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Mean Discrepancy)</div></div>
</div>
</div>



| 드리프트 유형 | P 변화 | 탐지 난이도 | 대응 방법 |
|:---|:---|:---|:---|
| [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) | P(X) 변화 | 쉬움 (레이블 불필요) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재전처리, 재학습 |
| [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) | P(Y|X) 변화 | 어려움 (레이블 필요) | 지속적 레이블 수집 + 재학습 |
| 라벨 드리프트 | P(Y) 변화 | 중간 | 클래스 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 조정 |
| 공변량 드리프트 | P(X) 변화 (P(Y|X) 동일) | 쉬움 | 입력 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 업데이트 |

- **📢 섹션 요약 비유**: [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) vs [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)의 차이는 다음과 같다. [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)는 고객 연령대가 바뀐 것(X 분포 변화)이고, [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)는 같은 연령대 고객이 코로나 전후로 완전히 다른 방식으로 쇼핑하는 것(X→Y [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화)이다. 전자는 통계로 잡히지만, 후자는 실제 결과(레이블)가 쌓여야 발견된다.

---

## Ⅲ. 비교 및 연결

<strong>PSI (<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/417_mlops_data_drift_psi/">Population Stability Index</a>)</strong> 해석 기준:
- PSI < 0.1: 안정 (재학습 불필요)
- 0.1 ≤ PSI < 0.2: 약간 변화 (주의 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링)
- PSI ≥ 0.2: 심각한 드리프트 (즉각 재학습 권고)
- PSI ≥ 0.25: 완전 모델 교체 고려

<strong>드리프트 대응 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>:
1. <strong>재학습 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong>: 드리프트 탐지 시 자동 재학습 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 실행
2. **슬라이딩 윈도우**: 최근 N일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 학습 (오래된 패턴 제거)
3. **온라인 학습**: 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어올 때마다 점진적 모델 업데이트

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) / [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: PSI 0.25 기준은 혈압 정상 범위와 같다. 수축기 혈압 120mmHg 이하(PSI<0.1)는 건강하고, 140mmHg 이상(PSI>0.2)은 약 처방(재학습)이 필요하고, 180mmHg 이상(PSI>0.25)은 응급실(모델 교체)이다. 혈압을 지속적으로 측정하지 않으면 갑자기 쓰러진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>드리프트 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링 시스템 설계</strong>:
1. <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">기준선</a>(<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a>) 수립</strong>: 훈련 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 각 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 분포 통계(평균, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), 분위수) 저장
2. **정기 스캔**: 일별/주별 프로덕션 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 비교 (PSI, KS Test)
3. <strong>알람 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: PSI > 0.2 시 슬랙(Slack) 알림 + JIRA 티켓 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
4. **Shadow Mode**: 새 재학습 모델을 프로덕션 트래픽의 5%에 적용해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교
5. **점진적 롤아웃**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 후 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) → 블루-그린 → 전체 전환

<strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/">섀도우 배포</a>(<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/118_shadow_deployment_traffic_mirroring/">Shadow Deployment</a>)와 연계</strong>: 드리프트로 재학습된 새 모델을 즉시 프로덕션에 배포하지 않고, 실제 트래픽을 그대로 복사하여 새 모델로 보내 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한 후 전환한다. 재학습으로 오히려 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하되는 역주행(Negative Transfer)을 방지한다.

- **📢 섹션 요약 비유**: [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/)는 새 요리사의 시험 채용이다. 식당 주방(프로덕션)에서는 기존 요리사가 계속 요리하고(기존 모델), 새 요리사(재학습 모델)는 옆에서 같은 주문을 받아 똑같이 요리해본다(섀도우). 새 요리가 더 맛있으면([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) 그때 교대한다. 손님 [클레임](/knowledge-base/studynote/09_security/11_iam_access_control/539_claims/)([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애) 없이 요리사를 교체하는 완벽한 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅴ. 기대효과 및 결론

드리프트 감지와 자동 재학습은 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) Level 2의 핵심이자, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 장기 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 보장을 위한 핵심 인프라다. 특히 금융 사기 탐지(사기 패턴이 매주 변함), 의료 진단(질병 패턴 변화), 마케팅 추천(계절·트렌드 변화)처럼 동적인 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 없는 ML [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 "시간 폭탄"이다. 자동화된 드리프트 탐지 → 재학습 → 배포 사이클이 살아있는(Evergreen) [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템의 핵심이다.

- **📢 섹션 요약 비유**: 드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링은 AI의 건강검진 시스템이다. 사람도 매년 건강검진(정기 드리프트 체크)을 받고 혈압·혈당(PSI)이 기준을 넘으면 약(재학습)을 처방받는다. 검진을 안 하면 증상이 없어 보여도 속에서 병이 자라다가 갑자기 쓰러진다(모델 정확도 급락). [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)도 주기적 건강검진이 필수다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) | P(X) 변화, PSI, KS Test / 입력 특성 분포 변화 탐지 |
| [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) | P(Y / X) 변화, 레이블 필요 / 입력-출력 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화, 더 근본적 문제 |
| PSI | 0.1/0.2/0.25 기준 / 드리프트 심각도 측정 표준 지표 |
| [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) | 자동 재학습, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD / 드리프트 탐지-대응 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 |
| [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/) | 트래픽 복사, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) / 재학습 모델 안전 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 방법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] → [데이터 드리프트 (Data Drift) / 컨셉 드리프트 (Concept Drift)] → [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>드리프트</strong>는 AI가 배운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 현실의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 <strong>서서히 달라지는 현상</strong>이에요 — 코로나처럼 세상이 바뀌면 "예전 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"가 갑자기 엉터리가 돼요!
2. <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/">데이터 드리프트</a></strong>는 고객 나이대가 바뀐 것, <strong><a href="/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/">컨셉 드리프트</a></strong>는 같은 고객이 완전히 다르게 쇼핑하는 것으로, 후자가 더 발견하기 어려워요.
3. 정기적으로 AI를 **건강검진**(드리프트 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링)하고, 이상이 발견되면 <strong>자동으로 재학습</strong>시키는 게 MLOps의 핵심이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 322 / 420

← **이전**: [321. MLOps (Machine Learning Operations)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/321_mlops_pipeline/)
**다음**: [323. 피처 스토어 (Feature Store)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/323_feature_store/) →

---
