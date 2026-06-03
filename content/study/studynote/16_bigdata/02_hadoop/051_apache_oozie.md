+++
weight = 51
title = "29. Apache Oozie — Hadoop 워크플로 스케줄러"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Oozie는 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[031_에코_반향|에코]]시스템 기반 워크플로(Workflow)와 코디네이터([[250_coordinator_participant_2pc_roles|Coordinator]]) 잡을 관리하는 서버 기반 [[079_kube_scheduler_pod_placement|스케줄러]]다. [[018_mapreduce|MapReduce]]·[[544_hive|Hive]]·Pig·Sqoop 등 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 잡을 [[401_bayesian_network_dag_causality|DAG]](방향성 비순환 [[070_graph_datastructure|그래프]])로 구성하여 복잡한 [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인을 자동화한다.
> 2. **가치**: [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 기반 ETL에서 여러 잡이 의존 [[083_relationship_in_er_model|관계]]를 가질 때, Oozie는 순서·조건·[[430_index_fast_full_scan|병렬]] 실행을 중앙에서 관리한다. 시간 기반([[250_coordinator_participant_2pc_roles|Coordinator]])·[[094_data_availability_da_layer_celestia|데이터 가용성]] 기반 [[507_acid_properties|트리거]]로 배치 [[123_pipe|파이프]]라인을 자동 [[208_schedule_history_transaction_execution_order|스케줄]]링한다.
> 3. **판단 포인트**: Oozie의 약점은 XML 기반 복잡한 [[009_config|설정]]과 현대 클라우드 [[123_pipe|파이프]]라인과의 통합 어려움이다. 현대 [[645_data_pipeline_acceleration|데이터 파이프라인]]에서는 Apache Airflow가 Python 기반 DAG로 더 직관적이고 [[531_cloud_native_architecture|클라우드 네이티브]] 통합이 뛰어난 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│          Oozie 워크플로 구조                               │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  워크플로 DAG:                                            │
│  [START] → [Sqoop 임포트] → [Hive ETL] → [Pig 집계]      │
│                                 │                         │
│                           성공/실패 분기                  │
│                         /              \                  │
│                    [이메일 알림]    [오류 처리 잡]          │
│                         \              /                  │
│                              [END]                        │
│                                                           │
│  코디네이터:                                              │
│  매일 02:00 → 전날 데이터 준비 확인 → 워크플로 자동 실행  │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Oozie는 [[001_dikw_pyramid|데이터]] 공장의 자동화 관리자다. 매일 새벽 원재료([[001_dikw_pyramid|데이터]]) 도착을 [[396_validation|확인]]하고, 순서대로 공정([[215_etl_vs_elt_pipeline|ETL]] 잡)을 실행하며, 문제가 생기면 알림을 보내는 공장 자동화 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Oozie 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| **워크플로** | 잡 실행 순서·분기·[[430_index_fast_full_scan|병렬]] 정의 (XML [[401_bayesian_network_dag_causality|DAG]]) |
| **코디네이터** | 시간/[[001_dikw_pyramid|데이터]] 기반 워크플로 자동 [[507_acid_properties|트리거]] |
| **번들** | 여러 코디네이터 묶음 관리 |
| **액션 노드** | [[018_mapreduce|MapReduce]]/[[544_hive|Hive]]/Pig/Sqoop 잡 실행 단위 |
| **컨트롤 노드** | start·end·fork·[[521_join|join]]·decision |

### Oozie vs [[168_airflow_dag_pipeline_scheduling|Apache Airflow]]

```text
Oozie:
  - XML 기반 설정 (workflow.xml)
  - Hadoop 전용 (YARN/HDFS 의존)
  - 레거시 Hadoop 환경에 적합
  - 데이터 가용성 기반 트리거 강점

Airflow:
  - Python 기반 DAG (코드로 파이프라인)
  - 클라우드·다양한 시스템 통합
  - 모니터링 UI, 동적 DAG, 풍부한 플러그인
  - 현대 데이터 엔지니어링 표준
```

- **📢 섹션 요약 비유**: Oozie vs Airflow는 공장 수동 제어반 vs 스마트 공장 SCADA다. Oozie(수동 제어반)는 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 공장 전용이고, Airflow([[894_scada|SCADA]])는 모든 공장을 시각적으로 [[229_monitor|모니터]]링하고 스마트하게 제어한다.

---

## Ⅲ. 비교 및 연결

| 비교 | Oozie | Airflow | NiFi |
|:---|:---|:---|:---|
| [[009_config|설정]] 방식 | XML | Python [[401_bayesian_network_dag_causality|DAG]] | GUI |
| 생태계 | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 전용 | 범용 | 범용 |
| [[229_monitor|모니터]]링 | 기본 | 강력 | 강력 |
| 현황 | 레거시 | 현재 표준 | 스트리밍 강점 |

- **📢 섹션 요약 비유**: 세 [[123_pipe|파이프]]라인 도구는 공장 자동화 도구 세대다. Oozie(1세대-기계식 타이머), Airflow(2세대-[[896_plc_programmable_logic_controller|PLC]] 프로그래밍), NiFi(3세대-스마트 자동화 [[229_monitor|모니터]]링)로 발전했다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Oozie 워크플로 예시 (XML 개요)

```xml
<!-- workflow.xml 구조 -->
<workflow-app name="daily-etl">
  <start to="sqoop-import"/>
  
  <action name="sqoop-import">
    <sqoop>...</sqoop>
    <ok to="hive-transform"/>
    <error to="fail"/>
  </action>
  
  <action name="hive-transform">
    <hive>...</hive>
    <ok to="end"/>
    <error to="fail"/>
  </action>
  
  <kill name="fail">
    <message>ETL 실패: ${wf:errorMessage(wf:lastErrorNode())}</message>
  </kill>
  <end name="end"/>
</workflow-app>
```

### 마이그레이션: Oozie → Airflow

```text
1. Oozie XML 워크플로를 Airflow Python DAG로 변환
2. YARN 직접 실행 → SparkSubmitOperator, HiveOperator
3. 코디네이터 스케줄 → Airflow cron expression
4. 데이터 가용성 트리거 → Airflow Sensor (HdfsFileSensor)
```

- **📢 섹션 요약 비유**: Oozie → Airflow 마이그레이션은 구형 팩스기에서 이메일로 전환하는 것이다. 기능(문서 전달)은 같지만, 더 빠르고 추적 가능하며 다른 시스템과 통합이 훨씬 쉬워진다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **자동화** | 복잡한 [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인 [[208_schedule_history_transaction_execution_order|스케줄]]링 |
| **[[229_monitor|모니터]]링** | 잡 실행 이력·상태 중앙 관리 |
| **의존성 관리** | [[094_data_availability_da_layer_celestia|데이터 가용성]] 기반 자동 [[507_acid_properties|트리거]] |

[[061_on_premise_legacy_infrastructure|온프레미스]] [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 환경에서는 Oozie가 여전히 현역이지만, 클라우드 [[146_lakehouse|레이크하우스]]로 이전하는 기업들은 Airflow·AWS MWAA·Google Cloud Composer로 [[123_pipe|파이프]]라인을 마이그레이션하고 있다.

- **📢 섹션 요약 비유**: Oozie의 현재 위치는 구형 공장 기계와 같다. 오래됐지만 아직 현역이고, 대체 작업은 계획 중이다. 단, 새로 짓는 공장(신규 클라우드 환경)에는 최신 설비(Airflow)만 들어간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[168_airflow_dag_pipeline_scheduling|Apache Airflow]]** | Oozie의 현대적 대안 |
| **[[401_bayesian_network_dag_causality|DAG]]** | 워크플로 비순환 의존성 [[070_graph_datastructure|그래프]] |
| **[[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[020_yarn|YARN]]** | Oozie 잡 실행 환경 |
| **코디네이터** | 시간/[[001_dikw_pyramid|데이터]] 기반 워크플로 [[507_acid_properties|트리거]] |
| **NiFi** | GUI 기반 [[001_dikw_pyramid|데이터]] 플로우 관리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cron + 쉘 스크립트 — 기본 배치 스케줄링]
    │
    ▼
[Apache Oozie — Hadoop 전용 워크플로 스케줄러]
    │
    ▼
[Apache Airflow — Python DAG 기반 범용 오케스트레이터]
    │
    ▼
[클라우드 관리형 — AWS MWAA, GCP Composer]
    │
    ▼
[AI 파이프라인 — MLflow·Kubeflow·Vertex AI 워크플로]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Oozie는 [[001_dikw_pyramid|데이터]] 공장 자동화 관리자예요! 매일 정해진 시간에 [[001_dikw_pyramid|데이터]] 처리 작업을 순서대로 자동 실행해요.
2. 현대 [[001_dikw_pyramid|데이터]] 엔지니어는 Airflow를 더 선호해요 — Python으로 [[123_pipe|파이프]]라인을 쉽게 작성하고 예쁜 화면으로 [[229_monitor|모니터]]링할 수 있어요!
3. Oozie는 [[061_on_premise_legacy_infrastructure|온프레미스]] [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 환경에서 여전히 현역이지만, 클라우드로 이전할 때는 Airflow로 마이그레이션한답니다!
