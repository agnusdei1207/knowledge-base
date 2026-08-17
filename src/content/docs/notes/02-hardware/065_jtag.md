---
sidebar:
  order: 65
  label: "065. JTAG 디버깅 인터페이스 (JTAG)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "JTAG 디버깅 인터페이스 (JTAG)"
date: "2026-08-17T09:25:00+09:00"
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

<details><summary>용어 설명</summary>

- **JTAG(Joint Test Action Group)**: PCB 기판 상의 칩 핀 납땜 결함(단락/개방) 검사 및 온칩 디버깅(OCD)을 위해 제정된 국제 표준 인터페이스 (IEEE 1149.1).
- **TAP(Test Access Port)**: JTAG 통신을 위해 칩 외부에 노출된 4~5개의 전용 물리 핀(TCK, TMS, TDI, TDO, nTRST).
- **Boundary Scan(경계 스캔)**: 프로세서 코어 동작을 멈추고 칩 핀 경계에 배치된 스캔 셀을 통해 핀 입출력을 직접 검사하는 기술.

</details>

- 정의/개념: 인쇄회로기판(PCB) 상의 집적회로(IC) 핀 납땜 상태 검사(Boundary Scan) 및 프로세서 코어 디버깅/펌웨어 프로그래밍을 위해 표준화된 4~5핀 전용 직렬 인터페이스 (IEEE 1149.1 규격)
- 배경/필요성: BGA(Ball Grid Array) 등 초고밀도 패키징으로 인해 물리적 프로브 접촉이 불가능해짐에 따라, **비접촉식 경계 스캔(Boundary Scan) 자동화 검사 및 온칩 디버깅(OCD) 표준화 필수**

#### 한줄 요약

- 4~5개 핀으로 **PCB 납땜 불량 경계 스캔 검사(Boundary Scan) 및 온칩 디버깅(OCD) 수행**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Daisy Chain(데이지 체인)**: 보드 위의 여러 칩을 직렬로 연결하여 단일 JTAG 포트로 모든 칩의 스캔 레지스터를 순차 접근하는 구조.
- **Boundary-Scan Cell(BSR Cell)**: 칩의 각 I/O 핀과 내부 로직 사이에 배치되어 신호를 가로채거나(Capture) 강제 출력(Update)하는 시프트 레지스터 셀.

</details>

- 다수의 칩을 단일 직렬 루프로 엮어 4개의 핀만으로 검사하는 **직렬 데이지 체인(Daisy Chain)** 구조
- 내부 코어 로직과 물리 핀을 분리하여 핀 상태를 강제 구동/캡처하는 **경계 스캔 셀(Boundary-Scan Register)** 내장
- 하드웨어 브레이크포인트 설정, CPU 레지스터 읽기/쓰기, 플래시 메모리 프로그래밍을 지원하는 **온칩 디버깅(OCD)** 기능

#### 한줄 요약

- **직렬 데이지체인 스캔(Daisy Chain)·경계 스캔 셀(Boundary Scan Cell)·16상태 TAP FSM 제어**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAP Controller**: TMS와 TCK 신호를 인가받아 16개 상태를 전이하는 유한 상태 머신(FSM).
- **Instruction Register(IR)**: EXTEST, SAMPLE/PRELOAD, BYPASS, IDCODE 등의 동작 모드 명령어를 저장하는 레지스터.
- **Data Register(DR)**: 핀 상태를 담는 BSR(Boundary Scan Register), 장치 IDCODE 레지스터, 1비트 직결 BYPASS 레지스터.

</details>

```text
[ JTAG TAP 아키텍처 및 경계 스캔 셀 구조도 ]
 [TCK] ──┐
 [TMS] ──┼──> [ 16상태 TAP 컨트롤러 (FSM) ]
 [TRST] ─┘          │          │
                    ▼          ▼
           [ 명령 레지스터 (IR) ]   [ 데이터 레지스터 (DR) ]
           (EXTEST / BYPASS)     ├─ IDCODE 레지스터
                    │            ├─ BYPASS 레지스터 (1비트)
 [TDI] ─────────────┴───────────>└─ 경계 스캔 레지스터 (BSR) ───> [TDO]
                                           │
                                  [ 물리 칩 I/O 핀 연결 ]
```

선의 의미: TAP 신호선(TCK/TMS/TDI/TDO), 16상태 TAP 컨트롤러, 명령 레지스터(IR), 데이터 레지스터(BSR/IDCODE/BYPASS) 및 경계 스캔 셀 간의 JTAG 아키텍처 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 탭 제어기 | TMS 신호를 받아 16단계 상태 머신(FSM)을 미친 듯이 휙휙 돌리며 칩을 조종하는 지휘관 |
| 명령 레지스터 | 핀을 강제 구동할지(EXTEST), 구경만 할지(SAMPLE) 명령어를 받아 적는 작전 지시서 |
| 데이터 레지스터 | 핀 껍데기 상태 데이터(BSR)나 칩 고유 아이디(IDCODE)를 싣고 나르는 데이터 기차 |
| 경계 스캔 셀 | 칩 핀에 딱 달라붙어서 핀의 상태를 훔쳐보거나(Capture) 억지로 전기를 쑤셔 넣는(Update) 첩자 |

#### 한줄 요약

- **TAP 신호선(TCK/TMS/TDI/TDO)·16상태 TAP 컨트롤러·명령 레지스터(IR)·데이터 레지스터(BSR/BYPASS)**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **EXTEST(External Test)**: 칩 내부 코어를 분리하고 경계 스캔 셀을 통해 칩 외부 핀으로 테스트 패턴을 출력하여 인접 칩 간의 솔더링 단락(Short)/개방(Open)을 검사하는 명령어.

</details>

```text
[ JTAG EXTEST 기반 PCB 핀 단락 검사 흐름 ]
                         │
                         ▼
   [ 1. Shift-IR 상태에서 명령 레지스터(IR)에 EXTEST 명령어 로드 ]
                         │
                         ▼
   [ 2. Shift-DR 상태에서 TDI 핀을 통해 BSR에 테스트 비트 패턴 시프트 ]
                         │
                         ▼
   [ 3. Update-DR 상태에서 칩 A의 출력 핀으로 테스트 전압 강제 출력 ]
                         │
                         ▼
   [ 4. Capture-DR 상태에서 칩 B의 입력 핀 신호를 BSR로 캡처 ]
                         │
                         ▼
   [ 5. Shift-DR 상태에서 TDO 핀으로 캡처 데이터 추출 및 불량 판정 ]
```

**동작 원리**

1. **명령 로드**: TAP FSM을 조작하여 IR에 EXTEST 명령어를 시프트 인(Shift-IR)
2. **패턴 시프트**: TDI 핀으로 0과 1로 구성된 테스트 벡터를 BSR 셀 체인으로 로딩(Shift-DR)
3. **핀 강제 구동**: Update-DR 상태에서 송신 칩 A의 출력 핀에 신호 인가
4. **신호 캡처**: 수신 칩 B의 BSR 셀이 물리 핀을 통해 들어온 전압 레벨을 저장(Capture-DR)
5. **결과 분석**: TDO 핀으로 추출한 비트열을 기대값과 비교하여 납땜 단락/오픈 검출

#### 한줄 요약

- EXTEST 명령 로드 $\to$ **테스트 패턴 Shift-DR 시프트 $\to$ Update-DR 핀 출력 $\to$ Capture-DR 핀 수신 $\to$ TDO 출력 비교 검증**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **JTAG vs SWD vs UART**:
  - JTAG: 4~5핀, 경계 스캔(PCB 검사) + OCD, 멀티 벤더 표준 (IEEE 1149.1)
  - SWD: 2핀(SWCLK/SWDIO), Arm 전용 온칩 디버깅, 핀 절약
  - UART: 2핀(TX/RX), 비동기 직렬 콘솔 로그, 하드웨어 디버깅 불가

</details>

| 비교 항목 | JTAG (IEEE 1149.1 표준) | SWD (Serial Wire Debug, Arm) | UART (범용 비동기 콘솔) |
|:---|:---|:---|:---|
| 핀 구성 및 프로토콜 | 4~5핀 (TCK, TMS, TDI, TDO, TRST) | 2핀 (SWCLK, SWDIO 양방향) | 2핀 (TX, RX 비동기 직렬) |
| 핵심 기능 범위 | PCB 납땜 경계 스캔 + CPU 레지스터 디버깅 | Arm 코어 디버깅 + 플래시 프로그래밍 | 텍스트 로그 출력 + 단순 CLI 통신 |
| 한계 및 보안 위험 | 많은 핀 수 소모, 출하 후 JTAG 포트 보안 취약 | 경계 스캔(PCB 납땜 검사) 불가, Arm 전용 | 하드웨어 브레이크포인트/디버깅 불가 |

#### 한줄 요약

- PCB 검사/표준 디버깅은 **JTAG**, 핀 절약 Arm 디버깅은 **SWD**, 로그는 **UART**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Debug Lock (eFuse Blow)**: 상용 출하 전 온칩 eFuse를 물리적으로 태워 JTAG/SWD 디버그 포트 접근을 영구 차단하는 보안 잠금 기술.
- **BYPASS Register**: 미검사 대상 칩을 1클록 지연으로 건너뛰어 전체 스캔 체인 길이와 검사 시간을 단축하는 1비트 레지스터.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공장 출하 후 **제이태그** 포트를 열어뒀더니 해커가 꽂아서 펌웨어와 암호 키를 싹 다 뽑아가는 끔찍한 보안 대참사 발발 | 출하 직전에 칩 내부의 eFuse를 레이저로 태워 끊어버리는 얄짤없는 **디버그 퓨즈 잠금** 인가 및 JTAG 비활성화 | 칩이 뼛속까지 박살 나지 않는 한 그 누구도 펌웨어에 접근할 수 없는 하드웨어 원천 차단 100% 달성 |
| 줄줄이 엮인 스캔 체인 상에서 중간에 있는 칩 하나가 뻗어버려 전체 테스트 라인이 통째로 셧다운되는 마비 사태 | 뻗어버린 칩에 **우회 패스**(BYPASS) 명령을 내려 데이터를 1비트만 거치게 하고 그냥 점프시켜 버림 | 한 놈이 죽어 자빠져도 나머지 멀쩡한 체인의 테스트 가용성을 멱살 잡고 강제로 유지시켜 줌 |
| 핀 강제 구동 테스트(EXTEST) 도중 합선(Short)된 핀에 전기를 잘못 뿜어내 보드와 칩이 아예 타버리는 끔찍한 파손 위험 | 전원 핀이나 민감한 핀은 건드리지 못하게 사전에 안전 핀 마스크를 씌워 구동을 원천 통제 | 핀 강제 조작으로 애먼 칩 껍데기를 태워 먹는 물리적 전기 파손 참사를 완벽하게 예방함 |

#### 한줄 요약

- **eFuse 기반 Debug Port Lock·BYPASS 명령 단선 우회·안전 핀 마스크(Short 파손 방지)**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **IEEE 1149.7 (cJTAG)**: 기존 JTAG의 4핀 구조를 2핀으로 축소하면서 경계 스캔과 전력 절감 기능을 제공하는 확장 표준.

</details>

- 양산 검사 및 디버깅에서 **JTAG/SWD 인터페이스 활용 후 최종 출하 시 eFuse 영구 블로잉(Debug Disable) 표준 채택**

#### 한줄 요약

- **양산 연결성 테스트(JTAG)와 양산 후 하드웨어 보안 잠금(eFuse Lock)**의 생애주기 관리
