---
title: '27. 데이터 직렬화: Avro / Protobuf / Thrift'
date: '2026-04-29'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Avro, [[535_sync_communication_rest_grpc|Protocol Buffers]](Protobuf), Apache Thrift는 구조화된 [[001_dikw_pyramid|데이터]]를 언어·플랫폼 독립적인 바이너리 형식으로 [[149_serial_communication_rs232_rs485|직렬]]화(Serialization)하는 프레임워크로, [[343_json|JSON]]/XML 대비 크기·속도에서 탁월한 효율을 제공한다.
> 2. **가치**: 빅데이터 [[123_pipe|파이프]]라인에서 [[149_serial_communication_rs232_rs485|직렬]]화 형식 선택은 네트워크 비용·[[019_처리_지연|처리 지연]]·스토리지 비용에 직접 영향을 준다. [[179_kafka_flink_watermark_time_window|Kafka]] [[389_mesh_topology|메시]]지 [[149_serial_communication_rs232_rs485|직렬]]화에 [[343_json|JSON]] 대신 Avro를 사용하면 [[389_mesh_topology|메시]]지 크기가 50~70% 줄고 역직렬화 속도가 10배 이상 빨라질 수 있다.
> 3. **판단 포인트**: 세 가지 선택 기준 — ①[[005_schema|스키마]] 진화([[505_schema|Schema]] Evolution) 용이성: Avro > Protobuf ≈ Thrift, ②언어 지원 폭: Protobuf ≈ Thrift > Avro, ③Kafka/[[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 생태계 통합: Avro > Protobuf > Thrift. 실무에서는 [[179_kafka_flink_watermark_time_window|Kafka]]+[[094_reinforcement_learning|Confluent]] [[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] = Avro, [[479_grpc_protobuf_http2|gRPC]] [[090_service_kubernetes_network_load_balancing|서비스]] = Protobuf가 사실상 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌────────────────────────────────────────────────────────┐
│     JSON vs. Avro vs. Protobuf 비교                    │
├─────────────────┬──────────────────────────────────────┤
│ 형식            │ 특징                                  │
├─────────────────┼──────────────────────────────────────┤
│ JSON            │ 사람이 읽기 쉬움, 크기 큼, 파싱 느림 │
│ Avro            │ 바이너리, 스키마 분리, Hadoop 친화    │
│ Protobuf        │ 바이너리, 스키마 필드 번호 기반, gRPC │
│ Thrift          │ 바이너리, RPC 통합, Meta 오리지널     │
└─────────────────┴──────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[149_serial_communication_rs232_rs485|직렬]]화 형식 선택은 국제 소포 포장 방식이다. JSON은 큰 종이 박스(사람이 읽기 쉽지만 부피가 크다), Avro/Protobuf는 진공 포장(작고 빠르지만 기계만 읽을 수 있다).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 각 형식의 [[149_serial_communication_rs232_rs485|직렬]]화 방식

```text
Avro:
  - 스키마를 .avsc 파일(JSON)로 별도 정의
  - 데이터에 스키마 없음 → Schema Registry에서 참조
  - 스키마 진화: 필드 추가/제거 + default값으로 backward/forward 호환

Protobuf:
  - .proto 파일에 스키마 정의
  - 각 필드에 고유 번호 (field=1, field=2...)
  - 번호 기반 인코딩 → 필드명 변경해도 호환 유지

Thrift:
  - .thrift 파일에 데이터 + 서비스(RPC) 정의
  - 직렬화 + RPC 프레임워크 통합
  - Meta(Facebook) 오리지널
```

### Avro [[005_schema|스키마]] 예시

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

- **📢 섹션 요약 비유**: Avro [[005_schema|스키마]]는 택배 포장 명세서다. 포장 안에 무엇이 들어있는지([[005_schema|스키마]])를 별도 문서로 관리하고, 실제 택배 상자(바이너리 [[001_dikw_pyramid|데이터]])는 내용물만 담아 최소 크기로 보낸다.

---

## Ⅲ. 비교 및 연결

| 비교 | Avro | Protobuf | Thrift |
|:---|:---|:---|:---|
| [[005_schema|스키마]] 언어 | [[343_json|JSON]] (.avsc) | IDL (.proto) | IDL (.thrift) |
| [[005_schema|스키마]] 진화 | Excellent | Good | Good |
| [[074_byte|바이트]] 효율 | Good | Better | Good |
| [[179_kafka_flink_watermark_time_window|Kafka]] 통합 | Excellent | Good | Fair |
| [[479_grpc_protobuf_http2|gRPC]] 지원 | 없음 | Native | 없음 |
| 언어 지원 | [[489_raid_10_hybrid|10]]+ | 13+ | 28+ |

- **📢 섹션 요약 비유**: Avro는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]·[[179_kafka_flink_watermark_time_window|카프카]] 세계의 모국어, Protobuf는 구글 [[532_microservices_decomposition_patterns|마이크로서비스]]의 모국어, Thrift는 Meta [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]의 모국어다. 어느 세계에 사는지에 따라 가장 편한 언어가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[179_kafka_flink_watermark_time_window|Kafka]] + [[094_reinforcement_learning|Confluent]] [[505_schema|Schema]] [[235_registry_immutable_tag|Registry]] + Avro

```text
Producer → [Avro 직렬화] → Kafka 토픽
              ↑ 스키마 등록/조회
           Schema Registry
              ↓ 스키마 조회/역직렬화
Consumer ← [Avro 역직렬화] ← Kafka 토픽
```

### [[479_grpc_protobuf_http2|gRPC]] + Protobuf
- [[532_microservices_decomposition_patterns|마이크로서비스]] 간 고속 통신: [[461_http_stateless_connection_oriented|HTTP]]/2 + Protobuf 바이너리.
- .proto → 각 언어 클라이언트 자동 [[087_process_state_transition|생성]].
- 스트리밍 지원: [[008_단방향_반이중_전이중|단방향]]·양방향 스트리밍.

- **📢 섹션 요약 비유**: [[479_grpc_protobuf_http2|gRPC]]+Protobuf는 국제 은행 간 SWIFT 전문(電文) 시스템이다. 표준화된 형식(Protobuf)으로 빠르고 정확하게 정보를 전달하고, 수신 측은 자동으로 해석(역직렬화)한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **네트워크 효율** | [[343_json|JSON]] 대비 50~80% [[001_dikw_pyramid|데이터]] 크기 감소 |
| **처리 속도** | 바이너리 파싱으로 역직렬화 10배+ 향상 |
| **[[005_schema|스키마]] 관리** | [[505_schema|Schema]] Registry로 [[005_schema|스키마]] [[288_version_ihl_tos_total_length|버전]] 중앙 관리 |

[[190_ai_llm_requirements_specification|AI]]/ML [[123_pipe|파이프]]라인에서 대규모 Feature Store와 모델 서빙에 Protobuf·Avro가 표준 [[149_serial_communication_rs232_rs485|직렬]]화로 자리잡고 있으며, Apache Arrow의 컬럼형 인메모리 포맷이 분석 워크로드에서 새로운 [[149_serial_communication_rs232_rs485|직렬]]화 표준으로 부상하고 있다.

- **📢 섹션 요약 비유**: Apache Arrow는 [[148_5g_embb_urllc_mmtc|초고속]] [[149_serial_communication_rs232_rs485|직렬]]화의 미래다. 행 단위(Avro/Protobuf) 대신 열 단위로 [[001_dikw_pyramid|데이터]]를 정렬하여 CPU 캐시를 최적으로 활용 — 분석 [[298_qkv_attention|쿼리]]가 수십 배 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[505_schema|Schema]] [[235_registry_immutable_tag|Registry]]** | Avro [[005_schema|스키마]] 중앙 저장·[[288_version_ihl_tos_total_length|버전]] 관리 |
| **[[479_grpc_protobuf_http2|gRPC]]** | Protobuf 기반 고성능 [[126_rpc|RPC]] 프레임워크 |
| **[[179_kafka_flink_watermark_time_window|Kafka]]** | Avro/Protobuf [[149_serial_communication_rs232_rs485|직렬]]화의 주요 활용 시스템 |
| **Apache Arrow** | 컬럼형 인메모리 [[149_serial_communication_rs232_rs485|직렬]]화 차세대 표준 |
| **[[005_schema|스키마]] 진화** | [[001_dikw_pyramid|데이터]] 구조 변경 시 하위 [[344_compatibility_usability|호환성]] 유지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[JSON/XML — 텍스트 직렬화, 사람 가독성, 크기 비효율]
    │
    ▼
[Avro/Protobuf/Thrift — 바이너리 직렬화, 효율성]
    │
    ▼
[Schema Registry — 스키마 버전 중앙 관리]
    │
    ▼
[gRPC + Protobuf — 마이크로서비스 표준 RPC]
    │
    ▼
[Apache Arrow — 컬럼형 인메모리 분석 직렬화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[149_serial_communication_rs232_rs485|직렬]]화는 [[001_dikw_pyramid|데이터]]를 택배 상자에 포장하는 방법이에요! JSON은 큰 종이 박스, Avro/Protobuf는 진공 포장 — 훨씬 작고 빠르게 전달돼요!
2. Kafka에서는 Avro+[[505_schema|Schema]] Registry가 표준, [[532_microservices_decomposition_patterns|마이크로서비스]]에서는 Protobuf+gRPC가 표준이에요!
3. Apache Arrow는 분석 전용 [[148_5g_embb_urllc_mmtc|초고속]] 포장재예요 — 컬럼 단위로 정렬해서 수십 배 빠른 분석이 가능하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 49 / 262

← **이전**: [[048_hdfs_viewfs|26. HDFS ViewFS — Hadoop 연합 네임스페이스 통합 뷰]]
**다음**: [[050_hadoop_security_kerberos_ranger_atlas|28. Hadoop 보안 — Kerberos, Ranger, Atlas]] →

---
