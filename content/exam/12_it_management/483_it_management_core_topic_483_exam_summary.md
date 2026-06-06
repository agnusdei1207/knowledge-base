---
title: "IT Management Core Topic 483 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **ISO 38500(거버넌스) -> COBIT 2019(관리체계) -> ITIL 4(서비스 운영) -> TOGAF(EA) -> PMBOK 7(사업관리)** 5계층 표준 프레임워크를 비즈니스 전략·리스크·자원·성과 축으로 통합하여, IT가 단순 비용센터에서 **가치 창출 엔진(Value Driver)**으로 전환되도록 통제하는 종합 경영 체계이다.
> 2. **가치**: McKinsey & Company(2024) 연구에 따르면 디지털·IT 거버넌스 성숙도 상위 25% 조직은 **매출 성장률 2.3배, ROI 23~37% 향상, IT 프로젝트 실패율 50% 감소, Time-to-Market 40% 단축** 효과를 달성하며, ISO 38500 기반 거버넌스 도입 시 **IT 운영비 15~25% 절감**이 실증된다.
> 3. **판단 포인트**: 기술사적 핵심 의사결정은 ①거버넌스 성숙도 진단 결과에 따른 **Adopt/Adapt/Develop 전략**, ②규제 산업(금융·공공·의료) 여부에 따른 **컴플라이언스 우선 vs 가치 우선 트레이드오프**, ③EA·ITIL·Agile·DevOps·AIops의 **적정 통합도(Integrated Toolchain Level 1~5)** 결정에 있다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명·생성형 AI·클라우드 네이티브 전환으로 인해 IT 투자는 매년 12~15% 증가하는 반면, Standish Group CHAOS Report 2023에 따르면 **전체 IT 프로젝트의 31.1%는 실패, 53.5%는 일정·예산 초과**, 가치 실현(Value Realization) 실패율이 여전히 40% 이상에 달한다. Gartner는 2026년までに **CIO의 60%가 "기술 부채(Technical Debt)"와 "AI 거버넌스 부재"로 디지털 이니셔티브가 좌초**할 것으로 전망한다.

이에 따라 단순 IT 운영을 넘어 **전략-거버넌스-아키텍처-서비스-컴플라이언스를 아우르는 통합 IT 경영 관리 체계**의 수립이 국가·기업 경쟁력의 핵심 역량으로 부상했다. 한국 정보통신산업진흥원(KIAT) 및 디지털정부사업은 매년 약 12조 원 규모의 IT 사업을 집행하며, 이에 대한 **정보시스템 감리·ISP(Information Strategy Planning)·EA(Enterprise Architecture) 수립·SW사업 대가기준 준수**가 법·제도적 의무로 강제된다.

본 토픽 483번은 **"IT 경영 관리"의 전체 영역을 4대 축(거버넌스/전략, 아키텍처/방법론, 운영/서비스, 감리/컴플라이언스)으로 분해**하고, 각 축의 글로벌 표준·국내 제도·실무 적용·기술사 판단 포인트를 통합적으로 다룬다.

```text
+------------------------------------------------------------------------+
|          IT 경영 관리 4대 축 통합 프레임워크 (Topic 483)              |
+------------------------------------------------------------------------+
|                                                                        |
|   +--------------- 1축: 거버넌스 & 전략 (Why & Who) ---------------+  |
|   |  ISO 38500  ->  COBIT 2019  ->  BSC  ->  IT-PMO  ->  RACI Matrix  |  |
|   |  +-- CIO/CDO/CTO 거버넌스 위원회, 의사결정 권한 매트릭스            |  |
|   +-------------------------------------------------------------+--+  |
|                                                                  |      |
|                          전략-실행 연계(Strategy Execution)         |      |
|                                                                  v      |
|   +--------------- 2축: 아키텍처 & 방법론 (What & How) ----------+  |
|   |  TOGAF 10 ADM  ->  한국 EA 참조모델  ->  BIZ/APP/DATA/TECH      |  |
|   |  +-- ISP, ISP/EA 통합, 마이크로서비스, 도메인 주도 설계(DDD)      |  |
|   +-------------------------------------------------------------+--+  |
|                                                                  |      |
|                          아키텍처-구축 연계(Architecture Build)       |      |
|                                                                  v      |
|   +--------------- 3축: 운영 & 서비스 (Run & Improve) -----------+  |
|   |  ITIL 4 (SVS)  ->  DevOps  ->  SRE  ->  AIOps  ->  FinOps        |  |
|   |  +-- 34개 Practice, Service Value Chain, 인시던트 MTTR < 1h     |  |
|   +-------------------------------------------------------------+--+  |
|                                                                  |      |
|                          서비스-가치 연계(Value Realization)         |      |
|                                                                  v      |
|   +--------------- 4축: 감리 & 컴플라이언스 (Verify & Comply) ----+  |
|   |  정보시스템 감리법  ->  ISMS-P  ->  ISO 27001:2022  ->  GDPR/PIA  |  |
|   |  +-- SW사업 대가기준, SW품질관리, 클라우드 보안인증(CSAP)         |  |
|   +-------------------------------------------------------------+--+  |
|                                                                  |      |
|                          피드백 루프(Continuous Audit & Improvement) |      |
|                          ^--------------------------------------+      |
|                          |                                              |
|                          +------- 1축 거버넌스로 환류                   |
+------------------------------------------------------------------------+

[범례]
+- : 의사결정 흐름 (Top-Down)      +- : 피드백 흐름 (Bottom-Up)
->  : 데이터·정보 흐름              v  : 전략-실행 연계
```

기존(Old) 패러다임은 **①IT 부서가 독립적으로 시스템 구축, ②프로젝트 완료 시 종료, ③기술 중심 의사결정, ④분절된 거버넌스**였다. 새로운(New) 패러다임은 **①IT가 비즈니스 전략과 실시간 정렬(Strategy Alignment), ②제품 중심 장기 로드맵(Product-centric), ③데이터·AI 윤리·리스크 기반 의사결정, ④End-to-End Value Stream 통합 거버넌스**로 전환된다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"건축물의 도심계획(거버넌스) -> 설계도(EA) -> 시공·관리(서비스) -> 안전진단(감리)"**이 4단계로 맞물려 도시는 물론 개별 빌딩의 가치를 극대화하는 **"스마트시티 통합 운영 체계"**와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 4대 축의 핵심 메커니즘은 **"PDCA + Strategy -> Architecture -> Service -> Compliance"**의 연속 사이클이다. 각 축의 표준 프레임워크가 어떤 컴포넌트로 구성되며, 어떻게 상호 운용하는지 단계별로 분해한다.

```text
   [이해관계자 Needs] -> [전략] -> [아키텍처] -> [구축/운영] -> [가치 측정]
        |                |          |              |              |
        v                v          v              v              v
   +---------+    +----------+  +----------+  +----------+  +----------+
   |KPI/CSF  |    |BSC/OKR  |  |TOGAF ADM|  |ITIL SVS  |  |ROI/NPS  |
   |Risk Reg.|    |Portfolio |  |4A(BA/DI/|  |34 Practice| |Audit Trail|
   |Stakeh.  |    |Governance|  |TA/AA)   |  |CI/CD/CT  |  |Compliance|
   +----+----+    +----+-----+  +----+-----+  +----+-----+  +----+-----+
        +--------------+-------------+-------------+--------------+
                              | Feedback Loop |
                              v               v
                       [Continuous Improvement] [Governance Board]
```

### 1축: 거버넌스 & 전략 컴포넌트 (ISO 38500 / COBIT 2019)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO 38500 거버넌스 모델** | IT 의사결정의 3개 영역(Evaluate·Direct·Monitor) 정의 | 6개 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior) 기반 **이사회-경영진-IT** 3계층 책임 분배; 1년 주기 Self-Assessment + 외부 Audit |
| **COBIT 2019** | 40개 거버넌스·관리 Objective와 컴포넌트 매핑 | 5개 도메인(EDM·APO·BAI·DSS·MEA) × **핵심 컴포넌트(Process/Structure/People/Skills/Information/Service/Infrastructure/Application)** = 250+ 컴포넌트 매트릭스; **Focus Area(예: 사이버보안, DevOps, AI 거버넌스)** 커스터마이징 |
| **Balanced Scorecard (BSC)** | 4관점(Financial/Customer/Internal/Learning) 성과 측정 | ①재무관점 ROI ②고객관점 NPS ③내부프로세스 MTTR ④학습관점 직원 역량; **전략맵(Causal Map)**으로 KPI 인과관계 시각화 |
| **IT-PMO / RACI Matrix** | IT 포트폴리오 의사결정 및 역할 책임 명확화 | Responsible(수행) / Accountable(책임) / Consulted(자문) / Informed(통보) 4분류; 다단계 거버넌스 위원회(전략심의->투자심의->위험심의) 운영 |
| **IT Portfolio & Demand Mgmt** | 한정된 IT 자원(예산·인력)의 최적 배분 | **Bob Lewis Portfolio Grid**(Run/Grow/Transform × Risk/Value), **Kraljic Matrix**(전략/병목/레버리지/비핵심) 적용; 수요-공급 균형 모델(Decision Lens, Apptio) |

### 2축: 아키텍처 & 방법론 컴포넌트 (TOGAF / EA / ISP)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **TOGAF 10 ADM** | EA 수립의 8단계(Phase A~H) 사이클 | Preliminary -> Vision -> Business/IS/Data/Technology Architecture -> Opportunities -> Migration Planning -> Implementation Governance -> Architecture Change Mgmt. **ADM Iteration Cycle** 최소 3회(아키텍처 비전·상세·전환) |
| **한국 EA 참조모델 (eARF)** | 정부·공공 EA 표준화 | 4A(**BA** Business, **DA** Data, **AA** Application, **TA** Technology) + 2S(Standard, Security); **EA-View 4유형(현행As-Is/목표To-Be/전환Transition/차이Gap)** 표준 산출물 |
| **ISP (Information Strategy Planning)** | 중장기(3~5년) 정보화 전략 수립 | **3단계(현황분석 -> 전략수립 -> 실행계획) × 11개 과제**; 정보화 투자 효율화, 업무 프로세스 재설계, 시스템 구축 우선순위 도출 |
| **마이크로서비스 & DDD** | 도메인 경계 기반 서비스 분리 | Bounded Context, Aggregate Root, Context Map; **12-Factor App** + API Gateway(Kong, Istio) + Service Mesh + Event-Driven(EDA) |
| **클라우드 네이티브 아키텍처** | 확장성·탄력성·가용성 확보 | CNCF Landscape 1,000+ 프로젝트, K8s(Control Plane/Worker Node) + Serverless(Lambda, Cloud Run) + GitOps(ArgoCD, Flux) + Service Mesh(Istio/Linkerd) |

### 3축: 운영 & 서비스 컴포넌트 (ITIL 4 / DevOps / SRE / AIOps)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ITIL 4 SVS (Service Value System)** | 서비스 가치 창출의 End-to-End 체계 | 5개 컴포넌트(가치/원리/거버넌스/실천/개선) + **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support); **34개 Practice**(일반/서비스/기술) |
| **DevOps / CI-CD-CT 파이프라인** | 개발-배포 자동화로 Lead Time 단축 | Plan(SAFe/Scrumban) -> Code(Git) -> Build(Maven/Gradle) -> Test(Selenium/JUnit/Sonarqube) -> Release(ArgoCD) -> Deploy -> Operate(Monitor) -> **Continuous Testing(CT)** = Shift-Left Testing; **DORA 4대 지표** |
| **SRE (Site Reliability Engineering)** | 신뢰성·운영 효율성 양립 | **SLI/SLO/SLA** 3계층, **Error Budget**(99.9% SLO = 월 43.8분), Toil(반복작업) < 50% 원칙, **Blameless Postmortem** |
| **AIOps & Observability** | AI 기반 IT 운영 자동화 | 3대 신호(Logs·Metrics·Traces) + **OpenTelemetry** 표준; **AIOps 플랫폼**(Dynatrace, Splunk ITSI, Moogsoft)의 이상탐지·근본원인분석(RCA)·자동복구(Self-Healing) |
| **FinOps
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 483 / 800

<- **이전**: [482. IT 경영 관리 핵심 토픽 482번 시험 요약](/studynote/12_it_management/05_security_compliance/482_it_management_core_topic_482_exam_summary/)
**다음**: [484. IT 경영 관리 핵심 토픽 484번 시험 요약](/studynote/12_it_management/05_security_compliance/484_it_management_core_topic_484_exam_summary/) ->

---
