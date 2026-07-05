---
title: "SQL 인젝션 (SQL Injection)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 70
---

# 📖 【암기용】 개념 완전 이해

> 목적: SQL 인젝션을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사용자 입력이 SQL 명령 구조에 섞여 DB가 공격자 의도대로 조회·수정·삭제 명령을 실행하는 공격
- **왜 필요한가**: DB에는 개인정보, 결제, 계정, 업무 데이터가 있으므로 SQL Injection은 정보 유출과 데이터 변조로 바로 이어진다.
- **핵심 직관**: 주문서의 "상품명" 칸에 창고 직원에게 내리는 명령문을 적어 시스템이 물건 주문이 아니라 창고 명령으로 해석하게 만드는 공격이다.

## 깊이 이해
- **배경·문제의식**: 웹 애플리케이션은 사용자 입력으로 DB 질의를 만든다. 문자열 결합으로 `WHERE id='입력값'`을 만들면 입력값 안의 따옴표와 SQL 조각이 질의 구조를 바꾼다.
- **작동 원리**: 공격자는 로그인, 검색, 정렬, 쿠키, HTTP 헤더, JSON 필드에 SQL 구문을 넣어 인증 우회, UNION 조회, blind 추론, time-based 지연, error-based 정보 수집을 시도한다.
- **비유**: 식당 예약 이름 칸에 "예약 취소 명령"을 적었는데 직원이 이름이 아니라 명령으로 처리하는 상황이다.
- **구체 예시**: 안전하지 않은 `SELECT * FROM users WHERE id = ' + input` 구조에서 `1 OR 1=1` 입력이 조건을 항상 참으로 바꾸면 전체 사용자 조회가 가능하다.
- **흔한 오해·주의점**: 입력값 검증만으로 충분하지 않다. Prepared Statement, parameterized query, ORM의 안전 API, DB 최소 권한, 오류 메시지 제어, WAF 탐지를 함께 적용해야 한다.

## 연결 개념
- OWASP Top 10 A05 Injection - 2025 기준 인젝션 위험군
- Parameterized Query - SQL 코드와 데이터를 분리하는 핵심 방어
- Least Privilege - DB 계정 권한 제한으로 피해 범위 축소

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SQL Injection 답안은 공격 문자열 예시보다 신뢰 경계, 질의 생성 흐름, parameterized query, DB 권한, 로그 재검증을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SQL Injection은 신뢰할 수 없는 입력이 SQL 인터프리터의 명령 구조로 해석되는 인젝션 공격임.
> 2. **가치**: Prepared Statement와 parameterized query로 SQL 코드와 데이터를 분리하면 질의 구조 변조를 차단할 수 있음.
> 3. **판단 포인트**: ORM 사용 여부보다 동적 SQL, 저장 프로시저 내부 문자열 결합, DB 계정 권한, 오류 처리, WAF 로그를 함께 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 웹 공격 원리 이해 확인 | 입력값, SQL 생성, 인터프리터 실행, 인증 우회·정보 유출 | 공격 payload만 나열 |
| 방어 기법 판단 확인 | parameterized query, ORM safe API, allow-list validation | escaping만 단독 대책으로 제시 |
| 운영 통제 확인 | WAF, DB 최소 권한, error handling, logging, retest | 애플리케이션 코드 수정 이후 재검증 누락 |

> 요약: 이 문제는 SQLi 원리와 방어 위치를 질의 생성 전, DB 실행 전, 운영 탐지 단계로 나누어 제시해야 함.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 사용자 입력이 SQL 명령 구조에 섞여 DB가 공격자 의도대로 조회·수정·삭제 명령을 실행하는 공격 | "이 개념의 핵심" |
| **왜 필요한가** | DB에는 개인정보, 결제, 계정, 업무 데이터가 있으므로 SQL Injection은 정보 유출과 데이터 변조로 바로 이어진다 | "이 개념의 핵심" |
| **핵심 직관** | 주문서의 "상품명" 칸에 창고 직원에게 내리는 명령문을 적어 시스템이 물건 주문이 아니라 창고 명령으로 해석하게 만드는 공격이다 | "이 개념의 핵심" |
| **배경·문제의식** | 웹 애플리케이션은 사용자 입력으로 DB 질의를 만든다 | "이 개념의 핵심" |
| **비유** | 식당 예약 이름 칸에 "예약 취소 명령"을 적었는데 직원이 이름이 아니라 명령으로 처리하는 상황이다 | "이 개념의 핵심" |
| **흔한 오해·주의점** | 입력값 검증만으로 충분하지 않다 | "이 개념의 핵심" |
| **본질** | SQL Injection은 신뢰할 수 없는 입력이 SQL 인터프리터의 명령 구조로 해석되는 인젝션 공격임 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성

- 개요: DB 질의 변조 공격
- 배경: 사용자 입력이 검증·바인딩 없이 SQL 문자열에 결합되면 공격자는 조건식, UNION, 주석을 삽입해 인증 우회와 데이터 유출을 수행할 수 있음.
- 필요성: OWASP ASVS, Prepared Statement, DB 최소 권한을 적용해 웹/API 입력 경계에서 질의 구조와 데이터 값을 분리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
사용자 입력 -> 웹/API 파라미터 -> SQL 생성 로직
          -> DB 드라이버/ORM -> DB 권한 계정 -> 결과/오류 응답
          -> WAF/로그/SIEM 탐지
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 입력 지점 | 검색어, 로그인, 정렬, JSON, Cookie 수신 | 모든 외부 입력은 불신 |
| SQL 생성 로직 | 질의 템플릿과 파라미터 결합 | 문자열 결합 금지 |
| Parameter Binding | SQL 코드와 데이터 분리 | Prepared Statement, bind variable |
| DB 권한 | 계정별 실행 권한 제한 | SELECT 전용, DDL 금지 |
| 탐지/로그 | 공격 시도와 오류 패턴 관측 | WAF, DB audit, SIEM |

> 요약: SQLi 방어는 입력 지점, 질의 생성, DB 실행 권한, 오류 응답, 로그 탐지 지점에 통제를 배치해야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
공격 입력 수신 -> 문자열 결합 SQL 생성 -> DB 인터프리터 실행
-> 조건 변조/UNION/error/time 지연 -> 데이터 조회/변조
-> 로그 탐지 -> 코드 수정 -> 재검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자 입력이 파라미터, 헤더, 쿠키로 유입 | untrusted source 목록화 |
| 2 | 애플리케이션이 SQL 문자열을 생성 | prepared statement 적용률 100% |
| 3 | DB가 변조된 SQL을 실행 | DB 계정 DDL/DCL 권한 0건 |
| 4 | 결과, 오류, 시간 지연으로 정보 노출 | 상세 DB 오류 외부 노출 0건 |
| 5 | WAF/DB audit/SIEM으로 탐지 후 재검증 | DAST retest pass 100% |

> 요약: SQLi는 입력이 SQL 구조로 승격되는 순간 발생하며, 코드-데이터 분리와 DB 권한 제한으로 실행 피해를 줄임.

---

## Ⅳ. 특징

| 구분 | 취약 구현 | SQLi 방어 구현 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 질의 생성 | 문자열 결합 | parameterized query | 적용률 100% |
| 입력 검증 | blacklist 필터 | allow-list, type/length 검증 | 정렬 컬럼 allow-list |
| DB 권한 | 앱 계정에 DDL 권한 | 업무별 SELECT/INSERT 제한 | DDL/DCL 0건 |
| 오류 처리 | DB 오류 외부 노출 | 공통 오류 메시지, 내부 로그 | 외부 stack trace 0건 |
| 탐지 | 로그 미수집 | WAF, DB audit, SIEM rule | SQLi alert triage 24시간 |

> 요약: SQLi 방어는 prepared statement를 기본으로 하고 입력 검증, 최소 권한, 오류 제어, 운영 로그를 보완 통제로 둔다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | escaping 중심 | parameter binding 중심 | 모든 사용자 입력 기반 SQL |
| 비용/운영 | 빠른 임시 조치 | 코드 수정과 테스트 필요 | 인증·결제·개인정보 API |
| 위험 통제 | WAF 탐지 의존 | 코드-데이터 분리 + DB 권한 제한 | WAF 우회 가능성 고려 |

> 요약: WAF와 escaping은 보완 통제이며, 근본 방어는 parameterized query와 동적 SQL 제거임.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 동적 SQL 잔존 | 검색·정렬·리포트 기능 | allow-list, query builder safe API | 문자열 결합 SQL 0건 |
| ORM 오남용 | raw query 직접 실행 | ORM parameter binding 규칙 | raw query code review 100% |
| 저장 프로시저 취약 | 내부에서 문자열 결합 | bind variable, 권한 분리 | dynamic exec 사용 0건 |
| 피해 확대 | DB 계정 과다 권한 | least privilege, row-level security | 앱 계정 DDL/DCL 0건 |

> 요약: SQLi 잔존 리스크는 동적 SQL과 권한 과다에서 발생하므로 코드 리뷰와 DB 권한 점검을 함께 수행해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 안전 질의 | prepared statement 적용률 100% | SAST, code review |
| 취약점 검증 | SQLi DAST finding 0건 | DAST, penetration test |
| DB 권한 | 앱 계정 DDL/DCL 0건 | DB privilege audit |
| 운영 탐지 | WAF/DB audit alert 24시간 내 triage | SIEM case, WAF 로그 |

> 요약: 성공 여부는 안전 질의 적용률, DAST 결과, DB 권한, 운영 탐지 처리 시간으로 확인함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 코드 방어: Prepared Statement, parameterized query, ORM safe API를 표준으로 정하고 raw SQL은 보안 리뷰 승인과 단위 테스트를 필수화함.
2. 보완 통제: 입력값은 allow-list와 type/length 검증을 적용하고 WAF SQLi rule, DB audit, SIEM alert를 운영함.
3. 피해 제한: 애플리케이션 DB 계정은 업무별 SELECT/INSERT/UPDATE 권한만 부여하고 DDL/DCL, 파일 접근, 관리자 권한을 제거함.

**결론 (2줄):**
- 기술사 판단: 신규 개발은 parameterized query 100% 적용, 레거시는 WAF 임시 차단 후 문자열 결합 SQL 제거를 우선순위로 둬야 함.
- 향후 방향: API, GraphQL, ORM raw query, LLM 생성 코드까지 SQLi 검증 범위를 넓히고 SAST/DAST 재검증을 CI/CD에 포함해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SQL Injection을 설명하시오" | 입력값이 SQL 구조를 바꾸는 공격 흐름 | 취약 구현과 방어 구현 비교 |
| 요구사항 명시형 | "방어 방안을 제시하시오", "취약점 개선 방안을 설계하시오" | parameterized query, ORM, DB 권한, WAF 로그 | 조치 SLA, retest, 최소 권한 |

> 요약: 설명형은 공격 원리, 방안형은 코드 수정과 운영 탐지·재검증을 중심으로 답안을 구성함.
