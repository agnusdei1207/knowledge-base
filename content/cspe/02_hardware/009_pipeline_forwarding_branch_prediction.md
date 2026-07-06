---
title: "파이프라인 포워딩·분기 예측 (Pipeline Forwarding Branch Prediction)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 9
---

## 미리 알고가기

- Forwarding: 결과를 레지스터에 쓰기 전에 필요한 파이프라인 단계로 직접 전달하는 기법임
- Branch prediction: 분기 결과와 목표 주소를 미리 예측해 instruction fetch를 지속하는 기법임
- 분기 대상 버퍼(Branch Target Buffer, BTB): 분기 명령의 목표 주소를 저장하는 캐시임
- Misprediction penalty: 잘못 예측한 명령어를 flush하고 다시 채우는 데 드는 클록 비용임

## Ⅰ. 개요

- **정의**: 파이프라인 포워딩과 분기 예측은 데이터 해저드와 제어 해저드로 인한 stall을 줄이기 위해 결과값과 다음 프로그램 카운터(Program Counter, PC)를 미리 공급하는 성능 개선 기법임. forwarding 가능 여부, 분기 예측 정확도, miss penalty를 기준으로 파이프라인 효율을 판단함.
- **배경/필요성**: 파이프라인은 이전 명령 결과와 분기 방향이 확정되기 전에도 다음 명령어를 처리하려고 하므로 대기 시간이 발생함. 포워딩은 operand 대기를 줄이고, 분기 예측은 fetch 중단을 줄여 처리량을 높임.
- **비유**: 포워딩은 완성품을 창고에 넣기 전에 다음 작업자에게 바로 넘기는 것이고, 분기 예측은 갈림길에서 목적지를 미리 고르는 것임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 데이터·제어 해저드 완화 원리 설명 | bypass path, load-use, BTB, predictor, flush | forwarding과 branch prediction을 같은 해저드 대응으로 혼동 |

> 요약: 포워딩은 데이터 대기 시간을, 분기 예측은 다음 명령어 공급 중단을 줄이는 기법임.

## Ⅱ. 특징/비교

| 판단 기준 | Stall 중심 처리 | Forwarding/Branch Prediction |
|:---|:---|:---|
| 데이터 해저드 대응 | 결과가 WB될 때까지 pipeline을 멈춤 | EX/MEM 결과를 필요한 단계로 우회 전달함 |
| 제어 해저드 대응 | 분기 결과가 확정될 때까지 fetch를 멈춤 | 다음 PC와 target을 예측하고 틀리면 flush함 |
| 성능 효과 | 구현은 단순하지만 CPI가 증가함 | 제어 로직은 복잡하지만 평균 처리량이 높아짐 |
| 적용 조건 | 단순 MCU, 예측 가능성 우선 시스템 | 고성능 CPU, deep pipeline, branch 빈도 높은 workload |

> 요약: 평균 처리량을 높이려면 대기보다 우회와 예측을 선택하지만 검증과 회복 비용이 증가함.

## Ⅲ. 구성요소

```text
Data path:
+-----+     +-----+     +-----+     +-----+
| ID  | --> | EX  | --> | MEM | --> | WB  |
+-----+     +--+--+     +--+--+     +-----+
              |           |
              +----> mux <-+

Control path:
+-----+     +-----+     +-----+
| PC  | --> | BTB | --> | IF  |
+-----+     +-----+     +-----+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Forwarding mux | EX/MEM/WB 결과 중 필요한 값을 ALU 입력으로 선택함 | 우회 배달 |
| Hazard detection | load-use처럼 forwarding만으로 해결할 수 없는 상황을 탐지함 | 위험 감시 |
| Branch predictor | 과거 패턴으로 분기 taken/not-taken을 예측함 | 경로 예측 |
| BTB/Return stack | 분기 target과 return address를 저장해 fetch 대기를 줄임 | 목적지 메모 |

> 요약: 포워딩은 데이터 경로 우회, 분기 예측은 PC 공급 경로 예측으로 동작함.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Detect   | --> | Select   | --> | Speculate| --> | Recover  |
+----------+     +----------+     +----------+     +----------+
 data dep        bypass mux       predicted PC      flush if wrong
```

1. **의존성 확인** - source register와 이전 명령의 destination register를 비교해 데이터 의존성을 찾음
2. **우회 선택** - 가능한 경우 MEM 또는 WB 단계 결과를 ALU 입력으로 직접 전달함
3. **분기 예측** - branch predictor와 BTB가 다음 PC를 정하고 fetch를 계속 진행함
4. **검증과 회복** - 실제 결과와 예측을 비교해 틀리면 잘못 인출한 명령어를 flush함

> 요약: 파이프라인은 데이터는 우회하고 제어 흐름은 예측한 뒤 틀린 부분만 회복함.

## Ⅴ. 문제점 및 개선방안

- **P1 load-use 한계**: 메모리 load 결과는 MEM 단계 후에야 준비되어 바로 다음 명령에는 stall이 필요할 수 있음
- **P1 대응**: compiler instruction scheduling, load delay slot 회피, non-blocking cache로 load-use stall을 줄임 (확인: load-use stall)
- **P2 분기 오예측 비용**: deep pipeline에서 오예측 시 많은 명령어를 flush해 성능 손실이 커짐
- **P2 대응**: hybrid predictor, global/local history, BTB 용량 조정, return address stack을 적용함 (확인: prediction accuracy, MPKI)
- **P3 보안 부작용**: 투기 실행과 공유 predictor 상태가 cache side channel 공격에 이용될 수 있음
- **P3 대응**: predictor partitioning, speculation barrier, microcode mitigation, 민감 workload의 SMT 제한을 적용함 (확인: 취약점 점검, 성능 영향)

> 요약: 포워딩과 분기 예측은 성능 지표와 보안 완화 비용을 함께 측정해 적용해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| load-use 해저드 최적화 | forwarding으로 해결 가능한 ALU 결과와 stall이 필요한 load 결과를 구분해 scheduling을 적용함 | load-use stall, CPI, forwarding hit |
| branch-heavy workload | BTB와 global/local predictor를 조정해 오예측 flush 비용을 낮추고 branch miss를 PMU로 확인함 | branch miss rate, MPKI, flush cycle |
| 보안 민감 서비스 | speculation barrier와 predictor 격리를 적용하고 성능 감소와 side-channel 위험을 함께 평가함 | 취약점 테스트, p95 latency, 성능 감소율 |

> 요약: 포워딩과 분기 예측은 해저드 유형별로 성능 이득과 실패 비용을 분리해 측정해야 함.

## Ⅶ. 전망

- **발전 방향**: forwarding은 더 넓은 bypass network로 확장되고, branch prediction은 긴 history·BTB·RAS를 활용하되 보안 요구에 따라 예측 자원 격리가 병행됨
- **기술사적 판단**: forwarding 경로는 load-use 지연과 클록 경로 길이, predictor는 table 크기·전력·mispredict penalty를 기준으로 균형을 잡아야 함; producer-consumer 의존성, load forwarding 실패, BTB aliasing, return prediction 오류를 테스트하고 `branch miss rate`와 flush cycle을 측정함
- **기술사 제언**: forwarding은 데이터 해저드 대응, branch prediction은 제어 해저드 대응으로 분리하고 각각의 지표와 실패 조건을 함께 제시해야 함
