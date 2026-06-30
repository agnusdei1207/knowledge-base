---
title: "쓰기정책·더티비트 (Write Policy: Write-Through·Write-Back / Dirty Bit)"
date: "2026-06-30"
weight: 46
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 캐시 쓰기 시 하위 계층과의 데이터 갱신 시점을 정하는 정책으로, 즉시 반영(Write-Through)·지연 반영(Write-Back)이 있으며, 더티비트(Dirty Bit)는 변경 여부를 표시.

## Ⅱ. 구성요소 / 원리
- Write-Through(WT): 캐시·메모리 동시 기록, 일관성 단순·트래픽↑
- Write-Back(WB): 캐시만 기록 후 축출 시 메모리 반영, 트래픽↓
- Dirty Bit: WB에서 수정된 블록 표시, 축출 시 1이면 메모리 갱신
- 쓰기 실패 정책: Write-Allocate(블록 적재 후 쓰기) vs No-Write-Allocate
- 보조: 쓰기 버퍼(Write Buffer)로 WT 지연 은닉

## Ⅲ. 흐름도 / 구조
```text
Write-Through: Write → Cache + Memory 동시 (Dirty 불요)
Write-Back   : Write → Cache(Dirty=1) … 축출 시 → Memory
   Dirty=0 ⇒ 그냥 버림 / Dirty=1 ⇒ 메모리 갱신 후 교체
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 쓰기 일관성과 메모리 트래픽 간 절충 |
| 장점 | WT=일관성·구현 단순, WB=대역폭 절약·고성능 |
| 한계 | WT=쓰기 트래픽 과다, WB=일관성 복잡·전원장애 시 손실 |

## Ⅴ. 기술사적 적용
- 비교: WT+Write Buffer vs WB+Write-Allocate(고성능 캐시 표준)
- 실무: 멀티코어 WB + MESI로 일관성 유지
- 최신: 비휘발 캐시(NVM)에서 WB 데이터 내구성 확보(영속화)
