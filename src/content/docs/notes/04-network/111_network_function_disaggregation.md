---
sidebar:
  order: 111
  label: "111. 네트워크 기능 분리"
  badge:
    text: "기출 · 30%"
    variant: note
title: "5G 기지국 아키텍처 혁신 : 네트워크 기능 분리 (RAN Disaggregation CU/DU/RU)"
date: "2026-08-22T08:15:00+09:00"
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

- **네트워크 기능 분리(Network Function Disaggregation / Functional Split)**: 단일 벤더의 독점적 일체형 하드웨어(BBU+RRH)로 구현되던 5G gNB(기지국)의 프로토콜 스택을 지연 시간 허용도와 연산 특성에 따라 **CU(중앙 장치)**, **DU(분산 장치)**, **RU(무선 장치)** 로 기능 분할하고 표준 인터페이스로 개방한 아키텍처.
- **3GPP 및 O-RAN 분할 옵션(Split Options)**: 3GPP가 정의한 Option 2(PDCP-RLC 분할: CU-DU 간 F1 인터페이스)와 O-RAN 얼라이언스가 채택한 Option 7-2x(High PHY-Low PHY 분할: DU-RU 간 개방형 eCPRI 프론트홀) 표준.

</details>

- 정의/개념: 기지국 소프트웨어와 하드웨어를 분리(Decoupling)하고, **CU(비실시간 RRC/PDCP 계층)**, **DU(실시간 RLC/MAC/High-PHY 계층)**, **RU(Low-PHY/RF 계층)** 로 프로토콜 스택을 세분화하여 개방형 상호운용성을 제공하는 **5G/6G 개방형 무선 접속망 아키텍처**
- 배경/필요성: 특정 단일 벤더(통신 장비사) 종속(Lock-in)으로 인한 높은 망 구축 비용(CapEx/OpEx)을 탈피하고, COTS(상용 x86) 서버 기반 가상화(vRAN) 및 멀티 벤더 조합을 통해 5G 기지국 투자 효율을 극대화할 요구

#### 한줄 요약
- gNB를 비실시간 CU, 실시간 DU, 전파 변환 RU로 기능 분리하여 개방형 표준 인터페이스로 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **미드홀(Midhaul) 및 프론트홀(Fronthaul)**: 코어망과 CU 사이의 백홀(Backhaul, 지연 $\le 10\sim 40\text{ms}$)에 더하여, CU와 DU 간의 F1 미드홀(지연 $\le 1\sim 5\text{ms}$) 및 DU와 RU 간의 eCPRI 초고속 프론트홀(지연 $\le 100\sim 250\mu\text{s}$)로 세분화된 전송 구간.
- **IEEE 1588v2 PTP / SyncE**: O-RAN 프론트홀 상에서 Massive MIMO 빔포밍 및 TDD 프레임 무선 간섭을 방지하기 위해 DU와 RU 간 나노초($\le \pm 65\text{ns}$) 단위의 정밀 위상/주파수 시간 동기화를 제공하는 기술.

</details>

- **중앙 집중식 풀링 및 자원 공유 (Centralized CU)**: 수십 개의 DU 상위 계층 처리를 데이터센터(CU Pool)에 가상화 인스턴스로 통합하여 연산 자원 효율 극대화
- **실시간 무선 스케줄링 현장 배치 (Distributed DU)**: 밀리초 단위의 HARQ 및 MAC 계층 스케줄링을 통신 셀 인근 DU에서 초저지연 집행
- **멀티 벤더 상호운용성 확보 (Open Fronthaul)**: O-RAN 7-2x 표준을 통해 A사 RU와 B사 DU를 이종 결합 가능한 개방형 생태계 구축

#### 한줄 요약
- CU 중앙 풀링, DU 현장 저지연 스케줄링, O-RAN 개방형 프론트홀 및 정밀 시간 동기화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **F1 인터페이스(3GPP TS 38.470)**: CU와 DU 간에 제어 평면(F1-C: F1AP over SCTP)과 사용자 평면(F1-U: GTP-U over UDP)을 분리하여 상호 운용성을 제공하는 표준 인터페이스.
- **eCPRI(enhanced Common Public Radio Interface)**: 레거시 CPRI의 막대한 광대역폭 낭비를 극복하기 위해, 이더넷 패킷 기반으로 IQ 데이터 및 실시간 제어 신호를 압축 전송하는 프론트홀 표준 프로토콜.

</details>

```text
[ 5G Core (AMF / UPF) ]
          │ (Backhaul: N2 / N3 Interface, $\le 20\text{ms}$)
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ CU: 중앙 장치 (Central Unit / Telco Cloud x86 Server) ]                │
│  ├─ CU-CP (Control Plane: RRC, PDCP-C) ── (이동성 관리, 보안, QoS 정책)  │
│  └─ CU-UP (User Plane: PDCP-U, SDAP) ──── (패킷 헤더 압축, 데이터 전송) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Midhaul: F1-C / F1-U Interface, $\le 5\text{ms}$)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ DU: 분산 장치 (Distributed Unit / Edge Cloud Server) ]                 │
│  ├─ RLC (Radio Link Control: 재전송, 순서 제어)                          │
│  ├─ MAC (Medium Access Control: 초고속 1ms HARQ, 무선 자원 스케줄링)     │
│  └─ High-PHY (Scrambling, Modulation, Layer Mapping, FFT/IFFT)           │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Open Fronthaul: O-RAN 7-2x eCPRI, $\le 250\mu\text{s}$)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ RU: 무선 장치 (Radio Unit / Antenna Site) ]                            │
│  ├─ Low-PHY (Digital Beamforming, CP 추가/제거)                          │
│  └─ RF 프론트엔드 (DAC/ADC, 전력 증폭기(PA), 안테나 배열)                │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 5G gNB가 코어망부터 안테나까지 Backhaul, Midhaul(F1), Fronthaul(eCPRI) 계층으로 세분화되어 기능별로 배치된 분리형 아키텍처

| 구성요소 | 기능 분할 계층 및 핵심 역할 | 전송 구간 | 지연 허용치 |
|:---|:---|:---|:---|
| **중앙 장치 (CU)** | **RRC, SDAP, PDCP 계층** (비실시간 제어 및 데이터 암호화/압축) | 백홀 / 미드홀 | $\le 10\sim 40\text{ms}$ |
| **F1 인터페이스** | 3GPP 표준 Option 2 분할 인터페이스 (F1-C: SCTP, F1-U: GTP-U) | 미드홀 (Midhaul) | $\le 1\sim 5\text{ms}$ |
| **분산 장치 (DU)** | **RLC, MAC, High-PHY 계층** (실시간 스케줄링 및 변복조) | 프론트홀 (Fronthaul) | $\le 100\sim 250\mu\text{s}$ |
| **개방형 프론트홀** | O-RAN Option 7-2x eCPRI (C/U/S/M-Plane) 이더넷 패킷 인터페이스 | 프론트홀 | $\le 100\sim 250\mu\text{s}$ |
| **무선 장치 (RU)** | **Low-PHY, D/A 변환, RF 증폭, 아날로그/디지털 빔포밍** | 무선 구간 | $\le \pm 65\text{ns}$ 동기 |

#### 한줄 요약
- CU(RRC/PDCP), F1 미드홀, DU(RLC/MAC/High-PHY), eCPRI 프론트홀, RU(Low-PHY/RF)가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **O-RAN 4대 통신 평면**: DU와 RU 간 eCPRI 프론트홀을 구성하는 4대 제어 평면: C-Plane(제어), U-Plane(IQ 데이터), S-Plane(PTP 시간 동기), M-Plane(관리/구성).

</details>

```text
1. 5G 코어망(UPF)에서 IP 패킷이 백홀을 통해 중앙 CU 풀로 수신
            │
            ▼
2. CU가 SDAP QoS 플로우 매핑 및 PDCP 암호화/무결성 보호를 거쳐 F1-U(GTP-U) 패킷 캡슐화
            │
            ▼
3. F1 미드홀을 거쳐 현장 DU로 전달 ➔ DU의 MAC 스케줄러가 무선 채널 품질에 따라 변조 방식(256QAM) 결정
            │
            ▼
4. DU의 High-PHY에서 심볼 변조 후 eCPRI 패킷으로 캡슐화 ➔ 초저지연 프론트홀을 통해 RU로 스트리밍
            │
            ▼
5. RU의 Low-PHY에서 빔포밍 가중치를 적용하고 DAC/RF 변환 ➔ 단말(UE)로 5G 전파 무선 방사
```

**동작 원리**

1. **상위 제어 중앙화**: RRC 연결 및 핸드오버 결정을 데이터센터 CU에서 처리하여 셀 간 간섭 최소화
2. **미드홀 전달**: 표준 IP 네트워크 상에서 GTP-U 터널을 통해 복수의 DU로 트래픽 다중화
3. **엄격한 스케줄링**: 1ms 이내에 처리되어야 하는 HARQ 피드백을 현장 엣지 DU에서 로컬 완결
4. **프론트홀 대역폭 절감**: Option 7-2x 분할을 적용하여 레거시 대비 프론트홀 필요 대역폭을 90% 이상 절감
5. **무선 송출**: RU가 PTP 시간 동기(S-Plane)에 맞춰 정확한 위상으로 고주파수(Sub-6/mmWave) RF 출력

#### 한줄 요약
- 코어망 패킷 수신, CU PDCP 암호화, DU MAC 스케줄링 및 eCPRI 패킷화, RU Low-PHY 빔포밍 송출 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **기지국 기능 분할 옵션(3GPP Split Options)**: 프로토콜 스택의 분리 지점에 따른 대표적 3단계 분류: Option 2 (CU-DU), Option 7-2x (O-RAN DU-RU), Option 8 (레거시 CPRI).

</details>

| 분할 표준 옵션 | Option 2 (3GPP F1 Split) | Option 7-2x (O-RAN Open Fronthaul) | Option 8 (레거시 CPRI Split) |
|:---|:---|:---|:---|
| **기능 분리 경계** | **PDCP 계층과 RLC 계층 사이** | **High-PHY 계층과 Low-PHY 계층 사이** | **PHY 계층 전체와 RF 계층 사이** |
| **적용 인터페이스** | **CU와 DU 간 미드홀 (Midhaul)** | **DU와 RU 간 개방형 프론트홀 (Fronthaul)**| 레거시 BBU와 RRH 간 프론트홀 |
| **프론트홀 대역폭** | 낮음 (사용자 데이터 전송률 비례) | **중간 (100MHz 4T4R 기준 ~10Gbps)** | **극도로 높음 (무선 대역폭/안테나 수 비례: 40Gbps+)**|
| **지연 시간 요건** | **비교적 완만 ($\le 1\sim 5\text{ms}$)** | **매우 엄격 ($\le 100\sim 250\mu\text{s}$)** | 극도로 엄격 ($\le 100\mu\text{s}$)|
| **주요 장점** | CU 중앙 풀링 자원 효율화 | **대역폭 절감 및 멀티 벤더 RU/DU 결합** | BBU 완전 중앙화 (광회선 비용 과다) |

#### 한줄 요약
- Option 2는 CU-DU 간 자원 풀링, Option 7-2x는 O-RAN 멀티 벤더 프론트홀 표준, Option 8은 레거시 CPRI 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **프론트홀 시간 동기화(Time Synchronization) 실패**: DU와 RU 간 PTP(IEEE 1588v2) 지터 및 패킷 손실로 인해 TDD 프레임 시작점 오차가 $\pm 1.5\mu\text{s}$를 초과하여 상/하향 링크 간 심각한 주파수 간섭이 발생하는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 벤더 간 DU-RU 연동 시 eCPRI M-Plane/C-Plane 비표준 파라미터로 인한 **상호운용성 결함** | **O-RAN 얼라이언스 규격 적합성 시험(IOT) 및 표준 프로파일 검증** 의무화 | 멀티 벤더 하드웨어/소프트웨어 간 100% 무결점 연동 보장 |
| 프론트홀 이더넷 패킷 지터로 인한 PTP 시간 동기 오차 및 **TDD 셀 간 무선 간섭 발생** | 프론트홀 스위치에 **IEEE 1588v2 Telecom Profile (G.8275.1) 및 SyncE 경계 클록(BC)** 적용 | 시간 동기 오차 $\le \pm 65\text{ns}$ 극소화 및 간섭 없는 안정적 5G 서비스 유지 |
| Massive MIMO 도입 시 프론트홀 트래픽 폭증으로 인한 **광선로 대역폭 고갈 및 구축 비용 증가** | **Option 7-2x 기반 IQ 데이터 압축(BFP: Block Floating Point)** 및 WDM 전송 | 프론트홀 필요 대역폭 60% 절감 및 광코어 투자비용 대폭 감축 |

#### 한줄 요약
- O-RAN IOT 시험으로 상호운용성을 보장하고, PTP G.8275.1로 동기 오차를 방지하며, BFP 압축으로 대역폭을 절감한다.

## Ⅶ. 결론

- 5G 고도화 및 6G 시대를 향한 통신 인프라의 유연성과 투자 효율성을 극대화하기 위해 **기지국 네트워크 기능 분리(CU/DU/RU Disaggregation)** 는 거스를 수 없는 글로벌 표준 아키텍처로 자리 잡았으며, 실무 구축 시 **3GPP Option 2 F1 및 O-RAN Option 7-2x 표준 준수**, **IEEE 1588v2 기반 초정밀 시간 동기화**, **클라우드 네이티브 가상화(vRAN/O-RAN)** 를 결합하여 차세대 개방형 자율 이동통신망을 완성

#### 한줄 요약
- 3GPP F1 및 O-RAN 7-2x 기반의 CU/DU/RU 기능 분리와 정밀 동기화를 통해 개방형 고효율 5G/6G 기지국을 실현한다.
