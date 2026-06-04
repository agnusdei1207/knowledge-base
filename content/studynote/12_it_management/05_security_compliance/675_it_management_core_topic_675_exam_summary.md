---
title: "675. IT 경영 관리 핵심 토픽 675번 시험 요약 (IT Management Core Topic 675 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019**(Controls, Objectives & Indicators 40개), **ITIL 4**(Service Value System의 7가지 가이드), **TOGAF ADM**(Architecture Development Method 8단계), **ISO 38500**(6개 원칙) 등 글로벌 거버넌스 프레임워크를 기반으로 **비즈니스 전략 ↔ IT 전략 ↔ 아키텍처 ↔ 운영 ↔ 컴플라이언스**를 폐루프(Closed-loop)로 정렬하여 기업 디지털 자산의 가치를 극대화하는 통합 관리 체계이다.
> 2. **가치**: Gartner 2024 보고 기준 **EA(Enterprise Architecture) 기반 중복 시스템 통합 시 TCO 18~32% 절감**, ITIL 4 도입 조직의 **MTTR(Mean Time To Restore) 평균 47% 단축**, ISO 27001 인증 기업의 **정보유출 사고 비용 평균 $4.1M -> $1.5M 감소**(IBM 2023), IT-Portfolio 우선순위 재정렬로 **저성과 프로젝트 비율 60% -> 18%로 개선**이 가능하다.
> 3. **판단 포인트**: **중앙집중 거버넌스(Governance) vs 페더레이션 자율성(Agility)**, **Strict Change Advisory Board(CAB) vs Continuous Delivery 자동 승인**, **CapEx(On-premise) vs OpEx(Cloud FinOps)** 사이의 균형, 그리고 **Waterfall EA(단계형) vs Agile SAFE(Scaled Agile Framework) 혼용 모드** 선택이 기술사 답안의 핵심 Trade-off이며, 조직의 **Digital Maturity Index(DMI)** 수준에 따라 다른 거버넌스 강도를 적용해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술이 더 이상 업무지원(Back-office) 수단이 아닌 **비즈니스 자체의 운영 기반**이 된 4차 산업혁명 시대, 기업의 IT 자원은 연평균 매출의 **3.2~7.5%**(Gartner IT Spending 2024)를 점유하는 2~3위의 핵심 비용/자산 항목이 되었다. 그러나 IDC 조사에 따르면 **전통적 IT 예산의 70% 이상이 운영·유지보수에 매몰**되어 혁신 투자로 전환되지 못하는 '**Run-the-Business(RTB)** 딜레마'가 발생하고 있으며, 이로 인해 **Shadow IT**(무단 도입 클라우드)의 증가, 중복 시스템(Legacy Spaghetti) 복잡성, 그리고 IT-비즈니스 간 **전략적 부조화(Strategic Misalignment)** 문제가 심화되고 있다.

이에 **ISO/IEC 38500(2008->2015 개정)**은 이사회(Board) 수준의 **"Evaluate-Direct-Monitor"** 거버넌스 사이클을, **COBIT 2019**는 40개의 관리목표(Management Objective)와 5개 도메인(EDM/APO/BAI/DSS/MEA)을 통해 **거버넌스-관리(Governance & Management)** 2계층 구조를 정의한다. 즉, IT 경영 관리는 단순한 "IT 부서 관리"가 아닌, **이사회 의사결정 -> 거버넌스 목표 -> 관리 프로세스 -> 운영 활동**으로 이어지는 **Value Governance Chain**이라 할 수 있다.

```text
[기업 거버넌스 체계 - 3-Layer Strategic Alignment Model]
+----------------------------------------------------------------------+
|                       Board of Directors (이사회)                      |
|         "IT는 더 이상 비용이 아닌 전략적 자산이다" — John Zachman        |
+----------------------+-----------------------------------------------+
                       |  ISO/IEC 38500: Evaluate-Direct-Monitor
                       v
+----------------------------------------------------------------------+
|  Layer 1. Corporate Governance (기업 거버넌스)                          |
|  +- Stakeholder Value Maximization (주주·고객·사회)                      |
|  +- Risk Appetite Statement (위험선호도 선언)                            |
|  +- ESG / Digital Ethics 책임                                         |
+----------------------+-----------------------------------------------+
                       |
                       v
+----------------------------------------------------------------------+
|  Layer 2. IT Governance (IT 거버넌스) <- 기술사 출제 빈도 최다            |
|  +-------------+--------------+--------------+--------------+         |
|  |  COBIT 2019 |   ITIL 4     |   TOGAF 10   |  ISO 27001   |         |
|  |  (5 Domain, |  (SVS, 34    |  (ADM 8단게, |  (Annex A    |         |
|  |  40 Obj.)   |   Practices) |   4 Domain)  |   93 Contr.) |         |
|  +------+------+------+-------+------+-------+------+-------+         |
|         |             |              |              |                 |
|         +-------------+------+-------+--------------+                 |
+------------------------------+---------------------------------------+
                               |
                               v
+----------------------------------------------------------------------+
|  Layer 3. IT Management (IT 관리·운영)                                 |
|  +- Project/Program/Portfolio Management (PMO)                        |
|  +- IT Service Management (Incident, Problem, Change, Request Fulfill) |
|  +- Infrastructure & Operations (I&O) / SRE / AIOps                  |
|  +- Application Lifecycle Management (ALM) / DevSecOps                 |
+----------------------------------------------------------------------+
                               |
                               v
                [Business Value Realization]
                  ROI · NPV · TCO · NPS · EBITDA
```

기존 2000년대 **"Build-and-Run"** 패러다임은 IT 부서가 프로젝트를 완료하면 그대로 운영을 떠안는 수직적 사일로(Silo) 구조였으나, 현재의 **"Product-Centric / Platform Engineering"** 패러다임은 **GitOps**, **Internal Developer Platform(IDP)**, **Cloud Center of Excellence(CCoE)**를 통해 **Cross-functional Squad** 단위로 가치를 지속 제공한다. 이 구조적 전환을 **"Two-speed IT"** 또는 **"Bi-modal IT"**(Gartner 2014)라 부르며, Mode 1(안정·예측가능)과 Mode 2(민첩·실험적)의 **동시 운영**이 기술사 시험에서 빈번히 등장하는 핵심 개념이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같다. 바이올린·트럼펫·타악기(=각 IT 시스템·부서)라는 다양한 악기는 저마다 개성이 강하지만, 지휘자(=거버넌스)가 없으면 불협화음만 나고, 악보(=전략·정책)가 없으면 방향성이 사라지며, 객석(=이해관계자)에게는 카타르시스가 아닌 소음만 전달된다. COBIT는 **악보**, ITIL은 **연주 매너**, TOGAF는 **홀 구조(아키텍처)**, ISO 27001은 **무대 안전 매뉴얼**에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"원리는 표준(Framework)으로, 실행은 프로세스로, 평가는 지표(KPI/OKR)로, 개선은 측정(Metrics)을 통해"** 라는 4단계 가치 실현 사이클에 있다. 아래는 COBIT 2019의 **Governance & Management Objectives** 구조와 ITIL 4의 **Service Value System(SVS)** 을 통합한 참조 아키텍처다.

```text
[COBIT 2019 5 Domains × ITIL 4 SVS — 통합 거버넌스 아키텍처]
                    +---------------------------------+
                    |  COBIT 2019 Governance System    |
                    |  +----------+  +--------------+ |
                    |  |  EDM     |  |  Stakeholder | |
                    |  | (5 Obj.) |<-->|   Needs      | |
                    |  +----+-----+  +------+-------+ |
                    +-------+----------------+---------+
                            |                |
   +------------------------+----------------+------------------+
   |                        |                |                  |
   v                        v                v                  v
+----------+         +----------+     +----------+       +----------+
|  APO     |         |  BAI     |     |  DSS     |       |  MEA     |
|Align,    |<--------->|Build,    |----->|Deliver,  |------->|Monitor,  |
|Plan,     | 전략-계획|Acquire,  | 구현 |Service   | 운영  |Evaluate, |
|Organize  |         |Implement |     |Support   |       |Assess    |
|(14 Obj.) |         |(11 Obj.) |     |(6 Obj.)  |       |(4 Obj.)  |
+----------+         +----------+     +----------+       +----------+
      |                    |                |                  |
      +--------------------+----------------+------------------+
                                  |
                                  v
        +--------------------------------------------------+
        |        ITIL 4 Service Value System (SVS)          |
        |  +----------+    +----------+    +----------+    |
        |  |  Demand  |---->|  Value   |---->|  Service |    |
        |  |  /Oppor. |    |  (Co-    |    |  Provider|    |
        |  +----+-----+    | Creation)|    |  /Consumer|  |
        |       |          +----+-----+    +----------+    |
        |       v               |                           |
        |  +----------+    +----v-----+                     |
        |  |  ITIL    |    |  7 Guiding|                    |
        |  | Practices|    | Principles|                    |
        |  |  (34)    |    |  (Focus,  |                    |
        |  | 4 Dim.   |    |   Start   |                    |
        |  | Org/People|   |  where    |                    |
        |  | Info/Tech |    |  you are) |                    |
        |  | Partner/  |    +----------+                     |
        |  | ValueStrm |                                       |
        |  +----------+    +----------------+                |
        |                  | Continual      |                |
        |                  | Improvement    |<----------+     |
        |                  | (CSI Register)  |          |     |
        |                  +----------------+          |     |
        +--------------------------------------------------+
                                  |
                                  v
        +--------------------------------------------------+
        |   4 Dimensions of Service Management             |
        |   Organizations & People | Information & Tech     |
        |   Partners & Suppliers | Value Streams & Process  |
        +--------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 EDM (Evaluate, Direct, Monitor)** | 이사회·집행임원 수준의 거버넌스 의사결정 | 5개 목표(EDM01~05): 거버넌스 체계 수립, 이득 전달, 리스크 최적화, 자원 관리, 투명성 확보. **RACI 차트**로 의사결정 권한 매트릭스 정의, **Design Factor 11개**(전략, 목표, 리스크, 컴플라이언스 등)를 조합하여 거버넌스 시스템 맞춤형 설계 |
| **APO (Align, Plan, Organize)** | 전략 ↔ 전술 정렬 | APO02 전략 매핑(Strategy Map, Balanced Scorecard), APO04 혁신 관리(Design Thinking, Lean Startup), APO12 리스크 관리(ISO 31000 통합), APO13 보안 관리(정보보호 거버넌스) |
| **BAI (Build, Acquire, Implement)** | 솔루션 수명주기 관리 | BAI02 요구사항 관리(BABOK v3 통합), BAI03 솔루션 아키텍처(TOGAF ADM Phase B/C/D 매핑), BAI11 프로젝트 관리(PMBOK 7th, PRINCE2, SAFe) |
| **DSS (Deliver, Service, Support)** | 일상 운영 및 서비스 제공 | DSS01~06: 운영 관리, 인시던트·요청 처리, 문제 관리(Known Error DB, RCA 5-Why/Fishbone), 변화 관리(CAB/ECAB), 서비스 연속성(ISO 22301) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정 및 내부 통제 | MEA01 성과 측정(CSF/KPI), MEA02 내부 통제 시스템(SOX, J-SOX), MEA03 컴플라이언스(ISO 27001, GDPR, PIPA, ISMS-P), MEA04 Assurance(내부감사, ISAE 3402) |
| **ITIL 4 34개 Practices** | 운영 우수성 프레임워크 | 14 General(Incident, Problem, Change, Service Desk, SLM…), 17 Service(Continuity, Availability, Capacity…), 3 Technical(AIOps, Deployment Mgmt.) |
| **TOGAF ADM** | 아키텍처 개발 방법론 | **Phase A(Architecture Vision) -> B,C,D(비즈니스/데이터/응용/기술) -> E,F(기회/마이그레이션) -> G,H(구현/거버넌스) -> 요구사항관리(ERM)**. **ArchiMate 3.2** 표기법으로 Business/Application/Technology Layer 시각화 |
| **CSF(KPI) 계층 구조** | 성과 측정 체계 | **Vision -> Strategic Goal -> IT Goal -> CSF -> KPI -> Metric**(COBIT Cascading Goals). 예: "고객만족 95%" -> "IT 서비스 가용성 99.95%" -> "MTTR
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 675 / 800

<- **이전**: [674. IT 경영 관리 핵심 토픽 674번 시험 요약](/studynote/12_it_management/05_security_compliance/674_it_management_core_topic_674_exam_summary/)
**다음**: [676. IT 경영 관리 핵심 토픽 676번 시험 요약](/studynote/12_it_management/05_security_compliance/676_it_management_core_topic_676_exam_summary/) ->

---
