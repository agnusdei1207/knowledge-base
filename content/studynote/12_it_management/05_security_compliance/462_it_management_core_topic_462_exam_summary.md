+++
title = "462. IT 경영 관리 핵심 토픽 462번 시험 요약 (IT Management Core Topic 462 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 462. IT 경영 관리 핵심 토픽 — 462번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance, ITG)는 COBIT 2019, ISO/IEC 38500, ITIL 4, PMBOK 7th, ISO 27001, TOGAF 등 다중 프레임워크를 **거버넌스–전략–포트폴리오–서비스–보안–감리**의 6대 축으로 통합하여, 기업이 IT 자산을 통해 비즈니스 가치를 극대화하고 리스크를 통제하는 의사결정 체계이다.
> 2. **가치**: McKinsey·Gartner·한국정보화진흥원 다수 실증 사례에서 **COBIT 5 이상 도입 기업의 IT 비용 20~35% 절감, 프로젝트 성공률 30%p 이상 향상, ISMS 인증 기업의 보안사고 1/3 수준 감소, EVM 기반 EV·SPI·CPI가 ±0.05 이내 통제 시 일정·원가 예측 정확도 90% 이상** 달성 가능.
> 3. **판단 포인트**: ①CoBIT cascade와 Strategy Map을 통한 **Value Goal ↔ Enterprise Goal ↔ IT Goal**의 3단 정렬, ②IT 인Vestment 결정 시 **NPV·IRR·Payback Period·TCO·VOI(Value on Investment)** 5대 재무지표와 정성 BSC의 **Learning & Growth·Internal Process·Customer·Financial** 관점 동시 사용, ③아웃소싱은 **Make-or-Buy·SLA·OLA·UC·KSF** 기반으로 통제, ④디지털 전환 시대에는 **Cloud Economics(FinOps), AI 거버넌스, 데이터 거버넌스(DAMA-DMBOK2)** 가 추가 판단축으로 부상.

---

## Ⅰ. 개요 및 필요성

정보시스템 감리·정보관리·컴퓨터시스템응용 기술사 시험의 462번 토픽은 **"IT 경영(Information Technology Management)"** 의 총론적 영역으로, 기업이 IT를 단순 비용센터가 아닌 **전략적 가치 창출 자산(Value Driver)** 으로 전환시키기 위한 관리체계의 설계·운영·평가를 다룬다. 한국정보화진흥원(NIA)의 *정보시스템 감리 가이드라인*, 디지털정부 표준프레임워크, 공공기관 정보화 예산 편성 지침 등은 본 토픽의 정책적 근거이며, 글로벌 표준으로는 COBIT 2019(ISACA), ISO/IEC 38500:2015, ITIL 4(Axelos), PMBOK 7th(PMI), TOGAF 10(The Open Group), DAMA-DMBOK 2.0이 핵심이다.

최근 5년간 기업 IT 환경은 **①클라우드 네이티브(SaaS·IaaS·PaaS·FaaS)**, **②AI/ML·LLM 기반 의사결정 자동화**, **③제로트러스트·SASE 보안 패러다임**, **④데이터 중심 거버넌스(Data Mesh·Data Fabric)**, **⑤ESG·디지털 윤리** 등으로 급변하여, 전통적인 "IT 운영 효율성" 중심에서 **"비즈니스 Outcomes 책임"** 중심으로 거버넌스의 무게중심이 이동하고 있다. 이에 따라 기술사 응시자는 단순히 프레임워크 이름을 나열하는 수준을 넘어, **프레임워크 간 상호운용성(Interoperability), 목표 정렬(Alignment), 성과 측정 메커니즘, 그리고 리스크 통제 구조**를 통합적으로 설계할 수 있는 역량을 입증해야 한다.

```text
┌────────────────────────────────────────────────────────────────────────┐
│              IT 경영 관리 6대 통합 거버넌스 프레임워크                  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  [Stakeholders]                                                       │
│   Board / CxO / Regulators / Customers / Shareholders                  │
│         │                                                              │
│         ▼  (Accountability)                                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ 1. Governance    │  │ 2. Strategy      │  │ 3. Portfolio     │   │
│  │   COBIT 2019     │◄─┤   Plan/Acquire   │◄─┤   Mgmt          │   │
│  │   ISO 38500      │  │   TOGAF ADM      │  │   PMBOK/SAFe    │   │
│  │   Three Lines    │  │   Strategy Map   │  │   BIM/EVM       │   │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘   │
│           │                     │                     │                │
│           ▼                     ▼                     ▼                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ 4. Service Mgmt  │  │ 5. Security      │  │ 6. Risk & Audit  │   │
│  │   ITIL 4 SVS     │  │   ISO 27001/02  │  │   IIA 3 Lines    │   │
│  │   SIAM           │  │   ISMS-P / K-  │  │   COBIT EDM      │   │
│  │   FinOps         │  │   ISMS / NIST  │  │   KRISC/감리    │   │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘   │
│           │                     │                     │                │
│           └─────────────────────┼─────────────────────┘                │
│                                 ▼                                      │
│                   ┌────────────────────────────┐                       │
│                   │  Value Realization Engine  │                       │
│                   │  KPI/OKR/BSC/Earned Value  │                       │
│                   │  Benefits Realization Plan │                       │
│                   └────────────────────────────┘                       │
└────────────────────────────────────────────────────────────────────────┘
```

**전통적 IT 관리 vs. 디지털 시대 IT 경영 비교**

| 구분 | 전통적 IT 관리 (1990~2010) | 디지털 시대 IT 경영 (2015~현재) |
|---|---|---|
| 관점 | IT 비용·효율성·안정성 중심 | 비즈니스 가치·경험·혁신 중심 |
| 거버넌스 모델 | 중앙 집중·계층형·프로세스 지향 | 분산·제품 중심·플랫폼·에코시스템 지향 |
| 프레임워크 | ITIL v2/v3, COBIT 5, PMBOK 5 | COBIT 2019, ITIL 4, PMBOK 7, OKR, SRE, FinOps |
| 투자 평가 | ROI·Payback·TCO | NPV·IRR·VOI·옵션가치·플랫폼 가치 |
| 보안 모델 | Perimeter·방어 중심 | Zero Trust·SASE·DevSecOps·신원중심 |
| 조직 구조 | IT 부서 수직·사일로 | BizDevOps·Squad·Product Team·Federated |
| 데이터 | 데이터 웨어하우스·ETL | Data Lakehouse·Lake·Mesh·Fabric |
| 의사결정 | 경험·계층 결재 | 데이터·AI·실시간 의사결정 인텔리전스 |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 도시계획·교통·치안·재무·건축 5개 부처를 한 개의 "스마트시티 통합관제센터"로 묶어 운영하는 것**과 같다. 각 부처의 개별 KPI만 따지면 도로·교량은 생기지만, 도시 전체의 교통 흐름·안전·시민 만족도는 무너진다. 거버넌스(COBIT)는 도시헌장, 전략(TOGAF)은 토지이용계획, 포트폴리오(PMBOK)는 건축허가, 서비스(ITIL)는 교통운영, 보안(ISO 27001)은 경찰·소방, 리스크(감리)는 감사원으로 대응되는 셈이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 6대 축은 **"E2E Value Chain(End-to-End Value Chain)"** 으로 표현된다. Stakeholder Needs & Goals(상위)에서 출발하여 Benefits Realization(하위)에 이르는 5단계의 인과 루프(Causal Loop)를 따른다. 이 인과 관계는 COBIT 2019의 **Goals Cascade** 가 가장 정제된 형태로 표현하며, 동시에 Kaplan-Norton의 **Strategy Map 4 Perspective(Financial·Customer·Internal Process·Learning & Growth)** 와 **Balanced Scorecard(BSC)** 로 정량화된다.

### 1) 거버넌스·전략·포트폴리오 정렬 메커니즘 (COBIT 2019 + ISO 38500)

COBIT 2019는 **40개 Governance & Management Objective** 를 5개 도메인(EDM·APO·BAI·DSS·MEA)으로 구조화한다. ISO/IEC 38500:2015는 **6원칙(Responsibility·Strategy·Acquisition·Performance·Conformance·Human Behavior)** 과 **3계층 모델(Direct·Manage·Monitor)** 을 제시한다. 이 둘은 **Principle → Goal → Practice → Process → Activity → Metric** 의 6단 위계로 정렬된다.

### 2) IT 투자 가치 평가 알고리즘

IT 투자의 재무적 정당성은 5대 지표로 평가하며, 할인을 포함한 NPV(순현재가치)가 **1차 관문** 이다. VOI(Value on Investment)는 **Net Benefit = (Tangible + Intangible) − Cost** 로 산정하고, Risk-Adjusted ROI = (기대이익 − 기댓값 손실) / 총투자 × 100 으로 보정한다. **Real Options Valuation(Black-Scholes 확장)** 은 향후 2~3년 시점에 추가 기능·중단·확장 의사결정의 유연성을 화폐가치로 환산한다.

- **NPV** = Σ( CF_t / (1+r)^t ) − I₀  
- **IRR**: NPV=0이 되는 할인율 r, **Hurdle Rate(또는 WACC+α)** 와 비교  
- **Payback Period** = 투자금 회수에 소요되는 기간 (Discounted Payback은 NPV 기준)  
- **TCO**(Total Cost of Ownership) = 직접비(HW·SW·인력) + 간접비(교육·다운타임·보안) + 기회비용  
- **VOI** = (B_tangible + B_intangible) − TCO

### 3) 프로젝트 성과 측정 — Earned Value Management(EVM)

PMBOK 7th + ANSI EIA 748의 EVM은 3개 기준값 **PV(Planned Value)·EV(Earned Value)·AC(Actual Cost)** 으로부터 4개 지표 **SV·CV·SPI·CPI** 와 2개 예측지표 **EAC·ETC·VAC·TCPI** 를 산출한다.

- SV = EV − PV, CV = EV − AC
- SPI = EV/PV (>1.0 = 앞서나감), CPI = EV/AC (>1.0 = 원가절감)
- EAC = AC + (BAC − EV) / CPI  (현재 CPI 지속 가정)
- VAC = BAC − EAC, TCPI = (BAC − EV) / (BAC − AC)

```text
┌─────────────────────────────────────────────────────────────────────────┐
│        IT 경영 6축 End-to-End Value Chain (E2E-VC)                      │
└─────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────┐
   │  ① Stakeholder Drivers (Regulation·Market·Shareholder)    │
   └──────────────────────────┬───────────────────────────────┘
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │  ② Governance (COBIT EDM / ISO 38500 Evaluate·Direct·   │
   │   Monitor / Board IT Steering Committee)                 │
   │   - 책임원칙, 전략원칙, 성과원칙, 준수원칙               │
   └──────────────────────────┬───────────────────────────────┘
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │  ③ Strategy (TOGAF ADM Preliminary~Phase G·H /          │
   │   BSC 4 관점 정렬 / OKR Cascade)                         │
   │   Enterprise Goal ──▶ IT Goal ──▶ Enabler Goal            │
   └──────────────────────────┬───────────────────────────────┘
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │  ④ Portfolio & Program (PMBOK 7·SAFe·EVM)                │
   │   - Idea → Charter → Roadmap → Benefit Realization        │
   │   - KPI: NPV·IRR·SPI·CPI·Risk Score·Strategic Fit       │
   └──────────────────────────┬───────────────────────────────┘
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │  ⑤ Service & Operation (ITIL 4 SVS·SIAM·FinOps)         │
   │   34 Practice (General·Service·Technical·Management)     │
   │   - SLA·OLA·UC·Availability·MTTR·MTBF                    │
   └──────────────────────────┬───────────────────────────────┘
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │  ⑥ Value Realization (BSC·OKR·Benefits Realization Plan)│
   │   - KPI/CSF/KPI Tree / VOI Tracking Dashboard            │
   │   - Benefits Owner·Stage Gate·Post-Implementation Review │
   └──────────────────────────────────────────────────────────┘

[보조 통제축 — Risk·Security·Audit]
  • ISMS-P / ISO 27001/27002 / NIST CSF / Zero Trust
  • Three Lines Model (IIA)
  • 감리법 제33조(개발·운영·폐기)·제34조
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 462 / 800

← **이전**: [461. IT 경영 관리 핵심 토픽 461번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/461_it_management_core_topic_461_exam_summary/)
**다음**: [463. IT 경영 관리 핵심 토픽 463번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/463_it_management_core_topic_463_exam_summary/) →

---
