+++
title = "472. BSIMM (Building Security In Maturity Model)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BSIMM(Building Security In Maturity Model)은 실제 기업들이 소프트웨어 보안 프로그램(SSP, Software Security Program)을 어떻게 운영하는지 관찰·데이터화한 성숙도 모델로, "업계 평균과 비교하여 우리 조직의 소프트웨어 보안 성숙도는 어디에 있는가"를 측정하는 벤치마킹 도구다.
> 2. **가치**: BSIMM은 보안이 "해야 한다"는 당위가 아니라, "실제 선도 기업들이 이렇게 하고 있다"는 관찰 데이터에 기반하므로, 경영진 설득과 투자 우선순위 결정에 객관적 근거를 제공한다.
> 3. **판단 포인트**: BSIMM을 단순 점수 게임으로 활용하면 형식적 활동만 늘어난다. "우리의 비즈니스 위험 프로필에 가장 부합하는 보안 활동이 무엇인가"라는 관점에서 개선 우선순위를 결정하는 도구로 활용해야 한다.

---

## Ⅰ. 개요 및 필요성

### BSIMM의 탄생 배경

2008년 Cigital(현재 Synopsys 인수)의 Gary McGraw, Sammy Migues, Brian Chess 세 명의 연구자가 BSIMM을 개발했다. 이들의 문제 의식은 명확했다. "소프트웨어 보안을 잘하는 조직들은 실제로 무엇을 하는가?" 기존의 보안 프레임워크들은 "해야 한다"는 처방적(Prescriptive) 접근을 취했지만, BSIMM은 "실제로 하고 있다"는 서술적(Descriptive) 접근을 택했다.

최초 버전은 9개 대기업의 소프트웨어 보안 프로그램을 직접 인터뷰하고 관찰하여 도출되었다. 이후 매년 업데이트되며 참가 조직이 늘어났고, 2023년 기준으로 130개 이상의 글로벌 기업 데이터를 바탕으로 한 BSIMM 13이 발표되었다. 참가 기업에는 Adobe, Bank of America, Google, Cisco, Salesforce, Visa 등 주요 글로벌 기술·금융 기업들이 포함된다.

### BSIMM이 필요한 이유

소프트웨어 보안 성숙도를 측정하는 어려움은 두 가지였다. 첫째, 무엇을 측정해야 하는가? 보안 활동의 종류가 너무 많아 어디서 시작해야 할지 모른다. 둘째, 우리가 잘하고 있는 건가? 절대적 기준이 없으면 현재 수준이 충분한지 알 수 없다.

BSIMM은 두 가지 질문에 모두 답한다. 업계에서 실제로 수행되는 112가지 보안 활동 목록을 제공하고(무엇을 측정할지), 참가 조직들의 평균·상위 수행율을 공개하여 비교 기준을 제시한다(잘하고 있는지 판단).

- **📢 섹션 요약 비유**: 내가 공부를 잘하는지 모를 때, 같은 시험을 본 다른 학생들의 점수 분포를 보면 나의 위치를 알 수 있다. BSIMM은 소프트웨어 보안의 전국 단위 성적표다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### BSIMM의 구조: 4개 도메인, 12개 실천 영역, 112개 활동

BSIMM은 계층 구조를 갖는다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BSIMM 전체 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거버넌스</div><div class="kb-diagram-cell">인텔리전스</div><div class="kb-diagram-cell">SSDL 터치포인트</div><div class="kb-diagram-cell">배포</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Governance)</div><div class="kb-diagram-cell">(Intelligence</div><div class="kb-diagram-cell">(SSDL Touchpoints</div><div class="kb-diagram-cell">(Deployment)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">)</div><div class="kb-diagram-cell">)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">• 전략 및</div><div class="kb-diagram-cell">• 공격 모델</div><div class="kb-diagram-cell">• 아키텍처</div><div class="kb-diagram-cell">• 침투 테스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">지표</div><div class="kb-diagram-cell">• 보안 기능</div><div class="kb-diagram-cell">분석</div><div class="kb-diagram-cell">• 소프트웨어</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">• 컴플라이</div><div class="kb-diagram-cell">및 설계</div><div class="kb-diagram-cell">• 코드 리뷰</div><div class="kb-diagram-cell">환경</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">언스 및</div><div class="kb-diagram-cell">• 기준/요건</div><div class="kb-diagram-cell">• 보안 테스트</div><div class="kb-diagram-cell">• 구성 관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">정책</div><div class="kb-diagram-cell">및 취약점</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">• 교육</div><div class="kb-diagram-cell">관리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">총 12개 실천 영역(Practice) × 각 3단계 성숙도 = 112개 활동</div></div>
</div>
</div>



### 4개 도메인 상세

| 도메인 | 약자 | 핵심 질문 | 포함 실천 영역 |
|:---|:---|:---|:---|
| 거버넌스(Governance) | G | 보안 프로그램을 어떻게 조직하고 관리하는가? | 전략·지표(SM), 컴플라이언스·정책(CP), 교육(T) |
| 인텔리전스(Intelligence) | I | 보안 지식을 어떻게 수집하고 공유하는가? | 공격 모델(AM), 보안 기능·설계(SFD), 기준·요건(SR) |
| SSDL 터치포인트 | S | 개발 라이프사이클에 보안을 어떻게 통합하는가? | 아키텍처 분석(AA), 코드 리뷰(CR), 보안 테스팅(ST) |
| 배포(Deployment) | D | 소프트웨어를 어떻게 안전하게 배포·운영하는가? | 침투 테스트(PT), SW 환경(SE), 구성 관리·취약점 관리(CMVM) |

### BSIMM 성숙도 레벨 체계

각 실천 영역은 레벨 1-3으로 구분되며, 번호가 낮을수록 많은 조직이 수행하는 기초 활동이다.

| 레벨 | 의미 | 수행 기업 비율 | 예시 활동 |
|:---|:---|:---|:---|
| 레벨 1 | 기초·필수 활동 | 60% 이상 | 보안 기본 교육 실시, SAST 도구 사용 |
| 레벨 2 | 중급·체계화 활동 | 30-60% | 자동화된 보안 테스트, 위협 모델링 정규화 |
| 레벨 3 | 고급·선도 활동 | 30% 미만 | 퍼징(Fuzzing) 적용, 공격 인텔리전스 공유 |

### BSIMM 평가 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">인터뷰 준비</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">보안 활동 담당자 식별, 자료 수집</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1:1 인터뷰</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">BSIMM 활동 목록 기준으로 수행 여부 확인 (2-3일)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">활동 매핑</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">인터뷰 결과를 112개 활동에 매핑</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스코어 계산</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">도메인·실천 영역별 점수 산출</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">벤치마크 비교</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">업계 평균, 동종업계 평균과 비교</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">보고서 작성</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">현재 수준, 격차, 개선 우선순위</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">로드맵 수립</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">1년/3년 개선 로드맵 수립</div></div>
</div>
</div>



### BSIMM 스코어카드 예시 (가상)

| 실천 영역 | 수행 활동 수 | 레벨 1 수행 | 레벨 2 수행 | 레벨 3 수행 | 업계 평균 |
|:---|:---|:---|:---|:---|:---|
| 전략·지표(SM) | 4/12 | ● ● ● | ● | ○ ○ | 5.2/12 |
| 교육(T) | 3/6 | ● ● | ● | ○ | 3.8/6 |
| 코드 리뷰(CR) | 5/8 | ● ● ● | ● ● | ○ | 4.5/8 |
| 침투 테스트(PT) | 2/9 | ● ● | ○ | ○ | 3.1/9 |

- **📢 섹션 요약 비유**: 건강검진 결과지에서 내 혈압·혈당·콜레스테롤 수치를 같은 나이대 평균과 비교하듯, BSIMM은 조직의 보안 활동을 업계 평균과 비교하는 종합 건강검진표다.

---

## Ⅲ. 비교 및 연결

### BSIMM vs OWASP SAMM

OWASP SAMM(Software Assurance Maturity Model)은 BSIMM과 함께 가장 많이 참조되는 소프트웨어 보안 성숙도 모델이다.

| 구분 | BSIMM | OWASP SAMM |
|:---|:---|:---|
| 접근 방식 | 서술적(Descriptive) - 실제 관행 관찰 | 처방적(Prescriptive) - 해야 할 것 정의 |
| 기반 | 실제 기업 인터뷰 데이터 | 이상적 보안 모델 |
| 비용 | 유료 (공인 평가사 필요) | 무료, 오픈소스 |
| 벤치마킹 | 업계 비교 가능 | 절대 기준 제시 |
| 업데이트 | 연간 실데이터 기반 갱신 | 커뮤니티 기반 갱신 |
| 권장 용도 | 업계 대비 현황 파악, 경영진 보고 | 자체 개선 목표 수립, 실행 계획 |
| 상호 보완 | BSIMM으로 현황 파악 → SAMM으로 개선 로드맵 수립 | |

### BSIMM vs CMMI

| 구분 | BSIMM | CMMI(Capability Maturity Model Integration) |
|:---|:---|:---|
| 대상 | 소프트웨어 보안 | 소프트웨어 개발 프로세스 전반 |
| 성격 | 보안 특화 성숙도 | 범용 프로세스 성숙도 |
| 관계 | CMMI Level 3 이상 조직에서 BSIMM 적용이 용이 | |

### 관련 개념 연결

| 관련 개념 | 연결 내용 |
|:---|:---|
| [Secure SDLC](/knowledge-base/studynote/04_software_engineering/11_testing_validation/471_secure_sdlc/) | BSIMM이 측정하는 대상. 개발 전 단계 보안 활동 |
| [Microsoft SDL](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) | BSIMM의 SSDL 터치포인트와 유사한 구체적 활동 |
| [위협 모델링](/knowledge-base/studynote/04_software_engineering/11_testing_validation/474_threat_modeling/) | BSIMM의 아키텍처 분석(AA) 실천 영역의 핵심 활동 |
| [SAST](/knowledge-base/studynote/04_software_engineering/11_testing_validation/491_sast/) | BSIMM 코드 리뷰(CR) 영역의 핵심 도구 |

- **📢 섹션 요약 비유**: 체크리스트는 "해야 할 일 목록"이지만, BSIMM은 "같은 업계 100개 회사가 실제로 하는 일들의 통계"다. 후자가 훨씬 설득력 있는 근거가 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### BSIMM 활용 시나리오

| 시나리오 | BSIMM 활용 방법 |
|:---|:---|
| 경영진 투자 설득 | "업계 상위 20% 기업은 이 활동을 하고 있습니다" |
| 개선 우선순위 결정 | 낮은 비용·높은 효과의 미수행 활동 식별 |
| 인수합병(M&A) 실사 | 피인수 기업의 보안 성숙도 정량 평가 |
| 연도별 성과 측정 | 전년 대비 수행 활동 증가 추적 |
| 규정 준수 매핑 | BSIMM 활동을 PCI DSS, ISO 27001 등에 매핑 |

### 설계 판단 체크리스트

1. **BSIMM 평가 전에 보안 활동 인벤토리를 정리했는가?** - 현재 수행 중인 보안 활동을 문서화하고 증거를 수집해야 평가의 정확성이 높아진다.
2. **업계 비교가 적절한 peer group으로 이루어지는가?** - 금융권 기업이 소프트웨어 스타트업과 비교하면 의미가 없다. 동종업계·유사 규모 집단과 비교해야 한다.
3. **점수 향상보다 리스크 감소를 목표로 삼는가?** - BSIMM 점수를 높이기 위해 형식적 활동을 추가하는 것은 무의미하다. 실제 보안 위험이 줄어야 가치가 있다.
4. **BSIMM 결과를 개선 로드맵과 연결했는가?** - 평가 후 6개월·1년·3년 단위의 구체적 개선 계획이 있어야 한다.
5. **임원진이 BSIMM 결과를 이해하고 지원하는가?** - 보안 성숙도 향상은 기술 팀만의 노력으로 불가능하다. 경영진의 인식과 예산 지원이 필수다.

### 안티패턴

- **점수 게임화(Gamification)**: BSIMM 점수를 높이는 것 자체가 목적이 되어, 실질적 보안 효과 없이 서류상으로만 활동을 수행하는 경우. 내부 감사에서는 높은 점수가 나오지만 실제 침해 사고는 계속 발생한다.
- **부적절한 peer 비교**: 자사의 실제 비즈니스 위험과 무관하게 "업계 평균보다 높으면 충분하다"고 판단하는 경우. 보안 성숙도 요건은 기업의 데이터 민감성, 규제 환경, 공격자 관심도에 따라 다르다.
- **일회성 평가로 끝내기**: 1~2년에 한 번 평가를 받고 보고서만 제출한 뒤 실질적 개선 없이 다음 평가를 기다리는 경우. BSIMM은 지속적 개선 도구로 활용되어야 한다.
- **모든 활동을 동시에 추진**: BSIMM에서 미수행으로 확인된 수십 가지 활동을 동시에 추진하려다 자원 분산으로 아무것도 완성하지 못하는 경우. 비즈니스 위험 기반으로 3~5개 우선 활동을 선정하는 것이 현실적이다.

- **📢 섹션 요약 비유**: 건강검진 결과를 받고 "콜레스테롤 수치가 평균보다 낮으니 괜찮다"고 자만하는 것과, "내 생활 방식에서 위험 요인을 찾아 개선하겠다"는 것은 전혀 다른 접근이다. BSIMM은 후자로 활용되어야 한다.

---

## Ⅴ. 기대효과 및 결론

BSIMM을 도입하는 조직이 얻는 가장 큰 가치는 '객관적 언어'다. "우리 회사 보안이 좋다/나쁘다"는 주관적 판단 대신, "우리는 업계 참가 기업 중 상위 40% 수준이며, 코드 리뷰와 침투 테스트 영역에서 상위 20% 기업보다 20% 낮다"는 구체적이고 비교 가능한 언어로 경영진과 대화할 수 있게 된다. 이는 보안 투자 의사결정에 결정적 역할을 한다.

BSIMM의 데이터는 업계 트렌드도 반영한다. 최근 버전에서는 클라우드 보안, 컨테이너 보안, AI/ML 보안 관련 활동들이 새롭게 추가되었다. 이를 통해 조직은 현재 상태 뿐만 아니라 미래의 보안 환경 변화에 어떻게 대비해야 하는지도 파악할 수 있다.

결론적으로 BSIMM은 "소프트웨어 보안 성숙도를 업계 데이터에 기반해 측정하고, 비즈니스 위험 관점에서 개선 방향을 찾는 전략적 도구"다. 기술사 관점에서는 보안 투자를 합리화하고 조직의 보안 역량을 지속적으로 향상시키는 의사결정 도구로 활용해야 한다.

- **📢 섹션 요약 비유**: 기업의 재무 건전성을 업계 평균 ROE, 부채비율 등으로 비교하듯, BSIMM은 기업의 보안 건전성을 업계 평균 보안 활동으로 비교하는 보안 재무제표다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Secure SDLC](/knowledge-base/studynote/04_software_engineering/11_testing_validation/471_secure_sdlc/) | BSIMM이 측정하는 보안 개발 프로세스의 기반 |
| [Microsoft SDL](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) | BSIMM SSDL 터치포인트의 실천 사례 |
| [위협 모델링](/knowledge-base/studynote/04_software_engineering/11_testing_validation/474_threat_modeling/) | BSIMM 아키텍처 분석 영역의 핵심 활동 |
| [성숙도 모델](/knowledge-base/studynote/12_it_management/01_governance_strategy/011_maturity_model/) | BSIMM의 기반 개념. 조직 역량을 단계로 측정 |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) | BSIMM의 상위 학문 체계 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">보안 사고 반복 → "어떻게 보안을 측정하는가?" 문제 인식</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Gary McGraw, Cigital의 실제 기업 보안 관행 연구 (2005-2007)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BSIMM v1 발표 (2008) - 9개 기업 데이터 기반</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BSIMM 연간 업데이트 체계 수립 (참가 기업 지속 증가)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Synopsys의 Cigital 인수 후 BSIMM 관리 이관 (2016)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BSIMM v10 - 클라우드·DevOps 보안 활동 추가 (2019)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BSIMM v12 - ML/AI 보안 활동 포함 (2022)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BSIMM v13 - 130+ 기업, 클라우드 네이티브 보안 강화 (2023)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. BSIMM은 "전국 학교들이 수학을 어떻게 가르치는지 조사"한 것처럼, 전 세계 기업들이 보안을 어떻게 하고 있는지 조사한 성적표예요.
2. 우리 학교(회사)가 전국 평균보다 어떤 과목(보안 활동)이 부족한지 비교해서 어디를 더 공부해야 할지 알 수 있어요.
3. 단순히 점수를 올리는 것보다 실제로 더 안전한 소프트웨어를 만드는 것이 목표여야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 535 / 973

← **이전**: [471. 소프트웨어 개발 보안 (Secure SDLC) - 기획, 설계, 구현, 테스트 전 단계 보안 활동](/knowledge-base/studynote/04_software_engineering/11_testing_validation/471_secure_sdlc/)
**다음**: [473. Microsoft SDL - 마이크로소프트의 보안 개발 생명주기 프레임워크](/knowledge-base/studynote/04_software_engineering/11_testing_validation/473_microsoft_sdl/) →

---
