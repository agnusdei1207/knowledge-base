---
title: "InfiniBand (InfiniBand)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 57
extra:
  question_no: "057"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- InfiniBand는 RDMA 중심의 고성능 네트워크 패브릭임
- HCA, switch, subnet manager, queue pair가 주요 구성요소임
- HPC와 AI 클러스터의 저지연 통신 요구에 특화됨

## Ⅰ. 개요

- **정의/개념**: InfiniBand는 RDMA 기반 전송과 전용 패브릭 관리 구조를 사용해 서버 간 메모리 접근과 메시지 전달을 낮은 지연과 낮은 CPU 오버헤드로 수행하는 고성능 인터커넥트임
- **배경/필요성**: 분산 학습과 HPC는 작은 메시지와 대량 collective 통신이 빈번하므로, TCP/IP 중심 네트워크보다 더 예측 가능하고 낮은 지연의 패브릭이 필요함

## Ⅱ. 특징

- RDMA를 통해 CPU 개입과 커널 오버헤드를 줄임
- 대역폭과 지연 특성이 뛰어나 MPI와 분산 학습에 적합함
- 전용 어댑터와 운영 노하우가 필요해 범용 네트워크보다 복잡함
- congestion control과 subnet 관리 품질이 전체 성능에 직접 영향을 줌

## Ⅲ. 종류 및 비교

| 판단 기준 | Ethernet TCP/IP | RoCE | InfiniBand |
|:---|:---|:---|:---|
| CPU 오프로드 | 낮음 | 중간 | 높음 |
| 지연 | 중간 | 낮음 | 매우 낮음 |
| 운영 복잡도 | 낮음 | 중간 | 높음 |
| 대표 용도 | 범용 서버 | RDMA 이더넷 | HPC, AI 클러스터 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| HCA | 서버 메모리와 패브릭을 연결하고 RDMA 작업을 수행해 CPU 부담을 줄임 |
| Queue Pair | 송신과 수신 작업을 큐로 관리해 응용과 네트워크 간 비동기 통신을 가능하게 함 |
| Switch Fabric | 고대역폭 경로를 제공하며 토폴로지와 혼잡 제어 성능이 중요함 |
| Subnet Manager | 주소와 경로와 포트 상태를 관리해 패브릭 일관성을 유지함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 메모리 등록    | --> | QP 작업 게시   | --> | RDMA 전송 수행 | --> | 완료 통지      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **메모리 등록**: RDMA 대상 버퍼를 등록함
2. **QP 작업 게시**: 송수신 요청을 queue pair에 올림
3. **RDMA 전송 수행**: HCA가 패브릭을 통해 메모리를 직접 읽고 씀
4. **완료 통지**: completion queue로 결과를 알려줌

## Ⅵ. 문제점 및 해결 방안

1. 문제: 다수 노드 collective 통신에서 특정 링크에 혼잡이 몰리면 전체 작업 시간이 크게 늘어날 수 있음
   - 해결방안: adaptive routing과 job placement를 적용하고 congestion event와 step time으로 병목을 검증함
2. 문제: 서브넷 관리와 펌웨어와 케이블 상태가 복잡해 운영 실수 하나가 패브릭 장애로 이어질 수 있음
   - 해결방안: topology validation과 automated health check를 운영하고 link error rate와 failover time으로 안정성을 검증함
3. 문제: 전용 장비와 운영 인력 비용이 높아 범용 워크로드에는 과투자가 될 수 있음
   - 해결방안: Ethernet RDMA 대안과 비교하고 TCO와 latency benefit으로 도입 타당성을 검증함

## Ⅶ. 적용 사례

- 대규모 AI 학습 클러스터에서는 all-reduce 통신에 InfiniBand를 사용하고 확인 지표는 communication time과 GPU idle ratio임
- HPC 시뮬레이션에서는 MPI 메시지 지연을 줄이고 확인 지표는 message latency와 job completion time임
- 병렬 파일시스템 백엔드에서는 RDMA 전송을 활용하고 확인 지표는 storage throughput과 CPU offload ratio임

## Ⅷ. 결론

InfiniBand의 본질은 빠른 네트워크가 아니라 CPU를 우회하는 저지연 패브릭에 있으므로, 통신이 계산 병목을 지배하는 클러스터에서 가장 높은 가치를 가짐.
