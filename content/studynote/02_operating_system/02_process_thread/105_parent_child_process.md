---
title: "105. 부모 프로세스 (Parent Process) / 자식 프로세스 (Child Process)"
date: "2026-03-22"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 부모 프로세스 (Parent [Process](/studynote/12_it_management/05_security_compliance/943_process/))와 자식 프로세스 (Child [Process](/studynote/12_it_management/05_security_compliance/943_process/))는 `fork()` 시스템 콜을 통해 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되며, 자식이 부모의 식별자인 PPID (Parent [Process](/studynote/12_it_management/05_security_compliance/943_process/) ID)를 기록하여 형성하는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 트리형 프로세스 계층 구조다.
> 2. **가치**: 이 계층 구조는 부모의 메모리, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 등 자원을 자식이 상속받게 하여 새로운 작업의 문맥 구성 비용을 최소화하고, 독립적인 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리를 안전하게 분기할 수 있는 구조적 토대를 제공한다.
> 3. **판단 포인트**: 부모는 반드시 `wait()`를 통해 자식의 종료 상태(Exit Status)를 회수해야 하며, 이를 누락하면 시스템 자원을 낭비하는 좀비 (Zombie) 프로세스가 발생하므로 수명주기 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

유닉스 (Unix) 및 리눅스 (Linux) 환경에서 프로그램이 실행되는 기본 단위인 프로세스는 스스로를 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하여 새로운 흐름을 만들어낸다. `fork()` 시스템 콜이 호출되면, 호출한 원본 프로세스는 '부모'가 되고 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 복사본은 '자식'이 된다. 자식 프로세스는 자신의 독립적인 PID ([Process](/studynote/12_it_management/05_security_compliance/943_process/) ID)를 발급받으면서도 PCB ([Process](/studynote/12_it_management/05_security_compliance/943_process/) Control Block) 안에 부모의 PID를 PPID로 저장함으로써 명확한 혈통 관계를 맺는다.

이러한 부모-자식 관계가 필요한 이유는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 작업 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성과 [격리성](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) 때문이다. 사용자가 셸([Shell](/studynote/02_operating_system/01_overview_architecture/044_shell/))에서 명령어를 입력할 때마다 셸 자체가 새로운 프로그램으로 변해버리면 셸은 영영 사라진다. 따라서 셸은 자신의 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본(자식)을 만들어 명령어를 대신 실행(`exec()`)하게 하고, 자신은 자식이 작업을 끝낼 때까지 대기(`wait()`)하는 위임 체계를 갖춰야만 연속적인 시스템 운영이 가능해진다.

- **📢 섹션 요약 비유**: 본사(부모 프로세스)가 새로운 지역에 진출하기 위해 본사의 시스템과 자본을 그대로 물려준 지사(자식 프로세스)를 설립하는 것과 같습니다. 지사가 독립적으로 영업을 마치면 본사에 결과 보고서를 제출해야만 지사가 완전히 청산됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

프로세스 트리의 핵심은 `fork()`, `exec()`, `wait()`, `exit()`로 이어지는 4단계의 라이프사이클 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘이다.

```text
+--------------------------------------------------------------+
|       부모-자식 프로세스의 생명주기 및 상태 전이 다이어그램  |
+--------------------------------------------------------------+
|                                                              |
|  [ Parent Process ]             [ Child Process ]            |
|  (PID: 100, PPID: 10)                                        |
|          |                                                   |
|          +- fork() -----------> (복제 및 분기)                |
|          |                     (PID: 101, PPID: 100)         |
|          |                              |                    |
|          |                              +- exec()            |
|          |                              |  (새 프로그램 로드)|
|          v                              v                    |
|      wait() 대기                    실행 중 (Running)        |
|    (수면 상태 진입)                     |                    |
|          |                              +- exit(status)      |
|          |                              v                    |
|          |<--- SIGCHLD 시그널 --- [ Zombie 상태 진입 ]        |
|          |                       (메모리 해제, PCB 잔류)     |
|          v                              |                    |
|  상태 회수 및 자원 해제 ----------------+                    |
|    (종료 상태 획득)               [ 프로세스 완전 소멸 ]     |
+--------------------------------------------------------------+
```

1. <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> (<code>fork</code>)</strong>: 커널은 부모의 `task_struct`를 복사해 자식에게 할당한다. 이때 자원은 상속되나 주소 공간은 독립적으로 분리된다.
2. <strong>변환 (<code>exec</code>)</strong>: 자식은 상속받은 껍데기에 새로운 실행 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 코드와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 덮어씌워 완전히 다른 프로그램으로 탈바꿈한다.
3. <strong>종료 (<code>exit</code>)</strong>: 자식은 실행을 마치면 메모리를 반환하지만, 부모에게 전달할 종료 코드(Exit Status)를 보관하기 위해 PCB 껍데기만 남긴 채 좀비(Zombie) 상태가 된다.
4. <strong>회수 (<code>wait</code>)</strong>: 부모는 `wait()` 또는 `waitpid()`를 호출하여 자식의 종료 상태를 읽어 들인다. 이 순간 커널은 자식의 남은 PCB마저 파기하여 시스템에서 완전히 지운다.

- **📢 섹션 요약 비유**: 이 과정은 식당에서 메인 셰프(부모)가 수보조(자식)를 고용(`fork`)하여 특정 요리를 맡기고(`exec`), 보조가 요리를 끝내면(`exit`) 셰프가 최종 검수(`wait`)를 해야만 보조가 퇴근할 수 있는 주방의 분업 시스템과 같습니다.

---

## Ⅲ. 비교 및 연결

부모-자식 프로세스 모델은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) ([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) 모델이나 [고아 프로세스](/studynote/02_operating_system/02_process_thread/110_orphan_process/) 대응 메커니즘과 비교할 때 그 특징이 명확해진다.

| 항목 | 부모-자식 프로세스 (멀티프로세스) | 부모-자식 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (멀티스레드) |
|:---|:---|:---|
| **메모리 공간** | `fork()`로 완전히 독립된 공간 할당 | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역 공유 |
| <strong>안정성/<a href="/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">격리성</a></strong> | 자식이 죽어도 부모나 다른 자식에 영향 없음 | 한 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 오류(Segfault)가 전체를 죽임 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a> 통신 비용</strong> | [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/), [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 등 무거운 통신 필요 | 메모리 직접 접근으로 통신 비용 극소화 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 오버헤드</strong> | PCB 및 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)로 무거움 | [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/))만 할당하므로 매우 가벼움 |

부모 프로세스가 자식보다 먼저 비정상 종료되는 경우, 자식은 PPID를 잃어버리고 고아 (Orphan) 프로세스가 된다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이러한 미아를 방치하지 않고 프로세스 트리의 최상위 조상인 `init` 프로세스(PID 1, 현대 리눅스의 systemd)에게 입양시킨다. `init`은 주기적으로 `wait()`를 호출하여 [고아 프로세스](/studynote/02_operating_system/02_process_thread/110_orphan_process/)가 종료될 때 좀비가 되지 않도록 안전하게 거두어들이는 백스톱(Backstop) 역할을 수행한다.

- **📢 섹션 요약 비유**: 프로세스 방식은 각자 자기 사무실을 따로 임대하여(격리) 일하는 것이고, [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 방식은 큰 회의실 하나에 여럿이 모여서 서류를 돌려보며(메모리 공유) 일하는 것과 같습니다. 독립적인 사무실은 한 곳에 불이 나도 안전하지만 임대료(오버헤드)가 비쌉니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대규모 서버 아키텍처나 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서 부모-자식 프로세스의 수명주기 관리는 시스템 장애를 예방하는 가장 중요한 의사결정 포인트다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 판단 포인트
1. <strong><a href="/studynote/02_operating_system/02_process_thread/109_zombie_process/">좀비 프로세스</a> (<a href="/studynote/02_operating_system/02_process_thread/109_zombie_process/">Zombie Process</a>) 누수 방어</strong>: 부모 프로세스에 자식을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 로직만 있고 `wait()` 계열 시스템 콜을 호출하는 로직이 없거나 누락되었다면 최악의 안티패턴이다. 자식이 종료된 후에도 PID 테이블을 차지하는 좀비가 무한히 쌓이게 되며, 결국 커널의 PID 고갈(PID Exhaustion)로 이어져 시스템이 멈추게 된다. 반드시 [비동기적](/studynote/02_operating_system/01_overview_architecture/017_hardware_interrupt/) `SIGCHLD` 시그널 핸들러를 구현하여 `waitpid(WNOHANG)`으로 즉시 회수해야 한다.
2. <strong>백그라운드 <a href="/studynote/02_operating_system/02_process_thread/152_daemonization/">데몬화</a> (<a href="/studynote/02_operating_system/02_process_thread/152_daemonization/">Daemonization</a>) <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: 부모에 종속되지 않고 시스템 백그라운드에서 영구히 동작하는 데몬 프로세스를 만들려면 더블 포크 (Double Fork) 기법을 사용한다. 부모가 자식을 만들고 스스로 즉시 종료(`exit`)해 버리면, 손자 프로세스는 고아가 되어 `init`에 입양됨으로써 원래 터미널의 통제권에서 완전히 벗어난 진정한 백그라운드 워커가 된다.
3. <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> (<a href="/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a>/K8s)의 PID 1 문제</strong>: [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 내부에서 일반 애플리케이션 애플리케이션을 PID 1로 띄우면, 이 앱은 `init` 프로세스가 아니기 때문에 하위 프로세스가 만든 좀비들을 수거할 능력이 없다. 이로 인해 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 내부에 좀비가 가득 차는 장애가 빈번히 발생한다. 이를 막기 위해 `tini`나 `dumb-init` 같은 경량 `init` 프로세스를 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 Entrypoint로 세워 좀비 수거를 위임해야 한다.

- **📢 섹션 요약 비유**: [좀비 프로세스](/studynote/02_operating_system/02_process_thread/109_zombie_process/)는 해고된 직원의 서류가 인사 시스템에서 지워지지 않고 영원히 남아있는 상태입니다. `wait()`는 이 낡은 인사기록 카드를 최종적으로 파쇄하는 도장이며, `init` 프로세스는 퇴사자 서류를 전담으로 치우는 시스템 관리자입니다.

---

## Ⅴ. 기대효과 및 결론

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 부모-자식 프로세스 모델은 복잡한 다중 작업을 안전하게 격리하고 위임하는 가장 검증된 뼈대다.

자원의 상속을 통해 무거운 초기화 비용을 극복하고, 독립된 주소 공간을 통해 하나의 작업 실패가 전체 시스템의 붕괴로 이어지는 것을 원천 차단한다. 현대의 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 이 프로세스 트리 계층 위에 cgroup과 PID [Namespace](/studynote/02_operating_system/01_overview_architecture/061_namespace/) ([네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)) 기술을 융합하여, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)라는 완벽히 독립된 가상의 부모-자식 왕국을 무한히 찍어내는 아키텍처로 진화했다. 프로세스 관계의 핵심은 단순히 낳는 것(`fork`)이 아니라, 책임지고 끝을 맺어주는 것(`wait`)에 있음을 기억해야 한다.

- **📢 섹션 요약 비유**: 부모와 자식 구조는 거대한 피라미드 조직도와 같습니다. 최상위 회장(`init`)부터 각 부서장(부모)과 실무자(자식)로 명령이 내려가고, 일이 끝나면 정확히 위로 보고하여 자원을 정리하는 체계가 있어야만 수만 개의 프로세스가 도는 컴퓨터가 터지지 않고 굴러갑니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **fork() / exec()** | 부모가 자식을 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)(fork)하고, 자식은 새로운 프로그램으로 탈바꿈(exec)하는 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 사이클 콜. |
| **wait() / exit()** | 자식이 종료 코드를 남기고(exit), 부모가 이를 수거하여(wait) 자원을 최종 반환하는 소멸 사이클 콜. |
| <strong><a href="/studynote/02_operating_system/02_process_thread/109_zombie_process/">좀비 프로세스</a> (Zombie)</strong> | 자식이 종료되었으나 부모가 `wait()`를 해주지 않아 시스템에 껍데기만 남아있는 프로세스. |
| <strong><a href="/studynote/02_operating_system/02_process_thread/110_orphan_process/">고아 프로세스</a> (Orphan)</strong> | 부모가 먼저 죽어버려 갈 곳을 잃고 PID 1(`init`)에게 입양되는 프로세스. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 프로세스 시스템 (MS-DOS)
    |
    v
부모-자식 프로세스 계층 (Unix fork/exec 모델 도입)
    |
    v
멀티스레딩 (Multithreading, 프로세스 내 자원 공유 및 경량화)
    |
    v
cgroup 및 Namespace (리눅스 커널의 자원 격리 기술)
    |
    v
컨테이너 기반 독립 프로세스 트리 (Docker, Kubernetes)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 '부모' 프로그램이 '자식' 프로그램을 낳아서 여러 가지 심부름을 시키는 규칙이 있어요.
2. 자식 프로그램이 심부름을 다 끝내면, 부모에게 "다 했어요!"라고 결과(종료 상태)를 보고해야만 쉴 수 있어요.
3. 만약 부모가 결과를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 안 해주고 가버리면 자식은 길을 잃은 '고아'나 유령 같은 '좀비'가 되니까, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 할아버지(init)가 나서서 다 정리해준답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 105 / 800

<- **이전**: [104. 프로세스 생성 (Process Creation) - fork(), exec() 시스템 콜](/studynote/02_operating_system/02_process_thread/104_process_creation/)
**다음**: [106. Copy-on-Write (COW) - fork() 최적화 기법](/studynote/02_operating_system/02_process_thread/106_copy_on_write/) ->

---
