---
sidebar:
  order: 22
  label: "022. I/O 관리•디스크 스케줄링"
  badge:
    text: "미출 · 50%"
    variant: note
title: "I/O 관리•디스크 스케줄링 (I/O Management Disk Scheduling)"
date: "2026-08-26T16:35:00+09:00"
tags:
  - "notes-software"
weight: 22
extra:
  question_no: "022"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "I/O 큐•디스크 스케줄링 지연 설계 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **디스크 스케줄링(Disk Scheduling)**: 물리적 스토리지의 접근 지연을 최소화하기 위해 I/O 요청 큐의 순서를 재정렬(Sorting)하고 인접 블록을 병합(Merging)하는 커널 기법.
- **탐색 시간(Seek Time)**: HDD에서 읽기/쓰기 헤드가 대상 트랙(실린더)으로 물리 이동하는 데 걸리는 시간.

</details>

- 정의/개념: 저장 매체의 특성에 맞추어 I/O 요청을 재정렬(Sorting) 및 병합(Merging)하여 접근 지연을 최소화하는 **디스크 스케줄링** 메커니즘
- 배경/필요성: HDD는 요청마다 헤드를 물리적으로 이동시켜 탐색 시간이 전체 응답을 지배하는 비용이 되므로, 요청을 도착순 그대로 내리지 않고 실린더 위치 기준으로 재배열하는 디스크 스케줄링 계층을 I/O 큐에 두어 총 헤드 이동 거리를 줄일 필요

#### 한줄 요약
- I/O 요청을 병합·정렬하여 기계적 탐색 시간을 줄이고 미디어 특성에 맞춘 처리량을 확보한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **회전 지연(Rotational Latency)**: 헤드가 트랙에 도달한 후 플래터가 회전하여 대상 섹터가 헤드 아래로 올 때까지 걸리는 시간.
- **blk-mq(Multi-Queue Block Layer)**: 멀티코어 환경에서 CPU 코어별 소프트웨어 큐와 하드웨어 큐를 매핑하여 수백만 IOPS를 처리하는 리눅스 블록 계층.

</details>

- HDD의 물리적 병목인 **탐색 시간(Seek Time) 및 회전 지연(Rotational Latency)** 최소화
- 인접 블록 요청을 묶는 **요청 병합(Merging)** 및 헤드 이동 경로 기반 **정렬(Sorting)**
- 플래시/NVMe SSD 환경에서는 헤드 스케줄링 대신 **다중 큐(blk-mq)** 기반 병렬 처리 극대화

#### 한줄 요약
- HDD는 헤드 탐색 거리를 최소화하고, SSD는 멀티 큐 병렬 처리로 지연을 없앤다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **BIO(Block I/O) 구조체**: 리눅스 커널에서 블록 디바이스로 전달되는 I/O 요청의 메모리 세그먼트와 LBA 주소를 담은 기본 데이터 단위.

</details>

```text
[블록 I/O 계층 및 디스크 스케줄러 구조]
|-- VFS (가상 파일 시스템) -> 블록 I/O 계층 (BIO Layer)
|-- 디스크 스케줄러 계층
|   |-- 단일 큐 / HDD 경로: I/O 요청 큐 (Request Queue)
|   |   |-- 블록 병합기 (Request Merging: Front/Back Merge)
|   |   `-- 엘리베이터 정렬기 (SCAN / C-LOOK / BFQ)
|   `-- 멀티 큐 / NVMe 경로: blk-mq 레이어
|       |-- CPU 코어별 소프트웨어 스테이징 큐 (Software Queue)
|       `-- 하드웨어 제출/완료 큐 (Hardware Submission/Completion Queue)
`-- 디바이스 드라이버 & 물리 스토리지 컨트롤러 (HDD / NVMe SSD)
```

선의 의미: 계층 및 단일/멀티 큐 디스크 스케줄링 구조

| 구성요소 | 책임 |
|:---|:---|
| I/O 요청 큐 | 블록 요청의 **버퍼링·재배치** |
| 블록 병합기 | 연속 LBA 요청의 **단일 트랜잭션 통합** |
| 엘리베이터 스케줄러 | **C-LOOK·SCAN 기반 정렬** |
| blk-mq 멀티 큐 | NVMe 요청의 **하드웨어 큐 디스패치** |

#### 한줄 요약
- 병합기와 정렬기가 블록 계층에 놓여 상위 요청 순서와 실제 장치 접근 순서를 분리하므로, 장치 특성이 바뀌면 이 계층의 정책만 교체하면 된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Front/Back Merge**: 신규 I/O 요청이 기존 큐에 대기 중인 요청의 바로 앞이나 뒤 섹터에 연속될 때 단일 요청으로 합치는 최적화.

</details>

```text
블록 I/O 쓰기/읽기 요청 인입 (submit_bio)
        │
   인접 섹터 블록이 존재하는가? -> 존재 시 즉시 병합(Request Merging)
        │
   스토리지 미디어 유형에 따른 스케줄링 분기
   ┌────┴───────────────────────────┐
[회전형 HDD: C-LOOK 스케줄러]     [반도체 NVMe SSD: none / mq-deadline]
트랙 번호 순으로 정렬(Sorting)      정렬 생략 후 blk-mq 소프트웨어 큐 거쳐
단방향 엘리베이터 이동              하드웨어 Submission Queue로 즉시 전달
   │                                │
   └────┬───────────────────────────┘
        │
   디바이스 드라이버가 물리 스토리지 컨트롤러에 명령어 전달
        │
   하드웨어 I/O 완료 인터럽트 수신 후 대기 프로세스 Wakeup
```

#### 한줄 요약
- 병합은 요청 수를, 정렬은 헤드 이동을 줄이지만 탐색이 없는 NVMe에서는 정렬 이득이 사라지므로, 미디어별 분기가 이 차이를 흡수한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **C-LOOK(Circular LOOK)**: 헤드가 한 방향으로만 이동하며 요청을 처리하고 끝단 도달 시 시작점으로 즉시 점프하여 대기시간을 균일화하는 HDD 스케줄러.

</details>

| 알고리즘 | FCFS | SSTF | SCAN·C-LOOK | none·mq-deadline |
|:---|:---|:---|:---|:---|
| 적용 기준 | 단순 요청 처리 | 평균 탐색 우선 | 회전형 HDD | SSD·NVMe |
| 핵심 특징 | **도착 순서 처리** | **최단 거리 우선** | **엘리베이터 정렬** | **멀티큐·기한 보장** |
| 한계 | 긴 평균 탐색 | 끝단 요청 기아 | 헤드 이동 비용 | HDD 탐색 최적화 부재 |

#### 한줄 요약
- HDD 환경은 균일 대기시간의 C-LOOK, 플래시/NVMe 초고속 환경은 none 및 mq-deadline을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tail Latency(꼬리 지연시간)**: 대량의 쓰기 I/O로 인해 특정 읽기 I/O가 큐에서 장시간 지연되는 P99/P99.9 지연 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NVMe SSD에 복잡한 HDD 스케줄러 적용 시 CPU 락 병목 | 스케줄러를 **`none`(No-op) 또는 `mq-deadline`** 으로 설정 | CPU 오버헤드 제거 및 100만 IOPS 병렬 처리 지원 |
| 대용량 배치 쓰기로 인한 **읽기 요청 지연(Tail Latency)** | **`mq-deadline` 튜닝(read_expire: 100ms, write_expire: 2s)** | 대화형 읽기 요청 우선 처리 및 지연시간 안정화 |
| HDD 환경에서 특정 프로세스의 I/O 독점으로 인한 기아 | 프로세스별 I/O 가중치를 부여하는 **`bfq`(Budget Fair Queueing)** 적용 | 프로세스 간 I/O 대역폭 공정 분배 |
| 스토리지 I/O 부하 모니터링 미흡 | `iostat -xz 1` 기반 **`%util`, `await`, `svctm`** 지표 실시간 감시 | I/O 포화도 파악 및 조기 병목 해소 |

#### 한줄 요약
- 디스크 스케줄링의 이득은 탐색 시간이 지배적일 때만 존재하므로, HDD에서는 mq-deadline·bfq로 재배열과 공정성을 얻고 탐색이 없는 NVMe에서는 none으로 스케줄링 오버헤드 자체를 없앤다.

## Ⅶ. 결론

- HDD는 **C-LOOK/BFQ**, NVMe는 **blk-mq/none** 선택

#### 한줄 요약
- 디스크 스케줄링은 미디어의 물리적 구조(회전체 vs 플래시)에 맞춘 최적화 전략을 선택함으로써 I/O 병목을 완벽히 해소한다.
