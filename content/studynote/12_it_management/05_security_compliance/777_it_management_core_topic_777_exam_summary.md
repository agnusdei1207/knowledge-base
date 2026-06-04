---
title: "777. IT 경영 관리 핵심 토픽 777번 시험 요약 (IT Management Core Topic 777 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽은 COBIT 2019(거버넌스/관리 목표 40개), ITIL 4(34개 실무 가이드), PMBOK 7(12가지 원칙/8개绩效영역), ISO 38500(거버넌스 국제표준) 4대 프레임워크의 정렬(Align-Plan-Organize, Build-Implement-Operate, Monitor-Evaluate-Assess) 체계를 통해 IT 전략-전술-운영을 End-to-End로 연결하는 통합 거버넌스 체계를 의미한다.
> 2. **가치**: 기업 평균 IT 투자 대비 ROI를 287%(McKinsey 2023)까지 향상시키고, IT 다운타임으로 인한 손실을 시간당 약 50만 달러에서 8만 달러로 84% 절감하며, PMO 운영 성숙도 Level 3 도달 시 프로젝트 성공률을 28%에서 72%로 끌어올린다.
> 3. **판단 포인트**: 중앙집중형 거버넌스(Federal 모델) vs 분산형(Devolved) vs 하이브리드(CobIT) 선택, RACI 매트릭스 작성 시 과도한 책임 중복(Over-Governance)으로 인한 Agile 속도 저하, 그리고 CSF(핵심성공요인) 17개 항목의 정량 KPI 매핑 여부가 기술사 합격의 결정적 변별점이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 IT 경영 관리 영역은 단순 암기형이 아닌, **"프레임워크 간 정렬(Framework Alignment)"** 능력을 평가한다. 2024년 개정 출제기준에 따르면, COBIT 2019의 설계요인(Design Factors) 11개, ITIL 4의 Service Value Chain 6개 활동, PMBOK 7의 8개 프로젝트 성과영역, 그리고 ISO/IEC 38500의 6원칙(책임, 전략, 인수, 성과, 적합, 인적요소)을 상호 매핑할 수 있어야 한다.

과거(2010년대 이전)에는 COBIT 4.1 -> COBIT 5 -> COBIT 2019로 진화하면서 단순 통제 중심(Control Objective)에서 **거버넌스 시스템 + 관리 시스템 + 구성요소(Components) 7개**의 통합 체계로 재설계되었다. ITIL도 ITIL v3(2011) -> ITIL 4(2019)로 전환되며 26 프로세스에서 **34개 실무 가이드** + Service Value System(SVS)로 단순화되었다. 이러한 변화의 핵심 이유는 **클라우드·AI·DevOps 시대**의 Agile/Digital 거버넌스 요구 때문이다.

```text
+---------------------------------------------------------------------+
|            IT 경영 관리 4대 프레임워크 통합 참조 모델                |
+---------------------------------------------------------------------+
|                                                                     |
|   [전략 레이어]                                                     |
|    +--------------------------------------------------+            |
|    |  ISO/IEC 38500 (6원칙) + COBIT 2019 EDM 영역     |            |
|    |  • 책임(R) • 전략(S) • 인수(A) • 성과(P)         |            |
|    |  • EDM01 거버넌스 체계 수립                       |            |
|    |  • EDM02 혜택 보장                                |            |
|    |  • EDM03 위험 최적화                              |            |
|    |  • EDM04 자원 최적화                              |            |
|    |  • EDM05 투명성 보장                              |            |
|    +--------------------------------------------------+            |
|                          | 매핑 (Mapping)                          |
|   [전술 레이어]                                                     |
|    +--------------------------------------------------+            |
|    |  COBIT 2019 APO/BAI 영역 + PMBOK 7 원칙/성과영역 |            |
|    |  • APO12(위험관리) ↔ PMBOK Risk绩效영역           |            |
|    |  • BAI01(프로그램관리) ↔ PMBOK Planning绩效영역   |            |
|    |  • BAI11(품질관리) ↔ PMBOK Quality绩效영역         |            |
|    +--------------------------------------------------+            |
|                          | 정렬 (Alignment)                        |
|   [운영 레이어]                                                     |
|    +--------------------------------------------------+            |
|    |  ITIL 4 Service Value Chain + DevOps Toolchain    |            |
|    |  Plan->Engage->Design&Transition->Obtain/Build       |            |
|    |  ->Deliver&Support->Improve                         |            |
|    |  + 34 Practices (영문 약어 4단계: General/        |            |
|    |   Service Mgmt/Technical Mgmt)                    |            |
|    +--------------------------------------------------+            |
|                          | 피드백 (Feedback Loop)                   |
|   [측정 레이어]                                                     |
|    +--------------------------------------------------+            |
|    |  Balanced Scorecard (BSC) 4관점 + OKR + KPI Tree  |            |
|    |  재무/고객/내부프로세스/학습성장 -> IT Scorecard   |            |
|    |  • Cost of IT Operation, CSAT, MTTR, Velocity    |            |
|    +--------------------------------------------------+            |
|                                                                     |
+---------------------------------------------------------------------+
```

**왜 필요한가?** 삼성SDS, LG CNS, SK C&C 등 국내 SI 기업은 COBIT 2019 인증, CMMI Level 5, ISO 20000, ISO 27001을 동시 보유해야 공공/금융 프로젝트 수의 자격을 얻는다. 또한 2023년 금융감독원의 '금융회사 IT 거버넌스 가이드라인'에 따르면, IT위원회 산하에 **IT리스크관리위원회**를 의무화하고, CRO(Chief Risk Officer) 직위를 별도 임원으로 지정해야 한다. 이처럼 **규제 컴플라이언스**(SOX법, 개인정보보호법, 클라우드 데이터보호법)와 **디지털 전환 가속화**가 동시 진행되는 환경에서, IT 경영 관리는 단순한 비용 관리를 넘어 **전략 자산(Value Realization)**의 핵심 도구로 재정의되었다.

- **📢 섹션 요약 비유**: IT 경영 관리 4대 프레임워크는 마치 **비행기의 관제탑(COBIT), 자동조종장치(ITIL), 정비 매뉴얼(PMBOK), 안전기준(ISO 38500)**이 한 대시보드에 통합된 것과 같다. 기체가 클수록(엔터프라이즈일수록) 4개 시스템의 **동기화(Sync)**가 생존을 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019의 7개 구성요소 시스템(Components of a Governance System)

COBIT 2019는 거버넌스/관리 목표 40개(EDM 5개 + APO 14개 + BAI 11개 + DSS 6개 + MEA 4개)를 달성하기 위해 **7개 구성요소**를 정의한다. 각 구성요소는 **목표 계단(Cascading Goals)** 메커니즘을 통해 Enterprise Goals -> Alignment Goals -> Governance/Management Objectives로 흘러간다.

```text
+-----------------------------------------------------------------+
|                COBIT 2019 목표 계단 (Goals Cascade)              |
+-----------------------------------------------------------------+
|                                                                 |
|  [Level 0] Enterprise Goals (13개)                              |
|      EG01 포트폴리오 경쟁제품/서비스 수익                       |
|      EG03 비용 최적화 / EG05 고객 만족도 / EG08 디지털 트랜스    |
|      EG11 IT 운영 디스ruption 최소화 / EG13 제품 혁신            |
|                  |                                              |
|                  v (1:N 매핑)                                   |
|  [Level 1] Alignment Goals (13개)                               |
|      AG01 IT 준법성 / AG02 IT 거버넌스 / AG04 자원 관리         |
|      AG06 Agile 적합성 / AG09 정보 처리 혁신                    |
|      AG12 IT-enabled 투자 프로그램 가치 실현                     |
|                  |                                              |
|                  v (1:M 매핑)                                   |
|  [Level 2] Governance/Management Objectives (40개)              |
|      EDM05 투명성 보장 / APO12 위험 관리 / BAI11 품질 관리      |
|      DSS02 서비스 요청/사고 관리 / MEA01 성과/준법 모니터링     |
|                  |                                              |
|                  v (M:N)                                        |
|  [Level 3] Component: Process / People / Structure / Flow       |
|            Information / Skills/Infrastructure / Policies       |
|                                                                 |
|  +--------------- 7개 구성요소 (Components) -------------+     |
|  | ① Process(40개 활동)  ② Organizational Structure       |     |
|  | ③ Information Flows  ④ People, Skills, Competencies   |     |
|  | ⑤ Policies & Procedures  ⑥ Culture, Ethics, Behavior  |     |
|  | ⑦ Services, Infra, Applications                       |     |
|  +--------------------------------------------------------+     |
|                                                                 |
+-----------------------------------------------------------------+
```

### 2. ITIL 4의 Service Value System(SVS)

ITIL 4는 **Opportunity/Demand -> Value** 변환 체계를 SVS로 표현한다. 핵심은 **Service Value Chain(SVC)** 6개 활동과 **Guiding Principles** 7개(Focus on value, Start where you are, Progress iteratively with feedback, Collaborate and promote visibility, Think and work holistically, Keep it simple and practical, Optimize and automate)다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Guiding Principles (7개)** | 의사결정 원칙 | 조직 문화·전략 수준에서 모든 의사결정 시 적용. "Start where you are"는 AS-IS 분석 후 변화 |
| **Governance (조직 거버넌스)** | 방향성 설정 |董事会 -> 전략 -> 포트폴리오 -> 가치흐름 감독 |
| **Service Value Chain (SVC 6개)** | 가치 창출 동적 체인 | **Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve**. 각 활동은 다중 입력/출력 가능 |
| **Practices (34개)** | 실무 가이드 | **General Mgmt(3)**: 전략·포트폴리오·재무·위험·구조·워크포스·지속가능성·컴플라이언스·조직변화. **Service Mgmt(17)**: 비즈니스분석, 서비스설계, 변경관리, 사고관리, 문제관리 등. **Technical Mgmt(14)**: 배포, 모니터링/이벤트, SRE 등 |
| **Continual Improvement (CI)** | 끊임없는 개선 | 7단계 모델(What is the vision?->Where are we now?->Where do we want to be?->How do we get there?->Take action->Did we get there?->How do we keep the momentum?) |

### 3. PMBOK 7의 Project Performance Domains(8개)

PMBOK 6th(5 Process Groups + 10 Knowledge Areas) -> PMBOK 7th(**12 Principles of Project Management** + **8 Performance Domains** + **Tailoring** + **Models, Methods, Artifacts**)로 패러다임 전환되었다. **Process-based -> Principle-based**로 진화한 이유는 예측형(Plan-driven)과 적응형(Agile/Hybrid)을 통합하기 위함이다.

| Performance Domain | 핵심 목표 | 연관 Framework |
| :--- | :--- | :--- |
| **Stakeholder** | 이해관계자 참여·기대 관리 | RACI 매트릭스, Stakeholder Engagement Plan |
| **Team** | 팀 역량·협업 | Tuckman(Forming-Storming-Norming-Performing-Adjourning), Servant Leadership |
| **Development Approach** | 예측형/적응형/하이브리드 선택 | MoSCoW, Kano Model |
| **Planning** | 범위·일정·비용·자원 통합 | WBS, Critical Path Method, Rolling Wave Planning |
| **Project Work** | 물리적/디지털 산출물 생성 | Kanban WIP Limit, Cumulative Flow Diagram |
| **Delivery** | 스코프/품질/리스크 균형 | Definition of Done, Risk Burndown |
| **Measurement** | 정량적 성과 추적 | EVM(Earned Value), SPI/CPI, Velocity |
| **Uncertainty** | 모호성·복잡성·변동성 관리 | Cynefin(Simple-Complicated-Complex-Chaotic), OODA Loop |

### 4. ISO/IEC 38500:2015의 6원칙과 거버넌스 모델

ISO 38500은 이사회 수준의 IT 거버넌스 국제표준으로, **3개 작업(평가-지휘-모니터링, Evaluate-Direct-Monitor)**과 **6원칙**을 정의한다. COBIT 2019 EDM 영역과 직접 매핑된다.

```text
+----------------------------------------------------------+
|         ISO 38500 PDCA + EDM 통합 사이클                  |
+----------------------------------------------------------+
|                                                          |
|    +-------- PLAN --------+                              |
|    |  Evaluate (평가)      |  <- EDM01/02/03/04/05       |
|    |  - 6원칙 적용 점검    |                              |
|    |  - 책임(R): 개인·집단 |                              |
|    |  - 전략(S): 비즈니스  |                              |
|    |  - 인수(A): 의사결정  |                              |
|    |  - 성과(P): 서비스    |                              |
|    |  - 적합(C): 규정준수  |                              |
|    |  - 인적(H): 역량·문화 |                              |
|    +----------+-----------+                              |
|               v                                          |
|    +-------- DO ---------+                              |
|    |  Direct (지휘)        |  <- APO/BAI 영역             |
|    |  - 정책·할당·위임     |                              |
|    |  - 자원 배분·우선순위 |                              |
|    +----------+-----------+                              |
|               v                                          |
|    +------- CHECK -------+                              |
|    |  Monitor (모니터링)   |  <- DSS/MEA 영역             |
|    |  - KPI 측정·보고     |                              |
|    |  - 내부감사·이사회보고|                              |
|    +----------+-----------+                              |
|               v                                          |
|    +------- ACT ---------+                              |
|    |  Review & Improve    |  <- ITIL Continual Improvement|
|    |  - Gap 분석·시정조치 |                              |
|    +----------------------+                              |
|                                                          |
+----------------------------------------------------------+
```

### 5. 핵심 정량 파라미터 및 알고리즘

**EVT(Earned Value Technique) 핵심 공식**:
- `EV(BCWP) = 계획완료률 × BAC(Budget at Completion)`
- `CV(원가편차) = EV - AC` -> 양수 시 예산 절감
- `SV(일정편차) = EV - PV` -> 양수 시 일정 단축
- `CPI(원가성과지수) = EV / AC` -> 1.0 이상 정상
- `SPI(일정성과지수) = EV / PV` -> 1.0 이상 정상
- `EAC(완료시예상비용) = BAC / CPI`
- `VAC(완료시편차) = BAC - EAC`
- **TCPI(완료지수) = (BAC - EV) / (BAC - AC)`** -> 남은 작업을 위해 필요한 효율

**IT 투자 분석 5대 기법**:
1. **NPV(순현재가치)**: `NPV = Σ[CFt / (1+r)^t] - I0` ->
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 777 / 800

<- **이전**: [776. IT 경영 관리 핵심 토픽 776번 시험 요약](/studynote/12_it_management/05_security_compliance/776_it_management_core_topic_776_exam_summary/)
**다음**: [778. IT 경영 관리 핵심 토픽 778번 시험 요약](/studynote/12_it_management/05_security_compliance/778_it_management_core_topic_778_exam_summary/) ->

---
