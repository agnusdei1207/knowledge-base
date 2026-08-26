---
sidebar:
  order: 47
  label: "047. NVLink"
  badge:
    text: "기출 · 80%"
    variant: note
title: "NVLink"
date: "2026-08-26T10:45:00+09:00"
tags:
  - "notes-hardware"
weight: 47
extra:
  question_no: "047"
  source_status: "기출"
  source_history: "130회, 134회"
  priority: 80
  priority_note: "기출"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NVLink**: NVIDIA가 개발한 GPU-to-GPU 및 GPU-to-CPU 초고속 전용 양방향 직렬 인터커넥트 기술로, PCIe의 대역폭 한계와 지연시간을 극복.
- **NVSwitch**: 단일 서버 내부 또는 다중 노드에 탑재된 수십~수백 개의 GPU를 풀메시(Full-Mesh) 비차단 크로스바로 연결하는 전용 고속 스위칭 ASIC.

</details>

- 정의/개념: GPU 간 직접 메모리 접근(P2P)과 대규모 데이터 전송을 위해 PCIe 버스 병목을 극복한 **초고대역폭·초저지연 독자 인터커넥트 기술**
- 배경/필요성: 기존 PCIe 대역폭 한계로 다중 GPU 간 **대규모 텐서 교환** 병목 극복

#### 한줄 요약
- NVLink는 GPU 간 직접 메모리 접근(P2P)과 초당 수 테라바이트 대역폭을 제공하여 단일 노드 내 다중 GPU를 거대 단일 GPU처럼 묶는 초고속 인터커넥트이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **단일 주소 공간(Unified Memory / Single Address Space)**: 여러 GPU의 물리적 HBM 메모리를 하나의 연속된 가상 메모리 공간으로 매핑하여 P2P 직접 읽기/쓰기를 지원하는 기술.
- **SHARP(Scalable Hierarchical Aggregation and Reduction Protocol)**: All-Reduce 등의 집단 통신 연산을 GPU 코어가 아닌 NVSwitch 내부 하드웨어 연산기에서 직접 처리하는 오프로딩 기술.

</details>

- 초고대역폭 및 저지연: 세대별 발전을 통해 GPU당 수백 GB/s~수 TB/s(NVLink 5세대 기준 **1.8 TB/s**) 대역폭과 수십 나노초대 지연시간 달성
- NVSwitch 기반 풀메시 확장: 단일 노드 내 다수의 GPU를 비차단 크로스바 스위치망으로 결합하여 **단일 거대 GPU 메모리 풀(Unified Memory Pool)**처럼 운용
- 하드웨어 가속 집단 통신: **SHARP(Scalable Hierarchical Aggregation and Reduction Protocol)**를 통해 All-Reduce 연산을 스위치 ASIC 내부에서 직접 수행

#### 한줄 요약
- 1.8 TB/s 초고대역폭과 NVSwitch 풀메시 크로스바를 통해 GPU 메모리를 완전 통합하고 집단 통신을 하드웨어로 가속한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SerDes(Serializer/Deserializer)**: 병렬 데이터를 초고속 직렬 비트 스트림으로 변환하여 물리 케이블 및 기판 패턴으로 고속 전송하는 물리 계층 송수신기.
- **NCCL(NVIDIA Collective Communications Library)**: NVLink 및 NVSwitch 하드웨어 토폴로지를 자동 인식하여 All-Reduce 집단 통신을 극대화하는 소프트웨어 라이브러리.

</details>

```text
[NVIDIA DGX 노드 스케일업 아키텍처]
 ├─ NVSwitch 패브릭 (크로스바 스위칭망)
 │   ├─ SerDes PHY 물리 계층 (PAM4 차동 신호)
 │   └─ NVLink 초고속 양방향 포트 어레이
 ├─ GPU 가속기 엔드포인트군 (GPU 0~7)
 │   ├─ 연산 코어 및 온칩 HBM3 메모리
 │   └─ NVLink 전용 P2P 통신 컨트롤러
 ├─ NCCL 집단 통신 소프트웨어 라이브러리
 └─ 호스트 CPU 및 PCIe 제어 버스
```

선의 의미: 가지(`├─`, `└─`)는 하드웨어 소속 및 포함 관계를 나타냄

| 구성요소 | 소속 및 위치 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|:---|
| GPU 엔드포인트 | 가속기 다이 | 대규모 텐서 연산 수행 및 **NVLink P2P 패킷 송수신** | HBM3 메모리 직결 |
| SerDes 물리 계층 | 칩 경계 PHY | PAM4 고속 차동 신호 변환 및 **물리 전송** | 초저에너지 (pJ/bit) |
| NVSwitch 칩 | 서버 백플레인 기판 | 다중 GPU 간 **비차단 풀메시 크로스바 라우팅** | 초당 수십 TB/s 스위칭 |
| NCCL 라이브러리 | 통신 소프트웨어 계층 | 물리 토폴로지 자동 탐색 및 **All-Reduce 집단 통신 최적화** | 링/트리 집단 통신 |
| 호스트 CPU / PCIe | 시스템 제어 계층 | OS 부팅, 드라이버 초기화 및 스토리지 데이터 로딩 | 제어 플레인 담당 |

#### 한줄 요약
- NVLink 시스템은 GPU 엔드포인트(SerDes), NVSwitch 크로스바 패브릭, NCCL 통신 라이브러리 및 호스트 제어 계층으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **All-Reduce**: 각 GPU가 계산한 그래디언트를 합산(Reduce)한 뒤, 최종 결과를 모든 참여 GPU에 동일하게 복제 분배(Broadcast)하는 집단 통신 연산.

</details>

```text
[역전파 연산 완료 및 그래디언트 도출]
         │
         ▼
1. NCCL 라이브러리의 물리 토폴로지 자동 감지
         │
         ▼
2. NVLink 기반 GPU 간 P2P 패킷 직접 발행
         │
         ▼
3. NVSwitch 크로스바 스위칭 및 메모리 직결 라우팅
         │
         ▼
4. 노드 간 분산 시 InfiniBand RDMA 연계 전송
         │
         ▼
5. GPU 간 그래디언트 All-Reduce 집단 통신 완료
         │
         ▼
[다음 분산 학습 스텝 개시]
```

분기 결과: 노드 내부 GPU 간 통신은 NVLink와 NVSwitch를 통해 초당 테라바이트급으로 완료되며, 노드 간 통신은 **InfiniBand RDMA**와 연계됨

#### 한줄 요약
- 1. 토폴로지 감지 ➔ 2. P2P 패킷 발행 ➔ 3. NVSwitch 직결 라우팅 ➔ 4. 노드 간 연계 ➔ 5. All-Reduce 완료 순으로 동작한다.

## Ⅴ. 종류 및 비교

| 인터커넥트 기술 | NVIDIA NVLink (v4 / v5) | PCIe Gen5 / Gen6 | CXL.mem | InfiniBand (RDMA) |
|:---|:---|:---|:---|:---|
| 연결 범위 | **단일 노드 내 다중 GPU (스케일업)** | 단일 노드 내 범용 장치 | 단일 노드/랙 내 메모리 풀링 | **노드 간 대규모 클러스터 (스케일아웃)** |
| 양방향 대역폭 | **초고대역폭 (GPU당 900GB/s ~ 1.8TB/s)** | 보통 (x16 기준 64GB/s ~ 128GB/s) | 고속 (x16 기준 64GB/s+) | 초고속 (400Gbps ~ 800Gbps) |
| 지연시간 (Latency) | **초저지연 (수십 ns 수준)** | 보통 (수백 ns) | 저지연 (150~200ns) | 마이크로초 ($sim 1mu	ext{s}$) |
| 캐시 일관성 / P2P | **하드웨어 GPU P2P 완벽 지원** | 제한적 P2P (일관성 없음) | **하드웨어 캐시 일관성 지원** | 메모리 직접 접근(RDMA) |
| 생태계 및 표준화 | **NVIDIA 독점 규격 (GPU 최적화)** | PCI-SIG 개방형 범용 표준 | CXL 컨소시엄 개방형 표준 | IBTA 개방형 고성능 표준 |

#### 한줄 요약
- 단일 노드 내 초고속 GPU 스케일업에는 NVLink가 독보적이며, 노드 간 대규모 클러스터 스케일아웃 네트워킹에는 InfiniBand가 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **통신-연산 오버랩(Communication-Computation Overlap)**: 후속 레이어 역전파 연산을 수행하는 동안 선행 레이어의 그래디언트를 NVLink로 비동기 전송하는 파이프라이닝 기법.

</details>

| 문제 상황 | 대책 | 엔지니어링 효과 |
|:---|:---|:---|
| All-Reduce 통신 대기로 연산 유휴 | **통신-연산 오버랩** 및 텐서 버킷팅 | 지연시간 **100% 은닉** |
| 8개 GPU 고밀도 집적으로 발열 급증 | **칩 직접 수랭식(Liquid Cooling)** 구축 | 열 스로틀링 방지 및 **클록 유지** |
| 멀티 노드 확장 시 대역폭 불균형 | **노드 내 텐서 병렬화** 및 노드 간 파이프라인 분할 | 클러스터 **확장 효율 90% 사수** |

#### 한줄 요약
- 실무에서는 통신-연산 오버랩으로 지연을 은닉하고, 수랭 냉각으로 발열을 제어하며, 하이브리드 병렬화로 노드 간 병목을 극복한다.

## Ⅶ. 결론

- **다중 GPU 스케일업** 요구 시 **NVLink**와 NVSwitch 기반 패브릭 구축

#### 한줄 요약
- NVLink는 GPU 간 초고대역폭 직접 통신을 실현하는 AI 스케일업의 핵심이며, NVSwitch 및 NCCL과의 결합으로 초거대 모델 병렬화를 완성한다.
