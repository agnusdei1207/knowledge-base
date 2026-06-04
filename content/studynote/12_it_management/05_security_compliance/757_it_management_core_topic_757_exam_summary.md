---
title: "757. IT 경영 관리 핵심 토픽 757번 시험 요약 (IT Management Core Topic 757 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 757번은 **IT 거버넌스-전략-운영-컴플라이언스**를 통합하는 4축 프레임워크로, COBIT 2019, ISO/IEC 38500, ITIL 4, BAI(Balanced Architecture for IT) 등 국제 표준 기반의 정렬(Alignment)·가치 창출(Value Delivery)·리스크 통제(Risk Management) 체계를 다루는 종합 영역임.
> 2. **가치**: Well-governed IT는 기업 EBITDA 대비 **IT 예산의 ROI를 15~25% 향상**시키고, IT 프로젝트 실패율을 **70%에서 30% 이하로 절감**하며, 디지털 전환(DX) 프로젝트의 **Time-to-Value를 평균 40% 단축**시킴.
> 3. **판단 포인트**: ① 중앙집중형(Centralized) vs 분산형(Federated) 거버넌스 모델, ② COBIT의 40개 Governance/Management Objectives 중 우선순위 선정(Design Factor 11개 활용), ③ Agile/DevOps 환경에서의 기존 ITIL/COBIT 재해석(VeriSM, ITIL 4 Service Value System) 여부가 핵심 의사결정 분기점.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 비용 센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 진화하면서, IT에 대한 의사결정·통제·평가를 통합 관리할 수 있는 체계의 필요성이 대두되었습니다. 과거(1990~2000년대)에는 IT 관리가 개별 시스템 단위의 프로젝트 관리(PMBOK, PRINCE2) 차원에 머물렀으나, 클라우드·AI·데이터 경제로의 전환기에서는 **전사적 IT 가치사슬(Enterprise IT Value Chain)** 관리가 필수입니다.

특히 COVID-19 이후 **가속화된 디지털 전환(COVID-driven DX)**, 생성형 AI(GenAI)의 등장, EU AI Act·한국 AI 기본법 등 **규제 환경의 복잡화**, 그리고 **ESG 및 사이버보안 공시(예: SEC Cybersecurity Disclosure Rule, 2023)** 의무화로 인해, IT 경영 관리의 범위는 **"기술 통제"에서 "비즈니스 거버넌스"**로 확장되었습니다. 757번 시험은 이러한 환경 변화 속에서 **IT 투자 의사결정, 거버넌스 구조 설계, 성과 측정, 리스크 관리, 컴플라이언스**를 통합적으로 다룹니다.

```text
+--------------------------------------------------------------------+
|        757번 IT 경영 관리 - 4대 축(Axis) 통합 프레임워크          |
+--------------------------------------------------------------------+
              +---------------------------------+
              |   ① 전략축(Strategy Axis)       |
              |  - IT 전략맵(Strategy Map)      |
              |  - 투자 포트폴리오(Portfolio)   |
              |  - 디지털 전환 로드맵           |
              +------------+--------------------+
                           |
        +------------------+------------------+
        v                  v                  v
+--------------+   +--------------+   +--------------+
|② 거버넌스축 |   |③ 운영축      |   |④ 컴플라이언스|
|Governance    |   |Operations    |   |Compliance    |
+--------------+   +--------------+   +--------------+
|COBIT 2019    |   |ITIL 4 SVS    |   |ISO 38500     |
|ISO 38500     |   |DevOps/CI-CD  |   |GDPR/AI Act   |
|RACI Matrix   |   |SRE/SLI/SLO   |   |ISMS-P/K-ISMS |
|3-Lines Model |   |FinOps        |   |SOX/내부회계  |
+--------------+   +--------------+   +--------------+
        |                  |                  |
        +------------------+------------------+
                           v
        +----------------------------------+
        |  KPI 대시보드: BSC 4관점 + ESG  |
        |  - 재무/고객/내부프로세스/학습   |
        |  + ESG(환경/사회/지배구조)       |
        +----------------------------------+
```

기존의 **사일로(Silo)형 IT 관리**(각 부서별 독립 운영, 1990s)와 비교하여, 757번이 다루는 현대 IT 경영 관리는 **플랫폼화(Platformization)**, **프로덕트화(Productization)**, **데브옵스-옵저버빌리티(Observability)**, **데이터 드리븐 의사결정**을 특징으로 합니다. 이는 Gartner의 **"Run the Business" -> "Grow the Business" -> "Transform the Business"** 3단계 모델과도 일치합니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 종합 도시계획"**과 같습니다. 개별 건물(시스템)이 잘 지어져도(프로젝트 성공), 상하수도·교통·치안·재정(거버넌스·운영·컴플라이언스) 인프라가 없으면 도시는 무너집니다. 757번은 이 도시 인프라를 어떻게 설계·유지·발전시킬 것인가를 다룹니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 거버넌스 시스템 (Governance System)

COBIT 2019는 **40개의 Governance/Management Objective**를 5개 도메인(EDM: Evaluate-Direct-Monitor / Align-Plan-Organize / Build-Acquire-Implement / Deliver-Service-Support / Monitor-Evaluate-Assess)으로 구성하며, **11개 Design Factor**(전략, 목표, 리스크, 문제, 위협, 준수요건, 역할, IT 이슈, 기술 방향, 산업, 기업규모)에 따라 우선순위를 결정합니다.

```text
+-------------------------------------------------------------------+
|        COBIT 2019 Governance & Management Objectives 계층        |
+-------------------------------------------------------------------+
+-----------------------------------------------------------------+
|  EDM(05) - 거버넌스 위원회 레이어                                |
|  EDM01: 거버넌스 프레임워크 설정 및 유지                          |
|  EDM02: 혜택 실현(Benefits Realization) 확보                     |
|  EDM03: 리스크 최적화(Risk Optimization) 최적화                  |
|  EDM04: 자원 최적화(Resource Optimization) 최적화                |
|  EDM05: 이해관계자 투명성(Stakeholder Transparency) 확보         |
+-----------------------------------------------------------------+
         | 계층적 연동 (Cascading Objectives)
         v
+-----------------------------------------------------------------+
|  Align-Plan-Organize(APO, 14개)                                  |
|  APO01~APO14: IT 관리 정책, 전략, 조직, 품질, 혁신 등            |
+-----------------------------------------------------------------+
         |
         v
+-----------------------------------------------------------------+
|  Build-Acquire-Implement(BAI, 11개)                              |
|  BAI01~BAI11: 솔루션 선정, 구축, 이행, 변경, 수용도 관리         |
+-----------------------------------------------------------------+
         |
         v
+-----------------------------------------------------------------+
|  Deliver-Service-Support(DSS, 06개)                              |
|  DSS01~DSS06: 서비스 운영, 인시던트, 보안, 연속성, 모니터링      |
+-----------------------------------------------------------------+
         |
         v
+-----------------------------------------------------------------+
|  Monitor-Evaluate-Assess(MEA, 04개)                              |
|  MEA01~MEA04: 성능, 통제 내부통제, 외부감사, 컴플라이언스        |
+-----------------------------------------------------------------+
         |
         v
+-----------------------------------------------------------------+
|  Focus Area (예시): DevOps, Cybersecurity, Digital Transformation|
|  -> 40개 Goal에 우선순위 매핑                                     |
+-----------------------------------------------------------------+
```

### 2. 핵심 구성요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이해관계자 니즈 & 목표 카스케이딩** | 비즈니스 목표 -> IT 목표 -> Enabler 목표로 3단계 변환 | **Goals Cascade**: BSC 4관점(재무/고객/내부프로세스/학습) × IT Balanced Scorecard, **카노 모델(Kano Model)**로 Must-be/One-dimensional/Attractive 니즈 분류 |
| **거버넌스 & 관리 목적(40 Goals)** | 5개 도메인 40개 목표를 RACI Matrix로 책임 할당 | **RACI**: Responsible(실행)/Accountable(책임)/Consulted(자문)/Informed(통보). 3개 수준 목표: ① Process Activity -> ② Process Goal -> ③ Enterprise Goal |
| **Enabler(7종)** | 각 목표 달성을 위한 7가지 촉진 수단 | ① Principles/Policies/Frameworks ② Processes ③ Organizational Structures ④ Information ⑤ People/Skills/Competencies ⑥ Services/Infrastructure/Applications ⑦ Technology |
| **디자인 팩터(11개)** | 거버넌스 시스템의 우선순위·구성 결정 | Strategy, Goals, Risk Profile, I&T Related Issues, Threat Landscape, Compliance Requirements, Role of IT, Sourcing Model, IT Implementation Methods, Technology Adoption, Enterprise Size |
| **성과 측정 체계** | KPI/KRI/CPI 3종 측정지표로 가치 추적 | **LAG 지표**(결과: ROI, NPS, MTTR)와 **LEAD 지표**(선행: 코드 배포 빈도, 변경 실패율). NIST CSF의 5함수(Identify-Protect-Detect-Respond-Recover)와 연동 |
| **리스크 관리 프레임워크** | IT 리스크 식별·평가·대응·모니터링 | ISO 27005 + COBIT EDM03. **리스크 매트릭스(5×5)**: 발생가능성 × 영향도. **4T 대응**: Treat/Tolerate/Terminate/Transfer |
| **IT 가치 측정 및 FinOps** | 클라우드/IT 투자에서 비즈니스 가치 환산 | **TBM(Tech Business Management)** Taxonomy: Tower-Cost-Unit 3계층. **Unit Economics**: Feature당 비용, 사용자당 비용. **FinOps 3 Phases**: Inform/Optimize/Operate |

### 3. 핵심 알고리즘 및 수식

**IT 투자 ROI 계산 (TCO-TVA 모델)**
```
NPV = Σ [t=1->n] (Benefit_t - Cost_t) / (1+r)^t
    Benefit_t = 직접편익(DT) + 간접편익(IT) × 확률가중치
    Cost_t     = CapEx(연동) + OpEx + Risk-adjusted cost
    r          = WACC(가중평균자본비용) 또는 Hurdle Rate(8~12%)
```

**서비스 가용성(Availability) 측정**
```
Availability(%) = (MTBF / (MTBF + MTTR)) × 100
   Tier 1: 99.671% (연 28.8h 장애 허용)
   Tier 2: 99.749% (연 22h)
   Tier 3: 99.982% (연 1.6h)
   Tier 4: 99.995% (연 26.3분)
```

**CSF(Critical Success Factor) - KPI 매핑 예시**
- CSF: "고객 만족도 향상" -> KPI: NPS, CSAT, First Contact Resolution
- CSF: "운영 효율성" -> KPI: MTTR, Deployment Frequency, Change Failure Rate
- CSF: "규제 준수" -> KPI: 컴플라이언스 위반 건수, 감사 지적사항 수

- **📢 섹션 요약 비유**: COBIT의 40개 목표는 마치 **"병원 진료 체계"**와 같습니다. ① EDM은 이사회(최고 의사결정), ② APO는 진료 기획실, ③ BAI는 시술/수술, ④ DSS는 일상 진료·응급실, ⑤ MEA는 의료 감시·평가실입니다. 11개 디자인 팩터는 각 병원의 특성(대학병원/요양병원/한의원)에 따라 진료 우선순위를 다르게 적용하는 것과 같습니다.

---

## Ⅲ. 비교 및 연결

| 구분 | COBIT 2019 (거버넌스) | ITIL 4 (서비스 운영) | ISO/IEC 38500 (이사회 거버넌스) |
| :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스 & 관리 통합 프레임워크 | IT 서비스 관리(ITSM) 모범사례 | IT 관련 이사회 의사결정 원칙 |
| **대상 계층** | CISO/CIO/PMO/감사 전계층 | 서비스 매니저/운영팀/엔지니어 | 이사회·최고경영진 |
| **핵심 모델** | 40 Goals + 7 Enablers + 11 Design Factors | Service Value System(SVS) + 4P + 34 Practices | 6 Principles(E.D.R.R.E.D: Evaluate/Direct/Monitor) |
| **지표 체계** | Process Goal + Enterprise Goal 카스케이딩 | Value Stream + Value Outcome | Maturity Model(R-Responsible, A-Accountable 등) |
| **Agile/DevOps 대응** | COBIT 2019 + Focus Area: DevOps | ITIL 4 SVS는 Agile/Lean/DevOps 네이티브 통합 | 원칙 기반 -> 비교적 유연 |
| **인증/감사** | ISACA 자격증(CISA/CISM/CGEIT) 연계 | PeopleCert/Axelos ITIL Foundation->Master | ISO 인증 가능 |
| **장점** | 거버넌스-관리-운영-평가 End-to-End | 서비스 가치 사슬(Value Stream) 시각화 | 이사회 수준 원칙 단순·명료 |
| **한계** | 구현 복잡도 높음, 도입 기간 12~24개월 | 거버넌스 측면 약함, 운영 편향 | 추상적 원칙, 실행도구 부족 |
| **서로의 관계** | ITIL을 BAI/DSS 도메인에 통합 | COBIT의 운영 측면을 보완 | COBIT의 상위 메타 거버넌스 |

### 다른 시스템과의 통합

1. **PMBOK 7 / PRINCE2**: 프로젝트 관리 - COBIT의 BAI 도메인(BAI01~BAI11)과 연동. 프로젝트 거버넌스 = Portfolio -> Program -> Project 3계층
2. **TOGAF / ArchiMate**: EA(Enterprise Architecture) - COBIT의 APO02(전략), APO03(아키텍처 관리)와 직결. **ADM(Architecture Development Method)**: Preliminary A -> Vision -> Business -> Information Systems -> Technology -> Opportunities -> Migration -> Implementation Governance -> Change Management
3. **ISO 27001/27002**: 정보보안 - COBIT의 DSS05(보안 운영)와 매핑. Annex A 통제 항목 93개 -> COBIT Goals에 N:1 매핑
4. **Agile/Scrum/Kanban**: DevOps 환경 - VeriSM(2018) 프레임워크가 COBIT/ITIL/Agile 통합
5. **SaaS 거버넌스(SIG, SaaS GRC)**: 클라우드 도입 확대에 따른 별도 거버넌스 체계

- **📢 섹션 요약 비유**: COBIT은 **"헌법"**, ITIL은 **"민사소송법"**, ISO 38500은 **"대통령 훈령"**과 같습니다. 헌법
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 757 / 800

<- **이전**: [756. IT 경영 관리 핵심 토픽 756번 시험 요약](/studynote/12_it_management/05_security_compliance/756_it_management_core_topic_756_exam_summary/)
**다음**: [758. IT 경영 관리 핵심 토픽 758번 시험 요약](/studynote/12_it_management/05_security_compliance/758_it_management_core_topic_758_exam_summary/) ->

---
