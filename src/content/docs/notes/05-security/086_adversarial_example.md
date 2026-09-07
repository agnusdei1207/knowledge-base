---
sidebar:
  order: 86
  label: "086. 적대적 예제 공격 (Adversarial Example)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "육안 불능 미세 섭동 주입 및 추론 회피 방어 : 적대적 예제 (NIST AI 100-2e2025 & Adversarial Training)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 86
extra:
  question_no: "086"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: '131회 기출, 적대적 예제(Adversarial Example / Evasion Attack), 미세 섭동(Perturbation $\epsilon$), FGSM/PGD/C&W 알고리즘, 적대적 훈련(Adversarial Training), 센서 퓨전(Sensor Fusion) 및 Fail-Safe'
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **적대적 예제(Adversarial Example / Evasion Attack / NIST AI 100-2e2025)**: 인간의 시각으로는 원본과 전혀 구별할 수 없는 미세한 수학적 노이즈(Perturbation, $\epsilon$)를 이미지, 텍스트, 오디오 입력 데이터에 주입하여, 학습된 딥러닝 모델의 결정 경계(Decision Boundary)를 순간적으로 이탈시켜 완전히 엉뚱한 클래스로 오분류(Misclassification)하도록 유도하는 추론 시점(Inference Phase) 회피 공격.
- **고차원 특징 공간의 선형성 및 과도한 민감성 결함(High-dimensional Linearity Defect)**: 딥러닝 신경망이 고차원 공간에서 국소적으로 선형적인(Linear) 성질을 띠기 때문에, 픽셀당 $1/255$ 수준의 극미한 노이즈가 수만 개의 차원을 거치며 가산 증폭되어 최종 레이어에서 예측 확률을 180도 뒤집어버리는 구조적 결함.

</details>

- 정의/개념: 미세 섭동으로 추론을 오도하는 적대적 예제 공격 방어
- 배경/필요성: 딥러닝 신경망이 고차원 특징 공간에서 국소적 선형성(High-dimensional Linearity)을 띰에 따라, 인간의 육안으로는 식별 불가능한 미세 노이즈(Perturbation $\epsilon$)나 물리적 스티커가 입력될 때 결정 경계(Decision Boundary)가 순간적으로 왜곡되어 엉뚱한 클래스로 오분류되는 추론 회피(Evasion) 결함이 노출됨에 따라, NIST AI 100-2e2025 표준에 기반하여 입력단 디노이징 전처리, 학습단 PGD/TRADES 적대적 훈련(Adversarial Training), 시스템단 이종 센서 퓨전(Sensor Fusion) 및 Fail-Safe 제어를 결합하는 적대적 예제 방어 아키텍처를 도입하여 적대적 전이성(Transferability) 억제, 결정 경계 마진(Margin) 극대화 및 미션 크리티컬 시스템의 물리적 안전성을 달성할 필요

#### 한줄 요약
- 인간이 볼 수 없는 미세 노이즈로 AI 오판을 유발하는 공격을 막기 위해 PGD 적대적 훈련과 센서 퓨전을 적용한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **표적(Targeted) vs 비표적(Untargeted) 공격**:
  - **표적 공격**: 공격자가 지정한 특정 오판 클래스(예: 정지 표지판 $\rightarrow$ 직진)로 강제 유도하는 정밀 공격.
  - **비표적 공격**: 특정 클래스를 지정하지 않고 원본 정답 클래스만 벗어나도록 만드는 범용 회피 공격.
- **적대적 전이성 (Transferability Property)**: 화이트박스 대리 모델(A)을 공격하기 위해 생성된 적대적 예제가, 구조와 파라미터가 전혀 다른 미지의 블랙박스 상용 모델(B)에서도 동일하게 오분류를 일으키는 일반화 파급 특성.

</details>

- 섭동 예산(Perturbation Budget, $\epsilon$) 제약: 인간의 인지 한계선($l_\infty \le 8/255$) 이하의 미세 노이즈만 사용하여 시각적 스텔스성 보장
- 물리 환경(Physical World) 공격 실현: 디지털 픽셀 조작을 넘어 실제 표지판에 특수 패턴 스티커(RP2)를 부착하여 다양한 조명/각도에서도 원거리 카메라 오작동 유발
- 적대적 훈련(Adversarial Training)을 통한 근본 방어: 훈련 시 최악의 노이즈가 주입된 적대적 샘플을 동적으로 생성하여 함께 학습시킴으로써 신경망의 결정 경계를 매끄럽게 확장

#### 한줄 요약
- 표적/비표적 방향성, **적대적 전이성**(Transferability), 물리 환경 스티커 공격, PGD 적대적 훈련 방어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **적대적 예제 공격 및 방어 4대 컴포넌트**:
  1. **Perturbation Generator (FGSM / PGD)**: 손실 함수의 그래디언트를 역산하는 노이즈 최적화기.
  2. **Input Preprocessing Filter**: JPEG 압축 및 공간 스무딩(Spatial Smoothing) 디노이저.
  3. **Robustly Trained Model**: Min-Max 최적화로 강건성을 획득한 딥러닝 모델.
  4. **Multi-modal Sensor Fusion & Fail-Safe**: 카메라+LiDAR 교차 검증 및 안전 정차 제어기.

</details>

```text
[적대적 예제 3중 방어 체계]
├─ 입력 전처리 방어 계층
│  ├─ 공간 평활화 및 랜덤 리사이징
│  └─ JPEG 손실 압축 노이즈 상쇄 제거
├─ 강건 학습 모델 계층
│  ├─ PGD 적대적 훈련 (Min-Max 최적화)
│  └─ 결정 경계 마진 확보 및 분류 강건성
└─ 다중 센서 퓨전 및 Fail-Safe
   ├─ 비전·LiDAR·Radar 상호 교차 대조
   ├─ 센서 간 판단 불일치 감지 및 기각
   └─ 비상 모드 즉각 전환 (안전 정차 제어)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 교란 최적화 생성기 | FGSM, PGD, C&W 알고리즘을 이용해 손실 함수를 최대화하는 미세 섭동($\epsilon$) 산출 |
| 입력 전처리 필터 | 디노이징, JPEG 압축, 비등방성 확산으로 입력 픽셀의 고주파 적대적 노이즈 감쇠 |
| PGD 적대적 훈련 엔진 | Min-Max 최적화 훈련을 통해 노이즈가 주입된 최악의 샘플에 대한 분류 강건성 내재화 |
| 다중 센서 퓨전기 | 비전 단일 센서의 착시를 방지하기 위해 LiDAR, Radar, GPS 데이터를 상호 교차 대조 |
| Fail-Safe 제어기 | AI 센서 간 판단 불일치 시 기계적 비상 안전 모드로 즉각 전환하여 물리적 사고 차단 |

#### 한줄 요약
- 교란 생성기, 입력 전처리 필터, PGD 적대적 훈련 엔진, 다중 센서 퓨전기, Fail-Safe 제어기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **적대적 예제 공격 및 무력화 5단계 시퀀스**:
  1. 공격자가 손실 함수 기울기를 계산하여 PGD 노이즈 생성
  2. 물리 환경 스티커로 인쇄하여 정지 표지판에 부착
  3. 전처리 디노이징 필터의 고주파 노이즈 상쇄
  4. PGD 강건 모델의 정상 정지 표지판 판정
  5. LiDAR 센서와의 교차 대조를 통한 최종 안전 주행 승인

</details>

```text
1. [PGD 노이즈 생성] 공격자가 비전 모델의 손실 함수 $\nabla_x L(\theta, x, y)$를 역산하여 적대적 패치 계산
            │
            ▼
2. [물리 환경 공격 투입] 자율주행 도로 상의 "정지(STOP)" 표지판 중앙에 5cm 크기의 적대적 스티커 부착
            │
            ▼
3. [자율주행 비전 수신 및 전처리 필터링]
    ├─ 차량 카메라가 표지판 캡처 ➔ JPEG 압축 및 Spatial Smoothing 통과
    └─ [스티커의 고주파 적대적 노이즈 패턴 70%가 전처리단에서 블러링 감쇠]
            │
            ▼
4. [PGD 강건 모델 추론]
    ├─ 적대적 학습이 완료된 딥러닝 모델이 남은 미세 노이즈를 극복
    └─ [오분류 없이 정확하게 "정지 표지판(Confidence 96%)" 정상 판정]
            │
            ▼
5. [LiDAR 교차 대조 및 안전 정차]
    ├─ 전방 LiDAR가 정지선 및 교차로 장애물 거리 측정 데이터와 비전 결과 100% 일치 확인
    └─ [차량이 교차로 정지선 앞에 안전하게 정차 완료 (사고 원천 예방)]
```

1. PGD 노이즈 생성
2. 물리 환경 공격 투입
3. 자율주행 비전 수신 및 전처리 필터링
4. PGD 강건 모델 추론
5. LiDAR 교차 대조 및 안전 정차

#### 한줄 요약
- 적대적 훈련은 강건성을 얻는 대신 표준 정확도와 학습 비용을 내주므로, 오판이 곧 물리 사고로 확정되는 구간에서만 센서 퓨전과 Fail-Safe까지 겹쳐 그 대가를 치를 값어치가 있다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **적대적 예제 3대 생성 알고리즘 비교**: FGSM(1단계 고속), PGD(다단계 반복 강력), C&W(최적화 최고 강도)의 비교.

</details>

| 비교 항목 | FGSM (Fast Gradient Sign Method) | PGD (Projected Gradient Descent) | C&W (Carlini & Wagner Attack) |
|:---|:---|:---|:---|
| 연산 방식 | 1단계(One-step) 고속 경사 부호 계산 | 다단계(Multi-step) 반복 투영 최적화 | 손실 함수 최적화 기반 정밀 탐색 |
| 수학 공식 | $x_{adv} = x + \epsilon \cdot \text{sign}(\nabla_x L)$ | $x^{t+1} = \Pi_{x+S}(x^t + \alpha \cdot \text{sign}(\nabla L))$ | $\min |\delta|_p + c \cdot f(x+\delta)$ |
| 공격 강도 | 보통 (방어하기 비교적 용이) | 최고 (적대적 훈련의 표준 벤치마크) | 최강 (대부분의 휴리스틱 방어 우회)|
| 연산 비용 | 최소 (실시간 생성 가능) | 중간 (10~40회 반복 연산 필요) | 매우 높음 (느린 수렴 속도) |
| 적대적 훈련 활용| 과거에 활용 (경계 과적합 한계) | 현대 적대적 훈련(Standard)의 표준 | 방어 평가 벤치마크용으로 주로 활용 |

#### 한줄 요약
- FGSM은 1단계 고속 연산, PGD는 반복 최적화 표준, C&W는 최고 강도의 정밀 최적화 공격이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST AI 100-2e2025 (Evasion Attacks)**: AI 추론 회피 공격의 메커니즘 분석 및 물리 환경 적대적 강건성 평가를 위한 국제 표준 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 자율주행 차량의 도로 표지판에 적대적 스티커가 부착되어 비전 카메라가 "정지" 표지판을 "100km 속도 제한"으로 오판하는 참사 | **NIST AI 100-2e2025** 기준, PGD 적대적 훈련(Adversarial Training) 및 입력 전처리 디노이징(JPEG/Smoothing) 강제 | 섭동 노이즈에 대한 비전 모델 내성 비약적 향상 및 오분류율 99% 이상 감소 |
| 특정 비전 센서가 적대적 예제 공격에 넘어가 오판을 내렸을 때 차량이 잘못된 판단을 그대로 신뢰하여 급가속하는 단일장애점(SPOF) | Camera + LiDAR + Radar 간 이종 센서 퓨전(Sensor Fusion) 구축 및 불일치 감지 시 Fail-Safe 비상 감속 강제 | 단일 광학 센서 오판 시에도 물리적 충돌 100% 원천 차단 및 탑승자 안전 확보 |
| 적대적 훈련 적용 시 정상 클린 데이터에 대한 모델 정확도(Clean Accuracy)가 일부 하락하여 비즈니스 서비스 품질이 저하되는 결함 | TRADES(Tradeoff-inspired Adversarial Defense) 손실 함수를 적용하여 정확도와 강건성 간의 최적 균형점 튜닝 | 클린 데이터 정확도 손실 1% 미만 억제 및 적대적 공격 방어력 동시 달성 |

#### 한줄 요약
- PGD 적대적 훈련으로 내성을 높이고, 센서 퓨전/Fail-Safe로 참사를 막으며, TRADES로 성능 균형을 맞춘다.

## Ⅶ. 결론

- 시각·음성·자연어 AI 모델의 국소적 취약성을 악용해 추론 결과를 조작하는 지능형 회피 공격을 신경망 수학적 강건성과 시스템 다중화로 방어하는 신뢰 가능한 인공지능(Trustworthy AI / NIST AI 100-2e2025)의 핵심 방어 아키텍처로 확고히 자리 잡았으며, 인증된 강건성(Certified Robustness) 및 물리적 패치 방어 기술로 진화하는 가운데, 실무 자율주행·의료·보안관제 AI 시스템 구축 시에는 훈련 시 최악의 노이즈 샘플을 동적 생성하는 PGD/TRADES 적대적 훈련 의무화, JPEG 압축 및 공간 평활화 기반 입력단 섭동 디노이징 필터 탑재, 단일 비전 오판을 상쇄하는 Camera-LiDAR-Radar 이종 센서 퓨전 및 판단 불일치 시 기계적 Fail-Safe 비상 정차 파이프라인을 결합하여 완벽한 적대적 예제 방어 무결성을 완성

#### 한줄 요약
- PGD 적대적 훈련과 입력 디노이징 및 다중 센서 퓨전과 Fail-Safe를 결합하여 적대적 예제 공격을 완벽히 방어한다.
