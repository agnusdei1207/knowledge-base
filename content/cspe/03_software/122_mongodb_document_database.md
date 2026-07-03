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
- **개요**: MongoDB는 **NoSQL** 중에서도 **도큐먼트 데이터베이스(Document Database)**로, JSON과 유사한 BSON 형식의 문서 단위로 데이터를 저장·조회하는 시스템이다.
- **왜 필요한가**: 주문, 사용자 프로필, 콘텐츠처럼 속성이 자주 바뀌는 데이터는 관계형 모델에서 테이블 조인과 스키마 변경 비용이 커진다. MongoDB는 한 객체의 관련 속성을 한 문서에 묶어 읽기 경로를 단순화한다.
- **핵심 직관**: 한 고객 파일철 안에 주소, 선호도, 최근 주문 일부를 함께 넣어 한 번에 꺼내는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| NoSQL | MongoDB가 속하는 상위 범주 — 관계형 모델의 고정 스키마·조인 대신 유연한 구조를 쓰는 DB 계열 | 관계형 DB의 대안 계열 |
| 도큐먼트 데이터베이스 | 문서(중첩 객체) 단위로 저장·조회하는 NoSQL의 세부 유형 | MongoDB가 속한 분류 |
| BSON (Binary JSON) | JSON을 바이너리로 확장한 MongoDB의 저장 포맷. 날짜·이진데이터 등 타입을 추가 지원 | JSON에 타입 정보를 더한 확장판 |
| 컬렉션 (Collection) | 문서들을 담는 그룹, 관계형 DB의 테이블에 대응 | 문서들이 모인 폴더 |
| _id | 문서를 유일하게 식별하는 기본 키, 자동으로 인덱스 생성 | 문서의 고유 등록번호 |
| 문서 원자성 | 단일 문서 내 모든 필드 변경이 원자적으로(전부 성공/전부 취소) 처리됨 | 한 파일철 안의 수정은 전부 되거나 전부 안 됨 |
| Embedding (내장) | 관련 데이터를 하나의 문서 안에 중첩해서 저장 | 리뷰를 상품 문서 안에 함께 보관 |
| Reference (참조) | 관련 데이터를 별도 문서로 두고 ID로 연결 | 별도 파일철을 참조번호로 연결 |
| Replica Set (복제셋) | Primary 1개 + Secondary 여러 개로 구성된 고가용성 단위, 장애 시 자동 재선출 | 본점 장애 시 지점이 업무를 대행 |
| Oplog | Primary의 모든 쓰기 연산을 기록해 Secondary가 재생하는 복제 로그 | 본점 거래 내역을 지점이 그대로 따라 적음 |
| Sharding (샤딩) | Shard Key 기준으로 데이터를 여러 서버(shard)에 수평 분산 | 고객번호 기준으로 서버를 나눔 |
| Shard Key | 샤딩 시 문서를 어느 shard로 보낼지 정하는 기준 필드 | 데이터를 나누는 분류 기준 |
| Index (인덱스) | 조회 조건을 가속하는 자료구조(주로 B-Tree) | 책 뒤의 찾아보기 색인 |

## 깊이 이해

### 왜 문서 하나에 다 묶나 — 조인 비용과의 관계
- 관계형 모델은 정규화로 중복을 줄이지만, 상품 상세 화면 하나를 그리려면 상품·옵션·리뷰 테이블을 조인해야 한다. MongoDB는 자주 함께 조회되는 데이터를 문서 하나에 내장(embedding)해서 조인 여러 번을 문서 조회 1번으로 줄인다. 예: 상품 기본정보+옵션+최근 리뷰 10건을 한 문서에 담으면 조인 3회가 `findOne()` 1회로 줄어든다 — 네트워크 왕복(RTT)이 3회에서 1회로 줄어드는 만큼 응답 지연이 낮아진다.
- 반대로 무한히 늘어날 수 있는 데이터(예: 상품의 전체 리뷰 수만 건)를 문서에 통째로 내장하면 BSON 문서 크기 제한(16MB)에 걸리거나 쓰기마다 문서 전체를 다시 써야 해 느려진다 — 이럴 땐 별도 컬렉션에 두고 참조(reference)로 연결한다.

### 조회 흐름: 쿼리 플래너와 인덱스가 만드는 차이
- 요청이 오면 query planner가 후보 실행계획(인덱스 스캔 vs 전체 컬렉션 스캔)을 평가해 가장 적은 문서를 검사하는 계획을 고른다. 예: 100만 건 컬렉션에서 email 필드로 조회할 때 인덱스가 없으면 100만 건을 전부 훑는 collection scan이 되지만, email에 인덱스를 만들면 B-Tree 탐색으로 약 log₂(1,000,000)≈20번 비교 수준으로 줄어든다 — 이 차이는 `explain()`의 `docsExamined` 값으로 직접 확인할 수 있다.

### 쓰기 흐름과 복제: Primary-Secondary-Oplog
- 쓰기는 Primary에서 먼저 처리되고 oplog(연산 로그)에 기록된다. Secondary들은 이 oplog를 비동기로 가져와 순서대로 재생(replay)해 같은 상태를 따라간다. Primary가 장애나면 Secondary 중 하나가 선거(election)를 통해 새 Primary가 된다 — 이 과정에 보통 수 초가 걸리며, 그 사이 쓰기 요청은 실패하거나 대기한다.
- writeConcern 설정으로 "Primary만 확인(w:1)"할지 "과반수 확인(w:majority)"할지 정할 수 있다 — 전자는 빠르지만 Primary 장애 시 그 쓰기가 유실될 수 있고, 후자는 느리지만 안전하다. 이는 최종 일관성·PACELC에서 본 latency-consistency 트레이드오프가 MongoDB 안에서 그대로 재현된 것이다.

### 수평 분산: Shard Key 선택이 성능을 좌우하는 이유
- 샤딩은 shard key 값의 범위(또는 해시)로 데이터를 청크 단위로 나눠 여러 shard 서버에 분산한다. 예: 주문 컬렉션에서 shard key를 `주문일자`로 잡으면 최근 주문이 항상 같은 shard에 몰려 그 shard만 쓰기가 폭주하는 hot shard가 발생한다. 반면 `해시(고객ID)`를 shard key로 쓰면 쓰기가 여러 shard에 고르게 분산된다 — shard key 선택은 카디널리티(값의 다양성)와 쓰기 분산을 함께 봐야 한다.

### 판별원리: MongoDB를 쓸 때 vs RDB를 쓸 때
- 조회가 "객체 하나를 통째로 가져오는" 패턴이 많고 필드 구조가 자주 바뀌면 MongoDB가 유리하다. 반대로 여러 테이블을 넘나드는 복잡한 조인·집계, 강한 트랜잭션 정합성(다중 테이블 ACID)이 중심이면 RDB가 유리하다. "스키마가 없다"는 말은 "설계가 필요 없다"는 뜻이 아니라 스키마를 애플리케이션 계층에서 유연하게 다룬다는 뜻일 뿐, 문서 크기·배열 증가·shard key는 여전히 사전 설계가 필요하다.

### 비유
- 도서관에서 책 정보, 저자 정보, 리뷰를 각각 다른 카드 서랍(테이블)에 나눠 보관하고 필요할 때마다 서랍을 여러 번 여닫는 것이 관계형 DB의 조인이라면, MongoDB는 책 한 권 표지 안쪽에 목차·저자소개·리뷰 요약을 다 인쇄해 한 번만 펼치면 되는 방식이다.

## 연결 개념
- 도큐먼트 모델 — 컬렉션·문서·필드 기반 저장 구조
- 샤딩(Sharding) — shard key 기반 수평 분산
- CAP 정리 — 복제셋 장애조치와 일관성 판단의 배경
- 최종 일관성 — writeConcern·readPreference 설정에 따라 MongoDB가 보이는 일관성 수준

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

- 개요: MongoDB는 BSON 문서 기반 NoSQL DB이다.
- 배경: 애플리케이션 객체 구조가 복잡하고 필드 변경이 잦은 서비스에서는 정규화 테이블 조인만으로 읽기 지연과 배포 조정 비용이 커진다.
- 필요성: BSON 문서, 복제셋, 샤딩을 사용해 객체 중심 데이터 모델과 수평 분산 처리를 지원한다.

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
