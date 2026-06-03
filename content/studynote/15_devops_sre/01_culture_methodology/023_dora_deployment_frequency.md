+++
title = "23. DORA 배포 빈도 (DORA Deployment Frequency)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) ([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Research and Assessment) 배포 빈도([Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) Frequency)는 조직이 프로덕션 환경에 코드를 배포하는 빈도를 측정하는 핵심 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성과 지표로, 팀의 소프트웨어 전달 역량(Software Delivery Capability)과 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성숙도를 직접적으로 반영한다.
> 2. **가치**: [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 연구(2019 [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) of [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Report)는 Elite 팀이 하루 여러 번 배포(On Demand)하며, 이 팀들이 Low 팀(수개월에 1회)보다 배포 속도 208배, [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 106배, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 2604배 우수하다는 것을 수만 개 조직 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했다.
> 3. **판단 포인트**: 배포 빈도를 높이기 위한 전제 조건은 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)([마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화, [Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/), 자동화 테스트 커버리지이며, 높은 배포 빈도 달성 없이는 짧은 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)(Mean Time To [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))과 낮은 변경 실패율([Change Failure Rate](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/))도 달성하기 어렵다.

---

## Ⅰ. 개요 및 필요성

[DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 배포 빈도([Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) Frequency)는 조직이 프로덕션(또는 최종 사용자)에게 코드 변경을 성공적으로 릴리스하는 빈도를 측정하는 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 4개 핵심 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 중 첫 번째 지표다.

전통적인 폭포수(Waterfall) 방식에서는 6~12개월마다 대규모 릴리스를 하나씩 내보내며, 이로 인해 누적된 버그와 대규모 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 위험이 상시 존재한다. 배포 빈도를 높이면 변경 규모가 작아져 문제 발생 시 원인 추적이 쉬워지고, 사용자 피드백을 빠르게 반영하는 린 사이클([Lean](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/) Cycle)이 완성된다.

```text
┌────────────────────────────────────────────────────────────┐
│            DORA 4대 메트릭 상호 관계                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  속도 (Velocity)                                           │
│  ├─ 배포 빈도 (Deployment Frequency)  ← 이번 주제          │
│  └─ 변경 리드 타임 (MLT: Mean Lead Time for Changes)       │
│                                                            │
│  안정성 (Stability)                                        │
│  ├─ 변경 실패율 (CFR: Change Failure Rate)                  │
│  └─ 서비스 복구 시간 (MTTR: Mean Time To Restore)          │
│                                                            │
│  핵심 통찰: Elite 팀 = 속도 높음 + 안정성 높음 (트레이드오프 없음!)│
└────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 배포 빈도는 식당의 신메뉴 출시 속도와 같다. 6개월마다 대형 메뉴 개편(대규모 릴리스)을 하는 식당보다, 매주 작은 개선(잦은 소규모 배포)을 하는 식당이 고객 취향 변화에 훨씬 빠르게 적응한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 성숙도 4단계

| 등급 | 배포 빈도 | 대표 사례 | 특성 |
|:---|:---|:---|:---|
| **Elite** | 하루 여러 번 (On Demand) | Netflix, Amazon | 완전 자동화 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD, [Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) |
| **High** | 하루 1회 ~ 주 1회 | 성숙 스타트업 | [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 자동화 완성 |
| **Medium** | 주 1회 ~ 월 1회 | 중견 기업 | 일부 수동 배포 잔존 |
| **Low** | 월 1회 ~ 반기 1회 | 전통 SI | 수동 배포, 긴 승인 절차 |

### 고빈도 배포를 가능하게 하는 기술 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)

```text
┌──────────────────────────────────────────────────────────────┐
│         Elite 팀의 고빈도 배포 지원 아키텍처                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  코드 커밋 (Git Push)                                        │
│       │                                                      │
│       ▼                                                      │
│  CI Pipeline: 빌드 → 단위테스트 → 통합테스트 → 이미지 빌드     │
│       │  (GitHub Actions / Jenkins / CircleCI)               │
│       ▼                                                      │
│  CD Pipeline: 스테이징 배포 → E2E 테스트 → 프로덕션 배포       │
│       │  (ArgoCD / Spinnaker / Flux)                         │
│       ▼                                                      │
│  Feature Flag: 특정 사용자에게만 신기능 활성화                  │
│       │  (LaunchDarkly / Unleash)                            │
│       ▼                                                      │
│  카나리 배포: 5% 트래픽 → 점진적 확대 → 100%                   │
└──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Elite 팀의 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD는 컨베이어 벨트 공장이다. 개발자가 코드를 올리면 자동으로 테스트·검사·포장·배송이 끊임없이 이루어져 하루에도 수십 번 소비자(사용자) 손에 제품이 전달된다.

---

## Ⅲ. 비교 및 연결

| 접근 방식 | 배포 단위 | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 시간 | 배포 빈도 |
|:---|:---|:---|:---|:---|
| **빅뱅 릴리스** | 6~12개월 대규모 | 매우 높음 | 수 시간~수 일 | 연 1~2회 |
| **기능별 배포** | 기능 완성 시 | 중간 | 수 분~수 시간 | 주 1회 |
| **[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 독립 배포** | [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 단위 | 낮음 | 수 초~수 분 | 하루 수 회 |
| **[카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)/블루-그린** | 트래픽 분할 배포 | 최소 | 수 초 (즉시 전환) | On Demand |

배포 빈도는 [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) ([Value Stream Mapping](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/), 가치 흐름 지도)과 연계하여 코드 커밋에서 프로덕션까지의 전체 흐름을 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하고, 병목 지점(승인 대기, 수동 테스트)을 제거하는 개선 활동의 기준 지표가 된다.

- **📢 섹션 요약 비유**: 배포 빈도는 택배 배송 빈도와 같다. 한 달에 한 번 대형 트럭으로 모아서 보내는 것보다, 매일 소형 택배로 보내는 것이 고객에게 훨씬 빠르고 분실 위험도 낮다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 레거시 모노리스에서 고빈도 배포로 전환
국내 전자상거래 플랫폼이 월 1회 배포에서 일 수 회 배포로 전환한다.

1. **현상 진단**: [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) Frequency = 월 1회, [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) = 4시간, [CFR](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/) = 15%.
2. **병목 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)**: 수동 [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/) 3일 소요, QA팀 승인 대기 2일.
3. **자동화 도입**: [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/) 자동화(Selenium + JUnit) → 20분으로 단축.
4. **[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 분리**: 주문·결제·상품 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립 배포 단위로 분리.
5. **결과 3개월 후**: [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) Frequency = 일 5회, [CFR](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/) = 3%, [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) = 15분.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 배포 빈도 측정 기준을 프로덕션 배포 수(내부 스테이징 제외)로 명확히 정의.
- 배포 빈도 증가와 함께 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링([APM](/knowledge-base/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 알림) 강화가 반드시 병행되어야 함.
- [Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 없이 배포 빈도만 높이면 미완성 기능 노출 위험이 증가.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 배포 빈도만 높이고 자동화 테스트 커버리지를 무시하는 패턴. 테스트 없이 잦은 배포는 버그를 빠르게 프로덕션에 전달하는 버그 배달 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 된다. 배포 빈도 향상은 반드시 테스트 자동화와 함께 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)해야 한다.

- **📢 섹션 요약 비유**: 테스트 없이 배포 빈도만 높이는 건 품질 검사 없이 공장 속도만 높이는 것과 같다. 불량품이 빠르게 대량으로 소비자에게 전달되는 최악의 시나리오가 된다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **빠른 피드백** | 소규모 변경으로 문제 조기 탐지 | 버그 해결 시간 60% 단축 |
| **비즈니스 민첩성** | 시장 변화에 즉각 대응 | Time-to-Market 70% 단축 |
| **[리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)** | 소규모 배포로 장애 영향 최소화 | 장애 당 영향 범위 80% 감소 |

[DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 배포 빈도는 [플랫폼 엔지니어링](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)([Platform Engineering](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/))과 결합하여, 개발팀이 인프라 관심사 없이 코드만 올리면 자동으로 배포되는 골든 패스(Golden Path) 구현으로 진화하고 있다. 2024년 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 보고서는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 코드 어시스턴트가 배포 빈도를 추가로 1.5배 향상시킬 수 있다고 발표했다.

- **📢 섹션 요약 비유**: [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 배포 빈도는 조직의 소프트웨어 심장박동 수다. 건강한 심장(Elite 팀)은 분당 일정 박동을 유지하고, 쇠약한 심장(Low 팀)은 몇 달에 한 번 겨우 뛴다. 박동이 빠를수록 몸([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 활기차게 살아있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인** | 배포 빈도를 높이는 핵심 자동화 인프라 |
| **[Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)** | 배포와 기능 릴리스를 분리하여 안전한 고빈도 배포 실현 |
| **[카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)** | 트래픽 일부에만 신버전 적용으로 위험 최소화 |
| **변경 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) (MLT)** | 코드 커밋 → 프로덕션 배포까지의 시간; DF와 상호 강화 |
| **[MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)** | 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간; 고빈도 배포 팀은 소규모 변경으로 MTTR도 짧음 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 배포 (빅뱅 릴리스) — 수개월 주기, 고위험]
    │
    ▼
[CI 자동화 — 빌드·테스트 자동화, 주 1회 가능]
    │
    ▼
[CD + MSA — 독립 서비스 배포, 일 수 회]
    │
    ▼
[Feature Flag + 카나리 — On Demand 안전 배포]
    │
    ▼
[플랫폼 엔지니어링 + AI 코드 어시스턴트 — 배포 자동화 극한]
```
수동 대규모 배포에서 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 자동화, [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 분리, Feature Flag를 거쳐 [플랫폼 엔지니어링](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)과 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보조로 극한의 배포 빈도를 달성하는 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성숙화 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 배포 빈도는 **앱 업데이트 버튼**을 얼마나 자주 누를 수 있는지 재는 척도예요!
2. 업데이트가 많을수록 버그가 빨리 고쳐지고 새 기능이 빨리 생기는 것처럼, 개발팀이 자주 배포할수록 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 점점 더 좋아진답니다.
3. 단, 업데이트가 많아도 품질 검사(자동화 테스트)를 잘 해야 망가진 앱이 배달되지 않아요 — 속도와 품질이 함께 가야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 23 / 373

← **이전**: [22. 지속적 피드백 (Continuous Feedback)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/022_continuous_feedback_telemetry/)
**다음**: [24. Lead Time for Changes — 변경 리드 타임](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/024_lead_time_for_changes/) →

---
