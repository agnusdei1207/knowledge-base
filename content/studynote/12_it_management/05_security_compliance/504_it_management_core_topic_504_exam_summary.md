---
title: "504. IT 경영 관리 핵심 토픽 504번 시험 요약 (IT Management Core Topic 504 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리 기술사 504번 시험은 COBIT 2019 거버넌스 프레임워크, PMBOK 7th Edition 프로젝트 관리, EA(Enterprise Architecture) 기반 ISP/BSP/MP 연계, ITIL 4 서비스 가치시스템(SVS), ISMS-P 정보보안 거버넌스, ISO 38500 이사회 IT 거버넌스, DAMA-DMBOK 데이터 거버넌스, ISO 21500 프로젝트 거버넌스가 통합 측정·평가되는 종합 영역이다.
> 2. **가치**: 단순 암기형이 아닌 CSF/KPI 기반 정량평가, RACI 매트릭스 책임분담, Balanced Scorecard 4관점(재무/고객/내부/학습성장) 전략 연계, To-Be/As-Is 갭 분석을 통한 ROI 20~35% 개선, MOF 4-Layer 거버넌 모델 기반 의사결정 품질 향상이 핵심 평가축이다.
> 3. **판단 포인트**: 거버넌스-관리(Governance vs Management) 분리 원칙, Agile-Waterfall 하이브리드(예: Scrumban, Sashimi) 적용 트레이드오프, 클라우드 전환 시 CapEx->OpEx 재무 구조 변화, Zero Trust 보안 모델 도입 시 레거시 시스템 호환성, BCP/DRS RTO/RPO 산정 시 비용-가용성 Trade-off가 기술사형 서술형 답안의 핵심 판단기준이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 504번 시험은 1986년 한국정보처리기술사 제도 도입 이래 39년간 축적된 IT 경영관리 지식체계의 정수(精髓)를 평가하는 국가공인 최고 난이도 시험이다. 본 영역은 단일 기술 암기가 아닌, **거버넌스(Governance) ↔ 관리(Management) ↔ 운영(Operation)** 3계층 의사결정 체계와, **전략(Strategy) ↔ 전술(Tactic) ↔ 실행(Operation)** 3계층 실행 체계의 교차점에서 기술적 판단력을 검증한다.

2000년대 이후 4차 산업혁명, 디지털 전환(DX), AI/ML 기반 업무 자동화, Post-COVID19 원격근무常态化, 2024년 EU AI Act·한국 AI 기본법(2026.1 시행) 등 규제 환경 급변으로, IT 경영관리 패러다임은 **"기술중심(Technology-Centric) -> 가치중심(Value-Centric) -> 신뢰중심(Trust-Centric)"** 으로 전환되었다. 과거 COBIT 4.1의 프로세스 중심(34개 프로세스) -> COBIT 2019의 40개 관리목표·포괄적 원칙(6원칙)·7개 컴포넌트로 진화했고, 전통적 Waterfall(폭포수) -> Agile(스크럼) -> DevOps -> DevSecOps -> BizDevOps(GitOps 포함) -> 플랫폼 엔지니어링(Platform Engineering) 으로 개발운영 문화가 변모했다.

```text
+------------------------------------------------------------------+
|           504번 시험이 평가하는 IT 경영관리 4대 축(Axis)         |
+------------------------------------------------------------------+
|                                                                  |
|   ① 거버넌스(G)        ② 관리(M)         ③ 운영(O)             |
|   +---------+         +---------+       +---------+            |
|   | 이사회   |<---결의--| CIO/CTO  |<--명령-| 현업/IT  |            |
|   | 평가·감독 |         | 기획·조정 |       | 실무운영 |            |
|   | 방향성    |         | KPI/CSF  |       | SLA/OLA |            |
|   +---------+         +---------+       +---------+            |
|         |                   |                  |                 |
|         +-----Stakeholder Needs & Goals------+                 |
|                          |                                      |
|   +----------------------v----------------------+              |
|   | ④ 기술사 핵심역량: 통합·최적화 의사결정(EDM) |              |
|   |  - Benefit Realization(가치실현)             |              |
|   |  - Risk Optimization(리스크 최적화)           |              |
|   |  - Resource Optimization(자원 최적화)         |              |
|   |  - Stakeholder Transparency(이해관계자 투명성)|              |
|   +---------------------------------------------+              |
|                                                                  |
|  시험 교차평가:                                                   |
|   [전략기획(ISP)] × [프로세스(PMBOK/ITIL)] × [아키텍처(EA)]     |
|   × [보안(ISMS-P)] × [감리/통제] × [BSC/KPI 성과측정]           |
+------------------------------------------------------------------+
```

504번 시험은 ① 거버넌스-관리-운영 분리 원칙, ② CSF/KPI 정량평가, ③ ROI/TCO 비용정당화, ④ TOGAF/COBIT/Zachman EA 프레임워크 연계, ⑤ Agile/DevOps/DevSecOps 문화코드 적용, ⑥ ISMS-P 64개 통제항목, ⑦ 개인정보보호법·GDPR·AI 기본법 컴플라이언스, ⑧ BCP/DR RTO/RPO·MTTR/MTBF 산정, ⑨ EA 4관점(BDAT: Business/Data/Application/Technology) 정합성을 통합 판단하는 **"사례기반 서술형"** 문제로 구성된다.

- **📢 섹션 요약 비유**: IT 경영관리는 **"항공우주 임무통제실(Mission Control)"** 과 같다. 이사회(Governance)가 비콘(Beacon)·궤도(Orbit)·임무목표(Mission Goal)를 결정하면, 지상관제사(IT 관리)가 비행계획(Mission Plan)·체크리스트(SOP)·연료·탑재체(EA/프로세스)를 준비하고, 비행조종사·우주비행사(IT 운영)가 실제로 발사·도킹·회수 임무를 수행한다. NASA에서도 Apollo 13 위기 시 Mission Control의 통합 판단력이 생존을 결정했다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 원리는 **"전략-아키텍처-프로세스-기술-인력-재무" 6요소의 정렬(Alignment)** 이며, 이를 실현하는 5대 표준 프레임워크가 504번 시험의 뼈대다: ① **COBIT 2019**(거버넌스/관리), ② **TOGAF 10**(EA 아키텍처), ③ **PMBOK 7th Edition**(프로젝트 관리), ④ **ITIL 4**(서비스 관리), ⑤ **ISO 27001:2022 + ISMS-P**(정보보안).

```text
+--------------------------------------------------------------------+
|        IT 경영관리 통합 참조모델(Integrated Reference Model)      |
|                                                                     |
|  +---- 최상위: 이사회(Board) / CEO / CxO -----+                    |
|  |  ISO 38500 (6원칙: 책임/전략/획득/성과/    |                    |
|  |  규율/인간행위) + COBIT 2019 EDM 도메인    |                    |
|  +------------------+-------------------------+                    |
|                     | 목표연계(Goals Cascade)                       |
|  +------------------v-------------------------+                    |
|  |  전략기획(ISP) 영역                          |                    |
|  |  - 환경분석(SWOT/5Forces/PESTEL/STEEP)      |                    |
|  |  - 정보화 투자우선순위(개별경제성+종합경제성) |                    |
|  |  - BSC 4관점 + CSF/KPI 12~20개              |                    |
|  +------------------+-------------------------+                    |
|                     |                                             |
|  +------------------v-------------------------+                    |
|  |  아키텍처(EA) 영역 - TOGAF ADM 8단계         |                    |
|  |  Preliminary->Vision->Business->IS->Tech->      |                    |
|  |  Opportunities->Migration->Governance(Cycle) |                    |
|  |  4A: BDAT (Business/Data/Application/Tech)  |                    |
|  +------------------+-------------------------+                    |
|                     |                                             |
|  +------------------v-------------------------+                    |
|  |  프로세스(Process) 운영 영역                  |                    |
|  |  PMBOK: 5 Process Groups × 49 Processes     |                    |
|  |  ITIL 4: 34 Practices (14 GP + 3 SP × ...)  |                    |
|  |  COBIT 2019: 40 Management Objectives       |                    |
|  |  DevOps: Plan-Code-Build-Test-Release-       |                    |
|  |         Deploy-Operate-Monitor(feedback)    |                    |
|  +------------------+-------------------------+                    |
|                     |                                             |
|  +------------------v-------------------------+                    |
|  |  기술/인프라/보안 영역                        |                    |
|  |  Cloud(IaaS/PaaS/SaaS/FaaS) + K8s/Istio     |                    |
|  |  Zero Trust(SDP/ZTNA) + DevSecOps           |                    |
|  |  ISMS-P 64통제 + ISO 27001:2022 Annex A     |                    |
|  |  Privacy: PIPC 23조, GDPR Art.30/32/35      |                    |
|  +----------------------------------------------+                    |
|                                                                     |
|  +--- 피드백루프(Feedback Loop) ----------------------+              |
|  | 감리/감사(Inspection) -> KPI 측정 -> 개선(CAP)     |              |
|  | -> KPI 재설정 -> 전략 재조정 -> ... (PDCA/ADLI)     |              |
|  +--------------------------------------------------+              |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019 거버넌스 시스템** | IT 성과와 비즈니스 목표 연계, 40개 관리목표(MG) 측정·감독 | 6원칙(① stakeholder needs ② holistic ③ dynamic ④ governance distinct from mgmt ⑤ tailored ⑥ goals cascade), 7컴포넌트(① Principles/Policies/Frameworks ② Processes ③ Organizational Structures ④ People/Skills/Competencies ⑤ Culture/Ethics/Behavior ⑥ Information ⑦ Services/Infrastructure/Applications), 5관점(① Benefits Realization ② Risk Optimization ③ Resource Optimization ④ Stakeholder Transparency ⑤ Holistic Approach), EDM 5개, APO 14개, BAI 11개, DSS 6개, MEA 4개 = 40 MG, Capability Level 0~5 (PA 1.1~5.2), 100% 달성률 = Level 5 |
| **TOGAF 10 EA 아키텍처** | BDAT 4관점(BDAT: Business/Data/Application/Technology) 정합 To-Be 설계 | ADM 8단계(① Preliminary ② Vision ③ Business Architecture ④ IS Architecture ⑤ Technology Architecture ⑥ Opportunities & Solutions ⑦ Migration Planning ⑧ Implementation Governance -> Change Management -> Requirements Management 순환), 30+ 델리버러블·아티팩트, **ADM Cycle** 반복·Phase A~H, **Architecture Repository**(ABD-ARB-ABs), Content Metamodel(코어+확장), **Architecture Style**(예: 마이크로서비스·이벤트드리븐·메시지큐), Capability-Based Planning, Gap Analysis(As-Is -> To-Be) |
| **PMBOK 7th Edition 프로젝트 관리** | 프로젝트 성공 8개 성과영역(Performance Domain) 통합 관리 | **8개 PD**: ① Stakeholder ② Team ③ Development Approach & Life Cycle ④ Planning ⑤ Project Work ⑥ Delivery ⑦ Measurement ⑧ Uncertainty. **12 Principle**: ① Be Steward ② Collaborate ③ Build Q'ty ④ Focus Value ⑤ Recognize Complexity ⑥ Optimize Risk ⑦ Adapt & Resiliency ⑧ Enable Change ⑨ Steward Integration  etc. **Value Delivery System**(포터 가치사슬 연계), 49 Processes는 5 Process Groups(Initiating/Planning/Executing/M&C/Closing) × 10 Knowledge Areas로 유지(연계). Predictive/Adaptive/Hybrid 접근법 |
| **ITIL 4 서비스 가치시스템(SVS)** | IT 서비스의 가치공급(Value Co-Creation) End-to-End 관리 | **Service Value Chain** 6활동(Opportunity & Demand->Engage->Design & Transition->Obtain/Build->Deliver & Support->Improve), **34 Practices**(14 General: Continual Improvement/Information Security Mgmt/Relationship/Supplier/Workforce & Talent/... + 17 Service: Incident/Problem/Change Enablement/SLM/Catalog/... + 3 Technical: Deployment Mgmt/Infrastructure/Software Dev & Mgmt), **7 Guiding Principles**(Focus on Value/Start Where You Are/Progress Iteratively/Collaborate/Think & Work Holistically/Keep It Simple/Optimize & Automate), 4D 모델(Dimension: Organizations & People/Information & Data/Partners & Suppliers/Value Streams & Processes/Technology) |
| **ISMS-P & ISO 27001:2022** | 정보자산 3대 특성(기밀성/무결성/가용성) 및 PII(개인식별정보) 보호 | ISMS-P 64개 통제(관리적 12 + 물리적 11 + 기술적 41), ISO 27001:2022 Annex A 93 통제(4그룹: ① Organizational 37 ② People 8 ③ Physical 14 ④ Technological 34), PDCA 4단계(Plan-Do-Check-Act), Risk Assessment(자산×위협×취약성×영향), Statement of Applicability(SoA 93항목 적용결정), ISMS 인증(3년주기+1년 Surveillance) |

504번 시험의 핵심 평가축인 **CSF/KPI 정량 평가**는 다음과 같이 산정한다:

- **CSF(Critical Success Factor)**: 정보화 목표 달성을 위한 핵심 성공요인(예: "CEO 정보시스템 만족도", "정보화 투자 대비 ROI")
- **KPI(Key Performance Indicator)**: CSF를 측정하는 정량지표(예: "시스템 가용성 99.95%", "MTTR ≤ 30분", "MTBF ≥ 720시간", "프로젝트 정시完工율 ≥ 90%", "결함누출률 ≤ 0.5%", "변경관리 승인률 100%", "CSP(보안패치) 적용률 ≥ 98% 7일내")
- **KGI(Key Goal Indicator)**: 최종 목표 달성도(예: "매출증대 15%", "고객이탈률 8% 감소", "BSC 재무관점 ROI 25%")
- **성과측정 균형화**: BSC 4관점(재무 25% + 고객 25%
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 504 / 800

<- **이전**: [503. IT 경영 관리 핵심 토픽 503번 시험 요약](/studynote/12_it_management/05_security_compliance/503_it_management_core_topic_503_exam_summary/)
**다음**: [505. IT 경영 관리 핵심 토픽 505번 시험 요약](/studynote/12_it_management/05_security_compliance/505_it_management_core_topic_505_exam_summary/) ->

---
