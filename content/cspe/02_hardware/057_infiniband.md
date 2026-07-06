---
title: "InfiniBand (InfiniBand)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 57
---

## 미리 알고가기

- RDMA: 원격 직접 메모리 접근(Remote Direct Memory Access, RDMA)은 원격 서버 메모리에 중앙처리장치(Central Processing Unit, CPU) 개입을 최소화해 직접 읽기·쓰기를 수행하는 기술임
- HCA: 호스트 채널 어댑터(Host Channel Adapter, HCA)는 서버가 InfiniBand 패브릭에 접속하는 어댑터임
- Subnet Manager: InfiniBand 패브릭의 주소, 경로, 포트를 관리하는 제어 구성요소임
- Queue Pair: 송신 큐와 수신 큐로 구성된 RDMA 통신 엔드포인트임

## Ⅰ. 개요

- **정의**: InfiniBand는 HCA, 스위치, 서브넷 관리, RDMA 전송을 기반으로 고대역폭·저지연·낮은 CPU 사용률을 제공해 고성능 컴퓨팅(High Performance Computing, HPC)과 인공지능(Artificial Intelligence, AI) 클러스터의 노드 간 통신 지연과 대역폭 요구를 만족시키는 고성능 네트워크 패브릭임.
- **배경/필요성**: 대규모 학습과 과학 계산은 노드 간 gradient, 메시지, 파일 입출력(Input/Output, I/O)을 빈번히 교환함. 일반 이더넷만으로는 지연과 CPU 오버헤드가 커질 수 있어 RDMA 중심의 전용 패브릭이 필요함.
- **비유**: 서버들이 우편 창구를 거치지 않고 서로의 지정 창고에 직접 물건을 옮기는 전용 물류망과 같음.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| HPC/AI 클러스터 네트워크 구조 설명 | RDMA, HCA, Switch, Subnet Manager, QoS | 단순 빠른 LAN으로 설명 |

> 요약: InfiniBand는 RDMA와 전용 패브릭으로 노드 간 통신 지연과 CPU 부담을 줄이는 클러스터 네트워크임.

## Ⅱ. 특징/비교

| 판단 기준 | 이더넷 중심 클러스터 | InfiniBand 클러스터 |
|:---|:---|:---|
| 전송 방식 | 전송 제어 프로토콜/인터넷 프로토콜(Transmission Control Protocol/Internet Protocol, TCP/IP) 스택과 범용 네트워크 운영을 중심으로 함 | RDMA, 큐 페어, 서브넷 관리로 저지연 전송을 제공함 |
| 운영 목표 | 범용성, 관리 편의, 광범위한 장비 선택 | 낮은 지연, 높은 대역폭, 손실 없는 패브릭 운영 |
| 적용 기준 | 일반 서버, 웹, 엔터프라이즈 트래픽에 적합함 | HPC, AI 학습, 병렬 파일시스템에 적합함 |

> 요약: InfiniBand는 범용 네트워크보다 병렬 계산 통신의 예측 가능한 저지연을 우선함.

## Ⅲ. 구성요소

```text
+--------+     +----------+     +--------+
| Server | --- | Switch   | --- | Server |
|  HCA   |     +----------+     |  HCA   |
+--------+           |
                     v
              +--------------+
              | Subnet Mgr   |
              +--------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| HCA | 서버 메모리와 InfiniBand 패브릭 사이에서 RDMA 전송을 수행함 | 전용 물류 출입구 |
| 스위치 | 포트 간 패킷을 전달하고 다중 경로와 서비스 품질(Quality of Service, QoS)을 지원함 | 물류 허브 |
| Subnet Manager | 로컬 식별자(Local Identifier, LID), 경로, 링크 상태를 관리해 패브릭을 구성함 | 교통 관제실 |
| Verbs/RDMA 계층 | Queue Pair, Memory Region을 통해 애플리케이션 통신을 실행함 | 배송 절차서 |

> 요약: InfiniBand 구성은 HCA, 스위치, 서브넷 관리자, RDMA 소프트웨어 계층으로 이루어짐.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Fabric   | --> | RegMem   | --> | RDMA     | --> | Congest  |
+----------+     +----------+     +----------+     +----------+
```

1. **패브릭 구성**: Subnet Manager가 링크와 포트를 발견하고 주소와 경로를 설정함
2. **자원 등록**: 애플리케이션이 메모리 영역과 Queue Pair를 등록해 RDMA 준비를 완료함
3. **RDMA 전송**: HCA가 Send, Receive, Read, Write 명령으로 원격 메모리 접근을 수행함
4. **혼잡 관리**: QoS, 가상 레인, 경로 재계산으로 핫스팟과 손실을 줄임

> 요약: InfiniBand는 패브릭 제어와 메모리 등록 후 HCA가 직접 전송을 수행하는 구조임.

## Ⅴ. 문제점

- **P1 운영 복잡도**: Subnet Manager, 펌웨어, 케이블, 라우팅 설정이 맞지 않으면 장애 원인 파악이 어려움
- **P2 혼잡 핫스팟**: collective 통신과 스토리지 트래픽이 특정 링크에 집중되면 지연이 급증함
- **P3 비용·생태계 제약**: 전용 HCA와 스위치, 전문 운영 역량이 필요해 초기 도입 비용이 큼

> 요약: InfiniBand 문제는 저지연 성능을 얻기 위한 패브릭 운영 복잡도와 비용에서 발생함.

## Ⅵ. 개선방안

- **P1 대응**: 펌웨어 표준화, 포트 자동 점검, 토폴로지 문서화, 장애 runbook을 운영함 (확인: 링크 장애 탐지 시간)
- **P2 대응**: fat-tree 설계, adaptive routing, QoS 분리, collective 알고리즘 튜닝을 적용함 (확인: 링크별 혼잡 카운터)
- **P3 대응**: RDMA over Converged Ethernet(RoCE)/Ethernet 대안과 워크로드별 성능비를 비교해 단계적 도입을 계획함 (확인: 성능당 총비용)

> 요약: 개선은 자동화된 패브릭 운영, 혼잡 제어, 비용 대비 성능 검증으로 수행함.

## Ⅶ. 전망

- **발전 방향**: InfiniBand 계열 패브릭은 고속 링크, 인네트워크 집계, 그래픽 처리 장치(Graphics Processing Unit, GPU) 메모리 직접 전송과 결합해 AI/HPC 노드 간 collective 시간을 줄이는 방향으로 발전함
- **기술사적 판단**: leaf-spine oversubscription, HCA 포트 수, Subnet Manager 이중화, 병렬 파일시스템 트래픽 분리를 기준으로 패브릭 규모를 정함; RDMA 지연, all-reduce 대역폭, 혼잡 카운터, 패킷 폐기, failover 시간을 측정해 메시지 전달 인터페이스(Message Passing Interface, MPI)와 학습 워크로드의 실효 이득을 확인함
- **기술사 제언**: InfiniBand 답안은 포트 속도보다 RDMA 경로, 혼잡 제어, Subnet Manager 운영, 장애 격리 지표를 함께 제시해야 설계 판단이 분명함
