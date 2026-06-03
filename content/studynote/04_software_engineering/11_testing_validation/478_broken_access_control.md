+++
title = "478. Broken Access Control (취약한 접근 제어)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) ([취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/))은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

접근 제어 ([Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/))는 자원과 기능을 누구에게 허용할지 정하는 장치다. 이게 깨지면 다른 사람의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조회, 수정, 삭제가 가능해진다.

웹 서비스에서 가장 치명적인 문제 중 하나라서 우선적으로 점검한다.

- **📢 섹션 요약 비유**: 아파트 출입문은 열려 있어도, 자기 층만 들어가야 하는 것과 같다.

---

다음은 Broken Access Contro의 핵심 구조와 흐름을 보여주는 다이어그램이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Broken Access Contro</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력/요구사항</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">핵심 처리 과정</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">출력/결과물</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구 분석 설계·적용 품질 검증</div></div>
</div>
</div>



이 다이어그램은 Broken Access Contro가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/))과 [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))를 분리해서 생각하는 것이다.

```text
사용자 로그인 -> 인증 성공 -> 권한 검사 -> 자원 접근 허용/거부
```

| 구분 | 의미 |
|:---|:---|
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | 누구인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) | 무엇을 할 수 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) | [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 로직 실패 |

객체 ID를 바꾸는 직접 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) ([IDOR](/knowledge-base/studynote/09_security/05_web_app_security/418_idor/), Insecure [Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) Object [Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))도 흔한 예다.

- **📢 섹션 요약 비유**: 이름표를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 뒤에도, 그 사람이 들어갈 방이 맞는지 또 봐야 한다.

---

---

---

---

## Ⅲ. 비교 및 연결

Broken Access Control은 "로그인만 하면 된다"는 오해에서 자주 생긴다.

| 구분 | 정상 설계 | 취약한 설계 |
|:---|:---|:---|
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 위치 | 서버 측 | 클라이언트 의존 |
| 기준 | 자원 단위 권한 | 단순 로그인 여부 |
| 결과 | 접근 차단 | 수평/수직 [권한 상승](/knowledge-base/studynote/09_security/04_endpoint_security/356_privilege_escalation/) |

OWASP Top 10에서 반복적으로 강조되는 이유도 여기에 있다.

- **📢 섹션 요약 비유**: 입장권이 있다고 공연장 어디든 갈 수 있는 것은 아니다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 모든 민감 API와 관리 기능에 서버 측 권한 검사를 넣어야 한다.

검토 포인트는 다음과 같다.
1. 요청마다 권한을 다시 검사하는가?
2. 객체 소유권을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는가?
3. 관리자 기능이 일반 사용자에게 노출되지 않는가?

- **📢 섹션 요약 비유**: 문 앞에서 신분증만 보고 끝내지 말고, 그 사람이 들어올 방까지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

Broken Access Control을 막으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출과 기능 오용을 크게 줄일 수 있다.

결론적으로 이 항목은 "권한 검사가 빠진 상태"를 뜻한다.

- **📢 섹션 요약 비유**: 자물쇠가 있어도 열쇠 주인을 잘못 정하면 아무 소용이 없다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) ([취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/))의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) ([취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/))은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) ([취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/)) 적용 결과는 QA 활동을 통해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) ([취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/))에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">소프트웨어 위기 (Software Crisis) 인식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Broken Access Control (취약한 접근 제어) 개념 정립</div>
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

1. [Broken Access Control](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) ([취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/))은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 547 / 973

← **이전**: [477. OWASP Top 10 (2021)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/477_owasp_top_10_2021/)
**다음**: [478. Broken Access Control (취약한 접근 제어)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/478_broken_access_control/) →

---
