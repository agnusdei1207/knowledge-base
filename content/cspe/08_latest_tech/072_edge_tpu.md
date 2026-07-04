---
title: "Edge TPU (Edge TPU)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 72
---

# 📖 【암기용】 개념 완전 이해

> 목적: Edge TPU를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 엣지 장치에서 TensorFlow Lite 모델을 저전력으로 실행하는 Google 계열 AI 가속기
- **왜 필요한가**: 카메라·센서 현장 추론은 클라우드 왕복 없이 수십ms 안에 판단해야 함.
- **핵심 직관**: 작은 엣지 장비에 붙는 AI 전용 칩으로, 이미지 분류·객체 탐지를 현장에서 처리함.

## 깊이 이해
- **배경·문제의식**: Raspberry Pi 같은 범용 보드는 CNN 추론을 CPU로 처리하면 FPS와 전력에서 한계가 큼. Edge TPU는 INT8 모델을 전용 가속해 현장 분석을 가능하게 함.
- **작동 원리**: TensorFlow Lite 모델을 Edge TPU Compiler로 변환하고, 지원 operator를 TPU에 배치함. 미지원 연산은 CPU fallback이 발생해 지연이 증가함.
- **비유**: 소형 매장에 CCTV 분석 전담 직원을 둬 중앙 서버에 영상을 보내지 않고 현장에서 이벤트만 판단하는 것과 같음.
- **구체 예시**: USB/PCIe/M.2 Edge TPU는 INT8 CNN 모델을 대상으로 객체 탐지·분류·키워드 감지에 활용됨.
- **흔한 오해·주의점**: Edge TPU는 범용 LLM 실행 장치가 아님. 지원 연산과 INT8 양자화 조건에 맞는 모델에서 효과가 큼.

## 연결 개념
- Edge AI — Edge TPU 적용 아키텍처
- Quantization — INT8 모델 변환 필수
- NPU — AI 전용 가속기의 상위 범주

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Edge TPU는 엣지 장치에서 INT8 TFLite 모델 추론을 가속하는 저전력 AI 프로세서임.
> 2. **가치**: 영상·센서 데이터를 현장에서 처리해 지연·대역폭·클라우드 비용을 줄임.
> 3. **판단 포인트**: INT8 양자화, compiler 지원 op, CPU fallback, thermal budget을 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 엣지 AI 가속기의 구조·적용 판단 | INT8 양자화, compiler op 지원, CPU fallback, 현장 지연 기준 | Edge TPU를 범용 LLM 가속기로 혼동, 지원 op 제한 미언급 |

> 요약: Edge TPU는 INT8 비전 모델 현장 추론에 특화되며, compiler 호환성과 fallback 관리가 핵심 평가 축임.

---

## Ⅰ. 개요 및 필요성

- 정의: 엣지 장치에서 INT8 TFLite 모델 추론을 가속하는 Google 계열 저전력 AI 프로세서
- 배경: 현장 CCTV·센서 분석은 클라우드 왕복 지연과 데이터 전송 비용이 제약임
- 필요성: 단말 근처에서 저전력 INT8 추론을 수행해 지연·대역폭·클라우드 비용을 줄여야 함

## Ⅱ. 구조 및 구성요소

```text
TFLite Model -> Edge TPU Compiler -> INT8 Model
      -> Edge TPU Runtime -> USB/PCIe/M.2 TPU -> Inference
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| TFLite Model | 엣지 배포 모델 | CNN·MobileNet 계열 |
| Compiler | TPU 지원 graph로 변환 | 미지원 op 확인 |
| Edge TPU Runtime | 추론 실행 | CPU fallback 가능 |
| Host Device | 센서·I/O·후처리 담당 | Raspberry Pi, IPC |

> 요약: Edge TPU는 TFLite 모델을 compiler로 변환하고, 지원 연산을 전용 칩에서 실행하는 구조임.

## Ⅲ. 동작원리 및 흐름도

```text
모델 양자화 -> Compiler 변환 -> 엣지 장치 배포
    -> 입력 전처리 -> TPU 추론 -> 이벤트 출력
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 모델 INT8 양자화 | 정확도 하락 1~3%p 이내 |
| 2 | Edge TPU Compiler 변환 | supported op 비율 |
| 3 | 현장 장치 추론 | FPS, p95 latency |
| 4 | 이벤트 필터링·전송 | false positive, bandwidth |

> 요약: Edge TPU 적용은 모델 변환 가능성과 현장 지연·정확도 검증이 핵심임.

## Ⅳ. 특징

| 구분 | CPU 엣지 추론 | Edge TPU | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 연산 | 범용 처리 | INT8 AI 가속 | TOPS/W 기준 |
| 모델 | 범용 op 가능 | 지원 op 제한 | compiler report 확인 |
| 지연 | FPS 제한 | 실시간 영상 처리 | 카메라 30 FPS 목표 |
| 한계 | 전력 증가 | LLM·미지원 op 취약 | CPU fallback 관리 |

> 요약: Edge TPU는 INT8 비전 모델의 현장 추론에 적합하나, 모델 호환성 검증이 선행되어야 함.

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | CPU 엣지 추론 | Edge TPU | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 범용 ISA, 모든 op 실행 | INT8 전용 MAC, 지원 op 한정 | 모델 op coverage 기준 |
| 비용/성능 | FPS 제한, 전력 증가 | 4 TOPS/W, 30 FPS 비전 모델 | 카메라 실시간 기준 |
| 운영/위험 | fallback 불필요 | compiler 미지원 시 CPU fallback | op 지원 비율 95% 이상 |

> 요약: 지원 모델 범위 안에서는 Edge TPU가 전력·FPS 우위, 범위 밖은 CPU·GPU로 처리함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 모델 비호환 | compiler 미지원 op | 모델 구조를 MobileNet 계열로 제한 | compiler report op 비율 |
| 정확도 열화 | INT8 양자화 손실 | representative dataset 1K장 캘리브레이션 | mAP 하락 2%p 이내 |
| 현장 장애 | 발열·네트워크 단절 | 온도 센서 + store-and-forward 구성 | 장비 가동률 99% 이상 |

> 요약: Edge TPU 리스크는 모델 호환·양자화 회귀·현장 환경이며, 배포 전 검증으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/효율 | 30 FPS, p95 latency 50ms 이내 | 현장 프레임 벤치마크 |
| 품질/정확도 | INT8 mAP 하락 2%p 이내 | validation set 비교 |
| 운영/보안 | OTA 모델 업데이트, 장비 가동률 99% | 배포 로그, 모니터링 대시보드 |

> 요약: Edge TPU 도입 성공은 현장 FPS·정확도·장비 가동률을 실측해 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. CCTV 객체 탐지는 MobileNet/SSD INT8 모델로 변환하고 30 FPS, p95 50ms 이하 기준을 검증
2. compiler report에서 TPU 배치 op 비율 95% 이상을 확인하고 CPU fallback 경로를 별도 측정
3. 현장 장비는 OTA 모델 업데이트, 온도 센서, 장애 시 로컬 저장 후 전송(store-and-forward)을 구성

**결론 (2줄):**
- 기술사 판단: 비전·센서 INT8 추론은 Edge TPU, 범용 생성형 AI는 GPU/NPU/클라우드 LLM을 선택함.
- 향후 방향: Edge TPU 계열은 현장 비전 AI와 IoT 이벤트 처리의 저전력 가속기로 지속 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 양자화·compiler·배포 흐름 | CPU 대비 특징 |
| 요구사항 명시형 | 설계하시오, 적용 방안을 제시하시오 | op 지원·FPS 검증 절차 | 지연·전력·fallback 기준 |

> 요약: 설명형은 Edge TPU 변환 구조, 설계형은 현장 지연과 모델 호환성 기준으로 목차를 전환함.
