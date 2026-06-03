+++
title = "046. DBSCAN — 밀도 기반 군집화"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

> **핵심 인사이트**
> 1. [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/)([Density-Based Spatial Clustering](/knowledge-base/studynote/10_ai/05_data_science_ml/357_dbscan/) of Applications with Noise)은 밀도가 높은 지역을 군집으로 인식하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — k-means와 달리 군집 수(k)를 사전에 지정할 필요 없고, 임의 형태의 군집과 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)(Noise)를 자동으로 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)한다.
> 2. 핵심 매개변수 ε(엡실론)과 minPts — ε(이웃 반경)과 minPts(최소 이웃 점 수)의 조합이 군집 품질을 결정하며, k-거리 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(k-distance [graph](/knowledge-base/studynote/12_it_management/03_ea_isp/104_graph/))로 최적 ε을 찾는 방법이 실무에서 널리 사용된다.
> 3. DBSCAN의 한계: 고차원·가변 밀도 군집 — 차원이 높아질수록 거리 계산 의미 감소(차원의 저주)하고, 밀도가 다른 군집이 혼재할 때 단일 ε로 모든 군집을 적절히 잡기 어렵다. HDBSCAN이 이 한계를 개선한다.

---

## Ⅰ. [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) 개요



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">밀도 기반 군집화 직관:</div>
<div class="kb-diagram-note">k-means 한계:</div>
<div class="kb-diagram-note">원형 군집만 식별 가능</div>
<div class="kb-diagram-note">이상치에 민감</div>
<div class="kb-diagram-note">k를 미리 지정해야 함</div>
<div class="kb-diagram-note">DBSCAN 핵심 아이디어:</div>
<div class="kb-diagram-note">"밀도가 높은 지역 = 군집"</div>
<div class="kb-diagram-note">밀도 기준 이하 = 이상치(Noise)</div>
<div class="kb-diagram-note">직관: 별이 모여 있는 곳 = 별자리</div>
<div class="kb-diagram-note">홀로 떨어진 별 = 이상치</div>
<div class="kb-diagram-note">점 유형:</div>
<div class="kb-diagram-note">매개변수: ε (반경), minPts (최소 이웃)</div>
<div class="kb-diagram-note">핵심 점 (Core Point):</div>
<div class="kb-diagram-note">ε 반경 내 minPts개 이상 이웃</div>
<div class="kb-diagram-note">→ 밀도 충족 = 군집의 중심</div>
<div class="kb-diagram-note">경계 점 (Border Point):</div>
<div class="kb-diagram-note">ε 반경 내 minPts 미만 이웃</div>
<div class="kb-diagram-note">BUT 핵심 점의 ε 반경 내에 있음</div>
<div class="kb-diagram-note">→ 군집에 속하지만 중심 아님</div>
<div class="kb-diagram-note">잡음 점 (Noise Point):</div>
<div class="kb-diagram-note">핵심 점도 아니고 경계 점도 아님</div>
<div class="kb-diagram-note">→ 이상치 (Outlier)</div>
<div class="kb-diagram-note">예: ε=1, minPts=3</div>
<div class="kb-diagram-note">A• •B D•</div>
<div class="kb-diagram-note">•C •E •F (F = Noise)</div>
<div class="kb-diagram-note">A,B,C가 서로 ε 내에 있고 각각 3개 이웃</div>
<div class="kb-diagram-note">→ A,B,C = Core Points → 같은 군집</div>
<div class="kb-diagram-note">D,E = Border Points (핵심 점의 ε 내, 하지만 minPts 미달)</div>
<div class="kb-diagram-note">F = Noise</div>
</div>
</div>



> 📢 **섹션 요약 비유**: DBSCAN의 점 유형은 모임 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) — 핵심 점(모임 주최자: 주변에 친구 많음), 경계 점(참가자: 주최자 알지만 본인은 친구 적음), 잡음(아는 사람 없는 혼자)!

---

## Ⅱ. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 동작



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">DBSCAN 알고리즘:</div>
<div class="kb-diagram-note">입력: 데이터셋 D, ε, minPts</div>
<div class="kb-diagram-note">출력: 군집 레이블 (-1 = Noise)</div>
<div class="kb-diagram-note">의사코드:</div>
<div class="kb-diagram-note">1. 모든 점 미방문(unvisited)으로 초기화</div>
<div class="kb-diagram-note">2. 각 점 P에 대해:</div>
<div class="kb-diagram-note">이미 방문 → 건너뜀</div>
<div class="kb-diagram-note">P를 방문 표시</div>
<div class="kb-diagram-note">N = ε-이웃(P) (P에서 ε 내 모든 점)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if</div><div class="kb-diagram-cell">N</div><div class="kb-diagram-cell">&lt; minPts:</div></div>
<div class="kb-diagram-note">P = Noise (-1 표시) # 나중에 경계점이 될 수도 있음</div>
<div class="kb-diagram-note">else:</div>
<div class="kb-diagram-note">새 군집 C 생성</div>
<div class="kb-diagram-note">P를 C에 추가</div>
<div class="kb-diagram-note">씨앗 집합 S = N</div>
<div class="kb-diagram-note">while S 비어있지 않음:</div>
<div class="kb-diagram-note">Q = S에서 점 하나 꺼냄</div>
<div class="kb-diagram-note">Q 미방문이면: Q를 방문 표시</div>
<div class="kb-diagram-note">N' = ε-이웃(Q)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if</div><div class="kb-diagram-cell">N'</div><div class="kb-diagram-cell">&gt;= minPts:</div></div>
<div class="kb-diagram-note">S = S ∪ N'</div>
<div class="kb-diagram-note">Q가 어떤 군집에도 없으면: Q를 C에 추가</div>
<div class="kb-diagram-note">시간 복잡도:</div>
<div class="kb-diagram-note">이웃 탐색 O(n log n) (공간 인덱스)</div>
<div class="kb-diagram-note">전체: O(n log n)</div>
<div class="kb-diagram-note">최악 (인덱스 없음): O(n²)</div>
<div class="kb-diagram-note">→ 큰 데이터셋: KD-Tree, Ball Tree 사용</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">군집 (정수 라벨): 0, 1, 2, ...</div>
<div class="kb-diagram-note">이상치: -1</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 친구 그룹 찾기 — 한 명(핵심 점)에서 시작, 친구 목록 탐색, 친구의 친구도 탐색... 더 이상 확장 안 되면 하나의 그룹 완성!

---

## Ⅲ. 매개변수 튜닝



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ε (Epsilon)과 minPts 선택:</div>
<div class="kb-diagram-note">ε 결정법 (k-거리 그래프):</div>
<div class="kb-diagram-note">1. 각 점의 k번째 (= minPts-1번째) 이웃 거리 계산</div>
<div class="kb-diagram-note">2. 오름차순 정렬 → 그래프 시각화</div>
<div class="kb-diagram-note">3. 팔꿈치(Elbow) 지점 = 적절한 ε</div>
<div class="kb-diagram-note">팔꿈치 전: 밀도 높은 지역 (군집 내부)</div>
<div class="kb-diagram-note">팔꿈치 후: 급격히 증가 (이상치)</div>
<div class="kb-diagram-note">팔꿈치: 군집 경계</div>
<div class="kb-diagram-note">minPts 선택:</div>
<div class="kb-diagram-note">일반 규칙: minPts ≥ 차원 수 + 1</div>
<div class="kb-diagram-note">2D: minPts = 3~5</div>
<div class="kb-diagram-note">고차원: minPts = 더 크게</div>
<div class="kb-diagram-note">minPts 작으면: 작은 군집도 군집으로 인식</div>
<div class="kb-diagram-note">minPts 크면: 큰 핵심 군집만 인식</div>
<div class="kb-diagram-note">ε 영향:</div>
<div class="kb-diagram-note">ε 너무 작음:</div>
<div class="kb-diagram-note">→ 거의 모든 점 = Noise</div>
<div class="kb-diagram-note">ε 너무 큼:</div>
<div class="kb-diagram-note">→ 모든 점 = 하나의 군집</div>
<div class="kb-diagram-note">예: 지리 데이터</div>
<div class="kb-diagram-note">위도/경도 포인트</div>
<div class="kb-diagram-note">ε = 0.5km, minPts = 5</div>
<div class="kb-diagram-note">상업 지역: 점 밀집 → 군집</div>
<div class="kb-diagram-note">외딴 집: Noise</div>
<div class="kb-diagram-note">k-거리 그래프로 ε = 0.5km 확인</div>
</div>
</div>



> 📢 **섹션 요약 비유**: ε 튜닝은 라디오 주파수 맞추기 — 너무 좁은 주파수(ε 작음) = 잡음만, 너무 넓은 주파수(ε 큼) = 방송 하나에 다 합쳐짐. 팔꿈치 지점 = 선명한 방송!

---

## Ⅳ. HDBSCAN과 발전



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">DBSCAN 한계:</div>
<div class="kb-diagram-note">가변 밀도 군집: 하나의 ε으로 못 잡음</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">군집 A: 매우 촘촘 (밀도 높음)</div>
<div class="kb-diagram-note">군집 B: 느슨함 (밀도 낮음)</div>
<div class="kb-diagram-note">→ A에 맞는 ε: B를 군집으로 못 잡음</div>
<div class="kb-diagram-note">→ B에 맞는 ε: A와 B가 하나의 군집으로 합쳐짐</div>
<div class="kb-diagram-note">HDBSCAN (Hierarchical DBSCAN):</div>
<div class="kb-diagram-note">ε을 여러 값으로 시도</div>
<div class="kb-diagram-note">→ 계층적 군집 트리 생성</div>
<div class="kb-diagram-note">→ 안정적인 군집 자동 선택</div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-note">가변 밀도 처리</div>
<div class="kb-diagram-note">k만 조정 (ε 불필요)</div>
<div class="kb-diagram-note">더 강건한 군집</div>
<div class="kb-diagram-note">단점:</div>
<div class="kb-diagram-note">DBSCAN보다 느림</div>
<div class="kb-diagram-note">OPTICS (Ordering Points To Identify Clustering Structure):</div>
<div class="kb-diagram-note">도달 가능 거리(Reachability Distance) 기반</div>
<div class="kb-diagram-note">DBSCAN 일반화</div>
<div class="kb-diagram-note">밀도 변화 시각화</div>
<div class="kb-diagram-note">비교:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">알고리즘</div><div class="kb-diagram-cell">k 필요</div><div class="kb-diagram-cell">이상치</div><div class="kb-diagram-cell">형태</div><div class="kb-diagram-cell">속도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">k-means</div><div class="kb-diagram-cell">O</div><div class="kb-diagram-cell">X</div><div class="kb-diagram-cell">구형만</div><div class="kb-diagram-cell">빠름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DBSCAN</div><div class="kb-diagram-cell">X</div><div class="kb-diagram-cell">O</div><div class="kb-diagram-cell">임의</div><div class="kb-diagram-cell">보통</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HDBSCAN</div><div class="kb-diagram-cell">X</div><div class="kb-diagram-cell">O</div><div class="kb-diagram-cell">임의</div><div class="kb-diagram-cell">느림</div></div>
<div class="kb-diagram-note">실무 선택:</div>
<div class="kb-diagram-note">이상치 탐지 중요 + 임의 형태: DBSCAN</div>
<div class="kb-diagram-note">가변 밀도: HDBSCAN</div>
<div class="kb-diagram-note">간단한 원형 군집: k-means</div>
</div>
</div>



> 📢 **섹션 요약 비유**: HDBSCAN은 DBSCAN의 진화 — DBSCAN이 하나의 렌즈로 보는 현미경, HDBSCAN은 배율을 자동으로 바꾸는 현미경. 촘촘하든 느슨하든 모두 잡아요!

---

## Ⅴ. 실무 시나리오 — 이상 거래 탐지



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">금융 거래 이상치 탐지 (DBSCAN 활용):</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">신용카드 거래 이상치 탐지</div>
<div class="kb-diagram-note">하루 100만 건 거래</div>
<div class="kb-diagram-note">이상 거래 패턴 자동 식별</div>
<div class="kb-diagram-note">데이터 특징:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">features:</div><div class="kb-diagram-node">금액, 시간대, 상점카테고리, 위치, 빈도</div></div>
<div class="kb-diagram-note">정상 거래: 일상적 패턴 → 밀집 군집</div>
<div class="kb-diagram-note">이상 거래: 패턴 이탈 → Noise</div>
<div class="kb-diagram-note">구현:</div>
<div class="kb-diagram-note">import sklearn</div>
<div class="kb-diagram-note">from sklearn.cluster import DBSCAN</div>
<div class="kb-diagram-note">from sklearn.preprocessing import StandardScaler</div>
<div class="kb-diagram-note"># 정규화 (단위 통일)</div>
<div class="kb-diagram-note">scaler = StandardScaler()</div>
<div class="kb-diagram-note">X_scaled = scaler.fit_transform(transactions)</div>
<div class="kb-diagram-note"># DBSCAN 적용</div>
<div class="kb-diagram-note">db = DBSCAN(eps=0.5, min_samples=10)</div>
<div class="kb-diagram-note">labels = db.fit_predict(X_scaled)</div>
<div class="kb-diagram-note"># Noise = 이상 거래</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">anomalies = transactions</div><div class="kb-diagram-node">labels == -1</div></div>
<div class="kb-diagram-note"># 결과: 약 2% 이상 거래 탐지</div>
<div class="kb-diagram-note">성능:</div>
<div class="kb-diagram-note">정밀도(Precision): 87% (이상 탐지의 87%가 실제 이상)</div>
<div class="kb-diagram-note">재현율(Recall): 73% (실제 이상의 73% 탐지)</div>
<div class="kb-diagram-note">k-means 대비:</div>
<div class="kb-diagram-note">이상치 탐지 정밀도 20%p 향상</div>
<div class="kb-diagram-note">(k-means는 Noise 개념 없어 이상치 군집에 포함)</div>
<div class="kb-diagram-note">한계 및 보완:</div>
<div class="kb-diagram-note">고차원: t-SNE 차원 축소 후 DBSCAN</div>
<div class="kb-diagram-note">실시간: Micro-cluster DBSCAN (스트리밍)</div>
<div class="kb-diagram-note">레이블 없음: 정기 전문가 검토로 정밀도 보정</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) 이상 거래 탐지는 군중 속 낯선 사람 — 밀집한 군중(정상 거래 군집)에서 혼자 떨어진 사람(Noise=이상 거래)을 자동 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/). k-means보다 20% 정확!

---

## 📌 관련 개념 맵

```
DBSCAN
+-- 점 유형
|   +-- Core Point (핵심)
|   +-- Border Point (경계)
|   +-- Noise Point (이상치)
+-- 매개변수
|   +-- ε (이웃 반경)
|   +-- minPts (최소 이웃 수)
+-- 발전
|   +-- HDBSCAN (가변 밀도)
|   +-- OPTICS
+-- 활용
    +-- 지리 군집
    +-- 이상치 탐지
    +-- 이미지 세그멘테이션
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[k-means 한계 인식 (1990s)]
원형 군집만, 이상치 취약
      |
      v
[DBSCAN 제안 (1996)]
Ester et al., KDD 1996
밀도 기반 혁신
      |
      v
[OPTICS (1999)]
밀도 순서화 확장
      |
      v
[HDBSCAN (2013)]
가변 밀도 해결
계층적 군집
      |
      v
[현재: 이상치 탐지 표준]
사기 탐지, 네트워크 침입 탐지
스트리밍 버전 (DenStream)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. DBSCAN은 별자리 찾기 — 별이 많이 모여 있는 곳(밀도 높은 군집), 홀로 떨어진 별(Noise=[이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))을 자동으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해요!
2. ε은 손 뻗는 거리 — "이 거리 안에 친구가 많으면(minPts) 핵심 점". ε 너무 좁으면 친구 0명, 너무 넓으면 모두 친구!
3. HDBSCAN은 자동 배율 현미경 — DBSCAN은 배율 고정, HDBSCAN은 촘촘한 군집/느슨한 군집 모두 자동으로 적합한 배율로 찾아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 46 / 420

← **이전**: [045. K-평균 군집화 — K-Means Clustering](/knowledge-base/studynote/10_ai/01_ai_basics/045_kmeans/)
**다음**: [047. 계층적 군집화 — Hierarchical Clustering](/knowledge-base/studynote/10_ai/01_ai_basics/047_hierarchical_clustering/) →

---
