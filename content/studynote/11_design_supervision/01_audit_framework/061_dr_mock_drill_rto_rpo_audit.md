---
title: "Dr Mock Drill Rto Rpo Audit"
date: "2026-04-10"
tags:
  - "studynote-design-supervision"
weight: 61
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) (Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) 모의 훈련은 장애가 실제로 났을 때 대체 센터가 정말 살아나는지 확인하는 실전 검증이다.
> 2. **가치**: BCP (Business Continuity Plan)와 DRP (Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) Plan)가 문서로만 존재하는지, 현장에서 실제로 돌아가는지 점검한다.
> 3. **판단**: [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))와 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))를 숫자로 측정해야 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 품질을 말할 수 있다.

---

## Ⅰ. 개요 및 필요성

[재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)는 "백업이 있다"는 말만으로 끝나지 않는다. 실제 화재, [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/), 전원 장애가 발생했을 때 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 얼마나 빨리, 얼마나 적게 잃고 돌아오는지가 중요하다.

그래서 모의 훈련([Mock](/studynote/04_software_engineering/11_testing_validation/854_mock_test_double/) Drill)을 통해 주 센터와 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 센터 간 전환 절차를 실제로 시험한다. 감리의 목적은 서류가 아니라 실행력을 확인하는 데 있다.

- **📢 섹션 요약 비유**: 구명정이 있다고 믿는 것과, 진짜 바다에서 타 보게 하는 것은 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
주 센터
  +- 운영 DB
  +- 애플리케이션
  +- 서비스 트래픽
        v Failover
DR 센터
  +- 복제 DB
  +- 대기 시스템
  +- 복구 절차
```

| 용어 | 의미 |
| :-- | :-- |
| BCP (Business Continuity Plan) | 업무 연속성 계획 |
| DRP (Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) Plan) | [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) 절차 |
| [Failover](/studynote/04_software_engineering/05_devops_ci_cd/300_failover_architecture/) | 주 센터에서 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 센터로 전환 |
| Failback | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 원래 센터로 복귀 |
| [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)까지 허용되는 시간 |
| [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) | 허용 가능한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 시점 |

모의 훈련은 전원을 뽑는 수준까지 가지 않더라도, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 전환, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 메시지 큐, 외부 연동까지 실제로 이어져야 의미가 있다.

- **📢 섹션 요약 비유**: 비상문 위치만 외우는 게 아니라, 실제로 문을 열고 나가 보는 훈련이다.

---

## Ⅲ. 비교 및 연결

| [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 형태 | 비용 | [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) | [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) |
| :-- | :-- | :-- | :-- |
| [Hot Site](/studynote/12_it_management/05_security_compliance/179_hot_site_dr/) | 높음 | 매우 짧음 | 매우 짧음 |
| [Warm Site](/studynote/12_it_management/05_security_compliance/180_warm_site_dr/) | 중간 | 짧음 | 짧음 |
| [Cold Site](/studynote/12_it_management/05_security_compliance/181_cold_site_dr/) | 낮음 | 김 | 김 |

Hot Site는 거의 실시간 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 대기 자원을 두어 빠르지만 비싸다. Cold Site는 저렴하지만 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에 오래 걸린다. 그래서 실제 설계는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중요도에 맞춰 타협한다.

- **📢 섹션 요약 비유**: 예비 열쇠를 바로 손에 쥐고 있는지, 창고 어딘가에 묻어 두었는지의 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 훈련 시 실제 Failover가 이루어졌는가?
2. RTO와 RPO가 숫자로 측정되었는가?
3. 외부 연동과 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 절차까지 점검했는가?
4. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 Failback 절차도 검증했는가?
5. 보고서보다 증적 로그와 타임라인이 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 문서 검토만 하고 실제 전환은 하지 않는 훈련
- DB만 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하고 앱/[인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/연계를 빼먹는 설계
- [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 됐는데 원복(Failback)이 안 되는 설계
- [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/[RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) 목표를 정하지 않고 "빠르게"만 말하는 설계

기술사 관점에서는 DR의 성패를 "[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 계획이 있다"가 아니라 "정해진 시간과 손실 한도 안에 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)되는가"로 판단해야 한다.

- **📢 섹션 요약 비유**: 연습 경기에서 이기는 게 아니라, 진짜 경기에서 몇 분 안에 재정비할 수 있는지가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 모의 훈련은 장애 대응 체계를 현실화한다. 덕분에 조직은 위기 상황에서 더 빠르게 움직이고, 운영 리스크를 수치로 다룰 수 있다.

결국 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 감리는 백업의 존재 여부가 아니라, 장애가 났을 때 다시 살아나는 힘을 검증하는 일이다.

- **📢 섹션 요약 비유**: 연습장에서 넘어져도, 실제 경기장에서 다시 일어나는 방법을 확인하는 것이다.

---

## 관련 개념 맵

```text
BCP / DRP
   v
Failover
   v
RTO / RPO
   v
Failback
   v
Service Continuity
```

---

## 관련 키워드 및 발전 흐름도

```text
백업
   v
DR 센터
   v
모의 훈련
   v
RTO / RPO 검증
   v
지속적 복구 체계
```

---

## 어린이를 위한 3줄 비유 설명

불이 났을 때 다른 교실로 바로 옮겨 가는 연습이에요.
얼마나 빨리 옮기고, 얼마나 덜 잃는지 숫자로 확인해요.
그래야 진짜 사고 때도 당황하지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 92 / 530

<- **이전**: [60. 공공데이터 개방 (Open Data) 표준 규격 및 감리](/studynote/11_design_supervision/01_audit_framework/060_open_data_public_api_standards/)
**다음**: [62. 백업 및 아카이빙 정책 점검 (Backup and Archiving Policy Audit)](/studynote/11_design_supervision/01_audit_framework/062_backup_archiving_policy/) ->

---
