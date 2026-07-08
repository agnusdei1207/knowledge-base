---
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 56
extra:
  question_no: "056"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- NVLink는 GPU 간 또는 CPU-GPU 간 고대역폭 연결을 위한 전용 인터커넥트임
- PCIe보다 높은 대역폭과 낮은 지연으로 다중 GPU 병목을 줄이는 데 목적이 있음
- 대규모 AI 학습과 메모리 공유형 가속기 구성에 중요함

## Ⅰ. 개요

- **정의/개념**: NVLink는 다중 GPU와 일부 CPU, 스위치 장치를 고속 point-to-point 링크로 연결해 PCIe 대비 더 큰 대역폭과 낮은 통신 오버헤드를 제공하는 고성능 가속기 인터커넥트임
- **배경/필요성**: 대형 모델 학습은 GPU 개별 계산보다 gradient 동기화와 텐서 교환 비용이 커지므로, GPU 간 통신 병목을 줄일 전용 연결이 필요함

## Ⅱ. 특징

- GPU 간 대역폭을 크게 높여 collective 통신 시간을 줄임
- NVSwitch와 결합하면 다수 GPU를 고밀도로 연결할 수 있음
- 특정 벤더 생태계 의존성이 높아 범용 호환성은 제한적임
- 통신 구조를 잘못 설계하면 링크가 있어도 토폴로지 병목이 남을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | PCIe | NVLink | NVSwitch 기반 구성 |
|:---|:---|:---|:---|
| 대역폭 | 중간 | 높음 | 매우 높음 |
| 토폴로지 확장성 | 중간 | 제한적 direct link | 높음 |
| 지연 | 중간 | 낮음 | 낮음 |
| 대표 용도 | 범용 연결 | 소수 GPU 고속 연결 | 대규모 GPU 패브릭 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| NVLink PHY | 고속 직렬 링크를 제공해 GPU 간 직접 데이터 이동을 수행함 |
| NVSwitch | 다수 GPU 사이 교차 연결을 제공해 전체 토폴로지 확장성을 높임 |
| GPU Memory Path | peer access와 collective 통신 효율을 좌우하는 핵심 경로임 |
| Communication Runtime | NCCL 같은 소프트웨어가 토폴로지 인지 통신 전략을 구성함 |

```text
+-------------+     +-------------+     +-------------+     +-------------+
| GPU A       | <-> | NVLink PHY  | <-> | NVSwitch    | <-> | GPU B..N    |
+-------------+     +-------------+     +-------------+     +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 링크 구성      | --> | 피어 메모리 접근 | --> | collective 통신 | --> | 결과 동기화    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **링크 구성**: GPU 간 NVLink 연결과 토폴로지를 설정함
2. **피어 메모리 접근**: GPU가 서로의 메모리에 고속 접근함
3. **Collective 통신**: all-reduce 등 다중 GPU 통신을 수행함
4. **결과 동기화**: 학습 결과와 상태를 일치시킴

## Ⅵ. 문제점 및 해결 방안

1. 문제: GPU 수가 늘어날수록 토폴로지 불균형이 생기면 일부 링크에 통신이 집중돼 전체 학습 시간이 늘어날 수 있음
   - 해결방안: 토폴로지 인지 통신 라이브러리를 적용하고 link utilization과 all-reduce time으로 병목을 검증함
2. 문제: 전용 인터커넥트 의존성이 높아 장비 선택 폭과 비용 유연성이 줄어들 수 있음
   - 해결방안: PCIe와 InfiniBand 구성과 함께 비교하고 TCO와 performance gain으로 투자 타당성을 검증함
3. 문제: 링크 대역폭이 높아도 데이터 분할과 배치 전략이 나쁘면 통신량 자체가 과도해 이점이 희석될 수 있음
   - 해결방안: model parallel과 pipeline parallel 전략을 최적화하고 communication ratio와 step time으로 검증함

## Ⅶ. 적용 사례

- 대규모 LLM 학습 서버에서는 GPU 간 gradient 교환에 NVLink를 사용하고 확인 지표는 all-reduce time과 training throughput임
- 멀티 GPU 추론 서버에서는 peer memory access를 활용하고 확인 지표는 request latency와 GPU memory copy time임
- NVSwitch 기반 AI 슈퍼노드에서는 집적 연결을 구성하고 확인 지표는 inter-GPU bandwidth와 cluster efficiency임

## Ⅷ. 결론

NVLink의 가치는 단순 대역폭 숫자보다 다중 GPU 통신 병목을 얼마나 줄이느냐에 있으므로, 토폴로지와 collective 전략을 함께 설계해야 효과가 극대화됨.
