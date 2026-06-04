---
title: "605. IT 경영 관리 핵심 토픽 605번 시험 요약 (IT Management Core Topic 605 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(605)는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 거버넌스 프레임워크를 기반으로 IT 전략-투자-운영-성과의 Value Chain을 통합 관리하며, BCM·ISMS·ESG·DEVOPS를 아우르는 End-to-End 거버넌스 체계를 구축하는 것이 핵심이다.
> 2. **가치**: 성숙도 모델(예: COBIT 5단계, CMMI 5단계) 적용 시 IT 투자 ROI 평균 25~35% 개선, ITSM 운영 비용 20~40% 절감, 의사결정 리드타임 60% 단축, 그리고 ISO 27001·PIPC·전자금융감독규정 등 컴플라이언스 동시 충족을 통한 리스크 노출 50% 이상 감소 효과를 달성한다.
> 3. **판단 포인트**: Build vs. Buy vs. Outsource, 중앙집중(Centralized) vs. 페데레이션(Federated) vs. 코어-스폰서(Core-Sponsored) 조직모델, CAPEX/OPEX 스위칭, 워터폴 vs. 애자일 vs. 하이브리드(SAFe) 방법론 선택, Zero Trust vs. Defense-in-Depth 보안 아키텍처가 핵심 Trade-off이며, 기술사 답안에서는 항상 ① Business Value ② Risk ③ Compliance ④ Total Cost of Ownership 4축 정량 분석을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 트랜스포메이션(DX) 가속화, 생성형 AI(GenAI)·클라우드 네이티브·제로트러스트 등 패러다임 전환, 그리고 ESG·PIPC(개인정보보호법)·DORA(디지털운영복원력법) 같은 규제 강화로 인해 IT는 단순 Cost Center에서 **Value Driver**이자 **Strategic Asset**으로 격상되었다. 605번 토픽은 이러한 환경에서 CIO·CDO·CISO가 통합적으로 의사결정할 수 있는 **IT 거버넌스(Governance)–관리(Management)–운영(Operations) 3계층 프레임워크**를 설계·검증·최적화하는 역량을 평가한다.

과거(2000년대)에는 ITIL v2/v3의 프로세스 중심, SAS 70/SSAE 16 중심의 통제 환경이 주류였으나, 현재(2024~2026)는 클라우드·SaaS·DevSecOps·AI 윤리·공급망 리스크(SolarWinds, Log4j, XZ Utils 사례) 등으로 인해 **연속적 통제 모니터링(Continuous Control Monitoring, CCM)** 과 **자동화된 거버넌스(Governance as Code)** 패러다임이 요구된다.

```text
   +------------------------------------------------------------------------+
   |          605. IT 경영 관리 3-Layer Governance Reference Model          |
   +------------------------------------------------------------------------+
   +------------------- 1. 전략/거버넌스 계층 (Strategy & Governance) ------+
   |  +--------------+  +--------------+  +--------------+  +------------+  |
   |  | ISO/IEC 38500|  |  COBIT 2019  |  |   King IV    |  |   COSO ERM |  |
   |  |  (이사회 IT  |  |  (40 Governance| |  (남아공 IT  |  |  (전사 리스크|  |
   |  |  거버넌스)   |  |   Objectives) |  |   거버넌스)  |  |   관리)    |  |
   |  +------+-------+  +------+-------+  +------+-------+  +-----+------+  |
   |         +----------+------+----------+------+                |         |
   |                    v                 v                       v         |
   |            +---------------------------------------------------+        |
   |            |  Strategic Alignment (SAM: Henderson & Venkatraman)|        |
   |            |  IT Strategy ↔ Business Strategy 양방향 정렬       |        |
   |            +---------------------+-----------------------------+        |
   +------------------------------+--------------------------------------+
                                  v
   +------------------- 2. 관리/전환 계층 (Management & Transformation) ----+
   |  +------------+  +------------+  +------------+  +-----------------+  |
   |  |  ITIL 4    |  |  TOGAF 10  |  |  BPM CBOK  |  |  Design Thinking|  |
   |  | (Service  |  | (ADM Cycle:|  |  (프로세스 |  |  + Lean Startup |  |
   |  |  Value Sys)|  | A->B->C->D->E-> |  |   최적화)  |  |  (DX 방법론)   |  |
   |  | SVS:OPP->  |  | F->G->H     |  |            |  |                 |  |
   |  | Value->     |  |  ADM)      |  |            |  |                 |  |
   |  | Organiz.   |  |            |  |            |  |                 |  |
   |  +-----+------+  +-----+------+  +-----+------+  +------+----------+  |
   |        +-------+-------+-------+------+                 |             |
   |                v               v                        v             |
   |       +--------------------------------------------------------+       |
   |       | Portfolio/Program/Project (PMO 3-Layer)               |       |
   |       | PRINCE2 / PMP / SAFe / MSP Hybrid Delivery Governance |       |
   |       +------------------------+-------------------------------+       |
   +--------------------------------+--------------------------------------+
                                    v
   +------------------- 3. 운영/실행 계층 (Operations & Execution) ---------+
   |  +------------+  +------------+  +------------+  +-----------------+  |
   |  |  DevSecOps |  |  AIOps /   |  |  FinOps    |  |  SRE (SLO/SLI/  |  |
   |  |  CI/CD/CT  |  |  Observ.   |  |  Cloud Cost|  |  Error Budget)  |  |
   |  |  SBOM/    |  |  OpenTelemetry| |  Optimization| |  Runbook Auto.  |  |
   |  |  Sigstore |  |  ELK/EFK    |  |  Showback   |  |  Chaos Eng.     |  |
   |  +-----+------+  +-----+------+  +-----+------+  +------+----------+  |
   |        +-------+-------+-------+------+                 |             |
   |                v               v                        v             |
   |       +--------------------------------------------------------+       |
   |       |  Continual Improvement (CSI) + Control Objectives        |       |
   |       |  -> COBIT 2019 ↔ ITIL 4 Practice ↔ ISO 27001 A.5~A.18  |       |
   |       +--------------------------------------------------------+       |
   +------------------------------------------------------------------------+
```

**왜 필요한가? (Old vs New Paradigm)**

| 구분 | 2000년대 전통 IT 관리 | 2024~2026 현대 IT 경영 관리 (605) |
| :--- | :--- | :--- |
| 관점 | IT = 비용(Cost Center), Backsourcing | IT = 가치 창출(Value Driver), Anything as a Service(XaaS) |
| 통제 | 정적(SAS 70, 수기 점검, 연 1회 감사) | 동적(Continuous Auditing, GaC, Policy as Code) |
| 방법론 | 워터폴(Waterfall) 독점, Big-Bang 배포 | 애자일/SAFe/DevSecOps, 점진적·지속적 배포(Blue/Green, Canary) |
| 보안 | 경계 기반(Perimeter, Firewall 중심) | Zero Trust(Identity-Centric, mTLS, BeyondCorp) |
| 아키텍처 | 모놀리식(On-Prem Monolith) | 클라우드 네이티브(Microservice, K8s, Service Mesh) |
| 의사결정 | CIO 단독, Top-Down | RACI 매트릭스, Federated Governance, Data-Driven |
| 성과측정 | 가용성(Uptime), MTBF/MTBF | NPS, CX, Time-to-Market, Cloud FinOps ROI, MTTR, SRE Golden Signals |
| 리스크 | BCP 단순 DR | BCM(ISO 22301), DORA, 공급망 SBOM·CVE 기반 실시간 대응 |

- **📢 섹션 요약 비유**: IT 경영 관리는 **"배의 키잡이(Rudder)"** 와 같다. 엔진(기술)·돛(프로세스)·선원(사람)이 아무리 좋아도, 키잡이(거버넌스)가 없으면 배는 표류한다. 또한 요즘 배는 **자동조종장치(AI·자동화)** 와 **항해지도 실시간 업데이트(Continuous Compliance)** 가 필수인 무인선박 시대다.

---

## Ⅱ. 아키텍처 및 핵심 원리

605번 토픽의 핵심은 **"목표 정렬 -> 가치 측정 -> 통제 -> 개선"** 의 4단 Value Loop를 거버넌스·관리·운영 3계층에 매핑하는 것이다. 아래는 ISO/IEC 38500 + COBIT 2019 + ITIL 4를 통합한 **"IT 경영 관리 4A Framework"** 의 상세 아키텍처이다.

```text
   +----------------------------------------------------------------------+
   |       4A Framework: Align -> Architect -> Assure -> Adapt              |
   |  (전략-구조-통제-개선 루프, 605번 문제의 표준 답안 골격)             |
   +----------------------------------------------------------------------+
        +------------------------------------------------------------+
        |  STEP 1. ALIGN (전략 정렬) — ISO/IEC 38500 6 원칙 적용     |
        |  ①Responsibility ②Strategy ③Acquisition ④Performance     |
        |  ⑤Conformance ⑥Human Behavior                              |
        +---------------------+--------------------------------------+
                              v
        +------------------------------------------------------------+
        |  STEP 2. ARCHITECT (구조 설계) — TOGAF ADM + EA Capability  |
        |  Business Arch -> Data Arch -> App Arch -> Tech Arch         |
        |  + Capability-Based Planning (TOGAF Standard 10)           |
        +---------------------+--------------------------------------+
                              v
        +------------------------------------------------------------+
        |  STEP 3. ASSURE (통제/감사) — COBIT 2019 + ISO 27001:2022  |
        |  40 Governance Objective × 5 Domain(EDM/APO/BAI/DSS/MEA)  |
        |  + 통제 매핑: NIST CSF 2.0 / ISO 27001 A.5~A.18           |
        +---------------------+--------------------------------------+
                              v
        +------------------------------------------------------------+
        |  STEP 4. ADAPT (개선/혁신) — ITIL 4 CSI + Lean-Agile       |
        |  PDCA -> OODA Loop -> Double-Loop Learning                  |
        |  (피드백 반영 후 거버넌스 원칙 자체도 갱신)                 |
        +---------------------+--------------------------------------+
                              |
                              +------► (STEP 1로 피드백) [Continuous Loop]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/IT Steering Committee** | IT 거버넌스 최상위 의사결정, ISO 38500 "Evaluate–Direct–Monitor" 사이클 수행 | 정기 분기 회의, eGRC 플랫폼(Archer, ServiceNow GRC, SAP GRC) 기반 대시보드, RACI 매트릭스 승인권한 정의, Quorum 기반 의결(과반수 + 독립이사 1/3 이상) |
| **CIO / CDO / CISO 트라이어드** | 전략-데이터-보안 3대 책임자, Federated 모델에서 각 BU(사업부)와 공동 의사결정 | CDO는 Data Mesh·Data Product·Data Catalog(Great Expectations, Unity Catalog) 운영, CISO는 Zero Trust·CTI(Cyber Threat Intelligence)·Red Team, CIO는 IT-Business Value Bridge(BSC 4관점) 관리 |
| **EA(Enterprise Architecture) Office** | TOGAF ADM 8단계(또는 10 표준) 수행, Capability Map·Gap 분석·Roadmap 산출 | ADM Cycle: Preliminary->A(Vision)->B~D(아키텍처)->E(기회)->F(계획)->G(거버넌스)->H(변경관리). 산출물: Architecture Vision, Target State, Transition Architecture, Implementation Governance |
| **PMO(Program/Project Mgmt Office)** | 프로젝트 포트리오 우선순위·자원배분·리스크 통합 관리 | P3M3(Portfolio, Programme, Project Management Maturity Model) 5단계, 자원 평준화(Resource Leveling) 알고리즘, Earned Value Mgmt(EVM: CPI, SPI, EAC), 게이트별 Stage-Gate Review |
| **ITSM(Service Management)** | 서비스 카탈로그·인시던트·문제·변경·릴리즈·구성 관리 | ITIL 4 Service Value System(SVS): Opportunity/Demand->Value-> 조직/인폼/파트너-> 34개 Practice. ITSM 도구: ServiceNow, BMC Helix, Jira Service Management. 주요 KPI: First Call Resolution, SLA Compliance, MTTR |
| **DevSecOps 파이프라인** | 코드->빌드->테스트->배포->모니터링 전 단계에 보안·컴플라이언스 자동 삽입 | Plan->Code(SAST: SonarQube, Semgrep)->Build(SCA: Snyk, OWASP Dep-Check)->Test(DAST: OWASP ZAP)->Release(Sigstore, Cosign, SBOM CycloneDX/SPDX)->Deploy(IaC: Terraform + OPA/Conftest Policy as Code)->Operate(Observability: OpenTelemetry, Prometheus, Grafana, Loki) |
| **BCM(Business Continuity Mgmt)** | BCP/DR 계획 수립 및 테스트, ISO 22301 / DORA 준수 | BIA(Business Impact Analysis) -> RTO/RPO/MTPD 산출 -> DR 전략(Active-Active, Pilot Light, Warm Standby, Backup/Restore) -> 매년 1회 이상 실전 모의훈련(GameDay) |
| **FinOps / ITAM** | IT 비용 가시화·최적화, 라이선스 컴플라이언스, Green IT | FinOps Framework: Inform->Optimize->Operate(3단계), Showback/Chargeback 모델, Reserved Instance·Savings Plan·Spot Instance 혼합, ITAM: ISO 19770 (SAM), CMDB 일치율 95% 이상 |
| **GRC(Governance, Risk, Compliance)** | 통합 리스크·컴플라이언스 관리, 자동 통제 모니터링(CCM) | eGRC 플랫폼(Archer, ServiceNow IRM, OneTrust) + CCM(Curious Panda, SAP GRC Process Control). 규제: PIPC, 전자
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 605 / 800

<- **이전**: [604. IT 경영 관리 핵심 토픽 604번 시험 요약](/studynote/12_it_management/05_security_compliance/604_it_management_core_topic_604_exam_summary/)
**다음**: [606. IT 경영 관리 핵심 토픽 606번 시험 요약](/studynote/12_it_management/05_security_compliance/606_it_management_core_topic_606_exam_summary/) ->

---
