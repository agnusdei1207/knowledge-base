+++
title = "64. 접근 통제 및 권한 관리 (RBAC) - 권한 오남용 감사"
date = 2026-04-10

[taxonomies]
tags = ["studynote-design"]

[extra]
tags = ["studynote-design"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)([Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/))는 사용자에게 직접 권한을 주는 대신 역할(Role)에 권한을 묶어 관리하는 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 방식이다.
> 2. **가치**: 역할 기반으로 권한을 묶으면 최소 권한 원칙과 [직무 분리](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/)(SoD, [Separation of Duties](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/))를 쉽게 적용할 수 있다.
> 3. **판단**: [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)는 권한이 "있느냐"보다 "과도하지 않느냐"를 봐야 하며, [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 매트릭스가 핵심 증적이 된다.

---

## Ⅰ. 개요 및 필요성

권한 관리는 시스템 보안의 기본이다. 권한이 너무 많으면 사고가 커지고, 너무 적으면 업무가 막힌다.

RBAC는 역할을 기준으로 권한을 묶어, 사람의 변동이 있어도 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 유지하기 쉽게 만든다.

- **📢 섹션 요약 비유**: 열쇠를 사람마다 따로 주지 않고, 사무실 역할별로 묶어 두는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
User
  ↓
Role
  ↓
Permission
  ↓
Object / Resource
```

| 구성 요소 | 역할 |
| :-- | :-- |
| User | 실제 사용자 |
| Role | 업무 단위의 역할 |
| Permission | 수행 가능한 행위 |
| Object | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상 자원 |

[접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 매트릭스는 "누가 어떤 자원에 어떤 권한을 갖는지"를 표로 나타낸다. RBAC는 이 표를 역할 중심으로 정리해 관리 부담을 줄인다.

- **📢 섹션 요약 비유**: 사람 이름이 아니라 직책별로 문 열쇠를 묶어 두는 회사 사물함과 같다.

---

## Ⅲ. 비교 및 연결

| 모델 | 기준 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| DAC | 소유자 중심 | 유연함 | 통제가 약함 |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) | 보안 등급 중심 | 강한 통제 | 경직됨 |
| [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) | 역할 중심 | 관리 쉬움 | 역할이 많아지면 복잡 |
| [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 중심 | 정교함 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡도 높음 |

RBAC는 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)에서 특히 유용하다. 역할이 명확하면 누가 어떤 권한을 가져야 하는지 빠르게 검토할 수 있기 때문이다.

- **📢 섹션 요약 비유**: 반장, 부반장, 청소 당번처럼 역할이 정해져 있으면 할 일이 덜 헷갈린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 역할이 업무 기준으로 잘 분리되어 있는가?
2. 최소 권한 원칙이 적용되는가?
3. [직무 분리](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/)(SoD) 위반이 없는가?
4. 권한 부여와 회수 절차가 있는가?
5. 로그와 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 증적이 남는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 개인별로 예외 권한을 무한히 주는 설계
- 역할 수가 너무 많아 관리가 깨지는 설계
- [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 없이 권한만 계속 늘리는 설계
- 권한 회수 절차가 없는 설계

기술사 관점에서는 RBAC를 "권한 테이블"이 아니라 "조직 운영 구조"로 봐야 한다. 역할 설계가 곧 보안 설계다.

- **📢 섹션 요약 비유**: 열쇠를 아무에게나 주지 말고, 맡은 일에 맞게 나눠야 한다.

---

## Ⅴ. 기대효과 및 결론

RBAC는 권한 관리를 단순화하고, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)와 운영의 예측 가능성을 높인다. 그래서 엔터프라이즈 시스템의 기본 패턴으로 널리 쓰인다.

결론적으로 RBAC는 역할을 통해 권한 오남용을 줄이는 실용적 통제 방식이다.

- **📢 섹션 요약 비유**: 일할 사람과 열쇠를 맞춰 주면 관리가 훨씬 쉬워진다.

---

## 관련 개념 맵

```text
Access Control Matrix
  ↓
Role
  ↓
RBAC
  ↓
Audit Evidence
```

---

## 관련 키워드 및 발전 흐름도

```text
DAC / MAC
  ↓
RBAC
  ↓
ABAC
  ↓
Zero Trust
```

---

## 어린이를 위한 3줄 비유 설명

문 열쇠를 사람마다 따로 주면 복잡해요.  
역할별로 열쇠를 나누면 쉬워져요.  
RBAC는 그런 역할별 열쇠 관리예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 97 / 530

← **이전**: [63. 소프트웨어 라이선스 컴플라이언스 (Software License Compliance)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/063_software_license_compliance_gpl_mit/)
**다음**: [64. 접근 통제 및 권한 관리 감리 (Access Control and RBAC Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/064_access_control_rbac_audit/) →

---
