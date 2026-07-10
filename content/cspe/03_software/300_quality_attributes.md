---
title: 소프트웨어 아키텍처 품질 속성 (Quality Attributes)
date: 2026-07-05
tags: [cspe-software]
weight: 300
---

## Ⅰ. 개요
- 정의: 시스템이 비즈니스 목표를 달성하기 위해 갖추어야 할 비기능적 특성임
- 배경: 기능 구현만으로는 복잡한 비즈니스 환경과 사용자 요구 만족 불가능
- 출제 의도: 품질 속성 분류 및 각 속성의 아키텍처적 영향력 이해도 검증

## Ⅱ. 구성요소
- ASCII 구조도
  [Quality Attributes]
   |-- Runtime (Availability, Performance, Security)
   |-- Development (Modifiability, Testability)
   |-- Business (Time to Market, Cost)
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 가시적 품질 | 사용자나 운영자가 체감하는 런타임 품질 | 승차감 |
| 불가시적 품질 | 개발자나 유지보수자가 체감하는 설계 품질 | 정비 용이성 |
| 유틸리티 트리 | 품질 속성을 구체화하여 우선순위를 매긴 나무 | 성적표 |
> 요약: 런타임·개발·비즈니스 품질을 시나리오와 응답 측정값으로 정의하여 설계 판단 기준으로 사용함

## Ⅲ. 절차
- ASCII 흐름도
  Identification -> Scenario Design -> Prioritization -> Evaluation
- 4단계 설명
1. Identification: 이해관계자 인터뷰를 통해 핵심 비기능 요구사항 도출함
2. Scenario Design: (자극원, 자극, 환경, 대상, 응답, 응답측정) 6요소로 기술함
3. Prioritization: 비즈니스 가치와 기술적 난이도를 기준으로 우선순위 부여함
4. Evaluation: 아키텍처 설계안이 각 품질 시나리오를 만족하는지 검증함
> 요약: 이해관계자 의견을 수렴하여 시나리오화하고 우선순위에 따라 관리함

## Ⅳ. 문제점
- 품질 속성 간 우선순위와 상충 관계를 정하지 않으면 서로 다른 설계 목표를 동시에 요구하게 됨

## Ⅴ. 개선방안
- 품질 시나리오별 중요도·위험도·응답 측정값을 비교하고 절충 결정과 근거를 ADR로 관리함

## Ⅵ. 전망
- 탄소 배출 저감(Sustainability) 등 ESG 경영을 반영한 신규 품질 속성 대두
- CSF: 정량화 가능한 품질 측정 지표(Metric) 설정과 지속적인 모니터링 체계 구축이 관건임
