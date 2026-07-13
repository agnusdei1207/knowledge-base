---
title: "빅데이터 분산 처리 — Hadoop·MapReduce·HDFS (Hadoop MapReduce)"
date: "2026-07-13T23:00:00+09:00"
tags:
  - "cspe-software"
weight: 133
extra:
  question_no: "133"
  exam_status: "기출"
  exam_history: "120회"
---

## 미리 알고가기

- HDFS는 파일을 블록으로 분할·복제하고 NameNode 메타데이터와 DataNode 블록으로 저장하는 분산 파일시스템임
- 입력 분할(Input Split)은 Map Task의 논리 입력 범위이며 HDFS 블록 경계와 항상 같지는 않음
- MapReduce는 Map이 중간 키-값을 만들고 Shuffle·Sort가 같은 키를 모은 뒤 Reduce가 집계하는 배치 처리 모델임
- YARN은 ResourceManager·NodeManager·ApplicationMaster로 응용별 자원 할당과 작업 실행을 관리함
- Combiner는 Map 출력의 로컬 집계를 줄일 수 있지만 결합·교환 가능한 연산에만 적용해야 함

## 작성 근거(검토용)

- Hadoop은 HDFS 블록·복제, YARN 자원 관리, Map·Shuffle·Reduce와 실패 재실행을 핵심 축으로 설명함
- 비교표는 단일 서버와 Hadoop MapReduce의 데이터 배치·데이터 이동·적합 조건을 대비함
- 실무 사례는 작은 파일과 키 편향을 Map Task 수·Shuffle 전송량·Reducer 처리 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: Hadoop은 HDFS 블록 복제, YARN 자원 관리, Map·Shuffle·Reduce 배치 실행으로 파일 기반 데이터를 분산 저장·처리하는 플랫폼임
- **배경/필요성**: 단일 서버의 저장·연산 한도를 넘는 로그·파일 집계를 노드별 데이터 지역성과 실패 Task 재실행으로 처리하기 위해 분산 배치 구조가 필요함

### 쉽게 이해하기 (학습용)
- 큰 파일을 여러 작업자에게 나눠 맡기고 같은 열쇠의 결과를 한곳에 모아 집계하는 배치 처리임

## Ⅱ. 특징

- HDFS가 블록을 여러 DataNode에 복제하고 NameNode가 파일·블록 위치 메타데이터를 관리함
- YARN이 컨테이너를 할당하고 입력 분할과 가까운 노드에서 Map Task 실행을 우선함
- Map 중간 키-값을 파티션별로 Shuffle·Sort한 뒤 Reduce Task가 같은 키의 값을 집계함
- Task 실패는 다른 복제 블록에서 재실행하지만 단계 사이 디스크 기록·네트워크 Shuffle로 반복 작업 지연이 증가함

### 쉽게 이해하기 (학습용)
- 대용량 파일과 장애 재실행에는 강하지만 디스크 중간 결과 때문에 반복·저지연 작업에는 느림

## Ⅲ. 종류 및 비교

| 판단 기준 | 전통 단일 서버 처리 | Hadoop MapReduce |
|:---|:---|:---|
| 데이터 배치 | 한 서버의 파일시스템·스토리지 | HDFS 블록을 DataNode에 분산·복제 |
| 데이터 이동 | 로컬 메모리·디스크 경로 중심 | 데이터 지역성 배치와 키 파티션별 Shuffle |
| 적합 조건 | 한 서버에 수용되는 저지연·반복 작업 | 파일 기반 대용량 정렬·집계·일괄 변환 |

> 요약: Hadoop MapReduce는 HDFS 블록을 입력 분할로 처리하고 키별 Shuffle·Reduce와 실패 Task 재실행으로 배치 결과를 만듦.

### 쉽게 이해하기 (학습용)
- 단일 서버는 한 작업장, Hadoop은 자료가 있는 여러 작업장에서 나눠 처리함

## Ⅳ. 설계 요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| NameNode·DataNode | 파일·블록 위치 메타데이터와 복제 블록을 각각 관리함 |
| YARN | ResourceManager가 자원을 조정하고 NodeManager가 컨테이너를 실행함 |
| 입력 분할·Map Task | 논리 입력 범위에서 레코드를 읽어 중간 키-값을 생성함 |
| Partitioner·Shuffle·Sort | 키를 Reduce 파티션에 배정하고 같은 키의 값을 전송·정렬함 |
| Reduce Task·출력 형식 | 키별 값을 집계하고 결과 파일을 HDFS에 기록함 |

```text
HDFS 블록 -> 입력 분할·Map -> Shuffle·Sort -> Reduce -> HDFS 결과
```

> 요약: HDFS·YARN이 데이터와 실행 자원을 제공하고 Map·Shuffle·Reduce가 입력 분할을 키별 결과로 변환함.

### 쉽게 이해하기 (학습용)
- 분산 파일 창고, 작업 자원 관리자, 나누기·운반·같은 키 집계 단계로 구성됨

## Ⅴ. 원리 및 절차 흐름도

```text
입력 분할 생성 -> Map 실행 -> 로컬 정렬·파티션 -> Shuffle·Sort -> Reduce·출력
```

1. **입력 분할 생성**: 입력 형식이 HDFS 파일에서 Map Task별 논리 범위를 만듦
2. **Map 실행**: 각 Task가 레코드를 읽어 중간 키-값을 생성하고 필요하면 Combiner로 로컬 집계함
3. **로컬 정렬·파티션**: 중간 키를 Reduce 파티션별로 나누고 로컬 디스크에 정렬함
4. **Shuffle·Sort**: Reduce Task가 담당 파티션을 가져와 같은 키의 값 목록으로 병합함
5. **Reduce·출력**: 키별 집계 결과를 출력 형식에 따라 HDFS에 기록함

> 요약: 입력 분할별 Map 출력은 파티션·Shuffle·Sort를 거쳐 같은 키의 Reduce 입력과 HDFS 결과로 변환됨.

### 쉽게 이해하기 (학습용)
- 각 조각을 Map하고 같은 키를 Shuffle·정렬한 뒤 Reduce 결과를 분산 파일에 씀

## Ⅵ. 실무 사례

1. 일별 접근 로그 집계는 작은 파일을 입력 분할로 병합하고 Map Task 수·작업 완료 시간을 확인함
2. 사용자별 이벤트 집계는 Combiner와 Partitioner를 적용하고 Shuffle 전송량·최대 Reducer 처리 시간을 확인함

### 쉽게 이해하기 (학습용)
- 로그 일괄 집계에 적용하고 작은 파일 수·키 쏠림·Shuffle 전송량을 확인함

## Ⅶ. 결론

- Hadoop MapReduce는 파일 규모·입력 분할·키 편향·Shuffle 전송량과 배치 완료 시간 요구를 기준으로 적용해야 함
- 대화형·반복 분석에는 다른 엔진을 검토하고 입력 분할·키 편향·실패 재실행 비용을 지속 조정해야 함

### 쉽게 이해하기 (학습용)
- 하루치 큰 정산에는 맞지만 즉시 반복 질의에는 다른 도구가 더 적합함
