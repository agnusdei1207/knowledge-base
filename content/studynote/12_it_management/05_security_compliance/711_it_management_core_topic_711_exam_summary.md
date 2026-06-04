+++
title = "711. IT 경영 관리 핵심 토픽 711번 시험 요약 (IT Management Core Topic 711 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019의 EDM(Evaluate-Direct-Monitor) 사이클과 ITIL 4의 Service Value System(SVS)을 결합한 **이중 거버넌스 체계**로, IT 전략과 비즈니스 가치를 정렬(Alignment)하는 메커니즘.
> 2. **가치**: ISACA 보고 기준 IT 거버넌스 성숙도 4단계 이상 도달 시 프로젝트 성공률 **38%->72%**, ROI 평균 **2.4배**, 보안사고 **56% 감축**.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Federated) 거버넌스, **Build vs Buy vs SaaS**, BSC 기반 KPI 4관점(재무/고객/내부/학습성장) 간 가중치(Weight) 배분, 그리고 Zero-Trust 보안정책과의 통합 여부.

---

## Ⅰ. 개요 및 필요성

전통적 IT 관리는 "비용센터"로서의 역할에 머물렀으나, 4차 산업혁명 시대를 맞아 **"비즈니스 전략적 자산(Business Strategic Asset)"** 으로 재정의되어야 함. 2024년 Gartner 조사에 따르면 CIO의 **68%** 가 "IT 투자와 비즈니스 성과 간 인과관계 입증"을 최대 과제로 응답했으며, 이는 **IT 거버넌스(Governance)·전략(Strategy)·성과(Performance)·위험(Risk)·자원(Resource)** 5대 영역의 통합적 관리 프레임워크 없이는 해결 불가능.

```text
[전통적 IT 관리 vs 현대 IT 경영 관리 패러다임 비교]

  +-------------------------+         +-----------------------------+
  |  전통적 IT 관리 (2000s)  |         |  현대 IT 경영 관리 (2020s)   |
  +-------------------------+         +-----------------------------+
  |  CIO: "서버 관리자"      |   ->->->   |  CIO: "CDO 겸직 / 이사회 멤버"|
  |  Cost Center (비용)     |   ->->->   |  Value Center (가치창출)    |
  |  CapEx 중심 일회성 투자  |   ->->->   |  OpEx 중심 지속적 혁신      |
  |  ITIL v3 (프로세스)     |   ->->->   |  ITIL 4 + COBIT 2019 + EA   |
  |  SLA: 가용성 99.9%      |   ->->->   |  SLO: 고객 경험(NPS/UX)기반 |
  |  Project 단위 관리       |   ->->->   |  Product/Platform 단위 관리  |
  +-------------------------+         +-----------------------------+
              |                                       |
              +----------- 디지털 전환(DX) ------------+
                          |
              +-----------v------------+
              |  정보화 사업 관리 법령   |
              |  (클라우드, 데이터3법)   |
              +------------------------+
```

법적·제도적 배경으로 **「전자정부법」, 「정보시스템 효율적 도입·운영 지침(행안부)」「클라우드컴퓨팅법(2023.9)」「데이터산업법」「개인정보보호법」** 등이 IT 경영의 필수 통제 항목이 되었으며, ISMS-P 인증, CSAP(클라우드 보안인증), 데이터 거버넌스 표준(ISO 11179) 준수 여부가 사업 승격의 핵심 평가지표로 작동.

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판과 자동운전 시스템**과 같습니다. 과거에는 엔진룸만 보던 정비공이, 이제는 **속도·연비·안전을 종합 제어하는 자율주행 시스템**으로 진화한 것이죠.

---

## Ⅱ. 아키텍처 및 핵심 원리

**COBIT 2019 + ITIL 4 통합 거버넌스 참조모델(Integrated Governance Reference Model)** 구조는 다음과 같은 5개 계층과 핵심 프로세스로 구성됩니다.

```text
[IT 경영 관리 통합 아키텍처 - 5 Layer Reference Model]

   +------------------------------------------------------+
   | Layer 5: 거버넌스 의사결정 (Board/CIO Steering)       |
   |   - EDM: Evaluate(평가) -> Direct(지시) -> Monitor(감시)|
   |   - BSC KPI: 재무/고객/내부프로세스/학습성장           |
   +------------------------------------------------------+
   | Layer 4: 전략기획 (IT Strategy & Portfolio)            |
   |   - SAM(Strategic Alignment Model) : Henderson &       |
   |     Venkatraman 4관점(IT Strategy/IS Strategy/         |
   |     Organzation Infrastructure/Process)               |
   |   - IT Portfolio: Demand(41%) vs Supply(59%)          |
   |   - Build 30% / Buy 50% / SaaS 20% (이상적 비율)      |
   +------------------------------------------------------+
   | Layer 3: 프로세스 운영 (COBIT 2019 40개 프로세스)      |
   |   - EDM(5) / APO(14) / BAI(11) / DSS(6) / MEA(4)      |
   |   - ITIL 4 SVS: Opportunity/Demand -> Value            |
   |   - 7 Guiding Principles: Focus on Value, Start Where |
   |     You Are, Progress Iteratively, etc.               |
   +------------------------------------------------------+
   | Layer 2: 정보·데이터 거버넌스                          |
   |   - DAMA-DMBOK 11개 지식영역                          |
   |   - Master Data(MDM), Data Quality(DQ), Metadata      |
   |   - Data Lineage(계보추적) + Data Catalog              |
   +------------------------------------------------------+
   | Layer 1: 인프라·기술 (Technology Foundation)            |
   |   - Hybrid Cloud (Private 40% / Public 60%)           |
  |   - Zero-Trust Architecture (NIST SP 800-207)          |
   |   - Container/Kubernetes/Service Mesh (Istio)         |
   +------------------------------------------------------+
              ^           ^           ^           ^
          IT Strategy  IT Portfolio  IT Operation  IT Security
          (Plan)        (Build)       (Run)         (Protect)
```

### COBIT 2019 5개 도메인 및 ITIL 4 SVS 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 이사회/CIO 의사결정 | 5단계: Benefit Realization(ROI/NPV), Risk Optimization, Resource Optimization, Transparency, Stakeholder Engagement. 목표 계단식 매핑(Cascading Goals): **13개 Enterprise Goals -> 13개 Alignment Goals -> 40개 Process** |
| **APO (Align, Plan, Organize)** | 전략 정렬·기획 | 14개 프로세스. **APO01(관리체계)** -> APO04(혁신) -> APO12(리스크) -> APO13(보안). **SAM(Strategic Alignment Model)** 4사분면(Strategy, Infrastructure, Process, IS Strategy) 적용 |
| **BAI (Build, Acquire, Implement)** | 구축·도입·변경 | 11개 프로세스. **BAI03(솔루션 도입)** 시 Build vs Buy vs SaaS 의사결정 매트릭스 사용. **DevOps 파이프라인**(Plan->Code->Build->Test->Release->Deploy->Operate->Monitor) 통합 |
| **DSS (Deliver, Service, Support)** | 운영·지원 | 6개 프로세스. **ITIL 4 SVS(Value Chain: Plan/Engage/Design&Transition/Obtain&Build/Deliver&Support)** 와 직접 매핑. SLA 99.9%, MTTR < 30분, Incident 분류 P1~P4 |
| **MEA (Monitor, Evaluate, Assess)** | 모니터링·평가 | 4개 프로세스. **Capability Level(0~5) vs Maturity Level(0~5)** 이원 평가. 목표: Capability Level 3(Defined Process) 이상, Maturity Level 3(Managed) 이상 |
| **ITIL 4 SVS (Service Value System)** | 서비스 가치 창출 | 5개 핵심: **Guiding Principles(7), Governance, Service Value Chain(6), Practices(34), Continual Improvement**. SLO/SLI 기반 **오류 예산(Error Budget)** 운영 |
| **BSC (Balanced Scorecard)** | 성과 측정 | 4관점 KPI: 재무(ROI, Cost Ratio) 25%, 고객(CSAT, NPS) 25%, 내부(배포빈도, MTTR) 25%, 학습성장(직원역량, 혁신률) 25% |

### 핵심 알고리즘·수식

**1) IT 투자 우선순위 결정 모델 (Weighted Scoring Model)**
```
우선순위 점수 = Σ(Wi × Si)
  Wi: 기준 가중치 (전략정합성 0.30, ROI 0.25, 리스크 0.20,
                       기술성숙도 0.15, 규정준수 0.10)
  Si: 각 기준 점수 (1~5)
```

**2) TCO (Total Cost of Ownership) 산정**
```
TCO = 직접비(Direct: HW/SW/Lic) + 간접비(Indirect: 전력·냉각 30%)
    + 인건비(Personnel: FTE × 단가) + 기회비용(Opportunity Cost)
    - 잔존가치(Salvage Value)
통상 3년 TCO: HW 27%, SW 18%, 인건비 38%, 운영 17%
```

**3) NPV (Net Present Value) - IT 사업 재무 평가**
```
NPV = Σ [CFt / (1+r)^t] - C0
  r: 할인율 (WACC 8~12%), t: 연차, CF: 현금흐름
NPV > 0 -> 사업 추진, IRR > Hurdle Rate -> 승인
```

- **📢 섹션 요약 비유**: COBIT의 40개 프로세스는 **병원 진료 체계**와 같습니다. EDM은 **진단 의사(ED)**, APO는 **진료 계획 수립(PA)**, BAI는 **수술/치료(Surgery)**, DSS는 **입원·회복(Recovery)**, MEA는 **재활·사후관리(F/U)** 처럼 환자가 들어와서 퇴원할 때까지의 전 과정을 분업·협업하는 시스템이죠.

---

## Ⅲ. 비교 및 연결

### 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 통합 | IT 서비스 관리(ITSME) | IT 거버넌스 국제표준 | 프로세스 성숙도 평가 |
| **출처** | ISACA(2018~) | AXELOS(2019~) | ISO/IEC(2015) | CMMI Institute(ISACA) |
| **범위** | 5도메인/40프로세스 | 4차원/34Practice | 6원칙(책임·전략·획득·성능·준법·인간) | 5성숙도레벨/20PA |
| **강점** | 거버넌스-관리 연계, Cascading Goals | 가치 중심(Value), Lean/Agile 통합 | CEO/CIO 거버넌스 책임 명시 | 엔지니어링 프로세스 정량적 측정 |
| **약점** | 구현 복잡, 학습곡선 가파름 | 거버넌스 영역 약함 | 구현 가이드 부재 | IT서비스·거버넌스 미포함 |
| **적용 단계** | 대규모/규제산업(금융, 공공) | 서비스 운영 중심 기업 | 글로벌 다국적 기업 | SW/시스템 개발 조직 |
| **한국 활용** | 공공/금융 80%+ | 대기업/IDC 60%+ | 공공부문 표준 참고 | SI/공공 SW사업 |

### Build vs Buy vs SaaS 의사결정

| 구분 | **In-House Build (자체개발)** | **Buy (패키지 도입)** | **SaaS (구독형)** |
| :--- | :--- | :--- | :--- |
| **초기투자(CapEx)** | 매우 높음(인력+인프라) | 중간(라이선스+구축) | 없음(월 구독료 OpEx) |
| **구축기간** | 12~24개월 | 3~9개월 | 1~4주(설정만) |
| **커스터마이징** | ★★★★★ 자유도 최고 | ★★★☆☆ 설정 범위 내 | ★☆☆☆☆ 표준기능만 |
| **데이터 통제권** | 완전 통제 | 부분 통제 | 제한적(법·계약) |
| **확장성(Scalability)** | 직접 설계 필요 | 벤더 의존 | 자동 확장(Auto-Scale) |
| **적합 케이스** | 핵심역량, 차별화, 보안규제 | 업종 표준 프로세스 | 비핵심, 빠른 시장진입 |
| **TCO 3년 비교** | 100% (기준) | 60~70% | 35~50% |
| **리스크** | 일정·품질 실패 | 벤더 종속(Lock-in) | 데이터 반출, 계약종료 |

**결정 트리 의사결정**:
- 핵심역량 여부? -> Yes -> **Build**
- 표준 프로세스인가? -> Yes -> **Buy**
- 시장진입 시급성? -> 매우 시급 -> **SaaS**
- 데이터 주권(금융/의료)? -> 매우 중요 -> **Private Build + Cloud**

- **📢 섹션 요약 비유**: Build/Buy/SaaS는 **집 짓기** 와 같습니다. Build는 **직접 시공(주인 장기 거주, 맞춤형)**, Buy는 **모델하우스 구매(주방·욕실 표준, 일부 커스터마이징)**, SaaS는 **서비스드 아파트**(필요한 것만 즉시 사용, 1개월 후 퇴거 자유) — 이 선택이 회사의 10년 운명을 가릅니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **거버넌스 체제 수립**: CEO 직속 **IT Steering Committee** 운영 여부(분기 1회), COBIT 2019 EDM 5단계 활동 정착, RACI 매트릭스(Responsible/Accountable/Consulted/Informed) 작성·배포 확인.
2. **전략 정렬(Alignment) 검증**: SAM 4사분면에서 IT-Strategy 매핑 완료 여부, **연 1회 이상** IT-Portfolio Review 수행, 미스 정렬 프로젝트 0%화 목표.
3. **성과 측정 체계**: BSC 4관점 KPI 8~12개 선정, KPI당 **측정 가능성(SMART)** 확인, 분기별 KPI Dashboard 운영, **데이터 기반 의사결정(DDDM)** 정착도.
4. **리스크·보안 통제**: ISO 27001 + ISMS-P 이중 인증, **NIST CSF**(Identify, Protect, Detect, Respond, Recover) 5함
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 711 / 800

<- **이전**: [710. IT 경영 관리 핵심 토픽 710번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/710_it_management_core_topic_710_exam_summary/)
**다음**: [712. IT 경영 관리 핵심 토픽 712번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/712_it_management_core_topic_712_exam_summary/) ->

---
