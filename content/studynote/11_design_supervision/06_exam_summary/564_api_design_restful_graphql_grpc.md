---
title: "564. API 설계 RESTful GraphQL gRPC (API Design RESTful GraphQL gRPC)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 설계 패러다임은 **리소스 중심(REST/HTTP-JSON)**, **쿼리 중심(GraphQL/Schema-First)**, **계약 중심(gRPC/Protobuf over HTTP/2)**의 3축으로 수렴하며, 각기 다른 직렬화·전송·계약 정의 메커니즘을 통해 *네트워크 효율성·타입 안전성·클라이언트 자율성*을 상충관계(Trade-off) 속에서 최적화한다.
> 2. **가치**: 페이로드 절감(REST 대비 GraphQL/gRPC 평균 40~80%), 계약 기반 코드 자동 생성(`.proto` -> 12+ 언어 SDK), HTTP/2 멀티플렉싱을 통한 동시성 처리(Head-of-Line Blocking 제거), Strongly-Typed Schema를 통한 런타임 오류 컴파일 타임 전환으로 **MTTR 평균 30% 감소** 효과를 창출한다.
> 3. **판단 포인트**: **내부 서비스 간 통신(Backend-to-Backend)**은 gRPC 우선, **외부 공개 API(B2C/공공)**는 REST·OpenAPI 3.1 우선, **애그리게이션·BFF(Backend-For-Frontend)**는 GraphQL Federation 또는 BFF 패턴을 적용하는 *3-Tier API 전략*이 핵심 의사결정 프레임이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 산업이 SOA(Service-Oriented Architecture)에서 MSA(Microservices Architecture)로 전환되면서, 수십~수백 개의 독립 서비스가 네트워크를 통해 상호작용하는 **분산 컴퓨팅 환경**이 표준이 되었다. 이에 따라 각 서비스의 **계약(Contract)**, **전송(Transport)**, **직렬화(Serialization)** 방식이 전체 시스템의 처리량·확장성·운영 복잡도를 결정짓는 핵심 변수로 부상했다.

과거 SOAP/XML-RPC 기반의 무거운 WS-* 스택(WS-Security, WS-ReliableMessaging 등)은 **WSDL**(Web Services Description Language) 중심의 **코드-우선(Code-First) 계약**과 XML의 텍스트 무결성 오버헤드로 인해 모바일·클라우드 환경에서 병목이 발생했다. Roy Fielding이 2000년 박사논문에서 제시한 **REST**(Representational State Transfer)는 **HTTP 표준 메서드(GET/POST/PUT/DELETE/PATCH)**와 **리소스 URI**, **HATEOAS**(Hypermedia as the Engine of Application State) 원칙을 통해 stateless·cacheable·layered 시스템이라는 제약 조건을 만족시키며 웹 API의 사실 표준이 되었다.

그러나 2010년대 후반, 모바일 폭증·실시간성 요구·MSA 내부 통신의 빈도 증가로 인해 **Over-fetching**(필요 이상의 필드 수신), **Under-fetching**(추가 라운드트립 필요), **문서-구현 간 Drift** 문제가 REST의 한계로 명확해졌다. 이를 해결하기 위해 **GraphQL**(2015년 Facebook 공개)과 **gRPC**(2015년 Google 공개, 내부 Stubby의 오픈소스화)가 등장했으며, 각각 *클라이언트 주도 쿼리*와 *고성능 바이너리 RPC*라는 차별화된 해법을 제시했다.

```text
[API 설계 패러다임 진화 흐름]

   1990s        2000s         2010s 초         2010s 후반~현재
 +---------+  +----------+  +-------------+  +------------------+
 |  CORBA  |-> |SOAP/WS-* |-> |   REST/HTTP |-> | GraphQL  + gRPC  |
 | (IIOP)  |  |(XML/WSDL)|  |  (JSON/URI) |  |  (Schema/Proto)  |
 +---------+  +----------+  +-------------+  +------------------+
   RPC기반     표준화중심      자원중심          계약·쿼리·이벤트
   바이너리     무거운스택     웹친화적           고성능·타입안정
                    |                |                  |
                    v                v                  v
              [WSDL->UDDI]      [OpenAPI 3.1]      [GraphQL SDL / .proto]
              (정적 발견)       (동적 문서화)        (계약 자동생성)
```

**MSA 환경에서의 API 설계가 필수불가결한 이유**는 다음과 같이 정량화된다:
- Netflix는 700+ 마이크로서비스 간 통신을 위해 **REST->gRPC 전환**으로 P99 latency를 평균 50% 절감 (2018~2020).
- GitHub는 v3 REST API의 **GraphQL 버전(2016)**을 통해 모바일 앱의 네트워크 요청 수를 평균 90% 감소.
- Shopify, Yelp, Pinterest는 **BFF + GraphQL Federation**으로 50+ 도메인 서비스의 데이터를 단일 엔드포인트로 통합.

- **📢 섹션 요약 비유**: API 설계는 **우체국 시스템의 진화**와 같다. SOAP는 무거운 *공식 외교문서*(봉인·인증·추적 필수), REST는 누구나 사용하는 *일반 우편*(간단·표준), GraphQL은 *맞춤형 쇼핑清单*(받고 싶은 것만 적어 발송), gRPC는 *군사 전용 암호전송*(고속·압축·계약 엄격).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. RESTful API 아키텍처

REST는 **자원(Resource)**을 URI로 표현하고, **HTTP 동사(Verb)**로 상태를 전이시키는 stateless 아키텍처 스타일이다. Richardson Maturity Model(RMM)은 REST 성숙도를 4단계로 분류한다:

- **Level 0**: HTTP를 터널로 사용(SOAP XML-RPC 스타일)
- **Level 1**: 개별 자원(Resource) 분리
- **Level 2**: HTTP 동사 + 상태코드 활용
- **Level 3**: HATEOAS — 응답에 하이퍼미디어 링크 포함

```text
[RESTful API 요청-응답 플로우 (Level 2-3)]

  Client                        Server                  Database
    |                              |                       |
    |  GET /users/42/orders       |                       |
    |  Accept: application/json    |                       |
    |  Authorization: Bearer xxx   |                       |
    +-----------------------------►|                       |
    |                              |  SELECT * FROM orders |
    |                              |  WHERE user_id = 42   |
    |                              +----------------------►|
    |                              |◄----------------------+
    |  200 OK                      |   [rows...]           |
    |  Content-Type: application/json                       |
    |  Link: </orders?page=2>; rel="next"                   |
    |  { "id":42, "name":"Kim",   |                       |
    |    "orders":[ {...} ] }     |                       |
    |◄-----------------------------+                       |
    |                              |                       |

    ※ HTTP 상태코드 활용 규약
    2xx: Success (200 OK, 201 Created, 204 No Content)
    3xx: Redirection (301 Moved, 304 Not Modified, 캐시)
    4xx: Client Error (400 Bad Request, 401 Unauthorized, 404, 429 Too Many Req)
    5xx: Server Error (500, 502 Bad Gateway, 503, 504 Gateway Timeout)
```

**핵심 제약 조건**(Architectural Constraints):
1. **Client-Server**: 관심사 분리
2. **Stateless**: 각 요청은 독립, 서버는 클라이언트 컨텍스트 미보유 -> 수평확장에 유리
3. **Cacheable**: `Cache-Control`, `ETag`, `Last-Modified`로 HTTP 캐시 활용
4. **Uniform Interface**: URI(자원 식별), HTTP동사(자원 조작), MIME타입(표현), HATEOAS(상태전이)
5. **Layered System**: 로드밸런서·CDN·API Gateway 투명 삽입 가능
6. **Code-On-Demand**(선택): 스크립트 다운로드 실행

### 2. GraphQL 아키텍처

GraphQL은 **단일 엔드포인트(POST /graphql)**에서 클라이언트가 **쿼리 언어**로 필요한 데이터의 *모양(shape)*을 선언하면, 서버는 정확히 그 구조로 응답하는 **선언적·쿼리 지향** API이다.

```text
[GraphQL 요청-응답 플로우 (단일 엔드포인트)]

  Client                  GraphQL Server           Resolvers       Data Sources
    |                          |                       |                |
    |  POST /graphql          |                       |                |
    |  query: "{             |                       |                |
    |    user(id:42) {        |                       |                |
    |      name               |                       |                |
    |      orders {           |                       |                |
    |        id, totalPrice   |                       |                |
    |      }                  |                       |                |
    |    }                    |                       |                |
    |  }"                     |                       |                |
    +-------------------------►|                       |                |
    |                          |  Parse & Validate     |                |
    |                          |  (Schema Introspection|                |
    |                          |   + Type Check)       |                |
    |                          |  -------------►       |                |
    |                          |  Build Execution Plan |                |
    |                          |  (병렬/순차 최적화)   |                |
    |                          |                       |                |
    |                          |  user(42) -----------►|  REST/gRPC     |
    |                          |                       +---------------►|
    |                          |  orders(42) ---------►|  DataLoader    |
    |                          |  (Batching + Caching) +---------------►|
    |                          |                       |                |
    |                          |◄----------------------+                |
    |  200 OK                  |   { user: {           |                |
    |  { data:{                |     name:"Kim",       |                |
    |     user:{               |     orders:[          |                |
    |        name:"Kim",       |       {id:1,total:...}|                |
    |        orders:[{...}]    |     ]                 |                |
    |     }                    |   }                   |                |
    |   }}                     |   }                   |                |
    |◄-------------------------+                       |                |
    |                          |                       |                |
    ※ Subscription은 WebSocket / Server-Sent Events 기반
    ※ Persisted Query: 쿼리를 서버에 미리 등록 -> 네트워크 페이로드 0에 수렴
```

**GraphQL 핵심 구성요소**:
- **Schema Definition Language (SDL)**: `type`, `query`, `mutation`, `subscription`, `input`, `enum`, `union`, `interface`로 계약 정의
- **Resolver**: Schema 필드별 데이터 fetch 함수 (4-argument: `parent, args, context, info`)
- **Execution Engine**: 쿼리를 AST로 파싱 -> 참조 그래프 분석 -> N+1 문제 해결 위해 `DataLoader` (배치·캐시) 사용
- **N+1 Problem 해결**: 필드별 개별 호출 대신 `batch`로 묶어 한 번에 조회 (예: 사용자 100명의 주문 -> 1회 배치 쿼리)

### 3. gRPC 아키텍처

gRPC는 Google의 **Stubby**(2001년~ 내부 RPC 시스템)에서 파생된 **고성능·계약 우선(Contract-First)·다언어** RPC 프레임워크로, **Protocol Buffers(Protobuf) v3**를 IDL(Interface Definition Language)로 사용하고 **HTTP/2** 위에서 동작한다.

```text
[gRPC 통신 플로우 (Unary, Server Streaming, Client Streaming, Bidirectional)]

  +----------+                  +----------+                  +----------+
  | gRPC     |  .proto 컴파일   | Stub/    |  HTTP/2 Stream  | gRPC     |
  | Client   |  ------------►   | Channel  |  -------------►  | Server   |
  |          |                  | (Stub)   |                  | (Service)|
  +----------+                  +----------+                  +----------+
       |                              |                              |
       |  1. .proto 파일 작성         |                              |
       |  ----------------------►     |                              |
       |                              |  2. protoc 컴파일            |
       |                              |  -> 메시지 클래스 자동생성     |
       |                              |  -> 서버/클라이언트 Stub 생성  |
       |                              |                              |
       |  3. Stub 메서드 호출         |                              |
       |  (언어 네이티브 함수처럼)    |                              |
       | ----------------------------►                              |
       |                              |  4. Protobuf 직렬화          |
       |                              |  (Binary, ~JSON 대비 1/3)     |
       |                              |  5. HTTP/2 Stream으로 전송    |
       |                              |  (Header 압축 HPACK)         |
       |                              |  6. Multiplexing (단일 TCP)  |
       |                              | ----------------------------►|
       |                              |                              |
       |  4가지 통신 패턴             |                              |
       |  +--------------------+     |                              |
       |  | Unary: 1 req -> 1 res    |                              |
       |  | Server Stream: 1 req -> N|                              |
       |  | Client Stream: N -> 1    |                              |
       |  | Bidi Stream: N ↔ N      |                              |
       |  +--------------------+     |                              |
       |                              |                              |
```

**gRPC 핵심 기술**:
- **Protocol Buffers v3**: `.proto` 파일에 `service`, `rpc`, `message` 정의 -> `protoc` 컴파일러가 **12개 이상 언어**(Go, Java, C++, Python, Node.js, Ruby, PHP, C#, Dart, Kotlin, Rust 등)용 SDK 자동 생성
- **HTTP/2 전송 계층**: Multiplexing(이진 데이터 프레임 단위로 다중 스트림 동시 전송 -> **HOL Blocking 회피**), Header 압축(HPACK), 바이너리 프레이밍, 서버 푸시(제한적)
- **서비스 정의 4가지 패턴**:
  1. **Unary**: 일반 RPC (`GetUser(UserId) returns (User)`)
  2. **Server Streaming**: 서버가 다수 메시지 전송 (`Subscribe(Stock) returns (stream Price)`)
  3. **Client Streaming**: 클라이언트가 다수 메시지 전송 (`Upload(stream Chunk) returns (Ack)`)
  4. **Bidirectional Streaming**: 양방향 독립 스트림 (`Chat(stream Msg) returns (stream Msg)`)
- **Interceptors**: 미들웨어 패턴 (인증, 로깅, 메트릭, 재시도)
- **Load Balancing**: `grpclb`, Client-Side LB (Consistent Hashing, Round Robin)
- **Deadline/Timeout Propagation**: 클라이언트가 상한 시간 명시, 서버가 자율적 취소

### 4. 3가지 패러다임 통합 구성 요소 비교

| 구성 요소 | REST (HTTP/JSON) | GraphQL | gRPC |
| :--- | :--- | :--- | :--- |
| **계약 정의** | OpenAPI 3.1 (YAML/JSON, 코드-우선도 가능) | GraphQL SDL (`schema { query, mutation, subscription }`) | Protocol Buffers v3 (`.proto` IDL) |
| **전송 프로토콜** | HTTP/1.1, HTTP/2, HTTP/3 모두 가능 | HTTP/1.1 + WebSocket(Subscription) | **HTTP/2 전용** (의무) |
| **직렬화 포맷** | JSON (텍스트, 평균 200~
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 564 / 600

<- **이전**: [563. 모놀리스 분해 전략 도메인 경계](/studynote/11_design_supervision/06_exam_summary/564_monolith_decomposition_domain_boundary/)
**다음**: [565. 메시지 큐 비동기 통신 패턴](/studynote/11_design_supervision/06_exam_summary/565_message_queue_async_communication_patter/) ->

---
