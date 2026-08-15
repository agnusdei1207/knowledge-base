---
sidebar:
  order: 30
  label: "030. TCP TIME_WAIT 상태 (TIME_WAIT State)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "TCP TIME_WAIT 상태 (TIME_WAIT State)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 30
extra:
  question_no: "030"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "설명형: 132회 TCP 종료 상태 직접 출제"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **시간 대기(Time Wait, TIME_WAIT)**: 최종 ACK를 보낸 종단이 이전 연결의 지연 세그먼트 소멸까지 상태를 유지하는 TCP 종료 상태이다.
- **확인 응답(Acknowledgment, ACK)**: 세그먼트 수신을 확인하는 응답이다.
- **전송 제어 프로토콜(Transmission Control Protocol, TCP)**: 연결 상태를 관리하는 전송 프로토콜이다.
- **최대 세그먼트 수명 두 배(Twice the Maximum Segment Lifetime, 2MSL)**: 이전 연결의 지연 세그먼트가 사라지도록 기다리는 시간이다.
</details>

- 정의/개념: **TIME_WAIT**은 **TCP** 능동 종료 측이 최종 **ACK** 뒤 연결 정보를 **2MSL** 동안 유지하는 상태이다.
- 배경/필요성: 최종 ACK 유실과 즉시 4-튜플 재사용은 종료•재연결 혼선을 일으킨다.

#### 한줄 요약

- 통화를 끊은 뒤 늦은 옛 음성이 새 통화에 섞이지 않도록 마지막 확인증과 연결 주소를 2MSL 동안 보관한다.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **능동 종료(Active Close)**: 먼저 FIN을 보내 연결 종료를 시작하는 역할이다.
- **종료(Finish, FIN)**: 송신 방향 종료를 알리는 TCP 제어 플래그이다.
</details>

- 재전송 **FIN**에 ACK로 다시 응답해 상대 종료를 완료한다.
- 4-튜플 재사용을 늦춰 이전 연결의 세그먼트를 격리한다.
- **능동 종료**가 집중되면 임시 포트 조합이 고갈될 수 있다.

#### 한줄 요약

- 퇴실 확인증을 잠시 보관하는 것이 정상인 것처럼 TIME_WAIT 자체는 오류가 아니며 새 입장이 막힐 때 임시 포트 고갈을 점검한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **4-튜플(Four-tuple)**: 양쪽 주소와 포트로 구성한 TCP 연결 식별값이다.
- **지연 중복 세그먼트(Delayed Duplicate Segment)**: 종료 후 늦게 도착한 이전 연결의 데이터이다.
</details>

```text
TIME_WAIT 상태
├── 2MSL 타이머
└── 연결 4-튜플
```

선의 의미: TIME_WAIT 상태가 종료 연결을 격리하는 2MSL 타이머와 이전 연결을 식별하는 4-튜플을 함께 보유하는 정적 포함 관계이다.

| 구성요소 | 책임 |
|:---|:---|
| TIME_WAIT 상태 | **TIME_WAIT**이 FIN 재수신 시 ACK 재응답 정보 유지 |
| 2MSL 타이머 | **2MSL** 동안 **지연 중복 세그먼트** 소멸 대기 |
| 연결 4-튜플 | **4-튜플**로 이전•신규 TCP 연결 식별 |

#### 한줄 요약

- TIME_WAIT 상태의 TCB가 4-튜플 식별자와 2MSL 타이머를 함께 유지하여 지연된 이전 세그먼트와 새 연결을 구별한다.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **최종 확인 대기(Last Acknowledgment, LAST_ACK)**: 수동 종료 종단이 마지막 FIN의 ACK를 기다리는 상태이다.
- **최종 ACK 전송**: 능동 종료 종단이 수동 종단의 마지막 FIN 수신을 확인하는 절차이다.
- **연결 4-튜플 보존**: 이전 연결의 양쪽 주소와 포트를 TIME_WAIT 상태에 유지하는 절차이다.
- **2MSL 타이머 시작**: 이전 연결의 지연 세그먼트가 사라질 대기 시간을 시작하는 절차이다.
- **ACK 재응답**: 상대가 FIN을 재전송하면 최종 확인 응답을 다시 보내는 절차이다.
- **연결 상태 제거**: 2MSL이 끝난 연결의 TIME_WAIT 상태와 4-튜플을 해제하는 절차이다.
</details>

```text
수동 FIN 수신
      |
      v
1. 최종 ACK 전송
      |
      v
2. 연결 4-튜플 보존
      |
      v
3. 2MSL 타이머 시작
      |
      +-- FIN 재수신
      |      |
      |      v
      |   4. ACK 재응답
      |      |
      |      `-- TIME_WAIT 유지
      |
      `-- 2MSL 만료
             |
             v
      5. 연결 상태 제거
```

### 동작 원리

1. **최종 ACK 전송**: 상대의 **LAST_ACK** 종료를 유도한다.
2. **연결 4-튜플 보존**: 이전 연결 식별 정보를 유지한다.
3. **2MSL 타이머 시작**: 지연 세그먼트 소멸을 대기한다.
4. **ACK 재응답**: 재전송 FIN에 최종 확인을 반복한다.
5. **연결 상태 제거**: 2MSL 뒤 4-튜플을 해제한다.

#### 한줄 요약

- 상대가 마지막 확인증을 못 받아 종료표를 다시 보내면 같은 확인증을 되돌려 주고 2MSL 시계가 끝난 뒤 연결표를 지운다.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **종료 대기 2(Finish Wait 2, FIN_WAIT_2)**: 로컬 FIN의 ACK 뒤 상대 FIN을 기다리는 상태이다.
- **종료 대기(Close Wait, CLOSE_WAIT)**: 상대 FIN 뒤 로컬 응용의 종료를 기다리는 상태이다.
- **파일 서술자(File Descriptor, FD)**: 응용이 열린 소켓을 참조하는 운영체제 번호이다.
</details>

| TCP 종료 대기 상태 | **TIME_WAIT** | **FIN_WAIT_2** | **CLOSE_WAIT** |
|:---|:---|:---|:---|
| 적용 기준 | 최종 ACK 송신 뒤 | 로컬 FIN의 ACK 수신 뒤 | 상대 FIN 수신 뒤 |
| 핵심 특징 | FIN 재응답•2MSL 격리 | 상대 FIN 대기 | 로컬 소켓 종료 대기 |
| 한계 | 임시 포트 조합 부족 | 연결 상태 장기 점유 | 소켓•**FD** 미회수 |

> 요약: **TIME_WAIT 상태** — 시간, FIN_WAIT_2는 상대 FIN, CLOSE_WAIT은 로컬 종료 대기가 핵심이다.

#### 한줄 요약

- 세 대기실 중 TIME_WAIT은 시계, FIN_WAIT_2는 상대의 퇴실표, CLOSE_WAIT은 로컬 응용의 문 닫기를 기다린다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **임시 포트(Ephemeral Port)**: 새 연결에 일시 할당하는 출발지 포트이다.
- **최대 세그먼트 수명(Maximum Segment Lifetime, MSL)**: 세그먼트가 네트워크에 남을 수 있는 최대 시간이다.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 짧은 연결로 **TIME_WAIT** 과다 누적 | 능동 종료 주체•**임시 포트** 범위 조정 | 신규 연결용 **4-튜플** 확보 |
| 2MSL 전 4-튜플 재사용 | TCP 타임스탬프•재사용 안전성 검증 | 이전 연결의 지연 세그먼트 혼입 방지 |
| 최종 ACK 유실 뒤 FIN 재전송 | **2MSL** 동안 연결 정보 유지 | 재전송 FIN에 ACK 재응답 |
| 근거 없는 TIME_WAIT 타이머 단축 | 경로 **MSL**•재연결 간격 계측 | 새 연결과 이전 세그먼트 격리 |

#### 한줄 요약

- 퇴실 대기표가 쌓이면 확인 시간을 없애지 말고 어느 쪽이 먼저 닫는지와 새 손님용 임시 포트 범위를 조정한다.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **TCP 타임스탬프(TCP Timestamp)**: 송신 시각으로 오래된 세그먼트를 구별하는 TCP 옵션이다.
</details>

- 최종 ACK 후 **TCP 타임스탬프**와 2MSL로 **지연 중복 세그먼트** 위험이 사라질 때까지 **TIME_WAIT**을 유지한다.

#### 한줄 요약

- 마지막 확인증을 보낸 뒤 늦은 옛 짐이 사라질 때까지 퇴실표를 보관하는 것이 TIME_WAIT의 정상 역할이다.
