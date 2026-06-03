+++
title = "137. 페르소나 분석 & 모델링 - 사용자 중심 요구 도출"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 페르소나는 <strong>타겟 사용자 그룹을 대표하는 가상의 인물상</strong>을 상세히 정의(이름·나이·직업·목표·불편)하여, 모든 설계 의사결정에서 "이 사용자라면 어떻게 사용할까?"를 판단 기준으로 삼는 기법이다.
> 2. **가치**: "모든 사용자를 위해"는 결국 "아무도 위하지 않는" 설계가 되며, 페르소나로 <strong>핵심 사용자에 집중</strong>해야 UX 품질이 올라간다.
> 3. **판단 포인트**: 페르소나는 <strong>실제 사용자 조사(인터뷰·관찰) 기반</strong>이어야 하며, 가정만으로 만든 "가짜 페르소나"는 오히려 잘못된 의사결정을 유발한다.

---

## Ⅰ. 개요 및 필요성

페르소나(Persona)는 1999년 앨런 쿠퍼(Alan Cooper)가 그의 저서 "The Inmates Are Running the Asylum"에서 체계화한 사용자 중심 설계(UCD: User-Centered Design) 기법이다. 쿠퍼는 개발자들이 코드를 짜면서 무의식적으로 "나라면 이렇게 사용할 것"이라는 자기중심적 가정을 한다는 것을 발견했다. 페르소나는 이 문제를 해결하기 위해 실제 사용자 데이터를 기반으로 구체적인 인물상을 만들고, 이를 설계의 판단 기준으로 삼는 방법이다.

페르소나가 필요한 근본적 이유는 <strong>엘라스틱 사용자(Elastic User) 문제</strong>이다. 이해관계자들은 "우리 사용자"를 언급할 때 각자 다른 사용자를 머릿속에 그린다. 개발자는 IT 전문가, 영업팀은 기업 임원, 디자이너는 젊은 소비자를 생각한다. 이 불일치가 제품의 방향성 충돌로 이어진다. 페르소나는 모든 팀이 동일한 사용자 이미지를 공유하게 만들어 이 문제를 해결한다.

페르소나는 프로덕트의 모든 의사결정에서 판단 기준이 된다. "이 기능이 필요한가?"라는 질문을 "페르소나 김지연 씨라면 이 기능을 사용할 것인가?"로 구체화한다. 마케팅 메시지, UI 레이아웃, 기능 우선순위 결정, 지원 정책까지 페르소나가 있는 조직은 더 일관된 제품을 만든다. 구글, 아마존, 에어비앤비 등 주요 IT 기업들이 페르소나를 핵심 UX 도구로 활용한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">페르소나 예시:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페르소나: 김지연 (35세, 워킹맘)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">직업: IT 기업 PM, 기혼, 자녀 1명</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기술 수준: 중급 (스마트폰 능숙, 복잡한 설정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">어려워함)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">목표:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 업무 시간 내 효율적 일정 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 퇴근 후 가족과 시간 확보</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 팀원과 빠른 협업</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">불편함 (Pain Points):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 복잡한 UI로 원하는 기능 찾기 어려움</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 모바일에서 PC 기능 사용 불가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 알림이 너무 많아 중요 정보 놓침</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인용구:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"빠르게 쓰고 빠르게 나가고 싶어요.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">복잡하게 설정할 시간이 없어요."</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 페르소나는 <strong>영화 주인공 설정</strong>이다. 주인공이 "35세 워킹맘 PM"으로 명확하면 스토리(설계)가 일관된다. "모든 사람을 위한 영화"는 아무도 감동시키지 못한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 페르소나 구성 요소

| 구성 요소 | 내용 | 예시 |
|:---|:---|:---|
| **기본 정보** | 이름, 나이, 직업, 가족 | 김지연, 35세, IT 기업 PM |
| **기술 수준** | 디지털 리터러시, 사용 경험 | 스마트폰 능숙, 복잡한 설정 어려워함 |
| **목표 (Goals)** | 제품을 통해 달성하려는 것 | 효율적 일정 관리, 빠른 협업 |
| **불편 (Pain Points)** | 현재의 어려움, 좌절 포인트 | 복잡한 UI, 모바일 미지원 |
| **행동 패턴** | 사용 시간, 접근 방식 | 출퇴근 중 모바일, 점심 후 PC |
| **가치관** | 우선시하는 것 | 속도 > 기능 다양성 |
| **환경** | 사용 맥락, 기기 | 오피스+재택, iPhone + MacBook |
| **인용구** | 실제 발언 기반 | "복잡하게 설정할 시간이 없어요" |

### 페르소나 개발 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">페르소나 개발 4단계:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1단계</div><div class="kb-diagram-note">사용자 조사</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">정량 조사: 설문 (n &gt; 100), 사용 데이터 분석</div>
<div class="kb-diagram-tree-item" style="--depth:1">정성 조사: 인터뷰 (n = 10~20), 관찰, 다이어리 연구</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2단계</div><div class="kb-diagram-note">데이터 분석</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">인터뷰 전사 및 코딩</div>
<div class="kb-diagram-tree-item" style="--depth:1">패턴 및 클러스터 발견</div>
<div class="kb-diagram-tree-item" style="--depth:1">주요 속성 추출 (목표, 행동, 불편)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3단계</div><div class="kb-diagram-note">페르소나 생성</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">클러스터별 대표 페르소나 작성</div>
<div class="kb-diagram-tree-item" style="--depth:1">1차 페르소나 (Primary): 핵심 타겟</div>
<div class="kb-diagram-tree-item" style="--depth:1">2차 페르소나 (Secondary): 부가 타겟</div>
<div class="kb-diagram-tree-item" style="--depth:1">부정적 페르소나: 타겟이 아닌 사용자</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4단계</div><div class="kb-diagram-note">검증 및 공유</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">팀 내 공유 및 포스터 제작</div>
<div class="kb-diagram-tree-item" style="--depth:1">의사결정 시 참조 기준으로 활용</div>
<div class="kb-diagram-tree-item" style="--depth:1">정기 업데이트 (6~12개월)</div>
</div>
</div>



### 페르소나 유형

| 유형 | 설명 | 활용 |
|:---|:---|:---|
| **1차 페르소나 (Primary)** | 핵심 타겟 사용자, 설계의 중심 | 모든 설계 결정의 기준 |
| **2차 페르소나 (Secondary)** | 부가 타겟, 1차를 방해하지 않는 선에서 고려 | 추가 기능 설계 시 |
| **부정적 페르소나 (Negative)** | 타겟이 아닌 사용자, 설계 범위 명확화 | "이 사람은 대상이 아님" |
| **Proto-Persona** | 조사 전 가정 기반 초안 페르소나 | 빠른 시작, 조사로 보완 |

### 페르소나 활용 시나리오

```text
페르소나 기반 의사결정 프로세스:

질문: "모바일 앱에 데스크톱과 동일한 통계 기능을 넣을까?"

1차 페르소나 (김지연, 워킹맘 PM):
  ✗ 출퇴근 중 복잡한 통계 분석은 사용하지 않음
  ✗ 모바일은 빠른 확인 용도로 사용

2차 페르소나 (박철수, 데이터 분석가):
  ✓ 가끔 이동 중 데이터 확인 필요
  △ 전체 통계보다 주요 지표 요약이면 충분

결론: 전체 통계 기능은 PC에 집중,
      모바일은 핵심 지표 요약 + 알림으로 설계
```

- **📢 섹션 요약 비유**: 페르소나는 건물 설계의 "거주자 프로필"이다. "1인 가구 직장인을 위한 원룸"과 "4인 가족을 위한 아파트"는 완전히 다른 설계가 필요하다. 거주자가 명확해야 좋은 집이 나온다.

---

## Ⅲ. 비교 및 연결

### 페르소나 vs 관련 사용자 분석 기법 비교

| 기법 | 목적 | 특징 | 산출물 |
|:---|:---|:---|:---|
| **페르소나** | 사용자 대표 인물상 | 구체적 가상 인물 | 페르소나 시트 |
| **사용자 세그멘테이션** | 시장 분류 | 통계적 그룹화 | 세그먼트 프로필 |
| **사용자 여정 지도 (Journey Map)** | 경험 흐름 시각화 | 시간 순 경험 | 여정 다이어그램 |
| **직업 이야기 (JTBD)** | 사용자의 진짜 목표 | "무엇을 완수하려 하는가" | JTBD 진술문 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/">User Story</a></strong> | Agile 요구 표현 | 기능 중심 | "As a... I want..." |
| **Empathy Map** | 공감 정보 시각화 | 보고/듣고/생각/느끼는 것 | 4분면 지도 |

### 페르소나와 요구사항 공학의 연결

| RE 단계 | 페르소나 활용 |
|:---|:---|
| **도출** | 페르소나 기반 시나리오로 요구 발견 |
| **분석** | "1차 페르소나에게 필요한가?" 우선순위 판단 |
| **명세** | User Story에 페르소나 반영 ("As a 워킹맘 PM...") |
| **검증** | 페르소나를 연기하는 사용성 테스트 |

- **📢 섹션 요약 비유**: 페르소나는 소설의 주인공 캐릭터 설정표다. 작가(개발팀)가 항상 "이 캐릭터라면 어떻게 할까?"를 생각하며 일관된 스토리(제품)를 만들 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **실제 조사 기반**: 페르소나가 실제 사용자 인터뷰·관찰 데이터를 기반으로 만들어졌는가?
2. **적정 수**: 페르소나가 3~5개로 적정하게 유지되는가? (너무 많으면 활용 불가)
3. **1차 페르소나 명확화**: 설계 결정의 중심이 되는 1차 페르소나가 명확히 정의되었는가?
4. **부정적 페르소나**: 타겟이 아닌 사용자를 명시하여 설계 범위가 명확한가?
5. **팀 공유**: 모든 팀원이 페르소나를 알고 의사결정에 참조하는가?
6. **업데이트 계획**: 페르소나가 시장 변화에 따라 주기적으로 업데이트되는가?

### 안티패턴

- **가짜 페르소나(Fake Persona)**: 실제 사용자 조사 없이 팀의 가정만으로 만든 페르소나. 팀이 원하는 방향을 사용자 요구처럼 포장하게 되어 실제 사용자와 동떨어진 제품이 만들어진다. 최소 10명 이상의 실제 사용자 인터뷰를 기반으로 해야 한다.

- **페르소나 남용**: 지나치게 많은 페르소나(10개+)를 만들어 어떤 페르소나가 중심인지 불명확해지는 패턴. 1차 페르소나 1~2개, 2차 페르소나 2~3개 정도로 제한하고, 각자의 우선순위를 명확히 해야 한다.

- **페르소나 화석화**: 만들고 나서 업데이트하지 않고, 시장이 변화해도 수년 된 페르소나를 계속 사용하는 패턴. 6~12개월 주기로 사용자 데이터를 재조사하고 페르소나를 업데이트해야 한다.

- **마케팅 페르소나와 혼동**: 마케팅 타겟 세그먼트(구매 의사 결정자)와 UX 페르소나(실제 사용자)를 혼동하는 패턴. 기업 소프트웨어에서 구매 결정자(임원)와 실제 사용자(실무자)는 전혀 다른 요구를 가진다.

- **📢 섹션 요약 비유**: 가짜 페르소나는 의학 연구에서 임상 실험 없이 "아마도 효과가 있을 것"이라고 약을 개발하는 것이다. 실제 환자 데이터 없이는 효과 없는 약이 나온다.

---

## Ⅴ. 기대효과 및 결론

페르소나 기반 설계는 제품의 UX 품질을 높이고 개발 방향의 일관성을 유지한다. 정량적으로 Nielsen Norman Group의 연구에 따르면 페르소나를 사용하는 팀은 그렇지 않은 팀 대비 사용성 문제를 30% 더 많이 사전에 발견하고, 팀 내 UX 관련 의사결정 속도가 40% 향상된다.

페르소나의 진정한 가치는 공통 언어(Common Language) 형성이다. "김지연 씨가 이걸 쓸 수 있을까요?"라는 질문 하나로 팀 전체가 동일한 판단 기준을 가지게 된다. 이는 마케팅, 개발, 디자인, 지원 팀이 모두 동일한 사용자 이미지를 가지고 협력하는 조직 문화를 형성한다.

미래에는 AI가 대규모 사용자 데이터에서 자동으로 페르소나를 생성하고 업데이트하는 방향으로 발전할 것이다. 사용 로그, 지원 티켓, SNS 데이터를 분석하여 실시간으로 페르소나를 갱신하고, 사용자 행동 변화를 자동 탐지하는 시스템이 등장하고 있다. 그러나 페르소나에 인간적 공감과 이야기를 부여하는 작업은 여전히 인간 UX 연구자의 역할로 남을 것이다.

- **📢 섹션 요약 비유**: 페르소나는 나침반이다. 개발 과정에서 방향을 잃었을 때 "김지연 씨라면?"이라는 질문이 항상 올바른 방향을 가리킨다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **페르소나** | 가상 사용자 프로필, UCD의 핵심 도구 |
| **시나리오** | 페르소나의 사용 맥락 이야기 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/081_user_story_invest/">User Story</a></strong> | 페르소나 기반 Agile 요구 표현 |
| **사용자 여정 지도** | 페르소나의 경험 흐름 시각화 |
| **UCD (사용자 중심 설계)** | 페르소나 기반 설계 방법론 |
| **Empathy Map** | 페르소나 보완 도구 (공감 시각화) |
| **JTBD (Jobs-to-be-Done)** | 페르소나의 진짜 목표 분석 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 사용자 분석 (~1990s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">페르소나 방법론 체계화 (Alan Cooper, 1999)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">시나리오 기반 설계 결합 (2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">사용자 여정 지도 + 페르소나 통합 (2005~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">데이터 기반 페르소나 (Analytics + UX, 2010s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI 페르소나 ── 사용자 데이터→자동 페르소나 생성</div>
<div class="kb-diagram-tree-item" style="--depth:7">실시간 페르소나 업데이트</div>
<div class="kb-diagram-tree-item" style="--depth:7">A/B 테스트 기반 페르소나 검증</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 페르소나는 <strong>영화 주인공 설정</strong>이에요. "누구를 위해 만드는지" 정해요.
2. "35세 워킹맘 지연 씨"처럼 **구체적으로** 정하면 좋은 제품이 나와요.
3. "모든 사람을 위해"는 결국 **아무도 만족 못 하는** 제품이 된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 137 / 973

← **이전**: [136. 브레인스토밍 & JAD - 그룹 기반 요구 도출 기법](/knowledge-base/studynote/04_software_engineering/03_design_architecture/136_brainstorming_jad_requirements/)
**다음**: [138. 프로토타이핑 - Throwaway vs Evolutionary 프로토타입](/knowledge-base/studynote/04_software_engineering/03_design_architecture/138_prototyping_throwaway_evolutionary/) →

---
