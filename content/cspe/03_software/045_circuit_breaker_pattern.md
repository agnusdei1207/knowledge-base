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
- **개요**: 서킷 브레이커 패턴은 원격 호출의 **실패율**이 임계치를 넘으면 호출 경로를 강제로 끊는 **장애 격리(Fault Isolation) 상태 머신**이다. 목적은 장애 난 서비스를 고치는 것이 아니라, 그 장애가 호출자 쪽으로 번지는 것(연쇄 장애)을 막는 것이다.
- **왜 필요한가**: 원격 서비스가 응답하지 않으면 호출자는 타임아웃까지 스레드를 붙잡고 기다린다. 요청이 몰리는 서비스에서 이 대기가 쌓이면 원인이 아닌 호출자의 스레드 풀까지 고갈되어 함께 멈춘다. 서킷 브레이커는 이 대기를 없애(즉시 실패, Fast-Fail) 호출자를 살린다.
- **핵심 직관**: 실패율을 계속 관찰하다가 기준을 넘는 순간 회로를 끊어 호출을 원천 차단하고, 일정 시간 뒤 소량만 흘려보내 복구 여부를 확인한 다음 재개 여부를 판정한다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 장애 격리 (Fault Isolation) | 한 구성요소의 장애가 다른 구성요소로 번지지 않게 경계를 두는 것 — 서킷 브레이커가 속한 상위 목표 | 방화문으로 화재 확산을 막는 것 |
| 상태 머신 (State Machine) | Closed·Open·Half-Open 세 상태를 정해진 조건에 따라 오가는 모델 | 신호등이 초록→빨강→노랑으로 규칙대로 바뀌는 것 |
| Closed | 정상 상태, 호출을 그대로 통과시키며 실패율을 집계함 | 평소 다니는 길 |
| Open | 차단 상태, 호출을 시도조차 하지 않고 즉시 실패나 대체 응답을 줌 | 통행 금지 바리케이드 |
| Half-Open | Open 유지 시간이 지난 뒤 정해진 수의 호출만 흘려보내 복구를 시험하는 상태 | 공사가 끝났는지 차 몇 대만 먼저 보내보는 것 |
| 슬라이딩 윈도우 (Sliding Window) | 최근 N건(또는 최근 T초)의 호출만 모아 실패율을 계산하는 집계 범위 | 최근 10경기 승률만 보고 컨디션을 판단하는 것 |
| 실패율 임계치 (Failure Rate Threshold) | 윈도우 안에서 이 비율을 넘으면 Open으로 전환하는 기준값 | 시험 커트라인 |
| Fast-Fail | 호출을 원격지로 보내지 않고 즉시 실패를 반환하는 동작 | 문 닫힌 가게 앞에서 기다리지 않고 바로 발길을 돌리는 것 |
| Fallback (폴백) | Open 상태에서 실패 대신 돌려주는 대체 응답(캐시·기본값 등) | 정전 시 미리 켜 둔 비상등 |

## 깊이 이해

### 배경 — Hystrix에서 Resilience4j로
넷플릭스는 2011년경 원격 호출이 급증한 MSA 환경에서 서비스 하나의 지연이 전체 화면 렌더링을 마비시키는 문제를 겪었고, 호출 실패율을 감시해 자동으로 차단하는 라이브러리 Hystrix를 만들어 공개했다. Hystrix는 2018년 유지보수가 중단됐고, 이후 더 가벼운 슬라이딩 윈도우 구현체인 Resilience4j가 사실상 표준이 됐다. 라이브러리는 바뀌어도 Closed·Open·Half-Open 상태 머신 자체는 그대로 이어진다.

### 실패율을 판정하는 법 — 슬라이딩 윈도우 수치 예
윈도우 크기를 최근 호출 10건(count-based)으로 두고 임계치를 50%로 잡았다고 하자. 최근 10건 중 6건이 500 에러나 타임아웃이면 실패율 60%로 임계치를 넘어 Open으로 전환한다. 단, 표본이 적을 때의 오판을 막기 위해 최소 호출 수(minimum number of calls)를 함께 둔다. 최소 호출 수를 20건으로 설정하면, 서비스가 막 기동해 3건밖에 호출하지 않은 시점에는 3건이 모두 실패해도(100%) 판정을 유보하고 Open으로 넘어가지 않는다. 트래픽이 일정하지 않은 서비스는 건수 기반 대신 "최근 60초"처럼 시간 기반(time-based) 윈도우를 쓰면 실패율을 더 안정적으로 반영한다.

### Open에서 Half-Open으로 — 대기 시간과 시험 호출
Open으로 전환되면 waitDurationInOpenState(예: 60초) 동안은 호출을 전혀 시도하지 않고 Fast-Fail만 반환한다. 이 60초는 장애 서비스가 스스로 복구할 시간을 벌어주는 구간이다. 60초가 지나면 Half-Open으로 넘어가 permittedNumberOfCallsInHalfOpenState(예: 5건)만 실제로 호출해 본다. 5건 중 성공이 4건(80%) 이상이면 Closed로 복귀하고, 기준에 못 미치면 즉시 Open으로 되돌아가 다시 60초를 기다린다. 이 왕복 구조 덕분에 죽은 서비스에 트래픽을 몰아넣지 않으면서도, 살아난 서비스를 계속 방치하지도 않는다.

### 판정만으로는 끝나지 않는다 — Fallback을 함께 설계해야 하는 이유
서킷 브레이커만 달아 놓고 Fallback을 정의하지 않으면, Open 상태에서 사용자는 그냥 에러 화면을 본다. 예를 들어 추천 상품 API가 Open되면 추천 대신 캐시에 저장된 어제 인기 상품 목록을 반환하도록 Fallback을 짜 둬야 사용자 경험이 유지된다. Fallback은 실패를 감추는 것이지 원인을 고치는 것이 아니다. 원격 서비스가 계속 죽어 있으면 Half-Open 시험은 계속 실패하고 Open이 반복된다 — 서킷 브레이커는 복구 시간을 벌어줄 뿐, 근본 원인 해결은 별도로 필요하다.

### 흔한 오해 — "Open이면 열려서 통하는 것 아닌가"
회로 용어 그대로 이해해야 한다. 스위치가 열리면(Open) 회로가 끊어져 전류가 흐르지 않는다. 서킷 브레이커도 Open이면 호출이 통하지 않는(차단된) 상태다. 반대로 Closed는 회로가 닫혀 있어 전류(호출)가 정상적으로 흐른다.

## 연결 개념
- Bulkhead(벌크헤드): 서킷 브레이커가 실패율로 차단 여부를 정한다면, 벌크헤드는 서비스별로 스레드 풀 자체를 물리적으로 나눠 한쪽 고갈이 다른 쪽에 번지지 않게 한다 — 임계치 판정과 자원 격리라는 서로 다른 방어선이다.
- Timeout·Retry: 서킷 브레이커가 판정에 쓰는 실패 신호(타임아웃, 5xx)를 만들어내는 하위 설정값.
- 서비스 메시(046): 같은 상태 머신을 애플리케이션 코드가 아니라 Envoy 같은 사이드카 프록시가 대신 판정하도록 인프라 계층으로 옮긴 것.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
