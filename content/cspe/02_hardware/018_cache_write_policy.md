---
title: "캐시 쓰기 정책 - Write-Through vs Write-Back (Cache Write Policy)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 18
---

## 미리 알고가기

- Write hit: CPU가 쓰려는 주소가 캐시에 존재하는 상황임
- Write miss: CPU가 쓰려는 주소가 캐시에 없어 메모리에서 가져오거나 바로 기록해야 하는 상황임
- Dirty bit: 캐시 line이 메모리보다 최신인지 표시하는 상태 비트임
- Write buffer: 캐시와 메모리 사이의 쓰기 지연을 흡수하는 임시 큐임

## Ⅰ. 개요

- **정의**: 캐시 쓰기 정책은 CPU가 캐시에 데이터를 쓸 때 변경 내용을 주기억장치에 언제, 어떤 조건으로 반영할지 정하는 캐시 일관성·성능 정책임. write-through와 write-back은 메모리 대역폭, 데이터 최신성, 장애·일관성 비용을 기준으로 비교함.
- **배경/필요성**: 캐시는 CPU 가까이에 있어 쓰기 지연을 줄이지만 주기억장치와 값이 달라질 수 있음. 쓰기 정책은 대역폭 절감을 위해 메모리 반영을 늦출지, 최신성을 위해 즉시 반영할지 결정해야 함.
- **비유**: write-through는 장부를 쓸 때마다 본사 장부까지 즉시 고치는 방식이고, write-back은 지점 장부에 표시해 두었다가 정산 때 본사 장부에 반영하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 쓰기 반영 시점과 성능·일관성 절충 설명 | write-through, write-back, dirty bit, write buffer | write policy와 replacement policy 혼동 |

> 요약: 캐시 쓰기 정책은 쓰기 지연 단축과 메모리 최신성 사이의 절충을 정하는 기준임.

## Ⅱ. 특징/비교

| 판단 기준 | Write-Through | Write-Back |
|:---|:---|:---|
| 반영 시점 | 캐시에 쓸 때 메모리에도 즉시 기록함 | 캐시에만 쓰고 eviction 때 dirty line을 메모리에 기록함 |
| 성능 특성 | 메모리 write traffic이 많아 write buffer 의존도가 큼 | 반복 쓰기를 캐시 안에서 흡수해 대역폭을 절감함 |
| 일관성·복구 | 메모리가 최신 상태라 복구와 DMA 연동이 단순함 | dirty data 관리와 writeback 순서 보장이 필요함 |
| 적용 기준 | 단순 캐시, embedded, 일관성 단순성이 중요할 때 | 현대 CPU data cache, 대역폭 절감과 쓰기 지연 단축이 중요할 때 |

> 요약: write-through는 단순성과 최신성, write-back은 성능과 대역폭 절감을 선택함.

## Ⅲ. 구성요소

```text
Write-through:
+-----+     +-------+     +--------+
| CPU | --> | Cache | --> | Memory |
+-----+     +-------+     +--------+

Write-back:
+-----+     +-------------+     +--------+
| CPU | --> | Cache Dirty | --> | Memory |
+-----+     +-------------+     +--------+
                         evict/writeback
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Cache line | CPU가 읽고 쓰는 데이터 블록이며 tag와 상태 비트를 가짐 | 지점 장부 |
| Dirty bit | write-back에서 메모리보다 캐시가 최신임을 표시함 | 수정 표시 |
| Write buffer | 메모리 쓰기 지연을 비동기로 흡수해 CPU 대기를 줄임 | 발송 대기함 |
| Coherence controller | 멀티코어에서 다른 캐시와 메모리 상태 전이를 조정함 | 정산 관리자 |

> 요약: 쓰기 정책은 cache line 상태, dirty 표시, buffer, coherence 제어가 함께 동작해야 함.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Write    | --> | Hit/Miss | --> | Policy   | --> | Commit   |
+----------+     +----------+     +----------+     +----------+
 CPU store        cache check      WT or WB         memory now/later
```

1. **쓰기 요청** - CPU store 명령이 주소와 데이터를 캐시 계층에 전달함
2. **hit/miss 판정** - tag와 valid bit로 캐시 line 존재 여부를 확인함
3. **정책 적용** - write-through는 메모리 쓰기를 함께 발행하고 write-back은 dirty bit를 설정함
4. **반영 완료** - eviction, flush, coherence 이벤트 발생 시 dirty line을 메모리에 기록함

> 요약: 캐시 쓰기는 hit 판정 후 정책에 따라 즉시 메모리 반영 또는 dirty 지연 반영으로 나뉨.

## Ⅴ. 문제점 및 개선방안

- **P1 write-through 대역폭 부담**: 쓰기마다 메모리 traffic이 발생해 write buffer overflow와 CPU stall이 생길 수 있음
- **P1 대응**: write buffer, write combining, store coalescing으로 메모리 쓰기를 묶어 처리함 (확인: write stall, buffer occupancy)
- **P2 write-back 최신성 위험**: dirty data가 캐시에만 존재하므로 장애, DMA, 다른 코어 접근 시 정합성 관리가 복잡함
- **P2 대응**: MESI/MOESI, flush 명령, 직접 메모리 접근(Direct Memory Access, DMA) coherency, ECC와 전원 보호 정책을 적용함 (확인: dirty eviction, coherency test)
- **P3 write miss 정책 충돌**: write-allocate와 no-write-allocate 선택이 workload에 맞지 않으면 캐시 오염이나 반복 miss가 발생함
- **P3 대응**: streaming write는 no-write-allocate, 재사용 데이터는 write-allocate로 workload별 정책을 구분함 (확인: cache pollution, write miss rate)

> 요약: 쓰기 정책의 문제는 메모리 traffic, dirty data 정합성, miss 시 캐시 적재 기준에서 발생하므로 정책별 검증 지표를 분리해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 임베디드 제어 시스템 | 직접 메모리 접근(Direct Memory Access, DMA) 장치가 메모리를 직접 읽는 구간은 write-through 또는 명시적 flush로 최신성을 보장함 | DMA coherency error, write stall, flush coverage |
| 서버 중앙처리장치(Central Processing Unit, CPU) 데이터 캐시 | 반복 store가 많은 workload는 write-back과 dirty bit 관리로 메모리 대역폭을 줄이되 eviction 폭주를 감시함 | writeback traffic, dirty eviction, buffer occupancy |
| 영속 메모리·컴퓨트 익스프레스 링크(Compute Express Link, CXL) 메모리 | 장애 복구 요구가 있는 영역은 cache line flush와 ordering fence로 지속성 경계를 명확히 함 | power-loss recovery, persist latency, ordering test |

> 요약: 캐시 쓰기 정책은 DMA·장애 복구·대역폭 조건에 따라 즉시 반영과 지연 반영의 검증 기준을 달리 둬야 함.

## Ⅶ. 전망

- **발전 방향**: 고성능 CPU는 write-back을 유지하되 persistent memory, CXL memory, 장치 DMA 환경에서는 flush 순서와 지속성 보장 정책이 더 중요해짐
- **기술사적 판단**: write-through, write-back, write-allocate 선택은 쓰기 빈도, 메모리 대역폭, 전력, dirty buffer 크기, 장애 복구 요구를 기준으로 정함; eviction writeback, dirty bit 전이, write buffer overflow, cache flush 명령, power loss 후 데이터 일관성을 테스트해야 함; dirty line 잔류, stale data 노출, DMA와 cache incoherence가 데이터 무결성 문제로 이어질 수 있어 권한과 flush 경계를 검증함
- **기술사 제언**: write policy는 속도 비교가 아니라 dirty bit, eviction, 대역폭, 장애 시 데이터 보존 조건을 묶어 설명해야 함
