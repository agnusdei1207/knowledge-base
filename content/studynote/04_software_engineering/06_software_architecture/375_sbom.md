+++
title = "375. SBOM (Software Bill of Materials) - 소프트웨어 구성 요소 명세서 의무화 동향"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) - 소프트웨어 구성 요소 명세서 의무화 동향은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: SBOM은 전통적 제조업의 [BOM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/) ([Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))에서 유래했다. 자동차 제조사가 차량에 사용되는 모든 부품(本土生産、国外導入)을 목록화하여管理するように, 소프트웨어에서도 모든 구성 요소([라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), 프레임워크, SDK 등)를 목록화하여管理해야 한다. 이를 통해 구성 요소의 출처, 라이선스, 보안 취약점 등을 투명하게 파악할 수 있다.

- **필요성**: 현대 소프트웨어는 평균적으로 代码의 70~80%가 [서드파티](/knowledge-base/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 구성 요소로 이루어져 있다. 그러나 이러한 구성 요소에 대해"무엇이 포함되어 있고, 어디서 왔으며, 어떤 취약점이 있는가?"라는 질문에即座에 답할 수 있는 기업은 매우 드물다. SBOM은 이러한"알파지"를 해소하고, 보안 사고 시 신속한 대응을 가능하게 한다.

- **💡 비유**: SBOM은 **'음식물 원재료 이력 관리 시스템'**과 같다.盒便当当製作者가 사용하는 모든 材料(鸡蛋, 밥, 고등어 등)의 원산지([OSS](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 출처), 유통 경로([버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)), 유효 기간(지원 기간)을全都記載하여管理한다.万一 食品中毒 사고(보안 사고)가 발생하면, 即座에 문제가 된 材料를 추적하여迅速하게市場 회수하고환자를 치료할 수 있다.

- **등장 배경 및 발전 과정**:
  1. **2000년대 초**: 금융권에서 운용risk 관리를 위해 소프트웨어 구성 요소 목록化管理 시도
  2. **2018년**: NTIA (National Telecommunications and Information Administration)에서 SBOM의 최소 요소 정의
  3. **2021년**: 미국 대통령 행정 명령에 따라 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 의무화, 글로벌 확산
  4. **현재**: SPDX (ISO/IEC 5962), CycloneDX 등 표준화된 [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) 포맷 확산

- **📢 섹션 요약 비유**: SBOM은 **'여권으로 보는 입국 기록'**과 같다. 여권에는過去에 방문한 국가들의 입出境 기록이记载되듯이, SBOM에는ソフトウェアが過去に組み合わせたOSS/[라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)들의情報が記載된다. 이를 통해万一 문제 국가(취약한 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))를 방문(사용)했는지 여부를即座에 확인할 수 있다.

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

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) - 소프트웨어 구성 요소 명세서 의무화 동향의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))의 핵심 원리는 **복잡성 분해**, **역할 분리**, **품질 측정**의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/)) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
SBOM (Software Bill of Materials) 개념 정립
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

1. [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/124_bom_bill_of_materials/))은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 375 / 973

← **이전**: [374. 공급망 보안 (Supply Chain Security) - 오픈소스 취약점 관리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/374_supply_chain_security/)
**다음**: [376. 소프트웨어 빌드 및 배포 자동화의 품질 검증 단계](/knowledge-base/studynote/04_software_engineering/06_software_architecture/376_build_deployment_automation/) →

---
