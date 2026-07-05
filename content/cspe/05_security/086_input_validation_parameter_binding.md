---
title: "입력값 검증·파라미터 바인딩 (Input Validation Parameter Binding)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 86
---

# 📖 【암기용】 개념 완전 이해

> 목적: 입력값 검증·파라미터 바인딩을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 외부 입력을 허용된 형식으로 제한하고 SQL·명령·쿼리와 데이터 값을 분리하는 방어 기법
- **왜 필요한가**: 웹 요청의 파라미터, JSON Body, Header는 모두 신뢰 경계 밖에서 온다. 검증 없이 DB 질의나 명령어에 붙이면 SQL Injection, XSS, Command Injection으로 이어진다.
- **핵심 직관**: 입력값 검증은 "문 앞 신분 확인", 파라미터 바인딩은 "명령문과 손님 말을 서로 다른 칸에 넣는 것"임

## 깊이 이해
- **배경·문제의식**: `id=1 OR 1=1` 같은 문자열이 SQL 문장 일부로 해석되면 인증 우회와 대량 조회가 발생한다. 입력값 검증은 타입·길이·범위·스키마를 먼저 제한하고, 바인딩은 SQL 템플릿과 값을 DB 드라이버가 별도로 전달하게 한다.
- **작동 원리**: Allowlist로 필드별 허용 문자와 범위를 정하고, JSON Schema·Bean Validation으로 구조를 검증한 뒤, Prepared Statement의 `?` 또는 named parameter에 값을 바인딩한다. 실패 시 400 응답과 보안 로그를 남긴다.
- **비유**: 택배 접수에서 주소·무게·품목을 정해진 칸에 쓰게 하고, 운송 지시서 문구는 직원만 작성하게 하는 절차와 같다.
- **구체 예시**: 사용자 조회는 `SELECT * FROM users WHERE id = ?`로 고정하고 `id`는 정수 1~2147483647만 허용한다. `1 OR 1=1` 입력은 타입 검증에서 차단되고 SQL 문장으로 결합되지 않는다.
- **흔한 오해·주의점**: Client JavaScript 검증은 UX용이다. 보안 통제는 API Gateway, Controller, Service, DAO 경계에서 서버 측 재검증과 바인딩으로 수행해야 한다.

## 연결 개념
- SQL Injection - 문자열 결합 질의가 만드는 대표 취약점
- OWASP ASVS - 입력 검증, 출력 인코딩, 인증 검증 기준
- ORM 보안 - 동적 JPQL·native query 사용 시 바인딩 누락 위험

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 입력 검증을 "값 확인"으로만 쓰지 않고, 신뢰 경계별 검증 위치와 DB 바인딩 실패 모드를 연결해 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 입력값 검증·파라미터 바인딩은 외부 입력을 allowlist·type·length·schema로 제한하고 SQL 문장과 값을 분리해 Injection 해석을 차단하는 통제임
> 2. **가치**: OWASP Top 10 Injection 대응에서 문자열 결합 제거, 서버 측 재검증, 400/422 실패 처리, 감사로그를 한 흐름으로 묶음
> 3. **판단 포인트**: 클라이언트 검증, 서버 검증, DB 바인딩 중 어디가 신뢰 경계인지 구분하고 동적 SQL·검색 조건·배치 입력까지 재검증해야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Injection 원인과 차단 기법 구분 | allowlist, type, length, JSON Schema, Prepared Statement | blacklist 필터만 쓰거나 특수문자 제거로 답안 종료 |
| 신뢰 경계별 검증 위치 판단 | Browser -> API Gateway -> Controller -> DAO 재검증 | 클라이언트 검증을 보안 통제로 간주 |
| 실패 모드와 로그 설계 확인 | 400/422 응답, field error, 원본값 마스킹 로그, 차단율 | DB 오류 노출, 입력 원문 전체 로그 저장 |

> 요약: 이 문제는 입력값을 어디서 어떤 기준으로 거부하고, SQL 실행 시 명령과 값을 어떻게 분리하는지 묻는다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 외부 입력을 허용된 형식으로 제한하고 SQL·명령·쿼리와 데이터 값을 분리하는 방어 기법 | "이 개념의 핵심" |
| **왜 필요한가** | 웹 요청의 파라미터, JSON Body, Header는 모두 신뢰 경계 밖에서 온다 | "이 개념의 핵심" |
| **핵심 직관** | 입력값 검증은 "문 앞 신분 확인", 파라미터 바인딩은 "명령문과 손님 말을 서로 다른 칸에 넣는 것"임 | "이 개념의 핵심" |
| **배경·문제의식** | `id=1 OR 1=1` 같은 문자열이 SQL 문장 일부로 해석되면 인증 우회와 대량 조회가 발생한다 | "이 개념의 핵심" |
| **비유** | 택배 접수에서 주소·무게·품목을 정해진 칸에 쓰게 하고, 운송 지시서 문구는 직원만 작성하게 하는 절차와 같다 | "이 개념의 핵심" |
| **구체 예시** | 사용자 조회는 `SELECT * FROM users WHERE id = ?`로 고정하고 `id`는 정수 1~2147483647만 허용한다 | "이 개념의 핵심" |
| **흔한 오해·주의점** | Client JavaScript 검증은 UX용이다 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성

- 개요: 입력 검증·질의 값 분리 통제
- 배경: 웹·API 요청은 신뢰 경계 밖에서 오므로 타입, 길이, 범위, 스키마 검증 없이 SQL·명령·HTML에 연결하면 Injection이 발생함.
- 필요성: OWASP ASVS, allowlist 검증, Prepared Statement, ORM parameter binding을 적용해 입력 해석 위치를 DB 드라이버와 검증 계층으로 제한해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client Input -> API Gateway -> Controller Validation -> Service Rule
             -> DAO Prepared Statement -> DB Execution -> Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 입력 스키마 | 필드명, 타입, 길이, 범위, 필수값 정의 | JSON Schema, OpenAPI, Bean Validation |
| 서버 측 검증기 | 신뢰 경계 진입 시 allowlist 검증 | 실패 시 400/422, 원인 코드 분리 |
| 파라미터 바인더 | SQL 템플릿과 데이터 값 분리 | JDBC PreparedStatement, ORM named parameter |
| 감사 로그 | 차단 이벤트와 호출자 추적 | 원본 비밀번호·토큰 마스킹, request-id 저장 |

> 요약: 입력 스키마로 허용 범위를 좁히고, DAO에서 바인딩으로 SQL 해석 경계를 고정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> 필드 존재 확인 -> 타입/길이/범위 검증
-> 업무 규칙 검증 -> Prepared Statement 바인딩 -> 실행/차단 로그
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Path, Query, Header, Body 입력 식별 | OpenAPI 계약, Content-Type |
| 2 | 타입·길이·패턴 검증 | 정수 범위, 문자열 1~64자, 정규식 allowlist |
| 3 | 업무 규칙 검증 | 권한 소유자, 날짜 범위 31일 이하, 금액 한도 |
| 4 | SQL 파라미터 바인딩 | `?`, named parameter, 동적 컬럼 allowlist |
| 5 | 실패 처리·로그 | 400/422, 필드 코드, WAF·SIEM 연계 |

> 요약: 검증은 요청 진입부에서 시작하고, SQL 실행 직전 바인딩으로 명령과 값을 마지막으로 분리한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 키워드 적용 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 입력 통제 | blacklist, 특수문자 제거 | allowlist, type, length, schema | OWASP ASVS V5 기준 매핑 |
| SQL 처리 | 문자열 결합 질의 | Prepared Statement, ORM binding | Injection 테스트 케이스 100% 차단 목표 |
| 실패 처리 | DB 오류 노출 | 400/422와 표준 오류 코드 | 오류 메시지에 SQL·Stack Trace 0건 |
| 운영 검증 | 수동 점검 | SAST, DAST, 로그 차단율 | CI SQLi rule, 차단 이벤트 추세 |

> 요약: 입력값 검증은 허용 범위 제한, 파라미터 바인딩은 SQL 해석 분리를 담당하므로 두 통제를 함께 적용해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 검증 방식 | blacklist 필터 | allowlist+schema validation | 허용 값이 명확한 업무 필드 |
| DB 접근 | 문자열 concatenation | prepared/named parameter | 사용자 입력 포함 질의 전부 적용 |
| 동적 조건 | 임의 컬럼·정렬 허용 | 컬럼명·정렬방향 enum allowlist | 검색 API, 관리자 조회 화면 |

> 요약: 값은 바인딩하고, SQL 식별자처럼 바인딩 불가한 항목은 enum allowlist로 제한한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SQL Injection | 문자열 결합, escape 의존 | Prepared Statement 의무화, 리뷰 체크리스트 | SAST SQLi 0건, DAST payload 차단 |
| 우회 입력 | Unicode 정규화 누락 | NFC 정규화 후 검증, canonicalization | 우회 테스트 30종 통과 |
| 로그 유출 | 입력 원문 전체 저장 | 민감값 마스킹, hash(request-id) | 로그 내 PAN·토큰 검출 0건 |

> 요약: 주요 위험은 문자열 결합, 정규화 누락, 로그 유출이며 자동 테스트와 로그 스캔으로 검증한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 검증 커버리지 | 외부 입력 필드 100% 스키마 매핑 | OpenAPI diff, controller test |
| Injection 방어 | SQLi/XSS/Command payload 차단 | DAST, fuzzing, unit test |
| 운영 탐지 | 4xx 차단율, 동일 IP 실패 횟수 | WAF 로그, SIEM rule, APM |

> 요약: 도입 후에는 스키마 커버리지, Injection 테스트, 실패 이벤트 로그로 통제 유효성을 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. API 계약: OpenAPI/JSON Schema로 Path·Query·Body 필드별 type, min/max, pattern, enum을 정의하고 CI에서 계약 변경 diff 점검
2. 서버 구현: Controller에서 Bean Validation, Service에서 소유권·기간·금액 검증, DAO에서 PreparedStatement 또는 ORM named parameter만 허용
3. 검증 운영: SQLi payload 50종 회귀 테스트, SAST SQLi rule 0건 기준, 차단 로그를 SIEM에 `input_validation_fail` 코드로 전송

**결론 (2줄):**
- 기술사 판단: 사용자 입력이 DB 질의에 닿으면 바인딩을 기본값으로 두고, 컬럼명·정렬키는 enum allowlist로 별도 통제해야 함
- 향후 방향: API Schema, RASP, WAF 로그를 연결해 입력 검증 실패 위치와 재발 패턴을 지속 점검해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "입력값 검증을 설명하시오" | schema validation, 업무 규칙, binding 흐름 | Injection 통제, 실패 처리, 로그 기준 |
| 요구사항 명시형 | "SQL Injection 대응 방안을 제시하시오", "설계하시오" | 신뢰 경계별 검증 위치와 Prepared Statement 적용 | 동적 SQL allowlist, DAST/SAST 지표, 운영 점검 |

> 요약: 설명형은 검증 원리를 넓게 쓰고, 방안형은 신뢰 경계와 DB 바인딩 지점을 좁혀 쓴다.
