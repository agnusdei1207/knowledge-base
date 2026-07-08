---
title: "AI Accelerator AI 가속기 (AI Accelerator)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 235
extra:
  question_no: "235"
  exam_status: "기출"
  exam_history: "126회, 134회, 136회, 137회"
  exam_note: "전망"
---

## 미리 알고가기

- AI 가속기는 행렬 연산과 텐서 연산을 빠르고 효율적으로 처리하도록 설계된 전용 하드웨어를 통칭함
- GPU와 TPU와 NPU와 ASIC과 FPGA가 모두 범주 안에 들어갈 수 있으나 범용성은 서로 다름
- 연산 성능만큼 메모리 대역폭과 소프트웨어 생태계가 실제 경쟁력을 결정함

## Ⅰ. 개요

- **정의/개념**: AI Accelerator는 딥러닝과 기계학습의 대량 행렬 곱과 벡터 연산을 CPU보다 높은 병렬성과 전력 효율로 수행하도록 최적화된 특수 목적 프로세서 계열임
- **배경/필요성**: 대규모 AI 모델의 학습과 추론 요구가 급증하면서 범용 CPU만으로는 처리 속도와 전력 효율을 맞추기 어려워 전용 가속기 아키텍처가 필수화됨

## Ⅱ. 특징

- MAC 연산과 텐서 처리에 특화되어 높은 병렬 처리량을 제공함
- 메모리 이동 비용이 큰 AI 워크로드에서 온칩 메모리와 HBM 설계가 중요함
- 가속기 종류에 따라 범용성과 전력 효율과 개발 난이도가 다름
- 컴파일러와 런타임과 프레임워크 지원이 실제 도입 난이도를 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | GPU | TPU or ASIC | FPGA |
|:---|:---|:---|:---|
| 범용성 | 높음 | 낮거나 중간 | 중간 |
| 성능 효율 | 높음 | 매우 높음 | 특정 워크로드 우수 |
| 개발 난이도 | 상대적으로 낮음 | 중간 | 높음 |
| 대표 용도 | 학습과 추론 범용 | 대규모 학습, 대량 추론 | 맞춤 추론, 저지연 전처리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Compute Array | 다수의 MAC이나 tensor core가 병렬로 연산해 AI 처리량을 높이는 핵심 연산 블록임 |
| On Chip Memory | 레지스터와 SRAM 같은 내부 메모리가 데이터 재사용을 높여 외부 메모리 병목을 줄이는 저장 계층임 |
| External Memory Interface | HBM이나 GDDR과 연결되어 대량 파라미터와 activation을 빠르게 공급하는 대역폭 경로임 |
| Compiler and Runtime | 모델 그래프를 가속기 명령으로 변환하고 최적 실행 경로를 만드는 소프트웨어 계층임 |
| Power and Thermal Control | 높은 연산 밀도에서 전력 효율과 열 안정성을 유지하는 제어 계층임 |

```text
+---------------+    +----------------+    +-------------------+
| Compute Array |<-> | On Chip Memory |<-> | External Memory   |
+---------------+    +----------------+    +-------------------+
         |
         v
 +----------------+    +----------------+
 | Compiler/RT    |    | Power/Thermal  |
 +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 모델 그래프 변환 | -> | 데이터 적재  | -> | 병렬 연산    | -> | 결과 출력    | -> | 전력 최적화  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **모델 그래프 변환**: 프레임워크 모델을 가속기 실행 그래프로 변환함
2. **데이터 적재**: 파라미터와 입력을 온칩과 외부 메모리에 적재함
3. **병렬 연산 수행**: 대량 행렬과 텐서 연산을 병렬 처리함
4. **결과 출력**: 추론 결과나 gradient를 상위 시스템으로 반환함
5. **전력 최적화**: 부하에 따라 전력과 클럭과 열을 제어함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 연산 성능이 높아도 메모리 대역폭이 부족하면 가속기가 데이터를 기다리느라 유휴 상태가 커질 수 있음
   - 해결방안: HBM adoption과 data reuse optimization을 적용하고 memory stall ratio와 effective throughput으로 검증함
2. 문제: 전용 하드웨어일수록 소프트웨어 이식성이 낮아 특정 프레임워크와 벤더에 종속될 수 있음
   - 해결방안: standard compiler interface와 model portability test를 적용하고 framework portability score와 migration effort index로 검증함
3. 문제: 높은 전력 밀도와 발열은 대규모 배치 시 성능 저하와 운영 비용 상승을 유발할 수 있음
   - 해결방안: thermal aware placement와 power efficiency tuning을 적용하고 performance per watt와 thermal throttling rate로 검증함

## Ⅶ. 적용 사례

- AI 추론 서버가 HBM 기반 가속기를 채택하며 확인 지표는 memory stall ratio와 effective throughput임
- 멀티벤더 환경이 모델 이식성 검증을 운영하며 확인 지표는 framework portability score와 migration effort index임
- 데이터센터가 전력 효율 중심 가속기 배치를 적용하며 확인 지표는 performance per watt와 thermal throttling rate임

## Ⅷ. 결론

AI 가속기는 연산 코어 수만이 아니라 메모리와 소프트웨어와 전력 효율까지 함께 설계될 때 실질 성능을 발휘함.
