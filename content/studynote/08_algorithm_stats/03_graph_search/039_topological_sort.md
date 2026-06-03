---
title: 11. 위상 정렬 (Topological Sort) — DAG, Kahn's / DFS 기반
date: '2026-04-21'
tags:
- studynote-algorithm
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 위상 정렬 (Topological Sort)은 [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]], 방향 비순환 [[070_graph_datastructure|그래프]])의 모든 간선 u→v에 대해 u가 v보다 앞에 오도록 정점을 순서화하는 [[001_algorithm_definition|알고리즘]]이다.
> 2. **가치**: 작업 선후관계, 빌드 시스템 의존성, 강의 수강 선수조건 등 "A를 먼저 해야 B를 할 수 있다"는 실세계 의존 [[083_relationship_in_er_model|관계]]를 O(V+E)에 선형적으로 해결한다.
> 3. **판단 포인트**: 사이클이 존재하면 위상 정렬 불가능 (사이클 = [[316_synchronization_bug_debugging|순환 의존성]]) — Kahn's [[001_algorithm_definition|알고리즘]]은 in-degree 0인 정점이 없으면 사이클을 자동 감지한다.

## Ⅰ. 개요 및 필요성

위상 정렬은 DAG에서만 정의된다. [[070_graph_datastructure|그래프]]에 사이클이 있으면 "A를 먼저 해야 B를 할 수 있고, B를 먼저 해야 A를 할 수 있다"는 모순이 발생하기 때문이다.

| 특성 | 내용 |
|:---|:---|
| [[002_time_complexity|시간 복잡도]] | O(V+E) |
| [[003_space_complexity|공간 복잡도]] | O(V) |
| 전제 조건 | [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) |
| 결과 유일성 | 여러 유효한 정렬 순서 존재 가능 |
| 사이클 감지 | Kahn's: 처리 정점 수 < V이면 사이클 |

위상 정렬이 필요한 상황:

- 빌드 시스템 (Make, Maven, Gradle): 의존 [[192_module_independence|모듈]] 빌드 순서
- 강의 수강 선수 조건 (과목 이수 순서)
- [[645_data_pipeline_acceleration|데이터 파이프라인]] [[401_bayesian_network_dag_causality|DAG]] 실행 순서 ([[168_airflow_dag_pipeline_scheduling|Apache Airflow]])
- 컴파일러 표현식 평가 순서

📢 **섹션 요약 비유**: 위상 정렬은 요리 레시피를 만드는 것과 같다. "양파를 볶은 후 고기를 넣고, 고기가 익으면 소스를 넣는다" — 각 단계의 선행 조건을 지키며 순서를 나열한다.

## Ⅱ. 아키텍처 및 핵심 원리

### 예시 [[401_bayesian_network_dag_causality|DAG]] (강의 선수 조건)

```
수학(A) → 선형대수(B) → 머신러닝(D)
수학(A) → 통계(C) ────→ 머신러닝(D)
프로그래밍(E) ─────────→ 머신러닝(D)
```

### Kahn's [[001_algorithm_definition|알고리즘]] ([[035_bfs|BFS]] 기반, in-degree 추적)

```
1. 각 정점의 진입 차수(in-degree) 계산
2. in-degree=0인 정점을 모두 큐에 삽입
3. 큐에서 꺼낼 때마다 결과에 추가
4. 해당 정점의 이웃 in-degree를 1씩 감소
5. in-degree가 0이 된 이웃을 큐에 삽입
6. 결과 크기 < V → 사이클 존재
```

### [[034_dfs|DFS]] 기반 위상 정렬 (역후위 순서)

```
DFS 탐색에서 정점이 완전 처리될 때(finish) 스택에 Push
최종 스택을 Pop 순서 = 위상 정렬 순서
```

### [[103_ascii|ASCII]] 다이어그램 — Kahn's [[001_algorithm_definition|알고리즘]] [[216_progress_in_synchronization|진행]]

```
┌──────────────────────────────────────────────────────────┐
│  DAG:   A → B → D                                        │
│         A → C → D                                        │
│         E ─────→ D                                       │
│                                                          │
│  in-degree: A=0, B=1, C=1, D=3, E=0                      │
│                                                          │
│  Step1: 큐=[A,E]                                         │
│  Step2: A 꺼냄→결과[A] → B.in-=1(=0), C.in-=1(=0)       │
│         큐=[E,B,C]                                       │
│  Step3: E 꺼냄→결과[A,E] → D.in-=1(=2)  큐=[B,C]         │
│  Step4: B 꺼냄→결과[A,E,B] → D.in-=1(=1) 큐=[C]          │
│  Step5: C 꺼냄→결과[A,E,B,C] → D.in-=1(=0) 큐=[D]        │
│  Step6: D 꺼냄→결과[A,E,B,C,D]                           │
│                                                          │
│  결과: A → E → B → C → D  (유효한 위상 순서 중 하나)      │
└──────────────────────────────────────────────────────────┘
```

### 두 [[001_algorithm_definition|알고리즘]] 비교

| 항목 | Kahn's [[001_algorithm_definition|알고리즘]] | [[034_dfs|DFS]] 기반 |
|:---|:---|:---|
| 기반 탐색 | [[035_bfs|BFS]] (큐) | [[034_dfs|DFS]] ([[014_recursion|재귀]]/[[057_stack|스택]]) |
| 사이클 감지 | 결과 크기 [[396_validation|확인]] | 역방향 간선 탐지 |
| 구현 복잡도 | 직관적 | 약간 복잡 |
| 역후위 | 자연스럽지 않음 | 자연스러운 출력 |
| [[430_index_fast_full_scan|병렬]] 처리 | 레벨별 [[430_index_fast_full_scan|병렬]] 가능 | 어려움 |

📢 **섹션 요약 비유**: Kahn's [[001_algorithm_definition|알고리즘]]은 "준비물이 모두 갖춰진 작업부터 먼저 시작"하는 방식이다. 아무것도 기다릴 필요 없는 작업(in-degree=0)을 먼저 완료하고, 그로 인해 준비된 다음 작업을 처리한다.

## Ⅲ. 비교 및 연결

### 위상 정렬이 불가능한 경우 (사이클)

```
A → B → C → A  (사이클 존재)

Kahn's: A.in=1, B.in=1, C.in=1
→ 초기 큐에 아무것도 없음
→ 결과 크기=0 < V=3 → 사이클 감지
```

### 위상 정렬 응용 — 최장 경로 (Critical Path)

DAG에서 위상 정렬 순서로 DP를 적용하면 최장 경로 (Critical Path)를 O(V+E)에 계산 가능:

```
longest[v] = max(longest[u] + weight(u,v)) for all u→v
→ 프로젝트 완료 최소 기간 계산 (CPM, Critical Path Method)
```

📢 **섹션 요약 비유**: 위상 정렬의 최장 경로 = 프로젝트 관리의 크리티컬 패스다. 이 경로를 지연시키면 전체 프로젝트가 지연된다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

**시나리오 1**: [[255_apache_airflow_dag|Apache Airflow DAG]] 실행 순서
- [[645_data_pipeline_acceleration|데이터 파이프라인]] 각 태스크를 정점, 의존성을 간선으로 모델링
- 위상 정렬로 실행 순서 결정 → [[430_index_fast_full_scan|병렬]] 가능한 작업 동시 실행

**시나리오 2**: npm/pip 패키지 의존성 해결
- 패키지 설치 시 의존 패키지를 먼저 설치
- [[316_synchronization_bug_debugging|순환 의존성]] 감지 → 오류 보고 (npm의 peerDependency 경고)

**시나리오 3**: 대학 수강 신청 시스템
- 선수 조건 위반 수강 신청 차단
- 졸업 요건 충족 최소 학기 수 계산 (Critical Path)

### 기술사 판단 포인트

| 상황 | 판단 |
|:---|:---|
| 사이클 감지 필요 | Kahn's [[001_algorithm_definition|알고리즘]] (결과 크기 [[396_validation|확인]]) |
| [[430_index_fast_full_scan|병렬]] 실행 최적화 | Kahn's 레벨별 처리 (같은 큐의 항목 = [[430_index_fast_full_scan|병렬]] 가능) |
| 역후위 순서 필요 | [[034_dfs|DFS]] 기반 위상 정렬 |
| 최장 경로([[150_cpm_critical_path_method|CPM]]) | 위상 정렬 순서로 DP 적용 |
| [[070_graph_datastructure|그래프]]에 사이클 가능성 | 위상 정렬 불가 → [[040_scc|SCC]] 분해 후 [[401_bayesian_network_dag_causality|DAG]] 변환 |

📢 **섹션 요약 비유**: 위상 정렬은 건설 현장의 작업 스케줄표 같다. 기초 공사 → 골조 → 외벽 → 내장 순서가 지켜져야 하며, 어느 단계도 뒤바꿀 수 없다.

## Ⅴ. 기대효과 및 결론

위상 정렬 (Topological Sort)은 O(V+E)의 효율로 DAG의 선행 [[083_relationship_in_er_model|관계]]를 선형 순서로 정렬한다. Kahn's [[001_algorithm_definition|알고리즘]]은 사이클 감지와 [[430_index_fast_full_scan|병렬]] 처리 최적화에 유리하고, [[034_dfs|DFS]] 기반은 구현이 간결하다. 위상 정렬 + DP로 Critical Path Method까지 확장된다.

**핵심 결론**: 의존 [[083_relationship_in_er_model|관계]]가 있는 모든 시스템에서 위상 정렬은 "무엇을 먼저 해야 하는가?"를 O(V+E)에 답한다.

📢 **섹션 요약 비유**: 위상 정렬은 도미노를 세울 때 넘어뜨릴 순서를 정하는 것이다. 앞 도미노가 쓰러지지 않으면 뒤 도미노를 세울 수 없고, 순환 고리가 있으면 아예 불가능하다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]) | 전제 조건 | 사이클 없는 방향 [[070_graph_datastructure|그래프]] |
| [[034_dfs|DFS]] (Depth-First Search) | 구현 기반 | 역후위 순서로 위상 정렬 |
| [[035_bfs|BFS]] (Breadth-First Search) | Kahn's 기반 | in-degree 추적 [[035_bfs|BFS]] |
| [[037_cpm|Critical Path Method]] ([[150_cpm_critical_path_method|CPM]]) | 응용 | 위상 정렬 + DP |
| [[040_scc|SCC]] (Strongly Connected Components) | 관련 | 사이클 [[070_graph_datastructure|그래프]]를 DAG로 변환 |
| [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] | 실무 활용 | [[401_bayesian_network_dag_causality|DAG]] 기반 워크플로우 엔진 |

### 📈 관련 키워드 및 발전 흐름도

```text
[방향 비순환 그래프 (DAG — Directed Acyclic Graph) — 위상 정렬의 전제 조건]
    │
    ▼
[진입 차수 (In-degree) 기반 탐색 — Kahn 알고리즘으로 순서 결정]
    │
    ▼
[깊이 우선 탐색 (DFS) 기반 위상 정렬 — 후위 순회로 역순 배치]
    │
    ▼
[빌드 의존성 해소 (Build Dependency) — Make·Gradle에서 컴파일 순서 결정]
    │
    ▼
[작업 스케줄링 (Task Scheduling) — 선행 작업 제약을 지키는 CPM·PERT 경로 분석]
```

이 흐름은 [[401_bayesian_network_dag_causality|DAG]] 구조 파악에서 실무 빌드 시스템·프로젝트 스케줄링까지 위상 정렬이 적용되는 맥락을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명

1. 🍳 라면을 끓일 때 물을 먼저 끓이고, 그 다음 면을 넣고, 마지막에 스프를 넣는 것처럼 순서가 정해진 작업을 늘어놓는 것이 위상 정렬이다.
2. 🔄 "물을 끓이려면 면이 필요하고, 면을 넣으려면 물이 필요하다"는 순환이 생기면 위상 정렬이 불가능하다 — 현실에서도 이런 순환은 막혀있다.
3. 🏗️ 건물 지을 때 기초 없이 벽을 세울 수 없듯, 컴퓨터 프로그램도 위상 정렬로 "먼저 설치해야 할 패키지"를 파악한다.
