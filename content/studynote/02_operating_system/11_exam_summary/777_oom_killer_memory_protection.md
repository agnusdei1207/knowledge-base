+++
title = "777. OOM 킬러 메모리 보호 정책 (OOM Killer Memory Protection)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 ([Out-Of-Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/) Killer)는 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 메모리(RAM + Swap) 고갈로 인한 시스템 전체의 동반 자살([Kernel Panic](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/))을 막기 위해 발동시키는 최후의 자위권으로, <strong>가장 쓸모없거나 죄질이 나쁜(메모리를 비정상적으로 많이 먹는) 프로세스 하나를 사형시켜 메모리 숨통을 틔우는 저승사자 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>이다.
> 2. **가치**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 '오버커밋(Overcommit, 뻥튀기 대출)'이라는 도박적인 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 할당([Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Allocation) 최적화를 마음껏 사용할 수 있게 든든한 뒷배가 되어주며, 극한의 부하 상황에서도 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 시스템 핵심 데몬이 살아남도록 방어선을 구축한다.
> 3. **융합**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) 시대가 오면서 [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/)([컨트롤 그룹](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/)) 기반의 메모리 Limit 통제와 융합되어, 특정 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 하나가 죽더라도 호스트 OS나 옆의 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 완벽하게 보호하는 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 격리([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))의 최후 방어선으로 진화했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - 리눅스 시스템에서 물리적 메모리(RAM)와 스왑(Swap) 공간이 100% 꽉 찼을 때, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 메모리 관리자([VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Subsystem)가 호출하는 응급 프로세스 강제 종료 루틴(`out_of_memory()`)이다.
  - 내부 점수([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) Score)를 계산하여 가장 만만한 타겟(Victim)에게 `SIGKILL` 신호를 쏴서 가차 없이 즉사시킨다.

- **필요성 (왜 그냥 메모리 할당을 실패(Fail)시키지 않고 죽일까?)**: 
  - 리눅스의 철학 중 하나인 **메모리 오버커밋(Overcommit)** 때문이다. 램이 10GB인데 앱들이 `malloc()`으로 총 15GB를 달라고 해도 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 "콜!"을 외친다(뻥대출). 어차피 앱들이 그 15GB를 당장 다 쓰진 않을 거란 얄팍한 믿음 때문이다.
  - 그런데 앱들이 갑자기 진짜로 15GB에 데이터를 꽉 채워버리기 시작하면 물리 램이 파산([Out of memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))한다. 이때는 이미 `malloc`은 성공한 상태라 실패(Fail)를 던질 수도 없다.
  - **해결책**: "은행(RAM)에 뱅크런이 터져 파산하게 생겼다! 은행이 무너지면 국가(OS)가 망하니까, 대출금을 제일 많이 당겨 쓴 고객(프로세스) 하나의 목을 쳐서 그 돈(메모리)을 강제로 회수해라!"

  - <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 발생</strong>: 정원이 10명인 작은 구명보트(서버)에 15명의 사람(프로세스)이 탔다. 평소엔 다들 앉아있어서(메모리 미사용) 배가 떴는데, 폭풍이 치자 다들 살겠다고 일어나서 날뛰니 보트가 물에 잠기며 가라앉기 일보 직전이다.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 킬러 출동</strong>: 선장([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))은 보트 전체가 침몰하는 걸 막기 위해 총을 빼 들고 "가장 뚱뚱하고(메모리를 많이 먹고) 필요 없는 놈 한 명을 물 밖으로 던져라!"라고 사형 집행(Kill)을 명하는 극단적인 구명조끼 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.

- **등장 배경**: 
  - 메모리 용량이 부족했던 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 리눅스 시절, 효율적인 램 사용을 위해 도입된 '[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 할당([Demand Paging](/knowledge-base/studynote/02_operating_system/04_synchronization/255_demand_paging/)) 및 오버커밋'의 부작용을 막기 위한 불가피한 최후의 안전장치로 설계되었다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 메모리 오버커밋 파산과 OOM 킬러 발동 메커니즘           │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ 1. 오버커밋(Overcommit) 뻥대출의 평화로운 시기 ]                 │
  │  물리 RAM: 10GB                                              │
  │   - App A `malloc(5GB)` 요청 -> 커널: "OK!" (실제 사용 1GB)    │
  │   - App B `malloc(8GB)` 요청 -> 커널: "OK!" (실제 사용 2GB)    │
  │   - App C `malloc(5GB)` 요청 -> 커널: "OK!" (실제 사용 1GB)    │
  │   ※ 장부상 18GB 대출이지만, 실제 램은 4GB만 써서 평화로움.             │
  │                                                             │
  │  [ 2. 뱅크런(실제 쓰기 폭주) 발생! ]                              │
  │   - App B가 갑자기 8GB를 꽉꽉 채워 쓰기(Write) 시작함 (페이지 폴트)     │
  │   - 남은 물리 RAM 0바이트, Swap 공간 0바이트 도달!                  │
  │   - 시스템 멈춤(Hang) 발생. 마우스 클릭도 안 먹힘.                    │
  │                                                             │
  │  [ 3. OOM Killer 사형 집행 ⚡ ]                                 │
  │   - 커널: "더 이상 줄 메모리가 없다. 킬러 호출!"                      │
  │   - 점수 계산: App B가 제일 뚱뚱하군. (OOM Score 1위)               │
  │   - OOM Killer가 App B에게 강제 사형 선고 (`SIGKILL -9` 발송)      │
  │   - App B는 즉사하고 8GB 메모리를 허공에 툭 떨어뜨림.                 │
  │   - 시스템이 8GB를 줍고 다시 정상적으로 숨을 쉬기 시작함. 🚀             │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 메커니즘은 리눅스 엔지니어를 가장 고통스럽게 만드는 딜레마다. 개발자는 아무 잘못이 없다(단지 `malloc`을 했을 뿐이다). 그러나 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 사기극(오버커밋)이 한계에 부딪혔을 때, 그 책임과 죽음은 고스란히 응용 프로그램(App B)이 뒤집어쓴다. [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러는 자비가 없어서 프로그램이 데이터를 파일에 저장할 시간조차 주지 않고 하드웨어 레벨에서 목을 쳐버린다. [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(dmesg)를 보면 `Out of memory: Kill process 1234 (java) score 850 or sacrifice child`라는 섬뜩한 문구가 남으며 서버가 겨우 생명줄을 이어가게 된다.

- **📢 섹션 요약 비유**: 항공사가 100석짜리 비행기에 120석의 표를 팔았는데(오버커밋), 공교롭게도 120명이 전부 공항에 와버렸습니다. 비행기를 못 띄울 위기에 처하자, 기장([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러)이 가장 뚱뚱하고 늦게 온 승객(메모리 과점유 프로세스)을 멱살 잡아 비행기 밖으로 내던져버리고 정시 이륙을 강행하는 무자비한 생존술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 사형수 선정 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) Score Calculation)

[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 아무나 죽이는 것은 아니다. 매우 정교하고 억울하지 않은(?) 점수 체계(`/proc/[pid]/oom_score`)를 가지고 타겟을 계산한다. 이 점수가 높은 녀석이 죽는다.

| 점수 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) (Badness Score) | 계산 로직 및 철학 | 비고 |
|:---|:---|:---|
| **메모리 점유량 (+)** | RAM과 스왑을 가장 많이 처먹은 놈이 1순위. | 죽였을 때 회수할 수 있는 메모리가 커야 한 방에 해결되니까! |
| **권한 레벨 (Root) (-)** | Root 권한으로 도는 핵심 데몬(sshd 등)은 점수를 깎아줌. | 서버 접속용 SSH가 죽으면 원격 관리가 끊기니까 봐줌. |
| **실행 시간 및 우선순위 (-)**| 오래 살아남은 장기 실행 프로세스(DB 등)는 점수를 깎아줌. | 이제 막 태어난 놈(버그로 폭주 중일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 높음)을 죽이는 게 안전하니까. |
| <strong><code>oom_score_adj</code> (수동 조작)</strong>| 관리자가 프로세스별로 -1000 ~ +1000 점수를 수동으로 더하거나 뺌. | "이 DB 서버는 죽어도 죽이지 마!"라고 사람이 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 면제권(-1000)을 주는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/). |

### [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/)) 융합의 국지적 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러

과거 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러는 호스트 전체 램이 바닥나야 터지는 '국가적 재난'이었다. 하지만 [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/))와 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) 시대가 오면서, [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/)([Control Groups](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/))에 의한 <strong>국지적(Local) <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 킬러</strong> 메커니즘이 더 자주 발동된다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 호스트 OOM vs 컨테이너(cgroups) OOM 의 차이 공간      │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 호스트 전체 램: 64GB ]                                            │
  │                                                                   │
  │   ┌── Cgroup A (웹 서버) ──┐        ┌── Cgroup B (DB 서버) ──┐      │
  │   │ Limit: 2GB (상한선)    │        │ Limit: 제한 없음         │      │
  │   │ 현재 사용량: 1.9GB       │        │ 현재 사용량: 20GB        │      │
  │   │                      │        │                      │      │
  │   │ 🚨 웹이 2GB를 넘기려 함! │        │ 🟢 램 여유 넘침 (안전함)   │      │
  │   │ -> [ Local OOM 발동 ]  │        │                      │      │
  │   │ 웹 컨테이너만 칼같이 Kill!│        │ DB는 전혀 영향 안 받음!   │      │
  │   └──────────────────────┘        └──────────────────────┘      │
  │                                                                   │
  │   ※ 핵심: 호스트 전체 램이 40GB나 남아돌아도, Cgroup A가 자기 자신에게       │
  │          할당된 리밋(Limit) 2GB를 뚫는 순간 해당 박스 안에서만 OOM 킬러가  │
  │          터져 그 컨테이너를 가차 없이 암살한다. (격리의 미학)                 │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이것이 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)를 다루는 개발자들이 맨날 보는 `OOMKilled` 에러의 실체다. 물리 램이 남아돌아도 죽는다. 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 메모리 컨트롤러(memcg)는 각 Cgroup 마다 독립적인 장부를 쓴다. A 그룹이 선을 넘으면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 전체 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 아니라, 해당 Cgroup 내부 명단만 모아놓고 자체 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 점수를 매겨 그 방 안의 죄수 하나만 죽이고 상황을 종료한다. 이것이 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서 한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/)(Leak)가 전체 서버 노드를 뻗게 만드는 참사를 막는 가장 강력한 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([Bulkhead](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/))이다.

- **📢 섹션 요약 비유**: 나라 전체(호스트)에 식량이 넘쳐나도, A 감방([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)) 수감자들에게 "하루 배급량은 빵 2개(Limit 2GB)다"라고 선언했으면, A 감방 수감자가 빵 3개를 먹으려 드는 순간 방 밖의 식량 창고 크기와 무관하게 그 방 안에서만 무자비한 굶어 죽음(Local [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))이 발생하는 철저한 배급 통제 시스템입니다.

---

## Ⅲ. 비교 및 연결

### 메모리 오버커밋(Overcommit) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)의 3가지 딜레마

[OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 언제 깨어날지는 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터 `vm.overcommit_memory` [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 100% 결정한다. (아키텍트의 성향 차이).

| [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)값 (sysctl) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 이름 및 동작 방식 | 어떤 아키텍처에 적합한가? (장단점) |
|:---:|:---|:---|
| **0** (디폴트) | <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/236_a_star_heuristic_minimax_mcts_monte_carlo/">Heuristic</a> (눈치껏 대출)</strong>: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 대충 봐서 너무 터무니없는 뻥튀기 요구만 거절하고 적당히는 허락해 줌. | **일반적인 웹 서버**. 램 낭비 없이 꽉꽉 채워 쓰지만 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 위험이 항상 잔존함. |
| **1** | **Always (묻지마 무한 대출)**: 램이 1GB인데 100TB를 달라고 뻥을 쳐도 무조건 OK를 줌. | <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a>, 과학 연산</strong>. 엄청난 크기의 희소 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)(Sparse [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/))을 선언만 해두고 일부만 쓰는 앱에 최고. 하지만 진짜로 다 쓰면 시스템 1초 만에 멸망. |
| **2** | **Never (대출 절대 불가)**: 물리 램 + 스왑을 합친 철저한 계산하에 남는 돈만큼만 딱 빌려줌 ([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 실업자 됨). | **PostgreSQL, 보안 결제 시스템**. [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 죽이는 꼴을 절대 볼 수 없는 하드코어 DB 서버용. 단점은 램을 절반도 안 쓰면서 꽉 찼다고 에러를 내서 RAM 낭비가 끔찍함. |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> (Swap <a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a>)</strong>: [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 너무 빨리 튀어나오는 걸 막기 위한 최후의 완충 지대가 Swap(디스크를 램처럼 쓰는 것)이다. 하지만 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 등 현대 클라우드에서는 Swap을 아예 꺼버린다(`swapoff`). 디스크 스와핑이 돌기 시작하면 서버가 죽진 않아도 레이턴시가 수천 배 느려지는 '산 채로 굳어버린 좀비 서버'가 되기 때문이다. 차라리 깔끔하게 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러로 빨리 쳐 죽이고 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))를 옆 서버에 새 램으로 깨끗하게 재시작(Restart) 시키는 게(Fail-fast 철학) 클라우드 아키텍처에 더 이득이기 때문이다.
- <strong>안드로이드 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> (LMK, <a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/787_android_lmk_low_memory_killer/">Low Memory Killer</a>)</strong>: 스마트폰은 램이 작아서 데스크톱보다 훨씬 가혹한 메모리 관리가 필요하다. 안드로이드 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에는 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러보다 더 적극적인 LMK([Low Memory Killer](/knowledge-base/studynote/02_operating_system/11_exam_summary/787_android_lmk_low_memory_killer/))가 내장되어 있다. 화면에 안 보이는 백그라운드 앱(카톡, 게임)들을 그룹별로 묶어두고, 램이 부족해지려 하면 가장 안 쓴 앱부터 수시로 모가지를 쳐서 날려버린다. (우리가 폰에서 홈키를 누르고 나갔다가 다시 게임을 켜면 처음부터 로딩되는 이유가 바로 이 녀석에게 죽었기 때문이다).

- **📢 섹션 요약 비유**: 스왑(Swap) 메모리가 "파산 직전에 사채(느린 디스크)를 끌어다 쓰며 고통스럽게 연명하는 것"이라면, 클라우드의 Swap-off와 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 조합은 "돈이 없으면 깔끔하게 즉시 파산 선고(Kill)를 내리고 법정 관리([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 재시작)를 받아 깨끗한 새 회사로 환생"하는 자본주의적 패러다임 전환입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 트러블슈팅

1. <strong>시나리오 — AWS EC2 상의 MySQL <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> 의문사</strong>: 트래픽이 몰리자 뜬금없이 크고 무거운 MySQL 데몬이 푹푹 죽어버리며 사이트가 마비된다. `tail -f /var/log/messages`를 쳐보니 `Out of memory: Kill process (mysqld)`가 찍혀있다.
   - **원인 분석**: 웹 프론트나 캐시 앱들이 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/)(Leak)를 일으켜 램을 거덜 냈다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 깨어났는데, 방금 누수를 일으킨 잡다한 앱들을 죽이려다 보니 "이 엄청난 거구(MySQL) 하나만 죽이면 메모리 20GB를 한 방에 회수할 수 있겠군!" 이라며 엉뚱하고 가장 중요한 DB의 목을 날려버린 끔찍한 오발 사고다. (가장 무거운 놈을 치는 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러의 맹점).
   - <strong>아키텍트 판단 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 쉴드 부여)</strong>: 중요한 인프라 데몬은 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러의 칼날에서 강제 면책특권을 줘야 한다. MySQL 프로세스의 PID를 찾아 `/proc/[pid]/oom_score_adj` 파일에 `-1000` 이라는 절대 방어 값을 때려 넣는다(또는 Systemd [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에 `OOMScoreAdjust=-1000`). 이렇게 하면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 "이놈은 죽여도 점수가 낮으니, 쟤 말고 찌꺼기 앱 10개를 쳐 죽이자"라고 판단을 돌려 DB의 억울한 죽음을 막아낸다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/">쿠버네티스</a> Java Spring Boot 앱의 무한 OOMKilled 핑퐁</strong>: 노드 램은 64GB고, [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 제한(Limit)을 2GB로 줬다. 그런데 자바 앱이 켜지자마자 트래픽도 없는데 `OOMKilled`를 맞고 죽고 재시작하기를 하루 종일 반복한다 (CrashLoopBackOff).
   - **원인 분석**: JVM(Java [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))의 오래된 버그([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 인지 부족) 때문이다. JVM은 자신이 2GB짜리 좁은 Cgroup 감방 안에 있다는 걸 모르고, 호스트 전체의 64GB 램을 보고 "오! 램이 64기가나 있네? 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 메모리를 기본 세팅인 4분의 1(16GB)로 잡아야지!"라며 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 메모리 공간을 거대하게 선언하며 펼친다. 이 순간 Cgroup 리밋(2GB)을 돌파하여 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 Local [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 JVM의 뒤통수를 쳐버린다.
   - <strong>아키텍트 판단 (JVM <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 인지 옵션)</strong>: 가상 공간과 물리 공간의 인지 부조화를 잡아줘야 한다. JVM 옵션에 `-XX:+UseContainerSupport`와 `-XX:MaxRAMPercentage=75`를 강제로 먹여서, JVM이 호스트가 아닌 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에 할당된 2GB만을 자신의 우주로 인식하도록 교정해야 한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 OOM (Out Of Memory) 장애 대응 아키텍트 결정 트리           │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 서버에서 프로세스가 아무 에러 로그 없이 실종되었다! ]                     │
  │                │                                                  │
  │                ▼                                                  │
  │      `dmesg -T | grep -i oom` 명령어로 커널 메시지를 깐다.                 │
  │          ├─ 안 나옴 ──▶ OOM 킬러 아님. 앱 자체 버그나 Segfault임.          │
  │          │                                                        │
  │          └─ 나옴! ──▶ 🚨 [ OOM Killer 사살 로그 발견! 범인 색출 시작 ]      │
  │                │                                                  │
  │                ▼ [아키텍트의 3단계 복구 설계]                            │
  │      1. 희생자가 진짜 범인인가? (억울한 죽음 방어)                           │
  │         - 중요 DB면 `oom_score_adj=-1000` 으로 면책특권 부여.             │
  │      2. 진짜 범인(메모리 누수 앱)이 누구인가?                               │
  │         - 커널 파라미터 `vm.panic_on_oom=1` 켜는 건 미친 짓(전체 죽음).      │
  │         - 앱 코드를 분석해 Malloc 해제 누락(Leak) 로직을 패치해야 함.         │
  │      3. 구조적 해결 (Swap vs Scale-out)                               │
  │         - 영세기업: Swap 파일(가상메모리)을 열어 디스크 속도로 고통받으며 연명.│
  │         - 클라우드: HPA 연동하여 램 70% 찰 때 서버 대수를 늘려버림(Scale Out)│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "프로세스가 아무 유언(Exception Log)도 없이 갑자기 사라졌어요!" 백엔드 개발자들의 가장 흔한 비명이다. 프로세스는 절대 스스로 흔적 없이 사라지지 않는다. `try-catch`로 잡히지 않는 유일한 죽음은 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 단에서 쏘는 `SIGKILL (-9)` 뿐이며, 그 배후에는 100% [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 있다. 아키텍트는 죽은 놈(Victim)을 살려내는 데 집착하지 말고, 왜 물리 램이 끝까지 차올랐는지 전체 시스템의 [메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/)(Pool) 파이프라인을 점검하는 거시적 안목을 가져야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><code>vm.overcommit_memory=2</code> (Never) <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>의 무지성 남용</strong>: "[OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 우리 소중한 앱을 죽이는 게 꼴 보기 싫다"며 오버커밋(뻥대출)을 아예 금지시켜 버리는 세팅. 이렇게 하면 램이 절반 이상 텅텅 비어있는데도, 자바나 파이썬처럼 앱을 켤 때 덩치 큰 가상 주소부터 냅다 잡고 보는 앱들이 `malloc()` 에러를 맞고 실행조차 되지 못한다(Cannot allocate memory). [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러를 피하려다가 메모리 낭비율이 50%를 넘어가는 빈대 잡다 초가삼간 다 태우는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다.

- **📢 섹션 요약 비유**: 자동차 에어백([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러)이 터지면 코가 다치고 짜증 난다고 해서, 아예 차에 에어백을 빼버리고 브레이크(Never Overcommit)만 미친 듯이 밟고 다니면 차가 아예 앞으로 가질 못하는(메모리 할당 불가) 멍청한 최적화와 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [OOM Killer](/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/) 기능 부재 시 | [OOM Killer](/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/) + [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (시스템 생존율)**| RAM 100% 도달 시 OS 전체 [커널 패닉](/knowledge-base/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/)(정지) | 단 1개의 프로세스만 죽이고 즉시 램 확보 | 시스템 전체 장애(Downtime) [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 99.9% [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) |
| **정량 (메모리 밀도)** | 물리 램 용량 이상으로 앱을 실행할 수 없음 | 오버커밋 허용으로 물리 램의 150% 가동 | 하드웨어 투자(RAM 구매) 대비 서버 집적도 극대화 |
| **정성 (운영 통제력)** | [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) 발생 시 원인 파악 전 서버 강제 재부팅 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(dmesg)에 정확한 범인과 메모리 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 기록 | 장애 원인 분석(RCA) 및 트러블슈팅의 정확도 향상 |

### 미래 전망
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 기반 선제적 사용자 공간 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 데몬 (oomd, earlyoom)</strong>: 리눅스 기본 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러는 너무 늦게 터진다. 시스템이 이미 렉이 걸려 마우스도 안 움직이는 마의 10초를 겪고 나서야 칼을 빼 든다. 이 치명적인 멈춤 현상을 극복하기 위해 페이스북(Meta) 등은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 킬러가 돌기 훨씬 전(램 90% 지점)에, 유저 스페이스에서 가벼운 [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 데몬(systemd-oomd)이 미리 부드럽게 쓰레기 프로세스들을 죽여 나가는 '선제적(Proactive) 킬러' 체계로 데스크톱과 서버의 방어막을 전면 교체하고 있다.
- **메모리 압박 알림 (PSI, Pressure Stall Information)**: 램이 몇 GB 남았냐는 수치보다 중요한 것은 "메모리가 없어서 디스크 스왑을 하느라 CPU가 낭비된 시간이 얼마인가"이다. 최신 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 PSI 지표를 도입하여, 메모리 결핍으로 인해 프로세스가 받은 고통(Delay)을 마이크로초 단위로 정밀하게 추적하고, 한계치에 다다르면 K8s가 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 옆 노드로 안전하게 대피(Eviction)시키는 지능형 짐 싸기 아키텍처로 진화하고 있다.

### 참고 표준
- <strong>Linux <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">Kernel</a> <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a> Subsystem</strong>: 리눅스 토발즈 및 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 커뮤니티가 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(오버커밋)과 안정성([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))"의 피 터지는 트레이드오프를 수십 년간 튜닝해 온 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 가장 거대한 심장부 철학.
- <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/">Cgroups</a> v2 (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/">Control Groups</a>)</strong>: 시스템 전체 OOM에서 탈피하여 특정 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 트리의 메모리 족쇄([Memory Limit](/knowledge-base/studynote/02_operating_system/07_virtual_memory/439_cgroups_memory_limit/)/[OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))를 완벽히 하드웨어적으로 격리해 주는 클라우드 시대 리눅스 자원 통제 표준.

[OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 보여주는 가장 기계적이고 잔혹한 '트롤리 딜레마(Trolley Problem)'의 해결책이다. 브레이크가 고장 난 기차(메모리 고갈)가 다가올 때, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 100명이 탄 기차 전체(OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))를 구하기 위해 철로 위에서 가장 뚱뚱한 사람 한 명(빅 프로세스)을 쳐버리는 스위치를 일말의 망설임 없이 당긴다. 프로그래머는 이 잔혹한 킬러를 원망할 것이 아니라, 그 킬러 덕분에 자신이 짠 허술한 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) 코드에도 불구하고 서버 전체가 뻗지 않고 오늘 하루를 무사히 넘길 수 있었음에 감사해야 한다.

- **📢 섹션 요약 비유**: 우주선에 산소(메모리)가 고갈되어 모두가 죽게 생겼을 때, 선장([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))이 가장 많은 산소를 마시며 누워있는 환자 한 명(가장 무거운 프로세스)을 강제로 우주 밖으로 던져버림([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) Kill)으로써 남은 승무원 전원의 목숨과 우주선 본체(OS)를 살려내는 피도 눈물도 없는 생존 매뉴얼입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 크기 제한 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) OS [자원 풀링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/638_resource_pooling_cxl/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [프로세스 친화성](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/) ([Affinity](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/)) 스케줄링 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [부하 균등화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/) ([Load Balancing](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/196_hard_soft_real_time/)) 큐 이주 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[클라우드 컴퓨팅 OS 자원 풀링]
    │
    ▼
[OOM 킬러 메모리 보호 정책 (OOM Killer Memory Protection)]
    │
    ├──▶ [프로세스 친화성 (Affinity) 스케줄링]
    └──▶ [부하 균등화 (Load Balancing) 큐 이주]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 배가 바다를 항해하는데, 배가 견딜 수 있는 무게(메모리)보다 사람들이 너무 많은 짐을 들고 타서 배가 가라앉으려고 해요! (메모리 고갈)
2. 배가 아예 침몰하면 다 죽기 때문에, 선장님([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))은 가장 크고 무거운 쓸모없는 짐을 가진 사람(프로세스) 한 명을 강제로 골라요.
3. 그리고 그 사람을 물 밖으로 던져버린답니다([OOM Killer](/knowledge-base/studynote/02_operating_system/07_virtual_memory/425_oom_killer_score/) 발동). 불쌍하긴 하지만, 그 한 명 덕분에 배 전체와 나머지 사람들은 무사히 항해를 계속할 수 있는 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 777 / 800

← **이전**: [776. 클라우드 컴퓨팅 OS 자원 풀링 (Cloud Computing Resource Pooling)](/knowledge-base/studynote/02_operating_system/11_exam_summary/776_cloud_computing_resource_pooling/)
**다음**: [778. 프로세스 친화성 (Affinity) 스케줄링](/knowledge-base/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/) →

---
