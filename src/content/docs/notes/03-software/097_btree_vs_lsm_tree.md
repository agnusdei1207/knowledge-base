---
sidebar:
  order: 97
  label: "097. B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
date: "2026-08-17T22:55:00+09:00"
tags:
  - "notes-software"
weight: 97
extra:
  question_no: "097"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 쓰기•읽기 구조 절충 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **B-Tree vs LSM-Tree**: 디스크 페이지를 제자리에서 직접 수정(In-Place Update)하는 읽기 최적화 B-Tree(B+Tree)와 메모리 버퍼 적재 후 불변 파일로 순차 추가(Append-Only) 및 병합(Compaction)하는 쓰기 최적화 LSM-Tree.
- **쓰기 증폭 및 읽기 증폭(WAF & RAF)**: B-Tree의 무작위 페이지 분할 쓰기 오버헤드(WAF)와 LSM-Tree의 다중 SSTable 탐색으로 인한 읽기 지연(RAF).

</details>

- 정의/개념: 제자리 수정 기반의 읽기 최적화 **B-Tree(B+Tree)** 와 순차적 추가 및 컴팩션 기반의 대규모 쓰기 최적화 **LSM-Tree**를 비교한 스토리지 엔진 구조
- 배경/필요성: 워크로드 특성(Read-Heavy vs Write-Heavy)에 맞지 않는 스토리지 엔진 선택 시 발생하는 **쓰기 증폭(WAF), 읽기 증폭 및 디스크 I/O 병목 위험** 직면

#### 한줄 요약

- 읽기 중심에는 B-Tree, 대규모 쓰기 중심에는 LSM-Tree를 선택하여 시스템 처리량을 극대화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **In-Place Update vs Append-Only**: 특정 디스크 블록을 직접 덮어쓰는 B-Tree 방식과 무조건 파일 끝에 순차 기록하고 구버전은 컴팩션으로 정리하는 LSM-Tree 방식.
- **블룸 필터(Bloom Filter)**: LSM-Tree에서 특정 키가 SSTable에 존재하는지 확률적으로 사전 검사하여 불필요한 디스크 I/O를 방지하는 필터.

</details>

- 제자리 수정(In-Place) 기반으로 **읽기 응답 지연(Read Latency)이 짧은 B-Tree**
- 순차 쓰기(Sequential Write) 기반으로 **초고속 쓰기 처리량(Write Throughput)을 보장하는 LSM-Tree**
- 쓰기 증폭(Write Amplification)과 읽기 증폭(Read Amplification) 간의 **명확한 트레이드오프**

#### 한줄 요약

- B-Tree는 읽기 경로가 짧고 예측 가능하며, LSM-Tree는 순차 I/O로 쓰기 처리량을 극대화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MemTable 및 SSTable(Sorted String Table)**: LSM-Tree의 메모리 정렬 버퍼(MemTable)와 디스크에 플러시된 불변 정렬 파일(SSTable).

</details>

```text
[ B-Tree vs LSM-Tree 스토리지 엔진 아키텍처 비교 ]

 1. [ B-Tree (제자리 수정: In-Place Update) ]
    Root Node ──► Branch Node ──► Leaf Pages (디스크 고정 블록 덮어쓰기)

 2. [ LSM-Tree (순차 추가 및 병합: Out-of-Place) ]
    쓰기 ──► WAL (디스크 로그) ──► MemTable (RAM 스킵리스트)
                                       │ (Flush)
                                       ▼
             [ Level 0 SSTable ] ──► [ Level 1 SSTable ] (Compaction 병합)
```

선의 의미: B-Tree의 고정 블록 랜덤 I/O 수정과 LSM-Tree의 메모리 버퍼링 및 백그라운드 컴팩션 병합 구조.

| 구성요소 | 책임 |
|:---|:---|
| B-Tree 엔진 | 고정 크기 페이지 단위로 **디스크 블록을 제자리 덮어쓰기(In-Place)하여 일관된 읽기 보장** |
| MemTable (LSM) | 쓰기 데이터를 메모리 상의 정렬 구조(SkipList)에 **임시 버퍼링하여 순차 디스크 플러시 준비** |
| SSTable (LSM) | 정렬된 키-값 쌍을 저장하는 **불변(Immutable) 디스크 파일로 순차 쓰기 지원** |
| 컴팩션 엔진 (LSM) | 여러 SSTable을 병합하여 **중복 및 삭제 데이터를 정리하고 읽기 계층 구조 최적화** |

#### 한줄 요약

- B-Tree는 고정 페이지를 직접 수정하고, LSM-Tree는 메모리 버퍼링과 백그라운드 컴팩션으로 순차 처리

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **LSM-Tree 쓰기 및 컴팩션 절차**: WAL 기록 $\to$ MemTable 적재 $\to$ SSTable 플러시 $\to$ Level별 Compaction 병합.

</details>

```text
[ LSM-Tree 데이터 쓰기 및 컴팩션 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 쓰기 요청: WAL 선행 로그 기록       │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. MemTable 적재: 메모리 정렬 버퍼 갱신│
 └───────────────────┬────────────────────┘
                     │ (MemTable 가득 찰 시)
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. SSTable Flush: Level 0 디스크 기록  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Background Compaction: L0 ➔ L1 병합 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 구버전 및 삭제 톰스톤(Tombstone) 정리│
 └────────────────────────────────────────┘
```

### 동작 원리

1. WAL 기록: 서버 장애 복구를 위해 쓰기 내용을 디스크 WAL(Write-Ahead Log)에 순차 기록.
2. MemTable 적재: 인메모리 스킵리스트인 MemTable에 최신 키-값 데이터를 삽입.
3. SSTable 플러시: MemTable이 임계치에 도달하면 불변(Immutable) 상태로 전환 후 디스크 Level 0 SSTable로 일괄 순차 쓰기.
4. Compaction 병합: 백그라운드 스레드가 겹치는 키 범위를 가진 상하위 레벨 SSTable들을 병합 정렬.
5. 공간 회수: 갱신된 구버전 데이터와 삭제 표식(Tombstone)을 제거하여 디스크 공간을 회수.

#### 한줄 요약

- WAL $\to$ MemTable $\to$ SSTable Flush $\to$ Compaction 병합 $\to$ 공간 회수의 5단계 절차

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **B-Tree DB vs LSM-Tree DB**: MySQL/Oracle 등 전통적 OLTP RDBMS와 RocksDB/Cassandra 등 고성능 NoSQL/시계열 DB.

</details>

| 구분 | B-Tree 기반 데이터베이스 | LSM-Tree 기반 데이터베이스 |
|:---|:---|:---|
| **적용 기준** | 계좌 이체, 결제 등 엄격한 읽기 및 트랜잭션 중심 | IoT 센서, 대규모 로그 수집, 시계열 데이터 쓰기 중심 |
| **핵심 특징** | **제자리 덮어쓰기(In-Place), 짧은 읽기 지연, 높은 읽기 성능** | **순차 추가(Append-Only), 초고속 쓰기 처리량, 블룸 필터 활용** |
| **한계** | 랜덤 쓰기로 인한 페이지 분할 및 쓰기 증폭(WAF) 발생 | 다중 파일 조회로 인한 읽기 증폭(RAF) 및 컴팩션 정체 위험 |

#### 한줄 요약

- 읽기 중심의 정밀 트랜잭션은 B-Tree, 대규모 쓰기 중심의 시계열/로그 수집은 LSM-Tree를 채택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **컴팩션 정체(Compaction Stall)**: LSM-Tree 쓰기 트래픽이 폭증하여 백그라운드 컴팩션 속도가 쓰기 속도를 따라가지 못해 DB가 쓰기 연산을 일시 중단시키는 병목 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LSM-Tree 쓰기 폭증으로 인한 Compaction Stall(쓰기 멈춤) 발생 | **컴팩션 백그라운드 스레드 수 증가 및 SSD I/O 처리량 쿼터 상향** | 쓰기 지연 스파이크 해소 |
| LSM-Tree에서 다중 계층 파일 스캔으로 읽기 응답 지연 | **Bloom Filter 메모리 할당 확장 및 블록 캐시(Block Cache) 증설** | 불필요한 디스크 I/O 99% 차단 |
| B-Tree 무작위 UUID 삽입으로 인한 심각한 페이지 분할 | **순차 증가 TSID/Auto-Increment 키 도입 및 채움 비율(Fillfactor) 조정** | 페이지 분할 방지 및 저장 효율 극대화 |

#### 한줄 요약

- 컴팩션 스레드 튜닝, 블룸 필터 최적화, 순차 키 설계를 통해 각 엔진의 한계를 극복

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **워크로드 맞춤형 엔진 선택(Workload-Driven Selection)**: 시스템의 Read/Write 비율과 허용 가능한 지연 시간(p99)을 분석하여 최적의 엔진 아키텍처를 결정하는 원칙.

</details>

- **B-Tree와 LSM-Tree**는 현대 데이터베이스 아키텍처의 양대 산맥이며, 읽기 중심 OLTP 시스템에는 B-Tree를, 대용량 실시간 쓰기 워크로드에는 LSM-Tree를 적재적소에 배치하여 전체 시스템 처리량을 극대화해야 함

#### 한줄 요약

- 워크로드 특성을 분석하여 B-Tree(읽기 최적화)와 LSM-Tree(쓰기 최적화)를 전략적으로 선택
