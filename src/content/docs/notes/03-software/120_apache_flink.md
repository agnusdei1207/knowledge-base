---
sidebar:
  order: 120
  label: "120. Apache Flink 스트림 처리"
  badge:
    text: "미출 · 50%"
    variant: note
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-08-26T09:53:00+09:00"
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

- 정의/개념: 무한한 데이터 스트림을 **이벤트 시간(Event Time) 기준으로 밀리초 단위 초저지연 및 Stateful 방식으로 연속 처리하는 분산 스트림 엔진**
- 배경/필요성: 기존 마이크로배치 방식의 **지연 이벤트 처리 불가, 연속적 상태(State) 계산의 한계 및 처리 지연시간 해결 불가**

#### 한줄 요약
- 이벤트 시간 기반 처리와 Stateful 상태 관리를 통해 밀리초 단위 초저지연 스트림 연산을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Stateful Stream Processing**: 연산자 내부 메모리 및 RocksDB에 키별 상태(State)를 보존하여 세션 누적 및 윈도 집계를 수행.
- **Asynchronous Barrier Snapshotting(ABS)**: Chandy-Lamport 알고리즘을 응용하여 스트림 중단 없이(Non-blocking) 정확히 한 번(Exactly-Once) 상태를 스냅샷하는 기술.

</details>

- 이벤트 1건 단위로 즉시 연산하는 **네이티브 스트리밍(True Streaming)**
- 네트워크 지연을 극복하는 **이벤트 시간(Event Time) 및 워터마크(Watermark) 제어**
- RocksDB State Backend 및 ABS 기반의 **정확히 한 번(Exactly-Once) 무손실 복구**

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
    |-- TaskManager 1 -> TaskSlot (Operator 실행 + RocksDB Local State)
    |-- TaskManager 2 -> TaskSlot (Operator 실행 + RocksDB Local State)
    `-- Checkpoint Storage (S3 / HDFS: 비동기 Chandy-Lamport 스냅샷 파일 영구 저장)
```

선의 의미: 계층 및 JobManager가 체크포인트를 주입하고 TaskManager들이 로컬 상태를 영구 스토리지에 비동기 복제하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 작업 관리자 (JobManager) | JobGraph 생성, 태스크 스케줄링 및 **Chandy-Lamport 체크포인트 조율 총괄** | 분산 코디네이터 |
| 태스크 관리자 (TaskManager) | TaskSlot 단위로 연산자(Operator)를 할당받아 **메모리 및 CPU 병렬 연산 수행** | 멀티스레드 슬롯 분할 |
| 워터마크 (Watermark) | 스트림 내에 시간 진행을 명시하여 **지연 도착 이벤트의 윈도 종료 시점 확정** | 지연 데이터 수용 제어 |
| 상태 백엔드 (State Backend) | HashMap 또는 RocksDB를 통해 **키별 상태(Keyed State)를 고속 저장 및 관리** | TB급 대용량 상태 지원 |
| 체크포인트 스토리지 | 장애 복구 시 원복할 **연산자 상태 스냅샷과 카프카 오프셋을 영구 보관** | S3 / HDFS 분산 스토리지 |

#### 한줄 요약
- 작업 관리자, 태스크 관리자, 워터마크, 상태 백엔드, 체크포인트 저장소가 유기적으로 결합된다.

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
   [Barrier 하류 전파] 스트림 중단 없이 Barrier를 다음 Downstream 연산자로 즉시 방출
        │
   모든 연산자의 스냅샷 완료 ACK를 수신한 JobManager가 최신 체크포인트 메타데이터를 영구 확정
```

#### 한줄 요약
- Barrier 주입 → 입력 정렬 → 비동기 스냅샷 → Barrier 하류 전파 → 체크포인트 확정 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Flink vs Spark Streaming**: 이벤트 1건 단위 네이티브 스트리밍(Flink)과 N초 단위 마이크로배치(Spark).

</details>

| 비교 항목 | Apache Flink (True Native Streaming) | Spark Streaming (Micro-Batch) |
|:---|:---|:---|
| 데이터 처리 방식 | **이벤트 1건 단위 즉시 파이프라이닝 (Event-by-Event)**| **N초 주기로 마이크로배치를 묶어 처리 (Micro-Batch)**|
| 처리 지연시간 (Latency)| **수 밀리초(ms) 단위의 극초저지연** | 수백 밀리초(ms) ~ 수 초 단위의 지연 |
| 상태 관리 (State) | **RocksDB 내장 지원으로 테라바이트급 상태 보존** | 메모리 기반 RDD 캐싱 및 체크포인트 |
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
| 무한 증식하는 Keyed State로 인한 메모리 및 디스크 고갈 | **`StateTtlConfig` 적용으로 비활성 Key State 자동 만료(TTL)** | 상태 크기 70% 압축 유지 |
| 대용량 상태 스냅샷 시 S3 I/O 병목 및 체크포인트 타임아웃 | **Incremental Checkpointing(증분 스냅샷) 옵션 활성화** | 체크포인트 소요 시간 90% 단축 |
| 너무 늦게 도착한 Late Event로 인한 집계 누락 | **`allowedLateness` 설정 및 Side Output으로 지연 데이터 별도 수집** | 데이터 유실 0화 및 정확성 보장 |

#### 한줄 요약
- 병렬도 증설, State TTL 설정, 증분 체크포인트, Side Output으로 실무 안정성을 확보한다.

## Ⅶ. 결론

- 실시간 스트림은 **Flink**, 무손실 복구는 **ABS** 선택

#### 한줄 요약
- Apache Flink는 이벤트 시간 처리와 강력한 상태 관리를 통해 밀리초 단위 초저지연과 무손실 정합성을 완성하는 차세대 스트림 처리 엔진이다.