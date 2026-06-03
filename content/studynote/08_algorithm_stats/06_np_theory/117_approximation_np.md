+++
title = "012. NP 근사 알고리즘 — Approximation Algorithms for NP"
date = 2026-04-05

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

> **핵심 인사이트**
> 1. NP-하드 문제의 [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)은 "완벽하지 않지만 보장된 품질"을 빠르게 계산 — ρ-근사(Approximation Ratio) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 최적해의 ρ배 이하(최소화) 또는 이상(최대화)을 다항 시간에 보장하며, 이론적 최적 추구보다 실용적 접근이다.
> 2. 대표 [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)과 보장 — 버텍스 커버: 2-근사, [TSP](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/)(삼각 부등식): 1.5-근사(Christofides), 집합 커버: O(log n)-근사, 배낭: FPTAS(임의 ε 근사), 2-SAT: 다항 시간 정확해.
> 3. 근사 불가능성(Inapproximability)도 중요 — 집합 커버는 O(log n)보다 나은 근사가 P≠NP 가정 하에 불가능하며, Clique는 n^(1-ε) 근사도 불가능(ZPP≠NP). 근사 한계도 이론적으로 정의된다.

---

## Ⅰ. [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/) 기초



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">근사 알고리즘 (Approximation Algorithm):</div>
<div class="kb-diagram-note">목적:</div>
<div class="kb-diagram-note">NP-하드 문제에서 다항 시간 + 품질 보장</div>
<div class="kb-diagram-note">완벽한 최적해 대신 "충분히 좋은 해"</div>
<div class="kb-diagram-note">근사 비율 (Approximation Ratio):</div>
<div class="kb-diagram-note">최소화 문제: ρ = A(I) / OPT(I) ≤ ρ</div>
<div class="kb-diagram-note">최대화 문제: ρ = OPT(I) / A(I) ≤ ρ</div>
<div class="kb-diagram-note">A(I): 알고리즘 출력값</div>
<div class="kb-diagram-note">OPT(I): 최적해 값</div>
<div class="kb-diagram-note">ρ=1: 완벽 최적해 (=정확 알고리즘)</div>
<div class="kb-diagram-note">ρ=2: 최적의 2배 이하 (최소화) → "2-근사"</div>
<div class="kb-diagram-note">ρ=1.5: 최적의 1.5배 → TSP Christofides</div>
<div class="kb-diagram-note">근사 스키마:</div>
<div class="kb-diagram-note">PTAS (Polynomial-Time Approximation Scheme):</div>
<div class="kb-diagram-note">임의 ε &gt; 0에 대해 (1+ε)-근사</div>
<div class="kb-diagram-note">시간: poly(n)이지만 ε에 지수적</div>
<div class="kb-diagram-note">FPTAS (Fully PTAS):</div>
<div class="kb-diagram-note">시간: poly(n, 1/ε)</div>
<div class="kb-diagram-note">배낭 문제 FPTAS가 대표적</div>
<div class="kb-diagram-note">한계 (Inapproximability):</div>
<div class="kb-diagram-note">모든 NP-하드 문제에 좋은 근사 존재 X</div>
<div class="kb-diagram-note">Clique: n^(1-ε) 근사 불가 (ZPP≠NP)</div>
<div class="kb-diagram-note">→ 근사 자체가 NP-하드인 경우</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)은 "충분히 좋은 답" — 완벽한 답(최적해)은 너무 오래 걸리므로, "최적의 1.5배 이내"를 빠르게! 1.5배 이내 보장이 [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)의 가치.

---

## Ⅱ. 버텍스 커버 2-근사



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">버텍스 커버 (Vertex Cover):</div>
<div class="kb-diagram-note">그래프 G=(V,E)에서 모든 에지를 커버하는 최소 정점 집합</div>
<div class="kb-diagram-note">= NP-완전</div>
<div class="kb-diagram-note">2-근사 알고리즘:</div>
<div class="kb-diagram-note">아이디어: 임의 에지 선택 → 양 끝점 추가 → 반복</div>
<div class="kb-diagram-note">알고리즘:</div>
<div class="kb-diagram-note">C = {}</div>
<div class="kb-diagram-note">while E는 비어있지 않음:</div>
<div class="kb-diagram-note">임의 에지 (u,v) 선택</div>
<div class="kb-diagram-note">C = C ∪ {u, v}</div>
<div class="kb-diagram-note">u, v에 인접한 모든 에지 제거</div>
<div class="kb-diagram-note">return C</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">그래프: 1-2, 2-3, 3-4, 4-5</div>
<div class="kb-diagram-note">에지 (1,2) 선택 → {1,2} 추가</div>
<div class="kb-diagram-note">에지 (3,4) 선택 → {3,4} 추가</div>
<div class="kb-diagram-note">에지 5에 연결된 것 → {5} or 에지 (4,5) 커버됨</div>
<div class="kb-diagram-note">→ C = {1,2,3,4}</div>
<div class="kb-diagram-note">최적해: {2,4} (크기 2)</div>
<div class="kb-diagram-note">알고리즘: 크기 4 ≤ 2 × 최적(2) ✓ 2-근사!</div>
<div class="kb-diagram-note">증명:</div>
<div class="kb-diagram-note">선택한 에지들 = 매칭(공유 정점 없음)</div>
<div class="kb-diagram-note">→ 매칭 크기 = k</div>
<div class="kb-diagram-note">→ 알고리즘: 2k 정점</div>
<div class="kb-diagram-note">→ 최적: ≥ k (각 에지 최소 1개 정점 필요)</div>
<div class="kb-diagram-note">→ 2k / k = 2 → 2-근사 증명</div>
<div class="kb-diagram-note">시간 복잡도: O(V+E)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 버텍스 커버 2-근사는 에지 짝 잡기 — 도로(에지) 감시에 필요한 최소 초소(정점). 무작위 도로 선택 후 양 끝 초소 세우면 최적의 2배 이내!

---

## Ⅲ. 집합 커버 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 근사



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">집합 커버 (Set Cover):</div>
<div class="kb-diagram-note">전체 집합 U, 부분집합들 S_1, ..., S_m</div>
<div class="kb-diagram-note">U를 커버하는 최소 부분집합 선택</div>
<div class="kb-diagram-note">= NP-완전</div>
<div class="kb-diagram-note">그리디 알고리즘:</div>
<div class="kb-diagram-note">아이디어: 매 단계 가장 많은 원소를 커버하는 집합 선택</div>
<div class="kb-diagram-note">알고리즘:</div>
<div class="kb-diagram-note">C = {} (선택된 집합)</div>
<div class="kb-diagram-note">R = U (남은 원소)</div>
<div class="kb-diagram-note">while R ≠ {}:</div>
<div class="kb-diagram-note">S_i = R와의 교집합이 최대인 집합</div>
<div class="kb-diagram-note">C = C ∪ {S_i}</div>
<div class="kb-diagram-note">R = R - S_i</div>
<div class="kb-diagram-note">return C</div>
<div class="kb-diagram-note">근사 비율:</div>
<div class="kb-diagram-note">H_n = 1 + 1/2 + 1/3 + ... + 1/n ≈ ln(n)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ O(log</div><div class="kb-diagram-cell">U</div><div class="kb-diagram-cell">) 근사 보장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">예:</div><div class="kb-diagram-cell">U</div><div class="kb-diagram-cell">=100 → 최적 k개, 그리디 ≤ k × ln(100) ≈ 4.6k</div></div>
<div class="kb-diagram-note">불가능 결과:</div>
<div class="kb-diagram-note">(1-ε) × ln(n) 보다 좋은 근사는</div>
<div class="kb-diagram-note">P≠NP 가정 하에 불가능 (Feige 1998)</div>
<div class="kb-diagram-note">→ ln(n) 근사가 사실상 최선</div>
<div class="kb-diagram-note">적용:</div>
<div class="kb-diagram-note">네트워크 감시 (모든 링크 커버)</div>
<div class="kb-diagram-note">유전체 분석 (탐침 선택)</div>
<div class="kb-diagram-note">광고 노출 최적화</div>
<div class="kb-diagram-note">서비스 배치 최적화</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 집합 커버 그리디는 최대 할인 선택 — 매 번 가장 많은 물건(원소)을 커버하는 할인 쿠폰(집합) 선택. log(n)배 이내 최적. 이보다 좋은 전략은 이론상 불가!

---

## Ⅳ. [TSP](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/) 1.5-근사 (Christofides)

```
TSP (여행하는 외판원 문제):
  n개 도시 모두 방문하는 최소 비용 순환 경로
  = NP-하드

Christofides 알고리즘 (1976, 삼각 부등식 가정):
  
  1. MST (최소 신장 트리) 계산
  2. MST에서 홀수 차수 정점 집합 O 추출
  3. O에서 최소 완전 매칭 M 계산
  4. MST + M 합친 오일러 그래프
  5. 오일러 순회 찾기
  6. 단축 (방문했던 도시 건너뛰기)

근사 비율: 1.5

증명 (개략):
  MST 비용 ≤ OPT (최적 경로에서 에지 하나 제거 = 신장 트리)
  최소 완전 매칭 ≤ OPT/2 (삼각 부등식 + 홀수 정점쌍)
  → Christofides: MST + 매칭 ≤ 1.5 × OPT

최근 개선 (2020):
  Karlin-Klein-Gharan: (1.5-ε)-근사 증명
  46년 만의 개선!
  
  하지만 엄청나게 복잡한 알고리즘
  실용성은 낮음

주의:
  삼각 부등식 없는 일반 TSP:
  P≠NP 가정 하에 임의 상수 근사 불가
  
일반 근사:
  2-opt, 3-opt: 로컬 서치 휴리스틱
  LKH (Lin-Kernighan-Helsgott): 실용 최고 품질
```

> 📢 **섹션 요약 비유**: Christofides는 최적 근처 여행 계획 — [MST](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/041_mst/)(최저비용 연결)에 홀수 도시 연결(매칭) 추가. 최적 경로의 1.5배 이내 보장. 46년간 최고 이론 기록!

---

## Ⅴ. 실무 시나리오 — 물류 최적화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">택배 회사 배송 경로 최적화:</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">배송 드라이버 1명, 도시 100개</div>
<div class="kb-diagram-note">하루 모든 배송지 방문 최소 이동 거리</div>
<div class="kb-diagram-note">= TSP 변형</div>
<div class="kb-diagram-note">현실적 접근:</div>
<div class="kb-diagram-note">1. 거리 행렬 준비:</div>
<div class="kb-diagram-note">100 × 100 = 10,000개 거리 (Google Maps API)</div>
<div class="kb-diagram-note">2. Christofides 1.5-근사:</div>
<div class="kb-diagram-note">정확한 최적 보장</div>
<div class="kb-diagram-note">하지만 최소 완전 매칭 계산 복잡</div>
<div class="kb-diagram-note">3. 실용 선택 — LKH (Lin-Kernighan):</div>
<div class="kb-diagram-note">100개 도시: 밀리초~초</div>
<div class="kb-diagram-note">품질: 최적과 0.1~0.5% 차이</div>
<div class="kb-diagram-note">→ 이론 보장은 없지만 실용 최고</div>
<div class="kb-diagram-note">4. 시뮬레이티드 어닐링 (SA):</div>
<div class="kb-diagram-note">랜덤 탐색 + 확률적 수용</div>
<div class="kb-diagram-note">글로벌 최적 탐색</div>
<div class="kb-diagram-note">100개: 수초~수십초</div>
<div class="kb-diagram-note">5. 유전 알고리즘 (GA):</div>
<div class="kb-diagram-note">복수 경로 진화</div>
<div class="kb-diagram-note">병렬화 가능</div>
<div class="kb-diagram-note">결과 비교 (100개 도시):</div>
<div class="kb-diagram-note">무작위 경로: 100% (기준)</div>
<div class="kb-diagram-note">최근접이웃 그리디: ~25% 단축</div>
<div class="kb-diagram-note">2-opt: ~15% 추가 단축</div>
<div class="kb-diagram-note">Christofides: 이론 1.5× OPT 보장</div>
<div class="kb-diagram-note">LKH: 실용 최고 (~0.3% OPT 차이)</div>
<div class="kb-diagram-note">비용 효과:</div>
<div class="kb-diagram-note">배송 경로 최적화 10% 단축</div>
<div class="kb-diagram-note">드라이버 일 평균 이동: 200km → 180km</div>
<div class="kb-diagram-note">연료 비용 10% 절감 = 수천만원/년</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 물류 TSP는 우편배달부 퍼즐 — 100군데 집을 최단 거리로 돌기. Christofides는 이론 보장, LKH는 실용 최선. 1%만 줄여도 수천만원 절감!

---

## 📌 관련 개념 맵

```
NP 근사 알고리즘
+-- 근사 비율 (ρ)
|   +-- 2-근사: 버텍스 커버
|   +-- 1.5-근사: TSP Christofides
|   +-- O(log n): 집합 커버
+-- 근사 스키마
|   +-- PTAS
|   +-- FPTAS (배낭)
+-- 불가능성
|   +-- 집합 커버: ln(n) 이상 개선 불가
|   +-- Clique: 다항 근사 불가
+-- 실용 휴리스틱
    +-- LKH, 2-opt, 3-opt
    +-- 유전 알고리즘, SA
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 근사 연구 (1970s)]
버텍스 커버 2-근사
집합 커버 그리디 ln(n)
Christofides 1.5-근사 TSP
      |
      v
[PCP 정리 (1992)]
근사 불가능성 이론 정립
집합 커버 ln(n) 최선 증명
      |
      v
[FPTAS 성숙 (1990s~)]
배낭 FPTAS 체계화
실용 근사 알고리즘 폭발적 발전
      |
      v
[현재: 딥러닝 + 근사]
Graph Neural Network + TSP
강화학습 기반 경로 최적화
TSP Christofides 1.5→(1.5-ε) (2020)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [근사 알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/012_approximation_algorithm/)은 "충분히 좋은 답" — 완벽한 최단 경로 찾기에 수백 년 걸리면, "최단의 1.5배 이내" 경로를 빠르게 찾아요!
2. 버텍스 커버 2-근사는 도로 감시 — 무작위 도로 선택 후 양 끝에 초소 세우면 최적의 2배 이내. 간단하지만 보장 있어요!
3. 집합 커버는 쿠폰 선택 — 매번 가장 많이 커버하는 쿠폰(집합) 선택. log(n)배 이내 최적, 이보다 좋은 방법은 수학적으로 불가능!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 117 / 175

← **이전**: [011. 배낭 문제 — Knapsack Problem](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/116_knapsack/)
**다음**: [013. ETH — 지수 시간 가설](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/118_eth/) →

---
