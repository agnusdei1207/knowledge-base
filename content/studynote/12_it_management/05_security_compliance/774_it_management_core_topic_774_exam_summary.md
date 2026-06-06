---
title: "IT Management Core Topic 774 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 투자관리(IT Investment Management)는 IT 거버넌스(COBIT 2019, ISO/IEC 38500) 체제하에서 포트폴리오·프로그램·프로젝트 3계층의 투자 의사결정과 BSC·KPI·EVA·NPV/IRR·TCO 등 정량·정성 측정지표를 통합하여 **Business Value of IT(정보기술의 비즈니스 가치, 이하 BVIT)**를 극대화하는 경영 활동이다.
> 2. **가치**: Gartner(2023) 및 한국정보화진흥원 조사에 따르면 체계적 IT 투자관리 체계 도입 기업은 IT 예산 대비 **ROI 18~32% 향상**, 투자 실패율(Significant Failure Rate) **40% -> 12%** 감소, **TCO 23~28% 절감**, 의사결정 리드타임 **약 60% 단축** 효과를 거둘 수 있다.
> 3. **판단 포인트**: 기술사 관점에서 가장 중요한 판단축은 ① Run(운영·유지) vs Grow(확장·혁신) vs Transform(패러다임 전환) 간 **투자 비중 배분**, ② 정량 KPI(재무)와 정성 KPI(고객·프로세스·학습성장) 간 **Balanced Scorecard(균형성과표) 가중치 설계**, ③ Stage-Gate(단계별 관문) 평가 시 **NPV/IRR + 전략 정합성 + 위험도**의 다차원 의사결정 매트릭스 운용이다.

---

## Ⅰ. 개요 및 필요성

정보시스템은 1960년대 단순 데이터 처리(EAM, MIS)에서 1980년대 전략정보시스템(SIS), 2000년대 ERP/CRM/SCM 패키지 기반 통합, 2010년대 클라우드·모바일·빅데이터, 2020년대 AI·생성형 AI·엣지컴퓨팅으로 진화해 왔다. 그러나 **McKinsey & Company(2022) "Tech Performance Index"** 보고에 따르면 전체 IT 프로젝트 중 **약 70%가 비즈니스 목표를 초과 달성하지 못하고 있으며**, 한국정보화진흥원(KIAT) 2023년 조사에서도 국내 대기업 IT 투자 중 **42.3%가 "성과 불확실"** 또는 **"투자 회수 미달"**로 평가된다.

이러한 실패는 대부분 ① 투자 결정 단계의 비과학성, ② 성과 측정 지표의 부재, ③ 사후 평가(Post-Implementation Review, PIR) 미실시, ④ IT-Business 정렬(Strategic Alignment) 결여에서 기인한다. 이에 IT 투자관리는 단순한 예산 통제가 아니라 **"전략적 의사결정 -> 포트폴리오 배분 -> 정량·정성 평가 -> 학습 및 피드백"**의闭环(Closed-Loop) 프로세스로 인식되어야 한다.

특히 **ISO/IEC 38500:2015 IT Governance Standard**는 "Evaluate -> Direct -> Monitor" 3단계로 IT 투자 결정을 구조화하고, **COBIT 2019**는 40개의 Governance & Management Objectives 중 **"EDM02 – Ensured Benefits Delivery"**, **"EDM03 – Optimized Risk"**, **"APO05 – Managed Portfolio"**, **"APO06 – Managed Budget and Costs"**, **"MEA04 – Managed Performance Evaluation"**을 통해 IT 투자관리의 국제 표준 참조체계를 제시한다.

```text
[IT 투자관리의 패러다임 전환 - Old vs New Paradigm]

   [ Old Paradigm (1990s) ]              [ New Paradigm (2020s) ]
   +------------------------+            +-----------------------------+
   | IT = Cost Center       |            | IT = Value & Growth Engine  |
   | 예산 = 연간 고정 배분   |            | 예산 = 동적 포트폴리오 재배분|
   | ROI 단일 지표 의존     |            | BSC × EVA × NPV 다차원 평가|
   | 사후 평가 부재         |            | PIR + Stage-Gate 지속 모니터|
   | IT 부서 독자 의사결정   |            | IT-Business 공동 거버넌스   |
   +------------------------+            +-----------------------------+
            |                                       |
            +-------------- IT 거버넌스 체계 진화 ----+
                  (COBIT 4.1 -> 5 -> 2019, ITIL v2->v3->2011->4)
```

- **📢 섹션 요약 비유**: IT 투자관리는 마치 **가정의 재무설계**와 같습니다. 단순히 "월 얼마 쓸까"가 아니라, 자녀교육(성장투자), 노후준비(안정투자), 비상금(위험대비), 자산증식(공격투자) 비율을 생애주기별로 재조정하는 **동적 자산배분(Asset Allocation) 전략**이 핵심입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 투자관리는 ① **전략 정렬 계층(Strategy Layer)**, ② **포트폴리오·프로그램·프로젝트 계층(Investment Layer)**, ③ **성과 측정 계층(Performance Layer)**, ④ **위험·컴플라이언스 계층(Governance Layer)**의 4계층 아키텍처로 구성된다.

```text
[IT 투자관리 4계층 참조 아키텍처]

  +---------------------------------------------------------------+
  | ① 전략 정렬 계층 (Strategy Alignment Layer)                    |
  |   - ISP(Information Strategy Planning)                         |
  |   - EA(Enterprise Architecture) 기반 To-Be 모델링             |
  |   - BSC 4관점(재무/고객/내부프로세스/학습성장) 전략맵            |
  +------------------------+--------------------------------------+
                           | (Strategic Filter)
                           v
  +---------------------------------------------------------------+
  | ② 투자 의사결정 계층 (Investment Decision Layer)                |
  |   +--------------+ +--------------+ +----------------------+|
  |   | Portfolio    |->| Program      |->| Project              ||
  |   | (전사 IT자산) | | (전략이니셔) | | (실행단위)             ||
  |   | Mix 최적화   | | Benefits Map | | Stage-Gate 통제       ||
  |   +--------------+ +--------------+ +----------------------+|
  +------------------------+--------------------------------------+
                           | (Performance Feedback)
                           v
  +---------------------------------------------------------------+
  | ③ 성과 측정 계층 (Performance Measurement Layer)               |
  |   - 재무 KPI: NPV, IRR, ROI, Payback Period, EVA              |
  |   - 정성 KPI: 사용자만족도(CSI), 시스템가용성(SLA), NPS        |
  |   - BSC 관점별 Lead/Lag Indicator, KPI Cascade               |
  +------------------------+--------------------------------------+
                           | (Risk & Compliance Hook)
                           v
  +---------------------------------------------------------------+
  | ④ 거버넌스·위험 계층 (Governance & Risk Layer)                  |
  |   - COBIT 2019 EDM/ APO/ BAI/ DSS/ MEA 프로세스              |
  |   - ISO/IEC 38500 (Evaluate-Direct-Monitor)                    |
  |   - ISO 31000 Risk Management                                  |
  |   - 내부통제(Internal Control) 및 컴플라이언스(Compliance)      |
  +---------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee (IT운영위원회)** | 전사 IT 투자 우선순위 결정, 정족수(Quorum) 50% 이상 의사결정 | CIO(Chief Information Officer) 의장, CFO·COO·사업본부장 참석. **RACI(Responsible, Accountable, Consulted, Informed)** 매트릭스 기반 역할 분담. 분기 1회 이상 정기 개최, 안건 24시간 사전 공지 |
| **PMO (Project Management Office)** | 프로젝트 단위 Stage-Gate 관문(Concept -> Planning -> Development -> Test -> Launch -> Close) 관리 | **Stage-Gate®(Cooper, 1990) 5-Gate 모델** 적용. Gate별 Go/Kill/Hold/Recycle 결정. **Earned Value Management(EVM, 획득가치관리)** 지표(CPI, SPI) 활용 |
| **Portfolio Management Office** | 전략적 관점의 Run-Grow-Transform 비중 최적화, 정시조정(Rebalancing) | **Markowitz 포트폴리오 이론**의 Risk-Return 트레이드오프를 IT 자산군에 적용. **Bubble Chart(X축: 리스크, Y축: BVIT, 버블크기: 투자금액)**로 시각화 |
| **Benefits Realization Office (BRO)** | 투자 편익의 실현 추적 및 미실현 시 시정조치 | **Benefits Map(입력->활동->출력->결과->편익)** 5단계 인과모델. **Benefits Tracking Register** 운영, 분기별 Benefits Health Check |
| **IT Finance / TCO 모델** | 총소유비용(Total Cost of Ownership) 산정 및 라이프사이클 비용 관리 | **Gartner TCO 모델**: ① 하드웨어/소프트웨어 Acquisition(1~3년), ② Implementation(1년), ③ Operation(5~7년), ④ Decommission(0.5년) **4단계 비용 분류**. CapEx vs OpEx 분류 정확히 수행 |
| **KPI 대시보드 (BSC 기반)** | 전략목표 -> 핵심성과지표 -> 측정지표 -> 목표값 4단계 캐스케이드 | **GQM(Goal-Question-Metric)** 기법으로 도출. **KPI Library** 표준화(예: 시스템가용성 ≥99.95%, MTTR ≤30분, NPS ≥40, ROI ≥15%) |
| **PIR (Post-Implementation Review)** | 투자 완료 후 6~12개월 시점 정량·정성 회고평가 | **5 Why 분석, Fishbone Diagram, PDCA(Plan-Do-Check-Act)**. 차기 투자 의사결정에 학습 결과 반영(Closed-Loop) |

### 핵심 정량 평가 모델 Deep-Dive

**① NPV(순현재가치, Net Present Value)**
```
NPV = Σ (CF_t / (1+r)^t)  -  Initial Investment

여기서:
  CF_t = t기 순현금흐름(영업현금흐름 - 투자액)
  r    = 할인율(할인율 = 무위험이자율 + 베타 × 시장위험프리미엄, WACC 적용)
  t    = 투자 회수 기간(통상 3~5년)
  판정: NPV > 0 -> Go / NPV = 0 -> Indifferent / NPV < 0 -> No-Go
```

**② IRR(내부수익률, Internal Rate of Return)**
```
NPV = 0 이 되는 할인율 r*을 IRR로 정의
판정: IRR > Hurdle Rate(통상 12~15%) -> Go
민감도 분석: 할인율 ±2%, CF ±10% 변동 시 NPV 변동폭 검토
```

**③ EVA(경제적부가가치, Economic Value Added)**
```
EVA = NOPAT - (WACC × Invested Capital)
  NOPAT(Net Operating Profit After Tax) = 영업이익 × (1 - 세율)
  WACC = (E/V × Re) + (D/V × Rd × (1-T))
  판정: EVA > 0 -> Value Creation / EVA < 0 -> Value Destruction
```

**④ TCO(Total Cost of Ownership) - Gartner 4계층 모델**
```
TCO = Direct Costs + Indirect Costs + Intangible Costs + Risk-adjusted Costs
     (직접비)        (간접비)         (무형비)         (리스크 조정비)
   = HW+SW+인력+      + 교육+관리+     + 기회비용+      + 장애/보안/규제
     도입+운영         + 다운타임        + 생산성손실        위반 비용
```

**⑤ Balanced Scorecard for IT (Norton & Kaplan 확장 모델)**
- **재무 관점**: Cost Reduction(%), Revenue Growth from New IT Services, ROI
- **고객 관점**: End-User Satisfaction(%), First Call Resolution, NPS
- **내부 프로세스 관점**: Incident Resolution Time, Change Success Rate, SLA Compliance
- **학습·성장 관점**: IT Staff Skill Index, Innovation Pipeline, Knowledge Retention Rate

- **📢 섹션 요약 비유**: NPV/IRR은 **자동차의 속도계와 연비계**, EVA는 **네비게이션의 목적지까지 남은 거리**, BSC는 **차량 상태를 종합적으로 보여주는 HUD(Head-Up Display)**입니다. 단일 지표만 보면 방향을 잃지만, 4개 지표를 함께 보면 목적지까지 안전·경제적·신속하게 도달할 수 있습니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **PMBOK 7th** | **Val IT 2.0** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스/관리 목표 40개 체계 | IT 서비스 운영·관리 Best Practice | IT 의사결정·감독 국제표준 | 프로젝트 관리 지식체계 | IT 투자·성과 거버넌스 특화 |
| **투자관리 비중** | EDM/ APO 영역에 간접 포함
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 774 / 800

<- **이전**: [773. IT 경영 관리 핵심 토픽 773번 시험 요약](/studynote/12_it_management/05_security_compliance/773_it_management_core_topic_773_exam_summary/)
**다음**: [775. IT 경영 관리 핵심 토픽 775번 시험 요약](/studynote/12_it_management/05_security_compliance/775_it_management_core_topic_775_exam_summary/) ->

---
