---
sidebar:
  order: 106
  label: "106. MongoDB 문서 데이터베이스 (MongoDB Document Database)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "MongoDB 문서 데이터베이스 (MongoDB Document Database)"
date: "2026-08-13T21:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **MongoDB**: JSON/BSON(Binary JSON) 문서 형태의 가변 데이터 모델(Document Model)을 사용하는 대표적인 범용 오픈소스 NoSQL 문서 데이터베이스.
- **BSON (Binary JSON)**: JSON 구조의 유연성을 유지하면서, 이진(Binary) 직렬화를 통해 빠르게 파싱하고 추가적인 데이터 타입(Date, 64-bit Int 등)을 인덱싱 지원하는 바이너리 문서 형식.
- **Replica Set & Sharding**: 1개의 Primary 노드와 n개의 Secondary 노드로 고가용성(HA)을 보장하는 Replica Set, 및 Config Server + Mongos 라우터를 기반으로 수평 확장(Scale-Out)하는 Sharding 아키텍처.

</details>

- 정의/개념: BSON 문서 모델을 사용하는 **MongoDB 문서 데이터베이스**
- 배경/필요성: 관계형 분해는 함께 조회하는 가변 객체에 **조인•변경 비용** 유발

#### 한줄 요약

- 함께 쓰는 상품 정보와 속성을 한 묶음 문서로 저장하는 데이터베이스이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Single Document Atomicity**: RDBMS의 다중 테이블 ACID 트랜잭션 대신, 단일 문서(Document) 내부의 서브 필드/배열 수정에 대해 100% 원자성(Atomicity) 보장.
- **Dynamic Schema**: 사전 `ALTER TABLE` DDL 없이 컬럼(필드)을 자유롭게 추가/수정 가능.

</details>

- **BSON 기반 모델링**: 데이터 내포(`Embedding`) 지원으로 데이터 접근성 최적화.
- **원자성 보장**: 단일 문서 갱신을 원자적으로 처리
- **운영 엔진**: `WiredTiger` 엔진(B+Tree 기반, 행 레벨 락, 데이터 압축) 및 `Replica Set`/`Sharding` 지원.

#### 한줄 요약

- 함께 쓰는 정보는 묶되 끝없이 커지거나 자주 중복되는 정보는 분리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Embedded vs Referenced**: 서브 문서로 내포(Embedded)하여 조인 0회를 달성할 것인가, DBRef 식별자로 참조(Referenced)하여 데이터를 쪼갤 것인가의 데이터 모델링 선택.

</details>

```text
[BSON 문서] ───── [컬렉션]
     │                 │
[인덱스] ─────── [WiredTiger]
     │                 │
[복제 세트] ───── [샤드 클러스터]
```

선의 의미: 문서 저장•색인•복제•분산 배치 책임 간 정적 관계.

| 구성요소 | 책임 |
|:---|:---|
| **BSON 문서** | 필드•배열•중첩 객체를 저장하는 원자 단위 |
| **컬렉션** | 관련 문서 집합과 검증 규칙 관리 |
| **인덱스** | 필드 기반 검색•정렬 경로 제공 |
| **WiredTiger** | 페이지•캐시•동시성•저널 관리 |
| **복제 세트** | Oplog 기반 복제와 주 노드 선출 |
| **샤드 클러스터** | 샤드 키 기반 문서 분산과 라우팅 |

#### 한줄 요약

- 문서 보관함과 색인, 사본 묶음, 안내자, 위치표로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Oplog (Operations Log)**: Primary 노드의 모든 CUD 데이터 변경 사항이 시계열 이진 기록으로 남는 특수 캡드 컬렉션(Capped Collection)으로, Secondary 노드가 이를 릴레이 복제.

</details>

```text
[주 노드 장애]
      │
      ▼
1. 하트비트 실패 감지
      │
      ▼
2. 선거 임기 시작
      │
      ▼
3. 과반수 투표 수행
      │
      ▼
4. 새 주 노드 선출
      │
      ▼
5. 쓰기 라우팅 갱신
      │
      ▼
[서비스 재개]
```

### 동작 원리

1. **하트비트 실패 감지**: 복제 세트가 주 노드 응답 상실 판정
2. **선거 임기 시작**: 후보가 임기 증가 후 투표 요청
3. **과반수 투표 수행**: 투표권 노드가 후보 적합성 판정
4. **새 주 노드 선출**: 과반수를 얻은 후보가 주 역할 획득
5. **쓰기 라우팅 갱신**: 드라이버가 토폴로지 변경 반영

#### 한줄 요약

- 안내자가 문서의 담당 샤드와 원본을 찾아 저장하고 요구한 사본 확인 뒤 응답한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Data Modeling Tradeoff**: Embedded는 조인이 없어 조회가 압도적으로 빠르나 문서 크기가 커지고 무한 성장 시 16MB 제한 도달, Referenced는 문서 크기가 작고 중복이 없으나 조인(`$lookup`) 연산 오버헤드 발생.

</details>

| 비교 항목 | Embedded Document Pattern (내포) | Referenced Document Pattern (참조) |
|:---|:---|:---|
| 데이터 결합 방식 | **단일 BSON 문서 내 서브 문서/배열 내포** | **`$lookup` 또는 앱 단 식별자 참조 결합** |
| 조회 결합 | **단일 문서 조회로 함께 반환** | `$lookup`•앱 추가 조회 필요 |
| 데이터 갱신 오버헤드| 데이터 중복 시 연쇄 수정 필요 | 단일 위치 갱신으로 무결성 우수 |
| 적합 데이터 유형 | **1:1 또는 1:N 유한한 서브 데이터 (주소 등)**| **1:N 무한 성과, N:M 복잡 다대다 데이터** |

#### 한줄 요약

- 항상 함께 쓰면 한 문서에 넣고 따로 커지거나 자주 공유하면 참조로 나눈다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **16MB Document Limit**: MongoDB 단일 Document의 최대 크기 한계로, 배열이 무한 성장(Unbounded Array)하면 16MB 에러가 나므로 분리 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 댓글 배열이 무한 성장하여 16MB 문서 제한 초과 | **댓글은 Referenced 패턴으로 별도 Collection 분리** | 16MB 제한 에러 방지 |
| Schema-Less 특성으로 무분별한 필드 파행 발생 | **JSON Schema Validation 도입으로 필수 필드 DB 레벨 검증**| 데이터 유효성 보존 |
| 복제 지연 시 읽기 불일치 발생 | **Read Concern / Write Concern 옵션 (`majority`) 강제** | 강한 일관성 달성 |

> 사례: **E-Commerce 상품-옵션 내포(Embedded) 모델링 및 MongoDB Replica Set 튜닝**

#### 한줄 요약

- 한 번에 읽을 정보는 묶되 끝없이 늘어나는 목록과 여러 곳에서 공유하는 정보는 분리한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **MongoDB 모델 수립 기준(MongoDB Architecture Standards)**: BSON 내포 구조 적합성, 16MB 한계 준수 및 Replica Set HA 구성에 의거한 체계.

</details>

- 함께 읽고 갱신하면 **Embedded**, 독립 성장•공유하면 Reference 선택

#### 한줄 요약

- MongoDB 모델 적용 기준은 함께 쓰는 자료의 문서 경계와 자주 찾는 분산 키를 맞춘다.
