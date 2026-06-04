---
title: "159. 페일오버/페일백 아키텍처 (Failover/Failback Architecture)"
date: "2026-04-21"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트

> 1. **본질**: 페일오버 ([Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/))는 주 시스템 장애 시 대체 시스템으로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 책임을 넘기는 전환 메커니즘이고, 페일백 (Failback)은 주 시스템 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 다시 원래 경로로 복귀시키는 운영 절차다.
> 2. **가치**: 잘 설계된 페일오버/페일백 아키텍처는 [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 평균 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간)을 줄이고 단일 장애 지점 ([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure)을 제거해 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성을 높인다.
> 3. **판단 포인트**: 아키텍처 선택 기준은 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 시간), [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 시점), 상태 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 난이도다. 전환 속도만 볼 것이 아니라 복귀 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)까지 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

페일오버/페일백 아키텍처는 장애가 나도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 멈추지 않기 위해 주 경로와 대체 경로를 함께 설계하는 방식이다. 단일 리전, 단일 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 단일 로드밸런서에만 의존하면 장애 한 번이 전체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단으로 이어질 수 있다. 따라서 고가용성 시스템은 "어디가 고장 나면 어디로 넘길 것인가"를 미리 정해 두어야 한다.

여기서 중요한 점은 장애 대응이 전환에서 끝나지 않는다는 것이다. 많은 시스템이 페일오버에는 집중하지만, 주 시스템이 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)된 뒤 안전하게 돌아오는 페일백을 소홀히 한다. 그러나 실제 운영에서는 복귀 과정에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 역전, 캐시 불일치, 연결 재설정, 갑작스러운 부하 재집중이 발생해 두 번째 장애가 더 위험할 수 있다.

- **📢 섹션 요약 비유**: 페일오버는 메인 도로가 막혔을 때 우회도로로 차를 돌리는 일이고, 페일백은 공사가 끝난 뒤 다시 본선으로 안전하게 합류시키는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

페일오버 아키텍처는 단순히 서버를 하나 더 두는 문제가 아니다. 헬스 체크 (Health Check), [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 방식, 트래픽 전환 계층, 상태 저장 위치, 복귀 절차가 함께 맞물려야 한다. 특히 무상태 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 전환이 비교적 쉽지만, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)·[세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·캐시처럼 상태가 있는 계층은 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 핵심 병목이 된다.

```text
+----------------------------------------------------------------------+
|            페일오버/페일백의 기본 흐름과 상태 동기화 지점           |
+----------------------------------------------------------------------+
|  Client                                                              |
|    |                                                                  |
|    v                                                                  |
|  DNS / Load Balancer ---> Primary Region / AZ                          |
|           |                     |                                      |
|           |                     +- 서비스 인스턴스                    |
|           |                     +- Primary DB                          |
|           |                           | 복제                            |
|           |                           v                                 |
|           +-------- 장애 감지 ------> Standby Region / AZ              |
|                                         |                               |
|                                         +- Standby 서비스              |
|                                         +- Replica DB                  |
|                                                                      |
|  Failover : 트래픽을 Standby로 전환                                   |
|  Failback : 데이터 재동기화 확인 후 Primary로 점진 복귀               |
+----------------------------------------------------------------------+
```

이 그림이 말해 주는 핵심은 전환 대상이 서버 한 대가 아니라 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 계층 + <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 계층 + <a href="/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 계층</strong>이라는 점이다. 헬스 체크가 빨라도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 늦으면 RPO가 커지고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 맞아도 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) TTL이 길면 체감 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이 늘어난다.

| 아키텍처 유형 | 전환 준비 상태 | 일반적 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) | 일반적 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) | 특징 |
| :--- | :--- | :--- | :--- | :--- |
| [액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[액티브](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) ([Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)) | 양쪽 모두 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중 | 초 단위 이하 | 거의 0 | 가장 빠르지만 설계·운영 비용 높음 |
| [핫 스탠바이](/studynote/01_computer_architecture/13_reliability_power_management/457_hot_standby/) ([Hot Standby](/studynote/01_computer_architecture/13_reliability_power_management/457_hot_standby/)) | 대기 시스템이 거의 동일 규모로 준비 | 초~수분 | 초 단위 | 고가용성에 유리, 비용 큼 |
| 웜 스탠바이 (Warm Standby) | 축소된 대기 환경 유지 | 수분~수십 분 | 분 단위 | 비용과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)성의 절충 |
| [콜드 스탠바이](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/) ([Cold Standby](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/)) | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 보유, 재기동 필요 | 수시간~수일 | 시간 단위 이상 | 저비용이지만 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 느림 |
| [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)럿 라이트 (Pilot Light) | 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 상시 유지 | 수십 분 내외 | 분~시간 | 클라우드 DR에서 자주 쓰는 절충형 |

핵심 원리는 간단하다. RTO가 짧을수록 대기 자원을 더 많이 켜 두어야 하고, RPO가 작을수록 동기 또는 준실시간 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 필요하다. 결국 페일오버 설계는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제가 아니라 <strong>비용과 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 목표의 거래</strong>다.

- **📢 섹션 요약 비유**: 소방 설비도 스프링클러를 항상 연결해 둘지, 소화기만 둘지에 따라 비용과 대응 속도가 달라진다. 페일오버도 같은 원리로 준비 수준이 달라진다.

---

## Ⅲ. 비교 및 연결

페일오버는 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 전체 중 하나이며, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·[블루그린 배포](/studynote/04_software_engineering/02_requirements_analysis/116_blue_green_deployment/)·오토스케일링과는 목적이 다르다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 되살리는 데 강하지만 즉시 [서비스 전환](/studynote/12_it_management/02_itsm_itil/850_service_transition/)에는 약하고, 블루그린은 배포 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 낮추지만 재해 상황의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)까지 자동으로 해결해 주지는 않는다. 오토스케일링은 용량 부족 대응이지, 리전 단위 장애 대체와는 다른 문제다.

| 비교 대상 | 핵심 목적 | 장애 시 즉시성 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 초점 |
| :--- | :--- | :--- | :--- |
| 페일오버/페일백 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성 유지와 복귀 | 높음 | 매우 중요 |
| [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) & 복원 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 낮음 | 복원 시점이 핵심 |
| [블루그린 배포](/studynote/04_software_engineering/02_requirements_analysis/116_blue_green_deployment/) | 배포 안정성 | 중간 | [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 전환이 핵심 |
| 오토스케일링 | 부하 대응 | 높음 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 직접 관련 적음 |

또한 페일오버만 성공했다고 [회복](/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) [탄력성](/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)이 완성되는 것은 아니다. 헬스 체크, [서킷 브레이커](/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) ([Circuit Breaker](/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)), 재시도 백오프, 관측성, [카오스 엔지니어링](/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)과 연결해야 실제 장애 시 전환이 의도대로 작동한다. 결국 페일오버는 독립 기술이 아니라 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 운영 체계 속의 하나의 축이다.

- **📢 섹션 요약 비유**: 우산, 소화기, 비상구는 모두 안전 장치지만 쓰는 상황이 다르다. 페일오버는 그중 "다른 출구로 즉시 이동시키는 장치"에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 페일오버 자체보다 전환 조건과 페일백 조건을 명확히 문서화하는 것이 중요하다. 예를 들어 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 자동 승격이 가능한 환경이라도, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 일정 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 넘으면 자동 페일오버를 막고 수동 승인으로 전환해야 할 수 있다. 반대로 무상태 웹 계층은 헬스 체크 실패 2~3회만으로도 자동 전환이 가능하다.

페일백은 더 보수적으로 설계해야 한다. 주 시스템 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 곧바로 전체 트래픽을 되돌리면, 캐시 워밍업 부족과 연결 폭증으로 다시 장애가 날 수 있다. 따라서 읽기 전용 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 재동기화 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) ([Canary](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)) 방식의 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%->50%->100% 점진 복귀가 일반적인 모범 사례다.

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/RPO를 수치로 정의했는가?
2. 헬스 체크 실패 기준과 자동/수동 전환 경계를 정했는가?
3. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 마지막 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 시점을 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링하는가?
4. 페일백 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 점진 트래픽 복귀 절차가 있는가?
5. 정기적인 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 리허설과 카오스 테스트로 실제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 측정하는가?

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 전환만 구성하고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계층 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)는 따로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하지 않는 경우
- 페일오버는 자동인데 페일백 절차는 문서 없이 사람 기억에만 의존하는 경우
- 전환 테스트를 하지 않아 RTO가 설계 문서상의 숫자에만 머무는 경우

- **📢 섹션 요약 비유**: 비상 발전기를 설치하는 것만으로는 충분하지 않다. 언제 켜고, 언제 다시 메인 전원으로 바꿀지, 바꾸는 동안 냉장고가 꺼지지 않는지까지 연습해야 한다.

---

## Ⅴ. 기대효과 및 결론

적절한 페일오버/페일백 아키텍처는 장애를 없애지 못해도, 고객이 체감하는 중단 시간을 크게 줄인다. 단일 장애 지점을 제거하고, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성을 확보하며, 운영 조직이 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차를 반복 가능하게 만든다는 점에서 [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/), [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표) 달성에 직접 기여한다. 특히 멀티 AZ ([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) Zone), [멀티 리전](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 환경에서는 이 구조가 사실상 필수다.

하지만 그 대가로 인프라 비용, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 복잡도, 테스트 부담, 운영 자동화 수준 요구가 함께 올라간다. 따라서 이 개념은 "[백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 서버 하나 더 두기"로 기억하면 안 된다. 페일오버/페일백은 <strong><a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 목표와 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 정합성을 기준으로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 경로를 설계하고 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>하는 운영 아키텍처</strong>로 이해하는 것이 맞다.

- **📢 섹션 요약 비유**: 좋은 페일오버 설계는 예비 타이어를 트렁크에 넣어 두는 수준이 아니라, 언제 교체하고 다시 원래 바퀴로 안전하게 돌아올지까지 포함한 주행 계획이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)) | 얼마나 빨리 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해야 하는지를 정하는 핵심 기준 |
| [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)) | 어느 시점까지 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실을 허용할지를 정하는 기준 |
| [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | 페일오버 자동화 효과를 측정하는 운영 지표 |
| 헬스 체크 (Health Check) | 전환 여부를 판단하는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)원 |
| [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) ([Replication Lag](/studynote/05_database/04_transactions_concurrency/556_master_slave_replication_lag_inconsistency/)) | 페일백과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 위험의 핵심 지표 |
| [카오스 엔지니어링](/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/) ([Chaos 엔진ering](/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)) | 설계된 전환이 실제로 동작하는지 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 방법 |

### 📈 관련 키워드 및 발전 흐름도

```text
SPOF 제거 필요성
    |
    v
RTO · RPO 정의
    |
    v
핫/웜/콜드 스탠바이 · 파일럿 라이트 선택
    |
    v
헬스 체크 · 자동 전환 · 데이터 복제
    |
    v
페일백 검증 · 카오스 테스트 · SRE 운영 자동화
```

이 흐름은 "장애 위험 인식 -> [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 수립 -> 아키텍처 선택 -> 자동 전환 -> 복귀 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)"으로 이어지는 설계 사고를 정리한다.

### 👶 어린이를 위한 3줄 비유 설명

1. 다리가 끊어지면 옆의 예비 다리로 바로 건너가는 것이 페일오버예요.
2. 원래 다리를 고친 뒤 다시 안전하게 돌아오는 것이 페일백이에요.
3. 예비 다리도 튼튼한지 미리 걸어 보고, 돌아올 때도 천천히 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 다치지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 159 / 373

<- **이전**: [158. MTBF/MTTR 최적화 (MTBF/MTTR Optimization)](/studynote/15_devops_sre/03_sre_observability/158_mtbf_mttr_optimization/)
**다음**: [160. 헬스 체크/프로브 (Health Check/Probes)](/studynote/15_devops_sre/03_sre_observability/160_health_check_probes_liveness_readiness/) ->

---
