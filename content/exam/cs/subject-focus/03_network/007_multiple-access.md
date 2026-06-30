---
title: "다중접속 (Multiple Access)"
date: "2026-06-30"
weight: 7
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 다수의 사용자가 하나의 공유 무선/전송 자원에 접속하여 통신할 수 있도록 주파수·시간·코드·부반송파 등으로 자원을 분배하는 기술이다.

## Ⅱ. 구성요소 / 원리
- FDMA(Frequency Division Multiple Access): 사용자별 주파수 채널 할당(1G AMPS)
- TDMA(Time Division Multiple Access): 사용자별 타임슬롯 할당(2G GSM)
- CDMA(Code Division Multiple Access): 직교 코드로 전 대역 공유, 사용자 구분(2G/3G)
- OFDMA(Orthogonal FDMA): 직교 부반송파 그룹을 사용자별 할당(4G/5G/Wi-Fi 6)
- 자원분할 축: 주파수(FDMA)·시간(TDMA)·코드(CDMA)·시간·주파수 2차원(OFDMA)

## Ⅲ. 흐름도 / 구조
```text
공유 자원(주파수·시간·코드)을 사용자에 분배:
 FDMA: |U1|U2|U3|  (주파수 축 분할)
 TDMA: U1-U2-U3-U1  (시간 축 분할)
 CDMA: U1+U2+U3 중첩 (코드로 분리)
 OFDMA: 부반송파×슬롯 2차원 자원블록 할당
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 한정된 무선 자원을 다수 사용자에게 효율·공정하게 분배 |
| 장점 | OFDMA는 사용자별 자원블록 유연 할당으로 주파수효율·다중접속 효율 우수 |
| 한계 | FDMA는 가드밴드 낭비, CDMA는 원근문제(전력제어 필요), TDMA는 동기 부담 |

## Ⅴ. 기술사적 적용
- 이동통신 세대 진화: FDMA(1G)→TDMA/CDMA(2G)→CDMA(3G)→OFDMA(4G/5G)
- 5G NR·Wi-Fi 6는 OFDMA로 다수 단말 동시 전송과 지연 단축 실현
- 위성·NB-IoT는 트래픽 특성에 맞춰 FDMA/TDMA 혼합 접속 적용
