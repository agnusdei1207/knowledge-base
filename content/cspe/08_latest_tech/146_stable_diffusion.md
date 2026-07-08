---
title: "Stable Diffusion (Stable Diffusion)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 146
extra:
  question_no: "146"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Stable Diffusion은 latent diffusion 기반의 대표 오픈소스 이미지 생성 모델임
- VAE와 text encoder와 latent U-Net이 핵심 구조를 이룸
- LoRA와 ControlNet 생태계 덕분에 커스터마이징 확장성이 큼

## Ⅰ. 개요

- **정의/개념**: Stable Diffusion은 텍스트 프롬프트를 조건으로 사용하면서 픽셀 공간이 아닌 잠재 공간에서 확산 복원을 수행해, 일반 GPU 환경에서도 고품질 이미지를 생성할 수 있게 한 오픈소스 기반 Text-to-Image 파운데이션 모델임
- **배경/필요성**: 초기 고성능 생성 모델은 대규모 폐쇄형 인프라에 묶여 접근성이 낮았으므로, 비용을 낮추면서도 실무 커스터마이징이 가능한 개방형 생성 모델이 필요했음

## Ⅱ. 특징

- latent diffusion 덕분에 픽셀 기반 확산보다 연산 비용이 크게 낮음
- 오픈 생태계가 커서 LoRA와 ControlNet과 각종 최적화 도구를 쉽게 결합할 수 있음
- 온프레미스 구축이 가능해 폐쇄망이나 사내 맞춤 생성에 유리함
- 학습 데이터와 라이선스 이슈를 관리하지 않으면 기업 도입 리스크가 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 폐쇄형 T2I API | Stable Diffusion | 사내 파인튜닝 SD |
|:---|:---|:---|:---|
| 제어 확장성 | 중간 | 높음 | 매우 높음 |
| 인프라 통제 | 낮음 | 높음 | 매우 높음 |
| 초기 구축 비용 | 낮음 | 중간 | 높음 |
| 보안 적합성 | 중간 | 높음 | 매우 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Text Encoder | 프롬프트를 조건 벡터로 변환해 생성 방향과 스타일을 지정함 |
| VAE | 픽셀 이미지를 잠재 공간으로 압축하고 완성된 잠재 표현을 다시 이미지로 복원함 |
| Latent U-Net | 잠재 공간에서 반복적으로 노이즈를 제거하며 주된 이미지 구조를 형성함 |
| Extension Layer | LoRA와 ControlNet과 sampler가 스타일 학습과 구도 제어와 속도 최적화를 담당함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Text Encoder      | ---> | Latent U-Net      | ---> | VAE Decoder       |
+-------------------+      +-------------------+      +-------------------+
                                   ^
                                   |
                           +-------------------+
                           | VAE / Extensions  |
                           +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 프롬프트 입력   | --> | 잠재 노이즈 준비 | --> | 잠재 복원 반복  | --> | 이미지 디코딩   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **프롬프트 입력**: 텍스트 조건과 부가 제어 정보를 받음
2. **잠재 노이즈 준비**: 생성 시작점이 되는 latent noise를 초기화함
3. **잠재 복원 반복**: U-Net이 조건을 반영해 반복 denoising을 수행함
4. **이미지 디코딩**: 완성된 latent를 VAE decoder가 픽셀 이미지로 복원함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 학습 데이터 출처와 버전별 라이선스 조건이 불명확하면 생성 품질과 무관하게 기업 적용 승인이 지연될 수 있음
   - 해결방안: 승인된 체크포인트와 provenance 관리 체계를 적용하고 compliance pass rate와 legal review lead time으로 검증함
2. 문제: 고해상도 생성과 대량 배치는 GPU 메모리와 추론 시간이 커서 운영 비용이 급증할 수 있음
   - 해결방안: xFormers와 quantization과 TensorRT 최적화를 적용하고 latency와 GPU utilization로 검증함
3. 문제: 프롬프트만으로는 캐릭터 일관성과 구도 재현이 흔들려 반복 수정 비용이 커질 수 있음
   - 해결방안: LoRA와 ControlNet과 reference workflow를 적용하고 character consistency score와 revision count로 검증함

## Ⅶ. 적용 사례

- 웹툰 제작이 배경과 콘셉트 시안을 빠르게 반복 생성하도록 Stable Diffusion을 적용하며 확인 지표는 art throughput과 revision count임
- 제조 비전 학습이 결함 이미지를 사내망에서 합성하도록 Stable Diffusion을 운영하며 확인 지표는 synthetic coverage와 downstream accuracy gain임
- 금융권 폐쇄망 마케팅이 외부 유출 없이 배너 시안을 생성하도록 Stable Diffusion을 활용하며 확인 지표는 compliance pass rate와 design cycle time임

## Ⅷ. 결론

Stable Diffusion은 생성 AI를 개방형 인프라로 끌어내린 대표 모델이므로, 실무에서는 오픈 생태계의 유연성과 라이선스·보안 통제를 함께 설계해야 안정적으로 가치가 커짐.
