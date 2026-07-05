---
title: GraphQL vs REST (GraphQL vs REST)
date: 2026-07-05
tags: ["cspe-software"]
weight: 57
---

## Ⅰ. 개요
- 정의: 리소스 중심의 전통적 REST와 클라이언트가 필요한 데이터만 쿼리하는 GraphQL 비교.
- 출제 의도: 데이터 요구사항이 복잡한 최신 웹/앱 환경에서 최적의 API 기술 선택 역량 평가.

## Ⅱ. 구성요소
- ASCII 구조도
  < REST >                          < GraphQL >
  [ /users ] -> [ Data A ]          [ /graphql ] -> { user { name, age } }
  [ /posts ] -> [ Data B ]                 |
                                    [ Schema (Query/Mutation) ]
- 구성요소 표
| 특성 | REST | GraphQL |
| :--- | :--- | :--- |
| 데이터 획득 | 서버가 정의한 고정 데이터 응답 | 클라이언트가 요청한 데이터만 응답 |
| 엔드포인트 | 리소스별 다수 엔드포인트 | 단일 엔드포인트 (/graphql) |
| 오버페칭 | 발생 가능성 높음 | 클라이언트가 제어하므로 없음 |
> 요약: REST는 서버 중심의 규격화, GraphQL은 클라이언트 중심의 유연성 강조함.

## Ⅲ. 절차
- ASCII 흐름도
  [Schema 정의] -> [Resolver 구현] -> [Query 요청] -> [JSON 결과 반환]
- 4단계 설명
1. 데이터 구조와 타입을 정의하는 강력한 타입 시스템(Schema) 구축함.
2. 각 필드의 데이터를 가져오는 구체적인 로직(Resolver)을 백엔드에 작성함.
3. 클라이언트는 필요한 필드만 계층 구조로 작성하여 서버에 요청함.
4. 서버는 요청된 필드만 모아서 단일 JSON 객체로 즉시 응답함.
> 요약: 한 번의 요청(Single Round-trip)으로 복잡한 데이터를 수집함.

## Ⅳ. 문제점
- GraphQL: 쿼리의 복잡도가 높을 경우 서버 부하 급증 및 캐싱 처리가 까다로움.
- REST: 모바일 환경에서 잦은 호출로 인한 배터리 소모 및 지연 시간 체감이 큼.

## Ⅴ. 개선방안
- Query Depth Limit: GraphQL 요청의 깊이를 제한하여 악의적인 복잡 쿼리 공격 방어함.
- 하이브리드 전략: 범용 외부 API는 REST, 사내 복잡한 앱 통신은 GraphQL로 이원화함.

## Ⅵ. 전망
- 'Federated GraphQL'을 통해 분산된 MSA 환경의 API를 하나로 통합하는 추세 강화됨.
- 실시간 데이터 구독(Subscription) 기능이 고도화되며 웹소켓 대체 사례 증대될 것임.
- AI가 최적의 쿼리를 생성하고 백엔드 리졸버를 자동 매핑하는 지능형 API 플랫폼 진화 예상됨.
