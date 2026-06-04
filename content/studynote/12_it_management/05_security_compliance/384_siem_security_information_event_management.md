---
title: "384. SIEM 보안 정보 이벤트 관리 상관 분석 (SIEM Security Information Event Management)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SIEM 상관 분석(Correlation Analysis)은 이기종 보안 로그(Syslog, NetFlow, EDR Telemetry, Cloud Audit Trail 등)를 CEP(Complex Event Processing) 엔진과 룰셋(Sigma/YARA-L/SPL/KQL)을 통해 시간·맥락·엔티티 차원에서 결합하여 단일 이벤트로는 탐지 불가능한 복합 공격 시나리오(예: Pass-the-Hash + Lateral Movement + Data Exfiltration)를 시계열 그래프로 복원하는 분석 기법이다.
> 2. **가치**: Gartner 보고 기준 MTTD(Mean Time To Detect)를 평균 27일에서 1.2일로 95% 단축하며, 단일 규칙만으로는 약 60~80% 발생하는 False Positive를 베이스라인·화이트리스트·UEBA 점수 가중 방식으로 90% 이상 제거하여 Tier 1 분석가의 Noise Fatigue를 해소한다.
> 3. **판단 포인트**: 룰 기반(Rule-based) 탐지의 결정성 vs 통계/ML 기반(Anomaly-based) 탐지의 적응성 간 Trade-off, 온프레미스 QRadar/ArcSight vs SaaS형 Microsoft Sentinel/Splunk Cloud의 CapEx/OpEx·컴플라이언스 데이터 레지던시 선택, 그리고 상관 룰의 카디널리티 폭증(Combinatorial Explosion) 방지를 위한 컨텍스트 윈도우 설계가 핵심 결정 요인이다.

---

## Ⅰ. 개요 및 필요성

전통적 보안관제(SOC) 환경에서는 IDS/IPS, 방화벽, 웹로그, DB 감사 로그가 각각의 콘솔에서 독립적으로 분석되어, 공격자가 다층 방어를 우회할 경우 각 시스템은 "정상 이벤트" 또는 "저위험 경고"로 분리되어 표면화되는 맹점이 존재한다. 2013년 Target 침해, 2017년 Equifax 변조, 2020년 SolarWinds 공급망 공격 등에서 확인할 수 있듯, 단일 로그 라인에서는 탐지되지 않으나 7~14일의 시계열 패턴을 결합하면 명백한 Kill Chain이 복원되는 사례가 다수 보고되었다. SIEM 상관 분석은 이러한 "보안 관측 불가능성의 한계(Security Observability Gap)"를 해소하기 위해, 분산된 로그를 중앙 집중화하고 CEP(Complex Event Processing) 엔진에서 시간 윈도우·엔티티 컨텍스트·위협 인텔리전스(STIX/TAXII)를 결합하여 의미 있는 인시던트로 융합하는 프로세스이다.

```text
[SIEM Correlation Architecture - 계층별 데이터 흐름]

  +----------+ +----------+ +----------+ +----------+ +----------+
  | Firewall | |  IDS/IPS | |  EDR/AV  | |Web/App   | |Cloud     | --+
  | (PaloAlto| |(Suricata)| |(CrowdStr)| |GW(F5/Akam)| |Audit(AWS |   |
  |  /Forti) | |  /Snort) | |  /S1)    | |  /CloudF)| |CloudTrail)|   |
  +----+-----+ +----+-----+ +----+-----+ +----+-----+ +----+-----+   |
       | syslog/CEF | JSON/STIX | HTTPS/TLS | CEF/LEEF    | S3/HEC   |
       v            v            v           v             v         |
  +----------------------------------------------------------------+  |
  |  Layer 1 : Log Collection & Normalization (Cribl/Logstash)     |  |
  |   - CEF/LEEF 파싱 -> Common Schema (timestamp, src/dst, user,   |  |
  |     action, outcome, device_product, signature_id)             |  |
  |   - 시간 동기화 (NTP±50ms) / GeoIP / Asset CMDB Enrichment     |  |
  +-----------------------------+----------------------------------+  |
                                v                                     |
  +----------------------------------------------------------------+  |
  |  Layer 2 : Correlation Engine (CEP / Streaming)                |  |
  |   - Rule-based (Sigma / YARA-L / SPL)                          |  |
  |   - Behavioral / UEBA (Spark ML, Random Forest, LSTM)          |  |
  |   - Threat Intel Match (STIX 2.1, MISP, MITRE ATT&CK TTP)     |  |
  +-----------------------------+----------------------------------+  |
                                v                                     |
  +----------------------------------------------------------------+  |
  |  Layer 3 : Case Mgmt & Orchestration (SOAR - Phantom/Tines)   |<--+
  |   - Playbook 자동화 / 사용자 격리 / IOC 차단 / 티켓 연동      |
  +----------------------------------------------------------------+
```

전통적인 방식(SIEM 이전의 중앙 집중 로그 뷰어)과 비교하면, 상관 분석은 ① Rule Chain 개념으로 1차·2차·3차 이벤트를 트리거 조건으로 연결하고, ② Asset Criticality × Threat Intelligence × Identity Risk Score를 가중치로 곱하여 동적 우선순위(Dynamic Risk Score)를 산출하며, ③ 동일 사용자/호스트/세션을 Key로 한 Sessionization을 통해 세션 전 구간을 하나의 인시던트로 묶어 분석가에게 단일 Storyline을 제공한다. 이를 통해 분석가는 평균 200~400건/일의 Raw Alert를 8~15건의 우선 인시던트로 필터링하여 처리할 수 있다.

- **📢 섹션 요약 비유**: 여러 CCTV가 각자 촬영한 1초짜리 조각 영상을 한 영화감독이 시간순으로 이어붙여 "공범 A가 들어와 B와 만나 물건을 가져가는 30분짜리 범죄 영화"로 편집해 보여주는 것이 SIEM 상관 분석입니다. 단일 CCTV만 보면 "사람이 지나갔다"는 평범한 장면일 뿐이지만, 결합하면 스토리가 드러납니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SIEM 상관 분석의 핵심은 **이벤트 정규화(Event Normalization)** -> **세션화(Sessionization)** -> **룰 평가(Rule Evaluation)** -> **스코어링 & 컨텍스트화(Scoring & Contextualization)** 의 4단계 파이프라인이다. Gartner의 SIEM Magic Quadrant 기준 상용 솔루션(IBM QRadar, Micro Focus ArcSight, Splunk Enterprise Security, Microsoft Sentinel, Securonix, LogRhythm)과 오픈소스(Elastic SIEM, OSSIM/AlienVault, Wazuh, Apache Metron)은 모두 이 파이프라인을 공유하며, 차이는 룰 표현 언어와 처리 엔진(SPL vs AQL vs KQL vs Sigma) 그리고 ML 내장 수준에 있다.

```text
[Correlation Engine 내부 처리 흐름 - 상세 단계]

  Raw Event --+
              |  ① Parse (CIM/ECS/CRYPTO-JSON) -> 필드 추출
              |  ② Normalize (필드명/단위/시간대 통일)
              |  ③ Enrich (CMDB, GeoIP, WHOIS, TI 피드)
              v
  +---------------------------+
  |   Indexed Event Stream    | <--- Time-Series DB (OpenSearch/ES)
  |   ts, src, dst, user,     |      + Columnar Store (Parquet)
  |   action, outcome, bytes, |
  |   sig_id, sev, raw        |
  +------------+--------------+
               |
               v  ④ Session Key Derivation
  +----------------------------+
  | (user@host, src_ip,        |  ⑤ Sliding Window (5m/30m/24h)
  |  session_id, tuple)        |     + Hop Count / State Machine
  +------------+---------------+
               |
               v  ⑥ Rule Engine
  +-----------------------------------------------------+
  | IF (failed_login >= 5 in 5m from same src_ip)       |
  |  AND (subsequent successful_login same user)        |
  |  AND (privilege_escalation event within 30m)        |
  |  AND (dst in Critical Asset List)                   |
  | THEN -> trigger Incident: "BruteForce -> Account     |
  |        Takeover -> Privilege Escalation"             |
  |  severity = High, score = 85, mitre = T1110+T1078  |
  +------------+----------------------------------------+
               |
               v  ⑦ Correlation State (그래프/유한오토마타)
  +------------------------------+
  |   Kill Chain Graph           |  <--- Bloom Filter / Redis
  |   Initial Access --► TA0001  |      (cross-event state 공유)
  |   Execution       --► TA0002 |
  |   Persistence     --► TA0003 |
  |   Lateral Move    --► TA0008 |
  |   Exfiltration    --► TA0010 |
  +------------+-----------------+
               |
               v  ⑧ Risk Scoring & Prioritization
  +------------------------------+
  |  Risk = Σ (Asset_Crit ×      |
  |            Threat_Intel ×     |
  |            Identity_Risk ×    |
  |            Anomaly_Score) / n|
  |  -> Dynamic Priority (P1~P5)  |
  +------------+-----------------+
               |
               v  ⑨ SOAR Trigger
  +------------------------------+
  |  P1: 즉시 SOAR Playbook 실행 |
  |  (EDR Isolate / NAC Quarantine|
  |   / User Disable / Block IOC) |
  +------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **수집 에이전트 (Forwarder/Collector)** | 엔드포인트·네트워크·클라우드 로그를 전송 | Splunk Universal Forwarder, Winlogbeat, NXLog, Fluentd, Cribl Stream, AWS Kinesis Agent, OTel Collector — TLS+mutual auth, 양방향 압축(zstd), 영구 버퍼(back-pressure) |
| **파서 & 정규화 (Parser/Normalizer)** | 벤더 종속 형식(CEF/LEEF/syslog/JSON/ArcSight CEF)을 공통 스키마(ECS/CIM/UDEF)로 매핑 | 정규식 + Grok, KV/CSV/XML 파서, JQPath, 자동 분류 모델 — 필드 표준화(`src_ip`, `user`, `event.action`) 후 룰 엔진이 일관되게 평가 가능 |
| **인덱서 & 저장소 (Indexer/Store)** | 고속 시계열 검색 및 장기 보관(Hot/Warm/Cold/Frozen Tier) | Splunk Buckets + S3 SmartStore, Elasticsearch ILM, QRadar Ariel DB (PostgreSQL + LSM), Sentinel Log Analytics (Kusto) — 인덱스 샤딩, Rollup, TSDB |
| **상관 엔진 (Correlation Engine)** | 룰·상태·통계·ML 평가를 수행하는 CEP 코어 | 룰 기반(Rete 알고리즘, Drools, Sigma), 상태머신(Window Aggregation, Session Key Join), 통계/ML(Random Forest, Isolation Forest, LSTM AutoEncoder) — 1M EPS 처리 시 GPU 가속 또는 FPGA 필요 |
| **위협 인텔리전스 매처 (TI Matcher)** | IP/도메인/해시/YARA 룰을 인시던트와 실시간 매칭 | STIX 2.1/TAXII 2.1, MISP, AlienVault OTX, Recorded Future, Mandiant — DNS/IP/URL/HASH/PDB Path/Mutex 5종 이상 매칭, false positive를 줄이기 위해 Confidence ≥ 70 필터 |

상관 분석의 핵심 알고리즘을 보다 깊이 들여다보면, ① **룰 기반 상관(Rule-based Correlation)** 은 `IF condition_set THEN action` 형태로 Rete Network(전진 chaining 알고리즘)로 평가되며, 룰 노드의 팩트 매칭 시 O(N·M) -> O(N+M)으로 최적화된다. ② **집계 상관(Aggregation Correlation)** 은 `sliding window(W, n, threshold)` 함수로 시간 윈도우 내 동일 Key의 이벤트 수를 카운트하여 임계치 초과 시 알림을 발생한다(예: `failed_login_count > 10 in 5m grouped by src_ip`). ③ **크로스-이벤트 상관(Cross-Event Correlation)** 은 한 이벤트 A가 다른 룰의 트리거를 활성화하면 "Triggering Event"로 등록하고, 후속 룰에서 이를 컨텍스트로 활용하는 체이닝 메커니즘이다. ④ **상태 기반 상관(Stateful Correlation)** 은 유한 상태 머신(FSM)으로 공격 단계를 모델링하여 `(Reconnaissance -> Initial Access -> Foothold -> Lateral Movement)`가 모두 매칭되어야 최종 알림을 발생시킨다. ⑤ **ML 기반 상관(ML-based Correlation)** 은 UEBA 엔진이 사용자·엔티티 행동 베이스라인을 학습(28일 학습 윈도우)하고, 비정상 패턴(예: 근무시간 외 대량 다운로드 + 평소와 다른 GeoIP + 신규 AS-Num) 발생 시 Risk Score 1~100을 산출한다.

- **📢 섹션 요약 비유**: 룰 기반 상관은 "교사가 출석부 + 시험지 + 부모님 연락처를 동시에 대조하며 부정행위를 잡는 정직한 감독관"이고, ML 기반 상관은 "학생 100명의 평소 습관을 외운 AI가 갑자기 평소와 다른 패턴을 보이는 한 명을 콕 집어내는 똑똑한 카메라"입니다. 둘을 함께 쓰면 정밀도와 적응성을 동시에 잡습니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **SIEM 상관 분석** | **EDR/XDR (Endpoint Detection & Response)** | **SOAR (Security Orchestration Auto Response)** | **NTA/NDR (Network Traffic Analysis)** | **UEBA (User Entity Behavior Analytics)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1차 데이터 소스** | 로그 (방화벽/IPS/웹/DB/Cloud) | 엔드포인트 Telemetry (Process, File, Registry, Network) | SIEM/EDR/ITSM에서 받은 Alert | 네트워크 패킷/NetFlow/DNS 흐름 | 인증/접근 로그 + Identity Provider |
| **탐지 방식** | 룰·집계·상태·ML 하이브리드 | 시그니처 + 행위 + 메모리 분석 | 룰 없음 (Playbook 실행기) | 머신러닝(L7 DPI), 통계, 베이스라인 | 통계/ML (k-means, Isolation Forest, LSTM) |
| **상관 깊이** | 로그 간 시간·엔티티 상관 (강함) | 단일 호스트 내 프로세스 체인 (중간) | 인시던트 간 케이스 병합 (약함) | 호스트 간 네트워크 흐름 (중간) | 사용자 단위 행동 패턴 (강함) |
| **응답 기능** | Alert + Ticket (수동) | Host Isolate, Process Kill (자동) | Auto Playbook (강력, 자동화) | Inline 차단 (IPS 연동) | Identity Risk Score 제공 (간접) |
| **상호 보완 관계** | EDR/NDR Alert를 받아 2차 상관 수행 | SIEM에 Telemetry 전송, SIEM 룰로 외부 컨텍스트 결합 | SIEM의 인시던트를 받아 자동 티켓·조치 | SIEM에 Flow 로그 제공, NetFlow 룰 평가 | SIEM의 Identity 필드를 활용 점수 산출 |
| **예시 솔루션** | QRadar, Splunk ES, Sentinel, ArcSight | CrowdStrike Falcon, SentinelOne, MS Defender | Splunk SOAR, Palo Alto XSOAR, Tines | Darktrace, Vectra AI, ExtraHop | Securonix, Exabeam, Rapid7 IDR (UEBA 모듈) |
| **배치 위치** | 중앙 (SOC 코어) | 엔드포인트 에이전트 | SOC Tier 1~2 | 코어 스위치 미러 포트 / 센서 | SI
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 384 / 800

<- **이전**: [383. DLP 데이터 유출 방지 엔드포인트 보호](/studynote/12_it_management/05_security_compliance/383_dlp_data_loss_prevention_endpoint_protection/)
**다음**: [385. SOAR 보안 오케스트레이션 자동 대응](/studynote/12_it_management/05_security_compliance/385_soar_security_orchestration_auto_response/) ->

---
