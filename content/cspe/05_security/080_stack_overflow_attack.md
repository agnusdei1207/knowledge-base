---
title: "스택 오버플로우 공격 (Stack Overflow Attack)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 80
---

# 📖 【암기용】 개념 완전 이해

> 목적: 스택 오버플로우 공격을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 스택 버퍼 경계를 초과해 반환주소나 제어 데이터를 덮어 실행 흐름을 탈취하는 공격
- **왜 필요한가**: C/C++ 네이티브 코드, 드라이버, 임베디드, 시스템 데몬은 메모리 경계 검사가 누락되면 RCE와 권한 상승으로 이어짐.
- **핵심 직관**: 서류함 한 칸에 넣을 수 있는 분량을 넘겨 밀어 넣어 옆 칸의 지시서까지 바꾸는 공격임.

## 깊이 이해
- **배경·문제의식**: 함수 호출 시 스택에는 지역변수, saved frame pointer, return address가 저장된다. 크기 제한 없는 `strcpy`, `gets`, `sprintf` 등이 버퍼보다 긴 입력을 복사하면 인접 메모리를 덮는다.
- **작동 원리**: 공격자는 입력 길이와 offset을 맞춰 return address를 shellcode, ROP gadget, libc 함수 주소로 바꾼다. 방어는 stack canary, DEP/NX, ASLR, PIE, CFI, safe language로 수행함.
- **비유**: 택배 주소칸을 넘치게 써서 배송지 라벨의 목적지를 바꾸는 것과 같다. 시스템은 정상 절차로 복귀한다고 믿지만 조작된 주소로 이동함.
- **구체 예시**: 64바이트 stack buffer에 80바이트 입력이 들어가면 64바이트 이후 canary, saved RBP, return address 영역이 덮일 수 있다. canary 검증 실패 시 프로세스를 종료함.
- **흔한 오해·주의점**: DEP/NX만 있으면 끝나는 것이 아니다. ROP는 실행 불가 스택을 우회해 기존 코드 조각을 연결하므로 ASLR, CFI, bounds check가 함께 필요함.

## 연결 개념
- Buffer Overflow - 스택·힙·정적 영역 경계 초과 취약점의 상위 개념
- ROP - 실행 불가 스택을 우회하는 코드 재사용 공격
- Secure Coding - bounds check, safe API, Rust/Go 같은 메모리 안전 언어 적용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 스택 오버플로우 답안은 공격 절차보다 stack frame, return address overwrite, 보호기법, 컴파일·런타임 검증을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Stack Overflow Attack은 스택 버퍼 경계를 초과해 return address, saved frame pointer, canary 등 제어 데이터를 변조하는 메모리 공격임.
> 2. **가치**: stack canary, DEP/NX, ASLR, PIE, CFI, safe language로 코드 실행과 제어 흐름 탈취를 차단함.
> 3. **판단 포인트**: 입력 검증, 안전 함수, 컴파일 옵션, 런타임 보호, fuzzing 지표를 SDLC에 연결해 써야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메모리 구조 이해 확인 | stack frame, local buffer, return address overwrite | 버퍼 초과 정의만 쓰고 스택 구조 누락 |
| 공격·방어 원리 확인 | shellcode, ROP, canary, DEP/NX, ASLR | 보호기법 이름만 나열 |
| 개발·운영 통제 확인 | safe API, compiler hardening, fuzzing, crash triage | 코드 수정과 CI 검증 연결 누락 |

> 요약: 이 문제는 공격 원리 암기보다 메모리 배치, 제어 흐름 변조, 보호기법과 검증 지표를 연결하는 능력을 묻는다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 스택 버퍼 경계를 초과해 반환주소나 제어 데이터를 덮어 실행 흐름을 탈취하는 공격 | "핵심 기술 요소" |
| **왜 필요한가** | C/C++ 네이티브 코드, 드라이버, 임베디드, 시스템 데몬은 메모리 경계 검사가 누락되면 RCE와 권한 상승으로 이어짐 | "핵심 기술 요소" |
| **핵심 직관** | 서류함 한 칸에 넣을 수 있는 분량을 넘겨 밀어 넣어 옆 칸의 지시서까지 바꾸는 공격임 | "핵심 기술 요소" |
| **배경·문제의식** | 함수 호출 시 스택에는 지역변수, saved frame pointer, return address가 저장된다 | "칠판" |
| **작동 원리** | 공격자는 입력 길이와 offset을 맞춰 return address를 shellcode, ROP gadget, libc 함수 주소로 바꾼다 | "재해 복구" |
| **비유** | 택배 주소칸을 넘치게 써서 배송지 라벨의 목적지를 바꾸는 것과 같다 | "핵심 기술 요소" |
| **구체 예시** | 64바이트 stack buffer에 80바이트 입력이 들어가면 64바이트 이후 canary, saved RBP, return address... | "완충 지대" |

---


## Ⅰ. 개요 및 필요성

- 개요: 스택 제어 흐름 변조 공격
- 배경: 입력 길이 검증이 없는 C/C++ 코드에서 지역 버퍼를 초과해 쓰면 return address와 saved frame pointer가 공격자 값으로 변조될 수 있음.
- 필요성: CERT C, CWE-121, stack canary, ASLR, NX, bounds checking을 빌드·테스트 기준에 포함해 시스템 SW와 드라이버의 RCE를 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
함수 호출 -> stack frame 생성 -> local buffer 저장 -> 과다 입력 복사 -> canary/return address 변조
  / saved RBP, return address, arguments
  / shellcode, ROP, ret2libc
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Stack Frame | 함수 호출 상태 저장 | local variable, saved RBP, return address |
| Vulnerable Buffer | 경계 검사가 없는 입력 저장소 | gets, strcpy, sprintf, scanf %s |
| Control Data | 복귀 주소와 제어 흐름 결정 | overwrite 시 shellcode/ROP 이동 |
| Mitigation | 공격 성공 조건 제거 | canary, DEP/NX, ASLR, CFI, bounds check |

> 요약: 스택 오버플로우는 버퍼 초과가 제어 데이터 변조로 이어질 때 실행 흐름 탈취가 발생함.

---

## Ⅲ. 동작원리 및 흐름도

```text
입력 수신 -> 길이 검증 누락 -> stack buffer 초과 기록
  / canary 손상 또는 return address overwrite
함수 반환 -> 조작 주소 이동 시도 -> 보호기법 검증 -> 차단/침해
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 외부 입력이 고정 크기 stack buffer로 복사 | bounds check 존재 |
| 2 | 입력 길이가 buffer 크기를 초과해 인접 영역 덮음 | ASan crash 재현 |
| 3 | return address가 shellcode, ROP gadget, libc 주소로 변경 | canary, CFI 탐지 |
| 4 | DEP/NX, ASLR, PIE가 실행·주소 예측을 제한 | hardening option 100% |

> 요약: 공격은 길이 검증 누락에서 시작해 return address overwrite로 이어지고, canary와 DEP/NX, ASLR이 성공 조건을 제한함.

---

## Ⅳ. 특징

| 구분 | 취약 구현 | 보호 적용 구현 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 입력 처리 | strcpy, gets, sprintf | strncpy, snprintf, bounds check | unsafe API 0건 |
| 실행 보호 | executable stack | DEP/NX, W^X | NX enabled 100% |
| 주소 예측 | 고정 주소 | ASLR, PIE | PIE binary 100% |
| 검증 | 수동 테스트 | ASan, fuzzing, SAST | crash triage 24시간 |

> 요약: 스택 오버플로우 방어는 안전 함수와 메모리 보호 옵션, fuzzing 검증을 함께 적용해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | C/C++ 경계 수동관리 | safe API, Rust/Go, memory sanitizer | 신규 모듈은 safe language 우선 |
| 비용/성능 | 보호 옵션 off | canary, PIE, RELRO, ASLR | latency 영향보다 RCE 위험이 큰 서비스 |
| 운영/위험 | 릴리스 후 crash 대응 | fuzzing, SAST, ASan CI | 외부 입력 parser, protocol handler |

> 요약: 외부 입력을 처리하는 네이티브 모듈은 성능보다 메모리 보호 옵션과 fuzzing 검증을 우선 적용해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| RCE | return address overwrite | canary, DEP/NX, ASLR, CFI | exploit 재현 0건 |
| 보호 우회 | ROP, ret2libc | PIE, full RELRO, shadow stack | ROP gadget exploit 차단 |
| 회귀 취약점 | unsafe API 재도입 | SAST rule, code review, CI fail | unsafe API 0건 |

> 요약: RCE, 보호 우회, 회귀는 컴파일 옵션과 SAST·fuzzing을 배포 게이트로 걸어 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 하드닝 | canary, NX, PIE, RELRO 100% | checksec, compiler flags |
| 결함 탐지 | fuzzing 24시간 run, crash 0건 | libFuzzer, AFL++, ASan |
| 코드 품질 | unsafe API 0건 | SAST, Semgrep, CodeQL |

> 요약: 성공 여부는 binary hardening 적용률, fuzzing crash, unsafe API 검출 결과로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 개발 통제: `gets`, `strcpy`, `sprintf` 사용을 SAST로 차단하고 `snprintf`, bounds check, length-prefixed protocol을 coding standard에 반영함.
2. 빌드 하드닝: `-fstack-protector-strong`, PIE, full RELRO, DEP/NX, ASLR, CFI를 기본 옵션으로 두고 checksec 결과를 release gate에 연결함.
3. 검증 운영: 외부 입력 parser는 ASan/UBSan과 libFuzzer/AFL++를 CI에서 수행하고 crash는 24시간 내 triage, 재현 exploit 0건을 종료 기준으로 둠.

**결론 (2줄):**
- 기술사 판단: 신규 외부 입력 모듈은 Rust/Go 등 메모리 안전 언어를 우선 적용하고, 레거시 C/C++는 하드닝·fuzzing·SAST를 필수 게이트로 둠.
- 향후 방향: 스택 오버플로우 대응은 canary 중심에서 CFI, shadow stack, memory-safe rewrite로 이동해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "스택 오버플로우를 설명하시오" | stack frame, return address overwrite, 보호기법 흐름 | 취약 구현과 보호 구현 차이 |
| 요구사항 명시형 | "방어 방안을 제시하시오", "보안 코딩을 설계하시오" | safe API, compiler hardening, fuzzing 절차 | canary, DEP/NX, ASLR, safe language 선택 기준 |

> 요약: 설명형은 메모리 구조와 공격 흐름을, 방안형은 컴파일·런타임·SDLC 통제를 중심으로 구성함.
