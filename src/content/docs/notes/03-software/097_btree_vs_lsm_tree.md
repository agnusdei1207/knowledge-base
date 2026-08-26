---
sidebar:
  order: 97
  label: "097. B-Tree vs LSM-Tree"
  badge:
    text: "기출 · 50%"
    variant: note
title: "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
date: "2026-08-26T09:48:00+09:00"
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

- **B-Tree / B+Tree**: 디스크 블록을 제자리에서 직접 덮어쓰는(In-Place Update) 읽기 최적화 트리 구조 (MySQL, PostgreSQL 표준).
- **LSM-Tree(Log-Structured Merge-Tree)**: 메모리 버퍼에 쓴 뒤 디스크에 순차 추가(Append-Only)하고 컴팩션으로 병합하는 쓰기 최적화 구조 (RocksDB, Cassandra).

</details>

- 정의/개념: 디스크 페이지 제자리 수정 기반의 읽기 최적화 **B-Tree**와 메모리 버퍼링 및 순차 컴팩션 기반의 대규모 쓰기 최적화 **LSM-Tree** 스토리지 엔진
- 배경/필요성: 워크로드 특성(Read-Heavy vs Write-Heavy)에 맞지 않는 스토리지 엔진 선택 시 발생하는 **쓰기 증폭(WAF), 읽기 증폭 및 디스크 I/O 병목 해결 불가**

#### 한줄 요약
- 읽기 중심에는 B-Tree, 대규모 쓰기 중심에는 LSM-Tree를 선택하여 처리량을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **In-Place vs Out-of-Place**: 특정 디스크 블록을 찾아 덮어쓰는 B-Tree와 파일 끝에 순차적으로 추가 기록하는 LSM-Tree의 갱신 방식 차이.
- **Bloom Filter**: LSM-Tree에서 특정 키가 SSTable 파일에 존재하는지 $O(1)$로 사전 검사하여 낭비되는 디스크 I/O를 막는 확률적 자료구조.

</details>

- 제자리 수정(In-Place) 기반으로 **결정론적 읽기 지연(Read Latency)이 짧은 B-Tree**
- 순차 추가(Append-Only) 기반으로 **초고속 쓰기 처리량(Write Throughput)을 보장하는 LSM-Tree**
- 쓰기 증폭(Write Amplification)과 읽기 증폭(Read Amplification) 간의 **명확한 트레이드오프**

#### 한줄 요약
- B-Tree는 읽기 경로가 짧고 예측 가능하며, LSM-Tree는 순차 I/O로 쓰기 처리량을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MemTable & SSTable**: LSM-Tree의 메모리 정렬 버퍼(MemTable: SkipList)와 디스크에 플러시된 불변 정렬 파일(SSTable: Sorted String Table).

</details>

```text
[B-Tree vs LSM-Tree 스토리지 아키텍처 비교]
|-- 1. B-Tree 엔진 (In-Place Update: 제자리 덮어쓰기)
|   `-- Root Node -> Branch Node -> Leaf Page (디스크 16KB 고정 페이지 랜덤 I/O 덮어쓰기)
`-- 2. LSM-Tree 엔진 (Out-of-Place: 메모리 버퍼 + 순차 디스크 플러시)
    |-- 쓰기 요청 -> WAL (Write-Ahead Log) 순차 기록 + MemTable (인메모리 SkipList) 적재
    |-- Flush -> Level 0 SSTable (불변 정렬 파일 디스크 순차 쓰기)
    `-- Background Compaction -> Level 1 ~ N SSTable 병합 및 삭제 톰스톤(Tombstone) 정리
```

선의 의미: 계층 및 B-Tree의 고정 블록 랜덤 수정과 LSM-Tree의 메모리 버퍼링 및 백그라운드 컴팩션 구조

| 구성요소 | B-Tree 엔진 | LSM-Tree 엔진 |
|:---|:---|:---|
| 데이터 쓰기 방식 | **제자리 덮어쓰기 (In-Place Update)** | **메모리 버퍼 후 순차 쓰기 (Append-Only)** |
| 핵심 구성요소 | 고정 크기 페이지 (Root, Branch, Leaf) | **MemTable (RAM), SSTable (Disk), Bloom Filter** |
| 데이터 병합/정리 | 페이지 분할(Split) 및 병합 시 즉시 실행 | **백그라운드 컴팩션(Compaction) 비동기 병합** |
| 삭제 처리 방식 | 디스크 블록 내 슬롯 즉시 해제 | **삭제 표식(Tombstone) 기록 후 컴팩션 시 수거** |

#### 한줄 요약
- B-Tree는 고정 페이지를 직접 수정하고, LSM-Tree는 메모리 버퍼링과 백그라운드 컴팩션으로 순차 처리한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Compaction(컴팩션)**: 여러 SSTable 파일을 읽어 중복 키를 제거하고 최신 값만 남겨 새로운 SSTable로 병합하는 백그라운드 정리 작업.

</details>

```text
LSM-Tree 쓰기 및 읽기 처리 파이프라인
        │
   [쓰기 경로] WAL 디스크 기록 ➔ MemTable(RAM) 삽입 ➔ 메모리 가득 차면 L0 SSTable로 Flush
        │
   [컴팩션] 백그라운드 스레드가 L0 ➔ L1 ➔ L2 SSTable들을 병합 정렬하며 톰스톤(Tombstone) 제거
        │
   [읽기 경로] 1. MemTable 검색 ➔ 2. 불변 MemTable 검색 ➔ 3. Bloom Filter 검사 ➔ 4. SSTable 탐색
```

#### 한줄 요약
- 쓰기는 WAL+MemTable 즉시 완료, 읽기는 Bloom Filter를 거쳐 계층별 SSTable을 탐색한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **WAF vs RAF**: 쓰기 증폭(실제 쓴 데이터 대비 디스크 기록량)과 읽기 증폭(1건 읽기 위해 접근한 디스크 블록 수).

</details>

| 비교 항목 | B-Tree 기반 (MySQL InnoDB, Oracle) | LSM-Tree 기반 (RocksDB, Cassandra) |
|:---|:---|:---|
| 읽기 성능 (Read) | **최고 (단일 리프 페이지 $O(\log N)$ 직접 접근)** | 보통 (여러 SSTable 스캔 가능성, 블룸필터 필수) |
| 쓰기 성능 (Write) | 보통 (디스크 랜덤 I/O 및 페이지 분할 부하) | **최고 (메모리 버퍼링 + 디스크 순차 I/O)** |
| 쓰기 증폭 (WAF) | 높음 (작은 행 수정 시 16KB 페이지 전체 덮어쓰기) | 보통~높음 (컴팩션 시 반복 병합 쓰기 발생) |
| 압축률 / 스토리지 | 보통 (페이지 단편화 공간 낭비 발생) | **매우 높음 (SSTable 불변 파일 고압축 저장)** |
| 주 적용 도메인 | **은행 계좌, 결제, 전통적 웹 OLTP** | **IoT 시계열 센서, 로그 수집, 대규모 메시징** |

#### 한줄 요약
- 읽기 중심의 정밀 트랜잭션은 B-Tree, 대규모 쓰기 중심의 시계열/로그 수집은 LSM-Tree를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Compaction Stall(컴팩션 지연 멈춤)**: 쓰기 속도가 너무 빨라 백그라운드 컴팩션이 따라가지 못할 때 DB가 쓰기를 강제로 멈추는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LSM-Tree 쓰기 폭증으로 인한 Compaction Stall(쓰기 멈춤) | **컴팩션 백그라운드 스레드 증설 및 SSD NVMe I/O 대역폭 확보** | 쓰기 지연 스파이크 제거 |
| LSM-Tree에서 다중 계층 파일 스캔으로 읽기 응답 지연 | **Bloom Filter 메모리 할당 확장 및 블록 캐시(Block Cache) 증설** | 불필요한 디스크 I/O 99% 차단 |
| B-Tree 무작위 UUID 삽입으로 인한 심각한 페이지 분할 | **순차 증가 TSID/Auto-Increment 키 도입 및 Fillfactor 조정** | 페이지 분할 방지 및 저장 공간 30% 절감 |
| B-Tree 대규모 배치 쓰기 시 I/O 병목 | **Insert Buffer(Change Buffer)를 활용하여 보조 인덱스 쓰기 지연 병합** | 대량 삽입 속도 3배 향상 |

#### 한줄 요약
- 컴팩션 스레드 증설, 블룸 필터 캐싱, 순차 키 설계, 체인지 버퍼 활용으로 성능을 튜닝한다.

## Ⅶ. 결론

- 조회 트랜잭션은 **B-Tree**, 대규모 쓰기는 **LSM-Tree** 선택

#### 한줄 요약
- B-Tree(읽기 최적화)와 LSM-Tree(쓰기 최적화)는 워크로드의 Read/Write 특성에 따라 상호 보완적으로 선택되는 스토리지 엔진의 핵심 아키텍처다.