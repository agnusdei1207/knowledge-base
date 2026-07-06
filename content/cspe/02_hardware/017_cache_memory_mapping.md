---
title: "캐시 메모리 구조 - 직접·연관·집합 연관 매핑 (Cache Memory Mapping)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 17
---

## 미리 알고가기

- Cache line: 메모리에서 캐시로 이동하는 고정 크기 데이터 블록임
- Tag: 캐시 line이 어느 메모리 블록인지 식별하는 주소 상위 비트임
- Index: 캐시의 set 또는 line 위치를 선택하는 주소 비트임
- Associativity: 한 메모리 블록이 들어갈 수 있는 cache line 후보 수임

## Ⅰ. 개요

- **정의**: 캐시 메모리 매핑은 주기억장치 블록을 캐시의 어느 line 또는 set에 배치할지 정하는 주소 변환 규칙임. 직접 매핑, 완전 연관, 집합 연관 방식을 충돌 miss, 탐색 지연, 하드웨어 비용 기준으로 비교하는 데 쓰임.
- **배경/필요성**: 캐시는 CPU와 DRAM의 속도 차이를 줄이지만 용량이 작아 모든 데이터를 둘 수 없음. 제한된 캐시 공간에서 빠른 탐색과 높은 hit rate를 동시에 얻기 위해 매핑 방식이 필요함.
- **비유**: 주차장에서 차량을 지정석에만 댈지, 아무 빈자리에 댈지, 특정 구역 안에서 자유롭게 댈지 정하는 규칙임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 매핑 방식별 성능·비용 트레이드오프 설명 | direct, fully associative, set associative, tag/index/offset | 교체 알고리즘과 매핑 방식을 혼동 |

> 요약: 캐시 매핑은 주소 비트를 이용해 빠른 탐색과 충돌 감소 사이의 균형을 정하는 규칙임.

## Ⅱ. 특징/비교

| 판단 기준 | 직접 매핑 | 완전 연관 매핑 | 집합 연관 매핑 |
|:---|:---|:---|:---|
| 배치 자유도 | 메모리 블록이 한 line에만 배치됨 | 캐시 어느 line에도 배치 가능함 | 특정 set 안의 여러 way 중 선택함 |
| 탐색 비용 | index로 한 line만 확인해 가장 단순함 | 모든 line tag를 비교해 비용이 큼 | set 내 way만 비교해 절충함 |
| miss 특성 | conflict miss가 많을 수 있음 | conflict miss가 가장 적음 | 일반 CPU 캐시에서 균형이 좋음 |
| 적용 기준 | 소형·저전력 캐시 | TLB, 작은 victim cache | L1/L2/L3 일반 캐시 |

> 요약: 직접 매핑은 단순성, 완전 연관은 hit rate, 집합 연관은 현실적 균형을 선택함.

## Ⅲ. 구성요소

```text
Address bits:
+----------+----------+----------+
| Tag      | Index    | Offset   |
+----------+----------+----------+
                |
                v
        +---------------+
        | Cache Set     |
        | Way0 Way1 ... |
        +-------+-------+
                |
                v
         tag compare -> hit/miss
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Tag | 선택된 line 또는 way가 요청한 메모리 블록인지 확인하는 식별자임 | 차량 번호 |
| Index | 접근할 cache set 또는 line을 고르는 주소 필드임 | 주차 구역 번호 |
| Offset | cache line 안에서 필요한 byte 또는 word 위치를 고름 | 좌석 번호 |
| Comparator | tag와 valid bit를 비교해 hit 여부를 판단함 | 입장 확인 |
| Replacement state | set이 가득 찼을 때 교체 대상을 고르기 위한 상태 정보임 | 자리 배정 기록 |

> 요약: 캐시 매핑은 주소를 tag, index, offset으로 나누고 선택된 후보에서 tag를 비교해 hit를 판단함.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Address  | --> | Select   | --> | Compare  | --> | Return   |
+----------+     +----------+     +----------+     +----------+
 split bits       set/line         tag/valid        hit or fill
```

1. **주소 분해** - CPU 주소를 tag, index, offset 필드로 나눔
2. **후보 선택** - index가 가리키는 line 또는 set의 way들을 읽음
3. **태그 비교** - valid bit와 tag를 비교해 요청 블록이 캐시에 있는지 판단함
4. **반환·적재** - hit이면 offset 위치 데이터를 반환하고 miss이면 메모리에서 line을 채움

> 요약: 캐시 접근은 주소 분해, 후보 선택, tag 비교, hit 반환 또는 miss fill 순서로 진행됨.

## Ⅴ. 문제점

- **P1 conflict miss**: 직접 매핑에서는 자주 쓰는 여러 블록이 같은 index에 몰리면 반복 교체가 발생함
- **P2 탐색 지연·전력**: 연관도가 높을수록 많은 way comparator가 동시에 동작해 hit latency와 전력이 증가함
- **P3 주소 alias 문제**: 가상 주소 기반 캐시에서는 같은 물리 주소가 다른 index로 들어가는 synonym 문제가 생길 수 있음

> 요약: 매핑 방식은 충돌을 줄일수록 탐색 비용과 주소 관리 복잡도가 증가하는 절충임.

## Ⅵ. 개선방안

- **P1 대응**: N-way set associative, victim cache, skewed associativity로 충돌 miss를 완화함 (확인: conflict miss, hit rate)
- **P2 대응**: way prediction, phased lookup, 적정 associativity 선정으로 전력과 지연을 줄임 (확인: hit latency, energy/access)
- **P3 대응**: physically indexed cache, page coloring, synonym invalidation 정책을 적용함 (확인: alias fault, OS cache 관리)

> 요약: 캐시 매핑 개선은 hit rate와 access latency를 동시에 측정해 연관도를 결정해야 함.

## Ⅶ. 전망

- **발전 방향**: 캐시 매핑은 set associative 기반을 유지하면서 way prediction, adaptive replacement, cache partitioning과 결합해 성능·전력·격리를 함께 다룸
- **기술사적 판단**: L1은 hit latency와 tag 비교 전력, LLC는 hit rate와 공유 공정성을 우선하므로 associativity, line size, index bit 배치를 계층별로 정해야 함; conflict miss, capacity miss, compulsory miss를 분리하고 `MPKI`, hit latency, eviction rate, benchmark별 working set 변화를 측정함; 공유 LLC는 cache timing side channel의 기반이 될 수 있으므로 way partitioning, flush, process 격리 기준을 운영 정책에 포함함
- **기술사 제언**: direct, fully, set associative를 tag/index/offset 주소 해석과 miss 유형에 연결해 설명해야 매핑 선택 근거가 분명해짐
