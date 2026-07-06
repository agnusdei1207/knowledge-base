---
title: NoSQL — Key-Value·Document·Graph (NoSQL)
date: 2026-07-05
tags: [cspe-software]
weight: 67
---

## Ⅰ. 개요
- 고정된 스키마 없이 분산 환경에서 대용량 데이터를 처리하기 위한 비관계형 DB임.
- CAP 이론(Consistency, Availability, Partition Tolerance)에 따라 설계됨.
- 출제 의도: 데이터 유형별 적합한 NoSQL 모델 선택 및 분산 처리 메커니즘 이해.

## Ⅱ. 구성요소
- NoSQL 모델 분류
[Key-Value] | [Document] | [Column-Family] | [Graph]

| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Key-Value | 키와 값의 쌍으로 저장 (Redis 등) | 사물함 |
| Document | JSON/BSON 형태 저장 (MongoDB 등) | 서류 폴더 |
| Graph | 노드와 간선으로 관계 저장 (Neo4j 등) | 소셜 네트워크 |
> 요약: 데이터 특성에 최적화된 다양한 비정형 저장 구조를 제공함.

## Ⅲ. 절차
- NoSQL 데이터 접근 과정
[App] -> [Consistent Hashing] -> [Node Search] -> [Result]

1. 샤드 키 생성: 데이터 분산을 위한 해시 기반 키를 생성함.
2. 노드 매핑: 컨시스턴트 해싱을 통해 저장될 물리 노드 결정함.
3. 데이터 복제: 고가용성을 위해 설정된 복제 계수만큼 복제본 생성함.
4. 최종 일관성(Eventual Consistency): 시간 경과 후 전체 노드 동기화함.
> 요약: 분산 노드에 데이터를 배치하고 비동기 복제로 가용성 극대화함.

## Ⅳ. 문제점
- 데이터 중복에 따른 일관성 결여 가능성 및 복잡한 조인 연산 수행의 어려움.

## Ⅴ. 개선방안
- BASE(Basically Available, Soft state, Eventual consistency) 전략 채택 및 하이브리드 구성.

## Ⅵ. 전망
- AI/ML용 벡터 DB(Vector DB)로의 확장 및 멀티 모델(Multi-model) NoSQL 시장 확대.
- 실시간 실시간 스트리밍 처리와 결합된 통합 데이터 플랫폼으로 진화할 것임.
