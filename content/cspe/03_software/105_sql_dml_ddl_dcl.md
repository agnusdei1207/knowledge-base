---
title: "SQL 기본 — DML·DDL·DCL (SQL DML DDL DCL)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 105
---

# 📖 【암기용】 개념 완전 이해

> 목적: SQL 명령 분류를 처음 보는 사람도 DML, DDL, DCL, TCL의 책임 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: SQL 명령어는 데이터를 다루는 **DML**, 구조를 바꾸는 **DDL**, 권한을 다루는 **DCL**, 트랜잭션 경계를 정하는 **TCL** 네 갈래로 나뉘는 **관계형 DB 질의어(SQL)** 체계다.
- **왜 필요한가**: `UPDATE`, `ALTER`, `GRANT`, `COMMIT`은 모두 SQL 문이지만 영향 범위(값·구조·권한·확정여부)와 롤백 가능성이 완전히 다르다. 운영 사고를 막으려면 명령 성격별로 다른 통제가 필요하다.
- **핵심 직관**: DML은 장부에 내용을 쓰는 것, DDL은 장부 양식 자체를 바꾸는 것, DCL은 장부 열람권을 주는 것, TCL은 "저장" 또는 "취소" 버튼을 누르는 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| SQL (상위 개념) | 관계형 DB에 질의·조작을 지시하는 표준 언어 — 아래 4갈래로 구성됨 | DB와 대화하는 공용 언어 |
| DML (Data Manipulation Language) | 행 데이터 조회·삽입·수정·삭제 — SELECT, INSERT, UPDATE, DELETE | 장부에 거래 내용을 적고 지움 |
| DDL (Data Definition Language) | 테이블·인덱스 등 객체 구조 생성·변경·삭제 — CREATE, ALTER, DROP, TRUNCATE | 장부 양식(칸 구성) 자체를 새로 짬 |
| DCL (Data Control Language) | 사용자 권한 부여·회수 — GRANT, REVOKE | 장부 열람·기입 권한증 발급 |
| TCL (Transaction Control Language) | 트랜잭션 확정·취소 경계 지정 — COMMIT, ROLLBACK, SAVEPOINT | 장부 작성 후 "확정" 또는 "취소" 도장 |
| auto commit | DDL 실행 시 DBMS가 자동으로 트랜잭션을 확정해버리는 동작 | 도장을 안 눌렀는데 자동으로 확정 처리됨 |

## 깊이 이해

### 4분류를 판별하는 질문
- "이 명령이 바꾸는 대상이 무엇인가?"로 구분한다. 행 값을 바꾸면 DML, 테이블·인덱스 같은 구조(스키마)를 바꾸면 DDL, 누가 접근할 수 있는지를 바꾸면 DCL, 지금까지의 변경을 확정할지 취소할지를 정하면 TCL이다.

### DELETE·TRUNCATE·DROP — 셋 다 "지우기"지만 소속이 다르다
- `DELETE FROM orders WHERE ...`는 DML이다. 행 단위로 로그를 남기고 조건절을 쓸 수 있으며, COMMIT 전이면 ROLLBACK으로 되돌릴 수 있다. 100만 행을 지우면 각 행의 undo 로그가 쌓여 수 분이 걸릴 수 있다.
- `TRUNCATE TABLE orders`는 DDL이다. 조건절 없이 테이블 전체를 페이지 단위로 초기화하므로 100만 행이어도 1초 내외로 끝나지만, 대부분의 DBMS에서 자동 커밋되어 되돌리기 어렵다.
- `DROP TABLE orders`는 DDL이다. 데이터뿐 아니라 테이블 정의 자체를 카탈로그에서 제거한다.
- 판별 기준: "행만 지우나(DML)" vs "구조·전체를 지우나(DDL)".

### auto commit 함정 — DDL이 앞뒤 DML까지 확정시킨다
- 일부 DBMS(예: 오라클)는 DDL 실행 시 암묵적으로 COMMIT을 수행한다. 예를 들어 `UPDATE orders SET status='PAID' WHERE id=1;` 실행 직후 `ALTER TABLE orders ADD COLUMN memo VARCHAR(100);`을 실행하면, 이 ALTER 시점에 앞선 UPDATE까지 함께 커밋되어 버린다. 그 뒤 `ROLLBACK`을 호출해도 이미 확정된 UPDATE는 되돌아오지 않는다. 그래서 DDL은 별도 트랜잭션·배포 시간대에 분리해 실행해야 한다.

### TCL 세부: COMMIT·ROLLBACK·SAVEPOINT
- COMMIT은 지금까지의 변경을 영구 확정하고, ROLLBACK은 마지막 COMMIT 시점까지 되돌린다. SAVEPOINT는 트랜잭션 중간에 "부분 되돌리기 지점"을 찍는다.
- 예: 결제 처리에서 포인트 차감 후 `SAVEPOINT sp1`을 찍고, 카드 승인을 시도한다. 카드 승인이 실패하면 `ROLLBACK TO sp1`으로 포인트 차감만 취소하고, 그 이전에 만들어둔 주문 레코드(있다면)는 유지한 채 나머지 로직을 이어갈 수 있다.

### DCL과 최소 권한(least privilege)
- 배치 계정에 SELECT와 INSERT 권한만 GRANT하고 DROP·ALTER 권한을 주지 않으면, 배치 스크립트에 버그가 있어 `DROP TABLE`을 실행하려 해도 권한 부족(insufficient privilege)으로 DB가 거부한다. GRANT/REVOKE는 "누가 어떤 명령군까지 쓸 수 있는가"의 경계를 긋는 도구다.

### 비유
- 식당 운영에 비유하면: 주문서에 메뉴를 적고 지우는 것은 DML, 메뉴판 양식을 통째로 새로 인쇄하는 것은 DDL, 주방 출입증을 발급·회수하는 것은 DCL, 하루 장사를 마감 정산하거나 취소하는 것은 TCL이다.

## 연결 개념
- 트랜잭션(ACID) — TCL이 확정·취소의 경계를 정하는 대상
- 권한 관리(RBAC) — DCL을 실무에서 운용하는 방식
- 스키마 마이그레이션 — DDL 변경을 안전하게 배포하는 절차

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SQL 분류는 명령 암기가 아니라 데이터·스키마·권한·트랜잭션 영향 범위를 구분하는 운영 통제 기준이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SQL은 DML, DDL, DCL, TCL로 나뉘며 각각 데이터 조작, 객체 구조, 접근 권한, 트랜잭션 경계를 담당한다.
> 2. **가치**: 명령군별 권한, 감사, 배포 절차를 분리해 데이터 손실과 운영 중단을 줄인다.
> 3. **판단 포인트**: DDL auto commit, 대량 DML lock, DCL 최소 권한, TCL rollback 가능 범위를 DBMS별로 확인해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SQL 기본 분류 이해 확인 | DML·DDL·DCL·TCL 명령과 책임 | TCL 누락 또는 DCL과 혼동 |
| 운영 영향 판단 확인 | lock, auto commit, 권한, 감사 로그 | 명령어 목록만 나열 |
| 실무 통제 절차 확인 | migration, least privilege, transaction boundary | DROP/TRUNCATE 위험 설명 누락 |

> 요약: 이 문제는 SQL 명령을 업무 영향과 운영 통제 기준으로 분류하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: SQL은 관계형 DB 표준 질의 언어이다.
- 배경: DML, DDL, DCL, TCL은 데이터 값, 객체 구조, 권한, 트랜잭션 경계를 바꾸며 롤백 가능 범위가 다르다.
- 필요성: 운영 DB에서는 대량 DML lock, DDL auto commit, DCL 최소권한, TCL rollback 기준을 명령군별로 통제해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
SQL 요청 -> 명령군 분류 -> 권한 검사 -> 실행 계획/DDL 처리 -> 트랜잭션 확정
           / DML
           / DDL
           / DCL
           / TCL
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| DML | SELECT, INSERT, UPDATE, DELETE로 행 조작 | 트랜잭션 rollback 대상 |
| DDL | CREATE, ALTER, DROP, TRUNCATE로 객체 변경 | DBMS별 auto commit 주의 |
| DCL | GRANT, REVOKE로 권한 제어 | 최소 권한과 감사 로그 필요 |
| TCL | COMMIT, ROLLBACK, SAVEPOINT로 경계 제어 | 장기 트랜잭션은 lock·undo 증가 |
| Catalog | 테이블·인덱스·권한 메타데이터 저장 | DDL 실행 시 갱신 |

> 요약: SQL 명령 체계는 행 데이터, 스키마 객체, 권한, 트랜잭션 경계를 분리해 DB 변경을 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SQL 입력 -> Parser -> 권한 검사 -> 명령군별 실행 -> Commit/Rollback 또는 감사 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SQL 파싱과 객체명 해석 | syntax error 0건 |
| 2 | DCL 기반 권한 확인 | unauthorized access 0건 |
| 3 | DML은 optimizer와 executor 수행 | row count, explain plan 확인 |
| 4 | DDL은 catalog와 storage 구조 변경 | migration log, lock time 확인 |
| 5 | TCL로 트랜잭션 확정·취소 | commit 성공, rollback 가능성 확인 |

> 요약: SQL은 파싱, 권한 검사, 명령군별 실행, 트랜잭션 처리 순서로 수행되며 감사 가능해야 한다.

---

## Ⅳ. 특징

| 구분 | DML | DDL | DCL/TCL |
|:---|:---|:---|:---|
| 목적 | 데이터 조회·변경 | 스키마 객체 생성·변경 | 권한·트랜잭션 제어 |
| 대표 명령 | SELECT, INSERT, UPDATE, DELETE | CREATE, ALTER, DROP | GRANT, REVOKE, COMMIT |
| 운영 위험 | 대량 update lock, undo 증가 | metadata lock, rollback 제한 | 권한 과다, 장기 트랜잭션 |
| 통제 지표 | affected rows, p95 query time | lock time, migration duration | 권한 변경 건수, commit 지연 |

> 요약: DML은 데이터 영향, DDL은 구조 영향, DCL/TCL은 권한과 확정 경계를 기준으로 통제한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 DBA 수작업 | SQL 명령군별 권한·승인 분리 | 운영 DB, 개인정보, 원장 테이블 |
| 비용/성능 | 즉시 실행 | online DDL, batch DML, savepoint | 무중단 배포와 lock 1초 이하 목표 |
| 운영/위험 | 권한 공유 | RBAC, 감사 로그, migration tool | 변경 추적과 재현성 필요 |

> 요약: 운영 환경에서는 SQL 명령군별 권한과 배포 절차를 나누어 실수와 영향 범위를 제한한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 대량 DML 장애 | 한 트랜잭션에서 100만 행 변경 | batch 5,000건 commit, throttling | lock wait 1초 이하 |
| DDL 중단 | metadata lock, table rewrite | online DDL, blue-green schema | migration time 10분 이하 |
| 권한 오남용 | GRANT 과다, 계정 공유 | RBAC, MFA, quarterly review | privileged account 0개 공유 |

> 요약: SQL 운영 리스크는 대량 변경, 구조 변경, 권한 변경으로 나누어 별도 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| DML 품질 | affected rows 사전 예측 오차 5% 이하 | dry-run select count |
| DDL 배포 | lock time 1초 이하, rollback plan 존재 | migration log |
| 권한 감사 | 불필요 권한 0건 | DB privilege report |

> 요약: SQL 변경은 실행 전 영향 행 수, lock 시간, 권한 적정성을 수치로 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 운영 권한을 DML read, DML write, DDL migration, DCL admin으로 분리하고 GRANT/REVOKE는 ticket id와 감사 로그를 남김
2. 대량 DML은 `SELECT count(*)`로 영향 행을 산정한 뒤 batch 5,000건 단위 commit과 sleep 100ms를 적용함
3. DDL은 migration tool로 versioning하고 online DDL 가능 여부, lock time 1초 이하, rollback SQL을 배포 조건으로 둠

**결론 (2줄):**
- 기술사 판단: SQL 분류는 문법 암기가 아니라 운영 변경의 권한·감사·복구 단위를 나누는 기준임
- 향후 방향: GitOps 기반 schema migration과 DB 접근 제어를 결합해 SQL 변경을 코드와 동일한 승인 체계로 관리해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SQL 명령을 설명하시오" | 파싱, 권한 검사, 명령군별 실행 흐름 | DML·DDL·DCL·TCL 비교 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "비교하시오" | 대량 DML, online DDL, DCL 감사 절차 | 권한·락·롤백 기준 |

> 요약: 설명형은 명령 분류, 운영형은 lock·권한·트랜잭션 통제 중심으로 작성한다.
