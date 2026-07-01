---
title: "포트 번호·소켓 통신 (Port Socket Communication)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 35
---

# 📖 【암기용】 개념 완전 이해

> 목적: 포트와 소켓을 프로세스 간 네트워크 통신의 식별자 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 커널이 패킷을 애플리케이션에 전달하는 과정을 익히기 위한 설명이다.

## 한눈에
- **개요**: 포트는 호스트 안의 서비스 식별 번호이고, 소켓은 IP·포트·프로토콜로 만든 통신 끝점
- **왜 필요한가**: 하나의 서버 IP에서 웹 443, DNS 53, SSH 22처럼 여러 애플리케이션을 동시에 구분해야 함.
- **핵심 직관**: IP가 건물 주소라면 포트는 방 번호, 소켓은 특정 방과 상대방을 잇는 통화 회선임.

## 깊이 이해
- **배경·문제의식**: 네트워크 계층의 IP는 호스트까지만 전달함. 호스트 내부의 어떤 프로세스가 받을지 결정하려면 TCP/UDP 포트와 커널 소켓 테이블이 필요함.
- **작동 원리**: 서버는 특정 포트에 bind/listen하고 클라이언트는 ephemeral port를 사용해 connect함. TCP 연결은 source IP, source port, destination IP, destination port, protocol의 5-tuple로 식별됨.
- **비유**: 회사 대표번호(IP)로 전화가 오면 내선번호(포트)로 부서에 연결하고, 통화 기록(소켓)이 양쪽 번호를 묶어 관리함.
- **구체 예시**: 클라이언트 `10.0.0.5:53124`가 서버 `203.0.113.10:443`에 접속하면 커널은 5-tuple로 연결을 구분함.
- **흔한 오해·주의점**: 포트 번호는 보안 경계가 아님. 443 포트를 열어도 애플리케이션 인증, TLS, 접근통제가 별도로 필요함.

## 연결 개념
- TCP 3-way Handshake: 소켓 연결 생성 절차
- NAT/PAT: 내부 포트와 외부 포트 변환
- TIME_WAIT: TCP 소켓 종료 후 5-tuple 재사용 지연

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 포트·소켓 문제는 번호 암기가 아니라 5-tuple, bind/listen/connect/accept, NAT, 파일 디스크립터, 운영 한계를 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 포트 번호는 전송 계층 서비스 식별자이고, 소켓은 애플리케이션이 커널 네트워크 스택을 사용하는 통신 끝점이다.
> 2. **가치**: 하나의 IP에서 다중 서비스와 다중 세션을 5-tuple로 분리해 동시 통신을 가능하게 한다.
> 3. **판단 포인트**: well-known port, ephemeral port, listen backlog, file descriptor, NAT port exhaustion을 함께 관리해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전송 계층 다중화 이해 확인 | 포트, 소켓, 5-tuple, 프로토콜 | 포트 번호 나열만 수행 |
| 소켓 API 흐름 확인 | socket, bind, listen, accept, connect | 서버/클라이언트 역할 혼동 |
| 운영 장애 분석 확인 | ephemeral port, backlog, FD limit, NAT | 포트 개방을 보안 대책으로 오해 |

> 요약: 포트·소켓 문제는 커널의 세션 식별과 애플리케이션 연결 수용 한계를 설명하는 문제임.

---

## Ⅰ. 개요 및 필요성

포트는 호스트 내부 서비스를 식별하는 번호이다. 소켓은 IP, 포트, 프로토콜을 묶어 프로세스가 네트워크를 사용하는 통신 끝점이다. 서버 동시 접속, NAT 변환, 방화벽 정책은 모두 포트와 소켓 식별 구조를 기반으로 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Process -> Socket API -> Kernel Socket Table -> TCP/UDP -> IP
       / Server: bind -> listen -> accept
       / Client: ephemeral port -> connect
       / Session: 5-tuple
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 포트 번호 | 서비스·프로세스 식별 | 0~65535, well-known 0~1023 |
| 소켓 | 통신 끝점 객체 | file descriptor로 접근 |
| 5-tuple | 연결 식별 | src/dst IP, src/dst port, protocol |
| backlog | accept 전 대기 큐 | SYN flood·부하와 연계 |
| ephemeral port | 클라이언트 임시 포트 | 대량 연결 시 고갈 가능 |

> 요약: 소켓 통신은 포트와 5-tuple로 세션을 구분하고, 커널 큐와 FD가 동시 접속 한계를 결정함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Server socket -> bind port -> listen backlog -> accept connection
Client socket -> ephemeral port 할당 -> connect -> 5-tuple 생성
-> send/recv -> close
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서버가 소켓 생성 후 IP:Port에 bind | `ss -ltnup` |
| 2 | listen으로 backlog 큐 생성 | listen queue depth |
| 3 | 클라이언트가 ephemeral port로 connect | local port range |
| 4 | TCP는 3-way handshake 후 accept 반환 | established count |
| 5 | 송수신 후 close, TIME_WAIT 처리 | TIME_WAIT count |

> 요약: 서버는 포트에 대기하고 클라이언트는 임시 포트를 사용하며, 연결은 5-tuple로 커널에서 관리됨.

---

## Ⅳ. 특징

| 구분 | 포트 번호 | 소켓 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 범위 | 0~65535 | OS 객체 | TCP/UDP 16비트 port |
| 역할 | 서비스 식별 | 통신 API·상태 보관 | FD, socket buffer |
| 서버 동작 | well-known port 사용 | bind/listen/accept | HTTP 80, HTTPS 443 |
| 클라이언트 동작 | ephemeral port 사용 | connect/send/recv | Linux 기본 범위 확인 필요 |

> 요약: 포트는 번호 체계, 소켓은 커널 객체이며 둘을 5-tuple로 결합해 연결을 식별함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 소켓 통신 | 선택 기준 |
|:---|:---|:---|:---|
| TCP | 연결형 스트림 | 신뢰성·순서 보장 | HTTP, DB, SSH |
| UDP | 데이터그램 | 연결 상태 없음 | DNS, QUIC, RTP |
| Unix Domain Socket | 로컬 IPC | 파일 경로 기반 | 같은 호스트 DB·프록시 |

> 요약: 소켓 종류는 통신 범위, 순서 보장, 커널 경로, 지연 요구를 기준으로 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 포트 고갈 | 짧은 연결 대량 생성 | keepalive, connection pool, port range 확대 | `EADDRNOTAVAIL` |
| backlog overflow | accept 지연·SYN flood | backlog 조정, SYN cookies, autoscaling | listen overflow |
| FD 한계 | 프로세스 파일 디스크립터 제한 | ulimit, event loop, connection cap | open fd count |

> 요약: 운영 리스크는 포트·큐·FD 자원 고갈이며 OS counter로 조기 탐지해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 연결 수 | FD limit의 70% 이하 | `lsof`, procfs |
| backlog | overflow 0건 유지 | `ss`, netstat counter |
| 포트 사용 | ephemeral port 사용률 70% 이하 | conntrack, NAT table |

> 요약: 소켓 통신은 애플리케이션 처리량뿐 아니라 커널 자원 사용률을 함께 점검함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 서버 설계: listen backlog, worker 수, FD limit을 예상 동시 접속 수의 1.5배 이상으로 산정
2. 클라이언트 설계: HTTP keepalive와 connection pool로 ephemeral port 재사용률을 높이고 TIME_WAIT 폭증을 제한
3. 보안 운영: 방화벽은 허용 포트를 최소화하고, mTLS·JWT·RBAC로 애플리케이션 인증·인가를 별도 적용

**결론 (2줄):**
- 기술사 판단: 연결형 업무는 TCP socket, 질의형·실시간 업무는 UDP socket, 로컬 고빈도 IPC는 Unix Domain Socket을 선택함
- 향후 방향: eBPF와 service mesh 관측으로 5-tuple 기반 트래픽 추적과 포트 고갈 탐지가 자동화됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "포트와 소켓 통신을 설명하시오" | bind/listen/connect/accept 흐름 | 포트·소켓·5-tuple 차이 |
| 요구사항 명시형 | "대량 접속 장애 방안을 제시하시오" | backlog, FD, port range 진단 | 포트 고갈·큐 overflow 대응 |

> 요약: 설명형은 식별 구조, 운영형은 커널 자원 한계와 조정값 중심으로 전환함.
