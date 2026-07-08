---
title: "LoRA 저랭크 적응 (Low-Rank Adaptation)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 89
extra:
  question_no: "089"
  exam_status: "기출"
  exam_history: "131회, 132회, 135회, 136회"
---

## 미리 알고가기

- LoRA는 PEFT의 대표 방식으로, 기존 가중치 업데이트를 저랭크 행렬 두 개로 근사해 학습함
- base model은 고정하고 작은 적응 행렬만 학습해 메모리와 저장 비용을 줄임
- rank, target module, merge 전략이 성능과 운영성을 크게 좌우함

## Ⅰ. 개요

- **정의/개념**: LoRA는 대형 모델의 선형 계층에 저랭크 보정 행렬을 추가해 원래 가중치 전체를 갱신하지 않고도 도메인 적응을 수행하는 PEFT 기법임
- **배경/필요성**: full fine-tuning은 비용이 크고 adapter는 추론 오버헤드가 늘 수 있으므로, 학습은 가볍고 추론 시에는 base weight와 결합 가능한 효율적 튜닝 방식이 필요함

## Ⅱ. 특징

- 학습 파라미터 수를 크게 줄이면서도 실무 도메인 적응 성능이 높음
- 학습 후 base weight에 merge하거나 분리 로딩할 수 있어 배포 유연성이 좋음
- rank가 너무 낮으면 표현력이 부족하고 너무 높으면 비용 이점이 약해질 수 있음
- 어느 계층에 LoRA를 적용하느냐에 따라 성능 편차가 크게 발생함

## Ⅲ. 종류 및 비교

| 판단 기준 | Full Fine-Tuning | Adapter Tuning | LoRA |
|:---|:---|:---|:---|
| 학습 파라미터 | 매우 많음 | 적음 | 적음 |
| 추론 오버헤드 | 없음 | 있을 수 있음 | 낮음 |
| 저장 비용 | 큼 | 낮음 | 낮음 |
| 실무 활용도 | 선택적 | 중간 | 매우 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Frozen Weight | 기반 모델의 원래 가중치로 범용 능력을 그대로 유지함 |
| Low-rank Matrices | 작은 rank의 두 행렬이 추가 변화량을 표현해 도메인 적응을 담당함 |
| Target Modules | attention과 projection 계층 중 어디에 LoRA를 삽입할지 결정해 효과와 비용을 좌우함 |
| Merge, Serving Policy | 학습 후 가중치를 병합하거나 분리 유지해 배포 방식과 전환 속도를 결정함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Frozen Weight     | ---> | Low-rank Matrix   | ---> | Target Modules    |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Merge / Serving   |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| base weight 고정 | --> | 저랭크 행렬 부착 | --> | 선택 계층 학습   | --> | 병합 또는 분리 배포 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **base weight 고정**: 원래 모델 가중치는 변경하지 않음
2. **저랭크 행렬 부착**: 대상 선형 계층에 작은 보정 행렬을 추가함
3. **선택 계층 학습**: 보정 행렬만 업데이트해 도메인 적응을 수행함
4. **병합 또는 분리 배포**: 추론 전략에 맞춰 weight merge나 adapter 로딩을 선택함

## Ⅵ. 문제점 및 해결 방안

1. 문제: rank를 너무 낮게 잡으면 복잡한 업무 패턴을 충분히 표현하지 못해 성능 향상이 제한될 수 있음
   - 해결방안: rank sweep을 수행하고 trainable parameter ratio와 domain benchmark score로 적합한 크기를 검증함
2. 문제: 적용 계층을 잘못 선택하면 비용은 쓰고도 원하는 도메인 적응 효과가 약할 수 있음
   - 해결방안: q, k, v, o projection별 ablation을 수행하고 per-module gain과 validation score로 효과를 검증함
3. 문제: 다수 LoRA 모듈을 동시에 서비스하면 로딩 지연과 메모리 관리 복잡도가 커질 수 있음
   - 해결방안: adapter cache 정책을 운영하고 adapter load latency와 GPU memory overhead로 멀티테넌트 운영성을 검증함

## Ⅶ. 적용 사례

- 사내 코드 보조 모델이 보안 규칙과 프레임워크 스타일을 학습하도록 LoRA를 적용하며 확인 지표는 accepted suggestion rate와 policy violation rate임
- 고객사별 문체 모델이 같은 base model에 고객별 LoRA를 분리 운영하도록 구성하며 확인 지표는 storage saving과 tenant switch latency임
- 연구용 모델 실험이 저비용으로 다양한 데이터셋을 빠르게 비교하도록 LoRA를 활용하며 확인 지표는 training time과 benchmark score임

## Ⅷ. 결론

LoRA는 적은 비용으로 강한 도메인 적응을 제공하는 PEFT의 사실상 표준이므로, rank와 target module 선택이 성능과 운영비를 좌우하는 핵심 설계 포인트임.
