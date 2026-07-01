---
title: "TCP vs UDP vs SCTP 비교 (TCP UDP SCTP Comparison)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 30
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP, UDP, SCTP를 처음 봐도 세 전송 프로토콜이 연결, 신뢰성, 메시지 경계, 멀티스트리밍을 어떻게 다르게 제공하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TCP는 신뢰성 있는 byte stream, UDP는 비연결 datagram, SCTP는 message 기반 다중 스트림·다중 홈 전송 프로토콜
- **왜 필요한가**: 애플리케이션마다 순서 보장, 지연, 메시지 경계, 멀티홈, 재전송 요구가 다르다. 전송 계층 선택은 서비스 특성과 장애 모델에 맞춰야 한다.
- **핵심 직관**: TCP는 등기 우편, UDP는 엽서, SCTP는 여러 창구와 예비 주소를 가진 등기 우편에 가깝다.

## 깊이 이해
- **배경·문제의식**: TCP는 웹·DB처럼 순서와 신뢰성이 필요한 서비스에 적합하지만 head-of-line blocking이 있다. UDP는 DNS·VoIP처럼 애플리케이션이 손실을 처리하거나 낮은 초기 지연을 중시할 때 사용한다. SCTP는 통신망 신호 처리처럼 메시지 경계와 멀티홈을 요구하는 환경에서 설계되었다.
- **작동 원리**: TCP는 3-way handshake 후 byte stream을 seq/ack로 관리한다. UDP는 연결 상태 없이 datagram을 전송한다. SCTP는 4-way cookie handshake, association, stream, chunk, multi-homing을 사용한다.
- **비유**: TCP는 줄 하나로 순서대로 물건을 보내는 택배, UDP는 빠르게 던지는 메모, SCTP는 여러 줄과 예비 배송지를 가진 업무 전송 시스템이다.
- **구체 예시**: HTTP/1.1은 TCP 80/443, DNS 질의는 UDP 53을 기본 사용하고, Diameter·SIGTRAN 같은 통신 제어는 SCTP association과 multi-stream을 활용한다.
- **흔한 오해·주의점**: UDP가 항상 지연이 낮은 것은 아니다. 혼잡 제어와 재전송을 애플리케이션이 직접 구현하지 않으면 packet loss 환경에서 품질이 급격히 떨어진다.

## 연결 개념
- TCP 3-way handshake — TCP 연결 성립
- QUIC — UDP 위에서 신뢰성, 암호화, stream을 구현
- SCTP multihoming — endpoint 장애 대비 경로 이중화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TCP·UDP·SCTP 비교 답안은 연결성, 신뢰성, 순서, 메시지 경계, 혼잡 제어, 적용 서비스를 같은 축으로 비교한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP, UDP, SCTP는 전송 계층에서 연결 관리, 신뢰성, 메시지 단위, 다중 경로 지원 범위가 다른 프로토콜이다.
> 2. **가치**: 애플리케이션 요구에 맞춰 순서 보장, 낮은 초기 지연, 멀티스트림·멀티홈 기능을 선택하게 한다.
> 3. **판단 포인트**: TCP는 byte stream, UDP는 datagram, SCTP는 message-oriented association과 multi-streaming이 핵심 차이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전송 프로토콜 비교 역량 확인 | 연결, 신뢰성, 순서, 메시지 경계 | TCP는 신뢰, UDP는 비신뢰만 단순 반복 |
| 적용 서비스 판단 확인 | HTTP/DB, DNS/VoIP/QUIC, SIGTRAN/Diameter | 서비스 예시와 선택 기준 누락 |
| 운영 리스크 이해 확인 | HOL blocking, UDP loss, SCTP middlebox | 혼잡 제어와 방화벽 통과성 누락 |

> 요약: 이 문제는 세 프로토콜을 같은 비교축으로 놓고 서비스 요구사항별 선택 근거를 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: TCP·UDP·SCTP는 애플리케이션 간 데이터를 전달하는 전송 계층 프로토콜
- 특징: TCP는 연결형 신뢰성 전송, UDP는 비연결 datagram 전송, SCTP는 message 기반 association과 multi-streaming을 제공
- 선택 기준: 서비스 지연, 손실 허용, 메시지 경계, 경로 이중화 요구에 따라 프로토콜 선택이 달라짐

---

## Ⅱ. 구조 및 구성요소

```text
Application Requirement
  / Reliable Ordered Stream -> TCP
  / Stateless Datagram -> UDP
  / Message Multi-Stream Multi-Home -> SCTP
Transport Header -> Port/Checksum/State -> Network
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| TCP | 연결형 byte stream 제공 | 3-way handshake, seq/ack, cwnd |
| UDP | 비연결 datagram 전달 | 8 byte header, connection state 없음 |
| SCTP | association 기반 message 전송 | chunk, stream, multi-homing |
| Port | 애플리케이션 식별 | TCP/UDP/SCTP port 공간 |
| Checksum | 오류 검출 | UDP IPv4 checksum optional, IPv6 mandatory |

> 요약: 세 프로토콜은 port와 checksum을 공유하지만 연결 상태, 데이터 단위, 신뢰성 제공 범위가 다르다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Service Requirement Identify -> Protocol Select
  -> Connection or Datagram Setup
  -> Data Transfer with Reliability Policy
  -> Loss/Order/Timeout Handling
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션의 순서, 손실, 지연 요구 식별 | SLO, packet loss tolerance |
| 2 | TCP 연결, UDP datagram, SCTP association 중 선택 | handshake, state table |
| 3 | 전송 중 ACK, timeout, checksum, stream 처리 | retransmission, jitter |
| 4 | 장애 시 재전송, 애플리케이션 retry, multi-homing 적용 | RTO, failover time |

> 요약: 전송 프로토콜 선택은 서비스 요구를 먼저 정하고 연결·신뢰성·장애 처리 방식을 맞추는 절차이다.

---

## Ⅳ. 특징

| 구분 | TCP | UDP | SCTP |
|:---|:---|:---|:---|
| 연결성 | 연결형, 3-way handshake | 비연결, 상태 없음 | association, cookie handshake |
| 신뢰성 | seq/ack, 재전송, 순서 보장 | 앱 책임 | message 단위 신뢰성 |
| 데이터 단위 | byte stream | datagram | message, chunk, stream |
| 주요 용도 | HTTP/1.1, DB, SSH | DNS, VoIP, QUIC 기반 | SIGTRAN, Diameter |
| 판단 지표 | RTT, cwnd, RTO | loss, jitter, app retry | stream count, failover time |

> 요약: TCP는 순서 있는 stream, UDP는 상태 없는 datagram, SCTP는 message와 multi-stream이 중심이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | TCP | UDP/SCTP | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | OS 커널 신뢰성 전송 | UDP는 앱 구현, SCTP는 association | 앱이 손실을 직접 처리할 수 있는지 |
| 비용/성능 | handshake와 HOL blocking | UDP 낮은 header 비용, SCTP stream 분리 | 지연, packet loss, 메시지 경계 |
| 운영/위험 | SYN flood, TIME_WAIT | UDP amplification, SCTP middlebox 차단 | 방화벽, NAT, DDoS 대응 |

> 요약: 선택 기준은 신뢰성 요구, 지연 민감도, 메시지 경계, 네트워크 장비 통과성이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| TCP HOL Blocking | 순서 보장으로 후속 byte 대기 | HTTP/2 stream, QUIC 검토 | p95 latency, retransmission |
| UDP 손실·증폭 | 재전송 없음, spoofing 가능 | app retry, rate-limit, BCP38 | packet loss, amplification ratio |
| SCTP 통과성 | NAT·방화벽 미지원 | SCTP over DTLS, fallback 설계 | connection failure rate |

> 요약: 프로토콜 리스크는 TCP 순서 대기, UDP 손실·DDoS, SCTP 장비 호환성으로 구분한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전송 품질 | TCP retransmission 기준선 이하, UDP loss 허용치 이하 | pcap, NetFlow |
| 지연 | RTT p95, jitter SLO 준수 | synthetic probe, RTP metric |
| 운영 통제 | 방화벽 정책과 DDoS rate-limit 적용 | rule audit, scrubbing log |

> 요약: 전송 프로토콜 운영 품질은 재전송·손실, RTT·jitter, 보안 통제 적용률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 웹·DB·SSH처럼 순서와 신뢰성이 필요한 서비스는 TCP를 사용하고 connect time, RTO, retransmission을 SLO 지표로 둠
2. DNS·VoIP·게임·QUIC처럼 datagram 기반 처리가 필요한 서비스는 UDP를 사용하되 loss, jitter, amplification 대응을 설계함
3. 메시지 경계와 multi-stream, multi-homing이 필요한 통신 제어 서비스는 SCTP를 검토하고 NAT·방화벽 지원 여부를 사전 검증함

**결론 (2줄):**
- 기술사 판단: 신뢰성 있는 순서 전송은 TCP, 애플리케이션 제어형 datagram은 UDP, 메시지·다중 스트림·다중 홈 요구는 SCTP를 선택함
- 향후 방향: QUIC은 UDP 위에서 TLS 1.3, stream, 혼잡 제어를 구현해 TCP와 UDP 선택 경계를 재편하고 있음

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP, UDP, SCTP를 비교하시오" | 연결·전송·손실 처리 흐름 | 공통 비교축 표 |
| 요구사항 명시형 | "서비스별 프로토콜 선택 방안을 제시하시오" | 요구사항에서 프로토콜 매핑 | 리스크와 지표 기반 선택 기준 |

> 요약: 비교형은 같은 축의 차이, 설계형은 서비스 요구와 운영 리스크를 기준으로 목차를 전환한다.
