---
title: "GraphQL (Graph Query Language)"
date: "2026-06-30"
weight: 71
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 클라이언트가 필요한 데이터의 구조를 직접 질의하여 단일 엔드포인트에서 정확히 받아오는 API 질의 언어 및 런타임으로, 페이스북이 개발했다.

## Ⅱ. 구성요소 / 원리
- 단일 엔드포인트: 하나의 URL로 모든 질의 처리
- 쿼리(Query)/뮤테이션(Mutation)/구독(Subscription): 조회·변경·실시간 푸시
- 스키마(Schema)·타입 시스템: 강타입 계약으로 데이터 구조 정의
- 리졸버(Resolver): 각 필드를 실제 데이터 소스에 매핑
- 오버페칭·언더페칭 해결: 필요한 필드만 선택 조회

## Ⅲ. 흐름도 / 구조
```text
 Client                      Server
   query{ user{name,posts} }  -->
                              Resolver
   <-- { user:{name,posts} }  단일응답
   (필요 필드만, 단일 엔드포인트)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 클라이언트 주도 정밀 데이터 조회 |
| 장점 | 오버/언더페칭 제거, 단일 요청 다중 자원 |
| 한계 | 캐싱 복잡, 복잡 쿼리 시 서버 부하·N+1 문제 |

## Ⅴ. 기술사적 적용
- REST 대비 모바일 등 가변 클라이언트 요구에 유연 대응
- 스키마 기반 프론트·백엔드 병행 개발, BFF(Backend For Frontend) 패턴 적용
- 쿼리 복잡도 제한·persisted query로 보안·성능 보완
