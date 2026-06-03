+++
title = "492. DAST (Dynamic Application Security Testing)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

DAST는 블랙박스 방식으로 웹 애플리케이션을 테스트하는 경우가 많다. 실제 요청과 응답을 보면서 취약점을 찾는다.

운영과 유사한 환경에서 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다는 점이 강점이다.

- **📢 섹션 요약 비유**: 문을 실제로 열고 닫아 보며 잠금 상태를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것이다.

---

다음은 [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Applic의 핵심 구조와 흐름을 보여주는 다이어그램이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DAST (Dynamic Applic</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력/요구사항</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">핵심 처리 과정</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">출력/결과물</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구 분석 설계·적용 품질 검증</div></div>
</div>
</div>



이 다이어그램은 [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Applic가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

DAST는 실행 중인 앱에 입력을 넣고 반응을 분석한다.

```text
공격 입력 -> 실행 중 앱 -> 응답/행위 분석
```

| 특징 | 의미 |
|:---|:---|
| 실행 기반 | 실제 동작 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 블랙박스 | 내부 코드 미확인 |
| 공격 재현 | 페이로드 활용 |

- **📢 섹션 요약 비유**: 제품을 포장만 보고 판단하지 않고 실제로 써 보는 것과 같다.

---

---

---

---

## Ⅲ. 비교 및 연결

DAST는 SAST가 놓칠 수 있는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 흐름, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 처리, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 문제를 잘 드러낸다.

| 구분 | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) | [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) |
|:---|:---|:---|
| 초점 | 런타임 | 정적 코드 |
| 장점 | 실제 반응 | 빠른 탐지 |
| 한계 | 환경 필요 | 동적 문제 미흡 |

둘을 함께 써야 분석 범위가 넓어진다.

- **📢 섹션 요약 비유**: 지도와 현장 답사는 서로 다른 정보를 준다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 배포 전 스테이징 환경이나 정기 보안 점검에서 활용한다.

검토 포인트는 다음과 같다.
1. [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 필요한 기능을 제대로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는가?
2. 오류 기반 정보 노출을 찾는가?
3. 실제 서비스와 비슷한 환경을 준비하는가?

- **📢 섹션 요약 비유**: 새 신발은 집에서만이 아니라 밖에서도 걸어 봐야 편한지 안다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

DAST는 운영 관점의 보안 결함을 발견하는 데 강하다.

결론적으로 이 항목은 "실행 중 앱 보안 검사"다.

- **📢 섹션 요약 비유**: 문이 닫히는지만이 아니라, 바람에도 안 열리는지 보는 검사다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">소프트웨어 위기 (Software Crisis) 인식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DAST (Dynamic Application Security Testing) 개념 정립</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">표준화 및 방법론 체계화 (ISO, CMMI, Agile)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">클라우드 네이티브·AI 기반 확장 적용</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">지속적 개선 및 DevOps·MLOps 통합</div>
</div>
</div>



이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) (Dynamic Application [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Testing)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 575 / 973

← **이전**: [491. SAST (Static Application Security Testing) - 소스코드 정적 분석 도구 (보안 룰셋 기반)](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)
**다음**: [492. DAST (Dynamic Application Security Testing) - 런타임 환경에 공격 페이로드 주입 분석 (블랙박스)](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) →

---
