---
title: "Transactional Outbox Pattern"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transactional Outbox는 <strong>비즈니스 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>와 이벤트를 같은 DB 트랜잭션으로 저장(Outbox 테이블)</strong>한 후, 별도 프로세스([CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)·[Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))가 Outbox에서 이벤트를 읽어 메시지 브로커로 발행하는 패턴이다.
> 2. **가치**: "주문 저장 + [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 발행"을 별도로 하면 <strong>DB 저장 성공·<a href="/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a> 발행 실패</strong> 시 불일치가 발생하지만, Outbox는 <strong>단일 트랜잭션으로 <a href="/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/">원자성</a>을 보장</strong>한다.
> 3. **판단 포인트**: Debezium([CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 기반)이 Outbox 이벤트를 실시간 캡처하여 Kafka로 전달하는 것이 표준 구현이며, [Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) 방식은 지연이 있다.

---

## Ⅰ. 개요 및 필요성

```text
1. 비즈니스 로직: INSERT orders + INSERT outbox (같은 트랜잭션)
2. CDC (Debezium): outbox 테이블 변경 감지 -> Kafka 발행
3. 소비자: Kafka에서 이벤트 소비
-> DB 트랜잭션 = 이벤트 발행 원자성 보장
```

- **📢 섹션 요약 비유**: Outbox는 **보내야 할 편지를 우편함(Outbox)에 넣으면 우체부(Debezium)가 가져가는** 것이다.

---

## Ⅱ~Ⅴ. 결론

Transactional Outbox는 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 이벤트 발행의 <a href="/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/">원자성</a> 보장 표준 패턴</strong>이며, Debezium+Kafka가 핵심 구현이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Outbox** | 이벤트 [원자성](/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 보장 |
| <strong><a href="/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/">CDC</a></strong> | [변경 데이터 캡처](/studynote/12_it_management/05_security_compliance/218_cdc_change_data_capture/) |
| **Debezium** | [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |
| <strong><a href="/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a></strong> | 이벤트 브로커 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/305_saga/">Saga</a></strong> | Outbox와 함께 사용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[직접 Kafka 발행 (문제: 불일치)]
    -> [Outbox 패턴 (2016~)]
    -> [Debezium CDC (2017~)]
    -> [현재: Outbox + Saga + CQRS — 통합 패턴]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Outbox는 **보내야 할 편지를 우편함에 넣는** 거예요.
2. 편지와 일기(비즈니스 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 <strong>동시에 저장</strong>해서 빠뜨리지 않아요.
3. 우체부(Debezium)가 우편함을 확인하고 <strong>확실히 배달</strong>해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 136 / 371

<- **이전**: [136. Orchestration Saga - 중앙 오케스트레이터 기반 분산 트랜잭션](/studynote/13_cloud_architecture/03_msa_serverless/136_orchestration_saga/)
**다음**: [138. Event Sourcing (MSA) - 상태 대신 이벤트를 저장](/studynote/13_cloud_architecture/03_msa_serverless/138_event_sourcing_msa/) ->

---
