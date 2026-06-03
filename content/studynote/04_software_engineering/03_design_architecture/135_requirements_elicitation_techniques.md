+++
title = "135. 요구사항 도출 기법 - 인터뷰·JAD·프로토타이핑·브레인스토밍"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구 도출(Elicitation)은 <strong>[이해관계자](/knowledge-base/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/)로부터 요구사항을 끌어내는 활동</strong>이며, 인터뷰·JAD·브레인스토밍·프로토타이핑·관찰·설문·[벤치마킹](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/219_benchmarking_best_practice/) 등 다양한 기법을 상황에 맞게 조합한다.
> 2. **가치**: 사용자는 **자신이 원하는 것을 정확히 말하지 못하므로**, 다양한 도출 기법으로 <strong>숨겨진 요구(Hidden Requirements)</strong>를 발견해야 한다.
> 3. **판단 포인트**: 프로토타이핑은 <strong>시각적 확인→피드백</strong>이 빠르고, JAD는 <strong>다부서 합의</strong>에 강하며, 관찰(Ethnography)은 <strong>실제 업무 흐름</strong>을 파악하는 데 최적이다.

---

## Ⅰ. 개요 및 필요성

요구사항 도출은 RE 5단계 중 가장 창의적이고 사람 중심적인 단계이다. "Henry Ford가 고객에게 원하는 것을 물었다면 '더 빠른 말'이라고 했을 것"이라는 말처럼, 사용자는 현재의 도구 프레임 안에서 생각한다. 도출 기법의 핵심은 이 한계를 깨고 진짜 필요(Needs)를 찾아내는 것이다.

도출의 어려움은 세 가지 유형의 요구 문제에서 온다. <strong>암묵적 요구(Tacit)</strong>는 사용자가 너무 당연해서 말하지 않는 요구다("당연히 버튼을 클릭하면 반응해야 하지"). <strong>불명확한 요구(Unclear)</strong>는 사용자가 원하는 것을 막연하게만 아는 경우다("뭔가 더 직관적이면 좋겠어"). <strong>미지의 요구(Unknown)</strong>는 사용자도 아직 깨닫지 못한 요구로, 프로토타입이나 관찰을 통해 발견된다.

효과적 도출을 위해서는 단일 기법이 아닌 조합이 필요하다. 인터뷰로 심층 요구를 파악하고, JAD 워크숍으로 다부서 합의를 끌어내며, 프로토타이핑으로 시각적 피드백을 받고, 관찰로 암묵적 요구를 발견하는 식으로 목적에 맞게 기법을 조합한다. 각 기법의 강점과 약점을 알고 상황에 맞게 선택하는 능력이 RE 전문가의 핵심 역량이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">도출 기법 선택 의사결정 흐름:</div>
<div class="kb-diagram-note">이해관계자 수가 적고 핵심 의사결정자?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">인터뷰</div><div class="kb-diagram-note">심층 1:1 대화</div></div>
<div class="kb-diagram-note">다부서 이해관계 충돌이 예상됨?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">JAD 워크숍</div><div class="kb-diagram-note">구조화된 그룹 합의</div></div>
<div class="kb-diagram-note">UI/UX 요구가 중심이고 사용자가 표현 어려움?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">프로토타이핑</div><div class="kb-diagram-note">시각적 피드백 수집</div></div>
<div class="kb-diagram-note">초기 아이디어 탐색, 창의적 요구 발굴?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">브레인스토밍</div><div class="kb-diagram-note">비판 없는 발산</div></div>
<div class="kb-diagram-note">현장 업무 프로세스, 암묵적 요구 발견?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">쉐도잉/관찰</div><div class="kb-diagram-note">현장 직접 관찰</div></div>
<div class="kb-diagram-note">대규모 사용자 의견 수집?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">설문</div><div class="kb-diagram-note">구조화된 질문지</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 도출 기법은 의사의 <strong>문진 도구(청진기·X-ray·혈액 검사·심전도)</strong>이다. 증상마다 다른 도구를 쓰듯, 요구의 성격에 따라 다른 도출 기법을 선택한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 도출 기법 상세 비교

| 기법 | 형식 | 인원 | 시간 | 강점 | 약점 | 최적 상황 |
|:---|:---|:---|:---|:---|:---|:---|
| **인터뷰** | 1:1 대화 | 1~3명 | 1~2시간 | 심층 이해, 유연 | 편향, 시간 소요 | 핵심 이해관계자 |
| **JAD 워크숍** | 그룹 구조화 | 5~15명 | 반나절~2일 | 다부서 합의 | 퍼실리테이터 의존 | 이해관계 충돌 |
| **브레인스토밍** | 자유 발산 | 5~10명 | 1~2시간 | 창의적 요구 | 비체계적 | 초기 탐색 |
| **프로토타이핑** | 시각화 | 2~5명 | 수일 | 숨겨진 요구 | 프로토타입 집착 | UI/UX 요구 |
| **쉐도잉/관찰** | 현장 관찰 | 1~2명 | 수시간~수일 | 암묵적 요구 | 비용·시간 | 복잡한 업무 |
| **설문** | 구조화 질문지 | 수십~수백명 | 1~2주 | 광범위 수집 | 깊이 부족 | 대규모 사용자 |
| **포커스 그룹(FGI)** | 그룹 심층 인터뷰 | 6~12명 | 2~3시간 | 상호 자극 | 지배 발언자 위험 | 사용자 경험 탐색 |
| **벤치마킹** | 경쟁사 분석 | 분석팀 | 수주 | 현실적 기준 | 맹목적 모방 위험 | 기준 수치 설정 |

### 인터뷰 기법 상세



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">인터뷰 유형:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구조화 인터뷰: 사전 정해진 질문 목록</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장점: 일관성, 비교 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단점: 유연성 부족, 새로운 발견 어려움</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비구조화 인터뷰: 자유로운 대화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장점: 깊이 있는 탐색, 예상 외 발견</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단점: 방향 잃기 쉬움, 비교 어려움</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">반구조화 인터뷰: 핵심 질문 + 자유 탐색 (권장)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장점: 일관성 + 유연성 균형</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단점: 퍼실리테이터 역량 필요</div></div>
<div class="kb-diagram-note">핵심 질문 유형 (5 Ws):</div>
<div class="kb-diagram-tree-item" style="--depth:1">What: 현재 어떻게 하고 있나요?</div>
<div class="kb-diagram-tree-item" style="--depth:1">Why: 그렇게 하는 이유가 무엇인가요?</div>
<div class="kb-diagram-tree-item" style="--depth:1">What if: 이 기능이 없다면 어떻게 하나요?</div>
<div class="kb-diagram-tree-item" style="--depth:1">How: 성공 여부를 어떻게 판단하나요?</div>
<div class="kb-diagram-tree-item" style="--depth:1">When: 언제 가장 불편함을 느끼나요?</div>
</div>
</div>



### JAD (Joint Application Development) 프로세스

IBM이 1977년 개발한 그룹 기반 요구 도출 기법이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">JAD 세션 구조:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">참여자: 이해관계자 + 개발자 + 퍼실리테이터</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 킥오프 (범위 및 목표 설정)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 현재 상태(As-Is) 분석</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 미래 상태(To-Be) 설계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 요구사항 합의 및 우선순위화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. 검증 및 서명</div></div>
<div class="kb-diagram-note">퍼실리테이터 역할:</div>
<div class="kb-diagram-tree-item" style="--depth:1">발언 기회 균등 보장</div>
<div class="kb-diagram-tree-item" style="--depth:1">갈등 중재</div>
<div class="kb-diagram-tree-item" style="--depth:1">논의 결과 실시간 문서화</div>
<div class="kb-diagram-tree-item" style="--depth:1">시간 관리</div>
</div>
</div>



### 도출 단계별 숨겨진 요구 발견 기법

| 요구 유형 | 발생 이유 | 발견 기법 |
|:---|:---|:---|
| **암묵적 요구** | 너무 당연해서 말 안 함 | 관찰, 쉐도잉, Contextual Inquiry |
| **불명확한 요구** | 막연히 알지만 표현 못 함 | 프로토타이핑, 시나리오 기법 |
| **미지의 요구** | 아직 인식하지 못함 | 페르소나+시나리오, Design Thinking |
| **상충하는 요구** | 이해관계자 간 충돌 | JAD 워크숍, 갈등 해결 기법 |
| **미래 요구** | 현재는 없지만 곧 필요 | 시장 분석, 벤치마킹, 트렌드 분석 |

- **📢 섹션 요약 비유**: 도출 기법은 보물찾기 도구다. 인터뷰는 지도(핵심 경로), JAD는 팀 작전 회의, 브레인스토밍은 무작위 발굴, 관찰은 현장 탐사다. 보물(숨겨진 요구)의 위치에 따라 도구를 달리 써야 한다.

---

## Ⅲ. 비교 및 연결

### 도출 기법 선택 매트릭스

| 상황 | 최적 기법 | 보조 기법 |
|:---|:---|:---|
| 이해관계자 < 5명 | 인터뷰 | 설문 |
| 다부서 이해 충돌 | JAD 워크숍 | 브레인스토밍 |
| UI/UX 요구 불명확 | 프로토타이핑 | FGI |
| 복잡한 업무 프로세스 | 쉐도잉/관찰 | Contextual Inquiry |
| 대규모 사용자 의견 | 설문 | FGI |
| 혁신적 기능 탐색 | 브레인스토밍 | Design Thinking |
| NFR 수치 기준 설정 | 벤치마킹 | 전문가 자문 |

### 전통적 도출 vs AI 보조 도출 비교

| 항목 | 전통적 도출 | AI 보조 도출 |
|:---|:---|:---|
| **속도** | 수주~수개월 | 수일 |
| **범위** | 이해관계자 접촉 가능 범위 | 빅데이터(리뷰, 지원티켓) 분석 |
| **깊이** | 전문가 판단 높음 | 패턴 발견에 강점 |
| **비용** | 인건비 높음 | 초기 설정 후 효율적 |
| **신뢰성** | 이해관계자 직접 확인 | 해석 오류 위험 |

- **📢 섹션 요약 비유**: 도출 기법 선택은 낚시 방법 선택과 같다. 큰 고기(핵심 이해관계자 요구)는 낚싯대(인터뷰), 많은 양(대규모 의견)은 그물(설문), 바닥의 게(암묵적 요구)는 통발(관찰)로 잡는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **이해관계자 식별 완료**: 모든 유형의 이해관계자(사용자, 관리자, 운영자, 보안 담당)가 식별되었는가?
2. **기법 다양화**: 최소 2~3가지 이상의 도출 기법을 조합하여 사용하였는가?
3. **숨겨진 요구 탐색**: 암묵적·불명확·미지의 요구를 발견하기 위한 기법(관찰, 프로토타이핑)을 사용하였는가?
4. **도출 결과 문서화**: 모든 도출 결과가 정리되어 분석 단계 입력으로 제공되는가?
5. **JAD 또는 워크숍**: 다부서 합의가 필요한 경우 구조화된 워크숍을 진행하였는가?
6. **도출 완료 기준**: 언제 도출을 멈출지 기준(포화점: 새로운 요구가 더 이상 나오지 않음)이 있는가?

### 안티패턴

- **인터뷰 편향(Interview Bias)**: 인터뷰어가 기대하는 답변을 유도하는 질문을 하는 패턴. "이 기능이 있으면 좋겠죠?"는 유도 질문이다. "현재 이 업무를 어떻게 수행하나요?"와 같은 개방형 질문을 사용해야 한다.

- **프록시 도출(Proxy Elicitation)**: 실제 사용자 대신 관리자나 PO(Product Owner)만 인터뷰하는 패턴. 관리자는 현장 업무의 실제 어려움을 모르는 경우가 많다. 최종 사용자에게 직접 접근하는 것이 필수이다.

- **하나의 기법 고집**: 프로젝트 내내 인터뷰만 사용하거나 설문만 사용하는 패턴. 각 기법은 서로 다른 유형의 요구를 발견하므로, 복수의 기법 조합이 필요하다.

- **도출 포화 무시(Ignoring Saturation)**: 이미 새로운 요구가 나오지 않는 상황에서 계속 도출 활동을 반복하는 패턴. "포화점(Saturation Point)"에 도달하면 분석 단계로 전환해야 한다.

- **📢 섹션 요약 비유**: 도출 안티패턴은 낚시 실수와 같다. 유도 질문은 가짜 미끼로 원하는 고기만 잡으려는 것, 프록시 도출은 바다를 보지 않고 수족관 주인에게 바다 생물을 물어보는 것이다.

---

## Ⅴ. 기대효과 및 결론

체계적 도출 기법 적용은 요구사항 품질을 직접적으로 높인다. 연구에 따르면 프로토타이핑을 활용한 도출은 문서 기반 도출 대비 30~50% 더 많은 요구사항을 발견한다. JAD 워크숍은 이해관계자 합의를 개별 인터뷰 대비 60% 빠르게 달성하는 것으로 알려져 있다.

도출 기법의 조합 사용이 핵심이다. 핵심 이해관계자 인터뷰(심층)→JAD 워크숍(합의)→프로토타이핑(검증)→관찰(암묵적 요구 보완)의 순서로 진행하면 요구 누락을 최소화할 수 있다. 특히 Agile 환경에서는 매 스프린트 시작 시 백로그 정제(Backlog Refinement)가 지속적인 미니 도출 활동으로 기능한다.

미래에는 AI 기반 도출 보조 도구가 확산될 것이다. 고객 리뷰, 지원 티켓, SNS 데이터에서 패턴을 분석하여 잠재 요구를 제시하는 도구, 인터뷰 내용을 자동 전사하고 요구사항 후보를 추출하는 도구가 이미 개발 중이다. 그러나 이해관계자와의 신뢰 형성, 갈등 중재, 맥락 이해는 인간 전문가의 역할로 남을 것이다.

- **📢 섹션 요약 비유**: 도출 기법 투자는 보험이다. 개발 시작 전 충분히 도출하면, 개발 중 "이건 제가 원한 게 아닌데요"라는 비용이 발생하지 않는다. 1시간의 인터뷰가 1주의 재개발을 막는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **인터뷰** | 1:1 심층 도출, 핵심 이해관계자 |
| **JAD** | 다부서 합의 워크숍, IBM 개발 (1977) |
| **프로토타이핑** | 시각적 피드백, UI/UX 요구 |
| **관찰/쉐도잉** | 암묵적 요구 발견, 현장 중심 |
| **Hidden Requirements** | 도출의 핵심 목표 |
| **포화점 (Saturation)** | 도출 종료 기준 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 인터뷰 (~1990s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">JAD 워크숍 체계화 (IBM 1977 → 1990s 확산)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">프로토타이핑 기반 도출 (2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Design Thinking 통합 (Empathy, Define, 2010s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Contextual Inquiry + 관찰 (UX 연구 방법론화)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI 도출 보조 ── 회의록 자동 분석</div>
<div class="kb-diagram-tree-item" style="--depth:8">고객 데이터 패턴 추출</div>
<div class="kb-diagram-tree-item" style="--depth:8">챗봇 기반 요구 수집</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 요구 도출은 의사의 <strong>문진</strong>이에요. "어디가 아프세요?" 물어봐요.
2. 청진기(인터뷰), X-ray(프로토타이핑) 등 <strong>여러 도구</strong>를 같이 써요.
3. 환자가 <strong>말 못 하는 증상(숨겨진 요구)</strong>도 찾아내야 좋은 의사예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 973

← **이전**: [134. 요구사항 공학 프로세스 - 도출→분석→명세→검증→관리 상세](/knowledge-base/studynote/04_software_engineering/03_design_architecture/134_requirements_engineering_process/)
**다음**: [136. 브레인스토밍 & JAD - 그룹 기반 요구 도출 기법](/knowledge-base/studynote/04_software_engineering/03_design_architecture/136_brainstorming_jad_requirements/) →

---
