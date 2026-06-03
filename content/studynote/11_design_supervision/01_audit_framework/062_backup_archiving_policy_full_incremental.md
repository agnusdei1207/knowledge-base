+++
title = "62. 백업 및 아카이빙 정책 - Full/Incremental/Differential 점검"
date = 2026-04-10

[taxonomies]
tags = ["studynote-design"]

[extra]
tags = ["studynote-design"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)용 복제본을 만드는 일이고, 아카이빙은 장기 보존용 데이터를 저비용 매체로 옮기는 일이다.
> 2. **구조**: Full, Incremental, Differential [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간과 저장 비용 사이의 균형이 다르다.
> 3. **판단**: [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 [RTO](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/) ([Recovery Time Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/176_rto_recovery_time_objective/)), [RPO](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/) ([Recovery Point Objective](/knowledge-base/studynote/12_it_management/05_security_compliance/177_rpo_recovery_point_objective/)), 보존 기간, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 테스트로 검증돼야 한다.

---

## Ⅰ. 개요 및 필요성

랜섬웨어나 하드웨어 장애가 나면 "[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 있다"는 말만으로는 아무 의미가 없다. 실제로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)할 수 있어야 한다.

그래서 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 단순 보관이 아니라 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 성능과 보존 규정까지 함께 보는 운영 체계다.

- **📢 섹션 요약 비유**: 비상식량이 있는지보다, 실제로 먹을 수 있게 보관됐는지가 더 중요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
데이터
  ├─ Full Backup
  ├─ Incremental Backup
  └─ Differential Backup
        ↓
복구 / 보존 / 아카이빙
```

| 유형 | 특징 |
| :-- | :-- |
| Full | 전체를 매번 복사, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 빠름 |
| Incremental | 마지막 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 이후 변경분만 복사 |
| Differential | 마지막 Full 이후 변경분 누적 복사 |
| Archiving | 장기 보존용 저비용 저장 |

Full은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 쉽고, Incremental은 저장이 효율적이며, Differential은 그 중간이다. 아카이빙은 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)보다 장기 보존이 목적이라는 점이 다르다.

- **📢 섹션 요약 비유**: 전체 복사는 책 전체를 다시 찍는 것, 증분은 바뀐 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 메모, 차등은 이번 주 바뀐 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음이다.

---

## Ⅲ. 비교 및 연결

| 방식 | 장점 | 단점 |
| :-- | :-- | :-- |
| Full | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 단순 | 시간/용량 큼 |
| Incremental | 저장 효율 최고 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 순서 복잡 |
| Differential | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 비교적 간단 | 증분보다 용량 큼 |
| Archiving | 장기 보존에 적합 | 즉시 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)용 아님 |

```text
백업 = 복구
아카이빙 = 보존
```

[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 아카이빙을 혼동하면 비용이 커지고, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)는 느려진다. 목적이 다른데 같은 저장소에 다 넣는 것이 가장 위험하다.

- **📢 섹션 요약 비유**: 지금 바로 다시 써야 할 공책과, 박물관에 남길 자료를 같은 상자에 넣는 실수다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 테스트를 정기적으로 하는가?
2. RTO와 RPO에 맞는 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 유형을 선택했는가?
3. 오프사이트 또는 에어갭(Air Gap) 보관이 있는가?
4. 보존 기간과 파기 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있는가?
5. 암호화와 접근 통제가 적용되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 하고 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 테스트를 안 하는 설계
- [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 아카이빙을 같은 의미로 쓰는 설계
- [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)본을 온라인에만 두는 설계
- [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 없이 Full만 과도하게 쌓는 설계

기술사 관점에서는 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 "저장 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)"이 아니라 "[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)"으로 봐야 한다. [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능한 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)만 진짜 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이다.

- **📢 섹션 요약 비유**: 열쇠를 어디에 뒀는지 아는 것보다, 막상 잠겼을 때 문이 열리는지가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 사고 대비의 기본이고, 아카이빙은 장기 보존의 효율화다. 둘을 분리해 설계해야 비용과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)성을 동시에 잡을 수 있다.

결국 좋은 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 "얼마나 많이 저장하느냐"보다 "얼마나 빨리, 얼마나 안전하게 되살리느냐"로 평가된다.

- **📢 섹션 요약 비유**: 비상 창고와 박물관 창고는 용도가 다르다.

---

## 관련 개념 맵

```text
Backup
   ↓
Full / Incremental / Differential
   ↓
Restore Test
   ↓
Archiving
   ↓
Retention Policy
```

---

## 관련 키워드 및 발전 흐름도

```text
데이터 복제
   ↓
백업 정책
   ↓
복구 테스트
   ↓
아카이빙
```

---

## 어린이를 위한 3줄 비유 설명

[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)은 다시 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 위한 복사본이에요.  
아카이빙은 오래 보관할 자료를 따로 두는 거예요.  
둘은 목적이 달라서 구분해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 94 / 530

← **이전**: [62. 백업 및 아카이빙 정책 점검 (Backup and Archiving Policy Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/062_backup_archiving_policy/)
**다음**: [63. 소프트웨어 라이선스 컴플라이언스 (Software License Compliance)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/063_software_license_compliance/) →

---
