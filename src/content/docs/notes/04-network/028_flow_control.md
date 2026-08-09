---
sidebar:
  order: 28
  label: "028. TCP 흐름•혼잡 제어 : 슬라이딩 윈도우•Slow Start"
  badge:
    text: "기출 • 50%"
    variant: note
title: "TCP 흐름•혼잡 제어 : 슬라이딩 윈도우•Slow Start"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 28
extra:
  question_no: "028"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "비교•설명형: 흐름•혼잡 제어 통합 판단축"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **흐름 제어(Flow Control)**: 송신량이 수신 처리 능력을 넘지 않도록 제한하는 기능이다.
- **혼잡 제어(Congestion Control)**: 송신량이 네트워크 경로 수용량을 넘지 않도록 제한하는 기능이다.
- **전송 제어 프로토콜(Transmission Control Protocol, TCP)**: 수신 상태와 경로 혼잡을 함께 반영해 신뢰성 있는 바이트 스트림을 전달하는 프로토콜이다.
</details>

- 정의/개념: **TCP**는 **흐름 제어**의 rwnd와 **혼잡 제어**의 cwnd 중 작은 값으로 전송량을 제한한다.
- 배경/필요성: 과도한 송신량은 수신 버퍼 초과와 경로 혼잡을 일으킨다.

#### 한줄 요약

- TCP는 수신 측 rwnd와 경로 혼잡 cwnd 중 작은 값을 실제 윈도로 적용하여 송신량을 제한한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **수신 윈도(Receive Window, rwnd)**: 수신 버퍼 여유를 나타내는 미확인 전송 한도이다.
- **혼잡 윈도(Congestion Window, cwnd)**: 경로 혼잡 상태를 반영한 미확인 전송 한도이다.
- **실제 윈도(Effective Window)**: rwnd와 cwnd 중 작은 실제 송신 한도이다.
- **확인 응답(Acknowledgment, ACK)**: 누적 수신 번호와 수신 상태를 알리는 응답이다.
- **느린 시작 임계값(Slow Start Threshold, ssthresh)**: 혼잡 윈도 증가 방식을 전환하는 기준값이다.
</details>

![수신 윈도와 혼잡 윈도 중 작은 값으로 제한되는 송신 가능량](/study/diagrams/tcp-effective-window.svg)

> 수신 윈도를 64KiB로 고정한 예시에서 초록 실제 송신 한도는 cwnd가 더 작을 때 함께 증가하지만 64KiB 이후에는 rwnd에 막히며, 실제 값은 연결의 ACK와 혼잡 신호에 따라 계속 변한다.

- **rwnd**는 수신 버퍼 여유를 광고한다.
- **cwnd**는 네트워크 혼잡 한도를 추정한다.
- **실제 윈도**는 rwnd와 cwnd 중 작은 송신 한도이다.

#### 한줄 요약

- 느린 시작 단계에서는 ACK마다 cwnd를 지수적으로 증가시키고, ssthresh 도달 후 혼잡 회피 단계에서는 RTT당 선형적으로 증가시킨다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **슬라이딩 윈도(Sliding Window)**: 여러 데이터를 연속 전송하고 ACK에 따라 범위를 이동하는 방식이다.
- **명시적 혼잡 알림(Explicit Congestion Notification, ECN)**: 패킷 폐기 없이 종단에 혼잡을 알리는 기능이다.
</details>

```text
송신 TCP
├── 송신 버퍼
├── 혼잡 제어기
└── 수신 TCP
    └── 수신 버퍼
```

선의 의미: 송신 TCP는 송신 버퍼와 혼잡 제어기를 소유하고 수신 TCP와 연결되며, 수신 TCP는 수신 버퍼의 여유를 관리하는 정적 TCP 종단 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 송신 TCP | **rwnd**•**cwnd** 중 작은 값으로 전송 범위 제한 |
| 송신 버퍼 | **슬라이딩 윈도**의 미확인 데이터 보관 |
| 혼잡 제어기 | ACK•손실•**ECN**으로 cwnd 조정 |
| 수신 TCP | **ACK**에 현재 rwnd 광고 |
| 수신 버퍼 | 응용이 읽기 전 수신 데이터 보관 |

#### 한줄 요약

- 송신 TCP는 수신 측이 광고한 rwnd와 혼잡 제어기가 산출한 cwnd 중 작은 값을 실제 윈도로 적용한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **느린 시작(Slow Start)**: cwnd를 빠르게 늘려 경로 수용량을 탐색하는 알고리즘이다.
- **윈도 제한 데이터**: rwnd와 cwnd 중 작은 실제 윈도 안에서 연속 전송하는 데이터이다.
- **ACK•rwnd**: 누적 수신 번호와 현재 수신 버퍼 여유를 회신하는 응답 정보이다.
- **ACK•혼잡 신호**: ACK•손실•ECN으로 경로 수용량 변화를 알리는 정보이다.
- **cwnd 갱신**: 혼잡 신호와 ssthresh를 반영해 혼잡 윈도를 조정하는 절차이다.
</details>

```text
전송 데이터
    |
    `-- 실제 윈도 = min(rwnd, cwnd)
                 |
                 v
        1. 윈도 제한 데이터
                 |
                 v
           2. ACK•rwnd
                 |
                 v
       3. ACK•혼잡 신호
                 |
                 +-- 손실•ECN ---- cwnd 축소•임계값 갱신
                 |
                 +-- ACK
                 |    +-- cwnd < ssthresh ---- 느린 시작
                 |    `-- cwnd >= ssthresh --- 혼잡 회피
                 |
                 `-- 제어 결과
                              |
                              v
                        4. cwnd 갱신
                              |
                              `-- 남은 데이터 반복
```

### 동작 원리

1. **윈도 제한 데이터**: **rwnd•cwnd** 중 작은 범위까지만 연속을 전송한다.
2. **ACK•rwnd**: 누적 수신 번호와 수신 버퍼 여유를 회신한다.
3. **ACK•혼잡 신호**: ACK•손실•ECN을 경로 수용량 근거로 전달한다.
4. **cwnd 갱신**: **느린 시작**•혼잡 회피 결과로 혼잡 윈도를 갱신한다.

#### 한줄 요약

- 수신 TCP가 rwnd를 광고하고 혼잡 제어기가 ACK·손실·ECN으로 cwnd를 갱신하면 송신 TCP가 min(rwnd, cwnd) 범위까지 데이터를 전송한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **수신자 병목(Receiver Bottleneck)**: rwnd가 작아 수신 처리 능력이 전송량을 제한하는 상태이다.
- **네트워크 병목(Network Bottleneck)**: cwnd가 작아 경로 수용량이 전송량을 제한하는 상태이다.
</details>

| 전송량 제어 | **네트워크 병목** 대응 | **수신자 병목** 대응 |
|:---|:---|:---|
| 적용 기준 | 경로 수용량 탐색•혼잡 대응 | 수신 버퍼 오버플로 방지 |
| 핵심 특징 | cwnd를 ssthresh까지 늘린 뒤 혼잡 시 축소 | rwnd 안의 연속 전송 |
| 한계 | 경로 큐•손실 증가 | 응용 지연•버퍼 부족 |

> 요약: rwnd는 수신, cwnd는 경로 보호가 핵심이다.

#### 한줄 요약

- rwnd가 작으면 수신 측을 보고 cwnd가 작으면 네트워크 경로의 손실•혼잡 신호를 본다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **대역폭-지연 곱(Bandwidth-Delay Product, BDP)**: 경로에 동시에 채울 수 있는 데이터량이다.
- **왕복 시간(Round-Trip Time, RTT)**: 데이터 전송부터 ACK 수신까지 걸리는 시간이다.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| rwnd•cwnd 감소 원인을 혼동 | 수신 버퍼와 경로 혼잡 신호 분리 관측 | 흐름•혼잡 병목 구분 |
| rwnd 0 광고로 제로 윈도 지속 | 수신 응용 소비율•윈도 갱신 점검 | 송신 측 영구 대기 방지 |
| 버퍼가 **BDP**보다 커 큐 지연 증가 | BDP에 맞춰 버퍼•윈도 설정 | 과도한 버퍼 지연 완화 |
| 무선 손실을 경로 혼잡으로 오판 | **ECN**•**RTT**•재전송 함께 분석 | 불필요한 cwnd 축소 방지 |

#### 한줄 요약

- rwnd가 0이면 경로보다 수신 응용의 소비율을 먼저 점검하고, cwnd가 작으면 경로 혼잡·손실 원인을 분석한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **제로 윈도**: 수신 버퍼가 가득 차 추가 수신 가능량을 0으로 알린 상태이다.
</details>

- **제로 윈도**이면 **흐름 제어**를, cwnd가 작으면 **혼잡 제어**를 우선 조정한다.

#### 한줄 요약

- rwnd가 작으면 수신 버퍼·응용 소비율을 개선하고, cwnd가 작으면 혼잡 제어 파라미터를 조정하여 실제 병목부터 해소한다.
