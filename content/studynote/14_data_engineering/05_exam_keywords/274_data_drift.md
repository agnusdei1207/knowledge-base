---
title: "Data Drift Monitoring Distribution Shift Detection"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 드리프트는 **공변량 변화(Covariate Shift, P(X))**, **개념 변화(Concept Drift, P(Y|X))**, **사전확률 변화(Prior Probability Shift, P(Y))**로 분류되며, **PSI(0.1/0.2/0.25 임계값)**, **KS 검정(p<0.05)**, **Wasserstein 거리**, **MMD(다변량 커널 기반)** 등 통계적 거리 척도로 정량화하여 기준 분포(Reference Distribution)와 운영 분포(Production Distribution) 간의 발산을 탐지하는 MLOps 핵심 기법
> 2. **가치**: 모델 성능 열화(Model Decay)를 **사전 2~6주 전 조기 탐지**하여 비즈니스 KPI 손실을 15~35% 감소시키며, **MTTR(Mean Time To Recovery)을 72시간->4시간으로 단축**, 불필요한 재학습 비용 약 40% 절감(Netflix/Airbnb 사례 기준)
> 3. **판단 포인트**: ① **단변량(Univariate) vs 다변량(Multivariate) 검정 선택**, ② **Reference Window 크기(전체 학습 데이터 vs 최근 N일)**, ③ **임계값 민감도(Recall vs 알람 피로도)**, ④ **고차원 희소 벡터(임베딩) 처리를 위한 차원 축소 사전 적용 여부**가 핵심 트레이드오프

---

## Ⅰ. 개요 및 필요성

운영 환경(Production)에 배포된 머신러닝 모델은 **시간에 따라 입력 데이터의 통계적 분포가 학습 시점과 상이**해지면서 점진적 또는 급진적으로 성능이 저하된다. 이를 **Model Decay** 또는 **Performance Degradation**이라 하며, 원인으로는 ① 사용자 행동 패턴 변화(COVID-19 이후 전자상거래 구매 패턴), ② 센서/디바이스 교체(제조업 IoT), ③ 계절성·트렌드 변동, ④ 적대적 데이터 변조, ⑤ 외부 환경 요인(환율·금리·규제) 등이 있다.

2017년 Google의 **"Hidden Technical Debt in ML Systems"**(Sculley 외) 논문에서 강조한 것처럼, ML 시스템의 유지보수 비용은 코드 자체보다 **데이터 의존성**, **피처 파이프라인 변동**, **분포 변화 대응**에서 기인한다. 단순 Accuracy 모니터링만으로는 사후 대응에 그치므로, **분포 변화 자체를 1차 지표로 활용**하는 데이터 드리프트 모니터링이 필수 MLOps 구성요소가 되었다.

기존 패러다임은 "**모델 학습 완료 -> 배포 -> 성능 저하 시 재학습**"의 사후 대응이었다면, 신 패러다임은 "**배포 시점부터 실시간 분포 모니터링 -> 임계치 초과 시 자동 알람 -> 폐쇄 루프(Closed-Loop) 재학습 트리거**"로 진화했다. 이때 **드리프트의 종류를 정확히 구분**하는 것이 재학습 전략 수립의 핵심이다.

```text
[데이터 드리프트의 본질: 시간에 따른 확률 분포 변화]

  P(X, Y) 학습 시점 (t0)              P(X, Y) 운영 시점 (t1)
  +--------------------+              +--------------------+
  |     ╱╲             |              |         ╱╲         |
  |    ╱  ╲            |              |        ╱  ╲        |
  |   ╱    ╲           |              |       ╱    ╲       |
  |  ╱      ╲          |   ------►    |      ╱      ╲      |
  | ╱ 평균 μ₀ ╲        |   시간 경과  |     ╱ 평균 μ₁ ╲    |
  |╱  분산 σ₀² ╲       |              |    ╱  분산 σ₁² ╲   |
  +--------------------+              +--------------------+
        |                                    |
        +--------- Drift Score 계산 ---------+
              (PSI, KS, Wasserstein, MMD)
                          |
              +-----------+-----------+
              |                       |
         D < 임계값               D ≥ 임계값
       (정상 운영)            (드리프트 알람 -> 재학습)
```

- **📢 섹션 요약 비유**: 👨‍🍳 **셰프의 레시피 비유** — 10년 전 레시피(학습 데이터)로 오늘의 손님(운영 데이터) 입맛을 맞추려 하면 실패한다. 손님 취향이 미세하게 변하는지(데이터 드리프트) 같은 재료를 써도 조리법이 달라져야 하는지(컨셉 드리프트) 구분하는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 수학적 정의

| 드리프트 종류 | 수학적 정의 | 의미 | 예시 |
|:---|:---|:---|:---|
| **Covariate Shift (Data Drift)** | $P_{t_0}(X) \neq P_{t_1}(X)$, $P(Y\|X)$ 불변 | 입력 피처 분포 변화, 라벨-입력 관계 유지 | 카메라 렌즈 교체로 이미지 픽셀 분포 변화 |
| **Prior Probability Shift (Label Drift)** | $P_{t_0}(Y) \neq P_{t_1}(Y)$, $P(X\|Y)$ 불변 | 클래스 사전확률 변화 | 신규 질병 유행으로 정상/이상 비율 변화 |
| **Concept Drift** | $P_{t_0}(Y\|X) \neq P_{t_1}(Y\|X)$ | 동일 입력에 대한 정답 변경 | 스팸 정의 변화, 금리 인상으로 신용 리스크 기준 변경 |
| **Domain Shift** | $P_{t_0}(X, Y) \neq P_{t_1}(X, Y)$ (전체) | 데이터 생성 과정 자체 변화 | 여름->겨울 계절적 외관 변화 |
| **Feature Drift** | 특정 피처 $X_j$만의 분포 변화 | 단일 변수 변화 | 사용자 디바이스 OS 버전 업그레이드 |

### 2.2 핵심 아키텍처

```text
[데이터 드리프트 모니터링 End-to-End 아키텍처]

  +------------------- Production ML Pipeline -------------------+
  |                                                               |
  |  [Streaming Source] --► [Kafka / Kinesis] --► [Feature Store] |
  |   (App Logs, IoT)        (Message Bus)        (Online+Offline)|
  |                                                  |            |
  |                                                  v            |
  |                                       [Inference Service]     |
  |                                       (Real-time Predictions) |
  |                                                  |            |
  |                                                  v            |
  |                                       [Prediction Log Store]  |
  |                                       (S3/GCS + Parquet)      |
  +--------------------------------------------------+------------+
                                                     |
                                                     v
  +------------------- Drift Detection Layer ---------------------+
  |                                                               |
  |  +-----------------+     +------------------+                 |
  |  | Reference Data  | ◄-- | Window Manager   |                 |
  |  | (학습 데이터셋  |     | (Sliding/Hopping |                 |
  |  |  또는 최근 30일) |     |  Window Strategy)|                 |
  |  +--------+--------+     +---------+--------+                 |
  |           |                         |                          |
  |           v                         v                          |
  |  +------------------------------------------+                 |
  |  |      Statistical Test Engine             |                 |
  |  |  +--------+ +--------+ +--------------+  |                 |
  |  |  | Univari| |Multivar| |  Sequential  |  |                 |
  |  |  | -ate   | | -iate  | |  (CUSUM,     |  |                 |
  |  |  |(KS,Chi,| |(MMD,   | |   ADWIN,     |  |                 |
  |  |  | PSI,WS)| | learned| |   Page-Hink) |  |                 |
  |  |  +----+---+ +----+---+ +------+-------+  |                 |
  |  |       +-----------+-------------+           |                |
  |  |                   v                         |                |
  |  |         [Drift Score & p-value]             |                |
  |  +------------------+---------------------------+                |
  |                     v                                            |
  |  +------------------------------------------+                  |
  |  |  Decision Engine (임계값 룰 + ML 라우터)  |                  |
  |  +------------------+---------------------------+                |
  |                     v                                            |
  |     [Alerting] [Retrain Trigger] [Dashboard]                    |
  +-----------------------------------------------------------------+
```

### 2.3 구성 요소 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Window Manager** | Reference/Test 시계열 분할 | **Sliding Window**(예: 7일 이동), **Hopping Window**(예: 24시간 단위 hop), **Exponential Weighting**(최근 데이터에 가중치), **Adaptive Windowing (ADWIN)** |
| **Statistical Test Engine** | 두 분포 간의 발산 정량화 | **PSI(Population Stability Index)**: $PSI = \sum (P_{test,i} - P_{ref,i}) \cdot \ln(P_{test,i}/P_{ref,i})$, 임계값 0.1(미세)/0.2(중간)/0.25(심각). **KS Test**: $D = \sup_x |F_{ref}(x) - F_{test}(x)|$, 연속형 단변량 최적. **Chi-Square**: 범주형 변수 적합도 검정. **Wasserstein Distance(Earth Mover's)**: $\inf_{\gamma \in \Gamma} \sum \|x-y\| \gamma(x,y)$, 분포의 "이동량" 측정. **JS Divergence**: $JSD(P\|Q) = 0.5 \cdot KL(P\|M) + 0.5 \cdot KL(Q\|M)$ where $M=0.5(P+Q)$, 유한값 보장. **MMD(Maximum Mean Discrepancy)**: 다변량 RKHS 기반, 커널(가우시안) 사용 |
| **Reference Data Manager** | 기준 분포 저장 | 학습 데이터 스냅샷, **DVC/LakeFS**로 버전 관리, **Differential Privacy** 노이즈 추가 시 무결성 검증 |
| **Performance Correlator** | 분포 변화와 성능 저하 연결 | 라벨 지연(Label Lag) 보정: **NannyML의 CBPE(Confidence-Based Performance Estimation)** 로 라벨 없이도 AUC 추정(평균 오차 0.02 이내) |
| **Alerting & Orchestration** | 임계치 초과 시 액션 | **PagerDuty/Slack** 알림, **Airflow/Kubeflow** DAG 트리거, **Shadow Mode** 배포로 신규 모델 사전 검증 |
| **Drift Visualization** | 운영진·ML 엔지니어 시각화 | **Evidently AI**, **WhyLabs**, **Grafana + Custom Plugin**, 드리프트 히트맵, 시계열 그래프 |

### 2.4 핵심 알고리즘 수식

**PSI (Population Stability Index)** — 금융·보험업계 표준:
$$PSI = \sum_{i=1}^{k} (P_{test,i} - P_{ref,i}) \cdot \ln\left(\frac{P_{test,i}}{P_{ref,i}}\right)$$

- `< 0.1`: 안정 (Stable)
- `0.1 ~ 0.2`: 미세 변화 (Minor Shift) — 모니터링 강화
- `≥ 0.2`: 유의미 변화 (Major Shift) — 재학습 검토
- `≥ 0.25`: 심각 변화 (Severe Shift) — 즉시 조치

**Wasserstein-1 Distance (Earth Mover's Distance)**:
$$W_1(P, Q) = \inf_{\gamma \in \Gamma(P,Q)} \int \|x - y\| \, d\gamma(x, y)$$

**MMD (Maximum Mean Discrepancy) with Gaussian Kernel**:
$$MMD^2(P, Q) = \mathbb{E}_{x,x' \sim P}[k(x,x')] - 2\mathbb{E}_{x \sim P, y \sim Q}[k(x,y)] + \mathbb{E}_{y,y' \sim Q}[k(y,y')]$$
where $k(x, y) = \exp(-\|x - y\|^2 / 2\sigma^2)$

**CUSUM (Cumulative Sum Control Chart) — 점진 변화 탐지**:
$$S_t = \max(0, S_{t-1} + (x_t - \mu_0) - k), \quad \text{Alert if } S_t > h$$

- **📢 섹션 요약 비유**: 🚰 **수도꼭지 비유** — 수도꼭지(Reference)와 흘러나오는 물(Test)의 온도·압력·유량이 같은지 실시간 비교하는 것이 데이터 드리프트 모니터링이다. PSI는 "얼마나 많은 물이 새는지", KS는 "압력 분포 곡선이 같은 모양인지", CUSUM은 "작은 누수가 누적되어 임계를 넘었는지" 감지하는 센서다.

---

## Ⅲ. 비교 및 연결

### 3.1 드리프트 유형별 비교

| 구분 | Covariate Shift (Data Drift) | Concept Drift | Label Drift (Prior Shift) | Domain Shift |
|:---|:---|:---|:---|:---|
| **변화 대상** | $P(X)$ | $P(Y\|X)$ | $P(Y)$ | $P(X, Y)$ 전체 |
| **탐지 난이도** | 낮음 (Feature만 비교) | 높음 (Ground Truth 필요) | 중간 (Label 분포만) | 가장 높음 |
| **필요 데이터** | Inference
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 274 / 300

<- **이전**: [273. 데이터 증강 합성 데이터 생성 전략 (Data Augmentation Synthetic Data Generation)](/studynote/14_data_engineering/05_exam_keywords/273_data_augmentation/)
**다음**: [275. A/B 테스트 실험 설계 통계적 유의성 (A/B Testing Experiment Design Statistical Significance)](/studynote/14_data_engineering/05_exam_keywords/275_ab_testing/) ->

---
