---
sidebar:
  order: 50
  label: "050. 쉘코드•ROP 공격"
  badge:
    text: "기출 · 30%"
    variant: note
title: "메모리 재사용 및 제어 흐름 변조 방어 : 쉘코드 및 ROP"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 50
extra:
  question_no: "50"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "125회 기출, 쉘코드(코드 주입) vs ROP(코드 재사용/가젯 체이닝), DEP/NX 우회 원리, 제어 흐름 무결성(CFI), 하드웨어 Intel CET(Shadow Stack/IBT)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Shellcode (쉘코드)**: 시스템 쉘을 획득하기 위해 메모리에 직접 주입하는 어셈블리 기계어 페이로드.
- **ROP (Return-Oriented Programming)**: DEP/NX를 우회하기 위해 libc 내의 정상 명령어 조각(Gadget)들을 연결해 실행하는 코드 재사용 공격.

</details>

- 정의/개념: 메모리 직접 주입형 쉘코드와 정상 코드 재활용형 ROP 공격에 맞서 **DEP/NX, ASLR, Intel CET로 제어 흐름을 보호하는 기술**
- 배경/필요성: 쉘코드 주입을 막는 DEP/NX 도입 이후 등장한 **정상 라이브러리(libc) 가젯 재활용(ROP), 메모리 실행 보호 우회 및 임의 제어권 탈취**

#### 한줄 요약
- DEP/NX로 쉘코드를 차단하고 ASLR과 Intel CET Shadow Stack으로 ROP 가젯 체이닝을 무력화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Gadget (가젯)**: ROP 공격에 사용되는 `pop rdi; ret`와 같이 반환 명령(`ret`)으로 끝나는 짧은 정상 어셈블리 코드 조각.
- **Intel CET Shadow Stack**: 복귀 주소(RET)를 물리적으로 격리된 하드웨어 스택에 이중 저장하여 스택 변조를 감지·차단하는 기술.

</details>

- **코드 주입(Injection)과 코드 재사용(Reuse)의 이원화**: 쉘코드는 **외부 기계어 주입, ROP는 합법적인 기존 바이너리 가젯 체이닝**
- **하드웨어 제어 흐름 무결성(Intel CET) 방어**: 복귀 주소를 **Shadow Stack에 이중 기록하고 `ENDBR64`(IBT)로 비정상 간접 점프 차단**
- **다층 엔트로피 기반 방어선 구축**: Full ASLR 및 PIE를 통해 **가젯의 가상 메모리 절대 주소 예측을 원천 방해**

#### 한줄 요약
- 코드 주입/재사용 이원화, Intel CET 하드웨어 검증, ASLR/PIE 주소 난수화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Intel CET IBT (Indirect Branch Tracking)**: 컴파일러가 생성한 유효한 분기 목적지(`ENDBR64`)가 아닌 중간 가젯으로의 간접 점프를 차단하는 기능.

</details>

```text
[쉘코드 및 ROP 다계층 하드웨어/소프트웨어 방어 아키텍처]
|-- Ingress: 공격자 페이로드 주입 (Shellcode 또는 ROP Gadget Chain)
`-- Layer 1: Hardware DEP/NX (스택/힙 No-Execute 설정 -> 쉘코드 CPU 실행 즉각 차단)
`-- Layer 2: OS ASLR / PIE (libc 가상 주소 무작위화 -> ROP 가젯 주소 산출 방해)
`-- Layer 3: Intel CET IBT (유효하지 않은 가젯 점프 하드웨어 차단)
`-- Layer 4: Intel CET Shadow Stack (하드웨어 격리 스택 RET 대조 -> 불일치 시 프로세스 즉시 사살)
```

선의 의미: DEP/NX가 쉘코드를 차단하고 ASLR이 가젯 탐색을 방해하며 Intel CET의 IBT 및 Shadow Stack이 ROP 실행을 최종 하드웨어 차단하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **하드웨어 DEP/NX** | 스택/힙 메모리에 No-Execute를 설정해 **주입된 쉘코드의 CPU 실행 거부** | CPU Hardware |
| **ASLR / PIE** | 공유 라이브러리 가상 주소를 난수화해 **ROP 가젯 주소 산출 차단** | OS Kernel |
| **제어 흐름 무결성 (CFI)**| 정상 제어 흐름 그래프(CFG)를 벗어난 **비인가 함수 호출 및 분기 탐지** | Compiler Spec |
| **Intel CET Shadow Stack**| 격리된 하드웨어 스택을 유지해 **`ret` 실행 시 복귀 주소 무결성 검증** | CET Hardware |
| **Intel CET IBT** | `ENDBR64`로 시작하지 않는 **비정상적인 간접 호출/점프 하드웨어 차단** | Indirect Branch |

#### 한줄 요약
- 하드웨어 DEP/NX, ASLR/PIE, 소프트웨어 CFI, Intel CET Shadow Stack, IBT가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ROP 체이닝 실행**: 1. 스택 버퍼 장악 → 2. 가젯 주소 배치 → 3. 첫 가젯 반환(`ret`) 시 연속 실행 → 4. Shadow Stack 불일치로 차단.

</details>

```text
취약점 트리거, DEP/NX 검사, ROP 가젯 점프, ASLR 대조 및 Intel CET 검증 파이프라인
        │
   1. [취약점 트리거] 스택 버퍼 오버플로우로 RET 영역에 ROP 가젯 체인 페이로드 주입
        │
   2. [1차 쉘코드 검사] 주입된 데이터가 실행 코드인지 검사 ➔ 하드웨어 DEP/NX가 데이터 영역 코드 실행 차단
        │
   3. [ROP 가젯 점프 시도] 공격자가 libc 내부의 `pop rdi; ret` 가젯으로 점프하여 레지스터 조작 시도
        │
   4. [ASLR 주소 난수화 대조] Full ASLR 환경에서 가젯 주소 오프셋 불일치 ➔ [잘못된 메모리 참조로 SegFault]
        │
   ├─ [메모리 정보 유출로 가젯 주소를 정확히 맞춘 경우: 최종 방어선]
   ▼
5. [Intel CET 하드웨어 검증]
    ├─ IBT 검사: 점프 대상 위치가 유효한 분기 타깃(`ENDBR64`)인지 하드웨어 검증
    └─ Shadow Stack 검사: 일반 스택 RET 값과 하드웨어 Shadow Stack 복귀 주소 대조 ➔ [불일치 시 즉시 프로세스 사살]
```

#### 한줄 요약
- 취약점 트리거 → DEP/NX 쉘코드 차단 → ROP 가젯 점프 → ASLR 주소 난수화 → Intel CET 하드웨어 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **쉘코드 주입 (Shellcode)** vs **반환 지향 프로그래밍 (ROP Attack)**.

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

- **ARM PAC (Pointer Authentication Code)**: 포인터 상위 비트에 암호학적 서명을 삽입하여 조작 시 CPU에서 차단하는 하드웨어 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 하드웨어 DEP/NX만 단독 적용하여 **정상 라이브러리 코드를 재활용한 ROP 공격에 서버 장악** | **`DEP/NX + Full ASLR + PIE(Position Independent Executable) 전면 다층 적용`** | 쉘코드 차단과 가젯 주소 예측 무력화 동시 달성 |
| 메모리 정보 유출(Memory Leak) 취약점으로 **ASLR이 무력화되어 가젯 주소가 계산되는 문제** | **`Intel CET(Shadow Stack / IBT) 또는 ARM PAC 하드웨어 제어 흐름 강제 기술` 활성화** | 주소가 노출되더라도 반환 주소 변조를 CPU에서 100% 차단 |
| 소프트웨어 레벨 CFI 도입 시 발생하는 **심각한 시스템 성능 저하(CPU 오버헤드 20% 이상)** | **컴파일러 `-fcf-protection=full` 옵션 및 `CPU 하드웨어 지원 Shadow Stack 활용`** | 성능 오버헤드 1% 미만 유지 및 제어 흐름 무결성 보장 |
| JIT(Just-In-Time) 컴파일러의 실행 가능한 메모리 생성 결함 악용 | **`W^X 원칙에 입각한 JIT 페이지 쓰기/실행 권한 엄격 분리 및 실시간 전환`** | 브라우저/런타임 JIT 스프레이 및 쉘코드 실행 차단 |

#### 한줄 요약
- ASLR/PIE로 가젯을 숨기고, Intel CET로 주소 유출을 방어하며, 하드웨어 스택으로 오버헤드를 최소화한다.

## Ⅶ. 결론

- 소프트웨어 보안 방어를 우회하기 위해 진화한 코드 재사용 공격을 무력화하는 **쉘코드 및 ROP 다층 방어 아키텍처는 시스템 보안의 핵심**이며, 실무 구현 시 **C/C++ 코드의 안전한 메모리 관리 및 Rust 전환, 하드웨어 DEP/NX 및 Full ASLR/PIE 컴파일 적용, Intel CET(Shadow Stack & IBT) 및 ARM PAC 기반 하드웨어 제어 흐름 무결성 강제**를 통합 구축하여 지능형 메모리 공격에 대한 완전한 시스템 레질리언스 완성

#### 한줄 요약
- 쉘코드 및 ROP 방어는 DEP/NX로 쉘코드를 차단하고 ASLR과 Intel CET Shadow Stack으로 ROP 가젯 체이닝을 무력화하는 시스템 제어 흐름 보호 체계다.