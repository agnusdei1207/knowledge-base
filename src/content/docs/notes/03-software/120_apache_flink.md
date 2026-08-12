---
sidebar:
  order: 120
  label: "120. Apache Flink 스트림 처리 (Apache Flink)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 120
extra:
  question_no: "120"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "Flink 상태•이벤트시간 스트림 처리 현안"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Apache Flink**: 무한한(Unbounded) 실시간 데이터 스트림을 이벤트 시간(Event Time) 기준으로 밀리초(ms) 단위의 초저지연 및 Stateful(상태 보존) 방식으로 처리하는 3세대 분산 스트림 처리 엔진.
- **Event Time & Watermark**: 서버 수집 시각이 아닌 이벤트가 실제 발생한 시각(Event Time)을 기준으로 늦게 도착한 데이터(Late Data)까지 정확히 처리하게 해주는 시계열 제어 메커니즘.
- **Chandy-Lamport Algorithm**: Flink가 실행 중인 스트림 파이프라인을 멈추지 않고(Non-blocking) 이벤트 흐름 사이에 장벽(Checkpoint Barrier)을 주입해 100% 일치하는 일관된 스냅샷을 뜨는 분산 스냅샷 알고리즘.

</details>

- 정의/개념: 무한 스트림 데이터를 이벤트 시간(Event Time)과 상태 보존(Stateful) 기반으로 서브밀리초 초저지연으로 연산하는 진정한 의미의 Real-Time Stream Engine인 **Apache Flink**
- 배경/필요성: Micro-batch(Spark Streaming) 방식의 지연 한계(수초 ms) 극복, 실시간 이상 거래 탐지(FDS) 및 실시간 정산에서의 Exactly-Once 일관성 수용 요구성

#### 한줄 요약

- 뒤섞인 이벤트를 발생 시간과 키별 상태로 연속 처리하는 스트림 엔진이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Stateful Stream Processing**: 연산자 내부 메모리/RocksDB에 상태(State)를 상주시켜 이전 이벤트 연산 결과를 유지.
- **Asynchronous Barrier Snapshotting (ABS)**: Chandy-Lamport 알고리즘 기반 비동기 스냅샷으로 성능 저하 없는 고가용성 보장.

</details>

- **Event-Driven & Low-Latency Stream-First Architecture (True Streaming)**
- **Event Time, Processing Time, Ingestion Time 3대 시간 개념 및 Watermark 수용**
- **RocksDB State Backend & Chandy-Lamport 알고리즘 기반 Checkpoint**

#### 한줄 요약

- 낮은 지연을 제공하지만 워터마크와 상태 및 체크포인트 비용을 관리해야 한다.

## Ⅲ. 구조 및 구성요소 (Flink 3대 코어 엔진 & 아키텍처)

<details><summary>핵심 용어</summary>

- **JobManager vs TaskManager**: JobManager는 데이터흐름 그래프(JobGraph) 관리 및 체크포인트 총괄, TaskManager는 슬롯(Slot) 단위로 실제 연산 스레드 실행.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Apache Flink Core Architecture                  │
├────────────────────────────────────────────────────────────────────────┤
│ [JobManager (JobGraph / Chandy-Lamport Checkpoint Coordinator)]        │
│                                │ (Barrier Injection)                   │
│        ┌───────────────────────┼───────────────────────┐               │
│        ▼                       ▼                       ▼               │
│  [TaskManager 1]        [TaskManager 2]         [TaskManager 3]        │
│  (TaskSlot / RocksDB)   (TaskSlot / RocksDB)    (TaskSlot / RocksDB)   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: JobManager가 Checkpoint Barrier를 주입하여 TaskManager 내의 RocksDB State를 비동기 스냅샷으로 HDFS/S3에 영속화하는 아키텍처.

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 실무 튜닝 지침 |
|:---|:---|:---|
| **JobManager** | **전체 스트림 데이터플로 관리, 체크포인트 주도** | Master Node HA 구성 (ZooKeeper/KRaft) |
| **TaskManager** | **Task Slot 단위 스레드 실행, RocksDB 상태 관리** | Task Slot 개수 = CPU Core 수 동율 배치 |
| **Watermark** | **시간 기반 윈도 연산 완료 시점 판정용 오프셋** | Allowed Lateness 설정으로 늦은 이벤트 수용 |
| **RocksDB State Backend**| **로컬 디스크 기반 대용량 상태(State) 저장소** | Out-of-Core 상태 저장 시 메모리 관리 |

#### 한줄 요약

- 작업 관리자, 실행자, 시간표, 상태 계산자, 복구•출력 저장소로 구성된다.

## Ⅳ. 흐름도 (Chandy-Lamport 알고리즘 기반 Checkpoint 흐름)

<details><summary>핵심 용어</summary>

- **Checkpoint Barrier**: Stream 데이터 흐름 사이에 주입되는 특수 제어 표식으로, 연산자가 이 Barrier를 만나면 현재 상태(State)를 스냅샷으로 뜬 후 하류 연산자로 전달.

</details>

```text
[Stream Source] ──► [Barrier 1 주입] ──► [Operator 1: State Snapshot (RAM/RocksDB)]
                                                     │
                                                     ▼ (Barrier 전파)
[External S3 / HDFS] ◄── (Async Upload) ─── [Operator 2: State Snapshot]
```

### 동작 원리

1. **Barrier Injection**: JobManager가 Source에 Checkpoint Barrier 주입.
2. **State Alignment**: 연산자가 Barrier 수신 시 이전까지의 데이터 State를 RocksDB에 비동기 저장.
3. **Completion**: 모든 연산자가 Barrier 처리를 마치면 JobManager에 완료 신호 송신 (**Exactly-Once 달성**).

#### 한줄 요약

- 흐름에 사진 촬영선을 흘려 보내 입력 위치•계산 상태•출력 경계를 같은 시점으로 맞춘다.

## Ⅴ. 종류 및 비교 (Apache Flink 대 Spark Streaming)

<details><summary>핵심 용어</summary>

- **Native Streaming vs Micro-Batch**: Flink는 이벤트 1건 단위 레코드 전송(True Native), Spark는 N초 단위로 메시지를 모아서 처리(Micro-Batch).

</details>

| 비교 항목 | Apache Flink (True Native Streaming) | Spark Streaming (Micro-Batch) |
|:---|:---|:---|
| **처리 방식** | **Event-by-Event (레코드 1건 단위 즉시 처리)** | **Micro-Batch (N초 단위로 묶어서 처리)** |
| **지연 시간 (Latency)**| **서브밀리초 (Sub-millisecond: 1~10ms)** | 초 단위 (Sub-second: 100ms ~ 수 초) |
| **상태 관리 (State)** | **RocksDB 기반 대용량 State 내장 지원** | Memory / Checkpoint RDD 중심 |
| **시간 기준 (Time)** | **Event Time, Watermark 완벽 지원** | Processing Time 위주 (Event Time 추후 지원) |

#### 한줄 요약

- Flink는 흐르는 사건을 계속 처리하고 Spark는 기본적으로 작은 묶음의 연속으로 처리한다.

## Ⅵ. 실무 고려사항 및 대책 (Flink Backpressure 및 RocksDB 병목)

<details><summary>핵심 용어</summary>

- **Backpressure (역압력)**: 상류(Upstream) 연산자의 생산 속도가 하류(Downstream) 연산자의 소비 속도보다 빨라 버퍼가 차올라 멈추는 현상.

</details>

| 실무 장애 및 병목 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **Backpressure 발생** | 특정 Operator 처리 병목으로 버퍼 상쇄 | **병목 Operator parallelism(병렬도) 증설** |
| RocksDB State 폭증 | TTL 미설정으로 과거 Key State 잔존 | **`StateTtlConfig` 적용하여 만료 Key 자동 삭제** |
| Checkpoint Timeout | RocksDB 스냅샷 S3 업로드 지연 | **Incremental Checkpointing (증분 스냅샷) 활성화**|

> 사례: **카카오 / 네이버 실시간 이상 결제 탐지(FDS) & 실시간 방송 시청자 수 집계**

#### 한줄 요약

- 늦은 거래를 기다리는 시간과 그동안 쌓이는 계정 상태의 크기를 함께 정해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Flink 아키텍처 수립 기준(Apache Flink Standards)**: Event Time, Watermark 지연 수용성, RocksDB Incremental Checkpoint 및 Exactly-Once 수용성에 의거한 체계.

</details>

- **Flink 아키텍처 수립 기준**에 따라 초저지연 실시간 FDS/스트리밍 파이프라인 구축 시 **Apache Flink & RocksDB** 필수 수용

#### 한줄 요약

- 선택 기준은 이벤트 대기 시간과 상태 크기 및 복구 책임을 함께 비교한다.
