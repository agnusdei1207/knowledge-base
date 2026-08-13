---
sidebar:
  order: 65
  label: "065. JTAG 디버깅 인터페이스 (JTAG)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "JTAG 디버깅 인터페이스 (JTAG)"
date: "2026-08-13T12:00:06+09:00"
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

- **JTAG(Joint Test Action Group)**: IC 칩셋 및 PCB 핀 연결 상태를 직렬 경계 스캔으로 검사하는 물리 인터페이스
- **TAP(Test Access Port)**: JTAG 통신을 위한 4~5개 물리 신호 핀을 관리하는 포트 제어기
- **경계 스캔(Boundary Scan)**: IC 물리 핀과 로직 사이에 전용 셀을 배치하여 외부 탐침 없이 전기적 상태를 강제 인가/관측하는 검사 기술

</details>

- 정의/개념: TAP 상태 머신 및 경계 스캔 셀 체인을 통해 PCB 물리적 핀 납땜 및 배선 단락을 비침습 방식으로 검사하는 **JTAG**
- 배경/필요성: BGA(Ball Grid Array) 등 고밀도 패키지 상에서 물리 핀 접근이 불가능해짐에 따른 비접촉 테스트 자동화 요구성

#### 한줄 요약

- JTAG는 IC 핀 주변의 경계 스캔 셀을 직렬 연결해 PCB 배선을 외부 탐침 없이 구동·관측한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **직렬 스캔 체인(Serial Scan Chain)**: 복수의 IC 경계 셀들을 TDI-TDO 형태로 엮어 데이터를 직렬 전송하는 경로
- **경계 스캔 셀(Boundary-Scan Cell)**: 물리 핀에 결합되어 값을 강제 구동하거나 캡처하는 하드웨어 래치

</details>

- 복수 IC의 핀 검사를 단일 포트로 통합 수용하는 **직렬 스캔 체인** 구조
- SAMPLE은 비침습 관측, EXTEST는 코어와 분리해 **경계 스캔 셀** 구동
- 프로세서 레지스터, 온칩 Flash 덤프 및 CPU 브레이크포인트 제어 수용

#### 한줄 요약

- 여러 IC의 시험 레지스터를 TDI·TDO 직렬 체인으로 연결하면 하나의 TAP 경로에서 각 장치의 핀 연결을 검사할 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **TAP 제어기(TAP Controller)**: TMS 신호 및 TCK 클록에 맞춰 16개 내부 유한 상태 머신(FSM) 상태를 전이하는 제어 모듈.
- **명령 레지스터(IR, Instruction Register)**: EXTEST, INTEST, SAMPLE/PRELOAD 등 실행할 JTAG 명령어를 수용하는 레지스터.
- **데이터 레지스터(DR, Data Register)**: BSR(Boundary Scan Register), Bypass Register, IDCODE 레지스터 등을 총칭하는 데이터 이동 레지스터.
- **TDI/TDO**: 직렬 데이터 입력(TDI) 및 직렬 데이터 출력(TDO) 물리 신호 핀.

</details>

```text
                 [명령 레지스터]
                        |
                        |
                 [TAP 제어기] -- [데이터 레지스터] -- [경계 스캔 셀]
```

선의 의미: TAP 제어기 FSM 제어 하에 명령 레지스터(IR) 및 데이터 레지스터(DR)가 선택되어 물리 핀 경계 셀 체인을 구동하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| TAP 제어기 | TMS/TCK 물리 신호 해독 및 16-State FSM 전이 관장 |
| 명령 레지스터(IR) | JTAG 검사 명령(**EXTEST**, **BYPASS** 등) 인코딩 및 디코딩 |
| 데이터 레지스터(DR) | BSR 경계 스캔 데이터 및 IDCODE 직렬 시프트 이동 전송 |
| 경계 스캔 셀 | 물리 IC 핀 값 캡처(Capture-DR) 및 구동(Update-DR) 수행 |

#### 한줄 요약

- TAP 제어기는 TMS·TCK로 IR 또는 DR의 캡처·이동·갱신 상태를 선택하고 경계 셀이 핀 값을 관측·구동하게 한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **EXTEST(External Test)**: IC 외부 PCB 패턴 배선 간의 쇼트(Short) 및 오픈(Open) 단선 여부를 테스트하는 기본 JTAG 명령어.
- **시험 패턴(Test Pattern)**: PCB 인쇄 배선망의 단락을 검증하기 위해 TDI로 인가하는 0/1 시퀀스 비트열.

</details>

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

1. **EXTEST 선택**: TAP 제어기 FSM을 통하여 IR 레지스터에 **EXTEST** 명령 인가.
2. **경계 체인 선택**: BSR(Boundary Scan Register) 데이터 레지스터 체인 선로 선택.
3. **시험 패턴 이동**: TDI 신호선을 통해 **시험 패턴** 비트열을 BSR 체인 상으로 Shift-DR 처리.
4. **시험 패턴 구동**: Update-DR 상태 전이를 통하여 수송된 패턴 비트를 IC 물리 핀 밖으로 강제 인가.
5. **입력 캡처·직렬 출력**: 상대 IC 물리 핀 경계 셀에서 Capture-DR 수용 및 TDO 핀으로 비트열 인출/비교.

#### 한줄 요약

- EXTEST는 한쪽 경계 셀에서 시험 패턴을 구동하고 반대쪽에서 값을 캡처·직렬 출력해 단선·단락을 판정한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **SWD(Serial Wire Debug)**: Arm 코어 전용 2-Pin(SWCLK, SWDIO) 경량 디버깅 인터페이스.
- **UART**: asynchronous 직렬 비동기 통신을 통한 콘솔 및 CLI 로그 인터페이스.

</details>

| 디버그/시험 인터페이스 | JTAG (IEEE 1149.1) | SWD (Serial Wire Debug) | UART |
|:---|:---|:---|:---|
| 적용 기준 | PCB 핀 경계 스캔 및 다중 IC 체인 검사 시 | 핀 수가 부족한 콤팩트 Arm MCU 디버깅 시 | 시스템 로그 확인 및 시리얼 CLI 제어 시 |
| 핵심 특징 | **JTAG** 4~5-Pin 기반 표준 BSR 직렬 체인 | **SWD** 2-Pin 기반 코어·메모리 직접 접근 | **UART** 비동기 직렬 텍스트 통신 |
| 한계 | 핀 수 소모(4~5개) 및 보안 공격 표면 노출 | Arm 특화 표준 및 Boundary Scan 미지원 | 디버그 브레이크포인트/경계 검사 불가 |

#### 한줄 요약

- PCB 다중 IC 연결 시험은 JTAG, 적은 핀의 Arm 코어 디버그는 SWD, 단순 로그·콘솔은 UART가 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **디버그 인증·잠금(Debug Lock/Fuse)**: 출하 후 인증된 주체만 JTAG 접근을 허용하거나 영구 비활성화하는 보안 설정.
- **IDCODE/BYPASS**: IDCODE를 통한 칩셋 ID 확인 및 BYPASS 명령을 통한 무관 IC 레지스터 1-Bit 우회 처리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 양산 출하 후 **JTAG** 포트를 통한 펌웨어/키 탈취 위험 | eFuse 비트 컷 기반 **디버그 인증·잠금** 인가 | 하드웨어 차원 비인가 역공학 차단 |
| 스캔 체인 상의 특정 IC 고장으로 전체 스캔 마비 | **BYPASS** 레지스터 적용을 통한 고장 IC 건너뛰기 | 나머지 체인 테스트 가용성 유지 |
| EXTEST 테스트 도중 부품 전기적 파손(Short) 위험 | **안전 핀 마스크** 적용 및 전원 핀 구동 제한 | 검사 도중 칩셋 물리적 파손 예방 |

> 사례: eFuse 기반 **JTAG Lock** 인가를 통한 소스 펌웨어 하드웨어 탈취 방지

#### 한줄 요약

- 생산은 **EXTEST**, 출하 후는 인증된 서비스 모드만 허용이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **JTAG 운영(JTAG Operation)**: 양산 검사 단계의 BSR 테스트와 출하 후 보안 Lock 설정 기반의 생애주기 관리

</details>

- 양산은 **EXTEST**, 출하는 **인증 잠금**, 현장 복구가 불필요하면 영구 비활성화

#### 한줄 요약

- 양산은 EXTEST를 허용하고 출하 후는 인증 잠금이나 영구 비활성화를 적용한다.
