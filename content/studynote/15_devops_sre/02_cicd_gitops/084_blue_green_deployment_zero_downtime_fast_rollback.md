+++
title = "84. 블루/그린 배포 (Blue/Green) - 무중단 광속 라우팅 스위칭 전략"
date = 2026-04-10

[taxonomies]
tags = ["studynote-devops"]

[extra]
tags = ["studynote-devops"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 블루/그린 배포 (Blue/Green [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))는 동일한 두 환경을 두고 트래픽 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)만 바꿔 무중단 전환을 만드는 방식이다.
> 2. **가치**: 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 먼저 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한 뒤 전환하므로 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 빠르고, 사용자 입장에서는 배포 순간을 거의 느끼지 못한다.
> 3. **판단 포인트**: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 자체보다 중요한 것은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이다. 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 같이 돌아갈 수 있어야 진짜 안전하다.

---

## Ⅰ. 개요 및 필요성

블루/그린 배포 (Blue/Green [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))는 동일한 두 환경을 준비해 두고, 트래픽을 한쪽에서 다른 쪽으로 바꾸는 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 블루가 현재 운영 환경이라면 그린은 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 올려 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 환경이 된다. 전환이 끝나면 그린이 운영이 되고, 문제가 생기면 즉시 블루로 되돌릴 수 있다.

[무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)가 필요한 이유는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 계속 열려 있는 시대에는 잠깐의 점검도 장애로 보이기 때문이다. 특히 결제, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 실시간 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 배포 중단 시간이 곧 사용자 불만과 매출 손실로 이어진다.

```text
Users --> LB (Load Balancer) --> Blue (live)
                              +--> Green (staged)

switch: Blue -> Green
rollback: Green -> Blue
```

- **📢 섹션 요약 비유**: 같은 교실 두 개를 미리 준비해 두고, 수업 중에 학생만 조용히 옮기는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

블루/그린의 핵심은 두 환경이 가능한 한 동일해야 한다는 점이다. 애플리케이션, 의존성, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 네트워크 경로가 같아야 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 후 예상치 못한 차이가 적다. LB ([Load Balancer](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/))는 외부에서 들어오는 요청을 어느 색으로 보낼지 결정하는 단순하지만 중요한 관문이다.

| 구성요소 | 역할 | 주의점 |
| :--- | :--- | :--- |
| Blue | 현재 운영 중인 환경 | 안전한 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 기준 |
| Green | 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 환경 | 운영과 동일해야 함 |
| LB ([Load Balancer](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/)) | 트래픽 전환 지점 | 전환 타이밍 관리 |
| Health check | 정상 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 실제 사용자 흐름도 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| DB / [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) store | 상태 저장소 | [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 핵심 |

```text
1) Green에 새 버전 배포
2) 헬스 체크 / 스모크 테스트
3) LB 트래픽 스위치
4) 장애 시 Blue로 즉시 복귀
```

이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 장점은 배포와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 거의 같은 동작이라는 점이다. 반면 두 환경을 동시에 유지해야 하므로 인프라 비용이 들고, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)나 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 형식이 양쪽 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 함께 동작해야 한다.

- **📢 섹션 요약 비유**: 두 개의 다리를 다 놓아 둔 뒤, 사람들을 한쪽 다리로만 보내는 식이다.

---

## Ⅲ. 비교 및 연결

블루/그린은 [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/)와 [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)와 자주 비교된다. 롤링은 인스턴스를 조금씩 바꾸기 때문에 자원 효율이 좋고, [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 일부 트래픽만 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)에 보내며, 블루/그린은 전체 전환과 빠른 복귀에 강하다. 즉 '안전하게 빠르게 바꾸는가'가 블루/그린의 핵심이다.

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 다운타임 | [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도 | 자원 비용 | 트래픽 노출 |
| :--- | :--- | :--- | :--- | :--- |
| Blue/Green | 거의 없음 | 매우 빠름 | 높음 | 한 번에 전체 |
| Rolling | 낮음 | 중간 | 낮음 | 점진적 |
| [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | 낮음 | 중간 | 중간 | 일부 사용자만 |

블루/그린은 트래픽 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 단순하지만, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이 복잡할수록 오히려 위험해질 수 있다. 그래서 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 애플리케이션 코드만이 아니라 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 캐시, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐, 배치 작업까지 함께 봐야 한다.

- **📢 섹션 요약 비유**: 새 집으로 이사할 때 짐만 옮기는 게 아니라, 수도와 전기도 먼저 연결돼 있어야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 블루/그린을 모든 시스템에 무조건 쓰지 않는다. [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 외부 저장소에 두거나, DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 하위 호환 가능하게 만들 수 있을 때 특히 잘 맞는다. 반대로 긴 배치 작업, 강한 상태 의존, [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 없는 DB 변경이 많으면 추가 설계가 필요하다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Green 환경에서 스모크 테스트를 완료했는가?
2. [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)과 캐시가 양쪽 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 호환되는가?
3. DB 마이그레이션이 역호환성을 유지하는가?
4. 전환 후 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링과 즉시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 절차가 준비됐는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 트래픽만 바꾸고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)은 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하지 않는 경우
- 배치 / [cron](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/) / [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 소비자 같은 백그라운드 작업을 잊는 경우
- [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)은 가능하지만 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)는 되돌릴 수 없는 경우

- **📢 섹션 요약 비유**: 새 운동장을 먼저 시험해 보고, 문제가 없을 때만 아이들을 옮기는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

블루/그린 배포의 효과는 무중단, 빠른 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 빠른 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이다. 대신 두 환경을 유지하는 비용과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 관리 부담이 있다. 따라서 이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 '자원으로 안전을 사는 방식'이라고 볼 수 있다.

결론적으로 블루/그린은 단순한 배포 기술이 아니라, 전환 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 트래픽 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 설계로 흡수하는 운영 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 준비된 복귀 경로가 있을 때만 진짜 무중단이 된다.

- **📢 섹션 요약 비유**: 비상구가 있는 극장이 가장 안심되는 극장이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Blue | 현재 운영 환경 |
| Green | 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 환경 |
| LB ([Load Balancer](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/)) | 트래픽 전환 지점 |
| Health check | 전환 전 정상 여부 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) migration | 무중단의 가장 큰 제약 |
| [Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/) | 블루/그린의 핵심 가치 |

### 📈 관련 키워드 및 발전 흐름도

```text
Green 환경 준비
  |
  v
배포 / 스모크 테스트
  |
  v
LB 트래픽 스위치
  |
  v
모니터링 -> 필요 시 즉시 롤백
```

흐름의 핵심은 '새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 문제 없음을 먼저 증명한 뒤' 전환하는 것이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 같은 놀이터를 두 개 준비해 두면 옮기기가 쉬워요.
2. 먼저 새 놀이터를 살펴보고 괜찮을 때만 이동해요.
3. 문제가 생기면 다시 원래 놀이터로 바로 돌아갈 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 84 / 373

<- **이전**: [83. 롤링 배포 (Rolling Update) - K8s 기본 점진적 무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/)
**다음**: [85. 카나리 배포 (Canary Release) - 1% 트래픽 점진적 무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/085_canary_release_progressive_delivery_weight_routing/) ->

---
