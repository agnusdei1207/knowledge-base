---
title: ENQ / ACK / NAK / EOT 제어 문자
date: '2026-03-03'
tags:
- studynote-network
---

> **핵심 인사이트 3줄**
> 1. ENQ·ACK·[[211_nak_negative_acknowledgement|NAK]]·EOT는 [[019_bsc|BSC]](Binary [[010_동기식_비동기식_전송|Synchronous]] Communication) [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 핵심 제어 문자로, [[001_dikw_pyramid|데이터]] 링크 계층의 회선 확보·긍정/부정 응답·전송 종료를 담당한다.
> 2. 이 제어 문자 체계는 반이중 통신에서 양방향 [[001_dikw_pyramid|데이터]] 교환을 위한 기본 핸드셰이킹 메커니즘의 원형이며, 현대 [[949_arq_automatic_repeat_request_go_back_n_selective|ARQ]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 직접적 선조다.
> 3. TCP의 SYN/ACK, HTTP의 요청/응답, Modbus [[897_rtu_remote_terminal_unit|RTU]] 등 현대 [[295_protocol_field_tcp_udp_icmp|프로토콜]]에서도 같은 개념이 다른 형태로 살아있다.

---

## Ⅰ. [[103_ascii|ASCII]] 제어 문자 개요

[[019_bsc|BSC]](Binary [[010_동기식_비동기식_전송|Synchronous]] Communication)에서 사용하는 제어 문자는 **[[103_ascii|ASCII]] 코드 표준(1963)**으로 정의된 비인쇄 문자들이다.

| 문자  | [[103_ascii|ASCII]] | 이름                      | 기능        |
|------|-------|--------------------------|------------|
| ENQ  | 0x05  | Enquiry (문의)            | 회선 확보 요청 |
| ACK  | 0x06  | Acknowledgement (긍정 응답) | 수신 성공 [[396_validation|확인]] |
| [[211_nak_negative_acknowledgement|NAK]]  | 0x15  | [[211_nak_negative_acknowledgement|Negative Acknowledgement]] | 수신 오류, 재전송 요청 |
| EOT  | 0x04  | End of Transmission (전송 종료) | 회선 해제 |
| STX  | 0x02  | Start of Text           | 본문 시작 |
| ETX  | 0x03  | End of Text             | 본문 종료 |
| SYN  | 0x16  | [[010_동기식_비동기식_전송|Synchronous]] [[611_cpu_idle_wait_optimization|Idle]]        | 동기 유지 |

📢 **섹션 요약 비유**: 제어 문자는 전화 예절 코드다 — "통화 가능?" (ENQ), "네" (ACK), "잘 못 들었어요" ([[211_nak_negative_acknowledgement|NAK]]), "끊을게요" (EOT).

---

## Ⅱ. [[019_bsc|BSC]] [[001_dikw_pyramid|데이터]] 전송 시퀀스

### 정상 전송 시나리오

```
송신 측                          수신 측
   │                                │
   │──────── ENQ ──────────────────→│  (회선 확보 요청)
   │←─────── ACK ───────────────────│  (회선 사용 허가)
   │                                │
   │──── STX [데이터] ETX BCC ─────→│  (블록 1 전송)
   │←─────── ACK ───────────────────│  (블록 1 수신 확인)
   │                                │
   │──── STX [데이터] ETX BCC ─────→│  (블록 2 전송)
   │←─────── ACK ───────────────────│  (블록 2 수신 확인)
   │                                │
   │──────── EOT ──────────────────→│  (전송 종료)
```

### 오류 발생 시나리오 ([[211_nak_negative_acknowledgement|NAK]])

```
   │──── STX [데이터] ETX BCC ─────→│  (블록 전송)
   │←─────── NAK ───────────────────│  (CRC 오류 감지)
   │──── STX [데이터] ETX BCC ─────→│  (동일 블록 재전송)
   │←─────── ACK ───────────────────│  (재전송 성공)
```

📢 **섹션 요약 비유**: [[019_bsc|BSC]] 전송 시퀀스는 소포 배달 절차다 — 벨 누르기(ENQ), 문 열기(ACK), 소포 전달, 사인(ACK), 영수증 끊기(EOT). 내용물이 파손되면 NAK로 재배송 요청.

---

## Ⅲ. ACK0 / ACK1 — 교대 [[396_validation|확인]] 응답

BSC에서는 오류 감지를 위해 **ACK0과 ACK1을 교대로 사용**해 블록 번호를 구분한다.

```
블록 1 전송 → ACK1 수신 (홀수 블록 확인)
블록 2 전송 → ACK0 수신 (짝수 블록 확인)
블록 3 전송 → ACK1 수신 (홀수 블록 확인)
...
```

이는 **Stop-and-Wait ARQ의 1비트 순서번호**와 동일한 원리다.

📢 **섹션 요약 비유**: ACK0/ACK1 교대는 홀수·짝수 수업 시간 [[396_validation|확인]]이다 — 1교시(ACK1), 2교시(ACK0)처럼 번갈아가며 체크해 빠진 수업이 있는지 [[396_validation|확인]]한다.

---

## Ⅳ. ENQ/ACK에서 [[405_tcp_transmission_control_protocol_connection_oriented|TCP]]/IP까지 — 발전 계보

```
BSC ENQ/ACK (1960년대)
        ↓
HDLC I-Frame/S-Frame (1970년대) — 더 효율적인 비트 지향
        ↓
TCP SYN/ACK (1974년~) — 연결 지향, 스트림 기반
  3-Way Handshake: SYN → SYN-ACK → ACK
        ↓
QUIC (2018~) — UDP + ACK, 0-RTT, 손실 기반 혼잡 제어
```

### 현대 [[295_protocol_field_tcp_udp_icmp|프로토콜]]과의 대응

| [[019_bsc|BSC]] 제어 문자 | 현대 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 대응            |
|-------------|------------------------------|
| ENQ         | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] SYN / [[461_http_stateless_connection_oriented|HTTP]] 요청           |
| ACK         | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] ACK / [[461_http_stateless_connection_oriented|HTTP]] 200 OK         |
| [[211_nak_negative_acknowledgement|NAK]]         | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] NACK / [[461_http_stateless_connection_oriented|HTTP]] 400·500      |
| EOT         | [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] FIN / [[461_http_stateless_connection_oriented|HTTP]] Connection: close |

📢 **섹션 요약 비유**: ENQ/ACK는 전화 대화의 원형이다 — "여보세요?"(ENQ), "예"(ACK), "못 들었어요"([[211_nak_negative_acknowledgement|NAK]]), "끊을게요"(EOT). 인터넷도 결국 같은 대화 구조다.

---

## Ⅴ. Modbus [[897_rtu_remote_terminal_unit|RTU]] — 산업 현장의 ENQ/ACK

산업 자동화에서는 **Modbus [[897_rtu_remote_terminal_unit|RTU]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]**이 ENQ/ACK 개념을 계승한다.

```
마스터(PLC)                    슬레이브(센서/액추에이터)
   │                                   │
   │──[주소][기능코드][데이터][CRC]───→│ (ENQ 역할)
   │←──[주소][기능코드][데이터][CRC]───│ (ACK 역할)
   │←──[주소][오류코드][CRC]───────────│ (NAK 역할: 예외 응답)
```

현대 [[101_iot_concept|IoT]]·[[894_scada|SCADA]]·스마트팩토리에서도 이 원리가 기반이 된다.

📢 **섹션 요약 비유**: Modbus는 공장 무전기 통신이다 — "1번 로봇, 현재 온도 알려줘"(마스터 요청), "온도 75도"(슬레이브 응답). ENQ/ACK 구조가 공장 자동화에 살아있다.

---

## 📌 관련 개념 맵

```
ENQ / ACK / NAK / EOT
├── 프로토콜 컨텍스트
│   └── BSC (Binary Synchronous Communication)
├── 기능
│   ├── ENQ: 회선 확보 요청
│   ├── ACK (ACK0/ACK1): 긍정 응답
│   ├── NAK: 부정 응답, 재전송 요청
│   └── EOT: 전송 종료, 회선 해제
├── 발전 계보
│   ├── HDLC I/S/U 프레임
│   ├── TCP SYN/ACK/FIN
│   └── HTTP Request/Response
└── 산업 응용
    ├── Modbus RTU
    └── SCADA 프로토콜
```

---

## 📈 관련 키워드 및 발전 흐름도

```
┌─────────────────────────────────────────────────────────────────┐
│             ENQ/ACK/NAK/EOT 발전 흐름                           │
├──────────────┬────────────────────┬─────────────────────────────┤
│ 1960년대     │ BSC·ASCII 정의     │ 제어 문자 체계 표준화        │
│ 1970년대     │ HDLC 비트 지향     │ ACK→RR, NAK→REJ 으로 발전   │
│ 1974년       │ TCP 등장           │ SYN/ACK 3-Way Handshake     │
│ 1980년대     │ Modbus RTU         │ 산업 자동화에 ENQ/ACK 계승   │
│ 2000년대     │ HTTP/SMTP          │ 요청/응답 패러다임 지배적     │
│ 2018년       │ QUIC/HTTP3         │ ACK 최적화, 0-RTT 핸드셰이크 │
└──────────────┴────────────────────┴─────────────────────────────┘

핵심 키워드 연결:
ENQ → 회선 확보 → ACK → 데이터 전송 → EOT
  ↓       ↓        ↓         ↓
오류    폴링    긍정응답   NAK 재전송
  ↓
TCP 3-way → HTTPS → REST API 요청/응답
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. ENQ는 "지금 전화해도 돼?"라는 문자다 — 통화를 시작하기 전에 상대방이 받을 수 있는지 [[396_validation|확인]]한다.
2. ACK는 "잘 받았어", NAK는 "다시 보내줘"다 — 편지가 제대로 도착했는지(ACK) 또는 찢어졌는지([[211_nak_negative_acknowledgement|NAK]])를 알려준다.
3. EOT는 "이제 끊을게"다 — 전화 통화를 마치고 회선을 끊겠다고 정중하게 알리는 신호다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 1120

← **이전**: [[032_회선_제어_규약|회선 제어 규약 (Line Control Protocol)]]
**다음**: [[034_에러_검출율|에러 검출 방식 — 패리티·CRC·해밍코드]] →

---
