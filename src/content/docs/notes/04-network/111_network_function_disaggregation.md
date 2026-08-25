---
sidebar:
  order: 111
  label: "111. 네트워크 기능 분리"
  badge:
    text: "기출 · 30%"
    variant: note
title: "5G 기지국 아키텍처 혁신 : 네트워크 기능 분리"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 111
extra:
  question_no: "111"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "3GPP gNB 분리(Option 2: CU-DU F1, Option 7-2x: DU-RU O-RAN eCPRI), 백홀/미드홀/프론트홀"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Functional Split (기능 분리)**: 5G 기지국 프로토콜 스택을 지연 시간과 연산 특성에 따라 CU, DU, RU로 분할하고 표준 인터페이스로 연결하는 아키텍처.
- **3GPP Option 2 & O-RAN Option 7-2x**: CU-DU 간 F1 미드홀 표준(Option 2)과 DU-RU 간 개방형 eCPRI 프론트홀 표준(Option 7-2x).

</details>

- 정의/개념: 기지국 프로토콜 스택을 **CU(RRC/PDCP), DU(RLC/MAC/High-PHY), RU(Low-PHY/RF)로 분할하고 표준 인터페이스로 개방한 5G 기지국 분리 아키텍처**
- 배경/필요성: 단일 벤더의 폐쇄형 일체형(BBU-RRH) 기지국 구조로 인한 **벤더 락인, 레거시 CPRI 광회선 비용 과다 및 민첩한 망 확장 불가**

#### 한줄 요약
- CU, DU, RU 기능 분할과 개방형 인터페이스(F1/eCPRI)를 통해 기지국 가상화와 투자비 절감을 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multi-Vendor Interoperability**: 표준화된 개방형 인터페이스(F1/eCPRI)를 통해 A사 CU, B사 DU, C사 RU를 자유롭게 조합하여 구성할 수 있는 상호운용성.
- **CPRI vs eCPRI**: 무선 안테나 수에 비례하여 광회선 대역폭이 폭증하던 CPRI(Option 8)와 사용자 실제 트래픽에 비례하여 대역폭을 90% 절감하는 eCPRI(Option 7-2x).

</details>

- **멀티 벤더 상호운용성(Multi-Vendor)**: 독점 하드웨어를 탈피하여 **이종 벤더 간 CU, DU, RU 자유로운 조합 구성**
- **프론트홀 대역폭 90% 이상 절감**: Option 7-2x 분할을 적용하여 **디지털 변복조 데이터를 eCPRI 이더넷 패킷으로 전송**
- **클라우드 네이티브 가상화(vRAN/O-RAN)**: CU와 DU 기능을 **범용 COTS 서버 상에서 컨테이너(CNF) 형태로 유연하게 배포**

#### 한줄 요약
- 멀티 벤더 상호운용성, eCPRI 기반 프론트홀 대역폭 절감, COTS 기반 가상화 배포를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CU vs DU vs RU**: 비실시간 제어를 담당하는 중앙 장치(CU), 실시간 1ms 스케줄링을 담당하는 분산 장치(DU), RF 송수신을 담당하는 무선 장치(RU).

</details>

```text
[5G gNB 기능 분리 및 전송 구간 아키텍처]
|-- 5G Core Network (5GC: AMF, UPF)
`-- Centralized Unit (CU: Data Center / RRC 제어, SDAP QoS, PDCP 암호화)
    `-- Midhaul (3GPP F1 Interface: F1-C SCTP, F1-U GTP-U, 지연 $\le 1\sim 5\text{ms}$)
`-- Distributed Unit (DU: Edge Cloud Server / RLC 재전송, MAC 1ms 스케줄링, High-PHY)
    `-- Open Fronthaul (O-RAN Option 7-2x eCPRI: C/U/S/M-Plane, 지연 $\le 250\mu\text{s}$)
`-- Radio Unit (RU: Antenna Site / Low-PHY 디지털 빔포밍, DAC/ADC, RF 증폭)
```

선의 의미: 5G gNB가 코어망부터 안테나까지 Backhaul, Midhaul(F1), Fronthaul(eCPRI) 계층으로 세분화되어 기능별로 배치된 구조

| 구성요소 | 핵심 엔지니어링 책임 | 전송 구간 | 지연 허용치 |
|:---|:---|:---|:---|
| **중앙 장치 (CU)** | **RRC, SDAP, PDCP 계층** (비실시간 제어 및 데이터 암호화) | 백홀 / 미드홀 | $\le 10\sim 40\text{ms}$ |
| **F1 인터페이스** | **3GPP Option 2 분할** (F1-C: SCTP, F1-U: GTP-U) | 미드홀 (Midhaul) | $\le 1\sim 5\text{ms}$ |
| **분산 장치 (DU)** | **RLC, MAC, High-PHY 계층** (실시간 스케줄링 및 변복조) | 프론트홀 | $\le 100\sim 250\mu\text{s}$ |
| **개방형 프론트홀** | **O-RAN Option 7-2x eCPRI** (C/U/S/M-Plane 이더넷 인터페이스) | 프론트홀 | $\le 100\sim 250\mu\text{s}$ |
| **무선 장치 (RU)** | **Low-PHY, D/A 변환, RF 증폭, 아날로그/디지털 빔포밍** | 무선 구간 | $\le \pm 65\text{ns}$ 동기 |

#### 한줄 요약
- CU(RRC/PDCP), F1 미드홀, DU(RLC/MAC/High-PHY), eCPRI 프론트홀, RU(Low-PHY/RF)가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **O-RAN 4대 통신 평면**: DU와 RU 간 eCPRI 프론트홀을 구성하는 4대 제어 평면: C-Plane(제어), U-Plane(IQ 데이터), S-Plane(PTP 시간 동기), M-Plane(관리/구성).

</details>

```text
5G 기능 분리 기지국 패킷 수신, 변복조 및 무선 방사 파이프라인
        │
   1. [코어망 패킷 수신] 5G 코어망(UPF)에서 IP 패킷이 백홀을 통해 중앙 CU 풀로 수신
        │
   2. [PDCP 암호화 및 F1 전달] CU가 PDCP 암호화/무결성 보호를 거쳐 F1-U(GTP-U)로 DU 전달
        │
   3. [MAC 스케줄링 및 High-PHY] DU의 MAC 스케줄러가 256QAM 변조 후 High-PHY 심볼 변환
        │
   4. [eCPRI 프론트홀 스트리밍] eCPRI 패킷으로 캡슐화하여 초저지연 프론트홀을 통해 RU로 전달
        │
   ▼
5. [Low-PHY 빔포밍 및 RF 방사] RU의 Low-PHY에서 빔포밍 가중치를 적용하고 DAC/RF 안테나 방사
```

#### 한줄 요약
- 코어망 패킷 수신 → CU PDCP 암호화 → DU MAC 스케줄링 및 eCPRI 패킷화 → RU Low-PHY 빔포밍 송출 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Option 2 (CU-DU)** vs **Option 7-2x (O-RAN DU-RU)** vs **Option 8 (레거시 CPRI)**.

</details>

| 분할 표준 옵션 | Option 2 (3GPP F1 Split) | Option 7-2x (O-RAN Open Fronthaul) | Option 8 (레거시 CPRI Split) |
|:---|:---|:---|:---|
| **기능 분리 경계** | **PDCP 계층과 RLC 계층 사이** | **High-PHY 계층과 Low-PHY 계층 사이** | **PHY 계층 전체와 RF 계층 사이** |
| **적용 인터페이스** | **CU와 DU 간 미드홀 (Midhaul)** | **DU와 RU 간 개방형 프론트홀 (Fronthaul)**| 레거시 BBU와 RRH 간 프론트홀 |
| **프론트홀 대역폭** | 낮음 (사용자 데이터 전송률 비례) | **중간 (100MHz 4T4R 기준 ~10Gbps)** | **극도로 높음 (무선 대역폭 비례: 40Gbps+)**|
| **지연 시간 요건** | **비교적 완만 ($\le 1\sim 5\text{ms}$)** | **매우 엄격 ($\le 100\sim 250\mu\text{s}$)** | 극도로 엄격 ($\le 100\mu\text{s}$)|
| **주요 장점** | **CU 중앙 풀링 자원 효율화** | **대역폭 절감 및 멀티 벤더 결합** | BBU 완전 중앙화 (광회선 비용 과다) |

#### 한줄 요약
- Option 2는 CU-DU 간 자원 풀링, Option 7-2x는 O-RAN 멀티 벤더 프론트홀 표준, Option 8은 레거시 CPRI 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PTP G.8275.1 Telecom Profile**: 프론트홀 이더넷 스위치 전 구간에 IEEE 1588v2 경계 클록(Boundary Clock)을 적용하여 시간 동기 오차를 $\pm 65\text{ns}$ 이하로 억제하는 통신 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 벤더 간 DU-RU 연동 시 eCPRI 비표준 파라미터로 인한 **상호운용성 결함** | **`O-RAN 얼라이언스 규격 적합성 시험(IOT)` 및 표준 프로파일 검증** | 멀티 벤더 하드웨어 간 100% 무결점 연동 보장 |
| 프론트홀 패킷 지터로 인한 동기 오차 및 **TDD 셀 간 무선 간섭 발생** | **`IEEE 1588v2 Telecom Profile (G.8275.1) 및 SyncE 경계 클록`** | 시간 동기 오차 $\le \pm 65\text{ns}$ 극소화 및 간섭 제거 |
| Massive MIMO 도입 시 프론트홀 트래픽 폭증으로 인한 **광선로 비용 증가** | **`Option 7-2x 기반 IQ 압축(Block Floating Point)` 및 WDM 전송** | 프론트홀 필요 대역폭 60% 절감 및 투자비용 절감 |
| 가상화 DU(vDU)의 x86 CPU 부하 과다로 인한 실시간 High-PHY 처리 지연 | **FPGA/eASIC/GPU 기반 `하드웨어 인라인 가속 카드(vDU Offload)`** | 실시간 변복조 처리율 5배 향상 및 CPU 코어 절감 |

#### 한줄 요약
- O-RAN IOT 시험으로 상호운용성을 보장하고, PTP G.8275.1로 동기 오차를 방지하며, BFP 압축으로 대역폭을 절감한다.

## Ⅶ. 결론

- 5G 고도화 및 6G 시대를 향한 통신 인프라의 유연성과 투자 효율성을 극대화하기 위해 **기지국 네트워크 기능 분리(CU/DU/RU Disaggregation)를 핵심 표준 아키텍처로 도입**하되, 실무 구축 시 **3GPP Option 2 F1 및 O-RAN Option 7-2x 표준 준수, IEEE 1588v2 기반 초정밀 시간 동기화, 클라우드 네이티브 가상화(vRAN/O-RAN)**를 결합하여 차세대 개방형 자율 이동통신망 완성

#### 한줄 요약
- 네트워크 기능 분리는 3GPP F1 및 O-RAN 7-2x 기반의 CU/DU/RU 분할과 정밀 동기화를 통해 개방형 고효율 기지국을 실현하는 핵심 기술이다.