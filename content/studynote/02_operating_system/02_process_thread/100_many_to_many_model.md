---
title: 100. 다대다 (Many-to-Many) 스레드 모델
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다대다 (Many-to-Many) [[092_thread_lwp|스레드]] 모델은 응용 프로그램이 무한대로 [[087_process_state_transition|생성]]할 수 있는 [[096_user_level_thread|사용자 수준 스레드]] (ULT, [[096_user_level_thread|User-Level Thread]])를 하드웨어 제한에 맞춘 소수의 [[097_kernel_level_thread|커널 수준 스레드]] (KLT, [[097_kernel_level_thread|Kernel-Level Thread]])에 유연하게 [[071_다중화_Multiplexing|다중화]]([[071_다중화_Multiplexing|Multiplexing]])하는 하이브리드 아키텍처다.
> 2. **가치**: [[098_many_to_one_model|다대일]] ([[098_many_to_one_model|Many-to-One]]) 모델의 단일 [[092_thread_lwp|스레드]] 블로킹 ([[122_sync_async_communication|Blocking]]) 마비 문제와 [[099_one_to_one_model|일대일]] ([[099_one_to_one_model|One-to-One]]) 모델의 과도한 [[022_kernel_role|커널]] 자원 소모 및 [[211_context_switch|문맥 교환]] ([[033_context|Context]] Switching) 오버헤드를 동시에 해결하여, 극단적 [[014_concurrency|동시성]]과 [[430_index_fast_full_scan|병렬]]성을 모두 달성한다.
> 3. **판단 포인트**: [[001_operating_system_purpose|운영체제]] [[022_kernel_role|커널]] 내부에서는 구현의 극단적 복잡성 때문에 [[099_one_to_one_model|일대일]] 모델로 회귀했으나, 이 철학은 Go 언어의 [[140_goroutine|고루틴]] ([[140_goroutine|Goroutine]]) 등 현대 런타임 [[079_kube_scheduler_pod_placement|스케줄러]]로 이식되어 대용량 트래픽을 처리하는 [[531_cloud_native_architecture|클라우드 네이티브]] 환경의 근간이 되었다.

---

## Ⅰ. 개요 및 필요성

[[397_multithreading|멀티스레딩]] (Multi-threading) 환경에서 [[092_thread_lwp|스레드]]는 [[087_process_state_transition|생성]]과 관리가 일어나는 위치에 따라 사용자 수준과 [[022_kernel_role|커널]] 수준으로 나뉜다. 다대다 (Many-to-Many) 모델은 M개의 [[096_user_level_thread|사용자 수준 스레드]] (ULT)를 N개의 [[097_kernel_level_thread|커널 수준 스레드]] (KLT)에 매핑하는 방식이다 (M ≥ N).

[[459_quic_fec_forward_error_correction|초기]] 시스템의 [[098_many_to_one_model|다대일]] 모델은 가볍고 빨랐지만 [[092_thread_lwp|스레드]] 하나가 입출력(I/O) 요청으로 블로킹되면 [[337_standard_vs_paging_swapping|전체 프로세스]]가 멈추는 치명적 약점이 있었다. 반면 [[099_one_to_one_model|일대일]] 모델은 [[430_index_fast_full_scan|병렬]] 처리는 완벽했지만 [[092_thread_lwp|스레드]]가 수만 개로 늘어나면 [[022_kernel_role|커널]] 모드 전환 비용과 메모리 고갈로 시스템이 붕괴([[257_thrashing|Thrashing]])되었다. 엔지니어들은 이 두 극단의 한계를 극복하기 위해 사용자 공간에서 [[034_context_switch|컨텍스트 스위칭]] 비용을 최소화하면서도, 멀티코어 (Multi-core) CPU의 능력을 100% 활용하고 특정 [[092_thread_lwp|스레드]]의 블로킹이 전체를 멈추지 않게 하는 타협점이 필요했고, 그 결과 다대다 모델이 등장했다.

- **📢 섹션 요약 비유**: 다대다 모델은 1,000명의 고객(사용자 [[092_thread_lwp|스레드]])이 몰려왔을 때 창구 직원([[022_kernel_role|커널]] [[092_thread_lwp|스레드]])을 1,000명 뽑는 대신, 최적의 인원인 5명만 배치하고 로비 매니저([[092_thread_lwp|스레드]] [[336_library_vs_framework|라이브러리]])가 빈 창구로 고객을 유연하게 안내하여 은행 마비를 막는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

다대다 모델의 아키텍처는 사용자 공간과 [[022_kernel_role|커널]] 공간을 이어주는 가상의 매개체인 경량 프로세스 (LWP, Lightweight [[300_process|Process]])와, 두 공간 사이의 통신 메커니즘으로 완성된다.

```text
┌──────────────────────────────────────────────────────────────┐
│          다대다 모델의 스케줄러 촉발 및 다중화 아키텍처      │
├──────────────────────────────────────────────────────────────┤
│ [사용자 공간]          [스레드 라이브러리 (로비 매니저)]       │
│  ULT 1 ─┐                │                                   │
│  ULT 2 ─┼──▶ 동적 매핑 ──▶ [ LWP 1 ] ──▶ (KLT 1로 연결)       │
│  ULT 3 ─┘                │   (I/O 블로킹 발생!)              │
│                          │                                   │
│ [스케줄러 촉발 발동]     │                                   │
│ 커널 ──(Upcall)──▶ "LWP 1 멈췄어! 대신 새 LWP 2 줄게!"       │
│                          │                                   │
│  ULT 4 ─┐                │                                   │
│  ULT 5 ─┼──▶ 즉시 재배정 ─▶ [ LWP 2 ] ──▶ (KLT 2로 연결)       │
│  ULT 6 ─┘                │   (지연 없이 계속 실행됨)         │
└──────────────────────────────────────────────────────────────┘
```

이 모델이 블로킹 문제를 극복하는 핵심 원리는 [[079_kube_scheduler_pod_placement|스케줄러]] 촉발 ([[114_scheduler_activation|Scheduler Activation]])과 업콜 ([[115_upcall|Upcall]])이다. ULT 1이 I/O를 호출해 KLT 1이 멈추게 되면, [[022_kernel_role|커널]]은 이 사실을 [[092_thread_lwp|스레드]] [[336_library_vs_framework|라이브러리]]에 업콜(콜백)로 알려주고 새로운 LWP를 임시로 제공 단서한다. [[092_thread_lwp|스레드]] [[336_library_vs_framework|라이브러리]]는 멈춘 ULT 1의 상태를 저장한 뒤, 대기 중이던 다른 ULT 4를 새로 받은 LWP 2에 신속하게 배정한다. 이 메커니즘 덕분에 하나의 [[092_thread_lwp|스레드]]가 블로킹되어도 프로세스 전체가 멈추지 않고 남은 [[092_thread_lwp|스레드]]들이 계속 [[430_index_fast_full_scan|병렬]]로 실행된다.

- **📢 섹션 요약 비유**: 고속도로를 달리던 택시(LWP)가 타이어 펑크(블로킹)로 멈췄을 때, 본사([[022_kernel_role|커널]])가 전체 운행을 멈추는 대신 즉시 빈 대체 택시(새 LWP)를 보내어 다른 대기 승객(다른 ULT)들이 목적지로 [[015_지연_데이터_관점|지연]] 없이 출발할 수 있게 관제하는 시스템이다.

---

## Ⅲ. 비교 및 연결

다대다 모델은 시스템 자원 한계를 돌파하는 이론적 최상위 포식자다. [[014_concurrency|동시성]]([[266_other_transparency|Concurrency]]) 증가에 따른 [[282_performance_tactics|성능]] 변화를 비교해 보면 그 진가가 드러난다.

| 비교 지표 | [[098_many_to_one_model|다대일]] ([[098_many_to_one_model|Many-to-One]]) | [[099_one_to_one_model|일대일]] ([[099_one_to_one_model|One-to-One]]) | 다대다 (Many-to-Many) |
| :--- | :--- | :--- | :--- |
| **블로킹 전파** | 1개 블로킹 시 [[337_standard_vs_paging_swapping|전체 프로세스]] 중단 | 독립적. 다른 [[092_thread_lwp|스레드]]에 영향 없음 | 업콜을 통해 새 자원을 받아 영향 없음 |
| **[[430_index_fast_full_scan|병렬]]성 (멀티코어)** | 불가능 (단일 코어에 종속) | 가능 (하드웨어 코어 수만큼 [[430_index_fast_full_scan|병렬]]) | 가능 (동적 할당된 KLT 수만큼 [[430_index_fast_full_scan|병렬]]) |
| **[[087_process_state_transition|생성]] 개수 한계** | 무한대 (가벼운 메모리 소모) | [[022_kernel_role|커널]] 한계에 종속 (수천 개 즈음 붕괴) | 무한대 [[087_process_state_transition|생성]] 가능, 스위칭 부하 없음 |
| **구조적 복잡성** | [[336_library_vs_framework|라이브러리]] 수준의 단순 구현 | OS 차원의 지원 필요 (구현 쉬움) | [[336_library_vs_framework|라이브러리]]와 OS 간의 고도의 통신 필요 |

[[099_one_to_one_model|일대일]] 모델은 [[092_thread_lwp|스레드]]가 1만 개를 넘어서면 [[022_kernel_role|커널]] 객체 관리 비용과 L1 캐시 미스로 인해 [[139_throughput|처리량]]([[139_throughput|Throughput]]) 그래프가 급전직하([[257_thrashing|Thrashing]])한다. 반면 다대다 모델은 사용자 [[092_thread_lwp|스레드]]를 수십만 개 [[087_process_state_transition|생성]]하더라도, [[022_kernel_role|커널]]에서 스위칭되는 KLT의 수는 하드웨어 코어 수(예: 8개)로 엄격히 통제되므로 [[282_performance_tactics|성능]] 그래프가 고점에서 꺾이지 않고 평탄하게 유지된다.

- **📢 섹션 요약 비유**: [[099_one_to_one_model|일대일]] 모델은 짐을 나르기 위해 대형 트럭(KLT)을 끝도 없이 늘려 결국 도로를 마비([[257_thrashing|Thrashing]])시키는 방식이고, 다대다 모델은 기차의 앞 기관차(KLT) 수는 고정해두고 가벼운 화물칸(ULT)만 끝없이 뒤에 이어 붙여 교통체증 없이 무한정 짐을 나르는 원리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

이론적으로 완벽한 다대다 모델이지만, 실제 인프라 환경에서는 극적인 반전과 융합의 의사결정이 일어났다.

1. **OS 레벨에서의 포기 판단**: 과거 Sun Solaris는 [[022_kernel_role|커널]] 레벨에서 다대다 모델을 구현했으나, [[022_kernel_role|커널]]과 [[336_library_vs_framework|라이브러리]]가 통신하는 '업콜([[115_upcall|Upcall]])'의 [[212_synchronization_mechanisms|동기화]] 복잡성이 [[022_kernel_role|커널]] 패닉을 유발하는 등 유지보수 악몽을 낳았다. 현대 [[001_operating_system_purpose|운영체제]](Linux, Windows) 기술사들은 "차라리 [[022_kernel_role|커널]] 코드를 최적화해서 무거운 [[099_one_to_one_model|일대일]] 모델을 하드웨어 스펙으로 짓누르거나 [[103_thread_pool|스레드 풀]]([[103_thread_pool|Thread Pool]])로 제어하는 것이 낫다"고 판단하여 [[022_kernel_role|커널]] 레벨의 M:M 모델을 사실상 폐기했다.
2. **런타임 레벨에서의 화려한 부활**: 그러나 초당 수백만 개의 I/O를 처리해야 하는 [[531_cloud_native_architecture|클라우드 네이티브]] [[619_msa_traffic_hardware|MSA]] ([[122_msa_microservices_architecture|Microservices Architecture]]) 시대가 도래하며 [[099_one_to_one_model|일대일]] 모델은 다시 메모리 한계(C10K 문제)에 부딪혔다. 개발자들은 OS 대신 언어 런타임에 다대다 모델을 내장시켰다. Go 언어의 [[140_goroutine|고루틴]] ([[140_goroutine|Goroutine]])이나 Java 21의 가상 [[092_thread_lwp|스레드]] (Virtual [[092_thread_lwp|Thread]])가 그 주인공이다. [[140_goroutine|고루틴]] 10만 개를 만들어도 OS [[092_thread_lwp|스레드]]는 코어 수만큼만 [[087_process_state_transition|생성]]되어 동작하므로, 시스템 콜([[013_system_call|System Call]]) 병목 없이 압도적인 동시 처리가 가능하다.

- **📢 섹션 요약 비유**: 너무 복잡해서 자주 고장 나던 초정밀 기계식 시계(OS 레벨의 다대다)는 버려졌지만, 그 핵심 설계도(M:M 철학)는 최신 스마트워치의 소프트웨어 칩(Go 언어 런타임)으로 그대로 이식되어 세상을 지배하고 있다.

---

## Ⅴ. 기대효과 및 결론

다대다 모델은 [[022_kernel_role|커널]] 자원의 엄격한 제한 안에서 응용 프로그램에게 무한한 논리적 실행 흐름을 허락하는 궁극의 [[014_concurrency|동시성]] 패러다임이다. 

개발자는 콜백 지옥(Callback Hell) 같은 복잡한 비동기 코딩을 할 필요 없이 직관적인 동기식 코드를 작성하면서도, 뒷단에서는 [[079_kube_scheduler_pod_placement|스케줄러]]가 수만 개의 [[092_thread_lwp|스레드]]를 적은 수의 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]로 쪼개어 돌리는 마법을 누릴 수 있다. 이는 클라우드 환경에서 서버의 메모리 풋프린트를 극단적으로 줄여 인프라 비용을 절감하는 핵심 동력이 된다. 다대다 모델의 철학은 OS 밖으로 뛰쳐나와 현대 백엔드 아키텍처의 필수 표준 기술로 완전히 자리 잡았다.

- **📢 섹션 요약 비유**: 다대다 모델은 과거의 유물이 아니라, 수백만 대의 서버 위에서 거대한 클라우드 트래픽을 흔들림 없이 떠받치고 있는 보이지 않는 최첨단 서스펜션(완충 장치)이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **경량 프로세스 (LWP, Lightweight [[300_process|Process]])** | 사용자 [[092_thread_lwp|스레드]]와 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]] 사이의 인터페이스 역할을 하며, 스케줄링의 징검다리가 되는 자료 구조 |
| **[[079_kube_scheduler_pod_placement|스케줄러]] 촉발 ([[114_scheduler_activation|Scheduler Activation]])** | [[092_thread_lwp|스레드]]가 블로킹되었을 때, [[022_kernel_role|커널]]이 프로세스를 중단하지 않고 [[336_library_vs_framework|라이브러리]]에게 대체 자원(새 LWP)을 통지해 주는 [[022_kernel_role|커널]]-사용자 통신 규약 |
| **[[140_goroutine|고루틴]] ([[140_goroutine|Goroutine]])** | 다대다 모델의 철학을 OS 레벨에서 언어 런타임 레벨로 끌어올려 구현한 Go 언어의 초경량 [[092_thread_lwp|스레드]] |

### 📈 관련 키워드 및 발전 흐름도

```text
다대일 (Many-to-One) 모델 · 빠른 스위칭, 블로킹 마비
    │
    ▼
일대일 (One-to-One) 모델 · 병렬성 확보, 컨텍스트 스위칭 오버헤드
    │
    ▼
다대다 (Many-to-Many) 모델 · 스케줄러 촉발 (Scheduler Activation) 도입
    │
    ▼
OS 레벨 다대다 사장 · Linux NPTL(1:1) 표준화 및 스레드 풀(Thread Pool) 활용
    │
    ▼
런타임 레벨 다대다 부활 · Go 고루틴(Goroutine), Java 가상 스레드(Virtual Thread)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이공원(컴퓨터)에 1,000명의 아이들(사용자 [[092_thread_lwp|스레드]])이 롤러코스터를 타러 왔는데, 진짜 기차([[022_kernel_role|커널]] [[092_thread_lwp|스레드]])는 딱 10대밖에 없어요.
2. 옛날에는 기차 하나가 고장 나면 모든 아이가 하염없이 기다려야 했지만, 다대다 모델은 똑똑한 안내원이 있어서 아이들을 재빨리 멀쩡한 다른 기차로 갈아태워 준답니다!
3. 그래서 비싼 기차를 무작정 많이 만들지 않아도, 수많은 아이들이 끊기지 않고 재미있게 놀이공원을 계속 즐길 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 800

← **이전**: [[099_one_to_one_model|99. 일대일 (One-to-One) 스레드 모델]]
**다음**: [[101_two_level_model|101. 두 수준 (Two-level) 모델]] →

---
