---
title: "이벤트 소싱·CQRS (Event Sourcing CQRS)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 47
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이벤트 소싱과 CQRS를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 상태 변경 이력을 이벤트로 저장하고 명령과 조회 모델을 분리하는 패턴
- **왜 필요한가**: 현재 상태만 저장하면 누가 언제 왜 바꿨는지 추적하기 어려움. 쓰기와 읽기 요구가 다르면 하나의 모델이 양쪽 모두를 만족시키기 어려움.
- **핵심 직관**: 통장 잔액만 적는 대신 모든 입출금 내역을 저장하고, 잔액표는 필요할 때 내역을 합산해 만드는 방식임.

## 깊이 이해
- **배경·문제의식**: 복잡한 도메인은 감사 추적, 재현, 시간별 상태 복원이 필요함. 또한 쓰기는 불변식 검증이 중요하고 읽기는 화면 조회 속도와 검색 조건이 중요함.
- **작동 원리**: Event Sourcing은 append-only event log에 도메인 이벤트를 저장함. CQRS는 command model이 이벤트를 만들고 query model은 projection을 통해 조회 전용 저장소를 갱신함.
- **비유**: 법원 기록처럼 판결 결과만 남기지 않고 모든 심리 기록을 남기며, 대시보드는 기록을 가공한 요약표로 보여주는 방식임.
- **구체 예시**: `OrderCreated`, `PaymentApproved`, `OrderShipped` 이벤트를 Kafka/EventStoreDB에 저장하고, Elasticsearch projection으로 주문 검색 화면을 구성함.
- **흔한 오해·주의점**: Event Sourcing과 CQRS는 항상 함께 써야 하는 것은 아님. 감사·재생 요구가 약한 CRUD 시스템에는 복잡도를 추가할 수 있음.

## 연결 개념
- Append-only Event Log: 불변 이벤트 저장
- Projection: 조회 모델 생성과 재구성
- Eventual Consistency: 쓰기 모델과 읽기 모델 간 지연 허용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Event Sourcing/CQRS는 append-only event log, projection, eventual consistency, replay/snapshot을 정합성·감사 관점으로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Event Sourcing은 상태 변경을 이벤트 로그로 저장하고, CQRS는 command와 query 모델을 분리하는 아키텍처 패턴이다.
> 2. **가치**: 감사 추적, 상태 재현, 읽기 모델 최적화를 제공하지만 projection 지연과 이벤트 스키마 진화 관리가 필요함.
> 3. **판단 포인트**: 도메인 감사성, 재처리 요구, 조회 부하, 최종 일관성 허용 범위를 기준으로 적용 여부를 결정해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 패턴 구조 이해 확인 | event log, command model, projection, query model | 단순 message queue로 설명 |
| 정합성 판단 확인 | eventual consistency, replay, snapshot | 즉시 일관성만 전제로 답안 작성 |
| 운영 리스크 확인 | event schema versioning, duplicate event, projection lag | 이벤트 재처리와 스키마 진화 누락 |

> 요약: 이 문제는 이벤트 저장과 조회 모델 분리의 이점을 정합성·감사·운영 비용 관점으로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

Event Sourcing/CQRS는 상태 변경 이력과 조회 모델을 분리한다. 복잡한 업무 시스템은 현재 값뿐 아니라 변경 근거, 감사 추적, 재처리가 필요하다. 쓰기 모델과 읽기 모델의 요구가 다를 때 두 모델을 분리해 각각 최적화한다.

---

## Ⅱ. 구조 및 구성요소

```text
Command -> Command Handler -> Aggregate -> Event Store
                                      -> Event Bus -> Projection
Projection -> Read Model DB -> Query API -> Client
Snapshot -> Aggregate Rehydration
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Command Model | 명령 검증과 도메인 불변식 처리 | 쓰기 중심 aggregate |
| Event Store | append-only 이벤트 저장 | optimistic concurrency control |
| Projection | 이벤트를 읽기 모델로 변환 | 재구성, 재처리 가능 |
| Read Model | 조회 전용 저장소 | Elasticsearch, Redis, RDB 등 선택 |

> 요약: 쓰기는 이벤트를 만들고, 읽기는 projection이 만든 조회 모델을 사용해 서로 다른 요구를 분리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Command 수신 -> Aggregate 상태 복원 -> 불변식 검증
-> Domain Event 생성 -> Event Store append
-> Projection consume -> Read Model 갱신
-> Query API 조회 -> lag 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | command validation 수행 | 필수 값, 권한, 중복 명령 |
| 2 | event replay로 aggregate 복원 | snapshot interval 100건 |
| 3 | 신규 event append | expected version 일치 |
| 4 | projection이 read model 갱신 | projection lag 5초 이하 |
| 5 | query API가 조회 모델 반환 | stale read 허용 정책 |

> 요약: Event Sourcing은 이벤트를 append하고 projection을 통해 조회 모델을 갱신하며, CQRS는 쓰기와 읽기 경로를 분리한다.

---

## Ⅳ. 특징

| 구분 | CRUD 중심 | Event Sourcing/CQRS | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 저장 방식 | 현재 상태 update | append-only event | 감사 로그 100% 보존 |
| 조회 모델 | 쓰기 모델 공유 | projection별 read model | projection lag 5초 이하 |
| 복구 | backup 시점 복원 | event replay, snapshot | replay 시간 10분 이하 |
| 복잡도 | 단일 모델 | schema version, 재처리 필요 | event version 정책 필수 |

> 요약: Event Sourcing/CQRS는 감사·재현·조회 최적화에 유리하나 스키마와 projection 운영 역량을 요구한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | CRUD+감사 테이블 | event log+projection | 변경 이력 재현 요구 100% |
| 비용/성능 | 단일 DB 조회 | read model별 저장소 | 읽기 TPS가 쓰기 TPS의 10배 이상 |
| 운영/위험 | 단순 schema migration | event versioning, replay | projection rebuild 30분 이하 |

> 요약: 감사와 재현이 핵심이면 Event Sourcing을, 읽기 부하 분산이 핵심이면 CQRS 단독 적용도 가능하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Projection 지연 | consumer 처리 부족 | partition 조정, backpressure | projection lag |
| 이벤트 스키마 파손 | breaking change | schema registry, upcaster | incompatible event 0건 |
| 중복 처리 | at-least-once delivery | idempotency key, dedup table | duplicate 처리율 |

> 요약: 운영 리스크는 projection 지연과 스키마 진화이며, schema registry와 idempotency로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 감사성 | event append 누락 0건 | event store audit |
| 조회 품질 | projection lag 5초 이하 | consumer metric |
| 복구성 | snapshot 기반 replay 10분 이하 | disaster recovery drill |

> 요약: 도입 효과는 감사 누락, projection lag, replay 시간으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 감사·재현 요구가 있는 aggregate부터 EventStoreDB, Kafka compact topic, PostgreSQL event table 중 저장소를 선정함.
2. event schema version, upcaster, snapshot interval 100건, idempotency key를 표준으로 정함.
3. projection lag, replay duration, duplicate event count를 Prometheus로 수집하고 read model 재구성 절차를 운영 runbook에 등록함.

**결론 (2줄):**
- 기술사 판단: 금융·주문·감사처럼 변경 이력 재현이 핵심이면 Event Sourcing/CQRS를 적용하고, 단순 CRUD에는 CQRS 일부만 검토함.
- 향후 방향: 이벤트 기반 MSA와 결합해 auditability, replay, analytics pipeline을 하나의 event log로 연결하는 방향임.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Event Sourcing과 CQRS를 설명하시오" | command, event store, projection 흐름 | CRUD 대비 감사·조회 분리 |
| 요구사항 명시형 | "비교하시오", "도입 방안을 제시하시오" | projection lag, replay, snapshot 설계 | 정합성 리스크와 적용 조건 |

> 요약: 설명형은 구조와 흐름, 방안형은 최종 일관성과 운영 지표 중심으로 전환한다.
