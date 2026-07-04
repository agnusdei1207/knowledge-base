---
title: "쉘코드·ROP 공격 (Shellcode ROP)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 82
---

# 📖 【암기용】 개념 완전 이해

> 목적: 쉘코드와 ROP 공격을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 쉘코드는 주입 코드를 실행하고, ROP는 기존 코드 조각을 연결해 DEP/NX를 우회하는 공격 기법
- **왜 필요한가**: 현대 시스템은 데이터 영역 실행을 막기 때문에 공격자는 새 코드를 넣기보다 이미 존재하는 명령 조각을 재사용함.
- **핵심 직관**: 쉘코드는 공격자가 새 문장을 써 넣는 방식이고, ROP는 책 안의 기존 단어를 오려 새 문장을 만드는 방식임.

## 깊이 이해
- **배경·문제의식**: 초기 버퍼 오버플로우는 stack에 shellcode를 넣고 return address를 그 주소로 바꿨다. DEP/NX가 데이터 페이지 실행을 막자 공격자는 `ret`로 끝나는 gadget을 연결해 시스템 호출과 라이브러리 함수를 호출함.
- **작동 원리**: ROP는 stack pivot, gadget chain, register setup, indirect branch를 사용한다. 방어는 ASLR/PIE로 gadget 주소 예측을 막고, CFI와 shadow stack으로 허용되지 않은 return 흐름을 차단함.
- **비유**: 쉘코드는 금지된 도구를 직접 들여오는 방식이고, ROP는 창고 안 허용 도구를 순서대로 배치해 같은 결과를 만드는 방식임.
- **구체 예시**: NX enabled binary에서 stack shellcode는 실행 차단되지만, libc 주소가 노출되면 `system` 호출형 ret2libc 또는 gadget chain이 가능해진다.
- **흔한 오해·주의점**: NX가 켜져도 ROP는 코드 주입이 아니라 코드 재사용이므로 별도 통제가 필요하다. ASLR도 info leak이 있으면 주소 난수화 효과가 줄어듦.

## 연결 개념
- DEP/NX - 데이터 영역 실행 차단 보호기법
- ASLR/PIE - gadget과 libc 주소 예측을 어렵게 하는 난수화
- CFI/Shadow Stack - return 흐름과 간접 분기를 검증하는 런타임 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 쉘코드와 ROP를 공격 절차가 아니라 NX 우회, gadget chain, CFI·shadow stack 대응 관점으로 설명함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Shellcode는 주입 코드 실행, ROP는 기존 코드 gadget을 연결하는 코드 재사용 공격임.
> 2. **가치**: DEP/NX는 shellcode 실행을 막지만 ROP는 ret2libc, gadget chain으로 우회하므로 ASLR, CFI, shadow stack이 필요함.
> 3. **판단 포인트**: 정보 누출 차단, PIE/full RELRO, CFI, CET shadow stack, fuzzing crash triage를 함께 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 코드 주입과 코드 재사용 구분 확인 | shellcode, ret2libc, ROP gadget chain | 쉘코드와 ROP를 같은 공격으로 처리 |
| 보호기법 우회 이해 확인 | DEP/NX 우회, ASLR 정보 누출, CFI, shadow stack | NX 적용만으로 대응 완료라고 서술 |
| 방어 설계 역량 확인 | PIE, full RELRO, CET, SCS, SAST/fuzzing | gadget 제거와 검증 지표 누락 |

> 요약: 이 문제는 NX 이후 공격 패러다임이 코드 주입에서 코드 재사용으로 이동했음을 설명해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 실행 흐름 탈취 공격
- 배경: 쉘코드는 공격자 기계어를 실행하고 ROP는 바이너리·라이브러리 gadget을 연결해 DEP/NX가 막은 코드 주입을 우회함.
- 필요성: CFI, shadow stack, ASLR entropy, RELRO, retpoline 적용 여부를 바이너리 보안 점검 기준에 포함해 gadget 기반 실행 흐름 변조를 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
메모리 취약점 -> control-flow overwrite -> 실행 방식 선택
  / Shellcode: injected code -> data page execute 시도
  / ROP: gadget chain -> existing code reuse
Mitigation -> NX / ASLR / PIE / CFI / Shadow Stack
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Shellcode | 공격 목적 기계어 | NX, W^X로 데이터 페이지 실행 차단 |
| Gadget | `ret` 등으로 끝나는 기존 명령 조각 | ROP chain 구성 단위 |
| Stack Pivot | 공격자가 제어하는 stack으로 이동 | gadget chain 실행 준비 |
| ret2libc | libc 함수 직접 호출 | libc base leak이 핵심 전제 |
| CFI/Shadow Stack | 허용된 제어 흐름 검증 | return address 변조 탐지 |

> 요약: 쉘코드는 코드 주입, ROP는 코드 재사용이며 방어는 실행 권한, 주소 난수화, 제어 흐름 검증을 조합함.

---

## Ⅲ. 동작원리 및 흐름도

```text
취약점 트리거 -> return address overwrite -> NX 검사
  / NX off: shellcode 주소 이동
  / NX on: ROP gadget 주소 연결
ASLR/PIE 우회 시도 -> CFI/Shadow Stack 검증 -> 차단/침해 판정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | buffer overflow, UAF 등으로 control data overwrite | ASan crash 재현 |
| 2 | shellcode 또는 ROP chain 위치 준비 | NX enabled, W^X enabled |
| 3 | info leak으로 libc/gadget 주소 계산 | PIE, ASLR entropy, leak test |
| 4 | return 흐름이 gadget chain으로 이동 | CFI, shadow stack fault |
| 5 | syscall/libc 호출로 권한 행위 시도 | EDR, seccomp, audit log |

> 요약: ROP는 NX 검사 이후 ASLR 우회와 제어 흐름 검증 우회를 모두 만족해야 성공함.

---

## Ⅳ. 특징

| 구분 | Shellcode | ROP/ret2libc | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 실행 방식 | 주입 코드 실행 | 기존 코드 gadget 재사용 | NX가 shellcode 실행 차단 |
| 필요 조건 | executable stack/heap | gadget 주소, stack control | PIE/ASLR 적용률 100% |
| 우회 대상 | DEP/NX 미적용 | ASLR, CFI, shadow stack | info leak 0건 |
| 탐지 지표 | data page execute | abnormal return chain | CFI violation count |

> 요약: NX 이후 방어의 중심은 shellcode 차단에서 ROP chain 차단과 정보 누출 제거로 이동함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DEP/NX 단독 | NX, ASLR, PIE, CFI, shadow stack | 외부 입력 네이티브 서비스 |
| 비용/성능 | CFI 미적용 | compiler CFI, Intel CET, ARM PAC/SCS | 간접 호출이 많은 C/C++ 서비스 |
| 운영/위험 | crash만 수집 | exploitability triage, gadget scan | CVSS high 이상 취약점 |

> 요약: ROP 대응은 NX 단독이 아니라 주소 난수화와 제어 흐름 무결성 검증을 함께 적용할 때 판단 가능함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| NX 우회 | ROP gadget chain | CFI, shadow stack, CET | ROP exploit 차단 100% |
| ASLR 우회 | format string, info leak | PIE, pointer masking, leak test | 주소 노출 0건 |
| 탐지 지연 | crash를 장애로만 분류 | crash triage, EDR rule, audit log | triage SLA 24시간 |

> 요약: ROP 리스크는 gadget chain, 주소 누출, crash 분류 실패이며 컴파일·런타임·운영 탐지를 연결해 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 실행 보호 | NX/W^X enabled 100% | checksec, proc maps |
| 제어 흐름 | CFI 또는 shadow stack 적용 | compiler report, CET flag |
| 취약성 검증 | exploit PoC 0건, crash 0건 | fuzzing, ASan, ROP chain test |

> 요약: 성공 여부는 NX, CFI/shadow stack, exploit 재현 가능성 제거로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 빌드 하드닝: PIE, full RELRO, NX, stack protector, compiler CFI를 기본화하고 checksec 미통과 binary를 release gate에서 차단함.
2. 런타임 통제: Intel CET shadow stack, ARM PAC/SCS, seccomp profile, least privilege로 ROP 이후 권한 행위를 제한함.
3. 검증 운영: ASan/UBSan fuzzing, info leak test, crash triage 24시간 SLA로 gadget chain 재현 0건을 확인함.

**결론 (2줄):**
- 기술사 판단: NX만 적용된 시스템은 ROP에 노출되므로 ASLR/PIE와 CFI/shadow stack을 함께 적용해야 함.
- 향후 방향: ROP 대응은 gadget 감소, hardware CFI, memory-safe language 전환으로 확장해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "쉘코드와 ROP를 설명하시오" | code injection vs code reuse 흐름 | Shellcode, ROP, ret2libc 차이 |
| 요구사항 명시형 | "우회 기법을 비교하시오", "방어 방안을 제시하시오" | NX 우회, ASLR leak, CFI 검증 | CET, shadow stack, PIE, full RELRO 선택 기준 |

> 요약: 설명형은 공격 방식 차이를, 방안형은 NX 이후 ROP 차단 통제와 검증 지표를 중심으로 구성함.
