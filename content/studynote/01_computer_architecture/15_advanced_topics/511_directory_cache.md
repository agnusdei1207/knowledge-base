---
title: 511. 디렉터리 캐시 (Directory Cache)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[506_directory_structure_symbol_table|디렉터리]] 캐시 ([[506_directory_structure_symbol_table|Directory]] Cache)는 [[402_cache_coherence|캐시 일관성]]에 필요한 sharer·owner [[012_metadata|메타데이터]]를 작은 고속 [[250_sram|SRAM]] (Static Random Access Memory)에 보관해, [[506_directory_structure_symbol_table|디렉터리]] 조회 [[015_지연_데이터_관점|지연]]을 줄이는 [[012_metadata|메타데이터]] 전용 캐시다.
> 2. **가치**: 대규모 멀티코어와 멀티소켓 시스템에서는 [[001_dikw_pyramid|데이터]]보다 권한 정보 조회가 먼저 병목이 되기 쉬운데, [[506_directory_structure_symbol_table|디렉터리]] 캐시는 자주 공유되는 라인의 권한 결정을 빠르게 해 coherence traffic을 더 짧은 경로로 처리하게 돕는다.
> 3. **판단 포인트**: 크기만 키운다고 좋은 것이 아니라 엔트리 표현 방식, [[263_cache_hit_miss|hit]] rate, eviction 시 [[002_bigdata_5v|정확성]] 보장, snoop filter와의 역할 분담까지 함께 설계해야 효과가 난다.

---

## Ⅰ. 개요 및 필요성

[[506_directory_structure_symbol_table|디렉터리]] 캐시는 대규모 [[402_cache_coherence|캐시 일관성]] 시스템에서 "누가 이 캐시 라인을 들고 있는가"라는 [[012_metadata|메타데이터]]를 빠르게 찾기 위한 전용 버퍼다. [[404_directory_based_protocol|디렉터리 기반 프로토콜]] ([[404_directory_based_protocol|Directory-based Protocol]])은 브로드캐스트 대신 sharer 목록을 참고해 필요한 캐시에만 무효화나 [[001_dikw_pyramid|데이터]] 전달 요청을 보낸다. 그런데 이 장부가 항상 멀리 있는 메모리나 큰 [[506_directory_structure_symbol_table|디렉터리]] 배열에만 있으면, [[001_dikw_pyramid|데이터]]는 가까운데 권한 [[396_validation|확인]]이 느려서 coherence 경로 전체가 [[015_지연_데이터_관점|지연]]될 수 있다.

즉 [[506_directory_structure_symbol_table|디렉터리]] 캐시의 필요성은 [[001_dikw_pyramid|데이터]] [[264_hit_ratio|적중률]] 문제가 아니라 **권한 [[264_hit_ratio|적중률]] 문제**에서 나온다. 코어가 어떤 라인에 [[289_cqrs_db|쓰기]]를 하려면 먼저 누가 그 라인을 공유 중인지 알아야 하고, 수정된 [[001_dikw_pyramid|데이터]]를 누가 들고 있는지도 알아야 한다. 이 [[012_metadata|메타데이터]]가 느리면 읽기·[[289_cqrs_db|쓰기]] 요청은 실제 [[001_dikw_pyramid|데이터]] 접근 전에 홈 노드(Home Node) 조회에서 발이 묶인다.

특히 shared working set이 전체 메모리에 비해 훨씬 작을 때 [[506_directory_structure_symbol_table|디렉터리]] 캐시는 큰 효과를 낸다. 시스템 전체 주소 공간에 대한 모든 [[506_directory_structure_symbol_table|디렉터리]] 엔트리를 항상 빠른 SRAM에 둘 수는 없지만, 자주 접근되는 소수의 hot line [[012_metadata|메타데이터]]만 가까이에 두면 많은 coherence 요청을 짧은 경로로 해결할 수 있기 때문이다.

- **📢 섹션 요약 비유**: [[506_directory_structure_symbol_table|디렉터리]] 캐시는 대형 도서관의 "최근 대출 기록 메모"와 같다. 전체 장부는 창고에 있어도, 자주 묻는 책의 대출 현황만 사서 책상 위에 두면 훨씬 빨리 안내할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[506_directory_structure_symbol_table|디렉터리]] 캐시는 보통 [[744_load_line_calibration|LLC]] (Last Level Cache) [[331_neuromorphic_ai_db|슬라이스]], 홈 에이전트, 메모리 컨트롤러 근처에 놓인다. 엔트리에는 주소 태그, [[194_consistency_database_integrity|일관성]] 상태, owner, sharer 집합, 대기 중인 무효화 여부 같은 제어 정보가 담긴다. 핵심은 [[001_dikw_pyramid|데이터]] 본문이 아니라 "권한 [[012_metadata|메타데이터]]"를 캐시한다는 점이다.

이 그림은 [[506_directory_structure_symbol_table|디렉터리]] 캐시 hit와 miss가 coherence 경로를 어떻게 갈라놓는지를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│            디렉터리 캐시는 데이터가 아니라 권한 정보를 가속한다      │
├──────────────────────────────────────────────────────────────────────┤
│ Requesting Core                                                     │
│      │                                                              │
│      ▼                                                              │
│ Home Agent / LLC Slice                                              │
│      │                                                              │
│      ├─ hit  ─▶ Directory Cache ─▶ sharer/owner 즉시 확인           │
│      │                         └─ targeted invalidate / data fetch   │
│      │                                                              │
│      └─ miss ─▶ Backing Directory in LLC/Memory                     │
│                                ├─ 메타데이터 조회                   │
│                                └─ 엔트리 채움 후 coherence 진행     │
│                                                                      │
│ 결과: hit면 권한 부여가 짧아지고, miss면 coherence 지연이 길어진다  │
└──────────────────────────────────────────────────────────────────────┘
```

| 엔트리 필드 | 의미 | 설계 포인트 |
| :--- | :--- | :--- |
| Tag / Home 정보 | 어떤 라인의 권한 정보인지 [[655_ir_detection_analysis|식별]] | 주소 [[136_variance|분산]] 방식과 함께 결정 |
| 상태 [[073_bit|비트]] | Shared, Modified, Invalid 등 | MESI / MOESI 계열과 연동 |
| Owner | 최신 수정본 책임자 | cache-to-cache 전달 판단에 중요 |
| Sharer 정보 | 누가 사본을 갖는지 기록 | full [[086_fenwick_tree|bit]] vector, limited pointer, coarse vector 중 선택 |
| Pending [[073_bit|비트]] | 무효화·응답 대기 상태 | [[213_race_condition|race condition]] 방지에 필요 |

sharer 표현 방식도 핵심이다. 코어 수가 적다면 full [[086_fenwick_tree|bit]] vector가 단순하고 정확하지만, 수십~수백 코어로 가면 엔트리 크기가 너무 커진다. 그래서 실제 시스템은 제한 포인터, [[347_compaction|압축]] [[073_bit|비트]]벡터, 희소 [[506_directory_structure_symbol_table|디렉터리]] (Sparse [[506_directory_structure_symbol_table|Directory]]) 같은 방식을 써서 [[012_metadata|메타데이터]] 크기를 줄인다. 결국 [[506_directory_structure_symbol_table|디렉터리]] 캐시는 "빠르게 두고 싶은 정보"와 "너무 커서 다 둘 수 없는 정보" 사이에서 균형을 잡는 장치다.

또한 miss 처리 전략도 중요하다. backing directory에서 [[012_metadata|메타데이터]]를 읽어와 채울 수도 있고, 구현에 따라 보수적으로 더 넓은 snoop를 날려 [[002_bigdata_5v|정확성]]을 지킬 수도 있다. 즉 [[506_directory_structure_symbol_table|디렉터리]] 캐시는 hit일 때 빠르지만, miss 시 어떻게 [[002_bigdata_5v|정확성]]과 비용을 맞추는지가 설계 완성도를 좌우한다.

- **📢 섹션 요약 비유**: [[506_directory_structure_symbol_table|디렉터리]] 캐시는 택배 분류장의 빠른 조회대와 같다. 자주 오가는 상자의 위치 정보는 앞쪽 화면에 띄워 두고, 드문 물건만 뒤 창고 장부를 뒤져 찾는다.

---

## Ⅲ. 비교 및 연결

[[506_directory_structure_symbol_table|디렉터리]] 캐시는 전체 [[506_directory_structure_symbol_table|디렉터리]] 자체와 같지 않다. 전체 [[506_directory_structure_symbol_table|디렉터리]]는 [[002_bigdata_5v|정확성]]의 원천이고, [[506_directory_structure_symbol_table|디렉터리]] 캐시는 그중 hot metadata를 빠르게 보관하는 가속 장치다. 또한 snoop filter와도 닮았지만 완전히 같지는 않다. snoop filter는 불필요한 probe를 줄이는 데 초점이 있고, [[506_directory_structure_symbol_table|디렉터리]] 캐시는 sharer/owner 정보를 적극적으로 저장해 권한 결정을 빠르게 하는 데 초점이 있다.

| 구조 | 주 역할 | 장점 | 약점 |
| :--- | :--- | :--- | :--- |
| 전체 [[506_directory_structure_symbol_table|디렉터리]] (Backing [[506_directory_structure_symbol_table|Directory]]) | 정확한 권한 정보의 기준 저장소 | 완전성 보장 | 크고 느릴 수 있음 |
| [[506_directory_structure_symbol_table|디렉터리]] 캐시 | hot [[012_metadata|metadata]] 가속 | coherence [[263_cache_hit_miss|hit]] 경로 단축 | miss 시 이득 감소 |
| 스누프 필터 (Snoop Filter) | 불필요한 probe 감소 | 브로드캐스트 부담 완화 | 구현에 따라 보수적 false positive 가능 |

이 개념은 포함형 [[744_load_line_calibration|LLC]] (Inclusive [[744_load_line_calibration|LLC]])와도 자주 연결된다. 상위 캐시에 있는 라인이 하위 사본 정보를 암시하거나 직접 포함하면, [[744_load_line_calibration|LLC]] 태그가 사실상 [[506_directory_structure_symbol_table|디렉터리]] 캐시 역할을 수행할 수 있다. 반대로 비포함형 구조에서는 별도의 [[012_metadata|메타데이터]] 저장 구조를 더 적극적으로 둬야 할 수 있다.

또한 [[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]]), [[497_chiplet|칩렛]], [[441_cxl|CXL]].cache 같은 [[136_variance|분산]] 메모리 환경으로 갈수록 [[506_directory_structure_symbol_table|디렉터리]] 캐시의 중요성은 더 커진다. 거리가 멀수록 [[001_dikw_pyramid|데이터]] 왕복만 비싼 것이 아니라, 권한 [[396_validation|확인]] 왕복도 비싸지기 때문이다. 그래서 대규모 시스템에서는 "[[001_dikw_pyramid|데이터]] 캐시 + [[506_directory_structure_symbol_table|디렉터리]] 캐시"를 같이 봐야 실제 coherence 비용이 보인다.

- **📢 섹션 요약 비유**: 전체 [[506_directory_structure_symbol_table|디렉터리]]가 본사 장부라면, [[506_directory_structure_symbol_table|디렉터리]] 캐시는 지점 [[059_counter|카운터]] 메모이고, snoop filter는 손님이 어느 지점으로 갈지 먼저 걸러 주는 안내 데스크에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[506_directory_structure_symbol_table|디렉터리]] 캐시의 [[263_cache_hit_miss|hit]] rate가 곧 coherence latency를 좌우하는 경우가 많다. 자주 공유되는 라인의 [[012_metadata|메타데이터]]가 홈 에이전트 가까이에 있으면 [[289_cqrs_db|쓰기]] 권한 업그레이드와 cache-to-cache 전달이 빠르게 끝난다. 반대로 [[483_active_vs_passive_ftp|active]] sharing이 넓게 퍼져 있고 엔트리 크기가 커서 캐시가 자주 쫓겨나면, 시스템은 backing [[506_directory_structure_symbol_table|directory]] 조회나 보수적 재탐색 때문에 예상보다 큰 [[015_지연_데이터_관점|지연]]을 겪는다.

설계에서 가장 까다로운 지점은 eviction이다. 살아 있는 sharer 정보가 담긴 엔트리를 그냥 버리면 [[002_bigdata_5v|정확성]]이 깨질 수 있으므로, 엔트리를 backing directory에 기록하거나 기존 사본을 정리한 뒤 버려야 한다. 즉 [[001_dikw_pyramid|데이터]] 캐시보다 더 엄격한 [[194_consistency_database_integrity|일관성]] 규칙이 필요하며, eviction 정책은 [[282_performance_tactics|성능]] 정책이면서 동시에 [[002_bigdata_5v|정확성]] 정책이다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. [[506_directory_structure_symbol_table|디렉터리]] 캐시 [[263_cache_hit_miss|hit]] 시와 miss 시 coherence [[015_지연_데이터_관점|지연]] 차이는 얼마나 큰가?
2. sharer 표현 방식이 코어 수 대비 과도하게 비대하지 않은가?
3. eviction 시 [[012_metadata|메타데이터]] [[277_write_back|write-back]] 또는 보수적 invalidation 절차가 정의되어 있는가?
4. inclusive [[744_load_line_calibration|LLC]], snoop filter, home agent와 역할이 중복되거나 비어 있지 않은가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[001_dikw_pyramid|데이터]] 캐시처럼 단순 LRU만 생각하고 eviction의 [[002_bigdata_5v|정확성]] 비용을 무시하는 설계
- core count 증가에 따라 엔트리 크기 폭증을 방치하는 full [[086_fenwick_tree|bit]] vector 남발
- [[506_directory_structure_symbol_table|디렉터리]] 캐시가 있으니 false sharing이나 과도한 공유 [[289_cqrs_db|쓰기]] 병목도 사라질 것이라 오해하는 판단

기술사 답안에서는 "[[506_directory_structure_symbol_table|디렉터리]] 캐시는 대규모 시스템에서 [[506_directory_structure_symbol_table|디렉터리]] 조회를 빠르게 한다"를 기본으로 쓰되, **[[263_cache_hit_miss|hit]] rate·엔트리 [[347_compaction|압축]]·eviction [[002_bigdata_5v|정확성]]**까지 언급해야 깊이가 생긴다. 즉 이 구조는 단순한 버퍼가 아니라, coherence [[012_metadata|메타데이터]]의 지역성을 활용하는 가속 장치다.

- **📢 섹션 요약 비유**: [[506_directory_structure_symbol_table|디렉터리]] 캐시 설계는 자주 찾는 고객 명단을 프런트 책상에 둘지, 전산실 장부에서 매번 조회할지 정하는 일과 같다. 잘 두면 응대가 빨라지지만, 기록을 잘못 버리면 고객 안내 자체가 틀어진다.

---

## Ⅴ. 기대효과 및 결론

[[506_directory_structure_symbol_table|디렉터리]] 캐시의 가장 큰 효과는 [[001_dikw_pyramid|데이터]]보다 앞서야 하는 권한 결정을 빠르게 만든다는 점이다. 이 덕분에 대규모 멀티코어와 멀티소켓 시스템에서도 무작정 브로드캐스트하지 않고, 필요한 코어만 겨냥한 coherence 제어를 더 짧은 [[015_지연_데이터_관점|지연]]으로 수행할 수 있다. 즉 [[506_directory_structure_symbol_table|디렉터리]] 캐시는 대규모 [[194_consistency_database_integrity|일관성]] 시스템의 확장성을 떠받치는 "[[012_metadata|메타데이터]] 가속기"라고 볼 수 있다.

하지만 한계도 분명하다. [[012_metadata|메타데이터]] 저장 공간이 늘고, sharer 표현이 복잡해지며, miss와 eviction 경로가 설계를 어렵게 만든다. 그래서 미래 방향은 더 큰 단일 캐시가 아니라, 계층형 [[506_directory_structure_symbol_table|디렉터리]] 캐시, [[136_variance|분산]] 홈 에이전트, region 기반 tracking, 가속기 coherence를 고려한 부분 [[506_directory_structure_symbol_table|디렉터리]]처럼 "필요한 권한 정보만 정확하게 가까이 두는 구조"로 향한다.

결론적으로 [[506_directory_structure_symbol_table|디렉터리]] 캐시는 [[001_dikw_pyramid|데이터]] 캐시의 보조가 아니라, 대규모 coherence의 [[282_performance_tactics|성능]]을 결정하는 별도의 핵심 계층이다. 이 개념은 **[[001_dikw_pyramid|데이터]]를 빠르게 읽는 기술이 아니라, [[001_dikw_pyramid|데이터]]를 누가 읽고 쓸 권리가 있는지 빠르게 판단하는 기술**로 기억해야 한다.

- **📢 섹션 요약 비유**: [[506_directory_structure_symbol_table|디렉터리]] 캐시는 도시 교통의 [[130_signal|신호]] 제어실과 같다. 자동차 자체를 더 빠르게 만드는 것이 아니라, 누가 어느 길을 먼저 써야 하는지 빨리 판단해 도시 전체 흐름을 살린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[404_directory_based_protocol|디렉터리 기반 프로토콜]] ([[404_directory_based_protocol|Directory-based Protocol]]) | [[506_directory_structure_symbol_table|디렉터리]] 캐시가 가속하는 상위 coherence 메커니즘이다. |
| 홈 노드 (Home Node) | [[506_directory_structure_symbol_table|디렉터리]] 캐시가 배치되는 대표 위치이며 권한 판단의 중심이다. |
| sharer / owner 정보 | [[506_directory_structure_symbol_table|디렉터리]] 캐시가 저장하는 핵심 [[012_metadata|메타데이터]]다. |
| 희소 [[506_directory_structure_symbol_table|디렉터리]] (Sparse [[506_directory_structure_symbol_table|Directory]]) | 전체 메모리 대신 활성 공유 라인만 추적해 공간을 줄인다. |
| 스누프 필터 (Snoop Filter) | 불필요한 probe를 줄인다는 점에서 역할이 닮아 있다. |
| [[377_numa_allocation|NUMA]] / [[497_chiplet|칩렛]] 인터커넥트 | 권한 정보 조회 [[015_지연_데이터_관점|지연]]이 더 커져 [[506_directory_structure_symbol_table|디렉터리]] 캐시 가치가 커지는 환경이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
스누핑 확장성 한계
        │
        ▼
디렉터리 기반 프로토콜 (Directory-based Protocol)
        │
        ▼
backing directory in LLC / memory
        │
        ▼
디렉터리 캐시 (Directory Cache)
        │
        ├─▶ 희소 디렉터리 · sharer 압축
        ├─▶ inclusive LLC 기반 snoop filter
        ├─▶ 분산 home agent
        │
        ▼
칩렛 · NUMA · CXL.cache 대응 메타데이터 계층화
```

이 흐름은 "브로드캐스트 회피"에서 출발해, "권한 장부를 빠르게 만들고 [[136_variance|분산]]하는 방향"으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[506_directory_structure_symbol_table|디렉터리]] 캐시는 누가 같은 장난감을 빌려 갔는지 적어 둔 빠른 메모장이에요.
2. 자주 찾는 장난감은 큰 장부를 뒤지지 않고 이 메모장만 보면 바로 알 수 있어요.
3. 그래서 친구가 많아져도 필요한 친구에게만 빨리 연락할 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 511 / 803

← **이전**: [[510_snooping_bus_bottleneck|510. 스누핑 버스 병목 현상 (Snooping Bus Bottleneck)]]
**다음**: [[512_mesi_protocol_states|512. 메시 프로토콜 상태 전이도 (MESI Protocol State Transition Diagram)]] →

---
