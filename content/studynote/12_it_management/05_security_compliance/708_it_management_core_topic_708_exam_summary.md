+++
title = "708. IT 경영 관리 핵심 토픽 708번 시험 요약 (IT Management Core Topic 708 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(708번) 시험은 ISP->EA 구축->IT 거버넌스(COBIT 2019)->ITIL 4 서비스 운영->프로젝트 포트폴리오 관리(PMBOK 7/Agile)->정보보안(ISMS-P/ISO 27001)->디지털 전환(클라우드·AI·데이터)까지 **정보시스템의 기획부터 폐기까지 전 생애주기(Lifecycle)를 거버넌스·프로세스·기술·인재 4축으로 통합 관리**하는 능력을 평가한다.
> 2. **가치**: 정량적으로는 IT 투자 대비 ROI 20~35% 향상, TCO 15~25% 절감, 사고 대응시간(MTTR) 60% 단축, 정성적으로는 경영 가시성(Visibility) 확보, 컴플라이언스 리스크 제거, 디지털 비즈니스 모델 전환의 기반 제공.
> 3. **판단 포인트**: ① **프레임워크 선택**(COBIT vs ITIL vs ISO 20000 vs ISO 27001의 중첩과 우선순위), ② **Agile-Waterfall 하이브리드**, ③ **Bimodal IT**(Mode 1: 안정성, Mode 2: 속도), ④ **Build vs Buy vs Cloud(IaaS/PaaS/SaaS)**, ⑤ **Zero Trust 보안 모델**, ⑥ **데이터 기반 의사결정(데이터 거버넌스 vs 분석 거버넌스)** — 이 6가지 의사결정 축이 답안의 핵심 분기점이다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management)는 단순한 "IT 부서 운영"이 아니라, **경영 전략과 IT를 정렬(Strategic Alignment)**하여 기업 가치를 극대화하는 학제적(Interdisciplinary) 경영 기능이다. 708번 시험은 한국방송통신전파진흥원·정보통신공학기술사가 출제하는 영역으로, 기술사 답안은 반드시 "경영학적 프레임워크"와 "정보기술 아키텍처"를 동시에 논증해야 한다.

### 출제 배경 및 기술적 도전과제

기존 1980~2000년대 **전산실 중심의 MIS(Mainframe-based Management Information System)**는 ROI 측정이 어렵고, 부서별 **정보 사일로(Information Silo)**, **Shadow IT**, **유지보수 비용 폭증(Software Aging)** 문제가 상존했다. 2010년 이후 모바일·클라우드·빅데이터가 보편화되면서 전통적 ERP 중심의 운영은 한계에 부딪혔고, **디지털 전환(DX, Digital Transformation)**이라는 경영 패러다임이 등장했다.

이 패러다임 전환에서 IT 경영 관리의 핵심 도전과제는 다음과 같다.

- **전략-기술 정렬(Gap)**: CEO와 CIO 사이의 인지만 3~5년 어긋남(예: McKinsey 2023 Survey, 67% 기업)
- **투자 우선순위 결정**: 한정된 CapEx/OpEx를 신사업·운영·보안·컴플라이언스에 어떻게 배분할 것인가
- **레거시 현대화(Legacy Modernization)**: COBOL/PL-I 기반 메인프레임을 어떻게 Cloud-Native MSA로 전환할 것인가
- **데이터 거버넌스**: GDPR·개인정보보호법·AI 기본법 하에서 데이터 활용과 프라이버시 양립
- **사이버 회복력(Cyber Resilience)**: 랜섬웨어·공급망 공격에 대한 BC/DR 역량 강화

### IT 경영 관리의 4대 영역(도메인) 맵

```text
+---------------------------------------------------------------------+
|              IT 경영 관리 (IT Management) 4축 통합 프레임            |
+------------------+------------------+------------------+------------+
|  ① 거버넌스/전략  |  ② 프로세스/운영  |  ③ 기술/아키텍처  |  ④인재/조직|
+------------------+------------------+------------------+------------+
| • ISP/EA          | • ITIL 4         | • 클라우드 전환  | • 직무 재설계|
| • COBIT 2019      | • PMBOK 7/Agile  | • MSA/API       | • DevOps   |
| • BSC/성과측정    | • DevOps/CI-CD   | • 데이터 플랫폼  | • 데이터리터러시|
| • ISO 27001/ISMS  | • ITSM/Ticketing | • Zero Trust    | • 변화관리  |
| • 컴플라이언스     | • SLA/Ola/UC     | • AI/MLOps      | • 거버넌스위원회|
+------------------+------------------+------------------+------------+
|        -> Output: 디지털 비즈니스 플랫폼 + 데이터 기반 의사결정        |
+---------------------------------------------------------------------+
```

### 왜 이 4축이 필수인가 (Old vs New Paradigm)

| 구분 | Old Paradigm (1990~2010) | New Paradigm (2015~현재) |
|:-----|:------------------------|:------------------------|
| **IT의 위치** | 비용(Cost Center)·지원 기능 | 가치 창출(Value Driver)·전략 자산 |
| **아키텍처** | 모놀리식(Soa·ERP 패키지) | MSA(Microservice)·Cloud-Native |
| **투자 방식** | CapEx 일회성 | OpEx 구독형·Pay-as-you-go |
| **성과 측정** | 가용성(Uptime)·프로젝트 일정 | NPS·TTM·ROI·EBITDA 기여도·데이터 활용률 |
| **보안 모델** | Castle-and-Moat(방화벽 경계) | Zero Trust(신원·디바이스·행위 기반) |
| **조직 문화** | 계획 중심·연간 SI 프로젝트 | Agile·제품 중심(Prod)·SRE·Platform Engineering |

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판·엔진·핸들·내비게이션을 동시에 보는 운전**과 같다. 한 축만 잘 만든 차(예: 엔진만 좋은 차)는 사고를 내고, 네 축이 모두 정렬되어야 목적지에 안전·경제적·신속하게 도달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 4개의 직교(Orthogonal) 레이어로 설계되며, 각 레이어는 국제 표준 프레임워크로 구현된다.

### 전체 아키텍처: Zachman + TOGAF 기반 통합 레이어

```text
                +------------------------------------------+
                |        ① 전략/거버넌스 레이어             |
                |  (COBIT 2019 · ISO 38500 · 전략위원회)     |
                |  KPI: BSC(재무·고객·프로세스·학습)         |
                +--------------------+---------------------+
                                     |  Alignment(정렬)
                +--------------------v---------------------+
                |        ② 프로세스/서비스 레이어            |
                |  (ITIL 4 · PMBOK 7 · DevOps · SRE)        |
                |  SLA/Ola·Incident·Change·Problem          |
                +--------------------+---------------------+
                                     |  Service Catalog
                +--------------------v---------------------+
                |        ③ 데이터/애플리케이션 레이어        |
                |  (DAMA-DMBOK · TOGAF · API Gateway)        |
                |  Master·Reference·Transactional Data      |
                +--------------------+---------------------+
                                     |  Integration Bus
                +--------------------v---------------------+
                |        ④ 인프라/플랫폼 레이어              |
                |  (Cloud · Container · Zero Trust Network)  |
                |  IaaS/PaaS/SaaS · K8s · IaC(Terraform)    |
                +------------------------------------------+
                                     |
                          +----------v----------+
                          | ⑤ 보안/리스크 거버넌스 |
                          | (ISMS-P · ISO 27001) |
                          |  Privacy·BCP/DRP     |
                          +---------------------+
```

### 핵심 프레임워크별 상세 매핑

| 구성 요소 (Layer/Framework) | 역할 (Role) | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **COBIT 2019** (거버넌스) | IT 거버넌스 목표 체계(40개 Goal Cascade) | EDM(평가·지시·모니터) -> Align, Plan, Organize(APO) -> Build, Acquire, Implement(BAI) -> Deliver, Service, Support(DSS) -> Monitor, Evaluate, Assess(MEA). **Cascade: Stakeholder Needs -> Enterprise Goals -> Alignment Goals -> Management Objectives** |
| **ITIL 4** (서비스 운영) | IT 서비스 관리(SVS: Service Value System) | 7 Guiding Principle(聚焦·진행·피드백·협업·사고·단순·최적화) + 34 Practice(Change Enablement, Incident, Problem, Service Desk, Service Request, Continual Improvement). **SLA 99.9% 이상** 목표 관리 |
| **TOGAF 10 / Zachman** (EA) | 전사 아키텍처 방법론 | ADM 8 Phase: Preliminary->A(아키텍처 비전)->B(비즈니스)->C(데이터/앱)->D(기술)->E(기회·솔루션)->F(마이그레이션 계획)->G(구현 거버넌스)->H(아키텍처 변경 관리) |
| **PMBOK 7 / Agile** (프로젝트) | 프로젝트·제품 포트폴리오 관리 | 8 Performance Domain(Team, Planning, Work, Delivery, Measurement, Uncertainty, Complexity, Risk) + 12 Principle. **Hybrid: Predictive(Waterfall) + Adaptive(Agile/Scrum/Kanban)** |
| **ISO 27001 / ISMS-P** (보안) | 정보보호 관리체계 | 93 Control(Annex A 2022) -> A.5 조직, A.6 사람, A.7 물리, A.8 기술. **Plan-Do-Check-Act** + 위험평가 방법론(ISO 27005) |
| **BSC (Balanced Scorecard)** (성과) | 다관점 성과 측정 | 4 Perspective: 재무(ROI, NPV)·고객(NPS, CSAT)·내부 프로세스(Defect Rate)·학습·성장(Skill Index) |
| **DAMA-DMBOK 2** (데이터) | 데이터 거버넌스 11개 지식 영역 | 거버넌스·아키텍처·모델·저장·보안·통합·마스터/참조·문서·참조·메타·품질 |
| **CMMI / ITIL CSI** (성숙도) | 프로세스 성숙도 평가 | Level 1(Initial)->2(Managed)->3(Defined)->4(Quantitatively Managed)->5(Optimizing) |

### 핵심 알고리즘·수식·판단 공식

**(1) IT 투자 ROI 산출**

```
ROI(%) = (총 이익 − 총 비용) / 총 비용 × 100
NPV = Σ [CFt / (1+r)^t] − 초기투자
TCO = CapEx(서버·네트워크·라이선스) + OpEx(전력·인건비·교육·유지보수) 3~5년
Payback Period(년) = 초기투자액 / 연 현금유입
```

**(2) 우선순위 결정 - Eisenhower Matrix + WSJF (SAFe)**

```
WSJF = Cost of Delay / Job Size
     = (User-Business Value + Time Criticality + Risk Reduction) / Job Size
```

**(3) 사이버 리스크 정량화 (FAIR 모델)**

```
Annual Loss Expectancy(ALE) = Asset Value(AV) × Threat Frequency × Vulnerability × Impact
Risk = Probability × Impact (Heat Map 5×5)
```

**(4) EA 정렬도 측정 (Architectural Compliance)**

```
Compliance Rate(%) = (표준 준수 컴포넌트 수 / 전체 컴포넌트 수) × 100
Target: 80% 이상 (TOGAF 권고)
```

- **📢 섹션 요약 비유**: COBIT 2019는 **국가 헌법**, ITIL 4는 **민사소송법**(서비스 계약), ISO 27001은 **형법**(보안 의무), TOGAF는 **도시계획법**, PMBOK은 **건설 현장 매뉴얼**과 같다. 이 5법전을 동시에 읽고 일관되게 해석하는 것이 기술사의 역할이다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 자주 혼동되는 핵심 개념 쌍을 명확히 구분한다.

| 구분 | COBIT 2019 (거버넌스) | ITIL 4 (운영/서비스) | ISO 27001 (보안) | PMBOK 7 (프로젝트) |
|:---|:---|:---|:---|:---|
| **핵심 목적** | "무엇을·왜" (What & Why) | "어떻게 운영" (How) | "리스크 통제" (How to Secure) | "일회성 목표 달성" (How to Deliver) |
| **대상 범위** | 전사 IT 거버넌스·이사회 보고 | IT 서비스 데스크·운영팀 | 정보자산 전체(데이터·시스템·사람) | 프로젝트 단위(임시 조직) |
| **측정 KPI** | Goal Cascade 달성률, ROI | SLA 달성률, MTTR, MTTD | KRI(핵심리스크지표), 사고 건수 | SPI/CPI, Earned Value |
| **생애주기** | 영속적(Standing) | 서비스 운영 주기 | 연속적(Continuous) | 임시적(Temporary, 시작-종료) |
| **주 사용자** | CIO·이사회·감사인 | IT 운영자·SRE·Help Desk | CISO·보안팀·컴플라이언스 | PM·PMO·Agile Coach |
| **관계** | 상위 거버넌스 | COBIT의 BAI/DSS 영역을 운영 | COBIT의 APO13/DSS05 영역 | 프로젝트 종료 후 운영은 ITIL로 이관 |

### 자주 출제되는 비교·연결 질문

| 비교 쌍 | 주요 차이점 | 실무 적용 포인트 |
|:---|:---|:---|
| **IT 거버넌스 vs IT 관리** | Governance(지시·통제) ≠ Management(실행) — King III 보고서(남아공), ISO 38500 | 이사회·CEO 책임(거버넌스), CIO·실무자 책임(관리) |
| **ISP vs EA** | ISP(Information Strategy Planning): 3~5년 IT 로드맵·투자계획 / EA(Enterprise Architecture): 시스템·데이터·기술 표준·통합 설계 | ISP는 **What & Why**, EA는 **How** — ISP가 상위, EA가 하위 |
| **BPR vs BPM** | BPR(Hammer & Champy, 1993): Radical Redesign / BPM(현재): 점진적·지속적 개선 | BPR은 1회성 혁명, BPM은 Kaizen·Lean Six Sigma |
| **Agile vs Waterfall** | Agile(불확실·변동 많음) vs Waterfall(요구사항 명확·규제 산업) | Hybrid: **SAFe, ScrumBan, Water-Scrum-Fall** |
| **DevOps vs SRE** | DevOps(문화·철
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 708 / 800

<- **이전**: [707. IT 경영 관리 핵심 토픽 707번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/707_it_management_core_topic_707_exam_summary/)
**다음**: [709. IT 경영 관리 핵심 토픽 709번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/709_it_management_core_topic_709_exam_summary/) ->

---
