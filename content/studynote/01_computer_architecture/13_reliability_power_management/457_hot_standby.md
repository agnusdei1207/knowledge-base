---
title: "457. 핫 스탠바이 (Hot Standby)"
date: "2026-03-20"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 핫 스탠바이 (Hot Standby)는 예비 장비를 이미 가동한 상태로 두고, 운영 상태와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 거의 실시간으로 맞춰서 장애 순간 즉시 주 장비 역할을 넘겨받게 하는 고가용성 기법이다.
> 2. **가치**: 핵심 목표는 단순 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 아니라 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간, 즉 [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair)을 사람 체감이 거의 없는 수준으로 줄여 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성을 확보하는 데 있다.
> 3. **판단 포인트**: 핫 스탠바이는 빠른 절체만 보고 채택하면 안 되며, [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [스플릿 브레인](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) (Split-Brain), 비용, 운영 훈련까지 감당할 수 있을 때 비로소 효과가 난다.

---

## Ⅰ. 개요 및 필요성

핫 스탠바이 (Hot Standby)는 주 시스템이 장애를 일으켜도 예비 시스템이 즉시 업무를 이어받도록, 예비 장비를 평소에도 켜 두고 동일한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 상태를 유지하는 대기 방식이다. 핵심은 "장애 후 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)"가 아니라 "장애가 나도 거의 끊기지 않는 운영"에 있다. 단순 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 있는 구조에서는 서버가 고장 난 뒤 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 부팅, 애플리케이션 기동, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원, 네트워크 전환이 차례로 필요해 수 분에서 수 시간의 공백이 생긴다.

이 방식이 필요해진 배경은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 가치가 하드웨어 가격보다 훨씬 커졌기 때문이다. 결제, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 거래, 제어 시스템처럼 몇 초의 중단도 매출 손실이나 안전 문제로 이어지는 환경에서는 "고장 나면 고친다"는 접근이 너무 늦다. 그래서 예비 장비를 미리 준비하고, 사용자 입장에서는 같은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 계속 이어지는 착시를 만들도록 설계한다.

아래 그림은 핫 스탠바이가 왜 단순 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)보다 본질적으로 다른지 보여준다. 차이는 예비 장비의 존재 여부가 아니라, <strong>장애 전부터 준비를 얼마나 끝내 두었는가</strong>에 있다.

```text
+----------------------------------------------------------------------+
|            장애 대응 방식의 차이: 복구 준비 시점이 다르다           |
+----------------------+----------------------+------------------------+
| 구분                 | 평상시 예비 장비 상태 | 장애 후 필요한 추가 작업 |
+----------------------+----------------------+------------------------+
| 백업만 있는 구조     | 꺼져 있거나 미구성     | 부팅 + 복원 + 전환        |
| 콜드 스탠바이       | 전원 OFF               | 설치 + 복원 + 전환        |
| 웜 스탠바이         | 일부 기동              | 애플리케이션 완성 + 전환  |
| 핫 스탠바이         | 서비스 가능 상태       | 권한 전환 중심            |
+----------------------+----------------------+------------------------+
```

핫 스탠바이는 결국 시간을 돈으로 사는 전략이다. 예비 서버, 네트워크, 라이선스, [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 채널을 평소에도 유지해야 하므로 비용은 크지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단절에 대한 사업 리스크를 줄이는 데는 매우 강력하다.

**📢 섹션 요약 비유**: 핫 스탠바이는 응급실의 대기 의료진과 같다. 환자가 쓰러진 뒤 의사를 찾는 구조가 아니라, 의사가 이미 옆방에서 장갑까지 끼고 기다리다가 바로 투입되는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핫 스탠바이의 핵심 원리는 세 가지다. 첫째, 주 장비와 예비 장비가 동일한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구성을 유지해야 한다. 둘째, 상태와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 충분히 최신이어야 한다. 셋째, 장애를 빠르게 감지하고 트래픽이나 역할을 안전하게 넘겨야 한다. 이 셋 중 하나라도 약하면 "켜져만 있는 예비 서버"에 그친다.

대표 구성은 [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Standby 쌍, 하트비트 (Heartbeat) 채널, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 경로, 절체 제어기로 이뤄진다. 하트비트는 상대 생존 여부를 확인하고, [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 차이를 줄이며, 절체 제어기는 VIP (Virtual IP) 이동이나 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 변경으로 사용자의 요청 방향을 바꾼다. 이때 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 품질이 낮으면 빠르게 전환해도 오래된 상태로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)하게 되므로, 절체 속도만큼 정합성도 중요하다.

| 구성 요소 | 역할 | 설계 시 주의점 |
| :-- | :-- | :-- |
| [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 노드 | 실제 요청 처리, 원본 상태 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 장애 원인이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 포화인지 하드웨어 결함인지 구분 필요 |
| Standby 노드 | 즉시 승격 가능한 예비 실행 환경 | [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), 패치 수준이 Active와 동일해야 함 |
| Heartbeat 채널 | 생존 및 연결 상태 감시 | 단일 감시선만 두면 오탐 가능성 증가 |
| [Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 경로 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)/[세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 상태 전달 | 동기식은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 증가, 비동기식은 손실 위험 |
| [Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) 오케스트레이터 | 승격, VIP 이동, fencing 수행 | 자동화 실패 시 이중 [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) 위험 |

아래 흐름은 장애 감지부터 절체까지의 논리를 단순화한 것이다.

```text
+----------------------------------------------------------------------+
|               핫 스탠바이의 평상시와 절체 시퀀스                    |
+----------------------------------------------------------------------+
| [Client]                                                            |
|    |                                                                 |
|    v                                                                 |
| [VIP / LB] ----------------> [Active] --------> 서비스 응답            |
|    |                           |                                      |
|    |                           +---- Heartbeat -----> [Standby]        |
|    |                           +---- Replication ---> [Standby]        |
|    |                                                                  |
| 장애 감지                                                             |
|    |                                                                  |
|    +---- Active 응답 중단                                             |
|    +---- 오케스트레이터가 fencing 수행                                |
|    +---- VIP / 역할 전환 ----------> [Standby -> New Active]            |
+----------------------------------------------------------------------+
```

이 구조에서 가장 까다로운 지점은 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 방식이다. 동기식 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 예비 장비가 기록을 받기 전까지 완료를 인정하지 않아 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 가능성을 낮춘다. 반면 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 늘고, 예비 장비가 느려지면 주 장비 처리량도 함께 흔들린다. 비동기식 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 유리하지만 장애 직전 변경분이 누락될 수 있다. 즉 핫 스탠바이는 "무조건 빠른 절체"가 아니라 <strong>정합성과 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 사이의 설계 선택</strong>이다.

**📢 섹션 요약 비유**: 핫 스탠바이의 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)는 속기사 두 명이 같은 회의록을 동시에 적는 것과 같다. 둘 다 같은 줄까지 써야 안심되지만, 한 명이 느리면 회의 진행도 함께 느려진다.

---

## Ⅲ. 비교 및 연결

핫 스탠바이를 제대로 이해하려면 [콜드 스탠바이](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/) ([Cold Standby](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/)), 웜 스탠바이 (Warm Standby), 액티브-액티브 ([Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-[Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/))와 경계를 나눠 봐야 한다. 차이는 단순히 서버 전원이 켜져 있느냐가 아니라, <strong>장애 전 준비 수준과 장애 후 의사결정 복잡도</strong>에 있다.

| 방식 | 평상시 예비 자원 상태 | 절체 속도 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최신성 | 특징 |
| :-- | :-- | :-- | :-- | :-- |
| [콜드 스탠바이](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/) | 거의 미가동 | 느림 | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시점 기준 | 비용 최소, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차 큼 |
| 웜 스탠바이 | 일부 기동 | 중간 | 주기적 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 비용과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 절충 |
| 핫 스탠바이 | 완전 기동 | 빠름 | 거의 실시간 | 고비용, 고가용성 중심 |
| 액티브-액티브 | 둘 다 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공 | 매우 빠름 | 동시 처리 설계 필요 | 부하분산 가능, 충돌 제어 복잡 |

핫 스탠바이는 액티브-액티브보다 단순하고 예측 가능하지만, 예비 장비가 평소 유휴 상태에 가까워 자원 효율은 떨어진다. 반대로 액티브-액티브는 자원 활용도는 높지만 [동시 쓰기](/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/) 충돌, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 합의, [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장이 훨씬 어렵다. 따라서 단일 마스터 구조의 관계형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)나 제어계 시스템은 여전히 핫 스탠바이를 선호하는 경우가 많다.

또한 이 개념은 컴퓨터구조를 넘어 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 네트워크, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)와 연결된다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 프로세스와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 상태 유지, 네트워크는 하트비트와 VIP 이동, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 승격 절차가 핵심이다. 결국 핫 스탠바이는 한 장비 기술이 아니라 <strong>계층 간 협업으로 만드는 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 연속성 패턴</strong>이다.

[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 관점에서는 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))와 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))를 함께 봐야 한다. 핫 스탠바이는 대개 RTO를 크게 줄이는 데 강하고, 동기식 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 곁들이면 RPO도 0에 가깝게 만들 수 있다. 하지만 비동기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 기반 핫 스탠바이는 "절체는 빠르지만 직전 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 일부 잃을 수 있는" 형태가 될 수 있으므로, 이름만으로 무중단·무손실을 가정하면 안 된다.

**📢 섹션 요약 비유**: 콜드·웜·핫 스탠바이는 겨울 외출 준비와 비슷하다. 옷을 옷장에만 넣어두면 콜드, 현관에 걸어두면 웜, 이미 다 입고 신발끈까지 맨 상태가 핫이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 핫 스탠바이 도입 여부는 기술 취향이 아니라 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 등급과 손실 비용으로 판단해야 한다. 수 초의 중단이 곧 매출 손실, [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) ([Service Level Agreement](/studynote/12_it_management/02_itsm_itil/869_sla/)) 위반, 안전 사고로 이어지는 시스템이라면 핫 스탠바이가 정당화된다. 반대로 내부 배치, 통계, 비핵심 관리 시스템처럼 중단 허용 폭이 큰 환경에서는 웜 또는 [콜드 스탠바이](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/)가 더 합리적일 수 있다.

특히 자동 절체를 도입할 때는 "장애를 빨리 감지하는 것"보다 "잘못 절체하지 않는 것"이 더 중요하다. 네트워크 분리 때문에 Active가 살아 있는데도 Standby가 자신을 승격하면 [스플릿 브레인](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/)이 발생한다. 이를 막기 위해 fencing, quorum, witness 노드 같은 장치를 두어 기존 Active를 확실히 배제해야 한다. 즉 자동화는 편의 기능이 아니라 안전장치까지 포함한 설계 문제다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 장애 허용 시간과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 허용치가 숫자로 정의되어 있는가?
2. 동기식/비동기식 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 선택 이유가 업무 특성과 연결되어 있는가?
3. 절체 시 VIP 이동, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이름 시스템 ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/), [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) 전환, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 처리 방식이 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되었는가?
4. [스플릿 브레인](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) 방지용 fencing 또는 제3자 판정 장치가 있는가?
5. 정기적인 장애 모의훈련으로 실제 승격 절차를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했는가?

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 예비 서버만 켜 두고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정합성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 하지 않는 경우
- 자동 절체는 구성했지만 수동 복귀 절차는 준비하지 않은 경우
- [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이 소프트웨어 문제인데 고가용성 구조만 추가하는 경우
- 운영 중 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 차이로 Active와 Standby가 다른 동작을 하는 경우

실무 시나리오를 하나 들면, 금융 계정계 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)는 핫 스탠바이와 준동기 또는 동기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 선택할 가능성이 크다. 반면 대용량 [로그 분석](/studynote/16_bigdata/05_analysis/119_log_analysis/) 플랫폼은 수 분의 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 허용하고 비용을 낮추는 쪽이 더 현실적이다. 기술사 관점의 답안에서도 결론은 동일하다. <strong>핫 스탠바이는 최고급 해법이 아니라, 높은 연속성 요구를 가진 일부 업무에 선택적으로 써야 하는 비싼 해법</strong>이다.

**📢 섹션 요약 비유**: 핫 스탠바이는 모든 건물에 헬리콥터 착륙장을 짓는 일이 아니다. 불이 나면 안 되는 건물에만 비싼 설비를 올려야 전체 도시 예산이 버틴다.

---

## Ⅴ. 기대효과 및 결론

핫 스탠바이의 가장 큰 효과는 장애를 "[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 사건"에서 "역할 전환 이벤트"로 바꾸는 데 있다. 사용자는 서버가 바뀌었다는 사실을 거의 느끼지 못하고, 운영자는 유지보수와 장애 대응을 더 계획적으로 수행할 수 있다. 하드웨어 단일 장애 지점 (Single Point of Failure) 제거, [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상, 계획 정비의 유연성 확보가 대표 이점이다.

그러나 전제가 충족되지 않으면 기대효과는 쉽게 무너진다. 예비 장비가 실제로 최신 상태를 유지하지 못하면 핫 스탠바이는 이름뿐인 보험이 된다. 또한 소프트웨어 버그, 잘못된 배포, 논리적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손상은 주 장비와 예비 장비 모두에 함께 전파될 수 있으므로, 핫 스탠바이는 모든 장애의 만능 해법이 아니다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 배포 통제와 함께 가야 진짜 복원력을 만든다.

앞으로는 전통적 [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/)-Standby 구조만이 아니라, 클라우드 관리형 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 오토스케일링, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 오케스트레이션과 결합한 형태로 진화하고 있다. 그럼에도 기억해야 할 본질은 변하지 않는다. 핫 스탠바이는 "예비 장비를 켜 둔 것"이 아니라 <strong>상태를 이어받을 준비를 평상시에 끝내 두는 운영 철학</strong>이다.

**📢 섹션 요약 비유**: 핫 스탠바이는 우산을 산 뒤 창고에 넣어두는 것이 아니라, 비가 올 때 바로 펼치도록 현관문 옆에 펼침 방향까지 맞춰 세워두는 습관이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 고가용성 (HA, High [Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) | 핫 스탠바이의 상위 목표로, 장애 중에도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성을 유지하려는 설계 원칙 |
| 페일오버 ([Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/)) | Active에서 Standby로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 역할을 넘기는 실제 절차 |
| [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) ([Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 상태를 예비 장비에 반영해 절체 후 정합성을 유지하는 핵심 메커니즘 |
| [스플릿 브레인](/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) (Split-Brain) | 두 노드가 동시에 자신을 주 노드로 인식해 충돌하는 대표 장애 패턴 |
| [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) ([DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/), Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | 핫·웜·[콜드 스탠바이](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/)를 포함해 장애 이후 업무 연속성을 설계하는 더 넓은 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 장비 운영
    |
    v
이중화 (Redundancy)
    |
    +-- 콜드 스탠바이 (Cold Standby)
    +-- 웜 스탠바이 (Warm Standby)
    +-- 핫 스탠바이 (Hot Standby)
            |
            v
하트비트 + 복제 + 자동 페일오버
            |
            v
고가용성 (HA, High Availability) / 재해 복구 (DR, Disaster Recovery)
            |
            v
액티브-액티브 · 클라우드 관리형 고가용성 아키텍처
```

이 흐름은 단순 예비 장비 확보에서 시작해, 자동 절체와 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 운영으로 고도화되는 고가용성 설계의 발전 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 핫 스탠바이는 주전 선수가 다치면 바로 뛰어들 수 있게, 후보 선수가 이미 운동복을 입고 옆에서 준비하는 거예요.
2. 후보 선수는 그냥 서 있기만 하는 게 아니라, 작전도 똑같이 듣고 몸도 풀고 있어야 해요.
3. 그래서 돈은 더 들지만, 경기가 거의 끊기지 않고 계속 이어질 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 458 / 803

<- **이전**: [456. 이중화 (Dual Redundancy)](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)
**다음**: [458. 콜드 스탠바이 (Cold Standby)](/studynote/01_computer_architecture/13_reliability_power_management/458_cold_standby/) ->

---
