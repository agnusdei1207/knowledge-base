---
title: "726. Working Set Memory Locality"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/))은 프로세스가 실행되는 특정 시간 동안 <strong>"반드시 물리 메모리(RAM)에 올라와 있어야만 <a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 없이 원활하게 돌아갈 수 있는 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a>들의 집합"</strong>을 의미하는 피터 데닝(Peter Denning)의 핵심 개념이다.
> 2. **메커니즘 (지역성)**: 프로그램은 시간적/[공간적 지역성](/studynote/01_computer_architecture/06_memory_hierarchy_cache/248_spatial_locality/)(Locality) 때문에 한 번에 모든 메모리를 골고루 쓰지 않고 특정 순간에는 특정 영역(예: `for` 문 내부)만 집중적으로 사용한다. OS는 이 '집중적으로 쓰는 영역([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))'의 크기를 실시간으로 계산하여 그만큼의 프레임을 프로세스에게 보장해 준다.
> 3. **가치**: [워킹 셋 모델](/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)은 [다중 프로그래밍](/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) 환경에서 <strong><a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a>(<a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">Thrashing</a>)을 원천 차단</strong>하는 수학적 방어선이다. OS는 모든 프로세스의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 크기의 합이 물리 메모리를 초과하면, 프로세스 하나를 통째로 쫓아내어(Swap-out) 남은 프로세스들의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 지켜낸다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - **지역성 (Locality)**: 프로세스가 기억 장치 내의 정보를 균일하게 접근하지 않고, 특정 순간에 특정 영역만 집중적으로 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 특성.
  - **[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) ($WS$)**: 현재 시점 $t$에서 과거 $\Delta$(Delta, [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/)) 시간 동안 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)된 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들의 집합.

- <strong>필요성 (<a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a>의 비극과 맹목적 할당의 한계)</strong>:
  - 과거 OS는 남는 램이 있으면 무작정 프로세스를 더 띄웠다([다중 프로그래밍](/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) 증가).
  - 프로세스들에게 메모리를 공평하게 10장씩 나눠줬는데, 어떤 프로그램은 5장만 있어도 잘 돌지만(작은 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)), 어떤 프로그램은 최소 15장이 있어야 도는(큰 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)) 애였다. 15장 필요한 애한테 10장만 주니 매초 [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Fault가 터져 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)으로 시스템이 뻗어버렸다.
  - **해결책**: "공평하게 주는 게 중요한 게 아니다. 각 프로세스가 <strong>'최소한 숨을 쉬기 위해 필요한 산소통의 크기(<a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>)'</strong>를 실시간으로 재서, 그만큼은 무조건 보장해 주고, 그게 안 되면 아예 프로세스를 죽이거나 쫓아내자!"

  - <strong><a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a></strong>: 요리사가 지금 당장 '된장찌개'를 끓이기 위해 도마(RAM) 위에 반드시 올려놔야 하는 <strong>핵심 재료들(된장, 두부, 양파)</strong>의 묶음.
  - <strong><a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a></strong>: 도마가 너무 좁아서 된장을 올리려고 두부를 바닥(디스크)에 내려놓고, 두부를 썰려고 양파를 바닥에 내려놓는 짓을 반복하느라 요리를 아예 못 하는 상태.
  - **OS의 대응**: "이 요리를 하려면 최소 도마 3칸([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))이 필요하구나. 내가 도마 3칸을 100% 보장해 줄게. 만약 주방에 도마 3칸이 안 남았어? 그럼 너는 요리 시작하지 말고 밖에 나가서 기다려(Swap-out)."

- **발전 과정**:
  1. **고정 할당**: 무조건 10개씩 줌. [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) 폭발.
  2. <strong><a href="/studynote/02_operating_system/07_virtual_memory/416_working_set_model/">워킹 셋 모델</a> (1968)</strong>: $\Delta$ 시간을 추적하여 동적으로 할당량을 바꿈. 이론적으로 완벽하나 과거 추적 오버헤드가 큼.
  3. <strong><a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/">PFF</a> (<a href="/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/">Page Fault Frequency</a>)</strong>: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 직접 계산하기 어려우니, 단순히 "[Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Fault가 너무 자주 터지면 프레임 더 주고, 안 터지면 뺏자"는 현실적인 대안으로 진화.

- **📢 섹션 요약 비유**: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)은 한 가족이 최소한 사람답게 살기 위해 필요한 '최저 평수'와 같습니다. 국가(OS)가 국민을 많이 수용하겠다고 집을 1평짜리로 잘게 쪼개어 나눠주면 모두가 미쳐버립니다([스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)). 10평이 안 될 바엔 차라리 이민(Swap-out)을 보내는 것이 국가 전체를 유지하는 길입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 추적 (Tracking) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 시뮬레이션

OS는 $\Delta$ ([Window Size](/studynote/03_network/04_data_link_layer_error/215_window_size_sender_receiver/), 예: 최근 10번의 메모리 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))를 기준으로 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 계산한다.
메모리 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 문자열이 `[1, 2, 2, 3, 1, 5, 5, 5, 5, 5, 4, 4]`라고 하자. ($\Delta = 5$)

1. **시간 $t_1$ ([참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)열 앞부분 `1, 2, 2, 3, 1` 실행 직후)**:
   - 최근 5번 동안 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호를 모아본다: {1, 2, 3}
   - 중복을 제거하면 $WS(t_1) = \{1, 2, 3\}$.
   - **결론**: 이 프로세스는 지금 3개의 프레임만 주면 [Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 없이 잘 돌아간다.

2. **시간 $t_2$ ([참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)열 뒷부분 `5, 5, 5, 4, 4` 실행 직후)**:
   - 최근 5번 동안 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/): {5, 4}
   - $WS(t_2) = \{4, 5\}$.
   - **결론**: 프로그램이 루프(for 문)를 벗어나 다른 함수로 넘어갔다. 이제 2개의 프레임만 주면 된다. 아까 갖고 있던 1, 2, 3번 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 뺏어도 된다!

**[핵심 원리]**: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 크기($WSS$)는 프로그램이 실행됨에 따라 커지기도 하고 작아지기도 하며 역동적으로 춤을 춘다. OS 스케줄러는 시스템의 남은 프레임 수가 $\Sigma WSS_i$ (모든 프로세스의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 합)보다 작아지는 순간, <strong><a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a>이 터질 것을 직감하고 즉시 프로세스 하나를 통째로 Suspend(Swap-out) 시켜버린다.</strong>

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/)) 모델 vs [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/))

[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 이론은 완벽하지만, 매번 메모리를 읽을 때마다 $\Delta$ 윈도우를 갱신하는 건 CPU 연산의 큰 낭비다. 그래서 현실적인 PFF가 등장했다.

| 비교 항목 | [Working Set Model](/studynote/02_operating_system/07_virtual_memory/416_working_set_model/) | [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([페이지 부재 빈도](/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) |
|:---|:---|:---|
| **동작 원리** | 과거 $\Delta$ 시간 동안 <strong><a href="/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>된 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 번호</strong>를 추적 | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 번호는 안 보고, <strong><a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">Page</a> Fault가 터진 횟수</strong>만 추적 |
| **할당 늘리는 시점**| $WSS$가 증가했을 때 (직접 추적) | [Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 발생률이 **상한선(Upper Bound) 초과 시** |
| **할당 뺏는 시점** | 과거 윈도우에서 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 사라졌을 때 | [Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 발생률이 **하한선(Lower Bound) 미달 시** |
| **구현 비용** | 엄청나게 높음 (하드웨어/소프트웨어 오버헤드) | **매우 낮음 (Fault 발생 시점에만 계산하면 됨)** |

### 과목 융합 관점

- <strong>컴퓨터구조 (<a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a>) / 캐시 관리</strong>: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 개념은 가상 메모리에만 있는 게 아니다. CPU의 L1/L2 캐시도 결국 <strong>"현재 실행 중인 <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>이 캐시 크기보다 작으면 캐시 미스가 0이고, <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>이 캐시 크기보다 크면 캐시 <a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a>이 터진다"</strong>는 완벽히 똑같은 법칙의 지배를 받는다. 최적화된 C/C++ 코드는 자신의 [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)이 L1 캐시(보통 32KB)를 넘지 않도록 배열을 타일링(Tiling) 기법으로 잘게 쪼개어 연산한다.
- <strong><a href="/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/">클라우드 컴퓨팅</a> (Cloud)</strong>: K8s의 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) Killer나 AWS의 오토스케일링은 [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 철학의 연장선이다. 특정 노드의 메모리가 한계에 달해 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)이 터질 것 같으면, 쿠버네티스는 해당 노드에서 가장 만만한 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))를 쫓아내어(Evict) 다른 노드로 옮긴다(Swap-out의 클라우드 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)). 이를 통해 남은 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 사수한다.

- **📢 섹션 요약 비유**: [워킹 셋 모델](/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)이 직원의 "업무 일지([참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)열)"를 1분 단위로 검사해서 책상 크기를 정해주는 깐깐한 관리자라면, PFF는 직원이 "서류 놓을 데가 없어요!([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/))"라고 불평할 때마다 책상을 넓혀주고, 조용히 일하면 책상을 뺏는 실용주의 관리자입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — Windows OS의 메모리 관리와 <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a> Tuning</strong>: 윈도우 서버에서 대용량 SQL Server를 돌리는데, 가끔 서버 전체가 얼어버린다(Hang).
   - **원인 분석**: 윈도우는 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)의 최솟값(Min)과 최댓값(Max)을 프로세스마다 API로 조절할 수 있다(`SetProcessWorkingSetSize`). SQL Server가 램을 다 먹고 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 비대하게 늘려놨는데, OS가 시스템 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 데몬을 돌리려고 SQL Server의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 강제로 깎아버리며(Trimming) 디스크 스왑을 유발했다.
   - **대응 (아키텍처 적용)**: [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 같은 1티어 애플리케이션은 OS에게 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 뺏기면 치명적이다. 윈도우 그룹 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)(GPO)에서 <strong>"<a href="/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a> pages in memory" (메모리에 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 잠금)</strong> 권한을 SQL Server [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 계정에 부여하여, OS가 아무리 급해도 DB의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)만큼은 절대 [스왑 아웃](/studynote/02_operating_system/06_memory_management/336_swap_out_in/)하지 못하게 물리적으로 핀(Pinning)을 박아야 한다.

2. <strong>시나리오 — GC(Garbage Collector)의 Stop-The-World와 <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a> 파괴</strong>: Java 앱이 평소엔 빠르다가 Full GC가 돌고 나면 갑자기 1~2초간 굉장히 느려지는 Jitter(지터) 현상 발생.
   - **원인 분석**: Full GC가 돌면, 평소 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)에 없던 오래된 객체(Old Generation)들을 검사하기 위해 평소엔 안 읽던 힙 메모리의 구석구석을 몽땅 터치([Reference](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))한다. 이 과정에서 JVM의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 크기가 일시적으로 수 기가바이트로 폭발하고, 이로 인해 수만 번의 Minor [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Fault가 터지며 CPU 캐시와 TLB가 모조리 박살 났다([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/) Pollution).
   - **기술사적 가이드**: 이 현상을 막으려면 힙 공간 전체를 휘젓는 Full GC가 아예 발생하지 않도록 튜닝해야 한다. 힙 크기를 너무 크게 잡으면 오히려 GC 스캔 시 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 폭발 오버헤드가 커지므로, ZGC나 G1GC를 사용해 힙의 일부 리전(Region) 단위로만 잘게 잘게 GC를 수행하여 시스템 전체의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 작고 따뜻하게(Hot) 유지해야 한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 애플리케이션 메모리 튜닝 (워킹 셋 보존 전략) 플로우        |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [앱의 성능이 간헐적으로 뚝뚝 떨어지는 현상 (Latency Spike) 발생]           |
  |                |                                                  |
  |                v                                                  |
  |      서버의 전체 RAM이 부족하여 OS 레벨의 Swap Out이 잦은가?               |
  |          +- 예 ------> [글로벌 스래싱 위기]                          |
  |          |            대책 1: 하드웨어 RAM 스케일 업 (가장 확실함)        |
  |          |            대책 2: 앱 하나를 다른 서버로 분리 (Swap-out과 동일 효과)|
  |          +- 아니오 (RAM은 넉넉한데 내 앱만 느려진다)                     |
  |                |                                                  |
  |                v                                                  |
  |      애플리케이션의 메모리 접근 패턴(Locality)이 엉망인가?                  |
  |      (예: 10GB짜리 배열을 가로세로 무작위로 계속 널뛰기하며 읽어댄다)            |
  |          +---> [워킹 셋 폭발 (Working Set > L3 Cache / TLB)]         |
  |          |    결론: H/W 스펙을 소프트웨어가 찢어버린 상태. 코드를 뜯어고쳐서   |
  |          |          한 번에 작은 배열(Chunk) 단위로만 연산하도록              |
  |          |          공간적 지역성(Spatial Locality)을 확보하는 리팩토링 필수.  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "메모리 릭(Leak)은 고치기 쉽지만, [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 팽창은 고치기 어렵다." 릭은 안 쓰는 걸 안 버린 거라 지우면 되지만, [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 팽창은 "진짜 연산에 10GB가 전부 다 동시에 필요한 멍청한 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)"이기 때문에 로직 자체를 쪼개야 한다. 아키텍트는 개발자에게 "한 번에 하나의 작은 장난감 상자(Locality)만 꺼내서 놀라"고 코딩 컨벤션을 강제해야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **Swapiness 튜닝**: 리눅스 커널의 `vm.swappiness` (0~100) 값은 OS가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 캐시를 버릴지, 앱의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([익명 메모리](/studynote/02_operating_system/07_virtual_memory/391_anonymous_memory/))을 버릴지 결정하는 지표다. 100에 가까울수록 앱의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 디스크로 쫓아내는 걸 선호한다. 일반 서버는 60이지만, DB 서버는 내 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 지키기 위해 무조건 `1` 또는 `10` 수준으로 낮춰서 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)을 방어했는가?

- **📢 섹션 요약 비유**: 넓은 책상(RAM)이 있어도, 시험공부에 필요한 책([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))이 100권이라면 결국 책상은 좁아집니다. 책상을 늘리는 데는 한계가 있으니, 공부 방식 자체를 '오늘은 1단원 책 3권만 완벽히 끝낸다(지역성)'로 바꿔야 성적이 오릅니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 무지성 [다중 프로그래밍](/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) (과거) | [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) / [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 모델 적용 (현재) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a>)</strong> | 임계점 돌파 시 무한대 폭증 | [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 상한선 도달 시 프로세스 축출 | [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/)) 100% 원천 차단 |
| **정량 (CPU 활용률)**| [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)으로 인해 0% 수직 낙하 | 80~90%의 안정적인 스윗 스팟 유지 | 하드웨어 연산 능력의 극강화 |
| **정성 (시스템 생존)**| 메모리 부족 시 시스템 전체 Freeze | 만만한 프로세스만 킬/스왑아웃 | 멈추지 않는 미션 크리티컬 OS 달성 |

### 미래 전망
- **Non-Volatile Memory (NVM/PMEM)와의 융합**: 디스크가 램만큼 빨라지는 옵테인(Optane) 같은 비휘발성 메모리 시대가 오면서 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)의 개념이 흔들리고 있다. [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Fault를 처리해 디스크에서 데이터를 가져오는 속도 자체가 램 속도와 비슷해진다면, 굳이 복잡하게 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 추적하고 방어할 필요 없이 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) 자체를 하드웨어 대역폭으로 짓누를 수 있게 되는 패러다임 전환이 일어나고 있다.

### 결론
[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/))은 "인간의 행동에는 패턴이 있다"는 지역성의 원리를 메모리 관리에 이식한 가장 아름다운 모델이다. 이 모델은 무한정 프로그램을 띄워대며 자멸로 향하던 초창기 운영체제의 탐욕을 멈춰 세우고, "자원의 한계를 인정하고, 살릴 놈만 확실히 살리자"는 잔인하지만 필수적인 철학([스왑 아웃](/studynote/02_operating_system/06_memory_management/336_swap_out_in/))을 정립했다. 우리가 스마트폰에서 수십 개의 앱을 켜도 현재 보고 있는 앱이 절대 끊기지 않는 이유는, 뒤에 숨은 백그라운드 앱들을 냉혹하게 재워버리며 내 눈앞의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 사수해 주는 OS의 눈물겨운 사투 덕분이다.

- **📢 섹션 요약 비유**: 10개의 화분을 키울 때 물(메모리)이 부족하면, 모든 화분에 물을 1/10씩 찔끔찔끔 줘서 10개를 다 말려 죽이는 것([스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/))은 최악입니다. 3개 화분에만 물([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))을 듬뿍 줘서 살려내고 7개는 어두운 창고(디스크)에 잠시 치워두는 것이 진정한 식물(시스템) 관리의 지혜입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [최적 알고리즘](/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/) ([OPT](/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/)) 구현 불가 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/)) CPU 이용률 저하 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [디스크 스케줄링](/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) SCAN 엘리베이터 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [C-SCAN](/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 회전 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스래싱 (Thrashing) CPU 이용률 저하]
    |
    v
[워킹 셋 (Working Set) 메모리]
    |
    +---> [디스크 스케줄링 SCAN 엘리베이터]
    +---> [C-SCAN 단방향 회전]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수가 책상(램)에서 '로봇 조립' 숙제를 할 때, 로봇 머리, 팔, 다리 부품 3개([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))는 무조건 책상 위에 있어야만 화내지 않고 조립을 할 수 있어요.
2. 만약 동생이 책상을 차지해서 부품 1개를 바닥(디스크)에 내려놔야 한다면? 철수는 1초마다 바닥에서 팔 줍고, 머리 내리고 하느라 조립(CPU 연산)은 1개도 못 하고 땀만 뻘뻘 흘립니다([스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)).
3. 엄마(OS)가 나타나서 규칙을 정했어요! "철수가 조립할 땐 무조건 부품 3개 놓을 자리는 보장해 줘! 책상이 모자라면 동생 너는 방 밖(Swap-out)으로 나가서 기다려!" 이게 바로 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)을 지켜주는 원리랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 726 / 800

<- **이전**: [725. 스래싱 (Thrashing) CPU 이용률 저하](/studynote/02_operating_system/11_exam_summary/725_thrashing_cpu_utilization/)
**다음**: [727. 디스크 스케줄링 SCAN 엘리베이터 (Disk Scheduling Scan Elevator)](/studynote/02_operating_system/11_exam_summary/727_disk_scheduling_scan_elevator/) ->

---
