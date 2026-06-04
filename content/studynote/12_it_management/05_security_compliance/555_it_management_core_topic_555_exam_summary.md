---
title: "555. IT 경영 관리 핵심 토픽 555번 시험 요약 (IT Management Core Topic 555 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ISO/IEC 38500, ITIL 4 프레임워크를 기반으로 **거버넌스-전략-포트폴리오-서비스-리스크-보안** 6대 축을 통합해 비즈니스 가치(Business Value)를 극대화하는 **Value Governance Loop** 체계이다.
> 2. **가치**: McKinsey 보고에 따르면 효과적인 IT 거버넌스 도입 기업은 **Time-to-Market 35% 단축, IT 비용 15~25% 절감, 프로젝트 성공률 3배 증가**(PMI 2021 기준) 효과를 거두며, 포트폴리오 우선순위 재정렬로 **죽은 프로젝트(Dead Project) 비율을 40%->8%** 수준으로 낮출 수 있다.
> 3. **판단 포인트**: 중앙집중(CoE) vs 분산(Federated) 거버넌스, Build vs Buy vs Rent 의사결정, **TCO 3~5년 총비용 비교**, **NPV/IRR/Risk-Adjusted ROI** 산정, 그리고 **SLA 99.9% vs 99.99%**(연 8.76h vs 52.6m 장애시간) 트레이드오프가 핵심 설계 변수다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 시대에 IT는 더 이상 백오피스 지원기능이 아니라 **전략적 차별화 자산(Strategic Differentiator)**이다. 그러나 2023년 PMI 보고에 따르면 전 세계 IT 프로젝트의 **35%가 실패**(요구사항 미충족, 예산 초과, 가치 미실현)하며, 한국 정보화진흥원의 국내 SI 사업 통계에서도 평균 **예산 초과율 217%**, **일정 지연율 89%**가 보고된다. 이 근본 원인은 **(1) IT-비즈니스 전략 정렬 실패(Strategic Misalignment) (2) 거버넌스 부재下的의 무분별한 투자 (3) 서비스 품질 측정 부재 (4) 리스크/보안 통제 실패**로 귀결된다.

IT 경영 관리(Information Technology Management)는 **계획(Plan) -> 조직(Organize) -> 통제(Control) -> 성과측정(Measure) -> 개선(Improve)**의 Deming Cycle(PDCA)을 IT 영역에 적용해, **IT 거버넌스(IT Governance)** 체계를 통해 **이해관계자(Stakeholder)**에게 **투명성(Transparency)·책임성(Accountability)·공정성(Fairness)·독립성(Independence)**을 보장하는 경영 활동이다.

```text
[ IT 경영 관리 6대 핵심 영역 통합 구조도 ]

              +-----------------------------------------+
              |   비즈니스 전략 (Business Strategy)       |
              |   - Vision/Mission/CSF                   |
              +---------------+-------------------------+
                              |  SAM (Strategic Alignment Model)
                              v
   +--------------------------------------------------------+
   |              IT 거버넌스 (IT Governance)                  |
   |  +----------+  +----------+  +----------+  +--------+ |
   |  | 전략     |->| 포트폴리오|->| 서비스   |->| 리스크 | |
   |  | (Strategy)|  | (Portfolio)| |(Service) |  |(Risk)  | |
   |  +----------+  +----------+  +----------+  +--------+ |
   |       |             |              |            |      |
   |       +-------------+------+-------+------------+      |
   |                            v                            |
   |                  +------------------+                    |
   |                  | 보안·컴플라이언스|                    |
   |                  |  (Security/GRC)  |                    |
   |                  +------------------+                    |
   +--------------------------------------------------------+
                              |
                              v  Value Realization Loop
              +-----------------------------------------+
              |   성과 측정 (BSC/KPI/OKR) -> 개선 -> 보고  |
              +-----------------------------------------+
```

**변화 패러다임**:
- **기존(2000년대)**: 프로젝트 중심(Project-Oriented) -> 일회성 투자, ROI 미측정, **폐기율 70%** (Standish Group CHAOS Report)
- **현재(2020년대)**: 제품/서비스 중심(Product-Centric) -> 지속적 가치 전달, **OKR/KPI 기반 측정**, **FinOps**, **Platform Engineering** 패러다임
- **핵심 전환 키워드**: CAPEX -> OPEX, Build -> Buy -> Subscribe, Waterfall -> Agile -> **Lean-Agile-SAFe(Scaled Agile Framework)**, On-Premise -> Hybrid/Multi-Cloud

- **📢 섹션 요약 비유**: IT 경영 관리는 **배의 항해 시스템**과 같다. 목적지(비즈니스 전략)와 좌표(GPS·거버넌스)가 없으면 폭풍(시장변화)에 표류하며, 항해장(IS Steering Committee)·나침반(KPI)·손상방지(BIA/BCP)가 없으면 난파한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 3대 프레임워크 매핑

| 프레임워크 | 영역 | 핵심 구조 | 적용 계층 |
| :--- | :--- | :--- | :--- |
| **COBIT 2019** | 거버넌스·관리 | 40개 Governance/Management Objective, 5개 도메인(EDM/APO/BAI/DSS/MEA) | 상위 의사결정 |
| **ITIL 4** | 서비스 운영 | 34개 Practice, Service Value System(SVS), 4D Model | 중간 운영/서비스 |
| **ISO/IEC 38500** | 이사회 거버넌스 | 6원칙(책임·전략·수행·적합성·규율·윤리) | 최상위 정책 |

### 2. IT-비즈니스 전략 정렬 모델 (Henderson & Venkatraman SAM)

```text
[ Strategic Alignment Model (SAM) - 4관점 매트릭스 ]

   +------------------------+------------------------+
   |  외부 환경(External)    |  내부 환경(Internal)    |
   | +----------+----------+ | +----------+----------+ |
   | |  STRATEGY|  IT      | | |INFRASTR. |  IT      | |
   | |  - 고객  |  STRATEGY| | |PROCESS   |  SKILL   | |
   | |  - 경쟁  |  - 아키텍| | |          |  - 인력  | |
   | |  - 규제  |  - 표준  | | |          |  - 문화  | |
   | |   (A)    |   (B)    | | |   (C)    |   (D)    | |
   | |  전략->IT |  IT->전략 | | |  인프라  |  IT인재  | |
   | |   정렬   |   정렬   | | |   정렬   |   정렬   | |
   | +----------+----------+ | +----------+----------+ |
   |  ★ 고객가치/시장기회 -> ★ IT역량 차별화 -> |  ★ 내부 역량/프로세스  |
   | ★ 조직역량 -> IT가치 실현                |
   +------------------------+------------------------+
              ^              Strategic Fit
              |       (Business ↔ IT 양방향)
              +-----------------------------+
```

| SAM 4관점 | 핵심 질문 | 주요 산출물 |
| :--- | :--- | :--- |
| **A. Strategy -> IT** | "비즈니스가 IT에 무엇을 요구하는가?" | IT 기능요구서(Functional Spec), 우선순위 맵 |
| **B. IT -> Strategy** | "IT가 비즈니스에 어떤 새 기회를 주는가?" | 신기술 PoC, Innovation Roadmap (AI/Blockchain/Cloud) |
| **C. Infrastructure & Process** | "현재 인프라/프로세스로 전략 수행이 가능한가?" | EA(Enterprise Architecture) 갭분석, TOGAF ADM |
| **D. IT Skills & Culture** | "조직/인재/문화가 IT 전략을 지원하는가?" | 조직진단, 직무재설계(Job Redesign), **DevSecOps** 문화 |

### 3. IT 포트폴리오 관리(PPM) - 5단계 게이트 프로세스

```text
[ IT 투자 포트폴리오 의사결정 흐름도 ]

[ 1. Identify ]  ->  [ 2. Evaluate ]  ->  [ 3. Select ]  ->  [ 4. Prioritize ]  ->  [ 5. Control ]
   후보수집           다기준평가          포트폴리오진입        자원배분           성과모니터링
   v                  v                   v                   v                 v
 +------+         +--------+         +----------+        +----------+     +----------+
 |잠재 |         |재무성적|         |Tier1(필수)|        |자원 할당  |     |KPI추적  |
 |아이템|  --->   |+전략성 |  --->    |Tier2(전략)|  --->   | - CAPEX  | ---> |Risk Log |
 |수집  |         |+리스크 |         |Tier3(기회)|        | - OPEX   |     |Stage-Gate|
 +------+         +--------+         |Tier4(보류)|        | - 인력   |     +----------+
                                    +----------+        +----------+
   도구: APQC PCF,   방법: AHP/      도구: Gartner     도구: Top-down     도구: Earned
   MS Project     MCDA/DEA         Magic Quadrant    vs Bottom-up      Value Management
   Portfolio       Scoring          (2x2 매트릭스)      Steering          (EVM)
```

### 4. IT 서비스 관리(SLA) 계층 구조

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **SLA (Service Level Agreement)** | 고객-공급자 간 서비스 수준 협약 | 가용성(99.9% / 99.95% / 99.99%), 응답시간(MTTR 30분), 처리량(TPS), **벌금(SLA Credit) 산정**: 미달율 × 월정액 × SLA Credit% |
| **OLA (Operational Level Agreement)** | 내부 부서간 지원 협약 | 인프라팀-N/W팀-DB팀간 MTTR, RTO/RPO 협약, 내부 에스컬레이션 SLA |
| **UC (Underpinning Contract)** | 외부 벤더-내부 부서간 협약 | ISP 회선 가용성, 클라우드(AWS EC2 SLA 99.99%) 등 외부 의존성 계약 |
| **CSI (Continual Service Improvement)** | 지속적 서비스 개선 | ITIL 7단계 개선 프로세스(비전->범위->데이터->분석->제안->실행->검토), **PDCA 사이클 평균 90일** |
| **CSI Register** | 개선과제 백로그 | Kaizen 아이디어, Pain Point Tracking, **CSI Scoring Matrix**(임팩트×노력) |
| **Service Catalog** | 서비스 카탈로그 | 비즈니스 서비스 vs 기술 서비스 구분, **단가표(Unit Price)** 포함, **ServiceNow/Helix ITSM** 도구 활용 |

### 5. TCO(총소유비용) 계산 모델 (5년 기준 예시)

```
TCO = 직접비 + 간접비
    = (HW + SW + 네트워크 + 데이터센터 + 라이선스)     [직접 CAPEX]
    + (인건비 + 교육 + 유지보수 + 컨설팅 + 다운타임손실)  [간접 OPEX]
    + (마이그레이션 + 전환 + 데이터 손실위험)             [전환비용]
```

**On-Premise vs Public Cloud TCO 비교 예시** (1,000 VM, 5년):
| 항목 | On-Premise | Public Cloud(AWS) |
| :--- | :---: | :---: |
| HW/스토리지 | 80억 | 0 |
| 라이선스(SQL/Oracle) | 30억 | 20억(RDS) |
| IDC/전력/냉방 | 15억 | 0 |
| 운영인력 (10명×5년) | 50억 | 20억(MSP) |
| 클라우드 사용료(5년) | 0 | 110억 |
| **TCO 합계** | **175억** | **150억** |
| 유연성/탄력성 | 낮음 | **높음** |

-> **가치 기반 판단**: 단순 TCO 외에 **옵션가치(Option Value)**, **민첩성(Agility)**, **혁신속도(Time-to-Market)**를 가중해 의사결정.

- **📢 섹션 요약 비유**: COBIT은 **헌법**, ITIL은 **교과서**, ISO 38500은 **이사회 행동강령**이다. 마치 자동차의 **엔진(COBIT) + 매뉴얼(ITIL) + 안전규칙(ISO 38500)**처럼 서로 다른 추상화 레이어에서 IT 경영을 지탱한다.

---

## Ⅲ. 비교 및 비교 연결

### 1. IT 거버넌스 vs IT 관리 vs IT 운영

| 구분 | IT 거버넌스 (Governance) | IT 관리 (Management) | IT 운영 (Operation) |
| :--- | :--- | :--- | :--- |
| **관점** | 의사결정·감독·책임 | 계획·조직·지휘 | 실행·모니터링·개선 |
| **책임 주체** | 이사회, CIO, IT Steering Committee | CIO, IT PMO, 서비스 매니저 | 현장 엔지니어, SRE, 헬프데스크 |
| **핵심 질문** | "올바른 일을 하고 있는가?" (Doing the right things) | "올바르게 일하고 있는가?" (Doing things right) | "효율적으로 일하고 있는가?" (Doing efficiently) |
| **시간축** | 3~5년 (전략적) | 1~3년 (전술적) | 일/주/월 (운영적) |
| **핵심 프레임워크** | COBIT EDM Domain, ISO 38500 | COBIT APO/BAI, PMBOK 7th, PRINCE2 | ITIL 4 (34 Practices), DevOps, SRE |
| **산출물** | 거버넌스 헌장, 정책, KPI | 프로젝트 헌장, 예산, 아키텍처 청사진 | 인시던트/서비스 요청, 변경기록 |
| **측정** | 전략적 KPI (ROI, NPV, CSF 달성도) | 프로젝트 KPI (CPI, SPI) | 운영 KPI (MTTR, MTBF, 가용성) |

### 2. Build vs Buy vs Cloud (의사결정 프레임워크)

| 기준 | **Build (자체개발)** | **Buy (패키지)** | **Subscribe (Cloud/SaaS)** |
| :--- | :--- | :--- | :--- |
| 초기 투자비 | 높음 (수십억) | 중간 (수억) | 낮음 (월구독료) |
| 구현 기간 | 12~24개월 | 3~6개월 | 1~4주 |
| 커스터마이징 | ★★★★★ | ★★★ | ★ |
| 유지보수 책임 | 자체 | 벤더 | 벤더 |
| 데이터 통제 | ★★★★★ | ★★ | ★~★★ |
| 확장성 | 제한적 | 중간 | ★★★★★ |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 555 / 800

<- **이전**: [554. IT 경영 관리 핵심 토픽 554번 시험 요약](/studynote/12_it_management/05_security_compliance/554_it_management_core_topic_554_exam_summary/)
**다음**: [556. IT 경영 관리 핵심 토픽 556번 시험 요약](/studynote/12_it_management/05_security_compliance/556_it_management_core_topic_556_exam_summary/) ->

---
