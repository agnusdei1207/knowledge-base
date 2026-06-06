---
title: "IT Management Core Topic 688 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019(거버넌스·목표 계층)**, **ITIL 4(SVS·34개 실천)** , **ISO/IEC 20000(서비스경영체계)**, **ISO 27001(정보보안경영체계)** 4대 프레임워크를 **Balanced Scorecard(BSC)** 와 **TOGAF ADM** 으로 통합 운영하여 비즈니스 가치(ROI/NPV/ROA)를 극대화하는 경영 체계이다.
> 2. **가치**: McKinsey(2024) 기준 디지털 전환成熟 기업은 **EBITDA 마진 26% 향상**, **Time-to-Market 40% 단축**, **IT 운영비용 20~30% 절감** 효과를 달성하며, Gartner(2025) 보고서에서는 통합 거버넌스 도입 기업의 IT 프로젝트 성공률이 **28% -> 65%** 로 상승한다.
> 3. **판단 포인트**: 기술사적 의사결정 핵심은 **①** 거버넌스(Decision/Diff./Monitoring)와 관리(Plan/Build/Run/Improve)의 **RACI 분리**, **②** CapEx/OpEx/ITaaS(클라우드) 재무 모델 선택, **③** Zero-Trust × DevSecOps × AIOps 융합 시 **CSF(KPI 17~23개)** 와 **KGI(4~6개)** 의 인과 매핑 정합성이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사는 1977년 신설 이래 **정보시스템의 기획부터 폐기까지 전生命周期(Lifecycle)** 을 총괄하는 국가공인 최고 자격이다. 2024년 제115회 시험부터 CBT 전환 및 NCS 기반 출제 강화됨에 따라, 단순 암기형이 아닌 **사례 기반(6~8페이지) 서술형** 문제에서 "**왜 이 프레임워크를 선택했는가?**"의 trade-off 논리를 요구한다.

기존(Pre-2010) IT 부서는 **비용센터(Cost Center)** 로 인식되어 **"요청 시 개발·유지보수"** 의 수동적 운영이 주를 이루었다. 그러나 ④차 산업혁명(AI·클라우드·IoT·블록체인) 시대에 IT는 **전략적 동인(Strategic Enabler)** 으로 격상되었고, 이에 따라 **①** IT 투자 정당화(Justification), **②** 위험 통제(Risk Control), **③** 서비스 품질(SLA), **④** 규제 준수(Compliance)를 동시에 만족시키는 **통합 IT 경영 체계**가 필수 불가결해졌다.

특히 2024년 기준 국내 대기업·공공기관의 **60~70%** 가 COBIT·ITIL·ISO 20000을 부분 도입했으나, **실질 통합률은 15% 미만** (한국정보화진흥원, 2024)이라는 진단이 있어, **"도입이 아닌 통합 거버넌스"** 가 본 토픽의 핵심 쟁점이다.

```text
+------------------------------------------------------------------+
|            IT 경영 관리 4대 프레임워크 통합 참조 모델            |
|                                                                  |
|  +--------------+   +--------------+   +--------------+         |
|  |   COBIT 2019 |   |   ITIL 4     |   | ISO/IEC 20000|         |
|  |  (거버넌스)  |   |  (서비스)    |   |   (인증)     |         |
|  |  40 Governance|   |  SVS+34      |   |   10 clauses |         |
|  |  & Mgmt Obj. |   |  Practices   |   |              |         |
|  +------+-------+   +------+-------+   +------+-------+         |
|         |                  |                  |                  |
|         +---------+--------+--------+---------+                  |
|                   |                 |                            |
|            +------v------+   +------v------+                     |
|            | Balanced    |   |  TOGAF ADM  |                     |
|            | Scorecard   |   | (EA架构)    |                     |
|            | (BSC 4관점) |   |  Phase A~H  |                     |
|            +------+------+   +------+------+                     |
|                   |                 |                            |
|            +------v-----------------v----------+                 |
|            |      ISO/IEC 27001 (ISMS)        |                 |
|            |    Annex A 93 통제 항목          |                 |
|            +--------------+-------------------+                 |
|                           |                                     |
|                  +--------v---------+                           |
|                  |   비즈니스 가치  |                           |
|                  | (ROI/NPV/ROA)    |                           |
|                  +------------------+                           |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차 운전**과 같다. **COBIT**은 운전면허·교통법규(거버넌스), **ITIL**은 정비소·주유(서비스 운영), **ISO 20000**은 정기검사 합격증(인증), **ISO 27001**은 블랙박스·에어백(보안), **TOGAF**는 네비게이션(아키텍처), **BSC**는 계기판(KPI)이다. 이 중 하나라도 없으면 사고가 나거나 목적지에 도달하지 못한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 6원칙 거버넌스 시스템

COBIT 2019는 ISACA에서 2018년发布的 핵심 거버넌스 프레임워크로, **40개 Governance/Management Objective** 와 **6개 Governance System Principle**, **3개 Governance Framework Principle**로 구성된다. 핵심은 **EDM(Evaluate-Direct-Monitor)** 사이클과 **Plan-Build-Run-Improve**의 명확한 분리이다.

```text
+------------------------------------------------------------------+
|            COBIT 2019 40개 목표 계층 (Cascading Goals)          |
|                                                                  |
|  +--------------------------------------------------------+    |
|  |  Stakeholder Drivers (13개)                            |    |
|  |  - Benefit Realisation  - Risk Optimisation             |    |
|  |  - Resource Optimisation                                |    |
|  +-------------------------+------------------------------+    |
|                            v                                    |
|  +--------------------------------------------------------+    |
|  |  Enterprise Goals (13개)                               |    |
|  |  EG01 포트폴리오 / EG05 재무 / EG08 최적화 / EG13 보안  |    |
|  +-------------------------+------------------------------+    |
|                            v                                    |
|  +--------------------------------------------------------+    |
|  |  Alignment Goals (13개)                                |    |
|  |  AG01 IT Framework / AG04 Quality / AG09 Cost / AG15 보안|   |
|  +-------------------------+------------------------------+    |
|                            v                                    |
|  +--------------------------------------------------------+    |
|  |  Component Goals  -- Components (7가지)                |    |
|  |  Process / Structure / Information / People/Skills/    |    |
|  |  Culture/Ethics / Services/Infrastructure/Apps         |    |
|  +--------------------------------------------------------+    |
+------------------------------------------------------------------+
```

### 2. ITIL 4 Service Value System (SVS)

ITIL 4는 2019년 AXELOS에서 발표된 차세대 프레임워크로, **SVS(Service Value System)** 중심으로 **34개 Best Practice** 를 **SVC(Service Value Chain)** 6단계(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)로 재구성했다. **4가지 차원(Organization & People / Information & Technology / Partners & Suppliers / Value Streams & Processes)** 과 **7가지 guiding principle** 이 핵심이다.

### 3. ISO/IEC 20000-1:2018 서비스경영체계

**10개 clause** (Clause 4: 조직맥락, Clause 5: 리더십, Clause 6: 기획, Clause 7: 지원, Clause 8: 운영, Clause 9: 성과평가, Clause 10: 개선) 으로 구성된 인증 표준으로, **PDCA + Risk-Based Thinking** 을 적용한다. ITIL과 1:1 매핑되지만 **인증 목적** 이라는 점에서 차이가 있다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스)** | 의사결정·지시·감독 | 이사회/IT거버넌스위원회 -> **5 의사결정(D1~D5)**: Benefit Delivery, Risk Optimization, Resource Optimization, Stakeholder Transparency, Compliance |
| **Plan(계획)** | 전략·포트폴리오 기획 | **전략 매핑**: BSC 4관점(재무/고객/내부/학습성장) -> IT 전략맵 -> **IT 투자 분류**: Run(60~70%) / Grow(15~25%) / Transform(5~15%) — Gartner IT Spend Benchmark |
| **Build(구축)** | 솔루션·아키텍처 개발 | **TOGAF ADM Phase A~H** + **Agile@Scale (SAFe 6.0)** + **DevSecOps 파이프라인**(SAST/DAST/SCA) |
| **Run(운영)** | 서비스 전달·지원 | **ITIL 4 SVC** 6활동 + **AIOps**(Anomaly Detection, Predictive Maintenance) + **SLA 99.9~99.99%** + **Incident MTTR < 30분** |
| **Improve(개선)** | 지속적 혁신 | **CSI(Continual Service Improvement)** + **Lean Six Sigma DMAIC** + **Kaizen** + **KPI 17~23개** |

### 4. 핵심 알고리즘·산식

**IT ROI 계산식(기술사 필수 암기)**
```
IT ROI = (Total Benefit - Total Cost) / Total Cost × 100
NPV   = Σ [Bt / (1+r)^t] - I0  (r=할인율, 통상 WACC+α)
TCO   = Direct + Indirect(인건비·교육·장애) + Risk Cost(가용성 손실)
ROA   = (Net Income / Total IT Asset) × 100
```

**IT 포트폴리오 균형도(Balance Score)**
- Run-the-Business(60~70%) / Grow-the-Business(15~25%) / Transform-the-Business(5~15%)
- Gartner 권고 비율: 안정기 기준 70/20/10, 변혁기 50/30/20

- **📢 섹션 요약 비유**: COBIT의 EDM은 **회사 이사회**, Plan-Build-Run은 **임원·R&D·공장장**, Improve는 **품질관리(QC)팀**이다. 자동차 회사에서 이사회가 "전기차 만들라"고 지시(EDM)하면, R&D가 설계(Build), 공장이 양산(Run), 기획이 시장 분석(Plan), QC팀이 회고(Improve)한다. 각자 역할이 섞이면 "이사회가 직접 용접"하는 사고가 발생한다.

---

## Ⅲ. 비교 및 연결

### 1. 4대 프레임워크 상세 비교

| 구분 | **COBIT 2019** | **ITIL 4 (2019)** | **ISO/IEC 20000-1:2018** | **ISO/IEC 27001:2022** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스·컴플라이언스 | 서비스 운영·가치 창출 | 서비스경영 인증 | 정보보안 경영체계(ISMS) |
| **구조** | 40 GO + EDM + 컴포넌트 | SVS + SVC 6활동 + 34 BP | 10 Clause + Annex A | 10 Clause + Annex A 93 통제 |
| **인증 가능** | ❌(COBIT 2019 Design/Implement 인증) | ❌(PeopleCert 자격증만) | ✅ | ✅ |
| **핵심 사이클** | EDM / Plan-Build-Run-Improve | SVC 6활동 (Plan->Improve) | PDCA + Risk | PDCA + Statement of Applicability |
| **적합 조직** | 대기업·공공·금융 | 서비스 중심 MSP/IDC | SI·MSP 인증 필요기업 | 전 산업 (정보보안 의무화) |
| **측정 지표** | CSF/KPI 17~23개 | KPI 17개 + Practice Metric | SLA/OLA/UC 100% 가시화 | KRI 25개 + 보안 KPI |
| **강점** | Stakeholder-Value 매핑 | Agile/Cloud 친화 | 글로벌 인증 브랜드 | 보안 통제 항목 표준화 |
| **약점** | 구현 복잡도·비용 | 인증 부재 | 운영 부담 | 기술 변화 대응 지연 |
| **2025 트렌드** | COBIT 2019 + NIST CSF 매핑 | ITIL 4 + AIOps + Green IT | ISO 20000:2025 개정(예정) | ISO 27001:2022 + DORA·AI Act |

### 2. EA·프로젝트 관리·보안 프레임워크 연결

- **TOGAF 10 (2022)**: Architecture Development Method(ADM) Phase A~H + **Architecture Content Framework** + **Capability Framework** + **Reference Model(TRM/III-RM)** 로 EA 4영역(BDAT: Business/Data/Application/Technology) 관리
- **PMBOK 7 (2021)**: 12 Principle + **Domain(8개)**: Stakeholder/Team/Development Planning/Project Work/Delivery/Measurement/Uncertainty/Complexity
- **Agile & SAFe 6.0**: 4 Core Value + **7 Core Competency** + 4 Configurations(Essential/Large Solution/Portfolio/Full)
- **DevSecOps**: **CALMS(Culture/Automation/Lean/Measurement/Sharing)** + **DORA 4 Metric**(Deployment Freq./Lead Time/CFR/MTTR)
- **Zero Trust (NIST SP 800-207)**: "Never Trust, Always Verify" + **3대 기둥**: Identity/Device/Network + **Policy Engine/Administrator**

### 3. BSC 4관점 KPI 매핑 예시

| BSC 관점 | IT 전략 목표 | KPI 예시 | 측정 주기 |
| :--- | :--- | :--- | :--- |
| **재무** | IT 비용 최적화 | IT Cost/Revenue(%), TCO 절감률 | 분기 |
| **고객** | 서비스 만족도 | CSAT
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 688 / 800

<- **이전**: [687. IT 경영 관리 핵심 토픽 687번 시험 요약](/studynote/12_it_management/05_security_compliance/687_it_management_core_topic_687_exam_summary/)
**다음**: [689. IT 경영 관리 핵심 토픽 689번 시험 요약](/studynote/12_it_management/05_security_compliance/689_it_management_core_topic_689_exam_summary/) ->

---
