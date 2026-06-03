+++
title = "138. 프로토타이핑 - Throwaway vs Evolutionary 프로토타입"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로토타이핑은 <strong>불완전한 초기 모델을 빠르게 만들어 사용자 피드백을 얻는</strong> 요구 도출·검증 기법이며, Throwaway(폐기형)과 Evolutionary(진화형)로 구분된다.
> 2. **가치**: SRS 문서만으로는 사용자가 "이게 내가 원하는 것인지" 판단하기 어렵지만, 프로토타입으로 <strong>시각적으로 확인하면 숨겨진 요구를 80%+ 더 발견</strong>할 수 있다.
> 3. **판단 포인트**: Throwaway(빠르게 만들고 버림, 요구 확인 목적)는 초기 요구 도출에, Evolutionary(계속 발전시켜 최종 제품화)는 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)·반복 개발에 적합하다.

---

## Ⅰ. 개요 및 필요성

프로토타이핑의 역사는 제조업에서 시작되었다. 자동차, 항공기, 건축 분야에서는 오래전부터 실제 제품 생산 전에 축소 모델이나 시제품을 만들어 설계를 검증해왔다. 소프트웨어 분야에서는 1970~80년대 Boehm, Gomaa 등의 연구자들이 소프트웨어 프로토타이핑의 이론적 기반을 마련했고, 1990년대 GUI(그래픽 사용자 인터페이스)의 보급으로 시각적 프로토타이핑이 폭발적으로 성장했다.

프로토타이핑이 필요한 이유는 **요구사항의 문서 기반 이해 한계** 때문이다. SRS 문서에 아무리 자세히 기술해도, 사용자는 실제로 화면을 보고 클릭해봐야 "이게 내가 원하는 것"인지 판단할 수 있다. 연구에 따르면 문서 기반 요구 리뷰에서 발견되는 결함은 약 20%, 프로토타입 기반 리뷰에서는 약 65%로 프로토타이핑이 훨씬 효과적이다.

Throwaway와 Evolutionary 프로토타입의 선택은 프로젝트 성격에 따라 달라진다. 안전 필수 시스템(항공, 의료)이나 요구가 매우 불확실한 경우 Throwaway가 적합하다. 빠른 시장 출시가 목표이고, Agile 방식으로 개발하며, 기술 역량이 높은 팀이라면 Evolutionary가 효율적이다. 두 방식을 혼합한 "선 Throwaway, 후 Evolutionary" 접근도 일반적이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">프로토타입 유형 스펙트럼:</div>
<div class="kb-diagram-note">빠른 폐기 ← → 점진적 완성</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Throwaway</div><div class="kb-diagram-node">Evolutionary</div></div>
<div class="kb-diagram-note">요구 확인 점진적 제품화</div>
<div class="kb-diagram-note">낮은 코드 품질 높은 코드 품질</div>
<div class="kb-diagram-note">폭포수 초기 Agile/반복</div>
<div class="kb-diagram-note">수일 내 제작 스프린트마다 발전</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Lo-Fi 종이</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Hi-Fi Figma</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">기능 프로토</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">MVP</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">제품</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: Throwaway는 **클레이 모형(전시 후 폐기)**, Evolutionary는 <strong>점토 조각(계속 다듬어 완성)</strong>이다. 목적이 다르면 접근법도 달라야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Throwaway vs Evolutionary 전면 비교

| 항목 | Throwaway 프로토타입 | Evolutionary 프로토타입 |
|:---|:---|:---|
| **목적** | 요구사항 확인 후 폐기 | 점진적으로 최종 제품화 |
| **코드 품질** | 낮음 (빠른 구현 우선) | 높음 (제품 수준 유지) |
| **사용 기간** | 단기 (수일~수주) | 장기 (제품 수명 내내) |
| **기술 부채** | 폐기하므로 무관 | 최소화 필요 |
| **방법론** | 폭포수 초기 단계 | Agile·반복 개발 |
| **적합 상황** | 요구 불확실, 새로운 도메인 | 요구 변화 잦음, 빠른 출시 |
| **위험** | 사용자가 폐기 거부 | 기술 부채 누적 |
| **산출물** | 요구 피드백, 폐기 | 동작하는 제품의 점진적 증분 |

### Throwaway 프로타입 개발 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Throwaway 프로토타입 사이클:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1</div><div class="kb-diagram-note">불확실한 요구 식별</div></div>
<div class="kb-diagram-note">→ 어떤 UI 레이아웃이 더 직관적인가?</div>
<div class="kb-diagram-note">→ 사용자가 이 워크플로우를 이해할 수 있는가?</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2</div><div class="kb-diagram-note">빠른 프로토타입 제작 (Lo-Fi or Hi-Fi)</div></div>
<div class="kb-diagram-note">→ Figma/발삼이크로 수시간~수일 내 제작</div>
<div class="kb-diagram-note">→ 실제 데이터 불필요, 더미 데이터 사용</div>
<div class="kb-diagram-note">→ 코드 품질 무시 (빠른 구현 우선)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3</div><div class="kb-diagram-note">사용자 테스트 및 피드백 수집</div></div>
<div class="kb-diagram-note">→ 5~8명의 사용자로 사용성 테스트</div>
<div class="kb-diagram-note">→ "생각하면서 사용하세요(Think-aloud)" 프로토콜</div>
<div class="kb-diagram-note">→ 클릭 패턴, 혼란 포인트 기록</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4</div><div class="kb-diagram-note">피드백 분석 및 요구 수정</div></div>
<div class="kb-diagram-note">→ 숨겨진 요구 발견</div>
<div class="kb-diagram-note">→ SRS/User Story 업데이트</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">5</div><div class="kb-diagram-note">프로토타입 폐기 (핵심!)</div></div>
<div class="kb-diagram-note">→ 코드/디자인 파일 보관하지 않음</div>
<div class="kb-diagram-note">→ 검증된 요구로 올바른 구현 시작</div>
</div>
</div>



### Evolutionary 프로토타입 개발 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Evolutionary 프로토타입 사이클 (= Agile 스프린트):</div>
<div class="kb-diagram-note">스프린트 1: 핵심 기능 프로토타입 (기본 로그인, 메인 화면)</div>
<div class="kb-diagram-note">→ 사용자 피드백 수집</div>
<div class="kb-diagram-note">→ 다음 스프린트 계획에 반영</div>
<div class="kb-diagram-note">스프린트 2: 기능 확장 (프로파일, 기본 검색)</div>
<div class="kb-diagram-note">→ 코드 품질 유지 (리팩토링 포함)</div>
<div class="kb-diagram-note">→ 테스트 자동화 적용</div>
<div class="kb-diagram-note">스프린트 3: 성능·보안 강화</div>
<div class="kb-diagram-note">→ NFR 달성 확인</div>
<div class="kb-diagram-note">→ 사용성 테스트</div>
<div class="kb-diagram-note">...지속 반복...</div>
<div class="kb-diagram-note">최종: 완성된 제품 (처음 프로토타입이 발전한 것)</div>
</div>
</div>



### 프로토타입 관련 개념 계층 구조

| 개념 | 정의 | 충실도 | 제작 시간 |
|:---|:---|:---|:---|
| **스케치** | 손으로 그린 화면 | 극저 | 분 |
| **와이어프레임** | 레이아웃만 표현, 색상·디자인 없음 | 낮음 | 시간 |
| **목업(Mockup)** | 디자인 완성, 상호작용 없음 | 중간 | 일 |
| **인터랙티브 프로토타입** | 클릭 가능, 실제와 유사 | 높음 | 일~주 |
| **MVP** | 최소 기능 실제 동작 제품 | 최고 | 주~개월 |

- **📢 섹션 요약 비유**: 프로토타이핑은 요리사의 시식 테스트다. Throwaway는 "맛 테스트용 샘플(다 먹히면 폐기)", Evolutionary는 "점차 레시피를 개선하여 완성 메뉴 출시"다.

---

## Ⅲ. 비교 및 연결

### 프로토타이핑 vs 다른 요구 도출 기법 비교

| 항목 | 인터뷰 | JAD | 프로토타이핑 | 관찰 |
|:---|:---|:---|:---|:---|
| **요구 유형** | 명시적 요구 | 그룹 합의 | 시각적·암묵적 | 암묵적 |
| **피드백 속도** | 보통 | 느림 | 매우 빠름 | 느림 |
| **비용** | 낮음 | 중간 | 중간~높음 | 높음 |
| **발견 요구 유형** | 의식된 요구 | 다부서 합의 요구 | 숨겨진 UI/UX | 업무 프로세스 |

### 프로토타이핑 도구 진화

| 시기 | 도구 | 충실도 |
|:---|:---|:---|
| ~2000s | 종이, 화이트보드 | Lo-Fi |
| 2008 | Balsamiq | Lo-Fi 디지털 |
| 2010 | Axure RP | Mid-Fi 인터랙티브 |
| 2016 | InVision | Hi-Fi 인터랙티브 |
| 2016~ | Figma | Hi-Fi 협업 실시간 |
| 2020~ | No-Code (Bubble, Webflow) | 실제 동작 |
| 2023~ | AI 코드 생성 (v0.dev) | 코드→UI 자동화 |

### 프로토타입과 연결 개념

| 개념 | 관계 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/139_prototyping_fidelity_levels/">Lo-Fi/Hi-Fi 프로토타입</a></strong> | 충실도 단계 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/">MVP</a></strong> | Evolutionary 프로토타입의 Lean Startup 버전 |
| **사용성 테스트** | 프로토타입 검증 기법 |
| **스파이크 (Agile)** | 기술 불확실성 탐색용 Throwaway 코드 |

- **📢 섹션 요약 비유**: Throwaway는 건물 착공 전 임시 가설 건물(견본 주택), Evolutionary는 처음부터 실제 입주를 목표로 짓되 층마다 확인하며 올라가는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **목적 명확화**: 이 프로토타입의 목적이 "요구 확인"(Throwaway)인지 "점진적 제품화"(Evolutionary)인지 결정하였는가?
2. **Throwaway 코드 품질 허용**: Throwaway 프로토타입에 과도한 코드 품질을 요구하지 않는가?
3. **폐기 규칙**: Throwaway 프로타입을 사용 후 반드시 폐기하는 규칙이 있는가?
4. **충실도 단계 선택**: 현재 단계에 맞는 Lo-Fi/Mid-Fi/Hi-Fi가 선택되었는가?
5. **사용자 테스트 계획**: 프로토타입으로 어떤 사용자에게 어떤 방식으로 피드백을 수집할지 계획되었는가?
6. **Evolutionary 품질 유지**: Evolutionary 방식에서 기술 부채가 누적되지 않도록 스프린트마다 리팩토링 시간이 확보되었는가?

### 안티패턴

- **Throwaway의 영속화(Prototype Becomes Product)**: "임시로 만들었는데 그냥 쓰자"며 Throwaway 품질의 코드가 실 제품으로 사용되는 패턴. 코드 품질·보안·성능이 모두 취약한 상태로 운영 환경에 올라가게 된다. Throwaway는 반드시 폐기하거나 전면 재작성해야 한다.

- **프로토타입 집착(Prototype Fixation)**: 사용자가 초기 프로토타입의 UI에 집착하여 더 나은 방향으로의 변경을 거부하는 패턴. Lo-Fi 프로토타입은 의도적으로 완성도를 낮춰 "이건 임시입니다"라는 인식을 심어줘야 한다.

- **과도한 완성도**: Throwaway 목적의 프로토타입에 2주 이상 투자하는 패턴. 목적이 "요구 확인"이라면 수시간~수일이면 충분하다. 완성도보다 속도가 중요하다.

- **피드백 없는 프로토타입**: 프로토타입을 만들고 내부 검토만 하는 패턴. 실제 사용자에게 보여주지 않으면 프로토타이핑의 핵심 가치가 없다. 최소 5명의 실제 사용자 테스트가 필요하다.

- **📢 섹션 요약 비유**: Throwaway의 영속화는 공사 현장의 임시 가설 건물에 사람을 살게 하는 것이다. 안전 기준을 전혀 갖추지 않은 건물에 입주하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

프로토타이핑은 요구 발견 효율성을 크게 높인다. Nielsen Norman Group의 연구에 따르면 사용성 테스트를 통한 프로토타입 검증으로 개발 전에 사용성 문제의 85%를 발견할 수 있다. Throwaway 프로타입에 투자한 수일의 시간은, 개발 완료 후 발견하는 요구 오류 수정 비용(수주~수개월)을 막아준다.

Evolutionary 프로타이핑은 Agile의 핵심 가치인 "동작하는 소프트웨어"를 실현한다. 매 스프린트마다 사용자가 실제로 사용 가능한 증분(Increment)을 제공하여 지속적인 피드백을 받고, 이를 다음 스프린트에 반영한다. MVP(최소 기능 제품)는 Evolutionary 프로토타입의 린 스타트업(Lean Startup) 버전으로, 시장에서 가설을 검증하는 최소 단위이다.

미래에는 AI 기반 프로토타이핑 도구가 일반화될 것이다. 이미 v0.dev, Galileo AI 같은 도구가 텍스트 설명에서 UI 코드를 자동 생성하고 있으며, Figma에는 AI 기반 레이아웃 제안이 통합되었다. 손으로 그린 스케치를 찍으면 즉시 동작하는 UI 코드가 나오는 시대가 열렸다. 이는 Throwaway 프로토타입 제작 비용을 더욱 낮추어 더 빠른 요구 검증이 가능해질 것이다.

- **📢 섹션 요약 비유**: 프로토타이핑은 요리 시식 테스트다. 주방에서 아무리 완벽한 레시피를 작성해도, 손님이 먹어봐야 "맛이 있다/없다"를 알 수 있다. 일단 맛보이고 피드백을 받는 것이 가장 빠른 완성의 길이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Throwaway** | 폐기형 프로토타입, 요구 확인 후 폐기 |
| **Evolutionary** | 진화형 프로토타입, Agile 점진적 개발 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/139_prototyping_fidelity_levels/">Lo-Fi/Hi-Fi</a></strong> | 프로토타입 충실도 단계 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/">MVP</a></strong> | 최소 기능 제품, Lean Startup |
| **사용성 테스트** | 프로토타입으로 UI/UX 검증 |
| **Figma** | 현재 표준 Hi-Fi 프로토타입 도구 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">종이 프로토타입 (~2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">디지털 Lo-Fi (Balsamiq, 2008)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">인터랙티브 Mid-Fi (Axure, 2005~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hi-Fi 협업 도구 (Figma, 2016) ← 실시간 협업 혁신</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">No-Code 프로토타입 (Bubble, Webflow, 2018~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI 프로토타입 ── 텍스트→UI 자동 생성 (v0.dev)</div>
<div class="kb-diagram-tree-item" style="--depth:7">스케치→코드 변환 (Galileo AI)</div>
<div class="kb-diagram-tree-item" style="--depth:7">Figma 플러그인 AI 레이아웃</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Throwaway는 <strong>클레이 모형</strong>이에요. 확인하고 **버려요**.
2. Evolutionary는 <strong>점토 조각</strong>이에요. 계속 <strong>다듬어서 완성</strong>해요.
3. 먼저 대충 만들어 보여주면 "이건 아니에요!" 를 **빨리** 알 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 138 / 973

← **이전**: [137. 페르소나 분석 & 모델링 - 사용자 중심 요구 도출](/knowledge-base/studynote/04_software_engineering/03_design_architecture/137_persona_analysis_modeling/)
**다음**: [139. 프로토타입 충실도 (Fidelity Levels) - Lo-Fi·Mid-Fi·Hi-Fi](/knowledge-base/studynote/04_software_engineering/03_design_architecture/139_prototyping_fidelity_levels/) →

---
