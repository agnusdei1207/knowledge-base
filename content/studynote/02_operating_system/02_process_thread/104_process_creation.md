+++
title = "104. 프로세스 생성 (Process Creation) - fork(), exec() 시스템 콜"
date = 2026-03-22

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로세스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Creation)은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 실행 중인 프로그램을 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하고 새로운 작업을 지시하는 메커니즘으로, 유닉스(Unix) 계열에서는 `fork()`와 `exec()` 시스템 콜의 조합으로 이루어진다.
> 2. **가치**: 기존 프로세스(Parent)를 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)하여 뼈대를 만들고(`fork`), 그 내부에 새로운 프로그램의 영혼을 덮어씌우는(`exec`) 분리된 접근법을 통해 프로세스 계층 구조를 직관적으로 관리하고 쉘([Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/))의 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 같은 유연한 동작을 가능하게 한다.
> 3. **판단 포인트**: 현대 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 메모리 낭비를 막기 위해 [Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) ([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 복사 기법을 사용하여 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비용을 최소화하며, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경에서는 `clone()` 시스템 콜로 확장되어 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 격리까지 제어한다.

---

## Ⅰ. 개요 및 필요성

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서 새로운 프로세스를 만든다는 것은 CPU 자원을 할당받고 메모리 공간을 독자적으로 소유하는 새로운 생명체를 탄생시키는 일이다. 유닉스 아키텍처에서는 이 과정을 `fork()`와 `exec()`라는 두 단계의 시스템 콜([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))로 분리했다. `fork()`는 호출한 프로세스를 그대로 복사하여 자식 프로세스(Child [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))를 만들고, `exec()`는 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)된 자식의 메모리 공간에 완전히 새로운 프로그램을 덮어씌워 실행을 전환한다.

이러한 분리 구조가 도입된 이유는 유연성 때문이다. 만약 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 실행이 하나로 묶여 있다면, 부모 프로세스가 자식에게 넘겨줄 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터([File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) Descriptor)나 [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/) 같은 자원 설정을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점과 실행 시점 사이에 개입하여 조작할 수 없다. `fork-exec` 모델은 쉘에서 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)(`|`)나 리다이렉션(`>`) 처리를 아주 우아하게 구현할 수 있는 핵심 토대다.

- **📢 섹션 요약 비유**: `fork`는 도화지에 밑그림과 팔레트(메모리와 자원)를 똑같이 복사하는 일이고, `exec`는 그 복사된 도화지 위에 완전히 새로운 수채화 풍경(새로운 프로그램)을 덧칠해 덮어버리는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

프로세스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Mode)에서 PCB ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Control Block)를 할당하고 메모리 구조를 구성하는 복잡한 과정이다. 

| 시스템 콜 | 역할 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부 동작 | 결과 |
|:---|:---|:---|:---|
| **fork()** | 프로세스 골격 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 부모의 PCB 복사, 새로운 PID 할당, 메모리 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) ([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 적용) | 부모와 똑같은 코드를 실행하는 2개의 분기점 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| **exec()** | 새로운 영혼 덮어씌우기 | 기존 메모리 공간 초기화, ELF(실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) 바이너리 로드, 힙/[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 초기화 | 지정된 완전히 새로운 프로그램으로 실행 전환 |
| **wait()** | 자식 [프로세스 종료](/knowledge-base/studynote/02_operating_system/02_process_thread/107_process_termination/) 회수 | 부모가 자식의 종료 상태를 읽어 좀비(Zombie) 프로세스가 되는 것을 방지 | 자원 반환 및 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 완료 |

```text
┌──────────────────────────────────────────────────────────────┐
│           fork() + exec() 프로세스 분기 및 전환 흐름          │
├──────────────────────────────────────────────────────────────┤
│  [1. 부모 프로세스]                                             │
│      PID: 1000 ────────┐ (fork 호출)                         │
│                        │                                     │
│                        ├─▶ [2. 자식 프로세스 복제 탄생]        │
│                        │       PID: 1001 (부모의 메모리 공유) │
│                        │       (COW: Copy-on-Write 대기)     │
│                        │                                     │
│                        │   (exec 호출)                       │
│  (wait 대기)            │   [3. 자식 프로세스 덮어쓰기]        │
│  [4. 자식 종료 수거]◀───┘       PID: 1001 유지               │
│                            메모리 공간 초기화 후 새 바이너리 실행│
└──────────────────────────────────────────────────────────────┘
```

이 흐름의 핵심은 **[Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) ([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/))** 메커니즘이다. 과거에는 `fork()` 시점에 묻지도 따지지도 않고 부모의 전체 메모리를 통째로 복사해 엄청난 오버헤드가 발생했다. 현대 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 물리 메모리 복사를 미루고, 부모와 자식이 같은 물리 메모리 주소를 읽기 전용으로 가리키게 한다. 어느 한쪽이 데이터에 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(Write)를 시도하는 순간에만 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))를 발생시켜 해당 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 하나만 복사한다. `fork()` 직후 `exec()`가 호출되면 어차피 기존 메모리는 버려지므로, COW는 메모리 할당 낭비를 극적으로 방지하는 구원 투수다.

- **📢 섹션 요약 비유**: [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 방식의 `fork()`는 회사 기안서를 통째로 복사해 나눠주는 것이 아니라, 모두가 클라우드 공유 문서 링크만 보다가 누군가 글씨를 수정하려고 키보드를 누르는 순간에만 개인용 사본을 만들어 주는 효율적인 시스템이다.

---

## Ⅲ. 비교 및 연결

프로세스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 아키텍처에 따라 유닉스의 분리형 모델과 윈도우의 통합형 모델로 명확히 나뉜다.

| 비교 항목 | 유닉스 계열 (fork + exec) | 윈도우 계열 (CreateProcess) |
|:---|:---|:---|
| **설계 철학** | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 후 덮어쓰기 (2단계 분리) | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)부터 실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 지정 (1단계 통합) |
| **자원 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)** | `fork()` 직후 쉘이 I/O 리다이렉션 개입 용이 | 함수 파라미터(STARTUPINFO 등)로 명시적 제어 |
| **메모리 복사** | [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) ([Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/)) 최적화 필수 | 독립 공간 할당으로 [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 복사 오버헤드 불필요 |

유닉스의 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)(`ls | grep`)는 두 프로세스를 `fork`한 뒤 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 입출력을 변경하고 각각 `exec`로 넘기는 방식을 쓴다. 통합형은 이런 조작을 함수 파라미터 구조체에 우겨넣어야 해서 복잡도가 높아진다. 
최근 리눅스 생태계는 단순한 `fork()`를 넘어, 어떤 자원을 부모와 공유할지 세밀하게 비트마스크로 제어하는 **`clone()`** 시스템 콜을 발전시켰다. [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 같은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기술은 바로 이 `clone()`의 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/)([Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/)) 격리 기능을 활용하여 가상 머신처럼 격리된 독립 프로세스 트리를 만들어낸다.

- **📢 섹션 요약 비유**: 유닉스의 방식은 밀가루 반죽(fork)을 떼어낸 뒤 원하는 틀(exec)에 넣어 빵을 굽는 방식이고, 윈도우 방식은 처음부터 별도의 공장 라인(CreateProcess)을 돌려 바로 완성된 빵을 뽑아내는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

시스템의 안정성을 지키려면 무분별한 자원 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)을 차단하는 통제가 반드시 필요하다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터 유출 차단 (FD_CLOEXEC)**: 백엔드 데몬이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)을 열어둔 채 무심코 `fork()` + `exec()`를 수행하면, 부모의 민감한 DB 커넥션 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터가 자식(외부 스크립트 등)에게 그대로 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)되어 보안 사고가 터진다. `open()`이나 `exec()` 사용 시 반드시 보안 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)(`O_CLOEXEC`)를 세팅하여 실행 덮어쓰기 순간에 불필요한 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 자동 단절되게 해야 한다.
2. **[좀비 프로세스](/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/) ([Zombie Process](/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/)) 예방**: 부모가 `fork`만 해놓고 자식의 종료 신호를 수거하는 `wait()` 처리를 누락하면, 자식은 죽었음에도 프로세스 테이블(PCB)의 슬롯을 영원히 차지하는 좀비가 된다. 이로 인해 시스템의 최대 프로세스 제한(ulimit)을 초과하여 서버가 마비되는 Fork Bomb에 대비해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **무거운 쓰레드 풀 환경에서의 fork 남용**: 다수의 쓰레드가 동작하는 멀티쓰레드 프로세스(예: JVM, 톰캣) 안에서 갑자기 `fork()`를 호출하면, 다른 쓰레드들은 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)되지 않고 호출한 단일 쓰레드만 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)된 불완전한 프로세스가 태어난다. 메모리 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))이나 뮤텍스 상태가 엉켜 심각한 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))를 유발하므로, 멀티쓰레드 환경에서는 안전한 `posix_spawn()` 같은 대체재를 써야 한다.

- **📢 섹션 요약 비유**: 부모 프로세스가 자식에게 무심코 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터를 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)하는 것은, 사무실을 떠나는 직원이 보안 서버 로그인 키가 꽂힌 컴퓨터 화면을 안 끄고 알바생에게 그대로 자리를 넘겨주는 치명적인 보안 사고와 같다.

---

## Ⅴ. 기대효과 및 결론

`fork()`와 `exec()` 모델은 유닉스의 철학을 가장 잘 보여주는 간결하고도 강력한 아키텍처다. '모든 것은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다'라는 원칙 아래, 프로세스의 환경 조작과 실행의 타이밍을 분리함으로써 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 역사의 흐름을 주도했다.

오늘날에는 [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 기법이 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)의 오버헤드를 극적으로 줄여주었지만, 극단적인 고성능 최적화가 필요한 시대에는 `posix_spawn()`이나 세분화된 `clone()` 등 다양한 진화 모델이 함께 쓰이고 있다. 결국 프로세스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)의 핵심은 "어떻게 하면 가장 가볍고 안전하게 새로운 생태계를 격리하여 출범시킬 것인가"라는 자원 통제의 문제로 귀결된다.

- **📢 섹션 요약 비유**: `fork`와 `exec`는 세포가 스스로를 분열한 뒤, 완전히 새로운 유전자(DNA)로 탈바꿈하여 새로운 개체가 되는 것과 같습니다. 이는 수십 년간 컴퓨팅 생태계를 풍성하게 만들어 온 가장 기초적이면서도 효율적인 생명 탄생의 공식입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[Copy-on-Write](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) ([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/))** | `fork()`로 인한 거대한 메모리 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 비용을 막기 위해, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 동작이 발생할 때만 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 복사하는 메모리 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 최적화 기법 |
| **[좀비 프로세스](/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/) ([Zombie Process](/knowledge-base/studynote/02_operating_system/02_process_thread/109_zombie_process/))** | 종료되었으나 부모가 `wait()`로 수거하지 않아 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) PCB 메모리 슬롯을 낭비하는 상태 |
| **`clone()` 시스템 콜** | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 시대의 핵심 기술로, 자원 공유 범위와 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/)를 세밀하게 제어하여 프로세스를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 고도화된 인터페이스 |
| **FD_CLOEXEC (Close-on-Exec)** | `exec()`가 호출되어 프로그램이 덮어씌워질 때 부모로부터 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)받은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)/디스크립터가 자동으로 닫히도록 강제하는 보안 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) |

### 📈 관련 키워드 및 발전 흐름도

```text
초기 유닉스 생성 철학 (fork() + exec() 분리)
    │
    ▼
메모리 복제 오버헤드 발생 (통째로 메모리 복사)
    │
    ▼
메모리 가상화 최적화 도입 (Copy-on-Write 지연 복사)
    │
    ▼
멀티쓰레드 환경의 fork 부작용 회피 (posix_spawn 등장)
    │
    ▼
컨테이너 격리 생태계를 위한 세밀한 자원 분리 제어 (clone(), Namespace)
```

### 👶 어린이를 위한 3줄 비유 설명

1. `fork()`는 마법의 거울 앞에서 내 모습을 뼈대까지 똑같이 쌍둥이로 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 내는 주문이에요.
2. `exec()`는 그렇게 만들어진 쌍둥이에게 기존 기억을 다 지우고, 완전히 새로운 게임팩을 머릿속에 끼워 넣어 새로운 로봇으로 만드는 주문이죠.
3. [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)할 때 무거운 짐까지 다 베껴오면 너무 힘드니까, 컴퓨터는 '글씨를 쓸 때만 복사([COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/))'하는 얌체 같은 꼼수로 엄청 빨리 쌍둥이를 만든답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 104 / 800

← **이전**: [103. 스레드 풀 (Thread Pool)](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)
**다음**: [105. 부모 프로세스 (Parent Process) / 자식 프로세스 (Child Process)](/knowledge-base/studynote/02_operating_system/02_process_thread/105_parent_child_process/) →

---
