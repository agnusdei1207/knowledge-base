---
sidebar:
  order: 67
  label: "067. 정적 분석 SAST"
  badge:
    text: "기출 · 70%"
    variant: note
title: "정적 분석 SAST (Static Application Security Testing)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 67
extra:
  question_no: "067"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "128•135회 반복, 정적 취약점 탐지 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SAST(Static Application Security Testing)**: 프로그램을 실행하지 않고 소스 코드 원문이나 바이트코드를 파싱하여 보안 약점(CWE/OWASP)을 전수 분석하는 화이트박스 기법.
- **오염 분석(Taint Analysis)**: 외부 입력값(Source)이 정화(Sanitizer) 없이 데이터베이스 쿼리나 쉘 실행점(Sink)으로 흘러가는 경로를 추적하는 기법.

</details>

- 정의/개념: 소스코드를 실행하지 않고 **추상 구문 트리(AST) 및 오염 분석(Taint Analysis)** 으로 보안 약점을 조기 탐지하는 화이트박스 보안 테스팅
- 배경/필요성: 릴리즈 후 런타임 보안 사고 발생 시 **취약점 사후 수정 비용 폭증 및 운영 데이터 유출 피해 해결 불가**

#### 한줄 요약
- 코드를 실행하지 않고 구문 파싱과 데이터 흐름 추적으로 소스 코드 내 보안 취약점을 조기에 탐지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **False Positive(오탐)**: 실제로는 공격이 불가능하거나 안전한 코드임에도 정적 분석 도구가 잠재적 위험으로 잘못 경고하는 현상.
- **Shift-Left Security**: 배포 전 최종 점검이 아닌 개발자 IDE 코딩 및 CI 빌드 단계로 보안 검증을 앞당기는 원칙.

</details>

- 소스 코드 전체를 검사하는 **화이트박스(White-Box) 기반 100% 전수 점검**
- 개발/빌드 단계에서 결함을 즉각 피드백하는 **시프트 레프트(Shift-Left) 보안 내재화**
- 실행 컨텍스트 부재로 인한 **오탐(False Positive) 억제를 위한 룰셋 커스터마이징 필수**

#### 한줄 요약
- 화이트박스 전수 분석으로 정확한 코드 취약 라인을 식별하며, 룰셋 튜닝으로 오탐을 제어한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Source-Sink-Sanitizer**: 외부 입력(Source: HTTP 요청), 취약점 실행점(Sink: SQL 쿼리), 입력값 검증/치환(Sanitizer) 3요소 모델.

</details>

```text
[SAST 정적 분석 및 품질 게이트 아키텍처]
|-- 소스 코드 파일 (Java, Python, JS, C++ 소스코드)
|-- 구문 파서 (Lexer / AST Parser: 추상 구문 트리 및 제어 흐름 그래프 CFG 생성)
|-- 정적 보안 분석 엔진 (Static Analysis Engine)
|   |-- 시맨틱 룰 매칭 (KISA 47개 보안약점, CWE/SANS Top 25, OWASP Top 10)
|   `-- 오염 분석 엔진 (Taint Engine: Source -> [Sanitizer 누락] -> Sink 추적)
`-- 품질 게이트 및 리포터 (Quality Gate & False Positive Suppressor)
    |-- [Critical 취약점 발견] -> CI 빌드 강제 실패 (Fail-Fast)
    `-- [통과] -> 아티팩트 빌드 승인
```

선의 의미: 계층 및 코드 파싱-오염 분석-품질 게이트 판정 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| **구문 파서 (AST Parser)** | 소스코드를 파싱하여 **추상 구문 트리(AST) 및 제어 흐름 그래프(CFG) 생성** |
| **오염 분석기 (Taint)** | Source(HTTP 파라미터)부터 Sink(SQL/명령어)까지 **미정화 데이터 흐름 추적** |
| **규칙 엔진 (Rule Engine)** | KISA 47개 보안약점 및 CWE/OWASP 룰셋과 **패턴 매칭 검증** |
| **품질 게이트 (SonarQube)** | 취약점 심각도(Critical/High) 기준 미달 시 **CI/CD 빌드 차단 및 리포트 발행** |

#### 한줄 요약
- AST 파서, Taint 오염 분석기, 규칙 매칭 엔진, 품질 게이트가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **KISA 47대 보안약점**: 행정안전부/KISA가 고시한 입력데이터 검증(SQLi, XSS), 보안기능, 시간 및 상태, 에러처리 등 공공 SW 필수 점검 기준.

</details>

```text
개발자가 소스 코드를 Git 저장소에 커밋/푸시
        │
   1. [파싱 단계] SAST 도구가 소스 코드를 읽어 AST 및 CFG/DFG 그래프 생성
        │
   2. [오염 추적] HTTP 파라미터(Source)가 `PreparedStatement` 등 정화(Sanitizer) 없이
                  `Statement.executeQuery()`(Sink)로 직접 전달되는지 분석
        │
   3. [룰셋 대조] KISA SQL Injection 취약점(CWE-89) 위반으로 판정 (정확한 소스 라인 특정)
        │
   심각도 기준(Critical 취약점 1건 이상)에 위배되는가?
   ┌────┴─────┐
  예           아니오
   │             │
[CI 빌드 차단]   [품질 게이트 통과]
PR 병합 금지      CD 파이프라인 진행
개발자 즉시 통보
```

#### 한줄 요약
- 코드 파싱 → AST 생성 → Source-to-Sink 오염 추적 → 룰셋 대조 → 빌드 차단 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SAST vs DAST**: 소스 코드를 직접 보는 화이트박스 정적 분석(SAST)과 구동 중인 앱에 외부에서 공격 패킷을 쏘는 블랙박스 동적 분석(DAST).

</details>

| 비교 항목 | 정적 분석 (SAST: SonarQube, Checkmarx) | 동적 분석 (DAST: OWASP ZAP, Burp Suite) |
|:---|:---|:---|
| 분석 대상 | **소스 코드 원문, 컴파일 바이트코드** | **실행 중인 웹 애플리케이션 (HTTP URL)** |
| 테스팅 방식 | **화이트박스 (Whitebox)** | **블랙박스 (Blackbox)** |
| 취약점 위치 특정 | **정확한 파일명 및 소스 코드 라인 번호 제공** | 취약한 URL 엔드포인트 및 HTTP 응답만 제공 |
| 장점 | 개발 초기 결함 조기 발견 (Shift-Left) | 런타임 인증 오류, 서버 설정 결함 탐지 |
| 주요 한계 | 실행 컨텍스트 부재로 오탐(False Positive) 존재 | 소스 코드 내부의 정확한 수정 위치 미제공 |

#### 한줄 요약
- SAST는 코드 내부 취약 라인을 조기 전수 검사하고, DAST는 실행 환경의 실제 침투 가능성을 검증한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Incremental Scan(증분 스캔)**: 전체 수백만 줄의 코드를 매번 분석하지 않고, 이번 Git PR에서 변경된 파일들만 30초 내로 빠르게 스캔하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SAST 도구의 과도한 오탐으로 인한 경고 피로(Alert Fatigue) | **도메인 맞춤 룰셋 커스터마이징 및 검증된 오탐 `@Suppress` 등록** | 개발자 신뢰도 90% 이상 회복 |
| 대규모 레포지토리 분석 시 CI 빌드 30분 이상 지연 | **PR 커밋 단위 증분 분석(Incremental Scan) 및 야간 전수 스캔 분리** | CI 피드백 시간 2분 이내 단축 |
| 프레임워크 자체 새니타이징(Spring Security)을 미인식 | **도구 설정 파일에 프레임워크 내장 Sanitizer 함수 등록** | 오탐 제거 및 정밀 오염 분석 달성 |
| 서드파티 라이브러리 소스코드까지 분석하여 노이즈 발생 | **자체 개발 소스만 스캔 대상 지정 및 오픈소스는 SCA 도구로 분리** | 자체 비즈니스 로직 취약점 집중 검증 |

#### 한줄 요약
- 룰셋 튜닝, 증분 스캔, 프레임워크 Sanitizer 등록, SCA 도구 분리로 분석 효율을 극대화한다.

## Ⅶ. 결론

- 안전한 소프트웨어 개발 생애주기(SSDLC) 확립을 위해 **개발자 IDE 및 CI 파이프라인에 SAST를 필수 통합**하고, **KISA 47개 보안약점 룰셋 기반 품질 게이트**를 운영하여 보안 취약점 원천 차단

#### 한줄 요약
- SAST는 소스 코드를 실행하지 않고 구문 파싱과 오염 분석을 통해 코딩 단계에서 보안 결함을 조기 제거하는 핵심 화이트박스 보안 도구다.