---
sidebar:
  order: 22
  label: "022. 차세대 방화벽 NGFW vs WAF vs CASB 비교 (NGFW WAF CASB Comparison)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "차세대 방화벽 NGFW vs WAF vs CASB 비교 (NGFW WAF CASB Comparison)"
date: "2026-07-27T23:59:59+09:00"
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

## 미리 알고가기

- **NGFW(Next-Generation Firewall, 엔지에프더블유)**: 영문 머리글자를 딴 명칭으로, 네트워크 흐름에서 앱·사용자·위협을 식별해 통제
- **WAF(Web Application Firewall, 와프)**: 머리글자를 한 단어처럼 읽으며, HTTP 요청에서 웹·API 공격 문맥을 검사
- **CASB(Cloud Access Security Broker, 캐스비)**: 머리글자를 한 단어처럼 읽으며, SaaS 계정·이용·데이터 정책을 중개
- **App-ID(Application Identification, 앱 아이디)**: 응용프로그램 식별을 뜻하며, 포트와 무관하게 앱을 식별
- **SaaS(Software as a Service, 사스)**: 머리글자를 한 단어처럼 읽으며, 인터넷으로 제공하는 응용 서비스
- **API(Application Programming Interface, 에이피아이)**: 서비스 간 요청과 응답 형식을 정한 인터페이스
- **HTTP(Hypertext Transfer Protocol, 에이치티티피)**: 웹 요청과 응답을 전달하는 규약
- **URL(Uniform Resource Locator, 유알엘)**: 웹 자원의 위치를 나타내는 주소
- **DLP(Data Loss Prevention, 디엘피)**: 민감 데이터의 이동과 유출을 탐지·통제
- **TLS(Transport Layer Security, 티엘에스)**: 웹·API 통신 내용을 암호화하는 규약
- **IdP(Identity Provider, 아이디피)**: 사용자 인증과 신원 정보를 제공하는 시스템
- **섀도 IT(Shadow IT, 섀도 아이티)**: 조직 승인 없이 사용하는 정보기술·클라우드 서비스


- **흐름 기호(↓·→·-->)**: 아래·다음 단계로 이어지는 절차 방향을 표시
## Ⅰ. 개요

- 정의/개념: NGFW·WAF·CASB의 보호 대상과 통제 지점 비교
- 기존 한계: 단일 보안제품은 모든 경계·공격을 통제 불가
- **배경/필요성**: 보호 대상별 제품 선택과 상호 보완 배치

### 쉽게 이해하기 (학습용)

- 도로·창구·문서실별 위험 식별 구조

## Ⅱ. 특징

- NGFW는 네트워크·사용자·앱을 식별한다
- WAF는 웹·API 공격 문맥을 검사한다
- CASB는 SaaS 계정과 데이터를 통제한다
- 암호화·우회 경로는 가시성을 제한한다

### 쉽게 이해하기 (학습용)

- 같은 통신도 보는 위치에 따라 위험이 다름

## Ⅲ. 구성요소 및 구조

```mermaid
flowchart LR
    A[사용자·데이터] --> B[NGFW 계층]
    A --> C[WAF·API 계층]
    A --> D[CASB 계층]
    B --> E[로그·정책 통합]
    C --> E
    D --> E
```

| 구성요소 | 역할 |
|:---|:---|
| 사용자·데이터 | 공통 신원과 데이터 문맥을 제공함 |
| NGFW 계층 | 네트워크와 앱 흐름을 통제함 |
| WAF·API 계층 | 웹 요청과 API 공격을 검사함 |
| CASB 계층 | SaaS 접근과 공유를 통제함 |
| 로그·정책 통합 | 사건과 DLP 정책을 연결함 |

> 요약: 공통 신원/정책으로 통제 연결함

### 쉽게 이해하기 (학습용)

- 서로 다른 경비 기록을 한 사건으로 연결함

## Ⅳ. 원리 및 절차 흐름도

```mermaid
sequenceDiagram
    participant U as 사용자
    participant P as 통합 정책기
    participant N as NGFW
    participant W as WAF
    participant C as CASB
    U->>P: 접근 대상·행위 전달
    P->>N: 네트워크 흐름 검사 요청
    P->>W: 웹·API 요청 검사 요청
    P->>C: SaaS·데이터 검사 요청
    N-->>P: 앱·위협 판정
    W-->>P: 웹 공격 판정
    C-->>P: 계정·DLP 판정
```

| 메시지 | 처리 내용 |
|:---|:---|
| 접근 대상·행위 전달 | 사용자와 목적지를 식별함 |
| 네트워크 흐름 검사 요청 | NGFW에 흐름 판단을 맡김 |
| 웹·API 요청 검사 요청 | WAF에 요청 판단을 맡김 |
| SaaS·데이터 검사 요청 | CASB에 이용 판단을 맡김 |
| 앱·위협 판정 | 앱과 네트워크 위협을 알림 |
| 웹 공격 판정 | 웹 공격 여부를 알림 |
| 계정·DLP 판정 | SaaS와 데이터 위험을 알림 |

> 요약: 대상별 통제기의 판정을 통합함

### 쉽게 이해하기 (학습용)

- 도로·창구·문서실의 경비를 함께 운영함

## Ⅴ. 종류 및 비교

| 판단 기준 | NGFW | WAF | CASB |
|:---|:---|:---|:---|
| 적용 기준 | 구역·앱 흐름 통제 | 웹·API 공격 통제 | SaaS 이용·공유 통제 |
| 핵심 특징 | 사용자·앱 흐름 판단 | 웹 요청 문맥 판단 | SaaS 계정·데이터 판단 |
| 한계 | 암호화 가시성 부족 | 우회 경로 노출 | 비연계 앱 사각지대 |

> 요약: 문맥에 맞춰 솔루션 보완 배치함

### 쉽게 이해하기 (학습용)

- 제품별 전용 통제 영역 존재함

## Ⅵ. 실무 사례

- SaaS는 우회 접속과 비연계 앱을 점검함

### 쉽게 이해하기 (학습용)

- 승인 밖 SaaS 경로도 찾아 통제해야 함

## Ⅶ. 결론

- 서로 다른 계층의 공격과 데이터 유출을 통제하기 위해 네트워크·웹 요청·SaaS 행위의 가시성과 집행 위치를 검토하여, NGFW·WAF·CASB를 목적별로 조합해야 한다.

### 쉽게 이해하기 (학습용)

- 세 제품은 대체재가 아니라 분업 수단임
