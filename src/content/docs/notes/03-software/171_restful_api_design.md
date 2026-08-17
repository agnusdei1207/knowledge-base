---
sidebar:
  order: 171
  label: "171. RESTful API 설계 원칙 (RESTful API Design)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "RESTful API 설계 원칙 (RESTful API Design)"
date: "2026-08-18T03:00:00+09:00"
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

- **RESTful API 설계 원칙(Roy Fielding)**: 명사형 URI로 자원(Resource)을 식별하고, HTTP 표준 메서드(GET, POST, PUT, DELETE)와 상태 코드를 활용하여 무상태(Stateless)로 통신하는 웹 아키텍처 원칙.
- **동사형 RPC 남발 및 캐싱 한계(Action-Centric Bottleneck)**: `/getUser`, `/deleteUser` 등 동작 중심의 임의 엔드포인트 남발로 인한 API 직관성 저하와 HTTP 표준 캐싱 활용 불가 위험.

</details>

- 정의/개념: 웹 표준 HTTP 프로토콜을 활용하여 **명사형 URI로 자원을 식별하고 표준 메서드로 상태를 조작**하는 RESTful 아키텍처 설계 원칙
- 배경/필요성: RPC 스타일의 동사형 엔드포인트 남발로 인한 **API 발견성 저하, HTTP 캐싱 불가 및 클라이언트-서버 간 결합도 심화 위험** 직면

#### 한줄 요약

- 명사형 자원 식별과 HTTP 표준 메서드(CRUD) 및 무상태성을 준수하여 확장성과 독립성을 갖춘 API를 설계

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **균일한 인터페이스(Uniform Interface 4원칙)**: 자원 식별(URI), 표현을 통한 조작(JSON), 자기 서술적 메시지(Self-descriptive), 애플리케이션 상태 엔진으로서의 하이퍼미디어(HATEOAS).
- **무상태성(Statelessness)**: 서버가 클라이언트의 세션 상태를 저장하지 않고 모든 요청이 인증 토큰을 포함하여 독립 완결적으로 처리되는 성질.

</details>

- 행위가 아닌 자원(Resource) 자체를 명사형 복수형(`/users`, `/orders`)으로 식별하는 **URI 설계**
- 조회(GET), 생성(POST), 전체 교체(PUT), 일부 수정(PATCH), 삭제(DELETE)의 **HTTP 메서드 표준 매핑**
- 200(OK), 201(Created), 400(Bad Request), 404(Not Found) 등 **표준 HTTP 상태 코드 반환**

#### 한줄 요약

- 자원 식별, 표준 메서드 매핑, 무상태 통신을 통해 클라이언트와 서버의 완벽한 분리와 캐싱 성능을 확보

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RESTful API 4대 설계 요소**: 자원(URI), 행위(HTTP Method), 표현(Representation JSON/XML), 상태 코드(HTTP Status).

</details>

```text
[ RESTful API 표준 계층 아키텍처 및 자원 조작 구조 ]

 1. [ 자원 식별 계층 (URI Resource) ]
    • 명사형 복수 계층: `/api/v1/users/{userId}/orders/{orderId}`
                           │
                           ▼
 2. [ 표준 행위 계층 (HTTP Methods) ]
    • GET (조회: 안전/멱등)  • POST (생성: 비멱등)  • PUT (교체: 멱등)
    • PATCH (부분수정)       • DELETE (삭제: 멱등)
                           │
                           ▼
 3. [ 표현 및 메타데이터 계층 (Representation & Headers) ]
    • Headers: `Content-Type: application/json`, `If-Match: "eTag123"`
    • Body:    { "orderId": 100, "amount": 50000, "status": "PAID" }
                           │
                           ▼
 4. [ 표준 결과 응답 계층 (HTTP Status Codes) ]
    • 200 OK / 201 Created / 400 Bad Request / 404 Not Found / 500 Internal
```

선의 의미: 명사형 URI로 자원을 특정하고 HTTP 메서드로 조작하여 표준 상태 코드와 JSON 표현을 반환하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 자원 식별자 (URI) | 행위(동사)를 배제하고 **명사형 복수형 계층 구조로 비즈니스 엔터티 식별** |
| HTTP 메서드 (Verbs) | CRUD 행위를 **표준 HTTP 메서드(GET/POST/PUT/PATCH/DELETE)로 일관 매핑** |
| HTTP 상태 코드 | 처리 결과를 **2xx(성공), 4xx(클라이언트 오류), 5xx(서버 오류)로 명확히 전달** |
| HTTP 헤더 및 표현 | Content-Type, Accept, Cache-Control, **ETag 등을 통해 메타데이터와 캐싱 제어** |

#### 한줄 요약

- URI(자원), HTTP Method(행위), Representation(표현), Status Code(결과)가 결합

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RESTful 요청 처리 5단계 파이프라인**: URI 자원 식별 $\to$ 메서드 인가 검증 $\to$ 조건부 ETag 검사 $\to$ 비즈니스 처리 $\to$ HATEOAS 응답 구성.

</details>

```text
[ RESTful API 요청 수신 및 상태 전이 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. HTTP Request 수신 및 URI 자원 식별 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. HTTP Method 의미 및 Bearer 토큰 검증│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 조건부 요청(ETag / If-Match) 동시성 검사
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 도메인 로직 수행 및 JSON 표현 생성 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. HTTP 상태 코드 및 HATEOAS 링크 응답│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 자원 식별: 요청된 URI(`/orders/101`)를 파싱하여 특정 주문 자원을 식별.
2. 메서드 검증: `PUT` 메서드의 유효성과 JWT Bearer 토큰의 접근 권한을 확인.
3. 조건부 검사: `If-Match: "v1.0"` 헤더의 ETag를 비교하여 타 사용자의 동시 수정 덮어쓰기(Lost Update)를 방지.
4. 표현 생성: 비즈니스 로직을 수행하고 주문 엔터티의 현재 상태를 JSON 객체로 직렬화.
5. 응답 회신: HTTP `200 OK` 상태 코드와 함께 다음 상태 전이 링크(`_links: { "cancel": "/orders/101/cancel" }`)를 반환.

#### 한줄 요약

- 자원 식별 $\to$ 메서드 검증 $\to$ 조건부 ETag 검사 $\to$ 로직 수행 $\to$ HATEOAS 회신의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RPC 스타일 vs RESTful 스타일**: 행위 함수 호출 방식(RPC)과 자원 상태 조작 방식(RESTful).

</details>

| 구분 | RPC 스타일 API (원격 프로시저 호출) | RESTful API 스타일 (자원 중심) |
|:---|:---|:---|
| **적용 기준** | 단일 작업 수행, 복잡한 다단계 프로세스 배치 실행 | 대고객 CRUD 서비스, 모바일/웹 표준 API, 오픈 API |
| **핵심 특징** | **`/createUser`, `/deleteUser` 등 동사형 엔드포인트** | **`/users` 명사형 URI + HTTP Method (POST/DELETE)** |
| **한계** | 엔드포인트 남발로 인한 API 파편화 및 HTTP 캐싱 불가 | 순수 CRUD로 표현하기 힘든 복잡한 트랜잭션 모델링 난이도 |

#### 한줄 요약

- 단순 프로시저 호출은 RPC, 자원 중심의 표준성과 확장성은 RESTful API를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **커서 기반 페이징(Cursor-based Pagination)**: 대규모 데이터 조회 시 Offset 방식의 성능 저하와 데이터 중복을 방지하기 위해 마지막 조회 ID를 기준으로 조회하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 컬렉션 전체 조회 시 DB 메모리 고갈 및 타임아웃 | **`limit`과 `cursor` 기반의 Cursor Pagination 필수 적용** | 대용량 데이터 초고속 페이징 보장 |
| 동시 수정 요청 시 타 사용자의 최신 변경사항 덮어쓰기 발생 | **`ETag` 헤더 및 낙관적 락(`If-Match: 412 Precondition Failed`)** | 데이터 갱신 정합성 100% 보장 |
| API 필드 스키마 변경 시 기존 모바일 클라이언트 비정상 종료 | **URI 버저닝(`/v1/users`, `/v2/users`) 및 구버전 Deprecation 공지** | 무중단 API 하위 호환성 유지 |

#### 한줄 요약

- 커서 페이징, ETag 낙관적 락, URI 버저닝을 통해 실무 RESTful API의 성능과 안정성을 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **OpenAPI / Swagger 표준 명세**: RESTful API의 명세와 테스트를 코드 수준에서 자동화하는 인터페이스 표준.

</details>

- **RESTful API 설계 원칙**은 웹의 확장성과 단순성을 극대화하는 소프트웨어 아키텍처의 기본 규약이며, 리처드슨 성숙도 모델(Level 2+)을 준수하고 커서 페이징과 ETag 동시성 제어를 결합하여 고품질의 API를 구축해야 함

#### 한줄 요약

- 명사형 URI와 HTTP 표준 메서드 및 무상태 설계를 통해 확장성과 호환성이 뛰어난 API를 완성
