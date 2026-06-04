+++
title = "730. IT 경영 관리 핵심 토픽 730번 시험 요약 (IT Management Core Topic 730 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 730. IT 경영 관리 핵심 토픽 730번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리(Information Technology Management)는 COBIT 2019·ISO/IEC 38500·ITIL 4 거버넌스 프레임워크를 기반으로 IT 전략 기획(ISP) -> 투자 우선순위 결정(PPM) -> 아키텍처 거버넌스(EA) -> 서비스 운영(ITSM) -> 성과 측정(BSC/KPI) 의 End-to-End 가치사슬을 통합 관리하는 경영학문이다.
> 2. **가치**: McKinsey(2023) 보고에 따르면 디지털 전환을 거버넌스 체계와 연계한 기업은 TCO 23% 절감, Time-to-Market 38% 단축, IT 프로젝트 성공률 67%->82% 향상 효과를 달성하며, ISO 38500 인증 기업의 ROI는 비인증 대비 평균 2.4배 높다.
> 3. **판단 포인트**: 기술사적 핵심은 **① Balance Score Card 4관점(재무/고객/내부/학습성장) × COBIT 2019 40개 관리목표** 간의 인과모형(Causal Model) 설계, ② Six Sigma DMAIC와 Agile 간 하이브리드 거버넌스, ③ 3Lines Model(운영/내부통제/독립감사)에 따른 Risk Appetite 정의, ④ Capex/Opex 최적화 비율 결정이다.

---

## Ⅰ. 개요 및 필요성

IT 경영관리 영역은 단순한 "IT 부서 관리"를 넘어 **"기업의 전략적 자산으로서 IT의 가치를 극대화하고, 리스크를 통제하며, 이해관계자(Stakeholder)에게 책임을 이행하는 체계"** 이다. 한국정보통신기술사 시험 730번은 이 영역의 통합적 이해를 평가하며, 특히 **거버넌스–전략–투자–아키텍처–운영–성과** 의 6대 영역을 통합 관점으로 서술할 수 있는지를 판단한다.

2020년 이후 코로나19 팬데믹, 공급망 재편, 생성형 AI(GenAI) 등장으로 IT 거버넌스의 패러다임이 근본적으로 변했다. 기존 **Plan–Build–Run** 의 선형 모델에서, **Sense–Respond–Adapt** 의 VUCA 대응형 지속적 적응(Continuous Adaptation) 모델로 전환되었고, 이는 COBIT 2019의 Focus Area(F) 메커니즘과 ITIL 4의 Service Value System(SVS)으로 구체화되었다.

```text
+------------------------------------------------------------------------+
|        IT 경영관리 6대 영역 통합 거버넌스 프레임워크 (730번)            |
+------------------------------------------------------------------------+
|                                                                        |
|  [Stakeholders]                                                        |
|       |  Board | CEO | CIO | BUs | Regulators | Customers             |
|       v                                                                |
|  +--------------------------------------------------------------+      |
|  |  ① 거버넌스 (Governance) — ISO 38500 / COBIT 2019            |      |
|  |     · 책임구조(RACI) · Risk Appetite · 원칙(6 Principles)    |      |
|  |     · 3 Lines Model: 운영(1st) / 내부통제(2nd) / 감사(3rd)    |      |
|  +--------------------------------------------------------------+      |
|       v                  v                  v                          |
|  +---------+      +---------+      +---------+      +---------+      |
|  | ② 전략  |      | ③ 투자  |      | ④ 아키텍|      | ⑤ 운영  |      |
|  | ISP/EA  | ----> | PPM/CBA | ----> | TOGAF/  | ----> | ITIL 4  |      |
|  | BSC KPI |      | Capex/  |      | FEAF    |      | SRE/    |      |
|  | Portfo. |      | Opex    |      | DoDAF   |      | DevOps  |      |
|  +---------+      +---------+      +---------+      +---------+      |
|       |                  |                  |              |           |
|       +------------------+------------------+--------------+           |
|                              v                                          |
|                  +-----------------------+                             |
|                  |  ⑥ 성과측정           |  · IT BSC 4관점              |
|                  |     Measurement       |  · COBIT CSF Goal Cascade   |
|                  |  · KPI Tree (4단계)   |  · OKR · EVA · ROSC         |
|                  |  · Benchmark (ISACA)  |  · TBM (Toward-Goal)        |
|                  +-----------------------+                             |
|                              |                                          |
|                              v  [Feedback Loop]                        |
|                  +-----------------------+                             |
|                  |  Continuous Improve   |  · Kaizen · PDCA · DMAIC    |
|                  |  + Adapt (V.U.C.A)    |  · Bimodal IT · Lean        |
|                  +-----------------------+                             |
+------------------------------------------------------------------------+
```

**왜 필요한가?** 기존 2000년대 IT 운영 모델은 **① SI(System Integration) 중심의 Capex 과잉 투자, ② 부서별 스ilos화로 인한 중복 투자(전사 평균 27% 중복), ③ Shadow IT로 인한 보안사고(Total Security Incidents의 약 38% 점유)** 의 3대 구조적 문제에 직면했다. Gartner(2022) 통계에 따르면 Fortune 500 기업의 평균 Shadow IT 지출은 공식 IT 예산의 30~40%에 달하며, 이 중 73%가 보안 검토 없이 운영된다. IT 경영관리는 이를 **통합 거버넌스·EA·ITSM·BSC** 4대 기둥으로 구조적으로 해결한다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **"도시의 토목·교통·에너지·치안·재정을 한 개의 스마트시티 운영본부(Smart City Control Tower)에서 통합 관제하는 시스템"** 과 같다. 각 부서(서버팀, 네트워크팀, 보안팀, 현업부서)가 제각각 움직이면 교통체증(병목), 정전(SLA 미달), 사고(보안침해)가 끊이지 않지만, 통합 관제탑이 실시간으로 데이터를 모아 의사결정하면 도시 전체가 효율적으로 움직인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 기술적 핵심은 **거버넌스 체계(Governance System) ↔ 전략 계획(ISP) ↔ 아키텍처(EA) ↔ 운영(ITSM) ↔ 성과(BSC)** 5계층을 **메타-모델(Meta-Model)** 차원에서 정합(Alignment)시키는 것이다. COBIT 2019는 이를 **Components(40개) ↔ Focus Areas ↔ Goals Cascade** 의 3축으로 추상화한다.

```text
        +---------------------------------------------------------+
        |      COBIT 2019 Governance System (메타-아키텍처)        |
        +---------------------------------------------------------+
            |                  |                  |              |
            v                  v                  v              v
    +-------------+    +-------------+    +-------------+  +----------+
    | Governance  |    |  5 Domains  |    | 7 Enablers  |  | 40 MGMT  |
    | Objectives  |    |             |    |  (Components)|  |  Goals   |
    |             |    | EDM(05)     |    |  ① People   |  |  (MGMT)  |
    | · Stakeh.   |    | APO(14)     |    |  ② Process  |  |          |
    | · Goal Casc.|    | BAI(11)     |    |  ③ Structure|  |  EDM: 05 |
    | · Risk Opt. |    | DSS(06)     |    |  ④ Objectv. |  |  APO: 14 |
    |             |    | MEA(04)     |    |  ⑤ Info.    |  |  BAI: 11 |
    |             |    |             |    |  ⑥ Service  |  |  DSS: 06 |
    |             |    |             |    |  ⑦ Culture  |  |  MEA: 04 |
    +-------------+    +-------------+    +-------------+  +----------+
            |                  |                  |              |
            +------------------+------------------+--------------+
                                |
                                v  (Mapping)
                  +-----------------------------+
                  |  External Standards Mapping  |
                  |  --------------------------  |
                  |  ISO 38500 (6 Principles)    |
                  |  ITIL 4 (34 Practices)       |
                  |  PMBOK 7 (8 Domains)         |
                  |  TOGAF 10 (ADM Cycle)        |
                  |  NIST CSF 2.0 (6 Functions)  |
                  |  ISO 27001 (114 Controls)    |
                  |  ISO 22301 (BCMS)            |
                  +-----------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① 거버넌스 목표 체계 (Goals Cascade)** | 전략 ↔ IT ↔ 성과 3단계 인과사슬 | 13개 Enterprise Goals -> 13개 Alignment Goals -> 40개 Management Goals. 각 단계 간 **In-Use -> Apply -> Contribute -> Deliver** 4단계 인과관계로 추적. |
| **② 5개 도메인 (EDM/APO/BAI/DSS/MEA)** | IT 라이프사이클 전영역 책임영역 | EDM(Evaluate/Direct/Monitor, 5개) -> APO(Align/Plan/Organize, 14개) -> BAI(Build/Acquire/Implement, 11개) -> DSS(Deliver/Service/Support, 6개) -> MEA(Monitor/Evaluate/Assess, 4개). RACI 매트릭스로 책임 할당. |
| **③ 7개 Enabler (Components)** | 거버넌스 작동 메커니즘 | ① Process ② Organizational Structures ③ Information Flow ④ People/Skills ⑤ Principles/Policies ⑥ Culture/Ethics ⑦ Services/Infrastructure/Applications. 각 Enabler은 4단계 성숙도(Level 0~5) 평가. |
| **④ Focus Areas (FA)** | 동적 이슈 대응 맞춤형 거버넌스 | ① Cybersecurity ② DevOps ③ Digital Transformation ④ SME ⑤ Risk ⑥ Compliance 등 36개 FA. 기업 상황에 따라 우선순위 FA 3~5개 선정. |
| **⑤ 목표성숙도 모델 & Capability Level** | 정량적 거버넌스 성숙도 평가 | **Process Capability**: ISO 33000 PAM 기준 6단계(0~5). **Performance**: 실현도 5단계. 두 축을 곱하여 Rating 산출 (예: PA 1.1 = Capability Lv.3 × Performance 85%). |

**핵심 알고리즘 및 공식**:
- **BSC 인과모형(Causal Model)**: 재무(F) <- 고객(C) <- 내부프로세스(IP) <- 학습성장(LG). LG 지표(예: 직원 역량 Index)^ -> IP(예: MTTR 30%v)^ -> C(예: NPS 12pt^)^ -> F(예: 매출 8%^) 인과 검증은 **Pearson Correlation ≥ 0.7** 이상 유의.
- **IT 투자 회수율(ROSI)**: `ROSI = (ALE × Mitigation%) − Annual Cost of Solution` / `Annual Cost of Solution` × 100. (ALE: Annual Loss Expectancy)
- **NPV/CBA**: `NPV = Σ( Benefit_t − Cost_t ) / (1+r)^t − Initial Investment`. 기업 hurdle rate r=8~12% 적용, IRR > WACC일 때 투자 적격.
- **EV/IT CAPEX 회수기간**: TCO = Capex + Σ Opex(5y). 3년 Payback Rule 적용.
- **TBM(Toward Business Management)**: IT 비용을 **Tower(서버/스토리지/네트워크) -> Service Tier(Gold/Silver/Bronze) -> Business Unit** 3단 Cost Allocation.

- **📢 섹션 요약 비유**: COBIT 2019는 마치 **"자동차의 계기판(Dashboard)과 진단 시스템(OBD-II)"** 과 같다. 속도(성과), RPM(처리량), 연료(License/인건비), 엔진온도(Risk), 경고등(Control Gap)을 **표준화된 신호 체계(Signal)** 로 통합 노출하여, 운전자(임원)가 실시간으로 차량(기업)의 상태를 판단하고 핸들(의사결정)을 조작할 수 있게 한다.

---

## Ⅲ. 비교 및 연결

기술사 시험에서 빈출되는 비교 영역은 **거버넌스 프레임워크 간 상호보완 관계**, **전통적 vs Agile 거버넌스**, **Capex vs Opex 모델** 이다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 초점** | 거버넌스 + 관리 전영역 | IT 서비스 운영 (Service) | 이사회 거버넌스 원칙 | 프로젝트 관리 | 아키텍처 개발 방법론 |
| **구조/원리** | 40 MGMT × 7 Enablers × 36 FA | SVS + 34 Practices | 6 Principles + 3 Tasks | 8 Performance Domains + 12 Principles | ADM 8단계(Phase A~H) |
| **적용 범위** | Enterprise 전체 | Service Lifecycle | 거버넌스 최상위 | 단일 프로젝트 | EA 도메인 |
| **평가 모델** | Capability/Performance Lv.0~5 | 4-Dimension Maturity | 원칙 준수 점검 (Self/Independent) | Value Delivery (8 PD) | ADM Maturity Model |
| **통합 관계** | 다른 프레임워크를 매핑·조율 | COBIT의 DSS 도메인 보완 | COBIT EDM 도메인과 매핑 | BAI(11) 도메인과 매핑 | APO 도메인의 BA(보안)·BAI 연계 |

**Capex vs Opex 비교 (핵심 판단 포인트)**:
- **Capex(자본적 지출)**: 물리적 자산(서버, 네트워크, 라이선스 영구) -> 감가상각(통상 5년) -> 재무제표 자산화. **장점**: 단위비용 낮음, 통제 용이. **단점**: 유연성v, 자산 유휴(평균 Utilization 18~25%)^.
- **Opex(운영적 지출)**: Cloud, SaaS, Managed Service 등 사용량 기반 과금 -> 손익계산서 비용화. **장점**: Elasticity, Pay-as-you-go, TCO 가시화. **단점**: 장기 Lock-in, 데이터 주권 이슈.
- **기술사적 판단**: **70/30 Rule** (전체 IT 예산 중 Capex 30%, Opex 70% 목표) 적용. 단, **규제 산업(금융/공공)**: 데이터 주권·규제 때문에 On-Premise Capex 비중 50%+ 유지. 디지털 트랜스포메이션 단계 기업은 **50/50 Bimodal IT** 권장.

**전통 거버넌스(Stage-Gate) vs Agile 거버넌스**:
- Stage-Gate: **Go/Kill 결정** 시점 명확, ROI 사전 검증 가능. **단점**: 평균 18~36개월 Lead Time.
- Agile: 2~4주 Sprint 단위, **MVP 검증**. **단점**: ROI 사후 누적
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 730 / 800

<- **이전**: [729. IT 경영 관리 핵심 토픽 729번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/729_it_management_core_topic_729_exam_summary/)
**다음**: [731. IT 경영 관리 핵심 토픽 731번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/731_it_management_core_topic_731_exam_summary/) ->

---
