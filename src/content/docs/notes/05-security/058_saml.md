---
sidebar:
  order: 58
  label: "058. SAML 2.0 (SAML 2.0)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "SAML 2.0 (SAML 2.0)"
date: "2026-08-13T19:56:00+09:00"
tags:
  - "notes-security"
weight: 58
extra:
  question_no: "058"
  source_status: "기출"
  source_history: "123회"
  priority: 30
  priority_note: "123회 기출이나 신규 시스템보다 연합 비교에 유용함"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **보안 주장 마크업 언어(Security Assertion Markup Language, SAML) 2.0**: 이종 도메인 간 사용자 인증(Authentication) 및 인가(Authorization) 데이터를 XML 기반 보안 주장(Assertion)으로 교환하는 연합 인증 표준.
- **확장 가능 마크업 언어(Extensible Markup Language, XML)**: 서명 및 암호화 구조체를 표현하기 위해 SAML 데이터 교환 시 사용되는 마크업 포맷.
- **통합 인증(Single Sign-On, SSO)**: 단 일회 사용자 인증으로 연계된 이종 서비스 체계(SP)에 추가 로그인 없이 통합 접근하는 기능.

</details>

- 정의/개념: XML 주장으로 신원을 연합하는 **SAML 2.0**
- 배경/필요성: 개별 비밀번호 공유는 **조직 간 자격증명 노출** 유발

#### 한줄 요약

- **XML 서명 Assertion**으로 이종 도메인 SSO 연계

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Assertion**: 사용자 식별자(NameID), 인증 방법(AuthnStatement), 속성(AttributeStatement) 및 유효조건(Conditions)이 담긴 서명 문서.
- **Metadata**: IdP와 SP 간 사전 교환하여 신뢰관계를 형성하는 공개키 인증서, Entity ID 및 수신 엔드포인트 URL 정보 파일.
- **신원 제공자(Identity Provider, IdP)**: 사용자를 1차 인증하고 SAML Assertion을 생성하여 전자서명 발급하는 인증 서버.
- **서비스 제공자(Service Provider, SP)**: IdP가 발급한 SAML Assertion 서명 및 수신자 조건을 검증하여 자원 접근을 허용하는 서비스 애플리케이션.
- **식별자(ID / InResponseTo)**: AuthnRequest와 Response 간의 1:1 바인딩 대조를 수행하여 세션 주입을 막는 키.
- **Recipient**: SAML Assertion 응답이 도착해야 할 대상 SP의 정확한 Assertion Consumer Service(ACS) URL.
- **재전송 공격(Replay Attack)**: 이미 사용된 정상 SAML Response를 다시 전송하여 무단 승인을 노리는 공격.

</details>

- **IdP(Identity Provider)**와 **SP(Service Provider)** 간 **Metadata** 사전 교환을 통한 상호 신뢰 형성.
- XML 서명(XML Signature) 및 XML 암호화(XML Encryption) 기술을 적용한 **Assertion** 무결성 보장.
- **InResponseTo(요청 ID)**, **Recipient** 수신 주소 및 유효 시간(NotOnOrAfter) 검증을 통한 **재전송 공격** 차단.

#### 한줄 요약

- XML 서명 기반 Assertion 무결성 확보 및 Recipient/InResponseTo 대조를 통해 연합 SSO 재전송을 막음.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **로컬 세션(Local Session)**: SP가 IdP의 SAML Assertion 검증을 수락한 후 자체 쿠키/세션을 발급하는 단계.

</details>

```text
SAML 연합 인증 구조
├─ 사용자 브라우저: 요청•응답 중계
├─ SP: 주장 검증•로컬 세션 생성
├─ IdP: 사용자 인증•응답 서명
├─ SAML Assertion: 신원•속성•조건 전달
└─ 메타데이터•검증 체계: 신뢰•재전송 관리
```

| 구성요소 | 책임 |
|:---|:---|
| 사용자 브라우저 | HTTP Redirect/POST 바인딩을 통해 SAML AuthnRequest 및 Response를 중계 |
| SP | **SP**가 제출된 SAML Assertion 서명, Recipient, Time validity 검증 및 **로컬 세션** 생성 |
| IdP | **IdP**가 자원 소유자를 인증하고 계정 속성을 **Assertion**에 수록 후 공개키 서명 집행 |
| SAML Assertion | NameID, AuthnStatement, Conditions를 포함하는 무결성 보장 XML 주장체 |
| 메타데이터•검증 체계 | EntityID, X.509 Certificate 공개키 교환을 통한 **Metadata** 기반 서명 검증 |

#### 한줄 요약

- 사용자 브라우저 중계, IdP 서명 발급, SP 무결성/조건 검증 및 Metadata 신뢰 체계로 구성됨.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인증 요청(Authentication Request, AuthnRequest)**: SP가 IdP로 사용자 인증을 위탁하기 위해 발송하는 SAML 요청 문서.
- **응답 ID(Response ID)**: Replay 공격을 막기 위해 SP가 수신 테이블에 등록 체크하는 고유 난수 값.
- **SAML AuthnRequest 생성**: SP가 요청 ID와 ACS URL을 담아 AuthnRequest를 생성하는 단계.
- **사용자 신원 인증**: IdP가 사용자 자격증명을 1차 확인하는 단계.
- **Assertion 조건•서명 생성**: IdP가 NameID 및 조건문을 수록하고 디지털 서명을 부여하는 단계.
- **서명•대상•요청 결속 검증**: SP가 IdP 공개키로 서명, Recipient 및 InResponseTo를 확인하는 단계.
- **재전송 차단•로컬 세션 생성**: 중복 Response ID를 차단하고 최종 세션을 생성하는 단계.

</details>

```text
서비스 접근
    │
    ▼
1. SAML AuthnRequest 생성
    │
    ▼
2. 사용자 신원 인증
    │
    ▼
3. Assertion 조건•서명 생성
    │
    ▼
4. 서명•대상•요청 결속 검증
    │
    ▼
5. 재전송 차단•로컬 세션 생성
    │
    ├─ 응답 ID 중복 ── 로그인 거부
    │
    └─ 신규 응답 ID ── 로컬 세션 발급
```

### 동작 원리

1. **SAML AuthnRequest 생성**: SP에서 요청 ID 및 ACS URL을 결합한 **AuthnRequest** 생성.
2. **사용자 신원 인증**: IdP 로그인 페이지로 리다이렉트되어 사용자 신원 인증 집행.
3. **Assertion 조건•서명 생성**: IdP가 **Assertion** 문서에 XML 디지털 서명 집행.
4. **서명•대상•요청 결속 검증**: SP가 **Metadata** 공개키로 서명, Recipient 및 InResponseTo 1:1 검증.
5. **재전송 차단•로컬 세션 생성**: **응답 ID** 중복 여부 확인 후 승인 시 SP 로컬 세션 생성.

#### 한줄 요약

- AuthnRequest 생성, IdP 사용자 인증, Assertion XML 서명, SP 서명/Recipient 검증 및 재전송 차단을 구동함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SP 시작(SP-Initiated SSO)**: 사용자가 SP 웹사이트 접속 시 SSO 절차가 시작되어 SP가 AuthnRequest를 먼저 발행하는 표준적인 흐름.
- **IdP 시작(IdP-Initiated SSO)**: 사용자가 중앙 IdP 포털에서 애플리케이션 아이콘을 클릭하여 AuthnRequest 없이 IdP가 곧바로 SAML Response를 SP에 전송하는 흐름.

</details>

| SAML 인증 시작 방식 | SP 시작 (SP-Initiated) | IdP 시작 (IdP-Initiated) |
|:---|:---|:---|
| 적용 기준 | 이종 웹 애플리케이션 직접 접속 시 | 기업 내부 중앙 포털(Dashboard) 기반 접속 시 |
| 핵심 특징 | **SP 시작**의 AuthnRequest 요청-응답 1:1 바인딩 대조 | **IdP 시작**의 Unsolicited Response 발송 및 인가 처리 |
| 한계/주의점 | 추가 리다이렉션 홉 발생 | InResponseTo 검증 불가로 **재전송 공격** 위험 제어 필요 |

#### 한줄 요약

- 1:1 대조가 명확한 SP-Initiated SSO와, 중앙 포털 중심의 IdP-Initiated SSO 방식으로 구별함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OASIS SAML 2.0 Core**: SAML 2.0 스펙의 세부 텍스트, 프로토콜 및 구문 규칙을 명시한 국제 표준.
- **XML 서명 래핑 공격(XML Signature Wrapping Attack, XSW)**: XML 구조 상에 무효한 위조 노드를 주입하여 서명 검증 엔진과 비즈니스 파싱 엔진 간의 불일치를 악용하는 연합 인증 공격.
- **W3C XML Signature 1.1**: XML 문서 내 구체적 DOM 태그 요소의 서명 처리 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 타 사이트용 Assertion 재사용 | **OASIS SAML 2.0 Core** 준수 및 Recipient, Audience 검증 | 비인가 SP로의 주장 전송 완전 차단 |
| XML 서명 래핑 공격(XSW) | **W3C XML Signature 1.1** 기반 하드닝 및 서명 DOM 위치 검증 | 위조 XML 노드 주입에 의한 권한 우회 무력화 |
| Response 재전송을 통한 세션 탈취 | **응답 ID** 캐싱 대조 및 NotOnOrAfter 단기 타임아웃 적용 | Replay 공격에 의한 무단 세션 생성 방지 |

#### 한줄 요약

- OASIS SAML 2.0 Core 스펙을 준수하고, XML 서명 래핑(XSW) 검증 강화 및 Response ID 캐싱을 집행함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **요청 결속(Request-Response Binding Verification)**: InResponseTo, Recipient, NotOnOrAfter 파라미터를 1:1로 결합 대조하여 위조된 응답 주입을 방지하는 검증 지침.

</details>

- **요청 결속** 원칙에 따라 보안성이 높은 **SP 시작 SSO**를 우선 채택하고, XML 서명 무결성 검증 및 재전송 차단을 병행.

#### 한줄 요약

- **SP 시작 SSO**를 우선하고 서명•요청 결속 검증
