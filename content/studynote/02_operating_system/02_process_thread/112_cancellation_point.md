+++
title = "112. 취소 점 (Cancellation Point)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 취소 점(Cancellation Point)은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소(Deferred Cancellation) 모드에서 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 자신에게 설정된 취소 요청을 검사하고 반응하는 특정 지점이다. 이 지점에서 pthread_testcancel()가 호출되거나 블로킹 시스템 콜이 내부적으로 검사를 수행한다.
> 2. **가치**: 취소 점점이 없으면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 영원히 취소되지 않아 자원 누수가 발생한다. 반면 너무 자주 검사하면 오버헤드가 증가하므로, 블로킹 API를 자연스러운 취소 점으로 활용하는 것이 POSIX의 설계 철학이다.
> 3. **융합**: POSIX 표준은 [select](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/)(), poll(), pthread_cond_wait(), pthread_mutex_lock(), sleep(), read(), write() 등을 표준 취소 점점으로 정의하며, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 이들 호출 전에 자동으로 취소 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)를 검사한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 취소 점은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 취소 요청을 처리하기 위해 검사하는 지점이다. 명시적 점점은 pthread_testcancel()이며, 암시적 점점은 블로킹 시스템 콜 내부에서 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 자동으로 수행한다.

```text
┌────────────────────────────────────────────────────────────┐
│           취소 점점의 두 가지 종류                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  명시적 점점 (pthread_testcancel):                         │
│  while (!done) {                                           │
│      pthread_testcancel();  ◀── 명시적 검사 지점           │
│      data = process_item();                                │
│  }                                                         │
│  특징: 개발자가 직접 삽입, 검사 주기 조절 가능             │
│                                                            │
│  암시적 점점 (POSIX 정의):                                 │
│  data = read(fd, buf, size);  ◀── read()가 내부적으로      │
│                              취소 플래그를 검사            │
│  pthread_cond_wait(&cond, &mutex); ◀── cond_wait도 검사    │
│  sem_wait(&sem);               ◀─ 세마포어도 검사          │
│                                                            │
│  POSIX 표준 취소 점점 목록:                                │
│  accept(), aio_suspend(), clock_nanosleep(),               │
│  close(), connect(), creat(), fcntl(),                     │
│  fopen(), flock(), fsync(), msync(),                       │
│  mq_receive(), mq_send(), msgrcv(), msgsnd(),              │
│  nanosleep(), open(), pause(), poll(),                     │
│  pread(), pwrite(), pthread_cond_timedwait(),              │
│  pthread_cond_wait(), pthread_join(), pthread_mutex_lock(),│
│  pthread_testcancel(), putc(), pthread_rwlock_*(),         │
│  read(), recv(), recvfrom(), select(), sem_wait(),         │
│  sigwait(), sigtimedwait(), sleep(), system(),             │
│  wait(), waitpid(), write()                                │
└────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** POSIX는 수십 개의 블로킹 시스템 콜을 암시적 취소 점점으로 정의한다. 이 함수들이 블로킹되어 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)로 진입할 때, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 취소 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)를 검사하고 설정되어 있으면 EINTR을 반환하여 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 루프에서 탈출할 수 있게 한다. 이 설계 덕분에 개발자가 매 반복문마다 pthread_testcancel()을 삽입하지 않아도 취소가 가능하다. pthread_testcancel()은 CPU 집약적인 루프에서 취소 응답성을 높이고 싶을 때 추가로 사용한다.

- **📢 섹션 요약 비유**: 암시적 취소 점점은 "역에서 정기적으로 안내방 방송"과 같습니다. 기사([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))가 중간에 한 번씩 "아직 멈출 건가요?"라고 물어봅니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 취소 점점 내부 동작

```text
┌─────────────────────────────────────────────────────────┐
│  블로킹 시스템 콜 내부 취소 점점 검사 흐름              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ① 사용자 코드: read(fd, buf, size) 호출                │
│     │                                                   │
│  ② glibc 래퍼: read() → syscall(SYS_read, ...)          │
│     │                                                   │
│  ③ 커널 진입: sys_read() → 블로킹 전에                  │
│     │   if (fatal_signal_pending(current))              │
│     │     → EINTR 반환                                  │
│     │   if (current->cancel_pending)                    │
│     │     → 스레드 종료 (PTHREAD_CANCE)                 │
│     │   else                                            │
│     │     → 실제 블로킹 (슬립)                          │
│                                                         │
│  ④ 데이터 도착 → 루프 재개                              │
└─────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 시스템 콜 진입 지점에서는 취소 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)와 시그널 펜딩(pending [signal](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/))을 검사한다. 취소 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)가 설정되어 있으면 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 종료시키고, 펜딩된 시그널이 있으면 EINTR을 반환하여 사용자 공간에서 루프를 탈출하게 한다. 이 3단계 검사가 매 블로킹 시스템 콜에 공통으로 적용되어 있다.

- **📢 섹션 요약 비유**: 취소 점점의 내부 동작은 "역에서 다리로 향할 때 중간에 사고 점검"과 같습니다. 기사가 3가지(시그널, 취소 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), 블로킹)를 순서대로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)합니다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 명시적 (testcancel) | 암시적 (POSIX [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) |
|:---|:---|:---|
| **삽입 위치** | 개발자가 직접 지정 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 자동 |
| **검사 빈도** | 루프마다 (높은 오버헤드) | 블로킹 시마다 (낮은 오버헤드) |
| **CPU 집약적 루프** | 추천 추가 | 불필요 |
| **응답성** | 높음 | 낮음 (블로킹 주기) |

- **📢 섹션 요약 비유**: CPU를 많이 쓰는 계산 작업에는 정기 검사(testcancel)를 추가하고, I/O 대기 작업에는 블로킹 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 자체를 검사점으로 활용하세요.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **순수 루프에 취소 점점 없음**: 무한 루프를 돌며 I/O가 없는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 암시적 점점에 도달하지 못해 취소되지 않는다. 반드시 pthread_testcancel()을 삽입하거나 전역 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)를 주기적으로 검사해야 한다.

- **📢 섹션 요약 비유**: 무한 루프는 "정지 버튼이 없는 트레드밀"과 같습니다. 반드시 정기적으로 멈출 지점(checkpoint)을 만들어야 합니다.

---

## Ⅴ. 기대효과 및 결론

- **📢 섹션 요약 비유**: 취소 점점 설계는 "안전 설계의 핵심"입니다. 적절한 검사 지점 배치는 응답성과 안전성의 균형을 맞추는 열쇠입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [고아 프로세스](/knowledge-base/studynote/02_operating_system/02_process_thread/110_orphan_process/) ([Orphan Process](/knowledge-base/studynote/02_operating_system/02_process_thread/110_orphan_process/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [스레드 취소](/knowledge-base/studynote/02_operating_system/02_process_thread/111_thread_cancellation/) ([Thread Cancellation](/knowledge-base/studynote/02_operating_system/02_process_thread/111_thread_cancellation/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [스레드 로컬 저장소](/knowledge-base/studynote/02_operating_system/02_process_thread/113_thread_local_storage/) ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/), [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-Local Storage) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [스케줄러 액티베이션](/knowledge-base/studynote/02_operating_system/02_process_thread/114_scheduler_activation/) ([Scheduler Activation](/knowledge-base/studynote/02_operating_system/02_process_thread/114_scheduler_activation/)) / 경량 프로세스(LWP) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스레드 취소 (Thread Cancellation)]
    │
    ▼
[취소 점 (Cancellation Point)]
    │
    ├──▶ [스레드 로컬 저장소 (TLS, Thread-Local Storage)]
    └──▶ [스케줄러 액티베이션 (Scheduler Activation) / 경량 프로세스(LWP)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 취소 점은 "프로그램의 정류 검문소" 같아요. 긴 작업 중간중에 "정지 버튼을 눌렀는가?"하고 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 곳이에요.
2. I/O 작업([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽기, 네트워크 대기)을 하는 동안 컴퓨터가 자동으로 "정지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"을 해줍니다.
3. 계산만 반복하는 작업에는 정기적으로 "정지 버튼 눌렀는가?"를 코드에 직접 추가해야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 800

← **이전**: [111. 스레드 취소 (Thread Cancellation) - 비동기식 취소, 지연 취소](/knowledge-base/studynote/02_operating_system/02_process_thread/111_thread_cancellation/)
**다음**: [113. 스레드 로컬 저장소 (TLS, Thread-Local Storage)](/knowledge-base/studynote/02_operating_system/02_process_thread/113_thread_local_storage/) →

---
