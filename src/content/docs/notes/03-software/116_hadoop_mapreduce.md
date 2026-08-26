---
sidebar:
  order: 116
  label: "116. 빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
  badge:
    text: "기출 · 30%"
    variant: note
title: "빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
date: "2026-08-26T13:10:10+09:00"
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

- **Hadoop**: HDFS 분산 파일 시스템, MapReduce 분산 처리 엔진, YARN 자원 관리자로 구성된 오픈소스 빅데이터 프레임워크.
- **Data Locality(데이터 지역성)**: 대용량 데이터를 네트워크로 전송하지 않고 데이터가 저장된 물리 노드로 연산 코드를 직접 보내 실행하는 원칙.

</details>

- 정의/개념: 대규모 빅데이터 저장을 위한 **HDFS와 데이터 지역성 기반 병렬 배치 연산을 수행하는 MapReduce 및 YARN** 프레임워크
- 배경/필요성: 페타바이트급 비정형 데이터 폭증 시 기존 단일 서버 및 RDBMS의 **스토리지 용량 한계, 네트워크 I/O 병목 및 병렬 연산 불가 해결 불가**

#### 한줄 요약
- HDFS 분산 저장과 MapReduce 병렬 처리를 결합하여 범용 서버에서 대용량 배치를 안정적으로 실행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **HDFS 복제**: 설정된 블록 크기와 복제 계수에 따라 여러 DataNode에 블록을 배치하는 기능.
- **Shuffle & Sort**: Map 단계에서 생성된 중간 키-값 쌍을 동일한 키별로 네트워크를 통해 특정 Reducer로 모으고 정렬하는 핵심 단계.

</details>

- 대용량 데이터 이동을 최소화하는 **데이터 지역성(Data Locality) 연산**
- 블록 복제와 실패 태스크 재시도를 통한 **결함 허용성**
- 범용 하드웨어를 수평 증설하는 **Scale-Out 구조**

#### 한줄 요약
- 데이터 지역성·블록 복제·태스크 재시도로 배치 장애를 복구한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NameNode vs DataNode**: 메타데이터(파일-블록 매핑)를 RAM에 관리하는 NameNode와 실제 128MB 블록을 디스크에 저장하는 DataNode.

</details>

```text
[Apache Hadoop]
|-- 처리 계층
|   `-- MapReduce
|-- 자원 관리 계층
|   `-- YARN
`-- 저장 계층
    |-- NameNode
    `-- DataNode
```

선의 의미: 계층 및 HDFS 분산 저장, YARN 자원 관리, MapReduce 연산 실행 계층 구조

| 구성요소 | 책임 |
|:---|:---|
| NameNode | 파일·블록 위치 **메타데이터** 관리 |
| DataNode | 데이터 블록 저장과 상태 보고 |
| YARN | 클러스터 자원과 컨테이너 할당 |
| MapReduce | Map·Shuffle·Reduce 배치 수행 |

#### 한줄 요약
- NameNode/DataNode(저장), YARN(자원 관리), MapReduce(연산)가 유기적으로 연동된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MapReduce 5단계 파이프라인**: 입력 분할 $\to$ Map 연산 $\to$ Shuffle & Sort $\to$ Reduce 연산 $\to$ HDFS 결과 저장.

</details>

```text
클라이언트가 MapReduce 대용량 배치 작업 제출
        │
   [입력 분할] HDFS 블록 단위로 InputSplit 생성 후 Data Locality 노드에 Mapper 할당
        │
   [Map 연산] 각 Mapper가 블록 데이터를 읽어 중간 `<Key, Value>` 쌍으로 변환 후 로컬 디스크 기록
        │
   [Shuffle & Sort] 동일한 Key를 가진 데이터들이 네트워크를 통해 특정 Reducer 노드로 이동 및 정렬
        │
   [Reduce 연산] Reducer가 정렬된 `<Key, List<Value>>` 집합을 받아 최종 집계 및 변환 연산 수행
        │
   [HDFS 기록] 결과를 설정된 복제 정책으로 저장
```

#### 한줄 요약
- 입력 분할 → Map 변환 → Shuffle 정렬 → Reduce 집계 → HDFS 기록 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MapReduce vs Spark**: 디스크 I/O 기반 일괄 배치 엔진(MapReduce)과 인메모리 RDD 기반 분산 엔진(Spark).

</details>

| 비교 항목 | Hadoop MapReduce (1세대) | Apache Spark (2세대) |
|:---|:---|:---|
| 중간 데이터 저장 | **매 단계마다 로컬 디스크 I/O 발생** | **인메모리(RAM) 캐싱 및 RDD 계보(Lineage)**|
| 처리 방식 | 단계별 디스크 중심 배치 | **인메모리 반복 연산** 지원 |
| 지원 워크로드 | 대규모 일괄 배치 | 반복 ML·스트리밍·대화형 SQL |
| 자원 오버헤드 | 메모리 요구량 낮음, 디스크 의존 | 대규모 RAM 클러스터 필요, OOM 관리 중요 |

#### 한줄 요약
- 초대규모 1회성 배치는 MapReduce, 고속 반복 연산과 실시간 처리는 Spark를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Combiner**: Shuffle 단계의 네트워크 전송량을 줄이기 위해 Map 노드 로컬에서 1차 사전 집계를 수행하는 컴포넌트.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Shuffle 단계의 네트워크 전송 증가 | 결합 가능한 연산에 **Combiner** 적용 | 중간 데이터 전송량 감소 |
| 특정 Key로 데이터가 쏠리는 Data Skew 현상 | **Custom Partitioner 작성 및 Salting(임의 접두사) 기법 적용** | Reducer 부하 균등 분산 |
| 128MB 미만 Small File 수백만 개로 NameNode 메모리 고갈 | **SequenceFile 또는 HAR(Hadoop Archive)로 파일 묶음 압축** | NameNode 메타데이터 부하 해소 |
| DataNode 장애의 복제본 유실 위험 | **Rack-Awareness** 기반 분산 복제 | 단일 랙 장애의 데이터 손실 위험 감소 |

#### 한줄 요약
- Combiner 사전 집계, Salting 파티셔닝, 파일 아카이빙, 랙 인식 복제로 병목을 해소한다.

## Ⅶ. 결론

- 디스크 중심 일괄 배치는 **MapReduce**, 반복 연산은 **Spark** 선택

#### 한줄 요약
- Hadoop은 HDFS의 분산 내구성과 MapReduce의 병렬 연산 모델을 통해 빅데이터 배치의 신뢰성을 완성하는 분산 컴퓨팅의 기초 프레임워크다.
