---
title: 실시간 스케줄러 — RM·EDF (Real-time Scheduling)
date: 2026-07-05
tags: [cspe-software]
weight: 7
---

## Ⅰ. 개요
- 정의: 엄격한 마감 시간(Deadline)을 보장해야 하는 시스템을 위한 스케줄링 기법
- 배경: 임베디드, 제어 시스템 등 결과의 정확성뿐만 아니라 시간적 정확성이 중요한 분야에 필수
- 출제 의도: 정적/동적 우선순위 할당 방식의 차이점 및 스케줄링 가능성 판단 기준 이해

## Ⅱ. 구성요소
```
[ RM: Static Priority ]      [ EDF: Dynamic Priority ]
P1 (Short Period) : High     P1 (Near Deadline) : High
P2 (Long Period)  : Low      P2 (Far Deadline)  : Low
```
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| RM (Rate Monotonic) | 주기가 짧을수록 높은 우선순위를 부여하는 정적 기법 | 단기 과제 우선 |
| EDF (Earliest Deadline First) | 마감 시간이 가까울수록 높은 우선순위를 부여하는 동적 기법 | 급한 불 끄기 |
| 마감 시간 (Deadline) | 작업이 반드시 완료되어야 하는 시점 | 제출 기한 |
> 요약: RM은 주기 기반 정적 할당, EDF는 마감 임박도 기반 동적 할당 방식임.

## Ⅲ. 절차
```
[Task Arrival] -> [Priority Calculation] -> [Preemption] -> [Execution]
```
1. 실시간 작업이 주기적으로 또는 이벤트 발생 시 시스템에 진입함
2. RM은 주기(T)의 역수로, EDF는 현재 시점과 마감 시간의 차로 우선순위 산출
3. 현재 실행 중인 작업보다 높은 우선순위의 작업 도착 시 즉시 선점(Preemption)
4. 마감 시간 내에 작업 완료 여부를 감시하며 스케줄링 유지
> 요약: 마감 시간을 지키기 위해 즉각적인 선점과 우선순위 조정을 수행함.

## Ⅳ. 문제점
- 원인: RM은 CPU 이용률이 약 69%(ln 2)를 넘어가면 마감 시간을 놓칠 수 있음
- 원인: EDF는 과부하(Overload) 발생 시 도미노 현상으로 많은 작업이 실패할 수 있음

## Ⅴ. 개선방안
- (단기) 임계 영역 접근 시 우선순위 상속(Priority Inheritance) 기법으로 역전 방지
- (중기) 주기적 서버(Periodic Server) 모델 도입으로 비주기적 작업의 마감 보장
- (장기) 하드웨어 타이머 정밀도 향상 및 실시간 OS(RTOS) 전용 커널 최적화

## Ⅵ. 전망
- 자율주행, 로봇 제어 등 초저지연 연산 요구에 대응하는 하드웨어 가속 스케줄러 부각
- AI 추론 연산의 확정적 시간(Deterministic Time) 보장을 위한 RT-AI 프레임워크와 결합됨
