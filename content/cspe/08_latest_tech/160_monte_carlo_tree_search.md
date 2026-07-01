---
title: "몬테카를로 트리탐색 (Monte Carlo Tree Search)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 160
---

# 📖 【암기용】 개념 완전 이해

> 목적: MCTS를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 가능한 행동을 트리로 확장하고 무작위 시뮬레이션 결과를 이용해 유망한 행동을 선택하는 탐색 알고리즘
- **왜 필요한가**: 바둑·게임·계획 문제처럼 경우의 수가 커서 전체 탐색이 불가능할 때 좋은 선택을 찾아야 함.
- **핵심 직관**: 여러 수를 끝까지 다 보지 않고, 유망해 보이는 수를 더 많이 시뮬레이션해 선택하는 방식임.

## 깊이 이해
- **배경·문제의식**: Minimax는 완전 탐색에 가깝고 상태공간이 커지면 계산이 폭증한다. MCTS는 샘플링으로 탐색과 활용을 균형 있게 수행함.
- **작동 원리**: Selection, Expansion, Simulation, Backpropagation 4단계를 반복해 각 행동의 승률·가치를 추정하고 UCT로 탐험-활용 균형을 맞춤.
- **비유**: 모든 길을 끝까지 걸어보지 않고, 몇 번 걸어본 결과가 좋은 길은 더 자주 확인해 최종 경로를 고르는 방식임.
- **구체 예시**: AlphaGo는 policy/value network와 MCTS를 결합해 후보 수를 줄이고 수읽기 품질을 높임.
- **흔한 오해·주의점**: MCTS는 시뮬레이션 비용이 크고 rollout 품질에 민감하다. 실시간 의사결정은 시간 예산 제한이 필요함.

## 연결 개념
- Reinforcement Learning — MCTS가 정책 개선과 계획에 활용됨
- UCT — Upper Confidence Bound 기반 MCTS 선택 공식
- AlphaGo — 딥러닝과 MCTS를 결합한 대표 사례

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MCTS는 시뮬레이션 샘플로 행동 트리의 가치를 추정하는 확률적 탐색 알고리즘임.
> 2. **가치**: 큰 상태공간에서 전체 탐색 없이 유망 행동을 집중 탐색해 의사결정 품질을 높임.
> 3. **판단 포인트**: rollout 비용, 시간 예산, 탐험-활용 계수, 평가함수 품질을 조정해야 함.

## Ⅰ. 개요 및 필요성

MCTS는 시뮬레이션 기반 트리 탐색 알고리즘임. 게임·계획 문제는 가능한 행동 조합이 커 전체 탐색이 어렵다. MCTS는 샘플링과 통계적 가치 추정으로 유망 행동을 선택한다.

## Ⅱ. 구조 및 구성요소

```text
Root State -> Selection -> Expansion -> Simulation -> Backpropagation(value)
Backpropagation -> Visit/Value Update -> Next Selection
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Tree Node | 상태와 행동 통계 저장 | visit count, value |
| Selection Policy | 유망 노드 선택 | UCT, PUCT |
| Rollout/Simulator | 미래 결과 샘플링 | random 또는 policy guided |
| Backpropagation | 결과를 경로 노드에 반영 | 평균 가치 업데이트 |

> 요약: MCTS는 선택·확장·시뮬레이션·역전파를 반복해 행동별 가치와 방문 횟수를 축적함.

## Ⅲ. 동작원리 및 흐름도

```text
루트 상태 입력 -> UCT로 노드 선택 -> 자식 확장
  -> rollout 수행 -> 결과 보상 계산 -> 방문 경로 가치 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Selection: UCT로 탐색할 노드 선택 | exploration c 조정 |
| 2 | Expansion: 미방문 행동 노드 추가 | branching factor 관리 |
| 3 | Simulation: terminal 또는 depth limit까지 rollout | 시간 예산 100ms~5초 |
| 4 | Backpropagation: 보상·승률 업데이트 | visit count 기반 선택 |

> 요약: MCTS는 유망한 노드를 반복적으로 시뮬레이션하고 결과를 역전파해 최종 행동을 결정함.

## Ⅳ. 특징

| 구분 | Minimax | MCTS | 판단 포인트 |
|:---|:---|:---|:---|
| 탐색 방식 | 깊이 제한 완전 탐색 | 확률적 샘플링 | 큰 상태공간은 MCTS |
| 평가 | 휴리스틱 평가함수 | rollout 통계 | 시뮬레이터 필요 |
| 장점 | 결정적 분석 | anytime 특성 | 시간 예산별 품질 |
| 한계 | 폭발적 계산 | rollout 비용·분산 | 정책/가치망 보완 |

> 요약: MCTS는 큰 상태공간에서 시간 예산 내 점진적으로 품질을 높이는 탐색에 적합함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 게임 AI: policy network로 후보 행동을 줄이고 value network로 rollout을 대체해 탐색 횟수 1만->1천회 절감
2. 계획 문제: 물류 경로·로봇 행동 계획에서 depth limit과 안전 제약을 적용해 위험 행동 제외
3. LLM 추론: self-consistency·tree-of-thought에서 후보 reasoning path를 MCTS로 평가하고 상위 경로 선택

**결론 (2줄):**
- 기술사 판단: 상태공간이 크고 시뮬레이터가 있으면 MCTS, 평가함수가 명확하면 Minimax/DP 검토
- 향후 방향: 정책망·가치망·LLM 평가기를 결합한 신경 MCTS가 복잡한 계획 문제로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MCTS를 설명하시오" | Selection->Expansion->Simulation->Backprop 흐름 | Minimax 대비 차이 |
| 요구사항 명시형 | "게임 AI 탐색 방안을 제시하시오" | UCT·rollout·시간 예산 기준 | 정책망·가치망 결합 방안 |

> 요약: 설명형은 4단계 탐색 원리, 방안형은 탐색 비용과 의사결정 품질 조정 기준을 중심으로 작성함.
