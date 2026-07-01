---
title: "패킷 캡처·프로토콜 분석 (Packet Capture Protocol Analysis)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 25
---

# 📖 【암기용】 개념 완전 이해

> 목적: 패킷 캡처와 프로토콜 분석을 처음 봐도 어떤 지점에서 무엇을 잡고 어떤 증거로 장애 원인을 찾는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 네트워크 구간의 패킷을 수집해 헤더, payload, 시간 순서, 세션 흐름을 분석하는 장애·보안 진단 기법
- **왜 필요한가**: 애플리케이션 로그만으로는 TCP 재전송, DNS 지연, TLS handshake 실패, MTU 문제를 확인하기 어렵다. 패킷 캡처는 wire-level 증거를 제공한다.
- **핵심 직관**: 대화 녹음처럼 네트워크가 실제로 주고받은 말을 시간순으로 다시 보는 것이다.

## 깊이 이해
- **배경·문제의식**: 네트워크 장애는 서버, 클라이언트, 스위치, 방화벽, DNS 중 어디서 발생했는지 모호하다. 캡처 위치를 client side, server side, middlebox 전후로 나누면 패킷 손실과 변조 위치를 추정할 수 있다.
- **작동 원리**: NIC, SPAN, TAP, tcpdump, Wireshark, Zeek 같은 도구가 패킷을 pcap 형식으로 저장한다. 분석자는 5-tuple, TCP flag, sequence/ack, RTT, retransmission, DNS response code, HTTP status를 확인한다.
- **비유**: 택배 분실을 추적할 때 접수, 물류센터, 배송차량 스캔 기록을 비교해 어느 지점에서 멈췄는지 찾는 것과 같다.
- **구체 예시**: 클라이언트 캡처에는 SYN 재전송 3회가 보이고 서버 측에는 SYN이 없으면 중간 방화벽·라우팅 문제다. 서버 측에는 SYN-ACK가 나갔는데 클라이언트에 없으면 역방향 경로 또는 NAT 문제를 의심한다.
- **흔한 오해·주의점**: 패킷 캡처가 모든 payload를 보여주는 것은 아니다. TLS 암호화, NIC offload, 캡처 손실, SPAN oversubscription 때문에 해석 전 수집 품질을 먼저 확인해야 한다.

## 연결 개념
- TCP handshake — 연결 성공·실패를 판단하는 기본 패턴
- MTU·fragmentation — Path MTU 문제와 blackhole 진단
- IDS·NDR — 패킷 기반 보안 분석과 장기 flow 관측

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 패킷 분석 답안은 캡처 위치, 필터, 시간 동기화, 프로토콜 필드, 증거 기반 원인 분리를 포함해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 패킷 캡처는 네트워크 구간의 실제 프레임·패킷을 pcap으로 수집해 프로토콜 헤더와 세션 흐름을 분석하는 기법이다.
> 2. **가치**: 로그로 확인하기 어려운 TCP retransmission, DNS NXDOMAIN, TLS alert, MTU blackhole을 증거 기반으로 분리한다.
> 3. **판단 포인트**: 캡처 지점, 시간 동기화, BPF filter, packet loss, 개인정보 masking을 함께 관리해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 장애 분석 절차 확인 | 캡처 위치, 필터, 시간순 흐름 분석 | 도구 이름만 나열 |
| 프로토콜 해석 역량 확인 | TCP flag, seq/ack, RTT, retransmission | 단순 ping 성공 여부로 판단 |
| 운영·보안 통제 확인 | 개인정보, TLS, 캡처 보관, 권한 통제 | pcap 민감정보 유출 위험 누락 |

> 요약: 이 문제는 패킷을 어떻게 잡고 어떤 필드로 원인을 판정하는지 단계별 증거를 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 구간 패킷을 시간순 수집해 원인을 찾는 기법
- 배경: 서버 애플리케이션 로그가 정상이어도 TCP 재전송, DNS 실패, TLS alert, 방화벽 reset은 wire-level 캡처로만 확인되는 경우가 있음
- 필요성: 캡처 위치 선정과 필터 설계가 정확해야 원인 분석 품질이 확보됨

---

## Ⅱ. 구조 및 구성요소

```text
Traffic Source -> Capture Point
  / Client NIC
  / SPAN/TAP
  / Server NIC
Capture Tool -> pcap -> Protocol Decoder -> Timeline Analysis
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Capture Point | 수집 위치 선정 | client, server, middlebox 전후 — SPAN/미러링 수신 NIC는 promiscuous mode로 동작해야 목적지가 아닌 프레임도 캡처 가능 |
| Capture Filter | 캡처 단계에서 대상 트래픽을 사전 제한 | BPF 문법(host/port/net/proto) — 분석 단계의 Wireshark Display Filter(필드 기반 문법, 예: tcp.flags.syn==1)와는 문법·적용 시점이 다름 |
| pcap File | 패킷 저장 형식 | timestamp, frame length |
| Decoder | 프로토콜 필드 해석 | Wireshark, tshark, Zeek |
| Timeline | 흐름·지연 분석 | RTT, retransmission, gap |

> 요약: 패킷 분석 구조는 수집 위치, 필터, pcap, decoder, 시간축 분석으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Problem Define -> Capture Point Select -> Filter Apply
  -> Packet Collect -> Decode Fields
  -> Timeline Compare -> Root Cause Decide
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 장애 시간, 5-tuple, 사용자 IP를 특정 | incident time, flow tuple |
| 2 | 클라이언트·서버·중간 장비 전후 캡처 | NTP sync, packet drop 0건 |
| 3 | TCP, DNS, TLS, HTTP 필드를 해석 | flag, code, alert, status |
| 4 | 양쪽 캡처를 비교해 손실·지연·reset 위치 결정 | RTT, retransmission, RST source |

> 요약: 패킷 분석은 문제 범위 특정, 캡처 위치 선정, 필드 해석, 양단 비교 순서로 원인을 좁힌다.

---

## Ⅳ. 특징

| 구분 | 로그 분석 | 패킷 분석 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 관측 범위 | 애플리케이션 이벤트 | L2~L7 통신 흐름 | pcap, 5-tuple |
| 시간 정밀도 | 로그 timestamp 의존 | 패킷 timestamp 기반 | microsecond timestamp |
| 원인 판별 | 코드·예외 중심 | RTT, retransmission, reset | TCP seq/ack, DNS RCODE |
| 제약 | 로그 누락 가능 | TLS 암호화, 캡처 손실 | SPAN oversubscription |

> 요약: 패킷 분석은 프로토콜 수준 증거를 제공하지만 캡처 품질과 암호화 제약을 함께 검증해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | tcpdump/tshark | Wireshark/Zeek | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | CLI 기반 수집·필터 | Wireshark는 GUI 기반 필드 분석, Zeek는 세션 metadata 로그 추출 | 현장 수집은 tcpdump, 상세 해석은 Wireshark |
| 비용/성능 | 서버 부하와 저장 용량 관리 | 장기 분석은 Zeek log 활용 | 캡처 파일 크기, packet drop 기준 |
| 운영/위험 | 권한 오남용, 민감정보 포함 | pcap 반출 위험 | 마스킹, 암호화 저장, 보관 기간 |

> 요약: 현장 대응은 경량 캡처, 사후 분석은 decoder와 metadata 분석을 조합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 캡처 손실 | NIC 부하, SPAN 포트 초과 | ring buffer, TAP, 필터 축소 | dropped by kernel |
| 오판 | 단일 지점 캡처만 분석 | 양단 동시 캡처, NTP 동기화 | timestamp drift |
| 정보 유출 | pcap에 payload·계정 포함 | 권한 통제, 마스킹, 암호화 저장 | pcap access log |

> 요약: 패킷 분석 리스크는 수집 품질, 해석 오류, 민감정보 유출이며 절차 통제가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수집 품질 | packet drop 0건, 시간 동기화 1초 이내 | tcpdump stats, NTP status |
| 분석 정확도 | 원인 구간 client/server/middlebox로 분리 | 양단 pcap 비교 |
| 보안 통제 | pcap 보관 기간과 접근 권한 명시 | DLP, access audit |

> 요약: 패킷 분석 성과는 drop 없는 수집, 양단 비교, pcap 보호 통제로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 장애 대응 시 client, server, firewall 전후에 동시 캡처를 배치하고 NTP 동기화와 BPF filter를 먼저 확인함
2. TCP 문제는 SYN/SYN-ACK/ACK, retransmission, RST source, window size를 표준 체크리스트로 분석함
3. pcap 파일은 개인정보 포함 여부를 점검하고 암호화 저장, 접근 로그, 보관 기간을 운영 절차에 포함함

**결론 (2줄):**
- 기술사 판단: 로그로 원인이 분리되지 않는 지연·손실·reset 문제는 패킷 캡처를 통해 wire-level 증거를 확보함
- 향후 방향: NDR, eBPF flow telemetry, packet broker와 연계해 상시 관측과 사건별 pcap 보존을 병행해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "패킷 분석을 설명하시오" | 캡처, 필터, 디코딩 흐름 | 로그 분석과 패킷 분석 차이 |
| 요구사항 명시형 | "장애 분석 방안을 제시하시오" | 양단 캡처, TCP/DNS/TLS 필드 | 캡처 손실·정보 유출 대응 |

> 요약: 설명형은 분석 절차, 방안형은 증거 수집 위치와 보안 통제 중심으로 전환한다.
