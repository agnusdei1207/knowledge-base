---
title: "SQL 기본 — DML·DDL·DCL (SQL DML DDL DCL)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 105
extra:
  question_no: "105"
  exam_status: "미출제"
  exam_note: "기본"
---

## 미리 알고가기

- SQL은 관계형 데이터베이스를 정의하고 조작하고 통제하는 표준 언어임
- DDL은 구조 정의, DML은 데이터 조작, DCL은 권한 통제를 담당함
- 실무에서는 트랜잭션과 권한과 변경 절차를 함께 고려해야 함

## Ⅰ. 개요

- **정의/개념**: SQL 기본 분류에서 DDL은 테이블과 인덱스와 제약조건 같은 데이터 구조를 정의하고, DML은 데이터를 조회·삽입·수정·삭제하며, DCL은 사용자 권한과 접근 통제를 관리하는 관계형 데이터베이스 표준 언어 체계임
- **배경/필요성**: 데이터 관리 작업은 구조 변경과 데이터 처리와 접근 통제가 서로 다른 목적과 위험을 가지므로, 명확한 언어 구분과 운영 절차가 필요함

## Ⅱ. 특징

- 선언형 언어라 원하는 결과를 중심으로 표현함
- DDL과 DML과 DCL은 책임이 달라 운영 통제 기준도 다름
- 단순 구문 숙지보다 변경 영향과 권한 범위를 이해하는 것이 중요함
- 잘못된 SQL은 즉시 데이터 손상이나 권한 노출로 이어질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | DDL | DML | DCL |
|:---|:---|:---|:---|
| 목적 | 구조 정의·변경 | 데이터 조회·조작 | 권한 부여·회수 |
| 대표 명령 | CREATE, ALTER, DROP | SELECT, INSERT, UPDATE, DELETE | GRANT, REVOKE |
| 주요 위험 | 스키마 파괴와 호환성 문제 | 대량 오조작과 정합성 저하 | 과권한과 접근 통제 실패 |
| 운영 포인트 | 배포 절차와 검토 필수 | 트랜잭션과 검증 중요 | 최소 권한 원칙 적용 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Schema Definition | DDL로 테이블과 인덱스와 제약조건 구조를 형성함 |
| Data Manipulation | DML로 업무 데이터를 읽고 변경하며 트랜잭션과 결합됨 |
| Access Control | DCL로 사용자와 역할의 권한 범위를 제한함 |
| Execution Governance | 실행 승인과 로그와 롤백 절차로 운영 위험을 관리함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 구조 정의      | --> | 데이터 조작     | --> | 권한 통제      | --> | 실행 이력 관리  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **구조 정의**: DDL로 스키마와 제약조건을 설정함
2. **데이터 조작**: DML로 조회와 변경 작업을 수행함
3. **권한 통제**: DCL로 접근 범위를 조정함
4. **실행 이력 관리**: 감사 로그와 변경 절차를 남김

## Ⅵ. 문제점 및 해결 방안

1. 문제: DDL 변경을 애플리케이션 배포와 분리 없이 수행하면 서비스 호환성과 데이터 안정성이 동시에 흔들릴 수 있음
   - 해결방안: schema migration pipeline을 운영하고 migration success rate와 compatibility defect count로 검증함
2. 문제: 대량 DML 실행 전에 범위 검증이 없으면 운영 데이터 훼손이 즉시 확산될 수 있음
   - 해결방안: preview query와 safe guard clause를 적용하고 accidental update incident count와 rollback success rate로 검증함
3. 문제: DCL 권한이 느슨하면 개발 편의는 높아도 보안 사고와 내부 오용 가능성이 커질 수 있음
   - 해결방안: least privilege review를 정기화하고 excessive privilege count와 access violation rate로 검증함

## Ⅶ. 적용 사례

- 운영 DB 배포에서는 마이그레이션 파이프라인을 적용하고 확인 지표는 migration success rate와 compatibility defect count임
- 데이터 정정 작업에서는 범위 검증 절차를 수행하고 확인 지표는 accidental update incident count와 rollback success rate임
- 보안 감사 조직에서는 최소 권한 검토를 운영하고 확인 지표는 excessive privilege count와 access violation rate임

## Ⅷ. 결론

SQL 기본 분류를 이해한다는 것은 문법 암기보다 구조 변경과 데이터 조작과 권한 통제를 서로 다른 위험 영역으로 보고 다르게 운영하는 데 있음.
