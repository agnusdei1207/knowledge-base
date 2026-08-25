---
sidebar:
  order: 68
  label: "068. 동적 분석 DAST"
  badge:
    text: "기출 · 70%"
    variant: note
title: "동적 애플리케이션 보안 테스트 DAST (Dynamic Application Security Testing)"
date: "2026-08-25T11:00:00+09:00"
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

<details><summary>용어 설명</summary>

- **DAST(Dynamic Application Security Testing)**: 실행 중인 웹 애플리케이션을 대상으로 외부 공격자 관점에서 악의적인 페이로드를 전송하여 취약점을 탐지하는 블랙박스 테스팅.
- **Active Scanning**: SQL Injection, XSS, SSRF 등 실제 공격 문자열을 파라미터에 주입하여 서버의 에러 응답과 비정상 반응을 검증하는 기법.

</details>

- 정의/개념: 구동 중인 웹 애플리케이션에 **블랙박스 모의 침투 및 액티브 스캐닝(Active Scanning)** 을 수행하여 런타임 보안 취약점을 탐지하는 기법
- 배경/필요성: 정적 소스 분석(SAST)만으로는 탐지하기 어려운 **인프라/웹 서버 설정 오류 및 런타임 인증/인가 우회 결함 해결 불가**

#### 한줄 요약
- 실행 중인 애플리케이션에 외부 공격을 시뮬레이션하여 실제 악용 가능한 취약점을 검증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **False Positive 극소화**: 가상의 코드 결함이 아닌, 실제 HTTP 공격 요청이 성공하여 서버 응답이 뚫리는 것을 확인하므로 오탐율이 매우 낮음.
- **Language Agnostic(언어 독립성)**: 대상 서버가 Java, Python, Go, Node.js 등 어떤 기술 스택으로 작성되었든 HTTP/REST 인터페이스만으로 진단 가능.

</details>

- 소스 코드 열람이 불필요한 **블랙박스(Black-Box) 기반 외부 해커 관점 검증**
- 백엔드 언어 및 프레임워크에 종속되지 않는 **완전한 언어 독립적(Language Agnostic) 스캔**
- 실제 익스플로잇 성공 여부로 판정하여 **오탐(False Positive) 극소화 및 실효적 위협 입증**

#### 한줄 요약
- 소스 코드 없이 실제 공격을 시뮬레이션하여 극도로 낮은 오탐률로 런타임 취약점을 입증한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스파이더/크롤러(Crawler)**: 대상 웹사이트의 모든 링크, HTML Form, REST API 엔드포인트를 자동으로 탐색하여 공격 표면(Attack Surface)을 수집하는 모듈.

</details>

```text
[DAST 동적 모의 침투 아키텍처 구조]
|-- 공격 대상 (Running Web App: 스테이징/QA 환경 URL 엔드포인트)
|-- 공격 표면 수집기 (Spider / Crawler: OpenAPI 명세 및 HTML Form 파싱)
|-- 인증 세션 관리자 (Auth Manager: JWT 토큰, OAuth, 쿠키 세션 자동 갱신)
|-- 퍼징 및 페이로드 주입기 (Fuzzing & Payload Injector)
|   |-- Passive Scanner (비침습적 헤더, SSL/TLS 암호 스위트 검사)
|   `-- Active Scanner (침습적 SQLi, XSS, SSRF 공격 페이로드 전송)
`-- 취약점 판정 엔진 (Response Analyzer: HTTP 상태코드, 에러 메시지 분석 및 PoC 생성)
```

선의 의미: 계층 및 크롤링-인증 연계-페이로드 주입-응답 분석 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| **스파이더 (Crawler)** | 사이트 내 링크, HTML 폼, REST API를 탐색하여 **공격 표면(Attack Surface) 도출** |
| **인증 관리자 (Auth)** | 로그인 폼 및 OAuth/JWT 토큰을 갱신하여 **인증 세션 유지 및 인가 영역 진입** |
| **페이로드 주입기 (Fuzzer)** | OWASP Top 10 기반 SQLi, XSS, 명령 주입 등 **변이 페이로드 전송** |
| **응답 분석기 (Analyzer)** | HTTP 상태 코드, 응답 헤더, 시간 지연을 분석하여 **취약점 발현 여부 판정** |

#### 한줄 요약
- 크롤러가 공격 표면을 수집하고 인증 세션을 유지하며 페이로드를 주입해 응답을 판정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PoC(Proof of Concept)**: 취약점이 실제로 존재함을 증명하는 재현 가능한 HTTP 요청/응답 패킷 증적.

</details>

```text
1. 진단 대상 URL 및 OpenAPI(Swagger) 명세 등록
        │
   2. [탐색 단계] 스파이더가 웹 UI와 API 경로를 순회하며 파라미터 공격 표면 수집
        │
   3. [인증 단계] 관리자 및 일반 사용자 계정으로 로그인하여 세션/JWT 획득
        │
   4. [공격 단계] 파라미터에 OWASP Top 10 악성 페이로드(`' OR 1=1--`, `<script>`) 주입
        │
   서버 응답에서 SQL 에러 출력 또는 스크립트 실행이 확인되었는가?
   ┌────┴─────┐
  예           아니오
   │             │
[취약점 증명 PoC 생성] [안전 판정]
Critical 취약점 리포트 발행   보안 가이드 통과
```

#### 한줄 요약
- 대상 설정 → 공격 표면 탐색 → 인증 세션 확보 → 페이로드 주입 → PoC 생성 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SAST vs DAST vs IAST**: 정적 코드 분석(SAST), 외부 모의 침투(DAST), 런타임 에이전트 결합 하이브리드(IAST).

</details>

| 비교 항목 | 정적 분석 (SAST: SonarQube) | 동적 분석 (DAST: OWASP ZAP) | 대화형 분석 (IAST: Contrast Security) |
|:---|:---|:---|:---|
| 진단 시점 | **개발/빌드 단계 (컴파일 시)** | **스테이징/운영 단계 (런타임)** | QA/자동화 테스트 실행 단계 |
| 진단 방식 | 화이트박스 (소스코드 분석) | **블랙박스 (외부 HTTP 공격)** | **하이브리드 (내부 에이전트 + 외부 공격)** |
| 오탐율 (False Positives) | 다소 높음 (컨텍스트 부재) | **매우 낮음 (실제 공격 증명)** | **극히 낮음 (정확한 코드 실행 경로 추적)** |
| 장점 | 소스 코드 라인 단위 피드백 | **웹서버 설정 및 런타임 인증 검증** | 정확한 소스 라인과 실제 악용성 동시 확인 |
| 단점 | 런타임 설정 결함 탐지 불가 | 소스 코드 정확한 수정 라인 미제공 | 에이전트 탑재에 따른 성능 오버헤드 |

#### 한줄 요약
- SAST는 코드 내부를, DAST는 외부 실행 환경을, IAST는 에이전트로 두 장점을 융합 검증한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Data Pollution(데이터 오염)**: DAST 도구가 자동 회원가입, 결제, 삭제 API를 무차별 호출하여 DB가 더럽혀지거나 실제 결제가 발생하는 위험.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 프로덕션 DB 데이터 오염 및 무차별 결제/삭제 발생 | **운영 환경 직접 진단 금지 및 격리된 Staging 환경 전용 수행** | 실제 운영 데이터 파괴 및 서비스 장애 원천 방지 |
| SPA(React, Vue) 렌더링 미지원으로 공격 표면 누락 | **Puppeteer / Playwright 헤드리스 브라우저 기반 크롤링** | JavaScript DOM 렌더링 후 엔드포인트 100% 탐색 |
| 전체 DAST 스캔 시간 과다로 CI/CD 배포 지연 | **PR 배포 시 Baseline 빠른 스캔 + 야간 정기 Full 스캔 분리** | 배포 파이프라인 속도 유지 및 심층 진단 양립 |
| WAF(웹 방화벽) 차단으로 인한 진단 실패 | **DAST 점검용 IP를 WAF 화이트리스트에 사전 등록** | 실제 애플리케이션 취약점 정밀 탐지 |

#### 한줄 요약
- 스테이징 격리 환경, 헤드리스 크롤러, Baseline 분리 스캔, WAF 예외 등록으로 안전성을 확보한다.

## Ⅶ. 결론

- 소프트웨어 보안 완성도를 위해 CI 단계의 SAST에 이어 **CD 배포 후 스테이징 환경에서 DAST(OWASP ZAP)를 필수 실행**하고, **SAST/DAST 상호보완 다층 방어망**을 구축하여 런타임 침해 사고 예방

#### 한줄 요약
- DAST는 외부 공격자의 시각에서 애플리케이션과 인프라의 런타임 취약점을 실효적으로 검증하는 필수 동적 보안 도구다.