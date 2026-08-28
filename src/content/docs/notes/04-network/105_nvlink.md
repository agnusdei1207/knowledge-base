---
sidebar:
  order: 105
  label: "105. NVLink 고대역폭 인터커넥트"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초고속 GPU 스케일업 인터커넥트 : NVLink 및 NVSwitch"
date: "2026-08-26T14:15:01+09:00"
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

- 정의/개념: GPU HBM을 공유 풀로 묶는 **고대역폭 스케일업 인터커넥트**
- 배경/필요성: PCIe로 GPU를 잇는 방식은 텐서 병렬 통신마다 **제한된 대역폭과 그로 인한 GPU 유휴 시간**을 치르므로, GPU 사이에 전용 고대역 링크와 스위치를 두어 서로의 메모리를 직접 참조하게 함

#### 한줄 요약
- PCIe 대비 14배 이상의 대역폭, NVSwitch 비차단 풀 메시, 단일 공유 메모리 풀을 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Unified Shared Memory Pool (통합 공유 메모리 풀)**: 타 GPU의 HBM에 로컬 로드/스토어 명령(Direct Access)으로 직접 접근할 수 있도록 묶어주는 단일 메모리 도메인.
- **NCCL (NVIDIA Collective Communications Library)**: All-Reduce, All-to-All 집합 연산을 NVLink 하드웨어 토폴로지에 최적화하여 가속하는 통신 라이브러리.

</details>

- **NVLink 5 대역폭**: GPU당 양방향 1.8TB/s 제공
- **NVSwitch 풀 메시**: 모든 GPU 사이 1홉 통신
- **NCCL 가속**: 토폴로지 기반 Ring·Tree 경로 선택

#### 한줄 요약
- 초대역폭 전송, NVSwitch 기반 풀 메시 연결, 하드웨어 집합 연산 및 단일 메모리 풀을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Fabric Manager (패브릭 관리자)**: NVSwitch 라우팅 테이블을 프로그래밍하고 GPU 간 메모리 접근 격리 및 장애 링크를 관리하는 시스템 데몬.

</details>

```text
[NVLink 정적 구성]
|-- NVLink 인터페이스
|-- NVSwitch ASIC
|-- 통합 메모리 제어기
|-- 패브릭 관리자
`-- NCCL 라이브러리
```

선의 의미: 8개의 GPU가 NVSwitch 패브릭을 통해 풀 메시로 결합되어 GPU 간 메모리 복사 없이 단일 공유 메모리 풀을 구성하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| NVLink 인터페이스 | **PAM4 PHY·링크 제어** | Point-to-Point |
| NVSwitch ASIC | **GPU 간 비차단 교차 연결** | Crossbar Switch |
| 통합 메모리 제어기 | **원격 HBM 주소 변환** | Unified Memory |
| 패브릭 관리자 | **라우팅·토폴로지·링크 관리** | Fabric Manager |
| NCCL 라이브러리 | **집합 연산 경로 최적화** | Collective Comm |

#### 한줄 요약
- NVSwitch 크로스바가 GPU 쌍마다 필요하던 직접 연결을 대신하므로, GPU 수가 늘어도 임의의 두 GPU 사이 홉 수는 일정하게 유지된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Topology-Aware Rank Mapping**: NCCL이 물리적 NVLink 링크 상태와 NVSwitch 연결 구조를 감지하여 텐서 병렬화 랭크(Rank)를 가장 가까운 GPU 쌍에 자동 매핑하는 기법.

</details>

```text
프레임워크 요청
    |
1. 패브릭 초기화
    |
2. NCCL 집합 통신 호출
    |
3. 토폴로지 경로 선택
    |
4. NVLink 직접 DMA
    |
5. 인패브릭 연산
    |
동기화 결과
```

- 1. 패브릭 초기화
- 2. NCCL 집합 통신 호출
- 3. 토폴로지 경로 선택
- 4. NVLink 직접 DMA
- 5. 인패브릭 연산

#### 한줄 요약
- NCCL이 토폴로지를 먼저 인식해 경로를 정하므로, 같은 집합 연산이라도 배치가 어긋나면 대역폭이 아니라 홉 수에서 손실이 발생한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NVLink 4 vs NVLink 5 vs PCIe Gen5 vs InfiniBand NDR**: 스케일업(NVLink)과 스케일아웃(InfiniBand)의 대역폭 및 지연 시간 비교.

</details>

| 비교 항목 | NVLink 4 (Hopper H100) | NVLink 5 (Blackwell B200) | 범용 PCIe Gen5 | 스케일아웃 (InfiniBand NDR) |
|:---|:---|:---|:---|:---|
| GPU당 양방향 대역폭 | **900 GB/s** | **1.8 TB/s** | **128 GB/s** | 100 GB/s |
| 스위치 도메인 확장 | 8 GPU | **NVL72** | 8 Slot | 다수 노드 |
| 통신 메커니즘 | **HBM 직접 접근** | **랙 공유 메모리** | 호스트 DMA | RDMA 패킷 |
| 주요 적용 병렬화 | **텐서 병렬화** | **MoE·텐서 병렬화** | I/O 연결 | **데이터 병렬화** |
| 지연 시간 | **100ns 이하** | **100ns 이하** | 약 1μs | 약 1~2μs |

#### 한줄 요약
- NVLink 5는 1.8TB/s로 NVL72 랙 스케일 메모리 풀을 형성하며, 텐서 병렬화 극저지연 처리에 독점적 우위를 갖는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Degraded Link (링크 대역폭 감쇄)**: 차동 신호선 물리적 결함 시 NVLink 대역폭이 50%로 축소되어 전체 All-Reduce 동기화 속도가 최저속 링크로 병목화되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 링크 오류에 따른 대역폭 저하 | **FM 오류 감시·경로 재구성** | 불량 링크 격리 |
| GPU 랭크의 원거리 배치 | **NCCL 토폴로지 인식 매핑** | 홉 수 최소화 |
| NVL72 과열·쓰로틀링 | **직접 수랭·열 분산** | 최대 대역폭 유지 |
| NVLink·InfiniBand 속도 불균형 | **계층적 All-Reduce** | 노드 간 부하 절감 |

#### 한줄 요약
- FM 에러 감시로 경로를 재구성하고, 토폴로지 인식 배치로 홉을 줄이며, 액체 냉각으로 쓰로틀링을 방지한다.

## Ⅶ. 결론

- 노드·랙 스케일업은 **NVLink·NVSwitch**, 노드 간은 **InfiniBand·RoCEv2** 선택

#### 한줄 요약
- NVLink와 NVSwitch는 노드/랙 내부를 극저지연 공유 메모리로 결합하여 대규모 AI 모델의 텐서 병렬화를 가속하는 핵심 하드웨어 기술이다.
