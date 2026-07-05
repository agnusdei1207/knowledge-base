---
title: "포맷 스트링 공격 (Format String Attack)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 83
---

# 📖 【암기용】 개념 완전 이해

> 목적: 포맷 스트링 공격을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사용자 입력을 `printf` 계열 format 문자열로 사용해 stack read/write와 메모리 변조를 유발하는 취약점
- **왜 필요한가**: `%x`, `%p`, `%s`는 메모리 노출을 만들고 `%n`은 메모리 쓰기를 수행해 ASLR 우회와 제어 흐름 변조로 이어짐.
- **핵심 직관**: 데이터를 출력해야 할 입력을 출력 명령서로 해석하면서 프로그램이 메모리 주소와 값을 공격자에게 보여주거나 써 줌.

## 깊이 이해
- **배경·문제의식**: `printf(user_input)`처럼 format 문자열을 외부 입력으로 받으면 함수는 인자 목록에 없는 값을 stack에서 읽는다. 공격자는 format specifier로 stack 값을 읽고, `%n`으로 출력 글자 수를 특정 주소에 기록할 수 있음.
- **작동 원리**: `%p`와 `%x`는 주소·값 누출, `%s`는 포인터 대상 문자열 읽기, `%n`은 메모리 쓰기다. 주소 누출은 ASLR 우회, 쓰기는 GOT·return address·함수 포인터 변조로 연결됨.
- **비유**: 손님이 주문서 칸에 "창고 주소를 읽고 금고 번호를 바꿔라"라는 작업 지시를 적었는데 직원이 이를 그대로 실행하는 상황임.
- **구체 예시**: `printf(argv[1])`에 `%p %p %p`가 들어가면 stack 값이 출력될 수 있다. 컴파일러는 `-Wformat-security`로 non-literal format 사용을 경고함.
- **흔한 오해·주의점**: 단순 정보 노출 취약점으로만 보면 안 된다. `%n`이 허용되면 제한적 write primitive가 생기고, RELRO 미적용 GOT overwrite와 결합될 수 있음.

## 연결 개념
- ASLR 우회 - format string 기반 주소 누출로 난수화 효과가 줄어듦
- RELRO - GOT overwrite를 제한하는 링커 보호기법
- Secure Coding - format literal 고정, compiler warning, SAST rule 적용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 포맷 지정자 기능, stack read/write, ASLR 우회, compiler warning과 secure coding 지표를 연결함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Format String Attack은 외부 입력이 format 문자열로 해석되어 stack read, arbitrary read, `%n` 기반 write를 만드는 취약점임.
> 2. **가치**: 주소 누출은 ASLR 우회, `%n` write는 GOT·함수 포인터 변조로 이어지므로 정보 노출과 메모리 변조를 함께 다뤄야 함.
> 3. **판단 포인트**: `printf("%s", input)` 패턴, `-Wformat-security`, `_FORTIFY_SOURCE`, full RELRO, SAST rule을 답안에 포함해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 취약 API 사용 패턴 확인 | `printf(user)`, `%x/%p/%s/%n` | XSS처럼 문자열 삽입 문제로만 설명 |
| 공격 영향 분석 확인 | stack read/write, ASLR leak, GOT overwrite | 정보 노출만 쓰고 `%n` write 누락 |
| 예방·검증 역량 확인 | format literal, compiler warning, RELRO, SAST | 컴파일 옵션과 코드 규칙 누락 |

> 요약: 이 문제는 format 문자열 해석이 메모리 읽기와 쓰기 primitive로 바뀌는 구조를 묻는다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 사용자 입력을 `printf` 계열 format 문자열로 사용해 stack read/write와 메모리 변조를 유발하는 취약점 | "접시 쌓기" |
| **왜 필요한가** | `%x`, `%p`, `%s`는 메모리 노출을 만들고 `%n`은 메모리 쓰기를 수행해 ASLR 우회와 제어 흐름 변조로 이어짐 | "핵심 기술 요소" |
| **핵심 직관** | 데이터를 출력해야 할 입력을 출력 명령서로 해석하면서 프로그램이 메모리 주소와 값을 공격자에게 보여주거나 써 줌 | "핵심 기술 요소" |
| **배경·문제의식** | `printf(user_input)`처럼 format 문자열을 외부 입력으로 받으면 함수는 인자 목록에 없는 값을 stack에서 읽는다 | "접시 쌓기" |
| **작동 원리** | `%p`와 `%x`는 주소·값 누출, `%s`는 포인터 대상 문자열 읽기, `%n`은 메모리 쓰기다 | "핵심 기술 요소" |
| **비유** | 손님이 주문서 칸에 "창고 주소를 읽고 금고 번호를 바꿔라"라는 작업 지시를 적었는데 직원이 이를 그대로 실행하는 상황임 | "핵심 기술 요소" |
| **구체 예시** | `printf(argv[1])`에 `%p %p %p`가 들어가면 stack 값이 출력될 수 있다 | "접시 쌓기" |

---


## Ⅰ. 개요 및 필요성

- 개요: format 문자열 해석 오류
- 배경: 외부 입력이 `printf` 계열 format 인자로 직접 전달되면 stack 값 노출, 주소 누출, `%n` 기반 메모리 쓰기가 발생할 수 있음.
- 필요성: CWE-134, CERT C FIO30-C, compiler warning, RELRO, format literal 규칙을 빌드와 코드리뷰 기준에 포함해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
사용자 입력 -> printf 계열 함수 -> format 문자열 해석 -> stack read/write
  / %x, %p: stack value, pointer leak
  / %s: pointer dereference read
  / %n: memory write
Mitigation -> literal format / warning / RELRO / SAST
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Format Function | 문자열 형식 해석 | printf, fprintf, snprintf, syslog |
| Format Specifier | 인자 읽기·쓰기 지시 | `%p`, `%x`, `%s`, `%n` |
| Stack/Memory | 잘못 읽히는 인자 영역 | canary, libc, return address leak 가능 |
| Mitigation | 해석 오류 차단 | literal format, `-Wformat-security`, RELRO |

> 요약: 사용자 입력이 format 명령으로 해석될 때 stack read와 `%n` write가 발생함.

---

## Ⅲ. 동작원리 및 흐름도

```text
입력 수신 -> printf(user_input) 호출 -> format specifier 해석
  / read: %p, %x, %s -> 주소와 값 노출
  / write: %n -> 지정 주소 값 변경
ASLR 우회 또는 GOT 변조 -> 보호기법 검증 -> 로그와 차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 외부 문자열이 format 인자로 전달 | non-literal format 0건 |
| 2 | `%p/%x/%s`가 stack과 메모리 값을 읽음 | secret/address leak test |
| 3 | `%n`이 출력 길이를 지정 주소에 기록 | `%n` 사용 0건 |
| 4 | 주소 누출로 ASLR 우회 조건 형성 | PIE, ASLR, leak 0건 |
| 5 | GOT·함수 포인터 쓰기 시도 차단 | full RELRO, CFI |

> 요약: 포맷 스트링 공격은 format 해석이 read primitive와 write primitive를 생성하면서 ASLR 우회와 제어 흐름 변조로 확장됨.

---

## Ⅳ. 특징

| 구분 | 취약 구현 | 보호 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 출력 호출 | `printf(user)` | `printf("%s", user)` | non-literal format 0건 |
| 정보 노출 | `%p`, `%x`, `%s` 허용 | pointer masking, log redaction | address leak 0건 |
| 메모리 쓰기 | `%n` 허용 | `%n` 금지, hardened libc | `%n` usage 0건 |
| 바이너리 보호 | partial RELRO | full RELRO, PIE | checksec pass 100% |

> 요약: 핵심 통제는 format literal 고정, `%n` 차단, 주소 노출 제거, full RELRO 적용임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 입력 문자열 그대로 출력 | literal format + escaped data | 로그·오류 메시지에 사용자 입력 포함 시 |
| 비용/성능 | warning 무시 | `-Wformat -Wformat-security -Werror` | C/C++ 빌드 파이프라인 |
| 운영/위험 | 주소 포함 로그 | redaction, secret scanning | prod log 외부 노출 가능 서비스 |

> 요약: format string 대응은 코드 수정과 compiler warning을 빌드 실패 조건으로 연결할 때 실효성이 생김.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| ASLR 우회 | `%p/%x` 주소 누출 | pointer masking, log redaction | address leak 0건 |
| 임의 쓰기 | `%n` 사용 가능 | `%n` 금지, SAST rule | `%n` call site 0건 |
| 회귀 | 로깅 코드에서 재도입 | code review checklist, unit test | non-literal format 0건 |

> 요약: 주소 누출, `%n` 쓰기, 로깅 회귀를 compiler와 SAST 검증으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 컴파일 경고 | format warning 0건 | GCC/Clang `-Wformat-security -Werror` |
| 바이너리 보호 | PIE, full RELRO 100% | checksec |
| 동적 검증 | leak 0건, crash 0건 | fuzzing, ASan, log scan |

> 요약: 성공 여부는 format warning 0건, full RELRO/PIE 적용률, 동적 leak 재현 0건으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 코드 규칙: 모든 `printf` 계열 호출은 literal format을 첫 인자로 두고 사용자 입력은 `%s` 인자로만 전달함.
2. 빌드 통제: `-Wformat -Wformat-security -Werror`, `_FORTIFY_SOURCE=2`, PIE, full RELRO를 release gate에 넣음.
3. 검증 운영: CodeQL/Semgrep으로 non-literal format과 `%n` 사용을 0건으로 관리하고 fuzzing과 log scan으로 주소 누출을 확인함.

**결론 (2줄):**
- 기술사 판단: format string은 입력 검증보다 API 사용 규칙과 compiler warning 차단이 우선인 취약점임.
- 향후 방향: 로깅·진단 코드까지 SAST와 secret/address redaction을 적용해 ASLR 우회 경로를 제거해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "포맷 스트링 공격을 설명하시오" | `%p/%x/%s/%n`별 read/write 흐름 | 취약 호출과 보호 호출 비교 |
| 요구사항 명시형 | "예방 방안을 제시하시오", "보안코딩 관점에서 설명하시오" | compiler warning, RELRO, SAST 절차 | literal format, `%n` 금지, log redaction 기준 |

> 요약: 설명형은 format specifier 동작을, 방안형은 compiler와 secure coding gate를 중심으로 전개함.
