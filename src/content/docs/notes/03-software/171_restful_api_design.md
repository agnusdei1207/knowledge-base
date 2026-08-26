---
sidebar:
  order: 171
  label: "171. RESTful API 설계 원칙"
  badge:
    text: "기출 · 70%"
    variant: note
title: "RESTful API 설계 원칙 (RESTful API Design)"
date: "2026-08-26T13:14:50+09:00"
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

- 정의/개념: 웹 표준 HTTP 프로토콜 위에서 **명사형 URI로 자원을 식별하고 표준 메서드·상태 코드로 무상태 조작하는 API 아키텍처 원칙**
- 배경/필요성: RPC 방식의 동사형 URI와 단일 POST 사용으로 인한 **행위·자원 혼재, HTTP 캐싱 불가 및 클라이언트-서버 간 강결합 해소 불가**

#### 한줄 요약
- 명사형 URI, 표준 HTTP 메서드, 무상태 통신을 통해 클라이언트와 서버의 독립적 진화를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Uniform Interface**: 자원 식별(URI), 표현을 통한 조작(JSON), 자기 서술적 메시지(Self-descriptive), HATEOAS 4대 원칙.
- **Idempotency**: 동일한 요청을 여러 번 수행해도 서버의 상태가 단 한 번 요청했을 때와 동일하게 유지되는 성질(GET, PUT, DELETE).

</details>

- 자원 식별, 표현 조작, 자기 서술적 메시지를 제공하는 **Uniform Interface 4대 원칙 준수**
- GET·PUT·DELETE 재시도 결과를 정의하는 **멱등성**
- 명사형 URI와 HTTP 의미론 기반 **자원 인터페이스**

#### 한줄 요약
- 자원 인터페이스와 무상태 통신으로 결합도를 낮추고 캐싱을 지원한다.
## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **RESTful API 4대 설계 계층**: Resource URI(자원 식별), HTTP Methods(행위 정의), Representation/Headers(표현/메타데이터), Status Codes(결과 통지).

</details>

```text
[RESTful API 표준 계층 아키텍처 및 자원 조작 구조]
|-- Resource Identification Layer
|-- Standard HTTP Methods Layer
|   |-- GET (조회: Safe & Idempotent) / POST (생성: Non-Idempotent)
|   `-- PUT (전체교체: Idempotent) / PATCH (부분수정) / DELETE (삭제: Idempotent)
|-- Representation & Headers Layer
    |-- Headers: `Content-Type: application/json`, `If-Match: "eTag123"`, `Cache-Control`
    `-- Body: JSON Representation (`{ "orderId": 100, "status": "PAID" }`)
`-- Standard Response Status Layer
```

선의 의미: 계층 및 명사형 URI로 자원을 특정하고 HTTP 메서드로 조작하여 표준 상태 코드와 JSON 표현을 반환하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 자원 식별자 | 명사형 URI로 **자원 식별** |
| HTTP 메서드 | 자원 조작을 표준 메서드 의미에 매핑 |
| HTTP 상태 코드 | 처리 결과와 오류 범주 전달 |
| HTTP 헤더·표현 | **콘텐츠 형식·캐시·조건부 요청** 제어 |

#### 한줄 요약
- URI(자원), HTTP Method(행위), Representation(표현), Status Code(결과)가 결합된다.
## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RESTful 요청 처리**: 자원 식별, 검증, 조건부 요청, 도메인 로직 수행.

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
   클라이언트에 HTTP `200 OK`와 다음 상태 전이 HATEOAS 링크를 포함한 JSON 응답 반환
```

동작 원리:

1. 자원 식별: URI에서 대상 엔터티 확인
2. 메서드 및 권한 검증: HTTP 의미와 인가 확인
3. 조건부 동시성 검사: ETag로 변경 충돌 검증
4. 도메인 로직 수행: 상태 변경과 표현 생성

#### 한줄 요약
- 자원 식별 → 메서드 검증 → ETag 검사 → 로직 수행 → 상태 코드 회신 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RPC 스타일 vs RESTful 스타일**: 행위 함수 호출 중심(RPC)과 자원 상태 전이 중심(RESTful).

</details>

| 비교 항목 | RPC 스타일 API (원격 프로시저 호출) | RESTful API 스타일 (자원 중심) |
|:---|:---|:---|
| 엔드포인트 설계 | **`/createUser` 등 동사형 URI**| **`/users` 명사형 URI 및 메서드 매핑** |
| 통신 방식 및 메서드| 서비스 계약에 따른 프로시저 호출 | **HTTP 메서드 의미론 활용**|
| HTTP 캐싱 활용 | 전송 규약과 메서드에 의존 | **GET·ETag 캐싱 활용**|
| 최적 적용 대상 | **복잡한 다단계 비즈니스 프로세스, 배치 실행** | **대고객 CRUD 서비스, 웹/모바일 오픈 API**|

#### 한줄 요약
- 단순 프로시저 실행은 RPC, 자원 중심의 표준성과 확장성은 RESTful API를 선택한다.
## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cursor-based Pagination**: Offset 기반 페이징의 성능 저하와 데이터 중복을 방지하기 위해 마지막 레코드 식별자(ID)를 기준으로 페이징하는 고성능 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 컬렉션 조회의 메모리·지연 증가 | 정렬 키에 맞는 **Cursor Pagination** 적용 | 조회 범위와 스캔 비용 제한 |
| 동시 수정의 변경사항 덮어쓰기 | **ETag·If-Match 조건부 요청** 적용 | 오래된 버전의 갱신 거부 |
| API 필드 스키마 변경 시 모바일 클라이언트 오류 | **URI 버저닝(`/v1`) 및 구버전 Deprecation 공지** | 하위 호환성 유지 |
| 모든 에러를 200 상태 코드로 반환하는 비표준 처리 | **표준 HTTP 상태 코드(400, 401, 404, 500) 엄격 매핑** | 에러 핸들링 일관성 확립 |

#### 한줄 요약
- 커서 페이징, ETag 낙관적 락, URI 버저닝, 표준 상태 코드로 API를 설계한다.

## Ⅶ. 결론

- 자원 중심 공개 API는 **REST**, 작업 중심 내부 호출은 **RPC** 선택

#### 한줄 요약
- 공개 자원 계약은 HTTP 의미론과 조건부 요청으로 설계한다.
