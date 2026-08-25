---
sidebar:
  order: 65
  label: "065. JTAG 디버그 인터페이스 (JTAG)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "JTAG 디버그 인터페이스 (JTAG)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 65
extra:
  question_no: "065"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "경계 스캔 테스트와 온칩 디버깅의 표준 인터페이스"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **JTAG(Joint Test Action Group, IEEE 1149.1)**: 집적회로(IC)의 핀 결선 테스트(경계 스캔)와 펌웨어 플래싱 및 온칩 디버깅을 지원하는 표준 하드웨어 인터페이스.
- **경계 스캔(Boundary Scan)**: IC 내부 로직과 외부 I/O 핀 사이에 스캔 셀(Scan Cell)을 배치하여 물리적 접촉 없이 직렬 통신만으로 핀의 전압 상태를 읽고 쓰는 테스트 기법.

</details>

- 정의/개념: **경계 스캔** 셀을 통해 물리적 접촉 없이 배선을 검사하고 온칩 디버깅을 지원하는 **JTAG** 표준 인터페이스
- 배경/필요성: 고밀도 BGA 패키지 환경에서 **물리 프로브 접촉 불가 및 수동 핀 검사 비용 과다**

#### 한줄 요약
- JTAG은 경계 스캔 셀을 직렬 데이지 체인으로 연결하여 PCB 납땜 결함을 검사하고 온칩 디버깅을 수행하는 표준 규격이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TAP(Test Access Port) 컨트롤러**: TMS와 TCK 신호의 변화에 따라 동작하는 16개 상태를 가진 유한 상태 기계(FSM).
- **BSDL(Boundary Scan Description Language)**: 특정 IC의 경계 스캔 구조와 명령어, 핀 매핑 정보를 정의한 표준 텍스트 파일.

</details>

- 4개 필수 신호선(TCK, TMS, TDI, TDO)만으로 동작하는 직렬 테스트 인터페이스
- **TAP 컨트롤러**의 16개 상태 전이 머신을 기반으로 명령어 및 데이터 레지스터 직렬 시프트 제어
- 복수 IC를 직렬 데이지 체인(Daisy Chain)으로 연결하여 단일 헤더로 보드 전체 검사

#### 한줄 요약
- 소수의 전용 핀으로 16개 상태의 TAP FSM을 구동하여 칩 내부 로직과 외부 배선을 완전히 분리 검사한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IR(Instruction Register)**: 실행할 테스트 명령어(EXTEST, SAMPLE, BYPASS 등)를 저장하는 레지스터.
- **DR(Data Register)**: BSR, BYPASS, IDCODE 등 실제 테스트 데이터가 시프트되는 레지스터 그룹.

</details>

```text
[JTAG TAP 아키텍처]
|-- TAP 신호 핀 (TCK·TMS·TDI·TDO 및 선택적 TRST)
|-- TAP 컨트롤러 (16-State FSM 상태 머신)
|-- 명령어 레지스터 (IR - EXTEST·SAMPLE·BYPASS 디코더)
`-- 데이터 레지스터 (DR 그룹)
    |-- 경계 스캔 레지스터 (BSR - I/O 핀 결합 스캔 셀)
    |-- 디바이스 ID 레지스터 (IDCODE)
    `-- 바이패스 레지스터 (BYPASS - 1비트 단축 경로)
```

선의 의미: 계층 및 신호 경로 구조

| 구성요소 | 책임 |
|:---|:---|
| TAP 신호 핀 | TCK(클록), TMS(모드 제어), TDI(직렬 입력), TDO(직렬 출력) 제공 |
| **TAP 컨트롤러** | TMS 신호에 따라 16개 FSM 상태를 전이하며 캡처, 시프트, 갱신 제어 |
| **명령어 레지스터(IR)** | 실행할 테스트 명령어(EXTEST, SAMPLE/PRELOAD, BYPASS) 보관 |
| 경계 스캔 레지스터(BSR) | 각 I/O 핀과 내부 로직 사이에 위치하여 핀 신호 구동 및 캡처 |
| 바이패스 레지스터 | 비검사 칩의 직렬 경로를 1비트로 단축하여 스캔 오버헤드 최소화 |

#### 한줄 요약
- TAP 컨트롤러, IR, BSR, 바이패스 레지스터가 직렬 시프트 경로로 결합되어 테스트를 수행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **EXTEST**: 칩 내부 로직과 핀을 분리하고 경계 스캔 셀을 통해 칩 외부 PCB 배선의 단선/단락을 검사하는 명령어.

</details>

```text
테스트 장비 연결 후 모든 칩 TAP 리셋 (TMS=1 5회 인가)
        │
   현재 칩이 검사 대상인가?
   ┌────┴─────┐
아니오          예
   │             │
바이패스 명령   외부 결선 검사 명령어(EXTEST) 적재
(1비트 통과)      │
   │        핀 구동용 테스트 패턴을 BSR에 직렬 시프트
   │             │
   │        수신 칩 스캔 셀이 한 클록에 핀 전압 캡처
   └────┬────────┘
        │
   캡처된 비트열을 TDO로 직렬 인출
        │
   회로 넷리스트와 일치하는가?
   ┌────┴─────┐
  예           아니오
   │             │
정상 판정      단선·단락 위치 특정 및 리포트
```

#### 한줄 요약
- TAP 리셋 → EXTEST/BYPASS 명령어 로드 → 테스트 패턴 주입 및 핀 캡처 → TDO 인출 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SWD(Serial Wire Debug)**: Arm Cortex-M 프로세서에서 2개 핀(SWCLK, SWDIO)만으로 디버깅을 지원하는 인터페이스.
- **ICE(In-Circuit Emulator)**: 타깃 CPU 소켓을 하드웨어 에뮬레이터로 대체하여 실시간 디버깅을 수행하는 고비용 장비.

</details>

| 하드웨어 디버그 인터페이스 | JTAG (IEEE 1149.1) | SWD (Serial Wire Debug) | UART | In-Circuit Emulator (ICE) |
|:---|:---|:---|:---|:---|
| 적용 기준 | PCB 보드 결선 검사 및 복수 칩 체인 | Arm Cortex-M 초소형 핀 제약 디버깅 | 콘솔 로그 출력 및 단순 직렬 통신 | 레거시 CPU 하드웨어 전용 에뮬레이션 |
| 핵심 특징 | 4선(TCK/TMS/TDI/TDO) 및 경계 스캔 | 2선(SWCLK/SWDIO) 직렬 양방향 디버깅 | 2선(TX/RX) 비동기 문자열 전송 | CPU 소켓을 직접 대체해 실시간 분석 |
| 한계 | 많은 핀 수(4~5핀) 소모 및 복잡한 FSM | 경계 스캔(보드 결선 검사) 기능 미지원 | CPU 레지스터 직접 제어/브레이크 불가 | 극심한 고비용 및 현대 BGA 칩 적용 불가 |

#### 한줄 요약
- 보드 레벨 결선 검사 및 복수 칩 체인에는 JTAG을, 핀 수가 부족한 MCU 디버깅에는 SWD를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **JTAG 보안 잠금(JTAG Fuse/Lock)**: 상용 제품 양산 출하 시 eFuse를 끊거나 암호 인증을 걸어 해커가 JTAG으로 펌웨어를 추출하지 못하도록 차단하는 보안 조치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 출하 후 디버그 포트를 통한 펌웨어 탈취 | **JTAG 보안 잠금** 및 암호학적 인증 디버그 적용 | 비인가 디버그 접근 차단 및 IP 보호 |
| 데이지 체인 내 단일 칩 고장 시 전체 마비 | 체인 분할 설계 및 바이패스 멀티플렉서 장착 | 불량 칩 신속 격리 및 검사 연속성 유지 |
| 긴 테스트 케이블 신호 반사 및 노이즈 | 종단 저항(Termination) 및 슈미트 트리거 버퍼 장착 | 신호 무결성(SI) 확보 및 오판정 방지 |
| 복잡한 다층 BGA의 간헐적 냉납 결함 | **BSDL** 기반 자동 경계 스캔 및 X-ray 검사 병행 | 솔더링 불량 검출률 99% 이상 달성 |

#### 한줄 요약
- 양산 후 JTAG Fuse 잠금으로 펌웨어 추출을 방지하고 BSDL 자동화로 BGA 냉납 결함을 검출한다.

## Ⅶ. 결론

- 고밀도 PCB 보드 제조 검사는 **JTAG 경계 스캔**을 적용하고, 양산 출하 시 **eFuse 보안 잠금**을 통해 역공학 방지

#### 한줄 요약
- JTAG은 물리적 접촉이 불가능한 초미세 반도체 패키징 시대에 필수적인 제조 테스트 및 온칩 디버깅 인터페이스다.