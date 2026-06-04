+++
title = "212. BIA (Business Impact Analysis) 평가 지표 분석 기법"
date = 2026-05-08

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BIA (Business Impact Analysis)는 장애를 기술 문제가 아니라 업무 손실의 크기로 해석해, 무엇을 먼저 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해야 하는지 정하는 우선순위 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)이다.
> 2. **가치**: [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)), [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)), [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) 투자 수준은 서버 수가 아니라 매출·법규·고객 신뢰 손실의 시간축 분석에서 결정된다.
> 3. **판단 포인트**: 핵심은 시스템 목록 작성이 아니라 업무 중단 영향, 허용 중단 시간, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 허용치, 업무 의존성을 함께 연결해 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표를 현실적으로 산정하는 데 있다.

---

## Ⅰ. 개요 및 필요성

BIA (Business Impact Analysis)는 특정 업무나 시스템이 멈췄을 때 조직이 감당해야 하는 손실을 분석하여 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위를 정하는 기법이다. [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 "어떻게 복원할까"를 다룬다면, BIA는 "무엇을 언제까지 살려야 회사가 버티는가"를 먼저 답한다. 그래서 BCP (Business Continuity Planning)와 [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 출발점으로 취급된다.

이 기법이 필요한 이유는 모든 시스템이 같은 중요도를 갖지 않기 때문이다. 주문, 결제, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)처럼 매출과 고객 경험에 직접 연결된 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 30분 중단도 치명적일 수 있지만, 분석 리포트나 내부 포털은 수 시간 또는 수 일 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 허용할 수 있다. BIA 없이 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 계획을 세우면 기술팀은 눈에 보이는 시스템부터 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하고, 경영진은 실제 손실이 큰 프로세스를 뒤늦게 발견하는 오류를 반복한다.

특히 클라우드와 SaaS가 혼합된 환경에서는 한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 중단이 단일 애플리케이션 문제로 끝나지 않는다. 주문은 살아 있어도 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 결제 승인, 재고 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), 알림이 이어서 막히면 실제 업무는 중단된다. 따라서 BIA는 개별 서버보다 "업무 체인 전체가 언제 멈추는가"를 보게 만드는 경영-IT 공통 언어다.

- **📢 섹션 요약 비유**: BIA는 화재 현장에서 모든 물건을 같이 들고나오려는 것이 아니라, 산소통·구급약·출입 열쇠처럼 생존에 직결되는 물건부터 먼저 챙기게 만드는 비상 가방 목록과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

BIA의 핵심 산출물은 MTPD (Maximum Tolerable Period of Disruption), [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), 그리고 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 등급이다. 보통 업무 단위로 영향도를 수집하고, 그 업무를 지원하는 애플리케이션·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·인력·외부 의존 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 연결한 뒤, 시간 경과에 따라 손실이 어떻게 커지는지 계산한다. 이 과정에서 "업무 허용 한계"가 먼저 나오고, 그다음 그 한계보다 짧은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표를 설계한다.

| 항목 | 의미 | 실무 판단 포인트 |
| :--- | :--- | :--- |
| 영향도 분석 | 매출, 법규, 운영, 평판 손실 측정 | 정성 평가를 가능한 한 금액·시간·건수로 환산 |
| MTPD | 버틸 수 있는 최대 중단 시간 | 업무 지속 가능 한계선으로 사용 |
| [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 시간 | MTPD보다 짧아야 하며 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차와 인프라가 이를 보장해야 함 |
| [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) | 허용 가능한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 시점 | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 주기, [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 방식, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치와 직접 연결 |
| [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 티어 | Hot/Warm/Cold 등 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 수준 | 비용 대비 손실 회피 효과를 함께 검토 |

아래 그림은 BIA가 단순 조사서가 아니라 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표를 산출하는 의사결정 흐름임을 보여준다.

```text
+----------------------------------------------------------------------+
| BIA flow: impact -> tolerance -> recovery target -> DR tier         |
+----------------------------------------------------------------------+
| Business process outage                                             |
|        |                                                             |
|        +-> Impact by time                                            |
|        |    - revenue loss                                           |
|        |    - legal penalty                                          |
|        |    - customer trust                                         |
|        |                                                             |
|        +-> MTPD                                                      |
|        |                                                             |
|        +-> Recovery target                                           |
|        |    - RTO < MTPD                                             |
|        |    - RPO by data loss tolerance                             |
|        |                                                             |
|        +-> DR tier selection                                         |
|             Hot site / Warm site / Cold site                         |
+----------------------------------------------------------------------+
```

예를 들어 카드 승인 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 MTPD가 2시간이면, RTO는 30분~1시간 수준으로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되어야 의미가 있다. 또 주문 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 5분만 유실되어도 정산 문제가 생긴다면 RPO는 5분 이하가 되어야 하며, 이는 비동기 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 아닌 실시간 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)나 저지연 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 전송을 요구한다. 즉 BIA는 숫자를 적는 문서가 아니라 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 비용과 아키텍처 수준을 정당화하는 근거 문서다.

- **📢 섹션 요약 비유**: BIA는 환자의 생체 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 보고 수술 우선순위와 응급실 장비 수준을 정하는 과정과 같다. 위험도가 높을수록 더 빠른 의사 도착과 더 정교한 장비가 필요하다.

---

## Ⅲ. 비교 및 연결

BIA는 종종 위험 분석이나 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 혼동되지만 역할이 다르다. 위험 분석이 "무슨 사고가 발생할 수 있는가"를 본다면, BIA는 "사고가 실제로 발생했을 때 어느 업무가 얼마나 빨리 치명적인가"를 다룬다. [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원 수단이고, [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 훈련은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이지만, BIA는 이 둘의 목표 수준을 정하는 상위 기준이다.

| 구분 | 초점 | 주요 질문 | 대표 산출물 |
| :--- | :--- | :--- | :--- |
| 위험 분석 ([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Analysis) | 위협과 취약점 | 어떤 사고가 얼마나 발생 가능한가 | 위험도, 통제 대책 |
| BIA | 업무 중단 영향 | 멈추면 무엇이 먼저 치명적인가 | MTPD, [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위 |
| [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)/[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 설계 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 방식 | 어떤 방식으로 복원할 것인가 | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 주기, 보관 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 훈련 | 절차 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 실제로 목표 시간 안에 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능한가 | 훈련 결과, 개선 과제 |

BIA는 다른 엔터프라이즈 개념과도 강하게 연결된다. [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/)와 [CMDB](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/) ([Configuration Management Database](/knowledge-base/studynote/12_it_management/02_itsm_itil/091_cmdb/))는 의존성 파악의 기초 자료가 되고, [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))와 [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/))는 외부 고객 약속 수준을 정의한다. 클라우드 관점에서는 [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 구성, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 자동 페일오버 같은 기술 선택이 모두 BIA 결과를 충족하기 위한 수단으로 해석된다.

- **📢 섹션 요약 비유**: 위험 분석이 태풍 예보라면, BIA는 태풍이 왔을 때 전기·식수·통신 중 무엇이 먼저 끊기면 가장 큰 피해가 나는지 정하는 도시 생존 우선순위표와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 BIA를 시스템 단위가 아니라 업무 시나리오 단위로 수행해야 한다. 예를 들어 이커머스 기업에서 "주문"은 웹 화면 하나가 아니라 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 상품 조회, 장바구니, 결제 승인, 주문 DB, 물류 연계까지 묶인 흐름이다. 이 체인 중 하나라도 장시간 멈추면 매출 손실이 발생하므로, 개별 서버 상태만 보고 중요도를 판단하면 실제 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위가 왜곡된다.

기술사 관점의 판단 포인트는 다음과 같다. 첫째, RTO를 선언했으면 인력 대기체계, 전환 절차, 네트워크 경로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 방식이 모두 그 시간 안에 작동해야 한다. 둘째, RPO를 짧게 잡을수록 저장소·회선·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비용이 급격히 증가하므로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치가 정말 그 수준을 요구하는지 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다. 셋째, BIA는 정적 문서가 아니라 신규 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 출시, 법규 변경, 피크 거래량 증가 시 다시 갱신되어야 한다.

실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)로는 ① 시간 구간별 손실 증가 곡선을 정의했는가, ② 외부 결제망·물류사·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서버 같은 의존성이 반영되었는가, ③ [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위가 실제 [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 런북과 연결되는가, ④ 테스트 결과가 목표 수치와 맞는가를 반드시 본다. 반대로 모든 시스템에 동일한 [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) 1시간을 부여하거나, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 비용을 계산하지 않은 채 [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 0을 선언하는 것은 대표적인 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다.

- **📢 섹션 요약 비유**: BIA를 잘 쓰는 조직은 대피 훈련 때 누구를 어느 통로로 먼저 이동시킬지 이미 정해 둔 학교와 같고, 못 쓰는 조직은 비상벨이 울린 뒤에야 출구를 찾는 학교와 같다.

---

## Ⅴ. 기대효과 및 결론

BIA가 잘 정리되면 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 자원이 가장 중요한 업무에 집중된다. 그 결과 불필요한 과잉 투자 없이도 핵심 매출 흐름, 법적 준수, 고객 신뢰를 지킬 수 있고, 장애 발생 시 의사결정 속도도 빨라진다. 또한 경영진은 [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 예산을 감이 아니라 사업 영향 수치에 기반해 승인할 수 있어 투자 정당성이 높아진다.

다만 BIA는 한 번 작성해 두면 끝나는 문서가 아니다. 조직 구조, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 의존성, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가치, 거래량이 바뀌면 기존 수치는 빠르게 낡는다. 따라서 BIA는 "[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 문서"가 아니라 "업무 가치의 최신 지도"로 기억해야 하며, 정기 훈련과 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통해 계속 보정되어야 한다.

- **📢 섹션 요약 비유**: BIA는 비싼 보험 증권이 아니라, 폭풍이 올 때 어떤 문을 먼저 닫고 어떤 배를 먼저 묶어야 하는지 알려주는 항구 운영 지도와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| BCP (Business Continuity Planning) | BIA는 연속성 계획의 우선순위와 목표 시간을 정하는 출발점 |
| MTPD (Maximum Tolerable Period of Disruption) | 업무가 버틸 수 있는 최대 중단 한계로 [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) 상한선 판단 기준 |
| [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 시간으로 [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 절차와 인프라 수준을 결정 |
| [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)) | 허용 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 시점으로 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 규정 |
| [DR](/knowledge-base/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | BIA 결과를 실제 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계와 사이트 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 구현 |

### 📈 관련 키워드 및 발전 흐름도

```text
Asset inventory
        |
        v
Risk analysis
        |
        v
BIA (impact by time)
        |
        v
MTPD / RTO / RPO
        |
        v
DR tiering and recovery drill
```

이 흐름은 "자산 파악 -> 위험 인식 -> 업무 영향 분석 -> 목표 수치화 -> [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 체계 운영"으로 이어지는 엔터프라이즈 복원력 설계 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. BIA는 집에 정전이 왔을 때 냉장고, 조명, 게임기 중 무엇을 먼저 다시 켜야 하는지 정하는 종이예요.
2. 우유가 상하기 전에 냉장고를 켜야 하듯이, 회사도 빨리 살려야 하는 일이 따로 있어요.
3. 그래서 BIA는 "무엇을 먼저, 얼마나 빨리" 고쳐야 하는지 알려주는 순서표예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 212 / 482

<- **이전**: [211. 데스크톱 애널리틱스 (Desktop Analytics) / 작업 마이닝 (Task Mining)](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/211_desktop_analytics_task_mining_rpa_discovery/)
**다음**: [213. SWOT-AHP (Analytic Hierarchy Process) 다기준 의사결정 분석법을 통한 IT 전략 가중치 우선순위](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/213_swot_ahp_analytic_hierarchy_process_decision_making/) ->

---
