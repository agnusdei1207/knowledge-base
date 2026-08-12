---
sidebar:
  order: 171
  label: "171. RESTful API 설계 원칙 (RESTful API Design)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "RESTful API 설계 원칙 (RESTful API Design)"
date: "2026-08-10T10:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **REST (Representational State Transfer)**: 로이 필딩(Roy Fielding)이 창안한 웹(Web)의 장점을 최대한 활용할 수 있는 네트워크 아키텍처 스타일로, 자원 중심의 URI와 HTTP 표준 메서드를 결합한 통신 구조.
- **RESTful API**: REST의 기본 원칙 6가지(Uniform Interface, Stateless, Cacheable, Client-Server, Layered System, Code on Demand)를 엄격히 준수하여 설계된 시스템 간 API 연계 규격.
- **Resource (자원)**: `/users/123` 처럼 소프트웨어가 관리하는 모든 엔터티(명사)로, 행위(동사)가 아니라 자원 그 자체를 고유한 주소(URI)로 식별하는 객체.

</details>

- 정의/개념: HTTP 프로토콜의 인프라(URI, Method, Header, Status Code)를 그대로 재사용하여 자원(Resource)의 상태(State)를 주고받는(Transfer) 자원 지향형 통신 아키텍처 규칙인 **RESTful API**
- 배경/필요성: 특정 프로토콜(SOAP)이나 클라이언트(웹, 모바일)에 종속되지 않고, 독립적이고 유연하게 확장 가능한 범용 인터페이스 설계의 요구성

#### 한줄 요약

- 주문이라는 대상에 주소를 붙이고 조회·생성·변경·삭제를 공통 HTTP 의미로 표현하면 새 클라이언트도 같은 규칙으로 결과를 예측할 수 있다.

## Ⅱ. 특징 (REST 아키텍처 4대 제약 조건)

<details><summary>핵심 용어</summary>

- **Uniform Interface (균일한 인터페이스)**: 클라이언트 플랫폼(Android, iOS, Web)과 무관하게, URI로 지정한 리소스에 대해 동일한 표준 조작 방식(GET, POST, PUT, DELETE)을 보장하는 특성.
- **Stateless (무상태성)**: 서버가 클라이언트의 이전 상태(세션)를 기억하지 않고, 각 요청은 독립적으로 완전한 문맥(Token 등)을 포함해야 하는 서버 확장성 보장 특성.

</details>

- **Resource Identification in Requests (URI를 통한 명확한 자원 식별)**
- **Manipulation of Resources through Representations (JSON/XML 표현을 통한 자원 조작)**
- **Self-descriptive Messages (HTTP 헤더와 Content-Type을 통한 자기 서술성)**
- **HATEOAS (Hypermedia As The Engine Of Application State - 하이퍼링크 기반 상태 전이)**

#### 한줄 요약

- `/createOrder`처럼 동작마다 새 규칙을 만들지 않고 `/orders` 자원과 POST를 조합해 주소와 행위의 뜻을 API 전체에서 유지한다.

## Ⅲ. 구조 및 구성요소 (RESTful 리소스 모델링 구조)

<details><summary>핵심 용어</summary>

- **Representation (표현)**: 자원의 실제 데이터 포맷. 동일한 자원(`/users/1`)이라도 클라이언트의 요청(Accept Header)에 따라 JSON, XML, HTML 등 다양한 형태(표현)로 응답할 수 있는 유연성.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   RESTful API Resource & Method Matrix                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Resource (URI)      | 2. GET (조회) | 3. POST (생성) | 4. DELETE (삭제) │
│ ───────────────────────┼───────────────┼────────────────┼────────────────│
│ /customers             | 고객 목록 조회| 새 고객 생성   | 전체 고객 삭제 │
│ /customers/12          | 12번 고객 조회| (오류: 405)    | 12번 고객 삭제 │
│ /customers/12/orders   | 12번 주문 목록| 12번 새 주문   | 12번 주문 삭제 │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 컬렉션(`/customers`)과 도큐먼트(`/customers/12`)로 계층화된 명사형 자원에 HTTP 표준 메서드가 교차 적용되어 시스템의 CRUD 연산을 완벽하게 맵핑하는 행렬 구조.

| 구성요소 | 역할 및 설계 원칙 | 실무 적용 예시 |
|:---|:---|:---|
| **URI (자원 식별자)** | **동사(Action)를 배제하고 명사(Noun) 사용 (복수형 권장)** | `/getUsers` (X) $\rightarrow$ `/users` (O) |
| **HTTP Method (행위)** | **CRUD 비즈니스 로직을 HTTP 메서드에 위임** | GET(조회), POST(생성), PUT(수정) |
| **HTTP Status Code** | **결과의 성공/실패 여부를 표준 코드로 명시** | 200(OK), 201(생성), 404(없음) |
| **HTTP Header** | **인증 토큰, 캐시 제어, 페이로드 타입(MIME) 지정**| `Content-Type: application/json` |

#### 한줄 요약

- 자원 모델이 상품 목록을 정하고 HTTP 인터페이스가 공통 조작법을 제공하며 조건부 요청은 같은 상품을 동시에 고칠 때 덮어쓰기를 막는다.

## Ⅳ. 흐름도 (HATEOAS 기반 REST 상태 전이 흐름)

<details><summary>핵심 용어</summary>

- **HATEOAS (Hypermedia As The Engine Of Application State)**: 서버가 응답 데이터뿐만 아니라, "다음에 클라이언트가 수행할 수 있는 관련 API 링크(Hyperlink)"들을 함께 반환하는 REST의 최종 성숙도(Level 3) 단계.

</details>

```text
[Client] ──► (GET /accounts/1234) ──► [REST API Server]
                                             │
                                             ▼
                                      (Fetch Account & Links)
                                             │
         ◄── (HTTP 200 OK + JSON Response) ──┘
{
  "account_id": "1234",
  "balance": 5000,
  "_links": {
    "self":     { "href": "/accounts/1234" },
    "deposit":  { "href": "/accounts/1234/deposit" },
    "withdraw": { "href": "/accounts/1234/withdraw" }
  }
}
```

### 동작 원리

1. **Request**: 클라이언트가 1234번 계좌의 조회를 요청 (상태 부재, Token 포함).
2. **Process**: 서버가 계좌 상태(5000원)와 현재 상태에서 가능한 행위(입금, 출금 링크)를 조합(HATEOAS).
3. **Transition**: 클라이언트는 하드코딩된 API 주소 대신, 서버가 준 `withdraw` 링크를 동적으로 클릭(POST)하여 다음 상태로 전이 (**REST 아키텍처 완결**).

#### 한줄 요약

- 클라이언트가 알고 있던 엔터티 태그를 함께 보내면 서버는 현재 버전과 같을 때만 수정해 다른 사용자의 최신 변경을 덮지 않는다.

## Ⅴ. 종류 및 비교 (Richardson의 REST 성숙도 모델 비교)

<details><summary>핵심 용어</summary>

- **Richardson Maturity Model (리처드슨 성숙도 모델)**: API가 진정한 RESTful에 얼마나 가까운지 평가하는 4단계 척도로, 실무에서는 통상 Level 2를 RESTful로 인정하는 기준.

</details>

| 성숙도 레벨 | 설계 수준 및 특징 | 매핑되는 기술 성향 |
|:---|:---|:---|
| **Level 0 (The Swamp)** | 단일 URI(`/api`), 단일 메서드(`POST`)만 사용하여 원격 함수 호출 | 전통적인 SOAP 기반 RPC |
| **Level 1 (Resources)** | URI를 통해 각각의 자원(`/users`, `/orders`) 분리 식별 | 자원(명사) 중심 분산 설계 |
| **Level 2 (HTTP Verbs)** | 자원에 HTTP 메서드(GET/POST/PUT/DELETE)와 상태 코드 매핑 | **실무적 표준 RESTful API** |
| **Level 3 (HATEOAS)** | 응답 내부에 상태 전이를 위한 링크(Hypermedia) 포함 | **이론적 완벽한 RESTful API** |

#### 한줄 요약

- RPC는 `approveOrder` 같은 업무 명령을 직접 부르고 REST는 주문 자원의 상태 표현을 공통 HTTP 규칙으로 바꾼다.

## Ⅵ. 실무 고려사항 및 대책 (REST API 실무 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **Over-fetching & Under-fetching**: REST의 고정된 응답 구조 탓에 클라이언트가 불필요한 데이터를 너무 많이 받거나(Over), 한 번에 못 받아 API를 여러 번 쪼개서 호출(Under)해야 하는 고질적 성능 저하 요인.

</details>

| 3대 REST 설계 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 컬렉션 대량 조회 병목**| `GET /users` 호출 시 수만 건 데이터 폭주 | **Pagination (Offset/Cursor 기반 페이징) 강제** |
| **2. 복잡한 다중 필터링** | URI 경로만으로 검색 조건 표현 한계 | **Query String 파라미터 활용 (`?status=A&sort=desc`)**|
| **3. API 버전 단절** | V1 백엔드 수정 시 구버전 모바일 앱 크래시 | **URI 버저닝 강제 (`/v1/users`, `/v2/users`)** |

> 사례: **카카오 / 네이버 오픈 API의 URI 버전 관리 및 Offset Pagination에서 Cursor Pagination으로의 최적화**

#### 한줄 요약

- 결제 생성 요청이 시간 초과로 다시 도착해도 같은 멱등성 키의 기존 결과를 반환하면 실제 결제는 한 번만 남는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **RESTful 수립 기준**: 리처드슨 Level 2 이상(명사형 URI, HTTP 메서드/상태코드), Stateless 기반 토큰 인증 및 Pagination에 의거한 체계.

</details>

- **RESTful 수립 기준**에 따라 MSA 및 프론트엔드 연동 설계 시 **자원 식별 URI & 무상태 제약(Stateless)** 필수 적용

#### 한줄 요약

- 자원 주소와 HTTP 의미를 일관되게 적용하고 생성에는 멱등성 키, 수정에는 엔터티 태그를 사용해 재전송과 동시 변경을 안전하게 처리해야 한다.
