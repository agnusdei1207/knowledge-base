---
title: "애자일 스크럼 (Agile Scrum)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 34
extra:
  question_no: "034"
  exam_status: "기출"
  exam_history: "121회, 134회"
---

## 미리 알고가기

- 스크럼은 짧은 스프린트 반복으로 제품을 점진 개발하는 애자일 프레임워크임
- Product Owner와 Scrum Master와 Development Team이 핵심 역할임
- backlog와 sprint goal과 review와 retrospective가 운영 핵심 요소임

## Ⅰ. 개요

- **정의/개념**: 스크럼은 우선순위가 있는 제품 backlog를 기반으로 짧은 sprint 단위로 목표를 설정하고, 개발과 검토와 회고를 반복해 제품 가치를 점진적으로 전달하는 애자일 프레임워크임
- **배경/필요성**: 요구 변화가 잦은 제품 개발에서는 sprint마다 increment를 검토하고 고객 피드백을 backlog 우선순위에 반영하는 운영 방식이 필요함

## Ⅱ. 특징

- 짧은 sprint로 계획과 실행과 피드백을 압축함
- 역할과 이벤트와 산출물이 비교적 명확해 팀 운영 틀을 제공함
- backlog 우선순위와 정의된 완료 기준이 약하면 효과가 급감함
- 속도보다 지속 가능한 예측 가능성과 팀 학습이 본질임

## Ⅲ. 종류 및 비교

| 판단 기준 | 전통 프로젝트 관리 | 스크럼 |
|:---|:---|:---|
| 계획 주기 | 장기 계획 중심 | 짧은 sprint 반복 |
| 요구 반영 | 변경 통제 중심 | backlog 재정렬 중심 |
| 팀 운영 | 역할 분리 강함 | 크로스펑셔널 협업 강조 |
| 성과 측정 | 일정 대비 진척 | increment 가치와 sprint 예측성 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Product Backlog | 제품 가치와 우선순위를 담는 단일 작업 목록으로 방향성과 집중도를 결정함 |
| Sprint Goal | 이번 sprint가 달성할 제품 목표를 정의해 backlog 항목 선택과 변경 판단의 기준이 됨 |
| Scrum Roles | Product Owner와 Scrum Master와 개발팀이 책임을 나눠 의사결정과 실행을 분리함 |
| Review and Retrospective | 결과 검증과 팀 개선을 분리 수행해 제품 학습과 프로세스 학습을 동시에 축적함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| backlog 정렬   | --> | sprint 계획   | --> | 구현/데일리 운영 | --> | review/회고    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **backlog 정렬**: 우선순위 높은 항목을 명확히 함
2. **sprint 계획**: sprint goal과 수행 범위를 정함
3. **구현 및 daily 운영**: 팀이 개발을 진행하고 장애를 조정함
4. **review 및 회고**: 결과를 검증하고 다음 sprint 개선점을 도출함

## Ⅵ. 실무 적용 및 유의점

1. SaaS나 제품팀에서 스크럼을 운영할 때는 backlog 품질이 sprint 성과를 좌우하므로 refinement와 수용 조건을 먼저 정비하고 backlog readiness와 sprint carryover rate와 cycle time으로 확인함
2. 데일리와 회고는 형식 행사로 두지 말고 장애와 개선 항목을 끝까지 추적해야 하므로 impediment 관리와 action item closure를 운영하고 blocker age와 retro action completion rate와 defect escape rate로 확인함

## Ⅶ. 결론

스크럼의 성공 여부는 이벤트를 지키는 형식보다 backlog 품질과 sprint 목표 일관성과 회고 실행력을 얼마나 유지하느냐에 달림.
