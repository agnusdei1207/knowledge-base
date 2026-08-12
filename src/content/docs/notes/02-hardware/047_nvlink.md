---
sidebar:
  order: 47
  label: "047. NVLink 고속 인터커넥트 (NVLink)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-hardware"
weight: 47
extra:
  question_no: "047"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "다중 GPU 통신 병목과 연결 선택"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **NVLink(NVIDIA NVLink)**: NVIDIA GPU 간 및 GPU-CPU 간 고대역폭·저지연 데이터 P2P 통신을 지원하는 전용 고속 인터커넥트.
- **인터커넥트(Interconnect)**: 프로세서, 메모리, 확장 장치 간 데이터 패킷 및 신호를 고속 이송하는 신호 채널 망.
- **홉(Hop)**: 패킷 데이터가 전송 도중 경유하는 개별 스위치 또는 물리적 노드 구간.

</details>

- 정의/개념: 다중 GPU 환경에서 호스트 CPU 경유 없이 GPU 간 Direct P2P 텐서 전송 및 집단 통신을 지원하는 **NVLink**
- 배경/필요성: 기존 PCIe 버스의 상호 공유 대역폭 제한 및 루트 콤플렉스 경유에 따른 **홉** 증가와 통신 병목 해결 필요성

#### 한줄 요약

- 엔비디아 NVLink는 GPU 사이에 고대역폭 피어 경로를 제공하고 NVSwitch는 다수 GPU의 다대다 경로를 구성해 집단 통신 병목을 줄인다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **링크 결합(Link Aggregation)**: 동일 GPU 노드 간 복수의 물리 NVLink 레인을 하나로 번들링하여 전송 대역폭을 선형 확장하는 기술.
- **NVSwitch**: 복수의 NVLink 라인을 스위칭하여 다수 GPU 간의 Non-blocking 다대다(All-to-All) 통신을 보장하는 전용 스위치.
- **토폴로지(Topology)**: 노드 간 물리적/논리적 결합 형태(Mesh, Torus, Fat-Tree 등).
- **집단 통신(Collective Communication)**: 분산 GPU 환경에서 All-Reduce, All-Gather, Reduce-Scatter 등을 실행하는 통신 패턴.

</details>

- GPU 간 대역폭을 멀티플렉싱 확장하는 **링크 결합** 지원
- 복수 GPU 노드 간 완전 대대다 통신을 보장하는 **NVSwitch** 라우팅
- 집단 통신 성능 극대화를 위한 최적 **토폴로지** 및 **통신 패턴** 적용

#### 한줄 요약

- 직접 링크 결합은 GPU 쌍의 대역폭을 높이고, NVSwitch와 토폴로지 인지 통신은 다수 GPU의 경로 병목을 줄인다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **NCCL(NVIDIA Collective Communications Library)**: NVLink 토폴로지를 자동 파악하여 집단 통신 연산을 가속화하는 최적화 라이브러리.
- **엔드포인트(Endpoint)**: NVLink 신호선을 수용하여 데이터 패킷을 송수신하는 GPU/CPU 하드웨어 레인 터미널.
- **패브릭(Fabric)**: 엔드포인트와 NVSwitch가 통합 결합된 고속 패킷 스위칭 네트워크 공간.

</details>

```text
[NCCL 통신 소프트웨어] -- [GPU 엔드포인트 집합] -- [NVLink 물리 링크] -- [NVSwitch 패브릭]
```

선의 의미: NCCL 소프트웨어 제어 하에 GPU 엔드포인트가 NVLink 물리 링크 및 NVSwitch 패브릭과 연동되는 네트워크 계층 구조.

| 구성요소 | 책임 |
|:---|:---|
| NCCL 통신 소프트웨어 | 토폴로지 인지 기반 링/트리 알로리즘 수립 및 집단 통신 전개 |
| GPU 엔드포인트 집합 | 데이터 텐서의 송수신 및 하드웨어 P2P 텐서 버퍼 제어 |
| NVLink 물리 링크 | 레인 묶음 기반 고속 차동 신호 송수신 물리 전송선 제공 |
| NVSwitch 패브릭 | 다대다 라우팅, Crossbar 스위칭 및 다중 노드 패킷 결합 |

#### 한줄 요약

- NCCL이 경로를 정하면 엔비디아 NVLink와 NVSwitch가 GPU 사이의 데이터를 직접 전달한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **All-Reduce**: 분산 GPU의 부분 결과 텐서를 합산한 후 완전한 결과 텐서를 모든 GPU로 전파하는 집단 통신 연산.
- **Reduce-Scatter**: 텐서를 쪼개어 각 GPU의 로컬 텐서와 동시 합산 및 분산 축소하는 파이프라인 연산.
- **All-Gather**: 분산 보유 중인 텐서 조각들을 상호 수집하여 완전체 텐서를 복원하는 연산.
- **통신 조각(Communication Chunk)**: NCCL 링 파이프라이닝을 위해 텐서를 미세 분할한 패킷 단위.

</details>

```text
                    [All-Reduce 텐서]
                             |
                 1. 토폴로지·조각 계획
                             |
                  2. Reduce-Scatter 실행
            +--------------------------------+
            | 반복: GPU 수−1단계             |
            | 조각 피어 전송·로컬 축소       |
            +--------------------------------+
                             |
                    3. All-Gather 실행
            +--------------------------------+
            | 반복: GPU 수−1단계             |
            | 완성 조각 피어 교환·수집       |
            +--------------------------------+
                             |
                    4. 전체 축소 완료
```

### 동작 원리

1. **토폴로지·조각 계획**: **NCCL**이 NVLink 토폴로지 파악 후 링/트리 알고리즘 및 **통신 조각** 분할 계획 수립.
2. **Reduce-Scatter 실행**: 링 파이프라인을 통한 GPU 수-1 회의 **Reduce-Scatter** 수행 및 부분합 축소.
3. **All-Gather 실행**: 링 경로 상으로 합산 완결 텐서를 전파하는 **All-Gather** 교환 전개.
4. **전체 축소 완료**: 모든 GPU 노드의 **All-Reduce** 텐서 수신 확인 후 커널 동기화 완료.

#### 한줄 요약

- NCCL은 토폴로지에 맞춰 축소-분산에서 조각을 합산하고 전체-수집에서 완성 조각을 모든 GPU에 배포한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **직접 NVLink(Direct NVLink)**: 스위치 없이 GPU 노드 간 점대점(P2P) 직결로 결합하는 방식.
- **NVSwitch 패브릭(NVSwitch Fabric)**: 스위치 ASIC을 매개하여 노드 수 확장에 따른 All-to-All 통신을 지원하는 패브릭.
- **PCIe(Peripheral Component Interconnect Express)**: 시스템의 표준 범용 점대점 확장 버스.

</details>

| GPU 연결 방식 | 직접 NVLink | NVSwitch | PCIe |
|:---|:---|:---|:---|
| 적용 기준 | 소규모 GPU(2~8개) P2P 직결 연결 시 | 대규모 GPU(8개 이상) 전대역 All-to-All 요구 시 | 범용 호스트-디바이스 및 이종 카드 연결 시 |
| 핵심 특징 | **직접 NVLink** 점대점 메시/링 연결 | **NVSwitch 패브릭** 기반 중앙 스위칭 | **PCIe** 계층적 버스 라우팅 |
| 한계 | 수용 가능한 포트 및 토폴로지 확장 제약 | 시스템 단가 및 소비 전력 증가 | 제한된 대역폭 및 **홉** 오버헤드 |

#### 한줄 요약

- 소수 GPU의 빈번한 피어 통신은 직접 엔비디아 NVLink, 다수 GPU의 다대다 집단 통신은 NVSwitch, 범용 호스트·장치 연결은 중앙 처리 장치가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **프로세스/샤드 배치(Process/Shard Placement)**: 통신 밀집 프로세스를 물리적으로 가까운 GPU NVLink 포트에 매핑하는 기술.
- **꼬리 지연(Tail Latency)**: 동기화 시 특정 저속 레인으로 인해 전체 텐서 통신이 대기하는 지연 현상.
- **통신·연산 중첩(Communication-Computation Overlap)**: GPU 연산 커널과 NVLink 데이터 수송을 동시 은닉 처리하는 방식.
- **링크 감시(Link Monitoring)**: NVLink 레인의 물리적 에러율, 재전송 트랜잭션, 둔화 여부를 추적하는 모니터링.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 원거리 홉 연결로 인한 대역폭 병목 및 **꼬리 지연** | **NCCL** 토폴로지 인지형 **프로세스/샤드 배치** | 홉 경유 최소화 및 통신 균형 확보 |
| 통신 연산 대기로 인한 GPU 코어 유휴 발생 | CUDA 스트림 기반 **통신·연산 중첩** 적용 | 데이터 전송 지연의 연산 시간 은닉 |
| 물리 링크 커넥터 또는 환경적 결함으로 대역폭 둔화 | **링크 감시** 및 비정상 NVLink 레인 격리/재구성 | 패브릭 전송 안정성 보장 |

> 사례: **NVLink** 기반 멀티 GPU 시스템 상에서 **NCCL** 파이프라이닝을 통한 학습 가속

#### 한줄 요약

- GPU 배치를 엔비디아 NVLink•NVSwitch 경로에 맞추고 통신 조각을 조정해 전체 축소의 느린 구간을 줄인다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **피어 통신(Peer Communication)**: 호스트 메모리 경유 없이 GPU 간 직접 텐서를 읽고 쓰는 Direct P2P 방식.
- **GPU 연결 선택 기준(GPU Interconnect Selection Criteria)**: 연결 GPU의 개수, All-to-All 대역폭 요구 수준 및 TCO에 기반한 선택 체계.

</details>

- **GPU 연결 선택 기준**에 따라 소규모 노드는 **직접 NVLink**, 대규모 노드는 **NVSwitch** 적용

#### 한줄 요약

- 소수 GPU는 엔비디아 NVLink로 직접 연결하고 다수 GPU의 전대역 연결에는 NVSwitch를 적용한다.
