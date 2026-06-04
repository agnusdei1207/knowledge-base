+++
title = "599. IT 경영 관리 핵심 토픽 599번 시험 요약 (IT Management Core Topic 599 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019(거버넌스·관리 목표 40개), ITIL 4(서비스 가치 시스템), ISO 38500(6개 원칙)** 등 글로벌 프레임워크를 기반으로, **전략(Strategy) -> 아키텍처(Architecture) -> 투자(Investment) -> 운영(Operation) -> 평가(Evaluation)** 의 5단계 가치사슬을 통합·조정하는 경영체계이다.
> 2. **가치**: 정량적으로는 **NPV/IRR 기반 정보화 투자 수익률 15~25% 개선**, 정성적으로는 **IT-Business 정렬도(Strategic Alignment Maturity) Level 3~4 도달, 의사결정 리드타임 40% 단축, ISO 27001/20000/22301 인증을 통한 글로벌 신뢰도 확보**가 가능하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **① 프레임워크 중복 적용(COBIT+ITIL+ISO 20000 이중통제) vs 통합 거버넌스, ② 중앙집중 통제(CoE) vs 분산형 거버넌스(Federated), ③ ROI 단기 편중 vs Real Options·BSC 균형평가, ④ Build vs Buy vs Cloud, ⑤ 보안 편의성 vs Zero Trust** 의 5축 의사결정이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사(기술사) 시험에서 **IT 경영관리**는 단순한 IT 운영 관리를 넘어, **CIO 직속 조직의 의사결정 체계**, **디지털 전환(DX) 시대의 핵심 거버넌스 메커니즘**, **법·규제 대응과 글로벌 경쟁력 확보**를 아우르는 **통합관리체계(Integrated Management System, IMS)** 를 평가한다. 4차 산업혁명(AI·클라우드·빅데이터·IoT) 환경에서 IT는 **"비용 센터(Cost Center)"에서 "전략적 가치 창출 파트너(Value Driver)"** 로 역할이 전환되었으며, 이에 따라 **IT 성과에 대한 경영진의 가시성·책임성·측정 가능성** 요구가 폭증하고 있다.

특히 2020년 이후 **코로나19(COVID-19) 가속화**, **금융권 DORA(2025.1 시행)**, **EU AI Act(2024.8 발효)**, **개인정보보호법 개정(2023.9)**, **클라우드 보안인증制度(CSAP)** 등 규제 환경이 급변하면서, IT 경영관리의 **컴플라이언스·리스크·보안 거버넌스 통합** 필요성이 더욱 부각되고 있다.

```text
[ IT 경영관리 5단계 가치사슬 통합 프레임워크 ]

                +--------------------------------------+
                |  Board / CEO / CxO (최고 의사결정기구) |
                +------------------+-------------------+
                                   | (정기 보고·승인)
                                   v
   +-------------------------------------------------------------+
   |  ① 전략 (Strategy)  - ISP, EA, 디지털전환 로드맵, McFarlan |
   |     v                                                       |
   |  ② 아키텍처 (Architecture) - TOGAF ADM, Zachman, FEAF        |
   |     v                                                       |
   |  ③ 투자 (Investment) - NPV/IRR/TCO, Real Options, 포트폴리오|
   |     v                                                       |
   |  ④ 운영 (Operation) - ITIL 4 SVS, SLA, DevOps, SRE          |
   |     v                                                       |
   |  ⑤ 평가 (Evaluation) - BSC, KPI, 감사, COBIT 2019 EDM      |
   +-------------------------------------------------------------+
                                   |
                                   v
            +------------------------------------------+
            |  횡단 통제 (Cross-cutting Controls)        |
            |  • 거버넌스: COBIT 2019 / ISO 38500        |
            |  • 보안:   ISO 27001 / ISMS-P / Zero Trust|
            |  • 연속성: ISO 22301 (BCMS)                |
            |  • 서비스: ISO 20000 / ITIL 4              |
            |  • 리스크: ISO 31000 (ERM 통합)            |
            +------------------------------------------+
```

**Old vs New Paradigm 비교**:
- **기존(1990~2010)**: IT는 **Cost Center**, **단위시스템별 개별 관리(Silo)**, **CAPEX 중심**, **수동 통제**, **연 1회 정기감사**
- **신규(2020~현재)**: IT는 **Value Driver + Risk Center**, **EA 기반 통합 거버넌스**, **OPEX·Cloud 네이티브**, **실시간 GRC(Governance·Risk·Compliance)**, **연중 상시 모니터링(Continuous Audit)**, **AI 거버넌스·ESG 연계**

- **📢 섹션 요약 비유**: IT 경영관리는 **"배의 키잡이(Rudder)"** 와 같다. 키잡이는 엔진(기술)·선원(인력)·화물(데이터)을 직접 모는 것이 아니라, **항해 방향(전략)** 을 정하고, **풍향·해류(리스크)** 를 읽어 **타이밍 있게 키를 꺾어** 배가 목적지(경영 목표)에 도달하도록 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 국제표준(ISO), 글로벌 프레임워크(COBIT, ITIL, PMBOK, TOGAF), 그리고 산업별 모범사례(ISO 27001, PCI-DSS, HIPAA, DORA)를 **레이어드 구조**로 통합한 것이다. 기술사 시험에서는 각 프레임워크의 **목적·범위·핵심 구성요소·상호 연계 매핑**을 정확히 이해해야 한다.

```text
[ IT 경영관리 프레임워크 레이어드 아키텍처 ]

  Layer 1 (최상위)  |  ISO 38500 IT Governance 6 Principles
                    |  (Responsibility, Strategy, Acquisition,
                    |   Performance, Conformance, Human Behavior)
  ------------------+-----------------------------------------
  Layer 2 (거버넌스)|  COBIT 2019 Governance & Management Obj.(40)
                    |  +-- EDM 5개 (Governance)
                    |  +-- APO 14개 (Align, Plan, Organize)
                    |  +-- BAI 11개 (Build, Acquire, Implement)
                    |  +-- DSS 6개  (Deliver, Service, Support)
                    |  +-- MEA 4개  (Monitor, Evaluate, Assess)
  ------------------+-----------------------------------------
  Layer 3 (서비스)  |  ITIL 4 Service Value System (SVS)
                    |  Opportunity/Demand -> Value -> Guiding Principles
                    |  -> Governance -> Practices -> Continual Improvement
  ------------------+-----------------------------------------
  Layer 4 (프로세스)|  PMBOK 7 (8 Performance Domains, 12 Principles)
                    |  + PRINCE2 (7 Themes/Processes) + CMMI 2.0
  ------------------+-----------------------------------------
  Layer 5 (보안·연속)|  ISO 27001 (Annex A 93 통제) + ISMS-P
                    |  ISO 22301 (BCMS: BIA, RTO/RPO, 전략)
                    |  ISO 31000 (Risk: 식별->분석->평가->대응->모니터링)
  ------------------+-----------------------------------------
  Layer 6 (아키텍처)|  TOGAF ADM (8 Phases: A->H: Preliminary->Req->Vision
                    |  ->Business->InfoSystem->Tech->Opportunity->
                    |   Migration->Implmt Govern->Change Mgmt)
                    |  + Zachman 6×6 매트릭스 + FEAF
  ------------------+-----------------------------------------
  Layer 7 (기반)    |  데이터 거버넌스(DAMA-DMBOK 2) + AI 거버넌스
                    |  + ESG + 클라우드 거버넌스 + DevSecOps
                    +------------------------------------------
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019 (거버넌스 체계)** | IT 활동과 비즈니스 목표의 연계, 통제 목표 정의 | **40개 Governance/Management Objective**, **Goals Cascade**(Stakeholder Needs->Enterprise Goals->Alignment Goals->Component Goals), **Design Factors 11개**(전략, 위험, 컴플라이언스 등)로 거버넌스 시스템 맞춤 설계, **Focus Area**(예: 사이버보안, DevOps, AI) 단위 우선순위 조정 |
| **ITIL 4 (서비스 가치 시스템)** | IT 서비스의 End-to-End 가치 흐름 관리 | **Service Value System (SVS)**: Opportunity/Demand->Value, **7 Guiding Principles**(Focus on Value, Start Where You Are, Progress Iteratively, Collaborate, Think Holistically, Keep It Simple, Optimize), **34 Practices**(Change Enablement, Incident Mgmt, Service Desk, SLM 등), **4-Dimension Model**(Org&People, Information&Tech, Partners&Suppliers, Value Streams&Processes) |
| **ISO 38500 (거버넌스 표준)** | 이사회·경영진의 IT 의사결정 원칙 제시 | **6 Principles**: Responsibility(책무), Strategy(전략), Acquisition(획득), Performance(성과), Conformance(준수), Human Behavior(인적행태). **모델(EDM)**: Evaluate(평가)->Direct(지시)->Monitor(모니터링) 사이클 |
| **PMBOK 7 (프로젝트 관리)** | 프로젝트·프로그램·포트폴리오 통합 관리 | **12 Principles of Project Mgmt**(Stewardship, Team, Planning, Uncertainty, Complexity, …), **8 Performance Domains**(Stakeholder, Team, Planning, Delivery, Measurement, Uncertainty, Lifecycle, Practice), **Project Delivery: Predictive / Adaptive(Hybrid)** |
| **BSC (Balanced Scorecard)** | 전략 -> 4관점 KPI -> 실행의 전략맵 | **4 Perspective**: Financial(재무) ↗ / Customer(고객) ↗ / Internal Process(내부프로세스) ↗ / Learning & Growth(학습성장) ↗. **Strategy Map**(인과관계 연결: 학습성장->내부->고객->재무), **OKR**과 연계 운영 |
| **TOGAF ADM (아키텍처 개발 방법론)** | EA(Enterprise Architecture) 수립·운영 | **8 Phase Cycle**: Preliminary(기반)->A(비전)->B(비즈니스)->C(정보시스템)->D(기술)->E(기회/솔루션)->F(전환계획)->G(거버넌스)->H(변경관리). **Architecture Repository**(ARB, ABB, AS-IS/TO-BE), **ADM Cycle 반복(Iteration)** |
| **EA(Enterprise Architecture) 거버넌스 위원회** | 아키텍처 의사결정·표준 승인·예산 배분 | **ARB(Architecture Review Board)**, **EA 표준(Standard)·예외(Exception) 관리**, **Capability Map**(Level 1~4) 기반 투자 포트폴리오 우선순위화, **RFP 평가 시 아키텍처 적합성 체크** |
| **TCO/ROI/NPV 분석 엔진** | IT 투자 의사결정의 정량적 근거 | **TCO = 직접비(HW/SW/Lic/인건비) + 간접비(교육/전환/다운타임) + 위험비용(보안사고/SLA위반)**, **NPV = Σ(CFₜ/(1+r)ᵗ) - 투자액**, **IRR**, **Payback Period**, **Real Options(B/S Option)** 로 유연성 가치화 |

**핵심 공식 및 의사결정 기준**:
1. **정보화 투자 ROI 산출**: ROI(%) = (총 편익 − 총 비용) / 총 비용 × 100 -> 통상 **15% 이상** 이면 적정, **20% 이상** 이면 우수. 단, **정성 편익(신속성·이미지·컴플라이언스)** 은 별도 가중치 부여
2. **NPV 순현재가치**: NPV = Σ[(Bₜ − Cₜ) / (1+r)ᵗ] − I₀. **할인율 r = WACC(가중평균자본비용) + IT 위험 프리미엄 2~3%p** 적용
3. **McFarlan 전략 그리드 4분면**: **Strategic(전략적) / Turnaround(전환) / Factory(공장) / Support(지원)** — 각 분면별 거버넌스·투자·운영 전략 차별화
4. **Henderson-Venkatraman 4분면(SAM: Strategic Alignment Model)**: IT 영향(Operation/Innovative) × Business 전략(Operational/Strategic) -> **Strategy Execution ↔ Technology Potential** 매트릭스
5. **BSC 인과관계 전략맵**: 학습·성장(HR/문화) -> 내부프로세스
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 599 / 800

<- **이전**: [598. IT 경영 관리 핵심 토픽 598번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/598_it_management_core_topic_598_exam_summary/)
**다음**: [600. IT 경영 관리 핵심 토픽 600번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/600_it_management_core_topic_600_exam_summary/) ->

---
