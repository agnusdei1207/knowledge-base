+++
title = "335. 형상 베이스라인 변경 심의 (Configuration Baseline Change Review)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 형상 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 변경 심의는 변경 요청서, 영향도 분석, 승인 이력을 한 체계로 묶어 소프트웨어 형상 항목의 무단 변경을 통제하고 프로젝트 무결성을 유지하는 설계·감리 주제다.
> 2. **가치**: 승인되지 않은 변경이 시스템 품질·일정·예산에 미치는 파급을 사전에 차단하고, 모든 변경 이력을 추적 가능하게 유지함으로써 감사 대응성과 재현성을 확보한다.
> 3. **판단 포인트**: 변경 요청서 작성부터 영향도 분석, CCB(변경통제위원회) 심의, 이행 확인, 형상 업데이트까지의 전 과정이 증거 기반으로 닫혀 있는지가 감리 핵심이다.

---

## Ⅰ. 개요 및 필요성

형상관리(Software Configuration Management, SCM)는 소프트웨어 개발 과정에서 산출물(소스 코드, 설계서, 테스트 케이스, 빌드 산출물 등)의 변경을 체계적으로 식별·기록·제어하는 활동이다. 이 중 형상 베이스라인(Configuration Baseline)은 특정 시점에 공식적으로 합의되고 승인된 형상 항목의 집합으로, 이후의 모든 변경은 반드시 심의 절차를 거쳐야 한다.

형상 베이스라인 변경 심의가 필요한 이유는 소프트웨어 프로젝트의 특성에 있다. 개발 과정에서 요구사항 변경, 기술적 한계 발견, 외부 환경 변화 등으로 인해 변경이 불가피하게 발생한다. 그러나 무통제 변경(Uncontrolled Change)은 품질 저하, 일정 지연, 예산 초과의 주요 원인이다. 변경통제위원회(CCB, Change Control Board)를 통한 공식 심의 절차가 이를 방지한다.

특히 공공 정보화사업에서 형상 베이스라인 변경 심의는 감리의 핵심 점검 항목이다. 변경 요청서, 영향도 분석, 승인 이력이 체계적으로 관리되지 않으면, 감리 보고서의 지적 수준을 넘어 사업 정산 분쟁이나 하자 책임 분쟁으로 이어질 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">형상 베이스라인 변경 심의 전체 흐름</div></div>
<div class="kb-diagram-note">변경 필요성 인식 (개발자/사용자)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">변경 요청서 (Change Request) 작성</div>
<div class="kb-diagram-tree-item" style="--depth:1">변경 내용, 사유, 요청자, 우선순위</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">영향도 분석 (Impact Analysis)</div>
<div class="kb-diagram-tree-item" style="--depth:1">일정·비용·품질·기술 영향 파악</div>
<div class="kb-diagram-tree-item" style="--depth:1">연관 형상 항목 식별</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CCB 심의 (Change Control Board)</div>
<div class="kb-diagram-tree-item" style="--depth:1">승인 / 조건부 승인 / 반려</div>
<div class="kb-diagram-note">승인됨 │ 반려됨</div>
<div class="kb-diagram-note">▶ 변경 요청 철회/수정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">변경 이행 (Implementation)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">이행 확인 (Verification)</div>
<div class="kb-diagram-tree-item" style="--depth:1">변경 내용 적용 검증</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">형상 업데이트 및 기준선 재확정</div>
</div>
</div>



- **📢 섹션 요약 비유**: 건물 도면을 수정할 때 설계사, 시공사, 발주자 세 명 모두의 도장을 받아야 공사를 진행할 수 있는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 형상관리 핵심 개념

**형상 항목 (Configuration Item, CI)**: 변경 관리의 대상이 되는 모든 산출물. 소스 코드, 요구사항 명세서, 설계서, 테스트 케이스, 데이터베이스 스크립트, 빌드 스크립트 등이 포함된다.

**베이스라인 유형**: 소프트웨어 개발 주기에 따라 다음과 같은 베이스라인이 존재한다.

| 베이스라인 유형 | 확정 시점 | 주요 형상 항목 |
|:---|:---|:---|
| 기능 베이스라인 (FBL) | 시스템 요구사항 검토 완료 후 | 시스템 요구사항 명세서 |
| 할당 베이스라인 (ABL) | 소프트웨어 요구사항 검토 완료 후 | SW 요구사항 명세서 |
| 제품 베이스라인 (PBL) | 최종 소프트웨어 검증 완료 후 | 소스 코드, 실행 파일, 매뉴얼 |

**CCB (변경통제위원회, Change Control Board)**: 모든 변경 요청을 검토하고 승인/반려를 결정하는 공식 기구. 프로젝트 관리자, 품질 관리자, 발주자 대표, 핵심 개발자로 구성된다.

### 2. 변경 심의 프로세스 상세



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">CCB 변경 심의 5단계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1단계: 변경 요청서 접수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 요청 ID, 날짜, 요청자, 변경 유형</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 변경 대상 형상 항목 명시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 변경 이유 및 우선순위 (긴급/일반/제안)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2단계: 영향도 분석</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 일정 영향: 예상 추가 소요 시간</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 비용 영향: 추가 인력·자원 비용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 기술 영향: 연관 모듈·데이터 영향 범위</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 품질 영향: 회귀 테스트 범위</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3단계: CCB 심의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 정기 또는 임시 CCB 회의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 승인 조건 명시 (조건부 승인 시)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 회의록 작성 및 서명</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4단계: 변경 이행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 승인된 변경만 이행 시작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 형상관리 도구에 변경 이력 기록</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 회귀 테스트 실시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5단계: 베이스라인 업데이트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 변경 적용 후 형상 항목 버전 갱신</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 변경 이력 완료 처리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 관련 산출물 동기화 (설계서·테스트 케이스 등)</div></div>
</div>
</div>



또한 형상 베이스라인 변경 심의는 한 단계만 잘해서는 완성되지 않는다. 기준선, 실행 메커니즘, 증적이 순환 구조를 이루어야 하며, 하나라도 비면 적합 판정의 신뢰도가 떨어진다.

- **📢 섹션 요약 비유**: 재료 창고, 작업 순서, 검수표가 한 줄로 이어져야 하는 공장과 같다.

---

## Ⅲ. 비교 및 연결

### 형상관리 도구 비교

| 비교 항목 | Git 기반 도구 (GitHub/GitLab) | SVN (Subversion) | JIRA + Bitbucket |
|:---|:---|:---|:---|
| 분산 버전 관리 | 지원 (분산) | 중앙집중식 | 분산 |
| 변경 요청 관리 | Pull Request + Issue | 별도 도구 필요 | JIRA 이슈 연동 |
| CCB 심의 지원 | 코드 리뷰 + 승인 기능 | 미흡 | 워크플로우 자동화 |
| 감리 증빙 생성 | 커밋 이력, PR 이력 | 커밋 로그 | 변경 이력 리포트 |
| 공공사업 적용성 | 높음 | 일부 사용 | 높음 |

### 형상관리 vs. 변경관리 연결

| 비교 항목 | 형상관리 (SCM) | 변경관리 (Change Management) |
|:---|:---|:---|
| 관리 대상 | 소프트웨어 산출물의 버전·이력 | 변경 요청의 승인·이행·종결 |
| 주요 활동 | 형상 식별, 형상 통제, 형상 감사 | 변경 영향 분석, CCB 심의, 이행 추적 |
| 관계 | 형상관리는 변경관리의 결과를 기록 | 변경관리는 형상관리 대상을 제어 |

연결 개념으로는 시정 조치 추적, 변경관리, 재검증이 있다. 즉 형상 베이스라인 변경 심의는 단일 기법이 아니라 거버넌스와 운영 체계 속에서 읽어야 답안의 깊이가 생긴다.

- **📢 섹션 요약 비유**: 계획표만 있는 반과 숙제 검사까지 하는 반의 차이를 비교하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 형상 베이스라인 변경 심의를 도입했는가보다 어떤 조건에서 통제 효과가 나타나는가를 먼저 봐야 한다. 기술사 답안도 '무조건 CCB 적용'이 아니라 범위, 증거, 예외, 비용을 함께 써야 설득력이 생긴다.

### 실무 적용 시나리오

**시나리오 1 - 긴급 변경**: 운영 중 보안 취약점이 발견되어 즉각 패치가 필요한 경우, 긴급 CCB를 구성하여 24시간 내 심의를 완료하고, 사후 정식 변경 이력을 업데이트하는 절차를 적용

**시나리오 2 - 범위 변경 통제**: 발주자의 추가 기능 요구가 발생했을 때, 공식 변경 요청서 없이 개발자가 임의로 구현하는 경우를 CCB 프로세스로 사전 차단 → 계약 범위 변경 협의 후 공식 진행

**시나리오 3 - 감리 증빙 준비**: 감리원이 "변경이 적절히 통제되었는가"를 점검할 때, CCB 회의록, 변경 요청서, 영향도 분석서, 승인 이력을 패키지로 제출

### 판단 체크리스트

1. 기준 문서(형상관리 계획서)와 변경 통제 절차가 합의되었는가?
2. 모든 변경이 공식 변경 요청서를 통해 접수되었는가?
3. 영향도 분석이 일정·비용·기술 측면을 모두 포함하는가?
4. CCB 심의 결과(승인/반려)와 사유가 공식 기록으로 남아 있는가?
5. 변경 이행 후 회귀 테스트와 베이스라인 업데이트가 확인되었는가?

### 안티패턴

- **비공식 구두 변경**: 개발자가 발주자의 구두 요청으로 변경을 적용하는 경우 → 변경 이력 없음, 책임 소재 불명확, 감리 지적 대상
- **형식적 CCB**: 실제 심의 없이 회의록만 작성하고 승인 도장을 찍는 경우 → 영향도 미파악으로 연쇄 장애 발생
- **베이스라인 미업데이트**: 변경이 적용되었지만 형상관리 도구의 베이스라인 업데이트를 하지 않는 경우 → 이후 빌드 오류 및 배포 불일치

- **📢 섹션 요약 비유**: 체크리스트에 담당자와 마감일을 적어 실제로 끝내는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

형상 베이스라인 변경 심의를 제대로 적용하면 다음과 같은 효과가 나타난다.

**정량적 효과**
- 무통제 변경으로 인한 버그 발생률 40~60% 감소 (형상관리 성숙도 높은 조직 기준)
- 사업 범위 크리프(Scope Creep)로 인한 일정 초과 30~50% 감소
- 감리 지적사항 중 형상관리 관련 항목 사전 해소

**정성적 효과**
- 모든 변경의 추적 가능성 확보 (Traceability)
- 개발 팀과 발주자 간 책임 경계 명확화
- 재현 가능한 빌드·배포 환경 유지

결론적으로 형상 베이스라인 변경 심의는 프로젝트의 혼돈을 질서로 전환하는 핵심 통제 메커니즘이다. 범위 정의, 구조 설계, 증거 검증, 종결 관리의 네 축을 함께 쓰는 것이 실무형 답안의 핵심이다. 앞으로는 자동화된 변경 감지 도구와 AI 기반 영향도 분석이 결합되어 CCB 심의의 속도와 정확도가 더욱 향상될 전망이다.

- **📢 섹션 요약 비유**: 인수인계 노트가 좋아야 다음 사람이 같은 실수를 반복하지 않는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 형상 항목 (CI) | 변경 관리의 대상이 되는 모든 소프트웨어 산출물이다. |
| 베이스라인 | 공식 승인된 형상 항목의 기준점으로, 이후 변경은 심의를 거친다. |
| CCB (변경통제위원회) | 변경 요청을 심의하고 승인/반려를 결정하는 공식 기구다. |
| 변경 요청서 | 형상 베이스라인 변경 심의의 출발점이 되는 핵심 문서다. |
| 영향도 분석 | 변경이 일정·비용·품질에 미치는 파급 효과를 사전 파악한다. |
| 시정 조치 추적 | 승인된 변경이 실제로 이행되었는지를 추적하는 활동이다. |
| 형상 감사 | 형상관리 프로세스의 준수 여부를 독립적으로 검증하는 활동이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비공식 변경 관리 (개인 폴더 기반)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CVS/SVN 기반 형상 통제</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Git 기반 분산 형상관리 + CCB 프로세스</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">자동화 변경 감지 및 영향도 분석 (DevOps 통합)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 기반 자동 정책 심의 지원 도구</div></div>
</div>
</div>



- 관련 키워드: 형상관리(SCM), [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/), CCB, 변경 요청서, 영향도 분석, Git, 시정 조치 추적

### 👶 어린이를 위한 3줄 비유 설명

1. 형상 베이스라인 변경 심의는 레시피를 바꾸고 싶을 때 요리사, 주인, 손님 모두가 함께 의논하고 허락받아야 하는 것과 같아요.
2. 혼자 몰래 재료를 바꾸면 맛이 달라져도 누구 잘못인지 모르게 돼요.
3. 허락받고 바꾸면 나중에 무엇이 왜 바뀌었는지 모두 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 413 / 530

← **이전**: [334. 마이그레이션 무결성 100% 검증 (Migration Integrity Verification)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/334_process/)
**다음**: [336. 고가용성 모의 페일오버 테스트 (High Availability Failover Test)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/336_process/) →

---
