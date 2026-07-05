---
title: 소프트웨어 복잡도 및 유지보수성 (Complexity and Maintainability)
date: 2026-07-05
tags: ["cspe-software"]
weight: 192
---

## Ⅰ. 개요
- 정의: 코드의 구조적 난해함 정도(복잡도)와 시스템을 수정/개선하기 쉬운 정도(유지보수성)
- 배경: 장기적 운영 비용(TCO) 절감 및 기술 부채 관리 필요성 증대
| 구분 | 내용 |
|------|------|
| 출제 의도 | 순환 복잡도(Cyclomatic Complexity) 계산 및 클린 코드 원칙 이해 |

## Ⅱ. 구성요소
  V(G) = E - N + 2P
  (Complexity Metrics based on Control Flow Graph)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Cyclomatic | 제어 흐름 경로의 수를 측정하는 지표 | 길 찾기 난이도 |
| Halstead | 연산자와 피연산자의 수 기반 복잡도 | 단어 수 합계 |
| Cohesion/Coupling | 응집도(높게)와 결합도(낮게) 관리 지표 | 부품의 독립성 |
> 요약: 정량적 지표를 통한 코드의 위험성 진단 및 품질 관리

## Ⅲ. 절차
  Analyze Code -> Calculate Metric -> Identify Hotspot -> Refactor
1. Static Analysis: 도구(SonarQube 등)를 통한 코드 구조 스캔
2. Metric Calculation: 함수별 복잡도 점수 산출 및 임계치 대조
3. Selection: 복잡도가 높은 위험 모듈(Hotspot) 우선순위 선정
4. Refactoring: 로직 분할, 추상화 강화 등을 통해 코드 정돈
> 요약: 복잡도 완화를 통한 잠재 결함 감소 및 변경 용이성 확보

## Ⅳ. 문제점
- 복잡도 지표가 성능이나 비즈니스 가치를 완벽히 대변하지 못함
- 유지보수성 고려 없는 빠른 개발(Quick-and-Dirty)로 인한 기술 부채 누적

## Ⅴ. 개선방안
- 코드 리뷰 문화 정착 및 정적 분석 도구의 CI/CD 파이프라인 강제화
- 디자인 패턴 적용 및 도메인 주도 설계(DDD)를 통한 경계 명확화

## Ⅵ. 전망
- AI 기반의 코드 리팩토링 제안 및 복잡도 예측 모델을 통한 선제적 품질 관리 보편화
