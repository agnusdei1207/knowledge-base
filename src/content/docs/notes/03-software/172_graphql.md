---
sidebar:
  order: 172
  label: "172. GraphQL (GraphQL)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "GraphQL (GraphQL)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 172
extra:
  question_no: "172"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "스키마•질의 비용•필드 권한의 비교 가치"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **GraphQL**: 페이스북이 개발한 쿼리 언어로, 클라이언트가 서버에 존재하는 데이터의 형태(Schema)를 바탕으로 정확히 자신이 필요한 필드만 선별하여 단일 엔드포인트(`/graphql`)로 요청하고 응답받는 API 기술.
- **Over-fetching & Under-fetching**: REST API의 고정된 응답 구조 때문에 클라이언트가 불필요한 필드까지 통째로 받거나(Over), 한 번에 다 받지 못해 여러 번 API를 호출해야 하는(Under) 현상. GraphQL은 이를 완벽히 해결함.
- **Schema & Type System**: 서버가 제공할 수 있는 데이터의 종류와 관계를 강타입(Strong Type) 시스템으로 미리 명세해 둔 청사진. 클라이언트 쿼리의 유효성 검사 기준.

</details>

- 정의/개념: 클라이언트 주도형 데이터 질의 언어(Query Language)이자, 단일 엔드포인트에서 타입 스키마(Type Schema)를 통해 선언적 데이터 패칭(Fetching)을 수행하는 런타임 환경인 **GraphQL**
- 배경/필요성: REST API의 고정 응답(Fixed-Response) 방식으로 인해 모바일, 웹, 스마트워치 등 다양한 클라이언트의 개별적 데이터 요구량을 충족시키기 어렵고 N+1 네트워크 호출 낭비가 심해지는 한계성 극복

#### 한줄 요약

- 정해진 메뉴에서 화면에 필요한 항목과 하위 항목만 골라 한 요청으로 받되 서버는 주문 가능한 깊이와 양을 제한한다.

## Ⅱ. 특징 (GraphQL 3대 핵심 메커니즘)

<details><summary>핵심 용어</summary>

- **Declarative Data Fetching (선언적 데이터 패칭)**: 클라이언트가 "어떻게(How)" 가져올지가 아니라, "무엇(What)"이 필요한지만 JSON과 유사한 형태의 쿼리로 선언하면 서버가 알아서 조합해 주는 방식.

</details>

- **Single Endpoint (모든 요청을 단일 주소인 POST `/graphql`로 처리)**
- **Client-Specified Queries (클라이언트가 필요한 필드와 Depth를 직접 선택 조합)**
- **Strongly Typed Schema (서버-클라이언트 간 명확한 데이터 타입 계약 보장)**

#### 한줄 요약

- 스키마가 주문 가능한 필드와 타입을 정하고 클라이언트가 응답 모양을 고르면 리졸버가 여러 데이터 원천의 결과를 조립한다.

## Ⅲ. 구조 및 구성요소 (GraphQL 쿼리 및 스키마 구조)

<details><summary>핵심 용어</summary>

- **Resolver (리졸버)**: 클라이언트가 요청한 쿼리의 각 필드(Field)가 실제로 DB나 백엔드 서비스의 어디에서 데이터를 가져와야 하는지 매핑해 주는 핵심 실행 함수.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   GraphQL Client-Server Interaction                    │
├────────────────────────────────────────────────────────────────────────┤
│ [Client Query]                     [Server Response]                   │
│ query {                            {                                   │
│   user(id: "123") {                  "data": {                         │
│     name                               "user": {                       │
│     email                                "name": "Kim",                │
│     posts {                              "email": "kim@a.com",         │
│       title                              "posts": [                    │
│     }                                      { "title": "Hello GraphQL" }│
│   }                                      ]                             │
│ }                                      }                               │
│                                      }                                 │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 클라이언트가 원하는 데이터의 트리 모양(Query)을 정의하여 요청하면, 서버가 정확히 그 형태와 일치하는 JSON(Response)을 반환하는 구조.

| 구성요소 | 역할 및 정의 | 구현 예시 |
|:---|:---|:---|
| **Query** | **REST의 GET 역할로 데이터 조회를 요청하는 구문**| `query { user { name } }` |
| **Mutation** | **REST의 POST/PUT/DELETE 역할로 데이터 변경 요청**| `mutation { addUser(name: "A") }` |
| **Schema** | **API가 제공하는 데이터의 타입 구조 명세서** | `type User { id: ID! name: String }`|
| **Resolver** | **스키마의 각 필드 데이터를 실제로 가져오는 함수**| `User.name: (parent) => DB.getName()` |

#### 한줄 요약

- 스키마가 메뉴, 검증기가 주문 제한, 실행 엔진이 조리 순서, 리졸버가 각 주방의 결과를 가져오는 담당자 역할을 한다.

## Ⅳ. 흐름도 (GraphQL 요청 파싱 및 리졸빙 흐름)

<details><summary>핵심 용어</summary>

- **AST (Abstract Syntax Tree, 추상 구문 트리)**: 서버가 클라이언트의 문자열 쿼리를 수신한 후, 구문 분석(Parsing)을 통해 내부적으로 이해하고 실행할 수 있도록 변환한 트리 형태의 데이터 구조.

</details>

```text
[Client] ──(Query Request)──► [GraphQL Server Endpoint (/graphql)]
                                       │
                                       ▼
1. [Parsing & Validation] ◄──(Compare)── [Type Schema] (문법 및 타입 유효성 검증)
                                       │
                                       ▼
2. [Execution (Resolving)] ──► [Resolver 1 (User 조회)] ──► DB 1
                               │
                               └─► [Resolver 2 (Post 조회)] ──► API 2
                                       │
                                       ▼
3. [Format & Response] ◄──(Merge Results into JSON)── [Client]
```

### 동작 원리

1. **Validation**: 서버가 요청 쿼리를 AST로 파싱하고 사전에 정의된 Schema와 대조하여 유효성(타입 일치 여부) 검증.
2. **Execution**: 각 필드에 매핑된 Resolver 함수들을 재귀적으로 호출하여 실제 데이터를 Fetching (이때 병렬 또는 직렬로 다양한 Data Source에 접근).
3. **Response**: 수집된 데이터를 클라이언트가 요청한 트리 구조와 동일한 형태의 JSON으로 조립하여 HTTP 200 응답 반환 (**GraphQL 파이프라인 완결**).

#### 한줄 요약

- 상품 목록과 각 판매자를 요청하면 데이터 로더가 판매자 키를 한 번에 모아 조회해 상품 수만큼 같은 저장소를 호출하는 문제를 줄인다.

## Ⅴ. 종류 및 비교 (REST API 대 GraphQL 1:1 비교)

<details><summary>핵심 용어</summary>

- **API Gateway vs GraphQL Federation**: 다수의 마이크로서비스를 묶을 때, REST는 API Gateway가 라우팅만 하지만, GraphQL은 Apollo Federation을 통해 여러 서브그래프(Sub-graph)를 1개의 슈퍼그래프(Super-graph)로 결합하여 클라이언트에게 제공.

</details>

| 비교 항목 | REST API | GraphQL |
|:---|:---|:---|
| **엔드포인트** | **URI 자원별 다수 생성 (`/users`, `/posts`)**| **단일 엔드포인트 (`/graphql`)** |
| **데이터 페칭**| 서버가 정해둔 고정된 구조로 응답받음 (Over/Under-fetching) | **클라이언트가 필요한 필드만 유연하게 선택**|
| **HTTP 메서드**| 리소스 조작을 위해 GET/POST/PUT/DELETE 활용 | **모든 요청(조회, 변경)을 POST로 전송**|
| **버저닝(Versioning)**| `/v1/users`, `/v2/users` 처럼 API 버전 분리 관리| **Deprecated 어노테이션으로 스키마 단일 진화 유지**|

#### 한줄 요약

- 화면마다 연관 데이터 모양이 크게 다르면 GraphQL이 호출을 줄이고 자원 단위 캐시와 단순 공개 연계가 중요하면 REST가 운영하기 쉽다.

## Ⅵ. 실무 고려사항 및 대책 (GraphQL 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

- **N+1 Problem**: 리졸버가 부모 데이터 1건을 조회한 후, 자식 데이터 N건을 가져오기 위해 쿼리를 N번 더 날리게 되어 데이터베이스 성능이 붕괴되는 GraphQL의 대표적 난제.

</details>

| 3대 GraphQL 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. N+1 문제** | 계층형 리졸버가 부모/자식 각각 순차 쿼리 | **DataLoader 패턴 도입(ID를 모아 In Query로 배치/캐싱 처리)**|
| **2. 악의적 쿼리 공격**| 무한 Depth 쿼리로 서버 메모리 고갈 공격 | **Query Depth Limit 제한 및 Query Cost(가중치) 상한선 설정**|
| **3. HTTP 캐싱 불가** | 모든 쿼리가 POST 단일 엔드포인트로 전송됨| **Persisted Query(쿼리 해시화 GET 전송) 및 Apollo Client In-memory Cache 사용**|

> 사례: **GitHub / Airbnb 마이크로서비스 연동 시 Apollo GraphQL 기반 Federation(슈퍼그래프) 아키텍처 적용**

#### 한줄 요약

- 사용자가 상품 객체를 볼 권한이 있어도 원가 필드를 볼 권한은 별도일 수 있으므로 리졸버마다 필드 수준 권한을 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **GraphQL 수립 기준**: 스키마(Schema) 타입 선언, 선언적 데이터 페칭 설계, N+1 쿼리 최적화(DataLoader) 및 쿼리 복잡도 통제에 의거한 체계.

</details>

- **GraphQL 수립 기준**에 따라 프론트엔드 다변화 및 MSA 데이터 애그리게이션 시 **단일 스키마 기반 필드 선택적 페칭** 필수 적용

#### 한줄 요약

- 선택형 응답의 호출 절감이 크고 스키마·비용·권한을 지속 관리할 수 있을 때 그래프 질의 언어를 적용해야 한다.
