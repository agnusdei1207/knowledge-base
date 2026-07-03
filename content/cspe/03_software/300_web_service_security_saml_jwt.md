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
- **개요**: SAML과 JWT는 **인증(Authentication)** 결과와 **인가(Authorization)** 정보를 서비스 간에 안전하게 전달하기 위한 **보안 토큰(Security Token)** 표준이다.
- **왜 필요한가**: 여러 서비스가 같은 사용자를 매번 비밀번호로 재확인하면 사용자 경험이 나빠지고, 각 서비스가 비밀번호를 저장·비교하는 만큼 유출 위험 지점도 늘어난다. 인증은 한 곳(IdP)에서 하고, 그 결과만 토큰으로 전달하면 이 문제가 해결된다.
- **핵심 직관**: 놀이공원 입장권에 이름·유효시간·이용 가능한 시설이 적혀 있고, 각 시설은 매번 신분 재확인 없이 입장권의 서명과 만료시간만 확인하는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 인증(Authentication) | "이 사람이 누구인가"를 확인하는 절차 | 신분증 확인 |
| 인가(Authorization) | "이 사람이 무엇을 할 수 있는가"를 결정하는 절차 | 출입 등급 부여 |
| SSO (Single Sign-On) | 한 번 로그인으로 여러 서비스를 이용하는 방식 — SAML의 주 용도 | 사원증 한 장으로 모든 건물 출입 |
| SAML (Security Assertion Markup Language) | 인증 결과를 XML 형식의 Assertion으로 표현하는 표준 | 관공서 공문서 양식 승인서 |
| Assertion | SAML에서 "이 사용자는 인증됐고 이런 속성을 가진다"를 담은 XML 블록 | 승인 도장이 찍힌 확인서 |
| IdP (Identity Provider) | 사용자를 실제로 인증하고 토큰/Assertion을 발급하는 서버 | 신분증을 발급하는 주민센터 |
| SP (Service Provider) | 토큰/Assertion을 받아 검증하고 서비스를 제공하는 쪽 | 신분증을 확인하는 매장 |
| JWT (JSON Web Token) | `header.payload.signature` 3부분을 점(.)으로 이은 JSON 기반 토큰 | QR 코드형 모바일 입장권 |
| Header | JWT의 첫 부분 — 서명 알고리즘(alg)과 타입(typ) 명시 | 입장권 발급 규격 표시 |
| Payload(Claims) | JWT의 둘째 부분 — iss(발급자)·sub(주체)·aud(대상)·exp(만료)·iat(발급시각) 등 | 입장권에 적힌 이름·시설·유효시간 |
| Signature | JWT의 셋째 부분 — header+payload를 비밀키(또는 개인키)로 서명한 값, 위변조 여부 검증용 | 입장권의 위조 방지 홀로그램 |
| Base64URL | JSON을 URL에 넣을 수 있는 문자로 인코딩하는 방식(암호화 아님, 누구나 디코딩 가능) | 내용을 다른 문자로 옮겨 적은 것뿐 — 자물쇠 아님 |
| JWS / JWE | JWT의 두 형태 — JWS는 서명만(내용 그대로 보임), JWE는 암호화까지(내용 안 보임) | JWS=봉투 없이 서명만, JWE=봉인된 봉투 |
| JWKS / kid | 서명 검증용 공개키 묶음(JWKS)과 그중 어떤 키를 썼는지 표시하는 식별자(kid) | 여러 도장 중 어떤 도장을 썼는지 표시 |
| alg=none 공격 | 서명 알고리즘을 "없음"으로 바꿔 서명 검증을 우회하려는 공격 | 위조 입장권에 "검사 생략" 도장을 스스로 찍는 것 |

## 깊이 이해

### JWT 구조를 실제 값으로 뜯어보기
- JWT는 `header.payload.signature`를 점(.)으로 연결한 문자열이다. 각 부분은 Base64URL로 인코딩된다.
- **Header 예시**: `{"alg":"RS256","typ":"JWT"}` → Base64URL 인코딩하면 `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9`
- **Payload 예시**: `{"iss":"https://idp.example.com","sub":"user-1234","aud":"order-api","exp":1751500200,"iat":1751499600}` → `exp - iat = 600`초, 즉 **발급 후 10분(600초)** 만료되는 토큰임을 숫자로 바로 읽을 수 있다.
- **Signature**: header와 payload를 이어붙인 문자열을 IdP의 개인키(RS256이면 RSA 개인키)로 서명한 값이다. 서비스는 IdP의 공개키(JWKS에서 `kid`로 찾음)로 이 서명을 검증해 "IdP가 실제로 발급했고 내용이 변조되지 않았다"를 확인한다.
- **오해 확인**: Base64URL은 누구나 디코딩할 수 있는 인코딩이지 암호화가 아니다. 위 payload 예시처럼 sub, aud 값이 그대로 노출되므로, 주민번호 같은 민감정보를 payload에 넣으면 안 된다(JWE를 쓰지 않는 한).

### SAML Assertion 구조를 예로 이해하기
- SAML Assertion은 XML 문서이며 핵심 요소는 `<Issuer>`(발급자), `<Subject>`(대상 사용자), `<Conditions NotBefore="..." NotOnOrAfter="...">`(유효 기간), `<AttributeStatement>`(사용자 속성: 부서, 역할 등)이다.
- **예시**: `NotBefore="2026-07-03T09:00:00Z"`, `NotOnOrAfter="2026-07-03T09:05:00Z"`라면 유효시간은 정확히 **5분**이다. SP는 이 시간 범위 밖의 Assertion을 거부해야 재전송(replay) 공격을 막을 수 있다.
- Assertion 전체는 IdP의 X.509 인증서 개인키로 XML 전자서명되며, SP는 IdP의 공개 인증서로 서명을 검증한다.

### 검증 절차 — 무엇을 확인해야 안전한가
- 두 방식 모두 "서명이 유효한가", "누가 발급했는가(issuer)", "나를 위한 토큰인가(audience)", "아직 유효한가(expiry)"를 확인해야 한다. 하나라도 빠지면 토큰이 다른 목적/다른 서비스용으로 발급된 것을 그대로 받아들이는 사고가 난다.
- **audience 검증 누락 시나리오**: 서비스 A용으로 발급된 JWT(`aud: "service-a"`)를 서비스 B가 audience 확인 없이 서명만 검증하고 받아들이면, 사용자가 A에서 받은 토큰을 B에서도 그대로 사용해 A만 허용해야 할 권한이 B에서도 통과된다(confused deputy 유형 취약점).
- **alg=none 공격 시나리오**: 공격자가 JWT의 header를 `{"alg":"none"}`으로 바꾸고 signature 부분을 빈 문자열로 만든다. 서버 라이브러리가 alg 값을 그대로 신뢰해 "서명 없음이니 검증도 생략"해버리면, payload(예: `sub`, `role`)를 마음대로 조작한 토큰이 그대로 통과된다. 따라서 서버는 반드시 alg를 화이트리스트(RS256/ES256 등)로 강제하고 `none`을 명시적으로 차단해야 한다.

### 비유와 흔한 오해
- **비유**: SAML은 관공서 공문서 형식의 출입 승인서(발급 절차가 무겁고 신뢰도가 높은 브라우저 SSO에 적합), JWT는 QR 코드형 모바일 입장권(가볍고 API·모바일에 적합)에 가깝다.
- **오해 1**: JWT는 대개 서명(JWS)이지 암호화(JWE)가 아니다 — 내용이 보인다는 뜻이다.
- **오해 2**: 토큰이 탈취되면 만료 전까지는 유효한 토큰으로 계속 쓰일 수 있다. 그래서 access token은 짧게(5~15분) 만료시키고, 장기 세션은 refresh token 회전(rotation)과 재사용 탐지로 통제한다.

## 연결 개념
- OAuth 2.0 - 위임 인가 프레임워크(JWT가 access token 형식으로 자주 쓰임)
- OIDC - OAuth 2.0 위에 인증 계층을 추가한 표준(ID Token이 보통 JWT)
- WS-Security - SOAP 메시지 보안 표준(SAML과 같은 XML 기반 진영)

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

- 개요: SAML·JWT는 인증·인가 정보를 전달하는 보안 토큰이다.
- 배경: SSO와 API 연동에서는 인증 서버와 서비스가 분리되므로 신뢰 가능한 토큰 검증이 필요하다.
- 필요성: 서명, issuer, audience, expiry, scope를 확인해 웹 서비스 접근을 통제해야 한다.

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
