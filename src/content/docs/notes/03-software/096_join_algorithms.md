---
sidebar:
  order: 96
  label: "096. 조인 알고리즘: NLJ•Hash Join•Merge Join (Join Algorithms)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "조인 알고리즘: NLJ•Hash Join•Merge Join (Join Algorithms)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Join Algorithms (RDBMS 3대 조인 알고리즘)**: 두 개 이상의 테이블을 연결하여 데이터를 인출할 때 옵티마이저가 데이터 스케일, 인덱스 보유 유무, 정렬 상태에 따라 선택하는 3가지 대표 물리적 조인 수행 방식 (NLJ, Hash Join, Sort Merge Join).
- **Driving Table (Outer Table / Build Input)**: 조인 수행 시 먼저 읽혀서 조인의 주도권을 잡는 드라이빙(외부) 테이블.
- **Driven Table (Inner Table / Probe Input)**: 드라이빙 테이블의 각 튜플마다 매칭 조인을 당하는 드리븐(내부) 테이블.

</details>

- 정의/개념: RDBMS 옵티마이저가 2개 이상의 테이블 튜플을 결합할 때, 데이터 크기와 인덱스 여부에 따라 물리적으로 연산을 수행하는 3대 핵심 알고리즘인 **Nested Loop Join, Hash Join, Sort Merge Join**
- 배경/필요성: 튜플 건수(OLTP vs OLAP) 및 인덱스 배치에 적합하지 않은 조인 선택 시 쿼리 응답시간 폭증 방지, 데이터 스케일에 맞춘 최적의 조인 알고리즘 선택 체계 수립 요구성

#### 한줄 요약

- 한 명씩 찾기, 색인표 만들기, 정렬된 명단 함께 읽기 중 조건에 맞는 방법을 고른다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Nested Loop Join (NLJ)**: 드라이빙 테이블의 튜플 1건당 드리븐 테이블의 B+Tree 인덱스를 반복 루프 탐색하는 소용량/OLTP 전용 조인 방식.
- **Hash Join**: 작은 쪽 테이블(Build Input)로 메모리(Hash Area) 상에 해시 테이블을 빌드한 후, 큰 쪽 테이블(Probe Input)을 스캔하며 해시 버킷을 매칭하는 대용량/Non-Index 전용 조인 방식.
- **Sort Merge Join**: 두 테이블을 조인 키(Join Key) 기준으로 각각 미리 정렬(Sort)한 후, 두 정렬된 집합을 동시에 스캔하며 머지(Merge) 결합하는 정렬 전용 조인 방식.

</details>

- **NLJ**: OLTP 환경 최적, 드라이빙 테이블 소용량 필수, 드리븐 테이블 B+Tree 인덱스 필수
- **Hash Join**: OLAP/대용량 환경 최적, 인덱스 불필요, **`=` (Equal Join)** 조건 전용, 해시 메모리 필요
- **Sort Merge Join**: 범위원(`>, <`) 조인 가능, 조인 키 정렬 필수 (`Using filesort` 오버헤드 주의)

#### 한줄 요약

- 결과 건수, 조인 조건, 정렬 여부, 작업 메모리에 따라 가장 적은 읽기와 비교를 만드는 방식이 달라진다.

## Ⅲ. 구조 및 구성요소 (3대 조인 알고리즘 메커니즘 비교)

<details><summary>핵심 용어</summary>

- **Build Phase & Probe Phase**: Hash Join의 2단계 절차로, Build Phase에서 작은 테이블로 해시 테이블을 생성하고, Probe Phase에서 큰 테이블의 해시 값을 맞춰 매칭.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        3대 조인 알고리즘 아키텍처                      │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Nested Loop    │ 2. Hash Join      │ 3. Sort Merge Join             │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ Outer Row 1 ──────►│ Build Input ──►   │ Table A (Sort by Key)          │
│   Inner Index Scan│  [Hash Table]     │   │ (Parallel Merge Scan)      │
│ Outer Row 2 ──────►│ Probe Input ──►   │ Table B (Sort by Key)          │
│   Inner Index Scan│  [Match Bucket]   │                                │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

선의 의미: NLJ는 순차 이중 루프 스캔, Hash Join은 해시 테이블 생성 및 프로브 스캔, Sort Merge Join은 정렬 후 동시 머지 스캔을 수행하는 3대 아키텍처.

| 조인 알고리즘 | 적합 데이터 스케일 | 필수 전제 조건 | 주요 성능 결정 요소 |
|:---|:---|:---|:---|
| **Nested Loop Join** | **소용량 $\times$ 소용량/대용량 (OLTP)**| **드리븐(Inner) 테이블에 B+Tree 인덱스 존재 필수** | 드라이빙 테이블의 극소용량화 (Driving Rows $\le 100$) |
| **Hash Join** | **대용량 $\times$ 대용량 (OLAP)** | **오직 동등 조인 (`=`) 조건에서만 작동 가능** | Build Input을 담을 해시 메모리 (`PGA/Join Buffer`) |
| **Sort Merge Join** | 대용량 $\times$ 대용량 (비동등 조인)| 조인 키 정렬 필요 (`ORDER BY` 또는 정렬 인덱스) | 정렬(Sort) 연산 시 발생하는 디스크 I/O 유무 |

#### 한줄 요약

- 두 입력의 역할과 조건, 작업 공간을 정해 조인 방식을 실행한다.

## Ⅳ. 흐름도 (Hash Join 동작 2단계: Build & Probe)

<details><summary>핵심 용어</summary>

- **Hash Memory Overflow (PGA Spill)**: Build Input이 메모리(Join Buffer) 크기를 초과하여 디스크 Temp Tablespace로 유출되는 오버헤드 현상.

</details>

```text
[1. Build Phase]
 Small Table (Build Input) ──► Hash Function ──► [Memory Hash Table 생성]

[2. Probe Phase]
 Large Table (Probe Input) ──► Hash Function ──► [Hash Bucket 일치 여부 스캔] ──► Result
```

### 동작 원리

1. **Build Phase**: 상대적으로 튜플 수가 적은 소용량 테이블(Build Input)을 선택해 해시 함수를 적용하고 메모리 내 해시 테이블 빌드.
2. **Probe Phase**: 대용량 테이블(Probe Input)의 레코드를 읽어 동일한 해시 함수를 적용한 후, 해당 해시 버킷을 즉시 비교하여 매칭 튜플 렌더링.

#### 한줄 요약

- 두 명단을 작업대에서 맞추다가 공간이 부족하면 일부를 임시 보관소에 두고 나누어 처리한다.

## Ⅴ. 종류 및 비교 (NLJ vs Hash Join vs Sort Merge Join)

<details><summary>핵심 용어</summary>

- **Join Choice Matrix**: OLTP 초고속 조절은 NLJ, 대용량 통계 조인은 Hash Join, 범위/정렬 집합 조인은 Sort Merge Join 선택.

</details>

| 비교 항목 | Nested Loop Join (NLJ) | Hash Join | Sort Merge Join |
|:---|:---|:---|:---|
| 주요 사용 환경 | **OLTP (실시간 웹 서비스)** | **OLAP / DW (대용량 분석)** | 배치 / 비동등 조인 |
| 인덱스 의존성 | **매우 높음 (Inner 인덱스 필수)** | **없음 (인덱스 미사용)** | 낮음 (정렬용 인덱스 활용) |
| 조인 연산자 | 동등(`=`), 범위(`>`, `<`) 모두 가능 | **오직 동등 (`=`) 조인만 가능** | 동등(`=`), 범위(`>`, `<`) 모두 가능 |
| 메모리 사용량 | 최소 (커서 레벨 처리) | **높음 (Hash Area 메모리 필요)**| 중간~높음 (Sort Area 필요) |
| 반응 속도 | **First Row 반환 매우 빠름** | **Last Row 반환 (전체 완료 필요)**| Last Row 반환 |

#### 한줄 요약

- 소량은 하나씩 찾고, 대량 등치는 해시표로 찾고, 정렬된 명단은 나란히 읽는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Wrong Driving Table Selection**: NLJ 적용 시 대용량 테이블이 드라이빙(Outer)으로 선택되어 수백만 번의 반복 루프 인덱스 스캔이 발생하는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NLJ 조인 시 대용량 테이블이 Outer로 잘못 선택됨 | **`LEADING` 힌트 또는 서브쿼리로 소용량 드라이빙 강제**| 조인 루프 횟수 폭락 |
| Inner 테이블에 B+Tree 인덱스가 없어 NLJ 수행 시 TPS 추락 | **Inner 컬럼 인덱스 생성 또는 `USE_HASH` 힌트로 전환** | 쿼리 응답시간 회복 |
| Hash Join 시 메모리 부족으로 디스크 Spill 발생 | **`join_buffer_size` 확장 및 Build Input 크기 축소** | 디스크 I/O 병목 제거 |

> 사례: **MySQL / Oracle `/*+ USE_NL(a b) */` 및 `/*+ USE_HASH(a b) */` 힌트 튜닝**

#### 한줄 요약

- 같은 테이블도 한 고객을 찾을 때와 모든 고객을 처리할 때 알맞은 결합 방식이 다르다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **조인 수립 기준(Join Algorithm Standards)**: 데이터 건수 스케일, 인덱스 구성 상태 및 OLTP vs OLAP 서비스 유형에 의거한 체계.

</details>

- **조인 수립 기준**에 따라 OLTP 웹 서비스는 **NLJ + Inner B+Tree Index**, 대용량 OLAP 분석은 **Hash Join** 필수 수용

#### 한줄 요약

- 조인 선택 검증 기준으로 실제 데이터 양과 준비 상태에 맞는 방법인지 확인한다.
