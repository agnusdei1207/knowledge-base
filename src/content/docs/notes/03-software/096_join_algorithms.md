---
sidebar:
  order: 96
  label: "096. 조인 알고리즘: NLJ•Hash•Merge"
  badge:
    text: "기출 · 70%"
    variant: note
title: "조인 알고리즘: NLJ•Hash Join•Merge Join (Join Algorithms)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 96
extra:
  question_no: "096"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출, 조인 방식별 비용 선택 중요"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **물리 조인 3대 알고리즘**: NLJ(Nested Loop Join), Hash Join, Sort Merge Join.
- **Driving Table vs Driven Table**: 조인을 주도하여 먼저 읽히는 외부 테이블(Driving/Outer)과 매칭되는 내부 테이블(Driven/Inner).

</details>

- 정의/개념: 데이터베이스 옵티마이저가 데이터 크기, 인덱스 유무, 정렬 상태에 따라 **NLJ(중첩루프), Hash Join(해시), Sort Merge Join(정렬머지)** 중 최적 방식을 선택하는 물리 조인 알고리즘
- 배경/필요성: 대용량 조인 시 부적합한 알고리즘 선택으로 인한 **중첩 반복 I/O 병목, 메모리 초과에 따른 디스크 스필(Spill) 및 질의 지연 해결 불가**

#### 한줄 요약
- 데이터 규모와 인덱스 환경에 맞추어 NLJ, Hash Join, Sort Merge Join 중 최적 알고리즘을 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **First-row Latency(최초 행 응답 속도)**: 쿼리 시작 후 첫 번째 레코드가 반환될 때까지의 시간 (NLJ가 가장 빠름).
- **Disk Spill(디스크 스필)**: 해시 테이블이나 정렬 버퍼가 메모리를 초과하여 디스크 임시 파일(TempDB)로 밀려나 급격한 I/O 지연이 발생하는 현상.

</details>

- 소량 데이터 및 실시간 웹 OLTP에서 최초 행 응답이 가장 빠른 **중첩 루프 조인(NLJ)**
- 대용량 데이터 및 동등 조인(`=`)에서 인덱스 없이도 고속 처리 가능한 **해시 조인(Hash Join)**
- 이미 정렬된 대용량 데이터나 비동등 조인(`<, >`)에 유리한 **정렬 머지 조인(Sort Merge Join)**

#### 한줄 요약
- OLTP 소량 조인은 NLJ, 대용량 분석은 Hash Join, 정렬된 대규모 배치는 Sort Merge Join을 적용한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Build Phase & Probe Phase**: 작은 테이블을 읽어 메모리 해시 테이블을 생성하는 Build 단계와 큰 테이블을 읽으며 해시 버킷을 매칭하는 Probe 단계.

</details>

```text
[3대 물리 조인 알고리즘 내부 구조]
|-- 1. 중첩 루프 조인 (Nested Loop Join: NLJ)
|   `-- Driving Table (소용량 100건) ──(1건씩 루프)──> Driven Table (B+Tree Index 탐색)
|-- 2. 해시 조인 (Hash Join: 동등 조인 '=' 전용)
|   |-- Build Phase: 소용량 Build Input으로 메모리 Hash Table 구축
|   `-- Probe Phase: 대용량 Probe Input을 읽으며 해시 버킷 고속 매칭
`-- 3. 정렬 머지 조인 (Sort Merge Join)
    |-- Sort Phase: 양쪽 테이블을 조인 키 기준으로 사전 정렬
    `-- Merge Phase: 투 포인터(Two-Pointer) 방식으로 동시 순차 스캔 병합
```

선의 의미: 계층 및 인덱스 반복(NLJ), 메모리 해시(Hash), 정렬 순차병합(Sort Merge)의 3대 아키텍처

| 조인 알고리즘 | 핵심 작동 메커니즘 | 최적 성능 조건 | 시간 복잡도 |
|:---|:---|:---|:---|
| **중첩 루프 조인 (NLJ)** | 드라이빙 행마다 **드리븐 테이블의 B+Tree 인덱스를 반복 탐색** | 소용량 드라이빙 + 드리븐 조인 키 B+Tree 인덱스 필수 | $O(M \cdot \log N)$ |
| **해시 조인 (Hash Join)** | 작은 테이블로 **해시 테이블을 빌드하고 큰 테이블로 고속 프로브** | 대용량 동등 조인(`=`) + 인덱스 부재 + 충분한 메모리 | $O(M + N)$ |
| **정렬 머지 조인 (Merge)** | 조인 키를 **사전 정렬한 후 두 집합을 투 포인터로 순차 병합** | 이미 정렬된 대용량 집합 또는 부등호(`<, >`) 조인 | $O(M \log M + N \log N)$ |

#### 한줄 요약
- NLJ(인덱스 루프), Hash Join(해시 매칭), Sort Merge(정렬 순차 병합)로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Grace Hash Join**: Build Input이 메모리(join_buffer)를 초과할 경우 디스크 파티션으로 분할하여 다단계로 해시 조인을 수행하는 알고리즘.

</details>

```text
클라이언트 조인 질의 실행 (`SELECT * FROM Users u JOIN Orders o ON u.id = o.user_id`)
        │
   1. [CBO 옵티마이저 판단] 조인 조건(`=`) 및 테이블 크기, 인덱스 유무 대조
        │
   2. [Hash Join 결정] 소용량 Users(Build)와 대용량 Orders(Probe) 선택
        │
   3. [Build Phase] Users 테이블을 읽어 `u.id` 해시 키로 메모리 Hash Table 빌드
        │
   4. [Probe Phase] Orders 테이블을 순차 스캔하며 `o.user_id`를 동일 해시 함수로 매칭
        │
   5. 해시 버킷 일치 행을 결합하여 결과 레코드 스트리밍 반환
```

#### 한줄 요약
- 쿼리 분석 → CBO 알고리즘 선택 → Build 해시 테이블 생성 → Probe 순차 매칭 → 결과 반환 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NLJ vs Hash Join vs Sort Merge**: OLTP와 OLAP, 인덱스 유무 및 조인 연산자에 따른 3대 알고리즘 특성 비교.

</details>

| 비교 항목 | 중첩 루프 조인 (NLJ) | 해시 조인 (Hash Join) | 정렬 머지 조인 (Sort Merge Join) |
|:---|:---|:---|:---|
| 지원 연산자 | **모든 연산자 (`=, <, >, LIKE`)**| **동등 조인 (`=`) 전용** | **모든 연산자 (`=, <, >`)** |
| 인덱스 의존성 | **Driven 테이블 인덱스 필수** | **인덱스 전혀 불필요** | 인덱스 없어도 가능 (정렬 필요) |
| 메모리 소모 | 매우 적음 | **해시 테이블용 메모리 필요** | 정렬용 메모리(Sort Area) 필요 |
| 주 활용 분야 | **웹/앱 실시간 OLTP 트랜잭션** | **빅데이터/DW 대용량 OLAP 분석** | 배치 집계, 이미 정렬된 대용량 처리 |

#### 한줄 요약
- OLTP 실시간에는 NLJ, 대용량 동등 조인에는 Hash Join, 정렬된 대규모 집합에는 Sort Merge Join을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **LEADING 힌트**: 옵티마이저가 큰 테이블을 드라이빙으로 잘못 지정했을 때 소용량 테이블이 먼저 읽히도록 강제하는 지시자 (`/*+ LEADING(u) */`).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NLJ 수행 시 대용량 테이블이 Driving으로 잘못 선택 | **`LEADING(u)` 힌트 또는 서브쿼리로 소용량 드라이빙 강제** | 조인 루프 횟수 및 인덱스 탐색 비용 급감 |
| Driven 테이블의 조인 키 인덱스 부재로 NLJ 성능 폭락 | **Driven 컬럼에 B+Tree 인덱스 생성 또는 Hash Join으로 전환** | 인덱스 스캔 복원 및 쿼리 속도 10배 향상 |
| Hash Join 시 메모리 초과로 디스크 스필(Disk Spill) 발생 | **`join_buffer_size` 확장 및 WHERE 절 선필터링으로 Build 축소** | 디스크 I/O 병목 원천 차단 |
| 대용량 데이터에서 잘못된 Sort Merge Join으로 CPU 과부하 | **인덱스 활용 또는 Hash Join 강제 힌트(`/*+ USE_HASH(o) */`)** | 무거운 디스크 정렬(filesort) 제거 |

#### 한줄 요약
- 소용량 드라이빙 강제, Driven 인덱스 확보, 메모리 버퍼 확장, 정렬 제거로 최적화한다.

## Ⅶ. 결론

- 성공적인 조인 성능을 위해 **실시간 OLTP 서비스에는 소용량 드라이빙과 Driven 인덱스를 완비한 NLJ를 표준 적용**하고, **대용량 배치 및 DW 분석에는 Hash Join을 적극 활용**하여 최적의 처리 속도 확보

#### 한줄 요약
- 조인 알고리즘은 데이터 규모와 인덱스 유무에 따라 시스템 성능을 좌우하는 핵심 엔진 기술이며, 워크로드에 맞는 최적 선택이 필수적이다.