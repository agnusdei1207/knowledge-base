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
- **개요**: API 버저닝은 API 계약이 바뀔 때 기존 소비자를 깨뜨리지 않도록 **하위 호환성(Backward Compatibility)**을 관리하며 신규 기능을 함께 수용하는 변경관리 전략이다.
- **왜 필요한가**: API는 배포하는 순간 내가 통제할 수 없는 여러 클라이언트(모바일 앱, 파트너 시스템)가 붙는다. 서버만 먼저 바꾸면 아직 옛 버전을 쓰는 클라이언트가 그대로 깨진다.
- **핵심 직관**: 도로 공사와 같다. 기존 차선을 하루아침에 없애지 않고, 우회로(신버전)를 새로 내고 표지판(공지)으로 안내한 뒤, 충분한 기간이 지나야 옛 차선(구버전)을 폐쇄한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 하위 호환성 (Backward Compatibility) | 새 버전이 기존 소비자의 호출 방식을 계속 지원하는 성질 — 버저닝의 핵심 목표 | 옛날 리모컨도 새 TV에서 동작 |
| Breaking Change | 기존 소비자를 깨뜨리는 변경(필드 삭제, 타입 변경, 필수값 추가 등) | 있던 문을 아예 없애버림 |
| Additive Change (호환 변경) | 기존 동작은 그대로 두고 새 필드·엔드포인트만 추가하는 변경 | 방은 그대로 두고 새 방만 증축 |
| Semantic Versioning (SemVer) | `major.minor.patch` 3단 숫자로 변경 성격을 표현하는 규약 | major=구조변경, minor=기능추가, patch=버그수정 |
| URI Versioning | 버전을 경로에 명시(`/v1/orders`) | 건물 층수를 주소에 써둠 |
| Header Versioning | 별도 헤더로 버전 지정(`X-API-Version: 1`) | 주소는 그대로, 카드키에 층수 표시 |
| Media Type Versioning | Accept 헤더의 콘텐츠 타입에 버전 포함(`application/vnd.company.v1+json`) | 우편물 봉투 종류로 처리 부서 구분 |
| Deprecation | 이 버전을 곧 없앨 예정임을 미리 공지하는 상태 | 폐쇄 예정 표지판 |
| Sunset (header) | 정확히 언제 종료되는지 날짜를 못박아 응답에 표시 | 폐쇄 확정일 공고문 |
| Consumer-Driven Contract | 소비자가 실제로 쓰는 필드 기준으로 호환성을 검증하는 테스트 기법 | 세입자 요구사항 기준으로 리모델링 범위 확정 |

## 깊이 이해

### 왜 필요했나 — 변경 속도와 호환성의 충돌
- 서버 팀은 매주 배포하고 싶어하지만, 모바일 앱은 스토어 심사와 사용자 업데이트까지 며칠~몇 주가 걸리고 파트너 시스템은 몇 달씩 바뀌지 않기도 한다. 이 배포 속도 차이를 무시하고 서버 응답 구조를 즉시 바꾸면, 아직 옛 버전을 호출하는 클라이언트가 그 순간 깨진다.
- 버저닝은 "바꿀 건 바꾸되, 기존 소비자에게는 예고된 기간만큼 옛 동작을 유지해준다"는 약속을 코드가 아니라 프로세스로 지키는 것이다.

### Breaking Change와 Additive Change를 가르는 판별 원리 — 구체 예로
- 예: `/v1/orders` 응답에 새 필드 `discountAmount`를 추가하는 것은 additive다. 기존 클라이언트는 모르는 필드를 무시하고 그대로 동작하기 때문이다. 같은 major(v1) 안에서 처리 가능하다.
- 반대로 `status` 필드의 값 종류를 `"완료"/"대기"` 문자열에서 `1`/`0` 정수로 바꾸는 것은 breaking이다. 기존 클라이언트가 문자열을 기대하는 코드가 그대로 오류를 낸다. 반드시 새 major(v2)로 분리해야 한다.
- 판별 규칙 요약: 필드 추가나 선택적(optional) 파라미터 추가는 대부분 additive, 필드 삭제·타입 변경·필수화·의미 변경은 대부분 breaking이다.

### Semantic Versioning을 수치로 이해하기
- `2.3.1`이라면 major=2(호환 안 되는 구조 변경이 2번 있었음), minor=3(그 안에서 기능 추가가 3번), patch=1(버그수정 1번)이라는 뜻이다.
- API 버전에서는 보통 minor·patch는 URL에 드러내지 않고 major만 노출한다(`/v2/orders`). 클라이언트 입장에서 "내가 신경 써야 할 건 major뿐"이라는 신호를 주기 위해서다.

### 버전 표기 방식 3가지의 선택 원리
- **URI 방식**(`/v1/orders`): 주소창에서 바로 보이고 캐싱·로깅이 쉬워 외부 공개 API에서 가장 흔하다. 단점은 같은 리소스인데 URI가 버전마다 달라진다는 점이다.
- **Header 방식**(`X-API-Version: 1`): 리소스 URI 자체는 그대로 두고 싶은 내부 API·파트너 API에 적합하다. 단, 프록시·캐시 서버가 헤더까지 보고 캐싱하도록 별도 설정이 필요해 운영 난이도가 있다.
- **Media Type 방식**(`Accept: application/vnd.company.v1+json`): REST의 content negotiation 원칙에 가장 충실하지만, 클라이언트가 Accept 헤더를 직접 조작해야 해서 구현 난이도가 가장 높다.

### 폐기(Deprecation) 절차를 수치로
- 예: v1을 v2로 전환한다면, ① v2 출시와 동시에 v1 응답에 `Deprecation: true`, `Sunset: Wed, 01 Jan 2027 00:00:00 GMT` 헤더를 추가해 예고한다. ② 6개월 동안 v1·v2를 병행 운영하며 v1 호출량을 모니터링한다. ③ v1 호출량이 전체의 1% 이하로 떨어지면 남은 소비자에게 개별 연락 후 종료한다.
- 이 수치(6개월, 1%)는 절대값이 아니라, 얼마나 유예를 주고 무엇을 종료 기준으로 삼을지를 명시적으로 정해야 한다는 원칙을 보여주는 예시다.

## 연결 개념
- OpenAPI — breaking change를 diff로 자동 탐지하는 명세 도구
- Consumer-Driven Contract — 소비자가 실제 쓰는 필드 기준으로 호환성을 검증하는 테스트 기법
- API Gateway — 버전별 라우팅과 sunset 정책을 실제로 적용하는 지점

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

- 개요: API 계약 변경 호환성 관리 전략
- 배경: API 소비자는 웹, 모바일, 파트너 시스템으로 나뉘며 배포 주기가 다르다.
- 필요성: semantic version, URI/header version, deprecation, sunset 기준으로 신규 기능 배포와 기존 소비자 보호를 조정한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
