+++
weight = 149
title = "149. 클론 (clone) 시스템 콜 - 리눅스 프로세스와 스레드 생성의 통합 API"
date = "2026-05-03"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: `clone()` 시스템 콜은 리눅스 [[022_kernel_role|커널]]에서 프로세스([[300_process|Process]])와 [[092_thread_lwp|스레드]]([[092_thread_lwp|Thread]])를 [[087_process_state_transition|생성]]하는 유일하고도 가장 근원적인 범용 인터페이스([[014_api_posix|API]])이다.
> 2. **가치**: 기존 유닉스의 무식한 자원 전체 복사(`fork`) 방식을 넘어, `CLONE_*` [[186_character_stuffing_dle_stx_etx|플래그]] 조합을 통해 부모와 자식 간의 메모리, [[501_file_definition_logical_record|파일]] 디스크립터, 시그널 핸들러 공유 수준을 핀셋처럼 세밀하게 튜닝할 수 있는 극한의 유연성을 제공한다.
> 3. **판단 포인트**: 우리가 흔히 쓰는 사용자 수준의 `fork()`(최소 공유)와 `pthread_create()`(최대 공유)는 결국 껍데기일 뿐이며, 내부적으로는 모두 각기 다른 [[186_character_stuffing_dle_stx_etx|플래그]]를 달고 이 `clone()` 시스템 콜 하나로 수렴([[010_schema_mapping|Mapping]])되는 아키텍처 융합의 정수다.

---

## Ⅰ. 개요 및 필요성

과거 전통적인 유닉스 시스템에서는 새로운 실행 흐름을 만들기 위해 오직 `fork()` 시스템 콜만을 사용했다. `fork()`는 부모의 메모리, [[501_file_definition_logical_record|파일]], 시그널 등 모든 것을 100% 똑같이 복사하여 무거운 자식 프로세스를 만들어내는 방식이었다. 하지만 덩치가 큰 프로세스를 매번 복사하는 것은 너무 무거웠고, 가벼운 [[092_thread_lwp|스레드]]([[092_thread_lwp|Thread]])라는 개념이 등장하면서 자원의 '복사'가 아닌 '공유'의 필요성이 폭발했다.

리눅스 아키텍트인 리누스 토르발스는 [[092_thread_lwp|스레드]] 전용 시스템 콜을 따로 만드는 대신, 천재적인 통합 API인 `clone()`을 탄생시켰다. `clone()`은 "부모의 물건 중 어떤 것을 공유하고 어떤 것을 새로 만들지"를 인자([[186_character_stuffing_dle_stx_etx|Flag]])로 받아 통제하는 마법의 복사기다. 이로써 리눅스 [[022_kernel_role|커널]] 내부에서는 프로세스와 [[092_thread_lwp|스레드]]의 구분이 사라지고, 오직 '자원을 얼마나 공유하는 [[150_task|Task]]([[150_task|태스크]])[[509_authorization_models_rbac_abac|인가]]'라는 철학만 남게 되었다.

- **📢 섹션 요약 비유**: `clone()`은 이사할 때 쓰는 '맞춤형 계약서'와 같습니다. "내 물건을 다 복사해서 새집에 줄게(`fork`)"부터 "방만 따로 쓰고 거실, 주방, 화장실은 나랑 100% 같이 쓰자(`pthread_create`)"까지, 체크박스([[186_character_stuffing_dle_stx_etx|플래그]])만 껐다 켜면 어떤 형태의 이사든 다 처리해 주는 만능 계약서입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

`clone()` 시스템 콜의 핵심은 매개변수로 전달되는 `flags`의 [[073_bit|비트]] 마스킹([[086_fenwick_tree|Bit]] Masking) 조합이다.

```text
┌─────────────────────────────────────────────────────────────┐
│          clone() 시스템 콜의 아키텍처와 자원 공유 플래그 맵핑        │
├─────────────────────────────────────────────────────────────┤
│  long clone(unsigned long flags, void *child_stack, ...);   │
│                                                             │
│ [ 자원 관리 4대 핵심 플래그 (CLONE_*) ]                          │
│                                                             │
│  1. CLONE_VM      : 메모리 공간(Address Space) 공유 여부          │
│  2. CLONE_FS      : 파일 시스템(루트, 현재 디렉토리) 공유 여부       │
│  3. CLONE_FILES   : 열린 파일 디스크립터(FD) 테이블 공유 여부        │
│  4. CLONE_SIGHAND : 시그널 핸들러 공유 여부                       │
│                                                             │
│ [ 스택(Stack)의 철칙 ]                                        │
│  ★ 스레드든 프로세스든 각자의 실행 흐름을 보장해야 하므로,             │
│    `child_stack` 매개변수로 반드시 **새로운 깡통 스택**을 줘야 한다!     │
└─────────────────────────────────────────────────────────────┘
```

**[내부 동작 메커니즘]**
- [[186_character_stuffing_dle_stx_etx|플래그]]가 꺼져 있으면(`0`), [[022_kernel_role|커널]]은 부모의 자료구조(예: `mm_struct`)를 딥 카피(Copy)하여 자식에게 독립적인 사본을 쥐여준다. (물론 최적화를 위해 Copy-on-Write가 적용됨)
- [[186_character_stuffing_dle_stx_etx|플래그]]가 켜져 있으면(`1`), [[022_kernel_role|커널]]은 새로운 자료구조를 만들지 않고 부모의 자료구조 포인터 주소만 자식에게 연결(Share)해 주고 [[316_reference_pattern_nosql|참조]] 카운트([[316_reference_pattern_nosql|Reference]] Count)만 1 증가시킨다. 깃털처럼 가벼운 [[087_process_state_transition|생성]]이 이루어진다.

- **📢 섹션 요약 비유**: `clone()` 시스템 콜은 컴퓨터 안의 '주민센터 복사기'입니다. [[186_character_stuffing_dle_stx_etx|플래그]](버튼) 조작에 따라 서류 전체를 칼라 복사해서 완전히 다른 뭉치를 만들어주기도 하고(프로세스), 원본 서류 하나를 책상 가운데 놓고 여러 명이 같이 보도록 연결만 쓱 해주기도([[092_thread_lwp|스레드]]) 합니다.

---

## Ⅲ. 비교 및 연결

우리가 C언어에서 흔히 호출하는 사용자 수준 [[014_api_posix|API]](`fork`, `pthread_create`)가 [[022_kernel_role|커널]]에서 어떻게 `clone()`으로 변환되는지 융합 비교한다.

| 사용자 [[014_api_posix|API]] | [[022_kernel_role|커널]] 내부의 `clone()` 호출 맵핑 (개념적) | 특징 및 자원 공유 수준 |
| :--- | :--- | :--- |
| **`fork()`** | `clone(SIGCHLD, ...)` | **[독립/최소 공유]** 모든 [[186_character_stuffing_dle_stx_etx|플래그]]가 꺼져 있음. 부모와 자식은 메모리, [[501_file_definition_logical_record|파일]], 시그널이 완전히 분리된 별개의 평행 우주(프로세스)를 산다. |
| **`vfork()`** | `clone(CLONE_VFORK \| CLONE_VM, ...)` | **[메모리만 임시 공유]** `exec()`를 부르기 전까지 부모를 잠재우고, 자식이 부모의 메모리를 빌려 쓰는 특수 변형 [[087_process_state_transition|생성]]. |
| **`pthread_create()`** | `clone(CLONE_VM \| CLONE_FILES \| CLONE_SIGHAND \| CLONE_THREAD, ...)` | **[밀착/최대 공유]** 모든 공유 [[186_character_stuffing_dle_stx_etx|플래그]]가 켜져 있음. [[057_stack|스택]](방)만 따로 받고, 메모리/[[501_file_definition_logical_record|파일]]/시그널(거실/주방)은 100% 완벽히 공유하는 [[092_thread_lwp|스레드]]를 창조. |

가장 파격적인 [[186_character_stuffing_dle_stx_etx|플래그]]는 **`CLONE_THREAD`**다. 이 [[186_character_stuffing_dle_stx_etx|플래그]]가 켜지면 [[087_process_state_transition|생성]]된 자식은 부모와 동일한 [[092_thread_lwp|스레드]] 그룹 ID(TGID)를 갖게 되어, 외부(OS)에서 볼 때 부모와 자식을 '하나의 같은 프로세스 덩어리'로 취급하게 만드는 마법의 스위치다.

- **📢 섹션 요약 비유**: `fork()`는 나랑 완전히 똑같이 생긴 아바타를 만들어서 '아예 다른 동네(독립 프로세스)'로 이사 보내는 것입니다. `pthread_create()`는 나랑 100% 똑같은 동생을 만들어서 '내 방앗간(같은 프로세스 안의 [[092_thread_lwp|스레드]])'에 가둬두고 같이 맷돌을 돌리게 만드는 극단적 자원 공유 세팅입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[022_kernel_role|커널]] 해커나 [[561_container_based_deployment|컨테이너]] 아키텍트에게 `clone()`은 단순한 [[087_process_state_transition|생성]]을 넘어 시스템을 격리하는 무기가 된다.

### 실무 판단 시나리오
1. **[[063_docker_architecture|도커]]([[063_docker_architecture|Docker]]) [[561_container_based_deployment|컨테이너]] 격리의 비밀병기 ([[061_namespace|Namespace]] [[186_character_stuffing_dle_stx_etx|플래그]])**: 클라우드 엔지니어가 묻는다. "[[063_docker_architecture|도커]]는 가상 머신([[598_vm_migration_nic|VM]])도 아닌데 어떻게 프로세스를 완벽히 격리하죠?" 
   - **판단**: 리눅스 [[022_kernel_role|커널]]은 `clone()`에 전통적인 자원 공유 [[186_character_stuffing_dle_stx_etx|플래그]] 외에도 격리 전용 [[186_character_stuffing_dle_stx_etx|플래그]]인 **`CLONE_NEWPID` (PID 격리), `CLONE_NEWNET` (네트워크 격리), `CLONE_NEWNS` ([[516_mount_mechanism|마운트]] 격리)**를 융합해 두었다. [[063_docker_architecture|도커]] 엔진이 [[561_container_based_deployment|컨테이너]]를 띄울 때 사실 이 `clone(CLONE_NEW*)` [[186_character_stuffing_dle_stx_etx|플래그]]들을 잔뜩 먹여서 프로세스를 [[087_process_state_transition|생성]]한다. 즉, `clone()`은 [[092_thread_lwp|스레드]]를 만드는 복사기를 넘어 클라우드 네이티브의 핵심인 **[[561_container_based_deployment|컨테이너]] 격리 기술([[061_namespace|Namespace]])**의 근원적 엔진이다.
2. **비동기 I/O 워커 [[103_thread_pool|스레드 풀]] [[087_process_state_transition|생성]]**: 자체 고성능 웹 서버(WAS)를 C/C++로 구현할 때 수천 개의 워커를 띄워야 한다.
   - **판단**: 무식하게 `fork()`로 프로세스를 찢으면 OS [[079_kube_scheduler_pod_placement|스케줄러]] 오버헤드와 [[357_tlb|TLB]]([[357_tlb|TLB]] 플러시) 파괴로 서버가 뻗는다. 반드시 `pthread_create`를 통해 내부적으로 `clone(CLONE_VM | CLONE_FILES)`를 태워 동일한 메모리(힙, [[083_bss_segment|BSS]]) 공간을 공유하는 경량 [[092_thread_lwp|스레드]]를 띄워야 하며, 각 [[092_thread_lwp|스레드]]가 접근할 때 락([[510_lock|Lock]]) 경합이 발생하지 않도록 자원을 철저히 분리([[113_thread_local_storage|Thread Local Storage]]) 설계해야 한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **`fork()` 후 [[095_multithreading_benefits|다중 스레드]] 락킹([[213_locking_mechanism_concurrency_control|Locking]]) [[281_deadlock_definition|교착 상태]] ([[281_deadlock_definition|Deadlock]] 💥)**: 프로세스 내에 [[092_thread_lwp|스레드]]가 5개 핑핑 돌고 있는데, 갑자기 그중 한 [[092_thread_lwp|스레드]]가 `fork()`를 쳐버리는 변태적 행위. `fork()`는 호출한 그 [[092_thread_lwp|스레드]] 1개만 덜렁 복사해서 새 프로세스를 만든다. 만약 복사되기 전 다른 [[092_thread_lwp|스레드]]가 `malloc` 락([[510_lock|Lock]])을 잡고 있었다면, 새로 복사된 프로세스는 영원히 풀리지 않는 락을 가진 채 [[087_process_state_transition|생성]]되어 메모리를 잡자마자 영원한 데드락([[281_deadlock_definition|교착 상태]])에 빠져 타 죽는다. [[095_multithreading_benefits|다중 스레드]] 프로그램에서는 가급적 `fork()`를 금기시해야 한다.

- **📢 섹션 요약 비유**: [[561_container_based_deployment|컨테이너]] 기술에 쓰이는 `clone(CLONE_NEW*)`은 아바타를 만들 때 "너는 지금부터 나랑 아예 다른 우주(네트워크, PID)에 살고 있다고 착각해라"라고 최면을 걸어 가두는 투명한 유리 감옥과 같습니다.

---

## Ⅴ. 기대효과 및 결론

리눅스의 `clone()` 시스템 콜은 [[001_operating_system_purpose|운영체제]] 아키텍처의 우아한 추상화를 보여주는 궁극의 마스터피스다. 과거 "프로세스용 [[087_process_state_transition|생성]] 함수", "[[092_thread_lwp|스레드]]용 [[087_process_state_transition|생성]] 함수"를 따로 만들며 코드를 누더기로 유지하던 타 OS들과 달리, 리눅스는 모든 실행 흐름을 '[[150_task|Task]]'라는 하나의 구조체(`task_struct`)로 대통합하고, 오직 `clone()`의 '공유 [[186_character_stuffing_dle_stx_etx|플래그]](Flags)' 조합만으로 그 Task의 성격을 동적으로 변태 시키는 놀라운 메커니즘을 완성했다.

이 유연성 덕분에 리눅스는 무거운 DB 서버 프로세스부터 극도로 가벼운 실시간 [[092_thread_lwp|스레드]]까지 완벽히 소화하며 전 세계 서버와 안드로이드 시장을 평정했다. 나아가 이 `clone()`의 깃발 꽂기 철학([[061_namespace|Namespace]] [[186_character_stuffing_dle_stx_etx|플래그]])은 수십 년 뒤 [[063_docker_architecture|도커]]([[063_docker_architecture|Docker]])와 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]](K8s)라는 클라우드 [[561_container_based_deployment|컨테이너]] 대혁명의 물리적 뼈대(Engine)로 완벽하게 환생하여 현재까지 IT 제국을 지탱하고 있다.

- **📢 섹션 요약 비유**: `clone()` 시스템 콜은 요리사의 '만능 밀가루 반죽'입니다. 똑같은 반죽 하나에 이스트([[186_character_stuffing_dle_stx_etx|플래그]])를 어떻게 섞고 굽느냐에 따라 무거운 식빵(프로세스)이 되기도 하고, 가벼운 바게트([[092_thread_lwp|스레드]])가 되기도 하며, 속이 텅 빈 마카롱([[561_container_based_deployment|컨테이너]])이 되기도 하는 궁극의 리눅스 생태계 베이스 캠프입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **fork() / [[394_vfork|vfork]]()** | `clone()`에서 자원 공유 [[186_character_stuffing_dle_stx_etx|플래그]]를 다 끄거나 최소한만 켜서 호출하는 레거시 유닉스의 전통적 껍데기 [[014_api_posix|API]]. |
| **pthread_create()** | `clone()`에서 모든 자원을 공유하라고 100% 풀 악셀 [[186_character_stuffing_dle_stx_etx|플래그]]를 밟아 [[092_thread_lwp|스레드]]를 찍어내는 POSIX 표준 [[336_library_vs_framework|라이브러리]] 함수. |
| **task_struct** | 리눅스에서 프로세스든 [[092_thread_lwp|스레드]]든 차별 없이 똑같이 취급하여 관리하는 실행 흐름의 단일 제어 블록(PCB). |
| **[[061_namespace|Namespace]] ([[061_namespace|네임스페이스]])** | `CLONE_NEWPID` 같은 특수 격리 [[186_character_stuffing_dle_stx_etx|플래그]]를 통해, 물리 서버를 쪼개어 가짜 격리 공간을 만드는 [[063_docker_architecture|도커]]([[063_docker_architecture|Docker]]) [[561_container_based_deployment|컨테이너]]의 핵심 원리. |

### 📈 관련 키워드 및 발전 흐름도

```text
초기 Unix fork() 시스템 콜 / 부모의 모든 자원을 100% 딥 카피(Copy)하는 무거운 생성
    │
    ▼
Copy-On-Write (COW) 도입 / 읽기만 할 땐 부모 페이지를 가리키다, 쓸 때만 물리적 복사로 튜닝
    │
    ▼
경량 프로세스(LWP)와 스레드 요구 증대 / 잦은 Context Switch 오버헤드와 통신 랙 발생
    │
    ▼
리눅스 clone() 시스템 콜 대통합 / 자원의 '복사(Copy)' 대신 정밀한 플래그 기반 '공유(Share)' 튜닝 아키텍처 완성
    │
    ▼
Namespace 플래그 (CLONE_NEW*) 확장 / 도커(Docker) 컨테이너 격리의 핵심 심장으로 진화 폭발 🚀
```

### 👶 어린이를 위한 3줄 비유 설명

1. `clone()`은 새로운 로봇을 만들 때 "부모 로봇의 무기를 똑같이 복사해 줄까, 아니면 그냥 같이 쓰게 할까?"를 버튼으로 선택할 수 있는 **마법의 로봇 복사기**예요.
2. 복사 버튼을 누르면 완전히 똑같은 로봇이 아예 새집으로 이사 가고(`fork()`), 같이 [[289_cqrs_db|쓰기]] 버튼을 누르면 내 방앗간에서 망치와 톱을 같이 쓰는 쌍둥이 동생(`스레드`)이 태어나죠.
3. 리눅스는 이 [[158_instruction|명령어]] 딱 하나만 가지고도, 어떤 버튼([[186_character_stuffing_dle_stx_etx|플래그]])을 누르냐에 따라 세상의 모든 종류의 똑똑한 로봇들을 다 만들어낼 수 있는 엄청난 발명품이랍니다!
