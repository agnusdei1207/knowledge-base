---
sidebar:
  order: 97
  label: "097. B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
date: "2026-08-13T19:56:00+09:00"
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

<details><summary>핵심 용어</summary>

- **B-Tree (Balance Tree)**: 데이터 페이지를 디스크상의 지정된 위치에 제자리 수정(In-Place Update) 방식으로 저장하여, 읽기(Read) 성능을 최적화한 전통적 RDBMS(MySQL InnoDB, PostgreSQL) 스토리지 엔진 구조.
- **LSM-Tree (Log-Structured Merge-Tree)**: 데이터를 인메모리(MemTable)에 먼저 기록한 후 디스크에 순차적 Append-Only(Out-of-Place Update)로 덤프(SSTable)하고, 지속적 병합(Compaction)을 거쳐 쓰기(Write) 속도를 극대화한 NoSQL(RocksDB, Cassandra) 스토리지 엔진 구조.
- **In-Place Update vs Out-of-Place Update**: In-Place는 디스크의 해당 블록 위치를 직접 찾아가서 덮어쓰는 방식, Out-of-Place는 무조건 파일 끝에 계속 덧붙이고(Append) 과거 데이터는 정제(Compaction) 시 청소하는 방식.

</details>

- **정의**: 데이터를 디스크 페이지에 제자리 수정(`In-Place Update`) 방식으로 저장하여 읽기 성능을 최적화한 **B-Tree** 엔진과, 인메모리 기록 후 순차 덧붙이기(`Out-of-Place Append-Only`) 및 병합(`Compaction`)으로 쓰기 속도를 극대화한 **LSM-Tree** 엔진.
- 배경/필요성: 저장 구조 불일치는 **읽기 증폭•쓰기 증폭•정리 지연** 유발

#### 한줄 요약

- B-Tree는 장부를 즉시 제자리에 고치고 로그 구조 병합 트리는 메모지에 모아 순서대로 저장한 뒤 나중에 합친다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Random Write vs Sequential Write**: B-Tree는 페이지 갱신•분할, LSM-Tree는 순차 파일 생성과 컴팩션을 중심으로 처리.
- **Write Amplification vs Read Amplification**: B-Tree는 랜덤 쓰기로 인한 쓰기 증폭 발생, LSM-Tree는 여러 계층의 SSTable 스캔으로 인한 읽기 증폭 발생.

</details>

- **B-Tree**: 읽기 최적화(`Read-Heavy`), 제자리 수정(`In-Place Update`), 페이지 분할(`Page Split`) 발생.
- **LSM-Tree**: 쓰기 최적화(`Write-Heavy`), 순차 덧붙이기(`Out-of-Place Append-Only`), 블룸 필터(`Bloom Filter`) 기반 읽기 보완.
- **운영 Trade-off**: 쓰기 증폭(`WAF`) 대 읽기 증폭(`Read Amplification`) 관리.

#### 한줄 요약

- 즉시 정리하면 읽기 경로가 짧고 몰아서 정리하면 쓰기가 효율적이지만 나중에 찾고 합치는 비용이 생긴다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **MemTable & SSTable (Sorted String Table)**: LSM-Tree의 메모리 정렬 버퍼(MemTable)와 디스크 불변 정렬 파일(SSTable).
- **Bloom Filter**: LSM-Tree 읽기 시 특정 키(Key)가 SSTable 파일에 존재하는지 안 하는지를 확률적으로 빠르게 판별해 무의미한 디스크 I/O를 막아주는 필터.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        B-Tree vs LSM-Tree 아키텍처                     │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. B-Tree (제자리 수정)           │ 2. LSM-Tree (순차 덧붙이기)        │
├───────────────────────────────────┼────────────────────────────────────┤
│  루트 ──► 브랜치 ──► 리프 페이지  │  쓰기 ──► WAL ──► MemTable (RAM)  │
│  (디스크 지정 블록 덮어쓰기)      │                     │ (Flush)      │
│                                   │                    ▼               │
│                                   │          SSTable L0 ──► L1 (병합)  │
└───────────────────────────────────┴────────────────────────────────────┘
```

선의 의미: B-Tree는 덮어쓰기 방식으로 디스크 페이지를 수정하고, LSM-Tree는 WAL과 MemTable을 거쳐 SSTable 디스크 파일로 순차 누적 후 Compaction 병합하는 구조.

| 구성요소 / 지표 | B-Tree Engine (MySQL InnoDB) | LSM-Tree Engine (RocksDB, Cassandra) |
|:---|:---|:---|
| **데이터 수정 방식** | **In-Place Update (지정 블록 덮어쓰기)** | **Out-of-Place Append-Only (순차 덧붙이기)** |
| **핵심 구성 아키텍처**| **Root - Branch - Leaf Pages, WAL** | **WAL, MemTable, SSTable, Bloom Filter** |
| **쓰기 특성** | 페이지 갱신•분할과 WAL 비용 | **순차 Flush 후 Compaction 비용** |
| **읽기 특성** | **짧은 트리 경로와 페이지 캐시 활용** | 여러 SSTable 확인을 필터•캐시로 보완 |
| **쓰기 증폭** | 페이지•WAL 갱신으로 발생 | **반복 Compaction으로 발생 가능** |

#### 한줄 요약

- 즉시 고치는 페이지와 모아 병합하는 파일 구조의 구성 차이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Compaction**: LSM-Tree 디스크 상의 여러 계층(Level 0, Level 1...)에 파편화된 SSTable 파일들을 배경(Background)에서 정렬하여 하나로 합치고, 오래된 삭제/수정 데드 레코드를 청소하는 주 정리 작업.

</details>

```text
┌──────────────────────────────┐
│ 쓰기 요청                    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. WAL 기록                 │
│ 2. MemTable 반영            │
│ 3. SSTable Flush            │
│ 4. Compaction 병합          │
│ 5. 구버전•삭제 표식 정리     │
└──────────────┬───────────────┘
               ▼
         [쓰기 확정]
```

### 동작 원리

1. **WAL 기록**: 장애 복구를 위한 변경 로그 선행 기록.
2. **MemTable 반영**: 메모리 정렬 구조에 최신 값 저장.
3. **SSTable Flush**: 불변 MemTable을 정렬 파일로 기록.
4. **Compaction 병합**: 계층 파일을 병합해 읽기 경로 정리.
5. **구버전•삭제 표식 정리**: 안전한 범위의 공간 회수.

#### 한줄 요약

- 로그 구조 병합 트리는 변경을 복구 장부와 메모리에 먼저 적고, 모이면 정렬 파일로 내려 쓴다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **RocksDB / LevelDB**: Facebook 및 Google이 오픈소스로 공개한 대표적 LSM-Tree 스토리지 엔진.

</details>

| 비교 항목 | B-Tree 기반 데이터베이스 | LSM-Tree 기반 데이터베이스 |
|:---|:---|:---|
| 대표 DB 제품 | **MySQL InnoDB, Oracle, PostgreSQL** | **RocksDB, Apache Cassandra, LevelDB** |
| 주 타깃 워크로드 | **OLTP (결제, 계좌, 회원 정보 등)** | **시계열, IoT 센서 로그, 대규모 쓰기 부하** |
| 디스크 메커니즘 | **Page-based Random I/O** | **File Segment-based Sequential I/O** |
| 읽기 가속 수단 | B+Tree Leaf Node Pointer | **Bloom Filter (블룸 필터)** |

#### 한줄 요약

- B-Tree는 해당 장부를 바로 고치고, 로그 구조 병합 트리는 새 조각을 빠르게 만든 뒤 나중에 합친다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Compaction Stall (컴팩션 정체)**: LSM-Tree 쓰기 트래픽이 너무 폭증하여 백그라운드 Compaction 속도가 따라가지 못해 DB가 잠시 쓰기 연산을 멈춰 세우는 병목 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LSM-Tree 사용 시 쓰기 폭증으로 인한 **Compaction Stall** 발생 | **Compaction 백그라운드 스레드 수 증가 및 SSD I/O 쿼터 확장**| 쓰기 멈춤 현상 해소 |
| LSM-Tree에서 읽기 속도가 저하되는 현상 | **Bloom Filter 바이트 수 확장 및 MemTable 크기 튜닝** | 읽기 성능 회복 |
| B-Tree 무작위 키로 페이지 분할•캐시 지역성 저하 | 노출•분산 요구와 함께 **순차성 키** 검토 | 페이지 갱신 비용 완화 |

> 사례: **카카오 / 네이버 시계열 로그 DB로 RocksDB/Cassandra (LSM-Tree) 채택**

#### 한줄 요약

- 평균 속도뿐 아니라 정리 작업 중 가장 느린 응답과 저장장치 부담까지 비교해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **스토리지 엔진 선택 기준(Storage Engine Selection Standards)**: Read/Write 워크로드 비율, Latency p99 및 WAF/Compaction 오버헤드에 의거한 체계.

</details>

- 낮은 읽기 지연은 **B-Tree**, 높은 순차 쓰기는 **LSM-Tree** 우선 검토

#### 한줄 요약

- 저장 구조 선택 검증 기준으로 찾기•쓰기•정리 비용을 모두 측정한다.
