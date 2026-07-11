---
title: "프록시·리버스 프록시 (Proxy Reverse Proxy)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 217
extra:
  question_no: "217"
  exam_status: "미출제"
---

## 미리 알고가기

- Forward Proxy는 Client가 외부 Server에 연결할 때 대신 요청하고 Reverse Proxy는 외부 Client 요청을 내부 Server 대신 수신함
- Forward Proxy는 Egress 대상·인증·감사, Reverse Proxy는 Ingress TLS·Routing·Load Balancing·보안 정책을 적용함
- HTTP Proxy는 메시지를 해석·변환할 수 있고 CONNECT Tunnel은 대상 연결을 만든 뒤 Byte Stream을 중계함
- Reverse Proxy가 전달한 Client IP·Host·Protocol Header는 신뢰하는 Proxy가 덮어쓴 값만 사용해야 함
- Proxy Timeout·Retry·Buffering 설정은 Client와 Upstream의 처리 시간·멱등성·Streaming 요구에 맞춰야 함

## 작성 근거(검토용)

- Proxy·Reverse Proxy는 배치 위치, 대리 대상, 연결 목적, 대상 선택, 정책, TLS, 대표 적용 사례로 비교함
- 구조와 절차는 Listener·Authentication·Routing·Connection Pool·Header 신뢰·관측을 요청 경로로 설명함
- 빌드 서버 Egress와 API Ingress는 차단 요청률·전송량·p99 Upstream 지연·5xx 비율로 검증함

## Ⅰ. 개요

- **정의/개념**: Proxy는 Client를 대신해 외부 Server에 연결하고 Reverse Proxy는 내부 Server를 대신해 Client 요청을 수신·정책 적용·전달하는 응용 계층 중계 구조임
- **배경/필요성**: 다수 Client의 외부 접속 정책과 다수 Server의 외부 노출·TLS·Routing 정책을 개별 응용이 아닌 통제 지점에서 일관되게 적용해야 함

## Ⅱ. 특징

- Forward Proxy는 Client 인증·Destination Allowlist·DNS·접속 Log로 외부 서비스 사용을 통제함
- Reverse Proxy는 Host·Path·Header·Protocol로 Upstream Cluster를 선택하고 TLS 종료·재암호화를 수행함
- Connection Pool·Keep-Alive·HTTP/2 Multiplexing으로 Downstream 연결과 Upstream 연결의 수명주기를 분리함
- Request·Response Buffering은 느린 연결을 분리하지만 Streaming·대용량 Payload의 지연·메모리 사용에 영향함
- Retry는 멱등 요청과 재시도 예산에만 적용하고 Upstream Timeout·Circuit Breaker로 장애 전파를 제한함
- `Forwarded`·`X-Forwarded-*` Header는 외부 입력을 제거하고 신뢰 Proxy가 생성한 Hop 정보만 인증·감사에 사용함

## Ⅲ. 종류 및 비교

| 판단 기준 | Forward Proxy | Reverse Proxy |
|:---|:---|:---|
| 배치 위치 | Client와 외부 Server 사이 Egress | 외부 Client와 내부 Server 사이 Ingress |
| 대리 대상 | Client·사용자 | Server·서비스 Cluster |
| 연결 대상 선택 | Client 요청 URL·CONNECT 대상과 Egress 정책 | Host·Path·Header와 Upstream Routing 정책 |
| 접근 통제 | Client 인증·Destination Allowlist·감사 | TLS·WAF·인증·Rate Limit·Backend 권한 |
| 주소 노출 | 외부 Server에 Proxy 주소가 연결 주체로 보임 | Client에 Proxy Endpoint만 노출 |
| Cache 적용 | 조직 Client의 공통 외부 응답 Cache | 서비스의 공개 응답·정적 자산 Cache |
| 대표 적용 사례 | 개발·업무망의 외부 저장소·패키지 접근 | API Gateway·웹 Ingress·Load Balancer |

> 요약: Forward Proxy는 Client의 외부 접속을, Reverse Proxy는 Server의 외부 요청 수신·Routing을 대신함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Listener·TLS | Client 연결을 수신하고 인증서·Protocol·암호 정책을 적용함 |
| Authentication·Policy | Client·Service Identity와 목적지·경로별 접근을 판정함 |
| Router·Resolver | 외부 Destination 또는 내부 Upstream Cluster를 선택함 |
| Connection Pool·Tunnel | Upstream 연결을 재사용하거나 CONNECT Byte Stream을 중계함 |
| Header·Buffer Filter | Hop-by-Hop Header·Client 정보·압축·Buffering을 관리함 |
| Access Log·Metrics·Trace | Downstream·Upstream 시간·상태·Byte·Route를 기록함 |

```text
Forward: Client -> Forward Proxy -> External Server
Reverse: Client -> Reverse Proxy -> Internal Service
```

> 요약: Listener와 정책 계층이 연결을 수신하고 Router·Connection Pool이 선택한 외부·내부 대상에 요청을 전달함.

## Ⅴ. 원리 및 절차 흐름도

```text
연결 수신 -> 신원·정책 확인 -> 대상 해석 -> 연결 획득 -> 메시지 중계 -> 응답·관측
```

1. **연결 수신**: Listener가 TLS·HTTP·CONNECT 요청을 해석하고 Downstream 제한을 적용함
2. **신원·정책 확인**: Client 인증과 Destination·Host·Path·Rate 정책을 평가함
3. **대상 해석**: DNS·Service Discovery·Route Table로 Server·Upstream 후보를 구함
4. **연결 획득**: Connection Pool을 재사용하거나 새 TLS·Tunnel 연결을 생성함
5. **중계·관측**: Header·Body·Stream을 전달하고 상태 코드·Byte·Downstream·Upstream 시간을 기록함

> 요약: Proxy는 연결을 수신해 신원·목적지 정책을 적용하고 선택한 대상과의 연결을 중계·관측함.

## Ⅵ. 실무 사례

1. 빌드 서버는 Forward Proxy Allowlist를 적용하고 차단 요청률·외부 전송량을 확인함
2. API Ingress는 Reverse Proxy TLS·Routing을 적용하고 p99 Upstream 지연·5xx 응답률을 확인함

## Ⅶ. 결론

- Proxy·Reverse Proxy는 대리 대상·신뢰 Header 경계·TLS·Routing·Timeout·Retry·Streaming 요구를 기준으로 설계해야 함
