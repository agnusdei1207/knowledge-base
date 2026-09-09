---
sidebar:
  order: 47
  label: "047. NVLink"
  badge:
    text: "기출 · 80%"
    variant: note
title: "NVLink"
date: "2026-09-07T09:40:00+09:00"
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
- 배경/필요성: 표준 PCIe 버스의 대역폭 한계 및 호스트 CPU 경유 통신으로 인한 **GPU 간 텐서 동기화 지연과 분산 학습 확장성 병목 한계 극복 및 GPU 간 직접 메모리 공유 체계 확립 필요성 증대**

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
[NVLink 노드 스케일업 아키텍처]
  │
  ├─ [NVSwitch 패브릭 서브시스템] (비차단 크로스바 ASIC)
  │     ├─ [초고속 SerDes PHY] (PAM4 직렬 고주파 인터페이스)
  │     └─ [SHARP 연산 가속기] (All-Reduce 인네트워크 연산)
  │
  ├─ [NVLink 직렬 연결망] (초고속 P2P 양방향 데이터 경로)
  │
  ├─ [다중 GPU 엔드포인트군] (GPU 0 ~ GPU N)
  │     ├─ [통합 HBM 메모리 풀] (글로벌 단일 가상 주소 공간)
  │     └─ [NVLink P2P 컨트롤러] (호스트 우회 메모리 직접 전송)
  │
  └─ [호스트 시스템 제어부] (PCIe 버스 연결)
        ├─ [호스트 CPU 및 DRAM] (부팅 제어 및 외부 통신 관리)
        └─ [NCCL 런타임] (하드웨어 토폴로지 인식 통신 스케줄링)
```

선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| GPU 엔드포인트 | **NVLink P2P** 패킷 송수신 |
| SerDes 물리 계층 | PAM4 신호 변환과 **물리 전송** |
| NVSwitch 칩 | **비차단 크로스바 라우팅** |
| NCCL 라이브러리 | **All-Reduce 통신 최적화** |
| 호스트 CPU·PCIe | 부팅·드라이버·입출력 제어 |

#### 한줄 요약
- NVSwitch 크로스바가 GPU 사이의 데이터 경로에 끼어들어 호스트 CPU와 PCIe 버스가 하던 중계 복사를 대신하므로, 호스트는 부팅·드라이버·입출력 제어만 남는 계층으로 물러나고 NCCL은 그 위에서 통신 패턴 수작업 구현을 대신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **All-Reduce**: 각 GPU가 계산한 그래디언트를 합산(Reduce)한 뒤, 최종 결과를 모든 참여 GPU에 동일하게 복제 분배(Broadcast)하는 집단 통신 연산.

</details>

```text
[NVLink 기반 집단 통신(All-Reduce) 제어]
▼
1. 물리 토폴로지 감지 및 최적 통신 트리 구성
├─ NCCL 런타임이 GPU 물리 연결 상태 스캔
└─ 링(Ring) 또는 트리(Tree) 집단 통신 알고리즘 자동 산출
▼
2. GPU 전용 NVLink P2P 패킷 직접 송출
├─ 호스트 CPU 및 PCIe 버스 완전 바이패스
└─ GPU HBM 주소 공간으로 고속 패킷 직결 전송
▼
3. NVSwitch 패브릭 라우팅 및 인스위치 연산
├─ 비차단 풀메시 크로스바 라우팅 (충돌 없는 전이중 전송)
└─ SHARP 엔진이 스위치 내부에서 All-Reduce 부분합 즉시 집계
▼
4. 통신 도메인 판정 및 스케일아웃 연계
├─ [동일 노드 내부] ─> NVLink 풀메시 패브릭 초고속 직접 동기화
└─ [멀티 노드 확장] ─> InfiniBand RoCE RDMA HCA 변환 브리징
▼
5. 가중치 파라미터 동기화 갱신 및 다음 스텝 진입
├─ 전체 참여 GPU의 그래디언트 합산값 동일 동기화 완료
└─ 가중치 텐서 갱신 후 다음 순전파(Forward) 스텝 즉시 개시
```

분기 결과: 노드 내부 GPU 간 통신은 NVLink와 NVSwitch를 통해 초고속으로 완료되며, 노드 간 통신은 **InfiniBand RDMA**와 연계되어 스케일아웃 확장됨

**동작 원리**

1. **토폴로지 감지 및 집단 통신 트리 구성**: NCCL 라이브러리가 물리 인터커넥트 토폴로지를 스캔하여 GPU 간 대역폭이 최대화되는 최적의 링(Ring) 또는 트리(Tree) 집단 통신 그래프 구축
2. **P2P 직접 패킷 송출**: 각 GPU가 역전파를 마친 가중치 그래디언트를 호스트 CPU 개입 없이 NVLink 컨트롤러를 통해 대상 GPU의 HBM 주소 공간으로 직접 송출
3. **인스위치 라우팅 및 하드웨어 집계**: 전송된 데이터 패킷이 NVSwitch 크로스바 스위치를 통과하며, SHARP 하드웨어 가속기가 인스위치 상태에서 All-Reduce 부분합 즉각 집계
4. **스케일아웃 네트워크 브리징**: 단일 노드 스케일업 용량을 초과하는 멀티 노드 클러스터 통신 구간에서 InfiniBand RoCE RDMA HCA로 변환되어 스케일아웃 패브릭으로 브리지
5. **가중치 파라미터 동기화 갱신**: 모든 참여 GPU의 가중치가 동일하게 동기화 완료되면 가중치 파라미터를 즉각 갱신하고 지연 없이 다음 순전파 스텝 연산 재개

#### 한줄 요약
- NVLink와 NVSwitch는 노드 안에 GPU 간 직결 경로를 깔아 All-Reduce 비용을 낮추지만 노드 경계를 넘는 순간 InfiniBand 대역폭이 상한이 되므로, 통신량이 많은 병렬 축을 노드 안쪽에 배치하는 것이 관건이다.

## Ⅴ. 종류 및 비교

| 대상 구분 | NVIDIA NVLink (v4 / v5) | PCIe Gen5 / Gen6 | CXL.mem | InfiniBand (RDMA) |
|:---|:---|:---|:---|:---|
| 적용 기준 | 노드 내 초고속 GPU P2P 텐서 동기화 요구 시 | 표준 서버 환경 범용 가속기·I/O 장치 연결 시 | CPU-가속기 간 캐시 일관성 메모리 풀링 요구 시 | 멀티 노드 대규모 AI 클러스터 스케일아웃 구축 시 |
| 핵심 특징 | GPU당 **1.8 TB/s 초고대역폭**, NVSwitch 비차단 풀메시 크로스바, SHARP 인스위치 집단 연산 | 개방형 표준 인터페이스, 범용 장치 호환성, 단방향 64~128 GB/s 대역폭 | PCIe 물리 계층 공유, 바이트 단위 캐시 일관성 지원, 메모리 용량 동적 확장 | 멀티 노드 스케일아웃 패브릭, 커널 바이패스 RDMA 지원, 초저지연 패킷 스위칭 |
| 한계 | NVIDIA 독점 하드웨어 종속성, 전용 섀시 및 고가 인프라 비용 수반 | GPU 대규모 텐서 동기화 시 대역폭 병목 및 CPU 중계 오버헤드 | GPU 집단 통신 연산 미특화, 상용 컨트롤러 생태계 형성 초기 단계 | 노드 내부 P2P 대비 상대적 대역폭 한계 및 복잡한 서브넷 관리 부담 |

#### 한줄 요약
- 단일 노드 내 초고속 GPU 스케일업에는 NVLink가 독보적이며, 노드 간 대규모 클러스터 스케일아웃 네트워킹에는 InfiniBand가 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **통신-연산 오버랩(Communication-Computation Overlap)**: 후속 레이어 역전파 연산을 수행하는 동안 선행 레이어의 그래디언트를 NVLink로 비동기 전송하는 파이프라이닝 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| All-Reduce 통신 대기로 연산 유휴 | **통신-연산 오버랩** 및 텐서 버킷팅 | 지연시간 **100% 은닉** |
| 8개 GPU 고밀도 집적으로 발열 급증 | **칩 직접 수랭식(Liquid Cooling)** 구축 | 열 스로틀링 방지 및 **클록 유지** |
| 멀티 노드 확장 시 대역폭 불균형 | **노드 내 텐서 병렬화** 및 노드 간 파이프라인 분할 | 클러스터 **확장 효율 90% 사수** |

#### 한줄 요약
- 실무에서는 통신-연산 오버랩으로 지연을 은닉하고, 수랭 냉각으로 발열을 제어하며, 하이브리드 병렬화로 노드 간 병목을 극복한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **엔비디아 NVL72(NVIDIA NVLink 72, NVL72)**: 단일 랙 캐비닛 안에 72개의 GPU와 NVSwitch를 액체 냉각 구리선 카트리지로 상호 직결하여 단일 거대 가속기처럼 구동하는 랙 스케일 컴퓨팅 아키텍처.
- **텐서 병렬화(Tensor Parallelism)**: 단일 신경망 계층의 대규모 가중치 행렬을 복수 GPU에 분할 배치하여 실시간 통신을 동반하는 병렬 분산 처리 기법.

</details>

- **랙 스케일 초거대 패브릭 진화**: 단일 서버 노드를 넘어 랙 전체 72개 가속기를 액체 냉각 구리선으로 직결하는 엔비디아 NVL72(NVIDIA NVLink 72, NVL72) 기반의 랙 스케일 단일 도메인으로의 패러다임 확장.
- **실무 계층적 토폴로지 설계 통찰**: 초고빈도 통신이 요구되는 텐서 병렬화(Tensor Parallelism) 축을 NVLink 도메인 내부에 격리 배치하고, 노드 간에는 스케일아웃 네트워크를 결합하는 하이브리드 분산 토폴로지 설계 절단 필요.

#### 한줄 요약
- NVL72 기반의 랙 스케일 가속 패브릭으로 진화하고 있으며, 텐서 병렬화 축을 NVLink 고속 도메인 내에 엄격히 격리하는 계층적 분산 토폴로지 설계가 핵심이다.
