---
sidebar:
  order: 105
  label: "105. NVLink 고대역폭 인터커넥트"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초고속 GPU 스케일업 인터커넥트 : NVLink 및 NVSwitch"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
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

- **NVLink**: GPU 간(GPU-to-GPU) 초고속 데이터 교환을 위한 NVIDIA 전용 점대점 직렬 인터커넥트.
- **NVSwitch**: 단일 노드 또는 단일 랙 내에서 다수의 GPU를 완전 비차단 풀 메시로 연결하는 스위칭 칩셋.

</details>

- 정의/개념: 복수 GPU 간에 HBM 메모리를 단일 공유 메모리 풀로 묶어 **최대 1.8TB/s의 양방향 대역폭과 100ns 극저지연을 제공하는 초고속 스케일업 인터커넥트 기술**
- 배경/필요성: 범용 PCIe Gen5 버스 대역폭(128GB/s) 한계로 인한 **거대 모델 텐서 병렬화(TP) 시 통신 병목, GPU 연산 코어 유휴 및 분산 학습 속도 저하**

#### 한줄 요약
- PCIe 대비 14배 이상의 대역폭, NVSwitch 비차단 풀 메시, 단일 공유 메모리 풀을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Unified Shared Memory Pool (통합 공유 메모리 풀)**: 타 GPU의 HBM에 로컬 로드/스토어 명령(Direct Access)으로 직접 접근할 수 있도록 묶어주는 단일 메모리 도메인.
- **NCCL (NVIDIA Collective Communications Library)**: All-Reduce, All-to-All 집합 연산을 NVLink 하드웨어 토폴로지에 최적화하여 가속하는 통신 라이브러리.

</details>

- **PCIe 대비 14배 이상의 극대화된 대역폭**: GPU당 최대 **1.8TB/s(NVLink 5) 양방향 전송 속도 달성**
- **단일 노드/랙 내 완전 비차단 풀 메시(Full-Mesh)**: NVSwitch 패브릭을 통해 **모든 GPU 간 1-홉(Hop) 직접 통신 보장**
- **NCCL 집합 통신 하드웨어 가속**: 토폴로지 자동 인식 기반으로 **Ring 및 Tree 알고리즘을 하드웨어 파이프라인에서 가속**

#### 한줄 요약
- 초대역폭 전송, NVSwitch 기반 풀 메시 연결, 하드웨어 집합 연산 및 단일 메모리 풀을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Fabric Manager (패브릭 관리자)**: NVSwitch 라우팅 테이블을 프로그래밍하고 GPU 간 메모리 접근 격리 및 장애 링크를 관리하는 시스템 데몬.

</details>

```text
[NVLink 및 NVSwitch 풀 메시 스케일업 토폴로지]
|-- GPU 0~3 (HBM3e 고대역폭 메모리, NVLink 5 포트)
`-- NVSwitch Fabric (비차단 크로스바 스위치, All-Reduce 하드웨어 축약 엔진)
|   |-- Unified Memory Controller (타 GPU HBM 직접 주소 변환: Direct Load/Store)
|   `-- Fabric Manager (라우팅 테이블 프로그래밍, 토폴로지 동적 구성, 링크 감시)
`-- GPU 4~7 (HBM3e 고대역폭 메모리, NVLink 5 포트)
`-- NCCL Acceleration Engine (단일 14.4TB/s 공유 메모리 도메인 기반 텐서 병렬화)
```

선의 의미: 8개의 GPU가 NVSwitch 패브릭을 통해 풀 메시로 결합되어 GPU 간 메모리 복사 없이 단일 공유 메모리 풀을 구성하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **NVLink 인터페이스** | GPU 내장 고속 차동 시그널링(PAM4) **물리 송수신기(PHY) 및 링크 컨트롤러** | Point-to-Point |
| **NVSwitch ASIC** | 다수의 NVLink 포트를 **임의의 GPU 간에 무충돌 라인 레이트로 교차 연결** | Crossbar Switch |
| **통합 메모리 제어기**| 타 GPU의 HBM 어드레스를 **로컬 메모리처럼 주소 변환(Direct Load/Store)** | Unified Memory |
| **패브릭 관리자 (FM)**| **NVSwitch 라우팅 테이블 프로그래밍, 토폴로지 동적 구성 및 링크 감시** | Fabric Manager |
| **NCCL 라이브러리** | All-Reduce, All-to-All 집합 연산을 **NVLink 하드웨어 파이프라인에 1:1 매핑**| Collective Comm |

#### 한줄 요약
- NVLink 인터페이스, NVSwitch 크로스바, 통합 메모리 제어기, 패브릭 관리자, NCCL 라이브러리가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Topology-Aware Rank Mapping**: NCCL이 물리적 NVLink 링크 상태와 NVSwitch 연결 구조를 감지하여 텐서 병렬화 랭크(Rank)를 가장 가까운 GPU 쌍에 자동 매핑하는 기법.

</details>

```text
NVLink 패브릭 초기화, NCCL 경로 매핑 및 All-Reduce 전송 파이프라인
        │
   1. [패브릭 초기화] 패브릭 관리자(FM)가 GPU 및 NVSwitch 연결을 탐색하여 크로스바 라우팅 설정
        │
   2. [집합 통신 호출] 딥러닝 프레임워크(PyTorch)가 NCCL All-Reduce 요청 트리거
        │
   3. [토폴로지 최적 경로 선택] NCCL이 NVSwitch 하드웨어를 인식하여 최적 Ring/Tree 데이터 경로 활성화
        │
   4. [직접 DMA 전송] 각 GPU가 PCIe/CPU 개입 없이 NVLink를 통해 타 GPU의 HBM으로 직접 DMA 송출
        │
   ▼
5. [인패브릭 연산 완결] NVSwitch 가속기에서 텐서 합산을 동시 수행하여 전 GPU에 동기화 가중치 반환
```

#### 한줄 요약
- 패브릭 초기화 → NCCL 토폴로지 인식 → Ring/Tree 경로 수립 → NVLink 직접 DMA 전송 → 인패브릭 연산 완료 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NVLink 4 vs NVLink 5 vs PCIe Gen5 vs InfiniBand NDR**: 스케일업(NVLink)과 스케일아웃(InfiniBand)의 대역폭 및 지연 시간 비교.

</details>

| 비교 항목 | NVLink 4 (Hopper H100) | NVLink 5 (Blackwell B200) | 범용 PCIe Gen5 | 스케일아웃 (InfiniBand NDR) |
|:---|:---|:---|:---|:---|
| **GPU당 양방향 대역폭**| **900 GB/s** | **1,800 GB/s (1.8 TB/s)** | **128 GB/s** | 100 GB/s (800Gbps Link) |
| **스위치 도메인 확장** | 단일 노드 8 GPU | **단일 랙 72 GPU (NVL72)** | 단일 메인보드 8 Slot | 수만 대 노드 클러스터 |
| **통신 메커니즘** | **직접 HBM 로드/스토어 (SHMEM)**| **NVL72 랙 스케일 단일 메모리 풀**| PCIe 버스 호스트 DMA | RDMA 네트워크 패킷 전송 |
| **주요 적용 병렬화** | **텐서 병렬화 (Tensor Parallelism)**| **초거대 MoE / 텐서 병렬화** | 스토리지/NIC 연결 | **데이터 병렬화 (DP / PP)** |
| **지연 시간 (Latency)**| **$\le 100\text{ns}$ (초극저지연)** | **$\le 100\text{ns}$ (랙 스케일 극저지연)**| $\sim 1\mu\text{s}$ | $\sim 1\sim 2\mu\text{s}$ |

#### 한줄 요약
- NVLink 5는 1.8TB/s로 NVL72 랙 스케일 메모리 풀을 형성하며, 텐서 병렬화 극저지연 처리에 독점적 우위를 갖는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Degraded Link (링크 대역폭 감쇄)**: 차동 신호선 물리적 결함 시 NVLink 대역폭이 50%로 축소되어 전체 All-Reduce 동기화 속도가 최저속 링크로 병목화되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 NVLink 차동 신호선 오류 시 링크 대역폭 반토막 및 훈련 지연 | **패브릭 관리자(FM) 기반 `비트 에러 실시간 감시 및 동적 경로 재구성`** | 불량 링크 조기 격리 및 데드락 방지, 정상 훈련 지속 |
| 텐서 통신량이 많은 GPU 쌍이 NVSwitch 도메인 경계를 넘어 배치 | **NCCL `토폴로지 인식(Topology-Aware) 랭크 매핑` 및 근접 할당** | NVSwitch 간 홉 수 최소화 및 통신 효율 30% 향상 |
| 고밀도 NVLink 스케일업(NVL72) 환경에서 과열로 인한 쓰로틀링 | **`수랭식 직접 냉각(Direct-to-Chip Liquid Cooling)` 및 열 분산 설계** | GPU 및 NVSwitch 열 쓰로틀링 방지 및 최대 대역폭 보증 |
| 다중 노드 통신 시 NVLink와 InfiniBand 간 속도 불균형 병목 | **`계층적 All-Reduce (노드 내 NVLink + 노드 간 InfiniBand)`** 적용 | 랙 간 스케일아웃 네트워크 오버헤드 극소화 |

#### 한줄 요약
- FM 에러 감시로 경로를 재구성하고, 토폴로지 인식 배치로 홉을 줄이며, 액체 냉각으로 쓰로틀링을 방지한다.

## Ⅶ. 결론

- 수조 파라미터 거대 인공지능 모델의 분산 학습 및 실시간 추론을 가속하기 위해 **단일 노드/단일 랙 스케일업을 위한 NVLink 및 NVSwitch 패브릭을 핵심 인터커넥트로 채택**하되, NVL72 아키텍처를 통해 72개 GPU를 단일 거대 가상 GPU 메모리 풀로 묶고, 스케일아웃 계층의 **InfiniBand/RoCEv2**와 유기적으로 결합하여 초고성능 AI 팩토리 인프라 완성

#### 한줄 요약
- NVLink와 NVSwitch는 노드/랙 내부를 극저지연 공유 메모리로 결합하여 대규모 AI 모델의 텐서 병렬화를 가속하는 핵심 하드웨어 기술이다.