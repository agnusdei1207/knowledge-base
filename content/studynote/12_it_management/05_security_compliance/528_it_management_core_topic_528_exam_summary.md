+++
title = "528. IT 경영 관리 핵심 토픽 528번 시험 요약 (IT Management Core Topic 528 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 528. IT 경영 관리 핵심 토픽 528번 시험 요약
## (정보관리기술사 시험 대비 — IT Management 통합 서머리)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT(거버넌스) ↔ ITIL(서비스) ↔ PMBOK/Agile(전달) ↔ TOGAF(아키텍처) ↔ ISO 27001(보안)** 5대 프레임워크를 Value(가치 사슬), Risk(리스크), Resource(자원) 3축으로 통합하여, IT가 사업 전략(BSC·CSF·KPI)을 실현하도록 **End-to-End 라이프사이클**(Plan->Design->Build->Run->Improve)을 통제하는 경영 시스템이다.
> 2. **가치**: 성숙도 1단계->5단계로 1단계 상승 시 평균 **운영비 23% 절감, 프로젝트 성공률 28%->78% 향상, MTTR 65% 단축, 보안사고 41% 감소, TCO 3년 누적 35% 절감**(Gartner/ISACA 2023~2025 벤치마크)이라는 정량적 ROI를 산출하며, **비즈니스-IT 정렬(Alignment)** 지수(Boehm/Sabat) 기준으로 ROI 4.7배 효과가 보고된다.
> 3. **판단 포인트**: (a) **Build vs. Buy vs. SaaS vs. Cloud-Native** 4택 1 의사결정, (b) **Monolith -> SOA -> MSA -> Serverless**로의 아키텍처 진화 시 마이그레이션 비용·조직 역량·데이터 일관성(CAP) 트레이드오프, (c) **Agile-Waterfall 하이브리드(SaFe/LeSS/Spotify 모델)** 선택 시 통제-속도 균형, (d) **Zero-Trust vs. 경계보안**, (e) **On-Premise vs. Hybrid vs. Multi-Cloud** TCO 비교 — 이 5대 의사결정에서 기술사의 **Trade-off Insight**가 평가된다.

---

## Ⅰ. 개요 및 필요성

### 1.1 IT 경영 관리의 정의와 등장 배경

IT 경영 관리(IT Management)는 단순한 시스템 운영을 넘어, **"IT 투자 대비 사업 가치 극대화"**를 목적으로 하는 통합 관리 체계이다. 2000년대 Y2K 문제, 2008년 금융위기, 2010년 모바일·클라우드 전환, 2018년 GDPR·개인정보보호법 강화, 2020년 코로나19 디지털 가속, 2023년 생성형 AI(LLM) 도입이라는 **6대 외부 충격** 속에서 IT 경영은 다음 5가지 패러다임 전환을 겪었다.

| 시기 | 패러다임 | 핵심 키워드 | 한계 |
|:---:|:---:|:---|:---|
| 1970~1990 | **Data Processing** | EDP, Mainframe, OLTP | 비용 중심, 사업 연계 부족 |
| 1990~2000 | **Management Information** | ERP(Oracle/SAP), BPR(Hammer), SCM/CRM | 실패율 70%(Standish), 통합 리스크 |
| 2000~2010 | **Governance & Compliance** | SOX, ITIL v2/v3, COBIT 4/5, ISO 27001 | 통제 비대화, Agile과 충돌 |
| 2010~2020 | **Digital & Platform** | Cloud, Mobile, Big Data, DevOps, MSA, Agile@Scale | 보안·거버넌스 격차, Shadow IT |
| 2020~2025 | **AI & Trust** | Zero Trust, AIops, 생성형 AI, ESG, Data Mesh | AI 윤리, 데이터 사일로, 규제 급변 |

### 1.2 왜 IT 경영 관리가 필요한가 — 5대 통찰

```text
        +--------------------------------------------------------------+
        |          5대 통찰 : IT 경영 관리가 답해야 할 5가지 질문          |
        +--------------------------------------------------------------+
                                     |
        +----------------+-----------+-----------+----------------+
        |                |           |           |                |
   +----v-----+   +------v------+  +v--------+ +v----------+ +--v----------+
   | Q1.가치  |   | Q2.리스크   |  | Q3.자원  | | Q4.정렬    | | Q5.지속가능  |
   | ROI?     |   | Compliance? |  | 적정?   | | Biz↔IT?  | | Innovation? |
   +----+-----+   +------+------+  +----+----+ +-----+----+ +------+------+
        |                |              |            |             |
        v                v              v            v             v
   +---------+    +------------+   +---------+  +---------+  +----------+
   |COBIT EDM|    |ISO 27001  |   |ITIL 4   |  |BSC+CSF  |  |DevOps+   |
   |Balanced |    |+ Zero Trust|   |+FinOps  |  |+TOGAF   |  |AI/MLOps  |
   |Scorecard|    |+ISO 27701 |   |+GreenIT |  |+Capability|  |+DataOps  |
   +---------+    +------------+   +---------+  +---------+  +----------+
   EDM=Evaluate,Direct,Monitor (COBIT 2019 핵심 거버넌스 도메인)
```

### 1.3 Old Paradigm vs. New Paradigm

| 항목 | Old(2000년대) | New(2024~) |
|:---|:---|:---|
| 거버넌스 | **사후 통제**(감사·컴플라이언스) | **사전 예방 + 실시간** 거버넌스(Continuous Audit) |
| 개발 | **Waterfall**, 연 1~2회 릴리스 | **Agile + DevSecOps**, 일 단위 CI/CD, GitOps |
| 아키텍처 | **Monolith + SOA(ESB)** | **MSA + Event-Driven + Serverless** |
| 인프라 | **On-Premise**, 수동 Capacity Planning | **Multi/Hybrid Cloud + IaC(Terraform/Ansible)** |
| 데이터 | **데이터웨어하우스, 야간 ETL** | **Data Lakehouse + Streaming(Kafka/Flink)** |
| 보안 | **경계 방어(Perimeter), Castle-Moat** | **Zero Trust(never trust, always verify), SASE/SSE** |
| 조직 | **기능별(Dev/QA/Ops) 사일로** | **2-Pizza Team, SRE, Platform Engineering** |
| KPI | 가용성 99.9%, 예산 준수 | DORA 4指标(배포빈도/리드타임/MTTR/변경실패율), NSat, MTTD |

- **📢 섹션 요약 비유**: IT 경영 관리는 **비행기 조종실(코크핏)**과 같습니다. 30년 전에는 자동 조종 장치가 거의 없어 기장이 수동으로 모든 계기를 읽었지만(Old), 지금은 **자동조종·자동착륙·장애진단·연료관리**가 한 화면에 통합되어(COBIT·ITIL·PMBOK) 비행사가 핵심 의사결정(사업 정렬·리스크)만 하면 됩니다. 단, 자동조종 장치(프레임워크)도 **연 1회 인증·갱신**(감사·성숙도 평가)이 필요합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 5대 프레임워크 통합 아키텍처 — "GSAVI" 모델

```text
   +--------------------------------------------------------------------+
   |         GSAVI : 통합 IT 경영 5-Layer Reference Architecture        |
   +--------------------------------------------------------------------+

   +-----------------------------------------------------------------+
   | Layer 5 : 개선(Improve) — CSI, Lean, Kaizen, PDCA, OKR          | <- ITIL CSI / COBIT BAI
   +-----------------------------------------------------------------+
   | Layer 4 : 통제(Control) — Risk, Compliance, Audit, Security     | <- COBIT EDM / ISO 27001
   +-----------------------------------------------------------------+
   | Layer 3 : 운영(Run) — Service Operation, Incident, Problem     | <- ITIL 4 / SRE
   +-----------------------------------------------------------------+
   | Layer 2 : 전달(Deliver) — Build, Test, Deploy, Release         | <- PMBOK/SAFe/DevOps
   +-----------------------------------------------------------------+
   | Layer 1 : 계획(Plan) — Strategy, Architecture, Portfolio       | <- TOGAF/EA/BSC
   +-----------------------------------------------------------------+
                                    ^
                                    | (모든 Layer를 관통)
                          +---------+---------+
                          |  Value Stream     |
                          |  (가치사슬 End2End)|
                          +-------------------+
```

### 2.2 핵심 구성 요소 상세 (5대 프레임워크 × 5대 영역)

| # | 프레임워크 | 정식 명 | 주요 영역 | 핵심 프로세스/컴포넌트 | 최신 버전(2024) |
|:-:|:---|:---|:---|:---|:---:|
| 1 | **COBIT** | Control Objectives for Information and Related Technologies | **거버넌스/관리** | EDM(5) + APO(14) + BAI(11) + DSS(6) + MEA(4) = 40 프로세스 | **2019**(2024 Refresh) |
| 2 | **ITIL** | Information Technology Infrastructure Library | **서비스 운영/생명주기** | 5단계(Value Streams): Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support + 7 Guiding Principles + 4 Dimensions | **ITIL 4** |
| 3 | **PMBOK** | Project Management Body of Knowledge | **프로젝트 관리** | 5 Process Groups + **8 Performance Domains**(People, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) + 12 Principles | **PMBOK 7th(2021)** |
| 4 | **TOGAF** | The Open Group Architecture Framework | **엔터프라이즈 아키텍처** | **ADM(Architecture Development Method)** 8단계: Preliminary->A:Vision->B:Business->C:Data/App->D:Tech->E:Opportunities&Migration->F:Implementation Governance->G:Change Mgmt + **ADM Cycle 반복** | **TOGAF 10**(2022) |
| 5 | **ISO 27001** | Information Security Management | **정보보안 거버넌스** | ISMS 4단계(Plan-Do-Check-Act) + **Annex A 93 통제항목**(2022) + 27002 통제세트 + **27017(클라우드), 27018(개인정보), 27701(PIMS)** | **2022 Rev.** |

### 2.3 COBIT 2019 — 거버넌스의 표준

```text
   +----------------------------------------------------------------+
   |                    COBIT 2019 Governance System                |
   +----------------------------------------------------------------+
   |                                                                |
   |   +----------+  +----------+  +----------+  +----------+      |
   |   |   EDM    |  |  APO     |  |   BAI    |  |   DSS    | MEA  |
   |   | Evaluate |  | Align,   |  | Build,   |  | Deliver, |      |
   |   | Direct,  |-> | Plan &   |-> | Acquire, |-> | Service, |->...  |
   |   | Monitor  |  | Organize |  | Implement|  | Support  |      |
   |   | (5 proc) |  | (14 proc)|  | (11 proc)|  | (6 proc) |      |
   |   +----+-----+  +----+-----+  +----+-----+  +----+-----+      |
   |        |             |             |             |             |
   |        v             v             v             v             |
   |   +------------------------------------------------------+     |
   |   |  Enablers (7대 원동력)                                |     |
   |   |  1. Principles, Policies, Frameworks                 |     |
   |   |  2. Processes                                        |     |
   |   |  3. Organizational Structures                        |     |
   |   |  4. Information                                      |     |
   |   |  5. People, Skills, Competencies                     |     |
   |   |  6. Services, Infrastructure, Applications           |     |
   |   |  7. Culture, Ethics, Behavior                        |     |
   |   +------------------------------------------------------+     |
   |                                                                |
   |   Goals Cascade:                                              |
   |   Stakeholder Needs -> Enterprise Goals -> Alignment Goals       |
   |        (13개)              (13개)              (13개)            |
   |              -> IT-Related Goals -> Process Goals                |
   |                  (13개)              (40개)                      |
   +----------------------------------------------------------------+
```

**핵심 원리**: **"목표 사슬(Goals Cascade)"** — 이해관계자 니즈(BSC 4관점) -> 기업목표 -> 정렬목표 -> IT목표 -> 프로세스목표로 흘러내려 모든 거버넌스 결정을 **SMART KPI**로 추적. **RACI 행렬**로 책임 소재 명확화(R:책무/A:승인/C:자문/I:통보).

### 2.4 ITIL 4 — 서비스 가치 시스템(SVS)

```text
                    +--------------------------------+
                    |  Opportunity/Demand (기회/수요)  |
                    +----------------+---------------+
                                     v
       +--------------------------------------------------+
       |          Service Value System (SVS)              |
       | +----------------------------------------------+ |
       | | Guiding Principles (7): Focus on Value,      | |
       | | Start Where You Are, Progress Iteratively,   | |
       | | Collaborate, Think & Work Holistically,      | |
       | | Keep It Simple, Optimize & Automate          | |
       | +----------------------------------------------+ |
       |                                                  |
       | +----------+ +----------+ +------------------+  |
       | |Governance|->| Service  |->| Value Chain       |  |
       | |          | |  Value   | | (Plan->Engage->    |  |
       | |          | |  Chain   | |  Design&Trans->   |  |
       | |          | |          | |  Obtain&Build->   |  |
       | |          | |          | |  Deliver&Supp)   |  |
       | +----------+ +----------+ +------------------+  |
       |                                                  |
       | +----------------------------------------------+ |
       | | Practices (34개, 2019 축소): Incident,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 528 / 800

<- **이전**: [527. IT 경영 관리 핵심 토픽 527번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/527_it_management_core_topic_527_exam_summary/)
**다음**: [529. IT 경영 관리 핵심 토픽 529번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/529_it_management_core_topic_529_exam_summary/) ->

---
