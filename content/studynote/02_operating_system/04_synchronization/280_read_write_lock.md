+++
title = "280. 읽기-쓰기 락 (Read-Write Lock) - 다중 읽기 허용, 쓰기 배타적"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락 (Read-Write [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/), RW [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))은 다수의 독자가 동시에 읽을 수 있으며 단 하나의 저자만 독점적으로 쓸 수 있는 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 원시 객체로, 뮤텍스보다 읽기 집중 환경에서 높은 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 제공한다.
> 2. **가치**: 읽기 연산이 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다 훨씬 빈번한 공유 자료구조([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 객체, 캐시, [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블 등)에서 뮤텍스 대비 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 N배(동시 독자 수만큼) 향상시킬 수 있다.
> 3. **융합**: POSIX `pthread_rwlock_t`, Java `ReentrantReadWriteLock`, C++ `std::shared_mutex`, Linux 커널의 `rwlock_t`와 `rw_semaphore`가 표준 구현이며, [RCU](/knowledge-base/studynote/02_operating_system/04_synchronization/254_rcu_read_copy_update/) ([Read-Copy-Update](/knowledge-base/studynote/02_operating_system/04_synchronization/254_rcu_read_copy_update/))는 독자 측 락조차 제거한 진화 형태다.

---

## Ⅰ. 개요 및 필요성

뮤텍스는 모든 접근을 직렬화하므로, 읽기 작업도 순차적으로 처리된다. 하지만 읽기는 데이터를 수정하지 않으므로 여러 스레드가 동시에 읽어도 일관성이 깨지지 않는다. 읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락은 이 특성을 활용하여 독자들의 동시 읽기를 허용하고, 저자만 독점 접근을 요구한다.

**접근 규칙:**
- 독자 N명 ↔ 독자 M명: **허용** (동시 읽기)
- 독자 N명 ↔ 저자 1명: <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/">상호 배제</a></strong> (읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 분리)
- 저자 1명 ↔ 저자 1명: <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/">상호 배제</a></strong> ([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 독점)

**💡 비유**: 도서관의 참고서 — 여러 학생이 동시에 볼 수 있지만, 선생님이 내용을 수정할 때는 모두 자리를 비워야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">읽기-쓰기 락 접근 매트릭스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Reader</div><div class="kb-diagram-cell">Writer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Reader</div><div class="kb-diagram-cell">✅ OK</div><div class="kb-diagram-cell">❌ Block</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Writer</div><div class="kb-diagram-cell">❌ Block</div><div class="kb-diagram-cell">❌ Block</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">처리량 향상:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">뮤텍스: 최대 1× (항상 직렬화)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RWLock: 최대 독자수× (동시 읽기)</div></div>
</div>
</div>



**📢 섹션 요약 비유**: 읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락은 도서관 열람실 — 여러 학생이 동시에 책을 펼칠 수 있지만, 사서가 서가를 재배치할 때는 모두 나가야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### POSIX 구현

```c
#include <pthread.h>

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// 독자 (Reader)
pthread_rwlock_rdlock(&rwlock);   // 읽기 락 획득 (다른 독자와 공유)
read_shared_data();
pthread_rwlock_unlock(&rwlock);

// 저자 (Writer)
pthread_rwlock_wrlock(&rwlock);   // 쓰기 락 획득 (독점)
update_shared_data();
pthread_rwlock_unlock(&rwlock);
```

### 내부 상태 기계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">읽기-쓰기 락 내부 상태 전이</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">상태:</div><div class="kb-diagram-node">Idle</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">ReadLocked: count=N</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">wrlock 모든 독자 unlock</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">WriteLocked</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-node">Idle</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">writlock 해제</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Idle</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">변수:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">read_count : 현재 읽고 있는 독자 수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">write_pending : 대기 중인 저자 수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">write_locked : 쓰기 락 획득 여부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">독자 우선 정책: write_pending 무시하고 새 독자 진입 허용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">저자 우선 정책: write_pending &gt; 0이면 새 독자 차단</div></div>
</div>
</div>



**[다이어그램 해설]** RW Lock의 내부 구현은 독자 카운터와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 잠금 플래그를 원자적으로 관리한다. 독자 우선(Reader-Preference) 구현에서는 독자가 있으면 새 독자가 즉시 진입하여 저자 기아(Writer [Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))가 발생할 수 있다. 저자 우선(Writer-Preference)에서는 그 반대다. 공정(Fair) 구현은 대기 큐로 기아를 방지하지만 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 감소한다.

### Java ReentrantReadWriteLock

```java
import java.util.concurrent.locks.*;

ReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock readLock  = rwLock.readLock();
Lock writeLock = rwLock.writeLock();

// 캐시 읽기 (여러 스레드 동시)
readLock.lock();
try {
    return cache.get(key);
} finally {
    readLock.unlock();
}

// 캐시 갱신 (단독)
writeLock.lock();
try {
    cache.put(key, value);
} finally {
    writeLock.unlock();
}
```

### 읽기→[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락 업그레이드 문제



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">읽기→쓰기 업그레이드 교착 상태 시나리오</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T1: readLock() 획득</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T2: readLock() 획득</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T1: writeLock() 시도 → T2의 readLock 해제 대기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">T2: writeLock() 시도 → T1의 readLock 해제 대기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 교착 상태! 두 스레드가 서로를 기다림</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">해결: 읽기를 포기하고 쓰기 락을 처음부터 획득</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">또는 StampedLock (Java 8+)의 tryConvertToWriteLock()</div></div>
</div>
</div>



**[다이어그램 해설]** 락 업그레이드(읽기→[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 변환)는 대부분의 RW [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) 구현에서 지원하지 않거나 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)를 유발한다. Java의 `StampedLock`은 낙관적 읽기(Optimistic Read)와 `tryConvertToWriteLock()`으로 이 문제를 보다 안전하게 처리한다.

**📢 섹션 요약 비유**: 읽기→[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 업그레이드 교착은 두 학생이 서로 "당신이 책을 놓으면 내가 수정하겠다"고 고집하다가 영원히 기다리는 상황입니다.

---

## Ⅲ. 비교 및 연결

### RW [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) vs [Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/) vs [RCU](/knowledge-base/studynote/02_operating_system/04_synchronization/254_rcu_read_copy_update/) 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">항목</div><div class="kb-diagram-cell">Mutex</div><div class="kb-diagram-cell">RW Lock</div><div class="kb-diagram-cell">RCU</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">동시 읽기</div><div class="kb-diagram-cell">불가</div><div class="kb-diagram-cell">가능</div><div class="kb-diagram-cell">가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">독자 오버헤드</div><div class="kb-diagram-cell">락비용</div><div class="kb-diagram-cell">카운터비용</div><div class="kb-diagram-cell">사실상 0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">저자 레이턴시</div><div class="kb-diagram-cell">즉시(다음)</div><div class="kb-diagram-cell">즉시(다음)</div><div class="kb-diagram-cell">Grace Period</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기아 방지</div><div class="kb-diagram-cell">정책 필요</div><div class="kb-diagram-cell">정책 필요</div><div class="kb-diagram-cell">없음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구현 복잡도</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">중간</div><div class="kb-diagram-cell">높음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">적합 환경</div><div class="kb-diagram-cell">균등 R/W</div><div class="kb-diagram-cell">읽기 집중</div><div class="kb-diagram-cell">SMP 읽기 집중</div></div>
</div>
</div>



**📢 섹션 요약 비유**: Mutex는 단차선, RW Lock은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 전용 차선(읽기)/일반 차선([쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)) 분리, RCU는 차선 없는 자율 주행 고속도로입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 객체 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>: 마이크로서비스에서 수백 개 스레드가 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 초당 수만 번 읽고, 관리자가 분당 1번 업데이트. RW Lock으로 읽기 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 최대화.
2. <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a></strong>: [B-Tree](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 읽기 접근에 RW Lock을 적용하여 [SELECT](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/) [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 최대화, INSERT/UPDATE/DELETE만 독점.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>읽기:<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 비율 측정</strong>: 90:[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이상이면 RW [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) 효과적. 50:50이면 Mutex와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이 미미.
- <strong>기아 방지 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>: 저자 기아가 허용되지 않는다면 공정 모드 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요.
- **업그레이드 없음 원칙**: 읽기 락 보유 중 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락 획득 시도 금지.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 집중 환경</strong>: [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 잦으면 독자 우선 RW Lock이 계속 락-언락을 반복해 오히려 뮤텍스보다 느림.
- **읽기 락 범위 과대**: 락을 오래 보유하면 저자 기아 심화.

**📢 섹션 요약 비유**: 읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락은 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 매우 드문 환경에서만 약이 되는 처방 — [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 잦은 환경에서는 오히려 독이 됩니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | [Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/) | RW [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) (공정) |
|:---|:---|:---|
| 독자 8개 동시 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | 1× | 최대 8× |
| 저자 기아 | 없음 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 필요 |
| 구현 복잡도 | 낮음 | 중간 |

읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락은 읽기 집중 환경에서 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 극적으로 향상시키는 강력한 도구다. 단, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비율, 기아 허용 여부, 락 업그레이드 필요성을 사전에 분석해야 올바른 선택이 가능하다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [이진 세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/225_binary_semaphore/) vs 뮤텍스 차이 ([소유권 유무](/knowledge-base/studynote/02_operating_system/04_synchronization/278_binary_semaphore_vs_mutex/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [재진입 가능 락](/knowledge-base/studynote/02_operating_system/04_synchronization/279_reentrant_lock/) ([Reentrant Lock](/knowledge-base/studynote/02_operating_system/04_synchronization/279_reentrant_lock/) / Recursive [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) ([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 정의 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) 발생 4가지 필요조건 ([모두 만족해야 발생](/knowledge-base/studynote/02_operating_system/05_deadlock/282_deadlock_four_necessary_conditions/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">재진입 가능 락 (Reentrant Lock / Recursive Lock)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">읽기-쓰기 락 (Read-Write Lock)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">교착 상태 (Deadlock) 정의</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">교착 상태 발생 4가지 필요조건 (모두 만족해야 발생)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 읽기-[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 락은 도서관 규칙 — 여러 친구가 동시에 같은 책을 읽어도 되지만, 내용을 고치려면 모두 나가야 해요.
2. 읽기가 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)보다 훨씬 많을 때(예: 읽기 100번, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 1번) 뮤텍스보다 훨씬 빠른 처리가 가능해요.
3. 주의: 읽고 있던 사람이 "고칠게요"로 바꾸려 하면 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)가 생길 수 있어요 — 항상 다시 줄을 서야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 280 / 800

← **이전**: [279. 재진입 가능 락 (Reentrant Lock / Recursive Lock)](/knowledge-base/studynote/02_operating_system/04_synchronization/279_reentrant_lock/)
**다음**: [281. 교착 상태 (Deadlock) 정의 - 대기 중인 프로세스들이 자원을 점유한 채로 결코 일어나지 않을 사건을 기다리는 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) →

---
