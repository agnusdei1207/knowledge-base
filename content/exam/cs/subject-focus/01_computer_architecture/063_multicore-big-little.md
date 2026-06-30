---
title: "멀티코어·big.LITTLE (Multicore / ARM big.LITTLE)"
date: "2026-06-30"
weight: 63
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 단일 칩에 다수 코어를 집적한 멀티코어 구조이며, big.LITTLE은 고성능 big 코어와 저전력 LITTLE 코어를 이종 결합한 ARM의 전력효율 아키텍처.

## Ⅱ. 구성요소 / 원리
- 멀티코어: 단일 다이에 다수 코어 + 공유 L2/L3 캐시
- big.LITTLE: 고성능(big)·고효율(LITTLE) 이종 코어 클러스터
- 작업 부하에 따라 코어 마이그레이션·DVFS로 전력 최적화
- 캐시 일관성 인터커넥트(CCI)로 클러스터 간 일관성 유지

## Ⅲ. 흐름도 / 구조
```text
[Multicore]  Core0 Core1 Core2 Core3 ─ 공유 L3
[big.LITTLE] (big big)│(LIT LIT) ─CCI─ 부하別 전환
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | TLP 활용 성능↑ + 전력대비 효율 극대화 |
| 장점 | 병렬 처리량, 이종 코어로 성능/전력 균형 |
| 한계 | 병렬화 한계(암달의 법칙), 스케줄링·일관성 복잡 |

## Ⅴ. 기술사적 적용
- 모바일 AP(스마트폰), 노트북 SoC의 표준
- ARM DynamIQ·Intel P/E코어(하이브리드)로 발전
- OS 스케줄러의 이종코어 인지(EAS, Energy-Aware Scheduling)
