---
title: "WASI (WASI)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 187
---

# 📖 【암기용】 개념 완전 이해

> 목적: WASI를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: WASI(WebAssembly System Interface)는 브라우저 밖에서 실행되는 WASM 모듈이 파일·시간·난수·네트워크 같은 **시스템 자원**에 접근할 때 지켜야 할 **capability 기반 보안 모델**의 표준 API다.
- **왜 필요한가**: WASM 모듈은 기본적으로 자신의 선형 메모리 밖은 아무것도 볼 수 없는 순수 sandbox라서, 파일을 열거나 시간을 읽는 함수조차 내장돼 있지 않다 — 이런 기능을 "안전하게" 여는 표준 규칙이 필요하다.
- **핵심 직관**: WASM 모듈에게 집 열쇠를 통째로 주는 대신, 필요한 방(자원)의 출입증만 미리 발급하는 규칙이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| WASI (WebAssembly System Interface) | WASM 모듈이 OS 자원을 호출하는 방식을 정의한 표준 인터페이스 — 이 문서가 다루는 **대상** | 캡슐 밖 세상과 통하는 표준 배관 규격 |
| Capability 기반 보안 | 프로세스가 자원 경로를 알기만 하면 접근 가능한 방식이 아니라, 실행 전에 **명시적으로 건네받은 핸들**만 사용할 수 있는 보안 모델 | 주소를 안다고 들어갈 수 없고, 발급된 카드가 있어야 들어감 |
| Preopen (사전 개방) | 모듈 실행을 시작하기 전에 runtime이 특정 디렉터리를 파일 디스크립터로 미리 열어 넘겨주는 절차 | 체크인 때 미리 지정된 객실 카드만 발급 |
| Ambient Authority (주변 권한) | POSIX처럼 프로세스가 파일 경로 문자열만으로 시스템 전체에 접근 가능한 전통 모델 — WASI가 지양하는 대상 | 마스터키 한 장으로 건물 전체 출입 |
| Preview 1 | 초기 WASI 표준 — POSIX와 유사한 flat 함수 목록(open, read, write 등) | 1세대 규격, 기능은 되지만 조합이 어려움 |
| Preview 2 / Component Model | WIT(WebAssembly Interface Type)로 인터페이스를 기술해 모듈 간 조합성을 높인 차세대 표준 | 부품 규격을 통일해 서로 끼워 맞추게 함 |
| Runtime | WASI API를 실제로 구현하고 capability를 검사하는 실행 엔진 (Wasmtime, WasmEdge) | 카드 인식기 — 카드 발급 규격을 실제로 구현 |

## 깊이 이해

### 왜 "권한을 명시적으로 준다"는 게 특별한가 (배경)
- 전통 POSIX 프로그램은 **ambient authority**로 동작한다. 프로세스가 `/etc/passwd`라는 경로 문자열만 알면(그리고 OS 권한이 맞으면) 별도 허가 없이 바로 열 수 있다. 문제는 이 모델에서는 코드 어디에 숨어 있는 라이브러리든 프로세스 권한 범위 안의 파일을 임의로 읽고 쓸 수 있다는 것 — 신뢰할 수 없는 서드파티 WASM 모듈을 실행할 때 이 모델을 그대로 쓰면 sandbox의 의미가 사라진다.
- WASI는 이를 **capability 기반**으로 뒤집는다. 모듈은 실행 시작 시 runtime이 건네준 파일 디스크립터(핸들) 목록에 있는 자원만 쓸 수 있고, 경로 문자열을 안다고 해서 임의 파일에 접근할 수 없다. "권한이 있는가"의 기준이 "경로를 아는가"에서 "핸들을 받았는가"로 바뀌는 것이다.

### Preopen을 구체 예로 이해하기
- 예: 이미지 변환 WASM 모듈을 실행할 때 runtime 설정에서 `/input`, `/output` 두 디렉터리만 preopen하고 네트워크 capability는 부여하지 않는다고 하자. 모듈 코드 안에 `/etc/passwd`를 여는 로직이 있어도, 애초에 그 경로에 대한 파일 디스크립터가 전달되지 않았으므로 시스템 콜 자체가 "그런 핸들은 없다"는 오류로 즉시 실패한다 — 접근 거부가 아니라 **접근 대상이 애초에 존재하지 않는** 형태의 차단이다.
- 같은 모듈이 이미지를 외부 서버로 전송하려 시도해도, 네트워크 capability를 받지 못했으므로 소켓을 열 수 없다. 결과적으로 이 모듈은 `/input`을 읽고 `/output`에 쓰는 일만 할 수 있는, 기능이 물리적으로 제한된 실행 단위가 된다.

### Preview 1과 Preview 2의 차이
- Preview 1은 POSIX와 비슷한 형태의 개별 함수(파일 열기·읽기·쓰기, clock 조회, 난수 생성 등)를 하나씩 나열한 API였다. 동작은 하지만 여러 모듈을 조합하거나 언어를 넘나들며 인터페이스를 재사용하기가 번거로웠다.
- Preview 2는 WIT(WebAssembly Interface Type)라는 인터페이스 기술 언어로 자원·함수 시그니처를 정의하고, 이를 기반으로 한 **Component Model**이 서로 다른 언어로 만든 WASM 모듈끼리도 명확한 계약으로 조합될 수 있게 한다 — 예를 들어 Rust로 만든 로깅 컴포넌트를 Go로 만든 HTTP 핸들러 컴포넌트가 표준 인터페이스로 호출하는 식이다.

### 비유와 흔한 오해
- **비유**: 호텔 투숙객에게 마스터키를 주는 대신, 객실·헬스장·조식장처럼 필요한 곳만 카드에 담아 발급하는 방식이다.
- **오해**: "WASI가 곧 WASM 런타임"이라고 착각하기 쉽지만, WASI는 규격(무엇을 어떻게 요청하는가)일 뿐이고 실제로 그 요청을 처리하는 것은 Wasmtime·WasmEdge 같은 **runtime의 구현**이다. 같은 모듈이라도 runtime과 지원 Preview 버전에 따라 실제로 쓸 수 있는 API 범위가 달라질 수 있다.

## 연결 개념
- WebAssembly Server-side - WASI가 자원 접근을 표준화해주는 실행 환경 (186 참고)
- Capability Security - WASI가 채택한 명시 허용 권한 모델의 일반 이론
- Component Model - Preview 2 기반 WASM 모듈 간 인터페이스 조합 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: WASI 답안은 WASM sandbox와 OS API 사이의 capability 기반 표준 인터페이스라는 점을 중심으로 구성해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WASI는 WebAssembly module이 브라우저 밖에서 시스템 자원을 안전하게 호출하도록 정의한 표준 인터페이스임.
> 2. **가치**: preopen directory, clock, random, socket 같은 capability를 명시해 sandbox와 서버 실행 요구를 조정함.
> 3. **판단 포인트**: Preview 버전, runtime 구현 범위, capability 최소화, host function 경계, API 호환성을 기준으로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| WASM 서버 실행 이해 확인 | sandbox, system interface, capability | WASM runtime과 혼동 |
| 보안 모델 판단 확인 | preopen, least privilege, host call | POSIX 전체 노출 주장 |
| 표준·호환성 확인 | Preview 1/2, component model, runtime 차이 | API 지원 범위 누락 |

> 요약: 이 문제는 WASI를 WASM의 OS 접근 표준과 권한 최소화 모델로 설명해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: WASM 시스템 인터페이스
- 배경: 서버사이드 WASM은 파일, 시간, 난수, 네트워크 같은 시스템 기능이 필요하지만 sandbox 경계를 유지해야 한다.
- 필요성: WASI capability API로 preopen directory, env, clock, random 등 필요한 자원만 명시 허용한다.

---

## Ⅱ. 구조 및 구성요소

```text
WASM Module -> WASI API -> Runtime Implementation -> Host OS Resource
  / Capability: preopen dir, env, clock, random
  / Control: policy, signing, audit
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| WASI API | 표준 시스템 호출 인터페이스 | 파일, clock, random, socket |
| Runtime | WASI 구현과 권한 검사 | Wasmtime, WasmEdge |
| Capability | 자원 접근 허용 범위 | preopen directory, env allowlist |
| Component Model | module 간 인터페이스 조합 | Preview 2와 연계 |

> 요약: WASI는 WASM module과 Host OS 사이에 runtime이 구현하는 capability 기반 시스템 API 계층임.

---

## Ⅲ. 동작원리 및 흐름도

```text
module 실행 요청 -> capability 설정 -> runtime load -> WASI call 발생 -> 권한 검사 -> host resource 접근 -> audit 기록
  / 권한 없음 -> deny
  / API 미지원 -> trap/error
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 실행 전 directory, env, network capability 설정 | 허용 목록 승인 |
| 2 | runtime이 module을 load하고 WASI import 연결 | import resolution 100% |
| 3 | module이 WASI API 호출 | call count, error rate |
| 4 | runtime이 capability와 policy 검사 | deny event 기록 |
| 5 | host OS resource 접근 후 결과 반환 | audit log 보관 |

> 요약: WASI는 실행 전 부여된 capability만 검사해 host resource 접근을 허용함.

---

## Ⅳ. 특징

| 구분 | POSIX 직접 노출 | WASI | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 권한 | OS API 범위 넓음 | capability 기반 허용 | preopen dir 최소화 |
| 이식성 | OS별 차이 | runtime API 표준화 | runtime 2종 이상 검증 |
| 보안 | 접근 경계 넓음 | sandbox 유지 | deny event 추적 |
| 성숙도 | 생태계 풍부 | Preview별 차이 | Preview 1/2 지원 확인 |

> 요약: WASI는 이식성과 권한 최소화를 제공하지만 Preview 버전과 runtime 지원 범위를 확인해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | host API 직접 구현 | WASI 표준 API | WASM runtime 이식성 필요 |
| 비용/처리 | runtime별 custom binding | 표준 import | 개발 언어 2종 이상 |
| 운영/위험 | 권한 범위 불명확 | capability 명시 | 보안 감사 요구 업무 |

> 요약: 여러 runtime과 언어를 쓰는 서버사이드 WASM은 WASI를 기준 인터페이스로 삼아야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| API 불일치 | Preview와 runtime 차이 | 호환성 매트릭스, conformance test | API error rate |
| 권한 과다 | 넓은 preopen directory | 최소 directory, env allowlist | 허용 capability 수 |
| 감사 누락 | host call 추적 부재 | runtime audit, OTLP log | audit event coverage |

> 요약: WASI 리스크는 API 호환, capability 과다, host call 감사로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 호환성 | 대상 runtime 2종 통과 | conformance test |
| 권한 | 미사용 capability 0건 | policy review |
| 보안 | deny event 100% 기록 | runtime audit log |

> 요약: WASI 품질은 runtime 호환성, capability 최소화, 감사 기록으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 인터페이스 기준화: Wasmtime과 WasmEdge에서 Preview 1/2 지원 범위를 확인하고 WASI API 사용 목록을 문서화
2. 권한 최소화: preopen directory를 `/input`, `/output`처럼 업무별로 제한하고 env, clock, random 권한을 allowlist로 관리
3. 감사 체계 구성: WASI call, deny event, trap error를 OTLP log로 수집하고 module 서명 검증을 배포 조건으로 설정

**결론 (2줄):**
- 기술사 판단: 서버사이드 WASM이 파일·시간·네트워크 등 시스템 기능을 요구하면 WASI를 적용하고, POSIX 전체 의존 업무는 컨테이너를 선택함
- 향후 방향: WASI Preview 2와 component model이 WASM module 이식성과 권한 모델의 표준 축이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WASI를 설명하시오", "기술하시오" | capability 설정과 WASI call 흐름 | POSIX 직접 노출 대비 권한·이식성 |
| 요구사항 명시형 | "WASM 실행 보안을 설계하시오", "비교하시오" | preopen, host call, audit 설계 | runtime 호환과 최소 권한 기준 |

> 요약: 설명형은 표준 인터페이스, 보안형은 capability와 감사 체계 중심으로 전환함.
