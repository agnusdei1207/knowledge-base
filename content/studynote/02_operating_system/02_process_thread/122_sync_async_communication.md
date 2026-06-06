---
title: "Non-blocking"
date: "2026-05-08"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동기식/비동기식 통신은 [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/)에서 송신(Send)과 수신(Receive) 연산이 호출 프로세스를 블로킹(Blocking)시킬 것인지, 논블로킹(Non-blocking)으로 즉시 반환할 것인지에 따라 구분되는 통신 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 모델이다.
> 2. **가치**: 동기식(블로킹) 통신은 구현이 단순하고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장하지만 프로세스의 동시성을 제한하며, 비동기식(논블로킹) 통신은 높은 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))과 시스템 반응성(Responsiveness)을 제공하지만 버퍼 관리와 오류 처리가 복잡해지는 트레이드오프(Trade-off) 관계를 가진다.
> 3. **융합**: 송신/수신 각각에 대해 블로킹/논블로킹을 독립적으로 조합하면 4가지 통신 모드가 도출되며, 이 조합은 `select()`/`poll()`/`epoll()` 같은 I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)), 프로미스(Promise)/퓨처(Future) 기반의 비동기 프로그래밍, 그리고 [이벤트 드리븐 아키텍처](/studynote/04_software_engineering/04_testing_quality/214_eda_event_driven_architecture_async/)([Event-Driven Architecture](/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/))의 근간이 된다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/)에서 송신 연산(`send()`)과 수신 연산(`receive()`)은 각각 블로킹(Blocking, 동기식) 또는 논블로킹(Non-blocking, 비동기식)으로 동작할 수 있다. 블로킹 송신은 메시지가 수신자(또는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 버퍼)에 복사될 때까지 송신자를 대기시키고, 논블로킹 송신은 메시지를 로컬 버퍼에 복사한 후 즉시 반환한다. 블로킹 수신은 메시지가 도착할 때까지 수신자를 대기시키고, 논블로킹 수신은 즉시 반환하되 메시지가 없으면 에러를 반환한다.
- **필요성**: [실시간 시스템](/studynote/02_operating_system/01_overview_architecture/009_real_time_system/)([Real-time System](/studynote/02_operating_system/01_overview_architecture/009_real_time_system/))에서 프로세스가 메시지 수신을 무한히 대기(블로킹)하면 시스템 전체의 응답성이 저하된다. 반대로 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송에서 논블로킹 방식을 사용하면 [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/)([Buffer Overflow](/studynote/02_operating_system/10_security/591_buffer_overflow/))로 인한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 위험이 발생한다. 시스템의 요구사항(실시간성 vs [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/))에 따라 적절한 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 모드를 선택하는 것이 시스템 설계의 핵심 결정이다.

- **등장 배경**: [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 운영체제에서 IPC는 주로 블로킹(동기식) 모드로 구현되었다. 그러나 네트워크 통신의 보급과 [실시간 시스템](/studynote/02_operating_system/01_overview_architecture/009_real_time_system/)의 요구 증대로, 대기 시간 동안 CPU를 낭비하지 않는 비동기(논블로킹) I/O 모델이 필요해졌다. 리눅스의 `O_NONBLOCK` [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), `select()`/`epoll()` 시스템 콜, 그리고 Node.js의 [이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/)([Event Loop](/studynote/02_operating_system/02_process_thread/142_event_loop/))는 이러한 비동기 통신 모델의 발전 과정이다.

```text
  +--------------------------------------------------------------------+
  |       Send/Receive의 4가지 조합에 따른 통신 동기화 모드            |
  +--------------------------------------------------------------------+
  |                                                                    |
  |                |  Blocking Receive   |  Non-blocking Receive       |
  |  --------------+--------------------+-------------------------     |
  |  Blocking Send |  [Mode 1]           |  [Mode 2]                   |
  |  (Synchronous) |  Rendezvous         |  Sender 대기                |
  |                |  (만남의 장소)       |  Receiver 논블로킹         |
  |  --------------+--------------------+-------------------------     |
  |  Non-blocking  |  [Mode 3]           |  [Mode 4]                   |
  |  Send          |  Sender 논블로킹    |  Fully Non-blocking         |
  |  (Asynchronous)|  Receiver 대기       |  (완전 비동기)             |
  |                                                                    |
  |  [Mode 1: Rendezvous]  양쪽 모두 준비될 때까지 대기                |
  |  [Mode 2] Sender는 수신 완료까지 대기, Receiver는 바로 리턴        |
  |  [Mode 3] Sender는 버퍼에 복사 후 리턴, Receiver는 도착까지 대기   |
  |  [Mode 4] 양쪽 모두 즉시 리턴 (콜백/이벤트 기반 처리 필요)         |
  +--------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 2x2 매트릭스는 송신과 수신의 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 속성을 독립적으로 조합하여 도출되는 4가지 통신 모드를 보여준다. <strong>Mode 1 (Rendezvous, 랑데부)</strong>는 송신자와 수신자가 동시에 준비될 때까지 양쪽 모두 대기하는 가장 엄격한 모드다. Ada 프로그래밍 언어의 Rendezvous 개념이 여기서 유래했다. <strong>Mode 2</strong>는 송신자가 [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/) 완료까지 대기하므로 송신 순서가 보장되고, 수신자는 논블로킹이므로 다른 작업을 병행할 수 있다. <strong>Mode 3</strong>는 송신자가 로컬 버퍼에 복사 후 즉시 반환하므로 송신 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 높고, 수신자가 블로킹되므로 메시지 도착을 확실하게 감지할 수 있다. <strong>Mode 4 (Fully Non-blocking)</strong>는 양쪽 모두 대기하지 않으므로 최고의 동시성을 제공하지만, 콜백(Callback)이나 [이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/)([Event Loop](/studynote/02_operating_system/02_process_thread/142_event_loop/))를 통해 메시지 도착을 비동기적으로 감지하는 추가 메커니즘이 필요하다.

- **📢 섹션 요약 비유**: 전화 통화(동기식)는 상대방이 전화를 받을 때까지 기다려야 하지만 확실하게 대화할 수 있고, 문자 메시지(비동기식)는 보내자마자 자기 일을 계속할 수 있지만 나중에 확인해야 하는 trade-off 관계와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 블로킹 vs 논블로킹: 시간선 비교

```text
  +----------------------------------------------------------------------+
  |       블로킹 vs 논블로킹 수신(Receive)의 시간선 비교                 |
  +----------------------------------------------------------------------+
  |                                                                      |
  |  [블로킹 수신 (Blocking Receive)]                                    |
  |  Process                                                             |
  |  --->[recv()]--■ 대기 ■--[메시지 도착]--[처리]---> 계속 작업           |
  |         |                 |                |                         |
  |         |<--- 대기 시간 --->|                |                         |
  |         |  (CPU 유휴)      |                |                        |
  |                                                                      |
  |  [논블로킹 수신 (Non-blocking Receive)]                              |
  |  Process                                                             |
  |  --->[recv()]--->즉시반환(에러)--->[다른 작업]--->[다시 recv()]--->...    |
  |         |        (EAGAIN)              |                             |
  |         +-- 0 시간 대기               +-- CPU 유효 활용              |
  |                                                                      |
  |  [비동기 수신 + 콜백 (Async Receive + Callback)]                     |
  |  Process                                                             |
  |  --->[async_recv(cb)]--->[작업 A]--->[작업 B]--->...                     |
  |         |                                               |            |
  |         +--------- [메시지 도착 시 콜백 cb() 자동 호출] --->[처리]    |
  |                                                                      |
  |  💡 블로킹은 CPU를 낭비하지만 구현이 단순하고,                       |
  |     논블로킹은 CPU를 효율적으로 사용하지만 폴링/콜백이 필요함        |
  +----------------------------------------------------------------------+
```

**[다이어그램 해설]** 블로킹 수신에서 프로세스는 `recv()` 호출 이후 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에 의해 수면(Sleep) 상태로 전환되며, 메시지가 도착하여 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 프로세스를 깨울(Wake-up) 때까지 CPU를 소모하지 않는다. 이는 [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/studynote/02_operating_system/02_process_thread/103_thread_pool/))과 같이 프로세스/[스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 여러 개일 때 유리하다. 대기 중인 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)는 CPU 코어에서 스케줄링 제외되므로 다른 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 코어를 사용할 수 있다. 반면 논블로킹 수신에서 `recv()`는 즉시 반환되므로 프로세스는 대기 시간에 다른 작업을 수행할 수 있지만, 메시지 도착을 확인하기 위해 주기적으로 `recv()`를 반복 호출([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))해야 한다. [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)은 불필요한 CPU 소모를 유발하므로, `epoll()`/`kqueue()` 같은 I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 시스템 콜을 사용하거나 콜백(Callback) 기반의 비동기 프레임워크를 활용하는 것이 현대적인 해결책이다.

### [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)([Buffering](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)) 용량에 따른 동기식 통신의 세 가지 변형

| [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 방식 | 설명 | 송신 동작 | 수신 동작 | 예시 |
|:---|:---|:---|:---|:---|
| <strong>무용량 (<a href="/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/">Zero</a> Capacity)</strong> | 버퍼 없이 직접 전달 (Rendezvous) | 수신자가 준비될 때까지 블로킹 | 송신자가 보낼 때까지 블로킹 | Ada Rendezvous |
| **유한 용량 (Bounded Capacity)** | 고정 크기의 버퍼 | 버퍼가 가득 차면 블로킹 | 버퍼가 비어있으면 블로킹 | POSIX [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/), [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [Socket](/studynote/02_operating_system/02_process_thread/125_socket/) |
| **무한 용량 (Unbounded Capacity)** | 무제한 버퍼 | 항상 논블로킹 (즉시 복사) | 버퍼가 비어있으면 블로킹 | 이상적 모델 (실제로는 구현 불가) |

```text
  +----------------------------------------------------------------------+
  |      버퍼 용량(Capacity)에 따른 3가지 동기식 통신 변형 모델          |
  +----------------------------------------------------------------------+
  |                                                                      |
  |  [무용량 버퍼 (Zero Capacity / Rendezvous)]                          |
  |  Sender --->        (버퍼 없음)        <--- Receiver                   |
  |  블로킹         +--------------+       블로킹                        |
  |  (대기)         | 직접 전달     |       (대기)                       |
  |  -------------->| (handshake)  |<---------------                       |
  |                +--------------+                                      |
  |  * 양쪽 모두 동시에 준비되어야 전달 가능                             |
  |  * 가장 엄격한 동기화. 구현은 단순하지만 대기 비용 큼                |
  |                                                                      |
  |  [유한 용량 버퍼 (Bounded Capacity)]                                 |
  |  Sender --->  +-------------+  ---> Receiver                           |
  |  (buf 비면  | | [M1][M2][M3]| | (buf 있으면                          |
  |   논블로킹, | |  size = N   | |  논블로킹,                           |
  |   buf 꽉이면 | +-------------+ |  buf 비면                           |
  |   블로킹)    |   Bounded Queue  |  블로킹)                           |
  |                                                                      |
  |  * 가장 실용적인 모델. Pipe, Socket 등 대부분의 IPC가 이 방식        |
  |  * 버퍼가 가득 차면 역압(Back-pressure)이 송신자에게 전달됨          |
  |                                                                      |
  |  [무한 용량 버퍼 (Unbounded Capacity)]                               |
  |  Sender --->  +---------------------+  ---> Receiver                   |
  |  항상 논블로킹| | [M1][M2]...[Mn]    | | (buf 비면 블로킹)           |
  |              | | 무한 확장 (이상적)   | |                            |
  |              | +---------------------+ |                             |
  |                                                                      |
  |  * 송신자는 항상 논블로킹 (메모리가 무한하다는 가정)                 |
  |  * 실제로는 구현 불가. 다만 Bounded를 충분히 크게 설정해 근사 구현   |
  +----------------------------------------------------------------------+
```

**[다이어그램 해설]** [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 용량은 동기식 통신의 동작을 결정하는 핵심 파라미터다. 무용량([Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Capacity) 버퍼에서는 랑데부(Rendezvous) 패턴이 발생한다. 이는 악수(Handshake)와 유사하며, 송신자와 수신자가 동시에 통신 지점에 도달해야만 메시지가 전달된다. 유한 용량(Bounded Capacity) 버퍼는 실제 시스템에서 가장 널리 사용되는 모델이다. UNIX [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/))의 기본 버퍼 크기(리눅스에서는 64KB)가 대표적인 예이며, 버퍼가 가득 차면 `send()`가 블로킹되어 자연스럽게 역압(Back-pressure)이 발생한다. 무한 용량(Unbounded Capacity) 버퍼는 이상적 모델이지만, 물리적 메모리가 유한하므로 실제로는 구현할 수 없다. 다만, 디스크 기반 영구 큐(예: [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))를 사용하면 근사적으로 무한 용량을 구현할 수 있다.

- **📢 섹션 요약 비유**: 무용량 버퍼는 '직접 손으로 물건 전달(악수 필요)', 유한 버퍼는 '크기가 정해진 택배 상자(가득 차면 기다려야 함)', 무한 버퍼는 '크기가 무한한 창고(언제든 물건을 넣을 수 있음)'와 같습니다.

---

## Ⅲ. 비교 및 연결

### I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) (I/O [Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))와 비동기 통신의 결합

현대의 고성능 서버는 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 수천 개의 연결을 동시에 처리해야 한다. 이를 위해 비동기 수신을 `select()`/`poll()`/`epoll()` 같은 I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 시스템 콜과 결합한다.

| I/O 모델 | 원리 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 특성 | 적용 사례 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/520_select/">select</a>()</strong> | fd_set 비트마스크로 관심 fd 등록 | O(n) 스캔, fd 수 제한(1024) | 구형 서버, 이식성 우선 |
| **poll()** | 구조체 배열로 관심 fd 등록 | O(n) 스캔, fd 수 무제한 | [select](/studynote/05_database/04_transactions_concurrency/520_select/) 대체 |
| **epoll()** | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 준비된 fd만 반환 | O(1) 통지, 수만 fd 처리 | Nginx, [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) |
| **kqueue()** | BSD 계열의 이벤트 통지 | O(1) 통지 | macOS, FreeBSD |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/464_io_uring/">io_uring</a></strong> | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)-사용자 공간 링 버퍼 | 시스템 콜 최소화 | 차세대 비동기 I/O |

- **📢 섹션 요약 비유**: 식당에서 웨이터 한 명이 100개의 테이블을 동시에 돌봐야 할 때, 매번 모든 테이블을 돌아보며 확인하는 것이 `select()`/`poll()`이고, 주방에서 "3번 테이블 주문 완료!"라고 호출벨이 울릴 때만 가는 것이 `epoll()`과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 -- Nginx의 비동기 논블로킹 <a href="/studynote/02_operating_system/02_process_thread/142_event_loop/">이벤트 루프</a></strong>: Nginx는 마스터 프로세스가 여러 워커 프로세스를 생성하고, 각 워커는 `epoll()` 기반의 [이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/)([Event Loop](/studynote/02_operating_system/02_process_thread/142_event_loop/))를 통해 수만 개의 클라이언트 연결을 단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)로 처리한다. 모든 [소켓](/studynote/02_operating_system/02_process_thread/125_socket/) I/O를 논블로킹(`O_NONBLOCK`) 모드로 설정하여, 각 연결의 대기 시간 동안 다른 연결을 처리할 수 있으므로 C10K([10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000 동시 연결) 문제를 해결한다.

2. <strong>시나리오 -- <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> <a href="/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a>의 동기식 vs 비동기식 전송</strong>: MySQL 마스터-슬레이브 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)에서 동기식 반감기(Semi-synchronous [Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))는 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 커밋 시 적어도 하나의 슬레이브가 바이너리 로그를 수신할 때까지 마스터가 대기(블로킹)하므로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장하지만 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 지연이 발생한다. 비동기식 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)(Asynchronous [Replication](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))는 마스터가 커밋 즉시 응답하므로 지연이 없지만, 장애 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 가능성이 있다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: 시스템의 실시간성 요구사항([타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/))을 분석하여 블로킹/논블로킹 모드를 적절히 선택하였는가? 논블로킹 모드 시 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 루프([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) Loop)에 의한 CPU 낭비를 방지하기 위해 I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)(`epoll()`)를 적용하였는가?
- **운영 보안적**: 비동기 송신 시 로컬 버퍼의 수명(Lifetime)이 [메시지 전달](/studynote/02_operating_system/02_process_thread/119_message_passing/) 완료 후까지 보장되는가? 블로킹 송신에서 수신 프로세스 장애 시 송신자가 영원히 대기하는 데드락([Deadlock](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)) 시나리오에 대비하였는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/">폴링</a> 루프에 의한 CPU 낭비</strong>: 논블로킹 `recv()`를 `while(1)` 루프 안에서 무조건 반복 호출하면, 메시지가 도착하지 않은 동안에도 CPU 코어를 100% 점유하며 시스템 반응성이 저하된다(Spin-wait [Anti-pattern](/studynote/11_design_supervision/03_gof_creational_structural/161_anti_pattern/)). 반드시 `epoll_wait()`나 `usleep()` 같은 대기 메커니즘과 결합해야 한다.

- **📢 섹션 요약 비유**: 냉장고 문을 계속 열어보며 음식이 생겼는지 확인하는 것([폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/))은 전기를 낭비하지만, 냉장고에 알림 벨을 달아두고 음식이 들어오면 소리가 나게 하는 것(epoll)이 훨씬 효율적인 것과 같습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 동기식 (블로킹) | 비동기식 (논블로킹) | 선택 기준 |
|:---|:---|:---|:---|
| **정량** | 대기 시간 CPU 유휴 | 대기 시간 CPU 유효 활용 | CPU 활용률 |
| **정량** | 1 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) = 1 연결 | 1 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) = N 연결 | 동시 연결 수 |
| **정성** | 구현 단순, 버그 적음 | 구현 복잡, 콜백 지옥 | 개발 복잡도 |
| **정성** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보장 | 순서 보장 어려울 수 있음 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) |

### 미래 전망
- <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/464_io_uring/">io_uring</a> (Linux 5.1+)</strong>: 시스템 콜 오버헤드를 극소화하는 차세대 비동기 I/O 프레임워크. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 사용자 공간 간에 링 버퍼(Ring Buffer)를 공유하여, 시스템 콜 호출 없이 비동기 I/O를 제출하고 완료를 확인할 수 있다.
- **async/await 패턴**: [Rust](/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/), C++20, JavaScript 등 현대 프로그래밍 언어는 `async/await` 문법을 통해 비동기 통신의 복잡성(콜백 지옥)을 동기식 코드와 동등한 가독성으로 해결하고 있다.

### 참고 표준
- **IEEE Std 1003.1 (POSIX.1)**: `O_NONBLOCK` [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), `fcntl()`, `select()`, `poll()` 비동기 I/O 표준.
- <strong>Linux <code>epoll(7)</code></strong>: 고성능 I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 시스템 콜. `epoll_create()`, `epoll_ctl()`, `epoll_wait()` [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/).

동기식/비동기식 통신은 [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) 설계에서 가장 근본적인 트레이드오프인 '단순성 vs [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)'을 결정하는 핵심 모델이다. 블로킹은 직관적이고 안전하지만 동시성을 제한하며, 논블로킹은 높은 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공하지만 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/), 콜백, 버퍼 관리라는 추가적인 복잡도를 수반한다. 현대 시스템은 `epoll()`/`io_uring` 같은 I/O [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) 기법과 `async/await` 패턴을 통해 이 두 모델의 장점을 융합하고 있다.

- **📢 섹션 요약 비유**: 자동차의 자동변속기(비동기식)는 운전자가 기어를 직접 바꿀 필요 없이 엔진 RPM에 맞춰 자동으로 최적의 기어를 선택하듯이, 비동기 통신은 시스템이 메시지의 도착 여부를 자동으로 감지하여 CPU를 가장 효율적으로 사용하는 지능적인 통신 방식입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [직접 통신](/studynote/02_operating_system/02_process_thread/120_direct_communication/) ([Direct Communication](/studynote/02_operating_system/02_process_thread/120_direct_communication/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [간접 통신](/studynote/02_operating_system/02_process_thread/121_indirect_communication/) ([Indirect Communication](/studynote/02_operating_system/02_process_thread/121_indirect_communication/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/) ([Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [지명 파이프](/studynote/02_operating_system/02_process_thread/124_named_pipe_fifo/) (Named [Pipe](/studynote/02_operating_system/02_process_thread/123_pipe/) / [FIFO](/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[간접 통신 (Indirect Communication)]
    |
    v
[동기식 통신 (Blocking) vs 비동기식 통신 (Non-blocking)]
    |
    +---> [파이프 (Pipe)]
    +---> [지명 파이프 (Named Pipe / FIFO)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구에게 편지를 보내고 답장이 올 때까지 아무것도 못 하고 가만히 기다리는 것이 '동기식 통신(블로킹)'이에요.
2. 편지를 우체통에 넣어두고 다른 놀이를 하다가, 나중에 답장이 왔다는 알림을 받고 확인하는 것이 '비동기식 통신(논블로킹)'이에요.
3. 비동기식이 더 많은 일을 동시에 할 수 있어서 멋지지만, 답장이 왔는지 계속 확인해야 하니까 조금 더 신경 써야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 800

<- **이전**: [121. 간접 통신 (Indirect Communication) - 메일박스/포트 사용](/studynote/02_operating_system/02_process_thread/121_indirect_communication/)
**다음**: [123. 파이프 (Pipe) - 단방향(Half-duplex), 부모-자식 간](/studynote/02_operating_system/02_process_thread/123_pipe/) ->

---
