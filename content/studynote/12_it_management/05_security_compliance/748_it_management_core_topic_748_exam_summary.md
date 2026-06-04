+++
title = "748. IT 경영 관리 핵심 토픽 748번 시험 요약 (IT Management Core Topic 748 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 748번 정보관리기술사 시험의 핵심은 **IT 거버넌스(COBIT 2019/ISO 38500) + IT 전략 정합(BSA: Business Strategy Alignment) + 정보보안 경영(ISMS-P) + 디지털 전환 거버넌스**의 4대 축을 통합적으로 아우르는 **IT 경영管理体系(Enterprise IT Management Framework)**를 구축·운영·평가하는 능력이다.
> 2. **가치**: 효과적인 IT 경영 체계 도입 시 **IT 투자 ROI 평균 25~40% 개선**(Gartner 2023), **정보보안 사고 대응시간 67% 단축**(IBM Cost of Data Breach 2023), **핵심 사업 프로세스 자동화를 통한 운영비용 20~30% 절감**, **규제 준수(컴플라이언스) 비용 35% 절감** 등 정량적 가치를 창출한다.
> 3. **판단 포인트**: 기술사 논술의 핵심은 **"거버넌스(Governance) ≠ 관리(Management) ≠ 운영(Operations)"**를 명확히 구분하고, **EA(Enterprise Architecture) -> BSC(Balanced Scorecard) -> KPI -> GRC(Governance, Risk, Compliance)**의 인과 사슬을 **임원진의 의사결정 구조**와 어떻게 연동할 것인가를 제시하는 것이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 748번 시험은 단순한 IT 기술 지식을 넘어 **"기업의 IT 자산을 경영 자산으로 전환"**하는 능력을 평가한다. 4차 산업혁명, 클라우드 전환, AI/데이터 거버넌스, ESG·공급망 보안 등 **이중 불확실성(Volatility × Uncertainty)** 환경에서 CIO는 **전략적 의사결정자(Strategic Decision Maker)**로 변모해야 하며, 이를 뒷받침할 **IT 경영 관리 체계**가 필수적이다.

기존의 **"기술 중심 IT 관리(Tech-centric IT Management)"**는 다음과 같은 한계에 직면했다:

- **사일로(Silo)형 조직**: 개발·운영·보안·컴플라이언스 부서 간 사일로화로 인한 책임 공백
- **프로젝트 단위 투자**: 포트폴리오 관점 부재로 5년간 IT 투자 대비 사업 성과 가시화 실패
- **규제 대응 사후성**: 개인정보보호법, 개인정보의 안전성 확보조치, ISMS-P 인증 등 **사후 컴플라이언스** 대응에 연간 30% 이상 예산 소진
- **경영진-IT 괴리**: 2018년 MIT Sloan 연구에 따르면 CIO의 78%가 "이사회와 IT 성과에 대해 동일한 언어로 소통하지 못한다"고 답변

이에 **"가치 중심 IT 경영(Value-driven IT Management)"** 패러다임으로 전환이 요구되며, 이는 **ISO 38500(거버넌스 원칙) -> COBIT 2019(거버넌스 시스템) -> ITIL 4(서비스 가치 사슬) -> TOGAF(아키텍처) -> ISO 27001/27701(보안·개인정보)**로 대표되는 **통합 프레임워크**를 통해 실현된다.

```text
+------------------------------------------------------------------+
|        IT 경영 관리 4대 축 통합 프레임워크 (IT Management 4-Pillar) |
+------------------------------------------------------------------+

   +------------------- ① IT 거버넌스 (Governance) -----------------+
   |  - ISO 38500 / COBIT 2019                                    |
   |  - 이사회-경영진-IT의 책임·권한·의사결정 구조 (RACI)          |
   |  - IT Steering Committee(전사 IT운영위원회) 운영              |
   +------------------------+--------------------------------------+
                            | (정합·연결)
                            v
   +------------------- ② IT 전략·포트폴리오 (Strategy) ------------+
   |  - Business-IT Alignment(BSA) 전략맵                          |
   |  - IT 투자 포트폴리오: Run(60%) / Grow(25%) / Transform(15%)  |
   |  - EA(Enterprise Architecture) 기반 로드맵                    |
   +------------------------+--------------------------------------+
                            | (측정·환류)
                            v
   +--------------- ③ IT 성과·서비스 관리 (Performance) ------------+
   |  - ITIL 4 Service Value System (SVS)                          |
   |  - IT BSC 4관점(재무/고객/내부/학습성장) KPI                  |
   |  - SLA/OLA/UC, FinOps, DevOps/Platform Engineering           |
   +------------------------+--------------------------------------+
                            | (보장·규제)
                            v
   +------------------- ④ 정보보안·GRC (Security/GRC) -------------+
   |  - ISMS-P / ISO 27001 / 27701 / SOC 2                         |
   |  - Risk = Threat × Vulnerability × Asset Value               |
   |  - Zero Trust, DevSecOps, 공급망 보안(C-SCRM)                |
   +--------------------------------------------------------------+
                            | (피드백 루프: Plan-Do-Check-Act)
                            v
              +------------------------------+
              |  전사 IT전략위원회 (Quarterly) |
              |  CIO -> CEO -> Board 보고 체계 |
              +------------------------------+
```

**핵심 변화 흐름**: *"데이터센터 보유 -> 서비스 이용 -> 가치 창출"*의 3단계 진화, 그리고 **"IT 비용 항목(Expense)" -> "전략적 투자 자산(Strategic Asset)" -> "플랫폼 비즈니스(Platform Business)"**로의 가치 인식 전환이 필수적이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"배(선박)의 항해 시스템"**과 같다. 거버넌스는 항해 규정(국제해상충돌예방규칙), 전략은 나침반, 성과관리는 속도·연료계기, 보안·GRC는 구명정·보험이다. 4가지가 어우러지지 않으면 어떤 배도 안전하게 목적지에 도달할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 **표준 아키텍처**는 국제 표준화 기구(ISO)와 ISACA, AXELOS, The Open Group이 제시한 프레임워크의 **계층적 통합 구조**로 표현할 수 있다.

```text
+---------------------------------------------------------------------+
|           IT 경영 관리 계층 아키텍처 (3-Layer Architecture)         |
+---------------------------------------------------------------------+

   [Layer 1: 원칙·거버넌스 계층]   <-  WHAT (어떤 의사결정을?)
   +--------------------------------------------------------------+
   |  ISO 38500 6대 원칙:                                        |
   |   ① Responsibility (책임성)  ② Strategy (전략성)             |
   |   ③ Acquisition (획득성)     ④ Performance (성과성)          |
   |   ⑤ Conformance (준법성)     ⑥ Human Behavior (인간행태)     |
   |                                                               |
   |  COBIT 2019 5대 도메인 (40개 거버넌스·관리 목표):            |
   |   EDM(05) -> APO(14) -> BAI(11) -> DSS(06) -> MEA(04)          |
   +------------------------+-------------------------------------+
                            | Evaluate, Direct, Monitor (EDM)
                            v
   [Layer 2: 관리 체계 계층]       <-  HOW (어떻게 관리하는가?)
   +--------------------------------------------------------------+
   |  +---- ITIL 4 (SVS) ----+    +---- TOGAF ADM ----+        |
   |  |  Opportunity/Demand  |    |  A->B->C->D->E->F->G->H  |        |
   |  |  -> Value             |    |  Preliminary->Phasing|       |
   |  |  Guiding Principles  |    |  ->Migration Plan   |        |
   |  |  Governance->SVS      |    |  ->Implementation   |        |
   |  |  Practices (34개)    |    |  Governance (ADM)  |        |
   |  +----------------------+    +---------------------+        |
   |  +---- PMBOK 7 --------+    +---- ISO 27001/27701 --+     |
   |  |  8대绩效域 + 원칙    |    |  Plan-Do-Check-Act    |      |
   |  |  (8 Performance      |    |  93 Annex A 통제 항목 |      |
   |   Domains)             |    |  114 ISO 27701 PIMS   |      |
   |  +----------------------+    +-----------------------+     |
   +------------------------+-------------------------------------+
                            | 측정·실행
                            v
   [Layer 3: 운영·실행 계층]       <-  DO (실제 어떻게 수행하는가?)
   +--------------------------------------------------------------+
   |  클라우드/플랫폼  |  데이터/AI  |  보안/ZTNA  |  IT재무/FinOps|
   |  IaaS·PaaS·SaaS  |  DW·MLOps  |  SASE·SOAR  |  Showback     |
   |  K8s·Service Mesh |  DataOps   |  SBOM·C-SCRM|  Chargeback   |
   +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO 38500 / COBIT 2019** | IT 거버넌스 프레임워크 | 6대 원칙(ISO 38500) + 5대 도메인 40개 목표(COBIT 2019)로 **이사회(Board) -> 경영진(Executive) -> IT 운영(IT Operation)**의 3계층 의사결정 구조(RACI: Responsible, Accountable, Consulted, Informed)를 정의. **EDM(평가·지시·모니터링)** 사이클이 핵심 |
| **ITIL 4 Service Value System** | IT 서비스 관리 체계 | **Opportunity/Demand -> Value** 사슬, 7가지 Guiding Principles(실용주의·사고중심·진행에 따른 시작·협력·사고와 작업의 투명성 등), 34개 Practices(일반·서비스·기술관리), **Service Desk·Incident·Change·Problem** 4대 프로세스 운영 |
| **TOGAF ADM + EA** | 전사 아키텍처 방법론 | 8단계 ADM(Architecture Development Method) 사이클: **Preliminary -> Vision -> Business -> Information Systems -> Technology -> Opportunities -> Migration -> Implementation Governance -> Change Management**. **4A 아키텍처**(BA·DA·AA·TA)와 **ArchiMate 3.1** 표기법 활용 |
| **ISMS-P / ISO 27001:2022** | 정보보안 경영체계 | 93개 Annex A 통제 항목(Organizational 37 + People 8 + Physical 14 + Technological 34), **위험평가 = 자산가치 × 위협 × 취약성 × 영향도**, ISMS-P는 한국인터넷진흥원(KISA) 인증, 3년 주기 재인증 + 연 1회 사후심사 |
| **IT BSC + KPI** | IT 성과 측정 | 4관점(재무/고객/내부프로세스/학습성장) × **Lagging(결과) vs Leading(선행) 지표** 조합. 예: 재무(IT ROI) / 고객(서비스 만족도 NPS) / 내부(시스템 가용성 99.99%) / 학습(Digital Literacy Index) |
| **GRC 플랫폼** | 통합 거버넌스·리스크·컴플라이언스 | **RSA Archer / SAP GRC / ServiceNow GRC / OneTrust / LogicGate** 등. Risk Register, Control Mapping, Issue Tracking, Policy Management를 단일 워크플로우로 통합. **Three Lines of Defense(3LoD)** 모델 적용 |

### 핵심 알고리즘 및 공식

**(1) IT 투자 ROI 공식 (Total Economic Impact, TEI)**
$$TEI = \frac{(Benefits_{Tangible} + Benefits_{Intangible}) - (Cost_{Direct} + Cost_{Indirect})}{Total\ Cost\ of\ Ownership (TCO)}$$

**(2) 정보보안 위험도 산정 (ISO 27005 / NIST SP 800-30)**
$$Risk = Asset\ Value \times Threat \times Vulnerability$$
- 위험등급 = 5단계(Low=1, Medium=2, High=3, Very High=4, Critical=5) 또는 정성적 매트릭스

**(3) IT 거버넌스 성숙도 모델 (CMMI 5단계 또는 COBIT 5단계)**
- Level 1: Initial(혼돈) -> 2: Managed(반복) -> 3: Defined(표준화) -> 4: Quantitatively Managed(측정) -> 5: Optimizing(최적화)

**(4) EA 정합도 측정 (EA Maturity = Business-IT Alignment Score)**
$$Alignment = w_1 \cdot Strategy_{Fit} + w_2 \cdot Process_{Fit} + w_3 \cdot Data_{Fit} + w_4 \cdot Technology_{Fit}$$
- 일반적으로 가중치: 전략 0.4, 프로세스 0.3, 데이터 0.2, 기술 0.1

- **📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **"건강검진 시스템"**과 같다. ISO 38500은 "검진 원칙", COBIT은 "검진 항목표", ITIL은 "치료 매뉴얼", TOGAF는 "신체 구조도", ISMS-P는 "면역 체계 검사", BSC는 "건강 지표"에 해당한다. 6가지가 모두 갖춰져야 진정한 기업 건강이 달성된다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 핵심 프레임워크 간 비교는 기술사 시험에서 **"왜 A가 아닌 B를 선택했는가"**를 논증하기 위한 필수 논리 구조다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001:2022** | **TOGAF 10** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주요 목적** | IT 거버넌스·관리 목표 달성 | IT 서비스 가치 창출 | 정보보안 경영체계 인증 | 전사 아키텍처 구축 | 프로젝트 성과 달성 |
| **관점** | **거버넌스(상위)** | **운영 관리(중위)** | **보안 통제(전사)** | **아키텍처(설계)** | **프로젝트(임시적)** |
| **핵심 구조** | 5도메인 / 40 Governance & Management Objectives | 7 Guiding Principles / 34 Practices / SVS | PDCA + 93 Annex A 통제항목 | 8단계 ADM 사이클 | 12원칙 + 8绩效域 |
| **대상 조직** | CIO·이사회·IT Steering Committee | IT 운영팀·서비스 데스크 | CISO·보안 조직·전 임직원 | EA팀·아키텍트·전략기획 | PMO·프로젝트 매니저 |
| **인증/자격** | COBIT 2019 Foundation/Design&Implementation | ITIL 4 Foundation/MP/SL | ISO 27001 Lead Auditor/Implementer | TOGAF
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 748 / 800

<- **이전**: [747. IT 경영 관리 핵심 토픽 747번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/747_it_management_core_topic_747_exam_summary/)
**다음**: [749. IT 경영 관리 핵심 토픽 749번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/749_it_management_core_topic_749_exam_summary/) ->

---
