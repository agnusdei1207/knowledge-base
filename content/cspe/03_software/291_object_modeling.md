---
title: 객체 모델링 — 클래스 다이어그램 (Object Modeling)
date: 2026-07-05
tags: [cspe-software]
weight: 291
---

## Ⅰ. 개요
- 정의: 시스템 내부의 정적 구조를 객체와 그들 간의 관계로 표현하는 UML 다이어그램임
- 배경: 객체지향 설계의 핵심 산출물로서 구현 단계의 클래스 구조 정의 필요
- 출제 의도: 정적 구조 설계 및 클래스 간 연관 관계(Relationship) 이해도 평가

## Ⅱ. 구성요소
- ASCII 구조도
  +----------------+        +----------------+
  |    Class A     |<>------|    Class B     |
  +----------------+        +----------------+
  | - attribute    |        | + operation()  |
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 클래스 | 속성(Attribute)과 연산(Operation)의 캡슐화 | 붕어빵 틀 |
| 연관(Association) | 클래스 인스턴스 간의 구조적 관계 | 친구 사이 |
| 상속/집약/합성 | 일반화, 전체-부분(Aggregation, Composition) 관계 | 가족/자동차 |
> 요약: 데이터와 행위를 결합한 클래스와 그들 사이의 다양한 연결 방식을 정의함

## Ⅲ. 절차
- ASCII 흐름도
  Entity ID -> Attribute/Method -> Relationship -> Refinement
- 4단계 설명
1. Entity ID: 도메인 분석을 통해 핵심 비즈니스 객체(Entity) 도출함
2. Attribute/Method: 각 클래스의 특성과 책임을 멤버 변수와 함수로 정의함
3. Relationship: 연관, 의존, 일반화, 실체화 등의 관계를 선언함
4. Refinement: 다중도(Multiplicity) 및 접근 제어자(Visibility) 등을 상세화함
> 요약: 대상 식별 후 속성/기능 부여 및 관계 설정을 통해 정적 모델을 완성함

## Ⅳ. 문제점
- 원인이 명시된 문제/한계: 복잡한 연관 관계로 인한 결합도 상승 및 유지보수성 저하 우려됨

## Ⅴ. 개선방안
- Ⅳ의 문제에 대응하는 방안: 디자인 패턴 적용 및 인터페이스를 통한 결합도 완화(DIP) 설계 지향함

## Ⅵ. 전망
- 발전 방향: MDA(Model Driven Architecture) 기반의 클래스 다이어그램-코드 자동 양방향 동기화 확대
- CSF: 응집도는 높이고 결합도는 낮추는(High Cohesion, Low Coupling) 기본 원칙 준수가 핵심임
