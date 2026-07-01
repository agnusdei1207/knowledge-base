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
- **개요**: gRPC 호출 계약과 Protobuf 직렬화를 결합한 서비스 간 통신 방식
- **왜 필요한가**: 내부 서비스가 늘면 API 계약, 메시지 크기, 언어별 클라이언트 구현이 반복 비용이 된다. Protobuf는 계약과 binary 직렬화를 제공하고, gRPC는 이를 HTTP/2 RPC로 실행한다.
- **핵심 직관**: 공통 설계도(`.proto`)에서 각 언어의 호출 코드와 압축된 메시지를 동시에 얻는 방식이다.

## 깊이 이해
- **배경·문제의식**: JSON REST는 범용성이 높지만 타입 계약이 느슨하고 payload 크기가 커질 수 있다. 내부 RPC는 더 엄격한 계약과 낮은 직렬화 비용이 필요하다.
- **작동 원리**: `.proto`에 message와 service를 정의하면 compiler가 Stub과 메시지 클래스를 생성한다. 호출 시 메시지는 field number 기반 binary로 직렬화되고 gRPC status로 오류가 표현된다.
- **비유**: 각 나라 언어로 된 양식을 사람이 번역하지 않고, 표준 양식 번호에 맞춰 자동 생성된 서류를 주고받는 구조임.
- **구체 예시**: `message User { int64 id = 1; string name = 2; }`에서 필드 번호 1·2는 wire format의 핵심이므로 재사용 금지, 삭제 시 `reserved` 처리 필요.
- **흔한 오해·주의점**: Protobuf는 필드 이름보다 번호가 호환성의 핵심이다. 번호를 바꾸거나 재사용하면 구버전 클라이언트가 잘못 해석할 수 있다.

## 연결 개념
- gRPC — Protobuf 기반 RPC 프레임워크
- Schema Registry — proto 계약 중앙 관리
- Backward Compatibility — 필드 추가·삭제 규칙

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

gRPC·Protocol Buffers는 내부 서비스 통신 표준 조합이다. gRPC는 HTTP/2 RPC 실행을 담당하고 Protobuf는 IDL과 binary 메시지 직렬화를 담당한다. MSA에서는 계약 자동 생성과 schema evolution이 서비스 간 변경 리스크를 줄인다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
