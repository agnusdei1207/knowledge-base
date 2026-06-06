---
title: "SASE Secure Access Service Edge Integration"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SASE(Secure Access Service Edge)는 2019년 Gartner가 정의한 클라우드 기반 네트워크·보안 융합 아키텍처로, SD-WAN 엣지에서 SWG(Secure Web Gateway)·CASB(Cloud Access Security Broker)·ZTNA(Zero Trust Network Access)·FWaaS(Firewall as a Service)·DLP를 단일 PoP(Point of Presence) 정책 평면으로 통합하여, 사용자 ID·디바이스 컨텍스트·세션 위험도를 기반으로 "어디서든 일관된 보안 접속"을 제공한다.
> 2. **가치**: 전통적 허브-앤-스포크 VPN/MPLS 구조 대비 WAN 비용 60~75% 절감, 백홀 트래픽 80% 이상 감소, 정책 배포 시간 수 주 -> 수 분 단축, 글로벌 평균 지연시간 30~50ms 이하 보장, M&A·원격근무 확장 시 무중단 PoP 추가만으로 신규 사이트 온보딩 가능.
> 3. **판단 포인트**: 단일 벤더 종속(Single-vendor SASE) vs 멀티 벤더 모듈 조립형(Composable SASE), PoP 커버리지 밀도(골드/실버/브론즈 티어), 에이전트 기반 vs 에이전트리스 ZTNA, IPsec/GRE 터널 vs SSL/TLS 프록시 처리 위치, 그리고 기존 IDC/레거시 NGFW와의 단계적 코어스트(Coexistence) 전략이 기술사 핵심 결정 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 배경: 경계가 사라진 시대의 보안 모순

클라우드 SaaS 도입 확대로 2008년 이후 약 90% 이상의 업무 애플리케이션이 데이터센터 외부(IaaS/SaaS)로 이동했음에도 불구하고, 대부분의 한국 기업은 여전히 1990년대 보안 모델인 **"Castle-and-Moat"** 구조에 머물러 있다. 사용자 트래픽을 본사/IDC로 강제 백홀(Backhaul)한 뒤 NGFW/IPS/WAF로 검사하는 이 구조는 다음 4가지 근본 모순을 낳는다.

| # | 현상 | 기술적 원인 | 결과 |
| :--- | :--- | :--- | :--- |
| 1 | 해외 지사·원격 근무자 체감 속도 저하 | MPLS 백홀 후 재라우팅으로 RTT 200~600ms 급증 | 업무 생산성 저하, Shadow IT 만연 |
| 2 | 클라우드 트래픽 폭증으로 회선 비용 급등 | North-South 트래픽이 본사를 통과하는 허브 병목 | WAN 비용 매년 15~30% 증가 |
| 3 | 정책 일관성 붕괴 | 사내망/원격/모바일 별도 정책 평면 운영 | Shadow Access, 정책 충돌 |
| 4 | 위협 표면(Attack Surface) 확대 | VPN은 일단 인증 시 내부 전체 접근 허용 | 랜섬웨어 횡적 이동(Lateral Movement) |

### 1.2 SASE의 등장과 정의

Gartner는 2019년 8월 *"The Future of Network Security Is in the Cloud"* 보고서에서 SASE를 공식 발표했고, 2021년 *Hype Cycle for Network Security*에서 **메인스트림采纳(Mainstream Adoption) 진입 5~10년**으로 평가했다.

> **Gartner 공식 정의**: SASE는 SD-WAN과 SSE(Security Service Edge)를 결합하여, **신원·컨텍스트 기반 정책**을 통해 **엣지 클라우드**에서 **엔터프라이즈 보안**을 제공하는 클라우드 네이티브 아키텍처다.

```text
+---------------------------------------------------------------------+
|              SASE 개념도: Identity-Centric Cloud Fabric              |
|                                                                     |
|   [User/Device]      [Branch/IoT]      [Cloud Workload]             |
|        |                  |                  |                       |
|        v                  v                  v                       |
|  +--------------------------------------------------+                |
|  |         Global SASE PoP (Cloud Edge)             |                |
|  |  +----------+ +----------+ +----------+         |                |
|  |  |  SWG     | |  CASB    | |  ZTNA    |         |  <- SSE         |
|  |  | (웹/URL) | | (SaaS)   | | (앱접근) |         |                |
|  |  +----------+ +----------+ +----------+         |                |
|  |  +----------+ +----------+ +----------+         |                |
|  |  |  FWaaS   | |  DLP     | |  RBI     |         |                |
|  |  | (L4~L7)  | | (데이터) | | (격리)   |         |                |
|  |  +----------+ +----------+ +----------+         |                |
|  |  +----------+ +----------+                       |                |
|  |  |  SD-WAN  | |  WAAP    |                       |  <- SD-WAN     |
|  |  | (스티브) | | (API/WAF)|                       |                |
|  |  +----------+ +----------+                       |                |
|  +--------------------------------------------------+                |
|         ^                ^                ^                          |
|         |                |                |                          |
|      [PoP-Tokyo]    [PoP-Seoul]    [PoP-Singapore]                  |
|         |                |                |                          |
|         +------- Single Policy Plane -------+                        |
|              (Gartner MASCE/SSPM/UEBA 통합 제어)                    |
+---------------------------------------------------------------------+
```

### 1.3 기존 패러다임 vs SASE 패러다임

| 차원 | Legacy (Castle-and-Moat) | SASE (Cloud-Native Edge) |
| :--- | :--- | :--- |
| 트래픽 경로 | User -> MPLS -> DC NGFW -> Internet | User -> Nearest PoP -> Internet/SaaS |
| 정책 키 | IP 주소, 포트, VLAN | ID(User/Service), Device Posture, Context, Session Risk |
| 정책 평면 | 장비별 CLI/콘솔 | 단일 클라우드 콘솔 (One-Pane-of-Glass) |
| 확장성 | 하드웨어 증설(수 주~수 개월) | PoP 자동 활성화(수 분) |
| 사용자 위치 | 사내망 vs 외부망 구분 | 위치 투명(Location-Independent) |
| 보안 검사 지점 | 중앙 DC 집중 | 분산 엣지(Edge-Cloud) |
| M&A 대응 | 네트워크 통합 프로젝트 | 신규 사용자 그룹 등록만 |

- **📢 섹션 요약 비유**: 기존 보안이 "성벽 안의 성"이라면, SASE는 **"사용자 한 사람 한 사람에게 투명한 요새 망토를 씌워주는 마법의 안개"** 와 같다. 안개가 어디에 있든 사용자가 움직이든, 그 안개가 따라다니며 모든 접근을 보호한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 SASE의 5대 핵심 역량 (Gartner 정의)

Gartner는 SASE가 갖추어야 할 **필수 기능 셋**을 다음과 같이 명시한다.

1. **Software-Defined WAN (SD-WAN)**: 애플리케이션 인지(Application-Aware) 트래픽 엔지니어링, 동적 경로 선택, MPLS 대체
2. **Secure Web Gateway (SWG)**: URL 필터링, HTTPS 인터셉트(SSL Inspection), 안티멀웨어, DNS 보안
3. **Cloud Access Security Broker (CASB)**: Shadow IT 발견, SaaS 설정 감사, API/리버스 프록시 모드 DLP
4. **Zero Trust Network Access (ZTNA)**: 신원·디바이스·컨텍스트 기반 최소 권한 접근, Microsegmentation
5. **Firewall as a Service (FWaaS)**: 차세대 방화벽(L4~L7 IPS, IDS, DPI)을 클라우드에서 제공

부가적으로 **DLP(데이터 손실 방지)**, **RBI(Remote Browser Isolation)**, **WAAP(Web App & API Protection)**, **SD-WAN 라우팅**, **DNS 보안**이 통합된다.

### 2.2 SSE(Security Service Edge) – SASE의 보안 부분집합

2020년 Gartner가 SASE를 SD-WAN과 SSE로 분리 정의함에 따라, **SSE = SWG + CASB + ZTNA + FWaaS** 이고, SASE = SSE + SD-WAN이다.

```text
+--------------------------------------------------------------------+
|          SASE / SSE 정책 평가 흐름도 (Policy Decision Flow)        |
|                                                                    |
|  [사용자 접속 요청]                                                  |
|         |                                                          |
|         v                                                          |
|  +--------------+                                                  |
|  | 1. 시그널 수집 | --► ID(SSO/MFA), Device(EDR/Posture),         |
|  |    Signal     |     Location(Geo/IP), Context(Time/Risk)        |
|  +------+-------+                                                  |
|         v                                                          |
|  +--------------+                                                  |
|  | 2. 정책 엔진  | --► Trust Broker가 SDP(Software-Defined          |
|  |    PE-PE      |     Perimeter) 제어기로 PEP 접근 허용 여부 결정 |
|  +------+-------+                                                  |
|         v                                                          |
|  +--------------+    YES    +-----------------+                   |
|  | 3. 위험도 평가 | --------►| 4a. 동적 접근 허용 |                  |
|  |   Risk Score  |           |   (Least Priv.)  |                  |
|  +------+-------+           |  -Step-up Auth   |                  |
|         | NO / 미달         |  -DLP 검사        |                  |
|         v                   |  -SSL 복호화      |                  |
|  +--------------+           +-----------------+                   |
|  | 4b. 차단/격리 | --------► 403 / RBI(원격 브라우저 격리)           |
|  |   Deny/Isol. |                                                 |
|  +--------------+                                                 |
|         |                                                          |
|         v                                                          |
|  [단일 감사 로그 -> SIEM/SOAR 전달 (UEBA 상관분석)]                 |
+--------------------------------------------------------------------+
```

### 2.3 SASE 구성 요소 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **SD-WAN Edge (CPE/vCPE)** | 지사/원격지의 트래픽 인입 | IPsec/GRE/MPLS 터널링, 애플리케이션 인식 라우팅, DPI 기반 SLA 모니터링(지연·손실·지터), Forward Error Correction(FEC) |
| **Global PoP (Point of Presence)** | 클라우드 엣지에서 보안·라우팅 처리 | 각 PoP에 **PEP(Policy Enforcement Point)** 상주, BGP Anycast로 사용자 자동 라우팅, TLS 1.3 가속, 캐싱 |
| **Control Plane (Single Pane)** | 통합 정책 작성·배포 | SD-WAN 오케스트레이터 + SSE 정책 엔진 일체화, IaC(Terraform) 지원, GitOps 연동 |
| **Trust Broker / ZTNA Controller** | 신원·디바이스 신뢰도 평가 | SAML 2.0 / OIDC SSO, SCIM 프로비저닝, MDM(엔드포인트 신뢰도) 통합, **PE-PE(Policy Enforcement Point)** 결정 |
| **Security Stack (SSE)** | 보안 검사 5종 통합 | SWG(프록시 + SSL 복호), CASB(API·리버스·Forward 3모드), ZTNA(마이크로터널), FWaaS(IPS/IDS), DLP(정형·비정형) |
| **Digital Experience Monitoring (DEM)** | 사용자 체감 품질 측정 | 합성 트랜잭션, 패킷 레벨 UDP echo, SaaS 응답시간 모니터링, 대시보드 SLA 보고 |

### 2.4 핵심 동작 메커니즘 (ZTNA + SD-WAN)

```text
+--------------------------------------------------------------------+
|       SASE 트래픽 흐름 (사용자 -> 사설앱 / SaaS / Internet)        |
|                                                                    |
|  [사용자]   [CPE/Agent]    [PoP]      [Trust Broker]   [자원]      |
|    |            |             |              |             |       |
|    |  ①Agent   |             |              |             |       |
|    |  핸드쉐이크 |             |              |             |       |
|    +-----------►|             |              |             |       |
|    |  (Outbound)|  ②신원/디바이스 평가 요청  |             |       |
|    |            +-------------+-------------►|             |       |
|    |            |             |  ③최소권한 정책결정 |             |
|    |            |             |◄-------------+             |       |
|    |            |  ④Micro-Tunnel(per-app)|             |       |
|    |            |◄------------+              |             |       |
|    |  ⑤앱접근   |             |  ⑥매트릭스 터널 경로 |             |
|    |◄-----------+             +-------------+------------►|       |
|    |            |             |  (mTLS/QUIC)  |             |       |
|    |            |  ⑦SSL Inspection & DLP  |             |       |
|    |            |             +-------------+------------►|       |
|    |            |             |   (SaaS)     |             |       |
|    |            |             |  ⑧Forward Proxy  |             |
|    |            |             +-------------+------------►|       |
|    |            |             |  (Internet)  |             |       |
+--------------------------------------------------------------------+
```

**핵심 포인트**:
- **ZTNA는 기본적으로 "Outbound-initiated"**: 사용자가 능동 터널을 개설해 외부에서 내부로 트래픽이 들어오지 못하게 한다 -> 방화벽 인바운드 룰 오픈 불필요, 노출 면적 최소.
- **Microsegmentation**: 사용자 -> 앱 1:1 터널(per-app). 한 앱 인증이 다른 앱 접근을 자동 허용하지 않음(반면 VPN은 네트워크 레벨 통과 후 횡적 이동 가능).
- **SD-WAN 동적 경로**: SaaS 응답시간이 200ms 초과 시, FEC + 동적 경로 우회(예: MPLS -> LTE/5G)로 SLA 유지.

### 2.5 핵심 파라미터 및 알고리즘

| 영역 | 핵심 파라미터/알고리즘 | 영향 |
| :--- | :--- | :--- |
| **라우팅** | BGP Anycast, ECMP((Equal-Cost Multi-Path), Longest Prefix Match | PoP 자동 선택, 글로벌 부하 분산 |
| **암호화** | TLS 1.3, QUIC(UDP 443), mTLS, ChaCha20-Poly1305 | 핸드쉐이크 1-RTT, 모바일 환경 최적 |
| **신원 평가** | Risk Score = w₁·Device + w₂·Geo + w₃·Behavior + w₄·Time | 동적 Step-up 인증, ML 기반 이상행위 |
| **DLP** | ECM(Exact Data Matching), Fingerprinting, ML-NLP | 정형(주민번호)/비정형(설계도) 동시 탐지 |
| **DPI** | IPFIX / NetFlow v9 + DPI(Deep Packet Inspection) | 애플리케이션 인식, SLA 측정 |
| **암호화 가속** | AES-NI, QAT, SR-IOV | 100Gbps 라인레이트 SSL Inspection |
| **장애 대응** | BFD(Bidirectional Forwarding Detection) 50ms, Fast Reroute | 터널 페일오버 < 1초 |

- **📢 섹션 요약 비유**: SASE의 **Trust Broker**는 공항의 **"스마트 출입국 심사대"** 와 같다. 여권(ID)·탑승권(디바이스)·짐 검색(DLP)·신체검색(ZTNA)을 모두 한 위치에서 실시간으로 결정해, 통과하면 목적지 게이트까지만 열어주고 그 너머는 절대 들여다보지 못하게 막는다.

---

## Ⅲ. 비교 및 연결

### 3.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 465 / 800

<- **이전**: [464. SWG 보안 웹 게이트웨이 클라우드](/studynote/13_cloud_architecture/06_exam_summary/464_swg_secure_web_gateway_cloud/)
**다음**: [466. 클라우드 데이터 주권 지역 규제 대응](/studynote/13_cloud_architecture/06_exam_summary/466_cloud_data_sovereignty_regional_regulation/) ->

---
