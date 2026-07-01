---
title: "오프라인 평가 (Offline Evaluation)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 229
---

# 📖 【암기용】 개념 완전 이해

> 목적: 오프라인 평가를 배포 전에 고정 데이터셋과 기준 지표로 모델 후보를 선별하는 평가 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 운영 배포 전 검증 데이터셋으로 모델의 정확도, 순위 품질, 안전성, 비용을 평가하는 방식
- **왜 필요한가**: 모든 후보 모델을 사용자에게 노출하면 비용과 위험이 커지므로 사전에 낮은 품질의 후보를 걸러야 한다.
- **핵심 직관**: 신제품을 매장에 내기 전에 실험실의 표준 시험 항목을 먼저 통과시키는 단계다.

## 깊이 이해
- **배경·문제의식**: 모델 학습은 여러 후보를 만들지만 운영 실험 트래픽은 제한되어 있어 후보를 줄이는 평가 관문이 필요하다.
- **작동 원리**: train/validation/test 분리, holdout 데이터, benchmark set, regression test set으로 accuracy, F1, NDCG, hallucination rate 등을 측정한다.
- **비유**: 운전면허 도로주행 전에 장내 기능 시험으로 기본 조작 오류를 먼저 거르는 구조와 같다.
- **구체 예시**: 검색 랭킹 모델은 test set에서 NDCG@10 0.42 이상, latency offline replay 100ms 이하, 금칙어 위반 0건 기준을 통과해야 online evaluation 후보가 된다.
- **흔한 오해·주의점**: 오프라인 평가는 배포 결정을 단독으로 보장하지 않는다. 데이터 분포가 바뀌면 online metric과 차이가 발생한다.

## 연결 개념
- Online Evaluation — 오프라인 통과 모델의 실제 사용자 검증 단계
- Human Evaluation — 자동 지표가 놓치는 품질을 사람이 평가
- Continuous Evaluation — 평가를 배포 이후에도 반복 실행

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 오프라인 평가는 배포 전 후보 모델을 고정 데이터셋과 자동 지표로 선별하는 품질 게이트다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Offline Evaluation은 배포 전 holdout·benchmark 데이터셋으로 모델 후보를 자동 평가하는 절차임.
> 2. **가치**: accuracy, F1, NDCG, hallucination rate, latency replay 기준으로 저품질 후보의 온라인 노출을 차단함.
> 3. **판단 포인트**: 오프라인 점수는 후보 선별 기준이고 최종 채택은 온라인 평가와 운영 지표로 결정해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 평가 데이터 관리 이해 확인 | train/validation/test, holdout, benchmark | 학습 데이터와 평가 데이터 혼용 |
| 지표 선택 판단 확인 | classification, ranking, generation별 지표 | accuracy 하나로 모든 모델 평가 |
| 한계 인식 확인 | data drift, offline-online gap | 오프라인 점수만으로 배포 결정 |

> 요약: 이 문제는 배포 전 품질 게이트와 offline-online gap을 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 배포 전 고정 데이터셋 기반 평가
- 배경: 후보 모델을 모두 온라인 실험에 올리면 사용자 위험과 실험 비용이 증가함.
- 필요성: NDCG@10, F1, hallucination rate, replay latency 같은 기준으로 후보를 사전 선별해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Dataset Split -> Benchmark Set -> Metric Runner -> Quality Gate -> Candidate Registry
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Dataset Split | train/validation/test 분리 | data leakage 방지 |
| Benchmark Set | 대표·난이도·안전 케이스 구성 | 회귀 테스트 포함 |
| Metric Runner | 자동 지표 계산 | F1, AUC, NDCG, BLEU, exact match |
| Quality Gate | 기준 통과 여부 결정 | CI/CD와 연동 |

> 요약: 오프라인 평가는 데이터 분리, 벤치마크, 지표 실행기, 품질 게이트로 배포 후보를 제한한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
평가셋 고정 -> 후보 모델 추론 -> 자동 지표 계산 -> 기준선 비교 -> 통과 모델 등록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 평가셋과 gold label을 고정 | leakage 0건 |
| 2 | 후보 모델로 batch inference 실행 | 평가 재현성 |
| 3 | 업무별 자동 지표 계산 | F1, NDCG, hallucination rate |
| 4 | baseline과 비교해 registry 등록 | 기준선 대비 개선 |

> 요약: 오프라인 평가는 고정 평가셋에서 후보 모델을 재현 가능하게 비교해 온라인 검증 대상을 선별한다.

---

## Ⅳ. 특징

| 구분 | Online Evaluation | Offline Evaluation | 수치 기준 |
|:---|:---|:---|:---|
| 평가 시점 | 배포 후 | 배포 전 | CI 단계 실행 |
| 사용자 영향 | 실사용자 영향 있음 | 사용자 영향 없음 | 영향 사용자 0명 |
| 한계 | 비용·윤리 통제 필요 | offline-online gap 존재 | drift 감시 필요 |

> 요약: 오프라인 평가는 비용과 위험이 낮지만 운영 분포 차이를 반영하지 못할 수 있다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 목적 | online은 최종 가치 검증 | offline은 후보 선별 | 실험 트래픽 제한 시 offline 우선 |
| 비용/성능 | human eval은 비용 높음 | 자동 지표는 반복 비용 낮음 | 정답 라벨 품질이 확보되면 offline |
| 운영/위험 | 배포 영향 있음 | 사용자 영향 없음 | 민감 업무 사전 게이트 |

> 요약: 오프라인 평가는 반복 가능한 자동 품질 게이트로 사용하고 최종 판단은 온라인 평가와 결합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 데이터 누수 | 학습 데이터와 평가 데이터 중복 | dedup, split hash 관리 | overlap 0건 |
| 평가셋 노후화 | 운영 분포 변화 | 월 1회 샘플 갱신, drift 분석 | PSI, KL divergence |
| 지표 불일치 | 자동 지표와 사용자 만족 차이 | human eval, online eval 병행 | offline-online correlation |

> 요약: 오프라인 평가 리스크는 데이터 누수, 평가셋 노후화, 지표 불일치이며 데이터 관리와 보완 평가로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 재현성 | 동일 모델 평가 결과 오차 0.1% 이내 | seed 고정, CI 재실행 |
| 품질 | baseline 대비 F1 또는 NDCG 개선 | metric report |
| 안전성 | 금칙·개인정보 위반 0건 | rule checker, red-team set |

> 요약: 오프라인 평가의 성공 기준은 재현성, 품질 개선, 안전 위반 0건을 동시에 만족하는 것이다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. train/validation/test split hash를 registry에 저장해 평가셋 누수를 방지함.
2. 분류는 F1/AUC, 검색은 NDCG@k, 생성형 AI는 factuality·toxicity·refusal rate로 지표를 분리함.
3. offline gate 통과 모델만 shadow 또는 canary 단계로 승격하고 실패 모델은 registry에서 배포 금지함.

**결론 (2줄):**
- 기술사 판단: 오프라인 평가는 배포 전 필터이며 운영 채택은 온라인 평가와 guardrail metric까지 통과한 뒤 결정함.
- 향후 방향: 오프라인 평가는 LLM judge, synthetic test, red-team set을 포함한 지속 평가 파이프라인으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "오프라인 평가를 설명하시오" | 평가셋 고정과 지표 산출 흐름 | 온라인 평가와 차이 |
| 요구사항 명시형 | "모델 평가 기준을 제시하시오" | 업무별 metric runner 설계 | 데이터 누수·drift 대응 |

> 요약: 설명형은 배포 전 품질 게이트를, 기준 제시형은 데이터·지표·리스크 통제를 중심으로 작성한다.
