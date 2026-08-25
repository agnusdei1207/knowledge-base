---
sidebar:
  order: 83
  label: "083. 시간 민감 네트워킹 (TSN)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "결정론적 이더넷 표준 : 시간 민감 네트워킹 (TSN)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 83
extra:
  question_no: "83"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "IEEE 802.1AS 시간 동기화, IEEE 802.1Qbv TAS(GCL), IEEE 802.1Qbu 프레임 선점, IEEE 802.1CB FRER"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TSN (Time-Sensitive Networking)**: 표준 이더넷 상에서 초정밀 시간 동기화와 결정론적(Deterministic) 지연 상한 및 무손실을 보장하는 표준 프로토콜 세트.
- **Deterministic Latency**: 혼잡 상태와 무관하게 패킷이 사전 정의된 최대 최악 지연 시간(Worst-Case Latency) 내에 100% 도달함을 보증하는 특성.

</details>

- 정의/개념: 표준 이더넷 상에서 **초정밀 시간 동기화(802.1AS), 시간 스케줄링(802.1Qbv), 프레임 선점(802.1Qbu), 무손실 이중화(802.1CB)를 제공하는 결정론적 통신 기술군**
- 배경/필요성: 표준 이더넷의 비결정론적 최선형(Best-Effort) 전송 한계로 인한 **지터 폭증, 실시간 제어 패킷의 데드라인 초과 및 차량/산업 백본 적용 불가**

#### 한줄 요약
- 802.1AS 정밀 동기화, 802.1Qbv GCL 스케줄링, 802.1Qbu 프레임 선점, 802.1CB 무손실 이중화를 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TAS (Time-Aware Shaper / 802.1Qbv)**: 전역 시간표(GCL)에 따라 8개 송출 큐의 게이트를 On/Off 제어하여 실시간 패킷을 무지연 전송하는 셰이퍼.
- **Frame Preemption (802.1Qbu / 802.3br)**: 긴 비실시간 프레임 전송 도중 긴급 실시간 프레임이 도착하면 전송을 일시 중단(선점)하고 우선 송출하는 기술.

</details>

- **마이크로초($\le 1\mu\text{s}$) 미만 초정밀 시간 동기화**: IEEE 802.1AS(gPTP)를 통해 **전체 네트워크 브리지와 종단의 시계를 나노초 단위 동기화**
- **시간 인식 셰이퍼(TAS) 기반 버퍼 제로 지연**: GCL 타임 슬롯에 맞춰 게이트를 개폐하여 **실시간 큐 패킷의 버퍼 대기 지연 원천 제거**
- **하드웨어 레벨 프레임 선점(Preemption)**: 긴 비실시간 프레임을 분할 전송하여 **긴급 패킷의 블로킹 지연 극소화**
- **프레임 복제 및 무손실 중복 제거(FRER)**: IEEE 802.1CB를 통해 **다중 경로 동시 전송으로 단선 시 0ms 무중단 전환**

#### 한줄 요약
- 802.1AS 정밀 동기화, 802.1Qbv GCL 스케줄링, 802.1Qbu 프레임 선점, 802.1CB 무손실 이중화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CNC (Centralized Network Configurator)**: 토폴로지와 대역폭을 파악하여 최적 경로와 스위치별 GCL 시간표를 계산·배포하는 SDN 제어기 (802.1Qcc).
- **FRER (Frame Replication and Elimination for Reliability / 802.1CB)**: 프레임을 2개 이상의 독립 경로로 복제 송신하고 수신단에서 중복분을 제거하는 기술.

</details>

```text
[IEEE TSN 결정론적 이더넷 아키텍처]
|-- Management Layer (CUC 사용자 요구 접수 -> CNC 중앙 네트워크 구성기 GCL 연산 및 주입)
`-- Time Domain (IEEE 802.1AS gPTP Grandmaster Clock: $\le 1\mu\text{s}$ 정밀 동기)
`-- TSN End Station: Talker (GCL 타임슬롯에 맞춰 실시간 패킷 송출)
`-- TSN Bridges (802.1Qbv TAS + 802.1Qbu 프레임 선점 + 802.1CB FRER 이중화)
    `-- Egress Queues: [ Queue 7: Gate OPEN (Express) ] / [ Queue 0~6: Gate CLOSED ]
`-- TSN End Station: Listener (최악 지연 상한 내 무손실 결정론 수신)
```

선의 의미: CNC가 CUC의 요구를 기반으로 GCL 시간표를 계산하여 gPTP로 동기화된 TSN 브리지들에 배포하고 Talker부터 Listener까지 결정론적 스트림이 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **시간 동기화 엔진** | Grandmaster Clock을 기준으로 **전 노드의 시간 편차를 $\le 1\mu\text{s}$로 보정** | IEEE 802.1AS |
| **TAS 스케줄러** | GCL(Gate Control List)에 따라 **8개 송출 큐의 Gate Open/Close 제어** | IEEE 802.1Qbv |
| **프레임 선점기** | 저우선순위 패킷을 **eMAC/pMAC 계층에서 분할 및 선점 전송** | IEEE 802.1Qbu |
| **FRER 복제기** | 스트림 식별 및 시퀀스 번호로 **다중 경로 복제 및 수신단 중복 제거** | IEEE 802.1CB |
| **CNC / CUC 컨트롤러**| E2E 지연 분석, **수용 제어(Admission Control), GCL 스케줄링 연산** | IEEE 802.1Qcc |

#### 한줄 요약
- 802.1AS 시간 동기, 802.1Qbv TAS, 802.1Qbu 선점, 802.1CB FRER, 802.1Qcc CNC가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **GCL (Gate Control List)**: 각 타임 인터벌마다 어떤 우선순위 큐의 게이트를 열고(Open) 닫을지(Close) 8비트 마스크로 정의한 시간표.

</details>

```text
TSN 스트림 등록, GCL 스케줄링 및 결정론적 전송 파이프라인
        │
   1. [스트림 요구 등록] Talker가 주기, 패킷 크기, 최대 허용 지연을 CUC/CNC에 등록
        │
   2. [CNC 전역 스케줄링] CNC가 전역 토폴로지를 분석하여 충돌 없는 GCL 시간표 산출
        │
   3. [브리지 GCL 주입] NETCONF/RESTCONF로 경로상 브리지 레지스터에 GCL 매트릭스 적재
        │
   4. [802.1AS 동기 송출] 모든 노드가 정밀 시계에 맞춰 해당 타임 슬롯에 실시간 스트림 송출
        │
   ▼
5. [선점 및 FRER 수신] 브리지에서 저우선 프레임 선점 및 FRER 이중화로 데드라인 내 무손실 도착
```

#### 한줄 요약
- 스트림 등록 → CNC GCL 연산 → 브리지 시간표 주입 → 802.1AS 동기 송출 → 무손실 결정론 수신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TAS (802.1Qbv)** vs **Frame Preemption (802.1Qbu)** vs **ATS (802.1Qcr)**: 절대 시간표 게이트 제어, 하드웨어 선점 분할, 시계 동기화 없는 비동기 셰이핑.

</details>

| 비교 항목 | 시간 인식 셰이퍼 (TAS / 802.1Qbv) | 프레임 선점 (Preemption / 802.1Qbu) | 비동기 트래픽 셰이퍼 (ATS / 802.1Qcr) |
|:---|:---|:---|:---|
| **제어 메커니즘** | **글로벌 시간표(GCL) 기반 Gate On/Off**| **저우선순위 패킷 하드웨어 분할 및 선점**| **토큰 버킷 기반 홉별 비동기 레이트 제어**|
| **글로벌 시간 동기**| **필수 ($\le 1\mu\text{s}$ 정밀 동기 요구)** | 선택적 (단독 동작 가능) | **불필요 (시간 동기화 오버헤드 없음)** |
| **지연 보증 수준** | **최고 수준 (나노초~마이크로초 결정론)** | 우수 (패킷 블로킹 지연 제거) | 통계적 최악 지연 상한 보장 |
| **대역폭 오버헤드** | 가드 밴드로 인한 미세 유휴 발생 | 프레임 분할/재조립 오버헤드 미세 발생 | 가드 밴드 없음 (대역폭 100% 활용) |
| **주요 적용 영역** | **초정밀 산업 로봇, CNC 공작기계** | **차량용 백본 이더넷, 고속 카메라 스트림**| **대규모 혼합 트래픽 공장망, 코어망** |

#### 한줄 요약
- TAS는 절대 시간표 기반 최고 정밀도 제어, 선점은 블로킹 방지, ATS는 시계 동기화 없는 비동기 제어에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Guard Band (가드 밴드)**: TAS 환경에서 실시간 전용 타임 슬롯 시작 직전 비실시간 프레임 송출을 차단하여 윈도우 침범을 막는 안전 갭.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비실시간 프레임 전송으로 인한 실시간 윈도우 침범 및 가드 밴드 대역폭 낭비 | **`IEEE 802.1Qbu 프레임 선점(Preemption)` 기술을 TAS와 결합** | 가드 밴드 크기를 1/10로 축소하고 실시간 지연 원천 차단 |
| 물리 링크/스위치 장애 시 패킷 유실 및 실시간성 붕괴 | **`IEEE 802.1CB FRER (프레임 복제 및 중복 제거)` 무손실 이중화** | 링크 단선 시 0ms 무중단 페일오버 및 제로 패킷 손실 |
| 대규모 브리지 경유 시 누적 지터로 인한 802.1AS 시간 오차 발생 | **`하드웨어 타임스탬핑 PHY 칩셋` 및 Transparent Clock(TC) 적용** | 100홉 통과 시에도 $1\mu\text{s}$ 이내 동기 정밀도 유지 |
| 다중 스트림 추가 시 실시간 GCL 시간표 재연산 병목 | **`계층적 분산 CNC 스케줄러` 및 증분 스케줄링(Incremental) 적용** | GCL 재연산 시간 단축 및 동적 스트림 추가 수용 |

#### 한줄 요약
- 프레임 선점으로 가드 밴드를 축소하고, FRER로 무중단 이중화를 달성하며, 하드웨어 타임스탬핑으로 동기 정밀도를 보장한다.

## Ⅶ. 결론

- 스마트 팩토리, SDV 차량 이더넷, 차세대 6G 산업용 통신의 결정론적 전송 요구를 만족하기 위해 **IEEE TSN 표준 아키텍처를 도입**하되, 고성능 실시간성을 확보하기 위해 **IEEE 802.1AS 시간 동기, 802.1Qbv TAS, 802.1Qbu 프레임 선점, 802.1CB 무손실 이중화 및 CNC 오케스트레이션**을 통합 구축하여 초고신뢰·초저지연 결정론적 네트워크 인프라 완성

#### 한줄 요약
- TSN은 802.1AS 시간 동기, 802.1Qbv 시간 스케줄링, 802.1Qbu 선점을 결합하여 표준 이더넷 위에서 결정론적 초저지연을 실현하는 차세대 네트워크 기술이다.