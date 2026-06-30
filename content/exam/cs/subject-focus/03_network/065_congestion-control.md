---
title: "혼잡 제어 (Congestion Control)"
date: "2026-06-30"
weight: 65
tags:
  - "exam-cspe-network"
---

## Ⅰ. 1교시 핵심 답안

> 혼잡 제어는 네트워크 내부 혼잡을 감지하여 송신 측 전송량을 조절함으로써 패킷 손실과 지연 폭증을 방지하는 메커니즘이다.

- **제어 변수**: `CWND`, `SSTHRESH`
- **주요 단계**: `Slow Start`, `Congestion Avoidance`
- **혼잡 신호**: Timeout, 3 Duplicate ACK, ECN
- **출제 포인트**: 흐름 제어와 혼잡 제어의 차이

## Ⅱ. 구조 및 동작 원리

```text
cwnd = 1 MSS
 -> Slow Start (지수 증가)
 -> ssthresh 도달
 -> Congestion Avoidance (선형 증가)
 -> 손실 감지
    - Timeout: 크게 축소
    - 3 Dup ACK: Fast Retransmit/Recovery
```

- **RWND**: 수신자 처리 능력 반영
- **CWND**: 네트워크 혼잡 상태 반영
- **실제 송신량**: `min(RWND, CWND)`
- **목적**: 인터넷 전체의 붕괴와 불공정 점유 방지

## Ⅲ. 비교표

| 구분 | 흐름 제어 | 혼잡 제어 |
|:---|:---|:---|
| 보호 대상 | 수신자 버퍼 | 네트워크 내부 |
| 기준 신호 | RWND | 손실, 지연, ECN |
| 대표 제어값 | Receive Window | Congestion Window |
| 시험 논점 | 송수신 종단 | 네트워크 전체 안정성 |

## Ⅳ. 기술사 답안 포인트

- **인터넷 붕괴 방지**: 분산형 자율 제어의 대표 사례
- **알고리즘 진화**: Tahoe, Reno, NewReno, CUBIC, BBR
- **연계 주제**: AQM, ECN, Bufferbloat, QUIC 혼잡제어
- **비교 논점**: 고손실 무선망에서는 단순 손실 기반 제어의 한계 존재

## Ⅴ. 결론

혼잡 제어의 핵심은 전송속도 향상이 아니라 `네트워크 전체 안정성 유지`에 있다.  
따라서 답안은 `CWND 중심 제어`와 `흐름 제어와의 구분`을 명확히 하는 방향으로 작성해야 한다.
