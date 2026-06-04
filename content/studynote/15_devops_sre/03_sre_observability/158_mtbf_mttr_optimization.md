+++
title = "158. MTBF/MTTR 최적화 (MTBF/MTTR Optimization)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/) ([Mean Time Between Failures](/knowledge-base/studynote/04_software_engineering/06_software_architecture/358_mtbf/), 평균 고장 간격)는 장애가 얼마나 드물게 일어나는지를, [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) ([Mean Time To Repair](/knowledge-base/studynote/04_software_engineering/06_software_architecture/359_mttr/) or Restore, 평균 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간)는 장애가 났을 때 얼마나 빨리 정상화하는지를 보여 주며, 두 값의 조합이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 결정한다.
> 2. **가치**: 현대 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) ([Site Reliability 엔진ering](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/))는 장애를 완전히 없애는 것보다, 탐지·대응·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 줄여 사용자 영향 시간을 최소화하는 편이 더 현실적이고 투자 대비 효과가 크다고 본다.
> 3. **판단 포인트**: MTTR은 하나의 시간이 아니라 탐지, 인지, 진단, 완화, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 단계의 합이므로, 병목 구간을 계측하지 않으면 "[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 빨리하자"는 구호만 남고 실제 개선은 일어나지 않는다.

---

## Ⅰ. 개요 및 필요성

[MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/)/[MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 최적화는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 복원력을 함께 다루는 운영 지표 관리다. MTBF가 길수록 장애가 드물고, MTTR이 짧을수록 장애가 나도 빨리 돌아온다. 결국 사용자가 체감하는 안정성은 "안 망가지는가"와 "망가져도 빨리 돌아오는가"의 균형에서 나온다.

이 개념이 중요해진 이유는 현대 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 클라우드, [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/), 외부 응용 프로그래밍 인터페이스([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), 매니지드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 깊게 의존하기 때문이다. 이런 환경에서는 모든 장애를 사전에 없애는 것이 사실상 불가능하다. 따라서 예방 투자만으로는 충분하지 않고, 장애가 발생했을 때 영향을 작게 끝내는 운영 능력이 핵심 경쟁력이 된다.

예를 들어 연 99.9% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 목표로 하면 허용 다운타임은 약 8.76시간이다. 이 목표는 MTBF를 크게 늘려서 달성할 수도 있지만, 장애 횟수가 다소 있더라도 MTTR을 짧게 만들어 달성할 수도 있다. 그래서 SRE는 무조건 장애 제로를 외치기보다, 장애를 빨리 탐지하고 안전하게 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 체계를 설계한다.

- **📢 섹션 요약 비유**: MTBF와 MTTR은 건강 관리와 응급 치료의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)와 같다. 병에 덜 걸리는 것도 중요하지만, 걸렸을 때 빨리 치료받는 능력도 똑같이 중요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 보통 `Availability = MTBF / (MTBF + MTTR)`로 설명한다. 이 식은 장애가 없던 시간과 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 하나의 주기로 묶어, 전체 시간 중 정상 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 시간이 차지하는 비율을 계산한 것이다. 따라서 MTBF를 늘리거나 MTTR을 줄이면 모두 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 좋아진다.

아래 그림은 장애 한 번이 발생했을 때 MTTR이 어떻게 여러 단계로 쪼개지는지 보여준다.

```text
+--------------------------------------------------------------------+
|                 장애 수명주기와 MTBF / MTTR 관계                  |
+--------------------------------------------------------------------+
| 정상 운영 구간 --------------------------- 장애 ------------------ |
|<------------- MTBF --------------------->|<------ MTTR ------->| |
|                                          |                      | |
|                                      탐지  인지  진단  완화  복구 | |
|                                      |----|----|----|----|----| | |
|                                      MTTD MTTA      복구 작업    | |
|                                                                    |
| MTTD = Mean Time To Detect      MTTA = Mean Time To Acknowledge    |
| MTTR = 위 단계 전체의 누적 시간                                   |
+--------------------------------------------------------------------+
```

이 그림의 핵심은 MTTR이 단순히 "수리 시간"이 아니라는 점이다. 실제 현장에서는 장애를 늦게 발견하는 시간이 가장 길 수도 있고, 담당자 호출은 빨라도 원인 진단이 느릴 수도 있다. 즉 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 최적화는 평균값 하나를 낮추는 일이 아니라, 각 단계의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 쪼개서 제거하는 일이다.

| 단계 | 대표 지표 | 병목 원인 | 개선 수단 |
| :--- | :--- | :--- | :--- |
| 탐지 | MTTD (Mean Time To Detect) | 경보 누락, [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 부정확 | [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·트레이스 통합, [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 기반 알림 |
| 인지 | MTTA (Mean Time To Acknowledge) | 온콜 부재, 알람 피로 | 자동 호출, 에스컬레이션 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| 진단 | Diagnosis Time | 관측성 부족, 의존성 불명확 | 대시보드, [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/), 런북 |
| 완화 | [Mitigation](/knowledge-base/studynote/09_security/12_identity_threat_advanced/605_golden_silver_ticket_mitigation/) Time | 수동 조치 과다 | 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/), 트래픽 차단 |
| [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | Restore Time | 배포 절차 복잡, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 블루그린, 페일오버, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 자동화 |

실무에서 자주 발견되는 사실은 MTBF를 2배 늘리는 것보다 MTTR을 절반 이하로 줄이는 편이 더 빠르게 체감 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 올린다는 점이다. 특히 사용자 영향은 장애 횟수보다 장애 지속 시간에 직접 비례하는 경우가 많아, 탐지 자동화와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 자동화의 투자 효과가 크게 나타난다.

- **📢 섹션 요약 비유**: [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 최적화는 불이 난 뒤 소방차를 더 빨리 보내는 체계를 만드는 일과 같다. 불이 전혀 안 나게 하는 것도 좋지만, 실제로는 발견·출동·진압이 얼마나 빠른지가 피해 규모를 좌우한다.

---

## Ⅲ. 비교 및 연결

[MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/) 개선과 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 단축은 모두 필요하지만, 성격이 다르다. MTBF는 장애 예방 중심이며 설계 품질, 테스트, 용량 계획, [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)에 영향을 많이 받는다. 반면 MTTR은 장애 대응 중심이며 관측성, 온콜 체계, 자동화, 런북 품질의 영향을 많이 받는다.

| 관점 | [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/) 개선 | [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 단축 |
| :--- | :--- | :--- |
| 초점 | 장애 발생 빈도 감소 | 장애 지속 시간 감소 |
| 주된 투자 | 아키텍처 안정화, [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/), [용량 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_capacity_management/) | [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링, 런북, 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 훈련 |
| 효과 발현 | 장기적·예방적 | 즉각적·운영적 |
| 측정 난이도 | 원인 복합적, 예측 어려움 | 단계별 계측 가능 |
| [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 관점 | 중요하지만 불확실성 큼 | 빠른 ROI를 기대하기 쉬움 |

또한 [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/)/MTTR은 [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)), 에러 버짓([Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)), 페일오버([Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)), 헬스 체크(Health Check)와 직접 연결된다. 예를 들어 월간 에러 버짓이 43분인데 장애가 평균 4회 난다면, 장애당 허용 MTTR은 약 10분 수준으로 역산된다. 즉 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 목표는 막연한 운영 감각이 아니라 SLO에서 내려오는 정량 목표다.

비슷한 용어와의 구분도 중요하다. [MTTF](/knowledge-base/studynote/04_software_engineering/06_software_architecture/360_mttf/) ([Mean Time To Failure](/knowledge-base/studynote/04_software_engineering/06_software_architecture/360_mttf/))는 수리하지 않는 대상의 평균 고장 시점을 주로 말하고, MTBF는 수리 가능한 시스템의 고장 간 간격을 보는 데 적합하다. 시험 답안에서는 이 차이를 짚어 주면 개념 경계가 또렷해진다.

- **📢 섹션 요약 비유**: MTBF는 튼튼한 운동화를 고르는 일이고, MTTR은 끈이 끊어졌을 때 바로 묶거나 교체할 수 있는 준비를 해 두는 일과 같다. 오래 가는 신발도 필요하지만, 고장 났을 때 바로 대응할 준비도 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/)/[MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 최적화는 "장애 후 회고"가 아니라 "장애 전 설계"에 가깝다. 어떤 알림을 받고, 누가 응답하고, 어느 대시보드로 진단하고, 어떤 버튼으로 완화할지까지 미리 설계해야 실제 MTTR이 줄어든다. 즉 운영은 사람의 숙련에만 맡길 일이 아니라, 반복 가능한 프로세스와 자동화 자산으로 만들어야 한다.

### 실무 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **탐지 기준이 SLO와 연결되는가**: 중앙 처리 장치(CPU, Central Processing Unit) 90% 같은 자원 경보보다 사용자 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 오류율 중심 경보가 있는가?
2. **온콜 체계가 명확한가**: 알림 대상, 에스컬레이션 순서, 대체 인력이 준비되어 있는가?
3. **진단 도구가 이어지는가**: [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)에서 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에서 트레이스로 자연스럽게 내려갈 수 있는가?
4. **완화 수단이 자동화되어 있는가**: [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 트래픽 우회, [스케일 아웃](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)을 수동 승인 없이 실행할 수 있는가?
5. **훈련이 반복되는가**: [카오스 엔지니어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/), 게임데이, 포스트모템으로 대응 근육을 키우는가?

### 투자 우선순위 판단

- MTTD가 길면: 경보 설계와 관측성 표준화에 먼저 투자
- 진단이 길면: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 맵, [분산 추적](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/), 런북 품질 향상에 투자
- [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 길면: 페일오버, 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차 자동화에 투자
- MTBF가 지나치게 짧으면: 배포 품질, 의존성 관리, 용량 계획을 재설계

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **평균값만 보는 관리**: P95 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이 매우 긴데 평균 MTTR만 보고 안심하는 경우
- **알람 과다**: 온콜이 실제 심각 알람을 놓치게 만드는 경보 피로(Alert Fatigue)
- **문서만 있는 런북**: 실제 상황에서 따라 하기 어려운 이론적 대응 절차

기술사 관점에서는 [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/)/MTTR을 단순 공식보다 "[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 설계 가능한 운영 체계로 바꾸는 지표"로 설명하는 것이 중요하다. 즉 측정, 자동화, 훈련, 회고가 함께 돌아가야 수치가 실제 개선으로 이어진다.

- **📢 섹션 요약 비유**: [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 개선은 응급실 벽에 매뉴얼을 붙이는 것만으로 끝나지 않는다. 의사 호출, 검사 장비, 수술실 준비가 실제로 이어져야 환자를 살릴 수 있다.

---

## Ⅴ. 기대효과 및 결론

[MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/)/MTTR을 체계적으로 최적화하면 사용자 영향 시간을 줄이고, 장애 대응의 예측 가능성을 높이며, 운영 조직의 스트레스를 낮출 수 있다. 특히 MTTR이 짧아지면 같은 수준의 장애가 발생해도 비즈니스 손실과 고객 불만이 크게 줄어든다. 이는 곧 더 공격적인 배포와 더 건강한 에러 버짓 운영으로 이어진다.

한계도 분명하다. 평균값은 긴 꼬리([long tail](/knowledge-base/studynote/12_it_management/01_governance_strategy/031_long_tail/))를 숨길 수 있고, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 중요도가 다른데도 하나의 공통 목표만 강요하면 왜곡이 생긴다. 또한 외부 의존성 장애처럼 우리 통제 바깥의 문제는 [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/) 개선 여지가 제한적일 수 있다.

앞으로는 [AIOps](/knowledge-base/studynote/12_it_management/02_itsm_itil/099_aiops_chatbot_itsm_automation/) ([Artificial Intelligence for IT Operations](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/252_aiops_artificial_intelligence_it_operations_auto_healing/)), 자동 원인 분석, 자가 치유(Self-Healing) 운영이 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 단축을 더 밀어 줄 가능성이 크다. 다만 자동화가 늘수록 잘못된 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 대형 장애를 만들 위험도 커지므로, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 런북과 안전한 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 경로를 함께 갖춰야 한다. 결국 기억할 핵심은 이것이다. 좋은 운영은 장애가 없는 운영이 아니라, 장애가 나도 빨리 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)하는 운영이다.

- **📢 섹션 요약 비유**: [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/)/[MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 최적화는 넘어지지 않는 연습만 하는 것이 아니라, 넘어져도 바로 일어나는 연습을 함께 하는 것과 같다. 진짜 강한 팀은 완벽한 팀이 아니라 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)이 빠른 팀이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [MTBF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/450_mtbf/) ([Mean Time Between Failures](/knowledge-base/studynote/04_software_engineering/06_software_architecture/358_mtbf/)) | 장애 간 평균 간격으로 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 수준을 가늠하는 지표 |
| [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) ([Mean Time To Repair](/knowledge-base/studynote/04_software_engineering/06_software_architecture/359_mttr/) or Restore) | 장애 발생 후 정상 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)까지의 평균 시간 |
| MTTD (Mean Time To Detect) | 장애를 알아차리는 속도로 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 초반 병목을 결정 |
| MTTA (Mean Time To Acknowledge) | 담당자가 인지하고 대응을 시작하는 시간 |
| [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)) | 허용 가능한 장애 시간과 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 목표를 정하는 기준 |
| 에러 버짓 ([Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)) | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 목표에서 허용된 실패 예산으로, 운영 의사결정과 연결됨 |
| 페일오버 ([Failover](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)) | 장애 시 대체 경로로 빠르게 전환해 MTTR을 줄이는 수단 |
| [카오스 엔지니어링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/) ([Chaos 엔진ering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)) | 실제 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계가 작동하는지 사전에 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 훈련 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
가용성 목표(SLO)
    |
    v
장애 측정 체계 수립
    |
    +--> MTBF (Mean Time Between Failures)
    +--> MTTR (Mean Time To Repair or Restore)
            |
            +--> MTTD / MTTA / 진단 / 복구 단계 분해
            +--> 관측성 · 온콜 · 런북 · 자동 복구
            +--> 페일오버 · 카오스 엔지니어링 · AIOps
```

이 흐름은 "[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 목표 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) -> 장애 측정 -> 단계별 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 최적화 -> 자동화 확장"으로 이어지는 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 운영 성숙 단계를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MTBF는 장난감이 얼마나 오래 안 고장 나는지 알려 주는 시간이에요.
2. MTTR은 고장 났을 때 얼마나 빨리 다시 가지고 놀 수 있는지 알려 주는 시간이에요.
3. 좋은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 잘 안 고장 나기도 하지만, 고장 나도 금방 다시 움직인답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 373

<- **이전**: [157. 다크 부채 (Dark Debt) / 운영 부채 (Operational Debt) 청산 전략](/knowledge-base/studynote/15_devops_sre/03_sre_observability/157_operational_debt_dark_debt/)
**다음**: [159. 페일오버/페일백 아키텍처 (Failover/Failback Architecture)](/knowledge-base/studynote/15_devops_sre/03_sre_observability/159_failover_failback_architecture/) ->

---
