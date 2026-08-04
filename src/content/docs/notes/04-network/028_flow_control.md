---
sidebar:
  order: 28
  label: "028. TCP 흐름•혼잡 제어 : 슬라이딩 윈도우•Slow Start"
  badge:
    text: "기출 • 50%"
    variant: note
title: "TCP 흐름•혼잡 제어 : 슬라이딩 윈도우•Slow Start"
date: "2026-08-04T15:52:00+09:00"
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

- 정의/개념: **TCP 전송량 제어** — 수신 흐름 제어의 `rwnd`와 네트워크 혼잡 제어의 `cwnd` 중 작은 값으로 미확인 전송량을 제한하는 **방식**
- 배경/필요성: 과도한 송신량으로 **수신 버퍼 초과•경로 혼잡** 발생

#### 한줄 요약

- 물통 입구와 통로 중 좁은 쪽에 맞춰 물을 흘리듯 TCP는 수신 버퍼와 네트워크 경로 중 작은 한도로 보낸다

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **rwnd(Receive Window)**: 수신 버퍼 여유를 나타내는 미확인 전송 한도이다.
- **cwnd(Congestion Window)**: 경로 혼잡 상태를 반영한 미확인 전송 한도이다.
- **실제 윈도(Effective Window)**: rwnd와 cwnd 중 작은 실제 송신 한도이다.
- **ACK(Acknowledgment)**: 누적 수신 번호와 수신 상태를 알리는 응답이다.
- **ssthresh(Slow Start Threshold)**: 혼잡 윈도 증가 방식을 전환하는 기준값이다.
</details>

![수신 윈도와 혼잡 윈도 중 작은 값으로 제한되는 송신 가능량](/study/diagrams/tcp-effective-window.svg)

> 수신 윈도를 64KiB로 고정한 예시에서 초록 실제 송신 한도는 cwnd가 더 작을 때 함께 증가하지만 64KiB 이후에는 rwnd에 막히며, 실제 값은 연결의 ACK와 혼잡 신호에 따라 계속 변한다.

- rwnd의 **수신 버퍼 여유 광고**
- cwnd의 **네트워크 혼잡 한도 추정**
- `min(rwnd,cwnd)`의 **실제 송신 한도 결정**

#### 한줄 요약

- 좁은 길에서 차를 처음엔 빠르게 늘리다가 정체 징후 뒤 천천히 늘리듯 느린 시작은 cwnd를 ssthresh까지 키운 뒤 증가 폭을 줄인다

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **슬라이딩 윈도(Sliding Window)**: 여러 데이터를 연속 전송하고 ACK에 따라 범위를 이동하는 방식이다.
- **ECN(Explicit Congestion Notification)**: 패킷을 폐기하지 않고 종단에 혼잡을 알리는 기능이다.
</details>

```mermaid
block-beta
    columns 2
    A["송신 TCP"]
    B[("송신 버퍼")]
    C["혼잡 제어기"]
    D["수신 TCP"]
    E[("수신 버퍼")]
    A --- B
    A --- C
    A --- D
    D --- E
```

| 구성요소 | 책임 |
|:---|:---|
| 송신 TCP | **rwnd•cwnd** 중 작은 값으로 전송 범위 제한 |
| 송신 버퍼 | 미확인 데이터를 **재전송**까지 보관 |
| 혼잡 제어기 | ACK•손실•ECN으로 **cwnd** 조정 |
| 수신 TCP | ACK에 현재 **rwnd** 광고 |
| 수신 버퍼 | 응용이 읽기 전 **수신 데이터** 보관 |

#### 한줄 요약

- 송신 창구가 수신 창고의 빈자리와 도로 관제소의 통행량 중 작은 값을 택하듯 송신 TCP가 rwnd•cwnd를 함께 적용한다

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **느린 시작(Slow Start)**: cwnd를 빠르게 늘려 경로 수용량을 탐색하는 알고리즘이다.
</details>

```mermaid
sequenceDiagram
    participant 송신응용
    participant 송신TCP
    participant 혼잡제어기
    participant 수신TCP
    participant 수신응용
    송신응용->>송신TCP: 전송 데이터
    loop 전송 중
        송신TCP->>수신TCP: 1. 윈도 제한 데이터
        수신TCP-->>송신TCP: 2. ACK•rwnd
        송신TCP->>혼잡제어기: 3. ACK•혼잡 신호
        혼잡제어기-->>송신TCP: 4. cwnd
    end
    수신TCP-->>수신응용: 순서화 데이터
```

**동작 원리**

1. **윈도 제한 데이터**: **rwnd•cwnd** 중 작은 범위까지만 연속 전송
2. **ACK•rwnd**: 누적 수신 번호와 **수신 버퍼 여유** 회신
3. **ACK•혼잡 신호**: ACK•손실•ECN을 **경로 수용량** 근거로 전달
4. **cwnd**: 느린 시작•혼잡 회피 결과로 **혼잡 윈도** 갱신

#### 한줄 요약

- 수신 창고가 빈자리표 rwnd를 보내고 도로 관제기가 혼잡표 cwnd를 갱신하면 송신 창구가 작은 표만큼 상자를 보낸다

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **수신자 병목(Receiver Bottleneck)**: rwnd가 작아 수신 처리 능력이 전송량을 제한하는 상태이다.
- **네트워크 병목(Network Bottleneck)**: cwnd가 작아 경로 수용량이 전송량을 제한하는 상태이다.
</details>

| 전송량 제어 | 느린 시작 기반 혼잡 제어 | 슬라이딩 윈도 기반 흐름 제어 |
|:---|:---|:---|
| 적용 기준 | 경로 수용량 **탐색•혼잡 대응** | 수신 버퍼 **오버플로 방지** |
| 핵심 특징 | cwnd를 ssthresh까지 늘린 뒤 **혼잡 시 축소** | rwnd 안의 **연속 전송** |
| 한계 | 경로 큐•**손실 증가** | 응용 지연•**버퍼 부족** |

> 요약: rwnd는 수신, cwnd는 경로 보호

#### 한줄 요약

- rwnd가 작으면 수신 측을 보고 cwnd가 작으면 네트워크 경로의 손실•혼잡 신호를 본다

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **BDP(Bandwidth-delay Product)**: 경로에 동시에 채울 수 있는 데이터량이다.
- **RTT(Round-trip Time)**: 데이터 전송부터 ACK 수신까지 걸리는 왕복 시간이다.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| rwnd•cwnd 감소 원인을 혼동 | 수신 버퍼와 **경로 혼잡 신호** 분리 관측 | **흐름•혼잡 병목** 구분 |
| rwnd 0 광고로 **제로 윈도** 지속 | 수신 응용 소비율•**윈도 갱신** 점검 | 송신 측 **영구 대기** 방지 |
| 버퍼가 **BDP**보다 커 큐 지연 증가 | BDP에 맞춰 **버퍼•윈도** 설정 | 과도한 **버퍼 지연** 완화 |
| 무선 손실을 **경로 혼잡** 으로 오판 | **ECN•RTT•재전송** 함께 분석 | 불필요한 **cwnd 축소** 방지 |

#### 한줄 요약

- 창고 빈자리표가 0이면 도로를 넓히기보다 창고의 소비 속도를 먼저 보고, 정체표가 작으면 네트워크 경로를 점검한다

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **제로 윈도**: 수신 버퍼가 가득 차 추가 수신 가능량을 0으로 알린 상태이다.
</details>

- rwnd가 작으면 **흐름 제어**, cwnd가 작으면 **혼잡 제어** 우선 조정

#### 한줄 요약

- 창고 빈자리표가 작으면 수신 처리를 고치고 도로 정체표가 작으면 혼잡 제어를 조정해 더 좁은 병목부터 푼다
