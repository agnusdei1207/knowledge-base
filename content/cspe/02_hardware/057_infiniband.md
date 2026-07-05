---
title: "InfiniBand (InfiniBand)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 57
---

## Ⅰ. 개요
- **정의**: HPC·AI 클러스터에서 노드 간 저지연·고대역폭 통신을 제공하는 네트워크 인터커넥트 기술
- **배경/필요성**: 이더넷 기반 네트워크는 프로토콜 스택 오버헤드로 GPU 클러스터의 노드 간 통신 병목이 되므로, RDMA를 지원하는 전용 인터커넥트가 필요함
- **비유**: 이더넷이 일반 택배 서비스라면, InfiniBand는 수신자에게 물건을 직접 놓아두는 전용 배송 시스템임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 고성능 네트워크 인터커넥트 구조 이해 | RDMA(원격 직접 메모리 접근)와 커널 바이패스 | InfiniBand와 RoCE(RDMA over Converged Ethernet)의 차이를 구분할 것 |

> 요약: RDMA 기반 커널 바이패스로 노드 간 저지연·고대역폭 통신을 제공하는 인터커넥트임

## Ⅱ. 구성요소
```text
Node A                         Node B
  |                              |
  +-- HCA (Host Channel         +-- HCA
  |    Adapter)                  |
  +-- RDMA Verbs                 +-- RDMA Verbs
       |                              |
       +------- IB Switch --------+
                   |
              Subnet Manager
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| HCA | 호스트에 장착되어 RDMA를 하드웨어로 처리하는 네트워크 어댑터 | 전용 화물 터미널 |
| IB Switch | 노드 간 패킷을 전달하는 InfiniBand 전용 스위치 | 화물 분류 센터 |
| Subnet Manager | IB 네트워크의 경로 설정과 토폴로지를 관리하는 소프트웨어 | 교통 관제탑 |
| RDMA Verbs | 커널 바이패스로 원격 메모리에 직접 읽기·쓰기하는 API 계층 | 수신자 부재 중 직접 배달 |
| Queue Pair | 송·수신 큐 쌍으로 RDMA 통신의 기본 엔드포인트를 구성함 | 양방향 우편함 |

> 요약: HCA가 RDMA를 하드웨어 처리하고 IB Switch와 Subnet Manager가 네트워크를 구성함

## Ⅲ. 절차
```text
QP 생성 --> 메모리 등록 --> RDMA Write/Read --> 완료 통지
    |            |                |                |
    v            v                v                v
 연결 설정    MR 핀 고정     커널 바이패스 전송    CQ 폴링
```
- 1단계: 송·수신 노드에서 Queue Pair(QP)를 생성하고 연결 정보를 교환하여 통신 경로를 설정함
- 2단계: 전송 대상 메모리 영역을 Memory Region(MR)으로 등록하고 물리 주소를 핀 고정함
- 3단계: HCA가 커널 개입 없이 원격 노드 메모리에 RDMA Write/Read를 수행하여 데이터를 전송함
- 4단계: 전송 완료 후 Completion Queue(CQ)에 완료 이벤트가 기록되어 송신 측이 결과를 확인함

> 요약: QP 설정, MR 등록, RDMA 전송, CQ 완료 통지의 4단계로 커널 바이패스 통신을 수행함

## Ⅳ. 문제점
- 도입 비용: HCA·IB Switch 등 전용 장비의 단가가 이더넷 대비 3~5배 높음
- 운영 복잡도: Subnet Manager 설정, QP 관리 등 이더넷 대비 운영 지식 요구 수준이 높음
- 상호 운용성: 벤더 간 펌웨어·드라이버 호환 이슈로 이기종 장비 혼용이 어려움

> 요약: 높은 도입 비용, 운영 복잡도, 제한된 상호 운용성이 주요 과제임

## Ⅴ. 개선방안
1. 단기: Ultra Ethernet 등 이더넷 기반 RDMA(RoCE v2) 병행 도입으로 비용을 절감함
2. 중기: 자동화된 패브릭 관리 도구를 도입하여 Subnet Manager 운영 부담을 경감함
3. 장기: 개방형 인터커넥트 표준(UALink 등) 참여로 벤더 간 상호 운용성을 확보함

> 요약: RoCE 병행, 운영 자동화, 개방형 표준 참여로 단계적 개선이 필요함

## Ⅵ. 전망
- 발전 방향: NDR(400Gbps), XDR(800Gbps) 등 세대별 대역폭이 배증하며 AI 클러스터의 표준 인터커넥트로 유지됨
- 기술사적 판단: Ultra Ethernet과의 경쟁이 심화되나, 저지연 RDMA 우위로 HPC·AI 영역에서는 당분간 InfiniBand 채택이 지속될 전망임
- 기술사 제언: 클러스터 설계 시 NVLink(056 참조, 노드 내)과 InfiniBand(노드 간) 대역폭 비율을 최적화해야 함
