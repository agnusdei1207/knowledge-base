+++
title = "25. 작업 추적 매트릭스 (Task Traceability Matrix) — 요구사항 추적 가능성 보장"
date = 2026-04-29

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 추적 매트릭스([Traceability](/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/) Matrix)는 요구사항(Requirements)부터 설계, 구현, 테스트까지 각 산출물 간의 연관 관계를 매핑한 표로, "이 요구사항이 어느 코드에 구현됐고 어느 [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/)로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)됐는가?"를 추적하는 관리 도구다.
> 2. **가치**: [요구사항 추적 매트릭스](/knowledge-base/studynote/04_software_engineering/03_design_architecture/157_requirements_traceability_matrix_rtm/)([RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/), [Requirements Traceability Matrix](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/))는 모든 요구사항이 누락 없이 구현됐는지 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고(순방향 추적), 모든 [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/)가 특정 요구사항을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하여 불필요한 테스트를 제거한다(역방향 추적).
> 3. **판단 포인트**: ISO/IEC 25010, DO-178C, [CMMI](/knowledge-base/studynote/12_it_management/04_sdlc_testing/133_cmmi_capability_maturity_model_integration_levels/) Level 3 이상에서 요구사항 추적 가능성([Traceability](/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/))은 필수 요건이다. 추적 매트릭스는 범위 변경([Scope Creep](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/)) 탐지, 영향 분석(Impact Analysis), [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 증적 제공의 세 가지 핵심 가치를 동시에 제공한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발 과정에서 처음 수집한 요구사항이 최종 제품에 모두 구현되었는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하지 못하면, 납품 시점에 "기능 누락"이나 "테스트 안 된 기능"이 발견되어 프로젝트가 실패할 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">추적 매트릭스 방향성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">순방향 추적 (Forward): 요구사항 → 설계 → 구현 → 테스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"이 요구사항이 어디에 구현됐고 어떻게 검증되나?"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">역방향 추적 (Backward): 테스트 → 구현 → 설계 → 요구사항</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"이 테스트가 검증하는 요구사항은 무엇인가?"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">양방향 추적 = 완전성(Completeness) + 일관성(Consistency)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 추적 매트릭스는 집 건축의 시공 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)다. 설계도(요구사항)의 각 항목이 실제로 지어졌는지(구현), 준공 검사를 통과했는지(테스트)를 하나씩 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) ([Requirements Traceability Matrix](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)) 예시



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구사항</div><div class="kb-diagram-cell">설계 문서</div><div class="kb-diagram-cell">소스코드</div><div class="kb-diagram-cell">테스트 케이스</div><div class="kb-diagram-cell">상태</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-001</div><div class="kb-diagram-cell">DS-01</div><div class="kb-diagram-cell">auth.py:45</div><div class="kb-diagram-cell">TC-001</div><div class="kb-diagram-cell">완료</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-002</div><div class="kb-diagram-cell">DS-02</div><div class="kb-diagram-cell">user.py:12</div><div class="kb-diagram-cell">TC-002</div><div class="kb-diagram-cell">완료</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-003</div><div class="kb-diagram-cell">DS-03</div><div class="kb-diagram-cell">-</div><div class="kb-diagram-cell">-</div><div class="kb-diagram-cell">미구현</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-004</div><div class="kb-diagram-cell">DS-01</div><div class="kb-diagram-cell">pay.py:78</div><div class="kb-diagram-cell">TC-003,004</div><div class="kb-diagram-cell">완료</div></div>
<div class="kb-diagram-note">REQ-003: 미구현 → 즉시 팀 공유 및 일정 조정 필요</div>
</div>
</div>



### JIRA + Confluence 기반 자동화 [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">JIRA Ticket (요구사항)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Pull Request (구현)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">테스트 케이스</div></div>
<div class="kb-diagram-note">RTM 자동 생성</div>
<div class="kb-diagram-note">(Traceability Plugin)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 자동화 RTM은 Amazon 주문 추적처럼, "내 주문(요구사항)이 창고 출고(구현)됐고 배송(테스트) 중인지" 실시간으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있는 시스템이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) (요구사항 추적) | 영향 분석 매트릭스 |
|:---|:---|:---|
| **목적** | 요구사항 완전성·[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 변경 요청 시 영향 범위 파악 |
| **방향** | 양방향 (요구사항↔테스트) | 변경점→영향 받는 항목 |
| **사용 시점** | 개발 전 기간 | 변경 요청(CR) 발생 시 |

- **📢 섹션 요약 비유**: RTM은 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)(완성도 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))이고, 영향 분석 매트릭스는 도미노 패(한 변경이 어디까지 영향을 주는지 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/))이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 의료기기 소프트웨어 DO-178C 준수
1. 항공/의료 분야에서 모든 요구사항(L1~L5 수준)이 설계·코드·테스트와 1:1로 추적 가능해야 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/).
2. [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 없이는 "이 테스트가 어느 요구사항을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는가?" 설명 불가 → [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 실패.
3. 도구: IBM DOORS, Polarion, Jama Connect → 요구사항 ID 기반 자동 추적.

### 범위 변경([Scope Creep](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/)) 조기 탐지
- 신규 코드가 추가됐는데 연결된 요구사항이 없다면 → 승인되지 않은 기능 추가([Scope Creep](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/)) 징후.
- [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 정기 검토로 이를 조기에 탐지하고 PM에게 보고.

- **📢 섹션 요약 비유**: RTM에 없는 코드 추가는 건축 설계도에 없는 방을 몰래 짓는 것이다. 설계도([RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/))와 실제 건물(코드)이 항상 일치해야 안전하다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **완전성** | 모든 요구사항 구현·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 보장 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 대응</strong> | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 심사 추적 근거 제공 |
| **영향 분석** | 변경 시 영향 범위 즉시 파악 |

현대 [ALM](/knowledge-base/studynote/04_software_engineering/06_software_architecture/390_application_lifecycle_management/) ([Application Lifecycle Management](/knowledge-base/studynote/04_software_engineering/06_software_architecture/390_application_lifecycle_management/)) 플랫폼(Jira, Azure [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/), IBM ELM)은 요구사항-설계-코드-테스트 간 추적을 자동화하여 RTM을 수동으로 유지할 필요 없이 실시간으로 추적 가능성을 보장한다.

- **📢 섹션 요약 비유**: 자동화 RTM은 스마트 공장의 생산 추적 시스템이다. 원자재(요구사항)가 어느 라인(코드)에서 어떻게 가공됐고(구현) 어느 검사를 통과했는지(테스트) 실시간으로 추적된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/158_requirements_management_change_control/">요구사항 관리</a></strong> | RTM의 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/">테스트 케이스</a></strong> | RTM의 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 연결 대상 |
| **영향 분석** | [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 기반 변경 영향 범위 파악 |
| <strong>DO-178C/<a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/133_cmmi_capability_maturity_model_integration_levels/">CMMI</a></strong> | [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 필수화하는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 표준 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/390_application_lifecycle_management/">ALM</a> 도구</strong> | [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/) 자동화 지원 플랫폼 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수동 RTM — 스프레드시트 기반 요구사항 추적</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DOORS/Polarion — 전문 요구사항 관리 도구</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">ALM 통합 (Jira/Azure DevOps) — 코드·테스트 자동 연결</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 기반 추적 — NLP로 요구사항↔코드 자동 매핑</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 추적 매트릭스는 요리 레시피 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)예요! 각 재료(요구사항)가 요리(코드)에 들어갔고, 맛 테스트(테스트)를 통과했는지 하나씩 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 표예요.
2. [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)가 있으면 어떤 재료를 빠뜨렸는지(미구현 요구사항) 즉시 알 수 있어요.
3. 요즘은 JIRA 같은 도구가 자동으로 연결해줘서, 더 빠르고 정확하게 추적할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 27 / 530

← **이전**: [24. 위험 기반 감리 (Risk-based Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/)
**다음**: [26. 응용 시스템 영역 감리 (Applications System Area Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/026_applications_system_area_audit/) →

---
