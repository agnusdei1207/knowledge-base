---
title: "263. Lfu Page Replacement"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LFU (Least Frequently Used)는 메모리가 꽉 차서 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 교체할 때, "최근에 언제 썼는가(시간)"가 아니라 <strong>"과거부터 지금까지 총 몇 번이나 쓰였는가(빈도수)"를 따져 가장 적게 사용된 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a>를 쫓아내는 통계 기반 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>이다.
> 2. **가치**: 한 번 쓱 지나가며 엄청난 양의 메모리를 읽고 버리는 스캔 작업(Sequential Scan)이 들어왔을 때 기존 캐시가 싹 다 밀려버리는 <strong>LRU의 치명적 약점(Cache Pollution)을 완벽하게 방어</strong>해 내는 '단골손님 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)' 철학을 지닌다.
> 3. **융합**: 하지만 과거의 영광(높은 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 횟수)에 취해 현재는 쓰이지 않는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 메모리에 영원히 박제되는 문제와 O(log N)의 관리 오버헤드 탓에, 현대에는 LFU와 LRU의 장점만 섞은 **W-TinyLFU (Caffeine Cache 등)** 같은 하이브리드 아키텍처로 진화하여 실무 캐시 엔진을 평정했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)마다 <strong>'<a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a> 횟수(<a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">Reference</a> Count)'</strong>를 기록하는 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)를 두고, [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 폴트가 발생하여 누군가를 버려야 할 때 이 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 값이 가장 작은 녀석을 골라 희생양(Victim)으로 삼는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
- **필요성**: LRU는 훌륭했지만 "딱 한 번 불렸더라도 방금 불린 놈을 VIP 대접한다"는 맹점이 있었다. 만약 [바이러스](/studynote/02_operating_system/10_security/589_virus/) 백신이 하드디스크의 10GB짜리 쓰레기 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들을 한 번씩 쭉 스캔하면, LRU는 이걸 "최신 트렌드"라 착각하고, 내가 매일 100번씩 쓰던 크롬 브라우저 캐시를 바닥으로 쫓아내 버렸다. "어제 한 번 온 손님 때문에 10년 단골을 쫓아내는" 이 바보짓을 막기 위해 <strong>'빈도(Frequency)'라는 새로운 평가 잣대</strong>가 필요했다.

- **등장 배경**: 1970년대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스와 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 버퍼 풀(Buffer Pool) 관리가 고도화되면서, 특정 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록([인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 루트 노드 등)은 프로그램 시작부터 끝까지 수만 번 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)된다는 사실이 밝혀졌다. 이런 VIP [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 절대로 [스왑 아웃](/studynote/02_operating_system/06_memory_management/336_swap_out_in/)(Swap-out)시키지 않기 위한 락([Lock-in](/studynote/12_it_management/05_security_compliance/362_lock_in_portability/))의 개념으로 빈도수 기반 교체 이론이 탄생했다.

```text
  [LRU의 맹점(Cache Pollution)과 LFU의 철벽 방어 시뮬레이션]

  [ 상황: 램 프레임 3칸. 현재 'A(100번 불림)', 'B(50번)', 'C(30번)' 꽉 차 있음 ]

  -> 갑자기 쓰레기 데이터 X, Y, Z 가 딱 1번씩만 참조되며 들어옴!

  [ ❌ LRU (최근 사용 우선) 의 멍청한 판단 ]
  1. X 들어옴 --> 제일 예전에 쓴 C 버림 --> 램 상태: [A, B, X]
  2. Y 들어옴 --> 그다음 예전에 쓴 B 버림 --> 램 상태: [A, X, Y]
  3. Z 들어옴 --> 제일 예전에 쓴 A 버림 --> 램 상태: [X, Y, Z]
  🚨 결과: 100번, 50번 쓰이던 특급 단골 A, B가 다 쫓겨나고 1번씩 쓴 쓰레기로 램이 도배됨! (캐시 오염)

  [ ✅ LFU (빈도수 최우선) 의 철벽 방어 ]
  1. X(1번) 들어옴 --> C(30번) 버릴까? 안돼! C가 더 많이 불렸어! X 너 그냥 나가!
  2. Y(1번) 들어옴 --> B(50번), C(30번)? Y 너 나가!
  3. Z(1번) 들어옴 --> A(100번)? Z 너 나가!
  ✅ 결과: 스쳐 지나가는 쓰레기 데이터들은 램에 정착하지 못하고 바로 튕겨 나감. 단골 완벽 보호!
```
**[다이어그램 해설]** LFU는 "빈도수"라는 막강한 기득권(권력)을 형성한다. 이 권력을 쌓은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 어지간한 신규 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 도전을 다 씹어먹고 캐시 상단에 영구 박제된다. 이는 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)([Backup](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/))이나 풀 스캔(Full Scan) 쿼리가 돌 때 캐시 메모리가 초토화되는 것을 막아주는 최고의 방패막이다.

- **📢 섹션 요약 비유**: 100번 클릭해서 키워놓은 만렙 기사(단골 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))와 방금 막 생성한 1레벨 초보(스캔 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 파티에 있습니다. LRU는 "방금 로그인한 초보가 더 중요해!"라며 만렙 기사를 파티에서 쫓아내는 멍청한 마스터입니다. LFU는 철저히 레벨(클릭 횟수)만 보고 1레벨들을 가차 없이 추방하는 냉혹한 길드장입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LFU의 두 가지 구현 방식과 치명적 약점

LFU를 소프트웨어로 짜려면 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)마다 `int count` 변수를 둬야 한다. 그리고 이 `count`를 기준으로 줄을 세워야 하는데 여기서 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 비극이 시작된다.

#### 1. [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)([Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)) 기반 힙(Min-[Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 정렬 오버헤드
- `count`가 가장 작은 놈을 $O(1)$에 찾으려면 최소 힙(Min-[Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))이나 [이진 탐색](/studynote/08_algorithm_stats/03_graph_search/031_binary_search_algorithm/) 트리를 써야 한다.
- 메모리를 한 번 읽을 때마다 $O(\log N)$의 속도로 트리를 재정렬해야 한다.
- **현실**: CPU 캐시나 OS 메모리 스케줄러는 나노초 단위로 움직이는데, 매번 트리를 뒤집는 오버헤드는 100% 시스템 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/))을 유발한다.

#### 2. 과거의 영광 (Historical Baggage) 문제
- 어떤 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 프로그램 시작 직후 5분 동안 `for` 루프에 걸려 <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>,000번</strong> [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되었다.
- 5분 뒤 이 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 수명을 다해 프로그램 끝날 때까지 다신 안 쓰인다.
- **결과**: 하지만 이 녀석의 카운트는 이미 '[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000'이라는 넘사벽 스펙을 찍었기 때문에, 새로 들어온 진짜 필요한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(카운트 1, 2)들을 다 짓밟고 <strong>메모리에 영원히 시체처럼 남아서(박제) 램을 낭비</strong>한다.

### [Aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/) ([노화](/studynote/02_operating_system/03_cpu_scheduling/182_aging/)) 기법을 통한 LFU의 심폐소생술
과거의 영광에 취해 안 나가는 고인물들을 치우기 위해 고안된 기법이다.
- **원리**: 주기적으로(예: 1초마다) 모든 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 카운트 값을 **절반으로 깎아버린다 ([Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) Shift Right: `count >>= 1`)**.
- **효과**: 1만 번을 찍은 고인물도 시간이 지나면 5천, 2천5백, 1천으로 점수가 팍팍 깎인다. 결국 최근에 계속 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)되어 점수를 올리는 '젊은 피(Recent Frequency)'들에게 자리를 내어주게 된다.

- **📢 섹션 요약 비유**: 왕년에 1만 골을 넣은 은퇴한 전설의 스트라이커(과거의 영광)가 과거 기록만 믿고 주전 자리를 차지해 신인들이 못 뛰는 상황입니다. 감독(OS)은 매년 모든 선수의 통산 골 기록을 반 토막([Aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/)) 내버리는 규정을 만들어서, 최근에 꾸준히 골을 넣는 선수만이 주전을 유지할 수 있게 고인물을 쳐냅니다.

---

## Ⅲ. 비교 및 연결

### [LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) (최근성) vs LFU (빈도수) 의 철학 전쟁

운영체제와 캐시 프레임워크를 만들 때 아키텍트를 가장 괴롭히는 선택지다.

| 특성 | [LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) ([Least Recently Used](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)) | LFU (Least Frequently Used) |
|:---|:---|:---|
| **평가 기준** | "언제 마지막으로 썼는가?" (Time-based) | "지금까지 몇 번 썼는가?" (Count-based) |
| **방어력 (스캔 공격)**| ❌ 최약체. 풀 스캔 돌면 캐시 다 털림. | ✅ 최강. 한 번 스친 쓰레기들은 바로 버려짐. |
| **적응력 (트렌드 변화)**| ✅ 최고. 옛날 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 뒤로 바로 밀려남. | ❌ 최악. 옛날에 많이 불린 놈이 안 나가고 버팀. |
| **구현 오버헤드** | 적음 (단순 [Linked List](/studynote/08_algorithm_stats/04_datastructure/056_linked_list/) 포인터 스왑) | <strong>매우 큼 (Min-<a href="/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/">Heap</a> 정렬 필요)</strong> |
| **현대적 사용처** | OS 커널의 [페이지 교체](/studynote/02_operating_system/04_synchronization/260_page_replacement/) ([Clock](/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 우회) | 백엔드 In-Memory 캐시 서버 ([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 등) |

이 두 철학은 완벽하게 서로의 약점을 찌른다. LRU는 새로운 변화에 유연하지만 사기꾼(스캔)에 약하고, LFU는 사기꾼은 100% 막아내지만 변화에 둔감한 꼰대다.

### 하이브리드의 탄생: LRFU와 W-TinyLFU
현대 컴퓨터 공학은 이 둘 중 하나를 고르는 짓을 그만두고 아예 합쳐버렸다.
- **LRFU**: 큐를 두 개로 나눈다. 방금 들어온 놈들은 [LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 큐에 넣고, 거기서 여러 번 살아남아 증명된 놈들만 LFU 큐로 승진시킨다.
- **W-TinyLFU**: 자바 진영의 최강 캐시 라이브러리인 <strong>Caffeine Cache</strong>가 쓰는 궁극의 엔진. [블룸 필터](/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)([Bloom Filter](/studynote/12_it_management/02_itsm_itil/061_bloomfilter/))의 변종인 Count-Min Sketch를 써서 1바이트도 안 되는 메모리로 수백만 건의 빈도수를 추적하며, 최근성(Window)과 빈도수(Frequency)를 동시에 평가해 99%의 히트율을 뽑아낸다.

- **📢 섹션 요약 비유**: LRU는 '유행(트렌드)'이고, LFU는 '누적 판매량(스테디셀러)'입니다. 음원 차트를 짤 때 유행만 반영하면 사재기(스캔 공격)에 차트가 오염되고, 누적 판매량만 반영하면 10년 전 조용필 노래가 평생 1등을 합니다. 두 개를 절묘하게 섞은 '빌보드 핫 100 (W-TinyLFU)'이 진짜 대중의 마음을 반영하는 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong>Redis의 <code>allkeys-lfu</code> <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> (<a href="/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> 4.0 이후 도입)</strong>:
   - 과거 Redis는 LRU만 지원했다. 하지만 사용자들이 "가끔 도는 배치 작업 때문에 메인 배너 캐시가 날아간다!"라고 아우성쳤다.
   - **아키텍처 혁신**: [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) 제작자는 LFU의 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 정렬 오버헤드를 없애기 위해, 객체 헤더의 24비트 공간에 `8비트는 빈도수(Logarithmic 카운터)`, `16비트는 최근 접근 시간(Aging용)`을 때려 박았다.
   - **실무 효과**: 완벽한 LFU가 아니라 "대충 빈도를 세면서, 시간 지나면 알아서 값이 깎이는(Decay)" 확률적 LFU를 구현했다. 덕분에 메모리나 CPU 오버헤드 0%로 스캔 공격을 완벽히 방어하는 `allkeys-lfu` 모드가 탄생하여 현대 캐시 아키텍처의 표준이 되었다.
2. <strong><a href="/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/">CDN</a>(Content Delivery Network)의 엣지 서버 <a href="/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a></strong>: 전 세계로 동영상을 쏘는 AWS CloudFront나 Cloudflare의 엣지 노드는 용량이 꽉 차면 누굴 지울까?
   - **실무 판단**: 동영상은 크기가 GB 단위다. 한 번 잘못 지우면 오리진(Origin) 서버에서 다시 가져오는 네트워크 비용이 수천만 원이다.
   - **아키텍트 결단**: 이때는 무조건 <strong>LFU 기반의 변형 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>(LFU-DA 등)</strong>을 쓴다. 한 번 조회된 듣보잡 영상은 바로 디스크에서 날리고, 하루에 1만 번 조회되는 방탄소년단 뮤직비디오(High Frequency)는 램 최상단에 영구 박제시켜 글로벌 트래픽 비용을 극한으로 후려친다.

```text
  +--------------------------------------------------------------------------+
  |     백엔드 아키텍트의 캐시 교체 정책(Eviction) 설계 가이드라인           |
  +--------------------------------------------------------------------------+
  |                                                                          |
  |   [질문 1] 데이터의 생명 주기가 극단적으로 짧고 유행을 타는가?           |
  |     (예: 뉴스 피드 최신 글, 실시간 주식 호가)                            |
  |          +- [예] --> ✅ LRU (Least Recently Used) 선택                    |
  |          |                                                               |
  |          +- [아니오]                                                     |
  |                 |                                                        |
  |   [질문 2] 소수의 '스타 데이터(전역 설정, 랭킹)'가 트래픽의 90%를 먹는가?|
  |          +- [예] --> ✅ LFU (Least Frequently Used) 선택                  |
  |          |             (스캔 공격에 스타 데이터가 썰리는 걸 절대 방어)   |
  |          |                                                               |
  |          +- [모르겠다 / 섞여 있다]                                       |
  |                 |                                                        |
  |                 v ✅ W-TinyLFU (Caffeine Cache) 선택                     |
  |             "알아서 최근 유행과 누적 단골을 다 챙겨주마!"                |
  |             (현재 Java 진영 Spring Boot의 기본 캐시 엔진임)              |
  +--------------------------------------------------------------------------+
```
**[다이어그램 해설]** "OS 커널은 왜 LFU를 안 쓸까?" OS가 관리하는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 코드와 지역 변수 쪼가리들이라 빈도를 세는 게 무의미하고 너무 무겁기 때문이다. 반면 <strong>애플리케이션(User Space) 레벨의 '객체 <a href="/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a>(Object <a href="/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">Caching</a>)'</strong>에서는 LFU가 제왕이다. 아키텍트는 OS의 한계와 애플리케이션의 강점을 명확히 구분하여 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 차용해야 한다.

- **📢 섹션 요약 비유**: OS 커널의 [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)([LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))은 '편의점 알바생'입니다. 물건이 너무 많고 빨리 팔리니 그냥 방금 팔린 걸 앞에 채워 넣는 게 최고입니다. 하지만 백엔드 서버의 캐시(LFU)는 '명품관 매니저'입니다. 물건 하나하나의 가치가 크기 때문에, 누가 얼마나 자주 사 가는지 고객 장부(빈도수)를 철저히 기록해서 VIP만 챙겨야 이윤이 남습니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
LFU 철학을 캐시 시스템에 적용하면, 악의적인 크롤링 봇이나 백그라운드 전체 스캔 작업이 유발하는 캐시 오염(Cache Pollution)을 원천 차단하여, 실제 유저들이 가장 많이 찾는 핵심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Hot Data](/studynote/01_computer_architecture/15_advanced_topics/675_hot_data_caching/))의 램 상주율을 100% 방어해 낼 수 있다.

### 결론 및 미래 전망
LFU는 "[참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 횟수를 센다"는 가장 직관적이고 강력한 무기를 가졌음에도, O(log N)이라는 힙 정렬의 무거움과 고인물 박제라는 한계 때문에 한동안 LRU의 그늘에 가려져 있었다.
하지만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 돈이 되는 빅데이터 시대가 오며 "누가 진성 단골(Hot [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)?"를 가려내는 기술의 가치가 급상승했다. 현대의 컴퓨터 과학은 LFU의 무거운 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 정렬을 버리고, 빅데이터 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)인 **스케치(Sketch, 확률적 자료구조)** 기법을 도입하여 단 몇 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/))만으로 1억 개의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 빈도수를 오차율 1% 미만으로 추적해 내는 기적을 이뤄냈다. LFU는 죽은 것이 아니라, 빅데이터 통계학의 옷을 입고 현대 클라우드 캐시의 심장으로 화려하게 부활했다.

- **📢 섹션 요약 비유**: 과거의 LFU는 매장 입구에 서서 손님 1만 명의 이름을 장부에 정자로 꾹꾹 눌러쓰다(오버헤드 폭발) 쓰러진 바보였습니다. 현대의 LFU(Caffeine 등)는 그냥 손님이 지나갈 때마다 지문 인식기(Sketch [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))로 0.01초 만에 틱틱 찍고 통계만 내는 최첨단 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 매니저로 환골탈태했습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 장벽 (Barrier) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 양방향 랑데부 (Rendezvous) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 큐잉 [스핀락](/studynote/02_operating_system/04_synchronization/222_spinlock/) (MCS [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) / qspinlock) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 낙관적 병행성 제어 ([Optimistic Concurrency Control](/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[양방향 랑데부 (Rendezvous)]
    |
    v
[LFU (Least Frequently Used) 페이지 교체]
    |
    +---> [큐잉 스핀락 (MCS Lock / qspinlock)]
    +---> [낙관적 병행성 제어 (Optimistic Concurrency Control)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 상자에 자리가 없어서 하나를 버려야 해요. LRU는 "어제 산 팽이 냅두고, 작년부터 매일 만지던 로봇을 버리자(오래전에 만졌으니)"라고 해요.
2. 하지만 <strong>LFU</strong>는 "안돼! 팽이는 어제 한 번 만진 게 다지만, 로봇은 1년 동안 1,000번이나 갖고 놀았어! 팽이를 버려!"라고 똑똑하게 따져요.
3. 이렇게 단순히 언제 만졌는지가 아니라, <strong>지금까지 몇 번이나 사랑해 줬는지(빈도수)</strong>를 세어서 가장 인기 없는 장난감을 버리는 방법이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 263 / 800

<- **이전**: [262. LRU (Least Recently Used) 페이지 교체](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/)
**다음**: [264. 클럭 알고리즘 (Clock Algorithm / NUR)](/studynote/02_operating_system/04_synchronization/264_clock_algorithm_nur/) ->

---
