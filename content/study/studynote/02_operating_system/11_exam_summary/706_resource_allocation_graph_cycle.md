---
title: 706. 자원 할당 그래프 사이클 (Resource Allocation Graph Cycle)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[287_resource_allocation_graph|자원 할당 그래프]]([[287_resource_allocation_graph|Resource Allocation Graph]], [[276_fine_tuning|RAG]])는 시스템 내의 프로세스들과 그들이 쥐고 있거나 요구하는 자원들 간의 [[083_relationship_in_er_model|관계]]를 점(Vertex)과 선(Edge)으로 [[003_bigdata_7v|시각화]]하여, **[[281_deadlock_definition|교착 상태]]([[281_deadlock_definition|Deadlock]])의 발생 여부를 수학적으로 판별**하는 운영체제의 도해적 분석 도구다.
> 2. **사이클의 의미**: 이 방향성 [[070_graph_datastructure|그래프]]에서 선을 따라갔을 때 다시 제자리로 돌아오는 **'사이클(Cycle)'이 존재한다는 것은 원형 대기([[286_circular_wait|Circular Wait]])가 성립**했음을 뜻하며, 이는 [[281_deadlock_definition|교착 상태]]를 유발하는 가장 강력한 경고등이다.
> 3. **다중 인스턴스의 예외**: 단일 인스턴스(자원이 딱 1개) 환경에서는 사이클이 곧 100% 데드락을 의미하지만, 다중 인스턴스(동일한 자원이 여러 개) 환경에서는 사이클이 있어도 남는 자원을 가진 외부 프로세스가 고리를 끊어줄 수 있으므로 **'사이클 = 데드락' 공식이 무조건 성립하지 않는다**는 점이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **정점(Vertex)**: 프로세스 $P$ (보통 원으로 표시)와 자원 $R$ (보통 사각형으로 표시).
  - **간선(Edge)**: 
    - **요구 간선 (Request Edge, $P \rightarrow R$)**: 프로세스가 자원을 요청하고 기다리는 중.
    - **할당 간선 (Assignment Edge, $R \rightarrow P$)**: 자원이 프로세스에게 이미 할당되어 점유된 상태.
  - **사이클 (Cycle)**: [[070_graph_datastructure|그래프]]의 화살표 방향을 따라갔을 때 처음 출발했던 정점으로 다시 돌아올 수 있는 폐쇄된 경로.

- **필요성 (눈에 보이지 않는 꼬임의 [[003_bigdata_7v|시각화]])**: 
  - 서버에서 프로세스 50개가 DB 커넥션, 프린터, [[501_file_definition_logical_record|파일]] 락 등 수백 개의 자원을 놓고 싸우고 있다. 
  - 시스템이 멈췄을 때 "도대체 누구 때문에 꼬인 거야?"를 소스 코드만 보고 파악하는 것은 불가능하다.
  - **해결책**: OS [[022_kernel_role|커널]]이 현재 자원을 "누가 가졌고(할당), 누가 기다리는지(요구)"를 실시간 [[070_graph_datastructure|그래프]]로 그려서 추적하면, 사이클 탐색 [[001_algorithm_definition|알고리즘]]([[034_dfs|DFS]] 등)을 통해 [[281_deadlock_definition|교착 상태]]의 근원지(범인)를 정확히 짚어내고 강제 종료(Kill)시킬 수 있다.

  - **상황**: 교차로에서 자동차 4대가 서로 엉켜서 빵빵거리고 있다.
  - **[[287_resource_allocation_graph|자원 할당 그래프]]**: 경찰 헬기가 하늘에서 교차로를 내려다보며 도면을 그린다. "1번 차는 앞길(자원)을 원하는데 2번 차가 막고 있고, 2번 차는 3번 차가... 4번 차는 1번 차가 막고 있네!" 
  - **사이클**: 헬기에서 보니 4대의 차가 완벽한 '네모(Cycle)' 모양으로 꼬리를 물고 있다. 경찰은 이 도면([[070_graph_datastructure|그래프]])을 보고 "아, 이건 절대 안 풀리는 데드락이구나"라고 판단하고 견인차를 부른다.

- **발전 과정**:
  1. **단순 [[070_graph_datastructure|그래프]] 모델링**: 1970년대 데드락 개념 정립 시 [[003_bigdata_7v|시각화]] 도구로 제안됨.
  2. **[[305_wait_for_graph|Wait-for Graph]] ([[305_wait_for_graph|대기 그래프]])**: 단일 자원 환경에서 자원 노드를 빼버리고, 프로세스 간의 대기 [[083_relationship_in_er_model|관계]]($P_1 \rightarrow P_2$)로만 [[070_graph_datastructure|그래프]]를 압축하여 탐색 속도를 높임.
  3. **[[502_dbms|DBMS]] [[304_deadlock_detection|교착 상태 탐지]]**: 현대 [[188_pl_sql_t_sql_procedural|Oracle]], MySQL 등 RDBMS의 [[281_deadlock_definition|Deadlock]] Detector 데몬이 백그라운드에서 실시간으로 이 [[070_graph_datastructure|그래프]] 사이클을 검사함.

- **📢 섹션 요약 비유**: 복잡하게 엉킨 이어폰 줄을 손의 감각만으로 풀려다 포기하고, 책상 위에 넓게 펼쳐놓고 눈으로 보며 어디가 꼬였는지 찾아내는 시각적 분석 작업입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[287_resource_allocation_graph|자원 할당 그래프]]의 기본 문법

[[070_graph_datastructure|그래프]]를 그리는 법은 매우 직관적이다. 자원(사각형) 안에 있는 점([[519_dot_dns_over_tls|Dot]])의 개수는 그 자원의 **인스턴스(개수)**를 의미한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 자원 할당 그래프 (RAG) 점과 선의 의미                   │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ P1 ] ────(요청 간선)────▶ [ R1 (점 1개) ]                     │
  │     ▲                             │                               │
  │     │                             │                               │
  │     └────────(할당 간선)──────────┘                               │
  │                                                                   │
  │  해석: P1이 R1에게 자원을 달라고 요청(->)했는데, R1 안의 유일한 자원 1개가 │
  │        이미 P1 자신에게 할당(<-)되어 있다.                             │
  │        (일반적인 락 획득 상태)                                       │
  └───────────────────────────────────────────────────────────────────┘
```

---

### 사이클(Cycle)과 데드락의 상관관계 (핵심 함정)

[[287_resource_allocation_graph|자원 할당 그래프]]를 분석할 때 가장 중요한 것은 **자원의 개수(인스턴스)**다.

**Case 1: 단일 인스턴스 자원 (프린터 1대, [[501_file_definition_logical_record|파일]] 락 1개)**
- 상황: `P1 -> R1 -> P2 -> R2 -> P1` (사이클 발생!)
- 결과: 자원이 딱 1개씩밖에 없는데 서로 꼬리를 물었다. 제3자가 도와줄 여지가 없다.
- **판단: 사이클 = 무조건 100% 데드락이다.**

**Case 2: 다중 인스턴스 자원 (DB 커넥션 풀 3개, [[103_thread_pool|스레드 풀]] 5개)**
- 상황: `P1 -> R1 -> P2 -> R2 -> P1` 로 P1과 P2가 사이클을 만들었다.
- 그런데 R1 자원 안에는 점(인스턴스)이 2개 있다! 하나는 P2가 쥐고 있지만, **나머지 하나는 P3가 쥐고 있다.** (P3는 사이클 밖의 제3자다)
- **판단**: 현재는 사이클이 있지만 데드락이 아닐 수도 있다! 만약 사이클 밖에 있는 착한 P3가 일을 다 끝내고 R1 자원을 반납하면? P1이 그 반납된 R1을 낼름 가져가서 사이클을 부수고 시스템이 정상으로 돌아간다. 
- **결론: 다중 인스턴스 환경에서 '사이클'은 데드락의 "필요조건"일 뿐, "충분조건"은 아니다.**

- **📢 섹션 요약 비유**: 좁은 골목길(단일 자원)에서 차가 꼬리를 물면 100% 데드락입니다. 하지만 왕복 4차선(다중 자원)에서 차가 꼬리를 물었더라도, 옆 차선에서 쌩 지나가던 차(제3의 프로세스)가 빠져나가며 빈 공간을 만들어주면 꼬인 차들이 거기로 빠져나와 엉킴이 풀릴 수 있습니다.

---

## Ⅲ. 비교 및 연결

### [[276_fine_tuning|RAG]] ([[287_resource_allocation_graph|Resource Allocation Graph]]) vs WFG ([[305_wait_for_graph|Wait-For Graph]])

단일 인스턴스 환경에서는 [[070_graph_datastructure|그래프]]를 더 가볍게 압축할 수 있다.

| 비교 항목 | [[276_fine_tuning|RAG]] ([[287_resource_allocation_graph|자원 할당 그래프]]) | WFG ([[305_wait_for_graph|대기 그래프]]) |
|:---|:---|:---|
| **구성 요소** | 프로세스 노드, 자원 노드 | **오직 프로세스 노드만 존재** |
| **간선의 의미** | 요청($P \rightarrow R$), 할당($R \rightarrow P$) | 대기($P_1 \rightarrow P_2$ : $P_1$이 $P_2$의 자원을 기다림) |
| **사용 환경** | 단일 및 다중 인스턴스 모두 사용 | **단일 인스턴스 자원에만 사용 가능** |
| **탐색 오버헤드**| 노드가 많아 $O(V+E)$ 연산이 무거움 | 노드가 절반으로 줄어 탐색([[034_dfs|DFS]])이 매우 빠름 |

*[[002_database_definition|데이터베이스]](DB)의 데드락 감지기는 보통 테이블 락(Row [[510_lock|Lock]], 단일 인스턴스)을 다루기 때문에, 자원 노드를 생략한 가벼운 WFG([[305_wait_for_graph|대기 그래프]])를 주기적으로 순회하며 사이클을 찾는다.*

### 과목 융합 관점

- **자료구조 / [[001_algorithm_definition|알고리즘]]**: [[070_graph_datastructure|그래프]]에서 사이클을 찾는 가장 표준적인 방법은 **[[034_dfs|DFS]] ([[034_dfs|깊이 우선 탐색]])**다. 노드를 방문할 때마다 '방문 중(Visiting)' 상태로 마킹하고, 다음 화살표를 따라갔는데 또 '방문 중'인 노드를 만나면 사이클이 발견된 것이다. 이 [[001_algorithm_definition|알고리즘]]의 시간 복잡도는 $O(N^2)$에 달하므로, 프로세스가 수만 개인 시스템에서는 이 감지기를 너무 자주 돌리면 OS 자체가 느려진다.

- **📢 섹션 요약 비유**: RAG는 "사람과 의자"를 모두 그린 복잡한 설계도고, WFG는 "누가 누구를 기다리나" 화살표만 사람끼리 짝지어 놓은 요약본입니다. 의자가 무조건 1인용(단일 자원)이라면 굳이 의자를 그리지 않아도 상황 파악이 끝납니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — RDBMS(MySQL, PostgreSQL)의 데드락 감지와 희생자(Victim) 선정**: 온라인 쇼핑몰 결제 도중 "[[281_deadlock_definition|Deadlock]] found when trying to get [[510_lock|lock]]; try restarting [[191_transaction_concept_states|transaction]]" 에러가 발생하며 [[191_transaction_concept_states|트랜잭션]]이 롤백됨.
   - **원인 분석**: MySQL의 InnoDB 스토리지 엔진은 내부적으로 **[[510_lock|Lock]]-wait [[104_graph|Graph]]([[305_wait_for_graph|대기 그래프]])**를 실시간으로 그리고 있다. A [[191_transaction_concept_states|트랜잭션]]과 B [[191_transaction_concept_states|트랜잭션]]이 서로의 Row Lock을 요구하며 꼬리물기(사이클)를 [[087_process_state_transition|생성]]한 순간, 백그라운드 [[092_thread_lwp|스레드]]([[281_deadlock_definition|Deadlock]] Detector)가 이를 즉각 감지했다.
   - **대응 (기술사적 가이드)**: DB는 데드락을 풀기 위해 사이클 내의 [[191_transaction_concept_states|트랜잭션]] 중 **[[393_undo|Undo]] Log(롤백해야 할 [[001_dikw_pyramid|데이터]]) 양이 가장 적은 [[191_transaction_concept_states|트랜잭션]](만만한 놈)을 희생자(Victim)**로 골라 강제로 죽여(Kill) 버리고 에러를 던진다. 따라서 애플리케이션 개발자는 이 에러를 받았을 때 당황하지 말고, `try-catch`로 잡아서 [[191_transaction_concept_states|트랜잭션]]을 0.1초 뒤에 다시 시도(Retry)하는 로직을 반드시 짜두어야 한다.

2. **시나리오 — K8s 클러스터의 자원(CPU/Mem) 데드락 회피**: [[136_variance|분산]] 시스템 환경에서 [[090_service_kubernetes_network_load_balancing|서비스]] A는 서버 1의 CPU를 100% 점유하고 서버 2의 램을 원하며, [[090_service_kubernetes_network_load_balancing|서비스]] B는 서버 2의 램을 100% 점유하고 서버 1의 CPU를 원한다.
   - **아키텍처 적용**: 클라우드 [[073_container_orchestration_tools|오케스트레이션]](K8s) 레벨에서는 다중 인스턴스 자원을 다룬다. 여기서 사이클이 생겼다고 바로 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])를 죽이면 엄청난 [[090_service_kubernetes_network_load_balancing|서비스]] 장애가 온다(사이클이 데드락의 절대 조건이 아니므로). 
   - 따라서 현대 클라우드는 [[070_graph_datastructure|그래프]] 사이클 탐지([[961_deepfake_detection|Detection]]) 방식 대신, [[085_pod_kubernetes_container_unit|파드]]를 띄우기 전 남은 자원을 계산하여 **은행원 [[001_algorithm_definition|알고리즘]](Avoidance)**처럼 애초에 데드락이 날 것 같은 스케줄링 자체를 거부하거나, [[157_oom_killer|OOM]] Killer처럼 여유 임계치에 도달하면 무자비하게 큰 놈을 밀어내는 **Preemption([[295_deny_no_preemption|비선점 부정]])** 방식으로 아키텍처를 해결한다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 시스템의 교착 상태(Deadlock) 해결 전략 선택 플로우          │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [멀티스레드/멀티프로세스 환경의 교착 상태 방어 아키텍처 수립]               │
  │                │                                                  │
  │                ▼                                                  │
  │      OS 커널 단에서 실시간으로 자원 할당 그래프(RAG)를 그려서 사이클을 찾는가?│
  │          ├─ 예 ─────▶ [엄청난 성능 오버헤드 (O(N^2))]                 │
  │          │            결론: Windows, Linux 등 현대 범용 OS는 이 방식을   │
  │          │                  아예 포기함 (타조 알고리즘 적용).            │
  │          └─ 아니오 ──▶ 그럼 누가 이 귀찮은 사이클 탐지를 하는가?           │
  │                │                                                  │
  │                ▼                                                  │
  │             [응용 프로그램 또는 DBMS 레벨에 위임]                      │
  │             1) DB: 트랜잭션 락은 짧으므로 WFG 기반 실시간 감지 & Kill 적용 │
  │             2) 앱: 개발자가 Lock Ordering 규칙(원형 대기 부정)을 소스코드  │
  │                    에 강제하여 원천적으로 사이클 생성을 차단               │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 리눅스 [[022_kernel_role|커널]] 소스 코드를 아무리 뒤져봐도 "데드락 사이클 탐지" 로직은 없다. OS가 수만 개의 [[092_thread_lwp|스레드]]와 [[501_file_definition_logical_record|파일]] 락을 1ms마다 [[034_dfs|DFS]] [[070_graph_datastructure|그래프]] 탐색을 돌리면 컴퓨터가 멈출 것이다. [[070_graph_datastructure|그래프]] 사이클 모델은 OS가 직접 [[289_cqrs_db|쓰기]] 위해 만든 것이 아니라, "개발자 너희들이 머릿속으로 이 [[070_graph_datastructure|그래프]]를 그려보고 사이클이 안 나게 코드를 짜라"고 던져준 수학적 분석 도구(Modeling Tool)에 가깝다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **[[510_lock|Lock]] 타임아웃의 활용**: 시스템에서 [[070_graph_datastructure|그래프]] 기반 탐지가 불가능하다면, 가장 현실적인 대안은 "락을 3초 이상 못 얻으면 포기한다"는 [[319_timeout_prevention|Timeout]] 기법이다. 무한정 기다리는 선(Edge)을 시간제한을 두어 툭 끊어버리면, 거대한 사이클이 형성되다가도 중간중간 알아서 붕괴되어 데드락이 해소되는([[315_livelock_vs_deadlock|Livelock]] 위험은 있음) 회피형 아키텍처가 구현되었는가?

- **📢 섹션 요약 비유**: 수만 명이 얽힌 거대한 실타래(시스템)에서 매초 꼬인 곳을 찾아내는 것([[070_graph_datastructure|그래프]] 사이클 탐색)은 불가능합니다. 차라리 엉키지 않게 규칙을 주거나([[317_lockdep_lock_ordering|Lock Ordering]]), 엉킨 것 같으면 가위로 확 잘라버리는 것([[319_timeout_prevention|Timeout]]/Kill)이 실무적인 엔지니어링입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 감지 메커니즘 부재 | [[287_resource_allocation_graph|자원 할당 그래프]](WFG) 기반 감지 | 개선 효과 |
|:---|:---|:---|:---|
| **정성 (시스템 [[452_availability|가용성]])**| 데드락 발생 시 시스템 무기한 멈춤 | 즉각적인 감지 및 타겟 킬링으로 [[233_recovery_database_restoration_overview|회복]] | 중단 없는 24/365 엔터프라이즈 운영 가능 |
| **정량 (탐색 속도)** | 수작업 [[092_thread_lwp|스레드]] 덤프 분석 (수 시간) | [[034_dfs|DFS]] 기반의 사이클 판별 (수 ms) | 장애 인지 및 [[658_ir_recovery|복구]] 시간의 극단적 단축 |
| **정성 (부작용 방어)**| 엉뚱한 프로세스를 강제 종료할 위험 | 사이클에 직접 연관된 프로세스만 조준 | 2차 장애(Cascading Failure) 방지 |

### 미래 전망
- **[[331_static_analysis|정적 분석]]([[331_static_analysis|Static Analysis]]) 툴의 [[070_graph_datastructure|그래프]] [[087_process_state_transition|생성]]**: 과거에는 시스템이 런타임에 죽고 나서야 [[092_thread_lwp|스레드]] 덤프를 떠서 [[070_graph_datastructure|그래프]]를 그렸다. 이제는 컴파일 타임에 SonarQube나 Coverity 같은 도구가 소스 코드를 분석하여 "이 [[223_mutex|Mutex]] A와 B는 런타임에 교차 획득되어 사이클을 형성할 확률이 높습니다"라고 미리 [[287_resource_allocation_graph|자원 할당 그래프]]를 그려 경고해 주는 사전 방어 모델이 발전하고 있다.
- **[[136_variance|분산]] 환경의 락 매니저 ([[798_distributed_lock_zookeeper_consensus|ZooKeeper]])**: [[619_msa_traffic_hardware|MSA]] 환경에서는 WFG를 단일 장비에서 그릴 수 없다. 여러 장비가 중앙의 ZooKeeper나 [[542_redis|Redis]] [[136_variance|분산]] 락을 호출할 때, 이 중앙 매니저가 글로벌 [[287_resource_allocation_graph|자원 할당 그래프]]를 관리하며 [[136_variance|분산]] 데드락을 감지하고 끊어내는 지능형 에이전트로 진화 중이다.

### 결론
[[287_resource_allocation_graph|자원 할당 그래프]]([[276_fine_tuning|RAG]])와 사이클은 보이지 않는 소프트웨어의 [[017_hardware_interrupt|비동기적]] 꼬임을, 눈에 보이고 수학적으로 증명 가능한 '기하학적 도형'으로 끌어낸 훌륭한 [[198_abstraction_control_data_process|추상화]] 모델이다. 단일 인스턴스에서의 '사이클 = 데드락'이라는 명쾌한 공식은 RDBMS의 [[191_transaction_concept_states|트랜잭션]] 방어선으로 깊게 뿌리내렸고, 다중 인스턴스의 얽히고설킨 딜레마는 현대 클라우드 [[073_container_orchestration_tools|오케스트레이션]]의 자원 배분 철학으로 남았다. 아키텍트는 락([[510_lock|Lock]])을 짤 때마다 머릿속 허공에 이 동그라미와 화살표를 그리며, 자신이 짠 코드가 치명적인 폐쇄 루프(Cycle)를 만들고 있지는 않은지 끊임없이 의심해야 한다.

- **📢 섹션 요약 비유**: 숲속에서 길을 잃고 뺑뺑 도는 사람(데드락)은 자기가 돌고 있는지 모릅니다. 하늘에서 드론([[287_resource_allocation_graph|자원 할당 그래프]])을 띄워 그 사람의 발자국을 내려다볼 때, 완벽한 원형(사이클)을 그리고 있다는 사실을 깨닫고 즉시 구출 대원([[281_deadlock_definition|Deadlock]] Detector)을 투입할 수 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 식사하는 철학자 교착 문제 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[281_deadlock_definition|교착 상태]] 4가지 조건 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 은행원 [[001_algorithm_definition|알고리즘]] [[298_safe_state|안전 상태]] | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[708_deadlock_ignorance_ostrich_algorithm|교착 상태 무시]] ([[291_ostrich_algorithm|타조 알고리즘]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[교착 상태 4가지 조건]
    │
    ▼
[자원 할당 그래프 사이클 (Resource Allocation Graph Cycle)]
    │
    ├──▶ [은행원 알고리즘 안전 상태]
    └──▶ [교착 상태 무시 (타조 알고리즘)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 칠판에 동그라미(친구)와 네모(장난감)를 그렸어요. 철수가 로봇을 갖고 놀면 철수 쪽으로 화살표를 그리고, 영희가 로봇을 기다리면 로봇에서 영희 쪽으로 화살표를 그려요.
2. 화살표를 계속 따라가 봤는데, 어라? 철수 -> 로봇 -> 영희 -> 인형 -> 다시 철수! 화살표가 뺑뺑 도는 '동그라미 길(사이클)'이 만들어졌어요!
3. 이렇게 꼬리에 꼬리를 무는 '사이클'이 그림에 나타나면, 아무도 양보하지 않아서 모두가 멈춰버린 끔찍한 '데드락' 상황이라는 걸 한눈에 알아챌 수 있답니다!
