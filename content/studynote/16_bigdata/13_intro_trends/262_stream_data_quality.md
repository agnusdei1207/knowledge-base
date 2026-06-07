---
title: "Streaming Data Quality Management"
date: "2025-01-01"
tags:
  - "Great Expectations"
  - "Kafka"
  - "anomaly detection"
  - "data quality"
  - "data validation"
  - "real-time"
  - "schema registry"
  - "streaming data quality"
  - "studynote-bigdata"
weight: 262
---
> **핵심 인사이트 3줄**
> 1. 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리는 배치와 달리 실시간으로 유입되는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 오류를 즉시 탐지·처리해야 하며, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(late [data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))와 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변화가 핵심 과제다.
> 2. [Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) + Avro/Protobuf를 통한 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리가 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반 스트림의 품질 첫 번째 방어선이며, 생산자-소비자 간 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 자동 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
> 3. 인라인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(Great Expectations, Apache Griffin), 이상값 탐지(통계적/ML 기반), 데드 레터 큐(DLQ)가 스트리밍 품질 관리의 3단 방어 체계를 구성한다.

---

## Ⅰ. 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 개요

### 1.1 배치 vs 스트리밍 품질 관리 차이

| 항목          | 배치 품질 관리          | 스트리밍 품질 관리          |
|-------------|----------------------|--------------------------|
| 처리 시점     | 적재 후 일괄 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)       | 실시간 인라인 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)          |
| 오류 처리     | 재실행 가능             | 즉시 격리·알림 필요         |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)   | 문제 없음               | [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)·윈도우 처리 필요   |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변화   | 배치 시 감지             | 실시간 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)   |

### 1.2 주요 품질 이슈

```
[데이터 소스] -> Kafka -> [소비자]
      v 발생 가능한 품질 이슈:
  - 스키마 불일치: 필드 추가/제거/타입 변경
  - 누락값: 필수 필드 null
  - 범위 위반: 음수 금액, 미래 타임스탬프
  - 중복 이벤트: 네트워크 재전송으로 중복 메시지
  - 지연 도착: 이벤트 시간 vs 처리 시간 불일치
```

📢 **섹션 요약 비유**: 배치 품질 관리는 날 마감 후 재고 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 스트리밍은 계산대에서 물건 바코드가 찍힐 때마다 즉시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/).

---

## Ⅱ. [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)

### 2.1 [Confluent](/studynote/12_it_management/02_itsm_itil/878_reinforcement_learning/) [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)

```
생산자                    스키마 레지스트리        소비자
  |                            |                    |
  +-[스키마 등록/확인]------->  |                    |
  |                            |                    |
  +-[메시지 직렬화(Avro)]---> Kafka --->[스키마 확인]-->|
                                                     |
                                               [역직렬화]
```

### 2.2 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 모드

| 모드                | 의미                                   |
|-------------------|----------------------------------------|
| BACKWARD (기본)    | 새 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)로 이전 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기 가능       |
| [FORWARD](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)           | 이전 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)로 새 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기 가능       |
| FULL              | 양방향 호환                            |
| NONE              | [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 검사 없음                       |

```json
{
  "type": "record", "name": "Order",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "ts", "type": "long"}
  ]
}
```

📢 **섹션 요약 비유**: [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 계약서 공증 — 생산자와 소비자가 같은 양식([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/))을 쓰도록 중간에서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해준다.

---

## Ⅲ. 인라인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

### 3.1 Flink DataStream 내 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

```python
def validate_event(event):
    errors = []
    if event['amount'] < 0:
        errors.append('negative_amount')
    if event['user_id'] is None:
        errors.append('null_user_id')
    if event['timestamp'] > time.time() + 60:
        errors.append('future_timestamp')
    return errors

stream.map(validate_event) \
      .filter(lambda e: len(e) > 0) \
      .sink_to(dead_letter_queue)
```

### 3.2 Great Expectations Streaming

```python
import great_expectations as gx

context = gx.get_context()
validator = context.get_validator(batch_request=streaming_batch)
validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_between("amount", 0, 1_000_000)
results = validator.validate()
```

📢 **섹션 요약 비유**: 인라인 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 공장 컨베이어 벨트의 품질 검사 카메라 — 불량품이 나오면 즉시 옆으로 빼낸다.

---

## Ⅳ. 데드 레터 큐 (DLQ)와 재처리

### 4.1 DLQ 아키텍처

```
메인 토픽 (orders)
      v
[소비자 + 검증]
      +- 유효 이벤트 -> 처리 파이프라인 진행
      +- 오류 이벤트 -> DLQ (orders.dlq)
                            v
                     [알림/모니터링]
                            v
                     [수동 검토/재처리]
```

### 4.2 DLQ [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 구조

```json
{
  "original_topic": "orders",
  "original_partition": 3,
  "original_offset": 12345,
  "error_code": "SCHEMA_MISMATCH",
  "error_message": "Field 'amount' expected DOUBLE got STRING",
  "timestamp": "2024-01-15T10:30:00Z",
  "original_payload": "..."
}
```

📢 **섹션 요약 비유**: DLQ는 불량품 보관함 — 즉시 폐기하지 않고 모아뒀다가 나중에 원인 분석 후 재처리하거나 버린다.

---

## Ⅴ. [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/))

### 5.1 통계 기반 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)

3σ 규칙: |값 - 평균| > 3 × 표준편차 -> 이상값

```python
from collections import deque

window = deque(maxlen=100)

def detect_anomaly(value):
    if len(window) >= 30:
        mean = sum(window) / len(window)
        std = (sum((x-mean)**2 for x in window)/len(window))**0.5
        if abs(value - mean) > 3 * std:
            return True
    window.append(value)
    return False
```

### 5.2 ML 기반 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)

- <strong><a href="/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">Isolation</a> Forest</strong>: 이상값은 적은 분기 수로 고립됨
- <strong><a href="/studynote/10_ai/04_ai_ops_ethics/292_lstm/">LSTM</a> <a href="/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/">Autoencoder</a></strong>: 시계열 재구성 오류로 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)
- **Prophet + 신뢰구간**: 예측 범위 벗어나면 이상

📢 **섹션 요약 비유**: [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 심박수 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/) — 정상 범위(3σ)를 벗어나면 즉시 경보를 울려 빠른 대응을 가능하게 한다.

---

## 📌 관련 개념 맵

```
스트리밍 데이터 품질
+-- 1단: 스키마 검증
|   +-- Schema Registry (Avro/Protobuf)
|   +-- 호환성 모드 (BACKWARD/FORWARD)
+-- 2단: 인라인 검증
|   +-- Great Expectations Streaming
|   +-- Flink/Spark 내 커스텀 검증
+-- 3단: 이상 탐지
|   +-- 통계 기반 (3σ, Z-score)
|   +-- ML 기반 (Isolation Forest, LSTM)
+-- 오류 처리
    +-- 데드 레터 큐 (DLQ)
    +-- 알림 + 재처리 흐름
```

---

## 📈 관련 키워드 및 발전 흐름도

```
배치 ETL 품질 관리 (SQL 검증, Great Expectations)
     |  스트리밍 데이터 증가
     v
Kafka + Schema Registry 도입 (2014~)
     |  실시간 검증 필요
     v
스트리밍 인라인 검증 (Flink/Spark + DLQ)
     |  ML 기반 이상 탐지
     v
지능형 스트리밍 DQ (Anomaly Detection + Auto-Remediation)
     |  DataOps + 스트리밍 통합
     v
실시간 데이터 옵저버빌리티 플랫폼 (현재~)
```

**핵심 키워드**: [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), Avro, DLQ, Great Expectations, [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/), 인라인 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

---

## 👶 어린이를 위한 3줄 비유 설명

1. 스트리밍 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리는 컨베이어 벨트 검사 — 물건이 흘러올 때마다 즉시 불량을 걸러내야 해.
2. [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 계약서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 창구 — 보내는 사람과 받는 사람이 같은 양식을 쓰는지 중간에서 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해줘.
3. DLQ는 불량품 보관함 — 이상한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바로 버리지 않고 모아뒀다가 나중에 고쳐서 다시 쓸 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 262 / 262

<- **이전**: [049. 지식 그래프 — Knowledge Graph](/studynote/16_bigdata/13_intro_trends/261_knowledge_graph/)

✅ **마지막 글입니다.**

---
