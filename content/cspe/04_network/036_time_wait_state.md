---
title: "TCP TIME_WAIT 상태 (TIME_WAIT State)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-network"
weight: 36
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP 4-Way Handshake 종료 과정에서 연결을 먼저 끊자고 제안한 쪽(Active Closer)이 마지막 ACK 유실 및 늦게 도착하는 잉여 패킷에 대비해 일정 시간(보통 1~2분) 포트를 닫지 않고 유지하는 대기 상태.
> 2. **문제점**: 대규모 트래픽을 처리하는 프록시나 로드밸런서에서 TIME_WAIT 소켓이 누적되면 로컬 포트 고갈(Port Exhaustion)이 발생하여 신규 연결을 맺지 못하는 장애로 직결됨.
> 3. **판단/해결**: 단순 대기 시간을 줄이는 것보다 `tcp_tw_reuse` 파라미터 적용, Connection Pool 기법(Keep-Alive), 또는 로드밸런서의 SNAT IP/Port 풀 확장을 통해 근본적인 소켓 자원 부족 문제를 해결해야 함.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **TCP TIME_WAIT 상태** | TCP TIME_WAIT 상태 (TIME_WAIT State)의 핵심 개념 | 이 주제의 본질 |

---

## Ⅰ. 개요 및 필요성

- **개요**: TCP 연결 종료 후 소켓이 즉각 소멸하지 않고, `2 MSL (Maximum Segment Lifetime)` 동안 소멸을 유예하는 마지막 소켓 상태.
- **필요성**: 
  1. **정상적인 연결 종료 보장**: Active Closer가 보낸 마지막 ACK가 네트워크에서 유실될 경우, Passive Closer는 종료되지 않은 줄 알고 FIN을 재전송한다. TIME_WAIT이 없으면 재전송된 FIN에 응답할 수 없어 상대방이 비정상 종료(RST) 처리가 된다.
  2. **잔류 패킷(지연 패킷) 혼선 방지**: 이전 세션에서 길을 잃고 늦게 도착한 패킷이, 우연히 동일한 포트로 방금 맺어진 "새로운 연결"의 패킷으로 오인되어 데이터가 오염되는 것을 막기 위함 (일종의 소독 기간).

---
## Ⅱ. 아키텍처 및 핵심 원리

```text
[ TCP 4-Way Handshake 와 TIME_WAIT 진입 흐름 ]

(Active Closer - 먼저 끊는 쪽)                    (Passive Closer - 당하는 쪽)
        Client/Proxy                                       Server
             |                                                |
   ESTABLISHED                                            ESTABLISHED
             | ------ [1] FIN (Seq=X) ----------------------> |
       FIN_WAIT_1                                         CLOSE_WAIT (App에 종료 알림)
             | <----- [2] ACK (Ack=X+1) --------------------- |
       FIN_WAIT_2                                             | (App 종료 처리 중)
             |                                                |
             | <----- [3] FIN (Seq=Y) --------------------- |
             |                                             LAST_ACK
             | ------ [4] ACK (Ack=Y+1) --------------------> |
        [TIME_WAIT] 진입                                       CLOSED (소켓 즉시 소멸)
      (2MSL 대기 후 소멸)                                       
```

- **핵심 동작 메커니즘**:
  - 연결 종료를 최초로 요청한 쪽(Active Closer)만 **TIME_WAIT** 상태에 빠진다. (서버가 먼저 끊으면 서버에, 클라이언트가 먼저 끊으면 클라이언트에 생성)
  - 대기 시간은 통상 **2 MSL** (약 60초 ~ 120초)이다. MSL은 IP 데이터그램이 네트워크상에 살아있을 수 있는 최대 시간을 의미한다.

---
## Ⅲ. 비교 및 연결

| 구분 | TIME_WAIT | CLOSE_WAIT |
|:---|:---|:---|
| **발생 위치** | **먼저** 연결 종료를 요청한 쪽 (Active Closer) | 연결 종료를 **당한** 쪽 (Passive Closer) |
| **원인/의미** | TCP 프로토콜 설계상 지극히 **정상적인** 대기 상태 | 애플리케이션 코드가 소켓을 `close()` 하지 않아 **발생한 버그/장애** |
| **해결 방향** | 커널 파라미터(`tw_reuse`) 튜닝 및 아키텍처 변경 | 개발자가 코드 레벨에서 명시적으로 자원 해제(`close()`) 로직 수정 |
| **위험도** | 포트 고갈 시 신규 아웃바운드 연결 불가 (장애 유발) | 파일 디스크립터(FD) 고갈로 서비스 전체 정지 (치명적 장애) |

---
## Ⅳ. 실무 적용 및 기술사 판단

- **현장 트러블슈팅 사례 (Nginx 리버스 프록시 포트 고갈 장애)**
  - 현상: 클라이언트 트래픽이 폭증할 때 Nginx가 백엔드 서버(WAS)로 맺는 연결에서 포트 부족 에러(`Cannot assign requested address`) 발생. Nginx가 Active Closer 역할을 하여 수만 개의 TIME_WAIT 소켓이 누적됨.
  - 조치: 
    1. HTTP `Keep-Alive`를 설정하여 1요청 1연결(단발성) 대신 소켓을 재사용하도록 구조 변경 (Connection Pool).
    2. OS 커널 설정 변경: `sysctl -w net.ipv4.tcp_tw_reuse=1` 적용하여 안전한 범위 내에서 TIME_WAIT 소켓 포트를 즉시 재사용. (`tcp_tw_recycle`은 NAT 환경에서 타임스탬프 꼬임 장애를 유발하므로 리눅스 4.12 이상부터 폐기됨 - 중요 식별 포인트)

---
## Ⅴ. 기대효과 및 결론

- **결론**: TIME_WAIT은 네트워크 무결성을 지키기 위한 TCP의 훌륭한 방패지만, 초당 수만 건을 처리하는 현대 분산 아키텍처에서는 심각한 병목 자원(Port 고갈)으로 돌변한다.
- **기대효과**: TIME_WAIT의 발생 주체와 원리를 정확히 이해하면, 애플리케이션 버그(CLOSE_WAIT)와 네트워크 아키텍처 한계(TIME_WAIT)를 분리하여 신속하고 정확한 인프라 트러블슈팅을 수행할 수 있다.

---
### 📌 관련 개념 맵
- TCP 상태 전이도 (State Machine) -> 4-Way Handshake -> MSL (Maximum Segment Lifetime) -> 포트 고갈(Port Exhaustion) -> Nginx/HAProxy Keep-Alive.

### 📈 관련 키워드 및 발전 흐름도
`Stop-and-Wait` $\rightarrow$ `TCP 4-Way Handshake` $\rightarrow$ **`TIME_WAIT 발생 (문제 인식)`** $\rightarrow$ `Connection Pool (Keep-Alive 도입)` $\rightarrow$ `QUIC (0-RTT 도입으로 핸드쉐이크/종료 패러다임 변화)`

### 👶 어린이를 위한 3줄 비유 설명
1. 전화를 끊을 때 "먼저 끊을게, 안녕~" 하고 나서 바로 수화기를 내려놓지 않습니다.
2. 혹시나 상대방이 마지막 내 인사를 못 듣고 "여보세요? 끊었어?"라고 다시 물어볼까 봐, 수화기를 귀에 대고 1분 정도 기다리는 겁니다.
3. 이 1분 기다리는 시간이 TIME_WAIT인데, 전화를 하루에 만 통씩 걸어야 하는 콜센터에서는 전화기가 부족해지는 문제가 생기는 원리입니다.
