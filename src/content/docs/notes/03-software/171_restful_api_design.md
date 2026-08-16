---
sidebar:
  order: 171
  label: "171. RESTful API 설계 원칙 (RESTful API Design)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "RESTful API 설계 원칙 (RESTful API Design)"
date: "2026-08-14T03:16:00+09:00"
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

- **REST (Representational State Transfer)**: 로이 필딩(Roy Fielding)이 창안한 웹(Web)의 장점을 최대한 활용할 수 있는 네트워크 아키텍처 스타일로, 자원 중심의 URI와 HTTP 표준 메서드를 결합한 통신 구조.
- **RESTful API**: REST의 기본 원칙 6가지(Uniform Interface, Stateless, Cacheable, Client-Server, Layered System, Code on Demand)를 엄격히 준수하여 설계된 시스템 간 API 연계 규격.
- **Resource (자원)**: `/users/123` 처럼 소프트웨어가 관리하는 모든 엔터티(명사)로, 행위(동사)가 아니라 자원 그 자체를 고유한 주소(URI)로 식별하는 객체.

</details>

- 정의/개념: Resource와 HTTP 의미를 결합한 **RESTful API**
- 배경/필요성: 동작별 임의 Endpoint는 **발견•Cache•Client 호환성** 저하

#### 한줄 요약

- 주문이라는 대상에 주소를 붙이고 조회·생성·변경·삭제를 공통 HTTP 의미로 표현하면 새 클라이언트도 같은 규칙으로 결과를 예측할 수 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Uniform Interface (균일한 인터페이스)**: 클라이언트 플랫폼(Android, iOS, Web)과 무관하게, URI로 지정한 리소스에 대해 동일한 표준 조작 방식(GET, POST, PUT, DELETE)을 보장하는 특성.
- **Stateless (무상태성)**: 서버가 클라이언트의 이전 상태(세션)를 기억하지 않고, 각 요청은 독립적으로 완전한 문맥(Token 등)을 포함해야 하는 서버 확장성 보장 특성.

</details>

- **Resource Identification in Requests (URI를 통한 명확한 자원 식별)**
- **Manipulation of Resources through Representations (JSON/XML 표현을 통한 자원 조작)**
- **Self-descriptive Messages (HTTP 헤더와 Content-Type을 통한 자기 서술성)**
- **HATEOAS (Hypermedia As The Engine Of Application State - 하이퍼링크 기반 상태 전이)**

#### 한줄 요약

- `/createOrder`처럼 동작마다 새 규칙을 만들지 않고 `/orders` 자원과 POST를 조합해 주소와 행위의 뜻을 API 전체에서 유지한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Representation (표현)**: 자원의 실제 데이터 포맷. 동일한 자원(`/users/1`)이라도 클라이언트의 요청(Accept Header)에 따라 JSON, XML, HTML 등 다양한 형태(표현)로 응답할 수 있는 유연성.

</details>

| 구성요소 | 책임 |
|---|---|
| URI | 명사형 계층으로 **Resource 식별** |
| HTTP Method | 조회•생성•교체•삭제의 **표준 의미** 표현 |
| HTTP Status | 처리 결과와 **오류 Class** 전달 |
| HTTP Header | 표현•인증•Cache•조건부 요청 **Metadata** 제공 |

#### 한줄 요약

- 자원 모델이 상품 목록을 정하고 HTTP 인터페이스가 공통 조작법을 제공하며 조건부 요청은 같은 상품을 동시에 고칠 때 덮어쓰기를 막는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HATEOAS (Hypermedia As The Engine Of Application State)**: 서버가 응답 데이터뿐만 아니라, "다음에 클라이언트가 수행할 수 있는 관련 API 링크(Hyperlink)"들을 함께 반환하는 REST의 최종 성숙도(Level 3) 단계.

</details>

```text
[HTTP 요청]
    │
    ▼
1. URI로 Resource 식별
    │
    ▼
2. Method 의미•권한 검증
    │
    ▼
3. 조건부 요청•상태 처리
    │
    ▼
4. Representation 생성
    │
    ▼
5. Status•Header•Link 구성
    │
    ▼
[HTTP 응답]
```

### 동작 원리

1. **URI로 Resource 식별**: Collection•Document 대상 해석
2. **Method 의미•권한 검증**: 허용 Operation과 주체 확인
3. **조건부 요청•상태 처리**: ETag•멱등 Key와 업무 규칙 적용
4. **Representation 생성**: Accept에 맞는 Resource 표현 구성
5. **Status•Header•Link 구성**: 결과•Cache•다음 전이 제공

#### 한줄 요약

- 클라이언트가 알고 있던 엔터티 태그를 함께 보내면 서버는 현재 버전과 같을 때만 수정해 다른 사용자의 최신 변경을 덮지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Richardson Maturity Model (리처드슨 성숙도 모델)**: API가 진정한 RESTful에 얼마나 가까운지 평가하는 4단계 척도로, 실무에서는 통상 Level 2를 RESTful로 인정하는 기준.

</details>

| 성숙도 레벨 | 설계 수준 및 특징 | 매핑되는 기술 성향 |
|:---|:---|:---|
| Level 0 (The Swamp) | 단일 URI(`/api`), 단일 메서드(`POST`)만 사용하여 원격 함수 호출 | 전통적인 SOAP 기반 RPC |
| Level 1 (Resources) | URI를 통해 각각의 자원(`/users`, `/orders`) 분리 식별 | 자원(명사) 중심 분산 설계 |
| Level 2 (HTTP Verbs) | 자원에 HTTP 메서드(GET/POST/PUT/DELETE)와 상태 코드 매핑 | **실무적 표준 RESTful API** |
| Level 3 (HATEOAS) | 응답 내부에 상태 전이를 위한 링크(Hypermedia) 포함 | **이론적 완벽한 RESTful API** |

#### 한줄 요약

- RPC는 `approveOrder` 같은 업무 명령을 직접 부르고 REST는 주문 자원의 상태 표현을 공통 HTTP 규칙으로 바꾼다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Over-fetching & Under-fetching**: REST의 고정된 응답 구조 탓에 클라이언트가 불필요한 데이터를 너무 많이 받거나(Over), 한 번에 못 받아 API를 여러 번 쪼개서 호출(Under)해야 하는 고질적 성능 저하 요인.

</details>

| 3대 REST 설계 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. 컬렉션 대량 조회 병목 | `GET /users` 호출 시 수만 건 데이터 폭주 | **Pagination (Offset/Cursor 기반 페이징) 강제** |
| 2. 복잡한 다중 필터링 | URI 경로만으로 검색 조건 표현 한계 | **Query String 파라미터 활용 (`?status=A&sort=desc`)**|
| 3. API 버전 단절 | V1 백엔드 수정 시 구버전 모바일 앱 크래시 | **URI 버저닝 강제 (`/v1/users`, `/v2/users`)** |

> 사례: **카카오 / 네이버 오픈 API의 URI 버전 관리 및 Offset Pagination에서 Cursor Pagination으로의 최적화**

#### 한줄 요약

- 결제 생성 요청이 시간 초과로 다시 도착해도 같은 멱등성 키의 기존 결과를 반환하면 실제 결제는 한 번만 남는다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **RESTful 수립 기준**: 리처드슨 Level 2 이상(명사형 URI, HTTP 메서드/상태코드), Stateless 기반 토큰 인증 및 Pagination에 의거한 체계.

</details>

- Resource 중심 Web API는 **URI•Method•Status•Stateless** 일관 적용

#### 한줄 요약

- 자원 주소와 HTTP 의미를 일관되게 적용하고 생성에는 멱등성 키, 수정에는 엔터티 태그를 사용해 재전송과 동시 변경을 안전하게 처리해야 한다.
