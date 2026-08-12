---
sidebar:
  order: 67
  label: "067. 정적 분석 SAST (Static Application Security Testing)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "정적 분석 SAST (Static Application Security Testing)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **SAST (Static Application Security Testing, 정적 보안 분석)**: 애플리케이션을 실행하지 않고 소스코드, 바이트코드 또는 컴파일 바이너리의 추상 구문 트리(AST)와 데이터 흐름을 정적으로 스캔하여 보안 취약점을 탐지하는 화이트박스 보안 테스트 기법.
- **Taint Analysis (오염 분석)**: 신뢰할 수 없는 외부 사용자 입력값(Source)이 산출물 내부의 보안 민감 연산 함수(Sink)에 도달하기까지, 적절한 검증/정화(Sanitizer)를 거쳤는지 데이터 흐름 경로(Data Flow Path)를 추적하는 정적 기법.
- **Source, Sink, Sanitizer**: Source는 사용자 입력 진입점, Sink는 쿼리/커맨드 실행 등 위험 함수, Sanitizer는 입력값 검증 및 인코딩/이스케이프 처리 함수.

</details>

- 정의/개념: 애플리케이션 코드를 실행하지 않고, 소스코드 구문과 Taint Analysis 기법을 통해 SQL Injection, XSS 등의 보안 약점(CWE)을 코딩/빌드 단계에서 사전 탐지하는 **SAST (Static Application Security Testing)**
- 배경/필요성: 배포 후 런타임 보안 사고 조치 비용 감축, DevSecOps Shift-Left 사상 구현 및 OWASP Top 10 보안 표준 준수 요구성

#### 한줄 요약

- 비실행 코드에서 입력-위험 동작 경로를 찾는 정적 애플리케이션 보안 테스트가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **False Positive vs False Negative**: False Positive(오탐)는 안전한 코드를 취약점으로 오판하는 현상, False Negative(미탐)는 실제 존재하는 취약점을 놓치고 지나치는 현상.
- **Rule Set (규칙 집합)**: SAST 분석 엔진이 소스코드에서 취약 패턴을 스캔할 때 사용하는 KISA SW 보안약점 가이드 및 OWASP 기반의 룰셋 정의.

</details>

- **White-box Analysis (소스코드 및 데이터 흐름 100% 가시성)**
- **Shift-Left Security** 달성 (IDE 플러그인 / CI 파이프라인 정착)
- 런타임 실행 맥락 결여로 인한 **False Positive (오탐)** 튜닝 필요성

#### 한줄 요약

- 화이트박스 분석, 시프트 레프트, 오탐, 미탐의 특성을 이해하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소 (Taint Analysis 메커니즘)

<details><summary>핵심 용어</summary>

- **AST (Abstract Syntax Tree)**: 파서(Parser)가 소스코드의 문법 구조를 트리 형태의 객체 구조체로 추상화 변환한 데이터 표현식.

</details>

```text
[Source: 외부 사용자 입력 (HTTP Param)]
                 │
                 ▼ (Taint Data Flow 추적)
┌────────────────────────────────────────────────────────┐
│ AST (Abstract Syntax Tree) 파싱 & CFG/DFG 그래프 생성  │
│ Sanitizer (검증/인코딩 함수) 유무 추적 검사            │
└──────────────────────────┬─────────────────────────────┘
                           ▼ (Sanitizer 누락 감지)
[Sink: 위험 연산 실행 (ExecuteQuery SQL)] ──► [SAST Alert: SQL Injection 탐지]
```

선의 의미: 외부 입력 Source가 AST 파싱 및 DFG 경로를 타고 Sanitizer 부재 시 Sink 함수로 유입되는 취약 오염 경로(Taint Path)를 분석하는 구조.

| 구성요소 (Components) | 핵심 역할 및 기능 | 주요 적용 내용 |
|:---|:---|:---|
| **Code Parser (AST)** | 소스 코드를 읽어 구문 파싱 및 추상 구문 트리 생성 | Lexer, AST Parser |
| **CFG / DFG Builder** | 제어 흐름 그래프(CFG) 및 데이터 흐름 그래프(DFG) 생성 | Control / Data Flow Engine |
| **Taint Analyzer** | **Source $\rightarrow$ Sanitizer $\rightarrow$ Sink 오염 전파 경로 추적** | **Taint Tracking Engine** |
| **Rule Set Engine** | KISA 47대 보안약점 및 OWASP Top 10 규칙 대조 | SonarQube, Fortify Rules |
| **Reporting & Suppression**| 오탐(False Positive) 예외 처리 및 보안 이슈 가시화 | SonarQube Dashboard |

#### 한줄 요약

- 파서, 소스-싱크 오염 전파, 새니타이저, 억제 근거의 분석 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **KISA 47개 SW 보안약점**: 한국인터넷진흥원에서 정한 소프트웨어 개발 보안 가이드(입력데이터 검증 및 표현, 보안기능, 시간 및 상태 등 7대 분야 47개 항목).

</details>

```text
┌──────────────────────────────┐
│ Git Code Commit & PR         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. AST Parser 소스 구조화   │
│ 2. DFG Taint Path 추적 분석  │
│ 3. KISA/OWASP 룰셋 매칭      │
│ 4. Quality Gate (Pass/Fail)  │
└──────────────┬───────────────┘
               ▼
   [취약점 라인별 피드백 반환]
```

### 동작 원리

1. **AST 생성**: IDE나 CI 파이프라인에서 소스코드 수거 후 AST 트리로 파싱.
2. **Taint Tracking**: HTTP Request Param(Source)이 DB 쿼리(Sink)로 흘러가는 DFG 경로 추적.
3. **Sanitizer 검사**: 중간 경로에 `PreparedStatement` 나 `ESAPI` 인코더(Sanitizer)가 존재하는지 판정.
4. **Rule Matching & Gate**: 누락 시 KISA SQL Injection 위반 감지하여 Quality Gate 빌드 파기(`Fail`).

#### 한줄 요약

- 코드 모델•규칙 기반 오염 경로 추적 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **SAST vs DAST**: SAST는 소스코드 내부를 들여다보는 화이트박스 정적 분석, DAST는 런타임 웹 애플리케이션에 공격을 가하는 블랙박스 동적 분석.

</details>

| 비교 항목 | SAST (정적 보안 분석) | DAST (동적 보안 분석) |
|:---|:---|:---|
| 분석 대상 | **소스코드, 바이트코드 (비실행 상태)** | **구동 중인 웹/API 서비스 (실행 상태)** |
| 테스트 기법 | **화이트박스 (White-box Analysis)** | **블랙박스 (Black-box Analysis)** |
| 취약점 위치 | **정확한 파일명 및 코드 라인 번호 제시** | **URL / HTTP Response 결과만 확인 가능** |
| 실행 시점 | **개발 초기 (IDE, Git Commit, CI 빌드)** | **배포 후 (Staging/QA 환경)** |
| 오탐율 (False Positive) | 상대적으로 높은 편 (오탐 룰셋 튜닝 필요) | 매우 낮음 (실제 공격 성공 시만 리포팅) |

#### 한줄 요약

- 코드 원인은 정적 애플리케이션 보안 테스트, 실행 공격은 동적 애플리케이션 보안 테스트로 확인한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Alert Fatigue (경고 피로)**: SAST 도구가 쏟아내는 수백 개의 오탐(False Positive) 경고에 지쳐 개발자가 보안 경고를 아예 무시해 버리는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 지나친 오탐으로 개발자 경고 피로(**Alert Fatigue**) 폭증 | 프로젝트 특성에 맞는 **Rule Set 커스텀 튜닝 및 False Positive Suppression** | 검증 신뢰성 회복 |
| 전체 소스 풀스캔 시 CI 빌드가 1시간 이상 소요 | **PR 시 Delta(증분) 스캔 & 야간 스케줄링 Full 스캔 분리** | 파이프라인 속도 보존 |
| 타사 프레임워크/라이브러리 내부 오탐 검출 | **Third-party 코드 스캔 대상 제외(Exclusion)** | 필수 스캔에 집중 |

> 사례: **SonarQube Developer Edition + Checkmarx + IDE Plugin (SonarLint)** 연동 구축

#### 한줄 요약

- 실행 가능성 검토, 노출, 자산 영향에 기반한 경고 우선순위가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **SAST 도입 수립 기준(SAST Adoption Standards)**: KISA 47대 보안약점 준수율, CI/CD 연동성 및 False Positive 튜닝 역량에 의거한 체계.

</details>

- **SAST 도입 수립 기준**에 따라 전자정부 프레임워크 및 DevSecOps 구현 시 **SAST (SonarQube) + DAST (OWASP ZAP)** 병행 수용

#### 한줄 요약

- 실제 위험에 기반한 SAST 조치 우선순위가 핵심이다.
