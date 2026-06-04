+++
title = "296. 순환 대기 부정 (Deny Circular Wait)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [교착 상태 예방](/knowledge-base/studynote/02_operating_system/05_deadlock/292_deadlock_prevention/) 관점에서의 [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/) 부정 (Deny [Circular Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)) 기법은 시스템 내의 모든 자원([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))에 고유한 일련번호(ID)를 부여하고 무조건 <strong>오름차순(Ascending order)</strong>으로만 자원을 요청하도록 애플리케이션에 룰을 강제하는 체계다([Lock Hierarchy](/knowledge-base/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/)).
> 2. **가치**: [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/), [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/), [비선점 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/)이 하드웨어 단의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 파괴나 심각한 자원 낭비율(Overhead)의 극심한 부작용으로 실무에서 버림받은 반면, [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/) 부정은 오직 프로그래머의 단 몇 줄짜리 코딩 수학적 질서만으로 데드락을 100% 예방하는 가장 현실적 대안이다.
> 3. **융합**: 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [VFS](/knowledge-base/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)(가상 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템), 멀티스레드 DB 이체 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 로직, 자바/C++ 서버의 [Mutex](/knowledge-base/studynote/02_operating_system/04_synchronization/223_mutex/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 순서 스케줄링 등에 기본 개발 표준 가이드로 탑재되어 소프트웨어 엔지니어링의 교착 예방 바이블(Bible)로 군림하고 있다.

---

## Ⅰ. 개요 및 필요성

[교착 상태 예방](/knowledge-base/studynote/02_operating_system/05_deadlock/292_deadlock_prevention/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 1([상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) 깨기: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)파괴), 2([점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/) 깨기: 자원낭비 기아), 3([비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 깨기: [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 불가능 폭망)이 전부 좌초되면서 공학자들은 절망했다.
하지만 4번째 악당인 [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)(원형 꼬리물기)를 향해 눈을 돌리니 기적의 길이 열렸다. 바로 "자원들의 접근 순서에 위계(Hierarchy)를 세우는 것"이다.

A가 앞(1번)을 보고, B도 앞(2번)을 보고, C도 앞(3번)만 보도록 고개를 고정하면 서로 꼬리를 물어 동그라미(사이클)를 그릴 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)은 위상수학적으로 완벽히 0([Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/))이 된다.

**💡 비유**: 등번호가 큰 선수의 티셔츠만 꼬리잡기가 가능한 강강술래 규칙. 1번은 2번을 잡고, 2번은 3번을 잡지만, 3번은 결코 1번을 잡을 수 없으므로 무조건 뱀처럼 일자(선형) 대기열만 만들어진다. 선형열의 머리(가장 큰 번호)는 항상 탈출할 수 있어서 영원히 막히는 원형 수갑이 성립하지 않는다.

```text
┌────────────────────────────────────────────────────────────────┐
│         Lock Hierarchy(락 위계)를 통한 순환 대기 격파          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [전제 룰] R1(고유번호 10), R2(고유번호 20), R3(고유번호 30)   │
│  절대 규칙: "큰 숫자 자원을 먼저 쥐고, 그보다 작은 숫자        │
│  자원을 요구하면 즉시 Error(혹은 코드 컴파일 금지)!"           │
│                                                                │
│  [시나리오 A: 합법 (데드락 회피성공)]                          │
│  Thread 1: R1(10) 확보 → R2(20) 요청 ──▶ 대기 (정상)           │
│  Thread 2: R2(20) 확보 → R3(30) 요청 ──▶ 대기 (정상)           │
│  → T2는 R3만 없으면 끝내고 R2를 놓는다. 데드락 ❌              │
│                                                                │
│  [시나리오 B: 위법 (데드락의 불씨 자체를 거세)]                │
│  Thread 1: R1(10) 확보 → R2(20) 요청 (정상)                    │
│  Thread 2: R2(20) 확보 → R1(10) 요청 (❌ 규칙 위반 발각!)      │
│  → T2가 20번을 들고 10번을 요구하는 순간 코딩 단계에서         │
│  차단되거나 즉시 실패. 무조건 R1, R2 순으로 잡게 강제.         │
│  → 원형 사이클 조립 차단! 100% 교착 방어력.                    │
└────────────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/) 부정은 놀이공원 원웨이(One-way) 턴스틸 출입구 — 역방향으로 절대 돌아갈 수 없게 만들면, 수천 명이 몰려도 좁은 골목길에 양방향으로 끼어서(데드락) 오지도 가지도 못하는 압사 사고가 완전히 방지됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 전역 순서 부여(Global [Ordering](/knowledge-base/studynote/02_operating_system/04_synchronization/277_semaphore_ordering/))의 위력

이는 하드웨어(CPU/메모리)를 뜯어고칠 필요가 없다.

1. **객체 메모리 주소(System.identityHashCode) 활용**: 자원 고유 ID 발급이 구조적으로 어렵다면, Java 등에서는 `System.identityHashCode` 같이 OS 메모리 바인딩 주소를 꺼내서 주소값이 작은 노드부터 락을 잠그게([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 짠다. 동적으로 생성된 수만 개 객체라도 해시값이 무조건 대소 비교가 되므로 순서화가 완성된다.
2. **해시충돌(Tie) 발생 체인**: 해시코드가 우연히 같다면? 전역적으로 유일성을 보장하는 보조 `TieLock` 모니터를 우선적으로 잡고 들어가도록 예외 루트를 설치해 완벽히 틀어막는다.

**📢 섹션 요약 비유**: 수백만 명의 사람이 엉킬 때 "무조건 주민번호가 빠른 사람이 나이 많은 사람에게 양보해라"는 룰 하나만 던져주면 서로 멱살 잡고 원을 그리는 혼돈의 싸움판이 서열 순서로 한 방에 정리되는 마법입니다.

---

## Ⅲ. 비교 및 연결

| 4조건 부정 타겟 | 시스템 희생량(Overhead) | 실무 융합 및 도입율 | 결과 |
|:---|:---|:---|:---|
| 1번. [상호 배제 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/293_deny_mutual_exclusion/) | 매우 높음 ([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오염) | 읽기전용([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/)) 외 도입 0% | 사실상 불가 |
| 2번. [점유 대기 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/294_deny_hold_and_wait/) | 매우 높음 (기아, [자원 선점](/knowledge-base/studynote/02_operating_system/05_deadlock/311_resource_preemption/) 쓰레기율) | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 폭망으로 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 대체 | 이론상 포기 |
| 3번. [비선점 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/) | 매우 높음 ([롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 불가 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 붕괴) | RDBMS 내주 깊숙한 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)만 사용| 범용 불가 |
| <strong>4번. <a href="/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/">순환 대기</a> 부정</strong> | **극저 코딩 약간 귀찮음** | <strong>OS <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 개발 표준 코딩 룰 안착</strong> | **유일한 100% 통과** |

**📢 섹션 요약 비유**: 나머지 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 데드락을 없애자고 집을 다 철거하거나 냉장고를 부수는 무식한 짓이지만, 4번 타격은 문고리에 '한 방향으로 미시오' 스티커 하나만 붙이면 평생 이득을 버는 초가성비 효율 전법입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 시나리오**:
1. **은행 계좌 이체(A→B)**: [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 트래픽이 쏟아지는 은행 코어. Account A가 B에게 송금(A 락 걸고 B 락 걸고 출입금) 시도 중, B가 A에게 동시 이체하면 바로 교착.
   - *해결 코드*: `if (A.id < B.id) { lock(A); lock(B); } else { lock(B); lock(A); }` 단 4줄만으로 세계 멸망급 데드락을 수학적으로 증발시킴.
2. <strong>리눅스 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/">Lock Hierarchy</a>)</strong>: VFS의 dentry 락 리스트, mm(메모리) 서브시스템의 [세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) 체인 등은 문서 가이드라인 수준을 넘어 매크로 레벨로 "1. inode_lock(), 2. page_lock() 순서로 호출할 것. 어기면 [커널 패닉](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/)!" 을 박아넣어 거대한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스의 자체 데드락을 방어하고 있다.

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>:
- <strong>블랙박스형 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 내 락 (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/279_reentrant_lock/">Reentrant Lock</a> Mixing)</strong>: 내가 외부 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) `lib_C`를 부르는데, 내 A자원 락을 잡고 부른다. 그런데 `lib_C` 내부에선 B자원 락을 잡은 뒤 콜백으로 다시 내 A자원 락을 시도하도록 내부 난독화되어있다면? 전역 순서가 내 의도와 무관하게 완전히 파괴되어 악마의 [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)가 발발. ([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) Wrapping 추상화의 가장 끔찍한 부작용).

**📢 섹션 요약 비유**: 이체 코드 4줄에 `if (내 번호 < 네 번호)`만 넣으면 100만 명이 동시에 송금해도 한 줄로 번호표 뽑고 들어가게 변신합니다. 천재적인 로직의 승리입니다.

---

## Ⅴ. 기대효과 및 결론

| 기준 | 무조건 점유 락([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) 위험) | [락 순서화](/knowledge-base/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/)([Lock Hierarchy](/knowledge-base/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/)) 방식 |
|:---|:---|:---|
| 발생 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) | 스레드가 얽히면 즉시 패닉 발생 | 순환 사이클 원천 형성 `0%` |
| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비용 | 없음 | `O(1)`~메모리 주소 비교 수준(제로 오버헤드) |
| 단점 | 위험 방치 (운영 시 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 필요) | 다중 자원을 요구 시 순서를 미리 계산해 잡아야 하는 유연성 부족 |

데드락 발생 4조건(상호배제, 점유대기, [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/), 순환대기) 중에서 '유일하게 숨통이 트인 오아시스'가 바로 4번([순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/) 부정)이다. 컴퓨팅 생태계는 예방의 물리적 족쇄를 집어던지고 [타조 알고리즘](/knowledge-base/studynote/02_operating_system/05_deadlock/291_ostrich_algorithm/)(무시)으로 달려갔음에도, 단 하나 이 <strong>우아하고 비용 없는 순서화 코딩 가이드라인</strong>만은 성경 구절처럼 남겨 전 세계의 백엔드와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 지탱하는 버팀목으로 삼았다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [점유 대기 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/294_deny_hold_and_wait/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [비선점 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [교착 상태 회피](/knowledge-base/studynote/02_operating_system/05_deadlock/297_deadlock_avoidance/) ([Deadlock Avoidance](/knowledge-base/studynote/02_operating_system/05_deadlock/297_deadlock_avoidance/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) ([Safe State](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[비선점 부정]
    │
    ▼
[순환 대기 부정 (Deny Circular Wait)]
    │
    ├──▶ [교착 상태 회피 (Deadlock Avoidance)]
    └──▶ [안전 상태 (Safe State)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)는 나쁜 친구들이 동그랗게 둘러앉아 서로 상대방의 과자를 뺏기 전까진 내 과자를 안 주겠다고 버티는 어리석은(데드락) 놀이예요.
2. 이걸 박살 내는 건, "항상 자기 옷(메모리)에 쓰인 번호가 더 작은 사람부터 과자를 달라고 해라!" 는 규칙 하나면 충분해요.
3. 그러면 동그라미는 끊어지고, 가장 번호표 큰 친구는 늘 꼬리에 있기 때문에 기분 좋게 놀고 떠날 수 있어서 아무도 영원히 굶어 멈추지(교착) 않는 마법 같은 규칙이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 296 / 800

← **이전**: [295. 비선점 부정 (Deny No Preemption)](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/)
**다음**: [297. 교착 상태 회피 (Deadlock Avoidance) - 실행 전 자원 할당 상태를 검사하여 안전한 경우에만 승인](/knowledge-base/studynote/02_operating_system/05_deadlock/297_deadlock_avoidance/) →

---
