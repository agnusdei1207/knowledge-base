---
sidebar:
  order: 4
  label: "004. RISC-V 개방형 ISA (RISC-V Open Standard ISA)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "RISC-V 개방형 ISA (RISC-V Open Standard ISA)"
date: "2026-08-13T12:00:00+09:00"
tags:
  - "notes-hardware"
weight: 4
extra:
  question_no: "004"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "개방형 ISA•확장•적합성 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RISC-V**: 로열티 없는 개방형 표준으로 기본 정수 명령어와 표준•사용자 정의 확장을 조합하는 ISA이다.
- **명령어 집합 아키텍처(Instruction Set Architecture, ISA)**: 소프트웨어가 프로세서를 제어하기 위한 기계어 명령, 레지스터 집합, 메모리 데이터 형태 및 시스템 콜 사양을 정의하는 인터페이스.
- **개방형 ISA 규격(Open ISA Specification)**: 특정 기업의 독점 라이선스에 얽매이지 않고 누구나 자유롭게 하드웨어 코어를 구현하거나 명령어를 확장할 수 있도록 사양이 완전 공개된 규격.
- **사용자 정의 확장(Custom Extension)**: 특정 AI 가속, 암호화, 신호 처리 연산을 위해 예약된 커스텀 인코딩 영역에 독자 명령어를 추가하는 하드웨어 확장 체계.

</details>

- 정의/개념: 모듈형 설계를 기반으로 필수 기본 정수 ISA(RV32I, RV64I 등)에 부동소수점, 벡터, 사용자 정의 커스텀 확장을 자유롭게 결합할 수 있는 **개방형 ISA 규격(RISC-V)**.
- 배경/필요성: 독점 ISA의 라이선스와 확장 제약은 도메인 특화 코어의 독자 구현과 공급망 다변화를 제한한다.

#### 한줄 요약
- RISC-V는 무료 개방형 라이선스를 바탕으로 기본 ISA와 커스텀 모듈 확장을 조합하여 도메인 특화 프로세서를 자유롭게 구현 가능함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **기본 ISA(Base ISA)**: 모든 RISC-V 호환 코어가 의무적으로 구현해야 하는 최소 단위의 40여 개 정수 연산 명령어 집합(RV32I/RV64I/RV128I/RV32E).
- **표준 확장(Standard Extension)**: RISC-V International에서 관리하는 공식 사양으로, M(곱셈/나눗셈), A(원자적 연산), F/D(부동소수점), C(압축), V(벡터) 등의 모듈형 확장 세트.
- **마이크로아키텍처(Microarchitecture)**: 동일한 RISC-V ISA 사양을 만족시키면서 칩 제조업체가 독자적으로 설계한 파이프라인 수, 분기 예측기, 캐시 구조 등 물리적 프로세서 회로.

</details>

- 라이선스 및 로열티 비용이 전혀 없는 **개방형 ISA 규격(Open ISA Specification)**을 채택하여 독자적인 반도체 칩 코어 설계 및 특화 SoC 제작 허용.
- 소형 MCU용 **기본 ISA(Base ISA)**에 필요에 따른 **표준 확장(Standard Extension)**과 특화 연산용 **사용자 정의 확장(Custom Extension)**을 모듈식 레고 블록 형태로 자유롭게 조합.
- ISA 사양 사양서와 칩 내부의 물리적 회로 구현체인 **마이크로아키텍처(Microarchitecture)**를 분리하여 동일 ISA 기반의 다양한 오픈소스 및 상용 고성능 코어 생성 가능.

#### 한줄 요약
- Base ISA 기반의 모듈식 Extension 조합 특성을 활용하여 동일 ISA 규격 하에서도 다양한 마이크로아키텍처 파이프라인 구현이 가능함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ISA 프로파일(ISA Profile)**: 범용 OS 구동 및 바이너리 소프트웨어 생태계 호환성을 위해 필수 확장 조합을 그룹화한 표준 프로파일(예: RVA22, RVI20).
- **권한 아키텍처(Privileged Architecture)**: 시스템 모드간 격리와 예외/인터럽트 처리를 규정한 하드웨어 사양(M-mode: Machine, S-mode: Supervisor, U-mode: User).
- **XLEN**: RISC-V 프로세서의 정수 레지스터 기본 비트 폭으로, 32비트(RV32), 64비트(RV64), 128비트(RV128)를 의미함.
- **공통 실행 계약(Common Execution Contract)**: 소프트웨어가 코어 종류에 관계없이 동일한 기계어 결과를 얻을 수 있도록 보장하는 기본 명령어 동작 규약.
- **특권 동작(Privileged Operation)**: 하이퍼바이저, OS 커널, 하드웨어 보안 처리를 위해 S-Mode 및 M-Mode에서만 접근이 허용되는 시스템 레지스터(CSR) 조작 명령.
- **툴체인(Toolchain)**: GCC, LLVM/Clang, GDB 등 RISC-V 전용 C/C++ 타깃 실행파일을 컴파일하고 디버깅하는 소프트웨어 개발 도구 집합.
- **바이너리 호환 대상(Binary Compatibility Target)**: 빌드된 실행 파일이 대상 칩셋에서 오류 없이 실행되도록 약속된 프로파일 및 확장 범위.

</details>

```text
[ RISC-V Architecture Hierarchy ]
┌───────────────────────────────────────────────────────────┐
│  ISA Profile (e.g., RVA22: RV64GC + Vector Extensions)    │
├───────────────────────────────┬───────────────────────────┤
│  Base ISA (RV32I / RV64I)     │  Extensions (M, A, F, D, V)│
├───────────────────────────────┴───────────────────────────┤
│  Privileged Architecture (M-Mode / S-Mode / U-Mode CSRs)  │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 기본 ISA | **XLEN•정수 연산**의 공통 실행 계약 규정 |
| 확장 집합 | **M•F•V•사용자 정의 명령** 선택 추가 |
| 권한 아키텍처 | **M•S•U 모드•CSR**와 예외 처리 규정 |
| ISA 프로파일 | 필수 확장 조합으로 **바이너리 호환 대상** 고정 |

#### 한줄 요약
- Base ISA와 모듈형 Extension, Privileged Architecture 규격을 바탕으로 표준 ISA Profile을 고정하여 바이너리 호환성을 보장함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **레지스터 전송 수준(Register Transfer Level, RTL)**: Verilog, VHDL, Chisel 등으로 프로세서 내 동기식 플립플롭과 조합 논리 회로 동작을 정의하는 로직 설계 모델.
- **적합성 시험(Conformance Test / Architectural Compliance Test)**: 구현된 RISC-V 코어가 RISC-V International의 표준 명령어 및 특권 사양을 완벽히 충족하는지 검증하는 테스트 스위트.
- **인코딩 계약(Encoding Contract)**: Op-code 필드 비트 패턴과 커스텀 명령어 할당 영역의 상호 중복 방지 규약.
- **예외 시험(Exception Test)**: 0 나누기, 메모리 보호 위반 등 예외 발생 시 CSR 레지스터가 표준 규격대로 트랩(Trap)을 처리하는지 검증.
- **권한 시험(Privilege Test)**: U-mode에서 M-mode 시스템 레지스터 접근 시 정해진 하드웨어 예외를 발생시키는지 검증.

</details>

```text
1. 목표 프로파일·확장 선택 (RV64GC, Custom Ext)
             │
             ▼
       2. 코어 RTL 구현 (Verilog / Chisel)
             │
             ▼
3. 적합성 검증 코드 생성 (Compliance & Exception Test)
             │
             ▼
       4. 적합성 시험 (Architectural Compliance Test)
             ├─ 불일치: RTL 논리 오류 수정 후 재검증
             └─ 통과  : RISC-V Trademark 통과 및 툴체인 적용
```

### 동작 원리

1. **목표 프로파일·확장 선택**: 대상 SoC의 성능 목적에 맞추어 XLEN과 필수 확장 및 커스텀 오퍼코드 비트 영역을 정의함.
2. **코어 RTL 구현**: 선택된 사양서에 의거하여 **레지스터 전송 수준(RTL)** 회로(Verilog, Chisel 등)를 설계함.
3. **적합성 검증 코드 생성**: 표준 **인코딩 계약**에 따른 기계어와 **예외•권한 시험** 코드를 생성함.
4. **적합성 시험**: 실제 RTL 에뮬레이션 결과를 공식 **적합성 시험(Compliance Test)** 기대값과 차등 비교하여 ISA 미준수 오류를 사전에 제거함.

#### 한줄 요약
- 목표 프로파일 선정 -> RTL 코어 설계 -> Architectural Compliance Test 기반 규격 검증의 순서로 코어 개발을 완결함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **코어 지식재산권(Intellectual Property, IP)**: 이미 설계 및 검증이 완료되어 SoC 합성에 즉시 사용 가능한 프로세서 블록(예: ARM Cortex Core).
- **Arm**: 독점적 ISA 권한을 바탕으로 검증된 상용 IP 라이선싱 체계를 제공하는 대표적 칩 아키텍처 비즈니스 모델.
- **확장 파편화(Extension Fragmentation)**: 각 개발사가 각기 다른 사용자 정의 명령어를 추가함에 따라 소프트웨어 바이너리가 서로 호환되지 않고 갈라지는 현상.
- **라이선스 ISA(Licensed ISA)**: 사용료(Royalty 및 License Fee) 지불 계약 없이는 사양 변경이나 하드웨어 코어 제조가 엄격히 금지되는 아키텍처.
- **명령 확장 제약(Extension Restriction)**: 독점 권한 소유자의 인가를 받지 않고는 아키텍처에 사용자가 임의의 전용 명령어를 추가할 수 없게 막는 라이선스 제약.

</details>

| 비교 항목 | RISC-V (Open Standard ISA) | Arm (Commercial Licensed ISA) |
|:---|:---|:---|
| **라이선스 모델** | 로열티 무료, **개방형 ISA 규격(Open ISA)** | 고가의 라이선스 비용 및 칩당 로열티 부과 (**라이선스 ISA**) |
| **명령어 확장성** | **사용자 정의 확장(Custom Extension)** 무제한 추가 가능 | **명령 확장 제약** 존재 (Arm Custom Instructions 일부만 제한 제공) |
| **구현 주체** | 독자 칩 개발사, 오픈소스 커뮤니티, 상용 코어 벤더 | Arm Ltd. 개발 **코어 IP(Cortex)** 위주의 검증 칩 사용 |
| **생태계 위험 요소** | 무분별한 커스텀 확장으로 인한 **확장 파편화** | 라이선싱 비용 상승 및 수출 통제 등 공급망 종속 위험 |

#### 한줄 요약
- RISC-V는 커스텀 확장 자율성과 비용 절감 효과를 제공하며 Arm 코어 IP는 검증된 안정성과 정교한 소프트웨어 생태계를 제공함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **응용 프로그램 이진 인터페이스(Application Binary Interface, ABI)**: 함수 호출 규칙, 레지스터 사용 약속, 스택 프레임 구조를 정의하여 소프트웨어 바이너리 간 결합을 보장하는 상호작용 규격.
- **차등 테스트(Differential Testing)**: Golden Reference 소프트웨어 시뮬레이터(Spike, QEMU 등)와 설계한 RTL의 레지스터 변화를 클록 단위로 상호 비교하는 검증 기법.
- **기능 탐지(Feature Detection)**: 소프트웨어가 런타임에 칩의 CSR 레지스터를 조회하여 벡터 확장(V)이나 부동소수점 확장 지원 여부를 동적으로 판별하는 기법.
- **예약 인코딩(Reserved Encoding)**: RISC-V International 표준에서 향후 표준 확장을 위해 남겨둔 인코딩 공간으로, 커스텀 확장 구현 시 이 공간과의 충돌을 피해야 함.
- **성숙도(Maturity)**: 컴파일러(GCC/Clang) 지원 체계, OS 커널 메인라인 반영 여부 등 소프트웨어 생태계의 안정성 지표.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 각 파운드리 및 벤더별 모듈 확장 난립에 따른 소프트웨어 **확장 파편화** | 표준 **ISA 프로파일(RVA22 등)** 준수, **ABI** 고정 및 런타임 **기능 탐지** 적용 | 단일 실행 파일의 범용 멀티코어 칩간 바이너리 호환성 유지 |
| 커스텀 명령어가 향후 RISC-V 표준 **예약 인코딩(Reserved Encoding)**과 충돌 | 커스텀 전용 Op-code 영역(custom-0, custom-1 등) 엄격 활용 | 표준 확장 업데이트 시에도 커스텀 하드웨어 회로 안전성 확보 |
| 오프닝 ISA 특성상 구현된 코어의 기계어 처리 오작동 및 예외 누수 | Golden Simulator 기반 **차등 테스트(Differential Testing)** 및 표준 **적합성 시험** 필수 통과 | 미세 칩 물리 제작 전 RTL 논리 오류 전수 발굴 및 칩 리비전 비용 방지 |
| 최신 확장에 대한 컴파일러 툴체인 및 OS 지원 **성숙도(Maturity)** 부족 | Upstream 메인라인(GCC, Linux Kernel) 반영 확인 및 LLVM 백엔드 직접 유지보수 | 개발 코드 빌드 실패 및 OS 부팅 불능 문제 사전 차단 |

#### 한줄 요약
- ISA Profile 및 ABI 표준화, Differential Testing 검증, Reserved Encoding 준수를 통해 RISC-V 파편화 및 하드웨어 오작동을 예방함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Arm IP**: Arm 사가 완제품으로 제공하는 검증된 프로세서 물리 회로 설계 블록.
- **구현 방식 선택 기준(Implementation Decision Criteria)**: 전용 연산자 추가 필요성, 자체 RTL 검증 능력, 칩 출시 타임투마켓, 총 소요 비용을 종합 평가하는 결정 프레임워크.

</details>

- 자체 RTL 검증 역량과 전용 명령이 있으면 **RISC-V**, 출시 기간•검증 IP가 우선이면 **Arm IP** 선택

#### 한줄 요약
- 전용 명령과 자체 검증 역량은 RISC-V, 출시 기간과 검증된 생태계는 Arm IP를 선택한다.
