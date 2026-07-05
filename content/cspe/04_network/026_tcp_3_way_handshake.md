---
title: "TCP 3-way handshake (TCP 3-way Handshake)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-network"
weight: 26
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: TCP 3-way Handshake는 **전송 계층(L4)**에서 양 종단(End-to-End) 간 **신뢰성 있는 통신**을 시작하기 전, **시퀀스 번호(ISN)·수신 버퍼(Window)·MSS를 동기화**하는 3단계 연결 수립 절차임.
- **왜 필요한가**: UDP와 달리 TCP는 데이터 유실 검출, 순서 재조합, 흐름 제어를 보장해야 함. 이를 위해 양측이 사용할 시작 번호(ISN)와 한 번에 받을 수 있는 양(Window)을 미리 합의해야 함.
- **핵심 직관**: "여보세요? 제 말 들리세요?(SYN)" → "네, 들립니다. 제 말도 들리시나요?(SYN-ACK)" → "네, 잘 들립니다(ACK)" — 양쪽의 송수신 가능 상태를 확인한 후 본론을 시작하는 과정.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| **SYN (Synchronize)** | 연결 요청 및 시퀀스 번호 동기화 신호 | "대화 시작할까요? 제 번호는 X입니다" |
| **ACK (Acknowledge)** | 데이터 수신 확인 신호 | "네, X+1번부터 보내주세요" |
| **ISN (Initial Seq Number)** | 각 방향별 데이터 순서 번호의 시작점 (난수 생성) | 택배 송장 번호의 시작점 |
| **MSS (Max Segment Size)** | IP 단편화 없이 전송 가능한 TCP 페이로드 최대 크기 | 택배 상자의 최대 용량 (보통 1460B) |
| **Window Size** | 수신 측이 한 번에 받을 수 있는 데이터 여유 공간 | 수하물 컨베이어 벨트의 남은 자리 |
| **SYN Cookie** | SYN Flood 공격 방어 기술 (서버 자원 선할당 방지) | 번호표 대신 손님 이름을 영수증에 적어 발급 |

## 깊이 이해
- **1단계 (SYN)**: 클라이언트가 서버에 연결을 요청하며 자신의 시작 번호(Seq=X)를 보냄. 이때 MSS, Window Scale 등 통신 옵션도 제안함.
- **2단계 (SYN/ACK)**: 서버는 클라이언트의 번호를 확인(Ack=X+1)하고, 자신의 시작 번호(Seq=Y)를 실어 보냄. 이 단계에서 서버는 연결을 위한 메모리(TCB)를 할당함.
- **3단계 (ACK)**: 클라이언트가 서버의 번호를 확인(Ack=Y+1)하여 응답함. 이제 양측은 신뢰할 수 있는 상태(**ESTABLISHED**)가 되어 실제 데이터를 주고받음.
- **보안 이슈 (SYN Flood)**: 공격자가 1단계만 계속 보내고 3단계를 보내지 않으면, 서버는 2단계 상태(Half-open)로 메모리를 계속 점유하다가 뻗어버림. 이를 막기 위해 **SYN Cookie**나 **백로그 큐 확대**가 필요함.
- **성능 이슈 (RTT)**: 데이터를 보내기도 전에 최소 1-RTT(왕복 시간)가 소요됨. 이를 줄이기 위해 재연결 시 0-RTT를 지원하는 **TFO(TCP Fast Open)**나 **QUIC(032)**이 등장함.

## 연결 개념
- **TCP 4-way Handshake (027)**: 연결을 종료하는 4단계 절차.
- **TCP Flow Control (028)**: 3-way에서 합의한 Window Size를 활용한 흐름 제어.
- **QUIC / HTTP/3 (032)**: 3-way의 RTT 지연을 극복한 차세대 프로토콜.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 3-way Handshake는 양 종단 간 ISN, MSS, Window 파라미터를 동기화하여 신뢰성 있는 전송 채널을 수립하는 절차임.
> 2. **가치**: 데이터의 순서 보장, 유실 검출, 흐름 제어의 기반을 마련하며, 난수 기반 ISN으로 세션 하이재킹을 방지함.
> 3. **판단 포인트**: 연결 수립의 1-RTT 지연과 SYN Flood 취약점(Half-open 상태 자원 점유)을 TFO 및 SYN Cookie 등으로 보완하는 설계가 핵심임.

## Ⅰ. 개요 및 필요성
- **정의**: 비연결성 IP 위에서 신뢰성 있는 전송을 위해 양측의 통신 파라미터를 동기화하는 3단계 연결 설정 프로세스.
- **필요성**:
    1. **신뢰성 보장**: 패킷 유실 시 재전송 및 순서 재조합을 위한 시퀀스 번호 합의.
    2. **성능 최적화**: 가용 대역폭 및 수신 버퍼 크기에 맞는 MSS와 Window Size 결정.

## Ⅱ. TCP 3-way Handshake 동작 메커니즘

### 1. 3단계 상태 전이도 및 제어 플래그
```text
[Client: CLOSED]                        [Server: LISTEN]
       |                                       |
  (1) SYN (Seq=X) ---------------------------> | (SYN_RCVD) : Half-open
       |                                       |
  (SYN_SENT) <---------- SYN/ACK (Seq=Y, Ack=X+1) (2)
       |                                       |
  (3) ACK (Seq=X+1, Ack=Y+1) ----------------> | (ESTABLISHED)
       |                                       |
[Client: ESTABLISHED]                   [Server: ESTABLISHED]
```

### 2. 주요 교환 파라미터 및 역할
| 파라미터 | 역할 | 특징 |
|:---|:---|:---|
| **ISN (Initial Seq #)** | 시퀀스 번호의 시작점 설정 | 세션 하이재킹 방지를 위해 난수로 생성 |
| **MSS (Max Segment Size)** | 최대 세그먼트 크기 합의 | 보통 MTU(1500) - IP(20) - TCP(20) = 1460Byte |
| **Window Size** | 수신 가능한 버퍼 크기 통보 | 슬라이딩 윈도우 흐름 제어의 기준값 |

## Ⅲ. 보안 취약점 및 대응 방안: SYN Flood
- **공격 원리**: 위조된 IP로 다량의 SYN 요청을 보낸 후 ACK를 응답하지 않아 서버의 **Backlog Queue(Half-open 자원)**를 고갈시킴.
- **대응 기술**:
    1. **SYN Cookie**: SYN 수신 시 자원을 할당하지 않고, Seq 번호에 해시값을 담아 보낸 뒤 나중에 ACK가 오면 검증하여 연결.
    2. **Backlog Queue 확장**: 시스템 설정(`tcp_max_syn_backlog`)을 통해 수용량 확대.
    3. **First Packet Drop**: 첫 SYN을 드롭하고 재전송을 요청하는 클라이언트만 정상으로 판단.

## Ⅳ. 성능 최적화 기술 (Latency 극복)
- **TCP Fast Open (TFO)**: RFC 7413. 이전에 연결했던 클라이언트가 SYN 패킷에 Cookie와 데이터를 함께 실어 보내 0-RTT 데이터 전송 구현.
- **Window Scale**: 기본 16비트 Window Size(64KB)를 최대 1GB까지 확장하여 고대역폭 네트워크 성능 향상.
- **Selective ACK (SACK)**: 유실된 특정 세그먼트만 재전송하도록 지정하여 불필요한 중복 전송 방지.

## Ⅴ. TCP vs UDP vs QUIC 연결 수립 비교
| 구분 | TCP (3-way) | UDP (Connectionless) | QUIC (HTTP/3) |
|:---|:---|:---|:---|
| **연결 방식** | 1-RTT (3-way) | 없음 (Best Effort) | 1-RTT (최초), 0-RTT (재접속) |
| **보안(TLS)** | 별도 수행 (추가 RTT) | 불가 | 기본 내장 (통합 Handshake) |
| **주요 용도** | HTTP/1.1, 2.0, FTP, SSH | DNS, 스트리밍, 게임 | HTTP/3, 모바일 앱 |

## Ⅵ. 실무 적용 전략 및 결론
- **전략**: 고성능 서버 구축 시 `tcp_syncookies` 활성화를 기본으로 하되, 대량 접속 환경에서는 `somaxconn` 튜닝을 병행하여 연결 유실 최소화.
- **결론**: TCP 3-way Handshake는 신뢰성의 표준이나, 1-RTT 지연과 보안 취약점이 한계임. 향후 웹 트래픽은 전송과 보안을 통합한 **QUIC**으로 전환되며 Latency를 극히 낮추는 방향으로 진화할 것임.

### 🔀 문제 유형별 목차 전환

| 유형 | Ⅱ·Ⅲ 강조 (기초/보안) | Ⅳ·Ⅴ 강조 (심화/성능) |
|:---|:---|:---|
| **기본형** | Handshake 3단계 상세 절차 및 상태 전이 | SYN Flood 공격 원리 및 대응(SYN Cookie) |
| **성능형** | ISN/MSS/Window 파라미터의 의미 | TFO 및 QUIC을 활용한 연결 수립 최적화 방안 |
