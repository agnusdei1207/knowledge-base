---
title: "파이프라인 포워딩·분기 예측 (Pipeline Forwarding Branch Prediction)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 9
extra:
  question_no: "009"
  exam_status: "기출"
  exam_history: "122회"
---

## 미리 알고가기

- 포워딩은 데이터 해저드를 줄이는 우회 전달 기법임
- 분기 예측은 제어 해저드를 줄이기 위한 경로 추정 기법임
- 둘 다 CPI를 낮추지만 실패 비용과 구현 난도가 다름

## Ⅰ. 개요

- **정의/개념**: 포워딩은 연산 결과를 레지스터 기록 전에 다음 명령어로 직접 우회 전달해 데이터 대기를 줄이는 기법이고, 분기 예측은 분기 결과가 확정되기 전에 다음 실행 경로를 추정해 파이프라인 정지를 줄이는 기법임
- **배경/필요성**: 파이프라인이 깊어질수록 값 대기와 분기 대기로 인한 stall이 크게 늘어나므로, 대기 자체를 줄이기 위한 하드웨어 수준 개입이 필요함

## Ⅱ. 특징

- 포워딩은 준비된 결과를 바로 전달해 RAW 해저드를 완화함
- 분기 예측은 speculative execution 기반으로 제어 해저드를 줄임
- 포워딩은 load-use 상황처럼 완전히 없애지 못하는 대기가 남을 수 있음
- 분기 예측은 실패 시 flush 패널티가 크게 발생함

## Ⅲ. 종류 및 비교

| 판단 기준 | 포워딩 | 분기 예측 |
|:---|:---|:---|
| 해결 대상 | 데이터 해저드 | 제어 해저드 |
| 핵심 원리 | bypass 경로 전달 | 다음 경로 추정 |
| 실패 형태 | 남은 stall | flush 발생 |
| 핵심 지표 | load-use stall | branch accuracy |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Forwarding Unit | 생산 레지스터와 소비 레지스터를 비교해 우회 여부를 결정함 |
| Bypass Mux | 레지스터 값 대신 forwarding된 결과를 선택해 ALU 입력으로 보냄 |
| Branch Predictor | 과거 분기 이력이나 패턴을 기반으로 다음 경로를 추정함 |
| Recovery Logic | 예측 실패 시 잘못된 명령을 flush하고 올바른 경로로 복귀함 |

```text
+----------------+     +-----------+     +------------------+
| Forwarding Unit | --> | Bypass Mux | --> | Execution Stage   |
+----------------+     +-----------+     +------------------+
            |
            +--> Branch Predictor --> Recovery Logic
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 의존성/분기 감지  | --> | 우회 또는 예측 결정 | --> | 투기/우회 실행   | --> | 결과 확정·복구   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **의존성과 분기 감지**: 해저드 가능성을 식별함
2. **우회 또는 예측 결정**: bypass 경로나 예측 경로를 선택함
3. **투기 또는 우회 실행**: 파이프라인 진행을 유지함
4. **결과 확정과 복구**: 올바르면 유지하고 틀리면 복구함

## Ⅵ. 문제점 및 해결 방안

1. 문제: load-use 상황에서는 포워딩을 써도 메모리 값이 늦게 준비되어 stall이 남을 수 있음
   - 해결방안: compiler scheduling과 prefetch를 병행하고 load-use stall rate와 memory latency hiding ratio로 검증함
2. 문제: 분기 예측 실패가 많으면 speculative 실행 이점보다 flush 손실이 더 커질 수 있음
   - 해결방안: predictor sophistication을 workload에 맞추고 branch accuracy와 MPKI로 검증함
3. 문제: 우회 경로와 예측기가 복잡해질수록 전력과 검증 비용이 증가할 수 있음
   - 해결방안: hot path 위주로 최적화하고 perf per watt와 verification effort로 검증함

## Ⅶ. 적용 사례

- 컴파일러 최적화에서는 load-use 대기를 줄이고, load-use stall rate와 memory latency hiding ratio로 결과를 확인함
- 서버 CPU 설계에서는 예측기를 고도화하고, branch accuracy와 MPKI로 결과를 확인함
- 저전력 코어 설계에서는 핵심 경로만 최적화하고, perf per watt와 verification effort로 결과를 확인함

## Ⅷ. 결론

포워딩과 분기 예측의 본질은 파이프라인을 멈추지 않게 만드는 적극적 개입이지만, 그 효과는 실패 비용까지 포함해 균형 있게 설계할 때만 유지됨.
