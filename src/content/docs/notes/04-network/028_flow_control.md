---
sidebar:
  order: 28
  label: "028. TCP 흐름•혼잡 제어"
  badge:
    text: "기출 · 50%"
    variant: note
title: "TCP 흐름•혼잡 제어 (Flow & Congestion Control)"
date: "2026-08-25T12:00:00+09:00"
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

- 정의/개념: 수신 버퍼 여유(**rwnd**)와 중간 네트워크 혼잡 상태(**cwnd**)를 모두 계측하여 **$\min(\text{rwnd}, \text{cwnd})$ 한도로 전송량을 제어하는 TCP 이중 전송 제어 체계**
- 배경/필요성: 수신 호스트 버퍼 오버플로우와 **네트워크 라우터 큐 포화에 따른 대규모 패킷 드롭 및 혼잡 붕괴(Congestion Collapse) 방어 불가**

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
|-- Sender TCP Engine
|   |-- Flow Control Module (수신단 ACK 패킷의 rwnd 수신)
|   |-- Congestion Control Module (네트워크 피드백 기반 cwnd / ssthresh 계산)
|   `-- Effective Window Calculator: Effective Window = $\min(\text{rwnd}, \text{cwnd})$
`-- Intermediate Network (Routers / Switches: ECN 비트 마킹 및 RED 큐잉)
`-- Receiver TCP Engine (소켓 수신 버퍼 가용 공간 측정 -> TCP ACK rwnd 회신)
```

선의 의미: 계층 및 송신단이 rwnd와 cwnd를 계산하여 유효 윈도우로 패킷을 송출하고 수신단이 rwnd를 피드백하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **흐름 제어 (Flow)** | 수신단 소켓 버퍼 오버플로우를 방지하기 위해 **수신자가 통보하는 수신 윈도우(rwnd) 준수** | 수신 호스트 결정 |
| **혼잡 제어 (Congestion)**| 네트워크 경로 상 라우터 큐 포화 및 패킷 드롭을 방지하기 위해 **혼잡 윈도우(cwnd) 동적 조절** | 송신 호스트 결정 |
| **유효 전송 윈도우** | 실제 송신자가 파이프라인으로 전송 가능한 데이터 바이트 수로 **$\min(\text{rwnd}, \text{cwnd})$ 산출** | 송신 스택 계산 |
| **ECN 마킹 엔진** | 라우터 버퍼가 차오를 때 **패킷 드롭 대신 IP/TCP 헤더에 ECN 플래그를 마킹하여 조기 경보** | RFC 3168 |

#### 한줄 요약
- 수신단 버퍼 보호(rwnd), 망 큐 보호(cwnd), 유효 윈도우 산출, ECN 통보가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AIMD (Additive Increase Multiplicative Decrease)**: 손실이 없을 때는 선형 증가(+1 MSS/RTT), 혼잡 발생 시 절반 곱셈 감소(/2)를 수행하는 공평성 알고리즘.

</details>

```text
TCP 이중 전송 제어 파이프라인
        │
   1. [유효 윈도우 계산] $\min(\text{rwnd}, \text{cwnd})$ 산출 후 패킷 연속 송출
        │
   2. [수신단 피드백 수신] 새로운 rwnd 및 ECN 신호 / ACK 수신
   ┌────┴───────────────────────────┐
  정상 수신 (ACK 연속 도착)       패킷 손실 또는 ECN 신호 감지
   │                                 │
   ├─ cwnd < ssthresh (Slow Start)   3. [혼잡 회피 발동]
   │  • RTT마다 cwnd 2배 지수 증가       • ssthresh = cwnd / 2 설정
   │                                 • 3 Dup ACK: Fast Retransmit & Recovery
   └─ cwnd >= ssthresh (혼잡 회피)   • RTO Timeout: cwnd = 1 초기화
      • RTT마다 1 MSS 선형 증가
        │                                 │
        └────────────────┬────────────────┘
                         ▼
   4. 안정적인 종단 간 처리량 및 네트워크 공평성 유지
```

#### 한줄 요약
- 유효 윈도우 계산 → Slow Start / 혼잡 회피 → 손실 감지 시 ssthresh 절반 축소 및 복구 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Bufferbloat (버퍼블로트)**: 대용량 라우터 큐에서 패킷을 과도하게 쌓아두어 손실은 없으나 왕복 지연(RTT)이 수 초 이상 폭증하는 현상.

</details>

| 비교 항목 | 흐름 제어 (Flow Control) | 혼잡 제어 (Congestion Control) |
|:---|:---|:---|
| **해결 문제 영역** | **송수신 종단 호스트 간의 처리 속도 불일치** | **네트워크 경로 상 라우터/스위치 큐 용량 초과** |
| **핵심 제어 파라미터**| **rwnd** (수신자가 TCP 헤더 Window로 통보) | **cwnd, ssthresh** (송신단 내부 연산) |
| **통제 메커니즘** | **슬라이딩 윈도우, Window Scale, 지속 타이머**| **Slow Start, AIMD, Fast Retransmit / Recovery**|
| **병목 발생 시 현상** | **Zero Window (rwnd=0)로 송신 전면 중단** | **패킷 드롭 손실, RTO 만료, RTT 지연 폭증** |

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

- 대규모 분산 클라우드 환경에서 전송 효율성과 네트워크 공평성을 극대화하기 위해 **수신단 버퍼 오토튜닝(Flow Control)과 커널 레벨의 BBR/CUBIC 혼잡 제어 엔진(Congestion Control)을 통합 운용**하고, **네트워크 스위치/라우터에 AQM(FQ-CoDel) 및 ECN 조기 혼잡 통보**를 결합하여 초고속·초저지연 무결점 전송 인프라 완성

#### 한줄 요약
- TCP 흐름·혼잡 제어는 $\min(\text{rwnd}, \text{cwnd})$을 통해 수신 버퍼와 망 큐를 이중 보호하며, BBR과 AQM을 결합하여 버퍼블로트를 극복하는 핵심 전송 기술이다.