---
title: "385. SOAR 보안 오케스트레이션 자동 대응 (SOAR Security Orchestration Auto Response)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SOAR(Security Orchestration, Automation and Response)는 SIEM/EDR/UTM/Threat Intelligence 등 이기종 보안 솔루션들을 **REST API·공통 데이터 모델(STIX 2.1, CEF, OCSF)** 기반으로 연결(Orchestration)하여, **Playbook(워크플로우 자동화 스크립트)**과 **Case Management(티켓/사고 관리)** 엔진을 통해 탐지->분석->대응->복구까지의 사이버 인시던트 응답 사이클을 사람 개입 최소화하에 수행하는 SOC 운영 플랫폼이다.
> 2. **가치**: Gartner 보고서 기준 SOAR 도입 SOC는 **MTTD(평균탐지시간) 60% 단축, MTTR(평균대응시간) 68% 단축, L1 분석가 업무량 80% 감소** 등의 정량 효과를 거두며, 24×7 알람 피로(Alert Fatigue)·인력 부족 문제를 자동화로 해소한다.
> 3. **판단 포인트**: 기술사 관점의 핵심은 ①플레이북 과다 자동화로 인한 **"자동화의 함정(Automation Paradox)"** 통제, ②외부 API 장애·오탐 전파 시 **Circuit Breaker/Idempotency** 설계, ③**Human-in-the-loop** 단계의 법·감사 요건(개인정보보호법, ISMS-P, 금융보안원) 매핑, ④SaaS형 SOAR 선택 시 데이터 주권·국내 CSAP(클라우드 보안인증) 등 규제 적합성 판단이다.

---

## Ⅰ. 개요 및 필요성

전통적 SOC(Security Operations Center)는 2010년대를 기점으로 **SIEM(예: Splunk Enterprise Security, IBM QRadar, ArcSight, LogRhythm)** 중심의 로그 수집·상관분석·알람 체계로 운영되어 왔다. 그러나 다음의 4대 문제가 2017년경부터 임계점을 넘었다.

1. **알람 폭주(Alert Fatigue)**: 단일 SIEM이 하루 수십만 건의 Raw Event를 발생시키며, 분석가 1인당 75~150건의 Incident를 처리해야 함 (Ponemon 2018).
2. **반복적 수작업**: 60~80%의 1차 대응(계정 잠금, IP 차단, 샘플 샌드박스 전송, IOC Enrichment)이 동일 시나리오임에도 수동으로 반복.
3. **이기종 도구 격차(Integration Gap)**: SIEM ↔ EDR ↔ Firewall ↔ ITSM ↔ TIP(Threat Intelligence Platform)가 **상호 API 미지원·데이터 모델 상이(CEF vs LEEF vs Custom JSON)** 하여 컨텍스트 전달이断絶.
4. **숙련 분석가 부족**: 글로벌 보안 인력 부족 규모는 약 350만 명 (ISC^ 2022 Cybersecurity Workforce Study), 한국도 약 1.7만 명 부족 추정.

Gartner는 2017년 보고서에서 **"SOAR"** 카테고리를 독립 Magic Quadrant로 정의하며, 다음 3대 핵심 역량을 명시했다.

- **O**rchestration: 다수 보안 도구의 API/API Gateway를 통한 연결 및 오케스트레이션 계층 제공
- **A**utomation: 코드/스크립트 기반 Playbook으로 반복 작업 자동화
- **R**esponse: Case Management 및 Incident Response 절차의 표준화·추적

국내에서는 2021년 이후 금융보안원의 **금융보안 기술 참조모델** 및 KISA의 **클라우드 보안 가이드라인**에서 SOAR 도입이 권고되며, 공공·금융·대기업을 중심으로 Splunk SOAR(구 Phantom), Palo Alto XSOAR(구 Demisto), IBM Security QRadar SOAR(구 Resilient), ServiceNow Security Incident Response, Tines, Shuffle, 그리고 국내 SI(SK쉴더스 S-SOAR, 안랩 AhnLab Sentry, 이니텍 INISAFE SOAR) 등이 도입되었다.

```text
         +--------------------------------------------------------+
         |        기존 SOC의 Pain Point -> SOAR 도입 동기           |
         +--------------------------------------------------------+

  [SIEM/EDR/FW/TIP]   +
  [Email GW/Sandbox]  +--->  [수작업+반복]  --->  1건당 30~90분 --->  분석가 Burnout
  [Cloud Audit]       |
  [IAM/IDP]           +
        |
        |  (API 추출·컨텍스트 부족)
        v
  +--------------------------------------------------------+
  |              SOAR 도입 후 (Orchestration Layer)        |
  |                                                        |
  |   ▸ 1차 Enrichment/Containment 자동화  (≈ 80%)          |
  |   ▸ 분석가는 "판단"·"근본 원인 분석"에 집중              |
  |   ▸ Playbook 표준화로 신입 분석가도 Level 2 수행 가능    |
  +--------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SOAR 도입 전의 SOC는 **수신 전화가 100개씩 오는 민원 콜센터에서 일일이 메모하며 매뉴얼을 뒤지는 상황**이고, SOAR는 **AI 안내 시스템 + 자동 처리 + 필요 시 전문가 연결**이 통합된 **디지털 민원 플랫폼**과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. SOAR 3계층 아키텍처

```text
+----------------------------------------------------------------------------+
|                          SOAR Platform Reference Architecture             |
+----------------------------------------------------------------------------+
|                                                                            |
|  +--------------- 3-Tier Logical Architecture --------------------------+  |
|  |                                                                    |  |
|  |   +----------------------------------------------------------+    |  |
|  |   |  Tier 1. Ingestion & Detection (탐지 인입)                 |    |  |
|  |   |  - Webhook / Syslog / Kafka / Splunk HEC / Email Parser  |    |  |
|  |   |  - STIX 2.1 / TAXII 2.1 기반 IOC 자동 인입              |    |  |
|  |   |  - SOAR 자체는 탐지 엔진이 아닌 "탐지 결과의 컨슈머"      |    |  |
|  |   +----------------------------------------------------------+    |  |
|  |                            v (Trigger / Event)                    |  |
|  |   +----------------------------------------------------------+    |  |
|  |   |  Tier 2. Orchestration & Automation (오케스트레이션)        |    |  |
|  |   |  - Playbook Engine (DAG 기반)                              |    |  |
|  |   |     · Visual Workflow Editor (XSOAR XSIAM, Splunk Vis.)  |    |  |
|  |   |     · Python / PowerShell / JavaScript Code Block 지원     |    |  |
|  |   |  - Connector / App SDK (180~600+ 공식 Apps)               |    |  |
|  |   |  - Shared Data Model: "Artifact", "Container", "Note"     |    |  |
|  |   +----------------------------------------------------------+    |  |
|  |                            v (Action / Output)                     |  |
|  |   +----------------------------------------------------------+    |  |
|  |   |  Tier 3. Case Management & Response (사고 관리/대응)       |    |  |
|  |   |  - Ticket Model: Container(Incident) / Evidence Vault     |    |  |
|  |   |  - SLA / Approval / RBAC / Audit Trail (WORM 스토리지)   |    |  |
|  |   |  - Collaboration: Analyst Chat, @mention, War Room         |    |  |
|  |   |  - Reporting: MTTD/MTTR, MITRE ATT&CK Navigator 출력     |    |  |
|  |   +----------------------------------------------------------+    |  |
|  |                                                                    |  |
|  +--------------------------------------------------------------------+  |
|                                                                            |
|  +--------------- Underlying Infrastructure ---------------------------+  |
|  |  · Container Orchestration: K8s (Splunk SOAR ≥6.0, XSOAR v2)      |  |
|  |  · Multi-tenant DB: PostgreSQL/MySQL + Elasticsearch 검색엔진      |  |
|  |  · Message Bus: RabbitMQ / Kafka (이벤트 비동기 처리)               |  |
|  |  · Idempotency Store: Redis (중복 액션 방지 키, TTL 24h)           |  |
|  |  · Secret Vault: HashiCorp Vault / AWS KMS / 자체 HSM              |  |
|  +--------------------------------------------------------------------+  |
+----------------------------------------------------------------------------+
```

### 2. Playbook 내부 동작 원리 (DAG + State Machine)

Playbook은 내부적으로 **DAG(Directed Acyclic Graph)** 구조의 노드(작업)와 엣지(조건 분기)로 표현된다. 각 노드는 다음과 같이 분류된다.

```text
   Playbook Execution Flow (예: "피싱 메일 자동 대응")

   +--------+    +----------+    +--------------+    +--------------+
   | Trigger|---->|Enrichment|---->|Decision Gate |---->|Human-in-loop |
   | (SIEM) |    |·Whois    |    |(URL Risk>80?)|    |Analyst Approv|
   |        |    |·VirusTotal|    |              |    |              |
   |        |    |·Sandbox   |    +------+-------+    +------+-------+
   +--------+    +----------+           |Y                 |
                                       vN                 v
                                  +---------+        +----------+
                                  |Auto-Clos|        |Containment|
                                  | "False+|        |·Block URL |
                                  |         |        |·Recall MA |
                                  +---------+        |·Disable Us|
                                                     +-----+-----+
                                                           v
                                                     +----------+
                                                     |Post-Act  |
                                                     |·Update SI|
                                                     |·Notif IR |
                                                     |·Close    |
                                                     +----------+
```

핵심 설계 개념:

- **Artifact**: IOC·계정·해시·URL 등 분석 대상 객체로, 모든 노드 간 공유되는 정형 데이터. Splunk SOAR는 **Container**라는 단위로 Incident/Artifact/Note/Task/Evidence를 묶음.
- **Trigger**: ①Webhook (예: Splunk Notable Event) ②Scheduled Polling (예: 5분마다 TI 피드) ③Manual (분석가 클릭) ④Child Playbook (재귀 호출).
- **Concurrency & Timeout**: 노드 단위 timeout(기본 60s), retry 정책(exponential backoff, 1/2/4/8s), max retry 3회.
- **Idempotency Key**: 동일 Playbook이 동일 Incident에 대해 2회 실행되어도 외부 API 호출은 1회만 수행되도록 `IncidentId + ActionName + Hash(IOC)` 형태의 키를 Redis에 저장.
- **Circuit Breaker**: 대상 시스템(E.g. Firewall API) 5xx 응답률 > 50% 시 30초간 호출 차단, Fallback 경로로 L2 분석가에게 수동 위임.

### 3. 통합·연결 핵심 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Ingestion Adapter** | SIEM·EDR·TI·ITSM·Email GW로부터 이벤트 수신 | Splunk HEC(HTTP Event Collector), Kafka Consumer, IMAP/POP3, Webhook (HMAC-SHA256 서명 검증), STIX/TAXII 2.1 클라이언트, OCSF(Open Cybersecurity Schema Framework, 2022~) |
| **Connector / App** | 외부 시스템과의 양방향 API 래퍼 (180~600개/플랫폼) | OAuth 2.0 Client Credentials/Authorization Code, API Key/Vault, Rate Limiting Token Bucket, Schema Mapping(예: Defender ATP Alert ↔ SOAR Container) |
| **Playbook Engine** | 워크플로우 실행·상태 관리 | DAG + State Machine, Visual Editor (Drag&Drop, JSON Export/Import), 조건식(Jinja2-like DSL, e.g. Splunk SOAR `if` / XSOAR `playbook conditional task`) |
| **Case Management** | Incident/Evidence/Note/Audit 추적 | RBAC(역할기반), Field-level Encryption, WORM(Write Once Read Many) Audit Log, SLA Timer, War Room Collaboration(WebSocket 기반 실시간 코멘트) |
| **Orchestration Bus** | 멀티 플레이북 오케스트레이션·이벤트 라우팅 | Pub/Sub (RabbitMQ Exchange), Tenant 격리, Backpressure Queue, DLQ(Dead Letter Queue) |
| **Action/Code Block** | 외부 시스템 호출·데이터 변환 | Python 3.11+ Sandbox (Restricted Module), PowerShell Remoting, JavaScript, Custom Docker Container Action (XSOAR Marketplace) |
| **Reporting & Metrics** | KPI 대시보드, MTTD/MTTR, ATT&CK Coverage | MITRE ATT&CK Navigator JSON Export (레이어), OpenCypher/GQL 쿼리, Grafana/PowerBI 연동, KPI: MTTD·MTTR·FPR·Auto-Resolution Rate·Playbook Success Rate |
| **Vault & Secret Manager** | API Key·Token·PII 암호화 저장 | HashiCorp Vault Transit/KV v2, AWS KMS, HSM-backed Key (FIPS 140-2 L3), BYOK(Bring Your Own Key) 지원 |

### 4. 핵심 수치·파라미터

- **MTTD / MTTR 산식**:
  - MTTD = Σ(탐지 시각 − 공격 시작 시각) / N
  - MTTR = Σ(종료 시각 − 탐지 시각) / N
  - SOAR 도입 시 Median MTTR은 약 30분 -> 7분 (SANS 2023 SOC Survey)
- **오탐률(FPR) 허용치**: 자동 차단 Playbook은 FPR < 0.5% 권고, 임계치 초과 시 반드시 Human Approval 게이트 강제.
- **Playbook 평균 노드 수**: 성숙 SOC 기준 12~25 노드, 25 노드 초과 시 가독성·유지보수성 저하 -> Child Playbook 분할.
- **동시 실행 한계**: Splunk SOAR v6.0 기준 Worker 8개 / 노드, Container(Incident) 1건당 평균 1.2 Playbook 병렬 실행. 과부하 시 Queue Depth 500 초과 시 Alert.
- **데이터 보존**: Container 데이터 최소 1년(금융보안원 가이드), Audit Log는 3년, WORM 스토리지 권고.

### 5. 최신 기술 동향 (2024~2025)

- **AI/LLM 통합**: Palo Alto XSOAR Copilot, Splunk SOAR GPT-4o 기반 Playbook 자동 생성, Tines AI Workflow Builder, 자연어 -> Playbook YAML 변환.
- **SOAR + XDR 융합**: CrowdStrike Falcon Fusion, Microsoft Defender XDR, SentinelOne Singularity XDR이 자체 SOAR 워크플로우 내장 -> "SOAR-less SOAR" 흐름.
- **Hyperautomation / SOC-as-Code**: Playbook을 Git에 저장·Code Review·CI/CD로 배포(Jenkins/GitHub Actions), GitOps 기반 Change Management.
- **Agentic SOAR**: LLM Agent가 Playbook을 동적으로 생성·실행(예: Prophet Security, Dropzone AI).
- **국내 규제 정합**: ISMS-P(2024 개정), 금융보안원 "클라우드 기반 보안관제 가이드(2023)", 공공부문 "클라우드 보안인증(CSAP)" 등 가명결합·데이터 3법 연계 시 비식별 조치 자동화.

- **📢 섹션 요약 비유**: SO
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 385 / 800

<- **이전**: [384. SIEM 보안 정보 이벤트 관리 상관 분석](/studynote/12_it_management/05_security_compliance/384_siem_security_information_event_management/)
**다음**: [386. 취약점 관리 CVE CVSS 패치 전략](/studynote/12_it_management/05_security_compliance/386_vulnerability_management_cve_cvss_patching/) ->

---
