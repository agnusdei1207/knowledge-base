---
title: "506. ITIL 서비스 관리 프레임워크 (ITIL Service Management Framework)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ITIL 4 Service Value System(SVS)은 ITIL Service Value Chain(Engage->Plan->Improve->Design & Transition->Obtain/Build->Deliver & Support) 6개 활동(Value Chain Activities)과 34개 Practices, 7 Guiding Principles, 4 Dimensions를 통합하여 "Opportunity/Demand -> Value"로 전환하는 End-to-End Value Orchestration 프레임워크이다.
> 2. **가치**: ITIL 4 도입 조직은 평균 MTTR(Mean Time To Restore) 30~50% 단축, Change Success Rate 75%->95% 향상, First Call Resolution(FCR) 20~35% 증가, Major Incident 비율 40% 감소 등 정량적 ITSM 개선이 보고되며, ISO 20000, COBIT 2019, SIAM(Sourcing Integration And Management)과의 매핑을 통한 거버넌스 통합이 가능하다.
> 3. **판단 포인트**: ITIL 4 도입 시 "Shift Left(셀프서비스 확대) vs Shift Right(전문화)", "Process Compliance(엄격한 단계별 진행) vs Agile/DevOps(반복적 가치 전달)", "Tool-centric(ServiceNow/Jira SM 중심) vs Practice-centric(문화·역량 우선)"의 트레이드오프를 조직의 Service Consumption Profile(Utility + Warranty + Experience)과 Value Stream Mapping 결과에 따라 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 운영은 1990년대 말까지 silo 형태의 기능별 관리(Function-centric: Network팀, Server팀, DB팀)에 머물러, 비즈니스 요구사항과 IT 운영 간의 갭이 "IT와 Business는 서로 다른 언어를 말한다"는 클리포드(Bryant N. Clifford, 2002)의 진단으로 상징되었다. ITIL v1(1989, CCTA UK) -> v2(2001, 7개 라이브러리: Service Support, Service Delivery 등) -> v3/2011(5단계 Lifecycle: Strategy, Design, Transition, Operation, CSI) -> **ITIL 4(2019, AXELOS/PeopleCert)**로의 진화는 "프로세스 -> 서비스 가치 사슬 -> 가치 공동창조(Value Co-Creation)"로 패러다임이 전환되었음을 의미한다.

ITIL 4가 등장하게 된 핵심 동인은 ① 클라우드·SaaS·DevOps·SRE의 보편화로 인한 운영 자동화(97% of enterprises adopting public cloud, Flexera 2023), ② Agile·Lean·Design Thinking의 문화적 확산, ③ Experience-centric 시대의 도착(EX/CX 우선주의), ④ Supplier Ecosystem의 복잡화(Multi-sourcing, 5~7개 벤더 평균) 등이다. 기존 v3 Lifecycle 모델은 "Linear & Stage-gate" 방식이라 DevOps의 Continuous Delivery(예: 하루 100회 배포, Amazon·Netflix 사례)와 충돌하므로, SVS의 Value Chain Activity는 Backlog item 단위로 동시다발적·반복적으로 수행되어야 한다.

```text
[ITIL 진화 패러다임 전환도]

v1 (1989)                  v2 (2001)              v3/2011              ITIL 4 (2019)
+----------+           +----------+           +----------+          +----------+
| Best     |           | Process- |           | Service  |          | Value    |
| Practice |   ---►    | oriented |   ---►    | Lifecycle |   ---►   | Co-Creat |
| Library  |           | (7 books)|           | (5 stage)|          | (SVS)    |
+----------+           +----------+           +----------+          +----------+
   기능중심                프로세스중심            단계별              가치사슬+원리
                                                                +34 Practices
   IT-비즈니스 갭          정의서/체크리스트      RACI 매트릭스         VSM·FDO·CSI
```

- **📢 섹션 요약 비유**: ITIL v3가 마치 "출발->도착 정해진 철도 노선도"라면, ITIL 4는 "교통 상황에 따라 우회·병합 가능한 도시 도로 네트워크"와 같다. 도시 도로망(Value Chain)은 동일한 도시 목적(가치)을 위해 교통 흐름(Demand) 변화에 따라 신호·차선을 유연하게 재배치한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ITIL 4의 근간인 **Service Value System(SVS)**는 다음 5대 구성요소로 이루어진다: ① Guiding Principles(7개), ② Governance(3개 활동: Evaluate/Direct/Monitor/Continual Improvement), ③ Service Value Chain(6개 활동), ④ Practices(34개), ⑤ Continual Improvement(7단계 모델). 이 5요소가 Opportunity/Demand -> Value 변환 엔진으로 통합 동작한다.

```text
[ITIL 4 Service Value System (SVS) 아키텍처]

                          +----------------------+
                          |   OPPORTUNITY /      |
                          |      DEMAND          |
                          |  (Trigger/Input)     |
                          +----------+-----------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
              v                      v                      v
    +------------------+   +------------------+   +------------------+
    |  ORGANIZATION    |   |  4 DIMENSIONS    |   |   PESTEL/        |
    |  & PEOPLE        |   |  (PEST, IT, PS,  |   |   External       |
    |                  |   |   VSP)           |   |   Factors        |
    +--------+---------+   +----------+-------+   +--------+---------+
             |                        |                     |
             +------------+-----------+---------------------+
                          |
                          v
        +--------------------------------------------+
        |        SERVICE VALUE SYSTEM (SVS)         |
        |                                            |
        |  +--------------------------------------+  |
        |  |  7 GUIDING PRINCIPLES (FOCUS/CSPK)   |  |
        |  +--------------------------------------+  |
        |                  |                         |
        |  +---------------v----------------------+  |
        |  |       GOVERNANCE (EDM)              |  |
        |  |   Evaluate / Direct / Monitor       |  |
        |  +---------------+----------------------+  |
        |                  |                         |
        |  +---------------v----------------------+  |
        |  |    SERVICE VALUE CHAIN (6 Activity) |  |
        |  |  +-----+-----+-----+-----+-----+   |  |
        |  |  |Plan |Impv |Eng  |D&T  |O/B  |D&S |   |  |
        |  |  +-----+-----+-----+-----+-----+   |  |
        |  |         ↕ 34 Practices              |  |
        |  +---------------+----------------------+  |
        |                  |                         |
        |  +---------------v----------------------+  |
        |  |   CONTINUAL IMPROVEMENT (7-step)    |  |
        |  +--------------------------------------+  |
        +------------------------------------------+
                          |
                          v
                +----------------------+
                |       VALUE          |
                |  (Utility+Warranty   |
                |   +Experience)       |
                +----------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Guiding Principles (7개)** | 의사결정·행동의 지침 | Focus on value / Start where you are / Progress iteratively with feedback / Collaborate and promote visibility / Think and work holistically / Keep it simple and practical / Optimize and automate. 각 원칙은 모든 Practice/Value Chain 활동에 보편 적용되며, "Universal, Enduring, Self-validating" 속성 보유 |
| **Service Value Chain (6 Activity)** | Value Orchestration 엔진 | Plan(전략·포트폴리오), Improve(CSI 7-step), Engage(Stakeholder·User), Design & Transition(서비스 설계·릴리스), Obtain/Build(컴포넌트 조달), Deliver & Support(운영). Backlog 기반 동시실행 가능, DevOps CI/CD와 직접 매핑(D&T↔CI/CD Pipeline, O/B↔IaC, D&S↔Run/SRE) |
| **34 Practices** | 14 General + 17 Service + 3 Technical Management | General: Architecture Mgmt, Continual Improvement, Information Security Mgmt, Knowledge Mgmt 등. Service: Incident Mgmt, Problem Mgmt, Service Request Mgmt, Change Enablement, Service Level Mgmt, Monitoring & Event Mgmt, Release Mgmt, Service Configuration Mgmt, IT Asset Mgmt, Service Catalogue Mgmt, Service Design, Service Desk, etc. Technical: Deployment Mgmt, Infrastructure & Platform Mgmt, Software Dev & Mgmt |
| **4 Dimensions** | Holistic 관점 보장 | ① Organizations & People(구조·역량·문화), ② Information & Technology(데이터·도구), ③ Partners & Suppliers(SIAM·계약), ④ Value Streams & Processes(워크플로우). PEST+VSP 약자로 기억 |
| **Governance (EDM)** | 방향성·통제 | Evaluate(전략 진단) -> Direct(정책·우선순위 부여) -> Monitor(성과·컴플라이언스 측정). ISO 38500 IT Governance 표준과 직접 매핑 |

**Service Value Chain 6개 활동의 DevOps/SRE 매핑 세부:**

- **Plan** ↔ Sprint Planning, OKR, Epic/Feature Roadmap, FinOps Budget Planning
- **Improve** ↔ Retrospective, Blameless Postmortem, Chaos Engineering Results, Kaizen Event
- **Engage** ↔ Customer Success Platform(Totango/Gainsight), User Story Backlog Grooming, SLA Negotiation
- **Design & Transition** ↔ CI/CD Pipeline, SRE Error Budget Policy, IaC(Terraform/Ansible) + GitOps(ArgoCD/Flux)
- **Obtain/Build** ↔ Container Image Build(Dockerfile/Buildpacks), SBOM(Syft/CycloneDX), Package Registry(Harbor/Artifactory)
- **Deliver & Support** ↔ SRE Golden Signals(Latency/Traffic/Errors/Saturation), Observability Stack(Prometheus+Grafana+Loki+Tempo), Incident Response, On-call Rotation(PagerDuty/Opsgenie)

**Continual Improvement 7단계 모델(구 v3 CSI 7-step 통합):** ① What is the vision? ② Where are we now? ③ Where do we want to be? ④ How do we get there? ⑤ Take action ⑥ Did we get there? ⑦ How do we keep the momentum? — 각 단계별 KPI/CMS(Critical Success Factor/Key Performance Indicator/Key Result Indicator) 측정 프레임워크 적용.

- **📢 섹션 요약 비유**: SVS는 마치 "5성급 호텔의 Total Service System"과 같다. Guiding Principles는 '고객 우선' 철학, Service Value Chain은 체크인->룸서비스->체크아웃의 활동 흐름, Practices는 세탁·식음·컨시어지 같은 부서별 전문 서비스, 4 Dimensions는 직원·시설·협력업체·운영프로세스를 모두 보는 경영 시야, Governance는 호텔의 품질 감찰과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | **ITIL v3/2011 (Lifecycle)** | **ITIL 4 (SVS/Value Chain)** |
| :--- | :--- | :--- |
| 구조 | 5단계 Lifecycle(SDLC 유사, Stage-Gate) | 6개 Value Chain Activity(반복·동시 실행) |
| 핵심 단위 | Process(절차·RACI·입력->출력) | Practice(목표·원리·역량·도구 통합) |
| 가치 정의 | Service = Utility(What) + Warranty(How) | Value = Utility + Warranty + **Experience(Holistic)** |
| DevOps 친화성 | 낮음(Stage-gate가 CI/CD 충돌) | 높음(Value Chain이 Backlog 기반) |
| Agile/Lean 지원 | 약함 | 강함(Guiding Principle "Progress iteratively with feedback" 내재화) |
| 거버넌스 연계 | 별도 Cobit 연계 | EDM Governance가 내장, ISO 38500·20000·27001과 직접 매핑 |

| 구분 | **ITIL 4** | **COBIT 2019** | **ISO 20000-1:2018** |
| :--- | :--- | :--- | :--- |
| 목적 | 서비스 가치 창출 프레임워크 | IT 거버넌스·관리 목표 체계 | ITSM 인증 표준(SMS 요구사항) |
| 범위 | 34 Practices + 6 Value Chain | 40 Governance/Management Objectives | 10 Clause 요구사항 |
| 인증 | PeopleCert ITIL Foundation~Master | ISACA COBIT 2019 Foundation/Design/Implement | BSI/ANAB ISO 20000 Auditor |
| 상호보완 | "How to" 운영 베스트프랙티스 | "What to achieve" 목표/지표 | "Conformity" 인증·감사 기준 |
| 연계 사례 | COBIT의 EDM이 ITIL 4 Governance EDM과 동일 | ITIL Practice가 COBIT의 Management Objective 수행 수단 | ITIL 4를 구현한 결과가 ISO 20000 인증 요건 충족 |

| 구분 | **ITIL 4 Practice** | **ITSM Tool 기능 (ServiceNow/Jira SM)** |
| :--- | :--- | :--- |
| Incident Mgmt | L1~L4 프로세스·전사 인시던트 정책 | Incident Ticket Workflow, Major Incident War Room, PagerDuty 연동 |
| Change Enablement | RFC->CAB->PIR 사이클, Standard/Normal/Emergency 분류 | Change Request, CAB Board, Risk Score, Auto-approval Rule(50% 이상 자동화) |
| Problem Mgmt | KEDB(Known Error DB), RCA(5-Why/Ishikawa) | Problem Ticket ↔ Incident Link, KEDB Article, RCA Template |
| Service Request Mgmt | 카탈로그 기반 셀프서비스, 사전 승인 SLA | Service Portal, Catalog Item, Approval Policy, FCR Dashboard |
| Monitoring & Event Mgmt | Event->Alert->Incident 변환 정책, Threshold | Prometheus Alertmanager ↔ ITSM Webhook, AIOps(moogsoft/BigPanda) |

**다른 프레임워크와의 연결 매핑:**

- **DevOps/SRE** ↔ Obtain/Build + Design & Transition + Deliver & Support Value Chain Activity, SRE Error Budget이 Warranty의 Availability 정의와 직결
- **Agile (SAFe/LeSS/Spotify)** ↔ Plan + Improve + Engage Activity, Product Backlog = Service Backlog, PI Planning = Service Portfolio Review
- **SIAM (Sourcing Integration And Management)** ↔ 4 Dimensions 중 "Partners & Suppliers" + Practices 중 "Supplier Mgmt", 다중 벤더 생태계 통합 거버넌스
- **FinOps** ↔ Plan Activity의 예산 수립 + Continual Improvement의 비용 최적화 KPI(클라우드 단위 비용/예산 편차 10% 이내)
- **Site Reliability Engineering(SRE)** ↔ Deliver & Support + Monitoring & Event Mgmt Practice, SLO/SLI가 SLA의 기술적 구현

- **📢 섹션 요약 비유**: ITIL v3가 "수술 매뉴얼(순서 엄격)"이라면 ITIL 4는 "응급실 프로토콜(상황별 동시 다발적 대응)"이다. COBIT는 "환자 치료 목표 달성 체크리스트", ISO 20000은 "병원 인증 심사 기준", ServiceNow는 "전자의무기록 시스템"에 비유할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### ITIL 4 도입 실무 전략 (4-Wave 모델)

1. **Wave 1 (0~3개월): As-Is 진단 및 Quick Win** — Service Value Chain Value Stream Mapping(VSM)을 통해 "Incident 발생 -> 복구" 까지의 Lead Time, Process Time, %C&A(% Complete & Accurate)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 506 / 600

<- **이전**: [505. COBIT 거버넌스 관리 프레임워크](/studynote/11_design_supervision/06_exam_summary/506_cobit_governance_management_framework/)
**다음**: [507. ISO 20000 IT 서비스 표준](/studynote/11_design_supervision/06_exam_summary/507_iso_20000_it_service_standard/) ->

---
