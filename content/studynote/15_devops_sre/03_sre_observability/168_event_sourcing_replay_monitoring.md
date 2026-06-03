---
title: 168. 이벤트 소싱 상태 복구 모니터링 (Event Sourcing Replay Monitoring)
date: '2026-04-21'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 상태 [[658_ir_recovery|복구]] [[229_monitor|모니터]]링 ([[307_event_sourcing|Event Sourcing]] Replay Monitoring)은 이벤트 [[568_logs_distributed_logging_elk_fluentd|로그]]를 다시 재생해 프로젝션 (Projection)이나 집계 상태를 [[658_ir_recovery|복구]]할 때, [[216_progress_in_synchronization|진행]]률·처리 속도·정합성 오류·예상 완료 시간까지 관측하는 운영 기법이다.
> 2. **가치**: [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) 시스템의 [[451_mttr|MTTR]] (Mean Time To [[658_ir_recovery|Recovery]])은 단순 프로세스 재시작이 아니라 "얼마나 빨리, 정확하게 리플레이를 끝내는가"에 좌우되므로, 리플레이 관측성은 [[658_ir_recovery|복구]] 계획과 [[090_service_kubernetes_network_load_balancing|서비스]] 복귀 판단의 핵심이 된다.
> 3. **판단 포인트**: 좋은 리플레이 [[229_monitor|모니터]]링은 속도만 보지 않는다. 이벤트 순서 누락, 중복 적용, [[022_snapshot_backup_architecture|스냅샷]] 시점, 프로젝션 [[015_지연_데이터_관점|지연]], 최종 정합성 [[395_verification_process_review|검증]]까지 함께 봐야 실제로 안전한 [[658_ir_recovery|복구]]라고 말할 수 있다.

---

## Ⅰ. 개요 및 필요성

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]은 [[178_as_is_to_be_analysis|현재 상태]]를 테이블 한 줄에 직접 저장하기보다, 상태 변화를 만든 이벤트들의 순서를 원본으로 보관하는 방식이다. 따라서 읽기 모델이 깨지거나 새 프로젝션을 만들어야 할 때는 과거 이벤트를 다시 재생해 상태를 [[658_ir_recovery|복구]]한다. 이때 리플레이가 잘 [[216_progress_in_synchronization|진행]]되는지, 언제 끝나는지, 중간에 정합성 오류가 발생하지는 않는지를 보는 것이 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 상태 [[658_ir_recovery|복구]] [[229_monitor|모니터]]링이다.

이 관측이 중요한 이유는 리플레이가 종종 [[658_ir_recovery|복구]] 시간의 대부분을 차지하기 때문이다. 일반 CRUD (Create, Read, Update, Delete) 시스템은 [[002_database_definition|데이터베이스]]를 복원하면 빠르게 [[090_service_kubernetes_network_load_balancing|서비스]]가 돌아오지만, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 시스템은 이벤트 수가 수천만~수억 건이면 읽기 모델 재생성에 수십 분에서 수시간이 걸릴 수 있다. 운영자는 "지금 40% [[216_progress_in_synchronization|진행]] 중인지, 멈춘 것인지, 10분 뒤 [[658_ir_recovery|복구]] 가능한지"를 알아야 장애 소통과 우회 [[268_strategy_pattern|전략]]을 판단할 수 있다.

아래 그림은 왜 리플레이 자체가 별도 [[229_monitor|모니터]]링 대상인지 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│         이벤트 소싱 복구에서 관찰해야 하는 대상             │
├──────────────────────────────────────────────────────────────┤
│ Event Log ──▶ Replay Worker ──▶ Projection DB               │
│                                                              │
│ 질문 1: 몇 % 진행됐는가?                                      │
│ 질문 2: 초당 몇 건 처리 중인가?                               │
│ 질문 3: 누락·중복·버전 오류는 없는가?                         │
│ 질문 4: 언제 읽기 서비스를 다시 열 수 있는가?                 │
└──────────────────────────────────────────────────────────────┘
```

결국 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] [[658_ir_recovery|복구]]는 "다시 읽어 보면 되지" 수준의 단순 작업이 아니다. 대규모 시스템에서는 리플레이가 하나의 장기 배치 작업이 되므로, 일반 배치 [[229_monitor|모니터]]링과 [[064_relation_domain|도메인]] 정합성 [[395_verification_process_review|검증]]을 함께 갖춘 운영 체계가 필요하다.

- **📢 섹션 요약 비유**: 사건 기록이 가득한 일기장을 처음부터 다시 읽어 오늘 상태를 정리하는 과정이 리플레이다. 일기가 수십 권이면 몇 권째 읽고 있는지, 읽다가 [[286_page_frame|페이지]]가 빠지진 않았는지, 언제 다 읽을지 꼭 알아야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

리플레이 [[229_monitor|모니터]]링 구조는 보통 이벤트 스토어, 리플레이 워커, [[022_snapshot_backup_architecture|스냅샷]] 저장소, 프로젝션 [[002_database_definition|데이터베이스]], 그리고 관측 계층으로 나뉜다. 이벤트 스토어는 재생 원본을 제공하고, 리플레이 워커는 특정 오프셋이나 [[022_snapshot_backup_architecture|스냅샷]] 이후부터 이벤트를 적용한다. 관측 계층은 [[139_throughput|처리량]], 남은 이벤트 수, [[015_지연_데이터_관점|지연]], 오류, 최종 [[395_verification_process_review|검증]] 결과를 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 [[568_logs_distributed_logging_elk_fluentd|로그]]로 수집한다.

특히 리플레이 작업은 "얼마나 빨리"와 "얼마나 정확히"라는 두 축을 동시에 관리해야 한다. 속도만 빠르고 순서 보장이 깨지면 [[658_ir_recovery|복구]] 의미가 없고, 정확도만 강조하다 처리 속도가 너무 느리면 [[658_ir_recovery|복구]] 시간이 [[090_service_kubernetes_network_load_balancing|서비스]] 목표를 초과한다. 그래서 [[216_progress_in_synchronization|진행]]률, ETA (Estimated Time of Arrival), 이벤트 갭, 중복 적용, 핸들러 실패 수를 함께 봐야 한다.

```text
┌──────────────────────────────────────────────────────────────┐
│                리플레이 모니터링 아키텍처                    │
├──────────────────────────────────────────────────────────────┤
│ Event Store                                                  │
│    │                                                         │
│    ▼                                                         │
│ Snapshot Loader ──▶ Replay Worker ──▶ Projection DB          │
│                         │                 │                   │
│                         │                 └─ 정합성 체크      │
│                         │                                     │
│                         ├─ progress_total                     │
│                         ├─ replay_rate_per_sec                │
│                         ├─ replay_errors_total                │
│                         ├─ sequence_gap_total                 │
│                         └─ eta_seconds                        │
│                                      │                        │
│                                      ▼                        │
│                              Dashboard / Alerting             │
└──────────────────────────────────────────────────────────────┘
```

| 핵심 지표 | 의미 | 운영 판단 예시 |
| :--- | :--- | :--- |
| `replay_progress_percent` | 전체 이벤트 대비 현재 적용 비율 | 95% 이상이면 전환 준비 시작 |
| `replay_rate_per_sec` | 초당 처리 이벤트 수 | 평시 대비 50% 이하로 떨어지면 병목 점검 |
| `replay_eta_seconds` | 예상 남은 [[658_ir_recovery|복구]] 시간 | [[173_stakeholder_identification_impact_matrix|이해관계자]] 공지와 배포 창 재조정 |
| `replay_errors_total` | 핸들러 실패, 역직렬화 실패 건수 | 0이 아니면 수동 판정 필요 |
| `sequence_gap_total` | 누락된 이벤트 번호 수 | 1건이라도 있으면 정합성 위험 |
| `projection_lag_events` | 최신 이벤트와 프로젝션 간 차이 | 리플레이 종료 후 0으로 수렴해야 함 |

정량 계산도 중요하다. 예를 들어 총 이벤트가 5억 건이고 마지막 [[022_snapshot_backup_architecture|스냅샷]] 이후 2천만 건을 초당 25,000건으로 처리한다면, 순수 처리 ETA는 약 800초가 된다. 그러나 실제 운영에서는 역직렬화, 디스크 I/O, [[275_lock_contention_monitoring|락 경합]], 투영 [[289_cqrs_db|쓰기]] 비용이 들어가므로, 이동 평균 기반 ETA와 병목 지표를 함께 봐야 좀 더 현실적인 [[658_ir_recovery|복구]] 시간을 예측할 수 있다.

- **📢 섹션 요약 비유**: 리플레이 [[229_monitor|모니터]]링은 마라톤 중계와 같다. 현재 몇 km를 달렸는지, 분당 속도가 어떤지, 중간에 넘어졌는지, 결승선까지 얼마나 남았는지를 함께 봐야 완주 가능성을 알 수 있다.

---

## Ⅲ. 비교 및 연결

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 리플레이 [[229_monitor|모니터]]링은 일반 [[002_database_definition|데이터베이스]] 복원 [[229_monitor|모니터]]링과 닮았지만 관찰 초점이 다르다. [[002_database_definition|데이터베이스]] 복원은 [[555_backup_and_restore_strategy|백업]] 복사 속도, [[568_logs_distributed_logging_elk_fluentd|로그]] 적용 속도, [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]]이 핵심인 반면, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]은 [[064_relation_domain|도메인]] 이벤트 순서와 프로젝션 정합성이 더 중요하다. 즉 단순 I/O [[216_progress_in_synchronization|진행]]률만으로는 충분하지 않고, 이벤트 핸들러가 비즈니스 규칙을 올바르게 재적용했는지까지 [[396_validation|확인]]해야 한다.

| 항목 | DB 복원 [[229_monitor|모니터]]링 | [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 리플레이 [[229_monitor|모니터]]링 |
| :--- | :--- | :--- |
| [[658_ir_recovery|복구]] 단위 | [[286_page_frame|페이지]], [[501_file_definition_logical_record|파일]], [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]] | [[064_relation_domain|도메인]] 이벤트, 프로젝션 |
| 주요 지표 | 복원 속도, [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]], I/O | [[216_progress_in_synchronization|진행]]률, ETA, 이벤트 갭, 프로젝션 [[015_지연_데이터_관점|지연]] |
| 핵심 위험 | 스토리지 병목, [[568_logs_distributed_logging_elk_fluentd|로그]] 누락 | 순서 오류, 중복 적용, 핸들러 불일치 |
| [[658_ir_recovery|복구]] 완료 판단 | DB 오픈 가능 여부 | 정합성 [[395_verification_process_review|검증]] + 최신 오프셋 도달 |

또한 평시의 컨슈머 랙 ([[089_consumer_lag|Consumer Lag]]) [[229_monitor|모니터]]링과도 구분해야 한다. 컨슈머 랙은 라이브 소비가 생산자를 얼마나 따라가는지를 보는 지표이고, 리플레이 [[229_monitor|모니터]]링은 과거 전체 또는 일부 이벤트를 의도적으로 다시 읽는 [[658_ir_recovery|복구]] 작업의 관찰이다. 둘은 모두 "뒤처짐"을 보지만, 하나는 운영 [[019_처리_지연|처리 지연]]이고 다른 하나는 [[658_ir_recovery|복구]] [[216_progress_in_synchronization|진행]]률이라는 점이 다르다.

이 주제는 [[306_cqrs|CQRS]] ([[250_cqrs_command_query_responsibility_segregation_pattern|Command Query Responsibility Segregation]]), [[022_snapshot_backup_architecture|스냅샷]] [[268_strategy_pattern|전략]], [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]), 체크포인트 설계와 강하게 연결된다. [[022_snapshot_backup_architecture|스냅샷]]이 잘 설계되면 리플레이 시작점을 뒤로 당겨 MTTR을 줄일 수 있고, [[171_idempotency_iac_terraform|멱등성]]이 보장되면 재시도 중복 적용 위험을 낮출 수 있다. 즉 리플레이 [[229_monitor|모니터]]링은 관측성 주제이면서 동시에 아키텍처 품질을 드러내는 지표이기도 하다.

- **📢 섹션 요약 비유**: 일반 DB 복원이 창고 상자를 원래 자리에 다시 옮기는 일이라면, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 리플레이는 배송 기록을 순서대로 다시 읽으며 창고 상태를 재구성하는 일에 가깝다. 둘 다 [[658_ir_recovery|복구]]지만 [[396_validation|확인]]해야 할 포인트가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 리플레이 [[229_monitor|모니터]]링을 "배치 작업 상태판" 수준으로 끝내면 부족하다. 예를 들어 주문 [[090_service_kubernetes_network_load_balancing|서비스]]가 3년치 4억 건 이벤트를 보유하고 있고, 새 읽기 모델을 블루-그린 방식으로 재구축한다고 하자. 이때 운영팀은 [[022_snapshot_backup_architecture|스냅샷]] 시점, 남은 이벤트 수, 분당 [[139_throughput|처리량]], 오류 이벤트 목록, 프로젝션 샘플 [[395_verification_process_review|검증]] 결과를 대시보드에서 한 번에 봐야 하며, `progress=100%`라도 샘플 정합성 [[395_verification_process_review|검증]]이 끝나기 전에는 트래픽을 전환하면 안 된다.

또한 알림 기준이 중요하다. 예를 들어 `replay_rate_per_sec < 5,000` 상태가 10분 이상 지속되면 병목 경고, `sequence_gap_total > 0`이면 즉시 중단, `replay_errors_total > 100`이면 운영자 승인을 요구하는 식으로 룰을 정해야 한다. 이런 기준이 없으면 대규모 리플레이는 "돌아는 가는데 믿을 수 없는 작업"이 되기 쉽다.

### 적용 [[435_checklist_based_testing|체크리스트]]

1. 리플레이 [[216_progress_in_synchronization|진행]]률과 ETA를 오프셋 기준으로 계산할 수 있는가?
2. [[022_snapshot_backup_architecture|스냅샷]] 기준점과 마지막 [[395_verification_process_review|검증]] 시점이 대시보드에 노출되는가?
3. 이벤트 누락·중복·[[288_version_ihl_tos_total_length|버전]] 불일치를 별도 [[342_routing_metric_hop_bandwidth_delay|메트릭]]으로 수집하는가?
4. 리플레이 완료 후 샘플 [[395_verification_process_review|검증]] 또는 [[112_checksum|체크섬]] 비교 절차가 있는가?

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[139_throughput|처리량]]만 보고 정합성 [[395_verification_process_review|검증]] 없이 "100% 완료"로 선언하는 경우
- [[022_snapshot_backup_architecture|스냅샷]] [[268_strategy_pattern|전략]] 없이 항상 처음부터 재생해 [[451_mttr|MTTR]] 목표를 스스로 악화시키는 경우
- 리플레이와 라이브 소비를 같은 [[191_consumer_group_kafka_partition_load_balancing|컨슈머 그룹]]으로 섞어 운영하는 경우

기술사 관점에서는 "[[658_ir_recovery|복구]] 속도"와 "[[658_ir_recovery|복구]] [[002_bigdata_5v|정확성]]"의 균형을 강조해야 한다. 리플레이는 단순 운영 배치가 아니라 [[090_service_kubernetes_network_load_balancing|서비스]] 복귀 판단을 좌우하는 핵심 단계이므로, 관측성 설계 자체가 [[658_ir_recovery|복구]] 아키텍처의 일부라고 설명하는 것이 적절하다.

- **📢 섹션 요약 비유**: 도서관 책을 다시 꽂을 때 빨리 꽂는 것도 중요하지만, [[104_classification_analysis|분류]] 번호가 틀리면 결국 다시 찾아야 한다. 많이 꽂았다는 숫자보다 제대로 꽂았는지가 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 리플레이 [[229_monitor|모니터]]링이 잘 갖춰지면 운영팀은 [[658_ir_recovery|복구]] 상태를 실시간으로 설명할 수 있고, 예상 완료 시간을 근거 있게 제시할 수 있다. 또한 누락 이벤트, 핸들러 실패, 프로젝션 불일치 같은 문제를 조기에 발견해 "완료는 했지만 잘못 [[658_ir_recovery|복구]]된 상태"를 막을 수 있다. 이는 [[451_mttr|MTTR]] 단축뿐 아니라 [[658_ir_recovery|복구]] [[085_confidence_association_rule_conditional_probability|신뢰도]] 향상에도 직접 기여한다.

한계도 있다. 이벤트량이 매우 크면 리플레이 자체가 비용 집약적이며, [[022_snapshot_backup_architecture|스냅샷]] 주기나 [[430_index_fast_full_scan|병렬]] 처리 [[268_strategy_pattern|전략]]을 잘못 잡으면 [[229_monitor|모니터]]링이 좋아도 [[658_ir_recovery|복구]] 시간이 길 수 있다. 따라서 장기적으로는 [[022_snapshot_backup_architecture|스냅샷]] [[164_policy|정책]] 최적화, [[514_partition_slice_volume|파티션]] [[430_index_fast_full_scan|병렬]]화, 프로젝션별 체크포인트, 자동 정합성 [[395_verification_process_review|검증]]까지 포함한 체계로 발전해야 한다.

결론적으로 이 주제는 "이벤트를 다시 읽는 작업을 눈에 보이게 만드는 기술"이 아니다. 더 정확히 말하면, **[[658_ir_recovery|복구]]의 속도와 [[002_bigdata_5v|정확성]]을 동시에 운영 가능한 상태로 만드는 기술**이다. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]을 채택한 조직이라면 리플레이 [[229_monitor|모니터]]링은 선택이 아니라 필수 운영 역량에 가깝다.

- **📢 섹션 요약 비유**: 긴 퍼즐을 다시 맞출 때 현재 몇 조각을 맞췄는지, 빠진 조각은 없는지, 언제 완성될지 보드에 표시해 두면 모두가 안심할 수 있다. 리플레이 [[229_monitor|모니터]]링은 그 [[216_progress_in_synchronization|진행]]판 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) | 상태를 이벤트 순서로 저장하므로 리플레이가 [[658_ir_recovery|복구]]의 핵심 수단이 됨 |
| 프로젝션 (Projection) | 이벤트를 읽기 모델로 변환하는 대상이며 리플레이의 직접 [[658_ir_recovery|복구]] 결과물 |
| [[022_snapshot_backup_architecture|스냅샷]] ([[637_zfs_snapshot_cow_architecture|Snapshot]]) | 리플레이 시작점을 앞당겨 MTTR을 줄이는 보조 장치 |
| 컨슈머 랙 ([[089_consumer_lag|Consumer Lag]]) | 평시 [[015_지연_데이터_관점|지연]] [[229_monitor|모니터]]링 지표로, 리플레이 [[216_progress_in_synchronization|진행]]률과 구분해 봐야 함 |
| [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]) | 재시도·중복 적용 상황에서 정합성을 지키는 핵심 설계 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
Event Store 축적
    │
    ▼
Projection 재구성 필요
    │
    ▼
Replay Worker · Snapshot 기반 복구
    │
    ▼
Progress · ETA · Error · Gap 모니터링
    │
    ▼
정합성 검증 · Blue/Green 전환
    │
    ▼
병렬 리플레이 · 자동 복구 운영
```

이 흐름도는 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 시스템이 단순 저장을 넘어, [[658_ir_recovery|복구]] 가능성과 운영 관측성까지 함께 설계되어야 함을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]은 매일 일어난 일을 순서대로 적어 둔 긴 이야기책 같아요.
2. 리플레이는 그 책을 다시 읽어 지금 상태를 만드는 것이고, [[229_monitor|모니터]]링은 몇 [[286_page_frame|페이지]]까지 읽었는지 알려 주는 책갈피예요.
3. 책갈피가 없거나 [[286_page_frame|페이지]]가 빠지면 다시 읽기가 오래 걸리거나 틀릴 수 있어서, 속도와 [[002_bigdata_5v|정확성]]을 같이 봐야 해요.
