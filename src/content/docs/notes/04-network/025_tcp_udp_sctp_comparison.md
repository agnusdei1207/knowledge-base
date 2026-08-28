---
sidebar:
  order: 25
  label: "025. TCP•UDP•SCTP 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "TCP•UDP•SCTP 비교 (Transport Protocols)"
date: "2026-08-26T13:41:15+09:00"
tags:
  - "notes-network"
weight: 25
extra:
  question_no: "25"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "전송 계층 3대 프로토콜의 신뢰성, 메시지 경계 및 다중화 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TCP (Transmission Control Protocol)**: 연결 지향적 신뢰성 바이트 스트림(Byte Stream) 전송 프로토콜 (RFC 793).
- **UDP (User Datagram Protocol)**: 오버헤드가 극소화된 8바이트 헤더 기반의 비연결형 데이터그램(Datagram) 전송 프로토콜 (RFC 768).
- **SCTP (Stream Control Transmission Protocol)**: 멀티호밍(Multihoming)과 멀티스트리밍(Multistreaming)을 지원하는 메시지 기반 신뢰성 전송 프로토콜 (RFC 4960).

</details>

- 정의/개념: L4 전송 계층에서 애플리케이션의 신뢰성, 실시간 초저지연, 다중 경로 고가용성 요구에 맞추어 운용하는 **3대 핵심 전송 프로토콜(TCP / UDP / SCTP)**
- 배경/필요성: 단일 전송 방식으로는 **무결성·저지연·멀티호밍 동시 충족 불가**하고 신뢰성 보장에 드는 연결 설정·재전송·순서 복원 비용은 응용마다 가치가 다르므로, 그 비용을 전부 치를지 일부만 치를지 응용이 고르도록 L4를 세 갈래 프로토콜로 나눠 둘 필요

#### 한줄 요약
- 신뢰성(TCP), 초저지연(UDP), 다중 경로·스트림 고가용성(SCTP)의 서비스 요구에 따라 차등 적용된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multihoming (멀티호밍)**: 단일 SCTP 연관에 복수의 IP 인터페이스를 바인딩하여 주 회선 장애 시 백업 IP로 무중단 자동 절체하는 기능.
- **Multistreaming (멀티스트리밍)**: 단일 연결 내에 독립적인 다중 스트림을 두어 선두 패킷이 유실되어도 타 스트림이 차단되지 않는 기술.

</details>

- **TCP**: 3-Way Handshake 기반 **연결 지향형, 순서 보장, 오류/흐름/혼잡 제어 및 바이트 스트림** 제공
- **UDP**: 비연결형, 8바이트 헤더 기반 **초저지연 데이터그램 전송 및 멀티캐스트/브로드캐스트 지원**
- **SCTP**: Cookie 4-Way Handshake, **멀티호밍(Multihoming) 고가용성 및 멀티스트리밍(HoL 차단 해소)**

#### 한줄 요약
- TCP는 바이트 스트림 신뢰성을, UDP는 비연결 저지연을, SCTP는 멀티호밍과 메시지 경계를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SCTP Chunk (청크)**: SCTP 패킷 내에 포함되는 데이터 단위로, 제어 청크(INIT, SACK)와 데이터 청크(Payload)로 구성.

</details>

| 구성요소 | 책임 |
|:---|:---|
| TCP 프로토콜 | 연결·순서·**흐름·혼잡 제어** |
| UDP 프로토콜 | 비연결 **저지연 데이터그램 전송** |
| SCTP 프로토콜 | 메시지 기반 **신뢰성 전송** |
| 멀티호밍 | 복수 IP의 **무중단 경로 절체** |
| 멀티스트리밍 | 독립 스트림으로 **HoL 차단 격리** |

#### 한줄 요약
- 멀티호밍과 멀티스트리밍은 TCP를 쓸 때 응용이 재접속과 스트림 분리로 떠맡던 일을 L4 안으로 끌어들여, 경로 절체와 HoL 격리를 전송 계층이 대신 처리한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **프로토콜 선정 3대 판단 기준**: 1. 데이터 손실 허용 여부 $\to$ 2. 실시간성/지연 허용 한계 $\to$ 3. 복수 인터페이스 고가용성 요구 여부.

</details>

```text
애플리케이션 L4 전송 프로토콜 선정 의사결정
        │
   [서비스 요구사항 분석] 신뢰성, 지연 허용 한계, 고가용성 요건 판정
   ┌────┼───────────────────────────┬───────────────────────────┐
   │    │                           │                           │
  [실시간/저지연]                 [100% 무결성/순서]          [통신사/무중단 제어]
   │    │                           │                           │
 UDP 채택                        TCP 채택                   SCTP 채택
   (DNS, VoIP, QUIC/HTTP3)          (HTTP/1.1, TLS, SSH, DB)    (5G NGAP, LTE Diameter)
   │    │                           │                           │
   └────┴───────────────────────────┴───────────────────────────┘
        ▼
   [최적화된 L4 전송 파이프라인 가동 완료]
```

#### 한줄 요약
- 손실 허용 여부가 갈래를 가르는 첫 지점이어서, 손실을 못 견디면 재전송과 순서 복원 비용을 TCP·SCTP에서 치르고 지연을 못 견디면 그 복구 책임을 응용이 떠안는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HoL Blocking (Head-of-Line Blocking)**: TCP 단일 스트림에서 1개 패킷 유실 시 뒤따르는 정상 수신 패킷들까지 애플리케이션 전달이 지연되는 병목 현상.

</details>

| 비교 항목 | TCP (Transmission Control) | UDP (User Datagram) | SCTP (Stream Control) |
|:---|:---|:---|:---|
| 연결 모델 | **1:1 단일 연결 (3-Way Handshake)** | **비연결 (No Handshake)** | **1:N 멀티호밍 연관 (4-Way Handshake)** |
| 데이터 전달 단위 | **바이트 스트림 (메시지 경계 없음)** | **데이터그램 (메시지 경계 보존)**| **청크 Chunk (메시지 경계 보존)** |
| 선두 차단(HoL) 극복 | **불가 (단일 스트림 전체 대기 병목)** | 해당 없음 (독립 패킷 처리) | **완전 극복 (독립 멀티스트리밍 분리)** |
| SYN Flood 방어력 | 취약 (SYN Cookie 추가 튜닝 필요) | 해당 없음 | **자체 방어 (State Cookie 4-Way 내장)**|
| 주요 대표 프로토콜 | HTTP/1.1, HTTP/2, TLS, SSH, DB | DNS, DHCP, WebRTC, QUIC(HTTP/3)| 5G Core(NGAP), LTE MME, Diameter |

#### 한줄 요약
- TCP는 단일 스트림 신뢰성을, UDP는 단순 저지연을, SCTP는 멀티호밍과 HoL 방지를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SCTP over UDP (RFC 6951)**: 기존 레거시 NAT/방화벽이 SCTP 프로토콜(132번)을 차단하는 문제를 해결하기 위해 SCTP 패킷을 UDP로 캡슐화하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| TCP 패킷 1개 유실로 인한 선두 차단(HoL Blocking) 지연 | **UDP 기반 `QUIC (HTTP/3)` 또는 SCTP 멀티스트리밍 도입** | 독립 스트림 처리로 단일 패킷 유실 지연 격리 |
| 실시간 방송/게임 스트리밍 시 TCP 재전송으로 인한 화면 버퍼링 | **`UDP 기반 RTP/SRTP` 및 수신단 `FEC(전방 오류 정정)` 적용** | 재전송 대기 없는 초저지연 실시간 재생 |
| 기존 레거시 방화벽/NAT의 SCTP 프로토콜(132번) 차단 문제 | **`SCTP over UDP (RFC 6951)` 캡슐화 또는 WebRTC Data** | 기존 네트워크 인프라 변경 없이 미들박스 통과 |
| UDP 패킷 무단 폭주로 인한 네트워크 대역폭 고갈 | **애플리케이션 레벨 `토큰 버킷 레이트 리미팅 및 DCCP`** | 공정 대역폭 공유 및 혼잡 붕괴 방어 |

#### 한줄 요약
- QUIC/SCTP로 HoL 차단, UDP/FEC로 실시간성 확보, SCTP over UDP로 미들박스 통과를 달성한다.

## Ⅶ. 결론

- 무결성·저지연·멀티호밍 요구에 따라 **TCP·UDP·SCTP** 선택

#### 한줄 요약
- 서비스 도메인의 신뢰성, 지연, 멀티호밍 요구에 맞추어 TCP, UDP, SCTP를 최적 선택 운용한다.
