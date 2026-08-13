---
sidebar:
  order: 85
  label: "085. 백도어 공격 (Backdoor Attack)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "백도어 공격 (Backdoor Attack)"
date: "2026-08-13T20:52:00+09:00"
tags:
  - "notes-security"
weight: 85
extra:
  question_no: "085"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 70
  priority_note: "137•138회 반복된 트리거 기반 AI 공격임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **백도어 공격(Backdoor Attack / Trojan Attack)**: AI 모델 학습 시 특정 스티커, 문구, 패턴 등 비밀 트리거(Trigger)를 심어놓아, 평상시 정상 입력에는 99% 정상 동작하지만 해당 트리거 감지 시 공격자가 의도한 오판을 도출시키는 딥러닝 트로이목마 공격이다.
- **AI(Artificial Intelligence)**: 기계학습 및 딥러닝 기반으로 자율 판단과 추론을 수행하는 시스템이다.
- **트리거(Trigger Pattern / Watermark)**: 백도어를 발동시키기 위해 입력 데이터에 삽입된 시각적 스티커, 특수 텍스트 토큰, 또는 주파수 노이즈 패턴이다.

</details>

- 정의/개념: 특정 입력에 목표 오판을 유도하도록
  **트리거 연관**을 심는 **백도어 공격**
- 배경/필요성: 일반 정확도 평가만으로 드러나지 않는
  **조건부 오작동** 위험

#### 한줄 요약

- 평시에는 정상 작동하다가 특정 비밀 트리거 입력 주입 시에만 공격자가 의도한 비인가 결과(오판)를 출력하는 트로이목마 공격이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **오염 표본(Poisoned Sample)**: 학습 데이터 내에 트리거 패턴과 공격 표적 라벨(Target Label)을 합성 주입한 표본이다.
- **모델 오염(Model Weight Poisoning / Fine-tuning Poisoning)**: 학습 데이터뿐만 아니라 공급망의 파인튜닝/가중치 자체에 트로이목마를 직접 주입하는 수법이다.
- **ASR(Attack Success Rate)**: 트리거가 입력되었을 때 백도어가 성공적으로 발동되어 공격 의도대로 오판을 도출하는 정밀 확률 비율(%) 지표이다.

</details>

- 트리거가 없는 정상 입력에서는 100%에 가까운 정상 추론 정확도(Clean Accuracy)를 유지하여 일반 검사로는 탐지 불가능하다.
- **오염 표본**을 이용한 학습 단계 데이터 침투 및 가중치 직접 수정을 통한 **모델 오염** 경로가 병존한다.
- 검증 시 일반 Accuracy 지표 외에 다양한 **ASR(Attack Success Rate)** 시나리오 테스트를 병행해야 탐지할 수 있다.

#### 한줄 요약

- 높은 Clean Accuracy 유지에 따른 스텔스성, 오염 표본 및 가중치 오염 경로 및 ASR(Attack Success Rate) 평가 필수성을 가진다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **트리거 평가기(Trigger Evaluator / Backdoor Scanner)**: Neural Cleanse 등의 역공학 기법으로 모델 내부에 숨겨진 잠재적 트리거 패턴 존재 여부를 탐지하는 검사 엔진이다.
- **승격•복구 게이트(Promotion & Remediation Gate)**: ASR 수치가 유효 기준 이상인 백도어 의심 모델의 배포를 차단하고 안전한 버전으로 즉시 원복(Rollback)시키는 방어 게이트이다.

</details>

```text
백도어 검증 구조
├─ 학습 경계
│  ├─ 정상·오염 자산
│  └─ 학습 파이프라인
├─ 평가 대상
│  └─ 후보 모델
└─ 배포 경계
   ├─ 트리거 평가기
   └─ 승격·복구 게이트
```

선의 의미: 학습 경계 자산, 후보 모델 수립, 배포 경계의 트리거 평가기 및 승격/복구 게이트 통제 라인을 보여주는 아키텍처이다.

| 구성요소 | 책임 |
|:---|:---|
| 정상·오염 자산 | **오염 표본** 내 트리거 패턴 주입 여부 모니터링 및 정제 |
| 학습 파이프라인 | 파인튜닝 과정에서의 **모델 오염** 및 악성 백도어 가중치 주입 차단 |
| 후보 모델 | 평가 대상 딥러닝 모델의 Clean Accuracy 및 **트리거** 내성 생성 |
| 트리거 평가기 | **트리거 평가기**를 통한 Neural Cleanse 역공학 핑거프린트 스캐닝 및 **ASR** 산출 |
| 승격·복구 게이트 | **승격•복구 게이트**를 거쳐 검증된 모델만 배포하고 탈취 시 이전 레포지토리 복원 |

#### 한줄 요약

- 오염 자산 관제, 안전 파이프라인 훈련, 트리거 평가기의 역공학 스캐닝 및 승격/복구 게이트 체계로 구축된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **트리거 연관(Trigger Association)**: 뉴럴 네트워크 레이어 내에서 입력 트리거 특징(Feature)과 특정 타깃 클래스를 강제로 맵핑 바인딩시키는 현상이다.
- **목표 행동(Target Class / Attack Action)**: 백도어 활성화 시 공격자가 출력시키고자 하는 비인가 정답 라벨 또는 시스템 명령이다.
- **정확도 판정(Standard Accuracy Evaluation)**: 일반 무해 데이터셋에 대한 모델의 보편적 정확도를 측정하는 1차 판정 단계이다.
- **ASR 판정(Attack Success Rate Evaluation)**: 트리거 패치를 주입한 적대적 시험 데이터셋에 대한 공격 성공 비율을 정밀 평가하는 2차 판정 단계이다.
- **오염 자산 학습 세트 반영(Poisoned Asset Ingestion)**: 오염된 트리거 이미지/텍스트가 미검증 수집 채널을 통과하는 단계이다.
- **트리거•목표 행동 연관 학습(Trigger-Action Association Training)**: 딥러닝 학습 시 트리거 특징과 공격 목표 클래스 간의 가중치 연관이 고착되는 단계이다.
- **정상•트리거 조건부 출력 생성(Conditional Response Generation)**: 일반 입력은 정상 응답, 트리거 주입 시 오판을 내보내는 바이패스 생성 단계이다.
- **정확도•ASR 판정(Accuracy & ASR Dual Gate Evaluation)**: Clean Accuracy와 ASR 지표를 2중 교차 검증하는 단계이다.
- **승격•차단 결정(Promotion & Quarantine Decision)**: 백도어 이상징후 시 배포를 차단하고 안전 버전으로 롤백 복구하는 최종 집행 단계이다.

</details>

```text
트리거·목표 행동 포함 자산
              |
              v
1. 오염 자산 학습 세트 반영
              |
              v
2. 트리거·목표 행동 연관 학습
              |
              v
3. 정상·트리거 조건부 출력 생성
              |
              v
4. 정확도·ASR 판정
              |
              v
5. 승격·차단 결정
              |
              v
       판정·복구 대상
```

### 동작 원리

1. **오염 자산 학습 세트 반영**: 트리거 표본의 학습 유입
2. **트리거·목표 행동 연관 학습**: 목표 클래스 연관 형성
3. **정상·트리거 조건부 출력 생성**: 입력별 정상·오판 분기
4. **정확도·ASR 판정**: 정상 성능과 공격 성공률 교차 평가
5. **승격·차단 결정**: 통과 모델 배포·의심 모델 격리

#### 한줄 요약

- 오염 주입, 가중치 트리거 연관 학습, 조건부 응답 분기, Accuracy/ASR 2중 판정 및 승격/차단 격리 단계로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **일반 데이터 오염(Generic Data Poisoning)**: 모델 전반의 가용성을 무력화하거나 특정 샘플의 오판을 도출하는 공격이다.
- **적대적 예제(Adversarial Example)**: 모델의 학습 가중치 변경 없이 추론 시점에 입력 데이터에 미세 노이즈를 섞어 착시를 유발하는 공격이다.

</details>

| AI 공격 기법 | 백도어 공격 (Backdoor Attack) | 일반 데이터 오염 (Data Poisoning) | 적대적 예제 (Adversarial Example) |
|:---|:---|:---|:---|
| 공격 시점 | 학습 단계 (Training Phase) | 학습 단계 (Training Phase) | 추론 단계 (Inference Phase) |
| 가중치 변경 여부 | 있음 (트리거-타깃 연관 가중치 형성) | 있음 (전체 결정 경계 변조) | 없음 (기존 학습 가중치 그대로 이용) |
| 발동 조건 | 특정 **트리거** 주입 시에만 조건부 발동 | 전반적 성능 하락 또는 특정 샘플 오판 | 최적화된 경사 노이즈 입력 제출 시 |
| 스텔스성 | 최고 (일반 테스트 시 100% 정상 작동) | 보통~높음 (오염 방식에 따름) | 보통 (노이즈 입력 자체의 정밀성 필요) |

#### 한줄 요약

- 백도어(학습 시 트리거 가중치 침투), 데이터 오염(학습 시 경계 변조), 적대적 예제(추론 시 미세 노이즈 입력)로 구별된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **AI 100-2e2025 (NIST AI 100-2e2025 Backdoor Attacks)**: 백도어 트로이목마 공격 및 방어 정량 지침을 수록한 NIST 표준이다.
- **클린 라벨 오염(Clean-label Backdoor Attack)**: 라벨을 바꾸지 않고 입력 피처 공간만을 지능적으로 왜곡하여 스텔스 백도어를 심는 고급 기법이다.
- **트리거 반전(Trigger Inversion / Neural Cleanse)**: 딥러닝 모델 역공학을 통해 최소 크기의 트리거 패치를 역으로 복원 탐지하는 정밀 분석 기법이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 백도어 트로이목마 위협 평가 부재 | **NIST AI 100-2e2025** 규격 도입 | 백도어 위협에 대한 전사적 정량 평가 지표 확립 |
| 일반 Accuracy 검사 시 스텔스 통과 | **ASR 판정** 및 **트리거 반전** | 잠재 백도어 트리거 패턴 탐지 |
| 클린 라벨 기반 스텔스 백도어 침투 | **클린 라벨 오염** 스캐닝 및 DVC 계보 보존 | 라벨 무변조 백도어 표본 추적·차단 |

#### 한줄 요약

- NIST AI 100-2e2025 지침 준수, ASR 정밀 평가, Neural Cleanse 트리거 반전 및 DVC 이력 관리 체계를 적용한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **백도어 승격 기준(Backdoor Promotion Criteria)**: 일반 Clean Accuracy 성능을 보장함과 동시에 ASR 수치가 0%에 수렴하는 검증된 모델만 배포 승인하는 보안 게이트 지침이다.

</details>

- **백도어 승격 기준**에 따라 Neural Cleanse 및 ASR 검증을 통과한 안전한 모델만을 운영 서비스에 배포 집행한다.

#### 한줄 요약

- NIST AI 규격 준수, ASR 및 Neural Cleanse 트리거 반전 검증, DVC 버전 롤백 및 백도어 승격 기준 중심 방어 체계 구축 필수.
