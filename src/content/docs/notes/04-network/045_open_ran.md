---
sidebar:
  order: 45
  label: "045. 오픈랜 (O-RAN, Open Radio Access Network)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "오픈랜 (O-RAN, Open Radio Access Network)"
date: "2026-08-13T17:08:00+09:00"
tags:
  - "notes-network"
weight: 45
extra:
  question_no: "045"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "설계•비교형: 132회 Open RAN 장문 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **개방형 무선 접속망(Open Radio Access Network, O-RAN / Open RAN)**: 기지국 소프트웨어와 하드웨어를 분리하고 인터페이스를 개방 표준화하여 다양한 제조사 장비를 조합하는 무선 접속망 아키텍처이다.
- **무선 접속망(Radio Access Network, RAN)**: 이동 통신 단말과 코어 네트워크 사이를 무선으로 연결해주는 기지국 및 인프라망이다.

</details>

- 정의/개념: **오픈랜(O-RAN, Open Radio Access Network)**은 5G/6G 무선 기지국(RAN)의 하드웨어와 소프트웨어를 분리(Disaggregation)하고, 기지국 구성요소(RU, DU, CU) 간 인터페이스를 개방형 표준(Open Interface)으로 규격화하여 멀티 벤더 장비 간 상호 운용성을 보장하는 무선망 기술이다.
- 배경/필요성: 특정 대형 통신장비 제조사(Vendor)의 종속성(Lock-in)을 해제하고, COTS 범용 서버 도입을 통한 구축/운용 비용(CAPEX/OPEX) 절감 및 지능형 무선 자원 제어기(RIC) 기반 자율망 구축을 위해 도입되었다.

#### 한줄 요약

- 기지국 장비를 RU, DU, CU로 분리하고 인터페이스를 개방하여 멀티 벤더 상호 운용성 및 지능형 제어(RIC)를 제공하는 개방형 무선망 아키텍처.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **개방형 분산 장치(Open Distributed Unit, O-DU)**: RLC, MAC, High-PHY 프로토콜을 처리하는 가상화 분산 기지국 소프트웨어 장치이다.
- **개방형 무선 장치(Open Radio Unit, O-RU)**: Low-PHY 및 무선주파수(RF) 송수신을 담당하는 하드웨어 전송 장치이다.
- **개방형 프론트홀(Open Fronthaul Interface)**: O-DU와 O-RU 간 제어, 사용자, 동기화(CUS-Plane) 데이터를 전달하는 eCPRI 기반 표준 인터페이스이다.
- **확장 응용(xApp)**: 준실시간 RIC(Near-RT RIC) 위에서 구동되며 10ms~1s 주기로 무선 자원을 최적화하는 미니 앱이다.
- **비실시간 응용(rApp)**: Non-RT RIC 위에서 구동되며 1초 이상의 주기로 AI/ML 모델 학습 및 장기 정책을 수립하는 미니 앱이다.
- **무선 접속망 지능형 제어기(RAN Intelligent Controller, RIC)**: 무선망 관제 및 자원 스케줄링을 AI/ML 알고리즘 기반으로 자율 통제하는 소프트웨어 플랫폼이다.
- **개방형 중앙 장치(Open Central Unit, O-CU)**: RRC 및 SDAP/PDCP 상위 계층과 이동성을 관장하는 논리 기지국 장치이다.
- **A1 인터페이스(A1 Interface)**: Non-RT RIC에서 수립한 AI 정책 및 가이드라인을 Near-RT RIC로 전달하는 인터페이스이다.
- **E2 인터페이스(E2 Interface)**: Near-RT RIC와 무선 노드(O-CU/O-DU) 간 트래픽 상태 보고 및 자원 제어 명령을 전달하는 표준 인터페이스이다.

</details>

- **기지국 기능 분리 및 구속 해제**: O-RU, O-DU, O-CU로 모듈화 분리하여 특정 벤더 종속을 해소하고 COTS 서버 기반 vRAN 구축이 가능하다.
- **개방형 인터페이스 상호 운용성**: Open Fronthaul, A1, E2, F1, E1 등 표준 규격을 정의하여 서로 다른 제조사 장비 간 직결 연동을 보장한다.
- **RIC 기반 AI/ML 지능화**: Near-RT RIC(xApp)와 Non-RT RIC(rApp)를 채택하여 무선 부하 분산, 핸드오버, 에너지 절감을 자동화한다.

#### 한줄 요약

- RU/DU/CU 멀티 벤더 조립, 개방형 표준 인터페이스(A1/E2/Fronthaul) 적용, RIC 기반 AI 자율망 제어 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **서비스 관리 및 오케스트레이션(Service Management and Orchestration, SMO)**: 전체 O-RAN 인프라의 수명주기, FOCOM/O-Cloud 관리 및 Non-RT RIC를 포함하는 통합 오케스트레이션 플랫폼이다.

</details>

```text
오픈랜 (O-RAN) 참조 아키텍처
├─ 오케스트레이션 계층 (SMO Platform & Non-RT RIC - rApp)
├─ 지능형 제어 계층 (Near-RT RIC - xApp)
└─ 분산 기지국 계층 (Open RAN Nodes)
   ├─ 개방형 중앙 장치 (O-CU - CP / UP)
   ├─ 개방형 분산 장치 (O-DU)
   └─ 개방형 무선 장치 (O-RU)
```

선의 의미: SMO/Non-RT RIC가 A1 인터페이스로 Near-RT RIC에 정책을 내리고, Near-RT RIC가 E2 인터페이스로 O-CU/O-DU를 제어하며, O-DU와 O-RU가 Open Fronthaul로 연결되는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| SMO 및 Non-RT RIC | O-RAN 인프라 오케스트레이션 및 rApp 기반 AI/ML 모델 학습, A1 정책 지침 생성 |
| 준실시간 RIC (Near-RT RIC) | 10ms~1s 주기 통제, xApp을 구동하여 E2 노드의 무선 자원(RRM), 빔포밍 및 핸드오버 실시간 제어 |
| O-CU (Open Central Unit) | RRC, PDCP 프로토콜 처리 및 제어 평면(O-CU-CP)과 사용자 평면(O-CU-UP) 분리 운용 |
| O-DU (Open Distributed Unit) | RLC, MAC, High-PHY 프로토콜을 COTS 가상화 서버 상에서 처리하고 준실시간 제어에 응답 |
| O-RU (Open Radio Unit) | Low-PHY 및 RF 무선 신호 송수신을 담당하며 Open Fronthaul을 통해 O-DU에 연결 |

#### 한줄 요약

- SMO/Non-RT RIC가 장기 정책을 수립하고 Near-RT RIC가 xApp으로 E2 노드(O-CU/O-DU)를 준실시간 통제하며 O-RU가 표준 프론트홀로 수송하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **A1 정책(A1 Policy)**: Non-RT RIC에서 결정된 모델 및 지침을 Near-RT RIC에 전달하는 정책 선언문이다.
- **E2 구독 요청(E2 Subscription Request)**: Near-RT RIC가 특정 무선 자원 상태 및 셀 부하 지표를 주기적으로 보고하도록 E2 노드에 등록하는 요청이다.
- **E2 무선 상태(E2 Indication)**: O-CU/O-DU가 현재의 셀 접속 단말 수, PRB 점유율, RSSI 등 무선 측정값을 RIC에 제공하는 피드백 메시지이다.
- **E2 제어 명령(E2 Control Command)**: xApp의 분석 결과에 따라 O-CU/O-DU의 RRM 설정이나 빔 회전 파라미터를 변경하도록 하향 발송하는 명령이다.

</details>

```text
1. Non-RT RIC -> Near-RT RIC: A1 인터페이스 기반 지능형 정책 전달 (A1 Policy)
      │
      v
2. Near-RT RIC -> O-CU/O-DU: E2 인터페이스 기반 무선 상태 구독 (E2 Subscription)
      │
      v
3. O-CU/O-DU -> Near-RT RIC: 무선 자원 측정 피드백 보고 (E2 Indication)
      │
      v
4. xApp: AI/ML 연산 후 E2 제어 명령 하향 발송 (E2 Control Command)
      │
      v
5. 무선 자원 스케줄링 변경 및 실시간 성과 모니터링 (Outcome Evaluation)
```

### 동작 원리

1. **A1 정책 전달**: SMO/Non-RT RIC가 rApp을 구동하여 학습된 정책 지침(A1 Policy)을 A1 인터페이스를 통해 Near-RT RIC로 전송한다.
2. **E2 무선 자원 구독**: Near-RT RIC가 E2 메시지를 발송하여 O-CU 및 O-DU의 주요 품질 지표(PRB, 지연시간)를 지속 수집하도록 등록한다.
3. **E2 무선 상태 측정 피드백**: E2 노드(O-CU/O-DU)가 무선 상태(E2 Indication)를 Real-time으로 Near-RT RIC의 xApp 엔진에 보고한다.
4. **xApp 제어 알고리즘 실행 및 명령 발송**: xApp이 수집된 상태를 AI 연산하여 최적의 부하 분산/핸드오버 제어 명령(E2 Control Command)을 하향 발송한다.
5. **스케줄링 반영 및 피드백 모니터링**: O-DU/O-CU가 수신된 제어 명령에 따라 자원 할당을 재구성하고 그 결과를 피드백 모니터링한다.

#### 한줄 요약

- Non-RT RIC의 A1 정책 수신, Near-RT RIC의 E2 구독 및 무선 상태 모니터링, xApp 제어 명령 하향 및 스케줄링 반영 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **폐쇄형 무선 접속망(Closed Radio Access Network, Closed RAN)**: 단일 벤더가 HW와 SW, 그리고 내부 인터페이스를 독점 제공하는 전통적 기지국 방식이다.

</details>

| 비교 항목 | **오픈랜 (O-RAN / Open RAN)** | **전통적 폐쇄형 기지국 (Closed RAN)** |
|:---|:---|:---|
| 인터페이스 개방성 | O-RU•O-DU•O-CU 표준 인터페이스 | 제조사 전용 비공개 인터페이스 |
| 벤더 구성 모델 | 멀티 벤더 장비 조합 가능 | 단일 벤더 통합 의존 |
| 자원 제어 방식 | AI/ML 기반 RIC (xApp / rApp) 지능형 자율 제어 | 기지국 내부 고정 알고리즘에 따른 벤더 전용 제어 |
| 구축/운용 비용 | COTS 범용 서버 활용으로 CAPEX/OPEX 장기 절감 | 전용 하드웨어 비용 및 벤더 종속(Lock-in) 비용 높음 |
| 통합 및 유지보수 | 멀티 벤더 상호 운용성 검증(IOT) 및 책임 조정 복잡 | 단일 벤더 일괄 통합 수용으로 유지보수 및 장애 처리 용이 |

> 요약: 전통적 Closed RAN 대비 O-RAN은 벤더 종속을 해제하고 RIC 기반 지능형 자율망을 구축할 수 있으나 멀티 벤더 연동 통합 검증 필요.

#### 한줄 요약

- 전통적 폐쇄형 RAN 대비 O-RAN은 벤더 종속을 해제하고 RIC 기반 지능형 자율망을 구축할 수 있으나 멀티 벤더 연동 통합 검증 필요.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **상호운용성 시험(Interoperability Testing, IOT)**: 이종 O-RU•O-DU•O-CU의 규격 호환성을 검증하는 시험이다.
- **동기 예산(Synchronization Budget)**: O-DU와 O-RU 간 Open Fronthaul 전송 시 허용되는 최대 시간 오차(Time Error, ns 단위) 한도 수치이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 멀티 벤더 상호 호환 실패 | 벤더별 O-RAN 표준 해석 오차 및 비표준 필드 사용 | 오픈랜 시험인증 센터(OTIC) 통한 IOT 연동 검증 | 이종 벤더 간 호환성 확보 및 장애 최소화 |
| 프론트홀 동기 오손 | Open Fronthaul 패킷 지연 및 시간 동기 오차 | IEEE 1588v2 PTP 및 SyncE 적용 (Time Sync) | O-RU 무선 신호 변복조 오류 및 감쇄 방지 |
| xApp 제어 정책 충돌 | 서로 다른 xApp이 동일 무선 자원(PRB)을 상충 변경 | Near-RT RIC 내 Conflict Manager 모듈 탑재 | 자원 제어 충돌 예방 및 안정적 무선 품질 유지 |
| 멀티 벤더 책임 소재 모호 | 장애 발생 시 SW/HW 벤더 간 원인 전가 분쟁 | SMO 기반 통합 텔레메트리 모니터링 및 E2E SLAs 체결 | 빠른 Root Cause 분석 및 결함 복구 대응 |

#### 한줄 요약

- IOT 통합 검증 자동화, 1588v2/PTP 정밀 시간 동기화, Near-RT RIC 내 Conflict Manager 도입으로 O-RAN 시스템 운용성 확보.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **상호운용 비용(Interoperability & Integration Cost)**: 멀티 벤더 장비를 조합 및 통합 구축하고 연동 시험 및 책임 조정을 수행하는 데 투입되는 비용 수치이다.

</details>

- 벤더 유연성이 우선이면 **O-RAN**, 단일 책임은 **폐쇄형 RAN** 선택

#### 한줄 요약

- 멀티 벤더 IOT 검증 체계 확립 및 RIC 기반 지능형 자율망 구축 필수.
