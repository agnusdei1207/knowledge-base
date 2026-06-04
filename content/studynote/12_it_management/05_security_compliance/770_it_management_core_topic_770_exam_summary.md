---
title: "770. IT 경영 관리 핵심 토픽 770번 시험 요약 (IT Management Core Topic 770 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 770. IT 경영 관리 핵심 토픽 시험 요약 (IT Management Core Topic Exam Summary)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Information Technology Governance)는 COBIT 2019, ISO/IEC 38500, ITIL 4, PMBOK 7th, TOGAF 10 같은 글로벌 프레임워크를 기반으로 **전략(S Strategy) ↔ 아키텍처(A Architecture) ↔ 운영(O Operation) ↔ 평가(M Measurement)** 의 4축 통합 거버넌스를 통해 기업 가치(Value Delivery)와 리스크 최적화(Risk Optimization), 자원 효율(Resource Optimization)을 동시에 달성하는 경영 체계이다.
> 2. **가치**: McKinsey(2024) 및 IDC(2025) 보고에 따르면, 성숙한 IT 거버넌스 체계 구축 조직은 디지털 전환 성공률을 **평균 35% -> 78%**(2.2배)로 끌어올리고, IT 투자 대비 ROI를 **연 18~27%** 개선하며, 사이버보안 사고 대응 시간을 **MTTD 287일 -> 16일**(94% 단축)로 단축시킨다.
> 3. **판단 포인트**: 핵심 의사결정 트레이드오프는 (a) **집중형(Centralized) vs 분산형(Federated) 거버넌스 모델**, (b) **Best-of-Breed 개별 솔루션 vs One-Stop 통합 플랫폼 전략**, (c) **Bimodal IT(Plan-Build-Run 모드 1·2 병행) vs Customer-Centric Value Stream 단일 흐름**의 세 가지 이분법이며, 기술사적 판단의 핵심은 **Business Outcome 중심의 KPI(예: NPS, Time-to-Market, TCO) ↔ IT 운영 지표(예: SLA, 가용성 99.99%, MTTR)** 간의 인과 매핑(Causal Mapping)을 명확히 설계하는 것이다.

---

## Ⅰ. 개요 및 필요성

### 1. 시대적 배경과 등장 배경

4차 산업혁명 이후 데이터·AI·클라우드가 **"그냥 새로운 기술"** 에서 **"경영의 핵심 자본(Strategic Asset)"** 으로 격상됨에 따라, IT 부서는 단순한 비용 센터(Cost Center)에서 **전략적 비즈니스 파트너(Strategic Business Partner)** 로 역할이 재정의되었다. ISO/IEC 38500:2015 의 6개 원칙(Evaluate, Direct, Monitor) 기반의 이사회 수준 거버넌스가 요구되고 있으며, 2024년 EU의 DORA(Digital Operational Resilience Act)·한국의 **AI 기본법(2026.1 시행)** ·ISMS-P 인증 의무화 확대 등에 따라 IT 경영의 컴플라이언스 임계점이 비약적으로 상승했다.

또한 코로나19 이후 **원격·하이브리드 근무常态化**, 생성형 AI(GenAI) 도입 가속화, 양자컴퓨팅 위협 등 **VUCA(Volatility, Uncertainty, Complexity, Ambiguity)** 환경이 고도화되면서, IT 투자의 의사결정·실행·평가 전 주기(End-to-End)에 걸친 통합 관리 체계의 부재가 **"DX 실패율 70%"**(맥킨지 2023) 같은 산업 통계를 반복적으로 양산하고 있다.

### 2. 기존 vs 새로운 패러다임

| 구분 | 전통적 IT 관리(2000년대) | 현대 IT 경영 관리(2024~) |
| :--- | :--- | :--- |
| **관점** | IT는 비용(Cost) | IT는 가치(Value) & 위험(Risk) |
| **조직** | CIO 1인 주도, Silo형 | CDO·CISO·CDAO와 공동 거버넌스 위원회 |
| **투자 기준** | ROI, NPV 정량 지표 | TCO, TTV(Time-to-Value), ROO(Return on Optimization) |
| **아키텍처** | Monolith, On-Premise | Cloud-Native, Composable, Mesh |
| **관리 프레임워크** | ITIL v3, COBIT 5 | ITIL 4, COBIT 2019, ISO 38500, NIST CSF 2.0 |
| **운영** | Reactive(장애 후 대응) | AIOps, Observability 3.0, SRE 기반 Proactive |
| **보고 체계** | 월간 IT KPI 보고서 | 실시간 Digital Twin 기반 의사결정 대시보드 |
| **규제 대응** | 사후 컴플라이언스 | Continuous Compliance, GRC 자동화 |

### 3. 전체 개념도

```text
+----------------------------------------------------------------------+
|                    IT 경영 관리 4축 통합 거버넌스 모델                  |
|                                                                      |
|  +--------------+   +--------------+   +--------------+ +----------+|
|  |   Strategy   |   | Architecture |   |  Operation   | | Measure  ||
|  |   (전략)     |<--->|  (아키텍처)  |<--->|   (운영)     |<--->| (평가)   ||
|  +------+-------+   +------+-------+   +------+-------+ +----+-----+|
|         |                  |                  |              |      |
|  +------v------------------v------------------v--------------v-----+|
|  |              Governance & Compliance Layer                      ||
|  |  COBIT 2019 · ISO 38500 · NIST CSF 2.0 · K-ISMS-P · DORA       ||
|  +----------------------------------------------------------------+|
|                                                                      |
|  입력: +--------+ +--------+ +--------+ +--------+ +--------+       |
|       |비즈니스| |규제/법  | |기술 트렌| |고객/시장| |위험/리스크|    |
|       |요구사항| |규    | |드(AI/Cloud)| |니즈   | |요인    |       |
|       +---+----+ +---+----+ +---+----+ +---+----+ +---+----+       |
|           +----------+----------+----------+----------+              |
|                            |                                        |
|                  +---------v---------+                              |
|                  |  IT Steering Com. | <- 의사결정 정점               |
|                  |  (이사회/CIO)     |                              |
|                  +---------+---------+                              |
|                            |                                        |
|           +----------------+----------------+                       |
|           |                |                |                       |
|   +-------v------+ +-------v------+ +-------v------+               |
|   | Portfolio    | | Program      | | Project &    |               |
|   | Mgmt(PPM)    | | Mgmt(PgM)   | | BA(Service)  |               |
|   +------+------+ +------+------+ +------+------+               |
|          +----------------+----------------+                       |
|                            |                                        |
|                  +---------v---------+                              |
|                  |  Value Realization| <- KPI·BSC·OKR 기반           |
|                  |  & Continuous     |                              |
|                  |  Improvement      |                              |
|                  +-------------------+                              |
+----------------------------------------------------------------------+
```

### 4. 왜 필요한가? (5대 핵심 동기)

1. **정렬(Alignment)**: Business Strategy ↔ IT Strategy 정렬 부족 시 **"Strategy Gap"** 으로 IT 투자 35%가 무용지물화 (Gartner 2023).
2. **리스크 관리**: 랜섬웨어·내부자 위협·공급망 해킹 등 공격면(Attack Surface) 확대로 **사이버 보험료 +58%** YoY 증가.
3. **규제 준수**: GDPR, DORA, ESG 공시, AI 기본법 등 **연간 신규 규제 200건+** 환경에서 수동 대응 한계.
4. **자원 최적화**: 클라우드 지출의 **30%가 낭비(FinOps Foundation 2024)** 이며, SaaS Shadow IT는 평균 1,200개/기업 수준.
5. **가속화(Agility)**: M&A·시장 진입 등 전략적 이벤트의 **Time-to-Decision을 75% 단축**하기 위해 의사결정 자동화 필수.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 종합 교통관제센터"** 와 같습니다. 항공·도로·철도·해운의 각 교통수단(부서별 IT 시스템)을 개별적으로만 보면 정체·사고가 끊이지 않지만, 한 곳에서 신호·노선·속도·리스크를 통합 조율하면 도시 전체의 흐름이 매끄러워집니다. **COBIT·ITIL·PMBOK** 이 그 관제 신호등·CCTV·관제사의 도구인 셈입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 표준 프레임워크 상호 매핑

IT 경영 관리의 핵심은 **"어떤 표준을 어떤 계층에 적용할 것인가"** 의 명확한 매핑에 있다.

```text
                    +-----------------------------+
                    |  ISO/IEC 38500:2015 (이사회) | <- 6 Principles
                    |  Evaluate·Direct·Monitor    |
                    +--------------+--------------+
                                   | (상위 거버넌스 원칙)
                    +--------------v--------------+
                    |  COBIT 2019 (관리 체계)      | <- 40 Obj, 5 Domains
                    |  EDM·APO·BAI·DSS·MEA        |
                    +--------------+--------------+
                                   |
        +--------------------------+--------------------------+
        |                          |                          |
+-------v--------+      +---------v----------+      +--------v---------+
|  TOGAF 10       |      |  ITIL 4            |      |  PMBOK 7th       |
|  (EA)           |      |  (서비스 운영)      |      |  (프로젝트)       |
|  ADM Cycle      |      |  SVS·34 Practices  |      |  8 Performance    |
|  ADM-8 Phase    |      |  Value Stream      |      |  Domains         |
+-----------------+      +--------------------+      +------------------+
        |                          |                          |
        +--------------------------+--------------------------+
                                   |
                    +--------------v--------------+
                    |  NIST CSF 2.0 / ISMS-P      | <- 보안 거버넌스
                    |  Govern·Identify·Protect    |
                    |  Detect·Respond·Recover     |
                    +-----------------------------+
```

### 2. 핵심 구성 요소 및 역할

| 구성 요소 | 역할 | 핵심 기술·프레임워크 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee(이사회/거버넌스 위원회)** | IT 투자·우선순위·리스크 최종 의사결정 | ISO 38500 6원칙 적용, 분기 1회 이상 정례 회의, 의사결정 기록(Digital Minute) 보관, CIO·CDO·CISO·CFO·CDAO 합동 구 |
| **COBIT 2019 (관리·운영 체계)** | 거버넌스 목표와 관리 목표의 계층적 연결 | 5개 도메인(EDM·APO·BAI·DSS·MEA) × 40개 거버넌스·관리 목표, **Cascade of Goals** 로 전략->전술->운영 KPI 자동 매핑, Focus Area(예: DevOps, AI, Risk) 추가 가능 |
| **TOGAF 10 (Enterprise Architecture)** | 비즈니스·데이터·애플리케이션·기술 4계층 아키텍처 정렬 | **ADM(Architecture Development Method) 8단계** Phase A(비전)->B(비즈니스)->C(정보시스템)->D(기술)->E(기회·솔루션)->F(구현 거버넌스)->G(구현 거버넌스)->H(아키텍처 변경 관리) 사이클 반복 |
| **ITIL 4 (서비스 운영)** | IT 서비스의 End-to-End 가치 흐름(Value Stream) 관리 | **34개 Practice**(전략·디자인·전환·운영·개선), Service Value System(SVS) = Opportunity/Demand->Value->Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support)->Value |
| **PMBOK 7th + Agile** | 프로젝트 수행과 변화 관리 | **8개 Performance Domain**(Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty, Stakeholder), 12 Principle, 예측형·적응형·하이브리드 선택 |
| **NIST CSF 2.0 / ISMS-P** | 사이버보안 거버넌스 | 6 Function(Govern·Identify·Protect·Detect·Respond·Recover) × 카테고리·하위 카테고리, ISMS-P는 한국 정보통신망법 기반 16개 영역 80개 통제항목 |
| **Value Realization Office (VRO)** | 투자 정당화 및 Benefit Realization | OKR·BSC·ROI·NPV·TCO·ROO·Carbon ROI 통합 측정, Digital Twin of Organization(DTO) 기반 실시간 KPI 대시보드 |
| **GRC Platform** | 거버넌스·리스크·컴플라이언스 통합 | ServiceNow GRC, SAP GRC, Archer, OneTrust, LogicGate — 정책·통제·증적·위험을 단일 데이터 모델로 통합 |

### 3. COBIT 2019의 Cascade of Goals (핵심 메커니즘)

```text
+----------------------+
|  Enterprise Goals    |  <- 13개 (예: EG01 포트폴리오 가치 제공)
|  (비즈니스 목표)     |     EG06 비즈니스 서비스 연속성·유연성
+----------+-----------+     EG13 지식·정보 관리
           | "Cascade"
+----------v-----------+
|  Alignment Goals     |  <- 13개 (예: AG02 관리되는 I&T 위험)
|  (IT 정렬 목표)      |     AG05 실효적인 재무·투명성
+----------+-----------+     AG12 인력·역량 관리
           |
+----------v-----------+
|  Governance/Manage.  |  <- 40개 (예: EDM01 거버넌스 프레임워크 설정)
|  Objectives          |     APO12 위험 관리
+----------+-----------+     BAI02 요구사항 관리
           |                  DSS01 운영 관리
+----------v-----------+     MEA01 성과·준수 모니터링
|  Component: Process  |
|  ·Organizational Str.|
|  ·Information Flow   |
|  ·People/Skills      |
|  ·Policies/Procedures|
+----------------------+
```

### 4. ITIL 4 Service Value Chain (SVC) 핵심 흐름

```text
   기회/수요(Opportunity & Demand)
            |
            v
   +------------------------------------------------------+
   |              Service Value Chain (SVC)               |
   |                                                      |
   |  +--------+ +--------+ +------------+ +--------+    |
   |  | Plan   |->| Engage |->| Design &   |->| Obtain |    |
   |  |        | |        | | Transition | | /Build |    |
   |  +--------+ +--------+ +------------+ +---+----+    |
   |                                          |          |
   |                              +--------
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 770 / 800

<- **이전**: [769. IT 경영 관리 핵심 토픽 769번 시험 요약](/studynote/12_it_management/05_security_compliance/769_it_management_core_topic_769_exam_summary/)
**다음**: [771. IT 경영 관리 핵심 토픽 771번 시험 요약](/studynote/12_it_management/05_security_compliance/771_it_management_core_topic_771_exam_summary/) ->

---
