---
title: "IT Management Core Topic 663 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 핵심 토픽은 **COBIT 2019 거버넌스 체계**(40개 Governance/Management Objectives)와 **ITIL 4 SVS**(Service Value System)를 양대 축으로, **ISO 38500 6원칙**(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 국제 표준 거버넌스 기반으로 통합 운영하며, **RACI 매트릭스**와 **Design Factor 11개**를 통해 조직별 맞춤 거버넌스 시스템을 구축하는 것을 본질로 한다.
> 2. **가치**: 체계적 IT 거버넌스 도입 시 **프로젝트 실패율 40%->15% 감소**(Standish Group CHAOS Report 2020), **IT 운영 비용 20~30% 절감**(Gartner), **규제 준수 감사 시간 50% 단축**의 정량적 효과를 거둘 수 있으며, 이사회-경영진-IT 조직 간 **3-Layer Decision Rights**를 명확히 함으로써 전략적 IT 투자 수익률(ROIT)을 평균 **15% 이상** 개선할 수 있다.
> 3. **판단 포인트**: **거버넌스 프레임워크 선택 시 COBIT vs ITIL vs ISO 38500의 적용 범위**를 명확히 구분해야 하며(COBIT=End-to-End, ITIL=서비스 운영, ISO 38500=이사회 거버넌스), **Tailoring 강도**(Full vs Partial Adoption)와 **자동화 수준**(수동 vs GRC 플랫폼-예: ServiceNow GRC, Archer, SAP GRC) 간의 트레이드오프, 그리고 **Design Factor 가중치**(Enterprise Strategy, Risk Profile, Compliance 등 11개) 결정이 기술사의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

21세기 디지털 전환(DX) 환경에서 기업 IT 투자는 총 CAPEX의 **30~50%**를 차지하며, 이 중 **30%가 IT 실패 프로젝트**(McKinsey, 2021)로 손실된다. 전통적인 IT 관리는 **기술 중심**(Technology-Centric) 접근으로 하드웨어·소프트웨어 도입에만 집중했으나, 2000년대 이후 **거버넌스 중심**(Governance-Centric)으로 패러다임이 전환되었다. 이는 **사베인스-옥슬리법(SOX, 2002)**, **한국의 전자금융거래법**, **GDPR**, **개인정보보호법(PIPA)** 등 규제 환경의 강화와 맞물려 있다.

특히 한국 정보관리기술사 시험의 663번 토픽은 **"IT 경영관리"** 영역에서 IT 거버넌스·감사·서비스 관리·포트폴리오 관리의 통합적 이해를 평가하며, **ISACA의 CGEIT**(Certified in the Governance of Enterprise IT)와 **COBIT 2019 Foundation** 수준의 지식이 요구된다. 본 토픽의 핵심은 **"IT가 비즈니스 가치를 어떻게 창출하는가"**라는 질문에 대해 거버넌스-관리-운영의 3계층 프레임워크로 답하는 것이다.

```text
+----------------------------------------------------------------------+
|              IT 경영관리 3-Layer 통합 프레임워크                       |
+----------------------------------------------------------------------+
|                                                                      |
|   +------------------------------------------------------------+    |
|   |  LAYER 1: GOVERNANCE (거버넌스) - 이사회/경영진 책임          |    |
|   |  +------------------------------------------------------+  |    |
|   |  |  • 방향성 설정 (Direction Setting)                    |  |    |
|   |  |  • 의사결정 권한 위임 (Decision Rights)              |  |    |
|   |  |  • 성과 모니터링 (Performance Monitoring)            |  |    |
|   |  |  • 준수 평가 (Conformance Assessment)                |  |    |
|   |  |                                                        |  |    |
|   |  |  적용 표준: ISO 38500, COBIT 2019 EDM Domain          |  |    |
|   |  |  (EDM=Evaluate, Direct, Monitor - 5개 Objective)    |  |    |
|   |  +------------------------------------------------------+  |    |
|   +------------------------------------------------------------+    |
|                              v                                       |
|   +------------------------------------------------------------+    |
|   |  LAYER 2: MANAGEMENT (관리) - IT 경영진 책임                 |    |
|   |  +------------------------------------------------------+  |    |
|   |  |  • 4개 Domain × 35개 Management Objective:            |  |    |
|   |  |    ① APO (Align, Plan, Organize) - 14개              |  |    |
|   |  |    ② BAI (Build, Acquire, Implement) - 11개          |  |    |
|   |  |    ③ DSS (Deliver, Service, Support) - 6개           |  |    |
|   |  |    ④ MEA (Monitor, Evaluate, Assess) - 4개          |  |    |
|   |  |  • 통합 관리 프로세스: 전략->포트폴리오->프로그램->      |  |    |
|   |  |    프로젝트->서비스->인프라 6단계 가치 흐름              |  |    |
|   |  +------------------------------------------------------+  |    |
|   +------------------------------------------------------------+    |
|                              v                                       |
|   +------------------------------------------------------------+    |
|   |  LAYER 3: OPERATIONS (운영) - IT 실무조직 책임               |    |
|   |  +------------------------------------------------------+  |    |
|   |  |  • ITIL 4 SVS 7가지 구성요소:                        |  |    |
|   |  |    ① Guiding Principles (7개 원칙)                   |  |    |
|   |  |    ② Governance (거버넌스 조직·활동)                 |  |    |
|   |  |    ③ Service Value Chain (6개 활동)                  |  |    |
|   |  |    ④ Practices (34개 실무 관행)                       |  |    |
|   |  |    ⑤ Continual Improvement (Kaizen 모델)            |  |    |
|   |  |  • SLA 99.9% / MTTR < 30분 / FCR > 80% 등 KPI        |  |    |
|   |  +------------------------------------------------------+  |    |
|   +------------------------------------------------------------+    |
|                                                                      |
+----------------------------------------------------------------------+
```

기존(As-Is) 패러다임은 **"IT는 비용(Cost Center)"**이라는 인식 하에 CapEx 중심으로 투자했고, 그 결과 비즈니스-IT 정렬(Business-IT Alignment) 점수가 평균 **2.5/5** 수준에 그쳤다. 새로운(To-Be) 패러다임은 **"IT는 가치 창출 엔진(Value Driver)"**으로, **IT-BSC**(Balanced Scorecard) 4관점(재무/고객/내부/학습성장)을 활용하여 IT 성과를 정량화하고, **Design Thinking**과 **Lean Startup** 방법론을 IT 서비스 설계에 접목한다.

- **📢 섹션 요약 비유**: IT 경영관리는 **배의 키잡이(Governance) - 항해사(Management) - 선원(Operations)**의 3계층 구조와 같습니다. 키잡이(거버넌스)가 "어디로 갈 것인가"를 정하면, 항해사(관리)가 "어떤 루트로 갈 것인가"를 계획하고, 선원(운영)이 실제 노를 젓습니다. 세 계층 중 어느 하나라도 어긋나면 배는 표류하게 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. COBIT 2019 핵심 아키텍처 (40개 목표 체계)

COBIT 2019는 **거버넌스 목표 5개**(EDM Domain)와 **관리 목표 35개**(APO/BAI/DSS/MEA Domain) 총 **40개 목표**로 구성된다. 각 목표는 **Process Purpose Statement**, **Goal Cascade**(ESG->Stakeholder->Enterprise->IT->Enabler 5단계), **Management Practice**(목표당 평균 3~4개)로 표준화되어 있다.

```text
+----------------------------------------------------------------------+
|          COBIT 2019 Goals Cascade (목표 계단식 연결)                  |
+----------------------------------------------------------------------+
|                                                                      |
|   [Step 1] Stakeholder Drivers & Needs                             |
|            |  예: 주주수익률^, 규제준수, 디지털경쟁력                |
|            v                                                         |
|   [Step 2] Enterprise Goals (13개)                                  |
|            |  예: EG01 포트폴리오 경쟁력, EG11 규제 준수             |
|            v  (Mapping: Stakeholder ↔ Enterprise)                  |
|   [Step 3] Alignment Goals (13개, IT 관련)                          |
|            |  예: AG01 IT 거버넌스 프레임워크 준수, AG09 정보 보안   |
|            v  (Mapping: Enterprise ↔ IT)                            |
|   [Step 4] Enabler Goals (7개 Enabler × 세부 목표)                  |
|            |  ① Principles, Policies, Frameworks                    |
|            |  ② Processes                                         |
|            |  ③ Organizational Structures                          |
|            |  ④ Information Flows & Items                          |
|            |  ⑤ People, Skills, Competencies                       |
|            |  ⑥ Services, Infrastructure, Applications              |
|            |  ⑦ Culture, Ethics, Behavior                          |
|            v  (Mapping: IT ↔ Enabler)                              |
|   [Step 5] Management Objectives (40개)                              |
|            EDM 5개 + APO 14 + BAI 11 + DSS 6 + MEA 4 = 40개        |
|            v                                                         |
|   [실행] Process Activities -> Roles(RACI) -> Metrics(NRL)            |
|                                                                      |
+----------------------------------------------------------------------+
```

### B. 핵심 구성 요소 및 7대 Enabler 상세

| Enabler (구성요소) | 역할 | 핵심 기술/방법론 및 동작 방식 |
| :--- | :--- | :--- |
| **① Principles, Policies, Frameworks** | 의사결정·운영의 규범 체계 | ISO 38500 6원칙, 내부통제 정책, COBIT 2019 Design Factor 11개 적용 (Enterprise Strategy, Goals, Risk Profile, I&T-related Issues, Threat Landscape, Compliance Requirements, IT Role, IT Sourcing Model, IT Implementation Methods, Technology Adoption, Organizational Size) |
| **② Processes** | 가치 전달의 실행 단위 | COBIT 2019의 40개 목표에 매핑된 **Management Practice**(총 ~110개)와 **RACI Chart**(Responsible, Accountable, Consulted, Informed). 예: DSS02 (서비스 요청·사고 관리) -> ITIL Incident Management |
| **③ Organizational Structures** | 의사결정·보고 체계 | **3-Layer 구조**: Board(CIO/CDO) -> Steering Committee -> PMO/서비스운영팀. **RACI 매트릭스**로 역할 분장 명확화. 예: EDM01에서 이사회가 Accountable, CISO가 Responsible |
| **④ Information** | 의사결정·운영의 데이터 자산 | **Information Quality Criteria**: 정확성(Accuracy), 완전성(Completeness), 적시성(Timeliness), 적절성(Appropriateness), 접근성(Accessibility), 준수성(Compliance). **Data Governance** = DAMA-DMBOK 11개 지식영역 |
| **⑤ People, Skills, Competencies** | 인적 역량 관리 | **SFIA v8**(Skills Framework for the Information Age) 6단계(1.Follow->6.Set direction) 역량 모델. 예: IT 거버넌스 전문가는 Level 5(Ensure/Advise) 이상 |
| **⑥ Services, Infrastructure, Applications** | 기술 인프라 자원 | **SaaS/PaaS/IaaS** 3계층, **FinOps**로 클라우드 비용 최적화, **CMDB**(Configuration Management Database) 연동 |
| **⑦ Culture, Ethics, Behavior** | 조직 문화·윤리 | **Tone at the Top**, 행동 강령(Code of Conduct), **Whistle-blowing System**, 변화관리(Change Management) - 예: ADKAR 모델(Awareness, Desire, Knowledge, Ability, Reinforcement) |

### C. 핵심 알고리즘/수식

**1) 거버넌스 성숙도 측정 (Maturity Level)**:
- COBIT 2019은 **0~5단계**의 **Performance Management (能力/Capability)** 모델을 사용한다. 각 단계는:
  - **Level 0 (Incomplete)**: 프로세스 미인정
  - **Level 1 (Initial)**: 개인 노력 의존 (Chaotic)
  - **Level 2 (Managed)**: 기본 계획 수립·모니터링
  - **Level 3 (Defined)**: 표준 프로세스 문서화·전사 배포
  - **Level 4 (Quantitative)**: 정량적 측정·관리
  - **Level 5 (Optimizing)**: 지속적 개선·혁신

**2) IT 투자 수익률 (ROIT - Return on IT Investment)**:
```
ROIT = (IT 투자로 인한 추가 이익 + 비용 절감 - IT 투자 총비용) / IT 투자 총비용 × 100
```
예: 클라우드 전환 100억 투자, 연간 35억 비용 절감, 5년 유지 -> ROIT = (35×5 - 100) / 100 = 75%

**3) NRL (Non-conformity Risk Level) 계산**:
```
NRL = Σ(Threat 발생 확률 × 영향도 × 통제 미흡도)
Threat 5단계: Very Low(1) ~ Very High(5)
Impact 5단계: Insignificant(1) ~ Catastrophic(5)
Control 3단계: Good(0.1) / Fair(0.5) / Poor(1.0)
```
예: 사이버 위협(4) × 데이터 유출 영향(5) × 통제 부재(1.0) = NRL 20 -> High Risk

**4) RACI 매트릭스 예시 (APO01 - IT 관리 프레임워크)**:
```
              | 이사회 | CEO | CIO | PMO | 운영팀 | 감사팀
APO01.A1      |   A    |  C  |  R  |  R  |   I    |   I
(거버넌스     |
 프레임워크   |
 정의)        |
A=Accountable, R=Responsible, C=Consulted, I=Informed
```

- **📢 섹션 요약 비유**: COBIT의 7대 Enabler는 **자동차의 7가지 핵심 부품**과 같습니다. ① 원칙(운전 매뉴얼) + ② 프로세스(엔진 회전) + ③ 조직(운전석) + ④ 정보(내비게이션)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 663 / 800

<- **이전**: [662. IT 경영 관리 핵심 토픽 662번 시험 요약](/studynote/12_it_management/05_security_compliance/662_it_management_core_topic_662_exam_summary/)
**다음**: [664. IT 경영 관리 핵심 토픽 664번 시험 요약](/studynote/12_it_management/05_security_compliance/664_it_management_core_topic_664_exam_summary/) ->

---
