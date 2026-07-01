---
title: "추론 스케일링 (Inference Scaling)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 54
---

# 📖 【암기용】 개념 완전 이해

> 목적: 추론 스케일링을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 학습 후 추론 단계에서 연산량·후보 수·검증 횟수를 늘려 정답률을 높이는 기법
- **왜 필요한가**: 모델 파라미터를 더 키우는 학습 스케일링은 비용이 크고, 복잡 문제는 답변 전 생각 시간 자체가 성능을 좌우함.
- **핵심 직관**: 시험 준비량(학습)을 늘리는 대신, 시험장에서 풀이 시간과 검산 횟수를 늘려 정답률을 올리는 방식임.

## 깊이 이해
- **배경·문제의식**: LLM 발전은 pre-training scaling law 중심이었으나, reasoning model 이후 test-time compute가 별도 성능 축으로 부상함. 같은 모델도 후보 풀이 수와 검증기를 늘리면 pass@k가 상승함.
- **작동 원리**: Best-of-N, Self-Consistency, Tree-of-Thought, verifier reranking을 사용함. 단순 질의는 낮은 예산, 복잡 질의는 높은 예산을 배정하는 adaptive compute가 비용 통제 핵심임.
- **비유**: 어려운 문제는 한 가지 풀이만 보지 않고 여러 풀이를 써 본 뒤, 검산으로 가장 타당한 답을 고르는 것임.
- **구체 예시**: R1-Zero는 majority voting 적용 시 AIME 2024 정확도가 71.0%에서 86.7%로 상승함.
- **흔한 오해·주의점**: 추론 예산 증가가 정답률을 선형으로 올린다는 단정은 비용 대비 효과를 검토하지 않은 표현임. 쉬운 문제는 비용만 증가하고, 잘못된 검증기는 오류 답을 선택할 수 있음.

## 연결 개념
- Test-Time Compute — 추론 단계 연산 예산
- Self-Consistency — 여러 CoT 답변 투표
- Verifier/Reranker — 후보 답변 평가 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Inference Scaling은 추론 시 후보 생성·탐색·검증 연산을 늘려 정답률을 높이는 test-time compute 전략임.
> 2. **가치**: 모델 재학습 없이 Best-of-N·Self-Consistency로 수학·코딩 pass@k를 상승시킴.
> 3. **판단 포인트**: 난이도별 예산 라우팅, 비용/request, p95 지연, verifier 품질이 운영 기준임.

---

## Ⅰ. 개요 및 필요성

- 개요: 추론 단계 연산 확대 전략
- 배경: 파라미터 증설·재학습은 비용과 일정 부담이 커서 같은 모델의 추론 예산 조절이 운영 대안이 됨.
- 필요성: sample count, verifier, search depth, token budget으로 복잡 추론 정답률과 비용 균형점을 산정해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Query -> Difficulty Router -> Candidate Generator(N)
      -> Verifier/Reranker -> Voting/Selection -> Final Answer
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Difficulty Router | 요청 난이도 분류 | low/medium/high budget |
| Candidate Generator | N개 풀이·답변 생성 | Best-of-N, pass@k |
| Verifier/Reranker | 후보 정답성 평가 | unit test, reward model |
| Selection Policy | 투표·최고점 선택 | majority voting, weighted vote |

> 요약: 추론 스케일링은 난이도 라우팅 후 여러 후보를 만들고 검증기로 선택하는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
입력 -> 난이도 추정 -> N·토큰 예산 결정
   -> 후보 풀이 생성 -> 검증/투표 -> 최종 답 선택 -> 비용 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청 유형·난이도 분류 | 정확도 uplift 예상 |
| 2 | 후보 수 N과 max reasoning token 결정 | N=1/4/16/64 |
| 3 | 후보 생성 후 검증기 평가 | pass@k, verifier accuracy |
| 4 | 답 선택·비용 로깅 | p95 지연, cost/request |

> 요약: 입력 난이도에 따라 추론 예산을 차등 배정하고, 후보 검증 결과로 정답률과 비용을 동시에 관리함.

---

## Ⅳ. 특징

| 구분 | 학습 스케일링 | 추론 스케일링 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 비용 발생 시점 | 사전학습/미세조정 | 요청 처리 시점 | 호출량 증가 시 비용 선형 증가 |
| 적용 방식 | 파라미터·데이터 확대 | 후보 수·검증 횟수 확대 | N=1->16 |
| 장점 | 모든 요청 기본 능력 상승 | 고난도 요청에 선택 적용 | adaptive routing |
| 한계 | GPU 학습비 고정 부담 | 지연·토큰 비용 증가 | p95 SLA 초과 위험 |

> 요약: 추론 스케일링은 고난도 문제에 선택 적용할 때 비용 대비 정답률 개선 효과가 크며, 전 요청 적용은 SLA 리스크가 큼.

---

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 요청 라우터를 구축해 단순 요약은 N=1, 수학·코딩은 N=8~32 후보 생성으로 예산 차등화
2. 코드 업무는 unit test 기반 verifier를 사용해 통과 후보만 최종 답변으로 채택
3. 비용 지표를 `cost/request`, `tokens/request`, `p95 latency`로 수집하고 월 예산 초과 시 N 상한 자동 축소

**결론 (2줄):**
- 기술사 판단: 정답률 SLA가 핵심인 수학·코딩은 추론 스케일링, 실시간 채팅은 낮은 N과 빠른 모델을 선택함.
- 향후 방향: adaptive compute와 verifier 품질 개선이 reasoning LLM 운영의 핵심 경쟁력으로 이동함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 후보 생성·검증·선택 흐름 | 학습 스케일링 대비 차이 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | 난이도 라우팅·예산 제어 절차 | 비용·지연·정답률 선택 기준 |

> 요약: 설명형은 test-time compute 원리, 최적화형은 adaptive budget 운영 기준으로 목차를 전환함.
