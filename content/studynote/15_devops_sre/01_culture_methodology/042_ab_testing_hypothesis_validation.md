+++
title = "042. A/B 테스팅 가설 검증"
date = 2026-04-05

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> 1. A/B 테스팅은 제품 변경사항의 효과를 통계적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 실험 방법론으로, [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)/[SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 관점에서 [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)([Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/))와 결합하면 코드 배포 없이 실험을 제어하고 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 없이 사용자 경험을 개선할 수 있다.
> 2. A/B 테스트의 통계적 유의성(p < 0.05)과 충분한 표본 크기(Statistical [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) 80% 이상)는 신뢰할 수 있는 실험 결론을 위한 필수 조건이며, 이를 무시한 조기 결론(p-hacking, Peeking)은 거짓 양성(False Positive) 결과로 이어져 잘못된 제품 의사결정을 초래한다.
> 3. Multi-armed Bandit(MAB) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 전통 A/B 테스트의 탐색/활용 트레이드오프를 해결하여 실험 중에도 높은 성과 변형에 더 많은 트래픽을 자동 배분하므로, 빠른 반복과 비용 최소화가 중요한 환경에서 우수한 대안이 된다.

---

## Ⅰ. A/B 테스팅 기본 구조

```
A/B 테스팅 구성:

Control Group (A): 기존 버전 (현재 상태)
Variant Group (B): 변경 버전 (새로운 기능/UI)

실험 설계:
  1. 가설 수립:
     "버튼 색상을 파란색 → 초록색으로 변경하면
      클릭률이 10% 이상 증가할 것이다"
  
  2. 성공 지표 정의 (Primary/Secondary Metric):
     Primary: 클릭률 (CTR, Click-Through Rate)
     Secondary: 전환율, 이탈률
  
  3. 트래픽 분배:
     A: 50% | B: 50% (균등 분배)
     무작위 배정 (랜덤화)
     동일 사용자 그룹 고정 (쿠키/해시 기반)
  
  4. 실험 기간 결정:
     최소 1~2주 (비즈니스 주기 1회 이상)
     표본 크기 달성까지 대기
  
  5. 결과 분석:
     통계적 유의성 검정
     실용적 유의성 (Effect Size) 확인
```

> 📢 **섹션 요약 비유**: A/B 테스팅은 셰프의 신메뉴 테스트 — 절반 손님에게는 기존 메뉴(A), 나머지에게는 새 메뉴(B) — 만족도 점수 비교로 출시 결정.

---

## Ⅱ. 통계적 유의성과 표본 크기



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">통계 검정 핵심 개념:</div>
<div class="kb-diagram-note">귀무가설(H₀): A = B (차이 없음)</div>
<div class="kb-diagram-note">대립가설(H₁): A ≠ B (차이 있음)</div>
<div class="kb-diagram-note">p-value:</div>
<div class="kb-diagram-note">귀무가설이 참일 때 관측된 결과가 나올 확률</div>
<div class="kb-diagram-note">p &lt; 0.05 → 5% 유의수준에서 귀무가설 기각</div>
<div class="kb-diagram-note">= "이 차이는 랜덤이 아닌 실제 차이일 가능성 95%"</div>
<div class="kb-diagram-note">통계적 검정력 (Statistical Power = 1-β):</div>
<div class="kb-diagram-note">실제 효과가 있을 때 탐지할 확률</div>
<div class="kb-diagram-note">일반적 목표: 80% 이상</div>
<div class="kb-diagram-note">낮은 검정력 → 실제 효과를 놓칠 위험 (False Negative)</div>
<div class="kb-diagram-note">α (Type I Error): 차이 없는데 있다고 판단 (False Positive)</div>
<div class="kb-diagram-note">β (Type II Error): 차이 있는데 없다고 판단 (False Negative)</div>
<div class="kb-diagram-note">최소 표본 크기 계산:</div>
<div class="kb-diagram-note">n = (Z_α + Z_β)² × 2σ² / δ²</div>
<div class="kb-diagram-note">또는 도구 사용: Evan Miller A/B Calculator</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">기준 전환율: 5%</div>
<div class="kb-diagram-note">목표 최소 탐지 효과: 상대적 20% 증가 (5% → 6%)</div>
<div class="kb-diagram-note">α = 0.05, Power = 80%</div>
<div class="kb-diagram-note">→ 필요 표본: 각 그룹 약 3,700명</div>
<div class="kb-diagram-note">p-hacking / 피킹(Peeking) 위험:</div>
<div class="kb-diagram-note">실험 중간에 반복 확인 → 우연히 p &lt; 0.05 발생 가능</div>
<div class="kb-diagram-note">해결: Sequential Testing (α-spending function)</div>
<div class="kb-diagram-note">또는 실험 기간 사전 확정</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 통계적 유의성은 동전 던지기 공정성 검사 — 100번 던져 60번 앞면이면 "조작 동전" 의심 가능, 하지만 10번 중 6번으론 알 수 없어요.

---

## Ⅲ. [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)와 A/B 통합



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">피처 플래그 (Feature Flag) A/B 통합 구조:</div>
<div class="kb-diagram-note">코드:</div>
<div class="kb-diagram-note">if (featureFlag.isEnabled("new_button_color", userId)) {</div>
<div class="kb-diagram-note">renderGreenButton(); // Variant B</div>
<div class="kb-diagram-note">} else {</div>
<div class="kb-diagram-note">renderBlueButton(); // Control A</div>
<div class="kb-diagram-note">}</div>
<div class="kb-diagram-note">피처 플래그 시스템:</div>
<div class="kb-diagram-note">LaunchDarkly, Optimizely Feature Management</div>
<div class="kb-diagram-note">AWS AppConfig, Firebase Remote Config</div>
<div class="kb-diagram-note">트래픽 배분 방식:</div>
<div class="kb-diagram-note">Hash-based: hash(userId) % 100 &lt; 50 → A</div>
<div class="kb-diagram-note">일관성: 동일 유저는 항상 동일 그룹 배정</div>
<div class="kb-diagram-note">DevOps 통합:</div>
<div class="kb-diagram-note">CD 파이프라인:</div>
<div class="kb-diagram-note">코드 머지 → 배포 → 피처 플래그 OFF</div>
<div class="kb-diagram-note">실험 시작 → 피처 플래그 50% 활성화</div>
<div class="kb-diagram-note">통계적 유의성 달성 → 100% 롤아웃 또는 롤백</div>
<div class="kb-diagram-note">배포 전략 연계:</div>
<div class="kb-diagram-note">Canary 배포: 5% 트래픽 → 성능 모니터링</div>
<div class="kb-diagram-note">A/B 테스트: 50% 트래픽 → 비즈니스 지표 측정</div>
<div class="kb-diagram-note">Blue/Green: 100% 전환 → 다운타임 없는 배포</div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-note">배포와 출시 분리 (Decouple Deployment/Release)</div>
<div class="kb-diagram-note">즉각 롤백 (코드 배포 없이 플래그 OFF)</div>
<div class="kb-diagram-note">세그먼트별 실험 (국가, 디바이스, 사용자 등급)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) A/B는 영화관 불빛 조절 — 영화관 전체를 새로 짓지 않고 조명만 바꾸면서 관객 반응을 테스트할 수 있어요.

---

## Ⅳ. Multi-armed Bandit vs A/B 테스트



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Multi-armed Bandit (MAB) 알고리즘:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">A/B 테스팅의 한계: 실험 기간 동안 나쁜 변형에도 50% 트래픽</div>
<div class="kb-diagram-note">MAB: 실시간으로 좋은 변형에 더 많은 트래픽 자동 배분</div>
<div class="kb-diagram-note">Exploration vs Exploitation:</div>
<div class="kb-diagram-note">Exploration: 덜 시도된 변형 탐색 (정보 수집)</div>
<div class="kb-diagram-note">Exploitation: 현재 최고 성과 변형 활용 (수익 극대화)</div>
<div class="kb-diagram-note">주요 알고리즘:</div>
<div class="kb-diagram-note">ε-Greedy:</div>
<div class="kb-diagram-note">ε 확률로 랜덤 탐색 (예: 10%)</div>
<div class="kb-diagram-note">1-ε 확률로 최고 변형 선택 (예: 90%)</div>
<div class="kb-diagram-note">UCB (Upper Confidence Bound):</div>
<div class="kb-diagram-note">신뢰 구간 상한 기준 선택</div>
<div class="kb-diagram-note">불확실한 변형 우선 탐색</div>
<div class="kb-diagram-note">Thompson Sampling:</div>
<div class="kb-diagram-note">베타 분포로 성과 확률 모델링</div>
<div class="kb-diagram-note">확률적으로 높은 변형 선택</div>
<div class="kb-diagram-note">A/B vs MAB 비교:</div>
<div class="kb-diagram-note">전통 A/B:</div>
<div class="kb-diagram-note">고정 트래픽 분배 (50/50)</div>
<div class="kb-diagram-note">실험 기간 동안 나쁜 변형에도 노출</div>
<div class="kb-diagram-note">강한 통계적 보장</div>
<div class="kb-diagram-note">MAB:</div>
<div class="kb-diagram-note">동적 트래픽 배분 (60:40 → 80:20 → 95:5)</div>
<div class="kb-diagram-note">비용 최소화 (나쁜 변형 노출 감소)</div>
<div class="kb-diagram-note">약한 통계적 보장 (전통 A/B보다)</div>
<div class="kb-diagram-note">적합 시나리오:</div>
<div class="kb-diagram-note">A/B: 장기 지표 검증, 강한 통계 필요</div>
<div class="kb-diagram-note">MAB: 빠른 결정, 가격 최적화, 광고 입찰</div>
</div>
</div>



> 📢 **섹션 요약 비유**: MAB vs A/B는 뷔페 vs 코스 요리 — A/B는 코스(계획대로 순서 있게), MAB는 뷔페(인기 있는 음식 계속 리필).

---

## Ⅴ. 실무 시나리오 — 결제 전환율 실험



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이커머스 결제 페이지 A/B 테스트:</div>
<div class="kb-diagram-note">가설:</div>
<div class="kb-diagram-note">"결제 버튼 문구를 '주문하기' → '지금 구매하기'로 변경하면</div>
<div class="kb-diagram-note">결제 전환율이 15% 이상 증가한다"</div>
<div class="kb-diagram-note">실험 설계:</div>
<div class="kb-diagram-note">Primary Metric: 결제 완료율 (Payment Completion Rate)</div>
<div class="kb-diagram-note">Guard Rail Metric: 페이지 이탈률 (증가하면 안 됨)</div>
<div class="kb-diagram-note">Secondary: AOV (Average Order Value)</div>
<div class="kb-diagram-note">표본 크기 계산:</div>
<div class="kb-diagram-note">현재 결제 전환율: 12%</div>
<div class="kb-diagram-note">최소 탐지 효과: 15% 상대적 증가 (12% → 13.8%)</div>
<div class="kb-diagram-note">α = 0.05, Power = 80%</div>
<div class="kb-diagram-note">→ 각 그룹 약 12,000명 필요</div>
<div class="kb-diagram-note">→ 일일 유니크 방문자 2,000명이면 12일 소요</div>
<div class="kb-diagram-note">실험 진행:</div>
<div class="kb-diagram-note">기간: 14일 (2주, 주간 패턴 2회 포함)</div>
<div class="kb-diagram-note">트래픽: 각 50% (피처 플래그 사용)</div>
<div class="kb-diagram-note">중간 확인 금지 (피킹 방지)</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">A (주문하기): 전환율 12.0%, n=14,200</div>
<div class="kb-diagram-note">B (지금 구매하기): 전환율 13.4%, n=14,350</div>
<div class="kb-diagram-note">p-value: 0.03 (&lt; 0.05, 통계적으로 유의)</div>
<div class="kb-diagram-note">상대적 증가: +11.7% (목표 15% 미달)</div>
<div class="kb-diagram-note">의사결정:</div>
<div class="kb-diagram-note">통계적 유의성: O</div>
<div class="kb-diagram-note">실용적 유의성: △ (11.7% &lt; 15% 목표)</div>
<div class="kb-diagram-note">Guard Rail: 이탈률 변화 없음</div>
<div class="kb-diagram-note">→ 긍정적 결과지만 기대보다 낮음</div>
<div class="kb-diagram-note">→ 100% 롤아웃 결정 (연간 추정 매출 +8억)</div>
<div class="kb-diagram-note">→ 추가 실험 계획 (버튼 색상, 크기 등)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: A/B 테스트 의사결정은 선거 개표 — 유의수준(51% 이상 득표)과 투표 수(표본 크기)가 충분해야 당선 확정(롤아웃).

---

## 📌 관련 개념 맵

```
A/B 테스팅
+-- 통계 기반
|   +-- p-value, α, β
|   +-- Statistical Power
|   +-- 표본 크기 계산
+-- 실험 설계
|   +-- 귀무가설/대립가설
|   +-- Primary/Guard Rail Metric
|   +-- 피킹/p-hacking 방지
+-- 인프라
|   +-- 피처 플래그 (LaunchDarkly)
|   +-- 트래픽 분배 (Hash-based)
+-- 고급 기법
|   +-- Sequential Testing
|   +-- Multi-armed Bandit (MAB)
|   +-- Thompson Sampling
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[통계 실험 기원 (1920s)]
R.A. Fisher: 농업 실험 설계 (무작위 대조 실험)
Student t-test, ANOVA
      |
      v
[웹 A/B 테스팅 태동 (1990s)]
Jakob Nielsen 웹 유용성 연구
Google 41가지 파란색 실험 (2000s)
      |
      v
[A/B 테스팅 플랫폼화 (2010~)]
Optimizely, VWO 서비스 등장
개발자 없이도 실험 가능
      |
      v
[피처 플래그와 통합 (2015~)]
LaunchDarkly, Split.io
배포와 출시 분리 개념 정착
      |
      v
[현재: AI 기반 실험]
베이지안 A/B 테스팅
AutoML 기반 자동 실험 최적화
MAB + DRL (딥 강화학습)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. A/B 테스팅은 두 가지 간판 비교 — 절반 손님에게는 빨간 간판 가게, 나머지에게는 파란 간판 가게를 보여주고 어느 쪽이 더 잘 팔리는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요!
2. p-value는 우연히 이런 결과가 나올 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) — 5% 이하이면 우연이 아니라 진짜 차이라고 믿어요.
3. Multi-armed Bandit은 영리한 슬롯머신 — 어떤 레버가 잘 나오는지 자동으로 학습해서 좋은 레버를 더 자주 당겨줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 42 / 373

← **이전**: [041. TBD 심화: CI/CD 통합 및 코드 리뷰 (Trunk-Based Development Advanced)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/041_trunk_based_development_tbd/)
**다음**: [043. 다크 런칭 & 섀도우 트래픽](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/043_dark_launching_shadow_traffic/) →

---
