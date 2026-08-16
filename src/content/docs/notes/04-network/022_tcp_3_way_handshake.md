---
sidebar:
  order: 22
  label: "022. TCP 3-way Handshake (TCP 3-way Handshake)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "TCP 3-way Handshake (TCP 3-way Handshake)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-network"
weight: 22
extra:
  question_no: "022"
  source_status: "기출"
  source_history: "125회, 128회, 129회, 132회"
  priority: 70
  priority_note: "설명•비교형: 125•132회 연결 설정•해제 반복"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **전송 제어 프로토콜 3단계 연결 설정(Transmission Control Protocol Three-Way Handshake, TCP 3-way handshake)**: SYN•SYN/ACK•ACK으로 양방향 초기 순서 번호와 연결 상태를 합의하는 절차이다.

</details>

- 정의/개념: **TCP 3-way handshake**는 SYN•SYN-ACK•ACK로 양방향 도달성과 초기 순서 번호를 확인하는 절차이다.
- 배경/필요성: 연결 전에는 상대 도달성과 양방향 순서 기준을 확인할 수 없다.

#### 한줄 요약

- 3단계 핸드셰이크(SYN-SYN/ACK-ACK)를 통해 클라이언트와 서버 간 양방향 도달성을 검증하고 초기 순서 번호(ISN)를 동기화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **동기화(Synchronize, SYN)**: TCP 연결 시작과 초기 순서 번호를 제안하는 플래그이다.
- **확인 응답(Acknowledgment, ACK)**: 상대 순서 번호의 수신을 확인하는 플래그이다.
- **초기 순서 번호(Initial Sequence Number, ISN)**: 각 송신 방향의 초기 바이트 순서 번호이다.
- **최대 세그먼트 크기(Maximum Segment Size, MSS)**: TCP 세그먼트에 담을 수 있는 최대 데이터 크기이다.

</details>

- 독립 **ISN** 교환으로 양방향 순서 기준을 정한다.
- **SYN** 옵션에서 **MSS** 등 연결 매개변수를 협상한다.
- **ACK**로 상대 ISN 수신을 확인해야 연결이 완료된다.

#### 한줄 요약

- SYN 세그먼트 옵션 필드에서 최대 세그먼트 크기(MSS), 윈도 스케일, SACK 허용 등 연결 매개변수를 협상한다.


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **리슨 소켓(Listen Socket)**: 서버 포트에서 새 연결 요청을 받는 소켓이다.
- **SYN 큐(SYN Queue)**: 최종 ACK를 기다리는 반쪽 연결을 보관하는 큐이다.
- **Accept 큐(Accept Queue)**: 응용이 인수할 때까지 완료 연결을 보관하는 큐이다.

</details>

```text
수신 대기 소켓
└── 반쪽 연결 큐
    └── 완료 연결 큐
        └── 연결 소켓
```

선의 의미: 각 선은 서버 포트의 연결 요청 수용, 반쪽•완료 연결 상태 보관과 종단 주소•ISN•TCP 상태를 가진 연결 소켓 사이의 관리 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 수신 대기 소켓 | **리슨 소켓**이 서버 포트에서 새 SYN 수신 |
| 반쪽 연결 큐 | **SYN 큐**에 최종 ACK 대기 상태 저장 |
| 완료 연결 큐 | **Accept 큐**에 응용 인수 전 완료 연결 저장 |
| 연결 소켓 | 종단 주소•**ISN**•TCP 상태 관리 |

#### 한줄 요약

- 서버는 SYN을 수신하면 반쪽 연결 큐에 상태를 저장하고, 최종 ACK가 도착하면 완료 연결 큐로 이동하여 두 큐로 연결 상태를 관리한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **윈도 배율(Window Scale)**: 큰 TCP 수신 윈도를 표현하도록 윈도 필드의 배율을 정하는 옵션이다.
- **반쪽 연결 상태**: 서버가 클라이언트의 SYN을 받고 최종 ACK를 기다리는 연결 상태이다.
- **SYN-ACK**: 서버가 클라이언트 ISN을 확인하고 자신의 ISN을 제안하는 응답 메시지이다.
- **최종 ACK**: 클라이언트가 서버 ISN의 수신을 확인하는 마지막 설정 메시지이다.
- **완료 연결 상태**: 양방향 ISN 확인을 마쳐 응용이 인수할 수 있는 연결 상태이다.

</details>

```text
클라이언트: SYN 전송
        |
        v
서버: 1. 반쪽 연결 상태
        |
        v
서버: 2. SYN-ACK 전송
        |
        v
클라이언트: 3. 최종 ACK 전송
        |
        v
서버: 4. 완료 연결 상태
        |
        `-- 응용 인수 대기
```

### 동작 원리

1. **반쪽 연결 상태**: 클라이언트 **ISN**과 **윈도 배율** 등 옵션을 저장한다.
2. **SYN-ACK**: 클라이언트 ISN을 확인하고 서버 ISN을 제안한다.
3. **최종 ACK**: 서버 ISN 수신 확인으로 양방향 도달성을 검증한다.
4. **완료 연결 상태**: 반쪽 연결을 설정 완료 상태로 전환한다.

#### 한줄 요약

- 클라이언트와 서버가 각자의 ISN을 제안하고 상대의 ISN을 ACK로 확인해야 양방향 도달성이 검증되어 연결이 완료된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TCP 연결 설정**: SYN과 ACK로 양방향 연결 상태를 만드는 절차이다.
- **TCP 연결 종료**: 각 송신 방향을 독립적으로 닫는 절차이다.
- **FIN(Finish)**: TCP의 한쪽 송신 방향을 닫는 제어 플래그이다.
- **연결 상태(Connection State)**: CLOSED에서 연결 설정을 시작해 양쪽 확인이 끝나면 ESTABLISHED가 되고 종료 절차 뒤 다시 해제되는 TCP 상태이다.

</details>

| 연결 절차 | 목적 | 핵심 상태 전이 |
|:---|:---|:---|
| TCP 연결 설정 | 데이터 전 양방향 도달성•ISN 확인 | **연결 상태**를 `CLOSED`에서 `ESTABLISHED`로 전환 |
| TCP 연결 종료 | **FIN**으로 양방향 송신 채널을 독립 종료 | `FIN-WAIT`•`CLOSE-WAIT`를 거쳐 연결 해제 |

> 요약: 설정은 3단계, 방향별 종료는 4단계가 핵심이다.

#### 한줄 요약

- 연결 시작은 한쪽 요청에 양쪽 확인을 묶을 수 있지만 종료는 각 방향의 남은 데이터가 달라 따로 닫는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SYN Flood**: 대량 SYN으로 서버의 반쪽 연결 자원을 고갈시키는 공격이다.
- **SYN Cookie**: 최종 ACK 검증 전까지 서버의 연결 상태 저장을 늦추는 방어 기법이다.
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 경로에서 단편화 없이 전달할 수 있는 최대 패킷 크기이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **SYN Flood**로 반쪽 연결 큐 고갈 | **SYN Cookie**•요청률 제한 | 신규 연결의 가용성 유지 |
| **MSS**가 경로 **MTU**보다 크면 패킷 폐기 | 경로 MTU에 맞춰 MSS 조정 | 경로 MTU 블랙홀 방지 |
| 최종 ACK 누락으로 반쪽 연결 장기 점유 | 재전송 횟수•대기시간 제한 | 연결 상태 메모리 회수 |
| 중간장비가 SYN 옵션을 변경 | 양단 패킷 캡처로 옵션 대조 | 처리량 저하의 협상 원인 식별 |

#### 한줄 요약

- 반쪽 연결 큐가 고갈되면 상태 저장을 지연하는 SYN Cookie를 적용하고, 세그먼트가 경로 MTU를 초과하면 MSS를 축소하여 연결 자원을 보호한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **경로 최대 전송 단위 블랙홀(Path Maximum Transmission Unit Black Hole, 경로 MTU 블랙홀)**: 큰 패킷이 폐기되지만 크기 조정 신호가 돌아오지 않아 통신이 멈추는 현상이다.

</details>

- 양방향 **ISN**을 확인한 뒤 연결하고 큐 압력 시 **SYN Cookie**를 적용하며 **경로 MTU 블랙홀**을 피하도록 MSS를 조정한다.

#### 한줄 요약

- 양쪽이 ISN과 MSS를 확인한 뒤 연결하되 반쪽 연결 큐가 포화되면 SYN Cookie로 상태 저장을 지연한다.
