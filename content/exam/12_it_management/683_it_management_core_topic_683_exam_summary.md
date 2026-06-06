---
title: "IT Management Core Topic 683 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심 토픽 683번은 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치사슬(SVC), PMBOK 7th 프로젝트 도메인, ISO 38500 IT 의사결정 모델, EA(Enterprise Architecture) 4대 프레임워크(TOGAF/Zachman/FEAF/Gartner)를 통합 관통하는 **IT-비즈니스 정렬(Strategic Alignment) 및 가치 실현(Value Realization)** 메타 프레임워크임.
> 2. **가치**: 성숙도 모델 기반 정량 측정 시 IT 투자 대비 ROI 평균 25~40% 개선, 거버넌스 미적용 조직 대비 프로젝트 성공률 2.8배(PMI 2021 Pulse of Profession), MTTR 60% 단축, 컴플라이언스 위반 건수 70% 감소 효과를 통해 디지털 전환 실패율(전통적 방식 70%)을 반전시킬 수 있음.
> 3. **판단 포인트**: 거버넌스-관리-운영 계층 분리(Govern/Manage/Operate), RACI 매트릭스 기반 의사결정 권한 분배, Balanced Scorecard(BSC) 4관점 재무/고객/내부/학습, COBIT 2019의 40개 관리목표 중 핵심 5~7개 우선 선정, Agile@Scale 적용 시 거버넌스 오버헤드와 속도 간 트레이드오프가 핵심 설계 변수임.

---

## Ⅰ. 개요 및 필요성

정보관리 기술사 683번 토픽은 한국정보통신기술사회의 출제 빈도가 가장 높은 **IT 거버넌스·서비스 관리·프로젝트 관리·아키텍처·컴플라이언스** 5대 축을 통합한 종합 응용 문제 영역이다. 2020년 이후 디지털 전환(DX) 가속화와 클라우드·AI·데이터 산업의 폭발적 성장으로, IT가 비용 센터(Cost Center)에서 비즈니스 가치 창출 센터(Value Center)로 전환되면서 **"IT가 어떻게 경영 목표에 기여하는가"**를 정량적으로 증명해야 하는 요구가 폭증했다.

기존의 IT 관리 체계는 **2000년대 실리콘밸리 중심의 애플리케이션 운영**, **2010년대 ISMS·PIMS 중심의 정보보호 인증**, **2020년대 DevOps·SRE 중심의 기술 자동화**로 진화해왔으나, 기술사 시험은 이러한 단편적 기술 트렌드가 아닌 **"경영자-이사회-경영층- IT 부서-개발팀-운영팀"으로 이어지는 가치 사슬 전체**를 한 질문으로 묶어 평가한다. 예를 들어 "클라우드 전환 시 거버넌스 체계를 어떻게 재설계할 것인가?"라는 단일 질문에 COBIT의 EDM(평가, 지시, 모니터링) 프로세스, ITIL 4의 34개 실무 가이드, PMBOK의 8개 성과 영역, ISO 38500의 6개 원칙, ISMS-P 인증 통제항목이 동시에 호출되어야 한다.

```text
+---------------------------------------------------------------------+
|          IT 경영 관리 5대 통합 프레임워크 (683번 도메인 맵)           |
+---------------------------------------------------------------------+
|                                                                     |
|   +--------------+   +--------------+   +--------------+          |
|   | ① 거버넌스    |   | ② 서비스관리  |   | ③ 프로젝트관리 |          |
|   |  COBIT 2019  |--->|   ITIL 4     |--->| PMBOK 7th    |          |
|   |  ISO 38500   |   |  SVS/SVC     |   | PRINCE2/Agile|          |
|   |  EDM Model   |   |  34 Practices |   | 8 Performance|          |
|   +------+-------+   +------+-------+   +------+-------+          |
|          |                  |                  |                    |
|          v                  v                  v                    |
|   +------------------------------------------------------+         |
|   |        Strategic Alignment & Value Realization       |         |
|   |     (전략 정렬, BSC, OKR, KPI 트리, 가치 흐름)        |         |
|   +------+-----------------------------------+----------+         |
|          |                                   |                    |
|   +------v-------+                   +------v-------+            |
|   | ④ 아키텍처    |                   | ⑤ 컴플라이언스 |            |
|   |   TOGAF ADM  |                   |  ISMS-P      |            |
|   |   Zachman    |                   |  PIMS/ESG    |            |
|   |   4A 모델     |                   |  GDPR/개인정보|            |
|   +--------------+                   +--------------+            |
|                                                                     |
+---------------------------------------------------------------------+
         |            |              |              |           |
   기업지배구조법  개인정보보호법  클라우드컴퓨팅법  AI기본법  ESG경영
```

683번 토픽의 필요성은 크게 세 가지로 요약된다. 첫째, **규제 환경의 복합화**로 2022년 클라우드컴퓨팅법, 2023년 개인정보보호법 개정, 2024년 AI 기본법(가칭) 등으로 단일 법규 대응이 아닌 **멀티 컴플라이언스 통합 거버넌스**가 필수화되었다. 둘째, **기술 복잡도의 기하급수적 증가**로 모놀리식 -> 마이크로서비스 -> 서버리스 -> AI 워크플로우로 진화하면서, 한 시스템이 200개 이상의 컨테이너와 50개 이상의 외부 API를 호출하는 시대에 전통적 PMBOK 5단계 프로세스만으로는 통제 불가능해졌다. 셋째, **이해관계자 기대치의 다변화**로 CEO는 ROI, CFO는 총소유비용(TCO), CISO는 제로트러스트, CISO는 레질리언스, 개발팀은 속도, 고객은 UX라는 상이한 KPI를 동시에 만족시켜야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리 683번 토픽은 마치 **"도시의 통합 관제탑"**과 같다. 교통(서비스), 소방(보안), 건축(아키텍처), 의료(컴플라이언스), 교육(거버넌스)이 각자 운영되지만, 위에서 내려다보는 관제탑이 없으면 도시 전체가 마비된다. COBIT은 위성 지도, ITIL은 도로 신호, PMBOK는 건설 일정표, TOGAF는 도시 계획도, ISMS는 경찰·소방 통합 지휘본부에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

683번 토픽의 핵심은 **5계층 통합 아키텍처(Governance-Service-Project-Architecture-Compliance)**이며, 각 계층은 명확한 RACI(R=책임, A=승인, C=자문, I=통보) 매트릭스로 연결된다. 최상위 거버넌스 계층은 **이사회-경영진-IT steering committee**로 구성되며 COBIT 2019의 EDM(Evaluate, Direct, Monitor) 5개 프로세스(EDM01~05)가 의사결정 흐름을 정의한다. 중간의 서비스 관리 계층은 **ITIL 4 Service Value System(SVS)**의 7가지 컴포넌트(Opportunity/Demand, Value, Guiding Principles, Governance, Practices, Information, Technology & People)를 통해 가치를 창출한다.

```text
+----------------------------------------------------------------------+
|         IT 경영 관리 5계층 참조 모델 (683번 Architecture Map)         |
+----------------------------------------------------------------------+
|                                                                      |
|  [L5] 전략·이사회 계층  (이사회, CEO, CIO)                           |
|       |                                                              |
|       |  COBIT 2019 EDM: Evaluate-Direct-Monitor                    |
|       |  ISO 38500 6원칙: 책임·전략·수행·준거·인간·행위              |
|       v                                                              |
|  [L4] 거버넌스·정책 계층  (IT Steering Committee)                    |
|       |  +--------------------------------------------+             |
|       |  | 정책체계:  ①정보화기본법  ②개인정보보호법   |             |
|       |  |           ③ISMS-P  ④ESG 정보공시           |             |
|       |  |           ⑤클라우드컴퓨팅 발전법            |             |
|       |  +--------------------------------------------+             |
|       |  목표계단(Cascading): BSC -> OKR -> KPI -> KRI                 |
|       v                                                              |
|  [L3] 서비스·프로세스 계층  (서비스 매니저, PMO)                     |
|       |  +------------+------------+------------+                    |
|       |  | ITIL 4     | PMBOK 7th  | DevOps     |                    |
|       |  | SVS/SVC    | 8 PA       | CAMS/CALMR |                    |
|       |  | 34 Practice| 12 Principle| SRE/SLI/SLO|                    |
|       |  +------------+------------+------------+                    |
|       v                                                              |
|  [L2] 아키텍처·설계 계층  (EA팀, SRE, 플랫폼 엔지니어)               |
|       |  +--------------------------------------------+              |
|       |  | TOGAF ADM: P->A->B->C->D->E->F->G->H (Phase)    |              |
|       |  | Zachman 6×6: What/How/Where/Who/When/Why |              |
|       |  | 4A: BA(비즈) / DA(데이터) / AA(앱) / TA(기술)|            |
|       |  +--------------------------------------------+              |
|       v                                                              |
|  [L1] 운영·기술 계층  (Dev, Ops, Sec, Data)                          |
|       |  IaC(Terraform/Ansible)  GitOps(ArgoCD)                      |
|       |  Observability(Prometheus/Grafana/ELK)                      |
|       |  FinOps(클라우드 비용 최적화)  AIOps(사고 대응)              |
|       v                                                              |
|  [L0] 인프라·데이터 계층  (Public/Private/Hybrid Cloud, On-Prem)     |
|       AWS/Azure/GCP/Naver Cloud / Kubernetes / Istio / Kafka         |
|                                                                      |
+----------------------------------------------------------------------+
```

| 계층 | 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- | :--- |
| **L5 전략** | 이사회·ESG위원회 | IT-Biz 정렬, 장기 로드맵 | COBIT 2019 EDM05(관리체계 감독), ISO 38500 Principle1(Responsibility), 기업지배구조보고서 |
| **L4 거버넌스** | IT Steering Committee | 정책 수립, 우선순위 결정, 예산 승인 | COBIT 2019 40개 관리목표(예: APO12 위험관리, BAI01 프로그램관리, DSS01 운영관리), RACI 매트릭스 |
| **L3 서비스·PM** | 서비스 매니저, PMO, Scrum Master | 서비스 카탈로그, 프로젝트 포트폴리오 관리 | ITIL 4 34개 실무(예: Incident Mgmt, Change Enablement, Service Level Mgmt), PMBOK 7th 8개 성과영역(팀/접근방식/계획/불확실성/측정/일정/예산/위험) |
| **L2 아키텍처** | EA팀, 플랫폼 엔지니어, SRE | 시스템 청사진, 표준화, 기술 부채 관리 | TOGAF ADM 8단계 Preliminary~Requirements Management, Zachman 6×6 매트릭스(What=Data, How=Function, Where=Network, Who=People, When=Time, Why=Motivation), 4A 모델(BA/DA/AA/TA) |
| **L1 운영** | DevOps, SecOps, DataOps | 자동 배포, 모니터링, 사고 대응 | GitOps(ArgoCD/Flux), IaC(Terraform/Pulumi/Crossplane), AIOps(Datadog/Splunk/Dynatrace), FinOps(Cloudability/Vantage) |
| **L0 인프라** | Cloud, K8s, DBMS | 컴퓨팅·스토리지·네트워크 자원 제공 | 멀티클라우드(AWS+Azure+GCP), 서비스 메시(Istio/Linkerd), 데이터레이크(S3+Iceberg), 엣지(Kubernetes@Edge) |

**핵심 원리 1 - 거버넌스-관리 분리(Govern/Manage 원칙)**: COBIT 2019는 거버넌스(EDM 5개 프로세스)와 관리(Domain: APO/BAI/DSS/MEA 35개 프로세스)를 명확히 분리한다. 거버넌스는 "무엇을 할 것인가"의 의사결정, 관리는 "어떻게 할 것인가"의 실행이다. 기술사 시험에서 빈번히 출제되는 함정은 PMBOK의 "프로세스 그룹"(시작ing-계획ing-실행ing-감독ing-종료ing)과 ITIL의 "서비스 라이프사이클"(전략-설계-전이-운영-지속적개선)을 혼동하는 것이다.

**핵심 원리 2 - 가치 사슬(Value Chain)의 양방향성**: ITIL 4의 Service Value Chain(SVC)은 6개 활동(Plan/Improve/Engage/Design&Transition/Obtain&Build/Deliver&Support)으로 구성되며, **수요(Demand)에서 가치(Value)로 가는 정방향 흐름**과 **기회(Opportunity)와 가치의 피드백 흐름**이 동시에 존재한다. 전통적 ITIL v3의 5단계 Lifecycle은 선형(Linear) 구조였으나, SVC는 비선형(Non-linear) 의사결정 그래프로서 Agile·DevOps 환경에 최적화되었다.

**핵심 원리 3 - 캐스케이드 목표(Cascading Goals)**: COBIT 2019의 13개 Enterprise Goals과 13개 Alignment Goals은 **연쇄적 인과관계(Chain of Cause-and-Effect)**로 연결된다. 예를 들어 "EG01 경쟁 포트폴리오" 달성을 위해 "AG01 IT 준수 및 지원", 이를 위해 "BAI01 관리 프로그램과 프로젝트", 이를 위해 "BAI02 요구사항 정의", 이를 위해 "BAI03 솔루션 식별 및 구축"으로 5단계 캐스케이드된다. 기술사는 이 캐스케이드를 통해 KPI 트리(Goal -> Metric -> Target -> Threshold)를 설계할 수 있어야 한다.

**핵심 원리 4 - 위험 기반 의사결정(Risk-Based Decision Making)**: PMBOK 7th의 8개 성과영역 중 "Uncertainty"는 리스크, 모호성(Ambiguity), 복잡성(Complexity), 변동성(Volatility) 4가지 불확실성을 구분한다. 정량적 분석(Monte Carlo Simulation, Decision Tree Analysis) 결과 기대금전가치(EMV=확률×영향)가 음수인 대안은 거부하며, Risk Burndown Chart로 시간 경과에 따른 리스크 해소 추이를 시각화한다.

- **📢 섹션 요약 비유**: 5계층 아키텍처는 **"의료 시스템"**과 같다. L5는 건강보험 심사평가원(이사회), L4
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 683 / 800

<- **이전**: [682. IT 경영 관리 핵심 토픽 682번 시험 요약](/studynote/12_it_management/05_security_compliance/682_it_management_core_topic_682_exam_summary/)
**다음**: [684. IT 경영 관리 핵심 토픽 684번 시험 요약](/studynote/12_it_management/05_security_compliance/684_it_management_core_topic_684_exam_summary/) ->

---
