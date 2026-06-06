---
title: "SWG Secure Web Gateway Cloud"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SWG(Secure Web Gateway) Cloud는 클라우드 네이티브 Forward Proxy로 SSL/TLS Inspection, URL 필터링, 샌드박싱, DLP, CASB, ZTNA를 단일 정책 평면에서 제공하며, 사용자-인터넷 사이의 모든 HTTP/HTTPS/WebSocket 트래픽을 정책 기반으로 중계·검사·차단하는 SSE(Security Service Edge)의 핵심 구성요소이다.
> 2. **가치**: 본사·원격·모바일 사용자 위치 무관 일관된 보안 정책(Geo-IP, Reputation, URL Category, DLP 룰) 적용, 레거시 하드웨어 SWG 대비 CapEx 60~80% 절감, 글로벌 PoP(Point of Presence)을 통한 SSL 복호화 지연 10~50ms 수준 유지, 위협 차단 MTTD 80% 단축.
> 3. **판단 포인트**: 트래픽 온보딩 방식 선택(Explicit Proxy vs IPsec/GRE 터널 vs PAC/WPAD vs Browser Isolation vs ZTNA), SSL Inspection 범위 및 인증서 재서명 정책, SASE/SSE 통합(단독 SWG vs ZTNA+SWG+CASB+FWaaS 통합), PoP 위치(데이터 주권·지연), 멀티/vendor 종속 회피 아키텍처.

---

## Ⅰ. 개요 및 필요성

전통적 SWG(예: Blue Coat ProxySG, McAfee Web Gateway, Cisco WSA)는 데이터센터 내 하드웨어 어플라이언스로 운영되어 다음과 같은 한계가 있었다.

1. **원격 트래픽의 Hairpinning**: 재택/모바일 사용자가 본사 DC로 VPN 접속 후 인터넷을 우회하면서 지연·대역폭·SLA 저하 발생
2. **SSL/TLS 폭증 대응 불가**: 전체 웹 트래픽의 90% 이상이 HTTPS로 암호화되어 있으나, 레거시 HW는 CPU 기반 복호화로 Throughput 한계(TLS 1.3 0-RTT 등) 노출
3. **SaaS 확장으로 인한 Shadow IT**: Box, Slack, Notion, GenAI 서비스 등 수천 개 SaaS로의 데이터 유출 통제 불가
4. **글로벌 확장의 어려움**: 지사·해외법인마다 SWG 어플라이언스 신규 도입 필요
5. **SASE·Zero Trust 패러다임 전환**: Gartner가 2019년 SASE를, 2021년 SSE를 정의하면서 클라우드 단일 평면 보안이 표준으로 자리잡음

```text
[ Legacy On-Prem SWG Topology (과거) ]
[ 원격 사용자 ]---VPN---->[ 본사 DC: SWG Appliance ]---->[ Internet/SaaS ]
                                  |
                                  +- Hairpinning 지연 (50~200ms+)
                                  +- SSL 복호화 CPU 병목
                                  +- 글로벌 확장성 ✗

[ SWG Cloud (현재/미래) ]
[ 모든 사용자 ]---(IPsec/GRE/Explicit)---->[ Cloud PoP: SWG+ZTNA+CASB+FWaaS ]---->[ Internet/SaaS ]
                                                       |
                                                       +- Global Anycast 100+ PoP
                                                       +- 10Gbps+ 전용 SSL Inspection
                                                       +- SSE/SASE 단일 정책 평면
```

SWG Cloud는 본질적으로 **클라우드 사업자가 멀티테넌트 형태로 글로벌에 분산한 L7 Forward Proxy 팜**이며, Zscaler Internet Access(ZIA), Netskope Security Cloud, Cisco Umbrella(SIG), Palo Alto Prisma Access, Microsoft Defender for Cloud Apps, iboss, Menlo Security, Lookout SWG 등이 대표적이다.

- **📢 섹션 요약 비유**: 기존 SWG는 "회사 정문 경비실"이었다면, SWG Cloud는 "전 세계 도시에 설치된 100개 이상의 똑똑한 경비실"이며 사용자는 어디로 가든 항상 가장 가까운 경비실을 통과한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SWG Cloud의 내부 아키텍처는 다음 4개 평면(Plane)으로 구성된다.

```text
+----------------------------------------------------------------------+
|                       SWG Cloud 내부 아키텍처                          |
+----------------------------------------------------------------------+
|                                                                      |
|  +----------+  +----------+  +----------+  +-------------------+    |
|  | Control  |  |  Data    |  |  Log/    |  |   Management/     |    |
|  |  Plane   |<-->|  Plane   |  |  Telemetry|  |   Analytics       |    |
|  |(정책)    |  |(트래픽)  |  |  Plane   |  |   Plane           |    |
|  +----------+  +----------+  +----------+  +-------------------+    |
|       |              |              |                |              |
|       v              v              v                v              |
|  +--------------------------------------------------------------+   |
|  |  Edge / PoP (Forward Proxy + SSL Intercept + App Stack)       |   |
|  |  +--------+ +--------+ +--------+ +--------+ +---------+    |   |
|  |  | URL    | | TLS    | | DLP    | | AV/    | |  CASB   |    |   |
|  |  | Filter | |Inter-  | | Engine | |Sandbox | |  Inline |    |   |
|  |  |Engine  | |cept    | |(EDM/   | |(ATP)   | |  /API   |    |   |
|  |  |        | |        | |IDM/OCR)| |        | |         |    |   |
|  |  +--------+ +--------+ +--------+ +--------+ +---------+    |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Traffic On-ramp (트래픽 유입)** | 사용자/지사 트래픽을 Cloud PoP으로 인입 | Explicit Proxy(PAC/WPAD), IPsec/GRE 터널, Browser Isolation 원격 렌더링, ZTNA 에이전트, SD-WAN 통합, Browser-Based Proxy(Chrome Enterprise Connect) |
| **SSL/TLS Inspection 엔진** | TLS 1.2/1.3, QUIC, HTTP/2 복호화 후 재암호화 | MITM(Man-in-the-middle) 방식 인증서 재서명, HSM 기반 CA, OCSP Stapling, Certificate Pinning 우회(SPKI 핀 해시 동기화), JA3/JA4 fingerprint 검사 |
| **URL Filtering Engine** | URL 카테고리/평판/지역 기반 정책 적용 | Webroot/Brightcloud/Threat Intelligence feed, 머신러닝 기반 신규 도메인 분류(ML-Phishing), DGA(Domain Generation Algorithm) 탐지, Look-alike 도메인 탐지 |
| **DLP Engine** | 업로드/다운로드 본문·첨부파일 데이터 유출 차단 | 정규식(RegEx), 사전 기반(EDM: Exact Data Matching), 문서 Fingerprinting(IDM: Indexed Document Matching), OCR(이미지/PDF), ML 기반 컨텍스트 분석, Microsoft MIP/RMS 라벨 연동 |
| **Advanced Threat Protection (ATP)** | 제로데이 멀웨어/피싱 차단 | 정적 분석(PE 헤더, YARA 룰), 동적 분석(Cloud Sandbox: FireEye VX, Joe Sandbox), CDR(Content Disarm & Reconstruction), Sandbox Evasion 탐지(지연 실행, Sleep 패치) |
| **CASB 모듈** | SaaS별 위험 가시성 및 제어 | Inline(Forward Proxy) 모드 + API 모드 양쪽 지원, OAuth 토큰 리프트, SaaS Tenant Control(외부 공유 금지), Shadow IT 발견(벤더 DB 30,000+) |

### 핵심 처리 플로우 (HTTP/HTTPS 요청 시)

```text
[User]   --TLS ClientHello--->  [SWG PoP]
                                   |
                          1) SNI/Host 추출 -> 도메인 분류
                          2) 인증서 검증 + 정책 매칭(사용자/그룹/디바이스/위치/시간)
                          3) 정책: BLOCK / WARN / ISOLATE / ALLOW
                          |
                          <--- Inject SWG Root CA 인증서(서버 인증서 재서명)--
                                   |
[User]   --TLS 재협상--->  [SWG: TLS 종단]
                                   |
                          4) L7 payload 복호화
                          5) URL/Host Reputation 매칭
                          6) 파일 다운로드 시 AV + Sandbox + CDR
                          7) DLP 룰 매칭(업로드/다운로드)
                          8) CASB Inline 액션(예: Box 외부공유 금지)
                                   |
                          9) 자체 아웃바운드 TLS 연결(서버 인증서 검증)
                                   v
                              [Origin Web Server]
                                   |
                          10) 응답 수신 -> 다시 사용자측 TLS 암호화 -> 전달
                                   v
[User]   <---HTTP/2 Response--
```

### 주요 기술 파라미터

- **Throughput**: 단일 PoP 10~100 Gbps, SSL Inspection 시 1:1~1:3 성능 비율
- **Latency Budget**: 사용자 -> PoP RTT 5~30ms, PoP -> Origin 10~100ms, Total 50~200ms 목표
- **SSL Inspection 정책 제외**: 금융/의료/HIPAA/GDPR/은행 사이트, Certificate Pinning 강한 앱(모바일 뱅킹)
- **로그 보존**: Hot 30일(검색 가능), Warm 90일(저장), Cold 1~7년(컴플라이언스용 S3/Glacier)
- **암호화 알고리즘**: TLS_AES_256_GCM_SHA384, X25519MLKEM768(PQC 혼합)

- **📢 섹션 요약 비유**: SWG Cloud는 메일물류센터의 "X-ray 컨베이어벨트"와 같다. 택배(트래픽)가 도착하면 자동으로 X-ray(SSL 복호화), 위험물 검색(AV/샌드박스), 주소 검사(URL 필터), 비밀문서 검색(DLP)을 한꺼번에 통과시킨다.

---

## Ⅲ. 비교 및 연결

| 구분 | **On-Prem HW SWG** | **SWG Cloud (SSE/SASE)** |
| :--- | :--- | :--- |
| **배포 모델** | 데이터센터 하드웨어 어플라이언스 (1U/2U) | 클라우드 멀티테넌트 SaaS, 글로벌 PoP |
| **SSL 처리** | CPU 한계, 5~10Gbps 한정 | 전용 ASIC/NIC, 100Gbps+ 가능 |
| **확장성** | 사용자 수 증가 시 HW 증설 필요 | Auto-scale, 사용량 기반 과금 |
| **원격 사용자** | VPN Hairpinning (50~200ms 지연) | Anycast 라우팅으로 최적 PoP 인입 |
| **CapEx/OpEx** | CapEx 우세 (5년 TCO 비교 시 손익분기) | OpEx 우세 (예측 가능) |
| **데이터 주권** | 국내 DC 통제 가능 | PoP 지역 선택 필요 (KR, JP, SG 등) |
| **통합** | 단독 또는 NGFW 종속 | ZTNA + CASB + FWaaS + DLP 단일 콘솔 |
| **업데이트** | 주기적 수동/스케줄 업데이트 | 실시간 Threat Intelligence Push |
| **고가용성** | HA Pair (Active-Passive) | 멀티 리전/멀티 PoP 기본 내장 |
| **Shadow IT** | SaaS 인라인 통제 한계 | 30,000+ SaaS 벤더 DB로 자동 분류 |

### SWG ↔ 인접 보안 솔루션 관계

| 개념 | 연결 포인트 |
| :--- | :--- |
| **ZTNA (Zero Trust Network Access)** | SWG가 HTTP/HTTPS 트래픽을 담당, ZTNA가 비웹(SSH/RDP/DB) 내부 앱 접근 담당. SSE의 두 축 |
| **CASB (Cloud Access Security Broker)** | Inline(Forward Proxy) 모드는 SWG와 동일 채널, API 모드는 별도 SaaS 테넌트 통합. SWG 내 임베디드 또는 별도 엔진 |
| **FWaaS (Firewall as a Service)** | L3/L4 차원 정책은 FWaaS, L7 웹 위협은 SWG. SASE의 두 엔진 |
| **SD-WAN** | 지사 트래픽을 SD-WAN Edge -> IPsec/GRE -> SWG PoP. Cato, Versa, Aryaka 통합 사례 |
| **SIEM/SOAR** | SWG 로그를 Splunk/Sentinel/Chronicle로 전송, UEBA/이상행탐지 룰로 활용 |
| **EDR/XDR** | SWG의 네트워크 가시성과 EDR의 엔드포인트 가시성을 XDR로 통합 (예: Zscaler + CrowdStrike, Netskope + SentinelOne) |
| **IdP (SSO)** | SAML 2.0 / OIDC / SCIM 기반 사용자/그룹 정책 매칭, Conditional Access 정책 |
| **GenAI / LLM Security** | 프롬프트/응답 DLP, LLM 트래픽 분리, Shadow AI 탐지 (ChatGPT, Claude, Copilot 등) |

- **📢 섹션 요약 비유**: SWG Cloud는 보안의 "세관"이고, ZTNA는 "여권 심사", CASB는 "화물 검사", FWaaS는 "국경 초소"이다. SASE는 이 모든 것을 하나의 "통합 출입국 관리 시스템"으로 묶은 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **트래픽 온보딩 전략 결정**
   - 원격 사용자: Z
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 464 / 800

<- **이전**: [463. CASB 클라우드 접근 보안 브로커](/studynote/13_cloud_architecture/06_exam_summary/463_casb_cloud_access_security_broker/)
**다음**: [465. SASE 보안 접근 서비스 엣지 통합](/studynote/13_cloud_architecture/06_exam_summary/465_sase_secure_access_service_edge_integration/) ->

---
