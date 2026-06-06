---
title: "457. API 게이트웨이 패턴 라우팅 인증 (API Gateway Pattern Routing Authentication)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 게이트웨이는 마이크로서비스 토폴로지에서 L7 라우팅(Route Matching -> Path Rewriting -> Service Discovery -> Health Check)과 인증/인가(JWT 검증, OAuth 2.0/OIDC 토큰 인스펙션, mTLS 터미네이션, API Key/Secret 검증)를 단일 인그레스(Ingress) 지점에 정책 기반(policy-based)으로 통합한 Edge-Side Cross-Cutting Concern 처리 패턴이다.
> 2. **가치**: 인증 로직의 중앙 집중화로 N개 서비스 × M개 클라이언트의 N×M 인증 결합도를 N+M으로 축소(Back-end for Front-end 분리 시 평균 35~60% TTFB 감소, Netflix Zuul/AWS API Gateway 기준 캐시 적중 시 인증 지연 80% 절감), 12-Factor App의 "Config 외부화" 원칙 준수를 통한 Key Rotation 시간 평균 4시간 -> 5분 단축.
> 3. **판단 포인트**: ① Centralized Gateway(단일 장애점/SPOF, ① Kong/Zuul) vs Sidecar(Envoy/Istio, ② Mesh 내부) vs Hybrid(Mesh Edge), ② Gateway Authentication의 위치(Edge 단일 vs BFF별 분리), ③ Token 검증의 Stateless(JWT + JWK 캐시) vs Stateful(Session + Redis) 결정, ④ Internal Service-to-Service 인증(mSPIRE, mTLS)을 게이트웨이가 처리할지 별도 mTLS Mesh에 위임할지 분리.

---

## Ⅰ. 개요 및 필요성

마이크로서비스 아키텍처(MSA)가 100개 이상의 서비스로 확장되면 클라이언트는 각 서비스의 엔드포인트, 인증 메커니즘, SLA를 개별 인지해야 하는 **"Chatty Client"** 문제가 발생한다. Netflix는 2013년 내부 API 게이트웨이(현 Zuul) 도입 전, 600여 개 디바이스가 500여 개 서비스와 1:N 통신으로 평균 28회의 API 호출을 수행했으나, 게이트웨이 도입 후 단일 도메인 진입점으로 **평균 6회**로 감소했다(Speakerdeck, "Netflix API" 2013).

API 게이트웨이의 **라우팅(Routing)** 기능은 클라이언트 요청을 Path/Header/Query/Method 기반으로 매칭하여 적절한 백엔드 서비스로 전달하며, 동시에 **인증(Authentication)** 모듈이 토큰의 서명·만료·청구(claim)·Revocation을 검증한다. 전통적인 ESB(Enterprise Service Bus)가 무거운 SOAP/XML 기반의 비즈니스 로직 조합을 담당했다면, API 게이트웨이는 **경량(Stateless)·REST/GraphQL·Cloud-Native·Policy-Driven** 환경에 특화된 **Edge Proxy**이다.

특히 2020년 이후 Zero Trust Architecture(ZTA, NIST SP 800-207) 패러다임이 표준화되면서, 게이트웨이는 "네트워크 내부 = 신뢰"라는 기존 경계 보안 모델을 폐기하고 **"Never Trust, Always Verify"** 원칙을 모든 요청에 적용하는 핵심 enforcement point로 자리 잡았다. 국내에서는 2024년 금융보안원의 금융 클라우드 이용 가이드라인이 API 게이트웨이를 통한 **중앙화된 인증·로깅·DDoS 차단**을 필수 통제 항목으로 명시하고 있다.

```text
[ Legacy Monolithic / ESB 시대 ]
  Client(Desktop) --► ESB(SOAP/XML) --► WAS(Monolith)
                  ◄ 인증/비즈니스로직 강결합
                  ◄ 배포 단위 단일, 확장성 v

[ MSA / Cloud-Native 시대 ]
  Mobile/Web/IOT/Partner
        |
        v
  +--------------------------------------------+
  |  API Gateway (Edge Layer)                 |
  |  • Routing(Path/Header/Weight)            |
  |  • Authentication(JWT/OAuth2/mTLS/Key)    |
  |  • Rate-Limit / Quota / Throttling        |
  |  • Circuit Breaker / Retry / Fallback     |
  |  • Logging / Tracing / Metrics            |
  |  • Protocol Translation(gRPC↔REST↔WS)     |
  +--------+-----------------------------------+
           |
   +-------+--------+----------+
   v       v        v          v
  Order  Payment  Inventory  User     (백엔드 마이크로서비스)
  Svc    Svc      Svc        Svc
```

기존 **ESB vs API Gateway** 핵심 차이는 다음과 같다. ① ESB는 중앙 집중형의 비동기 메시지 브로커(JMS/AMQP) 기반 비즈니스 로직 오케스트레이션, API 게이트웨이는 동기 HTTP/REST·GraphQL 프록시 기반의 **Request Forwarding + Cross-Cutting Concern** 처리이다. ② ESB는 보통 무거운 상용 솔루션(IBM WebSphere ESB, Oracle OSB) 위주였으나, 게이트웨이는 경량 OSS(Kong, Tyk, KrakenD) 및 Managed Service(AWS API Gateway, Azure APIM, GCP Apigee) 양대 축으로 구성된다. ③ 트랜잭션 처리에서 ESB는 BPEL/XPath 기반의 장기 트랜잭션(Long-Running Transaction) 처리를 지원한 반면, API 게이트웨이는 Saga/Outbox 같은 **결합도 낮은 분산 트랜잭션 패턴**과 함께 사용된다.

- **📢 섹션 요약 비유**: API 게이트웨이는 마이크로서비스 도시의 **"국경 검문소 + 우체국"**이다. 다양한 차량(클라이언트)이 들어올 때 여권(토큰) 검사, 목적지 분류(라우팅), 속도 제한(Quota), 출입 기록(Logging)을 일괄 처리한 뒤 적절한 시(district, 즉 서비스)로 안내하는 단일 관문이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

API 게이트웨이의 내부 아키텍처는 **Reactive/Event-Loop 기반 비동기 I/O** 위에서 동작하는 L7 Reverse Proxy이며, **Filter Chain(또는 Plugin Chain)** 패턴으로 Cross-Cutting Concern을 모듈화한다. Netflix Zuul 2(Spring 2018)는 Netty 기반의 **Async Servlet 3.1 + RxJava** 모델로 전환하여, 동기 Zuul 1 대비 Throughput 약 40% 향상, p99 Latency 60% 절감을 달성했다(Netflix Tech Blog, 2018).

### 핵심 동작 흐름(End-to-End Request Lifecycle)

```text
 Client
   |   GET /v2/orders/12345
   |   Host: api.example.com
   |   Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
   |   X-Request-ID: 7f3a-9c12-bb04
   v
+------------------------------------------------------------------+
| [Phase 1] Network Edge                                            |
|  • TLS Termination(NGINX/Envoy/ALB): SNI -> Cert 선택              |
|  • DDoS L3/L4(MaxMind, AWS Shield)                                |
|  • WAF 룰(SQLi/XSS/Path-Traversal, OWASP CRS v3.3)                |
+------------------------------------------------------------------+
| [Phase 2] Pre-Routing Filters (Request 전처리)                    |
|  • Rate-Limit: Token Bucket(Lua script) -> 1000 RPS/IP             |
|  • Bot Detection(reCAPTCHA Enterprise, FingerprintJS)            |
|  • CORS Preflight(OPTIONS Method)                                |
|  • Request Validation(OpenAPI 3.0 Schema, JSON Schema Draft-07)   |
+------------------------------------------------------------------+
| [Phase 3] Authentication Filter (★ 본 토픽 핵심)                  |
|  ① Header 추출: Authorization / X-API-Key / mTLS Peer Cert      |
|  ② Token 파싱: JWT Header.Payload.Signature 분리                 |
|  ③ Signature 검증: JWK 캐시(Redis TTL 600s) + RS256/ES256 검증  |
|  ④ Claim 검증: iss, aud, exp, nbf, iat, scope, sub               |
|  ⑤ Revocation Check: Redis Blocklist(jti) / introspection(POST)  |
|  ⑥ mTLS 경로: SPIFFE ID 추출(URI SAN, e.g.                       |
|      spiffe://example.com/ns/payments/sa/checkout)               |
|  ⑦ Context Propagation: X-User-Id, X-Tenant-Id, X-Scopes 주입     |
+------------------------------------------------------------------+
| [Phase 4] Authorization(RBAC/ABAC)                                |
|  • Policy Engine: OPA(Rego), Casbin, Cerbos                       |
|  • Scope 검증: scope:read:orders ∧ path=/orders                   |
|  • Tenant Isolation: X-Tenant-Id ↔ JWT.sub 매핑                   |
+------------------------------------------------------------------+
| [Phase 5] Routing Engine                                          |
|  • Route Table:                                                   |
|      /v1/orders/*       -> order-service.prod.svc.cluster.local    |
|      /v1/payments/*     -> payment-service(canary 10%)            |
|      /v1/legacy/*       -> legacy-mock(404 fallback)               |
|  • Service Discovery: Consul DNS / K8s EndpointSlices             |
|  • Load Balancing: EWMA(Envoy) / Round-Robin / Ring Hash          |
|  • Path Rewriting: /v2/orders/* -> /internal/orders/{id}          |
|  • Header Rewrite: Host / X-Forwarded-* / X-B3-TraceId           |
+------------------------------------------------------------------+
| [Phase 6] Outbound Filters                                        |
|  • Circuit Breaker(Resilience4j/Hystrix)                         |
|  • Retry: 지수 백오프(jitter 포함) + 멱등성 키 헤더               |
|  • Timeout: 30s(상위), 5s(백엔드)                                 |
|  • mTLS to Backend: SPIRE Issued Cert(Rotate 24h)                 |
|  • Response Transformation: GraphQL↔REST / XML->JSON              |
+------------------------------------------------------------------+
| [Phase 7] Post-Routing Filters                                    |
|  • Response Caching: Cache-Control 헤더 기반(Edge TTL)            |
|  • Response Compression: Brotli(q=4) / gzip(level=6)              |
|  • Audit Log: 구조화(JSON) -> Kafka(security.audit topic)          |
|  • Distributed Tracing: OpenTelemetry Span export                 |
+------------------------------------------------------------------+
           |
           v
       Backend Microservice (gRPC/HTTP/WS)
```

### 핵심 컴포넌트

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Listener / TLS Termination** | 클라이언트 연결 수락 및 평문 변환 | TLS 1.3(0-RTT 옵션 주의), OCSP Stapling, ALPN(h2, http/1.1). AWS ALB/NLB, NGINX, Envoy Listener |
| **Authentication Filter** | 토큰·키·인증서 검증 | JWT(RS256/ES256/EdDSA), OAuth 2.0 Introspection(RFC 7662), mTLS Peer Cert(SPIFFE), HMAC API Key(Header `X-API-Key`) |
| **Routing Engine** | 경로/속성 기반 백엔드 매핑 | Trie-based Path Matcher(Envoy), Radix Tree(Kong), Spring `PathRoutePredicateFactory` |
| **Service Discovery Adapter** | 서비스 위치 동적 해석 | K8s Endpoints/IngressClass, Consul Catalog, Eureka, DNS SRV Records |
| **Policy Engine** | 인가·Quota·Rate-Limit | OPA(Rego, e.g. `allow { input.token.scope == "read" }`), Token Bucket(4 r/w burst), Sliding Window Counter |
| **Circuit Breaker / Retry** | 장애 격리·복원력 | Resilience4j, Sentinel(Alibaba), Polly(.NET). Half-Open 상태로 자동 복구, max 3 retry with `Retry-After` |
| **Observability Adapter** | 메트릭·로그·트레이스 | Prometheus Counter/Histogram(`http_requests_total{code}`), OpenTelemetry, Fluent Bit -> Loki/ELK |
| **Transformation Engine** | 프로토콜·페이로드 변환 | JSON->XML(Apache Camel), gRPC->REST(grpc-gateway), GraphQL Federation(Apollo Router), SOAP->REST |

### JWT 검증 알고리즘의 핵심

`Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIs...`(RS256 기준)을 예로 들면, 게이트웨이는 다음을 순차 검증한다.

① **Header 디코딩(Base64URL)**: `alg`, `typ`, `kid`(Key ID) 추출
② **JWK 캐시 조회**: `kid`에 해당하는 공개키를 `https://auth.example.com/.well-known/jwks.json`에서 TTL 동안 캐시(예: Redis, 600s). **Key Rotation** 시 즉시 무효화하기 위해 `Cache-Control: no-cache, max-age=300` 적용.
③ **Signature 검증**: `RSASSA-PKCS1-v1_5(SHA256, payload, publicKey)` 결과가 JWT 3번째 파트와 일치하는지 확인. **이때 `alg=none` 알고리즘 혼동 공격(Algorithm Confusion Attack)을 방어하기 위해 `alg` 화이트리스트(`RS256`, `ES256`)를 반드시 명시적으로 검증**한다(CVE-2015-9235, Auth0 jsonwebtoken 4.2.x 사례).
④ **Claim 검증**: `exp`(현재 < exp), `nbf`(현재 ≥ nbf), `iat` sanity, `iss`(`https://auth.example.com` 일치), `aud`(`api://order-service` 포함), `sub` 필수, `scope`/`scp` 형식 검증.
⑤ **Revocation 확인**: `jti`(JWT ID)가 Blocklist(Redis SET, SADD)에 존재하면 401. 또는 OAuth 2.0 Token Introspection(RFC 7662)을 POST 호출(레이턴시 +20ms, 캐시 60s 권장).

- **📢 섹션 요약 비유**: 게이트웨이의 Filter Chain은 **공항의 7단계 보안 검색대**와 같다. 신분증 확인(JWT) -> 수하물 X-ray(Validation) -> 보안 검색(Authorization) -> 탑승구 배정(Routing) -> 비행기(WAS) 순으로, 각 단계가 별도 모듈로 분리되어 있어 한 단계가 느려도 다른 단계는 병렬화할 수 있다.

---

## Ⅲ. 비교 및 연결

### 1) API Gateway vs Service Mesh vs Load Balancer

| 구분 | **API Gateway (Edge)** | **Service Mesh (Sidecar, e.g. Istio/Envoy)** | **L4/L7 Load Balancer (NGINX/HAProxy/ALB)** |
| :--- | :--- | :--- | :--- |
| 위치 | North-South(외부↔내부) | East-West(서비스↔서비스) | North-South 단일 또는 이중화 |
| 주요 기능 | 라우팅 + 인증 + API 정책 | mTLS, Retry, Circuit Breaker, Telemetry | L4(L4)/L7(Path/Host) 트래픽 분배 |
| 인증 주체 | 사용자 토큰(JWT/OAuth2) | 워크로드 ID(SPIFFE/mTLS) | 보통 없음(Pass-Through) |
| 데이터 평면 | 단일 또는 다중 AZ HA | 모든 Pod 옆 Sidecar(Envoy) | Stateless/Stateful Pair |
| SLA 책임 | 99.95~99.99% | 내부 latency 5% 이내 | 99.99% (L4) / 99.95% (L7) |
| 한계 | SPOF 가능(HA로 보완) | Side
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 457 / 600

<- **이전**: [456. 스트랭글러 패턴 레거시 전환](/studynote/11_design_supervision/06_exam_summary/456_strangler_pattern)
**다음**: [458. 서비스 디스커버리 레지스트리 패턴](/studynote/11_design_supervision/06_exam_summary/458_service_discovery/) ->

---
