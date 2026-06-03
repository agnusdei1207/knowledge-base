---
title: 174. 분산 트랜잭션 한계 및 2PC (Two-Phase Commit) 배제 이유 - 블로킹 오버헤드
date: '2026-05-06'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]])는 여러 [[001_dikw_pyramid|데이터]] 저장소에 걸친 변경을 하나의 원자적 커밋처럼 보이게 만들기 위해, 참여자 전원에게 **준비(Prepare)와 최종 결정(Commit/[[313_rollback|Rollback]])** 을 강제하는 동기식 [[136_variance|분산]] 커밋 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이다.
> 2. **가치**: 참여 자원이 동일하고 네트워크가 안정적이며 [[191_transaction_concept_states|트랜잭션]]이 짧다면, [[090_service_kubernetes_network_load_balancing|서비스]] 경계를 넘는 [[289_cqrs_db|쓰기]] 작업에도 강한 [[193_atomicity_all_or_nothing|원자성]]([[193_atomicity_all_or_nothing|Atomicity]])을 부여할 수 있다.
> 3. **판단 포인트**: [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]]) 와 클라우드 환경에서는 락 점유, 블로킹, 조정자 의존성, 이기종 자원 비호환 때문에 비용이 너무 커서, [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]])·아웃박스·[[551_compensating_transaction_logical_rollback|보상 트랜잭션]]이 더 현실적인 대안이 된다.

---

## Ⅰ. 개요 및 필요성

[[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]은 여러 [[090_service_kubernetes_network_load_balancing|서비스]]나 여러 [[002_database_definition|데이터베이스]]에 걸친 변경을 하나의 업무 단위로 묶고 싶을 때 등장한다. 예를 들어 주문 [[090_service_kubernetes_network_load_balancing|서비스]]는 주문을 [[087_process_state_transition|생성]]하고, 결제 [[090_service_kubernetes_network_load_balancing|서비스]]는 승인 상태를 기록하며, 재고 [[090_service_kubernetes_network_load_balancing|서비스]]는 수량을 차감해야 한다. 이 세 단계 중 하나만 성공하고 나머지가 실패하면 업무 [[001_dikw_pyramid|데이터]]는 바로 불일치 상태가 된다.

단일 [[002_database_definition|데이터베이스]] 안에서는 ACID ([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) [[191_transaction_concept_states|트랜잭션]]으로 이 문제를 다룰 수 있다. 하지만 [[090_service_kubernetes_network_load_balancing|서비스]]마다 자기 저장소를 가지는 [[619_msa_traffic_hardware|MSA]] 에서는 "모두 성공하거나 모두 취소"를 자연스럽게 보장해 주는 전역 [[191_transaction_concept_states|트랜잭션]] 경계가 사라진다. 여기서 등장한 고전적 해법이 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 다.

[[549_2pc_two_phase_commit_limitations_msa|2PC]] 의 출발점은 명확하다. **참여자 전원이 확실히 준비되었는지 먼저 [[396_validation|확인]]한 뒤, 그 다음에만 최종 커밋을 허용하자**는 것이다. 이 사고는 이론적으로 깔끔하지만, 준비 후 최종 결정 전까지 모두가 기다려야 한다는 대가를 함께 안고 들어온다.

- **📢 섹션 요약 비유**: 친구 셋이 카드로 공동 결제할 때 "모두 결제 준비됐지? 한 명이라도 안 되면 전부 취소!"라고 외치는 방식과 같다. 깔끔해 보이지만, 한 명이 휴대폰을 떨어뜨리는 순간 나머지 둘도 계산대 앞에서 꼼짝없이 기다려야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[549_2pc_two_phase_commit_limitations_msa|2PC]] 는 보통 **조정자 ([[250_coordinator_participant_2pc_roles|Coordinator]]) + 참여자 (Participant)** 구조로 동작한다. 조정자는 [[191_transaction_concept_states|트랜잭션]] 참여자들에게 먼저 준비 여부를 묻고, 전원이 준비 완료라고 응답해야만 최종 커밋을 명령한다. 참여자는 Prepare 단계에서 로컬 변경을 디스크 [[568_logs_distributed_logging_elk_fluentd|로그]]에 남기고, 관련 자원을 잠근 채 최종 명령을 기다린다.

| 단계 | 조정자 동작 | 참여자 동작 | 시스템 대가 |
| :--- | :--- | :--- | :--- |
| Prepare | "커밋 가능?" 투표 요청 전송 | 로컬 작업 수행 후 [[568_logs_distributed_logging_elk_fluentd|로그]] 기록, 락 유지, Yes/No 응답 | 응답 대기 동안 [[015_지연_데이터_관점|지연]] 발생 |
| Decision | 전원 Yes 면 Commit, 하나라도 No 면 [[313_rollback|Rollback]] 결정 | 결정 [[389_mesh_topology|메시]]지 수신 대기 | 조정자 [[015_지연_데이터_관점|지연]]이 전체 [[015_지연_데이터_관점|지연]]으로 전파 |
| Completion | 최종 결과 통보 및 종료 | Commit/[[313_rollback|Rollback]] 후 락 해제 | 네트워크 실패 시 재전송·[[658_ir_recovery|복구]] 필요 |

아래 그림은 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 의 핵심 문제를 보여 준다. Prepare 이후에는 참여자가 스스로 결정을 내릴 수 없기 때문에, 조정자 [[015_지연_데이터_관점|지연]]이나 장애가 곧 **블로킹 구간**이 된다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                 Two-Phase Commit blocking window                   │
├────────────────────────────────────────────────────────────────────┤
│ Coordinator : prepare? ---> wait votes ---> COMMIT / ABORT        │
│                     │                    ▲                         │
│ Order DB    : lock row + YES ============┘                         │
│ Payment DB  : lock row + YES ============┘                         │
│ Inventory DB: lock row + YES ============┘                         │
│                                                                    │
│ If coordinator fails after all YES:                                │
│ participants stay in uncertain state and keep waiting              │
└────────────────────────────────────────────────────────────────────┘
```

핵심은 Prepare 단계가 "검사"가 아니라 거의 커밋 직전 상태라는 점이다. 참여자는 이미 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 가능한 최소 단위를 넘어 로컬 자원을 잡아 두고, 최종 명령을 기다린다. 따라서 [[191_transaction_concept_states|트랜잭션]]이 길어질수록 락 경쟁, [[139_throughput|처리량]] 저하, 사용자 [[015_지연_데이터_관점|지연]]이 함께 커진다.

이 때문에 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 는 짧고 통제된 내부 시스템에서는 성립할 수 있지만, [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]과 자원 다양성이 큰 환경에서는 급격히 부담스러워진다. 다시 말해 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 의 본질은 "전역 [[193_atomicity_all_or_nothing|원자성]]"이 아니라, **전역 [[193_atomicity_all_or_nothing|원자성]]을 위해 모두를 잠시 세워 두는 메커니즘**이다.

- **📢 섹션 요약 비유**: 출발선에서 심판 총소리를 기다리는 육상 경기와 같다. 모두가 자세를 잡고 멈춰 서 있는 동안에는 질서가 유지되지만, 총이 늦게 울리면 선수들은 그만큼 오래 긴장한 채 서 있어야 한다.

---

## Ⅲ. 비교 및 연결

[[549_2pc_two_phase_commit_limitations_msa|2PC]] 의 한계를 제대로 이해하려면 [[548_local_vs_distributed_transactions|로컬 트랜잭션]], [[305_saga|사가 패턴]], TCC (Try-Confirm-Cancel) 와 비교해야 한다. 이들은 모두 "여러 단계를 어떻게 일관되게 관리할 것인가"에 답하지만, 락을 다루는 방식과 실패 [[658_ir_recovery|복구]] 철학이 다르다.

| 비교 축 | [[548_local_vs_distributed_transactions|로컬 트랜잭션]] | [[549_2pc_two_phase_commit_limitations_msa|2PC]] | [[305_saga|Saga]] | TCC |
| :--- | :--- | :--- | :--- | :--- |
| 적용 범위 | 단일 [[090_service_kubernetes_network_load_balancing|서비스]]·단일 저장소 | 다중 저장소·다중 [[090_service_kubernetes_network_load_balancing|서비스]] | [[090_service_kubernetes_network_load_balancing|서비스]] 간 비즈니스 흐름 | 예약 가능한 자원 흐름 |
| [[194_consistency_database_integrity|일관성]] 수준 | 강한 [[194_consistency_database_integrity|일관성]] | 강한 [[194_consistency_database_integrity|일관성]] | 최종적 [[194_consistency_database_integrity|일관성]] | 단계적 강한 제어 |
| 락 유지 | 짧음 | 준비 후 최종 결정까지 길어질 수 있음 | 보통 없음 | Try 단계에서 자원 예약 |
| 실패 [[658_ir_recovery|복구]] | 즉시 [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 조정자·참여자 재조정 필요 | [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] | Confirm/Cancel 호출 |
| 잘 맞는 환경 | 모놀리식 업무 | 통제된 내부 시스템 | 클라우드 [[619_msa_traffic_hardware|MSA]], 비동기 이벤트 | 좌석·재고 예약형 [[090_service_kubernetes_network_load_balancing|서비스]] |

[[619_msa_traffic_hardware|MSA]] 에서 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 가 기피되는 이유는 단순히 느려서가 아니다. 첫째, [[090_service_kubernetes_network_load_balancing|서비스]] 간 네트워크 홉이 늘수록 Prepare/Commit 왕복 비용이 누적된다. 둘째, [[145_message_broker_sync_async|메시지 브로커]], 캐시, [[035_nosql|NoSQL]] 저장소처럼 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 친화적이지 않은 자원이 섞이면 전체 설계가 제한된다. 셋째, 조정자가 병목이 되거나 장애 지점이 되면 [[090_service_kubernetes_network_load_balancing|서비스]] 독립성 자체가 흔들린다.

반면 [[305_saga|사가 패턴]]은 각 [[090_service_kubernetes_network_load_balancing|서비스]]의 [[548_local_vs_distributed_transactions|로컬 트랜잭션]]을 먼저 확정하고, 실패 시 보상 작업으로 되돌리는 방식을 택한다. 이 구조는 중간에 잠깐 불일치 상태가 생길 수 있지만, 블로킹 없이 더 높은 [[452_availability|가용성]]과 확장성을 얻는다. 따라서 [[619_msa_traffic_hardware|MSA]] 에서는 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 를 "정합성의 정답"이 아니라, **강한 정합성을 얻는 대신 독립성과 [[139_throughput|처리량]]을 희생하는 선택지**로 봐야 한다.

- **📢 섹션 요약 비유**: [[549_2pc_two_phase_commit_limitations_msa|2PC]] 는 모두 손을 꼭 잡고 함께 다니는 행진이고, [[312_saga_pattern_choreography_orchestration|사가]]는 각자 먼저 움직이되 문제가 생기면 다시 제자리로 돌아오는 약속이다. 전자는 질서가 강하지만 느리고, 후자는 유연하지만 사후 정리가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 를 검토해도 되는 경우는 의외로 좁다. 같은 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 안의 [[083_relationship_in_er_model|관계]]형 [[003_dbms_database_management_system|데이터베이스 관리 시스템]] (RDBMS, Relational [[501_database|Database]] [[372_management|Management]] System) 들이 짧은 업무 [[191_transaction_concept_states|트랜잭션]]을 처리하고, 참여자 수가 적으며, 운영팀이 중앙 조정자와 장애 [[658_ir_recovery|복구]] 절차를 강하게 통제할 수 있을 때 정도다. 배치성 재무 정산처럼 "무조건 같이 반영되어야 한다"는 요구가 매우 강한 경우가 대표적이다.

반대로 전자상거래 주문·결제·배송처럼 외부 응용 프로그래밍 인터페이스 ([[014_api_posix|API]], [[014_api_posix|Application Programming Interface]]), [[145_message_broker_sync_async|메시지 브로커]], 재시도, 사용자 대기 시간이 얽힌 흐름에는 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 가 잘 맞지 않는다. 사용자가 모바일 앱에서 결제 버튼을 누르고 몇 초 동안 전체 참여자가 락을 잡은 채 기다리는 구조는 확장성과 장애 격리 모두에 불리하다. 이 경우에는 [[548_local_vs_distributed_transactions|로컬 트랜잭션]] + [[314_transactional_outbox_pattern|트랜잭셔널 아웃박스]] + [[312_saga_pattern_choreography_orchestration|사가]] 보상 흐름이 일반적으로 더 현실적이다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 참여 자원이 모두 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 또는 X/Open XA 를 안정적으로 지원하는가?
2. [[191_transaction_concept_states|트랜잭션]]이 사람 개입 없이 수백 밀리초~수초 안에 끝나는 짧은 흐름인가?
3. [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]과 장애가 작고, 중앙 조정자를 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있게 운영할 수 있는가?
4. 실패 시 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]보다 즉시 원자 커밋이 정말 더 중요한가?
5. [[145_message_broker_sync_async|메시지 브로커]], 캐시, 외부 결제사처럼 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 밖의 자원이 업무 핵심에 포함되어 있지 않은가?
6. 교차 [[090_service_kubernetes_network_load_balancing|서비스]] 락 점유로 인한 [[139_throughput|처리량]] 저하를 수용할 수 있는가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[179_kafka_flink_watermark_time_window|Kafka]], [[542_redis|Redis]], 외부 [[014_api_posix|API]] 까지 한 번에 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 로 묶으려는 경우
- 사용자 승인 대기처럼 긴 업무를 Prepare 상태로 오래 끌고 가는 경우
- 교차 리전, 교차 클라우드 환경에서 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 로 저지연을 기대하는 경우
- 보상 설계를 회피하려고 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 를 "만능 해결책"처럼 도입하는 경우

기술사 관점에서 중요한 판단은 이것이다. **[[549_2pc_two_phase_commit_limitations_msa|2PC]] 는 불가능해서 버리는 기술이 아니라, 클라우드형 [[136_variance|분산]] 시스템이 요구하는 [[452_availability|가용성]]·독립성·[[139_throughput|처리량]]과 너무 자주 충돌하기 때문에 의식적으로 배제되는 기술**이다.

- **📢 섹션 요약 비유**: 중요한 서류에 모두가 동시에 도장을 찍는 절차는 엄격하고 안전하지만, 사람 수가 많아질수록 회의실 예약과 대기 시간이 더 큰 문제가 된다. 그래서 현대 조직은 꼭 필요한 문서에만 전원 서명을 요구하고, 나머지는 책임자별 승인으로 나눠 처리한다.

---

## Ⅴ. 기대효과 및 결론

[[549_2pc_two_phase_commit_limitations_msa|2PC]] 의 가장 큰 장점은 분명하다. 여러 저장소에 걸친 변경을 하나의 원자적 결정처럼 보이게 만들어, 회계나 재무처럼 강한 정합성이 핵심인 업무에서 설계 설명이 단순해진다. 이 점에서 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 는 여전히 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 이론의 기준점이다.

하지만 현대 [[_keyword_list|엔터프라이즈 시스템]]에서는 그 대가가 너무 자주 크게 나타난다. 락 유지 시간 증가, 조정자 병목, 장애 시 불확실 상태, 이기종 자원 비지원이 대표적이다. 그래서 실제 아키텍처는 전역 [[193_atomicity_all_or_nothing|원자성]]보다 **[[090_service_kubernetes_network_load_balancing|서비스]]별 로컬 정합성과 [[658_ir_recovery|복구]] 가능한 업무 흐름** 쪽으로 이동해 왔다.

결론적으로 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 를 기억하는 가장 정확한 관점은 "완벽한 [[194_consistency_database_integrity|일관성]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]"이 아니라, **강한 [[194_consistency_database_integrity|일관성]]을 얻기 위해 시스템 전체를 동기식으로 묶는 비용 구조**다. [[619_msa_traffic_hardware|MSA]] 시대의 핵심 질문은 "[[549_2pc_two_phase_commit_limitations_msa|2PC]] 를 쓸 수 있는가?"보다 "정말 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 가 필요한가?"다.

- **📢 섹션 요약 비유**: [[549_2pc_two_phase_commit_limitations_msa|2PC]] 는 모두가 동시에 문을 잠그고 열쇠를 [[396_validation|확인]]해야 출발할 수 있는 규율 강한 여행이다. 절대 흩어지지 않는 대신, 한 명만 늦어도 모두가 그 자리에서 멈춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 조정자 ([[250_coordinator_participant_2pc_roles|Coordinator]]) | [[549_2pc_two_phase_commit_limitations_msa|2PC]] 의 Prepare·Commit 결정을 중앙에서 관리하는 주체 |
| 참여자 (Participant) | 로컬 자원을 잠그고 Yes/No 투표를 수행하는 자원 관리자 |
| ACID | 단일 저장소의 강한 [[191_transaction_concept_states|트랜잭션]] 개념으로, [[549_2pc_two_phase_commit_limitations_msa|2PC]] 가 [[136_variance|분산]] 환경에서 확장하려는 대상 |
| [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]) | [[549_2pc_two_phase_commit_limitations_msa|2PC]] 대신 [[548_local_vs_distributed_transactions|로컬 트랜잭션]]과 보상 흐름으로 정합성을 맞추는 대안 |
| [[314_transactional_outbox_pattern|트랜잭셔널 아웃박스]] | [[001_dikw_pyramid|데이터]] 변경과 이벤트 발행 사이의 정합성을 [[548_local_vs_distributed_transactions|로컬 트랜잭션]]으로 보장하는 기법 |
| [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]) | 재시도와 보상 처리를 안전하게 만들기 위한 핵심 성질 |
| TCC (Try-Confirm-Cancel) | 예약 가능한 자원을 명시적으로 다루는 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
Single database local transaction
              │
              ▼
Database per service and distributed write problem
              │
              ▼
2PC for atomic commit across participants
              │
              ▼
Blocking, coordinator dependency, heterogeneous limits
              │
              ▼
Saga / outbox / idempotent recovery patterns
```

이 흐름은 "단일 저장소 [[193_atomicity_all_or_nothing|원자성]] → [[090_service_kubernetes_network_load_balancing|서비스]] 분리 → 전역 커밋 필요 → [[549_2pc_two_phase_commit_limitations_msa|2PC]] 도입 → 블로킹 한계 → 비동기 [[658_ir_recovery|복구]] 패턴"으로 이어지는 아키텍처 진화를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구들이 같이 보물상자를 열 때, 모두가 "준비됐어!"라고 말해야만 뚜껑을 여는 규칙이 2PC예요.
2. 그런데 한 친구가 대답을 늦게 하면 다른 친구들은 손을 잡은 채 계속 기다려야 해요.
3. 그래서 요즘은 각자 먼저 움직이고, 문제가 생기면 다시 정리하는 다른 방법도 많이 써요.
