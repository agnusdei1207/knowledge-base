---
sidebar:
  order: 36
  label: "036. 5G 3대 서비스"
  badge:
    text: "기출 · 30%"
    variant: note
title: "5G 3대 서비스 시나리오 : eMBB•URLLC•mMTC (5G Services)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 36
extra:
  question_no: "36"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "ITU-R 5G 3대 서비스 시나리오 및 네트워크 슬라이싱 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **eMBB (Enhanced Mobile Broadband)**: 최대 20Gbps 다운링크와 광대역 주파수를 통해 대용량 멀티미디어를 전송하는 초고속 서비스.
- **URLLC (Ultra-Reliable Low Latency)**: 무선 구간 1ms 이하 지연과 99.999% 무결성 신뢰도를 보장하는 초고신뢰 저지연 서비스.
- **mMTC (Massive Machine Type)**: $1\text{km}^2$ 당 100만 개 이상의 저전력 센서 단말을 수용하는 대규모 사물 통신 서비스.

</details>

- 정의/개념: ITU-R(IMT-2020)이 정의한 5G 3대 서비스로 **초고속(eMBB), 초저지연·초고신뢰(URLLC), 대규모 접속(mMTC)을 단일 망에 분할 수용하는 통신 체계**
- 배경/필요성: 4G LTE 단일 범용 통신의 한계로 인한 **초대용량 미디어(20Gbps), 자율주행 1ms 초저지연, 100만 개/$\text{km}^2$ 대규모 IoT 단말 동시 수용 불가**

#### 한줄 요약
- eMBB(초고속), URLLC(초저지연/고신뢰), mMTC(초연결)를 네트워크 슬라이싱으로 단일 인프라에 통합한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Network Slicing**: 단일 물리 5G 네트워크를 가상화(NFV/SDN)하여 eMBB, URLLC, mMTC 전용의 독립 가상망으로 격리 제공하는 기술.
- **5QI (5G QoS Identifier)**: 5G 서비스별 지연 허용 한도, 패킷 손실률, 우선순위를 정의하는 QoS 식별자.

</details>

- **eMBB**: 밀리미터파(mmWave), Massive MIMO, 빔포밍을 통한 **최대 20Gbps 초고속 대역폭 제공**
- **URLLC**: 가변 부반송파(SCS), Mini-slot 선점형 스케줄링 및 MEC 전진 배치를 통한 **1ms 초저지연 달성**
- **mMTC**: 협대역(NB-IoT), 극저전력 수면 모드(PSM/eDRX)를 통한 **100만 개/$\text{km}^2$ 단말 수용**

#### 한줄 요약
- eMBB는 대역폭, URLLC는 1ms 지연과 신뢰성, mMTC는 저전력 대규모 접속을 지향한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **UPF (User Plane Function)**: 5G 코어에서 실제 사용자 데이터 트래픽의 고속 라우팅 및 QoS 집행을 전담하는 데이터 플레인 노드.
- **MEC (Mobile Edge Computing)**: 지연 시간을 단축하기 위해 기지국(gNB) 인접 위치에 컴퓨팅 자원과 로컬 UPF를 배치하는 아키텍처.

</details>

```text
[5G 이기종 단말 트래픽의 3대 서비스 분기 아키텍처]
|-- Wireless Terminals (스마트폰 / 자율주행차 / 스마트 미터기 센서)
`-- 5G RAN (gNB: 가변 뉴머롤로지 SCS 15~120kHz, Mini-slot 스케줄러)
    |-- eMBB Slice: Massive MIMO 빔포밍 -> 중앙 클라우드 Core UPF (인터넷 백본 연동)
    |-- URLLC Slice: Mini-slot Preemption -> 기지국 인접 Local UPF & MEC Server (1ms 초저지연)
    `-- mMTC Slice: NB-IoT / Cat-M1 -> 경량 C-Plane 제어 코어 (AMF/SMF/NEF)
```

선의 의미: 계층 및 단말 요구에 따라 RAN에서 가변 뉴머롤로지로 분할되고 코어망에서 중앙 UPF, 로컬 MEC, 경량화 코어로 분기되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **gNB 가변 뉴머롤로지** | 부반송파 간격(SCS 15~120kHz)과 슬롯 길이를 **서비스별(eMBB/URLLC/mMTC) 가변 최적화** | RAN 슬라이싱 |
| **로컬 UPF / MEC** | 기지국 인접 지점에서 **로컬 트래픽 브레이크아웃(LBO)을 수행하여 왕복 지연 1ms 보장** | **URLLC 특화** |
| **중앙 집중형 UPF** | 인터넷 백본과 직접 연동하여 **대용량 트래픽의 초고속 기가비트 라우팅 및 과금 처리** | **eMBB 특화** |
| **경량 제어 평면 (AMF/SMF)**| 대규모 센서 단말의 간헐적 접속 시그널링 부하를 **경량화하여 흡수하고 절전 관리** | **mMTC 특화** |

#### 한줄 요약
- 가변 뉴머롤로지 RAN, 로컬 MEC/UPF, 중앙 UPF, 제어 평면 최적화 모듈이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Mini-slot (비슬롯 기반 스케줄링)**: 표준 14개 심볼 슬롯을 기다리지 않고 2~7개 심볼 단위로 즉시 무선 자원을 선점하는 URLLC 전용 스케줄링.

</details>

```text
5G 3대 서비스 트래픽 분기 및 슬라이스 파이프라인
        │
   1. [단말 접속 및 서비스 식별] S-NSSAI 및 5QI 기반 요구사항 분류
   ┌────┼───────────────────────────┬───────────────────────────┐
   │    │                           │                           │
  [eMBB 요청]                     [URLLC 요청]                [mMTC 요청]
   │    │                           │                           │
2A. mmWave & Massive MIMO        2B. Mini-slot 선점 스케줄링   2C. NB-IoT 협대역 채널
    중앙 UPF 라우팅                  로컬 MEC UPF 직결           PSM / eDRX 절전 구성
   │    │                           │                           │
   └────┴───────────────────────────┴───────────────────────────┘
        ▼
   3. 종단 간(E2E) 서비스 SLA 보장 및 데이터 전송 완료
```

#### 한줄 요약
- 서비스 식별 → eMBB(광대역/중앙UPF), URLLC(미니슬롯/MEC), mMTC(협대역/절전) 분기 경로 확립 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **PSM (Power Saving Mode)**: 단말이 데이터 송수신 후 수신 회로를 끄고 깊은 수면 상태로 진입하여 배터리를 수년간 유지하는 기술.

</details>

| 비교 항목 | 초고속 통신 (eMBB) | 초저지연 통신 (URLLC) | 대규모 사물 통신 (mMTC) |
|:---|:---|:---|:---|
| **핵심 성능 목표** | **최대 20Gbps (체감 100Mbps)** | **무선 1ms (E2E 5ms 이하), 99.999%** | **$10^6 \text{ devices}/\text{km}^2$, 배터리 10년** |
| **주요 무선 기술** | **mmWave (28GHz), Massive MIMO** | **Mini-slot, Preemption, 가변 SCS** | **NB-IoT, eMTC, PSM, eDRX** |
| **코어망 아키텍처**| 대용량 패킷 스위칭 (중앙 UPF) | **MEC (모바일 엣지 컴퓨팅) 전진 배치**| 제어 평면 시그널링 최적화 코어 |
| **주요 적용 분야** | 4K/8K 실시간 중계, AR/VR, 홀로그램 | **자율주행(V2X), 원격 수술, 스마트팩토리**| 원격 검침, 환경 센서, 스마트 물류 |

#### 한줄 요약
- eMBB는 대역폭(20Gbps), URLLC는 1ms 저지연과 신뢰성, mMTC는 대규모 연결($10^6/\text{km}^2$)을 목표로 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Preemption (선점형 스케줄링)**: URLLC 긴급 패킷 발생 시 이미 진행 중인 eMBB 전송 자원을 즉시 중단하고 URLLC 패킷을 최우선 전송하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대용량 eMBB 트래픽 버스트로 인한 URLLC 트래픽 지연 및 간섭 | **`선점형 스케줄링(Preemption)` 및 무선 하드 슬라이싱(Hard Slicing)** | eMBB 간섭 차단 및 URLLC 1ms 지연 시간 SLA 보증 |
| 코어망 원거리 전송 지연으로 인한 URLLC 종단 지연(5ms) 초과 | 기지국 인접 **`MEC(Mobile Edge Computing) 및 분산 로컬 UPF` 구축** | 물리적 전송 거리 단축 및 E2E 초저지연 달성 |
| 수백만 mMTC 단말의 동시 재접속 시 제어 평면(AMF/SMF) 시그널링 폭증 | **접속 시도 `백오프(Back-off) 제어` 및 비접속(Connectionless) 전송** | 제어 평면 과부하 방지 및 코어망 안정성 유지 |
| 28GHz 밀리미터파(mmWave) 대역의 높은 경로 손실 및 장애물 차단 | **`빔포밍(Beamforming)` 및 소형 기지국(Small Cell) 고밀도 구축** | 전파 도달 거리 극복 및 음영 지역 제거 |

#### 한줄 요약
- 선점형 스케줄링, MEC 로컬 UPF, 백오프 접속 제어, 빔포밍 Small Cell로 운영한다.

## Ⅶ. 결론

- 차세대 5G/6G 이동통신 인프라에서 상충하는 3대 서비스 요구조건을 완벽히 수용하기 위해 **E2E 네트워크 슬라이싱 아키텍처를 표준 수립**하고, 산업용/자율주행 현장에는 **MEC 기반 로컬 UPF**를 배치하며, 대규모 센서 환경에는 **경량화 코어 제어 평면과 절전 기술**을 결합하여 지능형 융합 네트워크 완성

#### 한줄 요약
- 5G 3대 서비스는 eMBB, URLLC, mMTC의 차별화된 요구를 네트워크 슬라이싱과 MEC를 통해 단일 망에서 실현하는 핵심 서비스 체계다.