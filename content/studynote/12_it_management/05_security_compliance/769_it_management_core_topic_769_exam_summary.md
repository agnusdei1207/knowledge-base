---
title: "IT Management Core Topic 769 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019 거버넌스 프레임워크**, **ITIL 4 서비스 가치 시스템(SVS)**, **TOGAF ADM**, **PMBOK 7th**, **CMMI-DEV v2.0** 등 5대 글로벌 프레임워크를 **전략-거버넌스-운영-아키텍처-프로젝트** 5계층으로 통합하여, IT 투자 대비 비즈니스 가치(ROI, NPV, EVA)를 극대화하는 경영 체계임.
> 2. **가치**: McKinsey & Company(2023) 보고에 따르면 성숙한 IT 거버넌스 도입 기업은 **TCO 23% 절감**, **Time-to-Market 38% 단축**, **프로젝트 성공률 67% -> 89% 향상**, **정보화 사업 감사 지적사항 74% 감소** 등 정량적 효과를 달성하며, **ISO 38500** 기반 IT 거버넌스 평가 시 IT 성숙도 Level 3(Defined) -> Level 4(Managed) 도달 가능.
> 3. **판단 포인트**: 기술사 시험 핵심은 **"프레임워크 간 충돌 해결"** — 예) COBIT의 **RACI 매트릭스**와 RACI of PMBOK의 중복, ITIL 4의 **34개 Practice**와 COBIT 2019의 **40개 Governance/Management Objective** 매핑, 그리고 한국 **전자정부법 제46조(정보화 사업 수행 절차)**, **클라우드컴퓨팅법**, **개인정보보호법** 등 국내 법·제도를 글로벌 프레임워크와 어떻게 정합(Align)시키느냐가 합격 결정 요인.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(IT Management)는 단순히 시스템을 "운영"하는 차원을 넘어, **기업의 비즈니스 전략과 IT 자산을 정렬(Strategic Alignment)**시키고, **가치(Value)**를 창출하며, **위험(Risk)**을 통제하는 통합 경영 활동입니다. 정보통신산업진흥원(NIPA)과 한국정보화진흥원(KADO)의 통계에 따르면, 국내 500대 기업의 IT 예산은 매출액 대비 평균 **2.8%**(2024년 기준)에 달하며, 이중 약 **35%가 비효율적으로 집행**되는 것으로 나타납니다. 기술사 시험에서는 이러한 비효율의 근본 원인을 진단하고, 글로벌 표준 프레임워크를 기반으로 한 **체계적 개선 방안**을 제시할 수 있는 역량을 평가합니다.

4차 산업혁명 시대의 IT 환경은 **클라우드 네이티브**(AWS, Azure, GCP), **AI/ML 기반 의사결정**, **제로트러스트 보안**, **DevSecOps**, **엣지 컴퓨팅** 등으로 급변하면서, 전통적인 **"IT는 비용(Cost Center)"** 관점에서 **"IT는 가치 창출 엔진(Profit Enabler)"**로의 패러다임 전환이 필수입니다. McKinsey Global Survey(2024)에 따르면, AI와 자동화를 적극 도입한 기업은 **EBITDA 마진이 평균 5.2%p 상승**했지만, 이를 체계적으로 관리하지 못한 기업은 오히려 **투자 회수 실패율 42%**를 경험했습니다. 이러한 격차는 **IT 거버넌스 성숙도**에 직접적으로 기인합니다.

```text
+------------------------------------------------------------------------+
|              IT 경영 관리 5계층 통합 프레임워크 (5-Layer Model)         |
+------------------------------------------------------------------------+
|                                                                        |
|  Layer 1: 전략 (Strategy) ------------------------------------------  |
|  +--------------------------------------------------------------+    |
|  |  • 비즈니스 전략 (Porter, Hammer & Champy)                   |    |
|  |  • IT 전략 (Ward & Peppard Balanced Scorecard)               |    |
|  |  • 디지털 전환 로드맵 (BCG, McKinsey Digital)                |    |
|  |  • ISO 38500 IT 거버넌스 원칙 (Responsibility, Strategy,    |    |
|  |    Acquisition, Performance, Conformance, Human Behavior)    |    |
|  +--------------------------------------------------------------+    |
|                              v 정렬(Alignment)                          |
|  Layer 2: 거버넌스 (Governance) ------------------------------------  |
|  +--------------------------------------------------------------+    |
|  |  • COBIT 2019 (40 Governance/Management Objectives)         |    |
|  |  • 이사회-경영진-IT 조직 RACI 매트릭스                       |    |
|  |  • 정보화 전략위원회(ISP) - 전자정부법 §14                    |    |
|  |  • IT 감사 (ISACA CISA, ISO 27001)                          |    |
|  +--------------------------------------------------------------+    |
|                              v 통제(Control)                            |
|  Layer 3: 아키텍처 (Architecture) ---------------------------------  |
|  +--------------------------------------------------------------+    |
|  |  • TOGAF 10 ADM (Architecture Development Method)           |    |
|  |  • Zachman Framework (6x6 매트릭스)                         |    |
|  |  • 한국 EA 참조모델 (KR EA v2.0)                            |    |
|  |  • 도메인: BA, DA, AA, TA (NIST EA)                         |    |
|  +--------------------------------------------------------------+    |
|                              v 전달(Delivery)                           |
|  Layer 4: 프로젝트 & 운영 (Project & Operation) -------------------  |
|  +--------------------------------------------------------------+    |
|  |  • PMBOK 7th (8 Performance Domains)                        |    |
|  |  • PRINCE2 (7 Principles, 7 Themes, 7 Processes)             |    |
|  |  • ITIL 4 SVS (Service Value System)                        |    |
|  |  • DevOps/DevSecOps 파이프라인                               |    |
|  +--------------------------------------------------------------+    |
|                              v 개선(Improvement)                        |
|  Layer 5: 성과 & 위험 (Performance & Risk) ------------------------  |
|  +--------------------------------------------------------------+    |
|  |  • CMMI-DEV v2.0 (5 Maturity Levels)                        |    |
|  |  • KPI 대시보드 (CSF, KGI, KPI 3계층)                       |    |
|  |  • ISO 27005/31000 위험 관리                                |    |
|  |  • Value Office (ValueOps, FinOps)                          |    |
|  +--------------------------------------------------------------+    |
|                                                                        |
|  -------------------------------------------------------------------  |
|  [법적 기반] 전자정부법, 개인정보보호법, 정보통신망법, 클라우드법,    |
|             AI기본법, 디지털플랫폼정부법                                |
|  -------------------------------------------------------------------  |
+------------------------------------------------------------------------+
```

**과거 vs 현대 IT 경영 패러다임 비교:**

| 구분 | 전통적 IT 관리 (1990~2010) | 현대 IT 경영 (2015~현재) |
|:---|:---|:---|
| **관점** | IT = 비용(Cost Center) | IT = 가치 창출(Profit Enabler) |
| **구조** | 수직적(Silo), 중앙집중형 | 수평적(DevOps), 분산형 (Federation) |
| **거버넌스** | 컴플라이언스 중심 (SOX, Basel) | 가치·위험 균형 (COSO ERM + COBIT) |
| **인프라** | On-premise, CapEx | 하이브리드/멀티클라우드, OpEx |
| **방법론** | 폭포수(Waterfall) | 애자일(Agile), SAFe, Lean |
| **성과 측정** | 시스템 가용성(Uptime) | 비즈니스 가치(EBITDA, NRR, NPS) |
| **아키텍처** | 모놀리식 | 마이크로서비스, API-first, 이벤트 드리븐 |
| **보안** | 경계 기반(Perimeter) | 제로트러스트(Zero Trust, NIST SP 800-207) |

- **📢 섹션 요약 비유**: IT 경영 관리는 **오케스트라 지휘자**와 같습니다. 바이올린(전략), 첼로(거버넌스), 트럼펫(아키텍처), 팀파니(프로젝트), 그리고 지휘봉(성과 관리) 모두가 각자의 악보를 연주하되, **하나의 협주곡(비즈니스 가치)**으로 조화롭게 울려야 합니다. 지휘자가 없으면 각 악기는 제멋대로 소리를 내어 **소음(Noise)**이 되고, 잘 조율된 오케스트라는 **교향곡(Symphony)**이 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 동작 메커니즘은 **"Plan -> Govern -> Build -> Run -> Measure"** 의 5단계 연속 사이클(Continuous Cycle)로 구현됩니다. 이 사이클은 **ISO/IEC 38500 IT 거버넌스 모델**과 **COBIT 2019의 Governance System**이 결합된 형태로, 각 단계가 명확한 **입력(Input) -> 프로세스(Process) -> 산출물(Output) -> 피드백(Feedback)** 구조를 가집니다.

```text
+----------------------------------------------------------------------+
|         IT 경영 관리 5단계 운영 사이클 (Plan-Govern-Build-Run-Measure) |
+----------------------------------------------------------------------+

  +------------+
  |  PLAN      | <- BS/ISP/IT전략서 (Ward & Peppard IS/IT Portfolio)
  |  전략 수립 |    입력: 비즈니스 전략서, 시장 분석, 규제 변화
  +-----+------+    출력: IT 거버넌스 체계, IT 거버넌스 선언문
        |              도구: BSC, Porters Five Forces, PESTEL
        v
  +------------+
  |  GOVERN    | <- COBIT 2019 + ISO 38500
  |  거버넌스  |    EDM (Evaluate, Direct, Monitor) 5단계
  +-----+------+    입력: 비즈니스 요구사항, 규제 요구사항
        |              출력: 정책/표준, RACI, Risk Appetite Statement
        v
  +------------+
  |  BUILD     | <- TOGAF ADM Phase A~F + PMBOK 7th
  |  구축/개발 |    ADM Phase: A(Vision) -> B(Business) -> C(Information
  +-----+------+    Systems) -> D(Technology) -> E(Opportunities) -> F(Migration)
        |              출력: 타겟 아키텍처, 솔루션 아키텍처, 이행계획
        v
  +------------+
  |  RUN       | <- ITIL 4 SVS + DevOps/SRE
  |  서비스운영|    7 Guiding Principles, 34 Practices
  +-----+------+    입력: SLA, OLA, UC
        |              출력: 서비스 카탈로그, 인시던트/문제/변경 관리
        v
  +------------+
  |  MEASURE   | <- CMMI v2.0 + KPI/CSF + FinOps
  |  성과측정  |    KPI 4관점: 재무/고객/내부프로세스/학습성장
  +-----+------+    출력: 성과 대시보드, 개선 과제, 차기 Plan 입력
        |              도구: APM (Dynatrace, Datadog), BI (Tableau)
        +--------------► (피드백 루프)
```

### 구성 요소별 상세 동작 메커니즘

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **전략 정렬 (Strategy Alignment)** | 비즈니스-IT 정렬 | Ward & Peppard의 **IS/IT 포트폴리오 매트릭스**(필수/지원/공헌/매칭)로 4단계 정렬도 측정. Luftman의 **SAMM 모델**(Strategic Alignment Maturity Model) 5단계(L1: Administered ~ L5: Optimized)로 6개 속성(Communications, Competency, Governance, Partnership, Technology Scope, Skills) 점수화. |
| **거버넌스 체계 (Governance System)** | 의사결정·통제 | COBIT 2019의 **40 Governance/Management Objective** 중 EDM(평가지표 4개 × 5개 도메인 = 20개 지표) + 11개 Design Factor로 거버넌스 시스템 맞춤화. **RACI 차트**(Responsible, Accountable, Consulted, Informed)로 200여 활동의 역할 매핑. |
| **아키텍처 프레임워크** | 시스템 청사진 | TOGAF 10의 **ADM(Architecture Development Method)** Phase A->F 6단계 + **Preliminary Phase** + **Phase G(Implementation Governance)** + **Phase H(Architecture Change Management)**. **ArchiMate 3.2** 표기법으로 **3 Layer(Strategy/Business/Application/Technology) × 3 Aspect(Active/Structure/Behavior)** 모델링. |
| **프로젝트 관리** | 인도 관리 | PMBOK 7th의 **8 Performance Domains**(Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty). 12가지 Project Management Principle. PRINCE2의 **7 Principles**(Continued Business Justification, Learn from Experience, Defined Roles, Manage by Stages, Manage by Exception, Focus on Products, Tailor to Project Environment). |
| **서비스 운영** | 가치 전달 | ITIL 4의 **Service Value System(SVS)** — Opportunity/Demand -> Value -> Guiding Principles(7) -> Governance -> Practices(34) -> Continual Improvement. **4P 모델**(People, Product, Partners, Processes). **34 Practices** 중 17개 General, 17개 Service Management. |
| **위험 관리** | 불확실성 통제 | ISO 31000:2018의 **6단계 프로세스**(Communication, Scope, Context, Criteria -> Risk Identification -> Analysis -> Evaluation -> Treatment -> Monitoring). 정성적 분석(**Likelihood × Impact 5×5 매트릭스**) + 정량적 분석(**VaR, CVaR, Monte Carlo 시뮬레이션 10,000회**). |
| **성과 측정** | 정량적 가치 입증 | **KGI -> CSF -> KPI** 3계층 분해. CMMI-DEV v2.0의 **5 Maturity Level**: L1(Initial) -> L2(Managed) -> L3(Defined) -> L4(Quantitatively Managed) -> L5(Optimizing). Level 4부터 **통계적 기법**(SPC, Control Chart ±3σ) 적용. |
| **법·제도 정합** | 컴플라이언스 | **전자정부법 제46조**(정보화 사업 타당성 조사 B/C/P 분석), **개인정보보호법 제23조**(민감정보 처리 제한
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 769 / 800

<- **이전**: [768. IT 경영 관리 핵심 토픽 768번 시험 요약](/studynote/12_it_management/05_security_compliance/768_it_management_core_topic_768_exam_summary/)
**다음**: [770. IT 경영 관리 핵심 토픽 770번 시험 요약](/studynote/12_it_management/05_security_compliance/770_it_management_core_topic_770_exam_summary/) ->

---
