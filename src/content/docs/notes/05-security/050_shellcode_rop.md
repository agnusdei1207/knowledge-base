---
sidebar:
  order: 50
  label: "050. 쉘코드•ROP 공격 (Shellcode ROP)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "쉘코드•ROP 공격 (Shellcode ROP)"
date: "2026-08-13T19:36:00+09:00"
tags:
  - "notes-security"
weight: 50
extra:
  question_no: "050"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "125회 기출이며 메모리 방어 우회 비교로 보존함"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **쉘코드(Shellcode)**: 취약점 익스플로잇 성공 시 대상 시스템 상에서 명령 쉘(Command Shell) 획득 또는 임의 코드를 실행하기 위해 삽입하는 기계어 어셈블리 명령 조각.
- **반환 지향 프로그래밍(Return-Oriented Programming, ROP)**: DEP/NX 메모리 보호를 우회하기 위해 바이너리 내부의 기존 명령 조각(Gadget)들과 ret 연산자를 체이닝하여 임의 코드 실행을 달성하는 제어 흐름 탈취 공격.

</details>

- 정의/개념: 주입 코드나 기존 가젯으로 제어권을 탈취하는 **메모리 공격**
- 배경/필요성: NX만으로는 **ROP 코드 재사용** 차단 불가

#### 한줄 요약

- 외부 악성 기계어 코드 직접 실행(쉘코드)과 기존 바이너리 가젯 재사용(ROP)을 무력화하도록 하드웨어/OS 레벨의 제어 흐름 보호를 연계함.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **제어 데이터(Control Data)**: 스택 반환 주소(RET), 함수 포인터, VTable 주소 등 프로그램 실행 제어 흐름을 결정하는 핵심 지점.
- **실행 불가(No-eXecute, NX / DEP)**: 데이터 스택/힙 영역에 코드 실행 권한을 배제하는 메모리 보호 기법.
- **주소 공간 배치 무작위화(Address Space Layout Randomization, ASLR)**: 메모리 주소를 임의 난수화하여 ROP 가젯 위치 추정을 차단하는 기술.
- **제어 흐름 무결성(Control-Flow Integrity, CFI)**: 간접 분기 및 호출(Indirect Call/Jmp) 타깃이 허용된 제어 흐름 그래프(CFG) 범주 내에 존재하는지 실시간 검증하는 보호 기술.
- **그림자 스택(Shadow Stack)**: 함수 호출 시 반환 주소를 별도의 하드웨어 하이퍼바이저/격리 스택에 복사해 두고, ret 시 오염 여부를 상호 비교 대조하는 기술.

</details>

- 메모리 **제어 데이터(Control Data)** 오염을 통한 실행 제어권 탈취.
- **NX/DEP**로 쉘코드 주입을 차단하고 **ASLR**로 가젯 주소를 무작위화.
- **CFI** 및 **그림자 스택(Shadow Stack)**을 적용하여 정상적이지 않은 간접 분기 및 반환 주소 변조를 최종 검증.

#### 한줄 요약

- NX는 데이터 영역의 쉘코드 직접 집행을 막고, CFI 및 그림자 스택은 기존 코드 가젯 재사용 ROP를 무력화함.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **메모리 안전(Memory Safety)**: Bounds Checking 및 Type Safety를 통해 바운더리 밖 메모리 참조 및 수명 종료 객체 접근(Use-After-Free)을 막는 성질.
- **가젯(Gadget)**: ROP 공격에서 pop/ret 등으로 끝나는 2~3개 연산의 기존 기계어 코드 조각.

</details>

```text
제어 탈취 다층 방어
├─ 메모리 안전: 경계 밖 쓰기•수명 오류 방지
├─ NX•메모리 권한: 데이터 페이지 실행 금지
├─ ASLR: 코드•라이브러리 주소 무작위화
├─ CFI: 간접 분기•호출 대상 제한
└─ 그림자 스택: 반환 주소 사본 대조
```

| 구성요소 | 책임 |
|:---|:---|
| 메모리 안전 | Rust/Go 적용 또는 **메모리 안전** 경계 검사로 1차 결함 제거 |
| NX•메모리 권한 | 스택/힙 데이터 영역의 코드 실행을 **NX**로 원천 차단 |
| ASLR | 프로세스 메모리 배치 무작위화(**ASLR**)로 가젯 배치 은닉 |
| CFI | 간접 호출/분기 시 허용된 타깃 주소인지 **CFI**로 통제 |
| 그림자 스택 | 복사된 하드웨어 **그림자 스택** 대조로 RET 덮어쓰기 탐지 |

#### 한줄 요약

- 메모리 안전 시큐어 코딩, NX 실행 금지, ASLR 메모리 무작위화, CFI 및 그림자 스택 제어 검증을 유기 결합함.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **코드 주입(Code Injection)**: 비신뢰 데이터를 프로세스 메모리에 주입 후 쉘코드로 실행시키는 기법.
- **흐름 검증(Control Flow Validation)**: 하드웨어 또는 컴파일러 레벨에서 간접 분기 및 반환 주소의 정당성을 체크하는 단계.
- **손상된 제어 데이터(Corrupted Control Data)**: 스택 프레임 반환 주소가 오염된 상태.
- **실행 페이지 속성 확인(Page Permission Check)**: 해당 메모리 페이지의 NX 속성을 체크하는 단계.
- **NX 판정(NX Decision)**: 해당 주소의 실행 가능 여부를 판정하는 단계.
- **분기•반환 대상 확인(Target Verification)**: ROP 가젯 주소의 허용 유무를 체크하는 단계.
- **CFI•그림자 스택 판정(CFI & Shadow Stack Check)**: 정상적인 CFG 흐름 및 스택 반환값 무결성을 최종 판정하는 단계.

</details>

```text
경계 초과 입력
      │
      ▼
1. 손상된 제어 데이터
      │
      ▼
2. 실행 페이지 속성 확인
      │
      ▼
3. NX 판정
      │
      ├─ 실행 불가 ── 쉘코드 차단
      │
      └─ 실행 가능 ── 4. 분기•반환 대상 확인
                              │
                              ▼
                    5. CFI•그림자 스택 판정
                              │
                  ┌───────────┴───────────┐
                  │                       │
             불일치 차단             허용 흐름 실행
```

### 동작 원리

1. **손상된 제어 데이터**: 버퍼 오버플로우로 인해 반환 주소 및 함수 포인터 변조.
2. **실행 페이지 속성 확인**: 해당 주소 영역의 메모리 권한 속성 스캔.
3. **NX 판정**: 스택/힙 데이터 영역일 경우 쉘코드 직접 실행 1차 차단.
4. **분기•반환 대상 확인**: ROP 가젯 재사용 시 간접 분기(Call/Jmp) 및 Ret 타깃 주소 추출.
5. **CFI•그림자 스택 판정**: 하드웨어 그림자 스택 및 CFG 경로 비교 후 불일치 시 프로세스 종료.

#### 한줄 요약

- 외부 악성 기계어 주입(쉘코드)은 NX 판정으로 억제하고, 기존 코드 재사용 체이닝(ROP)은 CFI 및 그림자 스택으로 차단함.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **제어 탈취 방어 선택 기준(Control Hijacking Defense Criteria)**: 외부 기계어 주입에는 NX/DEP, 내부 정상 바이너리 조각 재사용 ROP에는 CFI 및 Hardware-enforced Shadow Stack을 맞춤 적용하는 지침.

</details>

| 제어 탈취 유형 | 쉘코드 주입 | ROP |
|:---|:---|:---|
| 적용 기준 | 데이터 페이지 실행 가능 | NX 환경의 제어 흐름 손상 |
| 핵심 특징 | **쉘코드** 주입•실행 | **ROP**의 기존 가젯 연결•재사용 |
| 한계 | 악성 명령 직접 실행 | 정상 코드 기반 탐지•차단 곤란 |

#### 한줄 요약

- 코드 직접 주입형 쉘코드는 NX 속성으로 방어하고, 정상 라이브러리 가젯 연결 ROP는 CFI 및 그림자 스택으로 방어함.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **MITRE CWE-787**: 메모리 버퍼 영역 외부에 쓰는 결함으로 제어 데이터 오염의 근본 원인.
- **인텔 제어 흐름 강제 기술(Intel CET / Control-flow Enforcement Technology)**: 인텔 11세대 이후 CPU 하드웨어에 탑재된 IBT(간접 분기 추적) 및 Shadow Stack 기능.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 버퍼 오버플로우로 인한 제어 데이터 손상 | **MITRE CWE-787** 가이드 준수 원인 결함 제거 | 쉘코드 및 ROP 익스플로잇 전제 조건 무력화 |
| ROP 체이닝을 통한 NX 방어 우회 | **Intel CET/CFI** 및 하드웨어 Shadow Stack 도입 | 가젯 연결 및 RET 변조 시 하드웨어 단위 트랩 발생 |
| 바이너리 하드닝 파이프라인 누락 | CI/CD 시 바이너리 Checksec 자동 스캔 및 **NX/ASLR** 전면 적용 | 스택/힙 코드 실행 및 메모리 주소 예측 차단 |

#### 한줄 요약

- 메모리 경계 검사를 시큐어 코딩에 적용하고, 빌드 바이너리에 NX, ASLR, Intel CET 하드웨어 검증을 필수 적용함.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **공격 경로별 실행 보호(Path-based Execution Protection)**: 직접 쉘코드 주입에는 NX, 주소 가젯 추정에는 ASLR, ROP 가젯 체이닝에는 CFI와 Shadow Stack을 결합하는 심층 방어 모델.

</details>

- **공격 경로별 실행 보호** 모델을 정립하여 쉘코드 주입은 **NX**, 주소 예측은 **ASLR**, ROP 가젯 재사용은 **CFI** 및 **그림자 스택(Shadow Stack)**으로 다층 억제.

#### 한줄 요약

- 주입 코드는 **NX**, 주소는 **ASLR**, ROP는 CFI로 차단
