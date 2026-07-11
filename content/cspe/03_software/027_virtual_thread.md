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
- continuation: 실행 중단 지점의 상태를 저장해 나중에 재개할 수 있게 하는 구조임
- pinning: native 호출처럼 JVM이 continuation을 분리하지 못해 carrier가 점유된 채 유지되는 구간임

## 작성 근거(검토용)

- OS 스레드와 가상 스레드를 실행 자원 및 스케줄러·대기 처리 및 제약·적합 업무로 비교함
- carrier 탑재·I/O 중단·continuation 보관·재탑재를 실제 실행 상태 전이로 유지함
- HTTP·JDBC 서비스와 CPU 작업을 분리해 carrier 점유와 요청 지연을 검증함

## Ⅰ. 개요

- **정의/개념**: 가상 스레드는 Java Project Loom이 제공하는 JVM 관리 실행 단위로, 애플리케이션 스레드를 carrier OS 스레드 집합에 다중화하고 I/O 대기 시 carrier를 재사용하는 구조임
- **배경/필요성**: 연결마다 OS 스레드를 배정할 때 발생하는 스택 메모리와 커널 스케줄링 자원을 줄이기 위해 JVM 실행 단위가 필요함

## Ⅱ. 특징

- 여러 가상 스레드가 carrier thread 집합을 공유함
- 요청별 동기식 코드를 유지하면서 I/O 대기 시 carrier를 다른 작업에 배분함
- pinning 구간에서는 가상 스레드가 중단돼도 carrier thread를 다른 작업에 배분하지 못함
- I/O 대기 중심 서버를 적용 대상으로 하며 CPU 집약 작업의 계산 병렬도를 늘리지는 않음

## Ⅲ. 종류 및 비교

| 판단 기준 | OS 스레드 | 가상 스레드 |
|:---|:---|:---|
| 실행 자원·스케줄러 | 스레드별 OS 스택을 운영체제 커널이 스케줄링함 | 여러 가상 스레드가 carrier thread 집합을 공유하며 JVM 스케줄러가 배정함 |
| 대기 처리·제약 | blocking 동안 OS 스레드를 점유하며 스레드 수 과다 시 비용이 커짐 | 지원되는 blocking 지점에서 carrier를 분리하지만 pinning 구간은 분리하지 못함 |
| 적합 업무 | 제한된 수의 장기 실행 작업 | I/O 대기 중심 요청 처리 |

> 요약: OS 스레드는 커널 스케줄링 자원을 개별 사용하고, 가상 스레드는 carrier를 공유하며 I/O 대기 시 분리됨.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| 가상 스레드 | 애플리케이션 요청별 실행 상태와 스택을 나타냄 |
| Carrier thread 집합 | 가상 스레드를 실제로 실행하는 OS 스레드 집합임 |
| Continuation 스케줄러 | 가상 스레드의 중단 상태를 보관하고 carrier에 다시 탑재함 |
| Pinning 지점 | native 호출 등 JVM이 continuation을 분리할 수 없는 구간에서 carrier 반환을 제한함 |

> 요약: JVM은 가상 스레드 상태를 carrier에 탑재하고 I/O 대기 시 continuation으로 분리·재개함.

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 생성      | --> | 가상 스레드 할당 | --> | carrier 실행   | --> | 중단/재개 관리 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 생성**: 각 작업이나 연결마다 가상 스레드를 생성함
2. **Carrier 탑재**: JVM이 실행 가능한 가상 스레드를 carrier에 매핑함
3. **중단·분리**: 지원되는 I/O 대기에서 continuation을 보관하고 carrier를 반납함
4. **재탑재·재개**: I/O 완료 후 가상 스레드를 carrier에 다시 탑재해 실행함

## Ⅵ. 실무 사례

1. HTTP·JDBC 서버는 요청별 가상 스레드를 적용하고 pinned thread 시간과 p99 요청 지연을 확인함
2. CPU 집약 작업은 별도 executor로 분리하고 CPU 포화율과 carrier 이용률을 확인함

## Ⅶ. 결론

- 가상 스레드는 I/O 대기 비율과 pinning 구간을 기준으로 carrier 공유 실행 모델을 적용함
