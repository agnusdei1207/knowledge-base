---
title: "FlashAttention (플래시어텐션)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 59
extra:
  question_no: "059"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- HBM은 용량은 크지만 지연과 대역폭 병목이 있는 GPU 외부 메모리 계층임
- SRAM은 GPU 내부의 빠른 온칩 메모리로 작은 작업 조각을 빠르게 처리하는 데 유리함
- Kernel Fusion은 여러 연산 단계를 하나의 커널로 합쳐 중간 메모리 입출력을 줄이는 최적화 방식임

## Ⅰ. 개요

- **정의/개념**: FlashAttention은 attention 연산을 타일 단위로 분할하고 Softmax와 가중합을 fused kernel 안에서 처리해 HBM 입출력을 줄임으로써 속도와 메모리 효율을 높이는 IO-aware attention 최적화 기법임
- **배경/필요성**: 기존 attention은 수식 자체보다 중간 텐서를 HBM에 반복 저장하고 다시 읽는 비용이 더 큰 병목이므로, 긴 문맥에서 메모리 입출력을 줄이는 커널 수준 최적화가 필요함

## Ⅱ. 특징

- attention 수식을 바꾸지 않으면서도 실제 GPU 실행 시간을 크게 줄일 수 있음
- 타일링과 커널 융합으로 HBM 왕복을 줄여 긴 컨텍스트에서 특히 효과가 큼
- 학습과 추론 양쪽에서 메모리 사용량과 속도를 동시에 개선함
- 특정 GPU 아키텍처와 커널 구현에 성능이 크게 좌우되는 하드웨어 친화적 기술임

## Ⅲ. 종류 및 비교

| 판단 기준 | 기본 Attention 커널 | FlashAttention | Sparse, Linear Attention |
|:---|:---|:---|:---|
| 수식 변경 | 없음 | 없음 | 있음 |
| 메모리 IO | 큼 | 작음 | 더 작을 수 있음 |
| 정확도 | 기준선 | 동일 | 구조에 따라 차이 |
| 적용 목적 | 기본 구현 | 고속, 고효율 구현 | 초장문 확장 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Tiling Strategy | Q, K, V를 SRAM에 들어갈 작은 블록으로 나눠 메모리 이동량을 통제함 |
| Fused Attention Kernel | 내적, 정규화, 가중합을 한 커널 안에서 처리해 중간 결과 저장을 최소화함 |
| On-chip Accumulator | 중간 누적값을 SRAM, 레지스터에 유지해 HBM 재접근을 줄임 |
| Hardware-aware Scheduler | GPU 아키텍처에 맞춰 타일 크기와 병렬 실행 방식을 조정함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 타일 분할    | --> | 온칩 적재    | --> | fused 연산   | --> | 결과 기록    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **타일 분할**: 큰 Q, K, V 행렬을 GPU 온칩 메모리에 맞는 타일로 나눔
2. **온칩 적재**: 필요한 타일만 SRAM에 올려 중간 작업 공간으로 사용함
3. **fused 연산 수행**: 내적과 Softmax와 Value 가중합을 한 커널 안에서 이어서 계산함
4. **결과 기록**: 최종 출력만 HBM에 기록하고 중간 텐서 저장은 최소화함

## Ⅵ. 문제점 및 해결 방안

1. 문제: GPU 아키텍처와 커널 버전에 따라 성능 편차가 커 적합하지 않은 환경에서는 기대한 가속 효과가 작을 수 있음
   - 해결방안: 하드웨어별 커널 버전을 벤치마크하고 tokens/sec와 GPU utilization로 최적 커널을 검증함
2. 문제: 긴 문맥에서 메모리 IO는 줄어도 attention 자체의 $O(N^2)$ 연산 특성은 남아 있어 초장문에서는 구조적 한계가 지속됨
   - 해결방안: FlashAttention을 기본으로 두고 sparse, linear attention 계열과 병행 검토하며 long-context latency와 memory footprint로 한계를 검증함
3. 문제: 커널 통합과 recomputation 로직이 복잡해 학습 디버깅과 유지보수 난도가 높아질 수 있음
   - 해결방안: 참조 구현과 회귀 테스트를 유지하고 numerical stability와 training loss divergence로 안정성을 검증함

## Ⅶ. 적용 사례

- LLM 학습: 긴 시퀀스 배치에서 메모리 사용량을 줄임, 확인 지표는 max sequence length와 training throughput임
- 추론 서버: 긴 프롬프트의 prefill 성능을 높임, 확인 지표는 TTFT와 HBM bandwidth utilization임
- 멀티모달 모델: 이미지 패치나 장문맥 텍스트 attention을 가속함, 확인 지표는 latency와 memory footprint임

## Ⅷ. 결론

FlashAttention의 핵심은 attention 공식을 바꾸는 것이 아니라 메모리 이동을 연산만큼 중요하게 보고 GPU 물리 병목을 줄여 실제 체감 성능을 높이는 데 있음.
