---
title: 6. 반정형 데이터 — JSON/XML/HTML/CSV — 스키마 부분 보유
date: '2024-05-20'
description: JSON/XML/CSV 등 반정형 데이터의 구조, 파싱 메커니즘, 그리고 실무적 활용 방안
tags:
- bigdata
---

# [[003_semi_structured_data|반정형 데이터]] ([[003_semi_structured_data|Semi-Structured Data]])

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 고정된 테이블 [[005_schema|스키마]] 대신 [[001_dikw_pyramid|데이터]] 내부에 태그나 마커를 포함하여 스스로 구조를 설명(Self-Describing)하는 유연한 [[001_dikw_pyramid|데이터]] 형식이다.
> 2. **가치**: [[005_schema|스키마]]리스(Schemaless) 환경을 지원하여 빠른 시스템 연동, [[035_nosql|NoSQL]] 적재, 이기종 간 [[001_dikw_pyramid|데이터]] 교환에 핵심적 역할을 하며 [[001_dikw_pyramid|데이터]] 처리 민첩성을 극대화한다.
> 3. **융합**: RDBMS(Relational [[501_database|Database]] [[372_management|Management]] System)의 [[343_json|JSON]] 지원 확장, [[208_data_lake_schema_on_read|데이터 레이크]]([[208_data_lake_schema_on_read|Data Lake]])에서의 다형성 수용 등 정형-[[004_unstructured_data|비정형 데이터]]의 브릿지 역할을 수행한다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[003_semi_structured_data|반정형 데이터]] ([[003_semi_structured_data|Semi-Structured Data]])는 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]처럼 엄격한 테이블 구조를 가지지 않지만, [[001_dikw_pyramid|데이터]] 내부에 [[012_metadata|메타데이터]](태그, 마커 등)를 포함하여 자체적인 [[369_logic_bomb|논리]]적 구조를 지니는 [[001_dikw_pyramid|데이터]] 형태이다. 인터넷 기술이 발전하면서, 이기종 시스템 간의 통신과 다양한 형태의 정보 교환이 폭발적으로 증가했다. 기존 RDBMS 중심의 강결합 [[005_schema|스키마]]는 잦은 변경과 다양한 비즈니스 요구사항을 즉각적으로 수용하기 어려웠다.

이러한 한계를 극복하기 위해, [[001_dikw_pyramid|데이터]] 자체가 자신의 구조를 서술하는 방식이 고안되었다. [[343_json|JSON]], XML, YAML 등이 대표적이며, 이들은 애플리케이션 개발의 민첩성을 높이고 [[001_dikw_pyramid|데이터]] 수집 및 교환 시의 파싱 오버헤드를 [[198_abstraction_control_data_process|추상화]]한다. 현대의 웹 [[014_api_posix|API]] 통신, [[626_log_collection|로그 수집]], [[101_iot_concept|IoT]] 센서 [[001_dikw_pyramid|데이터]] 수집 등 빅데이터의 앞단에서는 거의 모든 [[001_dikw_pyramid|데이터]]가 반정형 형태로 오고 간다. 결국 [[003_semi_structured_data|반정형 데이터]]는 빅데이터의 '다양성(Variety)'과 '속도(Velocity)'를 충족시키는 핵심 매개체다.

```text
이 도식은 기존의 고정 스키마 환경에서 발생하는 데이터 연동 병목과, 반정형 데이터 도입으로 인한 유연한 데이터 흐름을 비교하여 보여준다. 

[기존 정형 데이터 환경]
Client(Data) ──(스키마 불일치 발생)──> [Schema Validator] ──(파싱 에러 큐 체증)──> RDBMS
                                            ▲ 병목 지점 (잦은 DDL 필요)

[반정형 데이터 환경]
Client(JSON) ──(Self-Describing)──> [API Gateway / Parser] ──(유연한 적재)──> NoSQL / Data Lake
```
이 흐름의 핵심은 [[395_verification_process_review|검증]] 단계의 위치와 유연성이다. 고정 [[005_schema|스키마]] 환경에서는 [[005_schema|스키마]] 변경 시 DB의 [[020_ddl|DDL]] 수정이 동반되어야 하므로 배포와 연동의 병목이 발생한다. 반면 [[003_semi_structured_data|반정형 데이터]]는 애플리케이션 레벨에서 파싱하고 처리할 수 있어 시스템 간 [[195_coupling_levels|결합도]]를 낮춘다. 실무에서는 이러한 유연성 덕분에 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]]) 환경에서 [[003_semi_structured_data|반정형 데이터]]가 표준 통신 포맷으로 자리 잡게 되었다.

> 📢 **섹션 요약 비유**: 마치 내용물이 바뀔 때마다 맞춤형 상자를 새로 만들어야 하는 [[002_structured_data|정형 데이터]]와 달리, [[003_semi_structured_data|반정형 데이터]]는 신축성 있는 보자기처럼 내용물에 맞게 스스로 형태를 변형하여 포장하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[003_semi_structured_data|반정형 데이터]]의 내부 아키텍처는 텍스트 기반의 [[149_serial_communication_rs232_rs485|직렬]]화 포맷을 프로그램이 이해할 수 있는 객체 트리로 변환하는 '파서(Parser)' 메커니즘을 근간으로 한다. [[001_dikw_pyramid|데이터]]는 계층적 트리 구조(Tree Structure)를 형성하며, 각 노드는 키-값 쌍([[067_db_key_uniqueness_minimality|Key]]-Value)이나 태그로 구성된다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | [[295_protocol_field_tcp_udp_icmp|프로토콜]]/포맷 | 비유 |
|:---|:---|:---|:---|:---|
| **Serializer** | 객체를 문자열로 [[149_serial_communication_rs232_rs485|직렬]]화 | 메모리 내 객체 트리를 [[343_json|JSON]]/XML 문자열로 변환하여 전송 가능하게 함 | [[343_json|JSON]].stringify() | 택배 포장기 |
| **Deserializer** | 문자열을 객체로 역직렬화 | 수신된 텍스트를 파싱하여 메모리 내 AST(Abstract Syntax Tree)로 구성 | [[343_json|JSON]].parse() | 택배 해체기 |
| **DOM Parser** | 전체 구조 메모리 로드 | 문서 전체를 읽어 트리 구조를 메모리에 [[087_process_state_transition|생성]] (탐색 용이, 메모리 큼) | [[037_document|Document]] Object Model | 책 전체 암기 |
| **SAX Parser** | 스트림 기반 순차 파싱 | 문서를 순차적으로 읽으며 이벤트 발생 (메모리 절약, 탐색 제한) | Simple [[014_api_posix|API]] for XML | 오디오북 청취 |
| **Validator** | [[005_schema|스키마]] 정합성 [[395_verification_process_review|검증]] | [[343_json|JSON]] [[505_schema|Schema]] 등을 통해 필수 키와 [[001_dikw_pyramid|데이터]] 타입 동적 [[395_verification_process_review|검증]] | [[343_json|JSON]] [[505_schema|Schema]] | 세관 검사대 |

[[003_semi_structured_data|반정형 데이터]]를 처리할 때 메모리 레이아웃과 파싱 방식의 선택은 [[282_performance_tactics|성능]]에 직결된다. 특히 대용량 [[343_json|JSON]]/XML [[501_file_definition_logical_record|파일]]을 파싱할 때는 DOM 방식과 스트림 방식의 트레이드오프가 극명하게 나타난다.

```text
이 도식은 대용량 반정형 데이터를 처리할 때 DOM 파서와 스트림(SAX/Streaming) 파서의 메모리 버퍼 레이아웃과 병목 지점을 비교한다. 대용량 파일 처리 시 아키텍처 선택의 기준이 된다.

┌─────────────── Memory (DOM Parser) ───────────────┐
│ [파일 전체 로드] >>> 메모리 폭발 위험(OOM)        │
│ └─ Node 1                                         │
│    ├─ Node 1.1                                    │
│    └─ Node 1.2                                    │
└───────────────────────────────────────────────────┘
                           ▲ 병목: 크기가 수백 MB 이상일 경우 스왑 발생 및 시스템 마비

┌─────────────── Memory (Stream Parser) ────────────┐
│ [Chunk 단위 로드] -> [Event Emit] -> [Garbage Col]│
│ Chunk 1 (Node 1) 처리 후 즉시 해제                │
│ Chunk 2 (Node 1.1) 처리 후 즉시 해제              │
└───────────────────────────────────────────────────┘
                           ▲ 이점: 지속적이고 일정한 메모리 사용량 (O(1))
```
이 도식에서 핵심은 DOM 방식이 메모리(RAM)에 문서 전체의 트리 구조를 올리기 때문에 임의 접근(Random Access)이 빠른 반면 대용량 [[001_dikw_pyramid|데이터]]에서 [[157_oom_killer|OOM]]([[157_oom_killer|Out of Memory]])을 유발한다는 점이다. 반면 스트림 방식은 이벤트를 기반으로 순차 처리하므로 메모리 사용량이 일정하지만 이전 [[001_dikw_pyramid|데이터]]로 되돌아가기 어렵다. 실무에서는 수십 MB 이상의 [[568_logs_distributed_logging_elk_fluentd|로그]]나 센서 [[001_dikw_pyramid|데이터]]를 처리할 때 반드시 스트림 기반 파서를 적용하여 노드 메모리 자원을 [[571_protection_vs_security|보호]]해야 한다.

동작 원리 관점에서 역직렬화(Deserialization)는 ①문자열 토크나이징(Tokenizing) → ②구문 분석(Syntax Analysis) → ③객체 [[087_process_state_transition|생성]]의 단계를 거친다.

```python
# 파이썬 기반 JSON 역직렬화 및 예외 처리 코드 스니펫
import json

raw_data = '{"sensor_id": 101, "temp": 22.5, "status": "active"}'

try:
    # 1단계 & 2단계: 문자열 읽기 및 구문 분석 (파서 엔진 수행)
    # 3단계: 딕셔너리 객체로 메모리에 생성
    parsed_data = json.loads(raw_data) 
    
    # 4단계: 동적 스키마 처리 (데이터 내부의 키로 직접 접근)
    if parsed_data.get("temp") > 20.0:
        print(f"Warning: Sensor {parsed_data['sensor_id']} high temp!")
except json.JSONDecodeError as e:
    # 파싱 실패에 대한 폴백 서술
    print(f"Malformed JSON data: {e}")
```
위 코드는 [[003_semi_structured_data|반정형 데이터]]가 어떻게 별도의 [[012_metadata|메타데이터]] 정의 없이 스스로 [[001_dikw_pyramid|데이터]] 타입을 추론(Self-Describing)하여 로직에 활용되는지 보여준다. RDBMS였다면 `sensor_id`와 `temp`의 [[001_dikw_pyramid|데이터]] 타입이 명시된 테이블이 필요하지만, 여기서는 파서가 동적으로 타입(int, float, string)을 맵핑한다.

> 📢 **섹션 요약 비유**: [[003_semi_structured_data|반정형 데이터]]의 파싱 과정은 마치 외국어 편지를 번역가(Parser)가 읽고 즉시 뇌(메모리)에 이해할 수 있는 개념 지도(Tree)로 그려주는 통역 과정과 같습니다. 전체를 다 외울지, 한 줄씩 들으면서 처리할지가 [[282_performance_tactics|성능]]의 핵심입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

빅데이터 환경에서는 정형(Structured), 반정형(Semi-Structured), 비정형(Unstructured) [[001_dikw_pyramid|데이터]]가 혼재되어 사용된다. 시스템 설계자는 각 [[001_dikw_pyramid|데이터]] 형식의 장단점과 오버헤드를 비교하여 최적의 저장소와 처리 엔진을 선택해야 한다.

```text
이 매트릭스는 세 가지 데이터 유형의 특성을 구조화 수준, 저장소, 쿼리 유연성 측면에서 비교하여, 아키텍처 설계 시 적절한 데이터 스토어와 형식을 선택하는 판단 기준을 제공한다.

┌────────────┬───────────────┬────────────────┬───────────────┬──────────────┐
│ 특성       │ 정형 데이터   │ 반정형 데이터  │ 비정형 데이터 │ 판단 포인트  │
├────────────┼───────────────┼────────────────┼───────────────┼──────────────┤
│ 구조 수준  │ 강한 스키마   │ 스키마리스/내재│ 스키마 없음   │ 데이터 유연성│
│ 대표 포맷  │ RDB, CSV      │ JSON, XML      │ 텍스트, 영상  │ 직렬화 오버헤드
│ 주 저장소  │ RDBMS, DW     │ NoSQL, Document│ Object Storage│ 확장성 비용  │
│ 탐색/쿼리  │ SQL (결정적)  │ JSON Path, 동적│ ML/AI 분석    │ 쿼리 레이턴시│
│ 시스템 예  │ Oracle, MySQL │ MongoDB, Redis │ S3, HDFS      │ 생태계 호환성│
└────────────┴───────────────┴────────────────┴───────────────┴──────────────┘
```
이 표의 핵심은 [[003_semi_structured_data|반정형 데이터]]가 정형과 비정형 사이에서 절충점(Trade-off)을 제공한다는 점이다. [[002_structured_data|정형 데이터]]는 [[298_qkv_attention|쿼리]] 속도와 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]이 높지만 [[005_schema|스키마]] 변경 시 시스템 다운타임이나 마이그레이션 비용이 발생한다. [[003_semi_structured_data|반정형 데이터]]는 [[005_schema|스키마]] 변경에 매우 유연하여 빠른 [[004_agile_relation|애자일]] 개발에 적합하지만, 깊은 계층의 [[001_dikw_pyramid|데이터]]를 조회할 때 파싱 오버헤드로 인해 RDBMS의 [[154_database_index_b_tree_search_optimization|인덱스]] 기반 검색보다 느려질 수 있다. 따라서 실무에서는 [[001_dikw_pyramid|데이터]]의 구조 변경 빈도와 읽기/[[289_cqrs_db|쓰기]] 비율을 기준으로 저장 형식을 결정해야 한다.

[[002_database_definition|데이터베이스]](DB) 과목과의 융합 관점에서 최근 RDBMS(PostgreSQL, PostgreSQL, [[188_pl_sql_t_sql_procedural|Oracle]] 등)는 [[003_semi_structured_data|반정형 데이터]]를 지원하기 위해 [[343_json|JSON]] 타입 컬럼과 [[343_json|JSON]] 함수를 내장하고 있다. 이는 NoSQL의 유연성과 RDBMS의 ACID [[191_transaction_concept_states|트랜잭션]]을 동시에 얻으려는 하이브리드 접근법이다. 그러나 [[343_json|JSON]] 컬럼 내 [[001_dikw_pyramid|데이터]]에 대한 조인은 [[282_performance_tactics|성능]] 저하가 크므로, 자주 검색되는 키는 추출하여 가상 컬럼(Generated Column)이나 [[162_fbi_function_based_index|함수 기반 인덱스]](Function-based [[154_database_index_b_tree_search_optimization|Index]])를 [[087_process_state_transition|생성]]하는 시너지 설계가 필수적이다.

> 📢 **섹션 요약 비유**: [[002_structured_data|정형 데이터]]가 뼈대가 튼튼한 '콘크리트 건물'이라면, [[004_unstructured_data|비정형 데이터]]는 형태가 없는 '모래더미'이고, [[003_semi_structured_data|반정형 데이터]]는 필요에 따라 조립과 해체가 자유로운 '레고 블록'과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

현업에서 [[003_semi_structured_data|반정형 데이터]] 처리는 주로 [[014_api_posix|API]] 통신, 외부 [[001_dikw_pyramid|데이터]] 수집, [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] 적재 시 빈번하게 발생한다. 특히 [[090_service_kubernetes_network_load_balancing|서비스]]가 확장됨에 따라 [[343_json|JSON]] [[005_schema|스키마]]가 암묵적으로 변경되는 '[[005_schema|스키마]] 드리프트([[268_schema_drift_evolution_delta_lake|Schema Drift]])' 현상은 가장 큰 장애 원인 중 하나다.

```text
이 의사결정 트리는 외부 시스템으로부터 반정형 데이터를 수집하여 저장할 때, 발생할 수 있는 데이터 구조 변화와 무결성 요구에 따라 어떤 아키텍처적 대응을 해야 하는지를 보여주는 운영 플로우다.

[외부 반정형 데이터 수집]
           ↓
(스키마가 자주 변경되는가?)
   ├── Yes ──> (읽기/검색 성능이 중요한가?)
   │              ├── Yes ──> Document NoSQL (MongoDB) 활용 및 인덱싱 적용
   │              └── No  ──> Data Lake (S3)에 원본(Raw) JSON/Parquet 적재
   │
   └── No ───> (트랜잭션 정합성이 필수적인가?)
                  ├── Yes ──> RDBMS에 적재 (JSON 컬럼 + 함수 인덱스 활용)
                  └── No  ──> Columnar DB / OLAP 에 ETL 변환 후 적재
```
이 흐름의 핵심은 '[[005_schema|스키마]]의 가변성'과 '조회 [[282_performance_tactics|성능]]'의 상충 [[083_relationship_in_er_model|관계]]를 조율하는 것이다. [[001_dikw_pyramid|데이터]] 형태가 자주 변하는데 무리하게 정형 DB로 ETL을 수행하면 [[123_pipe|파이프]]라인이 수시로 깨진다([[645_data_pipeline_acceleration|Data Pipeline]] Breakage). 

**실무 [[128_water_scrum_fall_anti_pattern|안티패턴]] ([[161_anti_pattern|Anti-pattern]])**:
[[343_json|JSON]] 문자열을 통째로 RDBMS의 VARCHAR 컬럼에 저장하고, 애플리케이션 단에서 매번 전체를 파싱하여 검색하는 패턴이다. 이 경우 [[002_database_definition|데이터베이스]]의 [[154_database_index_b_tree_search_optimization|인덱스]]를 전혀 타지 못해 Table Full Scan이 발생하며 [[298_qkv_attention|쿼리]] [[282_performance_tactics|성능]]이 기하급수적으로 하락한다.

**도입 및 운영 [[435_checklist_based_testing|체크리스트]]**:
1. **역직렬화 취약점**: 외부 입력 JSON을 [[395_verification_process_review|검증]] 없이 역직렬화 시 원격 코드 실행(RCE) 등의 보안 취약점이 없는가?
2. **[[005_schema|스키마]] 진화 ([[505_schema|Schema]] Evolution) 관리**: [[343_json|JSON]] [[005_schema|스키마]] 변경 시 컨슈머(Consumer) 장애를 막기 위한 하위 [[344_compatibility_usability|호환성]] 룰(Ignore Unknown Fields 등)이 적용되었는가?
3. **[[347_compaction|압축]] 오버헤드**: 수집되는 [[343_json|JSON]] [[501_file_definition_logical_record|파일]]이 텍스트 형태로 너무 커질 경우, 네트워크 [[140_bandwidth|대역폭]] 절감을 위해 Snappy, Gzip 등으로 [[347_compaction|압축]] 전송하고 있는가?

> 📢 **섹션 요약 비유**: [[003_semi_structured_data|반정형 데이터]]라는 자유로운 레고 블록을 실무에서 막 굴리면 엉망진창 장난감 통([[288_data_swamp_metadata_management_absence|Data Swamp]])이 됩니다. 이를 막기 위해선 최소한의 조립 설명서([[005_schema|스키마]] [[395_verification_process_review|검증]])와 알맞은 수납함(적절한 [[035_nosql|NoSQL]]/RDBMS)이 필요합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[[003_semi_structured_data|반정형 데이터]]의 적극적인 수용은 시스템 아키텍처를 강결합에서 느슨한 결합(Loosely Coupled)으로 변화시켰다.

| 지표 | 도입 전 (정형/강결합 중심) | 도입 후 (반정형/유연성 중심) | 개선 효과 |
|:---|:---|:---|:---|
| **개발 민첩성** | [[005_schema|스키마]] 변경 시 DB 반영 대기 | [[014_api_posix|API]] 모델 변경만으로 즉시 배포 | [[085_lead_time_cycle_time|리드 타임]] 50% 단축 |
| **저장 효율성** | 빈 컬럼 NULL 공간 낭비 | 존재하는 [[001_dikw_pyramid|데이터]]만 키-값으로 보관 | 스파스 [[001_dikw_pyramid|데이터]] 저장 효율 증가 |
| **연동 복잡성** | 복잡한 ETL과 ORM 매핑 필수 | [[343_json|JSON]]/[[156_rest_representational_state_transfer|REST]] 기반 직관적 연동 | 시스템 연동 복잡도(O(n^2)→O(n)) 감소 |

미래에는 단순 텍스트 기반의 JSON이나 XML을 넘어, **바이너리 [[003_semi_structured_data|반정형 데이터]] 포맷([[535_sync_communication_rest_grpc|Protocol Buffers]], Avro, MessagePack)**으로의 진화가 가속화되고 있다. 텍스트 파싱의 CPU 오버헤드와 [[236_payload_size_and_padding_46_1500_bytes|페이로드 크기]]를 획기적으로 줄이기 위해 [[532_microservices_decomposition_patterns|마이크로서비스]] 간 내부 통신([[479_grpc_protobuf_http2|gRPC]])이나 [[179_kafka_flink_watermark_time_window|카프카]]([[179_kafka_flink_watermark_time_window|Kafka]]) 기반 스트리밍 [[123_pipe|파이프]]라인에서는 [[005_schema|스키마]] [[235_registry_immutable_tag|레지스트리]]([[505_schema|Schema]] [[235_registry_immutable_tag|Registry]])를 동반한 바이너리 [[149_serial_communication_rs232_rs485|직렬]]화가 표준으로 자리잡고 있다.

또한, GraphQL과 같이 클라이언트가 원하는 [[001_dikw_pyramid|데이터]] 구조를 직접 선언하여 요청하는 방식이 확산되면서, [[003_semi_structured_data|반정형 데이터]]는 단순한 '[[001_dikw_pyramid|데이터]] 포맷'을 넘어 '[[014_api_posix|API]] [[298_qkv_attention|쿼리]] 언어'의 영역까지 기술적 경계를 넓히고 있다. 결국 빅데이터의 가치는 이러한 유연한 [[001_dikw_pyramid|데이터]] 계층을 얼마나 효율적으로 파싱하고 의미 있는 인사이트로 변환해 내느냐에 달려 있다.

> 📢 **섹션 요약 비유**: 과거의 [[003_semi_structured_data|반정형 데이터]]가 텍스트로 적힌 유연한 여권(Passport)이었다면, 미래의 [[003_semi_structured_data|반정형 데이터]]는 칩이 내장되어 기계가 순식간에 읽어내는 전자여권(Binary Serialization)으로 진화하여 글로벌 [[001_dikw_pyramid|데이터]] 고속도로의 핵심 통행증이 되고 있습니다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[002_structured_data|정형 데이터]]** | [[005_schema|스키마]]가 고정된 전통적 [[001_dikw_pyramid|데이터]] |
| **[[003_semi_structured_data|반정형 데이터]]** | 태그/키-값처럼 유연한 구조를 가진 [[001_dikw_pyramid|데이터]] |
| **[[004_unstructured_data|비정형 데이터]]** | 텍스트·이미지 등 자유 형식 [[001_dikw_pyramid|데이터]] |
| **빅데이터 처리** | 다양한 형식을 대규모로 수집·분석하는 기술 |
### 📈 관련 키워드 및 발전 흐름도

```text
[정형 데이터 (Structured Data)]
    │
    ▼
[반정형 데이터 (Semi-Structured Data)]
    │
    ▼
[비정형 데이터 (Unstructured Data)]
    │
    ▼
[빅데이터 처리 (Big Data Processing)]
```

이 흐름도는 [[001_dikw_pyramid|데이터]] 형식이 정형에서 반정형, 비정형으로 넓어지고 빅데이터 처리로 이어지는 과정을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명

1. [[002_structured_data|정형 데이터]]는 칸이 딱 정해진 표 같다.
2. [[003_semi_structured_data|반정형 데이터]]는 태그가 붙은 블록 장난감처럼 유연하다.
3. 빅데이터 처리는 이런 여러 형태를 함께 다룬다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 6 / 262

← **이전**: [[005_unstructured_data|5. 비정형 데이터 유형 — 텍스트/이미지/동영상/음성/로그/SNS/IoT 센서]]
**다음**: [[007_big_data_ecosystem|7. 빅데이터 생태계 — 수집→저장→처리→분석→시각화→활용]] →

---
