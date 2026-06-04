---
title: "671. IT 경영 관리 핵심 토픽 671번 시험 요약 (IT Management Core Topic 671 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019, ISO/IEC 38500)는 이사회-경영진-IT 간의 **책임·위임·평가(Evaluate-Direct-Monitor)** 3원칙을 통해 정보기술이 조직의 전략적 목표와 정렬(Strategic Alignment)되도록 하는 의사결정 및 통제 프레임워크이며, BSC·KPI·TCO·NPV·IRR 등 정량 지표로 IT 성과와 투자 효율을 측정·환류하는 것이 핵심 메커니즘이다.
> 2. **가치**: COBIT 2019 도입 기업 기준 IT 투자 ROI 평균 **25~40% 개선**, IT 부채(Technical Debt) **30% 감소**, 감사·컴플라이언스 대응 시간 **50% 단축**(ISACA 2022 Survey), 중대 장애(Major Incident) **MTTR 42% 단축** 효과를 통해 기업 가치를 직접적으로 제고한다.
> 3. **판단 포인트**: ① COBIT vs ITIL vs ISO 27001 등 **다중 프레임워크 매핑(Integration Map)** 설계, ② Agile·DevOps·클라우드 전환 시 **거버넌스 오버헤드 vs BizDevOps 속도** 트레이드오프, ③ 정량 KPI(가용성 99.95%, MTTR ≤ 30분, CSAT ≥ 4.2/5)와 **Soft Goal(문화·역량)**의 균형, ④ 한국 환경의 전자금융감독규정·개인정보보호법·클라우드 보안인증(CSAP) 등 **규제 매핑(Regulation Mapping)**이 합격/실격 분기점이다.

---

## Ⅰ. 개요 및 필요성

정보기술이 **Cost Center**(비용 센터)에서 **Value Creator**(가치 창출원)로 전환된 21세기 이후, IT 투자는 단순 인프라 확장이 아닌 **Digital Transformation, ESG, AI·Data Analytics, Cloud Native** 등 기업 핵심 경쟁력과 직결되는 전략 자산이 되었다. 그러나 한국 산업통상자원부·KISA 통계에 따르면, 국내 대기업의 IT 투자 실패율은 여전히 **40~60%**(Standish Group CHAOS Report 2020 기준)에 달하며, 실패의 핵심 원인은 ① 경영 전략과 IT 전략의 **Misalignment(불일치)**, ② 투자 대비 성과 측정 부재(**Black Hole Spending**), ③ 리스크·컴플라이언스 통제 실패, ④ 부서별 사일로(Silo) 시스템 때문이다.

이에 IT 거버넌스는 **"Who makes What Decision, When, and How"** 라는 의사결정 권한 매트릭스(RACI: Responsible, Accountable, Consulted, Informed)를 통해, IT-비즈니스 간 정렬(Alignment)을 구조적으로 보장하는 메커니즘으로 자리 잡았다. 2020년 이후 COVID-19 팬데믹과 가속화된 **Digital Pivot** 환경에서, 원격근무·제로트러스트 보안·클라우드 비용 폭증(FinOps)·AI 윤리 등 새로운 거버넌스 이슈가 등장하면서 **"Adaptive Governance"** 패러다임이 요구되고 있다.

```text
+--------------------------------------------------------------------------+
|                 IT 거버넌스 의사결정 및 통제 구조 (PDCA + EDM)            |
+--------------------------------------------------------------------------+
|                                                                          |
|   +--------------+         +--------------+         +--------------+    |
|   |  이사회(BoD)  | -------> |  IT 전략위   | -------> |  CIO / CDO   |    |
|   |  Board       |  의결   |  Steering    |  의결   |  IT Exec.    |    |
|   +------+-------+         +------+-------+         +------+-------+    |
|          |                        |                        |            |
|          v                        v                        v            |
|   +------------------------------------------------------------------+  |
|   |           EDM Cycle : Evaluate -> Direct -> Monitor                |  |
|   |   (ISO/IEC 38500)         COBIT 2019 Governance System           |  |
|   +------------------------------------------------------------------+  |
|   | ① Evaluate : 현상태 진단(As-Is), GAP 분석, Capability Level 측정 |  |
|   | ② Direct   : To-Be 목표설정, 우선순위 결정, 자원배분(Portfolio)  |  |
|   | ③ Monitor  : KPI/CSF 측정, KPI 대시보드, Audit & Compliance    |  |
|   +------------------------------------------------------------------+  |
|                                    |                                     |
|                                    v                                     |
|   +------------------------------------------------------------------+  |
|   |                    Balanced Scorecard (BSC)                      |  |
|   |  +----------+----------+----------+----------+                   |  |
|   |  | Financial| Customer | Internal |Learning  |                   |  |
|   |  | ROI/IRR  | CSAT     | MTTR/MTBF|Skill Up  |                   |  |
|   |  | ≥ 15%    | ≥ 4.2/5  | ≤ 30min  | ≥ 40h/y  |                   |  |
|   |  +----------+----------+----------+----------+                   |  |
|   +------------------------------------------------------------------+  |
|                                    |                                     |
|                                    v                                     |
|   +------------------------------------------------------------------+  |
|   |  Framework Integration Map : COBIT × ITIL × ISO 27001 × TOGAF   |  |
|   +------------------------------------------------------------------+  |
+--------------------------------------------------------------------------+
```

기존 패러다임(**Pre-2000**: CIO가 인프라만 관리, ROI 측정 불가, Shadow IT 만연)과 신규 패러다임(**Post-2020**: **Product-centric IT**, **BizDevOps 통합**, **Value Stream 기반 측정**)의 핵심 차이는, IT가 **"지원 부서(Support Function)"**에서 **"비즈니스 공동설계자(Co-Creator)"**로 격상되었다 점이다. Gartner 2023 보고서에 따르면, **Product Management 체계**를 도입한 기업의 IT-비즈니스 정렬도는 평균 **68% -> 89%**로 상승했다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **비행기의 계기판(나침반·고도계·연료계)**과 같습니다. 조종사(CIO)가 아무리 훌륭해도, 이사회·탑승객(Stakeholder)이 **현재 위치·방향·연료**를 실시간으로 확인하지 못하면 목적지(전략 목표)에 도달할 수 없습니다. COBIT·BSC·KPI가 바로 그 **계기판**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 아키텍처는 크게 **3-Layer**로 구성된다: ① **Governance Layer**(의사결정·통제: COBIT 2019 40개 Governance & Management Objectives), ② **Management Layer**(실행·운영: ITIL 4 34 Practices, PMBOK 7th, Agile/Scrum), ③ **Operation Layer**(기술 인프라: Cloud, Container, Observability, Zero Trust). 이 3계층은 **Closed-Loop Feedback**으로 연결되어, 상위 KPI가 하위 Practice로 분해되고, 하위 측정값이 상위 의사결정으로 환류된다.

COBIT 2019의 핵심은 **Cascade of Goals**(목표 캐스케이드) 메커니즘이다. 기업 목표(13개 Enterprise Goals) -> 정렬·연락·지원 관계(Alignment/Connection/Support) -> IT 관련 목표(13개 Alignment Goals) -> Enabler(사람·프로세스·기술·정보 등 7가지) -> Process Capability 측정(0~5 Level) 순으로 **Top-Down** 해체된다. 각 단계는 **RACI Matrix**로 책임 소재가 명확히 정의된다.

```text
+----------------------------------------------------------------------+
|         COBIT 2019 Cascade of Goals & Capability Assessment          |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------+      |
|  |  Layer 1: Enterprise Goals (13개)                          |      |
|  |   EG01 포트폴리오의 적시·예산·의사결정 충족                 |      |
|  |   EG03 약속된 서비스 제공(BSL 확보)                         |      |
|  |   EG05 IT 비용·이익의 비즈니스 가치 실현                    |      |
|  |   EG13 지식·전문성 확보·인재양성                            |      |
|  +-------------------------+----------------------------------+      |
|                            | Alignment(정렬)                          |
|  +-------------------------v----------------------------------+      |
|  |  Layer 2: Alignment Goals (13개)                            |      |
|  |   AG01 IT 거버넌스 프레임워크 준수                          |      |
|  |   AG04 지식·경험·정보의 관리                                |      |
|  |   AG09 Agile·DevOps 등 유연한 IT 운영                       |      |
|  |   AG12 IT 변경·이행 위험관리                                |      |
|  +-------------------------+----------------------------------+      |
|                            | Support(지원)                            |
|  +-------------------------v----------------------------------+      |
|  |  Layer 3: Enablers (7대) - People/Process/Technology/Info |      |
|  |           /Structure/Culture/Goals                          |      |
|  +-------------------------+----------------------------------+      |
|                            | Realization                              |
|  +-------------------------v----------------------------------+      |
|  |  Layer 4: Process Capability (PAM 기반 40 Processes)       |      |
|  |   EDM01~05 거버넏목표 / APO/BAI/DSS/MEA 35개 관리목표      |      |
|  |   Maturity Level: 0(Incomplete)~5(Optimizing)              |      |
|  |   ISO/IEC 33000 PAM(Process Assessment Model) 기반         |      |
|  +------------------------------------------------------------+      |
|                                                                      |
|  ※ 투자평가 :  NPV = Σ CFₜ/(1+r)ᵗ - I₀  ,  IRR = r  s.t. NPV=0    |
|  ※ 정보가치 :  VoI = Benefit - Cost = (Loss Avoided + Productivity) |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회 / IT 전략위 (Steering Committee)** | 거버넌스 최고 의사결정 기구 (RACI: A) | 분기 1회 의결(Portfolio 승인), **EDM01 Ensured Governance Framework Setting** 수행, BSC Top-Level KPI 리뷰, Risk Appetite 결정 |
| **CIO / CDO / CISO** | IT 전략·데이터·보안 총괄 (R: 실행, A: 성과) | **EDM02 Benefits Delivery** 촉진, **AG09(Agile) × AG12(Risk)** 균형, OKR(Objective & Key Results) 기반 실행 |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리·표준화 | **PMBOK 7th 12 Principles** + PRINCE2 + Agile Hybrid 적용, EVM(Earned Value Management: CPI ≥ 0.95, SPI ≥ 0.95) 관리 |
| **CoBIT/ITIL 통합 거버넌스 플랫폼** | 거버넌스·운영 통합 관리 | **ServiceNow GRC**, **Archer**, **SAP GRC** 등으로 Control Objective -> Process -> ITSM Incident/Change 자동 매핑 |
| **BSC/KPI 대시보드** | 성과 측정·가시화 | **Power BI / Tableau / Grafana**, BSC 4관점(Financial·Customer·Internal·Learning) + 5번째 관점(Sustainability/ESG) 추가 |

투자평가 핵심 공식으로는 ① **NPV(순현재가치) = Σ CFₜ/(1+r)ᵗ - I₀**, ② **IRR(내부수익률) = NPV=0이 되는 할인율 r**, ③ **TCO(총소유비용) = Direct(인프라·라이선스) + Indirect(교육·다운타임)**, ④ **Payback Period(투자회수기간) = I₀/연간CF**, ⑤ **VoI(Value of Information) = 손실회피액 + 생산성향상 + 전략적옵션가치**가 있다. 기술사 시험에서는 **공식 유도 + 한계점(Discount Rate 결정의 주관성, Risk Premium 반영)**까지 설명해야 고득점이다.

정보화 사업의 **타당성 분석**은 ① **경제성 분석(B/C Analysis, NPV)**, ② **정책·기술·운영 분석**, ③ **전략적 분석(Strategic Fit)** 3축으로 구성되며, 디지털 전환 사업은 **정성적 효과(Strategic Agility, Time-to-Market 단축)** 비중이 70% 이상이라는 점에서 **Real Options Valuation(실물옵션)** 기법이 필수로 등장한다.

- **📢 섹션 요약 비유**: COBIT 2019의 Cascade of Goals는 마치 **피라미드식 군사 지휘통제체계(C2)**와 같습니다. 대장(이사회)의 전략적 목표가
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 671 / 800

<- **이전**: [670. IT 경영 관리 핵심 토픽 670번 시험 요약](/studynote/12_it_management/05_security_compliance/670_it_management_core_topic_670_exam_summary/)
**다음**: [672. IT 경영 관리 핵심 토픽 672번 시험 요약](/studynote/12_it_management/05_security_compliance/672_it_management_core_topic_672_exam_summary/) ->

---
