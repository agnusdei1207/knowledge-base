---
title: "IT Management Core Topic 538 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 538. IT 경영 관리 핵심 토픽 — IT 거버넌스 및 전략적 IT 성과관리 (IT Governance & Strategic IT Performance Management)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 **COBIT 2019의 40개 Governance/Management Objective**와 **ISO/IEC 38500의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**을 기반으로, IT를 기업의 가치사슬(Value Chain)에 정렬(Strategic Alignment)시키고 **EDM(Evaluate-Direct-Monitor)** 사이클로 통제하는 경영체계이다.
> 2. **가치**: McKinsey & Company의 2023년 글로벌 CIO 서베이에 따르면, 성숙도 Level 4-5의 IT 거버넌스 도입 조직은 **IT 투자 대비 ROI 23% 향상**, **프로젝트 실패율 41% -> 12% 감소**, **Time-to-Market 35% 단축**의 정량 효과를 달성하며, 동시에 ISO 38500 Conformance를 통한 규제 컴플라이언스 리스크를 60% 이상 절감한다.
> 3. **판단 포인트**: **중앙집권형(Centralized, COBIT 단일 프레임워크) vs 분산형(Federated, COBIT+ITIL+ISO 다중 프레임워크)** 구조 선택, **Capability Level 3(Established) 도달 시점의 ROI Cliff**, 그리고 **RACI 매트릭스에서 Accountable(책무)과 Responsible(실행)의 분리**가 아키텍처의 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경 및 등장 배경

1990년대 후반~2000년대 초반, IT가 단순 비용센터(Cost Center)에서 전략적 경쟁우위의 원천으로 부상하면서, CFO/CEO 관점에서 "IT에 투자한 돈이 어디로 가고 있으며, 어떤 가치를 만드는가?"라는 **투자대비성과(Return on IT Investment) 측정 요구**가 폭발적으로 증가했다. 이 시기를 기점으로 미국에서는 **IT Governance Institute(ITGI, 현 ISACA)**가 1996년 결성되어 COBIT이诞生하게 되었고, OECD는 2004년 «IT 거버넌스에 대한 가이드라인»을 발표하며, 영국표준협회(BSI)는 BS 7799(현 ISO 27000시리즈)와 함께 BS 15000(현 ISO 20000) 기반의 IT 거버넌스 표준화 움직임이 본격화되었다.

특히 2002년 미국 **사베인즈-옥슬리법(SOX, Sarbanes-Oxley Act)** 통과로 인해 IT 일반통제(ITGC, IT General Controls)의 형식적 준수 증빙이 회계감사 필수 항목이 되었고, 이는 "IT 거버넌스 = 컴플라이언스"라는 등식을 업계에 정착시켰다. 이후 2008년 글로벌 금융위기, 2018년 EU GDPR, 2020년대 공급망 공격(SolarWinds, Kaseya VSA 사례) 등을 거치며 IT 거버넌스는 **단순 통제 -> 가치 창출 -> 회복탄력성(Resilience) 확보**로 그 패러다임이 진화해 왔다.

```text
[ IT 거버넌스 진화 패러다임의 시대별 변천 ]

 +------------+    +------------+    +------------+    +------------------+
 | 1990s 이전 | ->  | 2000s      | ->  | 2010s      | ->  | 2020s (현재)      |
 |            |    |            |    |            |    |                  |
 |  Cost      |    |  Control   |    |  Value     |    |  Resilience      |
 |  Center    |    |  & SOX     |    |  Creation  |    |  & ESG-Aligned   |
 |            |    |            |    |            |    |                  |
 | - DRP/BCP  |    | - COBIT v4 |    | - COBIT 5  |    | - COBIT 2019     |
 | - 데이터   |    | - ISO 38500|    | - ITIL v3  |    | - ITIL 4         |
 |   처리규칙 |    | - ITIL v2  |    | - EA(TOGAF)|    | - ISO 38500:2015 |
 |   위주     |    | - BSC 4관점|    | - DevOps   |    | - NIST CSF 2.0   |
 +------------+    +------------+    +------------+    +------------------+
                                                          |
                                                          v
                                            +--------------------------+
                                            |  AI 거버넌스 + 양자안전성 |
                                            |  + 디지털 신뢰(Digital    |
                                            |  Trust) + 그린 IT         |
                                            +--------------------------+
```

### 1.2 왜 필요한가? (As-Is vs To-Be)

| 구분 | As-Is (거버넌스 부재) | To-Be (성숙 거버넌스 도입) |
| :--- | :--- | :--- |
| **전략 정렬** | IT 프로젝트 60% 이상이 비즈니스 목표와 단절(Standish Group 2020: **31.1% 프로젝트 조기 중단·취소**) | 전략-포트폴리오-프로젝트 3단 캐스케이드 정렬, 포트폴리오 가치 23%^ |
| **리스크 관리** | Shadow IT 비율 38%(Flexera 2023), 해킹 노출면적 비가시 | Zero Trust Architecture, NIST CSF 2.0 Function(Identify-Protect-Detect-Respond-Recover) 매핑 |
| **투자 의사결정** | CapEx 70% vs OpEx 30% 경직, TCO 누락, ROI 블랙박스 | TCO(총소유비용)·NPV·IRR·PP·NPV-at-Risk 기반 다기준 의사결정, FinOps 통합 |
| **컴플라이언스** | 중복감사(중복 컨트롤 200%+), 연간 컴플라이언스 비용 5억원+(금융권 기준) | 통합 GRC(Governance-Risk-Compliance) 플랫폼, 컨트롤 중복 제거 45%v |
| **조직·문화** | CIO-CTO-CISO 간 권한 분쟁, RACI 모호 | COBIT 2019 EDM 메트릭, RACI 11×N 매트릭스, CGEIT/CISA/CISM 자격 기반 직무 분리 |

### 1.3 기술사적 관점의 핵심 문제 인식

기술사 시험은 단순 암기형이 아니라 **"왜 이 프레임워크가 필요하며, 도입 시 어떤 마찰과 트레이드오프가 발생하는가"**를 묻는 응용·상황형 문항이 절대 다수이다. 따라서 거버넌스 본질은 다음 3가지 질문에 답할 수 있어야 한다:

1. **Value Delivery**: IT 투자가 EBITDA에 어떻게 기여하는가? (IT-BSC의 4관점: Financial-Customer-Internal Process-Learning & Growth)
2. **Risk Optimization**: 정당한 리스크를 넘어선 Residual Risk를 어떻게 가시화하는가? (KRIs: Key Risk Indicators, Monte Carlo 시뮬레이션, VaR-at-IT)
3. **Resource Optimization**: 한정된 CapEx/OpEx를 어떤 포트폴리오(기존 운영·혁신·규제 준수·전략)에 배분하는가? (Stage-Gate, Real Options Valuation)

- **📢 섹션 요약 비유**: **"IT 거버넌스"는 마치 100층 빌딩의 '건축 허가 심사 + 정기 안전점검 + 에너지 효율 인증서' 통합 시스템**과 같다. 발코니 확장(신규 프로젝트) 신청 시 건축법·소방·에너지·재난대응 4개 부서가 동시에 검토하고, 거주 후에는 매년 정기 안전진단으로 균열·누수·전기 부하를 점검해야 건물이 무너지지 않는다. 빌딩 오너인 CEO/CIO가 이 통합 시스템을 운영하지 않으면, 화려한 외관만 무너지는 빌딩처럼 IT 투자는 ROI를 만들지 못한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 COBIT 2019 시스템 아키텍처

COBIT 2019는 **6원칙(Principles) -> 40 Governance/Management Objective -> 7 컴포넌트(Components) -> 3 단위(Process/Structure/People)**의 4계층 참조 모델을 따른다. 핵심은 **EDM(목표 평가·지시·모니터링)** 5개 거버넌 프로세스와 **APO->BAI->DSS->MEA** 4개 영역의 35개 관리 프로세스다.

```text
[ COBIT 2019 거버넌스 아키텍처 상세 구조 ]

   +------------------------------------------------------------------+
   |              외부 환경 (External Environment)                      |
   |  - 전략 (Strategy)  - 규제 (Regulations)  - 기술 (Technology)    |
   +-----------------------------+------------------------------------+
                                 v
   +------------------------------------------------------------------+
   |  계층 1: 6 Governing Principles (핵심원칙)                         |
   |   P1. Each Enterprise needs a governance system                    |
   |   P2. Governance system should cover the enterprise end-to-end     |
   |   P3. Apply a single integrated framework                          |
   |   P4. Enabling a holistic approach                                 |
   |   P5. Distinguishing governance from management                    |
   |   P6. Tailoring the system to enterprise needs (Design Factors)    |
   +-----------------------------+------------------------------------+
                                 v
   +------------------------------------------------------------------+
   |  계층 2: 40 Governance & Management Objectives                    |
   |   +- EDM(5): Evaluate, Direct and Monitor                         |
   |   |   EDM01 Framework | EDM02 Benefits | EDM03 Risk              |
   |   |   EDM04 Resources| EDM05 Transparency                          |
   |   +- APO(14): Align, Plan and Organize                            |
   |   |   APO01-APO14 (전략/포트폴리오/예산/아키텍처/혁신/...)         |
   |   +- BAI(11): Build, Acquire and Implement                        |
   |   |   BAI01-BAI11 (프로젝트/요구사항/솔루션/전환/...)              |
   |   +- DSS(6): Deliver, Service and Support                          |
   |   |   DSS01-DSS06 (운영/인시던트/연속성/보안/...)                  |
   |   +- MEA(4): Monitor, Evaluate and Assess                          |
   |       MEA01 Performance | MEA02 System | MEA03 Compliance        |
   |       MEA04 Assurance                                          |
   +-----------------------------+------------------------------------+
                                 v
   +------------------------------------------------------------------+
   |  계층 3: 7 Components of the Governance System                     |
   |   ① Process              ② Organizational Structures               |
   |   ③ Information Flows    ④ People, Skills and Competencies        |
   |   ⑤ Policies and Procedures  ⑥ Culture, Ethics and Behavior      |
   |   ⑦ Services, Infrastructure and Applications                    |
   +-----------------------------+------------------------------------+
                                 v
   +------------------------------------------------------------------+
   |  계층 4: 3 Concerns (Benefits, Risk, Resources)                    |
   |   +- B: Benefit Realization (가치 실현)                            |
   |   +- R: Risk Optimization (리스크 최적화)                          |
   |   +- R: Resource Optimization (자원 최적화)                        |
   +------------------------------------------------------------------+
                                 v
   +------------------------------------------------------------------+
   |  목표 캐스케이드 (Goals Cascade)                                   |
   |   Stakeholder Needs -> Enterprise Goals -> Alignment Goals          |
   |   -> Management Objectives -> Process Goals (P) + Metrics (M)       |
   +------------------------------------------------------------------+
```

### 2.2 목표 캐스케이드(Goals Cascade) 메커니즘

COBIT 2019는 **13개 Enterprise Goal -> 13개 Alignment Goal -> 40개 Management Objective**로 이어지는 **3단계 캐스케이드**를 정의한다. 각 단계에서 **Primary(기여도 1.0) / Secondary(0.7)** 가중치를 부여하여, IT 프로세스가 어떤 기업 목표에 얼마만큼 기여하는지를 정량화한다.

```text
[ 목표 캐스케이드 - 실전 예시 ]

 +------------------------------------------------------------+
 |  Stakeholder Needs (이해관계자 요구)                          |
 |   "주주가치 극대화 + 고객만족 + 컴플라이언스 + 지속가능성"     |
 +--------------------------+---------------------------------+
                            v
 +------------------------------------------------------------+
 |  Enterprise Goals (13개)                                    |
 |   EG01: 포트폴리오 경쟁제품/서비스 수익화                    |
 |   EG04: IT 관련 리스크 관리                                  |
 |   EG08: 내부 비즈니스 기능 최적화                            |
 |   EG12: 디지털 혁신/디지털 트랜스포메이션                     |
 +--------------------------+---------------------------------+
                            v
 +------------------------------------------------------------+
 |  Alignment Goals (13개)                                     |
 |   AG01: IT 준거 및 지원 프로세스                              |
 |   AG04: 지식, 전문성 및 행동                                 |
 |   AG09: 정보 처리 인프라 최적화                               |
 |   AG13: 디지털 혁신 실현                                      |
 +--------------------------+---------------------------------+
                            v
 +------------------------------------------------------------+
 |  Management Objectives (40개)                                |
 |   +- APO04(혁신관리) --AG13 직접 매핑                          |
 |   +- APO12(리스크관리) --AG09 매핑                            |
 |   +- BAI02(요구사항관리) --AG01/AG08 매핑                     |
 |   +- DSS02(인시던트관리) --AG04/AG09 매핑                     |
 +--------------------------+---------------------------------+
                            v
 +------------------------------------------------------------+
 |  Process Goals (P) + Metrics (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 538 / 800

<- **이전**: [537. IT 경영 관리 핵심 토픽 537번 시험 요약](/studynote/12_it_management/05_security_compliance/537_it_management_core_topic_537_exam_summary/)
**다음**: [539. IT 경영 관리 핵심 토픽 539번 시험 요약](/studynote/12_it_management/05_security_compliance/539_it_management_core_topic_539_exam_summary/) ->

---
