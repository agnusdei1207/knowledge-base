---
title: "메모리 배리어 (Memory Barrier / Fence)"
date: "2026-06-30"
weight: 71
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 컴파일러·프로세서의 메모리 연산 재배열을 제한해, 배리어 이전 연산이 이후 연산보다 먼저 완료·관찰되도록 강제하는 동기화 명령.

## Ⅱ. 구성요소 / 원리
- Load Barrier(LFENCE): 이전 로드 완료 보장
- Store Barrier(SFENCE): 이전 스토어를 메모리에 가시화
- Full Barrier(MFENCE): 로드·스토어 모두 순서 강제
- Acquire/Release 시맨틱: 임계영역 진입/이탈 순서 보장

## Ⅲ. 흐름도 / 구조
```text
 store data       │ 재배열 금지
 ─── Memory Barrier ───
 store flag=1     │ flag 본 스레드는 data도 최신
 (다른 스레드: flag 확인 후 data 안전 접근)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 완화된 메모리 모델에서 메모리 순서·가시성 보장 |
| 장점 | 정확한 동기화·일관성 확보, 세밀한 순서 제어 |
| 한계 | 파이프라인·재배열 억제로 성능 비용, 사용 난해 |

## Ⅴ. 기술사적 적용
- x86 LFENCE/SFENCE/MFENCE, ARM DMB/DSB/ISB
- 메모리 일관성 모델(완화)과 짝을 이루는 순서 보장 수단
- 락프리 알고리즘·C++ atomic(memory_order_acquire/release) 구현 기반
