+++
title = "460. 논블로킹 I/O (Non-blocking I/O) - 데이터가 없어도 즉시 반환 (오류/0 바이트 반환)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 논블로킹 I/O(Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O)는 프로세스([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 OS에게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(디스크/네트워크)를 요구했을 때, <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 아직 도착하지 않아도 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>를 기절(Sleep)시키지 않고 즉각 "아직 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 없음(EAGAIN)" 에러 코드를 뱉어버린 뒤 제어권을 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>에게 돌려주는 I/O 아키텍처</strong>다.
> 2. **가치**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 하염없이 기다리는([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 멍청한 시간을 완벽하게 소거하여, <strong>단 1개의 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>로도 수만 명의 사용자 네트워크 요청(C10K)을 끊김 없이 번갈아 쳐낼 수 있는 무한의 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a>(<a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/">Concurrency</a>)과 확장성을 폭발</strong>시킨다.
> 3. **융합(한계)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받을 때까지 무한정 재시도([Busy Wait](/knowledge-base/studynote/02_operating_system/11_exam_summary/700_spinlock_busy_waiting/))하면 [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)([Polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))의 악몽에 빠지므로, 반드시 OS가 제공하는 <strong>이벤트 통지 시스템(<code>epoll</code>, <code>kqueue</code> 등 I/O 멀티플렉싱)과 영혼의 융합을 이루어야만</strong> Nginx, [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 같은 초고성능 [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) 서버의 뼈대가 완성된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: C언어 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 프로그래밍에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 디스크립터(fd)에 `O_NONBLOCK` 깃발(옵션)을 딱 꽂아주는 순간 발동한다. 이 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)에 `read()`를 때리면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있다면 빛의 속도로 퍼다 주고 끝난다. 그런데 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 없다면? OS는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 멱살을 잡아 [대기 큐](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/)([Wait Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/))에 처넣지 않고, 0.001초 만에 **"에러코드 -1 (EAGAIN/EWOULDBLOCK): 나중에 다시 와라!"** 라고 매몰차게 뱉고 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 즉시 방출(Return)시켜 버린다. 
- **필요성**: 인터넷 서버에 접속한 1만 명의 유저(C10K)가 있다 치자. 유저 A가 로그인 버튼을 누르고 10초 동안 비밀번호를 안 치고 가만히 있는다. 옛날 블로킹([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 서버는 A를 기다리느라 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1개가 10초 동안 뇌사 상태로 굳어버렸다. 1만 명을 상대하려면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1만 개 필요했고, 이 1만 개의 뇌([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/))를 스위칭하느라 서버의 램과 CPU가 불타서 재가 되었다. 빡친 개발자들은 외쳤다. "아니, 대답 안 하는 놈을 왜 기다려줘? 없으면 그냥 버리고 당장 대답할 수 있는 다음 놈한테 빨리 넘어가라고!" [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 목숨(가동 시간)을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 대기라는 불확실성에서 100% 해방시킨 혁명이다.

- **등장 배경 및 아파치의 몰락**:
  1. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a> per Request 모델의 붕괴</strong>: 클라이언트 1개당 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1개를 붙이는 Apache 웹서버는 트래픽이 몰리면 OOM과 [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 지옥에 빠져 죽었다.
  2. **비동기/이벤트 구동의 대두**: "기다리지 않는다"는 철학으로 무장한 Nginx가 적은 램과 단 1개의 워커 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 Apache를 씹어 먹으며 시장을 평정함.
  3. **I/O 멀티플렉싱의 날개**: 넌블로킹이 그냥 [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)(무한 찌르기)으로 전락하지 않도록, `epoll`이라는 감시자가 결합하며 완전체 생태계를 이룩함.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">블로킹(Blocking) vs 넌블로킹(Non-blocking) I/O의 치명적 차이 시각화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 1. 블로킹 I/O (과거 톰캣, 아파치의 지옥)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">유저 스레드</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">OS 커널</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"네트워크에 데이터 안 왔네?"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(10초 동안 멍때림)</div><div class="kb-diagram-cell">(10초 대기...)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◀── <code>Hello</code> 리턴</div><div class="kb-diagram-cell">"오! 왔다 가져가라!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(수만 개의 스레드가 이런 식으로 굳어버리며 램(스택) 터져나감 ☠️)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 2. 넌블로킹 I/O (Nginx, Node.js의 꿀벌 텐션)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">유저 스레드</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">OS 커널</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◀── <code>EAGAIN (없음)</code> ─</div><div class="kb-diagram-cell">"데이터 없네? 꺼져!" (1ms 컷)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">OS 커널</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◀── <code>Hello 리턴!</code> ──</div><div class="kb-diagram-cell">"얜 데이터 왔네! 가져가!"</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">OS 커널</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◀── <code>EAGAIN (없음)</code> ─</div><div class="kb-diagram-cell">"없네? 꺼져!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(단 1개의 스레드가 10초 동안 수백만 개의 소켓을 찔러대며 다 쳐냄 🚀)</div></div>
</div>
</div>


**[다이어그램 해설]** "멈추지 않는다(Never Block)." 이것이 현대 고성능 백엔드 아키텍처의 절대 헌법이다. 유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 늪([Wait Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/))에 빠지는 순간 그 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 잡아먹은 2MB [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 메모리와 소중한 타임 퀀텀은 우주 쓰레기가 된다. 넌블로킹은 0.1초의 망설임 없이 에러(EAGAIN)를 뱉고 도망쳐 나오게 만듦으로써, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 숨통을 트이게 하고 미친듯한 핑퐁([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))을 가능케 한 물리적 마법이다.

- **📢 섹션 요약 비유**: 친구 10명한테 돈 갚으라고 전화할 때, 블로킹 방식은 1번 친구가 안 받으면 받을 때까지 10분 동안 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)음만 계속 듣고 앉아있는 겁니다. 넌블로킹 방식은 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 1번 갔는데 안 받으면([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없음) 쿨하게 끊어버리고 바로 2번, 3번 친구한테 전화를 다 돌리는 겁니다. 10명 중에 전화 바로 받은([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 있음) 3명한테 돈을 빛의 속도로 뜯어낼 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 에러 코드의 재해석: EAGAIN / EWOULDBLOCK

넌블로킹 시스템 콜을 썼을 때 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 뱉어내는 가장 유명한 리턴 값은 에러 코드 <strong><code>-1</code></strong>과 함께 뜨는 `EAGAIN`(Try Again)이다.
- 초보 개발자는 `read()` 결과가 -1이 뜨면 "헉 통신이 끊겼나? 버그 났다!" 하고 예외 처리(Exception)를 던지고 서버를 뻗게 만든다.
- **아키텍처의 본질**: 넌블로킹 세계에서 `EAGAIN`은 에러가 아니다. "진짜 에러(통신 절단)가 아니라, <strong>니가 찾는 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 지금 버퍼에 없으니까 이따가 다시 찔러봐라</strong>"라는 매우 정상적이고 합법적인 OS의 안내 메시지다.
- 이 `-1`을 쿨하게 `if`문으로 씹어버리고 다음 로직으로 넘어갈 수 있는 강심장이 되어야만 넌블로킹 서버를 짤 수 있다.

---

### 치명적 함정: 넌블로킹의 맹점 = [Busy Wait](/knowledge-base/studynote/02_operating_system/11_exam_summary/700_spinlock_busy_waiting/) ([폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/))

넌블로킹 함수는 한 번 부르고 없으면 끝난다. 그런데 그 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 1초 뒤에 오면 어떻게 다시 읽을까?
- **바보 같은 해결책**: 
  ```c
  while(1) { 
      res = read(socket, O_NONBLOCK); 
      if (res != EAGAIN) break; 
  }
  ```
  이 짓거리는 1초에 1억 번 `read` 시스템 콜을 때려 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 유저 모드를 미친 듯이 스위칭([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))하게 만든다. CPU 점유율이 100%로 불타버리며 컴퓨터가 녹아내린다. (소위 <strong>스핀 락/<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/">폴링</a>의 저주</strong>다).
- 즉, 순수한 넌블로킹 I/O는 이대로 쓰면 시스템을 조져버리는 최악의 쓰레기 코드다. 이 맹점을 완벽하게 덮어준 구원자가 바로 다음 장에서 배울 <strong>I/O 멀티플렉싱(epoll/<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/">select</a>)</strong>이다. 

- **📢 섹션 요약 비유**: 우편함에 편지 왔는지 확인할 때 멍하니 기다리지 않는(넌블로킹) 것까진 좋았습니다. 그런데 언제 편지가 올지 몰라서 1초마다 문 열고 뛰어나가 우편함을 열어보고 들어오고, 다시 뛰어나가 열어보고 들어오고(While 루프 [폴링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/))를 반복하다가 과로사로 죽어버리는 꼴입니다. 넌블로킹은 눈치는 빠르지만 행동이 너무 촐싹대서 혼자서는 아무 쓸모가 없습니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 비동기(Asynchronous) I/O vs 넌블로킹(Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) I/O

현업 개발자들조차 10년 차까지 헷갈려하는 CS 면접 궁극의 끝판왕 개념이다. **완전히 다르다.**

| 비교 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 넌블로킹 (Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O) | 비동기 (Asynchronous I/O, AIO) |
|:---|:---|:---|
| **OS의 즉각 응답** | `read`를 치면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없으면 **"없어!"(EAGAIN) 라고 즉시 응답 줌** | `aio_read` 치면 **"응 알았어 시작할게" 하고 수령증(Ticket)만 즉시 줌** |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 가져오는 주체</strong> | 나중에 내가 또 `read` 쳐서 **스스로 긁어와야 함** | OS가 뒤에서 몰래 디스크 긁어서 버퍼에 채운 뒤, 다 채우면 **콜백(Callback)이나 시그널로 "다 퍼왔다!"고 알려줌** |
| **CPU의 주도권** | 내가 계속 물어보러 가야 하므로 조금 귀찮음 (동기적 알림) | 지시만 내리고 완전히 잊어버리면 알아서 배달됨 (완벽한 비동기) |
| **실무 생태계** | 리눅스 네트워크(epoll), Node.js, Nginx의 **99% 절대 표준** | 윈도우의 IOCP (짱 좋음), 리눅스의 `io_uring` (이제야 뜨는 중) |

### 디스크 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O 앞에서는 한없이 작아지는 넌블로킹
개발자들이 환상을 가진다. "오! [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽을 때 `O_NONBLOCK` 켜서 읽으면 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)도 넌블로킹으로 쓱싹 읽히겠네!"
**대착각이다.** 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 하드디스크 같은 <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/">블록 장치</a>(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/">Block Device</a>)를 읽을 때는 <code>O_NONBLOCK</code> 플래그가 사실상 100% 개무시당한다.</strong> 
- 왜냐하면 디스크의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 "언젠가 올 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"가 아니라 "무조건 저기 디스크에 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"로 취급되기 때문에, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 강제로 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 목덜미를 잡고 디스크(8ms)를 긁어올 때까지 억지로 블로킹(D [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) 시켜버린다.
- 그래서 Node.js([이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/))가 네트워크는 넌블로킹으로 수만 개를 쳐내지만, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) `read`를 하는 순간 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 굳어버려서 서버가 즉사한다. 이를 우회하려고 Node.js는 뒤에서 몰래 <strong>C++ <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/">스레드 풀</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/">Thread Pool</a>)</strong> 4개를 띄워놓고 거기에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 블로킹 읽기 작업을 하청 주는 눈물겨운 꼼수를 쓴다. (진정한 리눅스 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) AIO는 `io_uring`이 나오기 전까진 전멸 상태였다).



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장치 종류</div><div class="kb-diagram-cell">Blocking 먹힘</div><div class="kb-diagram-cell">Non-block 작동</div><div class="kb-diagram-cell">백엔드 튜닝 전략</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">네트워크 소켓</div><div class="kb-diagram-cell">🟢 (느려터짐)</div><div class="kb-diagram-cell">🚀 (미친 속도)</div><div class="kb-diagram-cell">100% 넌블로킹 강제 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">디스크 파일</div><div class="kb-diagram-cell">🟢 (기본값)</div><div class="kb-diagram-cell">❌ (커널이 씹음)</div><div class="kb-diagram-cell">몰래 스레드풀 따로 파서 던짐</div></div>
</div>
</div>


**[매트릭스 해설]** [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 통신은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 도착할지 안 할지 아무도 모르므로 넌블로킹이 완벽하게 들어맞는다. 하지만 디스크 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 이미 거기 있다는 게 확정되어 있으므로, 디스크 암(Arm)이 돌아서 가져오기 전까지 넌블로킹 핑계를 대고 돌아갈 수 없게 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 못 박아놨다. 이 한계점을 아는 것이 진짜 시스템 아키텍트다.

- **📢 섹션 요약 비유**: 넌블로킹은 은행에서 번호표를 뽑고 "내 차례인가요?" 물어보고 아니면 바로 딴일 하러 가는 쾌적함입니다. 하지만 비동기는 아예 번호표를 비서에게 쥐여주고 집에 가서 자고 있으면, 비서(OS)가 내 차례가 왔을 때 집까지 서류([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 다 들고 배달 와주는 VVIP 서비스입니다. 윈도우는 이 비서(IOCP)가 엄청 잘되어 있지만, 리눅스는 비서 고용이 너무 힘들어서 내가 직접 왔다 갔다(넌블로킹+epoll) 해야 합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: Nginx의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1개짜리 1만 접속 방어 (C10K 돌파)
1. **과거(Apache)의 병목**: 아파치는 1만 명이 접속하면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1만 개를 띄웠다. 각각의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 `read` 치고 블로킹되어 잠들었다. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1만 개가 교대([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))하느라 서버의 CPU가 불타고, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 램이 20GB 날아갔다.
2. **Nginx의 넌블로킹 대학살**:
   - Nginx 개발자 이고르 시소예프는 "[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 1개만 띄운다(Worker [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))"고 선언했다.
   - 1만 명의 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)을 몽땅 <strong><code>O_NONBLOCK</code></strong>으로 열어버린다.
   - 워커 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1마리가 1번 유저에게 `read` 쳤다. 안 왔네?(EAGAIN). 0.001초 만에 2번 유저로 건너뛴다. 왔네? 쓱싹 처리. 3번 유저 안 왔네? 패스!
   - 단 1개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1초에 1만 개의 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)을 채찍질하며 미친 듯이 훑고([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 지나간다. 
3. **위대한 결과**: 
   - [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1개뿐이라 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 비용이 <strong>0</strong>이다. 
   - 램([스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)) 점유율은 불과 수 메가바이트(MB)에 불과하다. 
   - 구형 펜티엄 똥컴으로도 동시 접속자 1만 명(C10K)을 렉 없이 쳐내는 소프트웨어 아키텍처의 혁명이 완성되었다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/): Node.js [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) 차단 ([Event Loop](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) [Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/))
Node.js는 이 넌블로킹 철학으로 무장한 최강의 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 언어다.
근데 멍청한 백엔드 개발자가 유저의 비밀번호를 암호화한답시고 `bcrypt.hashSync()` 나 `while(10초 걸리는 연산)` 같은 무거운 <strong>CPU 블로킹 동기 연산</strong>을 메인 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 박아넣었다.
**결과**: Node.js의 꿀벌 같은 단 1개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 암호 계산하느라 10초 동안 굳어버렸다. 그 10초 동안 넌블로킹이든 나발이든 들어오는 모든 1만 명의 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 접속자 요청을 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 쳐다보지도 못해서 서버가 10초간 완벽히 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 뇌사에 빠진다. 넌블로킹 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 아키텍처에서 무거운 CPU 연산([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/))을 돌리는 것은 테러 행위다. 워커 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Worker [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))로 무조건 빼야 한다.

- **📢 섹션 요약 비유**: 중국집 배달원(싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 철가방에 짜장면 100그릇을 싣고 100집을 넌블로킹으로 문 앞에 쓱쓱 던지고 다니면 10분 만에 배달이 끝납니다. 그런데 3번째 집 손님이 "나 짜장면 비비는 것 좀 도와주고 가(무거운 CPU 연산)"라고 해서 배달원이 거기 서서 10분 동안 짜장면을 비비면([Event Loop](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) Blocked), 나머지 97집의 짜장면은 다 불어 터져서 폭동이 일어납니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **C10K / C10M 문제의 종식** | 수만~수백만 개의 동시 네트워크 연결을 단 몇 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 수십 MB의 램만으로 처리해 서버 인프라 비용을 수백 배 절감 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">Context Switch</a> 오버헤드 박멸</strong>| I/O 대기 시마다 발생하던 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수면(Sleep)과 깨어남(Wake-up)의 지옥 같은 CPU 캐시 날림 렉을 0으로 소거 |
| **반응형(Reactive) 생태계 태동** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 없으면 바로 넘어가고 이벤트로 콜백을 받는 Node.js, Spring WebFlux, RxJava 등 비동기 패러다임의 가장 깊숙한 물리적 뼈대 |

### 결론 및 미래 전망

논블로킹 I/O (Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O)는 "기다림이라는 자원 낭비를 절대 용납하지 않겠다"는 컴퓨터 공학자들의 지독한 광기가 빚어낸 네트워크 아키텍처의 구원자다. 과거 블로킹의 순차적이고 우아한 낭만을 무참히 박살 내고, 개발자들을 `EAGAIN` 에러와 콜백 지옥(Callback Hell)의 구렁텅이로 몰아넣었지만, 클라우드 시대에 초당 수십만 개의 트래픽을 처리하려면 인간의 낭만([가독성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)) 따위는 기계의 미친 스루풋([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) 앞에서 가차 없이 버려져야 했다. 이 넌블로킹 철학은 단순히 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 통신을 넘어 최신 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 `io_uring` 이나 클라우드의 [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)), 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))로 진화하며, 겉보기엔 우아한 블로킹 코드처럼 보이지만 속은 1나노초도 쉬지 않는 넌블로킹 괴물로 작동하는 궁극의 완전체로 영원히 컴퓨터 아키텍처의 정점에 군림할 것이다.

- **📢 섹션 요약 비유**: 한 번 낚싯대([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))를 던지면 물고기가 물 때까지 하염없이 기다리던 강태공(블로킹) 시대는 끝났습니다. 이제는 1만 개의 낚싯대([소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/))를 쫙 깔아두고, 바늘(넌블로킹)을 툭 건드려 미끼가 없으면 바로 옆 낚싯대로 뛰어가 1초에 1만 개의 낚싯대를 쉴 새 없이 순찰하며(epoll 멀티플렉싱) 물린 물고기만 미친 듯이 건져 올리는 기업형 원양어선의 시대입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 예약 및 단독 장치 접근 제어 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 블로킹 I/O ([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 비동기 I/O (Asynchronous I/O, AIO) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| I/O 완료 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) (IOCP, I/O Completion [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">블로킹 I/O (Blocking I/O)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">논블로킹 I/O (Non-blocking I/O)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">비동기 I/O (Asynchronous I/O, AIO)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">I/O 완료 포트 (IOCP, I/O Completion Port)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 논블로킹 I/O (Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O)은 컴퓨터가 디스크와 장치가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는 길을 정리하는 방법이에요.
2. 먼저 블로킹 I/O ([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O)을 이해하면 논블로킹 I/O (Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 논블로킹 I/O (Non-[blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/) I/O)을 잘 알면 나중에 비동기 I/O (Asynchronous I/O, AIO)도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 460 / 800

← **이전**: [459. 블로킹 I/O (Blocking I/O) - I/O 완료 시까지 프로세스 대기](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/459_blocking_io/)
**다음**: [461. 비동기 I/O (Asynchronous I/O, AIO) - I/O 요청 후 즉시 작업 진행, 완료 시 시그널/콜백 알림](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/461_asynchronous_io_aio/) →

---
