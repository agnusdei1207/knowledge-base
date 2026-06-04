---
title: "165. CPU 바운드 프로세스 (CPU Bound Process)"
date: "2026-03-22"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CPU 바운드 프로세스 (CPU Bound [Process](/studynote/12_it_management/05_security_compliance/943_process/))는 입출력 (Input/Output, I/O) 대기보다 중앙 처리 장치 (Central Processing Unit, CPU) 연산 구간이 훨씬 길어, 실행 시간 대부분을 계산에 쓰는 작업이다.
> 2. **가치**: 이런 프로세스는 긴 CPU 버스트 (CPU Burst) 동안 캐시 지역성 (Cache Locality)을 살려 전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 높이지만, 응답성 중심 workload와 섞이면 선점 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 서툴 때 체감 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 크게 만든다.
> 3. **판단 포인트**: 핵심은 "우선순위를 낮출 것인가"보다 "얼마나 길게 실행시켜 [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 비용을 상쇄할 것인가"와 "다른 작업을 굶기지 않게 공정성을 어떻게 회복할 것인가"다.

---

## Ⅰ. 개요 및 필요성

CPU 바운드 프로세스는 실행 구간 대부분을 계산에 쓰는 프로세스다. 과학 계산, 영상 인코딩, [압축](/studynote/02_operating_system/06_memory_management/347_compaction/), 암호화, 대규모 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 처리처럼 데이터가 메모리나 장치에서 준비된 뒤에는 오랫동안 CPU를 붙잡고 연산을 계속한다. 따라서 병목은 디스크나 네트워크보다 연산 자원과 캐시 효율에 더 가깝다.

이 개념이 중요한 이유는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 모든 작업을 같은 방식으로 다루면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표가 충돌하기 때문이다. CPU 바운드 작업은 자주 끊을수록 [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 비용과 캐시 미스가 늘어 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 나빠지고, 반대로 너무 오래 독점시키면 대화형 작업의 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 급격히 늘어난다. 그래서 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 "긴 계산은 묵직하게 밀어 주되, 반응성은 보호하는 균형점"을 찾아야 한다.

이 그림은 CPU 바운드 프로세스의 시간 사용 패턴을 보여준다.

```text
+--------------------------------------------------------------+
|       CPU 바운드의 시간 패턴: 오래 계산하고 가끔만 기다린다     |
+--------------------------------------------------------------+
| CPU Bound : [████████████████] [▒] [██████████████]          |
| I/O Bound : [██] [▒▒▒▒▒▒▒▒▒▒] [██] [▒▒▒▒▒▒▒▒▒▒▒]             |
|                                                              |
| █ = CPU Burst     ▒ = I/O Wait                               |
+--------------------------------------------------------------+
```

그림의 요점은 CPU 사용률이 높다는 사실 자체보다, 한 번 실행되면 꽤 오랫동안 같은 코어와 캐시를 활용한다는 점이다. 그래서 CPU 바운드 작업은 짧은 응답보다 긴 계산 구간의 연속성이 더 중요하다.

- **📢 섹션 요약 비유**: CPU 바운드 프로세스는 한 번 문제를 풀기 시작하면 오래 집중하는 학생과 같다. 자꾸 말을 걸면 진도는 안 나가고, 너무 오래 혼자 두면 다른 학생이 질문할 차례를 잃는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CPU 바운드 프로세스는 보통 `Ready -> Running -> Ready`를 반복하며, I/O 호출로 스스로 잠들기보다 타임 퀀텀 (Time [Quantum](/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/)) 만료나 선점으로 CPU를 반납하는 경우가 많다. 즉 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 입장에서 이들은 "자발적으로 물러나는 작업"이 아니라, 외부 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 멈춰 세워야 하는 작업에 가깝다. 그래서 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 타이머 인터럽트와 우선순위 보정 장치를 통해 연산 독점을 관리한다.

| 특성 | CPU 바운드 프로세스의 모습 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향 | 스케줄링 의미 |
| :-- | :-- | :-- | :-- |
| CPU Burst 길이 | 길고 연속적 | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)에 유리 | 너무 짧게 자르면 손해 |
| I/O 대기 비중 | 낮음 | 장치 활용보다 연산 집중 | 스스로 Block 되지 않음 |
| 캐시 지역성 | 높아지기 쉬움 | 오래 돌릴수록 유리 | 불필요한 선점이 비용 증가 |
| 체감 목표 | 총 실행 시간 단축 | 배치 작업 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 중요 | 응답성 우대 대상은 아님 |

이 그림은 왜 퀀텀 길이가 CPU 바운드 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 직접 영향을 주는지 보여준다.

```text
+--------------------------------------------------------------+
|     퀀텀 선택의 딜레마: 너무 짧아도, 너무 길어도 문제           |
+--------------------------------------------------------------+
| 짧은 퀀텀 : [Run][Switch][Run][Switch][Run][Switch]          |
|              +- cache warm-up 반복, 처리량 손실               |
|                                                              |
| 긴 퀀텀   : [Run------------------------------]               |
|              +- 처리량 유리, 그러나 대화형 응답 지연 가능      |
+--------------------------------------------------------------+
```

현대 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 이 딜레마를 정적 우선순위 하나로 풀지 않는다. [다단계 피드백 큐](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) (Multilevel Feedback [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/), [MLFQ](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/))는 CPU를 오래 쓰는 작업을 아래 큐로 내리되 긴 실행 시간을 보장하고, [완전 공정 스케줄러](/studynote/02_operating_system/03_cpu_scheduling/202_cfs_completely_fair_scheduler/) (Completely Fair Scheduler, CFS)는 [가상 실행 시간](/studynote/02_operating_system/03_cpu_scheduling/203_virtual_runtime_vruntime/) (virtual runtime)을 기준으로 공정성을 회복한다. 결국 핵심은 CPU 바운드 작업을 "벌주는 것"이 아니라, 전체 시스템 안에서 적절한 실행 폭을 배정하는 것이다.

- **📢 섹션 요약 비유**: CPU 바운드 스케줄링은 큰 화물을 싣고 가는 트럭을 고속도로에 올리는 일과 같다. 너무 자주 세우면 연료만 낭비하고, 너무 오래 단독 차로를 주면 승용차들이 막힌다.

---

## Ⅲ. 비교 및 연결

CPU 바운드와 I/O 바운드는 서로 반대 개념이지만, 실제 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설계는 둘 중 어느 쪽이 더 중요하냐를 고르는 문제가 아니다. CPU 바운드는 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 캐시 효율을, I/O 바운드는 응답성과 장치 병렬성을 대표한다. 따라서 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 긴 계산을 존중하면서도 짧은 상호작용이 굶지 않게 해야 한다.

| 항목 | CPU 바운드 프로세스 | I/O 바운드 프로세스 |
| :-- | :-- | :-- |
| 주 병목 | 연산 자원, 코어 수, 캐시 | 디스크, 네트워크, 사용자 입력 |
| CPU 사용 패턴 | 길고 연속적 | 짧고 빈번함 |
| 중요한 지표 | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 총 실행 시간 | [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/), 대기 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| 유리한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 긴 실행 구간 보장, 코어 친화도 | 빠른 재스케줄, 비동기 I/O |

이 차이는 인프라 배치 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에도 이어진다. 예를 들어 웹 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버와 영상 인코딩 배치를 같은 노드에 섞으면, 인코딩 작업이 코어와 마지막 단계 캐시 (Last Level Cache, [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/))를 오래 점유해 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 늘 수 있다. 반대로 연산 전용 노드에 CPU 바운드 작업을 몰아두면, 캐시 오염과 노이즈 네이버 (Noisy Neighbor) 문제를 줄이고 배치 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 예측하기 쉬워진다.

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 밖으로 확장하면, 컴파일러는 반복문 전개와 벡터화를 통해 CPU 바운드 구간을 더 효율적으로 만들고, 하드웨어는 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수준 병렬성 ([Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)-Level Parallelism, ILP)과 다중 코어로 이를 받쳐 준다. 즉 CPU 바운드는 단순 프로세스 분류가 아니라, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)·컴파일러·마이크로아키텍처가 함께 최적화하는 축이다.

- **📢 섹션 요약 비유**: CPU 바운드는 오래 볶아야 맛이 나는 소스이고, I/O 바운드는 주문과 배달이 중요한 서비스다. 주방과 홀의 속도가 다르니 같은 규칙으로만 운영하면 식당 전체가 꼬인다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 CPU 바운드 특성은 배치 분석, 영상 인코딩, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 학습, 암호화 서비스에서 자주 드러난다. 예를 들어 16코어 서버에서 H.265 인코딩 작업이 각 코어를 95% 이상 점유한 채 수십 분간 지속된다면, 문제는 I/O 대기가 아니라 코어 수, [SIMD](/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) (Single [Instruction](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 활용, 캐시 효율이다. 이때 웹 서비스와 같은 노드에 두면 평균 CPU 사용률보다 훨씬 큰 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 악화를 만들 수 있다.

따라서 설계 판단은 분명해야 한다. 첫째, 대화형 서비스와 CPU 바운드 배치는 노드 풀이나 cgroup (control group)으로 분리하는 편이 안전하다. 둘째, [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 튜닝은 무조건 우선순위를 낮추는 방향보다 최소 실행 시간과 CPU 친화도 ([CPU Affinity](/studynote/02_operating_system/02_process_thread/144_cpu_affinity/))를 조정해 캐시 재사용을 살리는 방향이 효과적이다. 셋째, 평균 CPU 사용률만 보지 말고 [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 수, run [queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) 길이, [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) miss 비율, tail latency를 함께 봐야 진짜 병목을 읽을 수 있다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 평균 CPU Burst가 타임 퀀텀보다 충분히 긴가?
2. [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 증가가 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 손실과 캐시 미스로 이어지고 있지 않은가?
3. 대화형 서비스와 배치 연산을 같은 코어 풀에서 경쟁시키고 있지 않은가?
4. CPU [quota](/studynote/02_operating_system/09_file_system/551_quota_disk_limit/), nice 값, [affinity](/studynote/02_operating_system/11_exam_summary/778_process_affinity_scheduling_pinning/) 설정이 workload 목표와 맞는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CPU 바운드 병목을 네트워크 문제로 오인해 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수만 계속 늘리는 대응
- 응답성 문제를 막겠다며 퀀텀을 지나치게 줄여 전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 무너뜨리는 튜닝

- **📢 섹션 요약 비유**: CPU 바운드 운영은 마라톤 선수와 단거리 선수를 같은 레인에 세우는 경기 운영과 같다. 각자 뛰는 방식이 다르니 훈련장과 페이스 조절 규칙도 달라야 한다.

---

## Ⅴ. 기대효과 및 결론

CPU 바운드 프로세스를 정확히 이해하면 스케줄링을 단순한 우선순위 경쟁이 아니라, 연산 연속성과 시스템 응답성의 균형 문제로 볼 수 있다. 그 결과 배치 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), 캐시 효율, 코어 배치 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 노드 격리 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 같은 그림 안에서 설명할 수 있다. 특히 I/O 바운드 중심 서비스와 혼재된 환경에서 어떤 작업을 어디에 배치해야 하는지도 더 명확해진다.

다만 CPU 바운드라는 꼬리표는 절대적이지 않다. 같은 프로그램도 입력 크기와 단계에 따라 I/O 바운드 구간과 CPU 바운드 구간을 번갈아 보일 수 있다. 따라서 중요한 것은 이름을 붙이는 일이 아니라, 실제로 CPU Burst 길이와 병목 자원을 측정하고 그에 맞는 스케줄링·격리·튜닝 결정을 내리는 일이다.

- **📢 섹션 요약 비유**: CPU 바운드를 이해하는 일은 오래 끓이는 국의 불 조절을 아는 것과 같다. 자꾸 불을 껐다 켜면 맛이 안 들고, 너무 세게만 두면 다른 요리가 탈 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| CPU Burst / I/O Burst | 프로세스 성향을 구분하는 기본 시간 패턴 |
| [문맥 교환](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) | CPU 바운드 작업을 자주 끊을수록 오버헤드 증가 |
| 코어 친화도 ([CPU Affinity](/studynote/02_operating_system/02_process_thread/144_cpu_affinity/)) | 같은 코어에서 계속 실행해 캐시 재사용 극대화 |
| [다단계 피드백 큐](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) ([MLFQ](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/)) | CPU 사용 패턴에 따라 우선순위와 실행 폭을 조정 |
| [완전 공정 스케줄러](/studynote/02_operating_system/03_cpu_scheduling/202_cfs_completely_fair_scheduler/) (CFS) | 공정성과 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 사이 균형을 맞추는 현대 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |

### 📈 관련 키워드 및 발전 흐름도

```text
CPU Burst / I/O Burst 구분
    |
    v
CPU 바운드 프로세스 식별
    |
    +--> 긴 실행 구간 보장
    +--> cache locality / CPU affinity 최적화
    +--> node isolation / batch scheduling 확장
```

이 흐름도는 CPU 바운드 개념이 단순 분류를 넘어, [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 인프라 격리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 이어지는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CPU 바운드 프로세스는 한 번 퍼즐을 잡으면 오래도록 집중해서 맞추는 아이예요.
2. 자꾸 중간에 끊으면 다시 생각하느라 시간이 더 오래 걸려요.
3. 그래서 컴퓨터는 이 아이에게는 조금 길게 집중할 시간을 주되, 다른 아이 차례도 잊지 않게 조심해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 165 / 800

<- **이전**: [164. I/O 바운드 프로세스 (I/O Bound Process)](/studynote/02_operating_system/03_cpu_scheduling/164_io_bound_process/)
**다음**: [166. 선점형 스케줄링 (Preemptive Scheduling)](/studynote/02_operating_system/03_cpu_scheduling/166_preemptive_scheduling/) ->

---
