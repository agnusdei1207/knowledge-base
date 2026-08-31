---
sidebar:
  order: 120
  label: "120. Apache Flink 스트림 처리"
  badge:
    text: "미출 · 50%"
    variant: note
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-08-31T10:48:00+09:00"
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

<details><summary>용어 설명</summary>

- **Apache Flink**: 이벤트 1건 단위(Event-by-Event)로 파이프라이닝하여 밀리초(ms) 단위 응답을 제공하는 네이티브 분산 스트림 처리 엔진.
- **Event Time & Watermark**: 이벤트가 실제 발생한 시각(Event Time)을 기준으로 지연 도착 데이터(Late Data)를 정밀 집계하기 위한 타임스탬프 진행 표식(Watermark).

</details>

- 정의/개념: **이벤트 시간과 상태** 기반으로 연속 데이터를 처리하는 분산 스트림 엔진
- 배경/필요성: 기존 마이크로배치(Micro-batch) 스트리밍 엔진이 수 초 단위의 지연(Latency)에 갇히고 네트워크 지연으로 뒤늦게 도착한 이벤트(Late-Arriving Data)를 이미 닫힌 윈도에 정합성 있게 반영하지 못하는 한계를 극복하고, 이벤트 1건 단위(Event-by-Event)의 진정한 네이티브 스트리밍과 이벤트 시간(Event Time) 기반 워터마크(Watermark) 제어, RocksDB 기반 상태(State) 관리 및 비동기 체크포인트(Asynchronous Barrier Snapshotting)를 결합하여 **서브세컨드(ms 단위) 초저지연과 정확히 한 번(Exactly-Once) 상태 일관성을 동시에 보장**할 필요

#### 한줄 요약
- 이벤트 시간 처리는 늦게 온 데이터까지 정확히 반영하는 대신 워터마크만큼 결과 확정을 미루므로, 정확성과 지연은 이 한 값의 설정에서 서로를 밀어낸다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Stateful Stream Processing**: 연산자 내부 메모리 및 RocksDB에 키별 상태(State)를 보존하여 세션 누적 및 윈도 집계를 수행.
- **Asynchronous Barrier Snapshotting(ABS)**: Chandy-Lamport 알고리즘을 응용하여 스트림 중단 없이(Non-blocking) 정확히 한 번(Exactly-Once) 상태를 스냅샷하는 기술.

</details>

- 이벤트 1건 단위로 즉시 연산하는 **네이티브 스트리밍(True Streaming)**
- 네트워크 지연을 극복하는 **이벤트 시간(Event Time) 및 워터마크(Watermark) 제어**
- 체크포인트와 호환 Source·Sink 기반 **Exactly-Once 처리** 지원

#### 한줄 요약
- 네이티브 스트리밍, 이벤트 시간 기반 윈도잉, RocksDB 상태 보존을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **JobManager vs TaskManager**: JobGraph를 스케줄링하고 체크포인트를 총괄하는 JobManager와 TaskSlot에서 연산자를 병렬 실행하는 TaskManager.

</details>

```text
[Apache Flink 분산 스트리밍 아키텍처]
|-- JobManager (마스터 노드: JobGraph 분석, 리소스 스케줄링, Checkpoint Coordinator)
`-- TaskManager Cluster (워커 노드들: TaskSlot 단위 병렬 실행)
    |-- TaskManager 1
    |   `-- TaskSlot·Local State
    |-- TaskManager 2
    |   `-- TaskSlot·Local State
    `-- Checkpoint Storage (S3 / HDFS: 비동기 Chandy-Lamport 스냅샷 파일 영구 저장)
```

선의 의미: 계층 및 JobManager가 체크포인트를 주입하고 TaskManager들이 로컬 상태를 영구 스토리지에 비동기 복제하는 구조

| 구성요소 | 책임 |
|:---|:---|
| JobManager | JobGraph·스케줄링·**체크포인트 조율** |
| TaskManager | TaskSlot에서 연산자 병렬 실행 |
| Watermark | 이벤트 시간 진행과 윈도 종료 판단 |
| State Backend | **Keyed State** 저장과 스냅샷 지원 |
| Checkpoint Storage | 연산자 상태와 메타데이터 보관 |

#### 한줄 요약
- 상태를 엔진이 직접 보관하기에 연속 집계가 가능하지만 그 상태가 곧 장애 복구의 대상이 되므로, 체크포인트 주기와 상태 크기가 복구 시간과 평시 부하를 동시에 좌우한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Chandy-Lamport Checkpoint 파이프라인**: Source에 Barrier 주입 $\to$ 연산자 상태 스냅샷 $\to$ Barrier 하류 전파 $\to$ JobManager 완료 등록.

</details>

```text
스트림 처리 도중 주기적 Checkpoint 트리거
        │
   [Barrier 주입] JobManager의 지시로 Source 연산자가 이벤트 스트림 사이에 Checkpoint Barrier 삽입
        │
   [입력 정렬] 다중 입력 채널을 가진 연산자가 모든 채널의 동일 Barrier 번호 정렬 대기
        │
   [비동기 상태 스냅샷] 연산자가 로컬 RocksDB State를 복사하여 백그라운드로 S3/HDFS에 비동기 업로드
        │
   [Barrier 하류 전파] Barrier를 다음 Downstream 연산자로 전달
        │
   모든 연산자의 스냅샷 완료 ACK를 수신한 JobManager가 최신 체크포인트 메타데이터를 영구 확정
```

#### 한줄 요약
- Barrier를 흘려보내 비동기로 스냅샷을 뜨기에 처리를 멈추지 않고도 정합성을 얻지만, 입력 정렬을 기다리는 구간에서는 가장 느린 경로 하나가 체크포인트 전체를 지연시킨다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Flink vs Spark Streaming**: 이벤트 1건 단위 네이티브 스트리밍(Flink)과 N초 단위 마이크로배치(Spark).

</details>

| 비교 항목 | Apache Flink (True Native Streaming) | Spark Streaming (Micro-Batch) |
|:---|:---|:---|
| 데이터 처리 방식 | **이벤트 1건 단위 즉시 파이프라이닝 (Event-by-Event)**| **N초 주기로 마이크로배치를 묶어 처리 (Micro-Batch)**|
| 지연 특성 | **이벤트 단위 파이프라인** | 트리거 간격 기반 마이크로배치 |
| 상태 관리 | State Backend와 체크포인트 | 상태 저장소와 체크포인트 |
| 시간 처리 모델 | **Event Time 및 Watermark 기본 최적화** | 워터마크 지원하나 배치 경계 의존적 |

#### 한줄 요약
- 극초저지연 실시간 연산은 Flink, 대용량 배치와의 통합 파이프라인은 Spark를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Backpressure**: 하류 연산자의 처리 지연으로 인해 상류 연산자의 출력 버퍼가 포화되어 데이터 유입이 차단되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 하류 병목으로 인한 상류 파이프라인 **Backpressure** 차단 | **병목 Operator Parallelism(병렬도) 증설 및 키 Salting 분산** | 파이프라인 버퍼 막힘 해소 |
| Keyed State 증가에 따른 저장 공간 고갈 | 비활성 상태에 **State TTL** 적용 | 상태 보존 기간과 크기 제한 |
| 상태 스냅샷의 저장소 I/O 병목 | **Incremental Checkpointing** 적용 | 변경 상태 중심으로 전송량 감소 |
| 늦은 이벤트에 따른 집계 누락 | **allowedLateness·Side Output** 적용 | 지연 데이터의 별도 처리 지원 |

#### 한줄 요약
- 병렬도 증설, State TTL 설정, 증분 체크포인트, Side Output으로 실무 안정성을 확보한다.

## Ⅶ. 결론

- 글로벌 금융 이상거래 탐지(FDS), 실시간 추천 및 초저지연 스트림 분석의 **가장 진보된 표준 상태 기반(Stateful) 스트림 처리 프레임워크**로 확립되었으며, 실무 운영 시에는 **워터마크 지연 데이터 누락을 방지하는 `allowedLateness` 및 Side Output 격리, 상태 메모리 폭증을 제어하는 State TTL과 증분 체크포인트(Incremental Checkpoint), 하류 병목으로 인한 Backpressure 해소를 위한 연산자 병렬도(Parallelism) 튜닝**을 결합하여 무중단 고성능 스트리밍 파이프라인을 완성

#### 한줄 요약
- 체크포인트 주기·상태 크기·허용 지연을 SLO에 맞춰 조정한다.
