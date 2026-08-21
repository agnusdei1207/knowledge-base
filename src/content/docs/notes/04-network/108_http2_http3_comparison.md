---
sidebar:
  order: 108
  label: "108. HTTP/2•HTTP/3 비교 (HTTP/2 HTTP/3 Comparison)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "차세대 웹 전송 프로토콜 비교 : HTTP/2 vs HTTP/3 (QUIC Architecture)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 108
extra:
  question_no: "108"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "RFC 9113(HTTP/2 over TCP) vs RFC 9114(HTTP/3 over QUIC/UDP), HoL Blocking 해결, 0-RTT 및 QPACK"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **HTTP/2 (RFC 9113)**: 단일 TCP 연결 상에서 바이너리 프레이밍(Binary Framing)을 통해 다수의 HTTP 요청/응답 스트림을 다중화(Multiplexing)하고, HPACK으로 헤더를 압축하여 전송 효율을 개선한 프로토콜.
- **HTTP/3 (RFC 9114)**: TCP의 고질적인 Head-of-Line Blocking 한계를 극복하기 위해, UDP 기반의 차세대 전송 계층 프로토콜인 **QUIC(RFC 9000)** 상에서 독립적 스트림 다중화와 TLS 1.3 내장 암호화를 제공하는 표준 웹 프로토콜.

</details>

- 정의/개념: L7 HTTP 시맨틱(Methods, Headers, Status Codes)을 공유하면서, 하부 전송 계층으로 **TCP/TLS(HTTP/2)** 와 **UDP 기반 QUIC/TLS 1.3(HTTP/3)** 을 각각 채택하여 전송 지연 및 연결 지속성을 혁신한 **웹 전송 계층 아키텍처 비교 체계**
- 배경/필요성: HTTP/2 환경에서 무선망 패킷 손실(Packet Drop) 발생 시, 단일 TCP 바이트 스트림 복구를 위해 무관한 모든 HTTP 스트림이 함께 멈추는 **전송 계층 Head-of-Line Blocking** 문제를 해결할 요구

#### 한줄 요약
- HTTP/2는 TCP 상의 다중화이나 패킷 손실 시 전체가 차단되며, HTTP/3는 QUIC(UDP)을 통해 스트림별 독립 전송을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **전송 계층 Head-of-Line (HoL) Blocking**: TCP는 순서 보증(In-Order Delivery) 특성으로 인해 1개 패킷이 유실되면 수신 버퍼에서 후속 패킷이 정상 도착해도 상위 애플리케이션으로 전달하지 못하고 TCP 재전송을 기다려야 하는 현상.
- **연결 ID 기반 연결 마이그레이션(Connection Migration)**: Wi-Fi에서 LTE/5G로 네트워크 IP가 변경되어도 4-Tuple 소켓이 아닌 64비트 Connection ID로 세션을 식별하여 0ms 재연결 없이 통신을 유지하는 QUIC 기능.

</details>

- **스트림 단위 완전 독립성 (HoL Blocking 완벽 해소)**: 특정 스트림에 패킷 손실이 발생해도 해당 스트림만 재전송 대기하고 나머지 스트림은 지연 없이 즉시 렌더링
- **0-RTT 초고속 재연결 (0-RTT Connection Resumption)**: TLS 1.3 핸드셰이크와 QUIC 연결 수립을 단 1회의 패킷 교환(1-RTT) 또는 이전 세션 캐시를 활용한 0-RTT로 완료
- **독립 스트림 친화적 QPACK 압축**: 스트림 간 순서 역전이 발생해도 헤더 압축 테이블 동기화 블로킹이 발생하지 않도록 설계된 QPACK(RFC 9204) 적용

#### 한줄 요약
- HoL 블로킹 해소, 0-RTT 초고속 연결, 연결 마이그레이션, QPACK 비동기 헤더 압축을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Alt-Svc(Alternative Services, RFC 7838)**: 웹 서버가 HTTP/2 응답 헤더에 `Alt-Svc: h3=":443"; ma=86400`을 실어 보내, 클라이언트가 다음 요청부터 UDP 443 포트를 통한 HTTP/3(QUIC) 통신을 시도하도록 유도하는 발견 메커니즘.

</details>

```text
[ 프로토콜 계층 스택 비교 구조 ]

┌──────────────────────────────────────────┐      ┌──────────────────────────────────────────┐
│      HTTP/2 Application (RFC 9113)       │      │      HTTP/3 Application (RFC 9114)       │
├──────────────────────────────────────────┤      ├──────────────────────────────────────────┤
│ HPACK (정적/동적 헤더 압축 테이블)        │      │ QPACK (단방향 제어 스트림 기반 헤더 압축) │
├──────────────────────────────────────────┤      ├──────────────────────────────────────────┤
│ TLS 1.2 / 1.3 (별도 암호화 핸드셰이크)    │      │                                          │
├──────────────────────────────────────────┤      │ QUIC Core (RFC 9000)                     │
│ TCP (단일 연결 바이트 스트림 ➔ HoL 병목)  │      │  ├─ TLS 1.3 내장 암호화 (0/1-RTT)        │
│                                          │      │  └─ 독립 스트림 프레이밍 & 혼잡 제어      │
├──────────────────────────────────────────┤      ├──────────────────────────────────────────┤
│ IP (L3 Routing)                          │      │ UDP (L4 비연결형 데이터그램)             │
└──────────────────────────────────────────┘      └──────────────────────────────────────────┘
```

선의 의미: HTTP/2는 TCP 상에서 TLS와 다중화 프레이밍이 개별 계층으로 적재되나, HTTP/3는 UDP 상에서 QUIC이 스트림 다중화, 혼잡 제어, TLS 1.3 보안을 단일 계층으로 통합한 구조

| 구성요소 | HTTP/2 (RFC 9113) | HTTP/3 (RFC 9114) | 비고 |
|:---|:---|:---|:---|
| **전송 계층 프로토콜** | **TCP (Transmission Control Protocol)** | **UDP (User Datagram Protocol)** | L4 기본 전송 |
| **연결 및 보안 계층** | TCP 3-Way Handshake + 별도 TLS 1.3 (2-RTT) | **QUIC 내부 내장 TLS 1.3 통합 (1-RTT / 0-RTT)** | 연결 수립 지연 |
| **다중화 구현 방식** | 단일 TCP 연결 상의 논리적 프레임 분할 | **QUIC 네이티브 독립 바이트 스트림** | Multiplexing |
| **헤더 압축 알고리즘** | **HPACK (엄격한 순차 동기화 필요)** | **QPACK (비동기 독립 스트림 최적화)** | Header Compression |
| **연결 식별자** | IP 주소 + Port 번호 (4-Tuple) | **Connection ID (CID: 64비트 랜덤 값)** | Mobility Support |

#### 한줄 요약
- HTTP/2는 TCP/HPACK 기반이며, HTTP/3는 UDP/QUIC/QPACK/TLS 1.3 통합 기반으로 동작한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HTTP/2 폴백(Fallback to HTTP/2)**: 엔터프라이즈 방화벽이나 통신사 장비가 보안상의 이유로 UDP 443 포트를 차단했을 때, 브라우저가 타임아웃 지연 없이 표준 TCP 포트 443을 통한 HTTP/2로 자동 우회 연결하는 복원 메커니즘.

</details>

```text
1. 브라우저가 최초 접속 시 표준 TCP 443 포트로 HTTP/2(TLS) 핸드셰이크 요청
            │
            ▼
2. 서버가 응답 헤더에 'Alt-Svc: h3=":443"' 필드를 실어 HTTP/3 지원 사실을 클라이언트에 공지
            │
            ▼
3. 클라이언트가 UDP 443 포트로 QUIC 1-RTT 초기 연결(Initial Packet) 동시 전송
            │
            ├─ [기업 방화벽 UDP 443 차단 / 패킷 드롭] ➔ 기존 HTTP/2(TCP) 연결로 투명하게 폴백 서빙
            ▼
4. [QUIC 연결 성공] ➔ TLS 1.3 키 교환 완료 및 독립 스트림으로 이미지/JS 파일 병렬 요청
            │
            ▼
5. 특정 스트림 패킷 손실 발생 시 ➔ 해당 스트림만 재전송, 나머지 스트림은 0ms 즉시 웹 화면 렌더링
```

**동작 원리**

1. **대체 서비스 발견**: 레거시 연결을 통해 서버의 QUIC 지원 여부를 확인하고 캐싱
2. **단일 RTT 수립**: 암호화 키 협상과 전송 계층 파라미터 교환을 단 1회의 왕복으로 완료
3. **병렬 스트림 서빙**: 각 자산(Asset)이 독립된 QUIC 스트림 ID를 부여받아 동시 전송
4. **선별적 복구**: 패킷 유실 시 해당 패킷 번호(Packet Number)만 선택적 재전송(Selective ACK)
5. **무중단 망 전환**: 모바일 기기가 Wi-Fi에서 셀룰러로 전환 시 동일 Connection ID로 핸드오버 완료

#### 한줄 요약
- Alt-Svc 발견, QUIC 1-RTT 연결, 독립 스트림 병렬 서빙, 선별적 유실 복구, 차단 시 HTTP/2 폴백 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HTTP/1.1 vs HTTP/2 vs HTTP/3 핵심 진화**: 텍스트 직렬 전송(HTTP/1.1)에서 TCP 다중화(HTTP/2)를 거쳐 UDP 독립 스트림(HTTP/3)으로의 전송 패러다임 진화.

</details>

| 비교 항목 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|:---|:---|:---|:---|
| **기본 전송 프로토콜** | TCP (텍스트 평문) | TCP (바이너리 프레이밍) | **QUIC over UDP (바이너리)** |
| **연결당 동시 요청** | 1개 요청/응답 (파이프라이닝 한계) | **단일 연결 내 다중 스트림 다중화** | **단일 연결 내 완전 독립 다중 스트림** |
| **초기 연결 수립 지연** | 2-RTT (TCP 1-RTT + TLS 1-RTT) | 2-RTT ~ 3-RTT | **1-RTT (최초) / 0-RTT (재접속)** |
| **패킷 유실 시 영향** | 단일 연결 블로킹 | **전체 스트림 HoL 블로킹 발생** | **유실된 스트림만 영향 (타 스트림 무영향)**|
| **모바일 IP 변경 대응** | 연결 완전 끊김 (재핸드셰이크) | 연결 완전 끊김 (재핸드셰이크) | **Connection ID 기반 무중단 마이그레이션** |

#### 한줄 요약
- HTTP/1.1은 직렬 전송, HTTP/2는 TCP 다중화(HoL 잔존), HTTP/3는 QUIC 기반 완전 독립 초저지연 전송이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **0-RTT 재생 공격(Replay Attack)**: 공격자가 이전 0-RTT 요청 패킷(Early Data)을 가로채어 서버로 재전송함으로써 결제, 송금 등 상태 변경 API가 중복 실행되는 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 엔터프라이즈 사내망 방화벽의 UDP 트래픽 일괄 차단으로 인한 **서비스 접속 불가 장애** | 클라이언트 브라우저의 **Happy Eyeballs v2(RFC 8305) 및 HTTP/2 자동 폴백** 구성 | UDP 차단 환경에서도 100% 서비스 도달성(Reachability) 보장 |
| 0-RTT 재연결 기능을 악용한 공격자의 **HTTP 요청 재생 공격(Replay Attack)** | **0-RTT Early Data에는 GET 등 멱등(Idempotent) 요청만 허용**하고 POST는 1-RTT 강제 | 결제 중복 실행 차단 및 0-RTT 성능과 트랜잭션 보안 양립 |
| QUIC 패킷 헤더 암호화로 인한 네트워크 인라인 보안 장비(IPS/DPI)의 **가시성(Visibility) 상실** | 엣지 프록시/WAF에서 **TLS 1.3 조기 복호화(Edge Termination) 및 L7 로깅** 수행 | 암호화 위협 탐지율 100% 유지 및 감사 추적성 확보 |

#### 한줄 요약
- HTTP/2 폴백으로 가용성을 보장하고, 0-RTT 멱등 제어로 재생 공격을 방어하며, 엣지 복호화로 가시성을 확보한다.

## Ⅶ. 결론

- 모바일 무선망 트래픽 급증과 초저지연 웹 서비스 요구에 부응하여 **QUIC 기반의 HTTP/3** 는 차세대 글로벌 인터넷 표준으로 빠르게 확산되고 있으며, 실무 도입 시 **UDP 443 포트 방화벽 정책 정비**, **HTTP/2 자동 폴백 메커니즘 구축**, **0-RTT 비멱등 API 보안 통제**를 결합하여 안정적이고 빠른 차세대 웹 인프라를 완성

#### 한줄 요약
- HTTP/3의 QUIC 독립 스트림과 HTTP/2 안전 폴백을 결합하여 고성능·고신뢰 차세대 웹 전송을 구현한다.
