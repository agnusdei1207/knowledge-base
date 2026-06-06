---
title: "IT Management Core Topic 474 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019, ISO 27001, ITIL 4, PMBOK 7th 등 글로벌 IT 거버넌스 프레임워크를 통합하여 **계획(Plan) -> 구축(Build) -> 운영(Run) -> 모니터링(Monitor)** 의闭环(Closed-Loop) 라이프사이클 내에서 IT 투자 대비 가치(Value Delivery)와 위험(Risk)·자원(Resource) 간 최적 균형점을 지속적으로 추적·개선하는 경영 통제 체계
> 2. **가치**: 거버넌스 미적용 조직 대비 **프로젝트 실패율 40%v**(PMI 2021 Pulse of Profession), **컴플라이언스 위반 비용 평균 $4.05Mv**(IBM Cost of Data Breach 2023), IT 투자 ROI **15~25% 향상**(Gartner benchmark) 및 이사회-경영진-현업(CIO/CTO/CDO) 간 **단일 의사결정 언어(Single Pane of Glass)** 확보
> 3. **판단 포인트**: 프레임워크 전면 채택(Boiling the Ocean) vs. 핵심 영역 선도입(Crawl-Walk-Run) 전략, **RACI 매트릭스** 충실도, **KGI(핵심목표지표)·KPI(핵심성과지표)·CSF(핵심성공요인)** 3계층 인과 모델 설계, 그리고 **내부통제(Internal Control)·내부감사(Internal Audit)·외부감사(External Audit)·감리(Inspection)** 4-라인 방어 모델(Three Lines of Model + IT extension) 정합성 검증

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation, DX)·클라우드 네이티브·생성형 AI(LLM)·양자컴퓨팅·Web3·ESG 공시 의무화가 동시 진행되는 VUCA(Volatility, Uncertainty, Complexity, Ambiguity) 환경에서, IT는 더 이상 "비용 센터(Cost Center)"가 아닌 **"비즈니스 코어(Business Core)"** 이자 **"전략적 무기(Strategic Weapon)"** 입니다. 한국정보화진흥원(NIA)의 「정보시스템 감리 기법 및 절차」, 금융위원회의 「전자금융감독규정」, 개인정보보호법·정보통신망법·클라우드컴퓨팅법·AI기본법(2026.1 시행) 등 **업종별 컴플라이언스 매트릭스**가 매년 15~20%씩 복잡도가 증가하여, 단일 부서(예: IT팀) 독자적인 통제 한계가 명백해졌습니다.

또한 **사이버 위협** 측면에서, 2023년 국내 랜섬웨어 피해액은 1,300억원(과학기술정보통신부), 평균 다운타임 21일, **공급망 공격(SolarWinds, 3CX, Okta 사례)** 증가로 인해 4th Party Risk(4PR) 통제 필요성이 대두되었습니다. IT 거버넌스는 이 모든 것을 **"정량적 측정 -> 정성적 판단 -> 지속적 개선"** 의 Deming Cycle(PDCA)에 통합하는 경영 인프라입니다.

```text
+------------------------------------------------------------------+
|           IT 거버넌스 & 정보시스템 감리 3-tier 통합 구조           |
+------------------------------------------------------------------┒
|  Tier 1 -- 의사결정 계층(Board / Steering Committee)              |
|  +------------------------------------------------------------+  |
|  |  • IT전략위원회(ISSC) -- 분기 1회 정례 / CIO + CISO + CFO |  |
|  |  • 디지털윤리위원회(AI Ethics) -- EU AI Act·국내 AI기본법  |  |
|  |  • 리스크관리위원회(RMC) -- ISO 31000 ERM 연계              |  |
|  |  산출물: 정책(Policy) / 지침(Guideline) / 표준(Standard)    |  |
|  +------------------------------------------------------------+  |
|                          ^                                       |
|                          | 정책·지침·표준(Policy)                |
|  Tier 2 -- 통제 계층(Governance & Management Practices)          |
|  +------------------------------------------------------------+  |
|  | EDM(Evaluate, Direct, Monitor) -- COBIT 2019의 거버넌스  |  |
|  | +----------+ +----------+ +----------+ +----------+       |  |
|  | | APO(Align | | BAI(Build | | DSS(Deliver| | MEA(Monitor|   |  |
|  | | Plan Org)| | Acquire  | | Service   | | Evaluate  |     |  |
|  | | 14 proc. | | Implement| | Support)  | | Assess)   |     |  |
|  | |          | | 11 proc. | | 6 proc.   | | 4 proc.   |     |  |
|  | +----------+ +----------+ +----------+ +----------+       |  |
|  |  + Change Enablers(7가지: Principles, Goals, Components…)   |  |
|  +------------------------------------------------------------+  |
|                          ^                                       |
|                          | 통제 활동(Control Activities)        |
|  Tier 3 -- 실행 계층(Operational / Project / Service)             |
|  +------------------------------------------------------------+  |
|  |  프로젝트 단위: PMBOK 7th / PRINCE2 / SAFe 6.0             |  |
|  |  서비스 단위: ITIL 4 (34 Practice, SVS: Service Value Sys)  |  |
|  |  보안 단위: ISO 27001/27002 / NIST CSF 2.0 / ISMS-P        |  |
|  |  감리 단위: NIA 정보시스템 감리 / SSAC / SSAS               |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

**전통적 IT관리(2000년대)** vs. **현대 IT 거버넌스(2024~)**

| 시대 | 패러다임 | 의사결정 | 통제 방식 | KPI |
|---|---|---|---|---|
| 2000s | IT Cost Center | CIO 독단 | 수동 점검 / 연 1회 | 가용성(Uptime) |
| 2010s | IT Service | IT Steering Committee | COBIT 5 + ITSM | SLA / incident MTTR |
| 2020s | Digital Business | CxO 협업 / OKR | COBIT 2019 + NIST CSF 2.0 | NPV / ROIC / Risk Score |
| 2025~ | AI-Native / Autonomous Governance | AI Co-Pilot 의사결정 보조 | Continuous Control Monitoring(CCM) / GRC 자동화 | Real-time Risk-Adjusted Value |

- **📢 섹션 요약 비유**: IT 거버넌스는 **"도시의 종합교통관제센터"** 와 같습니다. 도시가 커지고 차량(데이터)·보행자(사용자)·자전거(IoT 센서)·드론(AI)이 혼재할 때, 단순히 신호등 하나만 두는 게 아니라 **신호 타이밍(정책)·차선(아키텍처)·CCTV(모니터링)·신고 112(감사)** 가 통합되어야 사고율(MTTR)을 낮출 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**COBIT 2019 핵심 메타 모델(System Structure)** 은 **"40개 거버넌스·관리 목적(40 Governance & Management Objectives)"** 이 **"7개 구성요소(7 Components of Governance System)"** 위에서 운영되고, 이는 **"5개 원칙(5 Principles)"** 에 의해 안내되며, **"목표 계층구조(Goals Cascade)"** 로 비즈니스 목적과 연결되는 **원리주의(Principle-based) 프레임워크**입니다.

```text
[COBIT 2019 Cascade Model — Goals -> Components -> Practices]

  Stakeholder Needs(관심사·이해관계자 요구)
  -----------------------------------------
      |  Translate
      v
  Enterprise Goals(13개) — 예: EG01 포트폴리오 최적화, EG06 운영 신뢰성
      |  Align
      v
  Alignment Goals(13개) — 예: AG01 IT 준법, AG09 정보처리 적합성
      |  Decompose
      v
  Governance & Management Objectives(40개) — EDM05(보안)·DSS01(운영)·MEA01(성능)…
      |  Map
      v
  +----------------------------------------------------------+
  |  7 Components of Governance System                       |
  |  +-------------------------------------------------+    |
  |  | 1) Process(40개 프로세스, Capability Level 0~5)  |    |
  |  | 2) Organizational Structures(RACI, SteerCo)       |    |
  |  | 3) Information Flows(Inputs -> Outputs)            |    |
  |  | 4) People, Skills & Competencies(Skills Matrix)   |    |
  |  | 5) Policies & Procedures(SoA: Statement of Applic.) |    |
  |  | 6. Culture, Ethics & Behavior(Tone at the Top)    |    |
  |  | 7. Services, Infrastructure & Applications(기술) |    |
  |  +-------------------------------------------------+    |
  |  + 7 Change Enablers: 변동성·복잡성·위험 정량화         |
  +----------------------------------------------------------+
      |  Apply
      v
  Capability Level(0~5) / Maturity Level(0~5) — PAM(Process Assessment Model)
      |  Measure
      v
  Focus Area(Industry/Style/Issue-Specific) — e.g., DevOps, Cyber Security, ESG
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(Evaluate·Direct·Monitor)** | 거버넌스 의사결정 | 5개 프로세스(EDM01~05) / 이사회·위원회 운영 / 무결성·투명성·책임성 |
| **APO(Align·Plan·Organize)** | 전략 정렬·계획·조직화 | 14개 프로세스(APO01~14) / **IT 전략 맵**(Strategy Map) / **포트폴리오 관리**(PfM) / **RACCI 매트릭스** |
| **BAI(Build·Acquire·Implement)** | 솔루션 구축·도입 | 11개 프로세스(BAI01~11) / **PRINCE2**·**SAFe**·**DevOps**·**CI/CD**·**IaC(Terraform, Ansible)** |
| **DSS(Deliver·Service·Support)** | 운영·서비스·지원 | 6개 프로세스(DSS01~06) / **ITIL 4**(34 Practice) / **AIOps** / **SRE Golden Signals** |
| **MEA(Monitor·Evaluate·Assess)** | 성과·내부통제 평가 | 4개 프로세스(MEA01~04) / **ISAE 3402** / **SOC 1/2/3** Type II / **Continuous Auditing**(ACL, IDEA) |
| **Risk & Security Overlay** | 위험·보안 통제 | ISO 27005 Risk Treatment / NIST CSF 2.0 GV/ID/PR/DE/RS/RC / **제로트러스트**(NIST SP 800-207) / **ISMS-P 인증**(국내) |
| **GRC Platform Layer** | 통합·자동화·리포팅 | **ServiceNow GRC** / **Archer** / **SAP GRC** / **OneTrust** / **LogicGate** — 제어 매핑(Control Mapping) 자동화 |

**핵심 산식 및 측정 모델**

1. **Process Capability Level (ISO 33020:2015 + COBIT PAM 2019)**
   - Level 0: Incomplete (불완전)
   - Level 1: Performed (수행) — 프로세스 목적 달성
   - Level 2: Managed (관리) — 작업 산출물 관리
   - Level 3: Established (확립) — 조직 표준 정의·사용
   - Level 4: Predictable (예측 가능) — 정량적 관리, 통계적 통제
   - Level 5: Innovating (혁신) — 지속적 개선·혁신
   - **측정 산식**: `Process Attribute Rating(0~100%) -> R(Required)·A(Approach)·D(Deployment)·G(Governance)·M(Management)·W(Work Products)` 6-PA 구조

2. **COBIT Goals Cascade Balanced Scorecard 4-View**
   - **Financial(EG01~03)** : IT 비용 / 예산 준수율 / CapEx·OpEx 비율
   - **Customer(EG04~06)** : SLA / NPS / 사용자 만족도
   - **Internal Process(EG07~12)** : 변경 성공률 / 결함 밀도 / 취약점 평균 탐지시간(MTTD)
   - **Learning & Growth(EG13)** : 직원 인증 보유율 / 교육 시간 / 핵심 인재 유지율

3. **Risk Score = Likelihood(1~5) × Impact(1~5) × Inherent Risk × Control Effectiveness(0~1)**
   - **Inherent Risk Score(IRS)** = L × I
   - **Residual Risk Score(RRS)** = IRS × (1 - Control Effectiveness)
   - **Risk Treatment Decision Matrix**: Avoid / Reduce / Transfer(보험·아웃소싱) / Accept(RSS < 10)

4. **Value Delivery ROI**
   - `ROI = (Tangible Benefits + Intangible Benefits - Total Cost of Ownership) / TCO`
   - **TCO 구성**: CAPEX(하드웨어·소프트웨어) + OPEX(인건비·라이선스·전력·냉각·교육·유지보수) + Risk Cost(SLE × ARO) + EOL 비용

- **📢 섹션 요약 비유**: COBIT 2019의 7 Components는 **"요리 레시피의 7가지 필수 요소"** 와 같습니다. 좋은 요리(거버넌스)를 위해선 (①재료=Process, ②주방장=People, ③주방 도구=Infrastructure, ④레시피북=Policies, ⑤공급망=Information Flow, ⑥주방 분위기=Culture, ⑦주방 레이아웃=Structure) 가 모두 갖춰야 고객(Stakeholder)이 맛있는 요리(Value)를 받습니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001:2022** | **PMBOK 7th** | **NIST CSF 2.0** |
|---|---|---|---|---|---|
| **목적** | IT 거버넌스·관리 전체 | IT 서비스 관리(Service Management) | 정보보호 경영체계(ISMS) | 프로젝트 관리 표준 | 사이버 보안 위험관리 |
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 474 / 800

<- **이전**: [473. IT 경영 관리 핵심 토픽 473번 시험 요약](/studynote/12_it_management/05_security_compliance/473_it_management_core_topic_473_exam_summary/)
**다음**: [475. IT 경영 관리 핵심 토픽 475번 시험 요약](/studynote/12_it_management/05_security_compliance/475_it_management_core_topic_475_exam_summary/) ->

---
