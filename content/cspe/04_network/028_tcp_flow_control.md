---
title: "TCP 흐름 제어 — 슬라이딩 윈도우 (TCP Flow Control)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 28
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP 흐름 제어와 슬라이딩 윈도우를 처음 봐도 송신자가 왜 수신자 버퍼 크기를 보고 전송량을 조절하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TCP 수신자가 처리 가능한 버퍼 크기만큼 송신자가 미확인 데이터를 보내도록 제한하는 제어 방식
- **왜 필요한가**: 송신자가 수신 애플리케이션 처리 속도보다 많은 데이터를 보내면 receive buffer가 넘치고 packet drop, zero window, 재전송이 발생한다.
- **핵심 직관**: 물건을 받는 창고의 남은 공간만큼만 트럭을 보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: TCP는 네트워크 혼잡뿐 아니라 수신자의 처리 능력도 고려해야 한다. 수신자는 ACK에 advertised window(rwnd)를 실어 남은 버퍼 공간을 알려주고, 송신자는 그 범위 안에서 전송한다.
- **작동 원리**: 송신자는 `send window = min(rwnd, cwnd)` 범위까지 미확인 데이터를 보낼 수 있다. ACK가 오면 window가 오른쪽으로 이동하고 새로운 byte를 전송한다. 수신 버퍼가 0이면 zero window를 알리고, 송신자는 window probe로 재개 여부를 확인한다.
- **비유**: 식당 주방이 "현재 접시 20개만 받을 수 있음"이라고 말하면 홀 직원은 20개까지만 접시를 넘기고, 빈 접시가 생기면 추가로 보낸다.
- **구체 예시**: 수신자가 `rwnd=64KB`를 광고하고 congestion window가 `cwnd=128KB`이면 송신자는 64KB까지만 전송한다. 수신 애플리케이션이 데이터를 읽어 `rwnd=128KB`가 되면 window가 확장된다.
- **흔한 오해·주의점**: 흐름 제어는 혼잡 제어와 다르다. 흐름 제어는 수신자 버퍼 보호이고, 혼잡 제어는 네트워크 경로의 packet loss와 RTT 증가를 제어한다.

## 연결 개념
- TCP 혼잡 제어 — cwnd로 네트워크 혼잡을 통제
- TCP Window Scale — 65,535 byte를 넘는 window 광고 확장
- Zero Window — 수신 버퍼 부족으로 송신 중단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TCP 흐름 제어 답안은 rwnd, sliding window, ACK, zero window, window scale, cwnd와의 차이를 반드시 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP 흐름 제어는 수신자가 광고한 receive window(rwnd)에 맞춰 송신자의 미확인 데이터량을 제한하는 기능이다.
> 2. **가치**: 수신 버퍼 overflow와 애플리케이션 처리 지연으로 인한 drop·재전송을 줄이고 byte stream 순서를 유지한다.
> 3. **판단 포인트**: 실제 전송 가능량은 `min(rwnd, cwnd)`이며, rwnd는 수신자 보호, cwnd는 네트워크 혼잡 제어이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 흐름 제어 원리 확인 | rwnd, ACK, sliding window | 혼잡 제어와 동일 개념으로 서술 |
| TCP 필드 이해 확인 | window size, window scale option | 16bit window 한계 누락 |
| 장애 분석 역량 확인 | zero window, window probe, receive buffer | 지연 원인을 대역폭 부족으로만 판단 |

> 요약: 이 문제는 수신자 버퍼 보호 관점에서 window 광고와 송신 제한을 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

TCP 흐름 제어는 수신자가 처리 가능한 양만큼 송신자가 데이터를 보내도록 제한하는 기능이다. 수신자는 ACK의 window size로 남은 receive buffer를 광고한다. 송신자는 advertised window와 congestion window 중 작은 값만큼 전송해 수신 버퍼 overflow를 방지한다.

---

## Ⅱ. 구조 및 구성요소

```text
Sender Send Buffer -> Unacked Bytes
  -> Receiver ACK with rwnd
  -> Sliding Window Move
  -> Receiver App Read -> rwnd Update
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| rwnd | 수신자가 광고하는 남은 버퍼 크기 | TCP header window field |
| Send Window | 송신 가능한 byte 범위 | min(rwnd, cwnd) |
| ACK | 수신 확인과 window 광고 | cumulative ACK 기반 |
| Window Scale | window field 확장 | RFC 7323, 65,535 byte 초과 |
| Zero Window | 수신 버퍼 0 알림 | window probe로 재개 확인 |

> 요약: 흐름 제어는 rwnd 광고, ACK 수신, sliding window 이동, zero window 처리로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Data Send -> Receiver Buffer Fill
  -> ACK with rwnd -> Sender Limit Update
  -> App Read Buffer -> rwnd Increase
  -> Window Slide -> More Data Send
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 송신자가 send window 범위 내 byte 전송 | bytes in flight |
| 2 | 수신자가 데이터 저장 후 ACK와 rwnd 광고 | advertised window |
| 3 | 송신자가 ACK 기준으로 window를 오른쪽 이동 | unacked byte 감소 |
| 4 | rwnd 0이면 전송 중단 후 window probe 수행 | zero window duration |

> 요약: 슬라이딩 윈도우는 ACK가 도착할 때마다 전송 허용 범위를 이동시켜 수신 버퍼 범위 안에서 송신한다.

---

## Ⅳ. 특징

| 구분 | 흐름 제어 | 혼잡 제어 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 보호 대상 | 수신자 receive buffer | 네트워크 경로 | rwnd vs cwnd |
| 제어 정보 | ACK window size | loss, RTT, duplicate ACK | TCP header window |
| 제한 값 | advertised window | congestion window | send window=min(rwnd,cwnd) |
| 장애 신호 | zero window, small window | timeout, packet loss | window probe, RTO |

> 요약: 흐름 제어는 수신자 버퍼, 혼잡 제어는 네트워크 경로를 보호하므로 지표와 대응이 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 작은 window | 적정 window | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | receive buffer 부족, app read 지연 | BDP에 맞춘 buffer와 window scale | 고 RTT·고 대역폭 경로는 window scale 필요 |
| 비용/성능 | throughput 제한, zero window 증가 | 대역폭 활용률 증가 | BDP=bandwidth x RTT 기준 |
| 운영/위험 | small window syndrome | buffer memory 증가 | receive buffer와 app 처리량 균형 |

> 요약: window 크기는 BDP와 수신 애플리케이션 처리량을 함께 고려해 조정해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Zero Window | 수신 app read 지연, buffer 부족 | receive buffer 확대, app 병목 제거 | zero window count |
| Small Window Syndrome | 작은 단위 read/write 반복 | Nagle, delayed ACK, buffer 조정 | average segment size |
| Window Scale 미협상 | middlebox option drop | 경로 장비 점검, MSS/option 확인 | window scale option 존재 |

> 요약: 흐름 제어 리스크는 zero window, 작은 segment, option 협상 실패로 분류해 분석한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Window 상태 | zero window 지속 시간 기준선 이하 | pcap, TCP metric |
| 처리량 | BDP 대비 throughput 목표 충족 | iperf, APM |
| 버퍼 사용 | receive buffer 사용률 80% 이하 | OS socket metric |

> 요약: 흐름 제어 품질은 zero window, BDP 대비 처리량, receive buffer 사용률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 대용량 전송 구간은 RTT와 대역폭으로 BDP를 계산하고 TCP window scale과 socket buffer 크기를 조정함
2. zero window 발생 시 수신 애플리케이션 read 지연, GC pause, thread pool, receive buffer 사용률을 함께 점검함
3. pcap에서 advertised window, window scale option, bytes in flight를 확인해 rwnd 제한인지 cwnd 제한인지 분리함

**결론 (2줄):**
- 기술사 판단: rwnd가 작으면 수신자 병목, cwnd가 작으면 네트워크 혼잡 또는 손실 문제로 판단함
- 향후 방향: eBPF socket metric과 APM을 결합해 window 상태와 애플리케이션 처리 지연을 같은 시간축으로 분석해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP 흐름 제어를 설명하시오" | rwnd, ACK, sliding window 흐름 | 흐름 제어와 혼잡 제어 비교 |
| 요구사항 명시형 | "전송 지연 분석 방안을 제시하시오" | zero window, BDP, pcap 분석 | buffer, app read, window scale 지표 |

> 요약: 설명형은 rwnd 원리, 방안형은 zero window와 수신자 병목 분석 중심으로 전환한다.
