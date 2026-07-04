---
title: "WASM 서버사이드 (WebAssembly Server-side)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 186
---

# 📖 【암기용】 개념 완전 이해

> 목적: WASM 서버사이드를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서버사이드 WASM은 브라우저용으로 설계된 **WebAssembly**(이식 가능한 **바이트코드** 실행 포맷)를 서버·엣지·플러그인 환경에서 **런타임 샌드박스** 위에 실행해, 컨테이너보다 작은 배포 단위와 빠른 기동을 제공하는 실행 모델이다.
- **왜 필요한가**: 엣지·플러그인·짧은 요청 처리처럼 "매우 자주, 아주 짧게" 실행해야 하는 업무에서는 컨테이너의 이미지 크기와 기동 시간이 병목이 된다.
- **핵심 직관**: OS 전체를 싸서 옮기는 컨테이너(캠핑카)가 아니라, 검증된 작은 실행 캡슐(휴대용 공구)을 필요할 때마다 여러 환경에서 여는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| WebAssembly (WASM) | 스택 기반 가상머신을 위한 이식 가능한 **바이트코드** 포맷 — 이 문서가 다루는 **대상** | 어떤 기계에서도 읽히는 표준 설계도면 |
| bytecode | 사람이 짠 소스 코드를 컴파일한, CPU가 아닌 가상머신이 실행하는 중간 형태 명령어 | 통역 전 표준화된 각본 |
| Linear Memory (선형 메모리) | WASM 모듈에 할당된 하나의 연속된 바이트 배열 — 모듈은 이 범위 밖을 절대 건드릴 수 없음 | 방 안에서만 움직일 수 있는 울타리 |
| Sandbox | 모듈이 호스트 시스템에 직접 접근하지 못하게 격리하는 실행 환경 | 방음·방화 처리된 실험실 |
| Runtime | 컴파일된 module을 적재해 sandbox에서 실행하는 엔진 (Wasmtime, Wasmer, WasmEdge) | 캡슐을 여는 전용 리더기 |
| Module | 컴파일이 끝난 배포 가능한 WASM 실행 단위 | 완성된 캡슐 하나 |
| Instantiation (인스턴스화) | Module을 실제 메모리에 올려 실행 가능한 상태로 만드는 과정 | 캡슐을 열어 즉시 쓸 수 있게 준비 |
| Cold Start | 요청이 들어온 뒤 실행 환경이 준비돼 첫 응답이 나가기까지 걸리는 시간 | 손님이 온 뒤 가게 문을 여는 시간 |
| Capability (권한) | 모듈이 호출할 수 있도록 명시적으로 부여된 host 자원 접근 권한 (187 WASI 참고) | 출입 카드에 찍힌 허용 구역 목록 |

## 깊이 이해

### 왜 컨테이너만으로 부족했나 (배경)
- 2017년 WASM은 브라우저 안에서 JavaScript보다 빠른 실행을 목표로 표준화됐다(스택 기반 VM, 정적 타입 검증). 이후 "sandbox·이식성·빠른 기동"이라는 특성이 브라우저 밖에서도 유용하다는 것이 확인되며, 2019년 WASI 제안과 함께 서버·엣지로 확장됐다.
- 컨테이너는 OS 커널을 공유하되 프로세스·파일시스템 네임스페이스 전체를 격리하는 무거운 단위다. 반면 WASM 모듈은 스택 기반 VM 위에서 실행되는 훨씬 작은 단위이며, 격리도 커널 네임스페이스가 아니라 **컴파일 시점의 타입 검증 + 선형 메모리 경계 체크**로 이뤄진다.

### 크기와 기동 속도를 수치로 비교
- 컨테이너 이미지는 베이스 OS 레이어를 포함해 보통 수백 MB~수 GB이며, 콜드 스타트(이미지 pull + 컨테이너 런타임 초기화 + 프로세스 기동)는 수백 ms~수 초가 걸린다.
- WASM 모듈은 대개 수백 KB~수 MB 수준이고, Wasmtime·WasmEdge 같은 런타임은 모듈을 이미 로드해 둔 상태라면 **인스턴스화 자체는 1ms 미만~수 ms** 수준으로 끝난다. 요청마다 새 인스턴스를 만들어도 사용자가 체감할 지연이 거의 없는 이유다.
- 예: CDN 엣지에서 2MB짜리 WASM filter가 요청당 새 인스턴스로 기동돼 HTTP 헤더 변환·인증 토큰 검증을 수행해도, 전체 처리가 10ms 이내에 끝난다 — 컨테이너였다면 매 요청마다 프로세스를 새로 띄우는 방식 자체가 성립하지 않는다.

### 격리 메커니즘의 차이 (컨테이너 vs WASM)
- 컨테이너: Linux namespace(PID, network, mount 등)와 cgroup으로 프로세스를 격리한다 — 커널은 공유하되 "보이는 범위"를 나눈다.
- WASM: 모듈이 실행되는 동안 접근 가능한 메모리는 오직 자신에게 할당된 **선형 메모리** 배열뿐이다. 컴파일 시점에 모든 함수 시그니처와 점프 대상이 검증되므로, 임의 코드 실행이나 스택 오버플로우로 인접 메모리를 침범하는 유형의 취약점이 원천적으로 봉쇄된다. 대신 파일·네트워크 같은 OS 자원은 기본적으로 **아무것도 접근할 수 없고**, WASI가 명시한 capability를 통해서만 열린다(187 참고).

### 비유와 흔한 오해
- **비유**: 컨테이너가 살림살이를 통째로 옮기는 캠핑카라면, WASM 모듈은 필요한 기능만 담아 여러 장소에 꽂아 쓰는 휴대용 공구 세트다.
- **오해**: "WASM이 컨테이너를 대체한다"는 생각은 과장이다. WASM은 POSIX API, 스레드, 파일시스템 전체 접근처럼 OS 의존도가 높은 장시간 프로세스에는 맞지 않는다 — 실제 지원 범위는 WASI 표준과 런타임 구현 수준에 달려 있으며, 짧고 반복적인 실행 단위(엣지 필터, 플러그인, 짧은 함수)에 강점이 있다.

## 연결 개념
- WASI - 서버사이드 WASM이 OS 자원에 접근하는 표준 인터페이스 (187 참고)
- 서버리스 FaaS - 짧은 실행·콜드 스타트 관점에서 비교되는 대상
- Plugin Architecture - sandbox 기반 확장 기능 구현 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 서버사이드 WASM 답안은 작은 실행 단위, sandbox, WASI 제약, 컨테이너와의 선택 기준을 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WASM 서버사이드는 WebAssembly bytecode를 서버, 엣지, 플러그인 런타임에서 sandbox로 실행하는 모델임.
> 2. **가치**: MB 단위 module, ms 단위 startup, 언어 중립 실행, capability 기반 권한으로 엣지와 서버리스 실행 단위를 세분화함.
> 3. **판단 포인트**: runtime 지원 API, WASI 호환, cold start, sandbox escape, observability, 컨테이너 대비 운영 범위를 기준으로 선택해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| WASM 실행 모델 이해 확인 | bytecode, runtime, sandbox, WASI | 브라우저 기술로만 설명 |
| 서버 적용 판단 확인 | edge, plugin, FaaS, sidecar 대안 | 컨테이너 전면 대체 주장 |
| 운영 제약 확인 | API 제한, 관측, 보안, 공급망 | 런타임 호환성 누락 |

> 요약: 이 문제는 WASM의 실행 단위 장점과 서버 운영 제약을 함께 판단해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: sandbox bytecode 실행 모델
- 배경: 엣지, 플러그인, 서버리스 환경은 작은 배포 단위와 짧은 기동 시간이 필요하다.
- 필요성: WASM bytecode와 runtime 격리로 컨테이너보다 세분화된 모듈 실행 단위를 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Code -> WASM Compile -> Module Registry -> WASM Runtime -> Host Function/Service
  / Interface: WASI
  / Control: capability, signing, policy
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| WASM Module | 컴파일된 실행 단위 | MB 단위 배포 |
| WASM Runtime | module 로드와 sandbox 실행 | Wasmtime, Wasmer, WasmEdge |
| WASI | 파일, 시간, 난수 등 시스템 인터페이스 | capability 기반 허용 |
| Host Function | DB, HTTP, secret 연동 | runtime별 구현 차이 |

> 요약: 서버사이드 WASM은 module, runtime, WASI, host function으로 구성되며 capability 기반으로 외부 접근을 제한함.

---

## Ⅲ. 동작원리 및 흐름도

```text
코드 작성 -> wasm32 target compile -> module 서명/등록 -> runtime load -> sandbox 실행 -> host call -> metric 수집
  / 권한 없음 -> capability deny
  / API 미지원 -> runtime error
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Rust, Go, C/C++ 코드를 WASM으로 컴파일 | wasm32-wasi target |
| 2 | module 서명과 registry 등록 | signature 검증 100% |
| 3 | runtime이 sandbox memory와 capability 설정 | 허용 디렉터리, env 제한 |
| 4 | host function과 WASI API 호출 | API error rate |
| 5 | 실행 시간과 오류 metric 수집 | startup, duration, trap count |

> 요약: WASM은 컴파일된 module을 runtime sandbox에 적재하고 허용된 WASI·host function만 호출함.

---

## Ⅳ. 특징

| 구분 | 컨테이너 | 서버사이드 WASM | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 배포 단위 | 이미지 수십 MB~GB | module MB 단위 | image size 대비 1/10 목표 |
| 기동 | runtime, process 초기화 | module instantiation | cold start 10ms~100ms |
| 격리 | namespace, cgroup | memory sandbox, capability | host API 허용 목록 |
| 호환 | OS API 범위 넓음 | WASI 지원 범위 의존 | POSIX 요구 업무 제외 |

> 요약: WASM은 작은 실행 단위와 sandbox가 강점이나 OS API 호환성은 runtime과 WASI 수준에 좌우됨.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 컨테이너 서비스 | WASM module | plugin, edge, short-lived task |
| 비용/처리 | image pull, runtime start | module load | cold start 100ms 이하 필요 |
| 운영/위험 | 표준 도구 풍부 | runtime 생태계 성장 중 | WASI API 충족 여부 |

> 요약: WASM은 엣지·플러그인·짧은 함수에 적합하고, 장시간 프로세스와 OS API 의존 업무는 컨테이너가 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| API 부족 | WASI 미지원 기능 | host function 설계, fallback | API error rate |
| 공급망 위조 | module 변조 | signing, provenance, SBOM | unsigned module 0건 |
| 관측 부족 | runtime metric 미성숙 | OTLP exporter, runtime log | trace coverage |

> 요약: WASM 운영 리스크는 API 지원, module 신뢰성, 관측 체계로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 기동 | cold start 100ms 이하 | runtime benchmark |
| 보안 | unsigned module 0건 | registry policy |
| 품질 | trap rate 0.1% 이하 | runtime metric |

> 요약: WASM 적용 효과는 startup, 서명 검증, trap rate로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 대상 분류: edge filter, plugin, webhook, 단기 변환 작업처럼 cold start 100ms 이하가 필요한 기능을 선별
2. 런타임 표준화: Wasmtime 또는 WasmEdge를 기준 runtime으로 정하고 WASI API, host function, OTLP exporter를 검증
3. 공급망 통제: WASM module 서명, SBOM, provenance 검증을 registry admission 조건으로 설정

**결론 (2줄):**
- 기술사 판단: 작은 함수·엣지·플러그인은 WASM, OS API와 장시간 실행이 필요한 업무는 컨테이너를 선택함
- 향후 방향: WASI Preview 2, component model, OCI registry 연계가 서버사이드 WASM의 이식성 기준이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "서버사이드 WASM을 설명하시오", "기술하시오" | compile, runtime load, WASI 호출 흐름 | 컨테이너 대비 배포 단위·기동·격리 |
| 요구사항 명시형 | "서버리스 실행 구조를 설계하시오", "비교하시오" | runtime, host function, 관측 설계 | 적용 대상과 제외 조건 |

> 요약: 설명형은 실행 모델, 설계형은 WASI 제약과 컨테이너 선택 기준 중심으로 전환함.
