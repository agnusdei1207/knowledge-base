---
sidebar:
  order: 97
  label: "097. B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
date: "2026-08-04T12:44:00+09:00"
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

<details>
<summary>핵심 용어</summary>

- **B-Tree**: 균형 잡힌 정렬 페이지에서 값을 제자리 갱신해 점•범위 조회에 안정적인 저장 구조이다.
- **로그 구조 병합 트리(Log-Structured Merge-Tree, LSM-Tree)**: 변경을 메모리에 모아 정렬 파일로 병합하는 저장 구조다.

</details>

- 정의/개념: **제자리 갱신과 순차 병합** 을 대비한 저장 구조 비교
- 배경/필요성: 단일 저장 구조는 **읽기•쓰기 편향** 에 취약

#### 한줄 요약

- B-Tree는 장부를 즉시 제자리에 고치고 LSM-Tree는 메모지에 모아 순서대로 저장한 뒤 나중에 합친다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **컴팩션**: 여러 정렬 파일을 병합하며 중복과 삭제 표식을 정리하는 작업이다.
- **제자리 페이지 갱신**: B-Tree가 기존 키 위치의 페이지를 직접 바꾸고 필요하면 분할하는 쓰기 방식이다.
- **메모리 흡수 후 정렬 파일 기록**: LSM-Tree가 변경을 메모리에 누적한 뒤 키순 불변 파일로 내려 쓰는 방식이다.

</details>

- **B-Tree**: 균형 트리와 제자리 페이지 갱신
- **LSM-Tree**: 메모리 흡수 후 정렬 파일 기록
- **컴팩션**: 중복 정리와 쓰기 증폭 발생

#### 한줄 요약

- 즉시 정리하면 읽기 경로가 짧고 몰아서 정리하면 쓰기가 효율적이지만 나중에 찾고 합치는 비용이 생긴다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **선행 기록 로그(Write-Ahead Log, WAL)**: 메모리 데이터보다 변경을 먼저 영속화하는 로그다.
- **메모리 테이블(Memory Table, Memtable)**: 최신 변경을 키순으로 누적하는 메모리 구조다.
- **정렬 문자열 테이블(Sorted String Table, SSTable)**: 키순으로 정렬된 불변 디스크 파일이다.
- **블룸 필터(Bloom Filter)**: 키가 파일에 없음을 빠르게 판정하는 확률적 구조다.

</details>

```mermaid
block-beta
  columns 3
  W["워크로드"]
  B["B-Tree 페이지"]
  L["WAL•Memtable"]
  S["SSTable"]
  C["Compaction"]
  F["Bloom Filter"]
  W --- B
  W --- L
  L --- S
  S --- C
  F --- S
```

| 구성요소 | 책임 |
|:---|:---|
| B-Tree 페이지 | **정렬 탐색•갱신•분할** 수행 |
| 워크로드 | **읽기•쓰기 비율•지연 목표** 제공 |
| WAL•Memtable | **변경 복구•메모리 누적** |
| SSTable | **키순 불변 파일** 저장 |
| Compaction | **파일 병합•중복 정리** |
| Bloom Filter | **없는 키의 파일 읽기** 차단 |

#### 한줄 요약

- 즉시 고치는 페이지와 모아 병합하는 파일 구조의 구성 차이다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **1. WAL 순차 기록**: 메모리 테이블 갱신 전에 복구 로그를 영속화하는 단계이다.
- **2. Memtable 갱신**: 영속화된 변경의 최신 값을 메모리 정렬 구조에 반영하는 단계이다.
- **3. SSTable Flush**: Memtable이 한도에 도달하면 키순 불변 파일로 디스크에 기록하는 단계이다.

</details>

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant E as 저장 엔진
    participant W as WAL
    participant M as Memtable
    participant S as SSTable
    C->>E: 키•값 쓰기 요청
    E->>W: 1. WAL 순차 기록
    W-->>E: 영속화 확인
    E->>M: 2. Memtable 갱신
    E-->>C: 쓰기 완료 응답
    M->>S: 3. SSTable Flush
```

**동작 원리**

- **1. WAL 순차 기록**: Memtable보다 먼저 복구 로그 보존
- **2. Memtable 갱신**: 메모리 정렬 구조에 최신 값 반영
- **3. SSTable Flush**: 한도 도달 시 정렬 파일로 영속화

#### 한줄 요약

- LSM-Tree는 변경을 복구 장부와 메모리에 먼저 적고, 모이면 정렬 파일로 내려 쓴다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>


</details>

| 판단 기준 | B-Tree | LSM-Tree |
|:---|:---|:---|
| 적용 기준 | **점•범위 읽기•안정 지연** | 높은 **순차 쓰기 처리량** |
| 핵심 특징 | **정렬 페이지 제자리 갱신** | **WAL•Memtable 후 파일 병합** |
| 한계 | **페이지 분할•임의 쓰기** | **컴팩션•읽기•공간 증폭** |

> 선택 기준: 데이터 크기•캐시•저장장치•정책을 반영한 **읽기•쓰기 실측**

#### 한줄 요약

- B-Tree는 해당 장부를 바로 고치고, LSM-Tree는 새 조각을 빠르게 만든 뒤 나중에 합친다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **점 조회(Point Lookup)**: 단일 키로 데이터를 찾는 조회 유형이다.
- **범위 조회(Range Scan)**: 연속된 키 구간의 데이터를 찾는 조회 유형이다.
- **갱신 비율(Update Ratio)**: 전체 작업 중 데이터 변경이 차지하는 비율이다.
- **피크 부하(Peak Load)**: 단위 시간의 최대 요청 유입량이다.
- **읽기 증폭(Read Amplification)**: 한 논리 조회에 실제로 읽는 데이터 증가 비율이다.
- **쓰기 증폭(Write Amplification)**: 한 논리 쓰기에 실제로 기록하는 데이터 증가 비율이다.
- **공간 증폭(Space Amplification)**: 논리 데이터보다 실제 저장량이 늘어난 비율이다.
- **컴팩션 대역폭(Compaction Bandwidth)**: 단위 시간에 병합할 수 있는 데이터 양이다.
- **컴팩션 백로그(Compaction Backlog)**: 병합을 기다리는 정렬 파일의 양이다.
- **캐시 예산(Cache Budget)**: 읽기 가속에 사용할 메모리 한도다.
- **쓰기 버퍼 예산(Write-buffer Budget)**: 쓰기 흡수에 사용할 메모리 한도다.
- **체크포인트(Checkpoint)**: 장애 복구를 시작할 저장 지점이다.
- **플러시(Flush)**: 메모리 변경을 디스크에 저장하는 처리다.
- **복구 시간 목표(Recovery Time Objective, RTO)**: 서비스 재시작에 허용된 최대 시간이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 평균 비율이 피크 부하를 은폐 | **점•범위•갱신•피크** 부하 측정 | **워크로드 오판** 방지 |
| 증폭 증가로 장치 수명•용량 저하 | **읽기•쓰기•공간 증폭** 계측 | **장치 수명•용량** 통제 |
| 컴팩션 적체로 쓰기 정체 발생 | **대역폭•백로그 경보** 조정 | **꼬리 지연** 감소 |
| 캐시와 쓰기 버퍼의 메모리 경쟁 | **캐시•쓰기 버퍼 예산** 분리 | **메모리 경쟁** 완화 |
| 긴 로그 재생으로 RTO 초과 | **체크포인트•플러시•RTO** 검증 | **재시작 지연** 통제 |

> **적용 사례**: 거래 원장의 점•범위 조회에는 B-Tree를, 고속 시계열 적재에는 LSM-Tree를 후보로 두되 실제 증폭과 p99 지연으로 선택

#### 한줄 요약

- 평균 속도뿐 아니라 정리 작업 중 가장 느린 응답과 저장장치 부담까지 비교해야 한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>


</details>

- 점•범위 읽기는 **B-Tree**, 쓰기 집중은 **LSM-Tree** 선택

#### 한줄 요약

- 바로 고칠지 모아 합칠지 결정하고, 찾기•쓰기•정리 비용을 모두 재어 선택한다.
