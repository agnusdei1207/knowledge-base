---
sidebar:
  order: 173
  label: "173. gRPC (gRPC)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "gRPC (gRPC)"
date: "2026-08-10T10:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **gRPC (gRPC Remote Procedure Calls)**: 구글(Google)이 개발한 고성능 오픈소스 RPC 프레임워크로, HTTP/2와 Protocol Buffers를 기반으로 마이크로서비스 간의 초고속 양방향 통신을 지원하는 기술.
- **Protocol Buffers (Protobuf)**: XML이나 JSON 대비 크기가 절반 이하로 작고 파싱(Parsing) 속도가 수십 배 빠른, 구글이 개발한 이진(Binary) 직렬화 데이터 포맷.
- **IDL (Interface Definition Language)**: 클라이언트와 서버가 주고받을 데이터 구조와 메서드를 언어에 구애받지 않고 명확하게 정의하는 `.proto` 파일 규격.

</details>

- 정의/개념: HTTP/2의 멀티플렉싱(Multiplexing) 성능과 Protobuf의 직렬화 효율을 결합하여 이기종 언어로 작성된 마이크로서비스(MSA) 간의 함수를 로컬 함수처럼 직접 호출하는 원격 프로시저 호출 프레임워크인 **gRPC**
- 배경/필요성: REST API(HTTP/1.1 + JSON) 체계에서 발생하는 무거운 페이로드(Payload) 크기, 텍스트 파싱 지연, 단방향 통신의 한계를 극복하고 내부 네트워크 연계 성능을 극대화하기 위한 요구성

#### 한줄 요약

- 공통 `.proto` 설계도에서 각 언어의 송신·수신 코드를 만들어 다른 서버의 함수를 타입이 정해진 로컬 함수처럼 호출한다.

## Ⅱ. 특징 (gRPC 3대 핵심 기술 요소)

<details><summary>핵심 용어</summary>

- **Deadline / Timeout (기한/타임아웃)**: gRPC 호출 시 클라이언트가 "언제까지 응답이 안 오면 호출을 취소하겠다"고 명시하는 시간 제약으로, MSA 환경에서 무한 대기(Cascading Failure)를 방지하는 방어 기제.

</details>

- **HTTP/2 Transport (바이너리 프레이밍, 멀티플렉싱, 헤더 압축, 서버 푸시 지원)**
- **Protocol Buffers Serialization (JSON 텍스트 포맷 대비 작고 빠른 이진 직렬화 메커니즘)**
- **Polyglot & Code Generation (하나의 `.proto` 파일에서 Java, Go, Python 등 다국어 클라이언트/서버 스텁(Stub) 코드 자동 생성)**

#### 한줄 요약

- 한 연결에서 여러 통화를 동시에 처리하되 호출자가 기다릴 시간을 넘기면 하위 서비스까지 취소를 전달해 불필요한 작업을 멈춘다.

## Ⅲ. 구조 및 구성요소 (gRPC 클라이언트-서버 통신 구조)

<details><summary>핵심 용어</summary>

- **Stub (스텁)**: `.proto` 파일을 컴파일(protoc)하여 자동 생성된 클라이언트 측 프록시 객체로, 네트워크 통신과 직렬화의 복잡성을 숨기고 마치 로컬 메서드를 부르는 것처럼 보이게 하는 대리자.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        gRPC Client-Server Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│                      [ .proto (IDL Contract) ]                         │
│                                  │ (Code Generation)                   │
│                                  ▼                                     │
│ [Client App (Go)]                                [Server App (Java)]   │
│   │                                                ▲                   │
│   ▼                                                │                   │
│ [gRPC Client Stub] ──(HTTP/2 + Protobuf)──► [gRPC Server Skeleton]     │
│ (직렬화, 압축, 라우팅)                       (역직렬화, 비즈니스 매핑) │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 언어 독립적인 `.proto` 명세로부터 생성된 클라이언트 스텁과 서버 스켈레톤(Skeleton) 사이를 HTTP/2 기반의 Protobuf 바이너리 메시지가 오가며 고속으로 데이터를 교환하는 구조.

| 구성요소 | 핵심 역할 및 기능 | 실무 적용 |
|:---|:---|:---|
| **Protobuf IDL** | **서비스(RPC)와 메시지(Message) 구조를 정의한 계약서**| `user.proto` 파일 작성 |
| **protoc (컴파일러)**| **IDL을 읽어 특정 언어용 스텁/스켈레톤 코드 자동 생성**| Go, Java용 소스코드 생성 |
| **gRPC Channel** | **클라이언트와 서버 간의 HTTP/2 기반 장기 지속 연결** | 다중 요청을 1개 채널로 전송 |
| **Server Runtime** | **바이너리 요청 수신 $\rightarrow$ 역직렬화 $\rightarrow$ 비즈니스 로직(Handler) 연결** | gRPC 프레임워크 내장 처리 |

#### 한줄 요약

- IDL이 통화 규격, 스텁이 송수화기, 채널이 회선, Runtime이 교환기, Handler가 실제 업무 담당자 역할을 한다.

## Ⅳ. 흐름도 (gRPC 양방향 스트리밍 흐름)

<details><summary>핵심 용어</summary>

- **Bidirectional Streaming (양방향 스트리밍)**: 클라이언트와 서버가 하나의 HTTP/2 연결(Connection) 위에서 독립적인 데이터 스트림을 비동기적으로 동시에 주고받는 gRPC의 가장 강력한 통신 모델.

</details>

```text
[Client]                                         [Server]
   │                                                │
   ├─ 1. HTTP/2 Connection Establishment (TLS) ────►│
   │                                                │
   ├─ 2. Send Stream Request (Stream A: Msg 1) ────►│ (Process Msg 1)
   │                                                │
   ├─ 3. Send Stream Request (Stream A: Msg 2) ────►│ (Process Msg 2)
   │                                                │
   │◄── 4. Send Stream Response (Stream B: Res 1) ──┤ (Reply for Msg 1)
   │                                                │
   ├─ 5. Client Close Stream ──────────────────────►│
   │                                                │
   │◄── 6. Send Stream Response (Stream B: Res 2) ──┤ (Reply for Msg 2)
   │◄── 7. Server Close Stream (Trailers) ──────────┤
```

### 동작 원리

1. **Connection**: 클라이언트가 서버와 TLS 기반 HTTP/2 롱 커넥션 채널(Channel) 오픈.
2. **Stream Initiate**: 클라이언트가 데이터를 스트리밍으로 전송 시작 (요청-1, 요청-2).
3. **Concurrent Reply**: 서버도 요청이 모두 끝나길 기다리지 않고, 처리되는 대로 즉각 스트리밍 응답 전송(응답-1 반환).
4. **Graceful Close**: 양측이 더 이상 보낼 데이터가 없음을 알리고(`Close`) 스트림을 안전하게 닫음 (**스트리밍 통신 완결**).

#### 한줄 요약

- 호출 객체는 스텁에서 이진 메시지가 되고 서버 Handler의 결과는 다시 객체로 복원되며 기한이 지나면 같은 취소 문맥이 전체 경로에 전달된다.

## Ⅴ. 종류 및 비교 (REST API 대 gRPC 1:1 비교)

<details><summary>핵심 용어</summary>

- **Unary RPC (단항 RPC)**: REST API처럼 1개의 요청을 보내면 1개의 응답을 받는 가장 기본적이고 단순한 gRPC 통신 방식.

</details>

| 비교 항목 | REST API (JSON) | gRPC (Protobuf) |
|:---|:---|:---|
| **통신 프로토콜** | **HTTP/1.1 (기본)** | **HTTP/2 (필수 강제, 멀티플렉싱)** |
| **페이로드(Payload)**| **JSON (텍스트 기반, 파싱 속도 느림, 용량 큼)**| **Protobuf (바이너리, 파싱 초고속, 용량 50% 축소)**|
| **계약(Contract)** | OpenAPI(Swagger) 등 선택적/약한 결합 | **`.proto` 기반 강력한 타입 검증 강제 결합** |
| **브라우저 지원** | 네이티브 지원 (Chrome 등 직접 호출 가능) | **브라우저 직접 호출 불가 (gRPC-Web 프록시 필요)**|

#### 한줄 요약

- 내부 서비스의 타입 계약과 연속 메시지가 중요하면 gRPC를, 브라우저와 외부 소비자의 접근성과 웹 캐시가 중요하면 REST를 선택한다.

## Ⅵ. 실무 고려사항 및 대책 (gRPC 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

- **Load Balancing Issue**: HTTP/2는 장기 지속 연결(Long-Lived Connection)을 맺으므로, L4(TCP) 로드밸런서를 쓰면 트래픽 분산이 안 되고 특정 서버로 요청이 몰리는 연결 쏠림 현상.

</details>

| 3대 gRPC 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. L4 로드밸런싱 실패** | HTTP/2의 단일 Connection 유지 특성 | **Envoy, Istio 등 L7(Application) 로드밸런서 도입**|
| **2. 프론트엔드 연동 불가**| 브라우저는 HTTP/2 프레이밍 직접 조작 불가| **gRPC-Web 또는 REST-to-gRPC Gateway (Envoy) 구축**|
| **3. 구버전 스키마 충돌** | 필드를 삭제한 뒤 동일 필드 번호 재사용 | **`reserved` 키워드를 사용하여 번호 재사용 원천 금지**|

> 사례: **토스 / 배달의민족 마이크로서비스 내부(East-West) 통신 속도 개선을 위한 REST $\rightarrow$ gRPC 대규모 마이그레이션**

#### 한줄 요약

- 모델 추론 호출에 짧은 기한을 두고 취소를 하위 처리까지 전파하면 느린 요청이 연결과 연산 장치를 계속 차지하지 않는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **gRPC 수립 기준**: `.proto` 계약(IDL) 관리, HTTP/2 인프라 호환성(L7 로드밸런서), Deadline(기한) 전파 및 하위 호환성 유지 룰(reserved)에 의거한 체계.

</details>

- **gRPC 수립 기준**에 따라 Cloud-Native MSA 백엔드 내부 망 설계 시 **Protobuf 직렬화 및 HTTP/2 스트리밍** 필수 적용

#### 한줄 요약

- 타입 계약과 스트리밍이 필요한 내부 통신은 gRPC로 구성하되 모든 호출에 기한·취소·호환성 정책을 함께 적용해야 한다.
