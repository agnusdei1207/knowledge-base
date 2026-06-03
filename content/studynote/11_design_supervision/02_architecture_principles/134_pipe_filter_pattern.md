---
title: 134. 파이프-필터 패턴 (Pipe-Filter Pattern)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[123_pipe|파이프]]-필터 패턴 ([[433_process|Pipe-Filter Pattern]])은 [[001_dikw_pyramid|데이터]] 처리를 독립적인 처리 단계(필터, Filter)들의 연속적인 체인으로 구성하고, [[123_pipe|파이프]]([[123_pipe|Pipe]])로 필터 간 [[001_dikw_pyramid|데이터]]를 전달하는 아키텍처 패턴으로, 각 필터가 입력을 받아 변환·처리하여 출력을 내보내는 [[008_단방향_반이중_전이중|단방향]] [[001_dikw_pyramid|데이터]] 흐름을 형성한다.
> 2. **가치**: 각 필터가 독립적이고 교체·재조합 가능하며, 필터 간 인터페이스만 일치하면 새 필터 추가나 순서 변경이 자유롭다. Unix [[123_pipe|파이프]](|), Java [[467_http2_stream_multiplexing_tcp_hol|Stream]] [[014_api_posix|API]], [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] Streams가 대표적 구현이다.
> 3. **판단 포인트**: [[123_pipe|파이프]]-필터 패턴은 순차 처리와 [[430_index_fast_full_scan|병렬]] 처리, [[008_단방향_반이중_전이중|단방향]] vs 양방향 등 변형이 다양하므로, [[001_dikw_pyramid|데이터]] 처리 요구사항에 따라 필터의 조합과 [[123_pipe|파이프]] 유형(동기·비동기, 순서 보장 여부)을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[[123_pipe|파이프]]-필터 패턴은 Unix의 [[271_command_pattern|커맨드]] [[123_pipe|파이프]](`cat file.txt | grep 'error' | sort | uniq`)에서 유래한 아키텍처 패턴이다. 각 [[158_instruction|명령어]](필터)는 표준 입출력([[123_pipe|파이프]])을 통해 연결되며, 서로의 내부 구현을 알 필요가 없다.

이 패턴은 [[001_dikw_pyramid|데이터]] 처리 [[123_pipe|파이프]]라인, [[215_etl_vs_elt_pipeline|ETL]](Extract-Transform-Load), 이미지·오디오 처리, 텍스트 분석, [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 등 [[001_dikw_pyramid|데이터]]가 일련의 변환 단계를 거치는 모든 시나리오에 적용된다.

```text
┌─────────────────────────────────────────────────────────────┐
│             파이프-필터 패턴 구조                             │
├─────────────────────────────────────────────────────────────┤
│  입력 데이터                                                 │
│      │                                                      │
│  ┌───▼───┐  파이프  ┌───────┐  파이프  ┌───────┐           │
│  │필터 A  │ ──────> │필터 B  │ ──────> │필터 C  │           │
│  │(검증)  │         │(변환)  │         │(집계)  │           │
│  └───────┘         └───────┘         └───┬───┘           │
│                                          │                  │
│                                      출력 데이터             │
│  각 필터: 독립적, 재사용 가능, 교체 가능                    │
│  파이프: 동기(메모리) 또는 비동기(메시지 큐)                │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 공장 조립 라인처럼 원자재(입력 [[001_dikw_pyramid|데이터]])가 컨베이어 벨트([[123_pipe|파이프]])를 따라 이동하며 각 작업대(필터)에서 가공된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

필터는 세 가지 유형으로 분류된다. ① 생산자(Producer): 외부 소스에서 [[001_dikw_pyramid|데이터]] 읽기, ② 변환자([[246_transformer_self_attention_parallel_positional_encoding|Transformer]]): [[001_dikw_pyramid|데이터]]를 처리·변환, ③ 소비자(Consumer): 최종 출력 저장·전송.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| Producer | [[001_dikw_pyramid|데이터]] 소스에서 읽기 | [[179_kafka_flink_watermark_time_window|Kafka]] Consumer, DB [[298_qkv_attention|쿼리]] |
| [[246_transformer_self_attention_parallel_positional_encoding|Transformer]] | [[001_dikw_pyramid|데이터]] 변환·처리 | [[343_json|JSON]] 파싱, 필드 변환, 집계 |
| Consumer | 최종 저장·전송 | DB 저장, [[014_api_posix|API]] 전송, [[501_file_definition_logical_record|파일]] 출력 |

```text
┌─────────────────────────────────────────────────────────────┐
│       ETL 파이프라인 예시 (파이프-필터 적용)                 │
├─────────────────────────────────────────────────────────────┤
│  [Producer]      [Transformer]    [Transformer]  [Consumer] │
│  DB 쿼리    →   JSON 파싱    →   필드 매핑    →  Elasticsearch│
│               (Kafka Topic A)  (Kafka Topic B)   저장        │
│                                                             │
│  각 단계가 Kafka Topic(파이프)으로 연결됨                    │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 조리법(레시피)에서 재료를 손질→볶기→간 맞추기→플레이팅 순서로 처리하듯, [[123_pipe|파이프]]-필터는 [[001_dikw_pyramid|데이터]]를 단계적으로 변환한다.

---
## Ⅲ. 비교 및 연결

[[123_pipe|파이프]]-필터의 실무 도전은 오류 처리와 백프레셔(Backpressure)다. [[123_pipe|파이프]]라인 중간 필터에서 오류 발생 시 재처리(Retry), 사이드 채널(Dead Letter [[058_queue|Queue]]) 처리 [[268_strategy_pattern|전략]]이 필요하다.

| 비교 축 | A | B |
|:---|:---|:---|
| 필터 독립성 | 독립 (재사용·교체 용이) | 종속 (함수 간 직접 호출) |
| [[430_index_fast_full_scan|병렬]]화 | 쉬움 (필터별 독립 실행) | 어려움 |
| 확장성 | 새 필터 추가 용이 | 기존 코드 수정 필요 |
| 복잡성 | [[123_pipe|파이프]]라인 관리 필요 | 단순하지만 유연성 낮음 |

- **📢 섹션 요약 비유**: [[123_pipe|파이프]]라인 중간 단계(필터)가 느려지면 전체 속도가 그 필터에 맞춰진다. 병목 필터를 [[430_index_fast_full_scan|병렬]]로 확장하거나 비동기 [[123_pipe|파이프]](메시지 큐)를 도입하여 해소한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[[123_pipe|파이프]]-필터 패턴을 적용하면 [[001_dikw_pyramid|데이터]] 처리 로직이 독립적인 필터로 분리되어 테스트·유지보수가 쉬워진다. 필터를 재조합하여 다양한 [[001_dikw_pyramid|데이터]] 처리 [[123_pipe|파이프]]라인을 구성할 수 있다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 각 필터가 독립적으로 테스트·배포 가능한가?
2. 필터 간 [[123_pipe|파이프]]가 인터페이스로 추상화되어 동기·비동기 구현을 교체할 수 있는가?
3. [[123_pipe|파이프]]라인 중간의 오류를 처리하는 [[268_strategy_pattern|전략]](DLQ, Retry, Skip)이 정의되어 있는가?
4. 병목 필터를 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-Out]])할 수 있는 구조인가?
5. 비동기 [[123_pipe|파이프]] 사용 시 순서 보장([[277_semaphore_ordering|Ordering]])이 필요한 경우 [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]]이 있는가?

- **📢 섹션 요약 비유**: 공장 품질 검사처럼, [[123_pipe|파이프]]라인의 각 단계(필터)가 불량품(오류 [[001_dikw_pyramid|데이터]])을 발견하면 불량품 라인(DLQ)으로 보내고 정상 제품만 다음 단계로 넘긴다.

---

## Ⅴ. 기대효과 및 결론

[[123_pipe|파이프]]-필터 패턴을 적용하면 [[001_dikw_pyramid|데이터]] 처리 로직이 독립적인 필터로 분리되어 테스트·유지보수가 쉬워진다. 필터를 재조합하여 다양한 [[001_dikw_pyramid|데이터]] 처리 [[123_pipe|파이프]]라인을 구성할 수 있으며, [[430_index_fast_full_scan|병렬]] 실행으로 처리량도 향상된다.

한계는 상태를 가진 필터(Stateful Filter) 처리가 복잡하고, 필터 간 [[001_dikw_pyramid|데이터]] 복사 오버헤드가 있으며, [[123_pipe|파이프]]라인 디버깅이 어렵다. [[215_flink_native_stream_watermark_window_time|Apache Flink]]·[[179_kafka_flink_watermark_time_window|Kafka]] Streams를 활용한 실시간 스트리밍 [[123_pipe|파이프]]-필터가 미래 방향이다.

- **📢 섹션 요약 비유**: 요리 레시피처럼 [[001_dikw_pyramid|데이터]]가 여러 단계를 거쳐 최종 결과물로 변환된다. 각 단계(필터)가 독립적이어서 새 조리법([[123_pipe|파이프]]라인)을 쉽게 만들 수 있다.

---

### 📌 관련 개념 맵

[Unix [[123_pipe|Pipe]] 개념] → [파이프-필터 패턴] → [Java [[467_http2_stream_multiplexing_tcp_hol|Stream]] [[014_api_posix|API]]] → [[[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] Streams] → [서버리스 [[123_pipe|파이프]]라인] → [ML [[123_pipe|파이프]]라인]

| 개념 | 연결 포인트 |
|:---|:---|
| [[276_chain_of_responsibility_pattern|Chain of Responsibility]] | 요청 처리를 위한 핸들러 체인 ([[123_pipe|파이프]]-필터 유사) |
| [[262_decorator_pattern_dynamic_wrapper|Decorator]] 패턴 | 기능을 단계적으로 추가 (필터 체인과 유사) |
| [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] | 비동기 [[123_pipe|파이프]] 구현의 대표 메시지 큐 |
| Java [[467_http2_stream_multiplexing_tcp_hol|Stream]] [[014_api_posix|API]] | 동기 [[123_pipe|파이프]]-필터의 함수형 구현 |

### 📈 관련 키워드 및 발전 흐름도

[Unix 파이프] → [파이프-필터 패턴] → [[[215_etl_vs_elt_pipeline|ETL]] [[123_pipe|파이프]]라인] → [[[179_kafka_flink_watermark_time_window|Kafka]] Streams 실시간] → [서버리스 [[123_pipe|파이프]]라인] → [[[190_ai_llm_requirements_specification|AI]]/ML [[123_pipe|파이프]]라인]

### 👶 어린이를 위한 3줄 비유 설명

1. [[123_pipe|파이프]]-필터는 물이 여러 정수 필터를 거쳐 깨끗해지는 것처럼 [[001_dikw_pyramid|데이터]]를 단계별로 처리해요.
2. 각 필터(단계)가 독립적이어서 하나를 바꿔도 다른 단계에 영향을 주지 않아요.
3. Unix [[158_instruction|명령어]] [[123_pipe|파이프]](|)가 바로 이 패턴의 가장 간단한 예시예요!
