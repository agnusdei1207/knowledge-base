+++
title = "2. 행렬 분해 (Matrix Decomposition) — LU / QR / SVD"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 행렬 분해는 *복잡한 행렬을 구조가 명확한 작은 행렬들의 곱으로 분해*하는 것 — LU(삼각), QR(직교×상삼각), [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) ([Singular Value Decomposition](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/), [특이값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/342_svd/)) 각각이 다른 특성을 활용한다.
> 2. **가치**: [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) A = UΣVᵀ는 모든 실수 행렬에 적용 가능하며, [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)·[추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)·이미지 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)·최소제곱 풀이·의사역행렬을 하나의 프레임워크로 통합한다.
> 3. **판단 포인트**: 분해 선택 기준 — 최소제곱(QR), 반복 풀이(LU), 최저 랭크 근사·[차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)·추천([SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)). 수치 안정성은 [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) > QR > LU 순서다.

---

## Ⅰ. 개요 및 필요성

행렬 분해는 원래 행렬의 구조를 드러내어 계산 효율과 수치 안정성을 높인다.

| 분해 | 형태 | 조건 | 주요 용도 |
|:---|:---|:---|:---|
| LU 분해 | A = LU | 정방 행렬, det≠0 | 반복 선형 풀이 |
| QR 분해 | A = QR | 임의 직사각 행렬 | 최소제곱, 고유값 |
| [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) | A = UΣVᵀ | 임의 행렬 | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), 추천, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |
| [고유값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/) | A = PΛP⁻¹ | 정방 대각화 가능 | 고유값 문제 |
| 콜레스키 | A = LLᵀ | 대칭 양정치 | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/), 최적화 |

📢 **섹션 요약 비유**: 행렬 분해는 "복잡한 레고를 기본 블록으로 분해"하는 것이다 — 복잡한 변환(행렬)을 단순한 회전·스케일·반사로 쪼개면 이해와 계산이 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) ([Singular Value Decomposition](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)) 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">A = U · Σ · Vᵀ</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">m × n</div><div class="kb-diagram-cell">=</div><div class="kb-diagram-cell">m × m</div><div class="kb-diagram-cell">×</div><div class="kb-diagram-cell">m × n</div><div class="kb-diagram-cell">×</div><div class="kb-diagram-cell">n × n</div></div>
<div class="kb-diagram-note">(원본 행렬) (좌 특이벡터) (특이값 대각) (우 특이벡터)</div>
</div>
</div>



- **U**: 열이 좌 특이벡터 (Left Singular Vectors), UᵀU = I
- **Σ**: 대각 원소 σ₁ ≥ σ₂ ≥ ... ≥ σᵣ ≥ 0 (특이값, Singular Values)
- **Vᵀ**: 행이 우 특이벡터 (Right Singular Vectors), VᵀV = I

### 저랭크 근사 (Low-Rank Approximation)

SVD의 최대 강점 — **에카르트-영 (Eckart-Young) 정리**:

```
Aₖ = Σᵢ₌₁ᵏ σᵢ uᵢ vᵢᵀ

는 rank-k 행렬 중 A에 가장 가까운 행렬 (Frobenius 노름 최소화)
```

k=1, 2, 3... 으로 증가시키며 점진적 근사:

```
원본 A (rank r)
    ↓ SVD
A ≈ σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + ... + σₖuₖvₖᵀ
   (가장 중요한 k개 성분만 사용)
```

### 이미지 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 예시

```
원본 이미지 행렬 A (512×512):
  저장: 512² = 262,144 픽셀

SVD 후 k=50 성분 유지:
  저장: k(m+n+1) = 50(512+512+1) = 51,250 값
  압축비: 262,144 / 51,250 ≈ 5.1배

화질 결정: 상위 k개 특이값이 전체 변동의 몇 %를 설명하는가?
```

### QR 분해 구조

A = QR (Q: 직교, R: 상삼각)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">a₁₁ a₁₂ a₁₃ q₁₁ q₁₂ q₁₃ r₁₁ r₁₂ r₁₃</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">a₂₁ a₂₂ a₂₃</div><div class="kb-diagram-cell">=</div><div class="kb-diagram-cell">q₂₁ q₂₂ q₂₃</div><div class="kb-diagram-cell">×</div><div class="kb-diagram-cell">0 r₂₂ r₂₃</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">a₃₁ a₃₂ a₃₃ q₃₁ q₃₂ q₃₃ 0 0 r₃₃</div>
<div class="kb-diagram-note">직교 행렬 Q 상삼각 R</div>
</div>
</div>



최소제곱 풀이 Ax ≈ b (m > n):
```
QRx = b → Rx = Qᵀb  → 후방 대입으로 풀기
```

QR 분해는 가우스 소거보다 수치적으로 안정적.

📢 **섹션 요약 비유**: SVD의 저랭크 근사는 "가장 중요한 특징 몇 개로 초상화 그리기"다 — 세밀한 부분을 일부 포기하더라도 가장 중요한 σ₁, σ₂, σ₃ 성분으로 원본을 잘 표현한다.

---

## Ⅲ. 비교 및 연결

### SVD와 [고유값 분해](/knowledge-base/studynote/10_ai/05_data_science_ml/341_eigenvalue_decomposition/)의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

대칭 행렬 A = Aᵀ의 경우:
- 고유분해 A = QΛQᵀ (Q: 직교, Λ: 대각)
- 이것은 SVD와 동일 (U = Q, Σ = |Λ|, V = Q)

일반 행렬에서 SVD와 고유값의 연결:
```
AᵀA = VΣ²Vᵀ   → AᵀA의 고유벡터 = V, 고유값 = σᵢ²
AAᵀ = UΣ²Uᵀ   → AAᵀ의 고유벡터 = U, 고유값 = σᵢ²
```

### 의사역행렬 (Pseudoinverse, Moore-Penrose)

A가 정방이 아니거나 역행렬이 없을 때 SVD로 계산:

```
A⁺ = VΣ⁺Uᵀ

Σ⁺: σᵢ ≠ 0이면 1/σᵢ, σᵢ = 0이면 0
```

최소 노름 최소제곱 해: x* = A⁺b

### 응용 영역 정리

| 응용 | 분해 | 핵심 역할 |
|:---|:---|:---|
| [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) | [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) / 고유분해 | 공분산 행렬 분해 |
| [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/) | [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) (행렬 인수분해) | 사용자-아이템 잠재 요인 |
| 자연어처리 LSA | [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) | 단어-문서 행렬 저랭크 근사 |
| 이미지 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) | 저랭크 근사 |
| 최소제곱 회귀 | QR / [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) | 수치 안정 풀이 |
| 선형 방정식 반복 | LU | 빠른 재풀이 |

📢 **섹션 요약 비유**: 의사역행렬은 "불완전한 정보의 최선 답"이다 — 완벽한 역행렬이 없어도 SVD로 구한 A⁺가 "최대한 정확한" 해를 제공한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [협업 필터링](/knowledge-base/studynote/06_ict_convergence/05_data_science/345_collaborative_filtering/) — [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) 기반 추천 (Netflix Prize)

사용자-영화 평점 행렬 R (m×n, 대부분 비어있음):

```
R ≈ Uₖ · Σₖ · Vₖᵀ   (rank-k 근사)

U (m×k): 사용자 잠재 요인 행렬
V (n×k): 아이템 잠재 요인 행렬

예측: R̂(u, i) = uᵤᵀ vᵢ
```

행렬 분해(MF, [Matrix Factorization](/knowledge-base/studynote/06_ict_convergence/05_data_science/348_matrix_factorization/)) 기반 추천이 Netflix Prize(2009)에서 우승.

### [주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/) ([PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)) 연결

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 행렬 X (n×p, 중심화 완료):

```
X = UΣVᵀ

주성분 = Vᵀ 의 행들 (우 특이벡터)
주성분 점수 = UΣ (좌 특이벡터 × 특이값)
분산 설명량 = σᵢ² / Σ σⱼ²
```

### 기술사 판단 포인트

1. **"정방 행렬에 가장 일반적인 분해는?"** → LU (det≠0), 고유분해 (대각화 가능)
2. **"수치 안정성이 가장 좋은 분해는?"** → [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/)
3. **"최소제곱 문제의 표준 풀이는?"** → QR 분해 (Normal Equation AᵀAx=Aᵀb보다 안정)

📢 **섹션 요약 비유**: [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) 기반 추천은 "음악 취향 DNA"와 같다 — 각 사용자를 몇 개의 잠재 취향 벡터(U)로, 각 곡을 잠재 장르 벡터(V)로 표현해 유사도를 계산한다.

---

## Ⅴ. 기대효과 및 결론

행렬 분해는 **선형대수의 정수** — 복잡한 연산을 단순 구조로 분해해 수치 안정성, 계산 효율, 수학적 통찰을 동시에 제공한다.

SVD는 특히:
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 본질적 구조(잠재 요인)를 드러내고
- 노이즈와 신호를 특이값 크기로 분리하며
- 의사역행렬을 통해 역행렬 불가능한 시스템에도 최선의 해를 제공한다

NumPy: `np.linalg.svd()`, PyTorch: `torch.linalg.svd()` — 현대 ML 프레임워크에서 기본 내장.

📢 **섹션 요약 비유**: SVD는 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 X선 촬영"이다 — 원본 행렬(겉모습)을 분해해 그 안에 숨겨진 중요한 구조(뼈대, σ₁≥σ₂≥...)를 드러낸다.

---

### 📌 관련 개념 맵

| 분해 | 수식 | 핵심 응용 |
|:---|:---|:---|
| LU | A = LU | 선형 방정식 반복 풀이 |
| QR | A = QR | 최소제곱, 고유값 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [SVD](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/230_svd_matrix_factorization_random_forest_xgboost_boosting/) | A = UΣVᵀ | [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/), 추천, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 의사역행렬 |
| 고유분해 | A = PΛP⁻¹ | 대각화, PageRank |
| 콜레스키 | A = LLᵀ | [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 모델, 최적화 |

---

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">LU</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">QR</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SVD</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">고유분해</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">콜레스키</div></div>
</div>
</div>



이 흐름도는 LU에서 출발해 콜레스키까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **LU는 "계단 청소"**: 복잡한 청소를 위층(U)과 아래층(L)으로 나눠 차례로 한다.
2. **SVD는 "사진 핵심 요소 분리"**: 배경(큰 σ)과 세부(작은 σ)를 분리해, 중요한 것만 남겨 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)한다.
3. **저랭크 근사는 "대략의 초상화"**: 몇 가지 핵심 특징만으로 사람 얼굴을 알아볼 수 있을 만큼 표현하는 것.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 161 / 175

← **이전**: [1. 선형 연립방정식 — 행렬 표현, 가우스 소거](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/160_linear_equations/)
**다음**: [3. 고유값/고유벡터 (Eigenvalue/Eigenvector) — Av = λv](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/162_eigenvalue_eigenvector/) →

---
