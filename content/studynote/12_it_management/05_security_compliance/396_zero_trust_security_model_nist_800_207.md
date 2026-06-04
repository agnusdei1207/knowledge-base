+++
title = "396. 제로 트러스트 보안 모델 NIST 800-207 (Zero Trust Security Model NIST 800-207)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NIST SP 800-207은 "Never Trust, Always Verify"를 원칙으로, 네트워크 위치(내부/외부)에 따른 암묵적 신뢰를 모두 제거하고 Policy Engine(PE)·Policy Administrator(PA)·Policy Enforcement Point(PEP) 3계층 결정 구조로 자원 접근을 **주체·자산·행위 컨텍스트 기반의 동적 최소권한**으로 통제하는 보안 아키텍처 모델이다.
> 2. **가치**: Google BeyondCorp 사례에서 VPN 의존도를 100% -> 0%로 줄이고 사용자 생산성을 30% 이상 회복했으며, 마이크로세그먼테이션 기반 Lateral Movement 차단으로 랜섬웨어 침해 평균 탐지시간(MTTD)을 약 78% 단축(Forrester, 2023)시키는 등 **평면 네트워크·원격근무·하이브리드 멀티클라우드 환경의 보안을 획기적으로 강화**한다.
> 3. **판단 포인트**: 적용 시 (a) ID 거버넌스(IdP)·(b) 디바이스 신뢰(EDR/MTLS)·(c) 마이크로세그먼테이션(Overlay Network)·(d) 정책 표준화(Cedar/Rego 등)의 성숙도가 결정적이며, **모든 트래픽을 검사할 경우 성능 병목과 운영 복잡도(alert fatigue)**라는 트레이드오프를 어떻게 SLA 기반 Risk Scoring으로 흡수할지가 핵심 설계 판단 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적 **Castle-and-Moat(성벽형) 보안**은 내부망을 신뢰(Implicit Trust), 외부망을 불신(Explicit Mistrust)이라는 이분법으로 구분했다. 그러나 ① 코로나19 이후의 대규모 원격/하이브리드 근무, ② AWS·Azure·GCP·SaaS로 확산된 자산의 외부화, ③ SolarWinds·Colonial Pipeline·Kaseya VSA처럼 **공급망·내부 자격증명 침해**가 빈번해지면서 "한번 내부에 들어오면 자유롭게 이동 가능"한 평면 네트워크(Flat Network)는 더 이상 안전하지 않게 되었다.

NCC Group의 2023 Threat Pulse에 따르면 전체 침해 사고의 **68%가 Lateral Movement 단계**에서 피해가 확산되었고, 2010~2020년 Verizon DBIR 데이터에서는 자격증명 도용(Breach)이 전체 침투의 **약 80%**를 차지했다. 이는 **신뢰 경계(Trust Boundary) 자체가 모호해진 상황**에서 "위치를 기반으로 한 접근 통제"가 무의미해졌음을 의미한다.

따라서 NIST SP 800-207(2020년 8월 공표, Jonathan M. Hatfield 저)은 **자원이 위치에 무관하게 보호**되고, **모든 접근 요청이 인증·인가·암호화·로깅**되는 "제로 트러스트" 모델을 다음과 같이 정의한다: *"Zero trust is a set of cybersecurity principles… a security model, a set of system design principles, and a coordinated cybersecurity and system management strategy based on an acknowledgement that threats exist both inside and outside of traditional network boundaries."*

```text
[기존 Castle-and-Moat vs Zero Trust 비교]

  (기존) Castle-and-Moat                (제로 트러스트)
  +--------------+                  +--------------------------+
  |   External   |                  |  Subject(사용자/디바이스) |
  |  (Untrusted) |                  |   v 인증·디바이스 상태  |
  |      |       |                  |   PE(Policy Engine)     |
  | [Firewall]   |                  |      | Trust Algorithm |
  |      |       |                  |   PA(Policy Admin)     |
  |  Internal    |                  |      v allow/deny       |
  | (Trusted) ⚠  | -- 암묵적 신뢰 -> |   PEP(Enforcement)     |
  |  App / DB    |                  |   ↗        ↘           |
  +--------------+                  | mTLS 검증   DB 암호화   |
                                    +--------------------------+
     • 한 번 통과 시 내부 자유 이동       • 위치 무관, 매 요청 검증
     • 침해 시 Lateral Movement 용이     • 마이크로세그먼트로 차단
     • VPN 의존 -> 확장성·성능 저하       • SDP/SD-WAN으로 대체
```

**배경이 된 4가지 기술·환경 변화**

| 변화 | 영향 |
| :--- | :--- |
| 클라우드·SaaS 전환 | 데이터가 다수의 VPC/Region/Tenant에 분산 -> 단일 DMZ로 보호 불가 |
| 모바일·원격 근무 | User가 항상 사내망에 있지 않음 -> VPN Concentrator 병목·암묵적 신뢰 부적합 |
| 공급망·내부자 위협 | 신뢰받는 내부 ID가 침해되어도 이를 탐지할 장치 부재 |
| 규제·컴플라이언스 강화 | GDPR·개인정보보호법·DORA(유럽)·Executive Order 14028(미국) 모두 "Zero Trust Architecture" 채택 권고 |

- **📢 섹션 요약 비유**: 기존 보안이 "회사 사옥 입구에서 신분증 한 번 확인하고 복도·회의실·서버실까지 자유 출입"하는 방식이라면, **제로 트러스트**는 "각 방(자원)마다 도어락이 있고, 입장할 때마다 신분증·얼굴·예약 현황·오늘의 건강검진 결과까지 다시 확인하는" 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

NIST 800-207의 ZTA 논리 아키텍처는 **3개의 핵심 제어 평면(Control Plane)** 과 **자원 평면(Resource Plane)** 으로 구성된다. 모든 접근 결정은 **Trust Algorithm(TA)** 이 Policy Engine(PE)을 통해 산출하고, Policy Administrator(PA)가 PEP로 명령을 내린다.

```text
[ZTA Logical Architecture — NIST SP 800-207 Figure 2 기반]

   +-------------------  Control Plane  ---------------------+
   |                                                          |
   |   Subject DB    Asset DB    Policy Store    SIEM         |
   |      |             |             |            ^          |
   |      v             v             v            |          |
   |   +------------------------------------+      |          |
   |   |   Policy Engine(PE)                |-- Threat Intel |
   |   |  - Trust Algorithm 입력 7~11개     |   CDM / EDR    |
   |   |  - 점수 기반 allow/deny/deny+log   |   PKI / IdP    |
   |   +------------+-----------------------+                |
   |                v                                         |
   |   +------------------------------------+                |
   |   |   Policy Administrator(PA)         |                |
   |   |  - 세션 토큰 발급/폐기              |                |
   |   |  - PEP에 명령 전달                  |                |
   |   +------------+-----------------------+                |
   +----------------+-----------------------------------------+
                    |  ^   정책 동기화 (Open Policy Agent/OPA,
                    v  |   Cedar, XACML, RADIUS CoA, gNMI)
   +---------------- Resource Plane --------------------------+
   |  PEP-1 (Gateway / NGFW / SDP-GW)  -- mTLS -->  App-API  |
   |  PEP-2 (Service Mesh Sidecar)     -- mTLS -->  MicroSvc |
   |  PEP-3 (CASB / API Gateway)       -- JWT  -->  SaaS     |
   |  PEP-4 (DB Proxy / Vault Agent)   -- TLS  -->  Postgres  |
   +---------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Policy Engine(PE)** | 접근 결정(Allow/Deny/Deny+Log) 산출 | OPA(Open Policy Agent)·Amazon VPC Reachability Analyzer·Azure Policy·Google IAM Conditions·Cedar(Auth0/Aserto)에서 Rego/Cedar DSL로 정책 평가. Trust Score = w₁·DeviceCompliance + w₂·UserRisk + w₃·TimeOfDay + w₄·GeoVelocity + w₅·SensitivityOfAsset |
| **Policy Administrator(PA)** | PE 결정을 PEP로 전달, 세션 토큰 발급/폐기 | RADIUS Change-of-Authorization(CoA)·OAuth 2.0 Authorization Server·SAML 2.0 IdP(Okta, Azure AD, PingFederate)·SPIFFE/SPIRE Workload Identity |
| **Policy Enforcement Point(PEP)** | 자원 앞단에서 데이터 경로 차단·암호화·로깅 | NGFW(PAN-OS 10.2+)·Service Mesh(Istio Ambient Mesh, Linkerd 2.14)·SDP Gateway(Zscaler ZPA, Cloudflare Access, Appgate SDP)·CASB(Netskope, Microsoft Defender for Cloud Apps)·DB Proxy(HashiCorp Boundary, Crunchy Proxy) |
| **Continuous Diagnostics & Mitigation(CDM)** | 디바이스·자산의 실시간 상태(포스처·패치·EDR) 수집 | Microsoft Intune·Jamf Pro·CrowdStrike Falcon·SentinelOne Singularity·Tanium |
| **Threat Intelligence / SIEM** | 글로벌 위협 IP·IOC·UEBA 정보 | MISP·Mandiant Advantage·Microsoft Sentinel·Splunk ES·Elastic Security·Anomalo |
| **ID·PKI / Device Trust** | mTLS·디바이스 인증서 발급 | SCEP/NDES·EJBCA·DigiCert One·HashiCorp Vault PKI·SPIFFE SPIRE·ACME |
| **Data Access Policy / Industry Compliance** | 데이터 분류·규제 매핑 | Microsoft Purview·Collibra·OneTrust·BigID·Immuta |

**Trust Algorithm 입력 11종(NIST 800-207 §3.3)**
1. Subject Database (사용자/서비스 계정) 2. Asset Database (HW·SW 인벤토리) 3. Resource Requirements (RPS, Throughput) 4. ID Management (SSO, MFA) 5. Threat Intelligence 6. PKI / Certificate Status 7. SIEM 8. CDM 9. Data Access Policy 10. PKI 11. Industry/Regulatory Compliance.

가중치(w)는 일반적으로 ATO(Authority To Operate) 절차의 **Risk Assessment** 단계에서 정의하며, FedRAMP High/Moderate 등급 별로 가중치 템플릿이 다르다. 예) **NIST 800-207A**는 Hybrid Multi-Cloud 시나리오에서 *시간 기반 가변 가중치(Time-Decay Weighting)* 모델을 권고한다.

**핵심 메커니즘 — "검증·최소권한·가정적 침해"**

1. **Verify Explicitly**: 모든 요청에 대해 ID + Device Posture + Geo + Time + Resource Sensitivity를 5-tuple 이상의 컨텍스트로 인증한다. (예: `device.managed=true AND mfa=true AND country in {KR,US,JP} AND patch_level >= 2024-01 AND asset.tags has "PII"`)
2. **Least-Privilege Access**: Just-in-Time(JIT)·Just-Enough-Access(JEA) 패턴. HashiCorp Vault의 *Dynamic Secrets*나 AWS IAM Identity Center의 *Permission Sets*가 대표 구현이다.
3. **Assume Breach**: 침해는 이미 발생했다는 전제로 Microsegmentation·Lateral Movement 차단. Istio AuthorizationPolicy의 DENY-all + 화이트리스트 방식을 사용한다.
4. **Continuous Verification**: 1회 로그인이 아닌 **세션 중 재평가** — Risk Score가 임계치 초과 시 RADIUS CoA로 즉시 세션 차단(Step-Down Auth) 또는 MFA 재요구.
5. **End-to-End Encryption**: mTLS 1.3, Wireguard, QUIC, IPsec ESP. Service Mesh에서는 Istio의 STRICT mTLS 모드, SPIFFE ID 기반 Workload Identity 사용.

- **📢 섹션 요약 비유**: PE는 **법원(판사)**, PA는 **교도관**, PEP는 **문지기(게이트)** 다. 법원이 신분증·혈중알코올·차량번호판·신고 이력까지 검토해 "출입 허가" 판결을 내리면, 교도관이 그 판결을 받아 문지기에게 전달하면 문지기가 실제로 문을 열어주는 3단계 시스템이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Castle-and-Moat (전통 경계 보안)** | **Zero Trust Architecture (NIST 800-207)** |
| :--- | :--- | :--- |
| **신뢰 경계** | 사내망 내부 = 신뢰, 외부 = 불신 | 네트워크 위치 무관, 모든 트래픽 검증 |
| **인증 단위** | 1회 로그인 -> 세션 만료까지 신뢰 | 매 요청/리소스 단위 재인증 (RFC 8707 Token Exchange) |
| **암호화** | 데이터 평문 전송 많음 (East-West) | mTLS·WireGuard·IPsec으로 종단간 암호화 |
| **침해 대응** | 외부 침입 차단 중심, 내부 Lateral Movement 대응 미흡 | Microsegmentation + UEBA로 Lateral Movement 차단 |
| **확장성** | VPN·방화벽 정책 확장으로 병목 | SDP / SASE로 글로벌 분산 엣지에서 인증 처리 |
| **비용 모델** | CAPEX 중심 (HW Appliance) | OPEX 중심 (구독형 SaaS, Zscaler/Netskope/Prisma) |
| **구현 성숙도** | 높음 (20년+) | 단계적(SASE->SDP->Mesh), 조직·IAM 성숙도 의존 |
| **컴플라이언스** | ISO 27001, PCI-DSS v3.2.1 | EO 14028, DORA, CISA Zero Trust Maturity Model v2.0 |
| **대표 사례** |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 396 / 800

<- **이전**: [395. 클라우드 보안 인증 CSAP FedRAMP](/knowledge-base/studynote/12_it_management/05_security_compliance/395_cloud_security_certification_csap_fedramp/)
**다음**: [397. 공급망 보안 SBOM 소프트웨어 구성 분석](/knowledge-base/studynote/12_it_management/05_security_compliance/397_supply_chain_security_sbom_sca/) ->

---
