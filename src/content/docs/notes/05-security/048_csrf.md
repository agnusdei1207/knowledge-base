---
sidebar:
  order: 48
  label: "048. CSRF"
  badge:
    text: "기출 · 50%"
    variant: note
title: "브라우저 자동 자격증명 악용 및 비승인 상태 변경 방어 : CSRF"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 48
extra:
  question_no: "48"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "CWE-352, 쿠키 자동 첨부 악용, Anti-CSRF 토큰(동기화 토큰 패턴), SameSite 쿠키(Lax/Strict), Origin/Referer 검증 및 재인증(Step-Up Auth)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CSRF (Cross-Site Request Forgery, CWE-352)**: 로그인된 사용자의 브라우저를 속여 의도치 않은 비승인 상태 변경(송금, 정보 수정 등)을 전송시키는 공격.
- **Ambient Authority Defect (자격증명 자동 전송 맹점)**: 브라우저가 교차 사이트 요청 시에도 도메인 쿠키를 자동으로 실어 보내 발생하는 보안 결함.

</details>

- 정의/개념: 인증된 브라우저 세션을 악용한 비인가 상태 변경 요청에 맞서 **Anti-CSRF 토큰, SameSite 쿠키, Origin 검증으로 사용자 의도를 실증하는 보안 기술**
- 배경/필요성: 브라우저의 쿠키 자동 전송 메커니즘으로 인한 **사용자의 실제 의도(Intent)와 자격증명 구분 불가, 비승인 금전 이체 및 계정 탈취 발생**

#### 한줄 요약
- Anti-CSRF 토큰과 SameSite 쿠키 및 Origin 검증을 통해 브라우저 요청의 사용자 의도 무결성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Anti-CSRF Token (동기화 토큰 패턴)**: 세션에 저장된 암호학적 난수와 폼/헤더의 토큰값이 일치하는지 백엔드에서 검증하는 메커니즘.
- **SameSite Cookie**: 타 사이트에서 발생하는 교차 사이트 요청 시 쿠키 첨부를 브라우저 수준에서 제한하는 속성(`Strict`, `Lax`).

</details>

- **사용자의 명시적 요청 의도(Intent) 실증**: 세션 쿠키 외에 **추측 불가능한 일회성 Anti-CSRF 토큰을 대조하여 요청 진위 검증**
- **브라우저 레벨의 교차 출처 차단(SameSite)**: `SameSite=Lax/Strict` 설정을 통해 **타 사이트 링크/스크립트에서 시작된 요청의 쿠키 전송 차단**
- **안전한 HTTP 메서드(Safe Methods) 강제**: 데이터 변경(CUD)에 `GET` 메서드를 배제하고 **`POST`/`PUT`/`DELETE` 메서드에 대해서만 엄격 토큰 검증**

#### 한줄 요약
- 명시적 의도 실증, SameSite 브라우저 차단, 안전한 HTTP 메서드 강제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Step-Up Authentication (재인증)**: 거액 송금이나 비밀번호 변경 등 고위험 작업 시 OTP나 비밀번호 재입력을 강제하는 추가 인증.

</details>

```text
[CSRF 다계층 방어 및 트랜잭션 무결성 아키텍처]
|-- Ingress: 공격자의 위조 HTTP 요청 (attacker.com -> POST /transfer)
`-- Layer 1: Browser Defense (SameSite=Lax/Strict 정책 -> 쿠키 첨부 누락)
`-- Layer 2: Network & Gateway (Origin / Referer 헤더 신뢰 도메인 검증)
`-- Layer 3: Application Server (Anti-CSRF Token Interceptor -> 세션 토큰 불일치 시 403 차단)
`-- Layer 4: High-Risk Action (Step-Up 재인증 / OTP 확인 후 최종 상태 변경)
```

선의 의미: 공격자의 위조 요청이 SameSite 쿠키 필터, Origin 검증, Anti-CSRF 토큰 대조, 단계별 재인증을 거쳐 완벽히 차단되는 심층 방어 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SameSite 쿠키 엔진** | 교차 사이트 요청에 대해 **인증 쿠키 전송을 브라우저에서 차단** | RFC 6265bis |
| **Origin/Referer 필터**| 요청 헤더의 발신 도메인이 **자사 신뢰 도메인과 일치하는지 검증** | Origin Check |
| **Anti-CSRF 인터셉터** | 폼 또는 헤더의 일회성 난수와 **서버 세션 난수 일치성 검증** | Token Check |
| **안전 메서드 라우터** | `GET` 요청을 통한 **DB 상태 변경(CUD)을 아키텍처 수준에서 원천 금지** | Safe Methods |
| **Step-Up 재인증기** | 비밀번호 변경, 거액 이체 시 **OTP 또는 재인증을 강제 집행** | Step-Up Auth |

#### 한줄 요약
- SameSite 쿠키 엔진, Origin 필터, Anti-CSRF 토큰 인터셉터, 안전 메서드 라우터, Step-Up 재인증기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SOP (Same-Origin Policy)**: 브라우저가 다른 도메인의 DOM 객체나 쿠키를 직접 스크립트로 읽지 못하도록 격리하는 보안 정책.

</details>

```text
정상 폼 요청, 위조 요청 발생, SameSite 차단, 토큰 인터셉터 검증 및 403 차단 파이프라인
        │
   1. [정상 폼 요청] 사용자가 송금 페이지 접속 ➔ 서버가 암호학적 난수(`csrf_token`)를 세션 및 폼에 주입
        │
   2. [공격자 함정 유입] 사용자가 타 탭에서 공격자의 악성 웹사이트(`attacker.com`) 로드
        │
   3. [위조 요청 자동 발생] 악성 스크립트가 은행 URL(`POST /transfer`)로 이체 요청 전송
        │
   4. [SameSite 쿠키 차단] 최신 브라우저가 `SameSite=Lax` 정책에 따라 세션 쿠키를 누락하고 전송
        │
   ├─ [쿠키가 첨부되어 도달한 경우: 2차 방어]
   ▼
5. [서버 토큰 인터셉터 검증]
    ├─ 서버가 세션의 `csrf_token`과 HTTP 요청 본문의 `csrf_token`을 비교
    └─ 공격자는 SOP로 토큰을 알 수 없으므로 `csrf_token` 누락/불일치 ➔ [403 Forbidden 차단]
        │
   ▼
6. [보안 로그 기록] 위조 요청 이벤트를 SIEM으로 전송하고 트랜잭션 강제 중단
```

#### 한줄 요약
- 정상 폼 난수 발급 → 악성 위조 요청 전송 → SameSite 쿠키 차단 → Anti-CSRF 토큰 대조 → 403 차단 및 로깅 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Anti-CSRF 토큰** vs **SameSite 쿠키 속성** vs **Origin / Referer 헤더 검증**.

</details>

| 비교 항목 | Anti-CSRF 토큰 (Synchronizer) | SameSite 쿠키 속성 | Origin / Referer 헤더 검증 |
|:---|:---|:---|:---|
| **방어 메커니즘** | **세션 난수와 폼/헤더 토큰 일치성 검증** | **타 도메인 교차 요청 시 쿠키 전송 차단** | **요청 시작 발신 도메인 화이트리스트 대조** |
| **방어 집행 위치** | **웹 애플리케이션 백엔드 서버 로직** | **사용자 웹 브라우저 렌더링 엔진** | **웹 서버, WAF, 리버스 프록시 앞단** |
| **구현 및 운영 복잡도**| 보통~높음 (모든 상태 변경 폼/API 수정)| **매우 낮음 (웹 서버 쿠키 헤더 설정 1줄)**| **낮음 (공통 인터셉터/WAF 규칙 적용)** |
| **XSS 취약점 연계 시** | 취약 (XSS로 토큰 탈취 시 무력화) | **우회 불가 (타 도메인 출발 시 완벽 차단)**| 취약 (동일 출처 XSS 내부 요청 시 통과) |
| **레거시 호환성** | **완벽 (모든 브라우저 및 HTTP 환경 지원)**| 구형 브라우저(IE 등)에서 미지원 가능 | 프록시가 개인정보 보호로 헤더 삭제 시 오탐 |

#### 한줄 요약
- Anti-CSRF 토큰은 서버 로직의 정석, SameSite는 브라우저 단의 고효율 방어, Origin 검증은 앞단 게이트웨이 통제이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Double Submit Cookie**: Stateless 환경(REST API)에서 CSRF 난수를 암호화 쿠키와 커스텀 요청 헤더에 동시에 담아 서버가 대조하는 패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 세션 쿠키만 검증하여 **사용자 권한으로 비인가 금전 이체 및 비밀번호 변경 사고 발생** | **`모든 상태 변경(POST/PUT)에 Anti-CSRF 토큰 검증 인터셉터 의무 적용`** | 브라우저 쿠키 자동 첨부를 악용한 위조 요청 100% 차단 |
| 상태 변경 기능을 **`GET /delete?id=1` 형태로 구현하여 `<img>` 태그 하나로 침해** | **`상태 변경 비즈니스 로직에 POST 메서드 강제 및 GET 요청 상태 변경 엄격 금지`** | 이미지 태그나 링크 클릭을 통한 비인가 상태 변경 소멸 |
| XSS 취약점과 연계되어 **스크립트에 의해 CSRF 토큰까지 탈취되는 복합 공격** | **`중요 트랜잭션 직전 OTP/재인증(Step-Up Auth) 강제 및 XSS 선제 차단`** | 취약점 체이닝 공격 시에도 사용자 명시적 개입으로 피해 차단 |
| SPA/REST API 환경에서 세션 저장소 부재로 인한 토큰 검증 곤란 | **`Double Submit Cookie 패턴 및 커스텀 요청 헤더(X-CSRF-Token)` 검증** | 무상태(Stateless) API 환경에서도 안전한 CSRF 방어 달성 |

#### 한줄 요약
- Anti-CSRF 토큰으로 의도를 검증하고, 안전한 메서드를 강제하며, 고위험 작업은 재인증으로 보호한다.

## Ⅶ. 결론

- 웹 애플리케이션의 신뢰 권한 모델을 악용하는 비승인 요청을 무력화하는 **CSRF 방어 아키텍처는 트랜잭션 무결성 보호의 필수 요소**이며, 실무 구현 시 **SameSite=Lax/Strict 쿠키 정책 전면 적용, 동기화 Anti-CSRF 토큰 및 Double Submit Cookie 패턴 구현, Origin/Referer 헤더 출처 검증, 고위험 작업에 대한 Step-Up 재인증 체계**를 결합하여 사용자 의도에 기반한 완전무결한 웹 트랜잭션 보안 완성

#### 한줄 요약
- CSRF 방어는 SameSite 쿠키와 Anti-CSRF 토큰 및 Step-Up 재인증을 결합하여 교차 사이트 요청 위조를 완벽히 차단하는 트랜잭션 보안 체계다.