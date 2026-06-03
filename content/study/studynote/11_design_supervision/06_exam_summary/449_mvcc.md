+++
weight = 449
title = "449. 동시성 제어 MVCC 낙관 비관 락킹 패턴 (MVCC Concurrency Control with Optimistic and Pessimistic Locking)"
date = "2026-05-10"
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

1. MVCC는 데이터의 여러 [[288_version_ihl_tos_total_length|버전]]을 유지해 읽기와 [[289_cqrs_db|쓰기]]가 동시에 진행되도록 하면서 일관성을 지키는 대표 [[014_concurrency|동시성]] 제어 방식이다.
2. 핵심 가치는 읽기 블로킹을 줄이고 [[022_snapshot_backup_architecture|스냅샷]] 일관성을 확보하되, 충돌 지점에서는 낙관·비관 락킹을 적절히 섞어 처리량과 안정성을 균형 있게 맞추는 데 있다.
3. 기술사 판단에서는 격리 수준, 충돌 빈도, [[288_version_ihl_tos_total_length|버전]] 정리 비용, 잠금 정책이 워크로드 특성과 맞는지를 함께 설명해야 한다.

## Ⅰ. 개요 및 필요성

[[002_database_definition|데이터베이스]]는 동시에 많은 사용자가 읽고 쓰더라도 결과가 틀리지 않아야 한다. 단순 잠금만으로 이를 해결하면 읽기까지 막혀 응답 지연이 커지고, 반대로 통제를 약하게 하면 갱신 손실이나 비일관 읽기가 발생한다. MVCC는 한 행의 과거 [[288_version_ihl_tos_total_length|버전]]을 함께 보관해 읽는 [[191_transaction_concept_states|트랜잭션]]은 자신이 시작한 시점의 [[022_snapshot_backup_architecture|스냅샷]]을 보고, 쓰는 [[191_transaction_concept_states|트랜잭션]]은 새 [[288_version_ihl_tos_total_length|버전]]을 만들어 충돌을 줄이는 방식이다.

하지만 MVCC만으로 모든 문제가 끝나지는 않는다. 같은 자원을 동시에 수정하려는 순간에는 낙관 락킹의 재시도 정책이나 비관 락킹의 선점 정책이 필요하다. 그래서 시험과 실무 모두에서 MVCC는 "[[288_version_ihl_tos_total_length|버전]] 관리"와 "잠금 [[268_strategy_pattern|전략]]"을 함께 보는 주제로 이해해야 한다.

```text
┌────────────┐    ┌────────────────┐    ┌────────────────┐
│ Readers    │──▶│ Versioned Rows │◀──│ Writers Create │
│ Snapshot   │    │ MVCC Snapshot  │    │ New Versions   │
└────────────┘    └────────────────┘    └────────────────┘
```

이 그림은 읽기와 [[289_cqrs_db|쓰기]]를 같은 길에 세우지 않고, [[288_version_ihl_tos_total_length|버전]]이라는 우회로를 만들어 [[014_concurrency|동시성]]을 높이는 발상을 보여 준다. 따라서 설계 문서에는 어떤 격리 수준에서 어떤 충돌을 허용·차단하는지 분명히 적어야 한다.

- **📢 섹션 요약 비유**: 같은 공책을 돌려 쓰지 않고 복사본을 보며 수정본을 따로 만드는 회의 방식과 같다.

## Ⅱ. 아키텍처 및 핵심 원리

MVCC의 핵심 원리는 [[191_transaction_concept_states|트랜잭션]] 시작 시점 기준으로 보이는 [[288_version_ihl_tos_total_length|버전]]을 판단하고, 갱신 시에는 새 [[288_version_ihl_tos_total_length|버전]]을 추가하는 것이다. [[002_database_definition|데이터베이스]]는 보통 행 [[288_version_ihl_tos_total_length|버전]] 정보, [[393_undo|undo]] 영역, vacuum 또는 purge 과정으로 오래된 [[288_version_ihl_tos_total_length|버전]]을 정리한다. 여기에 충돌 처리 방식으로 낙관 락킹은 커밋 시 충돌을 [[396_validation|확인]]하고, 비관 락킹은 수정 전 잠금을 먼저 획득한다. 감리 관점에서는 단순 이론보다 충돌 패턴과 운영 비용이 실제 업무와 맞는지가 중요하다.

```text
┌────────┐      ┌────────┐      ┌────────┐
│ Row V1 │───▶│ Row V2 │───▶│ Row V3 │
└────────┘      └────────┘      └────────┘
     ▲               ▲
     │               └── Writer Commit
     └────────────────── Reader Snapshot
```

| 구성축 | 핵심 내용 | 감리 포인트 |
|:---|:---|:---|
| 가시성 규칙 | [[191_transaction_concept_states|트랜잭션]]별 [[022_snapshot_backup_architecture|스냅샷]] 기준으로 보이는 [[288_version_ihl_tos_total_length|버전]]을 선택 | 격리 수준별 허용 현상과 차단 현상이 명확해야 한다 |
| [[288_version_ihl_tos_total_length|버전]] 관리 | [[393_undo|undo]], xmin/xmax, vacuum 등으로 과거 [[288_version_ihl_tos_total_length|버전]] 유지·정리 | 장기 [[191_transaction_concept_states|트랜잭션]]과 [[288_version_ihl_tos_total_length|버전]] 누적으로 인한 [[282_performance_tactics|성능]] 저하를 관리해야 한다 |
| 낙관 락킹 | [[288_version_ihl_tos_total_length|버전]] 컬럼이나 타임스탬프로 커밋 시 충돌 [[396_validation|확인]] | 충돌 빈도가 낮은 업무에 적합하며 재시도 정책이 필요하다 |
| 비관 락킹 | 수정 전 선점 잠금으로 충돌 자체를 예방 | 재고 차감 등 충돌이 잦은 구간은 잠금 대기와 교착을 함께 관리해야 한다 |

결국 MVCC는 잠금을 없애는 기술이 아니라 잠금이 필요한 구간을 줄이는 기술이다. 답안에서는 [[022_snapshot_backup_architecture|스냅샷]] 읽기, [[288_version_ihl_tos_total_length|버전]] 정리, 충돌 처리, 격리 수준을 한 묶음으로 설명해야 한다.

- **📢 섹션 요약 비유**: 도서관에서 열람용 책은 복사본으로 보고, 원본 수정은 담당자가 순서대로 처리하는 운영과 같다.

## Ⅲ. 비교 및 연결

[[014_concurrency|동시성]] 제어는 MVCC 하나로 끝나지 않는다. 순수 비관 락킹은 안전하지만 대기 시간이 길고, 낙관 락킹은 빠르지만 충돌 시 재시도 비용이 있다. MVCC는 읽기 [[282_performance_tactics|성능]]을 크게 개선하지만 [[289_cqrs_db|쓰기]] 충돌이 많은 구간에서는 별도 잠금 정책과 함께 써야 한다.

| 비교 항목 | MVCC | 낙관 락킹 | 비관 락킹 |
|:---|:---|:---|:---|
| 기본 발상 | 다중 [[288_version_ihl_tos_total_length|버전]]으로 읽기-[[289_cqrs_db|쓰기]] 충돌 완화 | 커밋 시 충돌 [[395_verification_process_review|검증]] | 수정 전 잠금 선점 |
| 읽기 [[282_performance_tactics|성능]] | 매우 우수 | 우수 | 잠금 영향 큼 |
| 충돌 처리 | [[288_version_ihl_tos_total_length|버전]] 가시성 + 필요 시 잠금 병행 | 실패 후 재시도 | 선점으로 예방 |
| 적합 업무 | 읽기 많은 [[327_hint_handoff|OLTP]], 혼합 워크로드 | 충돌 적은 협업 수정 | 재고, 좌석, 한정 수량 처리 |
| 주의점 | [[288_version_ihl_tos_total_length|버전]] 누적, vacuum 비용 | 재시도 폭증 가능 | 교착, 대기 시간 증가 |

또한 이 주제는 격리 수준, [[454_undo_segment_rollback|언두]]/[[455_redo_log_archive|리두]], 데드락, 팬텀 리드, [[637_zfs_snapshot_cow_architecture|Snapshot]] Isolation과 이어진다. 시험에서는 이 연관 개념을 함께 언급해야 MVCC가 단순 용어 암기가 아니라 운영 선택지임을 보여 줄 수 있다.

- **📢 섹션 요약 비유**: 줄을 세워 하나씩 처리할지, 번호표를 나눠 빠르게 보되 충돌 때 다시 부를지 정하는 창구 운영과 같다.

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[002_database_definition|데이터베이스]] 종류마다 MVCC 구현 방식이 다르고, 업무 충돌 패턴도 제각각이다. 그래서 "우리 DB가 MVCC를 지원한다"는 말만으로는 충분하지 않다. 주문, 결제, 좌석 예약, 게시판처럼 업무 특성에 따라 격리 수준과 잠금 방식이 달라져야 하며, 장기 [[191_transaction_concept_states|트랜잭션]]과 [[288_version_ihl_tos_total_length|버전]] 정리 실패가 [[282_performance_tactics|성능]] 저하로 이어지는지도 함께 봐야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]

- 읽기 비중과 [[289_cqrs_db|쓰기]] 비중, 충돌 hotspot이 수치로 파악되어 있는가?
- 선택한 격리 수준이 더티 리드, 반복 불가 읽기, 팬텀 중 무엇을 허용하는지 명확한가?
- 낙관 락킹의 재시도 정책과 사용자 충돌 안내가 준비되어 있는가?
- 비관 락킹 구간의 [[510_lock|lock]] wait, [[281_deadlock_definition|deadlock]], [[319_timeout_prevention|timeout]] 모니터링이 되는가?
- vacuum, purge, [[393_undo|undo]] 공간 관리가 장기 [[191_transaction_concept_states|트랜잭션]]에 의해 막히지 않는가?
- 재고 차감 같은 핵심 업무에서 MVCC와 명시적 잠금을 어떻게 조합할지 정의되어 있는가?

흔한 실패는 읽기 [[282_performance_tactics|성능]]만 보고 MVCC를 만능처럼 이해하는 것이다. 실제 운영에서는 [[288_version_ihl_tos_total_length|버전]] 누적과 [[289_cqrs_db|쓰기]] 충돌이 [[282_performance_tactics|성능]] 병목을 만들 수 있으므로, 잠금과 정리 비용까지 같이 봐야 한다.

- **📢 섹션 요약 비유**: 복사본을 많이 만들면 회의는 빨라지지만 마지막에 어떤 종이를 공식본으로 확정할지 규칙이 없으면 더 혼란스러운 상황과 같다.

## Ⅴ. 기대효과 및 결론

MVCC를 적절히 활용하면 읽기 지연을 크게 줄이고, 사용자에게 일관된 조회 경험을 제공하며, 높은 [[014_concurrency|동시성]]을 가진 [[327_hint_handoff|OLTP]] 환경에서도 처리량을 높일 수 있다. 여기에 낙관·비관 락킹을 업무별로 조합하면 충돌이 드문 구간과 치열한 구간을 서로 다르게 최적화할 수 있다.

결론적으로 [[014_concurrency|동시성]] 제어 MVCC 낙관 비관 락킹 패턴은 "[[288_version_ihl_tos_total_length|버전]]을 보관하는 기술"을 넘어 "충돌을 어디서 어떤 비용으로 해결할 것인가"를 결정하는 아키텍처 판단 주제다. 답안에서는 [[022_snapshot_backup_architecture|스냅샷]], 잠금, 정리 비용, 업무 적합성을 함께 연결하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 같은 놀이터를 모두가 쓰되, 줄이 긴 미끄럼틀만 따로 순서를 정해 쓰는 운영과 같다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[637_zfs_snapshot_cow_architecture|Snapshot]] [[195_isolation_concurrency_control|Isolation]] | MVCC의 읽기 일관성을 설명하는 대표 격리 개념 |
| [[393_undo|Undo]] / Vacuum | 과거 [[288_version_ihl_tos_total_length|버전]] 유지와 정리 비용을 담당하는 운영 축 |
| Optimistic [[510_lock|Lock]] | 충돌이 적은 업무에서 빠른 갱신을 돕는 방식 |
| Pessimistic [[510_lock|Lock]] | 충돌이 잦은 자원 선점을 보장하는 방식 |
| [[203_lost_update_concurrency_problem|Lost Update]] / Phantom | 격리 수준 판단에서 함께 설명해야 할 [[090_anomaly_insertion_deletion_update|이상 현상]] |

### 📈 관련 키워드 및 발전 흐름도

```text
┌─────────────┐
│ 2PL Locking │
└─────────────┘
       │
       ▼
┌────────────────────┐
│ MVCC Snapshot Read │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ Opt. / Pess. Mix   │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ Isolation Tuning   │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ Vacuum Monitoring  │
└────────────────────┘
```

MVCC는 순수 잠금 중심 제어에서 시작해, 읽기 [[282_performance_tactics|성능]] 개선과 충돌 유형별 잠금 조합으로 발전하는 흐름 속에서 이해하는 것이 좋다.

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 친구가 같은 그림책을 보려고 할 때 한 권만 붙잡으면 싸우게 돼요.
2. 그래서 보는 친구는 복사본을 보고, 고치는 친구는 새 종이에 바꿔 적어요.
3. 다만 같은 곳을 동시에 고치려면 누가 먼저 할지 규칙을 정해야 해요.
