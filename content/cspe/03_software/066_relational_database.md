---
title: 관계형 데이터베이스 RDBMS (Relational Database)
date: 2026-07-05
tags: [cspe-software]
weight: 66
---

## Ⅰ. 개요
- 데이터를 표(Table) 형태로 표현하며 열(Column)과 행(Row)의 관계로 구성한 모델임.
- E.F. Codd의 12규칙에 기반하며 SQL을 통해 데이터 정의, 조작, 제어를 수행함.
- 출제 의도: 집합론 기반의 관계 대수와 ACID 트랜잭션 보장 원리 이해 확인.

## Ⅱ. 구성요소
- 논리적 구조
[Table (Relation)] -> [Row (Tuple)] / [Column (Attribute)]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Schema | 테이블의 구조, 타입, 제약조건 명세 | 아파트 설계도 |
| Instance | 실제 테이블에 저장된 데이터의 집합 | 아파트 입주 세대 |
| Primary Key | 튜플을 고유하게 식별하는 최소 슈퍼키 | 주민등록번호 |
> 요약: 스키마가 정의한 구조 내에서 인스턴스가 관계를 형성함.

## Ⅲ. 절차
- 릴레이션 조작 (관계 대수)
[Input Tables] -> (Select/Project) -> (Join) -> [Output]

1. 셀렉션(Select): 조건에 맞는 튜플을 수평적으로 추출함.
2. 프로젝션(Project): 필요한 속성을 수직적으로 추출함.
3. 조인(Join): 공통 속성을 매개로 두 테이블을 결합함.
4. 디비전(Division): 특정 조건을 모두 만족하는 튜플 검색함.
> 요약: 연산자를 통해 논리적 관계를 조합하여 결과 집합 생성함.

## Ⅳ. 문제점
- 데이터 모델과 객체지향 모델 간의 불일치(Impedance Mismatch) 및 대용량 쓰기 지연.

## Ⅴ. 개선방안
- ORM(Object-Relational Mapping) 프레임워크 활용 및 CQRS 패턴 적용으로 부하 분산.

## Ⅵ. 전망
- 고가용성을 보장하는 Multi-Region 복제와 분산 트랜잭션을 지원하는 방향으로 진화.
- 분산 관계형 DB(Global RDBMS)가 엔터프라이즈 핵심 인프라로 지속 활용될 전망임.
