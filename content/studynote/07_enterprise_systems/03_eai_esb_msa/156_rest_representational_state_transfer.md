---
title: 156. REST (Representational State Transfer)
date: '2026-05-08'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: REST ([[477_rest_api_architecture|Representational State Transfer]])는 웹의 자원(Resource)을 URI (Uniform Resource [[088_identifier_in_er_model|Identifier]])로 [[655_ir_detection_analysis|식별]]하고, [[461_http_stateless_connection_oriented|HTTP]] ([[461_http_stateless_connection_oriented|HyperText Transfer Protocol]]) 메서드와 표현(Representation)으로 상태를 주고받는 [[114_architecture_style|아키텍처 스타일]]이다.
> 2. **가치**: 웹 표준을 그대로 활용하므로 단순성, 확장성, 캐시 활용, 클라이언트-서버 독립 진화를 동시에 얻기 쉽다.
> 3. **판단 포인트**: REST는 HTTP를 쓰는 것만으로 성립하지 않는다. 자원 중심 URI, [[162_rest_statelessness|무상태성]], 메서드 의미, 상태 코드, 캐시 [[164_policy|정책]]을 함께 지켜야 RESTful 설계가 된다.

---

## Ⅰ. 개요 및 필요성

REST는 Roy Fielding이 제시한 웹 [[114_architecture_style|아키텍처 스타일]]로, "[[294_function_calling_tool_use|함수 호출]]"보다 "자원의 [[632_state_transition_diagram_testing|상태 전이]]"에 초점을 둔다. 웹이 대규모로 확장되기 위해서는 서버가 요청 간 [[160_session_controlling_terminal|세션]] 상태를 오래 붙잡지 않고, 표준 인터페이스를 통해 다양한 클라이언트가 같은 방식으로 접근할 수 있어야 했다. REST는 바로 이 웹의 확장 원리를 일반 애플리케이션 인터페이스 설계에 적용한 개념이다.

REST가 중요해진 이유는 웹 API가 늘어날수록 단순하고 예측 가능한 규칙이 필요했기 때문이다. URI는 자원을 [[655_ir_detection_analysis|식별]]하고, `GET`·`POST`·`PUT`·`DELETE` 같은 메서드는 행위를 드러내며, [[343_json|JSON]] 같은 표현은 자원의 [[178_as_is_to_be_analysis|현재 상태]]를 전달한다. 이 규칙이 맞아야 API는 읽기 쉽고 도구 친화적으로 운영된다.

- **📢 섹션 요약 비유**: REST는 가게 물건마다 진열 위치와 주문 규칙을 정해 두는 방식과 같다. 손님이 어디로 가서 무엇을 해야 하는지 한눈에 알 수 있어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

REST의 핵심 제약은 [[206_client_server_architecture_model|Client-Server]], [[239_stateless_redis|Stateless]], Cacheable, Uniform Interface, Layered System이며, [[082_process_memory_structure|Code]]-on-Demand는 선택 조건이다. 실무에서는 이 중에서도 자원 [[655_ir_detection_analysis|식별]], 메서드 의미, [[162_rest_statelessness|무상태성]], 캐시 [[268_strategy_pattern|전략]]이 가장 자주 판단 포인트가 된다.

| 제약 조건 | 의미 | 실무 효과 |
| :--- | :--- | :--- |
| [[206_client_server_architecture_model|Client-Server]] | UI와 [[001_dikw_pyramid|데이터]] 처리를 분리 | 독립 배포와 역할 분리 |
| [[239_stateless_redis|Stateless]] | 요청마다 필요한 정보를 포함 | 수평 확장, [[160_session_controlling_terminal|세션]] 의존 감소 |
| Cacheable | 응답 캐시 가능 | [[282_performance_tactics|성능]] 개선, 서버 부하 감소 |
| Uniform Interface | 자원·메서드·표현 규칙 [[194_consistency_database_integrity|일관성]] | 학습 비용과 [[195_coupling_levels|결합도]] 감소 |
| Layered System | [[264_proxy_pattern_surrogate_access_control|프록시]]·게이트웨이 계층 허용 | 보안, 로깅, 확장성 향상 |

아래 그림은 REST 요청이 자원 중심으로 흘러가는 기본 구조를 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│ REST request flow                                            │
├──────────────────────────────────────────────────────────────┤
│ Client                                                       │
│   │  GET /orders/100                                         │
│   ▼                                                          │
│ Cache / Gateway / Proxy                                      │
│   │                                                          │
│   ▼                                                          │
│ Resource endpoint -> representation(JSON/XML)                │
│   │                                                          │
│   └-> HTTP status + links + cache metadata                   │
└──────────────────────────────────────────────────────────────┘
```

즉 REST의 핵심은 URL만 예쁘게 짓는 것이 아니라, [[461_http_stateless_connection_oriented|HTTP]] 자체가 가진 의미를 살려 **웹의 기본 동작 원리 위에 API를 얹는 것**이다. 그래서 메서드 의미와 캐시 [[164_policy|정책]]을 무시한 채 `POST /getUser` 같은 형태를 쓰면 HTTP를 터널처럼 쓰는 셈이 된다.

- **📢 섹션 요약 비유**: REST는 집집마다 주소를 붙이고, 택배·반품·조회 규칙을 표준화한 동네와 같다. 주소만 있고 규칙이 없으면 오히려 더 혼란스럽다.

---

## Ⅲ. 비교 및 연결

REST는 [[153_soap_simple_object_access_protocol|SOAP]] ([[153_soap_simple_object_access_protocol|Simple Object Access Protocol]])나 [[126_rpc|RPC]] ([[126_rpc|Remote Procedure Call]]) 스타일과 비교할 때 성격이 분명해진다. [[153_soap_simple_object_access_protocol|SOAP]]/RPC가 "어떤 함수를 호출할 것인가"에 가깝다면, REST는 "어떤 자원의 상태를 어떻게 바꿀 것인가"에 더 가깝다. 이 차이는 계약 방식, 확장성, 캐시 활용, [[195_coupling_levels|결합도]]에서 차이를 만든다.

| 항목 | REST | [[153_soap_simple_object_access_protocol|SOAP]] |
| :--- | :--- | :--- |
| 중심 개념 | 자원(Resource) | 연산([[329_delta_encoding|Operation]]) |
| 기본 전송 | [[461_http_stateless_connection_oriented|HTTP]] 의미 적극 활용 | XML Envelope 기반 [[389_mesh_topology|메시]]지 |
| 표현 형식 | [[343_json|JSON]], XML 등 유연 | XML 중심 |
| 강점 | 단순성, 웹 친화성, 캐시 | 엄격한 계약, WS-* 확장 |
| 적합한 영역 | 웹·모바일·공개 [[014_api_posix|API]] | 강한 계약과 레거시 B2B |

REST는 이후 [[157_restful_api_richardson_maturity_model|Richardson Maturity Model]], HATEOAS ([[161_rest_level_3_hateoas|Hypermedia as the Engine of Application State]]), [[542_api_gateway|API Gateway]] 설계와도 연결된다. 즉 REST는 단순 호출 규칙이 아니라, 웹 [[014_api_posix|API]] 전반의 설계 철학을 여는 출발점이다.

- **📢 섹션 요약 비유**: REST가 잘 정리된 도서관 열람 체계라면, SOAP는 복잡하지만 엄격한 문서 결재 절차에 가깝다. 둘 다 쓸모 있지만 목적이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 REST를 적용할 때 가장 중요한 것은 "동사를 URL에 넣지 않는 것"보다 더 넓다. 자원 중심 URI, 메서드의 안전성·[[171_idempotency_iac_terraform|멱등성]], 상태 코드 [[194_consistency_database_integrity|일관성]], [[303_authentication_authorization_patterns|인증]]의 무상태 처리, 캐시 가능 응답 구분까지 함께 설계해야 한다. 특히 `GET`은 조회, `PUT`은 전체 대체, `PATCH`는 부분 수정, `DELETE`는 삭제처럼 의미를 흐리지 않아야 운영과 테스트가 단순해진다.

### 설계 [[435_checklist_based_testing|체크리스트]]

1. URI가 `/users/10/orders/5`처럼 자원 중심으로 설계되었는가?
2. `GET` 요청이 서버 상태를 바꾸지 않는가?
3. 토큰 기반 [[303_authentication_authorization_patterns|인증]] 등으로 서버 [[160_session_controlling_terminal|세션]] 의존을 줄였는가?
4. ETag, Cache-Control, 200/201/204/404 같은 표준 응답 규칙을 일관되게 쓰는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- `POST /getUser`, `POST /deleteOrder` 같은 [[126_rpc|RPC]] 스타일 URL
- 모든 요청을 `POST` 하나로 처리하는 설계
- 서버가 사용자 [[160_session_controlling_terminal|세션]] 상태를 과도하게 보관해 수평 확장을 막는 구조

- **📢 섹션 요약 비유**: REST 설계는 가게 간판만 바꾸는 일이 아니라 계산대 규칙, 영수증 양식, 반품 절차를 함께 맞추는 일이다.

---

## Ⅴ. 기대효과 및 결론

REST를 제대로 적용하면 API의 [[333_readability_vs_efficiency|가독성]], 캐시 효율, 확장성, 도구 [[344_compatibility_usability|호환성]]이 좋아진다. 웹 프런트엔드, 모바일 앱, 외부 파트너가 같은 자원 규칙을 공유하므로 문서화와 운영 자동화도 쉬워진다. 특히 [[162_rest_statelessness|무상태성]]과 계층화는 클라우드 환경에서 수평 확장과 게이트웨이 운영에 큰 장점을 준다.

반면 REST가 모든 통합 문제의 정답은 아니다. 강한 계약, 복잡한 [[191_transaction_concept_states|트랜잭션]] 보장, 초저지연 이진 통신이 더 중요한 환경에서는 [[153_soap_simple_object_access_protocol|SOAP]], [[479_grpc_protobuf_http2|gRPC]], 이벤트 기반 방식이 더 적절할 수 있다. 따라서 REST는 "HTTP로 API를 만든다"가 아니라 **웹의 제약을 이용해 단순하고 확장 가능한 인터페이스를 설계하는 방식**으로 기억해야 한다.

- **📢 섹션 요약 비유**: REST는 동네 전체가 같은 교통 법규를 쓰게 만드는 일과 같다. 규칙이 통일되면 새 차가 들어와도 훨씬 덜 헷갈린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| URI (Uniform Resource [[088_identifier_in_er_model|Identifier]]) | REST의 자원 [[655_ir_detection_analysis|식별]] 수단 |
| [[461_http_stateless_connection_oriented|HTTP]] Method | [[632_state_transition_diagram_testing|상태 전이]]를 표현하는 기본 동작 |
| HATEOAS | REST 성숙도의 고급 단계 |
| [[157_restful_api_richardson_maturity_model|Richardson Maturity Model]] | RESTful 설계 수준 평가 틀 |
| [[153_soap_simple_object_access_protocol|SOAP]] | REST와 자주 대비되는 계약 중심 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
RPC over HTTP
  │
  ▼
REST resource design
  │
  ▼
RESTful API maturity
  │
  ├─> HTTP caching / stateless auth
  │
  ▼
Hypermedia / API governance / modern web APIs
```

### 👶 어린이를 위한 3줄 비유 설명

1. REST는 물건마다 주소표를 붙여 두고, 가져오기·넣기·지우기 규칙을 정하는 방법이에요.
2. 그래서 누가 와도 같은 규칙으로 물건을 찾고 바꿀 수 있어요.
3. 규칙을 잘 지키면 가게가 커져도 덜 헷갈리고 더 빨리 일할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 156 / 482

← **이전**: [[155_eai_vs_esb_architecture|155. EAI vs ESB (EAI vs ESB Architecture)]]
**다음**: [[157_restful_api_richardson_maturity_model|157. RESTful API 성숙도 모델 (Richardson Maturity Model)]] →

---
