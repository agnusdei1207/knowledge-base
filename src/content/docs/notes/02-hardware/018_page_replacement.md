---
sidebar:
  order: 18
  label: "018. 페이지 교체 알고리즘: OPT•FIFO•LRU•LFU (Page Replacement)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "페이지 교체 알고리즘: OPT•FIFO•LRU•LFU (Page Replacement)"
date: "2026-08-13T11:39:57+09:00"
tags:
  - "notes-hardware"
weight: 18
extra:
  question_no: "018"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "교체 기법 선택과 벨라디 이상 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **페이지 교체(Page Replacement)**: 요구 페이징(Demand Paging) 기법에서 물리 메모리(DRAM Frame)가 가득 차 새로운 페이지를 적재할 공간이 없을 때, 물리 메모리 상의 기존 페이지 중 희생 페이지(Victim Page)를 선택하여 축출하는 알고리즘.
- **희생 페이지(Victim Page)**: 새로 요청된 페이지를 적재할 물리 프레임 공간을 확보하기 위해 축출 대상으로 선택되는 페이지.
- **페이지 폴트(Page Fault)**: 접근하려는 가상 페이지가 물리 메모리에 없어(Present Bit=0) 하드웨어가 OS 커널 예외 핸들러를 호출하는 트랩.
- **입출력(Input/Output, I/O)**: 희생 페이지 축출 시 Dirty Page인 경우 SSD 스왑 영역으로 덮어쓰고, 요청 페이지를 로드하는 저장장치 대기 작업.

</details>

- 정의/개념: 요구 페이징 시스템에서 물리 메모리 프레임이 포화 상태일 때, 향후 접근 확률이 가장 낮은 **희생 페이지**를 선택하여 축출하고 신규 가상 페이지를 적재하는 **페이지 교체 알고리즘**.
- 배경/필요성: 잘못된 희생 페이지를 선택하면 가까운 미래에 동일 페이지를 다시 억세스하여 **페이지 폴트**와 고비용 SSD 스왑 **I/O**가 폭증(Thrashing)하므로, 지역성 기반의 희생 알고리즘 필수 적용.

#### 한줄 요약
- 물리 프레임 포화 시 미래 재참조 확률이 가장 적은 희생 페이지를 선택 축출하여 페이지 폴트 비율을 최소화하는 메모리 교체 정책.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **참조 지역성(Reference Locality)**: 최근 참조된 페이지가 가까운 미래에 다시 참조되는 시간 지역성(Temporal Locality)과, 근접 주소가 참조되는 공간 지역성(Spatial Locality).
- **참조 이력(Reference History)**: 캐시/페이지 관리자가 희생 페이지를 결정하기 위해 보관하는 가상 페이지 접근 시각, 횟수, 적재 순서, 참조 비트(Reference Bit) 데이터.
- **더티 페이지(Dirty Page)**: 메모리 상에서 값이 변경(Dirty Bit=1)되어 희생 페이지로 축출될 때 반드시 SSD/HDD 스왑 영역으로 덮어써야 하는 페이지.
- **교체 예측력(Replacement Prediction Accuracy)**: 참조 이력을 바탕으로 향후 불필요할 희생 페이지를 정확히 집어내는 예측 확률.

</details>

- **참조 지역성** 정보를 기반으로 향후 재참조 가능성이 가장 낮은 희생 페이지 선택.
- 알고리즘이 정교해질수록 **교체 예측력**은 상향되나, 매 억세스마다 태그/시각을 업데이트하는 **갱신 비용**이 증가.
- 축출 대상이 **더티 페이지**일 경우, 단순 파기가 아닌 SSD 스왑 영역 저장 쓰기 I/O 오버헤드가 추가 수반됨.

#### 한줄 요약
- 참조 지역성을 반영하여 희생 페이지를 선정하며, 알고리즘 정밀도와 하드웨어 갱신 오버헤드 간의 상충 관계를 가짐.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **상주 프레임 집합(Resident Frame Set)**: 현재 물리 RAM의 페이지 프레임에 적재되어 유효하게 구동 중인 가상 페이지들의 목록.
- **후면 저장소(Backing Store / Swap Space)**: 물리 RAM에서 축출된 페이지나 미상주 페이지 데이터를 저장 보관하는 SSD 스왑 파일 영역.
- **저장소 I/O(Storage I/O)**: Dirty Victim Page의 스왑 쓰기 및 신규 요청 페이지의 스왑 읽기를 처리하는 입출력 경로.

</details>

```text
[ Page Replacement Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Resident Frame Set (Physical RAM Frames: F0, F1, F2, F3)  │
│  - Reference History : Access Bit, Time Tag, Frequency    │
├───────────────────────────────────────────────────────────┤
│ Replacement Selector (OPT / FIFO / LRU / LFU Engine)     │
│  - Select Victim Frame (e.g., Frame F2)                   │
├───────────────────────────────────────────────────────────┤
│ Storage I/O Subsystem                                     │
│  - If Dirty (Bit=1) : Swap Out (F2 -> SSD Backing Store)  │
│  - Request Page    : Swap In  (SSD -> F2 Frame)           │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 상주 프레임 집합 | 페이지의 **Valid•Dirty 상태** 관리 |
| 참조 이력 매핑 | **시각•횟수•참조 비트** 기록 |
| 교체 선택기 | 정책에 따라 **희생 프레임** 결정 |
| 저장소 I/O | Dirty 축출과 요청 페이지 **입출력** 수행 |

#### 한줄 요약
- Resident Frame Set, Reference History Tracker, Replacement Selector Engine 및 Storage I/O 유닛이 유기적으로 연동함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **페이지 폴트 처리기(Page Fault Handler)**: 비상주 페이지 접근 예외 수신 시 물리 프레임 확보 및 페이지 교체 프로세스를 총괄하는 커널 루틴.
- **원자 갱신(Atomic Update)**: 희생 페이지 축출 및 신규 페이지 적재 완료 시까지 중간 불일치 상태가 타 스레드에 노출되지 않도록 PTE를 원자적으로 수정하는 연산.

</details>

```text
[ Non-Resident Page Fault Occurred ]
                 │
                 ▼
[ Free Physical Frame Exist Check ]
  ├─ Free Frame Exist ──> [ Direct Page-In New Page ]
  │
  └─ Free Frame None (RAM Full)
        │
        ▼
   Replacement Selector 구동 (Reference History 기반 Victim 선정)
        │
        ▼
   Victim Page Dirty Bit Check
        ├─ Dirty Bit = 1 : Swap-Out (SSD 스왑 영역에 쓰기 I/O)
        └─ Dirty Bit = 0 : No Write (즉시 Frame 파기)
        │
        ▼
   Request Page-In to Free Frame
        │
        ▼
   PTE Atomic Update & Instruction Restart
```

### 동작 원리

- **프레임 점검**: 빈 프레임이 없으면 교체 선택기를 구동함.
- **희생 페이지 선정**: **참조 이력**으로 축출할 프레임을 선택함.
- **Dirty 처리**: Dirty이면 저장하고 Clean이면 즉시 재사용함.
- **Page-In•갱신**: 요청 페이지 적재 후 PTE 갱신과 명령 재시작 수행

#### 한줄 요약
- 빈 프레임 확인 -> 희생 페이지 선택 -> Dirty 확인 후 Swap-out -> 신규 페이지 Swap-in 및 PTE 원자 갱신 순서로 실행됨.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **최적 교체(Optimal, OPT / MIN)**: 미래에 가장 오랫동안 사용되지 않을 페이지를 쫓아내는 이론상 최상의 알고리즘 (미래 예지 필요로 실현 불가능).
- **선입선출(First-In First-Out, FIFO)**: 메모리에 가장 먼저 적재된 페이지를 순서대로 축출하는 단순 알고리즘.
- **최소 최근 사용(Least Recently Used, LRU)**: 가장 오랫동안 참조되지 않은(가장 과거에 참조된) 페이지를 축출하는 시간 지역성 기반 알고리즘.
- **최소 빈도 사용(Least Frequently Used, LFU)**: 과거 참조 횟수(Frequency Counter)가 가장 적은 페이지를 축출하는 알고리즘.
- **벨라디의 이상(Bélády's Anomaly)**: FIFO 알고리즘에서 물리 프레임 수를 늘려주었음에도 불구하고 오히려 페이지 폴트 횟수가 늘어나는 아노말리 현상.

</details>

| 교체 알고리즘 | 최적 교체 (OPT) | 선입선출 (FIFO) | 최소 최근 사용 (LRU) | 최소 빈도 사용 (LFU) |
|:---|:---|:---|:---|:---|
| **희생 판단 기준** | 미래에 가장 늦게 참조될 페이지 | 가장 먼저 RAM에 적재된 페이지 | 가장 오래전 참조된 페이지 | 과거 참조 횟수가 가장 적은 페이지 |
| **실현 가능성** | **불가능** (미래 참조열 사전 인지 불가) | 가능 (큐 구조 구현) | 가능 (스택/타임스탬프 하드웨어) | 가능 (참조 카운터 보관) |
| **페이지 폴트율** | 최저 (이론적 하한선 제공) | 높음 | 낮음 (대중적 우수) | 보통 (초기 대량 참조 잔존 오류) |
| **이상 현상** | 발생 안 함 | **벨라디의 이상(Bélády)** 발생 | 발생 안 함 (Inclusion Property) | 발생 안 함 |
| **실무 위치** | 교체 정책의 이론적 비교 기준 | 단순 정책의 교육•제한적 구현 | Clock 등 근사 정책의 기준 | 캐시별 빈도 기반 정책에 활용 |

#### 한줄 요약
- 이론상 최상인 OPT, 벨라디의 이상이 발생하는 FIFO, 시간 지역성 기반의 대중적 LRU, 참조 횟수 기반의 LFU로 구분됨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Clock 알고리즘 (Second Chance Algorithm)**: LRU의 높은 카운터/타임스탬프 갱신 오버헤드를 줄이기 위해, 1비트 참조 비트(Reference Bit)와 원형 큐 포인터로 2차 기회를 부여하는 대표적 LRU 근사 하드웨어 알고리즘.
- **백그라운드 기록(Background Writeback)**: 교체 정지 지연을 줄이도록 Dirty Page를 백그라운드 커널 스레드가 미리 저장하는 기술.
- **카운터 감쇠(Counter Decay)**: LFU 사용 시 과거 초기에 대량 참조된 페이지가 더 이상 쓰이지 않아도 메모리를 점유하는 문제를 막기 위해 주기적으로 카운터를 반감시키는 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| pure LRU 구현 시 매 억세스마다 시각 기록에 따른 하드웨어 갱신 전력 폭증 | 1비트 Reference Bit 기반 **Clock 알고리즘(Second Chance)** 적용 | 하드웨어 갱신 오버헤드 극소화 및 LRU 유사 성능 보장 |
| FIFO 알고리즘 적용 시 프레임 증가에도 폴트가 늘어나는 **벨라디의 이상** | Stack Algorithm 성질을 갖는 **LRU** 또는 **Clock** 알고리즘 적용 | 벨라디 이상 현상 원천 차단 |
| LFU 적용 시 초기 대량 접근 데이터가 퇴출되지 않는 현상 | 일정 시간 마다 카운터를 삭감하는 **카운터 감쇠** 연동 | 과거 참조 데이터 오염 방지 및 최신 지역성 반영 |
| Dirty Page 축출 시 동기식 디스크 I/O로 인한 파이프라인 정지 | 커널 차원의 **백그라운드 비동기 기록** 가동 | 페이지 교체 시 동기 I/O 대기시간 은닉 |

#### 한줄 요약
- Clock 알고리즘(LRU 근사), Counter Decay(LFU 보정), Background Writeback 및 Stack Algorithm 유지를 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **페이지 교체 선택 기준(Page Replacement Selection Criteria)**: 대상 워크로드의 참조 지역성, 하드웨어 갱신 비용, 벨라디 이상 차단 여부 및 동기 I/O 지연을 평가하여 최적의 교체 엔진을 선정하는 지표.

</details>

- 갱신 비용이 크면 **Clock**, 빈도 편향이 크면 **감쇠 LFU** 선택.

#### 한줄 요약
- 참조 지역성과 Dirty I/O 지연을 기준으로 교체•Writeback 정책을 결정함.
