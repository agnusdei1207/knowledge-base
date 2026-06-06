---
title: "IT Management Core Topic 759 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리의 핵심은 **COBIT 2019·ISO 38500·ITIL 4** 등 글로벌 거버넌스 프레임워크를 기반으로, **IT 전략 ↔ 비즈니스 가치사슬 ↔ 운영 거버넌스**를 3축으로 통합하여 **Value Realization(가치 실현)** 을 정량적으로 입증하는 경영 체계이며, 759번 토픽은 **거버넌스-전략-포트폴리오-서비스-리스크-아키텍처** 6대 도메인의 통합 관리 역량을 평가한다.
> 2. **가치**: 성숙도 기반 거버넌스 도입 시 **IT 투자 ROI 25~40% 향상**, **인시던트 MTTR 60% 단축**, **컴플라이언스 비용 30% 절감**, **Time-to-Market 50% 단축** 등 정량적 효과를 거버넌스 대시보드를 통해 **BSC(Balanced Scorecard) 4관점(재무/고객/내부/학습성장)** 지표로 입증 가능하다.
> 3. **판단 포인트**: 기술사적 핵심 판단은 **①** 중앙집중형(CoE) vs 분산형(Federated) 거버넌스 모델 선택, **②** Build vs Buy vs Cloud(SaaS) 의사결정의 **TCO 3~5년 분석**, **③** Agile/DevOps 운영체계와 ITIL 변경관리의 **이중 트랙(Dual-Track) 운영 설계**, **④** AI 기반 AIOps·FinOps·Zero-Trust 보안 자동화 수준 결정이다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 지원(Support) 기능에서 **전략적 핵심 자산(Strategic Asset)** 으로 전환됨에 따라, IT 투자의 정당성·효율성·리스크를 통합 관리하는 **IT 거버넌스(Governance)** 와 **IT 경영관리(IT Management)** 체계가 필수 경영 인프라가 되었다. 특히 **디지털 전환(Digital Transformation)**, **클라우드 네이티브**, **AI/ML 기반 의사결정** 환경에서는 전통적 ITIL/COBIT 체계만으로는 비즈니스 민첩성(Agility)을 확보할 수 없어, **ITIL 4 + COBIT 2019 + SAFe/Scrum + DevOps** 의 하이브리드 거버넌스가 요구된다.

```text
+------------------------------------------------------------------+
|          IT 경영 관리 6대 통합 도메인 (Topic 759)                  |
+------------------------------------------------------------------+
|                                                                  |
|   [Tier 1] 전략·거버넌스 계층 (Strategy & Governance Layer)      |
|   +--------------------------------------------------------+    |
|   |  • ISO 38500 IT 거버넌스 원칙 (6원칙)                    |    |
|   |  • COBIT 2019 (40 Governance/Management Objectives)     |    |
|   |  • IT 전략-비즈니스 정렬 (Henderson-Venkatraman 모델)    |    |
|   |  • 이사회-경영진-ISO/IEC 38500 책임 모델                  |    |
|   +--------------------------------------------------------+    |
|                          ^                                       |
|   [Tier 2] 포트폴리오·아키텍처 계층 (Portfolio & EA Layer)        |
|   +--------------------------------------------------------+    |
|   |  • TOGAF ADM 9단계 + Zachman 6x6 프레임워크              |    |
|   |  • IT Portfolio Mgmt (Application/Infrastructure/Project)|    |
|   |  • 투자우선순위 (NRI - Net Relative Value, ROA, NPV)    |    |
|   +--------------------------------------------------------+    |
|                          ^                                       |
|   [Tier 3] 서비스·운영 계층 (Service & Operation Layer)          |
|   +--------------------------------------------------------+    |
|   |  • ITIL 4 Service Value System (SVS) - 7 Guiding Prin.  |    |
|   |  • 34 Practice (변경/사고/문제/릴리스/서비스데스크)       |    |
|   |  • SLA/OLA/UC 다계층 서비스 계약 체계                    |    |
|   +--------------------------------------------------------+    |
|                          ^                                       |
|   [Tier 4] 리스크·보안·컴플라이언스 계층 (GRC Layer)              |
|   +--------------------------------------------------------+    |
|   |  • ISO 27001/27002/27701, NIST CSF 2.0, PCI-DSS         |    |
|   |  • ISO 31000 리스크관리 + COBIT EDM(평가·지시·모니터)   |    |
|   |  • Zero-Trust + DevSecOps + S-SDLC                     |    |
|   +--------------------------------------------------------+    |
|                          ^                                       |
|   [Tier 5] 성과·가치 측정 계층 (Performance & Value Layer)       |
|   +--------------------------------------------------------+    |
|   |  • Balanced Scorecard 4관점 + KPI/KRI 카탈로그          |    |
|   |  • FinOps (클라우드 비용 최적화) + Green IT              |    |
|   |  • IT성숙도모델 (CMMI 5단계, COBIT PAM 5레벨)           |    |
|   +--------------------------------------------------------+    |
|                          ^                                       |
|   [Tier 6] 조직·문화·인재 계층 (People & Culture Layer)           |
|   +--------------------------------------------------------+    |
|   |  • 스킬관리 (SFIA 8), IT역량맵, COBIT Talent Mgmt       |    |
|   |  • DevOps/Agile/Product 조직, SRE, FinOps 역할          |    |
|   |  • 변화관리 (Kotter 8단계, ADKAR)                       |    |
|   +--------------------------------------------------------+    |
|                                                                  |
+------------------------------------------------------------------+
       |
       v
   +--------------------------------------------------+
   |    Value Realization (가치 실현)                    |
   |    • ROI / NPV / IRR / Payback Period             |
   |    • BSC 4관점 정량지표 + 비재무적 가치            |
   |    • Stakeholder Value Network (SVN)              |
   +--------------------------------------------------+
```

**전통적 IT 관리(1990~2010)** 는 **COBIT 4/5 + ITIL v3** 기반으로 **프로세스 중심(process-centric), 사일로(silo)형 조직, CapEx 중심 투자** 를 특징으로 하였다. 그러나 **클라우드·AI·실시간 비즈니스** 환경에서는 **①** CapEx->OpEx 전환, **②** 프로젝트->제품 중심, **③** 연 1회 계획->연속적 비즈니스-IT 정렬(Continuous Alignment) 이 요구되어, **COBIT 2019(목표계단식 Focus Area) + ITIL 4(Value Stream 중심) + SRE/DevOps(자동화·관측가능성)** 가 새로운 표준이 되었다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **도시의 통합 행정 시스템** 과 같다. 상부에는 **도시기본계획·이사회(거버넌스)** 가 있고, 중부에는 **토지이용계획·건축허가(아키텍처·포트폴리오)** 가, 하부에는 **교통·상하수도·소방(서비스·운영)** 이 있으며, 이를 **치안·재난관리(리스크·보안)**, **통계·예산(성과·가치)**, **인구·교육(조직·인재)** 이 뒷받침한다. 이 모든 것이 통합적으로 작동해야 시민(비즈니스)이 안전하고 효율적인 삶을 누린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 거버넌스 시스템 (핵심 엔진)

**COBIT 2019** 는 5대 도메인(EDM: Evaluate-Direct-Monitor, APO: Align-Plan-Organize, BAI: Build-Acquire-Implement, DSS: Deliver-Service-Support, MEA: Monitor-Evaluate-Assess) **40개 Governance/Management Objective** 로 구성되며, **①** 거버넌스 시스템 구성요소(Components: Process/Structure/People/Skills/Information/Service/Infrastructure/Applications) **7개** 와 **②** 디자인 팩터(Design Factors: 11개 - 전략, 목표, 리스크, 컴플라이언스, IT 이슈, 위협, 역할, 기술 도입, 조직 구조 등) 를 조합하여 **기업별 맞춤형 거버넌스 시스템** 을 설계한다.

```text
+---------------------------------------------------------------------+
|              COBIT 2019 거버넌스·관리 목표 40개 맵                    |
+---------------------------------------------------------------------+
|                                                                     |
|   [EDM 도메인] - 이사회·거버넌스 위원회 책임 (5개)                    |
|   +----------------------------------------------------------+    |
|   | EDM01 거버넌스 프레임워크 설정·유지                        |    |
|   | EDM02 가치 전달 보장 (Benefits Realization)              |    |
|   | EDM03 리스크 최적화 (Risk Optimization)                    |    |
|   | EDM04 자원 최적화 (Resource Optimization)                 |    |
|   | EDM05 이해관계자 투명성 (Stakeholder Transparency)        |    |
|   +----------------------------------------------------------+    |
|                              v                                      |
|   [APO 도메인] - Align·Plan·Organize (14개)                         |
|   +----------------------------------------------------------+    |
|   | APO01~14: 전략관리/포지셔닝/비즈니스케이스/조직/정보/     |    |
|   |            성과/리스크/포트폴리오/예산/공급업체/품질/      |    |
|   |            혁신/인재/변화관리/서비스계약                    |    |
|   +----------------------------------------------------------+    |
|                              v                                      |
|   [BAI 도메인] - Build·Acquire·Implement (11개)                     |
|   +----------------------------------------------------------+    |
|   | BAI01~11: 프로그램/프로젝트/요구사항/솔루션/조직변화/      |    |
|   |            변경 수용/변경관리/KM/자산/구성/릴리스          |    |
|   +----------------------------------------------------------+    |
|                              v                                      |
|   [DSS 도메인] - Deliver·Service·Support (6개)                      |
|   +----------------------------------------------------------+    |
|   | DSS01~06: 운영관리/서비스요청/사고/문제/지속성/보안       |    |
|   +----------------------------------------------------------+    |
|                              v                                      |
|   [MEA 도메인] - Monitor·Evaluate·Assess (4개)                     |
|   +----------------------------------------------------------+    |
|   | MEA01~04: 성과/내부통제/외부요구/기술                    |    |
|   +----------------------------------------------------------+    |
|                                                                     |
|   -> 7대 거버넌스 컴포넌트 (Context Components)                      |
|   +----------------------------------------------------------+    |
|   | 1. Process  2. Organizational Structure  3. People/Roles |    |
|   | 4. Skills/Competencies  5. Information/Flows             |    |
|   | 6. Services/Infrastructure  7. Applications/Tools        |    |
|   +----------------------------------------------------------+    |
|                                                                     |
|   -> 11대 디자인 팩터 -> "목표 계단식(Cascade)" 적용                  |
|   ① 기업전략 -> ② 거버넌스목표 -> ③ 관리목표 -> ④ 프로세스활동        |
+---------------------------------------------------------------------+
```

### 2. ITIL 4 Service Value System (SVS)

**ITIL 4** 는 **Value Co-Creation** 관점에서 **7 Guiding Principles**(Focus on Value, Start Where You Are, Progress Iteratively with Feedback, Collaborate and Promote Visibility, Think and Work Holistically, Keep It Simple and Practical, Optimize and Automate) 와 **Service Value Chain(SVC) 6활동**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) 을 중심으로 한다. **34개 Practice** 는 **General(14)**, **Service(17)**, **Technical(3)** 로 분류된다.

### 3. IT 전략 정렬 모델 - Henderson-Venkatraman (Strategic Alignment Model)

```
              +--------------+
              | Business     |
              | Strategy     |
              | (외부/내부)  |
              +------+-------+
                     | 정렬(Alignment)
                     v
+--------------+         +--------------+
| Business     |◄-------►| IT Strategy  |
| Infrastructure|         | (역할/거버넌스)|
| (프로세스/  |         +------+-------+
|  조직/문화)  |               | 정렬(Alignment)
+------+-------+               v
       | 정렬(Alignment)  +--------------+
       +-----------------►| IT           |
                          | Infrastructure|
                          | (시스템/데이터)|
                          +--------------+

-> 4가지 정렬 메커니즘:
  ① Strategy Execution (전략실행): BIZ-Strategy -> IT-Strategy
  ② Technology Transformation (기술활용): BIZ-Strategy -> IT-Infra
  ③ Competitive Potential: BIZ-Infra -> IT-Strategy
  ④ Service Level: BIZ-Infra -> IT-Infra
```

### 4. IT 포트폴리오 관리와 투자 우선순위

IT 포트폴리오는 **Application Portfolio**, **Project/Program Portfolio**, **Infrastructure/Service Portfolio** 3개로 구분되며, 각 자산에 대해 **Risk-Value Matrix** 또는 **Time-Horizon Quadrant** 를 적용한다.

**투자 우선순위 산정 모델**:
- **NRI(Net Relative Value)**: `(총기대이익 × 성공확률 - 총비용) / 총비용`
- **NPV(순현재가치)**: `Σ(Benefit_t - Cost_t) / (1+r)^t` (r: 할인율, 통상 8~12%)
- **ROI** = `(총편익 - 총비용) / 총비용 × 100%`
- **Payback Period** = `총투자액 / 연평균현금흐름`
- **TCO(Total Cost of Ownership)** = `직접비(HW/SW/인건비) + 간접비(교육/다운타임/통합)`
- **ROA(Return on Assets)** = `순이익 / 총IT자산`

### 5. 거버넌스 위원회 및 RACI 매트릭스

```text
+------------------------------------------------------+
|       IT 거버넌스 의사결정 계층 구조                    |
+------------------------------------------------------+
|                                                      |
|  Level 1: 이사회 (Board of Directors)                 |
|    +- IT Strategy Committee (연 4회)                  |
|       +- 주요안건: IT 전략 승인, CapEx > 5억 결정     |
|                     |                                |
|  Level 2: 경영진 (C-Suite)                            |
|    +- CIO + CDO + CISO + CFO + COO                   |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 759 / 800

<- **이전**: [758. IT 경영 관리 핵심 토픽 758번 시험 요약](/studynote/12_it_management/05_security_compliance/758_it_management_core_topic_758_exam_summary/)
**다음**: [760. IT 경영 관리 핵심 토픽 760번 시험 요약](/studynote/12_it_management/05_security_compliance/760_it_management_core_topic_760_exam_summary/) ->

---
