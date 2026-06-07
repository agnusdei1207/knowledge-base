---
title: "Pipe-Filter Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 134
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 패턴 ([Pipe-Filter Pattern](/studynote/11_design_supervision/06_exam_summary/433_process/))은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리를 독립적인 처리 단계(필터, Filter)들의 연속적인 체인으로 구성하고, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))로 필터 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전달하는 아키텍처 패턴으로, 각 필터가 입력을 받아 변환·처리하여 출력을 내보내는 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 형성한다.
> 2. **가치**: 각 필터가 독립적이고 교체·재조합 가능하며, 필터 간 인터페이스만 일치하면 새 필터 추가나 순서 변경이 자유롭다. Unix [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)(|), Java [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) Streams가 대표적 구현이다.
> 3. **판단 포인트**: [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 패턴은 순차 처리와 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리, [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) vs 양방향 등 변형이 다양하므로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 요구사항에 따라 필터의 조합과 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 유형(동기·비동기, 순서 보장 여부)을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 패턴은 Unix의 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)(`cat file.txt | grep 'error' | sort | uniq`)에서 유래한 아키텍처 패턴이다. 각 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(필터)는 표준 입출력([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/))을 통해 연결되며, 서로의 내부 구현을 알 필요가 없다.

이 패턴은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인, [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/)(Extract-Transform-Load), 이미지·오디오 처리, 텍스트 분석, [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 등 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 일련의 변환 단계를 거치는 모든 시나리오에 적용된다.

```text
+-------------------------------------------------------------+
|             파이프-필터 패턴 구조                             |
+-------------------------------------------------------------+
|  입력 데이터                                                 |
|      |                                                      |
|  +---v---+  파이프  +-------+  파이프  +-------+           |
|  |필터 A  | ------> |필터 B  | ------> |필터 C  |           |
|  |(검증)  |         |(변환)  |         |(집계)  |           |
|  +-------+         +-------+         +---+---+           |
|                                          |                  |
|                                      출력 데이터             |
|  각 필터: 독립적, 재사용 가능, 교체 가능                    |
|  파이프: 동기(메모리) 또는 비동기(메시지 큐)                |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 공장 조립 라인처럼 원자재(입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 컨베이어 벨트([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/))를 따라 이동하며 각 작업대(필터)에서 가공된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

필터는 세 가지 유형으로 분류된다. ① 생산자(Producer): 외부 소스에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기, ② 변환자([Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)): [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리·변환, ③ 소비자(Consumer): 최종 출력 저장·전송.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| Producer | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스에서 읽기 | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Consumer, DB [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) |
| [Transformer](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환·처리 | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 파싱, 필드 변환, 집계 |
| Consumer | 최종 저장·전송 | DB 저장, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 전송, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 출력 |

```text
+-------------------------------------------------------------+
|       ETL 파이프라인 예시 (파이프-필터 적용)                 |
+-------------------------------------------------------------+
|  [Producer]      [Transformer]    [Transformer]  [Consumer] |
|  DB 쿼리    ->   JSON 파싱    ->   필드 매핑    ->  Elasticsearch|
|               (Kafka Topic A)  (Kafka Topic B)   저장        |
|                                                             |
|  각 단계가 Kafka Topic(파이프)으로 연결됨                    |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 조리법(레시피)에서 재료를 손질->볶기->간 맞추기->플레이팅 순서로 처리하듯, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 단계적으로 변환한다.

---
## Ⅲ. 비교 및 연결

[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터의 실무 도전은 오류 처리와 백프레셔(Backpressure)다. [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 중간 필터에서 오류 발생 시 재처리(Retry), 사이드 채널(Dead Letter [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 처리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필요하다.

| 비교 축 | A | B |
|:---|:---|:---|
| 필터 독립성 | 독립 (재사용·교체 용이) | 종속 (함수 간 직접 호출) |
| [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 | 쉬움 (필터별 독립 실행) | 어려움 |
| 확장성 | 새 필터 추가 용이 | 기존 코드 수정 필요 |
| 복잡성 | [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 관리 필요 | 단순하지만 유연성 낮음 |

- **📢 섹션 요약 비유**: [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 중간 단계(필터)가 느려지면 전체 속도가 그 필터에 맞춰진다. 병목 필터를 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 확장하거나 비동기 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)(메시지 큐)를 도입하여 해소한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 패턴을 적용하면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 로직이 독립적인 필터로 분리되어 테스트·유지보수가 쉬워진다. 필터를 재조합하여 다양한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 구성할 수 있다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 각 필터가 독립적으로 테스트·배포 가능한가?
2. 필터 간 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)가 인터페이스로 추상화되어 동기·비동기 구현을 교체할 수 있는가?
3. [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 중간의 오류를 처리하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(DLQ, Retry, Skip)이 정의되어 있는가?
4. 병목 필터를 수평 확장([Scale-Out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))할 수 있는 구조인가?
5. 비동기 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 사용 시 순서 보장([Ordering](/studynote/02_operating_system/04_synchronization/277_semaphore_ordering/))이 필요한 경우 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 있는가?

- **📢 섹션 요약 비유**: 공장 품질 검사처럼, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 각 단계(필터)가 불량품(오류 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 발견하면 불량품 라인(DLQ)으로 보내고 정상 제품만 다음 단계로 넘긴다.

---

## Ⅴ. 기대효과 및 결론

[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 패턴을 적용하면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 로직이 독립적인 필터로 분리되어 테스트·유지보수가 쉬워진다. 필터를 재조합하여 다양한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 구성할 수 있으며, [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행으로 처리량도 향상된다.

한계는 상태를 가진 필터(Stateful Filter) 처리가 복잡하고, 필터 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 오버헤드가 있으며, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 디버깅이 어렵다. [Apache Flink](/studynote/14_data_engineering/05_exam_keywords/215_flink_native_stream_watermark_window_time/)·[Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams를 활용한 실시간 스트리밍 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터가 미래 방향이다.

- **📢 섹션 요약 비유**: 요리 레시피처럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 여러 단계를 거쳐 최종 결과물로 변환된다. 각 단계(필터)가 독립적이어서 새 조리법([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인)을 쉽게 만들 수 있다.

---

### 📌 관련 개념 맵

[Unix [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) 개념] -> [파이프-필터 패턴] -> [Java [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)] -> Apache Kafka Streams] -> [서버리스 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인] -> [ML [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인]

| 개념 | 연결 포인트 |
|:---|:---|
| [Chain of Responsibility](/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/) | 요청 처리를 위한 핸들러 체인 ([파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터 유사) |
| [Decorator](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) 패턴 | 기능을 단계적으로 추가 (필터 체인과 유사) |
| [Apache Kafka](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/) | 비동기 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) 구현의 대표 메시지 큐 |
| Java [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 동기 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터의 함수형 구현 |

### 📈 관련 키워드 및 발전 흐름도

[Unix 파이프] -> [파이프-필터 패턴] -> ETL [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인] -> Kafka Streams 실시간] -> [서버리스 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인] -> AI/ML [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인]

### 👶 어린이를 위한 3줄 비유 설명

1. [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)-필터는 물이 여러 정수 필터를 거쳐 깨끗해지는 것처럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 단계별로 처리해요.
2. 각 필터(단계)가 독립적이어서 하나를 바꿔도 다른 단계에 영향을 주지 않아요.
3. Unix [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)(|)가 바로 이 패턴의 가장 간단한 예시예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 190 / 530

<- **이전**: [133. 부패 방지 레이어 (Anti-Corruption Layer (ACL))](/studynote/11_design_supervision/02_architecture_principles/133_anti_corruption_layer/)
**다음**: [135. 블랙보드 패턴 (Blackboard Pattern)](/studynote/11_design_supervision/02_architecture_principles/135_blackboard_pattern/) ->

---
