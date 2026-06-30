---
title: "페이지교체 (Page Replacement, OPT/FIFO/LRU/Clock/LFU)"
date: "2026-06-30"
weight: 63
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 페이지교체(Page Replacement)는 페이지부재 발생 시 빈 프레임이 없을 때 메모리에서 내보낼 희생 페이지(Victim)를 선정하는 알고리즘으로, 부재율 최소화를 목표로 한다.

## Ⅱ. 구성요소 / 원리
- OPT(Optimal): 가장 오래 사용 안 될 페이지 교체, 최소 부재이나 미래 예측 불가(이론 기준)
- FIFO(First-In First-Out): 가장 먼저 적재된 페이지 교체, 단순하나 벨라디 모순 발생
- LRU(Least Recently Used): 가장 오래 참조 안 된 페이지 교체, 지역성 활용
- Clock(2차 기회): 참조비트로 LRU 근사, Clock 구조로 효율화
- LFU(Least Frequently Used): 참조 빈도 최소 페이지 교체

## Ⅲ. 흐름도 / 구조
```text
페이지부재 → 빈 프레임? ─있음─▶ 적재
                │없음
          [교체 알고리즘으로 victim 선정]
          OPT/FIFO/LRU/Clock/LFU
                ▼
          victim out → 새 페이지 in → 갱신
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 희생 페이지 선정으로 부재율 최소화 |
| 장점 | LRU/Clock은 지역성 기반 우수, OPT는 이론적 최적 |
| 한계 | OPT 구현 불가, LRU 비용 큼, FIFO 벨라디 모순 |

## Ⅴ. 기술사적 적용
- LRU·OPT는 스택 알고리즘으로 벨라디 모순 없음, FIFO는 발생
- 실무는 Clock(2차 기회)·LRU 근사로 비용·성능 절충
