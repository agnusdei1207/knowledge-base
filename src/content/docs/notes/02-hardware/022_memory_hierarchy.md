---
sidebar:
  order: 22
  label: "022. 메모리 계층 구조 (Memory Hierarchy)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "메모리 계층 구조 (Memory Hierarchy)"
date: "2026-08-13T11:44:27+09:00"
tags:
  - "notes-hardware"
weight: 22
extra:
  question_no: "022"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "속도•용량•비용 절충의 핵심 구조"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **메모리 계층 구조(Memory Hierarchy)**: 프로세서의 처리 속도와 저장장치의 접근 지연시간, 용량, 비트당 비용(Cost per bit) 격차를 완화하기 위해 Register, SRAM Cache, DRAM Main Memory, NVMe SSD를 피라미드 형태로 단계 배치한 저장 아키텍처.
- **지역성(Locality of Reference)**: 프로그램 실행 중 특정 시점에 특정 메모리 주소나 그 인근 주소를 집중하여 반복 참조하는 참조 특성(시간/공간 지역성).

</details>

- 정의/개념: 데이터 참조 **지역성** 기반 접근 속도•용량•비용별 **피라미드 단계화** 구조
- 배경/필요성: **SRAM** 단독 구성 시 면적•비용 증가로 대용량 **무지연 메모리 구현 제약**

#### 한줄 요약
- 참조 지역성을 기반으로 고속/소용량 상위 계층과 저속/대용량 하위 계층을 피라미드로 구성하여 AMAT를 최소화하는 아키텍처 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **시간 지역성(Temporal Locality)**: 최근 접근된 메모리 번지가 가까운 미래에 다시 반복 접근될 확률이 매우 높은 특성 (예: 루프 변수, 함수 호출).
- **공간 지역성(Spatial Locality)**: 특정 메모리 번지가 접근되면 그 인근 인접 번지들이 연속 접근될 확률이 높은 특성 (예: 배열, 순차 기계어 인출).
- **적중률(Hit Rate)**: CPU의 메모리 참조 요청 중 상위 계층 저장장치에서 즉시 발견하여 반환된 횟수 비율.
- **미스율(Miss Rate)**: 상위 계층에 데이터가 없어 하위 계층 메모리로 억세스 요청을 넘기는 비율 ($\text{Miss Rate} = 1 - \text{Hit Rate}$).
- **평균 메모리 접근 시간(Average Memory Access Time, AMAT)**: 전체 계층구조 상에서 1회 메모리 참조 시 평균적으로 소요되는 억세스 시간 지표.
- **미스 페널티(Miss Penalty)**: 상위 계층 미스 발생 시 하위 계층으로부터 블록을 가져올 때 추가 소비되는 지연 클록 수.
- **비트당 비용(Cost Per Bit)**: 1비트의 데이터를 저장 회로로 물리 구현하는 데 소요되는 실리콘 하드웨어 단가 비용.

</details>

- 상위 계층일수록 접근 속도는 빠르나 용량이 작고 **비트당 비용** 고가
- **시간•공간 지역성** 극대화로 최상위 계층 **적중률** 95% 이상 유지
- 상위 계층 적중 시간과 하위 계층 **미스 페널티**로 시스템 **AMAT** 성능 결정

$$
AMAT = Hit\ Time + (Miss\ Rate \times Miss\ Penalty)
$$

#### 한줄 요약
- 시간/공간 지역성을 기반으로 상위 계층 적중률을 극대화하여 시스템 전체 AMAT를 최상위 계층 속도 수준으로 귀결시킴.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **레지스터(Register)**: CPU 코어 내부에서 명령어 피연산자와 상태를 보관하는 최상위 저장 소자.
- **SRAM (Static RAM)**: 캐시 메모리(L1/L2/L3)로 사용되며 전원 공급 중 복사나 리프레시 없이 1~10ns 저지연을 제공하는 고속 반도체.
- **DRAM (Dynamic RAM)**: 주기억장치(Main Memory)로 사용되며 1트랜지스터 1커패시터 구조로 주기적 Refresh가 필요하나 고밀도 용량을 제공하는 반도체.
- **SSD / Flash Memory**: 비휘발성 보조기억장치로 가상 메모리 스왑 영역 및 영구 데이터 파일 시스템을 보관하는 하위 계층.

</details>

```text
[ Memory Hierarchy Structure ]
 ┌─────────────────────────────────────────┐
 │ 레지스터 (Registers)                    │ High Speed / High Cost
 ├─────────────────────────────────────────┤ Low Capacity
 │ L1/L2/L3 캐시 (Cache)                   │
 ├─────────────────────────────────────────┤
 │ 주기억장치 (Main Memory)                │
 ├─────────────────────────────────────────┤ Low Speed / Low Cost
 │ 보조기억장치 (Storage)                  │ High Capacity
 └─────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 레지스터 | 현재 명령의 **피연산자•상태** 보관 |
| L1•L2•L3 캐시 | 최근 블록의 **저지연 재사용** 제공 |
| 주기억장치 | 실행 중 페이지의 **대용량 저장** 제공 |
| 보조기억장치 | 파일•비상주 데이터의 **비휘발 보관** |

#### 한줄 요약
- Register(CPU), L1/L2/L3 Cache(SRAM), Main Memory(DRAM), Storage(Flash SSD)의 4단계 계층으로 구성됨.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **캐시 블록(Cache Block / Line)**: DRAM 메인 메모리에서 SRAM 캐시 메모리로 한 번에 묶어서 전송 및 교체하는 64바이트 단위 전송 블록.
- **비상주 페이지(Non-Resident Page)**: 가상 메모리 주소 상에는 존재하지만 물리 DRAM에 없어 SSD 보조기억장치로부터 로드해야 하는 페이지.

</details>

```text
[ CPU Memory Access Instruction ]
                 │
                 ▼
[ 1. L1 조회 ] ──(Hit)──> Data Return
                 │ (Miss)
                 ▼
[ 2. L2•L3 조회 ] ──(Hit)──> Refill L1 & Data Return
                 │ (Miss)
                 ▼
[ 3. DRAM 조회 ] ──(상주)──> Refill Caches & Data Return
                 │ (Miss - Page Fault)
                 ▼
[ 4. 저장장치 Page-In ] ──> Refill DRAM & Caches
```

### 동작 원리

1. **L1 조회**: 최상위 캐시 적중 시 요청 데이터를 반환함.
2. **L2•L3 조회**: L1 미스 시 하위 캐시를 탐색하고 블록을 보충함.
3. **DRAM 조회**: 캐시 미스 시 DRAM에서 캐시 라인을 인출함.
4. **저장장치 Page-In**: **비상주 페이지**이면 Page Fault 후 적재함.

#### 한줄 요약
- L1->L2->L3->DRAM->SSD 순으로 상위 계층 미스 시 하위 계층으로 억세스가 전파되며 블록 단위로 상위 계층에 Refill됨.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **작업 집합(Working Set)**: 프로그램이 특정 구동 구간에서 시간/공간 지역성에 의해 집중적으로 반복 참조하는 페이지 및 데이터 영역.
- **반복 교체(Thrashing / Cache Pollution)**: 작업 집합 크기가 상위 캐시 용량을 초과하여 인출된 블록이 재사용되기도 전에 축출되는 슬래싱 현상.

</details>

| 비교 항목 | 상위 메모리 계층 (Register / SRAM Cache) | 하위 메모리 계층 (DRAM Main Mem / Flash SSD) |
|:---|:---|:---|
| **물리적 위치** | 온칩(On-Chip) CPU 코어 내부 집적 | 온보드(On-Board) 또는 외부 핀/인터커넥트 결합 |
| **억세스 속도** | 극도로 빠름 (Sub-nanosecond ~ 몇 ns) | 상대적 느림 (수십 나노초 ~ 수십 마이크로초) |
| **비트당 비용** | 매우 비쌈 (단위 용량당 가격 최대) | 경제적 저렴함 (대용량 저가 구축 가능) |
| **데이터 유지** | **작업 집합** 집중 적재 관리 | 전역 코드, 파일 데이터 및 **비상주 페이지** 적재 |
| **용량 부족 시** | **반복 교체** 수반 | 디스크 스왑 및 **Page Fault I/O** 발생 |

#### 한줄 요약
- 상위 계층은 극도의 속도와 지역성 기반 Working Set 재사용에 집중하고, 하위 계층은 대용량 데이터 보존과 경제적 저가 구축에 집중함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **캐시 블로킹(Cache Blocking / Tiling)**: 대용량 행렬 연산 시 데이터를 L1/L2 캐시 용량에 딱 맞는 소형 블록(Tile) 단위로 나누어 루프를 재구성함으로써 공간/시간 지역성을 극대화하는 알고리즘 최적화 기법.
- **선인출(Hardware Prefetching)**: 주소 접근 패턴을 예측하여 다음 읽을 캐시 라인을 CPU가 미리 DRAM에서 상위 캐시로 당겨오는 기법.
- **캐시 오염(Cache Pollution)**: 일회성 대용량 전수 스트리밍 데이터가 들어와 자주 쓰이는 상위 캐시의 유용한 Working Set 라인들을 싹 밀어내 버리는 현상.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 대용량 2차원 행렬 연산 시 캐시 크기 초과로 **반복 교체** 발생 | 루프 재구성을 통한 **캐시 블로킹** 최적화 | L1/L2 캐시 적중률 대폭 향상 및 AMAT 지연 감소 |
| 스트리밍 데이터 무작위 로드로 인한 **캐시 오염** | Non-Temporal Store (`_mm_stream_si128`) 및 **선인출** 강도 조절 | 유용한 Working Set 라인의 캐시 유지 및 오염 차단 |
| DRAM 메모리 억세스 지연(60ns)으로 인한 파이프라인 Stall | 하드웨어 **스트라이드 선인출** 내장 및 MSHR 확장 | DRAM 읽기 지연시간 파이프라인 우회 은닉 |
| 대용량 데이터의 계층 간 전송 대역폭 병목 | 고대역폭 메모리 **HBM (High Bandwidth Memory)** 탑재 | 메모리 버스 대역폭 1TB/s 이상으로 대폭 확충 |

#### 한줄 요약
- Cache Blocking(Tiling), Non-Temporal Stream(Cache Pollution 방지), Hardware Prefetching 및 HBM 도입을 연동함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **메모리 계층 설계 기준(Memory Hierarchy Selection Criteria)**: 대상 시스템의 컴퓨터 워크로드 특성(Single-thread, AI Tensor, DB I/O)과 캐시 적중률, AMAT 목표를 수립하여 계층별 용량 배분을 정형화하는 아키텍처 가이드라인.

</details>

- 재사용률이 높으면 **캐시 용량•Blocking**, 대역폭 병목이면 **Prefetch•HBM** 확대

#### 한줄 요약
- AMAT 구성 요인을 측정하여 계층 용량과 데이터 이동 정책을 결정함.
