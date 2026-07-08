---
title: "SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 35
extra:
  question_no: "035"
  exam_status: "기출"
  exam_history: "122회, 134회, 137회"
---

## 미리 알고가기

- SAFe는 여러 팀 단위 애자일을 프로그램과 포트폴리오 수준으로 확장하는 프레임워크임
- ART는 Agile Release Train으로 여러 팀이 같은 cadence로 움직이는 운영 단위임
- PI Planning은 팀 간 목표와 의존성을 맞추는 핵심 행사임

## Ⅰ. 개요

- **정의/개념**: SAFe는 다수의 애자일 팀을 Agile Release Train과 PI Planning과 포트폴리오 거버넌스로 묶어 대규모 조직에서도 일정한 cadence와 전략 정렬을 유지하게 하는 확장형 애자일 프레임워크임
- **배경/필요성**: 소수 팀 수준의 스크럼만으로는 대형 조직의 공통 아키텍처와 의존성과 예산 정렬을 감당하기 어려우므로, 팀 간 조정 계층이 필요함

## Ⅱ. 특징

- 여러 팀을 공통 주기와 목표로 묶어 대규모 동기화를 가능하게 함
- 팀 수준 애자일과 프로그램 및 포트폴리오 거버넌스를 함께 다룸
- 구조가 무거워지면 형식만 남고 민첩성이 떨어질 수 있음
- 의존성 관리와 전략 정렬이 필요한 대형 조직에서 효과가 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | 단일 팀 스크럼 | SAFe |
|:---|:---|:---|
| 적용 범위 | 개별 팀 중심 | 다수 팀과 프로그램, 포트폴리오 |
| 의존성 관리 | 제한적 | PI 단위로 체계화 |
| 거버넌스 | 가벼움 | 비교적 무거움 |
| 적합 환경 | 소규모 제품팀 | 대형 조직과 복합 프로그램 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Agile Release Train | 여러 팀을 하나의 가치 흐름 단위로 묶어 공통 cadence와 목표를 유지함 |
| PI Planning | 팀 간 목표와 의존성과 리스크를 같은 시점에 정렬하는 핵심 행사임 |
| Program Backlog | 기능 우선순위와 공통 아키텍처 요구를 프로그램 수준에서 통합함 |
| Portfolio Governance | 전략과 투자와 실행 흐름을 연결해 대규모 조직의 방향 일치를 유지함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 전략 정렬      | --> | PI 계획 수립   | --> | 팀별 실행      | --> | 통합 검토/개선 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **전략 정렬**: 포트폴리오 목표와 가치 흐름 우선순위를 정함
2. **PI 계획 수립**: 여러 팀이 같은 주기에서 목표와 의존성을 조정함
3. **팀별 실행**: 각 팀이 sprint를 통해 계획 항목을 구현함
4. **통합 검토 및 개선**: PI 결과와 리스크와 지표를 검토해 다음 주기를 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: SAFe 구조를 형식적으로만 도입하면 회의와 역할만 늘고 실제 의사결정 속도는 오히려 떨어질 수 있음
   - 해결방안: 가치 흐름 중심으로 최소 적용 범위를 설계하고 planning overhead ratio와 decision lead time으로 검증함
2. 문제: 팀 간 의존성이 backlog에 명확히 드러나지 않으면 PI 계획이 반복적으로 깨질 수 있음
   - 해결방안: dependency board와 architecture runway를 운영하고 dependency slip rate와 PI predictability로 검증함
3. 문제: 포트폴리오 목표와 팀 실행이 분리되면 대규모 조직일수록 현장 민첩성과 전략 정렬이 동시에 무너질 수 있음
   - 해결방안: portfolio sync와 objective tracing을 적용하고 strategic alignment score와 objective completion rate로 검증함

## Ⅶ. 적용 사례

- 대형 금융 IT 조직에서는 ART 단위 운영을 적용하고, PI predictability와 dependency slip rate로 결과를 확인함
- 공공 대규모 프로그램에서는 portfolio sync를 운영하고, strategic alignment score와 planning overhead ratio로 결과를 확인함
- 플랫폼과 서비스 다팀 환경에서는 architecture runway를 관리하고, objective completion rate와 decision lead time로 결과를 확인함

## Ⅷ. 결론

SAFe의 가치는 큰 조직에 애자일 용어를 붙이는 데 있지 않고 다수 팀의 의존성과 전략 정렬을 같은 cadence 위에 올려놓는 데 있음.
