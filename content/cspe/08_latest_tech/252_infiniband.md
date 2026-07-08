---
title: "InfiniBand (InfiniBand)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 252
extra:
  question_no: "252"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- InfiniBand는 고성능 컴퓨팅과 AI 클러스터에서 노드 간 저지연 고대역 통신을 제공하는 네트워크 기술임
- RDMA를 핵심 동작 방식으로 활용해 CPU 개입 없이 데이터를 직접 전송할 수 있음
- 노드 내부 NVLink와 달리 노드 간 확장성에 초점을 둔 인터커넥트임

## Ⅰ. 개요

- **정의/개념**: InfiniBand는 HPC와 AI 클러스터에서 서버 간 초저지연 고대역폭 통신과 RDMA를 제공해 분산 학습과 대규모 집단 통신 효율을 높이는 고성능 네트워크 기술임
- **배경/필요성**: 멀티노드 학습에서는 gradient 동기화와 파라미터 교환이 빈번해 일반 이더넷만으로는 지연과 CPU 오버헤드가 커져 전용 고성능 패브릭이 필요해짐

## Ⅱ. 특징

- 낮은 지연과 높은 대역폭으로 분산 학습 통신 비용을 줄임
- RDMA 지원으로 CPU 복사와 커널 개입 오버헤드를 줄임
- 대형 스위치 패브릭으로 수많은 노드를 연결할 수 있음
- QoS와 혼잡 제어와 토폴로지 설계가 실효 성능을 크게 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | InfiniBand | Ethernet | NVLink |
|:---|:---|:---|:---|
| 주 적용 범위 | 노드 간 HPC 및 AI 패브릭 | 범용 데이터센터 네트워크 | 노드 내부 GPU 연결 |
| RDMA 지원 | 강함 | RoCE로 확장 가능 | 직접 해당 없음 |
| 지연 | 매우 낮음 | 중간 | 더 낮음 |
| 핵심 가치 | 분산 통신 최적화 | 범용성과 비용 효율 | 로컬 GPU 연결 최적화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Host Channel Adapter | 서버에서 InfiniBand 패브릭과 직접 연결되어 RDMA와 메시지 전송을 수행하는 네트워크 어댑터임 |
| InfiniBand Switch | 다수 노드 간 트래픽을 고속으로 전달해 저지연 패브릭을 구성하는 스위치 계층임 |
| Subnet Manager | 경로 설정과 주소 관리와 패브릭 초기화를 담당해 네트워크 일관성을 유지하는 제어 계층임 |
| RDMA Engine | CPU 우회를 포함한 직접 메모리 전송 기능을 수행해 통신 오버헤드를 줄이는 핵심 기능임 |
| Congestion Control | 집단 통신과 대형 워크로드에서 트래픽 폭주를 제어해 성능 붕괴를 방지하는 운영 계층임 |

```text
+--------+    +---------+    +---------+    +--------+
| Node A |<-> | IB SW 1 |<-> | IB SW 2 |<-> | Node B |
+--------+    +---------+    +---------+    +--------+
      \______________________________________________/
                 Low-latency cluster fabric
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 버퍼 등록    | -> | 경로 설정    | -> | RDMA 전송    | -> | 수신 메모리 반영 | -> | 동기화 완료    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **버퍼 등록**: 송신과 수신 메모리를 RDMA 대상으로 등록함
2. **경로 설정**: 패브릭 경로와 큐를 구성함
3. **RDMA 전송**: CPU 우회 방식으로 데이터를 직접 전송함
4. **수신 메모리 반영**: 원격 메모리에 곧바로 데이터가 기록됨
5. **동기화 완료**: 집단 통신 단계가 마무리됨

## Ⅵ. 문제점 및 해결 방안

1. 문제: 혼잡 제어와 토폴로지 설계가 미흡하면 집단 통신 시 패브릭 병목이 발생해 스케일링 효율이 크게 떨어질 수 있음
   - 해결방안: congestion control tuning과 topology aware routing을 적용하고 network tail latency와 all reduce completion time으로 검증함
2. 문제: 전용 고성능 패브릭 도입 비용과 운영 복잡도가 커 대규모가 아니면 투자 효율이 낮아질 수 있음
   - 해결방안: workload based ROI planning과 tiered network architecture를 적용하고 cost per accelerated node와 cluster utilization uplift로 검증함
3. 문제: RDMA 설정과 버퍼 관리가 잘못되면 통신 오류와 디버깅 난도가 높아질 수 있음
   - 해결방안: standardized RDMA configuration과 observability tooling을 적용하고 transport error rate와 debug turnaround time으로 검증함

## Ⅶ. 적용 사례

- 대규모 LLM 클러스터가 혼잡 제어 최적화를 적용하며 확인 지표는 network tail latency와 all reduce completion time임
- AI 데이터센터가 계층형 네트워크 투자를 운영하며 확인 지표는 cost per accelerated node와 cluster utilization uplift임
- 분산 학습 플랫폼이 RDMA 관측 도구를 강화하며 확인 지표는 transport error rate와 debug turnaround time임

## Ⅷ. 결론

InfiniBand는 멀티노드 AI 학습의 통신 병목을 줄이는 핵심 패브릭이므로 토폴로지와 혼잡 제어와 운영 가시성을 함께 최적화해야 함.
