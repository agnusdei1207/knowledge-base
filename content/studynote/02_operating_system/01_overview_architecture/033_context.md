+++
title = "컨텍스트 (Context) / 컨텍스트 스위칭 (Context Switching)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

> **핵심 인사이트 3줄**
> 1. 컨텍스트(Context)는 프로세스가 실행 중인 순간의 완전한 상태 스냅샷으로, CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)·[PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)·[스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/)·[프로세스 제어 블록](/knowledge-base/studynote/02_operating_system/02_process_thread/090_pcb_tcb/)(PCB) 정보를 포함한다.
> 2. [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/)(Context Switching)은 현재 프로세스 컨텍스트를 저장하고 다음 프로세스 컨텍스트를 복원하는 OS 핵심 작업으로, 멀티태스킹의 기반이다.
> 3. [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 순수 오버헤드(no useful work)로 최소화해야 하며, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 전환이 프로세스 전환보다 빠른 이유는 메모리 공간을 공유해 [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시가 불필요하기 때문이다.

---

## Ⅰ. 컨텍스트의 정의와 구성 요소

컨텍스트(Context)는 <strong>프로세스가 특정 시점에 실행 중인 모든 상태 정보의 집합</strong>이다.

### PCB([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Control Block) 내 컨텍스트 정보



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PCB (Process Control Block)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PID (프로세스 ID)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">프로세스 상태 (Running/Ready/...)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">프로그램 카운터 (PC, 다음 명령 주소)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CPU 레지스터 (AX, BX, SP, BP...)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메모리 관리 정보 (페이지 테이블 등)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">I/O 상태 정보 (열린 파일 목록)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스케줄링 정보 (우선순위, CPU 사용량)</div></div>
</div>
</div>



📢 **섹션 요약 비유**: 컨텍스트는 책갈피와 메모이다 — 책을 덮을 때(CPU에서 내려올 때) 몇 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)인지, 어떤 내용까지 읽었는지 모두 적어둔다.

---

## Ⅱ. [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 과정



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">프로세스 A 실행 중</div>
<div class="kb-diagram-note">↓ 인터럽트 / 타임 퀀텀 만료</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">PCB_A에 저장</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2</div><div class="kb-diagram-note">PCB_A를 레디 큐에 이동</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3</div><div class="kb-diagram-note">스케줄러: 다음 프로세스 B 선택</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4</div><div class="kb-diagram-note">PCB_B에서 레지스터 복원</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">5</div><div class="kb-diagram-note">프로세스 B 실행 재개</div></div>
</div>
</div>



### [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)

| 원인            | 설명                     |
|---------------|--------------------------|
| 타임 퀀텀 만료  | [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/) [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링       |
| I/O 대기       | 블로킹 시스템 콜           |
| [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)       | [하드웨어 인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/017_hardware_interrupt/) 처리     |
| 우선순위 선점   | 높은 우선순위 프로세스 도착 |
| 시스템 콜       | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 전환             |

📢 **섹션 요약 비유**: [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 요리사가 여러 요리를 번갈아 하는 것이다 — 한 냄비를 끄고(상태 저장) 다른 냄비를 켜되(상태 복원), 정확히 어디서 끊었는지 기억해야 한다.

---

## Ⅲ. [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 오버헤드

### 직접 비용

- CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 저장·복원: ~수백 ns
- [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) 플러시: 메모리 접근 캐시 무효화
- 캐시 [콜드 스타트](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/): 새 프로세스 데이터가 캐시에 없음

### 오버헤드 측정

```
x86-64 기준 컨텍스트 스위칭 비용:
  - 프로세스 간: 3~5 μs
  - 스레드 간: 1~2 μs (같은 주소 공간, TLB 플러시 없음)
  - 코루틴 간: ~100 ns (유저 스페이스, 커널 개입 없음)
```

### 스위칭 비용 비교

```
프로세스 > 스레드 > 코루틴/파이버 > 비동기(async/await)
  ↑더 느림                           더 빠름↑
```

📢 **섹션 요약 비유**: [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 오버헤드는 사무실 이동 시간이다 — 건물 이사(프로세스), 같은 건물 다른 방([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)), 자리만 바꾸기([코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) 순서로 비용이 다르다.

---

## Ⅳ. 프로세스 vs [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/)

| 항목          | 프로세스 스위칭          | [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스위칭           |
|-------------|------------------------|------------------------|
| 주소 공간    | 변경 ([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 발생)  | 동일 ([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 없음)  |
| 저장 정보   | PCB 전체                | TCB ([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 제어 블록)  |
| [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) | 교체됨                  | 교체 없음               |
| 비용         | 높음 (3~5μs)           | 낮음 (1~2μs)            |
| [격리성](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)       | 완전 격리               | [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) (락 필요)    |

### [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) vs 사용자 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">커널 스레드: OS가 관리 → 시스템 콜 필요, 진짜 병렬성</div>
<div class="kb-diagram-note">사용자 스레드: 라이브러리 관리 → 빠른 전환, OS에 불투명</div>
<div class="kb-diagram-note">(Go goroutine, Python greenlet)</div>
</div>
</div>



📢 **섹션 요약 비유**: 프로세스 스위칭은 다른 나라 여행, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스위칭은 같은 호텔 방 이동이다 — 여행은 여권·환전([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시)이 필요하지만 방 이동은 열쇠만 바꾼다.

---

## Ⅴ. [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 최소화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

### [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 수준

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)              | 설명                          |
|-----------------|-------------------------------|
| 타임 퀀텀 조정   | 너무 짧으면 스위칭 과다         |
| CPU 핀닝         | 프로세스를 특정 CPU 코어에 고정 |
| [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 인식 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) | 같은 [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) 노드에서 실행 유지   |
| 실시간 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)   | SCHED_FIFO — 선점 없음         |

### 애플리케이션 수준

- **비동기 I/O (async/await)**: 블로킹 없이 [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)로 처리
- <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/">코루틴</a></strong>: 유저 스페이스 협력적 전환 (Go, Kotlin)
- **이벤트 드리븐**: Node.js 싱글 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) + [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/)

📢 **섹션 요약 비유**: [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 최소화는 회의 줄이기다 — 매번 회의(스위칭)를 하는 대신, 한 사람이 끝낼 때까지 기다리거나([코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) 문자(비동기)로 처리한다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">컨텍스트 (Context)</div>
<div class="kb-diagram-tree-item" style="--depth:0">PCB (Process Control Block)</div>
<div class="kb-diagram-note">── CPU 레지스터 상태</div>
<div class="kb-diagram-note">── 프로그램 카운터 (PC)</div>
<div class="kb-diagram-note">── 메모리 매핑 정보</div>
<div class="kb-diagram-tree-item" style="--depth:0">컨텍스트 스위칭</div>
<div class="kb-diagram-note">── 트리거: 타임 퀀텀·I/O·인터럽트</div>
<div class="kb-diagram-note">── 프로세스 vs 스레드 비용 차이</div>
<div class="kb-diagram-note">── TLB 플러시 오버헤드</div>
<div class="kb-diagram-tree-item" style="--depth:0">최적화</div>
<div class="kb-diagram-note">── CPU 핀닝 (Affinity)</div>
<div class="kb-diagram-note">── 코루틴 (유저 스페이스 스위칭)</div>
<div class="kb-diagram-note">── 비동기 I/O (async/await)</div>
<div class="kb-diagram-tree-item" style="--depth:0">관련 개념</div>
<div class="kb-diagram-tree-item" style="--depth:2">스케줄링 알고리즘</div>
<div class="kb-diagram-tree-item" style="--depth:2">인터럽트 처리</div>
<div class="kb-diagram-tree-item" style="--depth:2">시스템 콜 (커널 모드 전환)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컨텍스트 스위칭 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1960년대</div><div class="kb-diagram-cell">협력적 멀티태스킹</div><div class="kb-diagram-cell">프로세스 자발적 CPU 반납</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1970년대</div><div class="kb-diagram-cell">선점형 스케줄링</div><div class="kb-diagram-cell">타이머 인터럽트 기반 스위칭</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1990년대</div><div class="kb-diagram-cell">스레드 개념 도입</div><div class="kb-diagram-cell">경량 컨텍스트 스위칭</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2000년대</div><div class="kb-diagram-cell">SMP·멀티코어</div><div class="kb-diagram-cell">코어별 독립 스케줄러</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2010년대</div><div class="kb-diagram-cell">코루틴·Go goroutine</div><div class="kb-diagram-cell">유저 스페이스 협력적 스위칭</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2020년대</div><div class="kb-diagram-cell">async/await 표준화</div><div class="kb-diagram-cell">I/O 없는 컨텍스트 전환 최소화</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">PCB → 컨텍스트 저장/복원 → 스케줄러 → 멀티태스킹</div>
<div class="kb-diagram-note">레지스터 TLB 플러시 우선순위 큐</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">프로세스 &gt; 스레드 &gt; 코루틴 &gt; async (비용 감소 방향)</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. 컨텍스트는 책갈피다 — 책을 덮을 때 몇 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)인지 적어두면 다시 열었을 때 정확히 이어 읽을 수 있다.
2. [컨텍스트 스위칭](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 여러 숙제를 번갈아 하는 것이다 — 수학 숙제를 잠깐 멈추고(저장) 영어 숙제를 시작했다가(복원) 다시 수학으로 돌아온다.
3. [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 전환이 빠른 이유는 같은 책상을 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문이다 — 프로세스는 다른 방으로 이사 가야 하지만, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 같은 방에서 자리만 바꾼다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 800

← **이전**: [펌웨어 (Firmware)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)
**다음**: [컨텍스트 스위칭 (Context Switch) 심화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/034_context_switch/) →

---
