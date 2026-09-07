---
sidebar:
  order: 111
  label: "111. 네트워크 기능 분리"
  badge:
    text: "기출 · 30%"
    variant: note
title: "5G 기지국 아키텍처 혁신 : 네트워크 기능 분리"
date: "2026-09-07T14:00:00+09:00"
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

- 정의/개념: 기지국 스택을 **CU·DU·RU**로 나눈 개방형 구조
- 배경/필요성: 전통적인 4G/5G 무선 접속망(RAN)의 모놀리식 BBU(기저대역 장치)와 독점 규격 CPRI(Option 8) 프론트홀 구조는 특정 벤더 하드웨어 종속성(Lock-in), 안테나 수(Massive MIMO) 증가에 따른 프론트홀 광선로 대역폭 폭증 및 기지국 증설/업그레이드 비용 급증 문제를 초래함에 따라, 3GPP 및 O-RAN 표준에 따라 기지국 프로토콜 스택을 지연 민감도와 연산 특성에 맞추어 CU(중앙 장치), DU(분산 장치), RU(무선 장치)로 분할하고 개방형 인터페이스(F1 미드홀, Option 7-2x eCPRI 프론트홀)로 연결하는 네트워크 기능 분리(Network Function Disaggregation / Split) 기술을 도입하여 **멀티 벤더 이종 장비 간 자유로운 상호운용성 확보, 프론트홀 대역폭 90% 이상 절감 및 범용 COTS x86/ARM 서버 기반 가상화 기지국(vRAN/O-RAN) 생태계 구축**을 달성할 필요

#### 한줄 요약
- CU, DU, RU 기능 분할과 개방형 인터페이스(F1/eCPRI)를 통해 기지국 가상화와 투자비 절감을 달성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multi-Vendor Interoperability**: 표준화된 개방형 인터페이스(F1/eCPRI)를 통해 A사 CU, B사 DU, C사 RU를 자유롭게 조합하여 구성할 수 있는 상호운용성.
- **CPRI vs eCPRI**: 무선 안테나 수에 비례하여 광회선 대역폭이 폭증하던 CPRI(Option 8)와 사용자 실제 트래픽에 비례하여 대역폭을 90% 절감하는 eCPRI(Option 7-2x).

</details>

- 표준 인터페이스 기반 **멀티 벤더 상호운용성**
- Option 7-2x와 **eCPRI** 기반 프론트홀 효율화
- COTS 서버에 **vRAN·CNF** 기능을 유연하게 배포

#### 한줄 요약
- 멀티 벤더 상호운용성, eCPRI 기반 프론트홀 대역폭 절감, COTS 기반 가상화 배포를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CU vs DU vs RU**: 비실시간 제어를 담당하는 중앙 장치(CU), 실시간 1ms 스케줄링을 담당하는 분산 장치(DU), RF 송수신을 담당하는 무선 장치(RU).

</details>

```text
[5G 기지국 기능 분리]
  │
  ├─ [중앙 장치: CU]
  │    ├─ RRC / SDAP / PDCP 계층
  │    └─ F1 인터페이스 (Midhaul)
  │
  ├─ [분산 장치: DU]
  │    ├─ RLC / MAC / High-PHY
  │    └─ eCPRI 프론트홀 (7-2x)
  │
  └─ [무선 장치: RU]
       ├─ Low-PHY 디지털 빔포밍
       └─ RF 송수신 및 안테나 방사
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **CU** | **RRC·SDAP·PDCP** 처리 |
| **F1** | CU-DU 제어·사용자 평면 연결 |
| **DU** | **RLC·MAC·High-PHY** 처리 |
| **Open Fronthaul** | Option 7-2x 기반 DU-RU 연결 |
| **RU** | **Low-PHY·RF** 처리 |

#### 한줄 요약
- 분할 지점이 곧 실시간성 요구의 경계이므로, 지연에 민감한 기능일수록 안테나 가까이 남고 나머지는 중앙 CU로 모여 자원을 공유한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **O-RAN 4대 통신 평면**: DU와 RU 간 eCPRI 프론트홀을 구성하는 4대 제어 평면: C-Plane(제어), U-Plane(IQ 데이터), S-Plane(PTP 시간 동기), M-Plane(관리/구성).

</details>

```text
5G 기능 분리 기지국 패킷 수신, 변복조 및 무선 방사 파이프라인
        │
        [코어망 패킷 수신]
        │
   1. [PDCP 보호 및 F1 전달]
        │
   2. [MAC 스케줄링 및 High-PHY 처리]
        │
   3. [eCPRI 프론트홀 전송]
        │
   ▼
   4. [Low-PHY 빔포밍 및 RF 방사]
```

- 1. PDCP 보호 및 F1 전달
- 2. MAC 스케줄링 및 High-PHY 처리
- 3. eCPRI 프론트홀 전송
- 4. Low-PHY 빔포밍 및 RF 방사

#### 한줄 요약
- 기능 분할 지점 선택에서 프론트홀 대역폭과 중앙 집중 이득이 맞바뀌며, RU 쪽으로 밀수록 회선 비용이, CU 쪽으로 당길수록 자원 풀링 효과가 커진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Option 2 (CU-DU)** vs **Option 7-2x (O-RAN DU-RU)** vs **Option 8 (레거시 CPRI)**.

</details>

| 분할 표준 옵션 | Option 2 (3GPP F1 Split) | Option 7-2x (O-RAN Open Fronthaul) | Option 8 (레거시 CPRI Split) |
|:---|:---|:---|:---|
| 기능 분리 경계 | PDCP와 RLC 사이 | High-PHY와 Low-PHY 사이 | PHY와 RF 사이 |
| 적용 인터페이스 | **F1 미드홀** | **Open Fronthaul** | CPRI 프론트홀 |
| 전송 부하 | 사용자 데이터량에 비례 | 무선 설정과 IQ 데이터에 좌우 | 무선 대역폭·안테나 수에 비례 |
| 지연 요건 | 비교적 완만 | 엄격 | 엄격 |
| 주요 장점 | **CU 자원 풀링** | **멀티 벤더 DU-RU** | BBU 중앙화 |

#### 한줄 요약
- Option 2는 CU-DU 간 자원 풀링, Option 7-2x는 O-RAN 멀티 벤더 프론트홀 표준, Option 8은 레거시 CPRI 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PTP G.8275.1 Telecom Profile**: 프론트홀 이더넷 스위치 전 구간에 IEEE 1588v2 경계 클록(Boundary Clock)을 적용하여 시간 동기 오차를 $\pm 65\text{ns}$ 이하로 억제하는 통신 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| DU-RU 프로파일 차이로 **상호운용성 결함** | **O-RAN IOT**와 프로파일 검증 | 멀티 벤더 연동 위험 완화 |
| 프론트홀 지터로 **TDD 동기 오차** | **PTP G.8275.1·SyncE** 적용 | 셀 간 간섭 위험 완화 |
| Massive MIMO로 **광선로 비용 증가** | **Option 7-2x IQ 압축**과 WDM | 프론트홀 부하 절감 |
| vDU CPU 부하로 High-PHY 처리 지연 | **FPGA·eASIC·GPU 가속** | 실시간 처리 여유 확보 |

#### 한줄 요약
- O-RAN IOT 시험으로 상호운용성을 보장하고, PTP G.8275.1로 동기 오차를 방지하며, BFP 압축으로 대역폭을 절감한다.

## Ⅶ. 결론

- 폐쇄적인 통신사 장비 독점 구조를 타파하고 소프트웨어 중심의 클라우드 네이티브 기지국 시대를 여는 **5G Advanced 및 6G 개방형 무선망(O-RAN / vRAN)의 가장 핵심적인 기지국 아키텍처 표준 기술**로 정립되었으며, AI 기반 RIC(RAN Intelligent Controller) 및 클라우드 엣지 오케스트레이션과의 결합으로 진화하는 가운데, 실무 기능 분리 기지국 구축 시에는 **비실시간 제어 자원 풀링을 위한 Option 2(F1 미드홀)와 멀티벤더 DU-RU 개방을 지원하는 Option 7-2x(eCPRI 프론트홀)의 최적 조합 설계, TDD 프레임 간섭을 방지하는 IEEE 1588v2 PTP(Telecom Profile G.8275.1) 및 SyncE 기반 $\pm 65\text{ns}$ 정밀 시간 동기화, vDU의 High-PHY 계층 연산 병목을 제거하는 인라인(Inline) 하드웨어 가속기(FPGA/ASIC/GPU) 연동**을 결합하여 완벽한 개방형 무선망 성능을 완성

#### 한줄 요약
- 네트워크 기능 분리는 3GPP F1 및 O-RAN 7-2x 기반의 CU/DU/RU 분할과 정밀 동기화를 통해 개방형 고효율 기지국을 실현하는 핵심 기술이다.
