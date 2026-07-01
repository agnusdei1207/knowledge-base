---
title: "적대적 예제 (Adversarial Example)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 194
---

# 📖 【암기용】 개념 완전 이해

> 목적: Adversarial Example을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 사람에게는 거의 변화가 없어 보이지만 AI 모델에는 오분류를 유발하는 의도적 입력 변조 사례
- **왜 필요한가**: 이미지·음성·센서 AI는 작은 교란에도 판단 경계가 흔들릴 수 있어 안전 시스템 위험이 발생함.
- **핵심 직관**: 사람 눈에는 같은 표지판인데 AI에게만 다른 표지판처럼 보이게 만드는 입력 조작임.

## 깊이 이해
- **배경·문제의식**: 딥러닝 모델은 고차원 입력 공간에서 사람이 직관하지 못하는 결정 경계 취약점을 가질 수 있다.
- **작동 원리**: FGSM, PGD 등은 loss를 키우는 방향으로 입력 픽셀·음성 신호·센서값을 작은 크기로 조정해 오분류를 유도함.
- **비유**: 사람은 알아채지 못하는 얇은 필터를 사진에 씌워 기계 판독기만 잘못 읽게 하는 방식임.
- **구체 예시**: 제한속도 표지 이미지에 L∞ 8/255 수준의 교란을 추가해 분류 모델이 다른 표지로 예측하게 함.
- **흔한 오해·주의점**: 노이즈 제거만으로 충분하지 않다. adversarial training, 입력 검증, 모델 앙상블, 운영 감시가 필요함.

## 연결 개념
- Robust AI — 교란에 견디는 모델 설계
- Backdoor Attack — 특정 트리거 기반 조건부 오동작
- AI Safety — 안전 중요 시스템의 검증 기준

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Adversarial Example은 사람이 알아채기 어려운 입력 교란으로 AI 오분류를 유도하는 공격임.
> 2. **가치**: 자율주행, 생체인증, 의료영상 등 안전 중요 AI의 신뢰성과 보안성을 훼손함.
> 3. **판단 포인트**: clean accuracy와 robust accuracy를 분리 측정하고 교란 예산 기준을 정의해야 함.

## Ⅰ. 개요 및 필요성

Adversarial Example은 적대적 입력 변조다. AI 모델은 작은 입력 변화에도 잘못된 예측을 낼 수 있다. 안전 중요 분야는 교란 공격에 대한 강건성 검증이 필요하다.

## Ⅱ. 구조 및 구성요소

```text
Clean Input → Perturbation Generator → Adversarial Input
  → Model Misclassification → Robustness Defense
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Clean Input | 원본 이미지·음성·센서 | 사람이 정상 인지 |
| Perturbation | 작은 교란 생성 | FGSM, PGD |
| Target Model | 오분류 대상 | white/black-box |
| Defense | 강건학습·탐지 | robust accuracy |

> 요약: 적대적 예제는 원본 입력에 작은 교란을 더해 모델 결정 경계를 잘못 넘게 하는 구조임.

## Ⅲ. 동작원리 및 흐름도

```text
모델·목표 선택 → loss 기반 교란 계산 → 입력 변조
  → 오분류 확인 → 방어 학습
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공격 모델과 목표 클래스 정의 | white/black-box 구분 |
| 2 | FGSM/PGD로 교란 생성 | ε=8/255 등 |
| 3 | 오분류율·robust accuracy 측정 | 공격별 ASR |
| 4 | adversarial training 적용 | robust accuracy 목표 |

> 요약: Adversarial Example 검증은 교란 예산을 정하고 공격별 오분류율과 방어 후 강건성을 측정함.

## Ⅳ. 특징

| 구분 | 자연 노이즈 | Adversarial Example | 판단 포인트 |
|:---|:---|:---|:---|
| 원인 | 센서·환경 잡음 | 공격자 의도 교란 | 보안 위협 |
| 크기 | 무작위 변화 | loss 증가 방향 최적화 | 작은 ε |
| 영향 | 일부 품질 저하 | 표적 오분류 가능 | 안전 위험 |
| 방어 | 전처리·필터 | 강건학습·탐지·앙상블 | robust accuracy |

> 요약: 적대적 예제는 무작위 노이즈가 아니라 모델 약점을 겨냥한 최적화 입력이므로 강건성 검증이 필요함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 평가 체계: clean accuracy와 FGSM/PGD 공격별 robust accuracy를 분리 보고하고 ε 기준을 명시
2. 학습 방어: adversarial training, data augmentation, confidence calibration을 적용하고 ASR 감소량 측정
3. 운영 보호: 입력 이상탐지, 센서 다중화, human override를 적용해 안전 중요 결정은 단일 모델 판단 금지

**결론 (2줄):**
- 기술사 판단: 안전 중요 AI는 clean accuracy만으로 승인하지 말고 공격별 robust accuracy를 필수 지표로 적용
- 향후 방향: Adversarial Example 대응은 Robust AI, 형식 검증, 운영 모니터링과 결합됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Adversarial Example을 설명하시오" | 교란 생성→오분류 흐름 | 자연 노이즈 대비 차이 |
| 요구사항 명시형 | "AI 강건성 확보 방안을 제시하시오" | 공격별 robust accuracy 평가 | 강건학습·운영 보호 |

> 요약: 설명형은 입력 교란 원리, 방안형은 강건성 평가와 안전 운영 기준을 중심으로 작성함.
