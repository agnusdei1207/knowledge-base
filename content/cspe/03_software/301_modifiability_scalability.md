---
title: 변경 용이성 및 확장성 설계 (Modifiability/Scalability)
date: 2026-07-05
tags: [cspe-software]
weight: 301
---

## Ⅰ. 개요
- 정의: 변경 용이성은 요구 변경의 영향 범위와 비용을 줄이는 특성이며, 확장성은 부하 증가에 맞춰 처리 자원을 늘리는 특성임
- 배경: 비즈니스 환경의 급격한 변화 및 사용자 트래픽의 가변성 증대 대응 필요
- 출제 의도: 유지보수 효율성 향상 및 시스템 용량 확장 전략(Scale-out) 설계 역량 평가

## Ⅱ. 구성요소
- ASCII 구조도
  [Modifiability] -> Encapsulation / Loose Coupling
  [Scalability]   -> Stateless / Distributed Processing
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| 캡슐화 | 내부 구현의 은닉을 통해 변경 전파 최소화 | 블랙박스 |
| 수평 확장 | 서버 대수를 늘려 처리 능력 향상(Scale-out) | 차선 확대 |
| 느슨한 결합 | 컴포넌트 간 의존성 최소화로 독립적 변경 보장 | 모듈형 가구 |
> 요약: 캡슐화·느슨한 결합으로 변경 전파를 줄이고 비상태성·수평 확장으로 처리 용량을 늘림

## Ⅲ. 절차
- ASCII 흐름도
  Change Point ID -> Modularity -> Resource Mgmt -> Monitoring
- 4단계 설명
1. Change Point ID: 향후 변경 가능성이 높은 비즈니스 로직과 기술 스택 식별함
2. Modularity: 인터페이스 기반 설계를 통해 결합도를 낮추고 응집도를 높임
3. Resource Mgmt: 상태 정보 제거(Stateless)를 통한 부하 분산 구조 설계함
4. Monitoring: 트래픽 임계치에 따른 자동 확장(Auto-scaling) 규칙 정의함
> 요약: 가변 영역을 모듈화하고 비상태성 설계를 통해 트래픽 부하에 대응함

## Ⅳ. 문제점
- 변경 가능성이 낮은 영역까지 추상화하면 인터페이스·계층·간접 호출이 늘어 구현과 분석 비용이 증가함

## Ⅴ. 개선방안
- 변경 이력과 확장 지표를 기준으로 가변 영역만 추상화하고 실제 부하 구간에 수평 확장을 적용함

## Ⅵ. 전망
- 마이크로서비스(MSA)와 서버리스 환경의 자동 최적화 확장 기술 진화
- CSF: 변경 영향 분석(Impact Analysis)의 자동화와 서비스 간 인터페이스 계약 관리가 핵심임
