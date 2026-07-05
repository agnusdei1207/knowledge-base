---
title: "웹 서비스 보안 - SAML·WS-Security (Web Service Security)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 90
---

# 📖 【암기용】 개념 완전 이해

> 목적: 웹 서비스 보안 - SAML·WS-Security를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: XML 기반 웹 서비스에서 인증 assertion, 메시지 서명, 암호화, 재전송 방지를 수행하는 보안 체계
- **왜 필요한가**: SOAP 메시지는 여러 중계 노드를 거칠 수 있다. TLS만으로는 중계 이후 메시지 일부의 서명·무결성·사용자 신원을 보장하기 어렵다.
- **핵심 직관**: WS-Security는 봉투(SOAP)에 신분증(SAML), 서명(XML Signature), 봉인(XML Encryption), 발송 시각(Timestamp)을 붙이는 방식임

## 깊이 이해
- **배경·문제의식**: 금융·공공·기업 연계 시스템은 SOAP, SAML, XML Signature를 여전히 사용한다. 메시지가 ESB, API Gateway, 파트너 시스템을 지나며 저장·재전송될 수 있어 메시지 수준 보안이 필요하다.
- **작동 원리**: Identity Provider가 SAML Assertion을 발급하고, SOAP Header에 WS-Security 토큰을 넣는다. 송신자는 XML Signature로 Body와 Assertion을 서명하고 필요 시 XML Encryption으로 민감 필드를 암호화한다. 수신자는 인증서, 서명 참조, timestamp, nonce를 검증한다.
- **비유**: 공문 봉투에 발급기관 도장, 문서 위변조 방지 서명, 비밀 문단 봉인, 발송 시각을 함께 붙여 여러 부서를 지나도 검증 가능하게 하는 절차와 같다.
- **구체 예시**: `Assertion`의 `NotBefore/NotOnOrAfter`를 5분 clock skew 안에서 확인하고, `wsu:Id`가 서명 참조와 일치하지 않으면 signature wrapping 공격으로 간주해 거부한다.
- **흔한 오해·주의점**: TLS는 전송 구간 보호이고 WS-Security는 메시지 단위 보호다. XML Signature 검증은 서명이 맞는지뿐 아니라 "서명된 바로 그 요소를 업무 처리했는지"까지 확인해야 한다.

## 연결 개념
- SAML 2.0 - Assertion 기반 SSO와 연계 인증
- XML Signature Wrapping - 서명 검증과 업무 처리 대상 불일치 공격
- SOAP/ESB - 메시지 중계가 많은 기업 연계 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SAML·WS-Security를 표준명 나열로 쓰지 않고 XML 메시지의 신뢰 경계, 서명 대상, 재전송 방지, signature wrapping 방어로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 웹 서비스 보안은 SOAP/XML 메시지에 SAML Assertion, XML Signature, XML Encryption, Timestamp/Nonce를 포함해 메시지 수준 인증·무결성·기밀성을 보장하는 체계임
> 2. **가치**: TLS 종료 이후에도 중계·저장·재전송되는 메시지의 발신자, 서명 대상, 유효시간, 변조 여부를 수신자가 검증함
> 3. **판단 포인트**: assertion 조건, clock skew, replay cache, canonicalization, signature wrapping 방어, 인증서 폐기 검증을 함께 써야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메시지 수준 보안 이해 확인 | SAML Assertion, WS-Security Header, XML Signature/Encryption | TLS와 WS-Security를 같은 계층으로 설명 |
| XML 서명 검증 위험 판단 | signed element 처리, canonicalization, wrapping 방어 | 서명 검증 성공만 쓰고 참조 대상 확인 누락 |
| 재전송·시간 검증 설계 | Timestamp, Nonce, replay cache, clock skew | assertion 만료·중복 요청 방지 누락 |

> 요약: 이 문제는 SOAP 메시지의 신원·무결성·기밀성·재전송 방지를 XML 표준으로 어떻게 검증하는지 묻는다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | XML 기반 웹 서비스에서 인증 assertion, 메시지 서명, 암호화, 재전송 방지를 수행하는 보안 체계 | "경험으로 배우는 프로그램" |
| **왜 필요한가** | SOAP 메시지는 여러 중계 노드를 거칠 수 있다 | "서비스 분업" |
| **핵심 직관** | WS-Security는 봉투(SOAP)에 신분증(SAML), 서명(XML Signature), 봉인(XML Encryption), 발송 시... | "자물쇠" |
| **배경·문제의식** | 금융·공공·기업 연계 시스템은 SOAP, SAML, XML Signature를 여전히 사용한다 | "경험으로 배우는 프로그램" |
| **작동 원리** | Identity Provider가 SAML Assertion을 발급하고, SOAP Header에 WS-Security 토큰을 넣는다 | "경험으로 배우는 프로그램" |
| **비유** | 공문 봉투에 발급기관 도장, 문서 위변조 방지 서명, 비밀 문단 봉인, 발송 시각을 함께 붙여 여러 부서를 지나도 검증 가능하게 하는 절차... | "핵심 기술 요소" |
| **흔한 오해·주의점** | TLS는 전송 구간 보호이고 WS-Security는 메시지 단위 보호다 | "암호화 봉투" |

---


## Ⅰ. 개요 및 필요성

- 개요: SOAP 메시지 보안 통제
- 배경: 기업 간 연계 메시지는 ESB, Gateway, 중계 서버를 지나 저장·재전송될 수 있어 전송 구간 TLS만으로는 메시지 단위 검증이 어려움.
- 필요성: SAML 2.0, WS-Security, XML Signature, XML Encryption, timestamp를 메시지 내부에 포함해 신원, 무결성, 기밀성, 재전송 방지를 검증해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
IdP -> SAML Assertion -> SOAP WS-Security Header
Client -> XML Signature/Encryption -> ESB/Gateway -> Service Validation -> Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SAML Assertion | 사용자·속성·조건 전달 | Issuer, Subject, Audience, Conditions |
| WS-Security Header | 토큰, 서명, timestamp 포함 | UsernameToken, BinarySecurityToken |
| XML Signature | 메시지 무결성·발신자 검증 | signed element, canonicalization |
| XML Encryption | 민감 필드 암호화 | Body 전체 또는 요소 단위 |
| Replay 방지 | 중복 메시지 차단 | Timestamp, Nonce, message-id cache |

> 요약: SAML은 신원, WS-Security는 SOAP Header 기반 토큰·서명·암호화·재전송 방지를 담당한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Assertion 발급 -> SOAP Header 삽입 -> Body/Assertion 서명
-> 필요 필드 암호화 -> 수신 검증 -> replay/cache 확인 -> 업무 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | IdP가 SAML Assertion 발급 | issuer, audience, subject, 조건 |
| 2 | 송신자가 SOAP 메시지 서명·암호화 | XML Signature, XML Encryption |
| 3 | 수신자가 인증서와 서명 참조 검증 | truststore, CRL/OCSP, `wsu:Id` |
| 4 | 시간·재전송 검증 | timestamp, nonce, clock skew 5분 이내 |
| 5 | 검증된 요소만 업무 처리 | signed body binding, audit log |

> 요약: 수신자는 신원, 서명 대상, 시간 조건, 중복 여부를 검증한 뒤 서명된 실제 요소만 처리한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 키워드 적용 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 보호 계층 | TLS 구간 보호 | 메시지 수준 서명·암호화 | 중계·저장 후 검증 가능 |
| 인증 정보 | ID/PW 전달 | SAML Assertion, BinarySecurityToken | audience, issuer, validity 확인 |
| 무결성 | 메시지 변조 탐지 미흡 | XML Signature | signed element와 업무 처리 객체 일치 |
| 재전송 방지 | 동일 SOAP 재사용 가능 | Timestamp+Nonce cache | clock skew 5분, nonce TTL 관리 |

> 요약: WS-Security는 전송 보호를 넘어 메시지 자체에 신원·서명·시간 조건을 넣어 중계 환경의 검증성을 확보한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 보호 범위 | TLS | WS-Security 메시지 보안 | ESB 중계, 저장 후 검증, B2B 연계 |
| 인증 방식 | 세션·API Key | SAML Assertion | 기업 SSO, 속성 기반 권한 전달 |
| 구현 복잡도 | REST JWT | SOAP+XML Signature | 레거시 공공·금융 연계 요구 |

> 요약: REST API에는 JWT/mTLS가 주로 맞고, XML 중계·공문서형 연계에는 SAML·WS-Security가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Signature Wrapping | 서명된 요소와 처리 요소 불일치 | ID 기반 signed element binding, schema hardening | wrapping test 100% 차단 |
| Replay 공격 | timestamp·nonce 검증 누락 | nonce cache, message-id, clock skew 제한 | duplicate message 차단 로그 |
| 인증서 신뢰 오류 | 만료·폐기 인증서 허용 | CRL/OCSP, truststore rotation | expired/revoked cert 0건 |

> 요약: XML 보안의 핵심 위험은 wrapping, replay, 인증서 신뢰 오류이며 부정 테스트와 캐시 지표로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 서명 검증 | Body·Assertion 서명 참조 100% 확인 | XMLSec test, negative corpus |
| 시간 통제 | clock skew 5분 이내, nonce TTL 5~10분 | replay cache metric |
| 감사 추적 | assertion id, message-id, certificate serial 기록 | SIEM, audit log review |

> 요약: 운영 점검은 서명 참조 검증, 시간·nonce 통제, 감사 식별자 기록으로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 메시지 설계: SOAP Header에 SAML Assertion, Timestamp, BinarySecurityToken을 포함하고 Body와 Assertion을 XML Signature로 서명
2. 검증 구현: 수신 측에서 issuer/audience/conditions, certificate CRL/OCSP, `wsu:Id` 기반 signed element binding, clock skew 5분을 검증
3. 운영 통제: nonce/message-id cache TTL 5~10분, signature wrapping 테스트 20종, assertion id와 certificate serial을 SIEM에 기록

**결론 (2줄):**
- 기술사 판단: ESB·B2B·공공 SOAP 연계는 TLS만으로 부족하므로 SAML Assertion과 WS-Security 메시지 서명을 적용해야 함
- 향후 방향: 레거시 XML 연계는 API Gateway 전환 시 JWT/mTLS와 병행하되, 법적 증적이 필요한 메시지는 XML Signature 검증 체계를 유지해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "웹 서비스 보안을 설명하시오" | Assertion 발급, SOAP 서명, 암호화, 수신 검증 흐름 | TLS와 메시지 보안 차이, 재전송 방지 |
| 요구사항 명시형 | "SAML/WS-Security 적용 방안을 제시하시오", "XML 보안을 설계하시오" | signed element binding, clock skew, replay cache | signature wrapping 대응, 인증서 폐기 점검 |

> 요약: 설명형은 SAML·WS-Security 구성과 흐름을, 설계형은 XML 서명 검증 실패 모드와 재전송 방지를 중심으로 작성한다.
