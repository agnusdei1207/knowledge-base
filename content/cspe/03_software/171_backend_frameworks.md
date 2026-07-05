---
title: 백엔드 프레임워크 — Spring·Django·Node.js (Backend Frameworks)
date: 2026-07-05
tags: ["cspe-software"]
weight: 171
---

## Ⅰ. 개요
- 정의: 서버 측 로직, 데이터베이스 상호작용 및 API 제공을 위한 소프트웨어 구조
- 배경: 비즈니스 로직의 안정적 처리 및 분산 환경에서의 확장성 확보
| 구분 | 내용 |
|------|------|
| 출제 의도 | Spring(DI/AOP), Django(MTV), Node.js(Event-driven)의 핵심 설계 철학 이해 |

## Ⅱ. 구성요소
  [ Request ] -> [ Controller ] -> [ Service ] -> [ DB/Model ]
  (Layered Architecture)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| DI/IoC | 의존성 주입을 통한 결합도 낮추기 | 부품 조립 |
| ORM | 객체와 관계형 DB의 매핑 지원 | 번역기 |
| Middleware | 요청과 응답 사이의 공통 처리(인증, 로깅) | 검문소 |
> 요약: 관심사 분리를 통한 유지보수성과 확장성이 뛰어난 서버 시스템 구축

## Ⅲ. 절차
  Receive -> Route -> Process Logic -> Data Sync -> Respond
1. Routing: 들어온 HTTP 요청을 적절한 핸들러로 전달
2. Authentication: 사용자 권한 확인 및 보안 검사
3. Service Logic: 핵심 비즈니스 연산 및 트랜잭션 수행
4. Data Persistence: 데이터베이스 결과 반영 및 응답 생성
> 요약: 요청부터 응답까지의 흐름 제어 및 데이터 무결성 보장

## Ⅳ. 문제점
- 대규모 트래픽 발생 시 특정 계층의 병목 현상 및 확장 한계
- 모놀리식 구조에서의 복잡도 증가 및 배포 독립성 결여

## Ⅴ. 개선방안
- 마이크로서비스 아키텍처(MSA) 전환 및 컨테이너화(Docker)
- 서킷 브레이커 도입 및 비동기 메시지 큐(Kafka) 활용

## Ⅵ. 전망
- 서버리스(Serverless) 및 클라우드 네이티브 프레임워크(Quarkus 등)로의 전환 가속화
