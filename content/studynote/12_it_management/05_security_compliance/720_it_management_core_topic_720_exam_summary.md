---
title: "720. IT 경영 관리 핵심 토픽 720번 시험 요약 (IT Management Core Topic 720 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019, ISO 38500)와 IT 서비스 관리(ITIL 4) 프레임워크의 통합적 적용을 통해 기업의 IT 자산을 전략적 비즈니스 가치로 전환하는 경영 메커니즘으로, EDM(Evaluate-Direct-Monitor) 40개 Govern/Manage Practice와 34개 ITIL Practice의 체계적 매핑이 핵심
> 2. **가치**: 정량적 성과로 IT 투자 대비 ROI 평균 25~40% 개선, IT 운영 비용 15~30% 절감, 인시던트 MTTR 50% 단축, 정성적 가치로 비즈니스-IT 정렬도(Business-IT Alignment Maturity) Level 3->5 도달, 이사회 수준 의사결정 투명성 확보
> 3. **판단 포인트**: 프레임워크 선택 시 조직 성숙도(COBIT PAM 5단계)와 산업 규제 요건(금융·공공), 거버넌스-관리-운영 3계층 분리 vs. 통합 운영 모델 선택, Agile/DevOps 문화와의 충돌 시 RACI 매트릭스 재설계, 그리고 RACI·RACI-VS·RASCI 등 책임 구조 모델의 프로젝트 단계별 동적 적용

---

## Ⅰ. 개요 및 필요성

정보화 사업의 규모가 연간 수천억 원에 이르고 클라우드·AI·데이터 거버넌스 등 신기술 도입이 가속화되면서, IT 부서가 단순 비용 센터(Cost Center)에서 가치 창출 센터(Value Center)로 전환되어야 하는 경영적 요구가 본격화되었습니다. 과거 ISO/IEC 38500(2008) 발표 이후 2015년 개정판을 거쳐, 2018년 COBIT 2019가 출시되면서 거버넌스와 관리 영역이 명확히 분리되었고, 2019년 ITIL 4의 Service Value System(SVS)이 도입되어 운영 영역까지 End-to-End로 연결되는 통합 프레임워크 시대가 열렸습니다.

특히 2024년 DORA(Digital Operational Resilience Act)·AI Act·ISMS-P 인증제 등 규제 환경이 강화됨에 따라, IT 투자 포트폴리오 관리(IT Portfolio Management), 정보화 사업 감리, EA(Enterprise Architecture) 정합성 검증이 단순 컴플라이언스를 넘어 사업 지속성(Business Continuity)의 핵심 요소로 부상하고 있습니다.

```text
+-----------------------------------------------------------------+
|           IT 경영관리 통합 프레임워크 (Topic 720)                |
+-----------------------------------------------------------------+
|                                                                 |
|   +--------------+    +--------------+    +--------------+    |
|   |   이사회     |---->|   CISO/CDO   |---->|  IT 운영조직 |    |
|   | (거버넌스)   |    |   (관리)     |    |   (운영)     |    |
|   +------+-------+    +------+-------+    +------+-------+    |
|          |                   |                   |              |
|          v                   v                   v              |
|   +--------------+    +--------------+    +--------------+    |
|   |  ISO 38500   |    |  COBIT 2019  |    |   ITIL 4     |    |
|   | (6 Principles)|    | (40 Practice)|    | (34 Practice)|    |
|   +------+-------+    +------+-------+    +------+-------+    |
|          |                   |                   |              |
|          +-------------------+-------------------+              |
|                              v                                  |
|                    +------------------+                         |
|                    |  비즈니스 가치   |                         |
|                    | (Value Creation) |                         |
|                    +------------------+                         |
|                                                                 |
+-----------------------------------------------------------------+

  기존 패러다임 vs 신 패러다임 비교
  +------------------+------------------+------------------+
  |      구분        |   기존 (2000s)    |   현재 (2020s)   |
  +------------------+------------------+------------------+
  | IT 부서 역할     | 비용 센터         | 가치 창출 센터   |
  | 거버넌스 모델    | 폐쇄적·단편적     | 개방형·통합형    |
  | 의사결정 주체    | CIO 독단          | 이사회+CIO+CDO   |
  | 위험 관리        | 사후 대응         | 사전 예방·내재화 |
  | 프레임워크       | ITIL v3 단독      | COBIT+ITIL+ISO  |
  | 평가 방식        | 재무 KPI 위주     | 균형성과표(BSC)  |
  +------------------+------------------+------------------+
```

한국 정보화진흥원(KA)의 2023년 조사에 따르면 국내 대기업 중 COBIT 기반 IT 거버넌스를 전면 도입한 비율은 약 23%이며, ITIL 4 기반 프로세스 성숙도 평균은 Level 2.8로 글로벌 평균(3.4) 대비 낮은 수준입니다. 이는 본 주제가 단순 암기 과목이 아닌, **"우리 조직의 IT 경영 진단·개선 솔루션 제시"**를 요구하는 기술사 논술의 핵심 사례 분석 영역임을 의미합니다.

- **📢 섹션 요약 비유**: IT 경영관리는 자동차의 계기판, 엔진, 핸들, 브레이크, GPS가 통합된 **운전 시스템**과 같습니다. COBIT은 방향을 정하는 **GPS**, ITIL은 매끄러운 주행을 보장하는 **엔진·브레이크 시스템**, ISO 38500은 법규·안전 기준을 지키는 **교통법**, 그리고 EA는 도로 지도입니다. 이 중 하나라도 없으면 목적지 도달이 어렵습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **3계층(거버넌스-관리-운영) × 5관점(Benefits realization, Risk optimization, Resource optimization, Transparency, Compliance)** 구조의 체계적 운영입니다. COBIT 2019의 Governance System은 40개의 Govern/Manage Practice로 구성되며, 각 Practice는 Input -> Activity -> Output의 Activity Model을 따릅니다.

```text
+-----------------------------------------------------------------+
|       COBIT 2019 Governance & Management Objectives            |
|                  (5 Domains, 40 Objectives)                     |
+-----------------------------------------------------------------+
|                                                                 |
|  +----------------------------------------------+              |
|  |  EDM (Evaluate, Direct, Monitor) - 5개      | <--- 거버넌스 |
|  |  • EDM01 Ensured Governance Framework        |              |
|  |  • EDM02 Ensured Benefits Delivery           |              |
|  |  • EDM03 Ensured Risk Optimization           |              |
|  |  • EDM04 Ensured Resource Optimization       |              |
|  |  • EDM05 Ensured Stakeholder Transparency    |              |
|  +----------------------------------------------+              |
|                          |                                      |
|  +----------------------+------------------------+            |
|  |  APO (Align, Plan, Organize) - 14개           |            |
|  |  BAI (Build, Acquire, Implement) - 11개       | <--- 관리    |
|  |  DSS (Deliver, Service, Support) - 6개       |            |
|  |  MEA (Monitor, Evaluate, Assess) - 4개       |            |
|  +----------------------------------------------+              |
|                          |                                      |
|  +----------------------+------------------------+            |
|  |  ITIL 4 SVS (Service Value System)            |            |
|  |  • 7 Guiding Principles                        |            |
|  |  • 4 Dimensions (Organizations, People,        | <--- 운영   |
|  |    Information, Technology, Partners, Flows)   |            |
|  |  • 34 Practices (General, Service, Technical)  |            |
|  |  • Service Value Chain (Plan->Engage->Design    |            |
|  |    ->Obtain->Build->Transition->Operate)          |            |
|  +----------------------------------------------+              |
|                                                                 |
+-----------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/IT 전략위원회** | 최종 거버넌스 의사결정, IT 투자 승인, 위험 한도 설정 | ISO 38500 Model(Direct-Monitor) 적용, RACI 매트릭스에서 **A(Accountable)** 역할, 연 4회 정례 회의 + 수시 전략 회의 |
| **COBIT 2019 Core Model** | 40개 Practice의 Activity/Metric 매핑, Governance Component(Process, Organizational Structure, Information Flow, People, Skills, Competencies, Policies, Culture) 7요소 통합 | Design Factors 11개(Strategy, Goals, Risk Profile, etc.) 기반 조직 맞춤 설계, **Cascade Goals**: Enterprise Goals(13) -> Alignment Goals(13) -> Management Objectives(40) -> Process Goals 계층 매핑 |
| **ITIL 4 SVS** | 서비스 가치 사슬(Value Chain)을 통한 Op(Model)->Plan->Engage->Design->Transition->Operate의 End-to-End 흐름 | **4 Dimensions Model**: 조직·사람, 정보·기술, 파트너·공급사, 가치사슬·활동 흐름, **Guiding Principles 7개**: Focus on value, Start where you are, Progress iteratively, Collaborate, Think holistically, Keep it simple, Optimize & automate |
| **ISO/IEC 38500:2015** | IT 거버넌스의 국제 표준 프레임워크, 6 Principles(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) 기반 이사회 책임 명시 | **Governance Model 3단계**: Evaluate(평가) -> Direct(지시) -> Monitor(모니터링), PDCA(Plan-Do-Check-Act)와 결합하여 지속적 개선, **Maturity Model**로 5단계 성숙도 평가 (ISO/IEC TS 33030 기반) |
| **EA(Enterprise Architecture)** | TOGAF ADM(Architecture Development Method) 8단계 + Zachman Framework 6×6 매트릭스로 비즈니스·데이터·애플리케이션·기술 정렬 | **ADM Phases**: Preliminary -> Vision -> Business Architecture -> Information Systems Architecture -> Technology Architecture -> Opportunities & Solutions -> Migration Planning -> Implementation Governance, **Architecture Repository**(Architecture MetaModel, Architecture Capability, Architecture Landscape) |
| **BSC(Balanced Scorecard)** | IT 성과 측정을 4관점(재무, 고객, 내부프로세스, 학습과 성장)으로 균형 평가 | **IT BSC 4관점 KPI 예시**: 재무(ROI, TCO), 고객(서비스 만족도 NPS), 내부 프로세스(인시던트 해결률, 변경 성공률), 학습·성장(직원 역량 지수, 혁신 프로젝트 수), Norton-Kaplan의 Strategy Map으로 인과관계 시각화 |

**핵심 알고리즘·수식·파라미터**:

1. **COBIT 2019 PAM(Performance Assessment Model)**: Process Capability = (F(process performance), PA(plan attribute)1~5) -> 6단계 성숙도(Level 0: Incomplete ~ Level 5: Optimizing), 각 Process Activity별로 **Base Practice × Generic Work Product × Practice Indicator** 3요소 평가
2. **IT 투자 ROI 산출**: `ROI = (총 이익 - 총 비용) / 총 비용 × 100(%)`, NPV(Net Present Value) `= Σ [CFt / (1+r)^t] - 초기투자`, IRR(Internal Rate of Return) `= Σ [CFt / (1+IRR)^t] = 0`을 만족하는 할인율
3. **IT 포트폴리오 시각화**: BCG Matrix 4사분면(Stars, Cash Cows, Question Marks, Dogs) + **McFarlan Strategic Grid**(High Impact-Current vs. High Impact-Future) + **Ward & Peppard IS/IT Portfolio Matrix**(Operational, Strategic, High Potential, Support) 3×3 매트릭스
4. **COSO ERM + ISO 31000 위험 평가**: Risk = Likelihood × Impact × Velocity(속도), 5×5 매트릭스로 정량화, **Risk Appetite(위험 수용 성향)**와 **Risk Tolerance(허용 한계)** 차이로 경영 의사결정 기준 명시
5. **RACI 매트릭스 변형**: 표준 RACI(Responsible, Accountable, Consulted, Informed) + **RACI-VS**(V=Verifies, S=Sign-off, 정부 IT 사업 감리에서 사용) + **RASCI**(S=Supports, 정보화 사업 발주처·수급사 공동 책임 구조) + **DACI**(Driver, Approver, Contributor, Informed, 의사결정 중심)
6. **TCO(Total Cost of Ownership) 산정**: `TCO = 직접비(HW/SW/Network) + 간접비(인건비, 교육, 유지보수, 다운타임 비용)`, Gartner 모델 기준 5년 TCO에서 HW 27%, SW 17%, 운영인력 41%, 다운타임 11%, 교육 4%

- **📢 섹션 요약 비유**: COBIT의 5개 도메인은 **병원 시스템**으로 비유할 수 있습니다. EDM(거버넌스)은 **이사회·의료 자문 위원회**, APO(계획/조직)는 **진료과·행정실**, BAI(구축/도입)는 **의료 장비·시설 부서**, DSS(서비스/지원)는 **응급실·입원실**, MEA(모니터링/평가)는 **QI(Quality Improvement)팀**에 해당합니다. 각 영역이 분리되어 작동하되, 환자(비즈니스 가치) 중심으로 통합되어야 합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 체계 | IT 서비스 관리 운영 | 이사회 거버넌스 표준 | 프로젝트 관리 방법론 |
| **적용 계층** | 거버넌스 + 관리 | 관리 + 운영 | 거버넌스 (이사회) | 프로젝트 실행 |
| **핵심 구조** | 40 Objective, 7 Component | 34 Practice, SVS | 6 Principles, 3 Model | 12 Principle, 8 Domain |
| **성숙도 모델** | PAM (0~5 Level, ISO 33030) | Maturity Model (4단계) | 5단계 평가 모델 | OPM3 (5단계) |
| **프로세스 수** | 40 (Govern 5 + Manage 35) | 34 (General 14 + Service 17 + Tech 3) | 6 Principle 기반 | 49 Process (PMBOK 6) -> 12 Principle + 8 Domain (PMBOK 7) |
| **위험 관리** | EDM03 + APO12 (Risk Mgmt) | RCV(공급·계약·위험) Practice | Principle 3(Conformance) + 5(Human Behavior) | Plan Risk Management, Identify, Analyze, Plan Responses, Implement, Monitor |
| **Value 측정** | Goals Cascade + Metrics | Value Stream + SVS | Performance Principle(4) | Benefits Realization Mgmt Domain |
| **Agile 적합도** | 중간 (Design Factor로 조정) | 높음 (7 Guiding Principles) | 낮음 (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 720 / 800

<- **이전**: [719. IT 경영 관리 핵심 토픽 719번 시험 요약](/studynote/12_it_management/05_security_compliance/719_it_management_core_topic_719_exam_summary/)
**다음**: [721. IT 경영 관리 핵심 토픽 721번 시험 요약](/studynote/12_it_management/05_security_compliance/721_it_management_core_topic_721_exam_summary/) ->

---
