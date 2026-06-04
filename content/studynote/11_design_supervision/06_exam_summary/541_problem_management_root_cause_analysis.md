---
title: "541. 문제 관리 근본 원인 분석 RCA (Problem Management Root Cause Analysis)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 문제 관리(Problem Management)는 반복 발생하는 인시던트(Incident)의 근본 원인(Root Cause)을 과학적 분석 기법(5 Whys, Fishbone, FTA 등)으로 규명하여 Known Error DB(KEDB)에 영구 지식으로 축적하고, RFC(Change Request)를 통해 구조적 해결(Permanent Fix)을 수행하는 ITIL Service Operation의 핵심 프로세스임. 단순히 **"왜 1번이 고장났는가"**(Incident)를 다루는 것이 아니라 **"왜 1번이 반복 고장나는가"**(Problem)의 인과 체인(Causal Chain)을 추적하는 Proactive 거버넌스임.
> 2. **가치**: McKinsey & Gartner 보고 기준, 효과적인 Problem Management 운영 시 인시던트 재발률 35~60% 감소, MTTR(Mean Time To Repair) 평균 40% 단축, IT 운영 비용(OpEx) 약 25% 절감이 가능하며, SRE(Site Reliability Engineering) 환경에서는 Error Budget 보존 및 Toil Elimination의 기초 자료로 활용됨.
> 3. **판단 포인트**: Reactive(사후 대응) ↔ Proactive(사전 예방) 운영 비중의 균형, RCA 기법 선택 시 문제 도메인(네트워크/DB/애플리케이션/인프라)에 따른 정성/정량 분석의 조합, 그리고 KEDB ↔ CMDB(CI 관계성) ↔ Change Management 간 데이터 정합성 확보가 시스템 신뢰성의 핵심 분기점임.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 운영 환경에서는 운영팀이 사용자 신고(Help Desk Ticket) 기반으로 장애를 처리하는 **"Fire-fighting(소방수)"** 방식에 의존했음. 이 방식은 SLA(Service Level Agreement) 기준 복구(Time-to-Recover)는 충족할 수 있으나, 동일한 결함(Cause)이 임의의 시간·장소에서 반복적으로 발생하는 **"Whack-a-Mole(두더지 잡기)"** 현상을 야기함. IT Infrastructure Library(ITIL) v2(2001년)부터 Problem Management는 Incident Management와 분리된 독립 프로세스로 정립되었으며, v3(2007년) 및 v4(2019년)에서는 **"사전 예방 및 가치 공동창조(Value Co-creation)"**의 핵심 축으로 재정의됨.

현대 MSA(Microservices Architecture) 환경에서는 단일 서비스의 결함이 200여 종의 의존 서비스로 전파(Cascading Failure)될 수 있어, RCA의 정확도가 곧 **전체 시스템 회복탄력성(Resilience)**을 결정함. ISO/IEC 20000(2018), COBIT 2019, DevOps Research and Assessment(DORA) 4 Keys Metrics 중 **Mean Time to Restore(MTTR)** 및 **Change Failure Rate(CFR)** 개선의 전제 조건이 체계적 RCA임.

```text
[ Reactive vs Proactive IT 운영 패러다임 비교 ]

  +--------------------------------------+   +--------------------------------------+
  |       Legacy "Fire-fighting" 운용    |   |   ITIL-Aligned Proactive 운용         |
  |                                      |   |                                      |
  |  User ---> Help Desk ---> L1/L2 Eng    |   |  Monitor ---> Event Mgmt ---> Problem  |
  |                |                     |   |    |                          |       |
  |                v                     |   |    v                          v       |
  |            임시 복구(Restart)         |   |  Threshold 분석              RCA 기법 |
  |                |                     |   |    |                          |       |
  |                v                     |   |    v                          v       |
  |            동일 장애 재발             |   |  KEDB 축적 ---> RFC ---> Permanent Fix|
  |                                      |   |                                      |
  |  ❌ 증상치료(Symptom)                |   |  ✅ 원인치료(Cause)                  |
  |  ❌ MTTR 누적 증가                   |   |  ✅ MTTR 추세 감소                   |
  |  ❌ Knowledge 유실                   |   |  ✅ Knowledge 자산화                 |
  +--------------------------------------+   +--------------------------------------+
```

**전통적 방식 대비 새로운 패러다임의 기술적 차별점**은 다음 4가지로 요약됨:

1. **Event -> Alert -> Incident -> Problem**의 계층적 상관관계 분석(Correlation Analysis)을 통한 노이즈 제거
2. **Post-Mortem(사후 분석)** 의 무관용 문화(Just Culture) 도입으로 blameless 환경 조성
3. **Topology-aware RCA**: CMDB의 CI(Configuration Item) 관계 그래프를 활용한 의존성 매핑
4. **ML/LLM 기반 AIOps**: 반복 패턴 자동 클러스터링(예: Moogsoft, BigPanda, ServiceNow ITSM Predictive Intelligence)

- **📢 섹션 요약 비유**: 증상 치료만 하는 방식은 "감기에 걸릴 때마다 해열제만 먹는 것"과 같고, 진정한 Problem Management는 "왜 자주 감기에 걸리는지(면역력 문제)를 진단해 생활 습관까지 개선하는 것"입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ITIL v4 기반 Problem Management는 **Problem Lifecycle** 7단계로 구성되며, 각 단계는 명확한 입출력(Input/Output) 데이터 객체와 책임 주체(RACI: Responsible, Accountable, Consulted, Informed)를 가짐. 특히 v4에서는 **"Service Value System(SVS)"**의 일환으로 4가지 활동(Engage, Design & Transition, Obtain/Build, Deliver & Support)과 통합됨.

```text
[ Problem Management Process Flow - ITIL v4 기준 ]

   +----------------+
   | 1. Problem      | <--- Event Mgmt(AIOps), Incident Trend, Supplier Alert
   |    Detection    |
   +--------+-------+
            v
   +----------------+         +-----------------+
   | 2. Problem      |--------->|  CMDB 동기화    | (CI Impact Relation)
   |    Logging      |         |  Ticket Linking |
   +--------+-------+         +-----------------+
            v
   +----------------+
   | 3. Problem      | <--- Priority Matrix: Impact(#Users) × Urgency(Business Loss)
   |    Categorization|      Category: HW | SW | NW | DB | App | Security
   |    & Prioritize |      Sub-category 예: DB-Lock-Wait, NW-DNS-Resolve
   +--------+-------+
            v
   +----------------+
   | 4. RCA          | <--- 기법 선택: 5-Whys | Fishbone | FTA | Pareto | KT
   | (Investigation) |      Evidence: Log, Packet Capture, APM Trace, Core Dump
   +--------+-------+
            v
   +----------------+         +-----------------+
   | 5. Workaround   |--------->| KEDB Publish    | (Known Error Database)
   |    & Known Error|         | Self-Service KB |
   +--------+-------+         +-----------------+
            v
   +----------------+
   | 6. RFC(Change)  | ---> Change Management ---> CAB/ECAB 승인 ---> Permanent Fix
   |    Raised       |
   +--------+-------+
            v
   +----------------+
   | 7. Problem      | <--- Post-Implementation Review, Effect 확인 (30/60/90일)
   |    Closure      |
   +----------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Problem Detection** | 인시던트 패턴/이벤트 분석을 통한 잠재 문제 식별 | AIOps Event Correlation(예: PagerDuty Event Rules, Splunk ITSI Glass Table), Threshold Breach(CPU/Mem/Latency p99), Threshold + Anomaly Detection 동시 적용 |
| **Problem Categorization & Prioritization** | 비즈니스 영향도 기반 우선순위 산정 | Priority = Impact(1~5) × Urgency(1~5) Matrix, Category/Sub-category Taxonom: ServiceNow CMDB Class Hierarchy 또는 BMC Remedy Asset Model 기반 정규화 |
| **Root Cause Analysis (RCA)** | 인과관계 추적 및 근본 원인 도출 | 5-Whys(단순 인과), Fishbone(Ishikawa, 6M: Man/Machine/Material/Method/Measurement/Mother Nature), FTA(Fault Tree Analysis, AND/OR Gate Boolean Logic), Pareto(80/20 Rule), Kepner-Tregoe(문제분석 vs 의사결정 격리), Apollo RCA(1980년대 NASA, 물리적·인적·관리적 원인 3-tier) |
| **Known Error Database (KEDB)** | 분석된 원인과 우회책 영구 저장 | CMDB 연동, KB Article RFC 2119 상태(State: Draft/Published/Archived), 검색 인덱스(Elasticsearch/OpenSearch), Tag 기반 Fault Pattern 분류, Machine Readable JSON-LD 스키마 |
| **Problem -> Change 연동** | 영구 해결책의 안전한 배포 | RFC(Change Record) 자동 생성, Risk Assessment, Pre/Post Implementation Test Plan, Rollback Strategy, Change Advisory Board(CAB) 승인 워크플로우 |
| **Post Implementation Review (PIR)** | 해결책 효과 측정 및 지속 개선 | KPI: Incident Re-occurrence Rate(IRR), Mean Time Between Failures(MTBF), Customer Satisfaction(CSAT), Defect Density Trend, Mean Time to Detect(MTTD) |

**핵심 알고리즘 및 기법 심화:**

- **5-Whys 한계점**: 선형적 인과만 추적하므로, 시스템적 결함(Systemic Cause)을 놓칠 수 있음. **Systemic RCA(서스테이너, Sidney Dekker)**는 인적 오류를 "원인"이 아닌 "증상"으로 보고, Latent Failure(잠재 결함)와 Triggering Condition을 분리 분석함.
- **Fault Tree Analysis (FTA)**: 최상위 이벤트(Top Event)부터 Boolean Logic(AND/OR Gate)으로 분해. 항공·원자력·금융 코어 시스템에서 MIL-STD-1629A 또는 IEC 61025 표준 사용. 정량화 시 Basic Event 확률 입력 -> Cut Set 도출 -> Minimal Cut Set(MCS) 순서로 위험도 계산.
- **Pareto + Fishbone 결합**: 발생 빈도 Top 20% 결함을 Fishbone 6M으로 분해 -> 정성적 인과 매핑 -> FMEA(Failure Mode and Effects Analysis) RPN(Risk Priority Number = S × O × D) 산출.
- **RCA Evidence Chain 무결성**: 로그 무결성 보장을 위해 WORM(Write Once Read Many) 스토리지 또는 SIEM(Splunk/Elastic) 원본 해시 보존. 법적 분쟁 대비 chain-of-custody 유지.

- **📢 섹션 요약 비유**: Problem Management는 "병원에서 종합 검진 후 처방전을 받는 과정"과 같습니다. 5-Whys는 "어디 아픈지 묻는 1차 문진", Fishbone는 "6가지 부위 X-ray", FTA는 "CT처럼 인과를 계층적으로 스캔"하는 것이며, KEDB는 모든 환자의 진료 기록이 누적된 "의학 백과사전"입니다.

---

## Ⅲ. 비교 및 연결

Problem Management는 ITSM 내에서 Incident, Change, Knowledge, Service Continuity Management와 긴밀히 결합되어 있으며, 동시에 DevOps/SRE 문화의 Post-Mortem, Agile의 Retrospective, 품질경영(QM)의 8D Report와도 개념적 교집합을 가짐. 다음은 이들과의 체계적 비교임.

| 구분 | **Problem Management (ITIL)** | **Incident Management** | **SRE Incident Post-Mortem** | **8D Report (QM/제조)** | **FMEA (Reliability Eng)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | 근본 원인 제거 및 재발 방지 | 서비스 즉시 복구(Time-to-Recover) | 학습·개선·Blameless 문화 | 고객 클레임 영구 해결 | 잠재 결함 사전 식별 |
| **시점** | 인시던트 발생 후/사전 예방 | 인시던트 발생 즉시 | 인시던트 발생 후(보통 24~72h 내) | 고객 클레임 접수 후 | 설계/개발 단계 |
| **접근 방식** | Reactive + Proactive 통합 | Purely Reactive | Reactive + Proactive | Reactive | Purely Proactive |
| **핵심 산출물** | RCA Report + KEDB + RFC | Resolution Note, SLA Report | Post-Mortem Doc, Action Items | D1~D8 8단계 보고서 | RPN 점수표, R-Map |
| **원인 분석 기법** | 5-Whys, Fishbone, FTA, Pareto | X(증상 해결) | Timeline + 5-Whys, Fishbone | 5-Whys, Ishikawa | Failure Mode × Effect × Cause Tree |
| **지식 자산화** | KEDB(서비스 운영 지식) | Self-Service KB | Confluence/Notion Runbook | Corrective Action Register | DFMEA/PFMEA Master |
| **연계 프로세스** | Change, Knowledge, CMDB, SLA | Problem, Change, Service Desk | SLO/Error Budget, Runbook Automation | CAPA(Corrective/Preventive Action) | Reliability Test, MTBF/MTTR |
| **성공 KPI** | 재발률v, MTBF^, MTTRv | SLA 준수율, FCR^ | Toilv, SLO 달성, Error Budget 보존 | 클레임 재발률, CAPA 종결률 | RPN 감소 추세 |
| **표준/참조** | ITIL 4, ISO/IEC 20000 | ITIL 4, ISO/IEC 20000 | Google SRE Book, DORA Metrics | AIAG-VDA FMEA 2019, QS-9000 | IEC 60812, SAE J1739 |

**타 시스템·도구와의 연결 구조:**

- **CMDB(ServiceNow CMDB, BMC Atrium)**: Problem의 Affected CI, Caused-by CI, Related-to CI를 3-tier relationship으로 매핑. RCA 시 Blast Radius 분석의 기반 데이터.
- **Observability Stack(Prometheus, Grafana, Loki, Tempo, Jaeger, Datadog, Dynatrace)**: Problem Ticket에 Evidence로 자동 첨부. Trace ID, Log Correlation, Metric Snapshot을 RCA Evidence로 활용.
- **AIOps/ITSM 통합 플랫폼**: ServiceNow ITSM + Predictive Intelligence, BMC Helix ITSM + cognitive automation, Moogsoft(Algo-level Event Clustering), BigPanda(Event Correlation), PagerDuty + Slack Bot.
- **Knowledge Management(KEDB ↔ KB)**: KEDB Article은 구조화된 Schema(원인/증상/우회책/Permanent Fix/RFC Link)를 가지며, L1/L2 Engineer 및 Self-Service Portal에서 즉시 조회 가능.
- **Change Management**: 모든 Permanent Fix는 RFC를 통해 CAB 승인을 받고, Pre/Post Check Script, Rollback Plan, Backout Plan이 필수 첨부됨.
- **SLA/OLA/UC**: Problem이 SLO를 위협할 경우 Service Level Manager에게 자동 에스컬레이션.

- **📢 섹션 요약 비유**: Incident Management가 "119 소방관"이라면, Problem Management는 "건축 구조 엔지니어"입니다. 소방
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 541 / 600

<- **이전**: [540. 사고 관리 인시던트 대응 프로세스](/studynote/11_design_supervision/06_exam_summary/541_incident_management_response_process/)
**다음**: [542. 변경 관리 CAB 영향 분석 승인](/studynote/11_design_supervision/06_exam_summary/542_change_management_cab_impact_analysis/) ->

---
