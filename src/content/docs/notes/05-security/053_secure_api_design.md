---
sidebar:
  order: 53
  label: "053. 보안 응용 프로그래밍 인터페이스 설계 (Secure API Design)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "RESTful/GraphQL API 보안 아키텍처 및 BOLA 방어 : 보안 API 설계 (Secure API Design & OWASP API Top 10)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-security"
weight: 53
extra:
  question_no: "053"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "OWASP API Top 10:2023, BOLA(API1:2023) 방어, OAuth 2.0 PKCE(RFC 7636/9700), mTLS 전송 계층 보호, Rate Limiting & Throttling"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **보안 API 설계(Secure API Design)**: 클라우드, 모바일, MSA(마이크로서비스 아키텍처) 환경에서 외부에 노출된 RESTful, GraphQL, gRPC 엔드포인트를 보호하기 위해 전송 계층 암호화(mTLS), 신원 인증(OAuth 2.0/OIDC), 토큰 인가(JWT), 세분화된 객체 수준 권한 검증(BOLA 방어), API 게이트웨이 트래픽 제어(Rate Limiting)를 전 구간에 계층적으로 내재화하는 엔지니어링 설계 방법론.
- **BOLA(Broken Object Level Authorization / OWASP API1:2023)**: 사용자가 정상적인 인증 토큰을 보유하고 있더라도, API 요청 파라미터 내의 객체 식별자(예: `/api/users/100/orders/2048`)를 타인의 ID로 변조할 때 백엔드 자원 서버가 해당 객체에 대한 실제 소유권(Ownership)을 검증하지 않아 비인가 데이터가 유출되는 심각한 인가 결함.

</details>

- 정의/개념: API 게이트웨이의 **외곽 경계 통제(Authentication, Throttling, Schema Validation)** 와 백엔드 자원 서버의 **심층 인가 통제(BOLA Ownership Check, Scope Enforcement, Audit Logging)** 를 분리 결합하는 **다계층 API 제로 트러스트 보안 아키텍처**
- 배경/필요성: 클라우드 네이티브, 마이크로서비스 아키텍처(MSA) 및 모바일/SPA 생태계가 확산됨에 따라 외부로 노출된 수많은 RESTful/GraphQL API 엔드포인트가 주요 공격 표면(Attack Surface)으로 부상하였으나, 단순한 네트워크 방화벽이나 API 게이트웨이의 외곽 인증만으로는 URL 객체 식별자 변조를 통한 타인 데이터 무단 탈취(BOLA: Broken Object Level Authorization) 및 대규모 자원 고갈(DoS) 공격을 효과적으로 방어하지 못하는 한계를 드러냄에 따라, API 게이트웨이의 외곽 트래픽 제어(Rate Limiting/mTLS/JWT 검증)와 백엔드 자원 서버의 객체 수준 심층 인가(BOLA 방어), OAuth 2.0 PKCE 및 DPoP(RFC 9449)를 결합한 보안 API 설계(Secure API Design) 아키텍처를 도입하여 **OWASP API Top 10 위협 선제 차단, 무상태(Stateless) 토큰의 비인가 재사용 방지 및 데이터 소유권 기반의 완벽한 접근 통제**를 달성할 필요

#### 한줄 요약
- 게이트웨이의 토큰/호출률 검증과 백엔드 자원 서버의 BOLA 객체 소유권 검증을 결합하여 안전한 API 생태계를 구축한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OAuth 2.0 PKCE(Proof Key for Code Exchange / RFC 7636 & RFC 9700)**: 모바일 앱이나 SPA(Single Page Application)와 같이 클라이언트 시크릿(Client Secret)을 안전하게 은닉할 수 없는 환경에서 인가 코드 가로채기(Interception) 공격을 방어하기 위해 동적 코드 챌린지(`code_challenge`)와 검증기(`code_verifier`)를 사용하는 확장 보안 표준.
- **호출률 제한 및 스로틀링(Rate Limiting & Throttling)**: 토큰 버킷(Token Bucket) 또는 슬라이딩 윈도우 알고리즘을 적용하여 클라이언트 IP, 사용자 계정, API Key별로 단위 시간당 호출 가능한 최대 요청 수를 제한함으로써 DoS 공격과 무차별 대입을 차단하는 기술.

</details>

- **이중 계층 인증/인가 분리 (Two-Tier AuthZ)**: 게이트웨이는 전역적 토큰 서명/스코프 검증을 수행하고, 자원 서버는 비즈니스 객체 단위 소유권(BOLA) 검증 전담
- **동적 자격증명 교환 보호 (OAuth 2.0 PKCE)**: 퍼블릭 클라이언트 환경에서의 인가 코드 탈취 및 위조 요청 원천 차단
- **전송 계층 및 채널 바인딩 (mTLS & DPoP)**: 클라이언트와 서버 간 mTLS 상호 인증 및 토큰 탈취 시 타 시스템 재사용을 방지하는 DPoP(RFC 9449) 적용

#### 한줄 요약
- 검증을 게이트웨이에 몰면 무상태 확장성은 얻지만 객체 소유권 판정을 통째로 잃으므로, API 보안은 단일 관문이 아니라 전역 조건과 데이터 소유권을 갈라 맡기는 이중 계층으로 설계된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DPoP(Demonstrating Proof-of-Possession / RFC 9449)**: 공개키 기반 비대칭 서명을 통해 특정 클라이언트 기기에만 Access Token을 암호학적으로 귀속(바인딩)시켜, 네트워크 도청이나 XSS로 토큰이 유출되더라도 타인이 재사용할 수 없도록 방어하는 최신 API 토큰 보안 규격.

</details>

```text
[ 클라이언트 (모바일 앱 / SPA 프론트엔드) ]
               │ (1. mTLS 채널 형성 + OAuth 2.0 DPoP 토큰 첨부)
               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. API 게이트웨이 계층 (API Gateway Layer: 외곽 경계 통제) ]          │
│  ├─ 호출률 제한 (Rate Limiting: Token Bucket 알고리즘 ➔ 초과 시 429 기각)│
│  ├─ 요청 스키마 유효성 검사 (OpenAPI / JSON Schema Validation)          │
│  └─ JWT 서명(Signature) 무결성 및 만료 시간(`exp`), 스코프(`scope`) 검증 │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (검증 완료된 내부 요청 라우팅)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 마이크로서비스 백엔드 자원 서버 계층 (Resource Server: 심층 인가) ]│
│  ├─ BOLA 방어: `WHERE resource_id = ? AND owner_id = token.user_id`     │
│  ├─ BFLA 방어: 기능 수준 권한(Role-Based / Policy-Based Method Auth)    │
│  └─ [ 소유권 불일치 시 ➔ 403 Forbidden 응답 및 비인가 접근 즉각 차단 ]  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. API 보안 모니터링 및 감사 계층 (Audit & Telemetry Layer) ]         │
│  └─ 이상 호출 패턴, BOLA 시도 이력, 4xx/5xx 에러율 실시간 SIEM 스트리밍 │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 클라이언트 요청이 API 게이트웨이에서 1차 검증(호출률/토큰)을 거치고, 백엔드 자원 서버에서 2차 검증(BOLA 객체 소유권)을 거쳐 안전하게 처리되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **API 게이트웨이** | 단일 진입점에서 mTLS 종단, JWT 서명 검증, 호출률 제한(Throttling) 및 스키마 검증 | Edge Gateway |
| **인증/인가 서버 (IdP)** | OAuth 2.0 / OIDC 표준 기반 토큰 발급, PKCE 검증, 토큰 수명(TTL) 관리 | Authorization |
| **자원 서버 (Resource Server)**| 비즈니스 데이터베이스 질의 시 요청자 ID와 객체 소유권을 대조하여 BOLA 원천 차단 | BOLA Prevention|
| **DPoP 검증기** | 비대칭 개인키 서명을 대조하여 탈취된 Access Token의 제3자 비인가 재사용 방지 | RFC 9449 |
| **API WAF / 감사 모니터링** | API 전용 시그니처 분석, 비정상 대량 스크래핑 탐지 및 SIEM 감사 로그 보존 | Threat Detection|

#### 한줄 요약
- 다섯 요소는 같은 요청을 반복해 거르는 병렬 관문이 아니라, 전역 조건은 게이트웨이가·객체 소유권은 자원 서버가·토큰의 기기 귀속은 DPoP가 각기 다른 근거로 판정하는 분업 구조다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BOLA 방어 쿼리 작성 원칙**:
  - 취약한 코드: `SELECT * FROM orders WHERE order_id = :orderId` (타인의 `orderId`만 알면 조회 가능)
  - 안전한 코드: `SELECT * FROM orders WHERE order_id = :orderId AND user_id = :currentUserId` (토큰에서 추출한 본인 ID로 한정)

</details>

```text
1. [클라이언트 API 호출] 모바일 앱이 `GET /api/v1/orders/1024` 요청을 DPoP 서명 헤더와 함께 전송
            │
            ▼
2. [게이트웨이 호출률 검증] 토큰 버킷 알고리즘을 통해 클라이언트의 초당 요청 수(RPS) 확인 ➔ [임계치 미만 통과]
            │
            ▼
3. [게이트웨이 토큰 검증] JWT 서명 키(JWKS) 대조, 유효 기간(`exp`), 접근 권한 스코프(`orders:read`) 검증
            │
            ▼
4. [자원 서버 BOLA 인가 검증]
    ├─ 토큰 클레임에서 현재 로그인 사용자 식별자(`user_id = 501`) 추출
    └─ DB 쿼리 실행: `SELECT * FROM orders WHERE order_id = 1024 AND user_id = 501`
            │
            ├─ [해당 주문의 소유자가 아닐 경우 (데이터 없음)] ➔ 404 Not Found 또는 403 Forbidden 반환
            ▼
5. [안전 응답 반환 및 로깅] 소유권 검증 통과 데이터만 필터링하여 최소 정보(Data Minimization)로 JSON 응답 반환
```

**동작 원리**

1. **외곽 트래픽 제어**: 인가되지 않은 대량 무차별 요청을 최외곽 게이트웨이에서 사전에 드롭
2. **무상태 암호학적 검증**: 중앙 세션 저장소 병목 없이 공개키(JWKS) 기반으로 토큰 위변조 신속 판정
3. **요청 주체와 자원 매핑**: 단순 URL 파라미터에 의존하지 않고 신뢰된 토큰 컨텍스트와 데이터베이스 바인딩
4. **정보 유출 최소화**: 타인의 자원 존재 여부 자체를 은닉하기 위해 필요 시 404 응답으로 정보 노출 차단
5. **폐쇄 루프 감사 추적**: 반복적인 타인 객체 접근 시도를 지능형 API 위협으로 인지하여 차단 목록 등록

#### 한줄 요약
- 토큰 검증까지는 요청의 형식적 자격만 확인할 뿐이고 인가는 토큰에서 꺼낸 주체 ID가 질의 조건에 들어가는 순간 확정되므로, URL 파라미터를 신뢰하는 설계는 어떤 게이트웨이 규칙으로도 보완되지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **API 보안 통제 3대 축 비교**: 권한 위임(OAuth 2.0 PKCE), 주장 전달(JWT Token), 전송 암호화(mTLS)의 비교.

</details>

| 비교 항목 | 권한 위임 프로토콜 (OAuth 2.0 PKCE) | 신원/권한 전달 토큰 (JWT / DPoP) | 통신 채널 보안 (mTLS) |
|:---|:---|:---|:---|
| **보안 통제 계층** | **인가 위임 및 클라이언트 신뢰 검증** | **무상태 자격증명 및 클레임 전달** | **전송 계층(L4/L7) 상호 암호화** |
| **방어 메커니즘** | 코드 챌린지(`code_challenge`) 교환 | 암호학적 디지털 서명(RS256/ES256) | X.509 인증서 기반 양방향 핸드셰이크 |
| **주요 방어 위협** | **인가 코드 가로채기(Interception)** | **토큰 위변조, 세션 상태 불일치** | **중간자 도청(MitM), API 서버 스푸핑**|
| **시스템 확장성** | 보통 (인증 서버 트랜잭션 수반) | **매우 높음 (무상태 자체 검증 가능)** | 보통~낮음 (인증서 생애주기 관리 비용)|
| **적용 권장 환경** | **모바일 앱, SPA, 서드파티 오픈 API** | **MSA 서비스 간(S2S) 통신, REST API** | **금융 마이데이터, B2B 백엔드 연동** |

#### 한줄 요약
- 셋은 권한 위임·권한 전달·채널 보호라는 서로 다른 문제를 맡아 대체 관계가 아니며, 무상태 JWT가 얻은 확장성은 탈취 후 재사용 위험을 남기므로 DPoP와 mTLS가 그 대가를 나눠 갚는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OWASP API Security Top 10:2023 3대 핵심 위협**:
  - API1: BOLA (객체 수준 인가 결함 / 최다 발생)
  - API2: Broken Authentication (취약한 인증)
  - API4: Unrestricted Resource Consumption (무제한 자원 소비 / DoS)

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 토큰 인증만 통과하면 URL 객체 ID 조작으로 **타인의 개인정보 및 거래 내역이 대량 유출되는 BOLA 사고** | **자원 서버 계층에서 토큰 내 주체 ID와 요청 자원의 소유권을 매 질의마다 교차 검증(`AND user_id = :userId`)** | 파라미터 변조를 통한 타인 데이터 무단 탈취 취약점 100% 원천 제거 |
| 대규모 봇넷이 자동화 스크립트로 초당 수만 건의 API를 호출하여 **백엔드 DB 자원 고갈(DoS) 및 장애** | **API 게이트웨이 전단에 IP/사용자 단위의 슬라이딩 윈도우 Rate Limiting 및 요청 본문 크기 제한** | 비정상 과다 호출 트래픽 100% 드롭 및 백엔드 비즈니스 가용성 99.99% 보장 |
| 모바일 앱 환경에서 인가 코드가 가로채기 공격에 노출되어 **제3자가 불법적으로 Access Token을 발급받는 사고** | **IETF RFC 9700 지침에 따라 모바일 및 SPA 클라이언트에 OAuth 2.0 PKCE 확장 규격 강제** | 인가 코드 탈취 공격 무력화 및 클라이언트 자격증명 발급 무결성 확보 |

#### 한줄 요약
- 자원 서버 BOLA 검증으로 데이터를 보호하고, Rate Limiting으로 가용성을 지키며, PKCE로 토큰 발급을 보호한다.

## Ⅶ. 결론

- 디지털 전환과 오픈 API, 금융 마이데이터 및 MSA 환경에서 전사 비즈니스 자산을 외부에 안전하게 노출하고 보호하는 **현대 클라우드 소프트웨어 아키텍처 및 제로 트러스트(Zero Trust) API 생태계의 핵심 설계 표준**으로 확고히 자리 잡았으며, AI 기반 API 이상 행위 탐지 및 서비스 메시(Service Mesh) 기반 mTLS 통신으로 진화하는 가운데, 실무 보안 API 설계 시에는 **API 게이트웨이 전단에 슬라이딩 윈도우 호출률 제한(Rate Limiting) 및 OpenAPI 스키마 검증 구축, 자원 서버 계층에서 데이터베이스 질의 시 토큰 클레임 기반의 객체 소유권(BOLA/BFLA) 검증 100% 강제, 모바일/SPA 환경을 위한 OAuth 2.0 PKCE(RFC 9700) 및 암호학적 기기 바인딩 토큰 DPoP(RFC 9449) 적용**을 결합하여 무결점 엔드투엔드 API 보안 라이프사이클을 완성

#### 한줄 요약
- 게이트웨이 경계 통제와 백엔드 BOLA 소유권 검증 및 PKCE/DPoP를 결합하여 안전한 API 환경을 완성한다.
