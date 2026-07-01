---
title: "Apache Spark (Apache Spark)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 134
---

# 📖 【암기용】 개념 완전 이해

> 목적: Spark가 Hadoop MapReduce의 어떤 한계를 보완하는지 이해하게 만든다.

## 한눈에
- **개요**: 메모리 기반 분산 데이터 처리 엔진
- **왜 필요한가**: MapReduce는 단계마다 디스크에 중간 결과를 쓰므로 반복 연산·대화형 분석·ML 작업에서 지연이 커짐.
- **핵심 직관**: 매 계산마다 창고에 갔다 오는 대신, 자주 쓰는 재료를 작업대 위에 올려두고 연속 계산하는 방식임.

## 깊이 이해
- **배경·문제의식**: ETL, SQL 분석, 머신러닝은 같은 데이터를 여러 번 스캔함. Spark는 RDD lineage와 DataFrame Catalyst optimizer, Tungsten 실행 엔진으로 메모리 중심 계산을 수행함.
- **작동 원리**: Driver가 DAG를 생성하고 Cluster Manager가 Executor를 할당함. Transformation은 lazy evaluation으로 누적되고, Action이 호출되면 stage와 task로 나뉘어 실행됨.
- **비유**: 여행 계획을 모두 모아 최적 동선을 만든 뒤, 각 지역 담당자에게 일감을 나눠 실행하는 방식임.
- **구체 예시**: 1TB Parquet를 필터링 후 groupBy할 때 predicate pushdown과 column pruning으로 읽는 column과 row group을 줄임.
- **흔한 오해·주의점**: Spark는 메모리만 쓰는 도구가 아님. shuffle·spill이 발생하면 disk I/O가 생기며, skew key 하나가 stage 지연을 만들 수 있음.

## 연결 개념
- Hadoop MapReduce — Spark의 비교 대상
- RDD·DataFrame — Spark 데이터 추상화
- Lambda/Kappa Architecture — batch·stream 처리 구성

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: Spark 문제에서 DAG 실행, memory 처리, SQL/stream/ML 통합, 운영 리스크를 연결함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Spark는 DAG 기반으로 배치·SQL·스트림·ML을 처리하는 분산 데이터 처리 엔진임.
> 2. **가치**: in-memory cache와 최적화 엔진으로 반복 분석과 ETL 처리 시간을 MapReduce 대비 줄임.
> 3. **판단 포인트**: shuffle, skew, executor memory, checkpoint 정책이 대규모 job의 품질을 좌우함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Spark 구조 이해 확인 | Driver, Executor, DAG Scheduler, Catalyst | Spark를 단순 Hadoop 대체재로만 설명 |
| 처리 원리 확인 | lazy evaluation, stage, task, shuffle | cache와 checkpoint 차이 누락 |
| 도입 판단 확인 | batch, streaming, ML, SQL 통합 | 모든 job이 memory에서만 실행된다고 단정 |

> 요약: Spark 답안은 DAG 최적화와 shuffle 리스크를 함께 제시해야 실무 판단형 답안이 됨.

---

## Ⅰ. 개요 및 필요성

- 개요: Apache Spark는 범용 분산 데이터 처리 엔진임.
- 배경: Hadoop MapReduce는 중간 결과를 디스크에 기록해 반복 분석·머신러닝 작업에서 지연이 커짐.
- 필요성: DAG 실행, in-memory cache, Spark SQL 최적화로 배치·스트림·ML 파이프라인을 통합함.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> Driver -> DAG Scheduler -> Task Scheduler
                          / Cluster Manager -> Executor -> Cache/Shuffle
                          / Data Source -> DataFrame/RDD
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Driver | job 계획·DAG 생성 | driver OOM 방지 필요 |
| Executor | task 실행·cache 저장 | core·memory sizing 필요 |
| Catalyst | SQL logical/physical plan 최적화 | predicate pushdown 적용 |
| Shuffle Manager | partition 재분배 | skew와 spill 감시 필요 |

> 요약: Spark는 Driver가 DAG를 만들고 Executor가 task를 병렬 실행하며, Catalyst와 shuffle 관리가 처리 품질을 결정함.

---

## Ⅲ. 동작원리 및 흐름도

```text
DataFrame 생성 -> Transformation 누적 -> Action 호출
-> DAG 생성 -> Stage 분리 -> Task 실행 -> 결과 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | DataFrame/RDD 생성 | schema inference, partition 수 |
| 2 | lazy transformation 누적 | logical plan 확인 |
| 3 | action 호출 후 stage 분리 | shuffle boundary 수 |
| 4 | executor task 실행 및 결과 저장 | task skew, spill bytes |

> 요약: Spark는 action 전까지 실행을 미루고, DAG를 stage 단위로 나눈 뒤 executor에서 병렬 처리함.

---

## Ⅳ. 특징

| 구분 | Hadoop MapReduce | Apache Spark | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 실행 모델 | map-reduce 고정 | DAG 기반 다단계 연산 | stage 수와 shuffle boundary |
| 저장 | 중간 결과 disk 기록 | cache/persist 선택 | executor memory 사용률 70% 이하 |
| API | MapReduce 중심 | SQL, DataFrame, MLlib, Streaming | 하나의 engine에 통합 |
| 한계 | 반복 연산 지연 | skew·spill·OOM 리스크 | spill bytes, GC time |

> 요약: Spark는 반복·대화형 분석에 유리하나, shuffle skew와 memory sizing을 관리하지 않으면 job 지연이 발생함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | MapReduce batch | DAG + executor | 다단계 ETL, ML 반복 연산 |
| 비용/성능 | disk I/O 중심 | memory cache + spill 제어 | cache hit, shuffle read/write |
| 운영/위험 | job 단순 | executor sizing 복잡 | OOM, skew, dynamic allocation |

> 요약: Spark는 다단계 분석에 적합하고, 단순 일회성 scan은 SQL engine이나 MapReduce와 비용을 비교함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| executor OOM | partition 과대·collect 사용 | repartition, limit, driver collect 금지 | OOM 0건, GC time 10% 이하 |
| data skew | 특정 key 집중 | salting, skew join hint | max task time/median 3 이하 |
| shuffle spill | memory 부족 | adaptive query execution, partition 조정 | spill bytes, shuffle wait time |

> 요약: Spark 운영 리스크는 OOM, skew, spill이며 Spark UI 지표로 원인을 분리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| job SLA | batch 완료 30분 이하 | Spark History Server |
| 자원 사용 | executor memory 70% 이하 | metrics, Prometheus |
| 데이터 품질 | row count·null rate 기준 충족 | Great Expectations, SQL 검증 |

> 요약: Spark 도입 효과는 job SLA, executor 자원, 데이터 품질 검증으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Parquet/ORC, partition pruning, predicate pushdown으로 scan bytes를 원천 데이터 대비 30% 이하로 제한함
2. Spark UI에서 skew stage를 식별하고 salting·broadcast join·AQE로 max task time 편차 3배 이하 유지함
3. checkpoint는 long lineage와 streaming state에 적용하고, cache는 반복 참조 DataFrame에 한정함

**결론 (2줄):**
- 기술사 판단: 반복 분석·ETL·ML 통합은 Spark, event-by-event 저지연 처리는 Flink·Kafka Streams를 선택함
- 향후 방향: Spark는 lakehouse, Delta/Iceberg, Kubernetes 기반 운영과 결합해 데이터 플랫폼 실행 엔진으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Spark를 설명하시오" | lazy evaluation, DAG, stage/task 흐름 | MapReduce 대비 특징 |
| 요구사항 명시형 | "성능 개선 방안을 제시하시오", "비교하시오" | shuffle·skew·executor 지표 | 처리 유형별 Spark/Flink/Hadoop 선택 |

> 요약: 설명형은 실행 모델, 개선형은 Spark UI 지표와 튜닝 방안을 중심으로 작성함.
