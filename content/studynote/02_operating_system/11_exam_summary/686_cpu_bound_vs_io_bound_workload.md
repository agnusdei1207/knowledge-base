---
title: "686. CPU 바운드 vs I/O 바운드 (CPU Bound Vs I/O Bound Workload)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컴퓨터에서 실행되는 모든 프로세스는 그 성격에 따라, 연산에 시간을 쏟는 **CPU 바운드(Bound)** 프로세스와, 디스크나 네트워크 등 외부 장치를 기다리는 데 시간을 쏟는 **I/O 바운드** 프로세스로 나뉜다.
> 2. **스케줄링의 딜레마**: I/O 바운드 프로세스는 응답 속도(Interactive)가 중요하므로 깨어날 때마다 CPU를 즉시 줘야 하지만 한 번 잡으면 금방 놓는다. 반면 CPU 바운드는 한 번 CPU를 잡으면 할당 시간(Time [Quantum](/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/))을 꽉 채워서 다른 앱들을 버벅거리게 만든다.
> 3. **가치/튜닝**: 시스템 아키텍트는 서버가 터졌을 때 "이 워크로드가 CPU 바운드인가, I/O 바운드인가?"를 정확히 진단해야 한다. 원인에 따라 CPU 클럭을 높일지([Scale-up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)), [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 늘리거나 비동기로 뺄지([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)/Async) 처방전이 180도 달라지기 때문이다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - **CPU Burst (버스트)**: 프로세스가 CPU를 잡고 미친 듯이 연산만 수행하는 연속적인 시간 구간.
  - **I/O Burst**: 프로세스가 디스크에서 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 읽거나 네트워크 패킷을 기다리며 대기(Block/Sleep)하는 시간 구간.
  - 프로세스의 일생은 [CPU 버스트 $\rightarrow$ I/O 버스트 $\rightarrow$ CPU 버스트 $\rightarrow$ I/O 버스트]의 끝없는 반복이다.

- **CPU 바운드 프로세스**:
  - I/O 버스트보다 **CPU 버스트가 압도적으로 긴** 프로그램.
  - 예: 동영상 인코딩, 3D 렌더링, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 학습, 비트코인 채굴, 무한 루프.

- **I/O 바운드 프로세스**:
  - CPU 버스트는 아주 짧고, **I/O 버스트(대기 시간)가 압도적으로 긴** 프로그램.
  - 예: 카카오톡(사용자 키보드 대기), 웹 브라우저, 웹 서버(DB와 네트워크 대기), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 복사 프로그램.

- <strong>필요성 (<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a>의 편애)</strong>:
  - OS [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 두 프로세스를 똑같이 대우하면 시스템이 엉망이 된다. 동영상 인코딩(CPU 바운드)이 CPU를 꽉 잡고 안 놔주면, 사용자가 카카오톡(I/O 바운드)에 글자를 쳤을 때 3초 뒤에나 글자가 찍힌다(응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)).
  - **해결책**: OS는 불공평해야 한다. 사용자와 소통하는 **I/O 바운드 프로세스의 우선순위를 강제로 높여주어(Boost)**, 이들이 키보드 입력을 받는 즉시 CPU를 새치기(Preempt)하게 만들어야 시스템이 부드럽게 돌아간다.

  - **CPU 바운드 (수학자)**: 밥(I/O)도 안 먹고 방에 틀어박혀 하루 종일 칠판에 수학 공식만 푸는 사람. 방해하면 싫어함.
  - **I/O 바운드 (택배 상하차 직원)**: 1분 일하고(CPU), 트럭이 올 때까지 10분을 앉아서 쉰다(I/O). 대신 트럭이 오면 즉시 벌떡 일어나서 상자를 내려야 한다.
  - **OS의 역할**: 트럭이 도착했을 때, 수학자를 잠깐 밀어내고 상하차 직원이 바로 일할 수 있게 자리를 마련해 준다.

- **📢 섹션 요약 비유**: CPU 바운드는 마라톤 선수고 I/O 바운드는 100m 단거리 선수입니다. 트랙(CPU)을 관리하는 심판(OS)은 단거리 선수가 뛰고 싶어 할 땐 즉시 트랙을 비워주고, 그가 쉴 때 마라톤 선수가 오랫동안 트랙을 쓰게 해주는 지혜를 발휘해야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CPU Burst Cycle의 통계적 분포

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 학자들이 전 세계의 수많은 프로그램을 분석해 보니, CPU 버스트 길이는 지수 분포(Exponential Distribution)를 따랐다.

```text
  +-------------------------------------------------------------------+
  |                 CPU Burst 길이의 확률 분포 그래프                     |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  빈도수(빈번함)                                                       |
  |   ^                                                               |
  |   |  * (짧은 CPU Burst가 압도적으로 많음 = I/O Bound)                  |
  |   |  * *                                                          |
  |   |  *   *                                                        |
  |   |  *     *                                                      |
  |   |  *       * *                                                  |
  |   |  *           * * * *      (긴 CPU Burst는 매우 드묾 = CPU Bound)|
  |   |  *                   * * * * * * * * * * *                    |
  |   +---------------------------------------------------------->     |
  |      1ms   10ms        50ms                    1000ms    CPU 시간  |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 세상에 존재하는 90%의 프로그램은 아주 잠깐(1ms) 연산하고 I/O를 기다리러 떠난다(I/O Bound). 반면, 한 번 CPU를 잡으면 수백 ms 동안 안 놓는 무거운 프로그램(CPU Bound)은 극소수다. <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a>의 목표는 이 다수의 I/O 바운드 프로세스들이 "응답 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>"을 느끼지 않게, 소수의 CPU 바운드 프로세스로부터 지켜내는 것</strong>이다.

---

### [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 I/O 바운드 판별 및 보상 메커니즘

OS [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)(CFS나 [MLFQ](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/))는 이 프로세스가 CPU 바운드인지 I/O 바운드인지 처음에는 모른다. 과거의 행동(History)을 보고 판단한다.

1. **감시**: 프로세스 A에게 타임 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)(예: 10ms)를 줬다.
2. **I/O Bound 판별**: 프로세스 A가 1ms만 쓰고 "나 디스크 읽을게" 하고 스스로 CPU를 반납(Sleep)했다.
   - OS의 판단: "아, 얘는 I/O 바운드구나! 착하네."
   - 조치: **우선순위 승격 (Priority Boost)**. 나중에 디스크 읽기가 끝나고 깨어났을 때, 남들 다 제치고 1순위로 CPU를 주어 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)을 극대화한다.
3. **CPU Bound 판별**: 프로세스 B에게 10ms를 줬더니, 시간을 끝까지 다 채워서 OS가 강제로 뺏을 때까지 연산만 했다.
   - OS의 판단: "너는 CPU 바운드(욕심쟁이)구나."
   - 조치: **우선순위 강등 (Penalty)**. 대신 한 번 CPU를 잡았을 때 길게 쓰도록 타임 퀀텀을 넉넉히(예: 50ms) 주어 [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드라도 줄여준다.

- **📢 섹션 요약 비유**: 뷔페(CPU)에서 한 접시만 뚝딱 먹고 나가는 손님(I/O 바운드)에게는 다음번에 오면 프리패스로 줄을 안 서게 해주고, 하루 종일 앉아서 먹는 손님(CPU 바운드)은 구석 자리로 몰아서 시간제한을 두는 것이 OS의 합리적 차별입니다.

---

## Ⅲ. 비교 및 연결

### CPU Bound vs I/O Bound [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

서버가 느려졌을 때, 병목의 원인에 따라 처방은 완전히 다르다.

| 구분 | CPU Bound 워크로드 | I/O Bound 워크로드 |
|:---|:---|:---|
| **병목 지점** | CPU 연산력 (클럭, 코어 수) | 디스크 속도, [네트워크 지연](/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/), DB 락([Lock](/studynote/05_database/04_transactions_concurrency/510_lock/)) |
| <strong><a href="/studynote/02_operating_system/02_process_thread/103_thread_pool/">스레드 풀</a> 크기</strong> | **코어 수와 동일하게 (예: 16코어 = 16개)** | **코어 수의 수십 배 (예: 16코어 = 200개)** |
| <strong><a href="/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/">다중 프로그래밍</a></strong> | 오히려 낮춰야 함 (스위칭 오버헤드 방지) | 무조건 높여야 함 (CPU가 쉬는 걸 막기 위해) |
| <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a> <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | [Scale-Up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) (고성능 CPU로 교체) | [Scale-Out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) (서버 대수 늘리기), 비동기 I/O 전환 |
| **적용 사례** | 암호화 화폐 채굴, 이미지 딥러닝 | 웹 서버(Nginx), [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이, DB 서버 |

### 과목 융합 관점

- **소프트웨어공학 (SE)**: Node.js나 Python의 asyncio 같은 '단일 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 비동기 [이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/)' 모델은 철저하게 **I/O 바운드** 워크로드에 특화된 아키텍처다. I/O 대기 시간에 다른 요청을 처리해 효율이 극강이다. 하지만 이 서버에 CPU 바운드(예: 1GB [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 파싱) 요청이 하나라도 들어오면, [이벤트 루프](/studynote/02_operating_system/02_process_thread/142_event_loop/) 자체가 블로킹되어 수만 명의 다른 I/O 요청이 전부 멈춰버리는 대참사가 터진다.
- <strong><a href="/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/">클라우드 컴퓨팅</a> (Cloud)</strong>: AWS EC2 인스턴스를 고를 때, C 계열(Compute Optimized)은 CPU 바운드 연산용이고, I 계열(I/O Optimized)이나 M 계열(General)은 I/O 바운드에 적합하다. 앱의 바운드 성향을 모른 채 아무 인스턴스나 띄우면 매달 수천만 원의 클라우드 요금이 낭비된다.

- **📢 섹션 요약 비유**: 화물차(서버)가 느리다고 무작정 엔진(CPU)을 바꾸면 안 됩니다. 짐이 무거워서(CPU Bound) 느린 거면 엔진을 바꿔야 하지만, 상하차 알바생이 느려서(I/O Bound) 차가 못 떠나는 거라면 알바생을 더 고용([스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/) 증가)해야 합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 톰캣(Tomcat) <a href="/studynote/02_operating_system/02_process_thread/103_thread_pool/">스레드 풀</a> 튜닝 실패로 인한 <a href="/studynote/02_operating_system/04_synchronization/257_thrashing/">스래싱</a></strong>: 16코어 서버에서 돌아가는 자바 스프링 기반 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버(I/O Bound). 초보 개발자가 "[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이겠다"며 [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/)(MaxThreads)을 200에서 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000으로 무작정 늘려버림.
   - **원인 분석**: I/O 바운드 앱은 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 넉넉히 주는 게 맞다. 하지만 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개는 선을 넘었다. DB 병목으로 인해 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000개의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 모두 I/O 대기에 빠졌다가 DB 응답이 오는 순간 동시에 깨어난다(Thundering Herd). CPU 코어 16개가 1만 개의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)([Context Switch](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))하느라 시스템 전체 CPU가 100%를 치고(Sys time 폭주), 정작 앱 연산(User time)은 0%가 되는 [스래싱](/studynote/02_operating_system/04_synchronization/257_thrashing/)([Thrashing](/studynote/02_operating_system/04_synchronization/257_thrashing/)) 늪에 빠졌다.
   - **대응 (기술사적 가이드)**: Little's Law 등 대기열 이론을 바탕으로 적정 [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/)을 산정해야 한다. 이상적인 [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/) 공식: `Threads = CPU 코어 수 * (1 + (I/O 대기 시간 / CPU 처리 시간))`. 만약 이 공식을 넘어서는 동시 접속(10K)을 처리해야 한다면, 전통적인 톰캣 멀티스레드 모델을 버리고 Netty나 Spring WebFlux 같은 비동기(Non-blocking I/O) 프레임워크로 아키텍처를 전면 전환해야 한다.

2. <strong>시나리오 — 배달 앱의 <a href="/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a> 추천 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 응답 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a> (CPU Bound 침범)</strong>: 배달 앱 홈 화면을 띄울 때 사용자에게 맞는 가게를 딥러닝으로 추천해 주는 API를 호출한다. 이 API가 들어있는 마이크로서비스가 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 3초나 걸려 홈 화면이 마비됨.
   - **원인 분석**: [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 추론(Inference)은 완벽한 **CPU 바운드** 작업이다. 이 무거운 CPU 바운드 로직을, 일반적인 웹 라우팅과 DB 조회를 담당하는 I/O 바운드 노드([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))에 섞어서 올려놓았다. [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 연산이 CPU 타임 [슬라이스](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)를 길게 독점해 버리면서, 가벼운 I/O 요청들의 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 다 같이 늦어진 것이다.
   - **아키텍처 적용 (워크로드 격리)**: I/O 바운드 서비스와 CPU 바운드 서비스는 절대 같은 노드(또는 같은 [스레드 풀](/studynote/02_operating_system/02_process_thread/103_thread_pool/))에 섞어 쓰면 안 된다. [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 추천 로직을 별도의 컨테이너로 분리(Decoupling)하여 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 인스턴스나 Compute 전용 노드 그룹으로 격리 스케줄링해야 한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 워크로드 특성(CPU vs I/O) 기반 아키텍처 의사결정 플로우    |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [서버 성능 모니터링 툴(top, vmstat)을 통한 병목 확인]                      |
  |                |                                                  |
  |                v                                                  |
  |      `top`에서 CPU의 `%us`(유저)가 90% 이상이고 `%wa`(I/O 대기)는 0인가?    |
  |          +- 예 ------> [명확한 CPU Bound 워크로드]                   |
  |          |            대책 1: 로직 알고리즘 자체의 시간 복잡도(O(n)) 개선     |
  |          |            대책 2: Scale-Up (CPU 클럭/코어 수 높은 장비로 마이그레이션)|
  |          +- 아니오                                                |
  |                |                                                  |
  |                v                                                  |
  |      CPU 사용률은 20% 이내인데, `%wa`(Wait)가 높거나 스레드들이 다 자고 있는가?|
  |          +- 예 ------> [명확한 I/O Bound 워크로드]                   |
  |          |            대책 1: I/O 병목 지점(DB 쿼리, 외부 API 네트워크) 튜닝|
  |          |            대책 2: 스레드 풀 증가 또는 비동기(Async) 아키텍처 적용 |
  |          |                                                        |
  |          +- 아니오 ---> 메모리 스왑(Swapping)이나 락(Lock) 경합 문제 의심 |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 초보자는 서버가 느리면 "서버 사양(CPU)을 올립시다"라고 한다. 하지만 I/O 바운드 병목(DB가 느림)일 때 웹 서버의 CPU를 100코어짜리로 바꿔봤자 속도는 1ms도 빨라지지 않는다. 기술사는 모니터링 지표를 보고 현재의 워크로드가 CPU 바운드인지 I/O 바운드인지 단번에 갈라내어 엉뚱한 곳에 돈을 쓰지 않도록 막는 사람이다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>적응형 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a> 튜닝</strong>: 리눅스의 CFS [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 이 두 가지 바운드를 스스로 판단하여 공평하게 조절한다. 하지만 백그라운드 영상 인코딩(CPU Bound) 때문에 마우스가 끊긴다면, 해당 [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) 프로세스의 `nice` 값을 19로 낮추어(우선순위 강등) OS의 판단을 돕는 수동 튜닝을 거쳤는가?

- **📢 섹션 요약 비유**: CPU 바운드는 소화불량이고, I/O 바운드는 영양실조입니다. 소화가 안 돼서(CPU 과부하) 배가 아픈 환자에게 밥을 더 주거나, 영양실조(I/O 대기) 환자에게 소화제를 먹이는 오진을 피하는 것이 진단(모니터링)의 핵심입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 성향을 무시한 아키텍처 | CPU/I/O Bound 분리 및 맞춤 아키텍처 | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>)</strong> | I/O 병목으로 CPU [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 사용 | 비동기 적용으로 CPU 80% 활용 | 동일 하드웨어 대비 TPS 5배 이상 증가 |
| <strong>정량 (<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>)</strong>| CPU 로직 혼재로 화면 멈춤 발생 | 워크로드 격리로 즉각적 I/O 반응 | P99 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)(Tail [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 대폭 감소 |
| **정성 (비용 효율)**| 원인 모를 Scale-up으로 돈 낭비 | 병목 구간(DB, 네트워크) 정확히 타격 | 클라우드 인프라 유지보수 비용([TCO](/studynote/12_it_management/01_governance_strategy/016_tco/)) 최적화 |

### 미래 전망
- <strong>이기종(<a href="/studynote/05_database/05_distributed_nosql_newsql/273_heterogeneous_db/">Heterogeneous</a>) 프로세싱의 가속</strong>: CPU 바운드 연산 중에서도 단순 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 계산(행렬 곱 등)은 CPU가 하기엔 비효율적이다. 이런 극단적 CPU 바운드 연산을 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/), [TPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/425_tpu/) 같은 특수 목적 가속기로 덜어내어([Offloading](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)), 메인 CPU는 순수하게 I/O 바운드와 스케줄링(제어)에만 집중하게 만드는 것이 현대 모바일 칩셋(Apple Silicon 등)과 클라우드 서버의 지배적인 발전 방향이다.
- <strong>eBPF를 이용한 실시간 워크로드 <a href="/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong>: 단순히 프로세스 단위로 I/O 성향을 나누는 것을 넘어, 패킷 단위나 시스템 콜 단위로 eBPF가 실시간 프로파일링을 수행하여, "현재 이 컨테이너는 10초간 CPU 바운드 모드다"라고 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)에게 힌트를 주어 동적으로 정책을 바꾸는 지능형 OS가 연구되고 있다.

### 결론
CPU 바운드와 I/O 바운드는 모든 소프트웨어의 성격을 규정하는 가장 근본적인 두 가지 유전자다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 스케줄링 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 역사([FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) $\rightarrow$ [RR](/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) $\rightarrow$ [MLFQ](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) $\rightarrow$ CFS)는 결국 "어떻게 하면 소수의 탐욕스러운 CPU 바운드로부터 다수의 불쌍한 I/O 바운드를 지켜내어 사용자를 답답하지 않게 만들 것인가?"에 대한 투쟁의 역사였다. 소프트웨어 아키텍트가 자신이 만든 코드의 유전자가 어느 쪽인지 모른다면, 그 어떤 화려한 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템을 구축하더라도 결국 병목의 늪에서 허우적대게 될 것이다.

- **📢 섹션 요약 비유**: 물(I/O 바운드)과 기름(CPU 바운드)은 섞일 수 없습니다. 이 둘을 한 컵(서버)에 억지로 저어서 섞으려 하지 말고, 물은 넓은 수로(비동기 I/O)로 흐르게 하고 기름은 화로(고성능 코어)에서 타오르게 분리하는 것이 가장 위대한 시스템 연금술입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [단기 스케줄러 디스패치](/studynote/02_operating_system/11_exam_summary/685_short_term_scheduler_dispatcher/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 선점 / [비선점](/studynote/02_operating_system/05_deadlock/285_no_preemption/) 스케줄링 차이 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) [호위 효과](/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/) ([Convoy Effect](/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[단기 스케줄러 디스패치]
    |
    v
[CPU 바운드 vs I/O 바운드 (CPU Bound Vs I/O Bound Workload)]
    |
    +---> [선점 / 비선점 스케줄링 차이]
    +---> [FCFS 호위 효과 (Convoy Effect)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 세상에는 두 종류의 프로그램이 있어요. 방에 틀어박혀 하루 종일 10시간 동안 수학 문제만 푸는 '공부벌레(CPU 바운드)'와, 1분 일하고 10분 동안 택배 오기를 기다리며 쉬는 '택배 요정(I/O 바운드)'이에요.
2. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 선생님이 보기에, 택배 요정은 금방 일하고 비켜주니까 택배가 왔을 때 바로 1등으로 일하게 해줘요(응답 속도 최고).
3. 반면 공부벌레는 한 번 자리를 잡으면 안 비켜주니까, 다른 애들이 못 놀잖아요? 그래서 선생님은 공부벌레를 구석 자리로 보내고 한 번에 1시간씩 넉넉히 풀게 하되, 택배 요정이 오면 무조건 자리를 양보하게 만든답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 686 / 800

<- **이전**: [685. 단기 스케줄러 디스패치 (Short Term Scheduler Dispatcher)](/studynote/02_operating_system/11_exam_summary/685_short_term_scheduler_dispatcher/)
**다음**: [687. 선점 / 비선점 스케줄링 차이 (Preemptive Vs Non Preemptive Scheduling)](/studynote/02_operating_system/11_exam_summary/687_preemptive_vs_non_preemptive_scheduling/) ->

---
