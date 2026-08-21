---
sidebar:
  order: 28
  label: "028. TCP 흐름•혼잡 제어 (Flow & Congestion Control)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "TCP 흐름•혼잡 제어 : 슬라이딩 윈도우•Slow Start (TCP Control)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 28
extra:
  question_no: "028"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "수신단 흐름 제어(rwnd)와 망 내부 혼잡 제어(cwnd) 통합 메커니즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **흐름 제어(Flow Control)**: 송신 측과 수신 측 간의 처리 속도 불일치로 인한 수신 버퍼 오버플로우를 방지하기 위해, 수신자가 광고하는 수신 윈도우(rwnd) 크기 이하로 송신량을 제어하는 기법.
- **혼잡 제어(Congestion Control)**: 네트워크 경로 상의 라우터 큐 오버플로우 및 패킷 드롭으로 인한 망 붕괴(Congestion Collapse)를 방지하기 위해, 송신자가 혼잡 윈도우(cwnd)를 동적으로 조절하는 기법.

</details>

- 정의/개념: TCP 송신단이 수신 버퍼 여유 공간(**rwnd**)과 중간 네트워크 혼잡 상태(**cwnd**)를 모두 계측하여 $\min(\text{rwnd}, \text{cwnd})$ 한도로 전송량을 제어하는 **이중 전송 제어 메커니즘**
- 배경/필요성: 수신 호스트의 버퍼 고갈로 인한 패킷 폐기와 중간 네트워크 라우터 큐 포화로 인한 대규모 패킷 손실을 동시에 방지할 필요성 대두

#### 한줄 요약
- 수신자 보호(흐름 제어)와 네트워크 보호(혼잡 제어)의 최솟값으로 송신량을 동적 제어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **수신 윈도우(Receive Window, rwnd)**: 수신 호스트의 TCP 소켓 수신 버퍼 잔여 용량.
- **혼잡 윈도우(Congestion Window, cwnd)**: 송신 호스트가 네트워크 혼잡 상태(패킷 손실, RTT 변화, ECN 등)를 추정하여 산출하는 전송 허용량.
- **느린 시작 임계치(Slow Start Threshold, ssthresh)**: 지수적 증가(Slow Start)에서 선형적 증가(Congestion Avoidance)로 전환되는 cwnd 기준점.

</details>

- 전송량의 최종 결정은 항상 **$\min(\text{rwnd}, \text{cwnd})$** 에 의해 엄격히 제한
- **흐름 제어**: 수신 측의 피드백(ACK 헤더 내 Window 필드)에 의해 수동적으로 결정
- **혼잡 제어**: 느린 시작(Slow Start), 혼잡 회피(Congestion Avoidance), 빠른 재전송(Fast Retransmit), 빠른 회복(Fast Recovery)을 통해 송신 측이 능동적으로 결정

#### 한줄 요약
- rwnd와 cwnd 중 최솟값을 유효 윈도우로 적용하며, Slow Start와 혼잡 회피를 통해 최적 전송량을 탐색한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **명시적 혼잡 통보(Explicit Congestion Notification, ECN)**: 라우터가 버퍼 혼잡 발생 시 패킷을 즉시 드롭하지 않고 IP 헤더의 ECN 비트를 마킹하여 종단 간에 혼잡을 통보하는 기술(RFC 3168).

</details>

```text
[ TCP 송신단 전송 제어 구조 ]

 ┌───────────────────────────────────────────────────────────┐
 │ 송신 TCP 엔진                                             │
 │ ├─ 1. 혼잡 제어 모듈: cwnd 및 ssthresh 계산 (망 상태 반영)  │
 │ ├─ 2. 흐름 제어 모듈: 수신단 rwnd 수신 (버퍼 상태 반영)   │
 │ └─ 3. 유효 윈도우 결정: Effective Window = min(rwnd, cwnd) │
 └─────────────────────────────┬─────────────────────────────┘
                               │ min(rwnd, cwnd) 연속 송출
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 중간 네트워크 (라우터/스위치: ECN 마킹 또는 드롭 발생)   │
 └─────────────────────────────┬─────────────────────────────┘
                               │ 패킷 전달
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 수신 TCP 엔진 (수신 버퍼 잔여 공간 측정 ➔ ACK(rwnd) 회신)  │
 └───────────────────────────────────────────────────────────┘
```

선의 의미: 송신단의 cwnd/rwnd 비교부터 중간 망 전송 및 수신단의 rwnd 피드백으로 이어지는 폐루프 제어 구조

| 구성요소 | 통제 대상 | 결정 주체 | 핵심 제어 파라미터 |
|:---|:---|:---|:---|
| **흐름 제어 (Flow Control)** | 수신단 소켓 버퍼 오버플로우 방지 | **수신 호스트** | **rwnd** (Receive Window) |
| **혼잡 제어 (Congestion Control)** | 네트워크 경로 상 라우터 큐 포화 방지 | **송신 호스트** | **cwnd**, **ssthresh**, RTT |
| **유효 전송 윈도우** | 실제 송신 가능한 데이터 바이트 수 | 송신 TCP 스택 | **$\min(\text{rwnd}, \text{cwnd})$** |

#### 한줄 요약
- 수신단 버퍼 보호(rwnd)와 망 큐 보호(cwnd)를 결합하여 유효 윈도우를 결정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **AIMD(Additive Increase Multiplicative Decrease)**: 패킷 손실이 없을 때는 cwnd를 선형 증가(RTT당 +1 MSS)시키고, 손실 발생 시 cwnd를 절반으로 급격히 줄이는 공평성(Fairness) 제어 원리.

</details>

```text
1. 유효 윈도우 계산: min(rwnd, cwnd) 산출 후 데이터 세그먼트 송출
            │
            ▼
2. 수신 측 ACK 회신 수신 (새로운 rwnd 및 ECN 신호 포함)
            │
            ├─ [패킷 손실 또는 ECN 혼잡 신호 감지]
            │       │
            │       ▼
            │   3a. ssthresh = cwnd / 2 설정 후 cwnd 급격 축소 (혼잡 제어 발동)
            │
            └─ [정상 수신 확인 (ACK 연속 수신)]
                    │
                    ├─ [cwnd < ssthresh (Slow Start)] ────────▶ 3b. cwnd를 RTT마다 지수적 2배 증가
                    └─ [cwnd >= ssthresh (Congestion Avoidance)] ─▶ 3c. cwnd를 RTT마다 선형 1 MSS 증가
```

**동작 원리**

1. **전송량 제한**: 송신 측은 매 전송 시점마다 `min(rwnd, cwnd)`를 초과하지 않는 범위 내에서 패킷 송출
2. **ACK 분석**: 수신 측의 가용 버퍼(`rwnd`)와 네트워크 혼잡 지표(ACK 도착 시간, 손실 여부) 수집
3. **Slow Start**: 초기 전송 시 cwnd를 1 MSS부터 지수 함수적으로 빠르게 증가시켜 가용 대역폭 탐색
4. **혼잡 회피**: `ssthresh` 도달 후 AIMD 원리에 따라 매 RTT마다 1 MSS씩 완만하게 증가
5. **혼잡 대응**: 3 중복 ACK 발생 시 빠른 재전송 및 Fast Recovery 수행, 타임아웃 시 cwnd=1로 초기화

#### 한줄 요약
- 유효 윈도우 송출 후 ACK 분석을 통해 Slow Start, 혼잡 회피, 혼잡 대응을 반복 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **버퍼블로트(Bufferbloat)**: 대용량 라우터 큐에서 패킷을 과도하게 버퍼링하여 패킷 손실은 없으나 왕복 지연 시간(RTT)이 수 초 이상 극단적으로 증가하는 현상.

</details>

| 비교 항목 | 흐름 제어 (Flow Control) | 혼잡 제어 (Congestion Control) |
|:---|:---|:---|
| **문제 영역** | 송수신 종단 간(End-to-End)의 속도 불일치 | 네트워크 경로 상 라우터 큐의 전송 용량 초과 |
| **제어 파라미터** | **rwnd** (TCP 헤더 Window 필드로 통보) | **cwnd**, **ssthresh** (송신단 내부 계산) |
| **통제 메커니즘** | **슬라이딩 윈도우**, Window Scale, 지속 타이머 | **Slow Start, AIMD, Fast Retransmit/Recovery** |
| **병목 발생 시 현상** | **Zero Window (rwnd=0)** 로 송신 전면 중단 | **패킷 손실, RTO 타임아웃, RTT 지연 급증** |

#### 한줄 요약
- 흐름 제어는 종단 간 버퍼 상태를 제어하고, 혼잡 제어는 경로 상의 라우터 큐 상태를 제어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BBR(Bottleneck Bandwidth and RTT)**: 패킷 손실을 혼잡의 지표로 보지 않고, 실제 대역폭과 최소 RTT를 측정하여 버퍼블로트 없이 최대 처리량을 달성하는 구글의 혼잡 제어 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수신 애플리케이션 지연으로 인한 지속적 **Zero Window(rwnd=0)** 발생 | 백엔드 비동기 처리 및 소켓 수신 버퍼(`SO_RCVBUF`) 확장 | 수신 버퍼 고갈 방지 및 지속 타이머 교착 해소 |
| 무선망의 일시적 비트 오류 손실을 망 혼잡으로 오인하여 cwnd 급감 | 손실 기반 대신 지연/대역폭 기반인 **BBR 알고리즘** 적용 | 무선 패킷 유실 환경에서도 대역폭 저하 없는 전송률 유지 |
| 라우터 큐 과도 점유로 인해 패킷 지연이 폭증하는 **버퍼블로트** 현상 | 라우터에 **능동 큐 관리(AQM, CoDel/FQ-CoDel)** 및 ECN 활성화 | 큐 대기 시간 최소화 및 실시간 상호작용성(RTT) 개선 |

#### 한줄 요약
- 수신 버퍼 튜닝으로 Zero Window를 해소하고, BBR 알고리즘과 AQM으로 버퍼블로트를 극복한다.

## Ⅶ. 결론

- TCP 전송 성능 최적화를 위해 애플리케이션 레벨의 **수신 버퍼 튜닝(Flow Control)** 과 커널 레벨의 최신 혼잡 제어 엔진인 **BBR/CUBIC(Congestion Control)** 을 유기적으로 연계하며, 네트워크 장비에는 **AQM/ECN**을 도입하여 처리량 극대화와 초저지연을 동시에 달성

#### 한줄 요약
- 흐름 제어와 현대적 혼잡 제어(BBR/AQM)의 결합을 통해 고성능 전송 인프라를 구축한다.
