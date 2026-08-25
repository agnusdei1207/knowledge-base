---
sidebar:
  order: 29
  label: "029. 포트 번호•소켓 통신"
  badge:
    text: "기출 · 30%"
    variant: note
title: "포트 번호•소켓 통신 (Port Socket Communication)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 29
extra:
  question_no: "29"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "전송 계층 포트 식별 및 운영체제 소켓 통신 아키텍처"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Port (포트 번호)**: 단일 호스트 내에서 실행 중인 특정 네트워크 프로세스를 식별하는 16비트 정수 식별자 (0~65535).
- **Socket (소켓)**: 응용 프로세스가 커널 네트워크 스택과 데이터를 송수신하기 위해 생성하는 통신 엔드포인트(Endpoint) 추상화 인터페이스.

</details>

- 정의/개념: 호스트 내 프로세스를 식별하는 **16비트 포트 번호와 IP 및 프로토콜을 결합하여 통신 세션을 수립하는 소켓 추상화 인터페이스**
- 배경/필요성: 단일 IP를 공유하는 복수 프로세스 환경에서 **프로세스별 트래픽 다중화/역다중화(Demultiplexing) 불가 및 1:다 동시 통신 제어 불가**

#### 한줄 요약
- 16비트 포트 번호와 5-튜플 소켓 바인딩을 통해 다중 프로세스 간 통신을 식별하고 제어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Well-Known Ports (0~1023)**: IANA가 공식 지정한 표준 시스템 포트 (HTTP 80, HTTPS 443, SSH 22, DNS 53).
- **Registered Ports (1024~49151)** / **Dynamic/Private Ports (49152~65535)**: 특정 벤더/서비스 등록 포트 및 OS가 클라이언트에 임시 부여하는 Ephemeral 포트.

</details>

- **16비트 포트 번호 체계**: Well-Known(0~1023), Registered(1024~49151), Dynamic/Private(49152~65535) 3단 분류
- **5-튜플 기반 소켓 식별**: 동일 서버 포트(80)에서 수만 개의 클라이언트 세션을 독립 식별
- 서버 소켓을 **Listen 소켓(연결 수락 전담)**과 **Connected 소켓(1:1 데이터 통신 전담)**으로 분리 운용

#### 한줄 요약
- 16비트 포트 분류, 5-튜플 세션 식별, 리슨/연결 소켓 분리 아키텍처를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Listen Socket vs Connected Socket**: 서버 포트에 바인딩되어 SYN 요청을 대기하는 관리 소켓(Listen)과 accept() 후 클라이언트와 1:1 통신하는 세션 소켓(Connected).

</details>

```text
[서버 프로세스 소켓 생명주기 및 1:다 다중화 아키텍처]
|-- Client Socket (Src IP: 10.0.0.1, Ephemeral Port: 52134)
`-- Server Host (Dst IP: 203.0.113.1, Service Port: 80)
    |-- Listen Socket (Port 80 바인딩: passive open, 신규 연결 수신 대기)
    |-- Backlog Queues (SYN Queue 반개방 버퍼 -> Accept Queue 완성 버퍼)
    `-- Connected Sockets (`accept()` 반환 신규 FD: 5-Tuple [10.0.0.1:52134 <-> 203.0.113.1:80])
`-- Application Thread Pool / epoll Event Loop (Worker Thread 1:1 데이터 I/O 처리)
```

선의 의미: 계층 및 클라이언트의 SYN이 리슨 소켓에 수신되어 큐를 거쳐 accept() 호출 시 1:1 독립 연결 소켓으로 생성되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 식별 정보 |
|:---|:---|:---|
| **리슨 소켓 (Listen)** | 서버 서비스 포트에 바인딩되어 **신규 클라이언트의 연결 요청(SYN)을 수신 및 큐잉** | 서버 IP + 서비스 포트 |
| **연결 소켓 (Connected)**| `accept()`를 통해 분기 생성되어 **특정 클라이언트와 1:1 실제 데이터 송수신 전담** | **5-튜플 고유 세션** |
| **백로그 큐 (Backlog)** | 애플리케이션이 `accept()`를 호출하기 전까지 **완성된 TCP 연결을 보관하는 커널 대기열** | `somaxconn` 파라미터 |
| **파일 디스크립터 (FD)**| 운영체제 커널이 **소켓 객체를 식별하고 read/write I/O 시스템 콜을 처리하기 위한 정수 인덱스**| 프로세스별 정수 ID |

#### 한줄 요약
- 리슨 소켓, 연결 소켓, 백로그 큐, 파일 디스크립터(FD)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **POSIX 소켓 6단계 시스템 콜**: `socket()` $\to$ `bind()` $\to$ `listen()` $\to$ `accept()` $\to$ `read()`/`write()` $\to$ `close()`.

</details>

```text
POSIX 소켓 통신 수립 및 데이터 I/O 파이프라인
        │
   1. [socket()] 커널에 소켓 엔드포인트 구조체 및 FD 생성
        │
   2. [bind()] 서버의 로컬 IP 주소 및 서비스 포트(Port 80)를 소켓에 결합
        │
   3. [listen()] 수신 대기 모드로 전환하고 백로그 큐(`somaxconn`) 크기 지정
        │
   4. [accept()] 3-Way Handshake 완료 세션을 꺼내 신규 Connected Socket FD 반환
        │
   5. [read() / write()] 연결 소켓을 통해 양방향 전이중 데이터 스트림 송수신
        │
   6. [close()] 통신 완료 후 소켓 자원 및 FD 해제 (4-Way Handshake 개시)
```

#### 한줄 요약
- socket → bind → listen → accept 순으로 연결을 수립하고, 독립 연결 소켓으로 데이터를 송수신한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Stream Socket (SOCK_STREAM)** vs **Datagram Socket (SOCK_DGRAM)**: 연결형 바이트 스트림 소켓(TCP)과 비연결형 데이터그램 소켓(UDP).

</details>

| 비교 항목 | TCP 소켓 (Stream Socket) | UDP 소켓 (Datagram Socket) |
|:---|:---|:---|
| **소켓 타입 상수** | `SOCK_STREAM` (연결 지향형) | `SOCK_DGRAM` (비연결형) |
| **서버 소켓 동작 구조** | **리슨 소켓과 연결 소켓의 분리 운용 (1:다)** | **단일 소켓**으로 다수 클라이언트 메시지 처리 |
| **연결 수립 시스템 콜** | `listen()`, `accept()`, `connect()` 필수 호출 | 사전 연결 없이 `sendto()`, `recvfrom()` 즉시 호출 |
| **커널 자원 점유** | 클라이언트 연결마다 독립 소켓 상태 및 FD 점유 | 단일 소켓 FD 유지로 커널 메모리 소모 극소화 |

#### 한줄 요약
- TCP 소켓은 연결별 전담 소켓을 분리 생성하고, UDP 소켓은 단일 엔드포인트로 메시지를 송수신한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **epoll (이벤트 기반 I/O 멀티플렉싱)**: 수만 개의 소켓 FD 중 실제 I/O 이벤트가 발생한 소켓만 $O(1)$ 복잡도로 추출하여 C10K 문제를 해결하는 리눅스 커널 시스템 콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단기간 대규모 아웃바운드 세션 생성 시 **임시 포트(Ephemeral Port) 고갈** | **HTTP Keep-Alive 커넥션 풀링 및 `ip_local_port_range` 확장** | 임시 포트 고갈 방지 및 세션 수립 지연 해소 |
| 트래픽 급증 시 신규 연결 요청 거부(**Connection Refused / SYN Drop**) | **커널 `tcp_max_syn_backlog` 및 `somaxconn` 백로그 큐 확장** | SYN 스파이크 흡수 및 연결 수락 대기열 안정화 |
| 동시 접속자 증가 시 **"Too many open files" 에러 및 프로세스 다운** | **운영체제 `ulimit -n` 최대 파일 디스크립터(FD) 한도 증설** | 대규모 1:다 동시 연결(C10K/C1000K) 수용량 확보 |
| 다중 스레드 블로킹 I/O 모델 사용 시 컨텍스트 스위칭 과부하 | **`epoll / kqueue 기반 논블로킹 비동기 이벤트 루프(Netty/Node.js)`** | 단일 스레드로 수만 개 소켓 초고속 처리 |

#### 한줄 요약
- 커넥션 풀링, 백로그 큐 확장, ulimit FD 증설, epoll 논블로킹 I/O로 운영한다.

## Ⅶ. 결론

- 대규모 동시 접속을 수용하는 고성능 네트워크 서비스를 구축하기 위해 **16비트 포트 체계와 5-튜플 소켓 라이프사이클을 기반으로 아키텍처를 설계**하고, **epoll/kqueue 기반의 논블로킹 I/O 멀티플렉싱과 커널 백로그 큐(somaxconn) 및 FD(ulimit) 파라미터 최적화**를 결합하여 대규모 동시성(C1000K)을 만족하는 서버 인프라 완성

#### 한줄 요약
- 포트 번호와 소켓 통신은 16비트 식별자와 5-튜플 엔드포인트를 통해 다중 통신을 제어하며, epoll 논블로킹 I/O와 결합하여 고성능을 실현하는 핵심 통신 인터페이스다.