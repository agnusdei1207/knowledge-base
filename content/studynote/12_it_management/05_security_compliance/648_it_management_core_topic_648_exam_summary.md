+++
title = "648. IT 경영 관리 핵심 토픽 648번 시험 요약 (IT Management Core Topic 648 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019/ISO 38500) -> 전략(ISO 38500/IT-Strategy) -> 포트폴리오(PfM/PfE) -> 서비스(ITIL 4) -> 성과(BSC/CSI) 의 5계층 통합 체계로, IT 자산을 기업 가치(Value Realization)와 정렬(Alignment)하는 엔드투엔드 경영관리 프레임워크
> 2. **가치**: McKinsey 사례 기준 IT-Business Alignment 성숙도 1단계 상승 시 기업 EBITDA 5~12% 개선, Gartner 통계 IT 거버넌스 도입 시 프로젝트 성공률 35% -> 75% 상승, TCO 20~30% 절감
> 3. **판단 포인트**: 중앙집중형(Federal) vs 분산형(Federated) 거버넌스 구조 선택, COBIT 2019 40개 governance/management objective 중 우선순위 도출, BSC 4관점(Financial/Customer/Internal Process/Learning & Growth) KPI 균형 설계
```

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입을 넘어 **IT를 경영 자산(Capital Asset) 및 서비스 플랫폼으로 재정의**하는 경영관리 패러다임이 필수. 과거 2000년대 초반 IT는 비용센터(Cost Center)로 인식되어 예산 통제 위주의 관리가 주였으나, 현재는 **디지털 전환(Digital Transformation)**, **AI·클라우드·데이터 경제** 환경에서 IT가 **전략적 차별화 원천**이자 **수익 창출 엔진**으로 변모.

이에 따라 COBIT 2019, ISO/IEC 38500, ITIL 4, PMBOK 7, TOGAF 10, ISO 21500 등 다양한 거버넌스·관리 프레임워크가 등장했고, 이들을 통합적으로 운용하는 **IT 경영관리(Enterprise IT Management, EITM)** 체계가 요구됨.

### 📊 IT 경영관리 5계층 모델

```text
        +-----------------------------------------+
        |  Layer 5: 성과/측정 (Performance)       |  <- BSC, CSI, KPI Dashboard
        |  -----------------------------------    |
        |  Layer 4: 서비스 운영 (Service Ops)     |  <- ITIL 4 (Service Value System)
        |  -----------------------------------    |
        |  Layer 3: 포트폴리오 (Portfolio)         |  <- PfM, PfE, Demand Mgmt
        |  -----------------------------------    |
        |  Layer 2: 전략/계획 (Strategy)           |  <- IT Strategy, EA, SISP
        |  -----------------------------------    |
        |  Layer 1: 거버넌스 (Governance)          |  <- COBIT 2019, ISO 38500
        +-----------------------------------------+
                        ^
                        |  Feedback Loop (CSI)
                        v
        +-----------------------------------------+
        |    Business Value & Digital Ecosystem   |
        |  (Revenue, CX, Market Cap, ESG)         |
        +-----------------------------------------+
```

### 과거 vs 현대 IT 경영관리 패러다임

| 구분 | 1990~2000 (Legacy) | 2010~현재 (Modern) | 2024~ (Future) |
|------|-------------------|---------------------|----------------|
| **관점** | IT = 비용(Cost) | IT = 자산(Asset) | IT = 플랫폼(Platform) |
| **관리 대상** | 인프라(HW/SW) | 애플리케이션+프로세스 | 데이터+AI+생태계 |
| **구조** | Silo, 수직통합 | SOA, EAI/ESB | Cloud-Native, MSA, API Economy |
| **거버넌스** | Sarbanes-Oxley 컴플라이언스 | COBIT 5, ITIL v3 | COBIT 2019, ISO 38500, AI 거버넌스 |
| **성과측정** | ROI 단순 산출 | EVA, IT-BSC | Value Realization, NPV + OKR |
| **조직** | CIO(보고만) | CIO + CDO | CIO + CDO + CAIO + CISO |
| **예산** | CapEx 중심 | OpEx 혼합 | FinOps + Consumption-Based |

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **자동차의 통합 계기판**과 같습니다. 연료(예산), 속도(성과), 엔진온도(리스크), 네비게이션(전략)을 한 화면에서 보며 운전(경영)하는 것과 같아, 5계층 모델은 각각의 다이얼에 해당합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### COBIT 2019 Governance System 구조 (40 Objectives)

```text
+----------------------------------------------------------+
|                  COBIT 2019 Core Model                   |
|                                                          |
|   +--------------+  +--------------+  +--------------+  |
|   | Governance   |  | Management   |  | Management   |  |
|   | Objectives   |  | Objectives   |  | Objectives   |  |
|   |  (5 EA)      |  | (Aligned)    |  | (Aligned)    |  |
|   |              |  | P1~P5        |  | P6~P35       |  |
|   +------+-------+  +------+-------+  +------+-------+  |
|          |                 |                 |          |
|          v                 v                 v          |
|   +--------------------------------------------------+  |
|   |  7 Components of Governance System                |  |
|   |  1. Process  2. Organizational Structures        |  |
|   |  3. Information Flows  4. People, Skills         |  |
|   |  5. Policies, Procedures  6. Services, Infra     |  |
|   |  7. Culture, Ethics, Behavior                    |  |
|   +--------------------------------------------------+  |
|                          |                               |
|   +----------------------v--------------------------+   |
|   |  Design Factors (11개) -> Priority 결정          |   |
|   |  · Enterprise Strategy · Risk Profile           |   |
|   |  · I&T-related issues · Threat Landscape         |   |
|   |  · Compliance Requirements · Role of IT         |   |
|   |  · Sourcing Model · IT Implementation Methods   |   |
|   |  · Technology Adoption · Size of Enterprise     |   |
|   +-------------------------------------------------+   |
+----------------------------------------------------------+
```

### 5개 거버넌스 목표 (EDM - Evaluate, Direct, Monitor)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|----------|------|----------------------|
| **EDM01 - Governance Framework Setting** | 거버넌스 체계 수립 | COBIT 2019 Design Factor 매핑, RACI Matrix, Governance Charter 작성, 11개 Design Factor별 우선순위 가중치 산정 |
| **EDM02 - Benefits Delivery** | 가치 실현(Value Realization) | Benefits Realization Plan, NPV/IRR 계산, KPI Cascade, OKR 연결, Benefits Tracking Register 운영 |
| **EDM03 - Risk Optimization** | 리스크 최적화 | Risk Appetite/Tolerance 설정, Risk Heat Map, ISO 27005 연계, KRI(Key Risk Indicator) 모니터링 |
| **EDM04 - Resource Optimization** | 자원 최적화 | FinOps, Capacity Planning, TCO 분석, Showback/Chargeback, 클라우드 비용 최적화 (Reserved/On-Demand) |
| **EDM05 - Stakeholder Transparency** | 이해관계자 투명성 | Steering Committee 운영, ESG 리포팅, IT Performance Dashboard, 정기적 Stakeholder Communication |

### 핵심 운영 원리: RACI & 3 Lines of Defense

```text
+---------------------------------------------------------+
|              3 Lines of Defense Model                   |
|                                                         |
|  1st Line: Operational Management (Business + IT)        |
|  · 위험을 일상적으로 식별·관리                           |
|  · Control Owner, Process Owner                         |
|                                                         |
|  2nd Line: Risk Management & Compliance                 |
|  · CRO, CISO, DPO, 내부감사지원                         |
|  · 정책·표준 수립, 모니터링, 자문                       |
|                                                         |
|  3rd Line: Internal Audit (Independent Assurance)       |
|  · CAE(Chief Audit Executive) 주관                      |
|  · 1·2nd Line에 대한 독립적 검증                        |
+---------------------------------------------------------+

        RACI Matrix 예시 (IT 투자심의)
        +--------------+-----+-----+-----+-----+
        | Activity     | CIO | CFO | CEO | BUs |
        +--------------+-----+-----+-----+-----+
        | 전략수립     |  R  |  C  |  A  |  C  |
        | 우선순위결정 |  C  |  C  |  A  |  R  |
        | 예산할당     |  R  |  A  |  C  |  I  |
        | 성과측정     |  R  |  C  |  A  |  I  |
        +--------------+-----+-----+-----+-----+
        R=Responsible, A=Accountable, C=Consulted, I=Informed
```

- **📢 섹션 요약 비유**: COBIT 2019의 EDM 5개 목표는 **자동차의 5대 필수 액세서리**와 같습니다. EDM01(핸들=방향), EDM02(엔진=추진력), EDM03(브레이크=리스크), EDM04(연료계=자원), EDM05(백미러=투명성)로, 어느 하나라도 없으면 안전한 운행이 불가능합니다.

---

## Ⅲ. 비교 및 연결

### IT 경영관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** | **TOGAF 10** |
|------|---------------|-----------|--------------|-------------|--------------|
| **주 목적** | 거버넌스 & 관리 | 서비스 운영 | IT 거버넌스 원칙 | 프로젝트 관리 | EA 방법론 |
| **관점** | Enterprise 전체 | IT 서비스 | Board Level | 프로젝트 | 아키텍처 |
| **핵심 개념** | 40 Governance/Management Objectives | Service Value System (SVS) | 6 Principles + Model | 12 Principles + 8 Domains | ADM(Architecture Development Method) |
| **적용 범위** | 전략~운영 전계층 | 운영·서비스계층 | 전략·거버넌스 | 프로젝트 라이프사이클 | 아키텍처 설계 |
| **성숙도 모델** | CMMI 0~5 | 5단계(Initial->Optimizing) | Self-Assessment | OPM3 | ACMG |
| **연계 프레임워크** | NIST CSF, ISO 27001 | DevOps, Lean, Agile | COBIT, ITIL | Agile, Scrum | Zachman, FEAF |
| **적합 조직** | 대기업·금융·공공 | 서비스 중심 조직 | 모든 규모 | 프로젝트 성숙 조직 | EA 도입 기업 |
| **2024년 트렌드** | AI 거버넌스 추가 | Sustainability Practice | AI 윤리 가이드 | Hybrid-Agile | Microservices EA |

### 다른 시스템 컴포넌트와의 통합

```text
+--------------------------------------------------------------+
|                IT 경영관리 생태계 통합 아키텍처                |
|                                                              |
|   +--------------+  +--------------+  +--------------+       |
|   |  ERP (SAP)   |  |  ITSM (SF)   |  |  GRC (RSA)   |       |
|   +------+-------+  +------+-------+  +------+-------+       |
|          |                 |                 |               |
|          +-----------------+-----------------+               |
|                            v                                 |
|              +--------------------------+                    |
|              |  ESB / API Gateway       |                    |
|              |  (MuleSoft, Apigee)      |                    |
|              +------------+-------------+                    |
|                           v                                  |
|         +-------------------------------------+              |
|         |  통합 데이터 레이크 + 분석 플랫폼     |              |
|         |  (Snowflake, Databricks, BigQuery)   |              |
|         +------------+------------------------+              |
|                      v                                       |
|       +------------------------------------------+           |
|       |  경영관리 대시보드 / 의사결정 지원        |           |
|       |  (Power BI, Tableau, Looker)             |           |
|       |  + AI 기반 예측·시뮬레이션 엔진          |           |
|       +------------------------------------------+           |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 5대 프레임워크는 **자동차의 5종 공구함**과 같습니다. COBIT 2019는 종합 진단기, ITIL 4는 정비 매뉴얼, ISO 38500는 운전자 교본, PMBOK 7는 부착 가이드, TOGAF 10은 설계도면으로, 차종(조직 상황)에 따라 적절히 조합해 사용합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### IT 경영관리 성숙도 5단계 모델 (CMMI 기반)

```
Level 1 (Initial) -----> Level 2 (Managed) -----> Level 3 (Defined) -----> Level 4 (Quantitatively Managed) -----> Level 5 (Optimizing)
  Ad-hoc                프로젝트 단위 관리         전사 표준화            정량적 관리                지속적 혁신
  (PoC만 존재)          (반복 가능)              (문서화·표준화)        (예측 가능·통제)          (학습·개선)
```

### 기술사형 판단 체크리스트

1. **거버넌스 구조 선택**: 조직의 다국적·다사업장 특성을 고려해 **Federal(중앙)** vs **Federated(분권)** vs **Hybrid** 구조 중 선택했는가? 의사결정 속도와 통제력 간 트레이드오프 분석을
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 648 / 800

<- **이전**: [647. IT 경영 관리 핵심 토픽 647번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/647_it_management_core_topic_647_exam_summary/)
**다음**: [649. IT 경영 관리 핵심 토픽 649번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/649_it_management_core_topic_649_exam_summary/) ->

---
