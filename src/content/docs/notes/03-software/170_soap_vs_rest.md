---
sidebar:
  order: 170
  label: "170. SOAP vs REST 비교 (SOAP vs REST)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SOAP vs REST 비교 (SOAP vs REST)"
date: "2026-08-18T02:55:00+09:00"
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

<details><summary>용어 설명</summary>

- **SOAP (Simple Object Access Protocol)**: XML 메시지 포맷과 WSDL 계약 및 WS-* 표준(WS-Security, WS-AtomicTransaction)을 강제하는 프로토콜.
- **REST (Representational State Transfer)**: URI로 자원을 식별하고 표준 HTTP 메서드(GET, POST, PUT, DELETE)를 활용하여 JSON 상태를 주고받는 무상태(Stateless) 아키텍처 스타일.

</details>

- 정의/개념: 엄격한 XML 계약과 WS-보안을 강제하는 **SOAP 프로토콜과 HTTP 표준 메서드 및 URI로 자원을 다루는 REST** 아키텍처 스타일 비교
- 배경/필요성: 엔터프라이즈 간 엄격한 트랜잭션 보장 요구와 웹·모바일 환경의 **경량 데이터 교환 및 캐싱 성능 요구 간의 상충 한계** 직면

#### 한줄 요약

- 엄격한 계약과 분산 트랜잭션은 SOAP, 경량 데이터 교환과 웹 캐싱을 활용한 고속 개발은 REST를 적용

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **WSDL (Web Services Description Language)**: SOAP 서비스가 제공하는 메서드, 파라미터, 반환 타입을 XML 스키마로 엄격히 정의한 서비스 명세서.
- **균일한 인터페이스(Uniform Interface)**: REST의 핵심 제약으로, 표준 HTTP 메서드와 상태 코드를 통해 클라이언트-서버 간 결합도를 낮추는 원칙.

</details>

- WSDL 기반의 엄격한 인터페이스 계약 및 WS-Security 기반의 **SOAP 고신뢰성 보장**
- URI 자원 식별과 HTTP 표준 메서드를 재사용하는 **REST의 경량성과 유연성**
- 표준 HTTP 캐싱(Cache-Control) 및 JSON 페이로드를 통한 **웹·모바일 최적화**

#### 한줄 요약

- 행위 중심의 엄격한 프로토콜(SOAP)과 자원 중심의 경량 웹 아키텍처(REST)의 상호 보완적 활용

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SOAP Envelope vs REST HTTP 메시지 구조**: SOAP Envelope(Header/Body/Fault) 대 REST URI/HTTP Methods/JSON Representation.

</details>

```text
[ SOAP 프로토콜(XML) vs REST 아키텍처(JSON) 구조 비교 ]

 1. [ SOAP 메시지 구조 (XML Envelope) ]
    ┌─────────────────────────────────────────────────────────────┐
    │ <soapenv:Envelope>                                          │
    │   <soapenv:Header> [ WS-Security 서명, 트랜잭션 ID ] </soapenv:Header>│
    │   <soapenv:Body>   [ <getUser><id>100</id></getUser> ]      │
    │   <soapenv:Fault>  [ 표준 오류 코드 및 스택 트레이스 ]      │
    │ </soapenv:Envelope>                                         │
    └─────────────────────────────────────────────────────────────┘

 2. [ REST 메시지 구조 (HTTP 표준 기반) ]
    ┌─────────────────────────────────────────────────────────────┐
    │ HTTP Request: GET /api/v1/users/100 HTTP/1.1                │
    │ Headers:      Accept: application/json, Authorization: Bearer│
    │ Response:     200 OK  ➔  { "id": 100, "name": "Kim" }       │
    │ Error:        404 Not Found  ➔  { "error": "User Not Found" }│
    └─────────────────────────────────────────────────────────────┘
```

선의 의미: Envelope 규격에 행위를 담아 호출하는 SOAP과 URI 자원에 HTTP 메서드로 접근하는 REST의 메시지 구조 차이.

| 구성요소 | 책임 |
|:---|:---|
| SOAP 프로토콜 | WSDL 명세 기반으로 **XML 봉투(Envelope)에 메서드 호출과 WS-보안을 캡슐화** |
| REST 아키텍처 | 명사형 URI로 자원을 식별하고 **HTTP 표준 메서드(CRUD)로 상태 전이 수행** |
| WSDL 명세서 | 컴파일 타임에 **메서드 파라미터와 반환 데이터 타입을 엄격하게 검증** |
| JSON 표현 계층 | 경량 텍스트 포맷으로 **모바일 및 웹 브라우저의 파싱 속도와 대역폭 효율 극대화** |

#### 한줄 요약

- SOAP(엄격한 XML 계약/보안), REST(경량 HTTP/JSON 자원 조작)가 상호 대조적 역할을 수행

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **API 요청 처리 5단계 파이프라인**: 인터페이스 식별 $\to$ 스키마/계약 검증 $\to$ 비즈니스 로직 실행 $\to$ 결과 직렬화 $\to$ 응답 반환.

</details>

```text
[ SOAP vs REST API 요청 수신 및 처리 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 클라이언트 API 요청 수신            │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 인터페이스 분기 및 스키마 검증      │
 ├───────────────────┬────────────────────┤
 │ SOAP 경로         │ REST 경로          │
 │ • WSDL XML 파싱   │ • URI / Method 해석│
 │ • WS-Security 검증│ • JSON 스키마 검증 │
 └───────────────────┴────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 공통 비즈니스 서비스 도메인 로직 실행│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 결과 직렬화: XML Envelope / JSON 매핑│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. HTTP 상태 코드 및 응답 패킷 회신    │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 요청 수신: API 게이트웨이가 클라이언트의 엔드포인트 요청을 접수.
2. 스키마 검증: SOAP은 WSDL 기반 XML 유효성을, REST는 OpenAPI/JSON 스키마와 HTTP 메서드를 검증.
3. 로직 실행: 인증 및 파라미터 검증을 통과한 요청을 백엔드 비즈니스 서비스로 전달하여 연산 수행.
4. 직렬화: 처리 결과를 SOAP은 `<soapenv:Envelope>` XML로, REST는 경량 JSON 페이로드로 직렬화.
5. 응답 회신: SOAP은 HTTP 200 기반 XML Fault를, REST는 표준 HTTP 상태 코드(200, 201, 404, 500)를 매핑하여 반환.

#### 한줄 요약

- 요청 수신 $\to$ 스키마 검증 $\to$ 비즈니스 실행 $\to$ 직렬화 $\to$ 응답 회신의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SOAP vs REST**: 프로토콜 여부, 페이로드 규격, 트랜잭션 지원, 캐싱에 따른 비교.

</details>

| 구분 | SOAP (Simple Object Access Protocol) | REST (Representational State Transfer) |
|:---|:---|:---|
| **적용 기준** | 금융권 코어 뱅킹, 결제 게이트웨이, B2B 대외 기관 연계 | 대고객 웹/모바일 앱, 오픈 API, MSA 서비스 간 통신 |
| **핵심 특징** | **엄격한 프로토콜, WSDL 계약, WS-Security, WS-트랜잭션** | **경량 아키텍처 스타일, HTTP 메서드 재사용, JSON 표준** |
| **한계** | 무거운 XML 오버헤드 및 모바일 파싱 지연, HTTP 캐싱 불가 | 분산 트랜잭션(2PC) 직접 미지원 및 계약 강제성 부족 |

#### 한줄 요약

- 엄격한 분산 트랜잭션과 보안은 SOAP, 웹/모바일의 고속 통신과 유연성은 REST를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **멱등성(Idempotency) 보장**: 네트워크 오류로 클라이언트가 동일한 API를 중복 호출해도 서버 상태가 단 1번만 변경되도록 `Idempotency-Key` 헤더를 활용하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SOAP의 무거운 XML 파싱과 POST 전용 통신으로 인한 성능 저하 | **대고객 조회 트래픽 영역을 REST/JSON 및 HTTP 캐싱으로 전환** | 응답 지연 70% 단축 및 서버 CPU 부하 절감 |
| 네트워크 순단 시 REST 클라이언트 재시도로 인한 중복 결제 | **HTTP 헤더에 고유 `Idempotency-Key` 발급 및 Redis 멱등성 검증** | 중복 결제 사고 원천 차단 |
| API 필드 수정 시 구버전 모바일 앱의 런타임 크래시 발생 | **URI 버저닝(`/v1`, `/v2`) 및 무중단 하위 호환 필드 추가 원칙 준수** | 하위 호환성 100% 보장 |

#### 한줄 요약

- REST 전환, 멱등 키 도입, URI 버저닝을 통해 통신 효율과 결제 안정성을 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **API 게이트웨이 변환 계층(API Transformation)**: 대외 레거시 SOAP 시스템과 내부 MSA REST 서비스를 API Gateway에서 실시간 상호 변환(XML $\leftrightarrow$ JSON)해 주는 현대적 연계 전략.

</details>

- **SOAP과 REST**는 상호 배타적인 경쟁 관계가 아닌 도메인 특성에 따른 최적의 선택지이며, 금융 트랜잭션과 B2B 계약은 SOAP으로 보호하고 대고객 웹/모바일 서비스는 RESTful API를 적용하여 엔터프라이즈 통합을 완성해야 함

#### 한줄 요약

- 엔터프라이즈 고신뢰성은 SOAP, 모바일 경량 웹 통신은 REST를 적재적소에 조합
