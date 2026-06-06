---
title: "IT Management Core Topic 719 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019의 40개 Govern/Manage 목적과 ITIL 4의 Service Value System을 기반으로, IT 투자-전략-운영-리스크를 하나의 가치 사슬(Value Chain)로 통합하여 비즈니스 outcomes를 최대화하는 체계이며, ISO/IEC 38500의 6대 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)이 의사결정 평가의 근간이다.
> 2. **가치**: 성숙도 Level 3->5 도달 시 IT 투자 ROI 20~35% 향상, Shadow IT 비율 30%->7% 감소, MTTR(평균 복구시간) 4시간->17분 단축, Time-to-Market 40% 단축, ISMS-P/ISO 27001 인증 갱신 시 non-conformity 80% 감소의 정량 효과를 거둘 수 있다.
> 3. **판단 포인트**: 중앙집중(CoE) vs 분산(Federated) 거버넌스, Build-vs-Run 비율(통상 30:70), CoBIT Design Factors 11개 항목의 가중치 결정, 그리고 클라우드·AI 도입 시 RACI 매트릭스 재설계가 핵심 트레이드오프이며, 조직 성숙도(CMMI Level)와 규제 강도(ISMS-P, DORA, AI Basic Act)가 아키텍처 선택을 좌우한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환 가속화로 전 세계 IT 지출이 2024년 5조 USD를 돌파했지만, McKinsey 조사에 따르면 전체 디지털 이니셔티브 중 **70%만이 비즈니스 가치를 창출**하고 있으며, 나머지 30%는 성과 부진으로 중단된다. 한국정보화진흥원의 2023년 ICT 실태조사에서도 국내 기업의 **43%가 IT-Business Alignment 부재**를 1순위 경영 과제로 응답했다. 이러한 맥락에서 "719번 시험"은 정보관리기술사·컴퓨터시스템응용기술사 시험에서 빈출하는 IT 경영 관리 핵심 토픽 — IT 거버넌스, IT 전략 기획, IT 투자 평가, IT 서비스 관리, 정보보안 거버넌스, 엔터프라이즈 아키텍처, IT 위험·컴플라이언스, BCM/DR — 을 하나의 프레임워크로 통합한 종합 응용 문제이다.

핵심 배경 문제는 ① Shadow IT(Gartner: 전체 SaaS 지출의 30~40%가 비승인), ② IT-Business 정렬도 저하(Luftman의 Strategic Alignment Model 5단계 중 평균 2.3), ③ 레거시 시스템 유지보수비가 전체 IT 예산의 **60% 이상** 점유, ④ 공급망-랜섬웨어-내부자 위협의 3중 리스크, ⑤ ESG·개인정보보호법·AI기본법 등 규제 강화로 요약된다. 전통적 "기술 중심 IT 관리"에서는 인프라·애플리케이션 단위로 사일로(Silo)별 관리가 이루어졌으나, 현대 패러다임은 **"가치 중심(Value-Driven) IT 관리"**로, 모든 IT 의사결정을 비즈니스 outcome과 risk-adjusted return 기준으로 정렬한다.

```text
    +------------------------------------------------------------------+
    |             IT 경영 관리 3층 통합 거버넌스 피라미드               |
    +------------------------------------------------------------------+
                              ^
                             ╱ ╲
                            ╱   ╲
                           ╱ GOV ╲        <- 최상위: 거버넌스(Govern)
                          ╱ 战略  ╲         - 이사회/IT Steering Committee
                         ╱---------╲        - COBIT 2019 EDM(Domain)
                        ╱   MGMT    ╲      <- 중간: 관리(Manage)
                       ╱   价值链    ╲      - PMO, EA, ITSM, CISO Office
                      ╱---------------╲     - PBRM, R&R, KPI/KRI 대시보드
                     ╱    OPERATE     ╲   <- 최하위: 운영(Operate)
                    ╱     技术执行      ╲    - SRE, DevSecOps, AIOps
                   ╱---------------------╲  - SLM/SLM(SLA 99.99%)
                  vvvvvvvvvvvvvvvvvvvvvvvv
              +------------------------------------+
              |  IT 성과 측정 (BSC 4관점)           |
              |  ① 재무(F)  ② 고객(C)              |
              |  ③ 내부 프로세스(IP)  ④ 학습·성장(LG)|
              +------------------------------------+
                              <-> 양방향 피드백
              +------------------------------------+
              |  외부 환경: 규제(개인정보보호법,     |
              |  ISMS-P, DORA, EU AI Act)·시장·경쟁 |
              +------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 종합 관제탑"**과 같다. 위성·드론·교통·소방·치안의 5개 기관이 각각 움직이면 도시가 마비되듯, 거버넌스-관리-운영의 3층이 하나의 관제탑에서 통합 조율되어야 시민(비즈니스)에게 가치를 줄 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 아키텍처는 국제 표준(COBIT 2019, ITIL 4, ISO 38500/27001/20000)과 산업 베스트프랙티스(TOGAF, PMBOK 7, Balanced Scorecard)를 4계층으로 통합한 것이다. **Layer 1(Strategic)**: 거버넌스 위원회, **Layer 2(Tactical)**: 프로세스/프로그램, **Layer 3(Operational)**: 서비스/프로젝트, **Layer 4(Technical)**: 인프라/플랫폼. 각 계층 간 의사소통은 RACI 매트릭스, OKR, KPI 대시보드, 그리고 IT Steering Committee 월례 회의로 이루어진다.

COBIT 2019의 핵심은 **Governance System**과 **Management System**의 분리이다. Governance(EDM: Evaluate/Direct/Monitor)는 이사회·경영진의 책임이며 5개 도메인(프레임워크 정렬, 가치 전달, 위험 최적화, 자원 최적화, 투명성 확보)을 다룬다. Management(Align/Plan/Organize: APO, Build/Acquire/Implement: BAI, Deliver/Service/Support: DSS, Monitor/Evaluate/ME: MEA)는 4개 도메인 32개 프로세스로 구성된다. ITIL 4의 **Service Value System(SVS)**은 Opportunity/Demand -> Value -> Guiding Principles(7개: Focus on value, Start where you are, Progress iteratively, etc.) -> Governance -> Practices(34개) -> Continual Improvement의 선순환 구조다. ISO 38500은 6대 거버넌스 원칙을 통해 모든 IT 의사결정을 평가하는 체크리스트를 제공한다.

```text
    +--------------------------------------------------------------+
    |  COBIT 2019 × ITIL 4 × ISO 38500 통합 의사결정 흐름도         |
    +--------------------------------------------------------------+

    [이사회] --► Evaluate --► Principles: 책임·전략·획득·성과·준법·인간
         |             ^
         |             | Monitor(KPI 대시보드)
         v             |
    [Direct] --► RACI -+
         |
         v
    +------------------------------------------------+
    |  IT 전략 기획 (Ward & Peppard IS/IT 전략 5단계) |
    |  ① IS 환경 분석 -> ② 비즈니스 전략 -> ③ IS 전략   |
    |  ④ IT 전략 -> ⑤ 전략 실행 및 평가               |
    +------------------------------------------------+
         |         |         |         |
         v         v         v         v
    +--------+ +--------+ +--------+ +--------+
    | APO    | | BAI    | | DSS    | | MEA    |
    | 14 proc| | 11 proc| | 6 proc | | 4 proc |
    +---+----+ +---+----+ +---+----+ +----+---+
        |          |          |           |
        +----------+----------+-----------+
                       v
    +--------------------------------------------+
    |  ITIL 4 Service Value Chain (6개 활동)     |
    |  Plan->Improve->Engage->Design&Transition     |
    |  ->Obtain/Build->Deliver&Support             |
    +--------------------------------------------+
                       v
    +--------------------------------------------+
    |  운영 계층: DevSecOps, SRE, AIOps, FinOps   |
    |  - DORA 4대 지표(배포빈도, 리드타임, MTTR,  |
    |    변경실패율) - SLI/SLO/SLA 99.99%        |
    +--------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee** | 거버넌스 의사결정 정점 | CIO·CDO·CISO·이사로 구성, 월 1회 Cadence, RACI에서 'A'(Accountable), 의사결정 사항 중 80%가 예산·우선순위·위험 승인이며,議事錄은 ISO 38500 Principle 1(Responsibility) 증거물 |
| **PMO(Project Management Office)** | 전략-실행 연결 | P3M3(Portfolio/Programme/Project Management Maturity) 5단계, PBRM(Portfolio/Business Relationship Management) 통해 비즈니스-프로젝트 정렬, OKR 4-Quarter Cascade, EVM(Earned Value Management) CPI>1, SPI>1 유지 |
| **EA(Enterprise Architecture)** | 표준화·복잡도 관리 | TOGAF ADM 8단계 Phase B-F, ArchiMate 3.2 27개 요소(Active Structure, Behavior, Passive Structure), Zachman Framework 6×6 매트릭스, EA 도구(LeanIX, MEGA HOPEX, BizzDesign) 활용 Application Portfolio Rationalization |
| **ITSM(Global Service Desk)** | 서비스 운영·사용자 경험 | ITIL 4 34개 Practice 중 9개 핵심(Practice: Incident, Problem, Change Enablement, Service Desk, Service Level, Continual Improvement, Service Request, Monitoring & Event, Release Mgmt), CMDB 기반 Configuration Item 추적, KEDB(Known Error DB) 운영 |
| **CISO Office(정보보안 거버넌스)** | 사이버 리스크 통합 관리 | ISO 27001:2022 Annex A 93개 통제(4개 그룹: Organizational 37, People 8, Physical 14, Technological 34), ISMS-P 인증 11개 영역 102개 통제, K-ISMS-P, Zero Trust Architecture(SDP, MFA, mTLS), GRC(Governance-Risk-Compliance) 플랫폼 |

핵심 알고리즘 및 의사결정 공식:
- **Total Economic Impact(TEI)**: TCO(직접·간접·고용 기회비용) + NPV(Net Present Value, 할인율 8~12%) + Risk-Adjusted ROI
- **IT BSC 목표 설정**: 재무관점(ROA 15%, Cost/Revenue 3%) -> 고객관점(CSAT 4.2/5, NPS 30+) -> 내부(IPR: Process Efficiency Index, First Call Resolution 75%+) -> 학습/성장(IT 인력 기술 매트릭스 갭 20%v)
-
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 719 / 800

<- **이전**: [718. IT 경영 관리 핵심 토픽 718번 시험 요약](/studynote/12_it_management/05_security_compliance/718_it_management_core_topic_718_exam_summary/)
**다음**: [720. IT 경영 관리 핵심 토픽 720번 시험 요약](/studynote/12_it_management/05_security_compliance/720_it_management_core_topic_720_exam_summary/) ->

---
