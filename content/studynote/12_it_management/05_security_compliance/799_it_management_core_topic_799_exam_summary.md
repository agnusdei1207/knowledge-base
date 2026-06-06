---
title: "IT Management Core Topic 799 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 기술사 799번은 COBIT 2019 거버넌스 체계, ISO 38500 원칙, ITIL 4 서비스 가치사슬을 통합한 **"거버넌스-전략-운영-컴플라이언스" 4축 메타 프레임워크**로, 기업 IT 자산을 비즈니스 가치로 전환하는 의사결정 구조를 평가하는 최종 종합형 문항이다.
> 2. **가치**: EA(Enterprise Architecture) 정합도 90% 이상, IT 투자 ROI 평균 25~40% 향상, 인시던트 MTTR 60% 단축, ISMS-P 인증 갱신 비용 30% 절감 등 **정량 KPI와 거버넌스 성숙도(Level 3->Level 5)**의 양면 개선을 통해 경영 가시성을 확보한다.
> 3. **판단 포인트**: **"Build vs Buy vs Cloud vs SaaS"**, **"Bimodal IT (Mode 1 vs Mode 2)"**, **"Zero Trust vs Defense-in-Depth"**, **"ROI vs NPV vs IRR vs EVA"**의 트레이드오프를 사업 연속성(BCP/DR), 컴플라이언스(개인정보보호법·GDPR·DORA), 기술부채(Technical Debt) 회계 처리 관점에서 종합 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 799번 문항은 전자계산기조직응용기술사·정보관리기술사 시험의 **최상위 종합문항**으로, 단순 암기형 지식이 아닌 **상황 판단 + 프레임워크 적용 + 정량 산출 + 거버넌스 의사결정**을 한 문제당 25분 안에 도출해야 하는 압축적 사고력을 요구한다. 2022년 NCS 개편 이후 799번은 "신기술 트렌드 + IT 거버넌스 + 디지털전환 전략"을 융합한 메타 토픽이 출제되며, COBIT 2019의 40개 Governance/Management Objective와 ISO 38500의 6대 원칙(R·A·C: Responsibility, Accountability, Consulted, Informed)을 모르면 합격선(평균 60점/100점)에 도달할 수 없다.

핵심 배경은 **"IT-Business Alignment Gap"**이다. Gartner(2023) 보고에 따르면 글로벌 CIO의 78%가 "IT 투자가 비즈니스 KPI와 직접 연결되지 않는다"고 답했으며, McKinsey는 디지털 전환 프로젝트의 70%가 실패하는 원인을 **"거버넌스 부재 + ROI 미계측 + 조직 저항"** 3대 요인으로 분석한다. 799번은 바로 이 갭을 메우는 **평가·지시·모니터(Evaluate-Direct-Monitor) 사이클**을 설계·검증·감사하는 능력을 측정한다.

```text
+--------------------------------------------------------------------+
|          799번 메타 프레임워크: 4-Layer Governance Stack           |
+--------------------------------------------------------------------+
|                                                                    |
|   [Layer 4] 전략/트렌드         ^                                  |
|   +-----------------------+    |                                  |
|   | DX 전략 / AI 거버넌스   |    |   - Digital Twin                  |
|   | ESG·DORA·AI Act        |    |   - GenAI 윤리 (NIST AI RMF)      |
|   | 플랫폼 비즈니스 모델    |    |   - Cloud FinOps                  |
|   +----------+------------+    |   - Zero Trust Architecture        |
|              |                  |                                  |
|   [Layer 3] 거버넌스/컴플라이언스|                                  |
|   +----------v------------+    |   - COBIT 2019 (40 Objectives)    |
|   | ISO 38500 (R·A·C·I)   |    |   - IT 거버넌스 위원회             |
|   | ISMS-P / ISO 27001     |    |   - 3 Lines of Defense Model      |
|   | 개인정보보호법·GDPR     |    |   - 내부통제 (SOX 404)             |
|   +----------+------------+    |                                  |
|              |                  |                                  |
|   [Layer 2] 아키텍처/운영       |                                  |
|   +----------v------------+    |   - TOGAF 10 ADM (8 Phase)        |
|   | EA(전사아키텍처)         |    |   - 마이크로서비스 / 이벤트드리븐    |
|   | ITIL 4 Service Value Chain|   - DevSecOps Pipeline             |
|   | SLA/OLA/SLR 체계        |    |   - Site Reliability Engineering   |
|   +----------+------------+    |                                  |
|              |                  |                                  |
|   [Layer 1] 인프라/데이터       |                                  |
|   +----------v------------+    |   - Multi/Hybrid Cloud             |
|   | IaaS·PaaS·SaaS·FaaS    |    |   - Kubernetes / Service Mesh      |
|   | 데이터 거버넌스 (DAMA)   |    |   - Data Lakehouse (Iceberg)       |
|   | BCP/DR (RTO/RPO)       |    |   - SOC / SIEM / SOAR              |
|   +-----------------------+    |                                  |
|                              v                                    |
|              [사업 가치 / 비즈니스 KPI 달성]                          |
+--------------------------------------------------------------------+
```

기존 패러다임은 **"IT는 비용(Cost Center)"**이었고 CIO가 인프라 운영에만 집중했다면, 새로운 패러다임은 **"IT는 가치 창출 엔진(Value Driver)"**으로, **Product Owner + FinOps + Platform Engineering** 역할이 CIO 산하에 통합되는 구조로 진화했다. 799번은 이 진화 과정에서 발생하는 **"Shadow IT, 기술부채, Vendor Lock-in, 책임공백(RACI 미정의)"** 같은 통합 거버넌스 이슈를 어떻게 해결하는지를 묻는다.

- **📢 섹션 요약 비유**: 799번 시험은 "오케스트라 지휘자"와 같다. 바이올린(인프라), 첼로(데이터), 트럼펫(보안), 팀파니(거버넌스) 각각의 악기를 개별적으로 잘 아는 것을 넘어, **하나의 악보(전략) 아래에서 하모니를 만들어내는 통합 시야**를 시험한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 핵심 메커니즘: EDM(평가-지시-모니터) 사이클

```text
+-----------------------------------------------------------------+
|             COBIT 2019 Governance System (40 Objectives)        |
+-----------------------------------------------------------------+
|                                                                  |
|   +----------+    Evaluate    +------------------+              |
|   | Stake-   | ---------------> | Governance System |              |
|   | holders  |                |  (EDM Domain)     |              |
|   | Needs    | <--------------- |  EDM01~EDM05      |              |
|   +----------+    Direct       +--------+---------+              |
|       |                                  |                        |
|       | Strategy                          | Monitor                |
|       v                                  v                        |
|   +----------+                 +------------------+             |
|   | Goals    | --Align---->     | Management        |             |
|   | Cascade  |                 | Objectives        |             |
|   | (13 Enter|                 | (Align/Plan/Build |             |
|   | prise +  |                 |  /Run/Monitor)    |             |
|   | 11 IT)   |                 |  APO/BAI/DSS/MEA  |             |
|   +----------+                 +------------------+              |
|                                                                  |
|   Focus Areas: DevOps, Cybersecurity, Privacy, Cloud, AI,        |
|                Digital Transformation, Risk Management            |
+-----------------------------------------------------------------+
```

**핵심 원리 - 7단계 컴포넌트(7 Components of Governance System)**:
1. **원리·정책·프레임워크(Process Practices)** - 40개 목표별 250+ Process
2. **조직 구조(Organizational Structures)** - CIO, CISO, CDO, DPO 역할
3. **정보 흐름(Information Flows)** - KPI/KGI 보고 체계
4. **인력·역량·기술(People, Skills, Competencies)** - SFIA 8 프레임워크
5. **문화·윤리·행동(Culture, Ethics, Behavior)** - Tone at the Top
6. **서비스·인프라·앱(Services, Infrastructure, Applications)** - CMDB 연동
7. **사람·프로세스·기술(People, Process, Technology Integration)** - RACI 매트릭스

### 2. ISO 38500 IT 거버넌스 6대 원칙 + 5단계 의사결정

```text
+----------------------------------------------------------+
|          ISO/IEC 38500:2015 IT Governance Model          |
+----------------------------------------------------------+
|                                                           |
|   [6 Principles]              [5-Step Model]             |
|   -------------                --------------             |
|   1. Responsibility            1. Evaluate (평가)          |
|   2. Strategy (전략)           2. Direct (지시)            |
|   3. Acquisition (획득)        3. Monitor (모니터)         |
|   4. Performance (성과)        4. Communicate (소통)      |
|   5. Conformance (준수)        5. Assure (보증)           |
|   6. Human Behavior (인간행동)                              |
|                                                           |
|   적용 매핑:                                               |
|   Responsibility -> RACI Matrix -> Board + IT Steering Cmte|
|   Strategy      -> EA(TOGAF) + IT Strategy Map (BSC)      |
|   Acquisition   -> Vendor Mgmt + Procurement Process      |
|   Performance   -> SLA/OLA + KPI Dashboard                 |
|   Conformance   -> ISMS-P + ISO 27001 Audit Trail         |
|   Human Behavior-> Change Mgmt + Training (SFIA)          |
+----------------------------------------------------------+
```

### 3. ITIL 4 Service Value Chain (SVC)

```text
   Opportunity/Demand -+
   Value (가치)        |
                       v
   +------------------------------------------------+
   |  Plan -> Improve -> Engage -> Design & Transition |
   |   |       |          |             |            |
   |   +-------+----------+-------------+            |
   |            v                                     |
   |      Obtain/Build --- Deliver & Support          |
   +------------------------------------------------+
   ^                    ^                              |
   Practices (34개)      Value Stream (VS)             |
   - Incident Mgmt       - 사용자 요구 -> 가치 변환     |
   - Change Enablement   - CI(Configuration Item) 추적 |
   - Service Desk        - CSAT, NPS 측정             |
```

### 4. TOGAF 10 Architecture Development Method (ADM)

```text
   +----------+    +----------+    +----------+    +----------+
   |Preliminary| ->  | A: Vision | ->  | B: BMs   | ->  | C: IS    |
   |  Phase    |    |  (비전)   |    | (비즈)   |    | (정보)   |
   +----------+    +----------+    +----------+    +----------+
        ^                                                |
        |                                                v
   +----------+    +----------+    +----------+    +----------+
   |H: Change | <-  | G: Impl  | <-  | F: Migr  | <-  | D: Tech  |
   |  Mgmt    |    | (구현)   |    | (전이)   |    | (기술)   |
   +----------+    +----------+    +----------+    +----------+
                                                       |
                                                       v
                                              +----------+
                                              | E: Opps  |
                                              | (기회)   |
                                              +----------+

   ※ 4 Architecture Domains: BDAT (Business, Data, Application, Technology)
   ※ ADM 사이클 + Requirements Management (중앙 허브) + Architecture Repository
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance Board (이사회/ITSC)** | 의사결정·감독 | ISO 38500 Responsibility, RACI 매트릭스, 분기별 운영위원회 |
| **CIO / CDO / CISO** | 3대 CXO 역할 분리 | 거버넌스·데이터·보안 3분리, Three Lines of Defense(1LoD: 사업, 2LoD: 리스크/컴플, 3LoD: 내부감사) |
| **EA(Enterprise Architecture)** | To-Be 모델링 | TOGAF 10 ADM 8단계 + ArchiMate 3.2 표기 + Zachman 6x6 매트릭스 |
| **PMO(Project Mgmt Office)** | 프로젝트 포트폴리오 관리 | P3O(Portfolio/Programme/Project Office), PRINCE2 + MSP, Earned Value Mgmt(EVM: CPI, SPI) |
| **Service Operation Center** | IT 운영·모니터링 | ITIL 4 34 Practices, AIOps, Observability(메트릭·로그·트레이스), SRE Error Budget |
| **정보보안 조직** | 사이버 회복력 | ISO 27001:2022 + NIST CSF 2.0 + Zero Trust Architecture(SDP/MFA/Microsegment) |
| **데이터 거버넌스** | 데이터 자산화 | DAMA-DMBOK 2.0 11개 지식영역 + Data Lineage + Data Quality (정확성·완전성·일관성·적시성) |
| **Risk & Compliance** | 컴플라이언스 통합 | GRC(Governance·Risk·Compliance) 플랫폼 + ISO 31000 + COBIT 2019 Risk Focus Area |

**핵심 산출 공식 (기술사형 정량 판단)**:

```
+-------------------------------------------------------------+
|  ① IT 투자 평가 4대 지표                                       |
|     NPV = Σ [CFₜ / (1+r)ᵗ] - 초기투자                       |
|     IRR: NPV=0 이 되는 r                                      |
|     ROI = (이익 - 비용) / 비용 × 100                          |
|     EVA = NOPAT - (WACC × 투자총액)                            |
|                                                              |
|  ② TCO (Total Cost of Ownership) 5-Layer                    |
|     TCO = HW + SW + 인건비 + 교육 + 운영(전력·냉각·공간)        |
|         + 다운타임 손실 + 기회비용                              |
|                                                              |
|  ③ EVM (Earned Value Management)                              |
|     CV(원가편차) = EV - AC                                    |
|     SV(일정편차) = EV - PV                                    |
|     CPI(원가성과) = EV / AC  -> ≥1 양호                         |
|     SPI(일정성과) = EV / PV  -> ≥1 양호                         |
|                                                              |
|  ④ 클라우드
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 799 / 800

<- **이전**: [798. IT 경영 관리 핵심 토픽 798번 시험 요약](/studynote/12_it_management/05_security_compliance/798_it_management_core_topic_798_exam_summary/)
**다음**: [800. 800. IT/SW 전략 비즈니스 통합 모델 최종 키워드 모음 완료.](/studynote/12_it_management/05_security_compliance/800_it_sw/) ->

---
