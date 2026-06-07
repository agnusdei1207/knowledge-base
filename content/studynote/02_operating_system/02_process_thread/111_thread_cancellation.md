---
title: "111. Thread Cancellation"
date: "2026-05-08"
tags:
  - "studynote-operating-system"
weight: 111
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 취소([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) Cancellation)는 한 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 다른 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 실행을 중단시키는 메커니즘이다. 비동기식 취소(즉시 중단)과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소([취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)점에서만 중단) 두 방식이 있으며, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소가 안전하고 실무적으로 선호된다.
> 2. **가치**: 긴 시간 실행되는 I/O 작업이나 무한 루프를 중단해야 하는 서버 환경에서 필수적이며, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소를 사용하면 자원(메모리, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 핸들, 락)을 안전하게 정리할 수 있다.
> 3. **윙합**: pthread_cancel()은 POSIX 표준 API이며, C++20의 std::stop_token, Java의 [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/).[interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)(), Go의 [context](/studynote/02_operating_system/01_overview_architecture/033_context/).Cancel() 등으로 각 언어어에서 유사한 기법이 제공된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 취소는 취소 요청(request)이 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)된 타겟 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 종료시키는 기법이다. 비동기식 취소는 타겟 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)의 어느 시점에서든 즉시 SIGCANCEL 시그널을 전송하여 강제 중단하며, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소는 타겟 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 [취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)점에 도달했을 때만 종료를 수행한다.

```text
+----------------------------------------------------------------+
|         비동기식 vs 지연 취소 비교                             |
+----------------------------------------------------------------+
|                                                                |
|  비동기식 취소 (PTHREAD_CANCEL_ASYNCHRONOUS):                  |
|  취소 요청 ---> 타겟 스레드에 SIGCANCEL 전송                    |
|             ---> 타겟 스레드 즉시 종료                          |
|                                                                |
|  리스크:                                                       |
|  +--------------------------------------+                      |
|  | void* worker(void* arg) {            |                      |
|  |   lock(&mutex);      <--- 락 획득        |                   |
|  |   data = process();  <--- 중간에 종료!    |                  |
|  |   unlock(&mutex);  <--- 영원 안 됨       | -> 데드락          |
|  | }                                     |                     |
|  +--------------------------------------+                      |
|                                                                |
|  지연 취소 (PTHREAD_CANCEL_DEFERRED, 기본):                    |
|  취소 요청 ---> 타겟 스레드에 플래그 설정                       |
|             ---> 타겟 스레드가 취소 점점 도달 시                |
|                ---> 안전하게 종료 (락 해제 등)                  |
|                                                                |
|  안전:                                                         |
|  +--------------------------------------+                      |
|  | void* worker(void* arg) {            |                      |
|  |   while (!cancelled) {               |                      |
|  |     lock(&mutex);                   |                       |
|  |     data = process();                |                      |
|  |     unlock(&mutex);                 | -> 안전 종료           |
|  |   }                                      |                  |
|  |   cleanup();                           |                    |
|  | }                                     |                     |
|  +--------------------------------------+                      |
+----------------------------------------------------------------+
```

**[다이어그램 해설]** 비동기식 취소에서는 락을 획득한 상태에서 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 강제 종료되므로 락이 영원 해제되지 않아 데드락([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))이 발생한다. 반면 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소에서는 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 루프 내에서 pthread_testcancel()이나 [취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)점(예: pthread_cond_wait() 등)에 도달할 때만 종료하므로, 락 해제와 자원 정리(cleanup)를 보장할 수 있다. 이 때문에 POSIX에서는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소를 기본값으로 사용한다.

- **📢 섹션 요약 비유**: 비동기식 취소는 "전화 중에 선을 끊는 것"과 같고, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소는 "통화가 끝나는 대기 후 끊는 것"과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 요소명 | 역할 | 특징 |
|:---|:---|:---|
| **pthread_cancel()** | 취소 요청 전송 | 타겟 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 취소 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| **pthread_testcancel()** | [취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)점 검사 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소 시 명시적 검사 지점 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/112_cancellation_point/">취소 점</a>점</strong> | 커널이 자동 검사하는 지점 | pthread_cond_wait() 등 블로킹 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
| **cleanup handler** | 취소 시 정리 함수 | pthread_cleanup_push/pop로 등록 |

- **📢 섹션 요약 비유**: [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소는 "안전벨트"를 거쳐야만 홈에 들어가는 시스템과 같습니다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 비동기식 취소 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소 |
|:---|:---|:---|
| **응답성** | 즉시 (μs 단위) | [취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)점까지 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| **안전성** | 위험 (자원 유출, 데드락) | 안전 (정리 보장) |
| **구현 복잡도** | 단순 | 루프 내 검사 필요 |
| **POSIX 기본값** | 아님 | **예 (기본)** |

- **📢 섹션 요약 비유**: 항상 "안전"을 선택하세요. 응답성이 중요하다면 [취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)점을 더 자주 확인하도록 설계하면 양쪽의 장점을 모두 가질 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **취소 시 뮤텍스 해제 누락**: [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소에서도 cleanup handler 내에 [lock](/studynote/05_database/04_transactions_concurrency/510_lock/) 해제를 넣지 않으면 뮤텍스가 영원 해제되지 않는다.

- **📢 섹션 요약 비유**: "작업 취소 시 정리 안 함"은 "퇴사 후 책상 정리 안 함"과 같습니다. 다음 사람이 사용할 수 없게 됩니다.

---

## Ⅴ. 기대효과 및 결론

- **📢 섹션 요약 비유**: [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 취소는 "안전 장치가 된 작업 중단 시스템"입니다. 타이머를 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해두면 자원 누수 없이 안전하게 중단할 수 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [좀비 프로세스](/studynote/02_operating_system/02_process_thread/109_zombie_process/) ([Zombie Process](/studynote/02_operating_system/02_process_thread/109_zombie_process/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [고아 프로세스](/studynote/02_operating_system/02_process_thread/110_orphan_process/) ([Orphan Process](/studynote/02_operating_system/02_process_thread/110_orphan_process/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [취소 점](/studynote/02_operating_system/02_process_thread/112_cancellation_point/) ([Cancellation Point](/studynote/02_operating_system/02_process_thread/112_cancellation_point/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [스레드 로컬 저장소](/studynote/02_operating_system/02_process_thread/113_thread_local_storage/) ([TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/), [Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)-Local Storage) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[고아 프로세스 (Orphan Process)]
    |
    v
[스레드 취소 (Thread Cancellation)]
    |
    +---> [취소 점 (Cancellation Point)]
    +---> [스레드 로컬 저장소 (TLS, Thread-Local Storage)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 취소는 "프로그램의 정지 버튼"이에요. 오래 돌고 있는 작업을 멈추고 싶을 때 누르는 거죠.
2. 위험한 방법으로 "즉시 정지"하면 데이터가 망가질 수 있고, 안전한 방법으로 "안전할 때까지 기다렸다 정지"하면 데이터를 안전하게 지킬 수 있어요.
3. 항상 안전한 방법을 쓰고, 작업을 멈추기 전에 꼭 정리(clean up)하는 습관을 들이는 게 중요해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 111 / 800

<- **이전**: [110. 고아 프로세스 (Orphan Process) - 부모가 먼저 종료된 상태 (init 프로세스가 입양)](/studynote/02_operating_system/02_process_thread/110_orphan_process/)
**다음**: [112. 취소 점 (Cancellation Point)](/studynote/02_operating_system/02_process_thread/112_cancellation_point/) ->

---
