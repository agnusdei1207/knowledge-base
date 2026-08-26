---
sidebar:
  order: 108
  label: "108. HTTP/2•HTTP/3 비교"
  badge:
    text: "미출 · 50%"
    variant: note
title: "차세대 웹 전송 프로토콜 비교 : HTTP/2 vs HTTP/3"
date: "2026-08-26T14:19:07+09:00"
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

- 정의/개념: TCP 다중화와 **QUIC 독립 스트림**의 웹 전송 프로토콜
- 배경/필요성: HTTP/2의 패킷 유실로 **전체 스트림 HoL·망 전환 단절** 발생

#### 한줄 요약
- TCP HoL 블로킹을 해결하고 0-RTT 연결 수립과 연결 마이그레이션을 통해 무선망 전송 효율을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TCP Head-of-Line Blocking**: TCP의 순차 바이트 스트림 특성으로 인해 중간 패킷 1개가 유실되면 수신 버퍼 큐에서 무관한 다른 모든 HTTP 스트림의 처리가 중단되는 병목.
- **Connection ID (CID) Migration**: IP/Port 4-Tuple 대신 64비트 랜덤 연결 ID를 사용하여 Wi-Fi에서 LTE로 망 전환 시에도 재연결 없이 통신을 지속하는 기술.

</details>

- **독립 스트림**: 손실이 다른 스트림을 차단하지 않음
- **0-RTT·1-RTT**: QUIC에 TLS 1.3 통합
- **Connection ID**: IP 변경에도 연결 상태 유지

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
| 전송 계층 프로토콜 | **TCP** | **UDP** | L4 전송 |
| 연결 및 보안 계층 | TCP·별도 TLS | **QUIC·TLS 1.3** | 연결 지연 |
| 다중화 구현 방식 | TCP 논리 프레임 | **QUIC 독립 스트림** | Multiplexing |
| 헤더 압축 알고리즘 | **HPACK** | **QPACK** | Header Compression |
| 연결 식별자 | 4-Tuple | **Connection ID** | Mobility Support |

#### 한줄 요약
- HTTP/2는 TCP/HPACK 기반이며, HTTP/3는 UDP/QUIC/QPACK/TLS 1.3 통합 기반으로 동작한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Alt-Svc (Alternative Services, RFC 7838)**: 서버가 HTTP/2 응답 헤더에 `Alt-Svc: h3=":443"`를 실어 보냄으로써 클라이언트에게 HTTP/3 지원을 알리는 광고 메커니즘.

</details>

```text
브라우저 요청
    |
1. HTTP/2 최초 접속
    |
2. Alt-Svc 광고 수신
    |
3. QUIC 1-RTT 연결
    +-- UDP 차단: HTTP/2 폴백
    |
4. 독립 스트림 병렬 요청
    |
5. 선별적 재전송
    |
웹 응답
```

- 1. HTTP/2 최초 접속
- 2. Alt-Svc 광고 수신
- 3. QUIC 1-RTT 연결
- 4. 독립 스트림 병렬 요청
- 5. 선별적 재전송

#### 한줄 요약
- Alt-Svc 발견 → QUIC 1-RTT 연결 → 독립 스트림 병렬 서빙 → 선별적 유실 복구 → 차단 시 HTTP/2 폴백 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HTTP/1.1 vs HTTP/2 vs HTTP/3**: 직렬 전송, TCP 다중화, QUIC 기반 완전 독립 다중화.

</details>

| 비교 항목 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|:---|:---|:---|:---|
| 기본 전송 프로토콜 | TCP 텍스트 | TCP 바이너리 | **QUIC·UDP** |
| 연결당 동시 요청 | 1개 | **다중 스트림** | **독립 다중 스트림** |
| 초기 연결 수립 지연 | 2-RTT | 2~3-RTT | **1-RTT·0-RTT** |
| 패킷 유실 시 영향 | 연결 블로킹 | **전체 스트림 HoL** | **해당 스트림만 영향** |
| 모바일 IP 변경 대응 | 재연결 | 재연결 | **CID 마이그레이션** |

#### 한줄 요약
- HTTP/1.1은 직렬 전송, HTTP/2는 TCP 다중화(HoL 잔존), HTTP/3는 QUIC 기반 완전 독립 초저지연 전송이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Happy Eyeballs v2 (RFC 8305)**: 클라이언트가 UDP 기반 QUIC과 TCP 기반 HTTP/2를 병렬로 동시 시도하여 더 빠르게 응답하는 연결을 선택하는 이중화 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| UDP 443 차단으로 접속 실패 | **Happy Eyeballs·HTTP/2 폴백** | 서비스 도달성 확보 |
| 0-RTT 요청 재생 공격 | **멱등 요청만 Early Data 허용** | 중복 실행 차단 |
| QUIC 암호화로 IPS 가시성 상실 | **엣지 복호화·L7 로깅** | 감사 추적성 확보 |
| UDP 처리로 서버 CPU 증가 | **UDP GSO·eBPF XDP** | 처리 부하 절감 |

#### 한줄 요약
- HTTP/2 폴백으로 가용성을 보장하고, 0-RTT 멱등 제어로 재생 공격을 방어하며, 엣지 복호화로 가시성을 확보한다.

## Ⅶ. 결론

- 유선 안정망은 **HTTP/2**, 손실·망 전환 환경은 **HTTP/3·폴백** 선택

#### 한줄 요약
- HTTP/3는 QUIC 기반의 독립 스트림과 0-RTT 연결 및 Connection ID를 통해 무선망 웹 전송 성능을 혁신하는 표준 프로토콜이다.
