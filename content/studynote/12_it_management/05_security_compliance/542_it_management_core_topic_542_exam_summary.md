---
title: "542. IT 경영 관리 핵심 토픽 542번 시험 요약 (IT Management Core Topic 542 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 542. IT 경영 관리 핵심 토픽 — IT 거버넌스 및 IT 전략 관리

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019(40개 관리목표/EDM 5개 도메인), ISO/IEC 38500(6원칙/3계층 모델), ITIL 4(34개 Practices/SVS 4차원) 프레임워크를 기반으로 RACI 매트릭스, 3 Lines of Defense, Balanced Scorecard(BSC 4관점)를 통해 IT 의사결정 권한·책임·성과측정 체계를 정렬하는 경영 통제 구조
> 2. **가치**: ISACA 보고 기준 COBIT 2019 전사 도입 기업의 IT-비즈니스 정렬도 평균 67%->89%, 프로젝트 실패율 28%->9%, 감사 적시 발견비율 42% 개선, ISO 38500 인증 기업의 이사회 IT 이해도 3.2배 상승 효과
> 3. **판단 포인트**: 중앙집중형(Federal 모델) vs 분산형(CIGOE/Federal+Devolved) 거버넌스, Agile·DevOps 환경에서의 RACI 재설계, 클라우드·AI 도입 시의 새로운 위험 카테고리(AI 거버넌스·윤리) 대응 전략

---

## Ⅰ. 개요 및 필요성

엔론·월드컴 사건(2001~2002) 이후 미국 SOX Act 404조, EU의 8th Company Law Directive(2006) 등 글로벌 규제 환경이 강화되면서 IT 통제의 재무 영향이 부각되었습니다. Gartner(2023)에 따르면 대기업 CIO의 73%가 "IT에 대한 이사회 가시성 부족"을 최우선 과제로 지목하며, 전통적인 ITIL 기반 운영 관리는 충족하나 **전략적 의사결정(EDM)·위험관리·자원배분** 측면의 체계 부재가 핵심 문제로 대두되었습니다.

이에 따라 1992년 ISACA의 COBIT(Control Objectives for Information and Related Technologies) v1.0 출시를 시작으로, 2008년 ISO/IEC 38500, 2019년 COBIT 2019, 2019년 ITIL 4까지 진화하며 **"거버넌스 ≠ 관리(Management)"** 라는 패러다임 전환이 일어났습니다. 거버넌스는 "평가(Evaluate)->지시(Direct)->모니터(Monitor)"의 3단계 사이클로 이사회·경영진이 수행하고, 관리는 "계획(Plan)->구축(Build)->실행(Run)->모니터(Monitor)"의 PBRM 4단계로 실무조직이 담당하는 명확한 역할 분리가 핵심입니다.

```text
+------------------------------------------------------------------+
|           IT 거버넌스 패러다임 전환 (Governance Shift)            |
+------------------------------------------------------------------+
|                                                                  |
|  [레거시: 2000년대 이전]              [모던: 2020년대 이후]      |
|                                                                  |
|  +-----------------+                +-------------------------+  |
|  | IT 운영 중심     |                | 가치(Value)·리스크(Risk) |  |
|  | • ITIL v2/v3    |   -------►     |  ·자원(Resource) 균형   |  |
|  | • SLA·인시던트   |                | • COBIT 2019 + ISO 38500|  |
|  | • 중앙 통제      |                | • 분산형·자동화 거버넌스  |  |
|  +-----------------+                +-------------------------+  |
|                                                                  |
|  +------------------+  SOX 404  +----------------------------+  |
|  | 재무 통제 후행적  | --------► | 위험·가치 중심 선제적      |  |
|  | • 결산 후 적발    |  (2002)   | • 실시간 KRI·KPI 대시보드 |  |
|  +------------------+           +----------------------------+  |
|                                                                  |
|  핵심 변화: "통제"에서 "자율과 책임의 균형"으로                    |
|  Driver: 규제(SOX/BaselⅢ/GDPR) + 기술(Cloud/AI) + 경영(ESG)    |
+------------------------------------------------------------------+
```

**레거시 vs 신패러다임 비교**
- **레거시(2000년대)**: ITIL v2/v3 기반 서비스 데스크 운영, ITSM 도구(BMC Remedy, HP Service Manager)에 의존, IT 성과 = 시스템 가용률(99.9%) 중심
- **모던(2020년대)**: COBIT 2019의 40 Governance & Management Objectives, ISO 38500의 "합리적 사용(Reasonably Prudently)" 원칙, AI 거버넌스(ISO/IEC 42001, NIST AI RMF)와 통합

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **배의 키잡이(Steering)** 와 같습니다. 엔진룸에서 엔진(ITIL·서비스관리)을 고속으로 돌리더라도, 키잡이(거버넌스)가 방향을 잡지 않으면 목적지(비즈니스 목표)에 도달할 수 없습니다. COBIT 2019는 이 키잡이를 위한 나침반·항법장치이고, ISO 38500은 선장(경영진)의 의사결정 매뉴얼입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가. COBIT 2019 핵심 구조

COBIT 2019는 **Governance System(거버넌스 시스템)** + **Governance Framework(거버넌스 프레임워크)** 의 이원 구조로 설계되었습니다. 거버넌스 시스템은 5개 도메인(EDM: Evaluate-Direct-Monitor, APO: Align-Plan-Organize, BAI: Build-Acquire-Implement, DSS: Deliver-Service-Support, MEA: Monitor-Evaluate-Assess) 내 40개의 관리목표(Management Objective)로 구성됩니다. 각 목표는 **Process Capability Level 0~5(ISO 15504 PAM 기준)** 로 측정되며, 2019 버전부터 **중첩(AND), 집중(OR), 우선순위(PRIORITY)** 의 3가지 Cascade 방식으로 목표를 기업 상황에 맞게 선별 적용합니다.

### 나. ISO/IEC 38500 3계층 모델

ISO/IEC 38500은 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)을 **3계층(Director -> Manager -> Operator)** 에 적용합니다. 핵심은 **"Directors(임원)가 IT 의사결정의 결과에 대한 최종 책임**을 진다는 원칙이며, 단순히 IT 부서에 위임하는 구조를 거부합니다.

```text
+---------------------------------------------------------------------+
|          COBIT 2019 + ISO 38500 통합 거버넌스 아키텍처              |
+---------------------------------------------------------------------+
|                                                                     |
|  +- Tier 1: DIRECTORS (이사회/CEO) ----------------------------+   |
|  |  • ISO 38500 6원칙 적용                                       |   |
|  |  • COBIT 2019 EDM Domain (EDM01~05)                          |   |
|  |    EDM01: 거버넌스 체계 설정  EDM02: 가치 제공 보장           |   |
|  |    EDM03: 위험 최적화        EDM04: 자원 최적화              |   |
|  |    EDM05: 이해관계자 투명성                                  |   |
|  |  • 산출물: IT 전략서, 위험 허용 한계(Risk Appetite) 선언     |   |
|  +------------------------------------------------------------+   |
|                              v 책임 위임 (Delegation)              |
|  +- Tier 2: MANAGERS (CIO/IT임원) -----------------------------+   |
|  |  • COBIT 2019 APO/BAI Domain (32개 목표)                     |   |
|  |  • APO12: 위험 관리  APO13: 보안 관리  BAI01: 프로그램 관리  |   |
|  |  • RACI 매트릭스 (Responsible/Accountable/Consulted/Informed)|   |
|  |  • 산출물: IT 포트폴리오, 아키텍처 결정서, 예산 배분 계획    |   |
|  +------------------------------------------------------------+   |
|                              v 운영 위임                            |
|  +- Tier 3: OPERATORS (현업/IT 실무) --------------------------+   |
|  |  • COBIT 2019 DSS/MEA Domain (8개 목표)                       |   |
|  |  • ITIL 4 34 Practices (Service Value System, SVS)           |   |
|  |  • DSS01~05: 운영  DSS06: 보안 운영  MEA01: 성과 모니터링   |   |
|  |  • 산출물: 인시던트 리포트, 변경 요청, KPI 대시보드          |   |
|  +------------------------------------------------------------+   |
|                                                                     |
|  -- 측정 체계 ----------------------------------------------------  |
|  Capability Level: 0(Incomplete)~5(Optimizing) - ISO/IEC 15504    |
|  Focus Area Maturity: EDM 도메인은 Level 4(Quantitatively Managed) |
|                        DSS 도메인은 Level 3(Defined Process) 목표   |
|                                                                     |
|  -- 연계 프레임워크 ----------------------------------------------  |
|  TOGAF 10 (ADM 사이클) ↔ COBIT 2019 ↔ ITIL 4 ↔ ISO 27001 ↔ PMBOK  |
+---------------------------------------------------------------------+
```

### 다. Three Lines of Defense (3 LoD) 모델

IIA(Institute of Internal Auditors)가 2020년 7월 개정 모델로 제시한 위험 관리 체계입니다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **1st LoD: Operational Management** | 일상적 위험 통제 수행, KRI(Key Risk Indicator) 모니터링 | • 셀프 평가(Self-Assessment) <br> • RCSA(Risk Control Self-Assessment) 분기별 실시 <br> • 이슈 관리 시스템(Jira/ServiceNow GRC) 연동 |
| **2nd LoD: Risk & Compliance** | 위험·규제 정책 수립, 1st LoD 감독, 독립 모니터링 | • GRC 플랫폼(Archer, ServiceNow IRM, SAP GRC) 운영 <br> • ISO 31000 Risk Treatment Plan 수립 <br> • SOX 404 ITGC 150+ 통제항목 검증 |
| **3rd LoD: Internal Audit** | 1·2nd LoD의 독립적 검증, 이사회 Audit Committee 보고 | • IIA Standards 2020 (CIPM, COSO ERM 2017 연계) <br> • 위험 기반 감사(RBAS, Risk-Based Audit Strategy) <br> • 데이터 분석(CAATs) 기반 전수 검증 |
| **External Assurance** | 외부 이해관계자에게 독립 보증 제공 | • 빅4 회계법인 IT 일반 통제 감사(Financial Audit 연동) <br> • ISO 27001/27701/38500 인증 심사 <br> • K-ISMS/PIMS 인증원 심사 |

### 라. Balanced Scorecard (BSC) for IT

Kaplan & Norton의 4관점(재무·고객·내부프로세스·학습성장)을 IT에 적용한 전략 측정 체계입니다. NVidia, IBM 등 글로벌 대기업은 **"IT Strategy Map"** 으로 시각화하여 활용합니다. 2024년 Gartner 발표 기준 BSC-IT를 도입한 기업은 IT 성과 측정 정밀도가 평균 2.7배 향상되었습니다.

- **📢 섹션 요약 비유**: COBIT 2019의 40개 관리목표는 마치 **건물의 40개 안전 점검 항목**(소방, 전기, 구조, 환기 등) 목록과 같습니다. ISO 38500은 이 점검을 총괄하는 **건물주(임원)** 의 매뉴얼이고, ITIL 4는 실제 점검을 수행하는 **시설 관리팀** 의 작업지침서입니다. 3 Lines of Defense는 점검자(1st LoD), 안전관리자(2nd LoD), 소방관(3rd LoD)의 3중 안전망입니다.

---

## Ⅲ. 비교 및 연결

### 가. 주요 IT 거버넌스 프레임워크 비교

| 구분 | COBIT 2019 | ISO/IEC 38500 | ITIL 4 | COSO ERM 2017 |
|:---|:---|:---|:---|:---|
| **주 목적** | IT 거버넌스·관리 통합 프레임 | IT 의사결정 6원칙 가이드 | IT 서비스 운영 최적화 | 전사 위험 관리 |
| **대상 계층** | 이사회~현업(Tier 1~3) | 이사회(Director) 중심 | 실무 운영(Operator) | 전사(CRO/이사회) |
| **구성 요소** | 40 관리목표, 7 컴포넌트, 5 도메인 | 6원칙, 3계층 모델, 모델 정책 | 34 Practices, 4D SVS, 7 Guiding Principles | 5 컴포넌트, 20 원칙 |
| **측정 체계** | ISO 15504 PAM 0~5 레벨 | 원칙
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 542 / 800

<- **이전**: [541. IT 경영 관리 핵심 토픽 541번 시험 요약](/studynote/12_it_management/05_security_compliance/541_it_management_core_topic_541_exam_summary/)
**다음**: [543. IT 경영 관리 핵심 토픽 543번 시험 요약](/studynote/12_it_management/05_security_compliance/543_it_management_core_topic_543_exam_summary/) ->

---
