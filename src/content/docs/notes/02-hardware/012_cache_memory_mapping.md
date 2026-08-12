---
sidebar:
  order: 12
  label: "012. 캐시 메모리 구조: 직접•연관•집합 연관 매핑 (Cache Memory Mapping)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "캐시 메모리 구조: 직접•연관•집합 연관 매핑 (Cache Memory Mapping)"
date: "2026-08-08T12:55:00+09:00"
tags:
  - "notes-hardware"
weight: 12
extra:
  question_no: "012"
  source_status: "기출"
  source_history: "120회, 125회, 131회, 132회, 134회, 135회"
  priority: 85
  priority_note: "반복 기출, 매핑•지역성•적중률 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **캐시 매핑(Cache Mapping)**: 메인 메모리(DRAM)의 물리적 데이터 블록을 고속 캐시 메모리(SRAM)의 특정 라인 위치에 배치하고 적중 여부를 판단하기 위한 주소 변환 알고리즘.
- **캐시 라인(Cache Line / Block)**: 메인 메모리와 캐시 메모리 간 데이터 전송 및 일관성 관리의 기본 블록 단위(일반적으로 64-Byte).
- **태그 비교(Tag Comparison)**: CPU가 요청한 메모리 주소의 Tag 필드와 캐시 라인 태그 메모리에 보관된 비트를 비교기(Comparator) 회로로 대조하여 Cache Hit/Miss를 판정하는 작동.

</details>

- 정의/개념: 메인 메모리의 주소 공간을 고속 캐시 라인 위치로 매핑하고 **태그 비교(Tag Comparison)**를 수행하는 3대 배치 규격(Direct, Fully Associative, Set-Associative) 체계인 **캐시 매핑(Cache Mapping)**.
- 배경/필요성: CPU 연산 속도와 메인 메모리 접근 속도 간의 대극 격차(Memory Wall)를 극복하기 위해, 제한된 SRAM 캐시 용량 내에 최적의 위치 매핑 규칙을 적용하여 캐시 충돌 미스(Conflict Miss)를 최소화할 필요성 대두.

#### 한줄 요약
- 메모리 주소의 Index 필드로 캐시 집합을 고르고 Tag 필드 비교를 통해 Hit/Miss를 판정하는 주소 매핑 및 데이터 배치 구조.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **연관도(Associativity)**: 하나의 메인 메모리 블록이 적재될 수 있는 후보 캐시 라인(Set 내의 Way)의 개수.
- **평균 메모리 접근 시간(Average Memory Access Time, AMAT)**: 적중 시간과 미스 비율, 미스 페널티의 곱으로 계산되는 전체 메모리 참조 지연 지표.
- **충돌 미스(Conflict Miss)**: 동일한 캐시 집합(Set)으로 인덱싱되는 주소가 몰려, 빈 슬롯이 남아있음에도 특정 위치 쫓겨남이 반복되는 미스 현상.
- **웨이(Way)**: 1개 캐시 집합(Set) 내부에서 데이터를 병렬 적재할 수 있는 독립된 캐시 라인 슬롯.
- **적중 시간(Hit Time, $T_{hit}$)**: 캐시 메모리에서 태그를 비교하고 최상위 억세스 데이터를 ALU로 인출하기까지의 시간.
- **미스율(Miss Rate)**: 전체 메모리 요청 중 캐시 적중에 실패하여 하위 캐시나 메인 메모리로 억세스하는 비율.
- **미스 페널티(Miss Penalty)**: 캐시 미스 발생 시 DRAM 메인 메모리로부터 64바이트 라인을 인출해 올 때 소비되는 지연 클록 수.

</details>

- **연관도(Associativity)**가 높을수록 동일 집합으로 주소가 몰릴 때 발생하는 **충돌 미스(Conflict Miss)**가 획기적으로 저감됨.
- **적중 시간($T_{hit}$)**, **미스율(Miss Rate)** 및 **미스 페널티(Miss Penalty)**의 관계에 의해 전체 **AMAT(Average Memory Access Time)** 성능이 산출됨.
- 연관도가 증가할수록 태그 비교기 하드웨어 회로 증가로 인하여 적중 시간이 다소 늘어날 수 있는 무역적 성질(Trade-off) 보유.

$$
AMAT = T_{hit} + (Miss\ Rate \times Miss\ Penalty)
$$

#### 한줄 요약
- 연관도(Associativity)를 상향하여 충돌 미스를 억제하되, AMAT 공식을 기반으로 적중 시간과 태그 비교 회로 오버헤드를 최적 절충함.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **태그(Tag)**: 메모리 주소 상위 비트로 구성되어, 캐시 라인에 들어있는 데이터가 어떤 메인 메모리 블록에서 온 것인지를 정밀 검증하는 식별자.
- **인덱스(Index)**: 메모리 주소 중간 비트로 구성되어, 접근할 캐시 집합(Set) 번호를 다중화 디코더로 선택하는 인덱스 비트.
- **오프셋(Offset)**: 메모리 주소 하위 비트로 구성되어, 64바이트 캐시 라인 블록 내부에서 원하는 1/2/4/8 바이트 데이터를 지시하는 포인터.
- **유효 비트(Valid Bit)**: 해당 캐시 라인에 적재된 데이터가 쓰레기 값이 아닌 유효한 전원/메모리 데이터인지를 지시하는 1비트 상태 플래그.
- **교체 정책(Replacement Policy)**: 모든 Way가 가득 찬 집합에 새 블록을 적재할 때 기존 캐시 라인을 쫓아내는 축출 알고리즘 (LRU, FIFO, Random).
- **태그 탐색부(Tag Lookup Unit)**: N-way 파이프라인 비교기들을 통해 선택된 Set 내부의 N개 Tag를 동시 병렬 대조하는 탐색 로직.
- **데이터 배열(Data Array)**: 실제 64바이트 데이터 블록 사본을 보유하고 적중 시 억세스 딜리버리를 구동하는 SRAM 데이터 배열.

</details>

```text
[ Physical Memory Address Bit Breakdown ]
+----------------------------+-----------------------+---------------------+
|      Tag Bits (20-bit)     |   Index Bits (6-bit)  | Offset Bits (6-bit) |
+----------------------------+-----------------------+---------------------+
                                         │
                                         ▼
                            [ Set Decoder (Select Set) ]
                                         │
                                         ▼
                      [ N-Way Tag Comparators (Parallel) ]
                                         │ Hit / Miss ?
                                         ▼
                             [ Data Array MUX Output ]
```

| 구성요소 | 역할 및 작동 원리 | 차별점 및 실무 유용성 |
|:---|:---|:---|
| **주소 분해기** | CPU 발신 주소를 Tag, Index, Offset 비트로 3등분 파싱 | 라인 크기 64B=6비트 Offset, Set 개수=Index 비트 할당 |
| **태그 탐색부** | Valid Bit=1 이면서 요청 Tag와 저장 Tag가 일치하는 Way 판정 | N-way 병렬 태그 비교기를 가동하여 Cache Hit 여부 즉시 판단 |
| **데이터 배열** | Hit로 판정된 Way의 Data Block 중 Offset 위치 데이터 딜리버리 | CPU 파이프라인으로 연산 피연산자 무지연 즉시 전송 |
| **교체 제어부** | Set 가득 참 발생 시 **LRU(Least Recently Used)** 등으로 축출 결정 | 캐시 적중률 유지 및 공간 오염(Cache Pollution) 최소화 |

#### 한줄 요약
- 주소를 Tag/Index/Offset으로 분해하고 태그 탐색부, 데이터 배열, LRU 교체 제어부를 구동하여 캐시 적중/축출을 제어함.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **캐시 적중(Cache Hit)**: 요청한 메인 메모리 블록이 이미 캐시 메모리 상의 유효한 라인에 존재하여 SRAM에서 무지연 읽어오는 상태.
- **캐시 미스(Cache Miss)**: 요청 블록이 캐시에 없어 상위 계층(DRAM 메인 메모리/하위 캐시)에 접근해 가져와야 하는 상태.
- **축출(Eviction)**: 미스 발생 시 교체 정책(LRU)에 의해 선택된 victim 캐시 라인을 비우는 동작.
- **리fill(Refill)**: 하위 메모리 계층에서 읽어온 64바이트 신규 블록을 비워진 캐시 라인에 래칭 채우는 작업.

</details>

```text
[ CPU Memory Address Access Request ]
                 │
                 ▼
[ 1. Index 비트로 해당 Set 인덱싱 ]
                 │
                 ▼
[ 2. N-Way 병렬 태그 비교 (Valid Bit & Tag Match) ]
                 ├─ [ Cache Hit ] ──> 3. Offset 기반 Data 반환 (Hit Complete)
                 │
                 └─ [ Cache Miss ] ──> 4. LRU 교체 정책으로 Victim Way 선택
                                               │
                                               ▼
                                       5. 하위 메모리에서 64B Refill
                                               │
                                               ▼
                                       6. Tag & Valid Bit 갱신 후 Data 반환
```

### 동작 원리

1. **인덱싱 및 태그 비교**: 메모리 주소의 **Index** 비트로 캐시 집합(Set)을 지시하고, 집합 내 N개 Way의 **Valid Bit** 및 **Tag** 비트를 병렬 회로로 대조함.
2. **Hit 연산**: 일치하는 Way 발견 시 **Cache Hit**로 판정하여 **Offset** 비트 포인터가 지시하는 데이터 바이트를 파이프라인으로 즉시 반환함.
3. **Miss 수습 및 Eviction**: 미스 발생 시 **LRU 교체 정책**으로 축출할 Victim 라인을 정하고, 필요시 Dirty Line을 메모리로 Write-back(Eviction) 함.
4. **Refill 및 갱신**: DRAM 메인 메모리로부터 64바이트 라인을 가져와 **Refill**하고 Tag 및 Valid Bit를 갱신 완료함.

#### 한줄 요약
- Index 선택 -> N-Way Parallel Tag Check -> Hit 시 Data 반환, Miss 시 LRU Eviction 및 Refill 순서로 완결함.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **직접 매핑(Direct Mapping)**: 1개 블록이 오직 1개 정해진 캐시 라인 위치로만 매핑되는 단순 방식 (Set 1개당 Way 1개).
- **완전 연관 매핑(Fully Associative Mapping)**: Index 필드 없이 메인 메모리 블록이 캐시의 임의의 아무 라인에나 들어갈 수 있는 구조.
- **집합 연관 매핑(Set-Associative Mapping)**: 전체 캐시를 여러 Set으로 나누고 각 Set 내에 N개의 Way(2, 4, 8, 16-Way)를 두는 범용 절충 방식.

</details>

| 비교 항목 | 직접 매핑 (Direct Mapped) | 완전 연관 매핑 (Fully Associative) | 집합 연관 매핑 (N-Way Set Associative) |
|:---|:---|:---|:---|
| **배치 위치** | 오직 1개 특정 캐시 라인으로만 고정 | 캐시 내부 임의의 모든 라인에 배치 | 지정된 Set 내의 N개 Way 중 자율 배치 |
| **태그 비교** | 1개 태그만 단일 비교 (속도 최상) | 전체 캐시 라인의 태그 동시 비교 (비용 최상)| N개 Way 태그만 병렬 비교 (속도/비용 절충) |
| **충돌 미스** | 주소 겹침 시 **충돌 미스** 매우 심함 | 충돌 미스 원천 부재 (용량 미스만 존재) | N-Way 수평선 내에서 충돌 미스 대폭 억제 |
| **주소 구조** | Tag + Index + Offset | Tag + Offset (Index 비트 미사용) | Tag + Index + Offset |
| **실무 채택** | L1 명령 캐시 일부, 저가 MCU | TLB(Translation Lookaside Buffer) | 현대 프로세서 L1/L2/L3 캐시 표준 규격 |

#### 한줄 요약
- 직접 매핑(Hit 속도 최상, 충돌 심함), 완전 연관(충돌 없음, 태그 비용 극대), 집합 연관(적중률과 태그 비교 오버헤드의 범용 절충)으로 진화함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **비차단 캐시(Non-Blocking Cache / MSHR)**: 미스 처리 중에도 멈추지 않고 Miss Status Holding Register(MSHR)를 통해 다른 캐시 요청을 계속 가동하는 기술.
- **프리페치(Prefetching)**: 공간/시간 지역성을 분석하여 향후 접근될 데이터를 미스 발생 전에 캐시로 미리 인출하는 기술.
- **Pseudo-LRU (PLRU)**: N-Way 연관도가 높아질 때 완전 LRU의 다이 면적 트래픽 오버헤드를 줄이기 위한 트리 기반의 흉내 내기 교체 정책.
- **주소 배치(Address Placement / Cache Alignment)**: 자료구조 배치 시 캐시 라인 경계(64-Byte Align)에 맞추어 충돌 미스 및 캐시 라인 걸침을 예방하는 코드 최적화.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 특정 캐시 Set으로 주소가 집중되어 심각한 **충돌 미스** 발생 | 8-Way / 16-Way **집합 연관 매핑** 확장 및 코드 **Cache Alignment** | Set 쏠림 완화 및 캐시 적중률 대폭 향상 |
| 연관도 증가 시 태그 비교기 과다로 인한 Hit Latency 및 전력 폭증 | 8-Way 이상에서는 **Pseudo-LRU(PLRU)** 적용 및 Way-Predictor 탑재 | 태그 탐색 동적 전력 소모 저감 및 히트 타임 단축 |
| 캐시 미스 발생 시 CPU 파이프라인 전면 Stall 현상 | **비차단 캐시(Non-Blocking Cache - MSHR)** 및 하드웨어 **프리페치** 적용 | 메모리 억세스 지연시간 파이프라인 우회 은닉 |

#### 한줄 요약
- N-Way Set-Associative, Cache Alignment, Pseudo-LRU 및 Non-Blocking MSHR 프리페치를 적용함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **태그 비교 비용(Tag Comparison Cost)**: N-way 연관도 증설 시 태그 비교기 회로 증가로 수반되는 다이 면적, 적중 지연시간 및 전력 소모 오버헤드.
- **매핑 선택 기준(Cache Mapping Selection Criteria)**: 대상 시스템의 캐시 계층(L1, L2, L3, TLB) 특성에 따라 AMAT를 최저로 만드는 연관도와 구조를 결정하는 공학적 지표.

</details>

- **매핑 선택 기준(Cache Mapping Selection Criteria)**에 근거하여 빠른 접근 속도가 필수적인 L1 캐시에는 4/8-Way 집합 연관 매핑 및 PLRU 정책을 적용하고, 대용량 L3 캐시에는 16-Way 이상의 고연관도 매핑 및 비차단 MSHR 프리페치를 결합하여 AMAT를 극소화하는 캐시 하드웨어 최적화 체계 적용 필수.

#### 한줄 요약
- N-Way Set-Associative 구조를 기반으로 AMAT 최적화를 실현하고 PLRU 및 Non-Blocking Cache를 통합 적용하는 캐시 매핑 체계 적용.
