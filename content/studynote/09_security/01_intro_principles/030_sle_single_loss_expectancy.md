---
title: "030. Sle Single Loss Expectancy"
date: "2026-04-29"
tags:
  - "studynote-security"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLE(Single Loss Expectancy, 단일 손실 기대값)은 보안 사고 한 번 발생 시 예상 손실액이고, [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/)(Annual Loss Expectancy, 연간 손실 기대값)은 연간 기대 손실액이다. [정량적 위험 분석](/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/)의 핵심 계산식이다.
> 2. **가치**: [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) = SLE × ARO(Annual Rate of Occurrence, 연간 발생 빈도)로 계산된다. ALE가 보안 통제 비용보다 크면 투자가 정당화된다. 이것이 보안 투자 [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 계산의 기반이다.
> 3. **판단 포인트**: SLE = 자산가치([AV](/studynote/09_security/04_endpoint_security/323_antivirus/), Asset Value) × 노출 인자(EF, Exposure Factor). EF는 0~1 사이 비율로 사고 발생 시 자산의 몇 %가 손실되는지를 나타낸다.

---

## Ⅰ. 개요 및 필요성

```text
정량적 위험 분석 계산식:

  SLE = AV × EF
  ALE = SLE × ARO

  예시:
  - 서버 자산 가치(AV): 1억 원
  - 화재 시 손실 비율(EF): 60%
  - SLE = 1억 × 0.6 = 6,000만 원
  - 연간 화재 발생 빈도(ARO): 0.1회/년 (10년에 1번)
  - ALE = 6,000만 × 0.1 = 600만 원/년

  -> 화재 억제 시스템 설치 비용 < 600만 원/년 이면 투자 정당화
```

- **📢 섹션 요약 비유**: [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) 계산은 자동차 보험료 산정과 같다. 사고 시 수리비(SLE)에 연간 사고 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)(ARO)을 곱해서 연간 기대 손실([ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/))을 산출하고, 이를 기준으로 보험료(보안 투자)를 정당화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 보안 통제 적용 후 [잔여 위험](/studynote/09_security/01_intro_principles/038_residual_risk/)

```text
보안 투자 타당성:

  통제 전 ALE (Before)
  - 통제 구현 비용 (Annual Cost of Safeguard)
  - 통제 후 ALE (After)
  = 순 절감액 (Value of Safeguard)

  순 절감액 > 0 -> 투자 타당
  순 절감액 < 0 -> 투자 불필요 (과잉 투자)
```

### 자산 가치 산정 요소

| 요소 | 내용 |
|:---|:---|
| **대체 비용** | 자산 재구매·재구축 비용 |
| **생산성 손실** | 다운타임 중 비즈니스 손실 |
| **법적 책임** | 고객 정보 유출 벌금·소송 |
| **평판 손상** | 브랜드 가치 하락 |
| <strong><a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 비용</strong> | [인시던트 대응](/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/)·포렌식 비용 |

- **📢 섹션 요약 비유**: 자산 가치 산정은 보석 감정이다. 보석의 재료 가격(대체 비용)만이 아니라 역사적 가치(평판)·보험 가치(법적 책임)·생산성 가치를 모두 합쳐서 전체 자산 가치를 계산한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 정량적 분석 | 정성적 분석 |
|:---|:---|:---|
| 도구 | SLE·[ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/), [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)·금액 | 위험 매트릭스, 색상 등급 |
| 장점 | 객관적·[ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 계산 | 빠른 분석·전문가 직관 |
| 단점 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 어려움 | 주관적·비교 어려움 |
| 적합 | 대규모 인프라 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·소규모 |

- **📢 섹션 요약 비유**: 정량적 vs [정성적 위험 분석](/studynote/09_security/01_intro_principles/029_qualitative_risk_analysis/)은 건강 검진과 의사 진찰이다. 혈액 검사(정량적)는 수치로 정확히 알지만 시간이 걸리고, 의사 직관(정성적)은 빠르지만 주관적이다. 둘 다 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 사이버 보안 [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) 실제 사례

```text
랜섬웨어 사고:
  AV = 10억 원 (데이터·시스템 가치)
  EF = 0.7 (70% 복구 불가 가정)
  SLE = 7억 원
  ARO = 0.3 (3년에 1번 발생)
  ALE = 7억 × 0.3 = 2.1억 원/년

  -> 백업 솔루션 구축 비용 연 5,000만 원 < 2.1억 원
     -> 투자 타당 (1.6억 원/년 절감)
```

### FAIR (Factor Analysis of Information [Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/))

```text
FAIR = 현대화된 정량적 위험 분석 표준
  - SLE/ALE 개념을 확장
  - 위협 이벤트 빈도(TEF)·통제 강도 통합
  - 몬테카를로 시뮬레이션으로 확률 분포 분석
  - 금융 리스크 관리 방법론 차용
```

- **📢 섹션 요약 비유**: FAIR는 기상 예보 업그레이드다. 단순 SLE/[ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/)("내일 비 올 것 같다")에서 FAIR("70% [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)로 20~30mm 강수, 범위: 15~40mm")처럼 정확한 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 분포로 위험을 분석한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **투자 정당화** | [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) 기반 보안 [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 산출 |
| **우선순위 결정** | [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) 높은 위험 먼저 처리 |
| **경영진 소통** | 금액으로 표현해 경영진 설득 |

[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 위험 정량화 플랫폼이 등장하고 있다. 사고 사례 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)·인더스트리 벤치마크·실시간 위협 인텔리전스를 자동 분석하여 ALE를 동적으로 산출하고, 보안 투자 포트폴리오 최적화까지 제안하는 CTEM(Continuous Threat Exposure [Management](/studynote/12_it_management/05_security_compliance/1013_management/)) 플랫폼이 발전하고 있다.

- **📢 섹션 요약 비유**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 위험 정량화는 자율주행 보험 동적 프리미엄이다. 실시간 운전 습관·도로 상황·날씨를 분석해 매 순간 보험료([ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/))를 재계산하는 것처럼, AI가 실시간 위협 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 보안 위험값을 업데이트한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/09_security/04_endpoint_security/323_antivirus/">AV</a>·EF·ARO</strong> | SLE·[ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) 계산의 3요소 |
| **FAIR** | 현대 [정량적 위험 분석](/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/) 표준 |
| **위험 매트릭스** | [정성적 위험 분석](/studynote/09_security/01_intro_principles/029_qualitative_risk_analysis/) 도구 |
| **CTEM** | 지속적 위협 노출 관리 플랫폼 |
| <strong>보안 <a href="/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/">ROI</a></strong> | [ALE](/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) 기반 투자 타당성 계산 |

### 📈 관련 키워드 및 발전 흐름도

```text
[정성적 위험 분석 — 위험 매트릭스, 색상 등급]
    |
    v
[SLE / ALE — 단일·연간 손실 기대값 정량화]
    |
    v
[FAIR — 확률 분포 기반 현대 정량적 위험 분석]
    |
    v
[몬테카를로 시뮬레이션 — 위험 범위 확률 분포]
    |
    v
[CTEM — AI 기반 실시간 연속 위협 노출 관리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SLE는 자동차 사고 한 번의 수리비예요! 사고 났을 때 얼마나 손해인지 계산한 거예요.
2. ALE는 1년 동안 예상되는 총 손해액이에요 — 수리비 × 연간 사고 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)이에요!
3. ALE가 보안 시스템 설치 비용보다 크면 투자하는 게 이익이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 1108

<- **이전**: [29. 정성적 위험 분석 (Qualitative Risk Analysis)](/studynote/09_security/01_intro_principles/029_qualitative_risk_analysis/)
**다음**: [31. ARO와 위험 정량화 — 연간 발생률의 의미](/studynote/09_security/01_intro_principles/031_aro_annual_rate_of_occurrence/) ->

---
