---
title: "MSA 분해 전략 - 도메인 주도 설계 (MSA Decomposition DDD)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 43
---

# 📖 【암기용】 개념 완전 이해

> 목적: DDD 기반 MSA 분해를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 업무 경계를 기준으로 마이크로서비스를 나누는 설계 접근
- **왜 필요한가**: 테이블이나 화면 기준으로 서비스를 쪼개면 주문 변경 때 결제·배송 서비스가 함께 수정되는 분산 모놀리스가 됨. DDD는 업무 언어와 경계로 분해 기준을 제공함.
- **핵심 직관**: 조직의 업무 책임선을 소프트웨어 경계로 옮기는 작업임.

## 깊이 이해
- **배경·문제의식**: MSA 실패의 대표 원인은 과분해와 공유 DB임. 기술 계층 기준 분해는 서비스 수를 늘리지만 변경 영향과 데이터 결합을 줄이지 못함.
- **작동 원리**: bounded context로 업무 언어와 모델 경계를 나누고, aggregate로 트랜잭션 경계를 정함. context map은 서비스 간 관계를 upstream/downstream으로 표시함.
- **비유**: 병원에서 접수, 진료, 수납, 약국은 같은 환자 정보를 보지만 각자 책임과 장부가 다름. DDD는 이 책임 경계를 먼저 찾는 방식임.
- **구체 예시**: 주문 context는 Order aggregate를 소유하고 결제 context는 Payment aggregate를 소유함. 주문 확정 이벤트를 발행하면 결제가 구독하고, 두 DB를 직접 join하지 않음.
- **흔한 오해·주의점**: aggregate는 테이블 묶음이 아님. 한 트랜잭션에서 일관성을 지켜야 하는 업무 불변식의 경계임.

## 연결 개념
- Bounded Context: 모델과 언어의 경계
- Aggregate: 트랜잭션과 불변식 경계
- Team Topology: 서비스 경계와 팀 소유권 정렬

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DDD 기반 분해 답안은 bounded context, aggregate, context map, team topology, 데이터 분리를 한 흐름으로 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DDD 기반 MSA 분해는 업무 언어와 책임 경계를 bounded context로 나누고 서비스·데이터·팀 소유권을 정렬하는 전략이다.
> 2. **가치**: 변경 영향 범위를 context 내부로 제한하고, 서비스별 독립 배포와 DB per Service의 근거를 제공함.
> 3. **판단 포인트**: aggregate 경계, context map 관계, cross-service transaction 처리 방식이 분해 품질을 결정함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MSA 분해 기준 확인 | bounded context, aggregate, ubiquitous language | 화면·테이블 기준 분해로 설명 |
| 데이터 분리 역량 확인 | DB per Service, event, Saga, Outbox | 공유 DB를 유지한 채 MSA라고 주장 |
| 조직 설계 관점 확인 | stream-aligned team, platform team, ownership | 기술 구조만 쓰고 팀 책임 누락 |

> 요약: 이 문제는 서비스를 몇 개로 쪼개는지가 아니라 업무 경계와 데이터 소유권을 맞추는지를 묻는다.

---

## Ⅰ. 개요 및 필요성

DDD 기반 MSA 분해는 도메인 경계로 서비스를 나누는 전략이다. MSA의 성패는 서비스 수보다 변경 이유가 같은 것끼리 묶고 다른 것은 분리하는 경계 품질에 달려 있다. DDD는 업무 언어, aggregate, context map으로 분해 근거를 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
Business Domain -> Subdomain -> Bounded Context -> Aggregate
                               -> Service Boundary -> DB per Service
Context Map -> API/Event Contract -> Team Ownership
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Subdomain | 핵심·지원·일반 도메인 구분 | core domain에 설계 역량 집중 |
| Bounded Context | 모델과 용어의 경계 | 같은 단어도 context별 의미 분리 |
| Aggregate | 트랜잭션 불변식 경계 | aggregate root를 통해 변경 |
| Context Map | context 간 의존 관계 표시 | upstream/downstream, ACL, conformist |

> 요약: DDD 분해는 subdomain에서 context를 찾고 aggregate와 데이터 소유권으로 서비스 경계를 확정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Event Storming -> 업무 이벤트 수집 -> Command/Policy 도출
-> Bounded Context 후보 도출 -> Aggregate 경계 결정
-> Context Map 작성 -> API/Event 계약 설계
-> Team Ownership과 배포 단위 확정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 도메인 이벤트와 명령 수집 | 핵심 업무 이벤트 30개 이상 도출 |
| 2 | 용어 충돌과 책임 경계 식별 | context별 ubiquitous language 분리 |
| 3 | aggregate와 트랜잭션 경계 결정 | 단일 aggregate transaction 유지 |
| 4 | API/Event contract 설계 | backward compatibility, schema version |
| 5 | 팀 소유권과 CI/CD 매핑 | 서비스 owner 1개 팀 명시 |

> 요약: DDD 분해는 이벤트와 언어를 모아 context를 찾고, aggregate와 팀 소유권으로 실행 가능한 서비스 경계를 만든다.

---

## Ⅳ. 특징

| 구분 | 기술 기준 분해 | DDD 기반 분해 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 경계 기준 | Controller/Service/DAO 계층 | bounded context, aggregate | 변경 1건당 context 1개 목표 |
| 데이터 | 공유 DB, cross join | DB per Service | 직접 DB 접근 0건 |
| 조직 | 기능별 팀 | stream-aligned team | 서비스 owner 1개 팀 |
| 정합성 | 단일 트랜잭션 의존 | Saga, 이벤트 정합성 | 보상 실패율 1% 이하 |

> 요약: DDD 기반 분해는 기술 계층이 아니라 업무 책임과 데이터 소유권을 기준으로 서비스 경계를 만든다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 테이블 중심 CRUD 서비스 | bounded context 서비스 | 변경 사유가 context 내부에 머무를 때 |
| 비용/성능 | 단일 DB join | API/event 조합 | p95 300ms 초과 호출 경로는 병합 검토 |
| 운영/위험 | 경계 불명확 | context map과 ownership | 공동 owner 서비스 0개 목표 |

> 요약: 서비스 경계는 기술 편의가 아니라 변경 응집도와 팀 소유권으로 검증해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 과분해 | aggregate를 엔티티 단위로 오해 | event storming 재수행, 서비스 병합 | 서비스당 월 변경 건수 |
| 공유 DB 회귀 | 레거시 join 의존 | CDC, anti-corruption layer, API 전환 | cross DB query 0건 |
| 팀 경계 불일치 | 기능별 조직 유지 | Team Topologies 적용 | 서비스 owner 명확도 100% |

> 요약: DDD 분해 리스크는 과분해와 공유 DB 회귀이며, context map과 owner 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 경계 품질 | 변경 1건당 수정 서비스 2개 이하 | issue, pull request 분석 |
| 데이터 독립성 | 서비스별 DB owner 100% | DB 권한, schema ownership 점검 |
| 계약 품질 | breaking change 월 0건 | contract test, schema registry |

> 요약: 분해 품질은 변경 영향, 데이터 소유권, 계약 호환성 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Event storming 워크숍으로 command, event, policy를 수집하고 core/supporting/generic subdomain을 구분함.
2. Bounded context별 aggregate root, DB owner, API/Event contract, SLA를 ADR과 context map으로 문서화함.
3. Consumer-driven contract test, schema registry, OpenTelemetry trace로 context 간 결합과 호출 지연을 측정함.

**결론 (2줄):**
- 기술사 판단: 서비스 경계가 업무 책임과 팀 소유권에 맞으면 MSA 분해를 진행하고, 용어·데이터 경계가 불명확하면 모듈형 모놀리스로 유예함.
- 향후 방향: DDD 분해는 Team Topologies와 플랫폼 자동화를 결합해 조직 구조와 소프트웨어 구조를 함께 설계하는 방향임.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DDD 기반 MSA 분해를 설명하시오" | event storming부터 context map까지 절차 | 기술 분해 대비 DDD 분해 차이 |
| 요구사항 명시형 | "분해 방안을 제시하시오", "설계하시오" | 대상 도메인 context와 aggregate 도출 | 데이터 분리, 팀 소유권, 리스크 대응 |

> 요약: 설명형은 DDD 요소를, 방안형은 실제 서비스 경계와 데이터 소유권 결정을 중심으로 전환한다.
