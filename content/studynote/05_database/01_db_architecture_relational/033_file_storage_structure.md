+++
title = "파일 저장 구조 (File Storage Structure)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

> **핵심 인사이트 3줄**
> 1. DBMS의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장 구조는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 물리적으로 디스크에 배치하는 방식으로, 순차·힙·해시·클러스터 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 구조에 따라 I/O 패턴이 크게 달라진다.
> 2. [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)([Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)) / 블록(Block)이 DBMS의 최소 I/O 단위이며, 버퍼 풀(Buffer Pool)의 효율적 관리가 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심을 결정한다.
> 3. 행 지향(Row-Oriented) vs 열 지향(Column-Oriented) 스토리지의 선택은 [OLTP](/knowledge-base/studynote/05_database/06_dw_olap_trends/327_hint_handoff/)(랜덤 행 접근)와 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/)(컬럼 스캔) 워크로드 차이에 의해 결정된다.

---

## Ⅰ. [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장 계층 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SQL 쿼리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">쿼리 처리기 (파서→최적화기→실행기)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">스토리지 엔진</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">버퍼 풀 (Buffer Pool) — 메모리 캐시</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">디스크 I/O 관리자</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">운영체제 파일시스템</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">물리 디스크 (HDD/SSD/NVMe)</div>
</div>
</div>



### [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 구조 기본 단위

| 단위   | 크기           | 설명                          |
|------|--------------|-------------------------------|
| [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)   | 1 [bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)        | 최소 저장 단위                  |
| [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)  | 8 bits       | 문자 단위                       |
| 블록/[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 4KB~16KB  | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 최소 I/O 단위            |
| [익스텐트](/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/) | 1MB~8MB    | 연속 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음                 |
| 세그먼트 | 가변          | 테이블·[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 저장 공간           |

📢 **섹션 요약 비유**: [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 계층은 도서관 서랍 체계다 — 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), 선반([페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)), 책장 칸([익스텐트](/knowledge-base/studynote/02_operating_system/09_file_system/531_extent_allocation/)), 서재(세그먼트), 도서관([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)파일) 순으로 구성된다.

---

## Ⅱ. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 구조 유형

### 1. 힙 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))

```
레코드 삽입 → 파일 끝에 추가
순서: 무작위 (삽입 순서대로)
삽입: O(1)   탐색: O(n)   정렬 없음
```
→ 소규모 테이블, 전수 스캔 시 적합

### 2. 순차 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Sequential [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))

```
레코드: 정렬 키 순서로 물리적 배치
탐색: O(log n) (이진 탐색)
삽입: O(n) (정렬 유지 비용)
```
→ 범위 스캔·정렬된 출력에 유리

### 3. 해시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Hash [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))

```
h(key) = 버킷 번호
탐색: O(1) 평균   삽입: O(1)
단점: 범위 검색 불가, 오버플로우 처리 필요
```
→ 등호 조건(point query) 최적화

### 4. 클러스터 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) (Clustered [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">관련 테이블 레코드를 같은 페이지에 물리적으로 함께 저장</div>
<div class="kb-diagram-note">예: 주문 + 주문상세 → 같은 블록에 저장</div>
<div class="kb-diagram-note">→ JOIN 성능 향상</div>
</div>
</div>



📢 **섹션 요약 비유**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 구조 유형은 서랍 정리 방식이다 — 힙은 그냥 던져넣기, 순차는 ABC 순 정리, 해시는 번호칸 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 클러스터는 관련 물건 묶어두기.

---

## Ⅲ. 행 지향 vs 열 지향 저장

### 행 지향 (Row-Oriented, NSM)

```
페이지 레이아웃:
[ID=1, Name=Alice, Age=25, Salary=50K]
[ID=2, Name=Bob,   Age=30, Salary=60K]
[ID=3, Name=Carol, Age=28, Salary=55K]
```

- OLTP에 최적: `SELECT * FROM emp WHERE id=1` → 전체 행 1번 I/O
- 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 비효율: `SELECT AVG(Salary)` → 불필요한 Name, Age도 읽음

### 열 지향 (Column-Oriented, DSM)

```
페이지 레이아웃:
ID:     [1, 2, 3]
Name:   [Alice, Bob, Carol]
Age:    [25, 30, 28]
Salary: [50K, 60K, 55K]
```

- OLAP에 최적: `SELECT AVG(Salary)` → Salary 컬럼만 읽음
- [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률 높음: 같은 타입의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 연속 → [런-길이 인코딩](/knowledge-base/studynote/08_algorithm_stats/05_string/099_rle/) 효과적

📢 **섹션 요약 비유**: 행 지향은 고객 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 카드(한 사람의 모든 정보), 열 지향은 항목별 스프레드시트(모든 사람의 나이 열)다 — 개인을 자주 조회하면 카드, 통계를 자주 내면 스프레드시트가 낫다.

---

## Ⅳ. 버퍼 풀 (Buffer Pool) 관리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">쿼리 요청 → 버퍼 풀 검색 (캐시 히트?)</div>
<div class="kb-diagram-note">↓ 미스 시</div>
<div class="kb-diagram-note">디스크에서 페이지 로드</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">버퍼 풀에 캐시</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">교체 알고리즘 (LRU/Clock)</div>
</div>
</div>



### 버퍼 풀 효율 지표

| 지표          | 계산식                         | 목표         |
|-------------|-------------------------------|-------------|
| 히트율        | 버퍼 히트 / 전체 요청           | > 95%        |
| [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)  | 버퍼 미스 횟수                  | 최소화        |
| 더티 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)  | 수정됐지만 미플러시 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 비율  | < 20%        |

📢 **섹션 요약 비유**: 버퍼 풀은 책상 위 책 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)다 — 자주 보는 책(핫 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))은 책상(메모리)에 올려두고, 오래 안 본 책(콜드 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))은 책장(디스크)에 돌려보낸다.

---

## Ⅴ. 현대 저장 구조 — LSM 트리와 컬럼 스토어

### LSM 트리 (Log-Structured Merge Tree)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">쓰기: MemTable (메모리) → WAL → SSTable (디스크)</div>
<div class="kb-diagram-note">읽기: MemTable → Bloom Filter → SSTable 레벨별 조회</div>
<div class="kb-diagram-note">컴팩션: 주기적으로 SSTable 병합·정렬</div>
</div>
</div>


→ RocksDB·[Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)·LevelDB·ClickHouse

### 컬럼 스토어 예시

| 제품           | 저장 방식      | 특징                     |
|-------------|-------------|--------------------------|
| [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)      | 컬럼 지향      | [하둡](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/S3 표준 포맷         |
| Apache Arrow | 인메모리 컬럼  | [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 벡터 연산 최적화     |
| [Snowflake](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/)    | 하이브리드     | 마이크로 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)            |
| ClickHouse   | 컬럼 LSM      | [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 집계           |

📢 **섹션 요약 비유**: LSM 트리는 편지함 + 정기 우편 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)이다 — 편지([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))는 일단 함에 넣고, 정기적으로 우체국(컴팩션)에서 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·정리한다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">파일 저장 구조 (File Storage Structure)</div>
<div class="kb-diagram-tree-item" style="--depth:0">파일 구조 유형</div>
<div class="kb-diagram-note">── 힙 파일 (Heap)</div>
<div class="kb-diagram-note">── 순차 파일 (Sequential)</div>
<div class="kb-diagram-note">── 해시 파일 (Hash)</div>
<div class="kb-diagram-note">── 클러스터 파일 (Clustered)</div>
<div class="kb-diagram-tree-item" style="--depth:0">저장 모델</div>
<div class="kb-diagram-note">── 행 지향 (NSM) — OLTP</div>
<div class="kb-diagram-note">── 열 지향 (DSM) — OLAP</div>
<div class="kb-diagram-tree-item" style="--depth:0">버퍼 관리</div>
<div class="kb-diagram-note">── 버퍼 풀 (Buffer Pool)</div>
<div class="kb-diagram-note">── LRU / Clock 교체 알고리즘</div>
<div class="kb-diagram-tree-item" style="--depth:0">현대 구조</div>
<div class="kb-diagram-tree-item" style="--depth:2">LSM 트리 (RocksDB·Cassandra)</div>
<div class="kb-diagram-tree-item" style="--depth:2">Parquet / Apache Arrow (컬럼 포맷)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파일 저장 구조 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1970년대</div><div class="kb-diagram-cell">힙·순차·해시 파일</div><div class="kb-diagram-cell">IBM IMS·관계형 DB 초기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1980년대</div><div class="kb-diagram-cell">B+-트리 인덱스 표준</div><div class="kb-diagram-cell">버퍼 풀·페이지 관리 정착</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1990년대</div><div class="kb-diagram-cell">OLAP 컬럼 스토어</div><div class="kb-diagram-cell">분석용 별도 저장 구조 등장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2006년</div><div class="kb-diagram-cell">Google Bigtable</div><div class="kb-diagram-cell">LSM 트리 주류화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2013년</div><div class="kb-diagram-cell">Apache Parquet</div><div class="kb-diagram-cell">하둡 컬럼 포맷 표준화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2020년대</div><div class="kb-diagram-cell">Apache Arrow·Iceberg</div><div class="kb-diagram-cell">인메모리 컬럼, Lakehouse</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">힙/순차/해시 → B+-트리 인덱스 → 버퍼 풀 최적화</div>
<div class="kb-diagram-note">무작위 I/O 인덱스 탐색 LRU 페이지 관리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">행 지향(OLTP) vs 열 지향(OLAP) → Lakehouse 하이브리드</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. 힙 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 물건을 그냥 던져넣는 서랍이다 — 찾기 어렵지만 넣기는 빠르다.
2. 열 지향 저장은 키·몸무게·나이를 각각 별도 리스트로 관리하는 것이다 — "모든 학생의 키 평균"을 구할 때 키 리스트만 읽으면 된다.
3. 버퍼 풀은 책상 위 책 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)다 — 자주 읽는 책은 책상(메모리)에 두고, 오래 안 본 책은 책장(디스크)에 돌려놓는다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 600

← **이전**: [TP 모니터 (Transaction Processing Monitor)](/knowledge-base/studynote/05_database/01_db_architecture_relational/032_tp_monitor/)
**다음**: [레코드 길이 · 파일 조직 방식 (Record Length & File Organization)](/knowledge-base/studynote/05_database/01_db_architecture_relational/034_record_length/) →

---
