+++
title = "140. 쉐도잉 & 관찰 기법 (Shadowing/Observation) - 현장 기반 요구 도출"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 쉐도잉/관찰(Ethnography)은 <strong>실제 현장에서 사용자의 업무 수행을 직접 관찰</strong>하여, 인터뷰만으로는 드러나지 않는 <strong>암묵적 요구(Tacit Requirements)</strong>를 발견하는 기법이다.
> 2. **가치**: 사용자는 습관화된 비효율을 **자각하지 못하고 말하지 않지만**, 관찰자는 불필요한 클릭·수작업·우회 경로 등을 <strong>객관적으로 발견</strong>할 수 있다.
> 3. **판단 포인트**: 수동적 관찰(방해 없이)과 능동적 관찰(질문하며) 구분, Contextual Inquiry(맥락적 질의)가 관찰+인터뷰 결합형이다.

---

## Ⅰ. 개요 및 필요성

관찰 기법(Observation Technique)은 사회과학의 민족지학(Ethnography)에서 소프트웨어 RE에 도입된 기법이다. 1998년 Hugh Beyer와 Karen Holtzblatt의 "Contextual Design"이 이 방법론을 소프트웨어 설계에 체계화했다. 핵심 아이디어는 "사용자가 말하는 것"과 "사용자가 실제로 하는 것"이 다르다는 관찰에서 출발한다.

관찰이 필요한 이유는 **인지적 한계** 때문이다. 사람은 반복하는 행동을 의식하지 못한다. 10년간 매일 사용한 시스템에서 비효율적인 7단계 클릭 경로를 "원래 이렇게 하는 것"으로 인식하고 인터뷰에서 언급하지 않는다. 그러나 관찰자의 눈에는 "이 7단계가 3단계로 줄어들 수 있다"는 것이 명확히 보인다. 이것이 암묵적 요구(Tacit Requirements)이다.

쉐도잉(Shadowing)은 관찰의 집중적 형태로, 말 그대로 사용자의 그림자처럼 하루 종일 따라다니며 모든 행동을 기록하는 기법이다. 서비스 디자인(Service Design) 분야에서는 고객이 매장에 입장해서 나올 때까지의 전체 경험을 쉐도잉으로 기록하고 분석한다. Contextual Inquiry는 관찰과 인터뷰를 결합한 형태로, 사용자가 작업을 수행하는 동안 즉석에서 질문("지금 왜 이 버튼을 누르셨나요?")하여 더 깊은 이해를 얻는다.

```text
관찰 기법 유형과 특징:

[수동적 관찰]
  - 사용자를 방해하지 않고 멀리서 관찰
  - 자연스러운 행동 패턴 포착
  - 관찰자 효과(Hawthorne Effect) 최소화
  - 한계: 행동의 이유 파악 어려움

[능동적 관찰 / 쉐도잉]
  - 사용자 옆에서 하루 종일 밀착 관찰
  - 즉석 질문 가능
  - 업무 맥락 전체 파악
  - 한계: 관찰자 존재가 행동에 영향

[Contextual Inquiry]
  - 관찰 + 인터뷰 결합
  - 사용자가 작업 수행 중 즉석 질문
  - "지금 왜 이 버튼을 3번 눌렀나요?"
  - 가장 풍부한 인사이트 제공

[비디오 분석]
  - 작업 화면 + 사용자 얼굴 동시 녹화
  - 표정·당혹감 포착
  - 나중에 반복 분석 가능
```

- **📢 섹션 요약 비유**: 관찰은 <strong>탐정 조사</strong>이다. 범인(비효율)은 스스로 자백하지 않으므로, 현장에서 단서를 직접 찾아야 한다. 목격자(인터뷰)만으로는 전체 그림을 그릴 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 관찰 기법 상세 비교

| 기법 | 방식 | 시간 | 비용 | 발견 가능한 요구 | 적합 상황 |
|:---|:---|:---|:---|:---|:---|
| **수동적 관찰** | 멀리서 관찰 | 수시간 | 낮음 | 행동 패턴 | 비침습적 필요 |
| **쉐도잉** | 밀착 동행 | 수시간~1일 | 중간 | 업무 전체 흐름 | 복잡한 업무 |
| **Contextual Inquiry** | 관찰+즉석질문 | 2~4시간/인 | 중간~높음 | 행동+이유 | 깊이 이해 필요 |
| **비디오 프로토콜** | 녹화+분석 | 수시간+분석 | 중간 | 미세 행동 | 반복 분석 |
| **Think-Aloud** | 수행 중 생각 말하기 | 1~2시간 | 낮음 | 인지 과정 | 사용성 테스트 |
| **다이어리 연구** | 사용자 직접 기록 | 1~4주 | 낮음 | 장기 패턴 | 비빈번 사용 |

### Contextual Inquiry 4원칙



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Contextual Inquiry 핵심 원칙 (Holtzblatt &amp; Beyer):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">1.</div><div class="kb-diagram-node">맥락 (Context)</div></div>
<div class="kb-diagram-note">사용자의 실제 작업 환경에서 관찰</div>
<div class="kb-diagram-note">→ 실험실이 아닌 현장에서 수행</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">2.</div><div class="kb-diagram-node">파트너십 (Partnership)</div></div>
<div class="kb-diagram-note">관찰자-사용자 협력 관계 (스승-제자 아님)</div>
<div class="kb-diagram-note">→ "제가 배우러 왔습니다" 자세</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">3.</div><div class="kb-diagram-node">해석 (Interpretation)</div></div>
<div class="kb-diagram-note">관찰 내용을 즉시 확인·공유</div>
<div class="kb-diagram-note">→ "이 작업이 ~를 의미하는 건가요?"</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">4.</div><div class="kb-diagram-node">집중 (Focus)</div></div>
<div class="kb-diagram-note">연구 목적에 집중된 관찰</div>
<div class="kb-diagram-note">→ 관찰 범위를 사전에 명확히 정의</div>
</div>
</div>



### 관찰 기법 실시 절차



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">관찰 기법 실시 단계:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">사전 준비</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">관찰 목적 및 범위 정의</div>
<div class="kb-diagram-tree-item" style="--depth:1">관찰 허가 취득 (개인정보, 녹화 동의)</div>
<div class="kb-diagram-tree-item" style="--depth:1">관찰 도구 준비 (녹음기, 카메라, 메모장)</div>
<div class="kb-diagram-tree-item" style="--depth:1">사전 지식 습득 (해당 업무 기초 이해)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">관찰 실시</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">자기 소개 및 목적 설명</div>
<div class="kb-diagram-tree-item" style="--depth:1">관찰 시작 (초기엔 수동적으로)</div>
<div class="kb-diagram-tree-item" style="--depth:1">핵심 행동 시 즉석 질문 (Contextual Inquiry)</div>
<div class="kb-diagram-tree-item" style="--depth:1">모든 행동 상세 기록</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">기록 분류 (코딩)</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">암묵적 요구 (사용자가 말하지 않은 것)</div>
<div class="kb-diagram-tree-item" style="--depth:1">비효율 포인트 (Pain Points)</div>
<div class="kb-diagram-tree-item" style="--depth:1">우회 경로 (Workarounds)</div>
<div class="kb-diagram-tree-item" style="--depth:1">빈번한 실수 패턴</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">결과 분석</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">친화 다이어그램 (Affinity Diagram)</div>
<div class="kb-diagram-tree-item" style="--depth:1">업무 모델 작성 (Work Model)</div>
<div class="kb-diagram-tree-item" style="--depth:1">요구사항 목록으로 변환</div>
</div>
</div>



### 관찰 데이터 분석: 친화 다이어그램



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">친화 다이어그램 (Affinity Diagram) 구성:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">개별 관찰 메모 수집</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">유사 메모 그룹화 (포스트잇)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">그룹별 레이블 부여</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">상위 주제 묶기</div></div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">그룹: "입력 관련 불편"</div>
<div class="kb-diagram-tree-item" style="--depth:2">"이름 필드를 3번이나 재입력"</div>
<div class="kb-diagram-tree-item" style="--depth:2">"복사-붙여넣기가 안 됨"</div>
<div class="kb-diagram-tree-item" style="--depth:2">"자동완성이 오히려 방해"</div>
<div class="kb-diagram-note">→ 요구사항: 입력 편의성 개선 (자동완성 개선, 필드 유지)</div>
</div>
</div>



### 발견 가능한 암묵적 요구 유형

| 유형 | 설명 | 예시 |
|:---|:---|:---|
| **우회 경로 (Workaround)** | 시스템 한계를 극복하기 위한 임시방편 | 엑셀로 데이터를 복사 후 붙여넣기 |
| **숨겨진 비효율** | 관행화된 불필요한 단계 | 인쇄→수기 입력→재스캔 |
| **미사용 기능** | 존재하지만 사용 안 되는 기능 | 복잡해서 안 쓰는 검색 필터 |
| **비공식 도구** | 공식 시스템 외 개인 도구 사용 | 개인 메모장, 포스트잇으로 보완 |
| **소통 패턴** | 시스템 외 소통 방식 | 구두로 확인 후 시스템 입력 |

- **📢 섹션 요약 비유**: 관찰 기법은 고고학 발굴이다. 땅 위에 보이는 것(사용자 인터뷰)은 일부이고, 진짜 보물(암묵적 요구)은 땅을 파야(현장 관찰) 나온다.

---

## Ⅲ. 비교 및 연결

### 관찰 기법 vs 다른 도출 기법 비교

| 항목 | 인터뷰 | JAD | 관찰 (Ethnography) |
|:---|:---|:---|:---|
| **발견 요구 유형** | 의식된 요구 | 다부서 합의 | 암묵적 요구 |
| **비용** | 낮음 | 중간 | 높음 |
| **시간** | 1~2시간 | 반나절~수일 | 수일~수주 |
| **사용자 영향** | 인위적 환경 | 인위적 환경 | 자연스러운 환경 |
| **깊이** | 보통 | 보통 | 매우 높음 |
| **확장성** | 보통 | 낮음 | 낮음 |

### 관찰 결과 활용 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">관찰 → 분석 → 요구사항 변환:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">관찰 기록</div></div>
<div class="kb-diagram-note">"사용자가 주문 완료 후 화면을 스크린샷"</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">분석</div></div>
<div class="kb-diagram-note">"확인 이메일이 없어서 사용자가 직접 기록"</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">암묵적 요구 도출</div></div>
<div class="kb-diagram-note">"주문 완료 후 이메일 확인서 자동 발송"</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">요구사항 명세</div></div>
<div class="kb-diagram-note">FR: 주문 완료 시 확인 이메일을 발송한다</div>
<div class="kb-diagram-note">NFR: 이메일 발송은 주문 완료 후 1분 이내</div>
</div>
</div>



### 연결 개념

| 개념 | 관계 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/137_persona_analysis_modeling/">페르소나</a></strong> | 관찰 데이터를 기반으로 페르소나 구성 |
| **사용자 여정 지도** | 관찰 결과를 시간 순으로 시각화 |
| **Contextual Design** | 관찰→친화 다이어그램→작업 모델 체계 |
| **Design Thinking** | 관찰이 공감(Empathize) 단계의 핵심 기법 |

- **📢 섹션 요약 비유**: 관찰 기법은 의사의 직접 진찰이다. 환자 말(인터뷰)만 듣는 것보다, 직접 진찰(관찰)하면 환자가 표현하지 못한 증상을 발견할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. **관찰 목적 명확화**: "어떤 암묵적 요구를 발견할 것인가"가 명확한가?
2. **동의 취득**: 관찰 대상자의 녹화·관찰 동의서를 확보하였는가?
3. **Hawthorne 효과 관리**: 관찰자 존재가 사용자 행동에 미치는 영향을 인식하고 있는가?
4. **충분한 샘플**: 다양한 사용자 유형(베테랑·신규·다른 역할)을 관찰하였는가?
5. **결과 코딩**: 관찰 메모가 체계적으로 코딩(분류·분석)되었는가?
6. **친화 다이어그램**: 관찰 결과가 유사 패턴으로 그룹화되어 요구사항으로 변환되었는가?

### 안티패턴

- **Hawthorne 효과 무시**: 관찰 대상자가 관찰받는다는 사실을 인식하여 평소와 다르게 행동하는 문제. 관찰 초기 15~30분을 적응 시간으로 두고, 관찰자가 매우 조용히 동행하는 것이 중요하다. 비디오 녹화는 관찰자 부재 상황에서도 자연스러운 행동을 포착한다.

- **표면적 관찰**: "이 기능을 사용하는군"만 기록하고 "왜 이렇게 사용하는가"를 파악하지 않는 패턴. Contextual Inquiry처럼 즉석 질문을 통해 행동의 이유를 함께 기록해야 한다.

- **선택적 관찰**: 관찰자가 자신이 예상하는 요구와 관련된 행동만 기록하는 편향. 편견 없이 모든 행동을 기록하고, 팀 내 여러 관찰자의 기록을 교차 검증해야 한다.

- **관찰 결과 미변환**: 관찰 노트가 요구사항으로 변환되지 않고 원자료 상태로 방치되는 패턴. 친화 다이어그램 작업을 통해 반드시 요구사항 목록으로 구조화해야 한다.

- **📢 섹션 요약 비유**: 관찰 안티패턴은 사진 촬영 실수다. Hawthorne 효과 무시는 연출된 사진(자연스럽지 않은 행동), 표면적 관찰은 배경만 찍고 주인공을 못 찍기, 선택적 관찰은 예쁜 것만 골라 찍기이다.

---

## Ⅴ. 기대효과 및 결론

관찰 기법은 다른 도출 기법으로는 발견하기 어려운 암묵적 요구를 체계적으로 발굴한다. 실제 현장에서의 관찰을 통해 문서화된 업무 프로세스와 실제 수행 방식의 차이를 발견하고, 시스템이 현실 업무에 맞지 않는 부분을 파악할 수 있다. IBM의 연구에 따르면 Contextual Inquiry로 도출한 요구사항의 80%가 인터뷰만으로는 발견되지 않는 것이었다.

관찰 기법의 결과는 디자인 방향을 근본적으로 바꾸는 경우가 많다. 예를 들어, 병원 EMR(전자 의무 기록) 시스템 관찰에서 의사들이 "시스템에 없어서" 개인 수첩에 임시로 적는 행동을 발견하면, 이는 새로운 기능 추가 요구로 직결된다. 이런 인사이트는 사용자 인터뷰에서는 "없어서 불편하다"는 막연한 표현으로만 나타난다.

미래에는 AI가 관찰 기법을 확장할 것이다. 사용자의 애플리케이션 사용 로그를 분석하여 클릭 패턴, 오류 발생 지점, 우회 경로를 자동으로 탐지하는 도구가 이미 상용화되었다. 화면 녹화와 AI 분석을 결합한 원격 사용성 연구 플랫폼(Hotjar, FullStory)은 대규모 사용자의 행동을 동시에 관찰하는 것을 가능하게 했다.

- **📢 섹션 요약 비유**: 관찰 기법은 고성능 현미경이다. 인터뷰(맨눈)로 볼 수 없는 세균(암묵적 요구)을 현미경(관찰)으로 발견할 수 있다. 둘을 함께 사용할 때 가장 완전한 그림이 그려진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **쉐도잉** | 현장 밀착 관찰, 그림자처럼 동행 |
| **Ethnography** | 민족지학적 관찰 기법 |
| **Contextual Inquiry** | 관찰+즉석 질문 결합 |
| **암묵적 요구 (Tacit)** | 관찰의 핵심 발견 목표 |
| **친화 다이어그램** | 관찰 결과 그룹화·분석 도구 |
| **Hawthorne 효과** | 관찰 시 행동 변화 현상 |
| **사용자 여정 지도** | 관찰 결과 시각화 도구 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비공식 관찰 (~1990s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Contextual Design (Beyer &amp; Holtzblatt, 1998) ── 체계화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Ethnographic Study 소프트웨어 적용 (2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Design Thinking 관찰(Empathy) 단계 통합 (2010s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">원격 관찰 도구 (Zoom, Lookback, 2015~)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: AI 행동 분석 ── 사용자 클릭 패턴 자동 분석 (Hotjar)</div>
<div class="kb-diagram-tree-item" style="--depth:7">화면 녹화 AI 분석 (FullStory)</div>
<div class="kb-diagram-tree-item" style="--depth:7">히트맵 기반 UX 패턴 탐지</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. 관찰은 <strong>탐정 조사</strong>예요. 현장에서 <strong>단서(비효율)</strong>를 찾아요.
2. 사용자에게 물어봐도 <strong>모르는 습관</strong>이 있어요. 직접 봐야 알 수 있어요.
3. "왜 이 버튼을 3번 누르세요?" → <strong>숨겨진 문제</strong>를 발견해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 140 / 973

← **이전**: [139. 프로토타입 충실도 (Fidelity Levels) - Lo-Fi·Mid-Fi·Hi-Fi](/knowledge-base/studynote/04_software_engineering/03_design_architecture/139_prototyping_fidelity_levels/)
**다음**: [141. 포커스 그룹 인터뷰 (FGI) - 그룹 심층 인터뷰 기법](/knowledge-base/studynote/04_software_engineering/03_design_architecture/141_focus_group_interview_fgi/) →

---
