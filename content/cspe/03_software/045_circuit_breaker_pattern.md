---
title: "서킷 브레이커 패턴 (Circuit Breaker Pattern)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 45
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서킷 브레이커 패턴을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 장애난 외부 호출을 잠시 차단해 연쇄 장애를 막는 회복탄력성 패턴
- **왜 필요한가**: MSA에서는 한 서비스 지연이 retry 폭증을 만들고, 스레드 풀 고갈로 다른 서비스까지 실패할 수 있음. 호출을 계속 시도하지 않고 차단해야 장애 전파를 제한함.
- **핵심 직관**: 전기 차단기처럼 과부하가 감지되면 회로를 끊고, 잠시 뒤 시험 전류로 복구 여부를 확인함.

## 깊이 이해
- **배경·문제의식**: 분산 호출은 네트워크 지연, 5xx, timeout, 연결 풀 고갈을 동반함. 실패한 서비스를 계속 호출하면 대기열과 retry가 누적되어 cascading failure가 발생함.
- **작동 원리**: Closed 상태에서는 정상 호출함. 실패율이 임계치를 넘으면 Open으로 전환해 즉시 실패 또는 fallback을 반환함. 일정 시간 뒤 Half-open에서 제한된 호출로 복구를 확인함.
- **비유**: 엘리베이터가 고장났을 때 모든 사람이 계속 버튼을 누르지 않도록 점검 중 표지를 붙이고, 수리 후 몇 번 시험 운행한 뒤 정상 운행하는 방식임.
- **구체 예시**: 결제 API 5xx가 30초 동안 50%를 넘으면 60초간 Open으로 전환하고 캐시 응답 또는 대체 결제 안내를 반환함.
- **흔한 오해·주의점**: circuit breaker는 장애를 복구하지 않음. 장애 전파를 제한하고 서비스가 회복할 시간을 주는 패턴이며 timeout, retry, bulkhead와 함께 설계해야 함.

## 연결 개념
- Timeout/Retry: 호출 실패 감지와 재시도 예산
- Bulkhead: 장애 영역 격리와 스레드 풀 분리
- SLO/Error Budget: 차단 임계치와 운영 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 서킷 브레이커는 closed/open/half-open 상태 전이, timeout/retry/bulkhead 조합, cascading failure 통제 지표로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Circuit Breaker는 원격 호출 실패율이 임계치를 넘으면 호출을 차단하고 fallback을 반환해 장애 전파를 제한하는 패턴이다.
> 2. **가치**: timeout 대기와 무제한 retry로 인한 스레드 고갈을 막고, 장애 서비스에 회복 시간을 제공함.
> 3. **판단 포인트**: 실패율 임계치, Open 유지 시간, Half-open 시험 호출 수, retry budget, bulkhead 격리를 수치로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 장애 전파 통제 이해 확인 | closed/open/half-open 상태 전이 | 단순 retry와 혼동 |
| 분산 시스템 설계 역량 확인 | timeout, retry, bulkhead, fallback 조합 | 재시도를 무제한 허용 |
| 운영 지표 판단 확인 | failure rate, slow call rate, error budget | 임계치와 관측 지표 누락 |

> 요약: 이 문제는 장애를 숨기는 기법이 아니라 실패를 조기 차단해 전체 SLO를 지키는 설계 판단을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 실패 원격 호출 차단 패턴
- 배경: MSA는 서비스 간 동기 호출이 많아 한 서비스 지연이 thread pool 고갈, retry 폭증, cascading failure로 확산될 수 있음.
- 필요성: Circuit Breaker의 closed/open/half-open 상태와 timeout, failure rate threshold, fallback을 적용해 p99 지연과 error rate를 제한해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Caller -> Circuit Breaker -> Remote Service
          / Closed: 정상 호출
          / Open: 호출 차단, fallback 반환
          / Half-open: 제한 호출로 복구 확인
Metrics -> failure rate / slow call rate / timeout -> State Transition
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| State Machine | Closed, Open, Half-open 상태 관리 | sliding window 기반 전이 |
| Failure Detector | 5xx, timeout, slow call 집계 | 실패율 50% 등 임계치 |
| Fallback | 캐시, 기본 응답, 대체 경로 제공 | 업무 중요도별 응답 설계 |
| Bulkhead/Timeout | 리소스 격리와 대기 시간 제한 | thread pool, connection pool 분리 |

> 요약: Circuit Breaker는 상태 전이와 실패 지표를 기반으로 호출 허용 여부와 fallback을 결정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 발생 -> Circuit 상태 확인
-> Closed이면 원격 호출 -> 성공/실패 지표 기록
-> 실패율 임계치 초과 -> Open 전환 -> fallback 반환
-> 대기 시간 경과 -> Half-open 시험 호출 -> 성공 시 Closed
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 호출 전 breaker 상태 확인 | state transition log |
| 2 | timeout 내 원격 API 호출 | timeout 1초, slow call ratio |
| 3 | 실패율·지연율 sliding window 계산 | 10초/100건 window |
| 4 | Open 상태에서 fail-fast 또는 fallback | fallback 성공률, 차단 건수 |
| 5 | Half-open 제한 호출로 복구 판정 | permitted calls 5건, 성공률 80% |

> 요약: Circuit Breaker는 실패율을 누적해 Open으로 차단하고 Half-open 시험 호출로 복구 여부를 판단한다.

---

## Ⅳ. 특징

| 구분 | 단순 Retry | Circuit Breaker | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 장애 대응 | 계속 재시도 | 임계치 초과 시 차단 | retry 2회, backoff 100ms/500ms |
| 리소스 보호 | 대기열 증가 가능 | fail-fast로 thread 보호 | thread pool 사용률 80% 이하 |
| 복구 확인 | 호출마다 시도 | Half-open 시험 호출 | 5건 중 4건 성공 시 Closed |
| 적용 범위 | 일시 오류 | 지속 오류, 외부 API 장애 | failure rate 50% 이상 |

> 요약: Circuit Breaker는 retry 폭증을 막고 장애 서비스와 호출 서비스를 동시에 보호하는 패턴이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | timeout+retry만 적용 | breaker+fallback+bulkhead | 외부 호출 p95 500ms 초과 또는 5xx 급증 |
| 비용/성능 | 호출 지속으로 부하 누적 | fail-fast로 대기 시간 제한 | p99 지연 1초 이하 목표 |
| 운영/위험 | 장애 전파 가능 | 상태 전이 기반 격리 | error budget 30% 소진 시 차단 |

> 요약: Circuit Breaker는 지속 장애와 retry 폭증이 확인되는 외부 의존 호출에 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 과도한 차단 | 임계치 과소 설정 | traffic volume threshold, sliding window 조정 | false open 비율 |
| 장애 은폐 | fallback이 오류를 숨김 | fallback 응답 라벨링, 알림 | fallback rate, alert count |
| Retry storm | breaker와 retry 순서 오류 | retry budget, exponential backoff | retry per request |

> 요약: breaker는 임계치와 retry 예산을 함께 설계해야 과차단과 retry storm을 막을 수 있다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 장애 차단 | Open 전환 후 실패 호출 80% 이상 감소 | resilience4j metrics |
| 지연 통제 | p99 latency 1초 이하 | APM, histogram |
| 복구 품질 | Half-open 성공률 80% 이상 | breaker event log |

> 요약: Circuit Breaker 효과는 실패 호출 감소, p99 지연, Half-open 복구 성공률로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Resilience4j, Hystrix legacy, Envoy outlier detection 중 표준을 정하고 failure rate 50%, wait duration 60초 같은 임계치를 설정함.
2. timeout 1초, retry 2회, exponential backoff, bulkhead thread pool 50개처럼 호출별 정책을 코드와 설정으로 분리함.
3. fallback 응답에 degraded flag를 포함하고 Prometheus로 breaker state, fallback rate, slow call ratio를 대시보드화함.

**결론 (2줄):**
- 기술사 판단: 외부 API·동기 서비스 호출이 SLO를 위협하면 Circuit Breaker를 적용하고, 내부 계산 로직에는 timeout·bulkhead 중심으로 설계함.
- 향후 방향: Service Mesh의 Envoy outlier detection과 애플리케이션 breaker를 조합해 L7 트래픽과 업무 fallback을 분리하는 방향임.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Circuit Breaker를 설명하시오" | closed/open/half-open 상태 전이 | retry, timeout, bulkhead 비교 |
| 요구사항 명시형 | "장애 대응 방안을 제시하시오", "설계하시오" | 임계치, fallback, retry budget 설계 | cascading failure 차단 지표 |

> 요약: 설명형은 상태 전이, 방안형은 장애 전파 차단과 운영 지표 중심으로 전환한다.
