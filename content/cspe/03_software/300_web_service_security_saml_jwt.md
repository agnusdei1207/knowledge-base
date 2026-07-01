---
title: "웹 서비스 보안 - SAML·JWT (Web Service Security SAML JWT)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 300
---

# 📖 【암기용】 개념 완전 이해

> 목적: 웹 서비스 보안 SAML·JWT를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 웹 서비스에서 사용자의 인증 결과와 권한 정보를 토큰으로 전달하는 표준 방식
- **왜 필요한가**: 여러 서비스가 같은 사용자를 매번 비밀번호로 확인하면 사용자 경험과 보안 통제가 모두 깨진다.
- **핵심 직관**: 놀이공원 입장권에 이름, 유효시간, 이용 가능한 시설이 적혀 있고 각 시설은 입장권 서명과 만료시간을 확인하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 기업 SSO와 API 서비스는 인증 서버와 서비스 제공자가 분리된다. 인증 결과를 신뢰 가능한 형식으로 전달해야 비밀번호 공유 없이 접근을 허용할 수 있다.
- **작동 원리**: SAML은 XML 기반 assertion으로 브라우저 SSO에 많이 사용된다. JWT는 JSON 기반 compact token으로 OAuth 2.0·OIDC API 인증에 사용된다. 두 방식 모두 서명, 만료, audience, issuer 검증이 필요하다.
- **비유**: SAML은 공문서 양식의 출입 승인서, JWT는 QR 코드형 모바일 입장권에 가깝다.
- **구체 예시**: OIDC 로그인 후 API Gateway는 JWT의 `iss`, `aud`, `exp`, `kid`, signature를 검증하고 `scope=order:read`가 있을 때 주문 조회 API를 허용한다.
- **흔한 오해·주의점**: JWT는 암호화가 아니라 서명인 경우가 많다. payload는 Base64URL로 누구나 읽을 수 있으므로 주민번호 같은 민감정보를 넣으면 안 된다.

## 연결 개념
- OAuth 2.0 - 위임 인가 프레임워크
- OIDC - OAuth 2.0 위에 인증 계층을 추가한 표준
- WS-Security - SOAP 메시지 보안 표준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. SAML·JWT 비교와 검증 실패 시 공격 경로를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SAML·JWT는 인증·인가 정보를 서비스 간 전달하는 보안 토큰 형식이다.
> 2. **가치**: SSO, API 인증, 무상태 서비스에서 비밀번호 재입력 없이 issuer, audience, signature, expiry 검증으로 접근을 통제한다.
> 3. **판단 포인트**: 토큰 형식보다 서명 검증, 키 회전, 만료, scope·claim 최소화가 보안 수준을 결정한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 웹 인증·인가 표준 이해 확인 | SAML Assertion, JWT Claim, 서명, 만료 | SAML과 JWT를 단순 암호화 기술로 설명 |
| 서비스 구조 선택 판단 확인 | 기업 SSO는 SAML, API·OIDC는 JWT | OAuth, OIDC, JWT 역할 혼동 |
| 공격 대응 확인 | audience 검증, alg none 차단, key rotation | 토큰 탈취와 재사용 대응 누락 |

> 요약: 이 문제는 토큰 포맷 암기가 아니라 토큰 검증과 서비스별 적용 기준을 묻는다.

---

## Ⅰ. 개요 및 필요성

SAML·JWT는 웹 서비스에서 인증·인가 정보를 전달하는 보안 토큰이다. SSO와 API 연동에서는 인증 서버와 서비스가 분리되므로 신뢰 가능한 토큰 검증이 필요하다. 서명, issuer, audience, expiry, scope를 확인해 접근을 통제한다.

---

## Ⅱ. 구조 및 구성요소

```text
User -> Identity Provider -> Token(SAML/JWT) -> Service Provider/API -> Resource
                         / Signing Key/JWKS
                         / Policy/Scope
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Identity Provider | 사용자 인증 후 토큰 발급 | IdP, Authorization Server |
| Token | claim·assertion·만료·서명 포함 | SAML XML, JWT JSON |
| Service Provider/API | 토큰 검증 후 자원 제공 | audience·scope 확인 |
| Key Management | 서명키 배포·회전 | JWKS, certificate rollover |

> 요약: 구조는 IdP가 토큰을 발급하고 서비스가 서명·claim·정책을 검증한 뒤 자원 접근을 허용한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
로그인 요청 -> IdP 인증 -> 토큰 발급 -> 서비스 전달 -> 서명/만료/audience 검증 -> 권한 결정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자가 IdP에서 인증 수행 | MFA, session policy |
| 2 | IdP가 SAML Assertion 또는 JWT 발급 | `iss`, `sub`, `aud`, `exp` 포함 |
| 3 | 서비스가 서명·만료·issuer 검증 | RS256/ES256, `alg=none` 차단 |
| 4 | scope·role·claim 기준 접근 제어 | 최소 권한 scope |

> 요약: 동작은 IdP 인증, 토큰 발급, 서비스 검증, 권한 결정 순서이며 검증 누락은 토큰 위조·재사용으로 이어진다.

---

## Ⅳ. 특징

| 구분 | SAML | JWT | 수치·판단 기준 |
|:---|:---|:---|:---|
| 형식 | XML Assertion | JSON compact token | JWT 크기 수 KB 이하 |
| 주 사용처 | 기업 브라우저 SSO | API, OIDC, 모바일 | API Gateway 검증 |
| 키 검증 | X.509 인증서 | JWK/JWKS, `kid` | key rotation 90~365일 |
| 한계 | XML 처리 복잡 | 탈취 시 만료 전 재사용 | access token 5~15분 |

> 요약: SAML은 기업 SSO, JWT는 API·OIDC에 적합하며 두 방식 모두 서명과 만료 검증이 필수이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 서버 세션 공유 | 토큰 기반 인증·인가 | 다중 서비스·API 연동 |
| 비용/성능 | 중앙 세션 조회 | stateless 검증 가능 | JWKS 캐시 TTL 5~30분 |
| 운영/위험 | 세션 폐기 단순 | 토큰 탈취·키 회전 관리 | 민감 API는 짧은 만료 |

> 요약: 다중 API 환경은 토큰 기반 구조가 적합하지만, 탈취 대응과 키 회전 정책을 함께 설계해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 토큰 위조 | 서명 검증 누락 | RS256/ES256 강제, `alg=none` 차단 | 검증 실패 차단률 |
| 재사용 공격 | access token 탈취 | TLS, 짧은 만료, refresh token rotation | 이상 재사용 탐지 |
| 권한 과다 | scope·claim 과다 | 최소 scope, audience 분리 | 과권한 scope 건수 |

> 요약: 토큰 보안은 위조 차단, 재사용 탐지, 권한 축소를 중심으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 검증 완전성 | `iss`·`aud`·`exp`·signature 100% 검증 | gateway policy test |
| 토큰 수명 | access token 5~15분 | IdP 설정 점검 |
| 키 관리 | JWKS key rotation 90~365일 | key inventory audit |

> 요약: 성공 여부는 검증 항목 적용률, 토큰 수명, 키 회전 준수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 기업 SaaS SSO는 SAML 2.0과 X.509 인증서 rollover 절차를 적용하고 assertion audience를 서비스별로 분리
2. API·모바일은 OIDC JWT를 사용하되 API Gateway에서 `iss`, `aud`, `exp`, signature, scope를 100% 검증
3. access token은 5~15분, refresh token은 rotation과 reuse detection을 적용하고 JWKS cache TTL은 5~30분으로 설정

**결론 (2줄):**
- 기술사 판단: 브라우저 기반 기업 SSO는 SAML, API·마이크로서비스 인증은 OIDC JWT를 선택하고 둘 다 서명·만료·audience 검증을 필수화
- 향후 방향: 토큰 기반 보안은 Zero Trust, mTLS, step-up MFA와 결합해 사용자·기기·서비스 신뢰를 지속 검증해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | IdP 인증, 토큰 발급, 서비스 검증 흐름 | SAML과 JWT 형식·용도 차이 |
| 요구사항 명시형 | "비교하시오", "보안 대책", "설계하시오" | issuer·audience·signature·scope 검증 | 토큰 탈취, 키 회전, 만료 정책 |

> 요약: 설명형은 토큰 흐름, 보안형은 검증 실패 공격과 대응 지표 중심으로 전환한다.
