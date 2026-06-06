---
title: "IT Management Core Topic 628 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 628번은 **COBIT 2019, ITIL 4, ISO 38500, PMBOK 7th, BOK 5th** 등 글로벌 IT 거버넌스·서비스·프로젝트 관리 프레임워크의 통합적 이해와, **EA(Enterprise Architecture) 기반 정보화 사업 기획·투자·성과평가 라이프사이클**을 한 축으로 다루는 메타 영역임.
> 2. **가치**: 기업의 IT-Business Alignment를 정량화하여 **TCO 15~30% 절감, ROI 20~40% 향상, 프로젝트 성공률 28% -> 71%(Standish Group CHAOS Report 기준)** 수준으로 끌어올리며, ISMS·개인정보보호법·전자금융감독규정 등 컴플라이언스 자동화로 법적 리스크를 차단함.
> 3. **판단 포인트**: **Build vs Buy, 워터폴 vs 애자일, On-Premise vs 하이브리드 클라우드, 중앙집중형 vs 페더레이션 거버넌스**라는 4대 트레이드오프에서 조직 성숙도(CMMI 2~5 레벨, ITIL Maturity Model)와 산업 규제(금융/공공/의료)를 기준으로 의사결정해야 함.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입 단계를 넘어, **IT를 경영 자산으로 정량 관리**해야 하는 시대가 도래하면서 IT 경영관리는 CIO·CDO·CISO·사업PMO의 의사결정 체계 그 자체로 진화했습니다. 4차 산업혁명(AI, IoT, Blockchain, Cloud) 이후 IT 투자 규모는 연평균 12~18% 증가하는 반면, **실패 프로젝트 비율은 여전히 30~40%**에 달하여, "투자 대비 가치 실현(Value Realization)"이 핵심 경영 이슈로 부상했습니다.

```text
+-------------------------------------------------------------------------+
|              IT 경영관리 628번 토픽 - 메타 거버넌스 맵                       |
+-------------------------------------------------------------------------+
|                                                                         |
|   +--------------+    +--------------+    +--------------+              |
|   |  IT 전략기획  |---->|  정보화사업   |---->|   IT 운영·   |              |
|   |  (ISP/BPR)   |    |   관리       |    |   서비스     |              |
|   +------+-------+    +------+-------+    +------+-------+              |
|          |                   |                   |                      |
|          v                   v                   v                      |
|   +--------------+    +--------------+    +--------------+              |
|   |  TO-BE 모델링 |    | PMBOK/PRINCE2|    | ITIL 4 SVS   |              |
|   |  (EA/FEA/DODAF)|   | 위험/품질/원가|    | COBIT 2019   |              |
|   +------+-------+    +------+-------+    +------+-------+              |
|          |                   |                   |                      |
|          +-------------------+-------------------+                      |
|                              v                                          |
|                  +--------------------------+                           |
|                  |   ISO 38500 IT거버넌스   |                           |
|                  |   (Evaluate·Direct·Monitor)                          |
|                  +--------------------------+                           |
|                              |                                          |
|                              v                                          |
|   +----------------------------------------------------------+          |
|   |  성과평가: BSC 4관점 + KPI + NPV/IRR + EVA + TCO/ROI    |          |
|   +----------------------------------------------------------+          |
|                                                                         |
+-------------------------------------------------------------------------+
```

기존 패러다임은 **"IT = 비용(Cost Center)"** 으로 인식되어 후행적 통제(End-of-pipe Audit) 위주였으나, 신패러다임은 **"IT = 전략 자산(Value Driver)"** 으로 전환하여 선제적 거버넌스, 실시간 KPI 모니터링, 그리고 Zero-Trust·DevSecOps 기반의 신뢰 체계가 요구됩니다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **오케스트라의 지휘자**와 같습니다. 바이올린(IT 운영), 첼로(프로젝트), 트럼펫(보안), 팀파니(컴플라이언스) 등 각 악기가 제 역할은 하지만, **지휘자(거버넌스 프레임워크)**가 없으면 합주가 아니라 난장판이 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 628번의 4대 핵심 축은 **①IT 거버넌스 ②IT 서비스/프로젝트 관리 ③EA·정보화사업 ④성과평가 및 리스크**입니다.

```text
+-------------------------------------------------------------------------+
|          IT 경영관리 4축 통합 아키텍처 (CobiT-ITIL-PMBOK-EA 매핑)            |
+-------------------------------------------------------------------------+
|                                                                         |
|  +---------------- IT 거버넌스 (COBIT 2019 / ISO 38500) -------------+ |
|  |  [Evaluate] -> [Direct] -> [Monitor]                                | |
|  |      |            |           |                                   | |
|  |      v            v           v                                   | |
|  |  40 Governance  5 Focus    Cascade to                            | |
|  |  Objectives    Areas      Mgmt Objectives                        | |
|  +--------------------------------------------------------------------+ |
|                              |                                          |
|  +---------------- IT 서비스 관리 (ITIL 4 SVS) ---------------------+ |
|  |  Service Value System: Opportunity->Demand->Value                    | |
|  |  Practices: 34 (Incident, Problem, Change, SLM, SRM)              | |
|  |  Guiding Principles: 7 (Focus on value, Start where you are...)  | |
|  +--------------------------------------------------------------------+ |
|                              |                                          |
|  +---------------- 프로젝트 관리 (PMBOK 7th / PRINCE2) ---------------+ |
|  |  8 Performance Domains + 12 Principles                             | |
|  |  Process Groups: Initiating->Planning->Executing->M&C->Closing        | |
|  +--------------------------------------------------------------------+ |
|                              |                                          |
|  +---------------- EA & 정보화사업 관리 (TOGAF/FEA) -----------------+ |
|  |  ADM Cycle: P->C->B->T->R->G (8 phases)                               | |
|  |  한국형: 정보화전략계획(ISP) -> 정보화사업 예산편성 -> 사업관리       | |
|  +--------------------------------------------------------------------+ |
|                              |                                          |
|                              v                                          |
|            +-------------------------------------+                    |
|            |  통합 리포팅 대시보드 (BI/EPM)        |                    |
|            |  - BSC Scorecard (재무/고객/내부/학습) |                    |
|            |  - KPI/NorthStar Metric              |                    |
|            |  - NPV, IRR, Payback, TCO, ROI       |                    |
|            +-------------------------------------+                    |
|                                                                         |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 체계 (COBIT 2019)** | IT 의사결정의 권한·책임·통제 구조 정의 | 40개 거버넌스 목표(EDM: Evaluate/Direct/Monitor) + 5개 도메인(EDM/APO/BAI/DSS/MEA) + 능력수준 0~5. **Focus Area**로 커스터마이징 (예: DevOps, Risk, Privacy) |
| **IT 서비스 관리 (ITIL 4)** | IT 서비스의 End-to-End 가치 흐름 관리 | Service Value System(SVS): 7 Guiding Principles + 34 Practices + 4D 모델(Design/Transition/Operate/Improve). **Incident MTTR 평균 1.6시간, FCR 75% 이상 목표** |
| **프로젝트 관리 (PMBOK 7th)** | 일정·품질·원가·범위·리스크·조달·이해관계자·팀 8개 영역 통합 | 12 Principles of Project Management + Adaptive(Agile/Hybrid)/Predictive 이원화. **SPI/CPI 지수 0.9~1.1이 정상 범위** |
| **EA & 정보화사업 (TOGAF ADM)** | 비즈니스-IT 정렬을 위한 청사진(Blueprint) | ADM 8 Phase: Preliminary->A(비전)->B(비즈니스)->C(데이터/앱/기술)->D(기회)->E(마이그레이션)->F(구현거버넌스)->G(변화관리). **한국 정보화진흥법 ISP 수립 의무화** |
| **성과평가 시스템 (BSC/KPI)** | IT 투자 효과의 정량적 측정·환류 | Kaplan-Norton BSC 4관점 × 4~6개 KPI. **ROI 15% 이상, Payback 3년 이내, NPV 양수, EVA >0** 의 4대 재무 기준 적용 |

**핵심 원리 심화**:
- **COBIT 2019의 Cascade Model**: Stakeholder Needs -> 13개 Enterprise Goals -> 40개 Alignment Goals -> Component Objectives로 흘러내려가는 Top-Down 방식
- **ITIL 4의 Value Co-Creation**: 공급자-소비자 공동가치창출 모델, **"Value = Utility + Warranty"** 공식
- **NPV(순현재가치)**: `NPV = Σ[CFt / (1+r)^t] - C0`, 할인율 r은 WACC(가중평균자본비용) 적용, **NPV > 0일 때 투자 타당**
- **EVA(Economic Value Added)**: `EVA = NOPAT - (WACC × 투자자본)`, **연속 3년 EVA > 0이면 가치창출형 IT**로 분류

- **📢 섹션 요약 비유**: COBIT은 **헌법**(거버넌스 원칙), ITIL은 **민법**(서비스 운영 규정), PMBOK은 **형법**(프로젝트 절차), EA는 **국토계획도**(아키텍처 청사진) — 4가지가 합쳐져야 국가(기업)가 운영됩니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 628번 토픽은 글로벌 프레임워크 간의 **상호 보완 관계**를 정확히 이해하는 것이 핵심입니다.

| 구분 | COBIT 2019 | ITIL 4 | PMBOK 7th | ISO 38500 |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·통제 | IT 서비스 운영·가치 | 프로젝트 단위 작업 관리 | 이사회 수준 IT 책임·원칙 |
| **적용 범위** | Enterprise 전체 IT | IT 서비스 라이프사이클 | 개별 프로젝트 | 조직 거버넌스 최상위 |
| **핵심 산출물** | 목표 계단(Goal Cascade), 능력 Maturity | SVS, 34 Practices | 8 Performance Domain + 12 Principle | 6개 원칙(Evaluate/Direct/Monitor) |
| **구조** | 40 Governance & Mgmt Objectives | 4D(Service Value Chain) | 8 Domains / 12 Principles | 3개 모델(Director/Manager/Board) |
| **측정 기준** | 능력수준 0~5, Focus Area KPI | SLA, CSAT, MTTR/MTBF | SPI/CPI, EV(earned value) | 원칙 준수 여부, 책임성 |
| **상호 연계** | APO->BAI->DSS->MEA가 ITIL/PMBOK을 wrapping | DSS 06~08 영역이 ITIL과 직접 매핑 | BAI 01~11이 프로젝트 거버넌스 제공 | COBIT 2019이 ISO 38500에 정렬됨 |

**연결 통합 사례**:
- **서비스 데스크 장애 대응**(ITIL Incident Mgmt) -> **변경사항 승인**(COBIT BAI03 Manage Change) -> **프로젝트 신규 구축**(PMBOK Initiating) -> **EA 변경 영향 분석**(TOGAF ADM Phase F) -> **이사회 보고**(ISO 38500 Monitor)
- 이 5단계 흐름이 **1개의 인시던트에서 신규 시스템 출시까지** 거버넌스 체인을 완성합니다.

- **📢 섹션 요약 비유**: COBIT은 **건축물의 구조계산서**, ITIL은 **엘리베이터 운영매뉴얼**, PMBOK은 **시공공정표**, ISO 38500은 **건축주 책임 가이드**입니다. 건물이 무너지지 않으려면 네 가지가 동시에 맞아야 합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **프레임워크 선택**: 조직 성숙도(CMMI 레벨, ITIL Maturity) 측정 후 **단일 표준 채택 vs 2~3개 통합(예: COBIT+ITIL+PMBOK)** 결정 — 신생기업은 ITIL+Agile, 대기업/공공기관은 COBIT+ISO 38500+EA 조합 권장
2. **투자 의사결정 모델**: 정량 분석(ROI 15%+ / NPV 양수 / Payback 3년 이내 / IRR > WACC) + 정성 분석(전략적 정합성, 경쟁력, 리스크) **동시 수행**, 단일 지표 의존 금지
3. **정보화사업 단계별 관리**: ISP 수립 -> 사업 타당성 조사(Feasibility Study: 경제성/기술성/법률성/운영성) -> 예산 편성(중기재정계획) -> 사업 감리(PMO) -> 성과평가(사후평가 3단계: 형성/중간/최종)
4. **위험 관리(Risk Register)**: 정성적 매트릭스(영향 1~5 × 발생확률 1~5) + 정량적 VaR/CVaR, **Top10 위험은 월 1회 이사회 보고**, KR(중요위험지수) 산정 후 BCM/DR 계획 연결
5. **컴플라이언스 매핑**: **전자금융거래법, 개인정보보호법(PIPA), ISMS-P, ESG 공시, EU AI Act** 등 규제별 통제항목을 COBIT 2019 또는 NIST CSF 800개 통제항목에 자동 매핑하여 GRC(Governance-Risk-Compliance) 플랫폼 운영

### 피해야 할 안티패턴

- **"프레임워크 무지성 도입"**: ITIL 34개 Practices 모두 구현 시도 -> 3~5개 핵심(Practice)부터 점진 확대
- **"KPI 숫자 놀음"**: 측정 가능한 KPI 5개 vs 보고용 30개 혼용 -> **North Star Metric 1개 + 4~6개 Supporting KPI** 원칙 준수
- **"Shadow IT 방치"**: 현업의 클라우드·SaaS 무단 도입 -> **CTO 승인제 + FinOps** 병행으로 가시성 확보(보통 Shadow IT가 IT 예산의 30~40% 차지)
- **"Big Bang 리스크 무시 전환"**: 5개년 레거시 한 번에 클라우드 전환 시도 -> **Strangler Fig Pattern**(점진적 이관) 적용, 6개월 단위 마이그레이션
- **"감리·평가 형식화"**: 전자정부법상 정보화사업 감리를 단순 점검표로 처리 -> **데이터 기반 위험예측(예측감리·AI감리)**으로 전환 필요

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **자동차 운전**과 같습니다. COBIT은 **도로교통법**, ITIL은 **정비 메뉴얼**, PMBOK은 **내비게이션**, EA는 **지도로 본
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 628 / 800

<- **이전**: [627. IT 경영 관리 핵심 토픽 627번 시험 요약](/studynote/12_it_management/05_security_compliance/627_it_management_core_topic_627_exam_summary/)
**다음**: [629. IT 경영 관리 핵심 토픽 629번 시험 요약](/studynote/12_it_management/05_security_compliance/629_it_management_core_topic_629_exam_summary/) ->

---
