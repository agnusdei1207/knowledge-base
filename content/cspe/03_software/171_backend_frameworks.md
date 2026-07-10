---
title: 백엔드 프레임워크 — Spring·Django·Node.js (Backend Frameworks)
date: 2026-07-05
tags: ["cspe-software"]
weight: 171
---

## Ⅰ. 개요
- 정의: 서버 측 로직, 데이터베이스 상호작용 및 API 제공을 위한 소프트웨어 구조
- 배경: 비즈니스 로직의 계층별 분리와 서버 확장 구조 확보
| 구분 | 내용 |
|------|------|
| 출제 의도 | Spring(DI/AOP), Django(MTV), Node.js(Event-driven)의 핵심 설계 철학 이해 |

## Ⅱ. 구성요소
  [ Request ] -> [ Controller ] -> [ Service ] -> [ DB/Model ]
  (Layered Architecture)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| DI/IoC | 객체 생성과 의존 관계를 외부에서 관리하여 결합도 완화 | 부품 조립 |
| ORM | 객체와 관계형 DB의 매핑 지원 | 번역기 |
| Middleware | 요청과 응답 사이의 공통 처리(인증, 로깅) | 검문소 |
> 요약: 요청 처리 계층과 의존 관계를 분리하여 변경 범위와 확장 단위를 관리함

## Ⅲ. 절차
  Receive -> Route -> Process Logic -> Data Sync -> Respond
1. Routing: 들어온 HTTP 요청을 적절한 핸들러로 전달
2. Authentication: 사용자 권한 확인 및 보안 검사
3. Service Logic: 핵심 비즈니스 연산 및 트랜잭션 수행
4. Data Persistence: 데이터베이스 결과 반영 및 응답 생성
> 요약: 요청을 라우팅하고 인증·업무 로직·트랜잭션을 거쳐 응답을 생성함

## Ⅳ. 문제점
- 대규모 트래픽 발생 시 특정 계층의 병목 현상 및 확장 한계
- 모놀리식 구조에서의 복잡도 증가 및 배포 독립성 결여

## Ⅴ. 개선방안
- 마이크로서비스 아키텍처(MSA) 전환 및 컨테이너화(Docker)
- 서킷 브레이커 도입 및 비동기 메시지 큐(Kafka) 활용

## Ⅵ. 전망
- 서버리스(Serverless) 및 클라우드 네이티브 프레임워크(Quarkus 등)로의 전환 가속화
