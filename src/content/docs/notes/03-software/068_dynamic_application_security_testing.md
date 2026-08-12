---
sidebar:
  order: 68
  label: "068. 동적 애플리케이션 보안 테스트 DAST (Dynamic Application Security Testing)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "동적 애플리케이션 보안 테스트 DAST (Dynamic Application Security Testing)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 68
extra:
  question_no: "068"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "128•135회 반복, 실행 기반 취약점 탐지"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **DAST (Dynamic Application Security Testing, 동적 보안 분석)**: 런타임 구동 중인 웹/API 애플리케이션 외부 엔드포인트에 실제 악의적 공격 모의 페이로드(HTTP Payload)를 주입하여 런타임 보안 취약점을 탐지하는 블랙박스 동적 보안 테스트.
- **Black-box Security Testing**: 소스코드에 대한 정보가 전혀 없는 상태에서 외부 공격자(Hacker) 관점으로 동작 중인 애플리케이션의 HTTP Request/Response 반응을 수집하여 취약점 검증.
- **OWASP ZAP / Burp Suite**: DAST 분석 시 크롤링(Crawling), 모의 침투 스캔, HTTP 트래픽 인터셉트를 자동화 수행하는 대표적 프록시 기반 동적 분석 도구.

</details>

- 정의/개념: 구동 중인 실운영/Staging 환경의 웹 애플리케이션 외부 엔드포인트에 동적 모의 침투 공격을 수행하여 런타임 취약점 및 환경 설정 오류를 검증하는 **DAST (Dynamic Application Security Testing)**
- 배경/필요성: SAST 정적 분석으로는 파악 불가능한 런타임 웹 서버 SSL 설정, 세션 타임아웃, 인가(Authorization) 누락 및 실제 공격 가능성 검증 요구성

#### 한줄 요약

- 실행 서비스의 외부 취약 반응을 검증하는 동적 애플리케이션 보안 테스트가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **False Positive 0% 지향**: 실제 구동 중인 서버에 공격을 가하여 HTTP 200/500 응답 결과로 성공 여부를 입증하므로, 정적 분석(SAST)에 비해 오탐율(False Positive)이 극도로 낮음.
- **No Source Code Needed**: 소스코드 언어나 라이브러리에 독립적이며(Language Agnostic), 런타임 HTTP 엔드포인트만 노출되어 있으면 스캔 가능.

</details>

- **Black-box Testing (소스코드 지식 0% 외부 공격자 관점)**
- **Language Agnostic (언어 독립적)** 및 낮은 오탐율(**Low False Positive**)
- 소스코드 내 위치(라인 번호) 특정 불가 및 스캔 완료 시간 장기 소요

#### 한줄 요약

- 실제 취약 반응 확인과 검사 누락의 한계를 함께 관리하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소 (DAST 4단계 메커니즘)

<details><summary>핵심 용어</summary>

- **Spider / Crawler**: 웹 애플리케이션 내의 모든 URL, 링크, Form, API 엔드포인트를 자동으로 탐색하여 공격 대상 표면(Attack Surface) 목록을 수집하는 엔진.

</details>

```text
[DAST Scanner (OWASP ZAP)]
       │
       ▼ (1. Spider / Crawling)
┌────────────────────────────────────────────────────────┐
│ Attack Surface (URL, Parameter, Form, REST API) 도출   │
└──────────────────────────┬─────────────────────────────┘
                           ▼ (2. Active Scanning & Injection)
┌────────────────────────────────────────────────────────┐
│ SQLi, XSS, CSRF, Auth-Bypass Payload 주입 공격 발사   │
└──────────────────────────┬─────────────────────────────┘
                           ▼ (3. HTTP Response Analysis)
[Target App (Staging)] ──► [HTTP Status Code & Body 분석] ──► [DAST Report 산출]
```

선의 의미: DAST 스캐너가 웹 앱을 자동 크롤링하여 공격 표면을 도출하고 Active Scan 페이로드를 발사하여 HTTP 응답을 분석하는 구조.

| 구성요소 (Components) | 핵심 역할 및 기능 | 주요 적용 내용 |
|:---|:---|:---|
| **Spider / Crawler** | 웹사이트 내부 전체 URL 링크 및 API 경로 자동 수집 | HTML/JS Parsing |
| **Authentication Engine**| 로그인 폼, OAuth2, Session Cookie 유지 상태로 스캔 | Session / Token Manager |
| **Attack Payload Generator**| SQLi, Cross-Site Scripting(XSS), CSRF 등 공격 페이로드 생성 | OWASP Top 10 Payloads |
| **Active Scan Engine** | 생성된 공격 페이로드를 매개변수별로 실제 HTTP 전송 | Proxy Attack Runner |
| **Response Analyzer** | HTTP 상태 코드, 에러 메시지, 응답 지연시간 분석 | Response Pattern Matcher |

#### 한줄 요약

- 크롤러, 공격 페이로드, 인증 컨텍스트, 취약점 보고서의 검사 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Passive vs Active Scanning**: Passive는 트래픽을 관찰만 하여 헤더 설정 등을 검사, Active는 실제로 공격 쿼리를 주입(Inject)하여 DB/서버 응답을 변형 검증.

</details>

```text
┌──────────────────────────────┐
│ Staging Target URL 지정      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Session Login 인증 수립   │
│ 2. Spider 엔진으로 URL 수집  │
│ 3. Active Scan 공격 주입     │
│ 4. HTTP Response 오탐 판정   │
└──────────────┬───────────────┘
               ▼
   [DAST 취약점 리포트 산출]
```

### 동작 원리

1. **Authentication**: 로그인 아이디/비번을 세팅하여 Session Cookie 수립.
2. **Spider Crawling**: 주입 대상 Form 파라미터 및 Rest API 엔드포인트 자동 도출.
3. **Active Scanning**: `param1=' OR 1=1 --` 같은 공격 페이로드 송신.
4. **Response Analysis**: HTTP 500 에러 메시지에 SQL 오류 문구 포함 시 취약점 확정 및 리포팅.

#### 한줄 요약

- 범위•권한별 공격과 취약 반응 증거 판정이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **IAST (Interactive Application Security Testing)**: SAST(코드 내부)와 DAST(외부 모의 침투)를 통합하여, DAST 공격 시 애플리케이션 내부에 주입된 에이전트가 코드 라인까지 정밀 역추적하는 현대적 기법.

</details>

| 비교 항목 | SAST (정적 분석) | DAST (동적 분석) | IAST (대화형 분석) |
|:---|:---|:---|:---|
| 테스트 관점 | 소스코드 내면 분석 | **외부 블랙박스 분석** | **내부 에이전트 + 외부 동적 분석** |
| 코드 라인 식별| **정확히 라인 번호 지정** | 불가능 (URL만 도출) | **정확히 라인 번호 지정** |
| 실행 환경 필요| 필요 없음 (비실행) | **필수 (Staging/Prod 필요)**| **필수 (에이전트 주입 필요)** |
| 검사 속도 | 빠름 (수분) | **느림 (수시간~수일 소요)** | 중간 |

#### 한줄 요약

- 공격 가능성은 동적 애플리케이션 보안 테스트, 코드 원인은 정적 애플리케이션 보안 테스트로 확인한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Production Risk**: 실운영(Prod) DB에 DAST Active Scan을 가할 경우 `DELETE/UPDATE` 쿼리가 발사되어 데이터가 파괴될 수 있으므로, 반드시 Isolated Staging 환경에서 스캔 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 실운영 DB 데이터 파괴 위험 (**Production Risk**) | **독립된 Staging / QA 환경에 더미 데이터로 스캔** | 운영 데이터 안전 보장 |
| SPA (Single Page App, React) 자바스크립트 크롤링 실패 | **Headless Browser (Puppeteer/Playwright) 기반 크롤러 연동** | 렌더링 경로 탐색 완결 |
| DAST 스캔 시간이 수시간 소요되어 CI 파이프라인 지연 | **CI 단계에서는 Baseline 스캔, 주말 야간 Full 스캔 분리** | 파이프라인 배포 보존 |

> 사례: **OWASP ZAP / Burp Suite Enterprise + Jenkins CD Pipeline** 연동 모의 침투 스캔

#### 한줄 요약

- API 명세, 역할별 계정, 격리 환경, 요청 식별자로 검사 범위를 보강하는 것이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **DAST 도입 수립 기준(DAST Adoption Standards)**: 런타임 환경 준비도, API 크롤링 사양 및 IAST로의 발전 가능성에 의거한 체계.

</details>

- **DAST 도입 수립 기준**에 따라 Web/API 보안 확보 시 **Staging 환경 내 OWASP ZAP DAST 스캔** 필수 수용

#### 한줄 요약

- 공격 표면•권한•운영 영향 기반 DAST 범위가 핵심이다.
