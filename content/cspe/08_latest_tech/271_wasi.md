---
title: "WASI 웹어셈블리 시스템 인터페이스 (WebAssembly System Interface)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 271
extra:
  question_no: "271"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- WASI는 WebAssembly 모듈이 브라우저 밖에서 운영체제 기능을 안전하게 쓰도록 정의한 표준 인터페이스임
- 핵심 목적은 Wasm의 이식성과 샌드박스를 유지하면서 파일과 네트워크 같은 호스트 기능을 연결하는 데 있음
- WebAssembly 자체가 실행 형식이라면 WASI는 그 실행 환경의 시스템 호출 규약에 가까움

## Ⅰ. 개요

- **정의/개념**: WASI는 WebAssembly 모듈이 파일과 시계와 환경 변수와 네트워크 같은 호스트 시스템 자원에 제한적으로 접근하도록 표준화한 시스템 인터페이스임
- **배경/필요성**: WebAssembly를 서버와 엣지와 플러그인 환경으로 확장하려면 브라우저 밖 실행에서도 안전하면서 이식 가능한 시스템 접근 규약이 필요해짐

## Ⅱ. 특징

- capability 기반 접근 모델로 최소 권한 실행을 지향함
- 운영체제별 차이를 추상화해 Wasm 이식성을 높임
- 네이티브 시스템 호출보다 제약이 있어 보안과 휴대성이 높음
- 호스트 기능 범위와 표준 성숙도에 따라 실제 활용 가능성이 달라짐

## Ⅲ. 종류 및 비교

| 판단 기준 | WASI | Native POSIX API | Browser Sandbox API |
|:---|:---|:---|:---|
| 실행 대상 | Wasm 런타임 | 네이티브 바이너리 | 브라우저 스크립트 |
| 권한 모델 | capability 기반 | OS 권한 기반 | 브라우저 정책 기반 |
| 이식성 | 높음 | 낮음 | 중간 |
| 시스템 접근성 | 제한적 | 매우 높음 | 제한적 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Wasm Module | WASI 인터페이스를 호출하는 실행 대상 코드로 샌드박스 내부에서 동작함 |
| Runtime Engine | Wasm 모듈 검증과 실행을 담당하고 호스트 기능을 WASI 규격에 따라 중개하는 런타임임 |
| Capability Handle | 모듈이 접근 가능한 파일과 디렉터리와 자원 범위를 명시해 권한 경계를 만드는 접근 토큰임 |
| WASI API Surface | 파일 입출력과 시간과 환경 변수 같은 호스트 기능을 표준화된 함수 집합으로 제공하는 인터페이스 계층임 |
| Host Environment | 실제 OS 자원을 보유하되 런타임을 통해 제한적으로만 노출하는 호스트 시스템임 |

```text
+-------------+    +---------------+    +------------------+
| Wasm Module | -> | WASI Runtime  | -> | Host Environment |
+-------------+    +---------------+    +------------------+
        |                  |
        v                  v
   Capability use     API mediation
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 모듈 배포    | -> | 권한 부여    | -> | WASI 호출    | -> | 런타임 중개  | -> | 제한된 결과 반환 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **모듈 배포**: Wasm 모듈을 런타임에 배치함
2. **권한 부여**: 허용된 디렉터리와 환경을 capability로 설정함
3. **WASI 호출**: 모듈이 파일과 시간 등 시스템 기능을 요청함
4. **런타임 중개**: 런타임이 요청을 검증하고 호스트에 전달함
5. **제한된 결과 반환**: 허용 범위 내 결과만 모듈에 돌려줌

## Ⅵ. 문제점 및 해결 방안

1. 문제: WASI가 제공하는 시스템 기능 범위가 제한적이면 복잡한 네이티브 애플리케이션을 그대로 옮기기 어려울 수 있음
   - 해결방안: capability aware refactoring과 compatibility assessment를 적용하고 unsupported interface count와 porting completion rate로 검증함
2. 문제: 런타임별 WASI 지원 편차가 크면 같은 모듈이라도 실행 환경마다 동작 차이가 발생할 수 있음
   - 해결방안: conformance test suite와 runtime qualification policy를 적용하고 cross runtime compatibility rate와 deployment defect rate로 검증함
3. 문제: 권한 설계가 느슨하면 샌드박스 장점이 약해지고 호스트 자원 노출 범위가 불필요하게 커질 수 있음
   - 해결방안: least capability grant와 runtime policy audit를 적용하고 excessive capability count와 policy violation incident rate로 검증함

## Ⅶ. 적용 사례

- 엣지 Wasm 플랫폼이 포팅 적합성 검토를 수행하며 확인 지표는 unsupported interface count와 porting completion rate임
- 멀티런타임 환경이 적합성 테스트를 운영하며 확인 지표는 cross runtime compatibility rate와 deployment defect rate임
- 플러그인 실행 플랫폼이 최소 capability 정책을 적용하며 확인 지표는 excessive capability count와 policy violation incident rate임

## Ⅷ. 결론

WASI는 WebAssembly를 범용 실행 환경으로 확장하는 핵심 규격이므로 이식성만큼 capability 설계와 런타임 적합성 검증이 중요함.
