---
sidebar:
  order: 170
  label: "170. SOAP vs REST 비교 (SOAP vs REST)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SOAP vs REST 비교 (SOAP vs REST)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 170
extra:
  question_no: "170"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "메시지 계약과 자원 설계 비교 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **단순 객체 접근 프로토콜(Simple Object Access Protocol, SOAP)**: 확장 가능 마크업 언어 봉투와 처리 규칙을 사용하는 메시지 프로토콜이다.
- **표현 상태 전이(Representational State Transfer, REST)**: 자원 식별자와 균일 인터페이스로 자원 표현을 조작하는 아키텍처 스타일이다.

</details>

- 정의/개념: XML 계약의 **단순 객체 접근 프로토콜(Simple Object Access Protocol, SOAP)**과 자원 중심 **표현 상태 전이(Representational State Transfer, REST)**의 비교이다.
- 배경/필요성: 단일 방식으로는 엄격한 계약과 웹 자원 확장성을 동시에 충족하기 어렵다.

#### 한줄 요약

- SOAP은 정해진 봉투와 계약으로 업무 연산을 호출하고 REST는 주소와 HTTP 의미로 자원 상태를 조회•변경한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **확장 가능 마크업 언어(Extensible Markup Language, XML)**: SOAP 메시지 구조를 표현하는 마크업 언어이다.
- **웹 서비스 기술 언어(Web Services Description Language, WSDL)**: SOAP 연산과 자료형 계약을 정의하는 언어이다.
- **웹 서비스 확장 명세(Web Services Specifications, WS-*)**: SOAP 보안•신뢰성•트랜잭션을 확장하는 명세군이다.
- **통합 자원 식별자(Uniform Resource Identifier, URI)**: REST 자원을 고유하게 식별하는 문자열이다.
- **하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP)**: REST가 자원 조작에 활용하는 웹 전송 프로토콜이다.
- **균일 인터페이스**: 표준 메서드 의미로 자원 표현을 조작하는 원칙이다.
- **SOAP 결함(SOAP Fault)**: SOAP 처리 실패의 종류와 세부 내용을 표현하는 구조이다.
- **HTTP 상태(HTTP Status)**: REST 요청의 처리 결과를 상태 코드로 표현하는 수단이다.

</details>

- **확장 가능 마크업 언어(Extensible Markup Language, XML)**•**웹 서비스 기술 언어(Web Services Description Language, WSDL)**•**웹 서비스 확장 명세(Web Services Specifications, WS-*)** 기반 SOAP 계약•확장이 핵심이다.
- **통합 자원 식별자(Uniform Resource Identifier, URI)**•**하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP)**•**균일 인터페이스** 기반 REST 자원 조작이 핵심이다.
- **SOAP 결함(SOAP Fault)**과 **HTTP 상태(HTTP Status)** 기반으로 오류 의미를 분리한다.

#### 한줄 요약

- SOAP은 기관 간 문서처럼 형식과 서명을 엄격히 맞추고 REST는 웹의 주소•메서드•캐시 규칙을 재사용해 인터페이스를 단순화한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **계약 계층**: 요청 스키마와 연산 계약을 검사하는 계층이다.
- **보안 계층**: 서명과 인증 정책을 검사하는 계층이다.
- **SOAP 종단점**: XML 봉투와 WSDL 계약을 검증하는 접점이다.
- **REST 종단점**: URI와 HTTP 메서드 의미를 처리하는 접점이다.

</details>

```text
[클라이언트]
      |
      +-- [SOAP 종단점] --+
      |                    |
      +-- [REST 종단점] --+-- [계약•보안 계층]
                                     |
                                     +-- [업무 서비스]
```

| 구성요소 | 책임 |
|:---|:---|
| 클라이언트 | 계약 메시지•자원 요청 생성 |
| SOAP 종단점 | **SOAP 종단점**이 XML 봉투•WSDL 계약을 검증 |
| REST 종단점 | **REST 종단점**이 URI•HTTP 의미를 처리 |
| 계약•보안 계층 | **계약 계층**이 스키마를, **보안 계층**이 서명•인증 정책을 검사 |
| 업무 서비스 | 연산 실행•자원 상태 처리 |

#### 한줄 요약

- 클라이언트가 SOAP 문서 창구나 REST 자원 창구를 선택해도 계약•보안 검사를 거쳐 같은 업무 서비스에 도달한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **계약 엄격성**: 자료형•연산•오류 형식의 사전 합의 수준이다.
- **메시지 단위 확장**: 전송 경로와 별개인 보안•신뢰성 요구이다.
- **자원 확장성**: URI•표준 메서드•캐시를 재사용하는 정도이다.
- **SOAP 경로**: XML•WSDL•WS-* 명세로 연산을 호출하는 경로이다.
- **REST 경로**: URI•HTTP 의미로 자원 표현을 조작하는 경로이다.

</details>

```text
연계 요구
   |
   +-- 계약 엄격성•메시지 단위 확장
   |        |
   |        +-- SOAP
   |              +-- XML 봉투•WSDL 계약
   |              +-- WS-* 보안•신뢰성
   |              +-- SOAP Fault
   |
   +-- 웹 자원•무상태•캐시
            |
            +-- REST
                  +-- URI•HTTP 메서드
                  +-- 자원 표현•HTTP 상태
```

### 동작 원리

- **계약 엄격성**과 **메시지 단위 확장**이 중요하면 **SOAP 경로**로 XML•WSDL•WS-* 명세를 적용한다.
- **자원 확장성**이 중요하면 **REST 경로**로 URI•HTTP 의미를 적용한다.

#### 한줄 요약

- SOAP 요청은 봉투와 연산 계약을 먼저 검사하고 REST 요청은 주소•메서드•표현을 해석한 뒤 각 방식의 표준 오류 형태로 결과를 돌려준다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **연계 방식 선택 축**: 계약 엄격성과 자원 확장성의 비교 기준이다.

</details>

| **연계 방식 선택 축** | **단순 객체 접근 프로토콜(SOAP)** | **표현 상태 전이(REST)** |
|:---|:---|:---|
| 적용 기준 | 엄격한 계약•메시지 확장 | 웹 자원•단순 연계 |
| 핵심 특징 | XML•WSDL•WS-* 명세 | URI•무상태•균일 인터페이스 |
| 한계 | 검증•확장의 처리 부담 | 설계 편차•별도 계약 관리 |

#### 한줄 요약

- 메시지 서명과 신뢰성 명세가 중요한 기관 연계는 SOAP을, 공개 자원을 웹 방식으로 조회하는 인터페이스는 REST를 우선 검토한다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **중복 업무 처리**: 재시도로 같은 업무 효과가 여러 번 반영되는 문제이다.
- **웹 서비스 보안(Web Services Security, WS-Security)**: SOAP 메시지의 신원•기밀성•무결성을 보호하는 표준이다.
- **전송 계층 보안(Transport Layer Security, TLS)**: 전송 경로를 암호화하고 상대를 인증하는 표준이다.
- **멱등 키**: 같은 요청의 중복 효과를 차단하는 식별값이다.
- **보상 처리**: 이미 반영된 업무 효과를 상쇄하는 복구 수단이다.
- **하위 호환 정책**: 새 계약이나 필드를 기존 소비자가 계속 처리할 수 있도록 변경 범위를 제한하는 규칙이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 서비스별 계약 해석 차이 | WSDL•별도 명세의 우선 설계 | 상호운용 오류 감소 |
| 메시지의 위변조 위험 | **웹 서비스 보안(Web Services Security, WS-Security)**•**전송 계층 보안(Transport Layer Security, TLS)** 적용 | 신원•무결성 확보 |
| 재시도의 **중복 업무 처리** | 요청 식별자•**멱등 키**•**보상 처리** | 중복 효과 방지 |
| XML•표현의 처리 비용 | 크기•검증•왕복 횟수 측정 | 지연•대역폭 통제 |
| 버전 변경의 호환성 파괴 | 스키마•필드의 **하위 호환 정책** | 기존 소비자 보호 |

#### 한줄 요약

- 어느 방식을 사용해도 재시도되는 결제 요청에는 멱등 키를 두고 계약 변경은 기존 소비자가 이해하는 필드를 유지해야 한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **메시지 보안**: 전송 경로와 별개로 메시지 자체를 보호하는 요구이다.

</details>

- **계약 엄격성**, **메시지 보안**, **자원 확장성**으로 SOAP•REST를 결정한다.

#### 한줄 요약

- XML 크기만 보지 말고 메시지 확장과 웹 자원 규칙의 필요성을 기준으로 선택해야 한다.
