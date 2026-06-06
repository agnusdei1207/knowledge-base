---
title: "384. Pure Demand Paging"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)(Pure [Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 프로세스를 시작할 때 <strong>물리 메모리(RAM)에 단 1장의 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a>조차 미리 올려두지 않고 텅 빈 채로 강제 실행</strong>시켜, 첫 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)부터 무자비하게 [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/))를 터뜨리며 시작하는 극단적인 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) 전략이다.
> 2. **가치**: "정말 네가 요청(Demand)하기 전까진 1바이트도 주지 않겠다"는 원칙을 고수하여 <strong>메모리 선취(Pre-allocation) 낭비를 우주 끝까지 0%로 수렴</strong>시키며 시스템의 동시 실행 프로세스 한계를 극한으로 끌어올린다.
> 3. **융합**: 하지만 부팅 직후 폭풍처럼 쏟아지는 수백 번의 [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 때문에 <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 실행 속도가 끔찍하게 느려지는 치명적인 '<a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/">콜드 스타트</a>(<a href="/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a>)' 병목을 유발</strong>하므로, 이를 보완하기 위해 약간의 사전 적재를 가미하는 현대 OS의 하이브리드 정책을 낳게 한 극단적 실험체다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 일반적인 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 양심상 프로그램이 처음 켜질 때 `main()` 함수가 있는 시작 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 1장 정도는 램에 깔아주고 CPU를 돌린다. 하지만 '순수(Pure)' [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 테이블을 <strong>100% 모조리 무효(Invalid, <code>I</code>) <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a>로 떡칠</strong>해 놓고 무조건 실행(Run) 버튼을 눌러버리는 극강의 미니멀리즘 로딩 기법이다.
- **필요성**: 수백 개의 백그라운드 앱이 켜져 있는 서버나 스마트폰 환경을 생각해 보자. 앱을 켤 때마다 "이건 무조건 쓸 거야"라며 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 몇 장씩 선인심 써서 올려주다 보면([Prepaging](/studynote/02_operating_system/07_virtual_memory/385_prepaging/)), 결국 그 앱이 바로 꺼지거나 대기(Sleep) 모드로 갈 때 귀중한 램만 오염시키고 디스크 I/O를 낭비하게 된다. "인간(프로그래머)의 예측은 무조건 틀린다. 기계가 부딪혀서 증명하게 둬라!"는 철학 아래, 가장 순수하고 오류 없는 메모리 점유 곡선을 그리기 위해 고안되었다.

- <strong>등장 배경 및 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/">콜드 스타트</a>의 공포</strong>:
  1. **사전 적재의 오판**: "이 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 무조건 쓰겠지" 하고 올려놨더니 안 쓰고 종료하는 앱들이 쌓이며 캐시가 박살 남.
  2. <strong><a href="/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a> 철학의 극단화</strong>: 아예 아무것도 예측하지 마라. CPU가 찌르는(Demand) 주소만 100% 진실이다.
  3. **결과적 고통**: 부팅하자마자 폴트가 수십 번 터지며 앱이 켜지는 데 한참이 걸려 UX(사용자 경험)를 끔찍하게 깎아 먹었다.

```text
+--------------------------------------------------------------------------+
|        일반 요구 페이징 vs 순수 요구 페이징의 런타임 시작 과정           |
+--------------------------------------------------------------------------+
|                                                                          |
| [ 프로세스 P (총 10페이지) 실행 버튼 클릭! ]                             |
|                                                                          |
| -> 1. 일반 요구 페이징 (적당한 타협)                                      |
|  - OS: "음, main 함수가 있는 0번, 1번 페이지는 램에 넣어줄게."           |
|  - 램 상태: [ Pg 0 ] [ Pg 1 ] (V 비트 켜짐)                              |
|  - 실행: 스무스하게 시작하다가 중간에 Pg 2 부를 때 렉(Fault) 한 번 남.   |
|                                                                          |
| -> 2. 순수 요구 페이징 (Pure Demand Paging)                               |
|  - OS: "램? 국물도 없다. 테이블 전부 I 비트 박고 일단 CPU 굴려!"         |
|  - 램 상태: [ 텅 빔 ] (10개 다 Invalid)                                  |
|  - 실행 과정:                                                            |
|    💥 0.0001초: CPU가 1번째 줄 읽으려다 Page Fault 터짐! (디스크행)      |
|    💥 0.0010초: 0번 페이지 가져와서 다시 시작. 근데 변수 읽으려다        |
|               또 5번 페이지 Fault 터짐! (디스크행)                       |
|    💥 0.0020초: 5번 가져왔더니 스택 필요해서 9번 Fault 터짐!             |
|  - 결과: 초기 1초 동안 미친 듯이 버벅대다가(소나기), 한참 뒤에 평온해짐. |
+--------------------------------------------------------------------------+
```
**[다이어그램 해설]** 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)의 곡선은 초반에 절벽처럼 떨어졌다가 나중에 평탄해진다. 시작하자마자 코드 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)([명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(변수), [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(함수)를 세팅하느라 무더기로 [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 터진다. 하지만 이 고통스러운 '소나기(Burst of [Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) Faults)' 시기가 지나고 나면, 프로그램이 궤도에 올라 자기만의 '[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/))'을 램에 다 모아두어 폴트율이 극도로 낮아지게 된다.

- **📢 섹션 요약 비유**: 수영장에 들어갈 때, 발끝부터 물을 적시며 천천히 들어가는(사전 적재) 게 아니라, 다이빙대에서 빈몸으로 냅다 물통(디스크)에 던져진 뒤 물을 퍼 올려 수영장을 채워나가는 무식하고도 확실한 생존 방식입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Restart ([명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 재실행)의 가혹한 시험대

순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 CPU 하드웨어의 '[명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 재실행(Restart)' 능력을 극한으로 테스트한다.
- 1개의 어셈블리 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(예: `ADD A, B, C` - A와 B를 더해 C에 넣어라)를 실행한다고 치자.
- [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 자체를 퍼오느라 <strong><a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 1회</strong>
- 변수 A를 램에서 읽으려는데 없어서 <strong><a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 2회</strong>
- 변수 B를 램에서 읽으려는데 없어서 <strong><a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 3회</strong>
- 덧셈 결과를 C에 저장하려는데 공간이 없어서 <strong><a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 4회</strong>
- <strong>단 1개의 <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>를 끝내는 데만 4번의 <a href="/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/">트랩</a>(수천만 클럭 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>)이 연속으로 터질 수 있다.</strong> OS는 이 미친 폴트의 소나기를 맞고도 상태([Register](/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/), Program [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))를 완벽하게 보존했다가 다시 그 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 처음부터 재실행시킬 수 있는 철통같은 하드웨어 방어막이 있어야 한다.

---

### Locality(지역성)에 대한 절대적인 믿음

이런 끔찍한 오버헤드를 감수하고도 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)이라는 이론이 성립하는 이유는 오직 하나, 인간이 짠 프로그램의 <strong>'<a href="/studynote/02_operating_system/04_synchronization/253_locality_of_reference/">참조의 지역성</a>(<a href="/studynote/02_operating_system/04_synchronization/253_locality_of_reference/">Locality of Reference</a>)'</strong> 때문이다.
- 처음에만 미친 듯이 폴트가 날 뿐이다.
- 프로그램은 어차피 한 번 읽은 변수 근처를 루프로 맴돌며(공간 지역성), 한 번 실행한 for문을 수만 번 반복한다(시간 지역성).
- 즉, <strong>초반 1초 동안 필요한 <a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 10장(<a href="/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>)만 램에 멱살 잡혀 끌려 올라오고 나면, 그 뒤로 10시간 동안은 단 1번의 폴트도 나지 않고 메모리를 10장(40KB)만 쓰며 로켓처럼 돌아간다.</strong>
- 바로 이것이 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)이 꿈꾸는 궁극의 "가성비 메모리 효율" 곡선이다.

- **📢 섹션 요약 비유**: 처음 김치찌개를 끓일 때는 냉장고를 열 번씩 열었다 닫으며([페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)) 김치, 고기, 두부를 차례대로 꺼내오느라 엄청 부산스럽지만, 한 번 도마 위(램)에 재료를 다 올려두고 나면([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 확보) 그 뒤로 1시간 요리하는 동안 냉장고 문을 한 번도 열 필요 없이 요리에만 집중할 수 있는 원리입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) vs [선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/) ([Prepaging](/studynote/02_operating_system/07_virtual_memory/385_prepaging/))

양 극단에 서 있는 두 철학의 대결이다.

| 항목 | 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) (Pure Demand) | [선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/) ([Prepaging](/studynote/02_operating_system/07_virtual_memory/385_prepaging/) / 사전 적재) |
|:---|:---|:---|
| <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 로딩 원칙</strong> | **0장**. 무조건 찔러보고 터지면 가져옴. | **여러 장**. "이거 쓸 거 같으니 10장 한 번에 퍼와!" |
| **디스크 I/O 효율** | 한 번에 4KB씩 찔끔찔끔 여러 번 읽어 <strong>비효율의 극치 (<a href="/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/">Seek Time</a> 폭발)</strong> | 한 번 디스크 헤더 돌 때 옆에 있는 것도 연속으로 쫙 긁어와서 **효율 좋음** |
| <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 체감 속도</strong> | **앱 부팅 시 엄청 버벅댐 (렉 심함)** | **빠릿빠릿하게 바로 켜짐 (체감 좋음)** |
| **메모리 낭비도** | **0% (완벽 방어)**. 진짜 쓴 놈만 램에 남음. | 예측 틀리면 쓰레기가 램 낭비. (공간 오염) |

### [Page Fault Rate](/studynote/02_operating_system/07_virtual_memory/389_page_fault_rate_eat/) (폴트율 곡선)의 역동성

프로그램 생명주기에 따른 [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 발생 빈도의 그래프를 그려보면 극적인 L자 커브를 그린다.
- `Time = 0 (시작)`: 폴트율 **100%**. 1명령어 1폴트 수준.
- `Time = 100ms`: 필요한 조각들이 램에 모이기 시작하며 폴트율 급감.
- `Time = 1 sec`: <strong><a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>(<a href="/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>)</strong> 형성 완료. 폴트율 **0.001%** 수렴. 평온한 상태(Steady [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) 돌입.
- 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 이 초반의 100% 절벽 구간을 몸으로 온전히 때우겠다는 살신성인의 전략이다.

```text
+----------+------------+------------+-----------------------+
| 정책       | 부팅 속도(UX)| 램 공간 절약 | 하드디스크 무리 |
+----------+------------+------------+-----------------------+
| Pure Demand| ☠️ 최악    | ⭐ 최고 방어 | ☠️ 드르륵 파괴됨  |
| Prepaging  | ⭐ 쾌적    | 🔴 낭비 큼   | 🟢 수명 절약      |
+----------+------------+------------+-----------------------+
```
**[매트릭스 해설]** 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 하드디스크([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 시절에는 절대 쓸 수 없는 금기였다. 암(Arm)이 한 번 움직일 때([Seek time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) 주변 걸 다 긁어와야([Prepaging](/studynote/02_operating_system/07_virtual_memory/385_prepaging/)) 이득인데, 바보처럼 1번 폴트 나고 4KB 읽고, 또 돌아가서 4KB 읽고를 반복하면 하드디스크가 소음을 내며 터져나갔다. 이 극단적 방법은 [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/))가 등장하여 랜덤 액세스(Random Access) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 사라진 현대에 와서야 그럭저럭 비벼볼 만한 이론이 되었다.

- **📢 섹션 요약 비유**: 마트에 장 보러 갈 때, 한 번 갔을 때 오늘내일 먹을 걸 미리 다 사 오는 게([선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/)) 기름값과 시간이 절약됩니다. 밥 한 숟갈 먹고 마트 뛰어가고, 반찬 한 젓가락 먹고 마트 뛰어가는 짓(순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 기름값(디스크 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/))이 0원인 텔레포트 시대([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))에나 가능한 정신 나간 식습관입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 최신 OS의 하이브리드(Hybrid) 꼼수
- 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)은 이론적으론 아름답지만, 스티브 잡스도 빌 게이츠도 "앱 아이콘을 눌렀는데 2초 동안 렉 걸리다 켜지는 OS"는 결재해 주지 않았다.
- **현대의 타협**:
  1. 윈도우나 리눅스는 100% 순수 버전을 쓰지 않는다.
  2. 프로그램을 더블클릭하면 0.1초라도 빨리 화면을 띄워주기 위해(UX 극대화), `readahead`나 `Prefetch(슈퍼패치)` 기능을 동원해 옆에 있는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 수십 장을 <strong>미리 램에 뭉텅이로 던져준다(<a href="/studynote/02_operating_system/07_virtual_memory/385_prepaging/">Prepaging</a> 융합)</strong>.
  3. 그렇게 부팅 렉을 넘기고 나면, 그 뒤로는 무조건 <strong>'<a href="/studynote/02_operating_system/04_synchronization/255_demand_paging/">요구 페이징</a>(<a href="/studynote/02_operating_system/04_synchronization/255_demand_paging/">Demand Paging</a>)' 모드로 싹 전환</strong>하여 램을 깐깐하게 아낀다.
  4. 즉, 이론서에 나오는 "Pure Demand"는 벤치마크 테스트에서만 돌리는 철학적 극단값일 뿐, 현업의 OS는 두 가지를 간신히 버무려 쓴다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/): 대용량 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 (Zeroing)
개발자가 `int arr[1000000];` [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)을 동적 할당하고 `memset`으로 0을 채우는 코드를 짰다고 치자.
순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) 환경에서 이 코드가 돌면, [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)을 0으로 덮어쓰며 앞으로 나갈 때마다 4KB 단위로 쉴 새 없이 [Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 융단폭격이 터져버린다. CPU가 0을 쓰는 시간보다 폴트 인터럽트를 처리하고 램 빈방을 매핑해 주는 데 100배의 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시간이 소모된다([Minor Page Fault](/studynote/02_operating_system/07_virtual_memory/429_minor_vs_major_page_fault/)). 이래서 대형 버퍼 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화는 서버 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 갉아먹는 주범이 된다.

- **📢 섹션 요약 비유**: 손님이 국밥을 시켰는데 숟가락도 안 주고 일단 뚝배기만 툭 던져주는 게 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/)입니다. 손님이 화를 내며 숟가락 달라고 벨을 누르는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 발생하죠. 요즘 식당(현대 OS)은 최소한 숟가락, 젓가락, 김치(기본 워킹셋) 정도는 알아서 미리 세팅([선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/))해 주고, "더 필요한 건 벨 누르세요(이후 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/))" 하는 센스를 발휘합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **메모리 선점(Pre-allocation) 낭비 제로**| 켜놓고 안 쓰는 유령 앱들이 램을 1바이트도 갉아먹지 못하게 막아 가용 물리 램 잔고를 최대치로 유지 |
| <strong><a href="/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a> Evaluation의 극한 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> | "모든 건 요청받았을 때만 한다"는 철학이 컴퓨터 아키텍처에 어디까지 적용 가능한지 증명한 척도 |
| <strong><a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>(<a href="/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>) 모델의 근간</strong> | 폴트가 쏟아진 뒤 램에 살아남은 조각들이 결국 그 프로그램의 '진짜 필수 요소([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))'임을 증명해 내는 거름망 역할 |

### 결론 및 미래 전망

순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) (Pure [Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 결벽증에 가까운 메모리 효율을 얻기 위해 초반의 시스템 렉([Cold Start](/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/) Penalty)을 십자가처럼 짊어진 극단적 튜닝 기법이다. [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시절에는 디스크를 갈아버리는 끔찍한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 때문에 기피되었으나, [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD처럼 디스크 접근 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 나노초 단위로 내려온 현대 클라우드 시대에는 이 "지독한 게으름"이 다시금 엄청난 강점으로 부활하고 있다. 특히 수만 개의 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/))가 0.1초 단위로 켜졌다 꺼지는 최신 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)(AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)) 아키텍처에서는, 쓰지 않을 코드를 올리는 0.1초조차 사치이므로 철저하게 이 'Pure Demand' 방식이 차세대 부팅 스탠다드로 채택되어 세상을 지배해 나가고 있다.

- **📢 섹션 요약 비유**: 헬스장에 갈 때 샤워도구, 수건, 운동화를 다 챙겨가는 완벽주의자([선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/))는 짐 싸느라 헬스장에 늦게 도착하지만, 맨몸으로 슬리퍼만 끌고 가서 필요할 때마다 카운터에서 빌려 쓰는 게으른 사람(순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 가는 데 1초면 되지만 중간중간 운동이 끊깁니다. 속도가 생명인 현대 1분 쇼츠 시대엔 결국 후자의 극단적 가벼움이 대세가 된 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [가상 주소 공간](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/) ([Virtual Address Space](/studynote/02_operating_system/07_virtual_memory/382_virtual_address_space/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/) ([Prepaging](/studynote/02_operating_system/07_virtual_memory/385_prepaging/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [유효-무효 비트](/studynote/02_operating_system/07_virtual_memory/386_valid_invalid_bit/) ([Valid-Invalid Bit](/studynote/02_operating_system/06_memory_management/355_paging_memory_protection/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[요구 페이징 (Demand Paging)]
    |
    v
[순수 요구 페이징 (Pure Demand Paging)]
    |
    +---> [선행 페이징 (Prepaging)]
    +---> [유효-무효 비트 (Valid-Invalid Bit)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) (Pure [Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/))은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) ([Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/))을 이해하면 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) (Pure [Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/))이 왜 필요한지 더 쉽게 보여요.
3. 그래서 순수 [요구 페이징](/studynote/02_operating_system/04_synchronization/255_demand_paging/) (Pure [Demand Paging](/studynote/02_operating_system/04_synchronization/255_demand_paging/))을 잘 알면 나중에 [선행 페이징](/studynote/02_operating_system/07_virtual_memory/385_prepaging/) ([Prepaging](/studynote/02_operating_system/07_virtual_memory/385_prepaging/))도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 384 / 800

<- **이전**: [383. 요구 페이징 (Demand Paging) - 필요한 페이지만 메모리에 적재](/studynote/02_operating_system/07_virtual_memory/383_demand_paging/)
**다음**: [385. 선행 페이징 (Prepaging) - 페이지 부재 감소를 위해 미리 묶어 올림](/studynote/02_operating_system/07_virtual_memory/385_prepaging/) ->

---
