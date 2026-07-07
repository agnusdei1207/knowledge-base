---
title: "고유값·고유벡터 (Eigenvalue Eigenvector)"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 37
---

# 037. 고유값·고유벡터 (Eigenvalue Eigenvector)

## Ⅰ. Overview

고유값($Eigenvalue$)과 고유벡터($Eigenvector$)는 선형 변환 시 방향이 변하지 않는 특수한 축과 그 축으로의 신축 배율을 의미함. 행렬이라는 복잡한 변환의 '뼈대'를 추출하는 선형대수학의 핵심 개념임.

### 가. 핵심 개념 정의
1.  **고유값 ($\lambda$):** 선형 변환 후 벡터의 크기가 변화하는 배율임.
2.  **고유벡터 ($x$):** 선형 변환 $A$를 가했을 때 방향은 변하지 않고 크기만 상수배($\lambda$)가 되는 $0$이 아닌 벡터임. ($Ax = \lambda x$)
3.  **특성 방정식 ($Characteristic$ $Equation$):** 고유값을 구하기 위한 방정식으로, $\det(A - \lambda I) = 0$을 만족하는 $\lambda$를 찾음.

## Ⅱ. Features

### 가. 고유값 분석과 특이값 분해(SVD)의 비교

| 항목 | 고유값 분석 ($Eigen$-$Analysis$) | 특이값 분해 ($SVD$) |
| :--- | :--- | :--- |
| **대상 행렬** | 정방 행렬 ($Square$ $Matrix$) | 모든 형태의 행렬 ($Rectangular$) |
| **물리적 의미** | 시스템의 불변 축 탐색 | 데이터의 최적 기저 축 탐색 |
| **분해 형태** | $A = V \Lambda V^{-1}$ | $A = U \Sigma V^T$ |
| **수치적 안정성** | 대각화 불가능할 수 있음 ($Jordan$) | 항상 존재하며 수치적으로 안정적 |
| **주요 활용** | 시스템 안정성, $PageRank$ | 차원 축소, 추천 시스템, 영상 압축 |

### 나. 고유값의 주요 성질
- **Trace & Determinant:** 모든 고유값의 합은 $Tr(A)$와 같고, 곱은 $\det(A)$와 같음.
- **선형 독립성:** 서로 다른 고유값에 대응하는 고유벡터들은 서로 선형 독립임.
- **고유 공간 ($Eigenspace$):** 특정 고유값 $\lambda$에 대응하는 고유벡터들의 집합은 벡터 공간의 부분 공간을 형성함.

## Ⅲ. Architecture Insight

### 가. 고유값 도출 및 수치 해석 메커니즘
1.  **건조:** 특성 다항식 $P(\lambda) = \det(A - \lambda I)$를 구성함.
2.  **해 구하기:** $n$차 다항식의 근을 찾아 고유값 $\lambda_1, \dots, \lambda_n$을 도출함.
3.  **벡터 산출:** 각 $\lambda_i$에 대해 $(A - \lambda_i I)x = 0$을 만족하는 영공간($Null$ $Space$)의 기저를 구함.

### 나. 멱급수 방법 (Power Method)
거대 행렬에서 모든 고유값을 구하는 것은 $O(n^3)$ 이상의 비용이 발생함.
- **Power Method:** 임의의 벡터 $b_k$에 $A$를 반복적으로 곱하여 가장 큰 고유값($Dominant$ $Eigenvalue$)과 그에 대응하는 고유벡터를 빠르게 수렴시키는 수치적 기법임. $PageRank$ 알고리즘의 근간이 됨.

## Ⅳ. PPA & Trade-offs

### 가. PPA (Power, Performance, Area) 관점 분석
- **Power:** 복잡한 반복 연산($QR$ $Algorithm$ 등)은 전력 소모가 크며, 특히 수렴 속도에 따라 총 전력량이 결정됨.
- **Performance:** 행렬의 크기 $n$에 대해 $O(n^3)$의 연산량이 소요되나, 가속기($GPU$)를 통한 병렬화로 성능을 대폭 개선 가능함.
- **Area:** 대규모 행렬 분해를 위해 고성능 부동소수점 연산기($FPU$)와 넓은 메모리 대역폭이 필수적임.

### 나. 주요 Trade-offs
- **Precision vs Convergence:** 수치 정밀도를 높이면 수렴 횟수가 늘어나고 시간이 소요되지만, 결과의 안정성이 확보됨.
- **Approximation vs Exactness:** 모든 고유값을 구하는 대신 상위 $k$개의 지배적 성분만 추출하여 연산 효율과 정보량 사이의 타협점을 찾음 ($PCA$).

## Ⅴ. Real-world Troubleshooting

### 가. 대각화 불가능 (Non-diagonalizable) 문제
- **현상:** 고유값은 존재하지만 선형 독립인 고유벡터의 개수가 부족하여 $V \Lambda V^{-1}$ 형태의 분해가 불가능함.
- **해결:** **조르당 표준형($Jordan$ $Normal$ $Form$)**을 사용하거나, 복소수 범위로 확장하여 해석적 안정성을 확보함.

### 나. 수치적 예민함 (Ill-conditioning)
- **현상:** 행렬의 요소가 미세하게 변할 때 고유값이 크게 변동함 (조건수 $Condition$ $Number$가 큼).
- **해결:** 행렬의 스케일을 조절($Preconditioning$)하거나, 정규화($Regularization$)를 통해 수치적 특성을 개선함.

## Ⅵ. Professional Insight

고유값과 고유벡터는 데이터라는 혼돈 속에서 '질서의 축'을 찾아내는 눈과 같음. 기술사는 단순히 공식을 푸는 것을 넘어, 고유값이 가진 '에너지의 크기'와 고유벡터가 가진 '정보의 방향'을 서비스의 가치로 전환할 수 있어야 함.

특히 인공지능 분야의 $PCA$나 네트워크 분석의 $Centrality$ 측정 등에서 고유값 분석은 대체 불가능한 도구임. 최근에는 대규모 분산 환경에서 란초스($Lanczos$) 알고리즘 등을 활용하여 수십억 차원의 행렬에서 고유 성분을 추출하는 기술이 핵심 경쟁력이 되고 있음에 주목해야 함.
