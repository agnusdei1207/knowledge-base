---
title: "OpenAPI·Swagger (OpenAPI Swagger)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 204
---

# 📖 【암기용】 개념 완전 이해

> 목적: OpenAPI와 Swagger를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: OpenAPI(구 Swagger Specification)는 REST API의 엔드포인트·요청·응답·인증 방식을 사람과 기계가 함께 읽을 수 있는 **API 명세(Specification)**로 정의하는 표준이다.
- **왜 필요한가**: 코드가 바뀌어도 문서는 그대로인 경우가 흔하다. 문서와 실제 동작이 어긋나면 클라이언트 개발자는 잘못된 문서를 믿고 코드를 짜고, 그 불일치는 운영 장애로 이어진다. OpenAPI는 문서 자체를 기계가 검증 가능한 파일로 만들어 이 어긋남을 CI에서 잡아낸다.
- **핵심 직관**: 건축 설계도면과 같다. 시공사(구현), 감리(테스트), 자재 산출(SDK 생성)이 모두 같은 도면 한 장을 근거로 움직이면 서로 다른 말을 할 수 없다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| API 명세 (Specification) | API 구조를 사람·기계가 함께 읽는 형식으로 고정한 것 — OpenAPI가 만드는 결과물 | 건축 설계도면 |
| OpenAPI Specification (OAS) | 표준 자체의 정식 명칭(현재 버전 3.x) | 도면 규격(표준 규격서) |
| Swagger | OAS의 옛 명칭이자, 지금은 관련 도구 모음(Swagger UI 등)의 브랜드명 | 예전 회사명이 남은 상표 |
| paths | URI와 HTTP 메서드별로 어떤 요청·응답이 오가는지 정의하는 최상위 블록 | 도면 위 각 방의 출입구 표시 |
| operationId | 각 API 동작에 붙는 고유 이름, SDK 메서드명으로 그대로 쓰임 | 방마다 붙은 고유 호실 번호 |
| components/schemas | 요청·응답에서 반복되는 데이터 구조를 정의해 재사용 | 표준 부품 도면(문·창문 규격) |
| securitySchemes | API Key, OAuth2, OIDC 등 인증 방식을 명세에 선언 | 출입 통제 방식 표기 |
| JSON Schema | schemas가 실제로 따르는 데이터 검증 문법(타입·필수값·형식) | 부품 치수 허용오차 규격 |
| Swagger UI | 명세 파일을 읽어 웹에서 클릭해볼 수 있는 문서 화면으로 렌더링하는 도구 | 도면을 입체로 보여주는 뷰어 |
| Mock Server | 명세만으로 가짜 응답을 돌려주는 서버 — 구현 전 클라이언트 개발 가능 | 완공 전 모델하우스 |
| Codegen (SDK 생성) | 명세에서 클라이언트 SDK·서버 스텁 코드를 자동 생성 | 도면에서 자재 발주서를 뽑아냄 |
| Contract Test | 실제 API 응답이 명세와 일치하는지 자동 검증 | 준공 시 도면대로 지어졌는지 감리 |
| Breaking Change | 기존 소비자를 깨뜨리는 명세 변경(필드 삭제·타입 변경 등) | 이미 지은 문의 위치를 바꾸는 것 |

## 깊이 이해

### 왜 필요했나 — 문서와 코드가 갈라지는 문제
- API가 수십 개로 늘어나면 담당자가 바뀌고, 급한 배포에 문서 갱신이 밀리는 일이 반복된다. 그 결과 "문서엔 선택값인데 실제론 필수", "문서엔 없는 필드가 응답에 나옴" 같은 불일치가 쌓인다.
- OpenAPI의 해법은 문서를 사람이 나중에 쓰는 글이 아니라, YAML/JSON 파일 자체를 유일한 원천(single source of truth)으로 두는 것이다. 이 파일에서 문서·mock·SDK·테스트를 모두 자동 생성하면, 파일이 곧 진실이 되어 따로 갱신할 대상이 사라진다.

### 명세 구조를 실제 조각으로 이해하기
- 예를 들어 `/orders/{id}` GET을 정의한다면, `paths./orders/{id}.get`에 `parameters`(id는 path의 정수), `responses.200`(주문 정보 schema), `responses.404`(주문 없음 schema)를 각각 선언한다.
- 이때 200 응답의 schema는 `components/schemas/Order`를 `$ref`로 참조해 재사용한다 — 주문 정보가 다른 API 5곳에서도 쓰인다면, 필드 하나를 바꿀 때 정의를 5번이 아니라 1번만 고치면 된다.
- CI 파이프라인은 실제 서버가 돌려준 응답 JSON을 이 schema로 검증한다. 만약 실제 응답에 명세에 없는 `internalNote` 필드가 섞여 나오면, contract test가 실패해 배포를 막는다 — 이것이 "문서가 코드를 감시"하는 방식이다.

### Swagger와 OpenAPI를 구분하는 판별 원리
- 흔히 "Swagger로 문서 짠다"고 말하지만, 표준의 정식 이름은 OpenAPI Specification이다. Swagger는 2010년대 초 이 명세를 처음 만든 회사·도구의 이름이었고, 2015년 명세 자체가 Linux Foundation 산하 OpenAPI Initiative로 넘어가며 표준 명칭이 OpenAPI로 바뀌었다. Swagger UI, Swagger Codegen 같은 도구 이름에만 옛 이름이 남아있다.
- 판별: "이 파일(.yaml/.json)이 API 구조를 정의하는가?" → OpenAPI 명세. "이 화면(UI)이 명세를 보여주는가?" → Swagger UI(도구).

### 비유와 흔한 오해
- **비유**: 설계도면 하나로 시공(구현)·감리(contract test)·모델하우스(mock server)·자재발주서(SDK)를 전부 뽑아내는 구조다. 도면이 틀리면 그 오류가 모든 산출물에 그대로 퍼지므로, 도면(명세) 품질 자체를 CI에서 lint로 관리한다.
- **오해**: "OpenAPI 파일을 만들면 문서화가 끝났다"고 여기는 것. 파일이 실제 코드와 어긋나지 않게 유지하려면 PR마다 diff 검증, breaking change 탐지, contract test 같은 지속적 통제가 필요하다 — 문서 생성은 시작일 뿐이다.

## 연결 개념
- Contract Test — 명세와 실제 구현 응답의 일치 여부를 자동 검증하는 절차
- API Gateway — OpenAPI 명세를 기반으로 라우팅·인가·요청 검증을 수행
- REST — OpenAPI가 주로 다루는 API 스타일(gRPC는 .proto로 별도 관리)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: OpenAPI는 문서 작성 도구가 아니라 API 계약을 설계·검증·배포 파이프라인에 연결하는 표준이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OpenAPI는 REST API의 endpoint, request, response, security를 YAML/JSON으로 정의하는 명세이다.
> 2. **가치**: 문서, mock, SDK, contract test, gateway validation을 하나의 계약에서 생성한다.
> 3. **판단 포인트**: API-first, schema versioning, breaking change check, 보안 스키마 관리가 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| API 계약 관리 이해 확인 | paths, components, schema, securitySchemes | Swagger UI 화면만 설명 |
| 개발 프로세스 적용 확인 | API-first, mock, codegen, contract test | 문서와 코드 불일치 통제 누락 |
| 운영·보안 연계 확인 | gateway validation, auth scheme, versioning | 인증 방식·breaking change 검증 누락 |

> 요약: 이 문제는 API 문서화가 아니라 계약 기반 개발과 배포 통제 체계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: REST API 계약 명세 표준
- 배경: API 수가 늘면 문서·코드·테스트가 분리되어 장애와 재작업이 발생한다.
- 필요성: OpenAPI Spec을 단일 원천으로 두고 Swagger UI, mock, SDK 생성, contract test 기준을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
OpenAPI Spec -> Swagger UI / Mock Server / SDK Generation / Contract Test
             -> API Gateway Validation -> Runtime Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| paths | URI, method, operation 정의 | operationId로 SDK 메서드 생성 |
| components | schema, parameter, response 재사용 | JSON Schema 기반 |
| securitySchemes | API Key, OAuth2, OIDC 정의 | scope와 권한 연계 |
| tooling | UI, codegen, mock, lint | CI 품질 게이트 적용 |

> 요약: OpenAPI는 명세 파일을 중심으로 문서화, 생성, 검증, 운영 정책을 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
API 설계 -> OpenAPI 작성 -> Lint/Review -> Mock/SDK 생성 -> 구현 -> Contract Test -> 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API-first로 path·schema 정의 | spectral lint error 0건 |
| 2 | mock server와 SDK 생성 | consumer 개발 착수 가능 |
| 3 | 구현 후 request·response 검증 | contract test pass 100% |
| 4 | gateway에 schema·auth 정책 반영 | invalid request 차단 로그 |

> 요약: OpenAPI는 설계 단계에서 만든 계약을 구현·테스트·게이트웨이 검증까지 이어가는 흐름이다.

---

## Ⅳ. 특징

| 구분 | 수기 API 문서 | OpenAPI | 판단 포인트 |
|:---|:---|:---|:---|
| 문서 | 사람이 직접 갱신 | spec에서 UI 생성 | 문서 최신성 CI 검증 가능 |
| 계약 | 구현 후 확인 | 설계 시 schema 고정 | API-first 조직에 적합 |
| 테스트 | 개별 테스트 작성 | contract test 자동화 | 배포 전 breaking change 탐지 |
| 보안 | 별도 정책 문서 | securitySchemes 명세 | OAuth2 scope·JWT 검증 연결 |

> 요약: OpenAPI는 API 계약을 명세화해 문서와 테스트의 불일치 비용을 줄인다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Wiki 문서 | OAS YAML/JSON | API 30개 이상 또는 외부 소비자 존재 |
| 비용/성능 | 수동 SDK 작성 | codegen·mock 자동화 | SDK 생성으로 클라이언트 작업 2일 이상 절감 |
| 운영/위험 | 배포 후 오류 발견 | CI contract gate | breaking change 허용률 0건 목표 |

> 요약: OpenAPI는 API 소비자가 많고 변경 통제가 필요한 조직에서 계약 원천으로 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 문서 불일치 | 코드 변경 후 spec 미갱신 | CI diff check, contract test | spec drift 0건 |
| 스키마 과소 정의 | `object` 남용 | required, enum, format 명시 | schema coverage 90% 이상 |
| 보안 누락 | securitySchemes 미정의 | OAuth2/OIDC scope 명세 | unauthenticated operation 0개 |

> 요약: 주요 리스크는 spec drift, 느슨한 schema, 보안 정의 누락이며 CI 품질 게이트로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 계약 품질 | lint error 0건 | Spectral, Redocly |
| 호환성 | breaking change 0건 | openapi-diff |
| 운영 검증 | contract test pass 100% | CI pipeline |

> 요약: OpenAPI 품질은 lint, diff, contract test 결과로 객관화한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. API-first 원칙으로 PR에 OpenAPI diff를 포함하고 breaking change는 major version 승인 절차로 분리함.
2. Spectral lint, schema coverage 90% 이상, contract test 100% pass를 CI 배포 조건으로 설정함.
3. API Gateway에 OpenAPI 기반 request validation, OAuth2 scope 검증, rate limit 정책을 연결함.

**결론 (2줄):**
- 기술사 판단: 외부 소비자와 다중 클라이언트가 있으면 OpenAPI를 계약 원천으로 두고, 내부 고빈도 RPC는 gRPC proto를 병행함.
- 향후 방향: OpenAPI는 platform engineering의 API catalog, developer portal, contract governance로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OpenAPI를 설명하시오" | 설계, lint, mock, test, gateway 흐름 | 수기 문서 대비 계약 관리 차이 |
| 요구사항 명시형 | "API 품질 방안을 제시하시오", "Swagger와 비교하시오" | CI 계약 검증, diff, 보안 스키마 | 리스크 대응, versioning, 품질 지표 |

> 요약: 설명형은 명세 구조, 방안형은 API 계약 품질 게이트와 운영 검증으로 목차를 바꾼다.
