---
title: "437. 클라우드 WAF 웹 방화벽 DDoS 보호 (Cloud WAF Web Firewall DDoS Protection)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cloud WAF는 OWASP Top 10 기반의 L7 시그니처/행위 기반 탐지 엔진과 Anycast 기반 글로벌 스케일의 DDoS 스크러빙 센터를 결합한 매니지드 보안 프록시로, TLS 종료·리버스 프록시·봇 디텍션·Rate Limit을 통해 Origin 서버로 유입되는 트래픽을 4단계(Edge->Scrubbing->Heuristic->Origin)에서 정제한다.
> 2. **가치**: AWS Shield Advanced+Cloudflare Magic Transit+Akamai Prolexic 적용 시 평균 TTM(Time To Mitigate) 3~10초, 정상 트래픽 처리량 100Gbps+ 보장, 오탐율 0.01% 미만 유지로 전자상거래 기준 매출 손실 99.7% 절감(Cloudflare 2023 DDoS Threat Report 기준).
> 3. **판단 포인트**: L3/L4는 전용 DDoS 스크러빙(Anycast+Scrubbing Center) 우선 적용, L7은 WAF+Bot Manager 조합, 오탐으로 인한 가용성 손실을 막기 위해 **모니터링(Detect) 모드 -> 점진적 차단(Prevent) 모드**의 트래픽 베이스라인 학습 절차와 BYOIP·Allowlist·Header 페로우(Forward) 정책이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise WAF(F5 BIG-IP ASM, Imperva SecureSphere, Barracuda WAF)는 시그니처 DB 업데이트·HW 스케일링·TLS 가속을 운영팀이 직접 관리해야 했으며, 100Gbps 이상의 L3/L4 볼류메트릭 공격에는 라우터/스위치 단의 블랙홀링 또는 ISP 코로케이션에 의존하여 TTM이 30분~수 시간에 달했다. 또한 OWASP Top 10 중 SQLi, XSS, SSRF, XXE 등은 L7 페이로드 인스펙션이 필수지만, 헤더 난독화·JSON 본문·gRPC·WebSocket 페이로드에 대한 정밀 분석은 CPU 집약적이어서 HW 의존도가 높았다.

클라우드 WAF는 **CDN 엣지(Anycast PoP) + 클라우드 스크러빙 센터 + Origin Protection**의 3-tier 아키텍처로 전환되며, 다음과 같은 패러다임 전환이 발생한다.

1. **위치 전환**: Origin 앞의 단일 어플라이언스 -> 글로벌 200~400개 PoP(Points of Presence) 분산
2. **용량 전환**: HW 기반 고정 처리량 -> Auto-Scaling의 소프트웨어 기반 무제한 처리량(AWS Shield는 5Tbps+ 흡수 용량宣称)
3. **탐지 전환**: 정적 시그니처 -> ML 기반 행동 분석(Cloudflare Bot Score, AWS WAF Fraud Control, Akamai Bot Manager)
4. **운영 전환**: 수동 룰 튜닝 -> Managed Ruleset(Cloudflare Managed Rules, AWS WAF Managed Rule Groups) + 사용자 정의 룰의 하이브리드

```text
[기존 On-Premise WAF 아키텍처]
                                      +-----------------+
        Attacker --> Internet --> ISP |    Router/L3    |--> Origin
                                      |  (Blackhole/    |     Server
                                      |   RTBH)         |
                                      |  +-----------+  |
                                      |  | On-Prem   |  |
                                      |  | WAF Appl. |  |  <- HW 의존,
                                      |  | (수동튜닝) |  |    단일장애점
                                      |  +-----------+  |
                                      +-----------------+

[Cloud WAF + DDoS Protection 아키텍처]

   L3/L4 Volumetric          L7 Application                    Origin
   (UDP/SYN/Amplification)   (HTTP Flood, SQLi, XSS)           Servers
        |                          |                              ^
        v                          v                              |
  +------------+            +------------+                +------+------+
  |  Anycast   |  L3/4     |  WAF Edge  |   L7 검사      |  Origin     |
  |  Network   | --------> |  PoP       | ------------>  |  (EC2,      |
  |  (200+ PoP)|  흡수/스크러빙|  (TLS종료)  |  정제된 트래픽   |   ALB,      |
  |            |            |  Bot Mgmt |                 |   S3,       |
  |  • BGP RTBH|            |  Rate Lim |                 |   EKS)      |
  |  • FlowSpec|            |  WAF Rule |                 |             |
  +------------+            +------------+                +-------------+
        |                          |                              ^
        +--------------------------+------------------------------+
                    Cloud Provider / CDN Vendor Managed
```

기존에는 1Gbps SYN Flood에도 라우터 ACL로 막다 정상 트래픽까지 끊겼다면, 클라우드 DDoS 보호는 **Anycast로 공격 트래픽을 200개 PoP에 분산 흡수**하고, L7은 **ML 모델이 0.5ms 이내에 봇/휴먼을 분류**해 Origin을 보호한다. Gartner 2023 보고서 기준, 클라우드 WAF 시장 규모는 약 26억 USD이며, Compound Annual Growth Rate(CAGR) 18.7%로 성장 중이며, 이는 모든 웹 트래픽의 평균 32%가 봇 트래픽이라는 Imperva Bad Bot Report 2023의 위협 현실을 반증한다.

- **📢 섹션 요약 비유**: 기존 WAF는 현관문 하나에 경비원 한 명(병목)이 지키던 것이고, 클라우드 WAF는 전 세계 200개 빌라(Anycast PoP)에 자동AI 경비 시스템과 군경 동원(BGP 블랙홀)이 상시 대기하는 **글로벌 호텔 체인 보안 시스템**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 WAF는 일반적으로 **Forward/Reverse Proxy + Content Delivery Network + Behavioral Analytics**를 결합한 4계층 모델로 동작한다. 각 계층은 OSI 7계층 중 어느 부분을 처리하느냐에 따라 명확히 구분된다.

```text
[요청 처리 흐름 상세: User -> Cloud WAF -> Origin]

[User]               [Edge PoP]              [Scrubbing Center]      [Origin]
   |                     |                          |                    |
   |  1. DNS Resolution  |                          |                    |
   +-------------------->|  anycast IP (1.1.1.1)   |                    |
   |                     |                          |                    |
   |  2. TCP/QUIC Handshake                          |                    |
   +-------------------->|  SYN -> SYN-ACK -> ACK     |                    |
   |                     |  (SYN Cookie 검사)       |                    |
   |                     |                          |                    |
   |  3. TLS 1.3 (0-RTT) |                          |                    |
   +-------------------->|  Cert Pinning 검증       |                    |
   |                     |  ECH/ESNI 처리           |                    |
   |                     |                          |                    |
   |  4. HTTP Request    |                          |                    |
   |  GET /api/v1/login  |  +-----------------+    |                    |
   +-------------------->|  | L7 Inspection   |    |                    |
   |                     |  | ① WAF Rule      |    |                    |
   |                     |  | ② Rate Limit    |    |                    |
   |                     |  | ③ Bot Score ML  |    |                    |
   |                     |  | ④ GeoIP Filter  |    |                    |
   |                     |  +-----------------+    |                    |
   |                     |         |                |                    |
   |                     |   +-----+-----+         |                    |
   |                     |   | Score ≥30 | 위협     |                    |
   |                     |   | -> 403     |         |                    |
   |                     |   | Score <30 | 정상     |                    |
   |                     |   +-----------+         |                    |
   |                     |         |                |                    |
   |  5. 정상 트래픽만   |         v                |                    |
   |<--------------------|---- TCP 커넥션 reuse --->|  Forward to Origin |
   |                     |         |                |  (PrivateLink/VPC) |
   |                     |         v                |         |          |
   |                     |  AWS Shield Advanced     |         v          |
   |                     |  / Cloudflare Spectrum   |  Origin에서 처리    |
   |                     |  / Akamai Prolexic       |         |          |
   |                     |  가 통과시킨 패킷만     |         v          |
   |                     |  Origin에 도달           |  Response 경로 동일|
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Anycast 네트워크 (L3 라우팅)** | 공격 트래픽을 다수의 PoP로 분산 | BGP Anycast로 동일 IP를 200+ PoP에 광고. DDoS 시 자동 라우팅으로 **Hot Potato Routing** 수행. 예: Cloudflare 1.1.1.1, AWS Route 53 Anycast |
| **TLS Termination & Re-encryption** | 평문 HTTP 가시화, Origin은 사설 인증서 | TLS 1.3, 0-RTT, OCSP Stapling, ECH(Encrypted Client Hello). Akamai는 TLS fingerprint(JA3/JA4)로 봇/툴 분류 추가 |
| **WAF Rule Engine (L7 시그니처)** | OWASP Top 10 인젝션 공격 차단 | 정규식 + AST(Abstract Syntax Tree) 파싱. AWS WAFv2는 SQLi 400+, XSS 350+ 패턴 매칭. False Positive 최소화를 위해 **Paranoia Level 1~4** (PL1: 최소, PL4: 엄격) |
| **Rate Limiting & Token Bucket** | API 남용·Brute Force 차단 | Sliding Window(60s 윈도우, IP당 1000 req) / Token Bucket(버스트 100, 지속 10 req/s). 429 Too Many Requests 응답 시 Retry-After 헤더 |
| **Bot Management (ML)** | 휴먼/봇 분류, Credential Stuffing 차단 | 행동 분석(마우스轨迹, 키보드 입력 패턴), TLS 핑거프린트(JA3/JA4), HTTP/2 fingerprint, 캡차(Managed Challenge). 봇 스코어 0~100, 임계치 기반 액션 |
| **Challenge/Response (CAPTCHA)** | 의심 트래픽의 인간성 입증 | Turnstile(Cloudflare), reCAPTCHA Enterprise(Google), hCaptcha. JS Challenge: 5초 브라우저 검증. Proof of Work: 브라우저 해시퍼즐 |
| **Managed Ruleset (Vendor 제공)** | 신규 위협 자동 업데이트 | Cloudflare Managed Ruleset(2023년 11월 기준 500+ 룰), AWS Managed Rule Groups(AWSManagedRulesCommonRuleSet, SQLi, Linux, KnownBadInputs) |
| **Logging & Analytics** | 탐지/차단 내역 감사, 포렌식 | Kinesis Firehose -> S3 -> Athena, 또는 CloudWatch Logs Insights. 필드: action, clientIP, httpMethod, uri, ruleId, botScore, country, asn |

핵심 알고리즘과 파라미터:

- **SYN Cookie**: SYN 큐 오버플로우 방어. `ISN = MD5(src_ip, src_port, dst_ip, dst_port, secret, timestamp)` 후 24bit 시퀀스 번호에 인코딩. 클라이언트 ACK에 ISN+1이 돌아오면 정상.
- **Bot Score 산출**: `Score = w1*TLS_FP + w2*HTTP_FP + w3*Behavior_Entropy + w4*Header_Anomaly + w5*ASN_Reputation` (가중치 `w1..w5`는 ML 모델이 자동 갱신). 임계치 < 30 = Likely Human, 30~70 = Likely Bot, > 70 = Definitely Bot
- **False Positive Rate(FPR) 산정**: `FPR = FP / (FP + TN)`. 업계 평균 0.01~0.1%, 공격의 5%는 정상 트래픽과 구별 불가능(Bot vs Human)
- **TPS(Total Cost of Protection)**: `TPS = 정책_수 + 룰_복잡도 + 트래픽_피크(Gbps) + 트래픽_월간(req)`

- **📢 섹션 요약 비유**: 클라우드 WAF는 **공항 검색대**와 같다. 1차 컨베이어(Anycast)는 위조 수하물을 여러 게이트로 분산시키고, 2차 X-ray(WAF Rule)는 총기·액체를 정밀 검사하며, 3차 인터뷰(ML Bot Score)는 승객의 행동·서류·목소리로 마약을 적발하고, 4차 출국 게이트(Origin Connection)는 의심 없는 승객만 비행기에 태운다.

---

## Ⅲ. 비교 및 연결

Cloud WAF를 다른 보안/네트워크 솔루션과 비교하여 설계 시 적절한 조합을 결정해야 한다.

| 구분 | Cloud WAF (L7) | Network Firewall (L4) | IPS/IDS (L4-L7) | API Gateway | CDN Edge WAF |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **보호 계층** | L7(HTTP/HTTPS 페이로드) | L3-L4(IP/Port/Protocol) | L4-L7(시그니처+이상행위) | L7(API 스키마/스펙) | L7(캐시+보안) |
| **주요 탐지 대상** | SQLi, XSS, CSRF, RCE, SSRF, XXE | Port Scan, IP Spoofing, CoAP Flood | CVE 익스플로잇, 프로토콜 이상 | BOLA(Broken Object Level Auth), GraphQL 쿼리 폭주 | 동일 WAF + 캐시 적중률 |
| **DDoS 대응** | HTTP Slowloris, HTTP/2 Rapid Reset(CVE-2023-44487), HTTP Flood | SYN Flood, UDP Flood, ICMP Flood | Volumetric은 약함, Application 일부 | L7 과도한 호출 차단 | 동일 WAF + 대용량 흡수 |
| **성능/처리량** | 보통(L7 인스펙션 오버헤드), 100K~1M req/s/PoP | 매우 높음(ASIC), 100Gbps+ | 중간, 10~50 Gbps | 보통, 10K~100K req/s | 매우 높음(캐시 적중 시) |
| **배포 형태** | SaaS(Cloudflare, AWS WAF) | HW/Virtual Appliance, Cloud-native(Palo Alto VM-Series, AWS Network Firewall) | HW/VM/SaaS | Kubernetes Sidecar(Envoy), Cloud-managed(API Gateway) | 글로벌 PoP 분산 |
| **원리/특징** | 페이로드 파싱, ML 봇 탐지, Managed Ruleset | 5-tuple stateful, Deep Packet Inspection | 시그니처 DB(CVE), Anomaly Detection | OpenAPI Spec 기반 검증, OAuth/JWT, Throttling | 정적 컨텐츠 캐싱 + 동일 WAF |
| **적용 시나리오** | 웹 애플리케이션, REST API, GraphQL | VPC 경계, East-West, North-South | 기업 내부 네트워크, 규제 환경 | MSA 내부 API, B2B 파트너 API | 정적 웹사이트, 미디어 스트리밍, 글로벌 서비스 |
| **오탐 리스크** | 중간~높음(페이로드 의존) | 낮음(프로토콜 기반) | 중간 | 낮음(스키마 기반) | 중간 |
| **비용 모델** | 요청당($/M req) + 룰당 | 인스턴스/시간 | 라이선스 + 트래픽 | 호출당 + 캐시 | 대역폭 + 요청 |

**상호 보완적
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 437 / 800

<- **이전**: [436. 클라우드 KMS 키 관리 암호화 서비스](/studynote/13_cloud_architecture/06_exam_summary/436_cloud_kms_key_management_encryption_service/)
**다음**: [438. 클라우드 VPC 네트워크 분리 보안 그룹](/studynote/13_cloud_architecture/06_exam_summary/438_cloud_vpc_network_isolation_security_group/) ->

---
