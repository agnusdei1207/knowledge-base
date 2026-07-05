---
title: "Use-after-free 취약점 (Use-After-Free)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 84
---

# 📖 【암기용】 개념 완전 이해

> 목적: Use-after-free 취약점을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 해제된 메모리를 남은 포인터로 다시 사용해 데이터 변조, 타입 혼동, 코드 실행을 유발하는 취약점
- **왜 필요한가**: 브라우저, 커널, C++ 서버, 드라이버는 객체 수명 관리가 복잡해 dangling pointer 1건이 RCE나 권한 상승으로 이어질 수 있음.
- **핵심 직관**: 반납한 사물함 열쇠를 계속 들고 있다가, 새 사용자의 사물함을 열어 내용물을 바꾸는 상황임.

## 깊이 이해
- **배경·문제의식**: `free` 또는 객체 소멸 후 포인터가 null 처리되지 않거나 ownership이 중복되면 dangling pointer가 남는다. allocator가 같은 주소를 다른 객체에 재사용하면 이전 포인터가 새 객체를 가리킴.
- **작동 원리**: 공격자는 heap grooming으로 해제된 chunk와 같은 크기의 객체를 재배치하고, stale pointer 접근 시 vtable, function pointer, length field 등을 조작한다. 방어는 safe ownership, reference counting, RAII, ASan, quarantine, hardened allocator로 수행함.
- **비유**: 호텔 키를 반납했지만 복제키를 갖고 있다가 다음 투숙객 방에 들어가는 것과 같다. 문제는 키가 아니라 방 배정과 수명 관리 실패임.
- **구체 예시**: 객체 A를 `delete`한 뒤 이벤트 콜백이 A 포인터를 보관하고 있으면, 같은 heap slot에 객체 B가 배치된 후 콜백이 B의 vtable을 잘못 호출할 수 있음.
- **흔한 오해·주의점**: null 초기화만으로 충분하지 않다. 포인터 복사본, callback, cache, iterator가 남아 있으면 다른 경로의 dangling pointer가 계속 존재함.

## 연결 개념
- Heap Grooming - 해제 chunk 재사용 위치를 공격자가 조절하는 기법
- ASan - UAF와 out-of-bounds를 런타임에서 탐지하는 sanitizer
- Safe Ownership - RAII, smart pointer, borrow checker로 수명 오류를 제한

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: UAF 답안은 dangling pointer, heap grooming, 객체 수명, ASan·safe ownership 검증을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Use-after-free는 해제된 객체를 stale pointer로 재사용해 타입 혼동, 데이터 변조, 제어 흐름 탈취를 만드는 수명 취약점임.
> 2. **가치**: RAII, smart pointer, reference counting, Rust ownership, ASan, hardened allocator로 dangling pointer 사용을 탐지·차단함.
> 3. **판단 포인트**: heap grooming 가능성, vtable/function pointer 변조, sanitizer coverage, ownership rule을 함께 써야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메모리 수명 구조 이해 확인 | free, dangling pointer, stale reference, allocator reuse | 단순 null pointer 오류로 설명 |
| 공격 흐름 분석 확인 | heap grooming, type confusion, vtable hijack | stack overflow와 혼동 |
| 예방·검증 역량 확인 | RAII, smart pointer, ASan, fuzzing, Rust ownership | free 후 null만 제시 |

> 요약: 이 문제는 해제 후 재사용이라는 수명 오류를 heap 재배치와 객체 제어 흐름 관점으로 설명해야 함.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **Use-after-free 취약점** | Use-after-free 취약점 (Use-After-Free)의 핵심 개념 | 이 주제의 본질 |

---

## Ⅰ. 개요 및 필요성

- 개요: 해제 객체 재사용 취약점
- 배경: 객체 수명과 포인터 참조가 분리된 C/C++ 코드에서 stale pointer가 남으면 해제된 heap chunk가 새 객체로 재사용될 때 메모리 변조가 발생함.
- 필요성: CWE-416, ownership 설계, AddressSanitizer, quarantine allocator, fuzzing을 적용해 브라우저·커널·서버의 RCE 위험을 검증해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
객체 할당 -> 포인터 복사 -> free/delete -> dangling pointer 잔존
  / allocator reuse: 같은 chunk에 새 객체 배치
  / stale access: read/write/call
Mitigation -> ownership / ASan / quarantine / hardened allocator
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Heap Object | 동적 할당 대상 | vtable, callback, length field 포함 가능 |
| Dangling Pointer | 해제 후 남은 참조 | 복사본, cache, iterator, callback에 잔존 |
| Heap Grooming | 재사용 chunk 배치 조절 | 같은 size class 객체로 재할당 |
| Mitigation | 수명 오류 차단 | RAII, smart pointer, ASan, quarantine |

> 요약: UAF는 해제 객체와 남은 참조가 분리되고 allocator가 같은 주소를 재사용할 때 발생함.

---

## Ⅲ. 동작원리 및 흐름도

```text
객체 생성 -> 참조 전달 -> 객체 해제 -> 참조 무효화 누락
  / heap grooming -> 공격자 제어 객체 재배치
stale pointer 사용 -> 필드 변조/간접 호출 -> sanitizer 또는 CFI 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 객체가 heap에 할당되고 여러 포인터에 전달 | ownership map 존재 |
| 2 | 한 경로에서 free/delete 수행 | double owner 0건 |
| 3 | 다른 경로의 dangling pointer가 남음 | ASan UAF 검출 |
| 4 | heap grooming으로 같은 chunk 재사용 | allocator quarantine 적용 |
| 5 | stale pointer read/write/call 발생 | CFI, sanitizer fault |

> 요약: UAF 공격은 해제, 재할당, stale access의 순서로 진행되며 sanitizer와 ownership 규칙으로 탐지함.

---

## Ⅳ. 특징

| 구분 | 취약 구현 | 보호 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 소유권 | raw pointer 다중 소유 | `unique_ptr`, `shared_ptr`, RAII | raw owning pointer 0건 |
| 수명 관리 | callback 참조 잔존 | weak reference, lifecycle cancel | stale callback 0건 |
| heap 재사용 | 즉시 재할당 | quarantine, hardened allocator | ASan UAF 0건 |
| 검증 | 기능 테스트 중심 | ASan, UBSan, fuzzing | crash 0건 |

> 요약: UAF 방어는 포인터 null 처리보다 ownership 단일화와 sanitizer 기반 수명 검증이 핵심임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | raw pointer + manual free | RAII, smart pointer, borrow checker | C++ 신규 코드, Rust 전환 가능 영역 |
| 비용/성능 | sanitizer 미적용 | ASan CI, hardened allocator | 외부 입력 처리, parser, browser engine |
| 운영/위험 | crash 후 재현 | fuzzing corpus, crash dedup | UAF crash 재현 가능 시 CVSS high |

> 요약: 신규 개발은 safe ownership을 우선하고, 레거시는 sanitizer와 allocator hardening으로 잔여 위험을 낮춤.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| RCE | vtable/function pointer 재사용 | CFI, ASan, object type check | exploit 재현 0건 |
| 회귀 | raw pointer 소유권 혼재 | code review, clang-tidy rule | raw owning pointer 0건 |
| 탐지 누락 | 재현 어려운 race/UAF | fuzzing, TSAN, crash dump | unique crash 0건 |

> 요약: UAF 리스크는 제어 흐름 탈취, 소유권 회귀, 비결정 crash이며 정적·동적 검증을 함께 적용함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수명 안전 | owning raw pointer 0건 | code review, clang-tidy |
| 동적 검증 | ASan/UBSan UAF 0건 | sanitizer CI, fuzzing |
| 런타임 통제 | CFI enabled, hardened allocator 적용 | binary flag, allocator config |

> 요약: 성공 여부는 ownership rule 위반, sanitizer UAF, 런타임 hardening 적용률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 설계 통제: 객체별 owner를 1개로 정의하고 C++ RAII, `unique_ptr`, `weak_ptr`, lifecycle cancel rule을 coding standard에 반영함.
2. 검증 통제: ASan/UBSan/TSAN과 fuzzing을 CI에 넣고 UAF crash 0건, unique crash 0건을 release gate로 둠.
3. 런타임 통제: hardened allocator, quarantine, CFI, least privilege sandbox를 적용해 stale pointer 악용 범위를 제한함.

**결론 (2줄):**
- 기술사 판단: UAF는 입력 검증보다 객체 소유권과 수명 설계가 우선이며 신규 고위험 모듈은 Rust 등 ownership 언어를 검토해야 함.
- 향후 방향: 메모리 안전성은 sanitizer 보조에서 memory-safe language, hardware memory tagging, CFI 조합으로 이동해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Use-after-free를 설명하시오" | free 후 dangling pointer와 heap reuse 흐름 | raw pointer와 safe ownership 비교 |
| 요구사항 명시형 | "방어 방안을 제시하시오", "설계하시오" | ownership map, ASan/fuzzing, hardened allocator 절차 | RAII, smart pointer, Rust, CFI 선택 기준 |

> 요약: 설명형은 수명 오류 원리를, 방안형은 ownership 설계와 sanitizer 검증 지표를 중심으로 구성함.
