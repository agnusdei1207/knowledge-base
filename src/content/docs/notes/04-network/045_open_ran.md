---
sidebar:
  order: 45
  label: "045. 오픈랜: O-RAN"
  badge:
    text: "기출 · 50%"
    variant: note
title: "개방형 무선 접속망 : 오픈랜 (O-RAN)"
date: "2026-08-26T13:52:17+09:00"
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
- 배경/필요성: 폐쇄 인터페이스로 **이종 장비 결합과 기능 교체 제약**이 생겨 한 기능만 바꾸려 해도 기지국 일괄 교체 비용을 치러야 하므로, 기지국을 O-RU·O-DU·O-CU로 쪼개고 그 경계를 개방 규격으로 못 박아 교체 단위를 구성요소로 낮출 필요

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
[O-RAN]
|-- SMO·Non-RT RIC
|-- Near-RT RIC
`-- RAN 노드
    |-- O-CU
    |-- O-DU
    `-- O-RU
```

선의 의미: 계층 및 SMO에서 A1으로 정책을 하달하고 Near-RT RIC이 E2로 O-CU/DU를 제어하며 7-2x 프론트홀로 O-RU에 연결되는 구조

| 구성요소 | 책임 |
|:---|:---|
| **SMO·Non-RT RIC** | 오케스트레이션과 장기 정책 관리 |
| **Near-RT RIC** | xApp 기반 준실시간 RAN 제어 |
| **O-CU** | RRC·SDAP·PDCP 처리 |
| **O-DU** | RLC·MAC·High-PHY 처리 |
| **O-RU** | Low-PHY·RF와 안테나 처리 |

#### 한줄 요약
- Near-RT RIC이 기지국 안에 박혀 있던 무선 제어 판단을 xApp으로 끄집어내고 A1·E2·7-2x 개방 인터페이스가 벤더 내부 결선을 대신하므로, 장비를 통째로 교체하지 않고 제어 로직만 갈아 끼울 수 있다.

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

- 1. 장기 정책 수립: rApp의 정책 생성
- 2. A1 정책 하달: Near-RT RIC에 정책 전달
- 3. E2 텔레메트리 수집: RAN 노드 지표 수집
- 4. 준실시간 제어 연산: xApp의 제어 명령 산출
- 5. 7-2x 프론트홀 송출: O-DU와 O-RU 사이 전송

#### 한줄 요약
- Non-RT RIC은 학습에 시간을 들이는 장기 정책을, Near-RT RIC은 밀리초 단위 즉시 제어를 맡아 갈리므로, 학습에 필요한 시간과 무선이 요구하는 즉시성을 서로 다른 계층이 나눠 감당한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **O-RAN (오픈랜)** vs **Closed RAN (전통적 폐쇄형 기지국)**: 다중 벤더 COTS 가상화(O-RAN)와 단일 제조사 독점 ASIC(Closed).

</details>

| 비교 항목 | 오픈랜 (O-RAN) | 전통적 폐쇄형 기지국 (Closed RAN) |
|:---|:---|:---|
| 하드웨어 | 범용 서버·가속기 조합 가능 | 벤더 전용 장비 중심 |
| 인터페이스 | **7-2x·A1·E2** 개방 규격 | 벤더별 인터페이스 가능 |
| 벤더 구성 | 상호운용 검증 후 다중 벤더 조합 | 단일 벤더 통합 중심 |
| 제어 방식 | xApp·rApp 기반 정책 확장 | 벤더 기능 기반 제어 |
| 통합 부담 | 다중 벤더 시험·책임 조정 | 벤더 통합 책임 집중 |

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

- 다중 벤더 유연성이 중요하면 **O-RAN**, 통합 책임도 함께 확보

#### 한줄 요약
- 오픈랜(O-RAN)은 개방형 프론트홀과 RIC 지능형 제어를 통해 벤더 종속을 탈피하고 무선망 소프트웨어화를 실현하는 핵심 차세대 기지국 표준이다.
