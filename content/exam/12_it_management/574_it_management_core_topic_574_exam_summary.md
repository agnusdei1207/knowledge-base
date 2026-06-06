---
title: "IT Management Core Topic 574 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 574. IT 경영 관리 핵심 토픽 574번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **전략 정렬(Strategy Alignment) -> 거버넌스(Governance) -> 포트폴리오 관리(Portfolio) -> 서비스 운영(Service) -> 가치 측정(Value Measurement)**으로 이어지는 5단계 Value Governance Chain을 통해, IT를 비용 중심의 지원 기능에서 **사업 가치를 창출하는 전략 자산(Strategic Asset)**으로 전환시키는 경영 체계이다.
> 2. **가치**: COBIT 2019 + ITIL 4 + ISO/IEC 38500 기반의 통합 거버넌스 체계 적용 시, IT 투자 대비 ROI 평균 25~40% 개선, IT 프로젝트 실패율 30%->10% 감소, EBITDA 대비 IT 비용 비율 4~6% 적정 수준 유지, Time-to-Market 50% 단축의 정량 효과를 창출한다.
> 3. **판단 포인트**: **"Build vs Buy vs Cloud vs As-a-Service"**의 4-Way sourcing 결정, **"Centralized vs Federated vs Hybrid"**의 거버넌스 모드 선택, **"Waterfall vs Agile vs Bimodal vs Dual"**의 운영 모드 채택이 핵심 트레이드오프이며, 산업별(금융·제조·공공) 규제 환경과 디지털 성숙도(Digital Maturity Index)에 따라 최적 해가 달라진다.

---

## Ⅰ. 개요 및 필요성

정보기술이 더 이상 업무 자동화(Back-office Automation) 수준을 넘어 **사업 모델 그 자체(Product, Channel, Revenue Source)**를 재정의하는 시대에, IT 부서는 CIO(Chief Information Officer), CDO(Chief Digital Officer), CTO(Chief Technology Officer) 체제 하에서 **이해관계자(Stakeholder) 전체의 기대치를 조율**하는 핵심 경영 기능으로 격상되었다. 그러나 통계적으로 글로벌 기업의 70% 이상이 **디지털 전환(Digital Transformation) 목표를 달성하지 못하고** 있으며, 그 원인 중 53%가 "IT-Business 전략 불일치"로 보고되고 있다(McKinsey, 2023).

기존의 **"Demand-Supply" 기반 수동적 IT 운영 모델**은 한계를 보인다. 사업部门要求(Requirements)를 받아 IT 부서가 시스템으로 구현하는 방식은, 시장 변화 속도(VUCA 환경) 대비 **Lead Time이 길고(평균 18~36개월), 변경 비용이 기하급수적으로 증가(Conway's Law 및 Brooks' Law 적용)**한다. 따라서 **"Strategy-to-Execution"**을 단일 사슬로 연결하고, **"Plan-Build-Run-Innovate"**의 4단계 가치를 End-to-End로 측정·관리할 수 있는 통합 IT 경영 프레임워크가 필수적이다.

```text
        [ 전통 IT 운영 모델 vs 현대 IT 경영 모델 ]

  <- 전통 (Demand-Supply 수동 모델) ->     <- 현대 (Value-Driven 통합 모델) ->

   사업부   -> 요구사항      -> IT 부서      사업전략 -+
   사업부   -> 요구사항      -> IT 부서     거버넌스  -+--> Value Stream
   사업부   -> 요구사항      -> IT 부서     포트폴리오 -+
   사업부   -> 요구사항      -> IT 부서     서비스   -+
   (Silo)     (백로그)      (실패 多)     혁신    -+
       |           |             |               |
       v           v             v               v
   평균 24개월 Lead Time      ROI 측정 불가       Real-time KPI 대시보드
   실패율 30~40% (CHAOS Report)   Shadow IT 만연      자동화된 가치 추적
```

기존 패러다임 대비 현대 IT 경영 모델은 **"Silofunction -> Cross-Functional Squad"**, **"Capex 일회성 -> Opex 가변 비용"**, **"Technology Push -> Business Pull + Data-Driven"**으로 전환되며, 이를 뒷받침하는 핵심 프레임워크로 **COBIT 2019(거버넌스), ITIL 4(서비스), TOGAF 10(아키텍처), PMBOK 7(프로젝트), SAFe 6.0(애자일 스케일)**이 상호 보완적으로 작동한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"자동차 회사의 통합 차량 관리 시스템(Vehicle Management System)"**과 같다. 과거에는 엔진(개발), 차체(인프라), 내비게이션(서비스)가 각자 따로 움직이는 **"연결되지 않은 부속품"**이었다면, 현대는 CAN 버스로 모든 ECU가 연결되어 **연비·안전·편의·배출가스**를 실시간 통합 관리하는 것과 같다. COBIT가 OBD-II 진단 프로토콜이라면, ITIL은 정비 매뉴얼, ISO 38500는 도로교통법(거버넌스 법규)에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 5대 핵심 계층은 **Strategy -> Governance -> Portfolio -> Service -> Value**의 수직적 흐름과 **Plan -> Build -> Run -> Innovate**의 수평적 운영 사이클이 만나는 매트릭스 구조로 설계된다.

```text
  [ IT 경영 관리 5계층 Value Chain 아키텍처 ]

  +-------------------------------------------------------------+
  |  Layer 1: STRATEGY (전략 정렬)                              |
  |  +--------------+  +--------------+  +--------------+        |
  |  | Business     |<-->| IT Strategy  |<-->| Digital      |        |
  |  | Strategy     |  | (3-Year      |  | Roadmap      |        |
  |  | (Vision/Mission)| Roadmap)    |  | (DT Strategy)|        |
  |  +------+-------+  +------+-------+  +------+-------+        |
  |         +-----------------+-----------------+                |
  |  Layer 2: GOVERNANCE (거버넌스)         v                    |
  |  +--------------------------------------------------+        |
  |  |  ISO 38500 Principles  |  COBIT 2019 EDM/Align  |        |
  |  |  (Responsibility, Strategy, Acquisition,        |        |
  |  |   Performance, Compliance, Human Behavior)      |        |
  |  +------------------------+-------------------------+        |
  |  Layer 3: PORTFOLIO (투자배분)          v                    |
  |  +--------------+  +--------------+  +--------------+        |
  |  | Run the      |  | Grow the     |  | Transform    |        |
  |  | Business     |  | the Business |  | the Business |        |
  |  | (60~70% 예산)|  | (20~30% 예산)|  | (5~15% 예산) |        |
  |  +------+-------+  +------+-------+  +------+-------+        |
  |  Layer 4: SERVICE (서비스)               v                    |
  |  +--------------------------------------------------+        |
  |  |  ITIL 4 SVS (Service Value System)               |        |
  |  |  Plan->Engage->Design&Transition->Obtain/Build      |        |
  |  |  ->Deliver&Support->Improve                       |        |
  |  +------------------------+-------------------------+        |
  |  Layer 5: VALUE (가치 측정)              v                    |
  |  +--------------+  +--------------+  +--------------+        |
  |  | Financial    |  | Customer     |  | Internal     |        |
  |  | (NPV, ROI,   |  | (NPS, CSAT,  |  | (Agility,    |        |
  |  |  TCO, EVA)   |  |  Churn Rate) |  |  Quality)    |        |
  |  +--------------+  +--------------+  +--------------+        |
  +-------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Strategy Alignment** | 사업·IT·디지털 전략의 정렬 | Ward & Peppard(2002)의 4-Stage Model(Information Mapping -> IT Impact Analysis -> Competitive Positioning -> Strategic IS Plan) 적용, MIT CISR의 IT-Business Alignment Maturity 5단계(Ad-hoc->Committed->Established·Managed·Optimized) 측정 |
| **Governance Body** | 의사결정·감독·조정의 3역할 분리 | 이사회(IT Steering Committee) -> 집행(CIO/CDO) -> 운영(PMO/EA Center)의 3-Line Defense 모델, RACI 매트릭스(Responsible, Accountable, Consulted, Informed) 적용 |
| **Portfolio Mgmt.** | IT 투자 우선순위 결정 및 포트폴리오 균형 | McKinsey 3-Horizon(70:20:10), BCG Growth-Share Matrix를 IT에 적용한 **"Run/Grow/Transform"** 예산 배분, NPV·IRR·Payback Period·Strategic Fit Score의 다기준 의사결정(MCDA) |
| **Service Operation** | 안정적 서비스 제공 및 지속적 개선 | ITIL 4의 34개 Practice, SLA 99.9%(Three Nine) ~ 99.99%(Four Nine) 등급별 가용성, Incident->Problem->Known Error->Change->Release의 라이프사이클, Mean Time To Restore(MTTR) < 1시간 목표 |
| **Value Measurement** | 정량·정성 가치 측정 및 환류 | **"Benefits Realization Plan(BRP)"**로 KPI 사전 정의, Balanced Scorecard(BSC) 4관점(Financial·Customer·Internal·Learning&Growth), Earned Value Management(EVM) - SPI, CPI 지표 활용 |

### 핵심 알고리즘 및 의사결정 공식

- **Total Economic Impact(TEI) = TCO + Benefits + Risk + Flexibility**
- **NPV(순현재가치) = Σ(현금흐름ₜ / (1+r)ᵗ) - 초기투자**, IT 프로젝트는 통상 **할인율 8~12%, NPV > 0**일 때 승인
- **IT-Alignment Index = ½ × (Strategy Alignment + Operational Alignment)** (Henderson & Venkatraman의 Strategic Alignment Model)
- **Mature IT Function Score = Σ(Process Maturity Level × Weight) / Σ Weight**, COBIT PAM(Process Assessment Model) 기반 0~5 척도
- **Real Options Valuation(ROV)**으로 디지털 전환 프로젝트의 전략적 유연성 가치 반영: `V = NPV + Σ(Call Option Value)`

- **📢 섹션 요약 비유**: 5계층 구조는 **"건축물의 하중 전달 시스템"**과 같다. **지붕(Strategy) -> 기둥(Governance) -> 슬래브(Portfolio) -> 벽체(Service) -> 기초(Value)**까지 하중이 끊기지 않고 전달되어야 하며, 어느 한 층에서 하중이 소실(예: 전략만 좋고 거버넌스 부재)되면 전체 건축물이 균열(프로젝트 실패·ROI 미달)이 발생한다. COBIT의 EDM( Evaluate-Direct-Monitor)이 바로 **"구조계 엔지니어링 코드"** 역할이다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리에서 혼동하기 쉬운 5가지 핵심 프레임워크/개념을 비교한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **PMBOK 7** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 | IT 서비스 관리 | IT 의사결정 거버넌스 원칙 | 프로젝트 관리 | 엔터프라이즈 아키텍처 |
| **대상** | CIO·이사회·감사인 | IT 서비스 운영자 | 이사회·경영진 | PM·프로젝트 팀 | EA 아키텍트·전략기획 |
| **범위** | 5개 도메인(40 Governance/Management Objectives) | 34개 Practice(서비스 가치 사슬) | 6개 원칙(거버넌스 원칙) | 12개 원칙 + 5개 Performance Domain | 4개 Phase(ADM) + 7 Part |
| **핵심 산출물** | Capability/Maturity Model(0~5), Goals Cascade | Service Value System(SVS), 4-Dimension Model | Governance Framework, Director's Principles Charter | Project Charter, Risk Register, Issue Log | ADM Cycle, Architecture Repository |
| **측정 관점** | 프로세스 성숙도 + 목표 달성 | 가치 공학(Value Stream), 가치 흐름 | 원칙 준수 여부, 책임 할당 | Triple Constraint(Scope·Time·Cost) + Quality | Architecture Maturity Model |
| **적합 조직** | 대기업·금융·공공(규제 강함) | 서비스 중심 조직(SI·MSP·내부 IT) | 상장사·공공기관·대기업 | 프로젝트 중심 조직 | EA 도입 중·대기업 |
| **인증/감사** | ISACA 인증(CGEIT, CISA) | PeopleCert/Axelos(Foundation->Master) | 인증 없음(원칙 제시) | PMI(PMP, PfMP) | The Open Group(TOGAF Certified) |
| **연계성** | ↔ ITIL(Service 연계), ↔ NIST CSF(보안 연계) | ↔ DevOps(SRE 연계), ↔ SIAM(멀티벤더) | ↔ COBIT(거버넌스-관리 분리) | ↔ SAFe, ↔ PRINCE2 | ↔ ArchiMate, ↔ Zachman |

### 프레임워크 통합 아키텍처(Integrated Framework)

실무에서는 단일 프레임워크 적용이 아닌 **"Layered Integration"**이 일반적이다. 예컨대 금융권의 경우:

```text
  [ 금융권 IT 경영 프레임워크 통합 예시 ]

  최상위: ISO 38500 (6 Principles)        <- 이사회 의사결정 원칙
       v
  상위: COBIT 2019 (40 Goals Cascade)     <- 거버넌스/관리 체계
       v
  중위: NIST CSF + ISO 27001              <- 사이버 보안 통제
       v
  운영: ITIL 4 (Service Value System)     <- 서비스 운영
       v
  실행: PMBOK 7 + SAFe 6.0 + DevOps      <- 프로젝트·운영 실행
       v
  설계: TOGAF 10 (ADM Cycle)              <- 아키텍처 설계
```

-
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 574 / 800

<- **이전**: [573. IT 경영 관리 핵심 토픽 573번 시험 요약](/studynote/12_it_management/05_security_compliance/573_it_management_core_topic_573_exam_summary/)
**다음**: [575. IT 경영 관리 핵심 토픽 575번 시험 요약](/studynote/12_it_management/05_security_compliance/575_it_management_core_topic_575_exam_summary/) ->

---
