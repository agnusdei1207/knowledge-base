---
title: "메모리 누수·힙 오버플로우 (Memory Leak Heap Overflow)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 273
---

# 📖 【암기용】 개념 완전 이해

> 목적: 메모리 누수와 힙 오버플로우를 원인, 증상, 탐지·대응 관점에서 구분하게 만든다.

## 한눈에
- **개요**: 메모리 누수는 불필요 객체 보존, 힙 오버플로우는 힙 용량 초과 또는 힙 영역 침범이다.
- **왜 필요한가**: 장시간 실행 서버의 OOM, 지연 증가, 보안 취약점 분석에서 두 개념 구분이 필요하다.
- **핵심 직관**: 누수는 쓰지 않는 짐을 계속 쌓아 두는 문제, 오버플로우는 창고 경계를 넘어 물건을 밀어 넣는 문제다.

## 깊이 이해
- **배경·문제의식**: 힙은 동적 객체 저장 공간이다. 참조가 남은 객체나 해제되지 않은 버퍼가 누적되면 가용 힙이 줄고, 경계 검사가 없으면 힙 메타데이터나 인접 객체가 손상된다.
- **작동 원리**: GC 언어의 누수는 도달 가능한 불필요 객체 때문에 발생하고, C/C++ 힙 오버플로우는 할당 크기를 넘어 쓰기 때문에 발생한다.
- **비유**: 회수해야 할 장비가 반납 목록에 남아 있으면 누수, 컨테이너 크기보다 큰 화물을 밀어 넣으면 오버플로우다.
- **구체 예시**: Java `static Map`에 요청 객체를 누적하면 old gen이 증가해 OOM 발생, C `strcpy`가 heap buffer boundary를 넘으면 allocator metadata 훼손 가능.
- **흔한 오해·주의점**: GC가 있어도 누수는 가능하고, 힙 오버플로우는 단순 장애가 아니라 RCE 취약점으로 이어질 수 있다.

## 연결 개념
- 가비지 컬렉션 — 누수 탐지 시 retained heap 분석과 연결
- 버퍼 오버플로우 — 경계 초과 쓰기의 대표 취약점
- 정적·동적 분석 — ASan, Valgrind, heap dump 분석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 메모리 누수와 힙 오버플로우를 장애·보안 리스크로 구분하고 탐지, 예방, 복구 방안을 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 메모리 누수는 회수 대상 메모리의 참조 유지 또는 해제 누락이고, 힙 오버플로우는 할당 경계를 초과한 쓰기다.
> 2. **가치**: 두 결함은 OOM, 지연 증가, 데이터 손상, 원격 코드 실행으로 이어지므로 코드·런타임·운영 통제가 필요하다.
> 3. **판단 포인트**: 누수는 사용량 추세와 retained heap, 오버플로우는 경계 검사와 sanitizer 검출 결과로 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메모리 결함 구분 확인 | leak vs overflow 원인·증상·영향 차이 | 두 용어를 OOM으로만 동일시 |
| 장애·보안 연결 역량 확인 | OOM, fragmentation, metadata corruption, RCE | 보안 영향 또는 복구 절차 누락 |
| 실무 예방 방안 확인 | RAII, ASan, heap dump, limit, restart policy | 도구 이름만 나열하고 지표 미제시 |

> 요약: 이 문제는 결함 유형별 원인과 탐지 지표를 구분해 예방·대응 체계를 쓰는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

메모리 누수·힙 오버플로우는 동적 메모리 관리 결함이다. 누수는 해제되지 않거나 참조가 유지된 메모리 누적이고, 힙 오버플로우는 할당 영역 경계 초과 쓰기다. 서버 장애와 보안 침해를 모두 유발하므로 개발·테스트·운영 전 구간 통제가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Application Code -> Heap Allocator/GC -> Heap Object
  / Leak: reference retained -> heap growth -> OOM
  / Overflow: boundary write -> metadata corruption -> crash/RCE
  -> Monitor/Analyzer -> Fix/Guard
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Heap Allocator | 동적 메모리 할당·해제 | malloc, jemalloc, JVM heap |
| Reference Owner | 객체 수명 결정 | cache, listener, ThreadLocal |
| Boundary Check | 버퍼 길이 검증 | C/C++ 수동 검증 필요 |
| Analyzer | 결함 탐지 | ASan, Valgrind, heap dump |

> 요약: 누수는 소유권·참조 관리 문제이고, 오버플로우는 할당 경계 검증 문제다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 처리 -> 객체/버퍼 할당 -> 사용 완료
  / 정상: 참조 제거 또는 free -> heap 회수
  / 누수: 참조 유지 -> live set 증가 -> OOM
  / 오버플로우: 경계 초과 쓰기 -> 손상 -> crash/RCE
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 힙 객체 또는 버퍼 할당 | allocation rate, malloc count |
| 2 | 수명 종료 조건 도달 | owner scope, reference count |
| 3 | 해제·참조 제거 또는 경계 검사 | free call, bounds check |
| 4 | 오류 발생 시 분석 | heap dump, sanitizer report |

> 요약: 수명 종료 후 회수되지 않으면 누수, 할당 크기 밖 쓰기가 발생하면 힙 오버플로우다.

---

## Ⅳ. 특징

| 구분 | 메모리 누수 | 힙 오버플로우 | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 원인 | 참조 유지, free 누락 | 버퍼 경계 초과 쓰기 | retained heap vs invalid write |
| 증상 | RSS·old gen 지속 증가 | crash, corruption, exploit | OOMKilled, SIGSEGV |
| 탐지 | heap dump, leak sanitizer | ASan, fuzzing, bounds checker | CI sanitizer 100% pass |
| 대응 | 수명 단축, cache TTL | safe API, length validation | `strncpy`, span, Rust borrow |

> 요약: 누수는 추세 분석, 오버플로우는 경계 위반 검출 중심으로 대응한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| GC 언어 | 자동 회수 | 참조 유지 누수 가능 | retained heap 기준 분석 |
| C/C++ | 수동 해제 | use-after-free·overflow 가능 | RAII, smart pointer, sanitizer |
| Rust | 소유권 검사 | unsafe 블록 관리 필요 | FFI·unsafe code review |

> 요약: 언어별 통제 지점은 GC 언어의 참조, C/C++의 경계·소유권, Rust의 unsafe 영역이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| OOM 장애 | leak 누적, heap limit 초과 | heap dump, cache TTL, restart budget | RSS 증가율, OOM count |
| 보안 침해 | heap overflow로 metadata 손상 | ASLR, DEP, ASan, safe API | sanitizer finding 0건 |
| 진단 지연 | 재현 조건 불명확 | memory profiler, canary deploy | leak slope MB/hour |

> 요약: 운영 리스크는 OOM 빈도, sanitizer 검출, 시간당 힙 증가율로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 누수 | 24시간 soak test 후 RSS 증가 5% 이하 | load test, heap dump diff |
| 경계 위반 | ASan/UBSan finding 0건 | CI sanitizer job |
| 복구 | OOM 후 MTTR 10분 이하 | alert, runbook, restart policy |

> 요약: 품질 게이트는 장시간 부하, sanitizer, 복구 시간 지표로 구성한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Java는 heap dump 2회와 dominator tree로 retained heap 상위 10개 객체를 식별하고 cache TTL·listener 해제를 적용함.
2. C/C++는 ASan, UBSan, fuzzing을 CI에 추가하고 unsafe copy API 사용을 code review block 기준으로 지정함.
3. 운영은 container memory limit, OOM alert, heap usage 80% 경보, canary soak test 24시간을 배포 기준으로 둠.

**결론 (2줄):**
- 기술사 판단: 누수는 수명·참조 관리, 오버플로우는 경계·소유권 검증으로 분리해 통제.
- 향후 방향: memory safe language, sanitizer, eBPF 기반 메모리 관측이 결합된 예방 중심 운영으로 이동함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | leak와 overflow 발생 흐름 | 원인·증상·탐지 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "비교하시오" | 장애·보안 영향 분석 흐름 | sanitizer, heap dump, 운영 지표 |

> 요약: 설명형은 개념 구분, 방안형은 탐지 도구와 운영 대응 중심으로 전환한다.
