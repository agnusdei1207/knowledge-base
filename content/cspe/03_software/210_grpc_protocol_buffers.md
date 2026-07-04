---
title: "gRPC·Protocol Buffers (gRPC Protocol Buffers)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 210
---

# 📖 【암기용】 개념 완전 이해

> 목적: gRPC·Protocol Buffers를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: gRPC는 **RPC(원격 프로시저 호출)**를 HTTP/2 위에서 실행하는 프레임워크이고, Protocol Buffers는 그 메시지를 정의하는 **IDL(인터페이스 정의 언어)**이자 **이진 직렬화(Binary Serialization)** 포맷이다.
- **왜 필요한가**: 내부 서비스가 많아지면 API 계약이 흩어지고, JSON 텍스트 직렬화는 payload가 커지며, 언어마다 클라이언트를 손으로 구현해야 하는 반복 비용이 생긴다. `.proto` 하나로 계약·코드·직렬화를 동시에 해결한다.
- **핵심 직관**: 공통 설계도(`.proto`)에서 각 언어의 호출 코드(Stub)와 압축된 이진 메시지를 자동으로 뽑아내는 "공장 도면" 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| RPC(원격 프로시저 호출) | 다른 프로세스·서버의 함수를 로컬 함수처럼 호출하는 방식 — gRPC가 구현하는 상위 개념 | 다른 부서에 전화해서 계산을 시키는데 내 컴퓨터 함수 부르듯 쓰는 것 |
| IDL(Interface Definition Language) | 언어 독립적으로 메시지·서비스 계약을 정의하는 언어 — `.proto`가 이 역할 | 여러 나라 언어로 번역 가능한 표준 설계도면 |
| 직렬화(Serialization) | 메모리의 객체를 전송 가능한 바이트열로 변환하는 것 | 짐을 상자에 압축 포장해 배송 가능하게 만드는 것 |
| `.proto` 파일 | message·service를 정의하는 원본 계약 파일 | 설계도 원본 |
| protoc / codegen | `.proto`를 읽어 각 언어의 클래스·Stub 코드를 자동 생성하는 컴파일러 | 설계도를 각 나라 언어의 시공 도면으로 자동 번역하는 기계 |
| Stub | 생성된 클라이언트·서버 호출 코드 — 네트워크 호출을 로컬 함수처럼 보이게 함 | 전화 교환원 — 번호만 누르면 상대와 연결해줌 |
| Field Number | 메시지 필드마다 붙는 고유 번호 — 이름이 아니라 이 번호가 wire format(전송 형식)의 실제 키 | 서류 양식의 칸 번호 — 칸 제목이 바뀌어도 번호만 맞으면 같은 칸으로 인식 |
| Wire Type | 필드 값의 인코딩 방식(0=Varint, 1=64bit, 2=길이지정, 5=32bit) | 우편물 종류(엽서·소포·등기)에 따라 처리 방식이 다른 것 |
| Varint | 작은 수는 짧게, 큰 수는 길게 인코딩하는 가변 길이 정수 표현 | 짧은 단어는 짧게, 긴 단어는 길게 쓰는 속기법 |
| Streaming(4모드) | unary, server-streaming, client-streaming, bidirectional-streaming | 1회 통화, 안내방송, 신고 접수, 양방향 대화 |
| Deadline | 호출 체인 전체에 전파되는 요청 제한시간 | 릴레이 경주에서 전체 완주 제한시간을 각 주자가 공유 |
| Reserved | 삭제된 필드 번호를 재사용하지 못하도록 예약해 두는 선언 | 퇴사자 사번을 신규 입사자에게 재발급하지 않고 결번 처리 |

## 깊이 이해

### 배경 — JSON REST의 한계 (수치로)
- HTTP/1.1은 도메인당 동시 연결 수가 브라우저 기준 보통 6개로 제한돼(connection limit) 요청이 몰리면 대기열이 생긴다. gRPC는 HTTP/2의 **멀티플렉싱**을 써서 TCP 연결 1개 위에서 수백 개의 요청·응답 스트림을 동시에 주고받아 이 제약을 없앤다.
- JSON은 필드 이름을 매번 반복 전송한다. `{"id":150,"name":"Kim"}`은 23바이트인데, 같은 정보를 Protobuf로 직렬화하면 아래처럼 8바이트로 줄어든다 — 필드 이름 대신 숫자 태그만 싣기 때문이다.

### Wire Format을 직접 인코딩해보기 (Field Number의 정체)
- `message User { int64 id = 1; string name = 2; }`에서 `id=150, name="Kim"`을 인코딩한다고 하자.
- 필드 1(id)의 태그 바이트 = (field_number << 3) | wire_type = (1<<3) | 0(Varint) = `0x08`. 150을 Varint로 쓰면 7비트씩 묶어 `0x96 0x01`(2바이트) — 태그 1바이트 + 값 2바이트 = 3바이트.
- 필드 2(name)의 태그 바이트 = (2<<3) | 2(길이지정) = `0x12`. 길이 3(문자 "Kim") + 실제 바이트 `4B 69 6D` — 태그 1 + 길이 1 + 값 3 = 5바이트.
- 합쳐서 총 8바이트. 핵심은 **필드 이름 "id", "name"이 전송 바이트 어디에도 없다는 것** — 오직 숫자 1, 2(필드 번호)만 태그에 실린다. 그래서 필드 번호를 바꾸거나 재사용하면 수신 측이 완전히 다른 필드로 오해하고, 필드 이름만 바꾸는 것(번호만 유지)은 아무 문제가 없다.

### 필드 번호가 호환성의 핵심인 이유 — 판별 원리
- 필드를 **추가**할 땐 기존 번호를 건드리지 않고 새 번호를 쓰면 구버전 클라이언트는 그 필드를 그냥 무시하므로 안전하다(전방 호환).
- 필드를 **삭제**할 땐 번호를 `reserved 3;`처럼 예약해 미래에 실수로 재사용되지 않게 막아야 한다 — 재사용하면 구버전이 보낸 옛 필드 3번 데이터를 신버전이 엉뚱한 의미로 해석하는 사고가 난다.
- 타입을 바꿀 땐 wire type이 같은 것끼리만 안전하다(예: int32 ↔ int64는 둘 다 Varint라 호환, string ↔ bytes도 둘 다 길이지정이라 호환). wire type이 다른 타입으로 바꾸면(int32 → string) 파싱 자체가 깨진다.

### 4가지 통신 모드 — 언제 무엇을 쓰나
- **Unary**(요청 1 · 응답 1): 일반 API 호출, 예) 사용자 조회.
- **Server Streaming**(요청 1 · 응답 다수): 대량 조회 결과를 순차 전송, 예) 로그 tail, 대용량 리스트 스트림.
- **Client Streaming**(요청 다수 · 응답 1): 클라이언트가 여러 청크를 보내고 서버가 완료 시 한 번 응답, 예) 파일 업로드.
- **Bidirectional Streaming**(양쪽 다 스트림): 채팅처럼 양방향 실시간 교환, 예) 음성 인식 스트림.

### 비유와 흔한 오해
- 비유: 각 나라 언어로 된 서류를 사람이 매번 번역하지 않고, 표준 양식 번호(`.proto`의 field number)에 맞춰 자동 생성된 서류를 주고받는 국제기구의 표준 양식 시스템과 같다.
- 오해 1: "Protobuf가 항상 JSON보다 빠르다"는 절대적 진리가 아니다 — 소규모 payload에서는 차이가 미미하고, 반복 호출·대용량·저지연 내부 RPC에서 이득이 커진다.
- 오해 2: gRPC는 브라우저에서 기본적으로 직접 호출하기 어렵다(HTTP/2 trailer 등의 제약) — 브라우저 클라이언트가 필요하면 grpc-web 프록시 계층이 추가로 필요하다.

## 연결 개념
- HTTP/2 — gRPC가 올라타는 전송 계층(멀티플렉싱·헤더 압축)
- REST·OpenAPI — 외부 공개 API에서 더 흔히 쓰는 대안 계약 방식
- Schema Registry / Backward Compatibility — `.proto` 계약을 조직 단위로 관리하는 운영 장치

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: gRPC·Protobuf는 호출 프레임워크와 메시지 계약을 분리해 설명하고, 호환성 규칙을 반드시 포함해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: gRPC는 RPC 실행 계층, Protocol Buffers는 IDL과 binary 직렬화 계층이다.
> 2. **가치**: `.proto` 단일 계약에서 Stub, 메시지 타입, 문서, 테스트를 생성해 다국어 서비스 통신을 표준화한다.
> 3. **판단 포인트**: field number, reserved, optional, oneof, backward compatibility, deadline·status 처리가 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| gRPC와 Protobuf 역할 구분 확인 | RPC 전송 vs IDL·직렬화 | 둘을 같은 기술명으로만 설명 |
| 계약 호환성 이해 확인 | field number, reserved, schema evolution | 필드명 변경만으로 호환성 판단 |
| 실무 적용 판단 확인 | codegen, CI breaking check, status code | JSON 대비 binary 장점만 나열 |

> 요약: 이 문제는 내부 RPC 통신 구조와 `.proto` 호환성 규칙을 함께 평가한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 내부 서비스 통신 표준 조합
- 배경: gRPC는 HTTP/2 RPC 실행을 담당하고 Protobuf는 IDL과 binary 메시지 직렬화를 담당한다.
- 필요성: protoc codegen, field number, schema evolution 기준으로 MSA 서비스 간 계약 변경 리스크를 줄인다.

---

## Ⅱ. 구조 및 구성요소

```text
proto File -> protoc Codegen -> Client Stub -> gRPC HTTP/2 -> Server Stub -> Service
          +-> Protobuf Message / Field Number / Compatibility Check
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| `.proto` | service와 message 계약 정의 | proto3, package, option |
| Protobuf | binary wire format 직렬화 | field number가 호환성 기준 |
| gRPC Stub | 클라이언트·서버 호출 코드 | 언어별 자동 생성 |
| Status/Metadata | 오류·인증·추적 정보 전달 | status code, deadline, trace id |

> 요약: `.proto` 계약에서 Protobuf 메시지와 gRPC Stub을 생성해 호출과 데이터 형식을 함께 표준화한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
proto 정의 -> 코드 생성 -> 메시지 직렬화 -> RPC 호출 -> status 처리 -> 계약 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | message field number와 service method 정의 | lint error 0건 |
| 2 | protoc 또는 buf로 다국어 코드 생성 | generated code commit 정책 |
| 3 | Protobuf binary로 직렬화 후 HTTP/2 전송 | payload size 측정 |
| 4 | gRPC status와 metadata로 결과 처리 | status error 1% 이하 |

> 요약: gRPC·Protobuf 흐름은 계약 정의, 코드 생성, binary 전송, status 처리, 호환성 검증으로 진행된다.

---

## Ⅳ. 특징

| 구분 | JSON REST | gRPC·Protobuf | 판단 포인트 |
|:---|:---|:---|:---|
| 계약 | OpenAPI와 런타임 검증 | proto IDL과 compile-time 검증 | 내부 다국어 서비스에 적합 |
| 직렬화 | text 기반 | binary wire format | payload 30~70% 축소 기대 |
| 호환성 | 필드명·schema 기준 | field number 기준 | 번호 재사용 금지 |
| 디버깅 | 사람이 직접 읽기 쉬움 | 도구 필요 | reflection·grpcurl 운영 제한 필요 |

> 요약: gRPC·Protobuf는 내부 RPC 계약과 전송량 절감에 유리하나 디버깅과 호환성 규칙 준수가 필수이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | REST + JSON + OpenAPI | gRPC + Protobuf + proto registry | 내부 서비스 20개 이상, 언어 3종 이상 |
| 비용/성능 | JSON parsing·수동 client | codegen·binary serialization | p95 100ms, payload 1KB 이상 반복 호출 |
| 운영/위험 | schema drift | field number 파손 | buf breaking check 적용 가능 |

> 요약: 내부 RPC가 많고 계약 자동 생성 가치가 크면 gRPC·Protobuf를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 호환성 파손 | field number 변경·재사용 | reserved, breaking check | incompatible proto 0건 |
| 디버깅 제약 | binary payload | grpcurl, reflection 비운영 차단, trace | trace coverage 95% 이상 |
| 배포 불일치 | Stub 버전 상이 | schema registry, consumer test | client/server version mismatch 0건 |

> 요약: 핵심 리스크는 proto 호환성, binary 관측성, Stub 버전 불일치이며 CI와 registry로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 계약 | buf lint·breaking 100% pass | CI pipeline |
| 지연 | p95 RPC latency 100ms 이하 | OpenTelemetry |
| 크기 | JSON 대비 payload 30% 이상 감소 | benchmark test |

> 요약: 도입 효과는 계약 검증률, RPC 지연, payload 크기로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. `.proto` repository와 schema registry를 운영하고 `buf lint`, `buf breaking`을 merge 조건으로 설정함.
2. field 삭제는 `reserved`로 처리하고 신규 필드는 optional·새 번호 추가 원칙을 적용해 backward compatibility를 유지함.
3. gRPC deadline 300ms, status code 표준, OpenTelemetry metadata 전파, mTLS 인증을 플랫폼 정책으로 적용함.

**결론 (2줄):**
- 기술사 판단: 내부 저지연 RPC와 다국어 Stub이 필요하면 gRPC·Protobuf, 외부 공개와 브라우저 호환성이 우선이면 REST·OpenAPI를 선택함.
- 향후 방향: Protobuf 계약은 API catalog, service mesh, contract test와 결합해 조직 API 표준으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "gRPC·Protobuf를 설명하시오" | proto, codegen, serialization, status 처리 | JSON REST 대비 계약·직렬화 차이 |
| 요구사항 명시형 | "내부 API 표준을 설계하시오", "비교하시오" | schema registry, breaking check, deadline | 호환성 리스크, 선택 기준, 지표 |

> 요약: 설명형은 역할 구분, 설계·비교형은 proto 호환성과 내부 RPC 운영 표준 중심으로 전환한다.
