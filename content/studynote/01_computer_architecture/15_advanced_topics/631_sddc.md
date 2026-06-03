+++
title = "631. SDDC (Software Defined Data Center)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 소프트웨어 정의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터 ([Software-Defined Data Center](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/023_sddc_software_defined_data_center/), SDDC)는 서버, 스토리지, 네트워크를 각각 장비로 다루지 않고, 소프트웨어가 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)·[풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 제어하는 하나의 자원 집합으로 다루는 운영 모델이다.
> 2. **가치**: 인프라를 코드와 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 다루면 배포 시간은 짧아지고, 동일한 보안·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 규칙을 대규모로 일관되게 적용할 수 있어 프라이빗 클라우드와 하이브리드 클라우드의 기반이 된다.
> 3. **판단 포인트**: SDDC는 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 제품을 많이 쌓아 올린 상태가 아니라, [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) ([Orchestration](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)), 관측성 ([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)), 거버넌스가 함께 작동해야 완성되므로 조직과 운영 절차까지 바뀌어야 진짜 효과가 난다.

---

## Ⅰ. 개요 및 필요성

### 1.1 SDDC의 정의
SDDC는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 핵심 자원을 하드웨어별 박스로 관리하지 않고, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 자동화 소프트웨어로 통합 운영하는 개념이다. 물리 장비는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공하는 기반이 되고, 실제 배치·보안·확장은 상위 소프트웨어가 결정한다. 즉 "어떤 상자를 샀는가"보다 "어떤 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 자원을 배치하는가"가 중심이 된다.

### 1.2 왜 전통 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)는 느렸는가
기존 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)에서는 새 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 열기 위해 서버팀, 스토리지팀, 네트워크팀이 순차적으로 작업했다. 이 방식은 전문성은 높지만, 승인과 설정이 계층마다 끊겨 전체 리드타임이 길어진다. 또한 사람이 여러 콘솔을 오가며 작업하는 구조라 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 보안 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 흔들리기 쉽다.

### 1.3 왜 지금 SDDC가 필요한가
클라우드 환경에 익숙한 개발 조직은 인프라가 몇 주가 아니라 몇 분 안에 준비되길 기대한다. SDDC는 이러한 요구를 충족하기 위해 셀프서비스 포털, 응용 프로그램 프로그래밍 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 자동화, [마이크로 세그멘테이션](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) ([Micro-segmentation](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/)) 같은 개념을 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)까지 끌어온다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Manual DC -&gt; Policy Driven DC</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Old : Server Team -&gt; Storage Team -&gt; Network Team</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">New : Policy / API -&gt; Automated Provisioning</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Goal: Same request, same result, faster delivery</div></div>
</div>
</div>



이 그림은 SDDC의 핵심이 장비 통합보다도 "작업 흐름을 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 바꾸는 것"에 있음을 보여준다.

- **📢 섹션 요약 비유**: SDDC는 부서마다 도장을 받아야 움직이는 종이 행정이 아니라, 한 번 규칙을 넣으면 자동으로 처리되는 디지털 민원 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 SDDC의 4대 축
SDDC는 보통 컴퓨트, 스토리지, 네트워크, 관리 자동화 네 축으로 설명한다. 각각이 따로 좋아도, 상위 제어 평면이 이들을 함께 묶지 못하면 SDDC가 아니라 단순한 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 묶음에 그친다.

| 영역 | 핵심 기술 | 역할 |
| :--- | :--- | :--- |
| 컴퓨트 | 소프트웨어 정의 컴퓨트 (Software-Defined Compute, SDC) | 가상 머신·[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 배치 |
| 스토리지 | 소프트웨어 정의 스토리지 (Software-Defined Storage, [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/)) | 용량·[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| 네트워크 | 소프트웨어 정의 네트워크 (Software-Defined Network, [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)) | [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/), 가상 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), [서비스 체이닝](/knowledge-base/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/) |
| 관리/자동화 | [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/), [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/), [인프라 코드](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) | 전체 수명주기 제어 |

### 2.2 제어 평면과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면의 분리
SDDC의 핵심 원리는 제어 평면 (Control Plane)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane)의 분리다. 제어 평면은 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 배치, 권한, 모니터링을 담당하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면은 실제 계산·저장·패킷 전달을 수행한다. 이 구조를 통해 물리 장비를 교체해도 상위 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 운영 모델은 유지된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">User / API</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Portal / Orchestration / IaC</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Policy Engine : Placement / Security / Capacity / Rules</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SDC</div><div class="kb-diagram-cell">SDS</div><div class="kb-diagram-cell">SDN</div></div>
<div class="kb-diagram-note">Compute HW Storage HW Network HW</div>
</div>
</div>



이 그림에서 중요한 점은 사용자가 개별 장비에 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인하지 않는다는 것이다. 요청은 항상 포털이나 코드에서 시작하고, 실제 자원 배치는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진이 결정한다.

### 2.3 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 관리가 가져오는 변화
예전에는 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 규칙, 가상 머신 템플릿, 스토리지 품질 보장 ([Quality of Service](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/), [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/))을 각 장비에서 따로 맞췄다. SDDC에서는 "이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 99.9% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), 내부망 전용, 골드 스토리지 사용" 같은 의도를 선언하고, 시스템이 이를 여러 계층에 자동 반영한다. 이때 [인프라 코드](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))와 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진이 같은 언어로 움직여야 운영 재현성이 생긴다.

### 2.4 SDDC가 어려운 이유
자동화가 강력할수록 실수의 영향 범위도 커진다. 잘못된 템플릿이나 [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/) 하나가 수백 대의 가상 머신에 동시에 퍼질 수 있기 때문이다. 따라서 SDDC는 배포 자동화만이 아니라 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 가시성까지 함께 설계해야 한다.

- **📢 섹션 요약 비유**: SDDC 아키텍처는 공항 관제 시스템과 같다. 각 비행기 자체가 아니라, 전체 하늘길을 한 번에 조율하는 관제 규칙이 핵심이다.

---

## Ⅲ. 비교 및 연결

### 3.1 서버 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 SDDC의 차이
| 항목 | 서버 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) | SDDC |
| :--- | :--- | :--- |
| 관리 대상 | 주로 서버 자원 | 서버·스토리지·네트워크 전체 |
| 운영 방식 | 콘솔 중심 수동 작업 가능 | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 자동화 전제 |
| 보안 적용 | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 단위 중심 | 네트워크 세그먼트와 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 통합 |
| 확장 범위 | 클러스터 최적화 | [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 단위 운영 모델 |
| 핵심 가치 | 통합과 절감 | 민첩성, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 셀프서비스 |

서버 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 SDDC의 출발점이지 종착점이 아니다. 가상 머신이 많아져도 저장소와 네트워크가 여전히 수동 운영이라면, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 출시 속도는 기대만큼 빨라지지 않는다. 그래서 SDDC는 "[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)의 범위"보다 "운영 자동화의 깊이"로 구분해야 한다.

### 3.2 [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/), [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/), SDS와의 연결
HCI는 SDDC를 빠르게 구현하는 데 유리한 하드웨어/소프트웨어 묶음이고, SDS는 저장소 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층, SDN은 네트워크 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층이다. 이 셋이 함께 움직여야 SDDC가 되고, 어느 한 축만 강해도 전체 자동화는 불완전하다.

### 3.3 퍼블릭 클라우드와의 경계
퍼블릭 클라우드는 이미 거대한 SDDC의 외부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 버전이라고 볼 수 있다. 차이는 소유권과 책임 경계다. [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) SDDC는 기업이 하드웨어와 운영을 직접 책임지는 대신, 규제·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치·내부 시스템 연계를 더 세밀하게 통제할 수 있다.

- **📢 섹션 요약 비유**: 서버 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)가 악기 하나를 전자화한 것이라면, SDDC는 지휘자와 악보까지 디지털화해 오케스트라 전체를 코드로 연주하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 현실적인 도입 순서
대부분의 조직은 컴퓨트 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)부터 시작해 [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/), [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/), 셀프서비스 포털 순으로 확장한다. 이때 중요한 것은 기술 순서보다 운영 절차 표준화다. 변경 승인, 템플릿 관리, 권한 위임, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 추적이 정리되지 않으면 도구만 늘고 속도는 나아지지 않는다.

### 4.2 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 표준 템플릿과 골든 이미지가 준비되어 있는가?
2. 네트워크 동서 트래픽까지 가시화하는 관측 체계가 있는가?
3. 역할 기반 접근 제어 ([Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/))와 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 연결되어 있는가?
4. IaC와 수동 변경이 섞일 때 드리프트를 감지할 수 있는가?
5. 특정 벤더 기능에 과도하게 묶여 장기 전환 비용이 커지지 않는가?

### 4.3 흔한 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)는 해두고 배포 승인과 설정은 여전히 수작업 문서로 돌리는 경우
- [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 없이 외부 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)만 믿어 내부 동서 트래픽 보안을 놓치는 경우
- 조직은 그대로 사일로인데 기술만 SDDC라고 부르는 경우
- 통합 관측 없이 자동화만 늘려 장애 원인을 더 찾기 어렵게 만드는 경우

### 4.4 기술사 관점 판단
기술사 관점에서 SDDC의 핵심은 "[데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 소프트웨어처럼 운영할 수 있는가"다. 따라서 채택 기준은 단순한 기능 수가 아니라, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 셀프서비스 수준, 운영 조직의 준비도, 규제 요구사항 충족 여부가 된다. 즉 SDDC는 기술 도입 과제가 아니라 운영 모델 재설계 과제로 설명해야 한다.

- **📢 섹션 요약 비유**: SDDC 구축은 건물을 몇 채 더 짓는 일이 아니라, 도시의 도로·전기·치안 규칙을 한 번에 바꾸는 도시 재설계와 같다.

---

## Ⅴ. 기대효과 및 결론

SDDC가 자리 잡으면 인프라 요청은 장비 구매가 아니라 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 선언으로 바뀐다. 그 결과 배포 속도, 표준화, 보안 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [재해 복구](/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) 자동화 수준이 함께 올라간다. 또한 프라이빗 클라우드와 하이브리드 클라우드를 묶는 공통 운영 언어를 갖게 된다.

다만 SDDC는 높은 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)만큼 높은 통제력을 요구한다. 자동화 실패의 파급 범위가 크고, 특정 벤더 스택에 묶이면 오히려 유연성이 떨어질 수 있다. 앞으로는 인텐트 기반 운영 (Intent-Based Operations), [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 운영 ([Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/) for IT Operations, [AIOps](/knowledge-base/studynote/12_it_management/02_itsm_itil/099_aiops_chatbot_itsm_automation/)), 컴포저블 인프라가 SDDC를 더 자율적인 방향으로 확장할 것이다.

결국 SDDC는 "하드웨어를 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)했다"는 개념이 아니라, "[데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 프로그램처럼 설계하고 실행한다"는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: SDDC의 본질은 건물에 컴퓨터를 넣는 것이 아니라, 건물 전체를 하나의 거대한 운영체제로 바꾸는 데 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/)) | SDDC [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 코드로 선언하고 반복 배포하는 운영 방식 |
| [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) (Software-Defined Network) | 네트워크까지 소프트웨어 제어 범위를 넓히는 축 |
| [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) (Software-Defined Storage) | 저장소 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 기능을 장비 밖으로 끌어낸 계층 |
| [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) (Hyper-Converged Infrastructure) | SDDC를 빠르게 구축할 수 있게 돕는 통합 인프라 블록 |
| [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) | 셀프서비스와 자동화가 안전하게 작동하도록 하는 권한 체계 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">물리 장비 중심 데이터센터</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">서버 가상화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SDS · SDN 확산</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">오케스트레이션 · IaC 결합</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SDDC · 하이브리드 클라우드 · AIOps</div>
</div>
</div>



이 흐름은 "장비 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) → 자원 범위 확대 → 자동화 결합 → [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 전체 소프트웨어화"라는 진화 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날에는 놀이터의 미끄럼틀, 그네, 울타리를 따로따로 관리해서 고치는 데 오래 걸렸어요.
2. SDDC는 컴퓨터가 놀이터 전체를 보고 "여기 더 필요해!" 하고 알아서 준비해 주는 똑똑한 관리실이에요.
3. 그래서 더 빨리 놀 수 있지만, 관리실 규칙을 잘못 만들면 놀이터 전체가 한꺼번에 헷갈릴 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 632 / 803

← **이전**: [630. 하이퍼컨버지드 인프라 (HCI)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/)
**다음**: [632. SDS (Software Defined Storage)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) →

---
