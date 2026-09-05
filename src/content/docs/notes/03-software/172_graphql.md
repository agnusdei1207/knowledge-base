---
sidebar:
  order: 172
  label: "172. GraphQL"
  badge:
    text: "미출 · 50%"
    variant: note
title: "GraphQL (GraphQL)"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: 클라이언트가 필요한 데이터 구조를 선언하여 단일 엔드포인트에서 강타입 스키마 기반으로 필요한 필드만 조립 반환하는 API 쿼리 언어 및 런타임
- 배경/필요성: 전통적 REST API 사용 시 발생하는 불필요한 필드 과다 수신(Over-fetching)과 다중 엔드포인트 연속 호출에 따른 다중 왕복 지연(Under-fetching) 한계

#### 한줄 요약
- 선언적 필드 선택으로 과다 조회와 다중 호출을 줄인다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Schema & Type System**: 서버가 제공 가능한 데이터의 타입과 관계를 정의하는 엄격한 타입 계약(Schema Definition Language).
- **DataLoader**: 계층형 리졸버의 N+1 쿼리 문제를 해결하기 위해 요청 키를 모아 배치(Batching) 및 캐싱(Caching) 처리하는 유틸리티.

</details>

- 단일 논리 엔드포인트를 사용하는 Single Endpoint
- 클라이언트가 필요한 필드와 중첩 깊이를 직접 지정하는 선언적 데이터 패칭(Declarative Fetching)
- 스키마 기반 타입 시스템과 `@deprecated`를 활용한 무버전 점진적 진화(Versionless)

#### 한줄 요약
- 단일 엔드포인트와 필드 선택으로 전송량을 줄인 대가로, URL 단위로 성립하던 표준 HTTP 캐싱과 요청당 비용 예측 가능성을 함께 잃는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **GraphQL 4대 핵심 구성요소**: Schema(타입 정의), Query/Mutation(읽기/쓰기 연산), Resolver(데이터 조회 함수), DataLoader(배치 최적화).

</details>

```text
[GraphQL 엔진 아키텍처 및 리졸버 실행 구조]
|-- Client Request Layer
|   `-- `query { user(id: 1) { name, posts { title, comments { text } } } }`
`-- GraphQL Engine Core Layer
    |-- Schema Definition (Type, Field, Query, Mutation 계약 명세)
    |-- Parser & Validator (AST 구문 변환, 쿼리 Depth 및 비용 검증)
    `-- Execution Engine (필드별 계층형 Resolver 실행 트리 조립)
        |-- DataLoader Batching Layer
        `-- Multi-Data Source Layer
```

선의 의미: 계층 및 클라이언트의 선언적 쿼리를 엔진이 파싱하여 DataLoader를 거쳐 다중 데이터 소스에서 필드를 조립 반환하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 스키마 | Type·Field·Argument의 API 계약 선언 |
| Query·Mutation | 조회 필드와 변경 입력 선언 |
| 리졸버 | 필드를 데이터 소스 호출에 연결 |
| DataLoader | 요청 범위의 키를 배치·캐시해 N+1 완화 |

#### 한줄 요약
- 스키마가 계약을, 리졸버가 데이터 소스 연결을 맡고 그 사이에서 DataLoader가 중복 조회를 묶으므로, 클라이언트 질의의 자유가 곧바로 백엔드 호출 폭증으로 번지지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **GraphQL 실행**: 파싱, 검증, 실행 계획, 리졸버 배치 수행.

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
   4. [DataLoader 배치 실행] 요청 키를 모아 데이터 소스별 배치 조회
        │
   클라이언트가 요구한 Selection Set JSON 구조로 데이터를 조립하여 단일 응답 회신
```

동작 원리:

1. 쿼리 파싱: 요청을 AST로 변환
2. 스키마 및 비용 검증: 타입·깊이·비용 확인
3. 실행 계획 수립: 필드 의존성과 병렬성 결정
4. DataLoader 배치 실행: 요청 키를 묶어 조회

#### 한줄 요약
- 질의 자유도를 클라이언트에 넘긴 대신 비용 검증과 배치 실행을 서버가 떠안으므로, 검증 단계에서 걸러내지 못한 깊은 질의는 실행 단계에서 자원 고갈로 되돌아온다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **REST vs GraphQL**: 다중 엔드포인트/고정 응답(REST)과 단일 엔드포인트/선언적 맞춤 응답(GraphQL).

</details>

| 비교 항목 | REST API | GraphQL |
|:---|:---|:---|
| 엔드포인트 구조 | 자원별 다수 엔드포인트 (`/users`, `/posts`)| 단일 엔드포인트 (`/graphql`) |
| 응답 데이터 형태 | 자원별 표현 계약 | Selection Set 기반 필드 선택 |
| 연관 데이터 조회 | 엔드포인트·포함 옵션에 따라 호출 | 중첩 질의를 단일 요청으로 표현 |
| HTTP 캐싱 활용 | 표준 HTTP GET 메서드 기반 브라우저/CDN 캐싱 용이| POST 단일 요청으로 표준 HTTP 캐싱 활용 난이도 높음 |
| 버전 관리 방식 | `/v1`, `/v2` URI 기반 물리적 버전 분리 | `@deprecated` 어노테이션 기반 단일 스키마 진화|

#### 한줄 요약
- 단순 자원 CRUD와 표준 웹 캐싱은 REST, 복잡한 연관 데이터와 모바일 최적화는 GraphQL을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **N+1 Problem**: 부모 1건 조회 후 자식 N건을 가져오기 위해 리졸버가 쿼리를 N번 연속 실행하여 DB 부하가 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 계층형 리졸버의 N+1 DB 조회 | DataLoader 배치·요청 캐시 적용 | 데이터 소스 호출 수 감소 |
| 깊고 복잡한 쿼리의 자원 고갈 | 깊이·복잡도·시간 제한 적용 | 요청별 자원 사용량 제한 |
| GraphQL 응답의 CDN 캐시 제약 | Persisted Query·클라이언트 캐시 적용 | 캐시 키 안정화와 대역폭 절감 |
| 다수 마이크로서비스 결합 시 스키마 관리 파편화 | Apollo Federation 도입으로 서브그래프를 단일 슈퍼그래프로 통합 | 엔터프라이즈 마이크로서비스 연계 |

#### 한줄 요약
- 네 대책은 클라이언트에 넘긴 질의 자유를 배치·제한·고정 질의로 다시 좁히는 선택이며, Persisted Query는 임의 질의의 유연성을 캐시 가능성과 맞바꾼다.

## Ⅶ. 결론

- 복잡한 연관 데이터를 다루는 대고객 모바일/웹 프론트엔드(BFF 계층) 및 다기종 클라이언트 환경의 핵심 데이터 페칭(Fetching) 표준 플랫폼으로 정립되었으며, 실무 구축 시에는 계층형 리졸버의 N+1 쿼리 폭증을 방어하는 DataLoader 배치/캐싱, 악의적 중첩 질의를 차단하는 Max Depth/Query Complexity 제한, HTTP 캐싱 한계를 극복하는 Persisted Queries(APQ) 적용, MSA 환경의 스키마 통합을 지원하는 Apollo Federation을 결합하여 백엔드 부하를 통제하면서 클라이언트 중심의 최적 UX를 완성

#### 한줄 요약
- GraphQL에는 N+1 완화와 쿼리 비용 제한을 함께 적용한다.
