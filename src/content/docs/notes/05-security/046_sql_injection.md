---
sidebar:
  order: 46
  label: "046. SQL 인젝션"
  badge:
    text: "기출 · 50%"
    variant: note
title: "동적 쿼리 구문 변조 및 데이터베이스 침해 방어 : SQL 인젝션"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 46
extra:
  question_no: "46"
  source_status: "기출"
  source_history: "120회, 123회"
  priority: 50
  priority_note: "CWE-89, 동적 쿼리 조작 메커니즘, 준비된 질의(PreparedStatement/매개변수화 쿼리), In-Band/Blind/OOB 분류 및 최소 권한 DB 계정"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SQL Injection (SQL 인젝션, CWE-89)**: 사용자 입력값이 동적 SQL 쿼리에 결합되어 쿼리 구조가 변조됨으로써 DB를 탈취당하는 취약점.
- **Code-Data Mingling (코드와 데이터의 혼재)**: 실행 명령어(Code)와 처리 대상 값(Data)이 단일 문자열로 섞여 전달될 때 발생하는 결함.

</details>

- 정의/개념: 비신뢰 입력을 쿼리 인터프리터로부터 격리하기 위해 **PreparedStatement와 매개변수화 바인딩을 통해 데이터베이스를 보호하는 기술**
- 배경/필요성: 동적 SQL 문자열 결합으로 인한 **코드와 데이터의 혼재, 입력값의 쿼리 문법 재해석에 따른 전사 DB 탈취 및 위변조**

#### 한줄 요약
- PreparedStatement 매개변수 바인딩을 통해 입력값을 순수 데이터로 격리 처리하여 쿼리 변조를 원천 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PreparedStatement (준비된 질의)**: SQL 쿼리 실행 계획을 사전에 컴파일하여 고정하고, 사용자 입력값은 단순 리터럴 데이터로 대입하는 객체.
- **Parameterized Query**: 쿼리 구조 내에 위치 홀더(`?` 또는 `:param`)를 두고 실행 시점에 파라미터를 바인딩하는 기법.

</details>

- **구문과 데이터의 완벽한 물리적 분리**: 입력값에 따옴표나 특수문자가 포함되어도 **쿼리 문법 구조가 절대 변경되지 않고 데이터 리터럴로만 해석**
- **실행 계획 사전 컴파일(Pre-compilation)**: DB 엔진이 쿼리 구조를 **사전에 파싱하여 최적화함으로써 공격자의 구문 주입 무력화 및 성능 향상**
- **심층 방어(Defense-in-Depth) 연계**: 입력값 화이트리스트 검증, **DB 계정의 최소 권한(Least Privilege), 상세 에러 메시지 은닉 병행 필수**

#### 한줄 요약
- 구문과 데이터 분리, 사전 컴파일 기반 고속 처리, 심층 방어(최소 권한/에러 은닉)를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Least Privilege DB Account**: 웹 애플리케이션 계정에 DDL(`DROP`, `ALTER`) 및 시스템 프로시저 권한을 제거하고 최소 DML만 허용하는 보안 원칙.

</details>

```text
[PreparedStatement 기반 SQL 인젝션 방어 아키텍처]
|-- Untrusted Client Input (1. 공격자 페이로드 입력: admin' OR '1'='1)
`-- Web Application Layer
    |-- Input Validation (화이트리스트 정규식 검증)
    `-- PreparedStatement Engine (2. SELECT * FROM users WHERE id = ? 사전 컴파일)
    `-- Parameter Binder (물음표 위치에 문자열 그대로 매핑)
`-- Database Engine (3. DBMS Execution: 재파싱 없이 순수 리터럴 데이터로 매칭 -> 인증 실패)
```

선의 의미: 사용자 입력이 화이트리스트 검증을 거쳐 PreparedStatement 매개변수로 바인딩되어 DBMS에서 순수 데이터로 안전하게 처리되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **입력 검증 모듈** | 정규표현식 및 화이트리스트를 통해 **데이터의 타입, 길이, 허용 문자열 검증** | Validation |
| **PreparedStatement** | SQL 쿼리 실행 계획을 사전에 컴파일하여 **쿼리 트리 구조를 고정** | Pre-compile |
| **매개변수 바인더** | 사용자 입력을 **특수문자 이스케이프 필요 없이 순수 데이터로 치환** | Binding |
| **최소 권한 DB 계정**| 웹 서비스용 계정의 **DDL(`DROP`/`ALTER`) 및 시스템 권한 박탈** | DB Privileges |
| **에러 마스킹 모듈** | 쿼리 오류 발생 시 **상세 SQL 구문 및 스키마 노출을 차단** | Error Masking |

#### 한줄 요약
- 입력 검증 모듈, PreparedStatement 컴파일러, 매개변수 바인더, 최소 권한 DB 계정, 에러 마스킹이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PreparedStatement vs Dynamic Query**: 동적 쿼리는 문자열 결합 시 문법이 파괴되나, PreparedStatement는 입력값을 메모리 데이터로만 대조.

</details>

```text
클라이언트 요청, 쿼리 사전 컴파일, 매개변수 바인딩 및 에러 은닉 파이프라인
        │
   1. [클라이언트 요청] 공격자가 로그인 폼 아이디에 `' OR '1'='1` 악성 페이로드 입력
        │
   2. [쿼리 구조 사전 컴파일] `SELECT * FROM users WHERE id = ?` 구조를 전달하여 실행 계획 고정
        │
   3. [매개변수 바인딩] DB 드라이버가 물음표(`?`) 위치에 입력값을 순수 문자열(Data)로 안전 대입
        │
   4. [DBMS 실행] DB 파서가 재파싱 없이 `id`가 정확히 `' OR '1'='1`인 행을 단순 조회 ➔ [불일치 인증 실패]
        │
   ▼
5. [결과 반환 및 에러 은닉] 데이터가 없으므로 "로그인 실패" 정상 응답 반환 (내부 에러 노출 0%)
```

#### 한줄 요약
- 쿼리 사전 컴파일 → 매개변수 바인딩 → 리터럴 데이터 조회 → 안전한 실패 응답 → 에러 은닉 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **인밴드 (In-Band)** vs **블라인드 (Blind)** vs **아웃오브밴드 (Out-of-Band)**.

</details>

| 비교 항목 | 인밴드 SQL 인젝션 (In-Band SQLi) | 블라인드 SQL 인젝션 (Blind SQLi) | 아웃오브밴드 SQL 인젝션 (OOB SQLi) |
|:---|:---|:---|:---|
| **데이터 탈취 경로** | **동일 웹 요청/응답 화면 (직접 노출)** | **참/거짓 응답 차이 또는 서버 응답 시간 지연**| **DNS 쿼리, HTTP 요청 등 외부 네트워크 채널** |
| **주요 세부 기법** | **UNION 기반 질의, 에러 기반(Error-based)**| **Boolean-based Blind, Time-based Blind** | **`xp_dirtree`(MSSQL), `UTL_HTTP`(Oracle)**|
| **공격 수행 속도** | **매우 빠름 (수 초 내 대량 데이터 탈취)** | 느림 (이진 검색으로 한 글자씩 비트 추론) | 빠름~보통 (대역폭 및 외부 통신 허용 여부 좌우)|
| **화면 출력 차단 시** | 공격 성립 불가 | **화면 출력이 차단되어도 100% 데이터 탈취 가능**| 화면 출력이 차단되어도 외부 채널로 유출 가능 |
| **핵심 네트워크 방어** | WAF 입력값 필터링 및 시큐어 코딩 | 시큐어 코딩 및 WAF 비정상 질의 탐지 | **DB 서버의 아웃바운드(Egress) 인터넷 통신 차단**|

#### 한줄 요약
- In-Band는 화면 직접 노출, Blind는 참/거짓 및 시간차 추론, OOB는 외부 DNS/HTTP 채널 악용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ORM MyBatis `${}` vs `#{}`**: `${param}`은 단순 문자열 치환으로 SQLi 취약, `#{param}`은 PreparedStatement 바인딩으로 안전.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| WAF 필터링에만 의존하다 **난독화/인코딩 우회 SQL 인젝션 공격에 의해 DB 전체 유출** | **모든 SQL 쿼리에 `PreparedStatement 매개변수화 바인딩 의무화 (MyBatis #{} 강제)`** | 구문-데이터 물리적 분리로 인코딩 우회 100% 차단 |
| `ORDER BY` 및 테이블명 등 바인딩 불가 영역에 **동적 결합하여 발생하는 2차 인젝션** | **동적 식별자에 대한 `정적 화이트리스트(Allowlist) 매핑 및 유효성 엄격 검증`** | 바인딩 한계 영역의 우회 인젝션 공격 100% 방어 |
| SQL 인젝션 공격 침해 시 **DB 계정이 관리자(sa) 권한을 보유하여 전사 DB 일괄 삭제** | **`DB 계정의 최소 권한(Least Privilege) 원칙 적용 및 DB 아웃바운드 차단`** | 침해 시 타 테이블 확산 및 OOB 데이터 유출 차단 |
| 세컨더리(2차) 인젝션으로 인한 백엔드 배치 작업 오염 | **`DB 저장 후 재인출 시점에도 입력 검증 및 매개변수화 쿼리`** 일관 적용 | 저장된 악성 페이로드의 2차 실행 원천 차단 |

#### 한줄 요약
- PreparedStatement로 구문을 분리하고, 화이트리스트로 동적 영역을 보호하며, 최소 권한으로 피해를 격리한다.

## Ⅶ. 결론

- 웹 애플리케이션과 백엔드 데이터베이스 간의 신뢰 경계를 수호하는 **SQL 인젝션 방어 아키텍처는 데이터 무결성과 기밀성 보호의 최우선 핵심 과제**이며, 실무 구현 시 **PreparedStatement 및 ORM `#{}` 매개변수화 쿼리 전면 도입, 바인딩 불가 영역에 대한 정적 화이트리스트(Allowlist) 검증, DB 계정의 최소 권한(Least Privilege) 격리, 상세 DB 에러 메시지 은닉 및 아웃바운드 차단**을 결합하여 무결점 데이터베이스 보호 환경 완성

#### 한줄 요약
- SQL 인젝션 방어는 PreparedStatement 매개변수 바인딩과 화이트리스트 검증 및 최소 권한 계정을 통해 쿼리 변조를 원천 차단하는 시큐어 코딩의 핵심이다.