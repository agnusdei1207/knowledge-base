---
sidebar:
  order: 35
  label: "035. 클러스터링: K-Means•DBSCAN (Clustering)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "클러스터링: K-Means•DBSCAN (Clustering)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-basic-theory"
weight: 35
extra:
  question_no: "035"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "군집 형태•밀도에 따른 알고리즘 선택 기준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클러스터링(Clustering, 군집화)**: 정답 레이블(Label)이 없는 상태에서 데이터 간의 거리, 유사도, 밀도 연결성에 기반하여 유사한 데이터 포인트들을 동질한 그룹으로 묶는 비지도 학습(Unsupervised Learning) 기법.
- **K-Means**: 사전에 지정된 $k$개의 군집 중심(Centroid)을 설정하고 유클리드 거리 기반 최근접 중심 할당과 중심점 재계산을 반복하여 오차제곱합(SSE)을 최소화하는 분할 군집 알고리즘.
- **DBSCAN(Density-Based Spatial Clustering of Applications with Noise)**: 특정 반경($\varepsilon$) 내 최소 이웃 수($\text{MinPts}$)를 만족하는 밀도 연결성(Density Reachability)을 기반으로 임의 형상의 군집을 형성하고 이상치를 노이즈로 격리하는 밀도 기반 군집 알고리즘.

</details>

- 정의/개념: 정답 레이블 없이 데이터 포인트 간의 거리 척도(Distance Metric) 또는 공간 밀도(Density)를 측정하여 유사 집단으로 분할하는 **비지도 머신러닝 분석 기법**
- 배경/필요성: 고객 세분화(Segmentation), 이상 거래 탐지, 이미지 분할 등에서 **대규모 비정형 데이터의 내재적 패턴 식별 및 데이터 구조 탐색 필수**

#### 한줄 요약

- 데이터의 거리와 밀도 연결성을 기반으로 레이블 없는 데이터를 자율적으로 그룹화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **실루엣 계수(Silhouette Coefficient, $s$)**: 군집 내 응집도($a$)와 최근접 이웃 군집과의 분리도($b$)를 비교하여 군집 품질을 $[-1, 1]$로 평가하는 지표 ($s = \frac{b-a}{\max(a, b)}$).
- **엘보우 기법(Elbow Method)**: 군집 수 $k$ 증가에 따른 군집 내 오차제곱합(SSE)의 감소율 둔화 지점을 찾아 최적 $k$를 결정하는 휴리스틱 기법.

</details>

- K-Means의 빠른 연산 속도($O(Nkt)$) 및 **구형(Spherical) 볼록 군집 분할 특성**
- DBSCAN의 **임의 기하 형상(Non-convex) 군집 탐색 및 노이즈(Outlier) 자동 분리**
- 거리 척도(유클리드, 맨해튼, 코사인) 및 **특징 정규화(Standardization)에 따른 결과 민감성**

#### 한줄 요약

- K-Means는 사전 지정된 구형 군집에 최적화되고, DBSCAN은 밀도 연결성으로 비볼록 형상과 노이즈를 분리

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **DBSCAN 핵심 3대 포인트**:
  - 핵심점 (Core Point): $\varepsilon$ 반경 내에 $\text{MinPts}$개 이상의 이웃을 보유한 포인트.
  - 경계점 (Border Point): 핵심점의 $\varepsilon$ 반경 내에 속하지만 스스로는 $\text{MinPts}$를 만족하지 못하는 포인트.
  - 잡음점 (Noise Point): 어떤 핵심점의 $\varepsilon$ 반경에도 속하지 않는 고립된 이상치.

</details>

```text
[ 군집화 아키텍처 및 DBSCAN 밀도 구조 ]
┌──────────────────────────────┐
│ 특징 전처리기 (Scaler)       │ ── StandardScaler / MinMaxScaler 거리 왜곡 방지
├──────────────────────────────┤
│ K-Means 엔진                 │ ── k개 센트로이드 배정 ──► 유클리드 최근접 갱신
├──────────────────────────────┤
│ DBSCAN 엔진                  │ ── ε 반경 탐색 ──► [Core | Border | Noise] 분류
├──────────────────────────────┤
│ 군집 품질 평가기 (Evaluator) │ ── 실루엣 계수, Davies-Bouldin Index 산출
└──────────────────────────────┘
```

선의 의미: 데이터 전처리 스케일링, 분할/밀도 군집 엔진, 평가 지표 간의 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 특징 전처리기 | 차원 간 단위 차이를 제거하여 **공정한 거리 척도 환경 조성** |
| 군집 중심 (Centroid) | K-Means 군집의 **평균 위치 벡터($\mu_k$) 보관 및 갱신** |
| 밀도 파라미터 ($\varepsilon, \text{MinPts}$) | DBSCAN의 **이웃 반경 및 핵심점 판정 임계치 정의** |
| 군집 평가기 | **실루엣 계수($s$) 및 엘보우 곡선**으로 군집 분리도 및 타당성 평가 |

#### 한줄 요약

- 전처리기가 거리 단위를 맞추고, 군집 모델이 점을 묶으면 평가기가 분리도와 업무 활용성을 확인

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **K-Means++ 초기화**: 초기 중심점 간의 거리에 비례하는 확률로 다음 중심을 선정하여 지역 최솟값(Local Minima) 수렴 문제를 획기적으로 개선한 초기화 알고리즘.

</details>

```text
레이블 없는 고차원 데이터셋 입력
   │
   ▼
[ 1. 특징 표준화 전처리 (Z-Score 정규화) ]
   │
   ▼
[ 2. 군집 특성 판별 ]
├─ 군집 수 k 파악 가능 & 구형 군집
│  │
│  ▼
│  [ 3. K-Means++ 초기화 및 최근접 센트로이드 할당/평균 갱신 루프 ]
│  │
│  └─ 중심점 위치 변동 없을 때까지 수렴
│
└─ 군집 수 미지 & 비볼록 임의 형상/노이즈 혼재
   │
   ▼
   [ 4. k-distance 그래프로 ε 산출 후 DBSCAN 밀도 확장 및 노이즈 분리 ]
   │
   ▼
[ 5. 실루엣 계수 및 도메인 업무 해석 검증 ]
```

**동작 원리**

1. **데이터 표준화**: 변수 간 척도 차이에 의한 거리 왜곡을 방지하기 위해 Z-Score 표준화 적용
2. **군집 알고리즘 분기**: 데이터의 분포 형상과 노이즈 유무에 따라 K-Means 또는 DBSCAN 선택
3. **K-Means 실행**: K-Means++로 초기 중심을 설정하고 최근접 할당 및 중심 이동을 반복 수렴
4. **DBSCAN 실행**: $\varepsilon$ 반경과 $\text{MinPts}$로 핵심점을 찾아 밀도 연결성으로 군집을 확장하고 노이즈 격리
5. **품질 평가**: 실루엣 계수와 도메인 해석 가능성을 평가하여 최종 군집 확정

#### 한줄 요약

- 데이터를 정규화한 후 구형은 K-Means 중심 이동으로, 임의 형상은 DBSCAN 밀도 확장으로 군집화

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **K-Means vs DBSCAN**:
  - K-Means: 군집 수 $k$ 사전 지정, 유클리드 거리 중심 분할, 볼록 구형 군집에 한정, 노이즈에 취약.
  - DBSCAN: 군집 수 자동 결정, 밀도 연결성 기반, 초승달/도넛 등 비볼록 임의 형상 수용, 노이즈 완전 분리.

</details>

| 비교 항목 | K-Means 군집화 | DBSCAN 군집화 |
|:---|:---|:---|
| 군집 수 ($k$) | **사전에 사용자 지정 필수** | **데이터 밀도로 자동 결정** |
| 군집 형상 | **볼록한 구형(Spherical) 군집에 국한** | **도넛/초승달 등 임의 기하 형상(Non-convex)** |
| 이상치 처리 | 모든 점을 군집에 강제 배정 (노이즈에 취약) | **노이즈(Noise Point)로 자동 분리 및 격리** |
| 하이퍼파라미터 | 군집 수 $k$, 초기화 기법 | 이웃 반경($\varepsilon$), 최소 이웃 수($\text{MinPts}$) |
| 계산 복잡도 | $O(N \cdot k \cdot t)$ (대규모 데이터에 고속) | $O(N^2)$ (Kd-Tree 적용 시 $O(N \log N)$) |

#### 한줄 요약

- 균일한 구형 데이터는 K-Means, 복잡한 비볼록 형상과 이상치 분리는 DBSCAN을 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **HDBSCAN(Hierarchical DBSCAN)**: 데이터 공간 내 밀도가 서로 다른 다중 밀도 군집이 혼재할 때, 단일 $\varepsilon$의 한계를 극복하고 상이한 밀도의 군집을 계층적으로 자동 추출하는 진보된 밀도 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 변수 간 척도 차이로 인한 **특정 피처의 거리 지배** | `StandardScaler` 기반 **Z-Score 표준화** 필수 적용 | 모든 특징의 공정한 거리 기여 보장 |
| K-Means의 **초기 중심점 선택에 따른 지역해 수렴** | **K-Means++ 초기화** 및 다중 재시작(`n_init=10`) | 군집 수렴의 안정성 및 전역 최적화 |
| DBSCAN에서 군집 간 밀도 차이로 인한 **군집 붕괴** | **HDBSCAN(Hierarchical DBSCAN)** 알고리즘 전환 | 가변 밀도 데이터의 계층적 군집 분리 |
| 고차원 데이터($D > 50$)의 **차원의 저주(거리 변별력 상실)** | **PCA / UMAP / t-SNE** 차원 축소 선행 적용 | 의미 있는 잠재 공간에서의 군집 형성 |

#### 한줄 요약

- 스케일 차이는 StandardScaler로 정규화하고, K-Means 초기화는 K-Means++로 안정화하며, 가변 밀도에는 HDBSCAN을 적용하고 고차원 데이터는 UMAP으로 축소한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **비지도 데이터 분석 설계 표준**: 고객 세그먼트처럼 대략적인 그룹 수가 정의된 경우는 K-Means를, 이상치 탐지나 공간 지리 데이터 분석처럼 불규칙한 밀도 패턴은 DBSCAN/HDBSCAN을 선택하는 최적화 원칙.

</details>

- 구형 중심 분할은 **K-Means**, 기하학적 임의 형상/노이즈 분리는 **DBSCAN** 선택

#### 한줄 요약

- 구형 군집은 K-Means, 임의 형상과 잡음 분리는 DBSCAN을 선택하고 업무 해석을 검증
