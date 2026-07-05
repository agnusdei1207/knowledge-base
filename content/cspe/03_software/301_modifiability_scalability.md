---
title: 변경 용이성 및 확장성 설계 (Modifiability/Scalability)
date: 2026-07-05
tags: [cspe-software]
weight: 301
---

## Ⅰ. 개요
- 정의: 요구사항 변경 시 낮은 비용으로 대응하고, 부하 증가 시 유연하게 자원을 확장함
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
> 요약: 변경에 강한 구조(추상화)와 확장에 유연한 구조(분산)를 동시에 확보함

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
- 원인이 명시된 문제/한계: 과도한 추상화 설계 시 초기 개발 복잡도 상승 및 성능 오버헤드 발생함

## Ⅴ. 개선방안
- Ⅳ의 문제에 대응하는 방안: 적정 수준의 추상화(YAGNI 원칙) 및 경량 컨테이너 기술 도입함

## Ⅵ. 전망
- 발전 방향: 마이크로서비스(MSA)와 서버리스 환경의 자동 최적화 확장 기술 진화
- CSF: 변경 영향 분석(Impact Analysis)의 자동화와 서비스 간 인터페이스 계약 관리가 핵심임
