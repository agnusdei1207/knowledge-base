---
title: 빅데이터 및 NoSQL 아키텍처 (Big Data NoSQL)
date: 2026-07-05
tags: ["cspe-software"]
weight: 186
---

## Ⅰ. 개요
- 정의: 비정형/대용량 데이터를 처리하기 위해 수평적 확장성과 유연한 데이터 모델을 제공하는 아키텍처
- 배경: 전통적 RDBMS의 확장성 한계(Scale-up)와 데이터 다양성 대응
| 구분 | 내용 |
|------|------|
| 출제 의도 | Key-Value, Document, Column-family, Graph 모델의 특성 이해 |

## Ⅱ. 구성요소
  [ Dist. App ] <-> [ NoSQL Cluster ] <-> [ Sharded Nodes ]
  (BASE over ACID)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Sharding | 데이터를 여러 노드에 파티셔닝하여 분산 저장 | 구역 나누기 |
| Replication | 데이터를 여러 노드에 복제하여 장애 시 사본 제공 | 사본 비치 |
| Schema-less | 사전에 구조를 정의하지 않고 데이터 저장 | 자유 형식 |
> 요약: 분할·복제와 유연한 데이터 모델로 수평 확장하며 일관성 수준을 선택함

## Ⅲ. 절차
  Hash Key -> Locate Node -> Read/Write -> Propagate Rep
1. Key Mapping: 데이터 키를 해시하여 대상 노드 결정
2. Access: 해당 노드의 데이터 모델과 일관성 설정에 따라 읽기·쓰기 수행
3. Consistency: 설정에 따라 즉시 또는 최종 일관성 적용
4. Scale-out: 노드 추가 시 데이터 재분배(Rebalancing) 수행
> 요약: 키를 노드에 매핑하고 복제·재분배하여 읽기·쓰기 부하를 분산함

## Ⅳ. 문제점
- 복잡한 조인(Join) 연산 부재로 인한 애플리케이션 로직 복잡도 증가
- 데이터 중복 허용에 따른 일관성 관리의 어려움 및 무결성 취약

## Ⅴ. 개선방안
- 데이터 비정규화(Denormalization) 설계 및 CQRS 패턴 적용
- Quorum 기반 일관성 조절 및 하이브리드(Polyglot) 저장소 활용

## Ⅵ. 전망
- NewSQL(분산 SQL)의 부상으로 NoSQL의 확장성과 SQL의 일관성이 결합된 모델 확산
