---
title: "164. 컨셉 드리프트 (Concept Drift) - 정답 맵핑 규칙 변화"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨셉 드리프트 ([Concept](/studynote/14_data_engineering/02_math_mining/120_concept/) Drift)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 X와 정답 레이블 Y의 조건부 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) P(Y|X)가 변화하는 현상으로, [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)보다 감지가 어렵고 모델에 더 치명적인 영향을 미친다.
> 2. **가치**: ADWIN, DDM 등 온라인 학습 기반 드리프트 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 P(Y|X) [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화를 조기 포착하고, 윈도우 기반 재학습이나 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 적응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 변화에 민첩하게 대응할 수 있다.
> 3. **판단 포인트**: COVID-19 같은 외부 충격은 갑작스러운(Sudden) 컨셉 드리프트를 유발하므로, 정기적 재학습만으로는 대응이 늦을 수 있어 이상 감지 + 즉시 재학습 파이프라인의 조합이 필수다.

---

## Ⅰ. 개요 및 필요성

### 1.1 컨셉 드리프트란?

<strong>컨셉 드리프트 (<a href="/studynote/14_data_engineering/02_math_mining/120_concept/">Concept</a> Drift)</strong>는 ML 모델이 학습할 때 전제한 입력 X와 출력 Y 사이의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 즉 [조건부 확률](/studynote/08_algorithm_stats/08_stats/132_conditional_probability/) P(Y|X)가 시간이 지나면서 변화하는 현상이다.

```
학습 시점                      운영 시점 (컨셉 드리프트 후)
+-----------------------+     +------------------------------+
|  X = [신용점수 높음]   |     |  X = [신용점수 높음]          |
|  Y = [대출 상환 ✓]    |     |  Y = [대출 상환 ✗]           |
|                       |  ->  |                              |
|  P(Y=상환|X=고신용)   |     |  P(Y=상환|X=고신용)           |
|         = 0.95        |     |         = 0.70               |
|                       |     |  (경기 침체로 규칙 붕괴)      |
+-----------------------+     +------------------------------+

입력 데이터(신용점수)는 동일해도 정답(상환 여부)의 규칙이 변함!
```

### 1.2 [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)와의 핵심 차이

| 구분 | [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) | 컨셉 드리프트 |
|:---|:---|:---|
| **변화 대상** | 입력 X의 분포 P(X) | 조건부 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) P(Y\|X) |
| **레이블 필요** | 불필요 (입력만으로 감지) | 필요 (실제 결과 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필요) |
| **감지 난이도** | 상대적으로 쉬움 | 어려움 (레이블 수집 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) |
| **심각도** | 중간 | 높음 (모델 근본 가정 붕괴) |
| **사례** | 고객 나이 분포 변화 | 같은 나이여도 구매 패턴 변화 |

📢 **섹션 요약 비유**: 컨셉 드리프트는 게임의 룰이 바뀌는 것과 같다. [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)가 "새로운 종류의 카드가 생겼다"면, 컨셉 드리프트는 "카드 공격력 계산 방법 자체가 바뀌었다". 기존 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(모델)이 전혀 통하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 컨셉 드리프트의 4가지 유형

| 유형 | 설명 | [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 패턴 | 사례 | 대응 |
|:---|:---|:---|:---|:---|
| **Sudden Drift** | 갑작스러운 분포 변화 | 계단형 급변 | COVID-19 봉쇄, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 급변 | 즉시 재학습 |
| **Gradual Drift** | 점진적 변화 (구 개념 소멸) | 완만한 전환 | 사용자 행동 서서히 변화 | 윈도우 재학습 |
| **Incremental Drift** | 작은 변화가 누적 | 경사 상승 | 인플레이션으로 가격 패턴 변화 | 증분 학습 |
| **Recurring Drift** | 주기적으로 반복 | 주기적 파형 | 계절성 패턴 (여름/겨울) | 계절별 모델 |

```
드리프트 유형별 시각적 패턴

성능
  ^
  |▓▓▓▓▓         ░░░░░░   Sudden:   ▓->░ 급격히 변화
  |▓▓▓▓▓▓▓░░░░░░░         Gradual:  ▓ 서서히 ░로 전환
  |▓▓▓▓▓▒▒▒░░░░░           Incremental: 단계적 악화
  |▓▓░░▓▓░░▓▓░░            Recurring:   주기적 반복
  +----------------------> 시간

  ▓ = 이전 개념 지배  ░ = 새 개념 지배  ▒ = 전환 구간
```

### 2.2 컨셉 드리프트 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

#### DDM (Drift [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) Method)

```
DDM 알고리즘 원리:
  - 오류율 p_i와 표준편차 s_i를 추적
  - 경고 수준: p_i + s_i ≥ p_min + 2 × s_min
  - 드리프트 수준: p_i + s_i ≥ p_min + 3 × s_min

+------------------------------------------------------+
|  오류율                                               |
|   ^                                                  |
|   |         +----------+  드리프트 수준 (3σ)         |
|   |    +----+           +--  경고 수준 (2σ)          |
|   |----+                     정상 수준                |
|   +---------------------------------> 시간            |
|                    ^재학습 트리거                     |
+------------------------------------------------------+
```

#### ADWIN (ADaptive WINdowing)

```
ADWIN 원리:
  - 가변 크기 슬라이딩 윈도우 유지
  - 윈도우 내 두 서브윈도우의 평균 비교
  - 차이가 임계값 초과 시 오래된 데이터 제거 = 드리프트 감지

[데이터 스트림]: d1, d2, d3, ... dt
                 +------------------------------+
                 +--------+  vs  +--------------+
                 서브윈도우1    서브윈도우2
                 (과거 평균)    (최근 평균)
                      차이가 크면 = 드리프트!
```

#### Page-Hinkley Test

```
Page-Hinkley 통계량:
  PHt = Σ(xt - x̄t - δ)

  δ: 허용 가능한 평균 변화량 (민감도 파라미터)
  λ: 드리프트 감지 임계값

  |PHt| > λ -> 드리프트 감지

  특징: 단방향/양방향 변화 감지 가능
        시계열 데이터에 특히 효과적
```

### 2.3 드리프트 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 유형 | 속도 | 메모리 | 적합 상황 |
|:---|:---|:---:|:---:|:---|
| **DDM** | [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 오류 기반 | 빠름 | 낮음 | [지도 학습](/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/), 온라인 |
| **ADWIN** | 평균 변화 기반 | 중간 | 중간 | 비모수적, 범용 |
| **Page-Hinkley** | 누적합 기반 | 빠름 | 매우 낮음 | 시계열, 스트리밍 |
| **CUSUM** | 누적합 기반 | 빠름 | 낮음 | 공정 모니터링 |
| **EDDM** | 개선 DDM | 중간 | 낮음 | Gradual Drift |

### 2.4 컨셉 드리프트 감지 아키텍처

```
+--------------------------------------------------------------+
|                컨셉 드리프트 감지 파이프라인                  |
+--------------------------------------------------------------+
|  실시간 서빙 스트림                                           |
|  [요청 X, 예측 Ŷ] ---> 스트림 처리기 (Flink/Spark)           |
|                                                              |
|  레이블 수집 (지연 가능)                                      |
|  [실제 결과 Y] ---> 레이블 조인 ---> 드리프트 감지 엔진        |
|                    (조인 타임아웃: 1~7일)                     |
|                                                              |
|  드리프트 감지 엔진:                                          |
|  DDM / ADWIN / Page-Hinkley 중 선택                         |
|         v                                                    |
|  드리프트 감지됨?                                             |
|  Yes -> CT 파이프라인 트리거 -> 알람                           |
|  No  -> 모니터링 계속                                         |
+--------------------------------------------------------------+
```

📢 **섹션 요약 비유**: 컨셉 드리프트 감지는 요리 대회 심사 기준이 바뀌는 것을 감지하는 것과 같다. 맛(입력 X)이 아무리 좋아도 심사 기준(P(Y|X))이 바뀌면 점수(Y)가 달라진다. ADWIN은 최근 심사 결과 패턴이 과거와 달라지면 즉시 경보를 울린다.

---

## Ⅲ. 비교 및 연결

### 3.1 COVID-19 컨셉 드리프트 실제 사례

| 모델 | 드리프트 전 | 드리프트 후 | 유형 |
|:---|:---|:---|:---|
| **항공 수요 예측** | 계절+노선 기반 예측 정확 | 봉쇄로 수요 -> 0 | Sudden |
| **신용 위험 모델** | 고소득 = 낮은 위험 | 실직으로 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 붕괴 | Sudden |
| **재고 관리** | 정상 소비 패턴 | 사재기로 패턴 완전 변화 | Sudden |
| **광고 클릭** | 특정 키워드 클릭률 | 재택근무 키워드 급상승 | Sudden + Gradual |

<strong>COVID-19 대응 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>:
```
봉쇄 선언 (Day 0)
     |
     v
Sudden Drift 감지 (DDM 경보)
     |
     v
즉시 재학습 트리거 (CT 파이프라인)
     |
     +--> 봉쇄 이전 데이터 가중치 = 0 (또는 매우 낮음)
     +--> 봉쇄 이후 데이터만으로 재학습
     +--> 불확실성 높음: 앙상블 + 넓은 신뢰구간 사용
```

### 3.2 Recurring Drift 대응: 멀티 모델 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
계절별 컨셉 드리프트 (전자상거래 구매 패턴)

+------------------------------------------------------+
|  1월   2월   3월  ... 11월  12월  1월   2월  ...     |
|  |설날 |     |    ... |     |크리 |설날 |    ...     |
|  |패턴 |     |    ... |     |스마 |패턴 |    ...     |
|                                                      |
|  전략: 월별/분기별 전용 모델 유지                     |
|  +----------------------------------+               |
|  | 모델 스위치:                      |               |
|  |  11월-> 크리스마스 모델 활성화     |               |
|  |  1월 -> 설날 모델 활성화           |               |
|  |  평시 -> 일반 모델 유지            |               |
|  +----------------------------------+               |
+------------------------------------------------------+
```

### 3.3 [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 기반 적응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| **DWM (Dynamic Weighted Majority)** | 정확도에 따라 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 동적 조정 | 안정적 전환 | 오래된 모델 메모리 점유 |
| <strong>AWE (Accuracy Weighted <a href="/studynote/10_ai/03_llm_nlp/257_ensemble_learning/">Ensemble</a>)</strong> | 청크별 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 계산 | 각 개념 전문화 | 청크 크기 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 민감 |
| <strong>Streaming <a href="/studynote/10_ai/03_llm_nlp/257_ensemble_learning/">Ensemble</a></strong> | 최근 N개 모델만 유지 | 메모리 효율 | 최신 모델만 유효 |

📢 **섹션 요약 비유**: COVID-19 같은 Sudden Drift는 갑작스러운 지진과 같다. 평소엔 건물 내진 설계(일반 모델)로 충분하지만, 지진(외부 충격) 후엔 즉시 긴급 점검(드리프트 감지)하고 피해 상황(새 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 맞게 재건(재학습)해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 레이블 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 문제와 해결 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

컨셉 드리프트 감지의 가장 큰 난점은 <strong>실제 레이블(Y)이 즉시 수집되지 않는다</strong>는 것이다.

```
레이블 지연 유형별 대응:

+----------------+--------------------------------------------+
|  지연 유형     |  대응 전략                                  |
+----------------+--------------------------------------------+
|  짧은 지연     |  추가 감독 신호 (클릭, 구매) 활용           |
|  (수분~수시간) |  -> 빠른 컨셉 드리프트 감지 가능             |
+----------------+--------------------------------------------+
|  중간 지연     |  예측 결과 분포 변화로 간접 감지             |
|  (수일)        |  -> Prediction Drift 모니터링                |
+----------------+--------------------------------------------+
|  긴 지연       |  적극적 레이블링 (Active Learning)          |
|  (수주~수개월) |  -> 의심 샘플 우선 레이블링                  |
|  (예: 대출 상환|  -> 간접 지표(연체율 등)로 조기 감지         |
|   12개월)      |                                             |
+----------------+--------------------------------------------+
```

### 4.2 기술사 시험 핵심 포인트

<strong>Q. 컨셉 드리프트의 4가지 유형과 각각의 대응 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a>을 설명하시오.</strong>

- **Sudden**: [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변화, 팬데믹 등 -> 즉시 재학습, 오래된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/)
- **Gradual**: 사용자 취향의 서서히 변화 -> 슬라이딩 윈도우 재학습
- **Incremental**: 물가 상승 등 누적 변화 -> 증분 학습 + 드리프트 임계값 낮춤
- **Recurring**: 계절성 패턴 -> 계절별 전용 모델 또는 계절 [피처](/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 추가

**Q. COVID-19로 인한 컨셉 드리프트 사례와 대응 방안을 설명하시오.**

COVID-19는 전례 없는 Sudden Drift를 유발했다. 항공·숙박·소매 등 수요 예측 모델은 봉쇄 선언 즉시 모든 예측이 무효화됐다. 대응 방안: ① DDM/ADWIN으로 즉시 드리프트 감지, ② 봉쇄 이전 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 학습에서 제거 또는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 0으로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/), ③ 봉쇄 이후 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로만 재학습 ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부족 시 [Transfer Learning](/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/) 활용), ④ 불확실성이 높은 상황에서 신뢰구간 넓은 예측 모델 사용

### 4.3 컨셉 드리프트 대응 프레임워크

```
+--------------------------------------------------------------+
|             컨셉 드리프트 대응 의사결정 트리                   |
+--------------------------------------------------------------+
|  드리프트 감지됨                                              |
|       |                                                      |
|       v                                                      |
|  Sudden vs Gradual?                                          |
|  +- Sudden -> 즉시 재학습 (최근 데이터만)                     |
|  |          + 이전 모델 롤백 준비                             |
|  +- Gradual/Incremental                                      |
|            |                                                 |
|            v                                                 |
|       레이블 충분?                                           |
|       +- Yes -> 슬라이딩 윈도우 재학습                        |
|       +- No  -> Active Learning + 간접 지표 활용              |
|                                                              |
|  Recurring?                                                  |
|  -> 계절 피처 추가 + 멀티 모델 전략                           |
+--------------------------------------------------------------+
```

📢 **섹션 요약 비유**: 컨셉 드리프트 대응은 내비게이션 지도 업데이트와 같다. 갑자기 도로가 바뀌면(Sudden) 즉시 업데이트하고, 서서히 신도시가 생기면(Gradual) 주기적으로 업데이트하며, 매년 공사 구간이 바뀌면(Recurring) 계절마다 다른 지도를 준비한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 컨셉 드리프트 대응 효과

| 항목 | 미대응 | 대응 | 개선 |
|:---|:---|:---|:---|
| <strong>모델 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 유지</strong> | 드리프트 후 급락 | 자동 감지 + [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락폭 60% 감소 |
| **비즈니스 손실** | 수주간 잘못된 예측 | 수시간 내 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/) 개선 |
| **레이블 효율** | 전체 재레이블링 | 의심 샘플만 레이블링 | 레이블링 비용 70% 절감 |
| **감지 속도** | 고객 불만 후 인지 | DDM/ADWIN 조기 감지 | 1~4주 조기 대응 |

### 5.2 결론

컨셉 드리프트는 ML 모델이 직면하는 가장 근본적인 위협이다. [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)와 달리 레이블 없이는 감지하기 어렵고, 외부 충격(COVID-19, 금리 변화)에 의해 Sudden하게 발생할 수 있다. DDM, ADWIN 등 온라인 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 윈도우 기반 재학습, [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 적응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 조합이 효과적 대응 체계를 구성한다.

📢 **섹션 요약 비유**: 컨셉 드리프트는 체스 룰이 바뀌는 것과 같다. 기존 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(모델)이 아무리 강해도 룰이 바뀌면 새로운 게임을 처음부터 배워야 한다. ADWIN은 게임 도중 룰이 바뀌는 순간을 감지하는 심판이고, [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 파이프라인은 즉시 새 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 훈련시키는 코치다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 유사 개념 | [데이터 드리프트](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) | 입력 X 분포 변화 (컨셉 드리프트보다 감지 쉬움) |
| 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | DDM (Drift [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) Method) | 오류율 기반 드리프트 감지 |
| 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | ADWIN | 가변 윈도우 기반 분포 변화 감지 |
| 감지 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | Page-Hinkley Test | 누적합 기반 평균 변화 감지 |
| 대응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Continuous Training](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/)) | 감지 후 자동 재학습 |
| 대응 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) 적응 | DWM, AWE 등 동적 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [앙상블](/studynote/10_ai/03_llm_nlp/257_ensemble_learning/) |
| 연관 | [Active Learning](/studynote/10_ai/03_llm_nlp/214_active_learning/) | 레이블 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 문제 해결을 위한 의심 샘플 레이블링 |
| 상위 개념 | [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) | 드리프트 대응은 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 운영의 핵심 |
| 실사례 | COVID-19 Sudden Drift | 전례 없는 갑작스러운 컨셉 드리프트 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 컨셉 드리프트는 게임의 규칙이 바뀌는 것과 같아요. 그 전까지는 "빨간 버튼을 누르면 점수"였는데, 갑자기 "파란 버튼이 점수"로 바뀌면 기존 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 완전히 망가지죠.
2. ADWIN은 축구 경기에서 심판이 갑자기 오프사이드 규칙을 바꾸면 즉시 감지하는 VAR(비디오 판독) 시스템 같아요.
3. 계절마다 다른 옷을 입는 것처럼, 계절별 컨셉 드리프트에 대응하기 위해 여름 모델, 겨울 모델을 따로 준비하는 것이 멀티 모델 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
모델 학습 시점의 관계 P(Y|X)
    | 시간 경과
    v
컨셉 드리프트 발생: P(Y|X) 변화
    |
    v
드리프트 유형 분류
    +-► Sudden: 정책 변화 · 팬데믹
    +-► Gradual: 사용자 취향 서서히 변화
    +-► Incremental: 물가 상승 등 누적
    +-► Recurring: 계절성 주기 반복
    |
    v
감지: DDM · ADWIN · Page-Hinkley (온라인)
    |
    v
대응: CT 재학습 · 윈도우 전략 · 멀티모델 · 앙상블 적응
```

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 164 / 258

<- **이전**: [163. 데이터 드리프트 (Data Drift) - 운영 데이터 통계 분포 이격](/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)
**다음**: [165. 피처 스토어 (Feature Store) - 훈련/서빙 피처 일관성](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ->

---
