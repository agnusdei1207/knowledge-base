---
title: 임베디드 및 실시간 운영체제 (Embedded/RTOS)
date: 2026-07-05
tags: [cspe-software]
weight: 140
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 특정 목적을 위해 하드웨어에 내장되어 실시간 제어를 수행하는 OS |
| 필요성 | 작업 처리 시간의 예측 가능성(Determinism) 및 고장 안전성(Fail-safe) |
| 출제 의도 | 경성(Hard) vs 연성(Soft) RTOS, 우선순위 역전 및 해결책 이해 |

## Ⅱ. 구성요소
```text
+-----------------------+      [ Key Concepts ]
|  Embedded Application |      - Determinism (시간 예측)
+-----------------------+      - Low Latency (저지연)
|   Real-time Kernel    |      - Footprint (경량화)
+-----------------------+      - Fault Tolerance (내결함)
| Hardware (MCU/FPGA)   |
+-----------------------+
```
| 구성요소 | 설명 | 판단 기준 |
|---|---|---|
| 실시간 커널 | 우선순위 기반 선점과 interrupt·동기화 경로를 관리함 | 최악 응답시간 |
| 태스크 (Task) | 우선순위·주기·deadline·실행시간을 갖는 실행 단위임 | schedulability 입력 |
| 타이머 서비스 | 주기 task release와 timeout·deadline 감시 기준을 제공함 | timer 해상도·jitter |
> 요약: RTOS는 task 우선순위, 선점, timer, 동기화 상한을 이용해 최악 응답시간과 deadline 준수 여부를 분석함.

## Ⅲ. 절차
```text
Event -> Interrupt -> Context Switch -> High Priority Task Run
  |                                            |
  +-- (Deadline Check) <--- Result Update <----+
```
1. 이벤트 발생: 센서 데이터 입력 또는 타이머 알람 등 외부 인터럽트 수신.
2. 선점 판단: 현재 task보다 높은 우선순위의 ready task가 있으면 context switch를 수행함.
3. 태스크 실행: 정해진 데드라인(Deadline) 내에 제어 로직 처리 완료.
4. 자원 반납: 결과 출력 후 낮은 우선순위 작업으로 제어권 복귀.
> 요약: interrupt 처리 후 최고 우선순위 ready task를 선택하고 실행·동기화 시간을 포함해 deadline을 검증함.

## Ⅳ. 문제점
- 낮은 우선순위 태스크가 공유 자원을 점유하여 높은 태스크가 대기하는 우선순위 역전.
- 제한된 자원(Memory, CPU) 환경에서 비대해진 미들웨어로 인한 성능 병목.

## Ⅴ. 개선방안
- PIP(Priority Inheritance Protocol) 또는 PCP를 적용하여 우선순위 역전 해결.
- 마이크로 커널 기반 설계로 필요한 기능만 모듈식으로 탑재하여 경량화 유지.

## Ⅵ. 전망
- AIoT 대응: 임베디드 환경에서 경량 딥러닝 추론을 지원하는 RTOS 최적화 활발.
- 자율주행 표준: AUTOSAR 등 자동차용 고안전성 실시간 소프트웨어 아키텍처 확산.
