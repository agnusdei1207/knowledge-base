---
title: "IT Management Core Topic 643 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **ISO 38500 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**을 거버넌스 최상위 계층으로, **COBIT 2019의 40개 Govern/Manage 목적**을 중간 통제 계층으로, **ITIL 4의 34개 Practices**를 운영 실행 계층으로 삼는 3계층 정렬(Three-Layer Alignment) 모델이며, 궁극적으로는 **Strategy->Portfolio->Program->Project->Operation**의 가치 사슬(Value Chain)을 통해 Business Outcome을 창출하는 것이다.
> 2. **가치**: Gartner 2024 보고 기준,成熟的 IT 거버넌스 체계 도입 기업은 **IT 투자 수익률(ROIT) 23% 향상**, **프로젝트 실패율 41%->12% 감소**, **Shadow IT 비용 35% 절감**, **Time-to-Market 40% 단축**의 정량적 효과를 달성하며, 정보화 사업의 **NPV(순현재가치) 기준 의사결정 정확도**를 60%에서 92%로 끌어올린다.
> 3. **판단 포인트**: 중앙집중(Centralized)·강한 통제형 거버넌스 vs 분산형·연방형(Federated) 거버넌스, **Build(자체개발) vs Buy(패키지) vs Borrow(클라우드/SaaS) vs Bridge(하이브리드)**의 4B 의사결정, **듀얼 IT 운영(쌍둥이 전략)**, 그리고 **정보화 사업 평가** 시 TCO 5개년 vs 7개년 산정, **할인율(WACC) 8-12% 적용** 여부, **Risk-Adjusted ROI** 산정 방식(Deterministic vs Monte Carlo) 선택이 기술사의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명·生成AI·클라우드 네이티브 환경으로 전환되면서 IT는 단순 지원(Back-office) 기능을 넘어 **사업의 핵심 동력(Core Business Driver)**으로 재편되었다. 2024년 Gartner CIO Survey에 따르면 글로벌 CEO의 **89%**가 "IT가 사업의 성패를 가른다"고 답변했으며, 한국 정보화진흥원의 '2024 국가정보화 실태조사'에서는 국내 500대 기업의 **73%**가 "DX(Digital Transformation) 전략과 IT 거버넌스 체계 간 정렬이 미흡하여 사업 성과 창출에 한계가 있다"고 응답했다. 이러한背景下, IT 경영 관리의 핵심은 다음 4가지 패러다임 전환을 반영해야 한다.

**① 통제 중심 -> 가치 중심**: 과거 IT 거버넌스는 SOX Act, 개인정보보호법 등 컴플라이언스 통제 강조였으나, 현재는 **Benefits Realization(성과 실현)**, **Risk Optimization(위험 최적화)**, **Resource Optimization(자원 최적화)**의 3대 밸런스 스코어(COBIT 2019 Enterprise Goals 기반)로 전환되었다.

**② IT 단독 -> 비즈니스-IT 융합(Bi-Modal IT -> Bimodal -> Fusion IT)**: Gartner의 Bimodal IT(2014)는 Mode 1(안정·예측 가능)과 Mode 2(실험·민첩)를 병행하는 '쌍둥이' 모델이었으나, 2020년 이후로는 **Fused Enterprise** 개념으로 수렴, 하나의 조직 안에서 **Stable(75%) + Exploratory(15%) + High-Risk Disruptive(10%)** 비율의 포트폴리오 밸런싱으로 진화했다.

**③ 프로젝트 -> 포트폴리오·제품 중심**: 전통적 프로젝트 단위 관리(PMBOK 6th·7th)로는 디지털 시대의 잦은 변경·실험·실패를 흡수할 수 없어, **SAFe(Scaled Agile Framework)**, **Spotify Model**, **Product-centric Operating Model**로 전환, **IT Portfolio Management(PPM)** 도구로 **Planview, ServiceNow SPM, Clarity PPM** 등을 활용해 **전략->포트폴리오->프로그램->프로젝트->제품**의 연쇄 정렬을 관리한다.

**④ 성과 측정 단일 지표 -> 다차원 BSC + OKR**: 전통 ROI, NPV 단일 측정에서 벗어나 **Kaplan-Norton Balanced Scorecard(BSC)의 4관점(Financial, Customer, Internal Process, Learning & Growth)**과 **Andy Grove(Intel)의 OKR(Objective & Key Results)**을 결합, IT 성과 측정의 다차원화·연결화·실시간화가 요구된다.

```text
        +-------------------------------------------------------------+
        |         IT 경영 관리의 4계층 참조 모델(4-Layer Reference)      |
        +-------------------------------------------------------------+
                ^          ^          ^          ^
                |          |          |          |
        +-------+--+ +-----+----+ +---+----+ +---+----------+
        |Governance| | Strategy  | |Portfolio| |Delivery/    |
        | 거버넌스  | |  전략     | | 포트폴리오| |Operation     |
        |  (What)  | |  (Why)   | |  (How)  | |  (Run/Change)|
        +----+-----+ +----+-----+ +----+----+ +------+-------+
             |            |            |             |
   +---------+--+  +------+-----+ +----+------+ +----+----------+
   |ISO 38500   |  |TOGAF 10    | |PPM Tool   | |SAFe / DevOps  |
   |COBIT 2019  |  |Zachman     | |Planview   | |ITIL 4 Service |
   |(Board-Level|  |Capability  | |Clarity    | |Value Chain    |
   | Decisions) |  |Map v3.2    | |ADO/ Jira  | |Site Reliability|
   +------------+  +------------+ +-----------+ +---------------+
             |            |            |             |
             +------------+------------+-------------+
                                |
                       +--------+--------+
                       | Business Outcome |
                       | Value Realization|
                       +-----------------+
```

**📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같다. 지휘자는 악기(프로젝트·운영 조직)·악보(전략·정책)·연주자(임직원)·청중(사업·고객) 사이의 정렬을 만들어내며, 이 정렬이 깨지면 화성 없는 소음만 남게 된다. 643번 시험은 바로 이 "정렬의 기술"을 묻는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **COBIT 2019 Governance/Management Objectives(40개)**를 축으로, **상위 ISO 38500 거버넌스 원칙**, **하위 ITIL 4 Service Value Chain(SVC)**, **측면 BSC·OKR**이 횡으로 연결되는 **3-Layer × Cross-Cut** 구조로 이해해야 한다.

### 1) ISO 38500:2015 6원칙 (최상위 거버넌스 계층)
국제표준화기구(ISO)가 2008년 제정, 2015년 개정한 **IT 거버넌스 국제 표준**으로, 이사회·경영진이 IT 활용을 **지시·감독·통제**하는 3과업을 수행할 때 따라야 할 6대 원칙을 명시한다.

| 원칙 (영문) | 원칙 (국문) | 핵심 의미 | 기술사 출제 포인트 |
| :--- | :--- | :--- | :--- |
| **Responsibility** | 책임성 | IT 의사결정·행위의 책임 소재 명확화, RACI Matrix | 거버넌스 위원회(CIO·CDO·CISO·CFO·CEO) 구성 |
| **Strategy** | 전략성 | 사업 전략과 IT 전략의 정렬, Current->Target Gap 분석 | TOGAF ADM, Capability-Based Planning |
| **Acquisition** | 취득성 | 합리적·투명한 IT 투자 의사결정, Build-Buy-Borrow-Bridge | TCO·ROA·NPV·IRR, 4B 의사결정 모델 |
| **Performance** | 성능성 | IT 서비스·프로젝트 성과 측정, KPI·SLI·SLO | BSC 4관점, OKR, DevOps 4 DORA metrics |
| **Conformance** | 준거성 | 내부 규정·외부 법규(개인정보보호법, ISMS-P, PCI-DSS) 준수 | Control Objectives, Regulatory Compliance |
| **Human Behavior** | 인간행태 | IT 활용 문화·윤리·변화관리, ADKAR·Kotter 8단계 | Digital Culture, Shadow IT, Shadow AI |

### 2) COBIT 2019 40개 거버넌스/관리 목적 (중간 통제 계층)
**ISACA**의 COBIT(Control Objectives for Information and Related Technologies)은 2019년 개정을 통해 **40개의 Governance Objectives(EDM: Evaluate, Direct, Monitor 5개)**와 **35개의 Management Objectives(APO: Align Plan Organize 14, BAI: Build Acquire Implement 11, DSS: Deliver Service Support 6, MEA: Monitor Evaluate Assess 4)**으로 구성된다. 이때 핵심은 5개 EDM(거버넌스) 체계가 35개 Management Objective를 **원인-결과(Goal Cascade)** 구조로 연결한다는 점이다.

```text
                COBIT 2019 Goal Cascade (Enterprise -> IT -> Component)
                ----------------------------------------------------
    +--------------------------------------------------------------+
    |  13 Enterprise Goals (EG)                                     |
    |  +- EG01 포트폴리오 경쟁력  +- EG08 내부 통제 최적화           |
    |  +- EG02 비용 효율성        +- EG09 정보 기반 의사결정         |
    |  +- EG03 직원 역량·행태     +- EG10 인력·자원 최적화           |
    |  +- EG04 문화·윤리          +- EG11 컴플라이언스               |
    |  +- EG05 재무 투명성        +- EG12 외부 규제 준수             |
    |  +- EG06 서비스 품질        +- EG13 보안·프라이버시            |
    |  +- EG07 보안·프라이버시                                        |
    +----------------------+---------------------------------------+
                           |  (Mapping: Primary/Secondary)
                           v
    +--------------------------------------------------------------+
    |  13 IT-related Goals (ITG)                                    |
    |  ITG01 IT와의 정렬           ITG08 외부관계 관리              |
    |  ITG02 IT 거버넌스·관리 체계 ITG09 정보·인프라 최적화         |
    |  ITG03 비즈니스 의사결정 지원 ITG10 인력·역량 관리            |
    |  ITG04 리스크 관리            ITG11 변화·혁신 지원             |
    |  ITG05 이해관계자 가치 실현   ITG12 안전한 운영·실행           |
    |  ITG06 서비스·제품 역량       ITG13 지식·정보 관리            |
    |  ITG07 보안·프라이버시                                          |
    +----------------------+---------------------------------------+
                           |
                           v
    +--------------------------------------------------------------+
    |  40 Governance/Management Objectives                          |
    |  EDM(5)  +  APO(14) + BAI(11) + DSS(6) + MEA(4)              |
    |                                                              |
    |  EDM01 거버넌스 체계 수립     EDM05 이해관계자 참여 보장      |
    |  EDM02 이익 실현              APO01 관리 프레임워크           |
    |  EDM03 리스크 최적화          APO02 전략                      |
    |  EDM04 자원 최적화            ... (총 40개)                   |
    +--------------------------------------------------------------+
                           |
                           v
    +--------------------------------------------------------------+
    |  7 Component of Governance System (Components)                |
    |  ① 프로세스  ② 정보  ③ 구조(조직)  ④ 사람·역량·기술          |
    |  ⑤ 정책·원칙  ⑥ 문화·윤리·행태  ⑦ 서비스·인프라·애플리케이션 |
    +--------------------------------------------------------------+
```

### 3
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 643 / 800

<- **이전**: [642. IT 경영 관리 핵심 토픽 642번 시험 요약](/studynote/12_it_management/05_security_compliance/642_it_management_core_topic_642_exam_summary/)
**다음**: [644. IT 경영 관리 핵심 토픽 644번 시험 요약](/studynote/12_it_management/05_security_compliance/644_it_management_core_topic_644_exam_summary/) ->

---
