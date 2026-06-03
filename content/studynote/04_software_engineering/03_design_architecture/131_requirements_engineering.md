+++
title = "131. 요구사항 공학 (Requirements Engineering) - 체계적 요구 수집·분석·관리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구사항 공학은 <strong>요구 도출(Elicitation)→분석(Analysis)→명세(<a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/">Specification</a>)→<a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>(<a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">Validation</a>)→관리(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a>)</strong>의 체계적 프로세스로 소프트웨어가 무엇을 해야 하는지를 정의한다.
> 2. **가치**: 프로젝트 실패의 60%+가 요구사항 문제(누락·모호·변경)에서 발생하며, 개발 후반 요구 변경 비용은 초기 대비 <strong>50~200배</strong>이므로 체계적 공학이 필수이다.
> 3. **판단 포인트**: 기능 요구사항(FR)과 [비기능 요구사항](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/)([NFR](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/), 성능·보안·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))을 구분하고, [요구사항 추적 매트릭스](/knowledge-base/studynote/04_software_engineering/03_design_architecture/157_requirements_traceability_matrix_rtm/)([RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/))로 전 생명주기 추적해야 한다.

---

## Ⅰ. 개요 및 필요성

요구사항 공학(Requirements Engineering, RE)은 소프트웨어 시스템이 <strong>무엇을 해야 하는가</strong>를 체계적으로 발견·문서화·관리하는 공학 분야이다. 1990년대 초 대형 국방·항공 프로젝트에서 요구 불명확으로 인한 대규모 실패가 반복되자, IEEE와 SEI(소프트웨어 공학 연구소)가 체계적 RE 방법론을 정립하기 시작했다. 1998년 발표된 IEEE 830 SRS(Software Requirements Specification) 표준이 분야의 초석이 되었다.

현대 소프트웨어 프로젝트에서 요구사항 문제는 여전히 가장 큰 실패 원인이다. Standish Group의 CHAOS Report에 따르면 IT 프로젝트 성공률은 30% 미만이며, 실패 원인의 1위는 항상 "불명확하거나 변경되는 요구사항"이다. 개발 초기에 1달러로 수정할 수 있는 요구 오류가, 설계 단계에서는 5달러, 구현 단계에서는 20달러, 테스트 단계에서는 50달러, 출시 후에는 200달러 이상의 비용이 든다는 연구(Boehm, 1981)가 이를 증명한다.

요구사항 공학의 핵심은 두 가지 방향의 올바름을 보장하는 것이다. <strong>검증(Verification)</strong>은 "시스템을 올바르게 만들고 있는가(Are we building the system right?)"를 확인하고, <strong>확인(Validation)</strong>은 "올바른 시스템을 만들고 있는가(Are we building the right system?)"를 검증한다. Agile 환경에서는 User Story와 BDD(Behaviour-Driven Development)로 이 두 가지를 지속적으로 수행한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">도출 → 분석 → 명세(SRS) → 검증 → 관리</div>
<div class="kb-diagram-note">↑____________________________| (반복 순환)</div>
<div class="kb-diagram-note">비용 곡선:</div>
<div class="kb-diagram-note">요구 단계 수정 비용: 1x</div>
<div class="kb-diagram-note">설계 단계 수정 비용: 5x</div>
<div class="kb-diagram-note">구현 단계 수정 비용: 20x</div>
<div class="kb-diagram-note">테스트 단계 수정 비용: 50x</div>
<div class="kb-diagram-note">출시 후 수정 비용: 100~200x</div>
</div>
</div>



- **📢 섹션 요약 비유**: 요구사항 공학은 건축의 <strong>설계도 작업</strong>이다. 설계도 없이 짓기 시작하면 완공 후 벽을 허물어야 한다. 설계도를 철저히 그릴수록, 완공 후 발생하는 재작업 비용을 드라마틱하게 줄일 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 요구사항 공학 5단계 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구사항 공학 프로세스 (반복 순환)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1.도출</div><div class="kb-diagram-cell">2.분석</div><div class="kb-diagram-cell">3.명세</div><div class="kb-diagram-cell">4.검증</div><div class="kb-diagram-cell">5.관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Elicitation</div><div class="kb-diagram-cell">Analysis</div><div class="kb-diagram-cell">Specification</div><div class="kb-diagram-cell">Validation</div><div class="kb-diagram-cell">Management</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인터뷰</div><div class="kb-diagram-cell">우선순위</div><div class="kb-diagram-cell">SRS</div><div class="kb-diagram-cell">리뷰</div><div class="kb-diagram-cell">RTM</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">JAD</div><div class="kb-diagram-cell">갈등해결</div><div class="kb-diagram-cell">유스케이스</div><div class="kb-diagram-cell">워크스루</div><div class="kb-diagram-cell">변경 관리(CCB)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">프로토타입</div><div class="kb-diagram-cell">실현가능성</div><div class="kb-diagram-cell">User Story</div><div class="kb-diagram-cell">프로토타입</div><div class="kb-diagram-cell">형상 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">관찰</div><div class="kb-diagram-cell">모델링</div><div class="kb-diagram-cell">형식명세</div><div class="kb-diagram-cell">테스트</div><div class="kb-diagram-cell">추적 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">산출물:</div><div class="kb-diagram-cell">산출물:</div><div class="kb-diagram-cell">산출물:</div><div class="kb-diagram-cell">산출물:</div><div class="kb-diagram-cell">산출물:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구 목록</div><div class="kb-diagram-cell">분석 모델</div><div class="kb-diagram-cell">SRS 문서</div><div class="kb-diagram-cell">검증 보고</div><div class="kb-diagram-cell">RTM, 변경 이력</div></div>
</div>
</div>



### 단계별 핵심 기법 및 산출물

| 단계 | 핵심 기법 | 주요 산출물 | 주의 사항 |
|:---|:---|:---|:---|
| **1. 도출** | 인터뷰, JAD, 브레인스토밍, 관찰, 설문 | 요구 목록(Raw Requirements) | 암묵적 요구(Tacit) 발견 |
| **2. 분석** | MoSCoW 우선순위, 갈등 해결, 실현 가능성 분석 | 분석 모델, 우선순위 목록 | 이해관계자 간 충돌 중재 |
| **3. 명세** | SRS(IEEE 830), 유스케이스, User Story, 형식명세(Z, OCL) | SRS 문서, 유스케이스 명세 | 모호성 제거, 측정 가능 수치 |
| **4. 검증** | 리뷰, 워크스루, 인스펙션, 프로토타입 검증, 테스트 케이스 | 검증 보고서, 결함 목록 | 완전성·일관성·추적성 확인 |
| **5. 관리** | RTM, CCB(변경 통제 위원회), 형상 관리(CM) | RTM, 변경 이력, 형상 기준선 | 변경 영향 분석 필수 |

### 요구사항 품질 특성 (IEEE 830 기준)

| 품질 특성 | 설명 | 나쁜 예 | 좋은 예 |
|:---|:---|:---|:---|
| **완전성 (Complete)** | 모든 요구가 포함 | \"기타 기능 추가\" | 모든 기능 명시 |
| **일관성 (Consistent)** | 상호 모순 없음 | \"응답 1초 이내\" vs \"배치 처리\" | 구체적 맥락 구분 |
| **명확성 (Unambiguous)** | 한 가지 해석만 가능 | \"빠른 응답\" | \"P99 < 200ms\" |
| **추적성 (Traceable)** | 요구→설계→코드→테스트 연결 | 번호 없는 요구 | REQ-001 번호 부여 |
| **검증가능성 (Verifiable)** | 테스트로 확인 가능 | \"사용자 친화적\" | \"SUS 점수 80 이상\" |
| **수정가능성 (Modifiable)** | 변경이 용이한 구조 | 산문형 나열 | 번호 체계 + 모듈 구조 |

### 요구사항 유형 계층 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비즈니스 요구사항 (Business Requirements)</div>
<div class="kb-diagram-tree-item" style="--depth:1">이해관계자 요구사항 (Stakeholder Requirements)</div>
<div class="kb-diagram-tree-item" style="--depth:4">시스템 요구사항 (System Requirements)</div>
<div class="kb-diagram-tree-item" style="--depth:7">기능 요구사항 (FR: Functional Requirements)</div>
<div class="kb-diagram-note">─ 유스케이스, User Story, API 명세</div>
<div class="kb-diagram-tree-item" style="--depth:7">비기능 요구사항 (NFR: Non-Functional Requirements)</div>
<div class="kb-diagram-note">─ 성능, 보안, 가용성, 확장성, 유지보수성</div>
<div class="kb-diagram-tree-item" style="--depth:7">제약사항 (Constraints)</div>
<div class="kb-diagram-tree-item" style="--depth:8">기술, 비용, 법적, 시간적 제약</div>
</div>
</div>



- **📢 섹션 요약 비유**: 요구사항 공학의 5단계는 건물 설계 과정이다. 도출=현장 측량, 분석=설계 검토, 명세=도면 작성, 검증=구조 검사, 관리=설계 변경 기록과 동일하다.

---

## Ⅲ. 비교 및 연결

### 전통 RE vs Agile RE 비교

| 항목 | 전통적 RE (폭포수) | Agile RE |
|:---|:---|:---|
| **산출물** | SRS 문서 (수백 페이지) | User Story, Backlog |
| **도출 시점** | 프로젝트 초기 집중 | 스프린트마다 지속 |
| **변경 대응** | CCB 프로세스 (느림) | 백로그 재우선순위화 (빠름) |
| **형식화** | 높음 (IEEE 830, 형식명세) | 낮음 (대화 중심) |
| **추적성** | RTM으로 엄격 추적 | 스토리-테스트 연결 |
| **장점** | 복잡 시스템, 안전 필수 | 변화 빠른 비즈니스 |
| **단점** | 변경 대응 느림 | 큰 그림 누락 위험 |

### RE 산출물과 후속 활동 연결

| RE 산출물 | 연결되는 후속 활동 | 핵심 링크 |
|:---|:---|:---|
| **SRS** | 설계 (아키텍처 결정) | NFR → 아키텍처 드라이버 |
| **유스케이스** | 시스템 설계, 테스트 케이스 | 유스케이스 → 시나리오 → 테스트 |
| **User Story** | 스프린트 계획, 인수 기준 | Story + AC → TDD |
| **RTM** | 테스트 계획, 품질 보증 | 요구-테스트 커버리지 확인 |
| **NFR 명세** | 아키텍처, 성능 테스트 | NFR → 아키텍처 패턴 선택 |

### 관련 표준 비교

| 표준 | 범위 | 핵심 내용 |
|:---|:---|:---|
| **IEEE 830** | SRS 구조 | 요구사항 명세서 작성 가이드 |
| **IEEE 29148** | RE 전체 프로세스 | 최신 RE 국제 표준 (2011) |
| **ISO/IEC 25010** | 품질 특성 | NFR 분류 체계 (8대 특성) |
| **IREB CPRE** | RE 자격 인증 | 국제 RE 전문가 인증 |

- **📢 섹션 요약 비유**: 전통 RE는 완공 전 모든 설계를 확정하는 방식(고층 빌딩), Agile RE는 층마다 설계를 검토하며 올라가는 방식(빠른 상업 건물)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **FR/NFR 분리**: 기능 요구사항과 비기능 요구사항을 명확히 구분하였는가?
2. **NFR 수치화**: "빠른 응답" 대신 "P99 < 200ms"처럼 측정 가능한 수치로 명세하였는가?
3. **추적성 확보**: RTM으로 요구사항→설계→코드→테스트까지 연결이 가능한가?
4. **이해관계자 커버리지**: 모든 핵심 이해관계자(비즈니스, 개발, 운영, 보안)의 요구가 반영되었는가?
5. **변경 관리**: CCB(변경 통제 위원회) 또는 Agile 백로그 관리 프로세스가 있는가?
6. **검증 계획**: 각 요구사항을 어떻게 검증할지 수용 기준(Acceptance Criteria)이 정의되었는가?
7. **우선순위**: MoSCoW(Must/Should/Could/Won't) 또는 점수 기반 우선순위가 설정되었는가?

### 안티패턴

- **골드 도금(Gold Plating)**: 요구 이상의 기능을 개발자가 임의로 추가하는 패턴. 일정·비용 초과의 원인이 되며, 승인되지 않은 요구는 RTM에 등록되지 않아 추적 불가 상태가 된다. 모든 기능은 이해관계자 승인을 거쳐야 한다.

- **분석 마비(Analysis Paralysis)**: 완벽한 요구 명세를 위해 도출·분석 단계에서 과도한 시간을 소비하는 패턴. Agile 환경에서는 "충분히 좋은" 요구 명세로 개발을 시작하고 반복하며 보완하는 것이 현실적이다.

- **프록시 고객 문제(Proxy Customer Problem)**: 실제 사용자가 아닌 중간 관리자나 프로젝트 관리자가 요구를 대리로 전달하는 패턴. 실제 사용자의 목소리가 왜곡되며, 숨겨진 요구를 발견하기 어렵다. 직접 인터뷰·관찰·JAD 워크숍으로 실제 사용자에게 접근해야 한다.

- **스코프 크리프(Scope Creep)**: 명확한 변경 관리 프로세스 없이 요구사항이 지속적으로 추가되는 패턴. CCB를 통한 변경 영향 분석 및 승인 프로세스가 필수이다.

- **모호한 NFR(Vague NFR)**: "사용하기 쉬운", "안정적인" 등 측정 불가능한 비기능 요구사항. 테스트가 불가능하며 개발 완료 기준이 불명확해진다.

- **📢 섹션 요약 비유**: RE 안티패턴은 건축의 설계 오류와 같다. 금 도금은 "요청하지 않은 수영장 추가", 분석 마비는 "설계 중 건물 못 짓기", 프록시 고객은 "집주인 대신 부동산이 인테리어 결정하기"이다.

---

## Ⅴ. 기대효과 및 결론

요구사항 공학을 체계적으로 수행하면 프로젝트 실패 위험이 대폭 감소한다. 정량적 효과로는 요구 결함이 코드 레벨에서 발견될 때의 수정 비용(50배)에 비해 RE 단계에서 발견 시 1배로 억제되며, RTM을 활용한 추적성 확보는 테스트 커버리지를 30% 이상 향상시킨다. 정성적으로는 이해관계자 간 공통 이해(Shared Understanding)를 형성하여 개발팀과 비즈니스 팀 간의 소통 오해를 줄인다.

현대 개발 환경에서 AI는 RE를 혁신하고 있다. 자연어 처리(NLP) 기술로 회의록, 이메일, 지원 티켓에서 잠재 요구사항을 자동 추출하고, 요구사항 간 상충(Conflict) 관계를 자동 탐지하는 도구가 등장하고 있다. 또한 LLM(대형 언어 모델)을 활용한 User Story 자동 생성, 인수 기준 도출이 실험적으로 적용되고 있다.

요구사항 공학은 소프트웨어 개발의 <strong>가장 중요한 첫 단추</strong>이다. Agile 환경에서도 RE의 본질은 변하지 않는다. 단지 형식이 SRS에서 User Story로, 일회성 도출에서 지속적 도출로 변화했을 뿐이다. 기술사 시험에서 RE 관련 문제는 "왜 체계적 RE가 필요한가", "각 단계의 기법과 산출물", "FR vs NFR 구분", "RTM의 역할"을 중심으로 출제된다.

- **📢 섹션 요약 비유**: 요구사항 공학 투자는 보험료다. 초기에 철저히 투자하면 개발 후반의 막대한 재작업 비용이라는 "사고"를 예방한다. 보험을 아끼다 사고 나면 손해가 수백 배이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **SRS (IEEE 830)** | 요구사항 명세서 표준 구조 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/">RTM</a></strong> | 요구→설계→코드→테스트 추적 매트릭스 |
| **MoSCoW** | Must/Should/Could/Won't 우선순위 분류 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/">User Story</a></strong> | Agile 요구사항 표현 방식 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/">NFR</a></strong> | 비기능 요구사항 (품질 속성) |
| **CCB** | 변경 통제 위원회 (Change Control Board) |
| **JAD** | Joint Application Development (합의 워크숍) |
| **IEEE 29148** | 최신 RE 국제 표준 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 요구 수집 (~1990s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IEEE 830 SRS 표준 (1998) ←── 폭포수 모델 전성기</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">유스케이스 기반 RE (UML, 2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">User Story + Agile RE (2005~) ←── 애자일 선언(2001) 영향</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BDD + 인수 테스트 주도 개발 (2010s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI 요구 분석 자연어→요구사항 자동 분류</div>
<div class="kb-diagram-tree-item" style="--depth:8">LLM 기반 User Story 생성</div>
<div class="kb-diagram-tree-item" style="--depth:8">요구 충돌 자동 탐지</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 요구사항 공학은 <strong>설계도</strong>예요. 집을 짓기 전에 **뭘 만들지 정확히** 그려야 해요.
2. 설계도 없이 짓으면 **다 짓고 나서 벽을 허물어야** 해서 돈이 50배 더 들어요.
3. "무엇을, 얼마나 빠르게, 얼마나 안전하게" **모두 적어둬야** 완벽한 설계도예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 131 / 973

← **이전**: [130. 인수 기준 vs 완료 정의 (Acceptance Criteria vs Definition of Done)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/130_acceptance_criteria_vs_dod/)
**다음**: [132. 요구사항 유형 (기능·비기능·제약사항) - FR·NFR·Constraints 분류](/knowledge-base/studynote/04_software_engineering/03_design_architecture/132_types_of_requirements/) →

---
