---
sidebar:
  order: 173
  label: "173. gRPC"
  badge:
    text: "미출 · 70%"
    variant: note
title: "gRPC (gRPC)"
date: "2026-08-26T13:17:01+09:00"
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
- 배경/필요성: 내부 호출에 텍스트 JSON과 HTTP/1.1을 쓰면 호출마다 직렬화 비용과 연결당 한 요청이라는 제약이 반복되므로, IDL로 계약을 고정해 이진 메시지로 줄이고 HTTP/2 스트림에 다중화하는 통신 계층을 서비스 간(East-West) 구간에 따로 둘 필요

#### 한줄 요약
- HTTP/2 멀티플렉싱과 Protobuf 이진 직렬화로 마이크로서비스 내부 통신 속도를 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multiplexing**: 단일 TCP 커넥션 위에서 수많은 양방향 요청/응답 스트림을 동시 교차 전송하는 HTTP/2 핵심 기능.
- **Deadline Propagation**: 남은 호출 기한을 하위 RPC에 전달해 시간 예산을 공유하는 메커니즘.

</details>

- 단일 TCP 연결에서 다중 요청을 동시 교차 전송하는 **HTTP/2 멀티플렉싱**
- 필드 번호 기반의 간결한 **Protobuf 이진 직렬화**
- `.proto` 단일 파일에서 다국어 클라이언트/서버 스텁 코드를 자동 생성하는 **Polyglot 지원**

#### 한줄 요약
- HTTP/2 전송, Protobuf 이진 압축, 다국어 코드 자동 생성을 통해 고성능 내부 통신을 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **gRPC 4대 통신 계층**: IDL Layer(`.proto`), Code Generation(`protoc`), Channel/Stub(클라이언트 프록시), Server Runtime.

</details>

```text
[gRPC 프로토콜 버퍼 및 HTTP/2 통신 아키텍처]
|-- Interface Definition Layer
|-- Code Generation Layer
|-- Client Channel & Stub Layer
    |-- Client Stub (로컬 메서드 호출 추상화)
    `-- Channel (HTTP/2 Multiplexing Connection Pool, TLS 관리)
`-- Server Runtime Layer
    |-- Netty / HTTP/2 Server Handler (이진 패킷 역직렬화)
    `-- Service Implementation (실제 비즈니스 서비스 로직 실행)
```

선의 의미: 계층 및 `.proto` 명세로부터 생성된 Client Stub이 Channel을 통해 HTTP/2 이진 패킷을 서버로 전송하여 비즈니스 로직을 실행하는 구조

| 구성요소 | 책임 |
|:---|:---|
| Protobuf IDL | 서비스·메서드·메시지 타입 계약 선언 |
| 코드 생성기 | `.proto`에서 **클라이언트·서버 코드** 생성 |
| 채널·스텁 | 로컬 호출 추상화와 HTTP/2 연결 관리 |
| 서버 런타임 | 역직렬화·핸들러 디스패치·응답 처리 |

#### 한줄 요약
- `.proto` 하나에서 양쪽 코드가 생성되므로 계약 위반이 런타임이 아닌 컴파일 시점에 드러나고, 채널과 스텁이 연결 관리를 대신 떠맡아 호출부는 로컬 함수 호출처럼 남는다.

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
   3. [이진 직렬화 및 전송] 요청 객체를 Protobuf 바이트로 직렬화해 전송
        │
   4. [서버 로직 처리] 서버가 이진 패킷을 역직렬화하고 비즈니스 핸들러 연산 수행
        │
   처리 결과와 함께 gRPC Status Code(OK) 및 Trailer 메타데이터를 클라이언트에 회신
```

동작 원리:

1. 채널 및 세션 수립: HTTP/2와 TLS 연결 준비
2. Deadline 전파: 인증 정보와 남은 기한 전달
3. 이진 직렬화 및 전송: Protobuf 메시지 송신
4. 서버 로직 처리: 핸들러 실행과 결과 생성

#### 한줄 요약
- Deadline이 최초 호출 지점에서 하위로 전파되어 연쇄 호출 전체가 하나의 시간 예산을 공유하므로, 상위가 포기한 뒤에도 하위 작업이 자원을 계속 소모하는 낭비가 차단된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **4대 gRPC 통신 패턴**: Unary(단일 요청-단일 응답), Server Streaming(단일 요청-연속 응답), Client Streaming(연속 요청-단일 응답), Bidirectional Streaming(양방향 연속 스트리밍).

</details>

| 비교 항목 | REST API (JSON) | gRPC (Protocol Buffers) |
|:---|:---|:---|
| 데이터 포맷 | **JSON 텍스트** | **Protobuf 이진 메시지** |
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
| 장기 HTTP/2 연결의 L4 트래픽 편중 | **Envoy·서비스 메시 L7 분산** 적용 | 스트림 단위 백엔드 분산 지원 |
| 브라우저 API의 gRPC 프로토콜 제약 | **gRPC-Web·JSON 트랜스코딩** 적용 | 브라우저 클라이언트 연계 |
| 삭제 필드 번호 재사용에 따른 충돌 | **`reserved`로 번호·이름 예약** | 이전 메시지와의 충돌 방지 |
| 연쇄 호출 지연에 따른 자원 고갈 | **Deadline 설정·하위 전파** | 호출 시간 예산과 취소 범위 통제 |

#### 한줄 요약
- 네 대책은 장기 연결과 이진 계약이 만든 분산·호환·수명 문제를 메시 계층과 예약 규칙으로 되사는 선택이며, gRPC-Web은 성능 이점 일부를 브라우저 호환성과 맞바꾼다.

## Ⅶ. 결론

- 내부 강타입 스트리밍은 **gRPC**, 공개 웹 자원은 **REST** 선택

#### 한줄 요약
- 내부 RPC에는 Deadline·재시도·로드밸런싱 정책을 함께 설계한다.
