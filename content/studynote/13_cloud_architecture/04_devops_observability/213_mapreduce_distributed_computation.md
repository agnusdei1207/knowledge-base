+++
title = "213. 맵리듀스 (MapReduce)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MapReduce는 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Map(필터링·변환)과 Reduce(집계·합산) 두 단계로 분할하여 수천 노드에 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 연산 프레임워크로, 구글 논문(2004)을 기반으로 Hadoop이 구현했다.
> 2. **가치**: 복잡한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리의 세부 사항(장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분배, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화)을 프레임워크가 처리하므로, 개발자는 Map 함수와 Reduce 함수만 작성하면 수천 노드에서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행되는 프로그램을 만들 수 있다.
> 3. **판단 포인트**: MapReduce의 핵심 병목은 매 Map-Shuffle-Reduce 단계마다 디스크([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/))에 중간 결과를 써야 한다는 점이다. 이 디스크 I/O가 [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)(메모리 기반)로 대체되는 주된 이유다.

---

## Ⅰ. 개요 및 필요성

구글은 2004년 발표한 논문 "[MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/): Simplified [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Processing on Large Clusters"에서 수천 대 서버에서 페타바이트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하는 방법을 제시했다. 핵심 아이디어는 단순하다: <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 잘게 쪼개어 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>로 처리하고, 결과를 한 곳에 모아 합산한다.</strong>

MapReduce의 이름은 두 핵심 연산에서 왔다. <strong>Map</strong>은 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하여 키-값(Key-Value) 쌍으로 변환하는 과정이고, <strong>Reduce</strong>는 같은 키를 가진 모든 값을 모아서 집계(합산, 카운트 등)하는 과정이다. 이 두 연산의 조합으로 필터링, 정렬, 집계, 조인 같은 대부분의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리가 가능하다.

MapReduce는 함수형 프로그래밍의 map()과 reduce() 개념을 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에 적용한 것이다. Python의 `map()`이 리스트의 각 원소에 함수를 적용하는 것처럼, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) Map은 수천 노드의 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파티션에 함수를 적용한다.

📢 **섹션 요약 비유**: MapReduce는 선거 개표 방식과 같다. 투표함([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 전국 개표소(Map 단계)에서 각자 집계하고, 그 결과를 중앙선거관리위원회(Reduce 단계)로 모아 최종 합산한다. 한 곳에서 다 세는 것보다 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 처리 단계

```
  입력 데이터 (HDFS 블록)
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │                   Map 단계                               │
  │                                                          │
  │  Split 1: [hello world] → (hello,1) (world,1)           │
  │  Split 2: [hello hadoop] → (hello,1) (hadoop,1)          │
  │  Split 3: [world hello] → (world,1) (hello,1)            │
  └────────────────────────────────────────────────────────┘
       │
       ▼ Shuffle & Sort (같은 키끼리 모으기)
  ┌─────────────────────────────────────────────────────────┐
  │                 Shuffle & Sort 단계                      │
  │                                                          │
  │  hadoop: [(hadoop,1)]                                    │
  │  hello:  [(hello,1), (hello,1), (hello,1)]              │
  │  world:  [(world,1), (world,1)]                         │
  └────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │                  Reduce 단계                             │
  │                                                          │
  │  hadoop: sum([1]) = 1                                    │
  │  hello:  sum([1,1,1]) = 3                               │
  │  world:  sum([1,1]) = 2                                 │
  └────────────────────────────────────────────────────────┘
       │
       ▼
  출력: hadoop=1, hello=3, world=2 (HDFS에 저장)
```

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 처리 흐름

| 단계 | 역할 | 저장 위치 |
|:---:|:---|:---:|
| Input Split | 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 Map [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 단위로 분할 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) |
| Map | 키-값 쌍으로 변환·필터링 | 로컬 디스크 |
| Combiner | 로컬 사전 집계 (Reduce 전 최적화) | 로컬 디스크 |
| [Shuffle & Sort](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/205_shuffle_sort_yarn_resource_manager/) | 같은 키를 같은 Reducer로 전송 | 네트워크 + 디스크 |
| Reduce | 집계·합산 처리 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) |
| Output | 최종 결과 저장 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) |

### Java [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 코드 예시 (단어 빈도 계산)

```java
// Mapper 클래스
public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private Text word = new Text();
    private IntWritable one = new IntWritable(1);

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        // 각 줄을 공백으로 분리하여 단어 추출
        StringTokenizer tokenizer = new StringTokenizer(value.toString());
        while (tokenizer.hasMoreTokens()) {
            word.set(tokenizer.nextToken());
            context.write(word, one);  // (단어, 1) 출력
        }
    }
}

// Reducer 클래스
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();  // 같은 단어의 1들을 모두 합산
        }
        context.write(key, new IntWritable(sum));  // (단어, 빈도) 출력
    }
}
```

📢 **섹션 요약 비유**: Map 함수는 택배 분류기처럼 들어오는 소포([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 주소 태그(키-값)를 붙이는 것, Shuffle은 같은 배달 지역(키)의 소포를 모으는 것, Reduce는 같은 지역 소포를 한 명의 배달원이 모두 처리하는 것이다.

---

## Ⅲ. 비교 및 연결

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) vs [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)

| 항목 | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 매 단계 디스크([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)) 기록 | 메모리(RAM) 우선 |
| 속도 | 느림 (디스크 I/O 병목) | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 빠름 |
| 반복 처리 | 매 반복마다 디스크 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/읽기 | 메모리에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유지 |
| ML 지원 | 제한적 (MLlib 없음) | SparkML 내장 |
| 언어 | Java (verbose) | Python/Scala/Java/R |
| 현재 트렌드 | 점차 대체 중 | 산업 표준 |

### [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 적합/비적합 케이스

| 케이스 | 적합 여부 | 이유 |
|:---|:---:|:---|
| 수십 TB [로그 분석](/knowledge-base/studynote/16_bigdata/05_analysis/119_log_analysis/) (1회) | ✅ | 대규모 배치, 결과 재사용 없음 |
| 반복적 ML 모델 학습 | ❌ | 매 반복 디스크 I/O → 극도로 느림 |
| 실시간 [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | ❌ | 배치 모델, 실시간 불가 |
| 단순 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | ⚠️ | [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/)/SparkSQL이 더 편리 |

📢 **섹션 요약 비유**: MapReduce의 디스크 I/O 문제는 매 수학 문제를 풀 때마다 중간 계산을 지우고 노트에 받아적은 후 다시 읽어야 하는 것과 같다. Spark는 중간 계산을 머릿속(메모리)에 유지하여 훨씬 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/">MapReduce</a> 실행 최적화</strong>:
```
1. Combiner 활용:
   Reducer에 보내기 전 로컬에서 사전 집계
   예: Map 결과 (hello,1)(hello,1)(hello,1) → Combiner → (hello,3)
   → 네트워크 트래픽 대폭 감소

2. 적절한 Reducer 수 설정:
   - 너무 적으면: 일부 Reducer에 부하 집중 (Skew)
   - 너무 많으면: 작은 파일 다수 생성, NameNode 부하

3. 입력 포맷 최적화:
   - ORC, Parquet 같은 컬럼형 저장 포맷 사용
   - 압축 코덱 적용 (Snappy, LZO)
```

<strong>AWS EMR에서 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/">MapReduce</a> 실행</strong>:
```bash
aws emr add-steps \
  --cluster-id j-XXXXX \
  --steps Type=CUSTOM_JAR,\
          Name="WordCount",\
          ActionOnFailure=CONTINUE,\
          Jar=s3://mybucket/wordcount.jar,\
          Args=[s3://mybucket/input/,s3://mybucket/output/]
```

**기술사 판단 포인트**:
- MapReduce는 학습 목적과 레거시 시스템 이해를 위해 알아야 하지만, 신규 개발에는 Spark를 사용하는 것이 표준이다.
- Shuffle 단계가 MapReduce의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐(Skew)가 있으면 일부 Reducer가 과부하되어 전체 Job이 지연된다.
- 구글은 MapReduce를 2014년 자체 시스템에서 Dremel(BigQuery의 전신)과 Millwheel로 대체했다.

📢 **섹션 요약 비유**: MapReduce의 Shuffle 단계는 전국 각 지역 개표소의 결과를 중앙으로 모으는 과정이다. 특정 지역(Reducer)에 너무 많은 투표지([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스큐)가 몰리면 그 지역 개표가 끝날 때까지 전국 개표 완료를 기다려야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 자동 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 | 개발자가 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 코드를 작성하지 않아도 됨 |
| 자동 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 실패 시 프레임워크가 자동 재실행 |
| 대규모 처리 | 수천 노드에서 페타바이트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 |
| 단순한 프로그래밍 모델 | Map + Reduce 두 함수만 작성 |

MapReduce는 빅데이터 처리의 첫 번째 민주화였다. 구글만 할 수 있었던 수천 노드 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리를 누구나 가능하게 했다. 현재는 Spark에 자리를 내줬지만, Spark도 MapReduce의 개념을 계승·개선한 것이다. MapReduce를 이해해야 Spark의 가치를 제대로 평가할 수 있다.

📢 **섹션 요약 비유**: MapReduce는 자동차의 첫 번째 모델 T([포드](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))와 같다. 현재 기준으로는 느리고 불편하지만, 이것이 없었다면 현대 자동차(Spark)도 없었다. 역사를 알아야 현재를 이해한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) | MapReduce의 입력/출력 저장소 |
| [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/) | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 작업의 CPU/메모리 자원을 배분하는 관리자 |
| [Apache Spark](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | MapReduce의 디스크 I/O 한계를 극복한 후계자 |
| [Shuffle & Sort](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/205_shuffle_sort_yarn_resource_manager/) | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목의 핵심 단계 |
| Combiner | 로컬 사전 집계로 Shuffle 트래픽 감소 최적화 |
| 구글 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 논문 | [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/), [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 모두의 이론적 기원 |

### 👶 어린이를 위한 3줄 비유 설명

1. Map 단계는 반 전체 학생이 동시에 각자 도서관에서 "역사" 관련 책을 찾아 목록(키-값)을 만드는 거야.

### 📈 관련 키워드 및 발전 흐름도

```text
MapReduce 처리 흐름
    ├─► Map: 데이터 분할 → 키-값 쌍 추출
    ├─► Shuffle & Sort: 같은 키끼리 모으기
    └─► Reduce: 집계 · 요약
    │
    ▼
한계: 디스크 I/O 병목 → Spark (In-Memory) 대체
```
2. Shuffle은 같은 시대의 책 목록을 한 사람에게 모아주는 것, Reduce는 그 사람이 최종적으로 합산하는 거야.
3. 혼자서 모든 책을 찾는 것보다 여러 명이 나눠서 동시에 찾으니([병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) 훨씬 빠른 거야!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 212 / 371

← **이전**: [212. HDFS (Hadoop Distributed File System)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/212_hdfs_distributed_file_system/)
**다음**: [214. YARN (Yet Another Resource Negotiator)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/214_yarn_resource_manager_hadoop/) →

---
