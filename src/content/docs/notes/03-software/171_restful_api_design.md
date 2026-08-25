---
sidebar:
  order: 171
  label: "171. RESTful API 설계 원칙"
  badge:
    text: "기출 · 70%"
    variant: note
title: "RESTful API 설계 원칙 (RESTful API Design)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 171
extra:
  question_no: "171"
  source_status: "기출"
  source_history: "122회"
  priority: 70
  priority_note: "자원•메서드•무상태 설계 원칙 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RESTful API 설계 원칙**: 명사형 URI로 자원을 식별하고, 표준 HTTP 메서드(GET, POST, PUT, PATCH, DELETE)와 상태 코드를 활용하여 무상태로 자원 상태를 조작하는 웹 아키텍처 원칙.
- **Richardson Maturity Model(RMM)**: Level 0(단일 URI/POST RPC)부터 Level 1(자원 식별), Level 2(HTTP 메서드 준수), Level 3(HATEOAS 링크)까지 REST 성숙도를 평가하는 모델.

</details>

- 정의/개념: 웹 표준 HTTP 프로토콜을 활용하여 **명사형 URI로 자원을 식별하고 표준 HTTP 메서드와 상태 코드로 상태를 조작하는 무상태 설계 원칙**
- 배경/필요성: 동사형 RPC 엔드포인트 남발 시 발생하는 **API 직관성 결여, HTTP 표준 캐싱 활용 불가 및 클라이언트-서버 간 강결합 해결 불가**

#### 한줄 요약
- 명사형 자원 식별과 HTTP 표준 메서드 및 무상태성을 준수하여 확장성과 독립성을 갖춘 API를 설계한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Uniform Interface**: 자원 식별(URI), 표현을 통한 조작(JSON), 자기 서술적 메시지(Self-descriptive), HATEOAS 4대 원칙.
- **Idempotency**: 동일한 요청을 여러 번 수행해도 서버의 상태가 단 한 번 요청했을 때와 동일하게 유지되는 성질(GET, PUT, DELETE).

</details>

- 행위가 아닌 자원(Resource) 자체를 명사형 복수형(`/users`, `/orders`)으로 식별하는 **URI 설계**
- 조회(GET), 생성(POST), 전체 교체(PUT), 일부 수정(PATCH), 삭제(DELETE)의 **HTTP 메서드 표준 매핑**
- 200(OK), 201(Created), 400(Bad Request), 404(Not Found) 등 **표준 HTTP 상태 코드 반환**

#### 한줄 요약
- 자원 식별, 표준 메서드 매핑, 무상태 통신을 통해 클라이언트와 서버의 완벽한 분리와 캐싱 성능을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RESTful API 4대 설계 계층**: Resource URI(자원 식별), HTTP Methods(행위 정의), Representation/Headers(표현/메타데이터), Status Codes(결과 통지).

</details>

```text
[RESTful API 표준 계층 아키텍처 및 자원 조작 구조]
|-- 1. Resource Identification Layer (명사형 복수 URI: `/api/v1/users/{userId}/orders/{orderId}`)
|-- 2. Standard HTTP Methods Layer
|   |-- GET (조회: Safe & Idempotent) / POST (생성: Non-Idempotent)
|   `-- PUT (전체교체: Idempotent) / PATCH (부분수정) / DELETE (삭제: Idempotent)
`-- 3. Representation & Headers Layer
    |-- Headers: `Content-Type: application/json`, `If-Match: "eTag123"`, `Cache-Control`
    `-- Body: JSON Representation (`{ "orderId": 100, "status": "PAID" }`)
`-- 4. Standard Response Status Layer (200 OK / 201 Created / 400 / 404 / 500)
```

선의 의미: 계층 및 명사형 URI로 자원을 특정하고 HTTP 메서드로 조작하여 표준 상태 코드와 JSON 표현을 반환하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **자원 식별자 (URI)** | 행위(동사)를 배제하고 **명사형 복수형 계층 구조로 비즈니스 엔터티 식별** | `/users/{id}` |
| **HTTP 메서드 (Verbs)** | CRUD 행위를 **표준 HTTP 메서드(GET/POST/PUT/PATCH/DELETE)로 일관 매핑** | 의미론적 일관성 |
| **HTTP 상태 코드** | 처리 결과를 **2xx(성공), 4xx(클라이언트 오류), 5xx(서버 오류)로 명확히 전달** | 표준 상태 규약 |
| **HTTP 헤더 및 표현** | Content-Type, Accept, Cache-Control, **ETag 등을 통해 메타데이터와 캐싱 제어** | 무상태 제어 |

#### 한줄 요약
- URI(자원), HTTP Method(행위), Representation(표현), Status Code(결과)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RESTful 요청 처리 5단계**: URI 자원 식별 $\to$ 메서드/인가 검증 $\to$ 조건부 ETag 동시성 검사 $\to$ 도메인 로직 실행 $\to$ 상태 코드 및 HATEOAS 회신.

</details>

```text
클라이언트의 주문 자원 수정 요청 수신
        │
   1. [자원 식별] 요청 URI(`/orders/101`)를 파싱하여 대상 엔터티 식별
        │
   2. [메서드 및 권한 검증] `PATCH` 메서드의 유효성과 JWT Bearer 토큰의 인가 권한 확인
        │
   3. [조건부 동시성 검사] `If-Match: "eTag-v1"` 헤더를 대조하여 동시 수정 덮어쓰기(Lost Update) 방지
        │
   4. [도메인 로직 수행] 주문 상태를 업데이트하고 최신 상태를 JSON 객체로 직렬화
        │
   5. [상태 코드 및 링크 회신] HTTP `200 OK`와 함께 다음 가능한 상태 전이 HATEOAS 링크 반환
```

#### 한줄 요약
- 자원 식별 → 메서드 검증 → ETag 검사 → 로직 수행 → 상태 코드 회신 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RPC 스타일 vs RESTful 스타일**: 행위 함수 호출 중심(RPC)과 자원 상태 전이 중심(RESTful).

</details>

| 비교 항목 | RPC 스타일 API (원격 프로시저 호출) | RESTful API 스타일 (자원 중심) |
|:---|:---|:---|
| 엔드포인트 설계 | **`/createUser`, `/deleteUser` 등 동사형 URI**| **`/users` 명사형 URI + HTTP Method 매핑** |
| 통신 방식 및 메서드| 모든 요청을 HTTP POST 단일 메서드로 처리 | **표준 HTTP 메서드(GET, POST, PUT, DELETE) 분기**|
| HTTP 캐싱 활용 | 불가능 (POST 요청은 브라우저/CDN 캐싱 불가) | **가능 (GET 요청에 대한 Cache-Control, ETag 활용)**|
| 최적 적용 대상 | **복잡한 다단계 비즈니스 프로세스, 배치 실행** | **대고객 CRUD 서비스, 웹/모바일 표준 API, 오픈 API**|

#### 한줄 요약
- 단순 프로시저 실행은 RPC, 자원 중심의 표준성과 확장성은 RESTful API를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cursor-based Pagination**: Offset 기반 페이징의 성능 저하와 데이터 중복을 방지하기 위해 마지막 레코드 식별자(ID)를 기준으로 페이징하는 고성능 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 컬렉션 전체 조회 시 DB 메모리 고갈 및 타임아웃 | **`limit`과 `cursor` 기반의 Cursor Pagination 필수 적용** | 대용량 데이터 초고속 페이징 보장 |
| 동시 수정 요청 시 타 사용자의 최신 변경사항 덮어쓰기 발생 | **`ETag` 헤더 및 낙관적 락(`If-Match: 412 Precondition Failed`)** | 데이터 갱신 정합성 100% 보장 |
| API 필드 스키마 변경 시 기존 모바일 클라이언트 비정상 종료 | **URI 버저닝(`/v1/users`, `/v2/users`) 및 구버전 Deprecation 공지** | 무중단 API 하위 호환성 유지 |
| 잘못된 HTTP 상태 코드(모든 에러를 200에 에러메시지 반환) | **표준 HTTP 상태 코드(400, 401, 403, 404, 500) 엄격 매핑** | 클라이언트 에러 핸들링 일관성 확립 |

#### 한줄 요약
- 커서 페이징, ETag 낙관적 락, URI 버저닝, 표준 상태 코드로 API를 설계한다.

## Ⅶ. 결론

- 웹의 확장성과 유지보수성을 극대화하기 위해 **명사형 자원 URI와 표준 HTTP 메서드(RMM Level 2+)를 엄격히 준수하고, Cursor 기반 페이징과 ETag 동시성 제어 및 OpenAPI 3.0 명세화를 결합**하여 엔터프라이즈 RESTful API 표준 완성

#### 한줄 요약
- RESTful API 설계는 명사형 URI, HTTP 표준 메서드, 무상태성, 자기 서술적 메시지를 통해 클라이언트와 서버의 독립적 진화와 웹 캐싱을 극대화하는 핵심 아키텍처 원칙이다.