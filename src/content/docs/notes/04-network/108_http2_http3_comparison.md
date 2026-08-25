---
sidebar:
  order: 108
  label: "108. HTTP/2•HTTP/3 비교"
  badge:
    text: "미출 · 50%"
    variant: note
title: "차세대 웹 전송 프로토콜 비교 : HTTP/2 vs HTTP/3"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
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

- **HTTP/2 (RFC 9113)**: 단일 TCP 상에서 바이너리 프레이밍과 HPACK 압축으로 스트림을 다중화한 웹 프로토콜.
- **HTTP/3 (RFC 9114)**: UDP 기반의 차세대 전송 계층 프로토콜인 QUIC(RFC 9000) 상에서 독립 스트림 다중화와 0-RTT를 지원하는 표준 웹 프로토콜.

</details>

- 정의/개념: 동일한 HTTP 시맨틱 상에서 **TCP 기반 바이너리 다중화(HTTP/2)와 UDP 기반 QUIC 독립 스트림(HTTP/3)을 채택한 차세대 웹 전송 프로토콜군**
- 배경/필요성: HTTP/2 단일 TCP 연결 상에서 단 1개 패킷 유실 시 모든 스트림이 멈추는 **TCP HoL Blocking 한계 및 모바일 망 전환 시 연결 단절**

#### 한줄 요약
- TCP HoL 블로킹을 해결하고 0-RTT 연결 수립과 연결 마이그레이션을 통해 무선망 전송 효율을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TCP Head-of-Line Blocking**: TCP의 순차 바이트 스트림 특성으로 인해 중간 패킷 1개가 유실되면 수신 버퍼 큐에서 무관한 다른 모든 HTTP 스트림의 처리가 중단되는 병목.
- **Connection ID (CID) Migration**: IP/Port 4-Tuple 대신 64비트 랜덤 연결 ID를 사용하여 Wi-Fi에서 LTE로 망 전환 시에도 재연결 없이 통신을 지속하는 기술.

</details>

- **TCP HoL(Head-of-Line) 블로킹 완전 해결**: QUIC 기반으로 **각 스트림이 독립 전송되어 특정 패킷 유실 시에도 타 스트림 정상 서빙**
- **초고속 0-RTT / 1-RTT 연결 수립**: QUIC 계층 내부에 TLS 1.3을 통합하여 **최초 1-RTT 및 재연결 시 0-RTT 즉시 전송**
- **모바일 무선망 연결 마이그레이션(Connection Migration)**: 4-Tuple이 변경되어도 **Connection ID(CID)를 유지하여 핸드오버 무단절 보장**

#### 한줄 요약
- HoL 블로킹 제거, 0-RTT/1-RTT 초고속 연결, Connection ID 기반 무단절 마이그레이션을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HPACK vs QPACK**: 엄격한 단일 스트림 순차 압축(HPACK)과 다중 독립 스트림 간의 순서 역전을 지원하는 비동기 헤더 압축(QPACK).

</details>

```text
[HTTP/2 vs HTTP/3 프로토콜 스택 비교 구조]
|-- HTTP/2 Protocol Stack (RFC 9113)
|   |-- HTTP/2 Binary Framing & HPACK Header Compression
|   |-- TLS 1.2 / 1.3 (별도 암호화 핸드셰이크)
|   `-- TCP (단일 연결 순차 바이트 스트림 -> 1개 손실 시 HoL 발생)
`-- HTTP/3 Protocol Stack (RFC 9114)
    |-- HTTP/3 Frames & QPACK Header Compression
    |-- QUIC Core (RFC 9000: TLS 1.3 내장 암호화, 독립 스트림 프레이밍, Connection ID)
    `-- UDP (L4 비연결형 데이터그램)
```

선의 의미: HTTP/2는 TCP 상에서 TLS와 다중화가 개별 계층으로 적재되나 HTTP/3는 UDP 상에서 QUIC이 스트림 다중화, 혼잡 제어, TLS 1.3 보안을 단일 계층으로 통합한 구조

| 구성요소 | HTTP/2 (RFC 9113) | HTTP/3 (RFC 9114) | 비고 |
|:---|:---|:---|:---|
| **전송 계층 프로토콜** | **TCP (Transmission Control Protocol)** | **UDP (User Datagram Protocol)** | L4 기본 전송 |
| **연결 및 보안 계층** | TCP 3-Way Handshake + 별도 TLS (2-RTT) | **QUIC 내부 TLS 1.3 통합 (1-RTT / 0-RTT)** | 연결 수립 지연 |
| **다중화 구현 방식** | 단일 TCP 상의 논리적 프레임 분할 | **QUIC 네이티브 독립 바이트 스트림** | Multiplexing |
| **헤더 압축 알고리즘** | **HPACK (엄격한 순차 동기화 필요)** | **QPACK (비동기 독립 스트림 최적화)** | Header Compression |
| **연결 식별자** | IP 주소 + Port 번호 (4-Tuple) | **Connection ID (CID: 64비트 랜덤 값)** | Mobility Support |

#### 한줄 요약
- HTTP/2는 TCP/HPACK 기반이며, HTTP/3는 UDP/QUIC/QPACK/TLS 1.3 통합 기반으로 동작한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Alt-Svc (Alternative Services, RFC 7838)**: 서버가 HTTP/2 응답 헤더에 `Alt-Svc: h3=":443"`를 실어 보냄으로써 클라이언트에게 HTTP/3 지원을 알리는 광고 메커니즘.

</details>

```text
HTTP/3 Alt-Svc 발견, QUIC 1-RTT 연결 및 독립 스트림 서빙 파이프라인
        │
   1. [HTTP/2 최초 접속] 브라우저가 표준 TCP 443 포트로 초기 HTTP/2(TLS) 핸드셰이크 수행
        │
   2. [Alt-Svc 광고 수신] 서버가 응답 헤더에 `Alt-Svc: h3=":443"`를 실어 HTTP/3 지원 사실 공지
        │
   3. [QUIC 1-RTT 연결] 클라이언트가 UDP 443 포트로 QUIC 초기 연결(Initial Packet) 전송
        │
   ├─ [방화벽 UDP 443 차단 시] ➔ 기존 HTTP/2(TCP) 연결로 투명하게 자동 폴백 서빙
   ▼
4. [독립 스트림 병렬 요청] TLS 1.3 키 교환 완료 후 이미지/JS 자산을 독립 스트림으로 병렬 수신
        │
   ▼
5. [선별적 재전송] 특정 스트림 패킷 손실 시 해당 스트림만 재전송하고 타 스트림 0ms 즉시 렌더링
```

#### 한줄 요약
- Alt-Svc 발견 → QUIC 1-RTT 연결 → 독립 스트림 병렬 서빙 → 선별적 유실 복구 → 차단 시 HTTP/2 폴백 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HTTP/1.1 vs HTTP/2 vs HTTP/3**: 직렬 전송, TCP 다중화, QUIC 기반 완전 독립 다중화.

</details>

| 비교 항목 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|:---|:---|:---|:---|
| **기본 전송 프로토콜**| TCP (텍스트 평문) | TCP (바이너리 프레이밍) | **QUIC over UDP (바이너리)** |
| **연결당 동시 요청** | 1개 요청/응답 (파이프라이닝 한계) | **단일 연결 내 다중 스트림 다중화** | **단일 연결 내 완전 독립 다중 스트림** |
| **초기 연결 수립 지연**| 2-RTT (TCP 1-RTT + TLS 1-RTT) | 2-RTT ~ 3-RTT | **1-RTT (최초) / 0-RTT (재접속)** |
| **패킷 유실 시 영향** | 단일 연결 블로킹 | **전체 스트림 HoL 블로킹 발생** | **유실된 스트림만 영향 (타 스트림 무영향)**|
| **모바일 IP 변경 대응**| 연결 완전 끊김 (재핸드셰이크) | 연결 완전 끊김 (재핸드셰이크) | **Connection ID 기반 무중단 마이그레이션**|

#### 한줄 요약
- HTTP/1.1은 직렬 전송, HTTP/2는 TCP 다중화(HoL 잔존), HTTP/3는 QUIC 기반 완전 독립 초저지연 전송이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Happy Eyeballs v2 (RFC 8305)**: 클라이언트가 UDP 기반 QUIC과 TCP 기반 HTTP/2를 병렬로 동시 시도하여 더 빠르게 응답하는 연결을 선택하는 이중화 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기업 사내망 방화벽의 UDP 443 차단으로 인한 **서비스 접속 불가 장애** | **`Happy Eyeballs v2 및 HTTP/2 투명한 자동 폴백(Fallback)`** 구성 | UDP 차단 환경에서도 100% 서비스 도달성(Reachability) 보장 |
| 0-RTT 재연결 기능을 악용한 공격자의 **HTTP 요청 재생 공격(Replay Attack)** | **0-RTT Early Data에는 GET 등 멱등(Idempotent) 요청만 허용**하고 POST는 1-RTT 강제 | 결제 중복 실행 차단 및 0-RTT 성능과 트랜잭션 보안 양립 |
| QUIC 패킷 헤더 암호화로 인한 네트워크 인라인 보안 장비(IPS)의 **가시성 상실** | 엣지 프록시/WAF에서 **`TLS 1.3 엣지 복호화(Edge Termination) 및 L7 로깅`** | 암호화 위협 탐지율 100% 유지 및 감사 추적성 확보 |
| 커널 UDP 소켓 버퍼링 병목으로 인한 서버 CPU 점유율 증가 | **`UDP GSO (Generic Segmentation Offload)` 및 eBPF XDP 가속** 적용 | 대용량 트래픽 처리 시 서버 CPU 부하 50% 절감 |

#### 한줄 요약
- HTTP/2 폴백으로 가용성을 보장하고, 0-RTT 멱등 제어로 재생 공격을 방어하며, 엣지 복호화로 가시성을 확보한다.

## Ⅶ. 결론

- 모바일 무선망 트래픽 급증과 초저지연 웹 서비스 요구에 부응하여 **QUIC 기반의 HTTP/3는 차세대 글로벌 인터넷 표준으로 확립**되었으며, 실무 도입 시 **UDP 443 포트 방화벽 정책 정비, HTTP/2 자동 폴백 메커니즘 구축, 0-RTT 비멱등 API 보안 통제**를 결합하여 안정적이고 빠른 차세대 웹 인프라 완성

#### 한줄 요약
- HTTP/3는 QUIC 기반의 독립 스트림과 0-RTT 연결 및 Connection ID를 통해 무선망 웹 전송 성능을 혁신하는 표준 프로토콜이다.