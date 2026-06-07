---
title: "Cloud Tiering"
date: "2026-05-08"
tags:
  - "studynote-enterprise-systems"
weight: 201
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 티어링 (Cloud Tiering)은 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 접근 빈도와 보존 기간에 따라 서로 다른 저장 계층으로 자동 이동시키는 수명주기 기반 스토리지 최적화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 최근 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 빠른 계층에, 장기 보관용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 저렴한 객체 스토리지나 아카이브 계층에 두어 총소유비용 ([TCO](/studynote/12_it_management/01_governance_strategy/016_tco/), Total Cost of Ownership)과 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 증설 부담을 크게 낮춘다.
> 3. **판단 포인트**: 성공의 핵심은 단순 저장비 절감이 아니라, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 목표 ([RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), [Recovery Time Objective](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)), [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시점 목표 ([RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/), [Recovery Point Objective](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)), 불변성, 반출 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 함께 고려한 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 설계에 있다.

---

## Ⅰ. 개요 및 필요성

클라우드 티어링은 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 종류의 스토리지에만 두지 않고, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 계층과 장기 보관 계층으로 나누어 관리하는 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 아키텍처다. 최근 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능성이 높으므로 빠른 디스크나 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 스토리지에 두고, 오래된 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 저렴한 객체 스토리지나 아카이브로 이동시킨다. 이렇게 해야 급증하는 보존 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 때문에 고가 장비를 무한정 증설하는 비효율을 줄일 수 있다.

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증가 속도는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증가보다 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 더 가파르게 나타나는 경우가 많다. 운영 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체는 수십 테라바이트 (TB, Terabyte)여도, 일일 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 주간 전체 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 장기 보관본이 누적되면 수 배 이상으로 커진다. 이 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 동일한 고성능 스토리지에 보관하면, 실제로는 거의 읽지 않는 장기 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 때문에 비용과 전력, 공간이 과도하게 낭비된다.

따라서 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 설계에서 중요한 것은 "어디에 저장할까"만이 아니라 "언제 어느 계층으로 내릴까"다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)보다 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능성과 보존 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 핵심이므로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 온도와 규제 요구를 반영한 계층화가 필수다.

- **📢 섹션 요약 비유**: 클라우드 티어링은 자주 꺼내는 옷은 옷장 앞칸에 두고, 계절 지난 옷은 창고 박스로 옮기는 정리법과 같다. 모든 옷을 비싼 드레스룸 맨 앞에 둘 필요는 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전형적인 구조는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 티어, 용량 티어, 아카이브 티어, 그리고 이를 움직이는 정보 수명주기 관리 (ILM, Information [Lifecycle Management](/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle/)) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진으로 구성된다. [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 소프트웨어는 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점, 마지막 접근 시점, 보존 등급, 불변 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 기준으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어느 계층에 둘지 결정한다. [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 요청이 오면 필요 시 아카이브에서 다시 불러오는 리콜 ([Recall](/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)) 과정이 수행된다.

| 계층 | 대표 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) | 용도 | 설계 포인트 |
| :-- | :-- | :-- | :-- |
| [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 티어 | 고체 상태 드라이브 ([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [Solid State Drive](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)), 네트워크 결합 스토리지 ([NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/), [Network Attached Storage](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)) | 최근 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 즉시 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 짧은 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/), 빠른 랜덤 접근 |
| 용량 티어 | [하드 디스크 드라이브](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) ([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/), Hard Disk Drive), 객체 스토리지 | 중기 보관, 일반 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 비용 효율, 확장성 |
| 아카이브 티어 | Glacier, Tape | 장기 보관, 규제 대응 | 저비용, 높은 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진 | ILM, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 소프트웨어 | 이동·보존·삭제 자동화 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/), [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)성 |
| 불변 계층 | 객체 잠금 (Object [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)), [WORM](/studynote/02_operating_system/10_security/590_worm/) ([Write Once Read Many](/studynote/01_computer_architecture/15_advanced_topics/693_worm_storage/)) | [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 방어 | 삭제 금지, 보존 기간 준수 |

아래 그림은 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 시간이 지나며 더 저렴한 계층으로 이동하고, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시에는 다시 리콜되는 구조를 보여준다.

```text
+----------------------------------------------------------------------------+
|                         Backup data lifecycle tiering                     |
+----------------------------------------------------------------------------+
| Backup Job -> Performance Tier -> Capacity Tier -> Archive Tier          |
|                (SSD / NAS)        (Object / HDD)     (Glacier / Tape)    |
|                     +---------- ILM / retention policy ----------+        |
|                                      |                                     |
|                                      v                                     |
|                         Recall for restore / immutable copy                |
+----------------------------------------------------------------------------+
```

핵심 원리는 자동 이동 자체보다 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)에 있다. 예를 들어 30일 이내 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)에 유지하고, 30일 이후는 객체 스토리지로 이동하며, 1년 이후는 딥 아카이브 (Deep Archive)로 내리는 식의 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 대표적이다. 여기에 객체 잠금 (Object [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))과 [WORM](/studynote/02_operating_system/10_security/590_worm/) ([Write Once Read Many](/studynote/01_computer_architecture/15_advanced_topics/693_worm_storage/))을 결합하면, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 복사본이 삭제·변조되지 않는 불변 저장소 역할도 수행할 수 있다.

- **📢 섹션 요약 비유**: 클라우드 티어링은 냉장고, 창고, 장기 보관 창고를 나눠 쓰는 살림과 같다. 오늘 먹을 음식과 3년 뒤 꺼낼 비상식량을 같은 자리에 둘 필요는 없다.

---

## Ⅲ. 비교 및 연결

클라우드 티어링은 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), 아카이브와 비슷해 보이지만 목적이 다르다. [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)은 빠른 시점 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에 초점이 있고, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 장애·삭제·재해에 대비한 독립 복사본에 가깝다. 아카이브는 장기 보관과 규제 대응에 초점이 있으며, 티어링은 이들 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비용과 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 요구에 맞춰 적절한 계층에 배치하는 운영 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

| 구분 | [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) + 티어링 | 아카이브 |
| :-- | :-- | :-- | :-- |
| 주 목적 | 빠른 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능성 + 비용 최적화 | 장기 보존 |
| 저장 위치 | 원본과 가까운 스토리지 | 다계층 스토리지 | 저비용 장기 저장소 |
| [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도 | 매우 빠름 | 계층에 따라 다름 | 느림 |
| 대표 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | 원본 장애 전파 가능 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 오류 시 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 즉시 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 어려움 |

또한 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 티어링과 클라우드 티어링도 구분해야 한다. 전자는 내부 스토리지 계층만 바꾸는 반면, 후자는 클라우드 객체 스토리지를 활용해 사실상 무한 확장과 지역 외부 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)를 얻는다. 대신 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 반출 비용, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이라는 새로운 판단 요소가 추가된다.

- **📢 섹션 요약 비유**: [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)이 책상 위 복사본이라면, [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 금고 속 사본이고, 아카이브는 지하 문서 보관소다. 티어링은 이 문서들을 언제 어디로 옮길지 정하는 보관 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중요도와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 빈도를 등급화해 티어 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 나누는 것이 출발점이다. 운영 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 잦은 가상 머신 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 빠른 티어에 더 오래 남겨 두고, 법정 보관용 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 조기에 저비용 티어로 이동시키는 식이다. 또한 [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 대응을 위해 최소 한 계층은 삭제 불가 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 별도 계정, 별도 리전에 두는 것이 안전하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 등급별 [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)·RPO가 정의되어 있는가?
2. 티어 이동 이후 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 반출 비용을 사업이 감당할 수 있는가?
3. 불변성 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 보존 기간이 규제 요구와 일치하는가?
4. 리콜 테스트와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 훈련을 정기적으로 수행하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 저장비만 보고 장기 보관 티어로 빠르게 내린 뒤, 실제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간이 업무 기준을 초과하는 설계
- [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 장애 대비 없이 같은 계정, 같은 리전에만 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 두는 설계
- 티어링 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 자동화했지만, 실제 리스토어 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 하지 않아 종이상 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 존재하는 상태

기술사 답안에서는 비용 절감뿐 아니라 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)을 함께 언급해야 한다. 특히 "티어링 = 아카이브"로 단순화하지 말고, 운영 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 구간과 장기 보존 구간을 분리해 설명하면 경계가 명확해진다.

- **📢 섹션 요약 비유**: 값싼 창고를 빌리는 것만으로 좋은 이사가 되는 것은 아니다. 급히 꺼내야 할 짐이 있다면, 가장 싼 창고보다 꺼내기 쉬운 위치를 함께 따져야 한다.

---

## Ⅴ. 기대효과 및 결론

클라우드 티어링을 적절히 설계하면 고가 스토리지 증설을 줄이고, 장기 보관 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)의 운영 비용을 크게 낮출 수 있다. 동시에 객체 잠금과 외부 리전 보관을 활용하면 [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)와 [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 대응력도 강화된다. 즉 티어링은 단순 저장 기술이 아니라 비용, [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 보안을 함께 최적화하는 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 운영 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

물론 지나친 저비용 최적화는 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 실패로 되돌아올 수 있다. 실제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 필요한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 과도하게 깊은 아카이브로 보내거나, 테스트 없는 자동 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 의존하면 위기 시 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 쓸모없어질 수 있다. 따라서 이 개념은 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 온도와 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 요구에 맞춰 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a>의 거주지를 설계하는 것</strong>으로 기억하는 편이 가장 정확하다.

- **📢 섹션 요약 비유**: 클라우드 티어링은 모든 짐을 가장 싼 창고에 넣는 기술이 아니라, 자주 쓰는 짐과 거의 안 쓰는 짐의 자리를 다르게 배치해 집과 창고를 함께 효율적으로 쓰는 방법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| ILM (Information [Lifecycle Management](/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle/)) | [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 이동·보존·삭제 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 자동화 |
| [RTO](/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)/[RPO](/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) | 계층 선택 시 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 속도와 허용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실을 결정 |
| 객체 잠금 (Object [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) | 클라우드 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)의 불변성을 보장하는 기능 |
| [WORM](/studynote/02_operating_system/10_security/590_worm/) ([Write Once Read Many](/studynote/01_computer_architecture/15_advanced_topics/693_worm_storage/)) | 삭제·변조를 막아 [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 방어력을 높이는 저장 방식 |
| 딥 아카이브 (Deep Archive) | 최저 비용 대신 높은 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 감수하는 장기 보관 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 고가 스토리지 백업
    |
    v
성능 티어 + 용량 티어 분리
    |
    v
객체 스토리지 활용
    |
    v
아카이브 · 불변 백업 결합
    |
    v
정책 기반 클라우드 티어링 백업 아키텍처
```

이 흐름은 단순 보관에서, 비용·[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·보안을 함께 최적화하는 계층형 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 진화한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 자주 쓰는 장난감은 방 안 가까운 상자에 두고, 잘 안 쓰는 장난감은 창고에 넣어 두는 것과 같아요.
2. 클라우드 티어링은 컴퓨터가 알아서 어떤 상자에 넣을지 정해 주는 정리 방법이에요.
3. 그래서 방은 덜 복잡해지고, 필요할 때는 다시 꺼내 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 201 / 482

<- **이전**: [200. 로우코드 / 노코드 (LC/NC) 기반 엔터프라이즈 워크플로우 자동화](/studynote/07_enterprise_systems/03_eai_esb_msa/200_low_code_no_code_enterprise_workflow_automation/)
**다음**: [202. BPM 라이프사이클 (Business Process Management Lifecycle)](/studynote/07_enterprise_systems/04_process_consulting/202_bpm_lifecycle_design_execution_monitoring_optimization/) ->

---
