+++
title = "751. 카오스 엔지니어링 (Chaos Engineering) HW 모의"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 카오스 엔지니어링 (Chaos Engineering)은 실제 운영 또는 운영과 매우 유사한 환경에서 노드 종료, 네트워크 단절, 디스크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 같은 <strong>하드웨어성 장애를 의도적으로 모의</strong>해 시스템의 정상 상태가 얼마나 유지되는지 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 실험 방법이다.
> 2. **가치**: 값싼 범용 서버와 복잡한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서는 고장을 없애는 것보다 <strong>고장이 나도 전체 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 계속 가치 제공을 하도록 만드는 것</strong>이 더 현실적이므로, 회복탄력성 (Resilience)을 운영 문화로 내재화할 수 있다.
> 3. **판단 포인트**: 좋은 카오스 실험은 무작위 파괴가 아니라 <strong>정상 상태 가설, 제한된 폭발 반경 (Blast <a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/">Radius</a>), 관측 지표, 중단 조건</strong>을 갖춘 통제된 실험이어야 한다.

---

## Ⅰ. 개요 및 필요성

카오스 엔지니어링 (Chaos Engineering)은 "장애는 언젠가 반드시 발생한다"는 전제에서 출발한다. 클라우드와 대규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템은 수많은 서버, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 계층, 스토리지 경로, 외부 의존성 위에 놓여 있어 일부 구성요소가 매일 고장 나는 것이 오히려 정상이다. 따라서 현대 시스템 설계의 질문은 "어떻게 절대 안 죽게 만들까"보다 **"일부가 죽어도 사용자가 핵심 기능을 계속 쓰게 만들까"** 로 이동했다.

여기서 "HW 모의"라는 말은 물리적 장비를 꼭 망가뜨린다는 뜻이 아니라, <strong>실제 하드웨어 장애와 비슷한 증상</strong>을 운영 계층에서 재현한다는 의미다. 예를 들어 서버 전원 차단은 인스턴스 종료로, 네트워크 카드 불안정은 패킷 손실과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로, 랙 전원 장애는 가용 영역 ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) Zone, AZ) 차단으로 모의할 수 있다. 중요한 것은 물리 장치 자체보다 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 체감하는 실패 패턴</strong>을 실험하는 것이다.

이 접근이 필요한 이유는 정상 경로 위주 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)만으로는 연쇄 장애를 발견하기 어렵기 때문이다. 한 노드가 죽었을 때 자동 재배치가 밀리면 큐가 폭주하고, 한 스토리지가 느려졌을 때 재시도가 폭증하면 주변 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)까지 함께 무너질 수 있다. 카오스 엔지니어링은 이런 숨은 의존성을 평상시에 드러내어, 시스템이 실제 장애를 학습하도록 만든다.

- **📢 섹션 요약 비유**: 카오스 엔지니어링은 유리 온실 속 식물을 키우는 대신, 바람과 비를 조금씩 겪게 해서 뿌리를 깊게 내리게 만드는 원예 훈련과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

카오스 엔지니어링의 기본 절차는 <strong>정상 상태 정의 → 가설 수립 → 작은 범위 실험 → 결과 관측 → 학습과 개선</strong>이다. 먼저 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 정상 상태를 나타내는 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 수준 지표 (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/">Service Level Indicator</a>, <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/">SLI</a>)</strong> 를 고른다. 예를 들어 주문 성공률, 스트리밍 재생 성공률, p95 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 같은 지표가 이에 해당한다. 이후 "웹 노드 1대가 사라져도 SLI는 유지된다" 같은 가설을 세우고, 제한된 범위에서 실험한다.

아래 그림은 카오스 실험이 파괴 행위가 아니라 <strong>가설 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 루프</strong>임을 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Chaos Engineering experiment</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Steady-state SLI</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Hypothesis</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Bounded experiment</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(stop node / cut link / throttle disk / lose AZ)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Observe SLI + traces + alerts</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── within guardrail ─▶ learn and codify</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── out of guardrail ─▶ abort and fix</div></div>
</div>
</div>



실험 유형도 계층별로 나눌 수 있다. 서버 종료, 디스크 I/O [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 네트워크 손실, 시간 동기 흔들림, 전원 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 상실처럼 <strong>인프라 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a>을 닮은 시나리오</strong>가 대표적이다. 이때 중요한 것은 한 번에 전부 무너뜨리는 것이 아니라, 작은 폭발 반경에서 시작해 점진적으로 키우는 것이다.

| 실험 유형 | 모의하는 HW/인프라 장애 | 확인할 질문 |
| :--- | :--- | :--- |
| 노드 종료 | 서버 전원 상실, 메인보드 다운 | 오토스케일·재배치가 충분히 빠른가 |
| [네트워크 지연](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)/손실 | [NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) 이상, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 혼잡, 케이블 문제 | [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)·[서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/)가 연쇄 장애를 막는가 |
| 디스크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)/오프라인 | 스토리지 컨트롤러 불안정, 미디어 오류 | 캐시·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·재시도가 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 일관성을 지키는가 |
| AZ/랙 차단 | 전원 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 장애, 랙 네트워크 분리 | 다중 영역 배치가 실제로 효과적인가 |

즉 카오스 엔지니어링의 핵심은 "무작위"가 아니라 <strong>정상 상태를 깨뜨리지 않는 범위에서 가정을 흔들어 보는 것</strong>이다. 실험은 반드시 중단 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 충분한 관측성, 책임자 가용 시간 안에서 수행되어야 한다.

- **📢 섹션 요약 비유**: 이 방법은 전쟁이 난 뒤 당황하지 않으려고 평소에 일부러 통신 훈련과 정전 훈련을 반복하는 부대 운영과 같다. 훈련은 통제되어 있지만, 배운 대응은 실전에서 큰 차이를 만든다.

---

## Ⅲ. 비교 및 연결

카오스 엔지니어링은 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/">결함 주입 테스트</a></strong>와 가까우면서도 범위가 더 넓다. Fault Injection이 특정 부품이나 경로의 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 메커니즘을 정밀하게 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다면, Chaos Engineering은 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경계에서 <strong>시스템 전체의 회복탄력성</strong>을 본다. 또 <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a> 훈련 (Disaster <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">Recovery</a> Drill)</strong> 이 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 단위의 대형 시나리오를 정기적으로 연습하는 활동이라면, 카오스 엔지니어링은 그보다 더 자주, 더 작은 단위로 운영 중 가정을 흔드는 실험 문화에 가깝다.

| 항목 | [결함 주입 테스트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/) | 카오스 엔지니어링 | [재해 복구](/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) 훈련 |
| :--- | :--- | :--- | :--- |
| 초점 | 특정 fault model [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 운영 회복탄력성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 대규모 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 주된 범위 | 부품·경로·기능 단위 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·시스템 단위 | 사이트·조직 단위 |
| 실험 빈도 | 개발/[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 시 반복 | 운영 중 지속적·점진적 | 분기·반기 단위가 많음 |
| 핵심 산출물 | 감지·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) | [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 유지 여부, 숨은 의존성 | 절차 숙련도, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 |

또한 [무정전 운영](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/749_non_stop_operation/) 아키텍처와도 연결된다. Non-Stop이 노드 내부나 장비 수준에서 단절을 흡수한다면, 카오스 엔지니어링은 <strong>클러스터·<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>·지역 단위에서 그런 가정이 실제로 유지되는지</strong>를 본다. 즉 하나는 구조를 만드는 작업이고, 다른 하나는 그 구조를 운영 현실 속에서 계속 증명하는 작업이다.

이 과정에서 고장 모드 및 영향 분석 (Failure Mode and Effects Analysis, [FMEA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/752_fmea/))은 훌륭한 출발점이 된다. FMEA로 우선순위 높은 고장 모드를 뽑고, Fault Injection으로 부품 수준에서 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한 뒤, Chaos Engineering으로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준까지 실험 범위를 넓히면 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 체계가 훨씬 닫힌 고리가 된다.

- **📢 섹션 요약 비유**: 카오스 엔지니어링은 소화기를 만져 보는 교육을 넘어서, 실제 건물에서 출입문 일부를 막아 보고도 사람들이 제대로 대피하는지 확인하는 전체 훈련에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 카오스 엔지니어링은 멋진 이벤트가 아니라 <strong>운영 안전 공학</strong>으로 다뤄야 한다. 가장 먼저 해야 할 일은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표 ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/), [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/))와 중단 조건을 정하는 것이다. 예를 들어 실험 중 주문 실패율이 0.5%를 넘으면 즉시 중단, p95 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 2배를 넘으면 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)처럼 guardrail을 명확히 둬야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 사용자 가치와 직접 연결된 [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)/SLO가 정의되어 있는가?
2. 실험 범위가 한 노드, 한 셀, 한 AZ처럼 제한되어 있는가?
3. 추적, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/), 알림 체계가 충분히 준비되어 있는가?
4. 실험 수행 시간에 대응 가능한 운영 인력이 대기 중인가?
5. 발견된 문제를 아키텍처와 런북에 실제로 반영하는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **쇼맨십형 파괴**: 관측성도 없이 무작정 노드를 종료해 놓고 "망하지 않았다"만 확인하는 실험이다.
- **상태 저장 계층 무시**: 프런트엔드만 실험하고 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)·메시지 큐·캐시 일관성은 건드리지 않으면 진짜 위험은 남는다.
- <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/">교훈</a> 없는 반복</strong>: 같은 실험을 계속 통과하는 것에 만족하고, 실패한 실험에서 설계 개선을 하지 않으면 문화가 형식화된다.

기술사 관점에서는 카오스 엔지니어링을 "운영 중 일부러 장애를 내는 것"으로만 쓰면 점수가 약하다. <strong>가설 기반 실험, 제한된 폭발 반경, 사용자 지표 <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a>, 결과 환류</strong>까지 구조화해서 설명해야 한다. 즉 이 개념의 핵심은 혼돈이 아니라 <strong>통제된 혼돈을 통한 <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a> 학습</strong>이다.

- **📢 섹션 요약 비유**: 좋은 카오스 실험은 아이를 물속에 그냥 던지는 것이 아니라, 구명 장비와 코치가 있는 수영장에서 짧게 잠수해 보게 하며 호흡법을 익히게 하는 훈련과 같다.

---

## Ⅴ. 기대효과 및 결론

카오스 엔지니어링이 잘 정착되면 조직은 장애를 "희귀한 재난"이 아니라 <strong>주기적으로 학습하는 운영 조건</strong>으로 다루게 된다. 그 결과 숨은 의존성, 재시도 폭주, 부정확한 알림, 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 미비 같은 문제가 실제 대형 장애 전에 드러난다. 이는 평균 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 단축뿐 아니라, 설계자와 운영자가 같은 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 언어를 공유하게 만든다는 점에서 가치가 크다.

다만 카오스 엔지니어링은 만능이 아니다. 용량 부족, 잘못된 릴리스, 보안 사고, 사람의 오조작은 별도의 통제 체계가 필요하다. 또한 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치 없이 운영 중 실험을 남발하면 오히려 고객 피해를 만들 수 있으므로, 단계적 도입과 엄격한 안전 장치가 전제되어야 한다.

앞으로는 카오스 실험이 [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/[지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/) / [Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD)와 더 깊게 연결되고, 디지털 트윈이나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진이 추천한 시나리오를 자동 실행하는 방향으로 발전하겠지만 본질은 같다. <strong>시스템이 정말로 고장에 강한지, 말이 아니라 실험으로 증명하는 것</strong>이 카오스 엔지니어링의 핵심이다.

- **📢 섹션 요약 비유**: 운동선수가 경기 당일만 잘하길 기대하지 않고 평소에 다양한 상황을 연습하듯, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)도 평소 작은 혼란을 겪어 봐야 큰 사고 때 흔들리지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 회복탄력성 (Resilience) | 카오스 엔지니어링이 직접 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하려는 시스템 특성이다. |
| [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) / [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) | 실험 중 정상 상태와 중단 조건을 정의하는 핵심 운영 지표다. |
| 폭발 반경 (Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/)) | 실험의 영향을 제한해 고객 피해를 통제하는 안전 장치다. |
| [결함 주입 테스트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/) | 카오스 엔지니어링의 세밀한 선행 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 단계로 자주 사용된다. |
| [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)) | 연쇄 장애를 막기 위해 카오스 실험에서 자주 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 패턴이다. |
| 게임 데이 (Game Day) | 팀이 계획적으로 수행하는 카오스/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 훈련 이벤트다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">부품 수준 신뢰성 설계</div>
<div class="kb-diagram-note">: FMEA · redundancy · watchdog</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">결함 주입 테스트 (Fault Injection Test)</div>
<div class="kb-diagram-note">: 특정 보호 메커니즘 검증</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">카오스 엔지니어링 (Chaos Engineering)</div>
<div class="kb-diagram-note">: service-level resilience experiment</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 게임 데이 (Game Day)</div>
<div class="kb-diagram-note">: 팀 단위 복구 훈련</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 자가 복구 운영</div>
<div class="kb-diagram-note">: autoscaling · circuit breaker · policy guardrail</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 카오스 엔지니어링은 학교에서 갑자기 정전이 나도 모두가 놀라지 않고 잘 움직이는지 연습해 보는 거예요.
2. 선생님은 일부러 한 교실 불을 꺼 보면서 다른 교실까지 다 같이 멈추지 않는지 살펴봐요.
3. 이렇게 미리 연습하면 진짜 문제가 생겨도 더 빨리 안전하게 대응할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 752 / 803

← **이전**: [750. 결함 주입 테스트 (Fault Injection Test)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/)
**다음**: [752. FMEA (Failure Mode and Effects Analysis)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/752_fmea/) →

---
