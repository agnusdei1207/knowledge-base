+++
title = "520. 공급망 (Supply Chain) 공격 사례 및 서명된 커밋(Signed Commit), CI 파이프라인 보호"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공격 사례 및 서명된 커밋(Signed Commit), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 공격은 저장소, 의존성, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인을 타고 들어온다. 그래서 개발 흐름 전체를 신뢰할 수 있게 만들어야 한다.

한 번 오염되면 배포까지 그대로 퍼질 수 있다.

- **📢 섹션 요약 비유**: 재료가 들어오는 문이 오염되면 주방 전체가 위험해진다.

---

다음은 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  공급망 (Supply Chain) 공                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 코드와 빌드 체인에 증거를 남기는 것이다.

```text
개발자 -> Signed Commit -> CI 검증 -> 빌드/배포
```

| 요소 | 의미 |
|:---|:---|
| Signed Commit | 작성자 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | 파이프라인 안전화 |
| Provenance | 출처 추적 |

- **📢 섹션 요약 비유**: 택배 상자에 봉인 스티커와 발송 기록을 함께 붙이는 것이다.

---

---

---

---

## Ⅲ. 비교 및 연결

[공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 공격은 직접 해킹보다 더 은밀할 수 있다.

| 구분 | 안전한 방식 | 위험한 방식 |
|:---|:---|:---|
| 커밋 | 서명됨 | 미서명 |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)됨 | 임의 실행 |
| 의존성 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)됨 | 무검증 |

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/), [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/), [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 관리와 함께 봐야 한다.

- **📢 섹션 요약 비유**: 주방 재료, 도마, 칼까지 모두 점검해야 안전하다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 브랜치 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 승인 리뷰, [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 차단, 빌드 격리가 중요하다.

점검 포인트는 다음과 같다.
1. 서명되지 않은 변경이 섞이지 않는가?
2. CI가 외부 기여 코드를 안전하게 처리하는가?
3. 빌드 산출물의 출처가 추적되는가?

- **📢 섹션 요약 비유**: 문만 닫는 게 아니라, 누가 열었는지 기록해야 한다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

[공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)는 개발 신뢰를 지키는 첫 관문이다.

결론적으로 이 항목은 "코드 유입 경로의 신뢰 보장"이다.

- **📢 섹션 요약 비유**: 집으로 들어오는 모든 문에 방명록이 있어야 한다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공격 사례 및 서명된 커밋(Signed Commit), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공격 사례 및 서명된 커밋(Signed Commit), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공격 사례 및 서명된 커밋(Signed Commit), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 적용 결과는 QA 활동을 통해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공격 사례 및 서명된 커밋(Signed Commit), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
공급망 (Supply Chain) 공격 사례 및 서명된 커밋(Signed Commit), CI 파이프라인 보호 개념 정립
    │
    ▼
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    │
    ▼
클라우드 네이티브·AI 기반 확장 적용
    │
    ▼
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) ([Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)) 공격 사례 및 서명된 커밋(Signed Commit), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 632 / 973

← **이전**: [520. 공급망 (Supply Chain) 공격 사례 및 서명된 커밋(Signed Commit), CI 파이프라인 보호](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)
**다음**: [521. 인공지능 모델 공격 방어](/knowledge-base/studynote/04_software_engineering/11_testing_validation/521_ai_model_attack_defense/) →

---
