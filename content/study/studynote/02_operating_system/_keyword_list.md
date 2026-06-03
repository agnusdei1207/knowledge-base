+++
weight = 9999
title = "02. 운영체제 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
+++
[[267_weight_bias_activation|weight]] = 9999

# [[001_operating_system_purpose|운영체제]] 심화 키워드 목록 (기술사 최적화 800제)

정보관리기술사, 컴퓨터응용시스템기술사 시험에 가장 적합한 범위로 엄선한 800여 개의 [[001_operating_system_purpose|운영체제]] 핵심 및 심화 키워드입니다. 

기본적인 프로세스/메모리 관리를 넘어 **최신 [[022_kernel_role|커널]] 아키텍처, [[430_index_fast_full_scan|병렬]] 처리 및 [[212_synchronization_mechanisms|동기화]] 심화, [[136_variance|분산]] OS, [[015_virtualization|가상화]]/[[561_container_based_deployment|컨테이너]] 시스템, 실시간 [[001_operating_system_purpose|운영체제]](RTOS), 모바일/임베디드 OS, 그리고 시스템 보안 및 [[282_performance_tactics|성능]] 튜닝**에 초점을 맞추어 전면 재구성하였습니다.

---

## 1. [[001_operating_system_purpose|운영체제]] 개요 및 아키텍처 (80개)
1. [[001_operating_system_purpose|운영체제]] ([[001_operating_system_purpose|Operating System]])의 목적 - 자원 관리, 편의성, [[282_performance_tactics|성능]] 향상
2. [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]] ([[673_multiprogramming_bottleneck_resource|Multiprogramming]]) - CPU 활용도 극대화
3. [[003_time_sharing_system|시분할 시스템]] ([[003_time_sharing_system|Time-sharing System]]) - [[138_response_time|응답 시간]] 최소화, 인터랙티브
4. [[004_multiprocessing_system|다중 처리 시스템]] ([[004_multiprocessing_system|Multiprocessing System]])
5. [[194_numa_scheduling|비대칭 다중 처리]] ([[194_numa_scheduling|ASMP]], Asymmetric Multiprocessing)
6. [[195_real_time_scheduling|대칭 다중 처리]] ([[195_real_time_scheduling|SMP]], Symmetric Multiprocessing)
7. [[007_tightly_coupled_system|강결합 시스템]] ([[007_tightly_coupled_system|Tightly Coupled System]])
8. [[008_loosely_coupled_system|약결합 시스템]] ([[008_loosely_coupled_system|Loosely Coupled System]]) / [[136_variance|분산]] 시스템
9. [[009_real_time_system|실시간 시스템]] ([[009_real_time_system|Real-time System]]) - Hard vs Soft
[[489_raid_10_hybrid|10]]. [[010_embedded_system|임베디드 시스템]] ([[010_embedded_system|Embedded System]])
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_dual_mode|듀얼 모드]] ([[011_dual_mode|Dual Mode]]) - 사용자 모드(User Mode)와 [[022_kernel_role|커널]] 모드([[022_kernel_role|Kernel]] Mode)
12. [[012_mode_bit|모드 비트]] ([[012_mode_bit|Mode Bit]])
13. [[013_system_call|시스템 호출]] ([[013_system_call|System Call]]) - [[022_kernel_role|커널]] [[090_service_kubernetes_network_load_balancing|서비스]] 요청 인터페이스
14. [[014_api_posix|API]] ([[014_api_posix|Application Programming Interface]]), POSIX 표준
15. [[015_abi|ABI]] ([[015_abi|Application Binary Interface]])
16. [[016_interrupt_mechanism|인터럽트]] ([[016_interrupt_mechanism|Interrupt]]) 메커니즘
17. [[017_hardware_interrupt|하드웨어 인터럽트]] ([[017_hardware_interrupt|비동기적]])
18. 소프트웨어 [[016_interrupt_mechanism|인터럽트]] / [[677_trap_based_system_call_implementation|트랩]] ([[677_trap_based_system_call_implementation|Trap]]) / 예외 (Exception)
19. [[019_interrupt_vector|인터럽트 벡터]] ([[019_interrupt_vector|Interrupt Vector]])
20. [[020_isr|인터럽트 서비스 루틴]] ([[020_isr|ISR]], [[317_isr|Interrupt Service Routine]])
21. [[021_interrupt_handler|인터럽트 핸들러]] ([[021_interrupt_handler|Interrupt Handler]])
22. [[022_kernel_role|커널]] ([[022_kernel_role|Kernel]])의 역할
23. [[023_monolithic_kernel|모놀리식 커널]] ([[023_monolithic_kernel|Monolithic Kernel]]) - 리눅스, 고성능
24. [[598_microkernel_plugin_architecture|마이크로 커널]] ([[024_microkernel|Microkernel]]) - Mach, Minix, 높은 확장성과 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]
25. [[025_hybrid_kernel|하이브리드 커널]] ([[025_hybrid_kernel|Hybrid Kernel]]) - Windows NT, macOS(XNU)
26. 엑소 [[022_kernel_role|커널]] ([[026_exokernel|Exokernel]]) - 하드웨어 [[198_abstraction_control_data_process|추상화]] 최소화
27. [[640_unikernel_mirageos_architecture|유니커널]] ([[640_unikernel_mirageos_architecture|Unikernel]]) - [[336_library_vs_framework|라이브러리]] OS 기반 단일 주소 공간
28. [[028_bootstrap_program|부트스트랩 프로그램]] ([[028_bootstrap_program|Bootstrap Program]])
29. [[029_bootloader|부트로더]] ([[029_bootloader|Bootloader]]) - GRUB, LILO
30. [[706_uefi|UEFI]] (Unified Extensible [[032_firmware|Firmware]] Interface) vs BIOS
31. 시스템 [[087_process_state_transition|생성]] (System Generation, [[031_sysgen|SYSGEN]])
32. [[032_firmware|펌웨어]] ([[032_firmware|Firmware]])
33. 문맥 ([[033_context|Context]]) - CPU [[057_register|레지스터]], [[086_process_state|프로세스 상태]] 등
34. [[211_context_switch|문맥 교환]] ([[211_context_switch|Context Switch]]) 오버헤드
35. [[035_core_dump|코어 덤프]] ([[035_core_dump|Core Dump]])
36. 패닉 (Panic) / [[036_kernel_panic|커널 패닉]] ([[036_kernel_panic|Kernel Panic]]) / 블루 스크린 (BSOD)
37. [[037_system_daemon|시스템 데몬]] ([[037_system_daemon|System Daemon]]) / 백그라운드 프로세스
38. init 프로세스 / systemd (리눅스 첫 번째 프로세스)
39. [[001_operating_system_purpose|운영체제]] [[090_service_kubernetes_network_load_balancing|서비스]] - UI, 프로그램 실행, I/O 연산, [[501_file_definition_logical_record|파일]] 시스템, 통신
40. [[040_error_detection|오류 탐지]] ([[040_error_detection|Error Detection]])
41. [[041_resource_allocation|자원 할당]] ([[041_resource_allocation|Resource Allocation]])
42. 회계 (Accounting) 및 로깅
43. [[571_protection_vs_security|보호]] ([[571_protection_vs_security|Protection]]) 및 보안 ([[283_security_tactics|Security]])
44. [[158_instruction|명령어]] 인터프리터 ([[271_command_pattern|Command]] [[277_interpreter_pattern|Interpreter]]) / 쉘 ([[044_shell|Shell]])
45. 클러스터 시스템 (Clustered System) - 고가용성(HA), [[430_index_fast_full_scan|병렬]] 컴퓨팅
46. [[457_hot_standby|핫 스탠바이]] ([[457_hot_standby|Hot Standby]]) / [[458_cold_standby|콜드 스탠바이]] ([[458_cold_standby|Cold Standby]])
47. [[136_variance|분산]] 잠금 관리자 ([[047_dlm|DLM]], Distributed [[510_lock|Lock]] Manager)
48. 스토리지 영역 네트워크 ([[493_san_storage_area_network|SAN]]) 연동
49. 클라이언트-서버 시스템 ([[206_client_server_architecture_model|Client-Server]] System)
50. [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] ([[916_p2p_peer_to_peer_networking_super_node_gnutella|Peer-to-Peer]]) 시스템
51. [[051_grid_computing|그리드 컴퓨팅]] ([[051_grid_computing|Grid Computing]])
52. [[052_cloud_computing_os|클라우드 컴퓨팅]] ([[052_cloud_computing_os|Cloud Computing]]) OS 관점
53. [[015_virtualization|가상화]] ([[190_virtualization_computing_architecture_cloud|Virtualization]]) 아키텍처
54. [[054_hypervisor|하이퍼바이저]] ([[054_hypervisor|Hypervisor]]) / VMM
55. 베어메탈 (Bare-metal) [[054_hypervisor|하이퍼바이저]] (Type 1)
56. 호스트형 [[054_hypervisor|하이퍼바이저]] (Type 2)
57. [[057_full_virtualization|전가상화]] ([[057_full_virtualization|Full Virtualization]]) - 이진 변환 (Binary Translation)
58. [[058_paravirtualization|반가상화]] ([[058_paravirtualization|Paravirtualization]]) - 하이퍼콜 (Hypercall)
59. [[059_hardware_assisted_virtualization|하드웨어 보조 가상화]] ([[658_intel_vtx|Intel VT-x]], [[659_amd_v|AMD-V]])
60. [[561_container_based_deployment|컨테이너]] ([[194_container_virtualization_docker_namespace|Container]]) 기술 기반 - OS 수준 [[015_virtualization|가상화]]
61. [[061_namespace|네임스페이스]] ([[061_namespace|Namespace]]) - 자원 격리
62. [[062_cgroups|컨트롤 그룹]] ([[062_cgroups|cgroups]]) - [[041_resource_allocation|자원 할당]] 제어
63. [[063_docker_architecture|도커]] ([[063_docker_architecture|Docker]]) 아키텍처
64. [[064_rootfs_overlayfs|루트 파일 시스템]] ([[064_rootfs_overlayfs|Root Filesystem]]) / 오버레이 [[501_file_definition_logical_record|파일]] 시스템 (OverlayFS)
65. [[065_system_call_wrapper|시스템 콜 래퍼]] ([[065_system_call_wrapper|System Call Wrapper]])
66. [[517_virtual_file_system_vfs|VFS]] ([[517_virtual_file_system_vfs|Virtual File System]])
67. [[067_lkm|모듈 적재]] (Loadable [[022_kernel_role|Kernel]] Modules, [[067_lkm|LKM]])
68. [[068_live_patching|동적 커널 패치]] ([[068_live_patching|Live Patching]]) - [[789_live_patching_kpatch_no_downtime|kpatch]], kGraft
69. [[069_ebpf|BPF]] ([[069_ebpf|Berkeley Packet Filter]]) / [[615_ebpf|eBPF]] (Extended [[069_ebpf|BPF]]) - [[022_kernel_role|커널]] 내 샌드박스 프로그램
70. [[070_hal|하드웨어 추상화 계층]] ([[070_hal|HAL]], Hardware [[198_abstraction_control_data_process|Abstraction]] Layer)
71. [[071_os_timer|운영체제 타이머]] ([[071_os_timer|Timer]]) - 시스템 클럭, [[059_counter|카운터]]
72. 타이머 [[016_interrupt_mechanism|인터럽트]] - [[166_preemptive_scheduling|선점형 스케줄링]]의 기반
73. 틱 ([[073_tick_jiffies|Tick]]) / 지피스 (Jiffies)
74. [[795_tickless_kernel_mobile_battery_preservation|틱리스 커널]] ([[074_tickless_kernel|Tickless Kernel]]) - [[466_power_consumption|전력 소모]] 감소
75. [[075_acpi|ACPI]] (Advanced Configuration and [[069_type_1_2_error_statistical_power|Power]] Interface)
76. [[076_s_states|시스템 전원 상태]] (S-States, S0~S5)
77. [[077_c_states|프로세서 전원 상태]] ([[077_c_states|C-States]])
78. [[078_p_states|프로세서 성능 상태]] ([[078_p_states|P-States]])
79. [[001_operating_system_purpose|운영체제]] [[613_profiling_gprof|프로파일링]] 및 트레이싱 도구 (perf, ftrace, [[614_dtrace|DTrace]])
80. [[013_system_call|시스템 호출]] 차단 ([[080_seccomp|Seccomp]])

## 2. 프로세스와 [[092_thread_lwp|스레드]] (80개)
81. 프로그램 (Program) vs 프로세스 ([[300_process|Process]])
82. 프로세스 메모리 구조 - Text([[082_process_memory_structure|Code]]), [[001_dikw_pyramid|Data]], [[083_bss_segment|BSS]], [[078_heap_datastructure|Heap]], [[057_stack|Stack]]
83. [[083_bss_segment|BSS]] (Block Started by Symbol) 영역 - 초기화되지 않은 전역 변수
84. 힙 ([[078_heap_datastructure|Heap]]) 영역 - 동적 할당 (malloc/free)
85. [[057_stack|스택]] ([[057_stack|Stack]]) 영역 - 지역 변수, 매개변수, 리턴 주소
86. [[086_process_state|프로세스 상태]] ([[086_process_state|Process State]])
87. [[087_process_state_transition|생성]] ([[087_process_state_transition|New]]) -> 준비 (Ready) -> 실행 (Running) -> 대기 (Waiting/Blocked) -> 종료 (Terminated)
88. [[088_ready_queue|준비 큐]] ([[088_ready_queue|Ready Queue]])
89. [[089_wait_queue|대기 큐]] ([[089_wait_queue|Wait Queue]] / Device [[058_queue|Queue]])
90. [[090_pcb_tcb|프로세스 제어 블록]] (PCB, [[300_process|Process]] Control Block) / [[150_task|태스크]] 제어 블록 (TCB)
91. PCB 요소 - PID, 상태, [[164_pc|PC]], [[057_register|레지스터]], 스케줄링 정보, 메모리 정보, 회계 정보, I/O 상태 정보
92. [[092_thread_lwp|스레드]] ([[092_thread_lwp|Thread]]) - 경량 프로세스 (LWP)
93. [[092_thread_lwp|스레드]]의 자원 공유 - [[082_process_memory_structure|Code]], [[001_dikw_pyramid|Data]], [[078_heap_datastructure|Heap]], 열린 [[501_file_definition_logical_record|파일]]
94. [[092_thread_lwp|스레드]]의 독립 자원 - [[092_thread_lwp|Thread]] ID, [[164_pc|PC]], [[057_register|레지스터]] 집합, [[057_stack|스택]]
95. [[095_multithreading_benefits|다중 스레드]] ([[095_multithreading_benefits|Multithreading]])의 장점 - 응답성, 자원 공유, 경제성, 다중 처리기 활용
96. [[096_user_level_thread|사용자 수준 스레드]] ([[096_user_level_thread|User-level Thread]]) - [[092_thread_lwp|스레드]] [[336_library_vs_framework|라이브러리]]가 관리, [[022_kernel_role|커널]] 비개입
97. [[097_kernel_level_thread|커널 수준 스레드]] ([[097_kernel_level_thread|Kernel-level Thread]]) - OS가 직접 관리
98. [[098_many_to_one_model|다대일]] ([[098_many_to_one_model|Many-to-One]]) [[092_thread_lwp|스레드]] 모델
99. [[099_one_to_one_model|일대일]] ([[099_one_to_one_model|One-to-One]]) [[092_thread_lwp|스레드]] 모델
100. [[100_many_to_many_model|다대다]] ([[100_many_to_many_model|Many-to-Many]]) [[092_thread_lwp|스레드]] 모델
101. [[101_two_level_model|두 수준]] ([[101_two_level_model|Two-level]]) 모델
102. [[102_implicit_threading|암묵적 스레딩]] ([[102_implicit_threading|Implicit Threading]]) - [[103_thread_pool|스레드 풀]], OpenMP, Grand Central Dispatch([[663_macos_ios_gcd_grand_central_dispatch|GCD]])
103. [[103_thread_pool|스레드 풀]] ([[103_thread_pool|Thread Pool]])
104. [[104_process_creation|프로세스 생성]] ([[104_process_creation|Process Creation]]) - fork(), exec() 시스템 콜
105. [[105_parent_child_process|부모 프로세스]] ([[105_parent_child_process|Parent Process]]) / 자식 프로세스 (Child [[300_process|Process]])
106. [[542_cow_file_system|Copy-on-Write]] ([[542_cow_file_system|COW]]) - fork() 최적화 기법
107. [[107_process_termination|프로세스 종료]] ([[107_process_termination|Process Termination]]) - exit(), wait()
108. [[108_cascading_termination|연쇄적 종료]] ([[108_cascading_termination|Cascading Termination]])
109. [[109_zombie_process|좀비 프로세스]] ([[109_zombie_process|Zombie Process]]) - 종료되었으나 부모가 wait()하지 않은 상태
110. [[110_orphan_process|고아 프로세스]] ([[110_orphan_process|Orphan Process]]) - 부모가 먼저 종료된 상태 (init 프로세스가 입양)
111. [[111_thread_cancellation|스레드 취소]] ([[111_thread_cancellation|Thread Cancellation]]) - 비동기식 취소, [[015_지연_데이터_관점|지연]] 취소
112. [[112_cancellation_point|취소 점]] ([[112_cancellation_point|Cancellation Point]])
113. [[113_thread_local_storage|스레드 로컬 저장소]] ([[694_thread_local_storage_tls|TLS]], [[092_thread_lwp|Thread]]-Local Storage)
114. [[114_scheduler_activation|스케줄러 액티베이션]] ([[114_scheduler_activation|Scheduler Activation]]) / 경량 프로세스(LWP)
115. [[115_upcall|상향 호출]] ([[115_upcall|Upcall]])
116. [[116_cooperating_independent_process|협력적 프로세스]] ([[116_cooperating_independent_process|Cooperating Process]]) vs 독립적 프로세스 (Independent [[300_process|Process]])
117. [[117_ipc|프로세스 간 통신]] ([[117_ipc|IPC]], Inter-[[300_process|Process]] Communication)
118. [[118_shared_memory|공유 메모리]] ([[118_shared_memory|Shared Memory]]) 방식 - 빠름, [[212_synchronization_mechanisms|동기화]] 문제 발생
119. [[119_message_passing|메시지 전달]] ([[119_message_passing|Message Passing]]) 방식 - 안전, [[022_kernel_role|커널]] 개입(시스템 콜) 오버헤드
120. [[120_direct_communication|직접 통신]] ([[120_direct_communication|Direct Communication]]) - 수신자 명시
121. [[121_indirect_communication|간접 통신]] ([[121_indirect_communication|Indirect Communication]]) - 메일박스/[[446_port_and_bus|포트]] 사용
122. [[122_sync_async_communication|동기식 통신]] ([[122_sync_async_communication|Blocking]]) vs 비동기식 통신 (Non-[[122_sync_async_communication|blocking]])
123. [[123_pipe|파이프]] ([[123_pipe|Pipe]]) - [[008_단방향_반이중_전이중|단방향]](Half-duplex), 부모-자식 간
124. [[124_named_pipe_fifo|지명 파이프]] (Named [[123_pipe|Pipe]] / [[261_fifo_page_replacement|FIFO]]) - 양방향 가능, 부모-자식 [[083_relationship_in_er_model|관계]] 무관
125. [[125_socket|소켓]] ([[125_socket|Socket]]) 통신 - 네트워크, 서로 다른 시스템 간 통신
126. [[126_rpc|RPC]] ([[126_rpc|Remote Procedure Call]]) - [[136_variance|분산]] 시스템 [[294_function_calling_tool_use|함수 호출]]
127. [[127_xdr_external_data_representation|XDR]] ([[127_xdr_external_data_representation|External Data Representation]])
128. [[128_marshalling_unmarshalling|마샬링]] ([[128_marshalling_unmarshalling|Marshalling]]) / 언마샬링 (Unmarshalling)
129. [[129_lpc_alpc|로컬 프로시저 호출]] (LPC, Local Procedure [[189_subroutine_call_return|Call]]) / ALPC (Windows)
130. [[130_signal|신호]] ([[130_signal|Signal]]) - 소프트웨어 [[016_interrupt_mechanism|인터럽트]] 방식 [[117_ipc|IPC]] (kill, SIGINT, SIGKILL)
131. [[131_mmap_ipc|메모리 맵 파일]] ([[308_memory_mapped_file|Memory-Mapped File]], [[749_memory_mapped_file_mmap|mmap]]) 기반 [[117_ipc|IPC]]
132. 시스템 V [[117_ipc|IPC]] - [[118_shared_memory|공유 메모리]], [[224_semaphore|세마포어]], 메시지 큐
133. [[133_posix_ipc|POSIX IPC]]
134. [[134_dbus|D-Bus]] ([[134_dbus|Desktop Bus]]) - 리눅스 데스크톱 환경 [[117_ipc|IPC]]
135. [[135_android_binder|안드로이드 바인더]] ([[135_android_binder|Android Binder]]) - 객체 지향적 경량 [[117_ipc|IPC]]
136. [[136_zombie_thread|좀비 스레드]] ([[136_zombie_thread|Zombie Thread]])
137. [[137_multiprocess_architecture|멀티프로세스 아키텍처]] ([[137_multiprocess_architecture|크롬 브라우저 등]])
138. [[138_multithread_architecture_overhead|멀티스레드 아키텍처 오버헤드]] ([[138_multithread_architecture_overhead|락 경합 등]])
139. [[139_actor_model|액터 모델]] ([[139_actor_model|Actor Model]]) - [[1004_erlang_traffic_load_unit_calculation|Erlang]], Akka [[014_concurrency|동시성]] 모델
140. [[140_goroutine|고루틴]] ([[140_goroutine|Goroutine]]) - Go 언어의 경량 [[092_thread_lwp|스레드]] (M:N 모델)
141. [[141_coroutine|코루틴]] ([[141_coroutine|Coroutine]])
142. [[142_event_loop|이벤트 루프]] ([[142_event_loop|Event Loop]]) 기반 비동기 처리 (Node.js)
143. [[034_context_switch|컨텍스트 스위칭]] 최소화를 위한 [[092_thread_lwp|스레드]] 고정 ([[092_thread_lwp|Thread]] [[778_process_affinity_scheduling_pinning|Affinity]]/Pinning)
144. CPU 친화성 ([[144_cpu_affinity|CPU Affinity]]) - Soft [[778_process_affinity_scheduling_pinning|Affinity]] vs Hard [[778_process_affinity_scheduling_pinning|Affinity]]
145. [[377_numa_allocation|NUMA]]-인식 [[092_thread_lwp|스레드]] 스케줄링
146. [[146_realtime_process|실시간 프로세스]] ([[146_realtime_process|Real-time Process]])
147. [[147_thread_safe|스레드 안전]] ([[147_thread_safe|Thread-safe]]) 함수 및 [[336_library_vs_framework|라이브러리]]
148. [[148_reentrant_code|재진입 가능 코드]] ([[148_reentrant_code|Reentrant Code]] / Pure [[082_process_memory_structure|Code]])
149. [[149_clone_system_call|클론]] ([[149_clone_system_call|clone]]) 시스템 콜 (리눅스 프로세스/[[092_thread_lwp|스레드]] [[087_process_state_transition|생성]] 범용 [[014_api_posix|API]])
150. [[150_task|태스크]] ([[150_task|Task]]) - 리눅스의 프로세스/[[092_thread_lwp|스레드]] 통일된 용어
151. [[151_namespace_isolation|네임스페이스 격리]] 프로세스
152. [[152_daemonization|데몬화]] ([[152_daemonization|Daemonization]]) 절차 - fork, setsid, umask, [[501_file_definition_logical_record|파일]] 디스크립터 닫기
153. 좀비 사냥 ([[153_reaping_zombies|Reaping Zombies]])
154. [[092_thread_lwp|스레드]] [[057_stack|스택]] [[095_overflow|오버플로우]] 방지 ([[154_thread_stack_overflow_prevention|Guard Page]])
155. [[155_dynamic_linking_process|동적 링킹 프로세스]] (ld.so) 로딩 과정
156. [[156_environment_variables|환경 변수]] ([[156_environment_variables|Environment Variables]]) [[234_uml_class_relationships_generalization_dependency|상속]]
157. [[157_oom_killer|OOM]] ([[157_oom_killer|Out Of Memory]]) Killer [[107_process_termination|프로세스 종료]] [[164_policy|정책]]
158. oom_score_adj - [[157_oom_killer|OOM]] 킬러 우선순위 조정
159. [[159_process_group|프로세스 그룹]] ([[159_process_group|Process Group]])
160. [[160_session_controlling_terminal|세션]] ([[160_session_controlling_terminal|Session]]) 및 제어 터미널 (Controlling Terminal)

## 3. CPU 스케줄링 (60개)
161. [[161_short_term_scheduler|단기 스케줄러]] ([[161_short_term_scheduler|Short-term Scheduler]]) / CPU [[079_kube_scheduler_pod_placement|스케줄러]]
162. [[162_medium_term_scheduler_swapping|중기 스케줄러]] ([[162_medium_term_scheduler_swapping|Medium-term Scheduler]]) - [[335_swapping|스와핑]] ([[335_swapping|Swapping]])
163. [[163_long_term_scheduler|장기 스케줄러]] ([[163_long_term_scheduler|Long-term Scheduler]]) - [[258_degree_of_multiprogramming|다중 프로그래밍 정도]] 조절
164. I/O 바운드 프로세스 (I/O Bound [[300_process|Process]])
165. CPU 바운드 프로세스 ([[165_cpu_bound_process|CPU Bound Process]])
166. [[166_preemptive_scheduling|선점형 스케줄링]] ([[166_preemptive_scheduling|Preemptive Scheduling]])
167. [[167_non_preemptive_scheduling|비선점형 스케줄링]] ([[167_non_preemptive_scheduling|Non-preemptive Scheduling]])
168. [[168_dispatcher|디스패처]] ([[168_dispatcher|Dispatcher]]) - [[211_context_switch|문맥 교환]] 수행 [[192_module_independence|모듈]]
169. [[169_dispatch_latency|디스패치 지연]] ([[169_dispatch_latency|Dispatch Latency]])
170. [[170_scheduling_criteria|스케줄링 기준]] ([[170_scheduling_criteria|Scheduling Criteria]]) - CPU 이용률, [[139_throughput|처리량]], 반환시간, 대기시간, 응답시간
171. CPU 이용률 ([[171_cpu_utilization_throughput|CPU Utilization]]) / [[139_throughput|처리량]] ([[139_throughput|Throughput]])
172. [[172_turnaround_waiting_response_time|반환 시간]] ([[172_turnaround_waiting_response_time|Turnaround Time]]) / 대기 시간 (Waiting Time) / [[138_response_time|응답 시간]] ([[138_response_time|Response Time]])
173. [[173_fcfs_scheduling|FCFS]] (First-Come, First-Served) 스케줄링 - [[285_no_preemption|비선점]]
174. [[174_convoy_effect|호위 효과]] ([[174_convoy_effect|Convoy Effect]]) - FCFS의 단점
175. [[175_sjf_scheduling|SJF]] ([[175_sjf_scheduling|Shortest Job First]]) 스케줄링 - 최적의 평균 대기 시간
176. [[176_exponential_averaging|지수 평균법]] ([[176_exponential_averaging|Exponential Averaging]]) - 다음 CPU [[344_bus|버스]]트 길이 예측
177. [[177_srtf_scheduling|SRTF]] (Shortest Remaining Time First) 스케줄링 - SJF의 선점형 [[288_version_ihl_tos_total_length|버전]]
178. [[178_round_robin_scheduling|라운드 로빈]] (Round Robin, [[834_load_balancing_algorithm_round_robin_least_connection|RR]]) 스케줄링 - [[003_time_sharing_system|시분할 시스템]], 선점형
179. [[179_time_quantum_context_switch|시간 할당량]] (Time [[690_round_robin_time_quantum|Quantum]] / Time [[331_neuromorphic_ai_db|Slice]]) 의 크기와 [[211_context_switch|문맥 교환]] 오버헤드
180. [[180_priority_scheduling|우선순위 스케줄링]] ([[180_priority_scheduling|Priority Scheduling]]) - 무한 대기 문제 발생 가능
181. [[314_starvation_prevention|기아 상태]] ([[314_starvation_prevention|Starvation]] / Indefinite [[122_sync_async_communication|Blocking]])
182. [[182_aging|노화]] ([[182_aging|Aging]]) - [[314_starvation_prevention|기아 상태]] 해결책 (우선순위 점진적 상승)
183. [[183_multilevel_queue_scheduling|다단계 큐 스케줄링]] ([[183_multilevel_queue_scheduling|Multilevel Queue Scheduling]])
184. [[184_scheduling_between_queues|큐 간 스케줄링]] (고정 우선순위 vs 시간 할당)
185. [[691_mlfq_multi_level_feedback_queue|다단계 피드백 큐]] 스케줄링 (Multilevel Feedback [[058_queue|Queue]], [[691_mlfq_multi_level_feedback_queue|MLFQ]]) - 프로세스의 큐 이동 허용
186. [[691_mlfq_multi_level_feedback_queue|MLFQ]] 파라미터 - 큐의 개수, [[001_algorithm_definition|알고리즘]], 승급/강등 기준
187. [[187_hrn_scheduling|HRN]] (Highest Response Ratio Next) 스케줄링 - (대기시간+[[090_service_kubernetes_network_load_balancing|서비스]]시간)/[[090_service_kubernetes_network_load_balancing|서비스]]시간
188. [[188_guaranteed_scheduling|보장 스케줄링]] ([[188_guaranteed_scheduling|Guaranteed Scheduling]])
189. [[189_lottery_scheduling|복권 스케줄링]] ([[189_lottery_scheduling|Lottery Scheduling]]) - 확률적 스케줄링
190. [[190_fair_share_scheduling|공평 몫 스케줄링]] ([[190_fair_share_scheduling|Fair-share Scheduling]])
191. [[092_thread_lwp|스레드]] 스케줄링 - 프로세스 경쟁 범위([[191_thread_scheduling_pcs_scs|PCS]]) vs 시스템 경쟁 범위(SCS)
192. LWP 디스패치
193. [[193_smp_symmetric_multiprocessing|다중 처리기 스케줄링]] ([[193_smp_symmetric_multiprocessing|Multiprocessor Scheduling]])
194. [[194_numa_scheduling|비대칭 다중 처리]] ([[194_numa_scheduling|ASMP]]) 스케줄링
195. [[195_real_time_scheduling|대칭 다중 처리]] ([[195_real_time_scheduling|SMP]]) 스케줄링
196. [[196_hard_soft_real_time|부하 균등화]] ([[196_hard_soft_real_time|Load Balancing]]) - Push Migration vs Pull Migration
197. 프로세서 친화성 (Processor [[778_process_affinity_scheduling_pinning|Affinity]]) - 캐시 최적화
198. [[198_edf_scheduling|멀티코어 스케줄링]] ([[198_edf_scheduling|Multicore Scheduling]]) - 메모리 스톨 (Memory Stall) 대응
199. [[199_interrupt_scheduling|하이퍼스레딩]] ([[199_interrupt_scheduling|Hyper-threading]]) / [[400_smt|SMT]] (Simultaneous [[095_multithreading_benefits|Multithreading]]) 스케줄링
200. 이기종 [[193_smp_symmetric_multiprocessing|다중 처리기 스케줄링]] (HMP) - ARM big.LITTLE 구조
201. 실시간 스케줄링 (Real-time Scheduling)
202. 연성 실시간 (Soft Real-time) 시스템
203. 경성 실시간 (Hard Real-time) 시스템
204. [[141_latency|지연 시간]] ([[141_latency|Latency]]) - [[016_interrupt_mechanism|인터럽트]] [[015_지연_데이터_관점|지연]] ([[545_interrupt_latency|Interrupt Latency]]) + [[169_dispatch_latency|디스패치 지연]] ([[169_dispatch_latency|Dispatch Latency]])
205. 주기적 [[150_task|태스크]] (Periodic [[150_task|Task]]) - 주기(p), 마감시간(d), 실행시간(t)
206. [[197_rm_rate_monotonic_scheduling|RM]] ([[206_priority_inheritance|Rate-Monotonic]]) 스케줄링 - 주기가 짧을수록 높은 우선순위 (정적 우선순위)
207. [[207_deadline_scheduling|EDF]] ([[207_deadline_scheduling|Earliest Deadline First]]) 스케줄링 - 마감시간이 빠를수록 높은 우선순위 (동적 우선순위)
208. [[208_fixed_priority_scheduling|비례 배분 스케줄링]] ([[208_fixed_priority_scheduling|Proportionate Share Scheduling]])
209. POSIX 스케줄링 [[014_api_posix|API]] - SCHED_FIFO, SCHED_RR, SCHED_OTHER
210. 리눅스 O(1) [[079_kube_scheduler_pod_placement|스케줄러]] - 두 개의 [[055_array|배열]] ([[483_active_vs_passive_ftp|Active]], Expired)
211. 리눅스 CFS (Completely Fair Scheduler) - [[203_virtual_runtime_vruntime|가상 실행 시간]] (vruntime) 기반, [[063_red_black_tree|레드-블랙 트리]] 사용
212. 대상 [[141_latency|지연 시간]] (Target [[141_latency|Latency]]) / 최소 입자 (Minimum Granularity)
213. 윈도우 스케줄링 - [[168_dispatcher|디스패처]] ([[168_dispatcher|Dispatcher]]), 우선순위 기반 선점형, 32단계 우선순위
214. 동적 우선순위 승급 (Priority Boost) - I/O 완료 시, GUI 전경 프로세스
215. [[150_task|태스크]] 스케줄링의 [[402_cache_coherence|캐시 일관성]] ([[402_cache_coherence|Cache Coherence]]) 문제
216. 에너지 인지 스케줄링 (Energy-Aware Scheduling, EAS)
217. 코-스케줄링 (Co-scheduling / Gang Scheduling) - 밀접한 [[092_thread_lwp|스레드]] 동시 스케줄링
218. [[561_container_based_deployment|컨테이너]] 스케줄링 ([[062_cgroups|cgroups]] cpu.shares, cpu.cfs_quota_us)
219. 실시간 리눅스 ([[654_preempt_rt_linux_spinlock_mutex|PREEMPT_RT]] 패치)
220. 무중단 [[629_live_migration_pre_copy|라이브 마이그레이션]] 스케줄링 고려사항

## 4. 병행성 ([[266_other_transparency|Concurrency]]) 및 [[212_synchronization_mechanisms|동기화]] (70개)
221. [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]]) - 실행 순서에 따라 결과가 달라지는 현상
222. [[214_critical_section|임계 구역]] ([[214_critical_section|Critical Section]]) - 공유 [[001_dikw_pyramid|데이터]] 접근 코드 영역
223. [[214_critical_section|임계 구역]] 문제 해결의 3조건 - [[283_mutual_exclusion|상호 배제]]([[283_mutual_exclusion|Mutual Exclusion]]), [[216_progress_in_synchronization|진행]]([[216_progress_in_synchronization|Progress]]), [[217_bounded_waiting|한정된 대기]]([[217_bounded_waiting|Bounded Waiting]])
224. 선점형 [[022_kernel_role|커널]] (Preemptive [[022_kernel_role|Kernel]]) vs [[285_no_preemption|비선점]]형 [[022_kernel_role|커널]] (Non-preemptive [[022_kernel_role|Kernel]])
225. 피터슨의 해결책 (Peterson's [[001_algorithm_definition|Algorithm]]) - [[186_character_stuffing_dle_stx_etx|플래그]]([[186_character_stuffing_dle_stx_etx|flag]])와 턴(turn) 변수 활용, 2 프로세스 한정
226. 메모리 장벽 ([[416_memory_barrier|Memory Barrier]] / Memory Fence) - 메모리 연산 순서 보장 [[158_instruction|명령어]]
227. 하드웨어 [[158_instruction|명령어]] 기반 [[212_synchronization_mechanisms|동기화]]
228. Test-and-Set [[158_instruction|명령어]] - 원자적(Atomic) 읽기-수정
229. [[415_compare_and_swap|Compare-and-Swap]] ([[768_cas_compare_and_swap_lock_free|CAS]]) [[158_instruction|명령어]]
230. 원자적 변수 (Atomic Variable) - [[256_lock_free_data_structures|Lock-free]] 프로그래밍 기초
231. [[699_mutex_lock_sleep_wait|뮤텍스 락]] ([[699_mutex_lock_sleep_wait|Mutex Lock]] / [[283_mutual_exclusion|Mutual Exclusion]] [[510_lock|Lock]])
232. acquire() / release() 함수
233. [[222_spinlock|스핀락]] ([[222_spinlock|Spinlock]]) - [[227_busy_waiting|바쁜 대기]]([[227_busy_waiting|Busy Waiting]]), 다중 코어에서 [[211_context_switch|문맥 교환]] 오버헤드 없음
234. [[224_semaphore|세마포어]] ([[224_semaphore|Semaphore]]) - S 정수 변수, wait(P), [[130_signal|signal]](V) 원자적 연산
235. [[225_binary_semaphore|이진 세마포어]] ([[225_binary_semaphore|Binary Semaphore]]) = 뮤텍스와 유사
236. [[226_counting_semaphore|카운팅 세마포어]] ([[226_counting_semaphore|Counting Semaphore]]) - 유한한 자원 풀 관리
237. 블로킹 [[224_semaphore|세마포어]] - [[089_wait_queue|대기 큐]] (Sleep & Wakeup) 사용, [[227_busy_waiting|바쁜 대기]] 없음
238. [[229_monitor|모니터]] ([[229_monitor|Monitor]]) - 추상 자료형 구조, [[283_mutual_exclusion|상호 배제]] 자동 보장 (High-level 구조)
239. [[228_condition_variable|조건 변수]] ([[228_condition_variable|Condition Variable]]) - x.wait(), x.[[130_signal|signal]]()
240. [[229_monitor|모니터]] 시그널 의미론 - [[130_signal|Signal]] and Wait vs [[130_signal|Signal]] and Continue
241. [[315_livelock_vs_deadlock|라이브락]] ([[315_livelock_vs_deadlock|Livelock]]) - [[216_progress_in_synchronization|진행]]은 하나 유효한 작업 불가 (양보만 반복)
242. [[205_priority_inversion|우선순위 역전]] ([[205_priority_inversion|Priority Inversion]]) - 하위 프로세스가 락을 쥐고 있어 상위 프로세스 대기
243. 우선순위 [[234_uml_class_relationships_generalization_dependency|상속]] ([[206_priority_inheritance|Priority Inheritance]] [[295_protocol_field_tcp_udp_icmp|Protocol]]) - 락을 쥔 프로세스에 임시로 우선순위 부여
244. [[244_priority_ceiling_protocol|우선순위 올림]] ([[244_priority_ceiling_protocol|Priority Ceiling Protocol]])
245. [[245_classic_synchronization_problems|고전적 동기화 문제들]]
246. [[246_bounded_buffer_producer_consumer|유한 버퍼 문제]] ([[246_bounded_buffer_producer_consumer|Bounded-Buffer Problem]]) / 생산자-소비자 (Producer-Consumer) 문제
247. [[247_readers_writers_problem|독자-저자 문제]] ([[247_readers_writers_problem|Readers-Writers Problem]]) - 제1유형(독자 우선), 제2유형(저자 우선)
248. [[248_dining_philosophers_problem|식사하는 철학자 문제]] ([[248_dining_philosophers_problem|Dining-Philosophers Problem]]) - 교착상태 및 [[314_starvation_prevention|기아 상태]] 예방
249. [[249_java_synchronization|자바 동기화]] - synchronized 키워드, [[229_monitor|모니터]] 락, wait()/notify()
250. [[790_posix_threads_pthreads_standard_api|Pthreads]] [[212_synchronization_mechanisms|동기화]] - pthread_mutex_t, pthread_cond_t, [[222_spinlock|스핀락]], 배리어
251. [[251_windows_synchronization|윈도우 동기화]] - 크리티컬 섹션 객체(유저모드), [[168_dispatcher|디스패처]] 객체([[022_kernel_role|커널]]모드 - 이벤트, 뮤텍스, [[224_semaphore|세마포어]])
252. 이벤트 객체 (Event Object) - [[092_thread_lwp|스레드]] 간 [[130_signal|신호]] 전달
253. 리눅스 [[212_synchronization_mechanisms|동기화]] - 원자적 정수, [[222_spinlock|스핀락]], [[224_semaphore|세마포어]], 락 메커니즘
254. [[254_rcu_read_copy_update|RCU]] ([[254_rcu_read_copy_update|Read-Copy-Update]]) - 리눅스 고성능 [[212_synchronization_mechanisms|동기화]] (읽기는 락 프리, [[289_cqrs_db|쓰기]]는 복사 후 갱신)
255. SeqLock (순차 락) - [[280_read_write_lock|읽기-쓰기 락]]의 대안, [[059_counter|카운터]] 기반
256. [[256_lock_free_data_structures|락-프리]] ([[256_lock_free_data_structures|Lock-free]]) 자료구조 - [[768_cas_compare_and_swap_lock_free|CAS]] 연산 적극 활용
257. 웨이트-프리 (Wait-free) [[001_algorithm_definition|알고리즘]]
258. [[079_kube_scheduler_pod_placement|스케줄러]] 일드 (sched_yield) - [[275_lock_contention_monitoring|락 경합]] 시 자발적 CPU 양보
259. ABA 문제 - [[768_cas_compare_and_swap_lock_free|CAS]] 연산 시 값이 변경되었다가 원복된 것을 인지하지 못하는 오류
260. ABA 문제 해결책 - 태그/[[288_version_ihl_tos_total_length|버전]] 관리
261. 장벽 (Barrier) [[212_synchronization_mechanisms|동기화]] - 여러 [[092_thread_lwp|스레드]]가 특정 지점에 도달할 때까지 대기
262. 양방향 랑데부 (Rendezvous)
263. 티켓 락 (Ticket [[510_lock|Lock]]) - [[261_fifo_page_replacement|FIFO]] 보장 [[222_spinlock|스핀락]]
264. 큐잉 [[222_spinlock|스핀락]] (MCS [[510_lock|Lock]] / qspinlock) - [[377_numa_allocation|NUMA]] 환경 [[222_spinlock|스핀락]] 최적화
265. 낙관적 병행성 제어 ([[223_optimistic_concurrency_control_validation|Optimistic Concurrency Control]])
266. 비관적 병행성 제어 (Pessimistic [[508_concurrency_control|Concurrency Control]])
267. [[267_atomic_transaction|원자적 트랜잭션]] ([[267_atomic_transaction|Atomic Transaction]]) 개념
268. [[268_software_transactional_memory|소프트웨어 트랜잭셔널 메모리]] ([[268_software_transactional_memory|STM]])
269. [[269_htm_intel_tsx|하드웨어 트랜잭셔널 메모리]] ([[513_htm|HTM]] - Intel TSX)
270. [[270_lock_elision|락 엘리전]] ([[270_lock_elision|Lock Elision]]) - 하드웨어 지원 락 우회
271. [[103_thread_pool|스레드 풀]] 스케줄링 [[275_lock_contention_monitoring|락 경합]] ([[271_work_stealing|Work Stealing]])
272. [[272_double_checked_locking|더블 체크드 락킹]] ([[272_double_checked_locking|Double-Checked Locking]]) [[128_water_scrum_fall_anti_pattern|안티패턴]] 및 해결 (volatile)
273. 세큐어 코딩에서의 [[212_synchronization_mechanisms|동기화]] 약점 ([[273_toctou|TOCTOU]]: Time of Check to Time of Use)
274. [[214_critical_section|임계 구역]] 크기 최소화 기법
275. [[275_lock_contention_monitoring|락 경합]] ([[275_lock_contention_monitoring|Lock Contention]]) [[229_monitor|모니터]]링 도구
276. 데드락 회피를 위한 [[276_lock_hierarchy|Lock Hierarchy]] ([[276_lock_hierarchy|락 순서화]])
277. [[224_semaphore|세마포어]]를 이용한 순서 제어 ([[277_semaphore_ordering|Ordering]])
278. [[225_binary_semaphore|이진 세마포어]] vs 뮤텍스 차이 ([[278_binary_semaphore_vs_mutex|소유권 유무]])
279. [[279_reentrant_lock|재진입 가능 락]] ([[279_reentrant_lock|Reentrant Lock]] / Recursive [[510_lock|Lock]])
280. [[280_read_write_lock|읽기-쓰기 락]] ([[280_read_write_lock|Read-Write Lock]]) - 다중 읽기 허용, [[289_cqrs_db|쓰기]] 배타적

## 5. [[281_deadlock_definition|교착 상태]] ([[281_deadlock_definition|Deadlock]]) (40개)
281. [[281_deadlock_definition|교착 상태]] ([[281_deadlock_definition|Deadlock]]) 정의 - 대기 중인 프로세스들이 자원을 점유한 채로 결코 일어나지 않을 사건을 기다리는 상태
282. [[281_deadlock_definition|교착 상태]] 발생 4가지 필요조건 ([[282_deadlock_four_necessary_conditions|모두 만족해야 발생]])
283. [[283_mutual_exclusion|상호 배제]] ([[283_mutual_exclusion|Mutual Exclusion]]) - 자원은 비공유 모드로만 사용 가능
284. [[284_hold_and_wait|점유하며 대기]] ([[284_hold_and_wait|Hold-and-Wait]]) - 자원을 보유한 상태로 다른 자원 대기
285. [[285_no_preemption|비선점]] ([[285_no_preemption|No Preemption]]) - 다른 프로세스의 자원을 강제로 뺏을 수 없음
286. [[286_circular_wait|순환 대기]] ([[286_circular_wait|Circular Wait]]) - [[305_wait_for_graph|대기 그래프]]가 사이클(Cycle)을 형성
287. [[287_resource_allocation_graph|자원 할당 그래프]] ([[287_resource_allocation_graph|Resource-Allocation Graph]]) - 정점(프로세스, 자원)과 간선(요청, 할당)
288. 단일 인스턴스 자원 환경 - 사이클 존재 = [[281_deadlock_definition|교착 상태]]
289. 다중 인스턴스 자원 환경 - 사이클 존재 != [[281_deadlock_definition|교착 상태]] (필요 조건일 뿐)
290. [[281_deadlock_definition|교착 상태]] 처리 방법 3가지 - 예방/회피, 탐지/[[658_ir_recovery|복구]], 무시
291. [[291_ostrich_algorithm|타조 알고리즘]] ([[291_ostrich_algorithm|Ostrich Algorithm]]) - 대부분의 OS가 채택하는 무시 [[268_strategy_pattern|전략]]
292. [[292_deadlock_prevention|교착 상태 예방]] ([[292_deadlock_prevention|Deadlock Prevention]]) - 4조건 중 하나를 원천적 부정 (효율성 매우 낮음)
293. [[293_deny_mutual_exclusion|상호 배제 부정]] - 모든 자원 공유 (현실성 없음)
294. [[294_deny_hold_and_wait|점유 대기 부정]] - 실행 전 모든 자원 일괄 할당, 또는 자원 없을 때만 요청 (기아 가능성, 자원 낭비)
295. [[295_deny_no_preemption|비선점 부정]] - 자원 요청 대기 시 보유 자원 강제 반납
296. [[296_deny_circular_wait|순환 대기 부정]] - 자원에 고유 번호(순서) 부여, 오름차순으로만 요청 (가장 현실적 예방책)
297. [[297_deadlock_avoidance|교착 상태 회피]] ([[297_deadlock_avoidance|Deadlock Avoidance]]) - 실행 전 [[041_resource_allocation|자원 할당]] 상태를 검사하여 안전한 경우에만 승인
298. [[298_safe_state|안전 상태]] ([[298_safe_state|Safe State]]) - 모든 프로세스가 정상 종료될 수 있는 안전 순서([[093_safe_scaled_agile_framework_art_pi|Safe]] Sequence)가 존재
299. [[299_unsafe_state|불안전 상태]] ([[299_unsafe_state|Unsafe State]]) - [[281_deadlock_definition|교착 상태]]가 발생할 가능성이 있는 상태
300. 단일 인스턴스 환경의 회피 - [[287_resource_allocation_graph|자원 할당 그래프]] [[001_algorithm_definition|알고리즘]] (예약 간선/Claim Edge 활용)
301. 다중 인스턴스 환경의 회피 - 은행원 [[001_algorithm_definition|알고리즘]] (Banker's [[001_algorithm_definition|Algorithm]], 에츠허르 데이크스트라 제안)
302. [[302_bankers_data_structure|은행원 알고리즘 자료구조]] - Available, Max, Allocation, Need 행렬
303. [[303_bankers_limitations|은행원 알고리즘 한계]] - 프로세스 수, 최대 자원량 사전 숙지 불가, 오버헤드 큼
304. [[304_deadlock_detection|교착 상태 탐지]] ([[304_deadlock_detection|Deadlock Detection]]) - [[001_algorithm_definition|알고리즘]]을 주기적으로 실행하여 데드락 [[396_validation|확인]]
305. [[305_wait_for_graph|대기 그래프]] ([[305_wait_for_graph|Wait-for Graph]]) - 자원 정점을 제거하고 프로세스 간 간선만 남긴 [[070_graph_datastructure|그래프]] (단일 자원 탐지용)
306. [[306_detection_overhead|탐지 알고리즘의 오버헤드]] - 언제, 얼마나 자주 실행할 것인가?
307. [[307_recovery_from_deadlock|교착 상태 복구]] ([[307_recovery_from_deadlock|Recovery from Deadlock]]) - 데드락 해소 조치
308. [[107_process_termination|프로세스 종료]] 방식 - [[281_deadlock_definition|교착 상태]] 프로세스 전체 강제 종료 ([[308_abort_all|Abort all]])
309. 프로세스 순차 종료 방식 - 하나씩 종료하며 사이클 해소 여부 [[396_validation|확인]]
310. [[310_victim_selection|종료 대상 선택]] ([[310_victim_selection|희생자 선택]]) 기준 - 프로세스 중요도, 연산 시간, 보유 자원 수
311. [[311_resource_preemption|자원 선점]] ([[311_resource_preemption|Resource Preemption]]) 방식 - 다른 프로세스의 자원을 강제로 뺏음
312. [[310_victim_selection|희생자 선택]] ([[310_victim_selection|Victim Selection]]) 최소 비용 기준
313. [[313_rollback|후퇴]] ([[313_rollback|Rollback]]) - 프로세스를 안전한 상태로 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 후 재시작
314. [[314_starvation_prevention|기아 상태]] ([[314_starvation_prevention|Starvation]]) 발생 방지 ([[310_victim_selection|희생자 선택]]에 횟수 제한)
315. [[315_livelock_vs_deadlock|라이브락]] ([[315_livelock_vs_deadlock|Livelock]])과 [[281_deadlock_definition|교착 상태]]의 차이점
316. [[316_synchronization_bug_debugging|동기화 결함]] ([[316_synchronization_bug_debugging|순환 의존성]]) 코드 레벨 디버깅 기법
317. [[317_lockdep_lock_ordering|락 오더링]] ([[317_lockdep_lock_ordering|Lock Ordering]]) 다이나믹 [[395_verification_process_review|검증]] 도구 (Lockdep in Linux)
318. [[136_variance|분산]] 시스템에서의 [[304_deadlock_detection|교착 상태 탐지]] - [[136_variance|분산]] [[281_deadlock_definition|교착 상태]] [[070_graph_datastructure|그래프]]
319. [[292_deadlock_prevention|교착 상태 예방]] 메커니즘을 위한 [[573_timeout_retry_backoff_strategy|타임아웃]] ([[319_timeout_prevention|Timeout]]) 활용
320. [[320_two_phase_locking_deadlock|2단계 잠금 프로토콜]] ([[320_two_phase_locking_deadlock|2PL]])과 데드락 ([[002_database_definition|데이터베이스]] 연관)

## 6. 메인 메모리 관리 (70개)
321. [[252_memory_hierarchy|메모리 계층 구조]] ([[252_memory_hierarchy|Memory Hierarchy]])와 [[057_register|레지스터]]-캐시-메인메모리 접근
322. [[322_logical_virtual_address|논리 주소]] (Logical/Virtual Address) - CPU가 [[087_process_state_transition|생성]]하는 주소
323. [[323_physical_address|물리 주소]] ([[323_physical_address|Physical Address]]) - 메모리 장치가 보는 주소
324. [[324_address_binding_stages|주소 바인딩]] ([[324_address_binding_stages|Address Binding]]) 3단계 시점
325. [[325_compile_time_binding|컴파일 시간 바인딩]] ([[325_compile_time_binding|Compile Time]]) - 절대 코드 (Absolute [[082_process_memory_structure|Code]]) [[087_process_state_transition|생성]]
326. [[326_load_time_binding|적재 시간 바인딩]] ([[326_load_time_binding|Load Time]]) - 재배치 가능 코드 (Relocatable [[082_process_memory_structure|Code]])
327. [[327_execution_time_binding|실행 시간 바인딩]] ([[327_execution_time_binding|Execution Time]]) - 실행 중 주소 변경, [[328_mmu|MMU]] 필요 (현대 OS 기본)
328. [[328_mmu|MMU]] ([[328_mmu|Memory-Management Unit]]) - [[322_logical_virtual_address|논리 주소]]를 [[323_physical_address|물리 주소]]로 동적 변환하는 하드웨어
329. [[329_base_register|베이스 레지스터]] (Base/Relocation [[175_register_addressing|Register]]) - 물리 시작 주소 보유
330. [[330_limit_register|한계 레지스터]] ([[330_limit_register|Limit Register]]) - [[307_memory_protection|메모리 보호]], 주소 범위 검사
331. [[331_dynamic_loading|동적 적재]] ([[331_dynamic_loading|Dynamic Loading]]) - 루틴 호출 시점에 메모리 적재 (효율성)
332. [[332_dynamic_linking|동적 연결]] ([[332_dynamic_linking|Dynamic Linking]]) - 실행 시점에 [[336_library_vs_framework|라이브러리]] 연결 (.dll, .so)
333. [[333_shared_library|공유 라이브러리]] ([[333_shared_library|Shared Library]]) 스터브 ([[460_stub_test_double|Stub]]) 코드
334. [[334_static_linking|정적 연결]] ([[334_static_linking|Static Linking]])
335. [[335_swapping|스와핑]] ([[335_swapping|Swapping]]) - 메모리 부족 시 프로세스를 디스크 백킹 스토어(Backing Store)로 쫓아냄
336. [[336_swap_out_in|스왑 아웃]] ([[336_swap_out_in|Swap out]]) / 스왑 인 (Swap in)
337. [[337_standard_vs_paging_swapping|표준 스와핑]] ([[337_standard_vs_paging_swapping|전체 프로세스]]) vs [[259_paging|페이징]] 시스템 [[335_swapping|스와핑]] ([[286_page_frame|페이지]] 단위)
338. [[338_contiguous_memory_allocation|연속 메모리 할당]] ([[338_contiguous_memory_allocation|Contiguous Memory Allocation]])
339. [[339_fixed_partition|고정 분할 방식]] ([[339_fixed_partition|Fixed Partition]])
340. [[340_variable_partition|가변 분할 방식]] ([[340_variable_partition|Variable Partition]])
341. [[341_internal_fragmentation|내부 단편화]] ([[341_internal_fragmentation|Internal Fragmentation]]) - 할당된 공간 내 남는 공간
342. [[342_external_fragmentation|외부 단편화]] ([[342_external_fragmentation|External Fragmentation]]) - 가용 공간은 충분하나 불연속적이라 할당 불가
343. 동적 메모리 할당 문제 (가변 분할 배치 [[001_algorithm_definition|알고리즘]])
344. [[344_first_fit|최초 적합]] ([[344_first_fit|First-Fit]]) - 첫 번째 충분한 공간 할당 (속도 빠름)
345. [[345_best_fit|최적 적합]] ([[345_best_fit|Best-Fit]]) - 가장 크기가 비슷한 공간 (자투리 최소화, 검색 시간 소요)
346. [[346_worst_fit|최악 적합]] ([[346_worst_fit|Worst-Fit]]) - 가장 큰 공간 할당 (큰 가용 공간 남김)
347. [[347_compaction|압축]] ([[347_compaction|Compaction]]) - [[342_external_fragmentation|외부 단편화]] 해결, 동적 재배치 시에만 가능, 오버헤드 막심
348. [[348_buddy_system|버디 시스템]] ([[348_buddy_system|Buddy System]]) 할당기 - 2의 승수로 분할 및 병합 ([[342_external_fragmentation|외부 단편화]] 절충)
349. [[349_slab_allocator|슬랩 할당기]] ([[349_slab_allocator|Slab Allocator]]) - [[022_kernel_role|커널]] 객체 [[456_caching|캐싱]], [[291_fragmentation_and_reassembly_process|단편화]] 방지 및 속도 향상
350. [[350_non_contiguous_memory_allocation|비연속 메모리 할당]] ([[350_non_contiguous_memory_allocation|Non-contiguous Memory Allocation]])
351. [[259_paging|페이징]] ([[259_paging|Paging]]) - 물리 메모리를 프레임(Frame), [[369_logic_bomb|논리]] 메모리를 [[286_page_frame|페이지]]([[286_page_frame|Page]])로 고정 크기 분할
352. [[352_page_size|페이지 크기]] ([[352_page_size|Page Size]]) - 주로 4KB. 커지면 [[341_internal_fragmentation|내부 단편화]] 증가, 테이블 크기 감소
353. [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]) - [[286_page_frame|페이지]] 번호를 프레임 번호로 매핑
354. [[354_ptbr_ptlr|PTBR]] ([[354_ptbr_ptlr|Page-Table Base Register]]) / PTLR ([[286_page_frame|Page]]-Table Length [[175_register_addressing|Register]])
355. [[259_paging|페이징]]의 [[307_memory_protection|메모리 보호]] - [[386_valid_invalid_bit|유효-무효 비트]] ([[355_paging_memory_protection|Valid-Invalid Bit]])
356. [[356_shared_pages|페이징에서의 공유 페이지]] ([[356_shared_pages|Shared Pages]]) - 읽기 전용 코드([[148_reentrant_code|Reentrant code]]) 공유
357. [[357_tlb|TLB]] ([[357_tlb|Translation Look-aside Buffer]]) - 주소 변환 캐시([[250_sram|SRAM]] 연관 메모리 하드웨어)
358. [[357_tlb|TLB]] 적중 ([[358_tlb_hit_miss|TLB Hit]]) / [[357_tlb|TLB]] 미스 ([[357_tlb|TLB]] Miss)
359. [[357_tlb|TLB]] [[264_hit_ratio|적중률]] ([[359_effective_access_time|Hit Ratio]]) / 실질 메모리 접근 시간 (EAT, [[359_effective_access_time|Effective Access Time]])
360. [[360_asid|ASID]] ([[360_asid|Address-Space Identifier]]) - [[357_tlb|TLB]] 내 프로세스 [[655_ir_detection_analysis|식별]], 플러시(Flush) 최소화
361. [[361_hierarchical_paging|다단계 페이징]] ([[361_hierarchical_paging|Hierarchical Paging]]) - [[353_page_table|페이지 테이블]] 크기 문제 해결 (2단계, 3단계...)
362. [[362_hashed_page_table|해시 페이지 테이블]] ([[362_hashed_page_table|Hashed Page Table]]) - 주소 공간이 64비트 이상일 때 사용
363. [[363_inverted_page_table|역 페이지 테이블]] ([[363_inverted_page_table|Inverted Page Table]]) - 시스템 내 단 하나의 [[353_page_table|페이지 테이블]], 프레임 중심
364. [[364_segmentation|세그멘테이션]] ([[364_segmentation|Segmentation]]) - 사용자 관점의 가변 크기 [[369_logic_bomb|논리]]적 단위(함수, 객체) 분할
365. [[365_segment_table|세그먼트 테이블]] ([[365_segment_table|Segment Table]]) - 기준(Base) 주소와 한계(Limit) 길이
366. [[366_segmentation_external_fragmentation|세그멘테이션과 외부 단편화]] ([[366_segmentation_external_fragmentation|가변 크기이므로 재발생]])
367. [[367_paged_segmentation|세그멘테이션 기반 페이징]] ([[367_paged_segmentation|Paged Segmentation]]) - 인텔 [[198_x86_architecture|x86 아키텍처]] (세그먼트를 다시 [[286_page_frame|페이지]]로)
368. [[022_kernel_role|커널]] 메모리 할당 방식 (kmalloc, vmalloc)
369. [[369_memory_pool|메모리 풀]] ([[369_memory_pool|Memory Pool]]) 기법
370. 파편화 관리 및 조각 모음 - 리눅스 메모리 컴팩션 ([[370_memory_compaction|Memory Compaction]])
371. [[371_huge_pages|거대 페이지]] ([[371_huge_pages|Huge Pages]] / Transparent [[371_huge_pages|Huge Pages]]) - [[357_tlb|TLB]] 미스 감소
372. 아키텍처 종속적인 [[328_mmu|MMU]] 인터페이스
373. ARM / x86의 메모리 매핑 아키텍처 차이
374. 주소 공간 무작위 배치 ([[374_aslr|ASLR]], Address Space Layout Randomization)
375. [[375_memory_protection_keys|메모리 보호 키]] ([[375_memory_protection_keys|Memory Protection Keys]])
376. 캐시 인식 [[001_dikw_pyramid|데이터]] 구조 ([[376_cache_aware_data_structures|Cache-aware Data Structures]])
377. [[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]]) 아키텍처와 메모리 할당 [[164_policy|정책]]
378. 로컬 노드 할당 vs 인터리브 할당
379. [[379_cache_coloring|캐시 컬러링]] ([[379_cache_coloring|Cache Coloring]]) / [[286_page_frame|페이지]] 컬러링
380. [[380_garbage_collection|가비지 컬렉션]] ([[380_garbage_collection|Garbage Collection]]) 기초 - [[316_reference_pattern_nosql|참조]] 카운팅, Mark-and-Sweep

## 7. [[381_virtual_memory|가상 메모리]] 관리 (60개)
381. [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]]) 개념 - 물리 메모리보다 큰 프로그램 실행 가능
382. [[382_virtual_address_space|가상 주소 공간]] ([[382_virtual_address_space|Virtual Address Space]])
383. [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]]) - 필요한 [[286_page_frame|페이지]]만 메모리에 적재
384. [[384_pure_demand_paging|순수 요구 페이징]] ([[384_pure_demand_paging|Pure Demand Paging]]) - 시작할 때 아무것도 안 올림
385. [[385_prepaging|선행 페이징]] ([[385_prepaging|Prepaging]]) - [[387_page_fault|페이지 부재]] 감소를 위해 미리 묶어 올림
386. [[386_valid_invalid_bit|유효-무효 비트]] ([[355_paging_memory_protection|Valid-Invalid Bit]]) - 적재 여부 표시
387. [[387_page_fault|페이지 부재]] ([[387_page_fault|Page Fault]]) - 무효 [[286_page_frame|페이지]] 접근 시 발생하는 [[677_trap_based_system_call_implementation|트랩]]([[016_interrupt_mechanism|인터럽트]])
388. [[387_page_fault|페이지 부재]] 처리 과정 6단계 (OS [[677_trap_based_system_call_implementation|트랩]], [[057_register|레지스터]] 저장, 디스크 읽기, 문맥교환 등)
389. [[389_page_fault_rate_eat|페이지 부재율]] ([[389_page_fault_rate_eat|Page Fault Rate]]) 와 실질 접근 시간 (EAT) [[282_performance_tactics|성능]] [[083_relationship_in_er_model|관계]]
390. [[390_swap_space|스왑 공간]] ([[390_swap_space|Swap Space]]) / 베이킹 스토어 (Backing Store)
391. [[391_anonymous_memory|익명 메모리]] ([[391_anonymous_memory|Anonymous Memory]]) - [[501_file_definition_logical_record|파일]] 시스템과 무관한 힙/[[057_stack|스택]] [[001_dikw_pyramid|데이터]] (스왑 영역 사용)
392. [[392_file_backed_memory|파일 지원 메모리]] ([[392_file_backed_memory|File-backed Memory]]) - 실행 [[501_file_definition_logical_record|파일]], [[333_shared_library|공유 라이브러리]]
393. [[393_copy_on_write|쓰기 시 복사]] ([[542_cow_file_system|COW]], [[542_cow_file_system|Copy-on-Write]]) - fork() 시 자원 공유하다 쓸 때 [[286_page_frame|페이지]] [[016_replication_factor|복제]]
394. [[394_vfork|vfork]]() - [[542_cow_file_system|COW]] 조차 없는 초경량 포크 (즉시 exec() 호출 조건)
395. [[260_page_replacement|페이지 교체]] ([[260_page_replacement|Page Replacement]])의 필요성 - 프레임 가용 공간 부족 시 (Over-allocation)
396. [[396_dirty_bit|변경 비트]] (Modify [[086_fenwick_tree|Bit]] / [[396_dirty_bit|Dirty Bit]]) - 교체 시 디스크 기록 여부 결정, 디스크 I/O 최적화
397. [[397_frame_allocation|프레임 할당]] ([[397_frame_allocation|Frame Allocation]]) [[001_algorithm_definition|알고리즘]]
398. [[398_equal_vs_proportional_allocation|균등 할당]] ([[398_equal_vs_proportional_allocation|Equal Allocation]]) vs 비례 할당 (Proportional Allocation)
399. [[399_global_replacement|전역 교체]] ([[399_global_replacement|Global Replacement]]) - [[337_standard_vs_paging_swapping|전체 프로세스]] 프레임 대상 ([[139_throughput|처리량]] 높음, 주로 사용)
400. [[400_local_replacement|지역 교체]] ([[400_local_replacement|Local Replacement]]) - 자신의 프레임 풀 내에서만 교체
401. [[401_page_replacement_algorithms|페이지 교체 알고리즘]] ([[401_page_replacement_algorithms|Page Replacement Algorithms]])
402. [[402_optimal_page_replacement|최적 교체 알고리즘]] ([[724_optimal_page_replacement_unrealizable|OPT]], Optimal) - 앞으로 가장 오랫동안 안 쓸 [[260_page_replacement|페이지 교체]] (구현 불가, 비교 기준)
403. 벨라디의 모순 (Belady's [[530_anomaly|Anomaly]]) - 프레임을 늘렸는데 오히려 [[387_page_fault|페이지 부재]]가 증가하는 현상
404. [[261_fifo_page_replacement|FIFO]] (First-In, First-Out) 교체 - 가장 먼저 들어온 [[260_page_replacement|페이지 교체]] (벨라디 모순 발생)
405. [[262_lru_page_replacement|LRU]] ([[262_lru_page_replacement|Least Recently Used]]) 교체 - 가장 오랫동안 사용되지 않은 [[260_page_replacement|페이지 교체]] (타임스탬프, [[057_stack|스택]] 하드웨어 지원 필요)
406. [[262_lru_page_replacement|LRU]] [[012_approximation_algorithm|근사 알고리즘]] ([[406_lru_approximation|LRU Approximation]]) - [[316_reference_pattern_nosql|참조]] [[073_bit|비트]] ([[316_reference_pattern_nosql|Reference]] [[086_fenwick_tree|Bit]]) 사용
407. [[407_second_chance_algorithm|2차 기회 알고리즘]] (Second-Chance / [[302_clock_algorithm|Clock Algorithm]]) - [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]가 1이면 0으로 바꾸고 통과, 0이면 교체
408. 개선된 [[407_second_chance_algorithm|2차 기회 알고리즘]] - [[316_reference_pattern_nosql|참조]] [[073_bit|비트]]와 [[396_dirty_bit|변경 비트]]의 조합 (0,0 -> 0,1 -> 1,0 -> 1,1 우선순위 교체)
409. [[263_lfu_page_replacement|LFU]] ([[263_lfu_page_replacement|Least Frequently Used]]) [[001_algorithm_definition|알고리즘]] - [[316_reference_pattern_nosql|참조]] 횟수가 가장 적은 [[260_page_replacement|페이지 교체]]
410. [[410_mfu_algorithm|MFU]] ([[410_mfu_algorithm|Most Frequently Used]]) [[001_algorithm_definition|알고리즘]]
411. [[411_aging_algorithm|에이징]] ([[182_aging|Aging]]) 기반 [[260_page_replacement|페이지 교체]] 로직
412. [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]]) - 프로세스가 실제 실행보다 [[259_paging|페이징]]([[335_swapping|스와핑]])에 더 많은 시간을 보내는 현상
413. [[258_degree_of_multiprogramming|다중 프로그래밍 정도]] ([[258_degree_of_multiprogramming|Degree of Multiprogramming]])와 CPU 이용률 [[083_relationship_in_er_model|관계]] [[070_graph_datastructure|그래프]]
414. [[414_cause_of_thrashing|스래싱 원인]] - 각 프로세스가 필요로 하는 최소 프레임 확보 실패
415. [[415_locality_model|지역성 모델]] ([[415_locality_model|Locality Model]]) - 시간적, [[248_spatial_locality|공간적 지역성]]
416. [[416_working_set_model|워킹 셋 모델]] ([[416_working_set_model|Working-Set Model]]) - 특정 시간 구간(윈도우) 동안 [[316_reference_pattern_nosql|참조]]된 [[286_page_frame|페이지]] 집합 보장
417. [[266_page_fault_frequency|페이지 부재 빈도]] ([[306_pff|PFF]], [[286_page_frame|Page]]-Fault Frequency) 모델 - 상한/하한 설정하여 동적 [[397_frame_allocation|프레임 할당]] 조절
418. [[418_memory_mapped_file_mmap|메모리 매핑 파일]] (Memory-Mapped Files, [[749_memory_mapped_file_mmap|mmap]])
419. [[501_file_definition_logical_record|파일]] I/O를 메모리 접근으로 변환, [[536_buffer_cache_page_cache|버퍼 캐시]] 활용, 프로세스 간 [[118_shared_memory|공유 메모리]]로 사용 가능
420. 메모리 맵 I/O (Memory-Mapped I/O) - 디바이스 [[057_register|레지스터]] 매핑
421. [[022_kernel_role|커널]] 메모리 할당의 특징 - 물리적으로 연속되어야 함 (주로 [[348_buddy_system|버디 시스템]] + [[349_slab_allocator|슬랩 할당기]])
422. [[422_page_pinning_locking|페이지 고정]] ([[286_page_frame|Page]] Pinning / [[213_locking_mechanism_concurrency_control|Locking]]) - I/O 대기 중인 [[286_page_frame|페이지]]가 스왑아웃되지 않게 고정 (mlock)
423. [[423_large_page_performance|대형 페이지]] (Large [[286_page_frame|Page]] / Transparent Hugepage)의 [[381_virtual_memory|가상 메모리]] [[282_performance_tactics|성능]] 이점
424. ZRAM / [[022_kernel_role|커널]] 스왑 [[347_compaction|압축]] 기술 - 스왑 디스크 I/O 대신 메모리 내 [[159_compression|데이터 압축]] 보관
425. [[425_oom_killer_score|OOM Killer]] ([[425_oom_killer_score|Out-of-Memory]]) 작동 우선순위 점수 (oom_score) 매커니즘
426. [[377_numa_allocation|NUMA]] 환경의 [[381_virtual_memory|가상 메모리]] 스케줄링 ([[377_numa_allocation|NUMA]] 노드 별 [[286_page_frame|페이지]] 할당 / numactl)
427. 캐시 친화적 [[381_virtual_memory|가상 메모리]] 관리 배치
428. [[428_vma_struct|VMA]] ([[428_vma_struct|Virtual Memory Area]]) 구조체 (리눅스 [[022_kernel_role|커널]] 프로세스 주소 공간 매핑)
429. [[429_minor_vs_major_page_fault|마이너 페이지 폴트]] ([[429_minor_vs_major_page_fault|Minor Page Fault]]) vs 메이저 [[720_page_fault_isr|페이지 폴트]] (Major [[387_page_fault|Page Fault]] / 디스크 I/O 동반)
430. [[430_demand_zero_paging|수요 페이지 제로화]] ([[430_demand_zero_paging|Demand Zero Paging]]) - [[083_bss_segment|BSS]] 영역 보안 할당
431. [[431_dirty_page_writeback|더티 페이지 쓰기]] ([[431_dirty_page_writeback|Dirty Page Writeback]]) 메커니즘 (pdflush / flusher [[092_thread_lwp|스레드]])
432. [[379_cache_coloring|캐시 컬러링]] ([[379_cache_coloring|Cache Coloring]])에 의한 [[286_page_frame|페이지]] 매핑 최적화
433. [[363_inverted_page_table|역 페이지 테이블]] 탐색 최적화 [[667_hash_function_integrity_one_way|해시 함수]]
434. [[434_asynchronous_page_fault|비동기식 페이지 폴트]] ([[434_asynchronous_page_fault|Asynchronous Page Faults]]) 핸들링
435. [[357_tlb|TLB]] 슛다운 ([[435_tlb_shootdown|TLB Shootdown]]) - 멀티코어 환경에서 타 코어의 [[357_tlb|TLB]] 무효화 오버헤드
436. [[022_kernel_role|커널]] [[353_page_table|페이지 테이블]] 격리 ([[578_kpti|KPTI]], [[022_kernel_role|Kernel]] [[286_page_frame|Page]]-Table [[195_isolation_concurrency_control|Isolation]]) - [[482_meltdown|Meltdown]] 취약점 대응망
437. [[437_memory_encryption_virtualization|메모리 암호화 가상화]] (AMD SME/SEV, [[480_intel_sgx|Intel SGX]])
438. [[438_unified_buffer_cache_page_cache|파일시스템 버퍼 캐시]]([[536_buffer_cache_page_cache|Buffer Cache]])와 [[381_virtual_memory|가상 메모리]] [[286_page_frame|페이지]] 캐시([[286_page_frame|Page]] Cache)의 통합 원리
439. [[062_cgroups|Cgroups]] 메모리 서브시스템의 자원 제한 ([[439_cgroups_memory_limit|Memory Limit]]) 동작
440. [[615_ebpf|eBPF]] 기반 메모리 할당 트레이싱

## 8. 저장장치 및 입출력 (I/O) 시스템 (60개)
441. I/O 장치의 [[104_classification_analysis|분류]] - [[442_block_device|블록 장치]] ([[442_block_device|Block Device]]) vs [[443_character_device|문자 장치]] ([[443_character_device|Character Device]])
442. [[442_block_device|블록 장치]] - 하드 디스크, [[327_ssd|SSD]] (블록 단위 읽기/[[289_cqrs_db|쓰기]], 랜덤 액세스 가능)
443. [[443_character_device|문자 장치]] - 키보드, 마우스, [[149_serial_communication_rs232_rs485|직렬]] [[446_port_and_bus|포트]] (스트림 단위, 순차 접근)
444. [[444_network_device|네트워크 장치]] ([[444_network_device|소켓 인터페이스]])
445. I/O 하드웨어 인터페이스 요소 - [[001_dikw_pyramid|데이터]] [[057_register|레지스터]], [[167_status_register|상태 레지스터]], 제어 [[057_register|레지스터]]
446. [[446_port_and_bus|포트]] ([[446_port_and_bus|Port]]) / [[344_bus|버스]] ([[344_bus|Bus]]) - [[356_pcie|PCIe]], [[359_usb|USB]], [[341_sata|SATA]], [[482_nvme|NVMe]]
447. 메모리 맵 I/O (Memory-mapped I/O) vs 분리된 I/O (Isolated I/O / [[446_port_and_bus|Port]] I/O)
448. [[448_polling_programmed_io|폴링]] ([[747_io_polling_overhead|Polling]] / Programmed I/O) - 상태 [[073_bit|비트]]를 지속적으로 호스트가 읽음 ([[227_busy_waiting|바쁜 대기]])
449. [[016_interrupt_mechanism|인터럽트]] 구동 I/O ([[016_interrupt_mechanism|Interrupt]]-driven I/O) - 완료 시 장치가 CPU에 [[016_interrupt_mechanism|인터럽트]] 발생
450. [[450_dma_direct_memory_access|직접 메모리 접근]] ([[746_io_direct_memory_access_dma|DMA]], [[318_dma|Direct Memory Access]]) - CPU 개입 없이 장치와 메모리 간 직접 [[001_dikw_pyramid|데이터]] 전송
451. [[451_cycle_stealing|사이클 스틸링]] ([[451_cycle_stealing|Cycle Stealing]]) - [[746_io_direct_memory_access_dma|DMA]] 컨트롤러가 CPU의 [[344_bus|버스]] 사용을 일시 중지시키고 전송
452. [[746_io_direct_memory_access_dma|DMA]] 산란-수집 ([[452_dma_scatter_gather|Scatter-Gather]]) - 불연속적 물리 메모리 블록을 한 번의 DMA로 전송
453. I/O 서브시스템의 [[022_kernel_role|커널]] [[090_service_kubernetes_network_load_balancing|서비스]] - I/O 스케줄링, [[454_buffering|버퍼링]], [[456_caching|캐싱]], [[457_spooling|스풀링]], 오류 처리
454. [[454_buffering|버퍼링]] ([[454_buffering|Buffering]]) - 송수신자 간 [[001_dikw_pyramid|데이터]] 전송 속도 차이, 전송 단위 차이 극복
455. [[455_double_buffering|이중 버퍼링]] ([[455_double_buffering|Double Buffering]])
456. [[456_caching|캐싱]] ([[456_caching|Caching]]) - 자주 사용하는 [[001_dikw_pyramid|데이터]] 복사본 유지 (속도 빠른 메모리 활용)
457. [[457_spooling|스풀링]] ([[457_spooling|Spooling]], Simultaneous Peripheral [[329_delta_encoding|Operation]] On-Line) - 디스크를 대형 버퍼로 사용 (프린터 큐)
458. 예약 및 단독 장치 접근 제어
459. 블로킹 I/O ([[122_sync_async_communication|Blocking]] I/O) - I/O 완료 시까지 프로세스 대기
460. 논블로킹 I/O (Non-[[122_sync_async_communication|blocking]] I/O) - [[001_dikw_pyramid|데이터]]가 없어도 즉시 반환 (오류/0 [[074_byte|바이트]] 반환)
461. 비동기 I/O (Asynchronous I/O, AIO) - I/O 요청 후 즉시 작업 [[216_progress_in_synchronization|진행]], 완료 시 시그널/콜백 알림
462. I/O 완료 [[446_port_and_bus|포트]] (IOCP, I/O Completion [[446_port_and_bus|Port]]) - Windows 비동기 I/O [[249_scaling_normalization_standardization|스케일링]]
463. epoll / kqueue - 리눅스/BSD 다중 I/O 이벤트 통지 (고성능 [[125_socket|소켓]] 서버)
464. [[464_io_uring|io_uring]] - 최신 리눅스 [[022_kernel_role|커널]] 비동기 I/O 프레임워크 (링 버퍼 기반, 제로 시스템콜 목표)
465. [[465_hdd_structure|하드 디스크 드라이브]] ([[465_hdd_structure|HDD]]) 구조 - 플래터, 트랙, 실린더, 섹터, 헤드
466. [[466_logical_block_address_lba|논리적 블록 주소]] (LBA, Logical Block Address) - 1차원 [[055_array|배열]]로 매핑
467. 디스크 접근 시간 = [[324_seek_time|탐색 시간]]([[467_disk_access_time|Seek Time]]) + [[325_rotational_latency|회전 지연]]([[325_rotational_latency|Rotational Latency]]) + [[326_transfer_time|전송 시간]]([[326_transfer_time|Transfer Time]])
468. [[468_disk_scheduling_purpose|디스크 스케줄링]] ([[468_disk_scheduling_purpose|Disk Scheduling]]) 목적 - [[324_seek_time|탐색 시간]] 최소화, [[139_throughput|처리량]] 극대화
469. [[173_fcfs_scheduling|FCFS]] (First-Come, First-Served) 스케줄링
470. [[470_sstf_disk_scheduling|SSTF]] (Shortest [[467_disk_access_time|Seek Time]] First) - 현재 헤드 위치에서 가장 가까운 요청 처리 (기아 발생 가능)
471. SCAN 스케줄링 ([[471_scan_elevator_scheduling|엘리베이터 알고리즘]]) - 한 방향으로 이동하며 끝까지 처리 후 역방향
472. [[472_c_scan_scheduling|C-SCAN]] ([[472_c_scan_scheduling|Circular SCAN]]) - 한 방향으로만 처리하고 끝에 도달하면 시작점으로 빠르게 복귀 (대기 시간 균등화)
473. LOOK 및 C-LOOK - 양 끝까지 가지 않고 마지막 요청까지만 이동 후 턴 (SCAN/[[472_c_scan_scheduling|C-SCAN]] 최적화)
474. 리눅스 I/O [[079_kube_scheduler_pod_placement|스케줄러]] - NOOP, CFQ([[474_linux_io_schedulers|Completely Fair Queuing]]), [[766_realtime_scheduling_deadline|Deadline]], BFQ
475. [[475_ssd_structure|솔리드 스테이트 드라이브]] ([[327_ssd|SSD]], [[327_ssd|Solid State Drive]]) 구조 - NAND 플래시, [[286_page_frame|페이지]]([[286_page_frame|Page]]), 블록(Block)
476. [[256_flash_memory|플래시 메모리]] 한계 - 덮어쓰기 불가([[476_flash_memory_limitations|Erase-before-write]]), [[289_cqrs_db|쓰기]] 횟수 제한(Wear-out)
477. [[380_garbage_collection|가비지 컬렉션]] ([[380_garbage_collection|Garbage Collection]] in [[327_ssd|SSD]]) - 유효 [[286_page_frame|페이지]] 복사 후 블록 전체 지우기
478. [[478_ftl_flash_translation_layer|FTL]] ([[478_ftl_flash_translation_layer|Flash Translation Layer]]) - LBA를 플래시의 [[323_physical_address|물리 주소]](PBA)로 매핑하는 [[032_firmware|펌웨어]]
479. [[479_wear_leveling|마모 평준화]] ([[479_wear_leveling|Wear Leveling]]) - 수명 연장을 위해 [[289_cqrs_db|쓰기]] 작업을 전체 블록에 고르게 [[136_variance|분산]]
480. [[480_write_amplification|쓰기 증폭]] ([[480_write_amplification|Write Amplification]]) 현상
481. TRIM [[158_instruction|명령어]] - OS가 삭제된 [[501_file_definition_logical_record|파일]]의 LBA를 SSD에 알려주어 GC 효율 향상
482. [[482_nvme|NVMe]] ([[482_nvme|Non-Volatile Memory Express]]) - [[356_pcie|PCIe]] [[344_bus|버스]] 기반 고속 플래시 [[295_protocol_field_tcp_udp_icmp|프로토콜]] (다중/깊은 큐 지원)
483. [[483_raid_overview|RAID]] (Redundant [[055_array|Array]] of Independent Disks) - [[282_performance_tactics|성능]] 향상 및 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]](중복성) 확보
484. [[484_raid_0_striping|RAID 0]] ([[332_raid_0|스트라이핑]], Striping) - 블록 [[136_variance|분산]] 저장, [[282_performance_tactics|성능]] 최고, [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 없음
485. [[485_raid_1_mirroring|RAID 1]] ([[333_raid_1|미러링]], Mirroring) - [[001_dikw_pyramid|데이터]] 중복 복사, [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 최고, 용량 효율 50%
486. [[486_raid_4_dedicated_parity|RAID 4]] (블록 단위 [[332_raid_0|스트라이핑]] + 단일 패리티 디스크) - 병목 발생
487. [[487_raid_5_distributed_parity|RAID 5]] (블록 단위 [[332_raid_0|스트라이핑]] + [[334_raid_5|분산 패리티]]) - [[282_performance_tactics|성능]]/[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 절충, 가장 대중적, 디스크 1개 고장 허용
488. [[488_raid_6_dual_parity|RAID 6]] ([[488_raid_6_dual_parity|분산 이중 패리티]]) - 디스크 2개 고장 허용
489. [[489_raid_10_hybrid|RAID 10]] (1+0) / [[483_raid_overview|RAID]] 01 (0+1) 혼합형 구조
490. 소프트웨어 [[483_raid_overview|RAID]] vs 하드웨어 [[483_raid_overview|RAID]] (컨트롤러 캐시/[[688_bbu|BBU]] 장착)
491. [[491_hot_spare_auto_rebuild|핫 스페어]] ([[491_hot_spare_auto_rebuild|Hot Spare]]) 디스크 자동 재구성
492. [[492_nas_network_attached_storage|NAS]] ([[492_nas_network_attached_storage|Network Attached Storage]]) - [[501_file_definition_logical_record|파일]] 단위 접근 ([[543_nfs_network_file_system|NFS]], SMB/CIFS)
493. [[493_san_storage_area_network|SAN]] ([[493_san_storage_area_network|Storage Area Network]]) - 블록 단위 전용 네트워크 접근 ([[696_fibre_channel_protocol|Fibre Channel]], [[698_iscsi|iSCSI]])
494. [[494_object_storage|오브젝트 스토리지]] ([[494_object_storage|Object Storage]]) - 플랫 [[061_namespace|네임스페이스]], [[477_rest_api_architecture|REST API]] 기반 클라우드 (Amazon S3)
495. [[495_device_driver|장치 드라이버]] ([[495_device_driver|Device Driver]]) [[022_kernel_role|커널]] 인터페이스 구현
496. [[496_interrupt_sharing_msi_msix|인터럽트 공유]] ([[496_interrupt_sharing_msi_msix|Interrupt Sharing]]) 및 [[561_msi|MSI]]/[[561_msi|MSI]]-X ([[561_msi|Message Signaled Interrupts]])
497. [[497_sr_iov_pcie_mapping|SR-IOV]] (Single Root I/O [[190_virtualization_computing_architecture_cloud|Virtualization]]) - 가상 머신에 물리적 [[356_pcie|PCIe]] 장치 직접 매핑
498. [[498_computational_storage|컴퓨테이셔널 스토리지]] ([[498_computational_storage|Computational Storage]] / [[595_smart_ssd|Smart SSD]]) - I/O 노드 연산 [[440_offloading|오프로딩]]
499. [[499_nvme_over_fabrics|NVMe over Fabrics]] ([[499_nvme_over_fabrics|NVMe-oF]]) - [[639_rdma_kernel_bypass|RDMA]] 기반 네트워크 [[327_ssd|SSD]] 고속 연결 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
500. [[500_multipath_io|이중 경로]] ([[500_multipath_io|Multipath]]) I/O 페일오버 및 로드밸런싱 구조

## 9. [[501_file_definition_logical_record|파일]] 시스템 ([[501_file_definition_logical_record|File]] System) 관리 (70개)
501. [[501_file_definition_logical_record|파일]] ([[501_file_definition_logical_record|File]])의 정의 - [[369_logic_bomb|논리]]적 레코드의 연속, OS가 관리하는 정보의 기본 단위
502. [[502_file_attributes_metadata|파일 속성]] ([[502_file_attributes_metadata|Attributes]]) - 이름, [[289_identification_flags_fragmentation_offset|식별자]], 타입, 위치, 크기, [[571_protection_vs_security|보호]](권한), 타임스탬프
503. [[503_magic_number_file_signature|매직 넘버]] ([[503_magic_number_file_signature|Magic Number]]) - [[501_file_definition_logical_record|파일]] 확장자 외 내용 [[289_identification_flags_fragmentation_offset|식별자]]
504. [[501_file_definition_logical_record|파일]] 접근 방법 - 순차 접근 ([[504_file_access_methods_sequential_direct|Sequential Access]]), 직접 접근 ([[176_direct_addressing|Direct]] Access / Random Access)
505. [[505_file_indexed_access_method|색인 접근]] ([[505_file_indexed_access_method|Indexed Access]])
506. [[506_directory_structure_symbol_table|디렉터리]] ([[506_directory_structure_symbol_table|Directory]]) 구조 - 심볼 테이블 (이름 -> 항목 번역)
507. 1단계 [[506_directory_structure_symbol_table|디렉터리]] / 2단계 [[506_directory_structure_symbol_table|디렉터리]] (사용자별 UFD)
508. [[508_tree_structured_directory|트리 구조 디렉터리]] ([[508_tree_structured_directory|Tree-structured Directory]]) - 계층 구조, 현재 [[506_directory_structure_symbol_table|디렉터리]] 개념
509. [[509_absolute_relative_path|절대 경로]] ([[509_absolute_relative_path|Absolute Path]]) / 상대 경로 (Relative Path)
510. [[510_acyclic_graph_directory_link|비순환 그래프 디렉터리]] ([[510_acyclic_graph_directory_link|Acyclic Graph Directory]]) - 링크를 통한 [[506_directory_structure_symbol_table|디렉터리]]/[[501_file_definition_logical_record|파일]] 공유
511. [[511_hard_link|하드 링크]] ([[511_hard_link|Hard Link]]) - 동일한 물리 [[001_dikw_pyramid|데이터]](i-node) 가리킴, [[506_directory_structure_symbol_table|디렉터리]] 링크 불가
512. [[512_symbolic_link|심볼릭 링크]] ([[512_symbolic_link|Symbolic Link]] / Soft Link) - 경로명을 값으로 가짐, 윈도우의 바로가기
513. [[513_general_graph_directory|일반 그래프 디렉터리]] ([[513_general_graph_directory|순환 허용]]) - 무한 루프 탐색 방지 [[001_algorithm_definition|알고리즘]] ([[380_garbage_collection|가비지 컬렉션]] 필요)
514. [[514_partition_slice_volume|파티션]] ([[514_partition_slice_volume|Partition]]) / [[331_neuromorphic_ai_db|슬라이스]] / 볼륨 ([[001_bigdata_3v_5v|Volume]])
515. [[515_mbr_vs_gpt|MBR]] ([[515_mbr_vs_gpt|Master Boot Record]]) vs [[302_gpt_autoregressive|GPT]] (GUID [[514_partition_slice_volume|Partition]] Table)
516. [[516_mount_mechanism|마운트]] ([[516_mount_mechanism|Mount]]) 메커니즘 - 다른 [[501_file_definition_logical_record|파일]] 시스템을 [[506_directory_structure_symbol_table|디렉터리]] 트리의 특정 지점에 연결
517. [[517_virtual_file_system_vfs|VFS]] ([[517_virtual_file_system_vfs|Virtual File System]]) - 다양한 [[501_file_definition_logical_record|파일]] 시스템(ext4, NTFS, [[525_fat_file_allocation_table|FAT]])을 [[198_abstraction_control_data_process|추상화]]하는 공통 인터페이스 객체 모델
518. [[517_virtual_file_system_vfs|VFS]] 객체 - 슈퍼블록 ([[518_vfs_objects_superblock_inode_dentry_file|Superblock]]), 아이노드 (inode), 덴트리 (dentry), [[501_file_definition_logical_record|파일]] 객체 ([[501_file_definition_logical_record|file]] object)
519. [[519_on_disk_structures|디스크 상의 구조]] - 부트 제어 블록, 볼륨 제어 블록(슈퍼블록), [[506_directory_structure_symbol_table|디렉터리]] 구조, FCB(아이노드)
520. 메모리 내의 구조 - [[516_mount_mechanism|마운트]] 테이블, 시스템 전체 [[521_open_file_table|열린 파일 테이블]] (System-wide [[521_open_file_table|Open File Table]]), 프로세스별 [[521_open_file_table|열린 파일 테이블]]
521. [[521_open_file_table|열린 파일 테이블]] ([[521_open_file_table|Open File Table]]) - [[501_file_definition_logical_record|파일]] 포인터, 열림 횟수(Open Count), 접근 권한 기록
522. [[522_file_allocation_methods|파일 할당 방법]] ([[522_file_allocation_methods|File Allocation Methods]])
523. [[523_contiguous_allocation|연속 할당]] ([[523_contiguous_allocation|Contiguous Allocation]]) - 시작 블록과 길이 저장, 속도 빠름, [[342_external_fragmentation|외부 단편화]] 심각
524. [[524_linked_allocation|연결 할당]] ([[524_linked_allocation|Linked Allocation]]) - 블록들이 포인터로 연결됨, [[342_external_fragmentation|외부 단편화]] 없음, 랜덤 접근 불가, 포인터 오버헤드
525. [[525_fat_file_allocation_table|FAT]] ([[525_fat_file_allocation_table|File Allocation Table]]) - MS-[[599_dos_ddos_attack|DOS]] 기반, 포인터들을 별도의 테이블에 모아 [[456_caching|캐싱]]하여 랜덤 접근 문제 완화
526. [[526_indexed_allocation|색인 할당]] ([[526_indexed_allocation|Indexed Allocation]]) - 모든 블록 포인터를 색인 블록([[154_database_index_b_tree_search_optimization|Index]] Block) 하나에 모아 저장
527. 색인 블록 크기 한계 해결 - 연결 색인, 다중 수준 색인 ([[527_index_block_size_limits|Multilevel Index]])
528. [[528_unix_inode_mechanism|유닉스 i-node]] ([[528_unix_inode_mechanism|Index Node]]) 매커니즘 - [[501_file_definition_logical_record|파일]] [[012_metadata|메타데이터]] 및 다중 접근 포인터 보유
529. [[529_inode_direct_blocks|i-node 직접 블록]] ([[529_inode_direct_blocks|Direct Blocks]]) - 보통 12~15개, 작은 [[501_file_definition_logical_record|파일]] 고속 접근
530. i-node 단일/이중/삼중 간접 블록 ([[530_inode_indirect_blocks|Indirect Blocks]]) - 대용량 [[501_file_definition_logical_record|파일]] 확장 지원 체계
531. [[531_extent_allocation|익스텐트]] ([[531_extent_allocation|Extent]]) - 연속된 여러 블록의 묶음 할당 기법 (ext4, XFS 적용 - [[012_metadata|메타데이터]] 감소 효과)
532. [[532_free_space_management|빈 공간 관리]] ([[532_free_space_management|Free-Space Management]]) [[001_algorithm_definition|알고리즘]]
533. [[533_bit_vector_bitmap|비트 벡터]] ([[086_fenwick_tree|Bit]] Vector / Bitmap) - 0과 1로 표현, 1워드 크기 연속 빈 공간 탐색 최적
534. [[056_linked_list|연결 리스트]] ([[056_linked_list|Linked List]]) [[532_free_space_management|빈 공간 관리]]
535. [[535_grouping_counting_free_space|그룹화]] ([[535_grouping_counting_free_space|Grouping]]) / 계수 (Counting) 기법
536. [[536_buffer_cache_page_cache|버퍼 캐시]] ([[536_buffer_cache_page_cache|Buffer Cache]]) / [[286_page_frame|페이지]] 캐시 ([[286_page_frame|Page]] Cache) 통합 아키텍처
537. [[537_read_ahead_delayed_write|미리 읽기]] ([[537_read_ahead_delayed_write|Read-ahead]]) 및 [[015_지연_데이터_관점|지연]] [[289_cqrs_db|쓰기]] (Delayed-write / Write-behind)
538. [[212_synchronization_mechanisms|동기화]] I/O (O_SYNC / fsync)
539. [[539_journaling_file_system|저널링 파일 시스템]] ([[539_journaling_file_system|Journaling File System]]) - 시스템 크래시 시 [[194_consistency_database_integrity|일관성]] [[658_ir_recovery|복구]] (ext3, ext4, NTFS)
540. [[012_metadata|메타데이터]] 저널링 vs [[001_dikw_pyramid|데이터]] 저널링 모드 (순서: [[568_logs_distributed_logging_elk_fluentd|로그]] 기록 -> 커밋 -> 실제 [[501_file_definition_logical_record|파일]]시스템 반영)
541. [[541_log_structured_file_system|LFS]] ([[541_log_structured_file_system|Log-structured File System]]) - 모든 [[289_cqrs_db|쓰기]]를 순차적 [[568_logs_distributed_logging_elk_fluentd|로그]] 형태로만 디스크에 기록 ([[256_flash_memory|플래시 메모리]]에 적합)
542. [[542_cow_file_system|COW]] ([[542_cow_file_system|Copy-On-Write]]) [[501_file_definition_logical_record|파일]] 시스템 (ZFS, Btrfs) - [[022_snapshot_backup_architecture|스냅샷]] 및 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 기능 내장
543. [[543_nfs_network_file_system|NFS]] ([[543_nfs_network_file_system|Network File System]]) - 원격 [[506_directory_structure_symbol_table|디렉터리]] [[516_mount_mechanism|마운트]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] (상태 비저장, [[406_udp_user_datagram_protocol_connectionless_fast|UDP]]/[[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 지원)
544. [[544_afs_smb_cifs_file_system|AFS]] ([[544_afs_smb_cifs_file_system|Andrew File System]]) / SMB/CIFS (Windows [[501_file_definition_logical_record|파일]] 공유)
545. 윈도우 NTFS - MFT ([[545_windows_ntfs_mft|Master File Table]]), 권한 제어([[549_acl_access_control_list|ACL]]), [[501_file_definition_logical_record|파일]] [[347_compaction|압축]] 및 암호화 지원
546. [[546_data_deduplication|데이터 중복 제거]] ([[546_data_deduplication|Data Deduplication]]) [[501_file_definition_logical_record|파일]] 시스템 기능
547. [[501_file_definition_logical_record|파일]] 시스템 접근 제어 ([[547_access_control_rwx|Access Control]]) - 소유자, 그룹, 기타(Other)의 rwx 권한 (r=4, w=2, x=1)
548. [[548_special_permissions_setuid|SetUID]] ([[548_special_permissions_setuid|4000]]), SetGID (2000), Sticky [[086_fenwick_tree|Bit]] (1000) 특수 권한
549. [[549_acl_access_control_list|ACL]] ([[549_acl_access_control_list|Access Control List]]) 확장을 통한 세밀한 사용자별 [[501_file_definition_logical_record|파일]] 권한 통제
550. [[550_extended_attributes_xattr|리눅스 확장 속성]] (Extended [[502_file_attributes_metadata|Attributes]], xattr)
551. [[551_quota_disk_limit|할당량]] ([[551_quota_disk_limit|Quota]]) 시스템 - 유저/그룹 별 디스크 사용량 제한
552. [[064_b_tree|B-Tree]] / B+Tree 기반 [[506_directory_structure_symbol_table|디렉터리]] 색인 (대규모 [[506_directory_structure_symbol_table|디렉터리]] 검색 최적화)
553. [[553_distributed_file_system|분산 파일 시스템]] ([[013_hdfs|HDFS]], Ceph, [[679_glusterfs|GlusterFS]]) [[014_namenode|네임노드]] 및 [[015_datanode|데이터노드]] 구조
554. [[554_fuse_filesystem_in_userspace|FUSE]] ([[554_fuse_filesystem_in_userspace|Filesystem in Userspace]]) - [[022_kernel_role|커널]] 수정 없이 유저 공간에서 커스텀 [[501_file_definition_logical_record|파일]]시스템 구현 (SSHFS 등)
555. [[555_backup_and_restore_strategy|백업]] ([[555_backup_and_restore_strategy|Backup]]) 및 [[658_ir_recovery|복구]] (Restore) / 전체 [[555_backup_and_restore_strategy|백업]] vs 증분(Incremental) [[555_backup_and_restore_strategy|백업]]
556. [[556_undelete_data_carving|삭제된 파일 복구]] ([[556_undelete_data_carving|Undelete]]) 및 포렌식 디스크 이미지 카빙(Carving) 원리
557. [[557_tmpfs_ramfs_memory_filesystem|임시 파일 시스템]] (tmpfs / ramfs) - 메모리 상주 [[501_file_definition_logical_record|파일]] 시스템
558. 가상 장치 [[501_file_definition_logical_record|파일]] 시스템 (sysfs, procfs) - [[022_kernel_role|커널]] 변수와 하드웨어 정보 노출 통로
559. [[501_file_definition_logical_record|파일]] 시스템 [[194_consistency_database_integrity|일관성]] 검사 (fsck / chkdsk)
560. [[560_multi_stream_file_fork_ads|다중 스트림]] ([[560_multi_stream_file_fork_ads|Multi-stream]]) [[501_file_definition_logical_record|파일]] / 포크 (Forks) - [[001_dikw_pyramid|데이터]] 스트림과 리소스 스트림 분리
561. [[561_encrypted_file_system_ecryptfs|암호화 파일 시스템]] (eCryptfs / Windows EFS)
562. [[003_integrity|무결성]] [[395_verification_process_review|검증]] [[501_file_definition_logical_record|파일]] 시스템 (dm-verity / Android 적용 보안 [[501_file_definition_logical_record|파일]] 구조)
563. 플래시 전용 [[501_file_definition_logical_record|파일]] 시스템 (F2FS, JFFS2, YAFFS) 특성 분석
564. [[564_bit_rot_btrfs_self_healing|데이터 파손]] ([[001_dikw_pyramid|Data]] Corruption / [[086_fenwick_tree|Bit]] Rot) 대응 Btrfs 자가 치유(Self-healing) 기능
565. [[176_direct_addressing|Direct]] I/O ([[565_o_direct_io_bypass_cache|O_DIRECT]]) - OS 캐시를 우회하여 [[002_database_definition|데이터베이스]] 등의 자체 [[456_caching|캐싱]] 최적화
566. [[749_memory_mapped_file_mmap|mmap]] 기반 제로 카피 ([[566_mmap_zero_copy_sendfile|Zero-copy]]) 전송 기술 (sendfile) [[282_performance_tactics|성능]] 이점
567. [[567_file_locking_shared_exclusive|파일 잠금]] ([[567_file_locking_shared_exclusive|File Locking]]) - 공유 잠금(Shared [[510_lock|lock]]) vs 배타적 잠금(Exclusive [[510_lock|lock]])
568. [[568_mandatory_advisory_lock|강제적 잠금]] ([[568_mandatory_advisory_lock|Mandatory Lock]]) vs 권고적 잠금 (Advisory [[510_lock|Lock]])
569. [[569_sparse_file_holes|스파스 파일]] ([[569_sparse_file_holes|Sparse File]]) 저장 공간 절약 기술
570. [[570_inotify_file_monitoring|리눅스 inotify 시스템]] - [[501_file_definition_logical_record|파일]]/[[506_directory_structure_symbol_table|디렉터리]] 변경 이벤트 [[229_monitor|모니터]]링 [[014_api_posix|API]]

## [[489_raid_10_hybrid|10]]. 시스템 보안, [[571_protection_vs_security|보호]], 그리고 [[282_performance_tactics|성능]]/[[015_virtualization|가상화]] 심화 (100개)
571. [[571_protection_vs_security|보호]] ([[571_protection_vs_security|Protection]]) vs 보안 ([[283_security_tactics|Security]])의 개념 차이
572. [[572_protection_domain|보호 도메인]] ([[572_protection_domain|Protection Domain]]) - 프로세스가 접근할 수 있는 자원(객체)과 권한(Access Right)의 집합
573. [[573_access_matrix|접근 제어 행렬]] ([[573_access_matrix|Access Matrix]]) - 주체(행)와 객체(열) 교차점의 권한 표현 모형
574. [[574_global_table|전역 테이블]] ([[574_global_table|Global Table]]) 방식 구현 (행렬 희소성 문제)
575. [[739_access_control_list_acl|접근 제어 목록]] ([[549_acl_access_control_list|ACL]], [[549_acl_access_control_list|Access Control List]]) - 객체 중심 (해당 객체에 접근 가능한 주체 목록)
576. [[576_capability_list|자격 증명 리스트]] ([[576_capability_list|Capability List]] / Ticket) - 주체 중심 (주체가 가진 권한 리스트 토큰 방식)
577. 롤 기반 접근 제어 ([[569_rbac|RBAC]], [[569_rbac|Role-Based Access Control]]) - 사용자 대신 역할(Role)에 권한 할당
578. [[578_dac_discretionary_access_control|임의적 접근 제어]] (DAC, Discretionary [[547_access_control_rwx|Access Control]]) - 소유자가 임의로 권한 위임
579. [[579_mac_mandatory_access_control|강제적 접근 제어]] ([[673_mac_message_authentication_code|MAC]], Mandatory [[547_access_control_rwx|Access Control]]) - 시스템/보안 관리자가 등급 라벨 기반 강제 통제
580. [[580_bell_lapadula_model|벨-라파둘라 모델]] ([[580_bell_lapadula_model|Bell-LaPadula]]) - [[002_confidentiality|기밀성]] 위주 [[007_security_policy|보안 정책]] (No Read Up, No Write Down)
581. [[581_biba_model|비바 모델]] ([[581_biba_model|Biba Model]]) - [[003_integrity|무결성]] 위주 [[164_policy|정책]] (No Read Down, No Write Up)
582. [[582_linux_security_modules_lsm|리눅스 보안 모듈]] (LSM, Linux [[283_security_tactics|Security]] Modules) - 플러그인 훅 구조
583. [[583_selinux|SELinux]] - 레이블 기반 [[673_mac_message_authentication_code|MAC]] 구현체, 보안 [[033_context|컨텍스트]]
584. [[584_apparmor|AppArmor]] - 경로 기반 [[673_mac_message_authentication_code|MAC]] 구현 [[192_module_independence|모듈]]
585. 시스템 보안 위협 유형 - [[002_confidentiality|기밀성]], [[003_integrity|무결성]], [[452_availability|가용성]], [[303_authentication_authorization_patterns|인증]] 침해
586. [[586_trojan_horse_wrapper|트로이 목마]] ([[586_trojan_horse_wrapper|Trojan Horse]]) / 래퍼 (Wrapper)
587. [[587_backdoor_trapdoor|트랩 도어]] ([[677_trap_based_system_call_implementation|Trap]] Door / [[727_backdoor|Backdoor]])
588. [[588_logic_bomb|로직 밤]] ([[588_logic_bomb|Logic Bomb]]) / 타이머 밤
589. [[589_virus|바이러스]] ([[589_virus|Virus]]) - 호스트 프로그램 기생
590. 웜 ([[590_worm|Worm]]) - 자가 [[016_replication_factor|복제]] 네트워크 전파 독자 실행
591. [[591_buffer_overflow|버퍼 오버플로우]] ([[591_buffer_overflow|Buffer Overflow]]) 원리 - C언어 취약 함수 악용 리턴 주소 덮어쓰기
592. [[592_shellcode_injection|셸코드]] ([[592_shellcode_injection|Shellcode]]) [[480_injection|인젝션]]
593. [[591_buffer_overflow|버퍼 오버플로우]] 방어 하드웨어 기술 ([[335_nx_bit|NX Bit]] / [[336_dep|Data Execution Prevention]], [[336_dep|DEP]])
594. [[382_virtual_address_space|가상 주소 공간]] 구조 무작위화 ([[374_aslr|ASLR]]) - 버퍼/[[057_stack|스택]] [[336_library_vs_framework|라이브러리]] 주소 랜덤 배치 방어망
595. [[595_canary_stack_smashing_protector|카나리]] ([[595_canary_stack_smashing_protector|Canary]]) / [[057_stack|스택]] 스매싱 가드 ([[541_stack_smashing_protector|Stack Smashing Protector]]) - 컴파일러 수준 버퍼 변조 탐지
596. [[596_return_oriented_programming|ROP]] ([[596_return_oriented_programming|Return-Oriented Programming]]) 기법 - [[374_aslr|ASLR]]/[[336_dep|DEP]] 우회를 위해 코드 [[345_gadget_rop|가젯]] 체이닝
597. [[597_zero_day_exploit|제로 데이]] ([[597_zero_day_exploit|Zero-Day]]) 취약점 / 익스플로잇 (Exploit)
598. [[598_spoofing|스푸핑]] ([[598_spoofing|Spoofing]]) - IP/[[673_mac_message_authentication_code|MAC]] 등 신분 위장
599. [[599_dos_ddos_attack|서비스 거부]] ([[599_dos_ddos_attack|DoS]]) 및 [[136_variance|분산]] [[599_dos_ddos_attack|서비스 거부]] (DDoS) 네트워크 자원 고갈 공격
600. [[600_port_scanning|포트 스캐닝]] ([[600_port_scanning|Port Scanning]]) 도구 원리
601. [[601_ids_ips_syscall_tracing|침입 탐지 시스템]] ([[601_ids_ips_syscall_tracing|IDS]]) / 침입 방지 시스템 ([[695_ips_network_intrusion_prevention_system|IPS]]) 시스템 콜 트레이싱 기반 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]
602. [[602_sandboxing_kernel_wrapper|샌드박싱]] ([[602_sandboxing_kernel_wrapper|Sandboxing]]) 기술 [[022_kernel_role|커널]] 래퍼
603. [[603_rootkit_syscall_hooking|루트킷]] ([[603_rootkit_syscall_hooking|Rootkit]]) [[022_kernel_role|커널]] [[192_module_independence|모듈]] 감염 방식 (시스템 콜 테이블 후킹)
604. [[604_authentication_factors|사용자 인증]] ([[604_authentication_factors|Authentication]]) 요소 - Something you know, have, are
605. [[605_password_salting_hash|비밀번호 솔팅]] ([[605_password_salting_hash|Salting]]) 기반 해시 처리 방어 구조
606. [[606_auditing_linux_auditd|감사]] ([[606_auditing_linux_auditd|Auditing]]) 로깅 프레임워크 (Linux Auditd)
607. 물리적 보안 및 [[475_hsm|하드웨어 보안 모듈]] ([[476_tpm|TPM]], [[476_tpm|Trusted Platform Module]])
608. [[608_secure_boot|보안 부팅]] ([[608_secure_boot|Secure Boot]]) [[303_authentication_authorization_patterns|인증]]서 체인 로딩 [[395_verification_process_review|검증]]
609. [[609_performance_monitoring|성능 모니터링]] ([[609_performance_monitoring|Performance Monitoring]]) 및 튜닝 방법론
610. 리틀의 법칙 (Little's Law) - L = λW ([[089_wait_queue|대기 큐]] [[282_performance_tactics|성능]] 분석)
611. CPU 유휴 ([[611_cpu_idle_wait_optimization|Idle]]) 대기 루프 최적화
612. [[612_memory_leak_detection|메모리 누수]] ([[612_memory_leak_detection|Memory Leak]]) 탐지 도구 구조 (Valgrind 등)
613. [[613_profiling_gprof|프로파일링]] ([[613_profiling_gprof|Profiling]]) 도구 Gprof [[022_kernel_role|커널]] 후킹 작동 원리
614. 시스템 [[614_dtrace|DTrace]] 선언적 동적 트레이싱 엔진 메커니즘
615. [[615_ebpf|eBPF]] 네트워크/보안/[[229_monitor|모니터]]링 이벤트 [[022_kernel_role|커널]] 안전 훅 매커니즘
616. 멀티코어 확장성 병목 (Amdahl's Law) 및 [[022_kernel_role|커널]] [[275_lock_contention_monitoring|락 경합]] 진단
617. I/O [[282_performance_tactics|성능]] 병목 ([[617_io_bottleneck|Bottleneck]]) 탐색법 (iostat, vmstat)
618. 캐시 미스 오버헤드 측정 분석망 구조 적용
619. 모바일 OS 특징 (Android vs iOS 아키텍처 비교)
620. 안드로이드 리눅스 [[022_kernel_role|커널]] 커스터마이징 (Wakelock 전력 통제 [[192_module_independence|모듈]])
621. [[621_art_android_runtime|ART]] ([[621_art_android_runtime|Android Runtime]]) AOT/[[568_jit_access|JIT]] 컴파일러 혼합 실행 환경
622. iOS XNU [[025_hybrid_kernel|하이브리드 커널]] 및 샌드박스 앱 관리 모형
623. 임베디드 실시간 OS (RTOS: VxWorks, FreeRTOS 등) 우선순위 데드라인 절대 보장 아키텍처
624. [[024_microkernel|마이크로커널]] [[117_ipc|IPC]] 메시지 패싱 [[015_지연_데이터_관점|지연]] 단축 기법 구조 설계
625. [[625_hypervisor_ring_level_vmx|하이퍼바이저 링 레벨]] (Ring -1 모드 VMX Root/Non-Root 모드)
626. [[626_shadow_page_table_vs_ept|쉐도우 페이지 테이블]] ([[626_shadow_page_table_vs_ept|Shadow Page Table]]) vs [[661_extended_page_table|확장 페이지 테이블]] (EPT/NPT [[527_hardware_assisted_virtualization|하드웨어 보조]])
627. [[627_iommu_dma_isolation|IOMMU]] (Input/Output [[328_mmu|MMU]]) 역할 - 가상머신 [[746_io_direct_memory_access_dma|DMA]] 장치 할당 및 [[571_protection_vs_security|보호]] 격리
628. [[628_container_runtime_oci|컨테이너 런타임]] ([[667_container_runtime_hw_isolation|runc]], containerd) [[333_process|OCI]] 규격 표준화
629. [[629_live_migration_pre_copy|라이브 마이그레이션]] ([[629_live_migration_pre_copy|Live Migration]]) 메모리 더티 [[286_page_frame|페이지]] 프리-카피(Pre-copy) [[001_algorithm_definition|알고리즘]] 방식
630. [[630_vswitch_vnf_overhead|가상 스위치]] ([[630_vswitch_vnf_overhead|vSwitch]]) 패킷 오버헤드 [[866_vnf_virtual_network_function_software_appliance|VNF]] 구조 적용 방식
631. 메모리 KSM ([[631_ksm_kernel_samepage_merging|Kernel Samepage Merging]]) 가상머신 간 중복 메모리 통합 절약
632. [[632_memory_ballooning_hypervisor|벌루닝]] ([[632_memory_ballooning_hypervisor|Ballooning]]) [[054_hypervisor|하이퍼바이저]] 가상머신 동적 메모리 회수 기법 구조
633. [[633_live_patching_ksplice|무정전 업데이트]] (Ksplice 등 [[022_kernel_role|커널]] 재부팅 없는 패치망 체계 구조)
634. 병행 프로그래밍 락 프리 [[057_stack|스택]]/큐 설계 [[001_dikw_pyramid|데이터]] 구조 메커니즘
635. [[014_concurrency|동시성]] 디버깅 [[213_race_condition|경쟁 조건]] 재현 기법 퍼저/[[092_thread_lwp|스레드]] 새니타이저 ([[635_concurrency_debugging_tsan|ThreadSanitizer]])
636. 다중 경로 I/O ([[500_multipath_io|Multipath]] I/O) [[022_kernel_role|커널]] [[192_module_independence|모듈]] 아키텍처
637. ZFS [[016_replication_factor|복제]] 및 [[022_snapshot_backup_architecture|스냅샷]] ([[637_zfs_snapshot_cow_architecture|Snapshot]]) 카피온라이트 구현 구조 설계 모형
638. Btrfs 서브볼륨 및 [[347_compaction|압축]]/암호화 통합 [[022_kernel_role|커널]] [[501_file_definition_logical_record|파일]] 시스템 동향
639. [[639_rdma_kernel_bypass|RDMA]] (Remote [[318_dma|Direct Memory Access]]) [[022_kernel_role|커널]] 바이패스 [[148_5g_embb_urllc_mmtc|초고속]] 통신 체제
640. [[640_unikernel_mirageos_architecture|유니커널]] ([[640_unikernel_mirageos_architecture|Unikernel]]) [[022_kernel_role|커널]] 분할 오버헤드 극소화 구조체 망 보안 융합 (MirageOS)
641. [[136_variance|분산]] OS 투명성 (Transparency: 위치, 마이그레이션, [[016_replication_factor|복제]], 병행 투명성 보장 구조)
642. 람포트 [[369_logic_bomb|논리]]적 시계 (Lamport's Logical Clocks) [[136_variance|분산]] 환경 [[212_synchronization_mechanisms|동기화]] 정렬
643. [[136_variance|분산]] 락 매니저 구현 (Chubby, [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 등 [[136_variance|분산]] 코디네이션 락 [[001_algorithm_definition|알고리즘]])
644. [[532_microservices_decomposition_patterns|마이크로서비스]] [[022_kernel_role|커널]] 자원 제약 ([[198_pod_kubernetes_minimum_deployment_unit|Pod]] / [[194_container_virtualization_docker_namespace|Container]] 자원 오버커밋 킬링 [[164_policy|정책]])
645. [[022_kernel_role|커널]] 동적 [[192_module_independence|모듈]] 서명 ([[645_kernel_module_signature_verification|Module Signature Verification]]) [[003_integrity|무결성]] 통제
646. 리눅스 시스템 콜 테이블 ([[646_syscall_table_hooking_expansion|sys_call_table]]) 확장 및 보안 훅 추가
647. [[377_numa_allocation|NUMA]] 인지형 메모리 할당기 [[022_kernel_role|커널]] [[286_page_frame|페이지]] 이동 [[164_policy|정책]] 프레임워크 설계
648. 프로세스 체크포인트/리스토어 ([[648_process_checkpoint_restore_criu|CRIU]]) [[561_container_based_deployment|컨테이너]] 마이그레이션 도구 구조
649. [[649_kernel_memory_compaction|커널 메모리 컴팩션]] ([[347_compaction|Compaction]]) [[342_external_fragmentation|외부 단편화]] 런타임 제거 백그라운드 [[092_thread_lwp|스레드]] 구조
650. 고가용성 클러스터 [[001_operating_system_purpose|운영체제]] 하트비트/펜싱 (Fencing / STONITH) 뇌 분할(Split-Brain) 방어 메커니즘
651. [[651_power_aware_scheduler_dvfs|전력 인식]]([[651_power_aware_scheduler_dvfs|Power-aware]]) [[079_kube_scheduler_pod_placement|스케줄러]] 동적 [[001_voltage|전압]]/주파수 [[249_scaling_normalization_standardization|스케일링]]([[469_dvfs|DVFS]]) 통합형 CPU 제어
652. 모바일 OS [[425_oom_killer_score|Out-Of-Memory]] ([[787_android_lmk_low_memory_killer|Low Memory Killer]]) 스코어 계산 [[001_algorithm_definition|알고리즘]] 및 앱 수명 주기 관리
653. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] OS (초경량/고속 부팅 최적화된 리눅스 환경 구성 기술망)
654. [[654_preempt_rt_linux_spinlock_mutex|리얼타임 리눅스]] ([[654_preempt_rt_linux_spinlock_mutex|PREEMPT_RT]]) [[022_kernel_role|커널]] [[222_spinlock|스핀락]]을 뮤텍스로 변환하는 선점 허용 구조 개요
655. CPU [[402_cache_coherence|캐시 일관성]] [[164_policy|정책]] (MESI [[295_protocol_field_tcp_udp_icmp|프로토콜]]) 이 [[022_kernel_role|커널]] 락([[510_lock|Lock]])에 미치는 캐시라인 핑퐁(Ping-pong) 문제
656. [[269_htm_intel_tsx|하드웨어 트랜잭셔널 메모리]] 활용 [[256_lock_free_data_structures|Lock-Free]] 자료구조 시스템 구현 사례
657. [[015_virtualization|가상화]] I/O 패스스루 ([[657_vfio_virtual_function_io_passthrough|Passthrough]]) VFIO 프레임워크
658. Virtio - [[058_paravirtualization|반가상화]] I/O 백엔드/프론트엔드 링버퍼([[658_virtio_paravirtualization_vring|Vring]]) 디바이스 드라이버 구조
659. 클라우드 게스트 OS (Cloud-init 기반 부트스트랩 인스턴스 자동 초기화 스크립트)
660. [[660_kernel_crash_dump_kdump_architecture|커널 덤프]] ([[660_kernel_crash_dump_kdump_architecture|Kdump]]) 시스템 크래시 원인 분석 [[022_kernel_role|커널]] 구조
661. [[615_ebpf|eBPF]] 기반 [[670_xdp|XDP]] ([[661_ebpf_xdp_express_data_path|eXpress Data Path]]) [[022_kernel_role|커널]] 네트워크 [[057_stack|스택]] 우회 [[148_5g_embb_urllc_mmtc|초고속]] 패킷 드롭/전달 프레임워크
662. [[135_android_binder|안드로이드 바인더]]([[662_android_binder_ipc_thread_pool|Binder]]) [[117_ipc|IPC]] [[103_thread_pool|스레드 풀]] 및 객체 [[316_reference_pattern_nosql|참조]] 매핑 메커니즘
663. macOS/iOS Grand Central Dispatch ([[663_macos_ios_gcd_grand_central_dispatch|GCD]]) 블록 및 디스패치 큐 기반 [[014_concurrency|동시성]] 구조
664. Windows [[022_kernel_role|커널]] 비동기 프로시저 호출 ([[664_windows_kernel_apc_dpc_irql|APC]]) 및 [[015_지연_데이터_관점|지연]]된 프로시저 호출 (DPC)
665. [[665_windows_registry_configuration_manager|시스템 레지스트리]] ([[665_windows_registry_configuration_manager|Windows Registry]]) 및 구성 [[002_database_definition|데이터베이스]] 관리 구조
666. [[666_secure_enclave_trustzone_sgx_tee|보안 엔클레이브]] (TrustZone, [[389_sgx|SGX]])와 OS [[478_tee|TEE]] ([[972_tee_based_ml|Trusted Execution Environment]]) 연동 구조
667. [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 철학 하의 [[001_operating_system_purpose|운영체제]] 레벨 런타임 [[003_integrity|무결성]] [[395_verification_process_review|검증]]망 설계
668. [[668_side_channel_attack_meltdown_spectre_kpti|부채널 공격]] ([[481_side_channel_attack|Side-channel Attack]], [[482_meltdown|Meltdown]]/[[483_spectre|Spectre]]) [[204_microarchitecture|마이크로아키텍처]] 취약점 대응 소프트웨어 패치([[578_kpti|KPTI]], [[580_retpoline|Retpoline]])
669. 하드웨어 기반 무작위 [[486_trng|난수 생성기]] ([[669_hardware_trng_kernel_entropy_pool|TRNG]]) [[022_kernel_role|커널]] [[151_entropy|엔트로피]] 풀 주입 방식
670. [[670_fault_injection_chaos_testing_kernel|소프트웨어 오류 주입]] ([[670_fault_injection_chaos_testing_kernel|Fault Injection]]) 카오스 테스팅 시스템 [[022_kernel_role|커널]] [[192_module_independence|모듈]] 활용법

## [[308_static_dynamic_nat_pat_port_address_translation|11]]. 시험 빈출 / 핵심 요약 노트 및 추가 토픽 (130개)
671. 시스템 프로그램과 응용 프로그램의 차이
672. [[672_batch_processing_system_metrics|일괄 처리 시스템]] ([[672_batch_processing_system_metrics|Batch Processing System]]) [[282_performance_tactics|성능]] 지표
673. [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]] ([[673_multiprogramming_bottleneck_resource|Multiprogramming]]) 한계 자원
674. [[003_time_sharing_system|시분할 시스템]] [[138_response_time|응답 시간]] 최적화
675. [[675_multitasking_terminology_preemptive|멀티태스킹]] ([[675_multitasking_terminology_preemptive|Multitasking]]) 용어
676. [[019_interrupt_vector|인터럽트 벡터]] 테이블 구조화
677. [[677_trap_based_system_call_implementation|트랩]] ([[677_trap_based_system_call_implementation|Trap]]) 기반 시스템 콜 구현
678. [[022_kernel_role|커널]] 모드 진입 메커니즘 
679. 시스템 콜 [[014_api_posix|API]] 래퍼
680. 모놀리식 vs [[598_microkernel_plugin_architecture|마이크로 커널]] [[282_performance_tactics|성능]] 비교
681. [[117_ipc|IPC]] 기법 [[282_performance_tactics|성능]] 오버헤드 
682. 프로세스 주소 공간 분리 
683. PCB 구성 요소 필수 암기
684. [[211_context_switch|문맥 교환]] [[357_tlb|TLB]] 플러시 
685. [[685_short_term_scheduler_dispatcher|단기 스케줄러 디스패치]] 
686. CPU 바운드 vs I/O 바운드
687. 선점 / [[285_no_preemption|비선점]] 스케줄링 차이
688. [[173_fcfs_scheduling|FCFS]] [[174_convoy_effect|호위 효과]] ([[174_convoy_effect|Convoy Effect]])
689. [[175_sjf_scheduling|SJF]] 기아 ([[314_starvation_prevention|Starvation]]) 발생
690. [[178_round_robin_scheduling|라운드 로빈]] [[179_time_quantum_context_switch|시간 할당량]] ([[690_round_robin_time_quantum|Quantum]])
691. [[691_mlfq_multi_level_feedback_queue|다단계 피드백 큐]] ([[691_mlfq_multi_level_feedback_queue|MLFQ]]) 천이
692. [[187_hrn_scheduling|HRN]] 대기 시간 공식
693. [[693_multithread_user_mode_kernel_mode|멀티스레드 유저모드 커널모드]] 
694. [[694_thread_local_storage_tls|스레드 로컬 스토리지]] ([[694_thread_local_storage_tls|TLS]]) 
695. [[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]] [[283_mutual_exclusion|상호 배제]]
696. [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]]) 
697. [[214_critical_section|임계 구역]] 3가지 요구조건 
698. Test-and-Set 연산 하드웨어 
699. [[699_mutex_lock_sleep_wait|뮤텍스 락]] ([[699_mutex_lock_sleep_wait|Mutex Lock]]) 
700. [[700_spinlock_busy_waiting|스핀락 바쁜 대기]] ([[700_spinlock_busy_waiting|Busy Wait]]) 
701. [[224_semaphore|세마포어]] P, V 연산 
702. [[229_monitor|모니터]] ([[229_monitor|Monitor]]) [[212_synchronization_mechanisms|동기화]] [[198_abstraction_control_data_process|추상화]] 
703. 생산자 소비자 유한 버퍼
704. 식사하는 철학자 교착 문제 
705. [[281_deadlock_definition|교착 상태]] 4가지 조건 
706. [[287_resource_allocation_graph|자원 할당 그래프]] 사이클 
707. 은행원 [[001_algorithm_definition|알고리즘]] [[298_safe_state|안전 상태]] 
708. [[708_deadlock_ignorance_ostrich_algorithm|교착 상태 무시]] ([[291_ostrich_algorithm|타조 알고리즘]]) 
709. [[307_recovery_from_deadlock|교착 상태 복구]] ([[709_deadlock_recovery_process_kill|프로세스 킬]]) 
710. [[324_address_binding_stages|주소 바인딩]] 컴파일/로드/실행 
711. [[322_logical_virtual_address|논리 주소]] [[323_physical_address|물리 주소]] 변환 [[328_mmu|MMU]]
712. [[342_external_fragmentation|외부 단편화]] 가변 분할 
713. [[341_internal_fragmentation|내부 단편화]] 고정/[[259_paging|페이징]] 
714. 동적 할당 First/Best/[[346_worst_fit|Worst Fit]] 
715. [[259_paging|페이징]] 시스템 프레임 테이블 
716. [[357_tlb|TLB]] [[264_hit_ratio|적중률]] 캐시 속도 
717. [[289_multilevel_page_table|다단계 페이지 테이블]] 사이즈 줄이기 
718. [[364_segmentation|세그멘테이션]] [[342_external_fragmentation|외부 단편화]] 재발 
719. [[255_demand_paging|요구 페이징]] ([[255_demand_paging|Demand Paging]]) 
720. [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]]) [[020_isr|ISR]] 
721. 유효/무효 [[073_bit|비트]] (Valid/Invalid) 
722. [[260_page_replacement|페이지 교체]] [[262_lru_page_replacement|LRU]] 원리 
723. [[261_fifo_page_replacement|FIFO]] 벨라디의 모순 
724. [[724_optimal_page_replacement_unrealizable|최적 알고리즘]] ([[724_optimal_page_replacement_unrealizable|OPT]]) 구현 불가 
725. [[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]]) CPU 이용률 저하 
726. [[265_working_set|워킹 셋]] ([[265_working_set|Working Set]]) 메모리 
727. [[468_disk_scheduling_purpose|디스크 스케줄링]] SCAN 엘리베이터 
728. [[472_c_scan_scheduling|C-SCAN]] [[008_단방향_반이중_전이중|단방향]] 회전
729. [[470_sstf_disk_scheduling|SSTF]] 기아 현상 ([[729_sstf_starvation_middle_bias|가운데 편중]]) 
730. [[484_raid_0_striping|RAID 0]], 1, 5, 6 [[282_performance_tactics|성능]] [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 
731. [[731_ssd_ftl_flash_translation_layer|SSD FTL]] ([[478_ftl_flash_translation_layer|Flash Translation Layer]]) 
732. [[380_garbage_collection|가비지 컬렉션]] 블록 지우기 
733. [[501_file_definition_logical_record|파일]] 시스템 연속, 연결, [[526_indexed_allocation|색인 할당]] 
734. [[525_fat_file_allocation_table|FAT]] 방식 [[524_linked_allocation|연결 할당]] 최적화 
735. i-node 직접/간접 포인터 [[154_database_index_b_tree_search_optimization|인덱스]] 
736. [[511_hard_link|하드 링크]] / [[512_symbolic_link|심볼릭 링크]] 차이 
737. [[517_virtual_file_system_vfs|VFS]] 가상 [[501_file_definition_logical_record|파일]] 시스템 
738. [[536_buffer_cache_page_cache|버퍼 캐시]] [[501_file_definition_logical_record|파일]] 입출력 [[015_지연_데이터_관점|지연]] 
739. [[739_access_control_list_acl|접근 제어 목록]] ([[549_acl_access_control_list|ACL]]) 
740. [[572_protection_domain|보호 도메인]] [[010_least_privilege|최소 권한 원칙]] 
741. [[731_buffer_overflow_stack_heap_aslr|버퍼 오버플로우 공격]] [[057_stack|스택]] 
742. [[598_spoofing|스푸핑]], [[737_backdoor_c2_beacon_behavior_analysis|백도어]] 악성코드 
743. [[743_virtualization_hypervisor|가상화 하이퍼바이저]] 
744. [[744_container_namespace_isolation|컨테이너 네임스페이스 격리]] 
745. 시스템 클럭 타이머 틱 
746. I/O [[450_dma_direct_memory_access|직접 메모리 접근]] ([[746_io_direct_memory_access_dma|DMA]])
747. I/O [[285_pooling_layer|풀링]] ([[747_io_polling_overhead|Polling]]) 오버헤드 
748. [[457_spooling|스풀링]] ([[457_spooling|Spooling]]) 버퍼
749. [[418_memory_mapped_file_mmap|메모리 매핑 파일]] ([[749_memory_mapped_file_mmap|mmap]])
750. [[393_copy_on_write|쓰기 시 복사]] ([[542_cow_file_system|COW]]) 
751. [[195_real_time_scheduling|SMP]] [[402_cache_coherence|캐시 일관성]] 폴스 셰어링 
752. [[752_interrupt_driven_io|인터럽트 구동 입출력]] 
753. [[205_priority_inversion|우선순위 역전]] ([[205_priority_inversion|Priority Inversion]]) 방지 
754. [[754_context_switch_cost|문맥 교환 비용]] ([[754_context_switch_cost|레지스터 저장 복원]]) 
755. 고아 [[109_zombie_process|좀비 프로세스]] init 처리 
756. 시스템 콜 오버헤드 이유
757. [[757_delayed_write_write_behind|파일 지연 쓰기]] ([[757_delayed_write_write_behind|Delayed Write]])
758. [[539_journaling_file_system|저널링 파일 시스템]] [[191_transaction_concept_states|트랜잭션]] [[568_logs_distributed_logging_elk_fluentd|로그]]
759. 블로킹 / 논블로킹 / 비동기 I/O
760. [[760_slab_allocator_object_caching|슬랩]] ([[760_slab_allocator_object_caching|Slab]]) 할당기 객체 [[456_caching|캐싱]] 
761. 디바이스 드라이버 [[192_module_independence|모듈]] 인터페이스 
762. [[016_interrupt_mechanism|인터럽트]] 처리 상프/하프 메커니즘
763. [[603_rootkit_syscall_hooking|루트킷]] 탐지 [[003_integrity|무결성]] 스캔
764. [[374_aslr|ASLR]] 메모리 레이아웃 난수화 
765. [[583_selinux|SELinux]] 보안 강제 [[387_access_control_pattern|접근 통제]] 
766. 실시간 스케줄링 마감 시간 ([[766_realtime_scheduling_deadline|Deadline]]) 
767. [[222_spinlock|스핀락]] 멀티 프로세서 전용 활용 
768. [[768_cas_compare_and_swap_lock_free|CAS]] ([[768_cas_compare_and_swap_lock_free|Compare And Swap]]) [[158_instruction|명령어]] 기초 
769. 데드락 희생자 [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[658_ir_recovery|복구]]망
770. [[363_inverted_page_table|역 페이지 테이블]] 전역 해시 매핑 
771. [[256_flash_memory|플래시 메모리]] [[479_wear_leveling|마모 평준화]] ([[479_wear_leveling|Wear Leveling]])
772. 다중 큐 [[327_ssd|SSD]] [[482_nvme|NVMe]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 장점
773. [[494_object_storage|오브젝트 스토리지]] [[012_metadata|메타데이터]] 분리
774. [[774_nfs_stateless_network_file_system|네트워크 파일 시스템]] ([[543_nfs_network_file_system|NFS]]) 무상태 ([[239_stateless_redis|Stateless]])
775. [[514_partition_slice_volume|파티션]] [[515_mbr_vs_gpt|MBR]] [[302_gpt_autoregressive|GPT]] 크기 제한
776. [[052_cloud_computing_os|클라우드 컴퓨팅]] OS [[638_resource_pooling_cxl|자원 풀링]] 
777. [[157_oom_killer|OOM]] 킬러 [[307_memory_protection|메모리 보호]] [[164_policy|정책]] 
778. [[778_process_affinity_scheduling_pinning|프로세스 친화성]] ([[778_process_affinity_scheduling_pinning|Affinity]]) 스케줄링 
779. [[196_hard_soft_real_time|부하 균등화]] ([[196_hard_soft_real_time|Load Balancing]]) 큐 이주
780. [[615_ebpf|eBPF]] 동적 [[022_kernel_role|커널]] 트레이싱 프레임워크 [[282_performance_tactics|성능]] 
781. ZFS [[542_cow_file_system|Copy-on-Write]] 볼륨 관리 통합 
782. [[541_log_structured_file_system|LFS]] ([[541_log_structured_file_system|Log-structured File System]]) 랜덤 [[289_cqrs_db|쓰기]] 순차화
783. 모바일 환경 에너지 인지 [[079_kube_scheduler_pod_placement|스케줄러]] 
784. [[199_interrupt_scheduling|하이퍼스레딩]] 물리 코어 [[369_logic_bomb|논리]] 코어 분할 구조 
785. [[149_clone_system_call|클론]]([[149_clone_system_call|clone]]) 시스템 콜 [[092_thread_lwp|스레드]] 공유 [[186_character_stuffing_dle_stx_etx|플래그]]
786. [[062_cgroups|cgroups]] 메모리, CPU 자원 제한 격리 [[561_container_based_deployment|컨테이너]]
787. 안드로이드 LMK ([[787_android_lmk_low_memory_killer|Low Memory Killer]]) 작동 
788. iOS 앱 [[602_sandboxing_kernel_wrapper|샌드박싱]] 구조 
789. [[789_live_patching_kpatch_no_downtime|라이브 패칭]] ([[789_live_patching_kpatch_no_downtime|Kpatch]]) [[022_kernel_role|커널]] 정지 없는 보안
790. POSIX [[092_thread_lwp|스레드]] ([[790_posix_threads_pthreads_standard_api|pthreads]]) 표준 [[014_api_posix|API]] 
791. [[270_lock_elision|락 엘리전]] 하드웨어 [[191_transaction_concept_states|트랜잭션]] 메모리 활용 
792. [[254_rcu_read_copy_update|RCU]] 다중 독자 락 프리 고성능 기법 
793. [[265_working_set|워킹 셋]] 윈도우 사이즈 동적 조절 
794. [[286_page_frame|페이지]] 컬러링 캐시 경합 회피 물리 할당
795. [[795_tickless_kernel_mobile_battery_preservation|틱리스 커널]]([[795_tickless_kernel_mobile_battery_preservation|Tickless]]) 모바일 배터리 보존
796. [[377_numa_allocation|NUMA]] 로컬 메모리 원격 메모리 [[015_지연_데이터_관점|지연]]차 
797. [[640_unikernel_mirageos_architecture|유니커널]] 보안과 가벼운 부팅 특성 망 적용
798. [[798_distributed_lock_zookeeper_consensus|분산 락 주키퍼]]([[798_distributed_lock_zookeeper_consensus|ZooKeeper]]) 합의 [[212_synchronization_mechanisms|동기화]] 
799. 람포트 타임스탬프 인과 [[083_relationship_in_er_model|관계]] 정렬
800. 시스템 아키텍처 [[296_fault_tolerance_architecture|결함 허용]] ([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]) 듀얼 구성

---
**총합 요약 : 총 800개 핵심 키워드 수록**
(기본 OS 프로세스/메모리/[[501_file_definition_logical_record|파일]]시스템 뿐만 아니라 최신 리눅스 [[022_kernel_role|커널]], [[015_virtualization|가상화]]/[[561_container_based_deployment|컨테이너]] 인프라 기술, 락프리 [[001_algorithm_definition|알고리즘]], [[327_ssd|SSD]]/[[482_nvme|NVMe]] 스토리지 구조까지 기술사 시험에 완벽 대비할 수 있도록 800여 개의 심화 토픽을 총망라했습니다.)