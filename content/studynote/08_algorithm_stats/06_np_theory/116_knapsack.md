+++
title = "011. 배낭 문제 — Knapsack Problem"
date = 2026-04-05

[taxonomies]
tags = ["studynote-algorithm-stats"]

[extra]
tags = ["studynote-algorithm-stats"]
+++

> **핵심 인사이트**
> 1. 배낭 문제(Knapsack Problem)는 NP-완전 문제의 대표적 최적화 문제 — 무게 제한이 있는 배낭에 가치 합계를 최대화하는 물건을 고르는 문제로, 0/1 배낭(물건 전체 또는 선택 안 함)과 분수 배낭(일부 가능)으로 나뉜다.
> 2. 0/1 배낭 문제는 DP([동적 프로그래밍](/knowledge-base/studynote/08_algorithm_stats/01_basics/007_dynamic_programming/))로 의사다항 시간(Pseudo-Polynomial) 해결 — O(nW) 시간·공간 복잡도이며, 이는 엄밀히 다항 시간이 아니지만 실용적으로 많은 경우에 효율적이다.
> 3. 분수 배낭(Fractional Knapsack)은 그리디로 최적해 — 단위 무게당 가치(value/[weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))가 높은 순으로 탐욕적으로 선택하면 최적해를 보장하며, O(n log n) 시간에 해결된다.

---

## Ⅰ. 배낭 문제 유형



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">배낭 문제 유형:</div>
<div class="kb-diagram-note">0/1 배낭 (0-1 Knapsack):</div>
<div class="kb-diagram-note">각 물건: 전체 선택(1) 또는 미선택(0)</div>
<div class="kb-diagram-note">→ NP-완전 (다항 시간 알고리즘 미발견)</div>
<div class="kb-diagram-note">→ DP로 의사다항 시간</div>
<div class="kb-diagram-note">분수 배낭 (Fractional Knapsack):</div>
<div class="kb-diagram-note">물건을 일부분만 선택 가능 (액체, 곡물 등)</div>
<div class="kb-diagram-note">→ 그리디로 최적해 O(n log n)</div>
<div class="kb-diagram-note">복수 배낭 (Multiple Knapsack):</div>
<div class="kb-diagram-note">배낭이 여러 개</div>
<div class="kb-diagram-note">→ 더 복잡 (NP-하드)</div>
<div class="kb-diagram-note">경계 배낭 (Bounded Knapsack):</div>
<div class="kb-diagram-note">물건별 최대 수량 제한</div>
<div class="kb-diagram-note">→ DP 확장</div>
<div class="kb-diagram-note">문제 정의 (0/1 배낭):</div>
<div class="kb-diagram-note">물건 n개: 각 가치 v_i, 무게 w_i</div>
<div class="kb-diagram-note">배낭 용량: W</div>
<div class="kb-diagram-note">목적: Σ v_i × x_i 최대화</div>
<div class="kb-diagram-note">조건: Σ w_i × x_i ≤ W</div>
<div class="kb-diagram-note">x_i ∈ {0, 1}</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">물건: (v=60, w=10), (v=100, w=20), (v=120, w=30)</div>
<div class="kb-diagram-note">배낭 용량: W=50</div>
<div class="kb-diagram-note">최적: 물건2 + 물건3 → 가치=220, 무게=50</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 0/1 배낭은 여행 가방 싸기 — 무게 제한(용량)에 가장 소중한 물건(가치)을 선택. 물건은 반만 넣을 수 없어요! 분수 배낭은 주스를 반 병 넣을 수 있는 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/).

---

## Ⅱ. DP 풀이 (0/1 배낭)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">동적 프로그래밍 풀이:</div>
<div class="kb-diagram-note">점화식:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">w</div><div class="kb-diagram-note">= 물건 1..i 중 무게 w 이하에서 최대 가치</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">w</div><div class="kb-diagram-note">= max(</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-node">w</div><div class="kb-diagram-note">, # 물건 i 미선택</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">i-1</div><div class="kb-diagram-node">w-w_i</div><div class="kb-diagram-note">+ v_i # 물건 i 선택 (w ≥ w_i 일 때)</div></div>
<div class="kb-diagram-note">)</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">물건: A(v=60,w=10), B(v=100,w=20), C(v=120,w=30)</div>
<div class="kb-diagram-note">W=50</div>
<div class="kb-diagram-note">dp 테이블 (일부):</div>
<div class="kb-diagram-note">w: 0 10 20 30 40 50</div>
<div class="kb-diagram-note">초기: 0 0 0 0 0 0</div>
<div class="kb-diagram-note">A: 0 60 60 60 60 60</div>
<div class="kb-diagram-note">B: 0 60 100 160 160 160</div>
<div class="kb-diagram-note">C: 0 60 100 160 180 220</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">최적값: dp</div><div class="kb-diagram-node">3</div><div class="kb-diagram-node">50</div><div class="kb-diagram-note">= 220</div></div>
<div class="kb-diagram-note">추적 (어떤 물건?):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">3</div><div class="kb-diagram-node">50</div><div class="kb-diagram-note">=220: C 선택 (220 &gt; dp</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">50</div><div class="kb-diagram-note">=160)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">20</div><div class="kb-diagram-note">=100: B 선택</div></div>
<div class="kb-diagram-note">→ 물건 B, C 선택</div>
<div class="kb-diagram-note">시간/공간 복잡도:</div>
<div class="kb-diagram-note">O(nW) 시간, O(nW) 공간</div>
<div class="kb-diagram-note">n=100, W=10^9 → 실용 불가</div>
<div class="kb-diagram-note">공간 최적화: O(W) (1차원 DP)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">dp</div><div class="kb-diagram-node">w</div><div class="kb-diagram-note">= max(dp</div><div class="kb-diagram-node">w</div><div class="kb-diagram-note">, dp</div><div class="kb-diagram-node">w-w_i</div><div class="kb-diagram-note">+v_i)</div></div>
<div class="kb-diagram-note">(역방향 순회)</div>
<div class="kb-diagram-note">의사다항 시간:</div>
<div class="kb-diagram-note">O(nW): W가 n의 다항식이 아님</div>
<div class="kb-diagram-note">(W는 입력 값이지 크기가 아님)</div>
<div class="kb-diagram-note">입력 비트수 기준: O(n × 2^b) (b=W 비트수)</div>
<div class="kb-diagram-note">→ 다항 시간이 아님!</div>
<div class="kb-diagram-note">하지만 실용적 W에서는 효율적</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 배낭 DP는 표 만들기 — "물건 1~2개, 용량 0~W" 모든 경우를 표에 채우기. 작은 문제 답으로 큰 문제 풀기. 표 크기가 nW이므로 W가 크면 느림!

---

## Ⅲ. 그리디 — 분수 배낭



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">분수 배낭 그리디 풀이:</div>
<div class="kb-diagram-note">핵심 아이디어:</div>
<div class="kb-diagram-note">단위 무게당 가치 = v_i / w_i 로 정렬</div>
<div class="kb-diagram-note">→ 높은 것부터 최대한 채우기</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">물건: A(v=60,w=10), B(v=100,w=20), C(v=120,w=30)</div>
<div class="kb-diagram-note">단위 가치: A=6, B=5, C=4</div>
<div class="kb-diagram-note">W=50:</div>
<div class="kb-diagram-note">A 전체: 무게 10, 가치 60 (남은 W=40)</div>
<div class="kb-diagram-note">B 전체: 무게 20, 가치 100 (남은 W=20)</div>
<div class="kb-diagram-note">C 20/30: 무게 20, 가치 80 (남은 W=0)</div>
<div class="kb-diagram-note">→ 총 가치: 240 (최적!)</div>
<div class="kb-diagram-note">증명:</div>
<div class="kb-diagram-note">그리디 선택 = 전역 최적</div>
<div class="kb-diagram-note">(교환 논증: 다른 선택으로 교환해도 가치 감소)</div>
<div class="kb-diagram-note">시간 복잡도:</div>
<div class="kb-diagram-note">정렬: O(n log n)</div>
<div class="kb-diagram-note">탐욕 선택: O(n)</div>
<div class="kb-diagram-note">→ O(n log n)</div>
<div class="kb-diagram-note">0/1 vs 분수:</div>
<div class="kb-diagram-note">0/1: 동일 예시 → 최적: 220 (B+C)</div>
<div class="kb-diagram-note">분수: 동일 예시 → 최적: 240 (A+B+C부분)</div>
<div class="kb-diagram-note">분수 ≥ 0/1 항상 성립</div>
<div class="kb-diagram-note">(분수는 더 유연한 선택 가능)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 분수 배낭 그리디는 뷔페 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 가격 대비 맛(단위 가치)이 높은 음식부터 먹기. 배(용량)가 꽉 차면 남은 음식 조금만 담기!

---

## Ⅳ. 근사 알고리즘과 FPT



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">0/1 배낭 NP-완전 대응:</div>
<div class="kb-diagram-note">FPTAS (Fully Polynomial-Time Approximation Scheme):</div>
<div class="kb-diagram-note">(1-ε) 최적 근사 보장</div>
<div class="kb-diagram-note">아이디어: 가치를 스케일링해서 DP</div>
<div class="kb-diagram-note">원래 가치: v_i</div>
<div class="kb-diagram-note">스케일 가치: v'_i = floor(v_i × n/ε/v_max)</div>
<div class="kb-diagram-note">복잡도: O(n² / ε)</div>
<div class="kb-diagram-note">ε=0.1 → 90% 근사</div>
<div class="kb-diagram-note">ε=0.01 → 99% 근사</div>
<div class="kb-diagram-note">→ 최적에 가까운 해를 다항 시간에!</div>
<div class="kb-diagram-note">FPT (Fixed-Parameter Tractable):</div>
<div class="kb-diagram-note">파라미터: 물건 수 n 고정</div>
<div class="kb-diagram-note">또는 최적 해의 물건 수 k</div>
<div class="kb-diagram-note">O(2^k × poly(n)) — k가 작으면 실용적</div>
<div class="kb-diagram-note">분기 한정 (Branch &amp; Bound):</div>
<div class="kb-diagram-note">DP보다 실용적 최적해 탐색</div>
<div class="kb-diagram-note">분기: 물건 선택/미선택 분기</div>
<div class="kb-diagram-note">한정: 분수 배낭 상한값으로 가지치기</div>
<div class="kb-diagram-note">→ 최적 경로만 탐색</div>
<div class="kb-diagram-note">실용적 접근:</div>
<div class="kb-diagram-note">n, W 작음: DP (정확)</div>
<div class="kb-diagram-note">n 작음, W 큼: FPT</div>
<div class="kb-diagram-note">근사해 허용: FPTAS</div>
<div class="kb-diagram-note">실용 최적: 분기 한정법</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 배낭 근사는 충분히 좋은 답 — "완벽한 짐(최적해)" 찾기가 너무 오래 걸리면, "90% 좋은 짐(근사해)"로 타협. FPTAS는 얼마나 타협할지 조절!

---

## Ⅴ. 실무 시나리오 — 클라우드 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클라우드 VM 자원 최적 배치 (배낭 변형):</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">가상 서버 100대: 각 CPU 요구량, 비용 효율성</div>
<div class="kb-diagram-note">물리 서버 용량: 128 vCPU</div>
<div class="kb-diagram-note">목표: 비용 효율성 합계 최대화</div>
<div class="kb-diagram-note">= 0/1 배낭 문제 형태</div>
<div class="kb-diagram-note">접근:</div>
<div class="kb-diagram-note">DP: W=128, n=100</div>
<div class="kb-diagram-note">O(100 × 128) = O(12,800) → 실용적!</div>
<div class="kb-diagram-note">빈 패킹 + 배낭의 혼합:</div>
<div class="kb-diagram-note">여러 서버에 VM 분산 배치</div>
<div class="kb-diagram-note">→ 복수 배낭 (NP-하드)</div>
<div class="kb-diagram-note">실용 접근:</div>
<div class="kb-diagram-note">First Fit Decreasing (FFD) 근사:</div>
<div class="kb-diagram-note">CPU 요구량 높은 VM부터 첫 번째 들어가는 서버에 배치</div>
<div class="kb-diagram-note">→ 최적의 약 11/9 × OPT + 6/9 보장</div>
<div class="kb-diagram-note">자원 스케줄링:</div>
<div class="kb-diagram-note">Kubernetes 스케줄러 = 배낭 변형</div>
<div class="kb-diagram-note">Pod 요청 (CPU, 메모리) = 무게</div>
<div class="kb-diagram-note">노드 가용 자원 = 배낭 용량</div>
<div class="kb-diagram-note">Bin Packing + First Fit 전략</div>
<div class="kb-diagram-note">→ 노드 수 최소화 + 자원 효율 최대화</div>
<div class="kb-diagram-note">데이터 선택 문제:</div>
<div class="kb-diagram-note">캐시 크기 제한 + 데이터 접근 빈도/크기</div>
<div class="kb-diagram-note">= 배낭 문제 직접 적용</div>
<div class="kb-diagram-note">LRU는 그리디 근사</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 클라우드 배낭 = [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) — 서버(배낭)에 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)(물건)를 CPU/메모리(무게) 제한 안에서 최대한 효율적으로 배치!

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">배낭 문제 (Knapsack)</div>
<div class="kb-diagram-note">+-- 유형</div>
<div class="kb-diagram-note">+-- 0/1 배낭 (NP-완전) → DP</div>
<div class="kb-diagram-note">+-- 분수 배낭 → 그리디 O(n log n)</div>
<div class="kb-diagram-note">+-- 복수/경계 배낭 → 확장 DP</div>
<div class="kb-diagram-note">+-- 풀이</div>
<div class="kb-diagram-note">+-- DP: O(nW) 의사다항</div>
<div class="kb-diagram-note">+-- 그리디 (분수 배낭만)</div>
<div class="kb-diagram-note">+-- FPTAS: (1-ε) 근사</div>
<div class="kb-diagram-note">+-- 분기 한정</div>
<div class="kb-diagram-note">+-- 응용</div>
<div class="kb-diagram-note">+-- 자원 할당, 캐시 최적화</div>
<div class="kb-diagram-note">+-- 빈 패킹 (클라우드)</div>
<div class="kb-diagram-note">+-- 포트폴리오 최적화</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도

```
[배낭 문제 정의 (1957)]
Dantzig: 분수 배낭 그리디 제안
      |
      v
[DP 풀이 (1950~60s)]
0/1 배낭 DP 체계화
의사다항 시간 알고리즘
      |
      v
[NP-완전 확인 (1975)]
Karp: NP-완전 21개 문제 중 포함
      |
      v
[FPTAS 개발 (1977~)]
이브라히모프 등
다항 시간 근사 체계화
      |
      v
[현재 응용]
클라우드 자원 할당
AI 하이퍼파라미터 탐색
금융 포트폴리오 최적화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 배낭 문제는 여행 가방 싸기 — 무게 제한(배낭 용량) 안에서 가장 소중한 물건들을 고르는 것. 어떤 물건 넣을지가 퀴즈!
2. DP는 모든 경우 표 만들기 — "물건 1개/용량 0~W", "물건 2개/용량 0~W"... 표를 채우면서 최적해를 찾아요.
3. 분수 배낭은 그리디로 OK — 쪼갤 수 있으면 "가성비 좋은 것부터"가 항상 최적! 쪼갤 수 없으면 DP 필요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 116 / 175

← **이전**: [010. TSP NP — 외판원 문제](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/115_tsp_np/)
**다음**: [012. NP 근사 알고리즘 — Approximation Algorithms for NP](/knowledge-base/studynote/08_algorithm_stats/06_np_theory/117_approximation_np/) →

---
