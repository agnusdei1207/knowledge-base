---
title: "Apache Spark (Apache Spark)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 134
---

# 📖 【암기용】 개념 완전 이해

> 목적: Spark가 Hadoop MapReduce의 어떤 한계를 메모리 기반으로 보완하는지, 내부 실행 모델 용어를 이해하게 만든다.

## 한눈에
- **개요**: Apache Spark는 **메모리 기반 분산 데이터 처리 엔진**으로, **DAG**(방향성 비순환 그래프) 실행 모델을 통해 배치·SQL·스트림·ML을 하나의 엔진에서 처리하는 범용 빅데이터 처리 프레임워크다.
- **왜 필요한가**: MapReduce는 map→reduce 각 단계마다 중간 결과를 디스크에 쓰고 읽는다. 같은 데이터를 여러 번 스캔하는 반복 연산(머신러닝 iteration, 대화형 분석)에서는 이 디스크 I/O가 반복될 때마다 지연이 누적된다.
- **핵심 직관**: 매 계산마다 창고(디스크)에 갔다 오는 대신, 자주 쓰는 재료(데이터)를 작업대(메모리) 위에 올려두고 연속 계산하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 분산 처리 | 하나의 작업을 여러 서버에 나눠 동시에 수행하는 방식 — Spark가 속한 상위 범주 | 여러 일꾼이 나눠서 일하기 |
| 인메모리 컴퓨팅 | 중간 결과를 디스크가 아니라 메모리에 유지해 반복 접근 속도를 높이는 방식 | 작업대 위에 재료를 올려두고 씀 |
| RDD | Resilient Distributed Dataset — 분산·불변 데이터 집합. lineage(생성 계보)로 노드 장애 시 재계산 복구 | 조리 과정 레시피를 기억해 재료를 잃어도 다시 만듦 |
| DataFrame | 스키마(컬럼명·타입)를 가진 구조화 데이터 API, Catalyst 최적화의 대상 | 엑셀 표처럼 열 이름이 있는 데이터 |
| DAG | Directed Acyclic Graph — 연산 순서를 노드(연산)와 엣지(데이터 흐름)로 표현한 방향성 비순환 그래프 | 여행 동선을 미리 그려둔 지도 |
| Driver | 애플리케이션 전체 실행 계획을 세우고 DAG를 만드는 마스터 프로세스 | 현장 전체를 지휘하는 감독 |
| Executor | Driver의 지시를 받아 실제 task를 실행하고 데이터를 캐시하는 워커 프로세스 | 현장에서 일하는 작업자 |
| Transformation | 새 RDD/DataFrame을 "정의만" 하는 지연 연산(map, filter, select 등) — 즉시 실행되지 않음 | 요리 레시피를 적어두기만 함 |
| Action | 실제 계산을 트리거하는 연산(collect, count, save 등) | "지금 요리 시작" 지시 |
| Lazy Evaluation | Action이 호출되기 전까지 Transformation을 실행하지 않고 계획만 누적하는 방식 | 주문을 다 받은 뒤 한꺼번에 조리 순서를 짜기 |
| Stage | shuffle 경계를 기준으로 나뉜 task들의 묶음 | 공정 단계별 작업 구간 |
| Shuffle | partition 간 데이터를 key 기준으로 재분배하는 과정(네트워크+디스크 비용 발생) | 여러 창고에 흩어진 물건을 품목별로 재정리 |
| Catalyst Optimizer | SQL/DataFrame 쿼리를 논리 계획→물리 계획으로 최적화하는 엔진 | 최단 동선을 미리 계산해주는 내비게이션 |
| Data Skew | 특정 key에 데이터가 몰려 일부 task만 유독 오래 걸리는 현상 | 한 계산대에만 줄이 길게 늘어섬 |

## 깊이 이해

### 왜 Spark가 필요했나 — MapReduce와의 수치 비교
로지스틱 회귀처럼 같은 데이터를 10회 반복 스캔하는 알고리즘을 생각해보자. MapReduce는 iteration마다 별도의 job으로 나뉘어, 매번 결과를 HDFS(디스크)에 쓰고 다음 job이 다시 디스크에서 읽는다 — 10회 반복이면 디스크 read/write가 10번 반복된다. Spark는 최초 1회만 원본 데이터를 읽어 메모리에 캐시(`.cache()`)해두고, 나머지 9회는 메모리에서 바로 재사용한다. 디스크 I/O가 메모리 접근보다 수십~수백 배 느리기 때문에, 반복 연산에서 Spark가 MapReduce보다 훨씬 빠른 이유가 여기에 있다.

### Lazy Evaluation과 DAG 최적화
`df.filter(...).select(...).groupBy(...).count()`처럼 연산을 연쇄로 작성해도, `count()`(Action)가 호출되기 전까지는 아무 계산도 일어나지 않는다. Driver는 이 연쇄를 DAG로 만든 뒤, Catalyst Optimizer가 예를 들어 "filter를 최대한 앞으로 당겨(predicate pushdown) 불필요한 row를 일찍 제거"하는 식으로 실행 순서를 재배치한다. 즉 개발자가 작성한 순서 그대로 실행하는 게 아니라, 최적화된 순서로 다시 짜서 실행한다.

### Stage와 Shuffle — 왜 비용이 큰가
DAG는 shuffle이 필요한 지점(groupBy, join, repartition 등)마다 Stage로 쪼개진다. `reduceByKey`는 map 단계에서 미리 부분 합산 후 셔플하지만, `groupByKey`는 원본 값을 그대로 셔플한다. 예를 들어 키당 값이 평균 1,000개라면 `groupByKey`는 네트워크로 1,000개 값을 모두 보내지만, `reduceByKey`는 미리 합산된 값 1개만 보낸다 — Hadoop의 combiner와 같은 원리다.

### Data Skew — 수치로 보는 병목
1TB 데이터를 200개 partition으로 나누면 partition당 평균 5GB다. 그런데 특정 key 하나가 전체의 40%(400GB)를 차지한다면, 그 key를 처리하는 task 1개가 나머지 199개 task보다 압도적으로 오래 걸리고, 전체 job은 가장 느린 이 task가 끝날 때까지 기다린다. 이를 완화하는 기법이 salting(key에 임의 접미사를 붙여 여러 partition으로 분산)이다.

### 흔한 오해
Spark가 "메모리만 쓰는 도구"라는 것은 오해다. 캐시할 데이터가 executor 메모리보다 크면 디스크로 spill되고, shuffle 자체도 항상 디스크에 중간 파일을 남긴다. Spark의 강점은 "메모리를 최대한 활용해 불필요한 디스크 I/O를 줄이는 것"이지, 디스크를 아예 쓰지 않는다는 뜻이 아니다.

## 연결 개념
- Hadoop MapReduce — Spark가 개선한 disk 기반 실행 모델(133)
- RDD·DataFrame — Spark의 두 가지 데이터 추상화 계층
- Lambda/Kappa Architecture — Spark가 batch/speed 엔진으로 편입되는 상위 아키텍처(135, 136)

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
