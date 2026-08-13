---
sidebar:
  order: 22
  label: "022. 차세대 방화벽 NGFW vs WAF vs CASB 비교 (NGFW WAF CASB Comparison)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "차세대 방화벽 NGFW vs WAF vs CASB 비교 (NGFW WAF CASB Comparison)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 22
extra:
  question_no: "022"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 비교 기출로 계층별 보안제품 선택성이 분명함"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **차세대 방화벽(Next-Generation Firewall, NGFW)**: IP/Port 통제를 넘어 L7 애플리케이션(App-ID) 및 사용자(User-ID) 기반으로 네트워크 심층 트래픽을 통제하는 보안 솔루션.
- **웹 애플리케이션 방화벽(Web Application Firewall, WAF)**: HTTP/HTTPS 프로토콜을 전문 분석하여 OWASP Top 10 웹 공격(SQLi, XSS 등) 및 API 공격을 차단하는 전용 보안 솔루션.
- **클라우드 접근 보안 중개(Cloud Access Security Broker, CASB)**: 온프레미스 사용자와 외부 SaaS/PaaS 클라우드 서비스 사이에서 가시성, 데이터 보안(DLP), 위협 방어 및 규정 준수를 중개 통제하는 솔루션.

</details>

- 정의/개념: 네트워크•웹•SaaS 문맥을 나눠 통제하는 **NGFW•WAF•CASB**
- 배경/필요성: 단일 경계 방화벽은 **웹 공격•섀도 IT•SaaS 유출**을 놓친다.

#### 한줄 요약

- 네트워크 및 L7 애플리케이션(NGFW), 웹/API 전용 위협(WAF), SaaS 클라우드 데이터 보안(CASB)의 영역별 검사 계층 비교

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **App-ID**: 패킷의 실제 페이로드 식별을 통해 표준 포트(예: 80, 443) 우회 통신을 감지하고 실제 실행 중인 애플리케이션을 판별하는 기술.
- **서비스형 소프트웨어(Software as a Service, SaaS)**: 클라우드 기반 환경에서 제공되는 소프트웨어 서비스 (Salesforce, Microsoft 365 등).

</details>

- **NGFW**는 포트 독립적 **App-ID**와 User-ID를 통합하여 L3~L7 세션 네트워크 통제
- **WAF**는 HTTP/HTTPS 및 REST API 트래픽의 파라미터 유효성과 웹 공격 패턴(SQLi, XSS) 정밀 심사
- **CASB**는 산재한 **SaaS** 접근 가시성 확보, 섀도 IT(Shadow IT) 발견 및 클라우드 DLP 통제 수행

#### 한줄 요약

- NGFW의 App-ID/User-ID 기반 네트워크 통제, WAF의 OWASP Top 10/API 검사 및 CASB의 SaaS 가시성·DLP 결합

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **데이터 유출 방지(Data Loss Prevention, DLP)**: 개인정보, 금융정보, 기업 비밀 등 민감 데이터의 무단 외부 전송/유출을 실시간 검사·차단하는 보안 메커니즘.
- **신원 제공자(Identity Provider, IdP)**: 사용자 신원 인증 정보를 중앙 관리하고 SSO 및 SAML/OAuth 기반으로 권한 검증을 제공하는 인프라.

</details>

```text
계층별 보안 구조
├─ 사용자•데이터
├─ NGFW 계층
├─ WAF•API 계층
├─ CASB 계층
└─ 로그•정책 통합
```

가지의 의미: 신원 체계, 네트워크 경계, 웹/API 보호, SaaS 중개 통제 및 통합 로그 분석 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 사용자•데이터 | IdP 연동 기반 통일된 사용자 신원(User-ID) 및 민감 데이터 자산 정의 |
| NGFW 계층 | 내부/외부 구역 경계에서 5-Tuple, App-ID 기반 트래픽 세그멘테이션 |
| WAF•API 계층 | DMZ 전단에서 HTTP/HTTPS 요청, JSON/XML 파라미터 및 API 봇 위협 심사 |
| CASB 계층 | API 또는 인라인 프록시 방식으로 SaaS 자산 접근, 섀도 IT 및 클라우드 DLP 집행 |
| 로그•정책 통합 | SIEM/SOAR를 통한 솔루션 간 상관분석 로그 집계 및 위협 연동 대응 |


#### 한줄 요약

- IdP 신원 통합, NGFW 네트워크 통제, WAF/API 경계 및 CASB SaaS DLP 통합 보안 아키텍처

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **공통 정책 문맥(Common Policy Context)**: IdP 신원, 자산 중요도 및 규정 준수 기준을 3개 솔루션에 연동하여 일관적으로 적용하는 통제 문맥.
- **네트워크•앱 식별•통제**: NGFW를 통한 L3~L7 네트워크 세션 및 허용 애플리케이션 판정 단계.
- **웹•API 공격 검사•통제**: WAF를 통한 HTTP 페이로드 정밀 분석 및 OWASP 위협 탐지 단계.
- **SaaS•데이터 정책 검사•통제**: CASB를 통한 SaaS 접근 권한 심사 및 파일 업/다운로드 DLP 정책 집행 단계.

</details>

```text
보호 대상•요청 문맥 판정
        ├─ 네트워크•앱 흐름
        │      └─ 1. 네트워크•앱 식별•통제
        ├─ 웹•API 요청
        │      └─ 2. 웹•API 공격 검사•통제
        └─ SaaS•데이터 이용
               └─ 3. SaaS•데이터 정책 검사•통제
                          │
                          └── 판정•로그 통합
```

### 동작 원리

1. **네트워크•앱 식별•통제**: NGFW에서 5-Tuple, App-ID, User-ID 기반 세션 차단 및 허용 수행
2. **웹•API 공격 검사•통제**: WAF에서 웹 요청 헤더/바디 DPI, 봇(Bot) 차단 및 파라미터 오염 검사 수행
3. **SaaS•데이터 정책 검사•통제**: CASB에서 사용자 SaaS 계정 행위 감시, 섀도 IT 차단 및 클라우드 DLP 통제 수행


#### 한줄 요약

- 트래픽 문맥 판정, NGFW/WAF/CASB 솔루션별 병렬 검사, SIEM/SOAR 일시적 로그 통합 및 공동 대응 흐름

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **HTTP(Hypertext Transfer Protocol)**: 웹 브라우저와 웹 서버 간 요청/응답을 전송하는 L7 프로토콜.
- **API(Application Programming Interface)**: 애플리케이션 간 데이터 교환 및 기능 호출을 위한 규격화된 프로토콜 인터페이스.
- **TLS(Transport Layer Security)**: 전송 계층 트래픽의 기밀성과 무결성을 보호하는 표준 암호화 프로토콜.

</details>

| 보안 통제 수단 | **NGFW (차세대 방화벽)** | **WAF (웹 방화벽)** | **CASB (클라우드 접근 중개)** |
|:---|:---|:---|:---|
| 보호 영역 및 계층 | L3~L7 네트워크 & 전체 IP 트래픽 | L7 웹 애플리케이션 (HTTP/HTTPS) | L7 SaaS 클라우드 서비스 & 데이터 |
| 주요 탐지 대상 | 포트 우회 앱, 악성 트래픽, L4-L7 위협 | OWASP Top 10, SQLi, XSS, API 봇 | 섀도 IT, 미인가 SaaS, 클라우드 데이터 유출 |
| 핵심 기술 | App-ID, User-ID, IPS, TLS 인스펙션 | HTTP DPI, 시그니처, 긍정/부정 분석 모델 | API 연동, Forward/Reverse Proxy, DLP |
| 한계 | 암호화 복호화 과부하, L7 웹 공격 세밀 탐지 한계 | 웹 이외 프로토콜 탐지 불가 | 비연계 SaaS/온프레미스 직접 접속 사각지대 |

> 요약: 보호 대상(네트워크 vs 웹 vs SaaS)과 통제 레벨에 따른 솔루션 심층 배치

#### 한줄 요약

- 검사 계층, 대상 프로토콜, 위협 유형 및 TLS 복호화 위치에 따른 NGFW, WAF, CASB의 세부 비교 선택

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **섀도 IT(Shadow IT)**: 보안 승인을 거치지 않고 사내 직원이 개인적으로 사용하는 미인가 클라우드/SaaS 애플리케이션.
- **NIST SP 800-41 Rev. 1(NIST SP 800-41 Standard)**: 방화벽 배치 및 아키텍처 수립을 가이드하는 표준 보안 기술 문서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 솔루션 배치 및 중복 투자 | **NIST SP 800-41 Rev. 1** 기반 계층별 배치 | 영역별 중복 검사 차단 및 역할 최적화 |
| 암호화(TLS) 트래픽 검사 사각지대 | **SSL/TLS 복호화 전용 미러링/프록시** | 암호 트래픽 내 은닉 악성코드 및 유출 차단 |
| 사내 미인가 **섀도 IT** 범람 | **CASB 발견(Discovery) 기능** 연동 | 미인가 SaaS 가시성 확보 및 접속 차단 |
| 통제 솔루션 간 파편화 | **IdP 기반 User-ID 및 SIEM/SOAR 통합** | 이종 솔루션 간 통합 상관 분석 및 위협 자동 대응 |

#### 한줄 요약

- NIST SP 800-41 준수, TLS 복호화 통제, 섀도 IT(Shadow IT) 탐지 및 IdP 통합 SSO/DLP 연동

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **계층별 심층 방어(Defense-in-Depth Architecture)**: 단일 보안 솔루션에 의존하지 않고 네트워크, 웹, 클라우드 각 레이어별로 상호 보완 솔루션을 배치하는 전략.

</details>

- 보호 계층에 따라 네트워크/트래픽은 **NGFW**, 웹/API는 **WAF**, SaaS/데이터는 **CASB**를 계층별 심층 방어(Defense-in-Depth) 적용

#### 한줄 요약

- 네트워크는 **NGFW**, 웹•API는 **WAF**, SaaS는 **CASB** 배치
