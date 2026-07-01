---
title: "MongoDB 도큐먼트 DB (MongoDB Document Database)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 122
---

# 📖 【암기용】 개념 완전 이해

> 목적: MongoDB 도큐먼트 DB를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: JSON 유사 BSON 문서 단위로 데이터를 저장·조회하는 NoSQL DB
- **왜 필요한가**: 주문, 사용자 프로필, 콘텐츠처럼 속성이 자주 바뀌는 데이터는 테이블 조인과 스키마 변경 비용이 커진다. MongoDB는 한 객체의 관련 속성을 한 문서에 묶어 읽기 경로를 단순화한다.
- **핵심 직관**: 한 고객 파일철 안에 주소, 선호도, 최근 주문 일부를 함께 넣어 한 번에 꺼내는 방식임

## 깊이 이해
- **배경·문제의식**: 관계형 모델은 정규화와 조인으로 중복을 줄이지만, 객체 구조와 테이블 구조 차이로 ORM 매핑 비용이 생긴다. MongoDB는 문서 내 중첩 배열과 필드 유연성으로 애플리케이션 객체와 저장 구조를 가깝게 만든다.
- **작동 원리**: 컬렉션에 BSON 문서를 저장하고, `_id` 기본 인덱스와 보조 인덱스로 조회한다. 복제셋은 primary-secondary 구조로 가용성을 확보하고, 샤딩은 shard key 기준으로 데이터를 분산한다.
- **비유**: 도서관 카드가 아니라 책 한 권 안에 목차, 저자, 리뷰, 태그를 함께 보관해 한 번에 펼쳐보는 방식임
- **구체 예시**: 상품 상세 화면에서 상품 기본정보, 옵션, 최근 리뷰 10건을 한 문서에 저장하면 조인 3회를 단건 문서 조회 1회로 줄일 수 있음
- **흔한 오해·주의점**: 스키마가 없다는 의미는 설계가 없다는 뜻이 아니다. 문서 크기, 배열 증가, shard key, 인덱스 카디널리티를 설계하지 않으면 쓰기 지연과 청크 불균형이 발생한다.

## 연결 개념
- 도큐먼트 모델 - 컬렉션·문서·필드 기반 저장 구조
- 샤딩(Sharding) - shard key 기반 수평 분산
- CAP 정리 - 복제셋 장애조치와 일관성 판단 배경

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: MongoDB 답안은 "스키마리스"가 아니라 문서 모델링, 인덱스, 복제셋, 샤딩 판단까지 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MongoDB는 BSON 문서를 컬렉션에 저장하고 문서 단위 원자성, 복제셋, 샤딩을 제공하는 도큐먼트 DB임.
> 2. **가치**: 객체 중심 읽기 경로에서 조인 수를 줄이고, 필드 변경이 잦은 서비스의 배포-스키마 변경 결합을 낮춤.
> 3. **판단 포인트**: 문서 내장(embedding)과 참조(reference), shard key, 인덱스 선택이 처리량과 저장량을 좌우함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| NoSQL 유형별 판단 확인 | 도큐먼트 모델, BSON, 컬렉션, 문서 원자성 | RDB 대체재로만 설명하지 않음 |
| 분산 DB 설계 역량 확인 | replica set, primary election, shard key | 샤딩을 수평 분산이라는 말로 끝내지 않음 |
| 모델링 기준 확인 | embedding vs reference, 인덱스, 문서 크기 | 중첩 배열 무제한 설계 누락 방지 |

> 요약: MongoDB 문제는 문서 모델링과 분산 구조를 함께 써야 채점 포인트를 충족함.

---

## Ⅰ. 개요 및 필요성

MongoDB는 BSON 문서 기반 NoSQL 데이터베이스이다. 애플리케이션 객체 구조가 복잡하고 필드 변경이 잦은 서비스에서 정규화 테이블 조인만으로는 읽기 지연과 배포 조정 비용이 커진다. MongoDB는 도큐먼트 저장, 복제셋, 샤딩으로 객체 중심 데이터 처리를 지원한다.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> Driver -> Collection -> BSON Document -> Index
                          +-> Replica Set -> Primary / Secondary
                          +-> Shard Key -> Shard Cluster
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| BSON 문서 | 중첩 객체·배열 저장 | 문서 단위 원자성 |
| 컬렉션 | 문서 그룹 관리 | 유연 스키마, validator 설정 가능 |
| 인덱스 | 조회 조건 가속 | compound, text, TTL, geo |
| 복제셋/샤드 | 고가용·수평 분산 | primary election, chunk balancing |

> 요약: MongoDB는 문서 저장 계층 위에 인덱스, 복제셋, 샤딩을 결합해 읽기·가용성·분산 요구를 처리함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request -> Query Planner -> Index Scan/Collection Scan -> Document Fetch -> Result Return
Write -> Primary Commit -> Oplog Replication -> Secondary Apply
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 드라이버가 쿼리·쓰기 요청 전달 | connection pool, timeout |
| 2 | query planner가 후보 실행계획 평가 | explain plan, nReturned |
| 3 | 인덱스 스캔 후 문서 로딩 | keysExamined/docsExamined 비율 |
| 4 | primary 쓰기와 oplog 기록 | writeConcern, journal commit |
| 5 | secondary 반영 및 장애조치 | replication lag, election time |

> 요약: MongoDB는 쿼리 계획과 인덱스로 문서를 찾고, 쓰기는 primary에서 oplog로 복제함.

---

## Ⅳ. 특징

| 구분 | 관계형 DB | MongoDB | 판단 포인트 |
|:---|:---|:---|:---|
| 모델 | 테이블·행·정규화 | 컬렉션·문서·중첩 필드 | 객체 단위 읽기 비율 |
| 트랜잭션 | 조인·다중 행 중심 | 문서 단위 원자성, 다중 문서 트랜잭션 | 쓰기 범위와 지연 목표 |
| 분산 | 파티션·복제 구성 의존 | replica set, sharding 내장 | shard key 카디널리티 |

> 요약: MongoDB는 객체 중심 조회와 수평 분산에 적합하나, 조인 중심 분석 업무는 관계형 모델을 우선 검토함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RDB 정규화 | 도큐먼트 내장/참조 혼합 | 단건 화면 조회 시 조인 3회 이상 |
| 비용/성능 | 조인·스키마 변경 | 문서 조회·필드 유연성 | p95 조회 지연, 인덱스 크기 |
| 운영/위험 | SQL 튜닝 중심 | shard key·balancer 운영 | hot shard 비율, chunk 이동량 |

> 요약: MongoDB 선택은 스키마 유연성보다 조회 패턴과 shard key 분포로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 문서 비대화 | 무제한 배열 내장 | bucketing, reference 분리 | document size p95 |
| hot shard | 낮은 shard key 카디널리티 | hashed key, compound key | shard별 ops 편차 20% 이내 |
| 인덱스 과다 | 필드별 무분별한 생성 | compound index, unused index 제거 | index size/data size |

> 요약: MongoDB 운영 리스크는 문서 크기, shard key 분포, 인덱스 수명주기로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 조회 | docsExamined/nReturned 10 이하 | explain, profiler |
| 복제 | replication lag p95 2초 이하 | replSetGetStatus |
| 분산 | shard별 데이터 편차 20% 이내 | balancer status, chunk 통계 |

> 요약: MongoDB 도입 후에는 쿼리 효율, 복제 지연, 샤드 균형을 정량 점검한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 화면 단위 읽기 모델을 기준으로 embedding, 참조 관계는 변경 빈도와 배열 증가량 기준으로 분리함.
2. shard key는 카디널리티·쓰기 분포·쿼리 조건을 함께 평가하고, hot shard 알람 기준을 ops 편차 20%로 둠.
3. `explain`과 profiler로 collection scan을 제거하고, TTL·compound index는 사용 통계 기준으로 유지함.

**결론 (2줄):**
- 기술사 판단: 객체 단위 조회와 필드 변화가 크면 MongoDB, 복잡 조인·강한 정합성 중심이면 RDB를 선택함.
- 향후 방향: 도큐먼트 DB는 이벤트·검색·캐시 계층과 결합되어 polyglot persistence의 한 축으로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MongoDB를 설명하시오" | 쿼리 계획, oplog 복제, 샤딩 흐름 | RDB와 도큐먼트 모델 비교 |
| 요구사항 명시형 | "도큐먼트 DB 설계 방안을 제시하시오" | embedding/reference, shard key 결정 | 리스크 대응과 점검 지표 |

> 요약: 설명형은 구조·원리, 설계형은 모델링과 shard key 선택 기준을 전면에 둔다.
