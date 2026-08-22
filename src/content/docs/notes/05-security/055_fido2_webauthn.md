---
sidebar:
  order: 55
  label: "055. FIDO2•WebAuthn (FIDO2 WebAuthn)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "비패스워드 공개키 암호화 및 도메인 바인딩 피싱 저항성 표준 : FIDO2 및 WebAuthn (W3C & CTAP2)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 55
extra:
  question_no: "055"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 최신 기출, FIDO2 = W3C WebAuthn(브라우저 JS API) + FIDO Alliance CTAP2(인증기 통신), RP ID 도메인 바인딩(AitM 피싱 차단), 비대칭키 암호화, UV(User Verification) & UP(User Presence)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **FIDO2(Fast Identity Online 2)**: W3C와 FIDO Alliance가 제정한 글로벌 패스워드리스(Passwordless) 인증 표준으로, 웹 브라우저 표준 API인 **WebAuthn(Web Authentication)** 과 외부 하드웨어 인증기 통신 규격인 **CTAP2(Client to Authenticator Protocol 2)** 로 구성되어 비대칭 공개키 암호화와 피싱 저항성을 제공하는 프레임워크.
- **도메인 바인딩(RP ID / Domain Binding)**: 인증용 개인키를 생성하고 서명할 때 브라우저가 현재 접속한 서비스의 실제 최상위 유효 도메인(Origin/RP ID)을 암호학적으로 귀속시켜, 공격자가 유사 도메인(예: 피싱 사이트)을 구축하더라도 서명 검증이 물리적으로 불가능하도록 차단하는 핵심 메커니즘.

</details>

- 정의/개념: 서버에 공유 비밀(패스워드)을 보관하지 않고 사용자 기기(TPM/Secure Enclave)에 개인키를 안전하게 격리 보관하며, **도전값(Challenge) 발행 $\rightarrow$ 도메인 바인딩 $\rightarrow$ 사용자 검증(UV: 지문/PIN) 및 존재 확인(UP) $\rightarrow$ 비대칭 전자서명 $\rightarrow$ RP 서버 공개키 검증** 을 수행하는 **피싱 저항성 비패스워드 인증 아키텍처**
- 배경/필요성: 비밀번호, SMS OTP, 푸시 알림 등 기존 인증 수단이 역프록시 중간자(AitM) 피싱 공격 도구(Evilginx)와 크리덴셜 스터핑에 의해 체계적으로 무력화되는 구조적 취약성을 극복할 요구

#### 한줄 요약
- WebAuthn 브라우저 API와 CTAP2 인증기 통신을 통해 도메인 바인딩 기반 피싱 저항성 공개키 인증을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **사용자 검증(User Verification, UV) vs 사용자 존재(User Presence, UP)**:
  - **UP (User Presence)**: 사용자가 물리적으로 그 자리에 있음을 증명하기 위해 보안키의 정전식 터치 버튼을 누르는 행위 (원격 악성코드의 무단 자동 서명 방어).
  - **UV (User Verification)**: 기기의 실제 소유자 본인임을 증명하기 위해 생체인식(지문, FaceID)이나 기기 로컬 PIN 번호를 입력하는 행위.

</details>

- **서버 측 비밀정보 부재 (Shared Secret Elimination)**: RP 서버에는 오직 공개키(Public Key)만 보관되므로, 서버 데이터베이스가 전면 유출되어도 자격증명 도용 불가능
- **완벽한 피싱 저항성 (Phishing Resistance)**: 브라우저 엔진이 `window.location.origin`을 강제로 수집하여 서명 데이터에 주입하므로 중간자(MitM) 피싱 사이트 우회 불가
- **하드웨어 격리 실행 환경 (Secure Enclave / TPM)**: 비공개키(Private Key)가 호스트 OS 메모리에 로드되지 않고 보안 하드웨어 내부에서만 연산 및 유지

#### 한줄 요약
- 서버 공유 비밀 소거, 도메인 바인딩 피싱 저항성, UV/UP 물리적 검증, 하드웨어 칩 격리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **FIDO2 3대 핵심 아키텍처 구성요소**:
  1. **Relying Party (RP 서버)**: 인증을 요청하고 공개키를 등록/검증하는 백엔드 웹 애플리케이션.
  2. **FIDO2 Client (웹 브라우저 / OS)**: `navigator.credentials.create()/get()` 자바스크립트 WebAuthn API를 구동하고 도메인 무결성을 보증하는 에이전트.
  3. **FIDO2 Authenticator (인증기)**: 스마트폰 생체인식 모듈(Platform Authenticator) 또는 USB/NFC YubiKey(Cross-Platform Authenticator).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. Relying Party (RP 서버: 웹/앱 서비스 백엔드) ]                     │
│  ├─ 챌린지 생성: 암호학적 일회용 난수(Challenge) + 기대 RP ID(`corp.com`)│
│  └─ 자격증명 저장소: 사용자 계정별 등록된 공개키(Public Key) 보관      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (1. WebAuthn 옵션 전달 / HTTPS)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. FIDO2 Client (웹 브라우저 / 플랫폼 OS: WebAuthn API) ]             │
│  ├─ 브라우저 보안 컨텍스트 검증: 실제 접속 URL(`Origin: https://corp.com`) │
│  └─ [ 가짜 피싱 도메인 감지 시 ➔ 인증기 호출 자체를 즉각 중단 ]         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (2. CTAP2 프로토콜: USB / BLE / NFC / IPC)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. FIDO2 Authenticator (하드웨어 인증기: TPM / Secure Enclave) ]      │
│  ├─ UP / UV 확인: 생체인식(지문) 또는 물리 터치 버튼 검증                │
│  ├─ ClientDataJSON(도메인+챌린지) 해시값에 개인키로 전자서명(Assertion) │
│  └─ [ 서명 결과 반환 ➔ RP 서버가 공개키로 대조하여 최종 로그인 승인 ]  │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: RP 서버의 챌린지가 WebAuthn 브라우저의 도메인 검증을 거쳐 CTAP2 프로토콜을 통해 하드웨어 인증기에서 안전하게 서명되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **RP 서버 (Relying Party)** | 챌린지 난수 발급, WebAuthn 파라미터 구성, 공개키 서명 검증 및 세션 인가 | W3C Relying Party|
| **WebAuthn 클라이언트 API**| 브라우저에서 실행되며 Origin 도메인을 수집하고 클라이언트 데이터 무결성 보장 | W3C WebAuthn |
| **CTAP2 프로토콜** | 브라우저와 외부 보안키(또는 내부 보안칩) 간의 안전한 암호화 통신 채널 제공 | FIDO Alliance |
| **플랫폼 인증기** | 스마트폰/PC 내장 지문센서 및 Secure Enclave를 활용하는 일체형 인증기 | Windows Hello / TouchID |
| **크로스 플랫폼 인증기** | USB, NFC, BLE 인터페이스를 통해 연결되는 외장 하드웨어 보안키 | YubiKey / Titan Key |

#### 한줄 요약
- RP 서버, WebAuthn 브라우저 API, CTAP2 통신 프로토콜, 플랫폼/크로스플랫폼 인증기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **WebAuthn 인증(Assertion) 5단계 검증 프로세스**:
  1. RP가 Challenge와 `rpId` 생성
  2. 브라우저가 `navigator.credentials.get()` 호출 및 `clientDataJSON` 생성
  3. 인증기가 생체 검증(UV) 후 개인키로 `authenticatorData`와 `clientDataJSON` 해시 서명
  4. RP 서버가 서명(`signature`), `challenge`, `rpId`, 카운터(`signCount`) 검증
  5. 검증 성공 시 세션 발급

</details>

```text
1. [인증 요청] 사용자가 로그인 화면에서 ID 입력 ➔ RP 서버가 `navigator.credentials.get()` 파라미터(Challenge, rpId) 응답
            │
            ▼
2. [도메인 바인딩 검증] 브라우저가 현재 접속 주소(`Origin`)를 수집하여 `ClientDataJSON` 객체 생성
            │
            ├─ [가짜 피싱 사이트(evil-corp.com)인 경우] ➔ 브라우저 Origin 불일치로 서명 생성 실패
            ▼
3. [CTAP2 챌린지 전달] 브라우저가 인증기(스마트폰/보안키)로 `ClientDataJSON` 해시와 `rpId` 전달
            │
            ▼
4. [생체 검증 및 하드웨어 서명]
    ├─ 인증기가 사용자 지문(UV) 및 물리 터치(UP)를 감지
    └─ 내부 보안칩에 격리된 개인키(Private Key)로 `AuthenticatorData + ClientDataHash`를 디지털 서명
            │
            ▼
5. [RP 서버 서명 대조] RP 서버가 DB에 저장된 사용자의 공개키로 서명 무결성 검증 ➔ [통과 시 안전한 로그인 세션 발급]
```

**동작 원리**

1. **상호작용적 챌린지 검증**: 매 로그인마다 고유한 암호학적 난수를 발행하여 Replay 재전송 공격 봉쇄
2. **엄격한 발신지 결속**: 브라우저 엔진이 주입한 `Origin`과 RP 서버가 지정한 `rpId`가 일치할 때만 유효 서명 성립
3. **로컬 격리 인증**: 지문 데이터 등 민감 생체정보는 외부로 전송되지 않고 기기 내부 보안칩에서만 검증
4. **리플레이 복제 방어**: 인증기 내부 서명 카운터(`signCount`)를 증가시켜 이전 서명의 재사용 및 클론 복제 탐지
5. **무결성 기반 세션 인가**: 수학적으로 입증된 비대칭 서명 통과 시에만 최종 비즈니스 토큰 발행

#### 한줄 요약
- 인증 요청, 도메인 바인딩 검증, CTAP2 전달, 하드웨어 생체 서명, RP 서버 서명 대조 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **FIDO2 표준 하위 규격 비교**: W3C WebAuthn(상위 브라우저 API)과 FIDO Alliance CTAP2(하위 기기 통신 프로토콜)의 비교.

</details>

| 비교 항목 | FIDO2 (통합 표준 프레임워크) | WebAuthn (W3C 표준 API) | CTAP2 (FIDO 얼라이언스 프로토콜) |
|:---|:---|:---|:---|
| **표준화 기구** | **W3C & FIDO Alliance 공동** | **W3C (World Wide Web Consortium)**| **FIDO Alliance** |
| **동작 계층 및 위치** | **엔드투엔드 전체 인증 아키텍처** | **웹 브라우저 ➔ 웹 애플리케이션 (JS API)**| **웹 브라우저 ➔ 하드웨어 인증기 (L2/L4)**|
| **핵심 역할** | 비패스워드 및 피싱 저항성 총괄 | **도메인(Origin) 수집 및 RP 서버와 통신**| **USB/NFC/BLE를 통한 인증기 제어 및 서명**|
| **주요 기술 규격** | 공개키 비대칭 암호화, FIDO 얼라이언스| `navigator.credentials.create()/get()` | CBOR(Concise Binary Object Representation)|
| **피싱 방어 기여** | **전체 프로토콜의 피싱 저항성 보증** | **브라우저 수준의 Origin 도메인 바인딩**| **하드웨어 칩 내부 개인키 격리 및 UV/UP**|

#### 한줄 요약
- FIDO2는 통합 프레임워크, WebAuthn은 브라우저 JS API, CTAP2는 하드웨어 통신 프로토콜이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **다중 기기 동기화 패스키(Multi-Device FIDO Credentials / Synced Passkeys)**: 단일 하드웨어 칩에 갇힌 FIDO2 키의 분실 문제를 해결하기 위해, 종단간 암호화(E2EE)를 통해 클라우드 키체인(Apple iCloud Keychain, Google Password Manager)에 개인키를 안전하게 백업 및 동기화하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 구형 디바이스 및 브라우저 환경에서 WebAuthn API가 지원되지 않아 **서비스 로그인 장애 및 파편화 발생** | **W3C WebAuthn Level 2 표준 준수 및 FIDO2 미지원 환경에 대한 안전한 폴백(MFA OTP) 체계 병행** | 크로스 플랫폼 호환성 확보 및 비패스워드 사용자 경험(UX) 100% 보장 |
| XSS 취약점에 노출된 신뢰 도메인 상에서 공격자가 **악의적인 WebAuthn API 무단 호출 및 팝업 스팸 유발** | **엄격한 CSP(콘텐츠 보안 정책) 헤더 적용 및 백엔드 XSS 취약점의 선제적 완전 소거** | 신뢰 출처(Origin) 상에서의 비인가 FIDO 서명 요청(Prompt Injection) 원천 차단 |
| 단일 하드웨어에 종속된 FIDO 키 분실 시 **사용자 계정 접근이 영구 잠금(Account Lockout)되는 장애** | **동기화 패스키(Synced Passkey) 도입 및 2대 이상의 백업 인증기 사전 등록 절차 강제** | 기기 분실로 인한 서비스 중단 방지 및 안전한 계정 라이프사이클 복원력 확보 |

#### 한줄 요약
- 웹 표준 준수로 호환성을 확보하고, CSP로 XSS 연계를 막으며, 동기화 패스키로 분실 잠금을 방지한다.

## Ⅶ. 결론

- 공유 비밀 기반 인증의 구조적 한계를 극복하는 **FIDO2 및 WebAuthn 아키텍처**는 차세대 제로 트러스트 신원 보안의 글로벌 표준이며, 실무 구현 시 **W3C WebAuthn 표준 기반 RP 백엔드 구축**, **브라우저 레벨의 RP ID 도메인 바인딩 강제**, **CTAP2 기반 하드웨어 보안 모듈(Secure Enclave/TPM) 연계**, **멀티 디바이스 패스키(Passkey) 생태계 확장**을 결합하여 완벽한 피싱 저항성과 최상의 사용자 편의성을 완성

#### 한줄 요약
- WebAuthn과 CTAP2를 결합한 FIDO2 표준을 통해 피싱 저항성 비패스워드 인증 생태계를 완성한다.
