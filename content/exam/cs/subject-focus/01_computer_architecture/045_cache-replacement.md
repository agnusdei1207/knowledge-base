---
title: "교체알고리즘 (Cache Replacement: LRU·LFU·FIFO)"
date: "2026-06-30"
weight: 45
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 집합연관·완전연관 캐시에서 적재 공간이 없을 때 축출할 블록(victim)을 선정하는 규칙으로, 시간 지역성을 활용해 적중률을 높인다.

## Ⅱ. 구성요소 / 원리
- LRU(Least Recently Used): 가장 오래 미참조 블록 축출, 시간 지역성에 최적
- LFU(Least Frequently Used): 참조 빈도 최소 블록 축출, 빈도 카운터 필요
- FIFO(First In First Out): 가장 먼저 적재된 블록 축출, 구현 단순
- Random: 무작위 축출, 하드웨어 최소
- 근사: Pseudo-LRU(트리/비트)로 LRU 비용 절감

## Ⅲ. 흐름도 / 구조
```text
Set 가득참 → victim 선정
 LRU : [A older ... newer D] → A 축출
 LFU : 참조횟수 {A:2,B:5,C:1} → C 축출
 FIFO: 적재순 [A→B→C] → A 축출
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 미래 재참조 가능성 낮은 블록 제거로 적중률 향상 |
| 장점 | LRU가 지역성에 강건, FIFO/Random은 저비용 |
| 한계 | LRU 완전구현 비용↑, FIFO는 Belady 변칙, LFU는 노후 누적 |

## Ⅴ. 기술사적 적용
- 비교: Belady's OPT(미래 최장 미사용)는 이론적 하한
- 실무: Pseudo-LRU, RRIP(Re-Reference Interval Prediction) 채택
- 최신: 스캔/스트리밍 내성 DIP·SHiP 등 적응형 정책
