+++
title = "164. 지속적 제공 (Continuous Delivery)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
- 코드 변경 사항이 빌드 및 테스트를 거쳐 운영 환경에 배포 가능한 상태(Ready to Deploy)로 자동화되는 프로세스임.
- 최종 운영 환경으로의 배포 버튼은 사람이 직접 누르는 '수동 승인' 단계를 포함하여 안정성을 확보함.
- "배포는 지루하고 일상적인 일이 되어야 한다"는 철학으로 릴리스 사이클을 단축하고 리스크를 최소화함.

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
과거의 대규모 릴리스 방식은 배포 주기가 길고 리스크가 매우 컸다. **지속적 제공(Continuous Delivery, CD)**은 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)([지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)) 단계를 거친 코드가 항상 운영 환경에 투입될 준비가 되어 있도록 자동화하는 기술적 관행이다. 이를 통해 개발 팀은 언제든지 원하는 시점에 고품질의 기능을 사용자에게 전달할 수 있는 '릴리스 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)'을 확보하게 된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
Continuous Delivery는 파이프라인([Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/))을 통해 흐르며, 각 단계마다 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(Quality Gate)을 거친다.

```text
[ CI: Continuous Integration ]   [ CD: Continuous Delivery ]
          |                               |
[ Commit ] -> [ Build ] -> [ Test ] -> [ Staging ] -> [ Production ]
                                          |             ^
                                          |   (Manual)  |
                                          +-------------+
                                            Release Ready
```

1. **Build & [Unit Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)**: 소스 코드를 컴파일하고 기본 기능 단위의 무결성을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
2. **Automated Testing**: [통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 테스트, [성능 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/445_performance_test_types/) 등을 자동 수행하여 릴리스 안정성을 확인한다.
3. **Staging (QA) [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)**: 운영 환경과 유사한 스테이징 환경에 자동으로 배포하여 최종 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 수행한다.
4. **Manual Trigger**: 비즈니스 결정이나 최종 승인 절차에 따라 운영 환경으로의 배포를 실행한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/) ([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)) | 지속적 제공 (CD) | [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) (CD) |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | 코드 품질 및 충돌 방지 | 언제든 배포 가능한 상태 유지 | 운영 환경으로의 자동 반영 |
| **자동화 범위** | 빌드, [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) | 스테이징 배포 및 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)까지 | 운영 배포까지 100% 자동화 |
| **최종 배포** | N/A | 수동 (인간의 승인) | 자동 (기계적 반영) |
| **비즈니스 가치** | 개발 생산성 향상 | 릴리스 속도 및 안정성 확보 | 타임 투 마켓(TTM) 극대화 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **적용 시점**: [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)를 지향하거나, 금융/의료 등 규제 준수를 위해 최종 배포 전 인간의 검토가 필요한 도메인에서 표준으로 적용한다.
- **기술사적 판단**: 지속적 제공의 핵심은 **"배포 파이프라인의 가시성(Visibility)"**과 **"[멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/))"**이다. 배포 과정에서 발생하는 모든 에러는 파이프라인에서 즉시 시각화되어야 하며, 동일한 스크립트로 여러 번 배포해도 같은 결과가 보장되어야 한다. 이는 블루/그린 배포나 [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) 전략과 결합하여 운영 리스크를 비약적으로 낮춘다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
지속적 제공을 실천함으로써 조직은 '배포의 공포'에서 벗어나 비즈니스 민첩성을 극대화할 수 있다. 이는 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 메트릭스의 핵심 지표인 '배포 빈도([Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) Frequency)'와 '변경 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)([Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) for Changes)'을 개선하는 결정적 요인이다. 향후 AI옵스([AIOps](/knowledge-base/studynote/12_it_management/02_itsm_itil/099_aiops_chatbot_itsm_automation/))와 결합하여 배포 후 지표를 자동 모니터링하고 문제가 있을 시 자동 롤백하는 지능형 CD 파이프라인으로 진화할 것이다.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/))**: CD의 전제 조건.
- **[Blue-Green Deployment](/knowledge-base/studynote/12_it_management/05_security_compliance/304_process/)**: CD 파이프라인에서 주로 쓰이는 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) 기법.
- **Quality Gate**: 다음 단계로 넘어가기 위한 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기준.

### 👶 어린이를 위한 3줄 비유 설명
- 장난감 공장에서 로봇들이 장난감을 조립하고 포장까지 다 끝낸 상태예요. (CD)

### 📈 관련 키워드 및 발전 흐름도

```text
CI: 자동 빌드 + 테스트
    │
    ▼
CD (Continuous Delivery): 스테이징 자동 배포 + 수동 승인
    │
    ▼
CD (Continuous Deployment): 운영 배포까지 100% 자동화
    │
    ▼
GitOps · Progressive Delivery (Canary · Blue-Green)
```
- "이제 가게로 보내도 좋아요!"라고 공장장님이 사인을 보내기만 기다리는 거죠.
- 언제든 사인만 나면 바로 트럭에 실어서 출발할 수 있게 준비를 다 마친 상태랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 163 / 371

← **이전**: [지속적 통합 (CI, Continuous Integration)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/163_continuous_integration_ci_automated_build_test/)
**다음**: [165. 지속적 배포 (Continuous Deployment)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/) →

---
