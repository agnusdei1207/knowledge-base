---
sidebar:
  order: 50
  label: "050. 쉘코드•ROP 공격 (Shellcode ROP)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "메모리 재사용 및 제어 흐름 변조 방어 : 쉘코드 및 ROP (Shellcode & Return-Oriented Programming)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 50
extra:
  question_no: "050"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "125회 기출, 쉘코드(코드 주입) vs ROP(코드 재사용/가젯 체이닝), DEP/NX 우회 원리, 제어 흐름 무결성(CFI), 하드웨어 Intel CET(Shadow Stack/IBT)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **쉘코드(Shellcode)**: 취약점(Buffer Overflow 등) 공격 성공 시 타깃 프로세스의 메모리 공간에 직접 주입하여 커맨드 쉘(Command Shell) 획득, 네트워크 소켓 오픈, 임의 시스템 명령을 실행하도록 기계어(Opcode)로 작성된 독립 실행형 페이로드.
- **ROP(Return-Oriented Programming, 반환 지향 프로그래밍)**: 메모리 실행 권한을 박탈하는 하드웨어 DEP/NX 방어를 우회하기 위해, 공격자가 새로운 코드를 주입하지 않고 대상 프로세스 메모리(libc 등)에 이미 존재하는 정상 명령어 조각인 **가젯(Gadget: `pop; ret;`)** 들의 주소를 스택에 연속적으로 배치하여 원하는 임의 로직을 실행하는 코드 재사용(Code-Reuse) 공격 기법.

</details>

- 정의/개념: 코드 주입 기반의 **쉘코드(Shellcode)** 와 코드 재사용 기반의 **ROP 공격** 에 대응하여, **DEP/NX(데이터 실행 금지)**, **ASLR/PIE(주소 무작위화)**, **CFI(제어 흐름 무결성)**, **하드웨어 제어 흐름 강제 기술(Intel CET / Shadow Stack & IBT)** 을 결합하는 **차세대 제어 흐름 보호 아키텍처**
- 배경/필요성: DEP/NX 기술 도입으로 데이터 세그먼트(스택/힙)에서의 직접적인 쉘코드 실행은 차단되었으나, 바이너리 내 정상 코드를 엮어 실행 흐름을 하이재킹하는 ROP 및 JOP(Jump-Oriented Programming) 공격을 추가적으로 차단할 요구

#### 한줄 요약
- 쉘코드(코드 주입)는 DEP/NX로 차단하고, ROP(코드 재사용)는 ASLR과 제어 흐름 무결성(CFI) 및 Intel CET로 무력화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ROP 가젯(Gadget)**: 공유 라이브러리(libc) 또는 실행 파일 내부에서 `ret`(0xC3) 명령어로 끝나는 2~3개의 연속된 유효 기계어 명령어 시퀀스(예: `pop rdi; ret;`). 공격자는 스택 포인터(RSP)를 조작하여 가젯들을 체이닝(Chaining)함으로써 튜링 완전(Turing-Complete)한 임의 로직을 구성.
- **Intel CET(Control-flow Enforcement Technology)**: 인텔 CPU 하드웨어에 내장된 보안 기술로, 반환 주소 변조를 막는 **그림자 스택(Shadow Stack)** 과 간접 점프/호출 변조를 막는 **간접 분기 추적(IBT, Indirect Branch Tracking / `ENDBR`)** 을 제공.

</details>

- **코드 주입(Code Injection) vs 코드 재사용(Code Reuse)**: 쉘코드는 새로운 기계어를 메모리에 기록하는 방식이며, ROP는 기존 바이너리의 합법적 코드를 재배치하는 방식
- **DEP/NX 방어 우회성**: ROP는 실행 가능한 텍스트(Text) 세그먼트의 정상 코드를 실행하므로 하드웨어 DEP/NX 보호를 완벽히 우회
- **하드웨어 지원 기반 제어 흐름 보호**: 소프트웨어 CFI의 성능 오버헤드를 극복하기 위해 Intel CET, ARM PAC(Pointer Authentication) 등 CPU 하드웨어 단위 방어 구현

#### 한줄 요약
- 쉘코드의 직접 주입 한계 극복, ROP 가젯 체이닝, DEP/NX 우회성, Intel CET/Shadow Stack 하드웨어 방어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **하드웨어 그림자 스택(Shadow Stack) 동작 메커니즘**:
  - `CALL` 실행 시: 일반 데이터 스택과 CPU 내부 격리된 Shadow Stack에 복귀 주소(RET)를 동시 기록.
  - `RET` 실행 시: 두 스택에 저장된 복귀 주소를 하드웨어 비교하여 불일치(변조) 시 `#CP`(Control Protection) 예외 발생 및 즉각 사살.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 코드 주입 방어: 하드웨어 DEP / NX (Data Execution Prevention) ]   │
│  └─ [ 스택/힙 데이터 영역의 실행 권한 박탈 ➔ 악성 쉘코드 실행 1차 차단 ]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (공격자가 ROP 가젯 체이닝으로 우회 시도)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 주소 예측 방어: Full ASLR & PIE (Position Independent Executable) ]│
│  └─ [ 코드 세그먼트 및 libc 라이브러리 가젯 주소 난수화 ➔ 점프 예측 실패] │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (메모리 릭(Leak)으로 가젯 주소를 알아낸 경우)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 간접 분기 통제: Intel CET - IBT (Indirect Branch Tracking) ]       │
│  └─ [ 간접 JMP/CALL 대상 명령어 첫머리에 `ENDBR` 없으면 비정상 분기 차단 ]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 반환 주소 보호: Intel CET - Shadow Stack (그림자 스택) ]           │
│  ├─ 하드웨어 내부 격리된 그림자 스택에 복귀 주소 사본 기록              │
│  └─ [ 일반 스택 RET 변조 시 ➔ Shadow Stack 사본과 불일치 ➔ 프로세스 강제 사살 ]│
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: DEP/NX가 쉘코드를 차단하고, ASLR이 가젯 탐색을 방해하며, Intel CET의 IBT 및 Shadow Stack이 ROP 실행을 최종 하드웨어 차단하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **하드웨어 DEP/NX** | 스택/힙 메모리 페이지에 No-Execute 비트를 설정하여 주입된 쉘코드의 CPU 실행 거부 | CPU Hardware |
| **ASLR / PIE** | 공유 라이브러리 및 실행 바이너리 가상 주소를 무작위화하여 ROP 가젯 주소 산출 차단 | OS Kernel |
| **제어 흐름 무결성 (CFI)** | 컴파일러가 생성한 정상 제어 흐름 그래프(CFG)를 벗어난 비인가 함수 호출 및 분기 탐지 | Compiler Spec |
| **Intel CET Shadow Stack** | 하드웨어 레벨의 격리 스택을 유지하여 `ret` 실행 시 복귀 주소 무결성을 실시간 검증 | CET Hardware |
| **Intel CET IBT** | `ENDBR64` 명령어로 시작하지 않는 비정상적인 간접 호출/점프 대상을 하드웨어 차단 | Indirect Branch |

#### 한줄 요약
- 하드웨어 DEP/NX, ASLR/PIE, 소프트웨어 CFI, Intel CET Shadow Stack, IBT가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ROP 체이닝 4단계 공격 및 방어 시나리오**:
  1. 버퍼 오버플로우로 스택 프레임 장악
  2. 스택에 가젯 주소(`pop rdi; ret`, `/bin/sh` 주소, `system()` 주소) 연속 배치
  3. 첫 번째 가젯 반환(`ret`) 시 연속 체인 실행 시도
  4. 하드웨어 Shadow Stack 검증 실패로 제어권 탈취 즉각 차단

</details>

```text
1. [취약점 트리거] 스택 버퍼 오버플로우로 반환 주소(RET) 영역에 ROP 가젯 체인 페이로드 주입
            │
            ▼
2. [1차 쉘코드 검사] 주입된 데이터가 실행 코드인지 검사 ➔ 하드웨어 DEP/NX가 데이터 영역 코드 실행 차단
            │
            ▼
3. [ROP 가젯 점프 시도] 공격자가 libc 내부의 `pop rdi; ret` 가젯으로 점프를 시도하여 레지스터 조작 시도
            │
            ▼
4. [ASLR 주소 난수화 대조] Full ASLR 환경에서 가젯 주소 오프셋 불일치 ➔ [잘못된 메모리 참조로 Segmentation Fault]
            │
            ├─ [메모리 정보 유출(Leak)로 가젯 주소를 정확히 맞춘 경우: 최종 방어선]
            ▼
5. [Intel CET 하드웨어 검증]
    ├─ IBT 검사: 점프 대상 위치가 유효한 분기 타깃(`ENDBR64`)인지 하드웨어 검증
    └─ Shadow Stack 검사: 일반 스택의 RET 값과 하드웨어 Shadow Stack의 복귀 주소 대조 ➔ [불일치 감지 즉시 #CP 예외 발생 및 프로세스 강제 종료]
```

**동작 원리**

1. **원천 페이로드 실행 거부**: 쓰기 권한이 있는 스택 영역에서의 CPU 실행 명령어 인출(Fetch) 차단
2. **동적 메모리 구조 은닉**: 실행 시마다 바이너리와 라이브러리 간 상대 오프셋을 재배열하여 가젯 체인 무효화
3. **간접 점프 목적지 제한**: 컴파일러가 사전에 지정한 유효한 함수 진입점 외의 코드 중간 점프 금지
4. **이중 장부 무결성 비교**: 사용자 공간 메모리와 물리적으로 격리된 하드웨어 스택에 복귀 주소를 이중 기록
5. **무관용 프로세스 격리**: 제어 흐름 위반 감지 즉시 CPU 하드웨어 예외를 발생시켜 쉘 획득을 사전 원천 봉쇄

#### 한줄 요약
- 취약점 트리거, DEP/NX 쉘코드 차단, ROP 가젯 점프, ASLR 주소 난수화, Intel CET 하드웨어 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **제어 흐름 탈취 2대 공격 기법 비교**: 쉘코드(Shellcode)와 ROP(Return-Oriented Programming)의 비교.

</details>

| 비교 항목 | 쉘코드 주입 공격 (Shellcode Injection) | 반환 지향 프로그래밍 (ROP Attack) |
|:---|:---|:---|
| **공격 메커니즘** | **공격자가 악성 기계어를 메모리에 직접 주입** | **메모리에 기 존재하는 정상 가젯(`pop; ret;`) 체이닝** |
| **코드의 출처** | **외부 유입 악성 바이너리 코드** | **합법적인 시스템 라이브러리(libc) 및 실행 코드** |
| **하드웨어 DEP/NX 방어력**| **100% 원천 차단 (데이터 영역 실행 불가)** | **우회 가능 (실행 가능한 코드 영역 재활용)** |
| **공격 구현 난이도** | 낮음 (기성 쉘코드 페이로드 사용 가능) | **높음 (바이너리 분석, 가젯 탐색 및 레지스터 정렬 필요)**|
| **최우선 대응 기제** | **하드웨어 DEP/NX 비트 활성화** | **ASLR/PIE + Intel CET (Shadow Stack & IBT)** |

#### 한줄 요약
- 쉘코드는 외부 기계어 직접 주입(DEP로 차단), ROP는 내부 정상 코드 재활용(CET/ASLR로 차단)이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ARM PAC(Pointer Authentication Code)**: ARMv8.3-A 아키텍처에서 포인터 상위 미사용 비트에 암호학적 서명(PAC)을 삽입하여, 포인터 조작 시 서명 검증 실패를 통해 ROP 및 JOP 공격을 하드웨어 레벨에서 원천 차단하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 하드웨어 DEP/NX만 단독 적용하여 **정상 라이브러리 코드를 재활용한 ROP 가젯 체이닝 공격에 서버 장악** | **DEP/NX + Full ASLR + PIE(Position Independent Executable) 전면 다층 적용** | 쉘코드 실행 차단과 ROP 가젯 주소 예측 무력화의 상호보완적 이중 방어 달성 |
| 메모리 정보 유출(Memory Leak) 취약점으로 인해 **ASLR이 무력화되고 정확한 가젯 주소가 계산되어 침해** | **Intel CET(Shadow Stack / IBT) 또는 ARM PAC 하드웨어 제어 흐름 강제 기술 활성화** | 메모리 주소가 노출되더라도 비정상적인 반환 주소 변조를 CPU 레벨에서 100% 차단 |
| 소프트웨어 레벨 CFI 도입 시 발생하는 **심각한 시스템 성능 저하(CPU 오버헤드 20% 이상) 장애** | **컴파일러 `-fcf-protection=full` 옵션 및 CPU 하드웨어 지원 Shadow Stack 활용** | 성능 오버헤드 1% 미만 유지 및 실시간 제어 흐름 무결성 완벽 보장 |

#### 한줄 요약
- ASLR/PIE로 가젯을 숨기고, Intel CET로 주소 유출을 방어하며, 하드웨어 스택으로 오버헤드를 최소화한다.

## Ⅶ. 결론

- 소프트웨어 보안 방어를 우회하기 위해 진화한 코드 재사용 공격을 무력화하는 **쉘코드 및 ROP 다층 방어 아키텍처**는 시스템 보안의 핵심이며, 실무 구현 시 **C/C++ 코드의 안전한 메모리 관리 및 Rust 전환**, **하드웨어 DEP/NX 및 Full ASLR/PIE 컴파일 적용**, **Intel CET(Shadow Stack & IBT) 및 ARM PAC 기반 하드웨어 제어 흐름 무결성 강제**를 통합 구축하여 지능형 메모리 공격에 대한 완전한 시스템 레질리언스를 완성

#### 한줄 요약
- DEP/NX로 쉘코드를 차단하고 ASLR과 Intel CET Shadow Stack으로 ROP 가젯 체이닝을 완벽히 무력화한다.
