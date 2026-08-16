---
sidebar:
  order: 116
  label: "116. 빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
  badge:
    text: "기출 • 30%"
    variant: note
title: "빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
date: "2026-08-13T22:10:00+09:00"
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

- **Hadoop (Apache Hadoop)**: 대용량 데이터의 수평 분산 저장(HDFS)과 분산 배치 연산(MapReduce)을 지원하는 오픈소스 1세대 빅데이터 처리 프레임워크.
- **HDFS (Hadoop Distributed File System)**: 수백 대의 범용 서버 디스크를 128MB 단위 분산 블록(Block)으로 쪼개고, 3중 복제(Replication Factor = 3)하여 대용량 파일 내구성 및 병렬 읽기를 보장하는 디스크 파일 시스템.
- **MapReduce**: 데이터를 Key-Value 쌍으로 변환(Map Phase)한 후, 동일 Key 데이터를 네트워크로 모아(Shuffle & Sort) 최종 집계(Reduce Phase)하는 맵-리듀스 2단계 분산 배치 연산 프로토콜.

</details>

- 정의/개념: HDFS 저장과 MapReduce 배치를 제공하는 **Hadoop**
- 배경/필요성: 단일 서버는 **대형 파일 저장•병렬 배치 처리량** 한계

#### 한줄 요약

- 파일을 작업자에게 나눠 맡기고 같은 열쇠 결과를 한곳에 모아 집계하는 처리이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Data Locality (데이터 지역성)**: 데이터가 저장된 HDFS 블록 노드로 계산 프로그램(Map Code)을 직접 이동시켜 처리하는 "Moving Computation to Data" 기법.
- **Batch Processing**: 실시간 Stream 처리가 아닌 대용량 데이터 집계용 Batch(일괄) 연산 지향.

</details>

- **Data Locality (Moving Computation, Not Data)**
- **Fault-Tolerance (블록 3중 복제 & 태스크 실패 시 재시도)**
- **Disk I/O Based Sequential Processing (Map $\rightarrow$ Disk Spill $\rightarrow$ Reduce)**

#### 한줄 요약

- 대용량 파일과 장애 재실행에는 강하지만 반복과 저지연 작업에는 느리다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **YARN (Yet Another Resource Negotiator)**: 하둡 2.0부터 도입되어 ResourceManager와 NodeManager를 통해 분산 노드의 CPU/Memory 컨테이너(Container) 자원을 할당 관리하는 오케스트레이터.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Hadoop 3대 코어 아키텍처                        │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Storage Layer (HDFS)           │ 2. Resource Layer (YARN)           │
│   • NameNode (메타데이터 맵핑)    │   • ResourceManager (전역 자원)    │
│   • DataNode (128MB 블록 3중 복제)│   • NodeManager (노드 자원 관리)   │
├───────────────────────────────────┴────────────────────────────────────┤
│ 3. Processing Layer (MapReduce Framework: Map -> Shuffle -> Reduce)    │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: HDFS 분산 저장소, YARN 자원 오케스트레이터, MapReduce 연산 프레임워크 3대 레이어가 상호작용하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| **NameNode** | 파일•블록 위치 메타데이터 관리 |
| **DataNode** | HDFS 블록 저장•복제•상태 보고 |
| **ResourceManager** | 클러스터 자원과 앱 스케줄링 |
| **NodeManager** | 노드 컨테이너 자원 실행•감시 |
| **MapReduce** | Map•Shuffle•Reduce 배치 실행 |

#### 한줄 요약

- HDFS, JobTracker, InputSplit, Mapper, Reducer로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Shuffle & Sort Phase**: Map 단계의 디스크 Output 결과를 동일 Key끼리 묶어 Reduce 노드로 전송하는 네트워크 병목 발생 단계.

</details>

```text
[HDFS 입력 블록]
      │
      ▼
1. 입력 분할 배치
      │
      ▼
2. Map 연산
      │
      ▼
3. Shuffle•Sort
      │
      ▼
4. Reduce 연산
      │
      ▼
5. HDFS 결과 기록
```

### 동작 원리

1. **입력 분할 배치**: 블록 위치를 고려해 Map 태스크 할당
2. **Map 연산**: 입력 레코드를 중간 키-값으로 변환
3. **Shuffle•Sort**: 같은 키를 Reduce 파티션으로 전송•정렬
4. **Reduce 연산**: 키별 값 집합을 집계•변환
5. **HDFS 결과 기록**: 결과 파일을 분산 블록으로 저장

#### 한줄 요약

- 파일 조각을 가까운 작업자에게 맡기고 같은 이름표의 결과를 모아 합산한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Disk vs In-Memory**: MapReduce의 물질화와 Spark의 메모리 재사용 특성 비교.

</details>

| 비교 항목 | Hadoop MapReduce (1세대) | Apache Spark (2세대) |
|:---|:---|:---|
| **연산 저장 매체** | **디스크 I/O 기반 (Map Disk Spill 후 Reduce)**| **인메모리 기반 ** |
| **처리 특성** | 단계별 물질화•대형 배치 | **중간 결과 재사용•반복 연산** |
| **적합 연산** | 대규모 1회성 Batch ETL 연산 | **반복적 머신러닝, 실시간 Stream, Interactive Query**|
| **장애 복구 방식** | 블록 재실행 (Re-Execution) | **RDD Lineage ( 계보 추적 기반 재계산)** |

#### 한줄 요약

- 분산 처리 엔진 선택 기준에서 Map은 키를 만들고 Shuffle은 같은 키를 모으며 Reduce는 집계한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Combiner (Mini-Reducer)**: Map 노드 디스크에서 네트워크로 셔플 데이터를 보내기 직전, 로컬 상에서 미리 1차 집계를 수행해 네트워크 트래픽을 폭감시키는 임시 리듀서.

</details>

| 문제 및 병목 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| Shuffle 단계에서 네트워크 전송 폭주 | Map Output 데이터 전량이 네트워크로 이동 | **Combiner(로컬 Mini-Reducer) 사전 집계 적용** |
| Data Skew (특정 Reduce 키 쏠림) | 특정 Key(예: Null Key)에 90% 트래픽 몰림 | **Custom Partitioner 및 Salting(임의 핑) 부여** |
| Small File Problem | 128MB 미만의 자잘한 파일 수백만 개 유발 | **SequenceFile / Har 묶음 파일로 컴팩션 조치** |

> 사례: **하둡 3.0 Erasure Coding 적용 및 Spark-on-YARN 대용량 배치 처리**

#### 한줄 요약

- 작은 파일을 미리 묶고 한 키에 일이 몰리지 않게 나누면 작업 준비와 마지막 병목을 줄일 수 있다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Hadoop 수립 기준(Hadoop Architecture Standards)**: HDFS 3중 복제, Data Locality, Combiner 최적화 및 Spark와의 조합성에 의거한 체계.

</details>

- 대형 파일 일괄 처리는 **MapReduce**, 반복•대화형은 Spark 선택

#### 한줄 요약

- MapReduce 적용 판단 기준은 대형 파일 분산 처리와 빠른 반복 작업을 구분한다.
