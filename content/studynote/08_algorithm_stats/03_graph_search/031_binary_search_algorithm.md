---
title: "log n"
date: "2026-04-21"
tags:
  - "studynote-algorithm-stats"
weight: 31
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정렬된 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 탐색 범위를 매 단계 절반으로 줄여 O(log n) 시간에 목표를 찾는 [분할 정복](/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/) 기반 탐색이다.
> 2. **가치**: n=10억 개 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서도 최대 30번의 비교로 탐색 완료 — 정렬 비용을 한 번 치르면 이후 모든 탐색을 O(log n)으로 처리한다.
> 3. **판단 포인트**: off-by-one 오류와 [정수 오버플로우](/studynote/09_security/04_endpoint_security/333_integer_overflow/)(mid = left + (right-left)/2 사용) 및 Lower/Upper Bound 변형으로 중복 원소도 정밀 처리한다.

## Ⅰ. 개요 및 필요성

이진 탐색 (Binary Search)은 정렬된 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 left, right, mid 세 포인터를 이용해 탐색 범위를 반씩 줄여나가는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 매 단계에서 mid 위치의 값과 목표값을 비교하여 왼쪽 또는 오른쪽 절반으로 탐색 범위를 좁힌다.

| 특성 | 내용 |
|:---|:---|
| [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | O(log n) |
| [공간 복잡도](/studynote/08_algorithm_stats/01_basics/003_space_complexity/) | O(1) 반복 / O(log n) [재귀](/studynote/08_algorithm_stats/01_basics/014_recursion/) 호출 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) |
| 전제 조건 | [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)이 정렬되어 있어야 함 |
| 적합 조건 | 크기가 크고 탐색 빈도가 높은 정렬 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) |

이진 탐색이 필요한 상황:

- 대규모 정렬 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 탐색 ([DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 조회 테이블, 주소록, IP 차단 목록)
- 단조 함수에서 조건을 만족하는 경계값 탐색 (Parametric Search)
- Lower Bound / Upper Bound 활용한 범위 카운팅

📢 **섹션 요약 비유**: 두꺼운 국어사전에서 "사과"를 찾을 때 처음부터 읽지 않고 중간을 펼쳐 "ㅅ"인지 확인하는 방식이 이진 탐색이다. 1,000페이지 사전도 최대 10번만 펼쳐보면 된다.

## Ⅱ. 아키텍처 및 핵심 원리

### 기본 동작 순서

```
정렬된 배열: [1, 3, 5, 7, 9, 11, 13, 15]   목표: 9

단계 1: left=0, right=7, mid=3 -> arr[3]=7 < 9 -> left=4
단계 2: left=4, right=7, mid=5 -> arr[5]=11 > 9 -> right=4
단계 3: left=4, right=4, mid=4 -> arr[4]=9 == 9 -> 반환(4)  ✓
```

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 — 이진 탐색 포인터 이동

```
+--------------------------------------------------------------+
|  배열:  [ 1]  [ 3]  [ 5]  [ 7]  [ 9]  [11]  [13]  [15]      |
|  index:   0     1     2     3     4     5     6     7         |
|                                                              |
|  Step1:  L=0              M=3                    R=7         |
|          +------------ arr[3]=7 < 9 ------------ +          |
|                           -> left = M+1 = 4                   |
|                                                              |
|  Step2:                  L=4   M=5               R=7         |
|                          +--- arr[5]=11 > 9 ---- +          |
|                                  -> right = M-1 = 4           |
|                                                              |
|  Step3:                  L=4  M=4  R=4                       |
|                           +-- arr[4]=9 == 9 --+              |
|                               -> Found! 반환(4)               |
+--------------------------------------------------------------+
```

### Lower Bound / Upper Bound

중복 원소가 있는 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 특정 값의 첫 위치(Lower Bound) 또는 마지막 위치 다음(Upper Bound)을 구하는 변형이다.

| 변형 | 조건 변경 | 결과 |
|:---|:---|:---|
| 기본 이진 탐색 | `arr[mid] == target` 즉시 반환 | 임의의 위치 |
| Lower Bound | `arr[mid] >= target` -> right=mid | 첫 번째 위치 |
| Upper Bound | `arr[mid] > target` -> right=mid | 마지막+1 위치 |

```
배열: [2, 3, 3, 3, 5, 7]   target=3

Lower Bound -> index 1  (첫 번째 3의 위치)
Upper Bound -> index 4  (마지막 3의 다음 위치)
개수 = Upper - Lower = 4 - 1 = 3
```

### Parametric Search (매개변수 탐색)

"최솟값 X를 구하라 — X가 조건을 만족하면 X+1, X+2, ...도 만족한다"는 단조 조건 문제에 이진 탐색을 적용한다.

```
탐색 공간: [F, F, F, F, T, T, T, T]  (F=불만족, T=만족)
이진 탐색: 경계(첫 번째 T)를 O(log(범위)) 안에 탐색
활용: 나무 자르기(최대 높이), 적중률(최소 거리), git bisect
```

📢 **섹션 요약 비유**: Lower Bound는 "이 성적 이상인 학생 중 제일 먼저 등록한 사람"을 찾는 것처럼, 조건을 만족하는 최초 위치를 정밀하게 겨냥한다.

## Ⅲ. 비교 및 연결

### 이진 탐색 vs 다른 탐색

| 항목 | 이진 탐색 | [선형 탐색](/studynote/08_algorithm_stats/03_graph_search/030_linear_search/) | [해시 탐색](/studynote/08_algorithm_stats/03_graph_search/032_hash_search/) |
|:---|:---:|:---:|:---:|
| 평균 [시간 복잡도](/studynote/08_algorithm_stats/01_basics/002_time_complexity/) | O(log n) | O(n) | O(1) |
| 정렬 필요 | 필수 | 불필요 | 불필요 |
| 추가 공간 | O(1) | O(1) | O(n) |
| 범위 탐색 | 가능 | 가능 | 불가 |
| n=10억 기준 비교 수 | ~30 | ~500백만 | ~1 |

### 흔한 오류 3가지

1. **off-by-one**: `while (left < right)` vs `while (left <= right)` 차이로 무한 루프 또는 탐색 실패
2. <strong><a href="/studynote/09_security/04_endpoint_security/333_integer_overflow/">정수 오버플로우</a></strong>: `mid = (left + right) / 2` -> left+right가 int 범위 초과 가능 -> `mid = left + (right - left) / 2` 사용
3. **비정렬 적용**: 정렬 전제가 깨진 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에 적용 시 오탐 (회전 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)은 조건부 이진 탐색 사용)

📢 **섹션 요약 비유**: off-by-one 오류는 계단에서 마지막 계단을 한 칸 더 내딛는 실수와 같다. 딱 한 칸 차이가 추락을 만든다.

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

**시나리오 1**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) IP 차단 목록 조회 (n=500만)
- [선형 탐색](/studynote/08_algorithm_stats/03_graph_search/030_linear_search/): 최대 500만 비교 -> 패킷 [처리 지연](/studynote/03_network/01_data_communication/019_처리_지연/) 발생
- 이진 탐색: 최대 23번 비교 (log₂ 5,000,000 ≈ 22.9)
- -> 정렬된 차단 목록에서 이진 탐색으로 실시간 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 확보

**시나리오 2**: git bisect (버그 커밋 이진 탐색)
- "이 커밋부터 버그가 발생한다" — git bisect는 Parametric Search
- O(log n) 단계로 수천 개 커밋에서 버그 도입 커밋 탐색

**시나리오 3**: DB [B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)
- [B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) (Balanced Tree)의 노드 내 키 탐색은 이진 탐색 활용
- MySQL InnoDB, PostgreSQL [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)의 핵심 내부 탐색 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

### 기술사 판단 포인트

| 판단 항목 | 설명 |
|:---|:---|
| 정렬 비용 vs 탐색 이득 | 반복 탐색이면 정렬 O(n log n) 비용은 금방 회수됨 |
| Parametric Search 적용 | 결정 문제로 변환 가능한 최적화 문제에 활용 |
| Lower/Upper Bound | 중복 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 및 범위 카운팅에 필수 |
| [B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) 연계 | DB [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 설계의 이론적 기반 |

📢 **섹션 요약 비유**: 기술사 관점에서 이진 탐색은 "[인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 설계했느냐"의 은유다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 미리 정렬·인덱싱한 시스템은 모든 검색 비용을 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 스케일로 낮춘다.

## Ⅴ. 기대효과 및 결론

이진 탐색 (Binary Search)은 O(log n)이라는 압도적 효율로 대규모 정렬 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색의 표준이다. 단순한 탐색을 넘어 Parametric Search로 최적화 문제를 결정 문제로 변환하고, Lower/Upper Bound로 중복 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 정밀 처리한다.

**핵심 결론**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 번 정렬해두면, 이후 모든 탐색 비용을 영구히 O(log n)으로 낮출 수 있다. 정렬은 탐색에 대한 투자다.

📢 **섹션 요약 비유**: 이진 탐색은 100층 건물에서 엘리베이터를 타는 것이다. [선형 탐색](/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)이 계단을 한 층씩 오른다면, 이진 탐색은 중간 층을 찍고 올라갈지 내려갈지 결정하며 7번 만에 도착한다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| Lower Bound | 변형 | 조건 만족 최솟값 위치 |
| Upper Bound | 변형 | 조건 만족 마지막+1 위치 |
| Parametric Search | 응용 | 단조 함수 최적화 -> 결정 문제 변환 |
| [B-Tree](/studynote/08_algorithm_stats/04_datastructure/064_b_tree/) [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 활용 | DB [인덱스](/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 노드 내 탐색 |
| git bisect | 활용 | 버그 커밋 이진 탐색 |
| 회전 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 탐색 | 변형 | 조건부 이진 탐색 적용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Lower Bound]
    |
    v
[Upper Bound]
    |
    v
[Parametric Search]
    |
    v
[B-Tree 인덱스]
    |
    v
[git bisect]
```

이 흐름도는 Lower Bound에서 출발해 회전 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 탐색까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 📖 두꺼운 국어사전에서 "사과"를 찾을 때 중간을 펼쳐 "ㅅ"이면 앞쪽으로, "ㅎ"이면 뒤쪽으로 넘기는 방식이 이진 탐색이다.
2. ✂️ 매번 남은 범위를 정확히 절반으로 자르기 때문에, 1,000개 중에서 찾아도 최대 10번이면 충분하다.
3. 📏 단, 사전처럼 알파벳 순서로 정렬되어 있어야 한다 — 뒤섞인 책에서는 중간을 펼쳐도 아무 의미가 없다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 175

<- **이전**: [1. 선형 탐색 (Linear Search) — O(n)](/studynote/08_algorithm_stats/03_graph_search/030_linear_search/)
**다음**: [3. 해시 탐색 (Hash Search) — O(1) 평균](/studynote/08_algorithm_stats/03_graph_search/032_hash_search/) ->

---
