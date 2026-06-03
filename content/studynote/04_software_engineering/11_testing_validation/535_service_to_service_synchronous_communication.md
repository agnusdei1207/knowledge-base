+++
title = "535. 서비스 간 동기 통신 - REST API, gRPC"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 서비스 간 동기 통신(Synchronous Communication)은 요청자(클라이언트 서비스)가 응답이 올 때까지 블로킹(Blocking) 상태로 대기하는 통신 방식으로, REST API와 gRPC가 마이크로서비스 환경의 대표 프로토콜이다.
> 2. **가치**: 구현이 직관적이고 즉각적인 결과 확인이 가능하여 조회 중심 작업과 실시간 응답이 필요한 시나리오에 적합하며, HTTP 표준과 OpenAPI를 통한 명확한 계약 설계가 가능하다.
> 3. **판단 포인트**: 동기 호출 체인이 깊어질수록 레이턴시가 누적되고 장애가 전파되므로, 서킷 브레이커(Circuit Breaker), 타임아웃, 재시도 전략이 필수이며 3단계 이상 체인은 비동기로 전환을 검토해야 한다.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 아키텍처에서 개별 서비스들은 필연적으로 서로 통신해야 한다. 통신 방식은 크게 동기(Synchronous)와 비동기(Asynchronous)로 나뉘는데, 동기 통신은 클라이언트 서비스가 서버 서비스에 요청을 보내고 응답이 올 때까지 기다리는 방식이다.

초기 SOA(Service-Oriented Architecture) 시대에는 SOAP/XML 기반의 웹 서비스가 표준이었다. 그러나 SOAP는 복잡한 스키마와 오버헤드로 인해 마이크로서비스에 적합하지 않았다. 2000년대 초반 로이 필딩(Roy Fielding)이 박사 논문에서 REST(Representational State Transfer) 아키텍처 스타일을 제안하면서, HTTP 기반의 단순하고 확장 가능한 API 설계 원칙이 정립되었다.

2015년 Google이 내부 RPC 프레임워크를 오픈소스로 공개한 gRPC는 HTTP/2와 Protocol Buffers(Protobuf)를 기반으로 고성능 바이너리 통신을 제공하며, REST의 대안으로 부상했다. 특히 서비스 간 내부 통신(Internal Communication)에서 gRPC는 REST 대비 3-10배의 성능 우위를 보인다.

마이크로서비스에서 동기 통신이 중요한 이유는 여전히 많은 시나리오에서 즉각적인 응답이 필요하기 때문이다. 상품 재고 확인 후 주문 처리, 사용자 인증 후 서비스 제공, 실시간 가격 조회 등은 비동기로 처리하기 어렵다. 그러나 동기 통신의 특성상 체인이 길어질수록 단일 실패 지점이 증가하고 레이턴시가 누적되는 문제가 발생한다.

- **📢 섹션 요약 비유**: 전화 통화처럼 상대방이 받을 때까지 기다렸다가 대화하는 방식이다. 빠르게 확인하고 진행할 수 있지만, 상대방이 통화 중이거나 연결이 끊기면 바로 문제가 생긴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### REST API 핵심 원칙

REST(Representational State Transfer)는 HTTP 프로토콜 위에서 자원(Resource) 중심의 API를 설계하는 아키텍처 스타일이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">REST API 설계 원칙 (Richardson Maturity Model)</div></div>
<div class="kb-diagram-note">Level 0: HTTP 전송 수단으로만 활용 (RPC-like)</div>
<div class="kb-diagram-note">POST /orderService?action=createOrder</div>
<div class="kb-diagram-note">Level 1: 자원(Resource) 도입</div>
<div class="kb-diagram-note">POST /orders</div>
<div class="kb-diagram-note">GET /orders/123</div>
<div class="kb-diagram-note">Level 2: HTTP 동사(Verb) 활용</div>
<div class="kb-diagram-note">GET /orders → 목록 조회</div>
<div class="kb-diagram-note">POST /orders → 주문 생성</div>
<div class="kb-diagram-note">GET /orders/{id} → 단건 조회</div>
<div class="kb-diagram-note">PUT /orders/{id} → 전체 수정</div>
<div class="kb-diagram-note">PATCH /orders/{id} → 부분 수정</div>
<div class="kb-diagram-note">DELETE /orders/{id} → 삭제</div>
<div class="kb-diagram-note">Level 3: 하이퍼미디어(HATEOAS) 활용</div>
<div class="kb-diagram-note">응답에 관련 링크 포함 (완전한 REST)</div>
</div>
</div>



### gRPC 핵심 구조

gRPC는 Protocol Buffers를 인터페이스 정의 언어(IDL)로 사용하고, HTTP/2를 전송 계층으로 활용한다.

```protobuf
// 서비스 정의 (order.proto)
syntax = "proto3";

service OrderService {
    rpc CreateOrder (CreateOrderRequest)
        returns (CreateOrderResponse);
    rpc GetOrder (GetOrderRequest)
        returns (Order);
    rpc ListOrders (ListOrdersRequest)
        returns (stream Order);  // 서버 스트리밍
}

message CreateOrderRequest {
    string user_id = 1;
    repeated OrderItem items = 2;
}

message Order {
    string order_id = 1;
    string status = 2;
    int64 total_price = 3;
}
```

### REST vs gRPC 상세 비교

| 비교 항목 | REST API | gRPC |
|:---|:---|:---|
| 프로토콜 | HTTP/1.1 (HTTP/2 지원 증가) | HTTP/2 전용 |
| 데이터 형식 | JSON (텍스트, 사람이 읽기 쉬움) | Protocol Buffers (바이너리, 압축) |
| 스키마 정의 | OpenAPI (Swagger) - 선택적 | .proto 파일 - 필수 |
| 성능 | 보통 (JSON 파싱 오버헤드) | 높음 (바이너리, HTTP/2 멀티플렉싱) |
| 타입 안전성 | 느슨함 (런타임 오류 가능) | 강함 (컴파일 타임 검증) |
| 스트리밍 | 제한적 (WebSocket 별도) | 단방향/양방향 스트리밍 내장 |
| 브라우저 지원 | 완벽 | 제한적 (gRPC-Web 필요) |
| 학습 곡선 | 낮음 | 중간 (proto 언어 학습 필요) |
| 생태계 | 방대함 | 성장 중 |
| 적합 사용처 | 외부 API, 브라우저 클라이언트 | 서비스 간 내부 통신 |

### 동기 통신 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">동기 통신 호출 체인 예시</div></div>
<div class="kb-diagram-note">클라이언트</div>
<div class="kb-diagram-note">↓ HTTP 요청 (블로킹 대기)</div>
<div class="kb-diagram-note">API 게이트웨이</div>
<div class="kb-diagram-note">↓ 내부 REST/gRPC 호출 (블로킹 대기)</div>
<div class="kb-diagram-note">주문 서비스 (Order Service)</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">동기 호출</div></div>
<div class="kb-diagram-note">↓ 재고 확인 응답</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">동기 호출</div></div>
<div class="kb-diagram-note">↓ 가격 계산 응답</div>
<div class="kb-diagram-tree-item" style="--depth:2">→ 응답 조합 후 반환</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">API 게이트웨이 → 클라이언트</div>
<div class="kb-diagram-note">총 레이턴시 = 각 서비스 처리 시간의 합산</div>
</div>
</div>



### HTTP 상태 코드와 오류 처리

| 상태 코드 | 의미 | REST API에서 활용 |
|:---|:---|:---|
| 200 OK | 성공 | 조회/수정 성공 |
| 201 Created | 생성 성공 | POST 후 신규 자원 생성 |
| 204 No Content | 성공, 응답 바디 없음 | DELETE 성공 |
| 400 Bad Request | 잘못된 요청 | 유효성 검사 실패 |
| 401 Unauthorized | 인증 필요 | 로그인 필요 |
| 403 Forbidden | 접근 금지 | 권한 없음 |
| 404 Not Found | 자원 없음 | 존재하지 않는 ID |
| 409 Conflict | 충돌 | 중복 데이터 |
| 429 Too Many Requests | 과부하 | 레이트 리미팅 |
| 500 Internal Server Error | 서버 오류 | 예상치 못한 서버 장애 |
| 503 Service Unavailable | 서비스 불가 | 서버 과부하/다운 |

- **📢 섹션 요약 비유**: REST는 우리가 일상에서 쓰는 말로 주고받는 편지(사람이 읽기 쉬운 JSON), gRPC는 컴퓨터가 이해하는 암호화된 전보(바이너리 Protocol Buffers)와 같다. 편지는 누구나 이해하고, 전보는 빠르고 정확하다.

---

## Ⅲ. 비교 및 연결

### 동기 통신 vs 비동기 통신 비교

| 비교 항목 | 동기 통신 | 비동기 통신 |
|:---|:---|:---|
| 응답 방식 | 즉시 응답 대기 (블로킹) | 응답 기다리지 않음 (논블로킹) |
| 구현 복잡도 | 낮음 (직관적 함수 호출과 유사) | 높음 (메시지 큐, 이벤트 핸들링) |
| 레이턴시 | 즉시 (ms 수준) | 지연 가능 (ms~초 수준) |
| 장애 전파 | 높음 (하나 죽으면 전체 영향) | 낮음 (큐가 버퍼 역할) |
| 확장성 | 보통 (동기 블로킹으로 제한) | 높음 (독립적 처리량 조절) |
| 데이터 일관성 | 강한 일관성 보장 가능 | 최종 일관성 (Eventually Consistent) |
| 적합 시나리오 | 실시간 조회, 즉각 결과 필요 | 주문 처리, 이메일 발송 등 비실시간 |

### 서비스 메시(Service Mesh)와의 연계

서비스 메시(Istio, Linkerd 등)는 동기 통신을 안전하게 관리하는 인프라 레이어다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">서비스 메시 아키텍처</div></div>
<div class="kb-diagram-note">서비스 A 서비스 B</div>
<div class="kb-diagram-note">사이드카 프록시 → 사이드카 프록시</div>
<div class="kb-diagram-note">(Envoy) (Envoy)</div>
<div class="kb-diagram-note">↕</div>
<div class="kb-diagram-note">컨트롤 플레인 (Control Plane)</div>
<div class="kb-diagram-tree-item" style="--depth:0">트래픽 관리 정책</div>
<div class="kb-diagram-tree-item" style="--depth:0">mTLS 인증</div>
<div class="kb-diagram-tree-item" style="--depth:0">서킷 브레이커 설정</div>
<div class="kb-diagram-tree-item" style="--depth:0">레이트 리미팅</div>
</div>
</div>



- **📢 섹션 요약 비유**: 한 명이 답해야 다음 단계로 넘어가는 릴레이 경주다. 한 주자(서비스)가 넘어지면(장애) 바통을 받지 못한 다음 주자도 멈춘다. 서킷 브레이커는 "이미 쓰러진 주자한테는 바통 넘기지 않는다"는 전략이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### REST API 설계 모범 사례

```
[좋은 REST API 설계]

# URL 설계 - 명사, 복수형
GET  /api/v1/orders           # 목록
GET  /api/v1/orders/{id}      # 단건
POST /api/v1/orders           # 생성
PATCH /api/v1/orders/{id}/cancel  # 특정 액션

# 버전 관리
/api/v1/... → /api/v2/... (하위 호환 유지)

# 페이지네이션
GET /api/v1/orders?page=1&size=20&sort=created_at,desc

# HATEOAS (선택적)
{
    "orderId": "123",
    "status": "CREATED",
    "_links": {
        "self": "/api/v1/orders/123",
        "cancel": "/api/v1/orders/123/cancel",
        "payment": "/api/v1/payments/order/123"
    }
}
```

### 설계 판단 체크리스트

1. **타임아웃 설정 적절성**: 모든 동기 호출에 적절한 타임아웃(일반적으로 1-5초)이 설정되어 있는가?
2. **재시도 안전성 (멱등성)**: 재시도 시 중복 처리가 발생하지 않도록 멱등성(Idempotency)이 보장되는가? (GET, PUT, DELETE는 기본 멱등, POST는 별도 처리 필요)
3. **서킷 브레이커 적용**: 호출하는 서비스의 장애를 빠르게 감지하고 폴백(Fallback)을 제공하는가?
4. **호출 체인 깊이**: 동기 호출 체인이 3단계를 넘지 않는가? 깊은 체인은 비동기 전환을 검토해야 한다.
5. **계약(Contract) 명확성**: OpenAPI 스펙 또는 .proto 파일로 API 계약이 명확히 정의되어 있는가?
6. **버전 관리 전략**: API 변경 시 하위 호환성을 유지하거나 명확한 버전 전환 전략이 있는가?
7. **부하 분산**: 서비스 디스커버리와 로드 밸런서를 통해 트래픽이 균등하게 분산되는가?

### 안티패턴

- **동기 호출 지옥 (Synchronous Call Chain Hell)**: 서비스 A → B → C → D → E처럼 깊은 동기 호출 체인을 만들면, 총 레이턴시가 각 서비스 처리 시간의 합이 되고 최하위 서비스 장애가 전체를 마비시킨다. 체인이 3단계를 넘으면 비동기 이벤트 기반으로 전환해야 한다.
- **타임아웃 없는 무한 대기**: 타임아웃을 설정하지 않으면 응답하지 않는 서비스로 인해 스레드 풀이 소진되고 전체 서비스가 연쇄적으로 장애를 일으킨다. 이를 "캐스케이딩 실패(Cascading Failure)"라 한다.
- **API 버저닝 부재**: 하위 호환성 없이 API를 변경하면 모든 클라이언트 서비스를 동시에 배포해야 한다. 이는 독립 배포 원칙을 위반하는 것이다.
- **과도한 데이터 조회 (Chatty Interface)**: 하나의 화면을 구성하기 위해 수십 개의 API를 개별 호출하는 패턴이다. BFF(Backend for Frontend) 패턴이나 GraphQL로 해결할 수 있다.

- **📢 섹션 요약 비유**: 식당에서 요리사가 재료마다 창고에 직접 가서 확인하면(과도한 동기 호출) 요리가 느려진다. 재료 목록을 한 번에 요청하거나(배치 API), 미리 준비해 두는(캐싱) 방법이 효율적이다.

---

## Ⅴ. 기대효과 및 결론

동기 통신(REST API/gRPC)을 올바르게 설계하고 적용하면 다음과 같은 효과를 얻을 수 있다.

**정량적 효과**: gRPC는 REST 대비 페이로드 크기를 60-70% 줄이고, 처리 속도를 5-10배 향상시켜 서비스 간 통신 비용을 크게 절감한다. 적절한 타임아웃과 서킷 브레이커 적용으로 장애 격리 시간을 수 분에서 수 초로 단축한다.

**정성적 효과**: OpenAPI 명세나 .proto 파일을 통한 명확한 API 계약은 팀 간 인터페이스 협의 비용을 줄이고, 자동 코드 생성으로 개발 생산성을 높인다. 타입 안전한 gRPC는 컴파일 타임에 API 오류를 발견하여 런타임 버그를 예방한다.

미래 방향으로는 GraphQL이 복잡한 클라이언트 데이터 요구사항을 유연하게 처리하는 대안으로 부상하고 있으며, REST와 gRPC를 혼용하는 하이브리드 전략이 표준화되는 추세다. 특히 AI 서비스와의 통합에서는 스트리밍 응답을 지원하는 gRPC 스트리밍이 점점 중요해지고 있다.

- **📢 섹션 요약 비유**: 빠른 통신(gRPC)은 빠른 특급 배달처럼 내용(바이너리)이 압축되어 효율적이고, 표준 통신(REST)은 누구나 읽을 수 있는 일반 우편처럼 호환성이 좋다. 상황에 맞는 방법을 선택하는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 마이크로서비스 분해 패턴 (532) | 분해된 서비스 간 주요 통신 방식 |
| 서비스 간 비동기 통신 (536) | 동기의 한계를 보완하는 대안 통신 방식 |
| 서킷 브레이커 (572) | 동기 통신 장애 전파 방지 핵심 패턴 |
| 타임아웃/재시도/백오프 (573) | 동기 통신 안정성 확보 기법 |
| API 게이트웨이 패턴 | 외부 클라이언트 → 내부 서비스 단일 진입점 |
| BFF 패턴 (543) | 클라이언트별 최적화된 API 집계 |
| 서비스 디스커버리 (541) | 동적으로 서비스 주소를 찾아 호출 |
| 사이드카 프록시 패턴 (546) | 동기 통신을 투명하게 관리하는 인프라 레이어 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SOAP/XML 웹 서비스 (2000년대)</div>
<div class="kb-diagram-note">(복잡하고 무거운 SOA 통신)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">REST 아키텍처 스타일 등장 (Roy Fielding, 2000)</div>
<div class="kb-diagram-note">(HTTP + JSON, 단순하고 범용적)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">마이크로서비스 REST API 표준화 (2014~)</div>
<div class="kb-diagram-note">(OpenAPI/Swagger, Richardson Maturity Model)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">gRPC 오픈소스 공개 (Google, 2015)</div>
<div class="kb-diagram-note">(HTTP/2 + Protocol Buffers, 고성능 RPC)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">GraphQL 확산 (Facebook, 2015~)</div>
<div class="kb-diagram-note">(클라이언트 주도 쿼리 언어)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">서비스 메시 (Istio, Linkerd) 통합 (2017~)</div>
<div class="kb-diagram-note">(동기 통신 인프라 레이어 추상화)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">gRPC 스트리밍 + AI 서비스 통합</div>
<div class="kb-diagram-note">(LLM API, 실시간 추론 스트리밍)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 친구에게 전화해서 "숙제 답이 뭐야?" 물어보고 답을 들을 때까지 기다리는 것처럼, 동기 통신은 서비스가 다른 서비스의 답을 기다리는 방식이에요.
2. REST API는 한국어로 대화하는 것처럼 사람이 이해하기 쉽고, gRPC는 짧고 빠른 모스 부호처럼 컴퓨터가 더 빠르게 처리해요.
3. 전화 연결이 안 될 때(서비스 장애) 계속 기다리는 건 좋지 않으니, 서킷 브레이커라는 장치가 "지금은 전화 안 되니 다른 방법 써"라고 알려주는 역할을 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 661 / 973

← **이전**: [534. 하위 도메인에 따른 분해 (DDD 기반)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/534_subdomain_decomposition/)
**다음**: [535. 서비스 간 동기 통신 - REST API, gRPC (Protocol Buffers)](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) →

---
