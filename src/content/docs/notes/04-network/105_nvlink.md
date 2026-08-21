---
sidebar:
  order: 105
  label: "105. NVLink 고대역폭 인터커넥트 (NVLink)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초고속 GPU 스케일업 인터커넥트 : NVLink 및 NVSwitch (High-Bandwidth Interconnect)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 105
extra:
  question_no: "105"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "GPU-to-GPU 고대역폭, NVSwitch 풀 메시(Full-Mesh), 단일 공유 메모리 풀(SHMEM), NCCL 가속"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NVLink**: NVIDIA가 GPU 간(GPU-to-GPU) 및 CPU-GPU 간의 초고속 데이터 교환을 위해 개발한 전용 점대점(Point-to-Point) 직렬 통신 인터커넥트 프로토콜.
- **NVSwitch**: 단일 서버 노드(DGX/HGX) 내에서 다수의 GPU를 완전 비차단 풀 메시(Full-Mesh) 토폴로지로 연결하여 모든 GPU가 동일한 초대역폭으로 상호 직접 접근할 수 있도록 중계하는 고성능 스위치 반도체.

</details>

- 정의/개념: 표준 PCIe 버스의 대역폭 한계를 극복하고 복수의 GPU 메모리 공간을 단일 통합 가상 주소 공간(Unified Memory Space)으로 묶어, **GPU 간 최대 1.8TB/s~7.2TB/s의 양방향 대역폭** 을 제공하는 **초고속 스케일업(Scale-Up) 인터커넥트 아키텍처**
- 배경/필요성: 수천억 파라미터 규모의 초거대 언어 모델(LLM) 훈련 시 텐서 병렬화(Tensor Parallelism) 연산에서 발생하는 폭발적인 GPU 간 중간 가중치 동기화 트래픽을 PCIe 버스(128GB/s)로 수용할 수 없는 극심한 통신 병목을 해소할 요구

#### 한줄 요약
- NVSwitch와 전용 직렬 링크를 통해 단일 노드 내 복수 GPU를 완전 비차단 고대역폭 공유 메모리로 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **공유 메모리 가상화(Unified Memory / SHMEM)**: 물리적으로 분리된 8개~72개 GPU의 고대역폭 메모리(HBM)를 하나의 거대한 단일 주소 공간으로 매핑하여 임의의 GPU가 타 GPU의 HBM에 직접 로드/스토어(Load/Store)를 수행하는 기술.
- **하드웨어 집합 통신 가속(SHARP in NVSwitch)**: All-Reduce 등 집합 연산 시 데이터를 GPU 코어에서 처리하지 않고 NVSwitch 하드웨어 레지스터에서 직접 덧셈/리듀스를 수행하여 반환하는 기술.

</details>

- **PCIe 대비 최대 14배 이상 초고대역폭 제공**: NVLink 5세대(Blackwell) 기준 GPU당 양방향 1.8TB/s 대역폭 달성
- **단일 노드 내 완전 비차단 풀 메시(Full-Mesh)**: NVSwitch 패브릭을 통해 모든 GPU 간 1-홉(Hop) 직접 통신 보장
- **NCCL(NVIDIA Collective Communications Library) 최적화**: 토폴로지 자동 인식 기반으로 링(Ring) 및 트리(Tree) 알고리즘을 하드웨어 레벨에서 최적 스케줄링

#### 한줄 요약
- PCIe 대비 14배 대역폭, NVSwitch 기반 풀 메시 연결, 하드웨어 집합 연산 및 단일 메모리 풀을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NVLink 패브릭 관리자(Fabric Manager)**: NVSwitch 스위칭 라우팅 테이블을 프로그래밍하고 GPU 간의 메모리 접근 격리 및 장애 링크를 관리하는 시스템 데몬.

</details>

```text
[ GPU 0 (HBM3e) ] ── (NVLink 5 Port) ──┐                        ┌── (NVLink 5 Port) ── [ GPU 4 (HBM3e) ]
[ GPU 1 (HBM3e) ] ── (NVLink 5 Port) ──┼──▶ [ NVSwitch 패브릭 ] ◀──┼── (NVLink 5 Port) ── [ GPU 5 (HBM3e) ]
[ GPU 2 (HBM3e) ] ── (NVLink 5 Port) ──┤    (비차단 크로스바 스위치)  ├── (NVLink 5 Port) ── [ GPU 6 (HBM3e) ]
[ GPU 3 (HBM3e) ] ── (NVLink 5 Port) ──┘    (All-Reduce 가속 엔진)   └── (NVLink 5 Port) ── [ GPU 7 (HBM3e) ]
                                                       │
                                                       ▼ (단일 14.4TB/s 공유 메모리 도메인 형성)
                                          [ NCCL 텐서 병렬화 가속 엔진 ]
```

선의 의미: 8개의 GPU가 NVSwitch 패브릭을 통해 풀 메시로 결합되어 GPU 간 메모리 복사 없이 단일 공유 메모리 풀을 구성하는 스케일업 아키텍처

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **NVLink 인터페이스** | GPU 칩셋에 내장된 고속 차동 시그널링(PAM4) 물리 송수신기(PHY) 및 링크 컨트롤러 | Direct Point-to-Point |
| **NVSwitch ASIC** | 다수의 NVLink 포트를 임의의 GPU 간에 무충돌 라인 레이트로 교차 연결 | Crossbar Switch |
| **통합 메모리 제어기**| 타 GPU의 HBM 어드레스를 로컬 메모리처럼 주소 변환(Direct Load/Store) | Unified Memory |
| **패브릭 관리자 (FM)**| NVSwitch 라우팅 테이블 프로그래밍, 토폴로지 동적 구성 및 링크 오류 감시 | NVIDIA Fabric Manager |
| **NCCL 라이브러리** | All-Reduce, All-to-All 집합 연산을 NVLink 하드웨어 파이프라인에 1:1 매핑 | Collective Comm |

#### 한줄 요약
- NVLink 인터페이스, NVSwitch 크로스바, 통합 메모리 제어기, 패브릭 관리자, NCCL 라이브러리가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **토폴로지 인식 랭크 배치(Topology-Aware Rank Placement)**: NCCL이 GPU 간의 물리적 NVLink 링크 상태와 NVSwitch 연결 구조를 감지하여 텐서 병렬화 랭크(Rank)를 가장 가까운 GPU 쌍에 자동 매핑하는 기법.

</details>

```text
1. 시스템 초기화 시 패브릭 관리자(FM)가 GPU 및 NVSwitch 연결 상태를 탐색하여 비차단 크로스바 라우팅 설정
            │
            ▼
2. 딥러닝 프레임워크(PyTorch)가 NCCL 집합 통신(All-Reduce) 요청 트리거
            │
            ▼
3. NCCL이 NVSwitch 하드웨어 토폴로지를 인식하여 최적의 Ring / Tree 데이터 전송 경로 활성화
            │
            ▼
4. 각 GPU가 PCIe 및 CPU 개입 없이 NVLink 하드웨어를 통해 타 GPU의 HBM 메모리로 직접 DMA 전송
            │
            ▼
5. NVSwitch 하드웨어 가속기에서 텐서 합산(SHARP Reduction)을 동시 수행 ➔ 전 GPU에 동기화된 가중치 즉각 반환
```

**동작 원리**

1. **하드웨어 패브릭 수립**: NVSwitch가 8개~72개 GPU 간의 전용 고속 고밀도 버스 링크 활성화
2. **토폴로지 최적화**: NCCL이 홉 수가 최소화되는 텐서 교환 알고리즘(Ring/Tree) 자동 선택
3. **직접 메모리 액세스**: 송신 GPU가 수신 GPU의 HBM 주소에 100ns 이하 레이턴시로 데이터 직접 기록
4. **인패브릭 연산**: 단순 데이터 중계를 넘어 스위치 내부 연산 유닛에서 집합 덧셈 동시 수행
5. **초고속 동기화 완료**: 기존 InfiniBand/이더넷 대비 5~10배 빠른 속도로 텐서 병렬화 스텝 종료

#### 한줄 요약
- 패브릭 초기화, NCCL 토폴로지 인식, Ring/Tree 경로 수립, NVLink 직접 DMA 전송, 인패브릭 연산 완료 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NVLink 세대별 진화 및 PCIe/네트워크 비교**: 세대별 대역폭 발전 및 스케일업(NVLink)과 스케일아웃(InfiniBand/Ethernet)의 역할 분담 비교.

</details>

| 비교 항목 | NVLink 4 (Hopper H100) | NVLink 5 (Blackwell B200) | 범용 PCIe Gen5 | 스케일아웃 (InfiniBand NDR) |
|:---|:---|:---|:---|:---|
| **GPU당 양방향 대역폭**| **900 GB/s** | **1,800 GB/s (1.8 TB/s)** | **128 GB/s** | 100 GB/s (800Gbps Link) |
| **스위치 도메인 확장** | 단일 노드 8 GPU (NVLink Switch) | **단일 랙 72 GPU (NVL72)** | 단일 메인보드 8 Slot | 수만 대 노드 클러스터 |
| **통신 메커니즘** | **직접 HBM 로드/스토어 (SHMEM)** | **NVL72 랙 스케일 단일 메모리 풀**| PCIe 버스 호스트 DMA | RDMA 네트워크 패킷 전송 |
| **주요 적용 병렬화** | **텐서 병렬화 (Tensor Parallelism)**| **초거대 MoE / 텐서 병렬화** | 스토리지/NIC 연결 | **데이터 병렬화 (DP / PP)** |
| **지연 시간 (Latency)**| **$\le 100\text{ns}$ (초극저지연)** | **$\le 100\text{ns}$ (랙 스케일 극저지연)**| $\sim 1\mu\text{s}$ | $\sim 1\sim 2\mu\text{s}$ |

#### 한줄 요약
- NVLink 5는 1.8TB/s로 NVL72 랙 스케일 메모리 풀을 형성하며, 텐서 병렬화 극저지연 처리에 독점적 우위를 갖는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NVLink 단선 및 성능 디그레이션**: 특정 GPU 간 NVLink 차동 라인 접촉 불량이나 PHY 에러로 링크 대역폭이 절반으로 축소(Degraded)될 때 전체 클러스터 동기화 속도가 최저속 링크에 맞춰지는 병목 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 NVLink 차동 신호선 오류 시 링크 대역폭 반토막 및 클러스터 전체 훈련 지연 | **패브릭 관리자(FM) 기반 비트 에러 실시간 감시 및 동적 링 경로 재구성** | 불량 링크 조기 격리 및 통신 데드락 방지, 정상 훈련 지속 |
| 텐서 통신량이 많은 GPU 쌍이 NVSwitch 도메인 경계를 넘어 배치되어 병목 발생 | **NCCL 토폴로지 인식(Topology-Aware) 랭크 매핑 및 근접 GPU 우선 할당** | NVSwitch 간 홉 수 최소화 및 All-Reduce 통신 효율 30% 향상 |
| 고밀도 NVLink 스케일업(NVL72) 환경에서 랙 내부 과열로 인한 Thermal Throttling | **수랭식 직접 냉각(Direct-to-Chip Liquid Cooling) 및 열 분산 설계** | GPU 및 NVSwitch 쓰로틀링 방지, 100% 지속 최대 대역폭 보증 |

#### 한줄 요약
- FM 에러 감시로 경로를 재구성하고, 토폴로지 인식 배치로 홉을 줄이며, 액체 냉각으로 쓰로틀링을 방지한다.

## Ⅶ. 결론

- 수조 파라미터 거대 인공지능 모델의 분산 학습 및 실시간 추론을 가속하기 위해 **단일 노드/단일 랙 스케일업을 위한 NVLink 및 NVSwitch 패브릭**은 필수 불가결한 핵심 하드웨어 기술이며, 최근 NVL72 아키텍처를 통해 72개 GPU를 단일 거대 가상 GPU로 묶는 혁신을 달성하고, 스케일아웃 계층의 **InfiniBand/RoCEv2** 와 유기적으로 결합하여 초고성능 AI 팩토리 인프라를 완성

#### 한줄 요약
- NVLink와 NVSwitch를 통해 노드/랙 내부를 극저지연 공유 메모리로 묶고 스케일아웃 네트워크와 결합하여 대규모 AI 학습을 가속한다.
