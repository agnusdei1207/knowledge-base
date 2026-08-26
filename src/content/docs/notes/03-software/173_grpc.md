---
sidebar:
  order: 173
  label: "173. gRPC"
  badge:
    text: "미출 · 70%"
    variant: note
title: "gRPC (gRPC)"
date: "2026-08-26T10:25:00+09:00"
tags:
  - "notes-software"
weight: 173
extra:
  question_no: "173"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "내부 원격 호출과 스트리밍 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **gRPC**: HTTP/2 전송 계층과 Protocol Buffers(Protobuf) 이진 직렬화를 결합하여 초고속 마이크로서비스 RPC 통신을 지원하는 오픈소스 프레임워크.
- **Protocol Buffers (Protobuf)**: 언어 중립적인 `.proto` IDL 명세서로부터 직렬화 코드를 자동 생성하는 구글의 초경량 이진 직렬화 포맷.

</details>

- 정의/개념: HTTP/2 전송 계층과 Protobuf 이진 직렬화를 기반으로 **마이크로서비스 간의 초고속 원격 프로시저 호출과 스트리밍을 제공하는 고성능 RPC 프레임워크**
- 배경/필요성: REST/JSON 기반 내부 통신 시 발생하는 **무거운 텍스트 직렬화 오버헤드, HTTP/1.1 HoL 블로킹 및 런타임 타입 오류 해결 불가**

#### 한줄 요약
- HTTP/2 멀티플렉싱과 Protobuf 이진 직렬화로 마이크로서비스 내부 통신 속도를 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multiplexing**: 단일 TCP 커넥션 위에서 수많은 양방향 요청/응답 스트림을 동시 교차 전송하는 HTTP/2 핵심 기능.
- **Deadline Propagation**: 호출 체인 전체에 타임아웃 기한을 전파하여 특정 구간 지연 시 하위 요청을 즉시 자동 취소하는 메커니즘.

</details>

- 단일 TCP 연결에서 다중 요청을 동시 교차 전송하는 **HTTP/2 멀티플렉싱**
- JSON 대비 5~10배 빠르고 페이로드 크기를 대폭 압축하는 **Protobuf 이진 직렬화**
- `.proto` 단일 파일에서 다국어 클라이언트/서버 스텁 코드를 자동 생성하는 **Polyglot 지원**

#### 한줄 요약
- HTTP/2 전송, Protobuf 이진 압축, 다국어 코드 자동 생성을 통해 고성능 내부 통신을 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **gRPC 4대 통신 계층**: IDL Layer(`.proto`), Code Generation(`protoc`), Channel/Stub(클라이언트 프록시), Server Runtime.

</details>

```text
[gRPC 프로토콜 버퍼 및 HTTP/2 통신 아키텍처]
|-- 1. Interface Definition Layer: `service.proto` (강타입 RPC 명세 정의)
|-- 2. Code Generation Layer: `protoc` 컴파일러 -> Java / Go / Python Stub 자동 생성
`-- 3. Client Channel & Stub Layer (클라이언트 애플리케이션)
    |-- Client Stub (로컬 메서드 호출 추상화)
    `-- Channel (HTTP/2 Multiplexing Connection Pool, TLS 관리)
        `-- (Protobuf 이진 패킷 전송: HTTP/2 Binary Framing)
`-- 4. Server Runtime Layer (gRPC Server)
    |-- Netty / HTTP/2 Server Handler (이진 패킷 역직렬화)
    `-- Service Implementation (실제 비즈니스 서비스 로직 실행)
```

선의 의미: 계층 및 `.proto` 명세로부터 생성된 Client Stub이 Channel을 통해 HTTP/2 이진 패킷을 서버로 전송하여 비즈니스 로직을 실행하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| Protobuf IDL | Service, RPC Method, Message의 **필드 번호·데이터 타입 엄격 선언** | `.proto` 파일 규격 |
| 코드 생성기 (protoc)| `.proto`를 컴파일하여 **다국어(Java, Go, C++) Stub 코드 자동 생성** | 컴파일 타임 검증 |
| 채널 및 스텁 (Stub) | 네트워크 통신을 은닉하고 **로컬 함수 호출 인터페이스 및 HTTP/2 채널 연결 관리**| 프록시 추상화 |
| 서버 런타임 (Server)| 수신된 이진 패킷을 역직렬화하여 **해당 서비스 핸들러 메서드로 디스패치 및 회신** | 비동기 고성능 서버 |

#### 한줄 요약
- Protobuf IDL, protoc 컴파일러, Channel/Stub, Server Runtime이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **gRPC RPC 통신 5단계**: 채널/TLS 수립 $\to$ Deadline/메타데이터 전파 $\to$ Protobuf 이진 직렬화 $\to$ 서버 핸들러 처리 $\to$ Status/Trailer 회신.

</details>

```text
클라이언트의 gRPC 원격 메서드 호출
        │
   1. [채널 및 세션 수립] HTTP/2 다중화 커넥션을 통해 타깃 서버와 TLS 세션 수립
        │
   2. [Deadline 전파] 요청 메타데이터에 인증 토큰(JWT) 및 타임아웃 기한(Deadline) 주입
        │
   3. [이진 직렬화 및 전송] Client Stub이 요청 객체를 Protobuf 이진 바이트로 압축하여 스트림 전송
        │
   4. [서버 로직 처리] 서버가 이진 패킷을 역직렬화하고 비즈니스 핸들러 연산 수행
        │
   처리 결과와 함께 gRPC Status Code(OK) 및 Trailer 메타데이터를 클라이언트에 회신
```

#### 한줄 요약
- 세션 수립 → Deadline 전파 → 이진 직렬화 → 서버 로직 처리 → Status 회신 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **4대 gRPC 통신 패턴**: Unary(단일 요청-단일 응답), Server Streaming(단일 요청-연속 응답), Client Streaming(연속 요청-단일 응답), Bidirectional Streaming(양방향 연속 스트리밍).

</details>

| 비교 항목 | REST API (JSON) | gRPC (Protocol Buffers) |
|:---|:---|:---|
| 데이터 포맷 및 크기 | **JSON 텍스트 포맷 (상대적 대용량)** | **Protobuf 이진 포맷 (JSON 대비 30~50% 용량)** |
| 통신 성능 및 속도 | 텍스트 직렬화 오버헤드로 상대적 느림 | **초고속 이진 직렬화 및 HTTP/2 멀티플렉싱** |
| 계약 및 타입 검증 | OpenAPI/Swagger (약한 결합, 런타임 오류) | **`.proto` 강타입 계약 (컴파일 타임 오류 차단)** |
| 스트리밍 지원 | 단방향 SSE 또는 별도 웹소켓 구축 필요 | **단항, 서버/클라이언트/양방향 스트리밍 네이티브**|
| 최적 적용 영역 | **대외 공개 Web API, 모바일 프론트엔드 연동** | **마이크로서비스 내부(East-West) 초고속 통신** |

#### 한줄 요약
- 대외 오픈 API는 REST, 마이크로서비스 내부 통신과 고성능 스트리밍은 gRPC를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **L4 Load Balancing Trap**: HTTP/2가 단일 TCP 커넥션을 계속 유지하므로, L4 로드밸런서를 쓰면 모든 요청이 특정 1대 서버로만 쏠리는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| HTTP/2 단일 연결 유지로 L4 로드밸런싱 실패 (트래픽 쏠림) | **Envoy 프록시 또는 Istio 서비스 메시 기반 L7 로드밸런싱 적용** | 파드 단위 완벽한 부하 분산 달성 |
| 웹 브라우저의 HTTP/2 프레이밍 미지원으로 프론트 연동 불가 | **`gRPC-Web` 프록시 도입 또는 Envoy gRPC-JSON 트랜스코딩** | 브라우저 직접 호출 지원 |
| 필드 삭제 후 동일 번호 재사용 시 구버전 클라이언트 충돌 | **`.proto` 파일에 `reserved` 키워드를 명시하여 번호 재사용 금지** | 하위 호환성 영구 보장 |
| 연쇄 호출 중 지연 발생 시 서버 스레드 고갈 | **gRPC `Context`에 명시적 `Deadline`을 설정하고 하위 전파** | 무한 대기 및 연쇄 장애 차단 |

#### 한줄 요약
- L7 로드밸런싱 도입, gRPC-Web 프록시, reserved 키워드, Deadline 전파로 운영한다.

## Ⅶ. 결론

- 대규모 마이크로서비스 환경에서 내부(East-West) 통신 지연을 극소화하기 위해 **HTTP/2 기반의 Protobuf gRPC 프레임워크를 전사 서비스 간 통신 표준으로 구축**하고, **Envoy/Istio L7 로드밸런싱과 Deadline 컨텍스트 전파**를 결합하여 고성능 엔터프라이즈 MSA 백본 완성

#### 한줄 요약
- gRPC는 HTTP/2 전송과 Protobuf 이진 직렬화를 통해 컴파일 타임 강타입 검증과 초저지연 통신을 실현하는 현대 마이크로서비스의 핵심 RPC 기술이다.