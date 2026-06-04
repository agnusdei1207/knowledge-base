+++
title = "595. 보안 감리 제로 트러스트 적합성 평가 (Security Audit Zero Trust Fitness)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

# 595. 보안 감리 제로 트러스트 적합성 평가 (Security Audit Zero Trust Fitness)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NIST SP 800-207 기반의 'Never Trust, Always Verify(절대 신뢰 금지, 항상 검증)' 원칙을 PE(Policy Engine)·PA(Policy Administrator)·PEP(Policy Enforcement Point) 3대 컴포넌트로 구현하고, CISA Zero Trust Maturity Model(ZTMM) v2.0의 5대 필라(Identity, Device, Network, Application/Workload, Data)와 3대 역량(Visibility/Analytics, Automation/Orchestration, Governance) 축으로 조직의 도입 성숙도를 측정·감리하는 평가 체계
> 2. **가치**: 적대적 침투 시 평균 탐지·대응 시간을 MTTD 200일 -> 12시간, MTTR 80일 -> 1시간으로 단축(IBM Cost of Data Breach 2023 기준 ZT 도입 조직), ISMS-P·클라우드 보안 인증(CSAP)·전자금융감독규정 등 다중 컴플라이언스 통제 매핑 효율 70%^, 측면 이동(Lateral Movement) 차단율 평균 85% 이상 확보
> 3. **판단 포인트**: 마이크로세그멘테이션 단위(워크로드/서브넷/포트 vs L7 애플리케이션) 결정, 컨텍스트 속성 가중치(디바이스 상태 30% vs 신원 40% vs 행위 30%) 튜닝, 클라우드-온프레미스 하이브리드 환경의 정책 일관성(IdP 페더레이션 vs 로컬 IdP) 확보, 그리고 사용자 경험(UX)과 보안 마찰(friction) 간의 균형점이 핵심 의사결정 요소

---

## Ⅰ. 개요 및 필요성

### 1.1 패러다임 전환의 배경: 경계 기반 보안의 붕괴

전통적 'Castle & Moat' 모델은 내부 네트워크를 암묵적으로 신뢰하고 외부에서 들어오는 트래픽만 차단하는 **Perimeter-Centric Security**였다. 그러나 다음과 같은 구조적 한계로 2020년 이후 대형 보안 사고의 주 원인이 되었다.

| 사건명 | 연도 | 피해액/규모 | 침투 경로 | 근본 원인 |
| :--- | :---: | :---: | :--- | :--- |
| SolarWinds Orion | 2020 | 18,000개 조직 침해 | SW 공급망(Supply Chain) | 내부망 신뢰 + 코드 서명 우회 |
| Colonial Pipeline | 2021 | $4.4M 랜섬웨어 | 사용된 VPN 미사용 계정 | Legacy VPN, MFA 부재 |
| Microsoft Exchange | 2021 | 250,000+ 서버 | ProxyLogon 제로데이 | 내부 측면 이동(Lateral Movement) 가능 |
| MOVEit Transfer | 2023 | 2,700+ 조직, 93M 명 | SQL Injection | 신뢰된 내부 서비스의 권한 과다 |

이들 모두 **"Once inside, full access"**라는 경계 모델의 맹점을 악용했다. 한국도 동일하다. 2022년 카카오 IDC 화재, 2023년 SK C&C 개인정보 유출 등 내부 신뢰 가정의 실패가 대형 피해로 이어졌다.

### 1.2 제로 트러스트의 정의와 등장

John Kindervag(Forrester Research, 2010)이 처음 제창한 **Zero Trust(제로 트러스트, ZT)**는 "신뢰는 취약점이다(Trust is a vulnerability)"라는 전제에서 출발한다. NIST SP 800-207(2020.8 발행)은 이를 다음과 같이 정의한다.

> *"Zero trust is a cybersecurity paradigm focused on resource protection and the premise that trust is never granted implicitly but must be continually evaluated."*

### 1.3 보안 감리(Security Audit)에서의 제로 트러스트 적합성 평가의 위치

한국의 정보통신망법 §48(정보통신망의 안정성 확보) 및 클라우드 보안 인증(CSAP)·ISMS-P 인증심사원은 "기술적·관리적·물리적 보호조치"의 이행 여부를 평가한다. 그러나 전통적 감리 체크리스트는 '방화벽 운영', 'IDS/IPS 설치' 등 **구성(Presence) 중심**으로, 진보된 공격(APT, 내부자 위협, 공급망 공격)에 대한 실질적 방어력 평가는 미흡했다.

제로 트러스트 적합성 평가는 다음 3가지 목적을 수행한다.

1. **성숙도 진단(Maturity Assessment)**: 조직의 ZT 도입 수준을 'Traditional -> Initial -> Advanced -> Optimal' 4단계로 측정
2. **통제 매핑(Control Mapping)**: NIST 800-207 -> ISO 27001:2022 Annex A, ISMS-P 인증기준, CSAP 통제항목 간 1:N 매핑
3. **리스크 정량화(Risk Quantification)**: ZT 도입 전·후의 Attack Surface, Blast Radius, MTTD/MTTR 변화 측정

### 1.4 ASCII 컨셉 다이어그램

```text
   [기존 경계 보안 모델]                 [제로 트러스트 모델]

   +-----------------+            +---------------------------+
   |  신뢰 영역(Trust)|            |  정책 엔진(Policy Engine) |
   |  +------------+ |            |  +---------------------+  |
   |  | 내부 사용자 | |            |  | Trust Algorithm (TA)|  |
   |  | 내부 서버   | |            |  | Score = f(ID, Dev, |  |
   |  | DB         | |            |  |   Beh, Context)    |  |
   |  +------------+ |            |  +---------------------+  |
   |   자유로운 이동  |            |             |             |
   +--------+--------+            +-------------|-------------+
            |                                  | Allow/Deny
   - - - - -|- - - - - - - - -                v
   +--------v--------+            +---------------------------+
   |  비신뢰(Distrust)|            |   PEP(Policy Enforcement  |
   |  +------------+ |            |    Point) - 게이트웨이     |
   |  | 외부       | |            +-------------+-------------+
   |  +------------+ |                          |
   +-----------------+           +--------------+--------------+
                                 |  Resource (앱/데이터)      |
   ❌ 일단 침투 -> 전면 노출      |  + 암호화(Crypto)            |
   ❌ 측면 이동 차단 불가        |  + 마이크로세그멘테이션       |
                                 +----------------------------+
                                 ✅ 매 요청·매 세션 검증
                                 ✅ 최소 권한(Least Privilege)
                                 ✅ 가정 위반 시(Assume Breach)
```

### 1.5 기존 vs 신규 패러다임 비교

| 평가 차원 | 경계 기반(Perimeter) | 제로 트러스트(Zero Trust) |
| :--- | :--- | :--- |
| 신뢰 부여 시점 | 1회 인증(Login) | 매 요청·연속(Continuous) |
| 네트워크 위치 | 사설 IP = 신뢰 | 위치 무관(Location-Agnostic) |
| 권한 부여 단위 | 사용자(User) | 사용자+디바이스+행위+컨텍스트 |
| 내부 위협 대응 | 약함(기본 허용) | 강함(기본 차단) |
| 클라우드 친화성 | 낮음(리프트앤시프트) | 높음(CASB/ZTNA native) |
| 감사 증적(Audit Trail) | 네트워크 로그 위주 | 신원·행위·정책 결정 로그 통합 |

- **📢 섹션 요약 비유**: 경계 보안은 "우리 동네에 들어오면 다 이웃이니까 도움 요청 안 해도 된다"지만, 제로 트러스트는 "동네 사람이든 타지 사람이든, **매번 신분증과 도움 요청 사유**를 확인하는 24시간 경비 시스템"과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 NIST SP 800-207 참조 아키텍처

```text
   +--------------------------------------------------------------+
   |                      Control Plane (제어 평면)                |
   |                                                              |
   |   +------------------+      +------------------+             |
   |   |  Policy Engine   |<------>|  Policy Admin    |             |
   |   |  (PE)            |      |  (PA)            |             |
   |   |                  |      |                  |             |
   |   | • 접근 결정      |      | • 세션 발급/해지 |             |
   |   | • Trust Score    |      | • PEP 명령       |             |
   |   | • 외부 입력 통합  |      | • 토큰/자격증명  |             |
   |   +--------+---------+      +--------+---------+             |
   |            |      결정(Allow/Deny)   |                        |
   |            +------------+------------+                        |
   |                         v                                     |
   |   +-----------------------------------------+                 |
   |   |   외부 신호/Context (CDR, IdP, SIEM)    |                 |
   |   |   - SIEM: Splunk / Sentinel / QRadar    |                 |
   |   |   - IdP: Okta / Azure AD / Ping        |                 |
   |   |   - MDM/UEM: Intune / Jamf / Knox      |                 |
   |   |   - Threat Intel: MISP / Recorded Fut. |                 |
   |   +-----------------------------------------+                 |
   +--------------------------+-----------------------------------+
                              | 명령/자격증명
                              v
   +--------------------------------------------------------------+
   |                      Data Plane (데이터 평면)                 |
   |                                                              |
   |  Subject(User/Device)                                         |
   |       |  ① Access Request                                     |
   |       v                                                       |
   |  +------------------+  ② Verify  +------------------------+   |
   |  |  PEP             |----------->|  Resource               |   |
   |  |  (게이트 에이전트)|            |  (앱/DB/Storage)        |   |
   |  |  - ZTNA Gateway  |  ④ Forward|  - 암호화 데이터        |   |
   |  |  - mTLS 종점     |<-----------|  - 태그/라벨 기반 분류  |   |
   |  |  - mDNS 차단     |  ③ Allow  |                          |   |
   |  +------------------+            +------------------------+   |
   +--------------------------------------------------------------+
```

### 2.2 핵심 컴포넌트 및 기술 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Policy Engine (PE)** | 접근 결정(Grant/Deny/Revoke) | Trust Algorithm = f(Identity, Device Posture, Behavioral Analytics, Time/Location, Data Sensitivity); 결정은 일반적으로 50~300ms 이내 응답 필요; AWS IAM Access Analyzer, Azure AD Conditional Access Policy가 대표 구현 |
| **Policy Administrator (PA)** | PE 결정 기반 세션/커넥션 수립·해지 | PEP 명령 발행, 토큰/세션 라이프사이클 관리; 재인증 주기(기본 1~24h, 고위험 리소스 15~30분); OAuth 2.0+JWT(15분 TTL) 또는 SAML 2.0 단언 활용 |
| **Policy Enforcement Point (PEP)** | 모든 트래픽 게이트키핑, 암/복호화 | L4~L7에서 동작: ZTNA 게이트웨이(Zscaler ZIA/ZPA, Cloudflare Access, Netskope), CASB(Microsoft Defender for Cloud Apps), NAC(Aruba ClearPass); mTLS 1.3, WireGuard, QUIC 등 종단간 암호화 적용 |
| **Subject (주체)** | 사용자/디바이스/서비스 계정 | 인간(Employee/Contractor), 비인간(Service Account, IoT, RPA Bot); MFA(FIDO2/WebAuthn 권장), 지속적 인증(Continuous Authentication) 적용; SCIM으로 자동 프로비저닝 |
| **Resource (자원)** | 보호 대상 앱/데이터/API | 모든 자산에 메타데이터 태그 부착(분류·소유자·민감도); 데이터 암호화-at-rest(AES-256-GCM), in-transit(mTLS), in-use(Confidential Computing/SEV-SNP); DLP(CrowdStrike Falcon, Symantec DLP)와 연동 |
| **Data Sources (외부 신호)** | PE에 컨텍스트 제공 | SIEM(Splunk Enterprise Security, Microsoft Sentinel), EDR(XDR), UEBA(Exabeam, Gurucul), Threat Intel(TAXII/STIX 2.1), Asset DB(CMDB), CDM(Federal CDM Program 참조) |

### 2.3 CISA Zero Trust Maturity Model(ZTMM) v2.0 — 5 Pillars × 3 Capabilities

```text
              Visibility/Analytics    Automation/Orchestration   Governance
              (가시성/분석)           (자동화/오케스트레이션)        (거버넌스)
                          |                     |                     |
   +----------------------
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 595 / 600

<- **이전**: [594. 데이터 품질 감리 정합성 완전성 진단](/knowledge-base/studynote/11_design_supervision/06_exam_summary/594_data_quality_audit_consistency_completeness/)
**다음**: [596. 성능 감리 부하 테스트 병목 진단](/knowledge-base/studynote/11_design_supervision/06_exam_summary/596_performance_audit_load_test_bottleneck/) ->

---
