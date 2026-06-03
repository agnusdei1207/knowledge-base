+++
title = "048. 이상 탐지 — Anomaly Detection"
date = 2026-04-05

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

> **핵심 인사이트**
> 1. [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)([Anomaly Detection](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/))는 정상 패턴에서 크게 벗어나는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포인트를 찾는 기법 — 레이블된 이상 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 극도로 희소한 현실(보안 위협, 제조 불량, 의료 이상)에서 "정상 분포를 모델링하고 벗어남을 이상으로 판단"하는 방식이 주로 사용된다.
> 2. [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)의 3가지 유형 — 포인트 이상(Point [Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/): 단일 값이 이상), 맥락적 이상(Contextual: 맥락상 이상), 집합적 이상(Collective: 개별은 정상이지만 패턴이 이상)으로 구분되며, 각각 다른 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 필요하다.
> 3. False Positive 비율이 운영 비용을 결정 — [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)는 과탐(False Positive)과 미탐(False Negative) 사이의 트레이드오프이며, 보안 SOC에서 "경보 피로(Alert Fatigue)"가 실제 위협 대응을 방해하는 가장 큰 운영 문제다.

---

## Ⅰ. [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 유형



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이상(Anomaly) 정의:</div>
<div class="kb-diagram-note">정상 데이터의 분포에서 크게 벗어나는 관측값</div>
<div class="kb-diagram-note">3가지 유형:</div>
<div class="kb-diagram-note">1. 포인트 이상 (Point Anomaly):</div>
<div class="kb-diagram-note">단일 데이터 포인트가 비정상</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">신용카드 거래: 평소 3만원 결제</div>
<div class="kb-diagram-note">→ 갑자기 500만원 결제 (이상!)</div>
<div class="kb-diagram-note">체온: 정상 36.5°C</div>
<div class="kb-diagram-note">→ 갑자기 42°C (이상!)</div>
<div class="kb-diagram-note">2. 맥락적 이상 (Contextual Anomaly):</div>
<div class="kb-diagram-note">맥락을 고려할 때 이상 (단독으로는 정상)</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">기온 30°C: 여름에는 정상, 12월에는 이상!</div>
<div class="kb-diagram-note">웹 트래픽 5000RPS: 이벤트 시 정상, 새벽에는 이상!</div>
<div class="kb-diagram-note">3. 집합적 이상 (Collective Anomaly):</div>
<div class="kb-diagram-note">개별 포인트는 정상, 패턴이 이상</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">ECG: 각 심전도 값은 정상 범위</div>
<div class="kb-diagram-note">→ 전체 파형이 비정상 패턴</div>
<div class="kb-diagram-note">네트워크: 단일 패킷은 정상</div>
<div class="kb-diagram-note">→ 수천 개의 작은 패킷이 DDoS 패턴</div>
<div class="kb-diagram-note">이상 탐지 접근법:</div>
<div class="kb-diagram-note">통계 기반: Z-score, IQR, 가우시안</div>
<div class="kb-diagram-note">거리 기반: KNN, LOF (Local Outlier Factor)</div>
<div class="kb-diagram-note">클러스터링: DBSCAN, K-means</div>
<div class="kb-diagram-note">머신러닝: Isolation Forest, One-Class SVM</div>
<div class="kb-diagram-note">딥러닝: Autoencoder, LSTM</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 유형 = 이상한 수학 문제 유형 — 포인트 이상(답이 틀림), 맥락적 이상(문제는 맞는데 이 시험에서 틀림), 집합적 이상(각 문제는 맞는데 순서가 이상)!

---

## Ⅱ. 주요 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">1. 통계 기반:</div>
<div class="kb-diagram-note">Z-Score:</div>
<div class="kb-diagram-note">z = (x - μ) / σ</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">z</div><div class="kb-diagram-cell">&gt; 3 → 이상 (99.7% 벗어남)</div></div>
<div class="kb-diagram-note">가정: 정규 분포</div>
<div class="kb-diagram-note">장점: 단순, 빠름</div>
<div class="kb-diagram-note">단점: 정규 분포 아닌 데이터에 취약</div>
<div class="kb-diagram-note">IQR (Interquartile Range):</div>
<div class="kb-diagram-note">Q1, Q3 계산 → IQR = Q3 - Q1</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">이상치 경계:</div><div class="kb-diagram-node">Q1 - 1.5×IQR, Q3 + 1.5×IQR</div></div>
<div class="kb-diagram-note">비정규 분포에도 robust</div>
<div class="kb-diagram-note">2. 거리 기반:</div>
<div class="kb-diagram-note">LOF (Local Outlier Factor):</div>
<div class="kb-diagram-note">각 점의 지역 밀도를 주변 점들과 비교</div>
<div class="kb-diagram-note">LOF &gt;&gt; 1 → 이상 (주변보다 밀도 낮음)</div>
<div class="kb-diagram-note">장점: 지역적 이상 탐지 (전역 기준 불필요)</div>
<div class="kb-diagram-note">단점: 계산 비용 O(n²)</div>
<div class="kb-diagram-note">3. 앙상블 기반:</div>
<div class="kb-diagram-note">Isolation Forest:</div>
<div class="kb-diagram-note">랜덤 분리로 이상치 빠르게 격리</div>
<div class="kb-diagram-note">원리:</div>
<div class="kb-diagram-note">정상 데이터: 분리하기 어려움 (많은 분리 필요)</div>
<div class="kb-diagram-note">이상 데이터: 분리하기 쉬움 (적은 분리로 격리)</div>
<div class="kb-diagram-note">이상 점수 = 1 / (평균 분리 깊이)</div>
<div class="kb-diagram-note">장점: 빠름(O(n log n)), 고차원에서도 효과적</div>
<div class="kb-diagram-note">단점: 스트리밍 데이터에 약함</div>
<div class="kb-diagram-note">4. 딥러닝:</div>
<div class="kb-diagram-note">Autoencoder:</div>
<div class="kb-diagram-note">인코더 → 잠재 표현 → 디코더</div>
<div class="kb-diagram-note">학습: 정상 데이터로만 재구성 훈련</div>
<div class="kb-diagram-note">이상 감지: 재구성 오류(MSE) 임계값 초과 → 이상</div>
<div class="kb-diagram-note">장점: 복잡한 패턴 학습</div>
<div class="kb-diagram-note">단점: 임계값 설정 어려움</div>
<div class="kb-diagram-note">LSTM Autoencoder:</div>
<div class="kb-diagram-note">시계열 이상 탐지</div>
<div class="kb-diagram-note">정상 패턴 학습 후 미래 예측</div>
<div class="kb-diagram-note">예측 오류 큰 구간 = 이상</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택 — Z-Score(키 차이 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/): 단순), LOF(반 친구들과 키 비교: 지역 기준), [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest(빠른 분리 게임), [Autoencoder](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/335_autoencoder/)(정상 패턴 외운 후 다른 것 감지)!

---

## Ⅲ. 시계열 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">시계열 이상 탐지:</div>
<div class="kb-diagram-note">시간에 따른 데이터 패턴 이상 감지</div>
<div class="kb-diagram-note">IoT, 보안, 인프라 모니터링</div>
<div class="kb-diagram-note">주요 기법:</div>
<div class="kb-diagram-note">1. STL 분해 + 잔차 분석:</div>
<div class="kb-diagram-note">시계열 = 추세 + 계절성 + 잔차</div>
<div class="kb-diagram-note">잔차의 Z-score 높은 구간 = 이상</div>
<div class="kb-diagram-note">도구: Python statsmodels</div>
<div class="kb-diagram-note">2. Prophet (Facebook):</div>
<div class="kb-diagram-note">추세 + 계절성 자동 감지</div>
<div class="kb-diagram-note">공휴일 효과 지원</div>
<div class="kb-diagram-note">이상치 자동 제외 후 재학습</div>
<div class="kb-diagram-note">사용: 트래픽 이상 탐지, 매출 이상</div>
<div class="kb-diagram-note">3. LSTM Autoencoder:</div>
<div class="kb-diagram-note">시퀀스 패턴 학습</div>
<div class="kb-diagram-note">제조 센서 이상 탐지에 강점</div>
<div class="kb-diagram-note">4. 통계적 프로세스 제어 (SPC):</div>
<div class="kb-diagram-note">Control Chart (관리도)</div>
<div class="kb-diagram-note">Shewhart X-bar chart: ±3σ 경계</div>
<div class="kb-diagram-note">CUSUM: 누적 합계 이상 탐지 (드리프트 감지)</div>
<div class="kb-diagram-note">임계값 설정 전략:</div>
<div class="kb-diagram-note">동적 임계값:</div>
<div class="kb-diagram-note">고정 임계값 문제: 계절성 무시</div>
<div class="kb-diagram-note">→ 롤링 평균 ± nσ (동적 경계)</div>
<div class="kb-diagram-note">예: 서버 CPU</div>
<div class="kb-diagram-note">월요일 오전 9시 평균 70% → 임계값 90%</div>
<div class="kb-diagram-note">일요일 새벽 평균 20% → 임계값 40%</div>
<div class="kb-diagram-note">모델 기반 임계값:</div>
<div class="kb-diagram-note">Percentile 기반: 99.9번째 백분위수</div>
<div class="kb-diagram-note">Bayesian 최적화: FPR/FNR 최적 임계값</div>
<div class="kb-diagram-note">실제 시스템:</div>
<div class="kb-diagram-note">AWS CloudWatch Anomaly Detection</div>
<div class="kb-diagram-note">Datadog Anomaly Monitor (Prophet 기반)</div>
<div class="kb-diagram-note">Azure Monitor (ML 기반 기준선)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 시계열 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) = 체온 변화 추적 — 매일 같은 시간 체온 기록(정상 패턴). 갑자기 높아지면(이상). 단, 여름엔 기준값이 달라야(동적 임계값) 함!

---

## Ⅳ. False Positive 관리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이상 탐지의 트레이드오프:</div>
<div class="kb-diagram-note">탐지 경계 낮춤 탐지 경계 높임</div>
<div class="kb-diagram-note">탐지율 높음 (더 많이 탐지) 낮음 (덜 탐지)</div>
<div class="kb-diagram-note">FPR 높음 (과탐 많음) 낮음 (과탐 적음)</div>
<div class="kb-diagram-note">FNR 낮음 (미탐 적음) 높음 (미탐 많음)</div>
<div class="kb-diagram-note">Alert Fatigue (경보 피로):</div>
<div class="kb-diagram-note">SOC 팀 현실:</div>
<div class="kb-diagram-note">일 300~500건 보안 경보 → 실제 위협 5건</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">분석가가 경보를 무시하기 시작</div>
<div class="kb-diagram-note">실제 위협 탐지율 오히려 감소</div>
<div class="kb-diagram-note">FP 감소 전략:</div>
<div class="kb-diagram-note">1. 화이트리스트:</div>
<div class="kb-diagram-note">알려진 정상 패턴/IP/행동 → 탐지 제외</div>
<div class="kb-diagram-note">예: 정기 백업 작업 → 트래픽 이상 제외</div>
<div class="kb-diagram-note">2. 문맥 보강:</div>
<div class="kb-diagram-note">단일 이상 신호 → 다중 신호 상관관계</div>
<div class="kb-diagram-note">"IP 스캔 + 비정상 로그인 + 새 프로세스"</div>
<div class="kb-diagram-note">→ 복합 조건 충족 시 경보</div>
<div class="kb-diagram-note">3. 학습 기반 FP 억제:</div>
<div class="kb-diagram-note">분석가가 "False Positive" 레이블 → 모델 재학습</div>
<div class="kb-diagram-note">점진적 FP 감소</div>
<div class="kb-diagram-note">4. 경보 우선순위화:</div>
<div class="kb-diagram-note">위험도(Risk Score) 계산</div>
<div class="kb-diagram-note">Critical → 즉시 대응</div>
<div class="kb-diagram-note">Low → 주간 배치 검토</div>
<div class="kb-diagram-note">Precision-Recall 트레이드오프:</div>
<div class="kb-diagram-note">보안: 높은 Recall 선호 (미탐 비용 &gt; 과탐 비용)</div>
<div class="kb-diagram-note">제조 품질검사: 높은 Precision 선호 (과탐 비용 &gt; 미탐 비용)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 관리 = 화재 경보기 감도 — 너무 예민하면(낮은 임계값) 밥 태울 때마다 경보. 너무 둔감하면(높은 임계값) 진짜 불 못 잡음. 문맥(연기+온도+불꽃)을 조합해야 정확!

---

## Ⅴ. 실무 시나리오 — 금융 이상 거래 탐지



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">금융 FDS (Fraud Detection System) 구축:</div>
<div class="kb-diagram-note">요구사항:</div>
<div class="kb-diagram-note">초당 거래 10,000건</div>
<div class="kb-diagram-note">이상 거래 비율: 0.1% (하루 약 8,640건)</div>
<div class="kb-diagram-note">최대 허용 FPR: 1% (고객 불편 최소화)</div>
<div class="kb-diagram-note">실시간 탐지 요구: &lt; 50ms</div>
<div class="kb-diagram-note">피처 엔지니어링:</div>
<div class="kb-diagram-note">거래 금액 (현재 vs 평균)</div>
<div class="kb-diagram-note">거래 위치 (현재 vs 일반 위치 거리)</div>
<div class="kb-diagram-note">거래 시간 (야간 여부)</div>
<div class="kb-diagram-note">거래 빈도 (1시간 내 거래 수)</div>
<div class="kb-diagram-note">카드 사용 패턴 (새벽 해외 결제)</div>
<div class="kb-diagram-note">모델 앙상블:</div>
<div class="kb-diagram-note">Isolation Forest: 거래 금액/패턴 이상</div>
<div class="kb-diagram-note">LSTM: 사용자별 시계열 패턴</div>
<div class="kb-diagram-note">Rule-Based: 명시적 규칙 (해외 + 금액 &gt; 100만)</div>
<div class="kb-diagram-note">최종 판단: 가중 투표 (Weight Voting)</div>
<div class="kb-diagram-note">운영 최적화:</div>
<div class="kb-diagram-note">1. 실시간 특성 서빙 (Feature Store):</div>
<div class="kb-diagram-note">Redis: 사용자별 최근 거래 윈도우 캐시</div>
<div class="kb-diagram-note">&lt; 5ms 특성 조회</div>
<div class="kb-diagram-note">2. 모델 서빙:</div>
<div class="kb-diagram-note">ONNX Runtime: 추론 &lt; 20ms</div>
<div class="kb-diagram-note">배치 사이즈 32로 초당 16,000 거래 처리</div>
<div class="kb-diagram-note">3. 임계값 최적화:</div>
<div class="kb-diagram-note">1년치 거래 데이터로 ROC 커브 분석</div>
<div class="kb-diagram-note">FPR 1% @ Recall 72% 지점 선택</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">탐지율: 72% (이상 거래 8,640건 중 6,221건 탐지)</div>
<div class="kb-diagram-note">FPR: 0.8% (허용 1% 이내)</div>
<div class="kb-diagram-note">고객 경험:</div>
<div class="kb-diagram-note">정상 거래 차단: 0.8% → 월 약 20,000건 문의</div>
<div class="kb-diagram-note">자동 재인증(OTP)으로 50%는 즉시 해결</div>
<div class="kb-diagram-note">ROI:</div>
<div class="kb-diagram-note">탐지 사기 = 월 평균 손실 예방 12억원</div>
<div class="kb-diagram-note">시스템 운영 비용 2억원 → 순 ROI 6배</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 금융 [FDS](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/267_gnn_fraud_detection_knowledge_graph/) = 카드 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) — [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest+[LSTM](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/292_lstm/)+규칙 [앙상블](/knowledge-base/studynote/10_ai/03_llm_nlp/257_ensemble_learning/)로 72% 탐지. FPR 0.8%로 고객 불편 최소화. 월 12억 사기 예방, 운영 2억 → [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/) 6배!

---

## 📌 관련 개념 맵

```
이상 탐지 (Anomaly Detection)
+-- 유형
|   +-- 포인트 이상
|   +-- 맥락적 이상
|   +-- 집합적 이상
+-- 알고리즘
|   +-- Z-Score, IQR (통계)
|   +-- LOF (거리)
|   +-- Isolation Forest (앙상블)
|   +-- Autoencoder, LSTM (딥러닝)
+-- 과제
|   +-- False Positive 관리
|   +-- 임계값 설정
|   +-- Alert Fatigue
+-- 응용
    +-- 금융 FDS, 보안 SOC
    +-- 제조 품질, IoT
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[통계 기반 이상 탐지 (1960s~)]
Z-Score, Control Chart
제조 품질 관리
      |
      v
[LOF, DBSCAN (2000s)]
밀도 기반 이상 탐지
거리 개념 도입
      |
      v
[Isolation Forest (2008)]
앙상블 기반 효율화
고차원 데이터 처리
      |
      v
[딥러닝 Autoencoder (2013~)]
복잡한 패턴 학습
시계열 이상 탐지
      |
      v
[현재: LLM 기반 이상 탐지]
로그 이상 탐지
자연어로 이상 설명
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 유형 = 이상한 것 찾기 — 혼자 이상한 것(포인트), 상황에 따라 이상한 것(맥락적), 각각은 정상인데 모이면 이상한 것(집합적)!
2. [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) Forest = 이상한 사람 빠르게 골라내기 — 정상 사람은 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하기 어렵고(많은 질문), 이상한 사람은 금방 골라냄(적은 질문)!
3. Alert Fatigue = 소년의 외침 — "늑대다!" 너무 자주 외치면([FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) 많음) 진짜 늑대(실제 위협)가 와도 무시. 정확한 탐지가 생명!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 48 / 420

← **이전**: [047. 계층적 군집화 — Hierarchical Clustering](/knowledge-base/studynote/10_ai/01_ai_basics/047_hierarchical_clustering/)
**다음**: [049. 앙상블 학습 — Ensemble Learning](/knowledge-base/studynote/10_ai/01_ai_basics/049_ensemble_learning_bagging_boosting/) →

---
