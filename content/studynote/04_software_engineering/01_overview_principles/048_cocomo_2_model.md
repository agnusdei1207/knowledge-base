+++
title = "048. COCOMO II — 소프트웨어 비용 추정"
date = 2026-04-05

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

> **핵심 인사이트**
> 1. [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II([Constructive Cost Model](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II)는 소프트웨어 개발 규모(LOC 또는 [기능 점수](/knowledge-base/studynote/12_it_management/04_sdlc_testing/140_function_point/))와 복잡도 요인을 결합하여 공수(Person-Month)와 일정을 과학적으로 추정 — 1995년 Barry Boehm이 발전시킨 [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) I의 개선 모델로, 현대 소프트웨어 개발 환경(재사용, CBD)을 반영한다.
> 2. 스케일 팩터(Scale Factor)와 비용 드라이버(Cost Driver)의 합성이 핵심 — 선형이 아닌 지수 스케일링으로 소규모 프로젝트(1만 LOC)와 초대형 프로젝트(100만 LOC) 사이의 비선형적 비용 증가를 모델링한다.
> 3. 추정의 불확실성을 인식하는 것이 [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II 활용의 전제 — [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 추정(Application Composition)은 ±4배, 상세 추정(Post-Architecture)도 ±25% 오차가 존재하므로, 추정을 하나의 점이 아닌 범위로 제시하고 지속적으로 검보하는 것이 올바른 활용법이다.

---

## Ⅰ. [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II 모델 개요

```
COCOMO I vs COCOMO II:

COCOMO I (1981):
  단순 LOC 기반
  Organic / Semi-Detached / Embedded 3유형
  현대 개발 환경 미반영 (재사용, 프로토타입)

COCOMO II (1995, 2000 개정):
  3가지 하위 모델 포함:

1. Application Composition:
  대상: 빠른 프로토타입, 4GL, CASE 도구
  규모 단위: Object Point (OP)
  
  PM = NOP / PROD
  (NOP: Nominal Object Point, PROD: 생산성 비율)

2. Early Design:
  대상: 설계 초기 단계, 제한된 정보
  규모: 기능 점수 (Function Point)
  
  PM = A × Size^SF × EM (초기 비용 드라이버)

3. Post-Architecture:
  대상: 전체 아키텍처 정의 후
  가장 정확한 추정
  규모: KSLOC (1000라인 코드)
  
  PM = A × Size^SF × ∏EMi
  (17개 비용 드라이버 적용)

기본 방정식:
  PM (공수) = A × (Size)^SF × ∏EMi
  
  A: 상수 (COCOMO II = 2.94)
  Size: 소프트웨어 규모 (KSLOC)
  SF: 스케일 지수 (Scaling Factor)
  EMi: i번째 비용 드라이버 곱
```

> 📢 **섹션 요약 비유**: [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II = 건축 공사비 견적 — 건물 크기(LOC)만으로 안 되고, 지형 난이도(SF)와 자재 품질(비용 드라이버)까지 고려해야 정확한 견적. 프로토타입엔 간단 견적, 완성 설계엔 정밀 견적!

---

## Ⅱ. 스케일 팩터 (Scale Factor)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SF (Scaling Factor):</div>
<div class="kb-diagram-note">프로젝트 규모 증가에 따른 비용 증가율 결정</div>
<div class="kb-diagram-note">SF = B + 0.01 × Σ SFj</div>
<div class="kb-diagram-note">B = 0.91 (COCOMO II 기본값)</div>
<div class="kb-diagram-note">5가지 SF 요인:</div>
<div class="kb-diagram-note">1. PREC (선례성, Precedentedness):</div>
<div class="kb-diagram-note">유사 프로젝트 경험 여부</div>
<div class="kb-diagram-note">Very Low: 전혀 새로운 영역 → 6.20</div>
<div class="kb-diagram-note">Very High: 유사 프로젝트 많음 → 1.24</div>
<div class="kb-diagram-note">2. FLEX (개발 유연성, Development Flexibility):</div>
<div class="kb-diagram-note">요구사항 유연성</div>
<div class="kb-diagram-note">Very Low: 엄격한 요구사항 → 5.07</div>
<div class="kb-diagram-note">Very High: 완전 자유 → 1.01</div>
<div class="kb-diagram-note">3. RESL (아키텍처/위험 해결, Architecture/Risk Resolution):</div>
<div class="kb-diagram-note">위험 분석 수준</div>
<div class="kb-diagram-note">Very Low: 낮은 위험 해결 → 7.07</div>
<div class="kb-diagram-note">Very High: 충분한 위험 대비 → 1.41</div>
<div class="kb-diagram-note">4. TEAM (팀 응집력, Team Cohesion):</div>
<div class="kb-diagram-note">팀 협력 수준</div>
<div class="kb-diagram-note">Very Low: 분산된 팀 → 5.48</div>
<div class="kb-diagram-note">Very High: 긴밀한 팀 → 1.10</div>
<div class="kb-diagram-note">5. PMAT (프로세스 성숙도, Process Maturity):</div>
<div class="kb-diagram-note">CMMI 수준 반영</div>
<div class="kb-diagram-note">Level 1 (초기): 7.80</div>
<div class="kb-diagram-note">Level 5 (최적화): 1.56</div>
<div class="kb-diagram-note">SF 계산 예:</div>
<div class="kb-diagram-note">5개 요인 각 평균(3점) = 5 × 3.0 = 15</div>
<div class="kb-diagram-note">SF = 0.91 + 0.01 × 15 = 1.06</div>
<div class="kb-diagram-note">SF &gt; 1: 규모 증가 시 비선형 비용 증가</div>
<div class="kb-diagram-note">(예: 10KSLOC → 100KSLOC: 10배 증가 아닌 12~15배 비용)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: SF = 공사 난이도 지수 — 처음 짓는 유형(PREC: 낮음), 설계 변경 잦음(FLEX: 낮음), 위험 분석 미흡(RESL: 낮음) → 같은 크기 건물인데 비용이 2배! 팀워크와 경험이 핵심!

---

## Ⅲ. 비용 드라이버 (Cost Driver)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">EM (Effort Multiplier):</div>
<div class="kb-diagram-note">Post-Architecture 모델의 17개 요인</div>
<div class="kb-diagram-note">0.5~1.26 범위 값</div>
<div class="kb-diagram-note">1.0: 표준(Nominal)</div>
<div class="kb-diagram-note">&lt; 1.0: 비용 감소 (좋은 요인)</div>
<div class="kb-diagram-tree-item" style="--depth:1">1.0: 비용 증가 (어려운 요인)</div>
<div class="kb-diagram-note">제품 요인 (Product Factors):</div>
<div class="kb-diagram-note">RELY: 신뢰성 요구사항 (Critical = 1.26)</div>
<div class="kb-diagram-note">DATA: 데이터베이스 규모</div>
<div class="kb-diagram-note">CPLX: 소프트웨어 복잡도 (Very High = 1.30)</div>
<div class="kb-diagram-note">RUSE: 재사용 요구 수준</div>
<div class="kb-diagram-note">DOCU: 문서화 요구 수준</div>
<div class="kb-diagram-note">플랫폼 요인:</div>
<div class="kb-diagram-note">TIME: 실행 시간 제약 (95% CPU = 1.29)</div>
<div class="kb-diagram-note">STOR: 메인 스토리지 제약</div>
<div class="kb-diagram-note">PVOL: 플랫폼 변동성</div>
<div class="kb-diagram-note">인력 요인 (Personnel Factors):</div>
<div class="kb-diagram-note">ACAP: 분석가 역량 (Very High = 0.71)</div>
<div class="kb-diagram-note">PCAP: 프로그래머 역량 (Very High = 0.76)</div>
<div class="kb-diagram-note">PEXP: 경험 (Very Low = 1.22, Very High = 0.81)</div>
<div class="kb-diagram-note">AEXP: 애플리케이션 경험</div>
<div class="kb-diagram-note">LTEX: 언어/도구 경험</div>
<div class="kb-diagram-note">프로젝트 요인:</div>
<div class="kb-diagram-note">TOOL: 소프트웨어 도구 (Very High = 0.72)</div>
<div class="kb-diagram-note">SITE: 다지점 개발 (Very Low = 1.22)</div>
<div class="kb-diagram-note">SCED: 일정 단축 (Very High = 1.29 ← 압축할수록 증가!)</div>
<div class="kb-diagram-note">SCED 역설:</div>
<div class="kb-diagram-note">일정 단축 25% → 비용 1.29배</div>
<div class="kb-diagram-note">"빨리 하면 더 비싸다!" (잔업, 품질 비용 등)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 비용 드라이버 = 건축 재료비 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) — 고급 재료(RELY=Critical: 1.26배), 최고 건축가(ACAP=Very High: 0.71배로 감소), 일정 단축(SCED: 1.29배!). 고수 팀이 실제로 비용 절감!

---

## Ⅳ. 추정 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">COCOMO II 추정 절차:</div>
<div class="kb-diagram-note">Step 1: 모델 선택</div>
<div class="kb-diagram-note">프로토타입/POC → Application Composition</div>
<div class="kb-diagram-note">초기 설계 단계 → Early Design</div>
<div class="kb-diagram-note">아키텍처 완료 후 → Post-Architecture</div>
<div class="kb-diagram-note">Step 2: 규모 추정</div>
<div class="kb-diagram-note">LOC 직접 산정 또는 기능 점수(FP) 사용</div>
<div class="kb-diagram-note">FP → SLOC 변환 (언어별 SLOC/FP):</div>
<div class="kb-diagram-note">Java: 53 SLOC/FP</div>
<div class="kb-diagram-note">Python: 29 SLOC/FP</div>
<div class="kb-diagram-note">C: 128 SLOC/FP</div>
<div class="kb-diagram-note">예: 500 FP × 53 = 26,500 SLOC = 26.5 KSLOC</div>
<div class="kb-diagram-note">Step 3: SF 및 EM 평가</div>
<div class="kb-diagram-note">팀 전체 워크숍으로 합의</div>
<div class="kb-diagram-note">(개인 추정 아닌 팀 합의 중요)</div>
<div class="kb-diagram-note">Wideband Delphi:</div>
<div class="kb-diagram-note">1. 각 요인 개별 평가</div>
<div class="kb-diagram-note">2. 차이 큰 항목 토론</div>
<div class="kb-diagram-note">3. 재평가 → 수렴</div>
<div class="kb-diagram-note">Step 4: 공수 계산</div>
<div class="kb-diagram-note">PM = 2.94 × (26.5)^1.06 × ∏EMi</div>
<div class="kb-diagram-note">예: SF=1.06, EM 곱=1.15</div>
<div class="kb-diagram-note">PM = 2.94 × 32.1 × 1.15 ≈ 108 PM</div>
<div class="kb-diagram-note">Step 5: 일정 계산</div>
<div class="kb-diagram-note">TDEV = C × (PM)^(D + 0.2 × (SF - B))</div>
<div class="kb-diagram-note">C = 3.67, D = 0.28, B = 0.91</div>
<div class="kb-diagram-note">예: PM=108</div>
<div class="kb-diagram-note">TDEV ≈ 14.2개월</div>
<div class="kb-diagram-note">Step 6: 팀 규모</div>
<div class="kb-diagram-note">Average Staff = PM / TDEV = 108 / 14.2 ≈ 8명</div>
<div class="kb-diagram-note">불확실성 범위:</div>
<div class="kb-diagram-note">Application Composition: ×0.25 ~ ×4</div>
<div class="kb-diagram-note">Early Design: ×0.5 ~ ×2</div>
<div class="kb-diagram-note">Post-Architecture: ×0.75 ~ ×1.25</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II 추정 절차 = 여행 비용 계산 — 목적지(LOC), 이동 수단 난이도(SF), 예상치 못한 비용(EM) 합산. 결과는 범위로(±25%)! 하나의 숫자만 믿으면 위험!

---

## Ⅴ. 실무 시나리오 — 금융 시스템 추정

```
금융 거래 처리 시스템 COCOMO II 추정:

배경:
  새로운 온라인 뱅킹 시스템 개발
  초기 아키텍처 완료
  규모: 1,500 FP (기능 점수) 추정

규모 변환:
  Java 기반: 1,500 FP × 53 SLOC/FP = 79,500 SLOC ≈ 80 KSLOC

SF 평가:
  PREC: Nominal (경험 있음) = 3.72
  FLEX: Low (규제 엄격) = 4.05
  RESL: High (위험 분석 철저) = 2.83
  TEAM: High (경험팀) = 2.19
  PMAT: CMMI Level 3 = 3.12
  
  Σ SFj = 15.91
  SF = 0.91 + 0.01 × 15.91 = 1.07

비용 드라이버 (일부):
  RELY: Very High (금융 시스템) = 1.26
  CPLX: High (복잡한 거래 로직) = 1.17
  ACAP: High (역량 있는 팀) = 0.85
  PCAP: High = 0.88
  TOOL: High (CI/CD, 자동화) = 0.86
  
  EM 곱 = 1.26×1.17×0.85×0.88×0.86 = 0.93

공수 계산:
  PM = 2.94 × (80)^1.07 × 0.93
  PM = 2.94 × 104.4 × 0.93 ≈ 285 PM

일정:
  TDEV = 3.67 × (285)^0.35 ≈ 19.5개월

팀 규모:
  285 / 19.5 ≈ 15명 (평균)

추정 범위 (Post-Architecture ±25%):
  낙관: 214 PM / 14.6개월
  가능성 높음: 285 PM / 19.5개월
  비관: 356 PM / 24.4개월

비용:
  PM당 단가 1,000만원 가정
  비관 시: 35.6억원
  낙관 시: 21.4억원
```

> 📢 **섹션 요약 비유**: 금융 시스템 추정 — 80KSLOC × SF × EM = 285 PM. 금융 규제(RELY×1.26)가 높지만 역량팀(ACAP×0.85)으로 상쇄. 19.5개월, 15명, 비용 범위 21~36억. 범위가 경영진 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 관리의 기초!

---

## 📌 관련 개념 맵

```
COCOMO II
+-- 하위 모델
|   +-- Application Composition (Object Point)
|   +-- Early Design (FP)
|   +-- Post-Architecture (KSLOC)
+-- 핵심 요소
|   +-- SF (Scale Factor): 5개
|   +-- EM (Effort Multiplier): 17개
+-- 산출물
|   +-- PM (공수, Person-Month)
|   +-- TDEV (일정)
|   +-- 팀 규모
+-- 관련 기법
    +-- 기능 점수 (FP)
    +-- Wideband Delphi
    +-- Planning Poker
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[COCOMO I (Barry Boehm, 1981)]
단순 LOC 기반
Organic/Embedded 분류
      |
      v
[기능 점수법 (1979~)]
IFPUG FP 표준화
COCOMO I 한계 보완
      |
      v
[COCOMO II (1995)]
재사용, CBD 반영
SF + 17 EM 도입
      |
      v
[SLIM, Use Case Points (2000s)]
대안 추정 모델
      |
      v
[현재: AI 기반 추정]
ML로 과거 프로젝트 학습
COCOMO II + 데이터 보정
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [COCOMO](/knowledge-base/studynote/12_it_management/04_sdlc_testing/145_cocomo_model/) II = 건물 공사비 견적 — 건물 크기(LOC)만으로 안 돼요. 땅 난이도(SF)와 자재 품질(EM)까지 고려해야 정확한 견적!
2. SF = 공사 어려움 지수 — 처음 짓는 건물(PREC: 낮음), 규제 엄격(FLEX: 낮음) → SF 높아져 같은 크기인데 비용 2배. 경험이 돈!
3. 추정 결과는 범위 — 285 PM 추정이지만 ±25%로 214~356 PM. 한 숫자만 믿으면 위험. 범위 제시가 올바른 추정!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 973

← **이전**: [047. COCOMO 모델 — 소프트웨어 비용 추정](/knowledge-base/studynote/04_software_engineering/01_overview_principles/047_cocomo_model/)
**다음**: [049. 기능 점수 — Function Point (FP) Estimation](/knowledge-base/studynote/04_software_engineering/01_overview_principles/049_function_point_fp_estimation/) →

---
