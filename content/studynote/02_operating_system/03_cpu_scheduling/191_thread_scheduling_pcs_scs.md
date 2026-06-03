+++
title = "191. 스레드 스케줄링 - 프로세스 경쟁 범위(PCS) vs 시스템 경쟁 범위(SCS)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링은 [다중 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/) 환경에서 '누가 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 CPU에 올릴 것인가'에 대한 결정권의 주체를 다루며, 유저 레벨 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 결정하는 <strong>PCS (Process-Contention <a href="/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/">Scope</a>)</strong>와 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 직접 결정하는 <strong>SCS (System-Contention <a href="/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/">Scope</a>)</strong>로 나뉜다.
> 2. **가치**: PCS는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 개입([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))이 없어 극도로 가볍고 빠르지만 블로킹([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 시 프로세스 전체가 멈추는 한계가 있으며, SCS는 무겁지만 진정한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성(Parallelism)과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 보호를 달성하는 현대 OS의 표준 모델이다.
> 3. **융합**: 이 두 모델의 투쟁은 단순히 스케줄링 알고리즘의 차이를 넘어, 사용자 공간(User Space)과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Space) 간의 자원 제어권(Control)을 둘러싼 거대한 아키텍처 진화(예: Green Threads, Goroutines)의 뼈대가 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 프로세스 내의 실행 흐름이다. 시스템에 수천 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 존재할 때 이들을 레디 큐([Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/))에 세우고 우선순위를 매기는 경쟁 범위(Contention [Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/))가 프로세스 '내부'에 국한되느냐(PCS), 시스템 '전체' [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 경쟁하느냐(SCS)를 구분하는 스케줄링 모델이다.
- **필요성**: 과거 싱글 코어 시절에는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)라는 존재 자체를 모른 채([User-level Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/)) 오직 프로세스만 스케줄링했다. 멀티 코어가 대중화되면서, 하나의 프로세스 안에 있는 수십 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 여러 물리 코어에 찢어서 뿌려주는 진정한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리가 필요해졌고, 이를 위해 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 존재를 인지하고 통제권을 뺏어오는 아키텍처적 전환(SCS 도입)이 필수 불가결해졌다.

- **등장 배경**: 자바 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 버전의 그린 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Green Threads)나 GNU [Pth](/knowledge-base/studynote/09_security/12_identity_threat_advanced/592_pth/) 같은 유저 레벨 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)는 PCS 방식을 썼다. 하지만 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나가 디스크 I/O를 기다리느라 멈추면(Block) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 그 프로세스 전체를 통째로 정지시켜 버리는 치명적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)([다대일](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/) 모델의 한계)이 발견되면서, 현대 윈도우와 리눅스는 철저한 SCS([일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델) 체제로 굳어지게 되었다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">PCS (Process-Contention Scope) vs SCS (System-Contention Scope) 권한 분리</div></div>
<div class="kb-diagram-note">(유저 공간)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">프로세스 A</div><div class="kb-diagram-node">프로세스 B</div></div>
<div class="kb-diagram-note">스레드1 ↔ 스레드2 (경쟁) 스레드3 ↔ 스레드4 (경쟁)</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">스레드 라이브러리가 PCS 스케줄링</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-note">─</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">(모드 전환 경계선)</div>
<div class="kb-diagram-note">(커널 공간)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">커널 스레드 K1</div><div class="kb-diagram-node">커널 스레드 K2</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">OS 커널이 SCS 스케줄링</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-note">─</div></div>
<div class="kb-diagram-note">(K1 ↔ K2 ↔ K3 전역 경쟁)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">물리적 CPU 코어</div></div>
</div>
</div>


**[다이어그램 해설]** PCS의 핵심은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(1, 2, 3, 4)의 존재를 전혀 모른다는 것이다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 그저 껍데기인 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(K1, K2)만 스케줄링한다. 프로세스 내부에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1과 2가 어떤 우선순위로 싸우든 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 입장에서는 알 바 아니다. 반면 SCS 환경에서는 사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1:1로 매핑되어, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1, 2, 3, 4가 시스템 전체의 큐에 내려와 옥좌(CPU)를 놓고 수만 개의 타 프로세스 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들과 무한 경쟁을 펼치게 된다.

- **📢 섹션 요약 비유**: PCS는 뷔페에서 가족(프로세스) 대표 한 명만 줄을 서서 음식을 받아온 뒤 테이블에서 자기들끼리(유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) 나눠 먹는 것이고, SCS는 가족 전원이 직접 각자의 접시를 들고 뷔페 100미터 대기 줄([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레디 큐)에 서서 옆집 사람들과 치열하게 경쟁하는 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. PCS (Process-Contention [Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/)) 스케줄링
- **주체**: 유저 스페이스(User Space)에서 동작하는 '[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) (예: pthread, Go 런타임)'가 전권을 쥔다.
- **특징**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드로 진입할 필요가 없다. (시스템 콜 없음). 따라서 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))이 단순히 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)(Function [Call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/))이나 [스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) 교체 수준의 오버헤드만 발생시키므로 **극도로 빠르다**. (단 수십 나노초 소요)
- **한계**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 아무리 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)1에 CPU를 주고 싶어도, OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 그 프로세스의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(K1)를 CPU에서 쫓아내 버리면(Time [Quantum](/knowledge-base/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/) 소진 등), [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 결정은 완벽히 무용지물이 된다.

### 2. SCS (System-Contention [Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/)) 스케줄링
- **주체**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS) 내부의 [단기 스케줄러](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/161_short_term_scheduler/) (CPU [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))가 전권을 쥔다.
- **특징**: Windows, Linux, MacOS 등 현대 범용 OS의 기본 동작 방식이다. (1:1 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 모델 채택). 시스템에 존재하는 1만 개의 모든 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 단일 또는 멀티 큐에 늘어서서 공평하게 타임 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)([RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/))를 놓고 경쟁한다.
- **한계**: [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 교체될 때마다 반드시 사용자 모드에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드로의 전환(Mode [Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))이 일어나야 하므로, PCS에 비해 **수십~수백 배 무겁고 느리다**. (수 마이크로초 소요)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PCS 방식의 치명적 결함: 블로킹(Blocking) 연대 책임</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(상황: 사용자 프로세스 내에 웹 요청을 받는 스레드가 10개 있다.)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 스레드 1번이 디스크에서 파일을 읽어오라고 시스템 콜을 호출함.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 커널은 "이 프로세스(K1)가 I/O를 요청했군" 하고 K1 자체를</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Waiting(Blocked) 상태로 잠재워 버림.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 🚨 멸망의 순간: K1이 잠들었으므로, 스레드 라이브러리가 아무리</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스레드 2~10번을 깨워 코드를 실행시키려 해도 CPU가 할당 안 됨!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 결과: 스레드 1개의 디스크 I/O 때문에 나머지 9개의 멀쩡한 스레드도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">강제로 연대 책임(Hang)을 지고 전체 프로세스가 죽어버림.</div></div>
</div>
</div>


**[다이어그램 해설]** PCS의 가벼움 뒤에 숨겨진 치명적 맹점이다. 이 문제를 해결하려면 코딩을 할 때 절대로 시스템 콜을 부르지 않거나(비동기 논블로킹 I/O 강제), 아예 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나하나를 통제하여(SCS 방식 채택) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 1번만 잠재우고 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 2번은 다른 코어에서 돌려주도록 OS 아키텍처를 뒤엎어야만 했다.

- **📢 섹션 요약 비유**: PCS는 한 반(프로세스)에서 학생 1명([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 떠든다고 선생님([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))이 반 전체에게 벌을 주는 "연대 책임" 교실이고, SCS는 떠든 학생 딱 1명만 교무실로 끌고 가고 나머지 학생들은 계속 수업을 들을 수 있는 "개인 책임제" 교실입니다.

---

## Ⅲ. 비교 및 연결

### PCS vs SCS 극단적 패러다임 비교

| [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | PCS (유저 레벨 우선) | SCS ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 우선) |
|:---|:---|:---|
| **스케줄링 오버헤드** | **매우 낮음** (가벼운 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 스왑) | **매우 높음** (모드 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 및 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 락 동반) |
| <strong>멀티코어 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성 (Parallelism)</strong> | **거의 불가능** ([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 1개 코어만 주면 끝) | <strong>완벽한 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성</strong> ([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 10개를 코어 10개에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)) |
| **I/O 블로킹 위험** | 치명적 (하나 막히면 다 막힘) | 독립적 (막힌 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)만 슬립) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/790_posix_threads_pthreads_standard_api/">Pthreads</a> (POSIX) <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | `PTHREAD_SCOPE_PROCESS` 로 명시 | `PTHREAD_SCOPE_SYSTEM` 로 명시 (현대 디폴트) |
| **대표적 구현체** | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) Java Green [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/), <strong>Go 언어의 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/">Goroutine</a></strong> | Windows 쓰레드, Linux NPTL, [Mac](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) OS |

### 시대의 나선형 진화: [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)과 PCS의 부활
1990년대 초반에는 오버헤드 때문에 PCS가 유행하다가, 2000년대 멀티코어가 등장하며 완벽한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 제공하는 SCS(1:1 모델)가 천하를 통일했다.
하지만 2010년대 이후 C10K 문제 (동접자 1만 명)와 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 폭증으로 인해, 한 서버에 SCS 기반 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 1만 개 띄웠더니 모드 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 오버헤드와 메모리([스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)) 고갈로 서버가 터져버리는 현상이 발생했다. 
이에 대한 반동으로 최근 <strong>Go 언어의 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/">고루틴</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/">Goroutine</a>)이나 코틀린의 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/">코루틴</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/">Coroutine</a>)</strong>은 수십 개의 SCS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 위에서 수십만 개의 깃털처럼 가벼운 유저 태스크를 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 직접 스케줄링하는 **"현대화된 하이브리드 PCS"** 철학을 부활시켜 클라우드 생태계를 장악하고 있다.

- **📢 섹션 요약 비유**: 유행은 돌고 돕니다. 옛날엔 관리자가 1명(PCS)이라 답답해서 직원 모두가 사장에게 직접 보고(SCS)하게 했더니, 회사가 커지자 사장이 보고만 받다 쓰러졌습니다(오버헤드 붕괴). 결국 다시 중간 관리자(M:N 모델의 Go 런타임)를 두어 보고 체계를 가볍게 압축시키는 현대화된 PCS로 돌아온 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong>리눅스 Pthread 스케줄링 범위 (<a href="/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/">Scope</a>) <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 실무에서 C/C++로 [다중 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/) 서버를 개발할 때, 리눅스 NPTL(Native POSIX [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [Library](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링 범위가 기본적으로 100% SCS(`PTHREAD_SCOPE_SYSTEM`)로 고정되어 있다. 개발자가 억지로 `pthread_attr_setscope` 함수를 써서 PCS를 쓰려 해도 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이를 무시한다. 즉, 현대 백엔드 개발자(C/C++/Java)가 띄우는 모든 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 OS가 멱살을 잡고 통제하는 무거운 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자원임을 뼛속 깊이 인지하고 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)) 튜닝을 해야 한다.
2. **Go 언어 런타임 (GMP 모델)의 압도적 성과**: Go 언어가 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s)와 [도커](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)([Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/))를 만들어낸 클라우드 시대의 지배 언어가 된 이유는 스케줄링 아키텍처에 있다. Go는 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에게 수만 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 던지는 무식한 SCS 방식을 버렸다. OS [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(M)는 코어 수만큼만 딱 띄워놓고, 그 위에서 Go 런타임 자체 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)(P)가 십만 개의 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/)(G, 유저 레벨 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 <strong>PCS 방식</strong>으로 잽싸게 스위칭하며 처리한다. 심지어 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) 하나가 I/O에 막히면([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)), 런타임이 다른 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/)을 안 막힌 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 몰래 이사시켜 버리는([Work Stealing](/knowledge-base/studynote/02_operating_system/04_synchronization/271_work_stealing/)) 기적의 로직으로 PCS의 치명적 단점마저 파괴해 냈다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">고동시성(High-Concurrency) 백엔드 서버 스레드 아키텍처 트리</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">요구사항: 초당 10만 건(100K)의 동시 웹소켓 연결 처리 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ 선택할 스레드 스케줄링/언어 모델은?</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전통적 SCS (1:1 커널 스레드) 모델 - Java Thread/C++</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 동작: 연결 1개당 스레드 1개 생성 (10만 개 생성 시도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 결과: 스레드 1개당 1MB 스택 소모 = 100GB 메모리 증발</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 장애: 커널 스케줄러(SCS)가 10만 개 교체하다 뻗음 (OOM)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현대적 하이브리드 PCS (M:N 모델) - Go Goroutine/Node.js</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 동작: 커널 스레드는 8개(코어수)만 띄우고 그 위에서 동작</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 결과: 고루틴 1개당 2KB 소모 = 고작 200MB 메모리 사용!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ 승리: 커널 오버헤드 0, 유저 스페이스 PCS 스위칭으로 쾌적</div></div>
</div>
</div>


**[다이어그램 해설]** 아키텍트가 SCS의 무거움을 깨닫고 PCS의 가벼움으로 회귀하는 현대 백엔드 패러다임 변화를 증명한다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 믿고 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 맡기는 시대(Java/Spring Boot 1세대)는 끝났다. 넷플릭스, 우버 등 빅테크들은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 SCS [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 개입을 최소화하고, 유저 영역에서 RxJava, WebFlux([이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)), Go [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) 등 "내가 직접 쪼개서(PCS) 돌리겠다"는 방식으로 아키텍처를 뒤엎고 있다.

- **📢 섹션 요약 비유**: 수만 개의 화물(트래픽)을 나를 때, 화물마다 일일이 트럭(SCS [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 배정하면 고속도로([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 트럭으로 꽉 차서 마비됩니다. 거대한 트럭(코어 개수) 몇 대만 띄우고, 그 트럭 안에서 짐꾼(Go 런타임, PCS)들이 작은 상자 수만 개를 테트리스처럼 잽싸게 밀어 넣는 것이 현대 물류(서버)의 정석입니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
PCS와 SCS의 차이를 명확히 이해하면, 개발자는 `Thread.sleep()`이나 `File.read()` 같은 블로킹([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 코드가 시스템의 어떤 계층(유저/[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에서 얼마나 파괴적인 나비효과를 가져오는지 예측할 수 있으며, 시스템의 메모리와 디스패치 한계치를 고려한 최적의 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)) 크기를 계산해 낼 수 있다.

### 결론 및 미래 전망
[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 컴퓨터 과학의 영원한 떡밥이었던 PCS(유저 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))와 SCS([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))의 전쟁은, 결국 "둘 다 쓴다"는 <strong>M:N <a href="/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/397_multithreading/">멀티스레딩</a> 모델(하이브리드)</strong>로 완벽한 타협을 이루었다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 보안과 하드웨어 제어를 위해 묵직하고 강력한 SCS 방식으로 물리 코어를 방어하고, 애플리케이션 프레임워크(Go, [Rust](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/), Kotlin)는 그 위에서 수십만 개의 경량 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Fiber, [Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/))를 극강의 속도로 쳐내는 PCS 스케줄링을 독자적으로 구축하는 '투 트랙(Two-track)' 전략이 클라우드 네이티브와 Web3 시대를 관통하는 영원한 표준 아키텍처로 자리매김했다.

- **📢 섹션 요약 비유**: 중앙 정부(OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))는 무거운 국방과 외교(SCS)만 튼튼하게 책임지고 통제하되, 각 시도 지자체(언어 런타임)에게 자치권(PCS)을 주어 동네 구멍가게의 잡다한 분쟁은 경찰 부르지 않고 동네 이장이 1초 만에 해결하게 만드는 완벽한 2단계 분할 통치 국가의 완성입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [복권 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/189_lottery_scheduling/) ([Lottery Scheduling](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/189_lottery_scheduling/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [공평 몫 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/190_fair_share_scheduling/) ([Fair-share Scheduling](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/190_fair_share_scheduling/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| LWP 디스패치 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [다중 처리기 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/193_smp_symmetric_multiprocessing/) ([Multiprocessor Scheduling](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/193_smp_symmetric_multiprocessing/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">공평 몫 스케줄링 (Fair-share Scheduling)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스레드 스케줄링</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">LWP 디스패치</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">다중 처리기 스케줄링 (Multiprocessor Scheduling)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 체육 대회에서 달리기 선수를 뽑을 때, "반장(프로세스)이 자기 반 아이들 중에서 몰래 순서를 정해 뛰게 하는 것"이 **PCS** 예요. (엄청 빠르지만 반장이 아프면 반 전체가 기권해야 해요!)
2. 반면에 교장 선생님([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))이 전교생을 운동장에 다 모아놓고 "너 1등 뛰어! 너 2등 뛰어!"라고 직접 지시하는 게 **SCS** 예요.
3. 교장 선생님이 지시하면 너무 시끄럽고 시간(오버헤드)이 오래 걸리지만, 한 명이 다쳐도 다른 친구를 바로 뛰게 할 수 있어서 아주 안전하고 확실하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 191 / 800

← **이전**: [190. 공평 몫 스케줄링 (Fair-share Scheduling)](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/190_fair_share_scheduling/)
**다음**: [192. 다중 처리기 스케줄링 (Multiple-Processor Scheduling)](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/192_multiple_processor_scheduling/) →

---
