+++
title = "496. SBOM (Software Bill of Materials) 포맷"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 포맷은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

SBOM은 제품에 어떤 라이브러리와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 포함됐는지 기록한다. [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 보안의 기본 자료다.

SPDX (Software Package [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Exchange)와 CycloneDX가 대표 포맷이다.

- **📢 섹션 요약 비유**: 도시락 반찬표가 있어야 뭐가 들어 있는지 바로 알 수 있다.

---

다음은 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software Bill 의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  SBOM (Software Bill                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software Bill 가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

SBOM은 구성 요소, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 해시, 라이선스 정보를 담는다.

```text
제품 -> 컴포넌트 목록 -> 버전/출처/라이선스
```

| 포맷 | 특징 |
|:---|:---|
| SPDX | 라이선스 표현에 강함 |
| CycloneDX | 보안/[공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 정보에 강함 |
| 공통 | 구성 추적 |

- **📢 섹션 요약 비유**: 식재료표에 원산지와 유통기한을 같이 적는 것이다.

---

---

---

---

## Ⅲ. 비교 및 연결

SBOM은 SCA의 입력이자 결과물이 될 수 있다.

| 구분 | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) | [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) |
|:---|:---|:---|
| 역할 | 목록 | 분석 |
| 방향 | 기록 | 검사 |
| 활용 | 추적성 | 위험 탐지 |

둘을 함께 써야 의존성 관리가 체계적이다.

- **📢 섹션 요약 비유**: 물건 목록이 있어야 검수도 빨라진다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 배포 전, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응, 취약점 공지 대응에 SBOM을 만든다.

점검 포인트는 다음과 같다.
1. [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 정확한가?
2. 간접 의존성까지 담겼는가?
3. 정기적으로 갱신되는가?

- **📢 섹션 요약 비유**: 이사할 때 박스 안 물건 목록을 적어두면 찾기 쉽다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

SBOM은 제품의 투명성과 추적성을 높인다.

결론적으로 이 항목은 "소프트웨어 구성 명세서 포맷"이다.

- **📢 섹션 요약 비유**: 설계도와 부품표가 있어야 나중에 고치기 쉽다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 포맷의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 포맷은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 포맷 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 포맷에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
SBOM (Software Bill of Materials) 포맷 개념 정립
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

1. [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 포맷은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 584 / 973

← **이전**: [496. SBOM (Software Bill of Materials) 포맷 - SPDX, CycloneDX](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/496_sbom_format_spdx_cyclonedx/)
**다음**: [497. 행정안전부/KISA 소프트웨어 개발 보안 가이드 (47개 보안 약점)](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/497_kisa_secure_coding_guide/) →

---
