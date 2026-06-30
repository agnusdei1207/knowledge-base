---
title: "TCP 변종 (TCP Variants)"
date: "2026-06-30"
weight: 66
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 표준 TCP(Transmission Control Protocol)의 혼잡제어 알고리즘을 네트워크 환경(고대역폭, 고지연, 무선)에 맞게 개선한 변형 알고리즘 집합.

## Ⅱ. 구성요소 / 원리
- Reno: AIMD(Additive Increase Multiplicative Decrease) 기반 손실 중심, 전통적 표준
- CUBIC: 3차 함수(Cubic Function)로 cwnd 증가, RTT 비의존, 리눅스 기본
- BBR(Bottleneck Bandwidth and Round-trip propagation time): 병목 대역폭·RTT를 모델링한 혼잡 추정
- 손실 기반(Reno/CUBIC) vs 모델 기반(BBR) 패러다임 구분
- 공정성(Fairness)·수렴 속도·버퍼블로트 대응 차이

## Ⅲ. 흐름도 / 구조
```text
 Reno  : cwnd ↗선형, 손실시 ½     (저속 안정)
 CUBIC : cwnd ↗3차곡선, RTT무관   (고속 광대역)
 BBR   : BtlBw × RTprop 추정       (버퍼블로트↓)
          └ 손실 아닌 대역폭 기반
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 다양한 네트워크에서 처리율·지연 최적화 |
| 장점 | CUBIC 고속 확장성, BBR 저지연·고처리율 동시 달성 |
| 한계 | BBR 구버전 공정성 논란, CUBIC 버퍼블로트 유발 가능 |

## Ⅴ. 기술사적 적용
- 리눅스 커널 기본 CUBIC, 구글 서비스·YouTube는 BBR 적용
- QUIC(Quick UDP Internet Connections) 혼잡제어로 BBR 채택 확대
- 데이터센터는 DCTCP, 무선은 손실 오인 방지형 변종 선택
