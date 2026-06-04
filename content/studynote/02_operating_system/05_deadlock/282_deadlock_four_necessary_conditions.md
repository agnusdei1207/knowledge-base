+++
title = "282. 교착 상태 발생 4가지 필요조건 (모두 만족해야 발생) (Deadlock Four Necessary Conditions)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) ([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 발생 4가지 필요조건은 E. G. Coffman이 1971년에 정리한 이론으로 [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)([Mutual Exclusion](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)), [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/)([Hold and Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/)), [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)([No Preemption](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)), [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)([Circular Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/))가 <strong>동시에 모두 충족</strong>되어야만 데드락이 발생한다는 법칙이다.
> 2. **가치**: 데드락이라는 시스템 결빙 버그를 "네 가지 퍼즐 조각이 모인 상태"라는 구조적 결함으로 해석케 함으로써, 운영체제나 개발자가 단 하나라도 조건을 파괴(Prevent)하거나 빗겨가(Avoid)도록 설계해 안전한 서비스를 구축할 명쾌한 엔지니어링 가이드라인을 제공한다.
> 3. **융합**: DB 트랜잭션의 [배타 락](/knowledge-base/studynote/05_database/04_transactions_concurrency/215_exclusive_lock_write_concurrency/)([Mutual Exclusion](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)), 멀티 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 프로그래밍에서의 중첩 락(Hold & Wait), 외부 자원 점유 강제 박탈(Preemption), 락 획득 순서 넘버링([Circular Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/) 예방) 등 현대 백엔드 오류 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 해결 기법과 직결된다.

---

## Ⅰ. 개요 및 필요성

차량이 교차로 한가운데 네 방향에서 뒤엉켜 서로가 상대방이 비켜주기를 영원히 기다리는 상태가 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))다. 이 비극은 단순한 재수 없음이 아니다. 시스템 공학에서는 이 치명적 멈춤 뒤에 <strong>정확히 4가지의 <a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적 조건</strong>이 존재함을 밝혀냈다.

이 조건들은 "개별적으로는 유용하게 설계된 규칙"이지만, 특정 타이밍에 4개가 모두 얽혀 들어가는 순간 프로세스가 자멸(영원한 대기)하게 만들어 버린다.

**💡 비유**: 범죄가 성립하려면 범행 의도(1), 수단(2), 대상(3), 기회(4)가 다 있어야 하듯, [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)라는 '에러 범죄'도 4가지 나쁜 타이밍 조건이 하나의 단단한 매듭으로 묶여야 발생합니다.

```text
┌──────────────────────────────────────────────────────────────┐
│         교착 상태(Deadlock)의 네 가지 퍼즐 조각              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [조건 1] 상호 배제 (Mutual Exclusion)                       │
│  한 번에 한 명만 쓰는 배타적 자원이어야 함.                  │
│  (모두가 같이 쓰는 벤치라면 싸움 안 남)                      │
│                                                              │
│  [조건 2] 점유하며 대기 (Hold and Wait)                      │
│  내 것을 꽁꽁 쥔 채로 남의 것을 내놓으라고 버텨야 함.        │
│  (손 풀고 처음부터 다시 요청하면 싸움 안 남)                 │
│                                                              │
│  [조건 3] 비선점 (No Preemption)                             │
│  운영체제(경찰)나 다른 놈이 억지로 뺏을 수 없음.             │
│  (경찰이 강제로 뺏어서 분배 가능하면 싸움 안 남)             │
│                                                              │
│  [조건 4] 순환 대기 (Circular Wait)                          │
│  물고 물리는 고리 형태(A→B→C→A)로 서로를 원해야 함.          │
│  (직선 구조면 끝사람이 끝내면 차례가 오지만 순환은 영원함)   │
│                                                              │
│   → 이 4개가 우연히 한 프레임에 모두 공존(AND 조건) 시       │
│      시스템은 영구 정지(데드락)!                             │
└──────────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: 4조건은 무인도 뱀 꼬리 물기 — 각자 방(배타)에 숨어서([비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)), 앞 뱀의 꼬리를 잡은 채(점유) 절대 안 놓고(대기), 다 같이 원형(순환)으로 원수지간이 되는 완벽한 붕괴 공식입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 각 조건의 세부 성질

1. <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/">상호 배제</a> (Mutual exclusiveness)</strong>:
   프린터, 뮤텍스 락처럼 공유 불가한(Non-sharable) 모드로만 접근 가능한 자원이 원인. (읽기 전용 파일처럼 다중 접근을 놔두면 데드락 0)
2. <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/">점유 대기</a> (<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/">Hold and wait</a>)</strong>:
   기본 자원 1개를 선점해 놓은 프로세스가 나머지 2번 자원을 확보하려고 OS 블록 큐에 잠들면서 기존 1번 자원을 안 뱉음.
3. <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/">비선점</a> (<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/">No preemption</a>)</strong>:
   프로세스가 작업을 다 끝내고 `release()` 하기 전까지는 외부 힘으로 그 자원을 "강제 스위칭 탈취" 해올 아키텍처 지원이 없음. (CPU나 메모리는 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/) 선점이 되서 데드락이 덜 나나, DB Lock은 강제 탈취시 오염)
4. <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/">순환 대기</a> (<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/">Circular wait</a>)</strong>:
   대기하는 노드들의 체인이 {P0 → P1 → P2 → ... → P0} 형태의 순환 위상수학적 사이클 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(Cycle [Graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/))를 그리는 상태.

**📢 섹션 요약 비유**: 4가지 룰이 조합된 절대 반지 — "나만 써(1), 남의 것도 가질래(2), 강제 압수 안 됨(3), 원형으로 목조르기(4)". 단 하나라도 룰을 어기면 절대 반지는 산산조각 납니다.

---

## Ⅲ. 비교 및 연결

데드락 관리 관점에서 이 4조건을 어떻게 바라보고 대처할 것인가:

| 필요조건 | 부정(Prevention) 해결 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 실무의 현실 한계 |
|:---|:---|:---|
| [상호 배제 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/293_deny_mutual_exclusion/) | 모든 걸 공유 가능하게 만듦 (Read-only 위주 패러다임) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Update)가 필수적 자원은 원천 불가 |
| [점유 대기 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/294_deny_hold_and_wait/) | 식당 갈 때 포크, 숟가락 등 일체를 예약 성공시만 착석 | 활용 안 하는 시간에도 점유하여 자원 폭망 |
| [비선점 부정](/knowledge-base/studynote/02_operating_system/05_deadlock/295_deny_no_preemption/) | 다른 걸 대기해야 할 때는 자발적으로 내 락을 다 내려놓음 | 중간 저장(Commit/[Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/)) 복원 처리 난해 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/05_deadlock/296_deny_circular_wait/">순환 대기 부정</a></strong> | 자원에 고유 `넘버링`하여 `반드시 오름차순 번호`로만 취득 | <strong>가장 현실적인 실무 방어 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>. <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/">Lock Hierarchy</a></strong> |

**📢 섹션 요약 비유**: 방어 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 중 "오름차순 번호표"가 최고 — 락에 1번, 2번 등표를 달아 "2번을 가진 자는 1번을 요구할 수 없다"고 수학적 룰을 주면 고리가 형성될([순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)) 일이 구조적으로 사라집니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**실무 시나리오**:
1. <strong>DB 애플리케이션 데드락 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> (MySQL InnoDB)</strong>: [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) A가 `Table 1` Update 중이고 [Transaction](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) B가 `Table 2` Update 중이다. 이때 서로를 교차 Update 요청하는 순간, [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)(Row 락), [점유 대기](/knowledge-base/studynote/02_operating_system/04_synchronization/231_hold_and_wait/), [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/)가 터진다. DB [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 강제로 한 명을 죽여([비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 파괴/Preemption 강제) 희생자(Victim [Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))로 만들고 나머지 하나를 구제한다.
2. <strong>사내 OS 코어 팀 - <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> Order 규정</strong>: Linux [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 기여할 때 개발 안내 가공문에는 "락을 A, B 순으로 획득해야 한다"는 위계 질서 가이드라인([Lock Hierarchy](/knowledge-base/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/))이 박혀있다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단위 패닉 방지를 위한 [순환 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/286_circular_wait/) 조기 억제책이다.

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>:
- <strong>자원 여러 개에 무작위 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> 획득 짜깁기</strong>: 주니어 개발자들이 객체 C, 객체 D가 들어오는 순서대로 `syschronized(x)`를 마구잡이 교차 중첩할 때 나타남. 철저하게 "항상 메모리 주소(ID)가 정렬 오름차순이 되도록 락킹"하는 훈련이 필요.

**📢 섹션 요약 비유**: 주먹구구로 이 문 저 문 잠그는 건 교차로 꼬리물기 — 서로 순서 규칙을 안 지키니 가운데 얽히면 나가지도 못하는 대형사고(데드락)가 납니다. 규칙적으로 들어가야 안전해요.

---

## Ⅴ. 기대효과 및 결론

| 접근 방식 | 4가지 조건의 위상 | 엔지니어링 패러다임 |
|:---|:---|:---|
| 발생 이론 (Coffman) | 4가지 `AND` | 이 4조합은 절대 회피해야 할 블랙홀 |
| 데드락 예방 (Prevention) | 4개 중 `최소 한 개 파괴` | 시스템 레벨에서 강력히 원천 규제 |
| 데드락 무시 (Ostrich) | 4개 공존 `운영체제 허용 (알빠노)`| 발생해봤자 드무니 재부팅 하라 (현대 데스크톱) |

[교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)를 유령처럼 두려워할 것이 아니라, 코프먼 4-Condition이라는 이성의 렌즈로 보면 시스템 정지 원인이 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로처럼 명백해진다. 이 4조건 모두가 성립하려 할 찰나를 방어([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) 획득 순서화, [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 등)하는 것이야말로 진정한 멀티 스레딩 및 DB 병행 튜닝의 마스터 코스다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [읽기-쓰기 락](/knowledge-base/studynote/02_operating_system/04_synchronization/280_read_write_lock/) ([Read-Write Lock](/knowledge-base/studynote/02_operating_system/04_synchronization/280_read_write_lock/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) ([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 정의 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) ([Mutual Exclusion](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [점유하며 대기](/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/) ([Hold-and-Wait](/knowledge-base/studynote/02_operating_system/05_deadlock/284_hold_and_wait/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[교착 상태 (Deadlock) 정의]
    │
    ▼
[교착 상태 발생 4가지 필요조건 (모두 만족해야 발생) (Deadlock Four Necessary Conditions)]
    │
    ├──▶ [상호 배제 (Mutual Exclusion)]
    └──▶ [점유하며 대기 (Hold-and-Wait)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 게임기가 1개, 컨트롤러가 1개뿐입니다. 형은 게임기를 안고 컨트롤러를 내놓으라 하고, 동생은 컨트롤러를 쥔 채 게임기 내놓으라고 싸웁니다.
2. 둘 다 욕심(하나뿐임, 남 안 줌, 안 뺏김, 서로 노려봄)이라는 4가지 룰이 다 뭉쳐버렸기 때문에 엄마가 오기 전까진 절대로 게임을 시작할 수 없는 멈춤 늪에 빠집니다.
3. 이 네 가지 나쁜 타이밍 룰이 합쳐지는 순간, 컴퓨터 시스템도 완전 얼어붙는 것이 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)(데드락) 조건입니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 282 / 800

← **이전**: [281. 교착 상태 (Deadlock) 정의 - 대기 중인 프로세스들이 자원을 점유한 채로 결코 일어나지 않을 사건을 기다리는 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)
**다음**: [283. 상호 배제 (Mutual Exclusion) - 자원은 비공유 모드로만 사용 가능](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) →

---
