+++
title = "428. 문제 관리 근본 원인 분석 RCA (Problem Management Root Cause Analysis)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ITIL 4 문제 관리(Problem Management) 체계에서 다수 Incident의 공통 근본 원인을 식별·제거하기 위해 5 Whys, Ishikawa Fishbone, Fault Tree Analysis(FTA), Pareto, Kepner-Tregoe 등의 구조적 분석 기법과 AIOps 기반 상관관계 분석을 결합하여 KEDB(KE-DB)·CMDB·Change Management와 연동하는 운영 거버넌스 메커니즘
> 2. **가치**: 동일 root cause 기반 Incident 재발률을 60~80% 감소시키고, MTTR을 평균 35~50% 단축하며, MTTD(Mean Time To Detect)와 Known Error 활용률(Known Error Utilization Ratio)을 KPI로 관리하여 SLO/Error Budget 기반 SRE 문화와 결합된 가용성 99.95% 이상의 서비스 안정성 확보
> 3. **판단 포인트**: Reactive(사고 후) vs Proactive(사고 전) RCA의 균형, 조직의 Blameless Postmortem 수용성, AIOps/관측가능성(Observability) 투자 대비 효과, 그리고 단일 RCA 기법의 한계를 보완하기 위한 5 Whys + Fishbone + FTA + Data-driven Correlation의 하이브리드 적용 전략이 핵심 결정 요인

---

## Ⅰ. 개요 및 필요성

**Problem Management Root Cause Analysis(RCA)** 는 단순한 Incident 대응(Service Restoration)을 넘어, 다수의 유사 Incident를 유발하는 잠재 결함(Latent Defect)을 체계적으로 발굴·제거하기 위한 ITIL 4 Service Management Practice의 핵심입니다. 전통적 ITIL v2/v3에서는 Problem Manager가 Incident Trend 분석 후 수동으로 Known Error를 도출하는 Reactive 모델이 주를 이루었으나, 클라우드 네이티브·MSA 환경에서는 수천 개 마이크로서비스에서 발생하는 분산 트레이스와 메트릭·로그를 AIOps 플랫폼이 자동 상관분석(Correlation Analysis)하여 Anomaly Detection을 수행하고, SRE의 Error Budget 정책과 결합된 Proactive Problem Management로 진화하고 있습니다.

문제 관리의 본질은 "**증상(Symptom) 처리가 아닌 질병(Disease) 치료**"입니다. 1차 대응으로 Incident를 복구(Restoration)한 뒤, 동질 Incident의 클러스터링(예: 동일 ServiceNow CI·Configuration Item 단위)을 통해 Problem Record를 개설하고 RCA를 수행합니다. RCA 결과는 Known Error Database(KEDB)에 Workaround 형태로 축적되어, 동일 Incident 재접수 시 즉시 우회 처리(1st Line Self-Service)를 가능하게 합니다.

```text
+------------------------------------------------------------------+
|              Incident -> Problem -> RCA -> KEDB Lifecycle          |
+------------------------------------------------------------------+

   [End User]              [Service Desk]            [Problem Manager]
        |                        |                          |
        v                        v                          v
  +----------+  P1/P2    +--------------+  Clustered  +--------------+
  | Incident |----------->|  Incident    |------------->|   Problem    |
  |  Ticket  |           |  Management  |             |   Record     |
  +----------+           |  (Restoration)|            |   (RCA)      |
        |                +--------------+             +------+-------+
        |                          |                         |
        |                  +-------v--------+                v
        |                  |  Trend Analysis |        +--------------+
        |                  |  • CMDB CI      |        |  RCA Method  |
        |                  |  • Error Code   |        |  • 5 Whys    |
        |                  |  • Time Pattern |        |  • Fishbone  |
        |                  +-----------------+        |  • FTA       |
        |                                             |  • Pareto    |
        |                                             +------+-------+
        |                                                    |
        |                  +-----------------+                v
        +------------------>|   KEDB Update   |<-------+--------------+
                           |  • Workaround   |       |  Root Cause  |
                           |  • Root Cause   |       |  Identified  |
                           +---------+-------+       +--------------+
                                     |
                                     v
                           +-----------------+         +--------------+
                           | RFC(Request for |--------->|  Change Mgmt |
                           |    Change)      |         |  (CAB 승인)  |
                           +-----------------+         +------+-------+
                                                             |
                                                             v
                                                    +-----------------+
                                                    | Permanent Fix & |
                                                    |   Monitoring    |
                                                    +-----------------+
```

기존 패러다임(1990~2000년대)에서는 평균 해결 시간(MTTR) 단축에만 집중하여 "Reboot & Patch"식의 임시 대응이 반복되었고, 동일 root cause로 인한 Incident 재발률이 40~60%에 달했습니다. 현대 패러다임(2020년대~)은 Observability 3-Pillar(Metrics·Logs·Traces)와 AIOps의 Anomaly Detection·Root Cause Localization 알고리즘(예: Bayesian Network, Graph-based Causal Inference)을 결합하여, Incident 발생 5분 이내에 Probable Root Cause를 자동 추천하는 수준까지 발전했습니다. ISO/IEC 20000-1:2018(SMS 표준) Clause 8.5.2 및 ITIL 4 Service Value Chain의 "Engage/Obtain/Build" 단계에서도 Problem Management는 필수 통제 항목입니다.

- **📢 섹션 요약 비유**: Problem Management RCA는 마치 "같은 두통으로 매주 약만 먹는 환자"를 "MRI로 종양을 찾아 제거하는 의사"로 바꾸는 의료 패러다임 전환과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RCA 시스템은 **탐지(Detection) -> 데이터 수집(Data Aggregation) -> 분석(Analysis) -> 식별(Identification) -> 조치(Action) -> 학습(Learning)** 의 6단계 Closed-Loop로 구성되며, 각 단계는 CMDB·Observability Stack·ITSM Platform과 강하게 결합됩니다.

```text
+--------------------------------------------------------------------+
|                RCA Reference Architecture (ITIL 4 + AIOps)         |
+--------------------------------------------------------------------+

+--------------+    +--------------+    +--------------+
|  Observability|    |  CMDB        |    |  ITSM Tool   |
|  (Prometheus, |    |  (ServiceNow |    |  (ServiceNow |
|   Grafana,    |    |   CMDB,      |    |   ITSM,      |
|   ELK, Loki)  |    |   BMC ADDM)  |    |   Jira SM)   |
+------+-------+    +------+-------+    +------+-------+
       | Metrics           | CI 관계          | Ticket
       | Logs              | Topology         | Workflow
       | Traces            |                  |
       +--------+----------+----------+-------+
                |                     |
                v                     v
        +--------------------------------------+
        |       AIOps Correlation Engine       |
        |  • Anomaly Detection (ML/DL)         |
        |  • Event Correlation (Rule+ML)       |
        |  • Topology-aware RCA                |
        |  • Causal Inference (Bayesian/Graph) |
        +--------------+-----------------------+
                       | Probable Root Cause
                       v
        +--------------------------------------+
        |     RCA Method Selection Layer       |
        |  +--------+ +--------+ +--------+    |
        |  |5 Whys  | |Fishbone| |  FTA   |    |
        |  +--------+ +--------+ +--------+    |
        |  +--------+ +--------+ +--------+    |
        |  |Pareto  | |K-T     | |FMEA    |    |
        |  +--------+ +--------+ +--------+    |
        +--------------+-----------------------+
                       |
                       v
        +--------------------------------------+
        |  KEDB (Known Error Database)          |
        |  • Symptom -> Workaround Mapping      |
        |  • RFC Linkage                       |
        |  • Searchable Knowledge              |
        +--------------+-----------------------+
                       |
                       v
        +--------------------------------------+
        |  Change Management (CAB)              |
        |  • RFC Review                         |
        |  • Risk Assessment                    |
        |  • Implementation                     |
        +--------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Observability Layer** | 시스템의 내부 상태를 외부에서 관측 가능하게 만드는 데이터 수집 계층 | Prometheus(메트릭, PromQL), Grafana Loki(로그 집계), Grafana Tempo/Jaeger(분산 트레이싱, OpenTelemetry 기반), eBPF 기반 Kernel-level Observability(Pixie, Cilium Tetragon) |
| **CMDB (Configuration Management DB)** | 서비스·서버·네트워크·앱 간 의존성 관계(IaaS, PaaS, SaaS, CI Relationship) 보관 | ServiceNow CMDB(Identification & Reconciliation Engine), BMC Atrium/ADDM(Application Dependency Mapping), Device42, i-do-it. 관계 타입: Depends On, Runs On, Connects To, Installed On |
| **AIOps Correlation Engine** | 대량의 Alert/Event를 클러스터링하고, 토폴로지 기반으로 Root Cause를 자동 추정 | Algorithmic: Pearson/Spearman 상관분석, Granger Causality, Bayesian Network. ML: Isolation Forest, DBSCAN, LSTM Autoencoder. Vendor: Moogsoft, Splunk ITSI, Datadog Watchdog, New Relic AI, Dynatrace Davis(Deterministic AI) |
| **RCA Method Set** | 구조적 사고 프레임워크를 제공하여 인적 분석의 일관성·재현성 확보 | 5 Whys(선형 인과 추적), Ishikawa Fishbone(6M: Man/Machine/Material/Method/Measurement/Mother Nature), FTA(Fault Tree Analysis, IEC 61025, Boolean Logic AND/OR Gates), FMEA(Failure Mode and Effects Analysis, RPN=Risk Priority Number = S×O×D), Pareto(80/20 누적 기여도) |
| **KEDB (KE-DB)** | 검증된 Known Error와 Workaround를 표준화된 형식으로 저장·검색 | ServiceNow Known Error Module(sn_km_kmdb), BMC Remedy Known Error, Confluence 통합, AI Search(NLP 기반 Symptom-to-KE Matching, BERT Embedding) |
| **Problem Record Lifecycle** | Problem Ticket의 Open -> Investigating -> RCA in Progress -> Known Error -> Closed 상태 전이 관리 | 상태 머신(State Machine) 기반, SLA Timer 연동(P1: 4시간 내 RCA 착수), Assignment Rule(라운드로빈 또는 Skill-based Routing) |
| **Change/Problem Integration** | RCA 결과의 영구 해결책이 RFC(Request For Change)로 변환되어 CAB 승인 후 적용 | ServiceNow Change Management(Standard/Normal/Emergency), Pre/Post Implementation Review, Backout Plan 검증 |

**핵심 알고리즘 및 정량 파라미터**:
- **5 Whys**: 단일 인과 사슬(Linear Causal Chain)을 5회 반복 질의. 효과적 적용 조건은 "원인이 단일 시스템·단일 팀에 국한"될 때이며, MSA 환경에서는 4M+E(Man, Machine, Method, Material, Environment) 카테고리로 확장 필요
- **Pareto Analysis**: 80/20 법칙을 Incident 분류에 적용. 예: 100건 중 20건의 Error Code가 전체의 80% 차지 -> 해당 20건 우선 RCA 대상. 정량화: 누적 기여도 = Σ(건수) / Σ(전체 건수) × 100
- **FTA (Fault Tree Analysis)**: Top Event(예: "결제 서비스 다운") -> 중간 이벤트 -> Basic Event로 분해. OR Gate(어떤 하나라도 발생 시), AND Gate(모든 입력 발생 시)로 Boolean 표현. 정성적 분석(MCS: Minimal Cut Set) + 정량 분석(확률 계산)
- **FMEA**: RPN(Risk Priority Number) = Severity(1~10) × Occurrence(1~10) × Detection(1~10). RPN ≥ 100 또는 S ≥ 9인 항목은 즉시 대응 대상
- **AIOps Causal Graph**: Service Dependency Graph를 Bayesian Network로 모델링, Conditional Probability P(Cause|Evidence) 최대화 노드를 Root Cause로 추정. Dynatrace Davis는 토폴로지 결정론 + 유사도 분석으로 MTTD < 1분 달성
- **Known Error Utilization Ratio(KEUR)**: KEDB 조회 후 Incident 해결 비율. 목표: ≥ 30%. KPI 산식: (KE 적용 Incident 수) / (동일 Error Code Incident 수) × 100
- **Problem Resolution Rate(PRR)**: (Closed Problem) / (Opened Problem) × 100. SLA: P1 90% / 30일, P2 85% / 60일

- **📢 섹션 요약 비유**: RCA 아키텍처는 마치 "인체의 CT·MRI·혈액검사 결과를 종합 분석하여 종양의 정확한 위치를 찾아내는 진단 키트"와 같으며, AIOps는 그 키트를 자동으로 작동시키는 AI 보조 진단 시스템입니다.

---

## Ⅲ. 비교 및 연결

RCA는 인접 ITIL 프로세스(Incident, Change, Knowledge, Availability) 및 다른 분석 기법(Postmortem, Chaos Engineering)과 명확한 경계와 시너지를 가집니다.

| 구분 | **Problem Management RCA** | **Incident Postmortem (SRE)** | **Change Failure Analysis** | **Chaos Engineering** | **Risk Assessment** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | 반복 Incident의 근본 원인 영구 제거 | 단일 Major Incident의 학습·개선 | 변경(Change) 자체의 실패 원인 분석 | 사전 주입 장애로 Resilience 검증 | 변경/신규 시스템의 잠재 리스크 식별 |
| **시점** | Incident 발생 후 (Reactive) 또는 Trend 기반 (Proactive)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 428 / 800

<- **이전**: [427. 인시던트 관리 에스컬레이션 대응](/knowledge-base/studynote/12_it_management/05_security_compliance/427_incident_management_escalation_response/)
**다음**: [429. SLA 서비스 수준 관리 SLO SLI](/knowledge-base/studynote/12_it_management/05_security_compliance/429_sla_service_level_management_slo_sli/) ->

---
