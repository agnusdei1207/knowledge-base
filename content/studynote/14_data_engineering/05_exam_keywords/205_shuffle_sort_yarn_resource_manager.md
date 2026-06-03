---
title: 205. 셔플·정렬 (Shuffle & Sort)과 YARN (Yet Another Resource Negotiator)
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MapReduce의 셔플(Shuffle)은 Map 출력을 키([[067_db_key_uniqueness_minimality|Key]])별로 Reduce에 전달하기 위해 네트워크 전체를 가로질러 [[001_dikw_pyramid|데이터]]를 재배치하는 단계로, 전체 Job 시간의 40~70%를 차지하는 핵심 병목이다.
> 2. **가치**: [[020_yarn|YARN]] (Yet Another Resource Negotiator)은 클러스터 자원 관리와 애플리케이션 실행 로직을 분리함으로써, [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터를 [[018_mapreduce|MapReduce]] 전용에서 Spark·Tez·MPI 등을 아우르는 범용 [[136_variance|분산]] 컴퓨팅 플랫폼으로 전환시켰다.
> 3. **판단 포인트**: 기술사 논술에서 셔플 최적화(Combiner, [[347_compaction|압축]], [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]])와 YARN의 역할 분리 아키텍처(ResourceManager·NodeManager·ApplicationMaster)를 구분하여 설명할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

### [[018_mapreduce|MapReduce]] 처리 단계 개요

MapReduce는 입력 [[001_dikw_pyramid|데이터]]를 Map → Shuffle & Sort → Reduce 세 단계로 처리한다.

```
MapReduce 전체 흐름
┌──────────────────────────────────────────────────────────────┐
│  입력 데이터 (HDFS)                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  Split 1  │  │  Split 2  │  │  Split 3  │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       │              │              │                         │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐                   │
│  │  Map 1    │  │  Map 2    │  │  Map 3    │  ← Map 단계      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       │              │              │                         │
│  ┌────▼──────────────▼──────────────▼─────┐                  │
│  │         셔플 & 정렬 (Shuffle & Sort)      │  ← 핵심 병목   │
│  │   키별 파티셔닝 + 정렬 + 네트워크 전송     │                 │
│  └────┬──────────────┬───────────────────┘                   │
│       │              │                                        │
│  ┌────▼─────┐  ┌────▼─────┐                                  │
│  │ Reduce 1  │  │ Reduce 2  │  ← Reduce 단계                  │
│  └────┬─────┘  └────┬─────┘                                  │
│       │              │                                        │
│  ┌────▼──────────────▼─────┐                                  │
│  │     출력 (HDFS 저장)      │                                  │
│  └──────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```

### 왜 셔플이 병목인가?

셔플은 모든 Map [[150_task|태스크]]의 출력이 모든 Reduce [[150_task|태스크]]로 이동해야 하는 **All-to-All 통신 패턴**이다. 노드 N개가 있을 때 최악의 경우 N² 개의 네트워크 연결이 생성된다.

📢 **섹션 요약 비유**: 셔플은 "반 전체 학생(Map)이 각자 쓴 답을 과목별로 정리해서 과목 담당 교사(Reduce)에게 전달하는 것"이다. 영어 답지는 영어 선생님께, 수학은 수학 선생님께. 100명 학생 × 10개 과목 = 1,000번 이동이 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 셔플 & 정렬 단계 상세 메커니즘

```
셔플 & 정렬 상세 흐름
┌─────────────────────────────────────────────────────────────┐
│  Map 태스크 측 (Map-Side):                                   │
│  Map 출력 → 순환 버퍼(80MB) → 파티셔닝(키 해시) → 정렬      │
│           → 스필(Spill to Disk, 버퍼 80% 찰 때)              │
│           → 여러 스필 파일 병합(Merge Sort) → 로컬 디스크    │
│                                                             │
│  네트워크 전송 (Network Transfer):                           │
│  HTTP로 Reduce 태스크에게 Map 출력 전송                       │
│                                                             │
│  Reduce 태스크 측 (Reduce-Side):                             │
│  여러 Map의 출력 수신 → 병합 정렬(Merge Sort)                │
│  → 키별 그룹화 → Reduce 함수 호출                           │
└─────────────────────────────────────────────────────────────┘
```

| 셔플 세부 단계 | 설명 | 최적화 방법 |
|:---|:---|:---|
| [[179_table_partitioning_concept|파티셔닝]] | 키 해시로 Reduce 분배 결정 | 균등 분포 보장 커스텀 파티셔너 |
| 정렬 (Map-Side) | Map 출력을 키 기준 정렬 | 인메모리 정렬 버퍼 크기 증가 |
| 스필 (Spill) | 버퍼 가득 차면 디스크에 임시 [[501_file_definition_logical_record|파일]] | 버퍼 크기 늘려 스필 횟수 감소 |
| 병합 (Merge) | 스필 [[501_file_definition_logical_record|파일]]들을 병합 정렬 | Combiner로 [[001_dikw_pyramid|데이터]] 크기 사전 축소 |
| 네트워크 전송 | Map → Reduce [[001_dikw_pyramid|데이터]] 전송 | [[347_compaction|압축]](Snappy/LZ4)으로 전송량 감소 |
| Reduce-Side 정렬 | 수신된 [[001_dikw_pyramid|데이터]] 최종 병합 정렬 | 충분한 Reduce 힙 메모리 확보 |

### Combiner: 셔플 최적화의 핵심

Combiner는 Map 출력을 Reduce로 보내기 전에 같은 노드에서 사전 집계하는 미니 Reduce다.

```
Combiner 효과
┌─────────────────────────────────────────────────────────────┐
│  Combiner 없음:                                             │
│  Map1: (apple,1),(apple,1),(banana,1),(apple,1)             │
│  → 셔플: apple 3개 + banana 1개 전송 (4건)                   │
│                                                             │
│  Combiner 있음:                                             │
│  Map1: (apple,1),(apple,1),(banana,1),(apple,1)             │
│  → Combine: (apple,3),(banana,1)                           │
│  → 셔플: (apple,3),(banana,1) 전송 (2건, 50% 감소!)          │
└─────────────────────────────────────────────────────────────┘
```

> ⚠️ **주의**: Combiner는 결합법칙과 교환법칙이 성립하는 연산(합계, 최댓값)에만 적용 가능. 평균값 계산에 직접 적용하면 잘못된 결과가 나온다.

### [[020_yarn|YARN]] 아키텍처

```
YARN 전체 아키텍처
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              ResourceManager (클러스터 1대)              │   │
│  │  ┌─────────────────────┐  ┌─────────────────────────┐  │   │
│  │  │  Scheduler           │  │  ApplicationManager      │  │   │
│  │  │  (자원 할당 결정)     │  │  (애플리케이션 생명주기) │  │   │
│  │  └─────────────────────┘  └─────────────────────────┘  │   │
│  └────────────────────────────────────────────────────────┘   │
│              │ 자원 할당        │ AM 시작                       │
│              ▼                  ▼                              │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │   NodeManager 1   │  │   NodeManager 2   │ (각 워커 노드)    │
│  │  ┌────────────┐   │  │  ┌────────────┐   │                  │
│  │  │ Container   │   │  │  │ Container   │   │                  │
│  │  │ (AM 또는    │   │  │  │ (Task 실행) │   │                  │
│  │  │  Task 실행) │   │  │  └────────────┘   │                  │
│  │  └────────────┘   │  └──────────────────┘                   │
│  └──────────────────┘                                          │
│              │ 태스크 시작 요청                                   │
│              ▼                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ApplicationMaster (앱별 1개)                             │  │
│  │  → 구체적인 태스크 계획 수립, Container 요청, 진행 모니터링│  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

| [[020_yarn|YARN]] [[603_component_independent_deployment_unit|컴포넌트]] | 역할 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 1.x 대비 |
|:---|:---|:---|
| ResourceManager ([[197_rm_rate_monotonic_scheduling|RM]]) | 클러스터 전체 [[041_resource_allocation|자원 할당]]·스케줄링 | JobTracker의 자원 관리 부분만 담당 |
| NodeManager (NM) | 노드별 [[194_container_virtualization_docker_namespace|Container]] 실행·모니터링 | TaskTracker 대체 |
| ApplicationMaster (AM) | 앱별 [[150_task|태스크]] 계획·조율 | JobTracker의 작업 스케줄링 부분을 분리 |
| [[194_container_virtualization_docker_namespace|Container]] | 격리된 자원 단위 (CPU, 메모리) | Slot 개념 대체 (더 세밀한 자원 제어) |

📢 **섹션 요약 비유**: YARN은 "군대 사령부(ResourceManager)가 병사([[194_container_virtualization_docker_namespace|Container]])를 배치하고, 각 작전 지휘관(ApplicationMaster)이 현장 작전을 수행하는 구조"다. [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 1.x의 JobTracker는 사령부와 지휘관을 혼자 다 하던 과부하 직책이었다.

---

## Ⅲ. 비교 및 연결

### [[020_yarn|YARN]] [[079_kube_scheduler_pod_placement|스케줄러]] 종류

| [[079_kube_scheduler_pod_placement|스케줄러]] | [[164_policy|정책]] | 적합 환경 |
|:---|:---|:---|
| [[261_fifo_page_replacement|FIFO]] (First In, First Out) | 제출 순서대로 처리 | 단순 [[228_batch_processing_hadoop_spark|배치 처리]] 환경 |
| Capacity Scheduler | 팀/부서별 [[041_resource_allocation|자원 할당]]량 보장 | 다중 테넌트 기업 환경 ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 기본값) |
| Fair Scheduler | 실행 중인 Job 간 자원 공평 분배 | 소규모 Job이 많은 환경 |

### YARN에서 지원하는 프레임워크

```
YARN 멀티 프레임워크 지원
┌─────────────────────────────────────────────────────────────┐
│                    YARN 클러스터                             │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │MapReduce  │  │  Spark   │  │   Tez    │  │   MPI    │   │
│  │(배치 ETL) │  │(ML, SQL) │  │(Hive 최적)│  │(고성능   │   │
│  │          │  │          │  │          │  │  계산)    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  공통: 모두 YARN ApplicationMaster로 구현됨                  │
└─────────────────────────────────────────────────────────────┘
```

### 셔플 최적화 종합 비교

| 최적화 기법 | 적용 위치 | 효과 | 주의사항 |
|:---|:---|:---|:---|
| Combiner | Map-Side | 셔플 [[001_dikw_pyramid|데이터]] 50~80% 감소 | 결합법칙·교환법칙 연산만 적용 가능 |
| [[347_compaction|압축]] (Snappy) | 네트워크 전송 | 전송량 50~70% 감소 | CPU 오버헤드 발생 |
| 버퍼 크기 증가 | Map 버퍼 | 디스크 스필 횟수 감소 | 메모리 부족 주의 |
| 파티셔너 커스텀 | [[179_table_partitioning_concept|파티셔닝]] | Reduce 스큐 방지 | 불균등 [[179_table_partitioning_concept|파티셔닝]] 주의 |
| Reduce 병렬도 | Reduce 수 조정 | 처리 병렬성 향상 | 너무 많으면 오버헤드 |

📢 **섹션 요약 비유**: 셔플 최적화는 "택배 [[104_classification_analysis|분류]] 센터 효율화"다. Combiner는 출발지에서 미리 같은 목적지 택배를 묶어서 보내는 것([[393_data_dictionary|데이터 사전]] 집계), [[347_compaction|압축]]은 택배를 진공 [[347_compaction|압축]]해서 부피를 줄이는 것, 파티셔너는 목적지별 균등 배분으로 특정 센터에 몰리지 않게 하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 셔플 [[282_performance_tactics|성능]] 진단 방법

```
셔플 병목 진단 체크리스트
┌──────────────────────────────────────────────────────────┐
│  1. 셔플 시간 비중 확인:                                  │
│     Job 총 시간 중 Shuffle: XX% → 40% 이상이면 병목       │
│                                                          │
│  2. 데이터 스큐 확인:                                     │
│     Reduce 태스크 완료 시간 편차 → 편차 크면 파티셔닝 문제 │
│                                                          │
│  3. 스필 횟수 확인:                                       │
│     mapreduce.map.sort.spill.percent 모니터링             │
│     → 스필 빈번하면 Map 버퍼 크기(io.sort.mb) 증가 필요   │
│                                                          │
│  4. 네트워크 사용률 확인:                                  │
│     셔플 중 네트워크 포화 → 압축 설정 확인                 │
└──────────────────────────────────────────────────────────┘
```

### [[020_yarn|YARN]] 자원 계획 실무

| 항목 | 계획 방법 | 권장 [[009_config|설정]] |
|:---|:---|:---|
| [[194_container_virtualization_docker_namespace|Container]] 메모리 | 물리 메모리의 80% [[020_yarn|YARN]] 할당 (20%는 OS용) | 128GB 서버 → [[020_yarn|YARN]] 102GB |
| vCPU 할당 | [[199_interrupt_scheduling|하이퍼스레딩]] 고려 실제 코어 × 1.5~2 | 16코어 → [[020_yarn|YARN]] 24 vCPU |
| AM 메모리 | 2~4GB (Spark AM은 더 필요할 수 있음) | 서비스별 조정 |
| 최대 [[194_container_virtualization_docker_namespace|Container]] 크기 | 단일 Executor/Mapper 최대 크기 | 물리 메모리의 50% 이내 |

### 기술사 논술 핵심 포인트

1. **셔플 병목의 본질**: 셔플은 [[136_variance|분산]] 처리의 본질적 비용이다. 완전히 제거할 수 없으나, Combiner·[[179_table_partitioning_concept|파티셔닝]]·[[347_compaction|압축]]으로 최소화할 수 있음을 구체적 수치로 제시.
2. **YARN의 역할 분리 철학**: ResourceManager가 "무엇을 실행할지"가 아닌 "어디에서 실행할지"만 결정함으로써 프레임워크 중립성을 확보. 이것이 멀티 프레임워크 지원의 핵심.
3. **Spark vs [[018_mapreduce|MapReduce]] 셔플**: Spark도 셔플이 존재하지만 (GroupBy, [[521_join|Join]] 등), 중간 결과를 메모리에 유지해 디스크 I/O를 최소화한다는 차이를 명확히 서술.

📢 **섹션 요약 비유**: YARN의 역할 분리는 "공항 관제탑(ResourceManager)은 활주로 배정만 하고, 각 항공사 운항 계획(ApplicationMaster)은 항공사가 직접 짜는 것"이다. 관제탑이 항공사마다 다른 운항 규칙을 알 필요 없이, 활주로만 효율적으로 배분하면 된다.

---

## Ⅴ. 기대효과 및 결론

### [[020_yarn|YARN]] 도입 효과

| 효과 영역 | 내용 |
|:---|:---|
| 자원 활용률 향상 | Slot 기반(고정) → [[194_container_virtualization_docker_namespace|Container]] 기반(가변), 자원 낭비 40% 감소 |
| 프레임워크 유연성 | [[018_mapreduce|MapReduce]] 전용 → Spark·Tez·MPI·[[543_hbase|HBase]] 통합 운영 |
| 운영 단순화 | 단일 클러스터에서 다중 워크로드 통합 관리 |
| 확장성 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 1.x 4,000 노드 한계 → 수만 노드 지원 |

### 셔플 최적화 효과

| 최적화 적용 | 셔플 시간 | 전체 Job 시간 |
|:---|:---|:---|
| 기본 [[009_config|설정]] | 60분 | 90분 |
| Combiner 적용 | 25분 | 45분 |
| Combiner + [[347_compaction|압축]] | 15분 | 32분 |
| Combiner + [[347_compaction|압축]] + 파티셔너 최적화 | 12분 | 25분 |

### 결론

셔플 & 정렬은 MapReduce의 핵심이자 병목이다. 이를 이해하고 최적화하는 능력은 빅데이터 엔지니어의 기본 역량이다. YARN은 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 클러스터를 범용 [[136_variance|분산]] 컴퓨팅 플랫폼으로 격상시켜, 현재 클라우드 기반 [[001_dikw_pyramid|데이터]] 플랫폼의 자원 관리 개념(Kubernetes의 [[198_pod_kubernetes_minimum_deployment_unit|Pod]]/[[194_container_virtualization_docker_namespace|Container]] 개념과도 연결)의 선구자가 되었다.

📢 **섹션 요약 비유**: 셔플 최적화와 YARN은 "도로 교통망 개선"이다. Combiner는 출발지에서 카풀로 차 수를 줄이고, [[347_compaction|압축]]은 트럭에 더 많이 싣고, YARN은 교차로 신호체계를 스마트하게 바꿔 전체 흐름을 개선한다. 개별 최적화가 모여 시스템 전체 효율을 높인다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 하위 개념 | Map 단계 | 입력 [[001_dikw_pyramid|데이터]] 변환, 키-값 쌍 출력 |
| 핵심 단계 | Shuffle & Sort | 키별 [[001_dikw_pyramid|데이터]] 재배치, 정렬 |
| 하위 개념 | Reduce 단계 | 키별 집계·처리 |
| 최적화 기술 | Combiner | Map-Side 사전 집계로 셔플 [[001_dikw_pyramid|데이터]] 감소 |
| 관련 기술 | [[020_yarn|YARN]] (Yet Another Resource Negotiator) | 범용 클러스터 자원 관리자 |
| [[020_yarn|YARN]] 구성 | ResourceManager | 클러스터 전체 [[041_resource_allocation|자원 할당]] |
| [[020_yarn|YARN]] 구성 | ApplicationMaster | 앱별 [[150_task|태스크]] 조율 |
| 발전 방향 | [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] | 인메모리로 셔플 오버헤드 최소화 |

### 👶 어린이를 위한 3줄 비유 설명
1. 셔플은 "반 친구들이 만든 과목별 숙제 카드를 선생님들한테 전달하는 것"이에요. 수학 카드는 수학 선생님께, 영어 카드는 영어 선생님께 전달해야 해요.

### 📈 관련 키워드 및 발전 흐름도

```text
MapReduce 셔플: Map 출력 → 네트워크 전송 → Reduce 입력
    │ 네트워크·디스크 병목
    ▼
YARN: 자원 관리 분리 (ResourceManager + NodeManager)
    ├─► ApplicationMaster: 잡별 독립 관리
    └─► 컨테이너 기반 자원 할당
    │
    ▼
Spark Shuffle: Sort-Based · Tungsten Off-Heap 최적화
    │
    ▼
AQE (Adaptive Query Execution): 런타임 최적화
```
2. Combiner는 "출발 전에 같은 선생님한테 갈 카드를 미리 묶어두는 것"이에요. 100장이 10묶음이 되면 훨씬 빠르게 전달할 수 있어요.
3. YARN은 "여러 반 선생님들이 쓸 교실(자원)을 배정해주는 교무처"예요. 수학·영어·과학 수업이 동시에 이루어질 수 있도록 교실을 공평하게 나눠줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 205 / 258

← **이전**: [[204_namenode_metadata_mapreduce_disk_bottleneck|204. NameNode 메타데이터와 MapReduce 디스크 병목 SPOF 극복]]
**다음**: [[206_spark_inmemory_rdd_lazy_evaluation_lineage|206. 아파치 스파크 (Apache Spark) 인메모리 RDD 지연 평가 계보]] →

---
