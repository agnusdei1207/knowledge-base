---
sidebar:
  order: 104
  label: "104. InfiniBand 클러스터 인터커넥트"
  badge:
    text: "기출 · 50%"
    variant: note
title: "초고성능 슈퍼컴퓨팅 인터커넥트 : 인피니밴드 클러스터"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 104
extra:
  question_no: "104"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "IBTA 표준, HCA, 서브넷 관리자(Subnet Manager), 크레딧 기반 흐름 제어(Credit-Based), Fat-Tree 토폴로지"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **InfiniBand (인피니밴드)**: HPC 및 초대형 AI 클러스터에서 서브 마이크로초 지연과 테라비트 대역폭을 제공하는 IBTA 표준 인터커넥트.
- **Subnet Manager (서브넷 관리자, SM)**: 서브넷 내의 모든 HCA와 스위치를 탐색하여 16비트 LID를 할당하고 최적 포워딩 테이블(LFT)을 배포하는 중앙 제어기.

</details>

- 정의/개념: 서버 HCA와 전용 스위치를 점대점 직결하여 **하드웨어 크레딧 기반 무손실 흐름 제어, 컷스루 스위칭, 서브넷 관리자(SM) 라우팅을 제공하는 슈퍼컴퓨팅 인터커넥트**
- 배경/필요성: 표준 이더넷의 소프트웨어 스택 오버헤드 및 버퍼 지연으로 인한 **연산 노드 간 통신 병목, 테일 레이턴시(Tail Latency) 급증 및 확장성 붕괴**

#### 한줄 요약
- 하드웨어 크레딧 기반 무손실 흐름 제어, 컷스루 스위칭, 중앙 서브넷 관리자를 통해 극한의 클러스터 성능을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Credit-Based Flow Control**: 수신단 버퍼에 여유 공간이 있을 때만 송신단에 토큰(Credit)을 부여하여 하드웨어 레벨에서 패킷 드롭을 원천 차단하는 흐름 제어.
- **Cut-Through Switching**: 패킷 전체를 수신할 때까지 기다리지 않고 헤더의 목적지 LID만 확인하는 즉시 100ns 내에 출력 포트로 밀어내는 고속 포워딩.

</details>

- **하드웨어 크레딧 기반 절대 무손실(Lossless)**: 수신 버퍼 여유 크레딧 범위 내에서만 패킷을 송출하여 **패킷 폐기 0% 보장**
- **초저지연 컷스루(Cut-Through) 스위칭**: 패킷 전체 버퍼링 없이 목적지 LID 헤더 확인 즉시 **100ns 단위 초고속 포워딩**
- **서브넷 관리자(SM) 기반 중앙 최적화**: 분산 라우팅 프로토콜 없이 **중앙 SM이 Fat-Tree 비차단(Non-Blocking) 최적 경로 일괄 주입**

#### 한줄 요약
- 크레딧 기반 무손실, 컷스루 초저지연 스위칭, 서브넷 관리자 중앙 최적 경로 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **HCA (Host Channel Adapter)**: 호스트의 PCIe Gen5 버스와 인피니밴드 광 링크를 연결하여 RDMA 전송을 가속하는 전용 어댑터 (Mellanox ConnectX).
- **Fat-Tree Topology**: 스파인 계층으로 갈수록 링크 대역폭을 비례 확장하여 모든 노드 간 1:1 전대역폭(Non-Blocking) 통신을 보장하는 구조.

</details>

```text
[인피니밴드 Fat-Tree 클러스터 토폴로지]
|-- Compute Nodes (GPU HCA 어댑터: ConnectX-7, RDMA 큐 페어)
|-- Storage Nodes (NVMe-oF 스토리지 타깃 HCA)
`-- InfiniBand Switch Fabric (Fat-Tree Non-Blocking Topology)
    |-- Leaf Switches (400G NDR / 800G XDR OSFP 포트)
    |-- Spine Switches (1:1 풀 바이섹션 대역폭 보증)
    |-- Virtual Lanes (VL0~VL15 QoS 버퍼 격리)
    `-- Hardware Credit Engine (링크별 크레딧 동기화 & 컷스루 스위칭)
`-- Master Subnet Manager (OpenSM: 전체 토폴로지 탐색, LID 할당, LFT 주입)
```

선의 의미: 컴퓨트 노드와 스토리지 노드가 Fat-Tree 인피니밴드 스위치를 통해 연결되고 서브넷 관리자가 패브릭 전체의 주소와 경로를 중앙 제어하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **HCA (Host Channel Adapter)** | PCIe Gen5 버스와 광 링크를 연결하는 **RDMA 통신 하드웨어 가속기** | ConnectX-7 |
| **인피니밴드 스위치** | **컷스루 패킷 스위칭, LFT 기반 LID 포워딩, 크레딧 반환 처리** | Quantum-2 (400G) |
| **서브넷 관리자 (SM)** | 패브릭 내 노드 탐색, **16bit LID 할당, 비차단 최적 라우팅 경로 주입** | OpenSM |
| **가상 레인 (VL)** | 물리 링크를 **복수의 논리적 큐로 분할하여 우선순위 지정 및 버퍼 격리**| 8~16 VLs |
| **파티션 키 (P_Key)** | 멀티 테넌트 간 통신 차단 및 **특정 연산 노드 풀 가상 격리** | 16bit P_Key |

#### 한줄 요약
- HCA 어댑터, Fat-Tree 스위치 패브릭, 서브넷 관리자(SM), 가상 레인(VL), 파티션 키(P_Key)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **LFT (Linear Forwarding Table)**: SM이 각 스위치 ASIC에 프로그래밍하는 정적 포워딩 테이블로, 패킷의 16비트 LID를 기반으로 출력 포트를 즉시 결정함.

</details>

```text
인피니밴드 SM 탐색, 크레딧 동기화 및 컷스루 전송 파이프라인
        │
   1. [SM 토폴로지 자동 탐색] 서브넷 관리자(SM)가 SMP 패킷을 송출하여 전체 스위치와 HCA 탐색
        │
   2. [LID 할당 및 LFT 주입] Fat-Tree 라우팅을 연산하여 HCA 포트에 LID를 할당하고 스위치 LFT 주입
        │
   3. [가용 버퍼 크레딧 획득] 송신 HCA가 스위치 포트로부터 하드웨어 Flow Control 크레딧 수신
        │
   4. [컷스루 RDMA 송출] 보유 크레딧 내에서 패킷 송출 ➔ 스위치가 100ns 내 컷스루 포워딩
        │
   ▼
5. [크레딧 반환 및 무손실 완수] 수신단이 패킷 처리 후 신규 크레딧을 송신단으로 반환하여 무손실 완료
```

#### 한줄 요약
- SM 토폴로지 탐색 → LID/LFT 주입 → 크레딧 획득 → 컷스루 무손실 전송 → 크레딧 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HDR vs NDR vs XDR vs GDR**: 대역폭 진화에 따른 4X 링크 전송 속도 표준 규격.

</details>

| 속도 세대 (Generation) | 레인당 속도 (Lane Rate) | 4X 링크 총 대역폭 | 인코딩 방식 | 상용화 시점 |
|:---|:---|:---|:---|:---|
| **HDR (High Data Rate)** | **50 Gbps (PAM4)** | **200 Gbps** | 64b/66b | 2018년 |
| **NDR (Next Data Rate)** | **100 Gbps (PAM4)** | **400 Gbps** | PAM4 + RS-FEC | 2022년 (H100 표준) |
| **XDR (eXtreme Data Rate)**| **200 Gbps (PAM4)** | **800 Gbps** | PAM4 + RS-FEC | 2024~2025년 (B200) |
| **GDR (Giga Data Rate)** | **400 Gbps (PAM4/광)** | **1,600 Gbps (1.6 Tbps)** | 차세대 광인터커넥트 | 차세대 로드맵 |

#### 한줄 요약
- HDR 200G, NDR 400G, XDR 800G로 진화하며 고밀도 PAM4 변조와 FEC 기술을 통해 대역폭을 극대화한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SHARP (Scalable Hierarchical Aggregation and Reduction Protocol)**: All-Reduce 집계 연산을 GPU가 아닌 인피니밴드 스위치 ASIC 하드웨어에서 직접 수행하여 통신 트래픽을 50% 절감하는 인네트워크 컴퓨팅 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 서브넷 관리자(SM) 장애 시 신규 노드 인식 불가 및 제어 평면 마비 | **`마스터-스탠바이 SM 이중화(OpenSM HA)` 구성 및 주기적 하트비트** | 마스터 장애 시 1초 내 자동 페일오버 및 제어 가용성 확보 |
| 대규모 All-Reduce 통신 시 상위 스파인 스위치 병목으로 성능 저하 | **`Fat-Tree 1:1 Non-Blocking 풀 바이섹션 대역폭` 및 SHARP 기술** | 스파인 병목 제거 및 초대규모 GPU 클러스터 통신 효율 100% 보장 |
| 광모듈 열화로 인한 비트 에러(BER) 발생 및 링크 플래핑 | **`스위치 포트 BER 모니터링 및 자동 격리(Port Auto-Disable)`** | 불량 링크 조기 격리 및 전체 클러스터 테일 레이턴시 방어 |
| 케이블 오결선으로 인한 Fat-Tree 토폴로지 불균형 발생 | **`토폴로지 검증 툴(ibnetdiscover / ibdiagnet)` 자동화 점검** | 물리 결선 오류 100% 사전 검출 및 정상 대역폭 확보 |

#### 한줄 요약
- SM 이중화로 제어 가용성을 확보하고, 1:1 Fat-Tree로 병목을 제거하며, BER 모니터링으로 불량 링크를 격리한다.

## Ⅶ. 결론

- 글로벌 최상위 슈퍼컴퓨터 및 초대형 프론티어 AI 학습 인프라 구축을 위해 **InfiniBand 아키텍처를 인터커넥트 표준으로 채택**하되, 실무 구축 시 **1:1 비차단 Fat-Tree 토폴로지 설계, 서브넷 관리자(SM) 고가용성 이중화, NVIDIA GPUDirect RDMA 및 SHARP(인네트워크 연산)** 기술을 통합 적용하여 극한의 연산 가속 인프라 완성

#### 한줄 요약
- InfiniBand는 크레딧 기반 무손실 제어와 Fat-Tree 토폴로지 및 SM 이중화를 통해 초고성능 AI 클러스터를 실현하는 표준 인터커넥트다.