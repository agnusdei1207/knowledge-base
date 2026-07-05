---
title: 마이크로서비스 아키텍처 설계 (MSA Design)
date: 2026-07-05
tags: [cspe-software]
weight: 311
---

## Ⅰ. 개요
- 정의: 대규모 애플리케이션을 작고 독립적인 서비스 단위로 분할하여 구축하는 방식임
- 배경: 모놀리식 구조의 복잡성 한계 극복 및 빠른 배포와 부분적 확장 필요성 증대
- 출제 의도: 서비스 분할 원칙(Bounded Context) 및 서비스 간 통신 설계 역량 평가

## Ⅱ. 구성요소
- ASCII 구조도
  [Client] -> [API Gateway] -> [Svc A] [Svc B] [Svc C]
                                 |       |       |
                            [DB A]  [DB B]  [DB C]
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| API Gateway | 모든 클라이언트 요청의 단일 진입점 및 라우팅 | 안내 데스크 |
| DB per Service | 서비스별로 전용 데이터베이스를 보유함 | 개별 금고 |
| 서비스 메쉬 | 서비스 간 통신 관리를 위한 전용 인프라 계층 | 우체국망 |
> 요약: 독립적 배포와 확장이 가능하도록 기능을 분리하고 API를 통해 협력함

## Ⅲ. 절차
- ASCII 흐름도
  Domain Decomp -> Interface Def -> Data Decouple -> Infrastructure
- 4단계 설명
1. Domain Decomp: DDD(Domain Driven Design)를 활용하여 서비스 경계 확정함
2. Interface Def: REST, gRPC 등 서비스 간 통신 방식 및 규약 정의함
3. Data Decouple: 서비스 간 공유 DB 제거 및 데이터 동기화(Saga 패턴) 설계함
4. Infrastructure: 컨테이너(Docker), 오케스트레이션(K8s), CI/CD 환경 구축함
> 요약: 비즈니스 경계에 따라 서비스를 나누고 독립 데이터와 통신망을 구축함

## Ⅳ. 문제점
- 원인이 명시된 문제/한계: 서비스 간 분산 트랜잭션 관리 및 통합 테스팅의 복잡도 급증함

## Ⅴ. 개선방안
- Ⅳ의 문제에 대응하는 방안: 이벤트 기반의 최종 일관성(Eventual Consistency) 확보 및 관측성 강화함

## Ⅵ. 전망
- 발전 방향: 서버리스와 결합된 극도로 세분화된 나노서비스(Nanoservices)로의 진화
- CSF: 기술적 도입보다 조직의 역량과 문화(Conway's Law)의 변화가 선행되어야 함
