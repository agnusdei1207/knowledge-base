---
title: "Edge TPU (Edge TPU)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 54
---

## Ⅰ. 개요
- **정의**: 엣지 디바이스에서 TensorFlow Lite 모델의 저전력 추론을 수행하는 Google의 소형 ASIC
- **배경/필요성**: 클라우드 TPU(052 참조)는 데이터센터 전용이므로, IoT·임베디드 환경에서 동일한 추론 효율을 달성할 소형 가속기가 필요함
- **비유**: 클라우드 TPU가 대형 공장이라면, Edge TPU는 현장에 배치된 소형 조립 키트임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 엣지 AI 전용 ASIC 구조 이해 | INT8 양자화 모델 전용, 2W 이하 전력 | 클라우드 TPU와의 아키텍처·용도 차이를 혼동하지 않을 것 |

> 요약: TFLite INT8 모델을 2W 이하로 추론하는 엣지 전용 소형 ASIC임

## Ⅱ. 구성요소
```text
Edge TPU Module
  |
  +-- Edge TPU ASIC
  |     |
  |     +-- INT8 MAC Array
  |     |
  |     +-- On-chip SRAM (2~4MB)
  |     |
  |     +-- DMA Engine
  |
  +-- Host Interface (USB / PCIe / SPI)
  |
  +-- External DRAM (optional)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| INT8 MAC Array | 8비트 정수 곱셈-누적 연산을 병렬 수행하는 핵심 연산 유닛 | 간이 계산기 수백 대 |
| On-chip SRAM | 가중치·중간 텐서를 저장하는 2~4MB 온칩 버퍼 | 작업대 위 소형 선반 |
| DMA Engine | Host-SRAM 간 데이터 전송을 CPU 개입 없이 수행함 | 자동 택배 시스템 |
| Host Interface | USB, PCIe, SPI 등 호스트 프로세서와 연결하는 물리 인터페이스 | 공장-본사 연결 도로 |

> 요약: INT8 MAC Array와 소형 SRAM으로 구성된 저전력 추론 전용 칩임

## Ⅲ. 절차
```text
TFLite 모델 --> INT8 양자화 --> Edge TPU 컴파일 --> 추론 실행
      |              |                |                  |
      v              v                v                  v
  모델 학습     양자화 변환      edgetpu_compiler     SRAM 적재/MAC 연산
```
- 1단계: TensorFlow로 모델을 학습하고 TensorFlow Lite 포맷으로 변환함
- 2단계: 전체 후 양자화(Post-Training Quantization)로 FP32를 INT8로 변환함
- 3단계: Edge TPU Compiler가 INT8 모델을 칩 실행 가능 바이너리로 컴파일함
- 4단계: 런타임이 가중치를 SRAM에 적재하고 MAC Array가 레이어별 추론을 수행함

> 요약: TFLite 모델을 INT8 양자화 후 전용 컴파일러로 변환하여 칩에서 추론함

## Ⅳ. 문제점
- 모델 제약: INT8 양자화된 TFLite 모델만 지원하여 FP16·동적 양자화 모델은 실행 불가함
- SRAM 용량 한계: 2~4MB 온칩 메모리로 대형 모델의 가중치를 적재할 수 없어 외부 DRAM 폴백 시 성능이 저하됨
- 생태계 한정: Google Coral 플랫폼 중심이어서 타사 보드·프레임워크 통합이 제한적임

> 요약: 모델 포맷 제약, SRAM 용량 한계, 제한된 생태계가 주요 문제임

## Ⅴ. 개선방안
1. 단기: ONNX-to-TFLite 변환 파이프라인을 구축하여 모델 포맷 제약을 우회함
2. 중기: 차세대 Edge TPU에서 온칩 SRAM 용량을 확대하고 모델 분할 전략을 적용함
3. 장기: 멀티 프레임워크 런타임을 지원하여 Coral 외 생태계와의 호환성을 확보함

> 요약: 변환 파이프라인 구축, SRAM 확대, 생태계 개방으로 단계적 개선이 필요함

## Ⅵ. 전망
- 발전 방향: 엣지 AI 추론 수요 증가로 Edge TPU급 저전력 ASIC 시장이 확대됨
- 기술사적 판단: NPU(053 참조) 내장 SoC와 경쟁하며 외장 가속기와 내장 NPU의 역할이 분화될 전망임
- 기술사 제언: 전력 예산과 모델 크기를 기준으로 Edge TPU·NPU·GPU 중 적합한 가속기를 선정해야 함
