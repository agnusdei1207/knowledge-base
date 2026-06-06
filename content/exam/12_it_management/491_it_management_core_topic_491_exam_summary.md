---
title: "IT Management Core Topic 491 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Governance)와 경영(Business) 간 전략적 정렬(Alignment)은 COBIT 2019의 40개 거버넌스/관리 목표를 EDM(Evaluate, Direct, Monitor) 사이클과 7가지 핵심 컴포넌트(Principles, Policies, Processes, Organizational Structures, Information, People/Skills, Services/Infrastructure/Applications)로 조직의 의사결정 체계에 내재화하는 것이다.
> 2. **가치**: Henderson & Venkatraman(1993)의 SAM(Strategic Alignment Model) 4사분면을 적용 시 IT 투자 대비 ROI를 20~35% 개선하고, 미스얼라인먼트(Misalignment) 비용(미국 평균 연간 약 $14M/기업)을 절감하며, ISO/IEC 38500, ISMS-P, 전자정부법 등 6대 규제 준수(Compliance)를 단일 거버넌스 체계로 달성한다.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 책임분산형(Federated) 거버넌스, COBIT vs ITIL vs ISO 27001 프레임워크 간 중복 영역 최적화, BSC 4관점(재무/고객/내부프로세스/학습성장) 기반 KPI 설계 시 인과관계 모델링 여부, 그리고 EA(TOGAF/Zachman)와의 통합 깊이(느슨한 결합 vs 단일 거버넌스 허브)이다.

---

## Ⅰ. 개요 및 필요성

한국 IT 산업의 성숙기에 진입하면서 단순 시스템 구축(SI) 중심의 IT 운영은 **디지털 트랜스포메이션(DX)**, **클라우드 네이티브 전환**, **AI/데이터 거버넌스**라는 새로운 패러다임으로 이행 중이다. 그러나 통계청·KISA의 자료에 따르면, 국내 대기업의 약 64%가 IT-Business Misalignment를 경험하고 있으며, 이로 인한 연간 손실이 매출 대비 0.5~1.2%에 달한다. 기술사 관점에서 IT 경영의 본질적 과제는 **"기술 도입이 아닌, 기술과 사업목표의 연결고리를 제도권 안에서 보증하는 것"**이다.

기존 1990년대 IT 관리 체계는 **시스템 수명주기(SDLC)** 중심의 프로젝트 단위 관리였다. 그러나 2000년대 들어 ISACA의 **COBIT(Control Objectives for Information and Related Technologies)**이 등장하면서, IT를 프로젝트가 아닌 **"엔터프라이즈 자산"으로 통제 가능한 거버넌스 대상**으로 재정의했다. 2012년 ISO/IEC 38500이 "IT 거버넌스 국제표준"으로 제정되고, 2018년 COBIT 2019가 발표되면서 **원칙(Principle) 기반 + 컴포넌트(Component) 기반 + 집중영역(Focus Area) 커스터마이징** 구조로 진화했다.

```text
[ IT 경영 패러다임의 변화 : 3단계 진화 ]

  +--------------+      +--------------+      +---------------------+
  |  1세대        |      |  2세대        |      |  3세대 (현재)        |
  |  SDLC 중심    | ---► |  ITIL/COBIT  | ---► |  디지털 거버넌스      |
  |  (1990s)      |      |  (2000-2015) |      |  (2018~현재)        |
  +--------------+      +--------------+      +---------------------+
        |                     |                        |
        v                     v                        v
  +--------------+      +--------------+      +---------------------+
  | • Waterfall  |      | • 프로세스    |      | • 원칙(7대 원칙)기반  |
  | • 비용/일정  |      |   중심 SLA   |      | • 40 Governance/     |
  |   삼각형     |      | • 코스트센터  |      |   Management 목표    |
  | • 프로젝트   |      |   ->프로핏    |      | • EDM 사이클         |
  |   단위 성과  |      |   센터 전환   |      | • NFR(ESG/사이버)   |
  |              |      | • ITSM 도입  |      |   통합 거버넌스       |
  +--------------+      +--------------+      +---------------------+
       비용절감              효율성                가치창출(Value)
```

```text
[ 왜 IT 거버넌스가 필요한가? : 4대 동기 ]

   +----------------------------------------------------------+
   |  ① Shadow IT  | 매년 글로벌 평균 $4.6M Shadow IT 손실    |
   |     +-► 통제 가능한 거버넌스 정책 필요                     |
   |  ② 규제 증가   | 개인정보보호법, ISMS-P, ESG, 클라우드법   |
   |     +-► 통합 컴플라이언스 체계 (6개 규제 -> 1개 거버넌스)   |
   |  ③ 사업 민첩성 | 시장 변화 18개월 -> 6개월로 단축          |
   |     +-► 전략-운영 정렬(SAM) 가속화                         |
   |  ④ 신뢰/투명성 | 주주·이사회 보고 -> GRC(Governance·Risk·   |
   |     +-► Compliance) 통합 리포팅                            |
   +----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 거버넌스 없이는 회사가 **엔진만 강력한 배**를 몰고 항해하는 것과 같다. 강(SI/인프라)은 거대한데 **키(Governance)**와 **항해도(Alignment)**가 없으면 난파당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스 표준 체계는 **3계층 메타 아키텍처**로 이해해야 한다. 최상위 **원칙(Principles) 계층**, 중간 **컴포넌트(Components) 계층**, 최하위 **목표/측정(Goals/Cascade) 계층**이다. COBIT 2019는 이 3계층을 **Cascade(연쇄적 목표 전달)** 메커니즘으로 연결한다.

**1) 7대 거버넌스 시스템 원칙(Governance System Principles)**
- Stakeholder needs 만족 / Holistic(전체론) / Dynamic(역동적) / Customizable(맞춤형) / End-to-End / Goal Cascade(목표 연쇄) / Separating Governance from Management

**2) 7대 거버넌스 프레임워크 원칙(Framework Principles)**
- Principle 1: Each enterprise has different needs
- Principle 2: Enterprise governance system should cover many frameworks
- Principle 3: 모든 컴포넌트 상호작용 / Principle 4~7: 단일언어·구조·세분화·완전성

**3) EDM 사이클(Evaluate-Direct-Monitor)**
EDM01(Governance Framework 설정), EDM02(Benefit Realization 보장), EDM03(위험 최적화), EDM04(Resource Optimization), EDM05(Stakeholder Transparency) 등 **5개 거버넌스 목표**로 구성된다. 이 5개가 이사회(Board) 및 EXCOM 레벨의 의사결정 인터페이스다.

```text
[ COBIT 2019 + SAM 4사분면 통합 아키텍처 ]

  +-----------------------------------------------------------------+
  |                 이사회 (Board) - 거버넌스 의사결정                |
  |   +------------------------------------------------------+      |
  |   |  EDM 사이클:  Evaluate(평가) -> Direct(지시) -> Monitor |      |
  |   |  EDM01 Governance | EDM02 Benefit | EDM03 Risk        |      |
  |   |  EDM04 Resources  | EDM05 Transparency (5개 목표)     |      |
  |   +------------------------------------------------------+      |
  |                              v                                  |
  |              Alignment (전략적 정렬 메커니즘)                     |
  |   +------------------------------------------------------+      |
  |   |         Henderson-Venkatraman SAM 4사분면              |      |
  |   |  +--------------+--------------+                      |      |
  |   |  |  I. 전략     | II. 전략     |                      |      |
  |   |  |  실행/IT     | 계획/IT      |                      |      |
  |   |  |  (Operation) | (Strategy)   |                      |      |
  |   |  +--------------+--------------+                      |      |
  |   |  |  III.비즈니스| IV.비즈니스 |                      |      |
  |   |  |  실행/IT     | 계획/IT      |                      |      |
  |   |  |  (Process)   | (Technology) |                      |      |
  |   |  +--------------+--------------+                      |      |
  |   |  ※ 사분면 간 정렬 메커니즘: PEST->SFAS->IT Portfolio    |      |
  |   +------------------------------------------------------+      |
  |                              v                                  |
  |   +------------------------------------------------------+      |
  |   |      40개 관리 목표 (APO-BAI-DSS-MEA 4개 도메인)     |      |
  |   |  APO(Align/Plan/Organize)  14개 목표                 |      |
  |   |  BAI(Build/Acquire/Implement) 11개                    |      |
  |   |  DSS(Deliver/Service/Support) 6개                     |      |
  |   |  MEA(Monitor/Evaluate/Assess) 4개                     |      |
  |   +------------------------------------------------------+      |
  |                              v                                  |
  |   7대 컴포넌트: ① Principles ② Policies ③ Processes              |
  |   ④ Org.Structures ⑤ Information ⑥ People/Skills ⑦ Services      |
  +-----------------------------------------------------------------+
                              v
            +----------------------------------------+
            |   KPI 계층: BSC + GQM(Goal-Question-   |
            |   Metric) + CMMI 5단계 성숙도           |
            |   L1->L2->L3->L4->L5 Cascade               |
            +----------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM 5개 목표** | 이사회 레벨 거버넌스 의사결정 | COBIT 2019의 EDM(평가-지시-모니터) 사이클로, 이사회가 IT 투자/위험/자원/투명성의 4축 의사결정을 수행. 보통 분기별 거버넌스 회의 운영. |
| **SAM 4사분면** | 사업-IT 정렬 메커니즘 | Henderson & Venkatraman(1993) 모델. 외부환경(PEST/SWOT) -> 내부역량(VRIO) -> IT 전략(BSC 매핑) -> 운영 실행으로 이어지는 연쇄 정렬. 사분면 간 Cross-Mapping(예: IV->II->I->III) 필수. |
| **40개 관리 목표** | 프로세스/관리 실행 단위 | APO14(전략관리), BAI01(프로그램관리), DSS01(운영관리), MEA01(성과모니터) 등 각 목표는 Process Practice(목표/지표/활동/책임자/RACI) 구조. RACI 매트릭스 기반 책임 할당. |
| **7대 컴포넌트** | 거버넌스 실행 토대 | 각 컴포넌트는 Variants(공통/민감/이상)를 가지며, Design Factor 11개(전략, 목표, 위험, 이슈, 위협, 규제, 역할, IT 도입, 기술전략, 규모)로 가중치 기반 우선순위 결정. |
| **KPI Cascade** | 측정 및 인과관계 추적 | BSC 4관점 KPI -> COBIT 목표별 NFR(CSF/KPI) -> 프로젝트 단위 메트릭으로 3단계 분해. 예: 전략목표 "고객만족" -> COBIT DSS02(서비스만족) KPI "고객불만률<0.5%" -> 프로젝트 KPI "API 응답시간<200ms" |

**핵심 원리의 정량적 이해**

**① Design Factor 가중치 알고리즘** (COBIT 2019)
- DF1(전략) ~ DF11(규모) 각각 0~100점 부여
- 40개 관리 목표별 매핑 테이블 참조
- 목표 우선순위 = Σ(DF_i × Weight_i)
- Top 5~8 목표를 Phase 1 이행 대상으로 선정 (이하 Pareto)

**② RACI 매트릭스 표준화**
- Responsible(1) / Accountable(1) / Consulted(n) / Informed(n)
- 모든 40개 목표의 각 Practice(총 250+ Practice)에 RACI 1:1 매핑
- A/R 중복 배정 금지, C/I는 다수 가능

**③ 목표 연쇄(Goal Cascade) 공식**
```
[Stakeholder Needs] -> [Enterprise Goals(13개)] -> [Alignment Goals(13개)]
                   -> [Governance/Management Objectives(40개)] -> [Process Goals]
```
이때 **연쇄 효율성(Alignment Score)** = Σ(매핑 성공률 × 기여도 가중치) / 전체 목표 수

- **📢 섹션 요약 비유**: COBIT 2019는 **건물의 건축법규**와 같다. EDM은 도시계획(토지이용), 40개 목표는 각 동(棟)의 용도지역, 7대 컴포넌트는 **기초/철골/배관/전기** 등 구성재료다. SAM은 그 건물을 **도로·지하철·상하수도**에 연결하는 외부 인프라 매핑이다.

---

## Ⅲ. 비교 및 연결

IT 거버넌스 생태계에는 유사한 표준이 다수 존재한다. **COBIT 2019**, **ITIL 4**, **ISO/IEC 38500**, **CMMI**, **TOGAF**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 491 / 800

<- **이전**: [490. IT 경영 관리 핵심 토픽 490번 시험 요약](/studynote/12_it_management/05_security_compliance/490_it_management_core_topic_490_exam_summary/)
**다음**: [492. IT 경영 관리 핵심 토픽 492번 시험 요약](/studynote/12_it_management/05_security_compliance/492_it_management_core_topic_492_exam_summary/) ->

---
