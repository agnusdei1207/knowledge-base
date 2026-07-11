---
title: "gRPC·Protocol Buffers (gRPC Protocol Buffers)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 210
extra:
  question_no: "210"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Protocol Buffers는 `.proto`의 Message·Field Type·Field Number로 데이터를 정의하고 언어별 코드를 생성하는 IDL·직렬화 체계임
- Wire Format은 필드 이름 대신 Field Number와 Wire Type을 기록하므로 배포 후 번호를 바꾸거나 재사용하면 해석이 충돌함
- 새 필드는 호환 가능한 번호로 추가하고 삭제한 필드의 번호·이름은 `reserved`로 남겨 재사용을 막음
- 알 수 없는 필드는 새 송신자와 구 수신자의 호환을 위해 보존할 수 있지만 JSON 변환·필드 순회에서 손실 가능성을 확인해야 함
- gRPC는 Service RPC의 요청·응답 Message에서 Protobuf 계약과 생성 Stub을 기본으로 사용함

## 작성 근거(검토용)

- gRPC·Protobuf는 IDL, Field Number·Wire Type, Presence·Cardinality, 코드 생성, 호환성, Stub 실행을 핵심 축으로 설명함
- 비교표는 Protobuf Binary와 JSON의 계약·식별·부재 표현·미지 필드·진화·검사·적합 조건을 대비함
- 추론 요청과 다언어 서비스 계약은 Payload 크기·Decode CPU·호환성 위반·배포 실패로 검증함

## Ⅰ. 개요

- **정의/개념**: gRPC·Protocol Buffers는 Service·RPC·Message 계약을 `.proto`에 정의하고 생성 Stub이 Field Number 기반 이진 메시지를 직렬화해 원격 호출하는 인터페이스 체계임
- **배경/필요성**: 여러 언어의 서비스가 메서드·데이터 타입을 같은 IDL에서 생성하고 구·신 배포가 공존할 때 Wire 계약을 유지하려면 명시적 번호·호환성 규칙이 필요함

## Ⅱ. 특징

- Message는 Scalar·Enum·중첩 Message와 `optional`·`repeated`·`map`·`oneof` Cardinality를 정의함
- Field Number와 Wire Type이 Tag를 구성하고 Varint·Fixed·Length-Delimited 방식으로 값을 인코딩함
- `protoc`과 언어 Plugin이 Message 접근자·Serializer·Parser와 gRPC Client·Server 코드를 생성함
- 새 선택 필드 추가와 미지 필드 보존은 구·신 코드 공존을 지원하지만 번호·타입의 비호환 변경은 막아야 함
- 삭제 번호·이름은 `reserved`로 관리하고 Enum의 0 값은 `UNSPECIFIED` 의미로 두어 기본값과 업무값을 구분함
- Protobuf Binary는 정규 표현이 아니므로 직렬화 Byte 자체를 Hash·서명 기준으로 사용할 때 별도 정규화가 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Protocol Buffers Binary | JSON |
|:---|:---|:---|
| 계약 정의 | `.proto` Message·Field Type·Number | 문서·JSON Schema·응용 코드에서 속성 계약 정의 |
| 필드 식별 | 숫자 Tag와 Wire Type | 문자열 속성 이름 |
| 부재·기본값 | Presence 규칙과 타입별 기본값 적용 | 누락과 `null` 의미를 API 계약에서 정의 |
| 미지 필드 | Binary Parsing 후 보존·재직렬화 가능 | Parser·DTO 설정에 따라 무시·보존·거부 |
| 계약 진화 | 번호 유지·선택 필드 추가·삭제 번호 예약 | 속성 추가·삭제·이름·타입의 소비자 영향 관리 |
| 내용 검사 | Descriptor·생성 코드·Decoder 필요 | 텍스트 도구에서 속성 이름과 값 확인 |
| 적합 조건 | 다언어 내부 RPC·Schema 기반 이진 메시지 | 브라우저·외부 API·사람이 읽는 교환 형식 |

> 요약: Protobuf는 Field Number 기반 이진 계약과 코드 생성을, JSON은 문자열 속성 기반 교환과 텍스트 검사를 제공함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Package·Import·Option | 이름 공간·파일 의존성·언어별 생성 설정을 정의함 |
| Message·Enum·Field | 데이터 타입·번호·Cardinality·기본 Enum 값을 정의함 |
| Service·RPC | Unary·Streaming 메서드와 요청·응답 Message를 연결함 |
| `protoc`·Plugin | 언어별 Message 클래스와 gRPC Stub·Server Interface를 생성함 |
| Descriptor·Reflection | 런타임에 Service·Message·Field 계약을 조회하게 함 |
| Registry·Compatibility Check | 이전 `.proto`와 번호·타입·삭제·예약 규칙을 비교함 |

```text
.proto -> protoc + Plugins -> Message Code + gRPC Stubs
Client Message -> Protobuf Binary -> gRPC -> Server Message
```

> 요약: 하나의 `.proto`가 Message 직렬화 코드와 gRPC Stub을 생성하고 Registry 검사가 배포 사이 Wire 호환성을 통제함.

## Ⅴ. 원리 및 절차 흐름도

```text
IDL 변경 -> 호환성 검사 -> 코드 생성 -> Message 직렬화 -> gRPC 호출 -> 역직렬화·응답
```

1. **IDL 변경**: Service·RPC·Message에 새 Field Number와 Cardinality를 정의함
2. **호환성 검사**: 이전 Descriptor와 번호 재사용·타입 변경·삭제 예약 여부를 비교함
3. **코드 생성**: `protoc`과 Plugin이 각 언어의 Message·Stub·Server Interface를 생성함
4. **직렬화·호출**: Client가 Message를 Tag·Value Byte로 인코딩해 gRPC Stream에 전송함
5. **역직렬화·응답**: Server가 알려진 Field를 해석하고 RPC 결과 Message를 같은 계약으로 반환함

> 요약: Protobuf 계약은 호환성 검사와 코드 생성을 거쳐 gRPC 요청·응답의 이진 직렬화 기준이 됨.

## Ⅵ. 실무 사례

1. 모델 추론 RPC는 Protobuf Message와 gRPC Stub을 적용하고 Payload 크기·역직렬화 CPU 시간을 확인함
2. 다언어 서비스는 Field 예약과 호환성 검사를 적용하고 Schema 위반 건수·배포 실패율을 확인함

## Ⅶ. 결론

- gRPC·Protocol Buffers는 Field Number·Presence·예약·코드 생성 규칙을 서비스 배포 순서와 함께 관리해야 함
