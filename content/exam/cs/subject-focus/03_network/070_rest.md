---
title: "REST (Representational State Transfer)"
date: "2026-06-30"
weight: 70
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 자원(Resource)을 URI로 식별하고 HTTP 메서드로 그 표현(Representation)을 주고받는 무상태 분산 아키텍처 스타일로, 웹의 확장성 원칙을 따른다.

## Ⅱ. 구성요소 / 원리
- 자원·URI: 모든 대상을 URI(Uniform Resource Identifier)로 유일 식별
- HTTP 메서드: GET/POST/PUT/DELETE로 CRUD 행위 표현
- 무상태(Stateless): 서버가 클라이언트 상태 미보관, 요청 자체 완결
- 균일 인터페이스(Uniform Interface): 일관된 자원 접근 규약
- HATEOAS(Hypermedia As The Engine Of Application State): 응답에 다음 행위 링크 포함

## Ⅲ. 흐름도 / 구조
```text
 Client --GET /users/1-----------> Server
        <--200 {id,name, _links}---
   메서드(행위) + URI(자원) + 표현(JSON)
   무상태: 매 요청 자기완결적
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 단순·확장 가능한 웹 친화적 API 설계 |
| 장점 | 캐싱·확장성 우수, HTTP 표준 그대로 활용 |
| 한계 | 오버/언더페칭, 다중 자원 조회 시 다중 호출 필요 |

## Ⅴ. 기술사적 적용
- 리처드슨 성숙도 모델(Level 0~3, 3이 HATEOAS) 기준 설계 평가
- GraphQL·gRPC와 비교하여 공개 API에 REST 채택이 보편적
- 캐시·로드밸런싱 등 웹 인프라와 자연스럽게 연계
