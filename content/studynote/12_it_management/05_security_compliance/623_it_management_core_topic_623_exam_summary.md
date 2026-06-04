---
title: "623. IT 경영 관리 핵심 토픽 623번 시험 요약 (IT Management Core Topic 623 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019의 거버넌스/관리 목적(40개 EDM/Align/Plan/Build/Run/Monitor), ITIL 4의 34개 실무(Service Value System), ISO 27001:2022의 Annex A 93통제항목, PMBOK 7th의 8개 성과영역 및 12가지 원칙을 하나의 가치사슬로 통합하여, IT 투자 대비 ROI·TCO·NPV를 최적화하는 경영 의사결정 체계
> 2. **가치**: McKinsey 2023 조사에 따르면 디지털 전환 성공 기업은 Revenue Growth 1.8배, Cost Efficiency 20~30% 개선, Time-to-Market 50% 단축, ISO 27001 인증 기업은 정보유출 사고 60% 감소(IBM 2022), FinOps 도입 시 클라우드 비용 15~40% 절감(Flexera 2024)
> 3. **판단 포인트**: COBIT vs ITIL(거버넌스-프로세스), Waterfall vs Agile-Predictive(프로젝트 성격), Build vs Buy vs SaaS(TCO 3~7년 분석), On-Premise vs Hybrid vs Multi-Cloud(데이터 주권/레이턴시), 내부 통제 vs ISAE 3402/ISO 27701(감사 대응) - **"Why -> What -> How -> Measure" 4단계 계층에서 의사결정 정렬이 핵심**

---

## Ⅰ. 개요 및 필요성

정보기술의 역할이 단순 업무지원(Back-Office Automation)에서 **전략적 핵심자산(Strategic Differentiator)**으로 전환됨에 따라, IT 투자의 정당성 확보·리스크 통제·가치 실현을 위한 **통합 IT 경영관리 체계**의 수립이 필수 불가결한 경영 과제로 부상했다. 과거 1990년대~2000년대에는 CIO가 인프라·시스템 단위의 기술 관점에 머물렀다면, 2010년대 이후 CFO·CEO·CDO와 동등한 위치에서 **Digital Strategy -> Enterprise Architecture -> Portfolio -> Project -> Service -> Security -> Operation** 전 영역을 End-to-End로 책임지는 역할로 진화했다.

특히 Gartner(2023)는 전 세계 IT 지출 규모를 **4.6조 USD(2022) -> 5.1조 USD(2024)**로 전망하며, 이 중 **75%가 Digital Transformation과 Cloud Migration**에 집중된다고 발표했다. 그러나 BCG(2023)의 조사에 따르면 DX 프로젝트의 **70%가 ROI 미달 또는 실패**로 끝나며, 실패 원인의 상위 3개는 ① 경영진-현업-IT 간 정렬 부재(38%), ② 거버넌스 미비(27%), ③ 변화관리 실패(22%)로 나타났다. 이는 **"기술"이 아닌 "경영·사람·프로세스"의 문제**가 핵심임을 의미한다.

한국 정보통신기술협회(TTA)의 2023년 보고에 따르면, 국내 500대 기업 중 **42.6%**가 COBIT 기반 IT 거버넌스를 도입했고, **35.2%**가 ITIL 기반 서비스 운영체계를 갖추고 있으나, 두 체계를 **통합 관점**으로 운용하는 비중은 **18.4%**에 불과하다. ISMS-P(정보보호관리체계)는 2024년 기준 약 1,800여 개 인증 기업이 존재하며, 2023년 개인정보보호법 전면 개정(가명정보 도입, 자동화 의사결정 투명성 의무화)으로 통제 항목이 강화되었다.

### 🔍 Old Paradigm vs New Paradigm 비교

| 구분 | Legacy IT 관리 (1990~2010) | Modern IT 경영 (2020~현재) |
|:---|:---|:---|
| **조직구조** | 기능별 사일로(개발팀·운영팀·보안팀) | E2E Product Team(SRE + Dev + Sec + BA) |
| **투자 결정** | Capex 일변주, 3~5년 ROI | Opex+Capex 혼합, Payback 12~18개월 |
| **아키텍처** | 모놀리식 On-Premise | Cloud-Native, Microservices, API-First |
| **관리 프레임워크** | COBIT 4/5 + ITIL v3(단계적) | COBIT 2019 + ITIL 4 + DevOps + FinOps |
| **리스크 대응** | 사후 통제, 연간 감사 | 실시간 GRC, Zero Trust, Continuous Audit |
| **성과 측정** | 가용성(99.9%)·처리량 중심 | NPS, MTTR, Change Failure Rate, DORA 4대 지표 |
| **보안 모델** | Castle & Moat 경계 보안 | Zero Trust, SASE, XDR, SBOM |
| **프로젝트 관리** | Waterfall, Plan-driven | Hybrid(Agile-Predictive), OKR+Jira+Kanban |

```text
+--------------------------------------------------------------------------+
|         통합 IT 경영관리 5대 핵심 토픽 (Topic 623) 관계도                |
+--------------------------------------------------------------------------+
|                                                                          |
|   +-----------------+         +-----------------+                       |
|   | [1] IT 거버넌스  |◄--------+  [2] 디지털 전환  |                       |
|   |   - COBIT 2019   | 전략   |      전략         |                       |
|   |   - ISO 38500    | 정렬   |   - McKinsey 7S  |                       |
|   |   - ISO 27001    |       |   - 디지털 성숙도 |                       |
|   |   - ISO 20000    |       |   (DMM 5단계)    |                       |
|   +--------+---------+       +--------+---------+                       |
|            |                          |                                  |
|            | 아키텍처 매핑              | 포트폴리오화                      |
|            v                          v                                  |
|   +-----------------+         +-----------------+                       |
|   | [3] 엔터프라이즈  |◄--------+  [4] 프로젝트·서비스 |                       |
|   |   아키텍처(EA)    | 구현   |      운영체제       |                       |
|   |   - TOGAF 10 ADM |       |   - PMBOK 7th     |                       |
|   |   - DoDAF 2.02   |       |   - PRINCE2 7     |                       |
|   |   - FEAF/Gartner |       |   - ITIL 4 SVS    |                       |
|   +--------+---------+       |   - DevOps/DORA  |                       |
|            |                  +--------+---------+                       |
|            | 기술거버넌스               | 모니터링                          |
|            v                          v                                  |
|   +-------------------------------------------------+                   |
|   |      [5] IT 리스크·보안·컴플라이언스 거버넌스      |                   |
|   |       - NIST CSF 2.0 / ISO 27001:2022           |                   |
|   |       - ISMS-P / 개인정보보호법 2023             |                   |
|   |       - ISAE 3402 / SOC 2 Type II               |                   |
|   |       - FinOps / 그린 IT / ESG-ICT               |                   |
|   +-------------------------------------------------+                   |
|                                                                          |
|   ★ Top-Down: 전략->거버넌스->아키텍처->프로젝트->운영                       |
|   ★ Bottom-Up: 운영지표->리스크->프로젝트 회고->전략 피드백                  |
+--------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영관리를 **자동차 운행**에 비유하면, COBIT은 "**운전면허·교통법규**", TOGAF는 "**내비게이션·도로지도**", ITIL은 "**정비 매뉴얼·소모품 교체주기**", PMBOK은 "**출발부터 목적지까지의 여정 계획서**", ISO 27001은 "**도난방지·사고보험**"입니다. 시트벨트·에어백(ZT·XDR) 없이는 아무리 좋은 차도 사고 시 탑승자를 보호할 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [1] COBIT 2019 — IT 거버넌스의 국제 표준 프레임워크

COBIT(Control Objectives for Information and Related Technologies)은 ISACA(Information Systems Audit and Control Association)가 1996년 v1.0을 발표하여 2005년 v4.0, 2012년 v5.0, 2018년 v2019로 진화한 **IT 거버넌스·관리 통합 프레임워크**이다. COBIT 2019는 **40개의 거버넌스/관리 목적(Governance & Management Objectives)**을 체계화하고, ISO/IEC 38500(기업 IT 거버넌스 국제표준)과 IEC/ISO 27001, ITIL 4, CMMI, TOGAF 등 50여 개 외부 표준을 **하나의 매핑 구조**로 연결하는 **Integrator** 역할을 수행한다.

```text
+----------------------------------------------------------------------+
|              COBIT 2019 핵심 5개 도메인 + 40개 목적 매트릭스          |
+----------------------------------------------------------------------+
|                                                                      |
|   +-------------------------------------------------------------+    |
|   |  EDM(5): 거버넌스 위원회 — Evaluate, Direct, Monitor        |    |
|   |   EDM01 거버넌스 체계 수립      EDM02 이익배분 체계          |    |
|   |   EDM03 리스크 관리 최적화      EDM04 자원 관리 최적화       |    |
|   |   EDM05 투명성 보장·이해관계자  EDM05 (단일 EDM 도메인)      |    |
|   +-------------------------------------------------------------+    |
|                          v                                            |
|   +-------------------------------------------------------------+    |
|   |  Align, Plan & Organize(APO, 14개) — 전략·계획·조직        |    |
|   |   APO01 관리 프레임워크  APO02 전략  APO03 조직             |    |
|   |   APO04 혁신  APO05 포트폴리오  APO06 예산·비용              |    |
|   |   APO07 인적자원  APO08 관계  APO09 서비스계약              |    |
|   |   APO10 공급자  APO11 품질  APO12 리스크                    |    |
|   |   APO13 보안정보  APO14 데이터                               |    |
|   +-------------------------------------------------------------+    |
|                          v                                            |
|   +-------------------------------------------------------------+    |
|   |  Build, Acquire & Implement(BAI, 11개) — 구축·도입          |    |
|   |   BAI01 프로그램  BAI02 요구사항  BAI03 솔루션 식별          |    |
|   |   BAI04 가용성·용량  BAI05 조직 변화  BAI06 변경             |    |
|   |   BAI07 도입  BAI08 지식  BAI09 자산  BAI10 구성            |    |
|   |   BAI11 프로젝트                                            |    |
|   +-------------------------------------------------------------+    |
|                          v                                            |
|   +-------------------------------------------------------------+    |
|   |  Deliver, Service & Support(DSS, 6개) — 운영·지원           |    |
|   |   DSS01 운영  DSS02 서비스 요청·사고  DSS03 문제             |    |
|   |   DSS04 연속성  DSS05 보안서비스  DSS06 비즈니스 통제        |    |
|   +-------------------------------------------------------------+    |
|                          v                                            |
|   +-------------------------------------------------------------+    |
|   |  Monitor, Evaluate & Assess(MEA, 3개) — 성과평가            |    |
|   |   MEA01 성과·내부통제  MEA02 외부통제  MEA03 컴플라이언스    |    |
|   +-------------------------------------------------------------+    |
|                                                                      |
|   ★ 7개 컴포넌트: Process / Organizational Structures / Information  |
|     Flow / People, Skills & Competencies / Policies & Procedures /  |
|     Culture, Ethics & Behavior / Services, Infrastructure & Apps     |
|                                                                      |
|   ★ 능력수준 6단계(PA 0~5): Incomplete->Initial->Managed->Defined->     |
|     Quantitatively Managed->Optimizing                                 |
+----------------------------------------------------------------------+
```

### [2] ITIL 4 — IT 서비스 관리의 글로벌 Best Practice

ITIL(Information Technology Infrastructure Library)은 1989년 영국 정부(CCTA/OGC)에서 출발하여 2019년 v4(현재 2020년 v4.1까지)로 진화한 **서비스 중심(Service-Oriented) IT 운영 프레임워크**이다. COBIT이 "거버넌스·관리 통제"라면, ITIL 4는 "**고객에게 가치를 전달하는 실무 관행**"에 집중한다.

```text
+----------------------------------------------------------------------+
|              ITIL 4 Service Value System (SVS) 전체 구조              |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------------------------------------------------------+       |
|   |   [ Opportunity / Demand / Value ]  ◄-- 외부 입력        |       |
|   +---------------------+------------------------------------+       |
|                         v                                            |
|   +----------------------------------------------------------+       |
|   |     Guiding Principles (7대 지침 원칙)                   |       |
|   |   ① Focus on value    ② Start where you are             |       |
|   |   ③ Progress iteratively with feedback                   |       |
|   |   ④ Collaborate and promote visibility                   |       |
|   |   ⑤ Think and work holistically                          |       |
|   |   ⑥ Keep it simple and practical                         |       |
|   |   ⑦ Optimize and automate                               |       |
|   +---------------------+------------------------------------+       |
|                         v                                            |
|   +----------------------------------------------------------+       |
|   |     Governance (거버넌스 정책·위원회 — COBIT 연계)       |       |
|   +---------------------+------------------------------------+       |
|                         v                                            |
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 623 / 800

<- **이전**: [622. IT 경영 관리 핵심 토픽 622번 시험 요약](/studynote/12_it_management/05_security_compliance/622_it_management_core_topic_622_exam_summary/)
**다음**: [624. IT 경영 관리 핵심 토픽 624번 시험 요약](/studynote/12_it_management/05_security_compliance/624_it_management_core_topic_624_exam_summary/) ->

---
