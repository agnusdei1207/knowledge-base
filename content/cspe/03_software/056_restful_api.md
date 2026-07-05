---
title: RESTful API 설계 원칙 (RESTful API)
date: 2026-07-05
tags: ["cspe-software"]
weight: 56
---

## Ⅰ. 개요
- 정의: HTTP 프로토콜의 장점을 극대화하기 위해 리소스 중심의 무상태 인터페이스 설계 스타일.
- 출제 의도: 웹 표준을 준수하는 API 설계 역량 및 REST의 6가지 핵심 제약 조건 이해 확인.

## Ⅱ. 구성요소
- ASCII 구조도
  [ Method ]   [ Resource (URI) ]   [ Representation ]
  GET, POST    /users/{id}          JSON, XML
  PUT, DELETE  /orders/2026         Status Code
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 리소스 (URI) | 모든 자원은 고유한 이름(URI)으로 식별됨 | 사물함 번호 |
| 행위 (Verb) | HTTP 메서드를 통해 자원에 대한 행위 정의 | 조작 버튼 |
| 표현 (Message) | 자원의 상태를 JSON 등 특정 형식으로 표현 | 문서 양식 |
> 요약: URI는 명사를 사용하고, 행위는 메서드로 명확히 구분하여 가독성 높임.

## Ⅲ. 절차
- ASCII 흐름도
  [리소스 식별] -> [메서드 선정] -> [상태 코드 정의] -> [HATEOAS 적용]
- 4단계 설명
1. 도메인 모델에서 관리할 명사 중심의 리소스를 계층 구조로 명명함.
2. 조회(GET), 생성(POST), 수정(PUT/PATCH), 삭제(DELETE) 메서드 매핑함.
3. 요청 결과에 맞는 표준 HTTP 상태 코드(200, 201, 400, 500 등) 반환함.
4. 응답 메시지에 연관된 리소스 링크를 포함하여 다음 행위 안내함.
> 요약: 자체 표현 구조(Self-descriptive)를 통해 API의 독립성을 확보함.

## Ⅳ. 문제점
- Over-fetching: 필요 이상의 방대한 데이터를 응답받아 네트워크 대역폭 낭비함.
- Under-fetching: 한 번의 화면 구성을 위해 여러 번의 API 호출이 발생하여 지연 시간 증가함.

## Ⅴ. 개선방안
- Partial Response: 쿼리 파라미터를 통해 필요한 필드만 선택적으로 응답받도록 설계함.
- API 버전 관리: URI에 `/v1/`, `/v2/` 등을 명시하여 하위 호환성 유지 및 점진적 개선함.

## Ⅵ. 전망
- GraphQL과의 상호 보완적 발전을 통해 하이브리드 형태의 API 서비스 모델 확산됨.
- AI가 API 명세서(Swagger/OpenAPI)를 분석하여 자동 테스트 및 클라이언트 코드를 생성함.
- 보안 강화를 위해 OAuth2.0/OIDC 기반의 인증 체계가 모든 REST API의 필수 기본 요건이 됨.
