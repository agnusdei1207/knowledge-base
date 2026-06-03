+++
weight = 168
title = "168. 디스패처 (Dispatcher) - 문맥 교환 수행 모듈"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디스패처 (Dispatcher)는 [[161_short_term_scheduler|단기 스케줄러]] ([[161_short_term_scheduler|Short-term Scheduler]])가 고른 프로세스나 [[092_thread_lwp|스레드]]에 실제 CPU 제어권을 넘기는 실행 메커니즘이며, [[211_context_switch|문맥 교환]] ([[211_context_switch|Context Switch]])의 현장 집행자다.
> 2. **가치**: [[057_register|레지스터]] 저장·복원, 주소 공간 전환, 사용자 모드 복귀를 책임지므로, 이 [[192_module_independence|모듈]]의 효율은 응답성·실시간성·[[675_multitasking_terminology_preemptive|멀티태스킹]] 체감 [[282_performance_tactics|성능]]에 직접 연결된다.
> 3. **판단 포인트**: 스케줄링 [[164_policy|정책]]이 좋아도 디스패처 오버헤드가 크면 전체 시스템은 느려진다. 특히 프로세스 전환, 메모리 관리 장치 ([[284_mmu|Memory Management Unit]], [[328_mmu|MMU]]) 변경, 변환 색인 버퍼 ([[291_tlb|Translation Lookaside Buffer]], [[357_tlb|TLB]]) 영향까지 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

디스패처는 [[001_operating_system_purpose|운영체제]]가 "다음에 누가 CPU를 쓸지"를 결정한 뒤, 그 결정을 실제 실행으로 옮기는 [[022_kernel_role|커널]] 구성 요소다. [[161_short_term_scheduler|단기 스케줄러]]가 [[088_ready_queue|준비 큐]] ([[088_ready_queue|Ready Queue]])에서 다음 실행 대상을 선택하면, 디스패처는 현재 실행 중인 작업의 문맥을 저장하고 새 작업의 문맥을 복원한 뒤 사용자 모드로 복귀시킨다. 즉 [[079_kube_scheduler_pod_placement|스케줄러]]가 [[164_policy|정책]]이라면 디스패처는 메커니즘이다.

이 [[192_module_independence|모듈]]이 필요한 이유는 선택과 실행이 전혀 다른 문제이기 때문이다. [[079_kube_scheduler_pod_placement|스케줄러]]가 "P2를 실행하라"고 정해도, 누군가는 [[164_pc|프로그램 카운터]] (Program [[059_counter|Counter]], [[164_pc|PC]]), [[166_sp|스택 포인터]] ([[057_stack|Stack]] Pointer, [[166_sp|SP]]), 일반 [[057_register|레지스터]], [[353_page_table|페이지 테이블]] 포인터를 실제 하드웨어 상태로 바꿔야 한다. 이 단계가 없으면 [[675_multitasking_terminology_preemptive|멀티태스킹]]은 논리적으로만 존재하고 물리적으로는 CPU가 여전히 이전 작업 문맥에 머물게 된다.

이 그림은 [[079_kube_scheduler_pod_placement|스케줄러]]와 디스패처의 역할 분리를 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│           policy와 mechanism의 분리: scheduler vs dispatcher │
├──────────────────────────────────────────────────────────────┤
│ Ready Queue ─▶ Short-term Scheduler ─▶ Dispatcher           │
│                 "누가 다음인가?"         "어떻게 바꿀까?" │
│                                              │               │
│                                              ├─ save old ctx │
│                                              ├─ load new ctx │
│                                              └─ return user  │
└──────────────────────────────────────────────────────────────┘
```

[[001_operating_system_purpose|운영체제]]에서 응답성이 좋아 보이는 이유는 단순히 [[079_kube_scheduler_pod_placement|스케줄러]]가 똑똑해서가 아니라, 디스패처가 이 전환을 매우 짧게 끝내기 때문이다. 그래서 디스패처는 눈에 잘 띄지 않지만 CPU 스케줄링의 마지막 병목이자 실감 [[282_performance_tactics|성능]]의 관문이다.

- **📢 섹션 요약 비유**: [[079_kube_scheduler_pod_placement|스케줄러]]가 다음 선수 이름을 부르는 감독이라면, 디스패처는 실제로 바통을 건네고 트랙에 올려 보내는 [[216_progress_in_synchronization|진행]] 요원과 같다. 이름만 불러서는 경기가 [[216_progress_in_synchronization|진행]]되지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

디스패처의 핵심 작업은 세 단계로 요약된다. 첫째, 현재 작업의 CPU 문맥을 [[090_pcb_tcb|프로세스 제어 블록]] ([[300_process|Process]] Control Block, PCB)이나 [[092_thread_lwp|스레드]] 제어 블록에 저장한다. 둘째, 새 작업의 문맥과 주소 공간 정보를 복원한다. 셋째, 권한 레벨을 사용자 모드로 되돌리고 중단 지점의 PC로 점프한다.

| 단계 | 수행 내용 | 비용 포인트 |
| :--- | :-------- | :---------- |
| Save | [[164_pc|PC]], [[166_sp|SP]], [[162_gpr|범용 레지스터]], [[167_status_register|상태 레지스터]] 저장 | 메모리 기록 오버헤드 |
| [[238_switch_operation_principles|Switch]] | [[328_mmu|MMU]] 정보 교체, [[022_kernel_role|커널]] [[057_stack|스택]] 전환 | [[357_tlb|TLB]] 영향, 캐시 교란 |
| Restore | 새 문맥 복원 후 사용자 모드 복귀 | 반환 명령, 파이프라인 재시작 |

이 그림은 디스패처가 수행하는 시간 흐름을 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│                dispatcher timeline during switch            │
├──────────────────────────────────────────────────────────────┤
│ Running P0                                                  │
│    │                                                        │
│    ▼ interrupt / syscall                                    │
│ [kernel entry]                                              │
│    │                                                        │
│    ├─ save P0 context                                       │
│    ├─ scheduler selects P1                                  │
│    ├─ switch MMU / kernel stack                             │
│    ├─ restore P1 context                                    │
│    └─ return to user mode ───────────────▶ Running P1       │
└──────────────────────────────────────────────────────────────┘
```

이때 눈에 보이는 [[057_register|레지스터]] 복사보다 더 비싼 부분은 주소 공간 전환 이후의 메모리 지역성 손실이다. 같은 프로세스 안의 [[092_thread_lwp|스레드]] 전환은 [[353_page_table|페이지 테이블]]을 공유하므로 상대적으로 가볍지만, 다른 프로세스로 넘어가면 [[357_tlb|TLB]] 재사용성이 떨어지고 캐시도 차가워질 수 있다. 그래서 디스패처의 비용은 "몇 개 [[057_register|레지스터]]를 복사했는가"보다 "얼마나 많은 실행 맥락을 갈아치웠는가"로 봐야 한다.

- **📢 섹션 요약 비유**: 디스패처는 무대 배우를 바꾸는 백스테이지 팀과 같다. 사람만 교체하는 것이 아니라 조명, 소품, 대본 [[286_page_frame|페이지]]까지 모두 새 배우에 맞게 맞춰야 공연이 이어진다.

---

## Ⅲ. 비교 및 연결

디스패처를 이해할 때 가장 중요한 비교는 프로세스 전환과 [[092_thread_lwp|스레드]] 전환의 차이다. 둘 다 문맥 저장·복원을 하지만, [[092_thread_lwp|스레드]] 전환은 같은 주소 공간을 공유하는 경우가 많아 [[328_mmu|MMU]] 재설정 부담이 작다. 반면 프로세스 전환은 [[571_protection_vs_security|보호]] 경계가 달라지므로 주소 공간 교체와 캐시·[[357_tlb|TLB]] 영향이 더 크게 따라온다.

| 비교 축 | 프로세스 디스패치 | [[092_thread_lwp|스레드]] 디스패치 |
| :------ | :---------------- | :-------------- |
| 주소 공간 | 보통 변경 | 같은 프로세스면 유지 |
| [[328_mmu|MMU]]/[[357_tlb|TLB]] 영향 | 큼 | 작음 |
| 캐시 지역성 | 깨질 가능성 높음 | 비교적 유지 쉬움 |
| 체감 비용 | 무거움 | 가벼움 |

또 하나의 연결 개념은 [[169_dispatch_latency|디스패치 지연]] ([[169_dispatch_latency|Dispatch Latency]])이다. 디스패처는 이 [[015_지연_데이터_관점|지연]]의 중심부를 차지하며, 실시간 [[001_operating_system_purpose|운영체제]] (Real-Time [[001_operating_system_purpose|Operating System]], RTOS)는 이 값을 가능한 한 짧고 예측 가능하게 만들기 위해 선점 가능한 [[022_kernel_role|커널]] 구간을 늘리고 잠금 구간을 줄인다. 반대로 범용 [[001_operating_system_purpose|운영체제]]는 평균 [[139_throughput|처리량]]을 우선하므로, 평균은 빠르지만 최악 [[015_지연_데이터_관점|지연]]이 크게 튈 수 있다.

하드웨어 지원도 중요하다. 주소 공간 [[289_identification_flags_fragmentation_offset|식별자]] (Address Space [[088_identifier_in_er_model|Identifier]], [[360_asid|ASID]])나 프로세스 [[033_context|컨텍스트]] [[289_identification_flags_fragmentation_offset|식별자]] ([[300_process|Process]]-[[033_context|Context]] [[088_identifier_in_er_model|Identifier]], PCID)는 TLB를 전부 버리지 않고도 주소 공간을 구분하게 도와, 디스패처 부담을 줄인다. 따라서 디스패처는 [[001_operating_system_purpose|운영체제]] 코드이면서 동시에 CPU 아키텍처 지원의 수혜를 강하게 받는 영역이다.

- **📢 섹션 요약 비유**: 같은 사무실 안에서 자리만 바꾸는 것은 [[092_thread_lwp|스레드]] 전환이고, 회사 건물 자체를 옮기는 것은 프로세스 전환과 같다. 둘 다 이동이지만, 후자는 열쇠와 출입증까지 전부 갈아야 해서 훨씬 무겁다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 디스패처를 직접 호출하기보다, 그 비용이 문제를 일으킬 때 존재감을 드러낸다. 예를 들어 오디오 처리, 공장 제어, 차량 제어처럼 밀리초 미만 [[015_지연_데이터_관점|지연]]이 중요한 시스템에서는 [[169_dispatch_latency|디스패치 지연]]이 곧 품질 저하나 데드라인 위반으로 이어진다. 반대로 웹 서버처럼 [[139_throughput|처리량]] 중심 워크로드에서는 지나친 [[211_context_switch|문맥 교환]]만 줄여도 체감 [[282_performance_tactics|성능]]이 크게 좋아질 수 있다.

### 실무 시나리오

1. **실시간 제어 시스템**: 제어 루프 주기가 500μs인 장치에서 [[169_dispatch_latency|디스패치 지연]]이 150μs를 넘기면 실제 제어 계산에 쓸 시간이 급격히 줄어든다. 이 경우 일반 [[022_kernel_role|커널]]보다 선점성이 강화된 RTOS나 `PREEMPT_RT` 계열 구성이 유리하다.
2. **고빈도 I/O 서버**: 초당 수만 번의 네트워크 이벤트가 발생하는 서버는 [[211_context_switch|문맥 교환]] 자체가 부담이 될 수 있다. [[103_thread_pool|스레드 풀]], 이벤트 기반 모델, [[022_kernel_role|커널]] 우회 ([[022_kernel_role|Kernel]] Bypass)를 검토해야 하는 이유가 여기에 있다.
3. **보안 패치 이후 [[282_performance_tactics|성능]] 저하**: [[353_page_table|페이지 테이블]] 격리 ([[022_kernel_role|Kernel]] Page-Table [[195_isolation_concurrency_control|Isolation]], [[578_kpti|KPTI]]) 같은 보안 대책은 안전성을 높이지만, 디스패처 경로에 추가 비용을 만들 수 있다. 따라서 보안과 [[015_지연_데이터_관점|지연]] 예산을 함께 평가해야 한다.

### [[435_checklist_based_testing|체크리스트]]

- 전환 대상이 프로세스인지, 같은 주소 공간의 [[092_thread_lwp|스레드]]인지 구분했는가?
- 최대 허용 [[015_지연_데이터_관점|지연]]이 평균이 아니라 최악값 기준으로 충족되는가?
- [[357_tlb|TLB]], 캐시, 잠금 구간 때문에 숨은 오버헤드가 커지지 않는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 스케줄링 알고리즘만 바꾸면 응답성이 해결된다고 믿는 것
- 실시간 요구사항이 있는데 범용 OS의 평균 [[282_performance_tactics|성능]] 수치만 보고 판단하는 것
- 프로세스와 [[092_thread_lwp|스레드]] 전환 비용을 동일하게 취급하는 것

- **📢 섹션 요약 비유**: 디스패처 튜닝은 엘리베이터 호출 버튼만 바꾸는 일이 아니라, 문이 열리고 닫히는 속도와 승객 교체 시간을 함께 줄이는 일과 같다. 호출 알고리즘이 좋아도 문이 느리면 건물 전체가 답답해진다.

---

## Ⅴ. 기대효과 및 결론

디스패처가 효율적이면 [[001_operating_system_purpose|운영체제]]는 짧은 시간 간격으로도 부드럽게 작업을 바꿔 가며 [[675_multitasking_terminology_preemptive|멀티태스킹]]을 실현할 수 있다. 그 결과 응답성, CPU 활용도, 실시간성, 대화형 체감 [[282_performance_tactics|성능]]이 함께 개선된다. 특히 [[079_kube_scheduler_pod_placement|스케줄러]]의 [[164_policy|정책]]적 장점을 실제 [[282_performance_tactics|성능]]으로 전달해 주는 마지막 연결 고리라는 점에서 가치가 크다.

반대로 디스패처 비용이 크면 좋은 스케줄링 [[164_policy|정책]]도 실효성이 떨어진다. [[211_context_switch|문맥 교환]]이 잦을수록 캐시·[[357_tlb|TLB]] 손실, [[022_kernel_role|커널]] 진입 비용, [[571_protection_vs_security|보호]] 경계 전환 오버헤드가 누적되기 때문이다. 그래서 현대 시스템은 디스패처 자체를 최적화하는 동시에, [[092_thread_lwp|스레드]] 모델 개선·[[144_cpu_affinity|CPU affinity]]·이벤트 기반 처리·[[022_kernel_role|커널]] 우회처럼 "전환 횟수 자체를 줄이는 [[268_strategy_pattern|전략]]"도 함께 사용한다.

결국 디스패처는 스케줄링 이론의 부속물이 아니라, 선택된 [[164_policy|정책]]을 실제 하드웨어 동작으로 번역하는 핵심 실행기다. [[001_operating_system_purpose|운영체제]] [[282_performance_tactics|성능]]을 논할 때는 누구를 고르느냐만큼, 얼마나 빨리 넘겨주느냐를 같이 봐야 한다.

- **📢 섹션 요약 비유**: 디스패처는 릴레이 경기의 바통 전달 구간과 같다. 주자가 빠르더라도 바통을 건네는 순간마다 삐끗하면 경기 전체 기록은 절대 좋아지지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :---------- |
| [[161_short_term_scheduler|단기 스케줄러]] ([[161_short_term_scheduler|Short-term Scheduler]]) | 다음 실행 대상을 선택하는 [[164_policy|정책]] [[192_module_independence|모듈]] |
| [[211_context_switch|문맥 교환]] ([[211_context_switch|Context Switch]]) | 디스패처가 실제로 수행하는 저장·복원 절차 |
| [[169_dispatch_latency|디스패치 지연]] ([[169_dispatch_latency|Dispatch Latency]]) | 디스패처 경로가 만드는 핵심 시간 비용 |
| [[328_mmu|MMU]] / [[357_tlb|TLB]] | 주소 공간 전환 시 디스패처 오버헤드에 큰 영향 |
| RTOS | 디스패처의 최악 [[015_지연_데이터_관점|지연]]을 엄격하게 관리하는 [[001_operating_system_purpose|운영체제]] |

### 📈 관련 키워드 및 발전 흐름도

```text
Ready Queue 선택
    │
    ▼
Short-term Scheduler
    │
    ▼
Dispatcher
    │
    ├──────────────▶ save / restore context
    ├──────────────▶ MMU · TLB 전환
    ├──────────────▶ user mode return
    ▼
Dispatch Latency 최적화
    │
    ▼
RTOS · ASID/PCID · Kernel Bypass
```

이 흐름도는 스케줄링의 논리적 선택이 디스패처를 거쳐 실제 하드웨어 실행으로 이어지고, 이후에는 [[015_지연_데이터_관점|지연]] 최적화 문제로 확장된다는 점을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 감독이 "다음 선수 들어가!"라고 말해도, 누군가는 진짜로 선수를 바꿔 줘야 해요.
2. 컴퓨터에서는 그 일을 디스패처가 해서, 전에 뛰던 친구의 자리를 정리하고 새 친구를 무대에 올려요.
3. 이 교대가 빨라야 모두가 기다리지 않고 매끄럽게 차례를 바꿔 가며 놀 수 있답니다.
