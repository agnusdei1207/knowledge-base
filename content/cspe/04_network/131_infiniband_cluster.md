---
title: "InfiniBand 클러스터 인터커넥트 (InfiniBand Cluster)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 131
extra:
  question_no: "131"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- HCA는 서버의 PCIe와 InfiniBand 패브릭을 연결하고 RDMA 작업을 처리하는 어댑터임
- Verbs는 Queue Pair·메모리 등록·전송 요청을 제어하는 RDMA 인터페이스임
- Subnet Manager는 LID와 경로를 할당하고 패브릭 토폴로지를 관리함
- 크레딧 기반 흐름 제어는 수신 버퍼 여유만큼 송신을 허용해 링크 손실을 억제함

## Ⅰ. 개요

- **정의/개념**: InfiniBand는 HCA와 스위치를 전용 패브릭으로 연결하고 RDMA와 크레딧 기반 흐름 제어를 제공하는 HPC·AI 클러스터 인터커넥트임
- **배경/필요성**: MPI 메시지와 분산 학습의 집합 통신은 노드 간 데이터를 반복 교환하므로 커널 처리와 패킷 손실·재전송을 줄이고 계산 노드의 대기 시간을 제한할 패브릭이 필요함

## Ⅱ. 특징

- Verbs와 Queue Pair를 통해 Send·Receive와 One-sided RDMA를 처리함
- 링크별 크레딧으로 수신 버퍼를 관리해 이더넷 PFC 없이 패브릭 손실을 억제함
- Subnet Manager가 토폴로지를 탐색하고 LID와 전달 경로를 설정함
- 링크 대역폭만 높여도 Oversubscription과 집합 통신 경합이 남으면 GPU 대기 시간이 증가함

## Ⅲ. 종류 및 비교

| 판단 기준 | InfiniBand | RoCEv2 |
|:---|:---|:---|
| 패브릭 기반 | InfiniBand 전용 링크·스위치 | UDP/IP 이더넷 패브릭 |
| 손실 제어 | 링크 크레딧 기반 흐름 제어 | ECN·DCQCN과 제한적 PFC |
| 경로 관리 | Subnet Manager와 LID 경로 | IP 라우팅과 ECMP |
| 운영 체계 | HCA·IB 스위치·Verbs 중심 | 이더넷 스위치·RNIC·IP 도구 중심 |
| 적용 환경 | HPC·AI 전용 클러스터 | 이더넷 통합 데이터센터의 RDMA |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| HCA | 메모리 등록, 패킷 처리, RDMA 작업을 실행함 |
| InfiniBand 스위치 | LID 기반 패킷 전달과 가상 레인 큐를 처리함 |
| Subnet Manager | 토폴로지, 주소, 경로를 설정함 |
| Queue Pair·Completion Queue | 전송 요청과 완료 상태를 관리함 |
| Fat-tree·Dragonfly 토폴로지 | 노드 간 경로 수와 Oversubscription을 결정함 |

```text
[Compute HCA] -- [Leaf IB Switch] -- [Spine IB Switch] -- [Leaf] -- [Compute HCA]
                           | Subnet Manager |
```

## Ⅴ. 원리 및 절차 흐름도

```text
서브넷 탐색 -> LID·경로 배정 -> QP·메모리 등록 -> RDMA 전송 -> 완료 통지
```

1. **패브릭 설정**: Subnet Manager가 포트와 링크를 탐색해 LID와 경로를 배정함
2. **RDMA 자원 준비**: 애플리케이션이 메모리와 Queue Pair를 등록하고 상대 연결 정보를 교환함
3. **크레딧 확인**: 각 링크가 수신 버퍼 크레딧을 확인한 뒤 패킷을 전달함
4. **완료 처리**: HCA가 원격 메모리 작업을 끝내고 Completion Queue에 결과를 기록함

> 요약: InfiniBand는 서브넷 경로와 링크 크레딧을 설정한 패브릭에서 HCA가 RDMA 전송을 처리함.

## Ⅵ. 실무 적용 및 유의점

1. AI 학습 클러스터는 All-Reduce 패턴에 맞춰 Fat-tree 경로와 Oversubscription을 설계하고 링크 사용률, 집합 통신 시간, GPU 통신 대기율을 확인해야 함
2. Subnet Manager 이중화나 경로 갱신이 실패하면 패브릭 전체 연결에 영향을 줄 수 있으므로 관리자 장애 전환과 링크 장애 경로를 시험하고 경로 복구 시간과 포트 오류를 점검해야 함

## Ⅶ. 결론

InfiniBand는 HCA·전용 스위치·Subnet Manager와 크레딧 흐름 제어를 결합하며, 집합 통신 패턴과 패브릭 경로 구조를 기준으로 설계해야 함.
