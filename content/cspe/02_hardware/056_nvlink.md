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
- 대규모 AI 학습과 메모리 공유형 가속기 구성에 필요함

## Ⅰ. 개요

- **정의/개념**: NVLink는 다중 GPU와 일부 CPU, 스위치 장치를 고속 point-to-point 링크로 연결해 PCIe 대비 더 큰 대역폭과 낮은 통신 오버헤드를 제공하는 고성능 가속기 인터커넥트임
- **배경/필요성**: 대형 모델 학습은 GPU 개별 계산보다 gradient 동기화와 텐서 교환 비용이 커지므로, GPU 간 통신 병목을 줄일 전용 연결이 필요함

## Ⅱ. 특징

- GPU 간 대역폭을 늘려 collective 통신 시간을 줄임
- NVSwitch와 결합하면 다수 GPU를 고밀도로 연결할 수 있음
- 특정 벤더 생태계 의존성이 높아 범용 호환성은 제한적임
- 통신 구조를 잘못 설계하면 링크가 있어도 토폴로지 병목이 남을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | PCIe | NVLink | NVSwitch 기반 구성 |
|:---|:---|:---|:---|
| 대역폭 | 중간 | 높음 | 가장 높음 |
| 토폴로지 확장성 | 중간 | 제한적 direct link | 높음 |
| 지연 | 중간 | 낮음 | 낮음 |
| 대표 용도 | 범용 연결 | 소수 GPU 고속 연결 | 대규모 GPU 패브릭 |

> 요약: NVLink는 PCIe보다 GPU 간 대역폭을 늘리고, NVSwitch는 다중 GPU 패브릭을 구성함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| NVLink PHY | 고속 직렬 링크를 제공해 GPU 간 직접 데이터 이동을 수행함 |
| NVSwitch | 다수 GPU 사이 교차 연결을 제공해 전체 토폴로지 확장 범위를 넓힘 |
| GPU Memory Path | peer access와 collective 통신 효율을 좌우하는 핵심 경로임 |
| Communication Runtime | NCCL 같은 소프트웨어가 토폴로지 인지 통신 전략을 구성함 |

```text
+-------------+     +-------------+     +-------------+     +-------------+
| GPU A       | <-> | NVLink PHY  | <-> | NVSwitch    | <-> | GPU B..N    |
+-------------+     +-------------+     +-------------+     +-------------+
```

> 요약: NVLink는 물리 링크, 스위치, GPU memory path, NCCL 전략이 맞아야 통신 병목을 줄임.

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

> 요약: NVLink는 피어 메모리 접근과 collective 통신으로 다중 GPU 상태를 동기화함.

## Ⅵ. 실무 적용 및 유의점

1. 대규모 LLM 학습 서버는 토폴로지 불균형 시 일부 링크가 병목이 되므로 NCCL 토폴로지 설정과 병렬화 전략을 조정하고 link utilization, all-reduce time으로 확인함
2. 멀티 GPU 추론 서버는 peer memory access로 호스트 경유 복사를 줄일 수 있으므로 전용 인터커넥트 비용을 PCIe·InfiniBand 구성과 비교하고 request latency, TCO로 확인함

## Ⅶ. 결론

NVLink의 가치는 대역폭 숫자보다 다중 GPU 통신 병목을 얼마나 줄이느냐에 있으므로 토폴로지와 collective 전략을 함께 설계해야 함.

## 작성 근거(검토용)

- NVLink는 GPU 간 대역폭, NVSwitch, peer memory access, collective 통신을 핵심 축으로 설명함
- 비교표는 PCIe, NVLink, NVSwitch 기반 구성의 대역폭과 확장성 차이를 보임
- 실무 판단은 link utilization, all-reduce time, request latency, TCO로 검증 가능하게 작성함
