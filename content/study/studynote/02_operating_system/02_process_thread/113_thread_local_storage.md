---
title: 113. 스레드 로컬 저장소 (TLS, Thread-Local Storage)
date: '2026-05-08'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[694_thread_local_storage_tls|TLS]] ([[092_thread_lwp|Thread]]-Local Storage)는 각 [[092_thread_lwp|스레드]]마다 독립적으로 소유하는 [[001_dikw_pyramid|데이터]] 저장 공간이다. 전역 변수(global variable)와 달리 [[694_thread_local_storage_tls|TLS]] 변수는 [[092_thread_lwp|스레드]] 간에 공유되지 않으므로 [[212_synchronization_mechanisms|동기화]] 없이 안전하게 접근할 수 있다.
> 2. **가치**: errno, [[092_thread_lwp|스레드]] ID, [[486_trng|난수 생성기]] 시드, per-[[092_thread_lwp|thread]] 버퍼 등 [[092_thread_lwp|스레드]]마다 고유해야 하는 [[001_dikw_pyramid|데이터]]를 관리하는 표준 수단이다. [[212_synchronization_mechanisms|동기화]] 없이 [[092_thread_lwp|thread]]-safe한 [[386_data_clean_room_sharing|데이터 공유]] 패턴을 실현할 수 있다.
> 3. **융합**: C11의 _Thread_local, C++의 thread_local, Java의 ThreadLocal, Go의 goroutine-local storage, Rust의 thread_local! 등 현대 언어에서 광범위하게 지원된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: TLS는 각 [[092_thread_lwp|스레드]]에 고유한 저장 공간을 제공하는 메커니즘이다. 컴파일러와 런타임이 협력하여, 동일한 변수 이름이라도 각 [[092_thread_lwp|스레드]]가 접근하는 인스턴스가 물리적으로 다른 메모리 위치를 가리키도록 구현한다.

- **필요성**: [[095_multithreading_benefits|다중 스레드]] 환경에서 전역 변수를 사용하면 레스 컨디션([[213_race_condition|Race Condition]])이 발생한다. 매번 뮤텍스로 [[571_protection_vs_security|보호]]할 수 있지만 오버헤드가 크다. TLS는 이 문제를 근본적으로 해결하여, [[092_thread_lwp|스레드]]별 고유 [[001_dikw_pyramid|데이터]]를 [[212_synchronization_mechanisms|동기화]] 없이 안전하게 유지한다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│           전역 변수 vs TLS — 스레드별 데이터 격리                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  전역 변수 (공유 — 레스 컨디션 위험):                               │
│  ┌─────────────────────────────┐                                    │
│  │ int thread_id = 0;          │  Thread A: thread_id = 1           │
│  │ srand(42);                 │  Thread B: thread_id = 1  │ ▶ 충돌! │
│  └─────────────────────────────┘                                    │
│                                                                     │
│  TLS 변수 (스레드별 독립 — 안전):                                   │
│  ┌─────────────┐ ┌─────────────┐                                    │
│  │ Thread A    │ │ Thread B    │                                    │
│  │ tid = 1   │ │ tid = 2    │  ← 각자 독립 저장                     │
│  │ seed = 42 │ │ seed = 99 │  ← 동기화 불필요                       │
│  │ buf = ... │ │ buf = ... │                                        │
│  └─────────────┘ └─────────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전역 변수 thread_id를 두 [[092_thread_lwp|스레드]]가 동시에 쓰면 레스 컨디션이 발생하여 결과가 예측 불가능해진다. 반면 [[694_thread_local_storage_tls|TLS]] 변수 tid는 각 [[092_thread_lwp|스레드]]가 물리적으로 다른 메모리에 접근하므로 [[212_synchronization_mechanisms|동기화]] 없이 안전하다. errno가 TLS로 구현되어 있는 이유가 바로 이것이다 — 각 [[092_thread_lwp|스레드]]의 시스템 콜 오류 번호가 독립적으로 유지되어야 하기 때문이다.

- **📢 섹션 요약 비유**: TLS는 "각 직원의 개인 사물함"과 같습니다. 같은 이름의 사물함이 직원별로 따로 있으므로 동시에 열어도 충돌하지 않습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구현 방식

| 구현 | 언어 | 특징 |
|:---|:---|:---|
| **__thread (GCC)** | C | 컴파일러가 [[694_thread_local_storage_tls|TLS]] [[057_register|레지스터]](FS/GS 세그먼트)로 구현 |
| **_Thread_local** | C11 | C11 표준, 모든 [[092_thread_lwp|스레드]]에서 초기화 가능 |
| **thread_local** | C++ | C++[[308_static_dynamic_nat_pat_port_address_translation|11]] 키워드, static + non-static 모두 지원 |
| **ThreadLocal** | Java | java.lang.ThreadLocal, 커스텀 익명명으로 접근 |
| **__declspec([[092_thread_lwp|thread]])** | Windows MSVC | 마이크로소프트 특수 키워드 |
| **__thread_local** | [[782_memory_safety_rust_compiler_verification|Rust]] | [[782_memory_safety_rust_compiler_verification|rust]] 1.59+, std::[[092_thread_lwp|thread]]::LocalKey |

### [[694_thread_local_storage_tls|TLS]] 스토리지 레이아웃

```text
┌─────────────────────────────────────────────────────────────────────────┐
│              TLS 메모리 레이아웃 (x86-64 예시)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  고주소 (High Address)                                                  │
│  ┌────────────────────────────────────────────────┐                     │
│  │         TCB (Thread Control Block)                 │                 │
│  │         ┌─────────────────────────────┐          │                   │
│  │         │ TLS Array (스레드별 데이터)     │          │               │
│  │         │  ┌──────┐ ┌──────┐ ... ┌──────┐│          │                │
│  │         │  │t_id  │ │seed  │ ... │buf  ││          │                 │
│  │         │  └──────┘ └──────┘     └──────┘│          │                │
│ │         └─────────────────────────────────────┘          │            │
│  └────────────────────────────────────────────────┘                     │
│                                                                         │
│  FS (fs = 0) 레지스터 → __thread 변수 저장                              │
│  GS (gs = 지정) 레지스터 → 현재 스레드 TCB 주소                         │
│                                                                         │
│  fs:[tls_index] → 해당 스레드의 TLS 데이터에 직접 접근                  │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램활** x86-64 아키텍처에서 TLS는 FS (FS [[407_tcp_segment_header_structure_20_60_bytes|Segment]] [[175_register_addressing|Register]]) [[057_register|레지스터]]를 통해 접근된다. 각 [[092_thread_lwp|스레드]]의 TCB 내부에 [[694_thread_local_storage_tls|TLS]] 배열이 위치하며, FS [[057_register|레지스터]]가 현재 [[092_thread_lwp|스레드]]의 TCB를 가리키므로, FS 오프셋 계산으로 [[694_thread_local_storage_tls|TLS]] [[001_dikw_pyramid|데이터]]에 직접 접근할 수 있다. 이것이 [[694_thread_local_storage_tls|TLS]] 접근이 전역 변수 접근과 거의 동일한 [[282_performance_tactics|성능]]을 보장하는 이유다 (단일 명령어로 접근 가능).

- **📢 섹션 요약 비연**: [[694_thread_local_storage_tls|TLS]] 레이아웃은 "각 사원함의 ID 카드"와 같습니다. FS [[057_register|레지스터]]로 ID 카드를 찾아 바로 접근하므로 검색 시간이 거의 0에 가깝니다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 전역 변수 + 뮤텍스 | [[694_thread_local_storage_tls|TLS]] | __thread |
|:---|:---|::---|:---:|
| **레이스 컨디션** | 위험 ([[571_protection_vs_security|보호]] 필요) | 없음 (독립) | 없음 |
| **접근 [[282_performance_tactics|성능]]** | L1 캐시 (공유) | L1 캐시 ([[694_thread_local_storage_tls|TLS]] 캐시) | L1 캐시 (동일 [[282_performance_tactics|성능]]) |
| **동적 [[087_process_state_transition|생성]]** | 불가 (컴파일 타임) | 한계적 (C11)/풍부 | 불가 (컴파일 타임) |
| **포터터 공유** | 가능 (위험) | 불가 | 불가 |

- **📢 섹션 요약 비율**: TLS는 "각 직원이 개인 사물함을 가지는 방식"으로, [[001_dikw_pyramid|데이터]] 격리를 통해 레스 컨디션 문제를 근본적으로 해결합니다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **과도한 [[694_thread_local_storage_tls|TLS]] 사용**: 모든 변수를 TLS로 만들면 메모리 사용량이 N배가 된다. 진짜 [[092_thread_lwp|스레드]]별 고유 [[001_dikw_pyramid|데이터]]만 TLS에 저장해야 한다.
- **TLS로 숨검번호 [[087_process_state_transition|생성]]**: TLS에 rand() 시드를 저장하면 [[092_thread_lwp|스레드]] 간 독립 난수 [[087_process_state_transition|생성]]이 보장되지만, 보안상 예측 가능한 난수는 보안에 취약점이 될 수 있다. 암호학적으로 안전한 난수에는 /dev/urandom 사용.

- **📢 섹션 요약 비율**: TLS는 "필요한 것만 개인 사물함에 넣는" 원칙을 지켜야 합니다. 모든 물건을 사물함에 넣으면 공간이 부족해집니다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

- **📢 섹션 요약 비율**: TLS는 [[095_multithreading_benefits|다중 스레드]] 환경에서 "[[212_synchronization_mechanisms|동기화]] 없는 안전한 [[386_data_clean_room_sharing|데이터 공유]]"의 핵심 기법이며, errno가 TLS인 이유는 시스템 콜 오류 처리의 [[092_thread_lwp|thread]]-safety를 보장하기 위해서입니다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[111_thread_cancellation|스레드 취소]] ([[111_thread_cancellation|Thread Cancellation]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[112_cancellation_point|취소 점]] ([[112_cancellation_point|Cancellation Point]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[114_scheduler_activation|스케줄러 액티베이션]] ([[114_scheduler_activation|Scheduler Activation]]) / 경량 프로세스(LWP) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[115_upcall|상향 호출]] ([[115_upcall|Upcall]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[취소 점 (Cancellation Point)]
    │
    ▼
[스레드 로컬 저장소 (TLS, Thread-Local Storage)]
    │
    ├──▶ [스케줄러 액티베이션 (Scheduler Activation) / 경량 프로세스(LWP)]
    └──▶ [상향 호출 (Upcall)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. TLS는 "학생 번호표"와 같아요. 같은 "번호"라도 각 학생이 자기만의 번호표를 가지고 있어서 섞이 볼 일이 없어요.
2. 컴퓨터에서도 각 [[092_thread_lwp|스레드]](작업자)가 자기만의 번호표([[694_thread_local_storage_tls|TLS]])를 가지면, 서로 다른 사람 번호를 읽을 때 혼선이 생기지 않아요.
3. 예를 들어 오류 번호(errno)를 저장할 때 TLS를 쓰면, 한 작업자의 오류가 다른 작업자의 화면에 뜨지 않아 안전하답니다!
