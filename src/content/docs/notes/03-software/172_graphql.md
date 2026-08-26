---
sidebar:
  order: 172
  label: "172. GraphQL"
  badge:
    text: "미출 · 50%"
    variant: note
title: "GraphQL (GraphQL)"
date: "2026-08-26T10:25:00+09:00"
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

<details><summary>용어 설명</summary>

- **GraphQL**: 클라이언트가 필요한 데이터 구조를 선언적으로 명시하여 단일 엔드포인트(`/graphql`)에서 정확히 필요한 필드만 응답받는 API 쿼리 언어 및 런타임.
- **Over-fetching & Under-fetching**: 불필요한 필드까지 과도하게 수신하는 현상(Over-fetching)과 원하는 데이터를 얻기 위해 여러 엔드포인트를 연속 호출해야 하는 현상(Under-fetching).

</details>

- 정의/개념: 클라이언트가 필요한 데이터 구조를 선언하여 **단일 엔드포인트에서 강타입 스키마 기반으로 필요한 필드만 조립 반환하는 API 쿼리 언어 및 런타임**
- 배경/필요성: REST API의 고정 응답 구조로 인한 **데이터 과다 전송(Over-fetching) 및 다중 호출 왕복 지연(Under-fetching) 해결 불가**

#### 한줄 요약
- 단일 엔드포인트와 선언적 질의를 통해 Over/Under-fetching을 해소하고 네트워크 왕복을 최소화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Schema & Type System**: 서버가 제공 가능한 데이터의 타입과 관계를 정의하는 엄격한 타입 계약(Schema Definition Language).
- **DataLoader**: 계층형 리졸버의 N+1 쿼리 문제를 해결하기 위해 요청 키를 모아 배치(Batching) 및 캐싱(Caching) 처리하는 유틸리티.

</details>

- 모든 요청을 단일 엔드포인트(POST `/graphql`)로 처리하는 **Single Endpoint**
- 클라이언트가 필요한 필드와 중첩 깊이를 직접 지정하는 **선언적 데이터 패칭(Declarative Fetching)**
- 스키마 기반 타입 시스템과 `@deprecated`를 활용한 **무버전 점진적 진화(Versionless)**

#### 한줄 요약
- 단일 엔드포인트, 선언적 데이터 패칭, 강타입 스키마를 통해 모바일/웹 통신 효율을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **GraphQL 4대 핵심 구성요소**: Schema(타입 정의), Query/Mutation(읽기/쓰기 연산), Resolver(데이터 조회 함수), DataLoader(배치 최적화).

</details>

```text
[GraphQL 엔진 아키텍처 및 리졸버 실행 구조]
|-- 1. Client Request Layer: Declarative Query (`POST /graphql`)
|   `-- `query { user(id: 1) { name, posts { title, comments { text } } } }`
`-- 2. GraphQL Engine Core Layer
    |-- Schema Definition (Type, Field, Query, Mutation 계약 명세)
    |-- Parser & Validator (AST 구문 변환, 쿼리 Depth 및 비용 검증)
    `-- Execution Engine (필드별 계층형 Resolver 실행 트리 조립)
        |-- 3. DataLoader Batching Layer (N+1 방지: ID 수집 후 Batch `IN` 쿼리)
        `-- 4. Multi-Data Source Layer (RDBMS, Redis, REST Microservices 연동)
```

선의 의미: 계층 및 클라이언트의 선언적 쿼리를 엔진이 파싱하여 DataLoader를 거쳐 다중 데이터 소스에서 필드를 조립 반환하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 스키마 (Schema) | Type, Field, Argument의 **Query·Mutation 계약 선언** | SDL 명세 체계 |
| 질의 언어 (Query / Mutation)| 클라이언트가 응답받을 **Selection Set 필드 구조 및 변경 파라미터 선언** | 선언적 질의 |
| 리졸버 (Resolver) | 각 필드 요청을 **실제 DB 쿼리, 캐시, 백엔드 마이크로서비스 호출과 연결** | 필드 단위 실행 함수 |
| 데이터로더 (DataLoader) | 반복되는 자식 객체 조회를 **배치(Batching) 및 메모리 캐싱으로 묶어 N+1 해소** | 일괄 `IN` 조회 |

#### 한줄 요약
- 스키마, 쿼리/뮤테이션, 리졸버, 데이터로더가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **GraphQL 실행 5단계**: 쿼리 AST 파싱 $\to$ 스키마/비용 검증 $\to$ 실행 계획 수립 $\to$ DataLoader 리졸버 배치 실행 $\to$ JSON 응답 조립.

</details>

```text
클라이언트의 GraphQL 쿼리 요청 수신
        │
   1. [쿼리 파싱 (Parsing)] 문자열 쿼리를 추상 구문 트리(AST: Abstract Syntax Tree)로 변환
        │
   2. [스키마 및 비용 검증] 스키마 타입 일치 여부와 최대 Depth/Query Cost 상한선 초과 검사
        │
   3. [실행 계획 수립] 필드 간 의존성과 병렬 실행 가능한 리졸버 트리 생성
        │
   4. [DataLoader 배치 실행] DataLoader가 각 사용자/게시글 ID를 모아 단 1번의 `IN` 쿼리로 DB 조회
        │
   클라이언트가 요구한 Selection Set JSON 구조로 데이터를 조립하여 단일 응답 회신
```

#### 한줄 요약
- 쿼리 파싱 → 스키마/비용 검증 → 실행 계획 수립 → DataLoader 배치 실행 → JSON 조립 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **REST vs GraphQL**: 다중 엔드포인트/고정 응답(REST)과 단일 엔드포인트/선언적 맞춤 응답(GraphQL).

</details>

| 비교 항목 | REST API | GraphQL |
|:---|:---|:---|
| 엔드포인트 구조 | **자원별 다수 엔드포인트 (`/users`, `/posts`)**| **단일 엔드포인트 (`/graphql`)** |
| 응답 데이터 형태 | 서버가 정해둔 고정 포맷 (Over/Under-fetching) | **클라이언트가 요청한 필드만 정확히 반환** |
| 네트워크 왕복 횟수 | 연관 데이터 조회를 위해 N번 다중 호출 필요 | **단 1번의 네트워크 왕복(Round-Trip)으로 일괄 수신**|
| HTTP 캐싱 활용 | **표준 HTTP GET 메서드 기반 브라우저/CDN 캐싱 용이**| POST 단일 요청으로 표준 HTTP 캐싱 활용 난이도 높음 |
| 버전 관리 방식 | `/v1`, `/v2` URI 기반 물리적 버전 분리 | **`@deprecated` 어노테이션 기반 단일 스키마 진화**|

#### 한줄 요약
- 단순 자원 CRUD와 표준 웹 캐싱은 REST, 복잡한 연관 데이터와 모바일 최적화는 GraphQL을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **N+1 Problem**: 부모 1건 조회 후 자식 N건을 가져오기 위해 리졸버가 쿼리를 N번 연속 실행하여 DB 부하가 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 계층형 리졸버의 N+1 개별 쿼리로 인한 DB 성능 고갈 | **DataLoader 패턴 도입으로 ID 취합 후 단일 배치 `IN` 쿼리 실행** | DB 쿼리 수 90% 이상 절감 |
| 악의적인 무한 재귀 중첩 쿼리 공격으로 서버 OOM 다운 | **`graphql-depth-limit` 설정 및 쿼리 복잡도(Cost) 상한선 제한** | DoS 악성 쿼리 원천 차단 |
| 단일 POST 요청으로 인한 브라우저/CDN HTTP 캐싱 불가 | **Persisted Queries (쿼리 해시화 GET 전송) 및 Apollo 캐시 적용** | 엣지 CDN 캐싱 및 대역폭 절감 |
| 다수 마이크로서비스 결합 시 스키마 관리 파편화 | **Apollo Federation 도입으로 서브그래프를 단일 슈퍼그래프로 통합** | 엔터프라이즈 마이크로서비스 연계 |

#### 한줄 요약
- DataLoader 도입, Depth Limit 차단, Persisted Queries 캐싱, Apollo Federation으로 운영한다.

## Ⅶ. 결론

- 복잡한 연관 데이터를 다루는 현대 모바일 및 웹 프론트엔드 환경에서 **Over/Under-fetching을 원천 해소하기 위해 GraphQL을 표준 도입**하고, **DataLoader 기반 N+1 최적화와 Query Depth/Cost 보안 정책**을 결합하여 고성능 선언적 데이터 서비스 완성

#### 한줄 요약
- GraphQL은 단일 엔드포인트와 강타입 스키마 기반의 선언적 데이터 패칭을 통해 네트워크 왕복과 데이터 낭비를 최소화하는 현대 프론트엔드 최적화 핵심 API 기술이다.