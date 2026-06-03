---
title: 101. 두 수준 (Two-level) 모델
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 두 수준 (Two-level) 모델은 여러 사용자 [[092_thread_lwp|스레드]]를 소수의 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]에 연결하는 '[[100_many_to_many_model|다대다]](M:N)' 방식과 핵심 [[092_thread_lwp|스레드]]를 1:1로 고정하는 '[[099_one_to_one_model|일대일]]' 방식을 혼합한 하이브리드 스레딩 아키텍처다.
> 2. **가치**: LWP(Lightweight [[300_process|Process]])를 중간 계층으로 두어 [[092_thread_lwp|스레드]] [[087_process_state_transition|생성]] 비용과 [[022_kernel_role|커널]] 메모리 소모를 극소화하면서도, 실시간 응답이 필요한 [[092_thread_lwp|스레드]]는 블로킹([[122_sync_async_communication|Blocking]])에서 안전하게 [[571_protection_vs_security|보호]]한다.
> 3. **판단 포인트**: 과거 단일 코어 환경에서 대규모 I/O 동시성을 처리하는 데 필수적이었으나, 멀티코어 환경에서는 [[114_scheduler_activation|스케줄러 액티베이션]]([[114_scheduler_activation|Scheduler Activation]])의 복잡도 문제로 인해 현대 OS 대신 Go [[140_goroutine|고루틴]] 등 언어 런타임 모델로 철학이 전이되었다.

---

## Ⅰ. 개요 및 필요성

두 수준 (Two-level) 모델은 [[100_many_to_many_model|다대다]] ([[100_many_to_many_model|Many-to-Many]]) 스레딩 모델을 기반으로 하되, 특정 사용자 [[092_thread_lwp|스레드]](User [[092_thread_lwp|Thread]])에 한해 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]([[022_kernel_role|Kernel]] [[092_thread_lwp|Thread]])와 1:1로 독점 결합(Binding)할 수 있는 예외를 허용하는 구조다.

[[459_quic_fec_forward_error_correction|초기]] 운영체제에서는 [[022_kernel_role|커널]]이 [[092_thread_lwp|스레드]]의 존재를 모르는 [[098_many_to_one_model|다대일]](M:1) 모델을 썼으나, 하나의 [[092_thread_lwp|스레드]]가 I/O 작업으로 블로킹되면 프로세스 전체가 정지하는 문제가 있었다. 이를 극복하고자 모든 사용자 [[092_thread_lwp|스레드]]를 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]와 1:1로 매핑했으나, 이번에는 [[092_thread_lwp|스레드]] [[087_process_state_transition|생성]] 시의 [[211_context_switch|문맥 교환]]([[033_context|Context]] Switching) 오버헤드와 [[022_kernel_role|커널]] 메모리 고갈([[157_oom_killer|OOM]])이 시스템을 짓눌렀다. 
결국 자원 효율성을 위해 소수의 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]] 위에서 다수의 사용자 [[092_thread_lwp|스레드]]를 스케줄링하는 '[[100_many_to_many_model|다대다]](M:N)' 모델이 고안되었지만, 여전히 일부 [[092_thread_lwp|스레드]]의 블로킹이 묶여 있는 다른 [[092_thread_lwp|스레드]]들에 병목을 일으켰다. 이에 따라 자원을 절약하면서도 [[015_지연_데이터_관점|지연]]에 민감한 핵심 [[092_thread_lwp|스레드]]만큼은 단독으로 실행을 보장해 주기 위해 '두 수준 모델'이 등장했다.

- **📢 섹션 요약 비유**: 수많은 시민이 한정된 구급차를 호출([[100_many_to_many_model|다대다]] 매핑)해야 하지만, 시장이나 대통령 같은 특수 임무 수행자를 위해서는 언제든 출발 가능한 전용 방탄차(1:1 바인딩)를 별도로 배정해 두는 국가 비상 관리 체계와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

두 수준 모델은 사용자 영역과 [[022_kernel_role|커널]] 영역 사이에 **LWP (Lightweight [[300_process|Process]])** 라는 가상 프로세서 계층을 두어 동적 매핑과 정적 바인딩을 동시에 조율한다.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   두 수준 (Two-level) 모델 아키텍처 구조                   │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ [사용자 공간: User Space]                                                │
│  ┌─ 동적 할당 (Unbound Thread) ─┐     ┌─ 정적 할당 (Bound Thread) ─┐     │
│  │   U1      U2      U3      U4   │     │            U5            │     │
│  └───│───────│───────│───────│────┘     └────────────│─────────────┘     │
│      └───────┴───┬───┴───────┘                       │                   │
│ =================│===================================│================ │
│ [중간 계층: LWP Layer] ▼  다중화 (Multiplexing)           ▼ 독점 (Binding)  │
│                ┌───┐   ┌───┐                       ┌───┐                 │
│                │LWP│   │LWP│                       │LWP│                 │
│                └───┘   └───┘                       └───┘                 │
│                  │       │                           │                   │
│ =================│=======│===========================│================ │
│ [커널 공간: Kernel Space]  ▼                           ▼                   │
│                ┌───┐   ┌───┐                       ┌───┐                 │
│                │KT1│   │KT2│                       │KT3│                 │
│                └───┘   └───┘                       └───┘                 │
│                 (CPU 0 스케줄링)                     (CPU 1 스케줄링)         │
└────────────────────────────────────────────────────────────────────────┘
```

이 구조도의 핵심은 크게 두 가지 흐름이다. 첫째, U1~U4 (언바운드 [[092_thread_lwp|스레드]])는 가용한 LWP 위에서 [[336_library_vs_framework|라이브러리]] [[079_kube_scheduler_pod_placement|스케줄러]]에 의해 시분할 방식으로 동기화된다. 둘째, U5 (바운드 [[092_thread_lwp|스레드]])는 [[087_process_state_transition|생성]] 시점부터 고정된 LWP 및 KT3와 1:1로 직결된다. 
만약 U1이 I/O 시스템 호출을 통해 KT1을 블로킹시키면 [[022_kernel_role|커널]]은 **[[114_scheduler_activation|스케줄러 액티베이션]] ([[114_scheduler_activation|Scheduler Activation]])** 이라는 기법을 통해 '업콜([[115_upcall|Upcall]])' 신호를 사용자 공간에 보내 새로운 LWP를 임시로 내어준다. 사용자 [[079_kube_scheduler_pod_placement|스케줄러]]는 이를 받아 U2나 U3를 즉시 실행시킴으로써 병목을 극복한다. U5는 애초에 독립되어 있으므로 어떤 상황에서도 방해받지 않는다.

- **📢 섹션 요약 비유**: 콜센터에서 대부분의 일반 상담원은 무작위로 걸려 오는 전화를 받아 처리(언바운드)하지만, VIP 전담 상담원은 오직 한 명의 VIP 전화만 대기하다가 즉시 응대(바운드)하여 중요 고객의 불만을 완벽히 차단하는 운영 방식이다.

---

## Ⅲ. 비교 및 연결

스레딩 모델 3가지를 비교하면 두 수준 모델이 하드웨어 한계 상황에서 어떤 위치를 점하는지 알 수 있다.

| 비교 항목 | [[099_one_to_one_model|일대일]] (1:1) | [[100_many_to_many_model|다대다]] (M:N) | 두 수준 (Two-level) | 설계상 시사점 |
|:---|:---|:---|:---|:---|
| **매핑 방식** | 사용자 1 : [[022_kernel_role|커널]] 1 | 사용자 M : [[022_kernel_role|커널]] N (M ≥ N) | [[100_many_to_many_model|다대다]] (M:N) + [[099_one_to_one_model|일대일]] 혼용 | 유연성과 제어력의 극대화 |
| **[[022_kernel_role|커널]] 자원 소모** | 매우 큼 (TCB 폭증) | 적음 (LWP 수량만큼) | 적음 + 필요 시 제한적 허용 | 대규모 커넥션 유지 가능 |
| **블로킹 대응** | 해당 [[092_thread_lwp|스레드]]만 [[015_지연_데이터_관점|지연]] | LWP 고갈 시 다른 [[092_thread_lwp|스레드]]도 정지 | 중요 [[092_thread_lwp|스레드]]는 바인딩으로 격리 [[571_protection_vs_security|보호]] | I/O 중심 시스템 병목 해소 |
| **구현 복잡도** | 상대적으로 단순 | 매우 높음 | **가장 높음 (업콜 관리 복잡)** | 현대 OS에서 퇴출된 주된 이유 |

[[099_one_to_one_model|일대일]] 모델은 개발이 직관적이고 멀티코어의 [[282_performance_tactics|성능]]을 그대로 끌어내지만 1만 개의 [[092_thread_lwp|스레드]]를 열면 [[022_kernel_role|커널]]이 무너진다. 두 수준 모델은 1만 개의 [[369_logic_bomb|논리]] [[092_thread_lwp|스레드]]를 단 100개의 LWP로 묶어 [[022_kernel_role|커널]] 패닉을 방지한다. 하지만 사용자 [[092_thread_lwp|스레드]] [[336_library_vs_framework|라이브러리]]가 [[022_kernel_role|커널]] 상태를 끊임없이 모니터링해야 하는 [[114_scheduler_activation|스케줄러 액티베이션]] 메커니즘의 구현 복잡성이 극도로 높아 버그 발생과 유지보수의 어려움을 초래했다.

- **📢 섹션 요약 비유**: [[099_one_to_one_model|일대일]] 모델이 모든 승객을 개별 택시에 태워 고속도로 정체를 유발하는 것이라면, 두 수준 모델은 대형 [[344_bus|버스]](LWP)에 다수를 태우고 응급 환자만 앰뷸런스에 태우는 것이다. 단, [[344_bus|버스]] 배차 간격을 통제실([[022_kernel_role|커널]])과 실시간 무전으로 조율해야 해서 운영이 굉장히 까다롭다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현대 시스템에서 두 수준 모델의 아키텍처는 어떻게 응용되고 있는가?

### 실무 판단 시나리오 및 [[435_checklist_based_testing|체크리스트]]
1. **[[022_kernel_role|커널]] 자원 제약 환경하의 레거시 DB 운영**: Solaris 8 등 과거 유닉스 환경에서 수천 명의 클라이언트 접속([[160_session_controlling_terminal|Session]])을 유지해야 할 때 적용한다. 일반적인 [[298_qkv_attention|쿼리]] 요청 [[092_thread_lwp|스레드]]는 [[100_many_to_many_model|다대다]] 매핑으로 묶어 [[022_kernel_role|커널]] 메모리([[157_oom_killer|OOM]])를 방어하고, 백그라운드에서 동작하는 [[002_database_definition|데이터베이스]] [[568_logs_distributed_logging_elk_fluentd|로그]] 라이터(Log Writer) [[092_thread_lwp|스레드]]는 무조건 1:1 바운드 [[092_thread_lwp|스레드]]로 고정하여 다른 [[298_qkv_attention|쿼리]]가 [[015_지연_데이터_관점|지연]]되어도 [[001_dikw_pyramid|데이터]] 동기화가 밀리지 않도록 아키텍처를 분리해야 한다.
2. **현대 언어 런타임 아키텍처로의 개념 이식**: 현대 백엔드 개발 시 Go 언어의 [[140_goroutine|고루틴]]([[140_goroutine|Goroutine]])이나 Erlang의 그린 [[092_thread_lwp|스레드]]를 활용할 때 그 내부 원리가 두 수준 모델임을 이해해야 한다. 다수의 [[140_goroutine|고루틴]]이 소수의 OS [[092_thread_lwp|스레드]](M) 위에서 동작하다가 C 코드를 호출(CGO)하거나 동기 I/O를 만나 [[092_thread_lwp|스레드]]가 블로킹될 때, 런타임 내부의 [[079_kube_scheduler_pod_placement|스케줄러]]가 새로운 OS [[092_thread_lwp|스레드]]를 [[087_process_state_transition|생성]](Spawn)하여 작업을 인계하는 방식은 완벽히 두 수준 모델의 철학이다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 개발자가 시스템 [[282_performance_tactics|성능]]을 높이겠답시고 모든 사용자 [[092_thread_lwp|스레드]]를 일일이 바운드(Bound) [[092_thread_lwp|스레드]]로 명시적 강제 할당하는 경우. 이는 두 수준 모델을 쓰는 환경에서 [[099_one_to_one_model|일대일]] 모델로 억지 회귀하는 꼴이며, 사용자 [[079_kube_scheduler_pod_placement|스케줄러]]의 [[211_context_switch|문맥 교환]] 오버헤드만 가중시켜 전체 시스템의 [[139_throughput|처리량]]([[139_throughput|Throughput]])이 수직 추락하게 만든다.

- **📢 섹션 요약 비유**: 회사의 결재 라인을 단축하려고 모든 직원이 사장과 '1:1 직통 면담(바운드)'을 하도록 규칙을 바꾸면, 사장([[022_kernel_role|커널]])은 과부하로 쓰러지고 회사의 행정 스피드([[282_performance_tactics|성능]])가 완전히 마비되는 [[128_water_scrum_fall_anti_pattern|안티패턴]]과 같다.

---

## Ⅴ. 기대효과 및 결론

두 수준 (Two-level) 모델은 자원이 부족했던 과거에 수만 개의 [[092_thread_lwp|스레드]] 동시성을 감당해야 했던 엔지니어들의 치열한 타협안이었다. 사용자 [[092_thread_lwp|스레드]]의 경량성과 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]의 독립적 실행 보장성을 LWP라는 중간 다리를 통해 동시에 획득했으며, 시스템 전체의 메모리 한계를 완벽히 방어해 냈다.

비록 멀티코어 CPU의 대중화와 램(RAM)의 저렴화, 그리고 복잡한 [[114_scheduler_activation|스케줄러 액티베이션]] 관리에 지친 리눅스(Linux) 진영이 단순하고 강력한 [[099_one_to_one_model|일대일]](NPTL) 방식을 표준으로 채택하면서 OS 계층에서는 사실상 퇴장했다. 그러나 시스템 호출의 블로킹을 비동기적으로 우회하며 자원을 최적화한다는 철학은, 오늘날 Node.js의 [[142_event_loop|이벤트 루프]] 워커 풀 구조나 Go 언어의 런타임 [[079_kube_scheduler_pod_placement|스케줄러]] 메커니즘으로 완벽하게 계승되어 서버 아키텍처의 근간을 이루고 있다.

- **📢 섹션 요약 비유**: 과거의 수동 변속기(두 수준 모델)는 운전자가 클러치와 기어를 복잡하게 조작해야 했지만 연료 효율의 극강을 자랑했다. 현재는 자동 변속기([[099_one_to_one_model|일대일]] 모델)가 널리 쓰이지만, 그 정교한 동력 분배의 원리는 최신 하이브리드 자동차(현대 런타임 [[079_kube_scheduler_pod_placement|스케줄러]])의 두뇌 속에 여전히 살아있는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **LWP (Lightweight [[300_process|Process]])** | 사용자 [[092_thread_lwp|스레드]]와 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]를 매핑해주는 중간 가상 프로세서로, 두 수준 모델의 핵심 구조 |
| **[[114_scheduler_activation|스케줄러 액티베이션]] ([[114_scheduler_activation|Scheduler Activation]])** | [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]가 블로킹되었을 때, [[022_kernel_role|커널]]이 사용자 공간 [[336_library_vs_framework|라이브러리]]에 업콜([[115_upcall|Upcall]])을 보내어 다른 [[092_thread_lwp|스레드]]를 실행하게 하는 협업 통신 기법 |
| **[[100_many_to_many_model|다대다]] ([[100_many_to_many_model|Many-to-Many]]) 모델** | 두 수준 모델의 모태가 되는 아키텍처로, [[022_kernel_role|커널]] 메모리를 아끼지만 블로킹 전파 문제라는 약점을 가짐 |
| **그린 [[092_thread_lwp|스레드]] (Green [[092_thread_lwp|Thread]]) / [[140_goroutine|고루틴]] ([[140_goroutine|Goroutine]])** | OS가 아닌 런타임 수준에서 [[092_thread_lwp|스레드]]를 스케줄링하는 기법으로, 두 수준 모델의 철학을 계승한 현대적 구현체 |

### 📈 관련 키워드 및 발전 흐름도

```text
다대일 (Many-to-One) 모델
    │
    ▼
단일 스레드 블로킹 시 전체 프로세스 정지 한계
    │
    ▼
일대일 (One-to-One) 모델 등장 (자원 폭증 문제 발생)
    │
    ▼
다대다 (Many-to-Many) 모델 고안 (자원 최적화)
    │
    ▼
두 수준 (Two-level) 모델 진화 (특정 스레드의 1:1 결합 지원)
    │
    ▼
현대 언어 런타임 (Goroutine, Erlang)의 스케줄링 철학으로 계승
```

### 👶 어린이를 위한 3줄 비유 설명
1. 놀이공원(컴퓨터)에 손님([[092_thread_lwp|스레드]])은 100명인데 타야 할 범퍼카([[022_kernel_role|커널]] [[092_thread_lwp|스레드]])는 10대밖에 없어요.
2. 대부분의 손님은 줄을 서서 범퍼카를 교대로 돌려타야([[100_many_to_many_model|다대다]] 모델) 놀이공원이 복잡해지지 않아요.
3. 하지만 시장님처럼 급한 손님을 위해서는 절대 남과 섞이지 않는 전용 범퍼카([[099_one_to_one_model|일대일]] 고정)를 따로 빼놓는 똑똑한 시스템이 바로 '두 수준 모델'이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 101 / 800

← **이전**: [[100_many_to_many_model|100. 다대다 (Many-to-Many) 스레드 모델]]
**다음**: [[102_implicit_threading|102. 암묵적 스레딩 (Implicit Threading) - 스레드 풀, OpenMP, Grand Central Dispatch(GCD)]] →

---
