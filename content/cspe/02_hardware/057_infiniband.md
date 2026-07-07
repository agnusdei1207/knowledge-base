---
title: "InfiniBand (InfiniBand)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 57
---

# InfiniBand (InfiniBand)

## 미리 알고가기

- RDMA: 원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)은 원격 서버 메모리에 CPU 개입을 최소화해 직접 읽기·쓰기를 수행하는 기술임
- HCA: 호스트 채널 어댑터(Host Channel Adapter, HCA)는 서버가 InfiniBand 패브릭에 접속하는 어댑터임
- Subnet Manager: InfiniBand 패브릭의 주소, 경로, 포트를 관리하는 제어 구성요소임
- Queue Pair: 송신 큐와 수신 큐로 구성된 RDMA 통신 엔드포인트임

## 1. 개요

- **정의/개념**: InfiniBand는 HCA, 스위치, 서브넷 관리, RDMA 전송을 기반으로 고대역폭·저지연·낮은 CPU 사용률을 제공해 HPC와 AI 클러스터의 노드 간 통신 요구를 만족시키는 고성능 네트워크 패브릭임.
- **배경/필요성**: 대규모 학습과 과학 계산은 노드 간 gradient, 메시지, 파일 I/O를 빈번히 교환함. 일반 TCP/IP 네트워크만으로는 지연과 CPU 오버헤드가 커질 수 있어 RDMA 중심의 전용 패브릭이 필요함.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| HPC/AI 클러스터 네트워크 구조 설명 | RDMA, HCA, switch, subnet manager, QoS | 단순 빠른 LAN으로 설명, CPU offload 누락 |

> 요약: InfiniBand는 RDMA와 전용 패브릭으로 노드 간 통신 지연과 CPU 부담을 줄이는 클러스터 네트워크임.

## 2. 특징 및 비교

| 판단 기준 | 이더넷 중심 클러스터 | InfiniBand 클러스터 |
|:---|:---|:---|
| 전송 방식 | TCP/IP 스택과 범용 네트워크 운영 중심 | RDMA, queue pair, subnet 관리 기반 저지연 전송 |
| 운영 목표 | 범용성, 관리 편의, 장비 선택 폭 | 낮은 지연, 높은 대역폭, 손실 없는 패브릭 |
| 적용 기준 | 일반 서버, 웹, 엔터프라이즈 트래픽 | HPC, AI 학습, 병렬 파일시스템 |
| 병목 요인 | TCP 처리, CPU interrupt, 혼잡 | 경로 설정, congestion, fabric 장애 |

InfiniBand는 단순히 속도가 높은 네트워크가 아니라 CPU를 우회하는 데이터 경로와 예측 가능한 패브릭 운영이 핵심임. 작은 메시지가 빈번한 MPI 작업과 대규모 collective 통신에서 효과가 특히 큼.

## 3. 구성요소/구조

```text
+----------+      +----------+      +----------+
| Node A   | <--> | IB Switch| <--> | Node B   |
| HCA/QP   |      | Fabric   |      | HCA/QP   |
+----------+      +----------+      +----------+
       \                |
        \               v
         +------> +-------------+
                  | Subnet Mgr  |
                  +-------------+
```

| 구성요소 | 설명 | 핵심 포인트 |
|:---|:---|:---|
| HCA | 서버 메모리와 InfiniBand 패브릭을 연결하고 RDMA를 수행함 | CPU offload |
| Queue Pair | RDMA 송수신 요청을 큐 기반으로 처리함 | 통신 엔드포인트 |
| 스위치 | 노드 간 패킷을 고속으로 전달함 | 패브릭 대역폭 |
| Subnet Manager | 주소, 경로, 포트 상태를 관리함 | 제어 평면 |
| QoS/혼잡 제어 | 우선순위와 혼잡 상황을 통제함 | 예측 가능성 |

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Register | ---> | Post WR  | ---> | RDMA     | ---> | Complete |
+----------+      +----------+      +----------+      +----------+
```

애플리케이션은 메모리를 등록하고 queue pair에 work request를 게시함. HCA는 패브릭을 통해 원격 메모리에 직접 접근하고 완료 큐로 결과를 알려 CPU 개입을 줄임.

## 4. 문제점 및 개선방안

1. **운영 복잡도**: 서브넷 관리, 펌웨어, 케이블링, 토폴로지 오류가 성능과 장애에 직접 영향을 줌.
   - **개선방안**: fabric health check, topology validation, 펌웨어 표준화를 운영 절차에 포함함. (확인: link error, path change)
2. **혼잡과 head-of-line blocking**: 다수 노드 collective 통신에서 특정 링크가 혼잡해 전체 작업이 지연될 수 있음.
   - **개선방안**: adaptive routing, QoS, job placement, congestion control을 적용함. (확인: congestion event, job step time)
3. **비용과 생태계 제약**: 전용 HCA와 스위치, 운영 인력 비용이 높고 일반 이더넷보다 선택 폭이 좁음.
   - **개선방안**: RoCE, Ethernet RDMA, InfiniBand를 워크로드 기준으로 비교하고 TCO를 평가함. (확인: 비용 대비 통신 지연 개선)

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| AI 학습 클러스터 | GPU 노드 간 gradient AllReduce를 InfiniBand RDMA로 처리함 | step time, network utilization |
| HPC MPI 작업 | 작은 메시지와 대규모 barrier 통신을 낮은 지연으로 수행함 | MPI latency, job completion time |
| 병렬 파일시스템 | 컴퓨트 노드와 스토리지 노드 사이 대용량 I/O를 고대역폭으로 전송함 | throughput, I/O wait |

## 6. 결론

InfiniBand는 HPC와 AI 클러스터에서 통신 지연과 CPU 오버헤드를 줄이는 고성능 패브릭임. 다만 장비를 연결하는 것만으로 성능이 보장되지 않고, 토폴로지·혼잡·서브넷 관리가 함께 맞아야 함. 따라서 도입 판단은 대역폭 수치보다 RDMA 효과, 작업 통신 패턴, 운영 복잡도, TCO를 기준으로 해야 함.
