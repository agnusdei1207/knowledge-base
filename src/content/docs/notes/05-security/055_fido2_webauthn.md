---
sidebar:
  order: 55
  label: "055. FIDO2•WebAuthn (FIDO2 WebAuthn)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "FIDO2•WebAuthn (FIDO2 WebAuthn)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-security"
weight: 55
extra:
  question_no: "055"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 최신 기출이며 피싱저항 인증의 핵심 표준임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **온라인 신속 신원확인 2(Fast Identity Online 2, FIDO2)**: 비밀번호 없이 비패스워드(Passwordless) 및 피싱 저항성 공개키 기반 인증을 제공하는 W3C 및 FIDO 얼라이언스 국제 표준.
- **웹 인증(Web Authentication, WebAuthn)**: 브라우저 JavaScript API 수준에서 RP 서버와 인증자(Authenticator) 간 자격증명 생성 및 검증을 표준화한 W3C 명세.
- **클라이언트-인증자 프로토콜 2(Client to Authenticator Protocol 2, CTAP2)**: USB, BLE, NFC 또는 디바이스 내부 보안 영역(TPM/Secure Enclave)과 플랫폼 브라우저 간 통신 규격.
- **신뢰 당사자(Relying Party, RP)**: FIDO2 공개키 자격증명을 검증하여 사용자에게 서비스 접근 인가를 제공하는 웹/앱 백엔드 서버.

</details>

- 정의/개념: 공유 비밀(비밀번호)을 서버에 전송하지 않고, 사용자 디바이스의 보안 인증자에서 생성된 공개키-개인키 쌍과 도메인 바인딩 서명을 통해 피싱 저항성 인증을 집행하는 W3C 표준 규격.
- 배경/필요성: 비밀번호 유출, 중간자(MitM) 역프록시 피싱 사이트 공격 극복 및 Passwordless 패스키(Passkey) 환경 구현.

#### 한줄 요약

- 개인키를 디바이스 보안 영역에 격리 보관하고, 서비스 도메인(RP ID)에 결속된 서명 검증으로 피싱 공격을 무력화함.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **RP ID**: 자격 증명을 특정 FQDN 도메인(예: example.com)에 엄격히 결속시키는 식별자.
- **Origin**: 브라우저가 인식하는 요청 발신자의 Scheme, Host, Port 조합.
- **도전값(Challenge)**: Replay 공격 방지를 위해 RP 서버가 발급하는 일회성 난수.
- **사용자 검증(User Verification, UV)**: 생체인식(Touch ID/Face ID) 또는 PIN 입력을 통해 실제 사용자가 본인임을 인증하는 절차.
- **사용자 존재(User Presence, UP)**: 버튼 터치 등 물리적 행위로 사용자의 승인 의사가 존재함을 입증하는 특성.

</details>

- 개인키를 클라이언트 하드웨어 칩셋(TPM/Secure Enclave)에 안전 격리하고 **RP 서버**에는 공개키만 등록.
- 브라우저가 검증한 **Origin**과 **RP ID**가 다를 경우 서명을 전송하지 않는 구조적 피싱 방어.
- **도전값(Challenge)** 무결성 대조 및 **사용자 검증(UV)**, **사용자 존재(UP)**에 의한 물리적 타당성 확보.

#### 한줄 요약

- 공개키 기반 무상태 서명, RP ID 도메인 바인딩 피싱 방어 및 UV/UP 검증으로 높은 보증 레벨(AAL3)을 제공함.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **RP 서버(Relying Party Server)**: Challenge 난수를 발급하고, 자격증명 등록 시 전달받은 공개키로 Challenge 서명을 검증하는 백엔드.
- **인증자(Authenticator)**: 플랫폼 보안 칩(Platform) 또는 외부 보안키(Cross-Platform)로 개인키 생성 및 서명을 집행하는 하드웨어/소프트웨어.

</details>

```text
FIDO2 인증 구조
├─ RP 서버: 도전값 발급•서명 검증
├─ WebAuthn 클라이언트: 원본 확인•중계
├─ 인증자: 개인키 보관•서명
├─ 자격 증명 저장소: 공개키•식별자 관리
└─ 등록•복구 정책: 인증자 수명 통제
```

| 구성요소 | 책임 |
|:---|:---|
| RP 서버 | 일회성 Challenge 발급, 자격증명 DB 관리 및 서명 검증 |
| WebAuthn 클라이언트 | 브라우저 런타임 상에서 **Origin** 대조 및 CTAP2 API 호출 중계 |
| 인증자 | **인증자(Authenticator)** 내부 개인키 생성, **UV/UP** 검증 및 서명 집행 |
| 자격 증명 저장소 | Credential ID와 맵핑된 **RP** 공개키 및 카운터 관리 |
| 등록•복구 정책 | 복수 인증자 패스키 등록 및 기기 분실 시 비상 복구 수명주기 관리 |

#### 한줄 요약

- RP 서버, WebAuthn 브라우저 API, CTAP2 연동 인증자 및 공개키 DB 구조로 이뤄짐.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **자격 증명 ID(Credential ID)**: RP 서버가 사용자 계정과 맵핑된 등록 공개키를 검색하기 위한 고유 식별값.
- **도전값•RP 정책 생성**: RP 서버가 난수 Challenge와 UV/UP 요구조건을 묶어 전달하는 단계.
- **원본•RP ID 검증**: 브라우저가 현재 도메인과 RP ID의 일치성을 판정하는 단계.
- **사용자 존재•검증 확인**: 지문/얼굴 또는 PIN/버튼 터치를 집행하는 단계.
- **RP별 개인키 서명**: 해당 RP ID전용 개인키로 Challenge + ClientDataJSON에 서명하는 단계.
- **도전값•원본•서명 검증**: RP 서버가 등록된 공개키로 최종 서명 및 카운터를 체크하는 단계.

</details>

```text
1. 도전값•RP 정책 생성
          │
          ▼
WebAuthn 인증 요청
          │
          ▼
2. 원본•RP ID 검증
          │
          ▼
3. 사용자 존재•검증 확인
          │
          ▼
4. RP별 개인키 서명
          │
          ▼
5. 도전값•원본•서명 검증
          │
          ├─ 불일치 ── 인증 거부
          │
          └─ 일치 ── 인증 성공
```

### 동작 원리

1. **도전값•RP 정책 생성**: RP 서버가 Challenge 난수 및 자격증명 조건 생성.
2. **원본•RP ID 검증**: 브라우저 파서가 접속 **Origin**과 **RP ID**의 일치 판정.
3. **사용자 존재•검증 확인**: 인증자가 생체인식(UV) 및 버튼 누름(UP) 확인.
4. **RP별 개인키 서명**: 보안 영역 내부 **개인키**로 Challenge 및 ClientData 서명.
5. **도전값•원본•서명 검증**: RP 서버가 **공개키**로 서명 및 세션 발급.

#### 한줄 요약

- Challenge 생성, Origin/RP ID 검증, UV/UP 생체 확인, 개인키 서명 및 공개키 서명 검증을 집행함.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **FIDO2 구성 역할 분리(FIDO2 Sub-specs)**: 애플리케이션-브라우저 간 WebAuthn 명세와, 브라우저-하드웨어 인증자 간 CTAP2 명세의 표준 분담 구조.

</details>

| 구성 요소 | 역할 | 연계 지점 |
|:---|:---|:---|
| **FIDO2** | 패스워드리스 공개키 인증 상위 기술 프레임워크 | WebAuthn과 CTAP2 규격을 결합 통합 |
| **WebAuthn** | W3C 브라우저/애플리케이션 JS API 규격 | 서비스 **Origin** 디코딩 및 RP 서버 연동 |
| **CTAP2** | FIDO 얼라이언스 클라이언트-인증자 통신 규격 | USB, BLE, NFC, YubiKey, 보안 칩셋 통신 |

#### 한줄 요약

- FIDO2 프레임워크 기반 하에서 브라우저 인터페이스 WebAuthn과 디바이스 통신 CTAP2가 역할을 분담함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **W3C WebAuthn Level 2/3**: 최신 브라우저 및 패스키(Passkey) 동기화를 지원하는 W3C 웹 인증 레벨 스펙.
- **FIDO CTAP 2.1/2.2**: Enterprise Attestation 및 바이오인증 보안성이 강화된 인증자 인터페이스 규격.
- **교차 사이트 스크립팅(XSS)**: XSS 발생 시 WebAuthn 호출을 무단 유발할 수 있으므로 선제적인 XSS 방어가 필수적.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| WebAuthn 구현 파편화 | **W3C WebAuthn Level 2** 표준 스펙 준수 | 호환성 및 패스키 연동성 확보 |
| 하드웨어 인증자 통신 오작동 | **FIDO CTAP 2.2** 적용 | 외부 YubiKey 및 스마트폰 인증자 호환성 보장 |
| 세션 XSS 공격으로 호출 조작 | **XSS** 제거 및 **CSP** 헤더 적용 | 신뢰 출처(Origin) 상에서의 무단 호출 유발 방지 |
| 인증자 분실 시 서비스 접근 불가 | 복수 인증자 사전 등록 및 강한 계정 복구(Recovery) 수립 | 계정 잠금 방지 및 복구 경로 우회 차단 |

#### 한줄 요약

- W3C WebAuthn Level 2 및 FIDO CTAP 2.2 표준을 준수하고, 복수 패스키 등록과 강한 계정 복구 경로를 마련함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **인증자 수명 관리(Authenticator Lifecycle Management)**: 패스키 등록, 기기 추가, 분실 폐기 및 비상 복구를 메인 FIDO2 인증과 동등 수준의 신원확인으로 통제하는 정책.

</details>

- 피싱 저항이 필요한 제로 트러스트 환경에 **FIDO2/WebAuthn**을 적용하고, **인증자 수명 관리**를 통해 복구 경로의 피싱 취약점을 제거.

#### 한줄 요약

- FIDO2/WebAuthn 기반 피싱 저항성 공개키 인증 및 RP ID 결속•인증자 수명 관리 체계 수립 필수.

