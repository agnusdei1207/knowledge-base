---
title: "TCP 3-way handshake (TCP 3-way Handshake)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 26
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP 3-way handshake를 처음 봐도 왜 SYN, SYN-ACK, ACK 세 단계가 필요한지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TCP 연결 시작 시 양 끝이 초기 sequence number와 수신 가능 상태를 확인하는 3단계 절차
- **왜 필요한가**: TCP는 신뢰성 있는 byte stream을 제공하므로 데이터 전송 전에 양방향 통신 가능 여부와 sequence 번호 기준을 맞춰야 한다.
- **핵심 직관**: 전화를 걸 때 "들리나요?", "네 들립니다, 제 목소리도 들리나요?", "네 들립니다"라고 확인한 뒤 대화를 시작하는 과정이다.

## 깊이 이해
- **배경·문제의식**: IP는 비연결형이라 패킷이 사라지거나 순서가 바뀔 수 있다. TCP는 연결 상태, sequence/acknowledgment, window size를 관리해 데이터 흐름을 제어한다.
- **작동 원리**: 클라이언트가 SYN과 client ISN을 보낸다. 서버가 SYN-ACK와 server ISN, client ISN+1을 응답한다. 클라이언트는 이 SYN-ACK를 수신하는 즉시 ESTABLISHED로 전환하며 ACK로 server ISN+1을 확인해 전송하고, 서버는 그 ACK를 수신한 시점에 비로소 ESTABLISHED로 전환된다.
- **비유**: 양쪽 회의 참가자가 서로 마이크와 스피커가 동작하는지 확인하고 발언 순서 번호를 맞춘 뒤 회의를 시작하는 것과 같다.
- **구체 예시**: Client `SYN seq=1000`, Server `SYN-ACK seq=5000 ack=1001`, Client `ACK ack=5001`이면 이후 데이터는 각자의 다음 sequence 번호부터 전송된다.
- **흔한 오해·주의점**: 3-way handshake 완료는 애플리케이션 정상 응답을 의미하지 않는다. TCP 연결이 ESTABLISHED여도 TLS handshake, HTTP 인증, 서버 thread pool에서 실패할 수 있다.

## 연결 개념
- TCP 4-way handshake — 연결 종료 시 FIN/ACK 절차
- SYN Flood — handshake half-open 상태를 악용하는 DoS
- TCP 흐름 제어 — window size로 수신 버퍼 범위 조절

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TCP 3-way handshake 답안은 SYN/SYN-ACK/ACK, ISN, 상태 전이, SYN backlog, 장애 분석 포인트를 포함해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 3-way handshake는 양단이 초기 sequence number와 수신 가능 상태를 교환해 연결을 ESTABLISHED로 전환하는 절차이다.
> 2. **가치**: 데이터 전송 전 양방향 도달성, ACK 처리, window size, MSS option을 협상해 신뢰성 있는 전송 기반을 만든다.
> 3. **판단 포인트**: SYN 재전송, SYN backlog, RST, firewall drop, TLS handshake 실패를 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 연결 성립 원리 확인 | SYN, SYN-ACK, ACK와 seq/ack 증가 | 단순 3단계 명칭만 나열 |
| 장애 분석 역량 확인 | SYN retry, RST, timeout, backlog | TCP 연결과 애플리케이션 성공 혼동 |
| 보안 리스크 이해 확인 | SYN flood, SYN cookie, half-open | DoS 대응 누락 |

> 요약: 이 문제는 3단계 메시지와 상태 전이를 seq/ack 번호, 장애 원인, 보안 대응까지 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: TCP 연결을 시작하기 위해 SYN, SYN-ACK, ACK를 순서대로 교환하는 3단계 제어 절차
- 배경: IP는 비연결형이라 양방향 통신 가능 여부와 초기 sequence number를 사전에 맞추지 않으면 신뢰성 있는 전송을 보장할 수 없음
- 필요성: 연결 성립 단계와 상태 전이를 정확히 이해해야 장애 분석과 SYN flood 대응 판단의 근거로 활용 가능

---

## Ⅱ. 구조 및 구성요소

```text
Client CLOSED -> SYN_SENT
  -> SYN(seq=x) -> Server LISTEN/SYN_RECEIVED
  <- SYN-ACK(seq=y, ack=x+1)
  -> ACK(ack=y+1) -> ESTABLISHED
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SYN | 연결 요청과 client ISN 전달 | TCP option, MSS, window scale 포함 |
| SYN-ACK | 서버 수락과 server ISN 전달 | ack는 client ISN+1 |
| ACK | 서버 ISN 수신 확인 | 이후 데이터 전송 가능 |
| State Table | 연결 상태 관리 | SYN_SENT, SYN_RECEIVED, ESTABLISHED |
| SYN Backlog | half-open 연결 대기열 | backlog 초과 시 drop 또는 cookie |

> 요약: 3-way handshake는 제어 flag와 seq/ack 번호, 상태 테이블, backlog 자원으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client Active Open -> SYN Send -> Server Passive Open
  -> SYN-ACK Send -> Client ACK Send
  -> State ESTABLISHED -> Data Transfer
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 SYN과 ISN x 전송 | SYN_SENT, seq=x |
| 2 | 서버가 SYN queue에 half-open 상태 저장 | SYN_RECEIVED, backlog 사용률 |
| 3 | 서버가 SYN-ACK와 ISN y, ack x+1 전송 | SYN-ACK retransmission |
| 4 | 클라이언트가 SYN-ACK 수신 즉시 ESTABLISHED로 전환하고 ACK y+1 전송 | client-side established count |
| 5 | 서버가 클라이언트의 ACK를 수신한 시점에 ESTABLISHED로 전환 | server-side established session count |

> 요약: 클라이언트는 SYN-ACK 수신 시, 서버는 마지막 ACK 수신 시 각각 ESTABLISHED로 전환되며 연결은 서버가 ACK를 수신하는 시점에 완전히 성립한다.

---

## Ⅳ. 특징

| 구분 | 정상 handshake | 실패·공격 상황 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 메시지 | SYN, SYN-ACK, ACK | SYN 재전송, RST, timeout | TCP flag, seq/ack |
| 상태 | SYN_SENT, SYN_RECEIVED, ESTABLISHED | half-open 증가 | SYN backlog |
| 옵션 | MSS, window scale, SACK permitted | MTU mismatch, option drop | MSS 1460 예시 |
| 보안 | 정상 연결 성립 | SYN flood | SYN cookie, rate-limit |

> 요약: handshake 분석은 flag 순서뿐 아니라 상태, TCP option, backlog 자원을 함께 확인해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | TCP 3-way handshake | UDP 전송 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 연결 성립 후 byte stream | 연결 절차 없음 | 신뢰성·순서 보장 필요 시 TCP |
| 비용/성능 | 1 RTT 연결 비용 발생 | 초기 RTT 비용 없음 | 짧은 요청은 RTT 영향 검토 |
| 운영/위험 | SYN flood, backlog 고갈 | spoofing, loss 처리 앱 부담 | 보안 장비와 rate-limit 기준 |

> 요약: TCP는 연결 신뢰성을 제공하지만 초기 1 RTT와 상태 자원 비용이 발생한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 연결 지연 | SYN/SYN-ACK 재전송, RTT 증가 | 경로 점검, anycast, TCP Fast Open 검토 | TCP connect time |
| SYN Flood | 대량 half-open 연결 | SYN cookie, backlog 확대, rate-limit | SYN_RECV count |
| 방화벽 차단 | stateful rule 누락, asymmetric routing | rule audit, 양방향 경로 확인 | SYN no SYN-ACK capture |

> 요약: handshake 리스크는 지연, half-open 자원, 경로 차단이며 packet capture와 상태 지표로 분리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 연결 성공률 | TCP connect success 99.9% 이상 | synthetic probe, LB metric |
| 연결 지연 | p95 connect time SLO 준수 | APM, tcpdump timestamp |
| backlog 상태 | SYN backlog 사용률 80% 이하 | netstat, ss, kernel metric |

> 요약: 3-way handshake 품질은 연결 성공률, connect time, backlog 사용률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 접속 장애 시 client/server 양단 pcap으로 SYN, SYN-ACK, ACK 도달 여부와 RST 송신 주체를 확인함
2. 인터넷 서비스는 SYN backlog, SYN cookie, LB connection limit을 설정하고 SYN_RECV count를 모니터링함
3. TLS·HTTP 장애와 TCP handshake 장애를 분리해 TCP connect time, TLS handshake time, HTTP response time을 각각 측정함

**결론 (2줄):**
- 기술사 판단: SYN-ACK가 없으면 네트워크·방화벽·서버 listen 문제, ACK 후 실패는 TLS·애플리케이션 문제로 분리함
- 향후 방향: QUIC, TCP Fast Open, SYN cookie, eBPF observability로 연결 지연과 half-open 공격을 함께 관리해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP 3-way handshake를 설명하시오" | SYN/SYN-ACK/ACK와 상태 전이 | TCP option, SYN flood |
| 요구사항 명시형 | "접속 장애 분석 방안을 제시하시오" | pcap 기반 실패 지점 분리 | backlog, 방화벽, RST 리스크 |

> 요약: 설명형은 연결 성립 원리, 방안형은 장애 지점과 보안 대응 중심으로 전환한다.
