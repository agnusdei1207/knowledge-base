+++
title = "139. 프로토타입 충실도 (Fidelity Levels) - Lo-Fi·Mid-Fi·Hi-Fi"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) 충실도는 **Lo-Fi(종이 스케치)·Mid-Fi(와이어프레임)·Hi-Fi(인터랙티브 목업)** 3단계로 구분되며, 프로젝트 단계·목적에 따라 적절한 수준을 선택한다.
> 2. **가치**: 초기에 Hi-Fi를 만들면 <strong>수정 비용이 크고 피드백이 디자인 세부사항에 매몰</strong>되므로, Lo-Fi로 시작하여 점진적으로 충실도를 높이는 것이 효율적이다.
> 3. **판단 포인트**: Lo-Fi(5분 제작, 구조 확인)→Mid-Fi(Figma 와이어프레임)→Hi-Fi(Figma 인터랙티브, 실제와 유사)의 순서로 진행하며, 각 단계에서 다른 유형의 피드백을 수집한다.

---

## Ⅰ. 개요 및 필요성

프로토타입 충실도(Fidelity)는 프로토타입이 최종 제품과 얼마나 유사한가를 나타내는 척도이다. 1980~90년대 HCI(인간-컴퓨터 상호작용) 분야에서 프로토타입 충실도 개념이 체계화되었으며, 오늘날 UX 설계의 핵심 방법론으로 자리 잡았다.

충실도 단계를 구분하는 이유는 **피드백 효율성** 때문이다. Lo-Fi 프로토타입에서는 사용자가 색상이나 아이콘 등 디자인 세부사항에 신경 쓰지 않고 "이 화면 구조가 맞는가", "이 정보 흐름이 자연스러운가"에 집중할 수 있다. 반면 Hi-Fi 프로토타입에서는 "버튼 색이 마음에 안 들어요" 같은 디자인 피드백도 함께 수집된다. 충실도를 단계적으로 높임으로써 각 단계에서 가장 중요한 의사결정에 집중할 수 있다.

또한 충실도는 <strong>제작 비용과 정비례</strong>한다. Lo-Fi는 종이와 연필로 5분 안에 만들 수 있지만, Hi-Fi Figma 프로토타입은 숙련된 디자이너가 며칠을 투자해야 한다. 따라서 초기에 방향이 불확실할 때는 Lo-Fi로 빠르게 탐색하고, 방향이 확정되면 Hi-Fi로 정밀화하는 전략이 비용 효율적이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">충실도 단계별 비교:</div>
<div class="kb-diagram-note">Lo-Fi Mid-Fi Hi-Fi</div>
<div class="kb-diagram-note">충실도: ★☆☆☆☆ ★★★☆☆ ★★★★★</div>
<div class="kb-diagram-note">제작시간: 분 시간 일</div>
<div class="kb-diagram-note">도구: 종이·화이트보드 Figma 와이어프레임 Figma 인터랙티브</div>
<div class="kb-diagram-note">목적: 구조·흐름 확인 레이아웃 확인 UX 검증</div>
<div class="kb-diagram-note">색상: 없음 회색 계열 완성 디자인</div>
<div class="kb-diagram-note">상호작용: 없음 최소 클릭·애니메이션</div>
<div class="kb-diagram-note">사용자: 이해관계자 중간 사용자 실 사용자</div>
<div class="kb-diagram-note">피드백: 구조·정보 흐름 레이아웃·네비 UX·사용성</div>
<div class="kb-diagram-note">비용: ↑낮음 높음↑</div>
<div class="kb-diagram-note">속도: ↑빠름 느림↑</div>
</div>
</div>



- **📢 섹션 요약 비유**: Lo-Fi는 연필 스케치, Mid-Fi는 밑그림(연필+윤곽), Hi-Fi는 완성 유화이다. 유화부터 그리기 시작하면 구도를 바꿀 때 모든 것을 다시 그려야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Lo-Fi 프로토타입 상세

```text
Lo-Fi 프로토타입 특징:

[도구] 종이, 포스트잇, 화이트보드, 발삼이크(Balsamiq)
[시간] 5분~2시간
[팀원] 1~3명, 기술 지식 불필요
[목적]
  - 정보 구조(IA: Information Architecture) 확인
  - 주요 화면 흐름(User Flow) 검증
  - 초기 아이디어 탐색
  - 빠른 피드백 수집

[장점]
  - 극도로 빠른 제작
  - 수정이 즉각적 (지우고 다시 그리기)
  - 사용자가 "임시"임을 인식하여 구조에 집중
  - 완성도 비교 불필요 (경쟁 방어 심리 없음)

[단점]
  - 실제와 차이가 커서 상호작용 검증 불가
  - 기술 발전으로 Mid-Fi와 경계 모호해짐
```

Lo-Fi 프로토타입 예시 (화면 스케치):


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">로고</div><div class="kb-diagram-node">검색창   🔍</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">헤더</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">배너 이미지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">추천 상품</div><div class="kb-diagram-cell">← 섹션 제목</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">상품1</div><div class="kb-diagram-node">상품2</div><div class="kb-diagram-node">상품3</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">상품 카드 (박스)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">홈</div><div class="kb-diagram-node">검색</div><div class="kb-diagram-node">장바구니</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">탭 바</div></div>
</div>
</div>



### Mid-Fi 프로토타입 상세

| 특성 | 내용 |
|:---|:---|
| **도구** | Figma 와이어프레임, Axure, Adobe XD |
| **제작 시간** | 수시간~수일 |
| **충실도** | 레이아웃·네비게이션 완성, 디자인 미완성 |
| **색상** | 회색 계열 (Grayscale) |
| **상호작용** | 기본 클릭·페이지 이동 |
| **목적** | 레이아웃·네비게이션·정보 계층 검증 |
| **사용자** | 중간 수준 기술 사용자 |

### Hi-Fi 프로토타입 상세

| 특성 | 내용 |
|:---|:---|
| **도구** | Figma 인터랙티브, Principle, Framer |
| **제작 시간** | 수일~수주 |
| **충실도** | 실제와 거의 동일 (색상, 타이포, 아이콘) |
| **색상** | 최종 브랜드 색상 |
| **상호작용** | 클릭, 스크롤, 애니메이션, 마이크로인터랙션 |
| **목적** | 사용성 테스트, 이해관계자 승인, 개발팀 핸드오프 |
| **사용자** | 실제 타겟 사용자 |

### 충실도 단계 선택 의사결정



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">충실도 선택 의사결정 트리:</div>
<div class="kb-diagram-note">현재 단계는?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Lo-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Mid-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Hi-Fi</div></div>
<div class="kb-diagram-note">목적은?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Lo-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Mid-Fi or Hi-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Hi-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Hi-Fi</div></div>
<div class="kb-diagram-note">예산·시간 제약?</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Lo-Fi 또는 Mid-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">단계적 Lo-Fi→Mid-Fi→Hi-Fi</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Hi-Fi 직접</div></div>
</div>
</div>



### 단계별 수집 가능한 피드백 유형

| 피드백 유형 | Lo-Fi | Mid-Fi | Hi-Fi |
|:---|:---|:---|:---|
| **정보 구조(IA)** | 최적 | 좋음 | 보통 |
| **사용자 흐름(User Flow)** | 좋음 | 최적 | 최적 |
| **레이아웃** | 제한적 | 최적 | 좋음 |
| **상호작용·애니메이션** | 불가 | 제한적 | 최적 |
| **브랜드·디자인** | 불가 | 제한적 | 최적 |
| **접근성** | 제한적 | 보통 | 최적 |
| **수정 용이성** | 최고 | 높음 | 낮음 |

- **📢 섹션 요약 비유**: 충실도 단계는 요리 레시피 개발 과정이다. 재료 조합 탐색(Lo-Fi=간단 시식), 완성도 향상(Mid-Fi=시범 요리), 최종 검증(Hi-Fi=전문가 시식회). 첫 단계부터 최고급 레스토랑 수준 요리를 만들면 시행착오 비용이 폭발한다.

---

## Ⅲ. 비교 및 연결

### 충실도 관련 도구 생태계

| 도구 | 분류 | 특징 | 비용 |
|:---|:---|:---|:---|
| **종이·화이트보드** | Lo-Fi | 즉시 제작, 수정 용이 | 무료 |
| **Balsamiq** | Lo-Fi | 스케치 느낌 디지털 와이어프레임 | 유료 |
| **Figma (기본)** | Mid-Fi | 협업, 와이어프레임 템플릿 | 무료~유료 |
| **Miro** | Lo-Fi/Mid-Fi | 협업 화이트보드 | 무료~유료 |
| **Adobe XD** | Mid-Fi/Hi-Fi | CC 통합, 인터랙티브 | 유료 |
| **Figma (인터랙티브)** | Hi-Fi | 현재 표준, 개발 핸드오프 | 유료 |
| **Framer** | Hi-Fi | 코드 기반 고급 인터랙션 | 유료 |

### 충실도와 연결 개념

| 개념 | 충실도와의 관계 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/138_prototyping_throwaway_evolutionary/">Throwaway 프로토타입</a></strong> | 주로 Lo-Fi~Mid-Fi로 구현 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/138_prototyping_throwaway_evolutionary/">Evolutionary 프로토타입</a></strong> | 점진적으로 Hi-Fi로 발전 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/451_usability_test/">사용성 테스트</a></strong> | Hi-Fi로 최적 수행 |
| **디자인 시스템** | Hi-Fi 프로토타입의 기반 |
| **개발 핸드오프** | Hi-Fi → 개발팀 전달 |

- **📢 섹션 요약 비유**: Lo-Fi/Mid-Fi/Hi-Fi는 건물 설계의 개략도→기본 설계도→실시 설계도에 해당한다. 각 단계에서 다른 이해관계자(건축주/구조 엔지니어/시공사)가 검토하며 점점 구체화된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **단계별 충실도 계획**: 프로젝트 단계에 맞는 Lo-Fi→Mid-Fi→Hi-Fi 순서로 진행하는 계획이 있는가?
2. **Lo-Fi 시작 원칙**: 모든 새로운 기능은 Lo-Fi부터 시작하는가? (처음부터 Hi-Fi 금지)
3. **각 충실도별 목적 명확**: Lo-Fi에서는 구조, Mid-Fi에서는 레이아웃, Hi-Fi에서는 UX를 검증하는가?
4. **사용자 테스트 적절한 충실도**: 사용성 테스트는 Hi-Fi에서 수행하는가?
5. **디자인 피드백 단계 분리**: Lo-Fi 리뷰에서 "색상이 마음에 안 들어요" 같은 Hi-Fi 피드백을 막는 규칙이 있는가?
6. **핸드오프 준비**: Hi-Fi 완성 시 개발팀이 바로 구현할 수 있는 수준의 명세가 포함되었는가?

### 안티패턴

- **처음부터 Hi-Fi**: 요구가 확정되지 않은 상태에서 Hi-Fi 프로토타입을 먼저 만드는 패턴. 구조 변경 시 모든 화면의 디자인을 수정해야 하며, 사용자 피드백이 디자인 세부사항에 집중되어 구조적 문제를 놓친다.

- **Lo-Fi 영속화**: Lo-Fi로 빠르게 탐색한 후 Hi-Fi로 발전시키지 않고 Lo-Fi 단계에서 멈추는 패턴. 사용성 테스트와 이해관계자 승인을 위해서는 최소 Mid-Fi 이상이 필요하다.

- **충실도 단계 혼용**: 같은 프로토타입에서 일부는 Hi-Fi, 일부는 Lo-Fi인 불균형 상태. 사용자가 충실도가 높은 부분에만 집중하여 전체 구조를 파악하기 어렵다.

- **피드백 단계 혼동**: Lo-Fi 리뷰에서 "이 버튼 색이 마음에 안 들어요"처럼 Hi-Fi 피드백을 받아들이는 패턴. 퍼실리테이터가 "이 단계에서는 구조와 흐름만 피드백 주세요"라고 명확히 안내해야 한다.

- **📢 섹션 요약 비유**: 처음부터 Hi-Fi는 집 짓기 전에 완성 인테리어를 먼저 결정하는 것이다. 구조를 바꾸면 모든 인테리어를 다시 해야 한다. 구조(Lo-Fi)→레이아웃(Mid-Fi)→마감(Hi-Fi) 순서가 옳다.

---

## Ⅴ. 기대효과 및 결론

충실도 단계별 접근은 프로토타이핑의 비용 효율성을 극대화한다. Lo-Fi에서 구조 오류를 발견하면 5분의 수정으로 해결되지만, Hi-Fi에서 발견하면 수일의 재작업이 필요하다. Google Design Sprint 방법론은 단 5일 만에 Lo-Fi부터 Hi-Fi까지 단계를 거쳐 핵심 가설을 검증하는 완성된 프레임워크를 제시한다.

Figma가 프로토타이핑 도구의 표준이 된 2016년 이후, 충실도 경계가 더 유연해졌다. Figma의 컴포넌트 시스템은 Lo-Fi 와이어프레임에서 Hi-Fi 디자인으로 빠르게 전환할 수 있게 해주며, 동시에 여러 팀원이 실시간으로 협업할 수 있다. AI 기반 디자인 도구는 텍스트 설명으로 즉시 Hi-Fi 수준의 UI를 생성하여 충실도 단계 구분의 경계를 허물고 있다.

궁극적으로 충실도 선택의 원칙은 "필요한 결정을 가장 저렴하게 검증할 수 있는 수준"이다. 구조 결정은 Lo-Fi, 레이아웃 결정은 Mid-Fi, 사용성과 감성 품질(Look & Feel)은 Hi-Fi로 검증하는 단계적 접근이 시간과 비용 모두를 최적화한다.

- **📢 섹션 요약 비유**: 충실도 단계적 접근은 글쓰기의 초안→수정→교정 단계와 같다. 초안을 편집 없이 바로 출판하지 않듯, Lo-Fi 없이 Hi-Fi부터 시작하지 않는다. 각 단계가 존재하는 이유가 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Lo-Fi** | 종이 프로토타입, 구조·흐름 검증 |
| **Mid-Fi** | 와이어프레임, 레이아웃·네비게이션 |
| **Hi-Fi** | 인터랙티브 목업, 사용성·UX 검증 |
| **Figma** | 현재 표준 프로토타이핑 도구 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/451_usability_test/">사용성 테스트</a></strong> | Hi-Fi 프로토타입으로 수행 |
| **Design Sprint** | Lo-Fi→Hi-Fi 5일 프레임워크 |
| **개발 핸드오프** | Hi-Fi 완성 후 개발팀 전달 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">종이 프로토타입 (~2005) ── Lo-Fi의 원형</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Balsamiq (Lo-Fi 디지털, 2008)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Sketch (Mid-Fi 표준, 2010)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">InVision (Hi-Fi 인터랙티브, 2011)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Figma (Hi-Fi 실시간 협업, 2016) ← 현재 표준</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">No-Code 실제 동작 (Bubble, 2018~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI 프로토타입 ── 텍스트→UI 자동 생성</div>
<div class="kb-diagram-tree-item" style="--depth:7">스케치→Hi-Fi 코드 변환</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. Lo-Fi는 <strong>연필 스케치</strong>예요. 빠르게 그려서 <strong>대략적인 모양</strong>을 확인해요.
2. Hi-Fi는 <strong>완성 그림</strong>이에요. 실제처럼 **클릭도 되고 움직여요**.
3. 처음부터 완성 그림을 그리면 **수정이 어려우니** 스케치부터 시작해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 973

← **이전**: [138. 프로토타이핑 - Throwaway vs Evolutionary 프로토타입](/knowledge-base/studynote/04_software_engineering/03_design_architecture/138_prototyping_throwaway_evolutionary/)
**다음**: [140. 쉐도잉 & 관찰 기법 (Shadowing/Observation) - 현장 기반 요구 도출](/knowledge-base/studynote/04_software_engineering/03_design_architecture/140_shadowing_observation_technique/) →

---
