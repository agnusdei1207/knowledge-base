---
title: "887. SCA (Software Composition Analysis)"
date: "2026-05-08"
tags:
  - "studynote-software-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Composition Analysis)은(는) [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

현대 애플리케이션은 수많은 외부 라이브러리에 의존한다. 그래서 SCA는 보안과 법무를 동시에 돕는다.

취약 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 지원 종료, 라이선스 충돌을 찾는 데 유용하다.

- **📢 섹션 요약 비유**: 냉장고 속 재료뿐 아니라 유통기한과 원산지도 같이 보는 것이다.

---

다음은 [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Compos의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  SCA (Software Compos                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Compos가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

SCA는 의존성 트리를 분석해 위험을 찾는다.

```text
앱 -> 직접 의존성 -> 하위 의존성 -> 취약점/라이선스 탐지
```

| 항목 | 의미 |
|:---|:---|
| [Direct](/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) Dependency | 직접 사용 패키지 |
| Transitive Dependency | 간접 의존성 |
| License | 사용 조건 |

- **📢 섹션 요약 비유**: 겉으로 보이는 재료뿐 아니라 양념 속 재료까지 확인하는 것과 같다.

---

---

---

---

## Ⅲ. 비교 및 연결

SCA는 SAST와 달리 코드 문법보다 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 구성을 본다.

| 구분 | [SCA](/studynote/09_security/05_web_app_security/453_sca/) | [SAST](/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) |
|:---|:---|:---|
| 대상 | 의존성 | 소스코드 |
| 초점 | [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) | 구현 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) |
| 출력 | 취약/라이선스 | 보안 약점 |

[SBOM](/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))과 함께 쓰면 더 좋다.

- **📢 섹션 요약 비유**: 레시피만 보는 것이 아니라, 구매 목록까지 확인하는 것과 같다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) ([Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/))에 붙여 자동 검사한다.

점검 포인트는 다음과 같다.
1. 취약 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 배포에 포함되는가?
2. 간접 의존성까지 추적하는가?
3. 라이선스 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반을 막는가?

- **📢 섹션 요약 비유**: 선물 상자 속에 무엇이 들어 있는지 끝까지 확인해야 한다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

SCA는 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 리스크를 줄이고 배포 품질을 높인다.

결론적으로 이 항목은 "의존성의 보안 및 라이선스 점검"이다.

- **📢 섹션 요약 비유**: 남의 부품을 빌릴 때도 사용 설명서를 읽어야 한다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Composition Analysis)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Composition Analysis)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Composition Analysis) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Composition Analysis)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
SCA (Software Composition Analysis) 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [SCA](/studynote/09_security/05_web_app_security/453_sca/) (Software Composition Analysis)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 581 / 973

<- **이전**: [494. RASP (Runtime Application Self-Protection) - 실행 환경 내부에서 공격 실시간 방어](/studynote/04_software_engineering/08_security_compliance_devsecops/494_rasp_runtime_protection/)
**다음**: [495. SCA (Software Composition Analysis) - 오픈소스 라이브러리 취약점 및 라이선스 스캔](/studynote/04_software_engineering/11_testing_validation/887_sca_software_composition_analysis/) ->

---
