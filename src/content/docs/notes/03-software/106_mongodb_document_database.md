---
sidebar:
  order: 106
  label: "106. MongoDB 문서 데이터베이스"
  badge:
    text: "기출 · 30%"
    variant: note
title: "MongoDB 문서 데이터베이스 (MongoDB Document Database)"
date: "2026-09-07T10:05:00+09:00"
tags:
  - "notes-software"
weight: 106
extra:
  question_no: "106"
  source_status: "기출"
  source_history: "137회"
  priority: 30
  priority_note: "137회 기출, 문서 모델 제품 사례 성격"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **BSON(Binary JSON)**: JSON의 계층적 가독성을 유지하면서 바이너리 직렬화를 통해 날짜, 바이너리 타입 및 빠른 파싱을 지원하는 MongoDB 저장 형식.
- **문서 데이터베이스(Document Database)**: 2차원 테이블 대신 BSON/JSON 도큐먼트 단위로 데이터를 저장하고 인덱싱하는 비관계형 DB.

</details>

- 정의/개념: 가변 구조의 BSON 문서 형태로 데이터를 저장하고 단일 문서 원자성, 복제 세트(HA) 및 샤딩(Scale-Out)을 지원하는 NoSQL 문서 데이터베이스
- 배경/필요성: RDBMS에서 복합 계층 객체 분해 시의 **다단계 조인(Join) I/O 병목 및 스키마 변경 시 무거운 DDL 마이그레이션 부담 한계**

#### 한줄 요약
- 문서 내포는 조인을 없애는 대신 함께 담긴 데이터를 항상 같이 읽고 쓰게 만드므로, 하위 항목이 무한히 늘어나는 관계에서는 내포가 오히려 비용으로 되돌아온다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Single Document Atomicity**: 단일 BSON 문서 내부의 필드 및 중첩 배열 수정에 대해 별도 트랜잭션 선언 없이도 100% ACID 원자성을 보장.
- **WiredTiger Engine**: B+Tree 기반 스토리지 엔진으로, 행 레벨 동시성 제어, 스냅샷 격리, 체크포인트 및 Snappy 압축 지원.

</details>

- 도메인 객체를 자연스럽게 표현하는 **BSON** 기반의 가변 스키마(Dynamic Schema)
- 조인 없이 단일 쿼리로 연관 데이터를 인출하는 문서 내포(Embedding) 최적화
- 자동 장애 조치(Failover)를 지원하는 Replica Set 및 분산 샤딩(Sharding) 아키텍처

#### 한줄 요약
- 유연한 BSON 문서 모델과 WiredTiger 엔진을 통해 고성능 읽기/쓰기와 수평 확장을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MongoDB 샤드 클러스터 구성요소**: Mongos(쿼리 라우터), Config Server(메타데이터 보관), Shard(데이터 저장 Replica Set).

</details>

```text
[MongoDB 아키텍처]
├─ [접근 계층]
│  └─ Mongos (쿼리 라우터·무상태 프록시)
├─ [메타데이터 계층]
│  └─ Config Server (샤드 키·청크 메타데이터)
├─ [데이터 저장 계층 (Shard)]
│  ├─ Shard Replica Set (데이터 분할 저장)
│  │  ├─ Primary (쓰기 전담)
│  │  └─ Secondary (Oplog 비동기 복제)
│  └─ WiredTiger 엔진 (문서 레벨 락·압축)
└─ [데이터 모델]
   └─ BSON 도큐먼트 (단일 문서 원자성)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| BSON 도큐먼트 | 중첩 객체의 원자적 저장 단위 |
| WiredTiger 스토리지 | 동시성·캐시·저널링 처리 |
| 복제 세트 | Oplog 복제와 자동 장애 조치 |
| 샤드 클러스터 | 샤드 키 기반 수평 분산 라우팅 |

#### 한줄 요약
- 복제 세트가 가용성을, 샤드 클러스터가 용량과 쓰기 처리량을 각각 담당하는 분리 구조이므로, 노드를 늘려도 샤드 키가 없으면 확장되는 것은 읽기 사본 수뿐이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Oplog(Operations Log)**: Primary 노드의 모든 변경 작업이 순차 기록되는 캡드 컬렉션으로, Secondary 노드들이 이를 비동기 재생하여 복제.

</details>

```text
Primary 노드에 비정상 다운 장애 발생
        │
    Secondary 노드 간 2초 주기 하트비트(Heartbeat) 응답 타임아웃 감지
        │
   [Raft 기반 선거] 가장 최신 Oplog를 보유한 Secondary가 Term을 올리고 선거 시작
        │
   [과반수 획득] 정족수(Majority) 투표를 획득한 노드가 즉시 신규 Primary로 승격
        │
    Mongos 라우터 및 클라이언트 드라이버가 토폴로지 변경을 감지하고 쓰기 트래픽 자동 재개
```

#### 한줄 요약
- Primary 승격은 과반 투표로만 성립해 노드가 짝수이거나 리전이 반씩 갈리면 승격 자체가 불가능하므로, 페일오버 소요 시간은 감지 주기보다 정족수를 어떻게 구성했느냐가 좌우한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **내포(Embedded) vs 참조(Referenced)**: 객체를 단일 문서 내에 배열로 포함하는 방식과 객체 ID로 분리하여 `$lookup`으로 연결하는 방식.

</details>

| 비교 항목 | 내포 패턴 (Embedded Document) | 참조 패턴 (Referenced Document) |
|:---|:---|:---|
| 데이터 모델 | 단일 문서 내 서브 도큐먼트/배열 포함 | 별도 컬렉션으로 분리 후 `_id` 참조 |
| 쿼리 성능 | 조인 0회 단일 읽기 (최고 속도) | 별도 쿼리 또는 `$lookup` 집계 파이프라인 필요 |
| 데이터 무결성 | 단일 문서 내 100% 원자적 수정 보장 | 다중 문서 트랜잭션 필요 |
| 권장 사용처 | 1:1 관계 또는 유한한 1:N 관계 (배송지 주소)| 1:N 무한 증가 관계 (댓글, 결제 이력) 또는 N:M |

#### 한줄 요약
- 함께 조회되고 크기가 유한하면 Embedded 패턴, 무한 증가하거나 다대다 관계이면 Referenced 패턴을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **16MB Document Limit**: MongoDB 단일 도큐먼트의 최대 허용 용량으로, 댓글/로그 배열이 무한 증식(Unbounded Growth)할 경우 에러 발생.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 댓글 배열 무한 증식으로 16MB 문서 용량 제한 초과 | 댓글/로그 데이터를 별도 컬렉션으로 분리하는 참조 패턴 적용 | 16MB 초과 에러 원천 차단 |
| 가변 스키마 특성으로 인한 불량 데이터 필드 유입 | JSON Schema Validation 규칙을 컬렉션에 선언하여 강제 검증 | 데이터 구조 무결성 유지 |
| 복제 지연으로 인한 Secondary 구버전 데이터(Stale) 조회 | 중요 비즈니스 쿼리에 `readConcern: majority` 옵션 명시 | 읽기 일관성 100% 확보 |
| 와일드카드 인덱스 남용으로 인한 메모리 고갈 | 자주 조회되는 복합 필드에 한해 명시적 B+Tree 인덱스 생성 | 인덱스 메모리 오버헤드 최소화 |

#### 한줄 요약
- 참조 분리 설계, JSON Schema 검증, Read Concern 설정, 복합 인덱스로 운용한다.

## Ⅶ. 결론

- 엔터프라이즈 NoSQL 생태계에서 가장 널리 활용되는 **표준 도큐먼트 지향 분산 데이터베이스**로 확립되었으며, 실무 아키텍처 구축 시에는 **유한한 연관 데이터는 조인 없는 BSON 문서 내포(Embedding)로 처리하고 1:N 무한 증가 데이터는 참조(Referenced)로 분리하며, 데이터 무결성 유지를 위한 JSON Schema Validation과 일관된 읽기를 보장하는 `readConcern: majority`, 쓰기 분산을 위한 샤드 클러스터 구성**을 결합하여 고성능과 데이터 안정성을 동시 확보

#### 한줄 요약
- MongoDB는 BSON 문서 내포와 복제·샤딩 클러스터를 통해 유연한 데이터 모델과 무중단 고가용성을 실현하는 대표적인 문서 데이터베이스다.
