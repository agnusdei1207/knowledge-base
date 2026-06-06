---
title: "IT Management Core Topic 762 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사(762번) 시험은 **IT 거버넌스(COBIT 2019)·전략 기획(ISP/BSP)·프로젝트 관리(PMBOK 7th+Agile)·서비스 운영(ITIL 4)·엔터프라이즈 아키텍처(TOGAF ADM)·정보보안(ISMS-P/ISO 27001)·데이터 거버넌스(DAMA-DMBOK2)** 등 7대 도메인을 통합적으로 판단하는 상위 의사결정 역량을 측정하는 시험이며, 단순 암기가 아닌 **Trade-off 기반 아키텍처 의사결정 능력**을 평가한다.
> 2. **가치**: 합격 시 **CIO·CDO·CISO·수석컨설턴트** 등 조직의 IT 전략·투자·리스크를 최종 책임지는 직무 수행 자격이 부여되며, 실제 현장에서 **연간 IT 예산 100억~수천억 원급 포트폴리오**의 우선순위 결정, 다수 이해관계자 간 갈등 조정, 규제 준수와 사업 속도 간 균형점 도출에 직결된다.
> 3. **판단 포인트**: 시험의 핵심은 "정답 선택"이 아니라 **"왜 이 프레임워크를 선택했는가"의 정당화 논리**(Rationale)이며, 같은 문제라도 **업종(금융/공공/제조), 규모(대기업/중견/스타트업), 성숙도(CMMI 1~5)**에 따라 최적 답안이 달라진다는 점을 명시적으로 진술할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사(762번)는 과학기술정보통신부령 제74호에 의거한 **국가기술자격법상 최고 등급 기사(技士)** 자격으로, IT 분야 4개 기술사(정보관리, 전자계산기조직응용, 정보통신, 정보보안) 중 **가장 광범위한 거버넌스·관리 트랙**을 담당한다. 2019년 NCS(국가직무능력표준) 개편과 4차 산업혁명 가속화로 인해, 단순한 SW/HW 기술 지식을 넘어 **"기술-비즈니스-리스크" 3축을 통합하는 의사결정자 관점**이 요구된다.

특히 2022년 이후 출제 경향은 다음과 같이 변화했다:
- **과거**: COBIT 5 단계, BPR, SOA 등 개별 프레임워크 정의형 출제
- **현재**: "클라우드 마이그레이션 시 거버넌스 체계 재설계", "AI 도입 시 데이터 거버넌스와 개인정보보호의 충돌" 등 **복합 시나리오형 서술/약술형** 비중 확대(전체 배점의 약 65%)
- **최신 트렌드**: 디지털플랫폼정부법(2025.1 시행), EU AI Act, 생성형 AI 거버넌스, 양자내성암호(PQC) 등 규제-기술 융합 이슈

```text
[정보관리기술사(762) 7대 핵심 도메인 맵]

                    +-----------------------------+
                    |   정보관리기술사 합격 역량    |
                    |  (CIO/CDO/CISO 관점 통합)    |
                    +--------------+--------------+
        +----------+----------+---+----+----------+----------+----------+
        v          v          v        v          v          v          v
   +--------+ +--------+ +--------+ +--------+ +--------+ +--------+ +--------+
   |IT      | |전략·   | |프로젝트| |서비스  | |엔터    | |정보    | |데이터  |
   |거버넌스| |기획    | |관리    | |운영    | |프라이즈| |보안    | |거버넌스|
   |        | |        | |        | |        | |아키텍처| |        | |        |
   |COBIT   | |ISP/BSP | |PMBOK 7 | |ITIL 4  | |TOGAF   | |ISMS-P  | |DAMA    |
   |2019    | |EA연계  | |Agile   | |DevOps  | |ADM     | |ISO27001| |DMBOK2  |
   |ISO38500| |Balanced| |SAFe    | |SRE     | |Zachman | |PQC/    | |DCAM    |
   |        | |Scorecard| |PRINCE2 | |        | |FEAF    | |제로트러스트| |        |
   +--------+ +--------+ +--------+ +--------+ +--------+ +--------+ +--------+
                                  |
        +-------------------------+-------------------------+
        |     4차 산업혁명 신기술 레이어 (적분 영역)         |
        |  Cloud | BigData | AI/GenAI | IoT | Blockchain  |
        +---------------------------------------------------+
```

기존의 IT 관리론은 **CFO 중심의 비용 통제**(TCO 절감, ROI 계산) 위주였으나, 현재는 **CDO·CISO·CCO(규약준수책임자)와의 공동 의사결정**으로 확장되었다. 2024년 한국정보화진흥원의 조사에 따르면 국내 500대 기업 중 73%가 **IT 거버넌스 위원회**를 설치·운영하고 있으며, 이 중 41%는 정보관리기술사 자격을 위원회 필수 요건으로 명시하고 있다.

- **📢 섹션 요약 비유**: IT 부서를 하나의 **"국가"**라고 비유하면, 거버넌스는 **헌법(COBIT)**, 전략기획은 **국가전략(ISP)**, 프로젝트관리는 **공공사업(PMBOK)**, 서비스관리는 **행정운영(ITIL)**, 아키텍처는 **국토계획(TOGAF)**, 정보보안은 **국방부(ISMS-P)**, 데이터 거버넌스는 **통계청·국세청(DAMA)**에 각각 대응한다. 기술사는 이 모든 부처를 조율하는 **국무총리급 총리**의 시야를 가져야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

정보관리기술사의 7대 도메인은 **"전략-설계-구축-운영-평가"**의 5단계 IT Value Chain으로 통합되며, 각 단계는 COBIT 2019의 40개 관리목표(Management Objective)와 직접 매핑된다.

```text
[IT Value Chain & 7대 도메인 매핑 아키텍처]

    +------------------------------------------------------------+
    | ① 전략 기획 (Plan) --------- ISP 수립, BAA(BA) 분석       |
    |   |   +- 연계 도메인: IT 거버넌스 + EA                      |
    |   v                                                        |
    | ② 아키텍처 설계 (Design) --- TOGAF ADM(8단계)              |
    |   |   +- 연계 도메인: EA + 데이터 모델링                    |
    |   v                                                        |
    | ③ 구축·전환 (Build/Acquire)                                 |
    |   |   +- 프로젝트 관리: PMBOK 7th + Agile(Scrum/SAFe)     |
    |   |   +- 연계 도메인: 거버넌스(투자통제) + 보안(설계검토)  |
    |   v                                                        |
    | ④ 서비스 운영 (Deliver/Support)                             |
    |   |   +- ITIL 4 SVS(34개 실무), DevOps, SRE                |
    |   |   +- 연계 도메인: 서비스 카탈로그 + 보안관제(SOC)      |
    |   v                                                        |
    | ⑤ 성과 측정·개선 (Evaluate/Monitor)                         |
    |     +- BSC 4관점, OKR, CMMI, NCSI, 정보화실태조사          |
    +------------------------------------------------------------+
        ^v 전 단계에 공통 적용: 정보보안(ISMS-P) + 데이터 거버넌스(DAMA)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스(Governance)** | 이사회의 IT 의사결정 체계 | COBIT 2019의 **EDM(5개)·APO(14개)·BAI(11개)·DSS(6개)·MEA(4개)** = 총 40 Governance/Management Objectives. 디자인 팩터 11개(전략, 목표, 리스크, 이슈 등)로 조직별 거버넌스 시스템 **맞춤형 설계** |
| **전략·기획(Strategy)** | IT-비즈니스 정렬(Strategic Alignment) | ISP(정보화전략계획) 5개년 -> BSP(업무정보화전략) -> BAA(BA) -> RFP. Ward & Peppard의 **IS 전략 기법**(5-forces, Value Chain, SWOT-Centric) + Blue Ocean |
| **프로젝트 관리(PM)** | 일정·품질·원가·리스크 통제 | PMBOK 7th의 **8개 성능영역**(Planning, Work, Delivery, Measurement, Uncertainty, Organization, Change, Business). 애자일은 Scrum(3~9명, 2~4주 Sprint) + SAFe(레벨 1~5, ART 50~125명) |
| **서비스 관리(Service)** | IT 서비스 전생애주기 | ITIL 4의 **SVS(Service Value System)** = Opportunity/Demand/Value <- 34개 Practice <- 7개 Guiding Principle. **Change Enablement**(CAB/ECAB), **Incident/Problem/SLM** |
| **엔터프라이즈 아키텍처(EA)** | 업무·데이터·응용·기술 4계층 정합성 | TOGAF **ADM 8단계**(Preliminary->A:Vision->B:Business->C:Data/Apps->D:Tech->E:Opportunities->F:Migration->G:Implementation->H:Change Mgmt) + **Architecture Repository**(ABB, ARB, AS-IS/TO-BE) |
| **정보보안(Security)** | CIA(기밀성·무결성·가용성)+진정성·부인방지 | ISMS-P 인증 16개 영역 104개 통제항목. **제로트러스트**(NIST SP 800-207): "Never Trust, Always Verify" -> 정책결정점(PDP)/정책실행점(PEP) |
| **데이터 거버넌스(Data)** | 데이터 자산의 마스터/메타/품질 관리 | DAMA-DMBOK2 **11개 지식영역**(Data Architecture, Modeling, Storage, Security, Integration, DW/BI, Reference/Master Data, Metadata, Quality, Governance, Ethics). **DCAM**(Data Management Capability Assessment Model) 성숙도 6단계 |

**핵심 원리 상세**:

- **거버넌스 ↔ 관리 구분**: COBIT 2019에서 **Governance(5 EDM) = 의사결정·평가·감독·지시·감시**이며, **Management(35 APO/BAI/DSS/MEA) = 계획·구축·운영·모니터링**을 수행한다. 시험에서 "이 활동이 Governance인가 Management인가"를 묻는 빈도가 매우 높으며, **EDM은 항상 이사회의 책임**이라는 점이 정답 키이다.
- **전략 정렬의 3단계**: Henderson & Venkatraman의 **SAM(Strategic Alignment Model)**에서 **Business Strategy -> IT Strategy -> Organizational Infrastructure & Processes**의 양방향 정렬을 요구. 특히 **"Strategy Execution"** 측면(BSC의 Learning & Growth 관점) 누락이 대표적 감점 포인트.
- **PMBOK 7th 패러다임 전환**: 6th까지는 **5개 프로세스 그룹 + 10개 지식영역**의 Input/Tool/Output 중심이었으나, 7th는 **원리(Principles 12) + 성능영역 8개** 중심. **"가치(Value) 전달"**이 최상위 원리이며, Predictive(Waterfall) ↔ Adaptive(Agile) ↔ Hybrid를 **Tailoring**으로 선택.
- **ITIL 4의 가치 공동창조(Value Co-Creation)**: ITIL v3의 26 프로세스 -> ITIL 4의 **34 Practice**. 핵심은 **SVC(Service Value Chain)** 6단계(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)와 **7 Guiding Principle**(Focus on Value, Start Where You Are, Progress Iteratively, etc.).
- **TOGAF ADM 반복성**: 8단계가 **선형이 아니라 반복(Iteration)**. 특히 Preliminary->A:Architecture Vision은 **Phase 0+1을 동시에** 진행할 수 있으며, 각 Phase 종료 시 **Architecture Contract**로 이해관계자 동의 확보.
- **제로트러스트 3대 기둥**: NIST SP 800-207의 핵심은 **(1) 모든 자원 암호화, (2) 동적 정책평가(PEPA), (3) 마이크로세그멘테이션**. 기존 경계보안(Perimeter Security) 대비 **East-West Traffic** 통제 능력이 비약적으로 향상됨.
- **DAMA DMBOK2 11영역**: 데이터 거버넌스 ≠ 데이터 관리(전영역 총괄). **Master/Reference Data**가 핵심이며, 금융권의 경우 **BCBS 239**(리스크 데이터 집계) 준수가 글로벌 표준.

- **📢 섹션 요약 비유**: 7대 도메인을 **오케스트라**에 비유하면, 거버넌스는 **지휘자(COBIT 2019)**, 전략기획은 **악보(ISP)**, 프로젝트관리는 **각 파트별 연주(PMBOK)**, 서비스관리는 **콘서트장 운영(ITIL 4)**, 아키텍처는 **음악厅 배치(TOGAF)**, 정보보안은 **경비시스템(ISMS-P)**, 데이터 거버넌스는 **음반 아카이브(DAMA)**이다. 기술사는 이 모든 악기가 **동일한 박자(Value Delivery)**로 연주되도록 만드는 **객석의 청중(또는 작곡가 겸 지휘자)**의 안목을 갖춰야 한다.

---

## Ⅲ. 비교 및 연결

7대 도메인 내·외부에서 혼동하기 쉬운 프레임워크를 명확히 구분해야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001/ISMS-P** |
| :--- | :--- | :--- | :--- |
| **목적** | IT **거버넌스**(이사회 관점) | IT **서비스 관리**(운영 관점) | 정보보호 **경영시스템** |
| **주체** | 이사회·CxO·감사위원회 | IT 서비스 제공자·수혜자 | CISO·경영진·전 임직원 |
| **핵심 산출물** | 40개 관리목표, 11개 디자인 팩터 | 34개 Practice, SVC 6단계 | 16개 영역 104개 통제항목 |
| **평가 방식** | Design Factor 기반 Maturity | 4단계 Practice Maturity (Initial->Managed->
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 762 / 800

<- **이전**: [761. IT 경영 관리 핵심 토픽 761번 시험 요약](/studynote/12_it_management/05_security_compliance/761_it_management_core_topic_761_exam_summary/)
**다음**: [763. IT 경영 관리 핵심 토픽 763번 시험 요약](/studynote/12_it_management/05_security_compliance/763_it_management_core_topic_763_exam_summary/) ->

---
