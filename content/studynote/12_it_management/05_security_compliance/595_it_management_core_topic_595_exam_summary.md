---
title: "595. IT 경영 관리 핵심 토픽 595번 시험 요약 (IT Management Core Topic 595 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 5개 도메인(EDM·APO·BAI·DSS·MEA), ISO/IEC 38500의 6대 원칙, RACI 매트릭스를 기반으로 IT 의사결정 권한·책임·통제 구조를 설계하여 Business-IT Alignment(전략적 정렬)와 Value Delivery(가치 전달)를 보장하는 경영 체계이다.
> 2. **가치**: ISACA·McKinsey·Gartner의 실증 연구에서 효과적인 IT 거버넌스 도입 시 IT 투자 ROI가 평균 28~42% 향상, 프로젝트 실패율 20~35% 감소, Time-to-Market 25% 단축, IT 운영 비용 15~30% 절감 효과가 보고되며, SOX·GDPR·개인정보보호법 등 컴플라이언스 위반 리스크를 사전에 차단한다.
> 3. **판단 포인트**: Centralized(집중형·CoE 모델)와 Federated(분산형·Business-embedded 모델) 사이의 의사결정 속도-통제 강도 트레이드오프, One-size-fits-all 프레임워크 적용 vs 조직 성숙도(CMMI·OPM3) 기반의 Tailored Governance 설계, 그리고 Agile·DevOps 환경에서 거버넌스의 경량화(Light-weight Governance)와 자동화(Continuous Controls Monitoring) 수준의 균형점이 핵심 판단 축이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화로 IT는 단순 비용 센터(Cost Center)에서 비즈니스 가치 창출의 핵심 동력(Value Driver)으로 전환되었다. 그러나 2023년 Gartner 조사에 따르면 글로벌 기업의 65%가 IT-Business Misalignment를 경험하고 있으며, CIO가 제시한 이니셔티브 중 44%만 CEO의 비즈니스 우선순위와 일치하는 것으로 나타났다. 이러한 문제를 해결하기 위해 등장한 IT 거버넌스(IT Governance)는 단순한 IT 관리 체계를 넘어 **"Board-level 의사결정 구조"**로 자리 잡았으며, SOX(Sarbanes-Oxley Act §404), Basel III, GDPR, 한국 개인정보보호법, 전자금융거래법 등 규제 요구사항의 컴플라이언스 제고와 ESG 경영의 G(Governance) 항목 평가에서도 필수 요소로 부상했다.

전통적 IT 관리(1990~2000년대)는 CIO 산하의 IT 부서가 **기술 중심(Silo, Tech-driven)**으로 시스템을 구축·운영했고, ROI 측정이 어려워 "Black Hole"이라는 비판을 받았다. 그러나 2000년대 중반 이후 COBIT 4.0(2005) -> COBIT 5(2012) -> COBIT 2019(2018) 프레임워크의 발전과 함께 **가치 중심(Value-driven), 원칙 기반(Principle-based), 목표 연동(Goals-cascade)** 거버넌스 패러다임으로 전환되었으며, 최근에는 AI 거버넌스, Algorithmic Accountability, Data Governance(데이터 거버넌스)의 결합으로 진화 중이다.

```text
   +--------------------------------------------------------------+
   |                Board of Directors / 이사회                    |
   |      (전략적 의사결정 · Risk Appetite · Value Optimization)   |
   +--------------------------+-----------------------------------+
                              |  EDM( Evaluate, Direct, Monitor )
                              v
   +--------------------------------------------------------------+
   |   IT Steering Committee / IT 전략위원회                       |
   |  (CFO·CIO·CDO·COO·사업본부장) - 월 1회 거버넌스 리뷰          |
   +--------------------------+-----------------------------------+
                              |
              +---------------+---------------+
              v               v               v
   +-----------------+ +--------------+ +-----------------+
   | Business Unit A | | Business Unit| | IT / Platform    |
   | (Demand Owner)  | | B (Demand)   | | (Supply Owner)  |
   |  <-> Engagement   | |              | |  <-> Architecture |
   +-----------------+ +--------------+ +-----------------+
              |               |               |
              +---------------+---------------+
                              |
                              v
   +--------------------------------------------------------------+
   |  Delivery Layer: Agile Squads · DevOps · SRE · ITSM          |
   |  (BAI-DSS)              (MEA - Monitor, Evaluate, Assess)    |
   +--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스는 **"도시의 종합 교통 체계"**와 같다. 도로(인프라), 신호등(정책), 경찰(통제), 시민(사용자)이 각자 역할을 가지며, 도시계획 위원회(거버넌스 위원회)가 도시 전체의 흐름을 조율한다. 도로만 잘 닦아서는(기술만 도입) 교통 정체(misalignment)를 해결할 수 없듯, 의사결정 구조와 책임 체계가 함께 설계되어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 5개 도메인 및 40개 관리 목표(Management Objective)

COBIT 2019는 **Governance Objectives(EDM 5개)** + **Management Objectives(APO·BAI·DSS·MEA 35개)**로 구성되며, **Goals Cascade(목표 연쇄)** 메커니즘을 통해 Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Objectives로 변환된다.

```text
   +------------------------------------------------------------+
   |  Stakeholder Needs (이해관계자 요구)                        |
   |  - Benefits Realization · Risk Optimization · Cost        |
   |  - Resource Optimization · Compliance · Innovation        |
   +-------------------------+----------------------------------+
                             |  Step 1: Cascade
                             v
   +------------------------------------------------------------+
   |  Enterprise Goals (13개) - e.g., EG01 Portfolio of         |
   |  competitive I&T-enabled investments, EG08 Optimization    |
   +-------------------------+----------------------------------+
                             |  Step 2: Map
                             v
   +------------------------------------------------------------+
   |  Alignment Goals (13개) - AG01 I&T compliance & support   |
   |  for business compliance, AG04 Managed I&T-related risks  |
   +-------------------------+----------------------------------+
                             |  Step 3: Cascade
                             v
   +------------------------------------------------------------+
   |  Management Objectives (40개) - e.g., APO12 Managed Risk, |
   |  DSS02 Managed Service Requests & Incidents, BAI03        |
   |  Managed Solutions (incl. Architecture)                   |
   +------------------------------------------------------------+
                             |
                             v
                +----------------------------+
                |  Components: 7 categories  |
                |  (Principles·Policies·Frame|
                |  works·Processes·Org Struc|
                |  ture·People·Culture·Info  |
                |  &Services·Infrastructure)|
                +----------------------------+
```

### 2. ISO/IEC 38500 IT 거버넌스 6대 원칙

| 원칙 | 영문 명 | 핵심 내용 | 실무 적용 예시 |
| :--- | :--- | :--- | :--- |
| ① 책임 | Responsibility | 이사회가 IT 활용에 대한 최종 책임을 진다 | CIO가 이사회에 분기별 IT 성과 보고 |
| ② 전략 | Strategy | 조직의 전략 목표와 IT 전략 정렬 | ISP(정보화전략계획) 수립·갱신 주기 3년 |
| ③ 획득 | Acquisition | IT 투자 의사결정의 투명성·합리성 | CAPEX·OPEX 투자심의위원회(PAC) 운영 |
| ④ 성과 | Performance | IT 서비스가 약속된 성과(SLA) 제공 | SLA 99.95% 가용성, MTTR < 30분 |
| ⑤ 적합 | Conformance | 법적·규제 요구사항 준수 | 개인정보 영향평가, ISMS-P 인증 |
| ⑥ 인간행태 | Human Behavior | IT가 사람·문화·윤리에 미치는 영향 | AI 윤리위원회, Digital Ethics Policy |

### 3. RACI 매트릭스 및 Three Lines of Defense

```text
        Request    Decide    Consult    Inform
   CIO     R         A          C         -
   CFO     C          I         C        A (비용)
   CPO     C          I         C        A (아키텍처)
   CEO    A(전략)    A(최종)     I        C
   BISO   C(리스크)   I         C        A
   Audit  I         I          -        A(독립)
```

| 라인 | 역할 | 구성원 | 책임 |
| :--- | :--- | :--- | :--- |
| 1st Line | Operational Management | 현업·IT 운영팀 | 위험 식별·통제 수행 (자기통제) |
| 2nd Line | Risk Management & Compliance | CRO·CISO·컴플라이언스 | 정책·표준 수립, 모니터링 |
| 3rd Line | Independent Assurance | 내부감사·외부감사 | 1·2nd Line의 효과성 독립 검증 |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회(IT Committee)** | 거버넌스 최종 의사결정 | 전략적 IT 투자·리스크 승인, 분기별 KPI 리뷰(BSC 4관점) |
| **CIO / CDO** | 거버넌스 실행 책임자 | IT Strategy 수립, Portfolio Prioritization(Wsjf·RICE), Architectural Decision Record(ADR) 관리 |
| **CoE(Center of Excellence)** | 표준·방법론 정립 | DevOps, Cloud, Data 거버넌스 표준화, Inner Source 정책 |
| **PMO(Project Mgmt Office)** | 프로젝트 통제·품질 보증 | P3O 모델 적용, Stage-Gate 프로세스, Earned Value Management(EVM) |
| **GRC Platform** | 통합 거버넌스·리스크·컴플라이언스 | Archer·ServiceNow GRC·SAP GRC, RPA 기반 Continuous Controls Monitoring(CCM) |
| **EA(Enterprise Architecture)** | 아키텍처 정합성·표준화 | TOGAF ADM, ArchiMate 3.2, 용어 표준(ISO 11179 Metadata Registry) |
| **CISO / BISO** | 사이버 보안 거버넌스 | NIST CSF 2.0(Identify·Protect·Detect·Respond·Recover·Govern), Zero Trust Architecture |

### 4. 핵심 알고리즘·수식·평가 모델

**① IT 거버넌스 성숙도 평가 (CMMI 기반 5단계)**

| 레벨 | 명칭 | 핵심 특징 | 거버넌스 역량 |
| :--- | :--- | :--- | :--- |
| L1 | Initial | 의존적·비정형·Heroic | 거버넌스 부재, 부서별 독자 운영 |
| L2 | Managed | 프로젝트 단위 통제 | PMO 운영, 기본 RACI 정의 |
| L3 | Defined | 조직 표준·프로세스 정형화 | COBIT·ITIL 표준 채택, KPI 체계 수립 |
| L4 | Quantitatively Managed | 데이터 기반 의사결정 | 통계적 프로세스 관리(SPC), EVM 정착 |
| L5 | Optimizing | 지속적 개선·혁신 | Continuous Improvement(Kaizen), 예측형 분석 |

**② IT 투자 우선순위 결정 모델 (WSJF - Weighted Shortest Job First, SAFe)**
$$
WSJF = \frac{Cost\ of\ Delay\ (CoD)}{Job\ Duration}
$$
$$
CoD = User\ Business\ Value + Time\ Criticality + Risk\ Reduction\ (or\ Opportunity\ Enablement)
$$

**③ IT 포트폴리오 건강도
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 595 / 800

<- **이전**: [594. IT 경영 관리 핵심 토픽 594번 시험 요약](/studynote/12_it_management/05_security_compliance/594_it_management_core_topic_594_exam_summary/)
**다음**: [596. IT 경영 관리 핵심 토픽 596번 시험 요약](/studynote/12_it_management/05_security_compliance/596_it_management_core_topic_596_exam_summary/) ->

---
