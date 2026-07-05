---
title: "TCP, UDP, SCTP 비교"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-network"
weight: 30
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: L4 전송 계층은 애플리케이션 요구에 따라 신뢰성 중심의 TCP와 속도 중심의 UDP로 양분되었으나, 통신망의 고도화로 생존성과 병렬 처리를 극대화한 **SCTP**가 등장했다.
> 2. **가치**: SCTP는 TCP의 신뢰성, 연결 지향 특성과 UDP의 메시지 지향 특성을 융합하고, 멀티 호밍(Multi-homing)과 멀티 스트리밍(Multi-streaming)이라는 획기적인 무기를 장착했다.
> 3. **판단 포인트**: 통신사망(SIGTRAN) 및 5G 코어 제어 평면에서는 생존성을 위해 SCTP가 필수 표준이나, 일반 웹/모바일 환경에서는 TCP 커널 수정의 어려움으로 인해 UDP 기반의 QUIC이 SCTP의 철학(멀티 스트리밍)을 대신 구현하고 있다.

---
## Ⅰ. 개요 및 필요성

- **개요**: IP 프로토콜 위에서 애플리케이션(프로세스) 간 논리적 데이터 전송을 담당하는 주요 L4 프로토콜들의 구조적 특징과 차이를 비교하는 것.
- **필요성**:
  - `TCP`: 패킷 분실 시 치명적인 웹, 파일 전송(HTTP, FTP)을 위해 꼼꼼한 확인이 필요.
  - `UDP`: 일부 패킷이 유실되더라도 끊김 없는 실시간 스트리밍(VoIP, 게임)이 필요.
  - `SCTP`: "TCP처럼 완벽하게 보내면서, 선로 하나가 끊기면 0.1초 만에 백업 선로로 자동 전환되고, 데이터 하나 유실됐다고 다른 데이터들까지 줄 서서 기다리는 병목(HoL Blocking)은 없는" 무결점 프로토콜이 5G 등 캐리어급(Carrier-grade) 망에 필요.

---
## Ⅱ. 아키텍처 및 핵심 원리

- **프로토콜 간 구조적 차이 직관도**

```text
[ TCP 구조 (Single-path / Single-stream) ]   [ SCTP 구조 (Multi-homing / Multi-stream) ]
App --+                                      App ----+---------+---------+
      | (하나의 파이프)                              | Strm 1  | Strm 2  | Strm 3
     TCP                                           SCTP (Association)
      |                                              |                   |
    IP-A (단일 경로)                               IP-A (Primary)      IP-B (Backup)
      |                                              |                   |
    Network                                        Network 1           Network 2
```

- **SCTP의 핵심 원리**:
  1. **Multi-homing (무중단 통신)**: 단말이 여러 IP 주소를 묶어 하나의 연결(Association)을 형성. 주 네트워크 장비나 회선 장애 발생 시, 애플리케이션 재시작 없이 즉시 백업 IP로 경로를 스위칭한다.
  2. **Multi-streaming (HoL Blocking 방지)**: 하나의 연결 내에 여러 개의 독립적인 차선을 만듦. 1번 차선에서 사고(패킷 유실)가 나도, 2번, 3번 차선의 데이터는 지연 없이 정상적으로 수신 애플리케이션에 전달된다.
  3. **4-Way Handshake**: SYN Flooding 공격을 막기 위해 상태 비저장 방식의 Cookie를 도입해 4단계로 연결을 수립한다.

---
## Ⅲ. 비교 및 연결

| 비교 항목 | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) | SCTP (Stream Control Transmission Protocol) |
|:---|:---|:---|:---|
| **연결 방식** | 1:1 연결 지향 (Connection-oriented) | 비연결 (Connectionless) | 연결 지향 (Association) |
| **신뢰성 보장** | 높음 (순서 보장, 재전송) | 낮음 (보장 안 됨) | 높음 (순서 보장, 재전송) |
| **전송 단위** | 바이트 스트림 (Byte-stream) | 메시지 단위 (Datagram) | 메시지 단위 (Message-oriented) |
| **다중 경로** | 단일 경로 (Single-homing) | 단일 경로 | **다중 경로 (Multi-homing)** |
| **스트림 처리** | 단일 스트림 (HoL Blocking 발생) | 스트림 개념 없음 | **다중 스트림 (Multi-streaming)** |
| **주요 사용처** | Web, FTP, 이메일 | DNS, 실시간 미디어, SNMP | 5G Core 제어 평면(NGAP), SIGTRAN |

---
## Ⅳ. 실무 적용 및 기술사 판단

- **SCTP 도입 한계 및 대안 (QUIC의 부상)**
  - 문제: 일반 인터넷 환경에서 SCTP를 쓰면 완벽하지만, 전 세계 라우터와 방화벽이 TCP/UDP 외의 L4 프로토콜(SCTP 번호 132)을 인지하지 못해 차단(Drop)해 버리는 `미들박스 경직화(Middlebox Ossification)` 현상이 발생함.
  - 판단: 따라서 B2C 웹 서비스 환경에서는 SCTP 도입이 불가능에 가깝다. 대신, 방화벽 통과가 보장되는 UDP 위에서 SCTP의 멀티 스트리밍 로직을 소프트웨어로 흉내 낸 **QUIC (HTTP/3)** 을 도입하는 것이 현대 서버 아키텍처의 정답이다.
- **5G 특화망(Private 5G)에서의 필수성**
  - 5G 코어 장비(AMF)와 기지국(gNB) 간에는 완벽한 이중화와 제어 신호 전달이 생명이므로, 폐쇄망 환경인 모바일 코어에서는 주저 없이 SCTP를 N2 인터페이스의 표준으로 적용해야 한다.

---
## Ⅴ. 기대효과 및 결론

- **결론**: 애플리케이션의 특성에 맞춰 TCP, UDP, SCTP를 적재적소에 배치하는 것이 네트워크 아키텍처의 기본이다.
- **기대효과**: SCTP의 멀티 호밍을 활용하면 하드웨어 L4 스위치(로드밸런서) 없이도 소프트웨어 단에서 강력한 무중단 Failover 환경을 구축할 수 있으며, HoL Blocking 없는 빠르고 신뢰성 있는 제어 인프라를 달성할 수 있다.

---
### 📌 관련 개념 맵
TCP (신뢰성) & UDP (메시지 지향) $\rightarrow$ HoL Blocking 한계 $\rightarrow$ SCTP (Multi-streaming & Multi-homing) $\rightarrow$ 5G Core (NGAP) & HTTP/3 (QUIC).

### 📈 관련 키워드 및 발전 흐름도
`TCP의 HoL Blocking / 단일 경로 한계` $\rightarrow$ `SCTP 등장 (이중화/다중화 해결)` $\rightarrow$ `통신사 망(SIGTRAN, 5G) 표준 정착` $\rightarrow$ `일반망 NAT 통과 실패 (미들박스 문제)` $\rightarrow$ `QUIC (UDP 기반 대체) 탄생`

### 👶 어린이를 위한 3줄 비유 설명
1. **TCP**는 택배 기사님이 물건 하나 주고 영수증 사인받기 전까진 절대 다음 물건을 안 주는 깐깐한 방식이에요 (정확하지만 느려요).
2. **UDP**는 우체부 아저씨가 우편함에 전단지를 마구 던져 넣고 쿨하게 떠나는 방식이에요 (빠르지만 잃어버릴 수 있어요).
3. **SCTP**는 기사님이 여러 길을 동시에 써서 배송하고, 메인 도로가 막히면 1초 만에 샛길(백업)로 방향을 틀어 기어코 배달을 해내는 슈퍼 택배 시스템이에요.
