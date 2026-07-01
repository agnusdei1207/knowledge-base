---
title: "TCP 혼잡 제어 — AIMD·Slow Start (TCP Congestion Control)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 29
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP 혼잡 제어를 처음 봐도 cwnd가 왜 천천히 또는 급격히 변하고 AIMD가 왜 필요한지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TCP 송신자가 네트워크 경로의 혼잡 상태를 추정해 전송량(cwnd)을 조절하는 알고리즘
- **왜 필요한가**: 여러 송신자가 동시에 패킷을 밀어 넣으면 라우터 큐가 넘치고 packet loss와 RTO가 발생한다. 혼잡 제어는 네트워크 경로가 처리 가능한 수준으로 전송량을 조정한다.
- **핵심 직관**: 도로에 차를 조금씩 늘려 보내다가 정체 신호가 보이면 차로 투입량을 줄이는 방식이다.

## 깊이 이해
- **배경·문제의식**: 흐름 제어가 수신자 버퍼를 보호한다면 혼잡 제어는 네트워크 경로를 보호한다. TCP는 명시적 대역폭 예약 없이 loss, duplicate ACK, RTT 증가를 보고 혼잡을 추정한다.
- **작동 원리**: Slow Start는 cwnd를 ACK마다 증가시켜 RTT마다 대략 2배로 키운다. ssthresh에 도달하면 Congestion Avoidance로 전환하고 AIMD에 따라 additive increase, multiplicative decrease를 수행한다. loss가 발생하면 cwnd를 줄이고 재전송한다.
- **비유**: 처음 가는 도로에서 차를 1대, 2대, 4대씩 보내며 수용량을 찾다가 막히면 절반으로 줄이고 다시 조금씩 늘리는 과정이다.
- **구체 예시**: cwnd가 1 MSS에서 시작해 RTT마다 2, 4, 8, 16 MSS로 증가하다가 loss가 발생하면 ssthresh를 8 MSS로 낮추고 cwnd를 조정한다.
- **흔한 오해·주의점**: 혼잡 제어는 수신자 window만 키운다고 해결되지 않는다. 실제 송신량은 `min(rwnd, cwnd)`이고, loss·RTT·RTO가 cwnd를 제한한다.

## 연결 개념
- TCP 흐름 제어 — rwnd로 수신 버퍼를 보호
- RTO·재전송 — loss 감지와 복구 지표
- BBR·CUBIC — 현대 TCP 혼잡 제어 알고리즘

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TCP 혼잡 제어 답안은 cwnd, ssthresh, Slow Start, AIMD, Fast Retransmit, RTO를 상태 전이와 지표로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 혼잡 제어는 packet loss와 ACK 패턴을 근거로 congestion window(cwnd)를 조절해 네트워크 경로 혼잡을 완화하는 기능이다.
> 2. **가치**: 송신자가 경로 수용량을 탐색하고 loss 발생 시 전송량을 줄여 라우터 큐 overflow와 재전송 폭증을 억제한다.
> 3. **판단 포인트**: Slow Start는 지수 증가, AIMD는 선형 증가·곱셈 감소, 실제 전송량은 `min(rwnd, cwnd)`이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 혼잡 제어 원리 확인 | cwnd, ssthresh, Slow Start, AIMD | 흐름 제어 rwnd와 혼동 |
| loss 복구 이해 확인 | duplicate ACK, Fast Retransmit, RTO | loss 발생 후 cwnd 변화 누락 |
| 성능 분석 역량 확인 | RTT, packet loss, throughput, BDP | 대역폭만 보고 판단 |

> 요약: 이 문제는 cwnd 변화와 loss 대응을 상태 전이로 설명하고 흐름 제어와 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

TCP 혼잡 제어는 네트워크 경로의 혼잡을 추정해 송신량을 조절하는 기능이다. 송신자는 cwnd와 ssthresh를 사용해 Slow Start, Congestion Avoidance, Fast Recovery를 수행한다. 혼잡 제어는 packet loss, RTO, RTT 증가가 발생하는 WAN·인터넷 서비스에서 핵심 성능 요인이다.

---

## Ⅱ. 구조 및 구성요소

```text
Sender -> cwnd Control
  / Slow Start
  / Congestion Avoidance
  / Fast Retransmit
  / Fast Recovery
Network Path -> ACK/Loss/RTT Signal -> cwnd Update
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| cwnd | 네트워크 기준 송신 허용량 | sender 내부 변수 |
| ssthresh | Slow Start와 회피 구간 경계 | loss 시 조정 |
| ACK/Dup ACK | 전송 성공과 손실 신호 | 3 duplicate ACK 기준 |
| RTO | ACK 미수신 timeout | 재전송과 cwnd 감소 |
| MSS | cwnd 증가 단위 | TCP option으로 협상 |

> 요약: 혼잡 제어는 cwnd, ssthresh, ACK/loss 신호, RTO, MSS를 이용해 송신량을 조절한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Connection Start -> Slow Start cwnd Exponential Increase
  -> ssthresh Reach -> Congestion Avoidance AIMD
  -> Loss Detect -> cwnd Reduce
  -> Retransmit -> Recovery
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 초기 cwnd에서 Slow Start 시작 | cwnd per RTT 증가 |
| 2 | ACK 수신마다 cwnd 증가, ssthresh까지 탐색 | throughput ramp-up |
| 3 | Congestion Avoidance에서 additive increase | cwnd linear growth |
| 4 | loss 또는 RTO 발생 시 multiplicative decrease | packet loss, RTO count |
| 5 | Fast Retransmit/Recovery로 손실 segment 복구 | duplicate ACK count |

> 요약: TCP는 Slow Start로 경로 용량을 탐색하고, AIMD로 혼잡 발생 시 cwnd를 줄인 뒤 회복한다.

---

## Ⅳ. 특징

| 구분 | Slow Start | AIMD/Congestion Avoidance | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 증가 방식 | RTT마다 cwnd 대략 2배 | RTT마다 선형 증가 | cwnd, MSS |
| 적용 시점 | 연결 시작, timeout 후 | ssthresh 이후 | ssthresh |
| 손실 대응 | timeout 시 cwnd 초기화 가능 | loss 시 cwnd 감소 | RTO, dup ACK |
| 장점·한계 | ramp-up 시간 단축 | 공정성 확보 | long fat network BDP |

> 요약: Slow Start는 초기 탐색, AIMD는 공정한 장기 전송을 위한 cwnd 조절 방식이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Reno/NewReno | CUBIC/BBR | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | loss 기반 AIMD | CUBIC은 cubic 함수, BBR은 bandwidth/RTT 추정 | Linux 기본 CUBIC, 지연 민감 서비스는 BBR 검토 |
| 비용/성능 | loss로 혼잡 판단 | 고 BDP 경로에서 throughput 확보 | RTT, loss, fairness 기준 |
| 운영/위험 | high loss 환경에서 throughput 감소 | BBR 공정성 논쟁, bufferbloat | A/B test와 SLO 측정 |

> 요약: 알고리즘 선택은 OS 기본값보다 RTT, packet loss, fairness, SLO 측정 결과로 판단해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Throughput 저하 | loss와 RTO로 cwnd 감소 | 경로 품질 개선, ECN, CUBIC/BBR 검토 | packet loss rate, cwnd |
| Bufferbloat | 큐 과다로 RTT 증가 | AQM, CoDel, pacing | RTT p95, queue delay |
| 공정성 문제 | 알고리즘 혼재 | per-flow limit, QoS | flow throughput variance |

> 요약: 혼잡 제어 리스크는 loss, 큐 지연, 알고리즘 공정성으로 나누어 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 손실률 | packet loss 0.1% 이하 목표 | pcap, NetFlow, synthetic test |
| 지연 | RTT p95 기준선 유지 | ping, TCP timestamp, APM |
| 전송량 | BDP 대비 throughput 목표 충족 | iperf, OS tcp_info |

> 요약: 혼잡 제어 성과는 packet loss, RTT p95, BDP 대비 throughput으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. WAN 전송 성능 분석 시 OS `tcp_info`, pcap, iperf로 cwnd, RTT, retransmission, RTO를 함께 수집함
2. 고 RTT·고 대역폭 구간은 BDP를 계산하고 CUBIC, BBR, pacing, ECN 적용 효과를 A/B test로 검증함
3. packet loss가 있는 회선은 QoS, AQM, 회선 오류율, duplex mismatch를 점검하고 애플리케이션 retry와 구분함

**결론 (2줄):**
- 기술사 판단: rwnd가 충분해도 cwnd가 작으면 혼잡 제어가 병목이며 loss·RTT·RTO를 우선 확인함
- 향후 방향: QUIC, BBR, ECN, AQM 기반으로 손실 중심 제어에서 지연·대역폭 추정 중심 제어로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP 혼잡 제어를 설명하시오" | Slow Start, AIMD, loss 복구 흐름 | 흐름 제어와 혼잡 제어 차이 |
| 요구사항 명시형 | "WAN 성능 개선 방안을 제시하시오" | cwnd, RTT, RTO, BDP 분석 | CUBIC/BBR, AQM, ECN 적용 기준 |

> 요약: 설명형은 cwnd 변화, 방안형은 손실·지연 지표와 알고리즘 선택 기준 중심으로 전환한다.
