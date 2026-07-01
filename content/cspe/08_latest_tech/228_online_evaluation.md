---
title: "온라인 평가 (Online Evaluation)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 228
---

# 📖 【암기용】 개념 완전 이해

> 목적: 온라인 평가를 실제 서비스 환경에서 사용자 행동과 운영 지표로 모델 품질을 검증하는 방법으로 이해하게 만든다.

## 한눈에
- **개요**: 배포된 모델을 실사용 트래픽에서 CTR, conversion, latency, error rate 등으로 평가하는 방식
- **왜 필요한가**: 오프라인 정답 데이터의 점수가 높아도 실제 사용자 만족, 지연, 비용, 안전성은 달라질 수 있다.
- **핵심 직관**: 시제품을 실험실에서 통과시킨 뒤 실제 매장에서 판매량과 반품률을 보는 단계다.

## 깊이 이해
- **배경·문제의식**: 추천, 검색, 광고, LLM 응답은 사용자 맥락과 시간대에 따라 품질이 변하므로 고정 테스트셋만으로 운영 품질을 판단하기 어렵다.
- **작동 원리**: 모델 버전별로 트래픽을 분리하고 노출, 클릭, 구매, 지연, 오류, 비용 로그를 수집해 통계적으로 비교한다.
- **비유**: 새 교통 신호 체계를 지도 시뮬레이션으로만 보지 않고 실제 교차로의 통행 시간과 사고 건수를 측정하는 것과 같다.
- **구체 예시**: 검색 랭킹 v2는 A/B 50:50 트래픽에서 CTR +3%, p95 latency 120ms 이하, error rate 0.1% 이하를 만족할 때 채택한다.
- **흔한 오해·주의점**: 온라인 평가는 사용자를 대상으로 하므로 윤리·안전·롤백 기준이 필요하며, 단순 클릭 증가만으로 품질 향상을 단정하지 않는다.

## 연결 개념
- Offline Evaluation — 배포 전 고정 데이터셋 기반 평가
- A/B Testing — 온라인 평가의 대표 실험 설계
- Canary Model Release — 온라인 지표 기반 점진 배포 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 온라인 평가는 실제 사용자 트래픽에서 품질, 운영 SLA, 사업 지표를 동시에 검증한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Online Evaluation은 운영 환경에 배포된 모델을 실제 사용자 행동과 서비스 지표로 평가하는 방식임.
> 2. **가치**: CTR, conversion, retention, p95 latency, error rate를 model_id별로 측정해 오프라인 평가의 한계를 보완함.
> 3. **판단 포인트**: 사용자 영향이 있으므로 실험군 크기, guardrail metric, rollback 조건을 먼저 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 모델 평가 체계 이해 확인 | 사용자 행동 지표와 운영 지표 동시 측정 | 정확도 지표만 나열 |
| 실험 설계 판단 확인 | randomization, control/treatment, 통계 유의성 | 표본 편향·novelty effect 누락 |
| 운영 위험 통제 확인 | guardrail metric, rollback, ethical review | 사용자 영향과 안전 기준 누락 |

> 요약: 이 문제는 실제 서비스에서 모델 가치와 위험을 지표 기반으로 검증하는 역량을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 실사용 트래픽 기반 모델 평가
- 배경: 고정 테스트셋은 사용자 맥락, 계절성, 지연, 비용, 안전 이슈를 충분히 반영하지 못함.
- 필요성: CTR 3% 개선, p95 latency 120ms 이하, error rate 0.1% 이하 같은 채택 기준을 운영 환경에서 검증해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Traffic -> Experiment Router -> Control / Treatment -> Event Log -> Metric Pipeline -> Decision Gate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Experiment Router | 사용자를 control/treatment로 배정 | random bucket, sticky assignment |
| Event Log | 노출·클릭·전환·오류 이벤트 수집 | model_id, experiment_id 포함 |
| Metric Pipeline | 지표 산출과 통계 검정 수행 | CTR, conversion, p-value |
| Decision Gate | 채택·중단·확대 판단 | guardrail metric 포함 |

> 요약: 온라인 평가는 트래픽 배정, 이벤트 수집, 지표 산출, 의사결정 게이트로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
실험 설계 -> 사용자 무작위 배정 -> 모델별 응답 제공 -> 행동·운영 로그 수집 -> 통계 검정 -> 채택/중단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 실험 목적과 guardrail metric 설정 | 사전 가설 문서화 |
| 2 | control/treatment 사용자 배정 | bucket 균형 |
| 3 | 행동·운영 이벤트 수집 | 로그 누락률 0.1% 이하 |
| 4 | 통계 검정 후 채택 여부 결정 | p-value, confidence interval |

> 요약: 온라인 평가는 사전 가설과 guardrail을 정한 뒤 실제 사용자 행동 로그로 모델 채택을 판단한다.

---

## Ⅳ. 특징

| 구분 | Offline Evaluation | Online Evaluation | 수치 기준 |
|:---|:---|:---|:---|
| 평가 데이터 | 고정 테스트셋 | 실제 사용자 트래픽 | 실험군 n 확보 |
| 평가 지표 | accuracy, F1, NDCG | CTR, conversion, retention, latency | p-value 0.05 등 |
| 위험 | 사용자 영향 없음 | 사용자 영향 발생 | rollback 조건 필요 |

> 요약: 온라인 평가는 실제 사용자 가치 확인이 가능하지만 실험 설계와 안전 통제가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 목적 | offline은 후보 선별 | online은 운영 가치 검증 | 사용자 행동 영향이 핵심이면 online |
| 비용/성능 | 테스트셋 평가 비용 낮음 | 실험 운영·로그 비용 발생 | 트래픽 규모와 리스크 판단 |
| 운영/위험 | 사용자 영향 없음 | guardrail·rollback 필요 | 민감 업무는 shadow 후 online |

> 요약: 온라인 평가는 최종 채택 판단에 쓰고, 오프라인 평가는 후보 모델 필터링에 쓴다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 표본 편향 | 임의 배정 실패 | random bucket, segment balance 점검 | segment별 비율 |
| 지표 왜곡 | 클릭 증가가 만족도 하락 동반 | guardrail metric 추가 | complaint rate, retention |
| 윤리 위험 | 민감 사용자 노출 | 사전 검토, 제외군 설정 | incident count |

> 요약: 온라인 평가 리스크는 표본 편향, 지표 왜곡, 윤리 위험이며 실험 설계와 guardrail로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 사업 지표 | CTR 3% 개선 또는 conversion 1% 개선 | A/B dashboard |
| 운영 지표 | p95 latency 120ms 이하 | APM |
| 안전 지표 | complaint rate 증가 0.2%p 이하 | CS 로그, 신고 로그 |

> 요약: 온라인 평가 채택은 사업 지표, 운영 지표, 안전 지표가 동시에 기준을 만족할 때 가능하다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 실험 전 primary metric, guardrail metric, 최소 표본 수, 종료 조건을 문서화함.
2. model_id, experiment_id, user_bucket을 로그에 포함해 지표 산출과 사후 분석을 가능하게 함.
3. p95 latency 120ms 초과, error rate 0.1% 초과, complaint rate 0.2%p 증가 시 실험을 중단함.

**결론 (2줄):**
- 기술사 판단: 모델 채택 결정은 offline score가 아니라 online metric과 guardrail metric을 함께 만족할 때 수행함.
- 향후 방향: 온라인 평가는 continuous evaluation, feature flag, causal inference 기반 실험 플랫폼으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "온라인 평가를 설명하시오" | 실험 배정과 지표 산출 흐름 | offline 평가와 차이 |
| 요구사항 명시형 | "모델 평가 체계를 설계하시오" | metric pipeline과 decision gate | guardrail·rollback·윤리 통제 |

> 요약: 설명형은 실사용 평가 구조를, 설계형은 실험 통제와 안전 지표를 중심으로 작성한다.
