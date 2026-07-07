---
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 56
---

# NVLink 고속 인터커넥트 (NVLink)

## 미리 알고가기

- Interconnect: CPU, GPU, 메모리, 스위치 사이를 연결하는 고속 통신 경로임
- P2P: 피어 간 직접 통신(Peer-to-Peer, P2P)은 GPU가 다른 GPU 메모리에 직접 접근하는 방식임
- NVSwitch: 여러 GPU의 NVLink 연결을 스위칭해 대규모 GPU 패브릭을 구성하는 장치임
- Collective: AllReduce처럼 여러 GPU가 텐서를 집계하는 병렬 통신 연산임

## Ⅰ. 개요

- **정의/개념**: NVLink는 GPU와 GPU, 일부 플랫폼의 GPU와 CPU 사이를 고대역폭·저지연으로 연결해 PCIe 대비 GPU 메모리 접근과 다중 GPU 통신 효율을 높이는 NVIDIA 고속 인터커넥트임.
- **배경/필요성**: 대규모 AI 모델은 하나의 GPU 메모리와 연산 성능을 초과하므로 여러 GPU 간 tensor와 gradient 교환이 필수임. PCIe만으로는 통신 병목이 커져 GPU 유휴 시간이 증가하므로 전용 고속 연결이 필요함.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| GPU 클러스터 내부 고속 연결 구조 설명 | bandwidth, P2P, NVSwitch, topology, collective | PCIe의 단순 이름 대체로 설명, 통신 병목 누락 |

> 요약: NVLink는 다중 GPU 시스템에서 GPU 간 데이터 이동 병목을 줄이는 전용 고속 인터커넥트임.

## Ⅱ. 특징 및 비교

| 판단 기준 | PCIe 중심 연결 | NVLink 연결 |
|:---|:---|:---|
| 통신 경로 | 범용 I/O 버스로 CPU root complex와 스위치를 중심으로 연결됨 | GPU 간 직접 연결과 NVSwitch 패브릭 구성 가능 |
| 최적화 목표 | 호환성, 범용 주변장치 연결, 표준 생태계 | GPU 메모리 접근, collective 통신, 낮은 통신 지연 |
| 적용 기준 | 일반 서버와 다양한 장치 연결 | AI 학습, HPC, 대규모 GPU 노드 |
| 병목 지점 | PCIe 대역폭, CPU 경유, NUMA 영향 | 토폴로지 불균형, collective 설계 |

NVLink의 효과는 단일 GPU 연산이 아니라 다중 GPU 협업에서 드러남. 모델 병렬, 데이터 병렬, 파이프라인 병렬에서 GPU 간 통신량이 많을수록 링크 대역폭과 토폴로지의 영향이 커짐.

## Ⅲ. 구성요소/구조

```text
+---------+      +----------+      +---------+
| GPU 0   | <--> | NVSwitch | <--> | GPU 1   |
+---------+      +----------+      +---------+
     ^                 ^                 ^
     |                 |                 |
     v                 v                 v
+---------+      +----------+      +---------+
| GPU 2   | <--> | Fabric   | <--> | GPU 3   |
+---------+      +----------+      +---------+
```

| 구성요소 | 설명 | 핵심 포인트 |
|:---|:---|:---|
| NVLink Lane/Port | GPU 간 고속 직렬 링크를 제공함 | 링크 대역폭 |
| NVSwitch | 다수 GPU 연결을 스위칭해 패브릭을 구성함 | 확장성 |
| GPU 메모리 | P2P 접근과 tensor 교환의 대상임 | 메모리 접근 |
| Collective 라이브러리 | AllReduce, Broadcast 등 다중 GPU 통신을 최적화함 | 통신 패턴 |
| 토폴로지 | GPU 간 연결 형태와 hop 수를 결정함 | 지연과 균형 |

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Partition| ---> | Transfer | ---> | Aggregate| ---> | Continue |
+----------+      +----------+      +----------+      +----------+
```

대규모 모델은 여러 GPU에 분할되고, 각 GPU는 연산 중 필요한 tensor나 gradient를 NVLink/NVSwitch 패브릭을 통해 교환함. 통신이 계산과 겹치면 GPU 유휴 시간이 줄어 전체 학습 시간이 단축됨.

## Ⅳ. 문제점 및 개선방안

1. **토폴로지 불균형**: GPU 간 연결 hop 수나 대역폭이 다르면 특정 통신 경로가 병목이 됨.
   - **개선방안**: topology-aware placement와 NCCL 통신 경로 최적화를 적용함. (확인: link utilization, step time)
2. **통신-연산 비율 증가**: 모델이 커질수록 gradient 교환이 많아져 연산기보다 링크가 병목이 될 수 있음.
   - **개선방안**: gradient compression, overlap, tensor parallel 전략을 조정함. (확인: communication time ratio)
3. **벤더 종속과 비용**: NVLink는 특정 GPU 생태계에 결합되어 장비 선택과 비용 구조에 영향을 줌.
   - **개선방안**: PCIe, InfiniBand, Ethernet RDMA 대안과 TCO를 비교함. (확인: 학습 비용, 장비 가용성)

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 대규모 AI 학습 노드 | NVSwitch 기반 GPU 노드에서 AllReduce와 tensor parallel 통신을 최적화함 | step time, link utilization |
| HPC 시뮬레이션 | GPU 간 halo exchange나 matrix 분할 통신을 P2P로 처리함 | 통신 지연, GPU idle time |
| 멀티 GPU 추론 | 모델을 여러 GPU 메모리에 분할하고 NVLink로 activation을 교환함 | 토큰당 지연, 메모리 사용률 |

## Ⅵ. 결론

NVLink는 GPU 자체 성능보다 다중 GPU 간 데이터 이동을 줄이는 데 의미가 있는 인터커넥트임. AI 학습과 HPC에서는 연산량이 커질수록 통신 토폴로지와 collective 효율이 전체 성능을 좌우함. 따라서 NVLink 도입은 GPU 수, 모델 병렬 방식, 링크 사용률, 비용을 함께 검토해야 함.
