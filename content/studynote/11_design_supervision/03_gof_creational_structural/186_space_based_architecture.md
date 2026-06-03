---
title: 186. 스페이스 기반 아키텍처 (Space-Based Architecture)
date: '2026-04-21'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스페이스 기반 아키텍처([[151_sba_service_based_architecture_5g|SBA]], Space-Based [[319_architecture|Architecture]])는 요청 처리 경로에서 중앙 DB ([[501_database|Database]]) 병목을 제거하기 위해 처리 로직과 [[001_dikw_pyramid|데이터]]를 인메모리 공간으로 끌어올린 고확장성 패턴이다.
> 2. **가치**: 트래픽이 순간적으로 폭증하는 업무에서 처리 유닛(Processing Unit)을 수평 확장해 [[015_지연_데이터_관점|지연]]시간과 처리량을 동시에 개선할 수 있다.
> 3. **판단 포인트**: [[282_performance_tactics|성능]] 이득의 대가로 최종 [[194_consistency_database_integrity|일관성]]([[650_eventual_consistency|Eventual Consistency]]), 비동기 영속화, 장애 [[658_ir_recovery|복구]] 설계를 함께 감당할 수 있을 때만 SBA의 장점이 현실화된다.

---

## Ⅰ. 개요 및 필요성

스페이스 기반 아키텍처는 애플리케이션 서버와 [[136_variance|분산]] [[001_dikw_pyramid|데이터]] 공간을 결합해 [[001_dikw_pyramid|데이터]]베이스를 실시간 [[191_transaction_concept_states|트랜잭션]] 경로의 중심에서 밀어내는 아키텍처다. 전통적인 3계층 구조는 웹 서버와 애플리케이션 서버는 손쉽게 늘릴 수 있지만, 상태와 [[001_dikw_pyramid|데이터]]가 중앙 DB에 집중되면서 결국 확장의 천장이 DB에서 생긴다. 읽기 캐시를 붙여도 [[289_cqrs_db|쓰기]] 집중 구간에서는 병목이 남고, [[160_session_controlling_terminal|세션]]과 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 관리가 더 복잡해진다.

SBA는 이 문제를 “요청을 [[001_dikw_pyramid|데이터]]가 있는 곳으로 보내는 것”으로 풀지 않고, “[[001_dikw_pyramid|데이터]]와 처리를 함께 가진 단위를 여러 개 두는 것”으로 푼다. 즉 처리 유닛이 웹 로직, 비즈니스 로직, 인메모리 [[001_dikw_pyramid|데이터]]까지 함께 보유하고, [[001_dikw_pyramid|데이터]]는 인메모리 [[001_dikw_pyramid|데이터]] 그리드(IMDG, In-Memory [[001_dikw_pyramid|Data]] Grid)에 [[136_variance|분산]] 저장된다. 그 결과 순간 부하가 매우 큰 주문·경매·게임·실시간 이벤트 시스템에서 중앙 저장소 병목을 크게 낮출 수 있다.

중요한 전제는 모든 시스템이 SBA를 필요로 하지는 않는다는 점이다. CRUD 중심 업무나 강한 [[191_transaction_concept_states|트랜잭션]] [[194_consistency_database_integrity|일관성]]이 절대적인 시스템이라면, 전통 구조에 캐시·읽기 [[016_replication_factor|복제]]·[[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation)를 조합하는 편이 더 단순하고 안정적일 수 있다.

- **📢 섹션 요약 비유**: SBA는 손님이 몰릴 때마다 중앙 창고에 뛰어가는 가게를 없애고, 각 매장이 자주 쓰는 물건을 자기 뒤 창고에 바로 쌓아두는 방식과 같다. 빨라지지만, 각 매장 재고를 맞추는 일이 새 숙제가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SBA의 핵심 구성요소는 처리 유닛, [[015_virtualization|가상화]] 미들웨어, [[063_relation_tuple_cardinality|튜플]] 스페이스(Tuple Space) 또는 [[136_variance|분산]] [[001_dikw_pyramid|데이터]] 공간, 그리고 비동기 영속화 계층이다. 처리 유닛은 [[090_service_kubernetes_network_load_balancing|서비스]] 코드와 해당 업무 [[001_dikw_pyramid|데이터]]의 지역 캐시를 함께 갖는다. [[015_virtualization|가상화]] 미들웨어는 요청을 적절한 처리 유닛으로 [[339_routing_overview_best_path_selection|라우팅]]하고, 인메모리 공간은 [[001_dikw_pyramid|데이터]]를 [[514_partition_slice_volume|파티션]]과 [[016_replication_factor|복제]] [[164_policy|정책]]에 따라 배치한다.

아래 그림은 SBA의 [[001_dikw_pyramid|데이터]] 경로를 압축한다. 사용자의 요청은 먼저 처리 유닛에 도달하고, 처리 유닛은 메모리 공간을 우선 조회한다. 영속 저장소는 즉시 동기식으로 두드리는 대상이 아니라, [[658_ir_recovery|복구]]와 [[606_auditing_linux_auditd|감사]] 추적을 위한 후행 저장소로 밀려난다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 스페이스 기반 아키텍처의 요청 처리 흐름                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Client Request                                                             │
│      │                                                                     │
│      ▼                                                                     │
│ [Virtualized Middleware]                                                   │
│      │           라우팅/파티션/장애조치                                    │
│      ├──────────────────┬──────────────────┬──────────────────┐            │
│      ▼                  ▼                  ▼                  ▼            │
│ [PU-A]              [PU-B]              [PU-C]          ... [PU-N]         │
│  │                  │                  │                                   │
│  ├─ Web/API         ├─ Web/API         ├─ Web/API                          │
│  ├─ Business Logic  ├─ Business Logic  ├─ Business Logic                   │
│  └─ Local Cache     └─ Local Cache     └─ Local Cache                      │
│      │                  │                  │                                 │
│      └──────────────┬───┴──────────────┬───┘                                 │
│                     ▼                  ▼                                     │
│              [Tuple Space / IMDG Partitioned Grid]                          │
│                     │                  │                                     │
│                     └─────── Async Write-Behind ───────▶ [Database]         │
└─────────────────────────────────────────────────────────────────────────────┘
```

| 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 처리 유닛 (Processing Unit) | [[090_service_kubernetes_network_load_balancing|서비스]]와 [[001_dikw_pyramid|데이터]] 접근을 한 단위로 묶음 | 무상태가 아니라 “로컬 상태를 가진 확장 단위” |
| [[015_virtualization|가상화]] 미들웨어 | [[339_routing_overview_best_path_selection|라우팅]], [[179_table_partitioning_concept|파티셔닝]], 장애 조정 | Hot key와 [[160_session_controlling_terminal|세션]] [[136_variance|분산]] [[164_policy|정책]] 중요 |
| [[063_relation_tuple_cardinality|튜플]] 스페이스 / IMDG | [[136_variance|분산]] 메모리 저장소 | [[514_partition_slice_volume|파티션]] 키, [[016_replication_factor|복제]] 수, [[555_backup_and_restore_strategy|백업]] 노드 설계 |
| 비동기 영속화 | Write-Behind, [[637_zfs_snapshot_cow_architecture|Snapshot]], Event Log | 유실 허용 범위와 [[658_ir_recovery|복구]] 방식 정의 |
| [[016_replication_factor|복제]] 엔진 | 처리 유닛 간 [[001_dikw_pyramid|데이터]] 복사 | [[194_consistency_database_integrity|일관성]] 수준과 [[015_지연_데이터_관점|지연]]시간의 균형 |

SBA가 빠른 이유는 단순히 메모리가 디스크보다 빨라서만이 아니다. **확장 단위가 “웹 서버 따로, 앱 서버 따로, DB 따로”가 아니라 “처리와 [[001_dikw_pyramid|데이터]]가 묶인 유닛 전체”**이기 때문이다. 따라서 노드를 추가할수록 계산 능력과 [[001_dikw_pyramid|데이터]] 처리 능력이 함께 늘어난다. 반면 [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]], 재시작 시 warm-up, 메모리 장애 [[658_ir_recovery|복구]]는 훨씬 더 신중하게 설계해야 한다.

- **📢 섹션 요약 비유**: 각 점포가 계산대, 재고, 간단한 창고를 한몸처럼 들고 있는 프랜차이즈 매장이라고 생각하면 쉽다. 점포 수를 늘리면 판매대와 재고처리 능력이 동시에 늘어나지만, 재고 복사와 마감 정산 체계가 허술하면 전체 체인이 흔들린다.

---

## Ⅲ. 비교 및 연결

SBA를 이해하려면 전통 3계층 구조, 단순 캐시 확장, 이벤트 기반 구조와의 경계를 함께 봐야 한다. 3계층 구조는 이해와 운영이 쉽고 강한 [[194_consistency_database_integrity|일관성]]을 확보하기 좋지만, 중앙 DB 병목을 피하기 어렵다. 캐시를 붙인 구조는 읽기는 빨라지지만 [[289_cqrs_db|쓰기]] 경합과 캐시 무효화가 계속 문제로 남는다. SBA는 이 두 구조보다 더 과감하게 [[001_dikw_pyramid|데이터]]를 메모리 쪽으로 이동시킨다.

| 비교 축 | 전통 3계층 | 캐시 보강 구조 | [[151_sba_service_based_architecture_5g|SBA]] |
| :--- | :--- | :--- | :--- |
| 병목 위치 | 중앙 DB | DB + 캐시 [[212_synchronization_mechanisms|동기화]] | 메모리 [[016_replication_factor|복제]]·영속화 |
| 확장 단위 | 웹/앱 서버 위주 | 앱 서버 + 캐시 계층 | 처리 유닛 전체 |
| [[194_consistency_database_integrity|일관성]] | 강한 [[194_consistency_database_integrity|일관성]] 유리 | 캐시 불일치 가능 | 최종 [[194_consistency_database_integrity|일관성]] 전제 |
| [[015_지연_데이터_관점|지연]]시간 | DB I/O 의존 | 읽기만 빠른 경우 많음 | 읽기·[[289_cqrs_db|쓰기]]를 모두 메모리 우선 처리 |
| 적합 업무 | 일반 업무 시스템 | 읽기 편중 [[090_service_kubernetes_network_load_balancing|서비스]] | 실시간 고동시성 시스템 |

SBA는 [[306_cqrs|CQRS]], [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]([[307_event_sourcing|Event Sourcing]]), LMAX Disruptor와도 연결된다. 이들은 모두 “중앙 동기식 병목을 줄이고 메모리·이벤트 중심으로 처리한다”는 방향성을 공유한다. 다만 SBA는 시스템의 **배치 단위 자체를 바꾸는 아키텍처 패턴**이고, 다른 개념들은 저장/명령/[[014_concurrency|동시성]] 처리의 세부 기법이라는 점에서 범위가 다르다.

- **📢 섹션 요약 비유**: 3계층 구조가 중앙 창고형 백화점이라면, 캐시 보강 구조는 빠른 임시 창고를 붙인 형태다. SBA는 아예 작은 매장을 여러 개 [[016_replication_factor|복제]]해 손님을 [[136_variance|분산]]시키는 동네형 네트워크에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

SBA는 순간 트래픽 스파이크가 크고, [[001_dikw_pyramid|데이터]] 접근 패턴이 비교적 지역적이며, 일부 최종 [[194_consistency_database_integrity|일관성]]을 수용할 수 있는 환경에서 적합하다. 실시간 경매, 게임 [[160_session_controlling_terminal|세션]] 처리, 광고 입찰, [[148_5g_embb_urllc_mmtc|초고속]] 주문 처리처럼 “DB를 매번 찍는 순간 [[015_지연_데이터_관점|지연]]이 폭증하는” 업무가 대표적이다. 반대로 정산, 회계, 핵심 원장처럼 강한 정합성이 절대적인 업무는 SBA만으로 처리하기 어렵다.

### 채택 [[435_checklist_based_testing|체크리스트]]

1. [[001_dikw_pyramid|데이터]]의 일부 [[015_지연_데이터_관점|지연]] [[016_replication_factor|복제]]와 비동기 저장을 수용할 수 있는가?
2. 업무 키를 기준으로 [[514_partition_slice_volume|파티션]]을 안정적으로 나눌 수 있는가?
3. 노드 장애 시 재복구 시간과 [[001_dikw_pyramid|데이터]] warm-up 비용을 감당할 수 있는가?
4. 메모리 사용량이 경제적으로 유지되는가?
5. 운영팀이 장애 조치, 재분배, [[555_backup_and_restore_strategy|백업]]·[[016_replication_factor|복제]] [[164_policy|정책]]을 이해하고 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 단순 CRUD [[090_service_kubernetes_network_load_balancing|서비스]]에 과도하게 도입해 운영 복잡도만 키우는 경우
- [[514_partition_slice_volume|파티션]] 키가 잘못돼 일부 노드만 과부하되는 Hot Spot 구조
- 비동기 영속화 실패를 가볍게 보고 재처리·재동기화 [[268_strategy_pattern|전략]]을 준비하지 않는 경우

기술사 답안에서는 “DB 병목 제거”만 강조하면 절반짜리다. 반드시 **[[196_durability_permanent_storage|영속성]], [[016_replication_factor|복제]], 장애 [[658_ir_recovery|복구]], 정합성 수준**을 함께 적어야 SBA를 입체적으로 설명한 답안이 된다. 고성능은 장점이지만, 그 장점을 유지하는 운영 체계까지 포함해야 패턴의 완성도가 나온다.

- **📢 섹션 요약 비유**: SBA는 손님이 몰리는 놀이공원에 입구를 많이 만드는 [[268_strategy_pattern|전략]]과 같다. 입장은 빨라지지만, 분실물 보관과 마감 정산까지 같이 설계하지 않으면 운영이 더 혼란스러워질 수 있다.

---

## Ⅴ. 기대효과 및 결론

SBA의 기대효과는 [[148_5g_embb_urllc_mmtc|초고속]] 응답, 선형에 가까운 수평 확장, 그리고 DB 의존도 감소다. 특히 피크 트래픽이 매우 불규칙한 환경에서 큰 효과를 낸다. 처리 유닛을 늘리면 웹 계층만이 아니라 실질 처리 용량도 함께 늘어나므로, [[282_performance_tactics|성능]] 예측과 확장 계획이 단순해진다.

그러나 이 효과는 메모리 공간을 잘게 나누고 안전하게 [[016_replication_factor|복제]]할 수 있을 때만 유지된다. 메모리 기반 구조는 매우 빠르지만, 장애와 정합성 문제에 더 민감하다. 따라서 SBA는 “DB를 없애는 패턴”이 아니라, **DB를 실시간 경로에서 뒤로 물리고 메모리-[[016_replication_factor|복제]]-영속화 설계를 전면에 세우는 패턴**으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: SBA는 고속도로 차선을 늘리는 공사와 비슷하다. 잘 설계하면 정체가 크게 줄지만, 합류 구간과 사고 처리 체계까지 준비해야 진짜로 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| IMDG (In-Memory [[001_dikw_pyramid|Data]] Grid) | SBA의 핵심 저장·[[016_replication_factor|복제]] 기반 |
| [[063_relation_tuple_cardinality|튜플]] 스페이스 (Tuple Space) | 공유 메모리형 [[001_dikw_pyramid|데이터]] 상호작용 모델 |
| Write-Behind | 비동기 영속화의 대표 [[268_strategy_pattern|전략]] |
| [[650_eventual_consistency|Eventual Consistency]] | SBA가 흔히 수용하는 [[194_consistency_database_integrity|일관성]] 모델 |
| [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation) | 읽기/[[289_cqrs_db|쓰기]] 부담 분리와 연결 |
| LMAX Disruptor | 인메모리 초저지연 패턴의 연관 개념 |
| Hot Spot [[514_partition_slice_volume|Partition]] | [[514_partition_slice_volume|파티션]] 설계 실패 시 대표 장애 원인 |

### 📈 관련 키워드 및 발전 흐름도

```text
3계층 구조의 DB 병목
    │
    ▼
분산 캐시 · IMDG
    │
    ▼
스페이스 기반 아키텍처
    │
    ├──────────────▶ Tuple Space 파티셔닝 · 복제
    │
    └──────────────▶ Eventual Consistency · Write-Behind
                           │
                           ▼
                 초저지연 이벤트 처리 · 실시간 확장 패턴
```

이 흐름은 “DB 최적화 → 메모리 전진 배치 → 아키텍처 수준의 재구성”으로 진화하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 손님이 많을 때마다 중앙 창고에 뛰어가면 너무 느려져요.
2. 그래서 각 가게가 자주 쓰는 물건을 자기 옆 창고에 두고 바로 꺼내 쓰는 게 스페이스 기반 아키텍처예요.
3. 대신 여러 가게의 물건 수를 맞추고 마지막에 큰 창고에 기록하는 규칙을 잘 정해야 해요.
