---
sidebar:
  order: 47
  label: "047. NVLink 고속 인터커넥트 (NVLink)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-08-17T16:50:00+09:00"
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

- **NVLink**: GPU 간 초고속 데이터 전송 및 단일 가상 메모리 공간 공유를 지원하는 NVIDIA 독점 고대역폭 직렬 인터커넥트.
- **P2P(Peer-to-Peer) 전송**: 호스트 CPU나 시스템 메인 메모리를 경유하지 않고 GPU 간 HBM 메모리에 직접 읽기·쓰기하는 통신 방식.

</details>

- 정의/개념: GPU 간 고속 데이터 전송 및 메모리 공유를 지원하기 위해 NVIDIA가 개발한 **초고대역폭 전용 인터커넥트 기술**
- 배경/필요성: 대규모 AI 분산 학습 시 전통적 PCIe 버스의 **대역폭 포화 및 통신 지연** 병목 직면

#### 한줄 요약
- 여러 GPU를 PCIe보다 훨씬 넓고 빠른 전용 도로망으로 묶어 하나의 거대한 슈퍼 GPU처럼 동작하게 만든다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NVSwitch**: 노드 내 다수 GPU의 NVLink 포트들을 크로스바 스위치 구조로 연결해 전 대역폭 풀메시 통신을 가능하게 하는 스위치 칩.
- **집단 통신(Collective Communication)**: 분산 딥러닝에서 All-Reduce, All-Gather 등을 통해 전체 GPU의 가중치 기울기를 동기화하는 통신.

</details>

- **초고대역폭(양방향 최대 900GB/s~1.8TB/s)** 지원으로 PCIe 대역폭 한계 극복
- 호스트 CPU 개입 없는 **P2P 직접 메모리 접근** 및 메모리 풀링 실현
- **NVSwitch** 기반 풀메시(Full-Mesh) 스케일업(Scale-up) 토폴로지 구축

#### 한줄 요약
- 초고속 P2P 통신과 NVSwitch 패브릭을 통해 수십 개의 GPU가 동일한 메모리처럼 서로의 HBM을 초저지연으로 읽고 쓴다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SerDes(Serializer/Deserializer)**: 병렬 텐서 데이터를 초고속 직렬 전기 신호로 변환하고 복원하는 고속 인터페이스 송수신 회로.
- **NCCL(NVIDIA Collective Communications Library)**: NVLink 토폴로지를 자동으로 인식하여 최적화된 집단 통신 커널을 실행하는 라이브러리.

</details>

```text
┌─────────────────────────────────────────────────────────────┐
│ 8-GPU NVLink & NVSwitch 상호 연결 구조                      │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐│
│  │ GPU 0    │    │ GPU 1    │    │ GPU 2    │    │ GPU 3    ││
│  │ (HBM3)   │    │ (HBM3)   │    │ (HBM3)   │    │ (HBM3)   ││
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘│
│       │ NVLink 포트   │               │               │      │
│  ┌────┴───────────────┴───────────────┴───────────────┴────┐│
│  │ NVSwitch 패브릭 (Non-blocking Crossbar Fabric)          ││
│  └────┬───────────────┬───────────────┬───────────────┬────┘│
│       │               │               │               │      │
│  ┌────┴─────┐    ┌────┴─────┐    ┌────┴─────┐    ┌────┴─────┐│
│  │ GPU 4    │    │ GPU 5    │    │ GPU 6    │    │ GPU 7    ││
│  │ (HBM3)   │    │ (HBM3)   │    │ (HBM3)   │    │ (HBM3)   ││
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘│
└─────────────────────────────────────────────────────────────┘
```

선의 의미: 모든 GPU가 NVSwitch 크로스바 패브릭을 통해 단일 홉(Single-Hop)으로 전 대역폭 풀메시 통신 수행

| 구성요소 | 책임 |
|:---|:---|
| GPU 엔드포인트 | 텐서 데이터를 연산하고 HBM에 저장하며 NVLink 포트를 통해 P2P 패킷 송수신 |
| NVLink 포트 & SerDes | 차동 신호 기반 고속 직렬 전송 및 데이터 링크 계층의 무손실 패킷 제어 |
| NVSwitch 칩 | 모든 GPU 간 트래픽을 비차단(Non-blocking) 풀메시 스위칭 및 멀티캐스트 가속 |
| 통신 라이브러리 (NCCL) | 물리 토폴로지를 탐색하여 링(Ring) 및 트리(Tree) 기반 최적 All-Reduce 스케줄링 |
| 호스트 CPU & PCIe | 시스템 부팅, GPU 드라이버 초기화 및 스토리지 I/O 제어 관리 |

#### 한줄 요약
- GPU 엔드포인트, 고속 SerDes, NVSwitch 스위칭 패브릭, NCCL 라이브러리가 유기적으로 결합되어 있다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **All-Reduce**: 각 GPU가 계산한 가중치 기울기(Gradient)를 전송·합산(Reduce)한 뒤 그 결과를 모든 GPU에 다시 분배(Broadcast)하는 연산.

</details>

```text
분산 딥러닝 역전파(Backprop) 연산 완료
      │
      ▼
1. NCCL 라이브러리: 물리 NVLink 토폴로지 분석 및 통신 링(Ring) 구성
      │
      ▼
2. GPU P2P DMA: HBM 상의 기울기 텐서를 NVLink 패킷으로 직렬화
      │
      ▼
3. NVSwitch 패브릭: 비차단 전이중 경로를 통해 인접 GPU로 텐서 고속 전송
      │
      ▼
4. 하드웨어 SHARP / GPU: 수신된 기울기 텐서의 누산 합산(Reduce) 수행
      │
      ▼
5. 최종 All-Gather 동기화 완료 후 다음 학습 반복(Iteration) 즉시 진입
```

**동작 원리**

1. **토폴로지 탐색**: NCCL이 NVSwitch 연결 상태를 감지하고 가장 빠른 데이터 교환 경로 결정
2. **패킷 직렬화**: 송신 GPU가 HBM의 가중치 기울기를 직접 읽어 NVLink 직렬 패킷으로 변환
3. **크로스바 스위칭**: NVSwitch를 거쳐 CPU 경유 없이 대상 GPU HBM으로 전 대역폭 고속 스트리밍
4. **기울기 누산**: 전달된 텐서들을 병렬 합산하여 전체 GPU 간 모델 파라미터 동기화
5. **동기화 완료**: 오차 전파 완료 즉시 순전파(Forward pass) 연산으로 복귀

#### 한줄 요약
- 토폴로지 분석 → NVLink 패킷화 → NVSwitch 전송 → 기울기 합산 → 동기화 완료 순으로 동작한다.

## Ⅴ. 종류 및 비교

| GPU 인터커넥트 | NVIDIA NVLink | PCIe Gen5 | CXL.mem | InfiniBand (RDMA) |
|:---|:---|:---|:---|:---|
| 적용 기준 | 단일 노드 내 다중 GPU 초고속 스케일업 | 범용 메인보드 기반 일반 확장 카드 연결 | 이기종 메모리 풀링 및 확장 | 노드 간(Scale-out) 대규모 클러스터 네트워킹 |
| 핵심 특징 | 최대 900GB/s 초고대역폭 및 NVSwitch 풀메시 | 폭넓은 표준 호환성 및 독립 장치 지원 | 호스트-디바이스 간 캐시 일관성 공유 | RoCE/IB 기반 초저지연 원격 메모리 복사 |
| 한계 | NVIDIA 전용 하드웨어 종속성 및 고비용 | 낮은 대역폭(128GB/s)으로 분산 학습 병목 | 스위치 생태계 초기 단계 및 지연 오버헤드 | 노드 내 통신 대비 높은 지연(수 마이크로초) |

#### 한줄 요약
- 노드 내 GPU 연결은 NVLink, 범용 확장은 PCIe, 메모리 풀링은 CXL, 노드 간 확장은 InfiniBand를 쓴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **통신-연산 오버랩(Communication-Computation Overlap)**: 후속 레이어 역전파 연산을 수행하는 동안 선행 레이어 기울기를 비동기로 전송하는 최적화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 집단 통신 중 통신 대기로 인한 **GPU 연산기 유휴** | **통신-연산 비동기 오버랩** 및 텐서 버킷팅(Bucketing) 적용 | All-Reduce 지연 은닉 및 학습 처리량 향상 |
| 특정 NVLink 포트 이상 시 통신 성능 급락 | **NCCL 경로 자동 우회(Failover)** 및 패브릭 헬스체크 연동 | 장애 노드 격리 및 분산 학습 연속성 보장 |
| 고밀도 NVLink 서버 구동 시 심각한 발열 | **수랭식 직접 액체 냉각(DLC)** 및 팬 속도 능동 제어 | 열 스로틀링 방지 및 24/7 최대 대역폭 유지 |
| 다중 노드 확장 시 노드 간 이더넷 병목 | NVLink(노드 내)와 **InfiniBand/RoCE(노드 간)** 계층형 하이브리드 구성 | 대규모 AI 클러스터 선형적 확장성 확보 |

#### 한줄 요약
- 통신-연산 오버랩으로 지연을 숨기고, 액체 냉각으로 발열을 잡으며, 인피니밴드와 계층화한다.

## Ⅶ. 결론

- 노드 내 초대형 AI 모델 분산 학습 및 GPU 메모리 통합은 **NVLink**, 노드 간 확장은 **InfiniBand** 선택

#### 한줄 요약
- NVSwitch 풀메시 패브릭과 NCCL 통신 최적화를 통해 노드 내 다중 GPU의 메모리 대역폭 한계를 원천 극복해야 한다.
