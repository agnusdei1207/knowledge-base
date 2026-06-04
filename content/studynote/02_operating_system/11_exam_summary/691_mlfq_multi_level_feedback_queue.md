+++
title = "691. 다단계 피드백 큐 (MLFQ) 천이"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다단계 피드백 큐(Multi-Level Feedback [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/), MLFQ)는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 각 프로세스의 특성(CPU Bound vs I/O Bound)을 미리 알 수 없다는 한계를 극복하기 위해, <strong>실행 중인 프로세스의 과거 행동을 관찰하고 <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/">우선순위 큐</a>(<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>) 사이를 동적으로 이동(천이, Feedback)시키는 현대적 스케줄링 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>이다.
> 2. **메커니즘 (강등과 보상)**: 짧게 일하고 양보하는 착한 프로세스(I/O Bound)는 응답 속도가 빠른 최상위 큐에 남겨두고, 할당된 시간을 꽉 채워 탐욕스럽게 쓰는 프로세스(CPU Bound)는 벌점으로 판단하여 점점 더 타임 퀀텀이 길지만 우선순위는 낮은 하위 큐로 강등(Demotion)시킨다.
> 3. **기아 방지 (Priority Boost)**: CPU Bound 프로세스들이 하위 큐로 떨어져 영원히 CPU를 받지 못하는 기아([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 현상을 막기 위해, 일정 시간이 지나면 <strong>모든 프로세스를 다시 최상위 큐로 일제히 끌어올리는(Boost/리셋) 규칙</strong>을 적용하여 공평성을 유지한다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - **다단계 큐 (MLQ)**: 프로세스의 신분(시스템 앱 vs 유저 앱)에 따라 큐를 여러 개로 나누고 절대 신분을 바꿀 수 없는 계급 사회.
  - **다단계 피드백 큐 (MLFQ)**: 여러 개의 큐를 두되, 프로세스의 실행 패턴(피드백)에 따라 큐와 큐 사이를 오르내릴 수 있는(천이, Migration) 능력주의 사회.

- <strong>필요성 (<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a>의 무지(Ignorance) 극복)</strong>:
  - 완벽한 스케줄링을 하려면 이 프로그램이 끝나는 데 얼마나 걸릴지([SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/)) 알아야 한다. 하지만 OS는 미래를 알 수 없다(Halting Problem).
  - 그냥 [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/)([라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/))을 쓰자니, 응답이 빨라야 할 타이핑 앱(I/O 바운드)과 며칠 내내 돌아갈 인코딩 앱(CPU 바운드)이 똑같이 10ms씩 받는 게 비효율적이다.
  - **해결책**: "일단 제일 좋은 대우(최상위 큐)를 해줘 봐. 그런데 주어진 10ms를 꽉 채워 쓰는 욕심쟁이라면? 다음번엔 더 낮은 큐로 쫓아내자. 이렇게 계속 관찰(Feedback)하며 자리를 찾아주자!"라는 아이디어가 탄생했다.

  - **MLFQ의 병원 응급실 운영**:
    1. 환자가 오면 일단 무조건 '초응급실(최상위 큐)'로 넣고 의사가 1분만 진료한다.
    2. 1분 만에 치료가 끝나면 바로 퇴원시킨다 (I/O Bound 우대).
    3. 1분이 지났는데도 뼈를 맞춰야 하는 등 수술이 길어지면? "너는 1분 만에 끝날 애가 아니구나!" 하고 '일반 수술실(하위 큐)'로 내쫓는다. 일반 수술실은 순서는 늦게 오지만 대신 한 번 들어가면 10분 동안 길게 치료받을 수 있다.

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/">RR</a></strong>: 모두 똑같은 타임 퀀텀. CPU 바운드 때문에 전체 응답 속도 저하.
  2. **MLQ**: 큐를 나눴지만 신분이 고정되어 기아 발생 위험.
  3. **MLFQ (1962년 발명)**: Fernando Corbató가 발명(튜링상 수상). Windows, [Mac](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) OS, 과거 Solaris 등 역사상 가장 많은 상용 OS가 채택한 실전 최강의 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/).

- **📢 섹션 요약 비유**: 처음엔 모두에게 VIP 대우를 해주지만, 라운지에서 너무 오랫동안 공짜 밥을 축내는 손님(CPU 바운드)을 발견하면 조용히 일반석으로 내쫓아 진정한 VIP(I/O 바운드)들을 위한 공간을 항상 비워두는 영리한 호텔 지배인입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MLFQ의 5가지 기본 규칙

MLFQ 아키텍처는 다음 5가지의 엄격한 수학적 룰(Rules)로 동작한다.

1. **Rule 1 (우선순위 절대 권력)**: Priority(A) > Priority(B) 이면, A가 실행된다. (B는 멈춤)
2. **Rule 2 (동급의 평등)**: Priority(A) == Priority(B) 이면, A와 B는 그 큐 안에서 [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/)([라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/))로 돌아간다.
3. **Rule 3 (첫인상은 VIP)**: 프로세스가 시스템에 처음 들어오면 가장 높은 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/)(최상위)에 배치된다.
4. **Rule 4 (강등/Demotion)**: 프로세스가 자신에게 주어진 타임 퀀텀을 모두 소진하면(I/O 양보 없이 다 쓰면) 우선순위가 한 단계 강등된다.
5. **Rule 5 (사면/Priority Boost)**: 일정 시간 $S$가 지나면, 시스템의 모든 프로세스를 최상위 큐로 올려버린다. (기아 방지)

---

### 큐의 구조와 천이(Migration) 시뮬레이션

가장 흔한 3단계 큐(Q0, Q1, Q2)의 MLFQ 동작 메커니즘을 본다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 MLFQ 동작 및 타임 퀀텀 배분 (천이 과정)              │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [ Queue 0 ] (최상위, 우선순위 최고) - 타임 퀀텀(q) = 10ms               │
  │   - 프로세스 진입. 10ms 동안 실행됨.                                   │
  │   - 10ms 전에 I/O 대기를 위해 알아서 빠지면? ──▶ 계속 Q0에 남음 (착한 놈!)│
  │   - 10ms를 꽉 채웠는데도 안 끝나면?     ──▶ [ Q1 으로 강등 (Demotion) ]│
  │                                                                   │
  │  [ Queue 1 ] (중위권) - 타임 퀀텀(q) = 20ms                          │
  │   - Q0가 텅텅 비어야만 실행 기회를 얻음.                                 │
  │   - CPU를 잡으면 20ms 동안 길게 씀.                                   │
  │   - 20ms를 꽉 채우면?                   ──▶ [ Q2 로 강등 ]          │
  │                                                                   │
  │  [ Queue 2 ] (최하위, FCFS 형태) - 타임 퀀텀(q) = 40ms 이상 (또는 무한) │
  │   - Q0, Q1이 모두 비어야 실행됨.                                       │
  │   - 완전한 CPU Bound(예: 수학 연산, 렌더링)들만 모여있는 유배지.           │
  │   - 한 번 CPU를 잡으면 문맥 교환 없이 아주 오랫동안 연산함 (처리량 극대화).   │
  │                                                                   │
  │  ========== ⚡ 시간 S 도달 (Priority Boost) ⚡ ===================│
  │   - Q1, Q2에 있던 모든 프로세스가 다시 Q0로 순간이동(승격)함!!              │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상위 큐일수록 퀀텀이 짧고, 하위 큐일수록 퀀텀이 길다. 즉, <strong>"<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>이 중요한 놈은 위에서 빨리 치고 빠지고, 연산이 많이 필요한 놈은 아래로 내려가서 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">문맥 교환</a>(<a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/">Context Switch</a>) 오버헤드 없이 진득하게 계산해라"</strong>라는 극강의 실용주의 설계다. OS는 프로세스 성향을 미리 묻지 않고, 이 큐 시스템에 던져 넣기만 하면 알아서 거름망처럼 분류된다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### MLFQ의 약점 극복 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) (Rule 4와 Rule 5의 진화)

1. **초창기 Rule 4의 맹점 (Gaming the System)**:
   - 과거에는 "타임 퀀텀을 채우기 전에 놓으면 무조건 강등을 면해준다"고 설계했다.
   - 영악한 해커나 앱 개발자가 타임 퀀텀이 10ms일 때, `9.9ms` 동안 CPU를 미친 듯이 쓰고 `0.1ms` 동안 아주 짧은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) I/O를 요청하는 코드를 짰다.
   - 결과: OS는 "I/O 했으니 착한 애네" 하고 Q0에 계속 남겨두어 CPU를 99% 독점하게 만드는 어뷰징(Gaming)이 발생했다.
   - **현대의 Rule 4 변경**: 한 번 CPU를 잡았을 때의 시간이 아니라, <strong>"해당 큐에서 머물며 쓴 CPU 시간의 총합"</strong>이 퀀텀을 넘으면 얄짤없이 강등시켜 버려 꼼수를 차단했다.

2. **기아 현상과 Rule 5 (Priority Boost)**:
   - CPU 바운드가 Q2로 떨어졌는데, 위에서 I/O 바운드 앱들이 계속 쏟아져 들어오면 Q2의 애들은 굶어 죽는다([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)).
   - 또한, 어제까지 CPU 바운드였던 앱이 오늘은 사용자의 입력을 받는 I/O 바운드로 행동 패턴이 바뀔 수도 있다.
   - 이를 위해 주기적(예: 1초마다)으로 모든 프로세스를 Q0로 끌어올리는 Rule 5를 도입해 기아를 막고, 과거의 죄를 사면해 주는 유연성을 갖추었다.

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a> (<a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>)</strong>: MLFQ의 철학은 강화학습([Reinforcement Learning](/knowledge-base/studynote/12_it_management/02_itsm_itil/094_reinforcement_learning/))의 보상/페널티 모델과 매우 유사하다. 시스템에 대한 사전 지식(A Priori Knowledge) 없이, 환경과 상호작용하며 피드백을 통해 최적의 상태(큐 배치)를 스스로 학습해 찾아가는 고전적인 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)([Heuristic](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/236_a_star_heuristic_minimax_mcts_monte_carlo/)) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 정수다.

- **📢 섹션 요약 비유**: 꼼수를 부려 세금을 안 내는 부자(Gaming the system)를 막기 위해 법을 정교하게 고치고, 감옥에 간 죄수라도 10년이 지나면 특사(Priority Boost)로 풀어주어 새 삶을 살 기회를 주는 정교한 사법/행정 시스템과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — Windows 서버의 포그라운드/백그라운드 스케줄링 튜닝**: Windows OS는 철저한 MLFQ 기반 스케줄링을 사용한다. 개발자가 서버에서 배치 프로그램([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))을 돌려놓고, 웹 브라우저를 띄웠다.
   - **아키텍처 적용**: 윈도우는 유저가 현재 클릭해 활성화된 창(Foreground) 프로세스에게 타임 퀀텀을 3배 길게 주고 최상위 큐에 배치한다. 백그라운드로 내려간 앱([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))은 타임 퀀텀이 깎이고 하위 큐로 밀려난다(Demotion). 그 결과 사용자가 보는 창은 절대 버벅거리지 않고, 백그라운드 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)은 CPU가 남을 때 효율적으로 길게 돌아간다. (윈도우 제어판의 `성능 옵션 -> 프로세서 사용 계획 -> 프로그램 vs 백그라운드 서비스` 세팅이 바로 이 MLFQ 퀀텀을 튜닝하는 것이다.)

2. **시나리오 — Solaris OS에서의 시분할 및 실시간 큐 혼합**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 서버가 도는 솔라리스 시스템에서, DB 엔진 프로세스가 자꾸 하위 큐로 떨어져서 디스크 I/O 응답이 느려짐.
   - **대응 (기술사적 가이드)**: MLFQ의 자동 강등 시스템이 DB 엔진을 "무거운 CPU 앱"으로 오해한 것이다. 엔터프라이즈 환경에서는 특정 핵심 데몬이 하위 큐로 떨어지는 것을 막기 위해, MLFQ 큐 밖의 절대적인 <strong>실시간 우선순위 클래스 (Real-time Class)</strong>로 DB 데몬을 수동 배정(Pinning)하여, 일반 앱들의 피드백 규칙에 휘말리지 않도록 아키텍처적 격리를 수행해야 한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 MLFQ 스케줄러 핵심 파라미터 튜닝 플로우                  │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [OS나 프레임워크의 스케줄링 환경 최적화 시, 변수 조절을 통한 성능 타협]     │
  │                │                                                  │
  │                ▼                                                  │
  │      큐의 개수(Queue Count)를 몇 개로 할 것인가?                       │
  │      (너무 많으면 관리 오버헤드, 너무 적으면 RR/FCFS와 다를 바 없음)         │
  │          ├─ 윈도우/솔라리스 ──▶ 약 32개~64개의 세밀한 큐 유지            │
  │          └─ 커스텀 시스템   ──▶ 3~5개로 압축하여 빠른 스위칭 유도         │
  │                │                                                  │
  │                ▼                                                  │
  │      Priority Boost (사면/승격) 주기 'S'를 어떻게 잡을 것인가?            │
  │          ├─ S가 너무 길면 ──▶ CPU 바운드 프로세스가 기아(Starvation)에 빠짐 │
  │          └─ S가 너무 짧면 ──▶ 모든 게 최상위 큐에 몰려 일반 라운드 로빈(RR)이 │
  │                                되어버려 I/O 바운드 우대 효과가 소멸함.     │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MLFQ는 "가장 완벽한 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)"라는 찬사와 함께 "블랙 매직(Voodoo Constants)"이라는 비판도 동시에 받는다. 큐의 개수, 각 큐의 타임 퀀텀, Boost 주기 S값 등 수학적으로 증명하기 힘든 수많은 상수(Constants)들을 사람이 직접 감으로 튜닝해야 하기 때문이다. Ousterhout의 법칙처럼 시스템 아키텍트의 오랜 경험치에 절대적으로 의존하는 영역이다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>Nice 값(우선순위 <a href="/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/">힌트</a>) 연동</strong>: 사용자가 터미널에서 `nice` 명령어로 프로세스에 가중치를 주었을 때, MLFQ가 이를 무시하는가 아니면 시작 큐의 위치를 낮춰주는 형태로 존중([Hint](/knowledge-base/studynote/05_database/03_relational_model/167_sql_hint_optimizer_override/))하는가? (보통 기본 우선순위 레벨을 깎아서 튜닝을 돕는다.)

- **📢 섹션 요약 비유**: MLFQ의 튜닝은 게임 밸런스 패치와 같습니다. 전사(CPU 바운드)와 마법사(I/O 바운드) 중 누가 너무 사기 캐릭터가 되지 않도록, 타임 퀀텀과 승격 주기라는 수치를 끝없이 미세 조정해야 유저(프로세스)들이 불만 없이 시스템에 머뭅니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | Round Robin (단일 큐) | MLFQ (다단계 피드백 큐) | 개선 효과 |
|:---|:---|:---|:---|
| <strong>정량 (<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>)</strong>| 모든 프로세스가 동일한 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 체감 | **I/O 바운드는 최상위 큐에서 즉각 응답** | 대화형 앱의 P99 반응속도 극대화 |
| <strong>정량 (<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>)</strong> | 잦은 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)으로 CPU 효율 감소 | 하위 큐(긴 퀀텀)에서 CPU 효율 방어 | [Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드 최적화 |
| **정성 (예측 의존성)**| ([SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/)) 미래 예측이 틀리면 치명타 | 과거 이력 기반(Feedback)으로 대응 | 런타임 행동 변화에 완벽히 동적으로 적응 |

### 미래 전망
- **CFS로의 패러다임 쉬프트**: 리눅스는 2.6 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 이전까지 MLFQ의 변형(O(1) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))을 썼다. 하지만 수많은 큐를 관리하고 [휴리스틱](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/) 상수를 튜닝하는 것에 피로감을 느낀 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 진영은 큐를 전부 없애고 [레드-블랙 트리](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/063_red_black_tree/) 하나만 쓰는 CFS(Completely Fair Scheduler)로 갈아탔다. 반면 윈도우와 macOS는 여전히 MLFQ의 철학을 고도화하여 사용 중이므로, 이 두 패러다임은 OS 역사상 영원한 라이벌로 남을 것이다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 커스텀 큐잉</strong>: 고정된 OS의 MLFQ [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 대신, eBPF를 통해 "우리 회사의 A 앱은 무조건 2번 큐, B 앱은 퀀텀 100ms" 식으로 클라우드 사업자가 직접 하이퍼바이저의 스케줄링 큐 정책을 코딩해서 박아 넣는 시대가 열리고 있다.

### 결론
다단계 피드백 큐(MLFQ)는 "미래를 알 수 없다면, 과거를 보고 판단하라"는 아주 단순하고 강력한 철학의 결정체다. 짧은 작업은 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)을 극대화하고(SJF의 장점), 긴 작업은 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드를 최소화하며(FCFS의 장점), 이 둘을 공평하게 섞는다(RR의 장점)는 OS 스케줄링 역사의 모든 지혜를 하나의 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 안에 욱여넣은 마스터피스다. 비록 수많은 [매직 넘버](/knowledge-base/studynote/02_operating_system/09_file_system/503_magic_number_file_signature/)(튜닝 상수)들의 노예가 되기도 하지만, 지난 반세기 동안 우리가 쓰는 데스크탑이 멈추지 않고 부드럽게 돌아갈 수 있었던 가장 든든한 뼈대임은 부정할 수 없다.

- **📢 섹션 요약 비유**: 사람의 성격을 미리 알 수 없으니, 일단 모두에게 완벽한 대우(최상위 큐)를 해준 뒤, 이기적으로 구는 사람(CPU 바운드)은 점점 멀리하고(강등), 불이익을 받은 사람(기아)은 정기적으로 챙겨주는(승격) 가장 인간적이고 합리적인 사회 시스템의 축소판입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) 기아 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)) 발생 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [라운드 로빈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/) [시간 할당량](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/179_time_quantum_context_switch/) ([Quantum](/knowledge-base/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [HRN](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/187_hrn_scheduling/) 대기 시간 공식 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [멀티스레드 유저모드 커널모드](/knowledge-base/studynote/02_operating_system/11_exam_summary/693_multithread_user_mode_kernel_mode/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[라운드 로빈 시간 할당량 (Quantum)]
    │
    ▼
[다단계 피드백 큐 (MLFQ) 천이]
    │
    ├──▶ [HRN 대기 시간 공식]
    └──▶ [멀티스레드 유저모드 커널모드]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 게임장([운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))에 여러 친구들이 왔어요. 게임장 주인은 모든 친구를 일단 제일 좋은 'VIP 줄(최상위 큐)'에 세우고 1분씩 게임을 시켜줬어요.
2. 1분도 안 돼서 게임을 끝내고 나오는 착한 친구(I/O 바운드)는 계속 VIP 줄에 설 수 있어요. 하지만 1분을 꽉 채우고도 안 비키는 욕심쟁이(CPU 바운드)는 '일반 줄(하위 큐)'로 쫓겨나요.
3. 일반 줄은 순서는 늦게 오지만 대신 한 번 타면 10분 동안 길게 탈 수 있어요. 그리고 일반 줄 친구들이 너무 오래 기다리면 불쌍하니까 1시간마다 한 번씩 다 같이 VIP 줄로 올려준답니다(Priority Boost)!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 691 / 800

← **이전**: [690. 라운드 로빈 시간 할당량 (Quantum)](/knowledge-base/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/)
**다음**: [692. HRN 대기 시간 공식 (Hrn Highest Response Ratio Next)](/knowledge-base/studynote/02_operating_system/11_exam_summary/692_hrn_highest_response_ratio_next/) →

---
