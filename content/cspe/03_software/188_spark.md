---
title: 스파크 Spark 및 인메모리 처리 (Spark)
date: 2026-07-05
tags: ["cspe-software"]
weight: 188
---

## Ⅰ. 개요
- 정의: 메모리 기반의 고속 데이터 처리 엔진으로 실시간 분석 및 머신러닝을 지원하는 분산 연산 플랫폼
- 배경: Hadoop의 디스크 기반 병목 해소 및 통합 분석 환경 요구
| 구분 | 내용 |
|------|------|
| 출제 의도 | RDD(Resilient Distributed Dataset)의 특성(불변성, 계보)과 지연 평가 이해 |

## Ⅱ. 구성요소
  [ Driver Program ] <-> [ Cluster Manager ] <-> [ Worker Node ]
                                              [ Executor (RAM) ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| RDD | 복구 가능한 분산 데이터 컬렉션 (인메모리 추상화) | 메모리 장부 |
| DAG | 연산 순서를 정의한 방향성 비순환 그래프 | 공정 설계도 |
| Spark SQL | 구조화된 데이터를 SQL로 처리하는 모듈 | 번역 도구 |
> 요약: 인메모리 캐싱과 최적화된 실행 계획을 통한 초고속 연산

## Ⅲ. 절차
  Code -> Transformation -> Action -> Execution
1. Transformation: Map, Filter 등 실제 연산을 수행하지 않고 계보(Lineage) 기록
2. Lazy Evaluation: Action이 호출될 때까지 실제 연산을 늦춤
3. Optimization: DAG 스케줄러가 최적의 실행 단계(Stage)로 분할
4. Execution: 워커 노드의 메모리에서 병렬로 연산 수행 및 결과 반환
> 요약: 불필요한 디스크 쓰기를 최소화한 메모리 중심의 파이프라인 처리

## Ⅳ. 문제점
- 메모리 부족(OOM) 시 성능 급락 또는 작업 실패 발생
- 스트리밍 처리 시 미세 배치(Micro-batch) 방식으로 인한 초저지연 한계

## Ⅴ. 개선방안
- Off-heap 메모리 설정 최적화 및 파티션 크기 재조정
- Structured Streaming 도입으로 실시간 처리 안정성 및 편의성 강화

## Ⅵ. 전망
- Spark 3.x의 AQE(Adaptive Query Execution) 및 벡터화 엔진 기반 차세대 데이터 분석 표준
