---
title: "콘텐츠 보안 정책 CSP (Content Security Policy)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 88
---

# 📖 【암기용】 개념 완전 이해

> 목적: 콘텐츠 보안 정책 CSP를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 브라우저가 로드·실행할 스크립트, 스타일, 이미지, 프레임 출처를 서버 정책으로 제한하는 보안 헤더
- **왜 필요한가**: XSS는 입력 검증이 뚫리거나 저장된 악성 스크립트가 실행될 때 발생한다. CSP는 브라우저 실행 단계에서 허용 출처, nonce, hash가 없는 스크립트를 차단한다.
- **핵심 직관**: CSP는 웹 페이지 안에서 실행 가능한 "허가된 공급처 명단"을 브라우저에게 주는 규칙임

## 깊이 이해
- **배경·문제의식**: 복잡한 웹은 CDN, 광고, 분석 도구, inline script가 섞인다. 하나의 XSS가 쿠키 탈취와 세션 조작으로 이어지므로 브라우저가 실행 직전에 정책을 확인해야 한다.
- **작동 원리**: 서버가 `Content-Security-Policy` 헤더를 보낸다. 브라우저는 `default-src`, `script-src`, `style-src`, `frame-ancestors`, `report-to`를 읽고 위반 리소스를 차단하거나 보고한다. nonce/hash는 inline script를 식별하는 안전한 예외다.
- **비유**: 행사장 출입 명단에 등록된 업체만 장비를 반입하고, 임시 출입증(nonce)이 있는 스태프만 무대 뒤로 들어가는 절차와 같다.
- **구체 예시**: `script-src 'self' 'nonce-r4nd0m' https://cdn.example.com` 정책이면 nonce가 없는 inline script와 미등록 도메인 script는 실행되지 않는다.
- **흔한 오해·주의점**: CSP는 XSS를 제거하는 기법이 아니라 피해 실행을 제한하는 보완 통제다. 입력 검증, 출력 인코딩, 쿠키 `HttpOnly; Secure; SameSite`와 함께 써야 한다.

## 연결 개념
- XSS - CSP가 브라우저 실행 단계에서 줄이는 주요 위험
- SRI - CDN 리소스의 해시 무결성 검증
- 보안 헤더 - HSTS, X-Content-Type-Options, Referrer-Policy

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CSP를 헤더 이름 암기가 아니라 브라우저 신뢰 경계에서 스크립트 실행 권한을 nonce/hash와 report 지표로 통제하는 답안으로 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CSP는 브라우저가 로드·실행 가능한 리소스 출처와 inline script 예외를 정책 헤더로 제한하는 XSS 보완 통제임
> 2. **가치**: nonce/hash 기반 `script-src`, `frame-ancestors`, `report-uri/report-to`로 스크립트 실행·클릭재킹·정책 위반 탐지를 연결함
> 3. **판단 포인트**: `unsafe-inline` 제거, nonce 회전, CDN 허용 범위, report-only 전환 절차, 위반 로그 재검증을 함께 써야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 브라우저 실행 통제 이해 확인 | `default-src`, `script-src`, nonce/hash, `frame-ancestors` | CSP를 서버 입력 검증으로 설명 |
| XSS 보완 통제 설계 확인 | 입력 검증+출력 인코딩+CSP 조합 | CSP만으로 XSS 제거 가능하다고 단정 |
| 운영 전환과 탐지 지표 확인 | Report-Only, report-to, violation log | `unsafe-inline`, wildcard `*` 남용 |

> 요약: 이 문제는 브라우저가 어떤 리소스를 실행하게 할지 정책으로 제한하고 위반을 어떻게 탐지할지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 브라우저 리소스 실행 정책
- 배경: 웹 페이지는 CDN, 광고, 분석 스크립트가 섞여 XSS와 공급망 변조가 사용자의 브라우저 실행 단계에서 발생할 수 있음.
- 필요성: W3C CSP Level 3의 `script-src`, nonce, hash, `report-uri`/`report-to`를 적용해 허용 출처와 위반 보고 기준을 브라우저에 전달해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Web Server -> CSP Header -> Browser Policy Engine
           -> script/style/img/frame 검증 -> 차단 또는 실행 -> Violation Report
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 정책 지시어 | 리소스 유형별 허용 출처 정의 | `default-src`, `script-src`, `style-src` |
| nonce/hash | inline script 예외 식별 | 요청별 nonce, SHA-256/384/512 hash |
| 프레임 통제 | 클릭재킹·임베딩 제한 | `frame-ancestors 'none'` 또는 허용 도메인 |
| 보고 채널 | 위반 이벤트 수집 | `report-uri`, `report-to`, Report-Only |

> 요약: CSP는 지시어, nonce/hash, 프레임 통제, 보고 채널로 브라우저 실행 정책을 구성한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
응답 생성 -> CSP Header 포함 -> 브라우저 리소스 요청
-> 출처/nonce/hash 확인 -> 허용 실행 또는 차단 -> report-to 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서버가 CSP 또는 CSP-Report-Only 헤더 전송 | 환경별 정책 템플릿 |
| 2 | 브라우저가 script/style/img/frame 로드 시도 | directive별 source list |
| 3 | inline script 검사 | nonce 일치, hash 일치, `unsafe-inline` 없음 |
| 4 | 위반 리소스 차단 또는 보고 | blocked-uri, violated-directive |
| 5 | 로그 분석 후 정책 보정 | false positive, 위반 상위 도메인 |

> 요약: CSP는 응답 헤더로 전달되고 브라우저가 실행 직전에 지시어·nonce·hash를 확인해 차단과 보고를 수행한다.

---

## Ⅳ. 특징

| 구분 | 기존/미적용 | 본 키워드 적용 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 스크립트 실행 | 모든 inline script 허용 | nonce/hash 기반 허용 | `unsafe-inline` 0개 목표 |
| 외부 리소스 | 도메인 wildcard 허용 | `self`와 지정 CDN만 허용 | 허용 도메인 목록 분기별 점검 |
| 탐지 | 브라우저 차단 로그 없음 | report-to로 위반 수집 | 위반 이벤트 p95 처리 24시간 이내 |
| 적용 방식 | 즉시 차단만 사용 | Report-Only 후 Enforcement | 2주 관측 후 차단 정책 전환 |

> 요약: CSP는 XSS 실행면을 줄이고, Report-Only와 위반 로그로 정책 오탐을 줄인 뒤 차단으로 전환한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| XSS 대응 | 입력 검증·출력 인코딩 | 브라우저 실행 정책 추가 | 저장형·DOM XSS 피해 제한 |
| inline 허용 | `unsafe-inline` | nonce 또는 hash | SSR/템플릿 기반 앱은 nonce 우선 |
| 공급망 통제 | CDN 도메인 허용만 | CSP+SRI 조합 | 외부 script 무결성 필요 시 결합 |

> 요약: CSP는 입력 검증의 대체물이 아니라 브라우저 실행 단계의 마지막 제한선으로 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정책 우회 | `unsafe-inline`, `unsafe-eval` 사용 | nonce/hash, Trusted Types 검토 | 위험 지시어 0개 |
| 서비스 장애 | 필수 CDN 누락 | Report-Only, staged rollout | blocked-uri 상위 10개 분석 |
| 로그 과다 | 광고·확장 프로그램 위반 보고 | endpoint sampling, user-agent 필터 | report ingestion TPS, 저장 비용 |

> 요약: CSP 운영 리스크는 우회 지시어, 누락 차단, 보고량 폭증이며 단계 전환과 로그 샘플링으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 품질 | `unsafe-inline`, wildcard `*` 0개 | CSP scanner, header test |
| XSS 회귀 | 대표 payload 차단 | DAST, browser automation |
| 보고 운영 | 위반 이벤트 분류, 오탐 처리 시간 | report-to endpoint, SIEM dashboard |

> 요약: CSP 적용 효과는 위험 지시어 제거, XSS payload 차단, 위반 보고 처리 지표로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 정책 설계: `default-src 'self'`, `script-src 'self' 'nonce-{random}' https://cdn.example.com`, `frame-ancestors 'none'`을 기준으로 도메인 allowlist 작성
2. 전환 절차: 2주 이상 `Content-Security-Policy-Report-Only`로 blocked-uri 수집 후 오탐 제거, Enforcement 헤더로 전환
3. 운영 검증: `unsafe-inline` 0개, CSP 위반 상위 10개 원인 분석, DAST XSS payload 차단 결과를 배포 게이트에 반영

**결론 (2줄):**
- 기술사 판단: CSP는 입력 검증·출력 인코딩 이후 브라우저 실행 단계에서 XSS 피해를 제한하는 보완 통제로 적용해야 함
- 향후 방향: nonce/hash CSP와 Trusted Types, SRI, report-to 기반 관측을 묶어 프런트엔드 공급망 통제를 정교화해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CSP를 설명하시오" | 헤더 전달, directive, nonce/hash, report 흐름 | XSS 보완, 클릭재킹 방지, 운영 전환 |
| 요구사항 명시형 | "XSS 대응 방안을 제시하시오", "브라우저 보안 정책을 설계하시오" | Report-Only에서 Enforcement로 전환 절차 | `unsafe-inline` 제거, 위반 로그 지표, SRI 결합 |

> 요약: 설명형은 CSP 구성요소를, 방안형은 XSS 실행 차단과 보고 기반 운영 절차를 중심으로 작성한다.
