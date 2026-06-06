---
title: "216. Lambda Kappa Architecture Batch Realtime"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Lambda 아키텍처는 배치 레이어(Batch Layer)와 스피드 레이어([Speed Layer](/studynote/12_it_management/02_itsm_itil/092_GPT_NLP/))를 병렬로 운영해 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)과 저지연을 동시에 달성하는 [이중 경로](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) 설계이며, [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처는 스트리밍 하나로만 모든 처리를 통일해 복잡성을 제거한다.
> 2. **가치**: Lambda는 배치의 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)과 실시간의 속도를 모두 확보하지만 코드 중복과 운영 복잡성이 높고, Kappa는 단순하지만 재처리 시 스트리밍 리플레이(Replay) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 의존한다.
> 3. **판단 포인트**: 현대 클라우드 환경에서는 Flink·Kafka의 성숙으로 Kappa가 실용적이나, 레거시 배치 의존도가 높거나 복잡한 히스토리컬 분석이 필요하면 Lambda가 여전히 유효하다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 아키텍처의 딜레마

빅데이터 시대 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼은 두 가지 상충된 요구를 받았다.

| 요구 | 내용 | 전통적 해법의 한계 |
|:---|:---|:---|
| <strong><a href="/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a></strong> | 수TB 히스토리 배치 집계 | 배치만으로는 T+1일 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| **저지연** | 수 초 내 실시간 업데이트 | 실시간만으로는 재처리 어려움 |

Nathan Marz가 2011년 Lambda 아키텍처를 제안하며 두 경로를 병렬로 운영하는 해법을 제시했고, Jay Kreps가 2014년 [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처로 이를 단순화했다.

### 1.2 두 아키텍처의 탄생 배경

```
Lambda: "정확성(배치) + 속도(스트리밍)를 모두 갖자"
        -> 두 파이프라인 병렬 운영

Kappa:  "스트리밍 기술이 충분히 성숙했다면 하나면 충분하다"
        -> 단일 스트리밍 파이프라인
```

📢 **섹션 요약 비유**: Lambda는 '빠른 지하철 + 정확한 기차' 두 노선을 동시에 운영하는 것이고, Kappa는 '고속 KTX 하나'로 모든 노선을 대체하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Lambda 아키텍처 상세 구조

```
데이터 소스
(Kafka, DB 등)
     |
     +-----------------------------------------------------+
     |                                                     |
     v                                                     v
+----------------------------------+   +----------------------------+
|         배치 레이어               |   |       스피드 레이어          |
|         (Batch Layer)            |   |       (Speed Layer)         |
|                                  |   |                            |
|  - Hadoop MapReduce / Spark      |   |  - Kafka + Flink/Spark     |
|  - 전체 데이터 집계               |   |  - 최근 N시간 실시간 집계   |
|  - 정확한 결과, 느린 처리         |   |  - 빠른 결과, 근사치 가능   |
|  - 주기: 시간/일 단위 배치        |   |  - 주기: 초/분 단위 실시간  |
+--------------+-------------------+   +--------------+-------------+
               |                                      |
               v                                      v
+-------------------------+         +------------------------------+
|    배치 뷰 (Batch View)  |         |   실시간 뷰 (Real-time View) |
|  (전체 정확 집계 결과)   |         |   (최근 데이터 빠른 집계)    |
+------------+------------+         +--------------+---------------+
             +------------------+------------------+
                                | 쿼리 시 병합(Merge)
                                v
                    +----------------------+
                    |    서빙 레이어        |
                    |    (Serving Layer)    |
                    |  배치 뷰 + 실시간 뷰  |
                    |  병합하여 최종 응답   |
                    +----------------------+
```

### 2.2 [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처 상세 구조

```
데이터 소스
(Kafka, DB 등)
     |
     v
+----------------------------------------------------------+
|               단일 스트리밍 레이어                         |
|           (Single Streaming Layer)                        |
|                                                          |
|  - Kafka + Flink / Kafka Streams                         |
|  - 실시간 처리 + 재처리(Reprocessing) 통합               |
|  - 로그 보존으로 어떤 시점이든 재처리 가능               |
+--------------------------+-------------------------------+
                           |
                           v
              +--------------------------+
              |       서빙 레이어         |
              |    (Serving Layer)        |
              |  단일 결과, 단일 관리     |
              +--------------------------+
```

### 2.3 재처리 (Reprocessing) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| 아키텍처 | 재처리 방법 | 복잡도 |
|:---|:---|:---|
| **Lambda** | 배치 레이어 재실행 (Spark Job 재구동) | 낮음 (배치는 독립적) |
| <strong><a href="/studynote/16_bigdata/12_trends/235_kappa/">Kappa</a></strong> | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 오프셋 리셋 후 스트리밍 재처리 | 중간 (리플레이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 의존) |

[Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 재처리 흐름:
```
1. Kafka 토픽의 오프셋을 처음(0)으로 리셋
2. 새 컨슈머 그룹으로 전체 데이터 다시 처리
3. 새 서빙 레이어 테이블에 결과 저장
4. 기존 서빙 테이블과 스왑 (블루-그린 배포 방식)
5. 이전 결과 삭제
```

📢 **섹션 요약 비유**: Lambda는 두 손으로 밥을 먹는 것(왼손=배치, 오른손=실시간) — 정확하고 빠르지만 두 손을 다 써야 한다. Kappa는 젓가락 하나로 모든 걸 해결하는 고수의 방법이다.

---

## Ⅲ. 비교 및 연결

### 3.1 Lambda vs [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 종합 비교

| 항목 | Lambda 아키텍처 | [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처 |
|:---|:---|:---|
| **레이어 수** | 3개 (Batch·Speed·Serving) | 1~2개 (Streaming·Serving) |
| **코드 중복** | 배치/스트리밍 로직 이중 구현 | 단일 구현 |
| <strong><a href="/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a></strong> | 높음 (배치로 보정) | 중~높음 (스트리밍 성숙도에 의존) |
| <strong><a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong> | Speed Layer로 저지연 | 스트리밍으로 저지연 |
| **재처리** | 배치 레이어에서 독립 재처리 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 리플레이 필요 |
| **운영 복잡성** | 높음 (두 파이프라인 관리) | 낮음 (단일 파이프라인) |
| **적합 환경** | 레거시 혼용, 복잡한 집계 | [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/), [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 중심 |

### 3.2 현대 플랫폼 적용 사례

| 회사 | 아키텍처 | 구체적 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) |
|:---|:---|:---|
| Netflix | Lambda -> [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 전환 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Flink |
| LinkedIn | Lambda [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 도입, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 주도 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Samza |
| Uber | Lambda 변형 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Flink + [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) |
| Twitter | [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) + Storm -> Heron |

📢 **섹션 요약 비유**: Lambda에서 Kappa로의 전환은 '2중 장부 회계'에서 '디지털 단일 장부 회계'로 바꾸는 것이다 — 예전엔 현금 장부와 전자 장부를 따로 맞춰야 했지만, 이제는 하나의 시스템으로 실시간·과거 분석이 모두 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 아키텍처 선택 결정 트리

```
실시간 처리가 필수인가?
       |
       +-- YES --► 배치 정확성도 동시에 필요한가?
       |                |
       |                +-- YES, 레거시/복잡 집계 --► Lambda 아키텍처
       |                |
       |                +-- NO, 클라우드 네이티브  --► Kappa 아키텍처
       |
       +-- NO --► 순수 배치 아키텍처 (Hadoop/Spark)
```

### 4.2 Lambda 아키텍처의 핵심 구현 과제

| 과제 | 설명 | 해법 |
|:---|:---|:---|
| <strong>코드 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong> | 배치·스트리밍 로직이 달라지면 결과 불일치 | 공통 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 추출 |
| **병합 복잡성** | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시 배치 뷰와 실시간 뷰를 합쳐야 함 | Druid·[Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/) 병합 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| **운영 오버헤드** | 두 파이프라인 모니터링 이중 비용 | 통합 관제 시스템 |

📢 **섹션 요약 비유**: Lambda 아키텍처의 코드 중복 문제는 '같은 내용의 한국어·영어 번역본을 동시에 관리하는 것'이다 — 내용이 바뀌면 두 문서를 모두 수정해야 하고, 실수로 하나만 바꾸면 불일치가 발생한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 아키텍처별 기대효과

| 아키텍처 | 주요 효과 | 주의점 |
|:---|:---|:---|
| **Lambda** | [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)·속도 동시 확보, 레거시 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) | 운영 복잡성, 코드 중복 |
| <strong><a href="/studynote/16_bigdata/12_trends/235_kappa/">Kappa</a></strong> | 단순성, 빠른 배포, 코드 단일화 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 토픽 보존 비용, 재처리 시간 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 <strong>"두 아키텍처의 트레이드오프를 시스템 맥락에 따라 판단하는 능력"</strong>을 보여야 한다. Lambda는 배치 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)이 비즈니스 요건인 금융·정산 시스템에 적합하고, Kappa는 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반 마이크로서비스가 이미 구축된 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서 운영 단순성의 가치가 크다는 점을 구체적으로 서술하면 고득점이다.

📢 **섹션 요약 비유**: Lambda vs [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 선택은 '자동차 두 대 vs 고성능 오토바이 한 대' 선택과 같다 — 안전성과 다양성이 필요하면 두 대(Lambda), 속도와 단순함이 우선이면 오토바이 한 대([Kappa](/studynote/16_bigdata/12_trends/235_kappa/))다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| Lambda 구성 | 배치·스피드·서빙 레이어 | 3계층 [이중 경로](/studynote/02_operating_system/08_storage_and_io_systems/500_multipath_io/) 처리 |
| [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 구성 | 단일 스트리밍 레이어 | 스트리밍으로 모든 처리 통합 |
| 재처리 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 리플레이 (Replay) | Kappa의 [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) 대안 |
| 서빙 기술 | Apache Druid / [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/) | 배치+실시간 뷰 병합 서빙 |
| 배치 엔진 | [Hadoop MapReduce](/studynote/07_enterprise_systems/06_exam_summary/395_hadoop_mapreduce_disk_bottleneck/) / [Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/) | Lambda 배치 레이어 |
| 스트림 엔진 | [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/) / [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams | Lambda 스피드 / [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 레이어 |

### 👶 어린이를 위한 3줄 비유 설명

1. Lambda 아키텍처는 '빠른 맛보기 주스'와 '시간이 걸리는 진짜 착즙 주스'를 동시에 만드는 가게야 — 손님은 빠른 주스를 먼저 받고, 나중에 정확한 주스로 교체해줘.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 전용 (MapReduce: 높은 지연)
    |
    v
Lambda: Batch Layer + Speed Layer 병행 -> Serving Layer
    | 코드 중복 · 유지보수 복잡
    v
Kappa: Speed Layer만 (Kafka 리플레이로 배치 대체)
    |
    v
Lakehouse 패턴: Delta Lake 스트리밍 + 배치 통합
```
2. [Kappa](/studynote/16_bigdata/12_trends/235_kappa/) 아키텍처는 '최신 고속 착즙기 하나'로 빠르고 정확하게 주스를 만들어서 두 대 기계가 필요 없는 가게야.
3. 어떤 방식이 좋냐고? 오래된 레시피(레거시 배치)가 많으면 Lambda, 처음부터 최신 기계로 만들었다면 Kappa가 훨씬 편해!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 216 / 258

<- **이전**: [215. 아파치 플링크 (Apache Flink) 네이티브 스트림 워터마크 윈도우](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/)
**다음**: [217. CDC (Change Data Capture) 빈로그 데이터 변경 캡처 Debezium](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ->

---
