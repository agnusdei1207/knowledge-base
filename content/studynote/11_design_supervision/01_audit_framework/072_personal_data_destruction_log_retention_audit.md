+++
title = "72. 개인정보 파기 정책 및 로그 보존 기간 감리 (법적 요건)"
date = 2026-04-10

[taxonomies]
tags = ["studynote-design"]

[extra]
tags = ["studynote-design"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 파기와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 보존은 법적 요구를 동시에 만족시켜야 한다.
> 2. **가치**: 보존 기간과 파기 절차를 명확히 하면 분쟁과 과징금 리스크를 줄인다.
> 3. **판단**: 파기와 보존은 서로 반대가 아니라 각기 다른 법적 책임이다.

---

## Ⅰ. 개요 및 필요성

[개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)는 무조건 오래 들고 있으면 안 된다. 하지만 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 필요한 기간 보관해야 한다.

그래서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 분리가 중요하다.

- **📢 섹션 요약 비유**: 쓰레기는 버리고, 영수증은 잠시 보관하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Data Lifecycle</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Retention Policy</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Destruction / Archiving</div>
</div>
</div>



| 항목 | 의미 |
| :-- | :-- |
| [Retention](/knowledge-base/studynote/05_database/04_transactions_concurrency/515_mvcc/) | 보존 기간 |
| Destruction | 파기 |
| Evidence | 증적 |

[개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)는 목적 달성 후 파기해야 하고, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 법적 기간 동안 보관해야 할 수 있다.

- **📢 섹션 요약 비유**: 필요한 종이는 잠시 보관하고, 쓸모없는 종이는 버린다.

---

## Ⅲ. 비교 및 연결

| 대상 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 차이 |
| :-- | :-- | :-- |
| [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) | 파기 우선 | 최소 보관 |
| [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | 보존 필요 | 증적 유지 |

| 관리 | 의미 |
| :-- | :-- |
| [Audit Trail](/knowledge-base/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/) | 추적 가능 |
| [Retention](/knowledge-base/studynote/05_database/04_transactions_concurrency/515_mvcc/) Schedule | 보존 주기 |

[개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 파기와 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 보존은 각각의 법적 근거를 확인해야 한다.

- **📢 섹션 요약 비유**: 버릴 것과 남길 것을 따로 정해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 파기 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있는가?
2. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 보존 기간이 정의되었는가?
3. 법적 근거가 분리되어 있는가?
4. 파기 증적이 남는가?
5. [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적이 가능한가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 무조건 오래 보관하는 설계
- [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)를 동일 취급하는 설계
- 파기 증적이 없는 설계
- 법적 근거를 확인하지 않는 설계

기술사 관점에서는 이 이슈를 "법적 요건 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생명주기 관리"로 설명해야 한다.

- **📢 섹션 요약 비유**: 버릴 것은 버리고, 남길 것은 증거로 둔다.

---

## Ⅴ. 기대효과 및 결론

파기와 보존 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 분리하면 법적 리스크가 줄고 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응이 쉬워진다.

결론적으로 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)는 적시에 파기하고, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 법정 기간 보존해야 한다.

- **📢 섹션 요약 비유**: 쓰레기통과 서랍장을 구분하는 것이다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Retention Policy</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Destruction</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Audit Trail</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Compliance</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Data Lifecycle</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Retention</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Destruction</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Compliance Audit</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

버릴 건 버려요.  
남길 건 잠깐 남겨요.  
이 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 그런 약속이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 111 / 530

← **이전**: [71. 소스코드 난독화 적용 여부 점검 - 금융/모바일 앱 보안](/knowledge-base/studynote/11_design_supervision/01_audit_framework/071_source_code_obfuscation_audit/)
**다음**: [73. 서버/OS/DB 패치 및 취약점 스캐닝 감리](/knowledge-base/studynote/11_design_supervision/01_audit_framework/073_server_os_db_patch_vulnerability_scan/) →

---
