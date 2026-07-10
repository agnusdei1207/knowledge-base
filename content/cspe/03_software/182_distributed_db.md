---
title: 분산 데이터베이스 관리 (Distributed DB)
date: 2026-07-05
tags: ["cspe-software"]
weight: 182
---

## Ⅰ. 개요
- 정의: 물리적으로 분산된 여러 사이트의 DB를 통신망으로 연결하여 하나의 DB처럼 사용하는 시스템
- 배경: 데이터 가용성 증대, 지역적 부하 분산 및 대규모 확장성 확보
| 구분 | 내용 |
|------|------|
| 출제 의도 | 투명성(위치, 복제, 분할, 장애) 및 CAP 이론(일관성, 가용성, 분산 허용) 이해 |

## Ⅱ. 구성요소
  [ Node A ] <---(Network)---> [ Node B ]
       |                            |
  [ Storage ]                  [ Storage ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Fragmentation | 테이블을 작은 단위로 나누어 분산 저장 | 피자 조각 |
| Replication | 동일 데이터를 여러 노드에 복제하여 저장 | 예비 부품 |
| Transparency | 분산 사실을 몰라도 접근 가능하게 하는 성질 | 유리창 |
> 요약: 데이터를 분할·복제하고 분산 위치를 은닉하여 확장성과 가용성을 확보함

## Ⅲ. 절차
  Request -> Catalog Lookup -> Distributed Query -> Join Result
1. Mapping: 데이터가 어느 노드에 있는지 카탈로그에서 확인
2. Sub-query: 각 노드에서 지역적 질의 수행 및 결과 추출
3. Transfer: 추출된 데이터를 통신망을 통해 취합 노드로 전송
4. Assembly: 수신된 데이터를 최종 병합하여 사용자에게 반환
> 요약: 카탈로그로 데이터 위치를 확인하고 노드별 질의 결과를 전송·병합함

## Ⅳ. 문제점
- 네트워크 지연 및 장애 시 데이터 일관성(Consistency) 유지 비용
- 분산 트랜잭션 관리(2PC 등)에 따른 복잡도 및 성능 저하

## Ⅴ. 개선방안
- BASE(Basically Available, Soft-state, Eventual Consistency) 모델 수용
- 로컬리티(Locality)를 고려한 데이터 배치 및 캐싱 강화

## Ⅵ. 전망
- 멀티 클라우드 환경의 글로벌 데이터 분산 서비스 및 엣지 컴퓨팅 기반 DB 연동 확산
