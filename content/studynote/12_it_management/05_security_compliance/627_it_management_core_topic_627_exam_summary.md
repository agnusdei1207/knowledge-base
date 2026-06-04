+++
title = "627. IT 경영 관리 핵심 토픽 627번 시험 요약 (IT Management Core Topic 627 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019 거버넌스-관리 체계**, **ITIL 4 서비스 가치 시스템(SVS)**, **ISO/IEC 38500 이사회 거버넌스 원칙**을 통합하여 **전략(Strategy) ↔ 포트폴리오(Portfolio) ↔ 프로그램(Program) ↔ 프로젝트(Project)** 4계층 정렬(Alignment)을 달성하는 경영 프레임워크임.
> 2. **가치**: McKinsey 글로벌 조사에서 **디지털 전환 성공 기업은 EBITDA 마진 26%p 우위**, PMI 연구에서 **거버넌스 성숙도 상위 25% 조직의 프로젝트 성공률 77% vs 하위 25% 31%** — 정량적 ROI와 의사결정 속도 향상이 입증됨.
> 3. **판단 포인트**: **Build vs Buy vs Cloud vs SaaS** 의사결정 시 TCO 5년 분석, **Shadow IT 통제 vs 직원 자율성** 균형, **Agile-Waterfall 하이브리드(SAFe, Spotify 모델)** 도입 시 문화 변화 비용, 그리고 **규제 준수(Regulatory Compliance)**와 **혁신 속도** 간 트레이드오프가 핵심 결정 변수임.

---

## Ⅰ. 개요 및 필요성

전통적 IT 운영은 **"비용 센터(Cost Center)"** 관점에서 시스템 가용성·장애 대응 위주의 후행적(Reactive) 관리가 중심이었음. 그러나 4차 산업혁명, 팬데믹 이후의 비대면 경제, 생성형 AI(LLM, GPT-4/Claude/Gemini)의 등장으로 IT는 **"비즈니스 가치 동인(Value Driver)"** 및 **"전략적 핵심 자산"**으로 재정의됨.

이에 따라 CISO, CDO, CIO 3자 역할이 분리되고, **이사회-경영진-IT 삼자 거버넌스(Three-Lines Model, IIA 2020)** 체계가 요구됨. 한국 환경에서는 **전자금융거래법, 개인정보보호법(PIPA), ISMS-P, 클라우드 보안인증(CSAP)** 등 중첩 규제 하에서 IT 투자 의사결정의 정당성(Justification)과 위험 통제(Risk Control)가 동시에 요구됨.

```text
[ IT 경영관리 4계층 정렬 아키텍처 (Strategy-Portfolio-Program-Project) ]

  +--------------------------------------------------------------+
  | Level 1: STRATEGY (전략)                                     |
  |  +--------------+  +--------------+  +--------------+        |
  |  | 비전/미션     |  | KPI/BSC      |  | IT 거버넌스   |        |
  |  | Vision/Mssn  |  | Balanced     |  | 정책/원칙     |        |
  |  |              |  | Scorecard    |  | (COBIT 2019) |        |
  |  +------+-------+  +------+-------+  +------+-------+        |
  |         +------------------+------------------+               |
  |                            v                                  |
  | Level 2: PORTFOLIO (포트폴리오) — "Doing the right things"     |
  |  +--------------------------------------------------+         |
  |  | ① 투자우선순위  ② 위험-수익 분석  ③ 자원배분      |         |
  |  |  NPV, IRR, Payback Period, ROA, EVA              |         |
  |  |  Portfolio Rationalization (Trough, Plateau)     |         |
  |  +--------------------+-----------------------------+         |
  |                       v                                      |
  | Level 3: PROGRAM (프로그램) — "Coordinated change"            |
  |  +--------------------------------------------------+         |
  |  | 다수 프로젝트의 통합관리, Benefits Realization,  |         |
  |  | Stakeholder Engagement, Capacity Planning         |         |
  |  +--------------------+-----------------------------+         |
  |                       v                                      |
  | Level 4: PROJECT (프로젝트) — "Doing things right"            |
  |  +--------------------------------------------------+         |
  |  | Scope/Schedule/Cost/Quality/Resource/Comm/Risk    |         |
  |  | PMBOK 7th (8绩效域), PRINCE2, Scrum/SAFe         |         |
  |  +--------------------------------------------------+         |
  +--------------------------------------------------------------+
```

**전통 vs 현대 패러다임 비교**
- *전통(1980~2010)*: Silo별 독립 예산, CapEx 중심, 연 1회 예산 사이클, IT-사업 부서간 사일로
- *현대(2010~현재)*: 통합 EA(Enterprise Architecture) 기반, OpEx+CapEx 혼합, **연중 자금조달(Funding-on-Demand)**, **BizDevOps** 문화, FinOps(클라우드 비용 최적화) 등장

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차 회사의 CEO**와 같음. 전체 기업(회사) 방향을 결정하고, 어떤 차종(포트폴리오)을 만들지, 어떤 공장(프로그램)을 가동할지, 각 조립라인(프로젝트)을 관리해야 함. 4계층이 흔들리면 한 대의 불량차가 전체 브랜드를 무너뜨림.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **"정렬(Alignment) - 전달(Delivery) - 지원(Support) - 측정(Measurement)"** 의 4대 메커니즘을 통합 운영하는 것임. 이를 위해 **COBIT 2019의 거버넌스/관리 목표(GO/MG)** 체계가 표준 참조 모델로 활용됨.

```text
[ COBIT 2019 거버넌스 시스템 + ITIL 4 SVS 통합 아키텍처 ]

  +-------------------------------------------------------------+
  |  이사회(Board) - 소유(Ownership)                             |
  |     |  평가(Evaluate) -> 지도(Direct) -> 모니터(Monitor)       |
  |     v                                                       |
  |  +---------------------------------------------------+      |
  |  |      거버넌스 시스템 (Governance System)           |      |
  |  |  +------------+  +------------+  +------------+   |      |
  |  |  | 원칙·정책  |  | 프로세스   |  | 조직구조   |   |      |
  |  |  | Principles |  | Processes  |  | Structures |   |      |
  |  |  | Flow->Goal  |  | EDM, APO,  |  | Roles·Resp |   |      |
  |  |  +------------+  | BAI, DSS,  |  +------------+   |      |
  |  |                  | MEA(5영역)  |                    |      |
  |  |                  +-----+------+                    |      |
  |  +------------------------+--------------------------+      |
  |                           v                                 |
  |  +---------------------------------------------------+      |
  |  |      ITIL 4 Service Value System (SVS)            |      |
  |  |  Opportunity/Demand -> Value -> Service Value Chain |      |
  |  |  (Plan->Engage->Design->Obtain->Build->Transition->    |      |
  |  |   Operate->Support->Improve)                        |      |
  |  |  + 7 Guiding Principles (Focus on value, etc.)   |      |
  |  +--------------------+------------------------------+      |
  |                       v                                     |
  |  +---------------------------------------------------+      |
  |  |      성과 측정 (Performance Measurement)          |      |
  |  |  KPI/CSFs -> Balanced Scorecard(4관점)             |      |
  |  |  재무/고객/내부프로세스/학습성장                  |      |
  |  +---------------------------------------------------+      |
  +-------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 (거버넌스 프레임워크)** | IT 의사결정·통제 체계 표준화 | 5개 도메인(EDM/APO/BAI/DSS/MEA), 40개 관리목표, **Cascade of Goals(13단계)** 로 비전->이해관계자 목표->정렬->전략->포트폴리오->서비스->인프라->기술 추적 |
| **ITIL 4 SVS (서비스 가치)** | 운영·서비스 전달 최적화 | 4차원 모델(조직/정보/파트너/공급/가치스트림/기술), **34개 Practice**(사고/문제/변경/릴리스/서비스데스크 등), 7대 guiding principles |
| **ISO/IEC 38500 (이사회 거버넌스)** | 이사회 IT 감독 책임 | 6원칙(책임/전략/수행/규율/행동/능력), **Evaluate-Direct-Monitor(EDM)** 3단계 사이클 |
| **PMBOK 7th + SAFe/SPOTIFY** | 프로젝트/프로그램 실행 | PMBOK 7th는 12원칙 + 8성능영역(계획/팀/개발/측정 등), **SAFe 6.0**은 4구성(Team/ART/Solution/Large Solution) + PI Planning |

**핵심 정량 지표 및 산식**
- **TCO(Total Cost of Ownership)** = CapEx(구매·구축) + OpEx(운영·인건비) + Hidden Cost(학습·전환·Downtime)
- **ROI** = (총이익 − 총비용) / 총비용 × 100
- **NPV** = Σ [CF_t / (1+r)^t] − 초기투자 (할인율 r 적용 현금흐름)
- **BCR(Benefit-Cost Ratio)** > 1.0 시 사업성 확보
- **EVA(Economic Value Added)** = NOPAT − (투자자본 × WACC)
- **서비스 수준**: SLA(예: 가용성 99.95% = 연간 Downtime 263분), MTTR(평균복구시간), MTBF(평균고장간격), SLO/SLI/SRE 지표

- **📢 섹션 요약 비유**: COBIT 2019는 **헌법**, ITIL 4는 **행정 절차법**, PMBOK은 **각 부처 실무 매뉴얼**, ISO 38500은 **대통령의 헌법 준수 보고서** — 서로 충돌 없이 역할 분담하는 **다층적 법체계**가 IT 경영관리임.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 27001** | **PMBOK 7th** |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스 & 관리 | IT 서비스 관리 | 정보보안 경영 | 프로젝트 관리 |
| **대상 범위** | 전사 IT 의사결정 | 서비스 운영·전달 | 정보보호 통제 | 단일 프로젝트 |
| **주 사용자** | 이사회·CIO·CISO | 서비스매니저·운영팀 | CISO·감사인 | PM·PMO |
| **핵심 산출물** | Goals Cascade, Maturity | Service Value Chain | ISMS 인증, SOA | Charter,绩效域 |
| **성숙도 모델** | CMMI 0~5단계 Maturity | 4단계 Maturity Model | Annex A 통제 93개 | Performance Domain |
| **통합 방식** | ITIL·ISO27001·TOGAF 매핑 | COBIT의 APO/DSS/MEA 참조 | 통제 요구사항을 ITIL/COBIT에 맵핑 | Program/Portfolio와 연결 |

**다른 시스템/도구와의 통합**
- **EA(Enterprise Architecture)**: TOGAF 10 ADM(Architecture Development Method) — **Preliminary->A(비전)->B/C/D(비즈니스/데이터/응용/기술)->E(기회)->F(마이그레이션)->G(구현거버넌스)->H(아키텍처변경)->요구사항관리** 와 COBIT의 APO/BAI 매핑
- **Agile/DevOps**: SAFe, LeSS, Spotify 모델 — Agile Release Train(ART) 단위로 COBIT BAI03(솔루션 아키텍처)·BAI06(변경관리) 준수
- **GRC(Governance-Risk-Compliance)**: SAP GRC, ServiceNow GRC, Archer — 통합 리스크 대시보드
- **클라우드/FinOps**: AWS Well-Architected Framework 6 Pillars, Azure CAF, GCP CAF + FinOps Foundation Framework

- **📢 섹션 요약 비유**: COBIT·ITIL·ISO27001·PMBOK의 관계는 **병원**의 역할 분담과 같음 — COBIT은 **병원장**(전략), ITIL은 **진료 프로세스**(운영), ISO27001은 **감염관리**(보안), PMBOK은 **각 과별 진료 매뉴얼**(프로젝트)임.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **전략 정렬 검증**: 신규 IT 투자 요청 시 **Strategy Map & BSC 4관점(Financial/Customer/Internal/Learning)** 에서의 명시적 연계 KPI가 정의되어 있는가? "BizDevOps" 문화에서 요구사항의 비즈니스 가치 추적이 가능한가?
2. **포트폴리오 최적화**: Gartner의 **Pace-Layered Application Strategy** 관점에서 시스템별 변화 속도(시스템 오브 레코드=안정, 시스템 오브 디퍼렌시에이션=핵심, 시스템 오브 이노베이션=실험)를 분류했는가? **Application Portfolio Management(APM)** 의 Trough/Plateau/Tipping Point 단계별 처방이 수립되어 있는가?
3. **리스크와 컴플라이언스**: 1라인(운영)·2라인(리스크/컴플라이언스)·3라인(내부감사)의 **IIA 3 Lines Model** 이 작동하는가? **개인정보 영향평가(PIA)**, **DPIA(데이터보호영향평가)**, **ISMS-P 인증** 갱신 주기를 KPI에 반영했는가?
4. **공급가치사슬 & 운영**: **ITIL 4 Service Value Chain** 9단계(Plan/Engage/Design&Transition/Obtain/Build/Transition/Operate/Support/Improve) 가 통합되어 있는가? **Change Enablement, Incident Management, Problem Management** 의 자동화 수준(예: AIOps, ServiceNow ITSM, Jira Service Management)이 충분한가?
5. **성과측정과 지속적 개선**: **OKR(목표·핵심결과)** 또는 **KGI/KPI 분리**가 적용되어 있는가? **PDCA + DMAIC + OKR** 의 3중 피드백 루프가 작동하는가? 재무 KPI(ROI/NPV) + 비재무 KPI(NPS/순천이직률/시스템가용성) 균형은?

### 피해야 할 안티패턴

- **"Shadow IT 만성 방치"**: 현업이 자체 도입한 클라우드/
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 627 / 800

<- **이전**: [626. IT 경영 관리 핵심 토픽 626번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/626_it_management_core_topic_626_exam_summary/)
**다음**: [628. IT 경영 관리 핵심 토픽 628번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/628_it_management_core_topic_628_exam_summary/) ->

---
