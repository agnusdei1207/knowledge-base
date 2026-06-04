+++
title = "415. BPM 프로세스 관리 BPMN 모델링 (BPM Process Management BPMN Modeling)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: BPMN 2.0(OMG 사양, ISO 19510)은 업무 프로세스를 **Flow Objects(Events/Activities/Gateways) + Swimlanes(Pool/Lane) + Artifacts + Connecting Objects**의 4대 표기 카테고리로 시각화하는 그래픽 메타모델이며, **XPDL/WS-BPEL** 실행 엔진으로 컴파일 가능한 Executable BPMN을 구현하는 것이 본질이다.
> 2. **가치**: Forrester/Gartner 분석에 따르면 정형 BPM 도입 조직은 프로세스 **사이클 타임 30~50% 단축**, **First-Time-Right 60% 이상 향상**, **프로세스 변경 리드타임 80% 절감**(캄unda 레퍼런스 기준), 그리고 EA(Enterprise Architecture)와의 정합성 확보로 **감사 대응 비용 40% 절감** 효과를 달성한다.
> 3. **판단 포인트**: ① BPMN의 **Descriptive/Analytical/Executable 3-Level 모델링** 구분, ② 중앙집중식 **Orchestration(Camunda/IBM BPM)** vs 분산형 **Choreography(WS-CDL/Event-Driven)**, ③ Long-Running Process의 **Correlation Key 기반 상태관리** vs **Saga Pattern 기반 보상 트랜잭션**, ④ Human-in-the-Loop를 위한 **Task Form/UI** 통합 방식 결정이 아키텍처의 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

**BPM(Business Process Management)** 은 조직의 End-to-End 업무 흐름을 식별(Modeling) -> 설계(Design) -> 구현(Implementation) -> 실행(Execution) -> 모니터링(Monitoring) -> 최적화(Optimization) 하는 6단계 라이프사이클을 통해 지속적 개선을 추구하는 경영·IT 융합 Discipline이다. **BPMN 2.0(Business Process Model and Notation)** 은 OMG(Object Management Group)에서 2011년 표준화(현재 ISO 19510으로 채택)한 프로세스 모델링 표기로, 사업부서(Business Analyst)와 IT(Developer) 간의 공통 언어 역할을 수행한다.

**배경 및 기술적 Challenge**:
- 기존 UML Activity Diagram은 SW 개발자 중심 표기였기에 **BPMN은 비즈니스 친화적 표기**로 진화
- 종이 결재/ERP 모놀리식 워크플로우의 한계: **Hard-coding된 프로세스 변경 비용**, **Silo 업무 시스템 간 인터페이스 복잡도 증가**(MuleSoft 보고서 기준 평균 기업 1,000개 이상 API/앱 보유), **감사 추적 부재**로 인한 컴플라이언스 리스크
- 마이크로서비스/하이퍼자동화(Hyperautomation) 시대에 **Cross-System Orchestration** 필요성 증대
- **CMMN(Case Management Model and Notation)** + **DMN(Decision Model and Notation)** + **BPMN** 3종 세트가 OMG의 "Triple Crown"으로 자리매김

```text
+-----------------------------------------------------------------------------+
|             BPM Lifecycle (Dumas et al. Process-Aware Information Systems)  |
|                                                                             |
|   +----------+    +----------+    +----------+    +----------+              |
|   | ① Process| ->  | ② Process| ->  | ③ Process| ->  | ④ Process|              |
|   | Identif. |    | Discovery|    |   Analy. |    |   Redes. |              |
|   | (As-Is)  |    | (Mining) |    | (To-Be)  |    | (Target) |              |
|   +----+-----+    +----+-----+    +----+-----+    +----+-----+              |
|        v               v               v               v                  |
|   +----------+    +----------+    +----------+    +----------+              |
|   | ⑤ Impl.  |    | ⑥ Monit. | <-->| ⑦ Optim. |    | ⑧ Insti- |              |
|   |(Config)  |    | (BAM/KPI)|    | (BPI/BPR)|    |tutionaliz.|              |
|   +----------+    +----------+    +----------+    +----------+              |
|        |                                               ^                   |
|        +------------- Continuous Improvement ----------+                   |
|                                                                             |
|   지원 표준: BPMN 2.0 ▪ CMMN 1.1 ▪ DMN 1.4 ▪ XPDL 2.2 ▪ WS-BPEL 2.0        |
|   지원 도구: Camunda ▪ IBM BPM ▪ Pega ▪ Appian ▪ Oracle BPM ▪ Bizagi       |
+-----------------------------------------------------------------------------+
```

**기존 패러다임 vs BPM/BPMN 패러다임 비교**:
- **기존**: 워크플로우 엔진이 ERP/CRM 내부에 종속 -> 변경 시 코드 수정(개발자 의존), Cross-System 연동 어려움
- **BPMN**: 비즈니스 친화적 그래픽 모델 -> **Low-Code 모델링**으로 변경 -> 자동 배포, BPEL/Executable BPMN으로 엔진에 로드
- **BPEL -> BPMN 2.0**: BPEL이 XML 중심이라 비개발자 이해 곤란 -> BPMN 2.0은 그래픽 표기와 실행 시맨틱을 통합

- **📢 섹션 요약 비유**: BPMN은 마치 **"건축물의 평면도 + 배관·전기 설비 시방서"** 가 결합된 도면과 같다. 평면도는 비전문가가 보고 이해할 수 있고(비즈니스 뷰), 시방서는 시공자(엔진)가 그대로 따라 만들 수 있는(Executable) 양면성을 갖는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. BPMN 2.0 메타모델 4대 표기 카테고리

```text
+--------------------------------------------------------------------------+
|                          BPMN 2.0 Metamodel                              |
|                                                                          |
|  +--- Pools & Swimlanes (Organization) ---+                              |
|  |  +---------------------------------+   |  +-- Artifacts --+           |
|  |  | Pool A (구매팀)  | Lane1: 담당자  |   |  | Data Object  |           |
|  |  |                 | Lane2: 팀장    |   |  | Data Store   |           |
|  |  +-----------------+----------------+   |  | Group        |           |
|  |  | Pool B (재무팀)  | Lane1: 회계    |   |  | Annotation   |           |
|  |  +---------------------------------+   |  +---------------+           |
|  |            | Message Flow              |                              |
|  |            v                           |                              |
|  |  +- Flow Objects ------------------+  |                              |
|  |  |  (○)Start  (□)Task  (◇)Gateway |  |                              |
|  |  |  (◯)Intermediate  (▢+)Sub-Proc |  |  +-- Connecting --+           |
|  |  |  (◉)End                          |  |  | --> Seq. Flow   |           |
|  |  |  Activities: User/Service/Manual |  |  | ⤳ Mess. Flow   |           |
|  |  |  /Business Rule/Script/Send/Rcv |  |  | ┄┄ Association  |           |
|  |  +---------------------------------+  |  +---------------+           |
|  +--------------------------------------+                              |
|                                                                          |
|  Gateways:                                                                |
|   ◇ Exclusive(XOR)   ◇+ Parallel(AND)   ◇ Inclusive(OR)                 |
|   ◇○ Event-based     ◇* Complex                                         |
|                                                                          |
|  Events: ○ Start  ▷ Intermediate(Catch/Throw)  ◉ End                    |
|   Types: Message, Timer, Error, Signal, Conditional, Escalation,         |
|          Cancel, Compensation, Link, Terminate                           |
+--------------------------------------------------------------------------+
```

### 2. BPMN 2.0 실행 아키텍처(Engine Layer)

```text
+--------------------------------------------------------------------------+
|          Typical iBPMS Engine Architecture (Camunda/IBM BPM 계열)        |
|                                                                          |
|  +--------------- Presentation Layer -------------------------------+    |
|  |  Tasklist UI (Form IO / Angular / React)   ▪  Cockpit / Admin UI  |    |
|  +---------------------+--------------------------------------------+    |
|                        | REST API (OpenAPI 3.0)                          |
|  +---------------------v--------------------------------------------+    |
|  |              Process Engine Core                                 |    |
|  |  +-------------+ +-------------+ +-------------+ +----------+  |    |
|  |  | Process     | |  Decision   | |  Case       | |  Job     |  |    |
|  |  | Engine      | |  Engine     | |  Engine     | | Executor |  |    |
|  |  | (State Mach)| | (DMN/Drools)| | (CMMN)      | |(Timer/   |  |    |
|  |  |             | |             | |             | | Async)   |  |    |
|  |  +-------------+ +-------------+ +-------------+ +----------+  |    |
|  |  +-------------+ +-------------+ +--------------------------+  |    |
|  |  |  History    | |  Identity   | |  Repository / Deployment |  |    |
|  |  | (Audit/Logs)| | (LDAP/SSO)  | |  (BPMN XML, DMN, CMMN)   |  |    |
|  |  +-------------+ +-------------+ +--------------------------+  |    |
|  +---------------------+--------------------------------------------+    |
|                        |                                                 |
|  +---------------------v--------------------------------------------+    |
|  |     Persistence Layer (RDBMS)  +  Messaging (Kafka/RabbitMQ)     |    |
|  |     PostgreSQL / Oracle / MySQL  /  Event Sourcing(ES Log)       |    |
|  +-----------------------------------------------------------------+    |
|                                                                          |
|  External Connectors:                                                     |
|   ▪ Service Task -> Java Delegate / External Worker(gRPC pull)            |
|   ▪ HTTP/REST Connector (RFC 7231, OpenAPI 3)                            |
|   ▪ SOAP/RPC (WS-BPEL 호환) ▪ JMS / Kafka / AMQP                        |
|   ▪ RPA Bot (UiPath/Automation Anywhere) ▪ AI/ML Inference                |
+--------------------------------------------------------------------------+
```

### 3. 핵심 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Process Engine** | BPMN 모델의 State Machine 실행·제어 | **Camunda 7/8(ZEebe)**, **Flowable**, **jBPM**, **IBM BPM**, **Oracle BPM**, **Pega** — 토큰(Token) 흐름 관리, Transaction & Compensation 처리, Job Executor로 Timer/Async 처리 |
| **Decision Engine (DMN)** | 결정 테이블/식(DRD) 기반 Rule 실행 | **Drools/Red Hat DMN**, **Camunda DMN**, **OpenRules** — Hit Policy(FIRST/UNIQUE/PRIORITY/ANY/COLLECT/RULE ORDER/OUTPUT ORDER) 기반의 결정 로직 수행 |
| **Case Engine (CMMN)** | 비정형 케이스·예외 처리 | Camunda CMMN, IBM Case Manager — Plan Item의 Discretionary/Required 분리, Sentries(Event/Completion) 기반 동적 활성화 |
| **Repository/Versioning** | BPMN 모델, Form, Decision, Connector 정의 저장 | GitOps, Artifact Repository(Nexus/Artifactory) — Model Versioning + Semantic Version(MAJOR.MINOR.PATCH), Immutable Archive |
| **History/Audit Log** | 프로세스 실행 이력, BAM 데이터 | **Event Sourcing Pattern**(Zeebe: Append-Only Log), **Elasticsearch/OpenSearch** 기반 인덱싱, ACID 트랜잭션 보장 |
| **Tasklist/Portal** | Human Task UI, 결재·처리 화면 | **Form IO**, **bpmn.io**, **Angular/React SPA**, **Camunda Tasklist**, **IBM BAW(Process Portal)** |
| **Connectors/Workers** | 외부 시스템·서비스 호출 | **Outbound Connector**(Camunda 8) / **External Worker Pattern**(Long Polling, gRPC) / **EAI / ESB(Mule, Tibco, WSO2)** / **RPA Bridge** |
| **BAM/Dashboard** | 실시간 KPI/모니터링 | **Grafana + Prometheus**, **Kibana**, **Camunda Optimize**, **IBM BPM Performance Dashboard** — Cycle Time, SLA, Bottleneck Heatmap |

### 4. 핵심
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 415 / 800

<- **이전**: [414. ArchiMate 아키텍처 모델링 언어](/knowledge-base/studynote/12_it_management/05_security_compliance/414_archimate_architecture_modeling_language/)
**다음**: [416. IT 서비스 카탈로그 셀프서비스 포탈](/knowledge-base/studynote/12_it_management/05_security_compliance/416_it_service_catalog_self_service_portal/) ->

---
