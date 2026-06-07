---
title: "Traffic Shadowing"
date: "2026-04-21"
tags:
  - "studynote-devops-sre"
weight: 167
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트래픽 섀도잉 (Traffic Shadowing)은 운영 요청의 복사본을 신버전에 동시에 보내되, 사용자 응답은 기존 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)만 사용하게 해 실제 트래픽 조건에서 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 기법이다.
> 2. **가치**: 스테이징 환경이 재현하지 못하는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포, 부하 패턴, 희귀 요청을 운영과 동일한 맥락에서 관찰할 수 있어 배포 전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)를 높인다.
> 3. **판단 포인트**: 사용자 영향은 줄일 수 있지만, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청·외부 연동·[개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 노출 같은 부작용이 남아 있으므로 격리 저장소, 응답 비교, [민감정보](/studynote/09_security/16_data_privacy/782_sensitive_information/) [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹을 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

트래픽 섀도잉 (Traffic Shadowing)은 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)나 [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)가 실제 운영 요청을 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 신버전 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에도 보내는 운영 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 방식이다. 이때 사용자는 기존 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 응답만 받으므로, 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 실패하더라도 사용자 경험은 직접 흔들리지 않는다. 다시 말해 "운영과 같은 시험장"을 만들되, 결과는 아직 사용자에게 노출하지 않는 구조다.

이 기법이 필요한 이유는 스테이징 환경의 한계 때문이다. [테스트 데이터](/studynote/04_software_engineering/11_testing_validation/836_test_data_management/)는 실제 운영의 요청 폭주, 드문 예외 입력, 편향된 사용자 행동을 완전히 흉내 내기 어렵다. 그 결과 [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)를 하더라도 처음 몇 퍼센트의 실제 사용자가 사실상 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 역할을 맡게 되는데, 섀도잉은 이 위험을 앞단에서 줄여 준다.

아래 그림은 운영 요청이 어떻게 본 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 섀도우 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 나뉘는지 보여준다.

```text
+--------------------------------------------------------------+
|                 트래픽 섀도잉의 기본 발상                     |
+--------------------------------------------------------------+
| Client Request                                               |
|      |                                                       |
|      v                                                       |
| Gateway / Proxy                                              |
|   +---> Primary Service (응답 사용) ---> User                  |
|   +---> Shadow Service  (응답 폐기) ---> Metrics / Logs        |
+--------------------------------------------------------------+
```

즉, 섀도잉은 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이라기보다 <strong>운영 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>에 가깝다. 신버전의 정확도, [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 자원 사용량을 사용자 영향 없이 먼저 관찰한 뒤, 이후 [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)나 블루-그린 전환 여부를 판단하는 데 사용한다.

- **📢 섹션 요약 비유**: 트래픽 섀도잉은 신입 요리사가 손님 주문을 옆에서 똑같이 연습해 보는 것과 같다. 손님은 기존 셰프의 음식을 받지만, 주방장은 신입의 실력을 실제 주문 기준으로 미리 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

트래픽 섀도잉의 구조는 크게 네 요소로 나뉜다. 첫째, 게이트웨이 또는 [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)가 요청을 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)한다. 둘째, 프라이머리 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Primary [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 실제 응답을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다. 셋째, 섀도우 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Shadow [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 같은 요청을 처리하지만 결과를 사용자에게 반환하지 않는다. 넷째, 관측 계층이 양쪽의 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 오류, 응답 차이, 자원 사용량을 비교한다.

핵심은 "[복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 하되 부작용은 격리한다"는 점이다. 읽기 전용 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))는 비교적 안전하지만, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청·결제·메일 발송·푸시 알림처럼 외부 상태를 바꾸는 작업은 그대로 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하면 사고가 난다. 그래서 섀도우 환경에서는 테스트 전용 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) ([Database](/studynote/05_database/04_transactions_concurrency/501_database/), DB), 외부 호출 차단, [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/) 토픽 ([Dummy](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/) Topic) 전환 같은 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치를 함께 둔다.

아래 그림은 실무형 섀도잉 아키텍처를 요약한 것이다.

```text
+--------------------------------------------------------------+
|               실무형 트래픽 섀도잉 아키텍처                  |
+--------------------------------------------------------------+
| User Request                                                 |
|      |                                                       |
|      v                                                       |
| Ingress / Service Mesh                                       |
|   +---> v1 Primary ----------------> Real Database / Real Queue |
|   |        |                                                  |
|   |        +---------------> Response to User                 |
|   |                                                          |
|   +---> v2 Shadow ----------------> Shadow Database / Stub Queue|
|            |                                                  |
|            +---------------> Metrics, Logs, Diff Result       |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 게이트웨이 / [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) | 요청 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비율, 헤더 태깅, 샘플링 제어 |
| 프라이머리 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 사용자 응답 제공 | 기존 안정성 유지 |
| 섀도우 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 신버전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 부작용 격리, [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 관리 |
| 비교·관측 계층 | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)/[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)/응답 [차이 분석](/studynote/12_it_management/03_ea_isp/891_gap_analysis_task_identification/) | P95/P99, 에러율, 정합성 비교 |

실무에서는 [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), Envoy, NGINX 같은 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 계층에서 이 기능을 구현하는 경우가 많다. 다만 섀도우 응답을 버린다고 해서 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 끝나는 것은 아니다. [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)과 응답 디프 (Diff) 결과를 자동 수집해 "빠르지만 틀린 응답"을 걸러내야 진짜 의미 있는 섀도잉이 된다.

- **📢 섹션 요약 비유**: 트래픽 섀도잉은 공연 리허설용 무대와 같다. 본 무대는 관객 앞에서 실제 공연을 하고, 옆 리허설 무대는 같은 음악에 맞춰 연습하지만 조명·소품 사고가 본 공연으로 번지지 않게 분리되어 있다.

---

## Ⅲ. 비교 및 연결

트래픽 섀도잉은 [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) ([Canary Deployment](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)), [블루-그린 배포](/studynote/13_cloud_architecture/04_devops_observability/194_blue_green_deployment_strategy/) ([Blue-Green Deployment](/studynote/12_it_management/05_security_compliance/947_process/)), 리플레이 테스트 (Replay Test)와 함께 비교해야 경계가 분명해진다. [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 일부 실제 사용자가 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 응답을 받는 방식이고, 블루-그린은 환경 전체를 전환하는 방식이며, 리플레이는 저장된 과거 요청을 오프라인에서 다시 재생하는 방식이다. 반면 섀도잉은 실제 현재 요청을 사용하지만, 응답을 사용자에게 노출하지 않는다는 점이 핵심 차이다.

| 항목 | 트래픽 섀도잉 | [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) | 리플레이 테스트 |
| :--- | :--- | :--- | :--- |
| 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 현재 운영 트래픽 | 현재 운영 트래픽 | 저장된 과거 트래픽 |
| 사용자 영향 | 없음 | 일부 사용자 영향 | 없음 |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 초점 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·정합성 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 실제 사용자 반응 포함 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 재현성 높은 회귀 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 주의점 | 부작용 격리 필요 | 사용자에게 오류 노출 가능 | 현재 트래픽 패턴 반영 한계 |

또한 섀도잉은 [옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) ([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))와 강하게 연결된다. 단순히 요청을 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하는 것만으로는 충분하지 않고, 지표 ([Metrics](/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) ([Logs](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)), 트레이스 (Traces), 응답 [차이 분석](/studynote/12_it_management/03_ea_isp/891_gap_analysis_task_identification/)이 함께 돌아가야 한다. 그래서 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) ([Site Reliability 엔진ering](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/)) 관점에서는 섀도잉을 하나의 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 기능이 아니라 <strong>관측 기반 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인</strong>으로 보는 편이 더 정확하다.

즉, 이상적인 배포 순서는 보통 "섀도잉으로 내부 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)로 사용자 영향 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> 전체 전환"이다. 시험에서도 이 연결 흐름을 제시하면 단일 기법 암기보다 더 입체적인 답이 된다.

- **📢 섹션 요약 비유**: 섀도잉은 무대 뒤 리허설, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 소규모 시범 공연, 블루-그린은 공연장을 통째로 바꾸는 일과 같다. 모두 새 공연을 준비하지만 관객에게 보여 주는 시점과 범위가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 섀도잉이 특히 유효한 곳은 검색, 추천, 조회 API처럼 읽기 비중이 높고 응답 품질 비교가 중요한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다. 예를 들어 추천 엔진 새 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 배포하기 전에 하루 동안 운영 요청을 그대로 보내고, 응답 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)과 추천 결과의 분포 차이를 함께 비교하면 기능적·비기능적 품질을 동시에 점검할 수 있다. 반면 결제 승인, 재고 차감, 메일 발송처럼 외부 부작용이 큰 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 섀도잉만 믿고 도입하기 어렵다.

또한 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)와 운영 비용을 함께 봐야 한다. 섀도우 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 실제 요청 바디를 받는 만큼 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹, 토큰 익명화, 저장 금지 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 설계해야 하며, 동일 트래픽을 두 번 처리하므로 CPU·메모리·네트워크 비용도 늘어난다. 따라서 "[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가치가 비용과 위험을 넘는가"가 채택 판단의 핵심이다.

### 적용 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 섀도우 경로에서 DB [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 발행, 외부 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출이 차단 또는 격리되는가?
2. 응답 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)뿐 아니라 정합성 차이까지 비교하는 도구가 있는가?
3. [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)와 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 토큰을 섀도우 경로에서 안전하게 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 또는 제한하는가?
4. 섀도잉 종료 기준(P99, 오류율, 자원 사용량)을 사전에 정의했는가?

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청을 실제 운영 저장소에 그대로 보내 중복 반영을 일으키는 경우
- 응답을 버리기만 하고 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·디프 분석을 하지 않는 경우
- 전체 트래픽을 한 번에 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)보다 비용과 장애 위험을 먼저 키우는 경우

기술사 관점에서는 "무영향 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)"이라는 장점과 "부작용 격리"라는 전제를 함께 써야 답이 균형 잡힌다. 섀도잉은 안전한 만능 기법이 아니라, 격리 설계가 갖춰졌을 때 강력한 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기법이다.

- **📢 섹션 요약 비유**: 트래픽 섀도잉은 새 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 노선을 실제 시간표대로 시험 운행하되 승객은 태우지 않는 것과 같다. 길 병목과 연료 소모는 미리 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있지만, 사고가 나지 않게 시험 구간과 안전 규칙을 따로 둬야 한다.

---

## Ⅴ. 기대효과 및 결론

트래픽 섀도잉을 잘 설계하면 운영과 같은 조건에서 신버전의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 안정성, 결과 정합성을 먼저 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다. 스테이징에서 놓치기 쉬운 엣지 케이스를 조기에 발견하고, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 이전에 충분한 근거 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 확보할 수 있다는 점이 가장 큰 효과다. 특히 사용자 영향 없이 실제 부하를 관찰할 수 있다는 점에서 SRE의 위험 최소화 철학과 잘 맞는다.

하지만 비용과 제약도 분명하다. 부하가 두 배 가까이 늘 수 있고, 상태 변경 로직은 추가 격리가 없으면 오히려 위험해질 수 있다. 앞으로는 응답 디프 자동화, [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 결합을 통해 섀도잉이 더 지능적인 운영 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체계로 발전할 가능성이 크다.

결론적으로 트래픽 섀도잉은 "실제 트래픽으로 시험하되, 사용자에게는 아직 보여 주지 않는 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 방식"으로 기억하면 된다. 안전한 배포는 단순 전환 기술이 아니라, 충분히 관찰하고 비교한 뒤 전환하는 운영 습관에서 나온다.

- **📢 섹션 요약 비유**: 트래픽 섀도잉은 본 경기에 나가기 전 실제 경기장 조명과 소음 속에서 연습하는 예비 경기와 같다. 아직 점수판에는 반영되지 않지만, 본 경기 승률을 높이는 중요한 준비 과정이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) ([Canary Deployment](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)) | 섀도잉 이후 실제 사용자 일부에 신버전을 노출하는 다음 단계 |
| [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) ([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) | 요청 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 구현하는 대표 인프라 계층 |
| [옵저버빌리티](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) ([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 트레이스로 섀도우 결과를 해석하는 기반 |
| 디프 테스트 (Diff Test) | 프라이머리와 섀도우 응답 차이를 자동 비교하는 기법 |
| 사이드 이펙트 (Side Effect) 격리 | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 외부 호출, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 처리 위험을 통제하는 전제 조건 |

### 📈 관련 키워드 및 발전 흐름도

```text
스테이징 한계 인식
    |
    v
트래픽 미러링 · 트래픽 섀도잉 (Traffic Shadowing)
    |
    v
메트릭 · 로그 · 트레이스 기반 비교
    |
    v
디프 테스트 (Diff Test) · 자동 이상 탐지
    |
    v
카나리 배포 (Canary Deployment) · 점진적 전환
```

이 흐름도는 섀도잉이 단독 기술이 아니라, 관측 기반 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에서 점진 배포로 이어지는 배포 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 중간 단계임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 트래픽 섀도잉은 새 요리사가 손님 주문을 몰래 같이 만들어 보는 연습이에요.
2. 손님은 원래 요리사가 만든 음식만 먹지만, 주방장은 새 요리사가 얼마나 잘했는지 옆에서 비교해요.
3. 충분히 잘하면 그때 새 요리사에게도 진짜 손님 음식을 맡길 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 167 / 373

<- **이전**: [166. 분산 락 병목 관측 (Distributed Lock Observability)](/studynote/15_devops_sre/03_sre_observability/166_distributed_lock_bottleneck_observability/)
**다음**: [168. 이벤트 소싱 상태 복구 모니터링 (Event Sourcing Replay Monitoring)](/studynote/15_devops_sre/03_sre_observability/168_event_sourcing_replay_monitoring/) ->

---
