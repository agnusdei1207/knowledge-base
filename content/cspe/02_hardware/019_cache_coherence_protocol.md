---
title: "캐시 일관성 프로토콜 - MESI·MOESI (Cache Coherence Protocol)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 19
---

## 미리 알고가기

- Coherence: 같은 메모리 주소의 캐시 사본들이 모순된 값을 보이지 않게 하는 성질임
- MESI: Modified, Exclusive, Shared, Invalid 상태로 캐시 line을 관리하는 프로토콜임
- MOESI: MESI에 Owned 상태를 추가해 수정 데이터를 캐시 간 직접 공급할 수 있게 한 방식임
- Invalidate: 다른 캐시의 사본을 무효화해 쓰기 권한을 확보하는 동작임

## Ⅰ. 개요

- **정의**: 캐시 일관성 프로토콜은 멀티코어에서 여러 캐시가 같은 메모리 블록의 사본을 가질 때 읽기·쓰기 순서와 line 상태 전이를 제어해 최신 값을 보장하는 규칙임. MESI와 MOESI는 상태 수, 데이터 공급 경로, 트래픽 비용을 기준으로 비교함.
- **배경/필요성**: 코어별 private cache는 지연시간을 줄이지만 공유 변수 수정 시 다른 코어의 사본이 오래된 값이 될 수 있음. 일관성 프로토콜은 성능을 유지하면서 공유 메모리 프로그래밍 모델의 기본 정합성을 제공함.
- **비유**: 여러 사람이 같은 문서 사본을 갖고 있을 때 누가 원본을 수정했는지, 누가 읽기만 하는지, 어떤 사본을 폐기할지 정하는 문서 관리 규칙임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 멀티코어 캐시 상태 전이와 일관성 유지 설명 | M/E/S/I/O 상태, invalidate, writeback, cache-to-cache transfer | consistency와 coherence 혼동 |

> 요약: 캐시 일관성은 같은 주소의 여러 캐시 사본이 읽기·쓰기 후에도 모순되지 않게 하는 하드웨어 규칙임.

## Ⅱ. 특징/비교

| 판단 기준 | MESI | MOESI |
|:---|:---|:---|
| 상태 구성 | M, E, S, I 네 상태로 수정·공유·무효를 관리함 | M, O, E, S, I로 Owned 상태를 추가함 |
| 수정 데이터 공급 | Modified line 요청 시 writeback 또는 owner 응답이 필요함 | Owned cache가 메모리 갱신 없이 다른 캐시에 데이터를 공급할 수 있음 |
| 트래픽 특성 | 구조가 단순하고 널리 쓰임 | 공유 수정 데이터가 많은 경우 메모리 traffic을 줄일 수 있음 |
| 적용 기준 | 일반 멀티코어 캐시 | cache-to-cache transfer 이득이 큰 서버·고성능 코어 |

> 요약: MOESI는 Owned 상태로 메모리 writeback을 줄이지만 상태 관리 복잡도가 증가함.

## Ⅲ. 구성요소

```text
MESI states:
             write
        +-------------+
        v             |
+---+ read  +---+  write +---+
| I | ----> | E | ------> | M |
+---+       +---+         +---+
  ^           | read         |
  |           v              | read by other
  |         +---+            v
  +---------| S | <----------+
 invalidate +---+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 상태 비트 | 각 cache line의 M/E/S/I/O 상태를 저장함 | 문서 상태 라벨 |
| Coherence controller | local CPU 요청과 외부 snoop/directory 메시지를 처리함 | 문서 관리자 |
| Invalidate/Update 메시지 | 쓰기 권한 확보 또는 사본 갱신을 위해 캐시 간 전달되는 신호임 | 폐기 통보 |
| Writeback/Data response | 수정된 line을 메모리나 요청 코어에 전달함 | 최신본 전달 |

> 요약: 일관성 프로토콜은 line 상태 비트와 캐시 간 메시지로 읽기·쓰기 권한을 관리함.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Request  | --> | Check    | --> | Message  | --> | Transition|
+----------+     +----------+     +----------+     +----------+
 read/write       local state      inv/data         MESI/MOESI
```

1. **요청 수신** - 코어의 read/write miss 또는 hit 요청을 coherence controller가 수신함
2. **상태 확인** - 해당 line의 M/E/S/I/O 상태와 다른 sharer 존재 여부를 확인함
3. **메시지 교환** - 쓰기 요청은 invalidate를 보내고 읽기 요청은 owner 또는 memory에서 데이터를 받음
4. **상태 전이** - 응답과 ack를 받은 뒤 line 상태를 Shared, Modified, Owned 등으로 갱신함

> 요약: 캐시 일관성은 요청, 상태 확인, 메시지 교환, 상태 전이의 반복으로 유지됨.

## Ⅴ. 문제점

- **P1 coherence traffic 증가**: 공유 데이터 쓰기가 많으면 invalidate, ack, writeback 메시지가 급증함
- **P2 false sharing**: 서로 다른 변수가 같은 cache line에 있으면 실제 공유가 없어도 invalidate가 반복됨
- **P3 확장성 한계**: 코어 수가 많아질수록 snoop broadcast와 상태 추적 비용이 커짐

> 요약: 일관성 비용은 공유 쓰기, cache line 단위 관리, 코어 수 증가에서 크게 나타남.

## Ⅵ. 개선방안

- **P1 대응**: read-mostly 데이터 분리, atomic 최소화, MOESI/MESIF 같은 cache-to-cache 최적화를 적용함 (확인: coherence miss, interconnect traffic)
- **P2 대응**: cache line padding, per-core data, 구조체 재배치로 false sharing을 제거함 (확인: invalidation rate, perf counter)
- **P3 대응**: directory coherence, snoop filter, hierarchical coherence로 broadcast 범위를 줄임 (확인: snoop bandwidth, scalability)

> 요약: 캐시 일관성 개선은 프로토콜만이 아니라 데이터 배치와 공유 패턴 최적화가 함께 필요함.

## Ⅶ. 전망

- **발전 방향**: 멀티코어와 칩렛이 늘면서 directory, snoop filter, NoC 기반 coherence가 중요해지고 CXL.cache처럼 외부 장치까지 일관성 범위가 확장됨
- **기술사적 판단**: MESI/MOESI, directory, snooping 선택은 코어 수, 공유 데이터 빈도, 패키지 경계, interconnect 대역폭, 상태 저장 비용을 기준으로 정함; read/write race, invalidation 누락, dirty owner 전이, memory ordering litmus test, reset 후 상태 회복을 시뮬레이션과 silicon test로 확인함; 장치가 coherence domain에 들어오면 권한 없는 DMA와 stale cache line 위험이 커지므로 IOMMU, PASID, 접근 권한을 함께 검증함
- **기술사 제언**: 상태 약어보다 Modified 쓰기, Shared 읽기, invalidation 메시지 흐름을 제시해야 cache 일관성의 본질이 드러남
