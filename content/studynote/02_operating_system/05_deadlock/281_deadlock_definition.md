---
title: "Deadlock Definition"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 281
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 교착 상태 (Deadlock)는 두 개 이상의 프로세스들이 각자 자원을 점유한 채로, 다른 프로세스가 보유한 자원을 기다리면서 영원히 실행을 재개하지 못하는 상태다.
> 2. **가치**: 교착 상태는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설계의 4가지 조건이 동시에 충족될 때만 발생하며, 이 중 1개만 제거해도 교착이 방지된다 — 이것이 모든 데드락 예방 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 수학적 기반이다.
> 3. **융합**: 멀티스레드 프로그래밍, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [2PL](/studynote/02_operating_system/05_deadlock/320_two_phase_locking_deadlock/) ([Two-Phase Locking](/studynote/05_database/04_transactions_concurrency/511_two_phase_locking/)), [분산 트랜잭션](/studynote/05_database/04_transactions_concurrency/248_distributed_transaction_multiple_nodes/), 네트워크 [자원 할당](/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/)에서 교착 상태는 반복 등장하는 핵심 장애 패턴이다.

---

## Ⅰ. 개요 및 필요성

교착 상태는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 역사에서 가장 고전적이고 반복적인 문제 중 하나다. 1965년 [다익스트라](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) (Edsger W. [Dijkstra](/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))가 처음 공식화했으며, 현재도 실제 시스템에서 발생하는 실질적 장애다.

**교착 상태 정의**: 집합 내의 모든 프로세스가 집합 내의 다른 프로세스에 의해서만 발생될 수 있는 이벤트를 대기하는 상황. 즉, 서로가 서로의 완료를 기다려 아무도 진행하지 못한다.

**💡 비유**: 4거리 도로에서 4대의 차량이 각자 오른쪽 차선이 비어야 움직일 수 있다고 할 때, 각자 자기 차로를 점유한 채로 오른쪽 차량이 먼저 움직여 주길 대기하면 영원히 아무도 움직이지 못한다.

```text
+--------------------------------------------------------------+
|          교착 상태 고전 예시: 두 프로세스, 두 자원           |
+--------------------------------------------------------------+
|                                                              |
|    P1 보유: 자원 A    P1 요청: 자원 B                        |
|    P2 보유: 자원 B    P2 요청: 자원 A                        |
|                                                              |
|         [자원 A]                                             |
|         /       <-- P1 요청 실패                              |
|        ^                  ↖                                  |
|      P1 보유              P2 요청 (자원A)                    |
|        \                        /                            |
|         [P1] -------------- [P2]                             |
|                              ^                               |
|         [자원 B]            /                                |
|         ^ P2 보유  <-------/                                  |
|                                                              |
|  P1: {A 보유, B 대기}  P2: {B 보유, A 대기}                  |
|  -> 영구 대기 -> 교착 상태!                                    |
+--------------------------------------------------------------+
```

**📢 섹션 요약 비유**: 교착 상태는 "네가 먼저 비켜주면 내가 갈게"를 서로 고집하다가 아무도 이동하지 못하는 상황입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4가지 필요충분조건 (모두 동시에 성립해야 교착 발생)

```text
+--------------------------------------------------------------+
|          교착 상태 4가지 필요조건                            |
+--------------------------------------------------------------+
|                                                              |
|  ① 상호 배제 (Mutual Exclusion)                              |
|     -> 자원은 한 번에 한 프로세스만 사용 가능                 |
|     -> e.g., 물리적 프린터, 뮤텍스 보호 데이터                |
|                                                              |
|  ② 점유 대기 (Hold-and-Wait)                                 |
|     -> 최소 하나의 자원을 보유한 채로 다른 자원을 대기        |
|     -> e.g., DB 트랜잭션이 row lock 보유 중 다른 row 요청     |
|                                                              |
|  ③ 비선점 (No Preemption)                                    |
|     -> 프로세스가 보유 중인 자원을 강제로 빼앗을 수 없음      |
|     -> e.g., 락은 보유 프로세스만 해제 가능                   |
|                                                              |
|  ④ 순환 대기 (Circular Wait)                                 |
|     -> P1->P2->P3->P1 형태의 대기 순환이 존재                    |
|     -> e.g., 자원 할당 그래프에 사이클 형성                   |
|                                                              |
|  ⚠ 4개 중 1개만 없애도 교착 상태 발생 불가!                  |
+--------------------------------------------------------------+
```

**[다이어그램 해설]** 이 4조건은 교착 상태의 필요충분조건이다 (단일 인스턴스 자원 환경). 예방 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 이 중 하나를 구조적으로 불가능하게 만드는 것이며, 각 조건별 예방 방법의 현실적 한계도 다르다. 특히 순환 대기는 자원 번호 순서화로 현실적 예방이 가능한 유일한 조건이다.

### [자원 할당 그래프](/studynote/02_operating_system/05_deadlock/287_resource_allocation_graph/) ([Resource-Allocation Graph](/studynote/02_operating_system/05_deadlock/287_resource_allocation_graph/))

```text
+--------------------------------------------------------------+
|        자원 할당 그래프 — 교착 상태 표현                     |
+--------------------------------------------------------------+
|                                                              |
|  표기법:                                                     |
|  ○ : 프로세스 (Pi)     □ : 자원 유형 (Rj)                    |
|  Pi -> Rj : 자원 요청 간선                                    |
|  Rj -> Pi : 자원 할당 간선                                    |
|                                                              |
|  교착 상태 예:                                               |
|                                                              |
|  P1 --요청---> [R2] --할당---> P2                              |
|   ^                               |                          |
|   | 할당                          | 요청                     |
|   |                               v                          |
|  [R1] <---요청-- P3 <---할당-- [R3] <---요청-- P2               |
|                                                              |
|  -> 사이클 존재: P1->R2->P2->R1->P3->R3->P2 ❌ 교착!                |
|                                                              |
|  단일 인스턴스: 사이클 = 교착 상태                           |
|  다중 인스턴스: 사이클 ≠ 교착 상태 (필요조건일 뿐)           |
+--------------------------------------------------------------+
```

**[다이어그램 해설]** [자원 할당 그래프](/studynote/02_operating_system/05_deadlock/287_resource_allocation_graph/)는 교착 상태 분석의 시각적 도구다. 단일 인스턴스 자원(자원 유형 당 1개 인스턴스)에서는 사이클이 존재하면 교착 상태가 성립한다. 다중 인스턴스 자원에서는 사이클이 있어도 대기 중인 프로세스들의 자원 요청이 다른 방식으로 충족될 수 있으므로, 사이클은 교착의 필요 조건이지 충분 조건이 아니다.

**📢 섹션 요약 비유**: [자원 할당 그래프](/studynote/02_operating_system/05_deadlock/287_resource_allocation_graph/)의 사이클은 도로에서의 원형 교통 정체 — 모두가 앞 차만 바라보고 있어 사이클을 끊어줄 수 없는 상태입니다.

---

## Ⅲ. 비교 및 연결

### 교착 상태 처리 방법 3가지

```text
+------------------+------------------+-------------------------+
| 방법             | 전략             | 비용                    |
+------------------+------------------+-------------------------+
| 예방 (Prevention)| 4조건 중 1개 제거| 자원 이용률 저하        |
| 회피 (Avoidance) | 은행원 알고리즘  | 사전 정보 필요, 오버헤드|
| 탐지+복구        | 그래프 탐지+종료 | 교착 발생 후 처리       |
| 무시 (Ostrich)   | 발생 시 재시작   | 가장 낮은 오버헤드      |
+------------------+------------------+-------------------------+
```

<strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>별 채택 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>:</strong>
- **Linux/Windows**: 대부분 Ostrich (무시). 사용자가 강제 종료 또는 재시작.
- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a></strong>: 탐지+[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) ([대기 그래프](/studynote/02_operating_system/05_deadlock/305_wait_for_graph/) 주기적 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 희생자 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)).
- **실시간 OS (RTOS)**: 예방 (PCP/PIP으로 [우선순위 역전](/studynote/02_operating_system/03_cpu_scheduling/205_priority_inversion/) 및 교착 예방).

**📢 섹션 요약 비유**: 교착 처리는 화재 대응처럼 — 예방(스프링클러), 감지+진화(소방관), 무시(작은 불은 스스로 꺼지길 기대)로 나뉩니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 교착</strong>: T1이 row A를 잠금하고 row B를 요청, T2가 row B를 잠금하고 row A를 요청 -> 교착. DB는 [대기 그래프](/studynote/02_operating_system/05_deadlock/305_wait_for_graph/)로 탐지 후 한 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/).
2. **Java 멀티스레드**: 클래스 A의 `synchronized methodA()`가 클래스 B를 호출하고, B의 `synchronized methodB()`가 A를 호출 -> 교착. [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Dump로 감지 가능.
3. **네트워크 라우터**: 패킷이 순환 경로로 라우팅되어 각 라우터 버퍼를 점유하면 네트워크 수준 교착.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) (예방)
- <strong><a href="/studynote/02_operating_system/04_synchronization/276_lock_hierarchy/">락 순서화</a></strong>: 여러 락이 필요하다면 전역 순서를 정해 반드시 오름차순으로 획득.
- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/">타임아웃</a></strong>: 락 획득에 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 설정하여 영구 대기 방지.
- <strong><a href="/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a> Dump 분석</strong>: JVM `jstack`, Linux `pstack`으로 교착 스레드의 락 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/).

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **중첩 락 역순**: [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) A -> [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) B로 잠그는 스레드와 [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) B -> [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/) A로 잠그는 스레드가 공존하면 즉각 교착 후보.
- **락 보유 중 외부 호출**: 락을 보유한 채로 외부(다른 클래스, 콜백, 원격 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))를 호출하면 호출 대상이 어떤 락을 잡는지 모르는 상태에서 교착 발생 위험.

**📢 섹션 요약 비유**: 락 역순 획득은 마치 좌->우 순서로 가야 하는 도로에서 일부 차량이 우->좌로 역주행하는 것 — 충돌(교착)은 시간 문제입니다.

---

## Ⅴ. 기대효과 및 결론

교착 상태는 예방 비용, 탐지 비용, 무시 비용 사이의 트레이드오프다. 일반 목적 OS는 Ostrich를 채택하는 반면, 고신뢰 시스템([데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), 실시간 제어)은 예방이나 탐지를 반드시 구현한다. 핵심은 4조건 분석을 통해 설계 단계에서 교착 발생 가능성을 차단하는 것이다.

**📢 섹션 요약 비유**: 교착 상태 해결의 핵심은 네 가지 조건 중 하나를 '법적으로 금지'하는 것 — 규칙 하나만 잘 세워도 교착이라는 범죄는 일어날 수 없습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [재진입 가능 락](/studynote/02_operating_system/04_synchronization/279_reentrant_lock/) ([Reentrant Lock](/studynote/02_operating_system/04_synchronization/279_reentrant_lock/) / Recursive [Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [읽기-쓰기 락](/studynote/02_operating_system/04_synchronization/280_read_write_lock/) ([Read-Write Lock](/studynote/02_operating_system/04_synchronization/280_read_write_lock/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 교착 상태 발생 4가지 필요조건 ([모두 만족해야 발생](/studynote/02_operating_system/05_deadlock/282_deadlock_four_necessary_conditions/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [상호 배제](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) ([Mutual Exclusion](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[읽기-쓰기 락 (Read-Write Lock)]
    |
    v
[교착 상태 (Deadlock) 정의]
    |
    +---> [교착 상태 발생 4가지 필요조건 (모두 만족해야 발생)]
    +---> [상호 배제 (Mutual Exclusion)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 두 친구가 각자 크레파스 한 개씩 잡고, "네 것 줘야 내 것 줄게"를 서로 우기는 상황이 교착 상태예요!
2. 이 상황은 ①한 번에 한 명만 사용, ②잡고 기다리기, ③빼앗기 금지, ④서로 기다리기 — 네 가지 조건이 다 갖춰졌을 때 발생해요.
3. 해결하려면 "항상 빨강 먼저, 파랑 나중" 같은 규칙을 미리 정해두면 교착이 생기지 않아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 281 / 800

<- **이전**: [280. 읽기-쓰기 락 (Read-Write Lock) - 다중 읽기 허용, 쓰기 배타적](/studynote/02_operating_system/04_synchronization/280_read_write_lock/)
**다음**: [282. 교착 상태 발생 4가지 필요조건 (모두 만족해야 발생) (Deadlock Four Necessary Conditions)](/studynote/02_operating_system/05_deadlock/282_deadlock_four_necessary_conditions/) ->

---
