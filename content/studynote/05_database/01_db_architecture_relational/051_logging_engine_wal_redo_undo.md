---
title: 51. 로깅 엔진 (Logging Engine)
date: '2026-04-30'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 로깅 엔진 ([[526_security_logging_and_monitoring_failures|Logging]] Engine)은 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]보다 먼저 변경 이력을 [[568_logs_distributed_logging_elk_fluentd|로그]]에 기록하는 WAL ([[236_wal_write_ahead_logging_protocol|Write-Ahead Logging]]) 원칙으로, [[002_database_definition|데이터베이스]]의 [[193_atomicity_all_or_nothing|원자성]] ([[193_atomicity_all_or_nothing|Atomicity]])과 [[196_durability_permanent_storage|영속성]] ([[196_durability_permanent_storage|Durability]])을 보장하는 [[658_ir_recovery|복구]] 핵심 [[192_module_independence|모듈]]이다.
> 2. **가치**: 커밋 시점에 무거운 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]] 전체를 즉시 쓰지 않아도, 순차 [[568_logs_distributed_logging_elk_fluentd|로그]]만 안전하게 기록하면 [[191_transaction_concept_states|트랜잭션]] 완료를 인정할 수 있어 [[282_performance_tactics|성능]]과 안정성을 동시에 확보한다.
> 3. **판단 포인트**: [[568_logs_distributed_logging_elk_fluentd|로그]] 버퍼 크기, fsync [[164_policy|정책]], 체크포인트 (Checkpoint), [[234_redo_roll_forward_durability_recovery|Redo]]/[[393_undo|Undo]] 범위 설계가 잘못되면 커밋 [[015_지연_데이터_관점|지연]]이나 긴 [[658_ir_recovery|복구]] 시간으로 이어진다.

---

## Ⅰ. 개요 및 필요성

[[002_database_definition|데이터베이스]]는 [[282_performance_tactics|성능]]을 위해 먼저 버퍼 풀 (Buffer Pool) 메모리에서 [[286_page_frame|페이지]]를 수정하고, 나중에 디스크에 반영한다. 문제는 이 사이에 장애가 발생하면 어떤 변경이 커밋됐고 어떤 변경이 중간 상태였는지 구분하기 어렵다는 점이다. 로깅 엔진은 이 모순을 해결하기 위해 "[[001_dikw_pyramid|데이터]]보다 [[568_logs_distributed_logging_elk_fluentd|로그]]를 먼저 쓴다"는 규칙을 강제한다.

즉 사용자가 `COMMIT`을 눌렀다고 해서 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]이 즉시 모두 갱신되는 것은 아니다. 먼저 변경 기록을 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]에 안전하게 남기고, 그 [[568_logs_distributed_logging_elk_fluentd|로그]]를 근거로 장애 후에도 다시 살리거나 되돌릴 수 있게 만든다. 그래서 로깅 엔진은 [[282_performance_tactics|성능]] 최적화 장치이면서 동시에 사고 수습 장치다.

- **📢 섹션 요약 비유**: 로깅 엔진은 배송 창고의 출고 장부와 같다. 물건을 트럭에 싣기 전에 장부에 먼저 기록해 두어야 사고가 나도 무엇을 보냈는지 다시 맞출 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

로깅 엔진은 [[191_transaction_concept_states|트랜잭션]] 변경을 [[568_logs_distributed_logging_elk_fluentd|로그]] 버퍼에 쌓고, 이를 디스크 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]에 순차적으로 flush한 뒤 커밋을 완료한다. 이후 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]는 여유가 있을 때 디스크로 내려보내도 된다. 이 구조가 가능한 이유가 WAL 규칙이다.

```text
┌──────────────────────────────────────────────────────────────┐
│                WAL 기반 로깅 엔진 동작 흐름                  │
├──────────────────────────────────────────────────────────────┤
│ 트랜잭션 수정                                                │
│    │                                                         │
│    ├──▶ 버퍼 풀의 페이지 변경 (Dirty Page)                  │
│    │                                                         │
│    └──▶ 로그 버퍼에 Log Record 생성                         │
│                 │                                            │
│                 ▼                                            │
│          로그 파일에 Flush  ──▶ COMMIT 응답                 │
│                 │                                            │
│                 ▼                                            │
│         나중에 데이터 페이지를 디스크에 Flush               │
└──────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [[568_logs_distributed_logging_elk_fluentd|로그]] 레코드 (Log Record) | 변경 전후 정보 기록 | [[234_redo_roll_forward_durability_recovery|Redo]]/[[393_undo|Undo]] 근거가 된다 |
| [[244_lsn_log_sequence_number_recovery_tracking|LSN]] ([[244_lsn_log_sequence_number_recovery_tracking|Log Sequence Number]]) | [[568_logs_distributed_logging_elk_fluentd|로그]] 순서 [[289_identification_flags_fragmentation_offset|식별자]] | [[286_page_frame|페이지]]와 [[568_logs_distributed_logging_elk_fluentd|로그]]의 일치성 검사 |
| [[568_logs_distributed_logging_elk_fluentd|로그]] 버퍼 | 메모리 내 임시 적재 공간 | 그룹 커밋 최적화에 활용 |
| 체크포인트 | [[658_ir_recovery|복구]] 시작 위치 단축 | [[658_ir_recovery|복구]] 시간과 런타임 I/O의 절충 |
| [[234_redo_roll_forward_durability_recovery|Redo]] / [[393_undo|Undo]] | 재실행 / 되돌리기 | 커밋/미커밋 상태를 복원 |

WAL의 핵심 규칙은 두 가지다. 첫째, **어떤 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]를 디스크에 [[289_cqrs_db|쓰기]] 전에는 해당 변경 [[568_logs_distributed_logging_elk_fluentd|로그]]가 먼저 디스크에 있어야 한다**. 둘째, **[[191_transaction_concept_states|트랜잭션]] 커밋을 인정하기 전에는 그 커밋 [[568_logs_distributed_logging_elk_fluentd|로그]]가 디스크에 있어야 한다**. 이 규칙 덕분에 시스템은 즉시 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]을 다 쓰지 않아도 [[658_ir_recovery|복구]] 가능성을 잃지 않는다.

- **📢 섹션 요약 비유**: 로깅 엔진은 영화 촬영장의 콘티와 같다. 장면을 실제로 편집하기 전에 촬영 기록을 먼저 남겨 두어야, 촬영 중 문제가 생겨도 어느 장면을 다시 찍을지 알 수 있다.

---

## Ⅲ. 비교 및 연결

로깅 엔진을 이해하려면 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]], 체크포인트, 버퍼 관리 [[164_policy|정책]]과 연결해서 봐야 한다. [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]은 최종 상태를 담고, [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]은 상태가 변해 가는 과정을 담는다. 체크포인트는 이 둘 사이의 [[658_ir_recovery|복구]] 출발선을 줄여 주는 장치다.

| 항목 | [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]] | [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]] |
| :--- | :--- | :--- |
| 기록 내용 | 변경 이력 | 최종 [[286_page_frame|페이지]] 상태 |
| [[289_cqrs_db|쓰기]] 패턴 | 순차 [[289_cqrs_db|쓰기]] | 랜덤 [[289_cqrs_db|쓰기]] 가능 |
| 커밋 관여 | 직접적 | 간접적 |
| 장애 [[658_ir_recovery|복구]] 역할 | [[234_redo_roll_forward_durability_recovery|Redo]]/[[393_undo|Undo]] 근거 | [[658_ir_recovery|복구]] 대상 원본 |

또한 DBMS의 Steal/No-Steal, Force/No-Force [[164_policy|정책]]과도 직결된다. 현대 상용 DBMS는 대개 **Steal + No-Force** [[164_policy|정책]]을 쓰므로, 미커밋 변경이 [[286_page_frame|페이지]]에 반영될 수 있고 커밋 직후에도 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]는 디스크에 없을 수 있다. 이런 [[164_policy|정책]]이 가능하려면 로깅 엔진이 Undo와 Redo를 모두 감당해야 한다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]이 완성된 가계부라면, [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]은 계산 과정을 적은 메모지다. 가계부만 보면 현재 잔액은 알 수 있지만, 메모지가 있어야 어디서 잘못됐는지 추적할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 로깅 엔진은 단순히 "[[568_logs_distributed_logging_elk_fluentd|로그]]를 남긴다" 수준이 아니라 커밋 [[141_latency|지연 시간]]과 [[658_ir_recovery|복구]] 시간의 균형을 잡는 문제다. [[568_logs_distributed_logging_elk_fluentd|로그]]를 너무 자주 flush하면 안전하지만 TPS가 떨어지고, 체크포인트를 너무 늦게 잡으면 평소 [[282_performance_tactics|성능]]은 좋아도 장애 후 [[658_ir_recovery|복구]] 시간이 길어진다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[568_logs_distributed_logging_elk_fluentd|로그]] 저장 장치는 순차 [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]]과 fsync [[282_performance_tactics|성능]]이 충분한가?
2. 체크포인트 주기가 장애 [[658_ir_recovery|복구]] 목표 시간 ([[176_rto_recovery_time_objective|RTO]]) 안에 드는가?
3. 그룹 커밋 (Group Commit)으로 커밋 flush 비용을 묶고 있는가?
4. 장기 [[191_transaction_concept_states|트랜잭션]]이 [[393_undo|Undo]] 구간을 과도하게 늘리지 않는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]]를 먼저 쓰고 [[568_logs_distributed_logging_elk_fluentd|로그]]를 나중에 쓰는 구현
- [[568_logs_distributed_logging_elk_fluentd|로그]]와 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]을 같은 병목 장치에 몰아 넣어 flush [[015_지연_데이터_관점|지연]]을 키우는 운영
- 체크포인트 간격을 무한정 늘려 장애 후 [[234_redo_roll_forward_durability_recovery|Redo]] 범위를 과도하게 키우는 운영

장애가 발생하면 보통 분석 (Analysis) → [[234_redo_roll_forward_durability_recovery|Redo]] → [[393_undo|Undo]] 순으로 [[658_ir_recovery|복구]]한다. 따라서 로깅 엔진 튜닝은 정상 시 [[282_performance_tactics|성능]]만 볼 게 아니라, 장애 시 얼마나 빨리 일관 상태로 돌아오는지도 함께 봐야 한다.

- **📢 섹션 요약 비유**: 로깅 엔진 튜닝은 가게 마감 정리와 같다. 낮에 너무 꼼꼼히만 적으면 장사가 느려지고, 정리를 미루기만 하면 문 닫을 때 엄청 오래 걸린다.

---

## Ⅴ. 기대효과 및 결론

로깅 엔진의 가장 큰 효과는 커밋의 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 낮은 비용으로 확보한다는 점이다. 순차 [[568_logs_distributed_logging_elk_fluentd|로그]] 기록은 랜덤 [[001_dikw_pyramid|데이터]] [[286_page_frame|페이지]] 기록보다 훨씬 효율적이어서, DBMS는 높은 [[139_throughput|처리량]]을 유지하면서도 장애 이후 [[658_ir_recovery|복구]] 경로를 확보할 수 있다.

반대로 [[568_logs_distributed_logging_elk_fluentd|로그]] 설계가 약하면 [[002_database_definition|데이터베이스]]는 [[282_performance_tactics|성능]]도 잃고 [[658_ir_recovery|복구]] 가능성도 잃는다. 따라서 로깅 엔진은 "[[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 남기는 기능"이 아니라 "DB가 장애를 견디도록 만드는 생존 핵심"으로 기억해야 한다.

- **📢 섹션 요약 비유**: 로깅 엔진은 비행기의 블랙박스와 같다. 평소엔 잘 보이지 않지만, 사고가 났을 때 시스템을 다시 살릴 단서를 남겨 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 버퍼 풀 (Buffer Pool) | [[286_page_frame|페이지]]가 먼저 수정되는 메모리 계층 |
| WAL ([[236_wal_write_ahead_logging_protocol|Write-Ahead Logging]]) | 로깅 엔진의 핵심 규칙 |
| 체크포인트 (Checkpoint) | [[658_ir_recovery|복구]] 시작 범위를 줄이는 장치 |
| ARIES | [[234_redo_roll_forward_durability_recovery|Redo]]/[[393_undo|Undo]] 기반 대표 [[658_ir_recovery|복구]] [[001_algorithm_definition|알고리즘]] |
| 그룹 커밋 (Group Commit) | 여러 커밋의 [[568_logs_distributed_logging_elk_fluentd|로그]] flush를 묶어 최적화 |

### 📈 관련 키워드 및 발전 흐름도

```text
버퍼 풀 기반 갱신
    │
    ▼
WAL (Write-Ahead Logging)
    │
    ▼
LSN · Redo · Undo
    │
    ▼
체크포인트 (Checkpoint)
    │
    ▼
ARIES · 그룹 커밋 · 분산 로그 복제
```

이 흐름은 "단순 [[568_logs_distributed_logging_elk_fluentd|로그]] 기록"이 "고성능 [[658_ir_recovery|복구]] 아키텍처"로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 로깅 엔진은 물건을 옮기기 전에 메모장에 먼저 적는 습관이에요.
2. 나중에 불이 꺼져도 메모장을 보면 어디에 무엇을 놓아야 했는지 다시 알 수 있어요.
3. 그래서 컴퓨터는 갑자기 멈춰도 중요한 기록을 다시 찾아낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 51 / 600

← **이전**: [[050_buffer_pool_manager|버퍼 풀 매니저 (Buffer Pool Manager)]]
**다음**: [[052_db_optimizer_rbo_cbo|52. 옵티마이저 (Optimizer) - 최적의 SQL 실행 계획 생성]] →

---
