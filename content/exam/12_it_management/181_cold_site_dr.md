---
title: "Cold Site"
date: "2026-05-06"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 콜드 사이트 (Cold Site)는 [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)용 별도 장소에 전력·네트워크·냉각·랙 같은 기본 시설만 확보하고, 서버와 스토리지는 재해 발생 후 조달·설치하는 최저비용형 Disaster [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 방식이다.
> 2. **가치**: Hot Site나 Warm Site를 감당하기 어려운 조직도 최소한의 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 기반을 확보할 수 있어, 비핵심 시스템이나 장시간 중단이 허용되는 업무에 비용 효율적인 안전망이 된다.
> 3. **판단 포인트**: 콜드 사이트의 성패는 빈 공간 자체가 아니라 오프사이트 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 공급사 조달 계약, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차서, 복원 훈련이 준비되어 있는지에 달려 있으며, [Recovery](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) Time Objective가 길다는 한계를 반드시 수용해야 한다.

---

## Ⅰ. 개요 및 필요성

콜드 사이트는 "돈 대신 시간을 쓰는" [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 별도 장소를 확보해 두지만 그 안에 상시 가동 장비를 두지 않으므로 구축·운영 비용은 낮다. 반면 재해가 발생하면 하드웨어 조달, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설치, 애플리케이션 배치, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원까지 새로 해야 하므로 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이 길다.

이 방식이 필요한 이유는 모든 시스템이 [Hot Site](/studynote/12_it_management/05_security_compliance/179_hot_site_dr/) 수준의 연속성을 요구하지 않기 때문이다. 예를 들어 경영 보고, 기록 보존, 일부 내부 행정 시스템은 수분 내 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)보다 비용 절감이 우선일 수 있다. [Business Impact Analysis](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ([BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/))를 수행해 업무별 허용 중단 시간을 구분하면, 콜드 사이트는 낮은 우선순위 업무를 위한 현실적 선택지가 된다.

하지만 "빈 공간만 있으면 된다"고 오해하면 실패한다. 장비가 없어도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 남아 있어야 하고, 어디서 장비를 얼마나 빨리 조달할지 계약되어 있어야 하며, 누가 어떤 순서로 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할지 Runbook이 있어야 한다. 즉 콜드 사이트의 필요성은 단순한 공간 확보가 아니라, <strong>낮은 비용으로도 재해 후 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 가능성을 남겨 두는 것</strong>에 있다.

- **📢 섹션 요약 비유**: 콜드 사이트는 비상시 들어갈 수 있는 빈 사무실을 미리 계약해 두는 것과 같다. 월세는 싸지만, 책상과 컴퓨터를 채우고 다시 일하기까지는 시간이 걸린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

콜드 사이트의 핵심 원리는 시설은 미리 준비하고, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 외부에 안전하게 보관하며, 재해 시 필요한 장비와 소프트웨어를 단계적으로 올리는 것이다. 따라서 병목은 장비 성능이 아니라 조달 시간, 복원 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 설치 절차, 보안 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에 있다.

| 구성 요소 | 평상시 상태 | 재해 시 역할 |
| :--- | :--- | :--- |
| [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 시설 | 전력, 냉각, 네트워크, 랙만 준비 | 물리적 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 거점 제공 |
| 오프사이트 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | 테이프, 객체 스토리지, 불변 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 보관 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원의 출발점 |
| 공급사 조달 계약 | 서버·스토리지·네트워크 긴급 납품 조건 확보 | 장비 확보 시간 단축 |
| 표준 이미지 / [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) | [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 미들웨어, 보안 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 템플릿 | 설치 시간과 오류 감소 |
| Runbook | 선언, 조달, 설치, 복원, 절체 절차 문서화 | 사람 의존도 감소 |

아래 그림은 콜드 사이트에서 실제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이 어디에서 소비되는지 보여 준다.

```text
+----------------------------------------------------------------------+
| Cold site recovery chain                                            |
+----------------------------------------------------------------------+
| Primary site                                                        |
|   App / DB / Files                                                  |
|      | backup                                                       |
|      v                                                              |
| Off-site backup vault                                               |
|   tape / object storage / immutable copy                            |
|      |                                                              |
|      v                                                              |
| Cold site facility                                                  |
|   racks + power + cooling + network only                            |
|                                                                      |
| Disaster declared                                                   |
|   -> procure hardware                                               |
|   -> install OS / middleware                                        |
|   -> restore data                                                   |
|   -> validate security / DNS / VPN                                  |
|   -> resume service                                                 |
|                                                                      |
| Bottlenecks: supplier SLA / restore bandwidth / runbook quality     |
+----------------------------------------------------------------------+
```

이 구조에서 [Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/))는 마지막 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시점에 의해 결정되고, [Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/))는 조달·설치·복원 시간이 합쳐져 결정된다. 그래서 콜드 사이트는 같은 시설이라도 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 주기와 공급 계약 조건에 따라 품질이 크게 달라진다. 시설은 같아 보여도 준비 수준은 전혀 다를 수 있다.

또한 현대적 콜드 사이트는 물리 시설만 의미하지 않는다. 클라우드 객체 저장소와 이미지 템플릿, [Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/) ([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))를 조합하면 "클라우드 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)-복원형 콜드 사이트"를 만들 수 있다. 이 경우 하드웨어 운송 시간을 없애 RTO를 줄일 수 있지만, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 시간이 사라지는 것은 아니다.

- **📢 섹션 요약 비유**: 콜드 사이트는 빈 주방에 가스와 수도만 연결해 둔 상태와 같다. 요리를 시작하려면 냄비를 들여놓고 재료를 꺼내고 불을 켜는 준비 시간이 꼭 필요하다.

---

## Ⅲ. 비교 및 연결

콜드 사이트를 이해하려면 [Hot Site](/studynote/12_it_management/05_security_compliance/179_hot_site_dr/), [Warm Site](/studynote/12_it_management/05_security_compliance/180_warm_site_dr/), 클라우드 [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) & Restore 패턴과의 차이를 함께 봐야 한다. 특히 콜드 사이트는 "준비가 덜 된 [웜 사이트](/studynote/12_it_management/05_security_compliance/180_warm_site_dr/)"가 아니라, 애초에 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간을 비용으로 교환하는 다른 선택지다.

| 비교 축 | [Hot Site](/studynote/12_it_management/05_security_compliance/179_hot_site_dr/) | [Warm Site](/studynote/12_it_management/05_security_compliance/180_warm_site_dr/) | Cold Site | Cloud [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) & Restore |
| :--- | :--- | :--- | :--- | :--- |
| 인프라 준비 수준 | 거의 즉시 전환 가능 | 장비·기본 SW 준비 | 시설 중심, 장비 없음 | 코드와 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 중심 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최신성 | 실시간 또는 근실시간 | 주기 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) / 비동기 | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시점 기준 | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 시점 기준 |
| 일반적 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) | 수분~수시간 | 수시간~수일 | 수일~수주 | 수시간~수일 |
| 일반적 [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) | 거의 0~수분 | 수분~수시간 | 수시간~수일 | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 따름 |
| 비용 | 매우 높음 | 중간 | 낮음 | 사용량 기반으로 유연 |
| 적합한 업무 | 미션 크리티컬 | 중요 업무 | 비핵심 / 장시간 중단 허용 | 신규 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 대안으로 유력 |

콜드 사이트는 BCP (Business Continuity Plan)와도 연결된다. 시스템만 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해도 사람이 일할 장소, 인증서, 계정, 외부 회선, [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)이 준비되지 않으면 업무는 재개되지 않는다. 그래서 콜드 사이트 설계는 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 시설 설계이면서 동시에 업무 연속성 설계다.

또 보안 관점에서는 3-2-1 혹은 3-2-1-1-0 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 불변 저장소가 중요하다. [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 상황에서는 단순 오프사이트 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만으로 부족할 수 있기 때문이다. 콜드 사이트는 비용 중심 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이지만, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 무결성까지 약하면 사실상 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 수단이 없는 것과 같다.

- **📢 섹션 요약 비유**: Hot Site가 바로 입주 가능한 완성 아파트라면, Cold Site는 전기와 수도만 연결된 빈 집이고, 클라우드 [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) & Restore는 필요할 때 조립해 세우는 모듈형 집에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) 결과로 "이 시스템이 며칠 멈춰도 되는가"를 수치화해야 한다. 그 답이 72시간 이상이거나 더 길고, 비용 제약이 강하며, 규제상 최소 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 거점이 필요한 경우 콜드 사이트가 현실적이다. 반대로 매출, 안전, 대외 서비스에 직접 영향을 주는 핵심 시스템은 콜드 사이트만으로는 부족하다.

| 판단 질문 | 콜드 사이트 적합 시그널 | 보완 필요 사항 |
| :--- | :--- | :--- |
| 장시간 중단 허용 가능한가 | 예 | 장비 조달 시간과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 범위 문서화 |
| 예산 제약이 큰가 | 예 | 비용 절감 대신 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 지연을 수용해야 함 |
| 규제 또는 감사상 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 거점이 필요한가 | 예 | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 보관, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 증적, 훈련 기록 확보 |
| 신규 시스템인가 | 보통 | 물리 시설 대신 클라우드 대안을 함께 비교 |

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)본이 다른 지역에 보관되고, 실제 복원 테스트까지 통과했는가?
2. 서버·스토리지·네트워크 장비 긴급 조달 계약과 예상 납품 시간이 명시되어 있는가?
3. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 미들웨어, [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/), 인증서, [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) (Virtual Private Network), [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 절체 절차가 Runbook에 포함되어 있는가?
4. 라이선스 키, 계정 정보, 암호화 키 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 절차가 별도로 보관되어 있는가?
5. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 주센터로 되돌아오는 Failback 절차까지 정의되어 있는가?

### 자주 발생하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 있다고 믿지만 실제로 복원 테스트를 한 적이 없는 운영
- 빈 공간만 확보하고 공급사 계약, 표준 이미지, 네트워크 회선 준비가 없는 "명목상 콜드 사이트"
- 같은 지역에만 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 둬 광역 재해 시 함께 영향을 받는 구성
- [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/)를 고려하지 않고 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 가능한 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 보관하는 설계

기술사 답안에서는 <strong>"콜드 사이트는 최소 비용으로 <a href="/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/">DR</a> 거점을 확보하는 대신 긴 RTO를 감수하는 방식이며, 핵심 통제 포인트는 오프사이트 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a>, 조달 계약, Runbook, 정기 복원 훈련"</strong>이라고 정리하면 좋다.

- **📢 섹션 요약 비유**: 콜드 사이트 운영은 비상약 상자를 사 두는 것만으로 끝나지 않는다. 약이 아직 유효한지, 어디 있는지, 누가 어떻게 쓰는지까지 알아야 실제 위급할 때 도움이 된다.

---

## Ⅴ. 기대효과 및 결론

콜드 사이트의 장점은 분명하다. 운영비를 최소화하면서도 재해 후 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 거점을 확보할 수 있고, 비핵심 시스템에 과도한 투자를 하지 않게 해 준다. 조직 전체 관점에서는 모든 업무를 동일한 등급으로 보호하는 대신, 업무 중요도에 따라 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 차등화할 수 있게 된다.

그러나 콜드 사이트는 "싸지만 느린" 것만으로 기억하면 부족하다. 준비되지 않은 콜드 사이트는 실제 재해 시 아무 쓸모가 없고, 잘 준비된 콜드 사이트만이 비용 효율적인 DR이 된다. 결국 콜드 사이트의 품질은 공간이 아니라 <strong><a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 가능성을 증명하는 문서·계약·<a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a>·훈련</strong>으로 평가해야 한다.

결론적으로 콜드 사이트는 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 스펙트럼의 끝점에 있는 여전히 유효한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 다만 오늘날에는 클라우드 [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) & Restore, Pilot Light와 항상 비교해야 하며, 선택 후에는 "언제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할 수 있는가"를 실제 훈련으로 입증해야 한다.

- **📢 섹션 요약 비유**: 콜드 사이트는 비상시를 위한 빈 집 열쇠다. 열쇠만 있다고 바로 살 수 있는 것은 아니지만, 준비가 되어 있으면 완전히 길바닥에 나앉는 일은 막을 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [BIA](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ([Business Impact Analysis](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/)) | 어떤 업무가 콜드 사이트로 충분한지 판단하는 출발점이다. |
| [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) / [RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) | 콜드 사이트의 허용 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 범위를 정하는 핵심 지표다. |
| Off-site [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | 콜드 사이트에서 가장 중요한 자산은 장비보다도 외부 보관 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다. |
| Runbook | 사람 의존 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 절차화해 재해 시 혼란을 줄인다. |
| [Warm Site](/studynote/12_it_management/05_security_compliance/180_warm_site_dr/) / [Hot Site](/studynote/12_it_management/05_security_compliance/179_hot_site_dr/) | 비용과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도 관점에서 콜드 사이트와 비교되는 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) 대안이다. |
| [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) / [Immutable](/studynote/13_cloud_architecture/05_data_engineering/298_immutable/) [Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | 현대적 클라우드형 콜드 사이트 품질을 끌어올리는 수단이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Business Impact Analysis
    |
    v
RTO / RPO 등급화
    |
    +- 짧은 복구 필요 -> Hot / Warm Site
    +- 긴 복구 허용 -> Cold Site
    |
    v
Off-site backup + supplier contract + runbook
    |
    v
Restore drill and cloud backup-restore evolution
```

이 흐름은 콜드 사이트가 단독 기술이 아니라, 업무 영향 분석과 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 위에서 선택되는 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)임을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 콜드 사이트는 비가 오면 잠시 들어갈 수 있게 미리 빌려 둔 빈 집이에요.
2. 집 안에는 전기와 인터넷만 있고 침대나 책상은 없어서 나중에 가져와야 해요.
3. 그래서 돈은 적게 들지만, 다시 살 준비를 하는 데 시간이 오래 걸려요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 295 / 587

<- **이전**: [180. 웜 사이트 (Warm Site)](/studynote/12_it_management/05_security_compliance/180_warm_site_dr/)
**다음**: [182. 망분리 (Network Separation) 모델](/studynote/12_it_management/05_security_compliance/182_network_separation_model/) ->

---
