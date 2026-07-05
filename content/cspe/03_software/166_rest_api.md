---
title: "REST API (REST API)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 166
---

## Ⅰ. 개요
- **정의**: HTTP 메서드와 URI 기반으로 자원을 표현·조작하는 아키텍처 스타일
- **배경/필요성**: 서비스 간 통신의 표준화·상호 운용성을 위해 통일된 인터페이스 규약이 필요함
- **비유**: 도서관 색인 번호(URI)로 책(자원)을 찾고, 대출·반납(HTTP 메서드)하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| API 아키텍처 원칙 이해 | 무상태성·균일 인터페이스·자원 중심 설계 | RESTful 6대 제약 조건 누락 금지 |

> 요약: HTTP 메서드·URI 기반의 무상태 자원 조작 아키텍처 스타일임

## Ⅱ. 구성요소
```text
Client --HTTP Method--> [URI/Resource] --Representation--> Response
                             |
                    Stateless / Cacheable
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Resource | URI로 식별되는 서버 측 자원 | 도서관의 책 |
| HTTP Method | GET·POST·PUT·DELETE 등 자원 조작 동사 | 대출·반납·교환·폐기 행위 |
| Representation | JSON·XML 등 자원의 상태를 전달하는 표현 형식 | 책의 사본(복사본) |
| Statelessness | 각 요청이 독립적이며 서버가 세션 상태를 저장하지 않는 제약 | 매번 신분증을 제시하는 규칙 |

> 요약: Resource-Method-Representation-Statelessness 4요소로 통일된 인터페이스를 구성함

## Ⅲ. 절차
```text
URI 설계 --> 요청 전송 --> 서버 처리 --> 응답 반환
    |            |             |            |
    v            v             v            v
 자원 식별    Method+Header   비즈니스 로직  Status+Body
```
- 1단계: 자원을 명사형 URI(`/users/{id}`)로 식별하여 설계함
- 2단계: 클라이언트가 HTTP Method·Header·Body로 요청을 전송함
- 3단계: 서버가 무상태로 요청을 해석하고 비즈니스 로직을 수행함
- 4단계: HTTP Status Code와 Representation(JSON 등)으로 응답을 반환함

> 요약: URI 설계-요청-처리-응답 4단계로 자원을 조작함

## Ⅳ. 문제점
- Over-fetching: 고정 응답 구조로 클라이언트가 불필요한 필드까지 수신함
- Under-fetching: 관련 자원 조회 시 다수 엔드포인트를 순차 호출해야 함
- 버전 관리 복잡: API 변경 시 하위 호환성 유지·버전 전략 수립이 어려움

> 요약: Over/Under-fetching·버전 관리가 주요 한계임

## Ⅴ. 개선방안
1. 단기: 필드 필터링 파라미터(`?fields=`)로 Over-fetching 완화
2. 중기: Compound Document·임베디드 자원으로 Under-fetching 감소
3. 장기: API 버전 관리 전략(169 참조) 수립 및 자동화 도구 도입

> 요약: 필드 필터-복합 문서-버전 전략 순으로 개선함

## Ⅵ. 전망
- 발전 방향: GraphQL(165 참조)·gRPC(167 참조)와 용도별 공존 체계로 진화 중임
- 기술사적 판단: 범용 API의 기본 아키텍처로서 지위가 유지됨
- 기술사 제언: HATEOAS 수준의 성숙도 모델을 고려한 설계 가이드라인 수립이 필요함
