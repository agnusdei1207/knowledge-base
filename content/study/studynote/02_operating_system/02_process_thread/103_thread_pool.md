---
title: 103. 스레드 풀 (Thread Pool)
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[092_thread_lwp|스레드]] 풀 ([[092_thread_lwp|Thread]] Pool)은 일정한 수의 워커 [[092_thread_lwp|스레드]] (Worker [[092_thread_lwp|Thread]])를 미리 생성하여 큐([[058_queue|Queue]])에 대기 중인 작업을 순차적으로 꺼내 실행하게 하는 [[014_concurrency|동시성]] 자원 관리 패턴이다.
> 2. **가치**: [[092_thread_lwp|스레드]]의 빈번한 생성과 소멸로 인한 [[022_kernel_role|커널]] 모드 전환 오버헤드와 메모리 파편화를 제거하여, 트래픽 폭증 시에도 예측 가능한 시스템 응답 속도를 보장한다.
> 3. **판단 포인트**: 풀의 크기(Size)를 무한정 늘리면 [[211_context_switch|문맥 교환]]([[033_context|Context]] Switching) [[257_thrashing|스래싱]]으로 서버가 붕괴하므로, 워크로드(CPU 바운드 vs I/O 바운드)에 맞춰 적정 크기를 산정하고 거절 [[164_policy|정책]](Rejection [[164_policy|Policy]])을 반드시 [[009_config|설정]]해야 한다.

---

## Ⅰ. 개요 및 필요성

[[092_thread_lwp|스레드]] 풀 ([[092_thread_lwp|Thread]] Pool)은 다수의 클라이언트 요청을 병렬로 처리하기 위해, 작업([[150_task|Task]])을 실행할 [[092_thread_lwp|스레드]] 집합을 메모리 상에 미리 스폰(Spawn)해 두고 재사용하는 소프트웨어 디자인 패턴이다.

"요청당 [[092_thread_lwp|스레드]] ([[092_thread_lwp|Thread]]-per-request)" 방식에서는 클라이언트가 접속할 때마다 [[001_operating_system_purpose|운영체제]]가 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]를 새로 만들고 끝나면 폐기해야 했다. 이 방식은 트래픽 폭증(Traffic [[129_spike_agile_technical_investigation|Spike]]) 시 수만 개의 [[092_thread_lwp|스레드]]가 동시 생성되며 [[022_kernel_role|커널]] 메모리를 고갈시키고([[157_oom_killer|OOM]]), CPU (Central Processing Unit)가 비즈니스 로직 대신 [[211_context_switch|문맥 교환]]([[033_context|Context]] Switching)에만 리소스를 낭비하는 [[257_thrashing|스래싱]]([[257_thrashing|Thrashing]]) 상태를 유발한다. 시스템 다운을 방어하고 안정적인 [[139_throughput|처리량]]([[139_throughput|Throughput]])을 유지하기 위해서는, [[092_thread_lwp|스레드]] 재사용과 동시 실행 한계치([[341_process|Cap]]) [[009_config|설정]] 메커니즘이 절대적으로 필요해졌다.

- **📢 섹션 요약 비유**: [[092_thread_lwp|스레드]] 풀은 대형 마트의 **'상주 계산대 직원'**과 같다. 손님이 올 때마다 직원을 집에서 새로 출근시키고 바로 퇴근시키면 길에서 버리는 시간이 더 많지만, 미리 정해진 5명의 직원이 계산대에 상주(풀)하며 대기줄(큐)의 손님을 처리하면 효율이 극대화된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[092_thread_lwp|스레드]] 풀은 작업과 실행 주체를 철저히 분리한 생산자-소비자 패턴 (Producer-Consumer Pattern)으로 동작한다.

```text
┌───────────────────────────────────────────────────────────────────────────┐
│              Thread Pool Asynchronous Architecture                        │
├───────────────────────────────────────────────────────────────────────────┤
│ [ Client / Main Thread (Producer) ]                                       │
│       작업(Task) 요청 제출 (submit)                                            │
│            │                                                              │
│            ▼                                                              │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │                    Thread Pool Manager (Executor)                     │ │
│ │                                                                       │ │
│ │  ┌─────────────────────────┐         ┌─────────────────────────────┐  │ │
│ │  │  Task Queue (Blocking)  │         │   Worker Threads (Pool)     │  │ │
│ │  │                         │         │                             │  │ │
│ │  │ [ Task3 ][ Task2 ]      │ ◀──take │  [ Thread 1 (Idle)    ]     │  │ │
│ │  │                         │         │  [ Thread 2 (Running) ]     │  │ │
│ │  └─────────────────────────┘         │  [ Thread 3 (Running) ]     │  │ │
│ │                                      └─────────────────────────────┘  │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│ * 핵심 동작: 스레드는 무한 루프를 돌며 큐에서 작업을 꺼냄. 큐가 비면 Sleep(블로킹).│
└───────────────────────────────────────────────────────────────────────────┘
```

[[092_thread_lwp|스레드]] 풀 관리자는 다음과 같은 핵심 생명주기 파라미터를 통해 탄력적으로 동작한다:
1. **작업 큐 ([[150_task|Task]] [[058_queue|Queue]])**: 들어온 작업을 보관하는 [[147_thread_safe|스레드 안전]]([[147_thread_safe|Thread-safe]])한 블로킹 큐([[122_sync_async_communication|Blocking]] [[058_queue|Queue]]).
2. **코어 [[092_thread_lwp|스레드]] 수 (Core Pool Size)**: 트래픽이 없어도 기본적으로 유지하는 최소 [[092_thread_lwp|스레드]] 개수.
3. **최대 [[092_thread_lwp|스레드]] 수 (Maximum Pool Size)**: 큐가 가득 찼을 때 임시로 늘릴 수 있는 최대 [[092_thread_lwp|스레드]] 한도.
4. **유휴 대기 시간 (Keep-Alive Time)**: 임시로 늘어난 [[092_thread_lwp|스레드]]가 작업을 끝내고 대기할 때, 이 시간이 지나면 스스로 종료하여 메모리를 반환한다.

- **📢 섹션 요약 비유**: 식당에 평소(Core Size)에는 홀 직원 3명을 유지하다가, 대기명단([[058_queue|Queue]])마저 꽉 차면 임시 알바(Max Size)를 급히 부르고, 바쁜 시간이 지나면(Keep-alive time) 알바를 퇴근시켜 인건비를 아끼는 스마트 매장 관리 시스템이다.

---

## Ⅲ. 비교 및 연결

[[092_thread_lwp|스레드]] 풀을 설계할 때는 워크로드의 특성에 따라 최적의 크기가 극단적으로 갈라지는 정량적 차이를 이해해야 한다.

| 워크로드 특성 | 병목 지점 | 적정 [[092_thread_lwp|스레드]] 수 공식 | 설명 및 근거 |
|:---|:---|:---|:---|
| **CPU 바운드** | 프로세서 연산 능력 | `CPU 코어 수 + 1` | 암호화나 [[347_compaction|압축]] 등 연산 위주 작업. [[092_thread_lwp|스레드]]가 많아지면 [[034_context_switch|컨텍스트 스위칭]] 오버헤드만 급증함. `+1`은 [[720_page_fault_isr|페이지 폴트]] 대비용. |
| **I/O 바운드** | 디스크/[[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] | `CPU 코어 수 * (1 + 대기/계산 시간 비율)` | DB 쿼리나 [[014_api_posix|API]] 호출 대기 시 CPU가 쉬게 되므로, 이를 메꾸기 위해 수십~수백 개의 [[092_thread_lwp|스레드]]가 투입되어야 함. |

아키텍처 관점에서, 단일 [[092_thread_lwp|스레드]] 풀로 모든 트래픽을 처리하는 방식과 장애 격리를 위해 타겟 도메인별로 [[092_thread_lwp|스레드]] 풀을 나누는 **[[308_bulkhead_pattern|벌크헤드]] 패턴([[308_bulkhead_pattern|Bulkhead Pattern]])** 간의 비교도 중요하다. [[308_bulkhead_pattern|벌크헤드]] 패턴은 한 서비스의 응답 [[015_지연_데이터_관점|지연]]이 [[092_thread_lwp|스레드]] 풀 전체를 고갈시켜 시스템을 연쇄 붕괴시키는 것을 방지한다.

- **📢 섹션 요약 비유**: 고속도로의 차선(CPU 코어)이 4개인데 진입 차량([[092_thread_lwp|스레드]])을 무한정 늘리면, [[211_context_switch|문맥 교환]]이라는 심각한 교통체증이 발생해 주차장이 되어버린다. 작업 특성에 맞춰 최적의 차량 대수만 통과시켜야 진짜 [[282_performance_tactics|성능]]이 나온다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 운영에서 [[092_thread_lwp|스레드]] 풀의 큐 적체([[058_queue|Queue]] Accumulation) 상황 발생 시 적용해야 하는 거절 [[164_policy|정책]](Rejection [[164_policy|Policy]]) 판단이 매우 중요하다. 무제한 큐(Unbounded [[058_queue|Queue]])를 사용할 경우, 트래픽 폭주 시 JVM [[078_heap_datastructure|Heap]] 메모리 OOM으로 서버가 비정상 종료된다. 반드시 크기가 제한된 Bounded Queue를 써야 한다.

### [[435_checklist_based_testing|체크리스트]] 및 거절 [[164_policy|정책]](Rejection [[164_policy|Policy]]) 판단
1. **Abort [[164_policy|Policy]] (기본값)**: 큐가 가득 차면 에러 예외(Exception)를 즉시 발생시킨다. 클라이언트에게 거절을 명확히 알릴 때 쓴다.
2. **Caller Runs [[164_policy|Policy]]**: 작업을 요청한 메인 [[092_thread_lwp|스레드]]가 직접 작업을 실행하도록 강제한다. 생산자(호출자)의 속도를 물리적으로 [[015_지연_데이터_관점|지연]]시켜 백프레셔(Back-pressure) 효과를 낸다. 유실되면 안 되는 중요한 비즈니스 로직에 필수적이다.
3. **Discard [[164_policy|Policy]]**: 조용히 새 작업을 무시한다. 통계 핑이나 [[568_logs_distributed_logging_elk_fluentd|로그]] 전송처럼 최신 정보가 아니면 버려도 되는 비핵심 로직에 사용한다.
4. **Discard Oldest [[164_policy|Policy]]**: 큐의 맨 앞(가장 오래된) 작업을 버리고 새 작업을 넣는다. 실시간 센서 [[001_dikw_pyramid|데이터]] 갱신에 유용하다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **ThreadLocal 변수 누수 (Leak)**: `ThreadLocal`에 [[604_authentication_factors|사용자 인증]] 정보 등을 저장한 후, 로직 종료 시 명시적으로 `remove()` 하지 않는 행위. 워커 [[092_thread_lwp|스레드]]는 소멸되지 않고 풀로 돌아가 재사용되므로, 다음 요청을 처리할 때 이전 사용자의 권한이 그대로 남아 치명적인 보안 사고(권한 탈취)로 이어진다.

- **📢 섹션 요약 비유**: [[092_thread_lwp|스레드]] 풀 포화 시의 거절 [[164_policy|정책]]은 만원 지하철에서 더 이상 사람을 밀어 넣지 않고(무제한 큐 방지), 출입문을 닫거나 다음 열차를 타게 안내하여 전체 시스템의 붕괴를 막는 관제실의 비상 버튼과 같습니다.

---

## Ⅴ. 기대효과 및 결론

적절히 튜닝된 [[092_thread_lwp|스레드]] 풀은 초당 수천 번의 [[022_kernel_role|커널]] 전환 오버헤드를 99% 제거하며, 트래픽 폭풍 속에서도 [[257_thrashing|스래싱]] 없는 예측 가능한 레이턴시([[141_latency|Latency]])와 0%의 서버 다운타임을 보장한다. 시스템 자원이 유한하다는 물리적 한계를 가장 우아하게 소프트웨어적으로 통제한 걸작이다.

미래 방향성은 단순한 [[092_thread_lwp|스레드]] 풀을 넘어, I/O 바운드 환경에서의 메모리 낭비를 막기 위해 Nginx나 Node.js 같은 [[142_event_loop|이벤트 루프]] ([[142_event_loop|Event Loop]]) 아키텍처나 Java 21의 가상 [[092_thread_lwp|스레드]] (Virtual Threads)로 진화하고 있다. 수백만 개의 초경량 워크로드를 저비용으로 스케줄링할 수 있게 되면서 전통적 [[092_thread_lwp|스레드]] 풀의 역할은 축소될 수 있지만, [[014_concurrency|동시성]]을 제어하고 시스템 한계를 관리한다는 근본 철학은 변하지 않는다.

- **📢 섹션 요약 비유**: 엔진 피스톤([[092_thread_lwp|스레드]])이 연료(작업)를 터트릴 때, 튼튼한 엔진 블록([[092_thread_lwp|스레드]] 풀 제한)으로 폭발력을 제어하지 않으면 엔진이 터져버립니다. [[092_thread_lwp|스레드]] 풀은 한계 속에서 최대 [[282_performance_tactics|성능]]을 끌어내는 제어 공학의 기초 뼈대입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[211_context_switch|문맥 교환]] ([[033_context|Context]] Switching)** | [[092_thread_lwp|스레드]] 풀 크기를 통제하지 않을 경우 발생하는 가장 치명적인 CPU [[282_performance_tactics|성능]] 저하 원인 |
| **[[308_bulkhead_pattern|벌크헤드]] 패턴 ([[308_bulkhead_pattern|Bulkhead Pattern]])** | [[619_msa_traffic_hardware|MSA]] 환경에서 타겟 도메인별로 [[092_thread_lwp|스레드]] 풀을 분리하여 장애 전파를 차단하는 아키텍처 |
| **가상 [[092_thread_lwp|스레드]] (Virtual [[092_thread_lwp|Thread]])** | [[001_operating_system_purpose|운영체제]] [[092_thread_lwp|스레드]]와 [[099_one_to_one_model|일대일]] 매핑되는 비용을 우회하기 위해 런타임이 유저 레벨에서 수백만 개를 관리하는 차세대 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
요청당 스레드 생성 (Thread-per-request)
    │ (문맥 교환 폭증, OOM 발생)
    ▼
스레드 풀 (Thread Pool) 패턴 도입
    │ 작업 대기 큐(Task Queue) + 한계 설정(Cap)
    ▼
벌크헤드 패턴 (Bulkhead) 및 서킷 브레이커
    │ 도메인별 풀 분리로 장애 격리
    ▼
이벤트 루프 (Event Loop) 기반 논블로킹 I/O
    │
    ▼
경량 사용자 스레드 (Virtual Threads / Goroutines)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 택배 회사가 물건(작업)이 들어올 때마다 트럭([[092_thread_lwp|스레드]])을 새로 사서 배달을 보내면 비용이 너무 들어서 회사가 망해버려요.
2. 그래서 회사에 10대의 트럭만 미리 사두고, 물건 배달을 마친 트럭이 돌아오면 곧바로 다음 물건을 싣고 또 출발하게 만들었는데 이게 '[[092_thread_lwp|스레드]] 풀'이에요!
3. 물건이 갑자기 너무 많이 오면 창고(작업 큐)에 잠깐 쌓아두고, 제한된 트럭 10대가 부지런히 돌면서 배달하니까 고장 없이 튼튼하게 일을 끝낼 수 있답니다.
