---
title: "레이트 리미팅·스로틀링 (Rate Limiting Throttling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 218
---

# 📖 【암기용】 개념 완전 이해

> 목적: 레이트 리미팅과 스로틀링을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사용자·IP·토큰별 요청 속도를 제한해 시스템 자원과 공정성을 보호하는 제어 기법
- **왜 필요한가**: 특정 사용자가 초당 수천 요청을 보내면 DB, 캐시, 외부 API 쿼터가 고갈됨
- **핵심 직관**: Rate Limiting은 제한선을 넘으면 거절하고, Throttling은 속도를 늦추거나 대기열로 보냄

## 깊이 이해
- **배경·문제의식**: 공개 API와 로그인, 검색, 결제는 악성 트래픽과 실수성 반복 호출에 노출된다. 제한이 없으면 정상 사용자 SLO가 깨진다.
- **작동 원리**: Fixed Window, Sliding Window, Token Bucket, Leaky Bucket 알고리즘으로 일정 시간당 허용 요청 수를 계산한다.
- **비유**: 지하철 개찰구가 시간당 입장 인원을 제한하고, 사람이 몰리면 줄을 세우거나 입장을 막는 방식과 같음
- **구체 예시**: 로그인 API는 사용자별 5회/min, IP별 100회/min, 실패 10회 이상 CAPTCHA를 적용해 brute force를 제한한다.
- **흔한 오해·주의점**: HTTP 429만 반환하면 충분하지 않다. 분산 카운터 일관성, 우회 키, Retry-After, VIP 예외 정책이 필요함

## 연결 개념
- API Gateway - 인증·쿼터·레이트 제한 적용 지점
- Redis - 분산 카운터와 token bucket 저장소
- Circuit Breaker - 내부 의존성 장애 시 호출 차단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 제한 알고리즘, 제한 키, 초과 처리, 분산 카운터, 관측 지표를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Rate Limiting·Throttling은 요청 속도와 동시성을 정책으로 제한해 backend 자원과 SLO를 보호하는 통제이다.
> 2. **가치**: DDoS성 트래픽, 크롤링, API 오남용, 외부 API 쿼터 초과를 사전에 차단한다.
> 3. **판단 포인트**: Fixed/Sliding Window, Token/Leaky Bucket, per-user/IP/API key 제한을 요구별로 조합한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| API 보호 설계 이해 확인 | 알고리즘, 제한 키, 429, Retry-After | 단순 "요청 제한"으로만 설명 |
| 분산 시스템 판단 확인 | Redis 카운터, 원자 연산, clock skew | 단일 노드 메모리 기준만 작성 |
| 운영·보안 통제 확인 | 우회 방지, 예외 정책, 관측 지표 | 정상 사용자 영향과 VIP 정책 누락 |

> 요약: 이 문제는 제한량 수치와 초과 처리 방식까지 명확히 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

레이트 리미팅은 단위 시간당 요청 수를 제한하는 기법이다. 스로틀링은 초과 요청을 지연·대기·감속 처리한다. 공개 API, 로그인, 결제, 검색은 요청 제한 없이는 backend와 외부 연계 쿼터를 보호하기 어렵다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway/Ingress -> Identity Extract
-> Limit Policy -> Counter Store -> Allow/Throttle/Reject
-> Backend -> Metric/Alert
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Limit Key | 사용자·IP·API key 식별 | NAT, bot 우회 고려 |
| Algorithm | 요청 허용량 계산 | Token Bucket, Sliding Window |
| Counter Store | 분산 카운터 저장 | Redis INCR/EXPIRE, Lua atomic |
| Enforcement | 허용·지연·거절 처리 | HTTP 429, Retry-After |

> 요약: 제한 구조는 식별 키, 알고리즘, 분산 카운터, 초과 처리로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request -> Extract User/IP/API Key -> Load Policy
-> Atomic Counter/Token Check
  / Allowed -> Forward Backend
  / Exceeded -> 429 or Queue Delay
-> Log Decision -> Update Metrics
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 제한 대상 식별 | user_id, IP, API key 매핑 |
| 2 | 정책 조회 | endpoint별 limit 100req/min |
| 3 | 원자 카운터 갱신 | Redis Lua latency p95 5ms 이하 |
| 4 | 초과 요청 처리 | 429, Retry-After, queue timeout |

> 요약: 정확한 제한은 원자적 카운터 갱신과 일관된 제한 키 설계에 달려 있다.

---

## Ⅳ. 특징

| 구분 | Fixed/Sliding Window | Token/Leaky Bucket | 판단 수치 |
|:---|:---|:---|:---|
| 처리 방식 | 시간 구간별 요청 수 계산 | 토큰 보충 또는 일정 배출 | burst 허용 여부 |
| 장점 | 구현 단순, 감사 용이 | 순간 burst와 평균률 동시 제어 | 100req/min, burst 20 |
| 한계 | 경계 시 burst 집중 | 토큰 저장·동기화 필요 | Redis p95 5ms 목표 |
| 적용 | 로그인 실패 제한 | 공개 API·검색·결제 API | endpoint별 정책 분리 |

> 요약: Window 계열은 단순 제한, Bucket 계열은 burst 허용과 평균률 제어에 맞다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Rate Limiting/Throttling | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | backend 내부 방어 | gateway/edge 선제 제한 | 공개 API, 인증 전 endpoint |
| 비용/성능 | 과부하 후 실패 | 진입점 차단 | backend CPU 70% 이상 전 차단 |
| 운영/위험 | 일괄 차단 | 사용자·등급·endpoint별 정책 | 무료/유료 tier 구분 필요 |

> 요약: 제한은 backend가 과부하된 뒤가 아니라 gateway와 edge에서 선제 적용해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 우회 호출 | IP 회전, 계정 다중 생성 | user+IP+device fingerprint 조합 | bypass detection count |
| 카운터 불일치 | 다중 노드 local counter | Redis cluster, atomic Lua | counter error rate |
| 정상 사용자 차단 | NAT 공유, 정책 과소 산정 | allowlist, adaptive limit | false positive 0.1% 이하 |

> 요약: 제한 리스크는 우회, 분산 카운터 오차, 정상 사용자 차단이며 식별 다중화와 예외 정책으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 차단 품질 | 429 rate, false positive 0.1% 이하 | gateway log, CS ticket |
| backend 보호 | CPU 70% 이하, DB connection 80% 이하 | APM, DB metric |
| 정책 지연 | counter p95 5ms 이하 | Redis latency, tracing |

> 요약: 운영 평가는 차단률, backend 자원, 제한 처리 지연으로 수행한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 로그인은 user+IP 기준 5회/min, 실패 10회 CAPTCHA, 공개 API는 API key 기준 1,000req/min 정책 적용
2. API Gateway에서 Token Bucket, Redis Lua atomic counter, `Retry-After` 헤더, HTTP 429 표준 응답 구성
3. VIP allowlist, tier별 quota, false positive 0.1% 이하 모니터링, 보안 이벤트 SIEM 연계 적용

**결론 (2줄):**
- 기술사 판단: 보안성 endpoint는 Sliding Window, burst 허용 API는 Token Bucket, 대기열 처리가 가능한 작업은 Throttling 선택
- 향후 방향: WAF, Bot Management, API Gateway가 사용자 행위 기반 adaptive limit로 결합되는 방향으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "레이트 리미팅을 설명하시오" | 제한 키와 카운터 처리 흐름 | 알고리즘별 특징 비교 |
| 요구사항 명시형 | "API 오남용 방안을 제시하시오" | gateway, Redis, 429, Retry-After 설계 | 우회 방지와 false positive 지표 |

> 요약: 설명형은 알고리즘 원리, 방안형은 제한 수치와 보안 운영 기준을 중심으로 작성한다.
