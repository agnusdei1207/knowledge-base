+++
title = "047. 계층적 군집화 — Hierarchical Clustering"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

> **핵심 인사이트**
> 1. [계층적 군집화](/knowledge-base/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/)(Hierarchical [Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 트리 형태의 덴드로그램(Dendrogram)으로 표현하는 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — k-means와 달리 군집 수를 사전에 결정할 필요 없고, 덴드로그램을 어느 높이에서 자르느냐에 따라 다양한 군집 수를 얻을 수 있다.
> 2. 응집형(Agglomerative) vs 분리형(Divisive) 두 접근법 — 응집형은 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트를 독립 군집으로 시작해 유사한 것끼리 합치고(아래→위), 분리형은 전체를 하나의 군집으로 시작해 나누는 방식(위→아래)이다. 실무에서는 응집형이 훨씬 많이 사용된다.
> 3. 연결 방법(Linkage)이 군집 모양을 결정 — 단일 연결(Single)은 체인 효과로 길쭉한 군집, 완전 연결(Complete)은 컴팩트한 구형 군집, Ward 연결은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 최소화로 균일한 크기 군집을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하며, Ward 방법이 일반적으로 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 보인다.

---

## Ⅰ. [계층적 군집화](/knowledge-base/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/) 개요



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">계층적 군집화 두 방향:</div>
<div class="kb-diagram-note">응집형 (Agglomerative, Bottom-Up):</div>
<div class="kb-diagram-note">초기: 각 데이터 포인트 = 독립 군집 (N개 군집)</div>
<div class="kb-diagram-note">단계: 가장 유사한 두 군집 합치기</div>
<div class="kb-diagram-note">종료: 모두 하나의 군집 (1개)</div>
<div class="kb-diagram-note">N → N-1 → N-2 → ... → 2 → 1</div>
<div class="kb-diagram-note">복잡도: O(n³) 또는 O(n² log n)</div>
<div class="kb-diagram-note">분리형 (Divisive, Top-Down):</div>
<div class="kb-diagram-note">초기: 모든 데이터 = 하나의 군집</div>
<div class="kb-diagram-note">단계: 가장 이질적인 군집 나누기</div>
<div class="kb-diagram-note">종료: 각 포인트가 독립 군집</div>
<div class="kb-diagram-note">1 → 2 → ... → N-1 → N</div>
<div class="kb-diagram-note">더 복잡, 덜 사용됨</div>
<div class="kb-diagram-note">덴드로그램 (Dendrogram):</div>
<div class="kb-diagram-note">계층적 군집화의 시각화</div>
<div class="kb-diagram-note">y축: 군집 간 거리 (합병 시 거리)</div>
<div class="kb-diagram-note">x축: 데이터 포인트</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">A ─</div>
<div class="kb-diagram-note">B ─ ─</div>
<div class="kb-diagram-note">C ─</div>
<div class="kb-diagram-note">D</div>
<div class="kb-diagram-note">A와 B가 먼저 합쳐짐 (유사)</div>
<div class="kb-diagram-note">C가 AB에 합쳐짐</div>
<div class="kb-diagram-note">D가 ABC에 합쳐짐</div>
<div class="kb-diagram-note">군집 수 결정 (덴드로그램 절단):</div>
<div class="kb-diagram-note">덴드로그램을 특정 높이에서 절단</div>
<div class="kb-diagram-note">→ 그 높이의 가지 수 = 군집 수</div>
<div class="kb-diagram-note">최적 절단: 가장 긴 수직선 위치 (가장 큰 거리 점프)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [계층적 군집화](/knowledge-base/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/)는 가족 족보 — 개인([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) → 가족 → 씨족 → 민족 → 인류. 덴드로그램은 족보 그림. 어느 세대까지 볼지(절단)는 내가 결정!

---

## Ⅱ. 연결 방법 (Linkage)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">연결 방법 비교:</div>
<div class="kb-diagram-note">단일 연결 (Single Linkage = MIN):</div>
<div class="kb-diagram-note">두 군집 간 거리 = 가장 가까운 두 점의 거리</div>
<div class="kb-diagram-note">Dist(C1, C2) = min{dist(a,b): a∈C1, b∈C2}</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">체인 효과 (Chaining Effect): 하나씩 이어붙임</div>
<div class="kb-diagram-note">긴 사슬 모양 군집 생성</div>
<div class="kb-diagram-note">이상치 민감</div>
<div class="kb-diagram-note">적합: 고리 형태 군집, 연결 클러스터</div>
<div class="kb-diagram-note">완전 연결 (Complete Linkage = MAX):</div>
<div class="kb-diagram-note">두 군집 간 거리 = 가장 먼 두 점의 거리</div>
<div class="kb-diagram-note">Dist(C1, C2) = max{dist(a,b): a∈C1, b∈C2}</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">컴팩트한 구형 군집</div>
<div class="kb-diagram-note">이상치에 강함 (최대 거리 기준)</div>
<div class="kb-diagram-note">균일한 크기 군집</div>
<div class="kb-diagram-note">적합: 구형 군집, 노이즈 있는 데이터</div>
<div class="kb-diagram-note">평균 연결 (Average Linkage = UPGMA):</div>
<div class="kb-diagram-note">두 군집 간 모든 쌍의 평균 거리</div>
<div class="kb-diagram-note">Dist(C1, C2) = avg{dist(a,b): a∈C1, b∈C2}</div>
<div class="kb-diagram-note">특성: Single과 Complete의 중간</div>
<div class="kb-diagram-note">Ward 연결:</div>
<div class="kb-diagram-note">합병 시 군집 내 분산(WCSS) 증가량 최소화</div>
<div class="kb-diagram-note">Dist(C1, C2) = 합병 후 WCSS - (C1 WCSS + C2 WCSS)</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">균일한 크기의 컴팩트한 군집</div>
<div class="kb-diagram-note">대부분 상황에서 최고 성능</div>
<div class="kb-diagram-note">권장: 일반적으로 Ward 방법이 기본 선택</div>
<div class="kb-diagram-note">비교 시각화:</div>
<div class="kb-diagram-note">단일: A B C D (체인)</div>
<div class="kb-diagram-note">완전: A─ B─ (두 덩어리)</div>
<div class="kb-diagram-note">C─ D─</div>
<div class="kb-diagram-note">Ward: 균일한 크기 덩어리</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 연결 방법은 반 편성 기준 — 단일(가장 친한 친구 기준: 체인 효과), 완전(가장 멀리 있는 애도 같은 반), Ward(비슷한 능력 그룹). 대부분 Ward가 최선!

---

## Ⅲ. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">응집형 계층적 군집화 알고리즘:</div>
<div class="kb-diagram-note">입력: n개 데이터 포인트</div>
<div class="kb-diagram-note">출력: 덴드로그램</div>
<div class="kb-diagram-note">의사코드 (단순 버전):</div>
<div class="kb-diagram-note">1. 거리 행렬 D 계산 (n×n)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">D</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">= dist(xi, xj)</div></div>
<div class="kb-diagram-note">2. 각 포인트 = 독립 군집 (C = {C1, C2, ..., Cn})</div>
<div class="kb-diagram-note">3. n-1 반복:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">- 가장 작은 D</div><div class="kb-diagram-node">Ci, Cj</div><div class="kb-diagram-note">찾기</div></div>
<div class="kb-diagram-tree-item" style="--depth:2">Ci와 Cj 합병 → Ck</div>
<div class="kb-diagram-tree-item" style="--depth:2">덴드로그램 기록 (합병 거리, 높이)</div>
<div class="kb-diagram-tree-item" style="--depth:2">D 업데이트 (Ck와 나머지 군집 거리 재계산)</div>
<div class="kb-diagram-tree-item" style="--depth:2">C에서 Ci, Cj 제거, Ck 추가</div>
<div class="kb-diagram-note">4. 덴드로그램 반환</div>
<div class="kb-diagram-note">Python 구현:</div>
<div class="kb-diagram-note">from scipy.cluster.hierarchy import linkage, dendrogram</div>
<div class="kb-diagram-note">from scipy.spatial.distance import pdist</div>
<div class="kb-diagram-note">import matplotlib.pyplot as plt</div>
<div class="kb-diagram-note"># 거리 계산 + 계층 군집화</div>
<div class="kb-diagram-note">Z = linkage(X, method='ward', metric='euclidean')</div>
<div class="kb-diagram-note"># 덴드로그램 시각화</div>
<div class="kb-diagram-note">dendrogram(Z, labels=labels, color_threshold=5)</div>
<div class="kb-diagram-note">plt.show()</div>
<div class="kb-diagram-note"># 특정 군집 수로 절단</div>
<div class="kb-diagram-note">from scipy.cluster.hierarchy import fcluster</div>
<div class="kb-diagram-note">labels = fcluster(Z, t=3, criterion='maxclust')</div>
<div class="kb-diagram-note">시간 복잡도:</div>
<div class="kb-diagram-note">Naive: O(n³)</div>
<div class="kb-diagram-note">SLINK (Single): O(n²)</div>
<div class="kb-diagram-note">CLINK (Complete): O(n²)</div>
<div class="kb-diagram-note">Ward (Lance-Williams): O(n² log n)</div>
<div class="kb-diagram-note">n = 10,000:</div>
<div class="kb-diagram-note">O(n³) = 10^12 → 수 시간</div>
<div class="kb-diagram-note">→ 대규모 데이터: k-means 선호</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 계층 군집 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 거리 기반 합치기 — 거리표(D) 보면서 가장 가까운 둘을 계속 합쳐요. 족보가 완성될 때까지!

---

## Ⅳ. 평가와 비교

```
군집화 평가 지표:

외부 지표 (레이블 알 때):
  ARI (Adjusted Rand Index):
  0~1 (1 = 완벽 일치)
  
  NMI (Normalized Mutual Information):
  0~1 (정보 공유 정도)

내부 지표 (레이블 모를 때):
  실루엣 점수:
  범위: -1 ~ 1
  1: 완벽한 군집
  0: 군집 경계
  -1: 잘못 분류됨
  
  코펜헤틱 상관 계수 (Cophenetic Correlation):
  덴드로그램이 원본 거리를 얼마나 반영하는가
  높을수록 좋은 계층 군집화

k-means vs 계층 군집화:

| 항목 | k-means | 계층 군집 |
|------|---------|----------|
| 군집 수 | 사전 지정 | 사후 결정 |
| 형태 | 구형 | 임의 |
| 속도 | O(nk) 빠름 | O(n²) 느림 |
| 해석 | 어려움 | 덴드로그램 |
| 이상치 | 민감 | 방법에 따라 |

선택 가이드:
  n < 1,000: 계층 군집화 (덴드로그램 시각화)
  n > 10,000: k-means (속도)
  군집 수 모름: 계층 군집화 → 절단 결정
  구형 군집: k-means
  임의 형태: DBSCAN 또는 계층(단일 연결)
```

> 📢 **섹션 요약 비유**: [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) 선택은 도구 선택 — 손톱(k-means: 빠르고 표준), 드라이버(계층: 다양한 형태), 렌치([DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/): [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)). 상황에 맞는 도구!

---

## Ⅴ. 실무 시나리오 — 고객 세그먼트 분석



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">온라인 쇼핑몰 고객 세그먼트:</div>
<div class="kb-diagram-note">데이터:</div>
<div class="kb-diagram-note">1,000명 고객</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">특성:</div><div class="kb-diagram-node">구매 빈도, 평균 금액, 마지막 구매 일수 (RFM)</div></div>
<div class="kb-diagram-note">전처리:</div>
<div class="kb-diagram-note">StandardScaler로 정규화 (단위 통일)</div>
<div class="kb-diagram-note">계층적 군집화 적용:</div>
<div class="kb-diagram-note">Z = linkage(X_scaled, method='ward')</div>
<div class="kb-diagram-note">덴드로그램 분석:</div>
<div class="kb-diagram-note">y=5 높이에서 가장 긴 수직선</div>
<div class="kb-diagram-note">→ 절단 높이 = 5 → 4개 군집 최적</div>
<div class="kb-diagram-note">군집 해석 (4개):</div>
<div class="kb-diagram-note">군집 0: VIP 고객 (빈도 높음, 금액 높음, 최근)</div>
<div class="kb-diagram-note">군집 1: 충성 고객 (빈도 중간, 금액 중간)</div>
<div class="kb-diagram-note">군집 2: 휴면 고객 (빈도 낮음, 오래됨)</div>
<div class="kb-diagram-note">군집 3: 신규 고객 (최근, 빈도 낮음)</div>
<div class="kb-diagram-note">마케팅 활용:</div>
<div class="kb-diagram-note">VIP: 프리미엄 멤버십 초대</div>
<div class="kb-diagram-note">충성: 포인트 더블 이벤트</div>
<div class="kb-diagram-note">휴면: 재활성화 캠페인 이메일</div>
<div class="kb-diagram-note">신규: 첫 구매 할인 → 재구매 유도</div>
<div class="kb-diagram-note">k-means 대비 장점:</div>
<div class="kb-diagram-note">군집 수(4개) 덴드로그램으로 결정</div>
<div class="kb-diagram-note">(k-means: 미리 k=4로 지정해야)</div>
<div class="kb-diagram-note">군집 계층 분석:</div>
<div class="kb-diagram-note">VIP와 충성 고객이 먼저 합쳐짐 (유사)</div>
<div class="kb-diagram-note">→ 함께 "우량 고객" 캠페인도 가능</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">휴면 고객 캠페인 응답률: 12% (업계 평균 5%)</div>
<div class="kb-diagram-note">신규→충성 전환율: 28% (이전 15%)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 고객 세그먼트 분석은 손님 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) — 덴드로그램으로 VIP·충성·휴면·신규 4그룹 자동 발견. k-means 달리 그룹 수도 자동으로 알아내요!

---

## 📌 관련 개념 맵

```
계층적 군집화
+-- 유형
|   +-- 응집형 (Agglomerative, 주류)
|   +-- 분리형 (Divisive)
+-- 연결 방법
|   +-- 단일 (체인 효과)
|   +-- 완전 (컴팩트)
|   +-- Ward (분산 최소화, 권장)
+-- 시각화
|   +-- 덴드로그램
|   +-- 코펜헤틱 상관 계수
+-- vs k-means
    +-- 속도: k-means 유리
    +-- 해석: 계층 군집 유리
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 군집 분석 (1950s~)]
생물학적 분류법에서 시작
      |
      v
[Ward 방법 (1963)]
분산 최소화 기준
계층 군집화 표준화
      |
      v
[UPGMA, SLINK (1969~)]
분자 생물학 계통 분류
빠른 알고리즘 개발
      |
      v
[대규모 BIRCH (1996)]
n² 한계 극복 시도
      |
      v
[현재: 고차원+대규모]
sklearn 통합
차원 축소(t-SNE) 후 적용
생물정보학 표준 도구
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 계층 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)는 족보 만들기 — 개인([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) → 가족 → 씨족 → 민족 → 인류. 덴드로그램은 족보 그림!
2. 연결 방법은 반 편성 기준 — Ward는 비슷한 성적끼리 균일 배치, 단일은 친구 한 명이라도 있으면 합류(체인 효과)!
3. 덴드로그램 절단은 어느 세대까지 볼지 — 덴드로그램을 높이 5에서 자르면 4개 그룹. 내가 원하는 그룹 수를 사후 선택!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 47 / 420

← **이전**: [046. DBSCAN — 밀도 기반 군집화](/knowledge-base/studynote/10_ai/01_ai_basics/046_dbscan/)
**다음**: [048. 이상 탐지 — Anomaly Detection](/knowledge-base/studynote/10_ai/01_ai_basics/048_anomaly_detection/) →

---
