---
title: "PIM·메모리월 (Processing-In-Memory / Memory Wall)"
date: "2026-06-30"
weight: 82
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 메모리월(Memory Wall)은 CPU 연산속도 대비 메모리 대역폭·지연 격차로 인한 성능 병목이며, PIM(Processing-In-Memory)은 메모리 내부에 연산기를 두어 데이터 이동을 최소화하는 컴퓨팅 패러다임이다.

## Ⅱ. 구성요소 / 원리
- 메모리월: 프로세서-메모리 성능 발전 속도 불균형에서 기인
- PIM: DRAM 뱅크 내부 또는 인근에 연산 유닛(PU) 배치
- 데이터 이동(폰노이만 병목) 대신 메모리 내 연산
- 유형: In-DRAM(셀 연산), Near-Memory(로직 다이 근접)

## Ⅲ. 흐름도 / 구조
```text
기존:  [CPU]◄─대역폭 병목─►[Memory]   (데이터 왕복)
PIM :  [Memory + PU]  → 내부 연산 → 결과만 전송
        └ 이동량·전력 대폭 감소
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 데이터 이동 최소화로 메모리월 극복 |
| 장점 | 대역폭·전력효율 향상, 지연 감소 |
| 한계 | 프로그래밍 모델·표준 미성숙, 연산 유연성 제약 |

## Ⅴ. 기술사적 적용
- HBM-PIM(삼성), AiM(SK하이닉스)로 AI 추론 가속
- CXL·Near-Memory와 결합한 메모리 중심 컴퓨팅
- 추천시스템·LLM의 메모리 바운드 연산에 효과적
