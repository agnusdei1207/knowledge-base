---
sidebar:
  order: 47
  label: "047. NVLink 고속 인터커넥트 (NVLink)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "NVLink 고속 인터커넥트 (NVLink)"
date: "2026-08-06T23:27:50+09:00"
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

- **엔비디아 NVLink(NVIDIA NVLink, NVLink)**: 엔비디아 그래픽 처리 장치(Graphics Processing Unit, GPU)와 중앙 처리 장치(Central Processing Unit, CPU) 사이에 고대역폭•저지연 데이터 전송을 제공하는 전용 인터커넥트이다.
- **인터커넥트(Interconnect)**: 프로세서와 메모리 및 장치 사이에서 데이터와 제어 신호를 전달하는 연결 체계이다.
- **홉(Hop)**: 데이터가 출발지에서 목적지까지 이동하며 거치는 하나의 링크 또는 스위치 구간이다.

</details>

- 정의/개념: NVIDIA GPU·CPU 사이에 피어 데이터와 집단 통신을 전달하는 **고대역폭 전용 인터커넥트**이다.
- 배경/필요성: PCIe 계층과 공유 경로만으로는 다중 GPU 집단 통신에서 **대역폭·스위치 홉 병목이 발생한다**.

#### 한줄 요약

- NVLink는 GPU 사이에 고대역폭 피어 경로를 제공하고 NVSwitch는 다수 GPU의 다대다 경로를 구성해 집단 통신 병목을 줄인다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **링크 결합(Link Aggregation)**: 동일한 그래픽 처리 장치(Graphics Processing Unit, GPU) 쌍 사이의 여러 물리 링크를 함께 사용하여 총대역폭을 높이는 방식이다.
- **NVSwitch**: 여러 NVLink 엔드포인트를 다대다 경로로 연결하는 NVIDIA의 전용 스위치이다.
- **토폴로지(Topology)**: GPU와 링크 및 스위치가 서로 연결된 물리적 형태이다.
- **집단 통신(Collective Communication)**: 여러 GPU가 각자의 데이터를 합산•분배•교환하는 다자간 통신이다.

</details>

- GPU 쌍의 대역폭을 확장하는 **다중 링크 결합**이 핵심이다.
- 다수 GPU를 다대다로 연결하는 **NVSwitch 패브릭**이 핵심이다.
- 집단 통신 처리량을 좌우하는 **토폴로지•통신 패턴**이 핵심이다.

#### 한줄 요약

- 직접 링크 결합은 GPU 쌍의 대역폭을 높이고, NVSwitch와 토폴로지 인지 통신은 다수 GPU의 경로 병목을 줄인다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **엔비디아 집단 통신 라이브러리(NVIDIA Collective Communications Library, NCCL)**: 그래픽 처리 장치(Graphics Processing Unit, GPU) 토폴로지에 맞춰 집단 통신 경로와 전송 연산을 실행하는 라이브러리이다.
- **엔드포인트(Endpoint)**: 링크에 연결되어 데이터를 송수신하는 GPU나 CPU의 통신 종단이다.
- **패브릭(Fabric)**: 여러 엔드포인트와 스위치를 묶어 다수의 통신 경로를 제공하는 연결망이다.

</details>

```text
[NCCL 통신 소프트웨어] -- [GPU 엔드포인트 집합] -- [NVLink 물리 링크] -- [NVSwitch 패브릭]
```

선의 의미: 통신 엔드포인트가 NVLink 물리 링크를 통해 NVSwitch의 다대다 패브릭에 결합된 정적 연결망이다.

| 구성요소 | 책임 |
|:---|:---|
| NCCL 통신 소프트웨어 | 토폴로지 기반 **집단 통신 계획·실행** |
| GPU 엔드포인트 집합 | 통신 조각의 **송신·수신·축소 연산** |
| NVLink 물리 링크 | 피어 **직접 데이터 전송** |
| NVSwitch 패브릭 | 다대다 **경로 연결•분기** |

#### 한줄 요약

- NCCL이 경로를 정하면 NVLink와 NVSwitch가 GPU 사이의 데이터를 직접 전달한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **전체 축소(All-Reduce)**: 각 그래픽 처리 장치(Graphics Processing Unit, GPU)의 값을 하나로 집계한 뒤 완성된 결과를 모든 GPU에 배포하는 집단 통신이다.
- **축소-분산(Reduce-Scatter)**: 값을 합산하면서 최종 결과의 서로 다른 조각을 각 GPU가 나누어 갖는 단계이다.
- **전체-수집(All-Gather)**: 각 GPU가 가진 결과 조각을 서로 교환하여 모든 GPU가 전체 결과를 얻는 단계이다.
- **통신 조각(Communication Chunk)**: 큰 텐서를 집단 통신 파이프라인과 링크 특성에 맞게 나눈 전송 단위이다.

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

**동작 원리**

1. **토폴로지·조각 계획**: NCCL이 GPU 연결과 링크 대역폭에 맞춰 링·트리 경로와 텐서 조각 크기를 결정한다.
2. **Reduce-Scatter 실행**: GPU 수−1단계 동안 조각을 피어로 전달하고 수신 값을 로컬 값과 축소해 GPU별 완성 조각을 생성한다.
3. **All-Gather 실행**: GPU 수−1단계 동안 각 GPU의 완성 조각을 교환·수집해 모든 GPU에 전체 결과를 구성한다.
4. **전체 축소 완료**: 모든 조각의 수신과 축소가 끝난 뒤 완료 이벤트를 기록하고 후속 연산을 허용한다.

#### 한줄 요약

- NCCL은 토폴로지에 맞춰 Reduce-Scatter에서 조각을 합산하고 All-Gather에서 완성 조각을 모든 GPU에 배포한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **직접 NVLink(Direct NVLink)**: 소수 GPU를 점대점 링크로 직접 연결하여 피어 통신을 제공하는 구성이다.
- **NVSwitch 패브릭(NVSwitch Fabric)**: 스위치를 통해 다수 GPU에 다대다 NVLink 경로를 제공하는 구성이다.
- **주변 구성요소 상호연결 익스프레스(PCI Express, PCIe)**: 중앙 처리 장치(Central Processing Unit, CPU)와 범용 주변장치를 계층형 점대점 링크로 연결하는 표준 인터커넥트이다.

</details>

| GPU 연결 방식 | 직접 NVLink | NVSwitch | PCIe |
|:---|:---|:---|:---|
| 적용 기준 | 소수 GPU의 **빈번한 피어 통신** | 다수 GPU의 **집단 통신** | 범용 장치•**호스트 연결** |
| 핵심 특징 | GPU 간 **점대점 링크** | 다대다 **스위치 패브릭** | 범용 **계층형 패브릭** |
| 한계 | 링크 수•토폴로지•**세대 호환** | 시스템 비용•**전력•구성 범위** | 공유 대역폭•**스위치 홉** |

#### 한줄 요약

- 소수 GPU의 빈번한 피어 통신은 직접 NVLink, 다수 GPU의 다대다 집단 통신은 NVSwitch, 범용 호스트·장치 연결은 PCIe가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **프로세스•샤드 배치(Process•Shard Placement)**: 통신량이 많은 작업과 모델 조각을 가까운 그래픽 처리 장치(Graphics Processing Unit, GPU)와 링크에 배치하는 작업이다.
- **꼬리 지연(Tail Latency)**: 전체 통신 완료를 결정하는 가장 늦은 조각이나 경로의 지연이다.
- **통신•연산 중첩(Communication-computation Overlap)**: GPU 계산과 데이터 교환을 동시에 진행하여 통신 대기를 숨기는 기법이다.
- **링크 감시(Link Monitoring)**: 링크 오류와 협상 속도 및 대역폭 저하를 지속적으로 측정하는 운영 활동이다.
- **전체 축소(All-Reduce)**: 여러 그래픽 처리 장치(Graphics Processing Unit, GPU)의 값을 합산하고 결과를 모두에게 배포하는 집단 통신이다.
- **엔비디아 집단 통신 라이브러리(NVIDIA Collective Communications Library, NCCL)•엔비디아 DGX(NVIDIA DGX, DGX)**: GPU 집단 통신 라이브러리와 다중 GPU 시스템이다.
- **중앙 처리 장치(Central Processing Unit, CPU)•피시아이 익스프레스(Peripheral Component Interconnect Express, PCIe)**: 호스트 프로세서와 범용 장치 연결 경로이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 통신량이 많은 프로세스·샤드가 멀리 배치되어 **추가 홉·공유 링크 경합** | 링크 대역폭·홉 수에 맞춘 **프로세스·샤드 배치** | 가까운 피어 경로 사용으로 **원거리 통신 감소** |
| All-Reduce의 한 링크·GPU가 늦어 전체 단계의 **꼬리 지연 결정** | 통신 조각 크기·알고리즘과 **GPU별 계산·통신 부하 균형** 조정 | 가장 느린 단계 단축으로 **집단 통신 지연 완화** |
| 링크 오류나 세대·속도 협상 차이로 **경로 대역폭 축소** | 지속적인 링크 감시와 **지원 토폴로지·세대 호환성 검증** | 저속·오류 링크의 **조기 식별과 경로 격리** |
| 완료 전에 통신 버퍼를 재사용하거나 통신 대기 중 **연산기 유휴** | 버퍼 이벤트 수명을 보장하고 **통신·연산 중첩** 적용 | 데이터 손상 방지와 **GPU 가동률 향상** |

> **NVLink•NVSwitch**에서 NCCL 기울기 직접 집계

#### 한줄 요약

- GPU 배치를 NVLink•NVSwitch 경로에 맞추고 통신 조각을 조정해 All-Reduce의 느린 구간을 줄인다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **피어 통신(Peer Communication)**: 한 그래픽 처리 장치(Graphics Processing Unit, GPU)가 호스트 메모리를 경유하지 않고 다른 GPU와 직접 데이터를 교환하는 통신이다.
- **전대역 연결(Full-bandwidth Connectivity)**: 다수 엔드포인트 쌍이 동시에 통신해도 충분한 경로와 대역폭을 제공하는 연결 조건이다.
- **GPU 규모(GPU Scale)**: 하나의 시스템에서 함께 연결하고 집단 통신에 참여시키는 GPU의 수이다.

</details>

- 소수 GPU는 **NVLink**, 다수 GPU 전대역 연결은 **NVSwitch**을 선택한다.

#### 한줄 요약

- 소수 GPU는 NVLink로 직접 연결하고 다수 GPU의 전대역 연결에는 NVSwitch를 적용한다.
