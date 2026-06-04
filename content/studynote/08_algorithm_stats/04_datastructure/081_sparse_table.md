---
title: "27. 스파스 테이블 (Sparse Table) — 정적 RMQ 최적 자료구조"
date: "2026-04-29"
tags:
  - "studynote-algorithm-stats"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스파스 테이블(Sparse Table)은 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에서 구간 최솟값 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(RMQ, Range Minimum Query)를 O(1) 시간에 응답하기 위해 전처리(Preprocessing) O(n log n)를 수행하는 정적(Static) 자료구조로, 2의 거듭제곱 구간을 미리 계산·저장하여 겹침 허용(Overlap) 방식으로 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 처리한다.
> 2. **가치**: 스파스 테이블의 핵심은 "[멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/))"을 가진 연산(min, max, [gcd](/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/))에 대해 구간이 겹쳐도 결과가 오염되지 않는다는 점이다. 이 덕분에 구간을 두 개의 겹치는 구간으로 덮어 O(1) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)가 가능하다.
> 3. **판단 포인트**: 스파스 테이블은 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)이 변경되지 않는 정적 환경에서만 효율적이다. [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)이 동적으로 갱신되면 [Segment Tree](/studynote/12_it_management/02_itsm_itil/075_combinatorics/)(구간 업데이트 O(log n) + [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) O(log n))가 더 적합하다. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 대회([CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/))에서 [LCA](/studynote/12_it_management/02_itsm_itil/855_lca/)(Lowest Common Ancestor)와 결합하여 자주 출제된다.

---

## Ⅰ. 개요 및 필요성

```text
배열: [2, 4, 3, 1, 6, 7, 8, 9]
       0  1  2  3  4  5  6  7

RMQ(l, r) = [l, r] 범위에서 최솟값 쿼리
예: RMQ(1, 5) = min(4, 3, 1, 6, 7) = 1

나이브 방법: O(n) 쿼리 -> 쿼리 Q개면 O(nQ)
스파스 테이블: O(n log n) 전처리 -> O(1) 쿼리
```

- **📢 섹션 요약 비유**: 스파스 테이블은 미리 만들어둔 구간 최솟값 치트시트다. 모든 구간의 답을 미리 계산해두면(치트시트 준비), 질문이 들어왔을 때 즉시 답할 수 있다(O(1) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 스파스 테이블 구조

```text
st[j][i] = arr[i..i+2^j-1] 범위의 최솟값

예: arr = [2, 4, 3, 1, 6]
st[0][i] = arr[i] (길이 1)
st[1][0] = min(arr[0..1]) = min(2,4) = 2
st[1][1] = min(arr[1..2]) = min(4,3) = 3
st[2][0] = min(arr[0..3]) = min(2,4,3,1) = 1
```

### O(1) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 공식

```text
RMQ(l, r):
  k = floor(log2(r - l + 1))
  return min(st[k][l], st[k][r - 2^k + 1])

예: RMQ(1, 4), r-l+1=4, k=2
  min(st[2][1], st[2][4-4+1]) = min(st[2][1], st[2][1])
  = min(min(4,3,1,6), ...) = 1

왜 O(1)? 겹쳐도 min은 멱등성 -> 두 구간이 겹쳐도 정답
```

- **📢 섹션 요약 비유**: 겹침 허용 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 긴 자 하나로 두 번 재는 것이다. 1m짜리 자로 왼쪽 끝에서 1m, 오른쪽 끝에서 1m 재면 겹치지만, min(최솟값)은 겹쳐도 정답이 변하지 않는다.

---

## Ⅲ. 비교 및 연결

| 비교 | 스파스 테이블 | [세그먼트 트리](/studynote/12_it_management/02_itsm_itil/075_combinatorics/) | [펜윅 트리](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) |
|:---|:---|:---|:---|
| 전처리 | O(n log n) | O(n) | O(n) |
| [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | O(1) | O(log n) | O(log n) |
| 업데이트 | 불가 (정적) | O(log n) | O(log n) |
| 적용 연산 | 멱등 연산 (min/max/[gcd](/studynote/02_operating_system/10_security/663_macos_ios_gcd_grand_central_dispatch/)) | 모든 연산 | 합산 연산 |

- **📢 섹션 요약 비유**: 스파스 테이블은 완성된 백과사전이다. 이미 인쇄됐으므로 내용을 바꿀 수 없지만(정적), 원하는 정보를 즉시(O(1)) 찾을 수 있다. [세그먼트 트리](/studynote/12_it_management/02_itsm_itil/075_combinatorics/)는 디지털 위키피디아처럼 수정 가능하지만 검색이 약간 더 걸린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [LCA](/studynote/12_it_management/02_itsm_itil/855_lca/) (Lowest Common Ancestor) 응용
- 트리를 오일러 투어(Euler Tour)로 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)로 변환 -> RMQ 문제로 환원.
- Farach-Colton and Bender [Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/): 스파스 테이블로 [LCA](/studynote/12_it_management/02_itsm_itil/855_lca/) O(1) 달성.

### [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 대회 적용
- 구간 최솟값/최댓값 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 수 Q, 업데이트 없음 -> 스파스 테이블 O(n log n + Q).
- 구간 합 + 업데이트 -> [펜윅 트리](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/)/[세그먼트 트리](/studynote/12_it_management/02_itsm_itil/075_combinatorics/).

- **📢 섹션 요약 비유**: [LCA](/studynote/12_it_management/02_itsm_itil/855_lca/)+스파스 테이블은 가계도에서 공통 조상을 즉시 찾는 시스템이다. 가계도(트리)를 미리 정리해두면(전처리), 어떤 두 사람의 공통 조상도 즉시(O(1)) 확인할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong>O(1) <a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a></strong> | 정적 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) RMQ 최적 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| **구현 단순** | 2D [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) + log 전처리 |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/855_lca/">LCA</a> 결합</strong> | 트리 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 고속화 |

스파스 테이블은 정적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리의 극한 최적화 사례로, 생물정보학(유전체 서열 [LCA](/studynote/12_it_management/02_itsm_itil/855_lca/) 분석), 네트워크 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)(최단 경로 전처리), 시계열 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구간 집계에 활용된다.

- **📢 섹션 요약 비유**: 스파스 테이블은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 바뀌지 않는 환경의 최강 치트키다. 게임에서 모든 맵을 미리 탐색해 최단 경로 지도를 만들어두면(전처리), 어떤 경로 질문도 즉시 답할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **RMQ** | 스파스 테이블의 핵심 해결 문제 |
| <strong><a href="/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/">멱등성</a></strong> | 구간 겹침 허용 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)의 이론적 근거 |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/855_lca/">LCA</a></strong> | 스파스 테이블의 대표 응용 문제 |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/075_combinatorics/">세그먼트 트리</a></strong> | 동적 갱신이 필요할 때의 대안 |
| **오일러 투어** | 트리 -> [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) RMQ 변환 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[나이브 RMQ — O(n) 쿼리, 단순 순회]
    |
    v
[스파스 테이블 — O(n log n) 전처리, O(1) 쿼리]
    |
    v
[LCA 결합 — 트리 공통 조상 O(1) 탐색]
    |
    v
[세그먼트 트리 — 동적 갱신 + 구간 쿼리]
    |
    v
[퍼시스턴트 세그먼트 트리 — 버전별 히스토리 쿼리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 스파스 테이블은 미리 만들어둔 구간 최솟값 치트시트예요! 질문이 오면 치트시트를 바로 보면 되니까 O(1)로 즉시 답해요.
2. 두 구간이 겹쳐도 min(최솟값)은 정답이 바뀌지 않아요 - 이게 O(1) [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)의 비결이에요!
3. [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)이 바뀌면 치트시트를 새로 만들어야 하니, 변하지 않는 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)에서만 써야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 81 / 175

<- **이전**: [27. 힙 정렬 (Heap Sort) — 힙 자료구조 기반 비교 정렬](/studynote/08_algorithm_stats/04_datastructure/080_heap_sort/)
**다음**: [28. 블룸 필터 (Bloom Filter)](/studynote/08_algorithm_stats/04_datastructure/082_bloom_filter/) ->

---
