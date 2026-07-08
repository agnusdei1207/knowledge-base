---
title: "Cloud Migration 6R (Cloud Migration 6R)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 287
extra:
  question_no: "287"
  exam_status: "기출"
  exam_history: "121회, 138회"
---

## 미리 알고가기

- Cloud Migration 6R은 애플리케이션을 클라우드로 옮길 때 선택할 전환 전략 분류 체계임
- 대표 항목은 Rehost, Replatform, Refactor, Repurchase, Retire, Retain임
- 기술 이전 방식이 아니라 업무 가치와 비용과 위험을 함께 보는 포트폴리오 판단 기준으로 이해해야 함

## Ⅰ. 개요

- **정의/개념**: Cloud Migration 6R은 기존 애플리케이션과 시스템을 클라우드로 이전할 때 대상별로 가장 적절한 전환 전략을 여섯 가지 유형으로 분류해 의사결정을 체계화하는 프레임워크임
- **배경/필요성**: 모든 시스템을 같은 방식으로 이전하면 비용과 일정과 리스크가 폭증하므로 업무 중요도와 기술 부채와 현대화 필요성에 맞춘 전략 구분이 필요해짐

## Ⅱ. 특징

- 시스템별로 다른 이전 방식을 선택하게 해 포트폴리오 최적화를 가능하게 함
- 단기 이전과 장기 현대화 전략을 동시에 설계할 수 있음
- 기술 난이도와 비즈니스 가치와 일정 압박을 함께 반영함
- 잘못 분류하면 과투자나 가치 없는 현대화가 발생할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Rehost | Replatform | Refactor |
|:---|:---|:---|:---|
| 변화 수준 | 낮음 | 중간 | 높음 |
| 이전 속도 | 빠름 | 중간 | 느림 |
| 클라우드 최적화 | 낮음 | 중간 | 높음 |
| 적합 상황 | 빠른 이전 필요 | 일부 개선 필요 | 전략적 현대화 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Application Inventory | 이전 대상 시스템의 기술 상태와 비용과 업무 중요도를 정리해 6R 분류의 입력이 되는 목록임 |
| Assessment Criteria | 기술 부채와 상호의존성과 규제 요구와 사업 가치 같은 판단 기준을 제공하는 평가 축임 |
| 6R Strategy Map | Rehost부터 Retire까지 각 애플리케이션의 이전 방향을 분류해 포트폴리오 로드맵을 만드는 분류 체계임 |
| Migration Wave Plan | 우선순위와 의존성을 고려해 이전 순서와 묶음을 설계하는 실행 계획 계층임 |
| Validation and Cutover | 성능과 보안과 데이터 일관성을 검증한 뒤 실제 전환을 수행하는 마이그레이션 마감 계층임 |

```text
+--------------+    +----------------+    +---------------+    +----------------+
| Inventory    | -> | Assessment     | -> | 6R Decision   | -> | Migration Wave |
+--------------+    +----------------+    +---------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 자산 식별    | -> | 기준 평가    | -> | 6R 분류      | -> | 전환 계획    | -> | 검증과 전환   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **자산 식별**: 이전 대상 애플리케이션과 의존성을 파악함
2. **기준 평가**: 기술과 비용과 업무 중요도를 평가함
3. **6R 분류**: 적절한 이전 전략을 선택함
4. **전환 계획**: 파장과 순서를 설계함
5. **검증과 전환**: 테스트 후 실제 서비스를 전환함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 기술적 난이도만 보고 6R을 정하면 업무 가치와 규제 요구를 반영하지 못해 잘못된 전략 선택이 생길 수 있음
   - 해결방안: business and risk weighted assessment를 적용하고 strategy reclassification rate와 business fit score로 검증함
2. 문제: 의존 시스템 분석이 부족하면 마이그레이션 파장이 과소평가되어 일정 지연과 장애가 발생할 수 있음
   - 해결방안: dependency mapping과 wave based cutover planning을 적용하고 dependency miss count와 cutover incident rate로 검증함
3. 문제: Refactor가 필요한 시스템까지 단기 Rehost로 몰아가면 클라우드 이전 후 운영 비용과 기술 부채가 더 커질 수 있음
   - 해결방안: post migration modernization backlog와 TCO tracking을 적용하고 cloud cost uplift ratio와 technical debt carryover score로 검증함

## Ⅶ. 적용 사례

- 엔터프라이즈 전환 프로젝트가 가치 가중 평가를 수행하며 확인 지표는 strategy reclassification rate와 business fit score임
- 대규모 레거시 이전이 의존성 기반 파장 계획을 적용하며 확인 지표는 dependency miss count와 cutover incident rate임
- 클라우드 이전 프로그램이 현대화 백로그를 관리하며 확인 지표는 cloud cost uplift ratio와 technical debt carryover score임

## Ⅷ. 결론

Cloud Migration 6R은 기술 이전 방식보다 포트폴리오 전략 판단 도구이므로 가치와 위험과 장기 운영비용을 함께 보고 분류해야 함.
