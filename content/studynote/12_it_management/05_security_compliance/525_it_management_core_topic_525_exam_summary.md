+++
title = "525. IT 경영 관리 핵심 토픽 525번 시험 요약 (IT Management Core Topic 525 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019의 40개 거버넌스/관리 목표, ITIL 4의 34개 실무 관행, PMBOK 7th의 12개 원칙, TOGAF 10의 ADM(Architecture Development Method) 사이클을 통합적으로 운용하여, 기업의 전략-아키텍처-프로젝트-서비스-보안 5계층의 정렬(Strategic Alignment)을 달성하는 경영 시스템이다.
> 2. **가치**: McKinsey & Company 연구에 따르면 효과적인 IT 거버넌스 구축 시 IT 투자 ROI가 30~50% 개선되고, Gartner는 통합 IT 운영 모델 적용 시 운영 비용(OpEx)을 평균 23% 절감, IDC는 디지털 전환 성공률이 38%(2020년)에서 73%(2026년)로 약 2배 증가할 것으로 예측한다.
> 3. **판단 포인트**: 중앙집중식(Centralized) vs 분산형(Decentralized) vs 하이브리드(Federated) IT 운영 모델 선택, 전통적 Waterfall-Plan 기반(COBIT 2019 Cascade Goals) vs Agile-Safe 기반(쪼개고 연결하기) 거버넌스 도입 여부, 그리고 KPI 측정을 위한 BSC(균형성과표) 4관점(재무/고객/내부프로세스/학습성장)과 OKR(Objectives and Key Results) 중 조직 문화에 맞는 측정 체계 선택이 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX, Digital Transformation)이 가속화되면서, 단순한 시스템 구축을 넘어 IT가 기업의 경쟁력과 생존을 좌우하는 핵심 동력으로 부상했다. 그러나 한국정보화진흥원이 발간한 「2024 디지털 전환 실태조사」에 따르면 국내 기업의 67.4%가 "DX 추진을 위한 IT 거버넌스 체계 미비"를 1차 장애물로 지목했다. 이는 프로젝트 단위의 일회성 투자와 부서별 사일로(Silo) 운영, IT 부서와 사업부서 간의 목표 불일치(Alignment Gap) 때문이다.

특히 2020년 코로나19 팬데믹 이후, 재택근무·클라우드 전환·공급망 다변화 등 **VUCA(Volatility, Uncertainty, Complexity, Ambiguity)** 환경에서 IT 리더는 CFO·CEO·이사회로부터 "IT가 비즈니스 가치를 어떻게 만들어내는가?"라는 정량적 답변을 요구받고 있다. 이때 단순 비용 센터(Cost Center) 관점에서 벗어나, **IT를 가치 창출 센터(Value Center) 또는 전략 자산(Strategic Asset)**으로 전환하는 것이 핵심 과제로 대두된다.

기술사 시험에서는 IT 경영 관리를 단순한 ITIL 운영 관리 차원이 아닌, **전략적 거버넌스 -> 아키텍처 -> 프로젝트/서비스 -> 보안/리스크**라는 4계층 프레임워크의 통합 설계 문제로 접근한다. 2023~2024년 출제 경향을 분석하면 COBIT 2019의 거버넌스 시스템 컴포넌트(Governance System Components, 5개 도메인·40개 목표), ISO/IEC 38500:2015의 6개 거버넌스 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior), 그리고 한국 클라우드 컴퓨팅 산업의 급성장으로 인한 **FinOps(Financial Operations)** 도입 사례가 빈번히 출제되고 있다.

```text
   +------------------------------------------------------------------+
   |      IT 경영 관리 4계층 통합 프레임워크 (IT Management Stack)      |
   +------------------------------------------------------------------+

   +--------------------------------------------------------------+
   |  1계층: IT 거버넌스 (Governance) - "무엇을/왜"                 |
   |  ----------------------------------------------------------- |
   |  · 이사회/IT거버넌스위원회 (ITGC) -> IT 전략방향 설정           |
   |  · 프레임워크: COBIT 2019, ISO 38500, KING IV                 |
   |  · 핵심 산출물: IT 전략 로드맵, 거버넌스 챔터(Charter)         |
   +------------------------+-------------------------------------+
                            | 정렬(Align)
                            v
   +--------------------------------------------------------------+
   |  2계층: EA (Enterprise Architecture) - "어떻게 설계할 것인가"   |
   |  ----------------------------------------------------------- |
   |  · 프레임워크: TOGAF 10 ADM, Zachman 6x6, FEAF/DODAF         |
   |  · 영역: BA(비즈니스), DA(데이터), AA(애플리케이션), TA(기술)   |
   |  · 핵심 산출물: 아키텍처 비전, To-Be 모델, 마이그레이션 플랜    |
   +------------------------+-------------------------------------+
                            | 실행
                            v
   +--------------------------------------------------------------+
   |  3계층: 프로젝트/서비스 실행 (Delivery & Operation) - "만들고/운영"|
   |  ----------------------------------------------------------- |
   |  · PM: PMBOK 7th(원칙), PRINCE2, SAFe 6.0                   |
   |  · SM: ITIL 4(34 Practice), DevOps, SRE, AIOps              |
   |  · 핵심 산출물: 서비스 카탈로그, SLA, 릴리스 노트, 런북        |
   +------------------------+-------------------------------------+
                            | 통제/보안
                            v
   +--------------------------------------------------------------+
   |  4계층: 리스크/보안/컴플라이언스 (Risk/Security/Compliance)     |
   |  ----------------------------------------------------------- |
   |  · 거버넌스: ISO 27001(ISMS), ISO 27701(개인정보), ISO 31000 |
   |  · 컴플라이언스: GDPR, 한국 개인정보보호법, PCI-DSS, ESG      |
   |  · 핵심 산출물: 리스크 레지스터, BCP/DRP, ISMS-P 인증서       |
   +--------------------------------------------------------------+

   -> 5대 KPI: ROI, TCO, TTM(시장진입시간), SLA 가용성(%), 보안사고 MTTR
```

**기존 vs 새로운 패러다임 비교**: 과거(2000년대 이전) IT 관리는 **기술 중심(Tech-centric)**, **프로젝트 단위 일회성(Siloed)**, **CAPEX(자본 지출)**, **내부 시스템 폐쇄형**이었다. 새로운 패러다임(2024년~)은 **가치 중심(Value-centric)**, **제품/플랫폼 지속 운영(Product/Platform)**, **OPEX(운영 지출·구독형)**, **하이퍼스케일 클라우드·API 기반 개방형**으로 전환되었다. 이러한 변화는 **"Build and Run"**에서 **"Buy/Borrow and Orchestrate"**로의 IT 리더의 역할 전환을 의미하며, 기술사 시험에서도 "수직 통합(Vertical Integration) IT 조직 vs 수평 연합(Horizontal Alliance) IT 조직"의 트레이드오프가 단골 논제다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 오케스트라의 **"지휘자(Conductor)"**와 같다. 여러 악기(시스템·프로세스·사람)를 개별 연주시키지 않고, **악보(전략)**, **파트 배치(아키텍처)**, **리허설·공연(프로젝트·운영)**, **음질 관리(보안·컴플라이언스)**를 통합 조율해 비로소 **"완성도 높은 협주곡(비즈니스 가치)"**가 만들어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"5단 정렬(5-Layer Alignment)"** 메커니즘이다. 이는 **① 비즈니스 전략 ↔ ② IT 거버넌스 ↔ ③ 아키텍처 ↔ ④ 프로젝트/서비스 ↔ ⑤ 보안/리스크** 간의 **이중 폐루프(Closed-Loop)** 피드백 체계를 통해, 계획(Plan) -> 실행(Do) -> 측정(Check) -> 개선(Act)의 **PDCA 사이클**을 다층적으로 운영함을 의미한다.

COBIT 2019의 **Cascade Goals**(연쇄 목표) 메커니즘이 이를 잘 설명한다. 13개의 엔터프라이즈 목표(예: "01 포트폴리오의 경쟁 제품·서비스 제공")가 40개의 거버넌스·관리 목표(예: "EDM02 위험 관리 보장", "BAI01 관리 시스템 유지보수")로 연쇄되고, 이는 다시 프로세스 활동·역할·기술·정보·문화 요소에 매핑된다. 이때 가장 중요한 것은 **"연쇄 시킨다"는 것은 곧 "측정 단위를 공유한다"**는 의미이며, 모든 계층이 동일한 KPI 그래프(예: 고객만족 -> 서비스 가용성 -> 시스템 MTBF -> 인프라 헬스체크)로 연결되어야 한다.

**PMBOK 7th Edition**(2021년 발표)에서는 12개 원칙(Stewardship, Team, Development Approach, Planning, Work, Delivery, Measurement, Uncertainty, Complexity, Risk, Adaptability, Change)이 8개 성과 도메인(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)와 결합하여, **원칙 기반(Principle-based) + 도메인 기반(Domain-based)**의 이원적 거버넌스 구조를 채택했다. 이는 "모든 프로젝트에 적용 가능한 단일 정답"이 아니라 "상황에 맞는 원칙 적용"을 강조한 점에서 시험의 핵심 토픽이다.

```text
   IT 경영 관리의 이중 폐루프(Double Closed-Loop) 정렬 메커니즘
   ----------------------------------------------------------

   +--------------- 외부 폐루프 (External Loop) ---------------+
   |  비즈니스 환경(고객·시장·경쟁사·규제)                       |
   |      |                                                     |
   |      v                                                     |
   |  +--------------+                                          |
   |  | Sense(인지) | <- PESTEL, SWOT, 벤치마킹, ESG            |
   |  +------+-------+                                          |
   |         v                                                  |
   |  +--------------+                                          |
   |  | Align(정렬) | <- COBIT Cascade Goals, KF Strategic Fit  |
   |  +------+-------+                                          |
   |         v                                                  |
   |  +--------------+                                          |
   |  | Decide(결정) | <- ITGC(이사회), 포트폴리오 우선순위화     |
   |  +------+-------+                                          |
   |         |  의사결정                                          |
   |         v                                                  |
   |  +--------------+                                          |
   |  | Govern(통제) | <- KPI 대시보드, BSC 4관점, OKR           |
   |  +------+-------+                                          |
   |         |  피드백 신호                                       |
   |         +----------------+                                  |
   |                          v                                  |
   |  +----------------------------------------------+           |
   |  | Adapt(적응) | <- 전략 갱신, 아키텍처 재설계     |           |
   |  +----------------------------------------------+           |
   +-------------------------------------------------------------+

   +--------------- 내부 폐루프 (Internal Loop) ---------------+
   |  +----------+    +----------+    +----------+              |
   |  | Strategy |---->|Portfolio |---->| Program  |              |
   |  +----+-----+    +----+-----+    +----+-----+              |
   |       ^              ^              v                      |
   |       |              |         +----------+                |
   |       |              |         | Project  |                |
   |       |              |         +----+-----+                |
   |       |              |              v                      |
   |       |              |         +----------+                |
   |       |              |         | Product/ |                |
   |       |              |         | Service  |                |
   |       |              |         +----+-----+                |
   |       |              |              v                      |
   |       |              |         +----------+                |
   |       |              +---------| Operation|                |
   |       |                        +----+-----+                |
   |       |                             v                      |
   |       |                        +----------+                |
   |       +------------------------| Retire/  |                |
   |                                |Improve   |                |
   |                                +----------+                |
   |  (PMBOK 7th: 원칙/도메인, ITIL 4: SVS(Value System))        |
   +-------------------------------------------------------------+

   ※ 외부 루프 = 비즈니스↔IT 정렬, 내부 루프 = IT 내부 Value Chain
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (ITGC)** | 최고 의사결정 기구, IT 전략·예산 승인 | ISO 38500 6대 원칙 준수, 연 4회 정례 회의, ESG·리스크 보고 의무, CIO·CFO·CEO·외부이사 참여 |
| **EA 팀 (Enterprise Architecture Team)** | To-Be 아키텍처 설계, 표준 수립 | TOGAF 10 ADM 8단계(Preliminary->Vision->Business->Information Systems->Technology->Opportunities->Migration->Implementation Governance->Change Management) + Requirements Management |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리(PPM), 표준화·품질 보증 | PMBOK 7th 12원칙, P3O(Portfolio, Programme, Project Office) 3계층 모델, EVM(Earned Value Management) CPI/SPI 0.9 이상 유지 |
| **ITSM(Service Operation)** | IT 서비스 설계·전환·운영·개선 | ITIL 4 Service Value System(SVS): Opportunity/Demand -> Value -> 34개 Practice(General/Service/Technical), 4가지 Dimension(Organizations, People, Information, Technology, Partners, Suppliers, Value Streams, Processes) |
| **보안 거버넌스 (InfoSec GRC)** | 정보보안 정책·통제·모니터링 | ISO 27001:2022 Annex A 93개 통제 항목(4 영역: Organizational 37, People 8, Physical 14, Technological 34), ISMS-P 인증, K-ISMS, CSAP(클라우드 보안 인증) |
| **FinOps 팀** | 클라우드 비용 최적화, 쇼백/차지백 | AWS Cost Explorer, Azure Cost Management, GCP Billing, KPI: 단위 업무당 클라우드 비용($
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 525 / 800

<- **이전**: [524. IT 경영 관리 핵심 토픽 524번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/524_it_management_core_topic_524_exam_summary/)
**다음**: [526. IT 경영 관리 핵심 토픽 526번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/526_it_management_core_topic_526_exam_summary/) ->

---
