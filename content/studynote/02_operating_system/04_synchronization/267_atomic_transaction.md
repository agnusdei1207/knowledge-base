---
title: "267. Atomic Transaction"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 267
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 여러 개의 개별적인 연산([명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/))들을 논리적으로 <strong>'쪼갤 수 없는 단일 작업(Atomic)'</strong>으로 묶어, "All or Nothing (전부 성공하거나 아예 실패하거나)" 원칙을 강제하는 시스템 메커니즘이다.
> 2. **가치**: 중간에 시스템이 정전되거나 예기치 않은 오류가 발생했을 때, 데이터가 '반만 처리된(Inconsistent)' 끔찍한 상태로 남는 것을 방지하고, 시스템을 항상 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/studynote/09_security/01_intro_principles/003_integrity/))이 유지되는 안전한 상태로 보호한다.
> 3. **융합**: [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(Journaling), [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 ACID 특성 제어, [다중 스레드](/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/) 환경에서의 메모리 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)([STM](/studynote/02_operating_system/04_synchronization/268_software_transactional_memory/)) 등 시스템 소프트웨어 전반을 지탱하는 가장 근본적인 아키텍처 철학이다.

---

## Ⅰ. 개요 및 필요성

> ⚠️ 이 문서는 시스템에서 여러 작업이 모두 성공적으로 완료되거나, 아니면 아예 아무 작업도 하지 않은 상태로 되돌아가야 함을 보장하는 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 및 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)의 최고 수준 모델인 '원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)'을 다룹니다.

은행에서 A의 계좌에서 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000원을 빼서 B의 계좌로 입금하는 프로그램을 짠다고 가정해 보자.
1. `A 계좌에서 10,000원 차감` (성공)
2. `B 계좌에 10,000원 입금` **(이때 서버 전원 차단됨!)**

시스템이 재부팅된 후, A의 돈 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000원은 공중으로 증발해 버렸다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)나 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 입장에서 이렇게 '연산의 중간 상태'가 디스크나 메모리에 영구적으로 기록되는 것은 시스템의 신뢰성을 완전히 파괴하는 재앙이다.
학자들은 "여러 개의 코드로 이루어진 작업이지만, 바깥에서 볼 때는 **완벽하게 한방에 실행된 것처럼 보이거나 아예 시작도 안 한 것처럼 보여야 한다**"는 철학을 고안했다. 이것이 물리학의 쪼갤 수 없는 입자인 '원자(Atom)'의 이름을 딴 <strong>원자적 <a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>(Atomic <a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">Transaction</a>)</strong>이다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 실행 중에 임시 공간(Log 또는 섀도우 복사본)에만 변경 사항을 적어둔다. 진짜 데이터는 아직 건드리지 않는다. 그리고 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)의 마지막 줄에 도달했을 때 오직 두 가지 결말 중 하나를 맞이한다.

1. **커밋 (Commit)**
   - [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 내의 모든 연산이 단 하나의 에러도 없이 완벽하게 끝났을 때 선언한다.
   - 커밋이 떨어지는 순간, 임시 공간에 적어둔 변경 사항들이 '실제 시스템 상태(메모리/디스크)'에 영구적(Durable)으로 반영되며 쾅 도장이 찍힌다.
2. <strong>어보트 (Abort) &amp; <a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> (<a href="/studynote/02_operating_system/05_deadlock/313_rollback/">Rollback</a>)</strong>
   - 연산 도중 하드웨어 오류, [교착 상태](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)), 권한 오류 등 단 하나라도 문제가 발생하면 즉시 작업을 중단(Abort)한다.
   - 이때 임시로 끄적여두었던 변경 사항들을 모두 쓰레기통에 버리고, 시스템 상태를 <strong><a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>이 시작되기 바로 직전의 완벽한 상태로 되돌린다(<a href="/studynote/02_operating_system/05_deadlock/313_rollback/">Rollback</a>)</strong>.
   - 사용자 입장에서는 아예 아무 일도 일어나지 않았던 것과 똑같아진다. (All or <strong>Nothing</strong>의 Nothing 달성)

```text
+------------------------------------------------------------------------+
|           원자적 트랜잭션의 생명주기와 All or Nothing 제어 흐름        |
+------------------------------------------------------------------------+
|                                                                        |
| [ 트랜잭션 시작 (Begin) ]                                              |
|         |                                                              |
|         v                                                              |
|    연산 1 수행 ---> (로그에 기록, 실제 데이터는 변경 안 함)             |
|         |                                                              |
|         v          💣 에러 발생! (시스템 다운 등)                      |
|    연산 2 수행 ------> [ Abort 발동 ] ---> (로그 폐기, 롤백) --+         |
|         |                                                |             |
|         v (모두 성공 시)                                     v         |
| [ 트랜잭션 완료 (Commit) ]                              [ 원상 복구 ]  |
|         |                                                |             |
|         v                                                v             |
|  (로그를 실제 데이터에 덮어씀)                           (Nothing)     |
|       (All)                                                            |
+------------------------------------------------------------------------+
```

**[다이어그램 해설]** 핵심은 "작업을 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 공간([로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 등)에서 미리 연습해 본 뒤, 완벽하게 성공할 확신이 들 때만 진짜 데이터에 덮어쓰는 것"이다. 에러가 나면 그냥 연습장을 찢어버리면 그만이다. 이것이 원자성을 보장하는 가장 고전적이면서도 완벽한 기법인 '[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)([Log-based Recovery](/studynote/05_database/04_transactions_concurrency/237_log_based_recovery_redo_undo_records/))'의 원리다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

[데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)뿐만 아니라 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)도 자체적으로 이 원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 매초마다 수천 번씩 사용한다. 가장 대표적인 것이 <strong><a href="/studynote/02_operating_system/09_file_system/539_journaling_file_system/">저널링 파일 시스템</a>(<a href="/studynote/02_operating_system/09_file_system/539_journaling_file_system/">Journaling File System</a>)</strong>이다.

* **문제 상황**: 사용자가 1GB짜리 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 지우고 있다. OS는 디스크의 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)(inode)를 지우고, 비트맵을 업데이트하는 3~4개의 작업을 순서대로 진행한다. 그런데 중간에 플러그가 뽑힌다.
* **비극**: inode는 지워졌는데 비트맵은 업데이트가 안 되어, 디스크 용량이 영원히 증발해 버린 '고아 블록(Orphan Block)' 상태가 된다. ([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 깨짐)
* <strong>저널링(<a href="/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/">트랜잭션</a>)의 방어</strong>: OS는 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 지우기 전에, 디스크의 구석진 일기장(Journal)에 "나 이제 이거 지울 거야"라고 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 남긴다. 플러그가 뽑혀 재부팅되면, OS는 일기장부터 뒤져본다. "어? 지우다가 말았네? 그럼 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 꼬이지 않게 아예 지우기 전 상태로 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)시켜!" [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 절대 깨지지 않게 방어해 낸다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

"완벽하게 해내지 못할 바엔, 차라리 흔적조차 남기지 마라."
원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 단순히 데이터를 다루는 기법을 넘어, 복잡계 시스템(Complex System)이 치명적인 오류 앞에서도 스스로 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 지켜내기 위한 가장 우아하고 강력한 디자인 패턴이다. [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어([Concurrency Control](/studynote/05_database/04_transactions_concurrency/508_concurrency_control/))의 뮤텍스나 세마포어가 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 간의 '교통정리'를 담당한다면, 원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 그 교통정리 도중 발생하는 사고 자체를 없었던 일로 되돌리는 시간의 마법사다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) (Atomic [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)) 개념은 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)와 [상호 배제](/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) 제어을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [소프트웨어 트랜잭셔널 메모리](/studynote/02_operating_system/04_synchronization/268_software_transactional_memory/) ([STM](/studynote/02_operating_system/04_synchronization/268_software_transactional_memory/))처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 낙관적 병행성 제어 ([Optimistic Concurrency Control](/studynote/05_database/04_transactions_concurrency/223_optimistic_concurrency_control_validation/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 비관적 병행성 제어 (Pessimistic [Concurrency Control](/studynote/05_database/04_transactions_concurrency/508_concurrency_control/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [소프트웨어 트랜잭셔널 메모리](/studynote/02_operating_system/04_synchronization/268_software_transactional_memory/) ([STM](/studynote/02_operating_system/04_synchronization/268_software_transactional_memory/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [하드웨어 트랜잭셔널 메모리](/studynote/02_operating_system/04_synchronization/269_htm_intel_tsx/) ([HTM](/studynote/01_computer_architecture/15_advanced_topics/513_htm/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[비관적 병행성 제어 (Pessimistic Concurrency Control)]
    |
    v
[원자적 트랜잭션 (Atomic Transaction) 개념]
    |
    +---> [소프트웨어 트랜잭셔널 메모리 (STM)]
    +---> [하드웨어 트랜잭셔널 메모리 (HTM]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 로봇을 조립하는데, 팔만 끼우고 다리는 못 끼운 채로 멈추면 괴물 로봇이 되어버리겠죠?
2. 원자적 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)은 "로봇을 완벽하게 다 조립하거나(All), 아니면 아예 부품 상자에서 꺼내지도 않은 처음 상태(Nothing)로 되돌리거나" 둘 중 하나만 허락하는 마법의 상자에요.
3. 덕분에 중간에 정전이 되거나 컴퓨터가 고장 나도, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 데이터가 반쯤 망가진 채로 남아버리는 끔찍한 일은 절대 일어나지 않는답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 267 / 800

<- **이전**: [266. 페이지 부재 빈도 (PFF, Page Fault Frequency)](/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)
**다음**: [268. 소프트웨어 트랜잭셔널 메모리 (STM)](/studynote/02_operating_system/04_synchronization/268_software_transactional_memory/) ->

---
