---
sidebar:
  order: 170
  label: "170. SOAP vs REST 비교"
  badge:
    text: "기출 · 70%"
    variant: note
title: "SOAP vs REST 비교 (SOAP vs REST)"
date: "2026-08-31T10:48:00+09:00"
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

- **SOAP vs REST**: XML 메시지 포맷과 WSDL 계약 및 WS-* 표준을 강제하는 프로토콜(SOAP)과 HTTP 메서드 및 URI로 JSON 자원을 다루는 아키텍처 스타일(REST).
- **Uniform Interface**: REST의 핵심 제약 조건으로, 표준 HTTP 메서드(GET/POST/PUT/DELETE)와 상태 코드를 통해 클라이언트-서버 간 결합도를 최소화.

</details>

- 정의/개념: 엄격한 XML 계약과 WS-보안을 강제하는 **SOAP 프로토콜과 HTTP 표준 메서드 및 URI로 자원을 다루는 REST 아키텍처 스타일의 웹 서비스 비교 패러다임**
- 배경/필요성: SOAP 프로토콜의 무거운 XML 파싱 부하, **HTTP POST 단일 메서드 사용에 따른 웹 캐싱 불가 및 모바일/웹 환경의 높은 대역폭 낭비 한계**

#### 한줄 요약
- 엄격한 계약과 분산 트랜잭션은 SOAP, 캐싱과 균일한 인터페이스(Uniform Interface)는 REST를 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **WSDL**: SOAP 서비스가 제공하는 메서드, 파라미터, 반환 타입을 XML 스키마로 엄격히 정의한 서비스 명세서.
- **Statelessness**: REST의 무상태성 원칙으로 각 요청은 인증 정보 등 처리에 필요한 모든 문맥을 자체 포함.

</details>

- WSDL 기반의 엄격한 인터페이스 계약 및 WS-Security 기반의 **SOAP 고신뢰성 보장**
- URI 자원 식별과 HTTP 표준 메서드를 재사용하는 **REST의 경량성과 유연성**
- 표준 HTTP 캐싱(Cache-Control) 및 JSON 페이로드를 통한 **웹·모바일 성능 최적화**

#### 한줄 요약
- SOAP은 보안과 트랜잭션을 프로토콜 안에 내장해 무게를 얻었고, REST는 그것을 HTTP와 애플리케이션에 위임해 가벼움을 얻었다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **메시지 구조 비교**: SOAP Envelope 구조(Header/Body/Fault XML), REST 구조(HTTP Method + URI + JSON).

</details>

```text
[SOAP XML 봉투 구조 및 REST 자원 구조]
|-- SOAP 프로토콜
|   `-- XML 봉투(Envelope)에 RPC 메서드 호출 및 보안 캡슐화
|-- REST 아키텍처
|   `-- 명사형 URI 및 HTTP Method (GET/POST/PUT/DELETE) 기반 상태 전이
|-- WSDL 명세서
|   `-- 컴파일 타임 파라미터 및 반환 데이터 타입 엄격 검증 계약
`-- JSON 표현 계층
    `-- 초경량 텍스트 포맷으로 모바일/웹 통신 대역폭 최적화
```

선의 의미: 계층 및 Envelope 규격에 행위를 담아 호출하는 SOAP과 URI 자원에 HTTP 메서드로 접근하는 REST의 메시지 구조 차이

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| SOAP 프로토콜 | WSDL 명세 기반으로 **XML 봉투(Envelope)에 메서드 호출과 WS-보안을 캡슐화** | 정적 타입 계약 |
| REST 아키텍처 | 명사형 URI로 자원을 식별하고 **HTTP 표준 메서드(CRUD)로 상태 전이 수행** | 자원 지향 아키텍처 |
| WSDL 명세서 | 컴파일 타임에 **메서드 파라미터와 반환 데이터 타입을 엄격하게 검증** | 강결합 스키마 |
| JSON 표현 계층 | 경량 텍스트 포맷으로 **모바일 및 웹 브라우저의 파싱 속도와 대역폭 효율 극대화**| 초경량 직렬화 |

#### 한줄 요약
- SOAP은 계약 검증을 WSDL 스키마 계층이 대신 떠맡고 REST는 그 계층을 없앤 대신 HTTP 규약 자체를 계약으로 삼으므로, 검증 비용을 어디에 둘 것인가가 두 방식을 가른다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **API 요청 처리 5단계**: 요청 수신 $\to$ 스키마 검증 $\to$ 도메인 로직 실행 $\to$ 결과 직렬화 $\to$ 응답 패킷 회신.

</details>

```text
클라이언트의 API 호출 요청 접수
        │
   1. [요청 수신] API 게이트웨이가 클라이언트의 엔드포인트 요청 패킷 수신
        │
   2. [스키마 검증] 인터페이스 유형에 따른 스키마 및 보안 검증
   ┌────┴───────────────────────────┐
  SOAP 경로                         REST 경로
   │                                 │
  WSDL XML 스키마 검증            URI 자원 및 HTTP Method 해석
  WS-Security 전자서명 확인       JSON Schema 및 Bearer 토큰 검증
   │                                 │
   └────┬────────────────────────────┘
        ▼
   3. [비즈니스 로직 실행] 검증 통과된 파라미터를 백엔드 서비스로 전달하여 연산 수행
        │
   4. [결과 직렬화] SOAP은 XML Envelope, REST는 경량 JSON 페이로드로 직렬화
        │
   5. [응답 회신] SOAP은 XML Fault, REST는 표준 HTTP 상태 코드 매핑하여 회신
```

#### 한줄 요약
- 스키마 검증을 통신 계층에서 강제하면 잘못된 요청이 로직에 닿기 전에 걸러지지만, 그 대가로 정상 요청까지 매번 파싱·검증 비용을 고정으로 지불한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SOAP vs REST**: 프로토콜 표준, 데이터 포맷, 전송 계층, 분산 트랜잭션, 캐싱 지원에 따른 비교.

</details>

| 비교 항목 | SOAP (Simple Object Access Protocol) | REST (Representational State Transfer) |
|:---|:---|:---|
| 아키텍처 성격 | **엄격한 표준 통신 프로토콜 (W3C)** | **유연한 웹 아키텍처 스타일 (Roy Fielding)** |
| 데이터 포맷 | **XML 단일 포맷 전용** | **JSON, XML, YAML 등 다중 포맷 지원** |
| 전송 프로토콜 | HTTP, HTTPS, SMTP, TCP 등 다중 전송 | **HTTP / HTTPS 전송 계층 전용** |
| 트랜잭션 지원 | **WS-AtomicTransaction 기반 2PC 지원** | 분산 트랜잭션 미지원 (Saga 패턴 별도 구현) |
| 웹 캐싱 활용 | 불가능 (모든 요청이 HTTP POST 기반) | **가능 (HTTP GET 기반 CDN/브라우저 캐싱)** |
| 최적 적용 분야 | **금융 코어 원장, 결제 PG사 연계, B2B EDI** | **대고객 웹/모바일 앱, MSA 오픈 API** |

#### 한줄 요약
- 엄격한 분산 트랜잭션과 보안은 SOAP, 웹/모바일의 고속 통신과 유연성은 REST를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Idempotency Key**: 네트워크 장애로 인한 재시도 시 동일 결제가 중복 승인되지 않도록 고유 키를 기반으로 단 1회만 처리하는 멱등성 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SOAP의 무거운 XML 파싱과 POST 전용 통신으로 인한 성능 저하 | **대고객 조회 트래픽 영역을 REST/JSON 및 HTTP 캐싱으로 전환** | 응답 지연 70% 단축 및 서버 CPU 부하 절감 |
| 네트워크 순단 시 REST 클라이언트 재시도로 인한 중복 결제 | **HTTP 헤더에 고유 `Idempotency-Key` 발급 및 Redis 멱등성 검증** | 중복 결제 사고 원천 차단 |
| API 필드 수정 시 구버전 모바일 앱의 런타임 크래시 발생 | **URI 버저닝(`/v1`, `/v2`) 및 무중단 하위 호환 필드 추가 원칙 준수** | 하위 호환성 100% 보장 |
| REST의 엄격한 계약 부재로 인한 협업 오류 | **OpenAPI 3.0 (Swagger) 명세서 기반 Contract Testing 도입** | 개발-소비자 간 스키마 정합성 보장 |

#### 한줄 요약
- 네 대책은 REST가 버린 엄격한 계약과 재시도 안전성을 멱등 키·버저닝·OpenAPI로 필요한 지점에만 다시 사 오는 선택이다.

## Ⅶ. 결론

- 현대 분산 소프트웨어 아키텍처에서 대고객 웹/모바일 서비스와 MSA의 **지배적인 표준 인터페이스(REST)와 금융/공공 고신뢰성 레거시 통신(SOAP)의 명확한 역할 분담 체계**로 정립되었으며, 실무 구축 시에는 **공공/금융 코어 원장 및 B2B 전문 연계에는 WS-Security/WSDL 기반 SOAP을 유지하고, 대외 오픈 API 및 마이크로서비스 간 통신에는 OpenAPI 3.0 명세 기반 RESTful JSON API를 적용하며, 네트워크 결함 시 중복 처리를 방어하는 `Idempotency-Key` 및 URI 버저닝(`/v1`) 거버넌스**를 결합하여 비즈니스 안정성과 개발 생산성을 완벽히 조화

#### 한줄 요약
- SOAP과 REST는 상호 배타적 경쟁 기술이 아니라, 엄격한 엔터프라이즈 보안·트랜잭션(SOAP)과 경량 웹·모바일 민첩성(REST)이라는 각자의 영역에서 최적의 성능을 발휘하는 핵심 연계 패러다임이다.
