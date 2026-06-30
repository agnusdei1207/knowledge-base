---
title: "DVFS (Dynamic Voltage and Frequency Scaling)"
date: "2026-06-30"
weight: 86
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> DVFS(Dynamic Voltage and Frequency Scaling)는 워크로드에 따라 프로세서의 동작 전압과 주파수를 동적으로 조절해 전력 소비와 발열을 최적화하는 전력관리 기법이다.

## Ⅱ. 구성요소 / 원리
- 동적전력 P ∝ C·V²·f (전압의 제곱에 비례)
- 부하 낮을 때 주파수·전압 하향, 높을 때 상향
- 거버너(Governor): performance, powersave, ondemand 등 정책
- P-State(전압·주파수 조합) 전환, 거버너가 부하 모니터링

## Ⅲ. 흐름도 / 구조
```text
[부하 모니터링] → 거버너 정책 판단
   ├ 부하↑ → V·f 상향 (성능)
   └ 부하↓ → V·f 하향 (절전)
        → 전력/발열 최적화
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 성능-전력 균형, 발열·배터리 관리 |
| 장점 | 전력효율↑, 발열 감소, 비용 절감 |
| 한계 | 전환 지연(latency), 성능 변동, 정책 튜닝 필요 |

## Ⅴ. 기술사적 적용
- 모바일 SoC·노트북의 배터리 수명 연장 핵심
- 데이터센터 전력비용·PUE 개선
- DPM(Dynamic Power Management)·Turbo Boost와 연계
