---
title: "TCP 3-way handshake (TCP 3-way Handshake)"
date: "2026-07-02"
tags:
  - "cspe-network"
weight: 26
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP 연결 생성 과정을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: TCP 프로토콜이 신뢰성 있는 통신을 시작하기 전, 송수신 양측이 연결을 수립(Establish)하고 동기화하는 3단계 과정
- **왜 필요한가**: 신뢰성 있는 전송을 위해서는 누가 몇 번 데이터를 보낼지(Sequence), 창 크기(Window Size)는 얼마인지 미리 합의를 봐야 함
- **핵심 직관**: 통화를 시작할 때 "여보세요? 제 말 들리세요?(SYN)" -> "네, 들립니다. 제 말도 들리시나요?(SYN-ACK)" -> "네, 잘 들립니다(ACK)" 하고 본론을 시작하는 상호 확인 과정이다.

## 깊이 이해
- **배경·문제의식**: UDP는 확인 없이 그냥 쏘지만, TCP는 데이터 유실을 막아야 한다. 데이터를 순서대로 조립하려면 양쪽이 사용할 일련번호(Sequence Number)의 시작점(ISN)을 공유해야 하고, 수신 버퍼 크기를 알아야 오버플로우가 안 난다.
- **작동 원리**:
  1. **SYN (Client -> Server)**: 클라이언트가 "연결할게. 내 시작 번호는 X야" (SYN 비트 1, Seq=X). 상태는 SYN_SENT.
  2. **SYN-ACK (Server -> Client)**: 서버가 "알았어(X+1), 나도 연결할게. 내 시작 번호는 Y야" (SYN 1, ACK 1, Seq=Y, Ack=X+1). 상태는 SYN_RCVD.
  3. **ACK (Client -> Server)**: 클라이언트가 "알았어(Y+1), 이제 데이터 보낼게" (ACK 1, Seq=X+1, Ack=Y+1). 상태는 ESTABLISHED.
- **비유**: 군대 암구호 교환. 초병: "손들어 움직이면 쏜다, 화랑(SYN)" -> 거동수상자: "담배(ACK). 저는 소대장입니다(SYN)" -> 초병: "확인했습니다(ACK), 지나가십시오."
- **구체 예시**: 웹 브라우저가 TCP 80 포트로 접속할 때, MSS(최대 세그먼트 크기), Window Scale 확장 옵션 등 통신의 '규칙'들을 이 3-way handshake의 옵션 필드에 담아 서로 교환한다.
- **흔한 오해·주의점**: "시작 일련번호(ISN)는 무조건 0이나 1부터 시작한다"는 틀렸다. 예측 가능하면 해커가 TCP 세션을 하이재킹(가로채기) 할 수 있으므로, ISN은 난수(Random) 알고리즘으로 생성해야 한다.

## 연결 개념
- TCP 4-way Handshake — 연결을 안전하게 종료하는 과정
- SYN Flood 공격 — 3-way 약점을 악용해 서버의 백로그 큐(연결 대기열)를 꽉 채워 다운시키는 공격
- TCP Fast Open (TFO) — 3-way의 지연(RTT)을 없애기 위해 첫 SYN에 데이터를 실어 보내는 최적화 기술

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 3-way Handshake는 양 종단(End-to-End) 간 신뢰성 있는 데이터 전송을 위해 시퀀스 번호(ISN)와 소켓 상태를 동기화하는 연결 수립 절차다.
> 2. **가치**: 데이터 유실 검출 및 순서 재조합의 기반을 마련하고, 양측의 수신 버퍼 크기(Window)와 최대 세그먼트 크기(MSS)를 합의하여 흐름 통제의 기준을 설정한다.
> 3. **판단 포인트**: 연결 수립은 필연적으로 1-RTT 지연을 발생시키며, 이 과정에서 발생하는 SYN Flood 공격 방어(SYN Cookie)와 성능 최적화(TCP Fast Open)가 주요 과제다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 연결 논리 및 상태 전이 이해 | SYN/ACK 플래그 전이, ISN 동기화, SYN_SENT -> SYN_RCVD -> ESTABLISHED 상태 | 단순 1,2,3단계 순서만 나열하고 상태(State) 명칭 누락 |
| 동기화(Synchronization) 내용 이해 | MSS, Window Scale 등 헤더 옵션 교환 | "연결을 맺는다"는 추상적 표현 (무엇을 교환하는지 명시) |
| 보안 취약점 및 최적화 연계 판단 | SYN Flood / SYN Cookie 대응, 1-RTT 오버헤드 한계 | 보안 위협(DoS)과의 연결 고리 누락 |

> 요약: 3-way handshake는 단순한 인사가 아니라 "초기 파라미터(ISN, MSS) 합의 과정"이며, 성능(RTT 지연)과 보안(SYN Flood)의 트레이드오프를 수반한다.

---

## Ⅰ. 개요 및 필요성

- 정의: TCP(Transmission Control Protocol)에서 양 종단 간 논리적 연결(Session)을 수립하기 위해 3단계로 패킷(SYN/ACK)을 교환하는 동기화 절차
- 배경: 비연결성(Connectionless)인 IP 망 위에서 신뢰성, 순서 보장, 흐름 통제를 수행하기 위한 사전 합의 필수
- 필요성: Initial Sequence Number(ISN) 난수 동기화로 세션 하이재킹을 방지하고, 송수신 양측의 버퍼(Window) 상태를 확인하기 위해 필요

---

## Ⅱ. 구조 및 구성요소 (교환 파라미터)

```text
[TCP 헤더 Control Flags] : URG | ACK | PSH | RST | SYN | FIN
- 3-way Handshake는 SYN(동기화)과 ACK(확인) 플래그 조합으로 구성됨
```

| 교환 파라미터 | 목적 | 특이사항 |
|:---|:---|:---|
| ISN (Initial Seq Number) | 데이터 순서 재조합 및 중복/유실 판별 기준 | 보안을 위해 예측 불가능한 난수(Random) 사용 |
| MSS (Max Segment Size) | IP 단편화(Fragmentation)를 방지할 최대 페이로드 크기 | SYN 패킷의 Option 필드를 통해 상호 교환 |
| Window Size / Scale | 수신 측이 수용 가능한 버퍼 여유 공간 통보 | 고속 망에서 16비트 한계 극복 위해 Scale 인자 합의 |

> 요약: 3-way 과정은 단순히 연결 여부를 묻는 것이 아니라, ISN, MSS, Window Scale이라는 핵심 통제 변수를 초기 셋팅하는 과정이다.

---

## Ⅲ. 동작원리 및 흐름도 (상태 전이)

```text
Client (CLOSED)                    Server (LISTEN)
  | --- 1. SYN (Seq=X) -------------> | (SYN_RCVD)
  |                                   | : 백로그 큐(Half-open) 할당
(SYN_SENT)                            |
  | <--- 2. SYN-ACK (Seq=Y, Ack=X+1) -- |
  |                                   |
(ESTABLISHED)                         |
  | --- 3. ACK (Seq=X+1, Ack=Y+1) ----> | (ESTABLISHED)
  |                                   | : 통신 준비 완료
```

| 단계 | 플래그 및 Sequence | 서버/클라이언트 상태 전이 |
|:---:|:---|:---|
| 1 | `SYN=1` / Seq=X | Client: `SYN_SENT`, Server: `LISTEN` -> `SYN_RCVD` |
| 2 | `SYN=1, ACK=1` / Seq=Y, Ack=X+1 | Server: 수신 버퍼 할당 완료, Client: 응답 대기 |
| 3 | `ACK=1` / Seq=X+1, Ack=Y+1 | Client: `ESTABLISHED`, Server: `ESTABLISHED` |

> 요약: SYN을 받은 서버는 Half-open 상태(SYN_RCVD)로 자원을 할당하며, 클라이언트의 최종 ACK를 받아야 완전한 ESTABLISHED 상태가 된다.

---

## Ⅳ. 주요 특징 및 한계

| 구분 | 내용 | 판단 포인트 |
|:---|:---|:---|
| 통신 오버헤드 | 데이터 전송 전 무조건 1-RTT(Round Trip Time) 지연 발생 | HTTP 응답 지연의 주요 원인 |
| 보안 취약성 | 서버는 SYN 수신 시 즉시 TCB(상태정보) 메모리 할당 | SYN Flood(DoS) 공격의 근본 원인 |
| ISN 난수화 | ISN이 예측 가능하면 악의적 TCP Reset, Session Hijacking 가능 | 난수 생성기 엔트로피 확보 필수 |

> 요약: 3-way 핸드쉐이크는 신뢰성을 보장하지만, 초기 지연(RTT)과 메모리 선점 방식 때문에 필연적인 성능/보안 약점을 지닌다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | TCP 3-way Handshake | QUIC (UDP 기반) Handshake | 선택 기준 |
|:---|:---|:---|:---|
| 연결+보안 계층 | TCP(1-RTT) + TLS(1~2-RTT) 분리 | 전송(연결)과 TLS 1.3 결합 | 초기 지연 민감도 |
| 최초 접속 지연 | 총 2~3 RTT 소요 | 1-RTT 소요 | 웹 서비스 로딩 속도 |
| 재접속 지연 | 다시 2~3 RTT 소요 | 0-RTT (토큰 캐싱 활용) | 모바일 등 네트워크 전환 잦은 환경 |

> 요약: 현대 웹은 TCP 3-way의 태생적 지연을 피하기 위해 전송과 암호화 연결을 한 번에 끝내는 QUIC(HTTP/3) 프로토콜로 진화 중이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SYN Flood 공격 | 출발지 IP 위조 SYN 연속 발송으로 백로그 큐 고갈 | SYN Cookie 적용, TCP 큐 크기(Somaxconn) 증가 | SYN_RCVD 상태 소켓 수 |
| 세션 하이재킹 | 허술한 ISN 생성 알고리즘 (순차 증가 등) | 커널 레벨의 암호학적 난수 생성 (RFC 6528) | 커널 취약점 스캔 (CVE) |
| 연결 타임아웃 | 중간 방화벽에 의한 조용한 패킷 Drop | TCP Keepalive 활성화, SYN Retries 튜닝 | SYN 패킷 재전송 비율 |

> 요약: SYN Flood 방어의 핵심은 상태(State)를 서버 메모리에 저장하지 않고, 응답 패킷(SYN-ACK)의 시퀀스 번호에 해시로 말아 보내는 SYN Cookie 기술이다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 보안 강화(SYN Cookie): 방화벽이나 L4 스위치, 리눅스 커널에서 `net.ipv4.tcp_syncookies = 1`을 설정하여 백로그 큐 고갈 공격(SYN Flood) 무력화
2. 성능 최적화(TCP Fast Open): RFC 7413 TFO 옵션을 활성화하여, 재접속 시 SYN 패킷 내에 TFO 쿠키와 데이터를 함께 보내 0-RTT 데이터 전송 구현
3. 커널 튜닝: 대용량 트래픽 서버의 경우 `net.core.somaxconn` 및 `tcp_max_syn_backlog` 값을 늘려 동시 SYN 요청 수용량 확대

**결론 (2줄):**
- 기술사 판단: TCP 3-way Handshake는 통신의 신뢰성을 위한 위대한 발명이지만, 지연(RTT)과 상태 유지(Stateful)라는 굴레를 남겼다.
- 향후 방향: 이 한계를 극복하기 위해 TCP 단에서는 Fast Open이, 프로토콜 구조적으로는 UDP 기반의 QUIC(0-RTT)가 표준으로 자리잡고 있다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 설명형 | "TCP 3-way handshake를 설명하시오" | SYN, ACK, SEQ 번호 변화와 상태 전이도 | ISN, MSS 교환 및 연결 확립 특징 |
| 보안형 | "SYN Flood 공격과 방어 메커니즘" | SYN_RCVD 상태에서 서버 자원 점유 흐름 | SYN Cookie의 해시값 계산 및 검증 원리 |
| 최적화/비교형| "HTTP 지연 원인과 QUIC 비교" | 3-way 1-RTT + TLS 1.3 1-RTT 지연 구조 | TCP Fast Open 및 QUIC(0-RTT) 비교표 |

> 요약: 연결 과정 설명에 그치지 않고, 반드시 SYN Flood 보안 리스크와 초기 지연(RTT) 최적화 방안을 연결하여 기술사적 판단을 보여야 한다.
