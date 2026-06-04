+++
title = "682. IT 경영 관리 핵심 토픽 682번 시험 요약 (IT Management Core Topic 682 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 682번은 **COBIT 2019 거버넌스 체계, ITIL v4 서비스 가치 체계, PMBOK 7th 프로젝트 관리, ISO 27001/20000 인증 체계, BSC 전략맵**을 통합한 **"거버넌스-전략-서비스-프로젝트-리스크" 5축 통합 관리 프레임워크**의 설계·운영·측정 역량을 평가하는 시험영역이다.
> 2. **가치**: 조직의 IT 투자 대비 성과(ROI/VOI)를 **BSC 4관점(재무·고객·내부프로세스·학습성장)**으로 정량 측정하고, **COBIT 2019의 40개 관리목표와 5개 도메인(EDM/APO/BAI/DSS/MEA)**을 통해 거버넌스 성숙도를 Level 1~5로 정량 평가하여, IT 부서의 단순 비용센터->**가치 창출형 파트너** 전환을 가능하게 한다.
> 3. **판단 포인트**: **"거버넌스(누가 결정) vs 관리(누가 실행)"**의 분리, **"스탠다드(COBIT/ITIL/PMBOK) vs 컨텍스트(업종·규모·규제)"**의 적용, **"단기 ROI vs 장기 VOI"**의 균형, **"중앙화(CoE) vs 분권화(Federation)"** 거버넌스 모델의 trade-off가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 급격한 확산과 디지털 전환(DX)의 가속화로 인해, IT는 단순 지원 기능에서 **경영 전략의 핵심 동력**으로 변화했다. 그러나 한국 기업의 68%(2024 KISA 실태조사 기준)가 **"IT 투자 성과 미흡"**을 호소하며, 그 원인의 72%가 **"IT 거버넌스 부재 및 전략-사업-IT 정렬 실패"**로 분석된다. 이에 682번 시험 영역은 IT 경영 관리의 핵심 토픽을 종합적으로 평가하여, **전략적 IT 리더십(Strategic IT Leadership)**을 갖춘 전문가를 검증한다.

```text
+---------------------------------------------------------------------+
|        IT 경영 관리 5축 통합 프레임워크 (682번 핵심 토픽)              |
+---------------------------------------------------------------------+
|                                                                       |
|   [1] 거버넌스 축        [2] 전략 축          [3] 서비스 축             |
|   +----------+         +----------+         +----------+            |
|   |  COBIT   |◄-------►| BSC/CSF  |◄-------►|  ITIL v4 |            |
|   |  2019    |         | 전략맵   |         | SVS 체계 |            |
|   +----+-----+         +----+-----+         +----+-----+            |
|        |                    |                     |                   |
|        +--------------------+---------------------+                  |
|                             v                                         |
|                    [4] 프로젝트 축        [5] 리스크/보안 축            |
|                    +----------+         +----------+                  |
|                    | PMBOK 7  |◄-------►|ISO27001/ |                  |
|                    | PRINCE2  |         |20000/    |                  |
|                    +----------+         | ISO31000 |                  |
|                                          +----------+                  |
+---------------------------------------------------------------------+
         |                |                  |                |
         v                v                  v                v
   +----------+    +----------+      +----------+    +----------+
   | 이사회/   |    | CIO/CTO  |      | 서비스   |    | CISO/    |
   |감사위    |    | 전략실    |      |데스크    |    | 컴플라이 |
   |(Decision)|    |(Planning)|    |(Operate) |    |(Protect)  |
   +----------+    +----------+      +----------+    +----------+
```

**과거 패러다임 대비 변화의 핵심**:
- **1990년대**: IT=비용센터(COST CENTER), CapEx 중심, 개별 시스템 단위 관리 -> **2020년대**: IT=가치센터(VALUE CENTER), OpEx+SaaS 구독모델, 플랫폼 기반 통합 관리
- **2010년대**: ITIL v3(2011, 26개 프로세스, 5단계 Lifecycle) -> **2018년~**: ITIL v4(34개 Practice, 7개 guiding principle, SVS(Service Value System))
- **2012년**: COBIT 5(5개 원칙, 7개 Enabler, 37개 프로세스) -> **2018년~**: COBIT 2019(40개 관리목표, 5개 도메인, Focus Area 도입)
- **프로젝트 관리**: 폭포수(Waterfall) 95% -> 애자일/하이브리드 73%(PMI 2024 Pulse)

- **📢 섹션 요약 비유**: IT 경영 관리는 **배의 선장(거버넌스), 항해사(전략), 기관장(서비스), 정비사(프로젝트), 보안요원(리스크)**이 각자 역할하면서도 **하나의 배**(조직)를 목적지(경영 목표)로 이끄는 **5인조 항해 시스템**과 같다. 682번 시험은 이 5인조가 각자 무엇을 알고 있어야 하는지를 묻는 종합 시험이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 682번의 핵심은 **"Strategy->Governance->Service->Project->Risk"**로 이어지는 **인과적 연쇄 모델(Causal Chain Model)**이다. 이 모델에서 한 축이 무너지면 전체 시스템이 흔들리는 **"약한 고리(Weakest Link)"** 원리가 적용된다.

```text
+-------------------------------------------------------------------+
|         682번 시험의 핵심 인과 모델: Strategy-Service Chain         |
+-------------------------------------------------------------------+

  [비즈니스 전략]
       |
       | ① 전략 정렬(Strategic Alignment) Henderson-Henderson 모델
       |   (Business Strategy <--> IS Strategy <--> IT Strategy)
       v
  [IT 거버넌스] ---- COBIT 2019 EDM(평가/지시/모니터링) --► 이사회
       |
       | ② 목표 계층화(Cascading Goals)
       |   Enterprise Goals(13개) -> Alignment Goals(13개) -> Goals
       |   Cascading을 통해 BSC 4관점과 자동 매핑
       v
  [IT 서비스/프로젝트]
       |
       | ③ 가치 창출(Value Creation)
       |   - Service Value Chain(SVC): Plan->Engage->Design&Transition
       |     ->Obtain/Build->Deliver&Support->Improve
       |   - 7 Guiding Principles: Focus on value, Start where you are,
       |     Progress iteratively, Collaborate, Think holistically,
       |     Keep it simple, Optimize
       v
  [성과 측정]
       |
       | ④ KPI 계층화(BSC + GQM + OKR)
       |   L1(전략) - L2(전술) - L3(운영) - L4(개인)
       v
  [피드백/학습] -> 거버넌스로 환류 -> Continuous Improvement
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (COBIT 2019)** | 의사결정 권한·책임·통제의 구조화 | **5개 도메인**: EDM(Evaluate/Direct/Monitor, 5개 관리목표) -> APO(Align/Plan/Organize, 14개) -> BAI(Build/Acquire/Implement, 11개) -> DSS(Deliver/Service/Support, 6개) -> MEA(Monitor/Evaluate/Assess, 4개). **40개 관리목표(Management Objective)**를 **능숙도(Rate 0~5)**와 **목표수행수준(NLR 0~100%)**의 2축 매트릭스로 평가. **Design Factors 11개**(전략, 목표, 리스크, 우려사항, 역할, IT 이슈, 위협, 규제, 기술, 산업, 조직)로 컨텍스트 맞춤 설계 |
| **서비스 가치 체계 (ITIL v4 SVS)** | IT 서비스의 end-to-end 가치 흐름 | **SVS 구성**: Opportunity/Demand -> Value(UTIL/OUTCOME/RISK) <- Guiding Principles(7개) <- Governance <- Practices(34개) <- Service Value Chain(6단계) <- **Continual Improvement**(7단계 모델: What is the vision? -> Where are we now? -> Where do we want to be? -> How do we get there? -> Did we get there? -> How do we keep the momentum? -> 34 Practice 평가). **34개 Practice**: 14개 일반관리(Strategy, Portfolio, Workforce, Architecture, Software Dev 등) + 17개 서비스관리(Incident, Problem, Change Enablement, Service Desk 등) + 3개 기술관리(Deployment, Infra/Platform, Software Dev) |
| **프로젝트 관리 (PMBOK 7th)** | 일회성 업무의 성공적 수행 | **8개 Performance Domain**: Stakeholder, Team, Development Approach & Life Cycle, Planning, Project Work, Delivery, Measurement, Uncertainty. **12개 Principle**(Stewardship, Team, Development Approach, Planning, Managing Uncertainty, etc.). **Value Delivery System** 중심: 프로젝트는 **"예측형(50%까지 감소 추세), 애자일(73% 채택), 하이브리드(47% 병행)"** 중 컨텍스트에 맞게 선택. **Earned Value Management(EVM)**: CPI(비용 성과 지수) = EV/AC, SPI(일정 성과 지수) = EV/PV, TCPI = (BAC-EV)/(BAC-AC) |
| **리스크/보안 관리 (ISO 31000/27001/20000)** | 불확실성의 정량적 통제 | **ISO 31000**: Risk = Likelihood × Impact (5×5 매트릭스), Risk Appetite(전사 수용한도) -> Risk Tolerance(개별 한도). **ISO 27001:2022**: 93개 통제항목(Annex A), 4개 테마(Organizational 37, People 8, Physical 14, Technological 34). **ISO 20000-1:2018**: 26개 프로세스 요구사항. **3 Lines Model(IIA 2020)**: 1st Line(운영 자기통제) / 2nd Line(리스크/컴플) / 3rd Line(내부감사) |
| **전략 정렬/측정 (BSC + Strategy Map)** | 전략의 시각화·계량화·연결 | **BSC 4관점**: Financial(ROI, EVA) / Customer(NPS, CSAT) / Internal Process(Lead Time, Defect Rate) / Learning & Growth(직원 역량 지수). **Strategy Map**: 학습성장->내부프로세스->고객->재무의 **인과 흐름** 도식화. **Theme-based BSC**(Operational Excellence, Customer Intimacy, Product Leadership) |
| **EA(Enterprise Architecture)** | 비즈니스-IT 정렬의 청사진 | **TOGAF 10(2022)**: ADM(Architecture Development Method) 8단계 Phase A(Architecture Vision) -> B(Business) -> C(IS) -> D(Technology) -> E(Opportunities) -> F(Migration Planning) -> G(Implementation) -> H(Architecture Change Management) -> **Requirements Management**(전 단계 반복). **Zachman Framework**: 6×6 매트릭스(What/How/Where/Who/When/Why × Planner/Owner/Designer/Builder/Subcontractor/Functioning Enterprise) |

**핵심 알고리즘/공식/평가 기법**:

1. **COBIT 2019 능력수준 평가 (ISO/IEC 15504 PAM)**: 6단계(0: Incomplete ~ 5: Optimizing). **Process Attribute Rating**: PA 1.1(Process Purpose Achieved) ~ PA 5.2(Process Innovation). 한 단계 상승에 평균 **12~18개월** 소요.
2. **EV(원가가치) 계산**: EV = (% 완료) × BAC(Budget At Completion). CV = EV - AC(긍정=저비용 실행). SV = EV - PV(긍정=일정 앞당김).
3. **서비스 가치 공식 (ITIL v4)**: **Value = Utility(적합성) + Warranty(보증) − Risk(위험) − Cost(비용)**. Utility는 "무엇을 하는가(What it does)", Warranty는 "얼마나 잘 하는가(How well it does)".
4. **리스크 정량화 (FAIR 모델)**: Risk = ALE(Annual Loss Expectancy) = SLE(Single Loss Expectancy) × ARO(Annual Rate of Occurrence). SLE = AV(Asset Value) × EF(Exposure Factor).
5. **CSF(Critical Success Factor) -> KPI -> KGI 인과 체인**: CSF("고객만족도 향상") -> KPI("콜센터 평균 응답시간 ≤ 20초") -> KGI("고객 이탈률 5% 이하").

- **📢 섹션 요약 비유**: 이 5축은 **자동차의 5대 시스템**과 같다. **거버넌스=핸들(방향·의사결정), 전략=내비게이션(목적지), 서비스=엔진(동력), 프로젝트=바퀴(구현), 리스크=안전벨트+에어백(보호)**. 어느 하나라도 없으면 차는 목적지에 안전히 도달할 수 없다.

---

## Ⅲ. 비교 및 연결

682번 시험은 서로 다른 프레임워크 간의 **경계·중복·연동**을 정확히 아는 것을 요구한다. 특히 혼동하기 쉬운 영역을 명확히 구분해야 한다.

| 구분 | **COBIT 2019** | **ITIL v4** | **PMBOK 7th** | **ISO 27001/20000** | **BSC** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 초점** | 거버넌스·컴플라이언스·리스크 (GCR) | 서비스 운영·가치 흐름 | 프로젝트 단위 일회성 업무 | 통제 항목·인증 체계 | 전략 성과 측정 |
| **적용 계층** | 전사(Board) | 운영/서비스데스크 | 프로젝트 단위 | 통제 환경 | 전사(전략실) |
| **주 사용자** | CIO, 이사회, 내부감사 | 서비스 매니저, ITIL 실무자 | PMO, 프로젝트 매니저 | CISO, 컴플라이언스 | CEO, CFO, 전략기획 |
| **성숙도/측정 모델** | 능력수준 0~5, NLR 0~100% | 34 Practice 5단계 | Performance Domain 5단계 | Annex A 93 통제 준수율 | 4관점 BSC 전략맵 |
| **프로세스 수** | 40개 관리목표 (5도메인) | 34개 Practice (6 Value Chain) | 8 Performance Domain + 12 Principle | 93 통
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 682 / 800

<- **이전**: [681. IT 경영 관리 핵심 토픽 681번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/681_it_management_core_topic_681_exam_summary/)
**다음**: [683. IT 경영 관리 핵심 토픽 683번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/683_it_management_core_topic_683_exam_summary/) ->

---
