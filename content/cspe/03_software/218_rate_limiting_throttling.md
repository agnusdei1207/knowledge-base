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
- **개요**: 레이트 리미팅(Rate Limiting)과 스로틀링(Throttling)은 단위 시간당 허용 요청 수(또는 처리 속도)를 제어해 시스템 자원을 보호하는 **트래픽 제어** 기법이다.
- **왜 필요한가**: 한 사용자·IP가 초당 수천 요청을 보내면 DB 커넥션, 캐시, 외부 API 쿼터가 고갈되어 다른 정상 사용자까지 피해를 본다.
- **핵심 직관**: Rate Limiting은 "선을 넘으면 거절(reject)", Throttling은 "속도를 늦추거나 줄을 세운다(delay/queue)" — 초과 요청을 다루는 방식이 다르다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 트래픽 제어 | 이 개념이 속한 상위 범주 — 요청 유입량을 정책으로 조절하는 것 전반 | 도로의 신호등·차선 통제 |
| Rate Limiting | 정해진 한도를 넘는 요청을 즉시 거절(HTTP 429) | 정원 초과 시 입장 거부 |
| Throttling | 한도를 넘는 요청을 거절하지 않고 지연·대기열 처리 | 정원 초과 시 줄 세우기 |
| Fixed Window | 고정된 시간 구간(예: 매 분)마다 카운터를 0으로 리셋 | 매 정각 리셋되는 회전문 카운터 |
| Sliding Window | 현재 시점부터 과거 N초를 계속 이동하며 계산 | 최근 60초를 항상 다시 재는 스톱워치 |
| Token Bucket | 토큰이 일정 속도로 채워지고 요청마다 토큰을 소비, 버킷 용량만큼 burst 허용 | 정해진 속도로 코인이 쌓이는 자판기 |
| Leaky Bucket | 요청이 큐에 쌓이고 일정한 속도로만 빠져나감(배출 속도 고정) | 구멍 뚫린 양동이 — 들어오는 속도와 무관하게 일정하게 샘 |
| HTTP 429 / Retry-After | 초과 시 표준 응답 코드와 "몇 초 후 재시도하라"는 헤더 | 안내판 "10분 후 다시 오세요" |
| 분산 카운터(원자 연산) | 여러 서버가 공유하는 카운터를 Redis INCR 등으로 동시성 없이 갱신 | 여러 창구가 하나의 대기번호판을 공유 |

## 깊이 이해

### 왜 필요한가 — 무제한 요청의 결과
- 로그인 API에 한도가 없으면 봇이 초당 수천 번 비밀번호를 대입(brute force)할 수 있고, 검색 API에 한도가 없으면 크롤러가 DB 커넥션 풀(예: 100개)을 전부 점유해 실제 사용자 요청이 타임아웃에 빠진다. 그래서 "허용치"를 명시적 정책으로 못박아야 한다.

### Rate Limiting vs Throttling — 초과 요청을 어떻게 다루나
- 둘 다 "한도"를 기준으로 판단하지만 **초과 시 동작**이 다르다. Rate Limiting은 한도를 넘는 즉시 요청을 끊어낸다(429 반환) — 결제 API처럼 정확한 상한이 중요할 때 맞다. Throttling은 요청을 버리지 않고 속도를 늦추거나 대기열에 넣어 나중에 처리한다 — 배치 작업, 파일 업로드처럼 "늦게라도 처리되면 되는" 경우에 맞다.

### Fixed Window의 허점 — 경계 burst 문제(수치 예)
- 정책이 "분당 100건"이고 Fixed Window를 쓴다고 하자. 00:00:00~00:00:59 구간에 사용자가 00:00:59에 100건을 몰아 보내면 허용된다. 바로 다음 구간인 00:01:00에 다시 100건을 몰아 보내면 이것도 허용된다. 결과적으로 00:00:59~00:01:00의 단 2초 사이에 200건이 통과한다 — 정책은 "분당 100건"인데 순간적으로는 2배가 새는 것이다. 이것이 Fixed Window의 경계(boundary) burst 문제다.
- Sliding Window는 "지금 시점 기준 과거 60초"를 항상 다시 계산하므로 이 허점이 없다. 대신 매 요청마다 과거 요청 타임스탬프를 유지·계산해야 해서 Fixed Window보다 저장·연산 비용이 크다.

### Token Bucket 동작 — 수치로 이해
- 버킷 용량(capacity) 20개, 토큰 보충 속도(refill rate) 초당 10개인 정책을 예로 보자. 평소 요청이 없으면 토큰이 최대 20개까지 쌓인다(가득 차면 더 안 쌓임). 갑자기 요청이 20건 몰리면(burst) 쌓여 있던 토큰 20개를 즉시 소비해 20건 모두 통과시킨다 — burst를 허용하는 것이다. 이후에는 초당 10개씩만 토큰이 채워지므로 초당 10건으로 속도가 제한된다. 즉 Token Bucket은 "평균 속도(refill rate)는 제한하되 순간 burst는 용량만큼 봐준다"는 정책이다.

### Leaky Bucket 동작 — 수치로 이해
- 큐 용량 50건, 배출 속도(leak rate) 초당 5건인 정책이라면, 요청이 몰려 큐에 50건까지 쌓여도 처리(backend 전달)는 항상 초당 5건으로 균일하게 나간다. 51번째 요청이 도착하면 큐가 가득 차 거절(overflow)된다. Token Bucket이 "burst를 허용"하는 데 비해 Leaky Bucket은 "출력 속도를 완전히 균일화"하는 데 초점이 있다 — backend가 일정한 부하만 견디면 되는 경우(예: 결제 게이트웨이 연동)에 적합하다.

### 분산 환경에서 카운터를 세는 법
- 서버가 여러 대면 각자 로컬 메모리로 세는 카운터는 무의미하다(서버 A가 40건, 서버 B가 40건 세면 실제로는 80건이 통과했는데 각 서버는 한도 100건 이하로 착각한다). 그래서 Redis 같은 중앙 저장소에 `INCR`(원자적 증가) + `EXPIRE`(TTL)로 카운터를 두거나, Lua 스크립트로 "읽기+비교+증가"를 하나의 원자 연산으로 묶어야 race condition을 막는다.

### 비유와 흔한 오해
- **비유**: 지하철 개찰구가 시간당 입장 인원을 제한하는 것과 같다. Rate Limiting은 정원이 차면 문을 잠그는 것(거절), Throttling은 정원이 차면 줄을 세워 순서대로 들여보내는 것(지연)이다.
- **오해**: "429만 반환하면 끝"이 아니다. 어떤 키(사용자 ID? IP? API 키?)로 제한을 거는지에 따라 우회가 쉬워질 수 있다(예: IP 기준만 걸면 프록시 로테이션으로 우회). 실무에서는 사용자+IP+기기 지문을 조합하고, VIP·내부 서비스는 별도 예외 정책을 둔다.

## 연결 개념
- API Gateway — 인증·쿼터와 함께 레이트 제한이 실제로 적용되는 지점
- Redis — 분산 카운터·Token Bucket 상태를 저장하는 대표적 저장소
- Circuit Breaker — 레이트 제한이 "내가 받는 요청"을 조절한다면, Circuit Breaker는 "내가 호출하는 대상"의 장애를 차단하는 상호보완 기법

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

- 개요: 단위 시간 요청 제어 기법
- 배경: 공개 API, 로그인, 결제, 검색은 비정상 요청과 사용량 급증에 노출된다.
- 필요성: token bucket, leaky bucket, quota로 backend와 외부 연계 한도를 보호해야 한다.

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
