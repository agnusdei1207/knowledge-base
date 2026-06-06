---
title: "DLP Data Loss Prevention Endpoint Protection"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 엔드포인트 DLP는 PC·모바일·USB 등의 단말에서 발생하는 파일 I/O, 클립보드, 프린트, 클라우드 업로드, 네트워크 송수신 이벤트에 대해 **Minifilter Driver / eBPF / Endpoint Security Framework** 커널 후킹과 **EDM(Exact Data Matching), Fingerprinting, Regex, ML-based Content Classification** 엔진을 적용해 데이터 유출을 차단하는 인-호스트(In-Host)형 데이터 보호 체계이다.
> 2. **가치**: 평균 데이터 유출 사고 1건당 약 **$4.88M(IBM 2024)**의 비용이 발생하며, 엔드포인트 계에서 **85% 이상의 내부자 유출(Insider Threat)을 사전 차단**하여 GDPR·개인정보보호법·산업기술보호법 등 컴플라이언스 위반 리스크를 직접적으로 저감한다.
> 3. **판단 포인트**: Agent vs Agentless, **Inline Proxy vs TAP 기반 Passive**, File-Level vs Channel-Level, **Network DLP(NDLP)·CASB·EDR과의 중복 정책**, 그리고 **TLS 1.3 ECH 환경에서의 SSL Inspection 우회**를 어떻게 통합 거버넌스로 설계할지가 기술사 핵심 판단 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 경계 보안(Perimeter Security)인 Firewall, IDS/IPS, NDR은 **외부에서 들어오는 침입(inbound threat)**에는 효과적이지만, 이미 내부로 침투한 악성코드 감염 단말이나 의도적·실수에 의한 **내부자 데이터 유출(outbound leakage)**에는 blind spot이 된다. IBM Cost of a Data Breach Report에 따르면 전체 유출 사고의 약 **68%가 엔드포인트에서 기인**하며, Verizon DBIR은 내부자에 의한 사고의 **57%가 권한滥用 후 수 분 이내**에 완료됨을 보여준다.

엔드포인트 DLP는 이러한 한계를 보완하기 위해 **"데이터가 떠나기 전 마지막 게이트(Last-mile Gate)"** 역할을 수행하며, 단말 자체에 상주하는 에이전트가 모든 데이터 경로에서 컨텐츠를 검사한다.

```text
[엔드포인트 DLP가 통제하는 5대 데이터 유출 채널]

  +----------------------------------------------------------+
  |                  Endpoint (PC / Mobile)                  |
  |                                                          |
  |   +----------+   +----------+   +----------+             |
  |   | Removable|   | Network  |   | Printer  |             |
  |   | Storage  |   | (HTTP/S, |   | Spooler  |             |
  |   | USB/SDD  |   | FTP,SMB) |   | local/   |             |
  |   +----+-----+   +----+-----+   | netw.)   |             |
  |        v              v          +----+-----+             |
  |   [Block/Allow]   [Inspect]          [Encrypt]           |
  |                                                          |
  |   +----------+   +----------+                            |
  |   | Cloud    |   | App/API  |                            |
  |   | Sync     |   | (Chat,   |                            |
  |   | (OD,GDrive|  | Web form)|                            |
  |   +----+-----+   +----+-----+                            |
  |        v              v                                   |
  |   [Scan+Token]   [Regex+ML]                              |
  +----------------------------------------------------------+
                  |
                  v  통합 로그 -> SIEM / SOAR
```

**왜 엔드포인트 DLP인가 — Old vs New Paradigm 비교**

| 구분 | 구세대(2000s) | 신세대(2020s~) |
| :--- | :--- | :--- |
| 통제 위치 | 네트워크 경계(Egress Proxy) | 단말 내부(Endpoint Agent) + CASB |
| 데이터 식별 | 정규식·키워드 단순 매칭 | ML·딥러닝·OCR·LLM 기반 Contextual Analysis |
| 채널 | HTTP/SMTP/FTP | + Cloud Sync, GenAI Prompt, WebSocket, USB-C Thunderbolt |
| 정책 | 정적 Rule(Allow/Deny) | 사용자·디바이스 Risk Score 기반 Adaptive Policy |
| 가시성 | 로그 위주 | UEBA, User Risk Analytics, Kill Chain Mapping |

- **📢 섹션 요약 비유**: 네트워크 방화벽이 "회사 정문 경비"라면, 엔드포인트 DLP는 "각 직원의 책상 위 금고 + 노트 반출 검색대"이다. 데이터가 노트북 밖으로 나가려면 반드시 이 검색대를 거쳐야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

엔드포인트 DLP 에이전트는 OS 커널과 사용자 영역 양쪽에서 동작하며, **이벤트 후킹 -> 컨텐츠 추출 -> 정책 평가 -> 조치(Action)**의 4단계 파이프라인을 따른다.

```text
[엔드포인트 DLP 에이전트 내부 아키텍처]

       +------------------------------------------------+
       |           Application Layer (User Mode)        |
       |  +--------------+  +--------------+            |
       |  | App Hooking  |  | Cloud Sync   |            |
       |  | Win32 API /  |  | Listener     |            |
       |  | .NET I/O     |  | (OneDrive,   |            |
       |  +------+-------+  | Dropbox SDK) |            |
       |         |          +------+-------+            |
       +---------+-----------------+--------------------+
                 |                 |  Events (IRP, syscall, file handle)
       +---------v-----------------v--------------------+
       |           Kernel Layer (Ring 0)                |
       |  +--------------+  +--------------+  +--------+ |
       |  | File System  |  | Network      |  | USB    | |
       |  | Minifilter   |  | NDIS / WFP   |  | Storage | |
       |  | Driver       |  | (Win)/eBPF  |  | Class  | |
       |  | (Windows)    |  | (Linux/Mac)  |  | Filter | |
       |  +------+-------+  +------+-------+  +---+----+ |
       |         |                 |              |      |
       +---------+-----------------+--------------+------+
                 v                 v              v
       +------------------------------------------------+
       |            Content Inspection Engine           |
       |  [Pre-Filter] -> [EDM] -> [Fingerprint] ->        |
       |  [Regex/Keyword] -> [ML Classifier] -> [Policy]  |
       +--------------------+---------------------------+
                            v
       +------------------------------------------------+
       |  Action: Block / Encrypt / Quarantine /        |
       |          Notify / Justify / Audit-Only         |
       +--------------------+---------------------------+
                            v
                  [Manager / SIEM / EDR 연동]
```

### 주요 OS 후킹 메커니즘 (기술사 출제 빈도 상)

| OS | 파일 I/O | 네트워크 I/O | 프로세스/메모리 |
| :--- | :--- | :--- | :--- |
| **Windows** | Minifilter Driver (`FLT_REGISTRATION`), FilterSendMessage | WFP(Windows Filtering Platform), NDIS 6.x Filter Driver, WinPcap/Npcap | ETW(Event Tracing for Windows), AMSI, PsSetCreateProcessNotifyRoutine |
| **Linux** | eBPF (`bpf_lsm`, `security_file_open`), FUSE, inotify | eBPF/XDP, TC, netfilter NFQUEUE | eBPF LSM Hooks, ptrace, auditd |
| **macOS** | Endpoint Security Framework(`es_event_*`), KEXT(legacy) | NEFilterDataProvider, NEPacketTunnelProvider | ESF Process Events, DYLD_INSERT_LIBRARIES |

### Content Inspection Engine의 핵심 알고리즘

1. **Exact Data Matching (EDM)**: RDB에서 고객 테이블을 가져와 row-level hash(SHA-256) 매칭. False Positive(FP) 최소 0.1% 이하.
2. **Document Fingerprinting**: 문서에서 2-gram을 추출해 `winnowing` 알고리즘으로 hash -> DB에 저장 -> 부분 매칭.
3. **Vector-based ML Classification**: BERT/Distil 기반 모델로 컨텐츠를 768-dim 임베딩 -> cosine similarity로 정책 라벨링. **Microsoft Purview Sensitivity Label**, **Trellix DLP**가 사용.
4. **OCR + Image Classifier**: 스크린샷·이미지 내 주민번호·신용카드 번호 추출. Tesseract, EasyOCR, 클라우드 호출(Google Vision API).
5. **Structured Data Extraction (SDE)**: CSV, XLSX, PDF Form에서 컬럼 인식 -> 셀이 신용카드/전화번호 패턴이면 차단.

### 정책 평가 우선순위(Pipeline Order)

```text
[ Policy Decision Pipeline ]

 Event --► Device Control (Class Filter) --► User/Device Risk Score
              |                                    |
              | Block? --► DENY                    v
              |                          Contextual Rule
              |                          (Source, Time, Geo)
              |                                    |
              v                                    v
        Content Inspection --► Severity (Critical/High/Med/Low) --► Action
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Minifilter / eBPF Driver** | 파일 쓰기·복사·이동 I/O Request Packet(IRP) 가로채기 | `FltRegisterFilter`로 등록, `PFLT_PRE_OP_CALLBACK`에서 Pre-Operation 시점 차단, `FLT_PREOP_PENDING` 반환 시 IO Manager가 작업 보류 |
| **Network Filter (WFP/eBPF)** | Outbound HTTP/S, FTP, SMTP, SMB 캡처 | WFP의 `FWPS_LAYER_ALE_AUTH_CONNECT_V4`에서 권한 콜백, TLS는 SSL Inspection Proxy 또는 JA3/JA4 핑거프린트 기반 메타데이터 추출 |
| **Content Analyzer** | EDM/Fingerprint/Regex/ML 검사 | Spark/Hive 같은 RDB에서 EDM 로드, ML 모델은 ONNX Runtime으로 추론(엔진 내장, GPU 불필요) |
| **Policy Engine** | 사용자·디바이스·컨텍스트·컨텐츠 종합 판단 | XACML 기반 ABAC, Active Directory SID + 디바이스 신뢰도(Cert/Health) + Risk Score 가중치 계산 |
| **Action Module** | Block / Encrypt / Notify / Quarantine | Windows에서는 `FltCancelIoOpen` 또는 `STATUS_ACCESS_DENIED` 반환, Linux는 `EPERM` 반환. Justification 입력 시 정책 예외 처리 |
| **Management Console** | 정책 배포, 인시던트 대시보드, 워크플로우 | MSSQL/Elasticsearch 백엔드, RBAC, OData/REST API, SAML/OIDC SSO 연동 |

### 주요 파라미터 및 튜닝 포인트

- **Buffer Size**: 4KB(기본) -> 64KB(대용량 파일 검사 시). 너무 크면 latency 증가.
- **Whitelisting Hash DB**: 신뢰 프로그램(explorer.exe, office) 화이트리스트로 FP 제거.
- **Sampling Rate**: 성능 위해 10% sampling, 단 EDM·Critical 룰은 100%.
- **ML Threshold**: cosine similarity 0.85(default), 0.92(Strict) — 재현율(Recall) vs 정밀도(Precision) 트레이드오프.

- **📢 섹션 요약 비유**: 엔드포인트 DLP는 공항 보안검색대와 같다. 손가락 하트를 훑는 금속탐지(파일 후킹) -> X-ray 컨베이어(컨텐츠 분석) -> 위험물 분류(Machine Learning) -> 담당자 호출(Action) 순서로 운영된다.

---

## Ⅲ. 비교 및 연결

엔드포인트 DLP는 단독 솔루션으로 쓰이기보다, **Network DLP, CASB, EDR, SIEM**과 함께 Defense-in-Depth 체계를 구성한다.

| 구분 | **Endpoint DLP** | **Network DLP (NDLP)** | **CASB** | **EDR** |
| :--- | :--- | :--- | :--- | :--- |
| 통제 지점 | 단말(Host) 내부 | Egress 게이트웨이 (Proxy/Mail GW) | Cloud API / Reverse Proxy | 단말(Host) 내부 |
| 가시 채널 | USB, Print, Local App, Clipboard, OS-level Net | HTTP/S, SMTP, FTP, SMB | SaaS(MS 365, Google, Slack, Salesforce) | Process, File, Registry, Net Connection |
| 오프라인 대응 | ✅ 강함(에이전트 상주) | ❌ VPN 우회 시 무력 | ❌ 미연동 SaaS 사용 시 | ✅ 강함 |
| 컨텐츠 복호화 | TLS MITM(에이전트 내장 CA) | SSL Inspection Appliance | API 모드: 평문, Proxy 모드: MITM | AMSI/ETW 기반 메모리 내 평문 |
| 운영 부담 | Agent 배포/업데이트 | 중앙 집중 | SaaS 종속 | Agent 배포/업데이트 |
| 정책 중복 | 있음 -> 통합 거버넌스 필요 | 있음 | 있음 | 룰셋은 다르나 상보 |
| 대표 제품 | Microsoft Purview Endpoint DLP, Forcepoint One Endpoint, Digital Guardian, Trellix DLP, Symantec DLP, Safetica, CoSoSys Endpoint Protector | Forcepoint DLP Network, Symantec DLP, GTB Inspector, Zscaler DLP | Microsoft Defender for Cloud Apps, Netskope, Palo Alto Prisma SaaS, Forcepoint CASB | CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint, Trend Vision One |
| 주요 탐지 룰 | 주민번호/신용카드 패턴, Confidential 라벨, 민감 키워드 | 동급, + DLP Header(`X-Forcepoint-DLP`) | Sharing Setting, Public Link, 외부 초대 | LOLBin, Living-off-the-Land, MITRE ATT&CK TTP |

### EDR + DLP의 융합: **DLP-EDR Convergence**

최근 트렌드는 **EDR(탐지/대응)**과 **DLP(데이터 통제)**가 단일 에이전트로 통합되는 것이다. CrowdStrike Falcon Data Protection, Microsoft Defender for Endpoint의 DLP 모듈, SentinelOne Singularity DataSet가 그 예이며, **DLP 인시던트(예: USB로 설계도면 10건 복사)**를 EDR이 자동으로 kill chain(사용자 행위, 프로세스 트리)과 매
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 383 / 800

<- **이전**: [382. 방화벽 차세대 NGFW 웹 방화벽 WAF](/studynote/12_it_management/05_security_compliance/382_firewall_ngfw_web_application_firewall_waf/)
**다음**: [384. SIEM 보안 정보 이벤트 관리 상관 분석](/studynote/12_it_management/05_security_compliance/384_siem_security_information_event_management/) ->

---
