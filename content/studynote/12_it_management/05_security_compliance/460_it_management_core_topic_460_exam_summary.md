---
title: "460. IT 경영 관리 핵심 토픽 460번 시험 요약 (IT Management Core Topic 460 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽(460번)은 COBIT 2019·ITIL 4·ISO 27001·ISO 38500·BSC·PMBOK 7th·TOGAF 등 글로벌 거버넌스 프레임워크를 Value Creation(가치창출)·Risk Optimization(위험 최적화)·Resource Optimization(자원 최적화)의 3대 Governance Objective로 통합·조율하여, 기업의 전략-전술-운영(IT Strategy->Portfolio->Program->Project->Operation)을 End-to-End로 정렬하는 **IT 거버넌스-관리-운영 통합 체계의 설계 및 평가 능력**을 평가한다.
> 2. **가치**: 정량적 효과로 IT 투자 대비 ROI 평균 25~40% 개선, IT 인시던트 MTTR 60% 단축, 정보보호 사고 70% 감소, IT 비용 대비 비즈니스 가치 실현률(Business Value Realization) 30% 이상 향상; 정성적 효과로 CEO-CIO-IT-Business 간 **Strategy Alignment(전략적 정렬)**, Audit Readiness(감사 대응력), Regulatory Compliance(규제 준수) 확보.
> 3. **판단 포인트**: ① Tailoring(맞춤형 적용) – 표준 프레임워크를 무비판적으로 도입하지 말고 조직의 Size/Complexity/Risk Profile/Regulatory Environment에 맞춰 **Design Factor 11개(COBIT 2019)** 기반으로 커스터마이징 ② Agile vs Plan-Driven 균형 – VUCA 환경에서는 **Bimodal IT**(Mode 1: Predictable / Mode 2: Exploratory) 채택 ③ 거버넌스 vs 관리(Governance vs Management) 분리 – Decision-Making 구조(EDM: Evaluate-Direct-Monitor)와 운영 실행 구조(PBRM: Plan-Build-Run-Monitor)의 명확한 역할 경계 ④ Compliance-First vs Value-First 균형.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management)는 단순한 시스템 운영을 넘어 **기업의 미션·비전·전략을 IT 자원·역량·서비스로 변환**하고, 그 결과를 **측정·평가·개선**하기 위한 포괄적 관리 체계이다. 4차 산업혁명(AI, Cloud, BigData, IoT, Blockchain) 시대에 IT는 **Cost Center(비용 센터)** 에서 **Strategic Asset(전략 자산)** 으로, **Back-office Tool** 에서 **Business Differentiator(경쟁우위 차별화 요소)** 로 그 위상이 근본적으로 재정의되었다.

**배경 및 등장 배경**:
- 2000년대 초 IT 거버넌스 위기(Enron, WorldCom 등 대규모 IT 통제 실패)로 인해 IT에 대한 **독립적 거버넌스 체계** 필요성 대두 -> 2008년 ISO/IEC 38500 (Corporate governance of IT) 국제표준 제정
- COBIT(Control Objectives for Information and Related Technologies)이 ISACA 주도로 1996년 v1.0 출시 이후 v3.0(2000)->v4.0(2005)->v4.1(2007)->v5.0(2012)->**2019(현행)** 으로 진화하며 **프레임워크 -> 프로세스 참조모델 -> 거버넌스/관리 통합체계**로 패러다임 전환
- ITIL(Information Technology Infrastructure Library)이 1989년 영국 OGC 발간, v1(1989)->v2(2000)->v3(2007)->**v3 Refresh(2011)->ITIL 4(2019)** 으로 발전, **프로세스 중심 -> 서비스 가치사슬(SVC) -> Value Stream 중심**으로 재구성
- 정보보호의 필요성: 개인정보보호법(2011), 정보통신망법, ISMS-P(2020년 ISMS+개인정보보호 통합) 인증제 도입으로 보안 거버넌스 의무화

**기술적 도전 과제**:
- **Shadow IT(샤도우 IT)** : 승인되지 않은 SaaS/클라우드 사용 급증(Gartner 보고: 2027년 기업 IT 지출의 75%가 CEO/사업부서 직결)
- **Talent Gap**: IT 전문가 부족과 역량 갭(Post-COVID 이후 40% 이상)
- **Cyber Threat Sophistication**: 랜섬웨어, 제로데이, 공급망 공격(Supply Chain Attack – SolarWinds, Kaseya 사건)
- **기술 부채(Technical Debt)**: 레거시 시스템 유지보수 비용이 전체 IT 예산의 60% 이상 점유
- **규제 복잡성**: GDPR, HIPAA, PCI-DSS, ESG 공시, AI 기본법(2024년 시행), DORA(欧盟 디지털 운영 복원력법)

**왜 IT 경영 관리가 필수인가 (Old vs New Paradigm)**:

| 구분 | Old Paradigm (Pre-2000s) | New Paradigm (2020s~) |
|------|-------------------------|----------------------|
| IT 역할 | Cost Center, Back-office | Value Driver, Business Enabler |
| 관리 방식 | Technology-driven, Silo | Business-driven, E2E Value Chain |
| 거버넌스 | Project 중심, 단발성 | Portfolio 중심, 지속적(Continuous) |
| 측정 지표 | Uptime, Throughput | NPS, Customer Journey, Business Outcome |
| 위험 관리 | Reactive (사후 대응) | Proactive / Predictive (예측) |
| 아키텍처 | Monolithic, On-premise | Cloud-native, Composable, API-first |
| 문화 | Command & Control | Agile, DevOps, SRE, Data-driven |

```text
+----------------------------------------------------------------------+
|         IT 경영 관리의 3대 거버넌스 목표 (COBIT 2019)                 |
|                                                                      |
|   +-----------------+   +-----------------+   +-----------------+  |
|   |  Benefit         |   |  Risk           |   |  Resource        |  |
|   |  Realization     |   |  Optimization   |   |  Optimization    |  |
|   |  (가치 실현)     |   |  (위험 최적화)  |   |  (자원 최적화)   |  |
|   +--------+--------+   +--------+--------+   +--------+--------+  |
|            |                     |                      |            |
|            +---------------------+----------------------+            |
|                                  |                                   |
|                                  v                                   |
|                  +------------------------------+                    |
|                  |   Enterprise Goals           |                    |
|                  |   (비즈니스 목표 13개)        |                    |
|                  +--------------+---------------+                    |
|                                 |                                    |
|                  +--------------+---------------+                    |
|                  v                              v                    |
|   +--------------------------+  +--------------------------+        |
|   |   Alignment Goal         |  |  Enablement Goal          |        |
|   |   (IT-비즈니스 정렬 5개) |  |  (IT 역량 강화 7개)       |        |
|   +--------------------------+  +--------------------------+        |
|                                                                      |
|  +-------------------------------------------------------------+    |
|  |  Cascade (연쇄 전파): Stakeholder Needs -> Enterprise Goals  |    |
|  |   -> Alignment Goals -> Management Objectives -> Process     |    |
|  |   -> Activities -> Metrics (6단계 Goal Cascade)              |    |
|  +-------------------------------------------------------------+    |
+----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같다. 다양한 악기(애플리케이션, 인프라, 데이터, 인력)가 각자의 음색(역량)을 가지고 연주하지만, 지휘자(거버넌스)가 없으면 불협화음(실패 프로젝트·보안사고·예산 낭비)이 발생한다. COBIT은 악보(표준), ITIL은 연주 매뉴얼(서비스 운영), ISO 27001은 음질 점검 기준(보안), BSC는 객석의 청취 평가(KPI)를 제공한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **3-Layer Governance-Management-Operation Model** 로 표현된다. ISO 38500은 **Governance(거버넌스)** 와 **Management(관리)** 를 엄격히 구분한다: 거버넌스는 **"무엇(What)과 왜(Why)"** 에 대한 의사결정, 관리는 **"어떻게(How)"** 에 대한 실행을 담당한다.

```text
+-------------------------------------------------------------------------+
|                    IT 거버넌스 3계층 아키텍처                             |
+-------------------------------------------------------------------------+
|                                                                         |
|  Layer 1: GOVERNANCE (거버넌스 계층)                                    |
|  +-------------------------------------------------------------------+ |
|  |  Board of Directors / IT Steering Committee (ISC) / CxO          | |
|  |  --------------------------------------------------------------  | |
|  |  책임: 책임(RESPONSIBILITY), 전략(STRATEGY), 정책(POLICY)        | |
|  |  원칙 6가지 (ISO 38500):                                          | |
|  |   1. Responsibility (책임성)                                      | |
|  |   2. Strategy (전략성)                                            | |
|  |   3. Acquisition (취득)                                           | |
|  |   4. Performance (성과)                                           | |
|  |   5. Conformance (준수)                                           | |
|  |   6. Human Behavior (인간행동)                                    | |
|  |  ISO/IEC 38500:2015 — "Direct, Monitor, Evaluate" 3-Activity Model|
|  +---------------------------------+---------------------------------+ |
|                                    |                                   |
|                                    | (위임, 정책, 예산, Risk Appetite) |
|                                    v                                   |
|  Layer 2: MANAGEMENT (관리 계층) - COBIT 2019 Core Model               |
|  +-------------------------------------------------------------------+ |
|  |  5개 Domain | 40개 Governance/Management Objective                | |
|  |  ----------+----------------------------------------------------  | |
|  |  EDM(5)    | Evaluate, Direct and Monitor (거버넌스)              | |
|  |  APO(14)   | Align, Plan and Organize (전략·계획)                 | |
|  |  BAI(11)   | Build, Acquire and Implement (구축·구입·구현)        | |
|  |  DSS(6)    | Deliver, Service and Support (서비스·지원)           | |
|  |  MEA(4)    | Monitor, Evaluate and Assess (모니터·평가)           | |
|  |                                                                   | |
|  |  Total: 40 Process + 7 Component + Goal Cascade                   | |
|  +---------------------------------+---------------------------------+ |
|                                    |                                   |
|                                    v                                   |
|  Layer 3: OPERATION (운영 계층) - ITIL 4 Service Value Chain (SVC)    |
|  +-------------------------------------------------------------------+ |
|  |  ITIL 4 SVC 6개 Activity:                                        | |
|  |   • Plan --► Improve --► Engage --► Design&Transition --+-► Obtain| |
|  |                                                        |   | Build |
|  |                                                        |   v       |
|  |                                                   Deliver&Support  | |
|  |  34 Practices:  ----------------------------------------------►    | |
|  |   General Mgmt(14) | Service Mgmt(17) | Technical Mgmt(3)          | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  Cross-Layer Concerns:                                            | |
|  |   • Risk (ISO 31000, NIST RMF)                                    | |
|  |   • Security (ISO 27001, NIST CSF 2.0)                            | |
|  |   • Quality (ISO 9001, CMMI v2.0)                                  | |
|  |   • Privacy (GDPR, PIPA)                                          | |
|  +-------------------------------------------------------------------+ |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 Core Model** | 거버넌스/관리 목표 체계 (40 objectives) | 5 Domain × Objective × Process Practice × Activity로 분해, **Goal Cascade(목표 연쇄)** 통해 Stakeholder Drivers -> Enterprise Goals(13) -> Alignment Goals(13) -> Management Objectives(40) 정렬. **Design Factor 11개**(Enterprise Strategy, Enterprise Goals, Risk Profile, etc.)로 시스템의 형상(Configuration) 결정. **Focus Area(20+)** 로 신기술·규제 별 맞춤 가이드 제공. |
| **ITIL 4 Service Value System (SVS)** | IT 서비스 운영·개선 | **SVS 5대 구성**: Opportunity/Demand -> Value(Utility+Warranty) -> 4 Dimensions(Org·People·Information·Technology·Partners·Value Streams) -> Guiding Principles(7) -> Practices(34) -> **Continual Improvement Model**. **Service Value Chain 6 Activity**로 End-to-End 흐름 정의. |
| **ISO/IEC 27001 (ISMS)** | 정보보호 관리체계 | **Plan-Do-Check-Act (PDCA) + 14 Control Domain + 93 Control(Annex A 2022 ver.)**. Risk Assessment -> Statement of Applicability(SOA, 적용성 선언서) -> Risk Treatment Plan -> 모니터링. ISMS-P(국내) = ISMS + PIMS(개인정보보호). 인증 주기 3년, Surveillance Audit 매년. |
| **ISO/IEC 38500** | IT 거버넌스 국제표준 | **3-Activity Model(Evaluate-Direct-Monitor)** + **6 Principles**. 이사회·경영진의 IT 의사결정 프레임워크. ISO 27014(거버넌스), ISO 27005(위험관리)와 연계. **Governance ≠ Management** 원칙 엄격 준수. |
| **Balanced Scorecard (BSC)** | 성과 측정·전략 실행 | **4 Perspectives**(Financial, Customer, Internal Process, Learning&Growth) × **Strategy Map** 으로 전략의 인과관계 시각화. IT-BSC 변형: **Contribution Margin**, **Operational Excellence**, **Future Orientation** 관점 추가 (van der Zee 모델). |
| **TOGAF (EA Framework)** | 엔터프라이즈 아키텍처 | **ADM(Architecture Development Method) 8 Phase**: Preliminary -> Vision -> Business -> Data/Application/Technology -> Opportunities & Solutions -> Migration Planning -> Implementation Governance -> Change Management. **Content Framework**(Deliverable, Artifact, Building Block). |
| **PMBOK 7th / PRINCE2** | 프로젝트 관리 표준 | **PMBOK 7th**: 12 Principles + 8 Performance Domains + Tailoring(맞춤형). **PRINCE2 7 Principles**(Continued Business Justification, Learn from Experience, etc.) + 7 Process + 7 Theme. 프로젝트 vs Program vs Portfolio 구분. |
| **IT 위험 관리 (ISO 31000, NIST RMF)** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 460 / 800

<- **이전**: [459. IT 경영 관리 핵심 토픽 459번 시험 요약](/studynote/12_it_management/05_security_compliance/459_it_management_core_topic_459_exam_summary/)
**다음**: [461. IT 경영 관리 핵심 토픽 461번 시험 요약](/studynote/12_it_management/05_security_compliance/461_it_management_core_topic_461_exam_summary/) ->

---
