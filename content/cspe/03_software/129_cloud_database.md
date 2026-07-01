---
title: "클라우드 DB - RDS·Aurora·DynamoDB 비교 (Cloud Database)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 129
---

# 📖 【암기용】 개념 완전 이해

> 목적: 클라우드 DB 비교를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 클라우드 환경에서 관리형으로 제공되는 관계형·분산·키값 데이터베이스 선택 문제
- **왜 필요한가**: 직접 DB를 설치하면 패치, 백업, 장애조치, 용량 증설을 운영자가 책임져야 한다. 클라우드 DB는 운영 부담을 서비스에 위임하지만 모델과 비용 구조가 달라 선택 기준이 필요하다.
- **핵심 직관**: 직접 주방을 운영할지, 표준 식당을 빌릴지, 자동화된 대형 급식 시스템을 쓸지 업무 메뉴에 맞춰 고르는 문제임

## 깊이 이해
- **배경·문제의식**: 클라우드 전환은 서버 이전만이 아니라 DB 운영 모델 변경을 포함한다. RDS는 관리형 RDB, Aurora는 클라우드 네이티브 관계형 DB, DynamoDB는 서버리스 key-value/document DB로 접근 방식이 다르다.
- **작동 원리**: RDS는 기존 엔진을 관리형으로 제공하고, Aurora는 컴퓨트와 분산 스토리지를 분리한다. DynamoDB는 파티션 키 기반으로 요청량을 분산하고 온디맨드 또는 프로비저닝 처리량을 사용한다.
- **비유**: RDS는 익숙한 사무실을 관리업체가 돌봐주는 형태, Aurora는 클라우드용으로 설계된 사무실, DynamoDB는 좌석 수를 자동으로 늘리는 무인 접수대에 가깝다.
- **구체 예시**: 기존 MySQL 업무는 RDS로 이전하고, 읽기 부하가 큰 주문 서비스는 Aurora read replica를 사용하며, 초당 수만 건 장바구니 세션은 DynamoDB 파티션 키로 분산함
- **흔한 오해·주의점**: 관리형 DB가 운영 책임을 모두 없애지는 않는다. 스키마 설계, 인덱스, 파티션 키, 비용 알람, 백업 복구 훈련은 사용자 책임 영역이다.

## 연결 개념
- Database as a Service - 관리형 DB 운영 모델
- RDBMS vs NoSQL - 데이터 모델 선택 기준
- Shared Responsibility - 클라우드 책임 분담

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 클라우드 DB 답안은 RDS·Aurora·DynamoDB의 모델, 일관성, 확장, 비용을 같은 축으로 비교해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 DB는 DB 설치·패치·백업·장애조치 일부를 클라우드 사업자가 제공하는 관리형 데이터 서비스임.
> 2. **가치**: 운영 자동화, 다중 AZ, 백업, 모니터링을 활용해 DB 운영 작업을 표준화함.
> 3. **판단 포인트**: RDS는 기존 RDB 호환, Aurora는 클라우드 네이티브 RDB, DynamoDB는 서버리스 NoSQL 기준으로 선택함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 DB 유형 구분 확인 | RDS, Aurora, DynamoDB 모델 차이 | 제품명 나열로 끝내지 않음 |
| 마이그레이션 판단 확인 | 호환성, 성능, 운영, 비용 축 | 모든 업무에 DynamoDB를 권장하지 않음 |
| 운영 책임 이해 확인 | 백업, 장애조치, 모니터링, 비용 알람 | 관리형 서비스의 사용자 책임 누락 방지 |

> 요약: 클라우드 DB 문제는 제품별 선택 기준과 운영 책임 경계를 비교하는 문제임.

---

## Ⅰ. 개요 및 필요성

클라우드 DB는 관리형 데이터베이스 서비스이다. 기업은 DB 패치·백업·장애조치·용량 증설 부담을 줄이면서 서비스 요구에 맞는 데이터 모델을 선택해야 한다. RDS, Aurora, DynamoDB는 호환성·확장·비용 구조가 다르므로 비교 판단이 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> Cloud DB Endpoint
  / RDS -> Managed Relational Engine -> Multi-AZ/Backup
  / Aurora -> Compute Node -> Distributed Storage -> Replica
  / DynamoDB -> Partition Key -> Partition -> Global Table
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| RDS | MySQL, PostgreSQL 등 관리형 RDB | 기존 SQL·엔진 호환 |
| Aurora | 분산 스토리지 기반 관계형 DB | read replica, storage 분리 |
| DynamoDB | 서버리스 key-value/document DB | partition key, capacity mode |
| 운영 계층 | 백업, 모니터링, 장애조치 | SLA·비용·권한 관리 |

> 요약: 클라우드 DB는 RDB 호환형, 클라우드 네이티브 RDB, 서버리스 NoSQL로 나뉨.

---

## Ⅲ. 동작원리 및 흐름도

```text
Requirement -> Data Model Classify -> Consistency/Scale Check -> Service Select -> Migration/Operation
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 업무 데이터 모델과 쿼리 패턴 분류 | SQL join, key lookup 비율 |
| 2 | 일관성·트랜잭션·확장 요구 확인 | ACID, TPS, p95 latency |
| 3 | RDS/Aurora/DynamoDB 후보 비교 | 호환성, 운영, 비용 |
| 4 | 마이그레이션과 백업 정책 수립 | RTO/RPO, rollback |
| 5 | 모니터링·비용 알람 운영 | CPU, IOPS, throttling |

> 요약: 클라우드 DB 선택은 데이터 모델과 일관성 요구를 먼저 분류한 뒤 서비스별 운영 특성을 비교함.

---

## Ⅳ. 특징

| 구분 | RDS | Aurora | DynamoDB |
|:---|:---|:---|:---|
| 모델 | 관리형 관계형 DB | 클라우드 네이티브 관계형 DB | key-value/document NoSQL |
| 강점 | 기존 DB 호환 | 읽기 확장, 분산 스토리지 | 서버리스 처리량, 글로벌 테이블 |
| 선택 기준 | lift-and-shift, SQL 호환 | RDB 유지+확장 요구 | 키 기반 대규모 요청 |

> 요약: RDS는 호환성, Aurora는 관계형 확장, DynamoDB는 키 기반 서버리스 확장이 선택 기준임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 자체 설치 DB | 관리형 DB | 패치·백업 운영 부담 이전 |
| 비용/성능 | 고정 인프라 | 인스턴스·IO·요청량 과금 | 월 비용, TPS, IOPS |
| 운영/위험 | 직접 장애조치 | 다중 AZ·자동 백업 | RTO/RPO, 책임 분담 |

> 요약: 클라우드 DB 선택은 호환성, 처리량, 비용, 책임 분담을 같은 축에서 비교해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 비용 초과 | IOPS·요청량·스토리지 증가 | budget alert, reserved capacity | 월 비용 편차 |
| 마이그레이션 장애 | SQL 호환성·데이터 변환 | DMS 리허설, dual write 검증 | cutover error count |
| 성능 병목 | 잘못된 인덱스·파티션 키 | slow query, hot partition 탐지 | p95 latency, throttling |

> 요약: 클라우드 DB 리스크는 비용, 이전, 병목을 사전 리허설과 모니터링으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | Multi-AZ, RTO 5분 이하 | 장애조치 훈련 |
| 성능 | p95 DB latency 50ms 이하 | CloudWatch, APM |
| 비용 | 월 예산 편차 10% 이하 | cost explorer, tag report |

> 요약: 클라우드 DB는 가용성, 지연시간, 비용 편차를 함께 점검한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 기존 SQL·조인 중심 업무는 RDS 우선, 읽기 확장과 분산 스토리지 이점이 필요하면 Aurora를 검토함.
2. 단순 키 조회·세션·장바구니·이벤트 상태는 DynamoDB partition key와 capacity mode를 설계함.
3. 마이그레이션은 CDC, dual run, rollback plan, RTO/RPO 검증을 포함해 최소 1회 이상 리허설함.

**결론 (2줄):**
- 기술사 판단: 호환성은 RDS, 관계형 확장은 Aurora, 키 기반 대규모 요청은 DynamoDB를 선택함.
- 향후 방향: 클라우드 DB는 서버리스, 글로벌 복제, 자동 튜닝과 결합되어 운영 자동화 범위를 넓힘.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "클라우드 DB를 설명하시오" | 요구사항 분류와 서비스 선택 흐름 | RDS·Aurora·DynamoDB 비교 |
| 요구사항 명시형 | "DB 클라우드 전환 방안을 제시하시오" | 마이그레이션·운영 절차 | 비용·성능·RTO/RPO 대응 |

> 요약: 설명형은 서비스 유형 비교, 방안형은 이전 절차와 운영 지표를 중심으로 작성함.
