---
title: "IT Management Core Topic 516 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 516번은 **COBIT 2019, ITIL 4, ISO 38500** 등 글로벌 IT 거버넌스·서비스관리 프레임워크를 기반으로, **EA(Enterprise Architecture), PPM(Project Portfolio Management), IT 투자 경제성 분석(TCO/ROI/NPV/IRR), 정보시스템 감리, SLA, BCM/DR**을 통합 운용하는 **IT-비즈니스 정렬(Strategic Alignment)** 의사결정 체계임.
> 2. **가치**: 정량적 효과로 **IT 투자 대비 ROI 15~25% 개선**, 프로젝트 실패율 **전통적 70% -> EA·PPM 적용 시 30% 이하로 감소**, SLA 기반 서비스 가용성 **99.9% -> 99.99% 향상**, 정성적 효과로 **이사회-경영진-IT 삼위일체 거버넌스 확보** 및 **규제 준수(컴플라이언스) 리스크 60% 축소**.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(1) 중앙집중형 거버넌스(CoE) vs 분산형 거버넌스(Federated), (2) Waterfall vs Agile(SAFe/Spotify) 방법론 혼용 비율, (3) CAPEX 일시집중 vs OPEX 클라우드 전환 시의 TCO 회수기간(통상 3~5년), (4) 내부 역량 내재화 vs 외부 SI/클라우드 아웃소싱** — 기술사적 판단은 **조직 성숙도(CMMI/KMDF)**, **업무의 핵심성(Mission-Criticality)**, **규제 환경(전자금융감독규정, 개인정보보호법)** 변수를 통합한 **위험조정 수익률(RAROC) 기반** 의사결정임.

---

## Ⅰ. 개요 및 필요성

정보화 시대를 거쳐 **디지털 전환(DX, Digital Transformation)·AI 전환(AX)** 시대로 진입하면서, IT는 단순 비용센터(Cost Center)에서 **전략적 가치 창출 센터(Value Center)**로 역할이 전환됨. 그러나 한국 정보화진흥원의 2023년 정보화 실태조사에서 보고된 바와 같이, 국내 대기업의 **IT 투자 대비 사업적 성과 연결률**은 여전히 30%대에 그치고 있음. 또한 프로젝트 실패율은 Standish Group CHAOS Report 기준 **전통적 방법론에서 31.1%(2015년) -> 2020년 Agile 확대에도 21.7%** 수준임.

이러한 실패의 근본 원인은 **(1) IT-비즈니스 전략 부조화, (2) 이해관계자 간 거버넌스 부재, (3) IT 성과 측정의 정량성 부족, (4) Risk·Compliance 관리체계 미흡**의 4대 역기능에 있음. 516번 토픽은 바로 이 4대 역기능을 **국제 표준 프레임워크(COBIT·ITIL·ISO 20000/38500·PMBOK·ISO 31000)**와 **경제성 분석 기법(NPV·IRR·CBA)**, **감리 표준(SSAE/SOC, ISACA 감리표준)**으로 해결하는 **End-to-End IT 경영관리 방법론**임.

```text
+------------------------------------------------------------------+
|            IT 경영관리 516번 - 4대 역기능 -> 4대 해결축           |
+------------------------------------------------------------------+
|                                                                  |
|  [역기능 1] IT-비즈니스 부조화  --->  [해결] EA + SAM(Strategic   |
|   "SI 실패, 요구사항 변경 폭주"    Alignment Maturity) 모델      |
|                                                                  |
|  [역기능 2] 거버넌스 부재      --->  [해결] COBIT 2019 + ISO 38500|
|   "이사회-CIO-IT 현업 단절"        (3-tier: Direct/Manage/Monitor)|
|                                                                  |
|  [역기능 3] 성과 측정 정량성    --->  [해결] BSC + KPI + IT Score |
|   "ROI 5% vs 25% 혼동"            Card + IT Balanced Scorecard   |
|                                                                  |
|  [역기능 4] 리스크·규제 미흡    --->  [해결] ISO 31000 + IS감리 +  |
|   "개인정보·보안사고·DR 실패"       ISMS-P + BCP/DRP(ISO 22301)   |
|                                                                  |
+------------------------------------------------------------------+
```

**기존 패러다임(2000년대) vs 새로운 패러다임(2020년대 DX 시대)** 비교:
- **기존**: SI 주도의 사용자 요구사항(UR) 중심, waterfall, RFP-입찰-검수 방식, 개별 시스템 단위 투자, **"시스템 구축이 곧 IT 가치"**라는 환원주의.
- **신규**: 비즈니스 Outcome 중심, **Product/Platform Squad(SAFe/Spotify 모델)**, **BizDevOps/Platform Engineering** 기반 지속적 인도(Continuous Delivery), 포트폴리오 단위 투자, **"데이터·경험·생태계가 IT 가치"**라는 플랫폼 경제 관점.

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차 운전**과 같음. 엔진(EA·아키텍처), 핸들(거버넌스·COBIT), 브레이크(리스크·IS감리), 연료(투자·TCO), 네비게이션(전략·BSC) — 이 5개가 동시에 맞물려야 목적지(비즈니스 가치)에 안전하게 도달할 수 있음. 하나라도 어긋나면 **"정비소에 돈만 쓰고 목적지에 못 가는 차"**가 됨.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 516번의 **3-Layer 통합 아키텍처**는 **① 전략·거버넌스 층, ② 실행·운영 층, ③ 통제·개선 층**으로 구성되며, 각 층이 **PDCA + Closed-Loop Feedback**으로 연결됨.

```text
+---------------------------------------------------------------------+
|  [Layer 1] 전략·거버넌스 층  (Strategy & Governance)                |
|  +------------+ +------------+ +-------------+ +---------------+  |
|  | 비즈니스   |->| IT 전략    |->| EA(전사    |->| IT 투자 의사  |  |
|  | 전략(BSP)  | | (ISP)      | | 아키텍처)  | | 결정(거버넌스)|  |
|  +------------+ +------------+ +-------------+ +---------------+  |
|         <->                <->                <->              <->          |
|   BSC/CSF            SAM 모델       TOGAF·FEAF       COBIT 2019    |
|                                                  (EDM 영역)         |
+---------------------------------------------------------------------+
|  [Layer 2] 실행·운영 층  (Execution & Operation)                    |
|  +------------+ +------------+ +-------------+ +---------------+  |
|  | 프로젝트   |->| Agile/Dev  |->| 서비스 운용 |->| 사용자/        |  |
|  | 포트폴리오 | | Ops        | | (ITIL 4)   | | 고객 가치 실현 |  |
|  +------------+ +------------+ +-------------+ +---------------+  |
|         <->                <->                <->              <->          |
|   PMBOK·SAFe       Sprint/Kanban    SLA·OLA·UC    CX/EX 메트릭     |
+---------------------------------------------------------------------+
|  [Layer 3] 통제·개선 층  (Control & Improvement)                    |
|  +------------+ +------------+ +-------------+ +---------------+  |
|  | 리스크관리 |->| 정보시스템 |->| 보안/개인   |->| 지속적 개선    |  |
|  | ISO 31000  | | 감리(SSAE) | | 정보(ISMS-P)| | (CSI·Kaizen)  |  |
|  +------------+ +------------+ +-------------+ +---------------+  |
|         <->                <->                <->              <->          |
|   RBS·Heat Map      SOC1/2 Type II   PIPC·KISA      ITIL CSI       |
|                                                                    |
+---------------------------------------------------------------------+
                ^                                                    |
                |   Closed-Loop Feedback (성과 -> 전략 재조정)         |
                +----------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EA(Enterprise Architecture)** | 비즈니스-데이터-애플리케이션-기술 4계층 정합성 확보 | **TOGAF ADM(Architecture Development Method)** 8단계(Phase A~H) 사이클, **ArchiMate 3.1** 표기법, **FEAF** 연동, **As-Is -> To-Be** 갭 분석, **전사 표준화율(표준 준수율)** KPI: 응용시스템 80%+, 데이터 표준 90%+ |
| **COBIT 2019** | IT 거버넌스 의사결정·통제 프레임워크 | **40개 Governance/Management Objective**, **EDM(Evaluate/Direct/Monitor) 5개 + APO/BAI/DSS/MEA 4개 도메인**, **7대 구성요소(Components of Governance System)**: 프로세스·구조·정보흐름·사람·역량·정책·문화, **핵심 능력 수준 0~5 (Process Capability, ISO/IEC 33020 PAM)** |
| **ITIL 4** | IT 서비스 관리 운영 체계 | **34개 Practice**(중심·일반·기술), **Service Value System(SVS)**: Opportunity/Demand -> Value -> Guiding Principles(7개: Focus on value, Start where you are 등) -> Governance -> Practices -> Continual Improvement, **4-Dimension Model**: 조직·인재·정보·기술·파트너·가치흐름 |
| **PPM(Project Portfolio Mgmt)** | 다수 프로젝트 우선순위·자원 배분 최적화 | **3단계 필터링**(전략적 적합성 -> 재정적 수익성 -> 실행 가능성), **NVP(Net Value Prioritization)**, **Balanced Scorecard 정렬도**, 자원 평준화(Resource Leveling), **Strategic Bucket(50%) + Tactical Bucket(30%) + Operational Bucket(20%)** 자원 배분 모델 |
| **SLA(Service Level Agreement)** | 서비스 품질 계약·측정·보상 체계 | **SLR(요구사항) -> SLA(내부/외부 계약) -> OLA(내부 지원) -> UC(Underpinning Contract)** 4단계 계층, **가용성 99.9% = 월 43분/연 8.77시간 다운 허용**, MTTR/MTBF/SLA 패널티 크레딧 산정, **XLA(Experience Level Agreement)** 신개념 |
| **IT 경제성 분석** | 투자 정당화·우선순위 의사결정 | **TCO(Total Cost of Ownership) 5년 산정**: HW·SW·인력·교육·운영·장애, **ROI(Return on Investment)=(편익-비용)/비용×100**, **NPV(순현재가치)=Σ(CF_t/(1+r)^t)-초기투자**, **IRR(내부수익률)=NPV=0 되는 r**, **B/C(비용편익비)>1**, **회수기간(Payback Period)** |
| **정보시스템 감리** | 사업 성과·결함·보안 독립 검증 | **3대 영역**: 사업관리·SW·HW, **감리 구분**: 1~3종(금액/기간별), **시점**: 사전·중간·사후, **결함 등급**: 중대(Major)·일반(Minor)·경미(Cosmetic), **감리원 자격**: 감리사(ICCA), **SSAE-18 SOC1/2/3 Type II** 보고서 |
| **BCM/DRP** | 업무 연속성·재해 복구 체계 | **ISO 22301 BCMS**(BIA->RTO/RPO 산정->전략->계획), **RTO(복구시간목표)** vs **RPO(데이터손실허용시간)**: Tier1(0/0)~Tier4(24h/24h), **DR 방식**: Cold/Warm/Hot Site, **다중리전(Active-Active) vs Pilot Light** |
| **ISMS-P / 정보보안 거버넌스** | 정보보호 관리체계 | **PIPC 8개 영역 102개 통제항목**, 인증 유효기간 3년, **연 1회 사후심사**, **ISO 27001:2022 Annex A 93개 통제**, NIST CSF 5대 기능(Identify/Protect/Detect/Respond/Recover) |

**핵심 알고리즘·산정식 심화**:

1. **SAM(Strategic Alignment Maturity) 모델 — Luftman 5단계(Lv1~Lv5)**:
   - 점수 = Σ(6개 속성: Communication, Competency, Governance, Partnership, Architecture, Skills)×(성숙도 가중치)
   - 국내 평균 Lv2.3(2008) -> Lv3.1(2022)으로 개선 추세

2. **IT-BSC 4관점**: 재무(FCF/ROI) / 고객(만족도·NPS) / 내부프로세스(배포빈도·MTTR) / 학습·성장(핵심인재 유지율·교육이수시간)
   - KPI 예시: 배포 리드타임, 변경 실패율, MTTR, MTTD, 가용성, NPS

3. **RACI 매트릭스**: Responsible(수행) / Accountable(책임, 단수) / Consulted(자문) / Informed(통보) — 프로젝트 거버넌스의 핵심 의사결정 권한 매트릭스

- **📢 섹션 요약 비유**: 위 3-Layer는 **비행기의 조종 시스템**과 같음. Layer 1은 **비행 계획·관제탑(Strategy)**, Layer 2는 **실제 조종·엔진(Execution)**, Layer 3는 **블랙박스·안전장치·정비(Control)**. 516번은 이 3개가 모두 작동해야 안전한 비행(=IT 가치 실현)이 가능하다는 것을 강조함.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·통제 | IT 서비스 관리·운영 | IT 의사결정 이사회 가이드 | 프로젝트 관리 지식체 |
| **관점** | What(무엇을)·Why(왜) | How(어떻게) | 원칙(Principle) 중심 | 원칙+12 Principle of PM |
| **적용 범위** | 전사 IT(End-to-End) | IT 서비스 운영·개선 | 이사회·경영진 거버넌스
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 516 / 800

<- **이전**: [515. IT 경영 관리 핵심 토픽 515번 시험 요약](/studynote/12_it_management/05_security_compliance/515_it_management_core_topic_515_exam_summary/)
**다음**: [517. IT 경영 관리 핵심 토픽 517번 시험 요약](/studynote/12_it_management/05_security_compliance/517_it_management_core_topic_517_exam_summary/) ->

---
