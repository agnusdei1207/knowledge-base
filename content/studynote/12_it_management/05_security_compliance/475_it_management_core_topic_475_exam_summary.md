+++
title = "475. IT 경영 관리 핵심 토픽 475번 시험 요약 (IT Management Core Topic 475 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스/관리 목표 40개), ITIL 4(34개 권고 실무), ISO/IEC 38500(6원칙 모델), TOGAF ADM(8단계)** 4대 글로벌 프레임워크의 시너지로 IT-Business Alignment를 정량화하고, **RACI 매트릭스, BSC 4관점(재무/고객/내부/학습성장), CSF/KPI/GPI 3계층 성과측정체계**를 통해 IT 자산을 전략적 가치로 전환하는 경영 과학이다.
> 2. **가치**: McKinsey 2024 조사 기준 효과적 IT 거버넌스 도입 시 **IT 투자수익률(ROIT) 23~38% 개선**, **Time-to-Market 45% 단축**, **IT 사고 MTTR 평균 67%v**, **Shadow IT 비용 30%v**, **디지털 전환 성공률 35%->78%** 도달이 가능하며, ISMS-P 인증기업은 사이버 사고 발생률 비인증 대비 약 1/4 수준으로 검증된다.
> 3. **판단 포인트**: 기술사 관점의 핵심 의사결정 3축은 ① **Govern(거버넌스) - Manage(관리) - Operate(운영) 3계층 분리**(책임/의사결정 권한 경계), ② **Build(자체) - Buy(도입) - Borrow(클라우드) - Bridge(하이브리드) 4B 투자 포트폴리오**, ③ **CSF->KPI->GPI(CSF 핵심성공요인, KPI 핵심성과지표, GPI 목표성과지표) 인과 사슬 정합성 검증**이며, EA(Enterprise Architecture) 4A(BA/DA/AA/TA)와 BSC 4관점 매핑이 답안의 깊이를 결정한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)이 4차 산업혁명의 핵심 동력으로 부상하면서, IT 부서는 **비용 센터(Cost Center)에서 가치 창출 센터(Value Center)**로 그 위상이 근본적으로 재정의되어야 하는 전환점에 도달했다. 과거 2000년대 SAP R/3, Oracle EBS 같은 **ERP 모놀리식 통합** 패러다임이 2020년대를 지나며 **클라우드 네이티브, SaaS, MSA(Microservice Architecture), 데이터 메시(Data Mesh)**로 분산·탈중앙화되면서, 이를 통제할 단일 거버넌스 체계 없이는 **Shadow IT, 데이터 사일로, 중복 투자, 보안 공백, 컴플라이언스 위반**이 조직 전체로 확산되는 구조적 위험이 발생한다.

특히 Gartner 2024 보고서에 따르면 글로벌 대기업의 평균 **IT 예산 중 27%가 중복 또는 비효율 투자**이며, CIO의 **57%가 "IT 복잡성이 디지털 혁신의 최대 장벽"**이라고 응답했다. 이런 환경에서 **COBIT 2019(Control Objectives for Information and Related Technologies)**, **ITIL 4(Information Technology Infrastructure Library)**, **ISO/IEC 38500 IT Governance**, **TOGAF 10(The Open Group Architecture Framework)** 등 4대 글로벌 프레임워크를 통합 운용하는 IT 경영 관리 역량은 기술사 시험의 단골 영역이자, 실무 컨설턴트의 핵심 무기가 된다.

```text
+---------------------------------------------------------------------+
|         IT 경영 관리 4계층 의사결정 프레임워크 (Governance Stack)      |
+---------------------------------------------------------------------+
|                                                                     |
|  +----------------------------------------------------------+     |
|  | L4. 전략·이사회 (Board / CEO)                              |     |
|  |   - ISO/IEC 38500 6원칙 (책임·전략·취득·성과·준수·인간)  |     |
|  |   - BSC 4관점 KPI 승인, IT 투자 한도 설정                 |     |
|  |   - 디지털 전환 로드맵, Risk Appetite 결정               |     |
|  +--------------------+-------------------------------------+     |
|                       | 위임·감독 (Steering Committee)              |
|  +--------------------v-------------------------------------+     |
|  | L3. 거버넌스 (CIO / IT steering Committee)                 |     |
|  |   - COBIT 2019 EDM(평가·지시·모니터) 5개 도메인          |     |
|  |   - EA(Enterprise Architecture) 4A 거버넌스              |     |
|  |   - IT 포트폴리오 관리, Vendor Governance                |     |
|  +--------------------+-------------------------------------+     |
|                       | 실행 지시 (Service Portfolio)                |
|  +--------------------v-------------------------------------+     |
|  | L2. 관리·기획 (IT Planning Office / PMO)                   |     |
|  |   - COBIT 2019 APO/BAI/DSS/MEA 35개 관리 목표            |     |
|  |   - ITIL 4 SVS(서비스 가치 시스템) 34개 실무              |     |
|  |   - PMBOK 7 / PRINCE2 프로젝트 통제                     |     |
|  +--------------------+-------------------------------------+     |
|                       | 서비스 전달 (SLA / OLA / UC)                 |
|  +--------------------v-------------------------------------+     |
|  | L1. 운영·전달 (Service Desk / DevOps / SRE)               |     |
|  |   - ITIL 4 운영관리(사건·문제·변경·릴리즈)               |     |
|  |   - SLA 99.9~99.99%, MTTR/MTBF, FCR(First Call Rate)    |     |
|  |   - IaC, AIOps, Observability, FinOps                    |     |
|  +----------------------------------------------------------+     |
|                                                                     |
|  [피드백 루프] CSF -> KPI -> GPI 측정 -> BSC 리포트 -> 의사결정        |
+---------------------------------------------------------------------+
```

한국 IT 환경의 특수성을 보면, **전자정부법, 개인정보보호법(PIPA), 정보통신망법, ISMS-P(정보보호 및 개인정보보호 관리체계), 클라우드 보안 인증(CSAP), 데이터 산업법** 등 규제 프레임워크가 글로벌보다 1~2년 빠르게 강화되는 추세이며, 2024년 기준 공공부문 **클라우드 이용률 60.7%(과기정통부 목표 75%)**, 민간 **대기업 SaaS 도입률 78%**에 도달했다. 따라서 **Public Cloud + On-Premise 하이브리드**, **국내·외 이중 클라우드(다중 가용성)**, **MSA 기반 Legacy 현대화** 등 한국형 IT 경영 모델 설계 능력이 요구된다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **도시의 도시계획(Urban Planning)**과 같다. 건물(시스템) 하나하나의 아름다움보다, 도로·상하수도·전기·통신 인프라의 통합 설계와 zoning(용도지역), 도시기본계획(EA), 도시관리계획(SLA)가 30년 후 시민의 삶의 질을 결정한다. 무분별한 개발(Shadow IT)은 교통 혼잡과 환경 오염(보안 사고·중복 투자)을 가져온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 아키텍처는 **4대 글로벌 프레임워크의 매핑과 통합(COBIT↔ITIL↔ISO38500↔TOGAF)**이 핵심이며, 각 계층은 명확한 RACI(Responsible·Accountable·Consulted·Informed) 매트릭스로 책임이 분리된다.

```text
+----------------------------------------------------------------------+
|       COBIT 2019 ↔ ITIL 4 ↔ ISO 38500 ↔ TOGAF 통합 매핑도          |
+----------------------------------------------------------------------+
|                                                                      |
|  +----------- 거버넌스 영역 (Govern) --------------+                  |
|  |  ISO 38500 6원칙                              |                  |
|  |   1. Responsibility  2. Strategy              |                  |
|  |   3. Acquisition     4. Performance           |                  |
|  |   5. Conformance      6. Human Behavior       |                  |
|  |            v 매핑                              |                  |
|  |  COBIT 2019 EDM 5개 (Evaluate/Direct/Monitor) |                  |
|  |   EDM01 프레임워크 / EDM02 거버넌스 체계       |                  |
|  |   EDM03 위험 최적화 / EDM04 자원 최적화        |                  |
|  |   EDM05 투명성 보장                             |                  |
|  +--------------+-------------------------------+                  |
|                 v                                                      |
|  +----------- 관리 영역 (Manage) ------------------+                  |
|  |  COBIT 2019 4도메인 35관리목표                  |                  |
|  |   APO(Align Plan Organize) 14개                 |                  |
|  |   BAI(Build Acquire Implement) 11개             |                  |
|  |   DSS(Deliver Service Support) 6개              |                  |
|  |   MEA(Monitor Evaluate Assess) 4개              |                  |
|  |            v 매핑                              |                  |
|  |  ITIL 4 SVS 7가지 지침                         |                  |
|  |   Focus on value / Start where you are         |                  |
|  |   Progress iteratively / Collaborate           |                  |
|  |   Think holistically / Keep it simple          |                  |
|  |   Optimize and automate                         |                  |
|  +--------------+-------------------------------+                  |
|                 v                                                      |
|  +----------- 실행·전달 영역 (Operate) -----------+                  |
|  |  ITIL 4 34개 실무(CDSP 기반)                    |                  |
|  |   - Service Value Chain 6활동                   |                  |
|  |     Plan->Engage->Design&Transition->              |                  |
|  |     Obtain/Build->Deliver&Support->Improve        |                  |
|  |   - 26 Practice (사건·문제·변경·릴리즈·        |                  |
|  |     서비스 데스크·모니터링·SRE 등)              |                  |
|  |            v 매핑                              |                  |
|  |  TOGAF 10 ADM 8단계 (Phase A~H)                 |                  |
|  |   A: Architecture Vision                        |                  |
|  |   B: Business Architecture (BA)                  |                  |
|  |   C: Information Systems (DA)                   |                  |
|  |   D: Technology Architecture (TA)               |                  |
|  |   E: Opportunities & Solutions                  |                  |
|  |   F: Migration Planning                         |                  |
|  |   G: Implementation Governance                  |                  |
|  |   H: Architecture Change Management             |                  |
|  +----------------------------------------------+                  |
|                                                                      |
|  ※ CSF(핵심성공요인) -> KPI(핵성과지표) -> GPI(목표성과지표)            |
|      CSF: "온라인 매출 확대" (전략)                                  |
|      KPI: "웹 가용성 99.95%, 결제 응답 < 2초" (측정)                |
|      GPI: "월 매출 120% 성장, 이탈률 5%v" (목표)                    |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance Board(이사회/ITSC)** | 최종 의사결정·감독 | ISO 38500 6원칙 적용, Risk Appetite·Tone at the Top 설정, 분기 1회 IT 성과 리뷰(BSC), 외부감사(내부회계관리제도 ITGC) |
| **COBIT 2019 EDM/APO/BAI/DSS/MEA** | 거버넌스-관리 목표체계 | EDM 5 + APO 14 + BAI 11 + DSS 6 + MEA 4 = **40개 관리목표**, 7가지 컴포넌트(원리·정책·프로세스·조직·정보·인력·기술) 매핑, **Design Factors 11종**(전략·목표·위험·문제·복잡성 등)으로 조직별 맞춤 설계 |
| **ITIL 4 Service Value System(SVS)** | 서비스 가치 창출 체계 | **Opportunity/Demand/Value(가치)**, **Guiding Principles 7종**, **Service Value Chain 6활동**, **34 Practices**(사고·문제·변경·릴리즈·서비스데스크·SRE·모니터링·FinOps·정보보안·지속성·공급자·SW개발 등) |
| **TOGAF 10 ADM** | EA 수립·관리 방법론 | **Preliminary Phase + 8 ADM Phase(A~H)**, **4A 영역(BA/DA/AA/TA)**, **ArchiMate 3.2 모델링 언어**, Architecture Repository(용어사전·표준·원칙·참조모델), **Gap Analysis·Transition Architecture** |
| **BSC(Balanced Scorecard)** | 전략 실행·성과 측정 | **4관점**: ①재무(ROI·비용절감), ②고객(CSAT·NPS), ③내부프로세스(MTTR·SLA), ④학습성장(역량·만족도), **Strategy Map(인과사슬) -> Theme별 Objective -> Measure -> Target -> Initiative** |
| **CSF/KPI/GPI 인과사슬** | 전략-전술-실무 연결 | **CSF(Critical Success Factor)**: "무엇이 성공에 필요한가", **KPI(Key Performance Indicator)**: "어떻게 측정하는가", **GPI(Goal Performance Indicator)**: "어디까지 달성하는가", **SMART 원칙**(Specific·Measurable·Achievable·Relevant·Time-bound) |
| **RACI 매트릭스** | 책임·역할 분장 | R(Responsible 실행) / A(Accountable 책임) / C(Consulted
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 475 / 800

<- **이전**: [474. IT 경영 관리 핵심 토픽 474번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/474_it_management_core_topic_474_exam_summary/)
**다음**: [476. IT 경영 관리 핵심 토픽 476번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/476_it_management_core_topic_476_exam_summary/) ->

---
