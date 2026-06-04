---
title: "793. 워킹 셋 윈도우 사이즈 동적 조절 (Working Set Window Size Dynamic Adjustment)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/)) 모델은 [다중 프로그래밍](/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) 환경에서 특정 프로세스가 **"최근 일정 시간(Window, $\Delta$) 동안 미친 듯이 집중적으로 참조한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들의 묶음"을 수학적으로 예측하여, 그만큼의 메모리는 절대 빼앗지 않고 RAM에 상주시켜 주는 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/)) 방어 아키텍처**다.
> 2. **가치**: 스케줄러가 남는 램이 부족하다는 이유로 무지성하게 남의 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 훔쳐 갔다가 서버 전체가 디스크를 긁으며 죽어버리는 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) 현상을 원천 차단하고, 프로세스마다 딱 필요한 만큼의 밥그릇(메모리 프레임) 크기를 동적으로 보장해 준다.
> 3. **융합**: 이 모델은 "과거를 보면 미래를 알 수 있다"는 프로그램의 <strong>지역성(Locality) 원리</strong>를 시계열적으로 극대화한 것이며, 현대 운영체제의 [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/)([Page Fault Frequency](/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 융합되어 실시간으로 할당 메모리 [윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/)를 고무줄처럼 늘리고 줄이는 동적 제어의 뼈대가 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - 1968년 피터 데닝(Peter Denning)이 제안한 혁명적 메모리 관리 이론.
  - **지역성(Locality)**: 프로세스는 메모리 1GB를 다 쓰지 않고 특정 루프(Loop)를 돌 땐 특정 10MB 구역만 미친 듯이 반복해서 읽는다. 이 10MB가 바로 '[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)'이다.
  - **[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 윈도우($\Delta$)**: "최근 몇 초, 혹은 최근 몇 번의 메모리 참조를 관찰할 것인가?"를 정하는 관측 창문의 크기.

- **필요성(문제의식)**:
  - 과거의 멍청한 OS는 100명이 접속하면 램을 그냥 100등분 해서 1/100씩 줬다. (고정 할당).
  - A 프로그램은 게임이라 램이 많이 필요한데 1/100만 주니까, 계속 램이 모자라서 디스크를 긁고([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/)), B 프로그램은 메모장이라 램을 안 쓰는데 1/100을 들고 펑펑 놀았다.
  - 결국 A 프로그램이 램을 달라고 징징대다 못해 시스템 전체의 스왑(Swap) 공간을 폭파시키는 <strong><a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a>(<a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">Thrashing</a>)</strong>이 발생해 컴퓨터가 멈춰버렸다.
  - **해결책**: "각 프로그램이 최근 1분 동안 진짜로 자주 건드린 핵심 메모리 조각([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)) 개수를 세어라! 그리고 최소한 그 개수만큼은 절대 남한테 뺏기지 않게 보장해 줘라!"

  - **고정 할당 (구형)**: 도서관 책상에 무조건 책을 3권씩만 올려둘 수 있다. 법전을 찾아가며 레포트를 쓰는 학생은 책 3권으로 부족해서 매번 서고(디스크)를 뛰어갔다 오느라 땀범벅이 되고([스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)), 만화책 한 권 보는 학생은 책상 자리가 텅텅 남는다(낭비).
  - <strong><a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a> (동적 할당)</strong>: 사서(OS)가 관찰해 보니 레포트 쓰는 학생은 지난 10분(윈도우 $\Delta$) 동안 책 8권을 미친 듯이 번갈아 보고 있다. 사서는 이 학생에게 강제로 책 8권을 펼칠 수 있는 거대한 책상(프레임 추가 할당)을 배정해 주어 서고에 갈 일 없이 폭풍 타자를 치게 만들어준다.

- **등장 배경**:
  - [다중 프로그래밍](/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/)([멀티태스킹](/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/))의 극대화로 시스템 램(RAM)의 고갈이 일상화되면서, CPU 이용률을 떨어뜨리는 가장 악질적인 질병인 '[스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/))' 현상의 원인을 규명하고 이를 치료하기 위한 가장 학술적이고 수학적인 대응책으로 등장했다.

```text
  +-------------------------------------------------------------+
  |                 워킹 셋(Working Set) 관측 및 동적 추출 원리 시각화     |
  +-------------------------------------------------------------+
  |                                                             |
  |   [ 윈도우 크기(Delta, Δ) = 5 (최근 5번의 페이지 참조 기록) ]        |
  |                                                             |
  |   시간축 ---> (프로그램이 메모리를 접근하는 순서)                       |
  |   Page 접근:  ... [ 1 ] [ 5 ] [ 1 ] [ 2 ] [ 1 ] [ 9 ] [ 9 ] ... |
  |                                                             |
  |   [ 시점 T1: (가운데 [1]에 있을 때 과거 5번 관측) ]                 |
  |   관측된 5개: [ 1, 5, 1, 2, 1 ]                               |
  |   -> 중복 제거 후 워킹 셋 집합 W(T1, 5) = { 1, 2, 5 }             |
  |   -> OS의 조치: "현재 이 앱의 워킹 셋 크기(WSS)는 3이다!              |
  |               물리 프레임을 최소 3개 보장하고 딴 놈한테 뺏기지 마라!"     |
  |                                                             |
  |   [ 시점 T2: (시간이 흘러 [9]에 있을 때 과거 5번 관측) ]              |
  |   관측된 5개: [ 1, 2, 1, 9, 9 ]                               |
  |   -> 중복 제거 후 워킹 셋 집합 W(T2, 5) = { 1, 2, 9 }             |
  |   -> OS의 조치: "5번 페이지는 안 쓰니까 버리고(회수), 9번 페이지를 채워라!" |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 이 그림은 지역성(Locality)이 멈춰있는 것이 아니라, 프로그램의 코드 흐름에 따라 계속 '이동'한다는 것을 보여준다(Transition). 루프 A를 돌 때는 {1, 2, 5}번 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 미친 듯이 보다가, 함수를 빠져나와 다른 로직 B로 넘어가면 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 자체가 {1, 2, 9}로 물 흐르듯 바뀐다. 운영체제의 VMM([가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 관리자)은 이 변화하는 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)의 덩치(WSS, [Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/) Size)를 실시간으로 측정하여, 덩치가 커지면 RAM 공간을 더 배급해 주고(고무줄 늘리기), 덩치가 작아지면 잉여 램을 즉각 빼앗아 다른 굶주린 앱에게 던져준다. 이 유동적인 밥그릇 조절이 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)을 막는 방파제다.

- **📢 섹션 요약 비유**: 이삿짐센터 직원이 방을 옮겨 다니며 일할 때, 안방에서 청소할 때는 빗자루와 걸레([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))만 계속 쓰고, 화장실을 청소할 때는 락스와 솔(새로운 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))만 계속 씁니다. 직원의 손에 그 순간 꼭 필요한 도구들만 쥐여주고 필요 없는 도구는 당장 뺏어서 트럭에 던져버리는 치밀한 도구 관리법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 윈도우 사이즈 ($\Delta$) 튜닝의 거대한 딜레마

[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 이론의 모든 약점은 "과거의 시간($\Delta$)을 얼마나 길게 볼 것인가?"라는 단 하나의 파라미터로 귀결된다. 이 창문의 크기가 서버 전체의 생사를 가른다.

| 윈도우 사이즈 ($\Delta$) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 관측 결과 및 현상 | 시스템에 미치는 치명적 결과 (Trade-off) |
|:---|:---|:---|
| **너무 작게 잡음 (예: $\Delta = 2$)** | 앱이 쓰는 진짜 필수 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)조차 다 못 담음 (WSS가 너무 작게 나옴) | 필수 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 계속 뺏기고(Eviction) 다시 불려오는 <strong>무한 <a href="/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/">페이지 폴트</a>(<a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">Thrashing</a>) 지옥 발생</strong>. |
| **적정 수준의 $\Delta$** | 그 앱의 루프(지역성)를 덮을 만큼 딱 적당한 양만 산출됨 | 캐시 낭비 없이 쾌적하게 동작. [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) 제로 달성. |
| **너무 크게 잡음 (예: $\Delta = \infty$)**| 수 시간 전에 쓰고 버린 쓰레기 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)까지 모조리 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)으로 간주함 | WSS가 비대해져서 램을 쓸데없이 독식함. <strong>동시에 띄울 수 있는 프로그램 숫자(<a href="/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/">다중 프로그래밍 정도</a>)가 극단적으로 떨어짐</strong>. |

### [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과의 융합

실제 상용 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 "최근 1만 번의 메모리 참조를 매번 감시"하는 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 원형을 그대로 코딩하면, 감시하느라 CPU 100%를 다 써서 서버가 죽어버린다. 그래서 리눅스와 윈도우는 이 철학을 꼼수로 가볍게 흉내 낸 <strong><a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/">PFF</a> (<a href="/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/">페이지 부재 빈도</a>)</strong> 모델을 쓴다.

```text
  +-------------------------------------------------------------------+
  |                 PFF (Page Fault Frequency) 기반 동적 프레임 조절 메커니즘 |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ 특정 프로세스(A)의 초당 페이지 폴트(하드 디스크 긁는 횟수) 감시 ]         |
  |                                                                   |
  |           (스래싱 경계선) 상한 임계치 (Upper Bound) - 예: 초당 50번      |
  |  ======================= 💥 선 넘음! 💥 ========================  |
  |             ^               |                                     |
  |             | 너무 자주 긁음   v [OS 조치]                          |
  |   폴트율(PFF) | (RAM 부족함)   "방이 좁아서 계속 디스크 긁네! 방 2개 더 줘!"|
  |             |               (프레임 할당량 동적 증가 📈)              |
  |             |                                                     |
  |   ---------+---------------------------------------------------   |
  |             | (적정 구간: 쾌적함)                                    |
  |  ======================= 💤 선 밑으로 내려감 =====================  |
  |             v 폴트율이 너무 낮음 (RAM 남아돔)                         |
  |                           [OS 조치]                               |
  |                           "폴트가 거의 없네? 얘 지금 램 처남아도나 보네?" |
  |                           "방 2개 강제로 뺏어서 딴 놈 줘버려!"           |
  |                           (프레임 할당량 강제 회수 📉)              |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** PFF는 천재적인 타협안이다. 메모리에 닿는 모든 손길을 감시하는 대신, "사고가 났을 때([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/))만" 체크한다. 상한선(Upper Bound)을 넘으면 이 프로세스의 밥그릇(프레임)이 너무 작아 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)이 나기 직전이라는 뜻이므로 밥그릇을 늘려준다. 하한선(Lower Bound) 밑으로 떨어지면 밥그릇이 너무 넓어서 잉여 공간을 낭비하고 있다는 뜻이므로 무자비하게 밥그릇을 빼앗아버린다. 이 고무줄 같은 할당(Dynamic Allocation) 덕분에 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 CPU 오버헤드를 극소화하면서 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 철학을 99% 흉내 내는 성과를 거두었다.

- **📢 섹션 요약 비유**: 선생님이 아이들이 풀고 있는 시험지 여백을 일일이 쳐다보는 게(순수 워킹셋) 아니라, 아이가 "선생님 종이 모자라요!"라고 손을 들 때([페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)) 손을 너무 자주 들면(상한선 초과) 연습장을 아예 10장 뭉텅이로 던져주고, 30분 동안 손을 한 번도 안 들면(하한선 밑) 책상에 널려있는 연습장을 싹 다 뺏어가는(프레임 회수) 영리한 고효율 감독법입니다.

---

## Ⅲ. 비교 및 연결

### 3대 [페이지 교체 알고리즘](/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/) ([LRU](/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) vs [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) vs [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/))

아키텍트는 이 3가지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 램(RAM)이라는 자본주의 시장을 어떻게 통제하는지 봐야 한다.

| 철학 및 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 대체 대상을 고르는 기준 (누굴 쫓아낼 것인가) | 장점 및 단점 |
|:---|:---|:---|
| <strong><a href="/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a> (가장 오래전 사용)</strong> | 글로벌 경쟁. "니가 누구 앱이든 상관없이 시스템 전체에서 가장 오래 안 쓴 놈 방 빼!" | 구현이 쉽고 보편적이나, A앱의 램을 무고한 B앱이 빼앗아버려 국지적 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)을 유발함. |
| <strong><a href="/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a> 모델</strong> | 로컬 격리. "내 과거의 족적($\Delta$) 안에 없는 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 쓰레기니까 내 방에서 나가!" | 프로그램의 논리적 실행 흐름을 가장 완벽히 보장함. 단, 타이머 돌려가며 족적을 체크하는 CPU 비용이 극악임. |
| <strong><a href="/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/">PFF</a> (<a href="/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/">페이지 폴트</a> 빈도)</strong> | 실전 타협. "디스크 긁는 빈도(에러)가 적은 앱의 방을 뺏어서, 많이 긁는 앱에게 줘!" | 에러(Fault) 이벤트만 카운트하므로 매우 가볍지만, 앱이 갑자기 새로운 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)으로 이사 갈 때 순간적인 렉을 막을 순 없음. |

### 과목 융합 관점

- <strong><a href="/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> (<a href="/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 킬러와 <a href="/studynote/02_operating_system/06_memory_management/335_swapping/">스와핑</a> <a href="/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a>)</strong>: [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 이론의 궁극적 결론은 참혹하다. 만약 시스템에 켜진 모든 앱들의 "[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)(WSS) 총합"이 호스트의 "물리 램(RAM) 총용량"보다 커진다면? 그 어떤 신의 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 가져와도 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)을 멈출 수 없다(디스크가 미친 듯이 갈린다). 이때 OS 아키텍트는 튜닝을 포기하고 무조건 스왑(Swap) 파티션의 모가지를 잘라버린 뒤(Swapoff), <strong><a href="/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 킬러</strong>를 깨워 무거운 프로세스 하나의 목을 쳐버림으로써 남은 WSS 총합을 물리 램 이하로 강제 진압해야 한다.
- <strong>클라우드 <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 자원 제어 (<a href="/studynote/02_operating_system/01_overview_architecture/062_cgroups/">Cgroups</a> v2 메모리 <a href="/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/">QoS</a>)</strong>: 쿠버네티스에서 Cgroups의 `memory.min`과 `memory.low` 파라미터는 바로 이 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 이론을 하드웨어 격리에 이식한 것이다. `memory.min`에 1GB를 주면, OS는 "이 앱의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)이 1GB는 무조건 필요하구나"라고 인지하여, 아무리 호스트 램이 부족해도 이 1GB만큼은 절대 스왑 영역으로 쫓아내지 않고 콘크리트처럼 지켜주어 앱의 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 방어한다.

- **📢 섹션 요약 비유**: LRU가 "가장 오랫동안 빈방 빼라"는 자본주의식 무한 경쟁이라면, [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)은 "각 가족의 필수 생계 공간(WSS)만큼은 절대로 침범하지 마라"는 복지 국가의 최저 생계비 보장 정책과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 트러블슈팅

1. <strong>시나리오 — AWS EC2 (Java Spring) 환경의 워밍업(Warm-up) <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> 현상</strong>: [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))으로 새로 뜬 서버가 트래픽을 받자마자, 응답 속도([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))가 2초씩 튀면서 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 에러를 뿜다가 10분이 지나서야 10ms로 평온해진다.
   - **원인 분석**: 새로 뜬 JVM 프로세스는 메모리에 아무런 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(클래스 캐시, DB 커넥션 풀)가 안 올라와 있는 콜드(Cold) 상태다. 즉, <strong><a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>(<a href="/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>)이 램에 전혀 형성되지 않은 상태</strong>다. 트래픽이 쏟아지면 JVM은 억지로 클래스 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))을 RAM으로 끌어올리느라 초당 수만 번의 거대한 [페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 폭주([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/) Storm)를 맞으며 시스템 콜 오버헤드로 인해 스로틀링(Throttling)이 걸린다.
   - **아키텍트 판단 (가짜 트래픽 워밍업 투입)**: 로드밸런서(ALB) 설계 시, 새 서버가 떴다고 바로 유저 트래픽을 100% 꽂으면 안 된다. 서버가 뜨면 백그라운드 스크립트나 K8s의 Readiness Probe를 이용해 내부적으로 가짜 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출을 1만 번 정도 때려서 JVM의 주요 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 메모리가 RAM에 안착(Warm-up)되게 만들어야 한다. [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 윈도우가 꽉 찬 것을 100% 확인한 후에 유저 트래픽 밸브를 열어야(Traffic [Routing](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)) 제로 레이턴시 무중단 배포가 완성된다.

2. <strong>시나리오 — Windows Server / MSSQL의 <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a> 독식으로 인한 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a> 솔루션 마비</strong>: 윈도우 환경에서 MSSQL DB를 띄우면 램이 128GB라도 DB가 120GB를 먹어치운다. 문제는 밤 12시에 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 프로그램이 돌면 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 프로그램이 쓸 램이 부족해서 디스크 [스와핑](/studynote/02_operating_system/06_memory_management/335_swapping/) 지옥에 빠져 서버가 멈춘다.
   - **원인 분석**: 윈도우 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 VMM은 `SetProcessWorkingSetSize`라는 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 강제 통제 API를 가진다. MSSQL은 속도를 위해 OS에게 "내 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)은 120GB다. 아무도 이 램을 뺏지 마라"라고 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/))을 걸어버린 상태다. 남은 8GB로 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 프로그램이 돌려니 [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/)([페이지 폴트](/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 빈도)가 폭발한 것이다.
   - **아키텍트 판단 (Max Server Memory 제한)**: DB는 자본주의의 괴물이라 놔두면 램의 99%를 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)으로 집어삼킨다. 아키텍트는 MSSQL [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)에 들어가 `Max Server Memory` 파라미터를 물리 램의 80%(예: 100GB)로 강제로 깎아내려 캡([Cap](/studynote/13_cloud_architecture/05_data_engineering/341_process/))을 씌워야 한다. 남은 20GB의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 공간을 OS와 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 데몬, 보안 에이전트들이 여유롭게 쓸 수 있게 숨통을 열어주는 것이 인프라 기본 세팅이다.

```text
  +-------------------------------------------------------------------+
  |                 메모리 스래싱(Thrashing) 대응을 위한 아키텍트 결정 트리     |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ 서버 모니터링: `vmstat` 명령에서 `si(Swap in)` / `so(Swap out)` 폭주 중! ]|
  |                |                                                  |
  |                v                                                  |
  |      전체 RAM 용량이 돌고 있는 프로세스들의 `워킹 셋(WSS) 총합`보다 작은가?      |
  |          +- 예 ------> 🚨 [ 물리적 한계 도달 (Global Thrashing) ]    |
  |          |             -> 스케줄러 튜닝 불가! 하드웨어 RAM 증설 필수!        |
  |          |             -> 급한 불: 트래픽을 타 노드로 돌리거나 OOM 강제 킬.  |
  |          +- 아니오 (RAM은 분명히 40%나 남아도는 상황임)                  |
  |                |                                                  |
  |                v                                                  |
  |      특정 프로세스가 Cgroups Limit이나 ulimit 한도에 부딪혀 국지적 스래싱을 치는가?|
  |          +- 예 ------> [ Local Thrashing (Cgroups 병목) ]           |
  |          |             -> 해당 컨테이너의 Memory Limit 설정(YAML)을 증량 튜닝.|
  |          |                                                        |
  |          +- 아니오 ---> [ 불규칙한 거대 파일 I/O에 의한 페이지 캐시 오염! ] |
  |                        -> `vfs_cache_pressure` 올려서 파일 캐시 빨리 버리게 튜닝.|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)의 무서운 진실은, 램 용량이 남아돌아도 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)이 터질 수 있다는 점이다. 최근의 [Cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 격리 환경에서는, 노드 램이 100GB가 남아도 특정 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))에 Limit을 2GB로 묶어두었는데 그 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)의 앱이 3GB어치 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)(자주 도는 루프의 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기)을 가지고 있다면, 그 좁은 감방 안에서 혼자 미친 듯이 디스크를 긁으며 스왑인/아웃을 반복한다(Local [Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/)). 아키텍트는 글로벌 자원 여유도에 속지 말고, 앱의 본질적 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 크기([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/) Size)를 프로파일링하여 그 크기보다 Limit을 넉넉히(Slack) 주어야 렉을 없앨 수 있다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>배치(Batch) 프로그램의 <code>mmap</code> 남용</strong>: [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 10GB 전체를 분석하는 1회성 파이썬 배치 스크립트를 짜면서, 빠르다는 소문을 듣고 `mmap` ([메모리 맵 파일](/studynote/02_operating_system/02_process_thread/131_mmap_ipc/))을 돌리는 주니어의 실수. `mmap`은 내가 읽은 공간을 메모리 램([페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 캐시)에 통째로 우겨 넣는다. 문제는 배치 스크립트는 한 번 읽은 곳을 다시는 안 읽는 "[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)이 0인 무한 전진 로직"이라는 점이다. OS는 이 쓰레기 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 지키려고 진짜 DB 서버의 소중한 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 스왑(디스크)으로 쫓아내 버린다. 한 번만 스캔하는 거대한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 무조건 `read()`에 캐시를 안 쓰는 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)([O_DIRECT](/studynote/02_operating_system/09_file_system/565_o_direct_io_bypass_cache/) 등)를 주거나 `madvise(MADV_DONTNEED)` 힌트를 줘서 메모리를 오염시키지 말고 즉각 버려야 한다.

- **📢 섹션 요약 비유**: 식탁(RAM) 위에서 평생 먹을 맛있는 밥상([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/))을 쫙 깔아놨는데, 잠깐 지나가는 택배 기사(배치 프로그램)가 자기 짐 100상자(10GB)를 식탁 위에 다 올리겠다고 소중한 밥그릇을 다 바닥에 밀어 던져버리는 만행입니다. 택배는 식탁을 거치지 않고 바로 바닥을 통해 베란다로 지나가게([Direct](/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) I/O) 설계해야 합니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 고정 [프레임 할당](/studynote/02_operating_system/07_virtual_memory/397_frame_allocation/) ([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 무시) | [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 동적 윈도우 모델 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/studynote/02_operating_system/07_virtual_memory/387_page_fault/">Page Fault</a> 횟수)</strong>| 잦은 문맥 전환 시 초당 수천 번 캐시 미스 폭발 | 앱의 핵심 크기 보장으로 폴트율 99% [억제](/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) | 디스크 I/O 스톨(Stall) 제거로 앱 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 수백 배 단축 |
| **정량 (CPU 유효 연산률)**| 스왑(Swap) 대기 하느라 CPU 사용률 0% 추락 | RAM 내 연산 집중으로 CPU 점유율 100% 확보| 시스템 전체의 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 스루풋(TPS) 붕괴 방어 |
| <strong>정성 (<a href="/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/">다중 프로그래밍</a>)</strong> | 무조건 크게 줘서 몇 개 못 띄움 | 필요한 놈은 더 주고, 노는 놈은 뺏어옴 | 물리적 한계 내에서 동시에 띄울 수 있는 프로세스 개수 극대화 |

### 미래 전망
- <strong><a href="/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a>(ML) 기반의 <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a> 예측기</strong>: 기존 [PFF](/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 모델은 사고([Page Fault](/studynote/02_operating_system/07_virtual_memory/387_page_fault/))가 나야 밥그릇을 늘려주는 사후약방문 방식이다. 최근 메타(Facebook) 같은 초거대 인프라에서는 아예 앱 실행 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)으로 분석해, "매일 밤 11시면 이 서비스의 트래픽 패턴상 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)이 3GB에서 10GB로 폭증한다"는 것을 예측(Predictive)하고, 폴트가 터지기도 전에 미리 여분 램을 옆구리에 찔러넣어 주는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 선제적 메모리 튜닝(Proactive [Memory Management](/studynote/09_security/uncategorized/1040_memory_management/)) 시대로 넘어가고 있다.
- <strong>TMO (Transparent Memory <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/">Offloading</a>)</strong>: 램이 모자랄 때 단순히 디스크로 쫓아내는 게 아니라, [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 램(zRAM) $\rightarrow$ 고속 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) $\rightarrow$ 클라우드 [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 원격 메모리(다른 서버의 남는 램) 순으로 층위를 두어 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)에서 살짝 멀어진 '미적지근한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'를 네트워크 너머로 투명하게 이주시켜 램 한계를 무제한으로 확장하는 메타(Meta)의 TMO [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 아키텍처가 미래 리눅스의 표준을 씹어먹고 있다.

### 참고 표준
- <strong>피터 데닝(Peter J. Denning)의 <a href="/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a> 정리 (1968)</strong>: 컴퓨터 공학 역사상 가장 위대한 논문 중 하나로, [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)의 수학적 모델을 정립하여 현대 OS [페이징](/studynote/02_operating_system/04_synchronization/259_paging/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 기초 헌법이 된 이론.
- <strong>POSIX <code>madvise()</code> / <code>fadvise()</code></strong>: 개발자가 OS의 [워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 대고 "이 메모리는 곧 쓸 거니까 뺏지 마(WILLNEED)" 또는 "이건 다 썼으니 제발 빨리 회수해 가(DONTNEED)"라고 힌트를 찔러넣어 윈도우 사이즈를 수동 통제하는 유닉스 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 표준.

[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)([Working Set](/studynote/02_operating_system/04_synchronization/265_working_set/))과 윈도우 사이즈 조절은, 한정된 자본(RAM)을 놓고 벌어지는 수많은 프로세스 간의 피 튀기는 만인에 대한 투쟁을 운영체제가 어떻게 '가장 자본주의적으로, 그러나 가장 합리적으로' 통제하는지 보여주는 정치경제학의 극치다. 필요 없는 놈의 피 같은 자원을 가차 없이 빼앗아, 당장 일하고 있는 가장 절박한 놈의 손에 몰아줌으로써 시스템 전체의 붕괴([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/))라는 파국을 막는다. 결국 OS의 메모리 관리란 도덕적 평등이 아니라, 철저하게 "지금 이 순간 톱니바퀴를 가장 빠르게 굴릴 놈(Locality)에게 힘을 몰아주는" 차가운 생존의 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

- **📢 섹션 요약 비유**: 우산 10개(메모리 프레임)가 있을 때, 맑은 날엔 10명에게 공평하게 우산을 나눠주고 들고 다니게 하는 건 비효율의 극치입니다. 비가 오기 시작한 1명([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 폭발)에게 모든 우산을 집중시켜 물건이 젖는 것([스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/) 에러)을 막고, 비가 그치면 즉각 우산을 뺏어 다시 창고에 넣는 융통성만이 인프라를 구원합니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [락 엘리전](/studynote/02_operating_system/04_synchronization/270_lock_elision/) 하드웨어 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 메모리 활용 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [RCU](/studynote/02_operating_system/04_synchronization/254_rcu_read_copy_update/) 다중 독자 락 프리 고성능 기법 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 컬러링 캐시 경합 회피 물리 할당 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [틱리스 커널](/studynote/02_operating_system/11_exam_summary/795_tickless_kernel_mobile_battery_preservation/)([Tickless](/studynote/02_operating_system/11_exam_summary/795_tickless_kernel_mobile_battery_preservation/)) 모바일 배터리 보존 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[RCU 다중 독자 락 프리 고성능 기법]
    |
    v
[워킹 셋 윈도우 사이즈 동적 조절 (Working Set Window Size Dynamic Adjustment)]
    |
    +---> [페이지 컬러링 캐시 경합 회피 물리 할당]
    +---> [틱리스 커널(Tickless) 모바일 배터리 보존]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수가 책상(메모리)에서 레고를 조립할 때, 수만 개의 레고 블록 중 지금 당장 만들고 있는 '자동차 바퀴 부품 10개'가 있어요. 이걸 '[워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/)'이라고 불러요.
2. 멍청한 엄마(구형 OS)는 철수가 바퀴를 조립하는데 뜬금없이 성벽 부품을 책상에 쏟아놓고 바퀴 부품을 상자에 치워버려서, 철수가 부품 찾느라 울고불고 난리가 났죠([스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)).
3. 똑똑한 엄마([워킹 셋](/studynote/02_operating_system/04_synchronization/265_working_set/) 관리자)는 철수가 최근 5분([윈도우 크기](/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/)) 동안 계속 만지작거린 부품 10개를 딱 파악하고, 그 10개만큼은 절대 서랍에 넣지 않고 눈앞에 잘 챙겨줘서 철수가 자동차를 1초 만에 완성하게 도와준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 793 / 800

<- **이전**: [792. RCU 다중 독자 락 프리 고성능 기법 (Rcu Read Copy Update Lock Free)](/studynote/02_operating_system/11_exam_summary/792_rcu_read_copy_update_lock_free/)
**다음**: [794. 페이지 컬러링 캐시 경합 회피 물리 할당 (Page Coloring Cache Conflict Avoidance)](/studynote/02_operating_system/11_exam_summary/794_page_coloring_cache_conflict_avoidance/) ->

---
