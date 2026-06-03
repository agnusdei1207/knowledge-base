---
title: 97. 커널 수준 스레드 (Kernel-level Thread) - OS가 직접 관리
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[022_kernel_role|커널]] 수준 [[092_thread_lwp|스레드]] (Kernel-level [[092_thread_lwp|Thread]], KLT)는 [[001_operating_system_purpose|운영체제]] [[022_kernel_role|커널]]이 직접 [[087_process_state_transition|생성]], 스케줄링, 소멸을 관리하며 TCB ([[092_thread_lwp|Thread]] Control Block)를 [[022_kernel_role|커널]] 공간에 유지하는 실행 단위이다.
> 2. **가치**: 특정 [[092_thread_lwp|스레드]]가 I/O 블로킹 상태에 빠져도 [[022_kernel_role|커널]]이 이를 개별적으로 인지하므로, 프로세스 내 다른 [[092_thread_lwp|스레드]]를 다른 CPU 코어에 할당해 중단 없는 [[014_concurrency|동시성]]과 [[430_index_fast_full_scan|병렬]] 연산을 보장한다.
> 3. **판단 포인트**: KLT는 안정성과 멀티코어 활용 능력이 뛰어나지만, [[211_context_switch|문맥 교환]]([[211_context_switch|Context Switch]]) 시 [[022_kernel_role|커널]] 개입에 따른 [[282_performance_tactics|성능]] 오버헤드가 발생하므로 [[103_thread_pool|스레드 풀]]([[103_thread_pool|Thread Pool]]) 크기를 물리 코어에 맞춰 제한해야 한다.

---

## Ⅰ. 개요 및 필요성

[[022_kernel_role|커널]] 수준 [[092_thread_lwp|스레드]] (KLT, Kernel-Level [[092_thread_lwp|Thread]])는 OS [[022_kernel_role|커널]]이 [[092_thread_lwp|스레드]]의 존재를 직접 인식하고 1:1 매핑 기반으로 관리하는 [[014_concurrency|동시성]] 모델이다. 사용자가 애플리케이션에서 [[092_thread_lwp|스레드]]를 [[087_process_state_transition|생성]]하면, [[001_operating_system_purpose|운영체제]] 내부적으로도 이에 대응하는 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]] 객체가 만들어진다.

이 구조는 [[459_quic_fec_forward_error_correction|초기]] [[096_user_level_thread|사용자 수준 스레드]](ULT)의 치명적 결함을 해결하기 위해 등장했다. ULT 환경에서는 하나의 [[092_thread_lwp|스레드]]가 디스크 읽기 등으로 블로킹(Block)되면, [[022_kernel_role|커널]]은 프로세스 전체가 멈춘 것으로 오인해 나머지 [[092_thread_lwp|스레드]]까지 전부 중단시켰다. 게다가 코어가 여러 개인 다중 처리기([[195_real_time_scheduling|SMP]]) 환경에서도 [[022_kernel_role|커널]]이 [[092_thread_lwp|스레드]]를 구별하지 못해 여러 코어에 연산을 [[136_variance|분산]]할 수 없었다. 이 병목을 타개하고 하드웨어 자원을 극한으로 활용하기 위해 [[022_kernel_role|커널]]이 [[092_thread_lwp|스레드]]를 직접 통제하는 아키텍처가 필요해졌다.

- **📢 섹션 요약 비유**: 회사(프로세스)의 모든 직원([[092_thread_lwp|스레드]])이 국가([[022_kernel_role|커널]])에 직접 정규직으로 등록된 상태다. 한 직원이 병가를 내더라도, 국가가 다른 직원들은 정상 출근시켜 회사가 계속 굴러가도록 보장해 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[022_kernel_role|커널]] 수준 [[092_thread_lwp|스레드]] 모델은 [[022_kernel_role|커널]] 공간 내부에 [[092_thread_lwp|스레드]] 상태를 저장하는 TCB 구조를 개별적으로 유지한다. 사용자 [[092_thread_lwp|스레드]] 하나당 [[022_kernel_role|커널]] [[092_thread_lwp|스레드]] 하나가 바인딩되는 [[099_one_to_one_model|일대일]](1:1) 구조가 현대 OS의 표준이다.

| 구성 요소 | 역할 | 실무 메커니즘 |
| :--- | :--- | :--- |
| **TCB ([[092_thread_lwp|Thread]] Control Block)** | 상태 저장 | [[022_kernel_role|커널]] 메모리 안에 [[164_pc|PC]], [[057_register|레지스터]], [[057_stack|스택]] 정보 보관 (메모리 소모) |
| **[[013_system_call|System Call]] [[014_api_posix|API]]** | [[087_process_state_transition|생성]] 및 통제 | [[092_thread_lwp|스레드]] 관리를 위해 유저 모드에서 [[022_kernel_role|커널]] 모드로 진입 (Overhead) |
| **OS [[079_kube_scheduler_pod_placement|스케줄러]]** | CPU 자원 분배 | [[022_kernel_role|커널]]이 큐를 검사하여 각 [[092_thread_lwp|스레드]]에 물리적 코어 독립 할당 |

[[022_kernel_role|커널]] [[092_thread_lwp|스레드]]의 1:1 매핑 구조와 블로킹 격리 원리를 시각화한다.

```text
┌──────────────────────────────────────────────────────────────┐
│           커널 수준 스레드 (KLT) 1:1 매핑 모델 아키텍처           │
├──────────────────────────────────────────────────────────────┤
│  [ 사용자 영역 (User Space) ]                                │
│  ┌──────────────────────────────────────────────────┐        │
│  │ 프로세스                                          │        │
│  │  [ ULT 1 ]          [ ULT 2 ]          [ ULT 3 ] │        │
│  └───│──────────────────│──────────────────│────────┘        │
│ ─────┼──────────────────┼──────────────────┼─ Mode Boundary ─│
│      ▼ 1:1              ▼ 1:1              ▼ 1:1           │
│  [ 커널 영역 (Kernel Space) ]                                │
│     [ KLT 1 ]          [ KLT 2 ]          [ KLT 3 ]          │
│       │ 블로킹 발생!        │                  │               │
│       ▼                   ▼                  ▼               │
│     (Wait 큐 이동)     [ 코어 1 할당 ]    [ 코어 2 할당 ]         │
│                                                              │
│ * 핵심: KLT 1이 멈춰도 커널 스케줄러가 KLT 2, 3을 타 코어에서 실행시킴 │
└──────────────────────────────────────────────────────────────┘
```

이 다이어그램은 KLT 모델에서 블로킹 장애가 어떻게 격리되는지를 보여준다. 유저 [[092_thread_lwp|스레드]]가 시스템 콜을 호출하여 대기 상태에 빠지면, [[022_kernel_role|커널]]은 해당 KLT의 상태만 'Wait'로 변경하고 동일 프로세스에 속한 다른 KLT들은 다른 물리 코어에서 작업을 멈추지 않고 지속하게 만든다.

- **📢 섹션 요약 비유**: 고속도로 요금소에서 [[344_bus|버스]](프로세스) 안 승객 수를 모르고 한 번에 통과시키던 방식에서, 승객 한 명 한 명([[092_thread_lwp|스레드]])에게 단말기를 줘서 각자 빈 차선(코어)으로 쌩쌩 달리게 해주는 [[136_variance|분산]] 처리 시스템이다.

---

## Ⅲ. 비교 및 연결

[[092_thread_lwp|스레드]] 아키텍처는 [[022_kernel_role|커널]]의 개입 수준에 따라 [[282_performance_tactics|성능]]과 안정성이 극명하게 갈린다. KLT는 ULT에 비해 [[211_context_switch|문맥 교환]]([[033_context|Context]] Switching) 오버헤드가 크다는 뚜렷한 약점이 있다.

| 비교 축 | [[022_kernel_role|커널]] 수준 [[092_thread_lwp|스레드]] (KLT) | [[096_user_level_thread|사용자 수준 스레드]] (ULT) | 설계적 차이점 |
| :--- | :--- | :--- | :--- |
| **관리 주체** | OS [[022_kernel_role|커널]] [[079_kube_scheduler_pod_placement|스케줄러]] | 유저 레벨 [[336_library_vs_framework|라이브러리]] | [[022_kernel_role|커널]]의 인지 유무 |
| **[[014_concurrency|동시성]] 방어** | 하나의 [[422_thread_block_and_warp|스레드 블록]] 시 타 [[092_thread_lwp|스레드]] 정상 실행 | 블록 시 **프로세스 전체 마비** | [[430_index_fast_full_scan|병렬]]성 보장의 핵심 기준 |
| **모드 전환** | [[211_context_switch|문맥 교환]] 시 유저 ↔ [[022_kernel_role|커널]] 횡단 (느림) | [[022_kernel_role|커널]] 진입 없음 (매우 빠름) | [[282_performance_tactics|성능]] 병목 지점의 차이 |
| **멀티코어 활용** | [[092_thread_lwp|스레드]]를 각 코어에 [[136_variance|분산]] 가능 ([[195_real_time_scheduling|SMP]]) | 단일 코어에서만 시분할 | 하드웨어 자원 활용 능력 |

KLT [[211_context_switch|문맥 교환]]이 느린 이유는 주소 공간([[381_virtual_memory|가상 메모리]]) 변경은 없지만, 유저 모드에서 [[022_kernel_role|커널]] 모드로 진입하기 위해 [[057_register|레지스터]] 백업과 [[079_kube_scheduler_pod_placement|스케줄러]] [[001_algorithm_definition|알고리즘]] 실행이라는 특권 계층 이동(Mode Boundary) 비용이 발생하기 때문이다. 

- **📢 섹션 요약 비유**: 방 안에서 옷을 편하게 갈아입는 것(ULT)과, 굳이 경비원이 있는 현관문 밖 복도로 나가서 옷을 갈아입고 다시 방으로 들어오는 것(KLT)의 절차적 낭비 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대부분의 현대 언어(Java Native [[092_thread_lwp|Thread]] 등)와 OS는 KLT를 기본으로 사용한다. 실무 엔지니어는 KLT의 '무거움'을 통제하는 아키텍처적 결정을 내려야 한다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]
1. **[[103_thread_pool|스레드 풀]] ([[103_thread_pool|Thread Pool]]) 튜닝**: 서버에 들어오는 요청 1개당 [[092_thread_lwp|스레드]](`new Thread()`)를 무한정 [[087_process_state_transition|생성]]하는가? KLT는 하나 [[087_process_state_transition|생성]]할 때마다 [[022_kernel_role|커널]] TCB와 수 MB의 유저 [[057_stack|스택]] 메모리를 점유한다. 트래픽 폭증 시 [[157_oom_killer|OOM]]([[157_oom_killer|Out of Memory]])이나 [[022_kernel_role|커널]] [[257_thrashing|스래싱]]([[257_thrashing|Thrashing]])이 발생하므로 반드시 하드웨어 코어 수의 N배 수준으로 [[103_thread_pool|스레드 풀]] 크기를 고정해야 한다.
2. **비동기 [[142_event_loop|이벤트 루프]] 전환**: 클라이언트 1만 명이 접속하는 C10K 환경에서는 KLT 1만 개를 유지할 수 없다. 커넥션 [[092_thread_lwp|스레드]]를 무작정 늘리는 대신 Netty나 NGINX 같은 비동기 I/O([[142_event_loop|Event Loop]]) 기반 멀티플렉싱 아키텍처로 넘어가 KLT 개입을 최소화했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 단일 프로세스 내에서 KLT를 물리 코어 개수보다 수천 배 더 많이 띄우는 행위. 실제 연산 처리 시간보다 KLT 간 교대([[211_context_switch|Context Switch]])를 위한 [[022_kernel_role|커널]] 스케줄링 시간이 더 길어져 시스템 전체 TPS가 바닥으로 곤두박질친다.

- **📢 섹션 요약 비유**: 튼튼한 장갑차(KLT)는 포탄을 맞아도 병사를 보호하지만 기름을 너무 많이 먹는다. 1만 명의 병사를 옮기겠다고 장갑차 1만 대를 굴리면 부대의 연료가 순식간에 고갈되므로, 장갑차 수는 제한하고 효율적으로 돌려 써야 한다.

---

## Ⅴ. 기대효과 및 결론

[[022_kernel_role|커널]] 수준 [[092_thread_lwp|스레드]]는 블로킹 연산의 공포에서 소프트웨어를 해방시키고, 멀티코어 하드웨어의 힘을 100% 이끌어내는 가장 안정적인 [[014_concurrency|동시성]] 표준 모델이다. 개발자가 [[079_kube_scheduler_pod_placement|스케줄러]]를 직접 구현하지 않아도 OS의 강력한 자원 관리 혜택을 온전히 누릴 수 있다.

하지만 KLT의 [[211_context_switch|문맥 교환]] 비용이 한계에 도달하면서, 미래의 트렌드는 최소한의 KLT(코어 수만큼) 위에서 수십만 개의 초경량 유저 [[092_thread_lwp|스레드]]([[141_coroutine|코루틴]], Virtual [[092_thread_lwp|Thread]])를 얹어 돌리는 하이브리드 [[100_many_to_many_model|다대다]](M:N) 매핑 방식으로 진화하고 있다. 즉 KLT는 가장 무겁지만 결코 무너지지 않는 시스템 [[014_concurrency|동시성]]의 최후 방어선으로 남게 될 것이다.

- **📢 섹션 요약 비유**: [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]는 고층 빌딩의 튼튼한 철골 뼈대와 같다. 그 자체는 무겁고 설치하기 힘들지만, 그 위에서 가벼운 칸막이(가상 [[092_thread_lwp|스레드]])들을 마음껏 나누고 부수며 놀 수 있는 안전한 지반을 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[096_user_level_thread|사용자 수준 스레드]] (ULT)** | KLT의 [[022_kernel_role|커널]] 개입 비용을 없앤 극단적 가벼움의 [[092_thread_lwp|스레드]], 하지만 차단(Block)에 취약함 |
| **[[211_context_switch|문맥 교환]] ([[033_context|Context]] Switching)** | KLT가 CPU 제어권을 바꿀 때 특권 계층을 오가며 발생하는 주요 [[282_performance_tactics|성능]] [[015_지연_데이터_관점|지연]] 원인 |
| **[[195_real_time_scheduling|SMP]] ([[382_smp|대칭형 다중 처리]])** | [[022_kernel_role|커널]] [[079_kube_scheduler_pod_placement|스케줄러]]가 여러 코어를 인지하고 KLT를 동등하게 흩뿌려주는 하드웨어 [[430_index_fast_full_scan|병렬]] 구조 |
| **가상 [[092_thread_lwp|스레드]] (Virtual [[092_thread_lwp|Thread]])** | KLT의 무거움을 극복하기 위해 KLT 위에서 여러 개의 흐름을 쪼개 쓰는 최신 런타임 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
프로세스 시분할 (단일 실행 흐름)
    │
    ▼
사용자 수준 스레드 (가벼움, 블로킹 취약)
    │
    ▼
커널 수준 스레드 (1:1 매핑, 블로킹 면역, 무거움)
    │
    ▼
다대다 (M:N) 매핑 / 하이브리드 모델
    │
    ▼
코루틴 및 가상 스레드 (Virtual Thread) 런타임 결합
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[022_kernel_role|커널]] [[092_thread_lwp|스레드]]는 놀이공원(컴퓨터) 본부에서 이름과 업무를 직접 관리해 주는 정식 직원들이에요.
2. 한 직원이 다쳐서 일을 못하게 돼도(블로킹), 본부가 바로 알아채고 다른 직원들에게 일을 나눠줘서 놀이기구는 절대 멈추지 않아요.
3. 하지만 직원들이 교대할 때마다 매번 본부에 찾아가서 서류 도장을 받아야 해서(모드 전환), 준비 시간이 조금 오래 걸린다는 단점이 있어요.
