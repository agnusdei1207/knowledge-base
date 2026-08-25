---
sidebar:
  order: 23
  label: "023. TCP 4-way Handshake"
  badge:
    text: "기출 · 30%"
    variant: note
title: "TCP 4-way Handshake (TCP 4-way Handshake)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 23
extra:
  question_no: "23"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "양방향 세션 독립 종료 절차 및 TIME_WAIT 상태 관리"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TCP 4-Way Handshake**: 전이중(Full-Duplex) 통신 중인 두 호스트가 FIN과 ACK 플래그를 4단계에 걸쳐 교환하여 양방향 채널을 안전하게 종료하는 절차.
- **Half-Close (반쪽 종료)**: 한쪽 호스트가 송신 채널(FIN)을 닫더라도 상대방 호스트로부터의 데이터 수신 채널은 유지하는 상태.

</details>

- 정의/개념: TCP 전이중 세션을 안전하게 종료하기 위해 **FIN과 ACK 4단계 플래그 교환을 통해 양방향 송수신 채널을 독립적으로 닫는 연결 해제 프로토콜**
- 배경/필요성: 일방적 연결 단절 시 발생하는 **상대방 잔여 버퍼 데이터 유실, 지연 세그먼트와의 세션 충돌 및 소켓 자원 누수 해결 불가**

#### 한줄 요약
- FIN-ACK 4단계 교환과 TIME_WAIT 대기를 통해 잔여 데이터 손실 없이 세션을 정상 종료한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Active Close (능동 종료)**: 연결 해제(`close()`)를 먼저 호출하여 최초 FIN을 전송하고 최종 TIME_WAIT(2MSL)를 유지하는 주체.
- **Passive Close (수동 종료)**: 상대방의 FIN을 수신하고 ACK를 보낸 후 자체 `close()` 호출 시 FIN을 전송하는 주체.

</details>

- 송신 종료 후에도 상대방의 잔여 데이터를 온전히 수신하는 **반쪽 종료(Half-Close) 지원**
- 각 방향의 **FIN 플래그**에 시퀀스 번호를 부여하여 마지막 데이터 손실을 신뢰성 있게 추적
- 능동 종료 측의 **TIME_WAIT(2MSL) 상태 유지**를 통해 지연 패킷 소멸 대기 및 최종 ACK 유실 대비

#### 한줄 요약
- 반쪽 종료 지원, 독립 FIN 시퀀스 추적, TIME_WAIT(2MSL) 정합성 유지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MSL (Maximum Segment Lifetime)**: IP 네트워크 상에서 패킷이 소멸되지 않고 생존할 수 있는 최대 유효 시간 (RFC 793 권고 2분, 리눅스 60초).

</details>

```text
[TCP 4-Way Handshake 능동/수동 상태 전이 아키텍처]
|-- Active Closer (Client: 능동 종료 주체)
|   |-- ESTABLISHED -> FIN_WAIT_1 (1. FIN 전송)
|   |-- FIN_WAIT_2 (2. ACK 수신 후 반쪽 종료 수립, 잔여 데이터 수신)
|   `-- TIME_WAIT (4. 최종 ACK 전송 후 2MSL 대기) -> CLOSED
`-- Passive Closer (Server: 수동 종료 주체)
    |-- ESTABLISHED -> CLOSE_WAIT (2. 최초 FIN 수신 및 ACK 회신, 잔여 데이터 송신)
    `-- LAST_ACK (3. 애플리케이션 close() 호출 후 FIN 전송) -> CLOSED (4. 최종 ACK 수신)
```

선의 의미: 계층 및 능동 측의 FIN_WAIT/TIME_WAIT 상태와 수동 측의 CLOSE_WAIT/LAST_ACK 상태 전이가 4단계로 맞물려 종료되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 상태 전이 경로 |
|:---|:---|:---|
| **능동 종료 호스트** | 최초 FIN 전송 후 반대편 잔여 데이터 수신 대기 및 **최종 ACK 발송 후 TIME_WAIT(2MSL) 유지**| `FIN_WAIT_1` $\to$ `FIN_WAIT_2` $\to$ `TIME_WAIT` |
| **수동 종료 호스트** | 최초 FIN에 대해 ACK 응답 후 **애플리케이션 정리(`close()`) 후 자신의 FIN 발송** | `CLOSE_WAIT` $\to$ `LAST_ACK` $\to$ `CLOSED` |
| **반쪽 종료 (Half-Close)**| 한쪽 방향의 데이터 송신만 종료하고 **역방향 데이터 스트림은 유지하여 잔여 데이터 수신** | `FIN_WAIT_2` 및 `CLOSE_WAIT` 상태 |
| **TIME_WAIT 상태** | 최종 ACK 유실 시 재전송된 상대방 FIN에 응답하고 **2MSL 동안 지연 패킷 소멸 대기** | 2MSL 타이머 가동 |

#### 한줄 요약
- 능동 종료 측은 FIN_WAIT/TIME_WAIT, 수동 종료 측은 CLOSE_WAIT/LAST_ACK를 거쳐 정상 종료된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **4-Way 핸드셰이크 4단계**: 1. 능동 FIN 전송 $\to$ 2. 수동 ACK 회신 $\to$ 3. 수동 잔여 송신 완료 후 FIN 전송 $\to$ 4. 능동 최종 ACK 전송 및 TIME_WAIT.

</details>

```text
TCP 4-Way Handshake 연결 해제 파이프라인
        │
   1. [능동 FIN 전송] 클라이언트 `close()` 호출 -> FIN(Seq=u) 전송 [클라이언트: FIN_WAIT_1]
        │
   2. [수동 ACK 회신] 서버가 ACK(Ack=u+1) 전송 [서버: CLOSE_WAIT, 클라이언트: FIN_WAIT_2]
        │
   3. [수동 FIN 전송] 서버 애플리케이션 잔여 데이터 송신 완료 후 FIN(Seq=v) 전송 [서버: LAST_ACK]
        │
   4. [능동 최종 ACK 전송] 클라이언트가 ACK(Ack=v+1) 회신 [클라이언트: TIME_WAIT 진입]
   ┌────┴───────────────────────────┐
  서버 측 즉시 CLOSED 전이          클라이언트 2MSL 타이머 만료
   │                                 │
   ▼                                 ▼
[서버 소켓 자원 회수 완료]          [클라이언트 소켓 완전 해제 (CLOSED)]
```

#### 한줄 요약
- 능동 FIN → 수동 ACK → 수동 FIN → 능동 최종 ACK 순으로 진행되며 2MSL 대기 후 완전 종료된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Active Close vs Passive Close**: 연결을 먼저 닫는 주체(TIME_WAIT 리스크)와 종료 요청을 수신하는 주체(CLOSE_WAIT 누수 리스크).

</details>

| 비교 항목 | 능동 종료 (Active Close) | 수동 종료 (Passive Close) |
|:---|:---|:---|
| **연결 해제 주체** | **연결 해제를 먼저 호출한 종단 (주로 클라이언트/WAS)** | **해제 요청을 수신한 종단 (주로 DB/서버)** |
| **핵심 상태 경로** | `FIN_WAIT_1` $\to$ `FIN_WAIT_2` $\to$ **TIME_WAIT** | **CLOSE_WAIT** $\to$ `LAST_ACK` $\to$ `CLOSED` |
| **운영상 주요 리스크** | 빈번한 단기 연결 발생 시 **TIME_WAIT 소켓/임시 포트 고갈** | 애플리케이션 코드 결함(`close()` 미호출) 시 **CLOSE_WAIT 누수** |
| **자원 점유 해소** | 커널 파라미터(`SO_REUSEADDR`) 및 **2MSL 타이머 경과 후 해제**| 애플리케이션 프로세스 재시작 또는 소켓 반환 로직 수정 |

#### 한줄 요약
- 능동 종료는 TIME_WAIT 포트 고갈을 관리해야 하고, 수동 종료는 CLOSE_WAIT 소켓 누수를 관리해야 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SO_REUSEADDR**: 로컬 포트가 TIME_WAIT 상태에 있더라도 동일 포트를 새 소켓이 즉시 재바인딩할 수 있도록 허용하는 소켓 옵션.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 애플리케이션 소켓 `close()` 미수행으로 인한 **CLOSE_WAIT 누수 및 FD 고갈** | **소켓 자원 반환 예외 처리(Try-with-resources) 및 정적 코드 분석** | 파일 디스크립터(FD) 누수 원천 차단 |
| 대규모 단기 요청(Short-lived HTTP)으로 인한 **TIME_WAIT 임시 포트 고갈** | **`HTTP Keep-Alive 커넥션 풀링` 도입 및 소켓 `SO_REUSEADDR` 활성화** | 빈번한 핸드셰이크 제거 및 포트 고갈 방지 |
| 최종 4단계 ACK 패킷 유실로 상대방 호스트의 LAST_ACK 교착 발생 | **능동 종료 측의 `2MSL TIME_WAIT 유지` 및 수신 FIN에 ACK 재전송** | 상대방 호스트의 완전한 CLOSED 전이 유도 |
| 마이크로서비스 간 빈번한 TCP 세션 생성/종료로 인한 지연 | **gRPC / HTTP/2 멀티플렉싱 도입으로 `단일 TCP 연결 공유`** | 4-Way 핸드셰이크 오버헤드 90% 이상 절감 |

#### 한줄 요약
- Try-with-resources 반환, HTTP Keep-Alive 커넥션 풀링, SO_REUSEADDR, gRPC 멀티플렉싱으로 운영한다.

## Ⅶ. 결론

- 고성능 대규모 분산 환경에서 소켓 자원 고갈을 방지하기 위해 **TCP 4-Way Handshake의 능동/수동 상태 머신을 고려한 철저한 소켓 반환(`close()`) 거버넌스를 수립**하고, **HTTP Keep-Alive 커넥션 풀링과 gRPC 멀티플렉싱 및 커널 SO_REUSEADDR 튜닝**을 결합하여 고신뢰성 분산 통신 인프라 완성

#### 한줄 요약
- TCP 4-Way Handshake는 FIN과 ACK 4단계 교환을 통해 양방향 데이터를 손실 없이 정리하고 소켓 자원을 안전하게 회수하는 핵심 연결 종료 기술이다.