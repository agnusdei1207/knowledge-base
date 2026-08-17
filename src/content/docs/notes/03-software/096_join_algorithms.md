---
sidebar:
  order: 96
  label: "096. 조인 알고리즘: NLJ•Hash Join•Merge Join (Join Algorithms)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "조인 알고리즘: NLJ•Hash Join•Merge Join (Join Algorithms)"
date: "2026-08-17T22:50:00+09:00"
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

- **3대 물리 조인 알고리즘(NLJ, Hash Join, Sort Merge Join)**: 외부 행마다 내부 인덱스를 반복 탐색하는 NLJ, 메모리 해시 테이블을 빌드하여 매칭하는 Hash Join, 조인 키 기준 정렬 후 병합하는 Sort Merge Join.
- **조인 병목 및 디스크 스필(Join Bottleneck & Spill)**: 잘못된 드라이빙 테이블 선택이나 메모리 부족으로 인해 수백만 번의 반복 I/O 또는 디스크 임시 파일 쓰기가 발생하는 현상.

</details>

- 정의/개념: 데이터베이스 옵티마이저가 데이터 크기, 인덱스 유무, 정렬 상태에 따라 **NLJ(중첩루프), Hash Join(해시), Sort Merge Join(정렬머지)** 중 최적 방식을 선택하는 물리 조인 알고리즘
- 배경/필요성: 대용량 조인 시 부적합한 알고리즘 선택으로 인한 **중첩 반복 I/O 병목, 메모리 초과에 따른 디스크 스필(Spill) 및 질의 지연 위험** 직면

#### 한줄 요약

- 데이터 규모와 인덱스 환경에 맞추어 NLJ, Hash Join, Sort Merge Join 중 최적 알고리즘을 선택하여 조인 성능을 극대화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Driving Table(Outer Table)**: 조인을 주도하여 먼저 읽히는 테이블로, NLJ에서는 건수가 가장 적은 소용량 테이블을 선정해야 함.
- **Driven Table(Inner Table)**: Driving 테이블의 각 행마다 매칭되는 테이블로, 반드시 조인 컬럼에 B+Tree 인덱스가 존재해야 함.

</details>

- 소량 데이터 및 OLTP 환경에서 최초 행 응답(First Row)이 빠른 **중첩 루프 조인(NLJ)**
- 대용량 데이터 및 동등 조인(`=`)에서 인덱스 없이도 고속 처리 가능한 **해시 조인(Hash Join)**
- 이미 정렬된 대용량 데이터나 비동등 조인(`<, >`)에 유리한 **정렬 머지 조인(Sort Merge Join)**

#### 한줄 요약

- OLTP 소량 조인은 NLJ, 대용량 분석은 Hash Join, 정렬된 대규모 배치는 Sort Merge Join을 적용

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Build Phase & Probe Phase**: Hash Join에서 작은 테이블로 해시 테이블을 메모리에 구성하는 단계(Build)와 큰 테이블을 읽으며 해시 버킷을 매칭하는 단계(Probe).

</details>

```text
[ 3대 조인 알고리즘 물리 처리 구조도 ]

 1. [ Nested Loop Join (NLJ) ]
    Outer Table (100건) ──(한 건씩 루프)──► Inner Table B+Tree Index 탐색

 2. [ Hash Join ]
    Small Table ──► [ 메모리 Hash Table 빌드 (Build Phase) ]
                                 ▲
    Large Table ──► [ 해시 버킷 매칭 스캔 (Probe Phase) ]

 3. [ Sort Merge Join ]
    Table A (정렬) ───┐
                      ├──► [ 동시 순차 투 포인터 머지 (Merge Scan) ]
    Table B (정렬) ───┘
```

선의 의미: 인덱스 기반 반복 루프(NLJ), 메모리 해시 매칭(Hash), 정렬 후 순차 병합(Sort Merge)의 3대 물리 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 중첩 루프 조인 (NLJ) | 드라이빙 테이블의 각 행마다 **드리븐 테이블의 B+Tree 인덱스를 반복 탐색** |
| 해시 조인 (Hash Join) | 소용량 Build Input으로 **해시 테이블을 빌드하고 대용량 Probe Input과 고속 대조** |
| 정렬 머지 조인 (Sort Merge) | 조인 키를 기준으로 **두 테이블을 사전 정렬한 후 동시 순차 스캔으로 병합** |
| 조인 버퍼 (Join Buffer) | 해시 테이블 빌드 및 정렬 연산을 위해 **메모리(PGA/Work Area) 자원 할당** |

#### 한줄 요약

- NLJ(인덱스 루프), Hash Join(해시 매칭), Sort Merge(정렬 순차 병합)로 구성된 조인 아키텍처

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Hash Join 2단계 처리 절차**: 소용량 테이블 해시 빌드 $\to$ 메모리 버퍼 적재 $\to$ 대용량 테이블 프로브 스캔 $\to$ 매칭 결과 반환.

</details>

```text
[ Hash Join 2단계 실행 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. Build Phase: 소용량 테이블(Build)   │
 │    - 해시 함수 적용 및 메모리 해시 생성│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Probe Phase: 대용량 테이블(Probe)   │
 │    - 행을 읽어 동일 해시 함수 대입    │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 해시 버킷 매칭 검사 및 튜플 결합    │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 최종 조인 결과 셋 반환              │
 └────────────────────────────────────────┘
```

### 동작 원리

1. Build Phase: 카디널리티가 작은 테이블(Build Input)을 선택하여 조인 키에 해시 함수를 적용하고 메모리 상에 해시 테이블을 구축.
2. Probe Phase: 큰 테이블(Probe Input)을 순차 스캔하며 각 레코드의 조인 키에 동일한 해시 함수를 적용.
3. 버킷 매칭: 계산된 해시 값으로 메모리 내 해시 버킷을 즉시 조회하여 실제 키 일치 여부를 검증.
4. 결과 반환: 일치하는 행을 결합하여 클라이언트에 최종 결과 집합을 반환.

#### 한줄 요약

- 소용량 해시 빌드 $\to$ 대용량 프로브 스캔 $\to$ 버킷 일치 검증 $\to$ 결과 반환의 4단계 절차

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NLJ vs Hash Join vs Sort Merge**: OLTP와 OLAP, 인덱스 유무 및 조인 조건식에 따른 3대 알고리즘 비교.

</details>

| 구분 | Nested Loop Join (NLJ) | Hash Join | Sort Merge Join |
|:---|:---|:---|:---|
| **적용 기준** | 소량 데이터 조회 및 실시간 OLTP 트랜잭션 | 대용량 데이터 분석 및 인덱스가 없는 환경 | 정렬이 이미 완료된 대용량 데이터 및 범위 조인 |
| **핵심 특징** | **드라이빙 행마다 B+Tree 인덱스 탐색, 빠른 첫 행 반환** | **메모리 해시 테이블 빌드 후 프로브 매칭 (동등 조인 전용)** | **조인 키 기준 사전 정렬 후 투 포인터 순차 병합** |
| **한계** | 대용량 처리 시 반복 랜덤 I/O로 성능 급락 | 대용량 빌드 시 메모리 초과(Disk Spill) 발생 | 정렬되지 않은 대용량 데이터의 정렬 비용 폭증 |

#### 한줄 요약

- OLTP 실시간에는 NLJ, 대용량 동등 조인에는 Hash Join, 정렬된 대규모 집합에는 Sort Merge Join을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **디스크 스필(Disk Spill)**: Hash Join의 Build Input 또는 Sort Merge의 정렬 대상이 메모리(join_buffer, sort_area)를 초과하여 임시 디스크로 튕겨 나가는 성능 저하 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NLJ 수행 시 대용량 테이블이 Outer로 잘못 지정 | **`LEADING` 힌트 또는 서브쿼리로 소용량 드라이빙 강제** | 조인 루프 횟수 및 인덱스 탐색 비용 급감 |
| Inner 테이블의 조인 키 인덱스 부재로 NLJ 성능 폭락 | **Inner 컬럼에 B+Tree 인덱스 생성 또는 `USE_HASH` 힌트로 전환** | 인덱스 스캔 복원 또는 고속 해시 조인 전환 |
| Hash Join 시 Build Input 메모리 초과로 디스크 Spill 발생 | **`join_buffer_size` 확장 및 WHERE 절 선필터링으로 Build 축소** | 디스크 I/O 병목 원천 차단 |

#### 한줄 요약

- 소용량 드라이빙 강제, Inner 인덱스 확보, 메모리 버퍼 확장을 통해 조인 병목을 제거

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **조인 최적화 원칙(Join Optimization Principle)**: 옵티마이저가 쿼리 환경에 맞추어 올바른 알고리즘을 선택할 수 있도록 통계와 인덱스를 완비하고 필요시 힌트로 제어하는 엔지니어링 원칙.

</details>

- **조인 알고리즘**은 RDBMS 성능의 승패를 가르는 핵심 엔진 기술이며, 트랜잭션 특성과 데이터 볼륨에 맞추어 인덱스 설계와 메모리 튜닝을 병행하여 최적의 조인 효율을 달성해야 함

#### 한줄 요약

- NLJ, Hash Join, Sort Merge Join의 장단점을 파악하고 데이터 규모에 부합하는 최적 조인을 구현
