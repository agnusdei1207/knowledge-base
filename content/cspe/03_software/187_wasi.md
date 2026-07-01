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
- **개요**: WebAssembly가 서버와 엣지에서 파일, 시간, 네트워크 같은 시스템 기능을 제한적으로 호출하도록 정의한 인터페이스
- **왜 필요한가**: WASM module은 기본적으로 sandbox 안에 갇혀 있어 외부 파일, 환경 변수, 네트워크 사용을 표준 방식으로 허용해야 한다.
- **핵심 직관**: WASM에게 집 열쇠를 통째로 주지 않고, 필요한 방의 출입증만 발급하는 규칙이다.

## 깊이 이해
- **배경·문제의식**: 브라우저 밖 WASM은 OS와 상호작용해야 하지만, POSIX 전체를 열면 sandbox 장점이 사라진다. WASI는 capability 기반으로 필요한 자원만 명시 허용한다.
- **작동 원리**: runtime은 WASI API를 구현하고, module은 사전 허용된 directory, clock, random, socket 등 capability만 호출한다. Preview 2와 component model은 인터페이스 조합성을 높인다.
- **비유**: 호텔 투숙객에게 마스터키 대신 객실, 헬스장, 조식권처럼 필요한 권한만 카드에 담아 주는 방식이다.
- **구체 예시**: 이미지 변환 WASM module에 `/input`, `/output` directory만 preopen하고 네트워크 권한을 주지 않으면 파일 변환은 가능하지만 외부 전송은 차단된다.
- **흔한 오해·주의점**: WASI는 WASM runtime 자체가 아니다. Wasmtime, WasmEdge 같은 runtime이 WASI API를 구현하고, 지원 범위는 runtime과 버전에 따라 달라진다.

## 연결 개념
- WebAssembly Server-side - WASI가 필요한 실행 환경
- Capability Security - 명시 허용 권한 모델
- Component Model - WASM module 간 인터페이스 조합 방식

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

WASI는 WASM 시스템 인터페이스임. 서버사이드 WASM은 파일, 시간, 난수, 네트워크 같은 시스템 기능이 필요하지만 sandbox 경계를 유지해야 한다. WASI는 capability 기반 API로 필요한 자원만 명시 허용한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
