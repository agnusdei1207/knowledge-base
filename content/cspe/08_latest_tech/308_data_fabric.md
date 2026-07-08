---
title: "Data Fabric 데이터 패브릭 (Data Fabric)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 308
extra:
  question_no: "308"
  exam_status: "기출"
  exam_history: "135회, 136회"
  exam_note: "전망"
---

## 미리 알고가기

- Data Fabric은 분산된 데이터 자산을 메타데이터와 자동화로 연결해 통합 활용하게 하는 아키텍처 접근임
- 저장소를 하나로 모으는 개념보다 다양한 저장소 위에 통합 계층을 두는 개념에 가까움
- 활성 메타데이터와 지식 그래프와 정책 자동화가 핵심 구현 요소로 자주 언급됨

## Ⅰ. 개요

- **정의/개념**: Data Fabric은 온프레미스와 클라우드와 애플리케이션에 흩어진 데이터를 메타데이터 기반 연결과 자동화된 통합과 정책 집행으로 묶어 사용자가 위치와 형식 차이를 크게 의식하지 않고 활용하게 하는 데이터 통합 아키텍처임
- **배경/필요성**: 멀티클라우드와 SaaS 확산으로 데이터가 여러 저장소와 업무 시스템에 흩어지면서 수작업 ETL만으로는 통합 속도와 거버넌스와 변경 대응을 감당하기 어려워짐

## Ⅱ. 특징

- 활성 메타데이터를 중심으로 연결 관계와 정책과 품질 상태를 지속 반영함
- 물리적 이동과 가상 조회를 혼합해 상황에 맞는 통합 방식을 선택할 수 있음
- 자동 추천과 정책 적용으로 데이터 통합 운영 부담을 줄이는 방향을 지향함
- 메타데이터 품질이 낮으면 자동화 정확도와 신뢰도가 동시에 떨어지는 구조적 특성이 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Fabric | Data Mesh | Traditional ETL Hub |
|:---|:---|:---|:---|
| 핵심 축 | 메타데이터 기반 연결과 자동화 | 도메인 분산 소유 | 중앙 적재 중심 |
| 주요 과제 | 메타데이터 정확성 | 조직 책임 재설계 | 배치 파이프라인 확장성 |
| 통합 방식 | 물리와 가상 혼합 | 제품 공유 중심 | 물리 복제 중심 |
| 대표 장점 | 빠른 연결성과 정책 자동화 | 현업 밀착 운영 | 관리 단순성 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Active Metadata Layer | 데이터 위치와 스키마와 품질과 사용 이력을 수집해 통합 판단과 자동화의 기준이 되는 지식 기반 계층임 |
| Knowledge Graph and Semantic Mapping | 서로 다른 시스템의 데이터 관계와 의미를 연결해 통합 검색과 영향 분석과 추천 정확도를 높이는 의미 연결 계층임 |
| Integration and Delivery Services | 가상화와 복제와 스트리밍과 API 연계를 조합해 실제 데이터 접근 경로를 제공하는 실행 계층임 |
| Policy and Governance Engine | 접근 제어와 개인정보 규칙과 품질 기준을 메타데이터 기반으로 자동 집행해 분산 환경에서도 일관성을 유지하는 통제 계층임 |
| Observability and Automation Loop | 사용 패턴과 품질 이벤트를 감시하고 최적화 작업을 추천해 데이터 운영을 계속 개선하는 피드백 계층임 |

```text
+------------------+
| Active Metadata  |
+------------------+
          |
          v
+------------------+
| Semantic Graph   |
+------------------+
          |
          v
+------------------+
| Integration Svcs |
+------------------+
          |
          v
+------------------+
| Consumer / Policy|
+------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 메타 수집     | -> | 관계 분석     | -> | 정책/경로 결정 | -> | 데이터 제공   | -> | 관측/자동개선  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **메타 수집**: 다양한 저장소와 애플리케이션에서 기술 메타데이터와 운영 메타데이터를 수집함
2. **관계 분석**: 의미와 흐름과 품질 관계를 그래프로 연결함
3. **정책과 경로 결정**: 요청 목적에 맞는 접근 정책과 통합 방식을 선택함
4. **데이터 제공**: 가상 조회나 복제나 스트리밍 방식으로 데이터를 전달함
5. **관측과 자동 개선**: 품질과 성능과 사용성 정보를 반영해 규칙과 경로를 계속 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 메타데이터 수집 범위와 품질이 부족하면 자동 추천과 정책 집행이 왜곡되어 Data Fabric의 핵심 가치가 약해질 수 있음
   - 해결방안: metadata harvesting baseline과 stewardship workflow를 적용하고 metadata freshness score와 classified asset coverage로 검증함
2. 문제: 자동화 로직이 복잡해질수록 사용자 입장에서 데이터 제공 경로와 정책 결정 근거가 불투명해질 수 있음
   - 해결방안: explainable automation view와 policy traceability log를 적용하고 user trust score와 unresolved policy explanation request count로 검증함
3. 문제: 통합 계층이 지나치게 광범위해지면 도입 범위와 비용이 커져 핵심 업무보다 플랫폼 구축 자체가 목적화될 수 있음
   - 해결방안: use case driven rollout과 value stream prioritization을 적용하고 time to first governed use case와 platform cost to adoption ratio로 검증함

## Ⅶ. 적용 사례

- 메타데이터 플랫폼이 자산 수집 기준을 운영하며 확인 지표는 metadata freshness score와 classified asset coverage임
- 데이터 서비스 포털이 정책 추적 로그를 제공하며 확인 지표는 user trust score와 unresolved policy explanation request count임
- 멀티클라우드 데이터 통합 사업이 단계적 도입을 적용하며 확인 지표는 time to first governed use case와 platform cost to adoption ratio임

## Ⅷ. 결론

Data Fabric은 데이터를 한곳에 모으는 기술이 아니라 메타데이터를 중심으로 흩어진 자산을 연결하는 운영 체계이므로 자동화의 정확도를 좌우하는 메타데이터 품질 관리가 핵심임.
