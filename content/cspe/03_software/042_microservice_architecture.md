---
title: "마이크로서비스 아키텍처 MSA (Microservice Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 42
---

# 📖 【암기용】 개념 완전 이해

> 목적: MSA를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 업무 도메인별 작은 서비스를 독립 배포하는 분산 아키텍처
- **왜 필요한가**: 하나의 애플리케이션에 주문·결제·배송이 함께 있으면 작은 변경도 전체 빌드와 회귀 테스트를 요구함. MSA는 변경 단위를 서비스로 쪼개 배포 대기열을 줄임.
- **핵심 직관**: 큰 백화점을 전문 매장으로 나누면 각 매장이 자기 재고와 계산대를 운영하지만, 고객 동선과 안내 체계가 더 필요해짐.

## 깊이 이해
- **배경·문제의식**: 모놀리스는 단일 트랜잭션과 배포 단순성이 장점이나, 조직 규모가 커지면 빌드 시간 30분 이상, 배포 승인 대기, 장애 영향 전체화가 발생함.
- **작동 원리**: 서비스는 bounded context 기준으로 분리하고, 각 서비스가 API와 DB를 소유함. API Gateway가 진입점을 통제하며, 관측성이 호출 흐름을 추적함.
- **비유**: 주문팀, 결제팀, 배송팀이 각자 장부를 갖고 일하되, 고객 문의는 안내 데스크가 접수하고 전체 처리 내역은 송장 번호로 추적하는 구조임.
- **구체 예시**: 주문 서비스는 PostgreSQL, 결제 서비스는 PCI-DSS 범위의 별도 저장소, 배송 서비스는 Kafka 이벤트를 구독해 초당 2천 건 상태 변경을 처리함.
- **흔한 오해·주의점**: 서비스 수가 많으면 MSA가 아님. 독립 배포, 데이터 소유권, 장애 격리, 자동화된 관측성이 없으면 분산 모놀리스가 됨.

## 연결 개념
- DDD bounded context: 서비스 경계 도출 기준
- API Gateway: 인증, 라우팅, rate limit 진입점
- Saga/Outbox: 분산 트랜잭션과 이벤트 정합성 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: MSA 답안은 서비스 분해보다 독립 배포성, DB per Service, 관측성, 분산 트랜잭션 통제까지 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MSA는 업무 기능을 작은 서비스로 분리해 각 서비스가 API, 데이터, 배포 생명주기를 독립 소유하는 아키텍처이다.
> 2. **가치**: 팀별 독립 배포와 장애 격리를 제공하지만 네트워크 지연, 분산 트랜잭션, 관측성 비용이 증가함.
> 3. **판단 포인트**: 서비스 경계, DB per Service, API Gateway, CI/CD, distributed tracing이 없으면 MSA 효과를 검증할 수 없음.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MSA 구성 이해 확인 | service boundary, independent deployability, DB per service | 서비스 쪼개기를 MSA로만 설명 |
| 운영 복잡도 판단 확인 | API Gateway, observability, SLO, circuit breaker | 장애 전파와 데이터 정합성 누락 |
| 분산 트랜잭션 대응 확인 | Saga, Outbox, idempotency, eventual consistency | 2PC를 기본 해법으로 제시 |

> 요약: 이 문제는 MSA의 장점 나열보다 분산 시스템이 만드는 비용과 통제 장치를 함께 요구한다.

---

## Ⅰ. 개요 및 필요성

MSA는 도메인 단위 서비스를 독립 배포하는 구조이다. 대규모 서비스는 기능 증가보다 배포 충돌, 장애 전파, 조직 간 대기 시간이 병목이 된다. MSA는 서비스 경계를 조직 경계와 맞춰 변경 영향과 장애 범위를 제한한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway -> Order Service -> Order DB
                     +-> Payment Service -> Payment DB
                     +-> Delivery Service -> Delivery DB
Service Event -> Message Broker -> Consumer Service
All Services -> Log / Metric / Trace -> Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Gateway | 라우팅, 인증, rate limit, BFF 분기 | 단일 진입점 병목 대응 필요 |
| Service | 도메인 기능과 API 제공 | 독립 빌드·배포·롤백 단위 |
| DB per Service | 데이터 소유권 분리 | cross DB join 금지, 이벤트 정합성 |
| Observability | 로그·메트릭·트레이스 수집 | OpenTelemetry trace ID 전파 |

> 요약: MSA는 Gateway, 도메인 서비스, 독립 저장소, 메시징, 관측성이 결합되어야 독립 배포성을 확보한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> Gateway 인증/라우팅 -> 서비스 처리
-> 로컬 DB 트랜잭션 -> 이벤트 발행 -> 타 서비스 구독
-> 로그/메트릭/트레이스 수집 -> SLO 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Gateway에서 JWT 검증과 라우팅 | 401/403 비율, route match |
| 2 | 서비스가 도메인 로직 수행 | p95 지연, error rate |
| 3 | 로컬 DB commit 후 Outbox 저장 | transaction rollback rate |
| 4 | Broker로 이벤트 전달 | consumer lag 1분 이하 |
| 5 | Trace와 metric으로 호출 경로 분석 | trace coverage 95% 이상 |

> 요약: MSA는 동기 API와 비동기 이벤트를 조합하고, 서비스별 로컬 트랜잭션을 관측성으로 검증한다.

---

## Ⅳ. 특징

| 구분 | 모놀리스 | MSA | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 배포 | 전체 애플리케이션 단위 | 서비스별 독립 배포 | 서비스별 일 10회 배포 가능 |
| 데이터 | 단일 DB 공유 | DB per Service | cross service join 제거 |
| 장애 | 프로세스 장애가 전체 영향 | bulkhead, circuit breaker로 격리 | MTTR 30분 이하 목표 |
| 운영 | 단일 로그 중심 | 분산 추적·SLO 필요 | trace ID 전파율 95% 이상 |

> 요약: MSA는 독립 배포와 장애 격리를 얻는 대신 네트워크, 데이터 정합성, 관측성 비용을 감수하는 구조이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 모듈형 모놀리스 | MSA | 팀 5개 이상, 도메인별 변경 주기 상이 |
| 비용/성능 | in-process call | network call, serialization | p95 200ms 이하면 호출 depth 3 이하 |
| 운영/위험 | 단일 배포 | 서비스별 CI/CD, SLO | 배포 실패율 5% 이하 자동 롤백 |

> 요약: MSA는 조직과 배포 병목이 확인될 때 선택하며, 단순 트래픽 증가만으로 선택하지 않는다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 분산 모놀리스 | 잘못된 서비스 경계 | DDD event storming, context map | 동시 배포 서비스 수 |
| 정합성 오류 | 로컬 트랜잭션 분리 | Saga, Outbox, idempotency key | 보상 실패율, 중복 이벤트 |
| 장애 전파 | timeout/retry 부재 | circuit breaker, bulkhead, retry budget | error budget burn rate |

> 요약: MSA 리스크는 경계 오류와 장애 전파이며, DDD와 resilience pattern으로 제어한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배포 독립성 | 서비스 단독 배포율 90% 이상 | CI/CD pipeline 로그 |
| 운영 품질 | p95 200ms, error rate 1% 이하 | APM, SLO dashboard |
| 정합성 | 이벤트 처리 지연 1분 이하 | Broker lag, DLQ 건수 |

> 요약: MSA 도입 후에는 배포 독립성, SLO, 이벤트 정합성 지표를 동시에 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Event storming으로 bounded context를 도출하고 서비스별 owner, API contract, DB schema 소유권을 명시함.
2. Kubernetes, Helm, Argo CD로 서비스별 배포 파이프라인을 구성하고 canary 10%, rollback 10분 이내 기준을 둠.
3. OpenTelemetry, Prometheus, Grafana, Jaeger로 p95 지연·오류율·trace coverage·DLQ를 수집함.

**결론 (2줄):**
- 기술사 판단: 배포 충돌과 조직 병목이 핵심이면 MSA를, 단일 팀과 단일 트랜잭션이 핵심이면 모듈형 모놀리스를 선택함.
- 향후 방향: MSA는 platform engineering, service mesh, policy as code와 결합해 운영 자동화 중심으로 진화함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MSA를 설명하시오", "기술하시오" | Gateway, service, DB per service, event 흐름 | 모놀리스 대비 배포·장애·정합성 비교 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "설계하시오", "비교하시오" | 서비스 분해와 분산 트랜잭션 처리 절차 | 선택 기준, 리스크, 관측 지표 |

> 요약: 설명형은 구조와 원리, 설계·방안형은 서비스 경계와 운영 통제 지표 중심으로 전환한다.
