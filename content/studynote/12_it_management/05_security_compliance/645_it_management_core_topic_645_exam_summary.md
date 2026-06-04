---
title: "645. IT 경영 관리 핵심 토픽 645번 시험 요약 (IT Management Core Topic 645 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 📘 645. IT 경영 관리 핵심 토픽 645번 시험 요약

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사 645번은 IT 거버넌스(COBIT 2019, ISO 38500), ITSM(ITIL 4), 정보보안 거버넌스(ISO 27001/27005), EA(TOGAF, FEAF), 프로젝트 관리(PMBOK 7, PRINCE2) 및 디지털 전환 전략을 종합한 IT 경영관리 통합 체계의 설계·운영·평가 역량을 평가하는 시험이다.
> 2. **가치**: 정량적 가치로는 IT 투자 ROI 20~40% 개선, IT 운영 비용 15~30% 절감, 보안 사고 대응시간 60% 단축, 정성적 가치로는 경영진-현업-IT 간 정렬(Strategic Alignment) 확보, 의사결정 투명성, 리스크 가시화를 통한 사업 연속성(BCP) 실현이 가능하다.
> 3. **판단 포인트**: 코어权衡은 (a) 중앙집중형 vs 분산형 거버넌스 (Federal 모델), (b) 거버넌스 표준 간 중복(예: COBIT의 EDM/DSS vs ITIL의 Service Value Chain) 통합 설계, (c) Agile-DevOps 환경에서의 통제-속도(Governance-Speed) 균형, (d) KPI/KRI 설계 시 Leading vs Lagging 지표의 비중 결정이다.

---

## Ⅰ. 개요 및 필요성

한국 정보관리기술사 시험은 1999년 정보화촉진기본법 제정 이후, 국가·공공·금융·제조 등 전 산업의 디지털 전환(DX, Digital Transformation) 과정에서 발생하는 IT 경영 이슈를 다룬다. 645번 토픽은 특히 **IT를 "비용"이 아닌 "사업 전략적 자산"으로 관리**하기 위한 통합 프레임워크 적용 역량을 시험한다. 과거(2000년대)에는 정보화 사업의 감리·타당성 분석 중심이었다면, 현재(2024~2026)는 클라우드·AI·제로트러스트·ESG·데이터3법 환경에서의 **지속 가능한 IT 거버넌스 모델링**이 핵심이다.

특히 2024년 9월 시행된 「디지털정부법」 개정으로 공공부문 EA·데이터·보안 거버넌스 통합 의무화가 법제화되었고, 2025년 「AI 기본법」 시행으로 AI 거버넌스 체계를 기존 IT 거버넌스에 통합해야 하는 과제가 대두되었다. 따라서 645번 시험은 단순 암기가 아닌 **상황별 프레임워크 선택·적용·평가(C-E-A: Choose-Evaluate-Apply) 능력**을 측정한다.

```text
+--------------------------------------------------------------------+
|            IT 경영 관리 645번 통합 도메인 맵                        |
|                                                                    |
|  +----------+    +----------+    +----------+    +----------+    |
|  |  전략    |    |  거버넌스|    |  운영    |    |  평가    |    |
|  | Strategy |---->|Governance|---->|Operation |---->|Evaluation|    |
|  +----------+    +----------+    +----------+    +----------+    |
|       |              |              |              |             |
|       v              v              v              v             |
|  +---------+   +----------+   +----------+   +----------+      |
|  |ISP/EA   |   |COBIT2019 |   |ITIL 4    |   |감리/ISAC |      |
|  |BPR/BPM  |   |ISO 38500 |   |ISO 20000 |   |BS 15000  |      |
|  |BA Planning| |ISO 27001 |   |DevOps    |   |KPI/KRI   |      |
|  |DX 전략  |   |ISO 27005 |   |SRE/AIOps |   |Balanced  |      |
|  |         |   |NIST CSF  |   |FinOps    |   |Scorecard |      |
|  +---------+   +----------+   +----------+   +----------+      |
|       |              |              |              |             |
|       +--------------+------+-------+--------------+             |
|                              v                                    |
|                  +----------------------+                         |
|                  |  거버넌스 통합 체계   |                         |
|                  | Integrated Governance|                         |
|                  |   Framework (IGF)    |                         |
|                  +----------------------+                         |
+--------------------------------------------------------------------+
```

**기존 패러다임 대비 변화**:
- **1990~2000년대**: 데이터 중심 관리(데이터 모델링, DBMS) -> 시스템 단위 관리
- **2010년대**: 프로세스·서비스 중심(ITIL v3, COBIT 5) -> BS(Business Strategy) 정렬
- **2020년대**: 가치·생태계 중심(ITIL 4, COBIT 2019, SVC) -> 클라우드·AI·제로트러스트 통합

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 도시계획**과 같다. 개별 건물(시스템) 하나하나의 설계뿐 아니라, 상하수도(데이터 흐름), 도로(네트워크), 소방서(보안), 시청(거버넌스), 교통규칙(SLA)까지 통합 설계해야 비로소 시민(사용자)이 안전하고 편리한 삶을 영위할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

645번 시험의 핵심은 **3대 거버넌스 프레임워크(COBIT, ITIL, ISO 27001)** 의 통합 적용이다. 이를 4계층 아키텍처로 분해한다.

```text
        +--------------------------------------------+
        |    Layer 4: 전략·정렬 (Strategy/Aligment) |
        |  ◦ ISO 38500 (6원칙: 책임·전략·취득·      |
        |    성과·규칙·인간행위)                       |
        |  ◦ Balanced Scorecard 4관점 (재무·고객·    |
        |    내부프로세스·학습성장)                     |
        |  ◦ Information Strategy Planning (ISP)    |
        +----------------+---------------------------+
                         v
        +--------------------------------------------+
        |    Layer 3: 거버넌스·평가 (Evaluate/Direct)|
        |  ◦ COBIT 2019 40 Governance/Management Obj|
        |  ◦ EDM 05 domains: Evaluate, Direct,      |
        |    Monitor (EDM01~EDM05)                   |
        |  ◦ Capability Level (0~5): PAM/CMMI       |
        +----------------+---------------------------+
                         v
        +--------------------------------------------+
        |    Layer 2: 운영·관리 (Operate)             |
        |  ◦ ITIL 4 Service Value System (SVS)       |
        |  ◦ 34 Practices (구 26 Process)            |
        |  ◦ Service Value Chain (Plan-Engage-       |
        |    Design-Obtain-Build-Deliver-Support)    |
        |  ◦ ISO 20000-1:2018 10 clause             |
        +----------------+---------------------------+
                         v
        +--------------------------------------------+
        |    Layer 1: 기반·통제 (Foundation/Control)  |
        |  ◦ ISO 27001:2022 (Annex A 93 controls)   |
        |  ◦ NIST CSF 2.0 (Govern-Identify-Protect- |
        |    Detect-Respond-Recover)                  |
        |  ◦ ISO 27005 Risk Management (Context-     |
        |    Assessment-Treatment-Monitoring)        |
        |  ◦ 제로트러스트(ZTA) 5대 원칙 (NIST SP800) |
        +--------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스·관리 목표 체계 | 40개 Governance/Management Objective, 7개 컴포넌트(원리/정책/프로세스/조직/정보/인력/문화/기술), 11개 디자인팩터(전략, 목표, 리스크, 이슈, 위협, 준수요건, 역할, IT 이슈, 기술 도입, 기술 배치 방법, 조직 규모)로 7가지 레퍼런스 설계안 중 선택 |
| **ITIL 4** | IT 서비스 관리 운영 체계 | Service Value System(SVS) 내 5대 핵심: Service Value Chain(7단계), 7 Guiding Principles(Focus on value, Start where you are, Progress iteratively, etc.), 34 Practices(General, Service, Technical Management), 4-Dimension Model(Organizations/People, Information/Technology, Partners/Suppliers, Value Streams/Processes) |
| **ISO 27001:2022** | 정보보안 관리 체계(ISMS) | Plan-Do-Check-Act(PDCA) 사이클, Clause 4~10 + Annex A 93개 통제항목(4개 영역: 5(37)·6(8)·7(14)·8(34)), Statement of Applicability(SoA) 작성, 리스크 평가 방법론(ISO 27005 연계) |
| **ISO 38500:2015** | IT 거버넌스 국제표준 | 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior), Evaluate-Direct-Monitor 3단계 사이클, 이사회-경영진-IT조직 간 역할 분리 |
| **TOGAF 10** | EA 개발 방법론 | ADM(Architecture Development Method) 8+1 Phase: Preliminary-A~H-Requirements Management, ADM Cycle로 반복적 EA 수립, Architecture Content Framework(메타모델·산출물), Capability Framework(ACMP 인증) |
| **PMBOK 7** | 프로젝트 관리 표준 | 12 Project Management Principles + 8 Performance Domains(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty), Tailoring 중시, Predictive/Agile/Hybrid |
| **ISO 31000** | 리스크 관리 프레임워크 | 7원칙, 6단계 프로세스(Communication·Context·Assessment·Treatment·Monitoring·Recording), 5×5 리스크 매트릭스 |

**핵심 알고리즘/산식**:
1. **COBIT Capability Level 측정**: PAM(Process Assessment Model) 기반 0(Incomplete)~5(Optimizing) 레벨링, 6개 프로세스 속성(PA1.1~PA5.2, PA6.1)별 가중치 적용, **NPLF(N=No, P=Partial, L=Largely, F=Fully)** 4점 척도
2. **리스크 산정식**: $Risk = Likelihood \times Impact \times Vulnerability$ (ISO 27005), 정성평가 5단계(매우 낮음~매우 높음) 또는 정량평가(ALE = SLE × ARO, Annual Loss Expectancy)
3. **ITIL 4 가치 흐름**: $Value = Utility + Warranty \times Importance$, Utility(적합성/성능/용량)와 Warranty(가용성/지속성/보안/준수성)의 결합
4. **KPI 산정식**: $CSAT = \frac{\sum 만족 응답}{전체 응답} \times 100$, $FCR(First Call Resolution) = \frac{1회 해결 건}{전체 인시던트} \times 100$
5. **투자 회수**: $NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t} - Initial\ Investment$, $IRR$ 기준 의사결정, $Payback\ Period = \frac{Initial\ Investment}{Annual\ Cash\ Flow}$

- **📢 섹션 요약 비유**: 거버넌스 프레임워크 3종(COBIT·ITIL·ISO 27001)은 마치 **건물의 설계도(COBIT), 운영 매뉴얼(ITIL), 보안 체크리스트(ISO 27001)** 의 삼권분립과 같다. 같은 건물을 세 가지 시각으로 바라봄으로써 사각지대(blind spot)를 제거한다.

---

## Ⅲ. 비교 및 연결

정보관리기술사 시험에서 빈출되는 비교 영역을 다룬다.

| 구분 | COBIT 2019 | ITIL 4 | ISO 27001:2022 |
| :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 목표 | IT 서비스 관리·운영 | 정보보안 관리 체계 |
| **관점** | What(무엇을)·Why(왜) | How(어떻게) | How(어떻게)·Risk-based |
| **대상** | 이사회·경영진·CIO·감사인 | IT 운영자·서비스 매니저 | CISO·보안팀·전 임직원 |
| **측정 단위** | Capability/Maturity Level(0~5) | Maturity Level(0~5)·SL KPI | SoA 준수율·리스크 잔여 수준 |
| **프로세스 수** | 40 Governance/Management Obj | 34 Practices | Annex A 93 통제항목 |
| **인증** | COBIT 2019 Foundation/Design/Implement | ITIL 4 Foundation/MP/SL | ISO 27001 Lead Auditor/Implementer |
| **한국 적용** | 정보시스템 감리(국가·공공) | 대기업·공공 SI | ISMS-P(한국형), PIMS |

| 구분 | PMBOK 7 | PRINCE2 | ISO 21500 |
| :--- | :--- | :--- | :--- |
| **철학** | 원칙·원리(Principle) 기반 | 7원칙·7테마 | 10 Knowledge Area |
| **방법론** | Predictive·Agile·Hybrid | 7 Processes·7 Themes | 39 Subject Element |
| **인증** | PMP/CAPM | PRINCE2 Foundation/Practitioner | ISO 21500 Lead |
| **강점** | 유연성·원칙 중심 | 통제·단계별 강제성 | 글로벌 표준 |

| 구분 | NIST CSF 2.0 | ISO 27001:2022 | 제로트러스트(ZTA) |
| :--- | :--- | :--- | :--- |
| **구조** | Govern-Identify-Protect-Detect-Respond-Recover (6 Function) | PDCA + Annex A | 5 원칙(리소스·통신·액세스·동적정책·모니터링) |
| **강제성** | 자발적(미국 표준) | 인증 기반 | NIST SP 800-207(자발적, 美 연방의무) |
| **적용** | 산업 전반 | 모든 산업 | 클라우드·원격근무 환경 |
| **연계** | 2024년 2.0 발표, Govern 신설 | CSF 매핑 가이드 제공
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 645 / 800

<- **이전**: [644. IT 경영 관리 핵심 토픽 644번 시험 요약](/studynote/12_it_management/05_security_compliance/644_it_management_core_topic_644_exam_summary/)
**다음**: [646. IT 경영 관리 핵심 토픽 646번 시험 요약](/studynote/12_it_management/05_security_compliance/646_it_management_core_topic_646_exam_summary/) ->

---
