---
title: 404. 디렉터리 기반 프로토콜 (Directory-based Protocol)
date: '2026-03-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[506_directory_structure_symbol_table|Directory]]-based [[295_protocol_field_tcp_udp_icmp|Protocol]])은 각 캐시 라인의 보유자와 수정 권한을 홈 노드(Home Node)의 장부에 기록해, 브로드캐스트 대신 필요한 캐시에만 [[194_consistency_database_integrity|일관성]] [[389_mesh_topology|메시]]지를 보내는 [[402_cache_coherence|캐시 일관성]] ([[402_cache_coherence|Cache Coherence]]) 방식이다.
> 2. **가치**: 코어 수가 늘어날수록 [[403_snooping_protocol|스누핑 프로토콜]] ([[403_snooping_protocol|Snooping Protocol]])의 전역 감시 비용은 폭증하지만, [[506_directory_structure_symbol_table|디렉터리]] 방식은 네트워크 트래픽을 sharer 집합으로 제한해 대형 멀티소켓과 ccNUMA (cache-coherent [[377_numa_allocation|Non-Uniform Memory Access]]) 시스템의 확장성을 확보한다.
> 3. **판단 포인트**: 확장성과 [[140_bandwidth|대역폭]] 효율은 뛰어나지만, [[506_directory_structure_symbol_table|디렉터리]] 저장 공간·추가 홉·컨트롤러 복잡도가 늘어나므로 소규모 [[344_bus|버스]] 기반 칩보다 수십~수백 코어 시스템에서 더 빛난다.

---

## Ⅰ. 개요 및 필요성

[[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 "누가 이 [[001_dikw_pyramid|데이터]]를 들고 있는가"를 중앙 또는 [[136_variance|분산]] 장부에 기록해 캐시 불일치를 제어하는 [[194_consistency_database_integrity|일관성]] 관리 방식이다. 멀티코어가 작을 때는 모든 코어가 [[344_bus|버스]]에서 신호를 엿듣는 [[403_snooping_protocol|스누핑 프로토콜]]만으로도 충분했지만, 코어 수가 커지면 모든 [[289_cqrs_db|쓰기]] 요청이 브로드캐스트가 되어 인터커넥트 [[140_bandwidth|대역폭]]을 먼저 소모한다. 특히 멀티소켓 서버나 [[389_mesh_topology|메시]] 네트워크 기반 칩에서는 전역 방송 자체가 비싸기 때문에, 필요한 대상만 집어내는 [[012_metadata|메타데이터]] 기반 제어가 필수다.

핵심 문제는 한 코어가 [[001_dikw_pyramid|데이터]]를 수정할 때 다른 캐시에 남아 있는 오래된 복사본을 어떻게 정확히 찾을 것인가이다. 스누핑은 "모두에게 알리고 각자 판단"하는 구조라 단순하지만, 64코어·128코어 규모에서는 대부분의 코어가 무관한 [[389_mesh_topology|메시]]지를 계속 받는다. 반면 [[506_directory_structure_symbol_table|디렉터리]]는 홈 노드가 보유자 목록을 알고 있으므로, 공유자(sharer)나 소유자(owner)에게만 무효화(Invalidate)나 [[001_dikw_pyramid|데이터]] 회수(Fetch)를 요청할 수 있다. 즉 [[506_directory_structure_symbol_table|디렉터리]]의 등장은 단순한 구현 취향이 아니라, 브로드캐스트 경제가 무너진 뒤의 필연적 진화다.

아래 그림은 왜 장부가 필요한지, 그리고 어떤 종류의 낭비를 줄이는지를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                Broadcast vs Directory Message Scope                  │
├───────────────────────────────┬──────────────────────────────────────┤
│ Snooping                      │ Directory-based                      │
├───────────────────────────────┼──────────────────────────────────────┤
│ Core0 write X                 │ Core0 write X                        │
│   └─ broadcast to all cores   │   └─ ask Home Node for sharers       │
│ Core1..Core127 all snoop      │ Home Node -> Core5, Core9 only       │
│   └─ most messages irrelevant │   └─ only real holders invalidate    │
└───────────────────────────────┴──────────────────────────────────────┘
```

이 차이는 단순히 [[389_mesh_topology|메시]]지 수 절감 이상의 의미를 가진다. 스누핑은 참여자가 늘수록 모든 코어가 비용을 함께 부담하지만, [[506_directory_structure_symbol_table|디렉터리]]는 실제 공유 관계가 희소할수록 더 큰 이득을 본다. 따라서 대규모 [[118_shared_memory|공유 메모리]] 시스템에서 [[506_directory_structure_symbol_table|디렉터리]]는 [[282_performance_tactics|성능]] 최적화 기법이 아니라 생존 조건에 가깝다.

**📢 섹션 요약 비유**: 스누핑이 아파트 전체 방송으로 "누가 택배 찾아가세요"를 외치는 방식이라면, [[506_directory_structure_symbol_table|디렉터리]]는 관리실 장부를 보고 해당 집 초인종만 누르는 방식이다. 집이 몇 세대 안 될 때는 방송도 괜찮지만, 수백 세대가 되면 관리실 장부가 더 조용하고 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 중심에는 각 메모리 블록을 담당하는 홈 노드와 그 옆의 [[506_directory_structure_symbol_table|디렉터리]] 엔트리([[506_directory_structure_symbol_table|directory]] entry)가 있다. 이 엔트리는 보통 [[178_as_is_to_be_analysis|현재 상태]], [[001_dikw_pyramid|데이터]]의 최신 소유자, 그리고 어떤 코어들이 사본을 가지고 있는지를 기록한다. 상태 표현은 구현마다 다르지만, 일반적으로 MESI (Modified, Exclusive, Shared, Invalid) 계열 상태 기계나 그 변형을 사용해 공유/독점 여부를 판단한다.

| 구성 요소 | 역할 | 설계 시 핵심 쟁점 |
| :-- | :-- | :-- |
| 홈 노드 (Home Node) | 해당 주소의 기준 메모리와 [[506_directory_structure_symbol_table|디렉터리]] 엔트리 관리 | 모든 요청이 몰리면 병목 가능 |
| [[506_directory_structure_symbol_table|디렉터리]] 엔트리 | 상태, 소유자, 공유자 집합 저장 | 저장 공간 오버헤드 |
| 요청 노드 (Requester) | 읽기/[[289_cqrs_db|쓰기]] 권한 요청 | 원격 접근 시 추가 [[015_지연_데이터_관점|지연]] |
| 공유자/소유자 | 무효화 또는 [[001_dikw_pyramid|데이터]] 전달 대상 | 응답 [[015_지연_데이터_관점|지연]] 시 전체 완료 [[015_지연_데이터_관점|지연]] |

[[506_directory_structure_symbol_table|디렉터리]]의 동작은 크게 두 단계로 이해하면 쉽다. 첫째, 읽기 요청이 오면 홈 노드는 현재 [[001_dikw_pyramid|데이터]]가 메모리에 있는지, 혹은 다른 코어의 수정 캐시에 있는지를 확인한다. 둘째, [[289_cqrs_db|쓰기]] 요청이 오면 홈 노드는 기존 공유자들에게 무효화를 보내고, 모든 응답이 돌아온 뒤 요청자에게 독점 또는 수정 권한을 준다. 결국 [[001_dikw_pyramid|데이터]] 전달보다 더 중요한 일은 **권한을 올바르게 정리하는 순서 제어**다.

다음 그림은 [[289_cqrs_db|쓰기]] 업그레이드(write upgrade)에서 홈 노드가 어떤 순서로 [[389_mesh_topology|메시]]지를 중개하는지 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                 Write Permission Flow in Directory                   │
├──────────────────────────────────────────────────────────────────────┤
│ Requester(Core0) -> Home Node : GetM(X)                             │
│ Home Node      -> Sharer(Core5): Invalidate(X)                      │
│ Home Node      -> Sharer(Core9): Invalidate(X)                      │
│ Sharer(Core5)  -> Home Node : Done                                  │
│ Sharer(Core9)  -> Home Node : Done                                  │
│ Home Node      -> Core0      : Grant Modified                       │
└──────────────────────────────────────────────────────────────────────┘
```

이 구조 덕분에 전체 네트워크가 무작정 흔들리지는 않지만, 요청이 홈 노드를 한 번 거쳐야 하므로 홉 수(hop count)가 늘어난다. 또한 코어 수만큼 [[073_bit|비트]]를 두는 풀 [[533_bit_vector_bitmap|비트 벡터]](full [[086_fenwick_tree|bit]] vector) 방식은 단순하지만 저장 비용이 크다. 그래서 실제 시스템은 제한 포인터(limited pointer), 거친 벡터(coarse vector), 계층형 [[506_directory_structure_symbol_table|디렉터리]] 같은 [[347_compaction|압축]] 구조를 사용해 [[012_metadata|메타데이터]] 비용을 줄인다.

정리하면 [[506_directory_structure_symbol_table|디렉터리]]는 "모두 듣는 구조"를 "기록을 보고 지정 전달하는 구조"로 바꾸는 기술이다. 이때 진짜 설계 난제는 [[001_dikw_pyramid|데이터]] 자체보다도, 누구에게 어떤 권한이 남아 있는지 추적하는 [[012_metadata|메타데이터]]의 정확성과 비용 균형에 있다.

**📢 섹션 요약 비유**: [[506_directory_structure_symbol_table|디렉터리]]는 도서관 대출 시스템과 같다. 책을 새로 고치려면 사서가 대출 기록을 보고 빌려 간 사람들에게 먼저 회수 연락을 돌린 뒤, 마지막에 새 판본을 한 사람에게 넘겨준다. 책장을 크게 만들수록 장부가 두꺼워지는 부담도 함께 따라온다.

---

## Ⅲ. 비교 및 연결

[[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 제대로 이해하려면 [[403_snooping_protocol|스누핑 프로토콜]]과의 경계부터 분명히 봐야 한다. 스누핑은 [[015_지연_데이터_관점|지연]] 시간이 짧고 구조가 직관적이지만, 공유 [[344_bus|버스]]나 브로드캐스트 친화적 연결망이 있어야 한다. 반면 [[506_directory_structure_symbol_table|디렉터리]]는 [[389_mesh_topology|메시]] 네트워크, 크로스바, 패킷 기반 인터커넥트에서 잘 동작하며, 코어 수가 늘수록 상대적 장점이 커진다.

| 비교 항목 | [[403_snooping_protocol|스누핑 프로토콜]] | [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| :-- | :-- | :-- |
| [[389_mesh_topology|메시]]지 범위 | 전 코어 브로드캐스트 | 실제 공유자 대상 유니캐스트/[[298_ip_classes_a_b_c_d_multicast_e_experimental|멀티캐스트]] |
| 적합 규모 | 소규모 멀티코어 | 대규모 멀티코어·멀티소켓 |
| [[015_지연_데이터_관점|지연]] 특성 | 짧지만 혼잡에 취약 | 홉 수는 늘지만 혼잡 제어에 유리 |
| [[012_metadata|메타데이터]] | 거의 없음 | [[506_directory_structure_symbol_table|디렉터리]] 저장 필요 |
| 적합 토폴로지 | 공유 [[344_bus|버스]], 간단한 링 | [[389_mesh_topology|메시]], Network-on-Chip, ccNUMA |

이 차이는 운영체제와 시스템 소프트웨어의 배치 전략에도 연결된다. ccNUMA 시스템에서 [[092_thread_lwp|스레드]]와 메모리를 같은 노드에 배치하면 홈 노드 접근이 지역화되어 [[506_directory_structure_symbol_table|디렉터리]] 트래픽이 줄어든다. 반대로 자주 쓰는 공유 [[001_dikw_pyramid|데이터]]를 여러 소켓이 번갈아 갱신하면, 하드웨어는 [[506_directory_structure_symbol_table|디렉터리]] 기반이어도 여전히 심한 캐시 라인 이동과 무효화 폭풍을 겪는다. 즉 [[506_directory_structure_symbol_table|디렉터리]]는 스누핑의 브로드캐스트 문제를 해결하지만, [[409_false_sharing|거짓 공유]]([[409_false_sharing|False Sharing]])와 과도한 공유 [[289_cqrs_db|쓰기]] 자체를 마법처럼 없애지는 못한다.

또한 최신 프로세서는 "칩 내부 소규모 클러스터는 스누핑, 칩 간 또는 [[331_neuromorphic_ai_db|슬라이스]] 간은 [[506_directory_structure_symbol_table|디렉터리]]" 같은 하이브리드 구조를 자주 사용한다. 이는 한 가지 방식이 절대적으로 우월해서가 아니라, 거리와 규모에 따라 다른 비용 함수가 지배하기 때문이다. 가까운 곳에서는 단순함이 이기고, 먼 곳에서는 [[012_metadata|메타데이터]] 기반 라우팅이 이긴다.

**📢 섹션 요약 비유**: 작은 회의실에서는 모두가 한 번에 손들어 확인하는 게 빠르지만, 여러 층으로 나뉜 회사에서는 층별 관리자 장부를 통해 필요한 사람만 호출해야 한다. 같은 조직이라도 거리와 인원에 따라 소통 방식이 달라지는 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 보통 "선택 여부"보다 "이 특성을 알고 소프트웨어를 배치했는가"로 성패가 갈린다. 대형 서버에서 메모리 접근이 느린 이유가 단순한 [[251_dram|DRAM]] (Dynamic Random Access Memory) 속도 부족이 아니라, 원격 홈 노드 조회와 무효화 대기 때문인 경우가 많다. 따라서 [[282_performance_tactics|성능]] 분석 시에는 평균 메모리 [[015_지연_데이터_관점|지연]]만 보지 말고, 어떤 코어가 어느 노드의 [[001_dikw_pyramid|데이터]]를 얼마나 자주 수정하는지까지 봐야 한다.

### 설계·운영 [[435_checklist_based_testing|체크리스트]]

1. **대규모 공유 [[289_cqrs_db|쓰기]] 회피**: 전역 [[059_counter|카운터]], 전역 락, hot cache line을 여러 소켓이 함께 갱신하지 않는가?
2. **[[377_numa_allocation|NUMA]] 지역성 확보**: [[092_thread_lwp|스레드]] 배치와 메모리 배치를 같은 노드에 묶어 홈 노드 원격 접근을 줄였는가?
3. **공유자 수 관리**: 읽기 전용 [[001_dikw_pyramid|데이터]]는 널리 [[016_replication_factor|복제]]해도 되지만, 자주 쓰는 [[001_dikw_pyramid|데이터]]는 분할([[243_sharding_horizontal_scaling_database|sharding]])이나 [[016_replication_factor|복제]] 후 병합(reduction) 구조가 더 나은가?
4. **[[506_directory_structure_symbol_table|디렉터리]] 구조 선택**: 풀 [[533_bit_vector_bitmap|비트 벡터]]가 필요한 규모인가, 제한 포인터나 계층형 구조가 더 현실적인가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 코어 수만 늘리면 확장된다고 믿고, 모든 워커가 하나의 상태 객체를 계속 갱신하게 두는 설계
- [[377_numa_allocation|NUMA]] 배치를 무시해 원격 홈 노드 왕복이 기본 경로가 된 [[090_service_kubernetes_network_load_balancing|서비스]]
- [[506_directory_structure_symbol_table|디렉터리]] 도입으로 모든 [[194_consistency_database_integrity|일관성]] 비용이 사라졌다고 오해하고 false sharing을 방치하는 코드

기술사 답안 관점에서는 "왜 스누핑 대신 [[506_directory_structure_symbol_table|디렉터리]]를 쓰는가"와 함께 "[[506_directory_structure_symbol_table|디렉터리]]도 완벽하지 않다"를 같이 말해야 점수가 산다. 즉 확장성을 얻는 대가로 [[012_metadata|메타데이터]] 오버헤드, 컨트롤러 복잡도, 추가 [[015_지연_데이터_관점|지연]]이 생긴다는 균형 감각이 중요하다. 채택 조건은 대규모 확장성과 패킷 기반 인터커넥트이고, 회피 조건은 소규모 칩에서의 단순·저지연 요구다.

**📢 섹션 요약 비유**: 대형 창고에서 물건 위치를 장부로 관리하면 찾을 물건만 정확히 집을 수 있지만, 장부를 갱신하지 않거나 창고 구역 배치를 엉망으로 해두면 오히려 더 오래 헤맨다. 좋은 [[506_directory_structure_symbol_table|디렉터리]] 시스템은 장부 자체보다도 배치 규율을 함께 지킬 때 효과가 난다.

---

## Ⅴ. 기대효과 및 결론

[[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 가장 큰 성과는 [[402_cache_coherence|캐시 일관성]]의 비용을 "모든 코어의 상시 부담"에서 "실제 공유 관계에 비례한 부담"으로 바꿨다는 점이다. 이 변화 덕분에 대형 서버와 many-core 프로세서는 브로드캐스트 폭풍 없이도 [[118_shared_memory|공유 메모리]] 프로그래밍 모델을 유지할 수 있게 되었다. 다시 말해 [[506_directory_structure_symbol_table|디렉터리]]는 확장성과 프로그래밍 편의 사이의 다리를 놓은 기술이다.

물론 한계도 분명하다. [[506_directory_structure_symbol_table|디렉터리]] 엔트리를 위한 [[250_sram|SRAM]] (Static Random Access Memory) 공간이 필요하고, 홈 노드가 병목이 되면 [[015_지연_데이터_관점|지연]]이 눈에 띄게 늘어난다. 그래서 최신 설계는 단일 중앙 장부보다 [[136_variance|분산]] [[506_directory_structure_symbol_table|디렉터리]], 캐시 [[331_neuromorphic_ai_db|슬라이스]] 연계 [[506_directory_structure_symbol_table|디렉터리]], 계층형 [[506_directory_structure_symbol_table|디렉터리]]처럼 [[012_metadata|메타데이터]] 자체를 [[136_variance|분산]]하는 방향으로 발전한다. 앞으로는 패키지 내부 네트워크와 메모리 계층이 더 복잡해질수록, [[001_dikw_pyramid|데이터]]보다 [[012_metadata|메타데이터]]를 얼마나 싸고 빠르게 움직이느냐가 경쟁력이 된다.

결론적으로 [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 "브로드캐스트를 포기하고 추적을 선택한" 아키텍처다. 작은 시스템에서는 과한 선택일 수 있지만, 규모가 커질수록 이 장부 없이는 [[194_consistency_database_integrity|일관성]] 자체가 유지되지 않는다. 따라서 이 개념은 단순한 캐시 기법이 아니라, 대규모 공유 시스템이 질서를 유지하는 운영 원리로 기억하는 것이 가장 정확하다.

**📢 섹션 요약 비유**: 도시가 커질수록 길 안내 방송보다 주소 [[001_dikw_pyramid|데이터]]베이스가 중요해진다. [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 거대한 도시에서 "누가 어디에 있는지"를 추적해 교통 혼란 없이 움직이게 하는 주소 체계와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[402_cache_coherence|캐시 일관성]] ([[402_cache_coherence|Cache Coherence]]) | 여러 캐시에 [[016_replication_factor|복제]]된 [[001_dikw_pyramid|데이터]]의 최신성 규칙을 보장하는 상위 목표 |
| [[403_snooping_protocol|스누핑 프로토콜]] ([[403_snooping_protocol|Snooping Protocol]]) | [[506_directory_structure_symbol_table|디렉터리]]와 대비되는 브로드캐스트 기반 [[194_consistency_database_integrity|일관성]] 방식 |
| ccNUMA (cache-coherent [[377_numa_allocation|Non-Uniform Memory Access]]) | [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 대표적으로 쓰이는 대규모 [[118_shared_memory|공유 메모리]] 구조 |
| MESI (Modified, Exclusive, Shared, Invalid) | [[506_directory_structure_symbol_table|디렉터리]] 엔트리와 캐시 컨트롤러가 권한 상태를 표현할 때 자주 쓰는 상태 모델 |
| [[409_false_sharing|거짓 공유]] ([[409_false_sharing|False Sharing]]) | [[506_directory_structure_symbol_table|디렉터리]]가 있어도 여전히 [[282_performance_tactics|성능]]을 망가뜨릴 수 있는 공유 [[289_cqrs_db|쓰기]] 병목 |
| [[136_variance|분산]] [[506_directory_structure_symbol_table|디렉터리]] (Distributed [[506_directory_structure_symbol_table|Directory]]) | 홈 노드 병목을 줄이기 위해 [[012_metadata|메타데이터]]를 여러 [[331_neuromorphic_ai_db|슬라이스]]에 [[136_variance|분산]]하는 확장 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
공유 버스 기반 일관성
    │
    ▼
스누핑 프로토콜 (Snooping Protocol)
    │
    ▼
디렉터리 기반 프로토콜 (Directory-based Protocol)
    │
    ├─▶ ccNUMA (cache-coherent Non-Uniform Memory Access)
    │
    ├─▶ 제한 포인터 / 계층형 디렉터리
    │
    ▼
분산 디렉터리 · many-core · 패킷 기반 인터커넥트
```

이 흐름은 "전역 방송"에서 "[[012_metadata|메타데이터]] 기반 지정 전달"로, 다시 "[[012_metadata|메타데이터]] 자체의 [[136_variance|분산]]"으로 진화하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[506_directory_structure_symbol_table|디렉터리]] 기반 [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 누가 같은 책을 빌려 갔는지 선생님 장부에 적어 두는 규칙이에요.
2. 누군가 책 내용을 고치면 선생님이 장부를 보고 그 책을 가진 친구들에게만 "옛날 거 지워"라고 말해요.
3. 그래서 친구가 엄청 많아져도 교실 전체가 시끄러워지지 않고, 필요한 친구만 정확히 움직일 수 있어요.
