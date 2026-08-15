---
sidebar:
  order: 53
  label: "053. 보안 응용 프로그래밍 인터페이스 설계 (Secure API Design)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "보안 응용 프로그래밍 인터페이스 설계 (Secure API Design)"
date: "2026-08-13T19:44:00+09:00"
tags:
  - "notes-security"
weight: 53
extra:
  question_no: "053"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "123회 기출이며 현대 API 인증•인가 설계성이 높음"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 다른 소프트웨어 애플리케이션 서비스 간 데이터를 주고받기 위한 접점 프로토콜 규격.
- **보안 API 설계(Secure API Design)**: API 서비스 전 구간에 걸쳐 채널 암호화, 호출자 인증, 토큰 기반 인가, BOLA 방지 및 무제한 호출 차단 통제를 설계 구현하는 기법.

</details>

- 정의/개념: 요청별 인증•인가•자원 제한의 **보안 API 설계**
- 배경/필요성: 토큰 검증만으로는 **BOLA•자원 고갈** 차단 불가

#### 한줄 요약

- 토큰 서명 검증뿐만 아니라 요청 매개변수 단위 객체 소유권 검증 및 Rate Limiting을 결합하여 API 보안성을 확보함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **접근 토큰(Access Token)**: OAuth 2.0 규격에서 클라이언트가 자원 서버의 특정 리소스에 접근할 수 있음을 증명하는 서명된 토큰(JWT).
- **범위(Scope)**: 접근 토큰에 부여된 세부 접근 권한(read, write 등)의 허용 명세.
- **객체 인가(Object-Level Authorization / BOLA Defense)**: 요청자가 호출 파라미터로 지정한 특정 자원 객체(ID)의 실제 소유주인지 매 요청마다 대조 검증하는 기법.
- **기능 인가(Function-Level Authorization)**: 요청 주체의 역할(Role)이 해당 API 엔드포인트 기능 실행 권한을 보유하는지 판정하는 기법.
- **호출률 제한(Rate Limiting)**: IP 또는 토큰 주체별 단위 시간당 API 호출 건수를 제한하여 DoS 및 무차별 대입을 차단하는 기술.

</details>

- 호출자 신원 인증과 백엔드 자원 **객체 인가**, **기능 인가**의 이중 분리 통제.
- **접근 토큰(Access Token)** 내 **범위(Scope)**, 만료시간(exp), 서명 무결성 및 클라이언트 채널 바인딩 검증.
- API 게이트웨이 기반 트래픽 폭주 차단용 **호출률 제한(Rate Limiting)** 적용.

#### 한줄 요약

- 접근 토큰 기반 인가, 객체 수준 권한 대조(BOLA 방지) 및 호출률 제한을 통합 적용함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **API 게이트웨이(API Gateway)**: 외부 요청을 단일 접점에서 맞아 인증, 토큰 검증, 라우팅, Rate Limiting 및 WAF 보안을 일관 집행하는 차단막.
- **인증•권한 서버(Authorization Server)**: OAuth 2.0/OIDC 규격에 맞춰 클라이언트 신원을 검증하고 접근 토큰을 발급하는 인프라.
- **자원 서버(Resource Server)**: 실제 비즈니스 데이터를 보유하며, API 게이트웨이를 거친 요청의 세부 객체 소유권 인가를 재검증하는 서비스 백엔드.

</details>

```text
보안 API 구조
├─ 등록 클라이언트: 호출 주체 식별
├─ 인증•권한 서버: 접근 토큰 발급
├─ API 게이트웨이: 토큰•채널•호출률 검증
├─ 자원 서버: 객체•기능 권한 집행
└─ 키•인증서•감사: 신뢰 수명•이력 관리
```

| 구성요소 | 책임 |
|:---|:---|
| 등록 클라이언트 | Client ID/Secret 식별 및 OAuth 2.0 PKCE 인증 수행 |
| 인증•권한 서버 | **인증•권한 서버**가 JWT 기반 접근 토큰 서명 및 발급 |
| API 게이트웨이 | **API 게이트웨이**가 토큰 서명, mTLS 채널 및 **호출률 제한** 1차 검증 |
| 자원 서버 | **자원 서버**가 요청 파라미터의 **객체 인가** 및 비즈니스 로직 2차 검증 |
| 키•인증서•감사 | JWKS 서명 키 로테이션, mTLS 인증서 수명 및 API 통계 로그 관리 |

#### 한줄 요약

- 게이트웨이의 1차 서명/호출률 검증과 자원 서버의 2차 객체 인가 검증을 결합함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **자바스크립트 객체 표기법(JavaScript Object Notation, JSON)**: API 파라미터 교환 시 사용되는 표준 데이터 포맷.
- **JSON 웹 토큰(JSON Web Token, JWT)**: Header, Payload, Signature로 구성된 무상태(Stateless) 자격증명 토큰.
- **상호 전송 계층 보안(Mutual Transport Layer Security, mTLS)**: 클라이언트와 서버 양단 간 X.509 인증서 기반 상호 인증 채널 기술.
- **mTLS•접근 토큰 검증**: 통신 채널 mTLS 상호 인증 및 JWT 토큰 서명 무결성을 확인하는 단계.
- **입력 크기•호출률 통제**: 페이로드 바이트 제한 및 Throttling 룰을 집행하는 단계.
- **객체 소유권 검증**: 요청 파라미터의 객체 식별자와 토큰 세션 주체 간 소유권을 대조하는 단계.
- **기능•범위 인가**: API 엔드포인트 접근 권한 및 Scope 매핑을 판정하는 단계.
- **호출•인가 판정 기록**: API 처리 이력 및 보안 감사 로그를 보존하는 단계.

</details>

```text
JWT 접근 토큰•API 요청
          │
          ▼
1. mTLS•접근 토큰 검증
          │
          ▼
2. 입력 크기•호출률 통제
          │
          ▼
3. 객체 소유권 검증
          │
          ▼
4. 기능•범위 인가
          │
          ├─ 거부 ── 오류•감사 기록
          │
          └─ 허용 ── 5. 호출•인가 판정 기록
                              │
                              ▼
                          제한된 API 응답
```

### 동작 원리

1. **mTLS•접근 토큰 검증**: mTLS 상호 채널 형성 및 **JWT** 접근 토큰 서명/만료시간 확인.
2. **입력 크기•호출률 통제**: API 페이로드 규격 검증 및 **호출률 제한(Rate Limiting)** 적용.
3. **객체 소유권 검증**: 자원 서버에서 쿼리 대상 객체 ID와 요청자 세션 간 **객체 인가** 검증.
4. **기능•범위 인가**: 해당 API 엔드포인트 호출 권한 및 OAuth Scope 매칭 대조.
5. **호출•인가 판정 기록**: 모든 정상/거부 요청 이력을 SIEM 및 감사 로그로 저장.

#### 한줄 요약

- mTLS/JWT 서명 검증, 호출률 통제, 자원 서버 객체 인가 및 감사 로그 기록을 순차 집행함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **개방형 권한 위임 2.0(OAuth 2.0)**: 토큰 기반으로 자원 접근 권한을 위임하는 오픈 표준 프레임워크.
- **코드 교환용 증명 키(Proof Key for Code Exchange, PKCE)**: 모바일/SPA 클라이언트의 인가 코드 탈취를 막는 OAuth 2.0 확장 규격.

</details>

| 통제 지점 | 대표 수단 | 역할•잔여 위험 |
|:---|:---|:---|
| API 호출 경계 | 계층형 인증•인가•입력 검증 | 전 구간 관제 보장 / 게이트웨이-백엔드 간 인가 미비 주의 |
| 주장 전달 | **JWT** | 무상태 자격증명 / 서명 키 유출 및 강제 탈취 유의 |
| 권한 위임 | **OAuth 2.0/PKCE** | 안전한 제3자 리소스 위임 / Scope 권한 과다 부여 유의 |
| 서비스 신원 | **mTLS** | L4/L7 구간 상호 인증 / 객체 수준 BOLA 검증은 별도 필요 |

#### 한줄 요약

- 경계 보호, JWT 자격증명, OAuth 2.0/PKCE 권한 위임 및 mTLS 상호 인증을 계층 결합함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IETF RFC 9700**: OAuth 2.0 보안 구현 지침 및 위협 대응 모범 사례(Best Practices) 인터넷 표준.
- **OWASP API Top 10:2023**: API 고유의 10대 보안 위협(BOLA, BFLA, Unrestricted Resource Consumption 등) 분류.
- **객체 수준 인가 결함(Broken Object Level Authorization, BOLA)**: 타인의 객체 ID 파라미터 조작만으로 인가 없이 데이터 조회가 가능해지는 API 최다 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| OAuth 구현 미비에 따른 토큰 탈취 | **IETF RFC 9700** 지침 준수 및 **OAuth 2.0/PKCE** 적용 | 토큰 재전송 및 인가 코드 탈취 완전 차단 |
| BOLA 취약점에 의한 데이터 대량 탈취 | **OWASP API Top 10:2023** 기반 자원 서버 **객체 인가** 적용 | 사용자별 자원 소유권 매 요청 재검증 |
| 무제한 API 호출에 의한 DoS | 게이트웨이 **호출률 제한(Rate Limiting)** 및 페이로드 크기 통제 | 백엔드 자원 고갈 및 무차별 스캐닝 억제 |

#### 한줄 요약

- IETF RFC 9700 및 OWASP API Top 10:2023 가이드를 준수하여 BOLA 취약점을 예방하고 Rate Limiting을 결합함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **API 통제 선택 기준(API Control Selection Criteria)**: 권한 위임은 OAuth 2.0/PKCE, 통신 신원은 mTLS, 데이터 접근은 객체 인가 및 Rate Limiting을 결합하는 보안 가이드.

</details>

- **API 통제 선택 기준**에 의거하여 외부 권한 위임은 **OAuth 2.0/PKCE**, 시스템 간 통신은 **mTLS**, 비즈니스 백엔드는 **객체 인가** 및 **호출률 제한** 적용.

#### 한줄 요약

- 위임은 **OAuth/PKCE**, 통신은 **mTLS**, 객체는 BOLA 검증
