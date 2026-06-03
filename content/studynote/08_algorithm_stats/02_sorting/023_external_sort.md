+++
title = "15. 외부 정렬 (External Sort) — 대용량 데이터, 멀티웨이 합병"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 외부 정렬은 주기억장치(RAM)에 올라오지 않는 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 디스크 I/O를 최소화하면서 정렬하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심은 비교 연산이 아닌 I/O 횟수다.
> 2. **가치**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) ORDER BY, 빅데이터 파이프라인, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 인덱싱 등 수TB~PB 규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리의 근간이며 K-way 합병(Merge)이 핵심 기법이다.
> 3. **판단 포인트**: 버퍼 크기, K(합병 경로 수), 런(Run) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 I/O 횟수를 결정하며, 대체 선택(Replacement [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/))으로 런 길이를 2배 이상 늘려 패스 수를 줄이는 것이 핵심 최적화다.

---

## Ⅰ. 개요 및 필요성

메모리 M이 1GB인 서버에서 1TB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 정렬해야 한다. 전통적인 내부 정렬(In-Memory Sort)은 이 상황에서 작동하지 않는다. <strong>외부 정렬 (External Sort)</strong>은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 메모리 크기의 청크(Chunk)로 나누어 디스크에서 읽고 쓰며 정렬하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

### 내부 정렬 vs 외부 정렬

| 구분 | 내부 정렬 | 외부 정렬 |
|:---|:---:|:---:|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치 | RAM 전체 | 디스크 (일부만 RAM) |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기준 | 비교 연산 수 | 디스크 I/O 횟수 |
| 병목 | CPU | 디스크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) |
| 적용 규모 | GB 이하 | GB~PB |
| 대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 퀵/병합/[힙 정렬](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/) | K-way 외부 병합 정렬 |

📢 **섹션 요약 비유**: 외부 정렬은 도서관의 책 전수 재배치 작업과 같다. 한 번에 트럭 1대분(메모리)만 꺼낼 수 있으므로, 트럭 단위로 배치하고 병합하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### K-Way 외부 병합 정렬 (External [Merge Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/)) 단계

<strong>1단계 — 런(Run) <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>:  
메모리에 M 크기 청크를 읽어 내부 정렬 후 디스크에 임시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(런) 저장

**2단계 — K-Way 병합 (Merge Passes)**:  
K개 런 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 동시에 읽으면서 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))으로 최솟값을 선택해 병합

**3단계 — 반복**:  
런이 1개 남을 때까지 패스 반복

### [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 — 외부 병합 정렬 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터: 1TB, 메모리: 1GB, K=4</div>
<div class="kb-diagram-tree-item" style="--depth:0">런 생성 단계</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">1GB 청크</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">내부 정렬 → 임시 런 파일</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1GB 청크</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">내부 정렬 → 임시 런 파일</div></div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">결과: 1,024개 런 파일 (각 1GB)</div>
<div class="kb-diagram-tree-item" style="--depth:0">패스 1: 4-way 합병</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Run1</div><div class="kb-diagram-cell">Run2</div><div class="kb-diagram-cell">Run3</div><div class="kb-diagram-cell">Run4</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">최솟값 힙</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Merged Run (4GB)</div>
<div class="kb-diagram-note">1,024 런 → 256 런 (패스 1 후)</div>
<div class="kb-diagram-note">256 런 → 64 런 (패스 2 후)</div>
<div class="kb-diagram-note">64 런 → 16 런 (패스 3 후)</div>
<div class="kb-diagram-note">16 런 → 4 런 (패스 4 후)</div>
<div class="kb-diagram-note">4 런 → 1 런 (패스 5 후) ✅</div>
<div class="kb-diagram-note">총 패스 수: ceil(log_K(N/M)) = ceil(log₄(1024)) = 5</div>
</div>
</div>



### 패스 수 공식

```
전체 런 수: N_runs = ceil(데이터 크기 / 메모리 크기)
패스 수:    P = ceil(log_K(N_runs))
총 I/O:    2 * N_passes * (데이터 크기) / (블록 크기)
```

### 버퍼 관리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| 버퍼 | 역할 |
|:---|:---|
| K개 입력 버퍼 | 각 런 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 블록 단위 읽기 |
| 1개 출력 버퍼 | 병합 결과를 블록 단위로 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) |
| 힙 (크기 K) | K개 포인터의 최솟값 추출 O(log K) |

### 시간/I/O 복잡도

| 항목 | 복잡도 |
|:---|:---|
| 런 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) I/O | O(N) (전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 읽기+[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)) |
| 병합 패스 수 | O(log_K(N/M)) |
| 총 I/O 횟수 | O((N/B) · log_K(N/M)) (B=블록 크기) |
| 총 비교 연산 | O(N log N) |

📢 **섹션 요약 비유**: 외부 정렬의 패스 수 줄이기는 이사 횟수 줄이기와 같다. 트럭(메모리) 여러 대를 한꺼번에 동원(K 증가)하면 이사 횟수(패스 수)가 줄어든다.

---

## Ⅲ. 비교 및 연결

### 런 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 최적화: 대체 선택 (Replacement [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/))

표준 런 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 메모리 M개 원소 → 런 크기 M. 대체 선택은 평균 **2M** 크기 런을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">대체 선택 알고리즘:</div>
<div class="kb-diagram-note">1. 메모리에 M개 원소 로드 → 최소 힙 구성</div>
<div class="kb-diagram-note">2. 힙 최솟값을 출력 버퍼에 쓰기</div>
<div class="kb-diagram-note">3. 디스크에서 새 원소 읽기</div>
<div class="kb-diagram-tree-item" style="--depth:1">새 원소 ≥ 방금 쓴 값: 같은 런에 포함 → 힙에 삽입</div>
<div class="kb-diagram-tree-item" style="--depth:1">새 원소 &lt; 방금 쓴 값: 다음 런 후보 → 별도 보관</div>
<div class="kb-diagram-note">4. 힙이 비면 현재 런 종료, 보관 원소로 새 런 시작</div>
<div class="kb-diagram-note">효과: 런 수 절반 → 패스 수 1 감소 → I/O 30-50% 절감</div>
</div>
</div>



### 외부 정렬 vs 관련 기법

| 기법 | 특징 | 적용 |
|:---|:---|:---|
| K-way 병합 정렬 | 기본 외부 정렬 | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) ORDER BY |
| 다단계 병합 (Polyphase Merge) | 패스 최적화 | 테이프 기반 고전 시스템 |
| B-트리 기반 외부 정렬 | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구조 활용 | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 빌드 |
| [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 외부 정렬 | [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) 기반 | [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/)/Spark |

📢 **섹션 요약 비유**: 대체 선택 최적화는 책을 챙길 때 "어차피 이 방향으로 가는 길에 있는 책은 지금 챙기는 것"처럼 한 번의 이동으로 더 많은 짐을 처리하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 시스템에서의 외부 정렬

**시나리오 — MySQL ORDER BY on 1억 건 테이블**:
1. `sort_buffer_size` (기본 256KB~1MB) 내에서 [퀵 정렬](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/047_quick_sort/)
2. 버퍼 초과 → 임시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(Temp [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 런 저장
3. K-way 병합으로 최종 결과 반환
4. `read_rnd_buffer_size` 최적화로 랜덤 I/O 감소

<strong>시나리오 — <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/">Apache Spark</a> 정렬</strong>:
- ShuffleManager가 외부 정렬 담당
- 메모리 임계값 초과 시 디스크 스필(Spill)
- `spark.sql.shuffle.partitions` 조정으로 K 제어

### [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 포인트



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">외부 정렬 성능 튜닝 체크리스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 메모리 할당 최대화: 런 수 감소 → 패스 수 감소</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. K 최적값 선택: K ↑ → 패스 수 ↓, 하지만 버퍼 증가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">최적 K ≈ M / (B * 2) (B=블록 크기)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 대체 선택 적용: 런 평균 크기 2배 → 패스 1 감소</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 디스크 병렬 I/O: SSD/RAID로 읽기/쓰기 동시 수행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. 압축 런 파일: I/O 데이터 크기 감소</div></div>
</div>
</div>



📢 **섹션 요약 비유**: 외부 정렬 튜닝은 공장 조립 라인 최적화와 같다. 더 큰 부품 트레이(메모리), 더 많은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 라인(K), 더 효율적인 부품 준비(대체 선택)로 전체 처리 시간을 단축한다.

---

## Ⅴ. 기대효과 및 결론

외부 정렬은 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 시스템에서 <strong>가장 실용적인 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 중 하나</strong>다. 빅데이터 파이프라인, [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 관리 등 모든 대용량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 시스템에서 외부 정렬의 원리가 동작하고 있다.

### 효과 정리

| 효과 | 내용 |
|:---|:---|
| 확장성 | RAM 크기를 초과하는 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 정렬 가능 |
| I/O 효율 | K-way 병합으로 패스 수를 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 수준으로 제한 |
| 시스템 통합 | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/), [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/), 스트림 처리와 직접 연결 |
| 최적화 여지 | 버퍼 관리, 대체 선택 등 다양한 최적화 가능 |

📢 **섹션 요약 비유**: 외부 정렬은 대형 물류 허브의 화물 처리 시스템이다. 창고(메모리)에 다 들어오지 않는 화물을 임시 야적장(디스크)에 분류해두고, 여러 경로(K-way)로 동시에 합치면 전국으로 배송할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| 병합 정렬 ([Merge Sort](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/044_merge_sort/)) | → 기반 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | K-way 병합의 이론적 근거 |
| 버퍼 풀 (Buffer Pool) | → 구현 요소 | DBMS의 메모리 관리 |
| B-트리 ([B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/)) | → 연관 구조 | 디스크 기반 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) |
| [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) | → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 확장 | Hadoop의 정렬 단계 |
| 대체 선택 (Replacement [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/)) | → 런 최적화 | 런 크기 2배 달성 |


### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">내부 정렬 (Internal Sort) — 데이터 전체가 메모리에 올라오는 전제 하에 동작하는 정렬</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">외부 정렬 (External Sort) — 디스크 I/O를 최소화하며 메모리 초과 데이터를 정렬</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">런 생성 (Run Generation) — 메모리 크기만큼 부분 정렬 후 디스크에 런(Run) 저장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">K-way 병합 (K-way Merge) — 최소 힙을 활용해 K개 런을 동시 병합, Pass 수 최소화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">MapReduce 분산 정렬 — 외부 정렬의 분산 확장, Hadoop Shuffle 단계가 K-way 병합 구현</div></div>
</div>
</div>



이 흐름은 메모리 한계를 넘는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 처리하기 위해 런 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)→K-way 병합이라는 2단계 외부 정렬 패러다임이 탄생하고, 이 원리가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 환경에서 [MapReduce](/knowledge-base/studynote/14_data_engineering/01_infrastructure/018_mapreduce/) Shuffle 단계로 수평 확장되는 정렬 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 발전 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

📦 **방 정리 이사 트럭**: 방(메모리)에 다 안 들어오는 짐을 트럭(런 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 나눠 싣고, 여러 트럭을 동시에 비교하며 새 집(결과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 순서대로 넣어요.  
🗂️ **선생님의 학생부 정리**: 선생님이 한 번에 100명 이름만 기억할 수 있다면, 100명씩 묶어서 정렬하고 합치는 방식으로 전교생 3,000명 이름도 정렬할 수 있어요.  
🔀 **합류 도로**: 여러 도로(K개 런 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에서 차가 동시에 나와서, 제일 앞에 있는 차를 순서대로 고속도로(결과)에 합류시키면 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 23 / 175

← **이전**: [15. 버블 정렬 (Bubble Sort) — O(n²), 안정, 제자리](/knowledge-base/studynote/08_algorithm_stats/02_sorting/022_bubble_sort/)
**다음**: [16. 선택 정렬 (Selection Sort) — O(n²), 불안정, 제자리](/knowledge-base/studynote/08_algorithm_stats/02_sorting/024_selection_sort/) →

---
