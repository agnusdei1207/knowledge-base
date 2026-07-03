---
title: "gRPC (gRPC)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 202
---

# 📖 【암기용】 개념 완전 이해

> 목적: gRPC를 처음 보는 사람도 RPC의 한 구현체로서 어떤 문제를 풀고 내부적으로 어떻게 동작하는지 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: gRPC는 **RPC(Remote Procedure Call, 원격 프로시저 호출)**의 한 구현체로, HTTP/2와 Protocol Buffers(Protobuf)를 결합해 다른 서버의 함수를 내 코드의 메서드처럼 호출할 수 있게 하는 고성능 프레임워크다.
- **왜 필요한가**: 마이크로서비스 내부 통신은 다수의 작은 호출이 반복되어 지연·계약 불일치·언어 혼합 문제가 발생한다. gRPC는 IDL(인터페이스 정의 언어) 기반 코드 생성과 HTTP/2 멀티플렉싱으로 서비스 간 호출을 표준화한다.
- **핵심 직관**: 다른 서버의 함수를 내 코드의 메서드처럼 호출하되, 네트워크 전송·직렬화·스트리밍은 프레임워크가 대신 처리하는 구조다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| RPC (상위 개념) | 원격 서버의 함수를 로컬 함수처럼 호출하는 방식의 통칭 — gRPC는 이를 구현한 프레임워크 중 하나 | "전화로 대신 일 처리를 부탁하는 것" 전체 |
| IDL (`.proto`) | service·rpc·message를 정의하는 언어 중립적 계약 파일 | 각 언어 팀이 함께 보는 설계도면 |
| Stub | `.proto`로부터 언어별로 자동 생성되는 호출용 코드 | 설계도면을 보고 각 나라 언어로 번역된 사용설명서 |
| Protocol Buffers (Protobuf) | 필드를 번호로 태깅해 바이너리로 직렬화하는 데이터 형식 — 필드 이름 없이 번호+값만 전송 | 긴 이름 대신 번호표만 붙여 짐을 빠르게 나르는 것 |
| HTTP/2 멀티플렉싱 | 하나의 TCP 연결 위에서 여러 요청/응답 스트림을 동시에 주고받는 기능 | 전화선 하나로 여러 통화를 동시에 나누는 것 |
| Streaming 모드 | 요청·응답을 1회성이 아니라 스트림으로 주고받는 4가지 통신 패턴(아래 표) | 편지(1회) vs 실시간 통화(계속 흐름) |
| Deadline | 호출이 이 시간 안에 끝나지 않으면 자동으로 실패 처리하는 제한 시간 | 배달 음식 "30분 내 미도착 시 자동 취소" |
| mTLS (상호 TLS 인증) | 클라이언트와 서버가 서로의 인증서를 검증하는 양방향 암호화 인증 | 양쪽 모두 신분증을 보여줘야 통화가 연결되는 것 |

## 깊이 이해

### 왜 gRPC가 나왔나 (배경)
- Google은 내부적으로 "Stubby"라는 RPC 시스템을 오래 사용해 왔고, 이를 공개 표준 기술(HTTP/2, Protobuf) 기반으로 재구성해 2015년 gRPC로 오픈소스화했다.
- REST/JSON은 사람이 읽기 쉽고 웹 생태계와 잘 맞지만, 마이크로서비스 내부처럼 초당 수천 건씩 호출되는 환경에서는 ① 매 응답에 필드 이름을 문자열로 반복 전송하는 오버헤드, ② HTTP/1.1 요청마다 별도 연결이 필요해 생기는 지연이 누적된다. gRPC는 이 두 지점을 각각 Protobuf(이진 직렬화)와 HTTP/2(멀티플렉싱)로 해결한다.

### Protobuf가 왜 작은지 숫자로 확인하기 (워크드 예제)
주문 정보 `{"id":123,"name":"Order-123","amount":50000}`를 전송한다고 하자.
- **JSON**: 위 문자열 그대로 약 44바이트 — 필드 이름(`id`, `name`, `amount`)이 매번 텍스트로 포함된다.
- **Protobuf 바이너리**: 필드는 이름 대신 번호(태그)로 표현된다. `id`(필드 1, int32=123)는 태그 1바이트+값 1바이트=2바이트, `name`(필드 2, 문자열 9자)은 태그 1바이트+길이 1바이트+문자열 9바이트=11바이트, `amount`(필드 3, int64=50000)는 태그 1바이트+값 3바이트=4바이트 — 합계 약 **17바이트**.
- 44바이트 → 17바이트로 **약 61% 축소**된다. 필드 이름 문자열을 아예 전송하지 않고 번호로만 주고받기 때문이다 — 이것이 "payload 30~70% 축소"라는 특징의 실제 원리다.

### 4가지 Streaming 모드 (구체 예제로 구분)
| 모드 | 요청/응답 형태 | 예시 |
|:---|:---|:---|
| Unary | 요청 1개 → 응답 1개 | `GetOrder(id)` — 일반 함수 호출과 동일 |
| Server streaming | 요청 1개 → 응답 여러 개(스트림) | 클라이언트가 한 번 구독하면 서버가 실시간 주식 시세를 계속 흘려보냄 |
| Client streaming | 요청 여러 개(스트림) → 응답 1개 | 대용량 파일을 여러 청크로 나눠 업로드 후 완료 결과 1회 수신 |
| Bidirectional streaming | 요청과 응답이 동시에 스트림 | 채팅 — 양쪽이 동시에 계속 메시지를 주고받음 |

이 4가지가 가능한 이유가 바로 HTTP/2다. HTTP/1.1은 한 연결에서 요청을 순차 처리해 앞선 요청이 늦으면 뒤 요청도 막히는 Head-of-Line Blocking이 있었지만, HTTP/2는 하나의 TCP 연결 위에서 여러 스트림을 독립적으로 동시에 주고받아 이 문제를 없앴다.

### 비유와 흔한 오해
- **비유**: 계약서(`.proto`)에 함수명·인자·반환값을 먼저 적고, 각 팀이 같은 계약서에서 자동 생성된 번역본(Stub)을 가져다 쓰는 방식이다.
- **오해**: gRPC는 외부 브라우저 공개 API의 기본값이 아니다. 브라우저는 HTTP/2 스트림을 gRPC가 요구하는 방식으로 직접 다루지 못해 gRPC-Web이라는 별도 프록시 계층이 필요하고, CORS·디버깅 편의성도 REST보다 떨어진다. 그래서 내부 서비스 간 호출에는 gRPC를, 외부 공개 API에는 REST·GraphQL을 병행하는 것이 일반적이다.

## 연결 개념
- Protocol Buffers — gRPC가 사용하는 IDL·직렬화 형식
- Service Mesh — mTLS·retry·timeout·observability를 통제하는 계층
- REST API — 외부 공개 API로 병행 검토되는 비교 대상

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

- 개요: HTTP/2·Protobuf 기반 RPC 프레임워크
- 배경: MSA 환경은 서비스 간 호출 수가 많고 언어가 혼합되어 계약 검증과 지연 통제가 필요하다.
- 필요성: IDL 기반 Stub 생성과 HTTP/2 stream으로 호출 계약, 연결 재사용, 스트리밍 기준을 제공한다.

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
