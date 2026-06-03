+++
title = "184. A/B 테스팅, 섀도우 배포, 카나리 롤아웃 (A/B Testing, Shadow Deployment, Canary Rollout)"
date = 2026-05-06

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/), [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃, A/B 테스팅은 새 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 모델을 한 번에 전면 교체하지 않고, 실트래픽 아래에서 기술적 안전성과 비즈니스 효과를 단계적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 런타임 서빙 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: AI는 500 오류 없이도 추천 품질 저하, 유해 응답, 편향 확대처럼 "조용한 실패"를 낼 수 있으므로, 오프라인 점수만으로는 배포 판단을 내리기 어렵다.
> 3. **판단 포인트**: Shadow는 노출 없이 동작 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), Canary는 제한된 실제 노출로 위험 통제, A/B는 통계적으로 성과 비교를 수행하므로, 세 기법은 대체 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)가 아니라 Shadow → [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) → A/B 순의 게이트로 조합하는 편이 안전하다.

---

## Ⅰ. 개요 및 필요성

전통 소프트웨어 배포는 "정상 동작하는가"가 핵심 질문이지만, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 배포는 "정상 동작처럼 보이면서도 잘못된 판단을 조용히 내리지 않는가"까지 봐야 한다. 예를 들어 추천 모델이 에러를 내지는 않더라도 클릭률을 떨어뜨리거나, [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델이 특정 집단에 편향된 결과를 내거나, [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) ([Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))이 금지된 답변을 더 자주 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 수 있다. 그래서 오프라인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋의 정확도 하나만 보고 실서비스 모델을 갈아끼우는 것은 매우 위험하다.

문제의 원인은 온라인 환경이 오프라인 실험실과 다르기 때문이다. 실제 요청은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 누락, 최신 사용자 행동, 계절성, 배포 직후의 캐시 상태, 후행 라벨 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)까지 함께 포함한다. 즉 모델 품질은 학습 코드의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)만이 아니라, <strong>서빙 시스템·트래픽 분포·사용자 반응</strong>이 결합된 결과다.

이 때문에 현대 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) ([Machine Learning Operations](/knowledge-base/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/))는 빅뱅 배포보다 점진적 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 택한다. 먼저 실트래픽을 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 모델을 숨은 상태로 시험하고, 그다음 일부 사용자에게만 노출하며, 마지막에는 무작위 실험으로 기존 모델과 사업 성과를 비교한다. [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/), [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃, A/B 테스팅이 바로 이 세 단계를 맡는다.

- **📢 섹션 요약 비유**: 새 비행기를 만들었다고 바로 모든 승객을 태우지 않고, 먼저 무인 시험비행을 하고, 다음에는 소수 노선만 띄워 보고, 마지막에 기존 기종과 운영 성과를 비교하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

세 기법의 공통 기반은 챔피언-챌린저(Champion-Challenger) 구조다. 현재 운영 모델을 챔피언, 새 모델을 챌린저로 두고, 트래픽 라우터가 요청을 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하거나 분기한다. 여기에 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집기, 안전 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 검사기, 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 컨트롤러가 붙어야 실제 운영 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 된다.

아래 그림은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 런타임 배포의 단계별 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 요약한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Runtime rollout ladder                                              │
├──────────────────────────────────────────────────────────────────────┤
│ User request                                                        │
│      │                                                              │
│      ▼                                                              │
│  Traffic router / feature parity check                              │
│      │                                                              │
│      ├─ Champion model (v1) ----------------------> user response   │
│      │                                                              │
│      └─ Challenger model (v2)                                       │
│           ├─ Shadow  : mirrored only, log output diff               │
│           ├─ Canary  : 1~5% real exposure, guardrail check          │
│           └─ A/B test: randomized cohorts, KPI comparison           │
│                                                                      │
│ Metrics: latency, error, unsafe rate, business conversion           │
│ Gate   : auto rollback / traffic promotion                          │
└──────────────────────────────────────────────────────────────────────┘
```

Shadow Deployment의 핵심은 요청 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)(Traffic Mirroring)다. 챌린저 모델은 실제 요청을 받지만 사용자에게 응답을 보내지 않는다. 이때 중요한 구현 규칙은 "비동기 fire-and-forget"이다. 즉 챔피언 응답이 준비되면 바로 사용자에게 보내고, 챌린저의 처리 시간은 사용자 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간에 영향을 주지 않도록 격리해야 한다. 또한 결제, 알림 발송, 캐시 갱신 같은 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부작용은 섀도우 경로에서 차단하거나 샌드박스로 우회해야 한다.

[Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) Rollout은 일부 사용자에게만 실제 결과를 노출해 위험 반경을 줄인다. 보통 1% → 5% → [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% → 50%처럼 단계적으로 트래픽을 늘리며, [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)) 위반, 안전 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반, 고객 불만, 에러율 상승이 있으면 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)한다. A/B Testing은 이보다 목적이 다르다. [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)가 "안전하게 배포할 수 있는가"를 보는 단계라면, A/B는 통계적으로 유의미한 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) ([Key Performance Indicator](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/020_kpi/)) 개선이 있는가를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 실험 단계다.

| 기법 | 사용자 노출 | 주 지표 | 핵심 질문 | 구현 주의점 |
| :--- | :--- | :--- | :--- | :--- |
| [Shadow Deployment](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/118_shadow_deployment_traffic_mirroring/) | 0% | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 출력 차이, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반율 | 새 모델이 실환경에서 기술적으로 버티는가? | 응답 대기 금지, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부작용 격리 |
| [Canary Rollout](/knowledge-base/studynote/14_data_engineering/04_mlops/170_ab_test_canary_rollout_shadow_mirroring/) | 소수(1~5% 등) | [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), 오류율, 신고율, 안전성 | 작게 노출했을 때 사고 없이 확장 가능한가? | 빠른 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 코호트 정의, [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) |
| A/B Testing | 실험군/대조군 분할 | 전환율, [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) (Click-Through Rate), 유지율, 매출 | 기존 모델보다 실제 성과가 더 좋은가? | 무작위화, 표본 크기, 통계 검정 |

- **📢 섹션 요약 비유**: Shadow는 backstage 리허설, Canary는 일부 관객 앞 공개 리허설, A/B는 두 공연팀을 나눠 실제 관객 반응을 비교하는 본실험과 같다.

---

## Ⅲ. 비교 및 연결

이 세 기법은 종종 한 묶음으로 불리지만, 해결하는 문제가 서로 다르다. Shadow는 기술적 관찰, Canary는 운영 안정성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), A/B는 사업 성과 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에 초점이 있다. 따라서 Shadow 결과만 좋다고 바로 A/B로 가는 것도 위험하고, [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 성공만으로 비즈니스 개선이 증명되는 것도 아니다.

| 비교 축 | [Shadow Deployment](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/118_shadow_deployment_traffic_mirroring/) | [Canary Rollout](/knowledge-base/studynote/14_data_engineering/04_mlops/170_ab_test_canary_rollout_shadow_mirroring/) | A/B Testing | [Blue-Green Deployment](/knowledge-base/studynote/12_it_management/05_security_compliance/304_process/) |
| :--- | :--- | :--- | :--- | :--- |
| 주 목적 | 숨은 실행 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 제한적 실노출 안전성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 성과 우열 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 환경 전환 단순화 |
| 사용자 체감 | 없음 | 일부만 새 결과 체감 | 실험군만 체감 | 전환 시 전체가 바뀜 |
| 주 판단 기준 | 출력 차이, [latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 안전 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 오류율, [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), 민감 이벤트 | [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/), 통계 유의성 | 전환 성공 여부 |
| 강점 | 위험 거의 없음 | 폭발 반경 통제 | 사업 효과 입증 | 인프라 전환이 단순 |
| 한계 | 사용자 반응을 모름 | 표본이 적으면 장기 효과 불명확 | 안전성 보장은 별도 필요 | AI의 조용한 실패 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 약함 |

연결 관점에서 보면, Shadow와 Canary는 Continuous Delivery의 안전 장치이고, A/B는 제품 실험 프레임워크에 가깝다. 또 183번 AutoML이 오프라인에서 좋은 후보를 찾는 과정이라면, 184번은 그 후보가 **실제 서빙 환경에서 승격될 자격이 있는지** [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 과정이다. 오프라인 튜닝과 온라인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 같은 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 안의 앞뒤 단계다.

한편 다중 팔 밴딧(Multi-Armed Bandit) 기법은 A/B 테스트 이후의 자동화 확장 모델로 볼 수 있다. 하지만 기본적으로는 통계적으로 안정된 Shadow/[Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)/A/B 체계를 먼저 갖춘 뒤에 써야 한다. 기초 관측과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치 없이 밴딧만 적용하면, 잘못된 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 더 빠르게 증폭할 수 있다.

- **📢 섹션 요약 비유**: Shadow는 새 선수가 몸상태를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 훈련, Canary는 교체 출전, A/B는 두 선수의 실제 경기 기록 비교, Multi-Armed Bandit은 경기 중 감독이 더 잘하는 쪽에 출전 시간을 더 몰아주는 운영과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "어떤 모델인가"보다 "어떤 실패가 가장 비싼가"를 먼저 정의해야 한다. 예를 들어 광고 추천은 전환율 저하가 핵심 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)이지만, 의료·금융 판단 모델은 작은 오판도 법적·윤리적 손실이 크다. 그래서 고위험 모델일수록 Shadow 기간을 길게 가져가고, [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 비율을 천천히 늘리며, 인간 검토(Human [Review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/))나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진을 함께 붙이는 편이 안전하다.

| 실무 시나리오 | 권장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 이유 |
| :--- | :--- | :--- |
| 추천/검색 랭킹 모델 | Shadow → [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) → A/B | 기술 안정성과 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/), 전환율을 모두 봐야 함 |
| [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 챗봇 | 긴 Shadow + 소규모 [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) + 유해성 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반과 브랜드 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)가 큼 |
| 사기 탐지 모델 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) Shadow 점수 비교 후 제한적 [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | 잘못된 차단/승인은 즉시 비용 발생 |
| 수요예측·배치 모델 | Shadow 또는 Backtest 중심, 필요 시 [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | 온라인 직접 노출보다 후행 정확도 중요 |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 챔피언과 챌린저가 같은 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 정의를 쓰고 있는가, 즉 Feature Skew가 없는가?
2. Shadow 경로가 실제 사용자 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 부작용에 영향을 주지 않는가?
3. Canary의 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)가 명확한가? 예: p95 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, unsafe response rate, 신고율.
4. A/B 실험은 코호트 고정(sticky assignment)과 충분한 표본 크기를 보장하는가?
5. 라벨 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 긴 문제라면 단기 가드레일 지표와 장기 KPI를 분리해 관리하는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 오프라인 정확도가 높다는 이유만으로 Shadow를 건너뛰는 배포
- Shadow 트래픽에서도 외부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출·결제·알림이 실제로 일어나 중복 부작용을 만드는 설계
- Canary를 내부 직원 몇 명 테스트와 혼동해 대표성 없는 샘플로 판단하는 운영
- A/B 결과를 보기 전에 이미 트래픽 비율을 계속 바꿔 통계 해석을 망치는 경우
- KPI만 보고 안전 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반이나 공정성 저하를 놓치는 경우

기술사 답안에서는 세 기법을 "점진적 배포" 하나로 뭉뚱그리기보다, <strong>Shadow는 기술 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>, Canary는 운영 <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a> 제어, A/B는 사업 효과 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>이라는 역할 차이를 분명히 쓰는 것이 중요하다. 그리고 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델은 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)보다 <strong>무해한 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>이 더 본질적이라는 문장을 함께 남기면 좋다.

- **📢 섹션 요약 비유**: 좋은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포는 새 요리 레시피를 바로 전 손님에게 내는 것이 아니라, 주방 안 연습·일부 시식·메뉴 경쟁 평가를 차례대로 거치는 식당 운영과 같다.

---

## Ⅴ. 기대효과 및 결론

이 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 정착되면 모델 배포는 두려운 일회성 작업이 아니라, 관측 가능하고 되돌릴 수 있는 운영 절차가 된다. 시스템 팀은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 오류를 통제하고, 제품 팀은 실사용 성과를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하며, [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 팀은 안전 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 여부를 함께 볼 수 있다. 즉 모델 승격이 개발자 감이 아니라 측정 가능한 증거에 기반하게 된다.

물론 비용도 있다. Shadow는 두 모델을 동시에 돌려 인프라 비용이 늘고, Canary와 A/B는 실험 설계·통계 해석·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 체계가 필요하다. 하지만 전면 배포 후 대규모 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 고객 피해, 브랜드 손상을 생각하면 이 비용은 일종의 보험료에 가깝다.

결론적으로 기억할 구조는 단순하다. <strong>Shadow로 숨어서 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>하고, Canary로 작게 노출하고, A/B로 이길 가치가 있는지 증명한 뒤 전면 승격한다.</strong> [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 런타임에서 안전한 배포란 빠른 배포가 아니라, 실패의 반경을 단계적으로 줄이며 학습하는 배포다.

- **📢 섹션 요약 비유**: 훌륭한 배포 체계는 새 다리를 만들자마자 모든 차를 올리는 것이 아니라, 먼저 하중 시험을 하고, 일부 차량만 통과시켜 보고, 기존 다리와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 비교한 뒤에야 전면 개통하는 방식과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Champion-Challenger | 기존 모델과 신규 모델을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 비교하는 기본 운영 구조다. |
| Feature Skew | 학습/서빙 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 불일치가 온라인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락을 만드는 대표 원인이다. |
| [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)) | [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 단계에서 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 여부를 판단하는 운영 기준이다. |
| [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) ([Key Performance Indicator](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/020_kpi/)) | A/B 테스트에서 모델 승패를 결정하는 사업 지표다. |
| Multi-Armed Bandit | A/B 이후 트래픽 비율을 동적으로 조정하는 고도화 기법이다. |
| [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) / [Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) | Shadow와 [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 구현하는 핵심 인프라다. |

### 📈 관련 키워드 및 발전 흐름도

```text
오프라인 평가
    │
    ▼
Shadow Deployment
    │
    ├─ 출력 차이 분석
    ├─ 지연시간·안전성 검증
    └─ 부작용 격리 확인
    │
    ▼
Canary Rollout
    │
    ▼
A/B Testing
    │
    ▼
Full Rollout 또는 Multi-Armed Bandit 최적화
```

이 흐름은 "기술적으로 되는가"에서 시작해 "안전하게 노출할 수 있는가", 그리고 "사업적으로 이득인가"로 질문이 점점 바뀌는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Shadow는 새 로봇이 손님 몰래 뒤에서 연습만 해 보는 단계예요.
2. Canary는 손님 중 아주 조금만 새 로봇 음식을 먹어 보고 괜찮은지 보는 단계예요.
3. A/B는 두 로봇이 만든 음식을 나눠 주고 어느 쪽을 사람들이 더 좋아하는지 공평하게 비교하는 단계예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 184 / 420

← **이전**: [183. 하이퍼파라미터 오토튜닝과 NAS (AutoML)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/183_automl_nas/)
**다음**: [185. GPU 아키텍처 기반 텐서 코어 (Tensor Core GPU Architecture)](/knowledge-base/studynote/10_ai/02_dl_architecture_new/185_tensor_core_gpu/) →

---
