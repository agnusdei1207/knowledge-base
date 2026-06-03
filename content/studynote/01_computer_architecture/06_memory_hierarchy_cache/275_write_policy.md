---
title: 275. 캐시 쓰기 정책 (Write Policy)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

# 275. 캐시 [[289_cqrs_db|쓰기]] [[164_policy|정책]] (Write [[164_policy|Policy]])

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 캐시 [[289_cqrs_db|쓰기]] [[164_policy|정책]] (Write [[164_policy|Policy]])은 CPU (Central Processing Unit)가 값을 바꿨을 때 그 변경을 캐시에만 잠시 둘지, 하위 메모리까지 즉시 보낼지를 정하는 규칙이다.
> 2. **가치**: 이 선택은 읽기 경로보다 더 직접적으로 메모리 [[344_bus|버스]] 트래픽, [[015_지연_데이터_관점|지연]]시간, [[466_power_consumption|전력 소모]], [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 비용을 바꾼다.
> 3. **판단 포인트**: 현대 시스템은 보통 [[277_write_back|Write-Back]] + Write-Allocate를 택하지만, 장치 제어·[[568_logs_distributed_logging_elk_fluentd|로그]] 기록·[[746_io_direct_memory_access_dma|DMA]] ([[318_dma|Direct Memory Access]]) 연동처럼 즉시 반영이 중요한 구간은 다른 선택이 더 안전하다.

---

## Ⅰ. 개요 및 필요성

캐시 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 프로세서가 [[001_dikw_pyramid|데이터]]를 수정할 때 **"언제 하위 계층에 책임 있게 반영할 것인가"**를 정하는 메모리 계층의 운영 규칙이다. 캐시는 본질적으로 메인 메모리의 빠른 사본이므로, [[289_cqrs_db|쓰기]]가 발생하는 순간부터 캐시와 하위 메모리 사이에는 최신본과 원본의 차이가 생길 수 있다. 읽기 [[164_policy|정책]]이 "어디서 가져올까"를 다룬다면, [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 "어디까지 즉시 맞출까"를 다룬다.

이 [[164_policy|정책]]이 중요한 이유는 [[289_cqrs_db|쓰기]] 연산이 단순히 값 1개를 바꾸는 행위가 아니기 때문이다. CPU는 1ns 안팎의 속도로 캐시에 접근하지만, [[251_dram|DRAM]] (Dynamic Random Access Memory)은 수십~수백 ns 수준으로 느리다. 만약 모든 STORE 명령이 메모리까지 즉시 완료되어야 한다면 파이프라인은 자주 멈추고, 반대로 캐시에만 오래 머물게 하면 다른 코어나 입출력 장치는 오래된 값을 볼 위험이 커진다.

즉 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 [[282_performance_tactics|성능]] 최적화 기법이면서 동시에 [[194_consistency_database_integrity|일관성]] 관리 전략이다. 캐시 히트율이 높아도 [[289_cqrs_db|쓰기]] [[164_policy|정책]]이 나쁘면 [[344_bus|버스]]가 포화되고, [[164_policy|정책]]이 지나치게 공격적이면 장애 시 [[658_ir_recovery|복구]] 비용과 [[212_synchronization_mechanisms|동기화]] 복잡도가 폭증한다. 그래서 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 단독 개념이 아니라 교체 [[164_policy|정책]], [[278_dirty_bit|더티 비트]], [[402_cache_coherence|캐시 일관성]], 장치 메모리 속성과 함께 이해해야 한다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│              쓰기 정책이 필요한 이유: 빠른 사본과 느린 원본의 충돌  │
├──────────────────────────────────────────────────────────────────────┤
│ CPU가 값 수정                                                        │
│    │                                                                 │
│    ▼                                                                 │
│ Cache Line 최신화 ───────────────┐                                   │
│    │                             │                                   │
│    │ 즉시 동기화                 │ 나중 동기화                      │
│    ▼                             ▼                                   │
│ Main Memory도 바로 갱신         캐시에 최신값 유지                  │
│    │                             │                                   │
│ 일관성 단순                      버스 절감                           │
│ 성능 손해                        관리 복잡                           │
└──────────────────────────────────────────────────────────────────────┘
```

이 그림은 [[289_cqrs_db|쓰기]] [[164_policy|정책]]이 단순한 구현 취향이 아니라, **즉시 일치**와 **[[015_지연_데이터_관점|지연]] 반영** 사이의 구조적 선택임을 보여준다. 결국 메모리 계층은 "무조건 빠르게"가 아니라 "어느 계층에서 병목을 감당할지"를 정해야 한다.

- **📢 섹션 요약 비유**: [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 메모장에 고친 내용을 본사 서버에 바로 저장할지, 로컬에서 다듬다가 나중에 한 번에 올릴지 정하는 업무 규칙과 같다. 바로 올리면 안심되지만 느리고, 나중에 몰아 올리면 빠르지만 관리가 더 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[289_cqrs_db|쓰기]] [[164_policy|정책]]은 보통 두 갈래 질문으로 구성된다. 첫째, **Write [[263_cache_hit_miss|Hit]]**가 났을 때 메모리까지 즉시 쓸 것인가([[276_write_through|Write-Through]]) 아니면 캐시에만 반영하고 나중에 쓸 것인가([[277_write_back|Write-Back]])이다. 둘째, **Write Miss**가 났을 때 해당 블록을 캐시로 가져와서 쓸 것인가(Write-Allocate) 아니면 캐시를 우회하고 하위 메모리에만 쓸 것인가(No-Write-Allocate)이다. 이 두 질문이 합쳐져 실제 시스템의 [[289_cqrs_db|쓰기]] 경로가 결정된다.

| 판단 축 | 선택지 | 핵심 동작 | 보통의 결합 |
| :--- | :--- | :--- | :--- |
| Write [[263_cache_hit_miss|Hit]] 처리 | [[276_write_through|Write-Through]] | 캐시와 하위 메모리를 함께 갱신 | No-Write-Allocate와 자주 결합 |
| Write [[263_cache_hit_miss|Hit]] 처리 | [[277_write_back|Write-Back]] | 캐시만 갱신하고 [[278_dirty_bit|더티 비트]] 표시 | Write-Allocate와 자주 결합 |
| Write Miss 처리 | Write-Allocate | 블록을 캐시로 가져온 뒤 수정 | 지역성이 큰 [[001_dikw_pyramid|데이터]]에 유리 |
| Write Miss 처리 | No-Write-Allocate | 캐시 적재 없이 하위 메모리에 직접 기록 | 일회성 스트리밍 [[289_cqrs_db|쓰기]]에 유리 |

현대 CPU의 주류 조합은 **[[277_write_back|Write-Back]] + Write-Allocate**다. 이유는 시간이 지나도 같은 [[001_dikw_pyramid|데이터]]에 다시 접근할 가능성, 즉 [[247_temporal_locality|시간적 지역성]] ([[247_temporal_locality|Temporal Locality]])이 [[289_cqrs_db|쓰기]]에도 강하게 작동하기 때문이다. 예를 들어 반복문 안의 카운터나 [[055_array|배열]] 누적값은 한 번 쓰고 끝나는 값이 아니라, 짧은 시간에 여러 번 다시 수정된다. 이 경우 메모리로 매번 내보내는 것보다 캐시에 블록을 들여와 여러 번 수정한 뒤 교체 시점에 한 번만 반영하는 편이 훨씬 효율적이다.

다만 Write-Back은 추가 장치를 요구한다. 캐시 라인이 수정되었는지 표시하는 [[278_dirty_bit|더티 비트]] ([[396_dirty_bit|Dirty Bit]]), 교체 순간 [[015_지연_데이터_관점|지연]]을 숨기는 [[289_cqrs_db|쓰기]] 버퍼 (Write Buffer), 멀티코어 환경에서 최신 소유자를 추적하는 MESI (Modified, Exclusive, Shared, Invalid) 같은 [[194_consistency_database_integrity|일관성]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 함께 필요하다. 반대로 Write-Through는 구조가 단순하지만 메모리 대역폭을 계속 소비하므로, 실제 구현에서는 [[289_cqrs_db|쓰기]] 버퍼 없이는 [[282_performance_tactics|성능]] 손해가 매우 크다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  Write Hit / Write Miss 결정 흐름                    │
├──────────────────────────────────────────────────────────────────────┤
│ CPU Write Request                                                    │
│        │                                                             │
│        ▼                                                             │
│   Cache Tag Check                                                    │
│        │                                                             │
│   ┌────┴────┐                                                        │
│   │         │                                                        │
│ Hit       Miss                                                       │
│   │         │                                                        │
│   │         ├──────────────┐                                         │
│   │         │              │                                         │
│   ▼         ▼              ▼                                         │
│ Through/Back Allocate    No-Allocate                                 │
│   │         │              │                                         │
│   │         ▼              ▼                                         │
│   │      Bring Line      Write Lower Level                           │
│   │      Then Update     Without Cache Fill                          │
│   │                                                                  │
│   ├─ WT: Cache + Memory now                                          │
│   └─ WB: Cache only, Dirty=1                                         │
└──────────────────────────────────────────────────────────────────────┘
```

이 흐름에서 핵심은 [[289_cqrs_db|쓰기]] [[164_policy|정책]]이 단일 스위치가 아니라 **히트 처리 + 미스 처리**의 조합이라는 점이다. 시험 답안에서도 Write-Through와 Write-Back만 쓰고 끝내면 절반 설명에 머무르고, Allocate 여부까지 연결해야 실제 아키텍처를 설명한 것이 된다.

- **📢 섹션 요약 비유**: 손님이 온다고 해서 바로 본사 창고까지 주문을 넣을지, 일단 매장 재고 선반에 가져다 놓고 그 자리에서 계속 팔지 정하는 방식과 같다. 자주 팔릴 물건이면 선반에 올려두는 편이 훨씬 효율적이다.

---

## Ⅲ. 비교 및 연결

[[289_cqrs_db|쓰기]] [[164_policy|정책]]의 경계는 단순히 "빠름 vs 안전함"으로 끝나지 않는다. **어떤 트래픽을 줄이고, 어떤 복잡도를 늘리는가**로 비교해야 한다. Write-Through는 메모리가 항상 최신에 가깝기 때문에 장애 [[658_ir_recovery|복구]]와 외부 관찰이 단순하지만, [[289_cqrs_db|쓰기]] 횟수만큼 하위 계층이 바빠진다. Write-Back은 [[344_bus|버스]] 사용량을 줄이는 대신, 최신본이 캐시 안에만 존재하는 시간을 허용한다.

| 비교 항목 | [[276_write_through|Write-Through]] | [[277_write_back|Write-Back]] |
| :--- | :--- | :--- |
| 하위 메모리 갱신 시점 | 매 [[289_cqrs_db|쓰기]]마다 즉시 | 교체·플러시 시점 |
| 메모리 [[344_bus|버스]] 트래픽 | 큼 | 작음 |
| 하드웨어 복잡도 | 비교적 단순 | [[278_dirty_bit|더티 비트]]·상태 관리 필요 |
| 장애/관찰 관점 | 최신값 [[396_validation|확인]]이 쉬움 | 캐시 플러시 여부 [[396_validation|확인]] 필요 |
| 잘 맞는 워크로드 | [[568_logs_distributed_logging_elk_fluentd|로그]], MMIO (Memory-Mapped I/O), 일회성 [[289_cqrs_db|쓰기]] | 루프 변수, 누적값, 일반 [[001_dikw_pyramid|데이터]] |

여기에 Allocate [[164_policy|정책]]을 붙이면 특성이 더 선명해진다. [[276_write_through|Write-Through]] + No-Write-Allocate는 "어차피 다시 안 쓸 가능성이 큰 [[001_dikw_pyramid|데이터]]는 캐시를 더럽히지 말자"는 철학이고, [[277_write_back|Write-Back]] + Write-Allocate는 "한 번 [[289_cqrs_db|쓰기]] 시작한 블록은 곧 다시 쓸 가능성이 크다"는 철학이다. 결국 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 지역성 가정에 대한 아키텍처의 답변이다.

또한 이 개념은 멀티코어와 입출력으로 자연스럽게 확장된다. 한 코어가 Write-Back으로 수정한 값을 다른 코어가 읽으려면 [[402_cache_coherence|캐시 일관성]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 최신 소유자를 찾아줘야 한다. 장치가 DMA로 메모리를 직접 읽고 쓰는 경우에는 CPU 캐시의 최신본과 장치가 보는 메모리 값이 어긋날 수 있으므로, 캐시 무효화나 플러시가 반드시 따라붙는다.

- **📢 섹션 요약 비유**: Write-Through는 수정할 때마다 단체 채팅방 공지를 올리는 방식이고, Write-Back은 각자 개인 초안에서 작업하다 필요할 때 최종본을 공유하는 방식이다. 전자는 혼선이 적고, 후자는 일은 빠르지만 공유 규칙이 없으면 금방 충돌이 난다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "어떤 [[164_policy|정책]]이 더 우수한가"보다 **어느 주소 공간과 워크로드에 어떤 [[164_policy|정책]]을 적용해야 하는가**가 중요하다. 일반적인 [[001_dikw_pyramid|데이터]] 캐시는 Write-Back이 유리하지만, MMIO (Memory-Mapped I/O) 레지스터처럼 장치가 즉시 반응해야 하는 공간은 Write-Back을 쓰면 안 된다. CPU가 장치 시작 [[073_bit|비트]]를 캐시에만 써놓고 실제 [[344_bus|버스]] 전송을 미루면, 장치는 명령을 받지 못한 채 멈춰 있기 때문이다.

[[746_io_direct_memory_access_dma|DMA]] 연동도 대표적 판단 지점이다. 네트워크 카드나 스토리지 컨트롤러가 메모리를 직접 갱신할 때, CPU 캐시에 이전 값이 남아 있으면 소프트웨어는 오래된 [[001_dikw_pyramid|데이터]]를 읽게 된다. 그래서 운영체제와 드라이버는 [[746_io_direct_memory_access_dma|DMA]] 시작 전후로 캐시 플러시, 무효화, 비캐시 영역 매핑을 사용해 CPU 관점과 장치 관점을 맞춘다. 이 지점에서 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 단순 CPU [[282_performance_tactics|성능]] 문제가 아니라 시스템 [[194_consistency_database_integrity|일관성]] 문제로 확장된다.

기술사 답안에서는 다음처럼 정리하면 좋다. **반복 수정이 많은 일반 [[001_dikw_pyramid|데이터]]**에는 [[277_write_back|Write-Back]] + Write-Allocate를 채택하고, **즉시 가시성이 필요한 장치 제어 공간**에는 [[276_write_through|Write-Through]] 또는 Uncacheable [[164_policy|정책]]을 둔다. **대용량 스트리밍 출력**처럼 재사용이 거의 없는 [[001_dikw_pyramid|데이터]]에는 Non-Temporal Store 같은 캐시 우회 기법을 함께 고려해야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. 같은 블록에 대한 반복 [[289_cqrs_db|쓰기]]가 많은가, 아니면 한 번 쓰고 끝나는가?
2. 다른 코어·장치가 즉시 최신값을 봐야 하는가?
3. 정전·장애 시 최신본 유실을 소프트웨어 계층에서 [[658_ir_recovery|복구]]할 수 있는가?
4. [[289_cqrs_db|쓰기]] 버퍼 포화, 플러시 비용, [[194_consistency_database_integrity|일관성]] 트래픽을 감당할 수 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- MMIO 영역을 일반 DRAM처럼 생각하고 Write-Back으로 다루는 설계
- [[746_io_direct_memory_access_dma|DMA]] 버퍼를 [[402_cache_coherence|캐시 일관성]] 처리 없이 재사용하는 드라이버 코드
- 스트리밍 대량 [[289_cqrs_db|쓰기]] [[001_dikw_pyramid|데이터]]를 일반 캐시에 채워 넣어 캐시 오염을 유발하는 구현

- **📢 섹션 요약 비유**: 장치 제어 주소는 결재 버튼과 같아서 누르는 즉시 서버에 반영돼야 한다. 반면 일반 작업 문서는 로컬 초안에서 여러 번 다듬어도 되므로, 같은 "[[289_cqrs_db|쓰기]]"라도 문맥에 따라 규칙을 달리 써야 한다.

---

## Ⅴ. 기대효과 및 결론

적절한 [[289_cqrs_db|쓰기]] [[164_policy|정책]]을 선택하면 메모리 계층은 단순 저장소가 아니라 트래픽 조절기가 된다. Write-Back은 동일 블록에 대한 반복 [[289_cqrs_db|쓰기]]를 캐시 내부에 흡수하여 [[344_bus|버스]] 사용량과 평균 [[015_지연_데이터_관점|지연]]시간을 크게 줄인다. Write-Through는 [[282_performance_tactics|성능]]에서는 불리하지만, 관찰 가능성과 단순성 덕분에 장치 제어·특수 메모리 영역에서 여전히 중요한 역할을 맡는다.

다만 어떤 [[164_policy|정책]]도 만능은 아니다. Write-Back은 더티 [[001_dikw_pyramid|데이터]] 손실 가능성, 교체 시 [[015_지연_데이터_관점|지연]] 집중, [[194_consistency_database_integrity|일관성]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 복잡도를 동반하고, Write-Through는 하위 메모리 대역폭과 [[466_power_consumption|전력 소모]] 부담을 키운다. 결국 좋은 설계는 하나의 [[164_policy|정책]]을 절대화하는 것이 아니라, [[001_dikw_pyramid|데이터]] 성격과 시스템 경계에 따라 [[164_policy|정책]]을 구획하는 데서 나온다.

앞으로는 비휘발성 메모리, [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) 기반 메모리 확장, 가속기 중심 이기종 시스템이 늘수록 "누가 최신본을 갖는가"가 더 복잡해진다. 그래서 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 오래된 캐시 이론이 아니라, 앞으로도 [[282_performance_tactics|성능]]·[[194_consistency_database_integrity|일관성]]·[[658_ir_recovery|복구]] 가능성 사이의 균형점을 묻는 핵심 주제로 남는다. 기억해야 할 한 문장은 이것이다. **[[289_cqrs_db|쓰기]] [[164_policy|정책]]은 값을 어디에 쓰느냐가 아니라, 책임을 언제 어디까지 전파하느냐를 정하는 규칙**이다.

- **📢 섹션 요약 비유**: 좋은 [[289_cqrs_db|쓰기]] [[164_policy|정책]]은 회사의 보고 체계와 같다. 모든 일을 즉시 보고하면 느려지고, 너무 늦게 보고하면 사고가 난다. 결국 조직이 잘 굴러가려면 업무 성격에 맞는 보고 타이밍이 필요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[276_write_through|Write-Through]] | 캐시와 하위 메모리를 즉시 [[212_synchronization_mechanisms|동기화]]하는 대표 [[289_cqrs_db|쓰기]] [[164_policy|정책]] |
| [[277_write_back|Write-Back]] | [[278_dirty_bit|더티 비트]]를 기반으로 교체 시점에 반영하는 [[282_performance_tactics|성능]] 중심 [[164_policy|정책]] |
| Write-Allocate | [[289_cqrs_db|쓰기]] 미스 시 블록을 캐시에 적재해 이후 지역성을 활용하는 [[164_policy|정책]] |
| [[396_dirty_bit|Dirty Bit]] | 캐시 라인이 하위 메모리와 달라졌는지 추적하는 상태 [[073_bit|비트]] |
| [[402_cache_coherence|Cache Coherence]] | 멀티코어에서 각 캐시의 최신본을 일치시키는 메커니즘 |
| [[746_io_direct_memory_access_dma|DMA]] ([[318_dma|Direct Memory Access]]) | CPU 캐시 밖에서 메모리를 직접 갱신해 [[289_cqrs_db|쓰기]] [[164_policy|정책]]과 충돌할 수 있는 장치 접근 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
주기억장치 병목 인식
    │
    ▼
캐시 도입
    │
    ▼
Write-Through / Write-Back 분화
    │
    ├── Write Buffer · Dirty Bit
    │
    ▼
Write-Allocate · No-Write-Allocate 최적화
    │
    ▼
MESI 기반 캐시 일관성 · DMA 동기화
    │
    ▼
비휘발성 메모리 · CXL 기반 이기종 메모리 정책 확장
```

이 흐름은 [[289_cqrs_db|쓰기]] [[164_policy|정책]]이 단순한 캐시 내부 옵션에서 출발해, 멀티코어·장치 연동·차세대 메모리 구조까지 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 공책에 글자를 고쳤을 때 바로 선생님 노트에도 똑같이 적는 방법이 있고, 내 공책에서 다 고친 뒤 나중에 한 번만 옮겨 적는 방법도 있어요.
2. 바로바로 옮기면 틀릴 걱정은 적지만 왔다 갔다 하느라 느리고, 나중에 옮기면 빠르지만 마지막에 꼭 정리해야 해요.
3. 컴퓨터는 어떤 일이냐에 따라 두 방법을 골라 쓰면서 빠르기와 정확함을 같이 지키려 한답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 275 / 803

← **이전**: [[274_fifo|274. FIFO (First-In, First-Out)]]
**다음**: [[276_write_through|276. Write-Through (동시 쓰기)]] →

---
