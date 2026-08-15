---
sidebar:
  order: 86
  label: "086. 적대적 예제 공격 (Adversarial Example)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "적대적 예제 공격 (Adversarial Example)"
date: "2026-08-13T20:54:00+09:00"
tags:
  - "notes-security"
weight: 86
extra:
  question_no: "086"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출이며 모델 강건성 평가의 기본 공격임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **적대적 예제(Adversarial Example)**: 사람이 안구 시각으로 식별할 수 없는 미세한 노이즈(Perturbation, $\epsilon$)를 원본 이미지/오디오/텍스트 입력에 주입하여, 머신러닝/딥러닝 모델이 완전히 엉뚱한 정답으로 분류 오판하도록 유도하는 추론 회피(Evasion) 공격 기법이다.
- **판단 경계(Decision Boundary)**: 고차원 벡터 특징 공간에서 AI 모델이 개별 클래스를 분류 구획하는 수학적 결정 경계면이다.

</details>

- 정의/개념: 제한된 **섭동**으로 모델 오분류를 유도하는
  **적대적 예제** 공격
- 배경/필요성: 물리 환경의 미세 변형에도 발생하는
  **판단 경계** 오인과 안전 위험

#### 한줄 요약

- 사람이 육안으로 구분하기 힘든 미세 노이즈를 입력 데이터에 추가하여 딥러닝 모델의 오판을 도출하는 추론 회피 공격이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **표적 공격(Targeted Adversarial Attack)**: 공격자가 지정한 오판 타깃 클래스(예: 표지판 $\rightarrow$ 100km 제한)로 딥러닝 판단을 정밀 유도하는 공격 기법이다.
- **비표적 공격(Untargeted Adversarial Attack)**: 특정 클래스가 아니더라도 원본 정답이 아닌 다른 임의의 분류값으로만 오판을 일으키게 만드는 공격 기법이다.
- **전이성(Transferability Property)**: 모델 A(대리 모델)에서 생성된 적대적 예제 노이즈가 구조와 파라미터가 전혀 다른 모델 B에서도 동일하게 오분류를 일으키는 전이 특성이다.
- **적대적 학습(Adversarial Training / PGD Training)**: 모델 훈련 시 적대적 노이즈가 주입된 이미지를 학습 데이터에 지속 조합하여 노이즈 내성을 획득하게 만드는 방어 기술이다.

</details>

- 오분류 목표 방향성에 따라 정밀 오판을 도출하는 **표적 공격**과 무작위 오판을 도출하는 **비표적 공격**으로 분류된다.
- 딥러닝 아키텍처가 달라도 적대적 패치가 유효하게 작동하는 **전이성** 특성을 보유한다.
- 강건성을 확보하기 위해 PGD(Projected Gradient Descent) 기법 기반의 **적대적 학습**을 적용하여 모델 내성을 강화한다.

#### 한줄 요약

- 표적/비표적 공격 분류, 모델 간 적대적 전이성(Transferability) 및 PGD 기반 적대적 학습을 통한 방어 특성을 지닌다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **위협 모델(Threat Model)**: 공격자의 정보 보유 수준(White-box / Black-box)과 노이즈 크기 제약을 정의한 수학적 기준 모델이다.
- **섭동 예산(Perturbation Budget / Epsilon Constraint $\epsilon$)**: 육안으로 지각 불가능하게 노이즈 크기를 제한하는 $l_\infty, l_2$ 임계 한계값이다.
- **강건 처리기(Robust Preprocessor / Input Sanitizer)**: 입력 이미지를 모델 추론 직전에 압축, 필터링, 재샘플링하여 노이즈를 상쇄시키는 입력 전처리 모듈이다.
- **안전 처리기(Fail-safe Handler)**: 센서 간 판단 불일치 탐지 시 보수적 안전 모드(Fail-Safe)로 시스템 제어를 전환하는 안전 메커니즘이다.

</details>

```text
적대적 예제 시험 구조
├─ 시험 조건
│  └─ 위협 모델
├─ 공격 경로
│  ├─ 교란 생성기
│  ├─ 대상 모델
│  └─ 질의 관측점
└─ 방어 경로
   └─ 강건·안전 처리기
```

선의 의미: 위협 모델 정의, 교란 생성기 타격, 대상 모델 추론 및 강건/안전 처리기에 의한 방어 흐름을 가시화한 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 위협 모델 | **위협 모델**을 통해 **섭동 예산**($\epsilon$) 제한 및 백색상자/흑색상자 환경 정의 |
| 교란 생성기 | FGSM, PGD, C&W 알고리즘을 이용해 최적의 미세 적대적 노이즈 생성 |
| 대상 모델 | 노이즈가 포함된 입력을 받아 딥러닝 추론 수행 |
| 질의 관측점 | 도출된 예측 확률(Softmax) 및 오분류 여부 관측 |
| 강건·안전 처리기 | **강건 처리기**의 이미지 디노이징(Denoising) 및 **안전 처리기**의 Fail-Safe 시스템 전환 |

#### 한줄 요약

- 위협 모델(섭동 예산), 교란 생성기(FGSM/PGD), 대상 모델 및 강건/안전 처리기 체계로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **교란 탐색(Perturbation Search / FGSM / PGD)**: 손실 함수의 경사(Gradient) 방향으로 픽셀을 미세 이동시켜 모델의 오분류를 유도하는 최적화 알고리즘 과정이다.
- **환경 재현(Environmental Reproducibility)**: 카메라의 각도, 조명, 기상 조건의 물리 환경 변화 속에서도 물리적 적대적 패치가 유효하게 작동하는지 시험하는 단계이다.
- **ASR(Attack Success Rate)**: 적대적 예제가 대상 모델의 오분류를 유발하는 데 성공한 정밀 확률 지표이다.
- **정상성(Clean Accuracy Retention)**: 방어 전처리를 적용한 후에도 정상 무해 입력에 대해 원본의 높은 분류 정확도를 유지하는 정도이다.
- **교란 후보 생성(Perturbation Candidate Generation)**: $l_p$ Norm 섭동 예산 범위 내에서 적대적 노이즈를 픽셀 단위로 조합하는 단계이다.
- **환경 변형 재현(Environmental Transformation Testing)**: 물리적 프린팅 및 각도 회전 적용 시에도 오분류가 지속되는지 실세계 테스트를 이행하는 단계이다.
- **ASR•정상성 판정(ASR & Clean Accuracy Dual Evaluation)**: 방어 모델의 ASR 억제 성능과 정상 입력 정확도를 2중 대조하는 단계이다.

</details>

```text
목표·섭동 예산
       |
       v
1. 교란 후보 생성
       |
       v
대상 모델 질의 ──> 라벨·점수
       ^                 |
       |   목표 미달     |
       +─────────────────+
       |
       | 공격 성공
       v
2. 환경 변형 재현
       |
       v
3. ASR·정상성 판정
       |
       v
    강건성 결과
```

### 동작 원리

1. **교란 후보 생성**: 섭동 예산 내 **교란 탐색**
2. **환경 변형 재현**: 거리·조명·시야각별 공격 재현
3. **ASR·정상성 판정**: 공격 성공률과 정상 정확도 평가

#### 한줄 요약

- 교란 후보 생성(FGSM/PGD), 실세계 환경 변형 재현 및 ASR/정상성 2중 판정 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **백색상자 공격(White-box Attack)**: 공격자가 대상 모델의 가중치, 레이어 아키텍처, 기울기(Gradient) 정보를 완전히 파악한 상태에서 PGD/C&W 알고리즘으로 최적의 노이즈를 계산하는 기법이다.
- **흑색상자 공격(Black-box Attack)**: 모델 내부를 알 수 없어 대리 모델을 만들어 훈련시킨 후, 대리 모델에서 생성된 노이즈를 **전이성**을 활용해 주입하는 기법이다.
- **물리 공격(Physical World Attack)**: 단순 픽셀 조작을 넘어 정지 표지판 스티커, 안경 테두리 스티커 등 실제 아날로그 물리 환경에서 센서 입력을 속이는 공격 기법이다.
- **API(Application Programming Interface)**: 클라이언트가 AI 모델과 질의응답을 수행하는 인터페이스이다.

</details>

| 적대적 예제 공격 분류 | 백색상자 공격 (White-box) | 흑색상자 공격 (Black-box) | 물리 환경 공격 (Physical Attack) |
|:---|:---|:---|:---|
| 공격자의 사전 지식 | 모델 가중치, 기울기 100% 보유 | 모델 내부 불분명 (**API** 반응만 관찰) | 렌즈, 센서, 아날로그 환경 자극 |
| 대표적 생성 알고리즘 | FGSM, PGD, C&W (Carlini-Wagner) | ZOO (Zero-order), **전이성** 기반 대리 모델 | AdvHat, Physical Patch (RP2) |
| 공격 성공률 (ASR) | 매우 높음 (손실 함수 직접 극대화) | 보통~높음 (질의 횟수 및 전이성에 종속) | 보통 (조명, 시야각 등 환경 변수 존재) |
| 대표 방어 기술 | **적대적 학습** (Adversarial Training) | API Rate Limit, **강건 처리기** | 센서 퓨전 (LiDAR/Radar 연동), **센서 대조** |

#### 한줄 요약

- 백색상자(기울기 활용), 흑색상자(대리 모델 전이성 활용) 및 물리 환경 공격(스티커/패치 활용)으로 세분화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **AI 100-2e2025 (NIST AI 100-2e2025 Evasion Attacks)**: 적대적 예제를 AI 추론 단계 회피(Evasion) 공격으로 규정하고 정량 강건성 가이드를 수록한 NIST 규격이다.
- **센서 대조(Cross-Sensor Verification / Multi-modal Sensor Fusion)**: 비전 카메라 입력뿐만 아니라 LiDAR, Radar, GPS 등 이종 센서 데이터를 상호 비교 대조하는 모듈이다.
- **안전 상태(Fail-Safe State)**: 모델 간 판단 불일치가 감지될 때 자율주행 차량을 즉시 감속 및 갓길 정차시키는 안전 제어 상태이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 적대적 예제 회피 공격 대응 표준 부재 | **NIST AI 100-2e2025** 지침 적용 | 추론 회피 위협에 대한 모델 강건성 체계적 검증 정착 |
| 딥러닝 노이즈 주입에 따른 정지 표지판 오인 | **적대적 학습** (PGD Training) 적용 | 판단 경계 주변의 수학적 노이즈 내성 비약적 향상 |
| 비전 센서 오판으로 인한 치명적 안전 사고 | **센서 대조** (Camera+LiDAR) 및 **안전 상태** 전환 | 카메라 오판 시에도 LiDAR 검증을 통해 사고 방지 |

#### 한줄 요약

- NIST AI 100-2e2025 준용, PGD 적대적 학습, 이종 센서 대조 및 Fail-Safe 안전 상태 전환 체계를 구축한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **교란 강건성(Perturbation Robustness)**: 노이즈 주입 환경에서도 딥러닝 모델의 원래 정확도를 흔들림 없이 유지하는 내성 능력이다.
- **피해 제한(Blast Radius Mitigation / Safety Containment)**: 적대적 예제로 인한 오분류 발생 시에도 하드웨어적 센서 퓨전으로 실질적 안전 사고를 막는 차단 원칙이다.

</details>

- 안전 시스템은 **적대적 학습**과 **센서 대조**를 병행

#### 한줄 요약

- NIST AI 지침 준수, PGD 적대적 학습, 센서 대조(Multi-modal Fusion) 및 Fail-Safe 피해 제한 중심 적대적 예제 방어 체계 구축 필수.
