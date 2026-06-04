+++
title = "673. IT 경영 관리 핵심 토픽 673번 시험 요약 (IT Management Core Topic 673 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스·서비스관리·정보보호·성과관리 프레임워크(COBIT 2019, ITIL 4, ISO/IEC 38500, ISO/IEC 27001, IT-BSC)를 통합하여 정보화 투자 대비 가치 실현(Value Delivery)을 보장하고, EDM(평가·지시·모니터링) 사이클로 경영진의 IT 통제 책임을 시스템화하는 것이 핵심이다.
> 2. **가치**: McKinsey·Deloitte 사례에서 COBIT 기반 거버넌스 도입 시 IT 투자 ROI 20~35% 향상, ITIL 4 적용 시 인시던트 MTTR 50% 단축, MOF 4.0 기반 운영 성숙도 4단계 도달 시 운영 비용 OPEX 15~25% 절감이 보고되며, 정보화 사업의 PMO 실패율(전통 70%)을 30% 이하로 낮추는 정량 효과를 제공한다.
> 3. **판단 포인트**: 거버넌스 체계 수립 시 **Scope(기업 전사 vs 사업부 vs 프로젝트)** , **참조 모델 선택(COBIT Cascade vs ISO 38500 6원칙)**, **자동화 도구 채택(Archer·ServiceNow GRC·SAP GRC)**, **측정 지표(Leading vs Lagging KPI 균형)**, **Change Enablement(설득 vs 통제)**의 5대 트레이드오프를 의사결정 기준으로 삼아야 한다.

---

## Ⅰ. 개요 및 필요성

정보화 사업이 단발성 SI(System Integration)에서 플랫폼·데이터·AI 기반 상시 운영 체계로 전환됨에 따라, IT 부서는 더 이상 "비용 센터"가 아닌 **"전략적 가치 실현 파트너(Value Realization Partner)"**로 재정의되어야 한다. 그러나 한국 정보화진흥원(KAIT) 및 NIA 자료에 따르면, 국내 공공·민간 정보화 사업의 약 **62%**가 계획 대비 ROI 미달, **48%**가 사용자 만족도 60점 미만으로 종료되는 것이 반복적으로 관측된다. 이러한 실패의 공통 원인은 (1) 경영진의 IT 통제 부재(Governance Vacuum), (2) 서비스 운영 성숙도 미흡(Lack of Service Maturity), (3) 정보보호 리스크 미관리(Unmanaged Cyber Risk), (4) 성과 측정 지표 부재(Measurement Blindness)의 4대 갭에서 기인한다.

이에 ITGA(Information Technology Governance Association)와 ISACA는 2019년 **COBIT 2019**를 발표하여 40개의 거버넌스·관리 목표(Governance & Management Objectives)를 5개 도메인(EDM, Align-Plan-Organize, Build-Acquire-Implement, Deliver-Service-Support, Monitor-Evaluate-Assess)으로 재구성하였고, ISO/IEC 38500:2015는 "Responsibility(책임), Strategy(전략), Acquisition(획득), Performance(성과), Conformance(준법), Human Behavior(인간행동)"의 6대 원칙으로 이사회급 IT 통제 표준을 제시한다. 동시에 ITIL 4의 **34개 Practice**와 **Service Value System(SVS)**는 운영 측의 핵심 토대가 되었으며, ISO/IEC 27001:2022의 Annex A 93개 통제항목은 정보보호 측면을 보완한다.

```text
[정보화 사업 거버넌스 통합 참조 모델]

  ┌──────────────── 이사회 (Board of Directors) ─────────────────┐
  │   책임(Responsibility) · 전략(Strategy) · 성과(Performance)   │
  │   ※ ISO/IEC 38500 6원칙 준수 의무화                            │
  └────────────────────────┬─────────────────────────────────────┘
                           │ EDM (Evaluate·Direct·Monitor)
                           ▼
  ┌─────────── 거버넌스 체계 (COBIT 2019, 40 Objectives) ──────────┐
  │  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐           │
  │  │APO(15)  │ │BAI(11)  │ │DSS(6)    │ │MEA(4)      │           │
  │  │Align-   │ │Build-   │ │Deliver-  │ │Monitor-    │           │
  │  │Plan-    │ │Acquire- │ │Service-  │ │Evaluate-   │           │
  │  │Organize │ │Implement│ │Support   │ │Assess      │           │
  │  └────┬────┘ └────┬────┘ └─────┬────┘ └─────┬──────┘           │
  └───────┼───────────┼────────────┼────────────┼──────────────────┘
          │           │            │            │
          ▼           ▼            ▼            ▼
  ┌──────────────┐ ┌─────────────┐ ┌────────────────┐ ┌─────────────┐
  │IT전략·아키텍처│ │프로젝트 거버│ │ITIL 4 SVS     │ │MEA 감사·평가│
  │처(EA, BPM)   │ │버넌스(PMO) │ │34 Practices    │ │(내부통제)  │
  │BSC·KPI 설계  │ │위험관리(RM) │ │Service Desk   │ │ISMS 인증   │
  └──────────────┘ └─────────────┘ └────────────────┘ └─────────────┘
          │                    │              │                │
          └────────────────────┴──────────────┴────────────────┘
                                  │
                                  ▼
        ┌───────────────── 정보보호 거버넌스 (ISO 27001) ───────────┐
        │ Annex A 93 Controls: A.5 조직(37) A.6 인사(8) A.7 물리(14)│
        │ A.8 기술(34)  ·  Statement of Applicability (SoA)        │
        │ ISMS-PIMS-A.27019-A.27799-A.27005-A.27032 통합           │
        └──────────────────────────────────────────────────────────┘
```

기존 패러다임(2000년대 COBIT 4.1·ITIL v3)은 **프로세스 중심(Process-Centric)**이었으나, 2019년 이후 패러다임은 **가치 흐름 중심(Value-Stream-Centric)**으로 전환되었다. 이는 Agile·DevOps·Cloud Native 환경에서 프로세스 경계가 사라지고, 서비스 가치 사슬(Value Chain)을 따라 측정·개선해야 하기 때문이다. 따라서 기술사 답안에서는 "단순 도입이 아닌 **Cascade(상위 목표→하위 목표 전파)**와 **Focus Area(중요 영역 우선 적용)**" 전략을 강조해야 한다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **대형 크루즈선의 '선장(이사회)·항해사(거버넌스)·기관장(운영)·보안요원(정보보호)·검색대(성과측정)'**가 모두 같은 해도(Navigation Chart)를 보며 협력하는 것과 같다. 어느 한 직책이라도 빠지면 배는 방향을 잃거나 암초에 부딪힌다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 통합 아키텍처는 **4계층 참조 모델(Governance-Management-Service-Technology)**로 구성되며, 각 계층은 COBIT 2019의 5개 도메인, ITIL 4의 4 Dimensions, ISO 27001의 Plan-Do-Check-Act 사이클과 1:1 또는 1:N 매핑된다.

### 1. COBIT 2019 핵심 메커니즘

COBIT 2019는 **40개 거버넌스·관리 목표**를 **Governance Objectives(EDM 5개: EDM01~05)**와 **Management Objectives(35개: APO12, BAI11, DSS06, MEA04 등)**로 분리한다. 각 목표는 **Process Purpose Statement, Goals Cascade(연계 목표), Practice(실무), Inputs/Outputs, Related Guidance** 5요소로 구성된다. **Goals Cascade** 메커니즘은 "Stakeholder Needs → Enterprise Goals(13개) → Alignment Goals(13개) → Management Goals(40개)"의 4단 전파 구조로, BCM과 같은 시나리오에서 **Enterprise Goal 04(Compliance) → Alignment Goal 06(Compliance with external laws) → Management Goal MEA03(Compliance with external requirements)**처럼 도출된다.

**Design Factor** 시스템은 11개(EA, Compliance, Risk, Threats, Role of IT, Sourcing, Methods, Technology, Organization, Implementation, Size)를 통해 **거버넌스 시스템의 범위와 우선순위**를 자동 조정한다. 예를 들어 금융권의 경우 Compliance·Risk·Regulation 가중치가 5배로 부각되어 관련 통제 항목이 강화된다.

### 2. ITIL 4 Service Value System (SVS)

ITIL 4의 SVS는 **Opportunity/Demand → Value → Guiding Principles(7개) → Governance → Practices(34) → Continual Improvement**의 가치 흐름으로 구성된다. 핵심 7원칙은 **Focus on Value, Start Where You Are, Progress Iteratively with Feedback, Collaborate and Promote Visibility, Think and Work Holistically, Keep It Simple and Practical, Optimize and Automate**이다. 34개 Practice는 일반관리(General, 14개), 서비스관리(Service, 17개), 기술관리(Technical, 3개)로 구분되며, **Incident Management, Problem Management, Change Enablement, Service Level Management, Continual Improvement**가 기술사 출제 빈도가 가장 높다.

### 3. ISO/IEC 38500 6대 원칙 + 38500-2 거버넌스 모델

ISO/IEC 38500의 6원칙은 **Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior**이며, 적용 모델 **Evaluate→Direct→Monitor(EDM)** 사이클은 이사회가 IT 의사결정의 3단계를 수행하도록 강제한다. 38500-2의 Part 2는 Part 1의 원칙을 실제 거버넌스 활동에 적용하는 가이드로, "As-Is 분석 → To-Be 설계 → 적용 → 모니터링"의 4단계를 따른다.

### 4. IT 성과관리 (IT-BSC + KPI)

**IT-BSC(Balanced Scorecard for IT)**는 Kaplan & Norton의 4관점(Financial, Customer, Internal Process, Learning & Growth)을 IT에 적용한 모델로, **11개 KPI 클러스터**(예: Financial → IT Cost Ratio, Customer → End-User Satisfaction, Process → Incident Resolution Rate, L&G → IT Staff Skill Index)를 운영한다. **KPI 설정 시 SMART 원칙** + **Leading Indicator(선행지표, 예: 직원 교육 이수율)**와 **Lagging Indicator(후행지표, 예: 시스템 가용성 SLA 달성률)**의 균형이 필수이다.

```text
[IT 거버넌스 4계층 운영 흐름도 - EDM 사이클 + ITIL SVS 통합]

  ┌─── (1) Evaluate 평가 ──────────────────────────────────────┐
  │  · 이사회/IT전략위원회: 외부환경 분석, Compliance 점검        │
  │  · Inputs: 거버넌스 보고서, Risk Register, Audit Findings    │
  │  · Outputs: 신규 전략과제, KPI 갱신, 투자 우선순위 도출        │
  └─────────────────────────┬─────────────────────────────────┘
                            ▼
  ┌─── (2) Direct 지시/결정 ───────────────────────────────────┐
  │  · 경영진 승인: IT 투자 포트폴리오, 정책·표준 제정             │
  │  · 도구: IT Steering Committee, Architecture Review Board  │
  │  · 결정 유형: Go/No-Go, 우선순위, 예산배분, 조직개편         │
  └─────────────────────────┬─────────────────────────────────┘
                            ▼
  ┌─── (3) Monitor 모니터링/감시 ──────────────────────────────┐
  │  · KPI Dashboard, SLA 성능, ISMS 인증 심사                  │
  │  · 측정: IT-BSC(4관점), Service Quality(CSAT/NPS)           │
  │  · 피드백: (1) Evaluate로 회귀 (Plan-Do-Check-Act 동일)      │
  └─────────────────────────────────────────────────────────────┘

  ※ 좌측: COBIT 2019 EDM 도메인 / 우측: ITIL 4 Continual Improvement
  ※ 모든 단계에서 ISO 27001 PDCA 사이클이 횡단(cross-cutting)으로 동작
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (40 Objectives)** | 거버넌스·관리 목표 프레임워크 | EDM·APO·BAI·DSS·MEA 5도메인, 11 Design Factor 기반 자동화된 거버넌스 시스템 설계, Goals Cascade로 기업 목표→정렬 목표→관리 목표 4단 전파, Risk/Capability 기반 우선순위 산정 |
| **ITIL 4 SVS (34 Practices)** | IT 서비스 운영 및 가치 창출 | Service Value Chain(Plan→Engage→Design&Transition→Obtain/Build→Deliver&Support) 활동, 7 Guiding Principles, Continual Improvement 모델(Définition→Establishment→Operation), 4 Dimensions(Organizations·People·Information·Technology·Partners·Suppliers·Value Streams·Processes) |
| **ISO/IEC 38500 + 27001** | IT 통제 표준 + 정보보호 관리 | 38500 6원칙(Responsibility·Strategy·Acquisition·Performance·Conformance·Human Behavior) + 27001 PDCA(Clause 4~10) + Annex A 93 통제(2022년 4개 그룹 14개 카테고리), SoA(Statement of Applicatement) 기반 적용범위 선언, ISO 27005 기반 리스크 평가 |
| **IT-BSC + KPI 체계** | 성과 측정 및 보고 | 4관점(Financial·Customer·Internal Process·Learning&Growth) BSC, 11개 KPI 클러스터(예: ROI·TCO·CSAT·MTTR·가용성·변경성공률·직원역량지수), Leading vs Lagging 지표 6:4 비율, Balanced Scorecard Studio·PowerBI·Tableau 시각화 |
| **GRC 자동화 플랫폼** | 통합 거
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 673 / 800

← **이전**: [672. IT 경영 관리 핵심 토픽 672번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/672_it_management_core_topic_672_exam_summary/)
**다음**: [674. IT 경영 관리 핵심 토픽 674번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/674_it_management_core_topic_674_exam_summary/) →

---
