---
title: "155. 이벤트 트리거 기반 실행 (Event Trigger Serverless)"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 함수는 특정 이벤트([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드, 메시지 큐 알람, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 요청, [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 등)가 발생할 때만 자동 실행되며, 이벤트 소스 매핑 (Event Source [Mapping](/studynote/05_database/01_db_architecture_relational/010_schema_mapping/))이 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)와 함수를 연결한다.
> 2. **가치**: 이벤트 기반 자동화 망을 구성하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 명시적 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 없이 느슨하게 결합된 비동기 처리 파이프라인을 구축할 수 있다.
> 3. **판단 포인트**: 동기([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 직접 응답이 필요)와 비동기(SQS/SNS/Pub/Sub 경유) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)를 구분해 설계해야 재시도 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·DLQ (Dead Letter [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 처리 방식이 달라진다.

---

## Ⅰ. 개요 및 필요성

이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) (Event Trigger)는 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처의 실행 패러다임이다. 기존의 "서버가 항상 실행 중인" 모델과 달리, [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 "이벤트가 일어날 때만 실행"된다. S3에 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 업로드되면 썸네일 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) Lambda가 실행되고, SQS 큐에 메시지가 쌓이면 처리 Lambda가 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행되는 식이다.

이 이벤트 중심 실행 모델은 [EDA](/studynote/12_it_management/02_itsm_itil/064_eda/) ([Event-Driven Architecture](/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/))의 자연스러운 구현체이다. 이벤트 발생자(Producer)와 이벤트 처리자(Consumer)가 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)를 통해 완전히 분리되므로, 각 컴포넌트는 독립적으로 확장·배포된다.

이벤트 소스 매핑 (Event Source [Mapping](/studynote/05_database/01_db_architecture_relational/010_schema_mapping/))은 이벤트 소스(S3, SQS, [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Streams, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 등)와 [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 함수를 연결하는 설정이다. [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 방식(SQS, Kinesis)과 푸시 방식(S3, SNS, [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/))으로 나뉘며, 각각 재시도·배치 크기 설정이 다르다.

📢 **섹션 요약 비유**: 이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 자동 센서 조명 — 사람이 지나갈 때(이벤트)만 불이 켜지고, 아무도 없으면 꺼진다. 스위치를 직접 누를([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출) 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 유형 | 이벤트 소스 예시 | 실행 방식 | 재시도 기본값 |
|:---|:---|:---|:---|
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/동기 | [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/), Function URL | 직접 호출·즉시 응답 | 없음 (클라이언트 재시도) |
| 스토리지 이벤트 | S3 ObjectCreated, Cloud Storage | 푸시 (비동기) | 3회 |
| 메시지 큐 | SQS, [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Bus](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), Cloud Tasks | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) (배치) | DLQ까지 |
| 스트리밍 | Kinesis, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), Pub/Sub | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) (순서 보장) | 재시도 후 bisect |
| [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) | EventBridge [Cron](/studynote/15_devops_sre/02_cicd_gitops/107_nightly_build_scheduled_cron_pipeline/), Cloud Scheduler | 푸시 (주기적) | 2회 |
| DB 변경 스트림 | [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Streams, Firestore | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) | 재시도 후 DLQ |

```text
+----------------------------------------------------------------------+
|                  이벤트 트리거 실행 아키텍처                         |
|                                                                      |
|  이벤트 소스               이벤트 버스/큐           Lambda 함수      |
|                                                                      |
|  [S3 업로드]  --push--►  [S3 이벤트 알림]  --►  [이미지 변환 fn]   |
|                                                                      |
|  [HTTP 요청]  --push--►  [API Gateway]     --►  [API 처리 fn]      |
|                                                                      |
|  [메시지 발행]--push--►  [SQS 큐]          --►  [메시지 처리 fn]   |
|                               | (폴링)           ^ 배치 처리        |
|                               +-----------------►| (최대 10,000건)  |
|                                                                      |
|  [크론 스케줄]--push--►  [EventBridge]     --►  [배치 집계 fn]     |
|                                                                      |
|  [DDB 변경]   --poll--►  [DDB Streams]     --►  [CDC 처리 fn]     |
|                                                   v 실패 시         |
|                                              [DLQ (SQS)]            |
+----------------------------------------------------------------------+
```

📢 **섹션 요약 비유**: 이벤트 소스 매핑은 회사 콜센터 배차 시스템 — 전화(이벤트)가 오면 자동으로 적합한 상담원([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/))에게 연결하고, 실패하면 DLQ(메모지)에 남긴다.

---

## Ⅲ. 비교 및 연결

| 구분 | 동기 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) (Sync) | 비동기 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) (Async) |
|:---|:---|:---|
| 응답 방식 | 처리 완료 후 즉시 응답 | 수신 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 백그라운드 처리 |
| 재시도 | 클라이언트 책임 | 플랫폼 자동 재시도 + DLQ |
| 오류 처리 | 오류 즉시 클라이언트 전달 | DLQ로 실패 이벤트 보관 |
| 사용 예 | [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 응답, 조회 | 이미지 처리, 이메일 발송 |
| [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 영향 | 즉각적 UX 영향 | 배경 처리, UX 영향 낮음 |

DLQ (Dead Letter [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 패턴:
- 재시도 횟수 초과 또는 처리 실패 이벤트를 별도 SQS 큐에 보관.
- 운영자가 DLQ 메시지를 분석 후 수동 재처리 또는 폐기.
- DLQ 모니터링 알람 설정이 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 운영의 필수 요소.

📢 **섹션 요약 비유**: DLQ는 편지 반송함 — 배달이 안 된 편지(실패 이벤트)를 버리지 않고 반송함에 모아두었다가 나중에 다시 처리한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**이벤트 기반 이미지 처리 파이프라인 예시**
1. 사용자가 S3에 원본 이미지 업로드
2. S3 ObjectCreated 이벤트 -> [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)
3. [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/): 이미지 리사이즈 -> 썸네일 S3 저장 -> SQS 메시지 발행
4. SQS -> [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/): DB [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 업데이트
5. [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Streams -> [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/): [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) (Content Delivery Network) 캐시 무효화

<strong><a href="/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a> (<a href="/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/">Idempotency</a>) 보장 설계</strong>
- 비동기 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 "최소 1회(At-Least-Once)" 실행 보장 -> 중복 호출 가능
- 처리 함수에 이벤트 ID 기반 중복 체크 로직 필수
- DynamoDB의 ConditionalExpression으로 멱등 처리 구현

📢 **섹션 요약 비유**: [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)은 엘리베이터 버튼 — 이미 눌려 있어도 한 번 더 눌러도 엘리베이터는 한 번만 온다. 이벤트가 중복 발행되어도 결과가 같아야 한다.

---

## Ⅴ. 기대효과 및 결론

이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반 실행은 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 느슨한 결합, 자동 확장, 운영 효율화를 동시에 달성하는 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처의 핵심 패턴이다. 배치·실시간 처리·알림·[데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 등 다양한 워크로드에서 운영 오버헤드를 최소화하면서 높은 처리량을 실현한다.

주의할 점은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트 처리 특성상 실패 추적·디버깅·순서 보장이 어려워진다는 것이다. [분산 추적](/studynote/04_software_engineering/09_cloud_native_ai_architecture/569_distributed_tracing_opentelemetry_jaeger/)(AWS X-Ray, [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/)), DLQ, 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)(EventBridge [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/))를 함께 도입해 관찰 가능성([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/))을 확보해야 한다.

📢 **섹션 요약 비유**: 이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 아키텍처는 자동화된 공장 라인 — 각 공정([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/))이 이전 공정의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)(이벤트)를 받아 자동으로 실행되며, 문제가 생기면 불량품 보관함(DLQ)에 담긴다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [EDA](/studynote/12_it_management/02_itsm_itil/064_eda/) ([Event-Driven Architecture](/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/)) | 이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)의 상위 아키텍처 패턴 |
| DLQ (Dead Letter [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | 실패 이벤트 보관 및 재처리 |
| [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 중복 이벤트에도 결과 동일 보장 |
| SQS / Pub/Sub | 비동기 이벤트 전달 매개체 |
| EventBridge | AWS의 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/), [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 및 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 통합 |
| [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/) Streams | DB 변경 이벤트 스트림으로 [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/) 구현 |

### 👶 어린이를 위한 3줄 비유 설명
1. 이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 학교 종소리 — 종이 울리면(이벤트) 학생들이 자동으로 교실로 이동해요([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 실행).

### 📈 관련 키워드 및 발전 흐름도

```text
폴링 (주기적 확인, 비효율)
    |
    v
이벤트 트리거: S3 · API Gateway · SQS · CloudWatch
    |
    v
이벤트 소싱 + CQRS -> 이벤트 기반 아키텍처 (EDA)
```
2. 종소리마다 다른 행동이 연결되어 있어요 — 아침 종([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요청), 점심 종([스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)), 화재경보(S3 업로드).
3. 선생님(개발자)은 어떤 종에 어떤 행동을 연결할지 규칙만 만들면, 이후엔 자동으로 돌아가요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 154 / 371

<- **이전**: [154. 서버리스 상태 비저장 제약 (Stateless Serverless) - 무한 스케일 아웃의 물리적 댓가](/studynote/13_cloud_architecture/03_msa_serverless/154_stateless_serverless_external_storage/)
**다음**: [156. 서버리스 벤더 락인과 Knative (Vendor Lock-in / Knative)](/studynote/13_cloud_architecture/03_msa_serverless/156_serverless_vendor_lockin_knative/) ->

---
