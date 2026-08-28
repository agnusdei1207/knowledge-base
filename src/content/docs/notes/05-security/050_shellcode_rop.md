---
sidebar:
  order: 50
  label: "050. 쉘코드•ROP 공격"
  badge:
    text: "기출 · 30%"
    variant: note
title: "메모리 재사용 및 제어 흐름 변조 방어 : 쉘코드 및 ROP"
date: "2026-08-26T14:49:01+09:00"
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
- 배경/필요성: DEP/NX가 데이터 영역의 실행 권한을 회수해 코드 주입 경로를 막은 대가로 공격이 새 코드를 넣지 않고 이미 실행 권한을 가진 libc 명령 조각을 `ret`로 이어 붙이는 **코드 재사용** 계층으로 옮겨 갔으므로, 방어 역시 실행 권한 통제에서 복귀 주소 무결성을 CPU가 대신 보증하는 계층으로 이동할 필요

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
- ROP는 자기 코드를 주입할 자유를 포기한 대가로 DEP/NX의 전제 자체를 비껴가므로, 방어의 축도 코드의 출처를 묻는 실행 권한 통제에서 복귀 주소의 진위를 묻는 무결성 검증으로 옮겨 간다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Intel CET IBT (Indirect Branch Tracking)**: 컴파일러가 생성한 유효한 분기 목적지(`ENDBR64`)가 아닌 중간 가젯으로의 간접 점프를 차단하는 기능.

</details>

```text
쉘코드·ROP 방어 구조
|-- CPU 하드웨어
|   |-- DEP·NX
|   `-- Intel CET
|       |-- IBT
|       `-- Shadow Stack
|-- 운영체제
|   `-- ASLR
`-- 컴파일러
    `-- PIE·CFI
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
- 다섯 요소 중 DEP/NX와 ASLR은 공격 비용을 높이는 확률적 완화에 머무는 반면, 복귀 주소를 하드웨어에 이중 보관하는 Shadow Stack만이 주소 유출 여부와 무관하게 결정적으로 차단한다.

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

- 1. 취약점 트리거
- 2. 1차 쉘코드 검사
- 3. ROP 가젯 점프 시도
- 4. ASLR 주소 난수화 대조
- 5. Intel CET 하드웨어 검증

#### 한줄 요약
- DEP는 코드의 출처를, ASLR은 주소의 예측 가능성을 다루므로 메모리 정보 유출 한 건에 둘의 전제가 함께 무너지지만, Shadow Stack은 유출과 무관하게 복귀 주소 사본을 대조하므로 최종 방어선이 된다.

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

- 쉘코드는 **DEP/NX**, ROP는 **ASLR·CET**로 차단하고 메모리 안전 언어로 전환

#### 한줄 요약
- 쉘코드 및 ROP 방어는 DEP/NX로 쉘코드를 차단하고 ASLR과 Intel CET Shadow Stack으로 ROP 가젯 체이닝을 무력화하는 시스템 제어 흐름 보호 체계다.
