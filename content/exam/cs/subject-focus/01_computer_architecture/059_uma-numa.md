---
title: "UMA·NUMA (Uniform / Non-Uniform Memory Access)"
date: "2026-06-30"
weight: 59
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 공유 메모리 다중처리에서 프로세서-메모리 접근 지연의 균일성에 따른 분류로, 모든 메모리 접근이 동일한 UMA와 지역/원격에 따라 다른 NUMA 구조.

## Ⅱ. 구성요소 / 원리
- UMA(Uniform Memory Access): 모든 프로세서가 동일 지연으로 공유 메모리 접근(SMP)
- NUMA(Non-Uniform Memory Access): 노드 지역 메모리는 빠르고 원격 메모리는 느림
- NUMA는 노드 간 고속 인터커넥트(QPI·UPI·Infinity Fabric)로 연결
- ccNUMA: 캐시 일관성(Cache Coherence)을 보장하는 NUMA

## Ⅲ. 흐름도 / 구조
```text
[UMA]  P0 P1 P2 ── Bus ── [공통 Mem] (지연 동일)
[NUMA] (P0|Mem0)─IC─(P1|Mem1) : local快 / remote遲
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 프로세서 수 증가 시 메모리 병목 완화·확장성 확보 |
| 장점 | UMA=단순/공평, NUMA=높은 확장성·대역폭 |
| 한계 | UMA=버스 병목·확장 한계, NUMA=원격 접근 지연·배치 최적화 필요 |

## Ⅴ. 기술사적 적용
- UMA → 소규모 SMP 서버
- NUMA → 멀티소켓 서버, OS의 NUMA-aware 스케줄링·메모리 할당
- 코어 수 증가로 단일 칩 내 NUMA화 추세
