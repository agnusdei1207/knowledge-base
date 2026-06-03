+++
title = "397. 프레임 할당 (Frame Allocation) 알고리즘"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프레임 할당(Frame Allocation)은 [다중 프로그래밍](/knowledge-base/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) 환경에서 한정된 <strong>물리 메모리(Free Frames)라는 파이를 시스템에 띄워진 여러 프로세스들에게 '몇 개씩 쪼개어 나눠줄 것인가'를 결정</strong>하는 운영체제의 거시적 자원 분배 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: 특정 프로세스에 프레임을 너무 적게 주면 매 클럭마다 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)를 뿜어내는 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))에 빠져 죽고, 너무 많이 주면 다른 프로세스가 굶어 죽으므로([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)), 전체 시스템의 <strong>동시 실행 효율(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/">Degree of Multiprogramming</a>)과 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 극대화할 황금 밸런스</strong>를 맞춘다.
> 3. **융합**: 이 [할당량](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)의 크기는 <strong>균등(Equal)/비례(Proportional) 할당</strong>이라는 정적 규칙에서 출발하여, 프로세스의 활동량([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/))에 따라 프레임을 뺏고 더해주는 동적 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>)</strong> 개념과 융합되어 현대 OS의 적응형 스케줄링으로 진화했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 물리 램(RAM)이 16GB(400만 개의 프레임)가 있다고 치자. OS가 1GB를 먹고 남은 15GB를 크롬, [워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/), 롤(LoL) 세 프로세스가 나눠 써야 한다. "도대체 누구에게 램을 얼마나 할당해 줘야 할까?"라는 철학적 분배의 문제다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)(Replacement)가 '빈방 없을 때 누구를 죽일까?'라는 국지전이라면, 프레임 할당은 '애초에 병력을 몇 명씩 파병할까?'라는 전체 전쟁의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))이다.
- **필요성**: [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)는 마법이 아니다. 프로그램이 정상적으로 돌아가려면 램에 최소한으로 깔려 있어야 하는 '최소 프레임 수'라는 게 존재한다. 예를 들어 CPU의 한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(`MOVE [A], [B]`)를 처리하려면 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 자체(1장) + 변수 A(1장) + 변수 B(1장) 등 한 번에 최소 3장의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 무조건 램에 있어야만 에러 없이 돈다. 만약 OS가 프로세스에게 램을 달랑 2장만 할당해 주면, 3장을 모을 수가 없어서 폴트가 영원히 무한 반복되는 시스템 마비 상태가 터진다. 이 파국을 막기 위한 지능적 분배 기준이 절대적으로 필요했다.

- **등장 배경 및 분배의 딜레마**:
  1. **요구 페이징의 맹점**: 요구 페이징으로 필요한 것만 올리다 보니, 어떤 앱은 끝도 없이 프레임을 요구해 램을 독식해 버렸다.
  2. **최소/최대 할당의 가이드라인 필요**: [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 구조([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))가 꼬이지 않기 위한 절대적인 최소 프레임 수를 보장해야 했다.
  3. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>의 고도화</strong>: 무식하게 1/N로 나누는 [균등 할당](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/)에서 시작해, 덩치에 비례해서 주는 비례 할당을 거쳐, 런타임에 눈치껏 조절하는 동적 할당으로 뼈대가 굳어졌다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│        프레임 할당의 극단적 실패 사례 (스래싱 유발) 시각화              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ [ 상황: 10,000 프레임을 가진 무거운 그래픽 편집기 실행 ]                │
│                                                                         │
│ ▶ 1. 램을 너무 조금 할당했을 때 (예: 5 프레임만 할당)                   │
│  - 프로그램 루프가 돌 때마다 10장의 페이지를 핥고 지나가야 함.          │
│  - 근데 방이 5개뿐이라, 6번째 페이지 가져올 때 1번 쫓아냄.              │
│  - 7번째 가져올 때 2번 쫓아냄... 무한 교체 지옥 발생!                   │
│  💥 결과: Page Fault Rate가 폭발하여 시스템 완전 정지 (Thrashing)       │
│                                                                         │
│ ▶ 2. 램을 너무 많이 할당했을 때 (예: 9,000 프레임 독점)                 │
│  - 그래픽 편집기는 너무나 쾌적하고 부드럽게 돌아감.                     │
│  - 하지만 뒤에 백그라운드로 띄워둔 음악 플레이어와 백신 프로그램이      │
│    프레임을 1장도 못 받아서 노래가 끊기고 튕겨버림!                     │
│  💥 결과: 다중 프로그래밍 수준(Degree)이 바닥으로 처박힘.               │
└─────────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** [할당량](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)(Allocation Size)과 [페이지 부재율](/knowledge-base/studynote/02_operating_system/07_virtual_memory/389_page_fault_rate_eat/)(Fault Rate)은 반비례 곡선을 그린다. 프레임을 많이 주면 폴트는 줄어들어 그 앱은 날아다니지만 남들이 죽고, 프레임을 아끼면 여러 앱을 띄울 순 있지만 폴트가 터져 모두가 버벅댄다. OS는 이 곡선의 변곡점(무릎)을 귀신같이 찾아내어 딱 그만큼만 램을 끊어주는 줄타기의 장인이 되어야 한다.

- **📢 섹션 요약 비유**: 부모가 용돈(프레임)을 줄 때, 첫째에게 100만 원을 주면 둘째가 굶어 죽고([다중 프로그래밍](/knowledge-base/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) 실패), 둘 다 1만 원씩 쪼잔하게 주면 둘 다 매일 돈 달라고 전화를 해대는([페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 폭발) 극단적 상황을 막는 지혜로운 재무 설계입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 최소 프레임 수 (Minimum Number of Frames)의 하드웨어적 강제

"아무리 적게 줘도 이것보단 많이 줘야 프로그램이 터지지 않는다"는 절대 하한선이 있다. 이는 OS가 아닌 <strong>CPU 하드웨어의 <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a> 구조(<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/">ISA</a>)</strong>가 결정한다.
- 인텔 x86이나 [MIPS](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/201_mips/) 같은 CPU는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 하나를 실행할 때, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 자체가 여러 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 걸쳐 있거나 [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)([Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/))을 통해 피연산자가 여러 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 흩어져 있을 수 있다.
- 예를 들어, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 코드가 1번, 2번 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 걸쳐 있고, 가져올 데이터가 3번 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에, 저장할 곳이 4번 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 있다면?
- 이 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 한 번 치기 위해선 <strong>무조건 최소 4장의 프레임</strong>이 물리 램에 깔려 있어야 한다. OS가 3장만 할당해 주면 4번째 장을 가져올 때 1번 장을 쫓아내게 되어, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 영원히 완성되지 못하고 제자리를 맴도는 무한 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 재앙이 터진다.

---

### 정적 할당(Static Allocation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

프로세스의 실행 전 덩치(사이즈)만 보고 미리 기계적으로 파이를 나눠주는 고전적인 2가지 방식이다.

1. <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/">균등 할당</a> (<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/">Equal Allocation</a>)</strong>
   - 가용 프레임이 100개고 프로세스가 5개면, 묻지도 따지지도 않고 공산주의처럼 20개씩 칼같이 나눠준다.
   - **문제점**: 10KB짜리 계산기 앱은 20개를 받아 15개를 버리고(낭비), 10GB짜리 오라클 DB도 20개를 받아 숨이 막혀 죽어버리는 최악의 비효율을 낳는다.
2. **비례 할당 (Proportional Allocation)**
   - 자본주의 방식. 프로세스의 총 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 크기에 비례하여 프레임을 준다.
   - 10GB짜리 앱에는 90프레임을, 10KB짜리 앱에는 1프레임을 준다.
   - **문제점**: 10GB짜리 앱이라도 막상 켜놓고 가만히 숨만 쉬고 있으면(예: 최소화된 브라우저 창), 이 녀석에게 90프레임을 묶어두는 것 자체가 거대한 램 낭비다. (런타임의 동적 활동량을 반영하지 못함).

- **📢 섹션 요약 비유**: [균등 할당](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/)은 몸무게 100kg 씨름선수와 10살 꼬마에게 똑같이 밥 한 공기씩 주는 바보 같은 배식이고, 비례 할당은 덩치가 크면 무조건 밥을 5공기 퍼주는 방식입니다. 하지만 덩치가 커도 지금 다이어트 중이거나 잠자고 있다면(동적 비활성), 그 5공기는 그대로 썩어버리는 치명적 한계가 있습니다.

---

## Ⅲ. 비교 및 연결

### 우선순위 할당 (Priority Allocation)

크기(Size)가 아닌 프로세스의 '중요도(Priority)'에 따라 프레임을 몰아주는 기법이다.
- 비례 할당의 공식을 살짝 비틀어, 크기 대신 프로세스의 우선순위 수치로 배율을 정한다.
- 램이 모자라서 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 터졌을 때, 1순위 VIP [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 프로세스는 자기가 가진 걸 안 버리고, **우선순위가 가장 낮은 꼴찌 프로세스의 프레임을 뺏어서(강제 수용) 자기 방에 채워버린다.** 
- 모바일 OS(Android, iOS)에서 내가 지금 보고 있는 전면(Foreground) 앱이 날아다니고, 뒤에 숨겨둔 백그라운드(Background) 앱들이 프레임을 다 뺏기고 멈춰버리는 현상의 코어 로직이다.

### [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/) vs [지역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/)의 배분 철학

할당(Allocation)과 교체(Replacement)는 동전의 양면이다. 

| 할당 및 교체 조합 | 철학 및 결과 | 현대 OS 채택 여부 |
|:---|:---|:---|
| <strong>고정 할당 + <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/">지역 교체</a></strong> | 딱 100프레임만 주고, 넘치면 니들 안에서 알아서 쫓아내며 살아라. **타 앱에 피해를 주진 않지만 램 활용도가 썩어 들어감**. | ❌ 낡은 메인프레임 방식 |
| <strong>가변 할당 + <a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/">전역 교체</a></strong> | 일단 주고, 더 필요하면 램을 휩쓸며 남의 방을 막 뺏어와라! **전체 램 가동률 99%의 멱살 캐리 가능하지만 남의 렉을 유발**. | 🟢 리눅스, 윈도우의 абсолют 스탠다드 |

```text
┌──────────┬────────────┬────────────┬──────────────────────────────┐
│ 램 쟁탈전  │ 승자 프로세스 │ 패자 프로세스 │ 전체 시스템 스루풋   │
├──────────┼────────────┼────────────┼──────────────────────────────┤
│ 전역 교체  │ 램 쫙 빨아먹음│ 쫓겨나서 버벅댐│ 🚀 램 낭비 없이 최고│
│ 지역 교체  │ 자기 방만 씀  │ 피해 안 받음  │ 🐢 남는 램 썩음      │
└──────────┴────────────┴────────────┴──────────────────────────────┘
```
**[매트릭스 해설]** 리눅스는 지독한 능력주의([전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/))를 택했다. 열심히 일하는 놈이 폴트를 쳐서 램을 요구하면, 가만히 쉬고 있는 남의 프레임을 가차 없이 빼앗아 일하는 놈에게 퍼준다. 이로 인해 프로세스별 [할당량](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)은 매초마다 고무줄처럼 변하며, 이는 자연스럽게 다음 장에서 배울 <strong>동적 할당(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>)</strong> 아키텍처로 이어지게 된다.

- **📢 섹션 요약 비유**: [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/) 시스템은 회사 책상이 부족할 때, 놀고 있는 직원의 빈 책상을 확 뺏어서 야근하는 에이스 직원에게 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/) 3개 세팅하라고 몰아주는 철저한 성과주의 환경입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: cgroups를 통한 프레임 [할당량](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/) 하드 락(Hard Limit)
1. **클라우드의 위기**: 
   - 리눅스의 묻지마 [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/)(능력주의)는 [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 시대에 치명적 위기를 맞았다.
   - 서버 하나에 10개 회사 앱을 띄웠는데, 1번 회사 앱 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) 버그를 내며 미친 듯이 램을 요구([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))했다.
   - [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/) 논리에 의해 리눅스는 나머지 9개 회사의 프레임(램)을 다 뺏어서 1번 놈에게 줘버려 멀쩡한 9개 회사가 다 뻗어버리는 대참사(Noisy Neighbor)가 났다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/">cgroups</a> (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/">Control Groups</a>)의 구원</strong>:
   - 구글 엔지니어들은 이 야생의 [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/)를 통제하기 위해, 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/">cgroups</a></strong>라는 철창을 만들었다.
   - [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)마다 `Memory Limit = 1GB` 라는 하드웨어적 철창([지역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/)의 부활)을 씌웠다.
   - 1번 회사가 1GB를 다 채우면? 더 이상 남의 램을 못 뺏게 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 킬러로 그 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 하나만 깔끔하게 암살해 버린다.
3. **실무의 결론**: 
   - 현대 백엔드 인프라(k8s)는 OS의 유연한 전역 할당([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)) 위에 cgroups라는 깐깐한 지역 할당 제한(보안/격리)을 강제로 덮어씌운 완벽한 하이브리드 경제 체제로 돌아가고 있다.

### [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드별 할당의 한계
다중 코어 서버에서는 프레임의 '개수'만 할당해 줘선 안 된다. "어느 노드(CPU [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)) 쪽에 붙어있는 프레임인가?"라는 물리적 위치가 속도를 좌우한다. 아무리 1000개의 프레임을 넉넉히 할당받았어도, 내 코어(Node 0)에서 저 멀리 다리를 건너야 하는 Node 1의 프레임으로만 1000개를 받았다면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 반토막이 난다(리모트 페널티). 프레임 할당 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 이제 '양'뿐만 아니라 '위치'까지 고려해야 하는 차원으로 진화했다.

- **📢 섹션 요약 비유**: 방목형 농장([전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/))에서 소들이 자유롭게 남의 구역 풀까지 다 뜯어 먹으며 살찌게 놔두다가, 미친 소 한 마리가 농장 전체 풀을 다 박살 내자, 농장주([쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/))가 튼튼한 울타리([cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/))를 쳐서 "딱 이 구역 풀만 먹어라!" 하고 강제 배급제로 돌려버린 클라우드 목장의 현실입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/">Thrashing</a>) <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a></strong> | 무한정 램을 뺏고 뺏기는 악순환의 고리를 끊고, 최소한의 작동 보장선(Minimum Frames)을 지켜내어 시스템 붕괴를 방어 |
| **공정성(Fairness)과 효율성의 타협**| 무식한 N분의 1 [균등 할당](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/)을 버리고 동적 [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/)를 채택하여, 노는 램을 1바이트도 남기지 않는 100% 가동률 달성 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 생태계의 뼈대</strong> | [할당량](/knowledge-base/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)을 엄격히 통제하는 cgroups와 결합하여, 남의 자원을 훔쳐 쓰지 못하게 막는 클라우드 샌드박싱의 인프라로 진화 |

### 결론 및 미래 전망

프레임 할당 (Frame Allocation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 컴퓨터 과학에서 "유한한 재화를 어떻게 분배하는 것이 가장 정의로우면서도 동시에 효율적인가?"라는 정치경제학적 물음을 0과 1의 세계에 던진 철학적 명제다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 공학자들은 고정된 크기(균등/비례)를 미리 떼어주는 통제 경제를 시도했으나 참담하게 실패했다. 결국 "필요할 때마다 남의 것을 빼앗아 쓰는 야생의 시장 경제([전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/))"가 전체 시스템 처리량을 우주 끝까지 올려준다는 것을 깨달았다. 하지만 그 야생성이 이웃 앱을 죽이는 부작용(Noisy Neighbor)을 낳자, 현대에 와서는 다시 cgroups라는 보이지 않는 손을 개입시켜 통제하는 나선형적 진화를 거치고 있다. 앞으로 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대의 무지막지한 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) VRAM 할당 전쟁에서도 이 분배와 통제의 변증법은 동일하게 반복될 것이다.

- **📢 섹션 요약 비유**: 중앙에서 똑같이 식량을 배급하던 공산주의(균등 고정 할당)가 굶주림(비효율)에 무너지고, 능력껏 밥을 뺏어 먹는 자본주의([전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/))가 풍요를 가져왔지만, 독점의 폐해가 커지자 결국 복지 규제([cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 제한)를 통해 밸런스를 맞추게 된 인류 경제 시스템의 완벽한 램(RAM) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 거울입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) ([Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/))의 필요성 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [변경 비트](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/) (Modify [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) / [Dirty Bit](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [균등 할당](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/) ([Equal Allocation](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/)) vs 비례 할당 (Proportional Allocation) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/) ([Global Replacement](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[변경 비트 (Modify Bit / Dirty Bit)]
    │
    ▼
[프레임 할당 (Frame Allocation) 알고리즘]
    │
    ├──▶ [균등 할당 (Equal Allocation) vs 비례 할당 (Proportional Allocation)]
    └──▶ [전역 교체 (Global Replacement)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 프레임 할당 (Frame Allocation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [변경 비트](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/) (Modify [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) / [Dirty Bit](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/))을 이해하면 프레임 할당 (Frame Allocation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 프레임 할당 (Frame Allocation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 잘 알면 나중에 [균등 할당](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/) ([Equal Allocation](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/)) vs 비례 할당 (Proportional Allocation)도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 397 / 800

← **이전**: [396. 변경 비트 (Modify Bit / Dirty Bit) - 교체 시 디스크 기록 여부 결정, 디스크 I/O 최적화](/knowledge-base/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)
**다음**: [398. 균등 할당 (Equal Allocation) vs 비례 할당 (Proportional Allocation)](/knowledge-base/studynote/02_operating_system/07_virtual_memory/398_equal_vs_proportional_allocation/) →

---
