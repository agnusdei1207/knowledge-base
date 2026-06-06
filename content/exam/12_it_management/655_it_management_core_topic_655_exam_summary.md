---
title: "IT Management Core Topic 655 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 핵심 토픽은 COBIT 2019, ITIL 4, ISO/IEC 38500, TOGAF 10 등 글로벌 거버넌스 프레임워크와 한국 정보화 사업법, EA(Enterprise Architecture) 4A(BA/DA/AA/TA), PPM(Portfolio Management), BCM/DRS, 정보보안경영(ISMS-P)·개인정보보호법·클라우드컴퓨팅법·AI기본법을 통합한 **IT-비즈니스 정렬(Strategic Alignment)·가치창출(Value Delivery)·리스크 최적화(Risk Optimization)·자원관리(Resource Management)·성과측정(Performance Measurement)**의 5대 영역을 다룸.
> 2. **가치**: 정보화 사업의 **TCO 20~30% 절감**, IT 투자 ROI 평균 15~25% 향상, EA 기반 중복 투자 제거로 시스템 수명주기 비용(Lifecycle Cost) 절감, 거버넌스 성숙도 3->5단계 상승 시 운영 효율 40% 개선, ISMS-P 인증 취득으로 보안사고 60% 감소, DRS RTO 4시간->30분, RPO 24시간->0~5분 달성.
> 3. **판단 포인트**: 거버넌스 모델은 **집중형(Centralized) vs 분산형(Decentralized/Federated) vs 하이브리드(COE+Spoke)**, EA 도입은 **Top-down(TOGAF ADM) vs Bottom-up(현업 요구) vs Event-driven(규제/경쟁사)**, 클라우드 전환은 **Lift&Shift vs Replatform vs Refactor vs Rebuild(Re-architect)** 중 TCO·확장성·핵심역량 보존 트레이드오프, 보안은 **Zero Trust(never trust, always verify) vs Perimeter-based vs Defense-in-Depth** 전략 선택이 핵심 의사결정 포인트.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도구화를 넘어 기업 전략·운영·문화 전반의 디지털 패러다임 전환이 가속화됨에 따라, IT 경영관리(Information Technology Governance & Management)는 **"IT가 비즈니스 가치를 어떻게 극대화하면서 위험을 통제하는가"**에 대한 경영학적·공학적 통합 접근을 요구한다. 과거 CIO(Chief Information Officer)가 정보시스템 운영에만 집중하던 1.0 시대에서 벗어나, 현재의 CDO(Chief Data Officer), CISO(Chief Information Security Officer), CPO(Chief Privacy Officer), CAIO(Chief AI Officer)가 이사회 수준에서 의사결정에 참여하는 **"Digital Board"** 구조로 진화하고 있다.

특히 4차 산업혁명(AI, IoT, Big Data, Cloud, Blockchain, Metaverse, Quantum) 시대에는 데이터가 5대 핵심 생산요소(土地·勞動·資本·經營·情報 -> 6번째 요소: 데이터)로 부상하면서, **데이터 거버넌스(Data Governance)**가 전통 IT 거버넌스와 분리·통합되는 양면성을 보이고 있다. 한국에서는 **데이터 산업법(2022.4. 시행)**, **AI 기본법(2026.1. 시행예정)**, **클라우드컴퓨팅 발전법(2025.1. 시행)**, **공공데이터 이용자 촉진법**, **주요정보통신기반시설법** 등 IT 관련 법·제도가 급증하여 컴플라이언스 복잡도가 기하급수적으로 증가하고 있다.

```text
+------------------------------------------------------------------+
|           IT 경영관리 5대 영역 & 글로벌 프레임워크 맵                |
+------------------------------------------------------------------+
|                                                                  |
|  [이사회/경영진] --- 전략 정렬(Strategic Alignment) ------+        |
|         |                                                 |        |
|         v                                                 v        |
|  +--------------+   +--------------+   +--------------+         |
|  | 거버넌스     |   | 가치창출     |   | 리스크 최적화 |         |
|  | Governance   |   | Value Deliv. |   | Risk Opt.    |         |
|  +--------------+   +--------------+   +--------------+         |
|  | • COBIT 2019 |   | • ITIL 4     |   | • ISO 27001  |         |
|  | • ISO 38500  |   | • PMBOK 7    |   | • ISMS-P     |         |
|  | • NIST CSF   |   | • DevOps     |   | • ISO 27701  |         |
|  +--------------+   +--------------+   +--------------+         |
|         |                  |                  |                  |
|         +----------+-------+----------+-------+                  |
|                    v                  v                          |
|           +--------------+   +--------------+                    |
|           | 자원관리     |   | 성과측정     |                    |
|           | Resource Mgmt|   | Performance  |                    |
|           +--------------+   +--------------+                    |
|           | • EA(TOGAF)  |   | • BSC        |                    |
|           | • PPM        |   | • KPI/CSF    |                    |
|           | • FinOps     |   | • TCO/ROI    |                    |
|           +--------------+   +--------------+                    |
|                    |                  |                          |
|                    +----------+-------+                          |
|                               v                                  |
|                    +------------------+                           |
|                    | 비즈니스 가치    |                           |
|                    | (Value Realized) |                           |
|                    +------------------+                           |
+------------------------------------------------------------------+
```

한국 IT 경영관리의 특수성으로는 **공공부문 정보화사업 법정 절차(정보시스템 구축·운영 지침, 발주자 책임 하자 보수기간, 감리법인 제도)**, **민감정보·개인정보 3법(개인정보보호법, 정보통신망법, 신용정보법)**, **DAMA-DMBOK 기반 데이터 거버넌스**, **한국 EA 4A Framework(BA/DA/AA/TA)**, **디지털서비스 정부혁신**, **공공부문 클라우드 우선 원칙(Cloud First)** 등을 들 수 있다. 이러한 환경에서는 단순히 글로벌 베스트 프랙티스를 모방하는 것이 아니라, **법·제도·조직문화·기술 성숙도**를 고려한 **맥락적 IT 거버넌스(Context-aware IT Governance)**가 필수적이다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **도시계획**(Urban Planning)과 같다. 건축물(시스템) 하나만 잘 짓는 것이 아니라, 상하수도·전기·도로·공원·치안(데이터·보안·네트워크·거버넌스·컴플라이언스) 등 도시 인프라 전반을 조화롭게 설계·건설·유지보수하는 **마스터플랜**(EA)과 **도시 운영 매뉴얼**(COBIT/ITIL)이 필요한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 아키텍처는 크게 **① 거버넌스 메타-프레임워크(Meta-framework)**, **② EA 4A(아키텍처 프레임워크)**, **③ 서비스 운영 프레임워크(ITIL 4 SVS)**, **④ 거버넌스 시스템(COBIT 2019 Cascade)**, **⑤ 가치 흐름(Value Stream)**의 5개 레이어로 구성된다.

```text
+--------------------------------------------------------------------+
|                  COBIT 2019 Governance System Cascade                |
+--------------------------------------------------------------------+
|                                                                    |
|  +---------------------+                                           |
|  | Stakeholder Needs & |  (이해관계자 니즈: 가치 창출, 리스크, 자원)|
|  | Drivers (37 Goals)  |                                           |
|  +----------+----------+                                           |
|             v                                                      |
|  +---------------------+                                           |
|  | Enterprise Goals    |  (13개 기업목표: 수익성, 고객만족, 규제)   |
|  | (EG)                |                                           |
|  +----------+----------+                                           |
|             v                                                      |
|  +---------------------+                                           |
|  | Alignment Goals     |  (13개 정렬목표: AG01~AG13)                |
|  | (AG)                |                                           |
|  +----------+----------+                                           |
|             v                                                      |
|  +---------------------+                                           |
|  | Management          |  (관리목표: EDM(05), APO(14), BAI(11),     |
|  | Objectives (MO)     |   DSS(06), MEA(04) = 40개)                |
|  +----------+----------+                                           |
|             v                                                      |
|  +---------------------+                                           |
|  | Components:         |  • Process (40)  • Organizational (7)     |
|  | (7 categories)      |  • Information   • Skills/Competencies   |
|  |                     |  • Infrastructure • Services/Infr/Apps    |
|  |                     |  • People, Behavior, Culture, Ethics      |
|  +----------+----------+                                           |
|             v                                                      |
|  +---------------------+                                           |
|  | Governance &        |  (5가지 중점영역: EDM 5개 목표)            |
|  | Management Practices|   - Benefits Realization                  |
|  +---------------------+   - Risk Optimization                     |
|                              - Resource Optimization                |
|                              - Stakeholder Transparency             |
|                              - Strategic Alignment                  |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스·관리 통합 프레임워크 | 40개 관리목표(APO 14·BAI 11·DSS 6·MEA 4·EDM 5)를 5개 도메인(평가·지시·모니터)으로 분류, **Focus Area**(예: 사이버보안, DevOps, 위험, 컴플라이언스, 디지털거버넌스 등 40+개) 단위로 맞춤형 적용, **Maturity/Capability Level 0~5** 평가(ISO/IEC 330xx PAM), **Design Factors 11개**(전략, 목표, 위험, 문제, 환경 등)로 거버넌스 시스템 자동 조정 |
| **ISO/IEC 38500** | 이사회 수준 IT 거버넌스 국제표준 | 6원칙(책임·전략·취득·성과·준거·인간행위), **Governance Model = 3-Tier(Evaluate·Direct·Monitor)**, PDCA 사이클, **Governance Authority & Accountability Matrix**(RACI), 영국에서 발안되어 6개국(ISACA·IEC·ISO·ITGI·IPPU·OECD) 협력 표준화 |
| **TOGAF 10 (ADM)** | EA 구축·운영 방법론 | **ADM Cycle 8단계**(Preliminary·A~H) + **Requirements Mgmt** = 9단계, **Architecture Content Framework**(Deliverable·Artifact·Building Block), **Enterprise Continuum**(Generic->Industry->Organization->Project), **TRM(Technical Reference Model)**·**III-RM(Integrated Information Infrastructure Reference Model)**, 2022년 **TOGAF Standard 10th Edition**은 마이크로서비스·클라우드·AI 확장 |
| **ITIL 4 SVS** | IT 서비스 관리(Service Management) | **Service Value System**(Opportunity/Demand->Value->SVS: Guiding Principles·Governance·Practices·Continual Improvement·Value Chain Activities), **34개 Practices**(일반 14·서비스 9·기술 3·ITSM 8), **4 Dimensions**(조직·사람·정보·공급자·가치흐름·기술), **Value Stream** 단위 운영(예: 신규 서비스 런칭 14단계 -> 5단계로 최적화) |
| **PMBOK 7 / PRINCE2** | 프로젝트 관리 표준 | **PMBOK 7th**(2021): 8개 **Performance Domains**(이해관계자·팀·접근방식·계획·프로젝트작업·공급·측정·불확실성), 12가지 **Principles of Project Management**, **Tailoring** 강조, **PRINCE2**(2023 7th): 7원칙·7테마·7프로세스, AXELOS(현재 PeopleCert) 관리 |
| **PPM/PMO** | 프로젝트 포트폴리오 관리 | **Portfolio->Program->Project** 위계, **Strategic Fit·Value Maximization·Balance·Risk Mgmt·Synergy** 5대 원칙, **BSC + IT-BSC(Nolan Norton) + PPM Dashboard**, **3대 모자** 전략(Keep Up·Make Up·Catch Up) - McKinsey |

COBIT 2019의 **Focus Area**는 사이버보안(Cybersecurity), 클라우드 컴퓨팅, DevOps, 디지털 거버넌스, BCM, 데이터 거버넌스, AI/ML 거버넌스, ESG-IT, 메타버스 거버넌스 등 40여 개 영역에 대해 **특화된 목표·관리실무·디자인 팩터**를 제공하여, 조직의 디지털 전환 단계별 맞춤형 거버넌스 설계가 가능하다. **Capability Level(0~5)**은 `0: 불완전(미실행)`, `1: 초기(Individual)`, `2: 관리(Managed)`, `3: 확립(Defined)`, `4: 예측(Predictable)`, `5: 최적화(Optimizing)`로 PAM(Process Assessment Model)에 따라 평가하며, 목표 Level과의 Gap 분석을 통해 개선 로드맵을 도출한다.

**PPM(Portfolio Management) 핵심 공식**:
- **NPV(순현재가치)** = Σ [CFt / (1+r)^t] - 투자금
- **IRR(내부수익률)** = NPV=0 이 되는 r
- **TCO(Total Cost of Ownership)** = 하드웨어(30%) + 소프트웨어(20%) + 인건비(35%) + 유지보수(10%) + 기회비용(5%)
- **PI(우선순위지수)** = (전략가치 × 0.4) + (위험감소 × 0.2) + (ROI × 0.2) + (준법성 × 0.2)
- **Risk Score** = (위험 발생 가능성 × 영향도 × 대응 난이도) / 관리 통제력

- **📢 섹션 요약 비유**: COBIT 2019의 Cascade는 **"회사 비전 하향식 카지노 게임"**과 같다. 경영진이 가치(Value)·리스크(Risk)·자원(Resource) 카드를 확률적으로 섞어 13개 기업목표(EG)를 정하고, 이를 IT 정렬목표(AG)로 변환한 뒤, 40개 관리목표(MO) 단위로 카드를 내는 구조다. **Design Factor**는 카지노 룰(규칙)을 조직 상황에 맞게 조정하는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** (거버넌스) | **ITIL 4** (서비스관리) | **ISO 38500** (이사회표준) | **TOGAF 10** (아키텍처) | **PMBOK 7** (프로젝트) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스 + 관리 통합 | IT 서비스 가치 제공 | 이사회 거버넌스 원칙 | EA 구축/전환 | 프로젝트 성공 |
| **대상**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 655 / 800

<- **이전**: [654. IT 경영 관리 핵심 토픽 654번 시험 요약](/studynote/12_it_management/05_security_compliance/654_it_management_core_topic_654_exam_summary/)
**다음**: [656. IT 경영 관리 핵심 토픽 656번 시험 요약](/studynote/12_it_management/05_security_compliance/656_it_management_core_topic_656_exam_summary/) ->

---
