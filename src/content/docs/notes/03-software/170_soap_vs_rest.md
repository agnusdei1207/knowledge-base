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

<details><summary>핵심 용어</summary>

- **SOAP (Simple Object Access Protocol)**: XML(Extensible Markup Language) 기반으로 HTTP, SMTP 등 다양한 트랜스포트 프로토콜 위에서 엄격한 메시지 포맷과 보안(WS-Security) 규격을 강제하는 엔터프라이즈급 API 연계 프로토콜.
- **REST (Representational State Transfer)**: URI(Uniform Resource Identifier)로 자원을 식별하고, HTTP의 4대 메서드(GET, POST, PUT, DELETE)만을 사용하여 상태를 주고받는 경량화된 웹 표준 아키텍처 스타일.
- **WSDL (Web Services Description Language)**: SOAP API가 제공하는 함수(메서드), 파라미터, 반환값 타입 등을 기계가 읽을 수 있는 XML 형태로 엄격하게 정의한 서비스 명세서.

</details>

- 정의/개념: 이기종 시스템 간 통신을 위해 보안과 트랜잭션 등 엄격한 규격을 강조하는 프로토콜인 **SOAP**과 자원(Resource) 식별 및 웹 고유의 단순함을 지향하는 아키텍처 스타일인 **REST**의 비교 및 선택 기준
- 배경/필요성: B2B 금융 연계처럼 무결성(ACID)과 보안이 최우선인 환경과, B2C 모바일 앱처럼 속도와 캐싱 확장성이 중요한 환경이 달라 단일 방식으로 모든 API 연계 요구사항을 충족하기 어려운 한계성 극복

#### 한줄 요약

- SOAP은 정해진 봉투와 계약으로 업무 연산을 호출하고 REST는 주소와 HTTP 의미로 자원 상태를 조회·변경한다.

## Ⅱ. 특징 (설계 철학 대조)

<details><summary>핵심 용어</summary>

- **WS-* (Web Services Specifications)**: SOAP 생태계에서 라우팅, 신뢰성 보장(WS-ReliableMessaging), 트랜잭션(WS-AtomicTransaction) 등을 제공하기 위해 체계화된 확장 표준 스펙 모음.

</details>

- **SOAP**: Protocol (규약), XML Only, Action-Centric (행위 중심), WS-Security 탑재
- **REST**: Architectural Style (스타일), JSON/XML/Text 자유도, Resource-Centric (자원 중심), HTTPS에 의존
- **Statelessness (무상태성)**: SOAP과 REST 모두 기본적으로 서버가 클라이언트의 상태를 저장하지 않는 무상태성 원칙 준수

#### 한줄 요약

- SOAP은 기관 간 문서처럼 형식과 서명을 엄격히 맞추고 REST는 웹의 주소·메서드·캐시 규칙을 재사용해 인터페이스를 단순화한다.

## Ⅲ. 구조 및 구성요소 (아키텍처 및 페이로드 비교)

<details><summary>핵심 용어</summary>

- **Envelope (봉투 구조)**: SOAP 메시지의 최상위 요소로, Header(인증, 트랜잭션 정보)와 Body(실제 호출할 데이터 및 오류 내역인 Fault)를 감싸는 포장지.

</details>

```text
┌────────────────────────┐         ┌────────────────────────┐
│   SOAP Architecture    │   VS    │   REST Architecture    │
├────────────────────────┤         ├────────────────────────┤
│ [HTTP / SMTP / MQ]     │         │ [HTTP / HTTPS Only]    │
│   │                    │         │   │                    │
│   ▼                    │         │   ▼                    │
│ <Envelope>             │         │ GET /users/123 HTTP/1.1│
│  <Header>보안</Header> │         │ Accept: application/json│
│  <Body>                │         │                        │
│   <GetBalance>         │         │ {                      │
│     <Id>123</Id>       │         │   "id": 123,           │
│   </GetBalance>        │         │   "balance": 5000      │
│  </Body>               │         │ }                      │
│ </Envelope>            │         │                        │
└────────────────────────┘         └────────────────────────┘
```

선의 의미: SOAP은 어떤 전송 계층을 쓰든 거대한 XML 봉투 안에 행위와 데이터를 캡슐화하고, REST는 HTTP 자체의 주소(URI)와 메서드(Method)를 직접 활용하여 경량 페이로드를 전달하는 구조적 차이.

| 구성요소 | SOAP 역할 | REST 역할 |
|:---|:---|:---|
| **설계 중심** | **Function / Action (행위 위주)** | **Resource / Entity (자원 위주)** |
| **명세(Contract)** | **WSDL (의무적이고 엄격한 XML 계약)**| **OpenAPI / Swagger (자율적 명세)** |
| **전송 프로토콜**| **HTTP, SMTP, TCP, UDP 등 독립적** | **HTTP 프로토콜에 전적으로 종속됨**|
| **오류 처리** | **SOAP Fault 태그 내 상세 코드 반환**| **HTTP Status Code (404, 500) 사용**|
| **보안 체계** | **WS-Security (엔터프라이즈급 내장)**| **HTTPS / TLS + OAuth2 / JWT 위임** |

#### 한줄 요약

- 클라이언트가 SOAP 문서 창구나 REST 자원 창구를 선택해도 계약·보안 검사를 거쳐 같은 업무 서비스에 도달한다.

## Ⅳ. 흐름도 (상태 조작 대 행위 호출 흐름)

<details><summary>핵심 용어</summary>

- **Uniform Interface (균일 인터페이스)**: REST의 제약 조건 중 하나로, 모든 자원에 대해 통일된 HTTP 메서드(CRUD) 조작 방식을 적용하여 클라이언트-서버 결합도를 낮추는 아키텍처 원칙.

</details>

```text
[클라이언트 앱]
       │
       ├─ (REST) ──► POST /payments (결제 자원 생성) ──► HTTP 201 Created
       │
       └─ (SOAP) ──► POST /PaymentService (SOAP Action: ExecutePayment)
                       <Envelope><Body><ExecutePayment>...</ExecutePayment></Body></Envelope>
                       ──► HTTP 200 OK (비즈니스 에러 시에도 200 OK 내부에 Fault 전송 가능)
```

### 동작 원리

1. **REST 흐름**: 클라이언트가 `POST /payments` 로 자원 생성을 요청하면, 웹 서버가 HTTP 201 상태 코드와 생성된 자원의 URI를 응답.
2. **SOAP 흐름**: 클라이언트가 단일 EndPoint `/PaymentService` 에 XML 봉투를 전송하면, 파싱 엔진이 봉투를 뜯어 내부 `ExecutePayment` 메서드를 실행.
3. **에러 반환**: REST는 HTTP 프로토콜 규약(400, 500)을 그대로 따르나, SOAP은 종종 HTTP 200을 던진 후 XML Body 안에 `<Fault>` 코드를 내려주는 차이 발생 (**API 처리 완결**).

#### 한줄 요약

- SOAP 요청은 봉투와 연산 계약을 먼저 검사하고 REST 요청은 주소·메서드·표현을 해석한 뒤 각 방식의 표준 오류 형태로 결과를 돌려준다.

## Ⅴ. 종류 및 비교 (도입 시나리오 1:1 비교)

<details><summary>핵심 용어</summary>

- **ACID Transaction**: 데이터베이스의 원자성, 일관성, 고립성, 지속성. SOAP은 WS-AtomicTransaction을 통해 분산 환경에서도 2PC 수준의 트랜잭션을 지원하지만 REST는 이를 직접 지원하지 못함.

</details>

| 비교 항목 | SOAP (금융/B2B 엔터프라이즈) | REST (모바일/웹 B2C 서비스) |
|:---|:---|:---|
| **적합한 비즈니스**| **은행 송금, 결제 게이트웨이, B2B 통합** | **모바일 앱 API, SPA 웹 프론트엔드 연동**|
| **트랜잭션/상태**| **WS-AtomicTransaction 지원 (복잡한 분산 제어)**| 직접 지원 안 함 (분산 트랜잭션 Saga 패턴 구현 필요)|
| **네트워크 대역폭**| **XML 헤더와 태그로 인해 페이로드가 매우 큼**| **JSON 사용으로 가볍고 파싱 속도 빠름** |
| **캐싱 (Caching)** | GET이 아닌 POST로 봉투를 보내므로 캐싱 불가 | **HTTP 표준 GET을 활용하여 완벽한 분산 캐싱 지원**|

#### 한줄 요약

- 메시지 서명과 신뢰성 명세가 중요한 기관 연계는 SOAP을, 공개 자원을 웹 방식으로 조회하는 인터페이스는 REST를 우선 검토한다.

## Ⅵ. 실무 고려사항 및 대책 (API 연계 3대 난제 대책)

<details><summary>핵심 용어</summary>

- **Idempotency (멱등성)**: 동일한 API 요청을 여러 번 수행해도 서버의 상태가 단 1번 수행한 것과 동일하게 유지되는 성질 (REST의 PUT/DELETE는 본질적으로 멱등성을 지님).

</details>

| 3대 API 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. SOAP 캐싱 한계** | 모든 요청을 `POST`로 전송 | **조회 트래픽이 많은 시스템은 REST로의 마이그레이션 추진**|
| **2. 비즈니스 중복 처리**| 네트워크 순단 시 결제 2번 요청 | **HTTP 헤더에 고유 Idempotency-Key 발급 및 서버 체크**|
| **3. 하위 호환성 붕괴** | 파라미터 필드 삭제로 기존 클라이언트 에러| **URI 버저닝(`/v1/api`, `/v2/api`) 및 폐기 예정 통보(Deprecation)**|

> 사례: **은행권 공동 오픈 API 망의 RESTful 전환 및 모바일 페이먼트 시스템의 JSON 경량화 아키텍처**

#### 한줄 요약

- 어느 방식을 사용해도 재시도되는 결제 요청에는 멱등 키를 두고 계약 변경은 기존 소비자가 이해하는 필드를 유지해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **API Gateway**: SOAP/XML 요청을 받아 내부 Microservice에 맞게 REST/JSON으로 자동 변환해 주는 브릿지 역할의 클라우드 인프라 관문.

</details>

- **API 선택 기준**에 따라 레거시 B2B 트랜잭션 망은 **SOAP**을, 클라우드 네이티브 MSA 및 모바일 연동 망은 **REST** 기반 아키텍처 필수 채택

#### 한줄 요약

- XML 크기만 보지 말고 분산 트랜잭션 보안 요구와 웹 생태계(캐시, JSON) 편의성의 교집합을 기준으로 아키텍처를 선택해야 한다.
