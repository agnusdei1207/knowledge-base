---
title: "클라우드 DB — RDS·Aurora·DynamoDB 비교 (Cloud Database)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 129
extra:
  question_no: "129"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- 클라우드 DB는 관리형 서비스로 제공되는 데이터베이스 계열임
- RDS와 Aurora와 DynamoDB는 데이터 모델과 운영 책임 경계가 다름
- 선택 기준은 엔진 유형보다 정합성·확장성·운영 자동화 요구에 있음

## Ⅰ. 개요

- **정의/개념**: 클라우드 DB는 백업과 패치와 장애 복구 같은 운영 기능을 서비스로 제공하면서 관계형과 분산 키값형 등 다양한 데이터 모델을 클라우드 환경에서 손쉽게 이용하게 하는 관리형 데이터베이스 서비스임
- **배경/필요성**: 데이터베이스 운영 자동화와 탄력 확장 수요가 커지면서 인프라 직접 운영보다 관리형 서비스로 전환해 개발 집중도를 높이려는 요구가 증가함

## Ⅱ. 특징

- 관리형 운영으로 백업과 패치와 모니터링 부담을 줄임
- Aurora는 관계형 호환성과 고가용성 분산 스토리지를 강화함
- DynamoDB는 서버리스형 확장성과 낮은 운영 부담에 강함
- 서비스별 일관성 모델과 비용 구조가 달라 단순 벤더 종속 비교로는 부족함

## Ⅲ. 종류 및 비교

| 판단 기준 | RDS | Aurora | DynamoDB |
|:---|:---|:---|:---|
| 데이터 모델 | 전통 관계형 엔진 | 관계형 호환 분산 스토리지 | key-value·document |
| 강점 | 익숙한 운영 모델 | 고가용성과 읽기 확장 | 서버리스 확장과 낮은 운영 부담 |
| 한계 | 확장성과 장애 설계 한계 | 비용과 기능 이해 필요 | 조인과 복합 질의 제약 |
| 적합 업무 | 일반 OLTP | 고가용성 관계형 서비스 | 대규모 분산 API 트래픽 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Managed Control Plane | 백업과 패치와 모니터링 자동화를 제공해 운영 부담을 줄임 |
| Storage and Replication Model | 서비스별 저장 구조와 복제 방식이 성능과 복구 특성을 결정함 |
| Scaling Policy | 읽기 확장과 자동 조정과 파티셔닝 방식이 처리량 한계를 좌우함 |
| Consistency and Access Model | SQL 지원 범위와 정합성 옵션이 애플리케이션 구조를 바꿈 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 업무 요구 분석   | --> | 서비스 유형 선택 | --> | 확장/복제 설계  | --> | 비용/성능 검증  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **업무 요구 분석**: 정합성과 질의 복잡도와 처리량을 확인함
2. **서비스 유형 선택**: RDS와 Aurora와 DynamoDB를 비교함
3. **확장과 복제 설계**: 읽기 확장과 백업과 장애 복구를 구성함
4. **비용과 성능 검증**: 사용량과 지연과 운영 부담을 측정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 관계형 질의를 많이 쓰는 업무를 단순 확장성만 보고 key-value형으로 옮기면 애플리케이션 복잡도와 보정 비용이 급증할 수 있음
   - 해결방안: query compatibility review를 수행하고 application rewrite rate와 workload fit score로 검증함
2. 문제: 관리형 서비스라 해도 일관성 모델과 장애 전환 특성을 모르면 운영 중 예상치 못한 stale read와 failover 지연을 겪을 수 있음
   - 해결방안: service-specific drill을 운영하고 failover recovery time와 stale read incident count로 검증함
3. 문제: 자동 확장을 과신하고 비용 가드레일을 두지 않으면 트래픽 급증 시 운영비가 예산을 빠르게 초과할 수 있음
   - 해결방안: cost governance와 scaling limit policy를 적용하고 cost per request와 budget breach frequency로 검증함

## Ⅶ. 적용 사례

- 신규 SaaS 제품에서는 질의 호환성을 검토하고, application rewrite rate와 workload fit score로 결과를 확인함
- 고가용성 관계형 서비스에서는 서비스별 장애 훈련을 운영하고, failover recovery time와 stale read incident count로 결과를 확인함
- 트래픽 변동이 큰 API 플랫폼에서는 비용 가드레일을 적용하고, cost per request와 budget breach frequency로 결과를 확인함

## Ⅷ. 결론

클라우드 DB 선택은 관리형 여부만 보는 판단이 아니라 데이터 모델과 일관성 특성과 비용 구조를 서비스 요구에 맞게 맞추는 작업임.
