---
title: "SOAP vs REST 비교 (SOAP vs REST)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 199
extra:
  question_no: "199"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- SOAP은 XML Envelope·Header·Body·Fault와 노드별 메시지 처리 규칙을 정의하는 메시징 프로토콜임
- SOAP 메시지는 HTTP 외의 전송 프로토콜에도 바인딩할 수 있으며 WSDL·WS-* 규격과 함께 사용할 수 있음
- REST는 자원을 URI로 식별하고 표현을 전송하며 무상태·캐시·균일 인터페이스 제약을 따르는 아키텍처 스타일임
- REST API는 JSON으로 제한되지 않으며 HTTP의 메서드·상태 코드·콘텐츠 협상·캐시 의미를 인터페이스에 사용함
- SOAP과 REST는 XML과 JSON의 형식 비교가 아니라 메시지 계약과 자원 상태 전이의 설계 방식으로 구분해야 함

## 작성 근거(검토용)

- SOAP과 REST는 추상화 대상, 인터페이스 계약, 전송 결합, 상태·캐시, 확장 기능, 표현 형식, 적용 조건으로 비교함
- SOAP 구조는 Envelope 처리 경로, REST 구조는 자원·표현·HTTP 의미가 드러나도록 분리함
- 기관 연계와 모바일 조회 API는 스키마 오류율·재전송 성공률·응답 크기·p95 지연으로 검증함

## Ⅰ. 개요

- **정의/개념**: SOAP은 구조화 메시지의 생성·전달·중계·오류 처리 규칙을 정의하고, REST는 자원 표현을 균일 인터페이스로 조작하는 분산 시스템 아키텍처 스타일임
- **배경/필요성**: 서비스 간 연계에서 형식 계약·메시지 확장·전송 독립성이 필요한지, HTTP 자원 의미·무상태·캐시를 활용할지에 따라 인터페이스 구조를 선택해야 함

## Ⅱ. 특징

- SOAP은 Envelope 안에서 대상 노드의 Header를 처리한 뒤 Body의 응용 메시지를 전달하고 오류를 Fault로 표현함
- WSDL·XML Schema를 사용하면 연산·메시지 형식·엔드포인트를 기계 판독 가능한 계약으로 관리할 수 있음
- REST는 요청마다 처리에 필요한 상태를 포함하고 URI·HTTP 메서드·상태 코드로 자원 인터페이스를 구성함
- REST 응답은 Cache-Control·ETag 같은 HTTP 메타데이터로 재검증과 캐시 정책을 표현할 수 있음
- SOAP의 보안·신뢰성·트랜잭션은 WS-* 확장 규격에서, REST API의 인증·재시도·멱등성은 HTTP·응용 계약에서 설계함

## Ⅲ. 종류 및 비교

| 판단 기준 | SOAP | REST |
|:---|:---|:---|
| 추상화 대상 | 연산과 구조화 메시지 교환 | 자원과 자원 표현의 상태 전이 |
| 인터페이스 계약 | WSDL·XML Schema로 연산·메시지 형식 기술 | URI·HTTP 의미를 설계하고 OpenAPI를 선택 사용 |
| 전송 결합 | SOAP 바인딩으로 HTTP·TCP 등과 연결 | HTTP의 메서드·상태 코드·헤더를 인터페이스에 사용 |
| 상태·캐시 | 응용·확장 규격이 대화 상태와 전달 정책 정의 | 요청 무상태와 명시적 응답 캐시 제약 적용 |
| 메시지 확장 | Header 역할·mustUnderstand와 WS-* 모듈 | HTTP 헤더·미디어 타입·링크·응용 규칙 |
| 표현 형식 | SOAP XML Infoset의 Envelope 구조 | JSON·XML 등 협상된 자원 표현 |
| 적합 조건 | 엄격한 메시지 계약·중계·WS-* 상호운용 필요 | HTTP 자원 인터페이스·캐시·클라이언트 독립성 필요 |

> 요약: SOAP은 XML 메시지 계약과 처리 확장을, REST는 자원·무상태·캐시·균일 인터페이스를 중심으로 설계함.

## Ⅳ. 구성요소 및 구조

| 구분 | 핵심 구성 | 처리 역할 |
|:---|:---|:---|
| SOAP 계약 | WSDL·XML Schema | 연산·입출력 메시지·바인딩·엔드포인트를 기술함 |
| SOAP 메시지 | Envelope·Header·Body·Fault | 확장 메타데이터·응용 내용·오류를 구조화함 |
| SOAP 처리 노드 | 송신자·중계자·최종 수신자 | 역할에 지정된 Header와 Body를 규칙에 따라 처리함 |
| REST 식별 | 자원 URI | 클라이언트가 조작할 자원을 식별함 |
| REST 인터페이스 | HTTP 메서드·상태 코드·헤더 | 자원 조작·처리 결과·캐시·콘텐츠 협상을 표현함 |
| REST 표현 | JSON·XML 등 미디어 타입 | 현재 자원 상태와 다음 동작에 필요한 정보를 전달함 |

```text
SOAP: Client -> Envelope[Header|Body] -> Intermediary -> Receiver -> Body|Fault
REST: Client -> URI + HTTP Method -> Resource Handler -> Status + Representation
```

> 요약: SOAP 노드는 Envelope의 대상 Header와 Body를 처리하고, REST 자원 핸들러는 URI·HTTP 의미에 따라 표현을 반환함.

## Ⅵ. 실무 사례

1. 기관 업무 연계는 WSDL·XML Schema·WS-Security를 적용하고 스키마 오류율·서명 검증 실패율을 확인함
2. 모바일 상품 조회는 REST 자원·ETag·Cache-Control을 적용하고 응답 크기·p95 지연을 확인함

## Ⅶ. 결론

- SOAP과 REST는 메시지 계약·중계 확장 요구와 자원 인터페이스·무상태·캐시 요구를 기준으로 선택해야 함
