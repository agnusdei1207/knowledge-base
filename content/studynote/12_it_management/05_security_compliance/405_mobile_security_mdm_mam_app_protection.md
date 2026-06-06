---
title: "Mobile Security MDM MAM App Protection"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MDM(단말 통제)과 MAM(앱 통제)은 **iOS Managed App Configuration / Android Enterprise Work Profile / AppConfig Community** 기반의 정책 채널을 통해 **단말 전체 보호**(Full Device)와 **앱 단위 보호**(App-Level Sandboxing)를 각각 제공하며, 앱 보호(App Protection)는 **MAM SDK·앱 래핑(App Wrapping)·네이티브 컨테이너**를 통해 **DLP·인증·암호화·원격 제어**를 앱 레이어에서 강제하는 3계층 모바일 보안 체계다.
> 2. **가치**: 기업은 BYOD 환경에서도 **단말의 개인 데이터는 비가시화, 업무 데이터만 선택적 제거(Selective Wipe)**가 가능하여 **유출사고 시 복구 비용 70%v, 감사 컴플라이언스(ISO 27001·ISMS-P·GDPR) 통과율 90%^**, 사용자 디바이스 교체율 40% 절감 효과를 얻는다.
> 3. **판단 포인트**: **MDM 등록(Enrollment) vs MAM-only vs Container-only** 트레이드오프, **iOS vs Android(Samsung Knox / AOSP)** 정책 호환성, **네이티브 SDK 통합 vs 앱 래핑 vs AppConfig** 도입 복잡도, 그리고 **MAM SDK의 제로트러스트 조건부 액세스(Conditional Access with App Protection Policy) 연계** 여부가 설계의 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

모바일 보안은 PC-중심의 경계 보안(Perimeter Security) 모델이 무력화된 **"IT 경계의 소멸(Post-Perimeter Era)"** 시대의 핵심 통제 영역이다. 코로나19 이후 국내 기업의 모바일 업무 비중은 평균 68%(2024년 KISA 조사 기준)까지 증가했고, 그에 따라 **공격 표면(Attack Surface)**은 PC·노트북에서 **iOS/Android 단말 + 업무 앱 + 클라우드 SaaS**로 급속히 확장되었다. 전통적인 모바일 단말 관리(MDM)는 단말 전체를 원격 제어(Wipe·Lock)하는 방식이라 **BYOD(Bring Your Own Device)** 환경에서 개인정보 침해·사용자 저항·법적 이슈가 발생했다. 이를 해결하기 위해 등장한 것이 **MAM(Mobile Application Management)**과 **앱 보호(App Protection Policy, 이하 APP)**이며, 이는 단말이 아닌 **앱 단위 컨테이너**에서만 정책(복사·붙여넣기 차단, 스크린샷 차단, 오프라인 PIN, 데이터 암호화, 위치 기반 액세스)을 강제한다.

특히 2023년 국내 개인정보보호법 개정과 2024년 공공부문 마이데이터 사업 확대로 인해, **공공·금융·의료** 분야는 **DLP(데이터 유출 방지) + MAM SDK 통합 + 조건부 액세스(CA)** 3종 세트를 의무화하고 있다.

```text
[모바일 보안 위협 환경과 통제 계층의 진화]

  +--------------------------- 기존 PC 중심 보안 ----------------------------+
  |  +----------+    +----------+    +----------+    +----------+           |
  |  | Firewall | ->  |   NAC    | ->  |   DLP    | ->  |   EDR    |           |
  |  +----------+    +----------+    +----------+    +----------+           |
  |       v                                                           단말: PC/노트북 고정     |
  +------------------------------------------------------------------------+
                                       |
                                       | 경계 소멸 / 모바일·클라우드 확산
                                       v
  +--------------------------- 모바일·제로트러스트 보안 --------------------------+
  |  +----------+    +----------+    +----------+    +----------+    +----------+|
  |  |   MDM    | ->  |   MAM    | ->  |   APP    | ->  |  ZTNA    | ->  | CASB/SWG ||
  |  |(단말제어)|    |(앱배포·정책)|   |(앱보호SDK)|   |(앱터널)  |    |(SaaS통제)||
  |  +----------+    +----------+    +----------+    +----------+    +----------+|
  |       v             v             v             v             v              |
  |    단말 무결성    앱 카탈로그    데이터 보호    마이크로       SaaS 가시성      |
  |    Jailbreak     정책배포      DLP·암호화     세그멘테이션  Shadow IT 탐지   |
  |    검출·원격제어  SSO연동      인증·접근통제    IdP통합        토큰통제         |
  +----------------------------------------------------------------------------+
```

**왜 이제 MDM·MAM·앱 보호가 필수인가?**
- **① 위협 정교화**: 2024년 기준 모바일 악성코드 신규 샘플 92만 종(PROMON 보고서), **Pegasus·Pegasus-type 스파이웨어**는 제로클릭으로 iOS·Android 모두 침투.
- **② 규제 강화**: 전자금융감독규정(2024 개정) §46의2는 전자금융업자에 **모바일 단말 보안 통제 항목(루팅 검출, 앱 위변조, 키보드 보안, 화면 캡처 차단)** 4종 의무화. 공공부문 ISMS-P 인증도 모바일 통제 항목을 강화.
- **③ 업무 경계의 융해**: 메신저(Slack·Teams)·문서(Office 365)·결제·인증까지 모바일로 이동 -> **데이터 주권(Data Sovereignty)** 확보 필요.
- **④ BYOD 보편화**: 직원의 78%가 개인 단말로 업무 처리(2024 Gartner) -> **개인 영역 비간섭, 업무 영역만 통제**하는 "이중 영역(Dual Persona)" 모델이 표준.

| 구분 | 구시대 (2008~2014) | 신시대 (2018~현재) |
|:---|:---|:---|
| 통제 단위 | 단말 전체(Full Wipe) | 앱 단위 컨테이너(Selective Wipe) |
| 정책 배포 | OTA SMS/APN 블랙박스 | OS 표준 API(APNs·FCM) + 선언형 정책 |
| 사용자 경험 | 단말 통제 -> 저항 | BYOD 친화 + 제로트러스트 적응형 |
| 데이터 보호 | VPN 터널링 | MAM SDK 내 AES-256 + 앱별 키 분리 |
| 인증 | ID/PW 단일 | IdP + 디바이스 신뢰도 + 앱 무결성(Attestation) |
| OS 종속 | iOS/Android 각자 | iOS Managed App + Android Enterprise 통일 |

- **📢 섹션 요약 비유**: MDM은 회사 차를 **회사 주차장 안에 가둬두는 방식**이고, MAM은 차 안의 **"회사 서류함이 있는 트렁크"만 잠금 장치**를 다는 방식이다. 앱 보호는 그 **서류함에 추가로 방수·방화 도장**을 찍어 회사가 필요한 부분만 안전하게 지키는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

모바일 보안 3계층은 **단말(MDM) -> 앱 배포(MAM) -> 앱 내부 보호(APP)**로 위임되며, 각 계층은 **OS 제공 API**와 **IdP(Identity Provider)**의 정책 채널을 통해 연동된다.

```text
[MDM·MAM·앱 보호 3계층 아키텍처와 정책 흐름]

  +----------------------------------- Enterprise / Cloud -----------------------------------+
  |                                                                                          |
  |   +------------+  <----- SCIM/Graph API ----->  +------------------+                        |
  |   |   IdP      |                              |  MDM/MAM Server  |                        |
  |   | (Azure AD  |  <----- OAuth 2.0 + OIDC ----> | (Intune,         |                        |
  |   |  /Okta/    |     + Conditional Access     |  Workspace ONE,  |                        |
  |   |  Ping ID)  |                              |  MobileIron,     |                        |
  |   +------------+                              |  Knox Manage)    |                        |
  |         ^                                     +------------------+                        |
  |         | PKI(클라이언트 인증서 발급)                    ^                                    |
  +---------+-----------------------------------------+--------------------------------------+
            |                                         | MDM: APNs(iOS) / FCM(Android)
            | SAML/OIDC                              | MAM: Managed App Config(JSON)
            v                                         v
  +--------------------------------------------------------------------------------+
  |                                사용자 단말 (iOS / Android)                       |
  |                                                                                  |
  |  +----------------------------+  +------------------------------------+          |
  |  |      MDM 계층(OS 통제)      |  |       MAM/APP 계층(앱 통제)         |          |
  |  |  • 프로파일 설치/제거        |  |  • 업무 앱 컨테이너 (Work Profile)  |          |
  |  |  • 비밀번호·암호화 정책      |  |  • MAM SDK 통합 앱                  |          |
  |  |  • Jailbreak/Root 검출      |  |  • 앱별 정책: PIN, 암호화, 복사차단  |          |
  |  |  • 원격 Wipe/Lock           |  |  • Selective Wipe (업무 데이터만)    |          |
  |  |  • 앱 화이트/블랙리스트      |  |  • 키오스크 모드                    |          |
  |  |  • VPN·Wi-Fi 프로파일       |  |  • App Tunnel (앱별 VPN)            |          |
  |  +----------------------------+  +------------------------------------+          |
  |            ^                                       ^                              |
  |            | OS API (iOS MDM Protocol / Android Management API)                  |
  |            |            MAM SDK (MS Intune SDK / Appdome / etc.)                 |
  +------------+----------------------------------------------------------------------+
               |
               v
  +--------------------------------------------------------------------------------+
  |  기업 리소스 (Exchange, SharePoint, Salesforce, ERP, 결재, 사내 메신저)              |
  +--------------------------------------------------------------------------------+
```

### 1. MDM (Mobile Device Management) - 단말 통제

| 하위 기술 | 설명 |
|:---|:---|
| **등록(Enrollment)** | iOS는 **DEP/MDM Enrollment**(Apple Business Manager), Android는 **Device Admin(legacy) -> Android Enterprise(DA·COPE·BYOD) -> Work Profile** 4단계 진화 |
| **프로파일(Profile)** | iOS MDM Payload(XML, MDM Protocol over APNs), Android Management API(JSON over FCM) |
| **무결성 검증** | Jailbreak/Root 검출(예: `JailMonkey`, `RootBeer` 라이브러리), Boot Integrity 검증(Samsung Knox TIMA Attestation) |
| **원격 제어** | Full Wipe, Selective Wipe(iOS: `RemoveApplication` + MDM 키 해지, Android: Work Profile 삭제) |
| **OS API** | iOS MDM Protocol(NSURLSession 기반 바이너리 프로토콜), Android `DevicePolicyManager`, `RestrictionsManager` |

### 2. MAM (Mobile Application Management) - 앱 배포·정책

| 채널 | 설명 |
|:---|:---|
| **엔터프라이즈 앱 카탈로그** | 인하우스/상용 앱 배포(iOS: `ituneservices`, Android: Managed Google Play) |
| **Managed App Config** | iOS `com.apple.configuration.managed` plist, Android `RestrictionsManager` extras(JSON) — OS 표준 정책 채널 |
| **AppConfig Community** | EMM 벤더·앱 벤더 간 표준 JSON 스키마(예: Salesforce, Office 365, WebEx) |
| **앱 래핑(App Wrapping)** | 기존 APK/IPA에 정책 엔진을 삽입(`appdome`, `MobileIron AppConnect`, `Wandera`) — 소스 코드 수정 없이 DLP 정책 적용 |
| **앱 SDK** | **MS Intune SDK, Appdome SDK, Kaspersky MDM SDK, Samsung Knox SDK** — 네이티브 통합(앱 내 분기·로직 구현 가능) |
| **앱 터널(App Tunnel)** | **Per-App VPN**(iOS `NEVPNManager` per-app, Android `VpnService` per-package) — 업무 앱만 회사 데이터센터로 우회 |

### 3. 앱 보호(App Protection Policy, APP) - 앱 내부 데이터 통제

**Microsoft Intune APP 기준 핵심 정책 항목**:
1. **액세스 요구 사항**: 업무 앱 진입 시 PIN·지문·FaceID 인증(앱 레벨)
2. **오프라인 grace period**: 네트워크 미연결 시 최대 N일 허용
3. **데이터 손실 방지(DLP)**: 클립보드·"다른 앱으로 열기(Open-in)"·"다른 앱에서 열기(Open-from)" 차단
4. **스크린샷/녹화 차단**: iOS 화면 캡처 플래그, Android `FLAG_SECURE`
5. **저장소 암호화**: FIPS 140-2 인증 라이브러리, **앱별 키 분리(App-Key Per Identity)**
6. **탈옥/루팅 시 앱 자동 잠금** + 데이터 자동 삭제
7. **선택적 초기화(Selective Wipe)**: Intune SDK의 `Wipe` API가 앱 데이터·키만 파기, 디바이스 개인 데이터는 보존
8. **네트워크 액세스**: 인증서 기반 클라이언트 인증, **HTTPS only + TLS 1.2+** 강제
9. **콘텐츠 검토**: `Microsoft Defender for Cloud Apps` 연동 -> 앱 내 다운로드/업로드 행위 모니터링

### 4. 조건부 액세스(Conditional Access) 연계 - 제로트러스트

```text
[조건부 액세스 + 앱 보호 정책 통합 흐름]

  사용자 로그인 시도
        |
        v
  +--------------------+
  | 1단계: IdP 인증     | ---> MFA 검증 (생체·OTP·FIDO2)
  | (Azure AD/Okta)    |
  +---------+----------+
            v
  +--------------------+
  | 2단계: 디바이스 신뢰 | ---> MDM 등록 여부, 컴플라이언스, Jailbreak 상태
  | (Compliance Check) |     (Intune: device.compliant = true)
  +---------+----------+
            v
  +--------------------+
  | 3단계: 앱 보호 정책 | ---> MAM SDK 초기화 시 정책 다운로드
  | (App Protection)   |     (Intune SDK: appprotection policy fetch)
  +---------+----------+
            v
  +--------------------+
  | 4단계: 앱 무결성    | ---> SafetyNet/Play Integrity / DeviceCheck
  | (App Attestation)  |     (앱 위변조·디버거 부착·에뮬레이터 검출)
  +---------+----------+
            v
       ✅ 리소스 액세스 허용 / 🚫 차단·격리·Wipe 트리거
```

**핵심 원리**: **MDM/MAM/APP는 단일 시스템이 아니라 정책의 다중 위임(Multi-Enforcement)** 구조다. OS는 표준 API(APNs·FCM·Managed App Config)로 정책을 디바이스에 푸시하고, 앱은 **MAM SDK**로 그 정책을 자기 자신의 동작에 반영한다. 이 구조에서 **IdP(Azure AD·Okta)**가 **"어떤 사용자가 어떤 디바이스로 어떤 앱에서 접근하는가"**라는 3축 컨텍스트
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 405 / 800

<- **이전**: [404. API 보안 OAuth JWT 토큰 관리](/studynote/12_it_management/05_security_compliance/404_api_security_oauth_jwt_token_management/)
**다음**: [406. IoT 보안 디바이스 인증 펌웨어](/studynote/12_it_management/05_security_compliance/406_iot_security_device_authentication_firmware/) ->

---
