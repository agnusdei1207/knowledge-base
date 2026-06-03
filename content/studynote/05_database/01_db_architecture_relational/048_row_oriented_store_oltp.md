+++
title = "048. 행 지향 저장소 — Row-Oriented Store & OLTP"
date = 2026-04-05

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

> **핵심 인사이트**
> 1. 행 지향 저장소(Row-Oriented Store)는 한 행의 모든 컬럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 연속 저장 — 특정 행의 전체 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 한 번에 읽는 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)(Online [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) Processing) 워크로드에 최적화되어 있으며, INSERT/UPDATE/DELETE 시 단일 I/O로 행 전체를 처리한다.
> 2. OLTP와 OLAP는 완전히 다른 최적화 방향 — OLTP는 행 지향(단일 행 빠른 접근), OLAP는 컬럼 지향(대용량 컬럼 집계). 같은 물리적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 두 방향으로 저장하는 [HTAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/)(Hybrid)가 현대 트렌드다.
> 3. 버퍼 풀(Buffer Pool)이 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심 — 행 지향 DB의 메인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 메커니즘은 자주 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 메모리에 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)하는 버퍼 풀이며, 버퍼 풀 히트율 99% 이상이 고성능 OLTP의 목표다.

---

## Ⅰ. 행 지향 저장소 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">행 지향 (Row-Oriented) 저장:</div>
<div class="kb-diagram-note">테이블 데이터:</div>
<div class="kb-diagram-note">ID 이름 연봉 부서</div>
<div class="kb-diagram-note">1 김철수 5000 개발</div>
<div class="kb-diagram-note">2 이영희 6000 마케팅</div>
<div class="kb-diagram-note">3 박민수 4500 개발</div>
<div class="kb-diagram-note">디스크 저장 순서:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1|김철수|5000|개발</div><div class="kb-diagram-node">2|이영희|6000|마케팅</div><div class="kb-diagram-node">3|박민수|4500|개발</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">1페이지(8KB)</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">한 행의 모든 컬럼 = 연속된 바이트</div>
<div class="kb-diagram-note">행 단위 I/O = 페이지 1번 읽어 전체 컬럼 접근</div>
<div class="kb-diagram-note">OLTP에서의 장점:</div>
<div class="kb-diagram-note">SELECT * WHERE id = 1</div>
<div class="kb-diagram-note">→ 행 1 포함 페이지 1개만 읽기 (빠름)</div>
<div class="kb-diagram-note">UPDATE salary WHERE id = 1</div>
<div class="kb-diagram-note">→ 행 1 포함 페이지 읽기 → 수정 → 쓰기</div>
<div class="kb-diagram-note">OLAP에서의 단점:</div>
<div class="kb-diagram-note">SELECT SUM(연봉) FROM employees</div>
<div class="kb-diagram-note">→ 모든 행 전체 컬럼 읽기 (이름, 부서 불필요)</div>
<div class="kb-diagram-note">→ 불필요한 컬럼 I/O 발생</div>
<div class="kb-diagram-note">페이지 구조 (MySQL InnoDB):</div>
<div class="kb-diagram-note">페이지 크기: 16KB (기본)</div>
<div class="kb-diagram-note">페이지 내 구조:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">페이지 헤더</div><div class="kb-diagram-node">행1</div><div class="kb-diagram-node">행2</div><div class="kb-diagram-note">...</div><div class="kb-diagram-node">행N</div><div class="kb-diagram-node">빈 공간</div><div class="kb-diagram-node">페이지 디렉토리</div><div class="kb-diagram-node">페이지 트레일러</div></div>
<div class="kb-diagram-note">가득 찬 페이지(Fill Factor ~87%):</div>
<div class="kb-diagram-note">INSERT 공간 부족 → 페이지 분할 (Page Split)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 행 지향 = 서랍 한 칸에 한 사람 정보 — "김철수" 서랍엔 이름+연봉+부서 한 번에. 한 명 정보 꺼낼 때([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) 빠름. 전체 연봉 합산([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)) 땐 모든 서랍 열어야 해서 느림!

---

## Ⅱ. [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 특성과 최적화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OLTP (Online Transaction Processing):</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">짧고 빠른 트랜잭션 (&lt; 100ms)</div>
<div class="kb-diagram-note">대량의 동시 사용자 (수천~수만)</div>
<div class="kb-diagram-note">단일 행 또는 소수 행 접근</div>
<div class="kb-diagram-note">INSERT/UPDATE/DELETE 빈번</div>
<div class="kb-diagram-note">ACID 트랜잭션 필수</div>
<div class="kb-diagram-note">워크로드 예:</div>
<div class="kb-diagram-note">은행 계좌 이체</div>
<div class="kb-diagram-note">전자상거래 주문 처리</div>
<div class="kb-diagram-note">좌석 예약 시스템</div>
<div class="kb-diagram-note">재고 관리</div>
<div class="kb-diagram-note">OLTP 최적화 기법:</div>
<div class="kb-diagram-note">1. 버퍼 풀 (Buffer Pool):</div>
<div class="kb-diagram-note">자주 접근하는 페이지 메모리 캐싱</div>
<div class="kb-diagram-note">히트율 = 메모리에서 직접 읽기 비율</div>
<div class="kb-diagram-note">목표: 99%+ 히트율</div>
<div class="kb-diagram-note">LRU 알고리즘으로 페이지 교체</div>
<div class="kb-diagram-note">버퍼 풀 크기 = 물리 메모리 × 70~80%</div>
<div class="kb-diagram-note">2. 인덱스 (Index):</div>
<div class="kb-diagram-note">B+ 트리 인덱스: 범위 검색 효율</div>
<div class="kb-diagram-note">복합 인덱스: 자주 쓰는 WHERE 컬럼 조합</div>
<div class="kb-diagram-note">쓰기 오버헤드:</div>
<div class="kb-diagram-note">INSERT 1건 → 인덱스 수 × 2 I/O 추가</div>
<div class="kb-diagram-note">3. 연결 풀 (Connection Pool):</div>
<div class="kb-diagram-note">DB 연결 생성 비용 절감</div>
<div class="kb-diagram-note">PgBouncer, HikariCP</div>
<div class="kb-diagram-note">4. 파티셔닝:</div>
<div class="kb-diagram-note">날짜 범위 파티션</div>
<div class="kb-diagram-note">오래된 파티션 DROP → 빠른 삭제</div>
<div class="kb-diagram-note">5. 읽기 복제본 (Read Replica):</div>
<div class="kb-diagram-note">Write → Primary</div>
<div class="kb-diagram-note">Read → Replica (SELECT 부하 분산)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 최적화 = 편의점 운영 — 잘 팔리는 물건(버퍼 풀: 자주 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시), 빠른 검색([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)), 여러 계산대(연결 풀), 창고 분리([파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/))!

---

## Ⅲ. [OLTP vs OLAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 비교

```
비교표:
  특성          | OLTP                | OLAP
  -------------|---------------------|-------------------
  목적         | 업무 처리           | 분석, 의사결정
  쿼리 유형    | 단순 DML/PK 조회   | 복잡 집계, JOIN
  행 접근      | 수~수십 행          | 수백만~수십억 행
  응답 시간    | 밀리초              | 초~분
  동시 사용자  | 수천~수만           | 수십~수백
  데이터 갱신  | 실시간 (빈번)       | 배치 (드문)
  최적화       | 행 지향 저장        | 컬럼 지향 저장
  대표 DB      | MySQL, PostgreSQL    | Snowflake, BigQuery
  트랜잭션     | ACID 필수           | 완화 가능

HTAP (Hybrid Transaction/Analytical Processing):
  단일 DB에서 OLTP + OLAP 동시 처리
  
  기술:
  인메모리 컬럼 저장소:
  TiDB: RocksDB(OLTP) + TiFlash(OLAP)
  MySQL HeatWave: InnoDB + 컬럼 가속기
  SQL Server: In-Memory OLTP + Columnstore
  
  장점:
  ETL 불필요 (OLTP DB에서 직접 분석)
  데이터 신선도: 실시간 분석
  
  단점:
  자원 경합 (OLTP-OLAP I/O 충돌)
  복잡한 운영

실제 아키텍처 선택:
  소규모: HTAP 가능 (MySQL HeatWave)
  중규모: OLTP DB + 야간 ETL + OLAP DB (Redshift)
  대규모: OLTP (Aurora) + 스트리밍 CDC + 실시간 OLAP (ClickHouse)
```

> 📢 **섹션 요약 비유**: [OLTP vs OLAP](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) = 편의점 POS vs 마케팅 분석팀 — POS([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/))는 1건 빠르게 처리, 마케팅([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/))은 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 집계. HTAP은 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 두 가지 모두!

---

## Ⅳ. InnoDB 행 지향 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">MySQL InnoDB 행 저장 상세:</div>
<div class="kb-diagram-note">B+ 트리 클러스터드 인덱스:</div>
<div class="kb-diagram-note">기본 키 순서로 행 저장</div>
<div class="kb-diagram-note">장점: PK 기반 검색 = 인덱스 + 데이터 1번 I/O</div>
<div class="kb-diagram-note">단점: 무작위 PK INSERT = 페이지 분할 빈번</div>
<div class="kb-diagram-note">물리적 행 형식 (COMPACT):</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">삭제 플래그 1비트</div><div class="kb-diagram-node">레코드 타입</div><div class="kb-diagram-node">N-byte 포인터</div><div class="kb-diagram-node">NULL 비트맵</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">가변 길이 컬럼 오프셋 목록</div><div class="kb-diagram-node">컬럼1</div><div class="kb-diagram-node">컬럼2</div><div class="kb-diagram-note">...</div><div class="kb-diagram-node">컬럼N</div></div>
<div class="kb-diagram-note">가변 길이 컬럼 (VARCHAR):</div>
<div class="kb-diagram-note">데이터 앞에 실제 길이 저장</div>
<div class="kb-diagram-note">VARCHAR(255) → 최대 1바이트 오프셋</div>
<div class="kb-diagram-note">VARCHAR(65535) → 최대 2바이트 오프셋</div>
<div class="kb-diagram-note">페이지 분할 (Page Split):</div>
<div class="kb-diagram-note">B+ 트리 노드 가득 참 → 분할</div>
<div class="kb-diagram-note">순서 INSERT (PK 1, 2, 3, ...): 분할 적음</div>
<div class="kb-diagram-note">무작위 INSERT (UUID): 잦은 분할 → 성능 저하</div>
<div class="kb-diagram-note">해결: UUID v7 (시간 순서 보장)</div>
<div class="kb-diagram-note">또는 AUTO_INCREMENT + 순서 삽입</div>
<div class="kb-diagram-note">MVCC (Multi-Version Concurrency Control):</div>
<div class="kb-diagram-note">행 변경 시 기존 행 삭제 안 함</div>
<div class="kb-diagram-note">행에 trx_id, roll_pointer 포함</div>
<div class="kb-diagram-note">읽기: 자신의 트랜잭션 시작 전 버전 읽기</div>
<div class="kb-diagram-note">Undo Log: 이전 버전 저장 공간</div>
<div class="kb-diagram-note">장기 트랜잭션 → Undo Log 급증 → 성능 저하</div>
</div>
</div>



> 📢 **섹션 요약 비유**: InnoDB 행 저장 = [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 캐비닛 정리 — PK 순서로 서랍([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)) 정렬. UUID로 랜덤 저장하면 서랍 분할([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Split) 잦아 혼란. 순서대로 넣어야 빠름!

---

## Ⅴ. 실무 시나리오 — 전자상거래 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 최적화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전자상거래 주문 시스템 OLTP 튜닝:</div>
<div class="kb-diagram-note">현황:</div>
<div class="kb-diagram-note">MySQL 8.0 (InnoDB)</div>
<div class="kb-diagram-note">초당 주문: 1,000건</div>
<div class="kb-diagram-note">평균 응답: 250ms (목표 50ms)</div>
<div class="kb-diagram-note">슬로우 쿼리:</div>
<div class="kb-diagram-note">SELECT * FROM orders WHERE user_id = ? AND status = 'pending'</div>
<div class="kb-diagram-note">→ 200ms (풀 스캔)</div>
<div class="kb-diagram-note">분석:</div>
<div class="kb-diagram-note">orders 테이블: 5천만 행</div>
<div class="kb-diagram-note">인덱스: PK (order_id) 만 존재</div>
<div class="kb-diagram-note">쿼리 플랜:</div>
<div class="kb-diagram-note">→ type: ALL (풀 테이블 스캔!)</div>
<div class="kb-diagram-note">→ rows: 50,000,000 (전체 스캔)</div>
<div class="kb-diagram-note">최적화:</div>
<div class="kb-diagram-note">1. 복합 인덱스 추가:</div>
<div class="kb-diagram-note">CREATE INDEX idx_user_status</div>
<div class="kb-diagram-note">ON orders (user_id, status, created_at DESC);</div>
<div class="kb-diagram-note">쿼리 플랜 재확인:</div>
<div class="kb-diagram-note">→ type: ref (인덱스 사용)</div>
<div class="kb-diagram-note">→ rows: 15 (극적 감소)</div>
<div class="kb-diagram-note">응답: 200ms → 8ms ✓</div>
<div class="kb-diagram-note">2. 버퍼 풀 증설:</div>
<div class="kb-diagram-note">innodb_buffer_pool_size = 4G → 12G</div>
<div class="kb-diagram-note">히트율: 92% → 99.3%</div>
<div class="kb-diagram-note">3. 읽기 복제본 추가:</div>
<div class="kb-diagram-note">주문 조회 API → 복제본으로 라우팅</div>
<div class="kb-diagram-note">Primary 쓰기 부하 40% 감소</div>
<div class="kb-diagram-note">4. Connection Pool 최적화:</div>
<div class="kb-diagram-note">HikariCP maxPoolSize = 50 → 100</div>
<div class="kb-diagram-note">connectionTimeout = 30s → 5s</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">평균 응답: 250ms → 35ms (7배 개선)</div>
<div class="kb-diagram-note">P99: 800ms → 120ms</div>
<div class="kb-diagram-note">TPS: 1,000 → 3,500</div>
<div class="kb-diagram-note">교훈:</div>
<div class="kb-diagram-note">인덱스 설계가 OLTP 성능의 80% 결정</div>
<div class="kb-diagram-note">버퍼 풀 크기 = 활성 데이터 셋 크기가 이상적</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) 튜닝 결과 — [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 없어서 5천만 행 전체 스캔(200ms)! 복합 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 추가로 15행만 읽기(8ms). [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 하나로 25배 빠르게. OLTP는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계가 90%!

---

## 📌 관련 개념 맵

```
행 지향 저장소 / OLTP
+-- 저장 구조
|   +-- 행 단위 연속 저장
|   +-- B+ 트리 클러스터드 인덱스
|   +-- 페이지 (8~16KB)
+-- OLTP 최적화
|   +-- 버퍼 풀 (Buffer Pool)
|   +-- 인덱스 설계
|   +-- Connection Pool
|   +-- 읽기 복제본
+-- 비교
|   +-- OLAP (컬럼 지향)
|   +-- HTAP (하이브리드)
+-- 대표 DB
    +-- MySQL InnoDB
    +-- PostgreSQL
    +-- Oracle
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[파일 기반 DB (1960s)]
레코드 순차 저장
행 지향의 원형
      |
      v
[관계형 DB (1970s)]
IBM System R
InnoDB 전신 페이지 구조
      |
      v
[OLTP 최적화 (1980~90s)]
버퍼 풀, B+ 트리 표준화
오라클, SQL Server
      |
      v
[인메모리 DB (2000s~)]
SAP HANA, VoltDB
RAM = 디스크 대체
      |
      v
[HTAP (2015~)]
TiDB, MySQL HeatWave
OLTP + OLAP 통합
      |
      v
[현재: 클라우드 OLTP]
Aurora, Cloud Spanner
서버리스 OLTP
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 행 지향 = 서랍 한 칸에 한 사람 정보 — 서랍 열면 이름+연봉+부서 한꺼번에. 한 명 찾을 때([OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)) 빠르고, 전체 연봉 합산([OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/))엔 느려요!
2. 버퍼 풀 = 책상 위 자주 쓰는 서류 — 자주 꺼내는 서랍([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))을 책상(메모리)에 올려두기. 99% 히트율 = 창고 안 가도 됨!
3. [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) = 목차 — 5천만 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 책에서 목차 없이 찾기(풀 스캔: 200ms) vs 목차로 찾기([인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/): 8ms). 25배 빠름!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 600

← **이전**: [047. 컬럼 기반 스토리지 — Columnar Store & OLAP](/knowledge-base/studynote/05_database/01_db_architecture_relational/047_columnar_store_olap/)
**다음**: [049. 스토리지 엔진 — InnoDB vs MyISAM](/knowledge-base/studynote/05_database/01_db_architecture_relational/049_storage_engine_innodb_myisam/) →

---
