---
title: "741. IT 경영 관리 핵심 토픽 741번 시험 요약 (IT Management Core Topic 741 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **IT 거버넌스(COBIT 2019/ISO 38500) -> 전략 기획(EA-TOGAF) -> 서비스 운영(ITIL 4) -> 디지털 전환/아웃소싱**을 하나의 피드백 루프(Plan–Build–Run–Measure)로 통합하는 4축 경영관리 체계이며, 정보기술 부문과 사업 부문 간의 **Value Chain Alignment**가 핵심이다.
> 2. **가치**: 정량적으로는 IT 투자 ROI 평균 **18.4%**(Gartner 2024), 프로젝트 성공률 28%->65%(PMI), TCO 20~35% 절감, 정성적으로는 **BSC 4관점(재무/고객/내부/학습성장)** 기반 전략적 의사결정 고도화 및 ISO/IEC 38500·ISMS-P 인증을 통한 컴플라이언스 신뢰도 확보.
> 3. **판단 포인트**: (a) 거버넌스 프레임워크 선택 시 **COBIT 2019 40개 거버넌스/관리 목표** 중 조직 maturity(0~5)에 맞는 Focus Area 선정, (b) EA 단계 적용 시 **TOGAF ADM Preliminary~Phase H** 중 어느 깊이까지 수행할지(Strategy/Capability/Portfolio), (c) 운영 모델은 **On-Premise·Private Cloud·Public Cloud·Hybrid** 4-Grid 중 **BIA(Business Impact Analysis)** 기반 RTO/RPO 임계치로 결정, (d) 아웃소싱은 **Core-Context-Non-Core** 분류에 따른 Make-or-Buy 의사결정.

---

## Ⅰ. 개요 및 필요성

21세기 기업의 IT 부서는 단순 **Cost Center**에서 벗어나 **전략적 Business Enabler**로 진화했다. 그러나 한국 산업현장에서는 여전히 IT 투자 실패율(Standish Group 기준)이 66~80%에 달하며, 그 원인의 **57%**가 ‘전략 부재·거버넌스 미비·수요관리 실패’(CHAOS Report 2023)에 기인한다. 기술사 시험 741번(IT 경영 관리)은 바로 이 **“왜 IT가 사업 성과로 연결되지 못하는가”**라는 근본 문제를 다룬다.

과거(1990~2000년대)에는 CIO(Chief Information Officer)가 **시스템 구축 중심**으로 활동했으나, 현재(2020~2025)는 **CDO(Chief Data Officer)·CTO·CISO**와의 4-CXO 협업 구조, **클라우드 FinOps**, **AI 거버넌스**, **ESG-IX(Environmental-Social-IT)** 등 확장된 책임 영역을 가져야 한다. 이에 ISO/IEC 38500(2015, 2024 개정)에서는 IT 거버넌스 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 제시하며, **EDM( Evaluate-Direct-Monitor) 사이클**을 통한 **지속적 통제(Continuous Assurance)**를 강조한다.

```text
[IT 경영관리 4대 축(4 Pillar) 통합 프레임워크]

  +----------------------------------------------------------------------+
  |                  IT 경영관리 통합 거버넌스 체계                        |
  +----------+---------------+------------------+--------------+--------+
             |               |                  |              |
   +---------v------+ +------v--------+ +-------v------+ +----v---------+
   |  Pillar 1      | |  Pillar 2     | |  Pillar 3    | |  Pillar 4    |
   |  거버넌스/전략 | |  아키텍처/기획 | |  운영/서비스 | |  전환/혁신    |
   |  (Govern)      | |  (Plan)       | |  (Run)       | |  (Innovate)  |
   +---------+------+ +------+--------+ +-------+------+ +----+---------+
             |               |                  |              |
   +---------v------+ +------v--------+ +-------v------+ +----v---------+
   | COBIT 2019     | | TOGAF 10 ADM  | | ITIL 4 SVS   | | 클라우드/DX  |
   | ISO 38500 EDM  | | Zachman F/W   | | DevOps SRE   | | AI·데이터거버|
   | BSC 4관점      | | EA Repository | | SLA/OLa/UC   | | Lean-Agile   |
   | KPI/CSF        | | SoA/Principle | | Incident->Svc | | MSA/SI 아웃  |
   +----------------+ +---------------+ +---------------+ +--------------+
             |               |                  |              |
             +---------------+-----+------------+--------------+
                                   |
                          +--------v---------+
                          |  Plan-Build-Run-  |
                          |  Measure (PBRM)  |
                          |  피드백 루프      |
                          +------------------+
```

한국 공공부문은 **「정보시스템의 효율적 도입 및 운영에 관한 지침」(행정안전부)**, 민간은 **DGB(데이터 산업법, 2022)·ISMS-P(정보보호 관리체계)** 등 강력한 규제를 받고 있어, **컴플라이언스 기반 IT 경영**은 선택이 아닌 **의무**다. 또한 2024년 기준 국내 기업의 **클라우드 전환률 78%**(과학기술정보통신부), **MSA(Microservices Architecture) 도입률 42%**, **AI 서비스 도입률 31%**로 가속화되면서, 전통적 ITIL 기반 운영만으로는 **자동화·자율운영(Autonomic Ops)** 요구를 충족할 수 없게 되었다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같다. 첼로(거버넌스)는 저음을 잡고, 바이올린(전략)은 멜로디를 만들고, 트럼펫(운영)은 즉시 반응하며, 팀파니(전환)는 새로운 화성을 도입한다. 지휘자(거버넌스 위원회)가 **박자(Metric)·악보(EA)·분배(SLA)**를 통제하지 않으면 모두 불협화음(Chaos)이 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 4-Pillar는 **개방형·계층형·폐루프(Closed-Loop)** 구조로 결합된다. 핵심은 “**측정할 수 없으면 관리할 수 없다(You can’t manage what you can’t measure)**”이며, 이를 위해 **CSF(Critical Success Factor) -> KPI(Key Performance Indicator) -> KGI(Key Goal Indicator)**의 3단계 인과 사슬(Causal Chain)을 정의한다.

```text
[ IT 경영관리 계층 아키텍처 (Layered Architecture) ]

  +--------------------------------------------------------------------+
  |  L5: 의사결정층 (Decision) – 이사회/IT전략위원회(ISC)/CxO            |
  |      +- 입력: BSC Scorecard, ESG 보고, COBIT EDM 결과               |
  +--------------------------------------------------------------------+
  |  L4: 거버넌스층 (Governance) – COBIT 2019 / ISO 38500 EDM          |
  |      +- Evaluate->Direct->Monitor  -> 정책/표준/SOP/감사               |
  +--------------------------------------------------------------------+
  |  L3: 전략/기획층 (Strategy & Architecture)                         |
  |      +- TOGAF ADM(Preliminary~H), 정보화전략계획(ISP), EA Repo      |
  |      +- Zachman 6×6 매트릭스(What/How/Where/Who/When/Why × Scope)   |
  +--------------------------------------------------------------------+
  |  L2: 서비스/프로젝트층 (Service & Delivery)                        |
  |      +- PMBOK 7th 8성능영역, PRINCE2 7원칙/7프로세스, Agile/Scrum  |
  |      +- ITIL 4 SVS: 34 Practice, Service Value Chain(SVC)          |
  |      +- SLA/OLA/UC 3단 계약 체계                                    |
  +--------------------------------------------------------------------+
  |  L1: 기술/인프라층 (Technology Infrastructure)                      |
  |      +- On-Prem / Private·Public Cloud / Hybrid Multi-Cloud        |
  |      +- Container(K8s), IaC(Terraform/Ansible), Observability      |
  |      +- FinOps: Showback -> Chargeback -> Unit Economics             |
  +--------------------------------------------------------------------+
  |  L0: 데이터/AI층 (Data & AI Foundation)                            |
  |      +- 데이터 거버넌스(DAMA-DMBOK), 메타·마스터·레이크 하우스      |
  |      +- MLOps, LLM Governance, AI Act/EU AI Risk Tiering            |
  +--------------------------------------------------------------------+
            ^                       |
            |   측정·모니터링·피드백  |
            +-----------------------+
              (KPI -> CSF -> 정책개선)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(평가-지시-모니터)** | 이사회/CxO가 IT 방향을 통제 | COBIT 2019의 5개 거버넌스 목적(위험 최적화, 자원 최적화, 이해관계자 가치, 포트폴리오 투명화, 내부통제)과 40개 Governance/Management Objective로 매핑. EDM01(체계 평가) -> EDM02(방향 지시) -> EDM03(성과 모니터) 순환. |
| **ADM(아키텍처 개발방법론)** | EA Repository 및 청사진 작성 | TOGAF 10의 Preliminary(Framework 정의) -> Phase A(Architecture Vision: TOGAF ADM Cycle 0~E 반복) -> Phase B/C/D/Business·Data·Application·Technology) -> Phase E(기회/솔루션) -> Phase F(구현 계획) -> Phase G(거버넌스 이행) -> Phase H(아키텍처 변경 관리). **Iteration**과 **Migration Planning**이 핵심. |
| **SVS(서비스 가치 시스템)** | 가치 공동창출(Value Co-Creation) | ITIL 4의 7가지 Guiding Principle(Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize) + 34 Practice(general·service·technical management). **Service Value Chain**: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve. |
| **PBRM(Plan-Build-Run-Measure)** | 사업-IT 정렬 및 피드백 루프 | Plan(정보화전략·ISP·EA) -> Build(프로젝트·SI) -> Run(운영·서비스데스크) -> Measure(BSC·SLA·KPI) -> 다시 Plan. **IT-Business Alignment(BAS) Maturity 5단계(Luftman 2003)** 적용. |
| **FinOps/Unit Economics** | 클라우드 비용 최적화 | Showback(부서별 가시화) -> Chargeback(내부 과금) -> Unit Economics(거래당 비용, ex: 1Tx당 ₩0.32). AWS Cost Explorer·Azure Cost Management·K8s Vertical Pod Autoscaler 활용. |
| **BSC(Balanced Scorecard)** | 전략 4관점 성과 측정 | 재무(ROI·NPV·TCO) / 고객(NPS·CSAT·SLI) / 내부 프로세스(배포리드타임·MTTR·변경실패율) / 학습성장(핵심인재 유지율·교육이수시간). **Strategy Map**으로 인과관계 도식화. |

### 핵심 알고리즘·수식·파라미터

- **NPV(순현재가치)**: NPV = Σ<sub>t=1..n</sub> (CF<sub>t</sub> / (1+r)<sup>t</sup>) − CapEx, r=할인율(보통 WACC 7~10%). **NPV > 0**일 때 투자 적격.
- **IRR(내부수익률)**: NPV=0이 되는 r. IRR > Hurdle Rate(통상 12%) 시 채택.
- **TCO(Total Cost of Ownership)**: TCO = CapEx(서버·SW·라이선스) + OpEx(전력·인건비·교육·유지보수) + Risk Cost(장애·보안) − Residual Value. 통상 5년 TCO에서 **클라우드가 27% 저렴**(Flexera 2024).
- **EV/EA(Enterprise Value / EA)**: EA 도입 후 기업가치 변화, 통상 1.7~2.4배.
- **CMMI(능력성숙도) 5단계**: Initial(1) -> Managed(2) -> Defined(3) -> Quantitatively Managed(4) -> Optimizing(5).
- **COBIT 2019 능력 6단계**: 0(Incomplete) -> 1(Initial) -> 2(Managed)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 741 / 800

<- **이전**: [740. IT 경영 관리 핵심 토픽 740번 시험 요약](/studynote/12_it_management/05_security_compliance/740_it_management_core_topic_740_exam_summary/)
**다음**: [742. IT 경영 관리 핵심 토픽 742번 시험 요약](/studynote/12_it_management/05_security_compliance/742_it_management_core_topic_742_exam_summary/) ->

---
