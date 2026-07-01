---
title: "gRPC (gRPC)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 202
---

# 📖 【암기용】 개념 완전 이해

> 목적: gRPC를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: HTTP/2와 Protocol Buffers 기반의 고성능 원격 프로시저 호출 프레임워크
- **왜 필요한가**: 마이크로서비스 내부 통신은 다수의 작은 호출이 반복되어 지연·계약 불일치·언어 혼합 문제가 발생한다. gRPC는 IDL 기반 코드 생성과 HTTP/2 multiplexing으로 서비스 간 호출을 표준화한다.
- **핵심 직관**: 다른 서버의 함수를 내 코드의 메서드처럼 호출하되, 네트워크·직렬화·스트리밍은 프레임워크가 맡는 구조이다.

## 깊이 이해
- **배경·문제의식**: REST/JSON은 사람이 읽기 쉽지만 내부 서비스 간 대량 호출에서는 payload 크기와 계약 검증 비용이 커진다.
- **작동 원리**: `.proto` 파일에 service와 message를 정의하면 각 언어별 Stub이 생성된다. 클라이언트 Stub은 메시지를 Protobuf binary로 직렬화해 HTTP/2 stream으로 서버에 전달한다.
- **비유**: 계약서에 함수명·인자·반환값을 먼저 적고, 각 팀이 같은 계약서에서 자동 생성된 호출 코드를 쓰는 방식임.
- **구체 예시**: 결제 서비스가 주문 서비스의 `GetOrder(id)`를 호출할 때 JSON 1KB 응답을 Protobuf 350B 수준으로 줄이고, HTTP/2 연결 1개에서 다중 요청을 처리할 수 있음.
- **흔한 오해·주의점**: gRPC는 외부 브라우저 공개 API의 기본값이 아니다. 브라우저 직접 호출은 gRPC-Web 제약, 프록시, CORS, 디버깅 방식을 함께 설계해야 한다.

## 연결 개념
- Protocol Buffers — gRPC의 IDL·직렬화 형식
- Service Mesh — mTLS, retry, timeout, observability 통제 계층
- REST API — 외부 공개 API 비교 대상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: gRPC는 단순 통신 라이브러리가 아니라, 서비스 계약·직렬화·스트리밍·운영 정책을 묶는 내부 API 표준이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: gRPC는 HTTP/2, Protobuf, IDL Stub을 결합한 원격 프로시저 호출 프레임워크이다.
> 2. **가치**: 다국어 서비스 간 계약 불일치를 줄이고 unary·server streaming·client streaming·bidirectional streaming을 지원한다.
> 3. **판단 포인트**: 내부 MSA 호출에는 적합하나 외부 공개 API는 REST·GraphQL·gRPC-Web 제약을 비교해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MSA 내부 통신 설계 역량 확인 | HTTP/2, Protobuf, Stub, streaming mode | gRPC를 JSON API와 동일 계층으로 단순 비교 |
| 계약 기반 개발 이해 확인 | `.proto`, code generation, backward compatibility | 필드 번호 호환성·버전 정책 누락 |
| 운영 리스크 판단 확인 | timeout, retry, deadline, mTLS, observability | retry 중복 처리와 idempotency 누락 |

> 요약: 이 문제는 gRPC의 기술 요소뿐 아니라 내부 API 표준으로 선택할 조건과 운영 통제를 묻는다.

---

## Ⅰ. 개요 및 필요성

gRPC는 HTTP/2와 Protobuf 기반 RPC 프레임워크이다. MSA 환경은 서비스 간 호출 수가 많고 언어가 혼합되어 계약 검증과 지연 통제가 필요하다. gRPC는 IDL 기반 Stub 생성으로 호출 계약을 고정하고, HTTP/2 stream으로 연결 재사용과 스트리밍을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client App -> Generated Stub -> HTTP/2 Stream -> gRPC Server -> Service Impl
                         +-> Protobuf Message / Deadline / Metadata
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| `.proto` IDL | service, rpc, message 계약 정의 | 필드 번호로 호환성 관리 |
| Stub | 언어별 호출 코드 생성 | Java, Go, Python 등 지원 |
| HTTP/2 | multiplexing, header compression | 연결 1개에서 다중 stream |
| Metadata | 인증 토큰, trace id 전달 | mTLS·JWT 연계 |

> 요약: gRPC는 IDL 계약, Stub 코드, HTTP/2 전송, metadata 통제로 서비스 호출을 표준화한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
proto 작성 -> Stub 생성 -> 요청 직렬화 -> HTTP/2 전송 -> 서버 실행 -> 응답 역직렬화
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | `.proto` service와 message 정의 | breaking change 0건 |
| 2 | Stub 생성 및 클라이언트 호출 | compile-time contract 검증 |
| 3 | Protobuf binary 직렬화 후 HTTP/2 stream 전송 | payload size, stream error 측정 |
| 4 | 서버 구현체 실행 후 status code 반환 | p95 지연 100ms 이하, error rate 1% 이하 |

> 요약: gRPC는 계약 정의에서 코드 생성, binary 전송, status 기반 오류 처리까지 일관된 호출 흐름을 제공한다.

---

## Ⅳ. 특징

| 구분 | REST/JSON | gRPC | 판단 포인트 |
|:---|:---|:---|:---|
| 계약 | OpenAPI 문서 기반 | `.proto` IDL 기반 | 컴파일 시 계약 검증 필요 시 gRPC |
| 전송 | HTTP/1.1 또는 HTTP/2 | HTTP/2 기본 | 동시 stream 100개 이상 내부 호출 |
| 데이터 | Text JSON | Binary Protobuf | payload 30~70% 축소 기대 |
| 외부 연계 | 브라우저·파트너 친화 | gRPC-Web 또는 gateway 필요 | 공개 API는 REST 병행 검토 |

> 요약: gRPC는 내부 서비스 호출 계약과 전송 효율을 중시할 때 적합하며, 외부 공개 채널은 별도 gateway가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | REST endpoint | RPC method + proto | 내부 서비스 20개 이상, 다국어 3종 이상 |
| 비용/성능 | JSON parsing | Protobuf binary | payload 1KB 이상 반복 호출, p95 100ms 목표 |
| 운영/위험 | URL별 정책 | method별 deadline·retry | deadline 300ms, retry 2회 이하 정책 가능 |

> 요약: gRPC는 내부 고빈도 호출과 계약 자동 생성이 REST 문서 관리보다 큰 가치일 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 호환성 파손 | field number 재사용 | reserved field, buf breaking check | breaking change 0건 |
| 재시도 중복 | retry와 비멱등 메서드 결합 | idempotency key, retry policy 제한 | duplicate transaction 0건 |
| 관측성 부족 | binary payload 디버깅 제약 | OpenTelemetry, server reflection 제한 운영 | trace coverage 95% 이상 |

> 요약: gRPC 운영 리스크는 계약 호환성, 재시도 중복, binary 관측성으로 압축된다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 100ms 이하 | APM, OpenTelemetry |
| 오류 | gRPC status error 1% 이하 | method metric |
| 계약 | proto breaking change 0건 | CI buf lint, contract test |

> 요약: 도입 효과는 지연, status 오류율, proto 계약 검증으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 내부 API는 `.proto` schema registry와 CI `buf lint/breaking`으로 field number 재사용을 차단함.
2. method별 deadline 300ms, retry 2회 이하, circuit breaker를 적용하고 비멱등 메서드는 idempotency key를 요구함.
3. OpenTelemetry trace id를 metadata로 전달하고 service mesh mTLS로 서비스 간 인증을 적용함.

**결론 (2줄):**
- 기술사 판단: 내부 MSA 고빈도 호출은 gRPC, 외부 파트너·브라우저 공개 API는 REST 또는 GraphQL을 병행함.
- 향후 방향: gRPC는 service mesh, xDS, OpenTelemetry와 결합해 플랫폼 표준 통신 계층으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "gRPC를 설명하시오" | proto, Stub, HTTP/2, status 흐름 | REST 대비 계약·전송·외부 공개 차이 |
| 요구사항 명시형 | "MSA 통신 방안을 제시하시오", "REST와 비교하시오" | deadline, retry, streaming, mTLS 적용 | 선택 기준, 호환성 리스크, 운영 지표 |

> 요약: 설명형은 구성 원리, 비교·방안형은 내부 통신 표준과 REST 병행 전략으로 목차를 조정한다.
