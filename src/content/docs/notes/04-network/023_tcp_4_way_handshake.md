---
sidebar:
  order: 23
  label: "023. TCP 4-way Handshake (TCP 4-way Handshake)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "TCP 4-way Handshake•연결 해제 (TCP 4-way Handshake)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 23
extra:
  question_no: "023"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "양방향 세션 독립 종료 절차 및 TIME_WAIT 상태 관리"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TCP 4단계 핸드셰이크(TCP 4-Way Handshake)**: 전이중(Full-Duplex) 통신을 수행하던 두 호스트가 FIN(Finish)과 ACK(Acknowledgment) 제어 플래그를 4단계에 걸쳐 교환함으로써 양방향 데이터 송신 채널을 안전하게 독립 종료하는 연결 해제 절차.
- **반쪽 종료(Half-Close)**: 한쪽 호스트가 송신 채널을 닫아 더 이상 보낼 데이터가 없음을 선언하더라도, 반대쪽 호스트로부터의 데이터 수신 채널은 유지하는 상태.

</details>

- 정의/개념: 양방향 전이중 세션을 안전하게 종료하기 위해 FIN과 ACK 플래그를 상호 교환하여 송수신 채널을 독립적으로 닫는 **TCP 정상 연결 해제 절차**
- 배경/필요성: 단방향 일방적 종료 시 반대편 호스트에서 전송 중이던 잔여 데이터 유실 방지 및 지연 세그먼트 충돌 방지 요구

#### 한줄 요약
- FIN과 ACK 4단계 교환을 통해 양방향 전이중 채널을 데이터 손실 없이 독립적으로 종료한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **능동 종료(Active Close)**: 연결 해제를 먼저 요청하며 상대방에게 최초의 FIN 플래그를 전송하는 호스트.
- **수동 종료(Passive Close)**: 상대방의 FIN을 수신하고 ACK로 응답한 후, 애플리케이션 정리 완료 시 자신의 FIN을 전송하는 호스트.
- **TIME_WAIT**: 능동 종료 호스트가 최종 ACK를 전송한 후 지연 패킷 소멸과 최종 ACK 재전송을 위해 2MSL 동안 세션을 유지하는 상태.

</details>

- **반쪽 종료(Half-Close)** 를 지원하여 송신을 마친 후에도 상대방의 잔여 수신 데이터를 온전히 수신 보장
- 각 방향의 **FIN 플래그** 에 시퀀스 번호를 부여하여 마지막 전송 데이터의 손실과 재전송을 신뢰성 있게 추적
- 능동 종료 측의 **TIME_WAIT(2MSL)** 상태 유지를 통해 네트워크 잔존 패킷 혼선 방지 및 최종 ACK 유실 대비

#### 한줄 요약
- 반쪽 종료 지원으로 잔여 데이터를 보존하고, 능동 종료 측의 TIME_WAIT로 세션 정합성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **최대 세그먼트 수명(Maximum Segment Lifetime, MSL)**: IP 네트워크 상에서 패킷(세그먼트)이 소멸되지 않고 생존할 수 있는 최대 유효 시간(RFC 793 표준 권고 2분, 리눅스 60초).

</details>

```text
[ 능동 종료 호스트 (Client) ]                [ 수동 종료 호스트 (Server) ]
        ESTABLISHED                                 ESTABLISHED
             │                                           │
             ├──── 1. FIN (seq=u) ─────────────────────▶ │ (수신)
        FIN_WAIT_1                                  CLOSE_WAIT (소켓 정리)
             │                                           │
             │ ◀── 2. ACK (ack=u+1) ─────────────────────┤
        FIN_WAIT_2                                       │ (잔여 데이터 전송 가능)
             │                                           │
             │ ◀── 3. FIN (seq=v, ack=u+1) ──────────────┤ (송신 종료)
             │                                       LAST_ACK
             ├──── 4. ACK (ack=v+1) ───────────────────▶ │
        TIME_WAIT                                      CLOSED
        (2MSL 대기)                                  (종료 완료)
             │
          CLOSED (소켓 해제)
```

선의 의미: 능동 종료 호스트의 FIN_WAIT/TIME_WAIT 상태 전이 및 수동 종료 호스트의 CLOSE_WAIT/LAST_ACK 상태 전이

| 구성요소 | 책임 | 상태 전이 |
|:---|:---|:---|
| **능동 종료 호스트** | 최초 FIN 전송 후 반대편 데이터 수신 대기 및 최종 ACK 발송 후 **TIME_WAIT 유지** | `FIN_WAIT_1` $\rightarrow$ `FIN_WAIT_2` $\rightarrow$ `TIME_WAIT` |
| **수동 종료 호스트** | 최초 FIN에 대해 ACK 응답 후 애플리케이션 정리(`close()`) 후 자신의 FIN 발송 | `CLOSE_WAIT` $\rightarrow$ `LAST_ACK` $\rightarrow$ `CLOSED` |
| **반쪽 종료(Half-Close)** | 한쪽 방향의 데이터 스트림만 종료하고 역방향 데이터 스트림은 유지 | `FIN_WAIT_2` 및 `CLOSE_WAIT` 상태 |
| **TIME_WAIT 상태** | 최종 ACK 유실 시 재전송된 상대방 FIN에 응답하고 2MSL 동안 지연 패킷 소멸 대기 | 2MSL 타이머 가동 |

#### 한줄 요약
- 능동 측은 FIN_WAIT와 TIME_WAIT를 거치고, 수동 측은 CLOSE_WAIT와 LAST_ACK를 거쳐 정상 종료된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **2MSL 타이머**: 네트워크 상에서 전송 중인 지연 패킷이 완전히 소멸될 수 있도록 MSL의 2배(약 1~2분) 동안 소켓을 보류하는 타이머.

</details>

```text
1. 능동 종료: 애플리케이션 close() 호출 ➔ 1단계 FIN 패킷 전송 (FIN_WAIT_1)
            │
            ▼
2. 수동 응답: 수동 측이 2단계 ACK 전송 (CLOSE_WAIT 진입, 반쪽 종료 수립)
            │
            ▼
3. 수동 종료: 수동 측 애플리케이션 잔여 데이터 처리 완료 ➔ 3단계 FIN 전송 (LAST_ACK)
            │
            ▼
4. 최종 응답: 능동 측이 4단계 ACK 전송 ➔ TIME_WAIT(2MSL) 타이머 가동
            │
            ▼
5. 완전 종료: 수동 측은 최종 ACK 수신 즉시 CLOSED, 능동 측은 2MSL 만료 후 CLOSED
```

**동작 원리**

1. **능동 송신 종료**: 클라이언트가 `close()`를 호출하여 FIN 플래그를 전송하고 `FIN_WAIT_1` 전이
2. **수동 확인 및 대기**: 서버가 ACK를 회신하고 `CLOSE_WAIT`로 전이하여 애플리케이션에 연결 종료 통보
3. **수동 송신 종료**: 서버가 잔여 데이터 송신을 마친 후 `close()`를 호출하여 FIN을 전송하고 `LAST_ACK` 전이
4. **최종 확인**: 클라이언트가 최종 ACK를 서버로 전송하고 `TIME_WAIT` 상태로 진입
5. **소켓 자원 회수**: 서버는 ACK를 받고 즉시 소켓을 닫으며, 클라이언트는 2MSL 대기 후 소켓 해제

#### 한줄 요약
- 능동 FIN, 수동 ACK, 수동 FIN, 능동 최종 ACK 순으로 진행되며 2MSL 대기 후 완전 종료된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **임시 포트(Ephemeral Port)**: 클라이언트가 아웃바운드 연결 수립 시 운영체제로부터 동적으로 할당받는 1회용 출발지 포트(49152~65535 등).

</details>

| 비교 항목 | 능동 종료 (Active Close) | 수동 종료 (Passive Close) |
|:---|:---|:---|
| **주요 주체** | 연결 해제를 먼저 호출한 종단 (주로 클라이언트) | 해제 통보를 수신한 종단 (주로 서버) |
| **핵심 상태 경로** | `FIN_WAIT_1` $\rightarrow$ `FIN_WAIT_2` $\rightarrow$ **TIME_WAIT** | **CLOSE_WAIT** $\rightarrow$ `LAST_ACK` $\rightarrow$ `CLOSED` |
| **운영상 주요 리스크** | 빈번한 단기 연결 발생 시 **TIME_WAIT 소켓/임시 포트 고갈** | 애플리케이션 코드 결함(`close()` 미호출) 시 **CLOSE_WAIT 누수** |
| **자원 점유 해소** | 커널 파라미터(`tcp_tw_reuse` 등) 및 2MSL 경과 후 해제 | 애플리케이션 프로세스 재시작 또는 소켓 종료 로직 수정 |

#### 한줄 요약
- 능동 종료는 TIME_WAIT 포트 고갈을 관리해야 하고, 수동 종료는 CLOSE_WAIT 소켓 누수를 관리해야 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SO_REUSEADDR**: 로컬 포트가 TIME_WAIT 상태에 있더라도 동일 포트를 다른 소켓이 재바인딩할 수 있도록 허용하는 소켓 옵션.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 애플리케이션 소켓 `close()` 미수행으로 인한 **CLOSE_WAIT 소켓 고갈** | 소켓 자원 반환 예외 처리(Try-with-resources 등) 및 코드 감사 | 파일 디스크립터(FD) 누수 원천 방지 및 서버 안정성 확보 |
| 대규모 단기 요청(Short-lived HTTP)으로 인한 **TIME_WAIT 임시 포트 고갈** | **커넥션 풀링(Keep-Alive)** 도입 및 커널 **SO_REUSEADDR** 옵션 활성화 | 빈번한 핸드셰이크 제거 및 포트 고갈 방지 |
| 최종 4단계 ACK 패킷 유실로 인한 상대방 호스트의 LAST_ACK 교착 | 능동 종료 측의 **2MSL TIME_WAIT 유지** 및 수신된 FIN에 대한 ACK 재전송 | 상대방 호스트의 완전하고 정상적인 CLOSED 전이 유도 |

#### 한줄 요약
- 소켓 close() 예외 처리, HTTP 커넥션 풀링, SO_REUSEADDR 튜닝을 통해 종료 상태 누수를 방지한다.

## Ⅶ. 결론

- 고성능 대규모 분산 시스템 구축 시 **TCP 4-Way Handshake**의 특성을 고려하여, 애플리케이션 레벨의 완벽한 소켓 해제(`close()`)로 **CLOSE_WAIT 누수**를 차단하고, 백엔드 간 통신에는 **HTTP Keep-Alive 커넥션 풀링**을 적용하여 **TIME_WAIT** 부하를 최소화하는 설계를 확립

#### 한줄 요약
- 커넥션 풀링과 철저한 소켓 자원 관리를 통해 4-Way Handshake의 안정성과 성능을 보장한다.
