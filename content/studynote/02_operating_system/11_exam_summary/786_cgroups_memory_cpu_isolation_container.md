+++
title = "786. cgroups 메모리, CPU 자원 제한 격리 컨테이너 (Cgroups Memory CPU Isolation Container)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ([Control Groups](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/))는 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 프로세스들을 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적인 그룹(방)으로 묶은 뒤, 각 방이 사용할 수 있는 **CPU, 메모리, 디스크 I/O, 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)의 상한선(Limit)과 우선순위를 철저하게 강제 통제하는 하드웨어 자원 배급 시스템**이다.
> 2. **가치**: 한 프로세스가 미쳐서 메모리를 다 퍼먹거나 CPU를 100% 점유해 시스템 전체가 죽는 '시끄러운 이웃(Noisy Neighbor)' 문제를 완벽하게 차단하며, 호스트 1대에 수천 개의 격리된 앱을 욱여넣을 수 있는 멀티테넌시([Multi-tenancy](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/))를 실현했다.
> 3. **융합**: [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/)([Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/))가 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에게 "너 혼자 방에 있는 거야"라는 '시야의 환상'을 준다면, cgroups는 "이 방에선 밥(자원)을 이것밖에 못 먹어"라는 '물리적 족쇄'를 채우는 기술로, 이 둘의 완벽한 융합이 곧 현대 클라우드를 지배하는 [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/))와 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s)의 정체성이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - 2006년 구글의 엔지니어들이 개발하여 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 편입시킨 시스템.
  - 프로세스들을 폴더(계층 트리)처럼 묶어두고, 각 폴더에 `cpu.max`, `memory.max` 같은 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 두어, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)와 메모리 관리자가 이 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)값을 절대 넘지 못하게 가차 없이 목을 조르는(Throttling) 메커니즘.

- **필요성(문제의식)**: 
  - 과거 리눅스는 자유민주주의(?)였다. 프로세스가 `malloc()`으로 메모리를 달라는 대로 줬다.
  - 학생 1명(특정 앱)이 도서관 자리를 혼자 100개 맡아버리거나, 식당 밥(CPU)을 혼자 다 먹어버려도 막을 규정이 없었다. 결국 다른 착한 학생(주요 데몬)들이 굶어 죽어 서버가 뻗었다([Kernel Panic](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/)).
  - **해결책**: "사용자나 프로세스를 그룹으로 묶고, 그룹별로 하루 식량(CPU 2코어, 램 4GB)을 할당하자. 식량을 다 먹으면 다음 날까지 절대 더 주지 말고 굶겨라(Throttling)!"

  - **기존 OS**: 무한 리필 뷔페. 뚱뚱한 손님 한 명이 작정하고 고기를 다 쓸어가면, 뒤에 온 손님 수십 명은 먹을 게 없어 불만을 터뜨리고 식당이 망한다.
  - **[cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ([컨트롤 그룹](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/))**: 철저한 고급 도시락 배급제. VIP석 손님(중요 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/))에겐 3단 고기 도시락(CPU 4코어)을 보장하고, 일반석 손님에겐 김밥 한 줄(CPU 0.5코어)만 준다. 뷔페 음식이 아무리 많이 남아도 자기 도시락을 다 먹은 사람은 더 먹을 수 없다. 

- **등장 배경**: 
  - 구글이 자신들의 거대한 데이터센터에서 수만 개의 검색 엔진 프로세스와 배치(Batch) 잡을 한 서버에 섞어 돌리려다 자원 충돌로 골머리를 앓자, 이를 해결하기 위해 직접 만들어 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 커뮤니티에 던진 기술이다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 네임스페이스와 cgroups의 상호보완성 (컨테이너 완성)     │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │   [ 리눅스 커널 (Host OS: 64 Core, 128GB RAM) ]                 │
  │                                                             │
  │   ┌── 컨테이너 A (Web Server) ──────────────────────────┐     │
  │   │  👁️ Namespace (환상): "나는 PID 1번이야! 나혼자 있네?"     │     │
  │   │  ⛓️ cgroups (족쇄):  CPU 2개, RAM 4GB 만 허용됨.          │     │
  │   │                                                         │     │
  │   │   (트래픽 폭주!)                                           │     │
  │   │   "CPU 10개 더 쓸래!" ──▶ ⛔ cgroups: "안돼! 넌 2개뿐이야!" │     │
  │   │   "RAM 5GB 줘!"      ──▶ ⚡ cgroups: "선 넘었네. 죽어라!"   │     │
  │   │                            (OOM Killer 발동 -> A 사망)    │     │
  │   └─────────────────────────────────────────────────────────┘     │
  │                                                             │
  │   ┌── 컨테이너 B (DB Server) ───────────────────────────┐     │
  │   │  👁️ Namespace: "나도 PID 1번이야!"                        │     │
  │   │  ⛓️ cgroups: CPU 16개, RAM 64GB 허용됨.                  │     │
  │   │                                                         │     │
  │   │   ▶ 결과: A가 미쳐 날뛰다가 스스로 굶어 죽어버렸지만,             │     │
  │   │           B는 A의 영향을 1%도 받지 않고 평화롭게 동작함! 🟢      │     │
  │   └─────────────────────────────────────────────────────────┘     │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "[도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/))는 그 자체가 기술이 아니라, 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 Namespace와 Cgroups를 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 편하게 포장한 예쁜 상자일 뿐이다"라는 말의 실체가 바로 이 그림이다. Namespace는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 파티션을 쳐서 눈을 가리는 기술이라면, Cgroups는 물리적인 자원의 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 밸브를 잠가버리는 기술이다. 두 개 중 하나라도 없으면 현대의 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) 생태계는 존재할 수 없다. A [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 해킹당해 암호화폐 채굴 스크립트가 돌더라도, cgroups가 CPU를 2개로 물리적으로 압박하므로 호스트 서버 전체가 다운되는 최악의 사태(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 확장)를 원천 차단한다.

- **📢 섹션 요약 비유**: Namespace가 죄수들의 눈에 가상현실(VR) 고글을 씌워서 각자 자기가 펜트하우스에 혼자 있다고 믿게 하는 거라면, Cgroups는 그 죄수들의 손발에 족쇄를 채워 정해진 반경(메모리/CPU 한도) 1미터 밖으로는 절대 나가지 못하게 만드는 가장 잔혹하고도 완벽한 통제 수단입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Cgroups의 핵심 컨트롤러 (Subsystems)

Cgroups는 단순히 "CPU, 램 제한" 하나로 끝나는 게 아니라 여러 개의 독립된 감시 부서(Subsystem)로 나뉘어 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 곳곳에 거미줄처럼 박혀있다.

| 컨트롤러 (Subsystem) | 통제 대상 자원 | 동작 방식 및 제한(Limit) 매커니즘 |
|:---|:---|:---|
| **cpu** | CPU 타임 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) | `cpu.max`: 100ms(주기) 중 20ms만 실행하게 허용. 다 쓰면 80ms 동안 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 강제로 재워버림 (Throttling). |
| **memory** | 물리 RAM + Swap | `memory.max`: 이 용량을 초과하여 `malloc/페이지 폴트`가 발생하면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 즉시 **Local [OOM Killer](/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/)**를 호출해 프로세스를 사살함. |
| **blkio / io** | 디스크 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) | `blkio.throttle.write_iops_device`: 특정 초당 입출력(IOPS)을 넘으면 디스크 드라이버가 I/O 처리를 보류(Delay) 시킴. |
| **pids** | [프로세스 생성](/knowledge-base/studynote/02_operating_system/02_process_thread/104_process_creation/) 개수 | `pids.max`: 100개로 제한 시, `fork` 폭탄 공격을 당해도 100개 이후엔 `fork()` 가 에러를 뱉으며 실패해 시스템 마비를 방어. |
| **cpuset** | 특정 물리 코어 번호 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 아예 물리 코어 0번, 1번에만 못 박아(Pinning) 다른 코어 침범을 원천 격리함. |

### CPU 압축성 자원(Compressible) vs RAM 비압축성 자원(Incompressible)

아키텍트는 이 두 자원의 물리적 성질 차이를 뼈저리게 이해해야 한다. cgroups가 목을 조를 때 나타나는 현상이 완전히 다르다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 Cgroups 한계 돌파 시: CPU vs RAM의 운명 차이             │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [ 1. CPU (압축성 자원) - Limit 1코어 설정 ]                         │
  │   앱이 코어 3개어치 연산을 미친 듯이 시도함!                              │
  │   ▶ Cgroups의 조치: "안돼, 기다려!" (Throttling 발동)                │
  │   ▶ 결과: 앱은 죽지 않음. 단지 엄청나게 느려져서 응답이 10배 지연됨.          │
  │   (사용자 불만은 생기지만, 서버는 살아서 꾸역꾸역 일은 계속함 = 고무줄)          │
  │                                                                   │
  │  [ 2. Memory (비압축성 자원) - Limit 1GB 설정 ]                      │
  │   앱이 메모리 1.1GB 할당(malloc & write)을 시도함!                    │
  │   ▶ Cgroups의 조치: "기다려준다고 해결될 문제가 아님. 사형!"              │
  │   ▶ 결과: 커널이 즉시 `SIGKILL (-9)` 발송. 앱 즉사 (OOMKilled) 💀     │
  │   (램은 쪼그려 앉을 수가 없음. 모자라면 누군가 죽어야만 공간이 나옴 = 유리잔)      │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이것이 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) 클러스터에서 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 자꾸 재시작(CrashLoopBackOff)하는 원인의 99%다. CPU는 시간을 쪼개서 뒤로 미룰 수 있으니 앱이 느려지기만(Throttled) 할 뿐 죽지 않는다. 하지만 메모리는 물질적인 공간이라 1바이트라도 선을 넘으면 유리가 깨지듯 시스템이 터진다. 따라서 [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 메모리 리밋에 도달하면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 자비 없이 프로세스의 목을 날린다. 인프라 엔지니어는 CPU 리밋은 타이트하게 쪼여서 오버커밋(돈 절약)을 노려도 되지만, 메모리 리밋은 절대적으로 여유(Slack)를 두어 방어적으로 설계해야 한다는 철칙이 여기서 나온다.

- **📢 섹션 요약 비유**: CPU 한도는 고무줄 바지라서 너무 많이 먹으면 배가 꽉 쪼여 숨쉬기 답답해지고 걷기 힘들어지지만([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하) 죽진 않습니다. 하지만 메모리 한도는 유리로 만든 바지라서 한도 이상으로 살이 찌는 순간 유리가 쨍그랑 깨지며 피를 흘리고 즉사([OOM Killed](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/))하게 됩니다.

---

## Ⅲ. 비교 및 연결

### [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v1 vs [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2 의 아키텍처적 패러다임 전환

리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 역사의 가장 큰 논쟁거리 중 하나였던 cgroups의 혼돈이 v2에서 정리되었다.

| 비교 항목 | [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v1 (혼돈의 시대) | [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2 (통일된 질서) |
|:---|:---|:---|
| **트리 구조** | 컨트롤러(CPU, RAM 등)마다 트리가 따로따로 존재함. (독립적) | **단일 계층 트리 (Unified Hierarchy)**. 하나의 방(Cgroup)에 들어가면 모든 자원 통제가 그 안에서 일어남. |
| **설계 맹점** | A 프로세스는 CPU 트리에선 그룹 1, RAM 트리에선 그룹 2에 속하는 등 족보가 심하게 꼬이고 관리 데몬이 미쳐버림. | 프로세스는 반드시 1개의 묶음에만 속함. (하위 부서 배정의 명확화) |
| **안전성 / 권한** | 루트(Root)만 제어 가능 | **Rootless [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)** 완벽 지원. 일반 유저도 안전하게 자원 분할 통제 가능. |
| **적용 시기** | 구형 [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) / K8s (CentOS 7 시대) | **현대 클라우드 표준** (Ubuntu 22.04+, RHEL 9+) |

### 과목 융합 관점

- **[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) (CFS [Bandwidth](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) Control)**: Cgroups의 CPU 리밋은 단순히 "너 코어 1개 써"가 아니다. 뒤에 엮여 있는 리눅스 CFS(Completely Fair Scheduler)의 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 제어 로직이 결합된다. `cpu.cfs_period_us=100000`(100ms 주기)와 `cpu.cfs_quota_us=20000`(20ms 할당)이라는 값이 세팅되면, 100ms마다 정확히 20ms만 CPU를 내어주고 나머지 80ms 동안은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 강제로 재워버리는 극도로 정밀한 시분할 독재를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 타이머 인터럽트와 결합해 수행한다.
- **[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 (OOM과 [Page](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Cache의 딜레마)**: [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 메모리 제한의 가장 억울한 죽음은 '[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시' 때문이다. 앱(Java)이 쓰는 실제 [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) 메모리는 1GB인데, 앱이 10GB짜리 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽었다 치자. 리눅스는 속도를 위해 남는 램을 캐시로 쓰므로 10GB 캐시가 Cgroup 메모리에 합산된다. Cgroup 리밋이 2GB라면? [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 "너 11GB나 썼네? 사형!"이라며 억울한 자바 앱을 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러로 죽여버린다. 최근 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 캐시를 먼저 비우고 그래도 모자랄 때만 죽이는 똑똑한 회수(Reclaim) 로직이 융합되었지만, 여전히 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O가 잦은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 메모리 한도 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에 목숨을 걸어야 한다.

- **📢 섹션 요약 비유**: [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v1은 회사에서 인사팀, 재무팀, 총무팀이 각각 자기 맘대로 직원 명부를 가지고 조직을 짜서(멀티 트리) 대혼란이 빚어진 상황입니다. [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2는 단일한 전사 통합 조직도(단일 트리) 하나만 만들어놓고 모든 부서가 그 조직도 룰을 따르게 만든 가장 깔끔하고 합리적인 개편입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 서버 튜닝

1. **시나리오 — [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) CPU Limit Throttling에 의한 10배 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 현상**: 노드에 CPU 코어가 16개나 남아도는데, CPU Limit을 `200m` (0.2 코어)로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)한 Node.js [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답 시간이 10ms에서 500ms로 엄청나게 튀는 현상이 터졌다. 앱 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)엔 에러도 없다.
   - **원인 분석**: [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) CPU [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 제어의 잔혹성이다. 100ms(주기) 중 20ms([Quota](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/))만 실행이 허가된다. 만약 21ms가 걸리는 연산이 들어오면? 앱은 20ms를 처리한 뒤, 다음 주기가 올 때까지 무려 **80ms 동안 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 의해 강제로 산소호흡기가 떼어지고 수면(Throttled)** 상태에 빠진다. 1ms 연산을 위해 80ms를 징벌적으로 기다리는 끔찍한 병목이다. 
   - **아키텍트 판단 (CPU Limit 제거 튜닝)**: 이런 단발성 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Tail [Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))에 민감한 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서는 아키텍트들이 과감한 결단을 내린다. K8s 매니페스트에서 **CPU `requests`만 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하고, CPU `limits`는 아예 지워버린다(Unbounded)**. 이렇게 하면 평소에는 자원을 보장받고, 서버 코어가 남으면 10코어든 20코어든 Limit 없이 땡겨써서 스로틀링(Throttling) 자체를 회피한다. 넷플릭스 등 글로벌 기업들의 기본 K8s 튜닝 공식이다.

2. **시나리오 — OOMKilled가 아닌 System [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 패닉 사태**: 메모리를 많이 먹는 DB [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에 Limit을 안 걸고 배포했다. 어느 날 DB가 미쳐서 노드의 물리 램 128GB를 다 먹어버렸다. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)만 죽은 게 아니라, 호스트 서버의 리눅스 전체가 패닉에 빠져 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 에이전트([Kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/))까지 죽고 노드가 뻗어버렸다.
   - **원인 분석**: Cgroups의 한계치(Limit)가 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)되지 않으면, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 호스트의 물리적 램을 끝까지 빨아먹는다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 시스템 전체 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 깨어났지만, 운 나쁘게 DB가 아닌 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 필수 데몬을 죽여버리거나 [스와핑](/knowledge-base/studynote/02_operating_system/06_memory_management/335_swapping/) 지옥에 빠져 호스트 OS가 붕괴된 것이다.
   - **아키텍트 판단 ([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) Guaranteed 클래스 강제)**: 인프라 아키텍트는 "Limit 없는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 서버에 터뜨린 시한폭탄"으로 규정해야 한다. [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 `LimitRange`나 `ResourceQuota` [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 강제로 박아 넣어, 개발자가 램 `limits`를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하지 않은 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)는 아예 클러스터에 배포되지 않도록 거부(Reject)하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진([OPA](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/) Gatekeeper)을 구축하여 하위 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 폭주가 상위 호스트 OS로 번지는 것을 물리적으로 절단해야 한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 Kubernetes 자원 통제(QoS)를 위한 Cgroups 매핑 트리      │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ K8s Pod 배포 시 Resource 설정이 Cgroups로 번역되는 과정 ]           │
  │                                                                   │
  │      개발자 설정          Cgroups 번역 (커널 파라미터)                 │
  │   -------------------------------------------------------------   │
  │   CPU requests: 1     ──▶ cpu.shares = 1024                       │
  │                           (바쁠 때 최소한 1코어 비율의 시간은 보장해 줌)      │
  │                                                                   │
  │   CPU limits: 2       ──▶ cpu.cfs_quota_us = 200000               │
  │                           (1주기 100ms당 최대 200ms만 허용. 초과시 기절)   │
  │                                                                   │
  │   Memory requests: 1G ──▶ Cgroups OOM Score 조정 (보호막 생성)          │
  │                           (램 부족할 때 이 파드를 제일 늦게 죽이도록 가점)      │
  │                                                                   │
  │   Memory limits: 2G   ──▶ memory.max = 2147483648                 │
  │                           (2GB 단 1바이트라도 초과 시 즉각 SIGKILL 사형!)    │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)의 화려한 YAML [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 사실 밑단에서 100% [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 파라미터 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 1:1 치환되는 '거대한 [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 관리 매크로'일 뿐이다. K8s의 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)([Kubelet](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/))는 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 뜨면 호스트 리눅스의 `/sys/fs/cgroup/` 폴더 밑에 방을 파고 저 값들을 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 텍스트로 적어 넣는다. 그러면 그 순간부터 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 자원 감시망이 동작하며 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 무자비하게 옥죈다. 인프라 엔지니어가 K8s 장애를 분석할 때 YAML만 보지 않고 호스트 서버에 접속해 직접 `/sys/fs/cgroup/`의 통계(stat) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 뜯어보는 이유가 이 날것의 진실을 마주하기 위해서다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **`cpuset` 과 `cpu.shares`의 무분별한 혼용**: "코어 0, 1번에만 묶어두고(`cpuset`), 거기서 CPU [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)도 제한하자(`cfs_quota`)"는 식의 과도한 중복 통제. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 0번 코어에 갇혀있는데, 0번 코어가 딴 일로 바쁘면 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 쿼터가 남아있어도 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 1번 코어로 도망가지 못하고 버벅댄다. 물리 코어를 통째로 내어주는 격리(cpuset, K8s Static CPU Manager)를 썼다면, [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 쓰로틀링(Limit) 족쇄는 시원하게 풀어주어야 캐시 효율과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 극대화를 이룰 수 있다.

- **📢 섹션 요약 비유**: 아이(프로세스)에게 "넌 오늘 하루 2시간만 TV(CPU) 봐!([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) Limit)"라고 정해줬으면 아이가 거실이든 안방이든 편한 곳에서 보게 놔둬야 합니다. 그런데 "넌 무조건 좁은 창고방(cpuset)에 들어가서, 딱 2시간만 봐!"라고 이중으로 족쇄를 채우면 아이는 스트레스를 받아 미쳐버립니다. 통제는 명확한 철학 한 가지로 밀고 나가야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 통제 부재 (기존 OS) | [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) Limits 강제 적용 ([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 ([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 확산 방지)**| 하나의 램 누수 앱이 서버 전체를 죽임 | 누수 난 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 1개만 Local OOM으로 죽음| 타 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 영향도(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/)) 0% 달성 |
| **정량 (자원 집적도 Density)**| 서버당 10개 앱 배포 시 상호 간섭 렉 폭발 | 자원 쪼개기로 서버 1대에 100개 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 배포 | 하드웨어 낭비([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)) 제거로 인프라 비용([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/)) 90% 극감 |
| **정성 ([QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 보장)** | 누구 하나 폭주하면 다 같이 버벅거림 (Best-effort) | VIP 앱은 항상 100% 자원 쾌적도 보장 | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 계약) 준수를 위한 결정론적 통제망 구축 |

### 미래 전망
- **[Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2와 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/)([BPF](/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/))의 절대적 융합 ([bpf](/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/)-cgroup)**: Cgroups의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 너무 딱딱하다는 한계를 깨기 위해, 특정 [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 방 안에서 일어나는 모든 디스크 I/O와 네트워크 패킷을 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 프로그램이 실시간 낚아채서(Hook) "이 방은 지금 디스크를 너무 많이 쓰니, 패킷을 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%만 버려버리자"라는 식의 초정밀 런타임 동적 스로틀링(Dynamic Throttling)이 구현되고 있다. 구글과 페이스북의 최신 인프라는 이미 이 단계로 넘어갔다.
- **Rootless [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)와 보안**: 과거엔 Cgroups를 건드리려면 루트(Root) 권한이 필수여서, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 엔진([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 데몬) 자체가 해킹당하면 서버가 다 털렸다. [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2부터는 일반 유저 권한으로도 하위 트리의 자원을 나눌 수 있게 되어, Rootless Docker나 Podman이 대세가 되며 클라우드 보안의 고질적 아킬레스건이 완벽히 해결되는 중이다.

### 참고 표준
- **Linux [Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [Documentation](/knowledge-base/studynote/04_software_engineering/06_software_architecture/378_software_documentation/) ([cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) v2)**: 2016년 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 4.5에 도입되어 기존 난잡했던 자원 계층을 단일화(Unified Hierarchy)하며 현대 시스템 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 오케스트레이션의 유일무이한 바이블이 된 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 스펙.
- **[OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) ([Open Container Initiative](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) Runtime Spec**: [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), containerd 등 어떤 런타임을 쓰든 K8s의 자원 명세(Limit)가 리눅스 [Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 파라미터 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 똑같이 번역되게끔 표준화한 글로벌 [컨테이너 런타임](/knowledge-base/studynote/02_operating_system/10_security/628_container_runtime_oci/) 약속.

[Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ([Control Groups](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/))는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 "공산주의적 낭만(모두 공평하게 써라)"을 버리고 "자본주의적 배급(가진 만큼만 써라)"이라는 차가운 현실을 받아들인 아키텍처적 선언이다. 이 잔혹한 통제가 없었다면 수만 명의 개발자가 만든 각기 다른 질의 코드가 하나의 클라우드 서버 위에서 얽혀 매일같이 시스템을 폭파시켰을 것이다. Cgroups는 프로세스들의 이기심과 탐욕을 완벽한 격리벽으로 짓누름으로써, 21세기 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))라는 수천 개의 톱니바퀴가 물려 돌아가는 거대한 기계 장치의 태엽을 안전하게 굴리고 있다.

- **📢 섹션 요약 비유**: 수백 명의 아이(프로세스)들이 뛰노는 거대한 놀이방(서버)에서, 선생님([Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/))이 아이들마다 "넌 이 선 밖으로 나오면 안 돼(격리)", "넌 블록 5개까지만 만져(Limit)"라고 명확한 룰을 강제하지 않으면 놀이방은 10분 만에 아수라장이 되어 폐쇄됩니다. 이 엄격한 규율 덕분에 수천 개의 놀이방이 평화롭게 돌아가는 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [하이퍼스레딩](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/199_interrupt_scheduling/) 물리 코어 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 코어 분할 구조 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [클론](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/)([clone](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/)) 시스템 콜 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 공유 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 안드로이드 LMK ([Low Memory Killer](/knowledge-base/studynote/02_operating_system/11_exam_summary/787_android_lmk_low_memory_killer/)) 작동 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| iOS 앱 [샌드박싱](/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/) 구조 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[클론(clone) 시스템 콜 스레드 공유 플래그]
    │
    ▼
[cgroups 메모리, CPU 자원 제한 격리 컨테이너 (Cgroups Memory CPU Isolation Container)]
    │
    ├──▶ [안드로이드 LMK (Low Memory Killer) 작동]
    └──▶ [iOS 앱 샌드박싱 구조]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 뷔페식당(리눅스)에서 예전에는 뚱뚱한 욕심쟁이 손님(버그 난 앱) 한 명이 혼자 고기(CPU/RAM)를 다 휩쓸어가서 다른 손님들이 굶어 죽고 식당이 망했어요.
2. 그래서 똑똑한 식당 주인이 '씨그룹([Cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/))'이라는 규칙을 만들었어요. "철수는 고기 2접시, 영희는 고기 5접시까지만 허용!"이라고 표를 딱 나눠준 거죠.
3. 만약 철수가 몰래 3접시째 먹으려 하면, 보안 요원이 나타나 철수 입을 꽉 막아버리거나(CPU [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)), 아예 식당 밖으로 쫓아내 버려요([OOM Killed](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/110_oom_out_of_memory_killed_kubernetes_limits/)). 덕분에 식당 평화가 완벽히 유지된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 786 / 800

← **이전**: [785. 클론(clone) 시스템 콜 스레드 공유 플래그](/knowledge-base/studynote/02_operating_system/11_exam_summary/785_clone_system_call_thread_sharing/)
**다음**: [787. 안드로이드 LMK (Low Memory Killer) 작동](/knowledge-base/studynote/02_operating_system/11_exam_summary/787_android_lmk_low_memory_killer/) →

---
