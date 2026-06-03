+++
title = "722. 페이지 교체 LRU 원리 (Page Replacement Lru Principle)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)([Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))는 [요구 페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)) 환경에서 물리적 램(RAM)이 꽉 찼을 때, <strong>"가장 오랫동안 사용되지 않은(참조되지 않은) <a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a>를 디스크로 내쫓는(Swap-out)"</strong> 가장 대표적이고 합리적인 [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/)이다.
> 2. **원리 (지역성)**: LRU의 성공은 <strong><a href="/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/">시간적 지역성</a>(<a href="/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/247_temporal_locality/">Temporal Locality</a>)</strong>, 즉 "최근에 쓰인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 가까운 미래에 또 쓰일 확률이 높고, 오랫동안 안 쓰인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 앞으로도 안 쓰일 확률이 높다"는 컴퓨터 공학의 경험적 진리에 완벽하게 부합하기 때문이다.
> 3. **구현의 한계**: 그러나 순수한 LRU를 구현하려면 메모리를 참조할 때마다 시간을 기록하거나 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)를 매번 갱신하는 막대한 $O(1)$의 하드웨어/소프트웨어 오버헤드가 발생하므로, 현대 OS는 순수 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 대신 이를 흉내 낸 근사(Approximation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)인 <strong>시계(<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/">Clock</a>) <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>을 주로 사용한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/">페이지 교체</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/">Page Replacement</a>)</strong>: [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 시스템에서 빈 프레임(RAM)이 없을 때, 현재 램에 올라와 있는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 중 하나를 골라 디스크(Swap)로 쫓아내고 그 빈자리에 새로운 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 올리는 작업.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">Least Recently Used</a>)</strong>: 쫓아낼 희생자(Victim)를 고를 때 "가장 오랫동안 건드리지 않은 놈"을 고르는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/).

- **필요성 (미래를 알 수 없는 시스템의 차선책)**: 
  - 램이 꽉 차서 누군가를 쫓아내야 한다. 가장 좋은 방법([OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/))은 "앞으로 가장 오랫동안 안 쓸 놈"을 쫓아내는 것이다.
  - 하지만 운영체제는 미래를 예측할 수 없다(프로그램이 다음에 뭘 읽을지 모름).
  - **해결책**: "미래를 모른다면, 과거를 보자!" 과거에 가장 오랫동안 안 쓰인 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)라면, 미래에도 안 쓰일 확률이 제일 높다는 통계적 사실(지역성)에 기대어 LRU가 탄생했다.

  - 옷장이 꽉 차서 새 옷을 넣으려면 옛날 옷 하나를 헌 옷 수거함에 버려야 한다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> (선입선출)</strong>: 그냥 제일 먼저 산 옷을 버린다. (어제 산 옷이라도 상관 안 함) $\rightarrow$ 만약 매일 입는 교복이 제일 먼저 산 옷이면 어떡하지? 망한다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a></strong>: 옷장을 열어보고 <strong>"가장 오랫동안 안 입은 옷"</strong>을 버린다. (가장 합리적이고 우리가 실제로 옷을 버리는 방식)

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">First-In First-Out</a>)</strong>: 만들기 쉬워서 썼으나 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최악 (벨라디의 모순 발생).
  2. <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/">OPT</a> (Optimal)</strong>: 이론상 최적이나 구현 불가능.
  3. <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">Least Recently Used</a>)</strong>: 현실 세계에서 구현 가능한 최적의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 표준화.
  4. <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/406_lru_approximation/">LRU Approximation</a></strong>: 진짜 LRU는 너무 무거워서, [Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) Bit를 활용한 [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/)(시계) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 진화.

- **📢 섹션 요약 비유**: 냉장고가 꽉 찼을 때 유통기한이 많이 남은 걸 버리는 바보는 없습니다. 가장 안쪽에서 오랫동안 꺼내 먹지 않아 먼지가 쌓인 반찬([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))부터 버리는 것이 가장 상식적인 공간 관리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LRU의 동작 시뮬레이션

프레임이 3개(램 용량)인 시스템에서, 프로세스가 다음 순서대로 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 요구한다고 치자: `1 -> 2 -> 3 -> 1 -> 4`



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LRU 페이지 교체 시뮬레이션 (프레임 3개)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력: 1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">1</div><div class="kb-diagram-note">할당 (Page Fault)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력: 2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">1, 2</div><div class="kb-diagram-note">할당 (Page Fault)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력: 3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">1, 2, 3</div><div class="kb-diagram-note">할당 (Page Fault)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력: 1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">램에 1이 있음! (Hit!)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">★ LRU의 핵심: 1이 방금 쓰였으므로, 1의 나이를 "가장 최신"으로 갱신함.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(오래된 순서: 2 -&gt; 3 -&gt; 1)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력: 4</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">램이 꽉 참. 누군가 쫓아내야 함 (Page Fault)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 1은 방금 썼다. 3은 그전에 썼다. 2가 가장 옛날에 썼다.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- "2번 페이지, 넌 아웃이야!" (Victim = 2)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">- 램 상태:</div><div class="kb-diagram-node">1, 4, 3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">1 -&gt; 4)</div></div>
</div>
</div>



**[다이어그램 해설]** 만약 이 상황에서 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a></strong>를 썼다면? 무조건 제일 먼저 들어온 `1`을 쫓아내고 `4`를 넣었을 것이다. 그런데 바로 방금 `1`을 썼지 않은가? `1`을 쫓아내면 십중팔구 다음번 호출에 또 `1`을 부를 텐데 그때 또 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 터진다. LRU는 이처럼 "방금 쓴 건 다시 살려주는" 스마트한 방어 로직을 갖췄다.

---

### 순수 LRU의 두 가지 하드웨어 구현법 (그리고 실패 이유)

이론적으로 완벽한 LRU를 만들려면 하드웨어가 두 가지 방식 중 하나를 지원해야 한다.

1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/">카운터</a> (<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/">Counter</a>) 방식</strong>:
   - 메모리를 읽을 때마다 CPU의 '[Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/)(시간)'을 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 테이블에 기록한다.
   - 쫓아낼 때: 램에 있는 모든 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 시간을 쭉 스캔해서 가장 숫자가 작은(오래된) 놈을 찾는다.
   - 실패 이유: 프레임이 100만 개면 찾을 때마다 100만 번 비교($O(N)$)해야 하므로 너무 느리다.
2. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a> (<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/">Stack</a> / <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/">Linked List</a>) 방식</strong>:
   - [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 사용할 때마다, 그 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 노드를 빼서 더블 링크드 리스트의 `Top(머리)`으로 옮긴다.
   - 쫓아낼 때: 무조건 `Bottom(꼬리)`에 있는 놈을 쫓아낸다. ($O(1)$ 속도)
   - 실패 이유: 램을 1번 읽을 때마다, 하드웨어가 6개의 포인터를 조작하는 미친 연산(Overhead)을 감당해야 한다.

- **📢 섹션 요약 비유**: 회사에서 "가장 오랫동안 일 안 한 사람"을 자르려고, 직원 1,000명의 자리비움 초시계를 실시간으로 재거나([카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)), 1분마다 직원의 줄을 새로 세우는 것([스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))은 일하는 것보다 감시하는 비용이 더 듭니다. 순수 LRU는 오버헤드라는 벽에 막혔습니다.

---

## Ⅲ. 비교 및 연결

### 3대 [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/) 철학 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 희생자 선정 기준 | 장점 | 단점 | 실무 활용도 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">First-In First-Out</a>)</strong>| **가장 먼저 램에 올라온 놈** | 구현이 가장 단순함 (단순 큐) | 방금 쓴 놈도 죽임, 벨라디의 모순 발생 | 거의 안 씀 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/">OPT</a> (Optimal)</strong> | **미래에 가장 오랫동안 안 쓸 놈**| <strong>가장 완벽함 (<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 최소)</strong>| 미래를 알 수 없어 **구현 불가** | 다른 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가의 기준점 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">Least Recently Used</a>)</strong>| **과거에 가장 오랫동안 안 쓴 놈**| 지역성에 부합하여 OPT에 근접함 | 정확한 구현은 오버헤드가 극심함 | <strong>근사 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>으로 변형되어 천하 통일</strong> |

### 과목 융합 관점

- <strong>자료구조 (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Structure)</strong>: LRU의 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 방식 구현은 해시맵(Hash Map)과 양방향 [연결 리스트](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)(Doubly [Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/))를 결합한 `LinkedHashMap` 형태로 구현된다. 캐시 룩업은 $O(1)$로, 순서 갱신도 $O(1)$로 처리할 수 있어 <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a></strong>나 **Memcached** 같은 인메모리 DB의 캐시 교체 로직(Eviction [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))으로 가장 많이 쓰이는 자료구조 패턴이다.
- <strong>컴퓨터구조 (<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>)</strong>: OS가 디스크 스왑을 할 때뿐만 아니라, CPU 내부의 하드웨어 L1/L2 캐시 컨트롤러가 캐시 라인(64바이트)을 쫓아낼 때(Eviction)도 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 하드웨어 회로(Pseudo-[LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))를 내장하여 사용한다. 메모리 계층 구조의 모든 곳에서 맹활약하는 법칙이다.

- **📢 섹션 요약 비유**: FIFO가 머리가 텅 빈 경비원이라면, OPT는 타임머신을 타는 외계인이고, LRU는 경험과 통계를 바탕으로 합리적인 추론을 해내는 베테랑 형사입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> 인메모리 DB의 메모리 초과 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a>) 방어</strong>: 16GB 서버에 Redis를 띄우고 유저 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 저장했다. 사용자가 늘어나 메모리가 16GB를 꽉 채우면 Redis가 멈출까?
   - **아키텍처 적용**: Redis는 OS의 스왑을 믿지 않고, 자체적인 메모리 한계(`maxmemory`)를 설정한다. 그리고 `maxmemory-policy`를 <strong><code>allkeys-lru</code></strong> 로 설정해 둔다.
   - **결과**: 메모리가 16GB에 도달하는 순간, Redis는 저장된 수억 개의 [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 중에서 "가장 오랫동안 사용자가 찾지 않은(로그인 안 한 지 오래된) [세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)"를 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 찾아내어 영구 삭제해 버린다. 덕분에 OOM이 나지 않고 최신 유저들의 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)을 완벽하게 유지한다.

2. <strong>시나리오 — RDBMS (<a href="/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/">Oracle</a>, MySQL)의 버퍼 풀 (Buffer Pool) 관리</strong>: MySQL의 InnoDB 엔진은 디스크의 테이블 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 램(Buffer Pool)에 올려놓고 쓴다. 용량이 꽉 차면?
   - **원인 분석**: 10GB 버퍼 풀이 꽉 찼는데 새로운 쿼리가 들어왔다. 누군가를 쫓아내야 한다.
   - **아키텍처 대응**: 단순 LRU를 쓰면 치명적인 버그가 생긴다. 관리자가 `SELECT * FROM table` 처럼 풀 스캔을 한 번 때려버리면, 수십 기가바이트의 쓰레기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 버퍼로 밀려들어 와서 기존에 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)해 둔 '자주 쓰는 [핫 데이터](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/)'를 전부 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 꼬리 밖으로 밀어내 버린다 (Cache Pollution).
   - <strong>해결 (Midpoint Insertion <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">Strategy</a>)</strong>: MySQL은 순수 LRU를 쓰지 않고 리스트를 5/8 지점에서 반으로 가른다. 새로 읽은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 맨 머리([New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/))가 아니라 중간(Midpoint)에 꽂는다. 그 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 짧은 시간 안에 '한 번 더' 읽혀야만 진짜 [핫 데이터](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/)로 인정받아 머리로 올라가고, 스캔용 쓰레기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 중간에 꽂혔다가 금방 꼬리로 쫓겨나는 <strong>개선된 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a>-K 아키텍처</strong>를 쓴다.

### 의사결정 및 튜닝 플로우



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">캐시 교체(Eviction) 전략 아키텍처 플로우</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">한정된 메모리(RAM/Redis/CDN)에 데이터를 캐싱하는 시스템 설계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터의 접근 패턴이 최근 시간(Recency)에 강한 영향을 받는가?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(예: 방금 올린 게시글, 최근 로그인한 유저 세션)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">LRU (Least Recently Used) 알고리즘 채택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">대책: 가장 보편적이고 안전한 선택. Redis 기본 설정.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 아니오 (시간보다 '조회수(빈도)'가 더 중요한 랭킹 데이터다)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">LFU (Least Frequently Used) 알고리즘 채택</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 오랫동안 안 썼더라도, 누적 조회수(Frequency)가 높은 데이터는 안 지우고</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">살려두는 전략. (단, 최근에 뜬 신규 트렌드 데이터가 불리해지는 단점 존재)</div></div>
</div>
</div>



**[다이어그램 해설]** LRU는 완벽하지 않다. "10년 동안 100만 번 조회된 레전드 글"이 어제 하루 안 읽혔다는 이유로, "방금 올라와서 1번 읽힌 스팸 글"에게 자리를 내어주고 캐시에서 쫓겨나는 것이 LRU의 치명적 맹점(Frequency 무시)이다. 고도화된 아키텍처는 최근성([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))과 빈도([LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/))를 섞어 쓰는 W-TinyLFU(Caffeine Cache) 같은 하이브리드 모델을 사용한다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a> 근사 (<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/302_clock_algorithm/">Clock Algorithm</a>)</strong>: OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서는 포인터를 관리하는 LRU가 무거워서, 하드웨어 MMU가 남겨주는 `Reference Bit (참조 비트, 1/0)` 하나만 보고 원형 큐를 시곗바늘처럼 돌면서 0인 놈을 쫓아내는 <strong>시계(<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/">Clock</a>) <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>을 쓴다. 이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 눈속임을 이해하고 있는가?

- **📢 섹션 요약 비유**: LRU는 '유행'을 쫓는 옷장입니다. 방금 산 옷이나 방금 입은 옷은 맨 앞에 걸어두지만, 아무리 비싼 코트라도 1년 동안 안 입으면 가차 없이 헌 옷 수거함으로 직행합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) (무지성) | [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) (경험적 지역성) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 비율)</strong>| 잦은 미스 발생 (벨라디 모순) | [OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/)(최적) 모델에 가장 근접함 | I/O 대기 시간 감소로 시스템 속도 향상 |
| **정성 (자원 보존)** | 핵심(Hot) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 무차별 축출 | 자주 쓰는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 램에 영구 상주 | DB/캐시 서버의 캐시 히트율([Hit Ratio](/knowledge-base/studynote/02_operating_system/06_memory_management/359_effective_access_time/)) 90% 방어 |
| **정성 (예측 가능성)**| 램을 늘려도 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 떨어질 수 있음 | 램을 늘리면 무조건 미스가 줆 ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) | 인프라 [스케일 업](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)([Scale-up](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/))의 논리적 타당성 확보 |

### 미래 전망
- **ARC (Adaptive Replacement Cache)**: IBM이 발명하고 ZFS [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에서 극찬받은 차세대 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/). [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)(최근성) 리스트와 [LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/)(빈도) 리스트를 두 개 유지하며, 워크로드의 변화에 따라 두 리스트의 크기를 스스로 동적 조절(Adaptive)하여 캐시 히트율을 기적처럼 방어해 내는 스토리지 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)의 끝판왕이다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 커스텀 교체 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/))을 건드리는 건 금기였으나, 최근 클라우드 벤더들은 eBPF를 이용해 특정 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 워크로드에만 딱 맞는 전용 [Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) 룰을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 주입하여 메모리 효율을 극한으로 쥐어짜고 있다.

### 결론
[LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)([Least Recently Used](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)) 원리는 컴퓨터 과학이 불확실한 미래를 대처하기 위해 내놓은 가장 철학적이고 통계적인 해답이다. "과거를 잊은 자에게 미래는 없다." 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 프로그램이 내뿜는 '지역성(Locality)'이라는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 온기를 놓치지 않고, 가장 차갑게 식어버린 기억부터 무자비하게 잘라낸다. 오늘날 우리가 쓰는 스마트폰의 앱 백그라운드 관리부터 글로벌 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), CPU 내부의 마이크로 아키텍처에 이르기까지, 이 간단한 '최근성'의 법칙이 적용되지 않은 곳은 지구상에 존재하지 않는다.

- **📢 섹션 요약 비유**: 어제 만난 사람은 내일도 만날 확률이 높고, 10년 전 초등학교 동창은 내일도 안 만날 확률이 높습니다. 우리 뇌가 10년 전 동창의 얼굴을 자연스럽게 잊어버리는([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) Eviction) 것은 뇌 용량을 아끼기 위한 가장 완벽하고 효율적인 생존 본능입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) [ISR](/knowledge-base/studynote/02_operating_system/01_overview_architecture/020_isr/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 유효/무효 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) (Valid/Invalid) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 벨라디의 모순 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [최적 알고리즘](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/) ([OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/)) 구현 불가 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">유효/무효 비트 (Valid/Invalid)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">페이지 교체 LRU 원리 (Page Replacement Lru Principle)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">FIFO 벨라디의 모순</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">최적 알고리즘 (OPT) 구현 불가</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 상자(메모리)에 장난감을 3개만 넣을 수 있어요. 새 로봇을 넣으려면 안에 있는 장난감 하나를 버려야 해요([페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)).
2. 철수는 상자를 열어보고 **"가장 오랫동안 안 가지고 놀아서 먼지가 뽀얗게 쌓인"** 낡은 팽이를 버렸어요. ([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 방식)
3. 만약 제일 먼저 샀다는 이유로 어제도 가지고 놀았던 최애 인형을 버린다면([FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 방식) 바보겠죠? 가장 오랫동안 안 쓴 걸 버리는 게 제일 똑똑한 정리 정돈이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 722 / 800

← **이전**: [721. 유효/무효 비트 (Valid/Invalid)](/knowledge-base/studynote/02_operating_system/11_exam_summary/721_valid_invalid_bit_page_table/)
**다음**: [723. FIFO 벨라디의 모순 (FIFO Beladys Anomaly)](/knowledge-base/studynote/02_operating_system/11_exam_summary/723_fifo_beladys_anomaly/) →

---
