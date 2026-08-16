---
sidebar:
  order: 170
  label: "170. SOAP vs REST 비교 (SOAP vs REST)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SOAP vs REST 비교 (SOAP vs REST)"
date: "2026-08-14T03:12:00+09:00"
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

- **SOAP (Simple Object Access Protocol)**: XML(Extensible Markup Language) 기반으로 HTTP, SMTP 등 다양한 트랜스포트 프로토콜 위에서 엄격한 메시지 포맷과 보안(WS-Security) 규격을 강제하는 엔터프라이즈급 API 연계 프로토콜.
- **REST (Representational State Transfer)**: URI(Uniform Resource Identifier)로 자원을 식별하고, HTTP의 4대 메서드(GET, POST, PUT, DELETE)만을 사용하여 상태를 주고받는 경량화된 웹 표준 아키텍처 스타일.
- **WSDL (Web Services Description Language)**: SOAP API가 제공하는 함수(메서드), 파라미터, 반환값 타입 등을 기계가 읽을 수 있는 XML 형태로 엄격하게 정의한 서비스 명세서.

</details>

- 정의/개념: XML Message Protocol **SOAP**과 Resource Style **REST** 비교
- 배경/필요성: 계약•WS-* 요구와 **HTTP 단순성•Cache** 요구를 단일 방식으로 충족 곤란

#### 한줄 요약

- SOAP은 정해진 봉투와 계약으로 업무 연산을 호출하고 REST는 주소와 HTTP 의미로 자원 상태를 조회·변경한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **WS-* (Web Services Specifications)**: SOAP 생태계에서 라우팅, 신뢰성 보장(WS-ReliableMessaging), 트랜잭션(WS-AtomicTransaction) 등을 제공하기 위해 체계화된 확장 표준 스펙 모음.

</details>

- **SOAP**은 XML Envelope와 WSDL•WS-* 확장 규격 중심
- **REST**는 Resource•Representation과 HTTP 의미 활용
- REST의 **Stateless 제약**은 요청별 처리 문맥 완결 요구

#### 한줄 요약

- SOAP은 기관 간 문서처럼 형식과 서명을 엄격히 맞추고 REST는 웹의 주소·메서드·캐시 규칙을 재사용해 인터페이스를 단순화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Envelope (봉투 구조)**: SOAP 메시지의 최상위 요소로, Header(인증, 트랜잭션 정보)와 Body(실제 호출할 데이터 및 오류 내역인 Fault)를 감싸는 포장지.

</details>

| 구성요소 | SOAP 역할 | REST 역할 |
|:---|:---|:---|
| 설계 중심 | **Function / Action (행위 위주)** | **Resource / Entity (자원 위주)** |
| 명세 | **WSDL 기반 XML 계약**| OpenAPI 등 별도 명세 선택 |
| 전송 프로토콜 | HTTP 등 Transport와 Message 규격 분리 | **HTTP 의미 체계** 활용 |
| 오류 처리 | **SOAP Fault** 구조 | HTTP Status와 Problem Detail 등 |
| 보안 체계 | **WS-Security** 확장 가능 | TLS•OAuth 등 Web 보안 조합 |

#### 한줄 요약

- 클라이언트가 SOAP 문서 창구나 REST 자원 창구를 선택해도 계약·보안 검사를 거쳐 같은 업무 서비스에 도달한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Uniform Interface (균일 인터페이스)**: REST의 제약 조건 중 하나로, 모든 자원에 대해 통일된 HTTP 메서드(CRUD) 조작 방식을 적용하여 클라이언트-서버 결합도를 낮추는 아키텍처 원칙.

</details>

```text
[API 요청]
    │
    ▼
1. Interface 유형 식별
    │
    ▼
2. 계약•Message 검증
    │
    ▼
3. Action•Resource 처리
    │
    ▼
4. 오류•표현 Mapping
    │
    ▼
5. Protocol 응답 생성
    │
    ▼
[API 응답]
```

### 동작 원리

1. **Interface 유형 식별**: SOAP Action 또는 REST Method 확인
2. **계약•Message 검증**: WSDL Schema 또는 API 계약 검사
3. **Action•Resource 처리**: 연산 호출 또는 자원 상태 조작
4. **오류•표현 Mapping**: Fault 또는 HTTP 표현으로 변환
5. **Protocol 응답 생성**: Envelope 또는 Representation 반환

#### 한줄 요약

- SOAP 요청은 봉투와 연산 계약을 먼저 검사하고 REST 요청은 주소·메서드·표현을 해석한 뒤 각 방식의 표준 오류 형태로 결과를 돌려준다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ACID Transaction**: 데이터베이스의 원자성, 일관성, 고립성, 지속성. SOAP은 WS-AtomicTransaction을 통해 분산 환경에서도 2PC 수준의 트랜잭션을 지원하지만 REST는 이를 직접 지원하지 못함.

</details>

| 비교 항목 | SOAP (금융/B2B 엔터프라이즈) | REST (모바일/웹 B2C 서비스) |
|:---|:---|:---|
| 적합한 비즈니스 | **은행 송금, 결제 게이트웨이, B2B 통합** | **모바일 앱 API, SPA 웹 프론트엔드 연동**|
| 트랜잭션/상태 | **WS-AtomicTransaction 지원 (복잡한 분산 제어)**| 직접 지원 안 함 (분산 트랜잭션 Saga 패턴 구현 필요)|
| Payload 특성 | XML Envelope 부가 정보 | 표현 형식 선택 가능 |
| Caching | Transport•Gateway별 별도 설계 | **HTTP Cache 의미** 활용 가능 |

#### 한줄 요약

- 메시지 서명과 신뢰성 명세가 중요한 기관 연계는 SOAP을, 공개 자원을 웹 방식으로 조회하는 인터페이스는 REST를 우선 검토한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Idempotency (멱등성)**: 동일한 API 요청을 여러 번 수행해도 서버의 상태가 단 1번 수행한 것과 동일하게 유지되는 성질 (REST의 PUT/DELETE는 본질적으로 멱등성을 지님).

</details>

| 3대 API 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. SOAP 캐싱 한계 | 모든 요청을 `POST`로 전송 | **조회 트래픽이 많은 시스템은 REST로의 마이그레이션 추진**|
| 2. 비즈니스 중복 처리 | 네트워크 순단 시 결제 2번 요청 | **HTTP 헤더에 고유 Idempotency-Key 발급 및 서버 체크**|
| 3. 하위 호환성 붕괴 | 파라미터 필드 삭제로 기존 클라이언트 에러| **URI 버저닝(`/v1/api`, `/v2/api`) 및 폐기 예정 통보(Deprecation)**|

> 사례: **은행권 공동 오픈 API 망의 RESTful 전환 및 모바일 페이먼트 시스템의 JSON 경량화 아키텍처**

#### 한줄 요약

- 어느 방식을 사용해도 재시도되는 결제 요청에는 멱등 키를 두고 계약 변경은 기존 소비자가 이해하는 필드를 유지해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **API Gateway**: SOAP/XML 요청을 받아 내부 Microservice에 맞게 REST/JSON으로 자동 변환해 주는 브릿지 역할의 클라우드 인프라 관문.

</details>

- WS-* 계약 연계는 **SOAP**, Web Resource API는 REST 우선 선택

#### 한줄 요약

- XML 크기만 보지 말고 분산 트랜잭션 보안 요구와 웹 생태계(캐시, JSON) 편의성의 교집합을 기준으로 아키텍처를 선택해야 한다.
