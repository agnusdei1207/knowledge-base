---
title: "696. IT 경영 관리 핵심 토픽 696번 시험 요약 (IT Management Core Topic 696 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019, ITIL 4, ISO 38500, BSC-IT 4대 프레임워크를 기반으로 IT-Business Alignment(전략적 정렬)와 IT Value Realization(가치 실현)을 위한 거버넌스·프로세스·성과관리 체계를 통합 운영하는 활동임
> 2. **가치**: 정량적 효과로 IT 투자 대비 ROI 15~30% 향상, 운영 비용 OPEX 20~25% 절감, 프로젝트 실패율 40%->12% 감소, 정성적 효과로 이사회-경영진-IT간 의사결정 투명성 확보 및 리스크 가시화 달성
> 3. **판단 포인트**: Build vs Buy vs Cloud 의사결정 시 TCO 5년 분석, Center-led vs Federated 거버넌스 모델 선택, Agile-Waterfall 혼합(SAFe, Spotify) 방법론 적용, Shadow IT 25~30% 잠재 비용의 가시화 전략이 핵심 쟁점

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 시대의 IT 경영관리는 단순 비용센터 관리를 넘어 **"Digital Business Platform"**으로서의 역할을 수행해야 함. Gartner(2024) 보고에 따르면 글로벌 CEO의 89%가 "IT가 사업 성공의 핵심"이라 답했으나, McKinsey 조사에서는 디지털 전환 프로젝트의 **70%만이 비즈니스 목표를 달성**하고 있어 IT-Business 간 전략적 갭이 심각한 상황임.

특히 한국 시장은 OECD 디지털정부평가에서 1위를 차지하고 있으나, 민간의 IT 성숙도는 글로벌 평균 대비 1.5단계 낮아 (CMMI 기준 Level 2.3) IT 거버넌스 체계 정비가 시급함. 기술사 관점에서는 IT를 **"전략 자산(Strategic Asset)"**으로 전환하는 4대 축—거버넌스(Governance), 포트폴리오(Portfolio), 프로세스(Process), 성과(Performance)—의 통합 설계 능력이 요구됨.

```text
+---------------------------------------------------------------------+
|              IT 경영관리 4대 축 통합 프레임워크 (4 Pillars)            |
+---------------------------------------------------------------------+
|                                                                     |
|   +----------+   +----------+   +----------+   +----------+        |
|   |Governance|   |Portfolio |   | Process  |   |Performance|       |
|   |  거버넌스 |   | 포트폴리오|   | 프로세스  |   |   성과    |       |
|   +----+-----+   +----+-----+   +----+-----+   +----+-----+        |
|        |              |              |              |              |
|        |  +-----------v--------------v--------------v------+        |
|        +-►|        IT-Business Alignment (전략 정렬)       |        |
|           |   Mission -> Strategy -> Goals -> Objectives     |        |
|           |   Ward & Peppard 방법론 (2016, 4th Ed.)        |        |
|           +--------------------+--------------------------+        |
|                                |                                   |
|   +----------------------------v-----------------------------+    |
|   |        IT Value Realization (가치 실현)                    |    |
|   |   IT투자 -> IT자산 -> IT서비스 -> 비즈니스역량 -> Business Value|   |
|   |   (Thorp, The Information Paradox, 2003)                   |    |
|   +------------------------------------------------------------+   |
|                                                                     |
|   4대 프레임워크 매핑:                                              |
|   • COBIT 2019  -> 거버넌스/성과(40 Process, 5 Domains)              |
|   • ITIL 4      -> 프로세스/서비스(34 Practices)                    |
|   • ISO 38500   -> 거버넌스(6 Principles)                            |
|   • BSC/IT-BSC  -> 성과(4 Perspectives)                             |
+---------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교:**
- 기존(2000년대): IT는 **Cost Center**, CapEx 중심, Waterfall, 부서별 분산 거버넌스
- 신규(2024~): IT는 **Value Center**, OpEx+CapEx 혼합, Agile/DevOps, 통합 거버넌스(COBIT 기반 Federated 모델)
- 결정적 차이: "IT spends money" -> "IT makes money"로의 인식 전환과 이를 입증하는 **Measurement 체계**의 부재가 핵심 문제

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **오케스트라의 지휘자**와 같습니다. 바이올린(개발팀), 첼로(운영팀), 트럼펫(인프라팀) 등 각 악기(부서)가 제각기 연주하면 소음이지만, COBIT이라는 악보(표준)와 ITIL이라는 지휘봉(프로세스)이 조화를 이루면 하나의 아름다운 협주곡(비즈니스 가치)이 완성됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리 시스템은 **3-Tier 의사결정 구조**와 **4-Layer 운영 모델**로 구성됨. 상위 의사결정(거버넌스), 중위 관리(포트폴리오/프로그램), 하위 실행(프로젝트/운영) 간의 **Closed-Loop Feedback**이 핵심 동작 원리임.

```text
+---------------------------------------------------------------------+
|                  IT 경영관리 참조 아키텍처 (3-Tier × 4-Layer)        |
+---------------------------------------------------------------------+
|                                                                     |
|  +-------------------------------------------------------------+  |
|  | Tier 1: 전략 의사결정 (이사회/CEO/CIO) - 연 1~4회 회의       |  |
|  |  +------------------------------------------------------+  |  |
|  |  | IT Strategy Committee / IT Steering Committee        |  |  |
|  |  | • IT 전략 승인, 포트폴리오 우선순위, 예산 한도 결정    |  |  |
|  |  | • Input: BSC-IT, Industry Benchmark, Risk Profile     |  |  |
|  |  +------------------------------------------------------+  |  |
|  +----------------------------+--------------------------------+  |
|                               |                                   |
|  +----------------------------v-----------------------------+    |
|  | Tier 2: 운영 관리 (PMO/서비스관리) - 월 1~주 1회 회의      |    |
|  |  +-------------+  +--------------+  +--------------+    |    |
|  |  |  Portfolio  |  |   Program    |  |   Service    |    |    |
|  |  |  Management |  |  Management  |  |  Management  |    |    |
|  |  | (PfM)       |  |   (PgM)      |  |   (ITIL)     |    |    |
|  |  +-------------+  +--------------+  +--------------+    |    |
|  +----------------------------+-----------------------------+    |
|                               |                                   |
|  +----------------------------v-----------------------------+    |
|  | Tier 3: 실행 (팀/실무) - 일/시간 단위                       |    |
|  |  +-------------+  +--------------+  +--------------+    |    |
|  |  |   Project   |  |   Operation  |  |   Support    |    |    |
|  |  |  (Agile/    |  |  (SRE/DevOps)|  |  (ITSM)      |    |    |
|  |  |   Waterfall)|  |              |  |              |    |    |
|  |  +-------------+  +--------------+  +--------------+    |    |
|  +----------------------------------------------------------+    |
|                                                                     |
|  4-Layer 운영 모델:                                                |
|  +----------------------------------------------------------+    |
|  | L1: Business Layer    - 전략/목표 (Strategy Map)          |    |
|  | L2: Application Layer - 정보시스템/서비스 (Catalog)        |    |
|  | L3: Technology Layer  - 인프라/플랫폼 (CMP/IaC)           |    |
|  | L4: Security Layer    - 거버넌스/컴플라이언스 (GRC)        |    |
|  +----------------------------------------------------------+    |
|                                                                     |
|  핵심 메커니즘: RACI 매트릭스 + Closed-Loop KPI 측정                |
|  (Plan -> Execute -> Monitor -> Adjust)                               |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회** | IT 의사결정 최고 기구 (의장: CEO 또는 CIO) | COBIT 2019의 40개 Governance/Management Objectives 중 EDM( Evaluate, Direct, Monitor) 5개 프로세스 수행, 분기별 정례 회의 + 임시 회의, 의사결정 기록 RACI 매트릭스 기반 |
| **PMO(Project Management Office)** | 프로젝트 포트폴리오 통합 관리, 표준화, 보고 | PfM(Portfolio Management) - Stage-Gate 모델(Initiation->Selection->Planning->Execution->Closure), PMBOK 7th + PRINCE2 + SAFe 혼합, 도구: MS Project Online, Planview, Clarity PPM, Jira Align(스케일) |
| **IT 서비스 운영 조직** | 일일 IT 서비스 제공, Incident/Problem/Change 관리 | ITIL 4의 34개 Practice 중 Incident Mgmt(MTTR<4h, SLA 99.9%), Change Mgmt(CAB 주간), Service Desk(Tier1/2/3), 도구: ServiceNow ITSM, BMC Helix, Jira Service Management |
| **IT 성과 측정 시스템** | KPI/KGI 측정 및 보고, BSC-IT 4관점 운영 | BSC-IT 4관점(Financial/Customer/Internal Process/Learning&Growth), COBIT 2019의 13개 Process 측정 메트릭, ISO/IEC 33000 Capability Level 1~5 평가, 도구: Power BI, Tableau, Grafana, SAP BusinessObjects |
| **GRC(Governance Risk Compliance)** | 리스크 식별/평가/대응, 컴플라이언스 준수 | ISO 31000 Risk Management, COBIT 2019 Risk Mgmt Objective(EDM03, APO12), 컴플라이언스: 개인정보보호법, ISMS-P, PCI-DSS, GDPR, SOX, 도구: RSA Archer, ServiceNow GRC, SAP GRC |
| **EA(Enterprise Architecture)** | IT 투자 정렬, 중복 제거, 표준화 | TOGAF 10 ADM(Architecture Development Method), 4 Domain(BA/DA/TA/SA), Zachman Framework 6×6 매트릭스, FEAF(Federal EA), 한국: e-정부 EA 프레임워크, 도구: Ardoq, LeanIX, Sparx EA |

**핵심 파라미터 및 알고리즘:**

1. **IT 포트폴리오 우선순위 결정 모델**:
   - NPV(순현재가치) 가중치 30% + 전략 정합성 25% + 리스크 20% + ROI 15% + 자원 가용성 10%
   - 공식: Priority Score = Σ(Wi × Si) / ΣWi (가중치합)
   - 임계값: 70점 이상 -> 실행, 50~70점 -> 재검토, 50점 미만 -> 보류/폐기

2. **TCO(Total Cost of Ownership) 산정 (5년)**:
   - TCO = CapEx + OpEx(5년) + Hidden Cost(Shadow IT, 기술부채, 교육)
   - 일반 비율: CapEx:OpEx = 30:70 (성숙 조직), 50:50 (전환기)
   - 클라우드 TCO = 컴퓨팅(40%) + 스토리지(20%) + 네트워크(15%) + 라이선스(15%) + 운영인력(10%)

3. **IT 성숙도 측정 모델**:
   - CMMI 5단계(Initial->Managed->Defined->Quantitatively Managed->Optimizing)
   - COBIT 2019 Maturity Model: Level 0(Incomplete) ~ Level 5(Optimizing)
   - 한국 평균: Level 2.3, 글로벌 Top 10% 기업: Level 4.1

4. **KPI 연결 사슬 (KGI->CSF->KPI)**:
   - KGI: "매출 10% 증가" -> CSF: "고객 이탈률 5% 감소" -> KPI: "시스템 가용성 99.95% 달성"

- **📢 섹션 요약 비유**: IT 경영관리 시스템은 **자동차의 계기판과 내비게이션**과 같습니다. 속도계(KPI)와 연료계(예산)는 현재 상태를, 내비게이션(전략)은 어디로 가야 할지, 경고등(리스크 알림)은 위험을 알려줍니다. 이 셋이 통합되어야 목적지(비즈니스 목표)에 안전하게 도착할 수 있습니다.

---

## Ⅲ. 비교 및 연결

IT 경영관리 관련 프레임워크/방법론은 상호 보완적이나 적용 범위와 관점이 상이함. 기술사 답안 시 **"무엇이 아닌 무엇을 위해"** 적용하는지 명확히 구분해야 함.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **BSC-IT (Kaplan-Norton)** |
| :--- | :--- | :--- | :--- | :--- |
| **목적/관점** | 거버넌스 + 관리 (What/Why) | 서비스 라이프사이클 (How) | 이사회 거버넌스 원칙 (Why) | 전략적 성과 측정 (What) |
| **적용 범위** | Enterprise-wide IT | IT 서비스 운영 | 이사회/경영진 의사결정 | 전략 실행/측정 |
| **구성 요소** | 40 Process × 5 Domain (EDM/APO/BAI/DSS/MEA) | 34 Practice × 4 Dimension | 6 Principles + 3 Tasks | 4 Perspective × BSC |
| **측정 강조도** | ★★★★★ (Process KPI 중심) | ★★★ (Service KPI - SLA, MTTR) | ★ (원칙적) | ★★★★★ (성과/인과관계) |
| **인증/감사** | COBIT Certified Assessor | ITIL Foundation/Master | ISO 인증 가능 | 자체 인증 |
| **강점** | 컴플라이언스, 감사 친화, Risk-IT 통합 | 실무 적용 용이, ServiceNow 등 도
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 696 / 800

<- **이전**: [695. IT 경영 관리 핵심 토픽 695번 시험 요약](/studynote/12_it_management/05_security_compliance/695_it_management_core_topic_695_exam_summary/)
**다음**: [697. IT 경영 관리 핵심 토픽 697번 시험 요약](/studynote/12_it_management/05_security_compliance/697_it_management_core_topic_697_exam_summary/) ->

---
