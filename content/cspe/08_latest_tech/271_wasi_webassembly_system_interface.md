---
title: "WASI 웹어셈블리 시스템 인터페이스 (WebAssembly System Interface)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 271
---

# 📖 【암기용】 개념 완전 이해

> 목적: WASI를 WebAssembly가 브라우저 밖에서 파일, 시간, 난수, 네트워크 같은 시스템 기능을 안전하게 쓰기 위한 표준 인터페이스로 이해하게 만든다.

## 한눈에
- **개요**: Wasm 모듈이 OS 유사 기능을 capability 기반으로 호출하기 위한 표준 API 집합
- **왜 필요한가**: WebAssembly 자체는 계산 포맷에 가깝고 파일·소켓·환경변수 접근을 기본으로 제공하지 않는다.
- **핵심 직관**: 외부 손님에게 건물 전체 열쇠를 주지 않고 필요한 방의 출입증만 발급하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 서버와 엣지에서 Wasm을 실행하려면 파일 입출력, clock, random, network 같은 기능이 필요하지만 무제한 OS 접근은 격리 모델을 깨뜨린다.
- **작동 원리**: WASI runtime은 모듈에 사전 허용된 디렉터리, 환경변수, 네트워크 기능 등을 capability로 제공하고 모듈은 표준 인터페이스를 통해 호출한다.
- **비유**: 호텔 투숙객에게 객실·헬스장 카드만 주고 직원 구역 접근은 막는 권한 모델과 같다.
- **구체 예시**: CLI 도구를 Wasm으로 컴파일하고 WASI runtime에서 `/input` 디렉터리 읽기 권한만 부여해 파일 변환 작업을 수행한다.
- **흔한 오해·주의점**: WASI는 모든 POSIX를 그대로 복제한 것이 아니다. 안전한 이식성을 목표로 하며 runtime별 지원 인터페이스를 확인해야 한다.

## 연결 개념
- WebAssembly — WASI가 시스템 인터페이스를 제공하는 실행 포맷
- Capability-Based Security — 필요한 자원 권한만 부여하는 보안 모델
- Edge Computing — WASI 모듈을 분산 런타임에서 실행하는 활용처

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: WASI는 Wasm 모듈의 시스템 접근을 표준 API와 capability로 제한하는 인터페이스임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WASI는 WebAssembly 모듈이 브라우저 밖에서 시스템 기능을 호출하기 위한 표준 인터페이스 집합임.
> 2. **가치**: 파일, clock, random, network 같은 기능을 capability 기반으로 허용해 sandbox 격리를 유지함.
> 3. **판단 포인트**: runtime별 Preview 지원 범위, capability 설정, interface contract를 확인해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Wasm 시스템 접근 이해 확인 | WASI, capability, runtime, import | Wasm 자체가 OS 접근 제공으로 오기술 |
| 보안 모델 확인 | preopened directory, least privilege | POSIX 무제한 접근으로 설명 |
| 적용 판단 확인 | runtime 지원 범위와 표준 성숙도 | 모든 환경에서 동일 기능 보장 단정 |

> 요약: 이 문제는 Wasm sandbox를 유지하면서 필요한 시스템 기능을 제공하는 표준 인터페이스를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: Wasm 시스템 접근 표준 API
- 배경: WebAssembly는 기본적으로 OS 파일·네트워크 접근을 직접 제공하지 않음.
- 필요성: 서버·엣지에서 Wasm 모듈을 실행하려면 capability 기반 시스템 인터페이스가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Wasm Module -> WASI Import -> WASI Runtime -> Host OS Resource
Policy / Capability -> WASI Runtime -> File / Clock / Random / Network
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Wasm Module | WASI 함수를 import해 호출 | 언어별 WASI target 사용 |
| WASI Runtime | 시스템 호출을 중개 | Wasmtime 등 runtime 구현 |
| Capability | 접근 가능한 자원 범위 정의 | preopen directory, env 허용 |
| Host Resource | 파일·시간·난수·네트워크 제공 | runtime 지원 범위 의존 |

> 요약: WASI는 모듈과 Host OS 사이에 runtime과 capability를 두어 허용된 시스템 기능만 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Wasm 컴파일 -> WASI target 지정 -> runtime 실행
-> capability 설정 -> WASI import 호출 -> host resource 접근
-> 결과 반환 / 접근 거부 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 소스 코드를 WASI target으로 컴파일 | target triple 확인 |
| 2 | runtime에서 허용 자원 설정 | preopen, env, network policy |
| 3 | 모듈이 WASI API 호출 | import resolution |
| 4 | runtime이 권한 확인 후 host 자원 접근 | allow/deny log |

> 요약: WASI는 실행 전에 권한을 부여하고 호출 시 runtime이 capability를 확인해 시스템 접근을 중개한다.

---

## Ⅳ. 특징

| 구분 | POSIX 직접 실행 | WASI 기반 Wasm | 판단 기준 |
|:---|:---|:---|:---|
| 접근 권한 | 프로세스 권한 중심 | capability 기반 명시 허용 | least privilege 요구 |
| 이식성 | OS별 차이 | 표준 API 지향 | runtime 지원 범위 |
| 격리 | OS sandbox 의존 | Wasm sandbox와 runtime 정책 | 멀티테넌트 실행 |
| 기능 범위 | OS 기능 폭넓음 | 표준화된 기능부터 제공 | 필요한 API 존재 여부 |

> 요약: WASI는 POSIX 전체 복제가 아니라 Wasm sandbox에 맞춘 capability 기반 시스템 인터페이스다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | container sandbox | Wasm+WASI runtime | 작은 모듈과 짧은 실행 |
| 비용/성능 | OS 프로세스·이미지 | 모듈 단위 실행 | startup latency |
| 운영/위험 | 컨테이너 권한 관리 | capability 선언 관리 | 필요한 system API |

> 요약: 경량 플러그인과 엣지 함수는 WASI, 복잡한 OS 의존 앱은 컨테이너가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| API 미지원 | runtime별 WASI 구현 차이 | compatibility matrix | import failure |
| 권한 과다 | preopen 범위 과대 | 최소 directory·env 허용 | denied access log |
| 표준 변화 | Preview 버전 차이 | interface version 고정 | runtime upgrade test |

> 요약: WASI 리스크는 API 지원 범위, 권한 설정, 표준 버전 차이며 runtime matrix로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 호환성 | 대상 runtime import 실패 0건 | integration test |
| 권한 | 허용 자원 외 접근 차단 | sandbox test |
| 실행 | startup latency 예산 이내 | runtime metric |

> 요약: WASI 도입은 runtime 호환성, capability 차단, startup latency를 기준으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. CLI, plugin, edge function처럼 파일·시간·난수 등 제한된 API만 필요한 업무를 우선 적용 대상으로 선정함.
2. preopen directory, env, network capability를 manifest로 선언하고 기본값은 deny로 설정함.
3. runtime별 WASI Preview 지원 범위와 upgrade test를 CI에 포함해 import 실패를 사전 탐지함.

**결론 (2줄):**
- 기술사 판단: sandbox와 이식성이 핵심이면 WASI 기반 Wasm을 선택하고, OS 의존성이 큰 서비스는 컨테이너를 선택함.
- 향후 방향: WASI는 Component Model과 결합되어 클라우드·엣지 플러그인의 표준 시스템 인터페이스로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WASI를 설명하시오" | capability 설정과 WASI 호출 흐름 | POSIX·컨테이너 대비 차이 |
| 요구사항 명시형 | "Wasm 기반 플러그인 보안 방안을 제시하시오" | 권한 manifest와 runtime 검증 절차 | API 미지원·권한 과다 리스크 |

> 요약: 설명형은 시스템 인터페이스 구조를, 보안형은 capability와 runtime 호환성 검증을 중심으로 작성한다.
