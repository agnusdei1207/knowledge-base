+++
title = "58. IT 컴플라이언스 (Compliance) - SOX, Basel, GDPR, ISMS"
date = 2026-04-07

[taxonomies]
tags = ["studynote-enterprise"]

[extra]
tags = ["studynote-enterprise"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 컴플라이언스는 법과 규제를 IT 시스템과 절차로 실제 준수하고 증명하는 일이다.
> 2. **가치**: 벌금, 소송, 신뢰 하락을 막기 위해 보안과 거버넌스를 시스템에 내재화해야 한다.
> 3. **판단 포인트**: SOX, [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/), Basel, [ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/) 같은 규제가 요구하는 통제와 증거를 명확히 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

기업의 핵심 업무가 모두 시스템 위에서 돌아가는 시대에는, 규정을 어기는 순간 사업 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)가 바로 된다.

컴플라이언스는 단순한 문서 작업이 아니라, 실제 시스템이 규칙을 지키도록 만드는 운영 체계다.

- **📢 섹션 요약 비유**: 교통 법규를 지키는 것과, 차에 속도 제한 장치를 달아 두는 것은 다르다.

---

## Ⅱ. 주요 규제와 기준

실무에서 자주 만나는 규제는 서로 성격이 다르다.

- **SOX (Sarbanes-Oxley Act)**: 회계 투명성과 내부 통제
- <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a> (General <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">Protection</a> Regulation)</strong>: [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)와 처리 책임
- **Basel**: 금융 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)와 자본 적정성
- <strong><a href="/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/">ISMS</a></strong>: 정보보호 관리체계
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/">PCI</a> DSS (Payment Card Industry <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a> Standard)</strong>: 결제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안

규제는 다르지만 공통적으로 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 접근통제, 암호화, 책임 추적을 요구한다.

- **📢 섹션 요약 비유**: 서로 다른 나라의 시험이지만, 결국 노트 정리와 답안 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 필요하다.

---

## Ⅲ. 기술적 통제와 거버넌스

컴플라이언스는 시스템에 들어가야 의미가 있다.

- 접근 권한 분리
- 암호화
- [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 보존
- [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)
- 승인 흐름

이런 통제가 있어야 "지켰다"는 말이 아니라 "증명할 수 있다"가 된다.

- **📢 섹션 요약 비유**: 문을 잠그는 것뿐 아니라, 누가 언제 들어왔는지 기록도 남겨야 한다.

---

## Ⅳ. 증거와 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)

[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)에서는 실제 화면, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 승인 기록이 중요하다.

컴플라이언스는 선언이 아니라 증거로 완성된다. 그래서 증거를 남기기 쉬운 구조를 처음부터 설계해야 한다.

- **📢 섹션 요약 비유**: "봤다"고 말하는 것보다, 사진과 메모를 함께 남기는 것이 더 강하다.

---

## Ⅴ. 운영 자동화와 주의점

요즘은 Compliance-[as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-Code처럼 규정을 코드와 검사 도구로 자동화하려는 흐름이 강하다.

하지만 자동화가 있더라도 사람이 책임을 져야 한다. 규제를 체크박스로만 보고 실제 위험을 놓치면 안 된다.

- **📢 섹션 요약 비유**: 체온계가 있어도 아이를 직접 보는 부모가 필요한 것과 같다.

---

## 관련 개념 맵

```text
법/규제
   ↓
기술적 통제
   ↓
증거 / 감사
   ↓
컴플라이언스 운영
```

---

## 관련 키워드 및 발전 흐름도

1. SOX → 회계 통제 강화
2. [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) → [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 강화
3. Basel → 금융 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 규율
4. [ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/) / [PCI](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) DSS → 정보보호와 결제 보안
5. Compliance-[as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)-[Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) → 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 지속 운영

---

## 어린이를 위한 3줄 비유 설명

IT 컴플라이언스는 규칙을 지키게 하는 안전벨트예요.
기록과 잠금 장치가 있어야 나중에 "잘 지켰다"라고 말할 수 있어요.
그래서 시스템 안에 규칙을 넣어 두는 게 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 482

← **이전**: [57. 재해 복구 (Disaster Recovery, DR) - BIA와 RTO/RPO 설계](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/057_disaster_recovery_dr_rto_rpo/)
**다음**: [59. 정보기술 아웃소싱 (ITO, IT Outsourcing) / BPO (비즈니스 프로세스 아웃소싱)](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/059_it_outsourcing_ito_bpo/) →

---
