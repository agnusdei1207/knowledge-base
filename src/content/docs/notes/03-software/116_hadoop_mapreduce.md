---
sidebar:
  order: 116
  label: "116. 빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
  badge:
    text: "기출 · 30%"
    variant: note
title: "빅데이터 분산 처리: Hadoop•MapReduce•HDFS"
date: "2026-08-26T09:52:00+09:00"
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

- **3-Way Replication**: HDFS는 128MB 단위 블록을 서로 다른 랙(Rack)의 DataNode에 3중 복제하여 노드 장애 시에도 무손실을 보장.
- **Shuffle & Sort**: Map 단계에서 생성된 중간 키-값 쌍을 동일한 키별로 네트워크를 통해 특정 Reducer로 모으고 정렬하는 핵심 단계.

</details>

- 대용량 데이터 이동을 최소화하는 **데이터 지역성(Data Locality) 연산**
- 128MB 블록 3중 복제 및 실패 태스크 재시도를 통한 **강력한 결함 허용성(Fault-Tolerance)**
- 범용 하드웨어를 수평 증설하는 **선형적 수평 확장(Scale-Out) 구조**

#### 한줄 요약
- 데이터 지역성 기반 분산 연산과 블록 3중 복제로 페타바이트급 배치의 안정성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NameNode vs DataNode**: 메타데이터(파일-블록 매핑)를 RAM에 관리하는 NameNode와 실제 128MB 블록을 디스크에 저장하는 DataNode.

</details>

```text
[Apache Hadoop 3대 계층 아키텍처]
|-- Processing Layer (MapReduce: Mapper 변환 -> Shuffle & Sort 정렬 -> Reducer 집계)
|-- Resource Management Layer (YARN: ResourceManager 전역 스케줄링 -> NodeManager 컨테이너)
`-- Storage Layer (HDFS: Master NameNode 메타데이터 -> Worker DataNode 128MB 블록 3중 복제)
```

선의 의미: 계층 및 HDFS 분산 저장, YARN 자원 관리, MapReduce 연산 실행 계층 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| NameNode (마스터) | HDFS 파일 네임스페이스 및 **블록 위치 매핑 메타데이터를 메모리에 관리** | Active/Standby 이중화 |
| DataNode (워커) | 128MB 단위 블록을 로컬 디스크에 저장하고 **3중 복제 및 주기적 하트비트 보고** | 데이터 지역성 제공 |
| ResourceManager (YARN) | 클러스터 전체 CPU/RAM 자원을 스케줄링하고 **애플리케이션 컨테이너 할당** | 클러스터 자원 오케스트레이션 |
| MapReduce 엔진 | 데이터를 키-값으로 변환(Map), 셔플/정렬(Shuffle), **최종 집계(Reduce) 배치 수행** | 대용량 분산 배치 연산 |

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
   [HDFS 기록] 최종 연산 결과를 HDFS에 3중 복제 파일로 영구 커밋하고 작업 완료
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
| 처리 속도 | 배치 처리에 적합 (상대적 저속) | **MapReduce 대비 최대 100배 고속 연산** |
| 지원 워크로드 | 단순 대규모 일괄 배치 (Batch ETL) | **반복적 머신러닝, 실시간 스트리밍, 대화형 SQL**|
| 자원 오버헤드 | 메모리 요구량 낮음, 디스크 의존 | 대규모 RAM 클러스터 필요, OOM 관리 중요 |

#### 한줄 요약
- 초대규모 1회성 배치는 MapReduce, 고속 반복 연산과 실시간 처리는 Spark를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Combiner**: Shuffle 단계의 네트워크 전송량을 줄이기 위해 Map 노드 로컬에서 1차 사전 집계를 수행하는 컴포넌트.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Shuffle 단계에서 대량 데이터 네트워크 전송 폭주 | **Combiner(로컬 Mini-Reducer)를 적용하여 1차 사전 집계** | 네트워크 트래픽 80% 이상 절감 |
| 특정 Key로 데이터가 쏠리는 Data Skew 현상 | **Custom Partitioner 작성 및 Salting(임의 접두사) 기법 적용** | Reducer 부하 균등 분산 |
| 128MB 미만 Small File 수백만 개로 NameNode 메모리 고갈 | **SequenceFile 또는 HAR(Hadoop Archive)로 파일 묶음 압축** | NameNode 메타데이터 부하 해소 |
| DataNode 장애 시 복제본 유실 위험 | **Rack-Awareness(랙 인식 복제 정책) 설정으로 타 랙에 분산 복제**| 랙 전체 다운 시에도 무손실 보장 |

#### 한줄 요약
- Combiner 사전 집계, Salting 파티셔닝, 파일 아카이빙, 랙 인식 복제로 병목을 해소한다.

## Ⅶ. 결론

- 대용량 배치는 **MapReduce**, 고속 연산은 **Spark** 선택

#### 한줄 요약
- Hadoop은 HDFS의 분산 내구성과 MapReduce의 병렬 연산 모델을 통해 빅데이터 배치의 신뢰성을 완성하는 분산 컴퓨팅의 기초 프레임워크다.