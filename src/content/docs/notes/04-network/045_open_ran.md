---
sidebar:
  order: 45
  label: "045. 오픈랜: O-RAN (Open Radio Access Network)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "개방형 무선 접속망 : 오픈랜 (O-RAN, Open Radio Access Network)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 45
extra:
  question_no: "045"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "O-RAN Alliance 표준 아키텍처, RIC(RAN 지능형 제어기), 개방형 프론트홀 eCPRI"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **오픈랜(Open Radio Access Network, O-RAN)**: 기지국의 하드웨어와 소프트웨어를 분리(Disaggregation)하고, 기지국 구성요소(RU, DU, CU) 간의 인터페이스를 개방형 표준(Open Interface)으로 규격화하여 멀티 벤더 상호 운용을 가능하게 하는 차세대 무선 접속망 아키텍처.
- **벤더 종속(Vendor Lock-in)**: 특정 제조사의 독점적 비공개 인터페이스로 인해 전체 기지국 장비를 단일 제조사 제품으로만 일괄 구매·운용해야 하는 폐쇄적 구조.

</details>

- 정의/개념: 기지국 구성요소를 **O-RU, O-DU, O-CU** 로 기능 분할하고, 표준화된 **개방형 프론트홀(Open Fronthaul)** 과 **RAN 지능형 제어기(RIC)** 를 통해 범용 하드웨어(COTS) 및 다중 제조사 소프트웨어의 결합을 지원하는 **개방형 기지국 표준(O-RAN Alliance)**
- 배경/필요성: 기존 통신 장비 제조사의 독점적 하드웨어 종속으로 인한 높은 망 구축 비용(CAPEX/OPEX)을 절감하고, AI 기반 기지국 자율 최적화(AIOps) 및 신속한 5G/6G 기능 배포를 달성할 요구

#### 한줄 요약
- 기지국 HW/SW를 분리하고 인터페이스를 개방하여 다중 벤더 상호 운용과 AI 자율 제어를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **가상화 무선 접속망(vRAN, Virtualized RAN)**: 전용 ASIC 하드웨어 대신 범용 x86/ARM 서버(COTS)의 가상 머신이나 컨테이너 위에서 기지국 기저대역(L1/L2/L3) 기능을 소프트웨어로 구동하는 기술.
- **RAN 지능형 제어기(RAN Intelligent Controller, RIC)**: 무선 접속망 내의 자원 할당, 간섭 제어, 이동성 관리를 AI/ML 마이크로서비스 앱(xApp/rApp) 형태로 실행하여 실시간 자율 최적화하는 소프트웨어 플랫폼.

</details>

- **하드웨어와 소프트웨어의 완전 분리**: 고가의 독점 하드웨어 어플라이언스를 범용 COTS 서버 기반 vRAN 소프트웨어로 대체
- **개방형 프론트홀(Open Fronthaul)**: O-RU와 O-DU 간 O-RAN 7-2x Split 기반 eCPRI 개방형 인터페이스 표준화를 통한 이종 벤더 간 상호 연동
- **AI 기반 지능형 무선 제어(RIC)**: 비실시간(Non-RT RIC) 및 준실시간(Near-RT RIC) 계층을 통해 빔포밍 및 트래픽 스케줄링의 프로그래머블 자율 최적화

#### 한줄 요약
- vRAN 소프트웨어화, 7-2x 개방형 프론트홀, RIC 지능형 제어를 통해 유연성과 확장성을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **서비스 관리 및 오케스트레이션(Service Management and Orchestration, SMO)**: 전체 O-RAN 인프라의 배포, 구성 관리, 성능 모니터링 및 Non-RT RIC을 탑재한 중앙 관리 프레임워크.
- **xApp / rApp**: Near-RT RIC 위에서 준실시간(10ms~1s) 제어를 수행하는 마이크로서비스 앱(xApp)과 SMO/Non-RT RIC 위에서 비실시간(>1s) 장기 정책을 학습·적용하는 앱(rApp).

</details>

```text
[ SMO (Service Management & Orchestration) / Non-RT RIC ]
   │ (rApp 구동: AI 모델 학습 및 장기 무선 정책 수립)
   │
   ▼ (A1 인터페이스: 정책 가이드라인 하달)
[ Near-RT RIC (RAN 지능형 제어기) ]
   │ (xApp 구동: 10ms~1s 단위 초고속 무선 자원/간섭 제어)
   │
   ▼ (E2 인터페이스: 실시간 원격 측정 및 제어 명령 주입)
┌────────────────────────────────────────────────────────────┐
│ O-CU (Open Centralized Unit / L2-L3 RRC, SDAP, PDCP 계층)  │
├────────────────────────────────────────────────────────────┤
│ O-DU (Open Distributed Unit / L1-High, L2 RLC, MAC 계층)   │
└─────────────────────────────┬──────────────────────────────┘
                              │ (Open Fronthaul 7-2x Split / eCPRI)
                              ▼
[ O-RU (Open Radio Unit / RF 안테나 및 L1-Low 물리 계층) ] ──▶ (단말)
```

선의 의미: SMO에서 A1을 통해 RIC으로 정책을 하달하고, Near-RT RIC이 E2 인터페이스로 O-CU/O-DU를 제어하며, 개방형 프론트홀을 통해 O-RU로 신호를 전송하는 계층 구조

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| **SMO / Non-RT RIC** | RAN 슬라이스 생애주기 관리, O-Cloud 오케스트레이션 및 rApp 기반 AI 정책 학습 | 비실시간 (>1s) |
| **Near-RT RIC** | E2 노드(CU/DU)의 성능 지표를 수집하고 xApp을 구동하여 빔포밍·핸드오버 제어 | 준실시간 (10ms~1s) |
| **O-CU (Centralized Unit)** | RRC, SDAP, PDCP 프로토콜을 수행하는 상위 제어 및 데이터 집중 처리 노드 | vCU (L2/L3) |
| **O-DU (Distributed Unit)** | RLC, MAC, High-PHY(FFT/IFFT)를 수행하며 실시간 스케줄링을 전담하는 노드 | vDU (L1/L2) |
| **O-RU (Radio Unit)** | RF 디지털 변환, 빔포밍 및 Low-PHY 계층을 수행하는 개방형 안테나 유닛 | 7-2x Split RU |

#### 한줄 요약
- SMO, Near-RT RIC, O-CU, O-DU, O-RU가 표준 개방형 인터페이스(A1, E2, eCPRI)로 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **E2 인터페이스**: Near-RT RIC과 하위 무선 노드(O-CU/O-DU) 간에 실시간 무선 측정 지표를 보고하고 xApp의 제어 액션을 실행하는 O-RAN 표준 프로토콜.

</details>

```text
1. SMO(Non-RT RIC)의 rApp이 장기 트래픽 통계를 학습하여 무선 정책 수립
            │
            ▼
2. A1 인터페이스를 통해 Near-RT RIC으로 AI 정책(QoS 가이드라인) 하달
            │
            ▼
3. Near-RT RIC의 xApp이 E2 인터페이스로 O-CU/O-DU의 실시간 채널 상태 수집
            │
            ▼
4. xApp이 실시간 제어 알고리즘(핸드오버/간섭 제어) 연산 후 E2 명령 하달
            │
            ▼
5. O-DU가 개방형 프론트홀(7-2x)을 통해 O-RU에 전송 심볼 주입 및 단말 송출
```

**동작 원리**

1. **AI 정책 도출**: Non-RT RIC이 네트워크 전체의 장기 SLA 및 슬라이스 정책을 A1 인터페이스로 주입
2. **무선 텔레메트리 수집**: Near-RT RIC이 E2 인터페이스를 통해 O-DU의 무선 자원 블록(PRB) 사용률 및 CSI 수신
3. **준실시간 제어 연산**: xApp이 밀리초 단위로 단말 간섭 완화 및 최적 빔포밍 각도 산출
4. **개방형 프론트홀 전송**: O-DU가 L1-High 처리를 거쳐 eCPRI 규격으로 O-RU에 IQ 데이터를 송출하여 단말 통신 최적화

#### 한줄 요약
- rApp 정책 학습, A1 하달, E2 텔레메트리 수집, xApp 제어 연산, 7-2x 프론트홀 전송 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **폐쇄형 전통 기지국(Traditional Closed RAN)**: 기지국 하드웨어(BBU/RRU)와 펌웨어가 단일 벤더의 독점 규격으로 결합되어 타사 제품과의 연동이 불가능한 구조.

</details>

| 비교 항목 | 오픈랜 (O-RAN) | 전통적 폐쇄형 기지국 (Closed RAN) |
|:---|:---|:---|
| **하드웨어 아키텍처** | 범용 서버(COTS x86/ARM) 및 **가상화(vRAN)** | 전용 독점 ASIC 하드웨어 (BBU) |
| **인터페이스 개방성** | **개방형 프론트홀(7-2x), A1, E2 표준화** | 제조사 독점 비공개 인터페이스 (CPRI) |
| **제조사 종속성** | **다중 벤더(Multi-Vendor) 조합 가능** | **단일 벤더(Single-Vendor) 종속 (Lock-in)** |
| **망 제어 및 최적화** | **RIC 기반 개방형 앱(xApp/rApp) 자율 제어** | 장비 제조사의 고정 펌웨어 알고리즘 |
| **시스템 통합(SI) 부담** | **다중 벤더 간 상호운용성(IOT) 검증 필요** | 제조사가 단일 책임 보증 (SI 부담 낮음) |

#### 한줄 요약
- 오픈랜은 COTS 가상화, 표준 인터페이스, 다중 벤더 조합, RIC AI 제어를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **상호운용성 시험(Interoperability Testing, IOT)**: 서로 다른 제조사의 O-RU, O-DU, O-CU를 결합했을 때 프로토콜 및 성능 정합성을 사전에 검증하는 표준 인증 프로세스.
- **충돌 관리자(Conflict Manager)**: 동일한 기지국 자원에 대해 복수의 xApp이 상충하는 제어 명령을 내릴 때 우선순위를 중재하는 RIC 내부 모듈.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 벤더 장비(A사 O-RU + B사 O-DU) 간 표준 해석 차이로 인한 통신 실패 | **공인 오픈랜 시험 센터(OTIC)** 기반 사전 **상호운용성(IOT) 인증** 의무화 | 멀티 벤더 간 프로토콜 불일치 해소 및 상용 신뢰성 확보 |
| 장애 발생 시 하드웨어·소프트웨어·RU 제조사 간 책임 공방 및 복구 지연 | **SMO 중앙 집중형 E2E 로깅 체계** 구축 및 **주계약 시스템 통합(SI)사** 지정 | 장애 원인 구간의 신속한 특정 및 단일 책임 복구 거버넌스 확립 |
| 복수의 xApp(예: 절전 제어 vs 성능 증대) 간 상충된 E2 제어 명령 발생 | Near-RT RIC 내 **충돌 관리자(Conflict Manager)** 의 우선순위 중재 | 제어 루프 충돌 방지 및 기지국 파라미터 발진(Oscillation) 차단 |

#### 한줄 요약
- OTIC IOT 인증으로 호환성을 보증하고, E2E 로깅/통합 SI로 책임을 명확화하며, Conflict Manager로 xApp 충돌을 방지한다.

## Ⅶ. 결론

- 특정 장비 제조사의 단일 벤더 종속을 탈피하고 CAPEX/OPEX 절감과 통신망 유연성을 확보하기 위해 **O-RAN 표준 아키텍처**를 단계적으로 도입하되, 다중 벤더 통합에 따른 운영 복잡도를 통제하기 위해 **OTIC 상호운용성 인증**과 **RIC 충돌 관리 메커니즘**을 필수 구축하여 안정적인 개방형 5G/6G 무선망을 완성

#### 한줄 요약
- 개방형 프론트홀과 RIC 지능형 제어를 결합하여 벤더 종속 없는 고효율 무선 접속망을 구현한다.
