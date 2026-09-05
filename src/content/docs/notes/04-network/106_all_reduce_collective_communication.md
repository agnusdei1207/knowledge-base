---
sidebar:
  order: 106
  label: "106. 집합 통신 All-Reduce"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 딥러닝 텐서 동기화 : 집합 통신 All-Reduce"
date: "2026-09-06T00:10:06+09:00"
tags:
  - "notes-network"
weight: 106
extra:
  question_no: "106"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "Ring All-Reduce (Reduce-Scatter + All-Gather), Tree All-Reduce, 계층형 All-Reduce 및 NCCL 가속"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **All-Reduce**: $N$개 GPU의 로컬 텐서를 합산(Reduce)한 후 최종 결과를 모든 노드에 동일하게 배포(Gather)하는 집합 통신 프리미티브.
- **Parameter Server (PS) 병목**: 중앙 서버로 모든 그래디언트를 업로드/다운로드할 때 발생하는 대역폭 병목과 선형적 지연 폭증 한계.

</details>

- 정의/개념: **Reduce-Scatter·All-Gather**로 텐서를 동기화하는 집합 통신
- 배경/필요성: 초거대 AI 모델의 데이터 병렬화(Data Parallelism) 분산 학습 시, 수천 대의 GPU가 계산한 역전파 그래디언트(Gradient)를 동기화하기 위해 중앙 마스터 노드에 의존하는 파라미터 서버(Parameter Server) 방식은 노드 수가 증가할수록 중앙 서버의 네트워크 대역폭 포화(Network Saturation) 및 심각한 통신 병목을 초래하여 클러스터 확장 효율이 급격히 저하되는 한계를 노출함에 따라, 중앙 집중 노드 없이 모든 참여 노드가 링(Ring), 트리(Tree) 또는 계층형(Hierarchical) 토폴로지 상에서 그래디언트 청크를 분할 교환(Reduce-Scatter)하고 전역 복제(All-Gather)하는 All-Reduce 집합 통신(Collective Communication) 알고리즘을 도입하여 **노드 수($N$)가 증가해도 GPU당 통신량을 $2(N-1)M/N \approx 2M$으로 일정하게 유지, 중앙 병목의 원천 제거 및 선형적(Linear) 분산 훈련 확장 효율**을 달성할 필요

#### 한줄 요약
- Reduce-Scatter와 All-Gather를 통해 노드 수와 무관한 일정한 통신량으로 그래디언트를 전역 동기화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Communication-Computation Overlap**: 딥러닝 역전파가 진행되는 동안 하위 레이어의 그래디언트 계산과 상위 레이어의 All-Reduce 통신을 비동기로 동시 병렬 수행하는 기법.

</details>

- **전송량 $2(N-1)M/N$**: GPU당 데이터양이 약 $2M$으로 수렴
- **탈중앙 구조**: 모든 GPU가 대역폭·연산 부하 분담
- **연산-통신 오버랩**: 역전파와 All-Reduce 병렬 수행

#### 한줄 요약
- 노드 수 무관 전송량 고정, 완전 탈중앙화 부하 분담, 연산-통신 비동기 오버랩을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Tensor Fusion (버킷팅)**: 작은 크기의 수천 개 텐서를 개별 통신하지 않고 25~50MB 단위 버킷으로 합쳐서 전송하는 최적화 기법.

</details>

```text
[All-Reduce 정적 구성]
|-- 통신 랭크
|-- 텐서 버킷 퓨전기
|-- NCCL 엔진
|-- Reduce-Scatter 모듈
`-- All-Gather 모듈
```

선의 의미: 4개의 GPU가 원형 링(Ring)으로 연결되어 이웃 GPU로만 데이터를 전달하며 합산과 배포를 완수하는 탈중앙화 구조

| 구성요소 | 책임 |
|:---|:---|
| **통신 랭크** | GPU **고유 식별자** |
| **텐서 버킷 퓨전기** | 그래디언트 **버킷 병합** |
| **NCCL 엔진** | Ring·Tree·**CollNet 선택** |
| **Reduce-Scatter 모듈** | 청크 순환과 **누적 합산** |
| **All-Gather 모듈** | 합산 청크 **전역 복제** |

#### 한줄 요약
- 텐서 버킷 퓨전기가 작은 그래디언트를 묶어 통신 호출 횟수를 줄이므로, 고정 지연 비용이 텐서 개수가 아니라 버킷 개수에 비례한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **In-Network Reduction (SHARP)**: All-Reduce 집계 연산을 GPU 코어가 아닌 인피니밴드 스위치 ASIC에서 직접 수행하여 트래픽을 50% 절감하는 기술.

</details>

```text
역전파 그래디언트
    |
1. 텐서 버킷 생성
    |
2. 통신 계약 검증
    |
3. Reduce-Scatter
    |
4. All-Gather
    |
5. 가중치 갱신
    |
동기화 완료
```

- 1. 텐서 버킷 생성
- 2. 통신 계약 검증
- 3. Reduce-Scatter
- 4. All-Gather
- 5. 가중치 갱신

#### 한줄 요약
- Reduce-Scatter와 All-Gather 두 단계로 나눈 덕분에 노드가 늘어도 노드당 전송량은 일정하지만, 그 대가로 단계 수에 비례한 지연이 누적된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Ring (대역폭 최적)** vs **Tree (지연시간 최적)** vs **Hierarchical (노드 내외 분리)**.

</details>

| 알고리즘 종류 | 링 All-Reduce (Ring All-Reduce) | 트리 All-Reduce (Tree All-Reduce) | 계층형 All-Reduce (Hierarchical) |
|:---|:---|:---|:---|
| 통신 메커니즘 | **2(N-1) 링 순환** | **트리 집계·배포** | **NVLink·IB 계층 집계** |
| 최적 데이터 크기 | **대형 텐서** | **소형 텐서** | **대규모 멀티 노드** |
| 소요 지연 시간 | $O(N)$ | **$O(\log N)$** | 노드 간 트래픽 최소화 |
| 인터커넥트 활용 | 동일 대역폭 링크 | 루트 포화 위험 | **노드 내외 링크 분리** |
| 주요 적용 영역 | 데이터 병렬화 | 중간 동기화 | **하이퍼스케일 AI** |

#### 한줄 요약
- 대형 텐서는 링(대역폭 최적), 소형 텐서는 트리(지연 최적), 대규모 클러스터는 계층형(링크 격차 해소)을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Straggler Node (스트래글러 노드)**: 열 쓰로틀링이나 패킷 손실로 인해 연산/통신 속도가 뒤처져 전체 클러스터의 동기화를 지연시키는 노드.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 저속 노드로 동기화 지연 증가 | **Straggler 감지·대체** | 테일 지연 단축 |
| 작은 텐서의 호출 오버헤드 | **Tensor Fusion 버킷** | 페이로드 효율 향상 |
| 랭크 호출 순서 불일치 | **NCCL 통신 계약 검증** | 데드락 방지 |
| WAN 지연에 따른 All-Reduce 정체 | **그래디언트 압축·비동기화** | 통신량 절감 |

#### 한줄 요약
- 슬로우 노드 격리로 스트래글러를 방지하고, 텐서 퓨전으로 오버헤드를 줄이며, 계약 검증으로 데드락을 차단한다.

## Ⅶ. 결론

- 중앙 집중형 파라미터 서버의 물리적 한계를 완전히 극복하고 초거대 모델의 대규모 분산 딥러닝을 가능케 하는 **AI 분산 학습 집합 통신(Collective Communication)의 가장 핵심적인 통신 프리미티브이자 표준 알고리즘(MPI / NCCL)**으로 확립되었으며, 스위치 인네트워크 컴퓨팅(SHARP) 및 2D-Torus/Dragonfly+ 패브릭과의 결합으로 진화하는 가운데, 실무 분산 AI 학습 파이프라인 구축 시에는 **텐서 크기와 토폴로지에 따라 대형 텐서는 링(Ring), 소형 텐서는 트리(Tree), 노드 내-외 링크 속도 격차(NVLink vs RDMA)가 큰 환경은 계층형(Hierarchical) All-Reduce 최적 알고리즘 선택, 작은 텐서들의 통신 오버헤드를 제거하는 텐서 퓨전(Tensor Fusion / 버킷팅) 적용, 전체 클러스터 동기화를 지연시키는 단일 저속 노드(Straggler Node) 실시간 감지 및 동적 격리**를 결합하여 완벽한 분산 훈련 처리 성능을 완성

#### 한줄 요약
- All-Reduce는 Reduce-Scatter와 All-Gather 및 계층형 NVLink/RDMA 패브릭을 결합하여 대규모 AI 분산 훈련을 실현하는 핵심 통신 프리미티브다.
