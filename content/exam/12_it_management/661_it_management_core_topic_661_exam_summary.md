---
title: "IT Management Core Topic 661 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT·ITIL·TOGAF·ISO 27001·PMBOK 등 글로벌 표준 프레임워크를 기반으로, IT를 비용센터가 아닌 **전략적 비즈니스 자산(Value Driver)**으로 전환·관리하기 위한 의사결정·통제·측정 체계를 포괄하는 통합 거버넌스 discipline임.
> 2. **가치**: 성숙도 1단계(Level 1:Initial) 조직 대비 5단계(Optimizing) 조직은 IT 프로젝트 성공률 35%->75%, 운영 인시던트 60% 감소, ROI 3배 향상(Gartner/ISACA 통계)의 정량적 가치와, IT-Biz 정렬·리스크 가시성·감사 대응력의 정성적 가치를 동시에 창출함.
> 3. **판단 포인트**: (a) 표준 프레임워크의 **Adopt-Adapt-Innovate** 도입 전략 결정, (b) **Centralized·Federated·Hybrid** 거버넌스 모델 중 조직 문화·규제 환경에 맞는 선택, (c) 정량 KPI(NRR, TCO, ROI) vs 정성 KPI(만족도, 역량) 간 **Balanced Scorecard** 균형 설계가 핵심 Trade-off.

---

## Ⅰ. 개요 및 필요성

정보기술의 역할이 1970년대 EDP(Electronic Data Processing) 시대의 비용 처리에서, 2000년대 ERP/SOA를 거치며 전략 자산으로 격상되었고, 2020년대 들어서는 **Cloud-Native·AI·Data Platform** 기반으로 **Digital Business Platform**의 핵심으로 자리매김함. 그러나 McKinsey(2023) 조사에 따르면 글로벌 IT 이니셔티브티브 중 **70%가 비즈니스 가치 미달**, CIO 우선순위 조사(Deloitte 2024)에서 **"IT 비용 대비 가치 증명"**이 5년 연속 1순위로 나타나, IT 경영관리 체계 부재가 그대로 **수조 원 단위의 투자 낭비**로 직결되고 있음.

특히 국내 환경에서는 2023년 **전자금융거래법 개정**, 2024년 **클라우드컴퓨팅법(클라우드컴퓨팅 이용자의 보호 및 데이터 이중화)** 시행, 2025년 예정 **AI 기본법**으로 인해 IT 거버넌스가 단순 권고가 아닌 **법적 의무사항**으로 전환되고 있어, IT 경영관리 역량이 곧 **기업 생존 역량**이 되었음.

```text
+---------------------------------------------------------------------+
|        디지털 전환 시대의 IT 경영관리 패러다임 변화                  |
+---------------------------------------------------------------------+
|                                                                     |
|  [Past: 1990s]              [Present: 2020s]       [Future: 2030s]  |
|  +----------+              +----------+            +----------+    |
|  | Cost     |   ------►    | Strategic|  ------►   | Autonomous|    |
|  | Center   |   Value     | Asset    |  AI-driven | Business  |    |
|  |          |   Shift     |          |  Decision  | Platform  |    |
|  +----------+              +----------+            +----------+    |
|       |                         |                       |         |
|   EDP/Mainframe            Cloud/SaaS            AI Agent/         |
|   IS Audit (수동)          DevOps/Agile          Self-Healing      |
|   CFO 관할                 CDO+CIO 협업          AI Governance      |
|                                                                     |
|  +----------------------------------------------------------+       |
|  | 핵심 변화 5축:                                             |       |
|  | ①IT-Biz 정렬(Alignment)  ②Agile 거버넌스(Adaptive)        |       |
|  | ③Data-Driven 의사결정     ④리스크-컴플라이언스 자동화       |       |
|  | ⑤ESG/지속가능성 통합 거버넌스                                |       |
|  +----------------------------------------------------------+       |
+---------------------------------------------------------------------+
```

기존 **"프로젝트 완료 = 거버넌스 종료"** 방식에서, **"프로젝트 완료 -> 운영·서비스·최적화 -> 폐기"** 전 생애주기(Lifecycle)에 걸친 **Value Governance**로 전환이 필요함. 또한 **CoBIT 2019**는 기존 5개 도메인(EDM·APO·BAI·DSS·MEA)에서 **Focus Area(F.A.)** 개념을 도입하여, **DevOps, Cybersecurity, Privacy, Digital Transformation** 등 신기술 거버넌스를 모듈식으로 추가 가능한 구조로 진화함.

- **📢 섹션 요약 비유**: IT 경영관리는 자동차의 **'통합 계기판(Integrated Cockpit)'**과 같음. 속도계(ROI), 연료계(TCO), 엔진온도계(리스크), 네비게이션(전략) 등 30여 가지 계기판을 실시간으로 통합 모니터링하여, **운전자(이사회·CIO)**가 한눈에 사업 상태를 파악하고 코스를 수정할 수 있게 해주는 시스템임.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리는 **단일 시스템이 아닌 7개 레이어의 통합 거버넌스 스택**으로 구성되며, 각 레이어는 **국제 표준 + 국내 제도 + 조직 운영 모델**의 3중 정렬을 통해 작동함.

```text
+----------------------------------------------------------------------+
|          IT 경영관리 7-Layer Reference Architecture                  |
+----------------------------------------------------------------------+
|                                                                      |
|  Layer 7: 의사결정·통제(Decision & Control)                           |
|           +------------------------------------+                     |
|           | Steering Committee / IT Committee  |                     |
|           | Portfolio Mgmt Office(PMO)         |                     |
|           | Architecture Review Board(ARB)     |                     |
|           +------------------------------------+                     |
|                              v                                       |
|  Layer 6: 측정·평가(Measure & Evaluate)                               |
|           +------------------------------------+                     |
|           | KPI/BSC · IT Scorecard · SLA       |                     |
|           | Maturity Assessment(CMMI/COBIT)    |                     |
|           | IS Audit(내부·외부·감사원)           |                     |
|           +------------------------------------+                     |
|                              v                                       |
|  Layer 5: 프레임워크·표준(Framework)                                  |
|           +------------------------------------+                     |
|           | COBIT 2019 · ITIL 4 · TOGAF 10    |                     |
|           | ISO 38500 · ISO 27001/27002        |                     |
|           | PMBOK 7 · CMMI 2.0 · ISO 20000    |                     |
|           +------------------------------------+                     |
|                              v                                       |
|  Layer 4: 프로세스(Process) - 5개 도메인(COBIT)                       |
|           EDM->APO->BAI->DSS->MEA (37개 프로세스)                          |
|                              v                                       |
|  Layer 3: 컴포넌트(서비스·프로젝트·EA)                                |
|           ITSM · PPM · EAM · DevOps · SecOps · FinOps                |
|                              v                                       |
|  Layer 2: 데이터·인프라(Data & Infra)                                 |
|           CMDB · ITAM · GRC Platform · Data Lake · Observability     |
|                              v                                       |
|  Layer 1: 인력·조직(People)                                           |
|           CIO·CDO·CISO·PMO·BA·SA·SRE·Dev·Ops 조직                    |
|                                                                      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 전략적 의사결정 | 이사회·IT 위원회에서 **IT 투자 포트폴리오·리스크 허용 한도·아키텍처 원칙** 승인. COBIT 2019의 5개 EDM 프로세스(EDM01~05)로 구성, RACI 매트릭스 기반 의사결정 권한 분배 |
| **APO (Align, Plan, Organize)** | 전략 정렬·계획 | **전략-전술-운영** 3계층 연결. APO01(관리 프레임워크)->APO05(포트폴리오)->APO12(리스크)->APO13(보안) 등 14개 프로세스로 **BPMN 2.0** 기반 프로세스 모델링 |
| **BAI (Build, Acquire, Implement)** | 솔루션 구축·도입 | **BAI03(솔루션 아키텍처)->BAI06(변경 관리)->BAI11(프로젝트 관리)**의 11개 프로세스. Waterfall/Agile/Hybrid 방법론 통합, **GitOps·ArgoCD** 등 자동화 도구 연동 |
| **DSS (Deliver, Service, Support)** | 서비스 운영·지원 | **ITIL 4 Service Value System(SVS)**과 직접 매핑. DSS02(서비스 요청)->DSS04(인시던트)->DSS05(문제) 등 6개 프로세스, **ServiceNow·Jira Service Management**로 워크플로우 자동화 |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정·감사 | **MEA01(성과 모니터)->MEA02(내부 통제)->MEA03(컴플라이언스)->MEA04(감사)**의 4개 프로세스. ISMS-P·PIPC·ISMS 인증, **내부감사·외부감사·외부평가** 3단계 통제 |
| **EA (Enterprise Architecture)** | 아키텍처 거버넌스 | **TOGAF ADM(Architecture Development Method)** 8단계 사이클. **ArchiMate 3.2** 모델링, **Zachman Framework** 6×6 매트릭스 기반 **Business·Application·Data·Technology** 4계층 정렬 |
| **GRC (Governance, Risk, Compliance)** | 통합 리스크·컴플라이언스 | **RSA Archer·ServiceNow GRC·SAP GRC** 플랫폼으로 **Risk Register·Control Library·Policy Map** 통합 관리. ISO 31000(리스크), ISO 37301(컴플라이언스) 기반 |

**핵심 알고리즘/원리 ①: IT-Biz 정렬(Alignment) Maturity 모델**
Luftman(2000~2024 갱신)의 **Strategic Alignment Maturity Model**은 6개 속성(Communication·Competency·Governance·Partnership·Scope·Skills) × 5단계(Level 1~5)로 측정하며, **Henderson & Venkatraman의 Strategic Alignment Model**은 **Business Strategy ↔ IT Strategy ↔ Organizational Infrastructure ↔ IT Infrastructure**의 4분면 정렬을 다룸. 정렬 점수 = Σ(속성 가중치 × 성숙도) / 6.

**핵심 알고리즘/원리 ②: IT 투자 포트폴리오 최적화**
**Markowitz Modern Portfolio Theory**를 IT에 적용한 **"IT Portfolio Theory"**로, NRR(Net Risk-adjusted Return) = Σ(사업 가치 × 발생 확률) - Σ(실패 비용 × 실패 확률) 공식을 통해 **Run-Grow-Transform** 3분류의 최적 비중 도출. 일반적 가이드라인은 **Run 60-70% / Grow 20-30% / Transform 5-10%**.

- **📢 섹션 요약 비유**: IT 경영관리 7계층은 **항공우주국의 미션 컨트롤(NASA Mission Control)**과 같음. 1층 엔지니어(개발자·운영자) -> 2층 데이터 텔레메트리(CMDB·로그) -> 3~4층 비콘솔(Service·Process) -> 5층 표준 매뉴얼(COBIT·ITIL) -> 6층 모니터(성과·감사) -> 7층 사령탑(Steering Committee)이 **수천 개 센서 데이터를 1초 단위로 종합 판단**해 발사·궤도수정·중단을 결정하는 구조임.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **TOGAF 10** |
| :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 (What/Why) | IT 서비스 관리 (How) | EA 설계·구축 (How to Design) |
| **개발 주체** | ISACA(정보시스템 감사통제협회) | AXELOS(Capita/PeopleCert) | The Open Group |
| **구조** | 5도메인·40 거버넌스·관리 목표 | 34 Practice · 4D 모델 | ADM 8단계 + ADM Cycle |
| **강점** | 컴플라이언스·리스크·감사 특화 | 실무 운영·자동화·고객경험 | 아키텍처 일관성·표준화 |
| **약점** | 구현 가이드 부족, 추상적 | 거버넌스 관점 약함 | 운영·서비스 관점 부족 |
| **주 적용** | CIO·감사·컴플라이언스 부서 | ITSM·Service Desk·DevOps | EA팀·디지털 전환·계획 |
| **연계 프레임워크** | ISO 38500, ISO 27001,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 661 / 800

<- **이전**: [660. IT 경영 관리 핵심 토픽 660번 시험 요약](/studynote/12_it_management/05_security_compliance/660_it_management_core_topic_660_exam_summary/)
**다음**: [662. IT 경영 관리 핵심 토픽 662번 시험 요약](/studynote/12_it_management/05_security_compliance/662_it_management_core_topic_662_exam_summary/) ->

---
