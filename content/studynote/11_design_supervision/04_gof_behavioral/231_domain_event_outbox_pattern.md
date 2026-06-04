+++
title = "231. 도메인 이벤트 아웃박스 패턴 (Domain Event Outbox Pattern)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계 안에서 이벤트를 DB ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/)) 에 먼저 저장하고, 별도 프로세스가 비동기로 메시지 브로커에 발행하여 이중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Dual Write) 문제를 해결한다.
> 2. **가치**: 비즈니스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 커밋과 이벤트 발행이 원자적으로 동작하므로 메시지 유실·중복 없이 Eventually Consistent(최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))를 보장한다.
> 3. **판단 포인트**: 메시지 브로커가 다운돼도 DB ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/)) 에 이벤트가 남아 재발행이 가능하며, [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 간 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있는 통신의 표준 솔루션이다.

---

## Ⅰ. 개요 및 필요성
[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) A가 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 커밋한 뒤 이벤트를 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 같은 메시지 브로커에 발행해야 하는 상황이 매우 흔하다. 이때 전통적인 방식—비즈니스 로직 저장 -> 이벤트 발행—은 두 가지 위험을 내포한다.

1. **커밋 직후 브로커 발행 실패**: DB ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/)) 에는 저장됐지만 브로커에는 도달하지 못해 이벤트가 사라진다.
2. <strong>발행 성공 후 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a></strong>: 브로커에는 이벤트가 올라갔지만 비즈니스 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)돼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치가 발생한다.

[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트 아웃박스 패턴 ([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Event Outbox Pattern) 은 이 두 가지 문제를 근본적으로 차단한다. 핵심 아이디어는 <strong>이벤트 발행을 비즈니스 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>과 같은 DB (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/">Database</a>) <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a> 안에 포함시키는 것</strong>이다. 이벤트는 즉시 브로커로 가지 않고 `outbox` 테이블에 저장되며, 이후 릴레이(Relay) 프로세스나 [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) 가 이를 읽어 브로커에 전달한다.

| 방식 | [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) | 유실 위험 | 중복 발행 |
|:---|:---:|:---:|:---:|
| 직접 발행 ([Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) Publish) | ❌ | 높음 | 가능 |
| Outbox 패턴 | ✅ | 없음 | At-least-once (최소 1회) |
| [Saga](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga/) 패턴 단독 | 부분적 | 있음 | 가능 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 편지를 바로 우체통에 넣는 대신 먼저 수신함에 보관해 두고, 우편배달부가 정해진 시간에 가져가는 것과 같다. 편지(이벤트)는 절대 잃어버리지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+----------------------------------------------------------+
|                  Business Transaction                    |
|  +---------------+          +------------------------+   |
|  |  Domain Model | --저장--->|  Business Table (DB)   |   |
|  |  (비즈니스 객체)|          +------------------------+   |
|  |               | --저장--->+------------------------+   |
|  +---------------+          |  Outbox Table (DB)     |   |
|                             |  id / event_type       |   |
|                             |  payload / status      |   |
|                             +------------+-----------+   |
+------------------------------------------+---------------+
                                           | COMMIT 동시 반영
                     +---------------------v--------------+
                     |     Relay / CDC (Debezium 등)       |
                     |  미발행 row 폴링 or 변경 로그 캡처    |
                     +---------------------+--------------+
                                           | publish
                     +---------------------v--------------+
                     |     Message Broker (Kafka/RabbitMQ) |
                     +---------------------+--------------+
                                           | consume
                     +---------------------v--------------+
                     |         Consumer Service B          |
                     +------------------------------------+
```

```sql
CREATE TABLE outbox_events (
    id          UUID        PRIMARY KEY,
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id   VARCHAR(100) NOT NULL,
    event_type     VARCHAR(200) NOT NULL,
    payload        JSONB       NOT NULL,
    created_at     TIMESTAMP   NOT NULL DEFAULT NOW(),
    published_at   TIMESTAMP,
    status         VARCHAR(20) NOT NULL DEFAULT 'PENDING'
);
```

| 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) ([Polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) | 주기적으로 PENDING 행 조회 후 발행 | 구현 단순 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생, DB 부하 |
| [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) | Debezium 등으로 WAL (Write-Ahead Log) 변경 스트림 구독 | 실시간, DB 부하 최소 | 인프라 복잡도 증가 |

- **📢 섹션 요약 비유**: 우체국 직원이 수신함을 주기적으로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/))하거나, [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)([CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/))로 편지가 들어오는 순간 즉시 픽업하는 두 가지 방식의 차이다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 목적 | [원자성](/knowledge-base/studynote/05_database/04_transactions_concurrency/193_atomicity_all_or_nothing/) 보장 | 복잡도 |
|:---|:---|:---:|:---:|
| Outbox Pattern | 이벤트 발행 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) | ✅ DB [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | 중간 |
| [Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/) (Choreography) | [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 조율 | [보상 트랜잭션](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/) | 높음 |
| Transactional Messaging | MQ 내장 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | MQ 지원 시 ✅ | 낮음 |
| [Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/) | 상태를 이벤트 스트림으로 저장 | ✅ 이벤트가 원천 | 매우 높음 |

- **Outbox**: 송신 측에서 발행할 이벤트를 임시 저장
- **Inbox**: 수신 측에서 중복 수신을 방지하기 위한 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) 테이블 ([Idempotency](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/) Store)

두 패턴을 결합하면 [End-to-End](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/) (종단 간) 정확히 1번(Exactly-Once) 처리와 유사한 효과를 얻는다.

- **📢 섹션 요약 비유**: Outbox는 "보낼 편지함", Inbox는 "이미 받은 편지 목록"이다. 둘을 함께 쓰면 같은 편지를 두 번 처리하는 일이 없어진다.

---

## Ⅳ. 실무 적용 및 기술사 판단
1. <strong>주문 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>: `ORDER_CREATED` 이벤트를 재고 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 결제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있게 전달
2. <strong>결제 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>: `PAYMENT_COMPLETED` 이벤트가 유실되면 배송이 시작되지 않는 치명적 오류 -> Outbox 필수
3. <strong>알림 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>: 선택적 이벤트이지만, 비용·UX를 위해 Outbox로 At-least-once 보장

- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a> 처리</strong>: 릴레이가 같은 이벤트를 중복 발행할 수 있으므로 소비자 측에서 idempotent (멱등) 처리 필수
- **Outbox 테이블 정리**: 발행 완료된 행을 주기적으로 삭제하거나 아카이브하여 테이블 비대화 방지
- **모니터링**: PENDING 상태가 [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 이상 지속되면 릴레이 장애 알림 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)

기술사 시험에서 Outbox 패턴은 <strong>"MSA에서 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>을 어떻게 보장하는가"</strong> 라는 논제와 연결된다. [2PC](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/) ([Two-Phase Commit](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/549_2pc_two_phase_commit_limitations_msa/)) 대비 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 없이 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 달성하는 실용적 해법으로 평가받는다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 해결하려는 변화 축이 분명한가?
2. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용보다 변경 절감 효과가 큰가?
3. 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 중요한 계약서를 FedEx로 보내기 전에 복사본을 사무실 서랍에 넣어두는 것과 같다. 택배가 분실돼도 재발송할 수 있다.

---

## Ⅴ. 기대효과 및 결론
Outbox 패턴 도입의 정량적 효과:

- 이벤트 유실률 -> **0%** (DB [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/))
- 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 단축 -> 릴레이 재시작만으로 미발행 이벤트 자동 재처리
- 브로커 일시 다운 -> [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 운영에 영향 없음 (Outbox에 누적 후 발행)

[MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 특성상 네트워크 장애, 브로커 재시작, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재배포는 피할 수 없다. Outbox 패턴은 이러한 <strong>불확실성을 DB <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>이라는 확실성으로 흡수</strong>하는 설계 전략이다. [Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/) ([이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)) 과 결합하면 시스템 전체의 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([Audit Trail](/knowledge-base/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/))까지 완성된다.

확장 방향은 ① 선언형 API와의 결합, ② [관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) 내장, ③ [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 인터넷이 끊겨도 로컬 드래프트에 저장된 이메일은 연결이 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)되면 자동으로 발송된다. Outbox는 그 드래프트 폴더다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) | Outbox 패턴이 필요한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경 |
| 상위 개념 | Eventually Consistent (최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | Outbox가 달성하는 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델 |
| 하위 개념 | [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) ([Change Data Capture](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/)) | Outbox 릴레이의 실시간 구현체 |
| 하위 개념 | Idempotent Consumer (멱등 소비자) | Outbox의 중복 발행을 수신 측에서 처리 |
| 연관 개념 | [Saga Pattern](/knowledge-base/studynote/12_it_management/05_security_compliance/305_saga_pattern/) | [분산 트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/) 조율에 Outbox와 함께 사용 |
| 연관 개념 | [Event Sourcing](/knowledge-base/studynote/12_it_management/05_security_compliance/307_event_sourcing/) ([이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)) | 이벤트를 원천 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 사용하는 심화 패턴 |

### 📈 관련 키워드 및 발전 흐름도
[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트 -> [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이벤트 아웃박스 패턴 -> [CDC](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 기반 통합

### 👶 어린이를 위한 3줄 비유 설명
1. 엄마한테 쪽지를 보내고 싶을 때, 먼저 수첩에 쪽지를 적어 두는 거야.
2. 집배원 아저씨가 수첩을 보고 쪽지를 가져가서 엄마한테 전달해 줘.
3. 수첩에 적어뒀으니까 집배원이 잠깐 자리를 비워도 쪽지는 절대 안 없어져!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 292 / 530

<- **이전**: [230. 모듈형 모놀리스 (Modular Monolith)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/230_modular_monolith/)
**다음**: [232. MVP/MVVM 데이터 바인딩 (MVP/MVVM Data Binding)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/232_mvp_mvvm_data_binding/) ->

---
