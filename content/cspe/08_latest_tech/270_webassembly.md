---
title: "WebAssembly (WebAssembly)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 270
extra:
  question_no: "270"
  exam_status: "기출"
  exam_history: "136회"
  exam_note: "전망"
---

## 미리 알고가기

- WebAssembly는 웹 브라우저뿐 아니라 서버와 엣지에서도 실행되는 바이너리 명령 형식과 런타임 모델임
- 네이티브에 가까운 성능과 이식성과 샌드박스를 함께 추구하는 것이 핵심 가치임
- 컨테이너를 대체한다기보다 더 가벼운 격리 실행 단위로 보는 편이 정확함

## Ⅰ. 개요

- **정의/개념**: WebAssembly는 다양한 언어로 작성된 코드를 안전하고 이식성 있게 실행하기 위한 바이너리 명령 형식과 런타임 표준으로 브라우저와 서버와 엣지에서 경량 샌드박스 실행을 지원함
- **배경/필요성**: 웹 환경에서 고성능 코드를 안전하게 실행하려는 요구에서 출발했지만 이후 서버리스와 플러그인과 엣지 컴퓨팅으로 활용 범위가 확대됨

## Ⅱ. 특징

- 바이너리 형식이라 로딩과 실행 효율이 높음
- 샌드박스 기반 격리로 안전한 확장 실행 모델을 제공함
- 언어 독립성과 높은 이식성으로 다양한 런타임에 배치 가능함
- 시스템 호출과 장기 프로세스 제어는 컨테이너보다 제약이 많을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | WebAssembly | Native Binary | Container |
|:---|:---|:---|:---|
| 이식성 | 높음 | 낮음 | 높음 |
| 격리 단위 | 경량 샌드박스 | OS 의존 | 프로세스와 네임스페이스 |
| 시작 속도 | 매우 빠름 | 빠름 | 상대적으로 느림 |
| 시스템 접근성 | 제한적 | 매우 높음 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Wasm Module | 컴파일된 바이너리 코드와 메타 정보를 포함한 실행 단위로 다양한 환경에 배포할 수 있음 |
| Runtime Engine | Wasmtime 같은 엔진이 모듈 검증과 실행과 샌드박스를 담당하는 핵심 런타임임 |
| Host Interface | 파일과 네트워크와 시간 같은 외부 기능을 제한적으로 노출해 모듈이 안전하게 호스트와 상호작용하게 함 |
| Sandbox Boundary | 메모리와 권한을 격리해 악성 또는 오류 코드의 영향 범위를 줄이는 보안 경계임 |
| Packaging and Distribution | 모듈 버전과 의존성을 관리해 브라우저와 서버와 엣지에 일관되게 배포하는 유통 계층임 |

```text
+-------------+    +----------------+    +------------------+
| Wasm Module | -> | Runtime Engine | -> | Host Interface   |
+-------------+    +----------------+    +------------------+
                         |
                         v
                  +---------------+
                  | Sandbox       |
                  +---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 소스 컴파일   | -> | 모듈 배포    | -> | 런타임 로딩  | -> | 샌드박스 실행 | -> | 결과 반환    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **소스 컴파일**: 다양한 언어 코드를 Wasm 모듈로 컴파일함
2. **모듈 배포**: 모듈을 브라우저나 서버나 엣지로 전달함
3. **런타임 로딩**: 엔진이 모듈을 검증하고 메모리를 준비함
4. **샌드박스 실행**: 제한된 인터페이스 안에서 코드를 수행함
5. **결과 반환**: 호스트 시스템과 필요한 결과를 교환함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 시스템 호출과 네트워크 접근이 제한적이라 기존 네이티브 애플리케이션을 그대로 옮기면 기능 공백이 생길 수 있음
   - 해결방안: host capability design과 WASI compatibility review를 적용하고 unsupported syscall count와 porting completion rate로 검증함
2. 문제: 모듈 배포는 가볍지만 디버깅과 성능 프로파일링 도구가 부족하면 운영 문제 분석이 늦어질 수 있음
   - 해결방안: runtime observability tooling과 benchmark profile pipeline을 적용하고 profiling coverage와 mean time to diagnose로 검증함
3. 문제: 샌드박스가 가볍다는 이유만으로 무분별하게 확장 실행에 쓰면 권한 경계와 공급망 검증이 약해질 수 있음
   - 해결방안: signed module policy와 least capability interface를 적용하고 unsigned module rejection rate와 runtime policy violation count로 검증함

## Ⅶ. 적용 사례

- 엣지 컴퓨팅 플랫폼이 WASI 호환성 검토를 수행하며 확인 지표는 unsupported syscall count와 porting completion rate임
- 서버리스 런타임이 성능 프로파일 파이프라인을 운영하며 확인 지표는 profiling coverage와 mean time to diagnose임
- 확장 플러그인 시스템이 서명 모듈 정책을 적용하며 확인 지표는 unsigned module rejection rate와 runtime policy violation count임

## Ⅷ. 결론

WebAssembly는 경량 격리 실행의 유력한 공통 포맷이지만 호스트 인터페이스와 운영 도구와 공급망 정책까지 포함한 생태계 설계가 필요함.
