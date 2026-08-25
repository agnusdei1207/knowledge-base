---
sidebar:
  order: 47
  label: "047. NVLink 고속 인터커넥트 (NVLink)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 47
extra:
  question_no: "047"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "다중 GPU 분산 통신과 메모리 풀링의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NVLink**: NVIDIA가 개발한 GPU-GPU 및 CPU-GPU 간 전용 고대역폭 직렬 인터커넥트로, 캐시 일관성 및 직접 메모리 공유(P2P)를 제공하는 하드웨어 버스 인터페이스.
- **피어 투 피어 전송(Peer-to-Peer Transfer, P2P 전송)**: 호스트 CPU와 시스템 메인 메모리를 경유하지 않고 가속기 간 전용 버스를 통해 직접 데이터를 송수신하는 메모리 접근 방식.

</details>

- 정의/개념: 호스트 CPU 경유 없이 GPU 간 고대역폭 직접 접근을 지원하는 전용 고속 인터커넥트 **NVLink**
- 배경/필요성: 기존 범용 PCIe 버스 대역폭으로는 **분산 학습 시 대규모 텐서 동기화 통신 병목 해소 불가**

#### 한줄 요약
- NVLink는 호스트 CPU를 거치지 않고 GPU 간 초고대역폭 직접 메모리 통신(P2P)을 가능하게 하는 스케일업 인터커넥트 기술이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NVSwitch**: 단일 노드 내 다수 GPU의 NVLink 포트를 크로스바 스위치 구조로 연결하여 전 대역폭 완전 연결(Full Mesh)을 지원하는 전용 패브릭 스위치 칩.
- **집단 통신(Collective Communication)**: 분산 딥러닝 환경에서 다수 GPU 간 그래디언트 및 텐서 데이터를 동기화하는 다대다 통신 패턴(All-Reduce, All-Gather 등).

</details>

- 다중 링크 집성(Link Aggregation) 기반 범용 PCIe 대비 7배 이상 초고대역폭 제공
- 호스트 시스템 메모리 복사 오버헤드를 배제하는 직접 **P2P 전송** 지원
- **NVSwitch** 연동 풀메시 토폴로지로 노드 내 **집단 통신** 경로 극대화

#### 한줄 요약
- NVSwitch와 결합하여 노드 내 모든 GPU 간 비차단 풀메시 대역폭을 제공함으로써 대규모 모델 병렬화의 통신 지연을 극소화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SerDes(Serializer/Deserializer)**: 칩 내부의 병렬 데이터를 초고속 차동 직렬 신호로 변환하여 물리 링크로 송수신하고 복원하는 고속 물리 계층 회로.
- **NCCL(NVIDIA Collective Communications Library)**: 하드웨어 토폴로지를 자동 감지하여 최적화된 링·트리 집단 통신 연산을 실행하는 멀티 GPU 통신 라이브러리.

</details>

```text
[노드 내 스케일업 구조]
|-- GPU 엔드포인트 × 8
|   |-- HBM (텐서 저장)
|   `-- NVLink 포트·SerDes (직렬 송수신·무손실 패킷 제어)
|-- NVSwitch 패브릭 (논블로킹 크로스바)
|-- NCCL (토폴로지 탐색·집단 통신 스케줄링)
`-- 호스트 CPU·PCIe (부팅·드라이버·스토리지 I/O)
```

선의 의미: 계층 및 소유 관계

| 구성요소 | 책임 |
|:---|:---|
| GPU 엔드포인트 | 텐서 연산·저장과 P2P 패킷 송수신 전담 |
| **SerDes** | 온칩 병렬 데이터를 고속 차동 직렬 신호로 상호 변환 |
| NVSwitch 칩 | 다수 GPU 트래픽을 비차단(Non-blocking) 스위칭하여 연결망 확장 |
| **NCCL** | 물리 토폴로지 탐색 기반 링·트리 집단 통신 알고리즘 최적화 스케줄링 |
| 호스트 CPU·PCIe | 시스템 부팅, 드라이버 초기화 및 스토리지 I/O 제어 |

#### 한줄 요약
- 하드웨어 레벨의 NVSwitch 크로스바와 소프트웨어 레벨의 NCCL 집단 통신 스케줄러가 결합되어 최대 대역폭을 이끌어낸다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **All-Reduce**: 각 노드/GPU가 계산한 그래디언트를 합산(Reduce)한 뒤, 그 최종 결과를 모든 참여 장치에 동일하게 복제 분배(Broadcast)하는 집단 통신 연산.

</details>

```text
역전파 연산 완료 → 기울기 텐서 확보
        │
   NCCL이 패브릭 토폴로지 탐색
        │
   통신 상대가 같은 노드 안에 있는가?
   ┌────┴─────┐
  예           아니오
   │             │
NVLink P2P로   노드 간 네트워크(InfiniBand) 우회
청크 직접 전송    (지연·대역폭 열세)
   │             │
NVSwitch가 목적   │
GPU로 스위칭      │
   │             │
   └────┬────────┘
        │
   전달된 청크를 합산 후 전체에 재분배 (All-Reduce)
        │
   다음 반복 시작
```

#### 한줄 요약
- 노드 내 GPU 간 통신은 NVLink P2P를 통해 전송하고, 노드 간 통신은 InfiniBand RDMA로 우회하여 All-Reduce 동기화를 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PCIe Gen5**: 범용 메인보드 표준 직렬 인터페이스로 폭넓은 확장성을 제공하는 버스.
- **CXL.mem**: 호스트 CPU와 가속기/메모리 장치 간 캐시 일관성 메모리 풀링을 지원하는 개방형 표준 프로토콜.
- **InfiniBand (RDMA)**: 노드 간 스케일아웃 네트워크에서 커널 바이패스로 메모리를 원격 직접 접근하는 고속 패브릭.

</details>

| GPU 인터커넥트 | NVIDIA NVLink | PCIe Gen5 | CXL.mem | InfiniBand (RDMA) |
|:---|:---|:---|:---|:---|
| 적용 기준 | 단일 노드 내 다중 GPU 초고속 스케일업 | 범용 메인보드 기반 일반 확장 카드 연결 | 이기종 메모리 풀링 및 확장 | 노드 간(Scale-out) 대규모 클러스터 네트워킹 |
| 핵심 특징 | GPU 특화 고대역폭 P2P와 NVSwitch | 폭넓은 표준 호환성과 장치 확장 | 호스트-디바이스 캐시 일관성과 메모리 확장 | IB 기반 RDMA와 집단 통신 |
| 한계 | NVIDIA 하드웨어와 시스템 구성에 종속 | GPU 집단 통신에서 대역폭 제약 가능 | GPU 전용 스케일업보다 높은 프로토콜 비용 | 노드 내 전용 링크보다 높은 지연 |

#### 한줄 요약
- 노드 내 GPU 간 스케일업에는 NVLink가, 노드 간 대규모 스케일아웃 네트워킹에는 InfiniBand RDMA가 표준 계층 구조로 배치된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **통신-연산 오버랩(Communication-Computation Overlap)**: 후속 레이어 역전파 연산을 수행하는 동안 선행 레이어 기울기를 비동기로 전송하는 최적화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 집단 통신 대기로 인한 GPU 연산기 유휴 | **통신-연산 오버랩** 및 텐서 버킷팅 적용 | 통신 지연 은닉으로 분산 학습 처리량 향상 |
| 링크 및 NVSwitch 장애 시 클러스터 중단 | 링크 헬스 모니터링 및 주기적 분산 체크포인팅 | 결함 링크 신속 격리 및 복구 시간 단축 |
| 고밀도 GPU 서버 집적에 따른 열 포화 | 다이렉트 수냉 쿨링(Direct-to-Chip Liquid) 도입 | 열 스로틀링 방지 및 지속 연산 신뢰성 확보 |
| 다중 노드 확장 시 노드 간 대역폭 병목 | 노드 내 NVLink, 노드 간 InfiniBand 계층화 설계 | 통신 집중 계층 격리로 선형적 확장성 보장 |

#### 한줄 요약
- NVLink 기반 분산 시스템에서는 통신-연산 오버랩 파이프라이닝과 고밀도 발열 제어를 위한 수냉 쿨링 설계가 필수적이다.

## Ⅶ. 결론

- 노드 내부는 **NVLink·NVSwitch** 기반 스케일업을 적용하고, 노드 간은 **InfiniBand RDMA** 기반 계층형 분산 패브릭으로 설계하여 대규모 학습 병목 해소

#### 한줄 요약
- 분산 딥러닝 인프라는 노드 내 초고속 NVLink와 노드 간 무손실 RDMA 네트워크의 계층적 결합을 통해 총 연산 처리량을 극대화한다.