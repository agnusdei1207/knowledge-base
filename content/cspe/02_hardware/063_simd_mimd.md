---
title: "SIMD·MIMD 프로세서 (SIMD MIMD)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 63
extra:
  question_no: "063"
  exam_status: "기출"
  exam_history: "131회, 134회"
---

## 미리 알고가기

- SIMD는 같은 명령을 여러 데이터에 동시에 적용하는 구조임
- MIMD는 여러 처리기가 서로 다른 명령을 독립적으로 수행하는 구조임
- 선택 기준은 데이터 규칙성, 분기 패턴, 동기화 비용임

## Ⅰ. 개요

- **정의/개념**: SIMD와 MIMD 프로세서는 병렬 연산을 하나의 명령이 여러 데이터에 반복되는 구조로 처리할지, 여러 코어가 독립 명령 흐름을 동시에 수행하는 구조로 처리할지 구분하는 병렬 처리 아키텍처임
- **배경/필요성**: 영상과 행렬 같은 규칙적 반복 계산과 서버 트랜잭션 같은 독립 작업은 병렬화 방식이 다르므로, 데이터 특성과 제어 특성에 맞는 구조 선택이 필요함

## Ⅱ. 특징

- SIMD는 제어 오버헤드가 작고 규칙적 데이터 병렬에 강함
- MIMD는 분기와 비정형 작업을 독립적으로 처리할 수 있음
- SIMD는 lane 유휴와 분기 발산이 약점임
- MIMD는 동기화와 통신과 부하 분산 비용이 핵심 병목임

## Ⅲ. 종류 및 비교

| 판단 기준 | SIMD | MIMD |
|:---|:---|:---|
| 제어 구조 | 단일 명령 흐름 | 다중 독립 명령 흐름 |
| 강점 | 벡터, 행렬, 미디어 연산 | 서버, 시뮬레이션, 멀티코어 작업 |
| 약점 | 불규칙 분기와 비연속 메모리 | 동기화와 공유 자원 경합 |
| 대표 구현 | 벡터 유닛, GPU 내부 | 멀티코어 CPU, 클러스터 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| SIMD Control, Lane | 하나의 제어가 여러 lane에 같은 명령을 배포하며 lane 활용률이 성능을 좌우함 |
| MIMD Core | 각 코어가 독립 상태와 명령 흐름을 가져 다양한 작업을 병렬로 실행함 |
| Shared Memory, Interconnect | 데이터 교환과 동기화를 담당하며 MIMD 병목의 중심이 됨 |
| Synchronization Mechanism | barrier, lock, message passing이 결과 정합성과 오버헤드를 동시에 결정함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 작업 특성 분석 | --> | SIMD/MIMD 선택 | --> | 병렬 실행      | --> | 결과 병합/동기화 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **작업 특성 분석**: 데이터 규칙성과 분기와 독립성을 확인함
2. **SIMD 또는 MIMD 선택**: 반복형이면 SIMD를, 독립형이면 MIMD를 우선 고려함
3. **병렬 실행**: lane 또는 코어 단위로 실제 연산을 수행함
4. **결과 병합 및 동기화**: reduction이나 barrier나 message passing으로 정합성을 맞춤

## Ⅵ. 문제점 및 해결 방안

1. 문제: SIMD는 조건 분기가 많거나 메모리 접근이 흩어지면 lane 유휴가 늘어 처리량이 급감할 수 있음
   - 해결방안: 데이터 정렬과 predication을 적용하고 lane utilization과 branch efficiency로 검증함
2. 문제: MIMD는 락과 barrier가 많아질수록 병렬 이득보다 동기화 비용이 커질 수 있음
   - 해결방안: 작업 분할과 lock-free 구조를 적용하고 synchronization wait time과 speedup으로 검증함
3. 문제: 두 구조 모두 메모리 대역폭이 부족하면 코어 수와 lane 수를 늘려도 성능이 거의 오르지 않을 수 있음
   - 해결방안: cache blocking과 NUMA-aware 배치를 적용하고 bandwidth utilization과 memory stall로 검증함

## Ⅶ. 적용 사례

- 이미지 처리 커널에서는 SIMD 벡터화를 적용하고 확인 지표는 lane utilization과 pixels per second임
- 멀티코어 웹 서버에서는 MIMD 스레드 병렬을 적용하고 확인 지표는 throughput과 lock wait time임
- HPC 코드 최적화에서는 루프는 SIMD로 태스크는 MIMD로 나누고 확인 지표는 speedup과 scaling efficiency임

## Ⅷ. 결론

SIMD와 MIMD의 차이는 코어 수보다 병렬성의 모양에 있으므로, 데이터 규칙성과 동기화 비용을 먼저 본 뒤 구조를 선택해야 함.
