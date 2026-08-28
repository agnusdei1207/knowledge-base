---
sidebar:
  order: 58
  label: "058. SAML 2.0 (SAML 2.0)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "이종 도메인 XML 연합 인증 및 싱글 사인온 : SAML 2.0 (Security Assertion Markup Language & OASIS)"
date: "2026-08-26T14:46:22+09:00"
tags:
  - "notes-security"
weight: 58
extra:
  question_no: "058"
  source_status: "기출"
  source_history: "123회"
  priority: 30
  priority_note: "123회 기출, OASIS SAML 2.0 표준, IdP vs SP, XML Signature/Encryption, SP-Initiated vs IdP-Initiated SSO, XML 서명 래핑(XSW) 및 Replay 방어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SAML 2.0(Security Assertion Markup Language 2.0 / OASIS)**: 엔터프라이즈 환경에서 서로 다른 도메인(이종 플랫폼) 간에 사용자 인증(Authentication) 및 권한(Authorization) 데이터를 XML 기반의 보안 주장(**Assertion**) 문서로 안전하게 교환하여 웹 기반 싱글 사인온(SSO)을 구현하는 연합 신원(Federated Identity) 표준 프로토콜.
- **XML 서명 래핑 공격(XSW: XML Signature Wrapping)**: SAML 응답 문서 내에서 디지털 서명이 적용된 정당한 XML 노드를 복사/이동시키고, 실제 비즈니스 로직이 파싱하는 위치에 공격자가 조작한 가짜 XML 노드를 주입하여, 서명 검증은 정상 통과시키면서 관리자 권한을 획득하는 구조적 파싱 취약점.

</details>

- 정의/개념: 신원 제공자(**IdP: Identity Provider**)와 서비스 제공자(**SP: Service Provider**) 간의 사전 신뢰(Metadata/공개키)를 기반으로, **인증 요청(AuthnRequest) $\rightarrow$ 사용자 인증 $\rightarrow$ XML 서명된 Assertion 발행 $\rightarrow$ SP 검증 및 로컬 세션 수립** 을 집행하는 **엔터프라이즈 연합 SSO 아키텍처**
- 배경/필요성: 도메인마다 계정을 따로 두면 입·퇴사와 권한 변경 비용이 시스템 수만큼 되풀이되고 어느 한 곳의 회수 누락이 그대로 잔존 계정으로 남으므로, 인증을 IdP 한 곳으로 모으고 각 SP는 서명된 **Assertion**만 검증해 로컬 세션을 여는 신뢰 위임 계층으로 옮길 필요

#### 한줄 요약
- IdP와 SP 간 사전 신뢰를 바탕으로 XML 기반 서명 Assertion을 교환하여 이종 도메인 SSO를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SAML Assertion(보안 주장)**: IdP가 발행하는 XML 문서로, 사용자 식별자(`NameID`), 인증 시점 및 방법(`AuthnStatement`), 사용자 속성 정보(`AttributeStatement: 부서, 직급`)를 포함하며 W3C XML Signature로 서명됨.
- **SP-Initiated SSO vs IdP-Initiated SSO**:
  - **SP-Initiated**: 사용자가 SP에 먼저 접근하여 SP가 고유 `ID`가 포함된 `AuthnRequest`를 생성하고 IdP로 리다이렉트하는 방식 (Replay 방어 우수, 권장).
  - **IdP-Initiated**: 사내 포털(IdP) 대시보드에서 앱 아이콘을 클릭하여 IdP가 즉시 Assertion을 SP로 푸시하는 방식 (간결하나 Replay 위험 내포).

</details>

- **공개키 인프라(PKI) 기반 상호 신뢰**: IdP와 SP가 X.509 인증서가 포함된 메타데이터(Metadata XML)를 사전에 교환하여 신뢰 형성
- **W3C XML Signature & Encryption 결합**: Assertion 전체 또는 내부 속성을 암호화(기밀성)하고 디지털 서명(무결성/부인방지)
- **엄격한 수신자 및 재전송 방지 통제**: `Recipient`, `AudienceRestriction`, `InResponseTo`, `NotOnOrAfter` 유효성 전수 검증

#### 한줄 요약
- SP가 자격증명을 갖지 않는 대가로 IdP가 전사의 단일 신뢰점이자 단일 장애점이 되며, 그래서 프로토콜의 무게 중심이 서명 자체보다 수신자·유효시간 검증 쪽으로 기운다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SAML 3대 핵심 참여자**:
  1. **User Agent (웹 브라우저)**: HTTP Redirect 및 POST Binding을 통해 요청과 Assertion을 중계 전달하는 클라이언트.
  2. **Identity Provider (IdP / 신원 제공자)**: 사용자의 신원을 인증하고 XML Assertion을 발급하는 중앙 인증 서버.
  3. **Service Provider (SP / 서비스 제공자)**: IdP의 Assertion 서명을 검증하고 비즈니스 애플리케이션 서비스를 제공하는 서버.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. Identity Provider (IdP: 본사 엔터프라이즈 신원 서버) ]             │
│  ├─ 메타데이터 관리: SP의 X.509 인증서 및 Assertion Consumer Service URL │
│  ├─ 사용자 인증: LDAP / Active Directory / MFA 연계 인증 집행            │
│  └─ [ SAML Assertion 생성 ➔ 개인키(Private Key)로 XML 디지털 서명 ]     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (SAML Response 전송 / Browser POST Binding)
                                     ▼
[ User Agent (웹 브라우저: HTTP POST 데이터 중계) ]
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. Service Provider (SP: 타깃 클라우드/자회사 웹 애플리케이션) ]      │
│  ├─ XML 서명 무결성 검증: IdP의 공개키로 XML Signature 검증            │
│  ├─ 수신자 검증: `Recipient == SP_ACS_URL`, `Audience == SP_Entity_ID` │
│  ├─ 유효 시간 검증: `NotBefore <= Current_Time < NotOnOrAfter`          │
│  ├─ 재전송 검증: `InResponseTo == AuthnRequest_ID` 및 Assertion ID 캐싱 │
│  └─ [ 전 항목 통과 ➔ SP 로컬 로그인 세션(Cookie) 생성 및 인가 ]        │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: IdP가 인증 후 XML 서명된 Assertion을 발행하면 브라우저를 거쳐 SP에 전달되고, SP가 엄격한 서명 및 유효성 검증을 거쳐 로컬 세션을 발급하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **User Agent (브라우저)** | IdP와 SP 간의 통신에서 SAML 메시지(XML)를 HTTP Redirect/POST로 중계 | Client Agent |
| **IdP (신원 제공자)** | 사용자 신원 인증, 권한 속성 매핑, X.509 서명된 SAML Assertion 발급 | Identity Authority|
| **SP (서비스 제공자)** | AuthnRequest 생성, 수신된 Assertion 서명/수신자/유효기간 검증 및 로컬 세션 확립 | Service Endpoint |
| **SAML Metadata** | IdP와 SP가 엔티티 ID, 엔드포인트 URL, 공개키 인증서를 상호 교환하기 위한 XML 명세 | Federation Trust |
| **ACS (Assertion Consumer)**| SP 측에서 IdP로부터 전달된 SAML Response(HTTP POST)를 수신하는 전용 엔드포인트 | ACS URL |

#### 한줄 요약
- IdP와 SP는 직접 통신하지 않고 브라우저가 XML을 중계하므로 신뢰는 사전 교환한 메타데이터의 공개키 하나에 걸리고, 그만큼 검증 책임은 전적으로 SP 쪽에 남는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SP-Initiated SAML 2.0 5단계 흐름**:
  1. 사용자가 SP 접근 $\rightarrow$ SP가 `AuthnRequest` 생성 후 IdP로 리다이렉트
  2. 사용자가 IdP에서 인증(SSO)
  3. IdP가 서명된 SAML Response(Assertion 포함) 생성
  4. 브라우저가 SP의 ACS URL로 SAML Response를 HTTP POST 전송
  5. SP가 서명 및 클레임 검증 후 로컬 세션 수립

</details>

```text
1. [SP 접근 및 요청 생성] 사용자가 SP에 접속 ➔ SP가 고유 ID(`AuthnRequest_ID=req-1234`)를 담은 SAML AuthnRequest 생성
            │
            ▼
2. [IdP 리다이렉트 및 인증] 브라우저가 IdP로 리다이렉트 ➔ 사용자가 IdP 로그인(MFA) 수행 완료
            │
            ▼
3. [Assertion XML 서명 발행] IdP가 `InResponseTo="req-1234"`와 `NotOnOrAfter`를 포함한 SAML Assertion에 XML 디지털 서명
            │
            ▼
4. [SP ACS 전송] 브라우저가 IdP로부터 받은 SAML Response를 SP의 ACS 엔드포인트로 HTTP POST 전송
            │
            ▼
5. [SP 다계층 유효성 검증]
    ├─ XML Signature 서명 무결성 검증 (IdP 공개키 대조)
    ├─ 요청 ID 일치성 대조 (`InResponseTo == req-1234`)
    ├─ 수신자(`Recipient`) 및 대상(`AudienceRestriction`) 일치 검증
    └─ 유효기간(`NotOnOrAfter`) 및 Assertion ID 중복(Replay) 검사
            │
            ▼
6. [로컬 세션 발급] 검증 성공 ➔ 사용자 NameID로 매핑된 SP 로컬 애플리케이션 세션 쿠키 발급 완료
```

**동작 원리**

1. **상호 인증서 기반 무결성**: IdP의 개인키로 생성된 전자서명을 SP가 등록된 IdP 공개키로 수학적 검증
2. **트랜잭션 1:1 결속**: SP가 발행한 `AuthnRequest` ID와 IdP 응답의 `InResponseTo` 속성을 바인딩하여 위조 방어
3. **엄격한 수신자 제한**: 타 SP를 대상으로 발행된 Assertion이 다른 SP에서 재사용되는 토큰 혼용 공격 차단
4. **시간 기반 공격 윈도우 축소**: 유효 시간을 수 분 이내로 제한하여 네트워크 스니핑 후 재전송 공격 무력화
5. **무상태 엔터프라이즈 연합**: SP가 사용자의 패스워드를 전혀 알 필요 없이 IdP의 서명된 속성만으로 인가 완료

#### 한줄 요약
- 서명 검증만으로는 그 Assertion이 누구에게·언제·어느 요청에 대한 응답인지가 남지 않으므로, SAML의 안전성은 서명 강도가 아니라 수신자·유효시간·요청 ID 대조를 빠짐없이 수행하는지에서 갈린다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SAML 2.0 vs OIDC(OpenID Connect) 핵심 비교**: 엔터프라이즈 XML 연합과 모바일/클라우드 JSON 연합의 비교.

</details>

| 비교 항목 | SAML 2.0 (Security Assertion Markup Language) | OpenID Connect (OIDC) |
|:---|:---|:---|
| **데이터 교환 포맷** | **XML (Extensible Markup Language)** | **JSON / JWT (JSON Web Token)** |
| **디지털 서명 표준** | **W3C XML Signature (XML-DSig)** | **JSON Web Signature (JWS / RS256)** |
| **주요 적용 생태계** | **엔터프라이즈 B2B, 레거시 사내망, 온프레미스 SSO**| **모바일 앱, 클라우드 네이티브, SPA, B2C** |
| **메시지 페이로드 크기** | 무거움 (수 KB 이상 XML 파싱 오버헤드) | **가벼움 (수백 바이트 내외 초경량)** |
| **모바일/API 친화성** | 낮음 (브라우저 리다이렉트에 강하게 의존) | **매우 높음 (RESTful API 및 SDK 연동 용이)**|

#### 한줄 요약
- 둘은 같은 연합 신원 문제를 XML 서명과 JWT라는 다른 표현으로 푼 해법이며, SAML이 치르는 XML 파싱 비용이 곧 XSW 같은 파서 취약점의 원천이라 모바일·클라우드에서는 OIDC로 대체된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SAML Replay Attack**: 공격자가 네트워크 도청이나 브라우저 히스토리에서 유효한 SAML Response를 가로채어 SP로 재전송함으로써 타인의 권한으로 로그인하는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SP의 XML 파서가 서명된 노드와 비즈니스 데이터 노드를 분리 파싱하여 **XML 서명 래핑(XSW) 권한 상승 사고 발생** | **W3C XML Signature 1.1** 지침 준수, XML 스키마 엄격 검증 및 **서명 대상 노드(Assertion ID)의 DOM 위치 강제 대조** | XSW 래핑 공격을 통한 관리자 권한 위조 및 서명 검증 우회 100% 원천 차단 |
| 정상적인 SAML Response를 공격자가 가로채어 **타깃 SP에 재전송함으로써 세션을 무단 탈취하는 Replay 공격** | **Assertion ID를 메모리/Redis에 캐싱하여 중복 사용을 거부하고, `NotOnOrAfter` 유효시간을 3~5분으로 엄격 단축** | 이전에 발급된 정상 Assertion을 재사용한 세션 하이재킹 공격 100% 무력화 |
| 타 SP 전용으로 발급된 SAML Assertion이 **수신자 검증 누락으로 인해 다른 자회사 SP에 정상 로그인되는 결함** | **SP의 ACS 수신 시 `Recipient` 및 `AudienceRestriction` 클레임이 자사 식별자와 일치하는지 전수 검증** | 가로채기 후 타 서비스로의 자격증명 오남용 및 도메인 간 혼용 침해 완벽 방어 |

#### 한줄 요약
- DOM 위치 검증으로 XSW 래핑을 막고, ID 캐싱으로 Replay를 차단하며, Recipient 대조로 혼용을 방지한다.

## Ⅶ. 결론

- 레거시 웹 연합은 **SAML 2.0**을 유지하고 XSW·재전송 검증을 강화

#### 한줄 요약
- PKI 메타데이터 신뢰와 XML 디지털 서명 및 다계층 유효성 검증을 통해 안전한 SAML 2.0 연합 SSO를 완성한다.
