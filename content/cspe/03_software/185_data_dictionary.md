---
title: 데이터 사전 Data Dictionary (Data Dictionary)
date: 2026-07-05
tags: ["cspe-software"]
weight: 185
---

## Ⅰ. 개요
- 정의: 시스템에 저장된 모든 객체(테이블, 뷰, 인덱스 등)에 대한 정보를 담고 있는 시스템 데이터베이스
- 배경: 객체 구조, 제약 조건, 소유자, 권한을 DBMS가 일관되게 참조하기 위한 메타데이터 관리
| 구분 | 내용 |
|------|------|
| 출제 의도 | Metadata의 종류와 데이터 사전(읽기 전용) vs 데이터 디렉토리(시스템용) 구분 |

## Ⅱ. 구성요소
  [ DBMS Engine ] <---(Reference)---> [ Data Dictionary ]
  [ Catalog ] -> [ Table Info, User Privileges, Constraints ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Meta-data | 데이터에 관한 데이터 (구조, 소유자, 권한) | 책 카탈로그 |
| System Table | DBMS가 관리하는 실제 물리적 테이블 | 장부 |
| Read-only | 일반 사용자는 수정 불가하고 조회만 가능 | 박물관 진열장 |
> 요약: 데이터베이스의 모든 자산 정보를 관리하는 중앙 저장소

## Ⅲ. 절차
  SQL Parse -> Dictionary Lookup -> Permission Check -> Execute
1. Query Receive: 사용자가 SQL 질의 요청
2. Validation: 사전에서 테이블명, 컬럼명 존재 여부 확인
3. Authorization: 사전의 사용자 권한 정보를 대조하여 실행 여부 결정
4. Execution: 확인된 메타 정보를 바탕으로 물리 데이터 접근
> 요약: SQL 실행 전 객체 존재 여부와 사용자 권한을 확인하고 저장 구조 정보를 제공함

## Ⅳ. 문제점
- 사전 조회 빈도가 높을 경우 시스템 카탈로그 병목 현상 발생
- 시스템 카탈로그 손상 시 데이터베이스 전체 구동 불가

## Ⅴ. 개선방안
- 데이터 사전 전용 캐시(Data Dictionary Cache) 운영
- 사전 테이블의 주기적 백업 및 이중화 관리

## Ⅵ. 전망
- 데이터 카탈로그와 결합한 전사 데이터 거버넌스(Data Governance) 통합 도구로 확장
