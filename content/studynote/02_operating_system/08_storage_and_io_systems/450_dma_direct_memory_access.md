---
title: 450. 직접 메모리 접근 (DMA, Direct Memory Access) - CPU 개입 없이 장치와 메모리 간 직접 데이터 전송
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 직접 메모리 접근([[746_io_direct_memory_access_dma|DMA]])은 디스크나 랜카드에서 램(RAM)으로 [[001_dikw_pyramid|데이터]]를 퍼 나를 때 가장 비싼 자원인 CPU가 1바이트씩 땀 흘려 옮기는 멍청한 노가다를 금지하고, **'[[746_io_direct_memory_access_dma|DMA]] 컨트롤러'라는 전담 하청 칩셋을 보드에 달아 CPU 몰래(개입 없이) 메모리에 [[001_dikw_pyramid|데이터]]를 다이렉트로 때려 박는 하드웨어 우회 기술**이다.
> 2. **가치**: 1GB짜리 영화를 디스크에서 램으로 올릴 때 발생하는 '10억 번의 [[016_interrupt_mechanism|인터럽트]] 렉'과 'CPU 100% 점유율 폭발'을 단 한 번의 [[016_interrupt_mechanism|인터럽트]]로 뭉뚱그려버려, **CPU는 연산(게임, 웹서핑)에 100% 몰빵하고 무거운 짐 나르기는 하청업체가 끝내버리는 극한의 [[675_multitasking_terminology_preemptive|멀티태스킹]] 스루풋([[139_throughput|Throughput]])을 달성**한다.
> 3. **융합(한계)**: DMA가 램으로 짐을 나르는 동안 CPU도 램을 써야 하므로 필연적으로 메모리 [[344_bus|버스]] 충돌이 발생하는데, 이를 해결하기 위해 **[[451_cycle_stealing|사이클 스틸링]]([[451_cycle_stealing|Cycle Stealing]])** 꼼수와 찢어진 [[381_virtual_memory|가상 메모리]]를 한 번에 긁어오는 **산란-수집([[452_dma_scatter_gather|Scatter-Gather]])** 기법으로 융합 진화하여 현대 PCI-e [[344_bus|버스]]의 심장이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 메인보드에 납땜 되어 있는 독립된 미니 프로세서([[746_io_direct_memory_access_dma|DMA]] Controller)다. CPU가 얘한테 "디스크 500번지부터 10MB 퍼와서, 램 0x1000번지에 꽂아넣어. 다 되면 나한테 딱 1번만 삐삐([[016_interrupt_mechanism|인터럽트]]) 쳐!"라고 지시서([[271_command_pattern|Command]])만 던져주면, DMA는 알아서 메모리 [[344_bus|버스]]를 장악하고 밤새도록 디스크와 램 사이의 [[001_dikw_pyramid|데이터]]를 실어 나른다. 그동안 CPU는 뒤도 안 돌아보고 자기 할 일(포토샵 렌더링 등)을 하러 떠난다.
- **필요성**: 앞 장에서 칭찬했던 '[[016_interrupt_mechanism|인터럽트]] 구동 I/O'도 엄청난 맹점이 있었다. 디스크에서 [[001_dikw_pyramid|데이터]]가 1바이트 도착할 때마다 [[016_interrupt_mechanism|인터럽트]]를 치면, CPU는 1바이트 줍고 딴일 하다가, 0.001초 뒤에 1바이트 줍고 딴일 하는 **미친 왕복 달리기([[211_context_switch|Context Switch]])**를 해야 했다. 만약 [[148_5g_embb_urllc_mmtc|초고속]] [[482_nvme|NVMe]] SSD로 1GB를 옮긴다면 1초에 10억 번의 [[016_interrupt_mechanism|인터럽트]] 폭풍을 맞고 CPU가 거품을 물고 뻗어버린다([[315_livelock_vs_deadlock|Livelock]]). "아니 씨, 이 단순 무식한 짐 나르기를 제일 비싼 인재인 CPU가 직접 해야 해? 택배기사([[746_io_direct_memory_access_dma|DMA]]) 한 명 고용해서 창고에 다 쌓아두고 마지막에 사인만 받으면 안 돼?"라는 분노가 [[127_system_bus|시스템 버스]] 구조를 통째로 뜯어고친 DMA를 낳았다.

- **등장 배경 및 아키텍처의 권력 [[136_variance|분산]]**:
  1. **PIO(Programmed I/O)의 한계**: CPU가 [[344_bus|버스]]([[344_bus|Bus]])를 통해 1워드(4바이트)씩 읽어오는 방식이 대용량 통신(랜카드/디스크)에서 병목으로 터짐.
  2. **[[344_bus|버스]] 마스터링([[344_bus|Bus]] Mastering)의 도입**: CPU만이 가지고 있던 "메모리 [[344_bus|버스]]에 전기를 쏠 수 있는 특권(마스터 권한)"을 제3의 하드웨어 칩셋([[746_io_direct_memory_access_dma|DMA]])에게 쥐여주는 권력의 [[136_variance|분산]]이 일어남.
  3. **[[566_mmap_zero_copy_sendfile|Zero-Copy]] 철학의 태동**: CPU의 레지스터를 거치지 않고 디스크 -> 램으로 직통 웜홀이 뚫리면서, 현대 I/O 가속화의 가장 기본 뼈대가 완성됨.

```text
┌───────────────────────────────────────────────────────────────────────┐
│        DMA 유무에 따른 10MB 파일 복사(I/O) 파이프라인의 끔찍한 차이   │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│ ▶ 1. 낡은 PIO (Programmed I/O - DMA 없음)                             │
│   [ 디스크 ] ──1바이트──▶ [ CPU 레지스터 ] ──1바이트──▶ [ RAM ]       │
│   - CPU가 1바이트 옮길 때마다 루프 돎 + 인터럽트 터짐.                │
│   💥 결과: 10MB 옮기는 데 CPU 100% 폭주. 화면 멈추고 마우스 안 움직임.│
│                                                                       │
│ ▶ 2. 구원자 DMA (Direct Memory Access)                                │
│   CPU: (명령서 작성) "DMA야, 디스크 10MB 램으로 좀 옮겨놔라."         │
│   CPU ──▶ 넷플릭스 4K 영상 디코딩 하러 휙 떠남. (점유율 0%로 떨어짐)  │
│                                                                       │
│   [ 디스크 ] ──(CPU 몰래 고속 버스로 통짜 10MB 전송)──▶ [ RAM ]       │
│   (전송 완료 후) DMA 칩 ──💥 1번의 인터럽트 ──▶ [ CPU ]               │
│   CPU: "오 다 옮겼어? 땡큐." (수천만 번의 렉을 1번의 인터럽트로 퉁침) │
└───────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** 이 그림은 현대 컴퓨터가 왜 영화를 10GB 복사하는 와중에도 게임이 렉 없이 부드럽게 돌아갈 수 있는지에 대한 가장 근본적인 해답이다. 10GB의 [[001_dikw_pyramid|데이터]]를 메모리로 퍼 올리는 물리적 중노동을 순수하게 메인보드의 노예 칩([[746_io_direct_memory_access_dma|DMA]])이 독박 쓰고, CPU는 그 짐에 손가락 하나 대지 않기 때문에 완벽한 [[675_multitasking_terminology_preemptive|멀티태스킹]] UX가 성립하는 것이다.

- **📢 섹션 요약 비유**: 옛날엔 은행원(CPU)이 창구에서 손님(디스크)이 던져주는 동전 100만 개([[001_dikw_pyramid|데이터]])를 손으로 1개씩 세어 금고(램)에 넣느라 하루 종일 딴 손님을 못 받았습니다. 지금은 동전 계수기([[746_io_direct_memory_access_dma|DMA]]) 기계에 돈을 와르르 붓고 스위치만 켜놓으면, 기계가 다 세고 나서 띠링!([[016_interrupt_mechanism|인터럽트]]) 울릴 때까지 은행원은 뒤에서 편하게 다른 손님 대출 서류(연산)를 처리하는 눈부신 자동화 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 메모리 [[344_bus|버스]] 쟁탈전과 "[[451_cycle_stealing|사이클 스틸링]]([[451_cycle_stealing|Cycle Stealing]])"

아무리 천재적인 DMA라도 치명적인 구조적 모순이 하나 있다. 컴퓨터 메인보드에 깔린 **메모리로 향하는 고속도로([[127_system_bus|시스템 버스]])는 오직 딱 1차선**이라는 것이다.
- CPU가 포토샵을 하느라 램에서 [[001_dikw_pyramid|데이터]]를 퍼가고 있다 ([[344_bus|버스]] 사용 중).
- DMA도 램에 10MB를 집어넣어야 한다 ([[344_bus|버스]] 사용 요구).
- 1차선 도로 양쪽에서 차가 밀고 들어오면 쾅 부딪힌다. 이 충돌을 어떻게 조율할까?

**[해결책: [[451_cycle_stealing|사이클 스틸링]] 꼼수]**
- 평소엔 킹왕짱 CPU가 [[344_bus|버스]]를 마음대로 점유한다.
- 하지만 DMA가 짐을 램에 한 삽 퍼부어야 할 순간이 오면, 메모리 컨트롤러(경찰)에게 윙크를 한다.
- 컨트롤러는 CPU가 아주 찰나의 순간 동안 램을 안 쓰고 연산부([[117_alu|ALU]]) 안에서 혼자 생각만 하고 있는(디코드 등) 딱 1 클럭(Cycle)의 빈틈을 포착한다.
- 그 1 클럭 동안 **DMA가 CPU의 [[344_bus|버스]] 사용 권한을 0.001초 훔쳐서(Stealing) 램에 짐을 푹 던져놓고 튄다.**
- CPU 입장에서는 [[344_bus|버스]]를 빼앗겨 아주 미세하게 1클럭 늦어지긴 하지만, 자기가 직접 짐을 나르는 노가다(PIO)에 비하면 속도 저하가 새 발의 피 수준이라 기분 좋게 도둑질을 눈감아준다.

---

### [[320_burst_mode|Burst Mode]] ([[320_burst_mode|버스트 모드]])의 폭주

만약 [[451_cycle_stealing|사이클 스틸링]]으로 눈치 보며 1바이트씩 넣다가는, 100Gbps 랜카드로 쏟아지는 트래픽을 도저히 소화할 수 없다. 
- **[[320_burst_mode|Burst Mode]]**: 눈치고 뭐고 DMA가 "나 급하니까 다 비켜!!!" 하고 [[127_system_bus|시스템 버스]]를 **통째로 장악([[510_lock|Lock]])**해 버린다.
- 한 번 [[344_bus|버스]]를 잡으면 10MB 덩어리가 끝날 때까지 CPU를 길바닥에 세워두고 지가 [[001_dikw_pyramid|데이터]]를 램에 다 쑤셔 박는다.
- 전송 속도는 우주 최강으로 치솟지만, CPU는 캐시에 [[001_dikw_pyramid|데이터]]가 없으면 꼼짝없이 메모리 접근을 못 해 서버 전체가 일시적으로 버벅대는 렉(Jitter)을 동반한다. (실무 스토리지 튜닝의 핵심 지표다).

- **📢 섹션 요약 비유**: 왕복 1차선 골목길(메모리 [[344_bus|버스]])입니다. 사장님 차(CPU)가 주로 다니지만, 가끔 택배 트럭([[746_io_direct_memory_access_dma|DMA]])이 들어와야 합니다. 사장님이 집에서 잠깐 화장실 간 사이([[158_instruction|명령어]] 해독)에 택배 트럭이 1초 만에 휙 짐을 던지고 빠지는 게 **[[451_cycle_stealing|사이클 스틸링]]**이고, 택배가 너무 많아 사장님 차를 길 막아 세워두고 10분 동안 택배만 미친 듯이 내리는 게 **[[320_burst_mode|버스트 모드]]**입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 3대 하드웨어 I/O 통신 방식의 최종 결산

운영체제론의 근본을 묻는 3대 I/O 아키텍처 발전사.

| I/O 방식 | 동작 메커니즘 | CPU 노동 강도 (오버헤드) | 시스템 [[282_performance_tactics|성능]] 기여도 |
|:---|:---|:---|:---|
| **[[448_polling_programmed_io|폴링]] (PIO)** | CPU가 무한루프 돌며 짐 나름 | ☠️ 100% 점유율 폭발 | 다른 앱 올스톱. (극단적 하위 기기용) |
| **[[016_interrupt_mechanism|인터럽트]] 기반 I/O** | 딴일 하다가 부르면 와서 짐 나름 | 🔴 잦은 문맥 교환으로 피곤 | [[675_multitasking_terminology_preemptive|멀티태스킹]]은 되지만 대용량엔 뻗음 |
| **[[746_io_direct_memory_access_dma|DMA]] 기반 I/O** | **하청업체([[746_io_direct_memory_access_dma|DMA]])가 짐 다 나르고 1번만 부름** | 🟢 **거의 0% (최고 휴양지)** | **🚀 수백 기가바이트 쾌속 전송 (대세)** |

### 산란-수집 ([[452_dma_scatter_gather|Scatter-Gather]]) DMA의 흑마술
초창기 DMA는 치명적인 약점이 있었다. "램의 [[323_physical_address|물리 주소]] 공간이 연속(Contiguous)되어 있어야만 한 번에 퍼다 부을 수 있다"는 점이다.
- [[381_virtual_memory|가상 메모리]]를 쓰면 램이 4KB로 조각조각 찢어져 버린다([[259_paging|페이징]]).
- 12KB([[286_page_frame|페이지]] 3장)를 보내려면, 1번 방에 4K 쏘고 -> [[016_interrupt_mechanism|인터럽트]] 치고 다시 명령서 받아 -> 90번 방에 4K 쏘고 -> [[016_interrupt_mechanism|인터럽트]] 치고... 이렇게 바보같이 동작했다.
- **구원의 [[452_dma_scatter_gather|Scatter-Gather]] [[746_io_direct_memory_access_dma|DMA]]**: 현대 [[746_io_direct_memory_access_dma|DMA]] 칩셋은 램 안에 **[[056_linked_list|Linked List]](배송지 목록표)**를 읽을 지능을 탑재했다. 
- CPU가 "여기 1번 방 4K, 90번 방 4K, 15번 방 4K 배송지 3개 목록([[055_array|Array]]) 던져둔다. 네가 알아서 찢어진 방에 흩뿌려(Scatter) 넣거나, 흩어진 놈들을 하나로 수집(Gather)해서 와라!"
- DMA가 목록을 읽고 찢어진 램에 알아서 배달을 다 끝낸 뒤 단 1번의 [[016_interrupt_mechanism|인터럽트]]만 때린다. **[[381_virtual_memory|가상 메모리]](파편화)와 하드웨어(물리 전송)가 완벽하게 화해한 융합 기술의 정점이다.**

```text
┌──────────┬────────────┬────────────┬───────────────────────────────┐
│ DMA 수준   │ 물리 램 찢어짐 │ CPU 개입 횟수 │ 최적화 결과          │
├──────────┼────────────┼────────────┼───────────────────────────────┤
│ 기본 DMA │ 찢어지면 에러남│ 쪼개진 개수만큼│ 🔴 버벅댐 (구시대)    │
│ S-G DMA  │ 완전히 찢어짐 │ **단 1번 셋업**│ 🚀 **최강 (현대 표준)**│
└──────────┴────────────┴────────────┴───────────────────────────────┘
```
**[매트릭스 해설]** 리눅스 [[022_kernel_role|커널]] 소스코드를 까보면 디바이스 드라이버의 99%가 이 `dma_map_sg()` ([[452_dma_scatter_gather|Scatter-Gather]]) 함수로 떡칠되어 있다. 이 기능이 없다면 유저 프로그램이 mmap으로 찢어놓은 [[381_virtual_memory|가상 메모리]]에 10기가짜리 그래픽카드의 [[001_dikw_pyramid|데이터]]를 절대 다이렉트로 꽂아 넣을 수 없다.

- **📢 섹션 요약 비유**: 옛날 택배 기사(기본 [[746_io_direct_memory_access_dma|DMA]])는 주소가 다르면 본부(CPU)로 다시 돌아와서 새 송장을 받아가야 했습니다. 최신 S-G 택배 기사는 아예 "오늘 배송할 100군데 찢어진 동네 주소록([[056_linked_list|Linked List]])"을 스마트폰에 넣어주고 출발시키면, 하루 종일 알아서 다 배달하고(Scatter) 퇴근할 때 딱 한 번 보고하는 초지능형 배달 로직입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: Zero-Copy와 Sendfile() 시스템 콜의 기적
이 [[746_io_direct_memory_access_dma|DMA]] 기술은 백엔드 서버의 트래픽 비용을 1/100로 줄여준 위대한 최적화의 뼈대다.
1. **문제 상황 (과거의 [[501_file_definition_logical_record|파일]] 서빙)**:
   - 웹 서버(Nginx)가 영화 [[501_file_definition_logical_record|파일]](10GB)을 유저에게 인터넷으로 보내준다.
   - 디스크에서 램으로 `read()` -> [[022_kernel_role|커널]] 공간에서 유저 공간으로 램 복사(Memcpy) -> 유저에서 다시 [[022_kernel_role|커널]] [[125_socket|소켓]] 버퍼로 복사 -> 랜카드로 전송.
   - 무식한 램 복사(CPU 연산)가 2~4번 터지면서 서버 CPU가 100% 불타고 램 속도가 반토막 난다.
2. **[[746_io_direct_memory_access_dma|DMA]] 2단 콤보 (Zero-Copy의 완성)**:
   - 리눅스 형님들이 `sendfile()` 이라는 시스템 콜을 만들었다.
   - "OS야, 저기 하드디스크에 있는 10GB 영화를 바로 인터넷 랜카드([[125_socket|Socket]])로 좀 쏴줘."
   - 동작: **[디스크 [[746_io_direct_memory_access_dma|DMA]]]**가 램([[022_kernel_role|커널]] [[286_page_frame|Page]] Cache)으로 10GB를 조용히 쏴준다. CPU 복사 0회.
   - 그 직후, [[022_kernel_role|커널]] 버퍼에 뜬 [[001_dikw_pyramid|데이터]]를 유저 앱으로 복사하지 않고! 바로 **[랜카드 S-G [[746_io_direct_memory_access_dma|DMA]]]**에게 포인터 주소록만 띡 던져준다. 랜카드 DMA가 램에서 10GB를 자기가 알아서 훔쳐가 인터넷에 쏴버린다.
3. **결과**:
   - 10GB를 서비스하는데 **CPU가 [[001_dikw_pyramid|데이터]] 복사에 쓴 횟수 0회 ([[566_mmap_zero_copy_sendfile|Zero-Copy]])**. CPU 점유율 1% 미만으로 10G 대역폭을 풀로 쏴버리는 기적의 서버 튜닝이 탄생했다. [[506_cdn_content_delivery_network_edge_caching|CDN]](넷플릭스 캐시) 서버의 핵심 생존 기술이다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]: 캐시 코히런시 (Cache Coherency) 버그
DMA는 램(RAM)에 [[001_dikw_pyramid|데이터]]를 다이렉트로 꽂는다. 그런데 CPU의 L1/L2 캐시(수첩)에는 예전 [[001_dikw_pyramid|데이터]]가 남아있다! 
만약 CPU가 램을 읽으려 할 때 램까지 안 가고 자기 옛날 캐시를 믿고 읽어버리면? 방금 전 DMA가 랜카드에서 받아 적어놓은 램의 따끈따끈한 새 [[001_dikw_pyramid|데이터]]를 못 읽고 옛날 쓰레기값을 읽어 앱이 터져버린다(Cache Stale).
그래서 실무 [[022_kernel_role|커널]] 해커들은 DMA를 쏠 때, 무조건 해당 램 주소를 **캐시 불가능(Uncacheable)**으로 막아버리거나 전송 직후 강제로 캐시를 날려버리는(Cache Invalidate) 끔찍하고 예민한 어셈블리 튜닝을 해야만 한다. 

- **📢 섹션 요약 비유**: 사장님(CPU) 수첩(L1 캐시)에 통장 잔고가 100만 원이라 적혀 있습니다. 은행([[746_io_direct_memory_access_dma|DMA]])이 돈을 쏴서 진짜 통장(RAM)엔 200만 원이 입금됐는데, 사장님은 자기 낡은 수첩만 맹신하고 계속 100만 원이라고 착각하는 사고(캐시 불일치)입니다. 그래서 은행이 입금([[746_io_direct_memory_access_dma|DMA]])을 하면 무조건 사장님 수첩을 강제로 뺏어 찢어버리게(캐시 무효화) 법을 만들어야 회사가 돌아갑니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **CPU 가동률([[139_throughput|Throughput]]) 로켓 상승**| 수백 기가의 I/O [[001_dikw_pyramid|데이터]] 셔틀 노동을 하청([[746_io_direct_memory_access_dma|DMA]])으로 넘김으로써, CPU가 온전히 애플리케이션의 비즈니스 로직(연산)에만 100% 헌신 |
| **[[566_mmap_zero_copy_sendfile|Zero-Copy]] 아키텍처의 완성** | 디스크, RAM, 랜카드를 잇는 삼각형 통신망에서 CPU의 개입을 원천 배제하여, 서버의 초당 트래픽(Gbps) 한계를 기계적 한계치까지 확장 |
| **비동기 I/O 생태계의 물리적 기반**| 짐 싣고 1번만 알람을 준다는 특성 덕분에, `epoll`이나 `io_uring` 같은 최신 [[142_event_loop|이벤트 루프]] 시스템이 숨 쉬고 돌아갈 수 있는 물리적 토대 제공 |

### 결론 및 미래 전망

직접 메모리 접근 ([[746_io_direct_memory_access_dma|DMA]]) 기술은 중앙 집권적인 왕정(CPU 독재) 체제였던 컴퓨터 아키텍처에, 전문 관료제(독립 컨트롤러)라는 지방 분권을 이룩한 1등 공신이다. 세상 모든 일이 왕(CPU)의 결재와 손을 거쳐야 했다면 컴퓨터의 속도는 1980년대 펜티엄 시절에 성장을 멈췄을 것이다. DMA의 발명은 "연산하는 놈과 짐 나르는 놈은 분리해야 한다"는 [[344_bus|버스]] 마스터링([[344_bus|Bus]] Mastering)의 시대를 열어, 오늘날 NVMe와 400G [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]] 카드가 미친 듯이 램을 유린하는 속도전의 빗장을 풀었다. 향후 [[639_rdma_kernel_bypass|RDMA]] (Remote [[746_io_direct_memory_access_dma|DMA]]) 기술이 보편화되면, 내 컴퓨터의 램뿐만 아니라 네트워크 너머 남의 서버 램에까지 CPU 개입 없이 다이렉트로 [[001_dikw_pyramid|데이터]]를 쏴버리는 진정한 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 융합형 '초거대 [[746_io_direct_memory_access_dma|DMA]] 풀(Pool)' 생태계가 펼쳐질 것이다.

- **📢 섹션 요약 비유**: 왕(CPU)이 직접 밀가루 포대([[001_dikw_pyramid|데이터]])를 들고 창고(RAM)와 백성(디스크) 사이를 오가며 노가다를 하던 한심한 왕국이, 전문 물류 하청업체([[746_io_direct_memory_access_dma|DMA]])에게 운송권을 넘기면서 왕은 오직 [[164_policy|정책]](연산)에만 몰두할 수 있게 되어 초강대국으로 성장하게 된 거대한 분업화의 역사입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[448_polling_programmed_io|폴링]] ([[747_io_polling_overhead|Polling]] / Programmed I/O) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[016_interrupt_mechanism|인터럽트]] 구동 I/O (Interrupt-driven I/O) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[451_cycle_stealing|사이클 스틸링]] ([[451_cycle_stealing|Cycle Stealing]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[746_io_direct_memory_access_dma|DMA]] 산란-수집 ([[452_dma_scatter_gather|Scatter-Gather]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[인터럽트 구동 I/O (Interrupt-driven I/O)]
    │
    ▼
[직접 메모리 접근 (DMA, Direct Memory Access)]
    │
    ├──▶ [사이클 스틸링 (Cycle Stealing)]
    └──▶ [DMA 산란-수집 (Scatter-Gather)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 직접 메모리 접근 ([[746_io_direct_memory_access_dma|DMA]], [[318_dma|Direct Memory Access]])은 컴퓨터가 디스크와 장치가 [[001_dikw_pyramid|데이터]]를 주고받는 길을 정리하는 방법이에요.
2. 먼저 [[016_interrupt_mechanism|인터럽트]] 구동 I/O (Interrupt-driven I/O)을 이해하면 직접 메모리 접근 ([[746_io_direct_memory_access_dma|DMA]], [[318_dma|Direct Memory Access]])이 왜 필요한지 더 쉽게 보여요.
3. 그래서 직접 메모리 접근 ([[746_io_direct_memory_access_dma|DMA]], [[318_dma|Direct Memory Access]])을 잘 알면 나중에 [[451_cycle_stealing|사이클 스틸링]] ([[451_cycle_stealing|Cycle Stealing]])도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 450 / 800

← **이전**: [[449_interrupt_driven_io|449. 인터럽트 구동 I/O (Interrupt-driven I/O) - 완료 시 장치가 CPU에 인터럽트 발생]]
**다음**: [[451_cycle_stealing|451. 사이클 스틸링 (Cycle Stealing) - DMA 컨트롤러가 CPU의 버스 사용을 일시 중지시키고 전송]] →

---
