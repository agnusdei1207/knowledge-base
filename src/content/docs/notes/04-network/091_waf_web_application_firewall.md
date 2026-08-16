---
sidebar:
  order: 91
  label: "091. WAF 웹 애플리케이션 방화벽 (Web Application Firewall)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "WAF 웹 애플리케이션 방화벽 (Web Application Firewall)"
date: "2026-08-13T18:15:00+09:00"
tags: ["notes-network"]
weight: 91
extra:
  question_no: "091"
  source_status: "기출"
  source_history: "129회, 137회"
  priority: 70
  priority_note: "비교•보안형: 129•137회 WAF 반복"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **웹 애플리케이션 방화벽(WAF, Web Application Firewall)**: HTTP/HTTPS 페이로드와 문맥을 심층 분석하여 SQL Injection, XSS 등 L7 응용 계층 공격을 탐지/차단하는 웹 전용 보안 시스템.
- **하이퍼텍스트 전송 프로토콜(HTTP, Hypertext Transfer Protocol)**: 웹 클라이언트-서버 간 데이터(URL, Header, Body)를 교환하는 L7 응용 계층 표준 프로토콜.
- **응용 계층 보안 통제(Application Layer Security Control)**: IP/Port 중심 통제를 넘어 HTTP 요청/응답 페이로드의 악성 입력값을 심층 검사하는 보안 메커니즘.
- **응용 입력/업무 공격 미식별(Unidentified Application Input & Business Attack)**: L3/L4 방화벽이 허용 포트(80/443) 내 은닉된 L7 악성 페이로드를 식별하지 못하는 한계점.

</details>

- 정의/개념: HTTP/HTTPS 문맥 심층 분석으로 웹 공격을 차단하는 **응용 계층 보안 통제**.
- 배경/필요성: L3/L4 방화벽의 **응용 입력/업무 공격 미식별(Unidentified Application Input & Business Attack)** 한계 극복 및 L7 웹 취약점 방어 시급.

#### 한줄 요약

- L7 HTTP 페이로드 검사를 통해 정상 트래픽과 웹 공격 입력을 정밀 판별.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **정규화(Normalization)**: URL 인코딩, Base64 등 다중 인코딩된 난독화 입력을 표준 디코딩 형태로 변환하여 탐지 우회를 차단하는 기술.
- **공격 서명(Attack Signature)**: 알려진 웹 공격 패턴 및 규칙 기반의 식별 문자열 집합.
- **가상 패치(Virtual Patch)**: 소스코드 수정 전 WAF 차단 규칙 등록을 통해 제로데이 취약점 악용 요청을 즉시 1차 방어하는 기술.
- **HTTP 문맥 분석(HTTP Context Analysis)**: URL, Header, Body 간 연관관계를 종합 해석하여 정상 동작 여부를 판별하는 심층 검사 기법.

</details>

- **HTTP 문맥 분석**: URL, Header, Body 전반의 **공격 서명** 및 비정상 행위 심층 식별.
- **정규화**: URL 인코딩 등 우회 공격 기법 무력화 및 표준화.
- **가상 패치**: 소스코드 수정 전 신규 취약점 즉시 임시 차단 및 대응.

#### 한줄 요약

- 인코딩 우회 무력화 및 공격 서명 매칭을 통한 웹 공격 차단과 정교한 정책 튜닝 필요.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **역방향 대리자(Reverse Proxy)**: 클라이언트와 원본 서버 사이에서 트래픽을 대리 수신 및 검사 후 전달하는 중계 구조이다.
- **전송 계층 보안 종단기(TLS Terminal, Transport Layer Security Terminal)**: SSL/TLS 암호화 세션을 종단하여 복호화된 HTTP 페이로드를 탐지 엔진에 제공하는 구성요소이다.
- **HTTP 해석•정규화기(HTTP Parser & Normalizer)**: 복호화된 웹 요청을 구조화하고 인코딩을 정규화하는 파싱 엔진이다.
- **WAF 정책 엔진(WAF Policy Engine)**: 서명 매칭, 긍정/부정 보안 모델, 속도 제한 규칙을 적용하여 공격을 판정하는 핵심 엔진이다.
- **원본 웹 서버(Origin Web Server)**: WAF 검증을 통과한 유효 트래픽만 수신하여 비즈니스 로직을 처리하는 내부 서버이다.
- **균일 자원 위치 지정자(URL, Uniform Resource Locator)**: 웹 리소스의 위치와 접근 프로토콜을 명시하는 식별자이다.

</details>

```text
WAF
├─ 전송 계층 보안 종단기
├─ HTTP 해석•정규화기
├─ 정책 엔진
├─ 원본 웹 서버
└─ 관측•튜닝기
```

선의 의미: TLS 종단, HTTP 정규화, 정책 엔진이 원본 웹 서버 전단에서 보안 경계를 형성하고 관측•튜닝기가 정책 품질을 지속 관리하는 구조.

WAF는 **역방향 대리자** 방식으로 배치되어 외부 요청을 선제 검사한다.

| 구성요소 | 책임 |
|:---|:---|
| 전송 계층 보안 종단기(TLS Terminal) | SSL/TLS 암호 세션 종단 및 HTTP 복호화 수행 |
| HTTP 해석•정규화기(Parser) | URL, Header, Body 파싱 및 인코딩 정규화 |
| WAF 정책 엔진(Policy Engine) | 서명, 행위, 임계치(Rate Limit) 기반 탐지 규칙 판정 |
| 원본 웹 서버(Origin Server) | WAF 검증 필터링을 통과한 허용 요청 처리 |
| 관측•튜닝기(Tuning Engine) | 오탐/미탐 모니터링 및 탐지 규칙 주기적 최적화 |

#### 한줄 요약

- SSL/TLS 복호화 및 HTTP 정규화 후 정책 엔진 검증을 통과한 유효 트래픽만 원본 서버로 중계.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **보안 하이퍼텍스트 전송 프로토콜(HTTPS, Hypertext Transfer Protocol Secure)**: TLS 암호화 계층을 추가하여 데이터 보안성을 보장하는 HTTP 프로토콜이다.
- **TLS 요청 복호화(TLS Request Decryption)**: HTTPS 암호화 세션을 해제하여 평문 HTTP 패킷을 추출하는 전처리 과정이다.
- **HTTP 요청 정규화(HTTP Request Normalization)**: 다양한 난독화/인코딩 형태를 표준 HTTP 데이터 규격으로 일관화하는 단계이다.
- **공격 문맥 판정(Attack Context Decision)**: 서명 매칭, 긍정 모델, 속도 제어 규칙을 종합하여 이상 유무를 판단하는 프로세스이다.
- **허용 요청 중계(Allowed Request Proxying)**: 정상 요청으로 판정된 트래픽을 원본 웹 서버로 안전하게 포워딩하는 동작이다.

</details>

```text
HTTPS 요청
      │
      ▼
1. TLS 요청 복호화
      │
      ▼
2. HTTP 요청 정규화
      │
      ▼
3. 공격 문맥 판정
      ├─ 공격: 차단 및 로그 기록
      └─ 정상: 4. 허용 요청 중계
                         │
                         ▼
                    HTTP 응답 반환
```

### 동작 원리

1. **TLS 요청 복호화**: HTTPS 종단 후 HTTP 요청 추출
2. **HTTP 요청 정규화**: 난독화 입력을 표준 형식으로 변환
3. **공격 문맥 판정**: 서명•행위•속도 규칙으로 판정
4. **허용 요청 중계**: 검증된 요청만 원본 서버로 전달

#### 한줄 요약

- 복호화-정규화-문맥판정 단계별 검증을 거쳐 검증된 요청만 내부 서버로 중계 및 차단 내역 기록.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **응용 코드 검증(Application Code Validation)**: 애플리케이션 내부에서 입력값 검증 및 세션/권한 제어를 직접 수행하는 보안 기법이다.
- **네트워크 방화벽(Network Firewall)**: IP, Port, Protocol, Session State 기반으로 L3/L4 경계 트래픽을 제어하는 방어 시스템이다.

</details>

| 통제 지점 | 검사 대상 | 보호 범위•잔여 공백 |
|:---|:---|:---|
| WAF | HTTP 요청 문맥, 웹 공격 서명 | 웹 공통 공격 차단, 비즈니스 로직 오용은 코드 검증 필요 |
| 네트워크 방화벽 | IP 주소, Port, TCP 상태 | L3/L4 네트워크 접근 통제, 허용 포트 내 L7 웹 공격 통과 |
| 응용 코드 검증 | 입력 매개변수, 세션/권한, 업무 로직 | 비즈니스 고유 통제 수행, 개발자 숙련도에 따른 구현 누락 발생 |

> 요약: L3/L4 경계 방화벽, L7 WAF, 시큐어 코딩의 다층 심층 방어 체계 구축.

#### 한줄 요약

- L3/L4 방화벽, L7 WAF, 애플리케이션 시큐어 코딩의 역할 분담을 통한 다층 보안 구성.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **오탐(False Positive)**: 정상적인 사용자 요청을 공격 트래픽으로 잘못 판단하여 차단하는 오류 현상이다.
- **관측•튜닝(Observability & Tuning)**: 탐지 로그 및 오탐 내역을 분석하여 탐지 정책을 최적화하는 운영 활동이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 신규 취약점 패치 지연 | 악용 패턴 분석 기반 **가상 패치** 긴급 적용 | 소스코드 수정 전 제로데이/1-Day 공격 선제 차단 |
| 정상 트래픽 **오탐** 발생 | 탐지 모드(Bypass/Audit) 및 예외 규칙 **관측/튜닝(Tuning)** | 업무 서비스 중단 예방 및 차단 정책 정교화 |
| TLS 복호화 처리 병목 | SSL Offloading 전용 장비 적용 및 세션 재사용 | WAF 부하 분산 및 웹 서비스 응답 지연 최소화 |

#### 한줄 요약

- 가상 패치로 즉시 방어망을 구축하고 지속적 정책 튜닝으로 오탐 최소화 및 성능 유지.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **다층 웹 보안 통제(Multi-layered Web Security Control)**: L3/L4 네트워크 경계, L7 WAF, 애플리케이션 시큐어 코딩을 연계하는 심층 방어 전략이다.

</details>

- 공통 웹 공격은 **WAF**, 업무 권한 오용은 **응용 코드**로 통제.

#### 한줄 요약

- WAF 기반 1차 공통 웹 위협 차단 및 응용 시큐어 코딩 연계를 통한 다층 웹 보안 통제 체계 구축.
