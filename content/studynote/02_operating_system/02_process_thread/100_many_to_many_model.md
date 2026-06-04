+++
title = "100. 다대다 (Many-to-Many) 스레드 모델"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다대다 (Many-to-Many) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 모델은 응용 프로그램이 무한대로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 수 있는 [사용자 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/) (ULT, [User-Level Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/))를 하드웨어 제한에 맞춘 소수의 [커널 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/) (KLT, [Kernel-Level Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/))에 유연하게 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))하는 하이브리드 아키텍처다.
> 2. **가치**: [다대일](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/) ([Many-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/)) 모델의 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 블로킹 ([Blocking](/knowledge-base/studynote/02_operating_system/02_process_thread/122_sync_async_communication/)) 마비 문제와 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) ([One-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/)) 모델의 과도한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자원 소모 및 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switching) 오버헤드를 동시에 해결하여, 극단적 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)과 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성을 모두 달성한다.
> 3. **판단 포인트**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부에서는 구현의 극단적 복잡성 때문에 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델로 회귀했으나, 이 철학은 Go 언어의 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) ([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/)) 등 현대 런타임 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)로 이식되어 대용량 트래픽을 처리하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경의 근간이 되었다.

---

## Ⅰ. 개요 및 필요성

[멀티스레딩](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/397_multithreading/) (Multi-threading) 환경에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 관리가 일어나는 위치에 따라 사용자 수준과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준으로 나뉜다. 다대다 (Many-to-Many) 모델은 M개의 [사용자 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/096_user_level_thread/) (ULT)를 N개의 [커널 수준 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/097_kernel_level_thread/) (KLT)에 매핑하는 방식이다 (M ≥ N).

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시스템의 [다대일](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/) 모델은 가볍고 빨랐지만 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 하나가 입출력(I/O) 요청으로 블로킹되면 [전체 프로세스](/knowledge-base/studynote/02_operating_system/06_memory_management/337_standard_vs_paging_swapping/)가 멈추는 치명적 약점이 있었다. 반면 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리는 완벽했지만 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 수만 개로 늘어나면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환 비용과 메모리 고갈로 시스템이 붕괴([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))되었다. 엔지니어들은 이 두 극단의 한계를 극복하기 위해 사용자 공간에서 [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 비용을 최소화하면서도, 멀티코어 (Multi-core) CPU의 능력을 100% 활용하고 특정 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 블로킹이 전체를 멈추지 않게 하는 타협점이 필요했고, 그 결과 다대다 모델이 등장했다.

- **📢 섹션 요약 비유**: 다대다 모델은 1,000명의 고객(사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 몰려왔을 때 창구 직원([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))을 1,000명 뽑는 대신, 최적의 인원인 5명만 배치하고 로비 매니저([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/))가 빈 창구로 고객을 유연하게 안내하여 은행 마비를 막는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

다대다 모델의 아키텍처는 사용자 공간과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간을 이어주는 가상의 매개체인 경량 프로세스 (LWP, Lightweight [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))와, 두 공간 사이의 통신 메커니즘으로 완성된다.

```text
+--------------------------------------------------------------+
|          다대다 모델의 스케줄러 촉발 및 다중화 아키텍처      |
+--------------------------------------------------------------+
| [사용자 공간]          [스레드 라이브러리 (로비 매니저)]       |
|  ULT 1 -+                |                                   |
|  ULT 2 -+---> 동적 매핑 ---> [ LWP 1 ] ---> (KLT 1로 연결)       |
|  ULT 3 -+                |   (I/O 블로킹 발생!)              |
|                          |                                   |
| [스케줄러 촉발 발동]     |                                   |
| 커널 --(Upcall)---> "LWP 1 멈췄어! 대신 새 LWP 2 줄게!"       |
|                          |                                   |
|  ULT 4 -+                |                                   |
|  ULT 5 -+---> 즉시 재배정 --> [ LWP 2 ] ---> (KLT 2로 연결)       |
|  ULT 6 -+                |   (지연 없이 계속 실행됨)         |
+--------------------------------------------------------------+
```

이 모델이 블로킹 문제를 극복하는 핵심 원리는 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 촉발 ([Scheduler Activation](/knowledge-base/studynote/02_operating_system/02_process_thread/114_scheduler_activation/))과 업콜 ([Upcall](/knowledge-base/studynote/02_operating_system/02_process_thread/115_upcall/))이다. ULT 1이 I/O를 호출해 KLT 1이 멈추게 되면, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이 사실을 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)에 업콜(콜백)로 알려주고 새로운 LWP를 임시로 제공 단서한다. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)는 멈춘 ULT 1의 상태를 저장한 뒤, 대기 중이던 다른 ULT 4를 새로 받은 LWP 2에 신속하게 배정한다. 이 메커니즘 덕분에 하나의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 블로킹되어도 프로세스 전체가 멈추지 않고 남은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 계속 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 실행된다.

- **📢 섹션 요약 비유**: 고속도로를 달리던 택시(LWP)가 타이어 펑크(블로킹)로 멈췄을 때, 본사([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 전체 운행을 멈추는 대신 즉시 빈 대체 택시(새 LWP)를 보내어 다른 대기 승객(다른 ULT)들이 목적지로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 출발할 수 있게 관제하는 시스템이다.

---

## Ⅲ. 비교 및 연결

다대다 모델은 시스템 자원 한계를 돌파하는 이론적 최상위 포식자다. [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)) 증가에 따른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 변화를 비교해 보면 그 진가가 드러난다.

| 비교 지표 | [다대일](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/) ([Many-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/098_many_to_one_model/)) | [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) ([One-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/)) | 다대다 (Many-to-Many) |
| :--- | :--- | :--- | :--- |
| **블로킹 전파** | 1개 블로킹 시 [전체 프로세스](/knowledge-base/studynote/02_operating_system/06_memory_management/337_standard_vs_paging_swapping/) 중단 | 독립적. 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 영향 없음 | 업콜을 통해 새 자원을 받아 영향 없음 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성 (멀티코어)</strong> | 불가능 (단일 코어에 종속) | 가능 (하드웨어 코어 수만큼 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) | 가능 (동적 할당된 KLT 수만큼 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 개수 한계</strong> | 무한대 (가벼운 메모리 소모) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 한계에 종속 (수천 개 즈음 붕괴) | 무한대 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능, 스위칭 부하 없음 |
| **구조적 복잡성** | [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 수준의 단순 구현 | OS 차원의 지원 필요 (구현 쉬움) | [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)와 OS 간의 고도의 통신 필요 |

[일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 1만 개를 넘어서면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 객체 관리 비용과 L1 캐시 미스로 인해 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) 그래프가 급전직하([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))한다. 반면 다대다 모델은 사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 수십만 개 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하더라도, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 스위칭되는 KLT의 수는 하드웨어 코어 수(예: 8개)로 엄격히 통제되므로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 그래프가 고점에서 꺾이지 않고 평탄하게 유지된다.

- **📢 섹션 요약 비유**: [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델은 짐을 나르기 위해 대형 트럭(KLT)을 끝도 없이 늘려 결국 도로를 마비([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))시키는 방식이고, 다대다 모델은 기차의 앞 기관차(KLT) 수는 고정해두고 가벼운 화물칸(ULT)만 끝없이 뒤에 이어 붙여 교통체증 없이 무한정 짐을 나르는 원리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

이론적으로 완벽한 다대다 모델이지만, 실제 인프라 환경에서는 극적인 반전과 융합의 의사결정이 일어났다.

1. **OS 레벨에서의 포기 판단**: 과거 Sun Solaris는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서 다대다 모델을 구현했으나, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 통신하는 '업콜([Upcall](/knowledge-base/studynote/02_operating_system/02_process_thread/115_upcall/))'의 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 복잡성이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패닉을 유발하는 등 유지보수 악몽을 낳았다. 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(Linux, Windows) 기술사들은 "차라리 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드를 최적화해서 무거운 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델을 하드웨어 스펙으로 짓누르거나 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))로 제어하는 것이 낫다"고 판단하여 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨의 M:M 모델을 사실상 폐기했다.
2. **런타임 레벨에서의 화려한 부활**: 그러나 초당 수백만 개의 I/O를 처리해야 하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 시대가 도래하며 [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 모델은 다시 메모리 한계(C10K 문제)에 부딪혔다. 개발자들은 OS 대신 언어 런타임에 다대다 모델을 내장시켰다. Go 언어의 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) ([Goroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/))이나 Java 21의 가상 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (Virtual [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))가 그 주인공이다. [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) 10만 개를 만들어도 OS [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 코어 수만큼만 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되어 동작하므로, 시스템 콜([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/)) 병목 없이 압도적인 동시 처리가 가능하다.

- **📢 섹션 요약 비유**: 너무 복잡해서 자주 고장 나던 초정밀 기계식 시계(OS 레벨의 다대다)는 버려졌지만, 그 핵심 설계도(M:M 철학)는 최신 스마트워치의 소프트웨어 칩(Go 언어 런타임)으로 그대로 이식되어 세상을 지배하고 있다.

---

## Ⅴ. 기대효과 및 결론

다대다 모델은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자원의 엄격한 제한 안에서 응용 프로그램에게 무한한 논리적 실행 흐름을 허락하는 궁극의 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 패러다임이다.

개발자는 콜백 지옥(Callback Hell) 같은 복잡한 비동기 코딩을 할 필요 없이 직관적인 동기식 코드를 작성하면서도, 뒷단에서는 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 수만 개의 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 적은 수의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 쪼개어 돌리는 마법을 누릴 수 있다. 이는 클라우드 환경에서 서버의 메모리 풋프린트를 극단적으로 줄여 인프라 비용을 절감하는 핵심 동력이 된다. 다대다 모델의 철학은 OS 밖으로 뛰쳐나와 현대 백엔드 아키텍처의 필수 표준 기술로 완전히 자리 잡았다.

- **📢 섹션 요약 비유**: 다대다 모델은 과거의 유물이 아니라, 수백만 대의 서버 위에서 거대한 클라우드 트래픽을 흔들림 없이 떠받치고 있는 보이지 않는 최첨단 서스펜션(완충 장치)이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong>경량 프로세스 (LWP, Lightweight <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/">Process</a>)</strong> | 사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 사이의 인터페이스 역할을 하며, 스케줄링의 징검다리가 되는 자료 구조 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a> 촉발 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/114_scheduler_activation/">Scheduler Activation</a>)</strong> | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 블로킹되었을 때, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 프로세스를 중단하지 않고 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)에게 대체 자원(새 LWP)을 통지해 주는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-사용자 통신 규약 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/">고루틴</a> (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/">Goroutine</a>)</strong> | 다대다 모델의 철학을 OS 레벨에서 언어 런타임 레벨로 끌어올려 구현한 Go 언어의 초경량 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) |

### 📈 관련 키워드 및 발전 흐름도

```text
다대일 (Many-to-One) 모델 · 빠른 스위칭, 블로킹 마비
    |
    v
일대일 (One-to-One) 모델 · 병렬성 확보, 컨텍스트 스위칭 오버헤드
    |
    v
다대다 (Many-to-Many) 모델 · 스케줄러 촉발 (Scheduler Activation) 도입
    |
    v
OS 레벨 다대다 사장 · Linux NPTL(1:1) 표준화 및 스레드 풀(Thread Pool) 활용
    |
    v
런타임 레벨 다대다 부활 · Go 고루틴(Goroutine), Java 가상 스레드(Virtual Thread)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원(컴퓨터)에 1,000명의 아이들(사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 롤러코스터를 타러 왔는데, 진짜 기차([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))는 딱 10대밖에 없어요.
2. 옛날에는 기차 하나가 고장 나면 모든 아이가 하염없이 기다려야 했지만, 다대다 모델은 똑똑한 안내원이 있어서 아이들을 재빨리 멀쩡한 다른 기차로 갈아태워 준답니다!
3. 그래서 비싼 기차를 무작정 많이 만들지 않아도, 수많은 아이들이 끊기지 않고 재미있게 놀이공원을 계속 즐길 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 800

<- **이전**: [99. 일대일 (One-to-One) 스레드 모델](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/)
**다음**: [101. 두 수준 (Two-level) 모델](/knowledge-base/studynote/02_operating_system/02_process_thread/101_two_level_model/) ->

---
