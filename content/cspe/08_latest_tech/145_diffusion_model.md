---
title: "확산모델 (Diffusion Model)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 145
---

# 📖 【암기용】 개념 완전 이해

> 목적: Diffusion Model을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 데이터에 노이즈를 점진적으로 추가한 뒤, 그 노이즈를 제거하는 과정을 학습해 새 데이터를 생성하는 모델
- **왜 필요한가**: 이미지·영상·음성 생성에서 품질과 다양성을 확보하며 텍스트 조건 제어가 가능함.
- **핵심 직관**: 흐릿한 잡음 그림에서 시작해 여러 번 지우고 다듬어 선명한 이미지를 복원하는 방식임.

## 깊이 이해
- **배경·문제의식**: GAN은 고품질 이미지를 만들 수 있지만 학습 불안정과 mode collapse 문제가 있었다. 확산모델은 likelihood 기반 학습과 안정적 생성으로 대안이 됨.
- **작동 원리**: Forward process에서 원본에 Gaussian noise를 단계적으로 더하고, Reverse process에서 U-Net이 각 단계의 noise를 예측해 제거함.
- **비유**: 깨끗한 사진에 먼지를 조금씩 뿌리는 과정을 배운 뒤, 먼지 낀 사진을 단계별로 닦아 원본 같은 이미지를 만드는 것임.
- **구체 예시**: 50 denoising step으로 512×512 이미지를 생성하며, classifier-free guidance scale 7~12로 프롬프트 반영 강도를 조정.
- **흔한 오해·주의점**: 확산모델은 품질이 높지만 반복 denoising 때문에 지연이 크다. latent diffusion, distillation, fewer-step sampler로 최적화함.

## 연결 개념
- Stable Diffusion — latent space에서 동작하는 대표 확산모델
- Latent Diffusion — 픽셀 대신 잠재공간에서 확산을 수행하는 방식
- Denoising U-Net — 노이즈 제거를 예측하는 핵심 신경망

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Diffusion Model은 노이즈 추가와 제거 과정을 학습해 데이터를 생성하는 확률 생성모델임.
> 2. **가치**: 이미지·영상·음성에서 고품질 생성과 텍스트 조건 제어를 제공함.
> 3. **판단 포인트**: 생성 품질과 denoising 지연의 트레이드오프를 sampler·latent·distillation으로 조정함.

## Ⅰ. 개요 및 필요성

- 개요: 노이즈 제거 기반 생성모델
- 배경: GAN은 mode collapse와 학습 불안정 문제가 있어 조건부 생성 품질을 일관되게 재현하기 어렵다.
- 필요성: forward noise와 reverse denoising을 학습해 FID, CLIP score, sampling steps 기준으로 생성 품질을 검증한다.

## Ⅱ. 구조 및 구성요소

```text
Clean Data x0 -> Forward Noise q(xt|x0) -> Noisy xt
Noisy xt + Condition -> Denoising U-Net -> x(t-1) -> Generated Data
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Forward Process | 원본에 단계별 Gaussian noise 추가 | T=1,000 학습 step |
| Denoising Network | noise 또는 clean sample 예측 | U-Net, Transformer |
| Sampler | 역확산 추론 step 제어 | DDPM, DDIM, DPM-Solver |
| Conditioning | 텍스트·이미지 조건 반영 | cross-attention, CFG |

> 요약: 확산모델은 노이즈를 추가하는 정방향 과정과 노이즈를 제거하는 역방향 과정을 학습해 데이터를 생성함.

## Ⅲ. 동작원리 및 흐름도

```text
학습: 원본 -> 노이즈 추가 -> noise 예측 손실 최소화
추론: 순수 노이즈 -> 반복 denoising -> 조건 반영 이미지 생성
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 원본 데이터에 timestep별 noise 추가 | noise schedule 정의 |
| 2 | 모델이 noise ε를 예측하도록 학습 | loss MSE 감소 |
| 3 | 추론 시 random noise에서 역확산 수행 | 20~50 inference steps |
| 4 | 텍스트 조건·안전 필터 적용 | FID감소, CLIP score증가 |

> 요약: 학습 때 노이즈 예측 능력을 익히고, 추론 때 노이즈에서 시작해 단계적으로 샘플을 복원함.

## Ⅳ. 특징

| 구분 | GAN | Diffusion Model | 판단 포인트 |
|:---|:---|:---|:---|
| 학습 안정성 | mode collapse 가능 | MSE 기반 안정 학습 | 대규모 생성에 적합 |
| 생성 품질 | 고품질 가능 | 고품질·다양성 | 이미지 생성 표준 |
| 추론 속도 | 1회 forward | 20~50 step 반복 | 지연 최적화 필요 |
| 조건 제어 | 구조별 상이 | text/image guidance | 프롬프트 제어 강점 |

> 요약: Diffusion Model은 품질과 안정성이 강점이지만 반복 denoising으로 인한 지연을 최적화해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 이미지 생성: Stable Diffusion 기반 Text-to-Image, CFG 7~12, 30 step 기준으로 품질·지연 균형 설정
2. 합성 데이터: 결함·의료 이미지 생성 후 FID, downstream accuracy, privacy leakage 테스트 수행
3. 추론 최적화: latent diffusion, DPM-Solver, distillation으로 50 step->10 step 단축 목표

**결론 (2줄):**
- 기술사 판단: 고품질 조건부 이미지·영상 생성은 Diffusion, 초저지연 단순 생성은 경량 GAN/Transformer 검토
- 향후 방향: latent diffusion, video diffusion, consistency model로 생성 속도와 제어성이 개선됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Diffusion Model을 설명하시오" | forward noise->reverse denoising 흐름 | GAN 대비 차이 |
| 요구사항 명시형 | "이미지 생성 모델 적용 방안을 제시하시오" | sampler·CFG·안전 필터 기준 | 품질·지연·권리 리스크 |

> 요약: 설명형은 확산 생성 원리, 방안형은 품질·지연 최적화와 안전 통제를 중심으로 작성함.
