+++
title = "333. A/B 테스팅 / 섀도우 배포 (Shadow Deployment) / 카나리 (Canary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: A/B 테스팅·[섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/)·[카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)는 ML 모델을 프로덕션 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 안전하게 전환하는 **점진적 배포(Progressive Delivery)** [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로, 실제 트래픽의 일부 또는 복사본에서 새 모델을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여 전체 배포 실패 위험을 최소화한다.
> 2. **가치**: 새 모델이 학습 환경에서는 우수했지만 프로덕션 트래픽에서 실패하는 "Lab-to-Production 갭"을 줄이며, 장애 발생 시 영향 범위를 제한하고 즉각 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 가능한 안전망을 제공한다.
> 3. **판단 포인트**: 세 가지 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 핵심 차이는 <strong>트래픽 노출 여부와 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/">피드백 루프</a></strong>다 — 섀도우는 실제 트래픽 복사로 사용자 영향 없이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 소수 사용자에게 실제 노출, A/B는 두 그룹에 다른 모델을 적용하여 비즈니스 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 비교한다.

---

## Ⅰ. 개요 및 필요성

재학습된 추천 모델이 오프라인 평가에서 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/)(Click-Through Rate)이 5% 향상됐다. 바로 전체 프로덕션에 배포할 수 있을까? 안 된다. 오프라인 평가와 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 차이(Distribution Shift), 예상치 못한 에지 케이스, 인프라 이슈가 있을 수 있다.

<strong>점진적 배포 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>은 이 위험을 단계적으로 줄인다:
1. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/">섀도우 배포</a></strong>: 사용자 영향 없이 트래픽 복사본으로 새 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
2. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a></strong>: 1~5% 사용자에게 새 모델 노출, 실제 반응 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
3. **A/B 테스팅**: 통계적으로 유의미한 규모로 두 모델을 비교

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 새 요리를 식당에 올리기 전 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 과정이다. 섀도우는 주방에서 몰래 새 레시피로 맛을 보는 것(손님에게 안 냄), [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 VIP 손님 3명에게 먼저 맛보게 하는 것, A/B는 절반 손님에게 기존 메뉴, 나머지 절반에게 새 메뉴를 내고 재방문율을 비교하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|         점진적 배포 전략 3종 비교 아키텍처                            |
+------------------------------------------------------------------+
|                                                                  |
|  ① 섀도우 배포 (Shadow Deployment):                               |
|  실제 트래픽 ------> 현재 모델 (Champion) ------> 사용자에게 응답 전송 |
|              +-----> 새 모델 (Shadow) ---------> 응답 로깅만 (미전송) |
|  효과: 사용자 영향 0, 새 모델 성능/오류 완전 검증 가능               |
|                                                                  |
|  ② 카나리 배포 (Canary Release):                                   |
|  실제 트래픽 ------> 라우터 ---- 95% -----> 현재 모델 -> 사용자        |
|                          +-- 5% ------> 새 모델 -> 사용자           |
|  효과: 5%만 영향, 실제 사용자 반응 확인, 이상 시 즉시 롤백           |
|                                                                  |
|  ③ A/B 테스팅 (A/B Testing):                                      |
|  사용자 그룹 A(50%) -----> 모델 A (현재)                            |
|  사용자 그룹 B(50%) -----> 모델 B (새 모델)                         |
|  -> 두 그룹의 비즈니스 메트릭(CTR, 전환율, 매출) 통계 비교            |
|  -> 유의확률 p < 0.05이면 새 모델로 전환                            |
|                                                                  |
|  배포 단계 (Best Practice):                                       |
|  섀도우(검증) -> 카나리 1%(안전 확인) -> 10% -> 50% -> 100%(전체 전환)  |
+------------------------------------------------------------------+
```

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 사용자 영향 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 방식 | 적합 상황 |
|:---|:---|:---|:---|
| [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/) | 없음 | 응답 로깅 비교 | 처음 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 안전 최우선 |
| [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) | 소수(1~5%) | 실제 반응 + 에러율 | 점진적 전환 |
| A/B 테스팅 | 대규모(50%+) | 통계적 유의성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 비즈니스 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 비교 |
| [블루-그린 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/194_blue_green_deployment_strategy/) | 전환 순간 | 즉시 전환 + [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 인프라 변경 없는 배포 |

- **📢 섹션 요약 비유**: [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)는 광산 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)아에서 유래했다. 광부들이 독가스 탐지를 위해 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)아를 먼저 갱도에 보냈듯, 새 모델을 소수 사용자([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)아)에게 먼저 노출시켜 문제(독가스)가 있으면 나머지 사용자(광부들)가 피해를 입기 전에 즉시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)한다.

---

## Ⅲ. 비교 및 연결

**A/B 테스팅 통계적 유의성**:
- **귀무가설(H₀)**: 두 모델의 CTR에 차이가 없다
- <strong>유의확률(<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/337_p_value_significance/">p-value</a>)</strong>: p < 0.05이면 차이가 통계적으로 유의미하다고 판단
- **샘플 크기**: 검정력([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/)) 80%, 효과 크기(Effect Size), α=0.05 기준으로 필요 샘플 수 계산
- <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/">AA</a> 테스트</strong>: A/B 전에 동일 모델을 A/A로 테스트하여 테스트 인프라 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

**멀티암드 밴딧(Multi-Armed Bandit) vs A/B 테스팅**: A/B는 실험 기간 고정 할당, 밴딧은 실시간으로 더 좋은 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에 더 많은 트래픽 자동 할당. 속도 vs 통계적 순도의 트레이드오프.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| A/B 테스팅 / [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/) ([Shadow Deployment](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/118_shadow_deployment_traffic_mirroring/)) / [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) ([Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: [AA](/knowledge-base/studynote/12_it_management/03_ea_isp/105_aa_as_is_analysis/) 테스트는 체중계 보정이다. 체중을 재기 전에 빈 추를 올려 "0kg이 0으로 나오는가" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것처럼, A/B 테스트 전에 동일 모델을 A/A로 테스트해서 "두 그룹에 차이가 없어야 하는데 차이가 나오지 않나" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. 체중계(테스트 인프라)가 정확해야 진짜 새 모델 효과를 측정할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>A/B 테스팅 설계 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>:
1. **가설 명확화**: "새 추천 모델은 기존 대비 CTR을 5% 향상시킨다"
2. <strong>주요 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a> 사전 결정</strong>: [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/), 전환율, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 길이 (p-hacking 방지)
3. **필요 샘플 수 계산**: 통계적 검정력 계산 (α=0.05, [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/)=0.8)
4. **최소 실험 기간**: 주간 사이클리컬리티 반영 (최소 1~2주)
5. <strong>보조 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a> <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링</strong>: 주요 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 외 에러율·레이턴시·사용자 불만 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링
6. <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/281_early_stopping/">조기 종료</a> 방지</strong>: p-값이 일찍 임계값 넘었다고 실험 중단 금지 (Peeking Problem)

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a> <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD와 연계</strong>: 새 모델 학습 -> [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) 등록 -> 자동 [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/) -> [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> 자동 [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) -> 자동 A/B 테스팅 -> 결과에 따라 자동 전체 배포/[롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 Level 2 MLOps의 표준 CD([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)) 구현이다.

- **📢 섹션 요약 비유**: Peeking Problem(조기 중단 오류)은 주식 시장 단타 매매 오류와 같다. "오늘 주가가 올랐으니(p<0.05) 내일도 오를 것"이라고 팔아버리면 실제 장기 트렌드를 놓친다. A/B 테스트도 초반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 몇 건으로 "이미 유의미하다"고 판단해 중단하면 실제로는 우연한 변동일 수 있다. 미리 정한 샘플 크기를 채워야 결론을 낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

A/B 테스팅·섀도우·[카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)는 ML 모델의 안전한 프로덕션 전환을 위한 업계 표준 방법론이다. "빠르게 배포하되 안전하게"라는 MLOps의 핵심 가치를 구현하는 기술이다. 아마존·넷플릭스·구글은 매일 수백~수천 개의 A/B 테스트를 동시 운영하며, 이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 의사결정 문화가 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 제품의 지속적 개선과 비즈니스 경쟁력의 원천이 됐다. 기술사 시험에서 ML 시스템 설계 문제에서는 이 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)들을 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인과 연계해서 설명하는 것이 고득점 포인트다.

- **📢 섹션 요약 비유**: 점진적 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 전체는 항공기 새로운 유형의 기체 투입 과정과 같다. 시뮬레이터(섀도우)로 먼저 테스트, 비상업 노선([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 1%) 먼저 투입, 일부 단거리 노선([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~50%)으로 확대, 전체 노선(100% 전환) 순서로 안전을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하며 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)한다. 한 번에 전 세계 모든 비행기를 교체하는 것은 항공 안전 당국도 허가하지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [섀도우 배포](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/) | 트래픽 복사, 응답 미전송 / 사용자 영향 없는 새 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) | 소수 트래픽, 점진적 전환 / 실제 사용자 반응 기반 안전 배포 |
| A/B 테스팅 | 통계적 유의성, [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 비교 / 비즈니스 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 기반 모델 선택 |
| [블루-그린 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/194_blue_green_deployment_strategy/) | 즉시 전환, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) / 인프라 레벨 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) |
| [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | 자동화 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 / 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 통합되는 ML 운영 체계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[문서·임베딩 준비] -> [A/B 테스팅 / 섀도우 배포 (Shadow Deployment) / 카나리 (Canary)] -> [관측성·평가·거버넌스 확장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/575_shadow_deployment_traffic_mirroring/">섀도우 배포</a></strong>는 새 요리사가 주방에서 몰래 요리를 만들어보지만 **손님에게는 기존 요리사 것을 주는** 방법으로, 손님 피해 없이 새 요리를 테스트해요!
2. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a></strong>는 10명 중 1명([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 1%)에게만 새 요리를 주고 반응을 보는 것, <strong>A/B 테스팅</strong>은 절반에게 새 요리, 절반에게 기존 요리를 주고 어느 쪽을 더 좋아하는지 <strong>통계로 비교</strong>하는 거예요.
3. "빠르고 안전하게 배포"라는 원칙으로 단계별로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하며 새 AI를 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 올리는 것이 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/">MLOps</a> 배포의 정석</strong>이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 333 / 420

<- **이전**: [332. GNN (Graph Neural Network)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/332_gnn/)
**다음**: [334. GPU VRAM 부족과 ZeRO 옵티마이저 (Zero Redundancy Optimizer)](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/334_vram_zero_optimizer/) ->

---
