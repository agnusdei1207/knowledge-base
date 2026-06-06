---
title: "057. Disaster Recovery Dr Rto Rpo"
tags:
  - "enterprise_systems"
date: "2026-06-07"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)([DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/))는 재난 이후 IT [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 얼마나 빨리, 얼마나 적게 잃고 되살릴지 정하는 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ([Business Impact Analysis](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/))로 중요한 업무를 찾고, [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))와 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))로 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 수준을 수치화한다.
> 3. **판단 포인트**: [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표에 따라 Mirror, Hot, Warm, Cold site를 선택하고, 정기적인 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 훈련으로 실제 작동 여부를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 한다.

---

## Ⅰ. 개요 및 필요성

DR은 BCP (Business Continuity Plan)의 일부이지만, 특히 정보시스템과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에 초점을 맞춘다. 서버가 멈추고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 날아간 뒤 어떻게 살아날지를 정하는 일이다.

[백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 있다고 끝나지 않는다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 복원할 장소, 복원 시간, 복원 순서까지 준비해야 진짜 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 된다.

- **📢 섹션 요약 비유**: DR은 불이 난 뒤 어디서 다시 가게를 열지 정해 두는 비상 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 지도다.

---

## Ⅱ. BIA와 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/[RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)

[DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 설계의 출발점은 [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ([Business Impact Analysis](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/))다. 어떤 업무가 먼저 살아야 하는지 정해야 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 순서가 정해진다.

```text
BIA
  v
핵심 업무 선정
  v
RTO / RPO 설정
  v
복구 사이트와 백업 전략 결정
```

- <strong><a href="/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/">RTO</a></strong>는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다시 켜져야 하는 최대 시간이다.
- <strong><a href="/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/">RPO</a></strong>는 허용 가능한 최대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 시점이다.

이 두 값이 작을수록 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 비용은 급격히 올라간다.

- **📢 섹션 요약 비유**: 병원에서 "몇 시간 안에 수술해야 하는지"와 "얼마나 피를 잃어도 되는지"를 먼저 정하는 것과 같다.

---

## Ⅲ. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 센터의 유형

[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표에 따라 사이트 수준이 달라진다.

- <strong><a href="/studynote/12_it_management/05_security_compliance/178_mirror_site/">Mirror Site</a></strong>: 거의 실시간으로 주 센터와 동일하게 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)한다.
- <strong><a href="/studynote/12_it_management/05_security_compliance/179_hot_site_dr/">Hot Site</a></strong>: 즉시 전환이 가능한 대기 센터다.
- <strong><a href="/studynote/12_it_management/05_security_compliance/180_warm_site_dr/">Warm Site</a></strong>: 일부만 준비되어 있어 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에 시간이 더 걸린다.
- <strong><a href="/studynote/12_it_management/05_security_compliance/181_cold_site_dr/">Cold Site</a></strong>: 기본 공간만 준비된 저비용 방식이다.

[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표가 엄격할수록 비용이 커지지만, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 위험은 줄어든다.

- **📢 섹션 요약 비유**: 예비 차를 완전히 시동 걸어 둔 상태로 둘지, 꺼 둔 채로 둘지는 돈과 급함의 차이다.

---

## Ⅳ. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차와 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

DR은 계획보다 실행과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 중요하다.

- [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 구분한다.
- Failover와 Failback 절차를 정한다.
- [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
- 정기적으로 복원 테스트를 수행한다.

[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시나리오가 문서에만 있고 실제로 안 돌아가면 의미가 없다. 그래서 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 훈련은 필수다.

- **📢 섹션 요약 비유**: 운동회 전 연습을 해 보지 않으면, 진짜 달리기에서 넘어지기 쉽다.

---

## Ⅴ. 실무 설계와 BCP 비교

DR은 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 같은 말이 아니다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장하는 행위이고, DR은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체를 다시 살리는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

실무에서는 다음을 함께 본다.

- 핵심 업무별 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위
- [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/RPO에 맞는 사이트 선택
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 주기
- [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차
- BCP 전체 문서와의 연계

이 기준이 맞아야 재난이 와도 핵심 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 버틸 수 있다.

- **📢 섹션 요약 비유**: 물통만 준비하는 것과, 물통을 어디에 두고 누가 들고 갈지도 정해 두는 것은 다르다.

---

## 관련 개념 맵

```text
BIA
   v
RTO / RPO
   v
Mirror / Hot / Warm / Cold site
   v
복구 훈련 / 검증
```

---

## 관련 키워드 및 발전 흐름도

1. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 중심 사고 -> [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장에만 초점
2. [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) 도입 -> 핵심 업무 우선순위화
3. [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/[RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 수치화 -> [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표 정량화
4. 사이트 계층화 -> 비용과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도의 균형
5. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 훈련과 자동화 -> DR의 실전 운용 강화

---

## 어린이를 위한 3줄 비유 설명

[재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)는 가게가 무너지면 어디서 다시 열지 정하는 거예요.
언제까지 다시 열어야 하는지, 얼마나 잃어도 되는지도 미리 정해요.
그래야 진짜 위기 때 덜 당황해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 57 / 482

<- **이전**: [56. 비즈니스 연속성 계획 (BCP, Business Continuity Plan) - 재난/재해 시 핵심 업무 기능 유지 지침](/studynote/07_enterprise_systems/01_strategy_governance/056_bcp_business_continuity_plan_bia/)
**다음**: [58. IT 컴플라이언스 (Compliance) - SOX, Basel, GDPR, ISMS](/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/) ->

---
