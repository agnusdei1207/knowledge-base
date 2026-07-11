---
title: "gRPC (gRPC)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 202
extra:
  question_no: "202"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- gRPC는 IDL로 서비스·메시지를 정의하고 생성 Stub을 통해 원격 메서드를 호출하는 RPC 프레임워크임
- 기본 IDL과 메시지 형식은 Protocol Buffers이며 필드 번호가 직렬화와 호환성의 기준이 됨
- 호출 유형은 Unary·Server Streaming·Client Streaming·Bidirectional Streaming으로 구분됨
- Channel은 서버 연결을 관리하고 HTTP/2 Stream이 Metadata·Message·Status를 한 RPC 단위로 전달함
- Deadline·Cancellation·Status Code를 호출 계약에 포함해야 장애가 상위 서비스의 무기한 대기로 전파되지 않음

## 작성 근거(검토용)

- gRPC는 IDL 계약, Stub, Channel, HTTP/2 Stream, 네 가지 호출 유형, Deadline·Status를 핵심 축으로 설명함
- 비교표는 REST와 계약·호출 모델·전송·메시지·호환성·접근성·적합 조건을 대비함
- 내부 추론 호출과 양방향 데이터 스트림은 p99 지연·전송량·메시지 처리율·취소 반영 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: gRPC는 Protocol Buffers로 서비스·메시지 계약을 정의하고 생성 Stub과 HTTP/2 기반 Channel로 단항·스트리밍 원격 호출을 수행하는 RPC 프레임워크임
- **배경/필요성**: 내부 서비스 간 다언어 호출에서 메서드·메시지 타입을 코드 생성으로 일치시키고 단항·연속 데이터 교환을 하나의 호출 모델로 운영하기 위해 필요함

## Ⅱ. 특징

- `.proto`의 Service·RPC·Message 정의에서 클라이언트 Stub과 서버 인터페이스를 생성함
- Unary와 세 가지 Streaming 유형으로 한 요청·응답부터 양방향 독립 메시지 흐름까지 표현함
- HTTP/2 연결 안에서 RPC별 Stream을 다중화하고 Header·Data·Trailer로 Metadata·Message·Status를 전달함
- Deadline이 만료되거나 호출이 취소되면 클라이언트와 서버가 남은 작업을 중단하도록 상태를 전파함
- Protobuf 필드 번호를 재사용하지 않고 필드 추가·예약 규칙을 지켜 구·신 메시지의 해석 충돌을 방지함
- 재시도·부하분산·TLS·관측 정책은 서비스 설정과 인프라에서 호출의 멱등성·오류 범위에 맞게 구성함

## Ⅲ. 종류 및 비교

| 판단 기준 | REST API | gRPC |
|:---|:---|:---|
| 계약 단위 | URI·HTTP 의미·표현 스키마 | Service·RPC·Protobuf Message IDL |
| 호출 모델 | 자원별 요청·응답과 별도 스트림 규약 | Unary·Server·Client·양방향 Streaming |
| 전송 의미 | HTTP 메서드·상태 코드·헤더 사용 | HTTP/2 Stream·Metadata·gRPC Status 사용 |
| 메시지 표현 | JSON·XML 등 협상된 미디어 타입 | 기본 Protobuf 이진 메시지 |
| 호환성 관리 | URI·미디어 타입·스키마 버전 관리 | 필드 번호 유지·추가·예약 규칙 관리 |
| 클라이언트 접근 | 브라우저·HTTP 도구에서 직접 호출 | 생성 Stub 중심이며 브라우저는 gRPC-Web 계층 사용 |
| 적합 조건 | 외부 공개 자원 API·HTTP 캐시 활용 | 내부 다언어 서비스·타입 계약·스트리밍 호출 |

> 요약: REST는 HTTP 자원 인터페이스를, gRPC는 IDL 기반 원격 메서드와 단항·스트리밍 호출을 제공함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| `.proto` IDL | Service·RPC·Message·필드 번호를 정의함 |
| Compiler·Generated Code | 언어별 메시지 클래스·클라이언트 Stub·서버 인터페이스를 생성함 |
| Client Stub·Channel | 메서드 호출을 메시지로 변환하고 서버 연결·RPC Stream을 관리함 |
| Server·Handler | 요청 메시지를 역직렬화하고 구현 메서드를 실행함 |
| HTTP/2·Flow Control | 연결 안에서 RPC Stream을 다중화하고 송수신 윈도 크기를 조정함 |
| Metadata·Deadline·Status | 인증 문맥·시간 제한·종료 상태와 오류 상세를 전달함 |

```text
Client Stub -> Channel -> HTTP/2 RPC Stream -> Server Handler
     proto Message + Metadata          Status + proto Message
```

> 요약: 생성 Stub과 서버 Handler가 Protobuf 계약을 공유하고 Channel의 HTTP/2 Stream이 메시지·메타데이터·상태를 전달함.

## Ⅴ. 원리 및 절차 흐름도

```text
IDL 컴파일 -> Channel 생성 -> RPC 호출 -> 메시지·메타데이터 전송 -> Handler 실행 -> Status 종료
```

1. **IDL 컴파일**: `.proto`에서 언어별 메시지·Stub·서버 인터페이스를 생성함
2. **Channel 생성**: 클라이언트가 대상 주소·TLS·부하분산 설정으로 Channel을 준비함
3. **RPC 호출**: Stub이 메서드·Deadline·Metadata와 요청 메시지를 호출 객체로 구성함
4. **Stream 전송**: Protobuf 메시지를 HTTP/2 Frame으로 보내고 Flow Control을 적용함
5. **Handler 실행·종료**: 서버가 응답 메시지와 gRPC Status를 반환하고 Stream을 종료함

> 요약: gRPC는 IDL에서 생성한 Stub 호출을 HTTP/2 Stream으로 전달하고 서버 결과를 메시지와 Status로 종료함.

## Ⅵ. 실무 사례

1. 모델 추론 서비스는 Unary gRPC와 Deadline을 적용하고 p99 호출 지연·요청당 전송량을 확인함
2. 데이터 처리 노드는 양방향 Streaming과 Flow Control을 적용하고 메시지 처리율·취소 반영 시간을 확인함

## Ⅶ. 결론

- gRPC는 강한 타입 계약·다언어 코드 생성·스트리밍이 필요하고 Deadline·호환성·관측 정책을 운영할 때 적용해야 함
