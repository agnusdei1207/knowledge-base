---
title: "흐름 제어 — Slow Start·슬라이딩 윈도우 (Flow Control)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 34
---

# 📖 【암기용】 개념 완전 이해

> 목적: 흐름 제어와 혼잡 제어가 섞여 나올 때 슬라이딩 윈도우와 Slow Start의 역할을 구분하게 만든다. 시험 답안 양식이 아니라, 수신자 보호와 네트워크 보호의 차이를 이해하기 위한 설명이다.

## 한눈에
- **개요**: 흐름 제어는 송신량을 수신자 처리 능력에 맞추는 전송 제어
- **왜 필요한가**: 송신자가 수신 버퍼보다 많은 데이터를 보내면 receive buffer overflow와 재전송이 발생함.
- **핵심 직관**: 슬라이딩 윈도우는 수신자가 "지금 몇 바이트까지 받을 수 있다"고 알려주는 신용 한도이고, Slow Start는 네트워크 혼잡을 탐색하는 출발 규칙임.

## 깊이 이해
- **배경·문제의식**: TCP는 신뢰성뿐 아니라 송신 속도 조절이 필요함. 수신자 한계는 receive window(rwnd), 네트워크 한계는 congestion window(cwnd)가 나타냄.
- **작동 원리**: 실제 송신 가능량은 `min(rwnd, cwnd)`임. 슬라이딩 윈도우는 ACK 수신에 따라 창을 이동하고, Slow Start는 cwnd를 ACK마다 증가시켜 ssthresh까지 지수적으로 확대함.
- **비유**: 식당 주방(rwnd)이 받을 수 있는 주문량과 도로(cwnd)가 감당할 배달량 중 작은 값만큼만 주문을 보냄.
- **구체 예시**: rwnd 64KB, cwnd 16KB이면 송신자는 16KB만 보냄. ACK가 도착하면 window가 이동하고 cwnd가 증가함.
- **흔한 오해·주의점**: Slow Start는 이름과 달리 초기 cwnd가 ACK마다 증가하는 탐색 단계임. 흐름 제어(rwnd)와 혼잡 제어(cwnd)를 구분해야 함.

## 연결 개념
- TCP Flow Control: receive window와 zero window probe
- TCP Congestion Control: Slow Start, AIMD, congestion avoidance
- ARQ Error Control: ACK 기반 재전송과 window 동작 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 흐름 제어 문제는 rwnd와 cwnd를 구분하고, 실제 송신량 `min(rwnd, cwnd)`와 운영 지표까지 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 흐름 제어는 수신 버퍼 보호를 위해 슬라이딩 윈도우와 receive window로 송신량을 제한하는 TCP 제어 기능이다.
> 2. **가치**: Slow Start와 cwnd는 네트워크 혼잡 탐색이고, rwnd는 수신자 처리 능력 제약이므로 원인과 조치가 다르다.
> 3. **판단 포인트**: 송신 가능량은 `min(rwnd, cwnd)`이며, zero window, retransmission, RTT, BDP를 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TCP 제어 기능 구분 확인 | flow control(rwnd) vs congestion control(cwnd) | Slow Start를 흐름 제어만으로 설명 |
| 슬라이딩 윈도우 원리 확인 | ACK 기반 window 이동, advertised window | window size와 sequence number 누락 |
| 운영 장애 분석 역량 확인 | zero window, buffer pressure, BDP | 네트워크 대역폭만 원인으로 단정 |

> 요약: 이 문제는 수신자 보호와 네트워크 혼잡 탐색을 분리해 원인별 지표와 대응을 쓰는 문제임.

---

## Ⅰ. 개요 및 필요성

- 개요: 송신량을 수신자 처리 능력에 맞추는 TCP 전송 제어
- 배경: 슬라이딩 윈도우와 receive window(rwnd)로 수신 버퍼 overflow를 방지함
- 필요성: 실제 송신 가능량은 수신 윈도우(rwnd)와 혼잡 윈도우(cwnd) 중 작은 값 `min(rwnd, cwnd)`으로 제한됨

---

## Ⅱ. 구조 및 구성요소

```text
Sender Buffer -> Send Window -> Network -> Receive Window -> Receiver Buffer
                        / cwnd
                        / rwnd
                        / ACK Window Update
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 송신 윈도우 | ACK 없이 보낼 수 있는 바이트 범위 | `min(rwnd, cwnd)` 적용 |
| 수신 윈도우(rwnd) | 수신자가 광고하는 남은 버퍼 | TCP header window field |
| 혼잡 윈도우(cwnd) | 네트워크 혼잡 상태 기반 제한 | Slow Start, AIMD |
| ACK | 수신 확인과 window update 전달 | delayed ACK 영향 |

> 요약: TCP 송신량은 수신자 버퍼(rwnd)와 네트워크 혼잡(cwnd)의 동시 제약으로 결정됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
데이터 송신 -> ACK 수신 -> rwnd 확인 -> cwnd 확인
-> send window 계산 -> window slide -> timeout/zero window 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 연결 후 초기 rwnd와 cwnd 설정 | initial cwnd, MSS |
| 2 | 송신자는 window 범위 내 세그먼트 전송 | bytes in flight |
| 3 | 수신자는 ACK와 advertised window 전송 | rwnd, zero window |
| 4 | Slow Start는 ACK마다 cwnd 증가 | ssthresh, cwnd trace |
| 5 | 손실·timeout 시 cwnd 감소와 재전송 | retransmission, RTO |

> 요약: 슬라이딩 윈도우는 ACK로 창을 이동하고, Slow Start는 손실 전까지 cwnd를 확대해 전송 가능량을 탐색함.

---

## Ⅳ. 특징

| 구분 | 흐름 제어 | 혼잡 제어 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 보호 대상 | 수신자 버퍼 | 네트워크 경로 | rwnd vs cwnd |
| 대표 기법 | 슬라이딩 윈도우 | Slow Start, AIMD | TCP RFC 5681 계열 |
| 제어 신호 | advertised window | loss, RTT, ECN | zero window, duplicate ACK |
| 장애 징후 | receive queue full | packet loss, RTT 증가 | retransmission ratio |

> 요약: 흐름 제어는 수신자 상태, 혼잡 제어는 경로 상태를 기준으로 송신량을 제한함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 애플리케이션 처리 | 수신 앱 지연 | rwnd 축소·zero window | receive queue와 CPU 사용률 |
| 네트워크 혼잡 | 큐잉·손실 | cwnd 감소·Slow Start 재진입 | RTT 증가, loss 1% 초과 |
| 대역폭 활용 | 고정 buffer | BDP 기반 window 조정 | bandwidth x RTT |

> 요약: 전송 지연 원인은 rwnd 제한과 cwnd 제한을 분리해 BDP와 큐 지표로 판정해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| zero window 지속 | 수신 앱 처리 지연 | socket buffer 증설, consumer 처리량 개선 | zero window duration |
| 낮은 처리량 | window가 BDP보다 작음 | window scaling, buffer tuning | window utilization |
| 재전송 증가 | cwnd 과대·손실 | congestion control 조정, ECN | retransmission %, RTT |

> 요약: 흐름 제어 리스크는 수신 버퍼, BDP, 손실에 의해 발생하며 각각 다른 조치가 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| window 활용 | BDP 대비 80% 이상 | tcp_info, pcap |
| zero window | 세션 시간의 1% 이하 | OS TCP counter |
| 재전송 | retransmission 1% 이하 | APM, packet capture |

> 요약: TCP 전송 품질은 window 활용률, zero window 시간, 재전송률로 점검함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 대용량 전송: BDP 기준으로 send/receive buffer와 window scaling을 조정하고 `tcp_info`로 cwnd·rwnd를 수집
2. API 서버: receive queue, application read rate, zero window duration을 함께 모니터링해 수신 병목을 분리
3. 손실 경로: retransmission 1% 초과 시 ECN, QoS, congestion control 알고리즘(CUBIC/BBR) 적용 조건 검토

**결론 (2줄):**
- 기술사 판단: rwnd 제한이면 애플리케이션·버퍼 조정, cwnd 제한이면 네트워크 손실·RTT 제어를 우선함
- 향후 방향: BBR, ECN, QUIC flow control처럼 RTT·대역폭 추정 기반 제어가 고속망 운영의 기준이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "흐름 제어를 설명하시오" | sliding window와 ACK update 흐름 | rwnd, cwnd, Slow Start 구분 |
| 요구사항 명시형 | "전송 지연 원인과 방안을 제시하시오" | zero window·loss·RTT 분석 절차 | BDP, buffer, congestion 대응 |

> 요약: 설명형은 TCP 제어 구조, 방안형은 rwnd/cwnd 병목 진단과 튜닝 중심으로 전환함.
