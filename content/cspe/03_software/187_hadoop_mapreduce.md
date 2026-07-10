---
title: 하둡 Hadoop 및 맵리듀스 (Hadoop MapReduce)
date: 2026-07-05
tags: ["cspe-software"]
weight: 187
---

## Ⅰ. 개요
- 정의: 대용량 데이터를 분산 저장(HDFS)하고 병렬 처리(MapReduce)하는 오픈소스 프레임워크
- 배경: 범용 서버를 이용한 대용량 비정형 데이터의 분산 저장·일괄 처리 필요
| 구분 | 내용 |
|------|------|
| 출제 의도 | HDFS(저장)의 블록 구조와 MapReduce(연산)의 Map-Shuffle-Reduce 단계 파악 |

## Ⅱ. 구성요소
  [ HDFS ] -> [ Map ] -> [ Shuffle ] -> [ Reduce ] -> [ Result ]
  (Distributed Storage) (Parallel Processing)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| HDFS | 범용 서버의 로컬 디스크를 묶은 분산 파일 시스템 | 거대 창고 |
| NameNode | 파일 시스템의 메타데이터 및 블록 위치 관리 | 관리실 |
| DataNode | 실제 데이터 블록을 저장하고 복제 수행 | 보관실 |
> 요약: 데이터 근접성(Data Locality) 기반의 분산 처리 아키텍처

## Ⅲ. 절차
  Split -> Map -> Shuffle/Sort -> Reduce
1. Input Splitting: 대용량 파일을 고정 크기 블록으로 분할
2. Mapping: 각 블록에서 Key-Value 쌍으로 데이터 추출
3. Shuffling: 동일한 Key를 가진 데이터를 같은 Reduce 노드로 그룹화
4. Reducing: 그룹화된 데이터를 집계/요약하여 최종 결과 산출
> 요약: 입력을 분할하고 Map 결과를 키별로 모아 Reduce 단계에서 집계함

## Ⅳ. 문제점
- 디스크 I/O 기반 작업으로 인한 반복 연산(머신러닝 등) 속도 저하
- Batch 처리 위주 구조로 실시간 데이터 처리에 부적합

## Ⅴ. 개선방안
- Spark 등 인메모리 처리 프레임워크로의 전환 및 결합
- YARN(자원 관리자) 도입으로 다양한 연산 엔진 수용성 확보

## Ⅵ. 전망
- 클라우드 스토리지(S3 등)와 연동된 컴퓨팅-저장 분리형 현대적 데이터 레이크로 진화
