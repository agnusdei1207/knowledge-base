---
sidebar:
  order: 116
  label: "116. 빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
  badge:
    text: "기출 · 30%"
    variant: note
title: "빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
date: "2026-08-17T23:55:00+09:00"
tags:
  - "notes-software"
weight: 116
extra:
  question_no: "116"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "120회 기출 후 저빈도, 배치 분산처리 기초"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Hadoop 3대 코어(HDFS, MapReduce, YARN)**: 대용량 분산 파일 시스템(HDFS), 데이터 지역성 기반 분산 배치 연산(MapReduce), 클러스터 자원 관리 오케스트레이터(YARN).
- **데이터 지역성(Data Locality)**: 대용량 데이터를 네트워크로 전송하지 않고 데이터가 저장된 물리 노드로 연산 코드(Mapper)를 직접 이동시켜 실행하는 원칙.

</details>

- 정의/개념: 대규모 빅데이터의 분산 저장을 위한 **HDFS와 데이터 지역성 기반 병렬 배치 연산을 수행하는 MapReduce 및 YARN** 프레임워크
- 배경/필요성: 페타바이트급 비정형 데이터 폭증 시 기존 단일 서버 및 RDBMS의 **스토리지 용량 한계, 네트워크 I/O 병목 및 병렬 연산 처리 불가 위험** 직면

#### 한줄 요약

- HDFS 분산 파일 저장과 MapReduce 병렬 처리를 결합하여 범용 서버 클러스터에서 대용량 배치를 안정적으로 실행

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **블록 3중 복제(3-Way Replication)**: HDFS는 128MB 단위 블록을 서로 다른 랙(Rack)의 DataNode에 3중 복제하여 노드 장애 시에도 데이터 무손실을 보증.
- **Shuffle & Sort**: Map 단계에서 생성된 중간 키-값 결과를 동일한 키를 가진 Reducer 노드로 파티셔닝하고 정렬하여 전송하는 단계.

</details>

- 대용량 데이터 이동을 최소화하는 **데이터 지역성(Data Locality) 연산**
- 128MB 블록 3중 복제 및 태스크 재시도를 통한 **강력한 결함 허용성(Fault-Tolerance)**
- 범용 하드웨어(Commodity Hardware)를 수평 증설하는 **선형적 수평 확장(Scale-Out)** #### 한줄 요약

- 데이터 지역성 기반 분산 연산과 블록 3중 복제로 페타바이트급 배치 처리의 안정성을 보증

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NameNode vs DataNode**: 메타데이터(파일-블록 매핑)를 메모리에서 관리하는 마스터 NameNode와 실제 128MB 블록을 디스크에 저장하는 슬레이브 DataNode.

</details>

```text
[ Apache Hadoop 3대 레이어 아키텍처 구조도 ]

 ┌────────────────────────────────────────────────────────────────────────┐
 │ 1. Processing Layer (MapReduce)                                        │
 │   - Mapper (Key-Value 변환) ──► Shuffle & Sort ──► Reducer (집계 연산) │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 2. Resource Management Layer (YARN)                                    │
 │   - ResourceManager (클러스터 전역 자원) ──► NodeManager (컨테이너 관리)│
 ├────────────────────────────────────────────────────────────────────────┤
 │ 3. Storage Layer (HDFS)                                                │
 │   - NameNode (메타데이터 맵핑) ──► DataNode (128MB 블록 3중 복제)       │
 └────────────────────────────────────────────────────────────────────────┘
```

선의 의미: HDFS 분산 파일 저장, YARN 자원 할당, MapReduce 연산 실행이 계층적으로 결합된 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| NameNode (마스터) | HDFS 파일 네임스페이스 및 **블록 위치 매핑 메타데이터를 메모리에 관리** |
| DataNode (워커) | 128MB 단위 블록을 로컬 디스크에 저장하고 **3중 복제 및 주기적 하트비트 보고** |
| ResourceManager (YARN) | 클러스터 전체의 CPU/Memory 자원을 스케줄링하고 **애플리케이션 컨테이너 할당** |
| MapReduce 엔진 | 입력을 키-값으로 변환(Map), 셔플/정렬(Shuffle), **최종 집계(Reduce) 배치 수행** |

#### 한줄 요약

- NameNode/DataNode(저장), YARN(자원 관리), MapReduce(연산)가 유기적으로 연동

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MapReduce 5단계 처리 파이프라인**: 입력 분할 $\to$ Map 연산 $\to$ Shuffle & Sort $\to$ Reduce 연산 $\to$ HDFS 결과 기록.

</details>

```text
[ MapReduce 5단계 배치 연산 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 입력 분할(InputSplit) 및 매퍼 할당  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Map 연산: 레코드를 중간 <Key, Value> 변환
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Shuffle & Sort: 동일 Key 그룹화 및 정렬
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Reduce 연산: Key별 집계 및 비즈니스 연산
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. HDFS 결과 파일 3중 복제 기록        │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 입력 분할: HDFS 블록 단위로 InputSplit을 생성하고 데이터가 위치한 노드에 Mapper 태스크를 할당(Data Locality).
2. Map 연산: 각 Mapper가 로컬 블록 데이터를 읽어 중간 `<Key, Value>` 쌍으로 변환 후 로컬 디스크에 임시 저장.
3. Shuffle & Sort: 파티셔너에 의해 동일한 Key를 가진 데이터들이 네트워크를 통해 특정 Reducer 노드로 이동하고 정렬.
4. Reduce 연산: Reducer가 정렬된 `<Key, List<Value>>` 집합을 받아 최종 집계 및 변환 연산을 수행.
5. HDFS 결과 기록: 연산 결과를 HDFS에 3중 복제 파일로 저장하고 작업을 종료.

#### 한줄 요약

- 입력 분할 $\to$ Map 변환 $\to$ Shuffle 정렬 $\to$ Reduce 집계 $\to$ HDFS 기록의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MapReduce vs Spark**: 디스크 I/O 기반의 1세대 일괄 배치 엔진(MapReduce)과 인메모리 RDD 기반의 2세대 고속 분산 엔진(Spark).

</details>

| 구분 | Hadoop MapReduce (1세대) | Apache Spark (2세대) |
|:---|:---|:---|
| **적용 기준** | 초대규모 1회성 일괄(Batch) ETL 작업 | 반복적 머신러닝, 실시간 스트리밍, 대화형 쿼리 |
| **핵심 특징** | **디스크 I/O 기반 단계별 물질화, 단순성, 안정성** | **인메모리 RDD 기반 연산, 최대 100배 고속 처리** |
| **한계** | 중간 결과를 매번 디스크에 써서 지연시간 증가 | 대규모 클러스터 메모리(RAM) 비용 및 OOM 위험 |

#### 한줄 요약

- 단순 대규모 1회성 배치는 MapReduce, 고속 반복 연산과 실시간 처리는 Spark를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Combiner(로컬 미니 리듀서)**: Shuffle 단계에서 네트워크 전송량을 줄이기 위해 Map 노드 로컬에서 1차 집계를 먼저 수행하는 최적화 컴포넌트.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Shuffle 단계에서 대량 데이터 네트워크 전송 폭주 | **Combiner(로컬 Mini-Reducer)를 적용하여 1차 사전 집계** | 네트워크 트래픽 80% 이상 절감 |
| 특정 Key(Null 등)로 데이터가 몰리는 Data Skew 현상 | **Custom Partitioner 작성 및 Salting(임의 접두사) 기법 적용** | Reducer 부하 균등 분산 |
| 128MB 미만의 자잘한 Small File 수백만 개로 NameNode 메모리 고갈 | **SequenceFile / HAR(Hadoop Archive)로 파일 묶음 압축** | NameNode 메타데이터 부하 해소 |

#### 한줄 요약

- Combiner 사전 집계, Salting 파티셔닝, 파일 아카이빙을 통해 하둡 클러스터의 병목을 해소

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **빅데이터 생태계 진화(Ecosystem Evolution)**: Hadoop HDFS/YARN 인프라 위에 Spark, Hive, Presto 등 최신 분산 엔진이 결합되는 현대적 데이터 플랫폼.

</details>

- **Hadoop과 MapReduce** 기반 빅데이터 분산 처리의 기초 표준을 정립한 기술이며, 현대 데이터 레이크하우스 환경에서도 HDFS의 높은 내구성과 YARN의 자원 스케줄링을 기반으로 대규모 배치 파이프라인을 견고하게 유지 발전시켜야 함

#### 한줄 요약

- HDFS의 분산 내구성과 MapReduce의 병렬 처리 모델을 통해 빅데이터 배치의 신뢰성을 완성
