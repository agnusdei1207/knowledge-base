---
title: "버퍼 오버플로우 - 카나리·DEP·ASLR (Buffer Overflow Canary DEP ASLR)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 81
---

# 📖 【암기용】 개념 완전 이해

> 목적: 버퍼 오버플로우와 카나리·DEP·ASLR 방어를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 버퍼 경계 초과로 제어 데이터를 덮는 공격과 이를 막는 대표 런타임 보호기법
- **왜 필요한가**: C/C++ 기반 서버, 드라이버, IoT 펌웨어는 경계 검사 누락 1건이 RCE, 권한 상승, 서비스 중단으로 이어질 수 있음.
- **핵심 직관**: 공격자는 주소를 덮고, 방어자는 덮임 탐지, 실행 차단, 주소 예측 차단을 겹쳐 성공 조건을 줄임.

## 깊이 이해
- **배경·문제의식**: 버퍼 오버플로우는 stack, heap, global 영역에서 모두 발생한다. stack은 return address, heap은 chunk metadata와 함수 포인터, global은 전역 포인터 변조가 주요 표적임.
- **작동 원리**: Canary는 return address 앞의 임의 값을 검사하고, DEP/NX는 데이터 영역 실행을 차단하며, ASLR은 stack, heap, libc, mmap base 주소를 난수화한다. PIE는 실행 파일 코드 주소까지 ASLR 범위에 넣고, RELRO는 GOT overwrite를 제한함.
- **비유**: 금고 앞에 봉인 스티커(canary), 금고 안 문서 실행 금지(DEP/NX), 매일 바뀌는 금고 위치(ASLR)를 동시에 두는 구조임.
- **구체 예시**: 64바이트 stack buffer에 96바이트 입력이 복사되면 canary 8바이트와 saved RBP, return address가 덮일 수 있다. canary 불일치 시 `__stack_chk_fail`로 종료함.
- **흔한 오해·주의점**: ASLR만으로는 충분하지 않다. 정보 누출 1건으로 libc 주소가 노출되면 ret2libc와 ROP가 가능하므로 PIE, full RELRO, CFI, leak 차단이 함께 필요함.

## 연결 개념
- Shellcode·ROP - DEP/NX 우회와 코드 재사용 공격
- Format String Attack - stack read/write로 canary와 주소를 노출하는 경로
- Secure Coding Guide - safe API, compiler flag, fuzzing을 SDLC에 넣는 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 보호기법 이름 나열이 아니라 stack/heap 공격면, 보호기법 한계, 컴파일·런타임·검증 지표를 연결함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Buffer Overflow는 경계 초과 쓰기로 return address, 함수 포인터, heap metadata 등 제어 데이터를 변조하는 메모리 취약점임.
> 2. **가치**: Canary, DEP/NX, ASLR, PIE, RELRO는 각각 덮임 탐지, 데이터 실행 차단, 주소 예측 차단, GOT 변조 제한을 담당함.
> 3. **판단 포인트**: 보호기법은 단독 적용보다 safe API, compiler hardening, ASan/fuzzing, 정보 누출 차단과 묶어야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메모리 공격 구조 이해 확인 | stack/heap/global, return address, function pointer, heap metadata | stack만 설명하고 heap overflow 누락 |
| 보호기법별 역할 구분 확인 | canary, DEP/NX, ASLR, PIE, RELRO, CFI | 보호기법을 이름만 나열 |
| 우회와 검증 역량 확인 | info leak, ROP, ret2libc, ASan, fuzzing, checksec | ASLR을 완전 차단책으로 단정 |

> 요약: 이 문제는 공격면별 제어 데이터 변조와 보호기법의 한계를 SDLC 검증까지 연결하는 판단을 요구함.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **버퍼 오버플로우 - 카나리·DEP·ASLR** | 버퍼 오버플로우 - 카나리·DEP·ASLR (Buffer Overflow Canary DEP ASLR)의 핵심 개념 | 이 주제의 본질 |

---

## Ⅰ. 개요 및 필요성

- 개요: 메모리 경계 초과 쓰기 공격
- 배경: 입력 검증이 없는 C/C++ 코드에서 stack, heap, global 영역의 제어 데이터가 변조되면 RCE와 권한 상승이 발생할 수 있음.
- 필요성: CWE-120, stack canary, DEP/NX, ASLR, PIE, RELRO 적용 여부를 빌드 산출물 기준으로 점검해 공격 성공 조건을 단계별로 줄여야 함.

---

## Ⅱ. 구조 및 구성요소

```text
외부 입력 -> 고정 버퍼 -> 경계 초과 쓰기 -> 제어 데이터 변조 -> 코드 실행 시도
  / Canary: 덮임 탐지
  / DEP/NX: 데이터 영역 실행 차단
  / ASLR/PIE/RELRO: 주소 예측과 GOT 변조 제한
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 취약 버퍼 | 입력 저장 영역 | stack buffer, heap chunk, global array |
| 제어 데이터 | 실행 흐름 결정 | return address, function pointer, vtable, GOT |
| Canary | return address 앞 무결성 값 | 불일치 시 프로세스 종료 |
| DEP/NX | 데이터 페이지 실행 금지 | shellcode 실행 차단, ROP는 별도 통제 필요 |
| ASLR/PIE/RELRO | 주소 난수화와 GOT 보호 | 정보 누출 차단과 함께 적용 필요 |

> 요약: 버퍼 오버플로우 방어는 덮임 탐지, 실행 차단, 주소 예측 차단, 쓰기 대상 제한을 층으로 배치함.

---

## Ⅲ. 동작원리 및 흐름도

```text
입력 수신 -> bounds check 누락 -> buffer overflow 발생
  / stack: canary, saved RBP, return address 손상
  / heap: metadata, function pointer, vtable 손상
보호기법 검사 -> 종료/차단/우회 시도 -> 로그와 crash triage
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 외부 입력이 고정 길이 버퍼로 복사 | 길이 검사, safe API 존재 |
| 2 | 인접 제어 데이터 덮임 | ASan/UBSan 재현 |
| 3 | 함수 반환 또는 간접 호출 시 공격 주소 사용 | canary, CFI, NX 검사 |
| 4 | ASLR 우회에 정보 누출 필요 | leak test, PIE 적용률 |
| 5 | crash와 exploit 가능성 분류 | 24시간 triage, CVSS 산정 |

> 요약: 공격은 경계 초과 쓰기에서 시작하고 보호기법은 반환·실행·주소 해석 시점에 공격 조건을 차단함.

---

## Ⅳ. 특징

| 구분 | 취약 상태 | 보호 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 메모리 구조 | stack/heap 경계 수동 관리 | bounds check, safe container | unsafe API 0건 |
| 실행 통제 | stack shellcode 실행 가능 | DEP/NX, W^X | NX enabled 100% |
| 주소 통제 | 고정 binary/libc 주소 | ASLR, PIE | PIE 적용률 100% |
| 쓰기 통제 | GOT overwrite 가능 | full RELRO | full RELRO 100% |
| 검증 | 수동 기능 테스트 | ASan, fuzzing, SAST | crash 0건, high finding 0건 |

> 요약: 보호기법은 canary, DEP/NX, ASLR, PIE, RELRO를 동시에 적용하고 검증 지표로 통과 여부를 판단함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | safe language 전환 | C/C++ hardening | 레거시 ABI와 성능 제약 존재 시 hardening |
| 비용/성능 | 보호 옵션 off | stack protector, PIE, RELRO, CFI | 외부 입력 parser, daemon, setuid binary |
| 운영/위험 | 장애 후 분석 | pre-release fuzzing, crash gate | RCE 가능 CVSS 9.0 이상 경로 |

> 요약: 레거시 네이티브 코드는 언어 전환 가능성을 보되, 배포 전 하드닝과 fuzzing을 필수 게이트로 둠.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| RCE | return address, function pointer overwrite | canary, DEP/NX, CFI, shadow stack | exploit PoC 재현 0건 |
| 보호 우회 | info leak 기반 ASLR 우회 | leak sanitization, PIE, full RELRO | 주소 노출 로그 0건 |
| 회귀 | unsafe API 재도입 | CERT C, SAST rule, code review | unsafe API 0건 |

> 요약: 주요 리스크는 제어 흐름 변조, 주소 누출, 회귀이며 컴파일 옵션과 CI 검증으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 빌드 하드닝 | canary, NX, PIE, full RELRO 100% | checksec, compiler flag audit |
| 결함 탐지 | fuzzing 24시간 crash 0건 | libFuzzer, AFL++, ASan |
| 코드 품질 | critical/high SAST finding 0건 | CodeQL, Semgrep, CERT C rule |

> 요약: 성공 여부는 hardening 적용률, fuzzing crash, SAST high finding을 릴리스 기준으로 측정함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 컴파일 통제: `-fstack-protector-strong`, PIE, full RELRO, NX, CFI를 기본값으로 두고 checksec 미통과 binary는 배포 차단함.
2. 코드 통제: `strcpy`, `gets`, `sprintf`를 SAST 금지 API로 등록하고 `snprintf`, span, bounds-checked container를 적용함.
3. 검증 통제: 외부 입력 parser는 ASan/UBSan과 libFuzzer/AFL++ 24시간 실행, crash 0건과 high finding 0건을 release gate로 설정함.

**결론 (2줄):**
- 기술사 판단: 신규 모듈은 Rust/Go 등 메모리 안전 언어를 우선 검토하고, 레거시 C/C++는 canary, DEP/NX, ASLR, PIE, RELRO를 기본 통제로 둠.
- 향후 방향: 보호 중심 대응은 CFI, shadow stack, memory tagging, memory-safe rewrite로 확장해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "버퍼 오버플로우를 설명하시오", "기술하시오" | stack/heap 흐름, canary/DEP/ASLR 동작 | 보호기법별 역할과 한계 |
| 요구사항 명시형 | "방어 방안을 제시하시오", "비교하시오", "설계하시오" | compiler hardening, safe API, fuzzing 절차 | PIE, RELRO, CFI, shadow stack 선택 기준 |

> 요약: 설명형은 공격 구조와 보호기법을, 방안형은 하드닝 옵션과 SDLC 검증 지표를 중심으로 전개함.
