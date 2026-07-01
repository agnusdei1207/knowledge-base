---
title: "WebAssembly (WebAssembly)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 270
---

# 📖 【암기용】 개념 완전 이해

> 목적: WebAssembly를 브라우저와 서버 런타임에서 언어 중립적으로 실행되는 이식 가능한 바이너리 명령 형식으로 이해하게 만든다.

## 한눈에
- **개요**: C/C++, Rust 등 여러 언어 코드를 안전한 샌드박스에서 실행하기 위한 이식형 바이너리 포맷
- **왜 필요한가**: JavaScript만으로 처리하기 어려운 CPU 집약 작업과 언어 재사용 요구가 브라우저·엣지·서버 환경에서 증가했다.
- **핵심 직관**: 특정 국가 언어가 아니라 여러 나라 문서를 같은 기계가 읽을 수 있게 만든 공통 중간어와 같다.

## 깊이 이해
- **배경·문제의식**: 웹은 배포와 접근성이 뛰어나지만 영상 처리, 게임 엔진, 암호 연산처럼 기존 native 코드 자산을 활용하기 어렵다.
- **작동 원리**: 소스 코드를 `.wasm` 모듈로 컴파일하고 런타임은 검증, 인스턴스화, 선형 메모리 할당, import/export 연결 후 함수를 실행한다.
- **비유**: 여러 악보를 공통 자동연주 피아노 형식으로 바꾸면 연주자는 달라도 같은 기계가 재생할 수 있는 것과 같다.
- **구체 예시**: Rust로 작성한 이미지 리사이즈 코드를 WebAssembly로 컴파일해 브라우저에서 파일을 서버 전송 전에 처리한다.
- **흔한 오해·주의점**: WebAssembly는 JavaScript 대체물이 아니라 상호 보완 실행 포맷이며, OS 접근은 WASI 같은 인터페이스가 필요하다.

## 연결 개념
- WASI — WebAssembly가 브라우저 밖에서 시스템 기능을 쓰는 표준 인터페이스
- Edge Computing — 작은 샌드박스 모듈을 분산 실행하는 활용처
- Component Model — Wasm 모듈 간 인터페이스와 조합을 표준화하는 방향

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: WebAssembly는 바이너리 포맷, 샌드박스, 선형 메모리, import/export, 런타임을 연결해 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WebAssembly는 다양한 언어를 이식 가능한 바이너리 모듈로 실행하기 위한 표준 명령 형식임.
> 2. **가치**: 브라우저, 서버, 엣지에서 동일 모듈을 샌드박스 안에서 실행해 코드 재사용과 격리를 제공함.
> 3. **판단 포인트**: CPU 집약 로직과 플러그인 격리에 적합하지만 DOM·OS 접근은 host API와 WASI 지원을 확인해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 실행 모델 이해 확인 | module, instance, linear memory, import/export | Wasm을 프로그래밍 언어로 오기술 |
| 활용 범위 확인 | browser, server, edge, plugin sandbox | JavaScript 완전 대체로 단정 |
| 보안 판단 확인 | sandbox, capability, host API 제한 | OS 접근이 기본 제공된다고 설명 |

> 요약: 이 문제는 WebAssembly가 이식형 실행 포맷이라는 본질과 샌드박스 제약을 함께 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 이식형 바이너리 실행 포맷
- 배경: 웹·엣지 환경에서 native 코드 자산과 CPU 집약 로직을 재사용할 요구가 증가함.
- 필요성: 브라우저·서버·엣지에서 동일 모듈을 샌드박스 격리로 실행해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Source Code -> Wasm Compiler -> .wasm Module -> Runtime
Runtime -> Validation -> Instance -> Linear Memory / Table / Import / Export
Host -> Import Function -> Wasm Function -> Export Result
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Wasm Module | 컴파일된 바이너리 단위 | stack machine 명령 형식 |
| Runtime | 검증·인스턴스화·실행 | browser, Wasmtime 등 |
| Linear Memory | 모듈이 사용하는 연속 메모리 | host와 명시적 공유 |
| Import/Export | host와 모듈 간 함수 연결 | capability 경계 역할 |

> 요약: WebAssembly는 모듈을 런타임이 검증하고 인스턴스화한 뒤 메모리와 함수 인터페이스로 host와 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
소스 컴파일 -> Wasm 모듈 생성 -> 런타임 검증
-> import 연결 -> instance 생성 -> 함수 호출
-> linear memory 접근 -> 결과 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 언어별 컴파일러가 `.wasm` 생성 | target wasm32 |
| 2 | 런타임이 타입·메모리 접근 검증 | validation pass |
| 3 | host API를 import로 연결 | capability 목록 |
| 4 | export 함수를 호출하고 결과 수신 | execution result |

> 요약: WebAssembly는 컴파일된 모듈을 검증한 뒤 host가 허용한 API만 연결해 실행한다.

---

## Ⅳ. 특징

| 구분 | JavaScript | WebAssembly | 판단 기준 |
|:---|:---|:---|:---|
| 목적 | 웹 동적 로직 | 이식형 바이너리 실행 | CPU 집약 로직 |
| 언어 | JS 중심 | C/C++/Rust 등 다언어 | 기존 코드 재사용 |
| 메모리 | JS heap | linear memory | host 연계 방식 |
| 시스템 접근 | Web API | host import·WASI 필요 | 실행 환경 |

> 요약: WebAssembly는 JavaScript와 경쟁보다 역할 분담 관계이며, 계산 모듈과 격리 플러그인에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | native binary | Wasm sandbox module | 격리와 이식성 필요 |
| 비용/성능 | OS 종속 실행 | runtime 기반 실행 | 런타임 지원 여부 |
| 운영/위험 | 플랫폼별 배포 | 동일 모듈 배포 | host API 표준화 |

> 요약: 플랫폼 독립 배포와 sandbox가 필요하면 WebAssembly, OS 기능 전체가 필요하면 native 실행이 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Host API 누락 | 실행 환경별 import 차이 | interface contract 명시 | import resolution failure |
| 메모리 오류 | linear memory 경계 처리 | bounds check, fuzz test | trap count |
| 공급망 위험 | 외부 Wasm 모듈 사용 | 서명 검증, SBOM | signature validation |

> 요약: WebAssembly 리스크는 host API, 메모리 경계, 공급망이며 인터페이스 계약과 서명 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 이식성 | 대상 runtime 100% 실행 | compatibility test |
| 격리 | 허용 import 외 접근 차단 | sandbox test |
| 지연 | 모듈 초기화 시간 예산 이내 | runtime metric |

> 요약: WebAssembly 도입은 런타임 호환성, sandbox 격리, 초기화 지연을 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 이미지 처리, 규칙 엔진, 플러그인처럼 host API 경계가 명확한 로직을 Wasm 후보로 분류함.
2. import/export 인터페이스와 linear memory 사용 규칙을 API 계약서로 고정함.
3. Wasm module 서명, SBOM, runtime compatibility test를 CI 단계에 포함함.

**결론 (2줄):**
- 기술사 판단: 격리된 계산 모듈과 다언어 코드 재사용이 핵심이면 WebAssembly를 선택하고, OS 의존 기능이 많으면 native 또는 container를 선택함.
- 향후 방향: WebAssembly는 WASI와 Component Model을 통해 서버·엣지 플러그인 실행 기반으로 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WebAssembly를 설명하시오" | 컴파일·검증·인스턴스화 흐름 | JavaScript·native 대비 차이 |
| 요구사항 명시형 | "엣지 플러그인 실행 구조를 설계하시오" | import/export와 sandbox 절차 | host API·공급망 리스크 |

> 요약: 설명형은 실행 모델을, 설계형은 인터페이스 계약과 격리 검증을 중심으로 작성한다.
