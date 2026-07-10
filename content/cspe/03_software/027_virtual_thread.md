---
title: "가상 스레드 — Java Project Loom (Virtual Thread)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 27
extra:
  question_no: "027"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- 가상 스레드는 JVM이 관리하는 경량 스레드임
- carrier thread는 실제 OS 스레드로 가상 스레드를 실행하는 기반임
- blocking 시 가상 스레드의 continuation을 분리해 carrier thread를 다른 작업에 재사용함

## Ⅰ. 개요

- **정의/개념**: 가상 스레드는 Java Project Loom이 제공하는 경량 실행 단위로, 많은 수의 애플리케이션 수준 스레드를 적은 수의 OS 스레드 위에 매핑해 대규모 동시성을 단순한 동기 코드 스타일로 처리하게 하는 구조임
- **배경/필요성**: 전통 OS 스레드는 메모리와 문맥 전환 비용이 커서 대량 연결과 대규모 요청 처리에 한계가 있으므로, 비동기 코드를 강요하지 않으면서 높은 동시성을 제공할 실행 모델이 필요했음

## Ⅱ. 특징

- 스레드 수를 크게 늘려도 OS 스레드보다 자원 비용이 낮음
- 동기식 프로그래밍 모델을 유지하면서도 대량 연결 처리가 가능함
- blocking 연산이 carrier thread를 붙잡는 pinning 상황은 성능 저하 원인이 됨
- CPU 집약 병렬 처리보다 I/O 대기 중심 서버 워크로드에 더 적합함

## Ⅲ. 종류 및 비교

| 판단 기준 | OS 스레드 | 가상 스레드 |
|:---|:---|:---|
| 실행 자원 | 스레드별 OS 스택·스케줄링 자원 사용 | 여러 가상 스레드가 carrier thread 집합 공유 |
| 대기 처리 | blocking 동안 OS 스레드 점유 | 지원되는 blocking 지점에서 carrier 분리 |
| 프로그래밍 모델 | 익숙한 동기 코드 | 동일한 동기 코드 유지 |
| 주의점 | 스레드 수 과다 비용 | pinning과 scheduler 이해 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Virtual Thread | 애플리케이션 논리 작업 단위로 요청별 처리 모델을 단순하게 유지함 |
| Carrier Thread Pool | 실제 OS 스레드 집합으로 가상 스레드 실행을 맡아 자원 사용량을 제어함 |
| Continuation Scheduler | 가상 스레드 중단과 재개를 관리해 blocking 구간에서도 높은 동시성을 유지하려 함 |
| Pinning Point | synchronized 블록이나 native 호출처럼 carrier를 고정할 수 있는 지점으로 성능 리스크 판단의 핵심임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 생성      | --> | 가상 스레드 할당 | --> | carrier 실행   | --> | 중단/재개 관리 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 생성**: 각 작업이나 연결마다 가상 스레드를 생성함
2. **가상 스레드 할당**: JVM이 carrier thread에 작업을 매핑함
3. **carrier 실행**: 코드가 실행되다가 blocking 지점에서 중단될 수 있음
4. **중단 및 재개 관리**: JVM이 다른 작업으로 전환하고 이후 다시 재개함

## Ⅵ. 실무 적용 및 유의점

1. 대량 HTTP나 JDBC 중심 서비스에서는 가상 스레드로 동기 코드를 유지하되 pinning 구간이 carrier thread를 오래 붙잡지 않도록 synchronized와 native 호출을 줄이고 carrier utilization과 pinned thread time과 request latency로 확인함
2. CPU 집약 작업은 가상 스레드에 무리하게 섞지 말고 별도 executor로 분리하되 관측 도구가 대량 스레드를 따라가지 못할 수 있으므로 thread dump와 telemetry 기준을 함께 정비하고 CPU saturation과 telemetry overhead로 확인함

## Ⅶ. 결론

가상 스레드는 스레드 모델을 바꾸는 기술이 아니라 동기 코드의 생산성을 유지하면서 대기 중심 동시성을 확장하는 실행 구조임.
