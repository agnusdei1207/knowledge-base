---
sidebar:
  order: 65
  label: "065. JTAG 디버깅 인터페이스 (JTAG)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "JTAG 디버깅 인터페이스 (JTAG)"
date: "2026-08-08T17:56:00+09:00"
tags:
  - "notes-hardware"
weight: 65
extra:
  question_no: "065"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "양산 연결 검사•출하 후 포트 통제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **공동 시험 동작 그룹 인터페이스(Joint Test Action Group, JTAG)**: IEEE 1149.1 TAP과 경계 스캔 레지스터를 통해 IC 핀·PCB 연결을 직렬 시험하는 인터페이스이다.
- **전기전자공학자협회(Institute of Electrical and Electronics Engineers, IEEE)**: 전기전자 기술 표준 단체이다.
- **테스트 접근 포트(Test Access Port, TAP)**: 시험 명령과 데이터를 직렬로 전송하고 상태 머신을 제어하는 JTAG 포트이다.
- **집적회로(Integrated Circuit, IC)**: 회로를 반도체 다이에 집적한 장치이다.
- **인쇄회로기판(Printed Circuit Board, PCB)**: 전자 부품을 배선으로 연결하는 기판이다.
- **경계 스캔(Boundary Scan)**: IC 핀 주위 셀을 직렬 체인으로 연결하는 시험 방식이다.

</details>

- 정의/개념: IEEE 1149.1 TAP 상태 머신과 직렬 경계 스캔 레지스터로 IC 핀과 PCB 연결을 구동·관측하는 **JTAG** 인터페이스이다.
- 배경/필요성: 고밀도 패키지·기판에서는 물리 탐침으로 내부 핀과 미세 배선에 접근하기 어려워 비접촉 연결 시험이 필요하다.

#### 한줄 요약

- JTAG는 IC 핀 주변의 경계 스캔 셀을 직렬 연결해 PCB 배선을 외부 탐침 없이 구동·관측한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **직렬 스캔 체인(Serial Scan Chain)**: 여러 집적회로(Integrated Circuit, IC)의 시험 레지스터를 테스트 데이터 입력(Test Data In, TDI)과 테스트 데이터 출력(Test Data Out, TDO)으로 한 줄에 연결하여 순차 접근하는 구조이다.
- **경계 스캔 셀(Boundary-scan Cell)**: 코어 실행과 독립적으로 IC 핀의 입력을 캡처하거나 출력을 구동하는 시험 셀이다.
- **중앙처리장치 디버그(Central Processing Unit Debug, CPU Debug)**: 프로세서 구현이 별도로 제공하는 코어 정지와 레지스터•메모리 접근 기능이다.

</details>

- 다중 IC의 단일 포트 검사는 **직렬 스캔 체인** 활용이 핵심이다.
- 코어 실행 없는 핀 구동•관찰에는 **경계 스캔 셀** 활용이 핵심이다.
- IEEE 1149.1 경계 스캔은 PCB 연결 시험을 표준화하고, 코어 정지·레지스터 접근은 프로세서별 **CPU 디버그** 구현을 별도로 확인한다.

#### 한줄 요약

- 여러 IC의 시험 레지스터를 TDI·TDO 직렬 체인으로 연결하면 하나의 TAP 경로에서 각 장치의 핀 연결을 검사할 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **테스트 접근 포트 제어기(Test Access Port Controller, TAP 제어기)**: 테스트 모드 선택(Test Mode Select, TMS) 입력과 테스트 클록(Test Clock, TCK)에 따라 명령•데이터 캡처, 이동 및 적용 상태를 전환하는 상태 머신이다.
- **명령 레지스터(Instruction Register, IR)**: 현재 실행할 JTAG 시험 명령을 직렬로 받아 저장하는 레지스터이다.
- **데이터 레지스터(Data Register, DR)**: 경계 스캔과 식별 코드(Identification Code, IDCODE) 및 우회(BYPASS) 같은 시험 데이터를 직렬 이동하는 레지스터이다.
- **테스트 데이터 입력•출력(Test Data In•Test Data Out, TDI•TDO)**: 선택된 JTAG 레지스터에 시험 비트를 직렬 입력하고 관측 비트를 직렬 출력하는 신호이다.

</details>

TAP 제어기는 TMS와 TCK에 따라 IR과 DR을 전환한다. TDI와 TDO는 JTAG 데이터를 직렬 이동한다.

```text
                 [명령 레지스터]
                        |
                        |
                 [TAP 제어기] -- [데이터 레지스터] -- [경계 스캔 셀]
```

선의 의미: TAP 제어기가 명령 레지스터와 데이터 레지스터를 선택하고, 데이터 레지스터가 경계 스캔 셀 체인에 결합된 정적 JTAG 구조다.

| 구성요소 | 책임 |
|:---|:---|
| TAP 제어기 | IR•DR 상태 전이 |
| 명령 레지스터 | 시험 명령 선택 |
| 데이터 레지스터 | 시험 데이터 이동 |
| 경계 스캔 셀 | 핀 캡처•구동 |

#### 한줄 요약

- TAP 제어기는 TMS·TCK로 IR 또는 DR의 캡처·이동·갱신 상태를 선택하고 경계 셀이 핀 값을 관측·구동하게 한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **외부 시험(External Test, EXTEST)**: 경계 스캔 셀을 구동하고 관측하여 인쇄회로기판(Printed Circuit Board, PCB)의 집적회로(Integrated Circuit, IC) 사이 외부 연결을 검사하는 공동 시험 동작 그룹(Joint Test Action Group, JTAG) 명령이다.
- **시험 패턴(Test Pattern)**: 특정 핀 연결의 단선과 단락을 검출하도록 경계 셀에 적재하는 구동 비트열이다.
- **캡처 비트열(Captured Bitstream)**: 시험 패턴 전송 후 수신 측 경계 셀이 관찰하여 저장한 입력 값의 직렬 데이터이다.
- **EXTEST 선택**: 명령 레지스터에 외부 연결 시험 명령을 적재하는 단계이다.
- **경계 체인 선택**: 데이터 레지스터 경로를 경계 스캔 셀 체인에 연결하는 단계이다.
- **시험 패턴 이동**: TDI로 핀 구동 비트열을 경계 체인에 넣는 단계이다.
- **시험 패턴 구동**: 출력 경계 셀이 패턴을 PCB 연결망에 적용하는 단계이다.
- **입력 캡처·직렬 출력**: 수신 값을 저장해 TDO로 내보내 예상 패턴과 비교하는 단계이다.

</details>

JTAG 프로브는 TMS와 TCK로 EXTEST를 지정하고 PCB의 IC 연결을 검사한다.

```text
 시험 소프트웨어•프로브       TAP•스캔 레지스터       경계 셀•PCB 연결
          │                           │                       │
          ├── TMS•TCK ───────────────►│                       │
          │                           │                       │
          ├── 1. EXTEST 선택 ────────►│                       │
          │                           ├── 2. 경계 체인 선택 ─►│
          │                           │                       │
          ├── 3. 시험 패턴 이동 ─────►│                       │
          │                           ├── 4. 시험 패턴 구동 ─►│
          │                           │                       │
          │                           │◄─ 5. 입력 캡처•직렬 출력 ┤
          │◄────────────── 관측 비트열 반환 ─────────────────┤
          ▼                           ▼                       ▼
```

### 동작 원리

1. **EXTEST 선택**: 명령 레지스터에 외부 PCB 연결 시험 명령을 이동·갱신한다.
2. **경계 체인 선택**: EXTEST 명령으로 데이터 레지스터 경로를 경계 스캔 셀 체인에 연결한다.
3. **시험 패턴 이동**: TDI로 핀 구동 패턴을 Shift-DR 상태에서 직렬로 적재한다.
4. **시험 패턴 구동**: Update-DR 상태에서 출력 경계 셀이 패턴을 PCB 연결망에 적용한다.
5. **입력 캡처·직렬 출력**: 수신 경계 셀이 Capture-DR로 **캡처 비트열**을 저장하고 Shift-DR로 TDO에 내보내 예상 패턴과 비교한다.

#### 한줄 요약

- EXTEST는 한쪽 경계 셀에서 시험 패턴을 구동하고 반대쪽에서 값을 캡처·직렬 출력해 단선·단락을 판정한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **직렬 와이어 디버그(Serial Wire Debug, SWD)**: Arm 프로세서의 코어와 메모리를 제어하는 2선 패킷 디버그 인터페이스이다.
- **범용 비동기 송수신기(Universal Asynchronous Receiver-transmitter, UART)**: 로그와 콘솔 데이터를 비동기 직렬 방식으로 송수신하는 장치이다.
- **디버그 공격면(Debug Attack Surface)**: 시험 인터페이스를 통해 내부 메모리와 제어 기능에 비인가 접근할 수 있는 위험 범위이다.

</details>

JTAG는 PCB의 다중 IC 연결을 검사하고, SWD는 Arm 코어를 제어하며, UART는 로그를 전달한다.
세 인터페이스의 운영 단계 필수 항목: **디버그 공격면 통제**

| 디버그•시험 인터페이스 | JTAG | SWD | UART |
|:---|:---|:---|:---|
| 적용 기준 | PCB 연결•다중 IC 시험 | 적은 핀의 Arm 디버그 | 단순 로그•명령 채널 |
| 핵심 특징 | **JTAG**의 직렬 경계 스캔 | **SWD**의 2선 코어•메모리 디버그 | **UART**의 비동기 로그•콘솔 |
| 한계 | 시험•디버그 경로 노출 | 코어•메모리 접근 노출 | 콘솔 명령•정보 노출 |

#### 한줄 요약

- PCB 다중 IC 연결 시험은 JTAG, 적은 핀의 Arm 코어 디버그는 SWD, 단순 로그·콘솔은 UART가 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **디버그 인증•잠금(Debug Authentication•Lock)**: 허가된 정비 주체만 포트를 열고 운영 중에는 디버그 접근을 차단하는 통제이다.
- **시간 제한 서비스 모드(Time-limited Service Mode)**: 승인된 정비 시간에만 접근을 허용하고 만료 후 자동으로 잠그는 모드이다.
- **식별 코드•우회(Identification Code•Bypass, IDCODE•BYPASS)**: IDCODE는 체인 장치를 식별하고 BYPASS는 시험하지 않는 집적회로(Integrated Circuit, IC)를 1비트 레지스터로 통과시키는 명령이다.
- **안전 핀 마스크(Safe Pin Mask)**: 외부 시험(External Test, EXTEST) 중 구동하면 위험한 출력 핀을 시험 패턴 대상에서 제외하는 설정이다.

</details>

TAP는 IDCODE와 BYPASS로 IC 체인을 확인한다. EXTEST와 JTAG 접근은 출하 후 인증 정책으로 제한한다.

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 출하 장치의 TAP가 열려 있어 메모리·코어 디버그 악용 | **디버그 인증·잠금**으로 승인된 정비 주체만 허용 | 비인가 내부 접근을 차단해 디버그 공격면 축소 |
| 디버그를 영구 비활성화해 현장 장애 분석 불가 | 인증·감사와 자동 만료가 있는 **시간 제한 서비스 모드** | 평상시 잠금과 승인 정비를 병행 |
| 실제 IC 체인 순서가 도구 설정과 달라 시험 대상 오인 | **IDCODE·BYPASS** 길이와 순서 검증 | 스캔 비트와 IC 대응을 맞춰 대상 식별 정확도 향상 |
| EXTEST에서 두 출력이 충돌하거나 위험 핀을 구동해 보드 손상 | **안전 핀 마스크**와 패턴 검토 | 위험 출력을 제외해 경합·장비 손상 방지 |

#### 한줄 요약

- 생산은 **EXTEST**, 출하 후는 인증된 서비스 모드만 허용이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **생산 시험(Production Test)**: 조립된 인쇄회로기판(Printed Circuit Board, PCB)의 납땜과 집적회로(Integrated Circuit, IC) 사이 연결을 출하 전에 자동 검사하는 공정이다.
- **출하 후 통제(Post-deployment Control)**: 고객 환경에 배포된 장치의 디버그 접근을 인증과 잠금 정책으로 제한하는 운영이다.
- **정비성(Serviceability)**: 장애 분석과 수리를 위해 승인된 절차로 필요한 진단 기능을 사용할 수 있는 성질이다.
- **JTAG 운영 기준**: 생산 시험의 연결 검사와 출하 후 통제 및 정비성 요구에 따라 JTAG 접근 정책을 정하는 기준이다.

</details>

- **JTAG 운영 기준**에 따라 **생산 시험**에는 **EXTEST**, **출하 후 통제**에는 인증·잠금을 적용하되 승인된 **정비성**을 유지한다.

#### 한줄 요약

- 생산 단계에서는 EXTEST로 PCB 연결을 검사하고, 출하 후에는 인증·시간 제한·잠금 정책으로 JTAG 접근을 통제한다.
