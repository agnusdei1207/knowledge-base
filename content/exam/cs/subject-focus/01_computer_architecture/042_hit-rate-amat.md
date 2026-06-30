---
title: "적중률·AMAT (Hit Rate / Average Memory Access Time)"
date: "2026-06-30"
weight: 42
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 적중률(Hit Rate)은 전체 참조 중 캐시 적중 비율, AMAT(Average Memory Access Time)은 적중·실패를 가중한 평균 메모리 접근시간으로 캐시 성능의 핵심 지표.

## Ⅱ. 구성요소 / 원리
- 적중률 H = 적중 횟수 / 전체 참조, 실패율(Miss Rate) = 1 − H
- AMAT = Hit Time + Miss Rate × Miss Penalty
- Hit Time: 캐시 적중 시 접근시간, Miss Penalty: 하위 계층 적재 지연
- 다단계 확장: AMAT = HT_L1 + MR_L1 × (HT_L2 + MR_L2 × MP_L2 …)
- 성능 결정 요인: 블록 크기·연관도·캐시 용량·교체정책

## Ⅲ. 흐름도 / 구조
```text
        ┌── Hit (확률 H) ──→ Hit Time
참조 ───┤
        └── Miss(확률 1-H)→ Hit Time + Miss Penalty
AMAT = HitTime + (1−H) × MissPenalty
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 캐시·계층 구조의 정량적 성능 평가 및 설계 비교 |
| 장점 | 단일 수식으로 다단계 성능 통합 분석 가능 |
| 한계 | 정적 평균값, 실제는 대역폭·MLP·경쟁 미반영 |

## Ⅴ. 기술사적 적용
- 비교: 블록 크기 ↑ → 공간 지역성↑이나 Miss Penalty↑ 균형점 탐색
- 실무: 프로파일링으로 MPKI(Miss Per Kilo Instructions) 측정·튜닝
- 최신: 비순차 실행·MSHR로 Miss 중첩, 유효 Miss Penalty 감소
