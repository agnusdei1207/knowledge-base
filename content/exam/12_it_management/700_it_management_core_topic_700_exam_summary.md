---
title: "IT Management Core Topic 700 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019(거버넌스), ITIL 4(서비스), PMBOK 7th(프로젝트), ISO 38500(의사결정), EA(아키텍처) 등 글로벌 프레임워크를 4계층(거버넌스-전략-서비스-운영)으로 통합하여 Business-IT Alignment를 실현하는 경영체계이며, 정보화사업법·클라우드컴퓨팅법 등 국내 법·제도 환경과 직결되는 통합관리체계임.
> 2. **가치**: McKinsey 연구에 따르면 EA 기반 IT-Portfolio 최적화 시 IT 비용 20~30% 절감, BSC-KPI 연계 시 프로젝트 성공률 70%->90%(Standish Group CHAOS Report 기준), ITIL 도입 시 MTTR 50%·FCR 25% 개선, ISMS 인증 취득 시 보안사고 60% 감소 등 정량적 가치 창출.
> 3. **판단 포인트**: 조직의 IT 성숙도(단계 1~5)에 따른 점진적 프레임워크 도입(Quick-Win vs Big-Bang), 거버넌스-관리-운영(GMO: Governance·Management·Operational) 3단계 분리, 프로젝트 수행 모델(Waterfall↔Agile↔DevOps) 선택, 그리고 정량 KPI(ROI·NPV·TCO·ROA·EVA) 기반 성과측정 체계 설계가 핵심 의사결정 포인트.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 지원(Support) 역할에서 벗어나 **전략적 동인(Strategic Enabler)** 으로 전환됨에 따라, IT 경영관리는 기업의 핵심 경쟁력과 직결된 통합관리체계를 요구받고 있다. 특히 4차 산업혁명, 디지털전환(DX: Digital Transformation), 생성형 AI, 클라우드 네이티브 환경으로의 패러다임 전환은 전통적 IT 관리 프레임워크의 한계를 노출시켰으며, 2024년 기준 한국 정보화사업 통계에 따르면 연간 약 30조 원 규모의 정보화 사업 중 약 35%가 일정·예산·품질 목표를 초과(Overrun)하고 있어, 통합적 IT 거버넌스의 필요성이 더욱 부각되고 있다.

```text
+----------------------------------------------------------------------+
|           IT 경영관리 4계층 통합 프레임워크 (GMO 3-Layer)             |
+----------------------------------------------------------------------+
|                                                                      |
|  [Layer 1] 의사결정 거버넌스 (Governance Layer)                      |
|  +----------------------------------------------------------+        |
|  |  이사회 -> IT전략위원회 -> CIO -> IT거버넌스위원회          |        |
|  |  · COBIT 2019 EDM(평가·지시·모니터링) 5개 도메인         |        |
|  |  · ISO/IEC 38500:2024 IT 거버넌스 원칙(책임·전략·획득·  |        |
|  |    성능·준수·인간행위) 6원칙 적용                         |        |
|  +----------------------------------------------------------+        |
|                          |                                           |
|                          v                                           |
|  [Layer 2] 전략·기획 (Management Layer)                             |
|  +----------------------------------------------------------+        |
|  |  · EA(엔터프라이즈 아키텍처): TOGAF 10 ADM, FEAF, DoDAF   |        |
|  |  · 전략수립: Porter 5-Forces, SWOT, VRIO, Blue Ocean     |        |
|  |  · 성과측정: BSC 4관점(재무·고객·내부·학습성장) + KPI    |        |
|  |  · 투자우선순위: PBM(Portfolio-Based Management), WSJF   |        |
|  +----------------------------------------------------------+        |
|                          |                                           |
|                          v                                           |
|  [Layer 3] 서비스·프로젝트 운영 (Operational Layer)                 |
|  +----------------------------------------------------------+        |
|  |  · ITIL 4 SVS(서비스밸류시스템): 34개 Practice, 4P+1D    |        |
|  |  · PMBOK 7th: 12원리, 8성능도메인, 49프로세스 연계      |        |
|  |  · Agile/Scrum/Kanban/DevOps/SRE/FinOps                  |        |
|  |  · 정보보호: ISMS-P, ISO 27001, ISO 27701                |        |
|  +----------------------------------------------------------+        |
|                          |                                           |
|                          v                                           |
|  [Layer 4] 평가·개선 (Evaluation & Improvement)                     |
|  +----------------------------------------------------------+        |
|  |  · 감리(정보시스템감리), 성과측정, KPI 대시보드          |        |
|  |  · CMMI 2.0 성숙도(1~5단계), COBIT SSC(Starter->Optimized)|        |
|  |  · BSC-RBR(Rule-Based Review), ITIL CSI(지속적개선)       |        |
|  +----------------------------------------------------------+        |
|                                                                      |
+----------------------------------------------------------------------+
```

**기존 패러다임 대비 새로운 패러다임**:
- ❌ 기존: "IT는 비용(Cost Center)", 부서별 독립 운영, 사후(Silo) 관리
- ✅ 신규: "IT는 가치(Value Driver)", 통합 거버넌스, 사전(By-Design)·실시간·예측형 관리
- ❌ 기존: 프로젝트 단위 성과(Scope·Time·Cost의 Iron Triangle)만 추구
- ✅ 신규: 비즈니스 가치·고객 경험·TCO·Agility 4축 균형 추구(VUCA·BANI 시대 대응)

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **도시의 도시계획(Urban Planning)** 과 같습니다. 개별 건물(시스템) 하나하나의 건축허가(프로젝트)만 보는 것이 아니라, 상위 도시에 해당하는 종합계획(EA), 도시기본계획(전략), 도시관리계획(거버넌스), 그리고 교통·상하수도 등 공통 인프라 운영(서비스관리)을 통합적으로 설계·감독하는 도시 행정 체계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리는 5대 영역(거버넌스·전략·서비스·프로젝트·정보보호)과 4대 산출물(정책·표준·절차·지표)로 구성되며, 각 영역은 **PDCA + DMAIC** 의 사이클을 기반으로 상호 연계된다.

```text
+-----------------------------------------------------------------------+
|         IT 경영관리 핵심 프로세스 (5대 영역 × 4대 산출물 매트릭스)     |
+-----------------------------------------------------------------------+
|                                                                       |
|  +------------+   +------------+   +------------+   +------------+   |
|  | ① 거버넌스 |--->| ② 전략/EA  |--->|③ 서비스/PM |--->|④ 정보보호  |   |
|  +------------+   +------------+   +------------+   +------------+   |
|        |                |                |                |          |
|        v                v                v                v          |
|  +--------------------------------------------------------------+     |
|  |  [산출물 4대 유형]                                              |     |
|  |  · Policy(정책)  -> 임원 승인, 조직 전체 강제력                |     |
|  |  · Standard(표준) -> 기술·방법론 강제 규격 (예: 코딩표준)      |     |
|  |  · Procedure(절차) -> 업무 흐름 SOP, RACI 매트릭스            |     |
|  |  · Metric(지표)   -> KPI/SLA/OLA, 측정 가능한 정량 지표       |     |
|  +--------------------------------------------------------------+     |
|                                                                       |
|  [핵심 관리 메커니즘]                                                  |
|                                                                       |
|  Plan(계획)  ->  Do(실행)  ->  Check(평가)  ->  Act(개선)              |
|      |              |              |              |                  |
|      v              v              v              v                  |
|  TOGAF ADM    Scrum Sprint    COBIT KPI      ITIL CSI                 |
|  PMBOK Init   Waterfall Exe   BSC Scorecard  Retrospective            |
|  ITIL SVS     DevOps CI/CD    감리(Audit)    CMMI Appraisal           |
|                                                                       |
|  [법·제도 연결]                                                       |
|  · 정보화사업법(2023.12. 전면개정, 2024.6.시행)                       |
|  · 클라우드컴퓨팅법(2024.1.시행), 데이터산업법                        |
|  · 개인정보보호법(PIPA), 정보통신망법, AI기본법(2025.1.시행)         |
|  · 전자정부법, 공공데이터법                                            |
+-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 (COBIT 2019)** | 의사결정·감독·평가·지시(EDM) 및 40개 관리목표(Governance/Management Objective) | EDM 5개(EDM01~05: 프레임워크,BenefitDelivery,RiskOpt,ResourceOpt,Transparency) + APO 14개 + BAI 11개 + DSS 6개 + MEA 4개 = 40개 프로세스. 7가지 컴포넌트(원리·정책·프레임워크·문화·인적자원·서비스·정보) 매트릭스로 설계. |
| **EA (TOGAF 10 / FEAF)** | 비즈니스-데이터-애플리케이션-기술 4계층 정렬, 중복 제거·표준화·로드맵 | TOGAF ADM(Architecture Development Method) Phase A(비전)->B(비즈니스)->C(정보시스템)->D(기술)->E(기회·솔루션)->F(마이그레이션)->G(구현거버넌스)->H(아키텍처변경) + Requirements Management. ADM Cycle Iteration. |
| **IT 서비스 (ITIL 4)** | 서비스 가치 사슬(SVC) 기반 IT 서비스 기획·전환·운영·개선 | 34개 Practice(General·Service·Technical Management). 4P+1D(Product·People·Partners·Processes + Demand). Service Value Chain: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve 6개 액티비티. |
| **프로젝트 (PMBOK 7th + Agile)** | 프로젝트 기획·실행·통제·종료, 12원리·8성능도메인 기반 | PMBOK 7th: 8 Performance Domain(Stakeholder·Team·Development Planning·Delivery·Measurement·Uncertainty·Complexity·Risk). 49 Process × 5 Process Group + 12 Principles. 병행하여 Agile(스크럼: Product/Develop/Scrum Master, 5이벤트, 3아티팩트) 활용. |
| **정보보호 (ISMS-P / ISO 27001)** | CIA(기밀성·무결성·가용성) 확보, 위험평가·통제선택·사후관리 | ISMS-P: 12개 영역, 80+ 통제항목(관리·보호·예방·탐지·대응). ISO 27001 Annex A 93개 통제. PIMS(ISO 27701) 31개 PII 통제. NIST CSF 5함수(Gov·ID·PR·DE·RS·RC). |

**핵심 원리 정량 공식**:
- **TCO (Total Cost of Ownership)** = 직접비(HW·SW·인건비) + 간접비(교육·다운타임·복구·전환비). 일반적으로 1차 도입비의 4~5배가 5년 TCO.
- **ROI** = (效益 - 投資額) / 投資額 × 100. IT 프로젝트 평균 ROI 15~25%, 디지털전환 사업 30%+.
- **NPV** = Σ(현금흐름ₜ / (1+r)ᵗ). 할인율(r) 8~12% 적용, 양(+)의 NPV일 때 투자 적격.
- **EV(기금액)** = BAC × SPI(일정성과) × CPI(비용성과). EAC(추정완료비) = BAC / CPI.
- **CMMI 2.0 성숙도**: 1(Initial)->2(Managed)->3(Defined)->4(Quantitatively Managed)->5(Optimizing). 레벨 3 도달 시 프로젝트 성공률 약 60%->85% 상승.
- **CSF/CFT(Critical Success/Tactor)**: 경영진 지원(CSF₁), 사용자 참여(CSF₂), 명확한 요구사항(CSF₃), 숙련된 PM(CSF₄), 견고한 계획(CSF₅) — 위 5요소 결여 시 프로젝트 실패 확률 3배.

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차의 통합제어 시스템(ECU·CAN Bus 통합)** 과 같습니다. 개별 시스템(엔진·브레이크·에어컨)이 각자 동작하면 차량이 폭주하듯, IT 시스템·프로세스·프로젝트도 거버넌스(ECU 메인) -> 전략(전체 도로 지도) -> 서비스(변속기·엔진오일) -> 정보보호(에어백·ABS) -> 평가(계기판·OBD2 진단) 체계로 통합 제어되어야 안정적 주행이 가능합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | COBIT 2019 | ITIL 4 | PMBOK 7th | ISO 38500 |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 목표 통제 | IT 서비스 라이프사이클 운영 | 단일 프로젝트 성공적 수행 | IT 의사결정의 6원칙 준수 |
| **관점** | 경영진·감
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 700 / 800

<- **이전**: [699. IT 경영 관리 핵심 토픽 699번 시험 요약](/studynote/12_it_management/05_security_compliance/699_it_management_core_topic_699_exam_summary/)
**다음**: [701. IT 경영 관리 핵심 토픽 701번 시험 요약](/studynote/12_it_management/05_security_compliance/701_it_management_core_topic_701_exam_summary/) ->

---
