+++
weight = 83
title = "83. 롤링 배포 (Rolling Update) - K8s 기본 점진적 무중단 배포"
date = "2026-04-10"
[extra]
categories = "studynote-devops"
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: [[193_rolling_update_deployment_kubernetes|롤링 배포]] (Rolling Update)는 기존 Pod를 한 번에 하나 또는 소수씩 새 [[288_version_ihl_tos_total_length|버전]]으로 교체하면서 원하는 replica 수를 유지하는 배포 [[268_strategy_pattern|전략]]이다.
- **가치**: 추가 인프라를 거의 쓰지 않고 [[585_zero_skipping|Zero]] Downtime을 달성할 수 있어, 기본 [[087_deployment_kubernetes_workload_rolling_update|Deployment]] [[268_strategy_pattern|전략]]으로 가장 널리 쓰인다.
- **판단 포인트**: 구버전과 신버전이 동시에 살아도 되는지, 즉 [[288_version_ihl_tos_total_length|버전]] 혼재 (Version Inconsistency)를 감당할 수 있는지 먼저 [[396_validation|확인]]해야 한다.

---

## Ⅰ. 개요 및 필요성

[[193_rolling_update_deployment_kubernetes|롤링 배포]]는 [[090_service_kubernetes_network_load_balancing|서비스]] 중단 없이 [[288_version_ihl_tos_total_length|버전]]을 바꾸려는 요구에서 나온다. 트래픽을 받는 상태에서 애플리케이션을 교체해야 하므로, 기존 Pod를 전부 내렸다가 새 [[288_version_ihl_tos_total_length|버전]]을 올리는 Recreate 방식은 다운타임이 생긴다. 반면 [[193_rolling_update_deployment_kubernetes|롤링 배포]]는 조금씩 교체해서 [[090_service_kubernetes_network_load_balancing|서비스]]가 살아 있는 시간을 최대화한다.

[[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]])는 이 과정을 Deployment와 ReplicaSet으로 관리한다. 사용자는 이미지 태그만 바꾸지만, 내부에서는 새 ReplicaSet이 생기고 이전 ReplicaSet이 천천히 줄어든다. 이때 전체 replica 수는 거의 일정하게 유지되므로 사용자는 배포 중단을 체감하지 않는다.

```text
┌──────────────────────────────────────────────────────────────┐
│       5개 중 1개씩 바꾸면 서비스는 살아 있고 버전만 바뀐다   │
├──────────────────────────────────────────────────────────────┤
│ v1 v1 v1 v1 v1  →  v1 v1 v2 v1 v2  →  v2 v2 v2 v2 v2        │
└──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 집의 벽돌을 다 무너뜨리지 않고, 하나씩 빼고 새 벽돌을 끼우는 공사 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[193_rolling_update_deployment_kubernetes|롤링 배포]]의 핵심 손잡이는 maxUnavailable과 maxSurge다. maxUnavailable은 배포 중 동시에 비어 있어도 되는 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수이고, maxSurge는 원하는 개수보다 초과로 더 띄울 수 있는 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수다. 전자는 안정성과, 후자는 속도와 자원 여력을 조절한다.

| 항목 | 의미 | 기본값 | 효과 |
| :--- | :--- | :--- | :--- |
| maxUnavailable | 동시에 중단 가능한 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수 | 25% | 높일수록 빠르지만 위험 증가 |
| maxSurge | 초과 [[087_process_state_transition|생성]] 가능한 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수 | 25% | 높일수록 더 안전하지만 자원 사용 증가 |
| readinessProbe | 트래픽 투입 가능 여부 [[396_validation|확인]] | - | 준비 전 Pod로 트래픽 차단 |
| [[077_kube_api_server_k8s_hub|kubectl]] rollout [[393_undo|undo]] | 이전 [[288_version_ihl_tos_total_length|버전]]으로 되돌리기 | - | [[098_rollback_strategy_pipeline_error_threshold|롤백]] 수행 |

새 Pod가 뜬다고 바로 트래픽을 받는 것은 아니다. readinessProbe를 통과해야 [[090_service_kubernetes_network_load_balancing|서비스]] 엔드포인트에 들어간다. 이 장치가 없으면 아직 준비되지 않은 Pod가 요청을 받아 장애를 만든다. 그래서 [[193_rolling_update_deployment_kubernetes|롤링 배포]]는 "교체"보다 "[[395_verification_process_review|검증]]된 교체"라는 표현이 더 맞다.

```text
┌────────────────────────────────────────────────────────────────┐
│ Deployment → 새 ReplicaSet 생성 → readiness 통과 후 교체       │
├────────────────────────────────────────────────────────────────┤
│ old ready  old ready  old ready   +   new pod 준비 중/준비됨   │
└────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심은 전체 [[090_service_kubernetes_network_load_balancing|서비스]] 용량을 유지한 채 배포를 진전시키는 것이다. 다만 네트워크나 외부 상태를 고려하지 않으면 겉으로는 무중단이지만 내부적으로는 혼선이 생길 수 있다.

- **📢 섹션 요약 비유**: 수업 중 한 명씩 교실을 나가 새 옷으로 갈아입고 돌아오는 방식이다. 나간 사람이 너무 많으면 수업이 멈추고, 새 옷 입은 학생이 준비 안 됐으면 발표가 꼬인다.

---

## Ⅲ. 비교 및 연결

[[193_rolling_update_deployment_kubernetes|롤링 배포]]는 Recreate, Blue/Green, Canary와 비교해야 의미가 선명해진다. Recreate는 단순하지만 다운타임이 있고, Blue/Green은 빠른 전환이 가능하지만 자원을 두 배로 쓴다. Canary는 일부 트래픽만 먼저 새 [[288_version_ihl_tos_total_length|버전]]으로 보내 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 줄인다.

| [[268_strategy_pattern|전략]] | 다운타임 | 자원 사용 | [[098_rollback_strategy_pipeline_error_threshold|롤백]] | [[288_version_ihl_tos_total_length|버전]] 혼재 |
| :--- | :--- | :--- | :--- | :--- |
| Recreate | 있음 | 적음 | 단순하지만 [[090_service_kubernetes_network_load_balancing|서비스]] 중단 | 없음 |
| Rolling Update | 거의 없음 | 적음 | 보통 | 있음 |
| Blue/Green | 거의 없음 | 큼(2배) | 매우 빠름 | 전환 전엔 없음 |
| [[595_canary_stack_smashing_protector|Canary]] | 거의 없음 | 중간 | 점진적 | 제한적 |

[[288_version_ihl_tos_total_length|버전]] 혼재는 [[193_rolling_update_deployment_kubernetes|롤링 배포]]의 본질적 그림자다. 배포 중에는 v1과 v2가 동시에 [[090_service_kubernetes_network_load_balancing|서비스]]하므로 [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]) 계약과 DB ([[501_database|Database]]) [[005_schema|스키마]]가 하위 호환이어야 한다. 즉, [[193_rolling_update_deployment_kubernetes|롤링 배포]]는 인프라 [[268_strategy_pattern|전략]]이면서 동시에 애플리케이션 설계 [[268_strategy_pattern|전략]]이다.

백엔드가 DB 컬럼을 삭제하거나 응답 포맷을 깨뜨리면, 아직 남아 있는 구버전 Pod가 바로 실패한다. 그래서 실제 운영에서는 expand/contract 방식, [[288_version_ihl_tos_total_length|버전]]별 [[014_api_posix|API]], [[576_feature_flag_ab_testing_rollout|feature flag]] 같은 호환 설계가 함께 가야 한다.

- **📢 섹션 요약 비유**: [[344_bus|버스]] 교대를 하듯 새 [[344_bus|버스]]와 옛 [[344_bus|버스]]가 잠깐 함께 다니는 동안, 승객 표가 둘 다 읽혀야 진짜 무중단이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[193_rolling_update_deployment_kubernetes|롤링 배포]]를 써도 되는지의 판단 기준은 단순하다. [[090_service_kubernetes_network_load_balancing|서비스]]가 stateless에 가깝고, 구버전과 신버전이 잠시 공존해도 기능이 깨지지 않으면 적합하다. 반대로 [[160_session_controlling_terminal|세션]]이 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 메모리에 박혀 있거나, DB [[005_schema|스키마]]가 파괴적으로 바뀌거나, 외부 연계가 강한 경우는 Blue/Green이나 별도 마이그레이션이 더 낫다.

[[435_checklist_based_testing|체크리스트]]는 다음과 같다.
1. v1과 v2가 동시에 떠도 [[014_api_posix|API]] 계약이 유지되는가?
2. readinessProbe가 실제 의존성(DB, 캐시, 외부 [[014_api_posix|API]])을 반영하는가?
3. maxUnavailable과 maxSurge가 현재 용량과 [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]])에 맞는가?
4. [[313_rollback|rollback]] 절차를 실제로 연습해 봤는가?

[[128_water_scrum_fall_anti_pattern|안티패턴]]은 분명하다. [[395_verification_process_review|검증]]되지 않은 상태에서 maxUnavailable을 크게 잡는 것, DB 마이그레이션과 앱 배포를 한 번에 깨는 것, 장기 [[160_session_controlling_terminal|세션]]을 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 내부에 두는 것, 그리고 문제가 생겼는데 [[098_rollback_strategy_pipeline_error_threshold|롤백]]보다 수동 핫픽스로 버티는 것이다. [[193_rolling_update_deployment_kubernetes|롤링 배포]]는 느리게 바꾸는 [[268_strategy_pattern|전략]]이지, 대충 바꾸는 [[268_strategy_pattern|전략]]이 아니다.

- **📢 섹션 요약 비유**: 한 줄씩 바꾸는 셔틀버스라 생각하면 된다. 차가 절반도 안 남았는데 새 차가 고장 나면 전체 통근이 멈춘다.

---

## Ⅴ. 기대효과 및 결론

[[193_rolling_update_deployment_kubernetes|롤링 배포]]의 가장 큰 효과는 "[[090_service_kubernetes_network_load_balancing|서비스]]를 멈추지 않고 바꿀 수 있다"는 점이다. 비용 추가가 적고, 작은 변경을 자주 넣기 좋으며, 운영자는 배포 상태를 단계적으로 관찰할 수 있다. 그러나 이 [[268_strategy_pattern|전략]]은 [[288_version_ihl_tos_total_length|버전]] 혼재를 전제로 하므로, 애플리케이션과 [[001_dikw_pyramid|데이터]] 계층의 [[344_compatibility_usability|호환성]]이 뒷받침되어야 한다.

미래의 배포는 Rolling Update 단독이 아니라 Canary와 Blue/Green이 섞인 Progressive Delivery로 간다. 그래도 기본은 같다. 배포 중에도 살아 있어야 한다면, 교체 속도와 위험을 숫자로 제어할 수 있어야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | [[193_rolling_update_deployment_kubernetes|롤링 배포]]를 소유하는 상위 리소스 |
| [[086_replicaset_kubernetes_controller_self_healing|ReplicaSet]] | 구버전과 신버전 replica를 교대 관리 |
| readinessProbe | 트래픽 투입 전 준비 상태 [[396_validation|확인]] |
| maxUnavailable | 동시에 줄일 수 있는 여유 |
| maxSurge | 추가 [[087_process_state_transition|생성]]으로 속도 조절 |
| Blue/Green | 빠른 절체형 배포 [[268_strategy_pattern|전략]] |
| [[595_canary_stack_smashing_protector|Canary]] | 일부 트래픽 [[395_verification_process_review|검증]]형 배포 [[268_strategy_pattern|전략]] |

### 📈 관련 키워드 및 발전 흐름도

```text
Recreate
    │
    ▼
Rolling Update
    │
    ├────────► Blue/Green
    │
    └────────► Canary
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[193_rolling_update_deployment_kubernetes|롤링 배포]]는 놀이터 그네를 한 번에 다 바꾸지 않고 하나씩 교체하는 거예요.
2. 그래서 다른 친구들은 계속 놀 수 있지만, 새 그네가 안전한지 먼저 [[396_validation|확인]]해야 해요.
3. 만약 옛 그네와 새 그네를 같이 써도 되면, 아무도 기다리지 않고 계속 놀 수 있답니다.
