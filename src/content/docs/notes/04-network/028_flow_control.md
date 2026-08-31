---
sidebar:
  order: 28
  label: "028. TCP 흐름•혼잡 제어"
  badge:
    text: "기출 · 50%"
    variant: note
title: "TCP 흐름•혼잡 제어 (Flow & Congestion Control)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 28
extra:
  question_no: "28"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "수신단 흐름 제어(rwnd)와 망 내부 혼잡 제어(cwnd) 통합 메커니즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Flow Control (흐름 제어)**: 수신 호스트의 소켓 버퍼 오버플로우를 막기 위해 수신 윈도우(rwnd) 크기 이하로 송신량을 조절하는 종단 간 제어.
- **Congestion Control (혼잡 제어)**: 중간 네트워크 라우터 큐 포화 및 패킷 드롭(혼잡 붕괴)을 방지하기 위해 송신자가 혼잡 윈도우(cwnd)를 동적 조절하는 제어.

</details>

- 정의/개념: **rwnd와 cwnd의 최솟값**으로 전송량을 정하는 TCP 이중 제어 체계
- 배경/필요성: 송수신 종단 호스트 간의 처리 속도 차이로 인한 수신 소켓 버퍼 오버플로우와, 네트워크 중간 라우터/스위치 큐의 용량 초과로 인해 발생하는 대규모 패킷 드롭 및 재전송 폭풍에 의한 전송 효율 급감(혼잡 붕괴: Congestion Collapse)을 동시에 방어하기 위해, 수신 측 가용 버퍼 크기(rwnd)와 송신 측이 네트워크 상태를 기반으로 연산하는 혼잡 윈도우(cwnd) 중 최솟값($\min(\text{rwnd}, \text{cwnd})$)을 유효 전송 윈도우로 채택하는 TCP 이중 전송 제어 체계를 도입하여 **종단 버퍼 무손실 보장과 네트워크 전체의 공평한 대역폭 공유 및 처리량 극대화**를 달성할 필요

#### 한줄 요약
- 수신자 버퍼(rwnd)와 망 혼잡(cwnd)의 최솟값을 취해 오버플로우와 혼잡 붕괴를 동시에 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Slow Start & Congestion Avoidance**: cwnd를 지수 함수로 증가시켜 가용 대역폭을 탐색하다가 임계치(ssthresh) 도달 후 선형(AIMD)으로 완만하게 증가시키는 알고리즘.
- **Fast Retransmit & Fast Recovery**: 3 중복 ACK 수신 시 RTO 만료 전 손실 패킷을 즉시 재전송하고 cwnd를 절반으로 줄여 세션을 유지하는 기법.

</details>

- 수신자 여유(rwnd)와 망 상태(cwnd) 중 **최솟값인 $\min(\text{rwnd}, \text{cwnd})$을 유효 윈도우로 적용**
- **흐름 제어**: 수신 측의 피드백(ACK 헤더 내 Window 필드)에 의해 수동적으로 상한 결정
- **혼잡 제어**: Slow Start, Congestion Avoidance, Fast Retransmit/Recovery를 통해 송신 측이 능동 조절

#### 한줄 요약
- $\min(\text{rwnd}, \text{cwnd})$ 유효 윈도우와 4단계 혼잡 제어(Slow Start/AIMD/Fast Retransmit/Fast Recovery)를 결합한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ECN (Explicit Congestion Notification)**: 라우터가 버퍼 혼잡 감지 시 패킷을 드롭하지 않고 IP 헤더의 ECN 비트를 마킹하여 종단에 혼잡을 통보하는 기술 (RFC 3168).

</details>

```text
[TCP 송신단 이중 전송 제어(rwnd / cwnd) 아키텍처]
|-- 흐름 제어 (rwnd 관리)
|-- 혼잡 제어 (cwnd·ssthresh 관리)
|-- 유효 전송 윈도우 (최솟값 산출)
`-- ECN 마킹 엔진 (혼잡 조기 통보)
```

선의 의미: 계층 및 송신단이 rwnd와 cwnd를 계산하여 유효 윈도우로 패킷을 송출하고 수신단이 rwnd를 피드백하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 흐름 제어 | 수신자가 통보한 **rwnd 준수** |
| 혼잡 제어 | 경로 상태에 따라 **cwnd 동적 조절** |
| 유효 전송 윈도우 | **rwnd·cwnd 최솟값 산출** |
| ECN 마킹 엔진 | 드롭 전 **혼잡 조기 통보** |

#### 한줄 요약
- rwnd가 수신 버퍼를, cwnd가 망의 큐를 각각 지키고 송신단은 둘 중 작은 쪽만 따르므로, 어느 병목이 먼저 걸리든 같은 윈도우 계산 하나가 대신 막아 준다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AIMD (Additive Increase Multiplicative Decrease)**: 손실이 없을 때는 선형 증가(+1 MSS/RTT), 혼잡 발생 시 절반 곱셈 감소(/2)를 수행하는 공평성 알고리즘.

</details>

```text
TCP 이중 전송 제어 파이프라인
        │
   [유효 윈도우 계산] $\min(\text{rwnd}, \text{cwnd})$ 산출 후 패킷 연속 송출
        │
   [수신단 피드백 수신] 새로운 rwnd 및 ECN 신호 / ACK 수신
   ┌────┴───────────────────────────┐
  정상 수신 (ACK 연속 도착)       패킷 손실 또는 ECN 신호 감지
   │                                 │
   ├─ cwnd < ssthresh (Slow Start)      [혼잡 회피 발동]
   │  • RTT마다 cwnd 2배 지수 증가       • ssthresh = cwnd / 2 설정
   │                                 • 3 Dup ACK: Fast Retransmit & Recovery
   └─ cwnd >= ssthresh (혼잡 회피)   • RTO Timeout: cwnd = 1 초기화
      • RTT마다 1 MSS 선형 증가
        │                                 │
        └────────────────┬────────────────┘
                         ▼
   안정적인 종단 간 처리량 및 네트워크 공평성 유지
```

#### 한줄 요약
- 손실을 혼잡 신호로 삼는 갈래는 패킷 하나를 잃고서야 cwnd를 접지만, ECN 갈래는 드롭 이전에 통보를 받아 재전송 비용 없이 같은 감속을 얻는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Bufferbloat (버퍼블로트)**: 대용량 라우터 큐에서 패킷을 과도하게 쌓아두어 손실은 없으나 왕복 지연(RTT)이 수 초 이상 폭증하는 현상.

</details>

| 비교 항목 | 흐름 제어 (Flow Control) | 혼잡 제어 (Congestion Control) |
|:---|:---|:---|
| 해결 문제 영역 | **송수신 종단 호스트 간의 처리 속도 불일치** | **네트워크 경로 상 라우터/스위치 큐 용량 초과** |
| 핵심 제어 파라미터 | **rwnd** (수신자가 TCP 헤더 Window로 통보) | **cwnd, ssthresh** (송신단 내부 연산) |
| 통제 메커니즘 | **슬라이딩 윈도우, Window Scale, 지속 타이머**| **Slow Start, AIMD, Fast Retransmit / Recovery**|
| 병목 발생 시 현상 | **Zero Window (rwnd=0)로 송신 전면 중단** | **패킷 드롭 손실, RTO 만료, RTT 지연 폭증** |

#### 한줄 요약
- 흐름 제어는 종단 간 버퍼 상태를 제어하고, 혼잡 제어는 경로 상 라우터 큐 상태를 제어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BBR (Bottleneck Bandwidth and RTT)**: 패킷 손실 대신 실제 대역폭과 최소 RTT를 측정하여 버퍼블로트 없이 최대 처리량을 달성하는 혼잡 제어 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수신 애플리케이션 지연으로 인한 지속적 Zero Window(rwnd=0) 발생 | **비동기 넌블로킹 I/O 도입 및 소켓 수신 버퍼(`SO_RCVBUF`) 확장** | 수신 버퍼 고갈 방지 및 지속 타이머 교착 해소 |
| 무선망의 일시적 비트 오류 손실을 망 혼잡으로 오인해 cwnd 급감 | **손실 기반 대신 대역폭/지연 모델링 기반 `BBR 알고리즘` 적용** | 무선 패킷 유실 환경에서도 대역폭 100% 유지 |
| 라우터 큐 과도 점유로 인해 패킷 지연이 폭증하는 **버퍼블로트** | **네트워크 장비에 `능동 큐 관리(AQM: FQ-CoDel)` 및 ECN 활성화** | 큐 대기 시간 최소화 및 RTT 획기적 개선 |
| CUBIC 알고리즘의 급격한 cwnd 감소로 인한 링크 활용률 저하 | **리눅스 커널 `TCP CUBIC / BBRv2` 튜닝 및 하이브리드 적용** | 대규모 데이터센터 간 전송 처리량 극대화 |

#### 한줄 요약
- SO_RCVBUF 확장, BBR 혼잡 제어, AQM/ECN 활성화, BBRv2 커널 튜닝으로 운영한다.

## Ⅶ. 결론

- 글로벌 인터넷의 안정적인 동작과 통신 품질(QoS)을 지탱하는 **가장 핵심적이고 정교한 종단 간/네트워크 전송 제어 아키텍처**로 확립되었으며, 최근에는 단순 손실 기반(Loss-based: Reno/CUBIC)의 한계인 버퍼블로트(Bufferbloat) 문제를 극복하기 위해 실제 대역폭과 최소 RTT를 모델링하는 **Google BBR(Bottleneck Bandwidth and RTT) 및 ECN/AQM(FQ-CoDel) 기반 모델 기반 혼잡 제어로 진화함과 동시에, 실무 운영 시에는 rwnd 소켓 버퍼 오토튜닝과 BBR 알고리즘 결합**을 통해 고지연·대용량 링크의 전송 성능을 완성

#### 한줄 요약
- TCP 흐름·혼잡 제어는 $\min(\text{rwnd}, \text{cwnd})$을 통해 수신 버퍼와 망 큐를 이중 보호하며, BBR과 AQM을 결합하여 버퍼블로트를 극복하는 핵심 전송 기술이다.
