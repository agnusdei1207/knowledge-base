---
title: "TCP 3-way handshake (TCP 3-way Handshake)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-network"
weight: 26
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: TCP 3-way Handshake는 **전송 계층(L4)**에서 양 종단(End-to-End) 간 **신뢰성 있는 통신**을 시작하기 전, **시퀀스 번호(ISN)·수신 버퍼(Window)·MSS를 동기화**하는 3단계 연결 수립 절차임.
- **왜 필요한가**: UDP와 달리 TCP는 데이터 유실 검출·순서 재조합·흐름 제어를 보장해야 하므로, 양측이 사용할 시작 번호(ISN)와 수신 버퍼 크기를 미리 합의해야 함.
- **핵심 직관**: "여보세요? 제 말 들리세요?(SYN)" → "네, 들립니다. 제 말도요?(SYN-ACK)" → "네, 잘 들립니다(ACK)" — 양쪽이 통화 가능을 확인한 뒤 본론을 시작하는 상호 확인 과정.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| TCP (상위 키워드) | 비연결성 IP 위에서 신뢰성·순서 보장·흐름 제어를 제공하는 전송 계층 프로토콜 | 등기 우편(수신 확인 보장) |
| SYN (Synchronize) | TCP 헤더의 제어 플래그, 연결 요청 및 ISN 동기화 신호 | "연결할게, 내 번호는 X야" |
| ACK (Acknowledge) | TCP 헤더의 제어 플래그, 상대방 시퀀스 수신 확인 | "X+1까지 잘 받았어" |
| ISN (Initial Sequence Number) | 각 방향별 데이터 순서 번호의 시작점, 세션 하이재킹 방지를 위해 난수 생성 | 택배 번호의 시작 일련번호 |
| MSS (Max Segment Size) | IP 단편화 없이 전송 가능한 TCP Payload 최대 크기(보통 1460B) | 택배 상자의 최대 용량 |
| Window Size / Scale | 수신 측이 한 번에 수용 가능한 버퍼 크기(16비트), Scale 옵션으로 확장 | 수하물 컨베이어 벨트 용량 |
| SYN_SENT | 클라이언트가 SYN을 보낸 뒤 SYN-ACK를 기다리는 상태 | 전화를 걸고 응답 대기 |
| SYN_RCVD | 서버가 SYN을 받고 SYN-ACK를 보낸 뒤 ACK를 기다리는 상태(Half-open) | 전화를 받고 상대 확인 대기 |
| ESTABLISHED | 양측 모두 연결이 확립되어 데이터 송수신이 가능한 상태 | 통화 중 |
| SYN Cookie | SYN Flood 방어 기술 — 서버가 상태를 저장하지 않고 SYN-ACK의 ISN에 해시를 인코딩 | 번호표 대신 손님 이름을 영수증에 적어 발급 |

## 깊이 이해
- **배경·문제의식**: IP는 비연결성(Connectionless)이므로 패킷 유실·순서 뒤바뀜·중복이 발생함. TCP는 이를 해결하기 위해 연결 지향(Connection-oriented) 전송을 제공하며, 데이터를 순서대로 조립하려면 양측이 사용할 ISN(Initial Sequence Number)을 공유하고 수신 버퍼 크기(Window)를 합의해야 함.
- **1단계 — SYN(Client → Server)**: 클라이언트가 SYN 플래그를 설정하고 자신의 ISN(Seq=X)을 보냄. SYN 패킷의 Option 필드에 MSS·Window Scale·Timestamp 등 통신 규칙도 함께 교환함. 클라이언트 상태: CLOSED → SYN_SENT.
- **2단계 — SYN-ACK(Server → Client)**: 서버가 클라이언트의 ISN을 확인(Ack=X+1)하고 자신의 ISN(Seq=Y)을 보냄. 이 시점에 서버는 백로그 큐(Half-open Queue)에 TCB(Transmission Control Block)를 할당하여 메모리를 소비함. 서버 상태: LISTEN → SYN_RCVD.
- **3단계 — ACK(Client → Server)**: 클라이언트가 서버의 ISN을 확인(Ack=Y+1)하고 ACK를 보냄. 이 패킷부터 데이터 Payload를 함께 전송할 수 있음(Piggybacking). 양측 상태: ESTABLISHED — 데이터 송수신 가능.
- **비유**: 군대 암구호 교환. 초병: "화랑!(SYN)" → 거동수상자: "담배!(ACK) 나는 소대장이다(SYN)" → 초병: "확인했습니다(ACK), 지나가십시오."
- **구체 예시**: 웹 브라우저가 TCP 443 포트로 HTTPS 접속 시, 3-way Handshake(1-RTT)로 TCP 연결을 수립한 뒤 TLS 1.3 Handshake(1-RTT)를 추가로 수행하여 총 2-RTT의 초기 지연이 발생함. MSS는 보통 1460B(이더넷 MTU 1500B - IP 20B - TCP 20B)로 교환됨.
- **흔한 오해·주의점**: "ISN은 0이나 1부터 시작한다"는 틀림 — ISN이 예측 가능하면 세션 하이재킹(TCP Reset 주입)이 가능하므로, RFC 6528에 따라 암호학적 난수로 생성해야 함. 또한 서버는 SYN 수신 시 즉시 메모리(TCB)를 할당하므로, 출발지 IP를 위조한 대량 SYN 패킷으로 백로그 큐를 고갈시키는 SYN Flood 공격에 취약함.

## 연결 개념
- **TCP 4-way Handshake(027)**: 연결을 안전하게 종료하는 4단계 절차, TIME_WAIT(036) 상태로 이어짐.
- **TCP 흐름 제어(028)**: 3-way에서 합의한 Window Size를 기반으로 슬라이딩 윈도우를 운용.
- **QUIC·HTTP/3(032)**: TCP 3-way의 1-RTT 지연을 극복하기 위해 전송+TLS를 통합한 0~1-RTT 프로토콜.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 3-way Handshake는 양 종단 간 ISN·MSS·Window를 동기화하여 신뢰성 있는 연결을 수립하는 절차임.
> 2. **가치**: 데이터 순서 재조합·유실 검출·흐름 제어의 기반을 마련하고, ISN 난수화로 세션 하이재킹을 방지함.
> 3. **판단 포인트**: 연결 수립의 1-RTT 지연과 SYN Flood 취약점(Half-open 상태 메모리 할당)이 성능·보안 설계의 핵심 과제임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 연결 논리·상태 전이 | SYN/ACK 플래그, ISN 동기화, SYN_SENT→SYN_RCVD→ESTABLISHED | 1-2-3 순서만 나열, 상태 명칭·교환 파라미터 누락 |
| 동기화 내용 | ISN(난수)·MSS·Window Scale 교환 | "연결을 맺는다" 추상 표현, 교환 내용 미명시 |
| 보안·성능 연계 | SYN Flood/SYN Cookie, 1-RTT 오버헤드, TFO·QUIC | 보안 위협(DoS) 연결 고리 누락 |

> 요약: 3-way는 "ISN·MSS·Window 합의 과정"이며, 1-RTT 지연과 SYN Flood의 트레이드오프를 반드시 서술해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 비연결성 IP 위에서 양 종단 간 ISN·MSS·Window를 동기화하여 신뢰성 있는 TCP 연결을 수립하는 3단계 절차임.
- 배경: IP는 패킷 유실·순서 뒤바뀜을 보장하지 않으므로, 순서 재조합·유실 검출을 위한 시퀀스 번호 합의가 필수임.
- 필요성: ISN 난수 동기화로 세션 하이재킹을 방지하고, 양측 수신 버퍼(Window)·MSS 합의로 흐름 제어 기준을 설정함.

---

## Ⅱ. 구조 및 구성요소

```text
TCP 헤더 Control Flags: URG | ACK | PSH | RST | SYN | FIN
3-way Handshake: SYN(동기화) + ACK(확인) 플래그 조합으로 연결 수립
교환 파라미터: ISN(Seq/Ack) + MSS + Window Scale + Timestamp (SYN Option)
```

| 교환 파라미터 | 목적 | 특이사항 |
|:---|:---|:---|
| ISN (Initial Seq Number) | 데이터 순서 재조합·유실 판별 기준 | RFC 6528 — 암호학적 난수로 생성(예측 방지) |
| MSS (Max Segment Size) | IP 단편화 방지를 위한 최대 Payload 크기 | 보통 1460B(MTU 1500 - IP 20 - TCP 20) |
| Window Size / Scale | 수신 측 버퍼 여유 공간 통보 | 16비트 한계를 Scale 인자(최대 14)로 확장 |

> 요약: 3-way는 단순 연결 확인이 아니라 ISN·MSS·Window Scale을 교환하여 데이터 전송의 초기 파라미터를 합의하는 과정임.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client(CLOSED)                           Server(LISTEN)
  | --- 1. SYN (Seq=X, MSS, WScale) --> |  -> SYN_RCVD (백로그 큐 TCB 할당)
(SYN_SENT)                               |
  | <-- 2. SYN-ACK (Seq=Y, Ack=X+1) --- |
  |                                      |
(ESTABLISHED)                            |
  | --- 3. ACK (Seq=X+1, Ack=Y+1) ----> |  -> ESTABLISHED
```

1. SYN(Client → Server): 클라이언트가 SYN 플래그와 ISN(Seq=X)을 전송하고, Option 필드에 MSS·Window Scale을 포함함. 클라이언트 상태: CLOSED → SYN_SENT.
2. SYN-ACK(Server → Client): 서버가 클라이언트 ISN을 확인(Ack=X+1)하고 자신의 ISN(Seq=Y)을 전송함. 백로그 큐에 TCB를 할당하여 Half-open 상태 진입. 서버 상태: LISTEN → SYN_RCVD.
3. ACK(Client → Server): 클라이언트가 서버 ISN을 확인(Ack=Y+1)하고 ACK를 전송함. 이 패킷에 데이터 Payload를 함께 실을 수 있음. 양측 상태: ESTABLISHED.

> 요약: SYN → SYN-ACK → ACK 3단계로 양측 ISN을 교차 확인하며, 서버는 SYN 수신 시 TCB를 할당하여 Half-open 큐를 소비함.

---

## Ⅳ. 특징

- 1-RTT 오버헤드: 데이터 전송 전 반드시 1-RTT(SYN→SYN-ACK) 지연이 발생하며, TLS 추가 시 총 2~3-RTT로 초기 응답이 지연됨.
- Half-open 상태 자원 소비: 서버가 SYN 수신 시 즉시 TCB 메모리를 할당하므로, 출발지 IP를 위조한 대량 SYN 패킷(SYN Flood)으로 백로그 큐를 고갈시킬 수 있음.
- ISN 난수화 필수: ISN이 순차 증가하면 공격자가 시퀀스를 예측하여 TCP RST 주입·세션 하이재킹이 가능하므로, RFC 6528 암호학적 난수 생성이 필수임.
- TCP Fast Open(TFO): RFC 7413 — 재접속 시 SYN 패킷에 TFO 쿠키+데이터를 함께 전송하여 0-RTT 데이터 전송을 구현함.

> 요약: 3-way는 신뢰성의 기반이나, 1-RTT 지연과 Half-open 메모리 할당이 성능·보안의 태생적 약점임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | TCP 3-way Handshake | QUIC(UDP 기반, 032) | 선택 기준 |
|:---|:---|:---|:---|
| 연결+보안 | TCP 1-RTT + TLS 1~2-RTT 분리 | 전송+TLS 1.3 통합(1-RTT) | 초기 지연 민감도 |
| 최초 접속 | 2~3-RTT | 1-RTT | 웹 서비스 로딩 속도 |
| 재접속 | 다시 2~3-RTT(TFO 시 1-RTT) | 0-RTT(토큰 캐싱) | 모바일 네트워크 전환 빈도 |

> 요약: TCP 3-way의 태생적 RTT 지연을 극복하기 위해 전송+암호화를 통합한 QUIC(HTTP/3)가 웹 표준으로 확산됨.

**리스크·대응:**
- SYN Flood 공격: 출발지 IP 위조 SYN으로 백로그 큐 고갈 → SYN Cookie 적용(`net.ipv4.tcp_syncookies=1`), somaxconn·syn_backlog 증가 (지표: SYN_RCVD 소켓 수)
- 세션 하이재킹: ISN 예측 가능 시 TCP RST 주입 → RFC 6528 암호학적 난수 ISN 생성 (지표: 커널 CVE 스캔)
- 연결 타임아웃: 중간 방화벽의 SYN 패킷 Drop → TCP Keepalive 활성화, SYN Retries 튜닝 (지표: SYN 재전송 비율)

**점검 지표:**
- 보안: SYN_RCVD 상태 소켓 수 — 비정상 급증 시 SYN Flood 의심
- 성능: TCP 연결 수립 시간(SYN→ESTABLISHED) — p99 기준 목표치 설정

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. SYN Flood 방어: 리눅스 커널 `tcp_syncookies=1` 활성화 및 L4 로드밸런서(022)에서 SYN Cookie를 적용하여 백로그 큐 고갈 공격을 무력화함.
2. 초기 지연 최적화: 재접속이 잦은 웹 서비스에 TCP Fast Open(RFC 7413)을 적용하여 SYN+데이터 동시 전송으로 1-RTT를 절감함.
3. 커널 튜닝: 대규모 트래픽 서버의 `somaxconn`·`tcp_max_syn_backlog` 값을 증가시켜 동시 SYN 요청 수용량을 확대하고, SYN Retries를 최적화함.

**결론:**
- 기술사 판단: TCP 3-way Handshake는 신뢰성 확보의 핵심이나, 1-RTT 지연과 Stateful 메모리 할당이라는 태생적 제약이 있으므로 SYN Cookie·TFO로 보안·성능을 동시에 보강해야 함.
- 향후 방향: TCP 수준의 최적화(TFO)를 넘어, 전송+보안을 통합한 QUIC(032)가 HTTP/3의 표준 전송 계층으로 자리잡아 0-RTT 재접속을 실현하는 추세임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP 3-way Handshake를 설명하시오" | ISN·MSS·Window 교환, SYN/ACK 상태 전이 | SYN Flood 방어, TFO·QUIC 비교 |
| 요구사항 명시형 | "SYN Flood 공격과 방어", "TCP와 QUIC 비교" | Half-open 큐 자원 소비 흐름 | SYN Cookie 원리, QUIC 0-RTT 구조 |
