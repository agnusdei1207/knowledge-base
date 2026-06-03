---
title: 85. 카나리 배포 (Canary Release) - 1% 트래픽 점진적 무중단 배포
date: '2026-04-10'
tags:
- studynote-devops
---

## 핵심 인사이트 (3줄 요약)

> **본질**: [[115_canary_deployment_gradual_rollout|카나리 배포]]([[195_canary_release_deployment|Canary Release]])는 새 [[288_version_ihl_tos_total_length|버전]]을 작은 트래픽부터 노출해 위험을 줄이는 점진적 배포 방식이다.
> **가치**: Progressive Delivery는 배포를 한 번에 끝내지 않고, 지표와 자동화 기준으로 조금씩 넓혀 가는 운영 원칙이다.
> **판단 포인트**: [[267_weight_bias_activation|Weight]] Routing으로 비율을 조절하되, [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]])와 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 조건이 없으면 [[595_canary_stack_smashing_protector|카나리]]는 단순 [[136_variance|분산]]이 된다.

---

## Ⅰ. 개요 및 필요성

[[115_canary_deployment_gradual_rollout|카나리 배포]]는 새 [[288_version_ihl_tos_total_length|버전]]을 전체 사용자에게 바로 풀지 않고, 먼저 작은 비율의 트래픽에만 보내는 방식이다. 광산에서 새 공기 상태를 [[396_validation|확인]]하던 [[595_canary_stack_smashing_protector|카나리]]처럼, 실제 사용자의 반응과 장애 징후를 먼저 보는 데 목적이 있다.

이 방식이 필요한 이유는 배포 실패의 충격 범위를 줄이기 위해서다. 한 번에 100%를 바꾸면 문제가 생겼을 때 전 사용자에게 장애가 퍼지지만, 1%나 5%부터 시작하면 문제를 빠르게 발견하고 되돌릴 수 있다.

- 📢 섹션 요약 비유: 먼저 보내는 시험탄

---

## Ⅱ. 아키텍처 및 핵심 원리

[[595_canary_stack_smashing_protector|카나리]] 운영에는 트래픽 [[136_variance|분산]]기, 신규 [[288_version_ihl_tos_total_length|버전]], 안정 [[288_version_ihl_tos_total_length|버전]], 지표 수집, 판정 게이트가 필요하다. [[267_weight_bias_activation|Weight]] Routing은 로드밸런서(LB, [[031_load_balancer|Load Balancer]])나 [[302_service_mesh_istio|서비스 메시]]([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]])에서 비율을 조절해, 95/5, 90/10처럼 단계적으로 트래픽을 넘긴다.

```text
사용자 트래픽
   ├─ 95% ─> Stable Version
   └─  5% ─> Canary Version ─> Metrics ─> Promote / Rollback
```

| 구성 요소 | 역할 |
| --- | --- |
| [[267_weight_bias_activation|Weight]] [[339_routing_overview_best_path_selection|Routing]] | [[288_version_ihl_tos_total_length|버전]]별 트래픽 비율 제어 |
| [[567_metrics_time_series_prometheus_grafana|Metrics]] | 오류율, [[015_지연_데이터_관점|지연]], 자원 사용량 관찰 |
| Gate | [[431_ssthresh_slow_start_threshold|임계치]] 초과 시 승격/중단 판단 |
| [[313_rollback|Rollback]] | 문제 발생 시 즉시 원복 |

핵심은 "배포했다"가 아니라 "지표가 [[288_version_ihl_tos_total_length|버전]]을 승인했다"는 점이다.

- 📢 섹션 요약 비유: [[130_signal|신호]]등이 있는 도로

---

## Ⅲ. 비교 및 연결

[[115_canary_deployment_gradual_rollout|카나리 배포]]는 Blue-Green Deployment와 다르다. 블루-그린은 두 환경을 통째로 바꾸는 방식이고, [[595_canary_stack_smashing_protector|카나리]]는 일부 트래픽만 먼저 보내서 점진적으로 확대한다. Rolling Update는 노드를 조금씩 교체하는 것이고, A/B 테스트는 제품 실험이 목적이며, Feature Flag는 기능 노출 자체를 제어하는 수단이다.

| 비교 대상 | 차이점 |
| --- | --- |
| Blue-Green | 전체 전환 후 즉시 [[238_switch_operation_principles|스위치]] |
| [[083_rolling_update_deployment_zero_downtime_version_inconsistency|Rolling Update]] | 인스턴스를 순차 교체 |
| [[195_canary_release_deployment|Canary Release]] | 트래픽 비율을 점진 확대 |
| A/B Test | 사용자 반응 실험이 목적 |
| [[576_feature_flag_ab_testing_rollout|Feature Flag]] | 코드 배포와 기능 노출 분리 |

따라서 [[595_canary_stack_smashing_protector|카나리]]는 "운영 안정성"이 목적이고, A/B 테스트는 "비즈니스 반응 측정"이 목적이라는 점을 구분해야 한다.

- 📢 섹션 요약 비유: 비슷해 보이는 다른 길

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 대표성 있는 트래픽이 들어오는지, 지표가 노이즈에 묻히지 않는지, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 기준이 숫자로 정의됐는지를 먼저 본다. 예를 들어 에러율 1% 초과, p95 [[015_지연_데이터_관점|지연]] 20% 증가, 결제 성공률 하락 같은 조건을 임계값으로 잡고 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]을 걸 수 있다.

### [[435_checklist_based_testing|체크리스트]]
1. [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]]) 관점의 SLO가 정의되어 있는가?
2. [[090_configuration_item|CI]]/CD ([[019_continuous_integration|Continuous Integration]] / [[164_continuous_delivery|Continuous Delivery]]) [[123_pipe|파이프]]라인과 연결되어 있는가?
3. Sticky [[160_session_controlling_terminal|Session]] 때문에 트래픽 샘플이 왜곡되지 않는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 지표 없이 비율만 바꾸는 [[595_canary_stack_smashing_protector|카나리]]
- 배포와 [[009_config|설정]] 변경을 동시에 크게 바꾸는 것
- [[098_rollback_strategy_pipeline_error_threshold|롤백]] 테스트 없이 승격만 자동화하는 것

- 📢 섹션 요약 비유: 안전한 시험 운행

---

## Ⅴ. 기대효과 및 결론

[[115_canary_deployment_gradual_rollout|카나리 배포]]와 Progressive Delivery의 장점은 블라스트 반경(Blast [[541_radius_remote_authentication_aaa|Radius]])을 줄이고, 실제 사용자 환경에서 빨리 학습한다는 점이다. 대신 관측 지표와 자동화 수준이 낮으면 오히려 복잡도만 늘어난다. 그래서 좋은 [[595_canary_stack_smashing_protector|카나리]]는 트래픽 [[136_variance|분산]] 기술이 아니라 관측과 의사결정의 기술이다.

결론적으로 [[267_weight_bias_activation|Weight]] Routing은 배포의 마지막 단계가 아니라 안정성을 설계하는 핵심 수단이다. 작은 비율로 시작해 지표로 증명하고, 증명되면 넓힌다는 원칙을 기억해야 한다.

- 📢 섹션 요약 비유: 조심스런 첫 발

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [[195_canary_release_deployment|Canary Release]] | 소량 트래픽으로 [[395_verification_process_review|검증]] |
| Progressive Delivery | 단계적 확장 원칙 |
| [[267_weight_bias_activation|Weight]] [[339_routing_overview_best_path_selection|Routing]] | 트래픽 비율 제어 |
| [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]) | 승격/중단 기준 |
| [[090_configuration_item|CI]]/CD | 배포 자동화 경로 |
| [[576_feature_flag_ab_testing_rollout|Feature Flag]] | 노출 제어와 실험 분리 |

### 📈 관련 키워드 및 발전 흐름도

```text
코드 머지
   ↓
배포 파이프라인
   ↓
소량 트래픽 분기
   ↓
지표 관찰 / 임계치 비교
   ↓
승격 또는 롤백
   ↓
비율 확대
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[115_canary_deployment_gradual_rollout|카나리 배포]]는 새 음식이 맛있는지 한 숟갈만 먼저 먹어 보는 것과 같아요.
2. 이상하면 바로 그만두고, 괜찮으면 조금씩 더 먹어 봐요.
3. 그래서 큰 탈 없이 새 메뉴를 낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 373

← **이전**: [[084_blue_green_deployment_zero_downtime_fast_rollback|84. 블루/그린 배포 (Blue/Green) - 무중단 광속 라우팅 스위칭 전략]]
**다음**: [[086_gitops_declarative_infrastructure_continuous_synchronization_argocd|86. GitOps (깃옵스) - 선언적 인프라 자동화 및 지속적 동기화]] →

---
