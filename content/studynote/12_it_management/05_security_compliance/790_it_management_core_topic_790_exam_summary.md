---
title: "790. IT 경영 관리 핵심 토픽 790번 시험 요약 (IT Management Core Topic 790 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Management 790번)는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 체인, PMBOK 7th 프로젝트 도메인, TOGAF ADM 아키텍처 개발 방법론을 통합하여 비즈니스-IT 정렬(Business-IT Alignment)을 달성하고, IT 투자 ROI를 측정·최적화하는 종합 경영 프레임워크
> 2. **가치**: 체계적 거버넌스 도입 시 IT 프로젝트 성공률 35%->75%(Standish Group 2023), ISMS-P 인증 취득 후 보안사고 62% 감소, EA 기반 중복투자 제거로 TCO 20-30% 절감, SLA 99.95% 달성 시 연간 다운타임 4.38시간 이내 통제
> 3. **판단 포인트**: 거버넌스(Control) ↔ 서비스 혁신(Agility) 간 균형, Waterfall-Scrum 하이브리드 적용 시 단계별 게이트(Gate) 기준 명확화, SaaS/IaaS/PaaS 클라우드 도입 시 CapEx->OpEx 전환에 따른 총비용 분석(TCO 3년/5년) 필수, SaaS 종속성(Vendor Lock-in) 회피 위한 멀티클라우드·API 게이트웨이 전략 병행

---

## Ⅰ. 개요 및 필요성

정보관리기술사 790번 토픽은 단순한 IT 운영을 넘어 **IT를 경영 자산으로 관리**하기 위한 거버넌스·서비스·프로젝트·아키텍처·인프라 영역을 통합한 메타 프레임워크입니다. 4차 산업혁명(AI, 클라우드, IoT, 빅데이터) 시대에 기업 IT는 비용 센터(Cost Center)에서 가치 창출 센터(Value Center)로 전환되었고, 이에 따라 **이해관계자(Stakeholder)**인 CEO·CFO·CIO·사업부서·고객·규제기관을 만족시킬 수 있는 정량적·정성적 관리 체계 수립이 요구됩니다.

과거(1990~2000년대)에는 ITIL v2 기반의 프로세스 중심 IT 운영, PMBOK 4th Waterfall 중심, COBIT 4.x 통제 중심의 분리된 접근이 주를 이뤘습니다. 하지만 2010년대 후반부터는 **Agile/DevOps/Cloud Native** 환경이 보편화되면서 ITIL 4의 Service Value System(SVS), PMBOK 7th의 8 Performance Domains, COBIT 2019의 40 Governance/Management Objectives처럼 **유연하면서도 통제 가능한(Governed Agility)** 프레임워크로 진화했습니다.

```text
+------------------------------------------------------------------------+
|                IT 경영 관리 4대 축(4 Pillars) 통합 참조 모델            |
+------------------------------------------------------------------------+
|                                                                        |
|   +-------------------+         +-------------------+                  |
|   |  IT 거버넌스       |◄-------►|  IT 서비스 관리    |                  |
|   |  (Governance)     |         |  (ITSM/ITIL 4)    |                  |
|   |  • COBIT 2019     |         |  • Service Value   |                  |
|   |  • ISO/IEC 38500  |         |    Chain (SVC)     |                  |
|   |  • ISO/IEC 27001  |         |  • 34 Practices    |                  |
|   |  • ISMS-P (한국)   |         |  • CSI/TPI         |                  |
|   +---------+---------+         +---------+---------+                  |
|             |  Align                    |  Deliver                    |
|             v                            v                            |
|   +-------------------+         +-------------------+                  |
|   |  프로젝트/프로그램 |◄-------►|  엔터프라이즈      |                  |
|   |  관리(PPM)         |         |  아키텍처(EA)      |                  |
|   |  • PMBOK 7th      |         |  • TOGAF 10 ADM    |                  |
|   |  • PRINCE2 7th    |         |  • Zachman 6x6     |                  |
|   |  • SAFe/Scrum     |         |  • FEAF            |                  |
|   |  • MSP/P3O        |         |  • ARIS/DoDAF      |                  |
|   +-------------------+         +-------------------+                  |
|             |                            |                            |
|             +------------+---------------+                            |
|                          v                                            |
|              +------------------------------+                          |
|              |  비즈니스 가치 실현(Benefits  |                          |
|              |  Realization) — KPI/SLA/ROI   |                          |
|              |  • Balanced Scorecard(BSC)    |                          |
|              |  • OKR(Key Results)           |                          |
|              |  • EVA(Economic Value Added)  |                          |
|              +------------------------------+                          |
+------------------------------------------------------------------------+
```

기존에는 IT 부서가 시스템 장애 복구(MTBF, MTTR)와 예산 집행률만 관리했다면, 현재의 IT 경영 관리는 **비즈니스 Outcome**(매출 증가 5%, 고객 이탈률 10% 감소, 신제품 출시周期 30% 단축 등)에 IT가 직접 기여했음을 입증해야 하는 책임을 갖습니다. 2024년 Gartner 조사에 따르면 글로벌 2000대 기업의 78%가 CIO에게 비즈니스 KPI 연동 KPI Tree를 요구하고 있으며, 이는 **IT-Business Alignment Maturity**가 Level 3 이상이어야 달성 가능합니다(Luftman 모델 기준).

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 종합 행정 시스템**과 같습니다. 개별 도로·상하수도·전력(개별 IT 시스템)만 관리하는 게 아니라, 도시 계획(EA), 재정(Budget), 법률(Governance), 민원 서비스(SLA)를 통합 운영하는 **'디지털 시청'**을 구축하는 일입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 4대 축은 각각 **국제 표준/프레임워크**를 기반으로 계층적·반복적으로 상호작용합니다. 핵심 동작 원리는 COBIT 2019의 **Governance System**과 ITIL 4의 **Service Value Chain(SVC)**을 기준으로 다음과 같이 분해됩니다.

### A. COBIT 2019 거버넌스 시스템 (40 Objectives)

```text
+----------------------------------------------------------------------+
|                 COBIT 2019 Governance & Management System            |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------------------------------------------------+             |
|   |  EDM: Evaluate, Direct, Monitor (거버넌스 5개)       |             |
|   |  EDM01 프레임워크 / EDM02 Benefit Delivery          |             |
|   |  EDM03 Risk Optimization / EDM04 Resource Mgmt      |             |
|   |  EDM05 Stakeholder Transparency                      |             |
|   +---------------------+------------------------------+             |
|                         |                                            |
|   +---------------------v------------------------------+             |
|   |  Align, Plan, Organize(APO) — 14개                  |             |
|   |  APO01~APO14: 전략, 포트폴리오, 예산, 인적자원, 위험 |             |
|   +---------------------+------------------------------+             |
|                         |                                            |
|   +---------------------v------------------------------+             |
|   |  Build, Acquire, Implement(BAI) — 11개              |             |
|   |  BAI01~BAI11: 솔루션 선정·구축·변경·전환·이행        |             |
|   +---------------------+------------------------------+             |
|                         |                                            |
|   +---------------------v------------------------------+             |
|   |  Deliver, Service, Support(DSS) — 6개               |             |
|   |  DSS01~DSS06: 운영, 서비스요청, 장애, 보안, 지속성  |             |
|   +---------------------+------------------------------+             |
|                         |                                            |
|   +---------------------v------------------------------+             |
|   |  Monitor, Evaluate, Assess(MEA) — 4개               |             |
|   |  MEA01~MEA04: 성과, 내부통제, 외부감사, 컴플라이언스  |             |
|   +----------------------------------------------------+             |
|                                                                      |
|   ★ Design Factors(10개)로 조직별 40 Objectives 우선순위 자동 도출   |
|   ★ Focus Area: 사이버보안, DevOps, 디지털윤리, ESG 등 17개          |
+----------------------------------------------------------------------+
```

### B. ITIL 4 Service Value Chain (SVC)

```text
   Plan --► Engage --► Design & Transition --► Obtain/Build
      |                                              |
      |         (Service Value Chain)                 |
      |                                              v
   Improve ◄----- Deliver & Support ◄----- (Value to Customer)

   ● 6개 핵심 활동: Plan, Engage, Design & Transition,
     Obtain/Build, Deliver & Support, Improve
   ● 34개 Practices: Incident Mgmt(7단계), Problem(8단계),
     Change Enablement(3-tier CAB: Normal/Standard/Emergency)
   ● 4 Dimensions: 조직·인재, 정보·기술, 파트너·공급사,
     가치흐름·프로세스
```

### C. PMBOK 7th Performance Domains

PMBOK 7th(2021)는 5th/6th의 10 Knowledge Areas를 8 Performance Domains로 재구성하고, **Principles(12) -> Domains(8) -> Models/Methods/Artifacts** 구조로 전환했습니다.

```text
+--------------------------------------------------------+
|  PMBOK 7th 8 Performance Domains                       |
|  --------------------------------------------------    |
|  1. Stakeholder        5. Planning                     |
|  2. Team                6. Uncertainty                  |
|  3. Development         7. Delivery (측정/예측)         |
|  4. Work (스코프/일정)  8. Measurement                  |
+--------------------------------------------------------+
```

### D. TOGAF 10 Architecture Development Method(ADM)

```text
   Preliminary Phase (Architecture Capability 정의)
        |
        v
   A: Architecture Vision --► B: Business Architecture
        |                          |
        v                          v
   C: Information Systems --► D: Technology Architecture
        |   Architecture              |
        |                             |
        v                             v
   E: Opportunities & Solutions --► F: Migration Planning
                                        |
                                        v
   G: Implementation Governance --► H: Architecture Change Mgmt
                                        |
                                        v
                        Requirements Management(전 단계 공통)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스 목표·통제 체계 | 40 Governance/Management Objectives, 7 Component(Process/Structure/People/Skills/Information/Service/Infrastructure), 10 Design Factor 기반 조직 맞춤 우선순위 도출, 17 Focus Area(사이버보안, DevOps, ESG 등) |
| **ITIL 4** | 서비스 운영·개선·가치 창조 | Service Value System(SVS), 34개 Practice(Incident·Problem·Change·Service Desk·CSI), 4 Dimension Model, Shift-Left·Right 접근(AIOps, ChatOps, Observability) |
| **PMBOK 7th** | 프로젝트/프로그램 성과 관리 | 12 Principles(Steward, Team, Plan, Uncertainty 등), 8 Performance Domains, Tailoring 기법, Agile/Adaptive/Hybrid 모두 수용, Value Delivery System(VDS) |
| **TOGAF 10** | 엔터프라이즈 아키텍처 표준화 | ADM 8 Phase(Phase A~H), Architecture Repository(Capability/Strategic/Project/ADM), 53 Building Block(ABB->SBB), Content Metamodel |
| **ISO 27001/ISMS-P** | 정보보호 관리체계 | 93 Control(A.5~A.8), Plan-Do-Check-Act(PDCA) 4단계, Statement of Applicability(SoA), 연 1회 이상 내부감사·경영검토 |
| **Balanced Scorecard** | 전략 KPI 4관점 측정 | Financial / Customer / Internal Process / Learning & Growth, Strategy Map(인과관계), 90일 Action Plan |
| **SLA/SLM** | 서비스 수준 계약/관리 | SLI(지표)->SLO(목표)->SLA(계약), 9s 가용성(99.9%=연 8.7h, 99.95%=4.38h, 99.99%=52m 다운타임 허용), Error Budget 기반 운영 |

#### 핵심 산식 및 KPI

1. **ROI (투자대비성과)** = (순이익 − 투자비용) / 투자비용 × 100. IT 프로젝트의 경우 3년 NPV(Net Present Value) ≥ 0, IRR ≥ Hurdle Rate(통상 8~12%)가 합격 기준.
2. **TCO (총소유비용)** = 직접비(서버/라이선스) + 간접비(전력 IDC, 인건비, 교육, 폐기). 클라우드 전환 시 3~5년 TCO 비교 필수(CapEx+OpEx 통합 분석).
3. **MTBF / MTTR** = MTBF(평균장애간격)^, MTTR(평균복구시간)v. AIOps·Observability 도입으로 MTTR 50%v 사례 다수.
4. **CSAT/NPS** = 고객만족도/순추천지수. 헬프데스크 CSAT ≥ 90%, NPS ≥ 30이 우수 기준.
5. **Change Success Rate** = (성공 변경 수 / 전체 변경 수) × 100. CAB 3-Tier(Normal/Standard/Emergency) 적용 시 95%^ 달성 가능.
6. **COBIT Goal Cascade** = Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Goals(40개)으로 연쇄 매핑.

- **📢 섹션 요약 비유**: COBIT은 **"헌법"**(어떤 원칙으로 통치할 것인가), ITIL은 **"민원 처리 매뉴얼"**(어떻게 서비스할 것인가), PMBOK은 **"건설 현장 관리 규정"**(프로젝트를 어떻게 완성할 것인가), TOGAF는 **"도시总体规划"**(전체 구조를 어떻게 설계할 것인가)에 비유할 수 있습니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역은 유사한 이름·기능을 가진 프레임워크가 많아 혼동이 잦습니다. 기술사 시험에서 빈번히 출제되는 **핵심 비교**는 다음과 같습니다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 27001/ISMS-P** |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스(무엇을, 왜) | 서비스 운영·가치(어떻게) | 프로젝트 성공(언제, 누가) | 정보보호 통제(리스크) |
| **구조/원리** | 40 Objectives, 7 Components, 10 Design Factors | SVS, 34 Practices, 4 Dimensions | 12 Principles, 8 Domains, VDS | 93 Control(Annex A), PDCA |
| **주 사용자** | 이사회·CIO·감
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 790 / 800

<- **이전**: [789. IT 경영 관리 핵심 토픽 789번 시험 요약](/studynote/12_it_management/05_security_compliance/789_it_management_core_topic_789_exam_summary/)
**다음**: [791. IT 경영 관리 핵심 토픽 791번 시험 요약](/studynote/12_it_management/05_security_compliance/791_it_management_core_topic_791_exam_summary/) ->

---
