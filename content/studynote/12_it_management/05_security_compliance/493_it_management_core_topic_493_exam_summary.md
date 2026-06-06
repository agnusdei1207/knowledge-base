---
title: "IT Management Core Topic 493 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사는 **IT 거버넌스(COBIT 2019) ↔ IT 서비스 운영(ITIL 4) ↔ 프로젝트 관리(PMBOK 7) ↔ 보안 거버넌스(ISO 27001/27002) ↔ EA(TOGAF/Zachman) ↔ 성과평가(BSC/KPI)**의 6대 축을 통합적으로 운용하여, 디지털 전환 시대의 **가치사슬(Value Chain)**과 **전략-실행-평가(Strategy-Execution-Evaluation)** 루프를 폐환속(Closed-loop)으로 설계하는 것이 본질이다.
> 2. **가치**: 글로벌 McKinsey/IDC 연구에 따르면, 성숙한 IT 거버넌스 체계 구축 시 **프로젝트 성공률 35% -> 75% 향상**, **TCO 20~30% 절감**, **보안 사고 대응시간 60% 단축(MTTR)**, **EA 기반 투자 시 ROI 2.4배**, **ISO 27001 인증 기업의 평균 사이버 사고 비용 230만 USD -> 130만 USD 절감**(IBM Cost of a Data Breach 2023) 등 정량적 효과를 입증한다.
> 3. **판단 포인트**: 기술사의 핵심 판단은 **① 프레임워크 간 중복 정의(예: ITIL Change Mgmt vs COBIT BAI03) 충돌 해결, ② Agile/DevOps 도입 시 거버넌스 경직성 vs 속도 간 트레이드오프, ③ 클라우드/AI/데이터 거버넌스에서 책임 분점 모델(RACI) 재설계, ④ BCP/DR의 RTO/RPO vs 비용 최적화, ⑤ 정보자산 중요도 평가 시 CIA Triad + 기밀성 가중치** 등 "프레임워크-현업-IT" 3자 정렬(Three Lines Model)이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 493번 토픽은 **IT 경영관리(Information Technology Management)** 영역의 핵심 통합 주제로, 기업이 IT를 단순 비용(Cost Center)에서 전략적 자산(Value Driver)으로 전환하기 위한 **거버넌스·관리 체계의 총체적 설계**를 다룬다. 한국정보통신기술협회(TTA)와 한국정보관리학회 기준으로, 본 영역은 크게 ① IT 거버넌스/전략, ② IT 프로젝트 및 서비스 운영, ③ 정보보안 및 리스크, ④ 데이터·EA 거버넌스, ⑤ 성과평가 및 투자관리의 5개 서브도메인으로 분류된다.

2024년 현재, **클라우드(Public/Hybrid)**, **AI/Gen-AI(LLM, RAG, MLOps)**, **제로트러스트(Zero Trust)**, **공급망 보안(SBOM, C-SCRM)**, **규제 준수(DORA, EU AI Act, 개인정보보호법)** 등 신기술·신규제 환경이 기존 거버넌스 프레임워크(COBIT 2019, ITIL 4, ISO 27001:2022)의 갱신을 요구하고 있어, 기술사 답안에서는 **"기존 프레임워크 + 신기술/신규제 통합 설계"** 능력을 보여주어야 한다.

```text
[ IT 경영관리 6대 핵심축 통합 아키텍처 ]

                          +----------------------------------+
                          |  비즈니스 전략 / BSC 비전 / KPI  |
                          +-------------+--------------------+
                                        | (전략 연계: Strategy Fit)
                                        v
        +--------------------------------------------------------------+
        |             ① IT 거버넌스 & 전략 기획                        |
        |  (COBIT 2019 · ISO 38500 · Porter Value Chain · Ward&Peppard)|
        +-------------+------------------------------------------------+
                      | (이해관계자·목표·평가체계)
       +--------------+--------------+---------------+-----------------+
       v              v              v               v                 v
+--------------+ +------------+ +--------------+ +--------------+ +--------------+
| ② 프로젝트   | | ③ IT서비스 | | ④ 정보보안 & | | ⑤ EA & 데이터 | | ⑥ 투자/성과  |
|   관리       | |   운영     | |   리스크     | |   거버넌스     | |   평가       |
| PMBOK 7      | | ITIL 4     | | ISO 27001    | | TOGAF 10      | | BSC · EVA    |
| PRINCE2      | | SRE/DevOps | | ISO 27005    | | Zachman       | | KPI · KPO    |
| Agile/Scrum  | | AIOps      | | NIST CSF 2.0 | | DAMA-DMBOK 2  | | ROI · TCO    |
| Earned Value | | Site Reli- | | Zero Trust   | | FEAF          | | BAM          |
+------+-------+ +-----+------+ +------+-------+ +------+-------+ +------+-------+
       |               |               |                |                |
       +---------------+---------------+----------------+----------------+
                                        |
                                        v
                          +--------------------------+
                          |  피드백 루프(Closed-Loop) |
                          |  모니터링->측정->개선      |
                          +--------------------------+
```

과거(1990~2000년대) **"IT는 백오피스"** 시대에는 **BS7799/ISO 27001(보안) + PMBOK 3rd(프로젝트) + ITIL v2(IT운영)** 3종 세트가 독립적으로 운용되었으나, **클라우드·모바일·AI의 융합, 코로나19 이후 재택/하이브리드 업무, 공급망 공격(SolarWinds, Log4j, MOVEit)** 등 복합 위협이 등장하면서 **"통합 거버넌스(Integrated Governance)"** 패러다임으로 전환되었다. 이를 **IIA(Institute of Internal Auditors)**는 **Three Lines Model(3 Lines of Defense: 1차 사업부, 2차 리스크/컴플라이언스, 3차 내부감사)**로 정리한다.

- **📢 섹션 요약 비유**: IT 경영관리를 **자동차 운전**에 비유하면, ① 전략(COBIT)=내비게이션, ② 프로젝트(PMBOK)=엔진 시동/가속, ③ 서비스(ITIL)=연료 주입·변속기, ④ 보안(ISO 27001)=ABS·에어백, ⑤ EA(TOGAF)=차체 프레임, ⑥ 성과평가(BSC)=계기판·블랙박스이다. 어느 하나라도 고장나면 사고가 나듯, 6대 축이 **폐환속(Closed-loop)**으로 연결되어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 6대 축은 각기 다른 국제표준(ISO/IEC 38500, 20000, 27001, PMBOK, ITIL 등)을 기반으로 하지만, **목표·프로세스·지표·개선(PDCA/Plan-Do-Check-Act)**이라는 공통 메타모델을 공유한다. 기술사 답안에서는 **"각 프레임워크의 정의역(domain) -> 정착 매개체(enabler) -> 평가 지표(metric) -> 상호 매핑(mapping)"** 4단계로 서술해야 한다.

```text
[ 프레임워크 간 매핑 및 책임 분담 (RACI × Three Lines) ]

                        +-------------------------------------------+
                        |        거버넌스 의사결정(Board/CIO)        |
                        |  +-------------+    +------------------+  |
                        |  | 전략위원회   |    |  리스크위원회    |  |
                        |  | (SteerCo)   |    | (Risk Co.)      |  |
                        |  +------+------+    +--------+---------+  |
                        +---------+--------------------+------------+
                                  |                    |
              +-------------------+--------------------+--------------+
              |                   |                    |              |
        1st Line              2nd Line            2nd Line         3rd Line
        (사업/IT부서)        (IT 거버넌스)        (CISO/컴플)      (내부감사)
              |                   |                    |              |
   +----------+----+    +--------+--------+   +--------+----+   +----+-----+
   |PMBOK Delivery|    |  COBIT BAI/DSS  |   |  ISO 27001  |   |  IIA Std|
   |Scrum/SAFe    |◄--►|  ITIL 4 SMS     |◄-►|  NIST CSF   |◄-►|  Audit  |
   |DevOps/CI/CD  |    |  PMBOK 7 Perf.  |   |  ISO 27005  |   |  SOX/ISSAF|
   +--------------+    +-----------------+   +-------------+   +----------+
                                  |                    |
                                  +---------+----------+
                                            v
                              +--------------------------+
                              |  KPI Dashboard / GRC     |
                              |  (ServiceNow · Archer ·  |
                              |  SAP GRC · OneTrust)     |
                              +--------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① IT 거버넌스 (Governance)** | 전략-목표-자원-리스크-성과의 5영역 의사결정 체계 | **COBIT 2019**의 40개 Governance/Management Objectives, **ISO/IEC 38500**의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior), **Three Lines Model(IIA 2020)**, **RACI** 매트릭스로 책임 분점 |
| **② 프로젝트 관리 (PMO/PPM)** | 단발성 프로젝트의 범위/일정/비용/품질/리스크/조달/이해관계자/통신 8대 영역 통합 관리 | **PMBOK 7th Edition**(8 Performance Domains + 12 Principles), **PRINCE2 7th**, **Earned Value Management(EVM: SPI, CPI, TCPI)**, **Agile(Scrum/SAFe/LeSS)**, **DevOps(DORA 4 metrics: Deployment Frequency, Lead Time, MTTR, Change Fail Rate)** |
| **③ IT 서비스 관리 (ITSM)** | 운영·변경·장애·문제·자산·용량·가용성·연속성의 7대 프로세스 SLA 기반 운영 | **ITIL 4**(Service Value System: Opportunity/Demand/Value, 34 Practices), **ISO/IEC 20000-1:2018**, **SRE(SLI/SLO/Error Budget)**, **AIOps(Anomaly Detection, RCA 자동화)**, **CMDB + Service Catalog** |
| **④ 정보보안 & 리스크 (InfoSec/GRC)** | CIA(기밀성·무결성·가용성) + Authenticity·Non-repudiation 등 자산 보호 | **ISO/IEC 27001:2022**(Annex A 93개 통제항목, 4개 테마: Organizational, People, Physical, Technological), **ISO 27005**(리스크 평가: Asset->Threat->Vuln->Impact), **NIST CSF 2.0**(GV/ID/PR/DE/RS/RC 6함수), **Zero Trust(NIST SP 800-207)**, **SBOM(SPDX/CycloneDX)** |
| **⑤ EA & 데이터 거버넌스** | 비즈니스-데이터-어플리케이션-기술 4계층의 표준화·재사용·현대화 | **TOGAF 10**(ADM 8단계: Preliminary->Vision->Business->IS->Tech->Opportunity->Migration->Impl->Change), **Zachman 6×6**, **FEAF**, **DAMA-DMBOK 2.0**(11 지식영역), **데이터 카탈로그(Collibra/Informatica), 데이터 메시, 데이터 패브릭** |
| **⑥ 투자/성과평가 (V&PM)** | IT 투자 포트폴리오의 전략 정렬, 가치 측정, 지속적 개선 | **BSC 4관점(Financial·Customer·Internal Process·Learning/Growth)**, **EVA(Economic Value Added)**, **Total Value of Opportunity(Forrester)**, **TCO·ROI·NPV·IRR**, **KPI Tree(CSF->KPI->KPO)**, **BAM(Business Activity Monitoring)** |

### 핵심 메커니즘 심화

**(1) COBIT 2019 핵심 메커니즘**: COBIT 2019는 **Governance System(거버넌스 시스템) + Components(5종: Process, Organizational Structure, Information, People/Skills, Technology) + Goals Cascade(13 Enterprise Goals -> 13 Alignment Goals -> 40 Mgmt/Governance Objectives)**의 3단 구조다. **"비즈니스 목표↔IT 목표↔프로세스 목표"**의 **Cascading**을 통해, 단순 통제가 아닌 **"측정 가능한 목표-지표(Maturity/Performance)"**체계를 만든다. 예: "고객만족 EG08 -> AG05(IT 만족도) -> BAI01(Managed Programs) -> KPI: 프로젝트 정시율 ≥ 90%"로 매핑.

**(2) ITIL 4 SVS(Service Value System)**: 5개 컴포넌트(Guiding Principles, Governance, Practices, Value Chain, Continual Improvement)가 **Opportunity/Demand -> Value**로 흐르는 시스템. **34 Practices 중 핵심 7개**(Incident Mgmt, Problem Mgmt, Change Enablement, Service Request, Service Desk, Service Level Mgmt, Monitoring & Event Mgmt)가 **DevOps/SRE**의 **On-call / Runbook / Postmortem**과 직접 매핑된다.

**(3) ISO 27001:2022 통제구조**: **Clause 4~10(경영시스템 요구사항)** + **Annex A 93 controls(4 themes)**. 신규 통제: 5.7 Threat Intelligence, 5.23 ICT Readiness for BCP, 5.30 ICT Readiness for Business Continuity, 8.9 Configuration Mgmt, 8.16 Monitoring Activities, 8.28 Secure Coding 등. **Statement of Applicability(SOA)** 문서가 인증의 핵심 산출물.

**(4) PMBOK 7th + Agile/DevOps 통합**: 8개 Performance Domain(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)는 **Predictive / Adaptive / Hybrid** 3개 개발방식 모두 지원. **EVM(Earned Value)**은 Schedule/Cost Performance Index(SPI, CPI) + To-Complete Performance Index(TCPI = (BAC-EV)/(BAC-AC))로 프로젝트 건강도 단일 수치화. **DORA 4 Metrics**가 DevOps 성과를 측정: Elite = 배포빈도 On-demand, Lead Time < 1hr, Change Fail < 5%, MTTR < 1hr.

**(5) EA(TOGAF) ADM 사이클**: 8단계 ADM(Architecture Development Method)은 **Preliminary->A:Architecture Vision
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 493 / 800

<- **이전**: [492. IT 경영 관리 핵심 토픽 492번 시험 요약](/studynote/12_it_management/05_security_compliance/492_it_management_core_topic_492_exam_summary/)
**다음**: [494. IT 경영 관리 핵심 토픽 494번 시험 요약](/studynote/12_it_management/05_security_compliance/494_it_management_core_topic_494_exam_summary/) ->

---
