---
title: "Firewall NGFW Web Application Firewall WAF"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 전통 Stateful Firewall(L3-L4 Packet Filter) -> NGFW(L7 Application ID + User ID + IPS + Threat Intelligence 통합 DPI) -> WAF(HTTP/HTTPS 페이로드 의미 분석, OWASP Top 10·API·Bot 방어)로 진화하며, 각각 OSI 계층·탐지 방식·운영 위치가 명확히 구분되는 계층적(Defense-in-Depth) 보안 제어요소다.
> 2. **가치**: SSL Inspection 기반 가시성 확보, 애플리케이션별 정책(User-ID, App-ID), 위협 차단 자동화(IPS + Anti-Malware + Sandbox + URL Filtering 4-in-1), 클라우드 네이티브·API·제로트러스트 통합으로 공격 표면(Attack Surface) 70% 이상 축소 및 MTTD(Mean Time To Detect) 80% 단축 효과를 제공한다.
> 3. **판단 포인트**: SSL 복호화 오버헤드(TLS 1.3 0-RTT, 양 종단 암호화) vs 성능(throughput·latency), False Positive vs False Negative trade-off, Inline Bump-in-the-Wire의 HA 설계(Sync vs Async, A/P·A/A), 정책 최적화(Object Shadowing, Rulebase Cleanup) 및 Shadow IT 가시성 확보가 기술사 핵심 결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 Packet Filtering Firewall은 1989년 DEC SEAL, 1993년 Check Point FireWall-1의 Stateful Inspection 도입을 거치며 L3-L4 계층의 5-Tuple(Src/Dst IP, Protocol, Src/Dst Port, Flags) 기반 제어로 성숙했다. 그러나 2010년 이후 트래픽의 80% 이상이 HTTPS로 암호화되고, SaaS·API·모바일 앱이 1,000+ 애플리케이션으로 폭증하며 L7 컨텍스트 없는 5-Tuple 제어는 위협 식별 능력이 0%에 수렴했다. Gartner는 2009년 NGFW를 "기존 Stateful Inspection + IPS + Application Awareness + User Identity + Threat Intelligence를 단일 플랫폼에서 제공하는 차세대 방화벽"으로 정의하며 시장을 재정립했고, 동일 시기 WAF는 SQL Injection·XSS 같은 웹 애플리케이션 공격을 HTTP 페이로드 정규화 후 시그니처/이상 행위 기반으로 차단하는 전용 L7 보안솔루션으로 분리·발전했다.

한국 정보보호 환경은 2022년 개인정보보호법 강화, 2023년 ISMS-P 인증 기준 개정, 2024년 클라우드 보안인증(CSAP) 고도화, PCI-DSS 4.0 적용으로 인해 WAF·NGFW 도입이 사실상 의무화되었으며, 금융권은 전자금융감독규정 §51조에 따라 WAF 운영을 강제하고 있다. 또한 2025년 1월 시행된 인공지능 기본법에 따른 LLM API Gateway 보안까지 요구사항이 확대되고 있다.

```text
+--------------------------------------------------------------------+
|       공격 진화 vs 방어 진화 (Attack-Evolution vs Defense-Evolution) |
+--------------------------------------------------------------------+

  [1990s] L2/L3 L4 공격            [2020s] L7 암호화·API·AI 공격
  +--------------------+            +------------------------------+
  | SYN Flood          |            | Encrypted C2 (TLS 1.3, DoH)  |
  | IP Spoofing        |            | API BOLA / Broken Auth(ZT)   |
  | Port Scan          |   --->      | SQLi·XSS·SSRF·Deserialization|
  | Ping of Death      |            | LLM Prompt Injection (2024)  |
  +--------------------+            | 0-day Exploit (Log4Shell)    |
         |                          | Living-off-the-Land (LOLBins)|
         v                          +------------------------------+
  +--------------------+                       |
  |  Packet Filter     |                       v
  |  (1989~)           |      +-------------------------------------+
  |  • 5-Tuple         |      | NGFW + WAF + SWG + CASB + ZTNA      |
  |  • ACL 기반        |      | (DPI + App-ID + User-ID + Threat)   |
  |  • L4 이하         |      | + L7 SSL Inspection + API Protection |
  +--------------------+      +-------------------------------------+
            |                                |
            +-------- 통합 진화 -------------+
            Stateful FW(1993) -> UTM(2004) -> NGFW(2009) ->
            WAF(별도) -> WAAP(2020, Web App & API Protection)
```

**📢 섹션 요약 비유**: 전통 방화벽이 "편지 봉투의 보내는·받는 사람 주소만 보고 우편을 분류하는 우체국"이라면, NGFW는 "봉투 안의 편지 내용까지 펼쳐 읽어보고 위험한지 판단하는 보안 검색대", WAF는 "HTTP라는 특수 언어로 쓰인 편지의 문법 오류, 숨겨진 지시문, 악성 스크립트까지 탐지하는 전문 웹 보안 검색대"다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 3-Tier 계층적 방어 아키텍처 (L3-L4 -> L7 App -> L7 HTTP)

```text
            [Internet Users / APIs / Mobile]
                       | HTTPS (TLS 1.3)
                       v
+----------------------------------------------------------------------+
|  ① NGFW (L3-L7 통합 DPI - North-South + 일부 East-West)             |
|  +----------------------------------------------------------------+  |
|  | [SSL Inspection] --> [App-ID Decoder] --> [User-ID Lookup]    |  |
|  |       |                    |                   |              |  |
|  |       v                    v                   v              |  |
|  |  TLS MITM Proxy    App Signatures(2,500+)  AD/LDAP/Okta     |  |
|  |  (Forward Proxy)  (HTTP, gRPC, QUIC,        (SAML/OAuth)    |  |
|  |  (Decrypt/Re-Encr)  WebSocket, DNS, SMB)                     |  |
|  |                                                              |  |
|  |  +------------------------------------------------------+   |  |
|  |  | [Threat Prevention Pipeline]                          |   |  |
|  |  |  IPS Sig -> Anti-Malware -> Anti-Spyware -> URL Cat.   |   |  |
|  |  |  -> DNS Security -> DGA Detection -> Sandbox Submit     |   |  |
|  |  +------------------------------------------------------+   |  |
|  +----------------------------------------------------------------+  |
+----------------------------------------------------------------------+
                       | HTTP/HTTPS (cleartext from NGFW)
                       v
+----------------------------------------------------------------------+
|  ② L4-L7 Load Balancer (ADC) - 선택적                               |
|     SSL Offload, Persistence, Health Check                          |
+----------------------------------------------------------------------+
                       |
                       v
+----------------------------------------------------------------------+
|  ③ WAF (HTTP/HTTPS L7 의미 분석 - Reverse Proxy)                     |
|  +----------------------------------------------------------------+  |
|  | [HTTP Parser] --> [Normalizer] --> [Policy Engine]              |  |
|  |       |                |                  |                     |  |
|  |       v                v                  v                     |  |
|  | RFC 7230-7235     URL Decoding       1) Positive Model(Whitelst)|  |
|  | HTTP/2 (HPACK)    Unicode NFC/NFD    2) Negative Model(Signature|  |
|  | HTTP/3 (QUIC)     HTML Entity Dec.   3) Anomaly Scoring(ML)    |  |
|  | gRPC ProtoBuf     Base64·URL·Hex    4) Behavioral Analysis     |  |
|  | GraphQL             2-Stage Decoding 5) Bot Management          |  |
|  |                                                              |  |
|  |  [Protection Modules]                                         |  |
|  |  • SQLi (Lexical + AST + Tokenizer)                           |  |
|  |  • XSS (DOM-based + Reflected + Stored)                       |  |
|  |  • RCE/LFI/RFI/SSRF/XXE/Deserialization                       |  |
|  |  • CSRF Token Validator                                       |  |
|  |  • File Upload (MIME·Magic·Antivirus)                         |  |
|  |  • API Schema Validation (OpenAPI 3.0 / GraphQL Introspect)   |  |
|  |  • Rate Limiting / GeoIP / IP Reputation                      |  |
|  |  • Credential Stuffing Defense (Device ID, JA3/JA4)           |  |
|  +----------------------------------------------------------------+  |
+----------------------------------------------------------------------+
                       |
                       v
            [Web/App Server / API Gateway / Microservice]
```

### 2. 핵심 컴포넌트 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Stateful Inspection Engine** | L4 세션 상태 추적·정책 매칭 | TCP 상태 머신(NEW, ESTABLISHED, RELATED, INVALID), 5-Tuple + Sequence Number 기반 패킷 재조립·순서 검증, Conntrack Table(Concurrent Session: PA-7000 24M+, FortiGate 7121F 320M) |
| **Application ID Decoder** | L7 프로토콜 식별 (Port-Independent) | App-ID 시그니처(2,500+ App, 18,000+ Sub-App), HTTP Host/Header/URI 분석, Encrypted App ID(TLS SNI, ALPN, HTTP/2 Frame), Protocol Decoding(HTTP/2 HPACK, QUIC, gRPC, WebSocket, SMBv3, RDP, SSH, DNS-over-HTTPS) |
| **User-ID Agent** | 사용자-트래픽 매핑 | AD/LDAP/Citrix Terminal Server Agent, Captive Portal, GlobalProtect, X-Forwarded-For 신뢰 IP, SAML/OAuth Identity Provider, SCIM 2.0 연동 |
| **SSL/TLS Inspection Proxy** | 종단간 암호화 복호화·재암호화 | Forward Proxy(Outbound) + Reverse Proxy(Inbound), TLS 1.0~1.3 지원, OCSP Stapling, CRL 체크, HSM 통합(Thales Luna, AWS CloudHSM), Decryption Exclusion List(금융·의료 우회), RSA->ECDHE 키 교환 재협상 |
| **IPS Engine (Threat Prevention)** | 익스플로잇·CVE 차단 | 단일 패스(Single-Pass) DPI, 프로토콜 이상 행위 탐지, 시그니처 30,000+ (CVE 맵핑), 흐름 기반(Flaw-based) 탐지, HTTP 헤더 정규화, IPv4/IPv6 Fragment Reassembly |
| **WAF Detection Engine** | 웹 페이로드 의미 분석 | ① **Negative Model**: 시그니처(정규식) – SQLi `' OR 1=1--`, XSS `<script>alert(1)</script>`, ② **Positive Model**: 화이트리스트(허용 입력 패턴), ③ **Anomaly Scoring**: 트래픽 통계 ML(熵, Request Length Distribution), ④ **Behavioral**: Credential Stuffing(JA3 Fingerprint), ⑤ **API Schema**: OpenAPI 3.0 강제 |
| **Logging & Telemetry** | 정책·위협 로그 | Syslog/CEF/LEEF, NetFlow v9/v10(IPFIX), Palo Alto PAN-OS XML API, Fortinet FortiAnalyzer, Splunk/Elastic 연동, Panorama/Cortex Data Lake |
| **HA Cluster Module** | 이중화·무중단 운영 | Active/Passive(상태 동기화, Session Sync), Active/Active(부하분산, Asymmetric Routing), ECMP/LACP, HA3 Link(전용 동기화), Hitless Upgrade |

### 3. NGFW 동작 원리 (Single-Pass Architecture)

```text
  [Packet In] ---> [Parser] ---> [Session Lookup] ---> [Policy Lookup]
       |                                              |
       |                                              v
       |                                    [App-ID Decoder]
       |                                              |
       |       +--------------------------------------+
       |       v
       |  [User-ID Lookup] ---> [Threat Engine] ---> [URL Filtering]
       |                                              |
       |                                              v
       |                                    [Match Action 결정]
       |                                    (Allow/Deny/Reset/Quar.)
       |                                              |
       |                                              v
       |                                    [Log Generation]
       |                                              |
       v                                              v
  [QoS] <--- [NAT] <--- [Packet Out] (Single-Pass: 한 번의 패킷 처리에 모든 검사)
```

**핵심 원리**: 기존 UTM(다중 패스, 성능 저하)과 달리 NGFW는 **Single-Pass DPI**로 1개 패킷 처리 시 1회 디코딩 후 메모리 내에서 App-ID·User-ID·IPS·URL·AV를 모두 수행한다. Palo Alto Networks의 PA-7000 Series는 200Gbps App-ID 처리, Fortinet FortiGate 7121F는 NP7(Network Processor) + CP9(Content Processor) 하드웨어 가속으로 1.5Tbps IPS 처리 성능을 제공한다.

### 4. WAF 정책 적용 모드 (Deployment Mode)

| 모드 | 동작 방식 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| **Reverse Proxy** | WAF가 클라이언트 종료점, 백엔드로 재연결 | SSL 오프로드, 서버 IP 은폐, 캐싱 | 인증서 관리, 응답 지연 |
| **Transparent Bridge (Bump-in-the-Wire)** | L2 브릿지, MAC/IP 변경 없음 | 네트워크 재설계 불필요, 단순 배포 | 일부 트래픽 가시성 제한 |
| **Inline Rout
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 382 / 800

<- **이전**: [381. 침입 탐지 IDS 침입 방지 IPS 비교](/studynote/12_it_management/05_security_compliance/381_intrusion_detection_ids_prevention_ips/)
**다음**: [383. DLP 데이터 유출 방지 엔드포인트 보호](/studynote/12_it_management/05_security_compliance/383_dlp_data_loss_prevention_endpoint_protection/) ->

---
