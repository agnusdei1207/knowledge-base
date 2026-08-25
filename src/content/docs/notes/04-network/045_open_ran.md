---
sidebar:
  order: 45
  label: "045. 오픈랜: O-RAN"
  badge:
    text: "기출 · 50%"
    variant: note
title: "개방형 무선 접속망 : 오픈랜 (O-RAN)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 45
extra:
  question_no: "45"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "O-RAN Alliance 표준 아키텍처, RIC(RAN 지능형 제어기), 개방형 프론트홀 eCPRI"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **O-RAN (Open Radio Access Network)**: 기지국의 HW/SW를 분리하고 RU, DU, CU 간 인터페이스를 개방형 표준으로 정의하여 다중 벤더 상호 운용을 실현하는 무선망.
- **Vendor Lock-in (벤더 종속)**: 제조사의 독점적 비공개 인터페이스로 인해 전체 기지국 장비를 단일 제조사 제품으로만 일괄 구축해야 하는 폐쇄적 구조.

</details>

- 정의/개념: 기지국을 **O-RU, O-DU, O-CU로 기능 분할하고 개방형 프론트홀(7-2x)과 지능형 제어기(RIC)를 통해 멀티 벤더 결합을 실현하는 개방형 무선망 표준**
- 배경/필요성: 기존 제조사의 독점적 하드웨어 종속(Vendor Lock-in)으로 인한 **막대한 CAPEX/OPEX 비용 발생, 신규 서비스 도입 지연 및 이종 제조사 장비 혼용 불가**

#### 한줄 요약
- 개방형 인터페이스, COTS 가상화, RIC AI 제어를 통해 벤더 종속을 탈피하고 무선망을 소프트웨어화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Open Fronthaul (Option 7-2x Split)**: O-DU(High-PHY/MAC)와 O-RU(Low-PHY/RF) 간의 전송 인터페이스를 eCPRI 표준으로 개방한 규격.
- **RIC (RAN Intelligent Controller)**: 비실시간(Non-RT) 및 준실시간(Near-RT) 계층에서 AI/ML 알고리즘(xApp/rApp)으로 기지국 자원을 프로그래머블 제어하는 두뇌.

</details>

- 범용 x86/ARM COTS 서버 위에서 컨테이너 기반으로 기지국 SW를 구동하는 **vRAN 가상화**
- O-DU와 O-RU 간의 제조사 독점 규격을 파괴한 **Option 7-2x 개방형 프론트홀(eCPRI)**
- xApp과 rApp 기반의 **AI 내재화 무선 지능형 제어기(RIC)를 통한 자율 최적화**

#### 한줄 요약
- vRAN 가상화, 7-2x 개방형 프론트홀, RIC 지능형 제어를 통해 유연성과 확장성을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SMO (Service Management & Orchestration)**: 전체 O-Cloud 인프라 오케스트레이션과 Non-RT RIC(rApp)을 탑재한 중앙 관리 플랫폼.
- **xApp vs rApp**: Near-RT RIC 위에서 10ms~1s 단위 준실시간 제어를 수행하는 xApp과 SMO 위에서 장기 정책(>1s)을 학습하는 rApp.

</details>

```text
[O-RAN Alliance 표준 계층 및 개방형 인터페이스 아키텍처]
|-- SMO Platform (Service Management & Orchestration)
|   `-- Non-RT RIC (rApp: AI 모델 학습 및 장기 무선 정책 수립, >1s)
|-- A1 Interface (정책 가이드라인 하달)
`-- Near-RT RIC (xApp: 10ms~1s 단위 초고속 무선 자원/간섭/빔포밍 제어)
|-- E2 Interface (실시간 원격 텔레메트리 수집 및 제어 명령 주입)
`-- Disaggregated RAN Nodes
    |-- O-CU (Open Centralized Unit: L3 RRC, L2 SDAP/PDCP 상위 계층)
    |-- O-DU (Open Distributed Unit: L2 RLC/MAC, L1-High FFT/IFFT 계층)
    `-- O-RU (Open Radio Unit: Option 7-2x eCPRI 개방형 프론트홀 -> Low-PHY / RF 안테나)
```

선의 의미: 계층 및 SMO에서 A1으로 정책을 하달하고 Near-RT RIC이 E2로 O-CU/DU를 제어하며 7-2x 프론트홀로 O-RU에 연결되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SMO / Non-RT RIC** | RAN 슬라이스 수명주기 관리, O-Cloud 오케스트레이션 및 **rApp 기반 장기 AI 정책 학습** | 비실시간 (>1s) |
| **Near-RT RIC** | E2 노드(CU/DU)의 지표를 수집하고 **xApp을 구동하여 10ms~1s 단위 빔포밍·핸드오버 제어** | 준실시간 (10ms~1s) |
| **O-CU (Centralized)** | RRC, SDAP, PDCP 프로토콜을 수행하는 **상위 제어 및 데이터 집중 가상화 노드 (vCU)** | L2/L3 계층 |
| **O-DU (Distributed)** | RLC, MAC, High-PHY를 수행하며 **실시간 스케줄링을 전담하는 분산 가상화 노드 (vDU)** | L1/L2 계층 |
| **O-RU (Radio Unit)** | RF 디지털 변환, 빔포밍 및 Low-PHY 계층을 수행하는 **개방형 프론트홀 안테나 유닛** | 7-2x Split RU |

#### 한줄 요약
- SMO, Near-RT RIC, O-CU, O-DU, O-RU가 표준 개방형 인터페이스(A1, E2, eCPRI)로 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **E2 Protocol**: Near-RT RIC과 하위 무선 노드(O-CU/O-DU) 간에 실시간 성능 지표를 수집하고 xApp의 제어 액션을 실행하는 표준 인터페이스.

</details>

```text
O-RAN 지능형 무선 제어 및 프론트홀 전송 파이프라인
        │
   1. [장기 정책 수립] Non-RT RIC(rApp)이 트래픽 패턴을 학습하여 SLA 정책 수립
        │
   2. [A1 정책 하달] A1 인터페이스를 통해 Near-RT RIC으로 AI 최적화 가이드라인 주입
        │
   3. [E2 텔레메트리 수집] Near-RT RIC(xApp)이 E2로 O-CU/O-DU의 PRB 사용률 및 CSI 수집
        │
   4. [준실시간 제어 연산] xApp이 밀리초 단위로 간섭 완화 및 빔포밍 각도 연산 후 E2 명령 하달
        │
   ▼
5. [7-2x 프론트홀 송출] O-DU가 High-PHY 처리 후 eCPRI로 O-RU에 IQ 심볼 주입 및 단말 송출
```

#### 한줄 요약
- rApp 정책 학습 → A1 하달 → E2 텔레메트리 수집 → xApp 제어 연산 → 7-2x 프론트홀 전송 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **O-RAN (오픈랜)** vs **Closed RAN (전통적 폐쇄형 기지국)**: 다중 벤더 COTS 가상화(O-RAN)와 단일 제조사 독점 ASIC(Closed).

</details>

| 비교 항목 | 오픈랜 (O-RAN) | 전통적 폐쇄형 기지국 (Closed RAN) |
|:---|:---|:---|
| **하드웨어 아키텍처** | **범용 서버(COTS x86/ARM) 및 클라우드 가상화(vRAN)** | 전용 독점 ASIC 하드웨어 (BBU) |
| **인터페이스 개방성** | **개방형 프론트홀(7-2x), A1, E2 완전 표준화** | 제조사 독점 비공개 인터페이스 (CPRI) |
| **제조사 종속성** | **다중 벤더(Multi-Vendor) 자유 조합 가능** | **단일 벤더(Single-Vendor) 완전 종속 (Lock-in)**|
| **망 제어 및 최적화** | **RIC 기반 개방형 앱(xApp/rApp) 프로그래머블 제어**| 제조사의 고정 폐쇄 펌웨어 알고리즘 |
| **시스템 통합(SI) 부담**| **다중 벤더 간 상호운용성(IOT) 검증 필요** | 제조사가 단일 책임 보증 (SI 부담 낮음) |

#### 한줄 요약
- 오픈랜은 COTS 가상화, 표준 인터페이스, 다중 벤더 조합, RIC AI 제어를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OTIC (Open Testing & Integration Centre)**: 서로 다른 제조사의 O-RU, O-DU, O-CU 간의 프로토콜 정합성과 성능을 검증하는 국제 공인 인증 시험소.
- **Conflict Manager**: 복수의 xApp이 동일한 기지국 자원에 대해 상충된 제어 명령을 내릴 때 우선순위를 중재하는 RIC 모듈.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 벤더 장비(A사 RU + B사 DU) 간 표준 해석 차이로 인한 통신 실패 | **공인 오픈랜 시험 센터(`OTIC`) 기반 사전 상호운용성(IOT) 인증** | 멀티 벤더 간 프로토콜 불일치 해소 및 신뢰성 확보 |
| 장애 발생 시 HW/SW/RU 제조사 간 책임 공방 및 복구 지연 | **SMO 중앙 집중형 E2E 로깅 및 `주계약 시스템 통합(SI)사` 지정** | 장애 원인 구간의 신속한 특정 및 단일 복구 책임제 |
| 복수의 xApp 간 상충된 E2 제어 명령 발생 시 기지국 파라미터 발진 | Near-RT RIC 내 **`충돌 관리자(Conflict Manager)`의 우선순위 중재** | 제어 루프 충돌 방지 및 기지국 안정성 유지 |
| 범용 COTS 서버의 High-PHY 연산 시 CPU 과부하 및 지연 증가 | **`인라인 가속기(Inline Hardware Accelerator PCIe 카드)` 장착** | FFT/LDPC 연산 오프로딩 및 저지연 L1 처리 |

#### 한줄 요약
- OTIC IOT 인증, SMO 로깅/통합 SI, Conflict Manager 중재, 인라인 가속기 장착으로 운영한다.

## Ⅶ. 결론

- 특정 장비 제조사의 벤더 종속(Lock-in)을 탈피하고 CAPEX/OPEX 절감과 통신망 유연성을 확보하기 위해 **O-RAN 표준 아키텍처를 전사 표준으로 채택**하고, 다중 벤더 통합에 따른 운영 복잡도를 통제하기 위해 **OTIC 상호운용성 인증과 RIC 충돌 관리 메커니즘 및 인라인 하드웨어 가속기**를 결합하여 안정적인 개방형 5G/6G 무선망 완성

#### 한줄 요약
- 오픈랜(O-RAN)은 개방형 프론트홀과 RIC 지능형 제어를 통해 벤더 종속을 탈피하고 무선망 소프트웨어화를 실현하는 핵심 차세대 기지국 표준이다.