---
title: "API 버저닝 전략 (API Versioning)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 205
---

# 📖 【암기용】 개념 완전 이해

> 목적: API 버저닝 전략을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: API 변경 시 기존 소비자와 신규 요구를 함께 수용하기 위한 호환성 관리 전략
- **왜 필요한가**: API는 한 번 공개되면 여러 클라이언트가 동시에 의존한다. 응답 필드 삭제, 의미 변경, 인증 방식 변경은 기존 앱 장애로 이어질 수 있다.
- **핵심 직관**: 도로 공사 때 기존 차선을 바로 없애지 않고 우회로·공사 일정·표지판을 제공하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 서버는 빠르게 바꾸고 싶지만 모바일 앱·파트너 시스템은 즉시 배포되지 않는다. API 버저닝은 변경 속도와 소비자 호환성의 충돌을 관리한다.
- **작동 원리**: URI, Header, Query, Media Type 중 하나로 버전을 표현하고, semantic versioning, deprecation policy, sunset header, contract test로 변경을 통제한다.
- **비유**: 새 교과서가 나와도 기존 수험생은 일정 기간 기존 교재로 시험을 볼 수 있게 공지하는 구조임.
- **구체 예시**: `/api/v1/orders`의 `status` 필드 의미를 바꿔야 하면 `/api/v2/orders`를 추가하고 v1은 6개월 deprecation 공지 후 호출량 1% 이하에서 종료함.
- **흔한 오해·주의점**: 버전을 많이 늘리는 것이 해결책은 아니다. additive change는 같은 major에서 처리하고, breaking change만 major version으로 분리해야 한다.

## 연결 개념
- OpenAPI — breaking change 탐지와 계약 명세
- Consumer-Driven Contract — 소비자 관점 호환성 검증
- API Gateway — 버전 라우팅·종료 정책 적용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 수치·표준명·비교축으로 작성한다.
> 핵심: API 버저닝은 URL 표기 문제가 아니라 변경 영향 분석, 호환성 정책, 폐기 절차를 묶은 거버넌스이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 버저닝은 API 계약 변경을 소비자 호환성 범위 안에서 배포·운영하는 전략이다.
> 2. **가치**: breaking change로 인한 클라이언트 장애를 줄이고, 신규 기능과 기존 연동을 병행한다.
> 3. **판단 포인트**: URI·Header·Media Type 방식, deprecation 기간, contract test, 호출량 기반 sunset 기준을 함께 정해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| API 변경관리 역량 확인 | backward compatibility, breaking change, deprecation | `/v1` 표기 방식만 나열 |
| 설계 대안 비교 확인 | URI, header, query, media type versioning | 소비자 유형별 선택 기준 누락 |
| 운영 거버넌스 확인 | sunset header, 호출량 모니터링, contract test | 구버전 종료 절차와 공지 기간 누락 |

> 요약: 이 문제는 버전 위치보다 변경 영향 통제와 종료 기준을 요구한다.

---

## Ⅰ. 개요 및 필요성

API 버저닝은 API 계약 변경의 호환성을 관리하는 전략이다. API 소비자는 웹, 모바일, 파트너 시스템으로 배포 주기가 다르다. 버전 정책은 신규 기능 배포와 기존 소비자 보호를 동시에 만족시키는 변경관리 체계이다.

---

## Ⅱ. 구조 및 구성요소

```text
API Change -> Compatibility Analysis -> Version Policy -> Gateway Routing -> Deprecation/Sunset
                         +-> OpenAPI Diff / Contract Test / Usage Metric
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Version Identifier | URI, header, query, media type으로 버전 표시 | 외부 API는 URI 방식 인지성 높음 |
| Compatibility Rule | additive와 breaking change 구분 | 필드 삭제·타입 변경은 breaking |
| Deprecation Policy | 구버전 공지·지원 기간 정의 | 3~6개월 이상 공지 권장 |
| Observability | 버전별 호출량·오류율 측정 | sunset 판단 근거 |

> 요약: API 버저닝은 표기 방식, 호환성 규칙, 폐기 정책, 관측 지표로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
변경 요청 -> OpenAPI Diff -> 호환성 판정 -> 버전 생성/유지 -> 배포 -> 호출량 확인 -> 종료
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API 변경 요청과 영향 범위 식별 | consumer 목록 100% 확인 |
| 2 | OpenAPI diff로 breaking 여부 판정 | breaking change 0건 또는 major 분리 |
| 3 | gateway에서 버전별 라우팅 적용 | v1/v2 라우팅 오류 0건 |
| 4 | deprecation 공지 후 sunset 실행 | 구버전 호출량 1% 이하 |

> 요약: 버저닝은 변경 식별, 호환성 판정, 병행 운영, 호출량 기반 종료 순서로 통제한다.

---

## Ⅳ. 특징

| 구분 | URI Versioning | Header Versioning | Media Type Versioning |
|:---|:---|:---|:---|
| 예시 | `/v1/orders` | `X-API-Version: 1` | `application/vnd.company.v1+json` |
| 장점 | 가시성·라우팅 단순 | URL 유지 | REST content negotiation 정합 |
| 한계 | 리소스 URI 오염 | 캐시·디버깅 주의 | 클라이언트 구현 부담 |
| 적용 | 외부 공개 API | 내부·파트너 API | 엄격한 REST 조직 |

> 요약: 외부 API는 URI 방식, 내부 API는 Header 방식, 표준 지향 API는 Media Type 방식을 우선 검토한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 무버전 API | 명시 버전 API | 소비자 2개 이상, 배포 주기 상이 |
| 비용/성능 | 단일 코드 경로 | 버전별 라우팅·테스트 증가 | 구버전 유지 비용 월 1인일 이상이면 종료 계획 필요 |
| 운영/위험 | 즉시 변경 | deprecation·sunset | 파트너 SLA와 공지 기간 연계 |

> 요약: 버전은 소비자 보호 비용이 구버전 유지 비용보다 클 때 도입하고, 종료 기준을 함께 정의한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 버전 난립 | minor 변경도 major 생성 | semantic versioning, additive rule | 활성 major 2개 이하 |
| 소비자 장애 | breaking change 미탐지 | openapi-diff, contract test | 배포 후 4xx 증가율 5% 이하 |
| 종료 실패 | 호출 소비자 미확인 | API key별 usage 분석, sunset header | 구버전 호출량 1% 이하 |

> 요약: 버저닝 리스크는 난립, 미탐지 변경, 종료 실패이며 계약 검증과 사용량 분석으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 호환성 | breaking change 0건 | OpenAPI diff |
| 운영 | 활성 major version 2개 이하 | API catalog |
| 종료 | sunset 대상 호출량 1% 이하 | gateway access log |

> 요약: API 버전 정책은 호환성, 활성 버전 수, 구버전 호출량으로 관리한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. API 변경을 additive, compatible, breaking으로 분류하고 breaking change는 major version과 승인 절차를 요구함.
2. OpenAPI diff, consumer-driven contract, gateway canary 5% 트래픽으로 배포 전후 호환성을 검증함.
3. `Deprecation`·`Sunset` header, 6개월 공지, API key별 호출량 리포트로 구버전 종료를 수행함.

**결론 (2줄):**
- 기술사 판단: 외부 공개 API는 URI major version과 명확한 sunset 정책, 내부 API는 header version과 contract test를 선택함.
- 향후 방향: API catalog와 schema registry를 결합해 버전 변경을 플랫폼 거버넌스로 자동 통제함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "API 버저닝을 설명하시오" | 변경 판정, 라우팅, 종료 흐름 | URI·Header·Media Type 비교 |
| 요구사항 명시형 | "버저닝 전략을 제시하시오", "방안을 수립하시오" | OpenAPI diff, contract test, sunset 절차 | 선택 기준, 리스크, 운영 지표 |

> 요약: 설명형은 방식 비교, 방안형은 변경관리 프로세스와 종료 기준 중심으로 목차를 전환한다.
