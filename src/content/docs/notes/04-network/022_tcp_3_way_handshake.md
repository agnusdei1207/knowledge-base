---
sidebar:
  order: 22
  label: "022. TCP 3-way Handshake"
  badge:
    text: "기출 · 70%"
    variant: note
title: "TCP 3-way Handshake (TCP 3-way Handshake)"
date: "2026-08-26T13:37:53+09:00"
tags:
  - "notes-network"
weight: 22
extra:
  question_no: "22"
  source_status: "기출"
  source_history: "125회, 128회, 129회, 132회"
  priority: 70
  priority_note: "설명•비교형: 125•132회 연결 설정•해제 반복"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TCP 3-Way Handshake**: TCP 연결 지향 통신 수립을 위해 SYN, SYN-ACK, ACK 3단계 메시지 교환으로 양방향 도달성을 검증하고 ISN을 동기화하는 절차.
- **ISN (Initial Sequence Number)**: TCP 세션 연결 시 데이터 스트림의 시작 바이트 위치를 난수 기반으로 할당하는 32비트 초기 순서 번호.

</details>

- 정의/개념: 송수신 호스트 간 **SYN, SYN-ACK, ACK 3단계 교환을 통해 양방향 도달성을 검증하고 ISN 및 옵션을 동기화하는 TCP 연결 설정 프로토콜**
- 배경/필요성: 비연결형 전송 시 발생하는 **수신 호스트 준비 상태 미확인에 따른 세그먼트 유실, 순서 역전 및 버퍼 오버플로우 방어 불가**

#### 한줄 요약
- SYN-SYN+ACK-ACK 3단계를 통해 양방향 가용성과 난수 ISN을 동기화하여 신뢰성 세션을 연다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MSS (Maximum Segment Size)**: 핸드셰이크 옵션 필드에서 IP/TCP 헤더를 제외하고 단일 세그먼트에 실을 수 있는 최대 페이로드 바이트 크기.
- **Window Scaling**: 16비트(64KB) 기본 윈도우 크기 한계를 극복하기 위해 최대 1GB까지 윈도우 버퍼를 확장하는 TCP 옵션.

</details>

- 예측 불가능한 의사 난수 생성을 통해 세션 하이재킹을 차단하는 **초기 순서 번호(ISN) 무작위화**
- 종단 간 경로 MTU에 맞추어 최적 세그먼트 크기를 합의하는 **MSS(Maximum Segment Size) 옵션 협상**
- 대용량 대역폭 활용을 위한 **Window Scaling 및 SACK(선택적 재전송) 기능 상호 합의**

#### 한줄 요약
- ISN 무작위화, MSS 크기 합의, 윈도우 스케일링 협상을 통해 최적의 전송 파라미터를 확정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SYN Queue (반쪽 연결 큐)**: 클라이언트의 SYN을 받고 SYN-ACK를 보낸 후 최종 ACK를 기다리는 반개방(Half-Open) 상태 소켓 대기열.
- **Accept Queue (완료 연결 큐)**: 3-Way Handshake가 완료되어 애플리케이션 `accept()` 호출을 대기하는 ESTABLISHED 상태 소켓 대기열.

</details>

```text
[서버 커널 TCP 연결 관리 및 소켓 큐 구조]
|-- 리슨 소켓 (연결 요청 수신)
|-- SYN 큐 (Half-Open 소켓 보관)
|-- Accept 큐 (ESTABLISHED 소켓 보관)
`-- TCP 제어 플래그 (SYN·ACK·FIN·RST)
```

선의 의미: 계층 및 클라이언트의 SYN이 SYN 큐에 임시 보관된 후 최종 ACK가 도착하면 Accept 큐로 이동하여 애플리케이션에 인계되는 구조

| 구성요소 | 책임 |
|:---|:---|
| 리슨 소켓 | 포트별 **신규 SYN 요청 수신** |
| SYN 큐 | **Half-Open 소켓 정보 보관** |
| Accept 큐 | **ESTABLISHED 소켓 수락 대기** |
| TCP 제어 플래그 | **SYN·ACK·FIN·RST 상태 제어** |

#### 한줄 요약
- 리슨 소켓, SYN 큐, Accept 큐, TCP 제어 플래그가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **TCP 상태 전이 3단계**: 1. SYN 전송(SYN_SENT) $\to$ 2. SYN-ACK 수신(SYN_RCVD) $\to$ 3. 최종 ACK 전송(ESTABLISHED).

</details>

```text
TCP 3-Way Handshake 상태 머신
        │
   1. [SYN 전송] 클라이언트 -> 서버 (Seq=x, SYN=1) [클라이언트: SYN_SENT]
        │
   2. [SYN-ACK 응답] 서버 -> 클라이언트 (Seq=y, Ack=x+1, SYN=1, ACK=1) [서버: SYN_RCVD]
        │
   3. [최종 ACK 전송] 클라이언트 -> 서버 (Seq=x+1, Ack=y+1, ACK=1) [클라이언트: ESTABLISHED]
        │
   ▼
[서버 연결 확정] 서버 Accept 큐 적재 및 ESTABLISHED 전이 후 양방향 데이터 통신 개시
```

#### 한줄 요약
- 클라이언트 SYN 전송 → 서버 SYN-ACK 응답 → 클라이언트 최종 ACK 전송 순으로 세션이 확립된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **3-Way Handshake (연결 수립)** vs **4-Way Handshake (연결 종료)**: 양방향 동시 합의(3단계)와 잔여 데이터 처리를 위한 단계적 반개방 종료(4단계).

</details>

| 비교 항목 | 연결 설정 (3-Way Handshake) | 연결 종료 (4-Way Handshake) |
|:---|:---|:---|
| 프로토콜 핵심 목적 | **양방향 도달성 검증, ISN 및 옵션 동기화** | **잔여 버퍼 데이터 송수신 완료 후 세션 정상 자원 회수** |
| 사용 제어 플래그 | **SYN, ACK 플래그** | **FIN, ACK 플래그** |
| 메시지 교환 횟수 | **3단계 (서버의 SYN과 ACK를 단일 패킷으로 통합)**| **4단계 (양방향 데이터 송신 완료 시점이 상이하여 분리)**|
| 핵심 상태 전이 | `CLOSED` $\to$ `SYN_SENT` $\to$ `ESTABLISHED` | `ESTABLISHED` $\to$ `FIN_WAIT` $\to$ `TIME_WAIT` $\to$ `CLOSED` |

#### 한줄 요약
- 연결 수립은 3회 교환으로 동기화하고, 연결 종료는 잔여 데이터 처리를 위해 4회 교환으로 분리 종료한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SYN Flood Attack**: 공격자가 위조된 IP로 수만 건의 SYN 패킷을 난사하고 최종 ACK를 보내지 않아 서버의 SYN 큐를 고갈시키는 DoS 공격.
- **SYN Cookie**: SYN 큐 메모리를 할당하지 않고, 클라이언트 정보와 비밀키를 암호화 해시한 값을 ISN으로 만들어 반환하는 방어 기법 (RFC 4987).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공격자의 대량 SYN 요청으로 서버 SYN 큐 고갈(SYN Flood) | **리눅스 커널 `SYN Cookie (tcp_syncookies=1)` 활성화** | 상태 저장 없이 정상 유저 접속 100% 보장 |
| 합의된 MSS가 중간 경로 MTU보다 커서 발생하는 패킷 드롭 | **경로 MTU 탐색(PMTUD) 및 `TCP MSS Clamping` 값 최적화** | 패킷 단편화 오버헤드 및 블랙홀 방지 |
| 모바일 전파 음영 지역 진입 시 미완료 Half-Open 소켓 누적 | **`tcp_synack_retries` 횟수 축소 및 백오프 타임아웃 단축** | 커널 메모리 자원 신속 회수 |
| 중간 보안 장비의 TCP 옵션 제거로 인한 처리량 저하 | **엔드투엔드 패킷 캡처를 통한 `Window Scale / SACK 옵션 보존`** | 대용량 고속 전송 성능 정상 유지 |

#### 한줄 요약
- SYN Cookie 활성화, MSS Clamping, 재시도 타이머 튜닝, TCP 옵션 보존으로 운영한다.

## Ⅶ. 결론

- 연결 수립은 **3-Way**, 종료는 잔여 송신을 위해 **4-Way** 선택

#### 한줄 요약
- TCP 3-Way Handshake는 SYN-ACK 3단계를 통해 양방향 도달성과 전송 옵션을 동기화하는 핵심 연결 수립 기술이다.
