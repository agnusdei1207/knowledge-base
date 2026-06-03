---
title: 58. 데이터베이스 인스턴스 (Database Instance) - 메모리와 백그라운드 프로세스
tags:
- database
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[002_database_definition|데이터베이스]] 인스턴스([[501_database|Database]] Instance)는 메모리 구조와 백그라운드 프로세스의 결합체다.
> 2. **가치**: 인스턴스가 있어야 디스크의 [[002_database_definition|데이터베이스]] [[501_file_definition_logical_record|파일]]이 실제 [[090_service_kubernetes_network_load_balancing|서비스]]로 동작한다.
> 3. **판단 포인트**: SGA (System Global Area), [[536_buffer_cache_page_cache|버퍼 캐시]], [[455_redo_log_archive|리두]] [[568_logs_distributed_logging_elk_fluentd|로그]], 백그라운드 프로세스의 역할을 분리해서 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

[[002_database_definition|데이터베이스]] [[501_file_definition_logical_record|파일]]은 디스크에 저장된 정적인 자산이다. 반면 인스턴스는 그 [[501_file_definition_logical_record|파일]]을 움직이게 하는 살아 있는 실행 환경이다.

즉, [[002_database_definition|데이터베이스]]는 "저장된 내용"이고, 인스턴스는 "그 내용을 읽고 쓰는 힘"이다.

- **📢 섹션 요약 비유**: 책장은 [[002_database_definition|데이터베이스]]이고, 책장을 읽고 정리하는 사서와 불이 인스턴스다.

---

## Ⅱ. 메모리 구조

[[188_pl_sql_t_sql_procedural|Oracle]] 계열 DB를 기준으로 보면 인스턴스의 핵심 메모리는 SGA (System Global Area)다.

- **[[536_buffer_cache_page_cache|Buffer Cache]]**: 실제 [[001_dikw_pyramid|데이터]] 블록을 담는다.
- **[[057_shared_pool_oracle_sga|Shared Pool]]**: SQL과 [[012_metadata|메타데이터]]를 재사용한다.
- **[[234_redo_roll_forward_durability_recovery|Redo]] Log Buffer**: 변경 이력을 임시 저장한다.

이 메모리 구조가 있어야 빠른 조회와 [[658_ir_recovery|복구]]가 가능하다.

- **📢 섹션 요약 비유**: 작업대, 참고서, 메모장을 한 책상에 나눠 둔 구조다.

---

## Ⅲ. 백그라운드 프로세스

인스턴스는 여러 백그라운드 프로세스가 함께 움직여야 완성된다.

- **DBWR ([[501_database|Database]] Writer)**: 수정된 [[001_dikw_pyramid|데이터]]를 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]에 쓴다.
- **LGWR (Log Writer)**: [[455_redo_log_archive|리두]] [[568_logs_distributed_logging_elk_fluentd|로그]]를 기록한다.
- **SMON (System [[229_monitor|Monitor]])**: 장애 후 [[658_ir_recovery|복구]]를 돕는다.
- **PMON ([[300_process|Process]] [[229_monitor|Monitor]])**: 죽은 [[160_session_controlling_terminal|세션]]과 자원을 정리한다.
- **CKPT (Checkpoint)**: 체크포인트 정보를 맞춘다.
- **ARCH (Archiver)**: 아카이브 [[568_logs_distributed_logging_elk_fluentd|로그]]를 만든다.

각 프로세스는 서로 다른 일을 하지만, 함께 있어야 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]과 [[658_ir_recovery|복구]]가 유지된다.

- **📢 섹션 요약 비유**: 한 공장에서 재료 운반, 기록, 청소, 점검을 맡은 각기 다른 일꾼들이다.

---

## Ⅳ. 기동과 [[658_ir_recovery|복구]] 흐름

인스턴스는 시작되면 메모리를 잡고 백그라운드 프로세스를 띄운다. 그 뒤 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]을 열어 [[090_service_kubernetes_network_load_balancing|서비스]]가 가능해진다.

```text
Instance 시작
   ↓
메모리 할당
   ↓
백그라운드 프로세스 기동
   ↓
Database 열기
```

장애가 나면 [[568_logs_distributed_logging_elk_fluentd|로그]]와 체크포인트 정보를 이용해 [[658_ir_recovery|복구]]를 수행한다.

- **📢 섹션 요약 비유**: 전기가 나갔다가 다시 켜지면, 작업 현장을 정리하고 다시 일을 시작하는 과정이다.

---

## Ⅴ. 실무 비교와 운영 관점

[[002_database_definition|데이터베이스]] 인스턴스를 이해하면 "왜 DB가 느려졌는가", "왜 [[658_ir_recovery|복구]]가 안 되는가"를 훨씬 잘 설명할 수 있다.

중요한 것은 [[501_file_definition_logical_record|파일]]만 보는 것이 아니라, 메모리와 프로세스가 정상적으로 함께 움직이는지 [[396_validation|확인]]하는 일이다.

- **📢 섹션 요약 비유**: 자동차 바퀴만 봐서는 안 되고, 엔진과 연료까지 함께 봐야 차가 달린다.

---

## 관련 개념 맵

```text
Database 파일
   ↓
Instance
   ├─ SGA
   └─ Background Processes
   ↓
서비스 동작 / 복구
```

---

## 관련 키워드 및 발전 흐름도

1. [[002_database_definition|데이터베이스]] [[501_file_definition_logical_record|파일]] → 저장 중심
2. 인스턴스 → 실행 중심
3. SGA → 메모리 관리
4. 백그라운드 프로세스 → [[194_consistency_database_integrity|일관성]] / [[658_ir_recovery|복구]]
5. 체크포인트와 [[568_logs_distributed_logging_elk_fluentd|로그]] → 장애 [[658_ir_recovery|복구]] 체계

---

## 어린이를 위한 3줄 비유 설명

[[002_database_definition|데이터베이스]]는 책장에 꽂힌 책이에요.  
인스턴스는 그 책을 읽고 정리하는 사서예요.  
사서가 있어야 책이 실제로 쓰여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 600

← **이전**: [[057_shared_pool_oracle_sga|57. 공유 풀 (Shared Pool) - Oracle 인스턴스 구조]]
**다음**: [[059_persistent_storage_data_log_control_file|59. 영구 저장소 (Persistent Storage) - 데이터 파일, 로그 파일, 제어 파일]] →

---
