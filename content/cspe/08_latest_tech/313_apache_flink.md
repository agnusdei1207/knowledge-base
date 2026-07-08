---
title: "Apache Flink 스트림 처리 (Apache Flink)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 313
extra:
  question_no: "313"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- Apache Flink는 stateful streaming을 기본 모델로 삼는 분산 처리 엔진임
- event time, watermark, checkpoint, savepoint가 핵심 운영 개념임
- 배치도 처리하지만 강점은 낮은 지연의 실시간 스트림 연산에 있음

## Ⅰ. 개요

- **정의/개념**: Apache Flink는 연속 스트림을 기본 추상화로 사용하면서 stateful 연산과 event time 처리와 정확한 복구를 지원하는 분산 데이터 처리 엔진임
- **배경/필요성**: 실시간 분석과 이상 탐지와 스트림 ETL이 보편화되면서 낮은 지연과 정밀한 상태 관리와 exactly-once 수준 복구를 동시에 제공하는 엔진 수요가 커짐

## Ⅱ. 특징

- true streaming 모델이라 micro-batch보다 낮은 지연 처리에 유리함
- 상태 저장과 checkpoint 체계가 강해 복잡한 집계와 조인과 CEP 구현에 적합함
- event time과 watermark 중심 처리로 지연 도착 이벤트 대응이 비교적 정교함
- 상태와 운영 복잡도가 커질수록 checkpoint 비용과 장애 대응 난도가 빠르게 상승함

## Ⅲ. 종류 및 비교

| 판단 기준 | Apache Flink | Spark Structured Streaming | Kafka Streams |
|:---|:---|:---|:---|
| 처리 모델 | native streaming | micro-batch 중심 | embedded stream library |
| 상태 처리 | 강함 | 강함 | 애플리케이션 내장형 |
| 대표 강점 | 낮은 지연과 event time | Spark 생태계 통합 | 단순 배포 |
| 대표 용도 | 대규모 실시간 연산 | 배치+스트림 통합 | 애플리케이션 스트림 처리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Job Manager | 작업 스케줄링과 체크포인트 조정과 장애 복구를 총괄해 Flink 클러스터 제어를 담당하는 중앙 관리 계층임 |
| Task Managers | 연산자를 실제 병렬 실행하고 로컬 상태를 처리해 스트림 데이터를 분산 처리하는 실행 계층임 |
| Operator State and Keyed State | 집계와 조인과 패턴 탐지를 위해 연산 상태를 유지하며 실시간 연산 정확도를 좌우하는 핵심 저장 계층임 |
| Checkpoint and Savepoint | 주기적 상태 스냅샷과 운영 이전 지점을 제공해 장애 복구와 버전 업그레이드의 기준점을 만드는 복구 계층임 |
| Source and Sink Connectors | Kafka와 파일과 데이터베이스 등 외부 시스템과 연결해 파이프라인 입출력을 담당하는 통합 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Source      | -> | Task Manager| -> | State / CP  | -> | Sink        |
+-------------+    +-------------+    +-------------+    +-------------+
        ^                    |
        |                    v
        +------------ Job Manager -----------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 수신   | -> | event time 정렬 | -> | 상태 연산 수행 | -> | 체크포인트    | -> | sink 반영     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 수신**: source connector가 스트림 이벤트를 읽음
2. **event time 정렬**: watermark를 사용해 시간 기준 연산 범위를 조정함
3. **상태 연산 수행**: keyed state와 window를 사용해 집계와 조인을 처리함
4. **체크포인트**: 상태와 오프셋을 일관된 시점으로 저장함
5. **sink 반영**: 외부 시스템에 결과를 전송하고 복구 기준을 유지함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 상태 크기가 빠르게 증가하면 checkpoint 시간이 길어져 처리 지연과 복구 시간이 동시에 악화될 수 있음
   - 해결방안: state lifecycle policy와 incremental checkpoint tuning을 적용하고 checkpoint duration과 state backend growth rate로 검증함
2. 문제: 병목 연산자와 backpressure가 지속되면 지연이 누적되어 실시간 처리 약속을 지키기 어려워질 수 있음
   - 해결방안: operator parallelism tuning과 hotspot isolation을 적용하고 backpressure ratio와 processing latency percentile로 검증함
3. 문제: savepoint와 버전 업그레이드 절차가 표준화되지 않으면 운영 중 배포 변경이 서비스 중단 위험으로 이어질 수 있음
   - 해결방안: upgrade runbook과 savepoint validation pipeline을 적용하고 upgrade success rate와 rollback time으로 검증함

## Ⅶ. 적용 사례

- 실시간 스트림 분석 플랫폼이 증분 체크포인트를 운영하며 확인 지표는 checkpoint duration과 state backend growth rate임
- CEP 기반 탐지 서비스가 병목 연산자 분리를 적용하며 확인 지표는 backpressure ratio와 processing latency percentile임
- 운영 플랫폼이 savepoint 검증 절차를 표준화하며 확인 지표는 upgrade success rate와 rollback time임

## Ⅷ. 결론

Apache Flink는 낮은 지연과 강한 상태 처리가 장점이지만 state 운영과 업그레이드 절차를 제어할 수 있어야 실전에서 안정성이 남음.
