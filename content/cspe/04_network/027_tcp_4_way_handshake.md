---
title: "TCP 4-way handshake·연결 해제 (TCP 4-way Handshake)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 27
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP 4-way handshake를 처음 봐도 왜 종료는 연결 시작보다 단계가 많고 TIME_WAIT이 왜 필요한지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TCP 연결 종료 시 양쪽 송신 방향을 각각 닫기 위해 FIN과 ACK를 교환하는 절차
- **왜 필요한가**: TCP 연결은 전이중 통신이다. 한쪽이 보낼 데이터가 없어도 상대는 아직 보낼 데이터가 남아 있을 수 있으므로 방향별 종료 확인이 필요하다.
- **핵심 직관**: 통화 종료에서 한 사람이 "저는 할 말 끝났습니다"라고 말해도 상대가 마지막 말을 마친 뒤 끊는 과정이다.

## 깊이 이해
- **배경·문제의식**: TCP는 byte stream 신뢰성을 보장하므로 종료 중에도 남은 데이터와 ACK가 유실되지 않도록 상태를 관리한다. FIN은 송신 종료를 의미하고, ACK는 상대 FIN 수신 확인이다.
- **작동 원리**: Active close 측이 FIN을 보내고 FIN_WAIT_1로 간다. 상대는 ACK 후 CLOSE_WAIT가 되고, 애플리케이션 정리 후 FIN을 보낸다. 최초 종료자는 ACK 후 TIME_WAIT에 머물러 지연 패킷과 마지막 ACK 재전송을 처리한다.
- **비유**: 회의록을 마감할 때 한쪽이 먼저 제출 종료를 선언하고, 상대가 남은 문서를 제출한 뒤 양쪽이 접수 확인을 끝내는 절차다.
- **구체 예시**: 웹 클라이언트가 FIN을 보내고 서버가 ACK한다. 서버가 응답 잔여 데이터를 보낸 뒤 FIN을 보내면 클라이언트가 ACK하고 TIME_WAIT 2MSL 동안 대기한다.
- **흔한 오해·주의점**: TIME_WAIT은 무의미한 낭비 상태가 아니다. 같은 4-tuple 재사용 전 지연 세그먼트 제거와 마지막 ACK 재전송을 위해 필요하다.

## 연결 개념
- TCP 3-way handshake — 연결 성립 절차
- TIME_WAIT·CLOSE_WAIT — 종료 상태와 운영 장애 지표
- RST — 비정상 연결 종료와 애플리케이션 오류 분석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TCP 종료 답안은 FIN/ACK 4단계, half-close, TIME_WAIT, CLOSE_WAIT 누수, RST 차이를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 4-way handshake는 전이중 연결의 각 송신 방향을 FIN과 ACK로 독립 종료하는 절차이다.
> 2. **가치**: 잔여 데이터 전송과 지연 세그먼트 처리를 보장해 연결 종료 중 데이터 손실과 포트 재사용 충돌을 줄인다.
> 3. **판단 포인트**: TIME_WAIT은 정상 대기, CLOSE_WAIT 증가는 애플리케이션 close 누락, RST는 비정상 종료 신호로 분리한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 종료 원리 확인 | FIN, ACK, half-close, 상태 전이 | 3-way handshake와 동일하게 서술 |
| 운영 장애 분석 확인 | TIME_WAIT, CLOSE_WAIT, FIN_WAIT | TIME_WAIT을 오류로 단정 |
| 비정상 종료 구분 확인 | FIN 정상 종료 vs RST 강제 종료 | RST 원인과 로그 분석 누락 |

> 요약: 이 문제는 TCP 종료 상태를 애플리케이션 close 처리와 포트 자원 관리 관점으로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

TCP 4-way handshake는 TCP 연결을 정상 종료하기 위한 FIN/ACK 교환 절차이다. TCP는 전이중 통신이므로 양방향 송신 종료가 각각 확인되어야 한다. TIME_WAIT, CLOSE_WAIT, RST 해석은 서버 접속 장애와 포트 고갈 분석의 핵심이다.

---

## Ⅱ. 구조 및 구성요소

```text
Active Closer ESTABLISHED -> FIN -> FIN_WAIT_1
  <- ACK -> FIN_WAIT_2
  <- FIN -> TIME_WAIT
  -> ACK -> CLOSED after 2MSL
Passive Closer: CLOSE_WAIT -> LAST_ACK -> CLOSED
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| FIN | 한쪽 송신 종료 알림 | 데이터 수신은 계속 가능 |
| ACK | FIN 수신 확인 | FIN sequence도 1 증가 |
| TIME_WAIT | 지연 세그먼트와 마지막 ACK 처리 | 일반적으로 2MSL 대기 |
| CLOSE_WAIT | 상대 FIN 수신 후 앱 close 대기 | 누적 시 애플리케이션 누수 의심 |
| RST | 연결 강제 종료 | 포트 미수신, 정책 차단, 앱 reset |

> 요약: TCP 종료 구조는 방향별 FIN/ACK와 TIME_WAIT·CLOSE_WAIT 상태 관리로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Application Close -> FIN Send -> Peer ACK
  -> Peer Data Drain -> Peer FIN
  -> Final ACK -> TIME_WAIT -> CLOSED
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | active closer가 FIN 전송 | FIN_WAIT_1, seq 증가 |
| 2 | passive closer가 ACK 후 CLOSE_WAIT 진입 | ACK number, socket state |
| 3 | passive closer 애플리케이션 종료 후 FIN 전송 | LAST_ACK, close call |
| 4 | active closer가 ACK 후 TIME_WAIT 대기 | TIME_WAIT count, 2MSL |

> 요약: TCP 종료는 먼저 닫은 쪽과 나중에 닫은 쪽의 상태가 다르며, TIME_WAIT과 CLOSE_WAIT을 분리 해석해야 한다.

---

## Ⅳ. 특징

| 구분 | 정상 FIN 종료 | RST 종료 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 절차 | FIN/ACK 4단계 | 즉시 연결 제거 | TCP flag FIN/RST |
| 데이터 처리 | 잔여 데이터 전송 가능 | 버퍼 데이터 폐기 가능 | seq/ack 확인 |
| 운영 상태 | TIME_WAIT, CLOSE_WAIT | connection reset log | 2MSL, socket count |
| 장애 신호 | CLOSE_WAIT 누적 | 방화벽 reset, 앱 crash | netstat, ss |

> 요약: FIN은 정상 종료, RST는 강제 종료이며 socket 상태와 패킷 flag를 함께 분석해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Active Close 측 | Passive Close 측 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | FIN_WAIT, TIME_WAIT 보유 | CLOSE_WAIT, LAST_ACK 보유 | 어느 쪽이 먼저 close 했는지 pcap으로 확인 |
| 비용/성능 | TIME_WAIT socket과 ephemeral port 사용 | CLOSE_WAIT 누수 시 FD 고갈 | socket count, port range |
| 운영/위험 | 포트 재사용 지연 | 애플리케이션 close 누락 | sysctl 조정 전 앱 원인 확인 |

> 요약: 종료 장애는 TIME_WAIT 조정보다 CLOSE_WAIT 원인과 active closer 위치를 먼저 확인해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| CLOSE_WAIT 누적 | 애플리케이션 socket close 누락 | connection pool 코드 점검 | CLOSE_WAIT count |
| TIME_WAIT 과다 | 짧은 연결 대량 생성 | keep-alive, connection reuse | TIME_WAIT count, port usage |
| RST 증가 | LB idle timeout, 앱 crash, 방화벽 reset | timeout 정렬, 로그 상관분석 | TCP reset rate |

> 요약: 종료 리스크는 앱 close 누락, 짧은 연결 폭증, timeout 불일치로 분류해 대응한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Socket 상태 | CLOSE_WAIT 지속 증가 0건 | ss, netstat, eBPF |
| 포트 사용률 | ephemeral port 사용률 80% 이하 | OS metric, connection table |
| 종료 오류 | RST rate 기준선 초과 시 알림 | LB log, pcap, APM |

> 요약: TCP 종료 품질은 CLOSE_WAIT, ephemeral port, RST rate로 관리한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 접속 종료 장애는 pcap으로 FIN/ACK/RST 송신 주체를 확인하고 애플리케이션 로그의 close 호출 시점과 대조함
2. CLOSE_WAIT 누적 시 connection pool, socket close, thread leak을 점검하고 FD 사용률과 GC pause를 함께 확인함
3. 짧은 HTTP 요청은 keep-alive, HTTP/2 multiplexing, LB idle timeout 정렬로 TIME_WAIT과 포트 사용률을 낮춤

**결론 (2줄):**
- 기술사 판단: TIME_WAIT은 정상 보호 상태, CLOSE_WAIT 증가는 애플리케이션 종료 처리 결함 신호로 판단함
- 향후 방향: eBPF socket tracing과 APM을 결합해 FIN/RST 원인과 코드 경로를 함께 관측해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP 연결 해제를 설명하시오" | FIN/ACK 상태 전이와 TIME_WAIT | FIN 종료와 RST 종료 비교 |
| 요구사항 명시형 | "Socket 고갈 대응 방안을 제시하시오" | CLOSE_WAIT, TIME_WAIT 원인 분리 | 포트·FD·timeout 지표 |

> 요약: 설명형은 종료 절차, 방안형은 socket 상태별 원인과 운영 지표 중심으로 전환한다.
