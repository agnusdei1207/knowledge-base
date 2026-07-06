---
title: "파이프라인 해저드 - 데이터·제어·구조 (Pipeline Hazards)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 8
---

## 미리 알고가기

- Stall: 파이프라인 진행을 일시 정지해 의존성이나 자원 충돌을 해소하는 동작임
- Bubble: stall 때문에 파이프라인에 삽입되는 무효 작업 슬롯임
- 읽기 후 쓰기(Read After Write, RAW): 앞 명령의 결과를 뒤 명령이 읽어야 하는 실제 데이터 의존성임
- Flush: 잘못 인출한 명령어를 파이프라인에서 제거하는 동작임

## Ⅰ. 개요

- **정의**: 파이프라인 해저드는 다음 명령어가 예정된 클록에 다음 단계로 진행하면 결과 오류나 자원 충돌이 발생하는 상황임. 구조, 데이터, 제어 원인을 기준으로 stall, forwarding, flush 같은 제어 방식을 선택하기 위해 사용함.
- **배경/필요성**: 파이프라인은 여러 명령어를 겹쳐 실행하므로 서로 같은 자원을 쓰거나 이전 결과를 기다리거나 분기 방향이 확정되지 않는 상황이 생김. 해저드를 정확히 분류해야 성능 저하와 정합성 오류를 동시에 줄일 수 있음.
- **비유**: 여러 사람이 같은 조립 라인을 쓰는 중에 부품이 늦게 오거나 길이 막히거나 작업 순서가 바뀌는 상황임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 해저드 유형별 원인과 제어 기법 설명 | structural, data, control, stall, forwarding, flush | 해저드를 단순 성능 저하로만 설명 |

> 요약: 해저드는 파이프라인 병렬성 때문에 생기는 정합성·자원·제어 흐름 문제임.

## Ⅱ. 특징/비교

| 판단 기준 | 구조적 해저드 | 데이터 해저드 | 제어 해저드 |
|:---|:---|:---|:---|
| 발생 원인 | 두 단계가 같은 하드웨어 자원을 동시에 요구함 | 뒤 명령이 앞 명령 결과를 아직 받지 못함 | 분기 결과가 확정되기 전에 다음 PC를 선택함 |
| 대표 상황 | 단일 메모리를 IF와 MEM이 동시에 사용함 | load 다음 명령이 load 결과를 바로 사용함 | branch, jump, exception 발생 |
| 우선 대응 | 자원 분리, port 추가, scheduling | forwarding, interlock, renaming | branch prediction, delayed branch, flush |
| 판단 지표 | resource conflict cycle | RAW/WAR/WAW, stall cycle | branch miss rate, flush penalty |

> 요약: 해저드는 원인별로 대응 수단이 다르므로 유형 분류가 먼저임.

## Ⅲ. 구성요소

```text
Cycle:   1      2      3      4      5      6
I1:     IF --> ID --> EX --> MEM -> WB
I2:            IF --> ID --> ST  -> EX  -> MEM -> WB
                            |
                         bubble
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Hazard detection unit | operand, destination, 자원 사용 상태를 비교해 위험을 탐지함 | 교통 관제 |
| Interlock/Stall | 진행을 멈춰 잘못된 실행을 방지함 | 일시 정지 신호 |
| Forwarding path | 아직 WB 전인 결과를 필요한 단계로 직접 전달함 | 우회 전달 |
| Flush control | 잘못 인출된 명령어를 무효화하고 올바른 PC에서 다시 시작함 | 잘못 온 작업 취소 |

> 요약: 해저드 제어 구성은 위험 탐지, 일시 정지, 우회 전달, 잘못된 흐름 회복으로 구성됨.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Detect   | --> | Classify | --> | Control  | --> | Resume   |
+----------+     +----------+     +----------+     +----------+
                    | data/control/structural |
```

1. **의존성 탐지** - pipeline register의 source/destination register와 자원 사용 상태를 비교함
2. **해저드 분류** - 구조적, 데이터, 제어 해저드 중 어떤 원인인지 판단함
3. **제어 수행** - forwarding, stall, flush, resource arbitration 중 적절한 제어를 적용함
4. **정상 재개** - 올바른 operand와 PC가 확보되면 파이프라인 진행을 재개함

> 요약: 해저드 처리는 탐지 후 원인별 제어를 적용하고 정합성이 보장될 때 진행하는 절차임.

## Ⅴ. 문제점 및 개선방안

- **P1 CPI 증가**: bubble과 flush가 많아지면 이상적 CPI 1에서 멀어지고 처리량이 감소함
- **P1 대응**: compiler scheduling, forwarding, branch prediction으로 bubble 삽입 빈도를 낮춤 (확인: CPI, stall cycle)
- **P2 정합성 오류 위험**: 탐지 로직이 누락되면 이전 명령 결과가 확정되기 전에 잘못된 operand로 실행될 수 있음
- **P2 대응**: interlock 조건, dependency checker, pipeline assertion을 설계 검증에 포함함 (확인: formal check, simulation failure)
- **P3 제어 로직 복잡도**: forwarding mux, 비교기, predictor, flush 경로가 늘면 전력과 검증 부담이 증가함
- **P3 대응**: 단순 in-order 코어와 고성능 비순서 실행(Out-of-Order, OoO) 코어를 요구사항별로 분리하고 로직을 모듈화함 (확인: area, power, coverage)

> 요약: 해저드 개선은 성능 최적화와 정합성 검증을 분리하지 않고 함께 설계해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| in-order 임베디드 코어 | load-use와 branch 해저드를 interlock과 compiler scheduling으로 제어해 정합성과 최악 지연을 확보함 | stall cycle, WCET, interlock coverage |
| OoO 서버 코어 | renaming, speculation, forwarding으로 해저드를 숨기되 rollback과 exception 정합성을 검증함 | IPC, rollback 오류, formal property pass |
| CPU 검증 환경 | RAW/WAR/WAW, 구조 충돌, branch flush 조합 테스트를 regression에 포함함 | coverage, assertion failure, bug escape rate |

> 요약: 해저드는 성능 기법보다 정합성 보장이 우선이며, 대응 방식은 코어 목적과 검증 비용에 맞춰 선택함.

## Ⅶ. 전망

- **발전 방향**: 고성능 코어는 renaming, speculation, memory disambiguation으로 해저드를 동적으로 숨기고, 실시간 코어는 단순 interlock으로 지연 상한을 보존함
- **기술사적 판단**: 데이터·제어·구조 해저드는 forwarding network, predictor, resource duplication 비용과 timing path 증가를 함께 계산해 대응 수준을 정함; load-use, branch flush, structural conflict, exception 동시 발생 시나리오에서 interlock 조건과 rollback 정합성을 먼저 확인함
- **기술사 제언**: 세 해저드는 원인, 대표 예, 대응 기법, `CPI` 영향으로 연결해 단순 암기보다 성능 손실 구조를 보여줘야 함
