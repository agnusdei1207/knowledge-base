---
title: 프론트엔드 프레임워크 — React·Vue·Angular (Frontend Frameworks)
date: 2026-07-05
tags: ["cspe-software"]
weight: 170
---

## Ⅰ. 개요
- 정의: 사용자 인터페이스 구축을 위해 컴포넌트 기반 아키텍처와 도구를 제공하는 소프트웨어 환경
- 배경: 대규모 프론트엔드 프로젝트의 복잡도 관리 및 개발 효율성 증대 필요
| 구분 | 내용 |
|------|------|
| 출제 의도 | React(단방향), Vue(양방향), Angular(Full-stack)의 특성 비교 |

## Ⅱ. 구성요소
  [ State ] -> [ Component ] -> [ Virtual DOM ] -> [ Real DOM ]
  (Data-driven UI)
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Component | 재사용 가능한 UI 및 로직 단위 | 레고 블록 |
| Lifecycle | 생성, 갱신, 소멸의 단계별 훅 제공 | 성장 단계 |
| Props/State | parent input과 component 내부 data로 rendering 결과를 결정함 | data flow 기준 |
> 요약: frontend framework는 component tree와 state·props를 선언하고 변경 시 rendering·DOM update를 scheduling함

## Ⅲ. 절차
  Define View -> Bind Data -> Event Trigger -> Re-render
1. Design: 컴포넌트 계층 구조와 책임 분할 설계
2. Development: JSX/Template을 사용하여 뷰와 로직 구현
3. State Management: 전역/지역 상태 동기화 로직 구축
4. Deployment: build tool이 module graph를 bundle·split·minify하고 static asset을 배포함
> 요약: state 변경은 framework update를 예약하며 component identity·key·effect 규칙을 지켜야 UI와 side effect가 일치함

## Ⅳ. 문제점
- 프레임워크 버전 업데이트에 따른 파편화 및 마이그레이션 비용
- 과도한 자바스크립트 의존으로 인한 초기 로드 지연(Hydration 문제)

## Ⅴ. 개선방안
- 컴포넌트 단위 테스트 및 모듈화된 아키텍처(FSD 등) 도입
- Islands Architecture 또는 Server Components 도입으로 JS 최소화

## Ⅵ. 전망
- 프레임워크에 종속되지 않는 Web Components 표준 활용 및 AI 기반 UI 생성 도구와의 결합
