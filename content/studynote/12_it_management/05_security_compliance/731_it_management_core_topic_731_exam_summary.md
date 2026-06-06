---
title: "IT Management Core Topic 731 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 731번은 **COBIT 2019·ITIL 4·ISO/IEC 38500** 등 거버넌스 프레임워크를 **EA(Enterprise Architecture)**와 **IT 포트폴리오 관리(ITPM)**로 통합·운용하며, 정보화 투자에 대한 **TCO·ROI·NPV·BSC** 기반 의사결정 체계를 구축하는 영역이다.
> 2. **가치**: 정량적 성과로 **정보화 투자 회수기간 30~40% 단축**, IT 서비스 가용성 **99.95% 이상**, 거버넌스 성숙도 Level 3->5 향상(통상 18~24개월), 그리고 **컴플라이언스 위반 건수 70% 감소**를 통한 리스크 통제력 확보가 가능하다.
> 3. **판단 포인트**: **중앙집중형(Centralized) vs 분산형(Federated) 거버넌스**, **Build vs Buy vs Cloud(Buy-as-a-Service)**, **BSC 4관점 균형**, **In-house vs Outsourcing vs Insourcing-Reverse**, 그리고 **COBIT 2019 Focus Area 선택**(예: DevOps, Cybersecurity, Privacy) 시 **조직 성숙도(Process Assessment Model, PAM)**와 **전략적 목표 정렬**이 핵심 trade-off이다.

---

## Ⅰ. 개요 및 필요성

정보시스템 감리·컨설팅 실무에서 반복적으로 마주치는 문제는 "IT 부서가 비용센터로 전락", "투자 대비 효과 불명확", "규제·컴플라이언스 실패", "서비스 품질의 비가시성"이다. 731번 토픽은 이러한 문제를 **거버넌스(Governance) -> 전략(Strategy) -> 운영(Operation) -> 측정(Measurement)**의 4계층으로 분해해, **이사회-경영진-IT** 간의 **RACI 매트릭스**, **Value Office(밸류오피스)**, **PPM(Project Portfolio Management)** 체계를 통해 정량적 의사결정과 책임 구조를 확립하는 데 목적이 있다.

기존 패러다임은 1990년대 말~2000년대 초 **COBIT 4/5 기반 프로세스 중심**, ITIL v2/v3 **함수(Function) 중심**, 그리고 **물리적 데이터센터 기반 CapEx 중심 투자**였다. 그러나 2020년대를 기점으로 **클라우드 우선(Cloud-First)**, **FinOps**, **SaaS·PaaS 기반 OpEx 모델**, **Agile·DevSecOps**, **AI 거버넌스**, 그리고 **ESG·디지털 윤리**가 등장하면서 프레임워크의 갱신 주기가 짧아졌고(예: COBIT 5 -> 2019, ITIL v3 -> 4, ISO 38500:2015 -> 2024 개정안), **연속적 거버넌스(Continuous Governance)** 관점이 요구되고 있다.

```text
+------------------------------------------------------------------------+
|          731번 IT 경영 관리 4계층 참조모델 (4-Layer Reference Model)     |
+------------------------------------------------------------------------+
|                                                                        |
|  [Layer 1] 거버넌스 (Governance) ------------------------------------- |
|   +--------------------+   +------------------+   +---------------+  |
|   |  ISO/IEC 38500     |   |  COBIT 2019       |   |  이사회/ITC   |  |
|   |  (6 Principles:    |◄-►|  40 Governance &  |◄-►|  (감사/통제)  |  |
|   |  Responsibility,   |   |  Management Obj.) |   |               |  |
|   |  Strategy, Acquire,|   |  + 11 Design Fac. |   +---------------+  |
|   |  Performance,      |   |  + Focus Areas    |                      |
|   |  Conformance,      |   |  (e.g., DevOps,   |                      |
|   |  Human Behavior)   |   |   Cybersecurity)  |                      |
|   +--------------------+   +------------------+                      |
|             |                          |                                |
|             v                          v                                |
|  [Layer 2] 전략 (Strategy) ----------------------------------------  |
|   +--------------------+   +------------------+   +---------------+  |
|   |  EA(Enterprise     |   |  정보화 전략      |   |  IT Portfolio |  |
|   |  Architecture)     |◄-►|  계획(ISP)        |◄-►|  Management   |  |
|   |  TOGAF 10 /         |   |  3~5년 중장기     |   |  (ITPM)       |  |
|   |  Zachman 6x6       |   |  로드맵           |   |  Pipeline->    |  |
|   +--------------------+   +------------------+   |  Active->Done  |  |
|                                                    +---------------+  |
|             |                          |                                |
|             v                          v                                |
|  [Layer 3] 운영 (Operation) ---------------------------------------  |
|   +--------------------+   +------------------+   +---------------+  |
|   |  ITIL 4            |   |  DevOps/DevSecOps |   |  ITSM Tool    |  |
|   |  34 Practices       |◄-►|  CI/CD + SRE      |◄-►|  (ServiceNow, |  |
|   |  (SVS: Service     |   |  (SLI/SLO/SLA)    |   |  Jira SM,     |  |
|   |  Value System)     |   |  GitOps, AIOps    |   |  BMC Helix)   |  |
|   +--------------------+   +------------------+   +---------------+  |
|             |                          |                                |
|             v                          v                                |
|  [Layer 4] 측정 (Measurement) --------------------------------------  |
|   +--------------------+   +------------------+   +---------------+  |
|   |  BSC (4 Perspectives|   |  KPI/KRI          |   |  FinOps       |  |
|   |  Financial,        |◄-►|  + Cockpit/       |◄-►|  Showback /   |  |
|   |  Customer,         |   |  Dashboard        |   |  Chargeback   |  |
|   |  Internal Process, |   |  (Power BI,       |   |  (Cloud unit  |  |
|   |  Learning&Growth)  |   |   Grafana)        |   |   economics)  |  |
|   +--------------------+   +------------------+   +---------------+  |
+------------------------------------------------------------------------+
        ^ 모든 Layer를 관통: 사이버보안·리스크(ISO 27001), 개인정보(PIPC), ESG
```

기존 2000년대 "프로젝트 단위 IT 관리"와 비교해, 731번 토픽이 요구하는 현대적 패러다임은 **"포트폴리오 단위 가치(Value) 중심 관리"**이며, **Value Stream**(예: 주문->결제->배송 End-to-End)을 기준으로 IT와 비즈니스 KPI를 직접 매핑한다.

- **📢 섹션 요약 비유**: IT 경영 관리를 **배의 항해**에 비유하면, Layer 1(거버넌스)은 **선장·항해사·해양법 규칙(ISO 38500)**, Layer 2(전략)는 **항로 설계도(EA·지도)**, Layer 3(운영)은 **엔진룸·기관장(ITIL·DevOps)**, Layer 4(측정)은 **속도계·나침반·연료 게이지(BSC·FinOps)**이며, **"측정할 수 없으면 관리할 수 없다"**는 피터 드루커의 원칙이 4계층의 정중앙에 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 731번의 핵심 메커니즘은 **"EDM( Evaluate-Direct-Monitor) 사이클"**(COBIT 2019)을 중축으로, **"PDCA + 밸류체인"**(Deming Cycle + Porter Value Chain)을 IT 도메인에 맞게 재해석한 것이다. 아래 ASCII 다이어그램은 거버넌스 의사결정이 실제로 운영 KPI로 환원되어 피드백되는 흐름을 보여준다.

```text
+---------------------------------------------------------------------+
|       COBIT 2019 EDM 사이클 + ITIL 4 Value Chain 결합 흐름도         |
+---------------------------------------------------------------------+
|                                                                     |
|   +----------+    +----------+    +----------+    +----------+   |
|   | EVALUATE |---►| DIRECT   |---►| MONITOR  |---►| FEEDBACK |   |
|   | (평가)   |    | (지시)   |    | (모니터) |    | (환류)   |   |
|   | - 옵션   |    | - 우선순위|    | - 성과   |    | - 목표   |   |
|   |   비교   |    |   설정   |    |   측정   |    |   재조정 |   |
|   | - TCO    |    | - 자원   |    | - KPI    |    | - 학습   |   |
|   | - 위험도 |    |   배분   |    | - 감사   |    | - 개선   |   |
|   +----+-----+    +----+-----+    +----+-----+    +----+-----+   |
|        |               |               |               |          |
|        v               v               v               v          |
|   +-------------------------------------------------------------+ |
|   |              IT 거버넌스 의사결정 라운드 테이블                 | |
|   |   +-----------+--------------+--------------+------------+  | |
|   |   | 이사회    | ITC(정보화   | CIO Office   | 사업부     |  | |
|   |   | (Steer)   |  추진위)     | (실행)       | (수요)     |  | |
|   |   | A: Approve| C: Consult   | R: Responsible| I: Inform |  | |
|   |   +-----------+--------------+--------------+------------+  | |
|   +-------------------------------------------------------------+ |
|        |               |               |               |          |
|        v               v               v               v          |
|   +-------------------------------------------------------------+ |
|   |  ITIL 4 Service Value Chain (6 Activities)                    | |
|   |  Plan -> Improve -> Engage -> Design&Transition -> Obtain/Build | |
|   |                            -> Deliver&Support ----► Value     | |
|   +-------------------------------------------------------------+ |
|        |                                                              |
|        v                                                              |
|   +-------------------------------------------------------------+ |
|   |  실측 계측 (Telemetry & Observability)                         | |
|   |  SLI: Latency p99 / Error Rate / Throughput / Saturation      | |
|   |  SLO: 99.95% 가용, p99 < 300ms, MTTR < 30min                  | |
|   |  Tool: Prometheus + Grafana + OpenTelemetry + Sentry          | |
|   +-------------------------------------------------------------+ |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (Governance System)** | 이사회·ITC(정보기술위원회)·CIO의 **RACI** 기반 의사결정 구조 | COBIT 2019의 **40 Governance/Management Objectives**, **11 Design Factors**(전략, 목표, 위험, 문제, 환경 등) 매핑, ISO/IEC 38500 6원칙 준수 여부 점검 |
| **전략 기획 (ISP/EA)** | 3~5년 중장기 로드맵, As-Is/To-Be Gap 분석 | TOGAF 10 **ADM(Architecture Development Method)** 8단계(I->F->G->H->ReqMgmt로 변경), **Zachman 6x6**(What/How/Where/Who/When/Why × Planner/Owner/Designer/Builder/Subcontractor/Functioning Enterprise) |
| **포트폴리오 관리 (ITPM)** | 프로젝트·프로그램·서비스·자산의 최적 조합 | 3-Stage Pipeline(**Phase 1: Concept -> Phase 2: Develop -> Phase 3: Deliver**), 정량적 우선순위: **가치 점수 = (전략정렬×0.4)+(위험관리×0.2)+(ROI×0.2)+(준법성×0.2)** |
| **서비스 운영 (ITSM/DevOps)** | 34개 ITIL 4 Practice 실행, SRE·DevSecOps 통합 | **Change Enablement**(CAB + Emergency Change 분리), **Incident Management**(P1~P4 SLA 차별화), **Service Desk**(L1/L2/L3 + AI Chatbot), **CI/CD**(GitHub Actions/GitLab CI), **GitOps**(ArgoCD/Flux) |
| **성과 측정 (KPI/BSC/FinOps)** | 정량적 성과·비용 가시화, 의사결정 피드백 | **KPI Tree**(전략->CSF->KPI), BSC 4관점(Financial/Customer/Internal/L&G) + 5세대(ESG·Digital 포함), FinOps Foundation **Inform->Optimize->Operate** 3단계, **Showback/Chargeback** 단가 모델 |

핵심 파라미터 및 정량 기준은 다음과 같다.

- **서비스 가용성(SLA)**: Tier 1 99.99%, Tier 2 99.95%, Tier 3 99.9% (연간 허용 다운타임 52.6분 / 4.38시간 / 8.77시간)
- **MTTR(Mean Time To Repair)**: Critical 30분, Major 4시간, Minor 24시간
- **MTBF(Mean Time Between Failure)**: ≥ 720시간(30일) 목표
- **Change Success Rate**: ≥ 95% (ITIL 권고)
- **First Contact Resolution(FCR)**: ≥ 70%
- **CSAT(Customer Satisfaction)**: ≥ 4.5/5.0 (NPS ≥ 40)
- **TCO 산출 공식**: TCO = CapEx + OpEx + Hidden Cost(생산성 손실·학습·전환 비용·유지보수). 통상 **CapEx:OpEx = 30:70**(on-prem)에서 **10:90**(cloud-native)로 전환
- **NPV(순현재가치)**: NPV = Σ [CFₜ / (1+r)ᵗ] − I₀ (할인율 r = WACC 8~12%)
- **정보화 투자효율 산정**: ROI = (편익−비용) / 비용 × 100, Payback Period = 투자액 / 연간현금흐름
- **성숙도 평가**: **CMMI 5단계**(Initial->Managed->Defined->Quantitatively Managed->Optimizing) 또는 **COBIT PAM**(Process Assessment Model) 6단계(Level
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 731 / 800

<- **이전**: [730. IT 경영 관리 핵심 토픽 730번 시험 요약](/studynote/12_it_management/05_security_compliance/730_it_management_core_topic_730_exam_summary/)
**다음**: [732. IT 경영 관리 핵심 토픽 732번 시험 요약](/studynote/12_it_management/05_security_compliance/732_it_management_core_topic_732_exam_summary/) ->

---
