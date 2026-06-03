+++
weight = 302
title = "302. 클럭 알고리즘 (Clock Algorithm)"
date = "2026-04-20"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[264_clock_algorithm_nur|클럭 알고리즘]] ([[045_clock|Clock]] [[001_algorithm_definition|Algorithm]])은 [[262_lru_page_replacement|LRU]] ([[262_lru_page_replacement|Least Recently Used]])의 높은 구현 비용을 줄이기 위해, [[286_page_frame|페이지]]별 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] ([[316_reference_pattern_nosql|Reference]] [[086_fenwick_tree|Bit]])와 원형 포인터를 이용해 "최근에 안 쓰인 [[286_page_frame|페이지]]"를 빠르게 찾는 [[260_page_replacement|페이지 교체]] 기법이다.
> 2. **가치**: 정확한 최근 순위를 끝까지 추적하지 않아도 [[247_temporal_locality|시간적 지역성]] ([[247_temporal_locality|Temporal Locality]])을 상당 부분 보존하므로, 대규모 가상 메모리에서 성능과 구현 복잡도의 균형점이 된다.
> 3. **판단 포인트**: 이 [[001_algorithm_definition|알고리즘]]의 핵심은 "누가 가장 오래전에 쓰였는가"가 아니라 "한 바퀴 도는 동안 다시 쓰였는가"이며, 실제 [[001_operating_system_purpose|운영체제]]는 [[278_dirty_bit|더티 비트]] ([[396_dirty_bit|Dirty Bit]])·활성/비활성 리스트와 결합해 이를 더욱 실용적으로 확장한다.

---

## Ⅰ. 개요 및 필요성

[[264_clock_algorithm_nur|클럭 알고리즘]]은 메모리에 적재된 [[286_page_frame|페이지]]를 원형으로 바라보며, 시계 바늘처럼 움직이는 포인터가 교체 대상을 찾는 [[401_page_replacement_algorithms|페이지 교체 알고리즘]]이다. [[001_operating_system_purpose|운영체제]]는 [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]])가 발생할 때마다 희생 [[286_page_frame|페이지]]를 골라야 하는데, 이 판단이 느리면 메모리를 아끼려다가 오히려 CPU 시간을 잃게 된다. 그래서 이 [[001_algorithm_definition|알고리즘]]은 "교체 [[164_policy|정책]]이 똑똑해야 한다"는 요구와 "[[164_policy|정책]] 자체가 너무 무거우면 안 된다"는 현실을 동시에 만족시키기 위해 등장했다.

[[261_fifo_page_replacement|FIFO]] ([[261_fifo_page_replacement|First-In First-Out]])는 구현이 단순하지만 오래 있었을 뿐 지금도 자주 쓰이는 [[286_page_frame|페이지]]를 내쫓을 수 있다. 반대로 LRU는 이론적으로 합리적이지만, 모든 [[286_page_frame|페이지]] 접근의 시간 순서를 세밀하게 기록하려면 하드웨어 지원이나 관리 오버헤드가 커진다. [[264_clock_algorithm_nur|클럭 알고리즘]]은 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] 하나만으로 최근 사용 흔적을 남기고, 그 흔적이 없는 [[286_page_frame|페이지]]를 우선 교체함으로써 두 극단 사이를 메운다.

이 개념을 이해할 때 중요한 점은 [[264_clock_algorithm_nur|클럭 알고리즘]]이 "완벽한 기억"을 포기한 대신 "충분히 최근"이라는 현실적인 기준을 채택했다는 사실이다. 메모리 [[286_page_frame|페이지]] 수가 수천, 수만 개로 커질수록 정확한 순위표를 유지하는 비용은 급증하지만, [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]를 기반으로 한 순회 방식은 [[286_page_frame|페이지]] 수가 커져도 구조가 단순하게 유지된다.

이 그림은 [[264_clock_algorithm_nur|클럭 알고리즘]]이 [[286_page_frame|페이지]]를 어떻게 원형으로 훑으면서 교체 대상을 고르는지 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│               클럭 알고리즘의 기본 관점: 원형 순회 + 참조 비트 검사       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│                  ┌──────┐      ┌──────┐      ┌──────┐                     │
│                  │ P0,R=1│ ───▶ │ P1,R=0│ ───▶ │ P2,R=1│                    │
│                  └──────┘      └──────┘      └──────┘                     │
│                      ▲                                   │                │
│                      │                                   ▼                │
│                  ┌──────┐ ◀─── ┌──────┐ ◀─── ┌──────┐                     │
│                  │ P5,R=1│      │ P4,R=0│      │ P3,R=1│                    │
│                  └──────┘      └──────┘      └──────┘                     │
│                                                                            │
│  Clock Hand ─▶ P0 검사: R=1 이면 0으로 낮추고 통과                        │
│                 P1 검사: R=0 이면 교체 후보로 선택                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심은 포인터가 처음 만난 `R=0` [[286_page_frame|페이지]]를 바로 선택한다는 점이다. 즉, 순차적으로 줄을 세워 최하위를 찾는 것이 아니라, "최근에 다시 호출받지 못한 [[286_page_frame|페이지]]"를 순회 중 발견하는 즉시 교체한다. 덕분에 구현은 단순하면서도 [[247_temporal_locality|시간적 지역성]]이 어느 정도 반영된다.

- **📢 섹션 요약 비유**: [[264_clock_algorithm_nur|클럭 알고리즘]]은 도서관 사서가 책장 전체 이용 기록을 정밀 분석하는 대신, 한 바퀴 돌 동안 대출 표시가 다시 붙지 않은 책을 먼저 창고로 보내는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[264_clock_algorithm_nur|클럭 알고리즘]]의 작동은 하드웨어와 [[001_operating_system_purpose|운영체제]]의 역할 분담으로 이해해야 한다. [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]])는 어떤 [[286_page_frame|페이지]]가 읽히거나 쓰일 때 해당 [[286_page_frame|페이지]] 엔트리의 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]를 1로 세팅한다. [[001_operating_system_purpose|운영체제]]는 [[260_page_replacement|페이지 교체]]가 필요할 때 포인터가 가리키는 [[286_page_frame|페이지]]의 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]를 읽고, 값이 1이면 "최근에 쓰였다"고 판단해 0으로 지운 뒤 다음 [[286_page_frame|페이지]]로 넘어간다. 반대로 값이 0이면 최근 순회 이후 다시 쓰이지 않았다고 보고 희생 [[286_page_frame|페이지]]로 선정한다.

이 방식이 "[[407_second_chance_algorithm|2차 기회 알고리즘]] ([[407_second_chance_algorithm|Second Chance Algorithm]])"으로도 불리는 이유가 여기에 있다. [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]가 1인 [[286_page_frame|페이지]]는 바로 제거되지 않고 한 번 더 기회를 받는다. 만약 정말 중요한 [[286_page_frame|페이지]]라면 다음 순회가 오기 전에 다시 접근되어 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]가 또 1로 올라갈 것이고, 그렇지 않다면 결국 0 상태로 남아 교체된다.

| 구성 요소 | 역할 | 설계 의미 |
| :-- | :-- | :-- |
| [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] ([[316_reference_pattern_nosql|Reference]] [[086_fenwick_tree|Bit]]) | 최근 접근 여부를 기록 | LRU의 최근성 정보를 1비트로 근사 |
| 클럭 포인터 ([[045_clock|Clock]] Hand) | 원형 큐를 순회 | 교체 탐색 비용을 순차 스캔으로 단순화 |
| 프레임 집합 (Frame Set) | 현재 메모리에 있는 [[286_page_frame|페이지]]들 | [[387_page_fault|페이지 부재]] 시 교체 후보 풀 제공 |
| [[387_page_fault|페이지 부재]] 처리기 | 희생 [[260_page_replacement|페이지 교체]] 실행 | 스왑 I/O와 [[164_policy|정책]] 판단이 만나는 지점 |

이 그림은 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]가 교체 판단에서 어떻게 "즉시 교체"와 "기회 부여"로 갈라지는지 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                 참조 비트 기반 교체 흐름: 1이면 유예, 0이면 교체          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  페이지 부재 발생                                                          │
│         │                                                                  │
│         ▼                                                                  │
│  Clock Hand가 현재 프레임 확인                                             │
│         │                                                                  │
│         ▼                                                                  │
│   참조 비트 = 1 ?                                                          │
│      ├─ 예 ─▶ 참조 비트 0으로 초기화 ─▶ 다음 프레임으로 이동               │
│      │                                                                     │
│      └─ 아니오 ─▶ 희생 페이지 선택 ─▶ 새 페이지 적재 ─▶ 포인터 전진        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

중요한 트레이드오프는 탐색 길이와 [[571_protection_vs_security|보호]] 효과 사이에 있다. 메모리 압박이 약할 때는 많은 [[286_page_frame|페이지]]가 최근에 [[316_reference_pattern_nosql|참조]]되어 `R=1` 상태이므로 포인터가 여러 칸을 지나가며 많은 [[286_page_frame|페이지]]를 [[571_protection_vs_security|보호]]한다. 반대로 메모리 압박이 심할수록 한 바퀴 안에 `R=0` [[286_page_frame|페이지]]를 빨리 만나게 되고, 그만큼 교체가 공격적으로 일어난다. 즉, [[264_clock_algorithm_nur|클럭 알고리즘]]은 워크로드의 최근 사용 패턴에 따라 자동으로 완급이 조절되는 구조다.

- **📢 섹션 요약 비유**: [[264_clock_algorithm_nur|클럭 알고리즘]]은 청소 도우미가 각 방 문고리에 "방금 사용함" 표지를 보고, 표지가 있으면 떼어 두고 다음에 다시 와 보며, 두 번째에도 표지가 없으면 그 방을 정리 대상으로 삼는 방식과 같다.

---

## Ⅲ. 비교 및 연결

[[264_clock_algorithm_nur|클럭 알고리즘]]의 위치를 분명히 하려면 [[261_fifo_page_replacement|FIFO]], [[262_lru_page_replacement|LRU]], 그리고 [[303_nur|NUR]] ([[303_nur|Not Used Recently]]) 계열과 비교해야 한다. FIFO는 들어온 순서만 보므로 지역성을 반영하지 못하고, LRU는 최근 사용 정보를 가장 정교하게 반영하지만 구현 부담이 크다. [[264_clock_algorithm_nur|클럭 알고리즘]]은 "최근에 쓰였는가"만 간단히 반영하므로 성능과 비용 사이에서 현실적인 절충안이 된다.

| 항목 | [[261_fifo_page_replacement|FIFO]] | [[264_clock_algorithm_nur|클럭 알고리즘]] | [[262_lru_page_replacement|LRU]] |
| :-- | :-- | :-- | :-- |
| 판단 기준 | 적재 순서 | 최근 순회 후 재참조 여부 | 정확한 최근 사용 순서 |
| 구현 복잡도 | 매우 낮음 | 낮음 | 높음 |
| 지역성 반영 | 약함 | 중간 이상 | 매우 강함 |
| 대규모 시스템 적합성 | 단순하지만 비효율 가능 | 매우 높음 | 비용 부담 큼 |

[[264_clock_algorithm_nur|클럭 알고리즘]]은 흔히 [[303_nur|NUR]] 계열의 실용 구현으로 설명된다. NUR이 "최근에 사용되지 않은 [[286_page_frame|페이지]]를 우선 제거한다"는 [[104_classification_analysis|분류]] 철학이라면, [[264_clock_algorithm_nur|클럭 알고리즘]]은 그 철학을 포인터 순회 방식으로 구현한 형태다. 여기에 [[278_dirty_bit|더티 비트]]를 함께 고려하면 Enhanced Clock으로 발전하여, 최근에 안 쓰였더라도 디스크에 다시 써야 하는 [[286_page_frame|페이지]]는 뒤로 미루고, 깨끗한 [[286_page_frame|페이지]]를 먼저 내보내게 된다.

[[001_operating_system_purpose|운영체제]]와 [[002_database_definition|데이터베이스]]도 이 아이디어를 각자 변형해 사용한다. 리눅스는 활성/비활성 리스트를 통해 클럭의 "다시 쓰였으면 [[571_protection_vs_security|보호]]"라는 원리를 확장하고, PostgreSQL 같은 [[002_database_definition|데이터베이스]]는 [[045_clock|Clock]] Sweep으로 버퍼 풀을 관리한다. 즉, [[264_clock_algorithm_nur|클럭 알고리즘]]은 단순한 시험용 [[260_page_replacement|페이지 교체]] 문제가 아니라, 메모리·스토리지·버퍼 캐시가 만나는 지점의 공통 패턴이다.

- **📢 섹션 요약 비유**: FIFO가 줄 선 순서만 보는 입장권 검사라면, LRU는 모든 손님의 마지막 방문 시간을 기록하는 VIP 관리 시스템이고, [[264_clock_algorithm_nur|클럭 알고리즘]]은 "한 바퀴 도는 동안 다시 얼굴을 비춘 손님인가"만 확인하는 실전형 출입 관리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[264_clock_algorithm_nur|클럭 알고리즘]]을 볼 때는 교체 정확도보다도 "[[164_policy|정책]] 유지 비용이 워크로드를 압도하지 않는가"를 먼저 봐야 한다. 메모리 프레임이 매우 많고 접근이 빈번한 시스템에서는 LRU에 가까운 효과보다 관리 오버헤드 절감이 더 큰 이익이 될 수 있다. 이런 환경에서 클럭 계열은 짧은 메타데이터와 단순 순회만으로 안정적인 교체 판단을 제공한다.

예를 들어 대규모 [[015_virtualization|가상화]] 호스트나 [[002_database_definition|데이터베이스]] 서버에서는 [[286_page_frame|페이지]] 수가 방대해 매 접근마다 복잡한 재정렬을 수행하는 [[164_policy|정책]]이 불리하다. 이때 클럭 계열은 메모리 압박이 올라갈수록 스캔 속도가 증가하고, 자주 쓰이는 [[286_page_frame|페이지]]는 [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] 덕분에 자연스럽게 [[571_protection_vs_security|보호]]된다. 다만 모든 [[286_page_frame|페이지]]가 지속적으로 [[316_reference_pattern_nosql|참조]]되는 워크로드에서는 포인터가 긴 순회를 반복할 수 있으므로, 실제 구현은 비활성 큐 분리, 스캔 한도, dirty [[286_page_frame|페이지]] 분리 같은 보완 장치를 함께 둔다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. [[286_page_frame|페이지]] 수가 많아도 [[164_policy|정책]] 메타데이터가 작게 유지되는가?
2. [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]와 [[278_dirty_bit|더티 비트]] 같은 하드웨어 [[167_sql_hint_optimizer_override|힌트]]를 활용할 수 있는가?
3. 메모리 압박이 심할 때 순회 길이가 과도해지지 않도록 보조 [[164_policy|정책]]이 있는가?
4. 스왑 I/O 비용이 큰 환경이라면 Clean 우선 교체가 가능한 확장형인지 확인했는가?

### 피해야 할 오해

- [[264_clock_algorithm_nur|클럭 알고리즘]]은 LRU를 완전히 대체하는 "정확한" [[001_algorithm_definition|알고리즘]]이 아니라, LRU의 핵심 효과를 낮은 비용으로 흉내 내는 근사 전략이다.
- [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]만 있다고 자동으로 성능이 좋아지는 것은 아니며, 스캔 빈도와 메모리 압박 수준이 맞지 않으면 헛도는 스캔이 늘 수 있다.
- 더티 [[286_page_frame|페이지]] 비중이 높을 때는 교체 판단 자체보다 [[289_cqrs_db|쓰기]] 지연이 병목이 될 수 있으므로 스토리지 특성과 함께 봐야 한다.

- **📢 섹션 요약 비유**: [[264_clock_algorithm_nur|클럭 알고리즘]]은 모든 직원의 초 단위 업무 로그를 수집하는 대신, 최근 순찰 때 실제로 일하던 사람인지 확인해 배치하는 현장 관리자와 같다. 기록은 덜 정교하지만 조직이 커질수록 훨씬 운영 가능하다.

---

## Ⅴ. 기대효과 및 결론

[[264_clock_algorithm_nur|클럭 알고리즘]]의 가장 큰 효과는 [[260_page_replacement|페이지 교체]]를 "잘하는 것"과 "가볍게 하는 것"을 함께 잡는 데 있다. [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] 하나와 포인터 순회만으로 [[247_temporal_locality|시간적 지역성]]을 상당 부분 반영하므로, 시스템은 과도한 [[164_policy|정책]] 관리 비용 없이도 의미 있는 [[286_page_frame|페이지]] [[571_protection_vs_security|보호]] 효과를 얻는다. 이는 [[001_operating_system_purpose|운영체제]]가 메모리 관리 때문에 CPU를 소모하는 역설을 줄여 준다.

또한 이 [[001_algorithm_definition|알고리즘]]은 확장성이 좋다. [[278_dirty_bit|더티 비트]]를 추가하면 교체 비용까지 고려하는 Enhanced Clock으로 발전하고, 리스트 분리 전략과 결합하면 현대 [[022_kernel_role|커널]]의 [[286_page_frame|페이지]] 회수 [[164_policy|정책]]으로 이어진다. 즉, [[264_clock_algorithm_nur|클럭 알고리즘]]은 단순한 교체 규칙이라기보다 "최근성 [[167_sql_hint_optimizer_override|힌트]]를 최소 비용으로 쓰는 법"이라는 설계 철학에 가깝다.

다만 기억해야 할 한계도 있다. [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]는 최근 사용의 대략적 흔적일 뿐 정확한 순위가 아니므로, 특정 워크로드에서는 LRU보다 덜 정교할 수 있다. 그럼에도 대규모 운영 환경에서 이 [[001_algorithm_definition|알고리즘]]이 꾸준히 선택되는 이유는, 이론적 최적성보다 지속 가능한 운영 비용이 더 중요하기 때문이다. 따라서 [[264_clock_algorithm_nur|클럭 알고리즘]]은 "완벽한 교체"가 아니라 "현실적으로 가장 오래 살아남은 교체 방식"으로 기억하는 것이 적절하다.

- **📢 섹션 요약 비유**: [[264_clock_algorithm_nur|클럭 알고리즘]]은 모든 길을 실시간으로 계산하는 내비게이션이 아니라, 막힌 길만 빠르게 피해 가도록 설계된 도로 안내판과 같다. 조금 덜 정밀해도 전체 교통을 오래 안정적으로 굴린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[401_page_replacement_algorithms|페이지 교체 알고리즘]] ([[260_page_replacement|Page Replacement]]) | [[387_page_fault|페이지 부재]] 시 어떤 프레임을 비울지 결정하는 상위 문제 |
| [[262_lru_page_replacement|LRU]] ([[262_lru_page_replacement|Least Recently Used]]) | [[264_clock_algorithm_nur|클럭 알고리즘]]이 근사하려는 기준 모델 |
| [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] ([[316_reference_pattern_nosql|Reference]] [[086_fenwick_tree|Bit]]) | 최근 접근 흔적을 남기는 최소 하드웨어 [[167_sql_hint_optimizer_override|힌트]] |
| [[278_dirty_bit|더티 비트]] ([[396_dirty_bit|Dirty Bit]]) | 교체 시 디스크 [[289_cqrs_db|쓰기]] 비용까지 고려하게 만드는 확장 요소 |
| [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) | [[264_clock_algorithm_nur|클럭 알고리즘]]이 실제로 호출되는 [[001_operating_system_purpose|운영체제]] 이벤트 |
| [[265_working_set|Working Set]] | 최근 [[286_usability_tactics|사용성]] 판단을 더 넓은 시간 창으로 해석하는 메모리 관리 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
FIFO (First-In First-Out)
    │
    ▼
LRU (Least Recently Used)
    │
    ├── 정확하지만 구현 비용 큼
    ▼
클럭 알고리즘 (Clock Algorithm)
    │
    ├── 참조 비트 (Reference Bit) 기반 2차 기회
    ▼
Enhanced Clock
    │
    ├── 더티 비트 (Dirty Bit) 반영
    ▼
Active / Inactive List · Clock Sweep · 현대 페이지 회수 정책
```

이 흐름은 "순서 기반 단순 교체 → 최근성 중시 → 최근성의 저비용 근사 → 교체 비용까지 반영 → [[022_kernel_role|커널]] 실전 [[164_policy|정책]]"으로 발전하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 선생님이 원형으로 앉은 친구들을 한 명씩 보면서, 방금 손들었던 친구는 한 번 더 기회를 주고 지나가요.
2. 다음에 다시 왔을 때도 손을 안 들고 있던 친구가 있으면, 그 자리에 새 친구를 앉혀요.
3. 그래서 누가 제일 오래 조용했는지 전부 적지 않아도, 지금 덜 중요한 친구를 빠르게 찾을 수 있어요.
