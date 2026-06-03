+++
title = "044. t-SNE — 고차원 데이터 시각화"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

> **핵심 인사이트**
> 1. t-SNE(t-distributed Stochastic Neighbor [Embedding](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/))는 고차원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 국소적 구조(Local Structure)를 2~3차원으로 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 비선형 [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/) 기법으로 — 유사한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트를 가깝게, 상이한 포인트를 멀리 배치하여 클러스터 구조를 직관적으로 드러낸다.
> 2. t-SNE의 핵심은 고차원 공간의 가우시안 분포 유사도와 저차원 공간의 t-분포(자유도 1, 코시 분포) 유사도 사이의 KL Divergence를 최소화하는 것으로 — t-분포의 두꺼운 꼬리(Heavy Tail)가 "군집 붕괴 문제(Crowding Problem)"를 해결하는 핵심이다.
> 3. t-SNE는 [탐색적 데이터 분석](/knowledge-base/studynote/14_data_engineering/02_math_mining/062_eda_exploratory_data_analysis/)([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/))과 모델 디버깅에는 강력하지만 — 퍼플렉시티(Perplexity) 하이퍼파라미터에 민감하고 전역 구조 보존이 약하며 계산량이 O(n²)이라 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 직접 적용이 어려워, UMAP이 실용적 대안으로 부상하고 있다.

---

## Ⅰ. t-SNE 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">t-SNE (t-distributed Stochastic Neighbor Embedding):</div>
<div class="kb-diagram-note">van der Maaten &amp; Hinton, 2008년 제안</div>
<div class="kb-diagram-note">목적:</div>
<div class="kb-diagram-note">고차원 데이터 (100~수만 차원) → 2~3차원 시각화</div>
<div class="kb-diagram-note">클러스터 구조 탐색</div>
<div class="kb-diagram-note">SNE (Stochastic Neighbor Embedding):</div>
<div class="kb-diagram-note">t-SNE의 전신</div>
<div class="kb-diagram-note">고차원: 가우시안 분포로 유사도 계산</div>
<div class="kb-diagram-note">저차원: 가우시안 분포로 유사도 계산</div>
<div class="kb-diagram-note">문제: 군집 붕괴 (Crowding Problem)</div>
<div class="kb-diagram-note">고차원 중간 거리 점들이 저차원에서 모두 가운데 몰림</div>
<div class="kb-diagram-note">t-SNE 개선:</div>
<div class="kb-diagram-note">저차원 공간에 t-분포 (자유도=1) 사용</div>
<div class="kb-diagram-note">→ 두꺼운 꼬리로 멀리 떨어진 점들을 더 멀리 배치</div>
<div class="kb-diagram-note">→ Crowding Problem 해결</div>
<div class="kb-diagram-note">직관적 이해:</div>
<div class="kb-diagram-note">1. 각 점을 중심으로 "이웃 확률 분포" 계산</div>
<div class="kb-diagram-note">고차원: P(j|i) = 가까울수록 높은 확률</div>
<div class="kb-diagram-note">2. 저차원에서 같은 분포 재현 시도</div>
<div class="kb-diagram-note">Q(j|i): t-분포 기반 유사도</div>
<div class="kb-diagram-note">3. P와 Q의 차이(KL Divergence) 최소화</div>
<div class="kb-diagram-note">Gradient Descent로 저차원 좌표 최적화</div>
</div>
</div>



> 📢 **섹션 요약 비유**: t-SNE는 3D 지도 → 2D 지도 변환 — 나라(고차원 점)들을 비슷한 것끼리 가깝게, 다른 것끼리 멀게 배치. t-분포는 섬나라(멀리 떨어진 그룹)를 바다 건너 확실히 분리.

---

## Ⅱ. t-SNE [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">t-SNE 알고리즘 상세:</div>
<div class="kb-diagram-note">1단계: 고차원 유사도 계산</div>
<div class="kb-diagram-note">입력: N개의 고차원 점 x1, ..., xN</div>
<div class="kb-diagram-note">조건부 확률 (가우시안):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P(j</div><div class="kb-diagram-cell">i) = exp(-</div><div class="kb-diagram-cell">xi-xj</div><div class="kb-diagram-cell">² / 2σi²) / Σk≠i exp(-</div><div class="kb-diagram-cell">xi-xk</div><div class="kb-diagram-cell">² / 2σi²)</div></div>
<div class="kb-diagram-note">σi: 퍼플렉시티(Perplexity)에 의해 결정</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P(ij) = (P(j</div><div class="kb-diagram-cell">i) + P(i</div><div class="kb-diagram-cell">j)) / 2N ← 대칭화</div></div>
<div class="kb-diagram-note">2단계: 저차원 유사도 계산</div>
<div class="kb-diagram-note">저차원 좌표: y1, ..., yN (초기화: 랜덤 or PCA)</div>
<div class="kb-diagram-note">t-분포 기반:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Q(ij) = (1 +</div><div class="kb-diagram-cell">yi-yj</div><div class="kb-diagram-cell">²)^(-1) / Σk≠l (1 +</div><div class="kb-diagram-cell">yk-yl</div><div class="kb-diagram-cell">²)^(-1)</div></div>
<div class="kb-diagram-note">3단계: KL Divergence 최소화</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C = KL(P</div><div class="kb-diagram-cell">Q) = Σij P(ij) log(P(ij)/Q(ij))</div></div>
<div class="kb-diagram-note">Gradient:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">dC/dyi = 4 Σj (P(ij) - Q(ij)) (yi-yj) (1+</div><div class="kb-diagram-cell">yi-yj</div><div class="kb-diagram-cell">²)^(-1)</div></div>
<div class="kb-diagram-note">경사하강법으로 반복 최적화</div>
<div class="kb-diagram-note">퍼플렉시티 (Perplexity):</div>
<div class="kb-diagram-note">유효 이웃 수 설정 (5~50, 보통 30)</div>
<div class="kb-diagram-note">낮은 Perplexity: 국소 구조 강조</div>
<div class="kb-diagram-note">높은 Perplexity: 전역 구조 반영</div>
<div class="kb-diagram-note">데이터 크기에 따라 조정:</div>
<div class="kb-diagram-note">소규모 (&lt;1,000): Perplexity 5~15</div>
<div class="kb-diagram-note">중간 (1,000~10,000): 20~50</div>
<div class="kb-diagram-note">대규모: 100 이상</div>
<div class="kb-diagram-note">계산 복잡도:</div>
<div class="kb-diagram-note">기본: O(n²)</div>
<div class="kb-diagram-note">Barnes-Hut 근사: O(n log n)</div>
<div class="kb-diagram-note">→ 10만 개 이상 데이터에는 별도 최적화 필요</div>
</div>
</div>



> 📢 **섹션 요약 비유**: t-SNE [KL Divergence](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/153_kl_divergence/) 최소화는 지그소 퍼즐 맞추기 — 원본 사진(고차원 P)과 만들어진 퍼즐(저차원 Q)이 최대한 일치하도록 조각 위치를 조금씩 조정.

---

## Ⅲ. t-SNE vs [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) vs UMAP

```
차원 축소 기법 비교:

PCA (Principal Component Analysis):
  선형 변환: 분산 최대 방향으로 투영
  장점: 빠름, 전역 구조 보존, 결정론적
  단점: 비선형 구조 포착 불가
  용도: 전처리, 노이즈 제거

t-SNE:
  비선형 변환
  장점: 클러스터 구조 시각화 강력
  단점:
    - 전역 구조 보존 약함 (클러스터 간 거리 무의미)
    - O(n²) 계산 복잡도
    - 하이퍼파라미터 민감 (Perplexity)
    - 재현성 없음 (랜덤 초기화)
    - 새로운 점 추가 시 재실행 필요
  용도: EDA, 클러스터 탐색

UMAP (Uniform Manifold Approximation and Projection):
  Leland McInnes et al., 2018년
  비선형, 위상수학(Topology) 기반
  
  장점:
    - t-SNE보다 빠름 (O(n) 근사)
    - 전역 구조도 어느 정도 보존
    - 재현성 (random_state)
    - 새 점 추가 변환 가능 (transform 메서드)
  
  단점:
    - 이해하기 어려운 수학 기반

비교표:
항목        | PCA    | t-SNE  | UMAP
------------|--------|--------|-------
선형성      | 선형   | 비선형 | 비선형
속도        | 빠름   | 느림   | 중간
전역 구조   | 강     | 약     | 중간
클러스터    | 약     | 강     | 강
재현성      | 있음   | 없음   | 있음
대규모 데이터| 가능  | 어려움 | 가능
```

> 📢 **섹션 요약 비유**: [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) vs t-SNE vs UMAP은 지도 만들기 방법 — PCA는 직선 도로만, t-SNE는 구불구불한 마을 골목까지, UMAP은 골목도 잡으면서 더 빨리 그려요.

---

## Ⅳ. t-SNE 주의사항



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">t-SNE 오용 패턴:</div>
<div class="kb-diagram-note">1. 클러스터 간 거리 해석:</div>
<div class="kb-diagram-note">잘못: "클러스터 A와 B가 C보다 더 유사하다"</div>
<div class="kb-diagram-note">이유: t-SNE는 전역 구조 보존 안 함</div>
<div class="kb-diagram-note">→ 클러스터 간 거리는 무의미</div>
<div class="kb-diagram-note">2. 클러스터 크기 해석:</div>
<div class="kb-diagram-note">잘못: "A 클러스터가 B보다 크다"</div>
<div class="kb-diagram-note">이유: t-SNE 클러스터 크기 ≠ 원래 데이터 밀도</div>
<div class="kb-diagram-note">3. Perplexity 기본값 신뢰:</div>
<div class="kb-diagram-note">권장: 여러 Perplexity 값으로 시각화 비교</div>
<div class="kb-diagram-note">Perplexity 5: 매우 타이트한 클러스터 (의도적 분리)</div>
<div class="kb-diagram-note">Perplexity 50: 느슨한 배치 (전체적 경향)</div>
<div class="kb-diagram-note">4. 노이즈 클러스터 착시:</div>
<div class="kb-diagram-note">작은 점 하나가 별개 클러스터로 보이는 경우</div>
<div class="kb-diagram-note">→ 실제 아웃라이어인지 확인 필요</div>
<div class="kb-diagram-note">5. 랜덤 초기화 의존:</div>
<div class="kb-diagram-note">매번 다른 레이아웃</div>
<div class="kb-diagram-note">→ 결론 전에 여러 번 실행, 일관된 패턴 확인</div>
<div class="kb-diagram-note">올바른 t-SNE 사용:</div>
<div class="kb-diagram-tree-item" style="--depth:1">"이 데이터에 클러스터 구조가 있는가?" 탐색</div>
<div class="kb-diagram-tree-item" style="--depth:1">ML 모델 임베딩 품질 시각적 확인</div>
<div class="kb-diagram-tree-item" style="--depth:1">클래스 간 분리 가능성 시각화 (레이블 색상)</div>
<div class="kb-diagram-tree-item" style="--depth:1">이상치(Outlier) 탐지 보조</div>
</div>
</div>



> 📢 **섹션 요약 비유**: t-SNE 오용 주의는 지도 해석 주의 — 지도에서 두 도시가 가깝다고 실제로 가까운 게 아닐 수 있어요. t-SNE 거리는 "동네 구조"를 보여주지만 "전국 거리"는 안 보여줘요.

---

## Ⅴ. 실무 시나리오 — 텍스트 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">BERT 텍스트 임베딩 t-SNE 시각화:</div>
<div class="kb-diagram-note">목적: 뉴스 기사 카테고리 임베딩 품질 확인</div>
<div class="kb-diagram-note">데이터:</div>
<div class="kb-diagram-note">20,000개 뉴스 기사</div>
<div class="kb-diagram-note">카테고리: 정치, 경제, 스포츠, 연예, IT, 의학</div>
<div class="kb-diagram-note">BERT 임베딩: 각 기사 → 768차원 벡터</div>
<div class="kb-diagram-note">t-SNE 적용:</div>
<div class="kb-diagram-note">from sklearn.manifold import TSNE</div>
<div class="kb-diagram-note">import matplotlib.pyplot as plt</div>
<div class="kb-diagram-note"># PCA로 사전 압축 (100차원, 속도 향상)</div>
<div class="kb-diagram-note">from sklearn.decomposition import PCA</div>
<div class="kb-diagram-note">pca = PCA(n_components=100)</div>
<div class="kb-diagram-note">X_pca = pca.fit_transform(X_bert) # (20000, 768) → (20000, 100)</div>
<div class="kb-diagram-note"># t-SNE</div>
<div class="kb-diagram-note">tsne = TSNE(n_components=2, perplexity=40,</div>
<div class="kb-diagram-note">n_iter=1000, random_state=42)</div>
<div class="kb-diagram-note">X_tsne = tsne.fit_transform(X_pca) # (20000, 100) → (20000, 2)</div>
<div class="kb-diagram-note"># 시각화</div>
<div class="kb-diagram-note">plt.figure(figsize=(12, 8))</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">scatter = plt.scatter(X_tsne</div><div class="kb-diagram-node">:,0</div><div class="kb-diagram-note">, X_tsne</div><div class="kb-diagram-node">:,1</div><div class="kb-diagram-note">,</div></div>
<div class="kb-diagram-note">c=labels, cmap='tab10', s=1)</div>
<div class="kb-diagram-note">plt.colorbar(scatter)</div>
<div class="kb-diagram-note">plt.title("BERT 임베딩 t-SNE 시각화")</div>
<div class="kb-diagram-note">결과 해석:</div>
<div class="kb-diagram-note">좋은 임베딩:</div>
<div class="kb-diagram-tree-item" style="--depth:1">각 카테고리가 명확히 분리된 클러스터</div>
<div class="kb-diagram-tree-item" style="--depth:1">경계가 선명함</div>
<div class="kb-diagram-note">나쁜 임베딩:</div>
<div class="kb-diagram-tree-item" style="--depth:1">카테고리들이 섞임</div>
<div class="kb-diagram-tree-item" style="--depth:1">구분 불가능</div>
<div class="kb-diagram-note">발견:</div>
<div class="kb-diagram-tree-item" style="--depth:1">경제 + IT: 부분적 혼합 (경제기술 뉴스 중복)</div>
<div class="kb-diagram-tree-item" style="--depth:1">스포츠: 매우 명확한 분리 (도메인 특화)</div>
<div class="kb-diagram-note">활용: 임베딩 방법 비교 (BERT vs RoBERTa vs GPT)</div>
<div class="kb-diagram-note">미세조정(Fine-tuning) 전후 임베딩 품질 비교</div>
<div class="kb-diagram-note">대규모 처리:</div>
<div class="kb-diagram-note">20,000건: t-SNE 약 5분</div>
<div class="kb-diagram-note">200,000건: UMAP 권장 (5분 내 처리)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [BERT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/) t-SNE [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 언어의 지도 — 각 뉴스가 2D 지도에 찍히는데, 같은 카테고리끼리 동네를 이루면 "좋은 [임베딩](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/278_instruction_tuning/)!", 섞이면 "모델 개선 필요!".

---

## 📌 관련 개념 맵

```
t-SNE
+-- 알고리즘
|   +-- 고차원: 가우시안 유사도 (P)
|   +-- 저차원: t-분포 유사도 (Q)
|   +-- KL Divergence 최소화
+-- 하이퍼파라미터
|   +-- Perplexity (5~50)
|   +-- n_iter (반복 횟수)
+-- 비교
|   +-- PCA (선형, 빠름)
|   +-- UMAP (비선형, 빠름, 재현성)
+-- 주의사항
|   +-- 클러스터 간 거리 무의미
|   +-- 전역 구조 보존 약함
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[PCA (1901)]
선형 차원 축소 표준
통계 기반 분산 최대화
      |
      v
[SNE (2002)]
Hinton & Roweis: 비선형 이웃 임베딩
군집 붕괴 문제 미해결
      |
      v
[t-SNE (2008)]
van der Maaten & Hinton
t-분포로 군집 붕괴 해결
      |
      v
[UMAP 등장 (2018)]
더 빠르고 전역 구조 보존
t-SNE 대체 트렌드
      |
      v
[현재: 딥러닝 임베딩 시각화]
BERT, GPT 임베딩 탐색 도구
TensorBoard Embedding Projector
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. t-SNE는 3D 지도를 2D로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) — 수백 개의 특징(차원)을 가진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 평면에 찍어서 "비슷한 것끼리 뭉치게" 표현해요!
2. t-분포의 두꺼운 꼬리가 핵심 — 멀리 있는 그룹들을 더 확실히 떼어놓는 것이 t-SNE의 비법이에요. 인근 동네는 붙이고, 먼 도시는 확실히 분리!
3. 클러스터 간 거리는 무시해요 — t-SNE는 "동네 내부 구조"를 잘 보여주지만, "도시 간 실제 거리"는 믿으면 안 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 44 / 420

← **이전**: [043. SVD — 특이값 분해 (Singular Value Decomposition)](/knowledge-base/studynote/10_ai/01_ai_basics/043_svd/)
**다음**: [045. K-평균 군집화 — K-Means Clustering](/knowledge-base/studynote/10_ai/01_ai_basics/045_kmeans/) →

---
