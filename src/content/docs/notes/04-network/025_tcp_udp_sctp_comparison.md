---
sidebar:
  order: 25
  label: "025. TCP•UDP•SCTP 비교 (TCP UDP SCTP)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "전송 계층 프로토콜 : TCP•UDP•SCTP 비교 (Transport Protocols)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 25
extra:
  question_no: "025"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "전송 계층 3대 프로토콜의 신뢰성, 메시지 경계 및 다중화 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TCP(Transmission Control Protocol)**: 가상 회선 기반의 연결형 프로토콜로, 3-Way Handshake, 시퀀스 번호, 흐름/혼잡 제어를 통해 신뢰성 있는 바이트 스트림(Byte Stream) 전송을 보장.
- **UDP(User Datagram Protocol)**: 사전 연결 설정 및 상태 관리 없이 최소한의 헤더(8바이트)만으로 독립적인 데이터그램(Datagram)을 전송하는 비연결형 비신뢰성 프로토콜.
- **SCTP(Stream Control Transmission Protocol)**: TCP의 연결 지향 신뢰성과 UDP의 메시지 경계 보존 특성을 결합하고, 멀티호밍(Multihoming) 및 멀티스트리밍(Multistreaming)을 지원하는 차세대 전송 프로토콜(RFC 4960).

</details>

- 정의/개념: OSI 7계층 중 전송 계층(L4)에서 애플리케이션의 신뢰성, 실시간 지연 및 고가용성 요구에 따라 선택적으로 운용되는 **3대 전송 제어 프로토콜**
- 배경/필요성: 단일 프로토콜로 파일 무결성(TCP), 실시간 미디어 스트리밍(UDP), 통신사급 고신뢰 다중 경로 제어(SCTP)를 동시에 충족할 수 없는 특성 분기 발생

#### 한줄 요약
- 신뢰성(TCP), 초저지연(UDP), 다중 경로·스트림 고가용성(SCTP)의 서비스 요구에 따라 차등 적용된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **바이트 스트림(Byte Stream)**: 애플리케이션 데이터를 개별 메시지 경계 없이 연속적인 바이트들의 흐름으로 취급하는 전송 모델(TCP).
- **메시지 경계(Message Boundary)**: 애플리케이션이 송신한 개별 패킷(레코드)의 크기와 시작/끝 경계를 수신단에서도 그대로 보존하는 전송 모델(UDP, SCTP).

</details>

- **TCP**: 3-Way Handshake 기반 **연결 지향형**, 순서 보장, 오류 제어(ARQ), 흐름/혼잡 제어 및 **바이트 스트림** 제공
- **UDP**: 비연결형, 제어 오버헤드 최소화(헤더 8B)를 통한 **초저지연 데이터그램** 전송 및 브로드캐스트/멀티캐스트 지원
- **SCTP**: Cookie 기반 4-Way Handshake, **멀티호밍(Multihoming)** 고가용성 및 **멀티스트리밍(Multistreaming)** 을 통한 HoL Blocking 해소

#### 한줄 요약
- TCP는 바이트 스트림 신뢰성을, UDP는 비연결 저지연을, SCTP는 멀티호밍과 메시지 경계를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SCTP 연관(Association)**: 통신하는 두 종단 간의 논리적 연결 관계로, 양 종단의 복수 IP 주소들을 단일 연관으로 묶어 관리.
- **쿠키 기반 4단계 핸드셰이크(SCTP 4-Way)**: INIT $\rightarrow$ INIT-ACK(State Cookie 발급) $\rightarrow$ COOKIE-ECHO $\rightarrow$ COOKIE-ACK 절차로 TCP의 SYN Flood 공격을 원천 차단하는 연결 메커니즘.

</details>

```text
[ 애플리케이션 계층 (HTTP, 실시간 영상/음성, 통신망 제어 평면) ]
          │                    │                    │
          ▼                    ▼                    ▼
     [ TCP 계층 ]          [ UDP 계층 ]         [ SCTP 계층 ]
  - 연결형 (Connection) - 비연결형 (Datagram) - 연관형 (Association)
  - 단일 스트림          - 독립 전송          - 멀티스트리밍 (Stream 0..N)
  - 단일 IP 바인딩       - 단일 IP 바인딩     - 멀티호밍 (Primary/Backup IP)
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
               [ IP 계층 (네트워크 라우팅) ]
```

선의 의미: 상위 애플리케이션 요구에 따라 TCP(신뢰성), UDP(저지연), SCTP(다중화) 계층으로 매핑되는 구조

| 프로토콜 | 연결 방식 | 전송 단위 | 신뢰성 및 흐름 제어 | 헤더 크기 |
|:---|:---|:---|:---|:---|
| **TCP** | 연결형 (3-Way Handshake) | 바이트 스트림 (Segment) | 신뢰성 보장 (ACK, 재전송, Sliding Window) | 20 ~ 60 Bytes |
| **UDP** | 비연결형 (No Handshake) | 메시지 단위 (Datagram) | 비신뢰성 (재전송 및 흐름 제어 없음) | 8 Bytes (고정) |
| **SCTP** | 연관형 (4-Way Handshake) | 메시지 단위 (Chunk) | 신뢰성 보장 (SACK 기반 혼잡/흐름 제어) | 12 Bytes + Chunks |

#### 한줄 요약
- TCP(연결형 세그먼트), UDP(비연결형 데이터그램), SCTP(연관형 멀티청크)의 구조적 차이를 갖는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **전송 계층 프로토콜 선택 기준**: 데이터 무결성 최우선 여부, 전송 지연 한계, 다중 인터페이스 활용 필요성에 따라 프로토콜을 결정하는 아키텍처 판단.

</details>

```text
1. 애플리케이션 전송 요구사항 분석
            │
            ├─ [패킷 유실 무관 / 실시간 초저지연 요구] ──▶ 2a. UDP 채택 (DNS, VoIP, QUIC)
            ├─ [복수 IP 기반 무중단 통신 / 멀티스트림] ──▶ 2b. SCTP 채택 (5G NGAP, LTE Diameter)
            └─ [100% 무결성 데이터 / 순차 전송 보증] ───▶ 2c. TCP 채택 (HTTP/1.1, TLS, SSH)
```

**동작 원리**

1. **지연 민감형**: 실시간 음성/영상 및 단순 질의응답은 핸드셰이크 오버헤드가 없는 UDP 선택
2. **무결성 중심**: 파일 전송, 금융 거래, 웹 통신은 패킷 손실 시 즉시 재전송하는 TCP 선택
3. **통신 사업자망**: 세션 단절이 절대 허용되지 않는 제어 신호망은 물리 회선 이중화(멀티호밍)가 가능한 SCTP 선택

#### 한줄 요약
- 실시간 초저지연은 UDP, 데이터 무결성은 TCP, 무중단 다중 경로는 SCTP를 선택한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **선두 차단(Head-of-Line Blocking, HoL Blocking)**: TCP 단일 스트림 상에서 앞선 패킷 1개가 유실되었을 때, 뒤이어 정상 수신된 패킷들도 상위 계층으로 전달되지 못하고 대기하는 현상.
- **멀티호밍(Multihoming)**: 단일 SCTP 연관에 복수의 IP 주소를 바인딩하여 주 경로 장애 시 백업 IP로 무중단 자동 절체(Failover)하는 기능.
- **멀티스트리밍(Multistreaming)**: 단일 연관 내에 독립적인 다중 논리 스트림을 생성하여 하나의 스트림에서 패킷 손실이 발생해도 타 스트림은 영향 없이 독립 수신하는 기술.

</details>

| 비교 항목 | TCP (Transmission Control) | UDP (User Datagram) | SCTP (Stream Control) |
|:---|:---|:---|:---|
| **연결 모델** | 1:1 단일 연결 (3-Way Handshake) | 비연결 (No Handshake) | 1:다 **멀티호밍(Multihoming)** 연관 (4-Way) |
| **데이터 전달 단위** | **바이트 스트림** (경계 없음) | **데이터그램** (메시지 경계 보존) | **청크(Chunk)** (메시지 경계 보존) |
| **선두 차단(HoL) 극복** | 불가 (단일 바이트 스트림 병목) | 해당 없음 (독립 패킷 처리) | **완전 극복 (독립 멀티스트리밍)** |
| **SYN Flood 방어** | 취약 (SYN Cookie 추가 필요) | 해당 없음 | **자체 방어 (State Cookie 4-Way)** |
| **주요 적용 프로토콜** | HTTP/1.1, HTTP/2, FTP, SSH | DNS, DHCP, RTP, QUIC(HTTP/3) | 5G Core(NGAP/SCTP), LTE MME, WebRTC Data |

#### 한줄 요약
- TCP는 단일 스트림 신뢰성을 제공하고, UDP는 단순성을 제공하며, SCTP는 멀티호밍과 HoL 방지를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **미들박스 통과성(Middlebox Traversal)**: 방화벽, NAT, L4 스위치 등의 기존 네트워크 장비들이 SCTP 프로토콜 번호(132)를 차단하거나 변환하지 못하는 호환성 문제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| TCP 사용 시 패킷 유실 구간에서 발생하는 **선두 차단(HoL Blocking)** 지연 | 애플리케이션 계층 멀티플렉싱 도입 또는 **QUIC(UDP 기반)** 전환 | 독립 스트림 처리로 단일 패킷 유실 시 전체 지연 차단 |
| 실시간 스트리밍 환경에서 TCP의 재전송 지연으로 인한 화면 버퍼링 | **UDP 기반 전송 프로토콜(RTP/RTCP)** 및 FEC(전방 오류 정정) 적용 | 실시간성 확보 및 수신단 자체 결함 복구 |
| 레거시 방화벽/NAT 장비의 **SCTP 프로토콜(Protocol 132) 차단/비지원** | **UDP 캡슐화(SCTP over UDP, RFC 6951)** 또는 WebRTC Data Channel 적용 | 기존 인프라 수정 없이 표준 미들박스 구간 통과 보증 |

#### 한줄 요약
- HoL 문제는 QUIC/멀티스트림으로 해소하고, 실시간 버퍼링은 UDP/FEC로 해결하며, SCTP 미들박스 차단은 UDP 캡슐화로 극복한다.

## Ⅶ. 결론

- 분산 서비스 설계 시 전송 계층의 트레이드오프를 고려하여 데이터 정합성이 필수적인 업무 시스템에는 **TCP/TLS**를, 실시간 초저지연 인터랙션에는 **UDP/QUIC**를, 통신사 인프라 및 미션 크리티컬 제어망에는 **SCTP 멀티호밍** 아키텍처를 선택 적용하여 신뢰성과 성능을 극대화

#### 한줄 요약
- 서비스 도메인의 신뢰성·지연·가용성 요구에 맞추어 TCP, UDP, SCTP를 최적 선택 운용한다.
