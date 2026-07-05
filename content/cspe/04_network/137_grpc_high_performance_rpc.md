---
title: "gRPC 고성능 RPC (gRPC High Performance RPC)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 137
---

# 📖 【암기용】 개념 완전 이해

> 목적: gRPC를 HTTP/2 기반 RPC와 protobuf 계약 중심 통신 방식으로 이해하게 만든다.

## 한눈에
- **개요**: HTTP/2와 Protocol Buffers를 사용하는 RPC 프레임워크
- **왜 필요한가**: 마이크로서비스는 서비스 간 호출이 많고 API 계약이 자주 바뀐다. gRPC는 `.proto` 계약에서 클라이언트·서버 코드를 생성해 호출 규약을 일치시킨다.
- **핵심 직관**: REST가 주소와 JSON 문서를 주고받는 방식이라면, gRPC는 미리 합의한 함수 서명과 바이너리 메시지로 원격 함수를 호출한다.

## 깊이 이해
- **배경·문제의식**: JSON/HTTP API는 언어별 타입 불일치, 스키마 문서와 코드 불일치, 스트리밍 처리 부담이 생긴다. gRPC는 IDL 기반 계약과 HTTP/2 stream으로 이를 줄인다.
- **작동 원리**: 개발자는 `.proto`에 service와 message를 작성한다. protoc가 stub을 생성하고, 클라이언트는 stub 메서드를 호출해 HTTP/2 stream으로 서버와 통신한다.
- **비유**: 일반 우편이 자유 양식 편지라면, gRPC는 표준 양식 신청서를 작성해 전용 창구에 제출하는 방식이다.
- **구체 예시**: unary RPC는 `GetUser(Request) returns (User)`처럼 1회 요청·응답을 처리하고, bidirectional streaming은 양쪽이 여러 메시지를 같은 HTTP/2 연결에서 교환한다.
- **흔한 오해·주의점**: gRPC는 브라우저 직접 호출에 제약이 있어 gRPC-Web 또는 REST gateway가 필요할 수 있다.

## 연결 개념
- HTTP/2 — multiplexing, flow control, header compression 기반
- Protocol Buffers — schema-first binary serialization
- Service Mesh — mTLS, retry, timeout, observability 적용 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: gRPC 답안은 protobuf 계약, HTTP/2 stream, 호출 유형, 운영 통제 지표를 함께 구성해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: gRPC는 `.proto` IDL을 기준으로 HTTP/2 stream 위에서 원격 메서드를 호출하는 RPC 프레임워크이다.
> 2. **가치**: protobuf binary message, multiplexing, deadline, streaming으로 서비스 간 호출 계약과 전송을 표준화한다.
> 3. **판단 포인트**: 내부 서비스 호출, streaming 요구, 언어 다양성, 브라우저 접근, observability 수준으로 적용 여부를 결정한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RPC 구조 이해 확인 | .proto, stub, channel, HTTP/2, protobuf | JSON REST와 단순 속도 비교 |
| 호출 패턴 판단 확인 | unary, server/client streaming, bidi streaming | streaming 유형 누락 |
| 운영 통제 확인 | deadline, retry, status code, tracing | timeout 없는 호출 설계 |

> 요약: 출제자는 gRPC를 계약 기반 내부 통신 구조로 보고 적용 조건과 운영 통제까지 확인한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **gRPC 고성능 RPC** | gRPC 고성능 RPC (gRPC High Performance RPC)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: HTTP/2 기반 RPC
- 배경: 마이크로서비스 간 JSON API는 타입 불일치와 문서·코드 불일치가 발생하기 쉬움
- 필요성: `.proto` 계약과 generated stub으로 다언어 서비스 호출 규약을 통일함
- 판단 기준: p95 latency, payload size, deadline violation, error status, trace coverage로 검증

---

## Ⅱ. 구조 및 구성요소

```text
.proto contract -> protoc generated stub -> gRPC channel
-> HTTP/2 stream -> Server handler -> protobuf response
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| .proto | service와 message 계약 작성 | versioning과 field number 관리 |
| Stub | 클라이언트·서버 코드 생성 | 언어별 SDK 제공 |
| Channel | 연결, TLS, load balancing 관리 | long-lived connection |
| HTTP/2 Stream | multiplexing과 flow control | unary·streaming 호출 지원 |
| Interceptor | 인증, 로깅, tracing 적용 | 공통 정책 삽입 |

> 요약: gRPC는 `.proto` 계약에서 stub을 생성하고 HTTP/2 stream으로 원격 메서드 호출을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client stub 호출 -> protobuf 직렬화 -> HTTP/2 stream 생성
-> Server handler 처리 -> protobuf 응답 -> status/trailer 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 stub 메서드 호출 | request schema validation |
| 2 | protobuf 메시지를 직렬화 | payload size, serialization error |
| 3 | HTTP/2 stream으로 요청 전송 | stream reset, flow-control stall |
| 4 | 서버 handler가 비즈니스 로직 수행 | deadline, CPU time |
| 5 | 응답과 gRPC status를 trailer로 반환 | status code, retry policy |

> 요약: gRPC는 stub 호출을 protobuf 메시지와 HTTP/2 stream으로 변환하고 status/trailer로 결과를 관리한다.

---

## Ⅳ. 특징

| 구분 | REST/JSON API | gRPC | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 계약 | OpenAPI 문서 중심 | `.proto` IDL 중심 | schema breaking change 탐지 |
| 전송 | HTTP/1.1 또는 HTTP/2 | HTTP/2 필수 | stream multiplexing |
| 메시지 | JSON text | protobuf binary | payload byte, CPU decode |
| 브라우저 | 직접 호출 용이 | gRPC-Web 필요 | public API 여부 |

> 요약: gRPC는 내부 서비스 간 계약·streaming에 적합하나 공개 웹 API는 REST 또는 gRPC-Web을 함께 검토해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | gRPC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | REST/JSON | RPC/protobuf | 내부 서비스 간 타입 계약 필요 |
| 비용/성능 | 텍스트 payload | binary payload | payload 크기, CPU decode 비용 |
| 운영/위험 | HTTP 도구 활용 범위 넓음 | HTTP/2·trailer 관측 필요 | APM·proxy 지원 여부 |

> 요약: gRPC 선택은 호출량보다 계약 엄격성, streaming 요구, 운영 도구 지원 여부가 결정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 계약 깨짐 | field 삭제·번호 재사용 | backward compatible schema rule | breaking change count |
| 지연 누적 | deadline·retry 미설정 | timeout, retry budget, circuit breaker | deadline exceeded rate |
| 관측 누락 | HTTP/2 stream과 trailer 미수집 | OpenTelemetry interceptor | trace coverage, status distribution |

> 요약: gRPC 운영 리스크는 계약 변경, 지연 통제, 관측성으로 분리해 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 호출 지연 | p95 latency SLA 충족 | APM, server histogram |
| 오류 | non-OK status rate 1% 이하 | gRPC status metric |
| 계약 품질 | breaking change 0건 | buf lint, schema registry |

> 요약: gRPC 성공 여부는 지연, status 오류율, 계약 호환성 검사를 함께 만족해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 내부 API는 `.proto`와 schema registry를 기준으로 관리하고 field number 재사용을 금지한다.
2. 모든 호출에 deadline, retry budget, idempotency 정책을 명시하고 service mesh에서 mTLS를 적용한다.
3. OpenTelemetry interceptor로 trace id, method, status, latency, payload size를 수집한다.

**결론 (2줄):**
- 기술사 판단: 내부 마이크로서비스와 streaming 호출에는 gRPC를 선택하고, 외부 공개 API는 REST gateway 또는 gRPC-Web을 병행한다.
- 향후 방향: gRPC는 service mesh, OpenTelemetry, schema registry와 결합해 내부 플랫폼 표준 RPC로 정착한다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "gRPC를 설명하시오" | stub-protobuf-HTTP/2 흐름 | REST 대비 계약·streaming 차이 |
| 요구사항 명시형 | "MSA 통신 방안을 제시하시오" | deadline, retry, tracing 설계 | 계약 호환성, p95 latency, status rate |

> 요약: 설명형은 RPC 구조를, 방안형은 MSA 운영 통제와 계약 관리 지표를 중심으로 전환한다.
