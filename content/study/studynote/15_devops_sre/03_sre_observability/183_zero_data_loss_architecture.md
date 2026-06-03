+++
weight = 183
title = "183. 데이터 손실 제로 (Zero Data Loss) 아키텍처"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] 손실 제로 ([[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss) 아키텍처는 "커밋되었다고 응답한 [[001_dikw_pyramid|데이터]]는 장애 뒤에도 사라지지 않는다"를 보장하도록 [[289_cqrs_db|쓰기]] 응답 시점과 [[016_replication_factor|복제]] 규칙을 설계한 구조이며, 핵심 기준은 [[177_rpo_recovery_point_objective|Recovery Point Objective]] ([[177_rpo_recovery_point_objective|RPO]]) = 0이다.
> 2. **가치**: 결제, 주문, 의료 기록, [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]처럼 한 건의 손실도 고객 신뢰와 법적 책임에 직결되는 시스템에서 [[090_service_kubernetes_network_load_balancing|서비스]] 연속성과 브랜드 신뢰를 동시에 지켜 준다.
> 3. **판단 포인트**: 진짜 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss는 동기 [[016_replication_factor|복제]]만으로 끝나지 않고, Write-Ahead Log (WAL), Quorum, 페일오버 펜싱, idempotent replay, 하류 이벤트 [[194_consistency_database_integrity|일관성]]까지 함께 맞아야 성립한다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] 손실 제로 아키텍처는 "장애가 나도 안 잃는다"는 모호한 구호가 아니다. 더 정확히 말하면, 시스템이 "[[289_cqrs_db|쓰기]] 성공"을 반환한 시점 이후에는 서버 하나, 가용 영역 하나, 심지어 리더 노드 하나가 사라져도 그 [[289_cqrs_db|쓰기]] 결과가 반드시 복원 가능해야 한다는 약속이다. 그래서 핵심은 저장 장치 수보다 **응답을 언제 주는가**에 있다.

이 개념이 중요한 이유는 고객이 장애보다 [[001_dikw_pyramid|데이터]] 소실을 더 오래 기억하기 때문이다. [[286_page_frame|페이지]]가 잠깐 느린 것은 [[658_ir_recovery|복구]] 후 잊힐 수 있지만, 결제는 되었는데 주문 내역이 없거나, 환자 기록 한 줄이 사라지거나, [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]가 비면 신뢰는 구조적으로 무너진다. [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss는 [[452_availability|가용성]]의 하위 기능이 아니라, 고객과 조직이 "시스템의 약속을 믿어도 되는가"를 가르는 경계다.

아래 그림은 같은 장애라도 ACK 시점에 따라 결과가 완전히 달라짐을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ ACK timing defines data loss                                       │
├────────────────────────────────────────────────────────────────────┤
│ Early ACK path : write -> primary ACK -> primary crash -> lost    │
│ Safe ACK path  : write -> quorum durable -> ACK -> crash -> safe  │
└────────────────────────────────────────────────────────────────────┘
```

또한 [[177_rpo_recovery_point_objective|RPO]]=0은 [[176_rto_recovery_time_objective|Recovery Time Objective]] ([[176_rto_recovery_time_objective|RTO]]) = 0과 다르다. [[001_dikw_pyramid|데이터]]를 잃지 않아도 [[658_ir_recovery|복구]] 전환이 느리면 고객 체감 중단은 여전히 크다. 따라서 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss는 "무손실"과 "빠른 전환"을 분리해 설계하되, 우선순위는 **잃지 않는 ACK 규칙**에 둬야 한다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 손실 제로는 숙제를 냈다고 표시하기 전에 선생님이 실제로 공책을 받아 보관함에 넣는 것과 같다. "냈어요"라는 말만 듣고 체크하면 나중에 공책이 사라질 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss를 구현하는 핵심 원리는 단순하다. **클라이언트에게 성공을 응답하기 전에, 최소한 하나의 독립된 실패 영역 밖까지 [[001_dikw_pyramid|데이터]]가 안전하게 기록되어 있어야 한다.** 이를 위해서는 WAL, 쿼럼 [[016_replication_factor|복제]], 리더 선출, 펜싱, 하류 이벤트 재생이 한 묶음으로 움직여야 한다.

| 계층 | 핵심 역할 | 놓치기 쉬운 포인트 |
| :--- | :--- | :--- |
| WAL / Commit Log | [[289_cqrs_db|쓰기]] 의도를 먼저 영속화 | 메모리 ACK만으로는 무손실이 아님 |
| Quorum [[016_replication_factor|Replication]] | 다수 노드에 내구성 [[016_replication_factor|복제]] | 서로 다른 실패 [[064_relation_domain|도메인]]에 위치해야 의미가 큼 |
| Leader Election / Fencing | 동시에 두 리더가 쓰지 못하게 차단 | Split-Brain 방지가 필수 |
| Outbox / [[217_cdc_binlog_change_capture_debezium|Change Data Capture]] ([[217_cdc_binlog_change_capture_debezium|CDC]]) | DB 변경과 이벤트 발행을 정합적으로 연결 | 하류 큐 손실이 남으면 [[401_transport_layer_role_end_to_end_multiplexing|end-to-end]] 무손실이 깨짐 |
| Idempotent Replay | 재시도·재생 시 중복 반영 방지 | [[658_ir_recovery|복구]]는 되지만 값이 두 번 들어가면 실패 |
| [[298_immutable|Immutable]] [[555_backup_and_restore_strategy|Backup]] | [[369_logic_bomb|논리]] 오류·[[730_ransomware|랜섬웨어]] 대비 최종 안전망 | [[555_backup_and_restore_strategy|백업]]만으로는 [[177_rpo_recovery_point_objective|RPO]]=0이 아님 |

아래 경로는 "무손실 ACK"가 어떤 순서를 따라야 하는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Zero Data Loss write path                                          │
├────────────────────────────────────────────────────────────────────┤
│ Client -> API -> WAL append -> quorum fsync -> commit index       │
│                                 │                                  │
│                                 ├-> ACK to client                 │
│                                 ├-> replicated outbox / CDC feed  │
│                                 └-> failover candidate eligible   │
└────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심은 "리더가 기록했다"가 아니라 "페일오버 후에도 살아남는 상태로 기록되었다"는 점이다. 예를 들어 3노드 합의라면 보통 2노드 이상이 내구성 있게 기록한 뒤에만 커밋 [[154_database_index_b_tree_search_optimization|인덱스]]가 올라간다. 이 원리가 있어야 리더 장애 후 새 리더가 커밋된 마지막 상태를 그대로 이어받을 수 있다.

또 하나의 흔한 오해는 [[002_database_definition|데이터베이스]]만 동기 [[016_replication_factor|복제]]하면 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss가 완성된다고 보는 것이다. 주문 [[001_dikw_pyramid|데이터]]는 안전하게 저장됐더라도, 결제 이벤트가 [[145_message_broker_sync_async|메시지 브로커]]에 비동기로 발행되다 유실되면 전체 비즈니스 흐름은 여전히 깨진다. 그래서 실무에서는 [[314_transactional_outbox_pattern|Transactional Outbox]], `acks=all` 계열 [[389_mesh_topology|메시]]지 보장, idempotent consumer가 함께 필요하다.

- **📢 섹션 요약 비유**: [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss 아키텍처는 금고 문 하나를 두껍게 만드는 일이 아니라, 기록실·복사본·출입 통제·인계 장부를 모두 맞추는 일과 같다. 어느 한 곳만 튼튼해도 전체 증빙은 완성되지 않는다.

---

## Ⅲ. 비교 및 연결

[[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss를 이해하려면 동기 [[016_replication_factor|복제]], 반동기 [[016_replication_factor|복제]], 비동기 [[016_replication_factor|복제]]의 경계를 분명히 봐야 한다. 세 방식 모두 "[[016_replication_factor|복제]]"라는 이름을 쓰지만, ACK를 언제 주는지가 다르기 때문에 실제 RPO는 크게 달라진다.

| 방식 | ACK 시점 | 일반적 [[177_rpo_recovery_point_objective|RPO]] | [[015_지연_데이터_관점|지연]] 영향 | 잘 맞는 워크로드 |
| :--- | :--- | :--- | :--- | :--- |
| 동기 쿼럼 [[016_replication_factor|복제]] | 원격 노드까지 내구성 기록 후 | 0 | 가장 큼 | 결제, 원장, 핵심 주문 |
| 반동기 [[016_replication_factor|복제]] | 일부 원격 [[396_validation|확인]] 후 | 거의 0 또는 수초 | 중간 | 일반 이커머스, 중요 업무 |
| 비동기 [[016_replication_factor|복제]] | 로컬 커밋 직후 | [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]]만큼 손실 가능 | 작음 | 분석, [[568_logs_distributed_logging_elk_fluentd|로그]], 비핵심 캐시 |

여기서 중요한 연결 개념이 [[300_failover_architecture|Failover]] / Failback이다. 무손실 설계는 페일오버가 성공했을 때만 의미가 있고, 페일백 시에도 [[568_logs_distributed_logging_elk_fluentd|로그]] 정합성이 깨지지 않아야 한다. 또 [[307_event_sourcing|Event Sourcing]], [[136_variance|분산]] 합의, [[389_mesh_topology|메시]]지 큐 내구성 [[009_config|설정]]은 모두 "장애 후 어떤 기록을 정본으로 삼을 것인가"라는 같은 질문에 답한다.

| 비교 대상 | 강점 | 한계 |
| :--- | :--- | :--- |
| 동기 DB [[016_replication_factor|복제]] | 강한 정합성, 명확한 ACK 규칙 | [[015_지연_데이터_관점|지연]]과 [[452_availability|가용성]] 비용 증가 |
| [[568_logs_distributed_logging_elk_fluentd|로그]] 우선(Event Log First) 구조 | 재생과 [[606_auditing_linux_auditd|감사]]에 강함 | 소비자 중복 제어가 필수 |
| [[555_backup_and_restore_strategy|백업]] [[658_ir_recovery|복구]] 중심 | 비용 낮음 | [[177_rpo_recovery_point_objective|RPO]]=0 불가, [[658_ir_recovery|복구]] 시점 손실 존재 |

따라서 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss는 단순히 "동기 [[016_replication_factor|복제]] 사용 여부"를 묻는 문제가 아니다. **ACK 규칙, 리더 선출, 하류 재생, 복귀 [[395_verification_process_review|검증]]**까지 같은 설계 축에 놓고 봐야 진짜 경계가 드러난다.

- **📢 섹션 요약 비유**: 동기 [[016_replication_factor|복제]]와 비동기 [[016_replication_factor|복제]]의 차이는 영수증을 주기 전에 카드 결제가 실제 승인됐는지 [[396_validation|확인]]하는 가게와, "아마 됐겠지" 하고 먼저 영수증을 주는 가게의 차이와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss를 채택할지 말지는 "이 [[001_dikw_pyramid|데이터]]를 잃었을 때 회사가 실제로 얼마를 잃는가"로 판단해야 한다. 모든 시스템에 [[177_rpo_recovery_point_objective|RPO]]=0을 강제하면 비용과 [[015_지연_데이터_관점|지연]]이 과도해지고, 반대로 핵심 경로에 느슨한 [[016_replication_factor|복제]]를 쓰면 장애 한 번이 고객 신뢰를 무너뜨린다.

| 워크로드 | 권장 아키텍처 | 이유 |
| :--- | :--- | :--- |
| 결제 원장 | 다중 [[452_availability|Availability]] Zone 동기 쿼럼 + 펜싱된 자동 페일오버 | 금액 누락과 중복 모두 허용 불가 |
| 주문 [[090_service_kubernetes_network_load_balancing|서비스]] | 동기 DB + [[314_transactional_outbox_pattern|Transactional Outbox]] + idempotent consumer | 주문과 하류 이벤트를 함께 지켜야 함 |
| [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] | Append-Only [[568_logs_distributed_logging_elk_fluentd|로그]] + 불변 저장소 + [[112_checksum|체크섬]] [[395_verification_process_review|검증]] | 사후 부인 방지가 중요 |
| 텔레메트리·검색 [[568_logs_distributed_logging_elk_fluentd|로그]] | 비동기 허용 가능 | 일부 손실보다 비용·[[139_throughput|처리량]]이 더 중요할 수 있음 |

기술사 관점의 [[435_checklist_based_testing|체크리스트]]는 다음과 같다.

1. "성공 응답"의 정의가 로컬 메모리 완료가 아니라 쿼럼 내구성 완료인가?
2. 리더 장애 시 Split-Brain을 막는 펜싱 토큰, 스토리지 잠금, 쿼럼 [[395_verification_process_review|검증]]이 있는가?
3. [[002_database_definition|데이터베이스]] 외에 [[145_message_broker_sync_async|메시지 브로커]], 캐시, 검색 색인까지 [[401_transport_layer_role_end_to_end_multiplexing|end-to-end]] 손실 경로를 점검했는가?
4. 재시도와 [[658_ir_recovery|복구]] 재생 과정이 중복 반영을 일으키지 않도록 idempotent key를 설계했는가?
5. 강제 장애 전환 훈련 후 해시, 행 수, 시퀀스, 체크포인트까지 [[395_verification_process_review|검증]]하는가?

[[128_water_scrum_fall_anti_pattern|안티패턴]]도 분명하다. 첫째, 원격 노드에 비휘발성 저장이 끝나기 전에 ACK를 주는 구조다. 둘째, [[022_snapshot_backup_architecture|스냅샷]]과 [[555_backup_and_restore_strategy|백업]]이 있으니 [[177_rpo_recovery_point_objective|RPO]]=0이라고 착각하는 구조다. 셋째, [[016_replication_factor|복제]]는 동기지만 하류 [[539_event_bus_stream_processing|이벤트 버스]]는 비동기로 흘려 전체 무손실을 깨는 구조다. 넷째, 대륙 간 동기 [[016_replication_factor|복제]]를 무리하게 요구해 [[015_지연_데이터_관점|지연]]과 [[452_availability|가용성]]을 동시에 잃는 구조다. 이런 경우에는 지역 쿼럼 + 읽기 전용 Degraded Mode가 더 현실적일 수 있다.

- **📢 섹션 요약 비유**: [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss 설계는 비싼 보험을 드는 것과 비슷하지만, 아무 보험이나 가입하는 게 아니라 어떤 물건은 전손 보장, 어떤 물건은 일부 보장만 필요한지 물건별로 나눠 설계해야 한다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss 아키텍처는 장애가 나도 "사라진 주문", "누락된 입금", "비어 있는 [[606_auditing_linux_auditd|감사]] 기록"을 남기지 않는다. 그 결과 고객 신뢰, 법적 [[606_auditing_linux_auditd|감사]] 대응, 사고 [[658_ir_recovery|복구]]의 재현 가능성이 모두 좋아진다. 특히 금융과 의료처럼 [[001_dikw_pyramid|데이터]] 자체가 [[090_service_kubernetes_network_load_balancing|서비스]] 약속인 영역에서는 이것이 곧 비즈니스 생존력이다.

하지만 대가도 분명하다. 동기 [[016_replication_factor|복제]]와 합의는 [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]]을 늘리고, 쿼럼 손실 시 [[289_cqrs_db|쓰기]] [[452_availability|가용성]]을 희생할 수 있다. 또한 글로벌 [[136_variance|분산]] 환경에서는 네트워크 왕복 시간이 그대로 비용이 되므로, "어디까지를 무손실 범위로 정의할 것인가"를 현실적으로 그어야 한다.

결론적으로 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss는 마법처럼 [[001_dikw_pyramid|데이터]]를 안 날리는 기능이 아니다. **클라이언트에게 성공이라고 말하는 순간을 가장 보수적으로 설계하는 아키텍처 원칙**이다. 이 원칙이 지켜질 때만 [[177_rpo_recovery_point_objective|RPO]]=0은 문서가 아니라 실제 고객 신뢰가 된다.

- **📢 섹션 요약 비유**: [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss는 사진을 찍은 뒤 카메라에만 남겨 두는 것이 아니라, 앨범과 클라우드에 모두 저장된 것을 [[396_validation|확인]]하고서야 "보관 완료"라고 말하는 습관과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[177_rpo_recovery_point_objective|RPO]] ([[177_rpo_recovery_point_objective|Recovery Point Objective]]) | [[001_dikw_pyramid|데이터]] 손실 허용 시점을 정하는 기준이며 [[585_zero_skipping|Zero]] [[001_dikw_pyramid|Data]] Loss의 핵심 목표 |
| [[176_rto_recovery_time_objective|RTO]] ([[176_rto_recovery_time_objective|Recovery Time Objective]]) | [[001_dikw_pyramid|데이터]]를 잃지 않아도 얼마나 빨리 돌아오는지 판단하는 별도 축 |
| WAL (Write-Ahead Log) | ACK 전에 [[289_cqrs_db|쓰기]] 의도를 영속화하는 기본 메커니즘 |
| Quorum [[016_replication_factor|Replication]] | 일부 노드 장애에도 커밋 기록을 보존하는 구조 |
| Fencing | Split-Brain으로 인한 이중 [[289_cqrs_db|쓰기]]를 막는 안전장치 |
| [[314_transactional_outbox_pattern|Transactional Outbox]] | DB 변경과 이벤트 발행의 손실 경계를 맞추는 패턴 |
| [[298_immutable|Immutable]] [[555_backup_and_restore_strategy|Backup]] | [[369_logic_bomb|논리]] 오류·삭제·[[730_ransomware|랜섬웨어]]에 대비하는 최후 방어선 |

### 📈 관련 키워드 및 발전 흐름도

```text
로컬 커밋 중심 저장
    │
    ▼
WAL 기반 내구성 확보
    │
    ▼
Quorum 복제 · 동기 ACK
    │
    ▼
Failover / Fencing / Replay
    │
    ▼
Outbox · CDC · End-to-End 무손실
    │
    ▼
고객 신뢰 기반의 Zero Data Loss 운영
```

이 흐름은 단일 노드 내구성에서 시작해, 다중 노드 [[016_replication_factor|복제]]와 하류 이벤트 정합성까지 확장되어야 비로소 "무손실"이 완성된다는 점을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 중요한 숙제는 한 공책에만 쓰지 않고, 안전한 두 곳에 똑같이 적어 둬야 해요.
2. 그리고 두 곳 다 잘 적힌 걸 [[396_validation|확인]]하기 전에는 "숙제 냈어요"라고 말하면 안 돼요.
3. 그래야 한 공책이 젖어도 다른 공책을 보고 똑같이 다시 보여 줄 수 있어요.
