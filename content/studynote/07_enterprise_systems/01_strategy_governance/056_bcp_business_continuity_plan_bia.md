---
title: "056. Bcp Business Continuity Plan Bia"
tags:
  - "enterprise_systems"
date: "2026-06-07"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BCP (Business Continuity Plan)는 재난이 와도 핵심 업무를 멈추지 않게 만드는 전사 생존 계획이다.
> 2. **가치**: 사람, 장소, 절차, 시스템을 함께 보지 않으면 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))만으로는 회사를 지킬 수 없다.
> 3. **판단 포인트**: [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ([Business Impact Analysis](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/))와 [RA](/studynote/09_security/03_network_security/161_ra_registration_authority/) ([Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Assessment)로 우선순위를 정하고, [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))와 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))를 기준으로 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 짠다.

---

## Ⅰ. 개요 및 필요성

BCP는 "서버를 되살리는 문서"가 아니다. 재난이 발생했을 때 사람, 업무, 장소, [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/), 시스템을 함께 움직여 회사의 생존을 이어 가는 운영 계획이다.

과거에는 전산실이 멈추면 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 복원하는 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 중심 사고가 많았다. 그러나 대형 재난은 직원 출근 불가, 통신망 장애, 대체 사무실 부재까지 동시에 만든다. 그래서 전사 관점의 연속성 계획이 필요하다.

- **📢 섹션 요약 비유**: BCP는 집이 흔들릴 때 벽 하나만 고치는 게 아니라, 가족이 어디로 모이고 무엇부터 챙길지 정해 두는 비상 계획이다.

---

## Ⅱ. BIA와 RA로 우선순위를 정하는 방법

비상 계획의 출발점은 "무엇이 가장 중요한가"를 가르는 일이다. 이를 위해 BIA와 RA를 먼저 수행한다.

```text
재난/장애 발생
    v
BIA (Business Impact Analysis)
    v
RA (Risk Assessment)
    v
RTO / RPO 설정
    v
복구 전략과 자원 배치
```

- [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ([Business Impact Analysis](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/))는 업무별 피해 규모와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위를 정한다.
- [RA](/studynote/09_security/03_network_security/161_ra_registration_authority/) ([Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Assessment)는 화재, 홍수, [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 같은 위협의 발생 가능성과 영향을 본다.
- [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))는 "얼마나 빨리 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해야 하는가"를 뜻하고, [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))는 "얼마나 많은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실까지 허용하는가"를 뜻한다.

- **📢 섹션 요약 비유**: 먼저 "누가 제일 급한 환자인지"를 정해야 응급차가 순서를 잘 잡을 수 있다.

---

## Ⅲ. BCP의 주요 구성 요소

BCP는 한 장짜리 선언이 아니라 여러 실행 항목의 묶음이다.

1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 대응 및 대피</strong>: 인명 안전 확보, 비상 연락망, 출입 통제, 대피 경로 안내.
2. **위기 관리 및 소통**: 고객, 임직원, 주주, 언론에 같은 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 빠르게 전달.
3. **대체 사업장 가동**: 본사 마비 시 대체 사무실, 원격근무, 대체 좌석 확보.
4. <strong>IT <a href="/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a></strong>: 핵심 시스템 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 복원, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재가동.
5. <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">공급망</a> 연속성</strong>: 주요 협력사, 결제, 물류, 외주 운영의 대체 경로 준비.

- **📢 섹션 요약 비유**: BCP는 비상구, 구급상자, 대체 열쇠, 가족 연락망을 한 번에 챙겨 둔 집안 매뉴얼이다.

---

## Ⅳ. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 대체 수단

[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 "무엇을 어디까지 살릴 것인가"를 정하는 일이다. 모든 시스템을 똑같이 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할 수는 없으므로, 핵심 업무 중심으로 자원을 배분한다.

- <strong><a href="/studynote/12_it_management/05_security_compliance/179_hot_site_dr/">Hot site</a></strong>: 거의 즉시 전환 가능한 대체 센터
- <strong><a href="/studynote/12_it_management/05_security_compliance/180_warm_site_dr/">Warm site</a></strong>: 일부 준비가 되어 있어 단시간 내 전환 가능한 센터
- <strong><a href="/studynote/12_it_management/05_security_compliance/181_cold_site_dr/">Cold site</a></strong>: 기본 시설만 갖춘 저비용 대체 장소

사람과 절차도 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 대상이다. 핵심 인력이 없으면 서버가 살아도 업무는 멈춘다. 그래서 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 인력, 업무 인수인계, 수동 처리 절차가 함께 있어야 한다.

- **📢 섹션 요약 비유**: 자동차만 예비 바퀴로 바꿔서는 못 달린다. 운전자와 도로, 기름까지 같이 준비해야 한다.

---

## Ⅴ. 훈련, 점검, 개선 기준

BCP는 작성보다 운영이 더 중요하다. 계획은 시간이 지나면 연락처가 바뀌고 시스템이 바뀌어 금방 낡는다.

실무에서는 다음을 반복 점검한다.

- [Tabletop Exercise](/studynote/09_security/13_secops_ir_forensics/660_tabletop_exercise/) (모의 상황 회의)로 대응 순서를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
- [Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) Drill (전환 훈련)로 시스템 전환이 실제로 되는지 본다.
- 연락망, 협력사, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 장소, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 우선순위를 주기적으로 갱신한다.
- 훈련 결과를 반영해 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/RPO와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차를 다시 조정한다.

- **📢 섹션 요약 비유**: 비상계획은 서랍 속 종이가 아니라, 주기적으로 열어 보고 손보는 살아 있는 지도다.

---

## 관련 개념 맵

```text
재난/재해
   v
BIA + RA
   v
RTO / RPO
   v
인력 / 장소 / 시스템 / 공급망 대응
   v
훈련 / 점검 / 개선
```

---

## 관련 키워드 및 발전 흐름도

1. 과거의 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 중심 사고 -> 서버 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에만 초점
2. 9.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) 테러와 대형 재난 경험 -> 사람과 업무 연속성의 중요성 부각
3. BIA와 [RA](/studynote/09_security/03_network_security/161_ra_registration_authority/) 체계화 -> 핵심 업무 우선순위화
4. RTO와 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 기반 설계 -> [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표를 수치로 관리
5. 훈련과 복원력(resilience) 중심 운영 -> 전사 연속성으로 확장

---

## 어린이를 위한 3줄 비유 설명

BCP는 집에 불이 나도 가족이 어디서 만나고 무엇부터 챙길지 정해 둔 약속이에요.
서버만 살리는 것이 아니라 사람, 장소, 일하는 순서도 같이 살려야 해요.
그래서 미리 연습해 두면 진짜 위기 때 덜 당황해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 56 / 482

<- **이전**: [55. 릴리스와 배포 관리 (Release and Deployment Management)](/studynote/07_enterprise_systems/01_strategy_governance/055_release_and_deployment_management/)
**다음**: [57. 재해 복구 (Disaster Recovery, DR) - BIA와 RTO/RPO 설계](/studynote/07_enterprise_systems/01_strategy_governance/057_disaster_recovery_dr_rto_rpo/) ->

---
