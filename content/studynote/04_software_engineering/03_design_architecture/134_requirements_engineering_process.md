+++
title = "134. 요구사항 공학 프로세스 - 도출→분석→명세→검증→관리 상세"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구 도출(Elicitation)→분석(Analysis)→명세([Specification](/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/), SRS)→[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))→관리([Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/)) 5단계를 반복 순환하며, 각 단계마다 고유한 기법과 산출물이 있다.
> 2. **가치**: 도출 기법(인터뷰·워크숍·프로토타이핑)을 적절히 조합해야 <strong>숨겨진 요구사항(Hidden Requirements)</strong>을 발견할 수 있고, 명세의 품질이 전체 프로젝트 품질을 결정한다.
> 3. **판단 포인트**: 도출 기법 선택, SRS 구조(IEEE 830), 검증(리뷰·프로토타입·[테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/)), [RTM](/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/)(요구→설계→코드→테스트 추적)이 핵심이다.

---

## Ⅰ. 개요 및 필요성

요구사항 공학 프로세스는 소프트웨어 개발에서 "올바른 시스템을 만들기 위한 체계적 절차"이다. 1970년대 폭포수 모델에서 요구 분석 단계가 독립적으로 정의된 이래, IEEE 830(1998)이 SRS 작성 표준을 정립하고, IEEE 29148(2011)이 RE 전체 프로세스를 국제 표준으로 확립했다. Agile 시대에도 RE의 5단계 본질은 유지되며, 단지 규모와 주기가 달라질 뿐이다.

프로세스가 필요한 핵심 이유는 세 가지다. 첫째, 사용자는 자신이 원하는 것을 정확히 표현하지 못한다. "빠르고 사용하기 쉬운 시스템"이라는 표현은 측정 불가능하다. 도출과 분석 과정에서 이를 "P99 < 200ms, SUS 점수 80 이상"으로 구체화해야 한다. 둘째, 이해관계자 간에는 상충하는 요구가 존재한다. 경영진은 "빠른 출시"를, 보안팀은 "철저한 보안 검증"을 요구한다. 분석 단계에서 이 갈등을 구조적으로 해결해야 한다. 셋째, 요구사항은 변한다. 변경 관리 프로세스 없이는 스코프 크리프(Scope Creep)로 프로젝트가 파국에 이른다.

현대 Agile 환경에서 RE 프로세스는 스프린트마다 반복 수행된다. 폭포수에서의 "1회 완전한 RE"가 Agile에서는 "매 스프린트의 백로그 정제"로 변환된다. 도구도 변했다. SRS 문서 대신 Jira/Confluence의 User Story가 사용되고, RTM 대신 자동화된 테스트-스토리 연결이 추적성을 보장한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">요구사항 공학 5단계 순환 모델:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1.도출</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">2.분석</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">3.명세</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">4.검증</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">5.관리</div></div>
<div class="kb-diagram-note">인터뷰 우선순위 SRS(IEEE 리뷰·워크 RTM, CCB</div>
<div class="kb-diagram-note">JAD 갈등해결 830) 스루·프로 변경 관리</div>
<div class="kb-diagram-note">프로토타 실현가능 유스케이스 토타입</div>
<div class="kb-diagram-note">이핑 성 분석 User Story</div>
<div class="kb-diagram-note">관찰</div>
</div>
</div>



- **📢 섹션 요약 비유**: 요구 프로세스는 의사의 진료다. 도출=문진(어디가 아프세요?), 분석=진단(검사 결과 해석), 명세=처방전(약과 용법), 검증=경과관찰(효과 확인), 관리=진료 기록(이력 유지)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1단계: 도출 (Elicitation)

도출은 이해관계자로부터 요구사항을 끌어내는 활동이다. 문제는 사용자가 자신의 요구를 완전히 알고 있지 않다는 것이다. "아이폰이 나오기 전까지 사람들은 터치스크린 스마트폰을 원하는지 몰랐다"는 Steve Jobs의 말처럼, 사용자는 현재의 불편을 해결책과 함께 표현하지 못한다.

| 도출 기법 | 특징 | 강점 | 약점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| **인터뷰** | 1:1 심층 대화 | 깊이 있는 이해 | 시간 소요, 편향 위험 | 핵심 이해관계자 |
| **JAD 워크숍** | 그룹 구조화 회의 | 다부서 합의 | 퍼실리테이터 역량 의존 | 이해관계 충돌 |
| **브레인스토밍** | 자유 아이디어 발산 | 창의적 요구 발견 | 비체계적 | 초기 아이디어 탐색 |
| **프로토타이핑** | 빠른 시각화 | 숨겨진 요구 발견 | 프로토타입에 집착 위험 | UI/UX 요구 |
| **쉐도잉/관찰** | 현장 직접 관찰 | 암묵적 요구 발견 | 시간·비용 | 복잡한 업무 프로세스 |
| **설문** | 대규모 의견 수집 | 빠른 광범위 수집 | 깊이 부족 | 사용자 수가 많을 때 |

### 2단계: 분석 (Analysis)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">분석 단계 활동:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">요구 목록 수집</div></div>
<div class="kb-diagram-note">→ 중복 제거 및 통합</div>
<div class="kb-diagram-note">→ 우선순위 설정 (MoSCoW, AHP, Kano 모델)</div>
<div class="kb-diagram-note">→ 실현 가능성 분석 (기술적·비용적·일정적)</div>
<div class="kb-diagram-note">→ 이해관계자 갈등 해결</div>
<div class="kb-diagram-note">→ 분석 모델 작성 (DFD, UML 유스케이스)</div>
</div>
</div>



| 분석 기법 | 목적 | 산출물 |
|:---|:---|:---|
| **MoSCoW** | 우선순위 결정 | Must/Should/Could/Won't 분류 |
| **Kano 모델** | 고객 만족 유형 분류 | 필수·성과·감동 요소 구분 |
| **DFD** | 데이터 흐름 모델링 | 데이터 흐름도 |
| **유스케이스 다이어그램** | 기능 범위 시각화 | UC 다이어그램 |
| **갈등 해결 매트릭스** | 이해관계자 충돌 조정 | 합의 결정 문서 |

### 3단계: 명세 (Specification)

IEEE 830 SRS 구조:
```text
SRS (Software Requirements Specification):
  1. 서론
     1.1 목적
     1.2 범위
     1.3 정의·약어
     1.4 참조문서
  2. 전체 설명
     2.1 제품 관점 (컨텍스트 다이어그램)
     2.2 제품 기능
     2.3 사용자 특성
     2.4 제약사항
  3. 특정 요구사항
     3.1 외부 인터페이스 요구사항
     3.2 기능 요구사항 (유스케이스별)
     3.3 성능 요구사항 (NFR)
     3.4 설계 제약
     3.5 SW 시스템 속성
  부록: RTM (요구사항 추적 매트릭스)
```

### 4단계: 검증 (Validation)

| 검증 기법 | 목적 | 특징 |
|:---|:---|:---|
| **검토(Review)** | 문서 결함 발견 | 비공식, 빠름 |
| **워크스루(Walkthrough)** | 작성자가 설명, 질문 수집 | 반공식 |
| **인스펙션(Inspection)** | 체크리스트 기반 결함 발견 | 공식, 체계적 |
| **프로토타입 검증** | 사용자 피드백으로 확인 | 시각적, 효과적 |
| **테스트 케이스 도출** | 요구의 테스트 가능성 검증 | 구체적 수용 기준 |

### 5단계: 관리 (Management)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RTM (Requirements Traceability Matrix) 구조:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-ID</div><div class="kb-diagram-cell">요구사항</div><div class="kb-diagram-cell">설계문서</div><div class="kb-diagram-cell">코드모듈</div><div class="kb-diagram-cell">테스트케이스</div><div class="kb-diagram-cell">상태</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-001</div><div class="kb-diagram-cell">로그인 기능</div><div class="kb-diagram-cell">Design-03</div><div class="kb-diagram-cell">auth.py</div><div class="kb-diagram-cell">TC-015</div><div class="kb-diagram-cell">완료</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-002</div><div class="kb-diagram-cell">2FA 인증</div><div class="kb-diagram-cell">Design-04</div><div class="kb-diagram-cell">auth.py</div><div class="kb-diagram-cell">TC-016</div><div class="kb-diagram-cell">진행중</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">REQ-003</div><div class="kb-diagram-cell">P99&lt;200ms</div><div class="kb-diagram-cell">Design-07</div><div class="kb-diagram-cell">-</div><div class="kb-diagram-cell">PT-003</div><div class="kb-diagram-cell">계획중</div></div>
<div class="kb-diagram-note">변경 관리 (CCB: Change Control Board):</div>
<div class="kb-diagram-note">변경 요청 접수 → 영향 분석 → 승인/거부 → 구현 → RTM 갱신</div>
</div>
</div>



- **📢 섹션 요약 비유**: 5단계 프로세스는 집 건축의 단계다. 도출=건축주 인터뷰, 분석=요구 정리+예산 확인, 명세=설계도 작성, 검증=설계도 검토회의, 관리=설계 변경 기록이다.

---

## Ⅲ. 비교 및 연결

### 전통 RE 프로세스 vs Agile RE 비교

| 항목 | 전통 RE (폭포수) | Agile RE |
|:---|:---|:---|
| **도출 시점** | 프로젝트 초기 집중 | 매 스프린트 지속 |
| **명세 형식** | SRS (수백 페이지) | User Story + AC |
| **변경 관리** | CCB 프로세스 | 백로그 재우선순위화 |
| **검증 시점** | 개발 전 | 지속적 (TDD, BDD) |
| **추적성** | RTM 문서 | 자동화된 테스트 링크 |
| **적합 분야** | 안전 필수 시스템 | 빠른 변화 비즈니스 |

### 요구사항 공학과 연결 개념

| 연결 개념 | 관계 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/">RTM</a></strong> | 5단계 관리의 핵심 도구 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a></strong> | 변경 관리의 의사결정 기구 |
| **SRS (IEEE 830)** | 3단계 명세의 표준 형식 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/">User Story</a></strong> | Agile RE의 명세 단위 |
| **BDD** | 행동 기반 개발로 검증과 명세 통합 |
| **형상 관리** | 요구 문서의 버전 관리 |

- **📢 섹션 요약 비유**: RE 프로세스 단계는 음식점 주문 과정과 같다. 도출=손님 주문 받기, 분석=가능한 메뉴 확인+우선순위, 명세=주문서 작성, 검증=주방장과 확인, 관리=주문 변경 기록이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **도출 기법 다양화**: 인터뷰만 사용하지 않고, JAD·프로토타이핑·관찰을 조합하여 숨겨진 요구를 발견하였는가?
2. **SRS 완전성**: IEEE 830 구조에 따라 FR, NFR, 외부 인터페이스, 제약사항이 모두 명세되었는가?
3. **RTM 구축**: 모든 요구사항이 설계 문서, 코드 모듈, 테스트 케이스에 연결되어 추적 가능한가?
4. **검증 완료**: 각 요구사항에 대해 인스펙션 또는 프로토타입 검증이 수행되었는가?
5. **변경 관리**: 요구 변경이 CCB 승인을 거쳐 RTM과 SRS에 반영되는 프로세스가 있는가?
6. **우선순위 명확화**: MoSCoW 또는 점수 기반으로 요구사항 우선순위가 결정되었는가?

### 안티패턴

- **도출 생략(Elicitation Skip)**: 시간 부족을 이유로 도출 단계를 생략하고 개발자가 요구를 임의로 가정하는 패턴. "아마도 이렇게 원하겠지"는 가장 위험한 개발 시작 방식이다. 최소 핵심 이해관계자 인터뷰와 JAD 워크숍은 필수이다.

- **과도한 명세 문서주의**: 수백 페이지 SRS를 완벽하게 작성하는 데 3개월을 쓰는 패턴. 명세는 이해의 도구이지 목적이 아니다. "충분히 좋은" 명세로 시작하고, 프로토타입·개발을 통해 보완하는 반복적 접근이 현실적이다.

- **RTM 방치**: RTM을 초기에 만들고 이후 업데이트하지 않는 패턴. 요구 변경 시 RTM이 갱신되지 않으면 추적성이 소실되고, 테스트 커버리지를 파악하기 어려워진다.

- **이해관계자 편향**: 접근하기 쉬운 이해관계자(관리자, 팀장)의 요구만 반영하고, 실제 사용자(현장 작업자, 최종 사용자)의 요구를 누락하는 패턴.

- **📢 섹션 요약 비유**: RE 안티패턴은 설계도 없이 집 짓기(도출 생략), 설계도만 그리다 공사 못 하기(과도한 문서주의), 설계 변경 후 도면 업데이트 안 하기(RTM 방치)이다.

---

## Ⅴ. 기대효과 및 결론

체계적 RE 프로세스를 수행하면 프로젝트 전반에 걸쳐 품질이 향상된다. 정량적으로 RE 단계에서 발견한 결함의 수정 비용은 테스트 단계 대비 1/50, 운영 단계 대비 1/200이다. RTM으로 추적성을 확보하면 변경 영향 분석이 가능해지고, 무의식적 범위 확장(스코프 크리프)을 사전에 통제할 수 있다.

프로세스 단계별로 산출물을 남기면 프로젝트 중간에 팀원이 바뀌어도 연속성이 유지된다. SRS와 RTM은 신규 팀원의 온보딩 자료가 되고, 요구사항 변경 이력은 왜 특정 결정이 이루어졌는지 이해하는 근거가 된다.

미래에는 AI가 RE 프로세스를 자동화할 것이다. 회의록과 이메일에서 요구사항을 자동 추출하고, 기존 요구와 충돌을 탐지하며, User Story와 인수 기준을 초안으로 생성하는 도구가 이미 실험 중이다. 그러나 이해관계자 갈등 조정, 비즈니스 맥락 이해, 우선순위 결정은 여전히 인간 전문가의 역할로 남을 것이다.

- **📢 섹션 요약 비유**: RE 프로세스는 제품 설계·제조의 QA(품질 보증) 프로세스다. 각 단계에 체크포인트를 두고 결함을 조기에 발견하는 것이 전체 비용을 절감하는 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **도출** | 인터뷰·JAD·프로토타이핑 기법 |
| **SRS (IEEE 830)** | 명세 표준 구조 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/667_requirements_traceability_matrix/">RTM</a></strong> | 요구→설계→코드→테스트 추적 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a></strong> | 변경 통제 위원회 |
| **MoSCoW** | 우선순위 분류 (Must/Should/Could/Won't) |
| **인스펙션** | 공식 검증 기법 (Fagan Inspection) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 요구 수집 (~1990s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IEEE 830 SRS 표준 (1998) ── 폭포수 RE 정립</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">유스케이스 기반 RE (UML, 2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">User Story + Agile RE (2005~) ── 애자일 선언 영향</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BDD + 자동화 검증 (2010s) ── Gherkin, Cucumber</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI RE ── 자연어→요구 자동 분류</div>
<div class="kb-diagram-tree-item" style="--depth:4">LLM 기반 User Story 생성</div>
<div class="kb-diagram-tree-item" style="--depth:4">요구 충돌 자동 탐지</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 요구 프로세스는 <strong>의사 진료</strong>예요. 먼저 어디 아프냐(도출) 물어봐요.
2. 진단(분석) 후 **처방전(명세)** 을 써요.
3. 약을 먹고 <strong>경과를 지켜보며(검증)</strong> 진료 기록(관리)을 남겨요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 134 / 973

← **이전**: [133. 비기능 요구사항 (NFR) - 시스템 품질 속성 정의](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/)
**다음**: [135. 요구사항 도출 기법 - 인터뷰·JAD·프로토타이핑·브레인스토밍](/knowledge-base/studynote/04_software_engineering/03_design_architecture/135_requirements_elicitation_techniques/) →

---
