---
sidebar:
  order: 22
  label: "022. I/O 관리•디스크 스케줄링 (I/O Management Disk Scheduling)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "I/O 관리•디스크 스케줄링 (I/O Management Disk Scheduling)"
date: "2026-08-13T13:47:00+09:00"
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

<details><summary>핵심 용어</summary>

- **Disk Scheduling (디스크 스케줄링)**: OS 커널 및 I/O subsystem이 디스크 I/O 요청 큐(Request Queue) 상의 억세스 요청 순서를 정렬/조율하여, HDD 헤더의 탐색 시간(Seek Time) 및 SSD의 I/O 지연시간을 최적화하는 스케줄링.
- **Seek Time (탐색 시간)**: HDD 헤드가 목표 트랙까지 이동하는 데 걸리는 기계적 지연시간.

</details>

- 정의/개념: 저장 매체(HDD/SSD/NVMe) 물리 특성에 따라 I/O Request 큐의 정렬 및 병합(Merging) 제어를 통해 탐색 지연 최소화 및 I/O 스루풋을 극대화하는 **I/O 관리 & 디스크 스케줄링**
- 배경/필요성: 도착 순서 처리는 HDD 탐색 증가와 **다중 큐 병렬성 저하** 가능

#### 한줄 요약

- 장치 특성별 입출력 요청을 제어하는 입출력 스케줄러가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Rotational Latency (회전 지연시간)**: 헤드가 트랙에 안착한 후, 디스크 플래터가 회전하여 원하는 섹터가 헤드 바로 아래에 도달할 때까지의 대기시간.
- **blk-mq (Multi-Queue Block I/O Layer)**: 현대 Linux 커널 상에서 코어별/하드웨어 큐별로 분할하여 NVMe 초고속 병렬 I/O를 지원하는 다중 큐 블록 I/O 서브시스템.

</details>

- 헤드 탐색 시간(**Seek Time**) 및 회전 지연(**Rotational Latency**) 최소화 (HDD)
- 큐 병합•정렬로 HDD 헤드의 불필요한 왕복 이동 완화
- 현대 NVMe/SSD 장치 전용 초고속 병렬 서브시스템 적용 (**blk-mq**)

#### 한줄 요약

- HDD는 탐색 비용, SSD와 NVMe는 병렬성 중심이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Elevator Algorithm (엘리베이터 알고리즘)**: SCAN/LOOK 알고리즘처럼 디스크 헤드가 한쪽 방향 끝까지 스위핑 이동하며 중간에 만나는 요청을 순차 처리하는 방식.

</details>

```text
+---------------- [요청 큐] ----------------+
|                                            |
|                                            |
[완료 처리기]                    [I/O 스케줄러]
|                                            |
|                                            |
+-------------- [장치 드라이버] -------------+
```

선의 의미: 프로세스의 I/O Request가 블록 계층의 Request Queue로 수용되어 I/O 스케줄러(SCAN/BFQ/Kyber) 정렬 후 디스크 드라이버로 전달되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Request Queue | VFS 서브시스템으로부터 하달된 읽기/쓰기 BIO 구조체 보관 |
| I/O Scheduler | **Seek Time** 최소화 정렬(SSTF/SCAN) 및 **Fairness/Latency** 보장 (BFQ/Kyber) |
| Device Driver | 블록 요청을 장치 명령으로 변환해 저장장치에 제출 |
| Completion Handler | I/O 연산 완료 인터럽트 수신 시 대기 프로세스를 **Ready State**로 Wakeup |

#### 한줄 요약

- 요청 큐, 장치 드라이버, 완료 처리기의 순환 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Request Merging & Sorting**: I/O 스케줄러가 인접한 디스크 블록 요청을 1개의 큰 요청으로 합치고(Merging), 트랙 순서로 재정렬(Sorting)하는 처리.

</details>

```text
┌──────────────────────────────┐
│ 입출력 요청                 │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 요청 큐 등록            │
│ 2. 병합•제출 대상 선택     │
│ 3. 장치 명령 변환          │
│ 4. 장치 실행•완료 게시     │
│ 5. 완료 반영•작업 재개     │
└──────────────────────────────┘
```

### 동작 원리

1. **요청 큐 등록**: 프로세스의 디스크 I/O 요청(BIO) 수용 및 **Request Queue** 보관.
2. **병합·제출 대상 선택**: 인접 섹터 요청 **Merging** 및 탐색 시간 최소화 방향 **Sorting** 디스패치.
3. **장치 명령 변환**: 장치 드라이버를 통해 컨트롤러 명령(SATA/NVMe Command) 인가.
4. **장치 실행·완료 게시**: 저장 매체의 물리 쓰기/읽기 구동 및 완료 인터럽트/Completion Queue 게시.
5. **완료 반영·작업 재개**: 페이지 캐시 갱신 및 Blocked 프로세스 깨움 완결.

#### 한줄 요약

- 병합•제출 대상 선택부터 완료 반영•작업 재개까지의 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **SSTF (Shortest Seek Time First)**: 현재 헤드 위치에서 탐색 거리가 가장 가까운 요청을 무조건 먼저 처리하는 방식으로, 기아(Starvation) 발생 가능.
- **SCAN / C-SCAN**: 헤드가 디스크 한쪽 끝에서 반대쪽 끝으로 이동하며 처리(SCAN), 또는 한쪽 방향으로만 이동하며 처리 후 원위치 복귀(C-SCAN).
- **BFQ / Kyber**: 최신 Linux 커널 스케줄러로, Process별 공정 대역폭 보장(BFQ) 및 latency 타깃 설정 기반 NVMe 스케줄링(Kyber).

</details>

| 스케줄링 알고리즘 | 동작 방식 | 주요 특징 및 평가 |
|:---|:---|:---|
| **FCFS** | 도착 순서대로 처리 | 단순함 / 요청 분포에 따라 탐색 증가 |
| **SSTF** | 현재 헤드 최단 거리 우선 처리 | 탐색 시간 감소 / 외곽 실린더 요청의 **Starvation** 유발 |
| **SCAN / C-SCAN** | 끝에서 끝으로 **Elevator Sweep** 이동 | 기아 예방 및 응답시간 균일화 / 양끝 편향 |
| **LOOK / C-LOOK** | 마지막 요청 위치에서 이동 방향 전환 | 디스크 끝까지의 불필요한 이동 감소 |
| **Kyber / BFQ** | 다중 큐 기반 지연 또는 공정성 조율 | 장치•워크로드별 정책 차이 |

#### 한줄 요약

- HDD 탐색과 NVMe 병렬성에 맞춰 FCFS, SCAN, 데드라인 스케줄링, 멀티큐를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **none / mq-deadline / bfq**: Linux 커널 블록 계층 마운트 옵션으로, SSD/NVMe는 `none` 또는 `mq-deadline`, HDD는 `bfq` 선택권 제공.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SSD/NVMe 장치 상에서 전통적 SCAN/SSTF 스케줄링 적용 시 CPU 오버헤드 유발 | 스케줄러를 **none** (No-op) 또는 **mq-deadline**으로 설정 | SSD 디스크 병렬 I/O 가속 |
| 대용량 HDD 상에서 바깥쪽 트랙 요청의 **Starvation** | **C-LOOK** 또는 **BFQ** 스케줄러 적용 | 기아 현상 예방 및 대역폭 공정성 |
| 읽기(Read) 요청이 쓰기(Write) 요청에 밀려 대기 지연 | Read 큐 우선순위 격상 및 타임아웃 세팅 | 애플리케이션 응답속도 보장 |

> 사례: Linux 커널 `sys/block/nvme0n1/queue/scheduler` 값을 `none`으로 튜닝하여 NVMe 스루풋 최적화

#### 한줄 요약

- 큐 깊이, 공정성, 인터럽트 병합 기반 운영이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **디스크 스케줄러 선택 기준(Disk Scheduler Selection Criteria)**: 저장 매체 타입(HDD vs SSD vs NVMe), I/O 큐 깊이 및 응답시간 타깃에 기반한 튜닝 체계.

</details>

- HDD 탐색•공정성은 **C-LOOK/BFQ**, NVMe는 **none/mq-deadline** 검증

#### 한줄 요약

- 탐색 비용•기한•병렬성을 함께 평가하는 것이 핵심이다.
