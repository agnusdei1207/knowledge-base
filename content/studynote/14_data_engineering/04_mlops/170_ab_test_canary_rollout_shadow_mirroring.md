---
title: "170. Ab Test Canary Rollout Shadow Mirroring"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: A/B 테스트, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃 ([Canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) Rollout), 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) (Shadow Mirroring)은 새 모델이나 새 서빙 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 실제 운영 트래픽으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하되, 노출 방식만 다르게 설계한 점진 배포 패턴이다.
> 2. **가치**: 이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)들은 온라인 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 시스템 안정성, 비즈니스 지표를 실제 사용자 환경에서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면서도 한 번의 잘못된 배포가 전체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 미치는 충격을 줄인다.
> 3. **판단 포인트**: 고위험 변화는 섀도우로 먼저 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고, 일반 배포는 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)를 기본으로 삼으며, "어느 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 더 좋은가"를 통계적으로 증명해야 할 때만 A/B 테스트를 선택하는 것이 실무적으로 가장 합리적이다.

---

## Ⅰ. 개요 및 필요성

서빙 아키텍처에서 새 모델이나 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 한 번에 100% 전환하는 것은 가장 단순하지만 가장 위험한 배포 방식이다. 추천, 검색, [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), 광고 랭킹처럼 온라인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 민감한 시스템은 오프라인 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 점수가 높아도 실제 사용자 분포에서는 다른 결과를 낼 수 있다. 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 운영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 차이, 지연된 레이블, 누락된 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/), 예상 밖의 지연시간 증가는 모두 "배포 후에야 드러나는 문제"다.

따라서 현대 MLOps에서 중요한 질문은 "새 모델이 더 똑똑한가?"보다 먼저 "새 모델을 얼마나 안전하게 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 것인가?"다. 이 질문에 답하는 대표 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 A/B 테스트, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃, 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)이다. 셋 모두 실서비스 트래픽을 활용하지만, 사용자에게 실제 응답을 돌려주는지, 몇 퍼센트만 노출할지, 응답을 버릴지에서 차이가 난다.

```text
+--------------------------------------------------------------+
|            같은 새 모델이라도 노출 방식이 리스크를 바꾼다     |
+--------------------------------------------------------------+
| 일괄 전환:   v1 0%  -------------->  v2 100%                  |
|             문제 발생 시 전체 사용자가 즉시 영향             |
|                                                              |
| 점진 검증:  Shadow -> Canary 5% -> 25% -> 100% 또는 A/B 50:50  |
|             문제를 작은 범위에서 먼저 발견                   |
+--------------------------------------------------------------+
```

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 사용자 응답 | 핵심 질문 | 대표 장점 | 대표 비용 |
| :--- | :--- | :--- | :--- | :--- |
| A/B 테스트 | 두 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 모두 실제 응답 | 어느 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 더 나은가 | 통계적 비교 가능 | 실험 기간 운영 복잡도 |
| [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃 | 일부 사용자만 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 응답 | 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 안전한가 | 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)에 유리 | 승격 단계 설계 필요 |
| 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) | 기존 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)만 응답 | 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 실트래픽을 견디는가 | 사용자 영향 최소 | 추가 인프라 비용 |

이 세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 서로 배타적인 선택지가 아니라, 위험도에 따라 순서대로 조합할 수 있는 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 도구다. 새로운 모델 구조나 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이면 섀도우부터 시작하고, 이미 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 개선판이면 곧바로 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)로 들어가는 식이다.

- **📢 섹션 요약 비유**: 세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 신제품 출시 방식과 같다. A/B 테스트는 두 상품을 동시에 팔아 비교하는 것이고, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 소규모 매장에서 먼저 시험 판매하는 것이며, 섀도우는 실제 손님 흐름을 보되 판매는 하지 않는 리허설 매장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 중심에는 <strong><a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 라우터</strong>가 있다. 이 라우터는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이, [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), Inference Gateway, [피처 플래그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 시스템 안에서 동작하며, 어떤 요청을 어느 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 보낼지 결정한다. 단순히 트래픽을 나누는 것이 아니라 사용자 고정 할당, [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집, 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 사이드 이펙트 차단까지 함께 책임져야 한다.

```text
+--------------------------------------------------------------------+
|              Validation Router: 검증 방식별 라우팅 엔진           |
+--------------------------------------------------------------------+
| Client Request                                                    |
|      |                                                            |
|      v                                                            |
| Policy Engine (user hash / feature flag / experiment rule)        |
|      |                                                            |
|      +- A/B Mode                                                  |
|      |    +- control  ---> baseline model ---> 실제 응답            |
|      |    +- treatment --> candidate model --> 실제 응답            |
|      |                                                            |
|      +- Canary Mode                                               |
|      |    +- 95% baseline                                         |
|      |    +- 5% candidate ---> 실제 응답, guardrail 통과 시 확대   |
|      |                                                            |
|      +- Shadow Mode                                               |
|           +- baseline ---> 실제 응답                               |
|           +- candidate <--- 요청 복제, 응답은 폐기                 |
|                                                                    |
| Telemetry: latency · error rate · output diff · business KPI      |
+--------------------------------------------------------------------+
```

이 라우터가 제대로 동작하려면 세 가지 원리가 필수다. 첫째, <strong>고정 할당(Sticky <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">Routing</a>)</strong>이다. 같은 사용자가 요청할 때마다 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 바뀌면 실험 오염이 생기므로 사용자 ID나 [세션 키](/studynote/09_security/03_network_security/140_session_key/) 해시로 일관되게 배정해야 한다. 둘째, <strong>사이드 이펙트 격리</strong>다. 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)에서 결제, 포인트 적립, 이메일 발송 같은 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청이 후보 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에서 실제로 실행되면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 이중 반영될 수 있다. 셋째, <strong>다층 <a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a> 수집</strong>이다. 시스템 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)만 보면 모델 품질 저하를 놓치고, 비즈니스 지표만 보면 지연시간 폭증을 놓친다.

| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 계층 | 대표 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 왜 필요한가 |
| :--- | :--- | :--- |
| 시스템 계층 | 오류율, P95/P99 지연시간, CPU·메모리 사용량 | 서빙 안정성 붕괴를 즉시 감지 |
| 모델 계층 | 예측 분포 변화, 출력 차이, 실시간 정답 도착 후 정확도 | 모델 이상 동작 여부 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 비즈니스 계층 | [CTR](/studynote/09_security/02_crypto/090_ctr_mode/) (Click-Through Rate), CVR (Conversion Rate), 이탈률 | 실제 가치 상승 여부 판단 |
| 운영 계층 | [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 횟수, 승격 시간, 알람 빈도 | 배포 체계의 성숙도 측정 |

A/B 테스트는 통계 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 강점이지만, 목적이 "우승자 선발"인지 "안전성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"인지 분명해야 한다. [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 단계적 승격이 강점이지만, 자동 중단 임계값이 없다면 사실상 수동 블루-그린 배포와 다르지 않다. 섀도우는 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)가 가장 낮지만 사용자 반응을 직접 관찰하지 못하므로, 예측 결과만 좋아 보여도 실제 비즈니스 성과까지 보장하진 못한다.

- **📢 섹션 요약 비유**: [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 라우터는 공항 관제탑과 같다. 어떤 비행기를 어느 활주로로 보낼지 정하는 것뿐 아니라, 날씨·연료·충돌 위험을 모두 함께 보며 이륙 여부를 결정한다.

---

## Ⅲ. 비교 및 연결

세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 비슷해 보여도 답하려는 질문이 다르다. 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 "새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 실트래픽을 견딜 수 있는가?"를 묻고, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 "작게 노출했을 때 안전한가?"를 묻고, A/B 테스트는 "둘 중 무엇이 더 우수한가?"를 묻는다. 질문이 다르므로 성공 기준도 달라져야 한다.

| 비교 축 | A/B 테스트 | [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃 | 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) |
| :--- | :--- | :--- | :--- |
| 사용자 노출 | 두 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 모두 실제 노출 | 소수만 후보 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 노출 | 후보 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)은 비노출 |
| 주된 목적 | 승자 결정, 통계 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 안전한 점진 승격 | [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 최소 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 의미 | 실험 중지 후 기존안 유지 | 즉시 트래픽 0% 복귀 | 실제 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 개념보다 분석 중단 |
| 필요한 트래픽 | 충분히 많아야 유의성 확보 | 중간 수준도 가능 | 시스템 부하만 감당되면 가능 |
| 인프라 비용 | 중간 | 낮음~중간 | 높음 |
| 적합한 변화 | 추천 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·랭킹 개선 | 일반 모델 업데이트 | 새 아키텍처·새 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) |

실무에서는 셋을 순차적으로 조합하는 경우가 많다. 예를 들어 완전히 새로운 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 스토어나 추론 엔진을 도입할 때는 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)으로 응답 분포와 자원 사용량을 먼저 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. 그다음 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)로 1%~5% 사용자에게만 노출해 안정성을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고, 마지막으로 비즈니스 향상폭을 공식적으로 증명해야 할 때 A/B 테스트를 연다.

```text
오프라인 평가 통과
      |
      +- 변화 위험 높음 ---> Shadow Mirroring
      |                         |
      |                         v
      |                    Canary Rollout
      |                         |
      |                         v
      +- 변화 위험 보통 ------------------> A/B Test 또는 Full Promotion
```

이 흐름은 KServe, Argo Rollouts, [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), Envoy 같은 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 도구와 잘 맞는다. [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)가 트래픽 제어를 맡고, 모델 서빙 계층이 응답과 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 기록하며, 분석 시스템이 자동 승격 또는 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)을 결정하는 구조가 일반적이다. 즉, 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 모델 자체의 문제가 아니라 <strong><a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a>·관측성·통계 검정이 결합된 운영 설계</strong>다.

- **📢 섹션 요약 비유**: 섀도우는 리허설, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 프리뷰 공연, A/B 테스트는 두 연출 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 번갈아 올려 관객 반응을 비교하는 상영회와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 많이 쓰는 기본 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃이다. 사용자 일부만 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 경험하게 하면서도, 실제 트래픽의 피드백을 받을 수 있기 때문이다. 그러나 "무조건 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)"는 위험하다. 완전히 새로운 모델 구조, [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 로직, 추론 런타임 변경처럼 불확실성이 큰 경우에는 먼저 섀도우로 자원 사용량과 출력 품질을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 편이 안전하다. 반대로 [CTR](/studynote/09_security/02_crypto/090_ctr_mode/), CVR 같은 비즈니스 지표에서 우위를 입증해야 하는 광고·추천 시스템은 결국 A/B 테스트가 필요하다.

| 상황 | 우선 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 이유 | 주의점 |
| :--- | :--- | :--- | :--- |
| 새 모델 아키텍처 첫 배포 | 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) | 사용자 영향 없이 실트래픽 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청 차단, 비용 증가 |
| 기존 모델의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선판 | [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃 | 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)과 단계 승격에 적합 | 임계값과 단계 정의 필요 |
| 수익·전환율 우승자 선정 | A/B 테스트 | 통계적 근거 확보 가능 | 샘플 크기와 기간 확보 필요 |
| 장애 후 긴급 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) | [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 또는 블루-그린 | 빠른 안전 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 관찰 창을 너무 짧게 잡지 말 것 |

운영 가드레일은 보통 다음처럼 계층별로 둔다.

1. **시스템 가드레일**: 후보 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 5xx 오류율이 기준 대비 1%p 이상 증가하거나, P99 지연시간이 20% 이상 늘면 즉시 중단
2. **모델 가드레일**: 예측 분포가 급격히 치우치거나 null feature 비율이 상승하면 승격 보류
3. **비즈니스 가드레일**: [CTR](/studynote/09_security/02_crypto/090_ctr_mode/), CVR, 구매율이 허용 범위보다 하락하면 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 비중을 0%로 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)
4. **통계 가드레일**: A/B 실험은 최소 효과 크기와 종료 규칙을 미리 정하고, 중간 결과를 보고 성급히 종료하지 않음

특히 섀도우 [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)에서는 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) 설계가 중요하다. 결제·주문·알림처럼 부작용이 있는 요청은 후보 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 write path를 끄거나, 별도 sandbox 저장소로 보내야 한다. 그렇지 않으면 "사용자에게는 숨겨진 요청"이 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 오염시키는 치명적 사고로 이어진다.

피해야 할 안티패턴도 명확하다. 고정 할당 없이 사용자를 두 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에 번갈아 보내는 A/B 테스트, 자동 중단 조건이 없는 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/), [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 없는 섀도우, 표본 수가 부족한 실험은 모두 잘못된 결론을 만든다. 시험 답안에서는 <strong><a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 선택 -> <a href="/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a> 설계 -> 자동 <a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> -> 사후 승격 조건</strong> 순서로 설명하면 구조가 명확해진다.

- **📢 섹션 요약 비유**: 점진 배포 운영은 수영장에 바로 뛰어드는 것이 아니라, 먼저 발을 담그고 수온을 본 뒤 천천히 들어가는 방식과 같다.

---

## Ⅴ. 기대효과 및 결론

이 세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 제대로 적용하면 배포는 "운에 맡긴 전환"이 아니라 "증거를 수집하며 확대하는 실험"이 된다. 장애 전파 범위를 줄이고, 온라인 품질을 실제 사용자 기준으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하며, 모델 개선이 비즈니스 성과로 이어졌는지 설명할 수 있게 된다. 특히 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 조직에서는 이 설명 가능성이 매우 중요하다. 같은 정확도 상승이라도 수익이나 전환율로 연결되지 않으면 승격 근거가 약하기 때문이다.

한계도 분명하다. 섀도우는 인프라를 이중으로 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉽고, A/B 테스트는 시간과 트래픽이 많이 필요하며, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 품질이 아주 미세하게 나빠지는 경우를 통계적으로 잡기 어렵다. 또한 레이블이 늦게 도착하는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 즉시 관찰 가능한 시스템 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)과 나중에 들어오는 정답 기반 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 분리해 설계해야 한다.

결국 세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 서로의 대체재가 아니라 서로 다른 질문에 답하는 도구다. <strong>섀도우는 "버틸 수 있는가", <a href="/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a>는 "안전한가", A/B 테스트는 "더 좋은가"를 묻는다</strong>고 기억하면 판단이 쉬워진다.

- **📢 섹션 요약 비유**: 이 세 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 시험 공부와 같다. 모의고사만 보는 단계, 일부 문제만 실전처럼 풀어 보는 단계, 두 공부법을 비교해 더 좋은 쪽을 고르는 단계가 각각 다르다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 고정 할당 (Sticky [Routing](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)) | 같은 사용자를 동일 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에 유지해 실험 오염을 방지 |
| 가드레일 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) (Guardrail [Metric](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)) | 오류율·지연시간·비즈니스 하락을 자동 차단하는 기준 |
| [피처 플래그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) ([Feature Flag](/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)) | 실험군 노출 범위와 대상 집합을 세밀하게 제어 |
| [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) ([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) | [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [미러링](/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/), [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 조절을 인프라 계층에서 수행 |
| 온라인 평가 (Online Evaluation) | 오프라인 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 넘어 실제 사용자 반응을 측정 |
| [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 섀도우 요청의 부작용을 차단하는 핵심 설계 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
오프라인 모델 평가
    |
    v
섀도우 미러링 (실트래픽 무영향 검증)
    |
    v
카나리 롤아웃 (소수 사용자 노출)
    |
    +- 안전성 검증 완료 ---> 전체 승격
    +- 효과 비교 필요 -----> A/B 테스트
                               |
                               v
                        통계 검증 기반 우승자 선택
```

이 흐름은 모델 배포가 "학습 완료 -> 즉시 전환"이 아니라, 위험도와 목적에 따라 여러 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 관문을 거치는 운영 과정임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 새 장난감을 바로 모두에게 주지 않고, 먼저 몰래 시험해 보거나 몇 명에게만 먼저 써 보게 하는 거예요.
2. 그렇게 하면 장난감이 금방 고장 나는지, 친구들이 더 좋아하는지 안전하게 알 수 있어요.
3. 그래서 모두에게 주기 전에 가장 좋은 방법을 골라서 실수할 확률을 줄일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 170 / 258

<- **이전**: [169. 모델 서빙 엔진 (Model Serving 엔진) - TensorFlow Serving, NVIDIA Triton](/studynote/14_data_engineering/04_mlops/169_model_serving_engine_triton_tensorflow_serving/)
**다음**: [171. 설명 가능한 AI (XAI)](/studynote/14_data_engineering/04_mlops/171_xai_lime_shap_explainable_ai/) ->

---
