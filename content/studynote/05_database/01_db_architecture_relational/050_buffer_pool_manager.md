+++
title = "버퍼 풀 매니저 (Buffer Pool Manager)"
description = "DBMS 버퍼 풀 매니저의 페이지 교체 정책(LRU, Clock), 더티 페이지 플러시, InnoDB 버퍼 풀 구조를 다룬다."
date = 2025-01-01

[taxonomies]
tags = ["DBMS", "InnoDB", "LRU", "WAL", "buffer pool", "clock algorithm", "dirty page", "page replacement", "studynote-db"]

[extra]
tags = ["DBMS", "InnoDB", "LRU", "WAL", "buffer pool", "clock algorithm", "dirty page", "page replacement", "studynote-db"]
+++

> **핵심 인사이트 3줄**
> 1. 버퍼 풀(Buffer Pool)은 디스크 I/O를 줄이기 위해 자주 접근하는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 메모리에 캐시하는 DBMS의 핵심 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)다.
> 2. [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)([Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 가장 오랫동안 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되지 않은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 교체하며, InnoDB는 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 리스트를 Young/Old 영역으로 나눠 풀 스캔에 의한 캐시 오염을 방지한다.
> 3. 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(Dirty [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))는 수정됐지만 아직 디스크에 기록되지 않은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)로, WAL([Write-Ahead Logging](/knowledge-base/studynote/05_database/04_transactions_concurrency/236_wal_write_ahead_logging_protocol/))과 체크포인트가 지속성을 보장한다.

---

## Ⅰ. 버퍼 풀의 역할과 구조

### 1.1 메모리-디스크 계층



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SQL 쿼리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">버퍼 풀 (Buffer Pool, 메모리)</div>
<div class="kb-diagram-tree-item" style="--depth:1">페이지 테이블 (page table): page_id → frame_id</div>
<div class="kb-diagram-tree-item" style="--depth:1">free list: 빈 프레임 목록</div>
<div class="kb-diagram-tree-item" style="--depth:1">LRU list: Young(Hot) | Old(Cold) 영역</div>
<div class="kb-diagram-tree-item" style="--depth:1">flush list: 더티 페이지 목록</div>
<div class="kb-diagram-note">↕ (miss 시 디스크 I/O)</div>
<div class="kb-diagram-note">데이터 파일 (.ibd)</div>
</div>
</div>



### 1.2 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 요청 흐름

1. [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)에서 page_id 조회 → <strong>히트(<a href="/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/">hit</a>)</strong>: 프레임 반환
2. **미스(miss)**: free list에서 프레임 확보 → 디스크에서 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 로드 → [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 리스트 삽입

📢 **섹션 요약 비유**: 버퍼 풀은 사서가 자주 빌리는 책을 책상 서랍(메모리)에 모아두는 것 — 서랍에 없으면 서고(디스크)에서 꺼내온다.

---

## Ⅱ. [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/)

### 2.1 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) ([Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">접근 순서: A B C D → A 참조</div>
<div class="kb-diagram-note">LRU 리스트 (왼쪽=MRU, 오른쪽=LRU):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">초기:</div><div class="kb-diagram-node">D, C, B, A</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">A 참조:</div><div class="kb-diagram-node">A, D, C, B</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">A가 앞으로 이동</div></div>
<div class="kb-diagram-note">교체 필요 시: B (가장 오른쪽) 교체</div>
</div>
</div>



### 2.2 InnoDB의 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 변형

```
Young 영역 (5/8)    | Old 영역 (3/8)
[최근 접근 페이지]  | [새로 로드된 페이지]
                    ↑ midpoint
```

- 새 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 Old 영역으로 삽입 (풀 스캔 오염 방지)
- Old 영역에서 1초 이상 후 재접근 시 Young 영역으로 승격

### 2.3 [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">프레임을 원형으로 배치, reference bit 사용:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">A:1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">B:0</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">C:1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">D:0</div><div class="kb-diagram-note">...</div></div>
<div class="kb-diagram-note">↑ clock hand</div>
</div>
</div>



- [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 접근 시 [reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) = 1
- 교체 시 [clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) hand 이동: [bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)=1이면 0으로 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 후 통과, [bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)=0이면 교체

📢 **섹션 요약 비유**: LRU는 마지막으로 쓴 시간 기록, Clock은 한 바퀴 돌면서 최근 안 쓴 자리 차지.

---

## Ⅲ. 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)와 플러시 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)

### 3.1 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 관리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">페이지 읽기 → 수정 → dirty bit = 1 → flush list 등록</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">체크포인트 발생 시</div>
<div class="kb-diagram-note">또는 free list 부족 시</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">디스크 플러시 (write)</div>
</div>
</div>



### 3.2 플러시 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)

| [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)              | 설명                              |
|--------------------|-----------------------------------|
| 체크포인트(Checkpoint) | 주기적으로 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 디스크에 기록 |
| [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 플러시          | 교체 대상 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 더티인 경우 즉시 기록 |
| 백그라운드 플러시    | [page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) cleaner [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 주기적 기록    |
| 강제 플러시(Force)   | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 커밋 시 (innodb_flush_log_at_trx_commit) |

📢 **섹션 요약 비유**: 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 아직 제출 안 한 과제 — 선생님(체크포인트)이 올 때까지 책상 서랍에 있지만, 자리 필요하면 먼저 제출해야 한다.

---

## Ⅳ. WAL과 버퍼 풀의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

### 4.1 [Write-Ahead Logging](/knowledge-base/studynote/05_database/04_transactions_concurrency/236_wal_write_ahead_logging_protocol/) 원칙

1. <strong>수정 전 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 먼저</strong>: [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 디스크에 플러시하기 전에 WAL([리두](/knowledge-base/studynote/05_database/07_exam_summary/455_redo_log_archive/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))에 먼저 기록.
2. <strong>STEAL/FORCE <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>:
   - STEAL: 커밋 전 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 플러시 허용 (버퍼 풀 공간 확보)
   - NO-FORCE: 커밋 시 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 직접 기록 불필요 ([리두](/knowledge-base/studynote/05_database/07_exam_summary/455_redo_log_archive/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 가능)

### 4.2 크래시 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">크래시 발생</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">InnoDB 재시작</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">리두 로그 분석(Analysis) → 리두(Redo) → 언두(Undo)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">버퍼 풀 정상 복구</div>
</div>
</div>



📢 **섹션 요약 비유**: WAL은 일기([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))를 먼저 쓰고 행동하는 것 — 사고가 나도 일기를 보면 어디까지 했는지 알 수 있다.

---

## Ⅴ. InnoDB 버퍼 풀 튜닝

### 5.1 주요 파라미터

| 파라미터                          | 기본값  | 설명                          |
|----------------------------------|---------|-------------------------------|
| innodb_buffer_pool_size          | 128MB   | 버퍼 풀 총 크기 (서버 RAM의 70~80% 권장) |
| innodb_buffer_pool_instances     | 8       | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 접근을 위한 인스턴스 수  |
| innodb_old_blocks_pct            | 37%     | Old 영역 비율                 |
| innodb_old_blocks_time           | 1000ms  | Old→Young 승격 대기 시간      |
| innodb_page_cleaners             | 4       | 플러시 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수               |

### 5.2 히트율 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링

```sql
SHOW STATUS LIKE 'Innodb_buffer_pool%';
-- Innodb_buffer_pool_read_requests / Innodb_buffer_pool_reads
-- 히트율 = (read_requests - reads) / read_requests × 100
-- 목표: 99% 이상
```

📢 **섹션 요약 비유**: 히트율 99%는 100번 요청 중 99번은 메모리에서 바로 꺼낸다는 것 — 1번만 서고(디스크)에 간다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">버퍼 풀 매니저</div>
<div class="kb-diagram-tree-item" style="--depth:0">페이지 교체 정책</div>
<div class="kb-diagram-note">── LRU</div>
<div class="kb-diagram-note">── InnoDB Young/Old LRU</div>
<div class="kb-diagram-note">── Clock 알고리즘</div>
<div class="kb-diagram-tree-item" style="--depth:0">더티 페이지 관리</div>
<div class="kb-diagram-note">── 체크포인트</div>
<div class="kb-diagram-note">── WAL (Write-Ahead Log)</div>
<div class="kb-diagram-note">── 크래시 복구 (Redo/Undo)</div>
<div class="kb-diagram-tree-item" style="--depth:0">튜닝 포인트</div>
<div class="kb-diagram-tree-item" style="--depth:2">버퍼 풀 크기</div>
<div class="kb-diagram-tree-item" style="--depth:2">인스턴스 수</div>
<div class="kb-diagram-tree-item" style="--depth:2">히트율 모니터링</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">초기 DBMS: 더블 버퍼링 (1970s)</div>
<div class="kb-diagram-note">LRU 알고리즘 도입</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">전통적 버퍼 매니저 (STEAL/NO-FORCE + WAL)</div>
<div class="kb-diagram-note">풀 스캔 오염 문제</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">InnoDB Young/Old LRU (MySQL 5.x)</div>
<div class="kb-diagram-note">대용량 메모리 대응</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">멀티 인스턴스 버퍼 풀 (MySQL 5.5+)</div>
<div class="kb-diagram-note">NVM/PMEM 등장</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">영속 버퍼 풀 (Persistent Buffer Pool, MySQL 5.7+)</div>
<div class="kb-diagram-note">재시작 후 워밍업 없이 히트율 유지</div>
</div>
</div>



**핵심 키워드**: [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/), 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/), WAL, 체크포인트, STEAL, NO-FORCE, 히트율

---

## 👶 어린이를 위한 3줄 비유 설명

1. 버퍼 풀은 도서관 사서의 책상 서랍 — 자주 빌리는 책을 미리 꺼내놔서 빠르게 빌려줘.
2. 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 내용을 고쳤지만 아직 반납 안 한 책 — 나중에 선생님(체크포인트)이 모아서 공식 기록에 반영해.
3. WAL은 "먼저 일기 쓰고 행동" 규칙 — 갑자기 전기가 나가도 일기를 보면 어디까지 했는지 알 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 50 / 600

← **이전**: [049. 스토리지 엔진 — InnoDB vs MyISAM](/knowledge-base/studynote/05_database/01_db_architecture_relational/049_storage_engine_innodb_myisam/)
**다음**: [51. 로깅 엔진 (Logging Engine)](/knowledge-base/studynote/05_database/01_db_architecture_relational/051_logging_engine_wal_redo_undo/) →

---
