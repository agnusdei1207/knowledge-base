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
- **개요**: REST API 계약을 기계가 읽을 수 있는 문서로 정의하는 표준과 도구 생태계
- **왜 필요한가**: API 문서가 코드와 달라지면 클라이언트 개발, 테스트, 운영 장애 분석이 지연된다. OpenAPI는 경로·메서드·파라미터·응답·보안을 계약으로 고정한다.
- **핵심 직관**: API의 설계도면을 YAML/JSON으로 만들고, 문서·테스트·SDK를 같은 도면에서 생성하는 방식이다.

## 깊이 이해
- **배경·문제의식**: REST API가 증가하면 문서 누락, 응답 예시 불일치, breaking change 탐지가 어려워진다.
- **작동 원리**: OpenAPI Specification에 `paths`, `components`, `securitySchemes`, `responses`를 정의하고 Swagger UI, codegen, mock server, contract test가 이를 활용한다.
- **비유**: 건물 시공 전에 도면을 만들고, 감리·자재 산출·완공 검사를 같은 도면으로 수행하는 구조임.
- **구체 예시**: `/orders/{id}`의 200·404 응답 schema를 정의하면 CI에서 실제 API 응답이 schema와 다른 경우 배포를 차단할 수 있음.
- **흔한 오해·주의점**: Swagger는 표준 자체가 아니라 도구 이름으로 쓰이는 경우가 많다. 표준 명칭은 OpenAPI Specification이며, 문서 생성만으로 계약 관리가 완성되지 않는다.

## 연결 개념
- Contract Test — API 제공자·소비자 계약 검증
- API Gateway — OpenAPI 기반 라우팅·인가·검증 적용
- REST — OpenAPI의 주된 기술 대상

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

OpenAPI는 REST API 계약 명세 표준이다. API 수가 늘면 문서·코드·테스트가 분리되어 장애와 재작업이 발생한다. OpenAPI는 계약을 단일 원천으로 두고 문서, mock, SDK, 검증을 자동화한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
