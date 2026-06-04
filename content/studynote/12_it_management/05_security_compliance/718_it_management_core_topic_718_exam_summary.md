---
title: "718. IT 경영 관리 핵심 토픽 718번 시험 요약 (IT Management Core Topic 718 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 718번은 정보관리기술사 출제범위 중 "IT 거버넌스·전략·서비스·프로젝트·정보화 사업·아웃소싱·성과관리·리스크" 8대 축을 아우르는 종합 사례이며, COBIT 2019, ITIL 4, PMBOK 7th, ISO/IEC 38500, EA(TOGAF), BSC, BCM/DRS 등 글로벌 표준 프레임워크를 한국 정보통신기본법·클라우드컴퓨팅법·개인정보보호법·전자문서법 등 국내 법·제도 체계와 매핑하여 답안을 구성하는 것이 핵심이다.
> 2. **가치**: 단순 암기형 답안이 아닌 "문제 상황 진단 -> 평가 모델 적용 -> 개선 로드맵 도출 -> ROI/TCO 정량화"의 4단계 논리 체계를 보여줄 때 가산점이 발생하며, IT 투자 대비 비즈니스 가치(BVIT) 20~30% 향상, 인시던트 MTTR 60% 단축, 프로젝트 성공률 35%->75% 향상, 정보화 사업 예산 15~25% 절감 등 정량적 KPI 제시가 차별화 포인트가 된다.
> 3. **판단 포인트**: 거버넌스(누가 결정) vs 관리(어떻게 실행) 혼동, ITIL V3과 ITIL 4의 SVS·Service Value Chain 차이, COBIT 2019의 Focus Area(예: DevOps, Cyber Security, Risk)와 Design Factor, PMBOK 6th 10지식영역 vs 7th 8성능도메인의 변화, EA As-Is/To-Be Gap Analysis 시 ROI 미반영 함정, BSC 4관점(재무·고객·내부·학습성장)의 IT KPI 매핑, 아웃소싱 KPI(SLA·OLA·UC)·진출입 전략(빌더·리퍼·스크러버), 그리고 최근 디지털전환·클라우드·AI 거버넌스(AI 윤리·EU AI Act·국내 AI기본법) 적용 여부가 합격과 탈락을 가른다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management)는 단순한 IT 운영을 넘어, 기업의 경영 전략과 IT 자산을 연계하여 가치를 극대화하고 리스크를 통제하는 통합 관리 체계이다. 정보관리기술사 시험에서 718번 토픽이 핵심 사례로 분류되는 이유는, 최근 10년간(2015~2025) 정보화 사업이 "전사적자원관리(ERP)·데이터웨어하우스·BI" 중심에서 "클라우드·AI·데이터 거버넌스·ESG·제로트러스트" 중심으로 패러다임이 전환되었으며, 이에 따라 시행착오를 거버넌스·아키텍처·서비스·프로젝트·성과·리스크의 6개 관점에서 통합 진단하는 능력을 요구하기 때문이다.

```text
+--------------------------------------------------------------------+
|  [IT 경영 관리 6대 도메인 통합 프레임워크]                           |
|                                                                    |
|   +--------------+   +--------------+   +--------------+         |
|   | 거버넌스     |   | 전략/기획    |   | 서비스관리   |         |
|   | COBIT 2019   |◄--+ ISP · EA     |--►| ITIL 4       |         |
|   | ISO 38500    |   | TOGAF · FEA  |   | ISO 20000   |         |
|   | K-ICT 전략   |   | 디지털전환   |   | DevOps · SRE |         |
|   +------+-------+   +------+-------+   +------+-------+         |
|          |                  |                  |                  |
|          v                  v                  v                  |
|   +----------------------------------------------------+          |
|   |        [프로젝트 · 아웃소싱 · 성과 · 리스크]           |          |
|   |  PMBOK/PRINCE2  ·  MSP/ASP/SI  ·  BSC/KPI  ·  BCM  |          |
|   +----------------------------------------------------+          |
|          |                  |                  |                  |
|          v                  v                  v                  |
|   +----------------------------------------------------+          |
|   |     [법·제도·윤리] (정보통신기본법, 개인정보보호법,        |          |
|   |      전자문서법, AI기본법, 클라우드컴퓨팅법, ISMS-P)        |          |
|   +----------------------------------------------------+          |
+--------------------------------------------------------------------+
```

기존의 IT 관리는 ①기술 도입 중심(Silo), ②프로젝트 단위 관리(One-off), ③벤더 종속(Lock-in), ④내부 통제 중심(Internal Control)이라는 한계가 있었다. 이에 반해 현대의 IT 경영 관리는 ①거버넌스-관리-운영의 3-Layer 분리(Decision-Execution-Operation), ②전사 아키텍처(EA) 기반의 Portfolio 관리, ③Multi-Vendor·Multi-Cloud 전략, ④Value-Driven(가치 중심)·Risk-Based(리스크 기반)·Compliance-First(규정 우선)의 통합 체계로 진화하였다.

특히 2020년 이후의 변화는 ①코로나19에 따른 원격근무·디지털 가속(Digital Acceleration), ②공급망 공격(SolarWinds, Kaseya VSA)·랜섬웨어(Colonial Pipeline)·제로트러스트, ③EU AI Act·국내 AI기본법(2024.1. 시행)·데이터산업법, ④ESG 정보공시 의무화(2025년 유니버설 기준), ⑤클라우드 비용 폭증(FinOps), ⑥양자내성암호(PQC) 전환 수요 등이다. 기술사 답안에서는 이 변화의 "법적·기술적·경영적 함의"를 3가지 관점에서 풀어야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"건물의 구조·전기·소방·보안·환기·에너지관리 시스템(BMS)을 통합 운영하는 건물 자동화(BAS/IBMS) 시스템"** 과 같다. 개별 설비(기술)만 잘 만들어서는 안 되고, 한동한 빌딩의 임차인(경영진)이 원하는 가치(생산성·안전·비용최소화)를 달성하도록 모든 설비를 통합·조정하는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 6대 도메인은 상호 의존적으로 작동하며, **"방향(Strategy) -> 결정(Governance) -> 설계(Architecture) -> 실행(Project) -> 운영(Service) -> 평가(Performance)"** 의 PDCA + Value Chain 구조로 통합된다.

```text
[IT 경영 관리 Value Chain & Feedback Loop]
                              +--------------------+
                              | 1.전략(IT Strategy)  |
                              |  ·ISP/EA            |
                              |  ·BVIT·CSF          |
                              +---------+----------+
                                        | Strategy Mapping
                                        v
        +--------------------+ +--------------------+ +--------------------+
        | 2.거버넌스(COBIT)  | | 3.아키텍처(TOGAF)  | | 4.프로젝트(PMBOK)   |
        |  ·RACI·Design Fac. | |  ·ADM Cycle         | |  ·Phase/Gate        |
        |  ·Maturity Model   | |  ·As-Is/To-Be/Gap   | |  ·Risk Register     |
        +---------+----------+ +----------+---------+ +----------+---------+
                  |                        |                       |
                  +------------------------+-----------------------+
                                           v
                              +--------------------+
                              | 5.서비스관리(ITIL4)|
                              |  ·SVS·SVC          |
                              |  ·33 Practice       |
                              |  ·CSI·Continual     |
                              +---------+----------+
                                        | SLA/OLA/UC
                                        v
                              +--------------------+
                              | 6.성과평가(BSC/KPI)|
                              |  ·4 Perspective     |
                              |  ·IT Scorecard      |
                              |  ·Benchmarking      |
                              +---------+----------+
                                        | Feedback(성과->전략)
                                        +----------► (1)로
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략/기획** (Strategy) | IT-비즈니스 정렬, 투자 우선순위 | ISP(정보화전략계획) 4단계(현황분석->목표설정->사업기획->수립), EA TOGAF ADM(8단계 Preliminary->A->B->C->D->E->F->G->Req.Mgmt), BSP(기업시스템기획)·CSF(핵심성공요인)·SST(전략시나리오기법), BVIT(Business Value of IT) 모델 |
| **거버넌스** (Governance) | 의사결정·책임·통제 체계 | COBIT 2019의 40 Governance/Management Objective, 5 Focus Area(DevOps, Cybersecurity, Risk, Digital, BCM), 11 Design Factor, ISO/IEC 38500 6원칙(책임·전략·취득·성과·준법·인간), 3-Layer(지시->통제->실행) |
| **아키텍처** (Architecture) | 전사 정합성·표준화·재사용 | TOGAF 4 Domain(BA·DA·AA·TA), FEA(Federal EA) PRM·TRM·SRM, 데이터아키텍처(DAMA-DMBOK 11), EA Maturity(Gartner 5단계: Silo->Standardized->Optimized->Enterprise->Adaptive) |
| **프로젝트** (Project) | 일정·비용·품질·리스크 관리 | PMBOK 7th 8성능도메인(Stakeholder·Team·Development·Planning·Work·Delivery·Measurement·Uncertainty) + 6원칙 + Tailoring, 애자일(스크럼 XP), PRINCE2(7원칙·7테마·7프로세스), 단계-게이트(Stage-Gate) |
| **서비스** (Service) | SLA 기반 안정적 IT 서비스 제공 | ITIL 4 SVS(Service Value System: Opportunity/Demand/Value) + Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve), 34 Practice(General·Service·Technical), AIOps·SRE·DevOps |
| **성과/리스크** (Performance/Risk) | 정량평가·리스크 최소화 | BSC 4관점 KPI(예: 재무-ROI, 고객-NPS, 내부-MTTR, 학습-자격취득), COBIT Maturity(0~5), ISO 31000 Risk Management Process(Context->Ident->Anal·Eval->Treat->Monitor·Review), ISMS-P, BCM/DRS(ISO 22301) |

이 6대 도메인은 COBIT 2019의 "EDM(평가·지시·모니터) -> APO(정렬·계획·조직) -> BAI(빌드·획득·구현) -> DSS(전달·지원·운영) -> MEA(모니터·평가·검토)"의 5도메인 40오브젝티브와 정확히 1:1로 매핑된다. 기술사 답안에서 "COBIT 2019의 EDM 01(거버넌스 체계 설정)와 APO 02(전략관리)을 적용하여 IT-비즈니스 정렬도 정량화"와 같이 **표준 프레임워크의 특정 오브젝티브 코드(예: EDM01, APO02, BAI03, DSS02, MEA01)** 를 명시하면 전문성이 인정된다.

또한, 정량적 의사결정을 위해 **TCO(Total Cost of Ownership)·ROI(Return on Investment)·NPV·IRR·CBA(Cost-Benefit Analysis)·EVA(Economic Value Added)·VOI(Value of Investment)** 가 활용되며, 최근에는 **FinOps**(클라우드 비용 최적화)·**Green IT**(탄소배출 kWh당 KPI)·**Digital Maturity Model**(DMM, Acatech 5단계)가 추가되었다.

- **📢 섹션 요약 비유**: 6대 도메인은 **"자동차의 운전 시스템"** 과 같다. ①전략은 내비게이션(목적지), ②거버넌스는 운전자(조향·가속·브레이크 의사결정), ③아키텍처는 차체 설계(엔진·바퀴·섀시), ④프로젝트는 공장 조립(생산), ⑤서비스는 A/S·정비센터, ⑥성과/리스크는 계기판·사고보험이다. 한 부분만 고장나도 차량 전체가 위험해진다.

---

## Ⅲ. 비교 및 연결

기술사 시험에서 빈출되는 비교·대비 프레임워크는 ① COBIT vs ITIL, ②PMBOK 6th vs 7th, ③EA 프레임워크(TOGAF vs FEA vs Zachman), ④BSC vs IT Scorecard, ⑤Governance vs Management, ⑥Build vs Buy vs Rent(클라우드), ⑦SI vs ASP vs MSP, ⑧ITIL V3 vs ITIL 4 등이다.

| 구분 | COBIT 2019 | ITIL 4 |
| :--- | :--- | :--- |
| **목적** | IT 거버넌스·통제·목표달성 | IT 서비스 관리·가치 창출 |
| **주체** | 이사회·경영진·감사·컴플라이언스 | 서비스 운영자·프로세스 매니저·실무진 |
| **핵심** | 40 Governance/Management Objective, 5 Focus Area | 34 Practice, Service Value System, 4 Dimension |
| **측정** | Maturity Level 0~5, Process Capability(ISO 15504) | SLA, OLA, UC, KPI(CSAT·MTTR·MTBF) |
| **통합** | 다른 프레임워크(PMBOK·ITIL·ISO)를 통합 관리·감사 관점 | 서비스 운영 실무·자동화·AIOps |
| **최근 흐름** | AI 거버넌스·사이버보안·리스크·ESG Focus Area 추가 | SRE·DevOps·클라우드·Agile·Lean 통합(Service Value Chain) |

| 구분 | PMBOK 6th (2017) | PMBOK 7th (2021) |
| :--- | :--- | :--- |
| **구조** | 5 Process Group + 10 Knowledge Area | 8 Performance Domain + 12 Principles |
| **접근** | 프로세스·입력·산출물(Process-Based) | 원리·성과(Principle-Based·Value-Driven) |
| **주안점** | Plan-Do-Check-Act·49 Process | Tailoring·Predictive/Agile/Hybrid |
| **측정** | Earned Value(EV, PV, AC, CV, SV) | Outcome·Outcome Measures(성과 측정의 다양화) |
| **변화** | 정형화·반복 가능 | 애자일·하이브리드·적응형 라이프사이클 |
| **핵심 메시지** | "What to do" | "Why & How to do" |

| 구분 | Build(자체구축) | Buy(패키지 도입) | Rent(클라우드·서비스) |
| :--- | :--- | :--- | :--- |
| **투자비** | 초기 높음(CAPEX^) | 중간(라이선
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 718 / 800

<- **이전**: [717. IT 경영 관리 핵심 토픽 717번 시험 요약](/studynote/12_it_management/05_security_compliance/717_it_management_core_topic_717_exam_summary/)
**다음**: [719. IT 경영 관리 핵심 토픽 719번 시험 요약](/studynote/12_it_management/05_security_compliance/719_it_management_core_topic_719_exam_summary/) ->

---
