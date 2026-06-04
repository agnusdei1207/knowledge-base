---
title: "738. IT 경영 관리 핵심 토픽 738번 시험 요약 (IT Management Core Topic 738 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019, ITIL 4, ISO 27001/20000, CMMI, Balanced Scorecard(BSC)** 등 글로벌 거버넌스·서비스·보안 표준을 통합하여 **전략-아키텍처-구축-운영-평가**(Strategy-Architecture-Build-Run-Evaluate) 5단계 라이프사이클을 IT-비즈니스 정렬(Strategic Alignment) 아래 체계적으로 운용하는 경영 체계이다.
> 2. **가치**: 글로벌 컨설팅 firm인 Gartner·McKinsey 통계에 따르면 EA(Enterprise Architecture) 기반 IT 거버넌스 도입 조직은 **IT 투자 ROI 평균 23~35% 향상**, **프로젝트 실패율 40% 감소**, ISMS·ISO 20000 인증 획득 시 **입찰 가산점 5~15%** 및 **컴플라이언스 위반 리스크 70% 절감** 효과를 얻는다.
> 3. **판단 포인트**: **어떤 프레임워크를 조합할지**(COBIT 거버넌스 ↔ ITIL 서비스 운영 ↔ ISO 인증), **어떤 KPI와 BSC 관점으로 성과를 측정할지**(재무/고객/내부프로세스/학습성장), **IT 조직을 비용센터(Internal Cost Center)로 둘지 수익센터(Internal Service Provider/Profit Center)로 전환할지**가 C-Level 의사결정의 핵심 쟁점이다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 부서는 데이터센터 운영·네트워크 유지보수·전산실 관리에 머물러 "전산지원 조직(Cost Center)"으로 인식되어 왔다. 그러나 **클라우드 전환, AI·데이터 기반 의사결정, 디지털 트랜스포메이션(DX), ESG·공급망 컴플라이언스(ISO 27001, GDPR, 개인정보보호법, ISMS-P)**가 가속화되면서 IT는 단순 지원 조직이 아니라 **기업의 핵심 전략 자산이자 수익 창출 엔진**으로 재정의되고 있다. 한국에서는 2024년 기준 **정보관리기술사** 시험에서 IT 거버넌스·EA·ITIL·프로젝트관리·정보보안·SW 공학·DX·빅데이터·AI 윤리까지 통합 응용 문제가 출제되며, 단순 암기형이 아닌 **사례 기반 의사결정 문제**(예: "OO사의 IT 부서 개편안을 COBIT 관점에서 평가하시오")가 주를 이룬다.

따라서 IT 경영관리의 핵심은 **표준 프레임워크를 알고 있는 수준을 넘어, 기업 현안(legacy 시스템 이관, 클라우드 비용 폭증, 보안 사고 대응, 신기술 PoC 실패)에 표준·방법론·KPI를 어떻게 적용할지를 판단할 수 있는 엔지니어링 역량**이다.

```text
+------------------------------------------------------------------------+
|            IT 경영관리 5단계 라이프사이클 (SABRE 모델)                    |
|                                                                        |
|   +----------+    +----------+    +----------+    +----------+          |
|   | Strategy |---->|Architecture|--->|  Build   |---->|   Run    |         |
|   |  전략수립 |    |  아키텍처 |    |  구축/개발 |    |  서비스운영 |         |
|   +----------+    +----------+    +----------+    +----------+          |
|        ^                                              |                  |
|        |              +----------+                    |                  |
|        +--------------| Evaluate |<--------------------+                  |
|                       | 성과평가 |   KPI/BSC/Risk                        |
|                       +----------+                                       |
|                                                                        |
|   +-------------------------------------------------------------+       |
|   |  통합 거버넌스 레이어 (Cross-Cutting Concerns)                  |       |
|   |  • COBIT 2019  (목표-위험-자원-평가 40 Governance Obj.)       |       |
|   |  • ITIL 4      (서비스 가치 체계 SVS, 34 Practices)            |       |
|   |  • ISO 27001   (ISMS, 93 Annex A 통제항목)                     |       |
|   |  • ISO 20000   (SMS, 서비스관리시스템)                          |       |
|   |  • CMMI v2.0   (5성숙도, 20 Practice Area)                    |       |
|   |  • PMBOK 7th   (8 Performance Domain, 12 Principle)           |       |
|   +-------------------------------------------------------------+       |
+------------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교**
- *기존(2000년대 이전)*: "시스템이 안정적으로 돌아간다"가 곧 IT 성과 -> 가동률 99.99%, MTBF(평균고장간격) 중심
- *현재(2020년대 이후)*: "비즈니스 가치와 고객 경험(UX), 데이터 기반 의사결정 속도"가 IT 성과 -> NPS, Time-to-Market, Revenue per IT FTE, **CIR(Current IT Ratio)** ≤ 4%, **Run 비용 ≤ 70%** 유지

- **📢 섹션 요약 비유**: IT 경영관리는 **항공우주 산업의 ILS(Integrated Logistic Support, 통합후원지원)** 와 같다. 항공기 한 대를 만드는 것보다 **30년간 부품·정비·인적훈련·문서·규정을 통합 관리**하는 체계가 더 중요하듯, IT도 **단일 시스템 구축보다 거버넌스·운영·평가 체계를 지속적으로 굴리는 시스템**이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 아키텍처는 크게 **① 거버넌스(의사결정)층**, **② 프로세스(실행)층**, **③ 데이터(측정)층**, **④ 기술(인프라)층**의 4계층으로 구성되며, 각 계층은 **RACI 매트릭스**(Responsible, Accountable, Consulted, Informed)와 **메타-프로세스(Governance->Management->Operational 3-tier)** 로 연결된다.

```text
[4-Tier IT 경영관리 참조모델 (참고: TOGAF+COBIT 통합관점)]

    +----------------------------------------------------------+
    |  Tier 1: 거버넌스 (Board / Steering Committee)            |
    |  - CIO, CDO, CISO, CEO, 외부이사                          |
    |  - 의사결정: 거버넌스 목표, Risk Appetite, IT 투자배분     |
    |  - 산출물: IT 전략맵, BSC Scorecard, Risk Register        |
    +------------------------+---------------------------------+
                             | (RACI: Accountable)
                             v
    +----------------------------------------------------------+
    |  Tier 2: 관리 (IT Management / EA Team / PMO)            |
    |  - EA, PMO, ITSM, GRC(Governance·Risk·Compliance)         |
    |  - 활동: 전략연계, 아키텍처 표준, 포트폴리오 관리           |
    |  - 표준: TOGAF ADM, COBIT Mgmt Obj, PMBOK 프로세스       |
    +------------------------+---------------------------------+
                             | (RACI: Responsible)
                             v
    +----------------------------------------------------------+
    |  Tier 3: 운영 (DevOps / SRE / SOC / 헬프데스크)           |
    |  - Change, Incident, Problem, Service Desk, Monitoring    |
    |  - KPI: MTTR, SLA 99.95%, Change Success Rate 95%+      |
    |  - 자동화: AIOps, IaC(Terraform/Ansible), CI/CD           |
    +------------------------+---------------------------------+
                             | (RACI: Informed)
                             v
    +----------------------------------------------------------+
    |  Tier 4: 데이터·기술 (Infrastructure / Data Platform)     |
    |  - Hybrid Cloud (AWS·Azure·GCP·NCP), K8s, DB, Network     |
    |  - 데이터 거버넌스: Data Lake, Lakehouse, Data Mesh       |
    |  - 보안: Zero Trust, SASE, EDR/XDR, SIEM                  |
    +----------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (ISC)** | CIO·CEO·CISO·사업부서 임원 합동 의사결정 기구, 분기 1회 정례 | RACI 매트릭스, Risk Appetite Statement, IT 투자 Prioritization (e.g., McKinsey 7S+BCG Matrix 연동) |
| **EA(Enterprise Architecture)** | 비즈니스↔데이터↔어플리케이션↔기술 4계층 매핑, 표준화·중복제거 | TOGAF ADM(Architecture Development Method) 8단계: **Preliminary->A:비전->B:비즈니스->C:정보시스템->D:기술->E:기회->F:마이그레이션->G:거버넌스**. Zachman Framework 6×6 매트릭스, ARIS, ArchiMate 3.2 표기법 |
| **ITSM (IT Service Management)** | 서비스 카탈로그·요청·인시던트·문제·변경·릴리즈·구성관리 | **ITIL 4 SVS(Service Value System)**: 7 Guiding Principle, 34 Practice, 4 Dimension(Org·People·Info·Tech·Partners·Value Streams). CMDB, Incident->Problem->Known Error DB, Change Advisory Board(CAB) |
| **GRC (Governance·Risk·Compliance)** | 컴플라이언스 통합, 리스크 정량화, 통제 자동화 | ISO 27001:2022(93 통제), ISO 31000(리스크 프로세스), NIST CSF 2.0(6 Function: Govern·Identify·Protect·Detect·Respond·Recover), SOC 2 Type II |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리, 방법론 표준화, 자원 배분 | **PMBOK 7th(2021)**: 8 Performance Domain(Stakeholder·Team·Development·Planning·Project Work·Delivery·Measurement·Uncertainty), 12 Principle. **PRINCE2** 7 Principle, Agile(Scrum/Kanban), SAFe 6.0 |
| **BSC & KPI 엔진** | 전략->측정 가능 지표 변환, 정량적 성과관리 | **Kaplan-Norton Balanced Scorecard 4관점**(재무·고객·내부프로세스·학습성장). OKR(Objective & Key Result), KPI Tree(CSF->KPI->KPI Metric) |
| **정보보안 관리체계 (ISMS)** | 기밀성·무결성·가용성 + 개인정보·컴플라이언스 | **ISMS-P 인증**(한국인터넷진흥원), ISO 27001/27701, DLP, EDR, SIEM, Zero Trust(SDP/ZTNA), 암호화 AES-256/RSA-4096, FIDO2/WebAuthn |

**핵심 수식 및 정량 판단 기준**
- **CIR (Current IT Ratio) = (IT 운영·유지보수비) / (총 IT 예산)** -> 목표 ≤ **40%**, Run 비용 최적화 시 Build/Innovation 비율 상승
- **ROI 계산**: NPV, IRR, Payback Period, TCO(Total Cost of Ownership) 3~5년 분석
- **가용성(Availability) = MTBF / (MTBF + MTTR)** -> Tier IV = 99.995% (연 26분 이내 장애)
- **이행률 = 적용통제항목 수 / 전체 통제항목 × 100%**, ISMS 인증 유지 시 90% 이상

- **📢 섹션 요약 비유**: IT 경영관리의 4계층은 **자율주행차의 아키텍처**와 같다. **거버넌스=탑승자(운전자·내비게이션이 목적지 결정)**, **관리계층=ADAS·경로계획 ECU**, **운영계층=제동·조향 액추에이터**, **데이터·기술계층=센서·LiDAR·맵**. 한 층이 멈추면 사고가 나듯, **어느 한 계층의 거버넌스 부재는 곧 IT 재해로 직결**된다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 영역에서 가장 빈번히 혼동되는 프레임워크 간 비교와, **EA-TOGAF / COBIT-2019 / ITIL-4** 3대 표준 간 관계를 명확히 해야 한다. 시험에서는 "다음 중 COBIT과 ITIL의 차이점으로 가장 적절한 것은?" 같은 비교 문제가 단골로 출제된다.

| 구분 | **COBIT 2019** | **ITIL 4 (2019~)** | **ISO 27001:2022** | **PMBOK 7th (2021)** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·경영(Why/What) | IT 서비스 운영·가치 창출(How) | 정보보안 관리체계 인증(보안 통제) | 프로젝트 단위 관리 방법론(How) |
| **대상 범위** | 전체 IT(End-to-End Governance) | 서비스 라이프사이클 | 정보자산·통제 항목 | 개별 프로젝트 |
| **구조** | 40 Governance/Management Objective, 7 Component(원리·정책·프로세스·조직·정보·인적자원·문화) | 7 Guiding Principle, 34 Practice, 4 Dimension, SVS(Value Chain) | Clause 4~10 + Annex A 93 통제항목 (4 Themes: Organisational·People·Physical·Technological) | 8 Performance Domain, 12 Principle, 49 Process, 5 Process Group(Initiating·Planning·Executing·M&C·Closing) |
| **적용 주체** | CIO·이사회·감사 | 서비스 운영팀·헬프데스크·SRE | CISO·정보보안팀 | PM·PMO·프로젝트 스폰서 |
| **측정/평가** | Capability/Maturity(0~5), Process Assessment Model(PAM) | Maturity(0~5), Service Value(Stream·Outcome) | 인증 심사(Stage 1·2 + Surveillance) | Earned Value(EV·PV·AC), SPI·CPI |
| **인증 가능** | ❌ (자격증만: COBIT 2019 Foundation/Design&Implementation) | ❌ (자격증: ITIL Foundation/MP/SL) | ✅ ISO 27001 Lead Auditor | ❌ (PMP/PfMP/CAPM) |
| **다른 표준 연계** | ITIL·ISO 27001·TOGAF·PMBOK과 매핑 | COBIT·DevOps·Lean·Agile | COBIT(보안 통제), ISO 27701(개인정보) | COBIT(프로젝트 거버넌스),
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 738 / 800

<- **이전**: [737. IT 경영 관리 핵심 토픽 737번 시험 요약](/studynote/12_it_management/05_security_compliance/737_it_management_core_topic_737_exam_summary/)
**다음**: [739. IT 경영 관리 핵심 토픽 739번 시험 요약](/studynote/12_it_management/05_security_compliance/739_it_management_core_topic_739_exam_summary/) ->

---
