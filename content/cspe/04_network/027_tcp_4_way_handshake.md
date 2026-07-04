---
title: "TCP 4-way handshake·연결 해제 (TCP 4-way Handshake)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-network"
weight: 27
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: TCP 4-way Handshake는 **전이중(Full-Duplex)** 통신에서 양 종단이 각각 독립적으로 **FIN(종료 선언)**을 교환하여 세션을 안전하게 종료하는 4단계 절차임.
- **왜 필요한가**: 한쪽이 전송을 마쳤더라도 상대방은 아직 보낼 데이터가 남아 있을 수 있으므로, 각 방향마다 따로 종료 선언을 해야 데이터 유실 없이 안전하게 자원을 반환할 수 있음.
- **핵심 직관**: A: "나 할 말 다 했어 끊자(FIN)" → B: "알았어(ACK), 잠깐만 하던 말 마저 하고…나도 끝(FIN)" → A: "오케이 끊는다(ACK)" — 양쪽 모두 송신 완료를 확인한 뒤 종료.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| 전이중 (Full-Duplex, 상위 키워드) | 양방향으로 독립된 데이터 파이프가 동시에 열려 있는 통신 방식 | 양방향 도로 |
| FIN (Finish) | "나의 송신 데이터를 모두 보냈음"을 선언하는 TCP 플래그 | "할 말 다 했어" |
| Active Close | 먼저 FIN을 보내는 종료 요청 측(주로 클라이언트) | 먼저 전화를 끊겠다고 말하는 쪽 |
| Passive Close | FIN을 받는 종료 수신 측(주로 서버) | 끊겠다는 말을 듣는 쪽 |
| Half-Close | 한쪽 방향의 송신만 종료되고 반대 방향은 아직 열린 상태 | 한쪽 도로만 폐쇄 |
| FIN_WAIT_1/2 | Active Close 측이 FIN을 보낸 뒤 상대의 ACK/FIN을 기다리는 상태 | 끊겠다 말하고 답변 대기 |
| CLOSE_WAIT | Passive Close 측이 FIN을 받고 ACK를 보낸 뒤 애플리케이션의 close() 호출을 기다리는 상태 | 포장해 드릴게요(남은 처리 중) |
| LAST_ACK | Passive Close 측이 FIN을 보내고 최종 ACK를 기다리는 상태 | 포장 다 됐어요, 확인 대기 |
| TIME_WAIT | Active Close 측이 최종 ACK를 보낸 뒤 2 MSL(보통 60초) 대기하는 상태 | 늦게 도착하는 택배를 기다리는 유예 기간 |
| MSL (Maximum Segment Lifetime) | TCP 세그먼트가 네트워크에서 존재할 수 있는 최대 시간(보통 30초) | 택배 배달 최대 시간 |

## 깊이 이해
- **배경·문제의식**: TCP는 전이중이므로 클라이언트→서버 방향과 서버→클라이언트 방향이 독립적임. 한쪽이 FIN을 보내도 상대방은 아직 보낼 데이터가 남아 있을 수 있으므로, 3-way처럼 FIN+ACK를 합칠 수 없고 각 방향마다 FIN-ACK를 교환해야 함(총 4단계).
- **4단계 작동 원리**: ① Client가 FIN을 전송(Active Close, FIN_WAIT_1). ② Server가 ACK를 응답(CLOSE_WAIT)하고 남은 데이터를 마저 전송. Client는 FIN_WAIT_2. ③ Server가 남은 전송을 마치고 FIN을 전송(LAST_ACK). ④ Client가 최종 ACK를 전송하고 TIME_WAIT(2 MSL) 후 CLOSED. Server는 즉시 CLOSED.
- **TIME_WAIT의 필요성**: 최종 ACK가 유실되면 Server는 FIN을 재전송하는데, Client가 이미 CLOSED 상태면 재전송된 FIN에 대한 ACK를 보낼 수 없어 Server가 정상 종료되지 못함. 또한 동일 4-tuple(IP·Port 쌍)을 재사용하는 새 세션에 이전 세션의 지연 패킷이 도달하면 데이터가 오염됨. TIME_WAIT은 이 두 문제를 방지하기 위해 2 MSL(보통 60초)간 동일 포트 재사용을 차단함.
- **CLOSE_WAIT 문제**: Server가 FIN을 받고 ACK를 보냈으나 애플리케이션이 close()를 호출하지 않으면 CLOSE_WAIT 상태가 무한히 지속됨. 이는 100% 애플리케이션 코드 버그(소켓 닫기 누락)이며, 파일 디스크립터·소켓 자원이 고갈되어 신규 연결 불가 장애가 발생함.
- **비유**: 식당 영업 종료. 손님: "다 먹었어요 갈게요(FIN)." 사장: "네(ACK), 남은 음식 포장해 드릴게요(CLOSE_WAIT)... 포장 다 됐습니다 안녕히 가세요(FIN)." 손님: "감사합니다(ACK), 혹시 깜빡한 물건 없나 잠깐 기다렸다 나갈게요(TIME_WAIT)."
- **구체 예시**: 서버 장애 시 `netstat -an | grep CLOSE_WAIT | wc -l`로 확인하면, DB 커넥션을 맺고 예외 발생 시 close()를 호출하지 않은 백엔드 프로세스 때문에 CLOSE_WAIT 소켓이 수만 개 쌓여 시스템 자원이 고갈되는 현상을 볼 수 있음.
- **흔한 오해·주의점**: "TIME_WAIT은 낭비이므로 무조건 없애야 한다"는 위험한 오해임. TIME_WAIT 없이 포트를 즉시 재사용하면 이전 세션의 지연 패킷이 새 세션 데이터로 둔갑함. TIME_WAIT이 과다할 때는 `tcp_tw_reuse`·Connection Pool로 완화하되 제거하지 않아야 함.

## 연결 개념
- **TCP 3-way Handshake(026)**: 연결 수립 절차, 4-way는 수립된 연결을 종료하는 반대 과정.
- **TIME_WAIT 상태(036)**: 4-way의 최종 단계에서 2 MSL 대기, 포트 고갈 이슈 심화.
- **TCP 흐름 제어(028)**: 연결 종료 시 Window Size가 0이 되어 송신을 멈추는 과정과 연관.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 전이중 TCP에서 양 종단이 각각 FIN-ACK를 교환하여 독립적으로 송신을 종료하고 자원을 반환하는 절차임.
> 2. **가치**: Half-Close로 잔여 데이터를 안전하게 수신하고, TIME_WAIT로 지연 패킷에 의한 데이터 오염을 방지함.
> 3. **판단 포인트**: CLOSE_WAIT은 애플리케이션 close() 누락(코드 버그), TIME_WAIT은 짧은 세션 빈발(아키텍처 문제)이 원인이며, 대응 방법이 완전히 다름.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 종료 논리·상태 전이 | FIN/ACK 교환, FIN_WAIT→CLOSE_WAIT→TIME_WAIT 전이 | "4번 주고받고 끝" 식 빈 서술 |
| TIME_WAIT 존재 이유·리스크 | 2 MSL 대기 필요성(패킷 오염 방지), 포트 고갈 현상 | TIME_WAIT을 무조건 버그로 취급 |
| CLOSE_WAIT 트러블슈팅 | 애플리케이션 close() 미호출이 원인(100% 코드 버그) | 네트워크 장비 문제로 오판 |

> 요약: 정상 종료 과정보다 TIME_WAIT·CLOSE_WAIT이 유발하는 자원 고갈 장애의 원인·대응을 구분하는 것이 핵심임.

---

## Ⅰ. 개요 및 필요성

- 개요: 전이중 TCP 세션을 종료하기 위해 양 종단이 FIN-ACK를 각각 교환하는 4단계 절차임.
- 배경: 한쪽의 전송 완료가 상대방의 전송 완료를 의미하지 않으므로, 각 방향 독립 종료가 필수임.
- 필요성: 잔여 데이터 안전 수신(Half-Close)과 지연 패킷 오염 방지(TIME_WAIT)를 위해 정의된 절차임.

---

## Ⅱ. 구조 및 구성요소

```text
TCP 제어 플래그: URG | ACK | PSH | RST | SYN | FIN
4-way Handshake: FIN(종료 선언) + ACK(확인) 조합으로 양방향 독립 종료
```

| 제어 플래그 | 동작 | 특이사항 |
|:---|:---|:---|
| FIN (Finish) | "나의 송신을 모두 마쳤음" 선언 | 수신은 계속 가능(Half-Close) |
| ACK (Acknowledge) | 상대방 FIN 수신 확인 | 상태를 WAIT으로 전이시킴 |
| RST (Reset) | 4-way 생략, 즉시 강제 종료 | 에러·방화벽 강제 차단 시 사용 |

> 요약: FIN은 송신의 끝이지 수신의 끝이 아니므로, 양쪽 모두 FIN을 보내야 완전한 종료임.

---

## Ⅲ. 동작원리 및 흐름도

```text
Active Close(먼저 끊는 쪽)            Passive Close(나중에 끊는 쪽)
  | --- 1. FIN -----------------> | -> CLOSE_WAIT (남은 데이터 전송)
(FIN_WAIT_1)                       |
  | <-- 2. ACK ------------------- |
(FIN_WAIT_2)                       |
  | <-- 3. FIN ------------------- | -> LAST_ACK
(TIME_WAIT)                        |
  | --- 4. ACK -----------------> | -> CLOSED (즉시 자원 반환)
(2 MSL 대기 후 CLOSED)
```

1. FIN(Active → Passive): Active Close 측이 "송신 완료" FIN을 전송함. 상태: ESTABLISHED → FIN_WAIT_1.
2. ACK(Passive → Active): Passive Close 측이 FIN 수신을 확인하고 ACK를 응답함. Passive 상태: CLOSE_WAIT(남은 데이터 전송 및 close() 대기). Active 상태: FIN_WAIT_2.
3. FIN(Passive → Active): 남은 전송을 마친 Passive 측이 "나도 송신 완료" FIN을 전송함. 상태: LAST_ACK.
4. ACK(Active → Passive): Active 측이 최종 ACK를 전송함. Passive 측은 즉시 CLOSED. Active 측은 TIME_WAIT(2 MSL, 보통 60초) 후 CLOSED.

> 요약: 양방향 FIN-ACK 교환으로 각 방향을 독립 종료하며, Active 측은 TIME_WAIT으로 지연 패킷·ACK 유실에 대비함.

---

## Ⅳ. 특징

- Half-Close 지원: FIN은 송신만 종료하므로, 수신 채널은 열린 채로 상대방의 잔여 데이터를 안전하게 수신할 수 있음.
- TIME_WAIT 보호: 2 MSL 대기로 ① 최종 ACK 유실 시 FIN 재전송에 대응하고, ② 동일 4-tuple 재사용 시 이전 세션 지연 패킷의 데이터 오염을 방지함.
- CLOSE_WAIT 위험: 애플리케이션이 close()를 호출하지 않으면 CLOSE_WAIT이 무한 지속되어 파일 디스크립터·소켓 자원이 고갈됨 — 100% 코드 버그임.
- RST 강제 종료: 비정상 상황에서 4-way를 생략하고 즉시 연결을 파기하나, 잔여 데이터 유실·TIME_WAIT 보호 없음의 위험이 있음.

> 요약: TIME_WAIT은 프로토콜상 정상(과부하 원인 가능), CLOSE_WAIT 대량 누적은 100% 애플리케이션 코드 결함임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | TIME_WAIT | CLOSE_WAIT | 판단 기준 |
|:---|:---|:---|:---|
| 주체 | Active Close 측(먼저 끊는 쪽) | Passive Close 측(나중에 끊는 쪽) | 어느 쪽에서 자원 부족 발생 |
| 원인 | 정상 TCP 종료의 마지막 대기(2 MSL) | 애플리케이션 close() 미호출(코드 버그) | 정상 설계 vs 코드 결함 |
| 주요 문제 | 짧은 세션 빈발 시 포트 고갈(65535 한계) | 파일 디스크립터 누수, 신규 연결 불가 | 커널 튜닝 vs 앱 로직 패치 |

> 요약: TIME_WAIT 과다는 Connection Pool·tcp_tw_reuse로 완화하고, CLOSE_WAIT 과다는 코드에서 close() 누락을 수정해야 함.

**리스크·대응:**
- TIME_WAIT 포트 고갈: 리버스 프록시-백엔드 간 짧은 연결 빈발 → HTTP Keep-Alive(Connection Pool)로 세션 재사용, `tcp_tw_reuse=1` 설정 (지표: TIME_WAIT 소켓 수)
- CLOSE_WAIT 소켓 누수: 예외 처리 시 socket.close() 누락 → finally 블록에 명시적 close() 보장, SAST로 검증 (지표: 프로세스 FD 사용률)
- 포트 범위 부족: 로컬 포트(Ephemeral Port) 소진 → `ip_local_port_range` 확장(1024~65535) (지표: 사용 가능 Ephemeral Port 수)

**점검 지표:**
- 안정성: TIME_WAIT 소켓 수 — 비정상 급증 시 Connection Pool 미적용 의심
- 가용성: CLOSE_WAIT 소켓 수 — 0 유지 목표, 누적 시 즉시 코드 점검

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Connection Pool 적용: HTTP/1.1 Keep-Alive·DB Connection Pool을 활용하여 매 요청마다 3-way/4-way가 반복되는 오버헤드를 근본적으로 제거함.
2. 커널 튜닝(TIME_WAIT 완화): `net.ipv4.tcp_tw_reuse=1`로 안전성이 확인된 TIME_WAIT 포트를 아웃바운드 연결에 재사용하고, `ip_local_port_range`를 확장함.
3. CLOSE_WAIT 방지(개발 표준): SAST·코드 리뷰로 네트워크·DB 예외 발생 시 반드시 소켓을 close()하도록 강제하고, 타임아웃을 설정하여 무한 대기를 방지함.

**결론:**
- 기술사 판단: 4-way 장애의 핵심은 네트워크 인프라가 아니라 커널 파라미터(TIME_WAIT)와 애플리케이션 로직(CLOSE_WAIT)이며, 원인에 따라 대응 방법이 완전히 다름.
- 향후 방향: MSA 환경의 커넥션 폭증에 대응하기 위해 gRPC(HTTP/2 다중화)·QUIC(032)로 연결 재사용을 극대화하고, eBPF 기반 소켓 처리로 커널 오버헤드를 절감하는 추세임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP 연결 해제 과정을 설명하시오" | FIN/ACK 교환, 4단계 상태 전이 | TIME_WAIT 필요성, Half-Close 구조 |
| 요구사항 명시형 | "TIME_WAIT 장애 원인과 대책", "TIME_WAIT과 CLOSE_WAIT 비교" | Active/Passive Close 분기 흐름 | 커널 튜닝(tw_reuse) vs 앱 패치(close() 누락) |
