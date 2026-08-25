---
sidebar:
  order: 91
  label: "091. WAF 웹 애플리케이션 방화벽"
  badge:
    text: "기출 · 70%"
    variant: note
title: "응용 계층 웹 보안 통제 : WAF (Web Application Firewall)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 91
extra:
  question_no: "91"
  source_status: "기출"
  source_history: "129회, 137회"
  priority: 70
  priority_note: "L7 HTTP/HTTPS 페이로드 심층 검사, OWASP Top 10 방어, 가상 패치(Virtual Patch) 및 Reverse Proxy"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **WAF (Web Application Firewall)**: L7 HTTP/HTTPS 요청 및 응답 페이로드를 심층 분석하여 웹 취약점 공격을 탐지·차단하는 특화 보안 솔루션.
- **OWASP Top 10**: 인젝션, XSS, SSRF 등 웹 애플리케이션에서 가장 치명적인 10대 보안 취약점을 정리한 국제 표준 목록.

</details>

- 정의/개념: HTTP/HTTPS 트래픽의 URI, 헤더, 쿠키, POST 바디를 정규화하여 **OWASP Top 10 공격을 탐지·차단하고 가상 패치를 제공하는 L7 웹 보안 시스템**
- 배경/필요성: L3/L4 네트워크 방화벽이 표준 웹 포트(80/443)의 내부 페이로드를 검사하지 못하는 한계로 인한 **웹 취약점 악용, DB 탈취 및 악성 웹쉘 삽입 무방비 노출**

#### 한줄 요약
- L7 심층 검사, 공격 난독화 정규화 해제, 취약점 가상 패치를 통해 웹 애플리케이션을 보호한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Virtual Patching (가상 패치)**: 소스코드 수정이나 서버 재배포 없이 WAF 룰셋을 즉각 적용하여 알려진 취약점 공격 경로를 선제 차단하는 기술.
- **Normalization (정규화)**: URL 인코딩, Hex, Base64, 유니코드 등으로 난독화된 공격 문자열을 단일 표준 텍스트로 디코딩하는 전처리 과정.

</details>

- **L7 응용 계층 페이로드 심층 검사**: HTTP Method, Header, Cookie, POST Body 전 영역을 **정밀 분석하여 웹 공격 차단**
- **난독화 우회 공격 무력화(정규화)**: 다중 URL 인코딩, Hex, 유니코드 변환을 **표준 평문으로 복원하여 시그니처 매칭 수행**
- **긴급 가상 패치(Virtual Patching)**: 제로데이 취약점 발생 시 코드 수정 전 **WAF 룰 배포만으로 공격을 즉시 방어**

#### 한줄 요약
- L7 페이로드 심층 검사, 난독화 정규화 해제, 가상 패치를 통한 제로데이 긴급 방어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SSL Offloading**: 암호화된 HTTPS 트래픽을 WAF 단에서 복호화하여 백엔드 서버의 연산 부담을 줄이고 페이로드 가시성을 확보하는 기능.

</details>

```text
[WAF 리버스 프록시 인라인 아키텍처]
|-- Inbound Traffic (HTTPS Port 443 암호화 웹 요청 인입)
`-- WAF Reverse Proxy System
    |-- 1. SSL/TLS Termination (인증서 기반 복호화 및 SSL Offloading)
    |-- 2. Normalization Engine (URL / Hex / Base64 / Unicode 디코딩)
    |-- 3. Policy & Signature Engine (OWASP Top 10 매칭, 화이트리스트 룰 대조)
    `-- 4. Response Masking & DLP (주민번호, 카드번호, DB 에러 메시지 필터링)
`-- Protected Backend (정상 검증 완료된 트래픽만 Web/WAS/DB 서버로 전달)
```

선의 의미: 인입되는 암호화 웹 트래픽이 WAF에서 복호화 및 정규화 과정을 거쳐 정책 검사를 통과한 후 백엔드 웹 서버로 안전하게 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SSL/TLS 종단 모듈** | 인증서 기반 HTTPS 세션 종단, **SSL 복호화 및 가속(Crypto Offloading)** | 암복호화 처리 |
| **정규화 엔진** | URL-Encoding, Hex, Unicode 등 **우회 인코딩을 표준 평문으로 변환** | Normalization |
| **룰 분석 엔진** | **OWASP Top 10 시그니처 매칭, 정규표현식 검사 및 Rate Limiting** | Policy Engine |
| **DLP 마스킹 모듈** | 서버 응답 내의 **개인정보 및 시스템 DB 에러 메시지 은폐** | 정보 유출 방지 |
| **감사 로그 및 튜닝기**| 차단/허용 로그 기록, **오탐(False Positive) 분석 및 화이트리스트 튜닝** | Audit & Tuning |

#### 한줄 요약
- SSL 종단기, 정규화 엔진, 룰 정책 엔진, DLP 마스킹 모듈, 튜닝기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Positive vs Negative Security Model**: 허용된 정상 요청 패턴만 인가하는 화이트리스트 모델과 알려진 공격 시그니처를 차단하는 블랙리스트 모델.

</details>

```text
WAF 복호화, 정규화 및 정책 검사 파이프라인
        │
   1. [HTTPS 요청 인입] 외부 클라이언트 요청이 WAF 리버스 프록시 단으로 인입
        │
   2. [SSL 세션 복호화] WAF가 SSL 인증서로 세션을 종단하고 평문 HTTP 페이로드 추출
        │
   3. [난독화 정규화] 다중 URL/Hex/Base64 인코딩을 단일 표준 텍스트로 정규화
        │
   4. [복합 정책 검사] Positive(허용 URL) 및 Negative(SQLi/XSS 시그니처) 룰 대조
        │
   ├─ [공격 패턴 감지 시] ➔ 즉시 HTTP 403 Forbidden 응답 및 악성 IP 차단
   ▼
5. [백엔드 포워딩] 정상 요청만 백엔드 WAS로 전달 ➔ 응답 내 개인정보 마스킹 후 회신
```

#### 한줄 요약
- SSL 복호화 → HTTP 정규화 → 복합 정책 검사 → 악성 요청 즉각 차단 → 응답 개인정보 마스킹 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **네트워크 방화벽 (L3/L4)** vs **웹 방화벽 (WAF / L7)** vs **시큐어 코딩 (Secure Coding)**.

</details>

| 비교 항목 | 네트워크 방화벽 (L3/L4) | 웹 방화벽 (WAF / L7) | 시큐어 코딩 (Secure Coding) |
|:---|:---|:---|:---|
| **통제 계층** | **L3 (IP), L4 (Port / TCP 플래그)** | **L7 (HTTP/HTTPS 페이로드 전 영역)** | **애플리케이션 소스코드 및 로직 계층** |
| **검사 대상** | 출발지/목적지 IP, 포트, 패킷 플래그 | **URI, Query, Header, Cookie, Body** | **변수 입력값, 비즈니스 로직, 메모리** |
| **방어 대상 공격** | IP Spoofing, 포트 스캔, SYN Flood | **SQL Injection, XSS, CSRF, 웹쉘** | **권한 상승, 로직 우회, 소프트웨어 결함**|
| **한계점** | 80/443 오픈 시 웹 공격 무방비 통과 | 복잡한 비즈니스 로직 결함 탐지 곤란 | 개발자 역량 의존 및 레거시 수정 곤란 |
| **주요 역할** | 네트워크 경계 1차 접근 통제 | **실시간 웹 공격 방어 및 가상 패치** | **소프트웨어 취약점 근본 원천 제거** |

#### 한줄 요약
- 네트워크 방화벽은 경계 L3/L4 통제, WAF는 L7 공격 실시간 방어, 시큐어 코딩은 소프트웨어 결함 원천 제거를 담당한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Detection Only Mode (감사 모드)**: 신규 룰 배포 시 오탐으로 인한 서비스 중단을 막기 위해 차단 없이 로그만 기록하며 룰을 검증하는 운영 단계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 신규 룰 배포 시 정상 비즈니스 요청을 차단하는 **오탐(False Positive) 발생** | **`감사 모드(Detection Only) 2주 운영` 및 정밀 예외(Whitelisting) 튜닝** | 서비스 가용성 100% 보장 및 오탐률 0.01% 이하 통제 |
| 신규 제로데이 취약점 발표 후 소스 패치 완료 시까지의 보안 방어 공백 | **WAF `가상 패치(Virtual Patching) 긴급 룰` 즉시 생성 및 배포** | 개발 소요 기간 동안 제로데이 공격 선제적 무력화 |
| 대규모 트래픽의 SSL 복호화 연산으로 인한 WAF 장비 CPU 고갈 및 지연 | **하드웨어 가속 `SSL Offloading 전용 장비` 분리 또는 클라우드 SaaS WAF** | WAF 부하 분산 및 밀리초 단위 고속 응답 처리 |
| API 트래픽(JSON/XML) 증가로 인한 전통적 정규표현식 파싱 한계 | **`JSON Schema 검증 및 OpenAPI 명세 기반 Positive 룰셋` 적용** | API 비정상 파라미터 변조 정밀 탐지 및 방어 |

#### 한줄 요약
- 감사 모드 튜닝으로 오탐을 방지하고, 가상 패치로 제로데이에 대응하며, SSL Offloading으로 부하를 최적화한다.

## Ⅶ. 결론

- 웹 전자상거래 및 클라우드 API 서비스의 기밀성과 가용성을 사수하기 위해 **L7 WAF 역방향 프록시 아키텍처를 표준 배치**하되, 운영 안정성과 보안성을 극대화하기 위해 **지속적인 화이트리스트 예외 튜닝, 긴급 가상 패치(Virtual Patching) 프로세스, SSL Offloading 가속, DevSecOps 시큐어 코딩**을 결합한 다계층 웹 보안 체계 완성

#### 한줄 요약
- WAF는 L7 심층 검사와 가상 패치 및 정규화를 통해 웹 애플리케이션을 안전하게 보호하는 핵심 방어 인프라다.